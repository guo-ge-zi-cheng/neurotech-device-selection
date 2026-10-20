# Maintaining the documents

The scripts use Python's standard library.

1. Edit the structured records under `data/`.
2. Run `python tools/build_docs.py` from the repository root.
3. Run `python tools/validate.py`.

The generator writes the short comparison, nine device guides and source index. Each guide shows what a source provides, how it relates to the device, how it helps a required report section and what is missing. Static course context and supporting notes are maintained directly. Validation checks structure and references; it does not refresh or independently validate the research.
