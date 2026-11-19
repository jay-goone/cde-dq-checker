# Word round trip: human-readable to machine-readable

The EIR is written and edited in Word. The checking rules need data. This folder connects the two.

```
Markdown (source)  ──pandoc + finish_docx.py──▶  Word (.docx)  ──you edit──▶  Word (edited)
                                                                                  │
               rules.csv / data_dictionary.csv  ◀── compare_clauses.py ◀── docx_to_clauses.py
```

## Files

| File | What it is |
|---|---|
| `LRHC-LRV-ZZ-ZZ-SP-K-000001_P04_EIR.docx` / `_P04_change_log.docx` | The EIR at P04 (adds Section 22, contractual mechanisms) and the change log P01 to P04 |
| `LRHC-LRV-ZZ-ZZ-SP-K-000001_P03_EIR.docx` | The EIR at P03, A4 landscape, every requirement in a table with its ID in the first column |
| `LRHC-LRV-ZZ-ZZ-SP-K-000001_P03_change_log.docx` | Change log P01 to P03 |
| `EIR_to_checks_workflow_P03.docx` / `.md` | Step-by-step workflow from EIR to checks, with risks |
| `clauses_P04.csv` | The P04 extract: 320 records (185 clauses, 135 IR items). Compared with P03 in `changes_P03_P04.md` |
| `clauses_P03.csv` | The P03 extract: 302 records (167 clauses, 135 IR items) |
| `clauses_P02.csv` | The P02 baseline extracted from the Word file: 166 records (76 clauses, 90 IR components) |
| `../tools/docx_to_clauses.py` | Reads a Word EIR into `clauses.csv` |
| `../tools/compare_clauses.py` | Compares two extractions and lists the rules and data dictionary rows each change touches |
| `../tools/finish_docx.py`, `../tools/word_reference.docx` | Formatting used to make the Word files from Markdown |

## Editing rules (so the round trip keeps working)

1. **Keep the clause ID in the first column** of its table. That's how a row is recognised.
2. **Never renumber or reuse an ID.** To retire a clause, delete the row. A new clause gets a new ID (e.g. `SEC-08`).
3. **Don't merge cells** in requirement tables.
4. **Keep the "IR-xx Title" headings.** The component tables under them are read as `IR-xx/<component>`.
5. **Track Changes is fine.** Changes are accepted before extraction. Comments are ignored.
6. Text outside tables (introductions, explanations) is for people. It isn't extracted.

## Commands

```
python tools/docx_to_clauses.py docs/<edited>.docx docs/clauses_P04.csv
python tools/compare_clauses.py docs/clauses_P03.csv docs/clauses_P04.csv . docs/changes_P03_P04.md
```

## Test (19 Nov 2026)

Three edits were made in a copy of the P02 Word file: TMV interval 6 → 3 months (AIR-19), area tolerance 2% → 1% (IR-04), and MID-02 deleted. The compare report showed:
- AIR-19 changed: review rule L1-22 and data dictionary row DD-062. The value itself lives in `reference/asset_types.csv` (`max_interval_months`).
- IR-04 acceptance criteria changed: **no rule yet.** The area-tolerance rule is still in the backlog (Annex B.2), so this showed the gap.
- MID-02 removed: rule L2-05 cites it and must be retired or re-pointed.
