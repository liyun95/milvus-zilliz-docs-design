"""Count new User Guide link targets: python3 churn.py <milvus-docs> <sha> <file of "date commit" lines>"""
import subprocess,re,sys,os
repo=sys.argv[1]
def targets(sha):
    fs=[f for f in subprocess.run(['git','-C',repo,'ls-tree','-r','--name-only',sha,'site/en/userGuide'],capture_output=True,text=True).stdout.split('\n') if f.endswith('.md')]
    t=set()
    for f in fs:
        s=subprocess.run(['git','-C',repo,'show',f'{sha}:{f}'],capture_output=True,text=True).stdout
        s=re.sub(r'```.*?```','',s,flags=re.S)
        for u in re.findall(r'(?<!!)\[[^\]]+\]\(([^)\s]+)\)',s):
            if u.startswith(('http','#','mailto')): continue
            p=u.split('#')[0]
            if p.endswith('.md'): t.add(os.path.basename(p))
    return t,len(fs)
now,nf=targets(sys.argv[2]); print('now',len(now),'files',nf)
for line in open(sys.argv[3]):
    d,c=line.split(); old,of=targets(c); new=now-old
    print(d,'targets',len(old),'files',of,'new_since',len(new),sorted(new)[:12])
