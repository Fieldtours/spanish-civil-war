# Map layers for wide overview maps (a whole region or country) from Natural Earth open data.
# usage: python3 from_ne.py <outdir> W S E N
import sys, json, os
from shapely.geometry import shape, box, mapping
from shapely.ops import unary_union
out = sys.argv[1]; W, S, E, N = map(float, sys.argv[2:6])
BB = box(W, S, E, N); os.makedirs(out, exist_ok=True)
def feats(n):
    for f in json.load(open(f'/home/claude/ne/{n}.geojson'))['features']:
        if f['geometry'] is None: continue
        g = shape(f['geometry'])
        if g.intersects(BB): yield g.intersection(BB), f['properties']
def dump(name, items):
    fs = [{'type':'Feature','geometry':mapping(g),'properties':p} for g, p in items if not g.is_empty]
    json.dump({'type':'FeatureCollection','features':fs}, open(f'{out}/{name}.geojson','w'), separators=(',',':')); return len(fs)
roads = []
for g, p in feats('ne_10m_roads'):
    t = p.get('type', '')
    if 'Ferry' in t or t in ('Track', 'Unknown'): continue
    c = 0 if p.get('expressway') == 1 else 2 if t == 'Major Highway' else 3 if t == 'Secondary Highway' else 4
    ref = (p.get('local') or p.get('label') or '').split(' ')[0]
    if not any(ch.isalpha() for ch in ref): ref = ''   # a bare number would look like one of our site numbers
    roads.append((g, {'c': c, 'ref': ref, 'name': ''}))
places = []
for g, p in feats('ne_10m_populated_places_simple'):
    pop = int(p.get('pop_max') or 0)
    places.append((g, {'name': p['name'], 'place': 'city' if (p.get('scalerank', 9) <= 4 or pop >= 250000) else 'town' if pop >= 30000 else 'village', 'pop': pop}))
rivers = [(g, {'name': p.get('name') or '', 'w': 'river'}) for n in ('ne_10m_rivers_lake_centerlines', 'ne_10m_rivers_europe') for g, p in feats(n)]
water = [(g, {}) for n in ('ne_10m_lakes', 'ne_10m_lakes_europe') for g, p in feats(n)]
urban = [(g, {}) for g, p in feats('ne_10m_urban_areas')]
land = unary_union([g for g, p in feats('ne_10m_land')] + [g for g, p in feats('ne_10m_minor_islands')])
sea = BB.difference(land)
borders = [(g, {}) for g, p in feats('ne_10m_admin_0_boundary_lines_land')]
n = {'roads': dump('roads', roads), 'places': dump('places', places), 'rivers': dump('rivers', rivers), 'water': dump('water', water),
     'urban': dump('urban', urban), 'sea': dump('sea', [(sea, {})]), 'borders': dump('borders', borders)}
for k in ('wood', 'wetland', 'rail'): dump(k, [])
print(out, n)
