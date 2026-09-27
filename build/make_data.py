import json,re
from shapely.geometry import Polygon
from shapely.ops import unary_union
geo=json.load(open('geo/spain_geo.json'))
regmeta=json.load(open('build/regions_meta.json'))
phases=json.load(open('build/phases_meta.json'))
ctx=json.load(open('research/context.json'))
W=json.load(open('research/weapons.json'))
stops=[]
for r in ['madrid','aragon','catalonia','north','south','levant','west','castile']:
  stops+=json.load(open('research/'+r+'.json'))
FIX=json.load(open('research/coord_fixes.json'))
FX={f[0]:f for f in FIX}
for s in stops:
  if s['id'] in FX: f=FX[s['id']];s['lat'],s['lon'],s['certainty']=f[5],f[6],f[7]
order={r['id']:i for i,r in enumerate(regmeta)}
stops.sort(key=lambda s:(order[s['region']],s['pri'],s['id']))
RNOTES=[]
NOTE=re.compile(r'verified|re-verified|this pass|coordinates|Mapcarta|Wikidata|fetched source|source checked|not confirmed from|exact (position|location|spot|address|entrance)|should be checked|check against|in the Teruel city article|follow Wikipedia|Wikipedia gives|from Wikipedia',re.I)
def split_ds(sid,ds):
  if not ds: return ''
  parts=re.split(r'(?<=[.;])\s+(?=[A-Z(])',ds.strip())
  keep=[];
  for p in parts:
    if NOTE.search(p): RNOTES.append((sid,p))
    else: keep.append(p)
  return ' '.join(keep).strip()
S=[]
for s in stops:
  s['disputed']=split_ds(s['id'],s.get('disputed'))
  s['plan']=s['plan'].replace('Opening hours were not verified, so contact','Opening hours vary; contact')
  pp=re.split(r'(?<=[.;])\s+(?=[A-Z])',s['plan'].strip());kp=[]
  for p in pp:
    if re.search(r'Coordinates|to be confirmed',p): RNOTES.append((s['id'],p));kp.append('The pin marks the town: ask locally for the exact spot.')
    else: kp.append(p)
  s['plan']=' '.join(kp)
  S.append({'id':s['id'],'n':s['name'],'r':s['region'],'la':round(s['lat'],5),'lo':round(s['lon'],5),'c':s['certainty'],'p':s['pri'],'m':int(s['min']),'k':s['cat'],'ph':s['phase'],'d':s['date'],'t':s['text'],'lk':s['look'],'pl':s['plan'],'pv':bool(s.get('priv')),'tw':s.get('town',''),'src':[u for u in ([s.get('coord_source')]+s.get('sources',[])) if u and u.startswith('http')][:5],'ds':s.get('disputed') or ''})
regions=[]
for r in regmeta:
  pl=geo['regions'][r['id']]
  u=unary_union([Polygon(p[0]) for p in pl]);c=u.representative_point()
  if r['id']=='levant': c=type(c)(-0.75,39.1)
  if r['id']=='castile': c=type(c)(-4.6,41.9)
  if r['id']=='madrid': c=type(c)(-3.3,39.6)
  regions.append(dict(r,poly=pl,lab=[round(c.y,3),round(c.x,3)]))
BLINK={'madrid-nov-1936':['madrid-01','madrid-09','madrid-10','madrid-11'],'jarama-1937':['madrid-03','madrid-04','madrid-14','madrid-15','madrid-21'],'guadalajara-1937':['madrid-17'],'belchite-1937':['aragon-01','aragon-13'],'teruel-1937':['aragon-02','aragon-05'],'ebro-1938':['catalonia-03','catalonia-01','catalonia-02','catalonia-10','catalonia-11','catalonia-14','catalonia-16']}
battles=[]
for b in ctx['battles']:
  b=dict(b);b['stops']=BLINK.get(b['id'],[]);b['stop']=b['stops'][0] if b['stops'] else ''
  battles.append(b)
IMG={'mauser-1893':('w-mauser','Drawing of the Spanish Mauser from the Encyclopaedia Britannica, 1911 (public domain).'),
 'mosin-nagant':('w-mosin','Mosin–Nagant M1891. Photo: Armémuseum, Stockholm (public domain), via Wikimedia Commons.'),
 'maxim-1910':('w-maxim','Maxim M1910 on its wheeled Sokolov mount. Photo: Geni, CC BY-SA 4.0, via Wikimedia Commons.'),
 'naranjero':('w-naranjero','The German MP 28, the gun the naranjero copied. Photo: NatanFlayer, CC BY-SA 3.0, via Wikimedia Commons.'),
 'astra-400':('w-astra','Astra 400 pistol. Photo: V-Hantarex, CC BY 4.0, via Wikimedia Commons.'),
 't-26':('w-t26','T-26B tank in Republican markings. Photo: MCAE Consulting, CC0, via Wikimedia Commons.'),
 'panzer-i':('w-panzer','Panzer I tanks during Condor Legion training in Spain. Bundesarchiv, Bild 183-E20569-21, CC BY-SA 3.0 DE.'),
 'cv-33':('w-cv33','Italian CV-33 tankette. Public domain, via Wikimedia Commons.'),
 'i-16':('w-i16','Polikarpov I-16 in Spanish Republican markings. Photo: Elchuso, CC BY-SA 4.0, via Wikimedia Commons.'),
 'ju-52':('w-ju52','A Condor Legion Junkers aircraft in Spain. Bundesarchiv, Bild 183-C0214-0007-013, CC BY-SA 3.0 DE.'),
 'he-111':('w-he111','Heinkel He 111 B of the Condor Legion, Spain 1937–38. Public domain, via Wikimedia Commons.'),
 'sm-79':('w-sm79','Savoia-Marchetti S.M.79 in the markings of the Aviazione Legionaria. Photo: Contando Estrelas, CC BY-SA 2.0, via Wikimedia Commons.'),
 'flak-18':('w-flak','8.8 cm Flak 18 gun preserved in Spain. Photo: Z3144228, CC BY-SA 4.0, via Wikimedia Commons.')}
