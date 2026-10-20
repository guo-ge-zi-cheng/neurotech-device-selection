"""Check repository integrity, local references and comparison consistency."""
from pathlib import Path
from urllib.parse import urlparse, unquote
import json, re, sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]
def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
D=read('data/device-records.json')
C=read('data/screening-matrix.json')
S=read('data/source-catalog.json')
ids={s['id'] for s in S}
if len(ids)!=len(S): errors.append('Duplicate source IDs')
if len(D)!=9 or len(C)!=9: errors.append('Expected nine device records and nine comparison rows')
if {d['id'] for d in D}!={c['device_id'] for c in C}: errors.append('Comparison/device ID mismatch')
readme=(ROOT/'README.md').read_text(encoding='utf-8')
if readme.count('## TL;DR')!=1: errors.append('TL;DR missing or duplicated')

for d,c in zip(D,C):
    if d['id']!=c['device_id']: errors.append('Device ordering mismatch')
    if len(c['grades'])!=5 or set(c['grades'])-{'S','P','G'}: errors.append('Invalid readiness labels')
    if not(len(c['why'])==len(c['topic_sources'])==5): errors.append('Incomplete grade explanations')
    p=ROOT/c['report']
    if not p.is_file(): errors.append(f'Missing report {p}');continue
    text=p.read_text(encoding='utf-8')
    expected='| ['+d['name']+']('+c['report']+') | '+' | '.join(c['grades'])+' |'
    if expected not in readme: errors.append(f'Comparison row out of sync: {d["id"]}')
    for i in range(1,6):
        if f'### {i}. ' not in text: errors.append(f'Missing coursework topic in {d["id"]}')
    all_refs=d['sources']+[k for keys in c['topic_sources'] for k in keys]
    for contact in d['contacts']:
        all_refs.append(contact['source'])
        if contact.get('route_source'): all_refs.append(contact['route_source'])
    for key in all_refs:
        if key not in ids: errors.append(f'Unknown source {key} in {d["id"]}')

checked=0
for p in ROOT.rglob('*'):
    if not p.is_file() or '.git' in p.parts: continue
    if p.suffix.lower() in ['.pdf','.zip']: errors.append(f'Unintended binary/source archive: {p}')
    if p.suffix not in ['.md','.json','.py'] and p.name not in ['.gitignore','.gitattributes']: continue
    text=p.read_text(encoding='utf-8')
    if re.search(r'[\u3400-\u4dbf\u4e00-\u9fff]',text): errors.append(f'Non-English CJK text: {p}')
    if re.search(r'[A-Za-z]:[\\/](?:Users|home)[\\/]',text): errors.append(f'Nonportable local user path: {p}')
    if p.suffix!='.md': continue
    definitions=dict(re.findall(r'^\[([^\]]+)\]:\s*(\S+)',text,re.M))
    links=re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)]+)\)',text)
    for label in re.findall(r'\[[^\]\n]+\]\[([^\]\n]+)\]',text):
        if label not in definitions: errors.append(f'Unresolved reference {label} in {p.name}')
    for link in links:
        u=urlparse(link.strip('<>'))
        if u.scheme or link.startswith('#'): continue
        if not (p.parent/unquote(u.path)).exists(): errors.append(f'Broken local link in {p.name}: {link}')
        checked+=1

for p in (ROOT/'tools').glob('*.py'):
    try: compile(p.read_text(encoding='utf-8'),str(p),'exec')
    except SyntaxError as e: errors.append(f'Script syntax: {e}')
result={'status':'PASS' if not errors else 'FAIL','devices':len(D),'public_sources':len(S),'local_links_checked':checked,'errors':errors,
        'limits':'Structural consistency and local references only; not a fresh clinical, patent, payer, contact or independent human audit.'}
print(json.dumps(result,indent=2))
sys.exit(bool(errors))
