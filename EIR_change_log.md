# Change log: LRHC-LRV-ZZ-ZZ-SP-K-000001 (Exchange Information Requirements)

| Revision | Status | Date | Summary |
|---|---|---|---|
| P01 | S2 | 2026-11-16 | First issue: single building, AIR, naming, status, MIDP, acceptance criteria |
| P02 | S3 | 2026-11-19 | Campus context, OIR, 15 information requirements, LOIN, security, exchange date types |
| P03 | S3 | 2026-11-19 | Atomic requirement IDs; connected systems and data integration; KPIs and benefits; reference information and Uniclass version control; spatial coordination; CRAV; information management function; tender response requirements |
| **P04** | **S3** | **2026-11-19** | **Contractual mechanisms (NEC4 ECC Option C under P23): CON-01 to CON-18; lever for each acceptance criterion, MIDP item and KPI; KPI-01 defined per container** |

---

## P02 → P03

### Why

The P02 review raised five gaps, all of which are standard EIR content (UK BIM Framework templates and published client EIRs):
- spatial coordination;
- an authorisation and acceptance process;
- reference information and shared resources, with version control;
- unique IDs fine enough for automated feedback;
- connected systems and benefits.

P03 fills them. Every P02 clause ID is kept, so the checking rules still link up.

### Changes by section (P03 numbering)

| P03 section | Change | Type | P02 section |
|---|---|---|---|
| Front matter | New: how requirements are identified (three ID kinds); verification categories; **order of precedence** (EIR → annexes → BEP → other references; rules never add requirements) | Added | — |
| 1 Introduction | Rewritten as the top-down chain: outcomes → requirements → information standard → delivery and acceptance; the role of the BEP | Changed | 1 |
| 2 Campus and ABS | Unchanged | — | 2 |
| 3.2 Requirement owners | Added Estates Digital Lead | Changed | 3.2 |
| 3.3 Information management function | **New:** roles for both sides, including asset information manager, Estates Digital Lead and connected systems integration lead | Added | — |
| 4.1 Performance outcomes | Each outcome now has an ID (`OIR-ENV-01` …) and points to the KPI that measures it | Changed | 4.1 |
| 5 Information requirements | **Restructured:** each IR is now a table of atomic requirements with their own IDs (`IR-04.G.02`), verification method and what verifies it. Each IR states the outcomes and KPIs it supports. Content reworded where one P02 cell held several requirements. **IR-16 Connected systems and live data is new.** | Changed | 5 |
| 6 Connected systems and data integration | **New:** systems in scope with protocols, write-back and KPIs fed; data flow; INT-01 to INT-12 (points schedule, asset linking, naming, Brick tagging, open protocols, integration specification, units and time, read-only rule, fire alarm independence, commissioning and soak test, defects-period data quality) | Added | — |
| 7–9 LOIN, spaces, AIR | Unchanged apart from renumbering; pointer to AIR-29 | Moved | 6–8 |
| 10 Reference information | **New:** REF-01 to REF-16 (every resource with container ID and revision); the ICB's own classification (LAC) and its mapping to Uniclass; **AIR-29** LAC code on every asset type; **CLS-05 to CLS-07** Uniclass version pinning, adoption only at stage boundaries, code-only comparison | Added | — |
| 11 Spatial coordination | **New:** GEO-01 to GEO-07: British National Grid / OSGB36, metres AOD, survey point SP-01 (E 522 624.500, N 171 528.300), project north, IFC georeferencing, units, survey tolerance | Added | — |
| 12 Exchange formats | Unchanged | Moved | 9 |
| 13 Naming | Document types `SU` (survey) and `PR` (programme) added for the new reference containers | Changed | 10 |
| 14 Status codes | Unchanged | Moved | 11 |
| 15 Security | Building control networks added to the triage; **SEC-08** (network addresses and credentials kept out of COBie, models and general documents; checkable by pattern scan); **SEC-09** (connected device and network security, IEC 62443 principles) | Changed | 12 |
| 16 Exchange dates and MIDP | Five connected-systems containers added to the MIDP, using volume code `03` | Changed | 13 |
| 17 Authorisation and acceptance | **New:** CRAV (Check, Review, Approve, Verify) with who, what, status and record per step; PRC-01 to PRC-07; where accepted information goes (destination systems) | Added | — |
| 18 Acceptance criteria | **ACC-09** widened to include SEC-08. **ACC-10 new:** a connected system failing its tests isn't accepted | Changed | 14 |
| 19 KPIs and benefits | **New:** 8 delivery KPIs (information management), 7 outcome KPIs, 6 benefits mapped enabler → change → benefit → objective, and dis-benefits | Added | — |
| 20 What the lead appointed party submits | Points schedule, integration specification, test records, CRAV record added | Changed | 15 |
| 21 Tender response requirements | **New:** TND-01 to TND-06, with weightings | Added | — |
| Annex A | Register now has 135 atomic rows (125 requirements, 10 *none required*) | Changed | A |
| Annex B | Replaced by **Checking configuration:** CHK-01 to CHK-05 (rules published at the same revision, every rule cites an ID, change control, testing before use, EIR prevails), plus verification counts | Changed | B |
| Annex C | Open points updated: CRAV closed; four new points | Changed | C |

### Clause register