weapons=[]
WNOTES=[]
def clean(story,wid):
  urls=re.findall(r'https?://[^\s;)]+',story)
  cut=re.search(r'\s(Source \(general\)|Sources?:|Treat as|Details of the Laffitte)',story)
  if cut:
    WNOTES.append((wid,story[cut.start():].strip()))
    story=story[:cut.start()].strip()
  if wid=='laffitte': pass
  return story,[u.rstrip('.') for u in urls]
for w in W:
  w['story'],w['src']=clean(w.get('story',''),w['id'])
  im=IMG.get(w['id'])
  weapons.append({'id':w['id'],'name':w['name'],'side':w['side'],'origin':w.get('origin',''),'specs':w.get('specs',[]),'t':w['t'],'good':w.get('good',''),'bad':w.get('bad',''),'changes':w.get('changes',''),'story':w.get('story',''),'img':('img/'+im[0]+'.jpg') if im else '','cap':im[1] if im else '','src':w['src']})
REGIMG={'madrid':('reg-madrid','Madrid after the air raid of 17 November 1936. Public domain.'),'aragon':('reg-aragon','Republican soldiers in the Battle of Teruel, winter 1937–38. Public domain (Google Art Project).'),'catalonia':('reg-catalonia','Republican forces crossing the Ebro, July 1938. Public domain (Google Art Project).'),'north':('reg-north','Gernika in ruins after the bombing of 26 April 1937. Public domain.'),'south':('reg-south','Inside the Civil War shelters of Almería. Photo: Shadowgate, CC BY 2.0.'),'levant':('reg-levant','A Civil War air-raid shelter under the Col·legi Balmes, Valencia. Photo: Fernando Mafé, CC BY-SA 4.0.'),'west':('reg-west','The bullring of Badajoz, August 1936. Public domain.'),'castile':('reg-castile','Generals Franco and Mola in Burgos, 1936. Public domain.')}
for r in regions:
  im=REGIMG[r['id']];r['img']='img/'+im[0]+'.jpg';r['cap']=im[1]
credits=["Cover and welcome: ruins of old Belchite — Diego Delso (CC BY-SA 4.0) and Fernando (CC BY-SA 2.0), via Wikimedia Commons."]+[f"{REG}: {c}" for REG,c in [(r['name'],r['cap']) for r in regions]]+["Poble Vell de Corbera d'Ebre — Juan Emilio Prades Bel (CC BY 4.0), via Wikimedia Commons."]+[w['cap'] for w in weapons if w['cap']]
simg={'catalonia-01':('img/stop-corbera.jpg',"The Poble Vell of Corbera d'Ebre today. Photo: Juan Emilio Prades Bel, CC BY 4.0.")}
for s in S:
  if s['id'] in simg: s['img'],s['imgc']=simg[s['id']]
ib=[x for x in ctx['glossary']]
D={'stops':S,'regions':regions,'phases':phases,'time':ctx['time'],'people':ctx['people'],'brief':ctx['briefing'],'orig':ctx['origins'],'factors':ctx['factors'],'clock':ctx['clock'],'gloss':ctx['glossary'],'links':ctx['links'],'battles':battles,'weapons':weapons,'credits':credits,
   'geo':{k:geo[k] for k in ['land','countries','prov','rivers','lakes','roads','places','mtns']}}
# extra mountain labels
extra=[["Sierra de Guadarrama",40.80,-4.00],["Sistema Ibérico",41.20,-2.20],["Montes de Toledo",39.50,-4.30],["Sierra de Gredos",40.25,-5.20],["Serra de Pàndols",41.01,0.47],["Sierra de Alcubierre",41.78,-0.45],["Montes Universales",40.35,-1.70],["Maestrazgo",40.55,-0.25],["Picos de Europa",43.20,-4.85]]
for n,la,lo in extra: D['geo']['mtns'].append({'n':n,'c':[la,lo],'r':6,'p':[]})
s=json.dumps(D,ensure_ascii=False,separators=(',',':'))
open('build/data.js','w').write('window.SCW='+s+';')
json.dump(RNOTES,open('research/stop_notes.json','w'),ensure_ascii=False,indent=1)
json.dump(WNOTES,open('research/weapon_notes.json','w'),ensure_ascii=False,indent=1)
print(len(s)//1024,'KB',len(S))
