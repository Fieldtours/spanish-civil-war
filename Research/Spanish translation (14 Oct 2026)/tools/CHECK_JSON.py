"""usage: python3 tools/CHECK_JSON.py EN.json ES.json  — checks same shape and unchanged fixed keys."""
import json,sys
FIX={"id","sort","a","solemn","stop","stops","url","img"}
def cmp(e,s,p="$"):
    if isinstance(e,dict):
        assert isinstance(s,dict), p
        assert set(e)==set(s), f"{p}: keys differ {set(e)^set(s)}"
        for k in e:
            if k in FIX: assert e[k]==s[k], f"{p}.{k} changed"
            cmp(e[k],s[k],f"{p}.{k}")
    elif isinstance(e,list):
        assert isinstance(s,list) and len(e)==len(s), f"{p}: list length"
        for i,(x,y) in enumerate(zip(e,s)): cmp(x,y,f"{p}[{i}]")
    elif isinstance(e,str):
        assert isinstance(s,str), p
    else:
        assert e==s, f"{p}: value changed"
e=json.load(open(sys.argv[1])); s=json.load(open(sys.argv[2]))
for k in ("geo_names","map_labels"):
    if k in e:
        assert isinstance(s[k],dict) and set(s[k])==set(e[k]), k
        e=dict(e); s=dict(s); e.pop(k); s.pop(k)
cmp(e,s); print("OK", sys.argv[2])
