/* ---------- AFTER ACTION REPORT / DIARIO DE CAMPAÑA (added Sep 2026) ----------
   A quiet end-of-day recollection: the places you ticked off today, put in the order the
   events happened, one question, one line in your own words, and a page for your journal.
   Everything stays on the phone. No points, no scores. */
(function(){
const C=window.AAR_CFG;if(!C)return;
const D=C.data||{};
const LS={get:(k,d)=>{try{const v=localStorage.getItem(C.key+"-"+k);return v?JSON.parse(v):d}catch(e){return d}},set:(k,v)=>{try{localStorage.setItem(C.key+"-"+k,JSON.stringify(v))}catch(e){}}};
const ESC=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const today=()=>{const d=new Date();return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")};
const MON=["January","February","March","April","May","June","July","August","September","October","November","December"],WD=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
function longDate(iso){if(iso==="earlier")return"Before you started your "+C.short;const [y,m,d]=iso.split("-").map(Number),dt=new Date(y,m-1,d);return `${WD[dt.getDay()]} ${d} ${MON[m-1]} ${y}`}
/* ---- which stops were visited on which day: the app keeps a set of visited stops; we keep the date ---- */
let LOG=LS.get("log",null);          /* [[id,date],…] in visit order */
function sync(){const now=C.visited();const set=new Set(now);
  if(LOG===null){LOG=now.map(id=>[id,"earlier"]);LS.set("log",LOG);return}
  const had=new Set(LOG.map(x=>x[0]));let ch=false;
  now.forEach(id=>{if(!had.has(id)&&D[id]&&C.stop(id)){LOG.push([id,today()]);ch=true}});
  const keep=LOG.filter(x=>set.has(x[0]));if(keep.length!==LOG.length){LOG=keep;ch=true}
  if(ch)LS.set("log",LOG)}
let REP=LS.get("rep",{});             /* date -> {line, ans, made} */
let SET=LS.get("set",{remind:true});
let SNOOZE=LS.get("snooze","");
function days(){sync();const m=new Map();LOG.forEach(([id,d])=>{if(!C.stop(id))return;if(!m.has(d))m.set(d,[]);m.get(d).push(id)});
  const ks=[...m.keys()].sort((a,b)=>a==="earlier"?-1:b==="earlier"?1:a.localeCompare(b));
  let n=0;return ks.map(k=>({date:k,n:k==="earlier"?0:++n,ids:m.get(k)}))}
const short=n=>String(n).split(/ — | – | \/ |, | \(|:/)[0].trim();
function dayTitle(dy){const ids=dy.ids;if(!ids.length)return"";if(C.title){const t=C.title(ids);if(t)return t}const a=short(C.stop(ids[0]).name),b=short(C.stop(ids[ids.length-1]).name);return a===b?a:`${a} to ${b}`}
function pickQ(dy){const c=dy.ids.map(id=>({id,s:C.stop(id),d:D[id]})).filter(x=>x.d&&x.d.q&&!x.d.solemn);c.sort((a,b)=>(a.s.pri||3)-(b.s.pri||3));return c[0]||null}
function remFor(dy,q){if(q)return D[q.id].rem;const c=dy.ids.filter(id=>D[id]).sort((a,b)=>(C.stop(a).pri||3)-(C.stop(b).pri||3));return c.length?D[c[0]].rem:""}
function events(dy,max){let L=dy.ids.filter(id=>D[id]).map(id=>({id,s:C.stop(id),d:D[id]}));
  if(L.length>max){L=L.slice().sort((a,b)=>(a.s.pri||3)-(b.s.pri||3)).slice(0,max)}
  const key=e=>/T00:00$/.test(e.d.sort)?e.d.sort.slice(0,11)+"12:00":e.d.sort;return L.sort((a,b)=>key(a).localeCompare(key(b)))}
function solemnIds(dy){return dy.ids.filter(id=>D[id]&&D[id].solemn)}
/* ---- the journal pages (A5): one or more pages per day, used for the preview, printing and the booklet ---- */
function pageHTML(dy,total){const T=C.theme,r=REP[dy.date]||{},q=pickQ(dy),sol=solemnIds(dy);
  const all=dy.ids.filter(id=>D[id]).map(id=>({id,s:C.stop(id),d:D[id]}));
  const key=e=>/T00:00$/.test(e.d.sort)?e.d.sort.slice(0,11)+"12:00":e.d.sort;all.sort((a,b)=>key(a).localeCompare(key(b)));
  const lab=`font-family:${T.mono};font-weight:700;font-size:10px;letter-spacing:1.6px;color:${T.faint}`;
  const HEADF=(title,ts)=>T.band?`<div style="background:${T.band};color:${T.bandInk};padding:18px 24px 14px;display:flex;flex-direction:column;gap:6px;margin:-22px -24px 0">
      <div style="display:flex;justify-content:space-between;font-weight:700;font-size:10.5px;letter-spacing:2px;opacity:.85"><span>${ESC(C.docName)}</span><span>DAY ${dy.n||"–"}${total?" OF "+total:""}</span></div>
      <span style="font-family:${T.disp};font-weight:${T.dispW};font-size:${ts}px;line-height:1.02;letter-spacing:.5px">${ESC(title)}</span>
      <span style="font-size:11px;letter-spacing:1px;opacity:.85">${ESC(longDate(dy.date).toUpperCase())} · ${ESC(C.place)}</span></div>`
    :`<div style="display:flex;justify-content:space-between;font-weight:700;font-size:10.5px;letter-spacing:1.8px;color:${T.ink2}"><span>${ESC(C.docName)}</span><span>DAY ${dy.n||"–"}${total?" OF "+total:""}</span></div>
      <div style="border-top:3px solid ${T.ink};border-bottom:1px solid ${T.ink};padding:10px 0 8px;display:flex;flex-direction:column;gap:4px">
      <span style="font-family:${T.disp};font-weight:${T.dispW};font-size:${ts}px;line-height:1.02;color:${T.title};letter-spacing:.5px">${ESC(title)}</span>
      <span style="font-size:11px;letter-spacing:1px;color:${T.ink2}">${ESC(longDate(dy.date).toUpperCase())} · ${ESC(C.place)}</span></div>`;
  const HEADM=title=>`<div style="display:flex;justify-content:space-between;font-weight:700;font-size:10.5px;letter-spacing:1.8px;color:${T.ink2};border-bottom:1px solid ${T.ink2};padding-bottom:8px"><span>${ESC(C.docName)} · ${ESC(title)}</span><span style="white-space:nowrap;padding-left:10px">CONTINUED</span></div>`;
  const ENTRY=(e,last)=>`<div style="padding:7px 0 8px;${last?"":`border-bottom:1px dashed ${T.rule};`}">
      <div style="font-size:11px;line-height:1.4;margin-bottom:2px"><span style="font-weight:700;color:${T.when};letter-spacing:.5px">${ESC(e.d.when)}</span><span style="color:${T.faint}"> · </span><b style="color:${T.ink}">${ESC(e.s.name)}</b></div>
      <p style="margin:0;font-size:11px;line-height:1.42;color:${T.ink}">${ESC(e.d.st||e.d.ev)}</p></div>`;
  const ENDB=()=>`${r.line?`<div style="display:flex;flex-direction:column;gap:5px"><span style="${lab}">WHAT STAYED WITH ME</span><p style="margin:0;font-family:${T.hand};font-size:18px;line-height:1.45">${ESC(r.line)}</p></div>`:""}
    <div style="display:flex;flex-direction:column;gap:5px;background:${T.box};padding:10px 12px"><span style="${lab}">ONE THING TO REMEMBER</span><p style="margin:0;font-size:12px;line-height:1.5">${ESC(remFor(dy,q))}</p></div>
    ${sol.length?`<div style="font-size:11.5px;line-height:1.5;color:${T.ink2}"><span style="${lab}">IN REMEMBRANCE · </span>${sol.slice(0,4).map(id=>ESC(short(C.stop(id).name))).join(" · ")}</div>`:""}`;
  const title0=dayTitle(dy).toUpperCase(),ts0=dayTitle(dy).length>26?26:32;
  /* measure real heights off-screen (fonts are loaded by now), then fill the pages */
  let M=document.getElementById("aar-measure");if(!M){M=document.createElement("div");M.id="aar-measure";M.setAttribute("aria-hidden","true");M.style.cssText="position:absolute;left:-10000px;top:0;width:456px;visibility:hidden;pointer-events:none";document.body.appendChild(M)}
  M.style.fontFamily=T.mono;const hOf=h=>{M.innerHTML=h;return M.firstElementChild?M.firstElementChild.offsetHeight:0};
  const entryH=e=>hOf(ENTRY(e,false));
  const endH=hOf(`<div style="display:flex;flex-direction:column;gap:12px">${ENDB()}</div>`);
  const headH=hOf(`<div>${HEADF(title0,ts0)}</div>`),miniH=hOf(`<div>${HEADM(title0)}</div>`);
  const INNER=700,FOOT=24,LAB=17,GAP=12,SAFE=4;
  const P=[[]];let room=INNER-headH-FOOT-LAB-GAP*3-SAFE;
  all.forEach(e=>{const h=entryH(e);if(h>room&&P[P.length-1].length){P.push([]);room=INNER-miniH-FOOT-LAB-GAP*3-SAFE}P[P.length-1].push(e);room-=h});
  if(endH+GAP>room)P.push([]);
  M.innerHTML="";
  const n=P.length,title=dayTitle(dy).toUpperCase(),ts=dayTitle(dy).length>26?26:32;
  return P.map((list,pi)=>{const last=pi===n-1;
    return `<div class="aar-page" style="width:559px;height:794px;box-sizing:border-box;background:${T.paper};color:${T.ink};padding:26px;font-family:${T.mono}">
  <div style="width:100%;height:100%;box-sizing:border-box;border:1.5px solid ${T.ink2};padding:22px 24px 18px;display:flex;flex-direction:column;gap:12px;position:relative;overflow:hidden">
  ${pi===0?HEADF(title,ts):HEADM(title)}
  ${list.length?`<div style="display:flex;flex-direction:column"><span style="${lab};margin-bottom:2px">${pi===0?"WHAT YOU SAW, IN THE ORDER IT HAPPENED":"WHAT YOU SAW, CONTINUED"}</span>${list.map((e,i)=>ENTRY(e,i===list.length-1)).join("")}</div>`:""}
  ${last?ENDB():""}
  <div style="flex-grow:1"></div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;border-top:1px solid ${T.ink2};padding-top:8px;font-size:9.5px;letter-spacing:1.3px;color:${T.ink2}"><span>${dy.ids.length} SITE${dy.ids.length===1?"":"S"} · REMEMBER · EXPLORE · RESPECT</span><span style="font-weight:700">${n>1?`PAGE ${pi+1} OF ${n} · `:""}DZ CHARLIE</span></div>
  ${last?`<div style="position:absolute;right:30px;bottom:44px;transform:rotate(-8deg);border:2.5px solid ${T.stamp};color:${T.stamp};font-family:${T.disp};font-weight:${T.dispW};font-size:14px;letter-spacing:2px;padding:3px 10px;opacity:.85;background:${T.paper}">${ESC(C.stamp)}</div>`:""}
  </div></div>`}).join("")}
function coverHTML(list){const T=C.theme,f=list[0],l=list[list.length-1],n=list.reduce((s,d)=>s+d.ids.length,0);
  const range=f.date==="earlier"||l.date==="earlier"?"":(f.date===l.date?longDate(f.date):`${longDate(f.date)} – ${longDate(l.date)}`);
  return `<div class="aar-page" style="width:559px;height:794px;box-sizing:border-box;background:${T.cover};color:${T.coverInk};padding:26px;font-family:${T.mono}">
  <div style="width:100%;height:100%;box-sizing:border-box;border:1.5px solid ${T.coverRule};padding:34px 30px 26px;display:flex;flex-direction:column;gap:18px;position:relative">
  <div style="display:flex;justify-content:space-between;font-weight:700;font-size:10.5px;letter-spacing:2px;opacity:.8"><span>FIELD RECORD · PERSONAL</span><span>DZ CHARLIE</span></div>
  <div style="flex-grow:1"></div>
  <span style="font-weight:700;font-size:13px;letter-spacing:3px;opacity:.85">${ESC(C.plural.toUpperCase())}</span>
  <span style="font-family:${T.disp};font-weight:${T.dispW};font-size:54px;line-height:.98;letter-spacing:1px">${ESC(C.coverTitle)}</span>
  <div style="border-top:3px solid ${T.coverInk};border-bottom:1px solid ${T.coverInk};padding:10px 0;display:flex;justify-content:space-between;gap:12px;font-size:12px;letter-spacing:1.2px"><span>${ESC(C.place)}</span><span>${ESC(range.toUpperCase())}</span></div>
  <div style="display:flex;flex-direction:column;gap:6px;font-size:12px;line-height:1.5;opacity:.9">${list.map(d=>`<span>${d.n?"DAY "+d.n:"EARLIER"} · ${ESC(dayTitle(d))}</span>`).join("")}</div>
  <div style="flex-grow:1"></div>
  <div style="display:flex;justify-content:space-between;font-size:10px;letter-spacing:1.8px;opacity:.8"><span>${n} SITES · ${list.length} DAY${list.length===1?"":"S"}</span><span style="font-weight:700">${ESC(C.foot)}</span></div>
  <div style="position:absolute;right:26px;top:64px;transform:rotate(8deg);border:2.5px solid ${T.coverStamp};color:${T.coverStamp};font-family:${T.disp};font-weight:${T.dispW};font-size:16px;letter-spacing:2px;padding:5px 12px">${ESC(C.done)}</div>
  </div></div>`}
/* ---- printing: one page, or the whole booklet ---- */
function printPages(html){let el=document.getElementById("aar-print");if(!el){el=document.createElement("div");el.id="aar-print";document.body.appendChild(el)}
  el.innerHTML=html;document.documentElement.classList.add("aar-printing");
  const done=()=>{document.documentElement.classList.remove("aar-printing");el.innerHTML="";window.removeEventListener("afterprint",done)};
  window.addEventListener("afterprint",done);const go=()=>{window.print();setTimeout(()=>{if(document.documentElement.classList.contains("aar-printing"))done()},60000)};
  (document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(()=>setTimeout(go,150))}
/* ---- the picture to send: drawn on a canvas, 1080 × 1350 ---- */
function wrap(ctx,t,w){const out=[];String(t).split(/\s+/).forEach(word=>{const l=out.length?out[out.length-1]:null;if(l!==null&&ctx.measureText(l+" "+word).width<=w)out[out.length-1]=l+" "+word;else out.push(word)});return out}
async function picture(dy){const T=C.theme,r=REP[dy.date]||{},W=1080,H=1350,cv=document.createElement("canvas");cv.width=W;cv.height=H;const x=cv.getContext("2d");
  try{await Promise.all([`${T.dispW} 90px ${T.dispC}`,`700 30px ${T.monoC}`,`400 30px ${T.monoC}`,`400 58px ${T.handC}`].map(f=>document.fonts.load(f)))}catch(e){}
  const D2=T.dispC,M=T.monoC,HF=T.handC;
  x.fillStyle=T.paper;x.fillRect(0,0,W,H);
  let fs=86;x.font=`${T.dispW} ${fs}px ${D2}`;let tl=wrap(x,dayTitle(dy).toUpperCase(),W-160);while(tl.length>2&&fs>54){fs-=6;x.font=`${T.dispW} ${fs}px ${D2}`;tl=wrap(x,dayTitle(dy).toUpperCase(),W-160)}
  tl=tl.slice(0,3);const band=96+fs*1.05*tl.length+110;
  x.fillStyle=T.band||T.title;x.fillRect(0,0,W,band);x.fillStyle=T.bandInk||"#efe9d2";x.textBaseline="alphabetic";
  x.font=`700 24px ${M}`;x.fillText(C.docName,80,96);const dl="DAY "+(dy.n||"–");x.fillText(dl,W-80-x.measureText(dl).width,96);
  x.font=`${T.dispW} ${fs}px ${D2}`;tl.forEach((l,i)=>x.fillText(l,80,96+fs*1.05*(i+1)));
  x.font=`400 26px ${M}`;x.fillText((C.place+" · "+longDate(dy.date)).toUpperCase(),80,band-40);
  let y=band+80;x.fillStyle=T.faint;x.font=`700 24px ${M}`;
  if(r.line){x.fillText("WHAT STAYED WITH ME",80,y);y+=74;x.fillStyle=T.ink;let hs=56;x.font=`400 ${hs}px ${HF}`;let ll=wrap(x,"“"+r.line+"”",W-160);while(ll.length>5&&hs>36){hs-=4;x.font=`400 ${hs}px ${HF}`;ll=wrap(x,"“"+r.line+"”",W-160)}
    ll.slice(0,6).forEach(l=>{x.fillText(l,80,y);y+=hs*1.35});y+=40}
  x.fillStyle=T.faint;x.font=`700 24px ${M}`;x.fillText("TODAY I STOOD WHERE",80,y);y+=20;
  let stop=false;events(dy,3).forEach((e,i,a)=>{if(stop||y+130>H-140){stop=true;return}x.font=`700 28px ${M}`;x.fillStyle=T.when;const top=y+44;x.fillText(e.d.when,80,top);x.fillStyle=T.ink;x.font=`400 28px ${M}`;
    const tl2=wrap(x,e.d.ev,W-160);tl2.slice(0,2).forEach((l,j)=>x.fillText(l,80,top+40+j*38));y=top+40+Math.min(2,tl2.length)*38;
    if(i<a.length-1&&y+150<=H-140){x.strokeStyle=T.rule;x.setLineDash([10,8]);x.lineWidth=2;x.beginPath();x.moveTo(80,y);x.lineTo(W-80,y);x.stroke();x.setLineDash([])}});
  x.fillStyle=T.ink;x.fillRect(80,H-110,W-160,3);x.font=`400 22px ${M}`;x.fillStyle=T.ink2;x.fillText(`${dy.ids.length} SITES · REMEMBER · EXPLORE · RESPECT`,80,H-68);
  x.font=`700 22px ${M}`;const ft="DZCHARLIE.COM";x.fillText(ft,W-80-x.measureText(ft).width,H-68);
  return new Promise(ok=>cv.toBlob(b=>ok(b),"image/png"))}
function fontsReady(){const T=C.theme;try{return Promise.all([`${T.dispW} 30px ${T.dispC}`,`700 12px ${T.monoC}`,`400 12px ${T.monoC}`,`400 18px ${T.handC}`].map(f=>document.fonts.load(f))).catch(()=>{})}catch(e){return Promise.resolve()}}
function fileName(dy){return `${C.fileBase}-day-${dy.n||"earlier"}.png`}
async function savePic(dy){const b=await picture(dy);const a=document.createElement("a");a.href=URL.createObjectURL(b);a.download=fileName(dy);document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},4000);msg("Picture saved to your downloads")}
async function send(dy){const r=REP[dy.date]||{};const text=`${C.docName} · Day ${dy.n||""}: ${dayTitle(dy)}${r.line?"\n\n“"+r.line+"”":""}\n\n${C.guide} · dzcharlie.com`;
  try{const b=await picture(dy),f=new File([b],fileName(dy),{type:"image/png"});
    if(navigator.canShare&&navigator.canShare({files:[f]})){await navigator.share({files:[f],title:C.docName,text});return}}catch(e){if(e&&e.name==="AbortError")return}
  try{if(navigator.share){await navigator.share({title:C.docName,text});return}}catch(e){if(e&&e.name==="AbortError")return}
  await savePic(dy);location.href="mailto:?subject="+encodeURIComponent(C.docName+" · "+dayTitle(dy))+"&body="+encodeURIComponent(text+"\n\n(The picture is in your downloads — attach it to this email.)")}
/* ---- the overlay ---- */
let S={view:"list",date:null,step:1,ans:null,draft:""};
function root(){let el=document.getElementById("aar");if(!el){el=document.createElement("div");el.id="aar";el.setAttribute("role","dialog");el.setAttribute("aria-modal","true");el.setAttribute("aria-label",C.plural);el.hidden=true;document.body.appendChild(el)}return el}
function msg(t){let el=document.getElementById("aar-toast");if(!el){el=document.createElement("div");el.id="aar-toast";el.setAttribute("role","status");document.body.appendChild(el)}el.textContent=t;el.hidden=false;clearTimeout(msg.t);msg.t=setTimeout(()=>el.hidden=true,2600)}
function open(view,date){sync();S={view:view||"list",date:date||null,step:1,ans:null,draft:""};if(S.view==="write"){const r=REP[S.date];S.draft=r&&r.line||"";if(!pickQ(dayByDate(S.date)))S.step=2}
  const el=root();el.hidden=false;document.documentElement.classList.add("aar-open");draw();el.scrollTop=0;const f=el.querySelector("h2");if(f){f.setAttribute("tabindex","-1");f.focus({preventScroll:true})}}
function close(){const el=root();el.hidden=true;document.documentElement.classList.remove("aar-open");if(C.onClose)C.onClose()}
const dayByDate=d=>days().find(x=>x.date===d);
function bar(title,sub,back){return `<div class="aar-bar"><button type="button" class="aar-ic" data-aar="${back||"close"}" aria-label="${back?"Back":"Close"}"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${back?'<path d="M15 5l-7 7 7 7"/>':'<path d="M6 6l12 12M18 6L6 18"/>'}</svg></button><div class="aar-bt"><span>${ESC(sub)}</span><b>${ESC(title)}</b></div></div>`}
function draw(){const el=root(),all=days(),total=all.filter(d=>d.n).length;let h="";
  if(S.view==="list"){const wrote=all.filter(d=>REP[d.date]);
    h=bar(C.plural.toUpperCase(),C.guide.toUpperCase())+`<div class="aar-in"><h2 class="aar-h">${ESC(C.plural)}</h2>
    <p class="aar-p">${ESC(C.intro)}</p>
    ${all.length?`<div class="aar-list">${all.map(d=>{const r=REP[d.date];return `<button type="button" class="aar-row" data-aar="write" data-date="${d.date}"><span class="aar-k">${d.n||"·"}</span><span class="aar-x"><b>${d.n?"Day "+d.n+" · ":""}${ESC(dayTitle(d))}</b><small>${ESC(longDate(d.date))} · ${d.ids.length} site${d.ids.length===1?"":"s"} visited</small></span><span class="aar-st${r?" ok":""}">${r?"Written":"Write"}</span></button>`}).join("")}</div>`
      :`<div class="aar-empty"><b>No visits yet</b><p>Tick <b>Visited</b> on each site as you see it. In the evening, come back here and write the day's page.</p></div>`}
    ${wrote.length?`<button type="button" class="aar-btn" data-aar="booklet">Make my trip booklet (${wrote.length} page${wrote.length===1?"":"s"})</button><p class="aar-note">Opens the print window: choose "Save as PDF" to keep it, or print it for your journal.</p>`:""}
    <label class="aar-sw"><input type="checkbox" data-aar="remind"${SET.remind?" checked":""}><span><b>Remind me on the Tour page</b><small>Shows "Write today's ${ESC(C.docNameShort)}" after you visit sites.</small></span></label>
    <p class="aar-note">Your pages stay on this phone. Nothing is sent anywhere unless you choose to share it.</p></div>`}
  else{const dy=dayByDate(S.date);if(!dy){S.view="list";return draw()}const q=pickQ(dy),hasQ=!!q,steps=hasQ?2:1,cur=hasQ?S.step:Math.max(1,S.step-1);
    const prog=S.step<3?`<div class="aar-prog">${Array.from({length:steps},(_,i)=>`<i class="${i<cur?"on":""}"></i>`).join("")}</div>`:"";
    const sub=`DAY ${dy.n||"–"}${S.step<3?` · STEP ${cur} OF ${steps}`:" · DONE"}`;
    if(S.step===1&&q){const d=D[q.id].q;const ans=S.ans;
      h=bar(C.docName,sub,"list")+`<div class="aar-in">${prog}<span class="aar-lab">ONE QUESTION TO REMEMBER</span><h2 class="aar-h">${ESC(d.t)}</h2>
      <div class="aar-opts" role="group" aria-label="Answers">${d.o.map((o,i)=>`<button type="button" data-aar="ans" data-i="${i}" class="${ans===null?"":(i===d.a?"right":(i===ans?"wrong":"dim"))}" aria-pressed="${ans===i}">${ESC(o)}</button>`).join("")}</div>
      ${ans!==null?`<div class="aar-card" role="status"><span class="aar-lab" style="color:var(--aar-accent)">${ans===d.a?"THAT'S RIGHT":"HERE IS WHAT HAPPENED"}</span><p>${ESC(d.x)}</p><small>${ESC(C.stop(q.id).name)}</small></div>`:""}
      <div class="aar-grow"></div><button type="button" class="aar-btn" data-aar="next"${ans===null?' aria-disabled="true"':""}>${ans===null?"Choose an answer":"Next"}</button>
      <button type="button" class="aar-link" data-aar="next">Skip the question</button></div>`}
    else if(S.step<3){h=bar(C.docName,sub,hasQ?"q":"list")+`<div class="aar-in">${prog}<span class="aar-lab">IN YOUR OWN WORDS</span><h2 class="aar-h">What stayed with you today?</h2>
      <p class="aar-p">A place, a name, a moment. One line is enough.</p>
      <label class="aar-lab" for="aar-line">YOUR LINE</label><textarea id="aar-line" maxlength="200" placeholder="${ESC(C.hint)}">${ESC(S.draft)}</textarea>
      <span class="aar-count" id="aar-cnt">${S.draft.length} of 200 letters</span>
      <div class="aar-tip">Stuck? Think of ${ESC(dy.ids.slice(0,3).map(id=>short(C.stop(id).name)).join(", "))}.</div>
      <div class="aar-grow"></div><button type="button" class="aar-btn" data-aar="make">Make my page</button><button type="button" class="aar-link" data-aar="skipline">Skip this, make the page anyway</button></div>`}
    else{h=bar(C.docName,sub,"list")+`<div class="aar-in">${(()=>{const pg=pageHTML(dy,total).split('<div class="aar-page"').slice(1).map(x=>'<div class="aar-page"'+x);return pg.map((x,i)=>`<div class="aar-prev"><div class="aar-sc">${x}</div></div>`).join("")+(pg.length>1?`<p class="aar-note">${pg.length} pages for this day. Scroll to see them all.</p>`:"")})()}
      <div class="aar-g2"><button type="button" class="aar-btn" data-aar="pic">Save picture</button><button type="button" class="aar-btn" data-aar="send">Send to family</button>
      <button type="button" class="aar-btn ghost" data-aar="print">Print page</button><button type="button" class="aar-btn ghost" data-aar="edit">Edit my line</button></div>
      <p class="aar-note">Saved in your ${ESC(C.short)}. When the trip is over, make the whole booklet from ${ESC(C.plural)}.</p>
      <button type="button" class="aar-link" data-aar="list">See all days</button></div>`}}
  el.innerHTML=h;
  const ta=el.querySelector("#aar-line");if(ta)ta.addEventListener("input",()=>{S.draft=ta.value;const c=el.querySelector("#aar-cnt");if(c)c.textContent=ta.value.length+" of 200 letters"});
  el.querySelectorAll(".aar-sc").forEach(sc=>{const w=Math.min(320,el.clientWidth-60);sc.style.transform=`scale(${w/559})`;sc.parentNode.style.width=w+"px";sc.parentNode.style.height=(794*w/559)+"px"});
}
function save(line){REP[S.date]={line:(line||"").trim(),ans:S.ans,made:Date.now()};LS.set("rep",REP)}
document.addEventListener("click",e=>{const t=e.target.closest("[data-aar]");
  if(!t){setTimeout(()=>{const b=LOG?LOG.length:0;sync();if(LOG&&LOG.length!==b&&C.onChange)C.onChange()},0);return}
  const a=t.dataset.aar;
  if(a==="open"){e.preventDefault();open("list");return}
  if(a==="today"){e.preventDefault();sync();const d=days().find(x=>x.date===today());open(d?"write":"list",d?d.date:null);return}
  if(a==="snooze"){SNOOZE=today();LS.set("snooze",SNOOZE);if(C.onChange)C.onChange();return}
  if(a==="close"){close();return}
  if(a==="list"){S.view="list";draw();return}
  if(a==="write"){open("write",t.dataset.date);const r=REP[t.dataset.date];if(r){fontsReady().then(()=>{S.step=3;draw()})}return}
  if(a==="ans"){if(S.ans===null){S.ans=+t.dataset.i;draw()}return}
  if(a==="q"){S.step=1;draw();return}
  if(a==="next"){if(t.getAttribute("aria-disabled")==="true")return;S.step=2;draw();const ta=root().querySelector("#aar-line");if(ta)ta.focus();return}
  if(a==="make"){save(S.draft);fontsReady().then(()=>{S.step=3;draw();if(C.onChange)C.onChange()});return}
  if(a==="skipline"){save("");fontsReady().then(()=>{S.step=3;draw();if(C.onChange)C.onChange()});return}
  if(a==="edit"){S.step=2;S.draft=(REP[S.date]||{}).line||"";draw();return}
  const dy=S.date&&dayByDate(S.date);
  if(a==="pic"&&dy){savePic(dy);return}
  if(a==="send"&&dy){send(dy);return}
  if(a==="print"&&dy){fontsReady().then(()=>{const tot=days().filter(d=>d.n).length;printPages(pageHTML(dy,tot))});return}
  if(a==="booklet"){fontsReady().then(()=>{const w=days().filter(d=>REP[d.date]),tot=days().filter(d=>d.n).length;if(w.length)printPages(coverHTML(w)+w.map(d=>pageHTML(d,tot)).join(""))});return}
});
document.addEventListener("change",e=>{if(e.target.dataset&&e.target.dataset.aar==="remind"){SET.remind=e.target.checked;LS.set("set",SET);if(C.onChange)C.onChange()}});
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!root().hidden){close()}});
/* ---- the card on the Tour page ---- */
function card(){if(!SET.remind)return"";sync();const all=days(),t=all.find(d=>d.date===today());
  if(t&&!REP[t.date]&&SNOOZE!==today())return `<div class="aar-cardin"><div class="aar-ch"><span class="aar-ico"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5"/><path d="M9 13h7M9 17h5"/></svg></span><span><small>${t.ids.length} SITE${t.ids.length===1?"":"S"} VISITED TODAY</small><b>Write today's ${ESC(C.docNameShort)}</b></span></div>
    <p>Two minutes. What you saw, put in the order it happened, one question, and a line of your own. You get a page for your journal.</p>
    <button type="button" class="aar-btn" data-aar="today">${ESC(C.startLabel||"Start my report")}</button><button type="button" class="aar-link" data-aar="snooze">Not tonight</button></div>`;
  const w=all.filter(d=>REP[d.date]).length;
  if(all.length)return `<button type="button" class="aar-mini" data-aar="open"><span><b>${ESC(C.plural)}</b><small>${w} of ${all.length} day${all.length===1?"":"s"} written</small></span><span aria-hidden="true">›</span></button>`;
  return ""}
window.AAR={open,card,sync,days,pageHTML,coverHTML};
sync();
})();
