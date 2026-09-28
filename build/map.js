/* ===== GeoMap: offline vector map of Spain drawn on a canvas (no internet needed) ===== */
(function(){
const G=window.SCW.geo;
const R2D=180/Math.PI;
function mx(lon){return lon}
function my(lat){return Math.log(Math.tan(Math.PI/4+lat*Math.PI/360))*R2D}
function ilat(y){return (2*Math.atan(Math.exp(y/R2D))-Math.PI/2)*R2D}
/* Google-style road-map colours (Sep 2026) */
const COL={sea:"#aadaff",land:"#f5f3ee",spain:"#f5f3ee",other:"#e8e6e1",prov:"rgba(120,114,140,.45)",reg:"rgba(95,60,30,.55)",river:"#8cc4f0",lake:"#aadaff",road:"#fde293",roadC:"#e0b95a",road1:"#f9bf5a",road1C:"#d18f2b",mtn:"rgba(150,140,110,.07)",txt:"#202124",halo:"rgba(255,255,255,.92)"};
function GeoMap(box,opt){
  opt=opt||{};this.opt=opt;this.box=box;
  const c=document.createElement("canvas");box.appendChild(c);this.c=c;this.ctx=c.getContext("2d");
  this.markers=[];this.ov={};this.sel=null;this.hl=null;
  this.cx=mx(-3.7);this.cy=my(40.2);this.k=40; // px per degree
  this.minK=18;this.maxK=9000;
  this._ptr=new Map();this._raf=0;
  const ro=new ResizeObserver(()=>this.resize());ro.observe(box);this.resize();
  this._bind();
}
GeoMap.prototype.resize=function(){const r=this.box.getBoundingClientRect();const d=Math.min(window.devicePixelRatio||1,2.5);
  this.w=Math.max(10,r.width);this.h=Math.max(10,r.height);this.c.width=this.w*d;this.c.height=this.h*d;this.dpr=d;
  if(!this._fitted&&this._pendingFit){this.fit(this._pendingFit[0],this._pendingFit[1]);}
  this.draw()};
GeoMap.prototype.px=function(lat,lon){return[(mx(lon)-this.cx)*this.k+this.w/2,(this.cy-my(lat))*this.k+this.h/2]};
GeoMap.prototype.ll=function(x,y){return[ilat(this.cy-(y-this.h/2)/this.k),this.cx+(x-this.w/2)/this.k]};
GeoMap.prototype.bounds=function(){const a=this.ll(0,this.h),b=this.ll(this.w,0);return{s:a[0],w:a[1],n:b[0],e:b[1]}};
GeoMap.prototype.fit=function(pts,pad){ // pts: [[lat,lon],...]
  if(!pts||!pts.length)return;pad=pad==null?40:pad;
  if(this.w<20){this._pendingFit=[pts,pad];return}
  let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;pts.forEach(p=>{const x=mx(p[1]),y=my(p[0]);x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y)});
  const dx=Math.max(x1-x0,0.02),dy=Math.max(y1-y0,0.02);
  this.k=Math.max(this.minK,Math.min(this.maxK*0.3,Math.min((this.w-2*pad)/dx,(this.h-2*pad)/dy)));
  this.cx=(x0+x1)/2;this.cy=(y0+y1)/2;this._fitted=true;this.draw()};
GeoMap.prototype.fitSpain=function(){this.fit([[43.8,-9.3],[36.0,3.3]],12)};
GeoMap.prototype.zoomAt=function(f,x,y){const nk=Math.max(this.minK,Math.min(this.maxK,this.k*f));f=nk/this.k;
  if(x==null){x=this.w/2;y=this.h/2}
  const wx=this.cx+(x-this.w/2)/this.k, wy=this.cy-(y-this.h/2)/this.k;
  this.k=nk;this.cx=wx-(x-this.w/2)/this.k;this.cy=wy+(y-this.h/2)/this.k;this.draw();this._moved()};
GeoMap.prototype.center=function(lat,lon,k){this.cx=mx(lon);this.cy=my(lat);if(k)this.k=k;this.draw()};
GeoMap.prototype._moved=function(){clearTimeout(this._mt);this._mt=setTimeout(()=>{this.opt.onMove&&this.opt.onMove(this.bounds())},180)};
GeoMap.prototype.draw=function(){if(this._raf)return;this._raf=requestAnimationFrame(()=>{this._raf=0;this._draw()})};
GeoMap.prototype._path=function(ctx,ring){let first=true;for(const p of ring){const x=(p[0]-this.cx)*this.k+this.w/2,y=(this.cy-my(p[1]))*this.k+this.h/2;if(first){ctx.moveTo(x,y);first=false}else ctx.lineTo(x,y)}};
GeoMap.prototype._polys=function(ctx,polys){for(const pl of polys){for(const ring of pl){this._path(ctx,ring);ctx.closePath()}}};
GeoMap.prototype._draw=function(){
  const ctx=this.ctx,d=this.dpr;ctx.setTransform(d,0,0,d,0,0);const k=this.k;
  ctx.fillStyle=COL.sea;ctx.fillRect(0,0,this.w,this.h);
  // land & countries
  ctx.fillStyle=COL.other;ctx.beginPath();this._polys(ctx,G.land);ctx.fill();
  ctx.fillStyle=COL.spain;ctx.beginPath();this._polys(ctx,G.countries.Spain||[]);ctx.fill();
  // mountains
  ctx.fillStyle=COL.mtn;ctx.beginPath();G.mtns.forEach(m=>this._polys(ctx,m.p));ctx.fill();
  // region highlight
  const sel=this.sel;
  if(sel&&sel.size){ctx.fillStyle="rgba(168,50,31,.16)";ctx.beginPath();window.SCW.regions.forEach(r=>{if(sel.has(r.id))this._polys(ctx,r.poly)});ctx.fill()}
  if(this.hl){ctx.fillStyle="rgba(194,138,44,.18)";ctx.beginPath();window.SCW.regions.forEach(r=>{if(r.id===this.hl)this._polys(ctx,r.poly)});ctx.fill()}
  // lakes
  ctx.fillStyle=COL.lake;ctx.beginPath();this._polys(ctx,G.lakes);ctx.fill();
  // rivers
  ctx.strokeStyle=COL.river;ctx.lineCap="round";ctx.lineJoin="round";
  for(const r of G.rivers){if(r.r>7&&k<120)continue;if(r.r>5&&k<60)continue;ctx.lineWidth=r.r<=3?1.8:(r.r<=6?1.3:0.9);ctx.beginPath();for(const l of r.l)this._path(ctx,l);ctx.stroke()}
  // roads
  if(k>=18){for(const pass of [0,1])for(const t of [2,1])for(const r of G.roads){if(r.t!==t)continue;if(r.t!==1&&k<110)continue;const w=r.t===1?(k<40?1.1:k<90?2:3):(k<250?1.6:2.2);ctx.strokeStyle=pass?(r.t===1?COL.road1:COL.road):(r.t===1?COL.road1C:COL.roadC);ctx.lineWidth=pass?w:w+1.6;ctx.beginPath();for(const l of r.l)this._path(ctx,l);ctx.stroke()}}
  // provinces
  if(k>=55){ctx.strokeStyle=COL.prov;ctx.lineWidth=1;ctx.setLineDash([2,3]);ctx.beginPath();for(const p of G.prov)for(const l of p.b)this._path(ctx,l);ctx.stroke();ctx.setLineDash([])}
  // regions
  ctx.strokeStyle=COL.reg;ctx.lineWidth=1.6;ctx.setLineDash([7,4]);ctx.beginPath();window.SCW.regions.forEach(r=>this._polys(ctx,r.poly));ctx.stroke();ctx.setLineDash([]);
  // labels: regions at low zoom
  ctx.textAlign="center";ctx.textBaseline="middle";
  const taken=[];const free=(x,y,w,h)=>{for(const t of taken)if(x<t[0]+t[2]&&x+w>t[0]&&y<t[1]+t[3]&&y+h>t[1])return false;taken.push([x,y,w,h]);return true};
  const lab=(s,x,y,font,col,halo)=>{ctx.font=font;const w=ctx.measureText(s).width;if(!free(x-w/2-2,y-8,w+4,16))return false;ctx.lineWidth=3.5;ctx.strokeStyle=halo||COL.halo;ctx.strokeText(s,x,y);ctx.fillStyle=col||COL.txt;ctx.fillText(s,x,y);return true};
  // markers first reserve space (drawn later) -> collect
  const mk=this._layoutMarkers();
  mk.forEach(m=>taken.push([m.x-m.r,m.y-m.r,2*m.r,2*m.r]));
  if(this.opt.regionLabels!==false&&k<140){window.SCW.regions.forEach(r=>{const p=this.px(r.lab[0],r.lab[1]);lab(r.short.toUpperCase(),p[0],p[1],"800 13px "+getComputedStyle(document.body).getPropertyValue("--disp"),"rgba(90,64,48,.8)","rgba(241,230,201,.7)")})}
  if(k>=40){for(const m of G.mtns){const p=this.px(m.c[0],m.c[1]);if(p[0]<-50||p[0]>this.w+50||p[1]<-20||p[1]>this.h+20)continue;lab(m.n,p[0],p[1],"italic 600 11px Georgia,serif","rgba(110,80,50,.85)")}}
  // places
  const pl=G.places;const lim=k<45?1:(k<90?2:(k<250?3:4));
  for(const q of pl){if(q[4]>lim)continue;const p=this.px(q[1],q[2]);if(p[0]<-40||p[0]>this.w+40||p[1]<-20||p[1]>this.h+20)continue;
    ctx.fillStyle=COL.txt;ctx.beginPath();ctx.arc(p[0],p[1],q[4]<=2?3:2.2,0,7);ctx.fill();
    ctx.textAlign="left";ctx.font=(q[4]<=2?"700 13.5px ":"500 12px ")+"system-ui,sans-serif";lab(q[0],p[0]+5+ctx.measureText(q[0]).width/2,p[1]-1,(q[4]<=2?"700 13.5px ":"500 12px ")+"system-ui,sans-serif",q[4]<=2?"#202124":"#3c4043");ctx.textAlign="center"}
  // overlays
  const ov=this.ov;
  if(ov.circle){const c=ov.circle;const p=this.px(c.la,c.lo);const r=c.km/111.32/Math.cos(c.la*Math.PI/180)*this.k*1; // approx in lon-deg units
    const rpx=c.km/(111.32*Math.cos(c.la*Math.PI/180))*this.k;ctx.fillStyle="rgba(26,115,232,.12)";ctx.strokeStyle="#1a73e8";ctx.lineWidth=2;ctx.beginPath();ctx.arc(p[0],p[1],rpx,0,7);ctx.fill();ctx.stroke();
    ctx.fillStyle="#1a73e8";ctx.beginPath();ctx.arc(p[0],p[1],5,0,7);ctx.fill()}
  if(ov.line&&ov.line.length>1){ctx.strokeStyle=ov.lineColor||"rgba(168,50,31,.85)";ctx.lineWidth=ov.lineWidth||2.5;ctx.setLineDash(ov.dash||[6,5]);ctx.beginPath();ov.line.forEach((q,i)=>{const p=this.px(q[0],q[1]);i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1])});ctx.stroke();ctx.setLineDash([])}
  if(ov.me){const p=this.px(ov.me[0],ov.me[1]);ctx.fillStyle="rgba(26,115,232,.25)";ctx.beginPath();ctx.arc(p[0],p[1],14,0,7);ctx.fill();ctx.fillStyle="#1a73e8";ctx.strokeStyle="#fff";ctx.lineWidth=2.5;ctx.beginPath();ctx.arc(p[0],p[1],6.5,0,7);ctx.fill();ctx.stroke()}
  // markers
  ctx.textAlign="center";ctx.textBaseline="middle";
  for(const m of mk){
    if(m.cl){ctx.fillStyle="rgba(61,43,31,.92)";ctx.strokeStyle="#f7f1e2";ctx.lineWidth=2.5;ctx.beginPath();ctx.arc(m.x,m.y,m.r,0,7);ctx.fill();ctx.stroke();ctx.fillStyle="#fff";ctx.font="800 13px system-ui,sans-serif";ctx.fillText(m.n,m.x,m.y+.5);continue}
    const s=m.m;const on=this.focus===s.id;
    ctx.fillStyle=s.fill||"#fffdf7";ctx.strokeStyle=on?"#1a73e8":(s.ring||"#3d2b1f");ctx.lineWidth=on?4:2.2;
    if(s.shape==="sq"){ctx.beginPath();ctx.rect(m.x-m.r,m.y-m.r,2*m.r,2*m.r);ctx.fill();ctx.stroke()}else{ctx.beginPath();ctx.arc(m.x,m.y,m.r,0,7);ctx.fill();ctx.stroke()}
    ctx.fillStyle=s.tc||"#3d2b1f";ctx.font="800 "+(String(s.label).length>2?10.5:12)+"px system-ui,sans-serif";ctx.fillText(s.label,m.x,m.y+.5);
    if(s.cert==="MEDIUM"||s.cert==="LOW"){if(k>600){const rpx=(s.cert==="LOW"?2:0.6)/(111.32*Math.cos(s.la*Math.PI/180))*this.k;if(rpx>m.r+4){ctx.strokeStyle="rgba(168,50,31,.55)";ctx.lineWidth=1.5;ctx.setLineDash([4,4]);ctx.beginPath();ctx.arc(m.x,m.y,rpx,0,7);ctx.stroke();ctx.setLineDash([])}}}
  }
  // scale bar
  const kmpx=111.32*Math.cos(this.ll(this.w/2,this.h/2)[0]*Math.PI/180)/this.k;let km=[1,2,5,10,20,50,100,200,500].find(v=>v/kmpx>60)||500;const L=km/kmpx;
  const x0=10,y0=this.h-(this.opt.capH||0)-12;ctx.fillStyle="rgba(255,253,247,.85)";ctx.fillRect(x0-4,y0-16,L+40,22);ctx.strokeStyle=COL.txt;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x0,y0-4);ctx.lineTo(x0,y0);ctx.lineTo(x0+L,y0);ctx.lineTo(x0+L,y0-4);ctx.stroke();ctx.fillStyle=COL.txt;ctx.font="700 11px system-ui";ctx.textAlign="left";ctx.fillText(km+" km",x0+L+5,y0-4);
  this._mk=mk;
};
GeoMap.prototype._layoutMarkers=function(){
  const out=[];const r=this.opt.r||13;const cellPx=this.opt.cluster===false?0:30;
  const vis=this.markers.map(m=>{const p=this.px(m.la,m.lo);return{m,x:p[0],y:p[1]}}).filter(o=>o.x>-30&&o.x<this.w+30&&o.y>-30&&o.y<this.h+30);
  if(!cellPx||this.k>=this.opt.clusterUntil){vis.forEach(o=>out.push({m:o.m,x:o.x,y:o.y,r}));return out}
  const used=new Set();const order=vis.slice().sort((a,b)=>(a.m.pri||3)-(b.m.pri||3));
  for(const o of order){if(used.has(o))continue;const grp=[o];used.add(o);for(const q of order){if(used.has(q))continue;if(Math.abs(q.x-o.x)<cellPx&&Math.abs(q.y-o.y)<cellPx){grp.push(q);used.add(q)}}
    if(grp.length===1)out.push({m:o.m,x:o.x,y:o.y,r});else{const x=grp.reduce((a,b)=>a+b.x,0)/grp.length,y=grp.reduce((a,b)=>a+b.y,0)/grp.length;out.push({cl:true,n:grp.length,x,y,r:14+Math.min(8,grp.length),g:grp.map(g=>g.m)})}}
  return out};
