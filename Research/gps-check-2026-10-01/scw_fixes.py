import json, re, sys
F = {
 'madrid-10': (40.43502, -3.72860, None, 'Civil War fortins in the Parque del Oeste (OSM)'),
 'madrid-13': (40.45694, -3.59550, None, 'Bunker de Miaja / Posición Jaca, El Capricho (OSM)'),
 'madrid-14': (40.22567, -3.43785, None, 'Museo de la Guerra y Posguerra, Morata de Tajuña (OSM)'),
 'madrid-16': (40.40505, -3.99799, None, 'Centre of Brunete (OSM)'),
 'madrid-18': (41.00518, -3.56140, None, 'Paredes de Buitrago village, where the route starts (OSM)'),
 'madrid-19': (40.70915, -4.14032, None, 'Civil War bunker at the Alto del León (OSM)'),
 'madrid-20': (40.42165, -3.63549, None, 'Cementerio Civil (OSM)'),
 'madrid-26': (40.30783, -3.68431, None, 'Sagrado Corazón monument, Cerro de los Ángeles (OSM)'),
 'madrid-27': (40.43591, -3.72020, None, 'Arco de la Victoria (OSM)'),
 'madrid-28': (40.50140, -4.13820, None, 'The group of fortins north of Fresnedillas (OSM)'),
 'madrid-29': (40.27735, -3.67192, None, 'Los Yesares site, Cañada Real Galiana (OSM / Comunidad de Madrid)'),
 'madrid-30': (40.84370, -3.69267, None, 'Destacamento penal de Bustarviejo (OSM)'),
 'aragon-03': (41.81845, -0.50918, None, 'Trincheras Orwell (OSM)'),
 'aragon-05': (40.39245, -1.10492, None, 'El Muletón (OSM + Nominatim)'),
 'aragon-06': (40.51911, -1.26827, None, 'Calle la Virgen, Villarquemado (official address)'),
 'aragon-07': (41.86686, -0.46073, None, 'Centre of Robres, the old schools (official description)'),
 'aragon-08': (41.40379, -0.48868, None, 'El Purburell hill (OSM)'),
 'aragon-11': (41.05190, -0.13428, None, 'Calle Teniente Moore, Alcañiz (official description)'),
 'aragon-14': (41.42383, -0.49830, None, 'Church of the Asunción, El Piquete (OSM)'),
 'aragon-17': (40.38849, -1.03633, None, 'Alto de la Torana bunker (OSM)'),
 'aragon-18': (42.63373, 0.21871, None, 'Museo de Bielsa (OSM + Nominatim)'),
 'aragon-23': (None, None, 'MEDIUM', 'Exact spot could not be confirmed; label lowered to MEDIUM'),
 'catalonia-13': (41.10950, 0.41983, None, 'Creu dels Quatre Camins (OSM + Nominatim)'),
 'catalonia-25': (42.13043, 1.01664, None, 'Mont de Conques (OSM + Nominatim)'),
 'north-11': (43.04164, -2.65514, None, 'Andikona square, Otxandio (OSM)'),
 'north-13': (43.04008, -3.87813, None, 'Italian mausoleum, Puerto del Escudo (OSM)'),
 'north-16': (43.37098, -2.76377, None, 'Sollube summit (OSM)'),
 'north-20': (43.31207, -2.67622, None, 'Astra air-raid shelter (OSM)'),
 'north-21': (43.36429, -2.99587, None, 'Iron Belt memorial museum, Berango (OSM)'),
 'south-06': (38.17936, -4.03492, None, 'Santuario de la Virgen de la Cabeza (OSM + Nominatim)'),
 'south-08': (36.74035, -4.09895, None, 'Next to the Torre del Mar bus station (official description + Nominatim)'),
 'south-10': (37.41885, -5.98084, None, 'Cementerio de San Fernando (OSM)'),
 'south-12': (37.67903, -4.54862, None, 'Robert Capa plaque, Espejo (OSM)'),
 'south-13': (36.75956, -3.85015, None, 'Old road crossing of the Barranco de Maro (OSM)'),
 'south-15': (36.69604, -3.43541, None, 'Castillo / Fuerte de Carchuna (OSM)'),
 'levant-08': (39.91212, -0.57844, None, 'Civil War trenches, Jérica (OSM)'),
 'levant-10': (39.92004, -0.39126, None, 'Las dos Tetas, Sierra de Espadán (OSM)'),
 'west-01': (38.87807, -6.96434, None, 'Puerta de Trinidad (OSM)'),
 'castile-03': (40.95975, -5.66730, None, 'CDMH, C/ Gibraltar 2 (official tourism site + OSM)'),
}
src, out = sys.argv[1], sys.argv[2]
s = open(src).read(); log = []
for k, (la, lo, conf, why) in F.items():
    m = re.search(r'"id":"' + re.escape(k) + r'","n":"((?:[^"\\]|\\.)*)","r":"[^"]*","la":(-?[\d.]+),"lo":(-?[\d.]+),"c":"([A-Z]+)"', s)
    assert m, k
    a, b = m.start(), m.end(); seg = m.group(0)
    new = seg
    if la is not None: new = new.replace(f'"la":{m.group(2)},"lo":{m.group(3)}', f'"la":{la},"lo":{lo}')
    if conf: new = new.replace(f'"c":"{m.group(4)}"', f'"c":"{conf}"')
    assert s.count(seg) == 1, k
    s = s[:a] + new + s[b:]
    log.append({'id': k, 'name': json.loads('"' + m.group(1) + '"'), 'old': [float(m.group(2)), float(m.group(3))], 'new': [la, lo] if la is not None else None, 'conf': [m.group(4), conf] if conf else None, 'why': why})
open(out, 'w').write(s); json.dump(log, open('scw/scw-fixes-log.json', 'w'), ensure_ascii=False, indent=1)
print(len(log), 'fixes applied')
