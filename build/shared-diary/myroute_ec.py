# Sep 2026 (JC): 1) the After Action Reports open from a button in the top bar, not a Home tile;
# 2) "Plan my tour" opens straight on the ready-made routes, with a slim switch to the other ways;
# 3) "Build my own route": choose the days, tap sites on the map or in the list, and the app
#    orders each day and gives the Google Maps route. It reuses the normal tour display, so the
#    day maps, Google Maps buttons, visited ticks, "On the road" and the diary all work with it.
import re

AAR_ICON = ('<svg class="aar-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            '<path d="M5 3.5h10.5a1.5 1.5 0 0 1 1.5 1.5v15a1 1 0 0 1-1 1H5z"/>'
            '<path d="M5 3.5v17.5"/><path d="M8.5 8h5M8.5 11.5h5M8.5 15h3"/>'
            '<path d="M20.5 7.5l-3.5 9-1.2 2.6.3-2.9 3.5-9z"/></svg>')
AAR_BTN = ('<button type="button" class="hbtn aar-hbtn" data-aar="open" '
           'aria-label="After Action Reports — your trip journal: save or share each day of your route" '
           'title="After Action Reports — your trip journal">' + AAR_ICON + '<span class="hl">AAR</span></button>')

CSS = """
.rd .hdr .aar-hbtn .aar-ico{width:24px;height:24px}
/* tour page: one slim switch instead of the question screen */
#uxpick .uxseg{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
#uxpick .uxseg button{all:unset;box-sizing:border-box;cursor:pointer;text-align:center;padding:10px 4px;min-height:48px;border-radius:12px;border:2px solid var(--line2,var(--khaki));background:var(--surface,var(--paper3));font-weight:700;font-size:14.5px;line-height:1.2;color:var(--ink);display:flex;align-items:center;justify-content:center}
#uxpick .uxseg button[aria-pressed=true]{background:var(--brand2,var(--olive2));border-color:var(--brand2,var(--olive2));color:#fff}
#uxpick .uxseg button:focus-visible{outline:3px solid var(--red);outline-offset:2px}
#uxpick .uxhint{margin:8px 2px 0;font-size:14px;color:var(--ink2);line-height:1.4}
/* build my own route */
#mybox .my-steps{margin:2px 0 10px;padding-left:20px;font-size:14.5px;line-height:1.45;color:var(--ink2)}
#mybox .my-steps li{margin:2px 0}
#mybox .my-lab{display:block;margin:12px 0 6px;font-weight:700;font-size:14px;letter-spacing:.04em;text-transform:uppercase;color:var(--ink2)}
#mybox .my-chips{display:flex;flex-wrap:wrap;gap:8px}
#mybox .my-chips button{all:unset;box-sizing:border-box;cursor:pointer;min-width:48px;min-height:48px;padding:0 12px;border-radius:24px;border:2px solid var(--line2,var(--khaki));background:var(--surface,var(--paper3));font-weight:700;font-size:16px;color:var(--ink);display:inline-flex;align-items:center;justify-content:center;gap:6px}
#mybox .my-chips button small{font-weight:600;font-size:13px;opacity:.85}
#mybox .my-chips button[aria-pressed=true]{background:var(--brand2,var(--olive2));border-color:var(--brand2,var(--olive2));color:#fff}
#mybox .my-chips button:focus-visible,#mybox .my-row button:focus-visible{outline:3px solid var(--red);outline-offset:2px}
#mybox .my-legend{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:13px;color:var(--ink2);margin:0 0 6px}
#mybox .my-legend i{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:-1px;margin-right:4px;border:2px solid #1c1a15}
#mybox .my-day{border:1.5px solid var(--line2,var(--khaki));border-radius:12px;padding:8px 10px;margin:8px 0;background:var(--surface,var(--paper3))}
#mybox .my-day .my-dh{font-weight:700;font-size:15px;margin:2px 0 4px}
#mybox .my-day ol{margin:0;padding-left:22px}
#mybox .my-day li{display:flex;align-items:center;justify-content:space-between;gap:8px;min-height:44px;font-size:14.5px}
#mybox .my-day li span{flex:1}
#mybox .my-x{all:unset;box-sizing:border-box;cursor:pointer;min-width:44px;min-height:44px;border-radius:10px;display:grid;place-items:center;font-weight:700;color:var(--red,#a3261e)}
#mybox .my-empty{font-size:14px;color:var(--ink2);margin:4px 0}
#mybox .my-go{all:unset;box-sizing:border-box;cursor:pointer;display:block;width:100%;text-align:center;margin:12px 0 4px;padding:14px;min-height:54px;border-radius:14px;background:#a3261e;color:#fff;font-weight:700;font-size:18px;box-shadow:0 3px 10px rgba(0,0,0,.3)}
#mybox .my-go[disabled]{opacity:.45;cursor:default;box-shadow:none}
#mybox .my-srch{width:100%;box-sizing:border-box;min-height:46px;padding:10px 12px;border-radius:12px;border:1.5px solid var(--line2,var(--khaki));font-size:16px;margin:0 0 6px}
#mybox .my-grp{margin:10px 0 2px;font-weight:700;font-size:14px;color:var(--ink)}
#mybox .my-row{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:6px 0;border-bottom:1px solid var(--line,rgba(0,0,0,.12))}
#mybox .my-row span{flex:1;font-size:14.5px;line-height:1.3}
#mybox .my-row small{color:var(--ink2)}
#mybox .my-row button{all:unset;box-sizing:border-box;cursor:pointer;min-height:44px;min-width:92px;padding:0 10px;border-radius:10px;border:2px solid var(--brand2,var(--olive2));font-weight:700;font-size:14px;text-align:center;display:grid;place-items:center;color:var(--ink)}
#mybox .my-row button.in{background:var(--brand2,var(--olive2));color:#fff}
#mybox .my-sum{font-weight:700;font-size:17px;margin:2px 0 4px}
#mybox .ap-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
#mybox .ap-map{position:relative;height:340px;border-radius:14px;overflow:hidden;border:1.5px solid var(--line2,var(--olive2));background:#cfc5a4;touch-action:none;margin:6px 0 8px}
#mybox .ap-svg{width:100%;height:100%;display:block;cursor:grab;user-select:none;-webkit-user-select:none}
#mybox .ap-zoom{position:absolute;right:8px;top:8px;display:grid;gap:6px}
#mybox .ap-zoom button{all:unset;box-sizing:border-box;cursor:pointer;width:44px;height:44px;border-radius:12px;background:#fff;color:#1c1a15;font-size:24px;font-weight:700;display:grid;place-items:center;box-shadow:0 1px 4px rgba(0,0,0,.35)}
#mybox .ap-town{font-family:var(--monoF,monospace);font-size:11px;font-weight:700;fill:#3f3a2e;paint-order:stroke;stroke:#efe9d2;stroke-width:3px}
#mybox .ap-btn{all:unset;box-sizing:border-box;cursor:pointer;display:flex;align-items:center;justify-content:center;text-align:center;min-height:52px;padding:10px 14px;border-radius:14px;background:var(--brand2,var(--olive2));color:#fff;font-family:var(--sans,inherit);font-weight:700;font-size:16px;line-height:1.25;flex:1 1 140px}
#mybox .ap-btn.ghost{background:var(--surface2,var(--paper));color:var(--ink);border:1.5px solid var(--line2,var(--khaki))}
#mybox .ap-btn:focus-visible,#mybox input:focus-visible{outline:3px solid var(--accent,var(--red));outline-offset:2px}
#mybox .ap-sub{font-size:14.5px;color:var(--ink2);line-height:1.4}
@media (prefers-color-scheme:dark){#mybox .ap-btn:not(.ghost),#mybox .my-chips button[aria-pressed="true"],#mybox .my-row button.in,#uxpick .uxseg button[aria-pressed="true"]{color:#121410}#mybox .my-go{color:#fff}}
"""

