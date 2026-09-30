# Add the Google-style multi-level map pictures to the Spain map (GeoMap). Works on build/map.js and on the same code inside index.html.
def rep(s, a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); return s.replace(a, b)
RAS = r'''const G=window.SCW.geo;
/* Google-style road-map pictures at several levels of detail, like the Easy Company maps (Sep 2026):
   a Spain overview plus close-ups around every group of sites. The sharpest level that suits the zoom is drawn,
   so village names and small roads appear as you zoom in. The drawn vector map stays underneath as a fallback. */
const RASTER=window.SCW_RASTER||[],RAS_PR=1.5,IMG=new Map(),ALLMAPS=new Set();
const RES=r=>r.w/(r.b[2]-r.b[0]);const FAM={};RASTER.forEach(r=>{const F=FAM[r.g]=FAM[r.g]||{};if(!(r.lv in F))F[r.lv]=RES(r)});
const LV0=Object.keys(FAM[0]||{}).map(Number).filter(l=>l>=0);const BASELV=LV0.length?Math.max(...LV0):null;
/* three tiers: 0 = Spain overview, middle areas (~1,400 px/degree), close-ups around the sites (~4,550 px/degree) */
const TOP={};Object.keys(FAM).forEach(g=>TOP[g]=Math.max(...Object.values(FAM[g])));const TIER=g=>+g===0?0:(TOP[g]<3000?1:2);
function rasPick(d,x0,x1,y0,y1){const pick={},best=[0,0,0];
  Object.keys(FAM).sort((a,b)=>TIER(a)-TIER(b)||a-b).forEach(g=>{const t=TIER(g);const lv=Object.entries(FAM[g]).map(([l,res])=>[+l,res]).filter(x=>x[0]>=0).sort((a,b)=>a[1]-b[1]);
    let c=lv.find(x=>x[1]>=d*0.8)||lv[lv.length-1];
    /* a middle area or close-up shows only where it adds detail to the tiers under it, and is never shrunk more than 4x */
    if(t>0&&(c[1]>d*4||c[1]<Math.max(best[0],t>1?best[1]:0)*1.5))c=null;
    if(c)best[t]=Math.max(best[t],c[1]);
    if(c&&c[1]<d*0.45&&(-1 in FAM[g]))c=[-1,FAM[g][-1]];pick[g]=c?c[0]:-9});
  return RASTER.filter(r=>pick[r.g]===r.lv&&r.b[2]>x0&&r.b[0]<x1&&my(r.b[3])>y0&&my(r.b[1])<y1).sort((a,b)=>TIER(a.g)-TIER(b.g)||RES(a)-RES(b))}
function rasImg(r){let o=IMG.get(r.src);if(!o){const im=new Image();o={im,ok:false};IMG.set(r.src,o);im.decoding="async";
  im.onload=()=>{o.ok=true;ALLMAPS.forEach(m=>m.draw())};im.onerror=()=>{o.bad=true};im.src=r.src}return o}'''
def patch(s):
    s = rep(s, 'const G=window.SCW.geo;', RAS)
    s = rep(s, '  this._ptr=new Map();this._raf=0;\n', '  this._ptr=new Map();this._raf=0;ALLMAPS.add(this);\n')
    s = rep(s, 'window.GeoMap=GeoMap;', 'GeoMap.all=ALLMAPS;window.GeoMap=GeoMap;')
    s = rep(s, '''  ctx.fillStyle=COL.spain;ctx.beginPath();this._polys(ctx,G.countries.Spain||[]);ctx.fill();
''', '''  ctx.fillStyle=COL.spain;ctx.beginPath();this._polys(ctx,G.countries.Spain||[]);ctx.fill();
  // road-map pictures (sharpest level for this zoom); while they load, the small overview picture shows underneath
  let ras=false,bare=false,close=false;
  if(RASTER.length){const bb=this.bounds();const want=rasPick(k*RAS_PR,bb.w,bb.e,my(bb.s),my(bb.n));
    if(want.length){ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality="high";
      const put=r=>{const o=rasImg(r);if(!o.ok)return false;const a=this.px(r.b[3],r.b[0]),b=this.px(r.b[1],r.b[2]);ctx.drawImage(o.im,a[0],a[1],b[0]-a[0]+.6,b[1]-a[1]+.6);return true};
      if(want.some(r=>!rasImg(r).ok)&&BASELV!==null)RASTER.filter(r=>r.g===0&&r.lv===BASELV&&r.b[2]>bb.w&&r.b[0]<bb.e).forEach(put);
      want.forEach(put);ras=true;bare=want.some(r=>r.g===0&&r.lv<0);close=want.some(r=>r.g>0)}}
''')
    s = rep(s, '  ctx.fillStyle=COL.mtn;ctx.beginPath();G.mtns.forEach(m=>this._polys(ctx,m.p));ctx.fill();',
               '  if(!ras){ctx.fillStyle=COL.mtn;ctx.beginPath();G.mtns.forEach(m=>this._polys(ctx,m.p));ctx.fill()}')
    s = rep(s, '  ctx.fillStyle=COL.lake;ctx.beginPath();this._polys(ctx,G.lakes);ctx.fill();',
               '  if(!ras){ctx.fillStyle=COL.lake;ctx.beginPath();this._polys(ctx,G.lakes);ctx.fill()}')
    s = rep(s, '  for(const r of G.rivers){', '  if(!ras)for(const r of G.rivers){')
    s = rep(s, '  if(k>=18){for(const pass of [0,1])', '  if(k>=18&&!ras){for(const pass of [0,1])')
    s = rep(s, '  if(k>=40){for(const m of G.mtns)', '  if(k>=40&&!ras){for(const m of G.mtns)')
    s = rep(s, '  for(const q of pl){if(q[4]>lim)continue;', '  if(!ras||(bare&&!close))for(const q of pl){if(q[4]>lim)continue;')
    s = rep(s, '  this._mk=mk;\n};', '''  if(ras){ctx.font="600 10px system-ui,sans-serif";ctx.textAlign="right";ctx.textBaseline="alphabetic";const t="© OpenStreetMap",tw=ctx.measureText(t).width,ya=this.h-(this.opt.capH||0)-4;ctx.fillStyle="rgba(255,253,247,.8)";ctx.fillRect(this.w-tw-10,ya-11,tw+8,14);ctx.fillStyle="#3c4043";ctx.fillText(t,this.w-6,ya)}
  this._mk=mk;\n};''')
    return s
if __name__ == '__main__':
    import sys
    f = sys.argv[1]; s = open(f).read(); open(sys.argv[2], 'w').write(patch(s)); print('patched', f)
