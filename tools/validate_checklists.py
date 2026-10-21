"""Check complete matching, reference pointers, access honesty and preserved prior evidence."""
from pathlib import Path
import json,re,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
d=load('data/evidence-checklists.json');sources={s['id'] for s in load('data/source-catalog.json')}
reading=load('data/research-explanations.json')
expected=['precision','rns','ceribell','saint','exablate','arcex','terra'];errors=[]
reqs=[r['id'] for s in d['sections'] for r in s['requirements']]
if len(reqs)!=31 or len(set(reqs))!=31:errors.append('31 unique requirements required')
if [x['device_id'] for x in d['devices']]!=expected:errors.append('Seven-device scope changed')
routes={r['id'] for r in d['routes']}
questions={q['id']:q for q in reading['requirements']}
readable={x['device_id']:x for x in reading['devices']}
if list(questions)!=reqs:errors.append('Readable requirements do not match original 31 questions')
if list(readable)!=expected:errors.append('Readable device scope mismatch')
for path,key in [('data/evidence-checklists.json','basis_sha256'),('data/source-catalog.json','source_catalog_sha256')]:
    if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=reading[key]:errors.append('Evidence basis changed during readability rewrite: '+path)
for dev in d['devices']:
    if [r['requirement_id'] for r in dev['rows']]!=reqs:errors.append('Requirement coverage mismatch '+dev['device_id'])
    p=ROOT/f'research/{dev["device_id"]}.md';text=p.read_text(encoding='utf-8')
    points={r['requirement_id']:r for r in readable[dev['device_id']]['points']}
    if list(points)!=reqs:errors.append('Readable point coverage mismatch '+dev['device_id'])
    for row in dev['rows']:
        for field in ['evidence','solidity','gap','next_route','query','query_status']:
            if not row.get(field):errors.append('Empty '+field+' '+dev['device_id']+' '+row['requirement_id'])
        if '→' not in row['evidence']:errors.append('No explicit contribution '+dev['device_id']+' '+row['requirement_id'])
        if row['source_ids'] and not row.get('locator'):errors.append('Source has no locator')
        if any(s not in sources for s in row['source_ids']):errors.append('Unknown source ID')
        if row['next_route'] not in routes:errors.append('Unknown Imperial/official route')
        if '('+row['requirement_id']+')' not in text:errors.append('Question missing in rendered file')
        point=points.get(row['requirement_id'],{})
        for field in ['found','use','missing']:
            if not point.get(field):errors.append('Missing readable '+field+' '+dev['device_id']+' '+row['requirement_id'])
        for sid in row['source_ids']:
            catalog=next(s for s in load('data/source-catalog.json') if s['id']==sid)
            if catalog['url'] not in text:errors.append('Original source link lost '+sid)
    for heading in [s['name'] for s in d['sections']]:
        if '\n## '+heading+'\n' not in text:errors.append('Topic missing in readable guide')
    for label in ['What the report needs to explain','What the sources actually tell us','What this lets us write','What we cannot yet answer','Next investigation']:
        if text.count('- **'+label+':**')!=31:errors.append('Five explanations missing '+dev['device_id']+' '+label)
for p in [ROOT/'README.md',*(ROOT/'research').glob('*.md')]:
    content=p.read_text(encoding='utf-8')
    if re.search(r'^\|.*\|\s*$',content,re.M):errors.append('Table remains in requested reading path: '+p.name)
overview=(ROOT/'research/README.md').read_text(encoding='utf-8')
if [line for line in overview.splitlines() if line.startswith('## ')]!=['## '+dev['name'] for dev in d['devices']]:errors.append('Overview must be organised by device')
for rec in load('data/checklist-preservation.json')['files']:
    if hashlib.sha256((ROOT/rec['path']).read_bytes()).hexdigest()!=rec['sha256']:errors.append('Prior evidence changed '+rec['path'])
if len(d['reviews'])!=1 or d['reviews'][0]['source_id']!='RNS-ECON-PUBLISHER':errors.append('Deeper-review scope mismatch')
for a in d['access_attempts']:
    if not all(a.get(k) for k in ['query','outcome','meaning','date']):errors.append('Incomplete access attempt')
result=dict(status='FAIL' if errors else 'PASS',devices=len(d['devices']),requirements_per_device=len(reqs),explicit_rows=sum(len(x['rows']) for x in d['devices']),preserved_files=len(load('data/checklist-preservation.json')['files']),readme_words=len((ROOT/'README.md').read_text(encoding='utf-8').split()),errors=errors,limit='Structural/source-pointer and preservation checks; claim-support judgements require the recorded source reading, not this script.')
print(json.dumps(result,indent=2));sys.exit(bool(errors))
