# usage: python3 make_tiles.py <app> <prefix> <area-for-g0,area-for-g1,...>  -> renders every level, cuts tiles, writes raster list
import sys, json, subprocess, os, math
sys.path.insert(0, '/home/claude/gmap'); from tiles import *
app, prefix, areas = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
G = groups(f'/home/claude/ecp/test/{app}.html'); L = levels(G)
labels = []
if False and app == 'normandy':
    geo = json.load(open('/home/claude/ecpdf/geo-normandy.json'))
    labels = [{'name': n.title() + ' Beach', 'lat': a + 0.045, 'lon': o, 'kind': 'sea'} for n, a, o in geo['REGIONS']]
only = os.environ.get('ONLY')
L = L + [dict(l, lv=-1) for l in L if l['g'] == 0 and l['lv'] == 0]   # names-free copy of the overview map, for stretched edges
os.makedirs('/home/claude/gmap/png/parts', exist_ok=True)
for l in L:
    if only and ('b' if l['lv']<0 else f"{l['g']}{l['lv']}") not in only.split(','): continue
    stem = f"/home/claude/gmap/png/parts/{prefix}-{l['g']}{'b' if l['lv']<0 else l['lv']}"
    area = areas[l['g']]
    zl = math.log2((l['w']/PR)*360/((l['b'][2]-l['b'][0])*512))
    if zl < 10.8 and os.path.isdir(f'/home/claude/gmap/data/{area}-lo'): area += '-lo'   # lighter data for zoomed-out levels
    J = chunk_jobs(l, area, stem, labels=labels)
    if l['lv'] < 0:
        for j in J: j['bare'] = True
    json.dump(J, open(f'/home/claude/gmap/jobs-tiles-{prefix}.json', 'w'))
    subprocess.run(['node', 'shoot.js', f'jobs-tiles-{prefix}.json'], cwd='/home/claude/gmap', env=dict(os.environ, NODE_PATH='/opt/node-tools/node_modules'))
    stitch(J, l, f"/home/claude/gmap/png/{prefix}-{l['g']}{'b' if l['lv']<0 else l['lv']}.png")
out = f'/home/claude/gmap/tiles/{prefix}'; os.makedirs(out, exist_ok=True); R = []
for l in L:
    png = f"/home/claude/gmap/png/{prefix}-{l['g']}{'b' if l['lv']<0 else l['lv']}.png"
    if os.path.exists(png): R += cut(png, l, prefix, out)
json.dump(R, open(f'{out}/raster.json', 'w'))
print(prefix, len(R), 'tiles')
