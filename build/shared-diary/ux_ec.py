# Ease-of-use pass (Sep 2026): shorter Home page, plain headings, one question first on the Tour page.
# Nothing is removed: the other tiles and downloads sit one tap away.
import re
VISIBLE=['tab-tour','tab-brief','tab-time','tab-dday','tab-men']   # then the diary tile
CSS="""
details.uxmore{margin-top:10px}
details.uxmore>summary{list-style:none}
details.uxmore>summary::-webkit-details-marker{display:none}
details.uxmore>.tiles{margin-top:10px}
details.uxmore[open]>summary .k{transform:rotate(45deg)}
details.uxpdf{margin:4px 0 0}
details.uxpdf>summary{cursor:pointer;min-height:44px;display:flex;align-items:center;font-weight:600;font-size:15px;color:var(--link,var(--olive2))}
details.uxpdf[open]>summary{margin-bottom:8px}
#uxpick .ap-big{margin:2px 0 10px;font-size:20px;font-weight:700;color:var(--ink)}
#uxpick .ap-list{display:grid;gap:10px}
#uxpick .ap-list button{all:unset;box-sizing:border-box;cursor:pointer;display:flex;flex-direction:column;gap:3px;text-align:left;padding:14px 16px;min-height:64px;border-radius:14px;border:2px solid var(--line2,var(--khaki));background:var(--surface,var(--paper3))}
#uxpick .ap-list button:first-child{border-color:var(--brand2,var(--olive2))}
#uxpick .ap-list b{font-size:17px;color:var(--ink)}
#uxpick .ap-list span{font-size:14.5px;color:var(--ink2);line-height:1.4}
#uxpick .ap-list button:focus-visible{outline:3px solid var(--red);outline-offset:2px}
#uxpick .uxsw{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:6px 12px}
#uxpick .uxsw span{font-size:15px;font-weight:600;color:var(--ink)}
.rd .hdr .hbtn .hl{font-size:11.5px!important}
.rd .hero .qa .cta.wide{background:#a3261e!important;color:#fff!important;border-color:#e0877d!important;font-size:19px!important;min-height:60px;box-shadow:0 4px 12px rgba(0,0,0,.45)!important}
.rd .hero .qa .cta.wide:active{transform:translateY(1px)}
"""
JS=r"""
/* ---------- TOUR PAGE: one question first (ease-of-use pass, Sep 2026) ---------- */
let UX_ASK=false;const UX_KEY="%(k)s-tourpick";
function uxGet(){try{return localStorage.getItem(UX_KEY)}catch(e){return null}}
function uxSet(v){try{v?localStorage.setItem(UX_KEY,v):localStorage.removeItem(UX_KEY)}catch(e){}}
function uxMode(){if(apOn())return "area";if(UX_ASK)return "ask";const p=uxGet();
  if(p==="area")return AP.step>0?"area":"ask";if(p==="days")return "days";
  let saved=false;try{saved=!!localStorage.getItem("%(k)s-plan")}catch(e){}
  if(saved||Object.keys(visited).some(k=>visited[k]))return "days";return "ask"}
function uxTourGate(){const box=document.getElementById("uxpick");if(!box)return;const m=uxMode();
  const d0=APP.dayChoices[0],d1=APP.dayChoices[APP.dayChoices.length-1];
  if(m==="ask"){box.hidden=false;box.innerHTML=`<div class="head">Start here</div><p class="ap-big">How much time do you have?</p><div class="ap-list"><button type="button" data-uxpick="area"><b>A few hours, or one area</b><span>Choose the part you want to see and the time you have. Three quick questions.</span></button><button type="button" data-uxpick="days"><b>One day or more</b><span>A ready-made route for ${d0} to ${d1} days, with the driving order and a place to stay each night.</span></button></div>`}
  else if(m==="days"){box.hidden=false;box.innerHTML=`<div class="uxsw"><span>Ready-made route</span><button type="button" class="linkbtn" data-uxpick="area">Only a few hours? Choose an area instead</button></div>`}
  else{box.hidden=true;box.innerHTML=""}
  const hide=(id,h)=>{const e=document.getElementById(id);if(e)e.style.display=h?"none":""};
  hide("apbox",m==="ask"||m==="days");hide("classicbox",m!=="days");const wiz=m==="area"&&!apOn();hide("addbox",m==="ask"||wiz);hide("tourout",m==="ask"||wiz)}
document.addEventListener("click",e=>{const t=e.target.closest("[data-uxpick],[data-ap]");if(!t)return;
  const v=t.dataset.uxpick;
  if(v==="area"){UX_ASK=false;uxSet("area");AP.step=1;renderTour();apScroll();return}
  if(v==="days"){UX_ASK=false;uxSet("days");renderTour();const c=document.getElementById("uxpick");if(c)c.scrollIntoView({block:"start",behavior:"smooth"});return}
  const a=t.dataset.ap;
  if(a==="classic"){UX_ASK=false;uxSet("days");uxTourGate();return}
  if(a==="back0"&&!apOn()){UX_ASK=true;uxSet(null);uxTourGate();const c=document.getElementById("uxpick");if(c)c.scrollIntoView({block:"start",behavior:"smooth"});return}
  if(a==="build"){UX_ASK=false;uxSet("area");uxTourGate();return}
});
"""
def rep(s,o,n,c=1):
    assert s.count(o)==c,(o[:70],s.count(o));return s.replace(o,n)
