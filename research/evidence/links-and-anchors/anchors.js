const {execFileSync}=require('child_process');
const slugify=require('slugify');
const [repo,sha]=process.argv.slice(2);
const git=(...a)=>execFileSync('git',['-C',repo,...a],{maxBuffer:1<<28}).toString();
const files=git('ls-tree','-r','--name-only',sha,'site/en').split('\n').filter(f=>f.endsWith('.md')&&!f.includes('/fragments/'));
const inScope=f=>/^site\/en\/(userGuide|embeddings)/.test(f);
const clean=t=>t.replace(/\[([^\]]*)\]\([^)]*\)/g,'$1').replace(/<[^>]+>/g,'').replace(/`/g,'').replace(/\*\*|__|\*/g,'').trim();
const milvusId=t=>clean(t).replace(/\s+/g,'-').replace(/[^A-Za-z0-9-]/g,'');
const zdocId=t=>slugify(clean(t),{lower:true,strict:true});
const heads={}; const stats={all:0,scope:0,mismatch:0,scopeMismatch:0}; const causes={}; const examples=[];
const linksRaw=[];
for(const f of files){
  const s=git('show',`${sha}:${f}`); let inCode=false; const hs=[];
  for(const line of s.split('\n')){
    if(/^\s*```/.test(line)){inCode=!inCode;continue}
    if(inCode) continue;
    const m=line.match(/^(#{2,4})\s+(.+?)\s*$/); if(m){hs.push(m[2]);}
    for(const l of line.matchAll(/\]\(([^)\s]+?\.md)#([^)\s]+)\)/g)) linksRaw.push({from:f,target:l[1],anchor:l[2]});
  }
  heads[f.split('/').pop()]=heads[f.split('/').pop()]||[];
  for(const h of hs){
    const mi=milvusId(h), zi=zdocId(h); heads[f.split('/').pop()].push({h,mi,zi});
    stats.all++; if(inScope(f)) stats.scope++;
    if(mi.toLowerCase()!==zi){ stats.mismatch++; if(inScope(f)) stats.scopeMismatch++;
      const c=/&/.test(h)?'&':/[<>|$%]/.test(h)?'<>|$%':/\s-\s|--/.test(h)?'连字符或多个空格':/[^\x00-\x7f]/.test(clean(h))?'非 ASCII 字符':/[_]/.test(h)?'下划线':'其他';
      causes[c]=(causes[c]||0)+1; if(examples.length<25) examples.push([c,h,mi,zi]); }
  }
}
// cross-page anchor links in scope
let L={total:0,resolved:0,lowerOk:0,lowerBad:0,unresolved:0}; const bad=[];
for(const l of linksRaw.filter(l=>inScope(l.from)&&!l.target.startsWith('http'))){
  L.total++; const name=l.target.split('/').pop(); const hs=heads[name];
  const hit=hs&&hs.find(x=>x.mi===l.anchor);
  if(!hit){L.unresolved++; if(!hs) L.noTarget=(L.noTarget||0)+1; else if(hs.some(x=>x.mi.toLowerCase()===l.anchor.toLowerCase())) L.caseOnly=(L.caseOnly||0)+1; else if(process.env.SHOW) console.log("UNRES",l.from,l.target+"#"+l.anchor); continue} L.resolved++;
  if(l.anchor.toLowerCase()===hit.zi) L.lowerOk++; else {L.lowerBad++; bad.push([l.from,l.target+'#'+l.anchor,hit.zi])}
}
console.log(JSON.stringify({stats,causes,links:L},null,1));
console.log('EXAMPLES'); for(const e of examples) console.log(e.join(' || '));
console.log('BAD LINKS'); for(const b of bad) console.log(b.join(' || '));