JS = r"""
/* ---------- BUILD MYR OWN ROUTE (Sep 2026) ---------- */
const MY_KEY="%(k)s-myroute";
let MYR={on:false,edit:false,days:2,cur:1,lists:[[],[]]},MY_Q="",MY_PM=null;
try{const s=JSON.parse(localStorage.getItem(MY_KEY)||"null");if(s&&Array.isArray(s.lists)&&s.days)MYR=Object.assign(MYR,s,{edit:false})}catch(e){}
const myNorm=s=>String(s).normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();
function mySave(){try{localStorage.setItem(MY_KEY,JSON.stringify(MYR))}catch(e){}}
function myOn(){return !!MYR.on&&!MYR.edit&&uxGet()==="my"&&!apOn()}
function myAll(){ensureDdayPool();return POOL.concat(plan.custom.map(c=>Object.assign({},c,{seq:99,pri:0,conf:"DOC",cat:"Your own stop",custom:true})))}
function myGet(id){return myAll().find(p=>p.id===id)}
function myDayOf(id){const i=MYR.lists.findIndex(l=>l.includes(id));return i<0?0:i+1}
function myCount(){return MYR.lists.slice(0,MYR.days).reduce((s,l)=>s+l.length,0)}
function mySetDays(n){n=Math.max(1,Math.min(7,n));while(MYR.lists.length<n)MYR.lists.push([]);
  if(MYR.lists.length>n){const extra=MYR.lists.splice(n).flat();MYR.lists[n-1]=MYR.lists[n-1].concat(extra)}
  MYR.days=n;if(MYR.cur>n)MYR.cur=n;mySave()}
function myToggle(id,day){day=day||MYR.cur;const d=myDayOf(id);MYR.lists=MYR.lists.map(l=>l.filter(x=>x!==id));
  if(d!==day)MYR.lists[day-1].push(id);mySave();return d===day?0:day}
function myBuild(){let prev=null;return MYR.lists.slice(0,MYR.days).map(l=>{const pts=l.map(myGet).filter(Boolean);
  const r=apOrder(pts,prev,40);if(r.length)prev=[r[r.length-1].lat,r[r.length-1].lon];return r})}
function myDrive(ds,di,days){let m=0,cur=null;if(di>0){const pd=days[di-1];if(pd&&pd.length)cur=[pd[pd.length-1].lat,pd[pd.length-1].lon]}
  ds.forEach(p=>{if(cur)m+=apDrive(apKm(cur[0],cur[1],p.lat,p.lon));cur=[p.lat,p.lon]});return m}
function mySummary(days){const all=days.flat(),vis=all.reduce((s,p)=>s+p.min,0),drv=days.reduce((s,ds,di)=>s+myDrive(ds,di,days),0),nDone=all.filter(p=>visited[p.id]).length;
  return `<div class="summ ap-summ"><b>Your own route · ${days.length} day${days.length>1?"s":""} · ${all.length} stop${all.length===1?"":"s"} · about ${apHm(vis+drv)} including ${apHm(drv)} driving</b><br>Each day is put in driving order; the first stop of a day follows on from where the day before ended.${nDone?` · ${nDone} visited`:""}</div>`}
function myDayLine(di,ds){const days=buildPlan(),vis=ds.reduce((s,p)=>s+p.min,0),drv=myDrive(ds,di,days);
  return `${ds.length} stop${ds.length===1?"":"s"} · about ${apHm(vis+drv)} (visits ${apHm(vis)} + driving ${apHm(drv)})${vis+drv>600?" · a long day: consider moving a stop":""}`}
function myEmptyDay(){return `<p class="small" style="margin-bottom:12px">No stops chosen for this day yet. Tap <b>Edit my route</b> above to add some.</p>`}
const MY_COL="#a3261e",MY_OTHER="#3f5a2a";
function myOverlay(M){let o="";const pts=myAll();
  const sh=pts.map(p=>[p,myDayOf(p.id)]).sort((a,b)=>(a[1]===MYR.cur)-(b[1]===MYR.cur)||a[1]-b[1]);
  sh.forEach(([p,d])=>{const x=M.X(p.lon),y=M.Y(p.lat);if(x<-10||y<-10||x>M.W+10||y>M.H+10)return;
    if(!d)o+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="7" fill="#fff" stroke="#1c1a15" stroke-width="2"/>`;
    else{const cur=d===MYR.cur;o+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${cur?11:9}" fill="${cur?MY_COL:MY_OTHER}" stroke="#fff" stroke-width="2"/><text x="${x.toFixed(1)}" y="${(y+4).toFixed(1)}" text-anchor="middle" font-size="${cur?12:10}" font-weight="700" fill="#fff" font-family="sans-serif">${d}</text>`}});
  return o}
function myBounds(){const pts=myAll(),la=pts.map(p=>p.lat),lo=pts.map(p=>p.lon);return[Math.min(...la),Math.min(...lo),Math.max(...la),Math.max(...lo)]}
function myListHtml(){const q=myNorm(MY_Q.trim()),pts=myAll().filter(p=>!q||myNorm(p.name+" "+(p.cat||"")).includes(q));
  const groups={};pts.forEach(p=>{const g=p.custom?"__own":apRegionOf(p);(groups[g]=groups[g]||[]).push(p)});
  let h="";AP_AREAS.map(a=>a.id).concat(["__own"]).forEach(g=>{const L=groups[g];if(!L||!L.length)return;
    const nm=g==="__own"?"Your own spots":(AP_AREAS.find(a=>a.id===g)||{}).name;h+=`<div class="my-grp">${esc(nm)}</div>`;
    L.sort((a,b)=>a.seq-b.seq).forEach(p=>{const d=myDayOf(p.id);
      h+=`<div class="my-row"><span>${esc(p.name)} <small>· ${p.min} min${p.pri<=1?" · must see":""}</small></span><button type="button" data-myadd="${esc(p.id)}" class="${d?"in":""}" aria-label="${d?(d===MYR.cur?"Remove from":"Move to Day "+MYR.cur+" from")+" Day "+d:"Add to Day "+MYR.cur}: ${esc(p.name)}">${d?(d===MYR.cur?"✓ Day "+d:"Day "+d+" → "+MYR.cur):"＋ Day "+MYR.cur}</button></div>`})});
  return h||`<p class="my-empty">No site matches "${esc(MY_Q)}".</p>`}
function myDaysHtml(){const days=myBuild();let h="";
  days.forEach((ds,i)=>{const n=i+1;h+=`<div class="my-day"><div class="my-dh">Day ${n}${n===MYR.cur?" · adding here":""}</div>${ds.length?`<ol>${ds.map(p=>`<li><span>${esc(p.name)} <small>· ${p.min} min</small></span><button type="button" class="my-x" data-myrm="${esc(p.id)}" aria-label="Remove ${esc(p.name)} from Day ${n}">✕</button></li>`).join("")}</ol>`:`<p class="my-empty">Nothing yet — choose Day ${n} above, then tap sites.</p>`}</div>`});
  return h}
function myRenderPanel(){const box=document.getElementById("mybox");if(!box)return;
  if(!MYR.edit&&MYR.on&&myCount()){box.innerHTML=`<div class="head">Your own route</div><p class="my-sum">${MYR.days} day${MYR.days>1?"s":""} · ${myCount()} stop${myCount()===1?"":"s"}</p>
    <div class="ap-row"><button type="button" class="ap-btn" data-my="edit">Edit my route</button><button type="button" class="ap-btn ghost" data-my="clear">Start again</button></div>`;return}
  const n=myCount();
  box.innerHTML=`<div class="head">Build my own route</div>
  <ol class="my-steps"><li>Choose how many days.</li><li>Pick a day, then tap sites on the map or in the list below to add them to it.</li><li>Tap <b>Make my route</b>: the app puts each day in driving order, with the Google Maps route.</li></ol>
  <span class="my-lab">1 · How many days?</span><div class="my-chips" role="group" aria-label="How many days">${[1,2,3,4,5,6,7].map(d=>`<button type="button" data-mydays="${d}" aria-pressed="${MYR.days===d}" aria-label="${d} day${d>1?"s":""}">${d}</button>`).join("")}</div>
  <span class="my-lab">2 · Add sites to</span><div class="my-chips" role="group" aria-label="Which day to add to">${MYR.lists.slice(0,MYR.days).map((l,i)=>`<button type="button" data-mycur="${i+1}" aria-pressed="${MYR.cur===i+1}">Day ${i+1} <small>(${l.length})</small></button>`).join("")}</div>
  <p class="ap-sub" style="margin:8px 0 4px">Tap a dot on the map to add it to <b>Day ${MYR.cur}</b>; tap it again to take it out. Where dots sit close together, zoom in with + or two fingers first.</p>
  <div class="my-legend"><span><i style="background:#fff"></i>Not chosen</span><span><i style="background:${MY_COL};border-color:#fff"></i>Day ${MYR.cur}</span><span><i style="background:${MY_OTHER};border-color:#fff"></i>Other days</span></div>
  <div class="ap-map" id="my-map"></div>
  <div id="my-days">${myDaysHtml()}</div>
  <button type="button" class="my-go" data-my="make"${n?"":" disabled"}>Make my route${n?` · ${n} stop${n===1?"":"s"}`:""}</button>
  <span class="my-lab">Or pick from the list</span><input type="search" class="my-srch" id="my-q" placeholder="Search sites" aria-label="Search sites" value="${esc(MY_Q)}">
  <div id="my-list">${myListHtml()}</div>`;
  const el=document.getElementById("my-map");
  MY_PM=apMap(el,{overlay:myOverlay,onTap:(x,y,M)=>{let best=null,bd=24;myAll().forEach(p=>{const d=Math.hypot(M.X(p.lon)-x,M.Y(p.lat)-y);if(d<bd){bd=d;best=p}});
    if(best)myTapped(best.id)}});
  MY_PM.fit(myBounds(),24);
  const q=document.getElementById("my-q");if(q)q.addEventListener("input",()=>{MY_Q=q.value;document.getElementById("my-list").innerHTML=myListHtml()})}
function myRefresh(){const d=document.getElementById("my-days");if(d)d.innerHTML=myDaysHtml();const l=document.getElementById("my-list");if(l)l.innerHTML=myListHtml();
  document.querySelectorAll("#mybox [data-mycur]").forEach(b=>{const i=+b.dataset.mycur;b.innerHTML=`Day ${i} <small>(${MYR.lists[i-1].length})</small>`});
  const g=document.querySelector("#mybox .my-go"),n=myCount();if(g){g.disabled=!n;g.textContent="Make my route"+(n?` · ${n} stop${n===1?"":"s"}`:"")}
  if(MY_PM)MY_PM.redraw()}
function myTapped(id){const p=myGet(id),r=myToggle(id);myRefresh();toast(r?`${p?p.name.split(/ — | \/ /)[0]:"Site"} added to Day ${r}`:"Taken out of your route")}
document.addEventListener("click",e=>{const t=e.target.closest("[data-my],[data-mydays],[data-mycur],[data-myadd],[data-myrm]");if(!t||!t.closest("#mybox"))return;
  if(t.dataset.mydays){mySetDays(+t.dataset.mydays);myRenderPanel();return}
  if(t.dataset.mycur){MYR.cur=+t.dataset.mycur;mySave();myRenderPanel();return}
  if(t.dataset.myadd){myTapped(t.dataset.myadd);return}
  if(t.dataset.myrm){MYR.lists=MYR.lists.map(l=>l.filter(x=>x!==t.dataset.myrm));mySave();myRefresh();toast("Taken out of your route");return}
  const a=t.dataset.my;
  if(a==="make"){if(!myCount())return;MYR.on=true;MYR.edit=false;mySave();renderTour();const o=document.getElementById("mybox");if(o)o.scrollIntoView({block:"start",behavior:"smooth"});return}
  if(a==="edit"){MYR.edit=true;renderTour();const o=document.getElementById("mybox");if(o)o.scrollIntoView({block:"start",behavior:"smooth"});return}
  if(a==="clear"){MYR={on:false,edit:true,days:MYR.days,cur:1,lists:MYR.lists.map(()=>[])};mySave();renderTour();return}
});
/* while your own route is showing, "+ Add to my route" anywhere in the guide adds to it (to the day you last chose) */
document.addEventListener("click",e=>{if(!myOn()&&!(MYR.edit&&uxGet()==="my"))return;const t=e.target.closest("[data-route],[data-drop]");if(!t||t.closest("#mybox"))return;
  e.stopImmediatePropagation();e.preventDefault();const k=t.dataset.route||t.dataset.drop;const p=myGet(k);if(!p)return;
  const was=myDayOf(k);if(t.dataset.drop||was){MYR.lists=MYR.lists.map(l=>l.filter(x=>x!==k));mySave();renderTour();toast("Taken out of your route");return}
  MYR.lists[MYR.cur-1].push(k);mySave();renderTour();toast(`Added to your route · Day ${MYR.cur}`)},true);
"""

