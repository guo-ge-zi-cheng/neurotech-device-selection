# Evidence records

device-records.json contains the expanded descriptions, five-section source guide and justified contacts. screening-matrix.json contains the short comparison shown in the README. source-catalog.json records URLs and what was actually reviewed. contacts.json and checks-and-corrections.json make the contact reasons and corrections inspectable.

Information access is described as Clear sources, Some gaps or Hard to find. It is not a clinical ranking. Regenerate documents after changing the records.

additional-research.json contains the dated follow-up across six devices and five topics: accepted findings, evidence labels, exact locators, source routes, reliability reasoning, use in the report, limits and unsuccessful searches. It generates Layer 2 of each device report and docs/additional-research-summary.md. Layer 1 preserves the original device-records.json text and access labels. New catalog entries supplement the original source records; deeper use of an existing source is labelled explicitly. Use docs/reliability-protocol.md before extending this evidence.

example-source-audit.json records the five-section audit of the two supplied examples, document/page provenance, lecturer-feedback limits and selected external checks. It generates docs/example-source-audit.md. This is shared research context, separate from the six devices' source catalog and access labels. Source use in an example is not a new verified source claim for one of our devices.

full-reports.json holds the six authored case-study bodies, reference-detail overrides, comparative review and writing-method text. Citations use [@SOURCE-ID] placeholders in this data file and become numbered references in generated reports. full-report-evidence.json records deeper source checks without modifying earlier coverage records. full-report-manifest.json records generated paths, complete-file word counts, references, selected independent claims and hashes. research-preservation.json protects the prior guide prefixes, research data and first 85 source records. Regenerate through tools/build_docs.py, then run both validation scripts.
