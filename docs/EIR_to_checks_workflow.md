# Workflow: from EIR to automated checks and report

**Exercise:** MA 4920.203 Larch Road Health Centre · **EIR revision:** P03 · **Date:** 2026-11-19

This note follows one requirement from being written to being checked. For each step it gives who does it, what goes in and comes out, what can go wrong, how you'd know, and how it's controlled. The last column says where this exercise stands.

```
DEFINE (client)            TRANSLATE (client IM)              RESPOND (delivery team)        VERIFY (client)
1 Outcomes and owners  →   4 Word → data                  →   8 Tender and BEP           →   11 Run the checks
2 Write the EIR        →   5 Compare revisions            →   9 Produce + self-check     →   12 Report and decide
3 Issue annexes and    →   6 Update dictionary and rules  →   10 Submit to the CDE       →   13 Feedback and resubmit
  reference info           7 Test the checker                                            →   14 Load to destination systems
                                                                                         →   15 Measure KPIs and benefits
                    ↑__________________ change control: a new EIR revision repeats steps 3 to 7 ________________|
```

---

## Phase 1: Define (appointing party)

| Step | Who | In → Out | What can go wrong | How you'd know | Control | Exercise status |
|---|---|---|---|---|---|---|
| **1. Set outcomes and owners** | ICB requirement owners, appointing party IM | Organisational objectives → OIR outcomes with IDs, named owners | Requirements nobody owns or uses: data is collected for its own sake | An IR has no owner or "so that", or links to no outcome or KPI | Every IR names an owner, a purpose and the OIR/KPI it supports (Section 5) | Done (P03 Sections 4, 5) |
| **2. Write the EIR** | Appointing party IM | OIR → EIR in Word with atomic IDs | Compound or vague requirements; values buried in prose; cross-references to section numbers | One table cell holds several requirements; Verification is hard to assign | One requirement per row with its own ID; values in tables; cite IDs, not section numbers | Done (P03). Still cites section numbers in places |
| **3. Issue annexes and reference information** | Appointing party IM | EIR → data dictionary, code lists, IDS, rules, templates in the CDE at the same revision (REF-01 to REF-14) | Annexes drift from the EIR; Uniclass changes underneath the project | Annex revision ≠ EIR revision; codes fail against the pinned tables | CHK-01 (same revision); CLS-05/06 (pinned Uniclass); REF-15/16 | **Partial:** annexes still at the P01 level, not yet updated for P03 |

## Phase 2: Translate (appointing party IM)

| Step | Who | In → Out | What can go wrong | How you'd know | Control | Exercise status |
|---|---|---|---|---|---|---|
| **4. Word → data** | Appointing party IM (script) | EIR `.docx` → `clauses.csv` | Rows missed: no ID, merged cells, tracked changes not accepted | Record count differs from the expected count; an ID you know exists is missing | Editing rules (IDs in first column, no merged cells); accept changes first; check record counts every revision | Done (`docx_to_clauses.py`: 302 records from P03) |
| **5. Compare revisions** | Appointing party IM (script) | Old and new `clauses.csv` → change list with affected rules | False changes from renumbering; real changes missed in tables without IDs | P02→P03 showed both: 3 false changes, 1 missed change (naming types) | Cite IDs not sections; give every value row an ID or move it into a machine-readable annex | Done (`compare_clauses.py`); both weaknesses found |
| **6. Update dictionary, code lists and rules** | Appointing party IM with requirement owners | Change list → updated `data_dictionary.csv`, `code_lists.csv`, `rules.csv` | **The biggest risk in the chain:** a person interprets the requirement wrongly, a requirement gets no rule, or a rule checks something the EIR doesn't ask for | Register rows with only a planned rule; a rule citing no ID; owner disagrees with a rule's logic | Every rule cites an ID (CHK-02); register shows coverage; owners review the rules for their IRs; EIR prevails (CHK-05) | **Partial:** rules cover P01/P02; P03's new rules (INT, GEO, AIR-29, SEC-08, CLS-05, PRC) are not written |
| **7. Test the checker** | Appointing party IM | Rules + sample with known errors + clean sample → caught, missed and false-alarm counts | Missed errors (false negatives); false alarms; seeded errors too easy to be convincing | Score against `seeded_errors.csv`; any fail on the clean sample | CHK-04 before each use; seeded errors reviewed by owners; test on a real model as well | **Partial:** passed for P01 rules (13/13 caught, 0 false alarms); scoring write-up (Stage 5) and real-model test outstanding |

