# Spanish Civil War app maps (v1.3, 30 Sep 2026): the Easy Company map standard for a whole country

Two tiers of Google-style road-map pictures on top of the drawn map of Spain (map.js keeps drawing it underneath as a fallback):
- g0 overview: all of Spain at 600 px/degree (levels 600, 300, 150, 75 px/degree) + a names-free copy.
  Data: Natural Earth (land, sea, rivers, lakes, borders) + OpenStreetMap motorway/trunk/primary roads and every city/town;
  the zoomed-out levels use a lighter merged road layer (data/spain-ov-lo) so they draw in time.
- g1..g75 close-ups: stops within 15 km grouped; box = stops ±0.07° lat, ±0.09° lon; 4,550 px/degree (Easy Company close-up level)
  with levels down to ~260 px. Data: OpenStreetMap from the 16 Geofabrik region files (one pass per file).

Steps
1. plan.py -> groups.json
2. Geofabrik region files (built-in browser: fetch the dated file, e.g. madrid-260929.osm.pbf, save as a blob) ->
   extract_multi.py <file> pkl/<region>.pkl  (about 30 s each) -> combine_multi.py -> add_outside.py
   (python3 ../from_ne.py data/spain-ne -9.9 35.6 4.6 44.1 first, for the Natural Earth layers)
3. make_tiles_scw.py [ids]  (renders with ../render.html + ../shoot.js; run ONE at a time: parallel runs crash the renderer
   and the level comes out without roads; ONLY_LV=0,1,b redraws only those levels). Plain one-colour tiles are dropped.
4. build_page.py <newest index.html> <out>  (adds window.SCW_RASTER, patches GeoMap via patch_map.py, updates credits)
   make_sw.py <old sw.js> <index.html> <raster list> <out sw.js>  (maps in their own cache "scw-maps", all saved by Save for offline)
Check contact sheets of every level by eye before hand-over. Credit: Map data © OpenStreetMap contributors.
(queries.py / convert.py: the Overpass route, used only for testing; Overpass bans the computer after many queries.)
