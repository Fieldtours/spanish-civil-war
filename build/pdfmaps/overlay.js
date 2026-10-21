// Print-quality area maps, step 2: the numbered sites, title, north arrow, scale and credit, drawn at 4x on a
// transparent layer for each area and language. Served from /home/claude/scw on :8900 (fonts under /site/fonts).
const {chromium}=require('/home/claude/gmap/node_modules/playwright');const fs=require('fs');
const W_='/home/claude/spanish-civil-war/build/pdfmaps/work';
const P=JSON.parse(fs.readFileSync(W_+'/plans.json'));
const NAMES={en:JSON.parse(fs.readFileSync('/home/claude/scw/build/data.js','utf8').slice(11,-1)).regions,es:JSON.parse(fs.readFileSync('/home/claude/scw/build/data_es.js','utf8').slice(11,-1)).regions};
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p=await (await b.newContext({viewport:{width:600,height:420},deviceScaleFactor:4})).newPage();
await p.goto('http://localhost:8900/build/');
for(const lang of ['en','es'])for(const r of NAMES[lang]){const pl=P[r.id];
 const svg=await p.evaluate(([pl,title,lang])=>{
  const {cx,cy,sc,W,H}=pl;const MY=la=>Math.log(Math.tan(Math.PI/4+la*Math.PI/360))*180/Math.PI;
  const X=lo=>W/2+(lo-cx)*sc,Y=la=>H/2-(MY(la)-cy)*sc;
  const R=10.5,MIN=2*R+2;const pts=pl.stops.map(([n,la,lo])=>({n,x0:X(lo),y0:Y(la),x:X(lo),y:Y(la)}));
  // spread markers that overlap; each keeps a thin leader line to its true spot
  for(let it=0;it<400;it++){let moved=false;for(let a=0;a<pts.length;a++)for(let c=a+1;c<pts.length;c++){const A=pts[a],B=pts[c];let dx=B.x-A.x,dy=B.y-A.y,d=Math.hypot(dx,dy);if(d>=MIN)continue;moved=true;if(d<.01){const an=a*2.399+c*1.7;dx=Math.cos(an);dy=Math.sin(an);d=1}const k=(MIN-d)/2+.2;A.x-=dx/d*k;A.y-=dy/d*k;B.x+=dx/d*k;B.y+=dy/d*k}
   pts.forEach(q=>{q.x=Math.max(R+4,Math.min(W-R-4,q.x));q.y=Math.max(46+R,Math.min(H-30-R,q.y))});if(!moved)break}
  const lat=Math.atan(Math.sinh(cy*Math.PI/180))*180/Math.PI;const mpp=40075016*Math.cos(lat*Math.PI/180)/(360*sc);
  const nice=[5,10,20,25,50,100,200];const km=nice.reduce((a,v)=>v*1000/mpp<=130?v:a,5);const len=km*1000/mpp;
  let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><style>@font-face{font-family:BSS;src:url(/site/fonts/bss-800.woff2)}@font-face{font-family:CP;src:url(/site/fonts/courier-prime-700.woff2)}</style>`;
  pts.forEach(q=>{if(Math.hypot(q.x-q.x0,q.y-q.y0)>2)s+=`<line x1="${q.x0}" y1="${q.y0}" x2="${q.x}" y2="${q.y}" stroke="#3d2b1f" stroke-width="1.2"/>`});
  pts.forEach(q=>{s+=`<circle cx="${q.x0}" cy="${q.y0}" r="2.6" fill="#a8321f" stroke="#fff" stroke-width=".8"/>`});
  pts.forEach(q=>{s+=`<circle cx="${q.x}" cy="${q.y}" r="${R}" fill="#fffdf7" stroke="#3d2b1f" stroke-width="2"/><text x="${q.x}" y="${q.y+3.9}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-weight="700" font-size="${q.n>99?9:10.5}" fill="#3d2b1f">${q.n}</text>`});
  const t=title.toUpperCase();s+=`<rect x="${W/2-Math.min(W-40,t.length*11+40)/2}" y="8" width="${Math.min(W-40,t.length*11+40)}" height="28" fill="#3d2b1f" opacity=".92"/><text x="${W/2}" y="28.5" text-anchor="middle" font-family="BSS,Impact,sans-serif" font-size="18" letter-spacing="1" fill="#f4efe1">${t}</text>`;
  s+=`<g transform="translate(22,22)"><circle r="14" fill="#fffdf7" opacity=".9"/><polygon points="0,-10 5,4 0,1 -5,4" fill="#3d2b1f"/><text y="11" text-anchor="middle" font-family="Helvetica" font-weight="700" font-size="7" fill="#3d2b1f">N</text></g>`;
  const bx=W-len-24;s+=`<rect x="${bx-8}" y="${H-44}" width="${len+16}" height="22" fill="#fffdf7" opacity=".85"/><line x1="${bx}" y1="${H-26}" x2="${bx+len}" y2="${H-26}" stroke="#3d2b1f" stroke-width="2.5"/><line x1="${bx}" y1="${H-31}" x2="${bx}" y2="${H-21}" stroke="#3d2b1f" stroke-width="2"/><line x1="${bx+len}" y1="${H-31}" x2="${bx+len}" y2="${H-21}" stroke="#3d2b1f" stroke-width="2"/><text x="${bx+len/2}" y="${H-30}" text-anchor="middle" font-family="CP,monospace" font-weight="700" font-size="10" fill="#3d2b1f">${km} km</text>`;
  s+=`<text x="${W-6}" y="${H-6}" text-anchor="end" font-family="Helvetica" font-size="8" fill="#3d2b1f" stroke="#fffdf7" stroke-width="2.5" paint-order="stroke">${lang==='es'?'© colaboradores de OpenStreetMap':'© OpenStreetMap contributors'}</text>`;
  return s+'</svg>'},[pl,r.name,lang]);
 await p.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);await p.waitForTimeout(400);
 await (await p.$('svg')).screenshot({path:`${W_}/ov-${lang}-${r.id}.png`,omitBackground:true})}
console.log('overlays done');await b.close()})();
