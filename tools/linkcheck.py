import os,re,sys,glob
import os; R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')+'/'; bad=0; n=0
for f in glob.glob(R+'**/*.html',recursive=True):
    if '_h.html' in f: continue
    t=open(f,encoding='utf-8').read()
    ids=set(re.findall(r'id="([^"]+)"',t))
    for m in re.finditer(r'(?:href|src|srcset)="([^"]+)"',t):
        u=m.group(1)
        if re.match(r'(https?:|mailto:|data:)',u): continue
        u=u.split(' ')[0]
        if u.startswith('#'):
            n+=1
            if u[1:] not in ids: bad+=1;print('NOANCHOR',f,u)
            continue
        p,_,a=u.partition('#'); p=p.split('?')[0]
        base=R+p.lstrip('/') if p.startswith('/') else os.path.join(os.path.dirname(f),p)
        if base.endswith('/'): base+='index.html'
        n+=1
        if not os.path.isfile(base): bad+=1;print('MISSING',f.replace(R,''),u)
        elif a and base.endswith('.html') and a not in set(re.findall(r'id="([^"]+)"',open(base).read())): bad+=1;print('NOANCHOR',f,u)
print('checked',n,'refs; broken',bad)
