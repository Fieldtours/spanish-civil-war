# Turn the Overpass downloads for one close-up area (1 or 4 parts, gzipped) into map layers, with the sea cut along the OSM coastline.
# usage: python3 convert.py a06   (reads osm/a06.json.gz or osm/a06-0..3.json.gz, writes /home/claude/gmap/data/scw-a06/)
import sys, json, gzip, os, glob, subprocess
from shapely.geometry import shape, box, LineString, Point, mapping
from shapely.ops import linemerge, unary_union, split, polygonize
k = sys.argv[1]; D = '/home/claude/gmap/scw'
G = {g['id']: g for g in json.load(open(f'{D}/groups.json'))}
parts = sorted(glob.glob(f'{D}/osm/{k}.json.gz') + glob.glob(f'{D}/osm/{k}-[0-3].json.gz'))
assert parts, k
seen = set(); E = []
for p in parts:
    for e in json.load(gzip.open(p))['elements']:
        key = (e['type'], e['id'])
        if key in seen: continue
        seen.add(key); E.append(e)
tmp = f'{D}/osm/{k}-merged.json'; json.dump({'elements': E}, open(tmp, 'w'))
out = f'/home/claude/gmap/data/scw-{k}'
subprocess.run(['python3', '/home/claude/gmap/from_overpass.py', tmp, out], check=True)
os.remove(tmp)
# sea: split the area box along the coastline; pieces mostly in Natural Earth's sea are sea
w, s, e, n = G[k]['b']; BB = box(w, s, e, n)
coast = [LineString([(p['lon'], p['lat']) for p in x['geometry']]) for x in E if x['type'] == 'way' and x.get('tags', {}).get('natural') == 'coastline' and len(x.get('geometry', [])) > 1]
sea = []
if coast:
    nesea = shape(json.load(open('/home/claude/gmap/data/spain-ne/sea.geojson'))['features'][0]['geometry'])
    lines = unary_union([linemerge(unary_union(coast)).intersection(BB), BB.exterior])
    for pc in polygonize(lines):
        if not pc.within(BB.buffer(1e-9)) or pc.area < 1e-7: continue
        pt = pc.representative_point()
        if nesea.contains(pt) or nesea.intersection(pc).area > 0.6 * pc.area: sea.append(pc)
json.dump({'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'geometry': mapping(g.simplify(0.00005)), 'properties': {}} for g in sea]},
          open(f'{out}/sea.geojson', 'w'), separators=(',', ':'))
print(k, 'parts', len(parts), 'elements', len(E), 'coast', len(coast), 'sea pieces', len(sea))