## Phase 3: Respond and produce (delivery team)

| Step | Who | In → Out | What can go wrong | How you'd know | Control | Exercise status |
|---|---|---|---|---|---|---|
| **8. Tender and BEP** | Lead appointed party | EIR → pre-appointment BEP; then confirmed BEP | The BEP proposes something the rules don't allow (e.g. Haystack instead of Brick tags) and nobody updates the rules | First submission fails on something the BEP agreed | Review the confirmed BEP against the rules before IE1; record agreed deviations as an EIR revision or a rules setting | Not started |
| **9. Produce and self-check (Check, Review, Approve)** | Task teams, task IMs, lead appointed party IM | Models, COBie, points schedule, documents → self-checked containers | Delivery team checks with a different tool or rules version; steps skipped under time pressure | No self-check report attached; CRAV record missing | Published rules and IDS (REF-12, REF-13); PRC-01 to PRC-03 | Simulated (generator script) |
| **10. Submit to the CDE** | Lead appointed party IM | Containers + register → submission | Wrong revision uploaded; register doesn't match the files | Name, status or revision fails; IFC and COBie don't match | Layer 1 and 2 rules; PRC-02 | Simulated |

## Phase 4: Verify (appointing party)

| Step | Who | In → Out | What can go wrong | How you'd know | Control | Exercise status |
|---|---|---|---|---|---|---|
| **11. Run the checks** | Appointing party IM (Colab notebook) | Submission + rules → results table | Environment differs (package versions, IFC reader); wrong check date or file paths; a broken rule silently skipped; slow on large models | `error` rows in the results; reader name printed at load; run time | Settings cell; rule errors reported, not hidden; seeded and clean tests (step 7); record run metadata | Done (Colab, ifcopenshell, about 4 s) |
| **12. Report and decide** | Appointing party IM and requirement owners | Results → decision (Section 18) and report | Automation trusted too much; flags ignored; decision logic coded wrongly; report says *what* failed but not *where* | Owners can't find the failing item; decision disagrees with a manual read | Assisted and Manual items to named people; decisions trace to ACC IDs; exact locations and BCF (next iteration) | **Partial:** report and decision done; exact locations and BCF not yet |
| **13. Feedback and resubmit** | Both | Rejected container with failed IDs → fixed resubmission | Fixes break something else; only the failed items are rechecked | New fails appear on resubmission | Full re-run every submission; PRC-07 lists failed requirement IDs | Not started |
| **14. Load to destination systems** | Asset information manager, Estates Digital Lead | Accepted COBie and points schedule → CAFM, data platform | Data passes every rule but fails the import (template mismatch); live data drops out after handover | Trial load rejects records; soak test below 95% | PRC-06 trial load; INT-11 soak test; INT-12 monthly reports | Not started (data layer workstream) |
| **15. Measure KPIs and benefits** | KPI owners | Check results, CAFM, live data → KPI values against targets | Baselines are guesses; KPIs have no owner; data pipeline not built | KPI shows "not measured" | Owners named in Section 19; replace estimate baselines; data pipeline | Not started (data layer workstream) |

---

## Where the risk concentrates

1. **Step 6, turning words into rules.** It's the only step where meaning is translated by a person, so errors here look like "correct" results later. The controls: every rule cites an ID, owners review the rules for their IRs, and step 7 tests catch what slips through.
2. **Steps 3 and 5, drift.** The document and its annexes are two copies of the truth. P02 → P03 showed both failure modes: false changes from renumbering, and a real change missed in a table without IDs.
3. **Steps 7 and 12, false confidence.** A clean report only means the rules found nothing. Seeded-error testing measures what the rules *can* catch, and the Assisted and Manual items keep a person in the loop.
4. **Step 8, the BEP.** Agreed deviations that never reach the rules cause disputes at the first exchange.
5. **Step 14, passing checks but failing in use.** The real test of asset data is the CAFM import and the live data, not the rules.

## Next steps in this exercise, in order

1. Bring the annexes up to P03 (step 3): data dictionary rows for AIR-29, the INT points schedule, GEO, and code list types `SU`, `PR`.
2. Write the new rules (step 6), starting with the points schedule (INT-02 to INT-09). It's a table, so it's the easiest new area to check, and it supports your integration focus.
3. Extend the sample data (step 7): a points schedule with seeded errors, georeferencing, LAC codes. Then do the Stage 5 scoring.
4. Then the programme (P6) and data layer workstreams.
