"""Build Spanish versions of the DZ Charlie Spanish Civil War place pages.

usage: build.py SRC_DIR ES_JSON_DIR OUT_DIR
  SRC_DIR      English pages (places/spanish-civil-war/*.html)
  ES_JSON_DIR  translated JSON (es/*.json)
  OUT_DIR      gets es/guerra-civil/*.html and places/spanish-civil-war/*.html (English pages with links to Spanish)
"""
import glob, html, json, os, re, sys
from bs4 import BeautifulSoup

SRC, ESJ, OUT = sys.argv[1:4]
SITE = "https://dzcharlie.com"
EN_BASE = "/places/spanish-civil-war/"
ES_BASE = "/es/guerra-civil/"
GUIDE = "Guerra Civil española 1936–1939"

AREA = {"Aragon": "Aragón", "Madrid & the Centre": "Madrid y el centro", "The North": "El norte",
        "Andalusia": "Andalucía", "Catalonia & the Ebro": "Cataluña y el Ebro", "Extremadura": "Extremadura",
        "Castile, León, Galicia, Navarre & La Rioja": "Castilla, León, Galicia, Navarra y La Rioja",
        "Valencia, Murcia & the Balearics": "Valencia, Murcia y Baleares"}
TYPE = {"Trenches & fortifications": "Trincheras y fortificaciones", "Memorial": "Memorial",
        "Repression & memory site": "Lugar de represión y memoria", "Air-raid shelter": "Refugio antiaéreo",
        "City site": "Lugar urbano", "Battlefield": "Campo de batalla", "Ruined village": "Pueblo en ruinas",
        "Museum": "Museo", "Interpretation centre": "Centro de interpretación", "Cemetery": "Cementerio"}
LOC = {"Exact spot known": "Punto exacto conocido", "General area only": "Solo la zona general",
       "Right area — the exact spot is uncertain": "Zona correcta; el punto exacto es incierto"}
FACT = {"Guide": "Guía", "Area": "Zona", "Type": "Tipo", "When": "Fecha", "Time to allow": "Tiempo recomendado",
        "Location": "Ubicación", "GPS": "GPS"}
DT = {"Open": "Horario", "Price": "Precio", "Booking": "Reservas", "Access": "Acceso", "Notice": "Aviso",
      "Parking": "Aparcamiento"}
H2 = {"The story": "La historia", "What you can see today": "Qué se puede ver hoy",
      "Plan your visit": "Organiza tu visita", "Sources": "Fuentes", "Nearby sites": "Lugares cercanos"}

es = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(os.path.join(ESJ, "*.json"))}


def esc(t):
    return html.escape(t, quote=True)


def frag(markup):
    """Parse an HTML fragment into nodes we can insert."""
    return BeautifulSoup(markup, "html.parser")


def alternates(slug):
    en = f"{SITE}{EN_BASE}{slug}.html"
    sp = f"{SITE}{ES_BASE}{slug}.html"
    return (f'<link rel="alternate" hreflang="en" href="{en}">\n'
            f'<link rel="alternate" hreflang="es" href="{sp}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{en}">')


