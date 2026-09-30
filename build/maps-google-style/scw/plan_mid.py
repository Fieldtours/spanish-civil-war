# Middle tier (like the Easy Company overview level, ~1,400 px/degree): stops within 40 km grouped, box = stops ±0.2°.
import json, math
G = json.load(open('/home/claude/gmap/scw/groups-close.json'))
d = json.load(open('/home/claude/scwmap/scw.json'))
def merc(l): return math.degrees(math.log(math.tan(math.pi/4 + math.radians(l)/2)))
def km(a, b): return math.hypot((a[0]-b[0])*111.2, (a[1]-b[1])*111.2*math.cos(math.radians(a[0])))
P = [(s['la'], s['lo'], s['id']) for s in d['stops']]
C = [[p] for p in P]; ch = True
while ch:
    ch = False
    for i in range(len(C)):
        for j in range(i+1, len(C)):
            if min(km(a, b) for a in C[i] for b in C[j]) < 40: C[i] += C[j]; del C[j]; ch = True; break
        if ch: break
C.sort(key=lambda c: -sum(p[0] for p in c)/len(c)); RES = 1400
for n, c in enumerate(C):
    la0 = min(p[0] for p in c) - .2; la1 = max(p[0] for p in c) + .2; lo0 = min(p[1] for p in c) - .26; lo1 = max(p[1] for p in c) + .26
    b = [round(lo0, 4), round(la0, 4), round(lo1, 4), round(la1, 4)]
    G.append({'id': f'm{n+1:02d}', 'b': b, 'stops': [p[2] for p in c], 'tier': 'mid', 'w': round((b[2]-b[0])*RES), 'h': round((merc(b[3])-merc(b[1]))*RES)})
json.dump(G, open('/home/claude/gmap/scw/groups.json', 'w'), indent=0)
print(len(G), 'groups;', sum(1 for g in G if g.get('tier') == 'mid'), 'middle')
