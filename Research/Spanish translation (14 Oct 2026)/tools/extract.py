"""Pull the translatable text out of each English Spanish-Civil-War place page into JSON."""
import glob, json, os, sys
from bs4 import BeautifulSoup
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
def inner(el): return el.decode_contents().strip()
for f in sorted(glob.glob(os.path.join(SRC, "*.html"))):
    slug = os.path.basename(f)[:-5]
    if slug == "index": continue
    s = BeautifulSoup(open(f), "html.parser")
    m = s.main
    facts = {d.b.text: d.span.text for d in m.select(".facts div")}
    secs = {}
    for h in m.find_all("h2", recursive=False):
        nxt = h.find_next_sibling()
        if h.text in ("The story", "What you can see today", "Plan your visit"):
            secs[h.text] = inner(nxt)
    vis, boxes = [], []
    for b in m.select("main > div.box"):
        if b.dl:
            vis = [{"label": dt.text, "text": inner(dt.find_next_sibling("dd"))} for dt in b.dl.find_all("dt")]
        else:
            lab = b.b.text
            b.b.extract()
            boxes.append({"kind": "private" if lab.startswith("Private") else "disagree", "text": inner(b)})
    d = {"slug": slug, "name": m.h1.text, "when": facts.get("When", ""),
         "story": secs["The story"], "see": secs["What you can see today"], "plan": secs["Plan your visit"],
         "vis": vis, "boxes": boxes}
    json.dump(d, open(os.path.join(OUT, slug + ".json"), "w"), ensure_ascii=False, indent=1)
print("done")
