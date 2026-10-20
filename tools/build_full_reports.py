"""Render the six authored case studies, visible reference lists and comparison."""
from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/full-reports.json').read_text(encoding='utf-8'))
SOURCES={s['id']:s for s in json.loads((ROOT/'data/source-catalog.json').read_text(encoding='utf-8'))}
def write(p,t):
    dest=ROOT/p;dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(t.strip()+'\n',encoding='utf-8')
def word_count(t):return len(t.split())
manifest=[]
for n,r in enumerate(DATA['reports'],1):
    used=[]
    def cite(m):
        sid=m.group(1)
        if sid not in SOURCES:raise ValueError('Unknown citation: '+sid)
        if sid not in used:used.append(sid)
        return '['+str(used.index(sid)+1)+']'
    body=re.sub(r'\[@([A-Z0-9-]+)\]',cite,r['body_markdown'])
    header=f'''# {r['device_name']}: {r['title']}

**AI-generated reference draft for selection and discussion. Not an assessed submission.** No interviews or original clinical data are claimed. Evidence cutoff: {DATA['updated']}.

[Research notes and preserved layers](../{n:02d}-{r['device_id']}.md) · [All six drafts](../../reports/README.md) · [Comparative review](../../reports/comparative-review.md)

**Scope:** {r['scope']}.

**Word count:** WORDCOUNT_PLACEHOLDER, including references, tables, diagram and notices (whitespace count; verify in submission software).

'''
    refs='\n\n## References\n\nSource identities and URLs are printed for retrieval without relying on embedded hyperlinks. Dates/coverage reflect the source records; deeper drafting checks are recorded separately in [the evidence log](../../data/full-report-evidence.json).\n\n'
    for i,sid in enumerate(used,1):
        s=SOURCES[sid]
        details=DATA.get('reference_details',{}).get(sid,{})
        date=details.get('date') or s['source_date'] or 'n.d.'
        title=details.get('title') or s['title']
        refs+=f'{i}. {title}. {date}. {s["url"]} (review record: {s["checked"]}).\n\n'
    notes='\n\n**Preparation note:** The specification/examples guided structure and source use; [method and limitations](../../docs/full-report-writing-method.md). No invented author responsibilities, interview accounts or policy-compliance declaration are included.\n'
    text=header+body.strip()+notes+refs
    count=word_count(text)
    text=text.replace('WORDCOUNT_PLACEHOLDER',f'{count:,}')
    dest=f'devices/{r["device_id"]}/full-report.md'
    write(dest,text)
    final=(ROOT/dest).read_text(encoding='utf-8')
    manifest.append(dict(device_id=r['device_id'],path=dest,total_words=word_count(final),narrative_words=word_count(body),
                         references=len(used),source_ids=used,selected_patent=r['patent_source'],independent_claims=r['independent_claims'],sha256=hashlib.sha256(final.encode()).hexdigest()))
write('reports/comparative-review.md',DATA['comparative_review_markdown'])
write('docs/full-report-writing-method.md',DATA['writing_method_markdown'])
index='''# Six full case-study reference drafts

These drafts turn the preserved research into complete narratives across the five course topics. They are AI-generated reference documents for selection/discussion, not assessed submissions. Each includes an executive summary, product scope, five sections, independent-claim explanations, an analytical stakeholder map, conclusion and numbered retrievable references. Evidence gaps remain visible.

Start with the [comparative review](comparative-review.md) for strengths, weaknesses, the actual writing difficulties and the most useful next investigations. See [how the module materials and examples guided writing](../docs/full-report-writing-method.md).

| Device | Full draft | Words including references | References | Original research |
|---|---|---:|---:|---|
'''
for n,(r,m) in enumerate(zip(DATA['reports'],manifest),1):
    index+=f'| {r["device_name"]} | [Read](../{m["path"]}) | {m["total_words"]:,} | {m["references"]} | [Preserved notes](../devices/{n:02d}-{r["device_id"]}.md) |\n'
index+='''
The word counts include Markdown notices, references, tables and diagram syntax, using whitespace-separated tokens. They are a working check, not a guarantee of the count from Word/Turnitin. All drafts retain substantial margin below the 4,000-word limit.

The comparison concerns report completeness and research difficulty, not clinical superiority. Counts of words or references are not quality scores. The exact lecture stakeholder-map format, genuine group contributions and any permitted final submission process remain separate requirements.

[Return to repository overview](../README.md).
'''
write('reports/README.md',index)
write('data/full-report-manifest.json',json.dumps(dict(updated=DATA['updated'],count_method='Whitespace-separated tokens in the complete generated Markdown, including references and notices',reports=manifest),indent=2))
if __name__=='__main__':
    print(json.dumps(dict(reports=len(manifest),word_counts={r['device_id']:r['total_words'] for r in manifest},references={r['device_id']:r['references'] for r in manifest}),indent=2))
