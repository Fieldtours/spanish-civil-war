# The Spanish Civil War 1936–1939 — a DZ Charlie field guide

A free, offline phone guide to 158 sites of the Spanish Civil War across the whole of Spain:
battlefields, trenches, ruined villages, air-raid shelters, museums, cemeteries and memorials.
Visitors choose the area they want to tour and how much time they have; the guide builds the route.

- `app/` — the finished website, ready to upload (Netlify drag-and-drop, or as `dzcharlie.com/spanish-civil-war/`)
- `Research/` — every site with its sources, and `accuracy-check.md` (facts to check)
- `Design/` — design brief, cover prompt, source pictures (with licences in the app credits), screenshots
- `build/` — source: `app.js`, `map.js` (offline map of Spain), `bm.js` (battle maps), styles, data builder
  (`make_data.py`), page assembler (`assemble.py`), PDF maker (`make_pdf.py`) and map data (`geo/`)
- `PROJECT NOTES.txt` — version history in plain English
- `app/es.html` — the same guide in Spanish (Castilian), added 14 October 2026. It was made from the finished
  `index.html`, not from `build/`, so rebuilding with `build/assemble.py` does not recreate it or the "Español"
  link; see `Research/Spanish translation (14 Oct 2026)/README.txt`
- `app/pdf/La-Guerra-Civil-espanola-guia-de-campo.pdf` — the printable guide in Spanish (added 18 October 2026),
  made from `app/es.html` by `build/make_pdf_es.py`

Version: v1 · 27 September 2026
