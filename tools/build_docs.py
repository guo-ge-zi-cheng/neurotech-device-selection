from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/device-records.json').read_text(encoding='utf-8'))
S=json.loads((ROOT/'data/source-catalog.json').read_text(encoding='utf-8'))
LOOKUP={s['id']:s for s in S}
CURATION={c['device_id']:c for c in json.loads((ROOT/'data/screening-matrix.json').read_text(encoding='utf-8'))}
def write(path,text):
    (ROOT/path).write_text(text.strip()+'\n',encoding='utf-8')
def dump(path,x): write(path,json.dumps(x,ensure_ascii=False,indent=2))
def report_path(d): return f'devices/{d["number"]:02d}-{d["id"]}.md'
def citation(keys): return ' '.join(f'[{k}][{k}]' for k in keys)
labels={'S':'Strong starting evidence','P':'Partial / follow-up needed','G':'Material gap'}
topic_labels=['Clinical need and evidence','IP and invention origin','Early funding','Regulatory path and manufacturing','Reimbursement and health economics']

dimensions=[
('Product scope and technical fit','What exactly is marketed, and does it record, stimulate, image, ablate, triage or diagnose?','Prevents future ambitions or related products from being treated as the selected device; connects the choice to the team’s neurotechnology interests.'),
('Clinical need and evidence','A bounded patient group, comparator, original studies, endpoints and limitations.','A convincing need section requires more than a large disease market or a headline accuracy figure.'),
('IP and invention origin','Original inventors and employers, assignments/licences, patent families and independent claims.','The assignment concerns early development; current company ownership or a patent count cannot explain how the invention arose.'),
('Early funding','Academic grants, seed/early company capital, dates, investors, valuations where disclosed, and attributable costs.','Late growth funding and parent-company R&D cannot be substituted for the original device’s financing.'),
('Regulatory path and manufacturing','Exact version, indication, jurisdiction, evidence pathway, production and outsourcing.','Authorization attaches to a defined product/use. Software deployment also needs a quality/production account.'),
('Reimbursement and economics','Who buys and pays, in which setting, eligibility, relevant policy and economic assumptions.','Clinical usefulness does not ensure a viable payment pathway; US, NHS, private and trial access differ.'),
('Public information accessibility','Usable primary records, accessible text, source dates, commercial provenance and unresolved gaps.','The team needs a report it can finish even if nobody agrees to an interview. Source availability is different from evidence quality.'),
('London/UK first-hand access','Exact product/site or clinician, founder-origin lead, domain expert, or remote-only route.','A concrete nearby route can improve the case, but proximity and a public email do not establish product experience or visit permission.')]

readme='''# Neurotechnology Device Selection

An evidence-led comparison of nine medical devices for an engineering entrepreneurship case study. It is written for a London-based biomedical engineering team choosing one topic: the aim is to identify a device that is interesting **and** has enough accessible evidence to support a complete case.

This repository has two reading levels: this README explains the screening dimensions and compares the results; `devices/` contains a separate, more detailed report for each device under the same dimensions. Research was checked on **19 October 2026** and reorganized for GitHub on **20 October 2026**. Reorganization is not a new verification of clinical status or contacts.

## TL;DR — the practical takeaway

- **Start with Exablate Neuro, Optune Gio and RNS.** Exablate offers the best balance of documented London clinical use and a specific UK commissioning pathway. Optune has a direct Imperial product-user lead and a rich commercialization history. RNS best matches neural recording and closed-loop stimulation, with substantial public evidence.
- **Choose MAGNETOM Terra if exact local equipment access is the priority**, while accepting harder early funding/IP attribution. **Choose Viz LVO if a founder-origin conversation is the priority**; a London co-founder is verified, but local clinical deployment is not.
- **Ceribell and SAINT are credible interest-led alternatives.** Both require careful product/version boundaries; exact-product London access is unverified in this search.
- **Precision and Canvas Dx need more gap-closing before becoming easy choices.** Precision has a marketed temporary electrode component distinct from its broader BCI ambition. Canvas Dx offers an interesting diagnostic-AI case, but indeterminate results, product-specific IP and actual payer coverage need particular care.

This is a **research-feasibility shortlist**, not a clinical ranking, recommendation for treatment, or final group allocation. Follow the linked reports for the evidence and the limits of each judgement.

## 1. Screening dimensions — what we checked and why

The five assessed content topics are clinical need, IP, funding, regulation and reimbursement. We added product scope, information accessibility and London access because they determine whether the team can research those topics accurately and on time. Writing quality is a separate assignment requirement; it is not an extra device score.

| Dimension | What we checked | Why it matters |
|---|---|---|
'''
readme+=''.join(f'| {a} | {b} | {c} |\n' for a,b,c in dimensions)
readme+='''
### How to read the results

**S = strong starting evidence:** substantive usable primary material or a specific policy was located. **P = partial:** there are concrete sources or leads, but important attribution, scope or interpretation work remains. **G = material gap:** a selection-critical answer remains unresolved in this bounded search. These grades are research-readiness judgements, not numerical scores, completed due diligence, or judgements of clinical effectiveness. An unverified fact is not evidence that something does not exist.

There is no weighted total: a team prioritizing BCI may prefer RNS to a device with easier local access, while a team prioritizing an in-person equipment discussion may prefer Terra. The eventual case must still address all five assessed topics.

## 2. Results across the nine devices

### Technical fit and public information

| Device and detailed report | What the technology does | Public-source accessibility |
|---|---|---|
'''
for d in D:
    c=CURATION[d['id']]
    readme+=f'| [{d["name"]}]({report_path(d)}) — {d["company"]} | {c["fit"]} | {d["desk"]} |\n'
