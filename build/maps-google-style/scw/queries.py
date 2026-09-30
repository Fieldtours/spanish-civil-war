import json
G = json.load(open('groups.json'))
HW = 'motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified'
def q(b, parts):
    w, s, e, n = b; mx = (e-w)*.02; my = (n-s)*.02
    return f'[out:json][timeout:600][maxsize:1073741824][bbox:{s-my:.4f},{w-mx:.4f},{n+my:.4f},{e+mx:.4f}];(' + ''.join(parts) + ');out geom qt;'
DET = [f'way[highway~"^({HW})$"];', 'way[railway=rail][!service];', 'way[waterway~"^(river|canal)$"];', 'way[natural=water];', 'relation[natural=water];',
       'way[landuse=reservoir];', 'relation[landuse=reservoir];', 'way[landuse=forest];', 'relation[landuse=forest];', 'way[natural=wood];', 'relation[natural=wood];',
       'way[landuse~"^(residential|industrial|commercial|retail)$"];', 'way[natural=wetland];', 'way[natural=coastline];',
       'node[place~"^(city|town|village|hamlet|suburb)$"];']
Q = {}
for g in G[1:]:
    w, s, e, n = g['b']
    if (e-w)*(n-s) > 0.12:   # big areas: fetch in 4 parts
        mw, mn = (w+e)/2, (s+n)/2
        for i, bb in enumerate([[w, s, mw, mn], [mw, s, e, mn], [w, mn, mw, n], [mw, mn, e, n]]): Q[f"{g['id']}-{i}"] = q(bb, DET)
    else: Q[g['id']] = q(g['b'], DET)
# Spain overview: towns, and the main roads (in 6 parts)
w, s, e, n = G[0]['b']
Q['spain-places'] = q(G[0]['b'], ['node[place~"^(city|town)$"];'])
xs = [w, -5.5, -1.0, e]; ys = [s, 40.0, n]
k = 0
for i in range(3):
    for j in range(2):
        Q[f'spain-roads-{k}'] = q([xs[i], ys[j], xs[i+1], ys[j+1]], ['way[highway~"^(motorway|trunk|primary)$"];']); k += 1
json.dump(Q, open('queries.json', 'w'))
print(len(Q), 'queries')