UX_JS_NEW = r"""
/* ---------- TOUR PAGE: straight to the ready-made routes, with a slim switch (Sep 2026) ---------- */
let UX_ASK=false;const UX_KEY="%(k)s-tourpick";
let UX_CUR=null;function uxGet(){if(UX_CUR===null){try{UX_CUR=localStorage.getItem(UX_KEY)||""}catch(e){UX_CUR=""}}return UX_CUR}
function uxSet(v){UX_CUR=v||"";try{v?localStorage.setItem(UX_KEY,v):localStorage.removeItem(UX_KEY)}catch(e){}}
function uxMode(){if(apOn())return "area";const p=uxGet();if(p==="area"||p==="my")return p;return "days"}
const UX_HINT={days:"A ready-made route for %(d0)s to %(d1)s days, with the driving order and a place to stay each night.",area:"A few hours, or only one part? Choose the area and the time you have.",my:"Choose your days and the sites you want; the app puts them in driving order."};
function uxTourGate(){const box=document.getElementById("uxpick");if(!box)return;const m=uxMode();
  box.hidden=false;box.innerHTML=`<div class="uxseg" role="group" aria-label="How to plan your tour">${[["days","Ready-made"],["area","By area"],["my","Build my own"]].map(x=>`<button type="button" data-uxpick="${x[0]}" aria-pressed="${m===x[0]}">${x[1]}</button>`).join("")}</div><p class="uxhint">${UX_HINT[m]}</p>`;
  const hide=(id,h)=>{const e=document.getElementById(id);if(e)e.style.display=h?"none":""};
  const wiz=m==="area"&&!apOn(),myEd=m==="my"&&!myOn();if(m==="my"&&!MYR.on)MYR.edit=true;
  hide("apbox",m!=="area");hide("classicbox",m!=="days");hide("mybox",m!=="my");hide("addbox",m!=="days"&&!(m==="area"&&apOn()));hide("tourout",wiz||myEd);
  if(m==="my")myRenderPanel()}
document.addEventListener("click",e=>{const t=e.target.closest("[data-uxpick],[data-ap]");if(!t)return;
  const v=t.dataset.uxpick;
  if(v==="days"){apOff();AP.step=0;MYR.edit=false;mySave();uxSet("days");renderTour();return}
  if(v==="area"){MYR.edit=false;mySave();uxSet("area");if(!apOn())AP.step=1;renderTour();if(!apOn())apScroll();return}
  if(v==="my"){apOff();AP.step=0;uxSet("my");if(!MYR.on||!myCount())MYR.edit=true;mySave();renderTour();return}
  const a=t.dataset.ap;
  if(a==="classic"){uxSet("days");uxTourGate();return}
  if(a==="back0"&&!apOn()){uxSet("days");renderTour();return}
  if(a==="build"){uxSet("area");uxTourGate();return}
});
"""


