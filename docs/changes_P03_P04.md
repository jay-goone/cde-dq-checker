# Clause changes: clauses_P03.csv → clauses_P04.csv

**2 changed · 18 added · 0 removed** (of 320 records)

## KPI-01 (changed) · 19.1 Delivery KPIs (information management)
- **Measure**
  - was: Submissions accepted at the first attempt ÷ all submissions
  - now: Containers accepted at their first submission for an exchange ÷ all containers submitted (definition: CON-13)
- **Rules to review:** none · **Data dictionary rows:** none

## PRC-05 (changed) · 17. Authorisation and acceptance (CRAV)
- **Requirement**
  - was: The ICB decides (accept or reject) within 5 working days of a submission (KPI-04).
  - now: The ICB decides (accept or reject) within 5 working days of a submission (KPI-04). This is the contract's period for reply for information (CON-05).
- **Rules to review:** none · **Data dictionary rows:** none

## CON-01 (added) · 22.2 Contract requirements
- {"Requirement": "X10 is used. The Information Model Requirements in the Scope are this EIR and the annexes issued with it (REF-01, REF-12, REF-13), at the revision stated in Contract Data part one. They change only through an instruction changing the Scope, which is a compensation event (60.1(1)).", "Verification": "Manual"}
- **Needs a rule?** Existing rules citing it: none

## CON-02 (added) · 22.2 Contract requirements
- {"Requirement": "The Scope states that the information containers in the MIDP are part of the works. Information that doesn't meet the acceptance criteria (Section 18) is therefore a Defect (11.2(6)).", "Verification": "Manual"}
- **Needs a rule?** Existing rules citing it: none

## CON-03 (added) · 22.2 Contract requirements
- {"Requirement": "The confirmed BEP is the Information Execution Plan. If it isn't identified in Contract Data part two, the first one is submitted for acceptance within 2 weeks of the Contract Date. It's revised with each revised programme and before each exchange, and its MIDP dates match the Accepted Programme.", "Verification": "Auto (REG; MIDP against programme)"}
- **Needs a rule?** Existing rules citing it: none

## CON-04 (added) · 22.2 Contract requirements
- {"Requirement": "The Project Manager holds the client's information management actions under X10. Before IE1 the Project Manager notifies the Contractor (14.2) that these are delegated: acceptance of the Information Execution Plan and of information submissions to the appointing party information manager; acceptance of sensitive information to the Senior Security Risk Owner. The Supervisor witnesses the INT-11 tests and notifies Defects found in them.", "Verification": "Manual"}
- **Needs a rule?** Existing rules citing it: none

## CON-05 (added) · 22.2 Contract requirements
- {"Requirement": "The period for reply for information submissions is 1 week, matching PRC-05 and KPI-04. A late reply is a compensation event (60.1(6)).", "Verification": "Auto (CDE timestamps)"}
- **Needs a rule?** Existing rules citing it: none

## CON-06 (added) · 22.2 Contract requirements
- {"Requirement": "A rejection under Section 18 is the Project Manager's non-acceptance (13.4). The reason given is that the information doesn't comply with the Scope, and the check report lists every failed requirement ID (PRC-07).", "Verification": "Auto (check report)"}
- **Needs a rule?** Existing rules citing it: none

## CON-07 (added) · 22.2 Contract requirements
- {"Requirement": "Rejected information, and each item on an ACC-06 correction list, is a notified Defect. The defect correction period for information is 2 weeks (project target). If a Defect isn't corrected in time, the Project Manager assesses the cost of having it corrected by others and the Contractor pays it (46.1). Under Option C, correcting Defects after Completion is Disallowed Cost.", "Verification": "Auto (REG: resubmission date against notification)"}
- **Needs a rule?** Existing rules citing it: none

## CON-08 (added) · 22.2 Contract requirements
- {"Requirement": "Two Key Dates are set. KD-1: IE1 information accepted with no rejection under ACC-01 to ACC-05, by the planned date of M-203-S4. KD-2: the same for IE2, by M-203-IE2. If a Condition isn't met by its Key Date, the Contractor pays the additional cost the Client incurs on the project (25.3).", "Verification": "Auto (decision log against Key Dates)"}
- **Needs a rule?** Existing rules citing it: none

