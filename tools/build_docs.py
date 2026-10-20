"""Render a simple five-topic comparison and device research guides."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/device-records.json').read_text(encoding='utf-8'))
S=json.loads((ROOT/'data/source-catalog.json').read_text(encoding='utf-8'))
SOURCES={s['id']:s for s in S}
FDA={'precision':'FDA-PRECISION-K242618','rns':'FDA-RNS-P100026','ceribell':'FDA-CERIBELL-K223504','saint':'FDA-SAINT-K220177','exablate':'FDA-EXABLATE-P150038','arcex':'FDA-ARCEX-DEN240014'}
EXTRA={'precision':['PRECISION-HOME'],'rns':['RNS-TRIAL','RNS-LONG','RNS-2026'],'ceribell':['CERIBELL-DECIDE','CERIBELL-ED','CERIBELL-ORIGIN'],'saint':['SAINT-FACT','SAINT-ABOUT'],'exablate':['EXABLATE-UCLH','EXABLATE-LONDON'],'arcex':['FDA-ARCEX-K251821','ARCEX-IFU','ARCEX-UPLIFT','ARCEX-PATHFINDER','ARCEX-CE','ARCEX-ANNUAL2025']}
def write(path,text): (ROOT/path).write_text(text.strip()+'\n',encoding='utf-8')
def links(keys):return '; '.join(f'[{SOURCES[k]["title"]}]({SOURCES[k]["url"]})' for k in dict.fromkeys(keys))
def path(d):return f'devices/{d["number"]:02d}-{d["id"]}.md'

readme='''# Choosing a device for our report

This repository compares six devices by **how easy it is to find useful information for the five sections in Project spec**. Open a device report to understand what it does, how far it has developed, which sources help each section, and which first-hand contacts have a specific connection to it.

## TL;DR

- **RNS is a clear starting point for public research.** Clinical trials, a patent, a prospectus and an economic model are identified; early funding still needs work.
- **ARC-EX combines good public records with nearby exact-device contacts.** Neurokinex lists Hemel Hempstead and Gatwick centres outside London; London-based Spinal Research can help with funding and UK access. Early product-specific finance and payment remain gaps.
- **Exablate has a documented London clinical team and a UK commissioning source.** It offers a direct local enquiry route, while early development funding is harder to find.
- **Ceribell and SAINT have useful clinical and IP sources.** Their reports explain the product/version limits; no London product user was verified for either.
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

The [five-topic research source guide](docs/research-source-guide.md) explains how investor/funder records, care-pathway studies, patent searches, procedure payment, comparators and real interviews can fill gaps. It draws on an [audit of the Optomed and Quadsense examples](docs/example-source-audit.md). The table below retains the device evidence already checked; these extra routes need investigation before any label changes.

| Device | Unmet need | IP | Fundraising | Regulatory | Reimbursement |
|---|---|---|---|---|---|
'''
for d in D:readme+=f'| [{d["name"]}]({path(d)}) | '+' | '.join(s['access'] for s in d['sections'])+' |\n'
readme+='''
All six have a public FDA record, making that a useful regulatory starting point. Other markets, standards and manufacturing still need to be completed. Disease-population figures alone will not answer unmet need, and a large company funding round will not answer early development finance.

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
'arcex':('Neurokinex lists exact-device centres in Hemel Hempstead and Gatwick, outside London. Spinal Research has a London office and an ARC-EX programme.','Device-study and rehabilitation workflow; programme funding and UK access. A charity office is not a clinic.')}

for d in [next(x for x in D if x['id']==k) for k in ['exablate','arcex']]:
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
    write(path(d),text)

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
write('docs/sources.md',source_text)

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
