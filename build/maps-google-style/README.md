# Google-style road maps (for the PDFs, and later the apps)

Familiar road-map look (light land, yellow/orange main roads with road-number signs, blue water,
green woods, clear town names), drawn by us from open data, so it works offline and prints sharply.
Our numbered sites sit on top; overlapping sites are spread out with a thin line to the true spot;
a numbered key goes under each map; far-away sites are listed "off this map".

1. `plan_areas.py <guide>...` — for each map, the view it will show and its tier:
   detail/mid (zoom >= 8.6): OpenStreetMap data for exactly that view;
   ne (wide overviews): Natural Earth (github.com/nvkelso/natural-earth-vector, via GitHub).
2. OpenStreetMap data: a Geofabrik .osm.pbf (`extract_osm.py`) or Overpass downloads made in the
   browser on JC's Mac (`overpass_q.py` -> osm-<map>.json -> `from_overpass.py`). Mirrors:
   overpass.kumi.systems, overpass-api.de, maps.mail.ru. Busy servers answer 504: retry another.
3. `jobs2.py <guide>` then `node shoot.js jobs-<guide>.json` renders each map with MapLibre GL
   (npm maplibre-gl@4, headless Chromium with SwiftShader; glyphs from github.com/protomaps/basemaps-assets).
4. `build/ec-pdf/make_pdf.py` puts each map with its key into the PDF. Credit: "Map data © OpenStreetMap contributors".

## Maps inside the Easy Company apps (multi-level tiles)
`make_tiles.py <app> <prefix> <data dirs per group>` draws each map group at several levels of detail
(L0 full, L1 half, ... down to ~640px) plus a names-free copy of the overview (lv -1), cuts them into
1024px JPEG tiles `maps/<prefix>-z<g><lv|b>-<r>-<c>.jpg` and writes `tiles/<prefix>/raster.json`.
`ONLY=00,01,b` limits which group/levels are redrawn; `SHOOT_MS` raises the per-chunk time limit for
dense areas. `ux_ec.py maps_patch()` swaps the tile list into each app and adds `rasPick()`, which picks
the sharpest level that suits the current zoom (cards, lightbox zoom, area planner).
