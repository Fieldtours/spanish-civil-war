# Build the list of maps for one guide's PDF from the extracted guide data.
import json, math, sys
key, area = sys.argv[1], sys.argv[2]
D = json.load(open(f'/home/claude/ecpdf/{key}.json')); G = json.load(open(f'/home/claude/ecpdf/geo-{key}.json')) if key=='normandy' else {}
beaches = [{'name': n.title() + ' Beach', 'lat': a + 0.045, 'lon': o} for n, a, o in G.get('REGIONS', [])]
def far(pts):
    la = sorted(p['lat'] for p in pts)[len(pts)//2]; lo = sorted(p['lon'] for p in pts)[len(pts)//2]
    return [p for p in pts if math.hypot(p['lat']-la, (p['lon']-lo)*0.65) > 1.2]
def job(name, pts, route, labels=True):
    off = far(pts); keep = [p for p in pts if p not in off]
    la = [p['lat'] for p in keep]; lo = [p['lon'] for p in keep]
    b = [[min(lo), min(la)], [max(lo), max(la)]]
    lab = [l for l in beaches if b[0][0]-.1 < l['lon'] < b[1][0]+.1 and b[0][1]-.1 < l['lat'] < b[1][1]+.15] if labels else []
    return {'area': area, 'w': 900, 'h': 560, 'ratio': 2, 'sites': [{'n': p['n'], 'lat': p['lat'], 'lon': p['lon']} for p in keep],
            'route': route, 'bounds': b, 'labels': lab, 'maxZoom': 13.5, 'towns': G.get('TOWNS', []), 'out': f'/home/claude/ecpdf/gmaps/{key}-{name}.jpg',
            'off': [p['n'] for p in off]}
J = []
for d in D['days']: J.append(job('day%d' % d['n'], [dict(s, n=i+1) for i, s in enumerate(d['stops'])], True))
if D['extra']: J.append(job('extra', [dict(s, n=i+1) for i, s in enumerate(D['extra'])], False))
J.append(job('tl', D['tl'], True))
J.append(job('dd', [dict(s, n=i+1) for i, s in enumerate(D['dd'])], False))
J.append(job('mus', [dict(s, n=i+1) for i, s in enumerate(D['mus'])], False))
json.dump(J, open(f'/home/claude/gmap/jobs-{key}.json', 'w'))
json.dump({j['out'].split('/')[-1]: j['off'] for j in J}, open(f'/home/claude/ecpdf/gmaps/{key}-off.json', 'w'))
print([(j['out'].split('/')[-1], len(j['sites']), j['off']) for j in J])
