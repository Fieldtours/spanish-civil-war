# Weapons & pictures: research notes

Files: `weapons.json` (14 weapons), `pictures.json` (24 images).

## IMPORTANT: licences were not read from the Commons pages
- This machine cannot reach commons.wikimedia.org. curl returns a proxy 403, and WebFetch says the domain is "cache-only". The Commons API, the mobile site, api.wikimedia.org and the toolforge mirrors were all blocked too.
- **What is verified:** every `file` name except the Laffitte grenade appeared in a Commons search result, so each of those files exists under that exact title.
- **What is computed:** each `url` was built with the standard Commons rule: `upload.wikimedia.org/wikipedia/commons/{md5[0]}/{md5[0:2]}/{Name_with_underscores}`, using the MD5 of the filename with underscores. It should resolve, but it has not been tested.
- **What is NOT verified:** `licence` and `author`. These are best guesses based on how each collection is normally licensed. Every item has a `check` field saying what to confirm. **Before shipping, run this once from a machine with Commons access:**
  `https://commons.wikimedia.org/w/api.php?action=query&titles=File:A|File:B|...&prop=imageinfo&iiprop=url|extmetadata&iiextmetadatafilter=LicenseShortName|Artist|ImageDescription&format=json` (up to 50 titles per call). Replace `licence` and `author` with what it returns, and drop any file that is not free.
- Collection rules I relied on:
  - Bundesarchiv Bild 183 files: CC BY-SA 3.0 DE.
  - Armémuseum `AM.*` files: CC BY 4.0.
  - West Point "Map of the Spanish Civil War in …" files: public domain (US government).
  - Gallica/French press-agency photos: public domain.
  - Gerda Taro (died 1937): public domain.
- My WebSearch budget ran out partway through (the limit is shared across the session), so some gaps below could not be filled.

## Weapon images that need replacing or checking
- **mauser-1893:** the file shows the post-war **M43** Mauser, not the M1893 or M1916. Look in Category:Mauser rifles / Mauser M1893 for a better one.
- **naranjero:** the file shows a German **MP 28**, which is the original design the naranjero copied, not a Spanish-made gun.
- **astra-400:** the file shows the **Campo-Giro** pistol (the Astra 400's predecessor) at the Eibar arms museum. No Astra 400 file was found.
- **laffitte:** no file was found. Choose one from Category:Hand_grenades_of_the_Spanish_Civil_War. The mechanism and weight in the text are hedged, so check them against a Spanish source.
- **t-26, ju-52, panzer-i:** I haven't seen what these images show. Confirm:
  - `T-26.JPG` is a single-turret model.
  - Bundesarchiv 183-C0214-0007-013 shows a Ju 52 (fallback: Bundesarchiv Bild 146-1989-014-30).
  - Bundesarchiv 183-E20569-21 shows Panzer I training (fallback: `SdKfz101.jpg`).
- **Other options found:** `Polikarpov I-15 (4321424501).jpg`, `Polikarpov I-16-Spain.jpg`, `Polikarpov I-16-Mosca.jpg`, `Captured L3 and L3 cc tankettes.jpg`, `Bf 109A from the Condor Legion with Nationalist Spain markings.jpg`, `Junkers Ju 87A with Spanish rebel markings.jpg`, `MWP Maxim wz1910.JPG`, `Mosin-Nagant M1891 Dragoon - Ryssland - AM.067668.jpg`.
- **Balance:**
  - Republic: Mosin, Maxim, Naranjero, T-26, I-16/I-15.
  - Nationalist: Panzer I, CV-33, Ju 52, He 111, SM.79, Flak 18.
  - Both: Mauser, Astra 400, Laffitte.
  - Left out for space: Hotchkiss M1914, DP-28, BA-6, Bf 109.

## Pictures
- **Cover:**
  - `Belchite - Vista general01.JPG` and `Alcazar Toledo Mirador Valle.jpg` are wide modern landscapes (CC BY-SA, to be confirmed).
  - `Barcelona bombing (1938).jpg` is a strong period alternative.
  - `Spanish Civil War poster 07.jpg` is tagged cover but I haven't seen it. Check the artist, and drop it if the artist died after 1945.
- **Region headers:** madrid, catalonia (two options), north, castile (two: Franco y Mola photo, Nationalist poster), aragon.
  - west, south and levant only have West Point situation maps. Replace these with photos when searching is possible again. Candidates: Badajoz 1936, Málaga–Almería road 1937, Valencia/Cartagena shelters.
- **Posters:** only one confirmed-anonymous Nationalist poster (`1937-1938 propaganda poster - El generalisimo.jpg`) is included. No Republican poster has been confirmed as public domain yet.
  - Many well-known Republican posters are by artists who died after 1945 (Renau d. 1982, Arteche d. 1964, Bardasano d. 1979). These are **not** PD in Spain, where the rule is 80 years after death for authors who died before 1987.
  - Rejected: `ARTECHE, Cristóbal. Les Milicies us necessiten!, 1936.jpg` (Arteche died in 1964).
  - Anonymous Spanish posters from 1936–39 are PD in Spain 80 years after publication. The US (URAA) status still needs checking for each file.
- **Period maps:** `Plano de Teruel (1937).jpg`. The West Point series is modern but historical and PD; there are also dated maps for Jul 1936, Oct 1937, Nov 1938, the Battles round Madrid (Blank), and a Frente del Norte svg.
- **Uncertain or dropped:**
  - `Nationalist soldiers raiding Madrid, March 1937.jpg` (dropped: title wording unclear).
  - `Battle of Badajoz.jpg` (might show the 1812 battle, not 1936).
  - `RetiradaAnnual.jpg` (probably Annual 1921).
  - `SCI1937spanish-civil-war01Evacuation.jpg` (place unknown).
  - `RIAN archive 604273 Barricades on city streets.jpg` (place unknown).
- **The Puigdendolas photo** comes from the Comunidad de Madrid "Delegación de Propaganda y Prensa" archive. Check that archive's licence and the photographers' dates.

## Sources for weapon anecdotes (Wikipedia pages cited; not re-fetched)
- Mauser Model 1893
- Maxim M1910
- MP 28
- Astra 400
- Bombing of Guernica
- T-26
- Panzer I
- Battle of Guadalajara
- Polikarpov I-16
- Junkers Ju 52
- Army of Africa
- CASA 2.111
- Bombing of Barcelona
- 8.8 cm Flak 18/36/37/41
- G. Howson, *Arms for Spain* (1998)

**Disputed figures, flagged in the text:**
- Strait airlift: c. 14,000 men.
- Barcelona March 1938 raids: c. 900–1,300 dead.
- Aircraft involved at Gernika.