readme+='''
### Readiness for the five coursework topics

| Device | Clinical need / evidence | IP / origin | Early funding | Regulation / manufacturing | Reimbursement / economics |
|---|---|---|---|---|---|
'''
for d in D:
    readme+='| ['+d['name']+']('+report_path(d)+') | '+' | '.join(CURATION[d['id']]['grades'])+' |\n'
readme+='''
Every device has an original FDA record in the source catalog. Regulation remains **P** because that alone does not complete the current indication, relevant UK/EU markets, manufacturing and outsourcing work. No device has a completed independent-patent-claim map in this repository.

### London access and likely workload

| Device | Verified local or remote access state | Relative research workload | Decision implication |
|---|---|---|---|
'''
for d in D:
    c=CURATION[d['id']]
    readme+=f'| [{d["name"]}]({report_path(d)}) | {c["access"]} | {d["difficulty"]} | {c["short"]} |\n'
readme+='''
The strongest local starting points are the UCLH/NHNN functional neurosurgery team for Exablate, Dr Matthew Williams at Imperial for Optune, and the King’s LoCUS facility for Terra. Manoj Ramachandran is a London Viz.ai co-founder, with a distinct business/origin perspective. Other named London experts are labelled as domain experts where exact-product experience was not verified. **No outreach has been sent; no interview or visit has been arranged.**

## Detailed reports and supporting material

Each device report explains the mechanism and clinical evidence, gives a reason for every readiness grade, identifies a public first-hand enquiry route, and sets out the gaps that should be closed before choosing it.

'''
readme+=''.join(f'{d["number"]}. [{d["company"]} — {d["name"]}]({report_path(d)})\n' for d in D)
readme+='''
- [Methodology and evidence rules](docs/methodology.md)
- [Course requirements](docs/course-requirements.md)
- [AI readings, failure modes and verification](docs/ai-critique-and-controls.md)
- [Public-source catalog and review coverage](docs/sources.md)
- [Editable screening matrix](data/screening-matrix.json), [device records](data/device-records.json) and [contact records](data/contacts.json)

## What to do after reading

Agree on the two priorities that matter most to the team, select three candidate devices, and open the decisive original records for those candidates. Before committing, identify at least one early patent family, a credible early financing trail, the exact initial authorization, and a payment/adoption pathway. A report should remain feasible if nobody replies to an interview request.

The supplied course specification calls for one device and a **4,000-word entire submission including references**. These materials are openly AI-generated selection research, not a completed assessed submission. See the course requirements for the supplied policy, and record real team contributions and source verification. Original course PDFs and extracted readings remain in the separate local workspace; this repository contains analysis and source references.

## Repository layout and maintenance

```text
README.md                 Screening rationale, comparison and TL;DR
devices/                  Nine detailed device-selection reports
docs/                     Methodology, course context, sources and AI checks
data/                     Editable records, qualitative grades and provenance
tools/build_docs.py        Regenerate README, device reports and source index
tools/validate.py          Check local links, source IDs and consistency
AGENTS.md / CONTEXT.md     Instructions and durable project context
```

Run `python tools/build_docs.py` after changing the structured records, then `python tools/validate.py`. Check any time-sensitive source again before changing its verification date. Team preferences can change the shortlist; they should not erase unresolved evidence gaps.
'''

