# Print-quality area maps for the Spanish Civil War PDFs, step 1: the frame of each area map
# (all its sites inside, 560x380 at 4x sharpness) and the road-map drawing jobs (saved OpenStreetMap data).
import json, math, os
H0 = '/home/claude/spanish-civil-war'; W_ = f'{H0}/build/pdfmaps/work'
s = open(f'{H0}/app/index.html').read(); i = s.index('window.SCW=')
D, _ = json.JSONDecoder().raw_decode(s[i + len('window.SCW='):])
merc = lambda la: math.degrees(math.log(math.tan(math.pi / 4 + math.radians(la) / 2)))
imerc = lambda y: math.degrees(math.atan(math.sinh(math.radians(y))))
W, H, PADX, PADT, PADB = 560, 380, 34, 58, 34
for n, st in enumerate(D['stops']): st['no'] = n + 1
plans, jobs = {}, []
for r in D['regions']:
    S = [x for x in D['stops'] if x['r'] == r['id']]
    w, e = min(x['lo'] for x in S), max(x['lo'] for x in S); s_, n_ = merc(min(x['la'] for x in S)), merc(max(x['la'] for x in S))
    sc = min((W - 2 * PADX) / max(e - w, .02), (H - PADT - PADB) / max(n_ - s_, .02))
    sc = min(sc, 512 * 2 ** 9 / 360)   # never closer than zoom 9
    cx = (w + e) / 2; cy = (s_ + n_) / 2 + (PADT - PADB) / 2 / sc
    z = math.log2(sc * 360 / 512); fz = math.floor(z); src = 6
    plans[r['id']] = dict(cx=cx, cy=cy, sc=sc, W=W, H=H, z=z, stops=[[x['no'], x['la'], x['lo']] for x in S])
    jobs.append({'w': W, 'h': H, 'ratio': 4, 'center': [cx, imerc(cy)], 'zoom': z, 'textScale': 1.35, 'png': True,
                 'shift': max(0, src - fz), 'srcMax': src, 'labels': [], 'out': f'{W_}/base-{r["id"]}.png'})
json.dump(plans, open(f'{W_}/plans.json', 'w')); json.dump(jobs, open(f'{W_}/jobs.json', 'w'))
print({k: round(v['z'], 2) for k, v in plans.items()})
