# Shared diary engine (After Action Report / Diario de campaña)

- `../aar.js` + `../aar.css`: the engine, the same in every DZ Charlie guide. Each guide sets
  `window.AAR_CFG` (names, colours, fonts, `visited()`, `stop(id)`, `title(ids)`, `onChange`) and its
  per-stop data (`when`, `sort`, `ev`, `q`, `rem`, `solemn`) before loading `aar.js`.
- `inject_ec.py`: how it was added to the three Easy Company guides (with their data files here).
- Spanish Civil War: config at the end of `../app.js`, data in `Research/raw/aar_data.json`.
