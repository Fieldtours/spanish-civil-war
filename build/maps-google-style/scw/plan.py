# Plan the Spanish Civil War app maps: a Spain overview (g0) plus close-up areas around every group of sites.
import json, math
d = json.load(open('/home/claude/scwmap/scw.json'))
def merc(l): return math.degrees(math.log(math.tan(math.pi/4 + math.radians(l)/2)))
def km(a, b): return math.hypot((a[0]-b[0])*111.2, (a[1]-b[1])*111.2*math.cos(math.radians(a[0])))
P = [(s['la'], s['lo'], s['id']) for s in d['stops']]
C = [[p] for p in P]; ch = True
while ch:
    ch = False
    for i in range(len(C)):
        for j in range(i+1, len(C)):
            if min(km(a, b) for a in C[i] for b in C[j]) < 15:
                C[i] += C[j]; del C[j]; ch = True; break
        if ch: break
RES0, RES = 600, 4550        # pixels per degree of longitude: overview, close-up (Easy Company close-up level)
G = [{'id': 'spain', 'b': [-9.9, 35.6, 4.6, 44.1]}]
C.sort(key=lambda c: (-sum(p[0] for p in c)/len(c)))
for n, c in enumerate(C):
    la0 = min(p[0] for p in c) - .07; la1 = max(p[0] for p in c) + .07
    lo0 = min(p[1] for p in c) - .09; lo1 = max(p[1] for p in c) + .09
    G.append({'id': f'a{n+1:02d}', 'b': [round(lo0, 4), round(la0, 4), round(lo1, 4), round(la1, 4)], 'stops': [p[2] for p in c]})
tot = 0
for g in G:
    r = RES0 if g['id'] == 'spain' else RES; w0, s0, e0, n0 = g['b']
    g['w'] = round((e0-w0)*r); g['h'] = round((merc(n0)-merc(s0))*r); tot += g['w']*g['h']
json.dump(G, open('groups.json', 'w'), indent=0)
print(len(G), 'groups', round(tot/1e6), 'Mpx at full detail')
for g in G[:6] + sorted(G, key=lambda g: -g['w']*g['h'])[:6]: print(g['id'], g['w'], g['h'], len(g.get('stops', [])))
