# Convert an Overpass JSON download into the map layers render.html draws.
# usage: python3 from_overpass.py osm-<key>.json <outdir>
import sys, json, os
from shapely.geometry import LineString, Polygon, mapping, MultiPolygon
from shapely.ops import linemerge, polygonize, unary_union
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
E = json.load(open(src))['elements']
ROADS = {'motorway':0,'motorway_link':0,'trunk':1,'trunk_link':1,'primary':2,'primary_link':2,'secondary':3,'secondary_link':3,
         'tertiary':4,'tertiary_link':4,'unclassified':5,'residential':6,'living_street':6}
L = {k: [] for k in ['roads','rail','rivers','water','wood','wetland','urban','places','sea']}
def kind(t):
    if t.get('natural') == 'water' or t.get('landuse') == 'reservoir': return 'water'
    if t.get('landuse') == 'forest' or t.get('natural') == 'wood': return 'wood'
    if t.get('natural') == 'wetland': return 'wetland'
    if t.get('landuse') in ('residential','industrial','commercial','retail'): return 'urban'
def line(g): return [(p['lon'], p['lat']) for p in g if p]
for e in E:
    t = e.get('tags', {})
    if e['type'] == 'node':
        if 'name' in t:
            pop = t.get('population', '').replace(' ', '').replace('.', '')
            L['places'].append({'type':'Feature','geometry':{'type':'Point','coordinates':[round(e['lon'],5), round(e['lat'],5)]},
                                'properties':{'name':t['name'],'place':t.get('place'),'pop':int(pop) if pop.isdigit() else 0}})
        continue
    if e['type'] == 'way':
        pts = line(e.get('geometry', []))
        if len(pts) < 2: continue
        hw = t.get('highway')
        if hw in ROADS: L['roads'].append((LineString(pts), {'c':ROADS[hw],'ref':t.get('ref','').split(';')[0],'name':t.get('name','')})); continue
        if t.get('railway') == 'rail': L['rail'].append((LineString(pts), {})); continue
        if t.get('waterway') in ('river','canal'): L['rivers'].append((LineString(pts), {'name':t.get('name',''),'w':t.get('waterway')})); continue
        k = kind(t)
        if k and len(pts) >= 4 and pts[0] == pts[-1]:
            try:
                p = Polygon(pts).buffer(0)
                if not p.is_empty: L[k].append((p, {}))
            except Exception: pass
    elif e['type'] == 'relation':
        k = kind(t)
        if not k: continue
        outer = [LineString(line(m['geometry'])) for m in e.get('members', []) if m.get('role') in ('outer', '') and m.get('geometry') and len(m['geometry']) > 1]
        inner = [LineString(line(m['geometry'])) for m in e.get('members', []) if m.get('role') == 'inner' and m.get('geometry') and len(m['geometry']) > 1]
        try:
            po = unary_union(list(polygonize(linemerge(outer)))) if outer else None
            if po is None or po.is_empty: continue
            if inner:
                pi = unary_union(list(polygonize(linemerge(inner))))
                po = po.difference(pi)
            L[k].append((po.buffer(0), {}))
        except Exception: pass
def dump(name, items, tol):
    fs = []
    for g, p in items:
        g = g.simplify(tol, preserve_topology=True)
        if g.is_empty: continue
        fs.append({'type':'Feature','geometry':mapping(g),'properties':p})
    json.dump({'type':'FeatureCollection','features':fs}, open(f'{out}/{name}.geojson','w'), separators=(',',':'))
    return len(fs)
n = {k: dump(k, L[k], tol) for k, tol in [('roads',0.00006),('rail',0.0001),('rivers',0.0001),('water',0.00006),('wood',0.0001),('wetland',0.0001),('urban',0.0001),('sea',0.0001)]}
json.dump({'type':'FeatureCollection','features':L['places']}, open(f'{out}/places.geojson','w'), separators=(',',':'))
n['places'] = len(L['places'])
if not os.path.exists(f'{out}/borders.geojson'): json.dump({'type':'FeatureCollection','features':[]}, open(f'{out}/borders.geojson','w'))
print(os.path.basename(src), n)