def es_page(slug, src_html):
    d = es[slug]
    s = BeautifulSoup(src_html, "html.parser")
    url = f"{SITE}{ES_BASE}{slug}.html"
    title = f"{d['name']} — lugar de la Guerra Civil española | DZ Charlie"
    s.html["lang"] = "es"
    s.title.string = title
    s.find("meta", attrs={"name": "description"})["content"] = d["desc"]
    s.find("link", rel="canonical")["href"] = url
    s.find("link", rel="canonical").insert_after(frag(alternates(slug)))
    for prop, val in (("og:title", title), ("og:description", d["desc"]), ("og:url", url)):
        s.find("meta", property=prop)["content"] = val
    s.find("meta", property="og:site_name").insert_after(frag('<meta property="og:locale" content="es_ES">'))
    # Structured data
    lds = s.find_all("script", type="application/ld+json")
    a = json.loads(lds[0].string)
    a.update({"name": d["name"], "description": d["desc"], "url": url, "inLanguage": "es",
              "touristType": "Viajeros interesados en la historia y los campos de batalla"})
    lds[0].string = json.dumps(a, ensure_ascii=False)
    lds[1].string = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "DZ Charlie", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": GUIDE, "item": SITE + ES_BASE},
        {"@type": "ListItem", "position": 3, "name": d["name"]}]}, ensure_ascii=False)
    # Header
    nav = s.select_one("header nav")
    nav.clear()
    nav.append(frag(f'<a href="{ES_BASE}">Todos los lugares</a><a href="/#guides">Guías</a>'
                    f'<a href="{EN_BASE}{slug}.html" hreflang="en" lang="en">English</a>'))
    m = s.main
    m.select_one("nav.crumb").replace_with(frag(
        f'<nav class="crumb" aria-label="Ruta de navegación"><a href="/">DZ Charlie</a> › '
        f'<a href="{ES_BASE}">{GUIDE}</a> › {esc(d["name"])}</nav>'))
    m.select_one("p.eyebrow").string = GUIDE
    m.h1.string = d["name"]
    sub = m.select_one("p.sub")
    parts = sub.text.split(" · ")
    parts[-1] = TYPE[parts[-1]]  # town names before " · " are Spanish place names already
    sub.string = " · ".join(parts)
    for div in m.select(".facts div"):
        k, v = div.b.text, div.span.text
        div.b.string = FACT[k]
        div.span.string = {"Guide": GUIDE, "Area": AREA.get(v, v), "Type": TYPE.get(v, v), "When": d["when"],
                           "Location": LOC.get(v, v)}.get(k, v)
    btns = m.select(".btns a")
    btns[0].string = "Abrir la guía gratuita"
    btns[0]["href"] = "/spanish-civil-war/es.html"
    btns[1].string = "Cómo llegar (Google Maps)"
    for h in m.find_all("h2", recursive=False):
        key = h.text
        if key in H2:
            h.string = H2[key]
        nxt = h.find_next_sibling()
        field = {"The story": "story", "What you can see today": "see", "Plan your visit": "plan"}.get(key)
        if field:
            nxt.clear()
            nxt.append(frag(d[field]))
    vis_i = box_i = 0
    for b in m.select("main > div.box"):
        if b.dl:
            for dt in b.dl.find_all("dt"):
                v = d["vis"][vis_i]
                vis_i += 1
                assert DT[dt.text] and v["label"] == dt.text, (slug, dt.text, v["label"])
                dd = dt.find_next_sibling("dd")
                dt.string = DT[dt.text]
                dd.clear()
                dd.append(frag(v["text"]))
            small = b.select_one("p.small")
            if small:
                links = ", ".join(str(x) for x in small.find_all("a"))
                small.clear()
                small.append(frag(f"Comprobado en septiembre de 2026 en fuentes oficiales: {links}. "
                                  "Las cosas cambian, así que compruébalo antes de viajar."))
        else:
            bx = d["boxes"][box_i]
            box_i += 1
            label = "Terreno privado:" if bx["kind"] == "private" else "Las fuentes no coinciden:"
            b.clear()
            text = bx["text"]
            if bx["kind"] == "private":
                text = "solo puede verse desde la carretera o desde un camino público."
            b.append(frag(f"<b>{label}</b> {text}"))
    assert vis_i == len(d["vis"]) and box_i == len(d["boxes"]), slug
    for a in m.select("ul.near a"):
        other = a["href"].rsplit("/", 1)[-1][:-5]
        if other in es:
            a["href"] = f"{ES_BASE}{other}.html"
            a.string = es[other]["name"]
    for li in m.select("ul.near li span.small"):
        li.string = li.text  # distances are already language-neutral ("· 5 km")
    last = m.find("a", href=EN_BASE, recursive=True, string=re.compile("All 158 sites"))
    last["href"] = ES_BASE
    last.string = "Los 158 lugares de la Guerra Civil española →"
    cta = m.select_one("section.cta")
    cta.clear()
    cta.append(frag(
        f"<h2>La Guerra Civil española 1936–1939</h2><p>Una guía de campo gratuita para el móvil: la ruta, los mapas "
        "y las historias, incluso sin cobertura. Los campos de batalla, trincheras, pueblos en ruinas, refugios, "
        "museos y memoriales de la Guerra Civil en toda España, contados con equilibrio desde ambos bandos.</p><a class=\"btn red\" href=\"/spanish-civil-war/es.html\">Abrir la guía</a>"))
    f = s.footer.select_one(".in")
    f.clear()
    f.append(frag(
        "<p>Guías de campo gratuitas para el móvil. Muchos terrenos son privados: obsérvalos desde la carretera. "
        "Los cementerios y memoriales son, ante todo, lugares de recuerdo.</p>"
        '<nav aria-label="Guías"><a href="/places/normandy/">Normandía 1944</a>'
        '<a href="/places/holland-bastogne/">Holanda y Bastoña 1944–45</a>'
        '<a href="/places/germany-austria/">Alemania y Austria 1945</a><a href="/places/italy/">Italia 1943–1945</a>'
        f'<a href="{ES_BASE}">{GUIDE}</a></nav><p>DZ Charlie · guías de campo hechas con cariño por JC</p>'))
    return str(s)


