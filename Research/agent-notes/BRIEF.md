# Spanish Civil War 1936–1939 field guide — research brief (for research agents)

We are building a free, offline phone guide for travellers to the sites of the Spanish Civil War across mainland Spain + Balearics. Tone: accurate, sober, fair to both sides, no glorification. Language: English (Spanish place names with accents).

## Regions (use these ids exactly)
- madrid   = Madrid & the Centre (Comunidad de Madrid + Castilla-La Mancha: Madrid city, Ciudad Universitaria, Casa de Campo, Jarama, Brunete, Guadalajara/Brihuega, Toledo Alcázar, Sierra de Guadarrama/Alto del León, Paracuellos, etc.)
- aragon   = Aragon (Belchite, Teruel, Huesca front, Zaragoza, Quinto, Codo, Alcubierre/Orwell trenches, Montes de Zuera, Gurs? no (France), Caspe, Fraga, etc.)
- catalonia= Catalonia & the Ebro (Barcelona: shelters, bombings, Montjuïc, Fossar de la Pedrera; Ebro battle: Gandesa, Corbera d'Ebre Poble Vell, Serra de Pàndols, Serra de Cavalls, Móra d'Ebre, Flix, Miravet, Vilalba dels Arcs, La Fatarella; Segre front / Lleida; Retirada to the French border: La Jonquera, Figueres castle, Portbou; airfields e.g. La Sénia/Rosell; Mas Perxés?)
- north    = The North (País Vasco, Cantabria, Asturias: Gernika, Durango, Bilbao Iron Belt (Cinturón de Hierro), Artxanda, Intxorta, Oviedo siege, El Mazuco, Santander, Gijón, Eibar, Otxandio, Sollube, Sierra de Guadarrama excluded)
- south    = Andalusia & the South (Seville, Córdoba front / Pozoblanco / Lopera, Granada / Víznar–Alfacar (Lorca), Málaga–Almería road (La Desbandá), Almería shelters, Cádiz/Algeciras (Strait airlift), Jaén/Santuario de Santa María de la Cabeza siege, etc.)
- levant   = Valencia, Murcia & the Balearics (Valencia capital of the Republic 1936–37, Valencia air-raid shelters, XYZ line (Línea XYZ) trenches, Alicante port (end of war, Campo de los Almendros), Cartagena (fleet, shelters/Refugio-Museo), Castellón / Sierra de Espadán, Mallorca (Bayo landing, Porto Cristo), Menorca, Ibiza)
- west     = Extremadura & the West (Badajoz 1936, Mérida, Talavera road, Mérida–Madrid "Column of Death" route, La Serena pocket 1938, Peraleda / Pozoblanco? (no, Córdoba))
- castile  = Castile, León, Galicia, Navarre & La Rioja — the Nationalist rear & Guadarrama north side (Burgos: Franco HQ, Salamanca HQ + Centro Documental de la Memoria Histórica, Valladolid, Pamplona (Mola), Alto del León north side, Somosierra, Segovia, Valle de Cuelgamuros is in Madrid region, Galicia sites, León, Palencia, etc.)

## Phases (use these ids)
P1 Coup & first summer (17 Jul–Oct 1936) · P2 Battle for Madrid (Nov 1936–Mar 1937) · P3 War in the North (Mar–Oct 1937) · P4 Aragon: Belchite & Teruel (Aug 1937–Feb 1938) · P5 Drive to the sea (Mar–Jun 1938) · P6 Battle of the Ebro (Jul–Nov 1938) · P7 Fall of Catalonia & the end (Dec 1938–Apr 1939) · P8 Aftermath & memory (1939–today)