PDFINFO={'45 pages · 4.6 MB':'37 pages · 3.5 MB','56 pages · 10.2 MB':'38 pages · 4.2 MB','40 pages · 6.2 MB':'32 pages · 3.5 MB'}  # new-style printed guides (Sep 2026)
MAPPREFIX={'ecn':'normandy','ech':'holland','ecg':'germany'}
RASPICK=r'''
/* pick the map pictures drawn for this zoom (Google-style road maps, several zoom levels; Sep 2026) */
const RAS_PR=1.5;
function rasPick(d,x0,x1,y0,y1,f){f=f||MY;const R=rasterUrls(),RES=r=>r.w/(r.b[2]-r.b[0]),fam={};
  R.forEach(r=>{const F=fam[r.g]=fam[r.g]||{};if(!(r.lv in F))F[r.lv]=RES(r)});const pick={};
  Object.keys(fam).forEach(g=>{const lv=Object.entries(fam[g]).map(([l,res])=>[+l,res]).filter(x=>x[0]>=0).sort((a,b)=>a[1]-b[1]);
    let c=lv.find(x=>x[1]>=d*0.8)||lv[lv.length-1];if(+g!==0&&c[1]>d*4)c=null;
    /* stretched far beyond its size: use the copy without place names, so no giant blurry names */
    if(c&&c[1]<d*0.45&&(-1 in fam[g]))c=[-1,fam[g][-1]];pick[g]=c?c[0]:-9});
  return R.filter(r=>pick[r.g]===r.lv&&r.b[2]>x0&&r.b[0]<x1&&f(r.b[3])>y0&&f(r.b[1])<y1).sort((a,b)=>RES(a)-RES(b))}
'''
def maps_patch(s,k):
    import os,json,re
    pre=MAPPREFIX[k];rf=f'/home/claude/gmap/tiles/{pre}/raster.json'
    if not os.path.exists(rf): return s
    R=json.load(open(rf))
    s=re.sub(r'const RASTER=\[.*?\];','const RASTER='+json.dumps(R,separators=(',',':'))+';',s,count=1,flags=re.S)
    s=rep(s,'let RASTER_URLS=null;','let RASTER_URLS=null;'+RASPICK)
    # small maps (cards, day maps, cover map)
    a=s.index('const ras=rasterUrls().filter(r=>r.b[2]>vw[0]');b=s.index('hasRaster=true});',a)+len('hasRaster=true});')
    s=s[:a]+'''const ras=rasPick(sc*RAS_PR,vw[0],vw[1],vh[0],vh[1]);
  let hasRaster=false;const RES=r=>r.w/(r.b[2]-r.b[0]);
  ras.forEach(r=>{const x=X(r.b[0]),y=Y(r.b[3]),w=X(r.b[2])-x,h=Y(r.b[1])-y;
    g+=`<image href="${r.url}" x="${x.toFixed(2)}" y="${y.toFixed(2)}" width="${(w+0.6).toFixed(2)}" height="${(h+0.6).toFixed(2)}" preserveAspectRatio="none"/>`;hasRaster=true});'''+s[b:]
    # the pan/zoom area map
    s=rep(s,'const want=RAS.filter(r=>(r.g===0||sc>=rr(r)*0.35)&&r.b[2]>lo0&&r.b[0]<lo1&&my(r.b[3])>y0&&my(r.b[1])<y1).sort((a,b)=>rr(a)-rr(b));','const want=rasPick(sc*RAS_PR,lo0,lo1,y0,y1,my);')
    # the enlarge viewer: swap to the level that suits the zoom
    a=s.index('function addSharp(svg){');b=s.index('\n}\n',a)+3
    s=s[:a]+'''function addSharp(svg){
  try{const pr=(svg.getAttribute("data-proj")||"").split(",").map(Number);if(pr.length<5||typeof RASTER==="undefined")return;
    const [cx,cy,sc,W,H]=pr,X=lo=>W/2+(lo-cx)*sc,Y=la=>H/2-(MY(la)-cy)*sc;
    const vw=[cx-(W/2)/sc,cx+(W/2)/sc],vh=[cy-(H/2)/sc,cy+(H/2)/sc];
    const used=[...svg.querySelectorAll("image")];if(!used.length)return;
    const z=typeof lbZoom==="number"?Math.max(1,lbZoom):2;const want=rasPick(sc*z*RAS_PR,vw[0],vw[1],vh[0],vh[1]);
    const ns="http://www.w3.org/2000/svg",first=used[0];
    want.forEach(r=>{const x=X(r.b[0]),y=Y(r.b[3]),w=X(r.b[2])-x,h=Y(r.b[1])-y;
      const im=document.createElementNS(ns,"image");im.setAttribute("href",r.url);im.setAttribute("x",x.toFixed(2));im.setAttribute("y",y.toFixed(2));
      im.setAttribute("width",(w+0.3).toFixed(2));im.setAttribute("height",(h+0.3).toFixed(2));im.setAttribute("preserveAspectRatio","none");
      first.before(im)});
    used.forEach(i=>i.remove());
  }catch(e){}
}
'''+s[b:]
    s=rep(s,'if(lbZoom>1.4&&!sharp){sharp=true;addSharp(svg)}','{const bd=Math.round(Math.log2(Math.max(lbZoom,1))*2);if(bd!==sharp){sharp=bd;addSharp(svg)}}')
    # files to save for offline use
    m=re.search(r'const FILES=\[(.*?)\];',s,re.S)
    items=[x.strip() for x in m.group(1).split(',') if x.strip() and 'maps/' not in x]
    s=s[:m.start()]+'const FILES=['+', '.join([json.dumps(r['src']) for r in R]+items)+'];'+s[m.end():]
    return s
