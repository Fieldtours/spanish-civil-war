"""Put the Spanish app (es.html) together from the translated parts.

Run from the dz folder. Writes app/out/es.html, app/out/site-es.webmanifest, app/out/sw.js and app/out/index.html
(the English app with an "Español" link added).
"""
import glob, json, os, re
from bs4 import BeautifulSoup

A = "app"
OUT = os.path.join(A, "out")
os.makedirs(OUT, exist_ok=True)
rd = lambda p: open(os.path.join(A, p), encoding="utf-8").read()
plain = lambda h: BeautifulSoup(h, "html.parser").get_text()

# ---------- main data (window.SCW) ----------
data_src = rd("part_data.txt")
m = re.match(r'(\s*window\.SCW=)(\{.*\})(;?\s*)$', data_src, re.S)
D = json.loads(m.group(2))
EN_D = json.loads(m.group(2))
es_pages = {}
for f in glob.glob("es/*.json"):
    j = json.load(open(f))
    es_pages[j["slug"]] = j
en_pages = {json.load(open(f))["name"]: json.load(open(f)) for f in glob.glob("en/*.json")}

missing = []
for s in D["stops"]:
    e = en_pages[s["n"]]
    sp = es_pages[e["slug"]]
    s["n"] = sp["name"]
    s["d"] = sp["when"]
    s["t"] = plain(sp["story"])
    s["lk"] = plain(sp["see"])
    s["pl"] = plain(sp["plan"])
    if s.get("ds"):
        ds = [b for b in sp["boxes"] if b["kind"] == "disagree"]
        s["ds"] = plain(ds[0]["text"])

ua = json.load(open(os.path.join(A, "units/es_data_a.json")))
ub = json.load(open(os.path.join(A, "units/es_data_b.json")))
for r, t in zip(D["regions"], ua["regions"]):
    assert r["id"] == t["id"]
    for k in ("name", "short", "blurb", "cap"):
        if k in t:
            r[k] = t[k]
for p, t in zip(D["phases"], ua["phases"]):
    p["name"], p["when"] = t["name"], t["when"]
for x, t in zip(D["time"], ua["time"]):
    for k in ("date", "title", "t", "place"):
        x[k] = t[k]
for x, t in zip(D["people"], ua["people"]):
    for k in ("name", "role", "dates", "t"):
        x[k] = t[k]
for k in ("brief", "orig", "factors", "clock", "gloss", "credits"):
    D[k] = ua[k]
for x, t in zip(D["links"], ua["links"]):
    x["title"] = t
for s in D["stops"]:
    if s["id"] in ua["imgc"]:
        s["imgc"] = ua["imgc"][s["id"]]
GEO = ua["geo_names"]
for k, v in D["geo"].items():
    if isinstance(v, list):
        for it in v:
            if isinstance(it, dict) and it.get("n"):
                it["n"] = GEO.get(it["n"], it["n"])
LAB = ub["map_labels"]


