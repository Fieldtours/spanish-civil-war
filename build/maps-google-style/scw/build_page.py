# Make the new index.html from the newest live copy: Google-style multi-level maps added, nothing else changed.
import json, glob, sys
sys.path.insert(0, '/home/claude/gmap/scw'); from patch_map import patch, rep
src, out = sys.argv[1], sys.argv[2]
s = open(src).read()
R = []
for f in sorted(glob.glob('/home/claude/gmap/scw/raster-*.json')): R += json.load(open(f))
R.sort(key=lambda r: (r['g'], r['lv'], r['src']))
s = rep(s, '</script>\n<script>\n/* ===== GeoMap', '</script>\n<script>\n/* map pictures: Google-style road maps at several levels of detail (Map data © OpenStreetMap contributors, Natural Earth) */\nwindow.SCW_RASTER=' + json.dumps(R, separators=(',', ':')) + ';\n</script>\n<script>\n/* ===== GeoMap')
s = patch(s)
s = rep(s, '<div class="mcap">Map: Natural Earth · numbers = sites', '<div class="mcap">Map: © OpenStreetMap · numbers = sites')
s = rep(s, '<p>Base map drawn from Natural Earth (public domain). Positions', '<p>Road maps drawn by us from OpenStreetMap data (© OpenStreetMap contributors, openstreetmap.org/copyright) and Natural Earth (public domain), in several levels of detail so village names and small roads appear as you zoom in. Positions')
open(out, 'w').write(s)
print('page ok', len(R), 'tiles', len(s))