def rep(s, o, n, c=1):
    assert s.count(o) == c, (o[:80], s.count(o))
    return s.replace(o, n)


def patch(s, k):
    # 1) AAR: off the Home tile list, onto the top bar
    s = rep(s, '<button type="button" class="hbtn wp-btn" data-go="tab-weap"', AAR_BTN + '<button type="button" class="hbtn wp-btn" data-go="tab-weap"')
    a = s.index('<div class="tiles">', s.index('id="p-home"'))
    m = re.compile(r'<button type="button" class="tile" data-aar="open">.*?</button>', re.S).search(s, a)
    assert m and m.start() < s.index('<details class="uxmore">', a), 'aar tile'
    s = s[:m.start()] + s[m.end():]
    # 2) tour page: replace the question-first gate with the slim switch; plain heading for the ready-made box
    a = s.index('/* ---------- TOUR PAGE: one question first'); b = s.index('/* ---------- MY ROUTE: add / remove from any tab', a)
    d0 = re.search(r'dayChoices:\[(\d+)', s); d1 = re.search(r'dayChoices:\[[^\]]*?(\d+)\]', s)
    s = s[:a] + UX_JS_NEW % {'k': k, 'd0': d0.group(1) if d0 else 1, 'd1': d1.group(1) if d1 else 7} + JS % {'k': k} + s[b:]
    s = rep(s, '<div class="head">Or a ready-made tour · Which tour?</div>', '<div class="head">Which tour?</div>')
    s = rep(s, '<div class="memo" id="apbox" aria-live="polite"></div>', '<div class="memo" id="apbox" aria-live="polite"></div>\n      <div class="memo" id="mybox" aria-live="polite" style="display:none"></div>')
    # 3) the tour display learns the third kind of plan
    s = rep(s, 'function buildPlan(){\n  ensureDdayPool();\n  if(apOn())return apBuild();', 'function buildPlan(){\n  ensureDdayPool();\n  if(myOn())return myBuild();\n  if(apOn())return apBuild();')
    s = rep(s, 'let html=apOn()?apSummary(days):', 'let html=myOn()?mySummary(days):apOn()?apSummary(days):')
    s = rep(s, 'const title=(!apOn()&&plan.days===DAYS.length', 'const title=(!apOn()&&!myOn()&&plan.days===DAYS.length')
    s = rep(s, '${apOn()?apDayLine(di,ds):', '${myOn()?myDayLine(di,ds):apOn()?apDayLine(di,ds):')
    s = rep(s, '} else if(apOn())html+=apEmptyDay();', '} else if(myOn())html+=myEmptyDay();\n    else if(apOn())html+=apEmptyDay();')
    i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
    return s
