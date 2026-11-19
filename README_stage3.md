# Stage 3: sample data with seeded errors (and the IDS)

## Files

| File | What it is |
|---|---|
| `sample/LRHC-BMC-ZZ-00-M3-W-000001.ifc` | IFC4 model: 19 spaces, 46 assets (one deliberately missing), 12 types, 6 systems, Uniclass classification, property sets, and simple geometry (rooms as boxes either side of a corridor, assets as small blocks in their rooms) so it opens in a 3D viewer |
| `sample/LRHC-BMC-ZZ-ZZ-IE-W-000001.xlsx` | COBie 2.4 workbook: Contact, Facility, Floor, Space, Type, Component, System, Job, Document, Attribute |
| `sample/document_register.csv` | Document register, one row per issue (container, title, originator, status, revision, status date) |
| `seeded_errors.csv` | The 13 known errors, with the rule expected to catch each one. Used for scoring in Stage 5 |
| `ids/LRHC_asset_requirements.ids` | buildingSMART IDS 1.0 file: 12 specifications for the IFC-side requirements |
| `tools/generate_sample.py` | Builds the three sample files from `reference/` plus the clean data and error list in the script |
| `tools/plan_from_ifc.py` | Draws a plan from the IFC file, with assets that have seeded errors in red: `python tools/plan_from_ifc.py sample/<ifc> seeded_errors.csv plan.png` |
| `tools/build_ids.py` | Builds the IDS from `data_dictionary.csv` and `asset_types.csv` |

Submission (check) date: **2027-06-04** (IE3 handover).

## Regenerate

```
python tools/generate_sample.py . .            # add --clean for the same files with no seeded errors
python tools/build_ids.py . ids/LRHC_asset_requirements.ids
```

Each seeded error is one `seed(...)` call in `generate_sample.py`. Delete or comment one out and re-run to get a file without that error. Add a new one the same way.

## What the IDS covers, and what it can't

The IDS holds the requirements that can be checked from the IFC alone: entity, name pattern, Uniclass code, containment in a space, and required properties with allowed values. It can't check:
- IFC against COBie (missing assets, GUIDs, values that disagree)
- COBie-only fields (maintenance jobs, the Contact sheet)
- the document register and the MIDP dates
- rules that compare objects (a TMV serving a basin in the same room, call points per room)

Those stay in `rules.csv`. That split is the point: the IDS is the standard, open way to state the IFC part, and the rules library does the rest.

## Tested here vs. not yet tested

**Tested here:**
- The IFC structure: every reference resolves, attribute counts match IFC4 for each entity type, and the 365 GUIDs are valid and unique.
- The COBie workbook opens and has every required sheet.
- All 13 seeded errors are present.
- Checks on GUIDs, serial numbers, spaces, dates, TMV coverage, PPM jobs, systems, call points and emergency lighting found nothing beyond the seeded errors.
- The IDS is well-formed XML.

**Not yet tested:** opening the IFC in ifcopenshell, validating the IDS against the buildingSMART schema, and running ifctester. ifcopenshell isn't installed here. The last cell of the Stage 4 notebook does all three on Colab.
