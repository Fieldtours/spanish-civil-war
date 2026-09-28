# Plan and cut the app's offline map pictures: every existing map area (RGROUPS) at its own size (level 0)
# plus smaller levels (1/2, 1/4, ...) drawn at a lower zoom so place names stay readable when zoomed out.
import json, math, re, sys, os
PR = 1.5          # drawing scale (text/lines drawn 1.5x per pixel)
def merc(lat): return math.log(math.tan(math.pi/4 + math.radians(lat)/2))
def imerc(y): return math.degrees(2*math.atan(math.exp(y)) - math.pi/2)
def groups(app_html):
    s = open(app_html).read()
    return json.loads(re.search(r'const RGROUPS=(\[.*?\]);', s).group(1))
def levels(G, minw=640):
    out = []
    for g, grp in enumerate(G):
        W, H = grp['w'], grp['h']; L = 0
        while True:
            w, h = round(W / 2**L), round(H / 2**L)
            out.append({'g': g, 'lv': L, 'b': grp['b'], 'w': w, 'h': h})
            if max(w, h) / 2 < minw or L >= 4: break
            L += 1
    return out
def job(lvl, area, png, textScale=1.35, labels=None):
    w0, s0, e0, n0 = lvl['b']
    cw, ch = lvl['w'] / PR, lvl['h'] / PR
    z = math.log2(cw * 360 / ((e0 - w0) * 512))
    cy = imerc((merc(s0) + merc(n0)) / 2)
    return {'area': area, 'w': round(cw), 'h': round(ch), 'ratio': PR, 'sites': [], 'route': False, 'center': [(w0+e0)/2, cy], 'zoom': z,
            'bounds': [[w0, s0], [e0, n0]], 'labels': labels or [], 'towns': [], 'textScale': textScale, 'out': png, 'png': True}
def cut(png, lvl, prefix, outdir):
    from PIL import Image
    im = Image.open(png).convert('RGB').resize((lvl['w'], lvl['h']), Image.LANCZOS)
    w0, s0, e0, n0 = lvl['b']; ms, mn = merc(s0), merc(n0)
    ents = []
    for r in range(math.ceil(lvl['h'] / 1024)):
        for c in range(math.ceil(lvl['w'] / 1024)):
            x0, y0 = c*1024, r*1024; x1, y1 = min(x0+1024, lvl['w']), min(y0+1024, lvl['h'])
            src = f"maps/{prefix}-z{lvl['g']}{'b' if lvl['lv']<0 else lvl['lv']}-{r}-{c}.jpg"
            im.crop((x0, y0, x1, y1)).save(os.path.join(outdir, os.path.basename(src)), quality=78, optimize=True, progressive=True)
            b = [round(w0 + (e0-w0)*x0/lvl['w'], 6), round(imerc(mn - (mn-ms)*y1/lvl['h']), 6), round(w0 + (e0-w0)*x1/lvl['w'], 6), round(imerc(mn - (mn-ms)*y0/lvl['h']), 6)]
            ents.append({'b': b, 'w': x1-x0, 'h': y1-y0, 'g': lvl['g'], 'lv': lvl['lv'], 'src': src})
    return ents

def chunk_jobs(lvl, area, stem, labels=None, textScale=1.35, CH=2048, PAD=256):
    """Split one level into overlapping pieces (drawn separately, then stitched)."""
    w0, s0, e0, n0 = lvl['b']; ms, mn = merc(s0), merc(n0); W, H = lvl['w'], lvl['h']
    lon = lambda x: w0 + (e0-w0)*x/W
    my = lambda y: mn - (mn-ms)*y/H
    z = math.log2((W/PR) * 360 / ((e0 - w0) * 512))
    out = []
    for r in range(math.ceil(H/CH)):
        for c in range(math.ceil(W/CH)):
            x0, y0 = c*CH, r*CH; x1, y1 = min(x0+CH, W), min(y0+CH, H)
            X0, Y0, X1, Y1 = x0-PAD, y0-PAD, x1+PAD, y1+PAD
            cx = lon((X0+X1)/2); cy = imerc(my((Y0+Y1)/2))
            out.append({'area': area, 'w': round((X1-X0)/PR), 'h': round((Y1-Y0)/PR), 'ratio': PR, 'sites': [], 'route': False,
                        'center': [cx, cy], 'zoom': z, 'bounds': [[w0, s0], [e0, n0]], 'labels': labels or [], 'towns': [],
                        'textScale': textScale, 'png': True, 'out': f'{stem}-{r}-{c}.png', 'box': [x0, y0, x1, y1], 'pad': PAD})
    return out
def stitch(jobs, lvl, png):
    from PIL import Image
    full = Image.new('RGB', (lvl['w'], lvl['h']), '#f5f3ee')
    for j in jobs:
        im = Image.open(j['out']).convert('RGB'); x0, y0, x1, y1 = j['box']; P = j['pad']
        sx = im.width / (x1-x0+2*P); sy = im.height / (y1-y0+2*P)
        piece = im.crop((round(P*sx), round(P*sy), round((P+x1-x0)*sx), round((P+y1-y0)*sy))).resize((x1-x0, y1-y0))
        full.paste(piece, (x0, y0))
    full.save(png)
