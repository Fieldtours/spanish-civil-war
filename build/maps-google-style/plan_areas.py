# Work out, for each map of a guide, what the map will show (so we fetch data for exactly that area),
# and whether it is a close-up (detailed OpenStreetMap), a mid-range map, or a wide overview (Natural Earth).
import json, math, sys
W, H, PAD, MAXZ = 900, 560, 70, 13.5
def merc(lat): return math.log(math.tan(math.pi/4 + math.radians(lat)/2))
def imerc(y): return math.degrees(2*math.atan(math.exp(y)) - math.pi/2)
def view(b):
    (w, s), (e, n) = b
    dx = math.radians(e - w) or 1e-6; dy = (merc(n) - merc(s)) or 1e-6
    z = min(math.log2((W-2*PAD) / dx * 2*math.pi / 512), math.log2((H-2*PAD) / dy * 2*math.pi / 512), MAXZ)
    scale = 512 * 2**z / (2*math.pi)          # px per radian
    cx = (w+e)/2; cy = (merc(s)+merc(n))/2
    hw = math.degrees(W/2/scale); hh = H/2/scale
    return z, [cx-hw, imerc(cy-hh), cx+hw, imerc(cy+hh)]
def sets(key):
    D = json.load(open(f'/home/claude/ecpdf/{key}.json'))
    S = [('day%d' % d['n'], [dict(s, n=i+1) for i, s in enumerate(d['stops'])]) for d in D['days']]
    if D['extra']: S.append(('extra', [dict(s, n=i+1) for i, s in enumerate(D['extra'])]))
    S += [('tl', D['tl']), ('dd', [dict(s, n=i+1) for i, s in enumerate(D['dd'])]), ('mus', [dict(s, n=i+1) for i, s in enumerate(D['mus'])])]
    return D, S
def bnd(ps): return [[min(p['lon'] for p in ps), min(p['lat'] for p in ps)], [max(p['lon'] for p in ps), max(p['lat'] for p in ps)]]
def split_far(pts):
    """Leave a far-away site off the map (listed as 'off this map') when that lets the map zoom in a lot."""
    keep = list(pts); off = []
    while len(keep) > 2:
        la = sorted(p['lat'] for p in keep)[len(keep)//2]; lo = sorted(p['lon'] for p in keep)[len(keep)//2]
        far = max(keep, key=lambda p: math.hypot(p['lat']-la, (p['lon']-lo)*0.65))
        rest = [p for p in keep if p is not far]
        if view(bnd(rest))[0] - view(bnd(keep))[0] >= 1.5 and len(off) + 1 <= 0.34 * len(pts):
            keep = rest; off.append(far)
        else: break
    return keep, off
if __name__ == '__main__':
    out = {}
    for key in sys.argv[1:]:
        D, S = sets(key)
        for name, pts in S:
            keep, off = split_far(pts)
            b = bnd(keep)
            z, v = view(b)
            tier = 'detail' if z >= 10.3 else 'mid' if z >= 8.6 else 'wide' if z >= 7 else 'ne'
            out[f'{key}-{name}'] = {'zoom': round(z, 2), 'tier': tier, 'view': [round(x, 4) for x in v], 'off': [p['n'] for p in off], 'bounds': b}
            print(f'{key}-{name}', round(z, 2), tier, [round(x, 3) for x in v], 'off', [p['n'] for p in off])
    json.dump(out, open('/home/claude/gmap/areas.json', 'w'), indent=1)