def ux(s,k):
    s=maps_patch(s,k)
    for a,b in PDFINFO.items(): s=s.replace(a,b)
    i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
    s=rep(s,'<h3 style="margin-top:14px">Orders — where to go from here</h3>','<h3 style="margin-top:14px">Explore the guide</h3>')
    s=rep(s,'<div class="head">Standing orders</div>','<div class="head">Before you visit</div>')
    # tiles
    a=s.index('<div class="tiles">',s.index('id="p-home"')); b=s.index('<div class="pdfdl pdfbtn" id="pdfdl-home">',a)
    blk=s[a:b]; e=blk.rindex('</div>'); inner=blk[len('<div class="tiles">'):e]
    tiles=re.findall(r'<button type="button" class="tile".*?</button>',inner,flags=re.S)
    assert ''.join(tiles)==inner.strip(),'tile parse'
    go=lambda t:(re.search(r'data-go="([^"]+)"',t) or re.search(r'data-(aar)=',t)).group(1)
    by={go(t):t for t in tiles}; assert len(by)==9,by.keys()
    vis=[by[g] for g in VISIBLE]; rest=[t for t in tiles if go(t) not in VISIBLE and go(t)!='aar']
    def num(t,n): return re.sub(r'<span class="k">\d\d</span>','<span class="k">%02d</span>'%n,t,count=1)
    vis=[num(t,n+1) for n,t in enumerate(vis)]; rest=[num(t,n+1+len(vis)) for n,t in enumerate(rest)]
    names=[re.sub(r'<svg.*?</svg>','',re.search(r'<b>(.*?)</b>',t,flags=re.S).group(1),flags=re.S) for t in rest]
    sub=', '.join(names[:-1])+' and '+names[-1]
    new='<div class="tiles">'+''.join(vis)+by['aar']+'</div>\n      <details class="uxmore"><summary class="tile"><span class="k">+</span><b>More to explore</b><span>'+sub+'.</span></summary><div class="tiles">'+''.join(rest)+'</div></details>\n\n      '
    s=s[:a]+new+s[b:]
    # downloads: this guide first, the rest folded
    a=s.index('<a class="pdl" href="pdf/Easy-Company-Common-Reference.pdf"'); b=s.index('<p class="pn">',a)
    s=s[:a]+'<details class="uxpdf"><summary>Other downloads (3)</summary>'+s[a:b]+'</details>'+s[b:]
    # tour page: the question box, and the switch-over
    s=rep(s,'<div class="memo" id="apbox" aria-live="polite"></div>','<div class="memo" id="uxpick" hidden></div>\n      <div class="memo" id="apbox" aria-live="polite"></div>')
    s=rep(s,'function renderTour(){\n  apRenderPanel();\n','function renderTour(){\n  apRenderPanel();uxTourGate();\n')
    s=rep(s,'/* ---------- MY ROUTE: add / remove from any tab, route buttons ---------- */',JS%{'k':k}+'/* ---------- MY ROUTE: add / remove from any tab, route buttons ---------- */')
    import myroute_ec
    s=myroute_ec.patch(s,k)
    return s
