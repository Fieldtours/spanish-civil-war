import json,html,asyncio,re
from playwright.async_api import async_playwright
D=json.loads(open('build/data.js').read()[len('window.SCW='):-1])
E=lambda s:html.escape(str(s or ''))
PH={p['id']:p for p in D['phases']}
for i,s in enumerate(D['stops']): s['no']=i+1
parts=[]
parts.append(f'''<section class="cover"><div class="doc"><span>PARTE DE GUERRA · FIELD GUIDE</span><span>1936–1939</span></div><h1>The Spanish<br>Civil War<span>1936–1939</span></h1><p class="sub">A DZ Charlie field guide to the fronts, the ruined villages, the shelters and the places of memory — across the whole of Spain.</p><p class="stamp">{len(D["stops"])} SITES · 8 AREAS</p><p class="note">Free guide · dzcharlie.com · Printed edition of the phone guide. Positions carry a rating for how sure we are of the exact spot: HIGH (exact spot known), MEDIUM (right area), LOW (general area only).</p></section>''')
parts.append('<section><h2>Contents</h2><ol class="toc">'+''.join(f'<li>{E(r["name"])} <span>{sum(1 for s in D["stops"] if s["r"]==r["id"])} sites</span></li>' for r in D['regions'])+'<li>Timeline</li><li>People</li><li>Words to know</li></ol>')
parts.append('<h2>The war in brief</h2>'+''.join(f'<h3>{E(b["h"])}</h3><p>{E(b["t"])}</p>' for b in D['brief'])+'</section>')
for r in D['regions']:
  L=[s for s in D['stops'] if s['r']==r['id']]
  parts.append(f'<section class="reg"><h2>{E(r["name"])}</h2><img class="rimg" src="../site/{r["img"]}"><p class="cap">{E(r["cap"])}</p><p class="lede">{E(r["blurb"])}</p><img class="rmap" src="pdfmaps/en-{r["id"]}.jpg" alt="Map of {E(r["name"])}"><p class="cap">The numbers on the map are the sites in this chapter. Map data © OpenStreetMap contributors.</p>')
  for s in L:
    parts.append(f'''<div class="stop"><div class="sh"><span class="no">{s["no"] if "no" in s else ""}</span><div><b>{E(s["n"])}</b><div class="meta"><span class="c c-{s["c"]}">{s["c"]}</span> {E(s["tw"])} · {E(s["k"])} · {E(s["d"])} · ≈{s["m"]} min{" · ★ must see" if s["p"]==1 else ""}</div></div></div>
<p>{E(s["t"])}</p><p class="look"><b>What you can see:</b> {E(s["lk"])}</p><p class="plan"><b>Plan:</b> {E(s["pl"])}{" <b>Private land — view from the road.</b>" if s["pv"] else ""}</p>{f'<p class="disp"><b>Where sources disagree:</b> {E(s["ds"])}</p>' if s["ds"] else ""}<p class="gps">GPS {s["la"]:.5f}, {s["lo"]:.5f}</p></div>''')
  parts.append('</section>')
