# Translating DZ Charlie Spanish Civil War site pages into Spanish

You translate JSON files describing one historical site each, from English into **Castilian Spanish as written in Spain** (castellano peninsular). Readers are Spaniards and visitors to Spain planning a trip.

## Output

For each input file `en/<slug>.json`, write `es/<slug>.json` with exactly this shape:

```json
{
 "slug": "<same as input>",
 "name": "...",          // Spanish page heading (see Names)
 "when": "...",          // translated date range
 "story": "...",         // translated, same HTML tags/links as input
 "see": "...",
 "plan": "...",
 "vis": [{"label": "<keep the English label exactly>", "text": "..."}],
 "boxes": [{"kind": "<same>", "text": "..."}],
 "desc": "..."           // NEW: Spanish meta description, 120–155 characters, plain text, no quotes
}
```

Keep every HTML tag, attribute and URL in the input exactly as is (e.g. `<a href="...">`, `<b>`). Translate only visible text. Keep the same number of `vis` and `boxes` entries in the same order. Write valid JSON (UTF-8, real accented characters, no `\u` escapes needed).

## Spain Spanish, not Latin American

- vosotros forms if addressing a group; prefer impersonal/usted-free phrasing ("Se recomienda reservar", "Conviene llevar linterna").
- móvil (not celular), coche (not carro/auto), aparcamiento/aparcar (not estacionamiento/estacionar), conducir (not manejar), ordenador, billete/entrada (not boleto), zumo, vale, gafas, autobús (not camión/colectivo), metro, ir a pie / andando (not caminar where "andar" is natural), recoger, coger (fine in Spain).
- Spanish punctuation and typography: ¿ ¡, comillas «», decimal comma (3,50 €), price after number with space (3,50 €), thousands with dot (1.000) or no separator for 4 digits per RAE (1000), 24-hour times (10:30), days and months lowercase (lunes, enero).
- Day abbreviations: lun., mar., miér., jue., vie., sáb., dom. Ranges: "mar.–sáb." Month abbreviations in dates: ene., feb., mar., abr., may., jun., jul., ago., sept., oct., nov., dic. Dates as "24 ago.–6 sept. 1937". Write "h" and "min" for durations.
- Address abbreviations stay as written locally (C/ Becú 2, Carrer Nou de la Rambla).
- Natural, clear, plain Spanish for a general reader. Not a word-for-word calque. Keep it about the same length as the English.

## History terms: neutral, "fairly from both sides"

- "Nationalists" → **sublevados** / **bando sublevado** (or **franquistas** when it is clearly Franco's forces after 1936). Never "nacionales" as our own voice (you may keep it inside a proper name or quoted term, e.g. "Monumento a los Caídos").
- "Republicans" → **republicanos** / **bando republicano**. "Popular Army" → Ejército Popular de la República.
- International Brigades → Brigadas Internacionales. Army of Africa → Ejército de África. Condor Legion → Legión Cóndor. Aviazione Legionaria stays as is. Iron Belt (Bilbao) → Cinturón de Hierro. Republican Zaragoza offensive → ofensiva republicana sobre Zaragoza. Battle of the Ebro → batalla del Ebro. Repression → represión. Mass grave → fosa común. Air-raid shelter → refugio antiaéreo. Concentration camp → campo de concentración. Requetés, Falange, CNT, POUM etc. unchanged.
- Do not add, remove or soften facts, figures or judgements. If the English hedges ("about", "usually", "sources disagree"), keep the hedge.

## Names (`name`)

- Use the name a Spaniard would search for. Keep local proper names as they are, including Catalan, Basque and Galician ones (Refugi 307, Poble Vell de Corbera d'Ebre, Gernika-Lumo).
- Translate only English descriptive parts: "Belchite old town (Pueblo Viejo)" → "Pueblo Viejo de Belchite"; "Suicide Hill (Colina del Suicidio), Jarama" → "Colina del Suicidio (Jarama)"; "Alcázar of Toledo & Army Museum" → "Alcázar de Toledo y Museo del Ejército"; "Basílica del Pilar – the unexploded bombs (Zaragoza)" → "Basílica del Pilar: las bombas que no estallaron (Zaragoza)".

## `desc`

One or two sentences in Spanish, 120–155 characters, that make someone searching on Google want to click: what the place is, what happened there, and that the page has visiting info. Example: "Ruinas del pueblo viejo de Belchite, arrasado en 1937. Historia de la batalla, qué ver hoy y cómo visitarlo con la visita guiada."

## Sources and links

Do not translate URLs or link text that is a web address (e.g. belchite.es).

---
# Extra rules for the APP data files (units/*.json)

- Input files are JSON. Write a translated copy with **exactly the same structure**: same keys, same list lengths, same order. Translate only human-readable English text values.
- **Never change**: any key named `id`, `sort`, `a`, `solemn`, `stop`, `stops`, `url`, `img`, numbers, booleans, and short codes such as "HIGH", "MEDIUM", "LOW", "P1"… Keep HTML tags exactly.
- Proper names of people, places, units and organisations stay as they are (Spanish/Catalan/Basque names unchanged). English descriptive labels on maps get translated ("Italian tankettes" → "Tanquetas italianas", "XI Int. Brigade" → "XI Brigada Internacional", "Front frozen until 28 Mar 1939" → "Frente estabilizado hasta el 28 mar. 1939"). Keep map labels about as short as the English (they sit on a small map).
- Glossary (`gloss`): each entry is [term, definition]. Keep Spanish terms/acronyms as they are; translate English terms (e.g. "Non-intervention" → "No intervención"). Write the definition in Spanish; drop English glosses of Spanish names that would be redundant in Spanish (e.g. "Partido Socialista Obrero Español — the Socialist Party…" → "Partido Socialista Obrero Español: el partido socialista…").
- `geo_names` is a list of map place names. Return an object {english: spanish} for every entry. Most stay the same; translate only English or foreign exonyms that have a usual Spanish form (e.g. "Cantabrian Mountains" → "Cordillera Cantábrica", "Garonne" → "Garona", "France" → "Francia", "Portugal" → "Portugal"). Empty string maps to empty string.
- `map_labels` is a list. Return an object {english: spanish} for every entry.
- Diary data (aar files): translate `when` (keep it in CAPITALS like the English, Spanish month abbreviations: "NOV. 1936–MAR. 1939"), `ev`, `st`, `rem`, and in `q`: `t`, every option in `o`, and `x`. Keep `a` (the index of the right answer) and the option order unchanged.
- Weapons `specs` are [label, value] pairs: translate both; units stay metric, decimal comma, thousands with a dot from 10.000 (e.g. "1.235 mm" is fine for readability in specs).
