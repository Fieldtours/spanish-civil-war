/* ===== Battle maps: step-by-step schematic maps (engine from the Easy Company guides) ===== */
(function(){
const NS="http://www.w3.org/2000/svg";const B=window.SCW.battles;const byId={};B.forEach(b=>byId[b.id]=b);
function el(tag,attrs,parent){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);if(parent)parent.appendChild(e);return e}
const P=pts=>pts.map(p=>p.join(",")).join(" ");
const Dp=pts=>"M"+pts.map(p=>p.join(",")).join(" L");
function txt(g,x,y,s,cls,anchor){const t=el("text",{x,y,class:cls+" halo","text-anchor":anchor||"start"},g);t.textContent=s;return t}
function unit(g,u){const s=u.s==="nat"?"nat":"rep";
  const w=el("g",{class:"u-"+s,transform:`translate(${u.x},${u.y})`},g);
  if(s==="rep")el("rect",{class:"frame",x:-17,y:-11,width:34,height:22},w);else el("polygon",{class:"frame",points:"0,-16 17,0 0,16 -17,0"},w);
  const r=s==="rep"?{x:17,y:11}:{x:8,y:8};
  if(u.k==="inf"){el("line",{class:"sym",x1:-r.x,y1:-r.y,x2:r.x,y2:r.y},w);el("line",{class:"sym",x1:-r.x,y1:r.y,x2:r.x,y2:-r.y},w)}
  if(u.k==="arm")el("ellipse",{class:"sym",cx:0,cy:0,rx:s==="rep"?11:8,ry:5},w);
  if(u.k==="art")el("circle",{class:"dot",cx:0,cy:0,r:4.5},w);
  if(u.k==="mg"){const t=el("text",{class:"mgtxt",x:0,y:3.5,"text-anchor":"middle"},w);t.textContent="MG"}
  if(u.l){const dy=u.above?-20:(s==="rep"?27:31);const t=el("text",{class:"ulab halo",x:0,y:dy,"text-anchor":"middle"},w);t.textContent=u.l}}
function kill(g,x,y){el("line",{class:"kill",x1:x-12,y1:y-12,x2:x+12,y2:y+12},g);el("line",{class:"kill",x1:x-12,y1:y+12,x2:x+12,y2:y-12},g)}
function drawBase(svg,base){const g=el("g",{},svg);
  base.forEach(b=>{if(b.t==="town")el("polygon",{class:"m-town",points:P(b.p)},g);if(b.t==="wood")el("polygon",{class:"m-wood",points:P(b.p)},g);if(b.t==="water")el("polygon",{class:"m-water",points:P(b.p)},g);
    if(["road","rail","hedge","dike","trench","ditch"].includes(b.t)&&b.p)el("polyline",{class:"m-"+b.t,points:P(b.p)},g);
    if(b.t==="bldg")(b.r||[]).forEach(r=>el("rect",{class:"m-bldg",x:r[0],y:r[1],width:r[2],height:r[3]},g))});
  base.filter(b=>b.t==="txt").forEach(b=>txt(g,b.x,b.y,b.s,b.big?"m-big":"m-txt",b.a))}
function drawPhase(g,items){g.innerHTML="";const side=i=>i.s==="nat"?"nat":"rep";
  items.filter(i=>i.t==="f").forEach(i=>el("polyline",{class:"f-"+side(i),points:P(i.p)},g));
  items.filter(i=>i.t==="a").forEach(i=>el("path",{class:"a-"+side(i)+(i.r?" ret":""),d:Dp(i.p)},g));
  items.filter(i=>i.t==="u").forEach(i=>unit(g,i));
  items.filter(i=>i.t==="x").forEach(i=>kill(g,i.x,i.y));
  items.filter(i=>i.t==="n").forEach(i=>txt(g,i.x,i.y,i.l,"m-note",i.a))}
let open=null,lastFocus=null;
function close(){if(!open)return;open.remove();open=null;document.body.classList.remove("bm-open");if(lastFocus&&lastFocus.focus)lastFocus.focus()}
function show(id,start){const b=byId[id];if(!b)return;close();lastFocus=document.activeElement;
  const o=document.createElement("div");o.className="bmap";o.setAttribute("role","dialog");o.setAttribute("aria-modal","true");o.setAttribute("aria-label","Battle map: "+b.name);
  const E=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  o.innerHTML=`<div class="bm-in">
    <div class="bm-bar"><span class="bm-k">Battle map</span><button type="button" class="bm-x" data-bmclose>✕ Close</button></div>
    <div><h2>${E(b.name)}</h2><p class="bm-when">${E(b.when)} · ${E(b.place)}</p></div>
    <div class="bm-ph" role="group" aria-label="Steps of the battle"></div>
    <svg class="bm-svg" viewBox="0 0 600 420" role="img" aria-label="Schematic map of ${E(b.name)}">
      <defs>
        <marker id="bm-hd-rep" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path class="hm-rep" d="M0,0 L10,5 L0,10 z"/></marker>
        <marker id="bm-hd-nat" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path class="hm-nat" d="M0,0 L10,5 L0,10 z"/></marker>
        <pattern id="bm-woodpat" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" style="fill:var(--bm-wood)"/><circle cx="5" cy="5" r="3" style="fill:var(--bm-wood2)"/><circle cx="13" cy="12" r="3" style="fill:var(--bm-wood2)"/></pattern>
      </defs></svg>
    <p class="bm-cap" aria-live="polite"></p>
    <div class="bm-nav"><button type="button" data-bmstep="-1">‹ Previous step</button><button type="button" data-bmstep="1">Next step ›</button></div>
    <div class="bm-leg"><span><i style="background:var(--bm-rep)"></i>Republican forces</span><span><i style="background:var(--bm-nat)"></i>Nationalist forces</span><span>Box = Republican unit · diamond = Nationalist unit</span><span>Dashed arrow = pulling back</span><span>✕ = destroyed or taken</span></div>
    <p class="bm-why">${E(b.why)}</p>
    <dl><dt>Republic</dt><dd class="s-rep">${E(b.rep)}</dd><dt>Nationalists</dt><dd class="s-nat">${E(b.nat)}</dd><dt>Result</dt><dd>${E(b.result)}</dd></dl>
    <p class="bm-note">${b.visit||""}</p>
    <p class="bm-note">Schematic sketch, not to scale. Positions are approximate, placed from published accounts; where sources disagree on numbers, this says so. Red and blue follow the usual convention of historical maps of this war, not a judgement.</p>
  </div>`;
  document.body.appendChild(o);document.body.classList.add("bm-open");open=o;
  const svg=o.querySelector("svg"),cap=o.querySelector(".bm-cap"),bar=o.querySelector(".bm-ph"),nav=o.querySelectorAll("[data-bmstep]");
  drawBase(svg,b.base||[]);const dyn=el("g",{},svg);let cur=0;
  const btns=b.phases.map((p,i)=>{const bt=document.createElement("button");bt.type="button";bt.innerHTML=`<b>${E(p.name)}</b>${E(p.time)}`;bt.addEventListener("click",()=>go(i));bar.appendChild(bt);return bt});
  function go(i){cur=i;btns.forEach((x,j)=>x.setAttribute("aria-pressed",j===i));drawPhase(dyn,b.phases[i].items||[]);cap.textContent=`Step ${i+1} of ${b.phases.length}: ${b.phases[i].cap}`;nav[0].disabled=i===0;nav[1].disabled=i===b.phases.length-1}
  nav.forEach(n=>n.addEventListener("click",()=>{const j=cur+(+n.dataset.bmstep);if(j>=0&&j<b.phases.length)go(j)}));
  o.querySelector("[data-bmclose]").addEventListener("click",close);
  go(Math.min(start||0,b.phases.length-1));o.querySelector("[data-bmclose]").focus()}
addEventListener("keydown",e=>{if(e.key==="Escape"&&open){e.stopImmediatePropagation();close()}},true);
document.addEventListener("click",e=>{const b=e.target.closest("[data-battle]");if(!b)return;e.preventDefault();e.stopPropagation();show(b.dataset.battle,0)},true);
window.showBattleMap=show;
})();
