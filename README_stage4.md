# Stage 4: the checker notebook

`cde_checks.ipynb` checks an IFC4 model, a COBie 2.4 workbook and a document register against the EIR. It runs all 57 rules in `rules.csv` and writes an Excel and an HTML report.

## Run it on Colab

1. Push this repo to GitHub.
2. Open `cde_checks.ipynb` in Colab (File → Open notebook → GitHub).
3. In the first code cell, set `REPO_URL` to the repo's clone URL. For a private repo, upload the folder to `/content/cde-data-quality` instead.
4. Runtime → Run all.

The setup cell installs ifcopenshell, ifctester and anthropic. Reports go to `out/`:
- `cde_check_report.xlsx`: Summary, Decision, Issues, By rule, By asset type, All checks
- `cde_check_report.html`: the same, in one page you can share
- `ids_report.html`: the ifctester result for the IDS file (Colab only)

To check a different delivery, change the file paths and `CHECK_DATE` in the settings cell.

## How it's built

| Part | Where |
|---|---|
| Rules: one function per rule, tagged `@rule("L1-04")` | the notebook, one cell per layer |
| Loading files, looking up values, writing reports | `tools/cde_lib.py` |
| What to check | `data_dictionary.csv`, `rules.csv`, `reference/` |

Rules L1-04 to L1-09 are generic: they read the data dictionary. Add a required field, pattern, allowed value or minimum there and it gets checked with no code change. A rule with new logic is one new function.

The IFC is read with ifcopenshell. If ifcopenshell isn't installed, a small built-in reader is used instead. It handles simple files like the sample, but use ifcopenshell for real models.

## Layer 4 (free-text review)

Layer 4 only ever returns `flag` or `no flag`, and a person decides.
- **Default (keywords):** looks for the required words in each maintenance description. It's free, and nothing leaves the notebook.
- **Model:** set `USE_LLM = True` and save an Anthropic API key as a Colab secret named `ANTHROPIC_API_KEY`. Only the description text is sent. The key is for a paid account, and sending client data to an outside service is the client's decision. With no key the notebook says so and uses keywords.

## Results on the sample

| Run | Checks | Issues | Outcome |
|---|---|---|---|
| Seeded sample (13 errors) | 4,091 | 31 fail, 1 warn, 1 flag | Rejected (IFC/COBie mismatch and safety-critical fails) |
| Clean sample (`generate_sample.py . <folder> --clean`) | 4,118 | none | Accepted |

All 13 seeded errors are caught. The remaining issues are the knock-on effects listed in `seeded_errors.csv`. The full run takes about 3 seconds.

## Tested here vs. not yet tested

**Tested here (with the built-in IFC reader):**
- Every rule runs with no errors on both samples.
- The seeded and clean results are as above.
- The code extracted from the `.ipynb` gives the same results.
- With the model switched on and no key, it falls back to keywords.

**Not yet tested (needs Colab):**
- The ifcopenshell reader.
- The IFC schema validation and ifctester cell.
- A real model call for layer 4.

If the ifcopenshell results differ from the built-in reader on the sample, that difference is the first thing to check.
