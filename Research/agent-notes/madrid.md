# Madrid & the Centre: research notes (30 stops)

## Coordinate verification status
The research tools were heavily limited. Bash had no network access (Wikipedia, Wikidata, OSM and Mapcarta were all blocked). WebFetch could only reach cached pages and usually stripped coordinates, and the shared WebSearch budget ran out partway through. So coordinates fall into three groups:

**Verified from a source (coords copied from it):**
- madrid-02 Alcázar of Toledo (en.wikipedia)
- madrid-03 Suicide Hill and madrid-15 IB memorials (Morata tourism PDF "9 Rutas", DMS waypoints)
- madrid-04 Pingarrón (Mapcarta/OSM N367865919, which matches the Morata PDF waypoint 40.2071,-3.5140 to within about 250 m)
- madrid-12 Templo de Debod (en.wikipedia)
- madrid-25 Sigüenza Cathedral (en.wikipedia)
- madrid-16 Brunete, madrid-17 Brihuega, madrid-23 Villanueva de la Cañada (town centres from en.wikipedia)

**From rutasconhistoria.es (NOT reliable):** its Pingarrón entry is about 12 km off, and its "nearby" distances often don't match its own coordinates. Used for madrid-10 Parque del Oeste bunkers (looks plausible), madrid-24 Blockhaus 13 (consistent with "near the M-510 west of Navalagamella") and madrid-28 Fresnedillas (LOW). For madrid-13 Posición Jaca I did NOT use its coords, which would put it about 2.5 km off. I used my own estimate for El Capricho instead.

**Best-knowledge estimates, not verified by a fetched source. Please re-check:**
- madrid-01 Ciudad Universitaria (general point, Facultad de Medicina area)
- madrid-05 Cuelgamuros basilica 40.6419,-4.1552
- madrid-06 Paracuellos cemetery (LOW; I only have the town coords, 40.5047,-3.5300, and the cemetery's exact spot is unconfirmed)
- madrid-07 Telefónica 40.4202,-3.7018
- madrid-08 Reina Sofía 40.4080,-3.6945
- madrid-09 Cerro Garabitas
- madrid-11 Puente de los Franceses
- madrid-13 El Capricho
- madrid-14 Morata museum (town centre; the address is Calle Carmen 35)
- madrid-18 Paredes de Buitrago
- madrid-19 Alto del León
- madrid-20 Cementerio Civil
- madrid-21 Jarama bridges
- madrid-22 Quijorna
- madrid-26 Cerro de los Ángeles
- madrid-27 Arco de la Victoria
- madrid-29 Pinto
- madrid-30 Bustarviejo

The coord_source for these is the site's reference page, not a confirmed coordinate.

## Open doubts
- **Left out, could not verify:** Loma del Noruego, Collado del Piornal, Peguerinos (Peguerinos is in Ávila, so arguably the castile region), El Espartal (only mentioned inside madrid-29), Cementerio de Fuencarral International Brigades memorial, Refugio de Chamberí (the Chamberí "shelter" news was a 2022 UNHCR staging at the metro museum, not a real Civil War shelter museum).
- **Almudena memorial (madrid-20):** the current state of the 2018–19 memorial to the executed is uncertain, and the "c. 2,900–3,000 executed" figure should be checked.
- **Posición Jaca:** visiting arrangements (weekend guided visits, booking) should be checked with the Madrid city council.
- **Museo Batalla del Jarama:** conflicting addresses (Calle Carmen 16 vs 35), and opening hours unknown.
- **Paracuellos cemetery:** opening hours are not confirmed.
- **Palacio de Ibarra:** the exact location (a few km south-east of Brihuega, on private land) is not verified.
- **Madrid-04/03 casualty figures** are marked as disputed in the JSON.

## Sources used
- https://en.wikipedia.org/wiki/Siege_of_Madrid · /Battle_of_Jarama · /Battle_of_Brunete · /Battle_of_Guadalajara · /Paracuellos_massacres · /Valley_of_the_Fallen · /Alcázar_of_Toledo · /Temple_of_Debod · /Casa_de_Campo · /Parque_del_Oeste · /Casa_de_Velázquez · /Arco_de_la_Victoria · /Cerro_de_los_Ángeles · /Sigüenza_Cathedral · /Brunete · /Brihuega · /Telefónica_Building
- https://es.wikipedia.org/wiki/Batalla_de_la_Ciudad_Universitaria · /Matanzas_de_Paracuellos · /Cerro_Garabitas · /Edificio_Telefónica · /Templo_de_Debod · /Puente_de_los_Franceses
- https://morataturismo.es/wp-content/uploads/2017/11/9-Rutas-Restos-Batalla-Jarama.pdf
- https://mapcarta.com/es/N367865919
- https://guerraenmadrid.net/2019/03/16/cinco-lugares-de-la-batalla-del-jarama-que-debes-visitar/
- https://www.viajaporlibre.com/espana/madrid/restos-de-la-guerra-civil-en-la-comunidad-de-madrid
- https://www.comunidad.madrid/cultura/patrimonio-cultural/ruta-guerra-civil-frente-agua
- https://www.rutasconhistoria.es/loc/… (Parque del Oeste bunkers, Posición Jaca, Colmenar del Arroyo, Fresnedillas, La Jarosa, Museo Batalla del Jarama)
- https://www.esmadrid.com/en/tourist-information/telefonica-building
