# Map jobs for a guide, using the area plan (areas.json): which data each map uses and what it shows.
import json, sys
key = sys.argv[1]
from plan_areas import sets, split_far, bnd
A = json.load(open('/home/claude/gmap/areas.json')); G = json.load(open(f'/home/claude/ecpdf/geo-{key}.json'))
COUNTRIES = [('Netherlands',52.25,5.55),('Belgium',50.55,4.55),('Luxembourg',49.78,6.05),('France',48.9,3.0),('Germany',50.9,9.6),
             ('Germany',48.75,12.3),('Austria',47.45,14.2),('Switzerland',46.8,8.2),('Czechia',49.8,14.9),('Italy',46.4,11.6)]
D, S = sets(key); J = []
for name, pts in S:
    a = A[f'{key}-{name}']; keep, off = split_far(pts)
    w, s, e, n = a['view']
    labels = [{'name': c, 'lat': la, 'lon': lo, 'kind': 'country'} for c, la, lo in COUNTRIES if a['tier'] in ('ne', 'wide') and w < lo < e and s < la < n]
    J.append({'area': ('ne-' if a['tier'] == 'ne' else '') + f'{key}-{name}', 'w': 900, 'h': 560, 'ratio': 2, 'maxZoom': 13.5,
              'sites': [{'n': p['n'], 'lat': p['lat'], 'lon': p['lon']} for p in keep], 'route': name.startswith('day') or name == 'tl',
              'bounds': bnd(keep), 'labels': labels, 'towns': G['TOWNS'], 'out': f'/home/claude/ecpdf/gmaps/{key}-{name}.jpg', 'off': [p['n'] for p in off]})
json.dump(J, open(f'/home/claude/gmap/jobs-{key}.json', 'w'))
json.dump({j['out'].split('/')[-1]: j['off'] for j in J}, open(f'/home/claude/ecpdf/gmaps/{key}-off.json', 'w'))
print(key, [(j['area'], len(j['sites']), j['off']) for j in J])
