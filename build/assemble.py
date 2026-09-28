import re,json,os,shutil,hashlib
B='/home/claude/scw/build/';OUT='/home/claude/scw/site/'
exec(open(B+'icons_py.py').read()) if os.path.exists(B+'icons_py.py') else None
app=open(B+'app.js').read()
# pull the IC icon strings from app.js to reuse in body
IC=dict(re.findall(r"\n (\w+):'(<svg.*?</svg>)'",app))
body=open(B+'body.html').read()
for k,v in {'BACK':IC['back'],'WEAP':IC['weap'],'SEARCH':IC['search'],'NEAR':IC['near'],'TOUR':IC['tour'],'BOOK':IC['book'],'CLOUD':IC['cloud'],'DL':IC['dl'],'PIN':IC['pin'],'FLAG':IC['flag'],'BM':IC['bm'],'PEOPLE':IC['people'],'STAR':IC['star'],'DOC':IC['doc'],'MAP':IC['map'],'HOME':IC['home'],'TIME':IC['time'],'MORE':IC['more']}.items():
  body=body.replace('__'+k+'__',v)
body=body.replace('${pill}','<button type="button" class="pill-c c-HIGH" data-cert="HIGH">HIGH</button> <button type="button" class="pill-c c-MEDIUM" data-cert="MEDIUM">MEDIUM</button> <button type="button" class="pill-c c-LOW" data-cert="LOW">LOW</button>')
assert '__' not in re.sub(r'__[a-z]','',body.replace('___','')), [m for m in re.findall(r'__\w+__',body)]
css=open(B+'app.css').read()+'\n'+open(B+'bm.css').read()+'\n'+open(B+'aar-theme.css').read()+'\n'+open(B+'aar.css').read()+'''
.bmbtn{display:flex;align-items:center;gap:12px;width:100%;margin:6px 0 12px;padding:10px 14px;min-height:56px;text-align:left;cursor:pointer;background:var(--surface);color:var(--ink);border:2px solid var(--red);border-radius:12px;font-family:var(--sans);font-size:inherit}
.bmbtn svg{flex:0 0 34px;width:34px;height:34px}
.bmbtn b{display:block;font-family:var(--disp);font-weight:800;font-size:18px;letter-spacing:.8px;text-transform:uppercase;color:var(--red)}
.bmbtn span span{display:block;font-size:14px;color:var(--ink2);line-height:1.3}
.cover{background-image:url(welcome.jpg)}
@media (min-width:700px){.cover{background-image:url(welcome-wide.jpg)}}
.wel{background-image:url(welcome.jpg)}
@media (min-width:900px) and (min-aspect-ratio:5/4){.wel{background-image:url(welcome-wide.jpg)}}
'''
head='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>The Spanish Civil War 1936–1939 — DZ Charlie field guide</title>
<meta name="description" content="A free, offline phone guide to the battlefields, trenches, ruined villages, shelters, museums and memorials of the Spanish Civil War across the whole of Spain. Choose your area and your time; the guide builds the tour.">
<meta name="theme-color" content="#3d2b1f">
<meta property="og:title" content="The Spanish Civil War 1936–1939 — a DZ Charlie field guide">
<meta property="og:description" content="Free phone guide to the sites of the Spanish Civil War, told fairly from both sides. Works with no signal.">
<meta property="og:image" content="welcome-wide.jpg">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="fonts/bss-800.woff2" as="font" type="font/woff2" crossorigin>
'''
html=head+'<style>\n'+css+'\n</style>\n</head>\n<body>\n'+body+'\n<script>\n'+open(B+'data.js').read()+'\n</script>\n<script>\n'+open(B+'map.js').read()+'\n</script>\n<script>\n'+open(B+'bm.js').read()+'\n</script>\n<script>\nwindow.AAR_DATA='+open('/home/claude/scw/research/aar_data.json').read()+';\n</script>\n<script>\n'+app+'\n</script>\n<script>\n'+open(B+'aar.js').read()+'\n</script>\n</body>\n</html>\n'
os.makedirs(OUT+'fonts',exist_ok=True)
for f in ['bss-800.woff2','bss-600.woff2','bsd-700.woff2','special-elite-400.woff2','courier-prime-400.woff2','courier-prime-700.woff2']:
  shutil.copy('/home/claude/scw/fonts/'+f,OUT+'fonts/'+f)
open(OUT+'index.html','w').write(html)
# service worker
files=['./','index.html','site.webmanifest','welcome.jpg','welcome-wide.jpg','favicon.ico','favicon-16.png','favicon-32.png','apple-touch-icon.png','icon-192.png','icon-512.png','icon-maskable-512.png']+['fonts/'+f for f in sorted(os.listdir(OUT+'fonts'))]+['img/'+f for f in sorted(os.listdir(OUT+'img'))]
ver=hashlib.md5(html.encode()).hexdigest()[:8]
sw='''/* The Spanish Civil War — DZ Charlie field guide: keeps the guide working with no signal */
const V="scw-core-%s", CORE=%s;
self.addEventListener("install",e=>{e.waitUntil(caches.open(V).then(c=>Promise.all(CORE.map(f=>fetch(f,{cache:"no-store"}).then(r=>r.ok&&c.put(f,r)).catch(()=>{})))).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith("scw-")&&k!==V&&k!=="scw-data").map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("message",e=>{if(!e.data||!e.data.save)return;const port=e.ports[0];const ALL=CORE.concat(["pdf/The-Spanish-Civil-War-field-guide.pdf"]);
  caches.open(V).then(async c=>{let n=0;for(const f of ALL){try{const r=await fetch(f,{cache:"no-store"});if(r.ok)await c.put(f,r)}catch(err){}n++;port&&port.postMessage({n,of:ALL.length})}port&&port.postMessage({done:true})})});
self.addEventListener("fetch",e=>{const req=e.request;if(req.method!=="GET")return;const u=new URL(req.url);if(u.origin!==location.origin)return;
  if(req.mode==="navigate"||/\\.html$/.test(u.pathname)){e.respondWith(fetch(req).then(r=>{if(r.ok){const c=r.clone();caches.open(V).then(x=>x.put("index.html",c))}return r}).catch(async()=>(await caches.match("index.html"))||(await caches.match("./"))));return}
  e.respondWith(caches.match(req,{ignoreSearch:true}).then(r=>r||fetch(req).then(res=>{if(res.ok&&!/\\/pdf\\//.test(u.pathname)){const c=res.clone();caches.open(V).then(x=>x.put(req,c))}return res})));
});
'''%(ver,json.dumps(files))
open(OUT+'sw.js','w').write(sw)
open(OUT+'site.webmanifest','w').write(json.dumps({"name":"The Spanish Civil War 1936–1939 — DZ Charlie field guide","short_name":"Spanish Civil War","icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},{"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},{"src":"icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}],"theme_color":"#3d2b1f","background_color":"#efe6cf","display":"standalone","start_url":"./","scope":"./"},ensure_ascii=False))
open(OUT+'_headers','w').write("/sw.js\n  Cache-Control: no-cache\n/*.html\n  Cache-Control: no-cache\n/\n  Cache-Control: no-cache\n")
print(len(html)//1024,'KB index', ver)
