# Turn an OpenStreetMap extract (.osm.pbf) into small GeoJSON layers for a Google-style road map.
# usage: python3 extract_osm.py <file.osm.pbf> <outdir> W S E N  [seed_lat,seed_lon ...]
import sys, json, osmium, os
from shapely.geometry import LineString, Polygon, MultiPolygon, box, Point, mapping, shape
from shapely.ops import linemerge, split, unary_union
from shapely import wkb as swkb
pbf, out = sys.argv[1], sys.argv[2]
W, S, E, N = map(float, sys.argv[3:7])
seeds = [tuple(map(float, s.split(','))) for s in sys.argv[7:]]
BB = box(W, S, E, N)
os.makedirs(out, exist_ok=True)
fab = osmium.geom.WKBFactory()
ROADS = {'motorway':0,'motorway_link':0,'trunk':1,'trunk_link':1,'primary':2,'primary_link':2,'secondary':3,'secondary_link':3,
         'tertiary':4,'tertiary_link':4,'unclassified':5,'residential':6,'living_street':6}
L = {k: [] for k in ['roads','rail','rivers','water','wood','wetland','urban','places','coast']}
def inside(g): return g.intersects(BB)
def geom_way(w):
    try: return swkb.loads(fab.create_linestring(w), hex=True)
    except Exception: return None
class H(osmium.SimpleHandler):
    def node(self, n):
        p = n.tags.get('place')
        if p in ('city','town','village','hamlet','suburb') and 'name' in n.tags:
            if W <= n.location.lon <= E and S <= n.location.lat <= N:
                pop = n.tags.get('population','')
                L['places'].append({'type':'Feature','geometry':{'type':'Point','coordinates':[round(n.location.lon,5),round(n.location.lat,5)]},
                    'properties':{'name':n.tags['name'],'place':p,'pop':int(pop) if pop.isdigit() else 0}})
    def way(self, w):
        t = w.tags; hw = t.get('highway')
        if hw in ROADS:
            g = geom_way(w)
            if g is not None and inside(g):
                L['roads'].append((g, {'c':ROADS[hw],'ref':t.get('ref',''),'name':t.get('name','')}))
        elif t.get('railway') == 'rail' and t.get('service') is None:
            g = geom_way(w)
            if g is not None and inside(g): L['rail'].append((g, {}))
        elif t.get('waterway') in ('river','canal'):
            g = geom_way(w)
            if g is not None and inside(g): L['rivers'].append((g, {'name':t.get('name',''),'w':t.get('waterway')}))
        elif t.get('natural') == 'coastline':
            g = geom_way(w)
            if g is not None and g.intersects(BB.buffer(0.3)): L['coast'].append(g)
    def area(self, a):
        t = a.tags; k = None
        if t.get('natural') == 'water' or t.get('waterway') == 'riverbank' or t.get('landuse') == 'reservoir': k = 'water'
        elif t.get('landuse') == 'forest' or t.get('natural') == 'wood': k = 'wood'
        elif t.get('natural') == 'wetland': k = 'wetland'
        elif t.get('landuse') in ('residential','industrial','commercial','retail'): k = 'urban'
        if not k: return
        try: g = swkb.loads(fab.create_multipolygon(a), hex=True)
        except Exception: return
        if g.area < 2e-6 and k != 'water': return   # skip tiny patches
        if inside(g): L[k].append((g, {}))
for f in pbf.split(','):
    H().apply_file(f, locations=True, idx='flex_mem')
def dump(name, items, tol):
    fs = []
    for g, p in items:
        g = g.intersection(BB).simplify(tol, preserve_topology=True)
        if g.is_empty: continue
        fs.append({'type':'Feature','geometry':mapping(g),'properties':p})
    json.dump({'type':'FeatureCollection','features':fs}, open(f'{out}/{name}.geojson','w'), separators=(',',':'))
    print(name, len(fs))
for k, tol in [('roads',0.00008),('rail',0.0001),('rivers',0.0001),('water',0.00008),('wood',0.00015),('wetland',0.00015),('urban',0.0001)]:
    dump(k, L[k], tol)
json.dump({'type':'FeatureCollection','features':L['places']}, open(f'{out}/places.geojson','w'), separators=(',',':'))
print('places', len(L['places']))
# sea: split the box along the coastline, keep the pieces that hold a sea seed point
sea = []
if L['coast']:
    lines = linemerge(unary_union(L['coast']))
    pieces = split(BB, lines) if not lines.is_empty else [BB]
    for pc in getattr(pieces, 'geoms', [pieces]):
        if any(pc.contains(Point(lo, la)) for la, lo in seeds): sea.append(pc)
dump('sea', [(g, {}) for g in sea], 0.00005)
