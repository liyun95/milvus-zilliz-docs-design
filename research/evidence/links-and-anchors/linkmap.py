import subprocess, re, os, sys, json, collections, glob
repo, sha, cloud = sys.argv[1], sys.argv[2], sys.argv[3]
def git(*a): return subprocess.run(['git','-C',repo,*a],capture_output=True,text=True,check=True).stdout
def fm(s):
    m=re.match(r'^---\n(.*?)\n---',s,re.S); d={}
    if m:
        for l in m.group(1).split('\n'):
            k,_,v=l.partition(':'); d[k.strip()]=v.strip().strip('"\'')
    return d
def strip_code(s): return re.sub(r'```.*?```','',s,flags=re.S)
LINK=re.compile(r'(?<!!)\[([^\]]+)\]\(([^)\s]+)\)')
norm=lambda t: re.sub(r'[^a-z0-9]+',' ',re.sub(r'`|\*','',t).lower()).strip()
# Milvus pages
allfiles=[f for f in git('ls-tree','-r','--name-only',sha,'site/en').split('\n') if f.endswith('.md') and '/fragments/' not in f]
mil={}
for f in allfiles:
    s=git('show',f'{sha}:{f}'); d=fm(s); base=os.path.basename(f)
    mil[base]={'path':f,'title':d.get('title',''),'text':s}
scope=[f for f in allfiles if f.startswith('site/en/userGuide/')]
mlinks=[]
for f in scope:
    for t,u in LINK.findall(strip_code(mil[os.path.basename(f)]['text'])):
        if u.startswith(('http','#','mailto')): continue
        p=u.split('#')[0]
        if not p.endswith('.md'): mlinks.append((f,t,u,None)); continue
        mlinks.append((f,t,u,os.path.basename(p)))
# Cloud pages
cl={}
for f in glob.glob(cloud+'/**/*.md*',recursive=True):
    s=open(f).read(); d=fm(s); slug=d.get('slug','').lstrip('/')
    if not slug: continue
    title=re.sub(r'\s*\|\s*(Cloud|BYOC)\s*$','',d.get('title',''))
    links=[(t,u) for t,u in LINK.findall(strip_code(s)) if u.startswith('./')]
    cl[slug]={'title':title,'links':links,'path':f}
title2slug=collections.defaultdict(set)
for k,v in cl.items(): title2slug[norm(v['title'])].add(k)
targets=collections.Counter(x[3] for x in mlinks if x[3])
uniq=list(targets)
# page correspondence for harvesting: Milvus source page -> Cloud page
def corr(base):
    slug=base[:-3]
    if slug in cl: return slug,'same-name'
    ts=title2slug.get(norm(mil.get(base,{}).get('title','')),set())
    if len(ts)==1: return next(iter(ts)),'title'
    return None,None
src_pages=sorted({os.path.basename(x[0]) for x in mlinks})
pairs={b:corr(b) for b in src_pages}
# harvest
votes=collections.defaultdict(collections.Counter)
for f,t,u,X in mlinks:
    if not X: continue
    P,_=pairs[os.path.basename(f)]
    if not P: continue
    cands=[cu for ct,cu in cl[P]['links'] if norm(ct)==norm(t)]
    for cu in set(c[2:].split('#')[0] for c in cands): votes[X][cu]+=1
# strategies per unique target
res={}
for X in uniq:
    same = X[:-3] if X[:-3] in cl else None
    ts = title2slug.get(norm(mil.get(X,{}).get('title','')),set()) if X in mil else set()
    title = next(iter(ts)) if len(ts)==1 else None
    hv = votes.get(X); harvest = hv.most_common(1)[0][0] if hv else None
    conflict = bool(hv and len(hv)>1)
    res[X]=dict(same=same,title=title,harvest=harvest,conflict=conflict,exists=X in mil,section=mil[X]['path'].split('/')[2] if X in mil else '?')
def cov(key, weight=False):
    n=sum((targets[X] if weight else 1) for X in uniq if res[X][key]); d=sum(targets.values()) if weight else len(uniq); return f'{n}/{d} ({n*100//d}%)'
out={}
out['milvus_scope_pages']=len(scope); out['links_total']=len(mlinks); out['links_md']=sum(1 for x in mlinks if x[3]); out['links_non_md']=[x[2] for x in mlinks if not x[3]][:15]
out['unique_targets']=len(uniq); out['cloud_pages']=len(cl)
out['src_pairs']=collections.Counter(v[1] for v in pairs.values())
for k in ['same','title','harvest']: out['cov_'+k]=(cov(k),cov(k,True))
any_=lambda X: res[X]['same'] or res[X]['title'] or res[X]['harvest']
n=sum(1 for X in uniq if any_(X)); w=sum(targets[X] for X in uniq if any_(X)); out['cov_any']=(f'{n}/{len(uniq)}',f'{w}/{sum(targets.values())}')
# agreement
agree=lambda a,b: [X for X in uniq if res[X][a] and res[X][b]]
for a,b in [('same','harvest'),('title','harvest'),('same','title')]:
    xs=agree(a,b); out[f'agree_{a}_{b}']=f'{sum(1 for X in xs if res[X][a]==res[X][b])}/{len(xs)}'
    out[f'disagree_{a}_{b}']=[(X,res[X][a],res[X][b]) for X in xs if res[X][a]!=res[X][b]][:10]
out['harvest_conflicts']=[(X,dict(votes[X])) for X in uniq if res[X]['conflict']][:10]
unres=[X for X in uniq if not any_(X)]
out['unresolved_by_section']=collections.Counter(res[X]['section'] for X in unres)
out['unresolved_links_weight']=sum(targets[X] for X in unres)
out['unresolved_missing_in_milvus']=[X for X in unres if not res[X]['exists']]
out['unresolved_sample']=[(X,targets[X],res[X]['section'],mil.get(X,{}).get('title','')) for X in sorted(unres,key=lambda x:-targets[x])[:40]]
pil={}
for p in ['delete-entities.md','filtered-search.md','openai.md']:
    ls=[x for x in mlinks if os.path.basename(x[0])==p]
    pil[p]=[(x[2],res.get(x[3]) if x[3] else 'non-md') for x in ls]
out['pilots']=pil
json.dump(res,open('linkmap-res.json','w'),indent=0)  # per-target results, written to the current directory
print(json.dumps(out,indent=1,ensure_ascii=False,default=str))
