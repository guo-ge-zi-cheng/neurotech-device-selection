"""Check document/data consistency and references, not the truth of every claim."""
from pathlib import Path
from urllib.parse import urlparse,unquote
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
D=load('data/device-records.json');S=load('data/source-catalog.json');M=load('data/screening-matrix.json')
errors=[];ids={s['id'] for s in S};links_checked=0
topics=['Unmet medical need','Intellectual property','Fundraising','Regulatory','Reimbursement']
expected_ids=['precision','rns','ceribell','saint','exablate']
if [d['id'] for d in D]!=expected_ids or [m['device_id'] for m in M]!=expected_ids:errors.append('Expected exactly the five selected devices')
expected_reports={Path(m['report']).name for m in M}
actual_reports={p.name for p in (ROOT/'devices').glob('*.md') if p.name!='README.md'}
if actual_reports!=expected_reports:errors.append('Device report files do not match the five-device scope')
if {c['device_id'] for c in load('data/contacts.json')} != set(expected_ids):errors.append('Contact scope mismatch')
if len(ids)!=len(S):errors.append('Duplicate source IDs')
readme=(ROOT/'README.md').read_text(encoding='utf-8')
if len(readme.split())>1050:errors.append('README exceeds the short comparison budget')
for d,m in zip(D,M):
    if d['id']!=m['device_id']:errors.append('Matrix/device mismatch')
    if [s['topic'] for s in d['sections']]!=topics:errors.append(f'Five required topics missing: {d["id"]}')
    if len(' '.join(d['description']).split())<150:errors.append(f'Device explanation too short: {d["id"]}')
    expected=f'| [{d["name"]}]({m["report"]}) | '+' | '.join(s['access'] for s in d['sections'])+' |'
    if expected not in readme:errors.append(f'Comparison out of sync: {d["id"]}')
    text=(ROOT/m['report']).read_text(encoding='utf-8')
    for field in ['What we found:','How it helps write this section:','Still needed:','How close is it to this device?']:
        if text.count(field)!=5:errors.append(f'Missing source-use explanation: {d["id"]}: {field}')
    for s in d['sections']:
        for k in s['sources']:
            if k not in ids:errors.append(f'Unknown source: {k}')
    for c in d['contacts']:
        for key in ['connection','how_helpful','limits','route','sources']:
            if not c.get(key):errors.append(f'Contact has no {key}: {d["id"]}')
        for k in c['sources']:
            if k not in ids:errors.append(f'Unknown contact source: {k}')
for p in ROOT.rglob('*'):
    if not p.is_file() or '.git' in p.parts or p.suffix not in ['.md','.json','.py']:continue
    text=p.read_text(encoding='utf-8')
    if p.suffix in ['.md','.json'] and re.search(r'Gregory Scott|Matthew Walker|Will Mandy|gregory\.scott99|w\.mandy',text,re.I):errors.append(f'Unjustified broad-domain recommendation remains: {p.name}')
    if re.search(r'[\u3400-\u4dbf\u4e00-\u9fff]',text):errors.append(f'CJK text in English repository: {p}')
    if p.suffix=='.md':
        for url in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)]+)\)',text):
            u=urlparse(url)
            if u.scheme or url.startswith('#'):continue
            if not (p.parent/unquote(u.path)).exists():errors.append(f'Broken link in {p.name}: {url}')
            links_checked+=1
for p in (ROOT/'tools').glob('*.py'):
    try:compile(p.read_text(encoding='utf-8'),str(p),'exec')
    except SyntaxError as e:errors.append(str(e))
result=dict(status='PASS' if not errors else 'FAIL',devices=len(D),sources=len(S),contacts=sum(len(d['contacts']) for d in D),local_links_checked=links_checked,readme_words=len(readme.split()),errors=errors,limits='Structure, source pointers and consistency only; no interview or independent clinical/patent/payer audit.')
print(json.dumps(result,indent=2));sys.exit(bool(errors))
