"""Render a simple five-topic comparison and device research guides."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/device-records.json').read_text(encoding='utf-8'))
S=json.loads((ROOT/'data/source-catalog.json').read_text(encoding='utf-8'))
SOURCES={s['id']:s for s in S}
A=json.loads((ROOT/'data/additional-research.json').read_text(encoding='utf-8'))
ADDITIONS={d['device_id']:d for d in A['devices']}
FDA={'precision':'FDA-PRECISION-K242618','rns':'FDA-RNS-P100026','ceribell':'FDA-CERIBELL-K223504','saint':'FDA-SAINT-K220177','exablate':'FDA-EXABLATE-P150038','arcex':'FDA-ARCEX-DEN240014','terra':'FDA-TERRA-K170840'}
EXTRA={'precision':['PRECISION-HOME'],'rns':['RNS-TRIAL','RNS-LONG','RNS-2026'],'ceribell':['CERIBELL-DECIDE','CERIBELL-ED','CERIBELL-ORIGIN'],'saint':['SAINT-FACT','SAINT-ABOUT'],'exablate':['EXABLATE-UCLH','EXABLATE-LONDON'],'arcex':['FDA-ARCEX-K251821','ARCEX-IFU','ARCEX-UPLIFT','ARCEX-PATHFINDER','ARCEX-CE','ARCEX-ANNUAL2025'],'terra':['TERRA-BROCHURE','TERRA-KCL-FACILITY','TERRA-X-2024','TERRA-ANEURYSM']}
def write(path,text): (ROOT/path).write_text(text.strip()+'\n',encoding='utf-8')
def links(keys):return '; '.join(f'[{SOURCES[k]["title"]}]({SOURCES[k]["url"]})' for k in dict.fromkeys(keys))
def path(d):return f'devices/{d["number"]:02d}-{d["id"]}.md'

readme='''# Choosing a device for our report

This repository compares seven devices by **how easy it is to find useful information for the five sections in Project spec**. Open a device report to understand what it does, how far it has developed, which sources help each section, and which first-hand contacts have a specific connection to it.

**Source collection:** [Information resource directory](docs/information-resources.md), including databases and worked examples from our studies.

For university subscriptions and support, see the [Imperial resource guide](docs/imperial-resources.md).

**New:** [Seven full case-study drafts](reports/README.md) turn that research into narratives. The [comparative review](reports/comparative-review.md) assesses their strengths, missing evidence and actual writing difficulties. Existing research layers are retained.

## TL;DR

- **RNS is a clear starting point for public research.** Trials, IP and economics now have a pre-approval financing filing and a payer policy alongside them; the earliest funding still needs work.
- **ARC-EX combines good public records with nearby exact-device contacts.** Neurokinex lists Hemel Hempstead and Gatwick centres outside London; London-based Spinal Research can help with funding and UK access. Early product-specific finance and payment remain gaps.
- **Exablate has a documented London clinical team and UK commissioning evidence.** New financing records and an England economic model add useful detail; a brain-specific early budget remains missing.
- **Ceribell and SAINT have useful clinical and IP sources.** Their reports explain the product/version limits; no London product user was verified for either.
- **Terra has a named scanner and enquiry team at St Thomas’ Hospital.** Regulatory/manufacturing records are strong; original IP, development spending and clinical payment need work.
- **Precision requires a clear choice of scope:** the temporary cortical electrode or the wider BCI programme. Payment and exact-product IP need more investigation.

## What information do we need?

These five questions follow the [project specification summary](docs/course-requirements.md):

| Report section | Information needed |
|---|---|
| Unmet medical need | The original problem, patient numbers and geography, alternatives, and costs before/after the device. |
| Intellectual property | Where the first version was invented, inventors and employers, patents/other IP, and at least the independent patent claims. |
| Fundraising | How early development was funded: grants, angels, VC, amounts, sources and valuations where available. Later growth funding is a different question. |
| Regulatory | Classification in the relevant markets, approval/clearance evidence, standards, and manufacturing/outsourcing. |
| Reimbursement | Who pays, relevant codes, the economic case and the required stakeholder map. |

## How easy is it to find useful information?

**Clear sources:** useful records provide a supported starting point. **Some gaps:** the sources answer only part of the question. **Hard to find:** important information remains unverified in this search. These describe access to information, not a completed report. Each device file explains the reason and how to use the sources.

The [source guide](docs/research-source-guide.md) draws on the [two course examples](docs/example-source-audit.md). We have now investigated its extra routes for all seven devices using a [reliability protocol](docs/reliability-protocol.md): read the actual evidence, match the product/market, examine the method and check important ambiguities.

**The table retains the original access labels.** Each device file has **Layer 1: original research** and **Layer 2: new findings**, covering all five topics. The [new-research overview](docs/additional-research-summary.md) explains what improved and what remains missing. Important update: SAINT and Ceribell's seizure-monitor US inpatient NTAP add-ons have ended for FY2027; this does not mean all hospital payment ends.

| Device | Unmet need | IP | Fundraising | Regulatory | Reimbursement |
|---|---|---|---|---|---|
'''
for d in D:readme+=f'| [{d["name"]}]({path(d)}) | '+' | '.join(s['access'] for s in d['sections'])+' |\n'
readme+='''
All seven have a public FDA record, making that a useful regulatory starting point. Other markets, standards and manufacturing still need to be completed. Disease-population figures alone will not answer unmet need, and a large company funding round will not answer early development finance.

## Who could provide useful first-hand information in or near London?

| Device | What is actually connected to the device? | What could it help us investigate? |
|---|---|---|
'''
local={
'precision':('No London user verified. A US co-founder/inventor is identified.','Product origin and the temporary electrode versus wider BCI; remote enquiry.'),
'rns':('No London RNS user verified. Product-specific US clinical leads are identified.','Original trials, development and follow-up; remote enquiry.'),
'ceribell':('No London Ceribell user verified. Co-founder Josef Parvizi is a US lead.','Actual invention, clinical studies and economic-model assumptions; remote enquiry.'),
'saint':('No licensed London SAINT site verified. Co-developer Brandon Bentzley is a US lead.','Academic development, licensing and commercialization; remote enquiry.'),
'exablate':('UCLH/NHNN paper names exact ExAblate equipment and a London clinical team.','Patient selection, treatment workflow, costs and UK adoption.'),
'arcex':('Neurokinex lists exact-device centres in Hemel Hempstead and Gatwick, outside London. Spinal Research has a London office and an ARC-EX programme.','Device-study and rehabilitation workflow; programme funding and UK access. A charity office is not a clinic.'),
 'terra':('King’s lists an exact MAGNETOM Terra at LoCUS, St Thomas’ Hospital, with dedicated enquiries.','Imaging workflow, configuration, scan resources and access funding; routine NHS use is unverified.')}

for d in [next(x for x in D if x['id']==k) for k in ['exablate','arcex','terra']]:
    a,b=local[d['id']];readme+=f'| [{d["name"]}]({path(d)}) | {a} | {b} |\n'
readme+='''
For **Precision, RNS, Ceribell and SAINT**, no London product user was verified. Their reports identify relevant US development or clinical leads for a possible remote discussion.

We do **not** have London user counts. This table uses documented connections, not general subject expertise or assumed popularity. No interview or visit is arranged.

The detailed reports show **source → connection to this device → use in a report section → missing information**. [Source notes](docs/sources.md) record dates and review limits. Existing research dates to 19 October 2026, with targeted additions/checks on 20 October. These are AI-generated preparation notes; the supplied course rules remain in the specification summary.
'''
write('README.md',readme)

for d in D:
    text=f'''# {d['name']}

**{d['company']}** · [Back to the comparison](../README.md)

## What does it do?

'''+ '\n\n'.join(d['description'])+f'''

## How far has it developed?

{d['stage']}

Sources for this description and stage: {links([FDA[d['id']]]+EXTRA[d['id']])}.

### What does the clinical evidence actually show?

{d['clinical_evidence']}

**Practical takeaway:** {d['summary']}

## Finding information for the five report sections

For gaps, use the [shared research source guide](../docs/research-source-guide.md). Its alternative routes need checking for this device before they become evidence.

'''
    for i,s in enumerate(d['sections'],1):
        text+=f'''### {i}. {s['topic']}

**Access to useful information: {s['access']}.**

**What we found:** {s['found']}

**How close is it to this device?** {s['relationship']}.

**How it helps write this section:** {s['how_to_use']}

**Still needed:** {s['missing']}

'''
        if s['sources']:text+='Useful sources: '+links(s['sources'])+'.\n\n'
    text+=f'''## Useful first-hand enquiries

**London position:** {d['london_summary']}

'''
    for c in d['contacts']:
        text+=f'''### {c['person']} — {c['location']}

**Why this person/team is included:** {c['connection']}

**What they could help us investigate:** {c['how_helpful']}

**What their connection does not establish:** {c['limits']}

**Public enquiry route:** {c['route']}

Evidence for the connection and route: {links(c['sources'])}.

'''
    text+='''No contact has been made and no visit has been agreed. Start with a short staff discussion about the specific questions above; do not assume access to patients or treatment sessions.

## Before choosing this device

'''
    text+='\n'.join(f'- **{s["topic"]}:** {s["missing"]}' for s in d['sections'] if s['access']=='Hard to find') or '- Read the linked records for the missing first-version, funding and payment details before committing.'
    text+='\n\nCheck the [source notes](../docs/sources.md) for what was reviewed and when. Existing evidence dates to 19 October 2026, with targeted checks/additions on 20 October. The lecture stakeholder-map format is still needed for the final report.\n'
    # Preserve every original paragraph/link; only move its headings down one level.
    header,body=text.split('\n\n',1)
    company,body=body.split('\n\n',1)
    import re
    original=re.sub(r'^(#{2,}) ',r'#\1 ',body,flags=re.M)
    addition=ADDITIONS[d['id']]
    original_note = ('Original snapshot: 20 October 2026. Terra was added after the six-device investigation; its initial access labels are retained below.' if d['id']=='terra' else 'Original snapshot: 19 October 2026, with earlier targeted additions on 20 October (ARC-EX was added on 20 October). The text and access labels below are preserved. Read Layer 2 for new evidence and dated updates.')
    layered=f'''{header}

{company}

[Original research](#layer-1-original-research) · [New findings](#layer-2-additional-research-20-october-2026) · [Reliability checks](../docs/reliability-protocol.md)

## Layer 1: Original research

{original_note}

'''+original.strip()+f'''

## Layer 2: Additional research (20 October 2026)

{addition['summary']}

**How to read this layer:** each finding states what the evidence supports, why it is usable, how it helps the report and where it stops. [Reliability protocol](../docs/reliability-protocol.md). “Context” is useful background, not a result for this product. No new interview has taken place.

'''
    for i,t in enumerate(addition['topics'],1):
        layered+=f'''### {i}. {t['topic']}

**Search route:** {t['search_route']}

'''
        for f in t['findings']:
            layered+=f'''#### {f['title']}

**{f['label']}.** {f['evidence']}

**Why this evidence is usable:** {f['reliability']}

**Use in the report:** {f['use_in_report']}

**Limit:** {f['limit']}

Sources: {links(f['sources'])}.

**Where checked:** {f['locator']}. **Evidence route:** {f['origin']}. Checked {A['checked']}; source dates and review coverage are in the [source index](../docs/sources.md).

'''
        layered+=f'**Remaining gap:** {t["remaining_gap"]}\n\n'
    layered+=f'''### What this changes for our choice

{addition['what_changes']}

These additions answer specific questions rather than re-grade the original table. See the [cross-device overview and unsuccessful searches](../docs/additional-research-summary.md). The required lecture stakeholder-map format still needs to be supplied.
'''
    layered+=f'''\n## Full case-study reference draft

[Read the full {d['name']} report]({d['id']}/full-report.md), with the five narrative sections, independent-claim explanations, stakeholder map and numbered references. The [comparative review](../reports/comparative-review.md) explains its strengths, gaps and writing difficulties. The two research layers above are preserved.
'''
    write(path(d),layered)

source_text='''# Sources and what was checked

The device reports explain how each source helps a report section. This index records the URL, source type and actual review coverage. An old decision or policy remains a historical record unless current applicability is checked. Course originals remain in the separate local workspace.

'''
for s in S:
    source_text+=f'''## {s['id']}

[{s['title']}]({s['url']})

- Type: {s['type']}
- Source date: {s['source_date'] or 'See the original record'}
- Checked: {s['checked']}
- What was reviewed: {s['review_coverage']}

'''
    if s.get('access_route'):source_text+=f'- Access route: {s["access_route"]}\n\n'
write('docs/sources.md',source_text)

overview='''# Additional research: what the extra sources actually add

Checked 20 October 2026. We investigated all seven devices across the same five topics, using the [reliability protocol](reliability-protocol.md) before accepting claims. The extra routes came from the [course-example source audit](example-source-audit.md); using a route does not make its claims automatically correct.

Each device report preserves its original research as Layer 1 and adds the findings as Layer 2. The original device data, contacts and access labels have not been replaced. A deeper read of an already-used patent or prospectus is labelled as such; it is not a new independent confirmation. Dates and actual review limits appear in the [source index](sources.md).

## What improved, and what did not

| Device | Result of the additional search |
|---|---|
'''
for d in D:
    overview+=f'| [{d["name"]}](../{path(d)}#layer-2-additional-research-20-october-2026) | {ADDITIONS[d["id"]]["what_changes"]} |\n'
overview+='''
## Important dated updates

- The FY2027 US inpatient final rule ends the NTAP add-ons for SAINT and the Ceribell Status Epilepticus Monitor. This is not a finding that all underlying payment ends. A new Ceribell delirium award is a separate product/indication decision.
- RNS MRI labeling differs between models: a historical RNS-300M restriction must not be applied to RNS-320 without its model-specific conditions.
- UK essential-tremor commissioning does not establish the same route for Parkinsonian tremor. NICE's Parkinsonian-tremor procedure guidance restricts use to formal approved research.
- Insightec's 2012 agreement record contains conflicting valuation figures. Neither is presented as settled. The economic model also has an abstract/body comparator-cost discrepancy; the body tables were checked.

The linked Layer 2 findings supply the relevant primary sources and scope for these statements. Original authorisation, current indication, coding, coverage and payment amount remain distinct questions.

## Searches that did not yield an accepted answer

'''
for lead in A['leads_not_accepted']:
    overview+=f'''### {lead['question']}

**Route tried:** {lead['route']}.

{lead['reason']}

'''
overview+='''## How to continue

Choose the precise device/version and geography before narrowing population, claims or payment. Use each topic's remaining gap as the next research question. An unpublished price or earliest round can remain unknown; an explicit estimate is a different kind of answer. No new outreach, interview, site visit or access permission is implied by these records.

The original six-device extension added 34 catalog entries and 35 findings; Terra adds its separately dated evidence above. These are an audit trail, not a quality score. Reliability is assessed claim by claim; this targeted review is not a full legal, clinical, global regulatory or payer audit.
'''
write('docs/additional-research-summary.md',overview)

audit=json.loads((ROOT/'data/example-source-audit.json').read_text(encoding='utf-8'))
audit_text='''# Sources used in the two course examples

This audit records what the examples used, what those sources help explain and where the inference stops. Use the [research source guide](research-source-guide.md) for the practical method. Checked 20 October 2026. Physical PDF page numbers include the opening anonymisation page and differ from printed page numbers.

## Authority and review scope

'''
for item in audit['authority']:
    audit_text+=f'- **{item["level"]}:** {item["finding"]} ({item["provenance"]}).\n'
audit_text+='\n'+audit['review_scope']+'\n\n'
for topic in dict.fromkeys(r['topic'] for r in audit['rows']):
    audit_text+=f'## {topic}\n\n'
    for r in [x for x in audit['rows'] if x['topic']==topic]:
        audit_text+=f'''### {r['report']}

Location: {r['pages']}. References: {r['references']}.

**Sources used:** {r['sources']}.

**What they help explain:** {r['use']}

**Extra route for our research:** {r['alternative']}

**Limits:** {r['limit']}

**Lecturer evidence:** {r['lecturer_status']}

'''
audit_text+='## Selected external checks\n\nThese targeted checks were made on 20 October 2026; they do not verify every reference in either example.\n\n'
for c in audit['external_checks']:
    audit_text+=f'''### {c['title']}

[{c['source_title']}]({c['url']})

**Checked finding:** {c['finding']}

**Use and limit:** {c['limit']}

**Review coverage:** {c['coverage']}

'''
audit_text+='''## Reference handling

Optomed's opening note reports that embedded reference links were lost in submission, causing a mark deduction. The supplied copy nevertheless contains recoverable link annotations. These observations concern different copies and can both be true. Quadsense has a printed bibliography; its image-based body was read with OCR and visual checks. Use full retrievable references in the eventual report as the specification requires.

The original course/example PDFs and interview material have not been republished. Interviews described in the examples were conducted by those reports' authors, not this team. No complete patent-status, database-valuation or payer audit is claimed. This example audit does not change the six devices' access labels.
'''
write('docs/example-source-audit.md',audit_text)

# The full drafts are authored separately from the preserved research layers.
import runpy
runpy.run_path(str(ROOT/'tools/build_full_reports.py'))
