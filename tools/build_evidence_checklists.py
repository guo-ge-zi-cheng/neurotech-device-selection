"""Render the requirement-to-evidence view; retain historical research and full drafts."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/evidence-checklists.json').read_text(encoding='utf-8'))
SOURCES={x['id']:x for x in json.loads((ROOT/'data/source-catalog.json').read_text(encoding='utf-8'))}
REQS={r['id']:r for s in DATA['sections'] for r in s['requirements']}
ROUTES={r['id']:r for r in DATA['routes']}
def write(p,t):
    path=ROOT/p;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(t.strip()+'\n',encoding='utf-8')
def cell(t):return str(t).replace('|',' / ').replace('\n',' ')
def route_link(key,base='../docs/'):
    return f'[{key}]({base}imperial-gap-searches.md#{key.lower()})'
def evidence_text(row,used):
    refs=[]
    for sid in row['source_ids']:
        if sid not in used:used.append(sid)
        refs.append(f'[{used.index(sid)+1}]({SOURCES[sid]["url"]})')
    passage=f'<br>Passage: {row["locator"]}.' if row['locator'] else ''
    return row['evidence']+(' '+', '.join(refs) if refs else '')+passage
legend='**Strength is claim-specific:** Direct = an appropriate original record/study for the stated fact; Limited = important design/scope limits; Partial = only part answered; Model = conditional analysis; Indirect/Context = background; Mismatch = evidence concerns the wrong product/period; Missing = no accepted answer; Inference/Provisional = our analysis. A direct source can still leave fields missing.'
paths={d['device_id']:f'research/{d["device_id"]}.md' for d in DATA['devices']}
for d in DATA['devices']:
    used=[];rows={r['requirement_id']:r for r in d['rows']}
    text=f'''# {d['name']}: evidence checklist

**Scope:** {d['scope']}

Matched to the supplied guide on {DATA['updated']}. [Overall comparison](README.md) · [All required elements](../docs/report-evidence-requirements.md) · [Imperial search outcomes](../docs/imperial-gap-searches.md).

{legend}

'''
    for s in DATA['sections']:
        text+=f'''## {s['name']}

Guide physical PDF pp{s['guide_pages']}. Each required element is one row. “Next step” is a proposal, not evidence already retrieved; route codes link to actual access outcomes.

| What this section must include | Exact evidence → contribution | How solid? | Exactly missing | Imperial / next step |
|---|---|---|---|---|
'''
        for q in s['requirements']:
            r=rows[q['id']]
            # Spaces around slash-separated alternatives allow GitHub tables to wrap.
            need=f'**{q["id"]}: {q["label"]}.**<br>'+q['fields'].replace('/',' / ')
            next_step=f'{route_link(r["next_route"])}<br>Search: {r["query"]}'
            text+='| '+' | '.join(map(cell,[need,evidence_text(r,used),r['solidity'],r['gap'],next_step]))+' |\n'
        text+='\n'
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

There are **31 elements per device**: six in each topic, plus the stakeholder map. Every [device checklist](../research/README.md) has the same elements and five fields: requirement, exact source content/contribution, strength, exact gap, and next source/access action. The overall comparison highlights selected evidence; it is not a substitute for these 31 rows.

'''
for s in DATA['sections']:
    t+=f'## {s["name"]}\n\nGuide physical PDF pp{s["guide_pages"]}.\n\n| ID | Element | Evidence needed |\n|---|---|---|\n'
    for r in s['requirements']:t+=f'| {r["id"]} | {r["label"]} | {r["fields"]} |\n'
    t+='\n'
t+='''## Interpret the result

Read the exact evidence and its scope before the strength label. A source can directly establish a regulatory decision while leaving current labels unresolved. An economic model can answer an analytical question while leaving actual prices unknown. A wrong-period patent or implant-programme funding record is marked as a mismatch rather than counted as support.

Unknown is not the same as false or undisclosed. A proposed query is not a completed search. Database access does not create missing private facts, and an additional source does not automatically close a gap. [Reliability protocol](reliability-protocol.md).
'''
write('docs/report-evidence-requirements.md',t)

t='''# Imperial resources matched to the gaps

Checked 21 October 2026. These routes explain the final column in every [checklist](../research/README.md). Each query there is proposed unless the outcomes below explicitly record it as completed. Institutional listings are not proof that a particular device fact is available.

## What actually happened

| Route tried | Query/action | Actual outcome | What changes in the evidence? |
|---|---|---|---|
'''
for a in DATA['access_attempts']:t+='| '+' | '.join(map(cell,[a['route'],a['query'],a['outcome'],a['meaning']]))+' |\n'
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

- For a weak finance row, first recover an attributable old transaction or award. A recent-only deal collection or a whole-company R&D total will not answer original development finance.
- For a model/effect row, retrieve the original full paper and its methods. The RNS access test demonstrates that Imperial can add detail beyond an abstract.
- For an unknown price or capacity row, look for a contract or actual service record. A library subscription cannot substitute for a quotation or a conversation that has not happened.
- For an IP row, use the correct original family and official status/assignment records. A licence to a database does not complete legal/product mapping.
- For the stakeholder-format row, retrieve the actual lecture instruction. Existing diagrams remain provisional.

The broader [Imperial directory](imperial-resources.md) and [general source collection](information-resources.md) remain useful discovery tools. The narrower actions above exist to close a named requirement, rather than increase the source count.
'''
write('docs/imperial-gap-searches.md',t)

t=f'''# Evidence available for the seven device reports

This is the current information-research comparison, matched to the supplied guide on {DATA['updated']}. Start with the [31 common required elements](../docs/report-evidence-requirements.md). Open a device for every element's source content, direct contribution, strength, exact gap and next action.

{legend}

The tables below highlight one informative evidence match per device/topic; **the linked device files contain all 31 rows**. Source checks originally date to 19–20 October unless the [new access/review log](../docs/imperial-gap-searches.md) states otherwise. No total richness/readiness score is calculated.

'''
for s in DATA['sections']:
    sid=s['id']
    t+=f'## {s["name"]}\n\n**Included:** '+'; '.join(f'{r["id"]} {r["label"].lower()}' for r in s['requirements'])+'.\n\n'
    t+='| Device | Exact evidence → matched need | How solid? | Exactly missing | Imperial / next action |\n|---|---|---|---|---|\n'
    for d in DATA['devices']:
        v=d['overview'][sid];r=next(x for x in d['rows'] if x['requirement_id']==v['focus'])
        refs=' '.join(f'[source {n}]({SOURCES[x]["url"]})' for n,x in enumerate(r['source_ids'],1))
        evidence=f'**{r["requirement_id"]}:** {r["evidence"]} '+refs
        t+='| '+' | '.join(map(cell,[f'[{d["name"]}]({d["device_id"]}.md#{s["name"].lower().replace(" ","-")})',evidence,r['solidity'],v['gap'],v['next']]))+' |\n'
    t+='\n'
t+='''The precise source locators, remaining subquestions and proposed search strings are in each device checklist. [Imperial route codes and actual outcomes](../docs/imperial-gap-searches.md) distinguish a successful full-text retrieval from a resource that is only listed or inaccessible for this use. The earlier [narrative-draft review](../reports/comparative-review.md) assesses dated drafts; it is not the current source-to-need comparison.
'''
write('research/README.md',t)

desc={'precision':'Temporary cortical electrode for recording/monitoring/stimulation.','rns':'Implanted closed-loop recording and seizure stimulation.','ceribell':'Rapid scalp EEG in acute care, with version-specific software.','saint':'MRI-informed accelerated TMS treatment pathway.','exablate':'MR-guided focused-ultrasound thermal lesion treatment.','arcex':'External spinal stimulation with functional rehabilitation.','terra':'7T MRI for defined head/extremity imaging uses.'}
t='''# Choosing a device through evidence

**Start with the [requirement-to-source comparison](research/README.md).** It replaces broad comments about “information richness” with explicit matches to the supplied report guide.

Each device checklist has the same **31 required elements** across unmet medical need, IP, fundraising, regulation and reimbursement. Every row shows five things:

1. What the section needs.
2. Exact source content and how it answers that need.
3. How solid that particular support is.
4. Exactly what is still missing.
5. The next Imperial or official source/action to try.

| Device | What it does | Current evidence checklist |
|---|---|---|
'''
for d in DATA['devices']:t+=f'| {d["name"]} | {desc[d["device_id"]]} | [Open]({paths[d["device_id"]]}) |\n'
t+='''
The [common requirements](docs/report-evidence-requirements.md) come from the supplied guide's evidence tables, with page provenance. The [Imperial access/search log](docs/imperial-gap-searches.md) records what was actually tried. One concrete improvement is full access to the RNS economic paper; its cost inputs remain a historical model, rather than a current device quote. Proposed searches are labelled and do not count as evidence found.

Use the [general information resources](docs/information-resources.md) and [Imperial resource directory](docs/imperial-resources.md) to locate databases. Use the checklist's exact missing field and query to decide what to retrieve. A subscription does not guarantee a private valuation, original budget or hospital contract.

Earlier material is retained: [original research layers](devices/README.md), [full narrative reference drafts](reports/README.md), [dated narrative-draft comparison](reports/comparative-review.md), [source dates/coverage](docs/sources.md), and [course requirements](docs/course-requirements.md). The new checklists are the main path for judging available information. They do not rank clinical superiority, claim interviews, or certify assessed-work compliance.
'''
write('README.md',t)