GeoMap.prototype.setMarkers=function(list){this.markers=list||[];this.draw()};
GeoMap.prototype._hit=function(x,y){const mk=this._mk||[];for(let i=mk.length-1;i>=0;i--){const m=mk[i];if(Math.hypot(m.x-x,m.y-y)<=m.r+8)return m}return null};
GeoMap.prototype._bind=function(){
  const c=this.c;let last=null,moved=0,pinch=null,lastTap=0;
  const pos=e=>{const r=c.getBoundingClientRect();return[e.clientX-r.left,e.clientY-r.top]};
  c.addEventListener("pointerdown",e=>{c.setPointerCapture(e.pointerId);this._ptr.set(e.pointerId,pos(e));moved=0;
    if(this._ptr.size===2){const [a,b]=[...this._ptr.values()];pinch={d:Math.hypot(a[0]-b[0],a[1]-b[1]),k:this.k}}last=pos(e)});
  c.addEventListener("pointermove",e=>{if(!this._ptr.has(e.pointerId))return;const p=pos(e);this._ptr.set(e.pointerId,p);
    if(this._ptr.size===2&&pinch){const [a,b]=[...this._ptr.values()];const d=Math.hypot(a[0]-b[0],a[1]-b[1]);const f=(pinch.k*d/pinch.d)/this.k;this.zoomAt(f,(a[0]+b[0])/2,(a[1]+b[1])/2);moved+=10;return}
    if(last){const dx=p[0]-last[0],dy=p[1]-last[1];moved+=Math.abs(dx)+Math.abs(dy);this.cx-=dx/this.k;this.cy+=dy/this.k;last=p;this.draw();this._moved()}});
  const up=e=>{const p=pos(e);this._ptr.delete(e.pointerId);if(this._ptr.size<2)pinch=null;
    if(this._ptr.size===0){ if(moved<8){const now=Date.now();
        const h=this._hit(p[0],p[1]);
        if(h){if(h.cl){this.zoomAt(2.4,h.x,h.y)}else this.opt.onTap&&this.opt.onTap(h.m)}
        else{ if(now-lastTap<320)this.zoomAt(2,p[0],p[1]); else this.opt.onMapTap&&this.opt.onMapTap(this.ll(p[0],p[1]))}
        lastTap=now}
      last=null}else{last=[...this._ptr.values()][0]}};
  c.addEventListener("pointerup",up);c.addEventListener("pointercancel",e=>{this._ptr.delete(e.pointerId);last=null;pinch=null});
  c.addEventListener("wheel",e=>{e.preventDefault();const p=pos(e);this.zoomAt(Math.exp(-e.deltaY*0.0022),p[0],p[1])},{passive:false});
  c.setAttribute("tabindex","0");c.setAttribute("role","application");c.setAttribute("aria-label",this.opt.label||"Map of Spain. Use the plus and minus buttons to zoom; the list below has every stop.");
  c.addEventListener("keydown",e=>{const s=60/this.k;if(e.key==="ArrowLeft")this.cx-=s;else if(e.key==="ArrowRight")this.cx+=s;else if(e.key==="ArrowUp")this.cy+=s;else if(e.key==="ArrowDown")this.cy-=s;else if(e.key==="+"||e.key==="=")return this.zoomAt(1.5);else if(e.key==="-")return this.zoomAt(1/1.5);else return;e.preventDefault();this.draw();this._moved()});
  if(this.opt.controls!==false){const z=document.createElement("div");z.className="mz";
    z.innerHTML='<button type="button" aria-label="Zoom in">+</button><button type="button" aria-label="Zoom out">−</button><button type="button" aria-label="Show all of Spain"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg></button>'+(this.opt.expand?'<button type="button" aria-label="Full screen map"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M14 4h6v6M10 20H4v-6M20 4l-7 7M4 20l7-7"/></svg></button>':"");
    const b=z.querySelectorAll("button");b[0].onclick=()=>this.zoomAt(1.8);b[1].onclick=()=>this.zoomAt(1/1.8);b[2].onclick=()=>{this.opt.home?this.opt.home():this.fitSpain();this._moved()};if(b[3])b[3].onclick=()=>this.opt.expand();
    this.box.appendChild(z)}
};
GeoMap.prototype.regionAt=function(lat,lon){const x=lon,y=lat;const inRing=(ring)=>{let ins=false;for(let i=0,j=ring.length-1;i<ring.length;j=i++){const xi=ring[i][0],yi=ring[i][1],xj=ring[j][0],yj=ring[j][1];if(((yi>y)!==(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi))ins=!ins}return ins};
  for(const r of window.SCW.regions){for(const pl of r.poly){if(inRing(pl[0]))return r.id}}return null};
window.GeoMap=GeoMap;
})();
