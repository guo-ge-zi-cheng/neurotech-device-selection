"""Render a simple five-topic comparison and device research guides."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/device-records.json').read_text(encoding='utf-8'))
S=json.loads((ROOT/'data/source-catalog.json').read_text(encoding='utf-8'))
SOURCES={s['id']:s for s in S}
FDA={'precision':'FDA-PRECISION-K242618','rns':'FDA-RNS-P100026','ceribell':'FDA-CERIBELL-K223504','saint':'FDA-SAINT-K220177','exablate':'FDA-EXABLATE-P150038','terra':'FDA-TERRA-K170840','viz':'FDA-VIZ-DEN170073','optune':'FDA-OPTUNE-P100034S013','canvas':'FDA-CANVAS-DEN200069'}
EXTRA={'precision':['PRECISION-HOME'],'rns':['RNS-TRIAL','RNS-LONG','RNS-2026'],'ceribell':['CERIBELL-DECIDE','CERIBELL-ED','CERIBELL-ORIGIN'],'saint':['SAINT-FACT','SAINT-ABOUT'],'exablate':['EXABLATE-UCLH','EXABLATE-LONDON'],'terra':['TERRA-KCL','TERRA-CLINICAL'],'viz':['VIZ-FOUNDER'],'optune':['OPTUNE-IMPERIAL'],'canvas':['CANVAS-UPDATE']}
def write(path,text): (ROOT/path).write_text(text.strip()+'\n',encoding='utf-8')
def links(keys):return '; '.join(f'[{SOURCES[k]["title"]}]({SOURCES[k]["url"]})' for k in dict.fromkeys(keys))
def path(d):return f'devices/{d["number"]:02d}-{d["id"]}.md'

readme='''# Choosing a device for our report

This repository compares nine devices by **how easy it is to find useful information for the five sections in Project spec**. Open a device report to understand what it does, how far it has developed, which sources help each section, and which first-hand contacts have a specific connection to it.

## TL;DR

- **RNS and Optune offer clear starting points for public research.** Relevant clinical/regulatory records and company filings are identified; original financing still needs work.
- **Optune, Exablate and Terra have documented London product or equipment connections.** Exablate has a useful UK commissioning source but harder early funding. Terra's original IP and development finance are harder.
- **Viz has a London co-founder lead for the business history**, not a verified London stroke-product user.
- **Ceribell and SAINT have useful clinical and IP sources, but no London product user was verified.** Precision needs a clear choice between the temporary electrode and the larger BCI. Canvas Dx has an actual US payer bulletin, but product-specific IP and local access are still gaps.

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

**Clear sources:** useful direct records are identified. **Some gaps:** the sources answer only part of the question. **Hard to find:** important information remains unverified in this search. These describe access to information, not a completed report. Each device file explains the reason and how to use the sources.

| Device | Unmet need | IP | Fundraising | Regulatory | Reimbursement |
|---|---|---|---|---|---|
'''
for d in D:readme+=f'| [{d["name"]}]({path(d)}) | '+' | '.join(s['access'] for s in d['sections'])+' |\n'
readme+='''
All nine have a public FDA record, making that a useful regulatory starting point. Other markets, standards and manufacturing still need to be completed. Disease-population figures alone will not answer unmet need, and a large company funding round will not answer early development finance.

## Who could provide useful first-hand information in London?

| Device | What is actually connected to the device? | What could it help us investigate? |
|---|---|---|
'''
local={
'precision':('No London user verified. A US co-founder/inventor is identified.','Product origin and the temporary electrode versus wider BCI; remote enquiry.'),
'rns':('No London RNS user verified. Product-specific US clinical leads are identified.','Original trials, development and follow-up; remote enquiry.'),
'ceribell':('No London Ceribell user verified. Co-founder Josef Parvizi is a US lead.','Actual invention, clinical studies and economic-model assumptions; remote enquiry.'),
'saint':('No licensed London SAINT site verified. Co-developer Brandon Bentzley is a US lead.','Academic development, licensing and commercialization; remote enquiry.'),
'exablate':('UCLH/NHNN paper names exact ExAblate equipment and a London clinical team.','Patient selection, treatment workflow, costs and UK adoption.'),
'terra':("King's lists an exact Terra scanner at St Thomas' and a facility contact.",'Practical scanning, operating costs, capacity and clinical/research access.'),
'viz':('Manoj Ramachandran is a London Viz.ai co-founder; his specialty is orthopaedics.','Company formation, early finance and first hospital relationships; not local stroke deployment.'),
'optune':('Imperial explicitly identifies Dr Matthew Williams with introducing Optune in the UK.','Patient experience, adherence, support needs, private payment and adoption barriers.'),
'canvas':('No London Canvas Dx user verified. Founder Dennis Wall is a US lead.','Academic/product origin and assessment design; remote enquiry.')}
for d in [next(x for x in D if x['id']==k) for k in ['optune','exablate','terra','viz']]:
    a,b=local[d['id']];readme+=f'| [{d["name"]}]({path(d)}) | {a} | {b} |\n'
readme+='''
For **Precision, RNS, Ceribell, SAINT and Canvas Dx**, no London product user was verified. Their reports identify relevant US development or clinical leads for a possible remote discussion.

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
