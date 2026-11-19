# cde-data-quality

An end-to-end test of checking information deliveries automatically against an EIR: requirements, then rules, then sample data, then automated checks. Built on a fictional single-storey GP practice and clinic (Larch Road Health Centre), using ISO 19650-2 and UK National Annex terms, Uniclass 2015, IFC4 and COBie 2.4.

## What's here

| Step | Files |
|---|---|
| 1. EIR in Word and Markdown, with a Word-to-data round trip (`docs/`). Revision P02: campus context, OIR, 15 information requirements, LOIN, security), written so each requirement can be checked | `01_EIR_Larch_Road_Health_Centre.md`, `EIR_change_log.md`, `eir_requirements_register.csv` |
| 2. Data dictionary and rules (57 rules in four layers, plus submission decisions) | `data_dictionary.csv`, `rules.csv`, `reference/`, `README_data_dictionary.md`, `README_rules.md` |
| 2b. The IFC-side requirements as a buildingSMART IDS | `ids/LRHC_asset_requirements.ids`, `tools/build_ids.py` |
| 3. Sample IFC, COBie and document register with 13 seeded errors | `sample/`, `seeded_errors.csv`, `tools/generate_sample.py`, `README_stage3.md` |
| 4. Colab notebook that runs the checks and writes a report | `cde_checks.ipynb`, `tools/cde_lib.py`, `README_stage4.md` |

## Rule layers

1. **Metadata vs data dictionary:** required fields, formats, allowed values, naming, classification, status and revision.
2. **Status vs programme:** right status and revision by the MIDP date.
3. **Content and consistency:** IFC ↔ COBie match, assets in spaces, spaces on floors, systems, and safety rules such as every patient-area basin having a TMV.
4. **Free-text flagging:** maintenance descriptions checked for required tasks. This only flags for a person to decide and never passes or fails anything.

## Design choices

- One data dictionary drives the rules and the IDS. Most client-specific requirements are configuration, not code.
- The IDS covers what can be checked from the IFC alone. Cross-file, COBie-only, register and programme checks stay in the rules library.
- Results feed the EIR's acceptance criteria directly: which fails reject a submission, which reject one container, and which go on a correction list.