## Output: one JSON file, a list of stop objects
{
 "id": "<region>-NN",
 "name": "Short site name as a visitor would search it",
 "region": "<region id>",
 "lat": 40.12345, "lon": -3.12345,          // 4–5 decimals, WGS84, of the thing to visit
 "certainty": "HIGH" | "MEDIUM" | "LOW",       // HIGH = exact spot known (museum, memorial, surviving trench, ruin); MEDIUM = right area, exact spot uncertain; LOW = general area only
 "coord_source": "URL where you verified the coordinates (Wikipedia/Wikidata/official site/TracesOfWar/Mapcarta etc.)",
 "pri": 1|2|3|4,        // 1 = must-see of national importance, 2 = very worthwhile, 3 = for enthusiasts, 4 = minor/extra
 "min": 45,             // typical visit minutes
 "cat": "Battlefield" | "Trenches & fortifications" | "Ruined village" | "Museum" | "Interpretation centre" | "Air-raid shelter" | "Cemetery" | "Memorial" | "City site" | "Repression & memory site",
 "phase": "P1".."P8",
 "date": "e.g. 24 Aug–6 Sep 1937",
 "text": "80–140 words: what happened here, who fought, why it matters. Fair to both sides; name units/people where known; numbers only if sourced.",
 "look": "1–2 sentences: what the visitor can actually see on site today.",
 "plan": "1–2 sentences: practical tip — opening days, guided visits only, walking time, parking, entry fee if known.",
 "priv": false,          // true if on private land / view from the road only
 "town": "nearest town",
 "sources": ["url", "url"],
 "disputed": "optional: where sources disagree (casualty numbers, who did what) — say so plainly"
}

## Rules
- Only real, visitable (or visible-from-road) places. Prefer places with something to see: trenches, bunkers, ruins, museums, interpretation centres, memorials, cemeteries, shelters, plaques at real event sites.
- VERIFY every coordinate from a real source (Wikipedia/Wikidata coordinates, official site, TracesOfWar, Mapcarta, the regional heritage catalogues e.g. Espais de la Batalla de l'Ebre, Memoria Democrática inventories). Put that URL in coord_source. If you can only find the town, use the town centre and certainty LOW.
- Keep text neutral. For repression and mass-grave sites, be factual and respectful; include both Republican-zone and Nationalist-zone repression where there are real memorial sites (e.g. Paracuellos AND Badajoz/Víznar).
- Mark "disputed" honestly (e.g. Gernika death toll, Badajoz killings numbers, Paracuellos responsibility).
- Aim for the target count given to you, most important first. Quality over quantity.
- Write the JSON array (valid JSON, UTF-8) to the file path given, and a short markdown list of your sources and any open doubts to the .md path given.
- Tools: WebSearch and WebFetch. Wikidata JSON (https://www.wikidata.org/wiki/Special:EntityData/Q123.json) and Wikipedia pages give coordinates. Don't use a browser. If a site refuses, use another source.

## Battle-map format (only for the context agent)
Each battle map is a JS-style object in a schematic 600×420 drawing space (x right, y down; not geographic):
{ id, name, when, place, why, rep: "Republican forces", nat: "Nationalist forces (+ Condor Legion / CTV if present)", result, visit: "<b>Today:</b> what to see",
  stop: "id of the matching stop if known (e.g. madrid-03)",
  base: [ {t:"town",p:[[x,y],...]}, {t:"wood",p:[...]}, {t:"water",p:[...]} (river as polygon) , {t:"road",p:[[x,y],[x,y]]}, {t:"rail",p:[...]}, {t:"trench",p:[...]}, {t:"hedge",p:[...]} (use for ridgelines), {t:"bldg",r:[[x,y,w,h],...]}, {t:"txt",x,y,s:"label",a:"middle|end",big:1} ],
  phases: [ {name:"Phase 1", time:"6–9 Feb 1937", cap:"2–3 sentence caption", items:[
     {t:"u",s:"rep"|"nat",k:"inf"|"mg"|"art"|"arm",x,y,l:"label",above:true},
     {t:"a",s:"rep"|"nat",p:[[x,y],[x,y],[x,y]],r:1 /*r=retreat*/},
     {t:"f",s:"rep"|"nat",p:[[x,y],[x,y]]} /*line of fire*/,
     {t:"x",x,y} /*destroyed/captured*/,
     {t:"n",x,y,l:"note",a:"end"} ]} ]  // 3–4 phases
}
Keep geography roughly right (north up) and labels short.
