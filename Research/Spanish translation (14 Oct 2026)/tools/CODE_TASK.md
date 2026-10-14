# Make the Spanish version of the Spanish Civil War app's interface

Folder: /tmp/claude-0/-home-claude/97b29c6b-c547-5908-ac6a-97847beb6e88/scratchpad/dz/app

The app is one big HTML file, already split into parts:
- `part_html.html` – the page itself; script/style bodies replaced by `/*BLOCK*/` placeholders (keep every placeholder exactly where it is).
- `part_app.txt` – main app code. `part_aar.txt` – the "Diario de campaña" diary code. `part_geomap.txt` – offline map. `part_battlemaps.txt` – battle maps. `part_mappics.txt` – map tiles. `part_vz.txt` – visiting-info box (a big data object `V` at the top, then code). `part_counter.txt` – visitor counter (no visible text). `part_css.txt` – styles.

The **data** (site stories, timeline, people, weapons, glossary, diary questions, visiting details) is being translated separately and will be swapped in later. Your job is **everything else the visitor reads**: every visible English string in the HTML and in the code.

Write your results as new files next to the originals, named `es_part_html.html`, `es_part_app.txt`, `es_part_aar.txt`, `es_part_geomap.txt`, `es_part_battlemaps.txt`, `es_part_mappics.txt`, `es_part_vz_code.txt` (see below), `es_part_css.txt` (only if CSS contains visible text such as `content:"..."`; otherwise copy unchanged). Never edit the original files.

## Language

Follow `../tools/STYLE.md` (Castilian Spanish of Spain, not Latin American; neutral history terms: "sublevados"/"bando sublevado", "republicanos"). Interface Spanish should be short and natural, like a well-made Spanish app: use the informal "tú" for buttons and instructions ("Elige tu zona", "Empieza la ruta", "Añadir al diario"). Spanish date style ("17 jul. 1936", "lunes"), 24-hour times, decimal comma. Keep button labels about as short as the English so the layout doesn't break.

## What to translate

- All visible text in the HTML: headings, paragraphs, buttons, labels, `aria-label`, `title`, `alt`, `placeholder`, `<title>`, meta description, og/twitter title+description, JSON-LD name/description (it is inside a placeholder block in the html file – the ld+json block is `part_ld.txt`; also write `es_part_ld.txt`).
- Every English string in the code that ends up on screen or in an alert/confirm/share text/print/PDF/image: template literals, string concatenations, labels objects (e.g. `CERTTXT`, `L={open:"Open",…}` → Spanish), toast messages, empty states, the generated diary page text, share/email subjects and bodies, etc.
- Number/date formatting: if code formats dates with English month/day names or `toLocaleDateString("en…")`, switch to Spanish (`"es-ES"`). Plural helpers ("1 site / 2 sites") must produce correct Spanish.

## What must NOT change (or the app breaks)

- Logic, ids, CSS classes, `data-*` attribute names, localStorage keys, URLs, file paths, function names, event names, SVG paths.
- **Data enum values stay English in the data and are compared in code.** In the Spanish data the following fields will remain exactly in English: each stop's `k` (type: "Battlefield", "Museum", "Cemetery", "Memorial", "Repression & memory site", "Trenches & fortifications", "Air-raid shelter", "City site", "Ruined village", "Interpretation centre"), certainty codes `c` ("HIGH"/"MEDIUM"/"LOW"), people `side` (e.g. "Republic", "Nationalist", …), weapons `side` ("Both", …), timeline `certainty`, phase ids, region ids. Find every place where code **displays** one of these values and show a Spanish label instead, via ONE lookup helper added near the top of `part_app.txt`, e.g. `const TR={k:{"Battlefield":"Campo de batalla",…},side:{…}}; const tr=(g,v)=>(TR[g]&&TR[g][v])||v;` Keep all comparisons on the English values. Use these type labels: Trincheras y fortificaciones, Memorial, Lugar de represión y memoria, Refugio antiaéreo, Lugar urbano, Campo de batalla, Pueblo en ruinas, Museo, Centro de interpretación, Cementerio. Find all distinct side values by reading the data block start (`grep -o '"side": *"[^"]*"' part_data.txt | sort -u`).
- Fields that WILL be Spanish in the data (so code must not compare them to English literals): region `name`/`short`/`blurb`, phase `name`/`when`, stop `n` (name), `d` (date), `t`, `lk`, `pl`, `ds`, all timeline/people/battle/weapon text, glossary, diary texts. If code compares any of these to an English literal, change the code to compare an id/enum instead, and list each such change in your report.
- `part_vz.txt`: do NOT rewrite the big `V={...}` data object. Copy ONLY the code that follows it into `es_part_vz_code.txt`, starting from the text `,K={},G=` (inclusive) to the end, translated (labels object `L`, "Checked … from official sources", "Things change, so check before you travel.", "No confirmed visiting details…", "Visiting", "see notice", "Report a problem", the email subject/body text, `G` = "La Guerra Civil española", `CK` = "sept. 2026"). Use exactly these Spanish labels: open→"Horario", price→"Precio", booking→"Reservas", parking→"Aparcamiento", access→"Acceso", notice→"Aviso"; and the sentence "Comprobado en septiembre de 2026 en fuentes oficiales" + ": links" + ". Las cosas cambian, así que compruébalo antes de viajar." (build it so the result reads exactly like that, with CK used for the date part as "sept. 2026" → write the sentence as 'Comprobado en '+CK+' en fuentes oficiales').

## Language switch and links (Spanish version)

- `<html lang="es">`. `<link rel="manifest" href="site-es.webmanifest">`. Canonical `https://dzcharlie.com/spanish-civil-war/es.html`, plus `<link rel="alternate" hreflang="en" href="https://dzcharlie.com/spanish-civil-war/">`, `hreflang="es"` → the es.html URL, `x-default` → English.
- Add a clearly visible language switch "English" that links to `./` (the English app) — put it where a user would look for settings/language (the More/Más screen is ideal; if the header has room, also fine). Report exactly where and how you added it (the file, the surrounding code), because the same "Español" link (to `es.html`) must be added to the English app in the same spot.
- Links to the English website pages for sites (`/places/spanish-civil-war/<slug>.html`) should point to the Spanish ones (`/es/guerra-civil/<slug>.html`); links to `/places/` → `/es/guerra-civil/`. Links to the PDF stay, labelled as English ("Guía en PDF (en inglés)").
- The service worker registration stays as is.

## Check your work

For each JS file you produce run `node --check <file>` after copying it to a `.js` name in /tmp/claude-0/-home-claude/97b29c6b-c547-5908-ac6a-97847beb6e88/scratchpad/dz/app/check/ (create it). All must pass. Then grep your es_ files for leftover English UI words (e.g. `grep -nE '"(Open|Close|Back|Search|Tour|Map|Home|More|Start|Next|Previous|Today|Save|Share|Print|Cancel|Done|sites?|minutes?|hours?|days?)"' es_part_app.txt`) and fix real misses (not keys/class names).

## Report

Reply in under 25 lines: files written; the TR helper and where enum values are displayed; any code you changed beyond strings (with reason); exactly where you put the language switch (so it can be mirrored in English); anything you were unsure about.
