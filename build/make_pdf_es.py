# Makes the Spanish (Castilian) printable PDF from the Spanish app (app/es.html).
# Same layout as make_pdf.py. Run from the project folder:  python3 build/make_pdf_es.py
# Output: app/pdf/La-Guerra-Civil-espanola-guia-de-campo.pdf
import json, html, asyncio, re, os, threading, http.server, functools
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, 'app')
OUT = os.path.join(APP, 'pdf', 'La-Guerra-Civil-espanola-guia-de-campo.pdf')

h = open(os.path.join(APP, 'es.html'), encoding='utf-8').read()
i = h.find('window.SCW='); j = h.find('</script>', i)
D = json.loads(h[i + len('window.SCW='):j].strip().rstrip(';'))
# Spanish labels for the English codes kept in the data (same table the app uses)
i = h.find('const TR={'); j = h.find('};', i)
TR = json.loads(re.sub(r'([{,]\s*)([A-Za-z]+):', r'\1"\2":', h[i + 9:j + 1]))
tr = lambda g, v: TR.get(g, {}).get(v, v)

E = lambda s: html.escape(str(s or ''))
fmt = lambda x: f'{x:.5f}'.replace('.', ',')
for n, s in enumerate(D['stops']): s['no'] = n + 1

P = []
P.append(f'''<section class="cover"><div class="doc"><span>PARTE DE GUERRA · GUÍA DE CAMPO</span><span>1936–1939</span></div><h1>La Guerra<br>Civil española<span>1936–1939</span></h1><p class="sub">Una guía de campo de DZ Charlie por los frentes, los pueblos en ruinas, los refugios y los lugares de memoria de toda España.</p><p class="stamp">{len(D["stops"])} LUGARES · {len(D["regions"])} ZONAS</p><p class="note">Guía gratuita · dzcharlie.com · Edición impresa de la guía para el móvil. Cada ubicación lleva una valoración de la certeza que tenemos sobre el punto exacto: ALTA (lugar exacto conocido), MEDIA (zona correcta), BAJA (solo zona general).</p></section>''')
P.append('<section><h2>Índice</h2><ol class="toc">' + ''.join(f'<li>{E(r["name"])} <span>{sum(1 for s in D["stops"] if s["r"]==r["id"])} lugares</span></li>' for r in D['regions']) + '<li>Cronología</li><li>Personajes</li><li>Glosario</li></ol>')
P.append('<h2>La guerra en breve</h2>' + ''.join(f'<h3>{E(b["h"])}</h3><p>{E(b["t"])}</p>' for b in D['brief']) + '</section>')
for r in D['regions']:
    P.append(f'<section class="reg"><h2>{E(r["name"])}</h2><img class="rimg" src="../app/{r["img"]}"><p class="cap">{E(r["cap"])}</p><p class="lede">{E(r["blurb"])}</p>')
    for s in [s for s in D['stops'] if s['r'] == r['id']]:
        P.append(f'''<div class="stop"><div class="sh"><span class="no">{s["no"]}</span><div><b>{E(s["n"])}</b><div class="meta"><span class="c c-{s["c"]}">{tr("c", s["c"])}</span> {E(s["tw"])} · {E(tr("k", s["k"]))} · {E(s["d"])} · ≈{s["m"]} min{" · ★ imprescindible" if s["p"]==1 else ""}</div></div></div>
<p>{E(s["t"])}</p><p class="look"><b>Qué se puede ver hoy:</b> {E(s["lk"])}</p><p class="plan"><b>Prepara la visita:</b> {E(s["pl"])}{" <b>Terreno privado: obsérvalo solo desde la carretera o un camino público.</b>" if s["pv"] else ""}</p>{f'<p class="disp"><b>Donde las fuentes discrepan:</b> {E(s["ds"])}</p>' if s.get("ds") else ""}<p class="gps">GPS {fmt(s["la"])}; {fmt(s["lo"])}</p></div>''')
    P.append('</section>')
P.append('<section><h2>Cronología</h2>' + ''.join(f'<p class="tl"><b>{E(t["date"])}</b> — <b>{E(t["title"])}</b> ({E(t["place"])}). {E(t["t"])}</p>' for t in D['time']) + '</section>')
P.append('<section><h2>Personajes</h2>' + ''.join(f'<p class="tl"><b>{E(p["name"])}</b> ({E(tr("side", p["side"]))}; {E(p["dates"])}) — {E(p["role"])}. {E(p["t"])}</p>' for p in D['people']) + '</section>')
P.append('<section><h2>Glosario</h2>' + ''.join(f'<p class="tl"><b>{E(g[0])}</b> — {E(g[1])}</p>' for g in D['gloss']) + '<h2>Créditos</h2>' + ''.join(f'<p class="cap">{E(c)}</p>' for c in D['credits']) + '<p class="cap">Mapas base: Natural Earth. Ubicaciones comprobadas con Wikipedia, Wikidata, OpenStreetMap (© colaboradores de OpenStreetMap), TracesOfWar, Mapcarta e inventarios oficiales de patrimonio.</p></section>')

css = open(os.path.join(ROOT, 'build', 'make_pdf.py'), encoding='utf-8').read()
css = css[css.index("css='''") + 7:]; css = css[:css.index("'''")].replace('../site/', '../app/')
doc = '<!doctype html><html lang="es"><head><meta charset="utf-8"><style>' + css + '</style></head><body>' + ''.join(P) + '</body></html>'
open(os.path.join(ROOT, 'build', 'print_es.html'), 'w', encoding='utf-8').write(doc)

srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8901), functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto('http://127.0.0.1:8901/build/print_es.html'); await pg.wait_for_timeout(1500)
        await pg.pdf(path=OUT, format='A4', print_background=True, display_header_footer=True, header_template='<span></span>',
                     footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#6f6150">La Guerra Civil española 1936–1939 · Guía de campo de DZ Charlie · <span class="pageNumber"></span></div>',
                     margin={'top': '16mm', 'bottom': '16mm', 'left': '15mm', 'right': '15mm'})
        await b.close()
asyncio.run(main()); srv.shutdown()
print('PDF made:', OUT)