def relabel(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("l", "n") and isinstance(v, str) and v:
                o[k] = LAB.get(v, v)
            else:
                relabel(v)
    elif isinstance(o, list):
        for x in o:
            relabel(x)


for b, t in zip(D["battles"], ub["battles"]):
    assert b["id"] == t["id"]
    for k in ("name", "when", "place", "why", "rep", "nat", "result", "visit"):
        b[k] = t[k]
    for p, tp in zip(b["phases"], t["phases"]):
        for k in ("name", "time", "cap"):
            if k in tp:
                p[k] = tp[k]
    relabel(b["base"])
    for p in b["phases"]:
        relabel(p["items"])
for w, t in zip(D["weapons"], ub["weapons"]):
    assert w["id"] == t["id"]
    for k in ("name", "origin", "specs", "t", "good", "bad", "changes", "story", "cap"):
        if k in t:
            w[k] = t[k]
es_data = m.group(1) + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + m.group(3)

# ---------- diary data ----------
aar_src = rd("part_aar_data.txt")
m2 = re.match(r'(\s*window\.AAR_DATA=)(\{.*\})(;?\s*)$', aar_src, re.S)
AAR = json.loads(m2.group(2))
for i in range(4):
    AAR.update(json.load(open(os.path.join(A, f"units/es_aar_{i}.json"))))
es_aar_data = m2.group(1) + json.dumps(AAR, ensure_ascii=False) + m2.group(3)

# ---------- visiting info ----------
vz_src = rd("part_vz.txt")
i0 = vz_src.index("var V=") + len("var V=")
i1 = vz_src.index(",K={},G=")
V = json.loads(vz_src[i0:i1])
LBL = {"Open": "open", "Price": "price", "Booking": "booking", "Parking": "parking", "Access": "access", "Notice": "notice"}
by_id = {s["id"]: s for s in EN_D["stops"]}
vz_miss = []
for sid, r in V.items():
    if sid not in by_id or not r.get("f"):
        continue
    e = en_pages[by_id[sid]["n"]]
    sp = es_pages[e["slug"]]
    got = {LBL[v["label"]]: plain(v["text"]) for v in sp["vis"]}
    en_got = {LBL[v["label"]]: plain(v["text"]) for v in e["vis"]}
    for k, val in r["f"].items():
        if en_got.get(k) == val and k in got:
            r["f"][k] = got[k]
        else:
            vz_miss.append((sid, k, val))
es_vz = vz_src[:i0] + json.dumps(V, ensure_ascii=False, separators=(",", ":")) + rd("es_part_vz_code.txt")

# ---------- put it together ----------
parts = [rd("es_part_ld.txt"), rd("es_part_css.txt"), es_data, rd("es_part_mappics.txt"), rd("es_part_geomap.txt"),
         rd("es_part_battlemaps.txt"), es_aar_data, rd("es_part_app.txt"), rd("es_part_aar.txt"), rd("part_vzcss.txt"),
         es_vz, rd("part_counter.txt")]
page = rd("es_part_html.html")
assert page.count("/*BLOCK*/") == len(parts)
for p in parts:
    page = page.replace("/*BLOCK*/", p, 1)
open(os.path.join(OUT, "es.html"), "w", encoding="utf-8").write(page)

# manifest
man = json.loads(rd("site.webmanifest"))
man.update({"name": "La Guerra Civil española 1936–1939 — guía de campo DZ Charlie", "short_name": "Guerra Civil",
            "start_url": "./es.html", "lang": "es"})
json.dump(man, open(os.path.join(OUT, "site-es.webmanifest"), "w"), ensure_ascii=False)

# service worker: keep the English and Spanish pages apart in the offline copy
sw = rd("sw.js")
old_v = re.search(r'const V="(scw-core-[0-9a-f]+)"', sw).group(1)
sw = sw.replace(f'const V="{old_v}"', 'const V="scw-core-es-20261014"', 1)
assert '"index.html", "site.webmanifest",' in sw
sw = sw.replace('"index.html", "site.webmanifest",', '"index.html", "es.html", "site.webmanifest", "site-es.webmanifest",', 1)
old_nav = ('e.respondWith(fetch(req).then(r=>{if(r.ok){const c=r.clone();caches.open(V).then(x=>x.put("index.html",c))}return r})'
           '.catch(async()=>(await caches.match("index.html"))||(await caches.match("./"))));return}')
assert old_nav in sw
sw = sw.replace(old_nav, (
    'const pg=/\\/es(\\.html)?$/.test(u.pathname)?"es.html":"index.html";'
    'e.respondWith(fetch(req).then(r=>{if(r.ok){const c=r.clone();caches.open(V).then(x=>x.put(pg,c))}return r})'
    '.catch(async()=>(await caches.match(pg))||(await caches.match("index.html"))||(await caches.match("./"))));return}'), 1)
open(os.path.join(OUT, "sw.js"), "w").write(sw)

# English app: language switch on the More page + hreflang
en = open(os.path.join(A, "index.html"), encoding="utf-8").read()
read_eb = '<p class="eb">Read</p>'
assert en.count(read_eb) == 1, en.count(read_eb)
en = en.replace(read_eb, '<p class="eb">Language</p>\n'
                '<a class="tile" href="es.html" hreflang="es" id="lang-switch"><span class="n">ES</span><span class="x">'
                '<b lang="es">Español</b><span lang="es">Esta guía en español.</span></span></a>\n'
                '<p class="eb" style="margin-top:18px">Read</p>', 1)
canon = re.search(r'<link rel="canonical" href="([^"]+)">', en)
en = en.replace(canon.group(0), canon.group(0) +
                '\n<link rel="alternate" hreflang="en" href="https://dzcharlie.com/spanish-civil-war/">'
                '\n<link rel="alternate" hreflang="es" href="https://dzcharlie.com/spanish-civil-war/es.html">'
                '\n<link rel="alternate" hreflang="x-default" href="https://dzcharlie.com/spanish-civil-war/">', 1)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(en)

print("es.html", len(page), "| visiting details not matched:", len(vz_miss))
for x in vz_miss[:20]:
    print("  ", x)
