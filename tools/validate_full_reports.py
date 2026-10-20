"""Validate report budgets, citations, scope and preservation; not clinical/legal truth."""
from pathlib import Path
import json,re,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
data=load('data/full-reports.json');manifest=load('data/full-report-manifest.json')
sources=load('data/source-catalog.json');source_ids={s['id'] for s in sources}
expected=['precision','rns','ceribell','saint','exablate','arcex','terra'];errors=[]
if [r['device_id'] for r in data['reports']]!=expected:errors.append('Seven full reports required')
if [r['device_id'] for r in manifest['reports']]!=expected:errors.append('Manifest scope mismatch')
claims_expected={'precision':[1,5,13,17],'rns':[1,46],'ceribell':[1,18,20,26],'saint':[1,10,19,24],'exablate':[1,11,21,26],'arcex':[1],'terra':[1,12]}
for r,m in zip(data['reports'],manifest['reports']):
    p=ROOT/m['path'];text=p.read_text(encoding='utf-8');body,refs=text.split('## References',1)
    count=len(text.split())
    if count!=m['total_words'] or count>4000:errors.append('Word budget/count mismatch: '+r['device_id'])
    if hashlib.sha256(text.encode()).hexdigest()!=m['sha256']:errors.append('Draft/manifest content mismatch: '+r['device_id'])
    if 'AI-generated reference draft' not in text:errors.append('Missing provenance: '+r['device_id'])
    for n,topic in enumerate(['Unmet medical need','Intellectual property','Fundraising','Regulatory','Reimbursement'],1):
        if not re.search(r'^## '+str(n)+r'\. '+re.escape(topic),body,re.M):errors.append('Missing topic: '+r['device_id']+' '+topic)
    if '```mermaid' not in body or '*Figure 1.' not in body:errors.append('Missing stakeholder diagram/caption: '+r['device_id'])
    if r['independent_claims']!=claims_expected[r['device_id']]:errors.append('Selected independent-claim coverage mismatch')
    for claim in claims_expected[r['device_id']]:
        if f'| {claim} |' not in body:errors.append('Independent claim explanation absent: '+r['device_id']+' '+str(claim))
    used={int(x) for x in re.findall(r'\[(\d+)\]',body)}
    defined={int(x) for x in re.findall(r'^(\d+)\. ',refs,re.M)}
    if used!=defined or defined!=set(range(1,m['references']+1)):errors.append('Citation/reference mismatch: '+r['device_id'])
    if '[@' in text:errors.append('Unresolved citation marker: '+r['device_id'])
    if any(k not in source_ids for k in m['source_ids']):errors.append('Unknown report source')
    if any(s['url'] not in refs for s in sources if s['id'] in m['source_ids']):errors.append('Reference has no retrievable URL: '+r['device_id'])
preservation=load('data/research-preservation.json')
for record in preservation['files']:
    content=(ROOT/record['path']).read_bytes()
    if record['mode']=='exact':checked=content
    elif record['mode']=='prefix':checked=content[:record['bytes']]
    elif record['mode']=='json_prefix':checked=json.dumps(load(record['path'])[:record['entries']],sort_keys=True,ensure_ascii=False).encode()
    elif record['mode']=='json_devices_prefix':
        a=load(record['path'])
        checked=json.dumps(a['devices'][:record['entries']],sort_keys=True,ensure_ascii=False).encode()
        if any(a[k]!=v for k,v in record['preserved_metadata'].items()):errors.append('Prior research metadata changed')
        if a['leads_not_accepted'][:len(record['original_leads'])]!=record['original_leads']:errors.append('Prior search leads changed')
    else:raise ValueError('Unknown preservation mode')
    if hashlib.sha256(checked).hexdigest()!=record['sha256']:errors.append('Prior research changed: '+record['path'])
prefix=sources[:preservation['source_entries']]
if hashlib.sha256(json.dumps(prefix,sort_keys=True,ensure_ascii=False).encode()).hexdigest()!=preservation['source_catalog_prefix_sha256']:errors.append('Original source catalog records changed')
old_bodies=[r['body_markdown'] for r in data['reports'][:preservation['full_report_body_entries']]]
if hashlib.sha256(json.dumps(old_bodies,ensure_ascii=False).encode()).hexdigest()!=preservation['full_report_body_prefix_sha256']:errors.append('Original six narrative bodies changed')
if 'later' not in data['reports'][-1]['patent_scope'].lower():errors.append('Terra patent scope boundary missing')
for review in load('data/full-report-evidence.json')['reviews']:
    if review['source_id'] not in source_ids:errors.append('Unknown rechecked source')
result=dict(status='PASS' if not errors else 'FAIL',full_reports=len(manifest['reports']),word_limit=4000,
 word_counts={r['device_id']:r['total_words'] for r in manifest['reports']},
 independent_claims_explained=sum(len(r['independent_claims']) for r in data['reports']),
 preserved_research_files=len(preservation['files']),preserved_source_records=preservation['source_entries'],errors=errors,
 limit='Structural and preservation checks; no independent examiner grade, legal opinion, interview or clinical/payer audit.')
print(json.dumps(result,indent=2));sys.exit(bool(errors))