parts.append('<section><h2>Timeline</h2>'+''.join(f'<p class="tl"><b>{E(t["date"])}</b> — <b>{E(t["title"])}</b> ({E(t["place"])}). {E(t["t"])}</p>' for t in D['time'])+'</section>')
parts.append('<section><h2>People</h2>'+''.join(f'<p class="tl"><b>{E(p["name"])}</b> ({E(p["side"])}; {E(p["dates"])}) — {E(p["role"])}. {E(p["t"])}</p>' for p in D['people'])+'</section>')
parts.append('<section><h2>Words to know</h2>'+''.join(f'<p class="tl"><b>{E(g[0])}</b> — {E(g[1])}</p>' for g in D['gloss'])+'<h2>Credits</h2>'+''.join(f'<p class="cap">{E(c)}</p>' for c in D['credits'])+'<p class="cap">Base maps: Natural Earth; area maps: © OpenStreetMap contributors (openstreetmap.org/copyright). Positions checked against Wikipedia, Wikidata, OpenStreetMap (© OpenStreetMap contributors), TracesOfWar, Mapcarta and official heritage inventories.</p></section>')
# numbering like app
for i,s in enumerate(D['stops']): s['no']=i+1
css='''@font-face{font-family:BSS;src:url(../site/fonts/bss-800.woff2)}@font-face{font-family:SE;src:url(../site/fonts/special-elite-400.woff2)}
@page{size:A4;margin:16mm 15mm 16mm 15mm}
body{font-family:Georgia,serif;font-size:10.5pt;line-height:1.45;color:#1f1a14}
h1,h2,h3{font-family:BSS,Impact,sans-serif;text-transform:uppercase;color:#3d2b1f;letter-spacing:.5px}
h2{font-size:26pt;margin:0 0 8px;border-bottom:3px double #a8321f;padding-bottom:4px}
h3{font-size:14pt;margin:12px 0 2px}
section{page-break-before:always}
section.cover{page-break-before:auto;box-sizing:border-box;height:258mm;background:#3d2b1f url(../site/welcome.jpg) center/cover;color:#fff;padding:18mm 14mm;position:relative}
.cover .doc{display:flex;justify-content:space-between;font-family:SE;font-size:9pt;letter-spacing:2px;border-bottom:1px dashed rgba(255,255,255,.5);padding-bottom:6px;background:rgba(0,0,0,.4)}
.cover h1{font-size:60pt;line-height:.9;color:#fff;margin-top:60mm;text-shadow:0 2px 12px rgba(0,0,0,.6)}.cover h1 span{display:block;color:#f0c46b}
.cover .sub{font-family:SE;font-size:13pt;background:rgba(0,0,0,.45);padding:6px}
.cover .stamp{display:inline-block;border:3px solid #ff9b87;color:#ff9b87;font-family:BSS;font-size:16pt;padding:2px 10px;transform:rotate(-5deg);background:rgba(0,0,0,.35)}
.cover .note{position:absolute;bottom:14mm;left:14mm;right:14mm;font-size:9pt;background:rgba(0,0,0,.55);padding:6px}
.toc li{font-size:13pt;margin:4px 0}.toc span{color:#6f6150;font-size:10pt}
.rimg{width:100%;max-height:70mm;object-fit:cover}
.rmap{width:100%;display:block;border:1px solid #c9b994;margin:8px 0 2px;break-inside:avoid}
.cap{font-size:8.5pt;color:#6f6150;margin:2px 0 8px}
.lede{font-style:italic}
.stop{break-inside:avoid;border-top:1px dashed #c9b994;padding:8px 0 4px}
.sh{display:flex;gap:8px;align-items:flex-start}.no{flex:0 0 26px;height:26px;border:2px solid #3d2b1f;border-radius:50%;text-align:center;font-family:BSS;font-size:12pt;line-height:24px}
.sh b{font-size:12pt;font-family:Helvetica,Arial,sans-serif}
.meta{font-size:8.5pt;color:#6f6150;font-family:Helvetica,Arial,sans-serif}
.c{font-weight:bold;padding:0 5px;border-radius:6px;color:#fff}.c-HIGH{background:#2e7d32}.c-MEDIUM{background:#f2c200;color:#1c1a15}.c-LOW{background:#c62828}
.stop p{margin:4px 0}.look,.plan{font-size:9.5pt}.disp{font-size:9pt;border:1px dashed #a8321f;padding:3px 5px}.gps{font-family:monospace;font-size:8.5pt;color:#6f6150}
.tl{font-size:9.5pt;margin:0 0 5px}'''
# rebuild parts with numbers (regions loop used s["no"] before assignment -> regenerate)
doc='<!doctype html><html><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(parts)+'</body></html>'
doc=re.sub(r'<span class="no"></span>','<span class="no">?</span>',doc)
open('build/print.html','w').write(doc)

async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page()
    await pg.goto('http://localhost:8900/build/print.html');await pg.wait_for_timeout(1500)
    await pg.pdf(path='/home/claude/scw/site/pdf/The-Spanish-Civil-War-field-guide.pdf',format='A4',print_background=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#6f6150">The Spanish Civil War 1936–1939 · DZ Charlie field guide · <span class="pageNumber"></span></div>',margin={'top':'16mm','bottom':'16mm','left':'15mm','right':'15mm'})
    await b.close()
import os;os.makedirs('/home/claude/scw/site/pdf',exist_ok=True)
asyncio.run(main())
