# New sw.js: same as before, plus the map pictures (their own cache "scw-maps", saved with "Save for offline").
import json, re, hashlib, sys
old, html, raster, out = sys.argv[1:5]
s = open(old).read(); R = json.load(open(raster))
core = json.loads(re.search(r'CORE=(\[.*?\]);', s).group(1))
g0 = [r for r in R if r['g'] == 0 and r['lv'] >= 0]; top = max(r['lv'] for r in g0)
base = [r['src'] for r in g0 if r['lv'] == top]             # the small overview picture: kept from the first visit
maps = [r['src'] for r in R if r['src'] not in base]
ver = hashlib.md5(open(html, 'rb').read()).hexdigest()[:8]
s = re.sub(r'const V="scw-core-[0-9a-f]+", CORE=\[.*?\];', 'const V="scw-core-%s", MC="scw-maps", CORE=%s, MAPS=%s;' % (ver, json.dumps(core + base), json.dumps(maps)), s, count=1)
def rep(a, b):
    global s; assert s.count(a) == 1, a; s = s.replace(a, b)
rep('k!==V&&k!=="scw-data"', 'k!==V&&k!=="scw-data"&&k!==MC')
rep('const ALL=CORE.concat(["pdf/The-Spanish-Civil-War-field-guide.pdf"]);\n  caches.open(V).then(async c=>{let n=0;for(const f of ALL){try{const r=await fetch(f,{cache:"no-store"});if(r.ok)await c.put(f,r)}catch(err){}n++;port&&port.postMessage({n,of:ALL.length})}port&&port.postMessage({done:true})})',
    'const ALL=CORE.concat(["pdf/The-Spanish-Civil-War-field-guide.pdf"]).concat(MAPS);\n  Promise.all([caches.open(V),caches.open(MC)]).then(async([c,m])=>{let n=0;for(const f of ALL){try{const x=/^maps\\//.test(f)?m:c;if(!(x===m&&await m.match(f))){const r=await fetch(f,{cache:"no-store"});if(r.ok)await x.put(f,r)}}catch(err){}n++;if(n%10===0||n===ALL.length)port&&port.postMessage({n,of:ALL.length})}port&&port.postMessage({done:true})})')
rep('if(res.ok&&!/\\/pdf\\//.test(u.pathname)){const c=res.clone();caches.open(V).then(x=>x.put(req,c))}',
    'if(res.ok&&!/\\/pdf\\//.test(u.pathname)){const c=res.clone();caches.open(/\\/maps\\//.test(u.pathname)?MC:V).then(x=>x.put(req,c))}')
open(out, 'w').write(s); print('sw ok', len(core), len(base), len(maps), ver)
