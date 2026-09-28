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
PDFINFO={'45 pages · 4.6 MB':'37 pages · 2.6 MB','56 pages · 10.2 MB':'38 pages · 3.0 MB','40 pages · 6.2 MB':'32 pages · 2.7 MB'}  # new-style printed guides (Sep 2026)
def ux(s,k):
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
    return s