## CON-09 (added) · 22.2 Contract requirements
- {"Requirement": "The Scope states that Completion requires: IE3 information accepted with no rejection under ACC-01 to ACC-05, ACC-09 or ACC-10; the CAFM and data platform trial loads passed (PRC-06); and the connected system tests passed (INT-11).", "Verification": "Auto (decision log; load logs; test records)"}
- **Needs a rule?** Existing rules citing it: none

## CON-10 (added) · 22.2 Contract requirements
- {"Requirement": "X7 is used at the rate in Contract Data part one (set by the ICB's commercial team; not stated in this exercise). Because of CON-09, late or rejected handover information delays Completion and delay damages run.", "Verification": "Manual"}
- **Needs a rule?** Existing rules citing it: none

## CON-11 (added) · 22.2 Contract requirements
- {"Requirement": "The activity schedule has one information management activity per exchange (IE1 to IE4). Each is complete only when its exchange is accepted. IE4 comes after Completion, so this is the main lever for record information.", "Verification": "Auto (decision log)"}
- **Needs a rule?** Existing rules citing it: none

## CON-12 (added) · 22.2 Contract requirements
- {"Requirement": "The Incentive Schedule (X20) holds KPI-01, KPI-03, KPI-07 and KPI-08. The other KPIs stay out of it, for the reasons in 22.3.", "Verification": "Manual"}
- **Needs a rule?** Existing rules citing it: none

## CON-13 (added) · 22.2 Contract requirements
- {"Requirement": "KPI-01 is measured per container. A container counts once per exchange (IE2 to IE4). It counts as first-time accepted if its first submission for that exchange is accepted, including acceptance with a correction list (ACC-06). Warnings and flags never count against it. A rejection overturned under CON-14 is removed. Security rejections (ACC-09) count. The figure comes from the checker decision log and CDE timestamps, and is reported monthly with a forecast of the final result.", "Verification": "Auto (decision log)"}
- **Needs a rule?** Existing rules citing it: none

## CON-14 (added) · 22.2 Contract requirements
- {"Requirement": "The Contractor may notify, within 5 working days of a rejection, that it believes the rejection is wrong. The Project Manager (or delegate) decides within 5 working days. If the Contractor is right, the rule is corrected (CHK-05) and the rejection is removed from KPI-01. A disagreement goes through the contract's dispute resolution procedure.", "Verification": "Assisted"}
- **Needs a rule?** Existing rules citing it: none

## CON-15 (added) · 22.2 Contract requirements
- {"Requirement": "The Contractor has the same checking rules and checker version as the ICB throughout (CHK-01, PRC-02). Each check report states the rules revision used. A change to the rules comes only with a revision of this EIR, so it's a change to the Scope.", "Verification": "Auto (rules revision in check report)"}
- **Needs a rule?** Existing rules citing it: none

## CON-16 (added) · 22.2 Contract requirements
- {"Requirement": "Either party gives an early warning (15.1) of anything that could delay an exchange, stop an X20 KPI reaching its target or impair the information in use. Early warning register entries cite the requirement IDs affected. If the forecast for an X20 KPI misses its target, the Contractor submits proposals for improving performance (X20.3) and revises the Information Execution Plan to match.", "Verification": "Assisted"}
- **Needs a rule?** Existing rules citing it: none

## CON-17 (added) · 22.2 Contract requirements
- {"Requirement": "If the same requirement ID fails at two submissions in a row after a Defect has been notified, it's discussed at the next early warning meeting and the actions are recorded. If the failure continues, the Project Manager may, after advice, notify a default for substantial failure to comply (91.2, R11). The Contractor then has 4 weeks to put it right.", "Verification": "Manual"}
- **Needs a rule?** Existing rules citing it: none

## CON-18 (added) · 22.2 Contract requirements
- {"Requirement": "Option Z is kept to a minimum. It's used only to align X10 terms with BS EN ISO 19650 where needed. KPI damages are not used: consequences come from CON-02 to CON-11.", "Verification": "Manual"}
- **Needs a rule?** Existing rules citing it: none
