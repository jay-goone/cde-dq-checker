# Delivery planner checks

Checks whether the information planned in the MIDP arrives on time, at the right status, with metadata that matches the plan and the client's reference data.

Scenario: Larch Road Health Centre (MA 4920.203), design and build, offsite modular construction. Contract award 25 Nov 2026, practical completion 4 Jun 2027. Data date for the checks: 1 May 2027.

**Result:** 25 checks. The perfect data gives 0 issues. 28 deliberate faults are each caught by the check aimed at them, with 0 false alarms. With all 28 faults at once: 34 issues (31 errors, 3 warnings).

## Run it

**On Colab:** open `delivery_planner_checks.ipynb` (Colab → File → Open notebook → GitHub, or upload it), then Runtime → Run all. The second cell gets the code from GitHub (public repo) or asks you to upload the repo zip (private repo).

**On a computer with Python and pandas**, from this folder:

```
python -m checks.run          # checks on the perfect data
python -m faults.score        # fault scoring, broken data, and outputs/delivery_check_report.xlsx
```

## How it fits together

```
INPUTS (as exported)                 ADAPTERS                      CHECKS                       OUTPUTS
data/reference_library.csv  ─────────────────────────────┐
data/midp.csv               ─────────────────────────────┤
data/programme/*.xer / .csv ──▶ adapters/p6.py ─────────┼──▶ checks/common.py (load,     ──▶ delivery status register
data/cde/projectwise_*.csv  ──▶ adapters/cde_projectwise.py      prepare, due dates)          issues list
                                                         └──▶ R, P, C, T, M checks         outputs/*.csv, report.xlsx

TEST HARNESS: faults/catalogue.py (28 faults) ──▶ faults/score.py (break, run, score)
SCENARIO GENERATORS (make the practice data; not needed on a real project):
tools/scenario.py + tools/scheduler.py ──▶ tools/build_scenario.py ──▶ midp.csv, programme files
                                           tools/build_cde.py      ──▶ ProjectWise export
                                           tools/plot_programme.py ──▶ summary Gantt
```

## Files

| Folder / file | What it is |
|---|---|
| `data/reference_library.csv` | Client's codes: project, originators, volume (zones), levels, types, roles, suitability, stages, exchanges. Each code has a status and approval date. 93 codes. |
| `data/midp.csv` | MIDP by the lead appointed party: 50 rows, 45 containers, each linked to a P6 activity. No due dates: they come from the programme. |
| `data/programme/` | P6 programme: baseline (25 Nov 2026) and update 6 (data date 1 May 2027), as `.xer` and as `.csv` with identical content. 419 activities, 663 relationships, 2 calendars. Plus a summary Gantt. |
| `data/cde/projectwise_export_2027-05-01.csv` | ProjectWise-style export, one row per version: 108 versions of 38 containers. |
| `data/broken/` | The same inputs with all 28 faults applied (written by `faults/score.py`). |
| `adapters/p6.py` | Reads `.xer` or `.csv` into the standard `activities` table. |
| `adapters/cde_projectwise.py` | Reads the ProjectWise export into the standard `cde_versions` table. |
| `checks/common.py` | Loads the inputs, works out due dates and what the CDE holds per MIDP row, and defines the issue format. |
| `checks/reference.py` … `metadata.py` | The 25 checks in five groups. See `checks/README_checks.md`. |
| `checks/run.py` | Runs every check and builds the delivery status register. |
| `faults/catalogue.py` | 28 deliberate faults, each aimed at one or two checks. |
| `faults/score.py` | Applies each fault, runs the checks, scores caught / missed / false alarms; builds the broken data and the report. |
| `delivery_planner_checks.ipynb` | Colab notebook that runs all of the above, one step per cell. |
| `outputs/` | Registers, issues, fault scores and `delivery_check_report.xlsx`. |
| `tools/` | Scenario generators: `scenario.py`, `scheduler.py`, `build_scenario.py`, `build_cde.py`, `plot_programme.py`. |

## The two outputs

- **Delivery status register:** one row per MIDP row. Baseline and forecast due dates, versions in the CDE, latest revision and suitability, the date the required suitability was reached, a delivery status (*Delivered on time, Delivered late, Overdue, Not yet due, No due date*), and the count of errors and warnings.
- **Issues list:** one row per problem, always with the same columns: `check_id, check_name, dimension, severity, source, midp_id, container, field, found, expected, message`.

## Scenario notes

- **Programme:** WBS project → RIBA stage (4, 5, 6) or KEY → package. EIR milestones are fixed dates: M-203-S4 (IE1) 15 Jan 2027, M-203-IE2 16 Apr, M-203-PC (IE3) 4 Jun, M-203-REC (IE4) 2 Jul. Calendars: 5-day with English bank holidays and a Christmas shutdown; 7-day for the 14-day soak test. No open ends. Update at 1 May 2027: progress exactly as planned.
- **CDE versions:** each MIDP row gives a work-in-progress share during its Develop activity (S1 for models and drawings, S2 otherwise), then the issue at its required suitability on the finish date of its linked activity. Stage 4 deliverables are authorised at A4 (C01) when the client signs off Stage 4. Revisions run per container: P01, P02 … for S codes; C01 … for A codes and CR.
- **Zones** (volume codes Z1–Z4, EW) were proposed by the architect on 30 Nov and approved by the client on 4 Dec 2026, so they can't be used before then (check R03).
- The `.xer` files have been read by our own adapter only, not by P6 or a viewer.

Rebuild the practice data from the repo root:

```
python delivery_planner/tools/build_scenario.py
python delivery_planner/tools/build_cde.py
python delivery_planner/tools/plot_programme.py
```