write('README.md',readme)

for d in D:
    c=CURATION[d['id']]
    doc=f'''# {d['name']}

**{d['company']} · Detailed selection report**  
Evidence snapshot: 19 October 2026 · Repository edition: 20 October 2026

[Back to the nine-device comparison](../README.md)

## Selection takeaway

{d['verdict']}

| Decision dimension | Result |
|---|---|
| Technical fit | {c['fit']} |
| Public information | {d['desk']} |
| First-hand access | {c['access']} |
| Relative workload | {d['difficulty']} |

{c['alternative']}

## Product scope and mechanism

{d['mechanism']}

## Clinical evidence and its limits

{d['evidence']}

{citation([x for x in d['sources'] if x.startswith('FDA-') or x in ['RNS-TRIAL','RNS-LONG','CERIBELL-DECIDE','CERIBELL-ED','EXABLATE-LONDON','TERRA-CLINICAL']])}

## Detailed assessment of the five coursework topics

The labels below describe source readiness, not whether this topic has been fully researched. “Strong” can coexist with a small study or a narrow indication: the evidence is available to analyse, but its quality and applicability still need to be judged.

'''
    for i,((_,p),why,grade,keys) in enumerate(zip(d['topics'],c['why'],c['grades'],c['topic_sources'])):
        doc+=f'### {i+1}. {topic_labels[i]} — {labels[grade]}\n\n{p}\n\n**Why this grade:** {why}\n\n'
        if keys: doc+=citation(keys)+'\n\n'
    doc+=f'''## London/UK first-hand access

{d['access']}

'''
    for contact in d['contacts']:
        keys=[contact['source']]
        if contact.get('route_source') and contact['route_source'] not in keys: keys.append(contact['route_source'])
        doc+=f'- **{contact["person"]}** — {contact["kind"]}. Public route: {contact["route"]}. {citation(keys)}\n'
    doc+='''
These are public enquiry leads, not introductions or confirmations of availability. No contact has been made. An educational staff discussion may be more realistic than clinical observation; a local domain specialist is not automatically an exact-device user.

### Questions for a useful interview

'''+''.join(f'{i}. {q}\n' for i,q in enumerate(d['questions'],1))
    doc+='\n## What would make this topic easier to complete?\n\n'+''.join(f'{i}. {x}\n' for i,x in enumerate(c['next'],1))
    doc+=f'''
## Stakeholders to map

{c['stakeholders']}

This is a provisional list to guide the eventual map. It does not claim to follow the lecture-specific map format, which has not yet been supplied. Trace who uses, pays, approves, purchases and benefits; these may be different people or institutions.

## Selection gate and unresolved evidence

{d['gap']}

The judgement is based on the sources located, rather than an exhaustive publication count. Missing IP, early budgets or local use should stay visible until verified. This report does not complete a global current-label audit, freedom-to-operate analysis or independent human review.

## Sources and review coverage

'''
    used=list(dict.fromkeys(d['sources']+[c0['source'] for c0 in d['contacts']]+[c0['route_source'] for c0 in d['contacts'] if c0.get('route_source')]))
    for key in used:
        s=LOOKUP[key]
        doc+=f'- **{key}** — [{s["title"]}]({s["url"]}). {s["type"]}; {s["source_date"] or "undated/current page"}. Checked {s["checked"]}. Coverage: {s["review_coverage"]}.\n'
    doc+='\n'+''.join(f'[{k}]: {LOOKUP[k]["url"]}\n' for k in used)
    write(report_path(d),doc)

source_doc='# Public-source catalog\n\nEvidence checked 19 October 2026. Source existence is not full review. Original documents remain in the separate local workspace.\n\n'
for s in S:
    source_doc+=f"## {s['id']}\n\n[{s['title']}]({s['url']})\n\n- Type: {s['type']}\n- Source date: {s['source_date'] or 'Undated/current page'}\n- Checked: {s['checked']}\n- Review coverage: {s['review_coverage']}\n\n"
write('docs/sources.md',source_doc)
