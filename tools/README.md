# Maintaining the documents

The scripts use Python's standard library.

1. Edit the structured records under `data/`.
2. Run `python tools/build_docs.py` from the repository root.
3. Run `python tools/validate.py`.

The generator writes the root README, nine device reports and source index. Static methodology, course context, AI critique and folder indexes are maintained directly. Validation checks structure and references; it does not refresh or independently validate the research.
