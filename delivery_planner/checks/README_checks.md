# Check catalogue

25 checks in five groups. Each check reads the standard tables (never the raw files), yields one issue per problem,
and is mapped to a DAMA DMBOK2 data quality dimension. Severity: **error** = the delivery is wrong or the data can't be trusted;
**warning** = a planning signal to act on.

Every check has at least one fault in `faults/catalogue.py` aimed at it. The perfect data gives 0 issues; all 28 faults are caught with 0 false alarms.

| Check | What it tests | Dimension | Severity | File | Faults aimed at it |
|---|---|---|---|---|---|
| R01 | MIDP codes are in the reference library and approved | Validity | error | `checks/reference.py` | F01 MIDP asks for suitability S5, which is not a code, F02 MIDP number has 5 digits, F03 Client has not approved zone Z4 (still 'proposed') |
| R02 | CDE attribute codes are in the reference library and approved | Validity | error | `checks/reference.py` | F03 Client has not approved zone Z4 (still 'proposed'), F04 CDE version carries suitability S5 |
| R03 | Codes used in the CDE only after the client approved them | Validity | error | `checks/reference.py` | F05 Zone Z3 used on 2 Dec, before the client approved it on 4 Dec |
| R04 | MIDP container name matches its own fields | Consistency | error | `checks/reference.py` | F06 MIDP volume says Z1 but the container name says ZZ |
| P01 | MIDP row links to an activity that exists in the programme | Integrity | error | `checks/programme.py` | F07 MIDP links to an activity that does not exist |
| P02 | MIDP stage matches the stage of the linked activity | Consistency | error | `checks/programme.py` | F08 MIDP says Stage 5 for a Stage 4 deliverable |
| P03 | Linked activity finishes on or before its exchange milestone | Reasonability | error | `checks/programme.py` | F09 MIDP links an IE1 deliverable to an activity after IE1 |
| C01 | Due deliverables are in the CDE | Completeness | error | `checks/completeness.py` | F10 A due deliverable is missing from the CDE |
| C02 | Every container in the CDE is planned in the MIDP | Integrity | error | `checks/completeness.py` | F11 An unplanned container appears in the CDE |
| C03 | No duplicate MIDP rows | Uniqueness | error | `checks/completeness.py` | F12 MIDP row entered twice |
| C04 | Required MIDP fields are filled | Completeness | error | `checks/completeness.py` | F13 MIDP title left blank |
| C05 | Required CDE fields are filled | Completeness | error | `checks/completeness.py` | F14 CDE version has no 'Updated By' |
| C06 | No duplicate CDE version records | Uniqueness | error | `checks/completeness.py` | F15 Same CDE version exported twice |
| T01 | Delivered by the baseline due date | Timeliness | error | `checks/timeliness.py` | F16 Delivered 2 weeks late (no change to the programme), F17 Issued at S2 when the MIDP asks for S3, F18 Issue activity slipped 5 days and the delivery followed it |
| T02 | Delivered by the current forecast due date | Timeliness | warning | `checks/timeliness.py` | F16 Delivered 2 weeks late (no change to the programme), F17 Issued at S2 when the MIDP asks for S3 |
| T03 | Early warning: forecast due date has slipped past the baseline | Timeliness | warning | `checks/timeliness.py` | F19 Programme forecast for the O&M manual slipped 10 days |
| T04 | CDE export is current at the data date | Timeliness | error | `checks/timeliness.py` | F20 CDE export is a week old |
| M01 | CDE container name matches its attribute fields | Consistency | error | `checks/metadata.py` | F21 Originator attribute says FLD on a CKE container |
| M02 | File name matches the container name | Accuracy | error | `checks/metadata.py` | F22 File name carries the revision |
| M03 | CDE description and title attribute agree | Accuracy | error | `checks/metadata.py` | F23 Description and title attribute disagree on one version |
| M04 | CDE title matches the MIDP title | Consistency | error | `checks/metadata.py` | F24 CDE title differs from the MIDP title |
| M05 | Revision type matches suitability (S → P, A/CR → C) | Consistency | error | `checks/metadata.py` | F25 A4 version given a P revision |
| M06 | Workflow state matches suitability (Shared for S, Published for A/CR) | Consistency | error | `checks/metadata.py` | F26 S4 version left in the Published state |
| M07 | Revisions run in order with no gaps, and dates go forward | Reasonability | error | `checks/metadata.py` | F27 Revision jumps from P01 to P03 |
| M08 | Status dates fall between project start and the data date | Reasonability | error | `checks/metadata.py` | F28 Status date after the data date |

## Coverage by DAMA dimension

| Dimension | Checks |
|---|---|
| Accuracy | M02, M03 |
| Completeness | C01, C04, C05 |
| Consistency | R04, P02, M01, M04, M05, M06 |
| Integrity | P01, C02 |
| Reasonability | P03, M07, M08 |
| Timeliness | T01, T02, T03, T04 |
| Uniqueness | C03, C06 |
| Validity | R01, R02, R03 |

**Accuracy is partial.** Metadata can't prove what is inside a file. M02 and M03 only test whether two independent records of the same fact agree (file name vs container name; description vs title attribute).

## Rules the checks follow

- **Due dates come from the programme, never the MIDP.** Baseline due = finish of the linked activity in the baseline; forecast due = its finish in the current update.
- **'Delivered' means the first version at the required suitability or better** (S0 < S1 < … < S4 < A1–A7 < CR), so an A4 counts for an S4 requirement.
- **One fault, one check.** Checks skip what another check owns: a blank field is C04/C05 only; a deliverable with nothing in the CDE is C01 only (not T01); an unknown code is R01/R02 only.
- **Late against baseline is an error (contractual); late against forecast is a warning (planning).** T03 warns before a deliverable is due if its forecast has slipped.
