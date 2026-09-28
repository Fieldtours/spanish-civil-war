# Overpass queries for each map area (run in the browser on JC's Mac; the results come back as JSON files).
import json
A = json.load(open('/home/claude/gmap/areas.json'))
HW = {'detail': 'motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified',
      'mid': 'motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link',
      'wide': 'motorway|trunk|primary|secondary'}
def q(k, a):
    w, s, e, n = a['view']; mx = (e-w)*.03; my = (n-s)*.03
    bb = f'{s-my:.4f},{w-mx:.4f},{n+my:.4f},{e+mx:.4f}'
    t = a['tier']; hw = HW[t] + ('|residential|living_street' if a['zoom'] >= 12.4 else '')
    parts = [f'way[highway~"^({hw})$"];']
    if t != 'wide':
        parts += ['way[railway=rail][!service];', 'way[waterway~"^(river|canal)$"];', 'way[natural=water];', 'relation[natural=water];',
                  'way[landuse=forest];', 'relation[landuse=forest];', 'way[natural=wood];', 'relation[natural=wood];',
                  'way[landuse~"^(residential|industrial|commercial|retail)$"];']
        if t == 'detail': parts += ['way[natural=wetland];']
        parts += ['node[place~"^(city|town|village|hamlet|suburb)$"];' if t == 'detail' else 'node[place~"^(city|town|village)$"];']
    else:
        parts += ['way[waterway=river];', 'relation[natural=water][name];', 'way[natural=water][name];', 'node[place~"^(city|town|village)$"];']
    return f'[out:json][timeout:300][bbox:{bb}];(' + ''.join(parts) + ');out geom qt;'
Q = {k: q(k, a) for k, a in A.items() if a['tier'] in ('detail', 'mid', 'wide') and not k.startswith('normandy')}
json.dump(Q, open('/home/claude/gmap/queries.json', 'w'), indent=1)
for k, v in Q.items(): print(k, A[k]['tier'], len(v))
