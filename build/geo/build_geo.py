import json
from shapely.geometry import shape, box, mapping, MultiPolygon, Polygon, LineString, MultiLineString
from shapely.ops import unary_union
BB=box(-10.2,35.2,4.8,44.4)
def rnd(c,n=3): return [round(c[0],n),round(c[1],n)]
def polys(g):
  if g.is_empty: return []
  gs=[g] if isinstance(g,Polygon) else list(getattr(g,'geoms',[]))
  out=[]
  for p in gs:
    if not isinstance(p,Polygon) or p.area<0.0004: continue
    out.append([ [rnd(c) for c in p.exterior.coords] ])
  return out
def lines(g):
  if g.is_empty: return []
  gs=[g] if isinstance(g,LineString) else [x for x in getattr(g,'geoms',[]) if isinstance(x,LineString)]
  return [[rnd(c) for c in l.coords] for l in gs if len(l.coords)>1]
REG={'Madrid':'madrid','Castilla-La Mancha':'madrid','Aragón':'aragon','Cataluña':'catalonia','País Vasco':'north','Cantabria':'north','Asturias':'north',
 'Andalucía':'south','Valenciana':'levant','Murcia':'levant','Islas Baleares':'levant','Extremadura':'west','Castilla y León':'castile','Galicia':'castile','Foral de Navarra':'castile','La Rioja':'castile'}
d=json.load(open('ne_10m_admin_1_states_provinces.geojson'))
prov=[];regs={}
for f in d['features']:
  p=f['properties']
  if p['admin']!='Spain' or p['region'] not in REG: continue
  g=shape(f['geometry']).buffer(0)
  regs.setdefault(REG[p['region']],[]).append(g)
  prov.append({'n':p['name'],'b':lines(g.boundary.simplify(0.01))})
R={}
for k,v in regs.items():
  u=unary_union(v).simplify(0.012)
  R[k]=polys(u)
# land
land=unary_union([shape(f['geometry']).buffer(0) for f in json.load(open('ne_10m_land.geojson'))['features']]).intersection(BB).simplify(0.006)
countries={}
for f in json.load(open('ne_10m_admin_0_countries.geojson'))['features']:
  n=f['properties']['ADMIN']
  if n in ('Spain','Portugal','France','Morocco','Andorra','Gibraltar'):
    g=shape(f['geometry']).buffer(0).intersection(BB).simplify(0.006)
    if not g.is_empty: countries[n]=polys(g)
spain_outline=unary_union([g for v in regs.values() for g in v])
# rivers
rv=[]
for fn in ['ne_10m_rivers_lake_centerlines.geojson','ne_10m_rivers_europe.geojson']:
  for f in json.load(open(fn))['features']:
    g=shape(f['geometry']).intersection(BB)
    if g.is_empty: continue
    sr=f['properties'].get('scalerank',10) or 10
    rv.append({'n':f['properties'].get('name') or '', 'r':sr, 'l':lines(g.simplify(0.004))})
lk=[]
for f in json.load(open('ne_10m_lakes.geojson'))['features']:
  g=shape(f['geometry']).buffer(0).intersection(BB)
  if not g.is_empty: lk+=polys(g.simplify(0.003))
SP=unary_union([g for v in regs.values() for g in v]).buffer(0.02)
rd=[]
for f in json.load(open('ne_10m_roads.geojson'))['features']:
  p=f['properties']
  g=shape(f['geometry'])
  if not g.intersects(SP): continue
  g=g.intersection(SP)
  if g.is_empty: continue
  rd.append({'t':1 if p.get('type')=='Major Highway' else 2,'l':lines(g.simplify(0.003))})
pl=[]
for f in json.load(open('ne_10m_populated_places.geojson'))['features']:
  p=f['properties']
  if p['ADM0NAME']!='Spain' and p['ADM0NAME'] not in('Portugal','France','Morocco','Andorra','Gibraltar'): continue
  x,y=f['geometry']['coordinates']
  if not BB.contains(shape(f['geometry'])): continue
  pop=p.get('POP_MAX') or 0
  if p['ADM0NAME']!='Spain' and pop<300000: continue
  if pop<12000 and not p.get('ADM1CAP'): continue
  pl.append([p['NAME'],round(y,3),round(x,3),pop,1 if p.get('ADM0CAP') else (2 if p.get('ADM1CAP') else 3)])
mt=[]
for f in json.load(open('ne_10m_geography_regions_polys.geojson'))['features']:
  p=f['properties']
  if p.get('FEATURECLA')!='Range/mtn': continue
  g=shape(f['geometry']).buffer(0)
  if not g.intersects(spain_outline): continue
  g=g.intersection(BB)
  c=g.representative_point()
  mt.append({'n':p.get('NAME_EN') or p.get('NAME'),'c':[round(c.y,3),round(c.x,3)],'r':p.get('SCALERANK'),'p':polys(g.simplify(0.02))})
out={'bb':[-10.2,35.2,4.8,44.4],'land':polys(land),'countries':countries,'regions':R,'prov':prov,'rivers':rv,'lakes':lk,'roads':rd,'places':pl,'mtns':mt}
s=json.dumps(out,separators=(',',':'),ensure_ascii=False)
open('/home/claude/scw/geo/spain_geo.json','w').write(s)
print(len(s)//1024,'KB', {k:len(v) for k,v in out.items() if isinstance(v,(list,dict))})
print(mt)
