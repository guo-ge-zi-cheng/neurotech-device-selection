"""Render the requirement-to-evidence view; retain historical research and full drafts."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/evidence-checklists.json').read_text(encoding='utf-8'))
READING=json.loads((ROOT/'data/research-explanations.json').read_text(encoding='utf-8'))
QUESTIONS={q['id']:q for q in READING['requirements']}
EXPLANATIONS={d['device_id']:d for d in READING['devices']}
SOURCES={x['id']:x for x in json.loads((ROOT/'data/source-catalog.json').read_text(encoding='utf-8'))}
REQS={r['id']:r for s in DATA['sections'] for r in s['requirements']}
ROUTES={r['id']:r for r in DATA['routes']}
def write(p,t):
    path=ROOT/p;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(t.strip()+'\n',encoding='utf-8')
def cell(t):return str(t).replace('|',' / ').replace('\n',' ')
def route_link(key,base='../docs/'):
    return f'[{key}]({base}imperial-gap-searches.md#{key.lower()})'
def evidence_sources(row,used):
    refs=[]
    for sid in row['source_ids']:
        if sid not in used:used.append(sid)
        refs.append(f'[{SOURCES[sid]["title"]}]({SOURCES[sid]["url"]})')
    if not refs:return ''
    return ' Source: '+'; '.join(refs)+'. Relevant passage: '+row['locator'].rstrip('.')+'.'
paths={d['device_id']:f'research/{d["device_id"]}.md' for d in DATA['devices']}
for d in DATA['devices']:
    used=[];rows={r['requirement_id']:r for r in d['rows']}
    readable=EXPLANATIONS[d['device_id']]
    points={p['requirement_id']:p for p in readable['points']}
    text=f'''# {d['name']}: what we can write, and what is missing

{readable['summary']}

This guide works through the five report sections for a teammate deciding what investigation is still needed. Each question explains the requirement, the actual evidence, the conclusion it supports, the unanswered part and a way to investigate it. Evidence limitations are explained in sentences rather than assigned a grade.

[Device-by-device overview](README.md) · [The shared requirements](../docs/report-evidence-requirements.md) · [What Imperial access actually recovered](../docs/imperial-gap-searches.md).

The evidence comes from the existing 19–21 October research. This revision clarifies that evidence; it adds no new retrievals. The next investigations below are proposals unless the access log explicitly records otherwise.

'''
    for s in DATA['sections']:
        text+=f'## {s["name"]}\n\n'
        for q in s['requirements']:
            r=rows[q['id']];question=QUESTIONS[q['id']];p=points[q['id']]
            route=ROUTES[r['next_route']]
            route_text=f'[{route["name"]}](../docs/imperial-gap-searches.md#{r["next_route"].lower()})'
            text+=f'''### {question['question']} ({q['id']})

- **What the report needs to explain:** {question['need']}
- **What the sources actually tell us:** {p['found']}{evidence_sources(r,used)}
- **What this lets us write:** {p['use']}
- **What we cannot yet answer:** {p['missing']}
- **Next investigation:** {question['next_step']} Start with {route_text}; the linked access log states what was actually tried and any access limits.

'''
    text+='''<details>
<summary>Source identities and actual review scope</summary>

Evidence was matched against the repo's existing studies, source records and full drafts on 21 October. Earlier source checks retain their dates; this is not a fresh full-source/current-label/payer audit. The original studies are [retained](../devices/README.md). No interview or visit has occurred. The source catalog's earlier coverage is not silently upgraded by a proposed subscription search.

'''
    for i,sid in enumerate(used,1):
        src=SOURCES[sid]
        text+=f'{i}. **{sid}: {src["title"]}.** {src["source_date"] or "Date in original record"}. {src["url"]} — checked {src["checked"]}; {src["review_coverage"]}\n\n'
    if d['device_id']=='rns':
        text+='**New Imperial review, 21 October:** the existing economic paper was opened in full through the library; methods 2.1/2.2/2.6, Table 1 and limitations 4.1 were read. This deepens the same paper rather than provides independent corroboration. [Review record](../data/evidence-checklists.json).\n\n'
    text+='The supplied guide defines this working checklist. Project spec remains the authority for assessment. Original course/guide PDFs and licensed exports are not redistributed. These are research preparation notes.\n\n</details>\n'
    write(paths[d['device_id']],text)

# One common requirements list fixes the denominator; no hidden or device-dependent criteria.
t='''# Required evidence: the common checklist

Derived from the team's supplied Medical_Device_Report_Guide.pdf, sections 3–7, on 21 October 2026. This is the team's working decomposition; it does not replace Project spec or create a new grading rubric. The PDF remains outside the public repo. Its identity and review scope are recorded in [structured data](../data/evidence-checklists.json).

There are **31 questions per device**: six in each topic, plus the stakeholder map. Every [device research guide](../research/README.md) explains each requirement in full sentences, then distinguishes evidence, what it supports, what remains unanswered and the next investigation. No scale or grade replaces that explanation.

'''
for s in DATA['sections']:
    t+=f'## {s["name"]}\n\nGuide physical PDF pp{s["guide_pages"]}.\n\n'
    for r in s['requirements']:
        q=QUESTIONS[r['id']]
        t+=f'- **{q["question"]} ({r["id"]})** {q["need"]}\n\n'
    t+='\n'
t+='''## Interpret the result

Read what a source establishes and then the specific question it leaves unanswered. A regulatory decision can establish original market entry while leaving later labels unresolved. An economic model can show the authors' assumptions while leaving actual prices unknown. A later patent or another product's funding cannot fill an original-device gap.

Unknown is not the same as false or undisclosed. A proposed query is not a completed search. Database access does not create missing private facts, and an additional source does not automatically close a gap. [Reliability protocol](reliability-protocol.md).
'''
write('docs/report-evidence-requirements.md',t)

t='''# Imperial resources matched to the gaps

Checked 21 October 2026. These routes support the next-investigation bullets in every [device guide](../research/README.md). Proposed search strings are retained in the structured evidence record; only the outcomes below count as completed access attempts. Institutional listings are not proof that a particular device fact is available.

## What actually happened

| Route tried | Query/action | Actual outcome | What changes in the evidence? |
|---|---|---|---|
'''
for a in DATA['access_attempts']:
    query='Search strings retained in data/evidence-checklists.json' if a['id']=='IC-OTHER' else a['query']
    t+='| '+' | '.join(map(cell,[a['route'],query,a['outcome'],a['meaning']]))+' |\n'
t+='''
The RNS paper's public identity is [Youngerman et al., DOI 10.1111/epi.17049](https://doi.org/10.1111/epi.17049). Its library record offered an institutional Wiley service and the article displayed full access. The new review supplies historical model inputs/limitations; it does not establish a present hospital purchase or NHS price. No personal account details, authentication/session URLs, raw licensed exports or article copies are published.

The PitchBook route was left at its terms page without accepting the agreement or using subscriber data. Factiva's catalog restriction is kept visible. Ask the library about permitted use rather than passing restricted exports into an AI tool. This is an observed access boundary, not a finding that the databases lack relevant company records.

## Route codes and the exact output needed

'''
for r in DATA['routes']:
    t+=f'''### {r['id']}

**{r['name']}:** {r['offers']} [Official starting point]({r['url']}).

**Actual status:** {r['status']}

**Retrieve:** {r['output']}

**Limit:** {r['limit']}

'''
t+='''## Best use of a student's next hour

- For a missing finance answer, first recover an attributable old transaction or award. A recent-only deal collection or a whole-company R&D total will not answer original development finance.
- For an economic model or clinical-effect question, retrieve the original full paper and its methods. The RNS access test demonstrates that Imperial can add detail beyond an abstract.
- For an unknown price or capacity, look for a contract or actual service record. A library subscription cannot substitute for a quotation or a conversation that has not happened.
- For an IP question, use the correct original family and official status/assignment records. A licence to a database does not complete legal/product mapping.
- For the stakeholder format, retrieve the actual lecture instruction. Existing diagrams remain provisional.

The broader [Imperial directory](imperial-resources.md) and [general source collection](information-resources.md) remain useful discovery tools. The narrower actions above exist to close a named requirement, rather than increase the source count.
'''
write('docs/imperial-gap-searches.md',t)

t=f'''# Seven devices: what the evidence lets us write

This page is for teammates choosing a report case. Each device starts with a paragraph explaining what it does and where its investigation stands. The five bullets then explain what the available material contributes to each report section and what we still need to find. Open the detailed guide for the requirement-by-requirement reasoning.

All seven use the same [31 questions from the supplied guide](../docs/report-evidence-requirements.md). This is a rewrite of evidence reviewed on 19–21 October, not a new source audit. [The Imperial access log](../docs/imperial-gap-searches.md) separates completed retrievals from proposed searches.

'''
for d in DATA['devices']:
    readable=EXPLANATIONS[d['device_id']]
    t+=f'## {d["name"]}\n\n{readable["summary"]}\n\n'
    for s in DATA['sections']:
        anchor=s['name'].lower().replace(' ','-')
        t+=f'- **{s["name"]}:** {readable["overview"][s["id"]]} [Sources and unanswered questions]({d["device_id"]}.md#{anchor}).\n\n'
    t+=f'[Read the complete evidence guide]({d["device_id"]}.md).\n\n'
t+='''The detailed guides retain source links and passages and explain why a missing answer matters. Original search strings remain in the [structured evidence record](../data/evidence-checklists.json). The earlier [narrative-draft review](../reports/comparative-review.md) assesses dated drafts; use the guides above for the current explanation of evidence gaps.
'''
write('research/README.md',t)

t='''# Choosing a device through evidence

**Start with the [device-by-device research overview](research/README.md).** Each device below has a plain-language guide explaining what its sources let us write and exactly what is still missing.

The guides address unmet medical need, intellectual property, fundraising, regulation and reimbursement. Each uses the same 31 questions from the supplied report guide. Answers are written as bullet lists: the requirement, the source content, its contribution and limits, the unanswered question and the next investigation. There are no evidence grades or comparison tables in this reading path.

'''
for d in DATA['devices']:
    t+=f'## {d["name"]}\n\n{EXPLANATIONS[d["device_id"]]["summary"]} [Read the evidence guide]({paths[d["device_id"]]}).\n\n'
t+='''
The [common requirements](docs/report-evidence-requirements.md) come from the supplied guide's evidence tables, with page provenance. The [Imperial access/search log](docs/imperial-gap-searches.md) records what was actually tried. One concrete improvement is full access to the RNS economic paper; its cost inputs remain a historical model, rather than a current device quote. Proposed searches are labelled and do not count as evidence found.

Use the [general information resources](docs/information-resources.md) and [Imperial resource directory](docs/imperial-resources.md) to locate databases. Use the checklist's exact missing field and query to decide what to retrieve. A subscription does not guarantee a private valuation, original budget or hospital contract.

Earlier material is retained: [original research layers](devices/README.md), [full narrative reference drafts](reports/README.md), [dated narrative-draft comparison](reports/comparative-review.md), [source dates/coverage](docs/sources.md), and [course requirements](docs/course-requirements.md). The new checklists are the main path for judging available information. They do not rank clinical superiority, claim interviews, or certify assessed-work compliance.
'''
write('README.md',t)