def en_page(slug, src_html):
    """English page + hreflang links + a link to the Spanish version (idempotent)."""
    if 'hreflang="es"' in src_html:
        return src_html
    out = src_html.replace(
        f'<link rel="canonical" href="{SITE}{EN_BASE}{slug}.html">',
        f'<link rel="canonical" href="{SITE}{EN_BASE}{slug}.html">\n{alternates(slug)}', 1)
    out = out.replace('<a href="/#guides">Guides</a></nav>',
                      f'<a href="/#guides">Guides</a><a href="{ES_BASE}{slug}.html" hreflang="es" lang="es">Español</a></nav>', 1)
    assert out.count('hreflang="es"') == 2, slug
    return out


ENJ = os.path.join(os.path.dirname(ESJ.rstrip("/")), "en")
en_when = {k: json.load(open(os.path.join(ENJ, k + ".json")))["when"] for k in es}


def es_hub(src_html):
    s = BeautifulSoup(src_html, "html.parser")
    url = SITE + ES_BASE
    title = "Guerra Civil española 1936–1939: los 158 lugares, mapas y cómo visitarlos | DZ Charlie"
    desc = ("Los 158 lugares de la Guerra Civil española en toda España: campos de batalla, trincheras, refugios, "
            "museos y memoriales, con su historia y cómo visitarlos.")
    s.html["lang"] = "es"
    s.title.string = title
    s.find("meta", attrs={"name": "description"})["content"] = desc
    canon = s.find("link", rel="canonical")
    canon["href"] = url
    canon.insert_after(frag(f'<link rel="alternate" hreflang="en" href="{SITE}{EN_BASE}">\n'
                            f'<link rel="alternate" hreflang="es" href="{url}">\n'
                            f'<link rel="alternate" hreflang="x-default" href="{SITE}{EN_BASE}">'))
    for prop, val in (("og:title", title), ("og:description", desc), ("og:url", url)):
        s.find("meta", property=prop)["content"] = val
    s.find("meta", property="og:site_name").insert_after(frag('<meta property="og:locale" content="es_ES">'))
    ld = s.find("script", type="application/ld+json")
    a = json.loads(ld.string)
    a["name"] = "Lugares de la Guerra Civil española 1936–1939"
    a["inLanguage"] = "es"
    for it in a["itemListElement"]:
        k = it["url"].rsplit("/", 1)[-1][:-5]
        it["url"] = f"{SITE}{ES_BASE}{k}.html"
        it["name"] = es[k]["name"]
    ld.string = json.dumps(a, ensure_ascii=False)
    nav = s.select_one("header nav")
    nav.clear()
    nav.append(frag(f'<a href="{ES_BASE}">Todos los lugares</a><a href="/#guides">Guías</a>'
                    f'<a href="{EN_BASE}" hreflang="en" lang="en">English</a>'))
    m = s.main
    m.select_one("nav.crumb").replace_with(frag(
        f'<nav class="crumb" aria-label="Ruta de navegación"><a href="/">DZ Charlie</a> › {GUIDE}</nav>'))
    m.select_one("p.eyebrow").string = "Lugares de la guerra"
    m.h1.string = "Guerra Civil española 1936–1939: los 158 lugares"
    intro = m.h1.find_next_sibling("p")
    intro.string = ("Los campos de batalla, trincheras, pueblos en ruinas, refugios, museos y memoriales de la Guerra "
                    "Civil en toda España, contados con equilibrio desde ambos bandos. Cada lugar tiene su historia, "
                    "qué se puede ver hoy y cómo visitarlo.")
    btn = m.select_one(".btns a")
    btn.string = "Abrir la guía gratuita"
    btn["href"] = "/spanish-civil-war/es.html"
    trips = m.select_one(".btns").find_next_sibling("p", class_="small")
    if trips:
        trips.decompose()
    for h in m.find_all("h2"):
        h.string = AREA.get(h.text, h.text)
    for li in m.select("ul.list li"):
        a_ = li.a
        k = a_["href"].rsplit("/", 1)[-1][:-5]
        a_["href"] = f"{ES_BASE}{k}.html"
        a_.string = es[k]["name"]
        sp = li.select_one("span.m")
        parts = [TYPE.get(x, es[k]["when"] if x == en_when[k] else x) for x in sp.text.split(" · ")]
        sp.string = " · ".join(parts)
    rest = [x for x in m.find_all(recursive=False) if x.name in ("section", "p") and x.find_previous_sibling("ul")]
    for x in rest:
        if x.name == "section" and "cta" in x.get("class", []):
            x.clear()
            x.append(frag(
                "<h2>La Guerra Civil española 1936–1939</h2><p>Una guía de campo gratuita para el móvil: la ruta, los "
                "mapas y las historias, incluso sin cobertura.</p>"
                '<a class="btn red" href="/spanish-civil-war/es.html">Abrir la guía</a>'))
    f = s.footer.select_one(".in")
    f.clear()
    f.append(frag(
        "<p>Guías de campo gratuitas para el móvil. Muchos terrenos son privados: obsérvalos desde la carretera. "
        "Los cementerios y memoriales son, ante todo, lugares de recuerdo.</p>"
        '<nav aria-label="Guías"><a href="/places/normandy/">Normandía 1944</a>'
        '<a href="/places/holland-bastogne/">Holanda y Bastoña 1944–45</a>'
        '<a href="/places/germany-austria/">Alemania y Austria 1945</a><a href="/places/italy/">Italia 1943–1945</a>'
        f'<a href="{ES_BASE}">{GUIDE}</a></nav><p>DZ Charlie · guías de campo hechas con cariño por JC</p>'))
    return str(s)