| Group | P02 | P03 | Change |
|---|---|---|---|
| PUR, FMT, LOC, STA, MID | unchanged | unchanged | none |
| CLS | 01–04 | 01–07 | **05–07 added** (Uniclass version control) |
| AIR | 01–28 | 01–29 | **29 added** (LAC code) |
| NAM | 01–07 | 01–07 | NAM-01 code list: `SU`, `PR` added |
| SEC | 01–07 | 01–09 | **08–09 added** |
| ACC | 01–09 | 01–10 | ACC-09 widened; **10 added** |
| IR | 15 × 6 components | 16 IRs, 135 atomic items | **restructured**; IR-16 added |
| OIR, KPI, BEN | — | 10, 15, 6 | **added** |
| INT, GEO, PRC, REF, CHK, TND | — | 12, 7, 7, 16, 5, 6 | **added** |

### Checkability

Verified by a rule (Auto), excluding supporting information:
- **P02:** 59%, counted over 71 components;
- **P03:** 70%, counted over 112 atomic requirements.

**The rise is mostly a measurement change, not new capability.** P02 cells often mixed a checkable item with a judgement item, and the whole cell was scored by its weaker part. Splitting cells into single requirements scores each one on its own. 28 of the 112 are covered by rules that exist today. The rest name a planned rule or a role.

### Effect on the checking rules and sample data

| Item | Effect |
|---|---|
| Existing rules | Still valid. P02 clause IDs and meanings are unchanged |
| Rules to write | INT-02 to INT-09 (points schedule), SEC-08 scan, AIR-29 (LAC mapping), GEO-04 (IFC georeferencing), CLS-05 (codes against pinned tables), PRC rules (need CDE metadata) |
| Sample data | Still passes the P02 checks. It has no points schedule, no georeferencing and no LAC codes yet, so the new rules will fail it until it's extended |
| Word round trip | Parser updated to read atomic IR IDs and the new clause groups. The P03 extract has 302 records (167 clauses, 135 IR items) |

### Found while checking P03

1. **Renumbering shows up as change.** Comparing P02 and P03 flagged AIR-27, AIR-28 and NAM-07 as changed only because their section cross-references were renumbered. Cross-references to section numbers inside requirement text create false changes. Better to cite IDs, not section numbers.
2. **Tables without IDs escape the round trip.** The naming code lists (e.g. the new `SU` and `PR` types) sit in a table with no clause ID per row, so the compare didn't see that change. Every row that carries a requirement value needs an ID, or the value must live in a machine-readable annex (REF-01).

---

## P03 → P04

### Why

P03 said what information is needed and how it's accepted, but not what happens contractually when it isn't. P04 adds that, for an assumed NEC4 ECC Option C contract under ProCure23. The aim is that every acceptance criterion, MIDP item and KPI has a named contract lever, or a stated reason it has none.

No requirement was removed or weakened. The new section is at the end of Part D, so no section was renumbered.

### Changes by section

| Section | Change | Type |
|---|---|---|
| Document control | P04 row added | Changed |
| How requirements are identified | `CON-nn` added to the clause examples | Changed |
| Contents | Section 22 added | Changed |
| 3.3 Information management function | Project Manager and Supervisor (NEC4) added | Changed |
| 17 CRAV | **PRC-05:** the 5-working-day decision is now also the contract's period for reply (CON-05) | Changed |
| 18 Acceptance criteria | Pointer to Section 22 for contract consequences | Changed |
| 19.1 Delivery KPIs | **KPI-01** measure now counts containers per exchange, defined in CON-13. Pointer to which KPIs are in the Incentive Schedule | Changed |
| 22 Contractual mechanisms (NEC4) | **New:** 22.1 assumed contract; 22.2 **CON-01 to CON-18**; 22.3 lever for each ACC, MID, PRC and KPI item; 22.4 what happens when information fails | Added |
| Annex C | Open points 17 to 20 added (contract form, information as part of the works, damages rate and correction period, Incentive Schedule amounts) | Changed |

### Clause register

| Group | P03 | P04 | Change |
|---|---|---|---|
| CON | — | 01–18 | **added** |
| PRC | 01–07 | 01–07 | PRC-05 text extended |
| KPI | 15 | 15 | KPI-01 measure redefined |
| All others | unchanged | unchanged | none |

### Decisions made in P04

1. **No KPI damages.** X20 stays positive only. Consequences for poor information come from the Scope: non-acceptance, Defects, Key Dates, Completion and the activity schedule (CON-18).
2. **Only four KPIs go in the Incentive Schedule:** KPI-01, KPI-03, KPI-07 and KPI-08. KPI-02 is already mandatory (ACC-03). KPI-04 and KPI-05 measure the ICB. KPI-06 depends partly on the ICB. Outcome KPIs depend on how the building is run.
3. **KPI-01 counts containers, not exchanges.** With four exchanges, a per-exchange figure could only be 0%, 25%, 50%, 75% or 100%.
4. **The ICB is bound too.** PRC-05 becomes the period for reply, so a late decision is a compensation event for the Contractor.

### Effect on the checking rules and sample data

| Item | Effect |
|---|---|
| Existing rules | Unchanged. No rule cites KPI-01 or PRC-05 |
| Rules to write | A decision log (container, exchange, submission number, decision, failed IDs, timestamps) is needed for CON-05 to CON-09, CON-11 and CON-13. The current checker writes a report, not a log |
| Word round trip | Parser updated to read `CON-nn`. P04 extract: 320 records (185 clauses, 135 IR items). Compare against P03: 2 changed, 18 added, 0 removed |

### Found while checking P04

1. **Changes without IDs were missed again.** The compare found the 20 clause changes but not the new rows in 3.3 (no IDs), the new Annex C rows or the document control row. Same weakness as in P03. This log was written by hand from the source diff.
2. **The contract section can't be fully checked by rules.** 7 of the 18 CON clauses are Manual, because they're about how the contract is drafted. The Auto ones depend on a decision log that doesn't exist yet.
