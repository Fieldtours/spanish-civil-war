import json
from ux_ec import ux
SRC='/home/claude/ecp/out/'; OUT='/home/claude/aar/ec-out/'
JS=open('/home/claude/aar/aar.js').read(); CSS=open('/home/claude/aar/aar.css').read()
APPS={
 'normandy':dict(k='ecn',place='NORMANDY',guide='Easy Company · Normandy',file='easy-company-normandy'),
 'holland-bastogne':dict(k='ech',place='HOLLAND & BASTOGNE',guide='Easy Company · Holland & Bastogne',file='easy-company-holland-bastogne'),
 'germany-austria':dict(k='ecg',place='GERMANY & AUSTRIA',guide='Easy Company · Germany & Austria',file='easy-company-germany-austria'),
}
UI=""":root{--aar-bg:#f2efe6;--aar-surface:#fffdf8;--aar-ink:#1c1a15;--aar-ink2:#3f3a2e;--aar-faint:#6f6a58;--aar-line:#dcd6c4;--aar-line2:#b9b39c;--aar-btn:#4b5320;--aar-btnInk:#ffffff;--aar-head:#3a4118;--aar-headInk:#f1f0e3;--aar-accent:#a3261e;--aar-tip:#e9e6d4;
--aar-sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;--aar-disp:"Stardos Stencil",Impact,sans-serif;--aar-dispW:700;--aar-mono:"Courier Prime","Courier New",monospace;--aar-hand:"Special Elite","Courier New",monospace}
"""
def rep(s,o,n,c=1):
    assert s.count(o)==c,(o[:70],s.count(o));return s.replace(o,n)
for name,a in APPS.items():
    s=open(SRC+name+'.html',encoding='utf-8').read()
    data=json.load(open('/home/claude/aar/out/'+name+'-full.json'))
    # 1. each guide keeps its own ticks and plan (they were shared between the three guides on dzcharlie.com)
    if a['k']!='ecn':
        k=a['k']
        s=rep(s,'try{visited=JSON.parse(localStorage.getItem("ecn-visited")||"{}")||{}}catch(e){visited={}}',
          'try{["visited","plan","today"].forEach(x=>{const o=x==="today"?"ec-today":"ecn-"+x,n="%s-"+x;if(localStorage.getItem(n)===null&&localStorage.getItem(o)!==null)localStorage.setItem(n,localStorage.getItem(o))})}catch(e){}\ntry{visited=JSON.parse(localStorage.getItem("%s-visited")||"{}")||{}}catch(e){visited={}}'%(k,k))
        s=rep(s,'localStorage.setItem("ecn-visited"','localStorage.setItem("%s-visited"'%k)
        s=rep(s,'localStorage.getItem("ecn-plan")','localStorage.getItem("%s-plan")'%k)
        s=rep(s,'localStorage.setItem("ecn-plan"','localStorage.setItem("%s-plan"'%k)
        s=rep(s,'localStorage.getItem("ec-today")','localStorage.getItem("%s-today")'%k)
        s=rep(s,'localStorage.setItem("ec-today"','localStorage.setItem("%s-today"'%k)
    # 2. css
    i=s.rindex('</style>'); s=s[:i]+UI+CSS+s[i:]
    # 3. slot at the top of the Tour page
    s=rep(s,'function renderTour(){\n  apRenderPanel();\n','function renderTour(){\n  apRenderPanel();\n  {const as=document.getElementById("aar-slot");if(as&&window.AAR)as.innerHTML=AAR.card()}\n')
    # 4. home tile after the tour planner tile, and a row in More
    t0='<button type="button" class="tile" data-go="tab-tour"><span class="k">01</span><b>Tour planner</b>'
    i=s.index(t0); j=s.index('</button>',i)+len('</button>')
    s=s[:j]+'<button type="button" class="tile" data-aar="open"><span class="k">AAR</span><b>After Action Reports</b><span>Optional: save or share your route. A page for each day of your tour, for your journal or to send to family.</span><em>Your journal · stays on your phone</em></button>'+s[j:]
    m0='<div class="rdsec">Use it without internet</div>'
    if False: s=rep(s,m0,'<div class="rdsec">Your journal</div><div class="rdlist"><button type="button" class="rdrow" data-aar="open"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5"/><path d="M9 13h7M9 17h5"/></svg></span><b>After Action Reports</b><small>A page about each day of your tour, to keep or send to family.</small></button></div>'+m0)
    # 5. the module: config + engine, before "MY ROUTE"
    cfg='''window.AAR_CFG={key:"%(k)s-aar",data:%(data)s,
 tourCard:false,docName:"AFTER ACTION REPORT",docNameShort:"After Action Report",plural:"After Action Reports",short:"reports",guide:"%(guide)s",place:"%(place)s",
 foot:"DZ CHARLIE · EASY COMPANY",stamp:"VISITED",done:"COMPLETED",coverTitle:"IN THE FOOTSTEPS OF EASY COMPANY",fileBase:"%(file)s",
 intro:"At the end of each day, write a one-page report: the places you saw, put in the order the events happened, one question to fix it in your memory, and a line in your own words. Keep the pages for your journal, or send them to family.",
 hint:"The moment you want to remember",
 theme:{paper:"#ece5cc",ink:"#1c1a15",ink2:"#3f3a2e",faint:"#6f6a58",title:"#3a4118",when:"#1c1a15",rule:"#8b8a4e",box:"#e2d9ba",stamp:"#a3261e",band:null,bandInk:"#efe9d2",
  disp:"'Stardos Stencil',Impact,sans-serif",dispW:700,mono:"'Courier Prime','Courier New',monospace",hand:"'Special Elite','Courier New',monospace",dispC:'"Stardos Stencil", Impact, sans-serif',monoC:'"Courier Prime", "Courier New", monospace',handC:'"Special Elite", "Courier New", monospace',
  cover:"#3a4118",coverInk:"#efe9d2",coverRule:"#a9a77a",coverStamp:"#e0877d"},
 visited:()=>Object.keys(visited).filter(k=>visited[k]),
 title:ids=>{ensureDdayPool();const c={};ids.forEach(id=>{const p=POOL.find(x=>x.id===id);if(p&&p.day)c[p.day]=(c[p.day]||0)+1});const k=Object.keys(c).sort((a,b)=>c[b]-c[a])[0];return k&&DAYNAMES[k-1]||""},
 stop:id=>{ensureDdayPool();const p=POOL.find(x=>x.id===id);return p?{name:p.name,pri:p.pri}:null},
 onChange:()=>{const as=document.getElementById("aar-slot");if(as&&window.AAR)as.innerHTML=AAR.card()}};
'''%dict(k=a['k'],data=json.dumps(data,ensure_ascii=False),guide=a['guide'],place=a['place'],file=a['file'])
    s=rep(s,'/* ---------- MY ROUTE: add / remove from any tab, route buttons ---------- */',cfg+JS+'\n/* ---------- MY ROUTE: add / remove from any tab, route buttons ---------- */')
    s=ux(s,a['k'])
    open(OUT+name+'.html','w',encoding='utf-8').write(s); print(name,len(s))