def en_hub(src_html):
    if 'hreflang="es"' in src_html:
        return src_html
    out = src_html.replace(f'<link rel="canonical" href="{SITE}{EN_BASE}">',
                           f'<link rel="canonical" href="{SITE}{EN_BASE}">\n'
                           f'<link rel="alternate" hreflang="en" href="{SITE}{EN_BASE}">\n'
                           f'<link rel="alternate" hreflang="es" href="{SITE}{ES_BASE}">\n'
                           f'<link rel="alternate" hreflang="x-default" href="{SITE}{EN_BASE}">', 1)
    out = out.replace('<a href="/#guides">Guides</a></nav>',
                      f'<a href="/#guides">Guides</a><a href="{ES_BASE}" hreflang="es" lang="es">Español</a></nav>', 1)
    assert out.count('hreflang="es"') == 2
    return out


os.makedirs(os.path.join(OUT, ES_BASE.strip("/")), exist_ok=True)
os.makedirs(os.path.join(OUT, EN_BASE.strip("/")), exist_ok=True)
for slug in sorted(es):
    src = open(os.path.join(SRC, slug + ".html")).read()
    open(os.path.join(OUT, ES_BASE.strip("/"), slug + ".html"), "w").write(es_page(slug, src))
    open(os.path.join(OUT, EN_BASE.strip("/"), slug + ".html"), "w").write(en_page(slug, src))
hub = open(os.path.join(SRC, "index.html")).read()
open(os.path.join(OUT, ES_BASE.strip("/"), "index.html"), "w").write(es_hub(hub))
open(os.path.join(OUT, EN_BASE.strip("/"), "index.html"), "w").write(en_hub(hub))
print("built", len(es), "+ list pages")
