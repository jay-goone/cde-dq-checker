# Exchange Information Requirements (EIR)
**Programme:** MA 4920 Larch Valley Health Campus
**Appointment:** MA 4920.203 Larch Road Health Centre (project code **LRHC**)
**Container:** LRHC-LRV-ZZ-ZZ-SP-K-000001 · **Status:** S3 (suitable for review and comment) · **Revision:** P04 · **Date:** 2026-11-19
**Standards:** BS EN ISO 19650-1, -2 (with UK National Annex), -3, -5 · BS EN ISO 7817-1 (level of information need)

> Fictional project made for a test exercise. All organisations, targets and baselines are invented. Values marked *project target* or *estimate* are set for this exercise, not taken from guidance.

## Document control

| Revision | Status | Date | Author | Description |
|---|---|---|---|---|
| P01 | S2 | 2026-11-16 | LRV Information Manager | First issue for information: single building, asset information requirements, naming, status, MIDP, acceptance criteria |
| P02 | S3 | 2026-11-19 | LRV Information Manager | Campus context (MA 4920), OIR, 15 information requirements, level of information need, security, exchange date types |
| P03 | S3 | 2026-11-19 | LRV Information Manager | Atomic requirement IDs; connected systems and data integration; KPIs and benefits; reference information and Uniclass version control; spatial coordination; CRAV acceptance process; information management function; tender response requirements. Full list of changes in the change log |
| P04 | S3 | 2026-11-19 | LRV Information Manager | Contractual mechanisms (NEC4 ECC Option C under P23): CON-01 to CON-18, lever for each acceptance criterion, MIDP item and KPI; KPI-01 measure defined per container; Project Manager and Supervisor added to the information management function |

### How requirements are identified

Every requirement has an ID that never changes between revisions. A retired ID is never reused. There are three kinds:

| Kind | Form | Example | Used for |
|---|---|---|---|
| Information requirement tree | `IR-nn` → `IR-nn.<component>` → `IR-nn.<component>.nn` | `IR-04.G.02` = space management, graphical, second requirement | The 16 information requirements (Section 5). Components: G graphical, NG non-graphical, D documentation, AC acceptance criteria, SI supporting information, EX exchange date |
| Outcome and measure | `OIR-xxx-nn`, `KPI-nn`, `BEN-nn` | `OIR-SOC-03`, `KPI-16`, `BEN-05` | Outcomes (Section 4), KPIs and benefits (Section 19) |
| Information standard clause | `XXX-nn` | `AIR-07`, `NAM-01`, `INT-03`, `GEO-04`, `PRC-05`, `CON-07` | The detailed rules every requirement relies on (Sections 6 to 22) |

Each requirement's **Verification** says how acceptance is decided:
- **Auto:** a checking rule passes or fails it.
- **Assisted:** a rule finds candidates or checks form, and a named person decides.
- **Manual:** professional judgement, site inspection or a third party.

The **Checked in** column says where a check looks: IFC (model), COBie (spreadsheet), REG (document register), points schedule or live data.

### Order of precedence

If anything conflicts, this order applies:
1. This EIR
2. The machine-readable annexes issued with it at the same revision (REF-01, REF-12, REF-13)
3. The confirmed BEP
4. Other reference information

Checking rules implement this EIR. They never add requirements to it.

**Contents**
- **Part A, context and purpose:** 1 Introduction · 2 Campus and asset breakdown structure · 3 Parties, requirement owners and information management function · 4 Organisational information requirements
- **Part B, what information is needed:** 5 Information requirements · 6 Connected systems and data integration · 7 Level of information need · 8 Spaces and assets in scope · 9 Asset information requirements
- **Part C, how it's produced:** 10 Reference information and shared resources · 11 Spatial coordination · 12 Exchange formats · 13 Naming · 14 Status codes and revisions · 15 Security
- **Part D, delivery, acceptance and benefits:** 16 Exchange dates, milestones and MIDP · 17 Authorisation and acceptance (CRAV) · 18 Acceptance criteria · 19 KPIs and benefits · 20 What the lead appointed party submits · 21 Tender response requirements · 22 Contractual mechanisms (NEC4)
- **Annexes:** A Requirements register · B Checking configuration · C Open points

---

# Part A: Context and purpose

## 1. Introduction

This EIR sets out the information Larch Valley ICB (the appointing party) needs from the lead appointed party for **MA 4920.203 Larch Road Health Centre**, a single-storey GP practice and clinic with paediatric care. It's one of seven entities on the **MA 4920 Larch Valley Health Campus**. Campus-wide requirements are included where they bind this appointment: security, the substation that feeds the campus, programme milestones and the ICB data platform.

The EIR works top-down:
1. The ICB's outcomes (Section 4)
2. The information requirements that serve them (Section 5), each with an owner, a level of information need, acceptance criteria, supporting information and an exchange date
3. The information standard every requirement relies on (Sections 6 to 15)
4. How information is delivered, accepted and measured (Sections 16 to 21)

The pre-appointment BEP responds to this EIR, and Section 21 lists what it must cover. Once the appointment is made, the confirmed BEP, this EIR, the MIDP and the information protocol together form the information management part of the appointment.

---

## 2. The campus and its asset breakdown structure

| ABS level | Meaning | MA 4920 example |
|---|---|---|
| Complex | The whole campus | **MA 4920** Larch Valley Health Campus |
| Entity | A building or site-wide facility | **MA 4920.203** Larch Road Health Centre (this appointment) |
| Space | A room or zone | 00-010 Paediatric clinic room |
| System | Services serving the entity | Ventilation, domestic hot water, nurse call, lighting |
| Element / product | Maintainable assets and products | AHU, TMV, fire doorset, washbasin |

**Entities on the campus**

| Code | Entity | Volume code | Notes |
|---|---|---|---|
| MA 4920.200 | Site-wide infrastructure (roads, drainage, utilities, landscaping) | 00 | Enabling works; serves all entities |
| MA 4920.201 | Diagnostic and treatment centre (2 storeys) | 01 | Largest building; depends on .204 for power |
| MA 4920.202 | Pharmacy and medical stores | 02 | **Sensitive:** controlled drugs store |
| MA 4920.203 | **Larch Road Health Centre (GP practice and clinic)** | 03 | This appointment |
| MA 4920.204 | 11 kV primary substation and standby generation | 04 | **Sensitive:** feeds every building; adopted by the DNO |
| MA 4920.205 | Clinical waste treatment plant | 05 | **Sensitive:** hazardous process; environmental permit |
| MA 4920.206 | Administration and staff building | 06 | |
| MA 4920.207 | Multi-storey car park | 07 | |

**Volume codes:** the *volume* field (2 characters) of a container name carries the entity: `00` site-wide, `01` to `07` for .201 to .207, `ZZ` all. For example, `LRHC-KBS-03-00-M3-M-000002`. That lets a rule tell which building a container belongs to, which the security rules need. Details in Section 13.1.

---

## 3. Parties, requirement owners and information management function

### 3.1 Parties to this appointment

| Role (UK NA term) | Organisation | Originator code |
|---|---|---|
| Appointing party | Larch Valley ICB, Estates team | LRV |
| Lead appointed party | Brook & Mason Construction Ltd (main contractor) | BMC |
| Appointed party (architect) | Field Architects | FLD |
| Appointed party (building services) | Kestrel Building Services | KBS |

**Facility:** single-storey GP practice and clinic with paediatric care, entity MA 4920.203 on the MA 4920 campus. 19 spaces and 47 maintainable assets (see Section 8).

### 3.2 Requirement owners

| Organisation | Team | Roles that own requirements |
|---|---|---|
| Larch Valley ICB (appointing party) | Estates and Facilities | Responsible Person (Water); Fire Safety Manager; Maintenance Manager; Space Planner; Energy and Sustainability Manager; Environmental Compliance Manager; Equality and Access Lead |
| Larch Valley ICB | Finance | Capital Accountant |
| Larch Valley ICB | Programme | Project Sponsor (MA 4920.203); Programme Sponsor (MA 4920) |
| Larch Valley ICB | Resilience and Security | Business Continuity Manager; Senior Security Risk Owner |
| Larch Valley ICB | Estates Digital | Estates Digital Lead (IR-16) |
| Larch Valley ICB | Clinical | Infection Prevention and Control Lead |
| Distribution Network Operator (third party) | Adoptions | Adoptions Engineer |
| Environment Agency (third party, regulator) | Permitting | Receives permit returns; doesn't own an EIR requirement but sets acceptance criteria for IR-13 |

### 3.3 Information management function

| Role | Organisation | Responsible for |
|---|---|---|
| Appointing party information manager | Larch Valley ICB | This EIR; reference information (Section 10); Verify step of CRAV (Section 17); KPI-01 to KPI-07 |
| Asset information manager | Larch Valley ICB | CAFM and asset register; trial loads (PRC-06); the ICB classification mapping (REF-03) |
| Estates Digital Lead | Larch Valley ICB | ICB data platform; IR-16 acceptance; witnessing INT-11(b) |
| Senior Security Risk Owner | Larch Valley ICB | Section 15; approving sharing of sensitive information |
| Lead appointed party information manager | Brook & Mason Construction | BEP; MIDP; Approve step of CRAV for submissions; self-check reports |
| Task information managers | Each task team (Field Architects, Kestrel Building Services) | Check, Review and Approve steps within the task team; TIDPs |
| Connected systems integration lead | Lead appointed party (may be a specialist) | Points schedule, integration specification, commissioning of data (Section 6) |
| Project Manager (NEC4) | Appointed by the ICB | Holds the client's information management actions under X10; delegates acceptance of information to the appointing party information manager (CON-04) |
| Supervisor (NEC4) | Appointed by the ICB | Witnesses connected system tests (INT-11); notifies Defects found in them (CON-04) |

---

## 4. Organisational information requirements (OIR)

### 4.1 Performance outcomes

| ID | Theme | Outcome | Measure | Project target | Information that proves it |
|---|---|---|---|---|---|
| OIR-ENV-01 | Environment | Energy use | Operational energy, kWh per m² per year | ≤ 110 (*project target*) | IR-06, IR-16 → KPI-11 |
| OIR-ENV-02 | Environment | Carbon | Fossil fuel used for heating on site | None: all-electric (*project target*) | IR-06 meter register |
| OIR-ENV-03 | Environment | Water | m³ per m² per year | ≤ 0.6 (*project target*) | IR-06, IR-16 → KPI-12 |
| OIR-ENV-04 | Environment | Waste | Clinical waste treated on campus | ≥ 90% by weight (*project target*) | IR-13 |
| OIR-SOC-01 | Social | Availability | Clinical rooms available in session hours | ≥ 98% (*project target*) | IR-03 → KPI-13 |
| OIR-SOC-02 | Social | Utilisation | Session hours rooms are occupied | ≥ 75% (*project target*) | IR-04, IR-16 → KPI-14 |
| OIR-SOC-03 | Social | Reliability and safety | Safety-critical PPM overdue | 0 (*project target*) | IR-01, IR-02, IR-03 → KPI-15, KPI-16 |
| OIR-SOC-04 | Social | Resilience | Clinical buildings served by two independent supplies | 100% (*project target*) | IR-07, IR-12 |
| OIR-ECO-01 | Economic | Capital cost | Final account vs approved budget | ≤ 100% | IR-05, IR-10 |
| OIR-ECO-02 | Economic | Operating cost | Facilities cost, £ per m² per year | ≤ business case budget | IR-05 → KPI-17 |

### 4.2 When the information is needed

| Phase | Stage | What the information is used for | Requirements |
|---|---|---|---|
| Delivery | Design (RIBA 2–3) | Test the operational strategy; check operational plans and assumptions | IR-04, IR-06, IR-08, IR-11 |
| Delivery | Technical design (RIBA 4) | Review how specified products will perform; refine design and construction approach | IR-01, IR-02, IR-04, IR-08, IR-09, IR-10 |
| Delivery | Construction (RIBA 5) | Plan commissioning and handover; verify commissioning performance; prepare for start-up | IR-01 to IR-03, IR-10, IR-12, IR-14 |
| Operation | Year 1 | Monitor and evaluate performance; find and fix any shortfall | IR-03, IR-06, IR-13 |
| Operation | Year 2 | Monitor performance; delivery team explains any dip | IR-06, IR-15 |
| Operation | Lessons learned | Capture changes and share with later campus buildings | IR-15 |

### 4.3 Information purposes

| ID | Purpose | What the estates team will do with the information |
|---|---|---|
| PUR-01 | **Operation and maintenance (O)** | Load assets and planned maintenance into the CAFM system on day one. Raise reactive jobs against the right asset and location. Track warranties. |
| PUR-02 | **Compliance (C)** | Plan statutory and safety testing: fire doors, fire dampers, thermostatic mixing valves (scald risk), nurse call and emergency assistance call, emergency lighting. |
| PUR-03 | **Space management (S)** | Hold a correct room list with classification, area and patient-area flag for planning, cleaning and infection control. |

Every attribute in Section 9 is tagged with the purpose(s) it serves.

---

# Part B: What information is needed

## 5. Information requirements

Each requirement has six components, broken into atomic requirements with their own IDs (see *How requirements are identified*). The **Verification** column says how each is accepted:
- **Auto:** a rule passes or fails it with no judgement.
- **Assisted:** a rule finds candidates or checks form, and a person decides.
- **Manual:** it needs professional judgement or site inspection, or it sits outside the information model.

**Verified by** names the checking rule (Annex B), a planned rule in brackets, or the role that decides. The full register is Annex A.

### IR-01 Scald protection (TMVs)

**Requirement owner:** ICB Estates – Responsible Person (Water)  
**Requirement description:** As the Responsible Person (Water), I need to test and maintain every thermostatic mixing valve that serves a patient basin, so that patients, especially children, are not scalded and the water safety plan can be audited.  
**Supports:** OIR-SOC-03 · KPI-02, KPI-15, KPI-16

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-01.G.01 | LOIN – graphical | Each TMV is modelled as a symbolic object inside its room, within 1 m of the basin it serves. | Auto | (geometry rule) |
| IR-01.NG.01 | LOIN – non-graphical | Each TMV carries the attributes in AIR-08 to AIR-23. | Auto | L1-04, L1-08 |
| IR-01.NG.02 | LOIN – non-graphical | Each basin in a patient area is served by exactly one TMV in the same room. | Auto | L3-13 |
| IR-01.D.01 | LOIN – documentation | One commissioning certificate per TMV, linked to that TMV in the COBie Document sheet. | Auto | (document link rule) |
| IR-01.D.02 | LOIN – documentation | Each certificate records the measured outlet temperature at commissioning. | Assisted | RP (Water); layer 4 flag |
| IR-01.AC.01 | Acceptance criteria | TMV3 approval and a 41 °C set point at washbasins. | Auto | L1-08 |
| IR-01.AC.02 | Acceptance criteria | Water temperature monitoring at each TMV outlet is live and linked to the TMV (IR-16). | Auto | (INT rules) |
| IR-01.SI.01 | Supporting information | ICB water safety plan template (REF-06). | Auto | appointing party issues before tender |
| IR-01.SI.02 | Supporting information | HTM 04-01 (reference standard). | Manual | designer |
| IR-01.EX.01 | Exchange date | At M-203-PC. | Auto | L2-02 |
| IR-01.EX.02 | Exchange date | In operation: within 10 working days of any TMV replacement (trigger). | Auto | (CAFM event rule) |

### IR-02 Fire safety (doors and dampers)

**Requirement owner:** ICB Estates – Fire Safety Manager  
**Requirement description:** As the Fire Safety Manager, I need to inspect and maintain every fire door and fire damper on the compartment lines, so that the fire strategy works as designed and the fire risk assessment stays valid.  
**Supports:** OIR-SOC-03 · KPI-02, KPI-15

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-02.G.01 | LOIN – graphical | Each fire door and damper sits in a wall between two spaces. | Auto | (geometry rule) |
| IR-02.G.02 | LOIN – graphical | That wall is a compartment line in the fire strategy. | Assisted | Fire Safety Manager |
| IR-02.NG.01 | LOIN – non-graphical | Fire rating, certification number, actuation type and PPM interval (AIR-20 to AIR-22). | Auto | L1-04, L1-08, L1-22 |
| IR-02.D.01 | LOIN – documentation | Fire strategy report and plans. | Assisted | Fire Safety Manager |
| IR-02.D.02 | LOIN – documentation | Damper drop-test record and doorset certificate per asset, linked to the asset. | Auto | (document link rule) |
| IR-02.AC.01 | Acceptance criteria | Data conforms to the data dictionary. | Auto | layer 1 rules |
| IR-02.AC.02 | Acceptance criteria | Design complies with HTM 05-02 and BS 9999. | Manual | fire engineer |
| IR-02.SI.01 | Supporting information | Existing MA 4920 site fire plan (REF-05). | Auto | appointing party issues before tender |
| IR-02.EX.01 | Exchange date | At M-203-PC. | Auto | L2-02 |
| IR-02.EX.02 | Exchange date | In operation: inspection records every 6 months. | Auto | (frequency rule) |

### IR-03 Planned maintenance in CAFM

**Requirement owner:** ICB Estates – Maintenance Manager  
**Requirement description:** As the Maintenance Manager, I need every maintainable asset and its PPM schedule loaded into CAFM before the building opens, so that nothing is missed in the first year and clinical rooms stay available.  
**Supports:** OIR-SOC-01, OIR-SOC-03 · KPI-06, KPI-07, KPI-13

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-03.G.01 | LOIN – graphical | Each maintainable asset is in exactly one room. | Auto | L3-04 |
| IR-03.NG.01 | LOIN – non-graphical | Asset register fields AIR-01 to AIR-19, plus the ICB classification code (AIR-29). | Auto | L1-04, L1-05, (AIR-29 rule) |
| IR-03.NG.02 | LOIN – non-graphical | The same assets, with the same GUIDs, in IFC and COBie. | Auto | L3-01, L3-02, L3-03 |
| IR-03.NG.03 | LOIN – non-graphical | A PPM job for every maintainable type, within the maximum interval. | Auto | L3-16, L1-22 |
| IR-03.D.01 | LOIN – documentation | An O&M manual section linked to every asset type. | Auto | (document link rule) |
| IR-03.D.02 | LOIN – documentation | The O&M content is correct for the installed product. | Assisted | Maintenance Manager |
| IR-03.AC.01 | Acceptance criteria | A trial load into the CAFM test environment completes with no rejected records (PRC-06). | Auto | CAFM load log |
| IR-03.SI.01 | Supporting information | CAFM import template (REF-08); SFG20 schedule list. | Auto | appointing party issues before tender |
| IR-03.EX.01 | Exchange date | Draft at M-203-IE2; final at M-203-PC. | Auto | L2-01, L2-02 |
| IR-03.EX.02 | Exchange date | Quarterly updates during the 12-month defects period. | Auto | (frequency rule) |

### IR-04 Space management

**Requirement owner:** ICB Estates – Space Planner  
**Requirement description:** As the Space Planner, I need an accurate room list with areas, classification and patient-area flags, so that I can plan clinical sessions, cleaning and infection control, and report space use to the ICB.  
**Supports:** OIR-SOC-02 · KPI-14

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-04.G.01 | LOIN – graphical | Space boundaries modelled to ±50 mm. | Assisted | survey comparison |
| IR-04.G.02 | LOIN – graphical | Net area from the space geometry is within 2% of the stated NetArea. | Auto | (geometry rule) |
| IR-04.NG.01 | LOIN – non-graphical | Room name, SL code, net area and patient-area flag match the space schedule. | Auto | L1-17, L1-18, L1-19, L3-05 |
| IR-04.D.01 | LOIN – documentation | One room data sheet per space. | Auto | (document link rule) |
| IR-04.D.02 | LOIN – documentation | Room data sheet content is complete. | Assisted | Space Planner |
| IR-04.AC.01 | Acceptance criteria | Space schedule in Section 8.1. | Auto | L3-05 |
| IR-04.AC.02 | Acceptance criteria | HBN 11-01 space standards are met. | Manual | architect |
| IR-04.SI.01 | Supporting information | Schedule of accommodation; room data sheet template (REF-07). | Auto | appointing party issues before tender |
| IR-04.EX.01 | Exchange date | At M-203-S4 (design) and M-203-PC (as built). | Auto | L2-02 |

### IR-05 Capital asset register

**Requirement owner:** ICB Finance – Capital Accountant  
**Requirement description:** As the Capital Accountant, I need the replacement cost and expected life of each asset, so that I can set up depreciation and plan lifecycle replacement funding.  
**Supports:** OIR-ECO-01, OIR-ECO-02 · KPI-17

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-05.G.00 | LOIN – graphical | None required. | – | – |
| IR-05.NG.01 | LOIN – non-graphical | Replacement cost (GBP) and expected life (years) for every asset type. | Auto | L1-04, L1-09 |
| IR-05.D.01 | LOIN – documentation | Cost reconciliation against the final account. | Manual | Capital Accountant |
| IR-05.AC.01 | Acceptance criteria | Replacement cost within 10% of the final account line for the same asset type. | Assisted | rule compares if the final account is supplied as data |
| IR-05.SI.01 | Supporting information | ICB asset valuation guidance. | Auto | appointing party issues before tender |
| IR-05.EX.01 | Exchange date | At M-203-REC, with the final account. | Auto | L2-02 |

### IR-06 Energy and water performance

**Requirement owner:** ICB Estates – Energy and Sustainability Manager  
**Requirement description:** As the Energy and Sustainability Manager, I need metered energy and water data against the design targets, so that I can show the building meets its operational targets in year 1 and explain any shortfall in year 2.  
**Supports:** OIR-ENV-01, OIR-ENV-02, OIR-ENV-03 · KPI-08, KPI-11, KPI-12

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-06.G.01 | LOIN – graphical | Each meter is located in a room. | Auto | L3-04 |
| IR-06.NG.01 | LOIN – non-graphical | Meter register: what each meter measures, units and point ID (via the points schedule, INT-02). | Auto | (INT rules) |
| IR-06.D.01 | LOIN – documentation | Energy model report and metering strategy. | Assisted | Energy Manager |
| IR-06.D.02 | LOIN – documentation | Year 1 and year 2 performance reports. | Assisted | Energy Manager |
| IR-06.AC.01 | Acceptance criteria | Meter data at least 95% complete each month. | Auto | data platform check |
| IR-06.AC.02 | Acceptance criteria | Measured performance against the OIR targets. | Auto | KPI-11, KPI-12 calculation |
| IR-06.SI.01 | Supporting information | Design energy targets; NHS Net Zero Building Standard; point naming standard (REF-09). | Auto | appointing party issues before tender |
| IR-06.EX.01 | Exchange date | Monthly meter data from handover. | Auto | (frequency rule) |
| IR-06.EX.02 | Exchange date | Performance reports at handover + 12 and + 24 months. | Auto | (milestone rule) |

### IR-07 Business continuity

**Requirement owner:** ICB – Business Continuity Manager  
**Requirement description:** As the Business Continuity Manager, I need details of all emergency plans and escape routes, so that I can prepare, maintain and implement the business continuity plan.  
**Supports:** OIR-SOC-04

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-07.G.01 | LOIN – graphical | Escape routes and assembly points on plans. | Manual | Business Continuity Manager |
| IR-07.NG.01 | LOIN – non-graphical | A critical-services link for every critical asset (which service it supports, which supply feeds it). | Assisted | rule checks the link exists; manager checks it's right |
| IR-07.D.01 | LOIN – documentation | Emergency plan and escape route document using the ICB template headings. | Assisted | rule checks headings; manager checks content |
| IR-07.AC.01 | Acceptance criteria | ICB emergency plan template (REF-10). | Assisted | template structure check |
| IR-07.SI.01 | Supporting information | Existing MA 4920 business continuity plan. | Auto | appointing party issues before tender |
| IR-07.EX.01 | Exchange date | Last working day of each quarter (fixed). | Auto | (calendar rule) |

### IR-08 Infection prevention and control

**Requirement owner:** Clinical – Infection Prevention and Control Lead  
**Requirement description:** As the IPC Lead, I need to confirm that clinical rooms have the right basins and finishes, so that cross-infection risk is controlled before the building opens to patients.  
**Supports:** OIR-SOC-01

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-08.G.00 | LOIN – graphical | None required. | – | – |
| IR-08.NG.01 | LOIN – non-graphical | Every clinical room has a clinical washbasin (Pr_40_20_96_35). | Auto | (room-to-product rule) |
| IR-08.NG.02 | LOIN – non-graphical | Finish type recorded per room. | Auto | (data dictionary row) |
| IR-08.D.01 | LOIN – documentation | IPC sign-off record before occupation. | Assisted | IPC Lead signs |
| IR-08.AC.01 | Acceptance criteria | HBN 00-09 and HBN 00-03. | Manual | IPC Lead |
| IR-08.SI.01 | Supporting information | HBN 00-09; room data sheet template (REF-07). | Auto | appointing party issues before tender |
| IR-08.EX.01 | Exchange date | At M-203-S4 (design review) and M-203-PC (before occupation). | Auto | L2-02 |

### IR-09 Accessibility

**Requirement owner:** ICB Estates – Equality and Access Lead  
**Requirement description:** As the Equality and Access Lead, I need evidence that accessible WCs and assistance calls are provided and working, so that the practice meets its Equality Act duties and patients can call for help.  
**Supports:** OIR-SOC-01

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-09.G.01 | LOIN – graphical | Accessible WC dimensions at or above the Approved Document M minimum. | Auto | (geometry rule) |
| IR-09.G.02 | LOIN – graphical | Accessible WC layout (transfer space, grab rails). | Manual | access consultant |
| IR-09.NG.01 | LOIN – non-graphical | An emergency assistance call in each accessible WC (AIR-24). | Auto | L3-14 |
| IR-09.D.01 | LOIN – documentation | Access statement; commissioning test of each assistance call. | Assisted | Access Lead |
| IR-09.AC.01 | Acceptance criteria | Approved Document M; BS 8300-2. | Manual | access consultant |
| IR-09.SI.00 | Supporting information | None required. | – | – |
| IR-09.EX.01 | Exchange date | At M-203-S4 and M-203-PC. | Auto | L2-02 |

### IR-10 Delivery assurance (MIDP and programme)

**Requirement owner:** ICB – Project Sponsor (MA 4920.203)  
**Requirement description:** As the Project Sponsor, I need to see each deliverable's status against the programme, so that I can spot information that will delay construction or handover before it does.  
**Supports:** OIR-ECO-01 · KPI-01, KPI-03, KPI-04

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-10.G.00 | LOIN – graphical | None required. | – | – |
| IR-10.NG.01 | LOIN – non-graphical | Document register with status, revision, date and security marking. | Auto | L1-24, L1-25, SEC-01 |
| IR-10.NG.02 | LOIN – non-graphical | Each MIDP deliverable linked to a programme activity or milestone ID. | Auto | (programme link rule) |
| IR-10.NG.03 | LOIN – non-graphical | Each deliverable due before the activity that needs it starts. | Auto | (programme logic rule) |
| IR-10.D.01 | LOIN – documentation | Monthly information delivery report. | Auto | generated from check results |
| IR-10.AC.01 | Acceptance criteria | Status and revision rules (Section 14) and MIDP dates. | Auto | L2-01 to L2-04 |
| IR-10.SI.01 | Supporting information | MA 4920 programme (P6 export) and MIDP template (REF-14). | Auto | appointing party issues before tender |
| IR-10.EX.01 | Exchange date | Register weekly; programme update monthly. | Auto | (freshness rule) |

### IR-11 Security of sensitive information

**Requirement owner:** ICB – Senior Security Risk Owner  
**Requirement description:** As the Senior Security Risk Owner, I need sensitive information about the substation, clinical waste plant, controlled drugs store and building control networks to be marked and shared only with named parties, so that the campus's critical services aren't exposed to attack or misuse.  
**Supports:** OIR-SOC-04

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-11.G.01 | LOIN – graphical | Shared site models show .204, .205 and the .202 store as envelope only. | Auto | SEC-04 |
| IR-11.NG.01 | LOIN – non-graphical | Every container carries a security marking (SEC-01, SEC-02). | Auto | SEC rules |
| IR-11.NG.02 | LOIN – non-graphical | No network addresses or credentials in COBie, models or general documents (SEC-08). | Auto | (pattern scan rule) |
| IR-11.D.01 | LOIN – documentation | Security management plan; information sharing agreements. | Assisted | Senior Security Risk Owner |
| IR-11.AC.01 | Acceptance criteria | BS EN ISO 19650-5; the security management plan. | Assisted | Senior Security Risk Owner |
| IR-11.SI.01 | Supporting information | Security triage outcome; NPSA guidance. | Auto | appointing party issues before tender |
| IR-11.EX.01 | Exchange date | Before any sensitive information is shared outside the appointing party (trigger). | Auto | (event rule) |
| IR-11.EX.02 | Exchange date | Plan reviewed every 6 months. | Auto | (frequency rule) |

### IR-12 Substation adoption (third party)

**Requirement owner:** Distribution Network Operator – Adoptions Engineer  
**Requirement description:** As the DNO's Adoptions Engineer, I need as-built records and test certificates for the substation, so that I can adopt and energise it safely.  
**Supports:** OIR-SOC-04

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-12.G.01 | LOIN – graphical | As-built cable routes and substation layout (restricted under IR-11). | Manual | DNO |
| IR-12.NG.01 | LOIN – non-graphical | Equipment schedule: switchgear and transformer ratings and serial numbers. | Auto | (data dictionary rows) |
| IR-12.D.01 | LOIN – documentation | ENA G81 adoption pack items present. | Auto | (document checklist rule) |
| IR-12.D.02 | LOIN – documentation | Test certificates acceptable to the DNO. | Manual | DNO |
| IR-12.AC.01 | Acceptance criteria | ENA G81 and the DNO's own standards. | Manual | DNO |
| IR-12.SI.00 | Supporting information | None required. | – | – |
| IR-12.EX.01 | Exchange date | 4 weeks before M-204-EN (energisation). | Auto | (milestone rule) |

### IR-13 Clinical waste plant permit compliance

**Requirement owner:** ICB Estates – Environmental Compliance Manager  
**Requirement description:** As the Environmental Compliance Manager, I need emissions and throughput records for the clinical waste plant, so that we comply with the environmental permit and can report to the regulator.  
**Supports:** OIR-ENV-04

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-13.G.00 | LOIN – graphical | None required. | – | – |
| IR-13.NG.01 | LOIN – non-graphical | Monitoring point register with permit limit per parameter. | Auto | (data dictionary rows) |
| IR-13.D.01 | LOIN – documentation | Monthly monitoring returns present. | Auto | (frequency rule) |
| IR-13.D.02 | LOIN – documentation | Return content. | Manual | Environmental Compliance Manager |
| IR-13.AC.01 | Acceptance criteria | Readings within permit limits (Environmental Permitting Regulations 2016; HTM 07-01). | Auto | data platform check |
| IR-13.SI.00 | Supporting information | None required. | – | – |
| IR-13.EX.01 | Exchange date | Monthly from commissioning of .205. | Auto | (frequency rule) |

### IR-14 Health and safety file

**Requirement owner:** ICB – Client (CDM 2015)  
**Requirement description:** As the client under CDM 2015, I need the health and safety file, so that future maintenance, alteration and demolition can be done safely.  
**Supports:** OIR-SOC-03

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-14.G.01 | LOIN – graphical | Each residual hazard has a location. | Auto | (data rule) |
| IR-14.NG.01 | LOIN – non-graphical | Residual hazard register with required fields. | Auto | (data dictionary rows) |
| IR-14.D.01 | LOIN – documentation | H&S file with the ICB template sections. | Assisted | rule checks sections; client checks content |
| IR-14.AC.01 | Acceptance criteria | CDM 2015. | Manual | Principal Designer |
| IR-14.SI.00 | Supporting information | None required. | – | – |
| IR-14.EX.01 | Exchange date | At M-203-PC. | Auto | L2-02 |

### IR-15 Post-occupancy evaluation and lessons learned

**Requirement owner:** ICB – Programme Sponsor (MA 4920)  
**Requirement description:** As the Programme Sponsor, I need year 1 and year 2 performance evaluations and lessons learned, so that later campus buildings and future ICB projects are briefed better.  
**Supports:** all OIR outcomes · KPI-11 to KPI-17; BEN-01 to BEN-06

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-15.G.00 | LOIN – graphical | None required. | – | – |
| IR-15.NG.01 | LOIN – non-graphical | Measured value of every KPI against target (Section 19). | Auto | KPI calculation |
| IR-15.D.01 | LOIN – documentation | POE report and lessons learned log. | Manual | Programme Sponsor |
| IR-15.AC.01 | Acceptance criteria | Each benefit (BEN-xx) reported with baseline, target and measured value. | Auto | (benefit register check) |
| IR-15.SI.00 | Supporting information | None required. | – | – |
| IR-15.EX.01 | Exchange date | Handover + 12 months and + 24 months. | Auto | (milestone rule) |

### IR-16 Connected systems and live data

**Requirement owner:** ICB Estates – Estates Digital Lead  
**Requirement description:** As the Estates Digital Lead, I need every sensor, meter and control point to arrive named, linked to its asset and streaming into the ICB data platform, so that alarms raise work orders automatically and the energy, water temperature and room use KPIs are measured from the first day of operation.  
**Supports:** OIR-ENV-01, OIR-SOC-01, OIR-SOC-02, OIR-SOC-03 · KPI-08, KPI-11, KPI-12, KPI-14, KPI-16

| ID | Component | Requirement | Verification | Verified by |
|---|---|---|---|---|
| IR-16.G.01 | LOIN – graphical | Each field device (sensor, meter, controller) is located in a room. | Auto | L3-04 |
| IR-16.NG.01 | LOIN – non-graphical | A points schedule with one row per point, in the format of INT-02. | Auto | (INT-02 rule) |
| IR-16.NG.02 | LOIN – non-graphical | Every point links to an asset that exists in COBie, with a matching GUID (INT-03). | Auto | (INT-03 rule) |
| IR-16.NG.03 | LOIN – non-graphical | Point IDs follow the naming convention (INT-04). | Auto | (INT-04 rule) |
| IR-16.NG.04 | LOIN – non-graphical | Each point tagged with a Brick schema class (INT-05). | Assisted | rule checks the class exists; Digital Lead checks it's right |
| IR-16.D.01 | LOIN – documentation | Integration specification: systems, interfaces, protocols, data flows, security (INT-07). | Assisted | Digital Lead and IT/OT security |
| IR-16.D.02 | LOIN – documentation | Point-to-point test records for 100% of points (INT-11). | Auto | (completeness rule) |
| IR-16.D.03 | LOIN – documentation | 14-day data soak test report (INT-11). | Auto | data platform metrics |
| IR-16.AC.01 | Acceptance criteria | Open protocols only: BACnet/IP for building controls; Modbus TCP or M-Bus for meters (INT-06). | Auto | (points schedule rule) |
| IR-16.AC.02 | Acceptance criteria | At least 95% of expected readings received during the soak test, with UTC timestamps and values in range (INT-11). | Auto | data platform check |
| IR-16.AC.03 | Acceptance criteria | End-to-end test: a simulated TMV over-temperature alarm creates a CAFM work order within 5 minutes (INT-11). | Assisted | witnessed by Digital Lead |
| IR-16.AC.04 | Acceptance criteria | Operational technology security requirements met (SEC-08, SEC-09). | Assisted | IT/OT security |
| IR-16.SI.01 | Supporting information | ICB point naming and integration standard (REF-09). | Auto | appointing party issues before tender |
| IR-16.SI.02 | Supporting information | ICB data platform interface specification and test environment (REF-11). | Auto | appointing party issues before tender |
| IR-16.EX.01 | Exchange date | Integration specification at M-203-S4. | Auto | L2-02 |
| IR-16.EX.02 | Exchange date | Draft points schedule at M-203-IE2; final at M-203-PC. | Auto | L2-02 |
| IR-16.EX.03 | Exchange date | Soak test report before M-203-PC. | Auto | L2-02 |
| IR-16.EX.04 | Exchange date | Monthly data quality report during the 12-month defects period. | Auto | (frequency rule) |

---

## 6. Connected systems and data integration

This section turns IR-16 into an information standard for connected systems. It covers **what** the appointed parties hand over, so the systems can feed the ICB data platform on day one. How the ICB then uses the data (condition monitoring, energy management, maintenance planning) is part of its asset management system and drives the outcomes in Section 4. It isn't specified here.

### 6.1 Systems in scope (MA 4920.203)

| System | Purpose | Data to the ICB platform | Protocol | Write-back from the platform | KPIs fed |
|---|---|---|---|---|---|
| Building management system (BMS): AHU, heating, ventilation | Comfort, energy, plant status | Temperatures, status, alarms, set points | BACnet/IP | Listed set points only | KPI-11 |
| Energy metering (main and sub-meters) | Energy use by end use | kWh, kW | Modbus TCP or M-Bus via gateway | None | KPI-11 |
| Water metering | Water use | m³ | M-Bus or pulse via gateway | None | KPI-12 |
| Water temperature monitoring (each TMV outlet and sentinel outlets) | Scald and water safety | °C, alarms | Gateway to BACnet/IP or MQTT (proposed in BEP) | None | KPI-16 |
| Emergency lighting monitoring (addressable self-test) | Compliance testing | Test results, faults | Gateway | None | KPI-15 |
| Room occupancy sensors (consulting and treatment rooms) | Room use | Occupied / unoccupied (presence only) | Gateway | None | KPI-14 |
| Nurse call and assistance call | Fault monitoring | System fault status only | Gateway | None | KPI-15 |
| Fire detection and alarm (BS 5839-1) | Life safety | Alarm, fault, disablement status only (INT-10) | Gateway, one way | **Never** | – |

Occupancy sensors detect presence only. No cameras, no counting of individuals and no personal data, so no personal data reaches the platform.

### 6.2 How the data flows

Field devices (sensors, meters, controllers) → system controllers and gateways on a segregated building network → integration gateway → ICB data platform (time-series store) → two consumers: **CAFM** (alarms become work orders) and **ICB reporting dashboards** (KPIs in Section 19).

The appointed parties deliver everything up to and including the connection to the ICB data platform's interface (REF-11). The ICB owns the platform, CAFM and dashboards.

### 6.3 Requirements

| ID | Requirement | Checked in | Verification |
|---|---|---|---|
| INT-01 | Every system in 6.1 is delivered with a points schedule (INT-02), an integration specification (INT-07) and test records (INT-11). | REG | Auto |
| INT-02 | The **points schedule** has one row per point with these columns: `point_id`, `asset_name`, `asset_guid`, `system`, `point_type`, `unit`, `data_type`, `sampling_interval_s`, `range_min`, `range_max`, `alarm_low`, `alarm_high`, `writable` (Y/N), `brick_class`, `device_ref`. It's delivered as `.csv` or `.xlsx` and contains **no network addresses** (see SEC-08). | Points schedule | Auto |
| INT-03 | Every point's `asset_name` exists as a COBie Component, and its `asset_guid` matches that component's GUID. Points not linked to an asset are not accepted. | Points schedule + COBie | Auto |
| INT-04 | Point IDs follow `<project>-<volume>-<asset name>-<point type>[-<qualifier>]`. Example: `LRHC-03-TMV-00-004-TMP` (mixed water temperature at TMV-00-004); `LRHC-03-AHU-00-001-TMP-SUP` (AHU supply air temperature). Point type codes come from REF-09. | Points schedule | Auto |
| INT-05 | Each point is tagged with a class from the Brick schema (an open vocabulary for building data), so the platform can read it without manual mapping. The BEP may propose Project Haystack tagging instead. | Points schedule | Assisted |
| INT-06 | Only open protocols: BACnet/IP for building controls; Modbus TCP or M-Bus for meters, through gateways. Proprietary-only interfaces aren't accepted. The ICB receives all software licences and administrator rights in its own name. | Points schedule, integration specification | Auto (protocol), Assisted (licences) |
| INT-07 | An **integration specification** describes each interface: systems connected, protocol, data flow direction, sampling and transmission frequency, alarm priorities and how they map to CAFM work order types, and security controls. | Document | Assisted |
| INT-08 | Units are SI and taken from the code list in REF-09. Timestamps are UTC in ISO 8601 format. All controllers are time-synchronised to the ICB time source. | Points schedule, live data | Auto |
| INT-09 | The platform is read-only, except for points marked `writable = Y` in the points schedule and agreed in the integration specification. | Points schedule | Auto |
| INT-10 | Fire detection and alarm stays an independent life-safety system. Only alarm, fault and disablement status may leave it, one way, through a gateway. Nothing may write to it. | Integration specification, points schedule | Auto (no writable fire points), Assisted (design) |
| INT-11 | **Commissioning and acceptance of the data**: (a) point-to-point test of 100% of points, recorded per point; (b) an end-to-end test, witnessed by the Estates Digital Lead, in which a simulated TMV over-temperature alarm creates a CAFM work order within 5 minutes; (c) a 14-day soak test before M-203-PC, with at least 95% of expected readings received, UTC timestamps and values within range. | Test records, live data | Auto (a, c), Assisted (b) |
| INT-12 | During the 12-month defects period, the lead appointed party provides a monthly data quality report (completeness, gaps, out-of-range values per point) and fixes failed points within 10 working days. | Live data, report | Auto |

### 6.4 What a rule can check, and what it can't

- **Before handover, from the points schedule:** INT-02 to INT-06, INT-08 and INT-09 are checkable. The schedule is a table, so every row can be tested, and INT-03 joins it to COBie.
- **During the soak test, from the live data:** completeness, freshness, timestamps and ranges (INT-11c, INT-12). These need the data pipeline, not the file checker.
- **What stays with people:** whether the integration design is sound (INT-07), whether Brick tags are the right class (INT-05), and witnessing the end-to-end test (INT-11b).

---

## 7. Level of information need: MA 4920.203

G = graphical, NG = non-graphical, D = documentation. LOIN changes by stage because the procurement route (design and build) moves detail to the contractor from Stage 4.

| ABS level | Design (RIBA 2–3) | Technical design (RIBA 4) | Construction (RIBA 5) | Handover (RIBA 6) | In use (RIBA 7) |
|---|---|---|---|---|---|
| **Complex** (MA 4920) | G: site masterplan, building outlines. NG: entity list and codes. D: campus brief | G: site model, envelopes only for sensitive entities. D: security management plan | G: logistics plans | NG: campus asset register index | NG: performance data per entity |
| **Entity** (.203) | G: massing. NG: area schedule. D: stage report | G: coordinated model. NG: room data. D: fire and access strategies | D: construction issue drawings | G: as-built model. D: O&M manual, H&S file | D: year 1 and 2 reports |
| **Space** | G: room outlines. NG: room name, area, SL code | G: accurate boundaries. NG: patient-area flag, finishes. D: room data sheets | as Stage 4 | G: as-built ±50 mm. NG: verified areas | NG: utilisation |
| **System** | NG: system list and Ss codes | G: routes. NG: system membership | as Stage 4 | NG: as-commissioned membership. D: commissioning records | NG: meter data |
| **Element / product** | none | G: symbolic block in room. NG: type and Pr code | NG: manufacturer and model as selected | G: position. NG: full AIR (serial, dates, warranty, PPM). D: certificates | NG: work orders (CAFM) |

---

## 8. Spaces and assets in scope

### 8.1 Space schedule

| Space name | Room name (Description) | Uniclass SL code | Patient area |
|---|---|---|---|
| 00-001 | Entrance and reception | SL_20_15_71 Reception areas | N |
| 00-002 | Waiting area | SL_90_20_96 Waiting rooms | N |
| 00-003 | Children's play area | SL_40_05_43 Indoor play spaces | Y |
| 00-004 to 00-007 | Consulting rooms 1–4 | SL_35_10_15 Consulting rooms | Y |
| 00-008, 00-009 | Treatment rooms 1–2 | SL_35_10_53 Medical treatment rooms | Y |
| 00-010 | Paediatric clinic room | SL_35_10_15 Consulting rooms | Y |
| 00-011 | Nurse room | SL_35_10_53 Medical treatment rooms | Y |
| 00-012, 00-013 | Accessible WCs 1–2 | SL_35_80_03 Accessible toilets | Y |
| 00-014 | Baby change | SL_35_80_06 Baby changing rooms | Y |
| 00-015 | Staff room | SL_90_20 Common spaces *(group code, see Annex C)* | N |
| 00-016 | Staff WC | SL_35_80_89 Toilets | N |
| 00-017 | Plant room | SL_90_90 Plant and control spaces *(group code, see Annex C)* | N |
| 00-018 | Store | SL_90_50_35 General storerooms | N |
| 00-019 | Corridor | SL_90_10_15 Corridors | N |

One floor: **00** (ground).

### 8.2 Asset types

| Code | Asset type | IFC entity | Uniclass Pr code | Uniclass Ss code (System) | Qty |
|---|---|---|---|---|---|
| AHU | Air handling unit | IfcUnitaryEquipment, AIRHANDLER | Pr_60_65_03_87 Supply and return air-handling units | Ss_65_40_33_49 Mechanical supply and extract ventilation systems | 1 |
| FD | Fire doorset | IfcDoor | Pr_30_59_24_97 Wood doorsets | none | 4 |
| FDM | Fire damper | IfcDamper, FIREDAMPER | Pr_65_65_24_30 Fire dampers | Ss_65_40_33_49 | 4 |
| TMV | Thermostatic mixing valve | IfcValve, MIXING | Pr_65_54_95_88 Thermostatic mixing valves | Ss_55_70_38_42 Indirect hot water storage supply systems | 11 |
| NCU | Nurse call unit | IfcCommunicationsAppliance, USERDEFINED (`NURSECALL`) | Pr_75_75_04_57 Nurse call units | Ss_75_50_11_57 Nurse call systems | 4 |
| EAC | Emergency assistance call (pull cord) | IfcCommunicationsAppliance, USERDEFINED (`ASSISTANCECALL`) | Pr_75_75_04_28 Emergency assistance call pull cord units | Ss_75_50_11_25 Emergency assistance call systems | 2 |
| LF | Light fitting (general) | IfcLightFixture | Pr_70_70_48_70 Recessed downlights | Ss_70_80_33_35 Hardwired general lighting systems | 3 |
| LF | Light fitting (emergency) | IfcLightFixture | Pr_70_70_48_77 Self-contained emergency luminaires | Ss_70_80_33_78 Self-contained emergency lighting systems | 3 |
| WC | WC pan | IfcSanitaryTerminal, TOILETPAN | Pr_40_20_93_94 WC pans | none | 3 |
| WHB | Washbasin (clinical rooms) | IfcSanitaryTerminal, WASHHANDBASIN | Pr_40_20_96_35 Healthcare clinical washbasins | none | 8 |
| WHB | Washbasin (WCs and baby change) | IfcSanitaryTerminal, WASHHANDBASIN | Pr_40_20_96_37 Healthcare general washbasins | none | 4 |

Total: 47 assets. Safety-critical types: **FD, FDM, TMV, NCU, EAC and emergency LF.**

| ID | Requirement | Checked in |
|---|---|---|
| CLS-01 | Every asset type uses the Pr code given in 4.2. | IFC + COBie |
| CLS-02 | Every space uses the SL code given in 4.1. | IFC + COBie |
| CLS-03 | Every asset in a system listed in 4.2 belongs to a COBie System (and an IFC `IfcSystem`) carrying the Ss code shown. | IFC + COBie |
| CLS-04 | No code marked "not in use" in Uniclass is used. For example, **Pr_30_59_24_28 Fire doorsets was withdrawn in 2023** and must not be used. Fire doors are classified by doorset type, with the fire rating held as an attribute (AIR-20). | IFC + COBie |

### 8.3 Where assets must be

| ID | Requirement | Checked in |
|---|---|---|
| LOC-01 | Every asset sits in exactly one space: contained in or referenced by one `IfcSpace`, with the same space in COBie `Component.Space`. | IFC + COBie |
| LOC-02 | Every space belongs to floor 00 (`IfcBuildingStorey` / COBie `Space.FloorName`). | IFC + COBie |
| LOC-03 | Every washbasin in a space with Patient area = Y is served by a TMV in the same space (see AIR-23). | COBie |
| LOC-04 | Each treatment room, the paediatric clinic room and the nurse room has at least one NCU. Each accessible WC has at least one EAC. | COBie |
| LOC-05 | The corridor and the plant room each have at least one emergency light fitting. | COBie |

---

## 9. Asset information requirements (AIR)

### 9.1 Common attributes

✔ = required · – = not required. Purposes: O = operation and maintenance, C = compliance, S = space management.

| ID | Attribute | COBie field | IFC location | AHU | FD | FDM | TMV | NCU / EAC | LF | WC / WHB | Purpose |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AIR-01 | Asset name | Component.Name | element Name | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | O |
| AIR-02 | Type name | Component.TypeName, Type.Name | type object Name | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | O |
| AIR-03 | Description | Component.Description | element Description | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | O |
| AIR-04 | Space | Component.Space | spatial containment | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | O, S |
| AIR-05 | Classification (Pr) | Type.Category | IfcClassificationReference | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | O |
| AIR-06 | Manufacturer | Type.Manufacturer | Pset_ManufacturerTypeInformation.Manufacturer | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | O |
| AIR-07 | Model number | Type.ModelNumber | Pset_ManufacturerTypeInformation.ModelReference | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | O |
| AIR-08 | Serial number | Component.SerialNumber | Pset_ManufacturerOccurrence.SerialNumber | ✔ | – | ✔ | ✔ | ✔ | – | – | O, C |
| AIR-09 | Installation date | Component.InstallationDate | LRHC_AssetData.InstallationDate | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | – | O |
| AIR-10 | Warranty start date | Component.WarrantyStartDate | LRHC_AssetData.WarrantyStartDate | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | – | O |
| AIR-11 | Warranty duration (parts) and unit | Type.WarrantyDurationParts, Type.WarrantyDurationUnit | LRHC_AssetData.WarrantyDurationParts | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | – | O |
| AIR-12 | Expected life (years) | Type.ExpectedLife, Type.DurationUnit | LRHC_AssetData.ExpectedLife | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | O |
| AIR-13 | Maintenance frequency | Job.Frequency, Job.FrequencyUnit (Job.Category = `PPM`) | n/a (COBie only) | ✔ | ✔ | ✔ | ✔ | ✔ | emergency only | – | O, C |
| AIR-14 | Maintenance task description | Job.Description | n/a (COBie only) | ✔ | ✔ | ✔ | ✔ | ✔ | emergency only | – | O, C |

### 9.2 Value rules for common attributes

| ID | Requirement | Checked in |
|---|---|---|
| AIR-15 | `Type.Manufacturer` is an email address that exists in the COBie Contact sheet (COBie links manufacturers through Contact). | COBie |
| AIR-16 | Required fields are not blank and not a placeholder (`n/a`, `TBC`, `-`, `0`, `unknown`). | IFC + COBie |
| AIR-17 | Warranty start date is on or after the installation date. | COBie |
| AIR-18 | Installation date is not later than the date of the submission. | COBie |
| AIR-19 | Maximum maintenance intervals (project requirement, set by the appointing party): AHU 6 months · FD 6 months · FDM 12 months · TMV 6 months · NCU/EAC 6 months · emergency LF 1 month. | COBie |

### 9.3 Type-specific attributes

These go in the COBie Attribute sheet and in IFC `LRHC_AssetData`, unless a standard property set is named.

| ID | Asset type | Attribute | Allowed values | Purpose |
|---|---|---|---|---|
| AIR-20 | FD | FireRating (IFC: `Pset_DoorCommon.FireRating`) | FD30, FD30S, FD60, FD60S | C |
| AIR-21 | FD | CertificationNumber (third-party doorset certificate) | Not blank | C |
| AIR-22 | FDM | FireResistanceMinutes; ActuationType | 60 or 120; `FusibleLink` or `Motorised` | C |
| AIR-23 | TMV | TMVApproval; SetTemperature; ServesComponent | `TMV3`; `41` (°C, washbasins, project requirement; designer to confirm against HTM 04-01); the name of a WHB in the same space | C |
| AIR-24 | NCU, EAC | CallType | `PatientCall`, `StaffEmergency`, `EmergencyAssistance` (EAC must be `EmergencyAssistance`) | C |
| AIR-25 | LF | EmergencyLighting | `Y` or `N`. Must be `Y` for Pr_70_70_48_77 and `N` for Pr_70_70_48_70 | C |
| AIR-26 | AHU | AirflowRate (m³/s) | Number greater than 0 | O |
| AIR-27 | Space | NetArea (m²); PatientArea | Number greater than 0; `Y`/`N` matching Section 8.1 | S |

### 9.4 Free-text requirement (human review)

| ID | Requirement | Checked in |
|---|---|---|
| AIR-28 | Each maintenance task description (AIR-14) states the actual tasks, not just "service as per manufacturer". For TMVs it must include an **outlet temperature check** and a **fail-safe test (cold supply isolation)**. For fire dampers it must include a **drop test and reset**. | COBie (automated flag only; a person decides, see Section 18) |

The ICB classification code for every asset type (AIR-29) is in Section 10.2.

---

# Part C: How the information is produced

## 10. Reference information and shared resources

### 10.1 What the ICB provides

All reference information is issued as information containers in the ICB's CDE, in the *Reference* area, with a stated revision. The appointed parties work to the revision listed here. A later revision only applies once this EIR is revised to name it.

| ID | Resource | Container | Revision | Format |
|---|---|---|---|---|
| REF-01 | Data dictionary and code lists: machine-readable annex to this EIR | LRHC-LRV-ZZ-ZZ-SH-K-000002 | P03 | `.csv` / `.xlsx` |
| REF-02 | Uniclass 2015 tables Pr, SL, Ss, with the version number of each (see 10.3) | LRHC-LRV-ZZ-ZZ-SH-K-000003 | P01 | `.xlsx` |
| REF-03 | ICB asset classification (LAC) and its mapping to Uniclass (see 10.2) | LRHC-LRV-ZZ-ZZ-SH-K-000004 | P01 | `.xlsx` |
| REF-04 | Topographical survey and survey control (SP-01) | LRHC-LRV-00-ZZ-SU-K-000001 | C01 | `.dwg`, `.ifc`, `.pdf` |
| REF-05 | Existing campus utilities records and site fire plan | LRHC-LRV-00-ZZ-DR-K-000001 | C01 | `.pdf` |
| REF-06 | Water safety plan template | LRHC-LRV-ZZ-ZZ-SP-K-000005 | C01 | `.docx` |
| REF-07 | Room data sheet template | LRHC-LRV-ZZ-ZZ-SH-K-000006 | C01 | `.xlsx` |
| REF-08 | CAFM import template | LRHC-LRV-ZZ-ZZ-SH-K-000007 | C01 | `.xlsx` |
| REF-09 | Point naming and integration standard (point type codes, units, Brick classes) | LRHC-LRV-ZZ-ZZ-SP-K-000008 | P01 | `.pdf` + `.csv` |
| REF-10 | Emergency plan template | LRHC-LRV-ZZ-ZZ-SP-K-000009 | C01 | `.docx` |
| REF-11 | ICB data platform interface specification and test environment access | LRHC-LRV-ZZ-ZZ-SP-K-000010 | P01 | `.pdf` (OFFICIAL-SENSITIVE) |
| REF-12 | Asset requirements as a buildingSMART IDS file | LRHC-LRV-03-ZZ-IE-K-000001 | P03 | `.ids` |
| REF-13 | Checking rules used for acceptance (Annex B) | LRHC-LRV-ZZ-ZZ-SH-K-000011 | P03 | `.csv` |
| REF-14 | MA 4920 programme (P6 export) and MIDP template | LRHC-LRV-ZZ-ZZ-PR-K-000001 | P01 | `.xer`, `.xlsx` |

| ID | Requirement | Verification |
|---|---|---|
| REF-15 | Each resource above is in the CDE at the listed revision before the invitation to tender is issued. | Auto (register) |
| REF-16 | A change to a listed resource is issued as a new revision, and this EIR names it before it applies. | Auto (register) |

### 10.2 ICB asset classification and Uniclass

The ICB classifies its estate with its own scheme, **LAC (Larch Valley Asset Classification)**. It runs site → building → system → asset class → asset type, for example `MEC.HWS.TMV` (mechanical / hot water services / thermostatic mixing valve). LAC is what the ICB's CAFM and finance systems use.

Uniclass remains the classification for design and construction information. The ICB doesn't add its own codes to Uniclass; the Uniclass licence asks users to suggest new codes to NBS rather than adapt the tables. REF-03 maps each LAC asset type to its Uniclass Pr and Ss codes.

| ID | Requirement | Checked in | Verification |
|---|---|---|---|
| AIR-29 | Every asset type carries its LAC code (COBie Attribute `LACCode`; IFC `LRHC_AssetData.LACCode`). The LAC code is the one mapped to the type's Uniclass Pr code in REF-03. | IFC + COBie | Auto |

### 10.3 Uniclass version control

NBS updates the Uniclass tables every quarter, and codes are added, renamed and withdrawn (for example, Pr_30_59_24_28 *Fire doorsets* was withdrawn in 2023). To keep everyone on the same codes:

| ID | Requirement | Verification |
|---|---|---|
| CLS-05 | This project uses the Uniclass Pr, SL and Ss tables at the versions recorded in REF-02 (the October 2026 release). Each table's version number is recorded separately. | Auto (codes checked against REF-02) |
| CLS-06 | A newer Uniclass release is adopted only at a stage boundary, by a revision of this EIR and REF-02, with a list of changed codes and their replacements. | Assisted |
| CLS-07 | Checks compare the code only, not the title, so a renamed title doesn't fail a submission. | Auto |

---

## 11. Spatial coordination

The ICB sets the coordinate reference system and the survey control here. The BEP sets out how each task team's models use them, for example shared coordinates and the project base point in each authoring tool.

| ID | Requirement | Checked in | Verification |
|---|---|---|---|
| GEO-01 | Horizontal coordinate reference system: British National Grid on OSGB36 (EPSG:27700). | IFC | Auto |
| GEO-02 | Heights in metres above Ordnance Datum Newlyn (m AOD). | IFC | Auto |
| GEO-03 | Survey control point **SP-01**: E 522 624.500, N 171 528.300, 50.000 m AOD (height to be confirmed by the topographical survey, REF-04). SP-01 is the project base point. | IFC | Auto |
| GEO-04 | Project north = grid north (0° rotation). Each IFC model records its georeferencing in `IfcMapConversion` and `IfcProjectedCRS`, and the values match GEO-01 to GEO-03. | IFC | Auto |
| GEO-05 | Coordinates are in metres. Models are authored in millimetres, with the model origin at SP-01, so geometry stays close to the origin and avoids precision loss at grid coordinates. | IFC | Auto |
| GEO-06 | Storey elevations are stated in m AOD and named per the level codes in Section 13. | IFC | Auto |
| GEO-07 | As-built positions of maintainable assets are within ±50 mm of their installed position. | Site survey | Manual |

---

## 12. Exchange formats

| ID | Requirement | Checked in |
|---|---|---|
| FMT-01 | Models are delivered as **IFC4** (`.ifc`, STEP format). | IFC |
| FMT-02 | Asset data is delivered as **COBie 2.4** in one spreadsheet (`.xlsx`). | COBie |
| FMT-03 | The COBie file contains at least these sheets: Contact, Facility, Floor, Space, Type, Component, System, Job, Document, Attribute. | COBie |
| FMT-04 | Each asset appears in both the IFC and the COBie file. COBie `Component.ExtIdentifier` equals the IFC `GlobalId` of the same element. | IFC + COBie |
| FMT-05 | Dates use ISO 8601 (`yyyy-mm-dd` or COBie's `yyyy-mm-ddThh:mm:ss`). Numbers use SI units with no unit text in the value. Yes/no values are `Y` or `N`. | IFC + COBie |
| FMT-06 | Attributes that COBie has no column for go in the COBie **Attribute** sheet. In IFC they go in the property set **`LRHC_AssetData`**, with the same property name. Standard property sets are used where named in Section 5. | IFC + COBie |
| FMT-07 | Classification in IFC uses `IfcClassificationReference` to Uniclass 2015. In COBie it goes in the `Category` field as `code : title`, e.g. `Pr_65_54_95_88 : Thermostatic mixing valves`. | IFC + COBie |

---

## 13. Naming

### 13.1 Information containers (documents, models, COBie files)

Pattern: **Project – Originator – Volume – Level – Type – Role – Number**, separated by hyphens.

| Field | Allowed values |
|---|---|
| Project | `LRHC` |
| Originator | `LRV`, `BMC`, `FLD`, `KBS` |
| Volume / system | `ZZ` (all), `XX` (none), `00` site-wide (MA 4920.200), `01`–`07` entities MA 4920.201–.207 (see Section 2) |
| Level / location | `00` (ground), `RF` (roof), `ZZ` (multiple), `XX` (none) |
| Type | `M3` 3D model, `M2` 2D model, `DR` drawing, `SH` schedule, `SP` specification, `RP` report, `IE` information exchange file, `SU` survey, `PR` programme |
| Role | `A` architect, `E` electrical, `M` mechanical, `P` public health, `W` contractor, `K` client, `Z` general |
| Number | 6 digits, e.g. `000001` |

Examples: `LRHC-KBS-ZZ-00-M3-M-000001` (planned before P02, keeps its name); `LRHC-KBS-03-00-M3-M-000002` (a new container from P02 onwards).

Container names are fixed for the life of the container. Containers already in the MIDP keep `ZZ`. New containers created from P02 use the entity's volume code. The security rules (SEC-02) need that code, so sensitive entities (`02`, `04`, `05`) must always use it.

| ID | Requirement | Checked in |
|---|---|---|
| NAM-01 | Every container name matches the pattern and uses only the allowed values above. | REG + COBie (Document sheet) |
| NAM-02 | Each container name is unique in the register. | REG |

### 13.2 Assets, types and spaces

| ID | Requirement | Pattern | Example | Checked in |
|---|---|---|---|---|
| NAM-03 | Asset (component) names: asset code, level, 3-digit number | `AAA-00-NNN` | `TMV-00-004` | IFC + COBie |
| NAM-04 | Asset names are unique across the facility. | | | IFC + COBie |
| NAM-05 | Type names: asset code, `Type`, 2-digit number | `AAA-TypeNN` | `TMV-Type01` | IFC + COBie |
| NAM-06 | Space names: level, 3-digit number. Room name goes in Description. | `00-NNN` | `00-010` | IFC + COBie |
| NAM-07 | The asset code at the start of each name matches the asset type's classification in Section 8.2. | | | IFC + COBie |

---

## 14. Status codes and revisions (UK National Annex)

| Code | Meaning | Revision form |
|---|---|---|
| S0 | Work in progress | P01.01 (not submitted, not checked) |
| S1 | Suitable for coordination | P01, P02 … |
| S2 | Suitable for information | P01, P02 … |
| S3 | Suitable for review and comment | P01, P02 … |
| S4 | Suitable for stage approval | P01, P02 … |
| A*n* | Authorised and accepted at stage *n* (e.g. A4, A6) | C01, C02 … |
| CR | As-constructed record | C01, C02 … |

S6, S7 and B codes are not used on this project.

| ID | Requirement | Checked in |
|---|---|---|
| STA-01 | Every submitted container has a status from the table above (not S0). | REG |
| STA-02 | S1–S4 use a preliminary revision (`P` + 2 digits). A*n* and CR use a contractual revision (`C` + 2 digits). | REG |
| STA-03 | Revisions only move forward. The same container never has the same revision twice. | REG |
| STA-04 | By its due date in the MIDP, each container has at least the status shown there. For this check the order is S0 → S1 → S2 → S3 → S4 → A → CR. | REG |

---

## 15. Security (BS EN ISO 19650-5)

### 15.1 Sensitivity triage

| Entity | Sensitive? | Why |
|---|---|---|
| Building control networks (all entities) | **Yes** | Network addresses and credentials would let an attacker reach plant controls (SEC-08, SEC-09) |
| .204 Substation | **Yes** | Single point of supply for clinical buildings. Location and layout aid hostile planning. Third party (DNO) involved |
| .205 Clinical waste plant | **Yes** | Hazardous process; regulated permit; process details could enable misuse |
| .202 Pharmacy store | **Yes** (store area only) | Controlled drugs: layout and access arrangements aid theft |
| .201 Diagnostic and treatment centre | Partly | Critical clinical services; protect plant rooms and the critical services list |
| .203 GP practice, .206, .207 | No (OFFICIAL) | Normal public-facing buildings |

None of the campus is critical national infrastructure, nor does it serve a defence function or host major events. The sensitivity comes from service continuity, hazardous materials and controlled drugs.

### 15.2 Risk scoring

Score = likelihood (1–5) × impact (1–5). 12 or more is **high** and must be reduced. 10 or less can be accepted with the Senior Security Risk Owner's sign-off.

| ID | Threat | L | I | Score | Mitigation | Residual |
|---|---|---|---|---|---|---|
| T1 | Hostile reconnaissance of the substation from shared drawings | 3 | 5 | **15** | Envelope-only in shared models; OFFICIAL-SENSITIVE marking; named access list | 2 × 5 = 10 |
| T2 | Theft of controlled drugs using store layout information | 3 | 4 | **12** | Store layout in a restricted container; access list; no store detail in COBie shared outside Estates | 2 × 4 = 8 |
| T3 | Exposure of waste plant process details | 2 | 4 | 8 | Restricted container; information sharing agreement with the operator | 1 × 4 = 4 |
| T4 | Unauthorised CDE access (stolen login) | 3 | 3 | 9 | Multi-factor login; quarterly access review; leavers removed in 1 working day | 2 × 3 = 6 |
| T5 | Over-sharing with third parties beyond need | 3 | 3 | 9 | Information sharing agreements listing exactly what's shared | 2 × 3 = 6 |

Controls cover all three kinds: **behavioural** (login, need-to-know), **physical** (locks on comms rooms) and **technological** (CDE permissions, audit logs). Risks are reviewed every 6 months and whenever the context changes: political, economic, social, technological, legal or environmental (PESTLE). A new tenant, a security incident or a regulation change all count.

### 15.3 Security management plan: contents for this project

| Section | For MA 4920 |
|---|---|
| Policies | Need-to-know; OFFICIAL-SENSITIVE for .202 store, .204 and .205 detail |
| Methods and procedures | Marking, storage in a restricted CDE area, approval before sharing |
| Information exchange | Sensitive containers shared only with named parties; never in the federated site model |
| Logistics | Site hoarding and deliveries for .204 kept off public plans |
| Breach and incident management | Report within 24 hours to the Senior Security Risk Owner; contain, assess, notify |
| Accountability | Senior Security Risk Owner (ICB); a security lead named by each appointed party |
| Monitoring and audit | Quarterly CDE access review; automated marking checks every exchange |
| Review | Every 6 months, or on a PESTLE change |

### 15.4 From plan to checkable requirements

The security management plan → appointment agreements → information protocol → AIR. These are the parts a rule can check:

| ID | Requirement | Check | Source of data |
|---|---|---|---|
| SEC-01 | Every container has a security marking (OFFICIAL or OFFICIAL-SENSITIVE) | Auto | Register |
| SEC-02 | Containers for volume 04, 05, or the 02 store, are OFFICIAL-SENSITIVE | Auto | Register (volume field + marking) |
| SEC-03 | OFFICIAL-SENSITIVE containers are only shared with parties on their access list | Auto | CDE permission export |
| SEC-04 | The shared site model holds only envelope elements for .204, .205 and the .202 store | Auto | IFC |
| SEC-05 | Sensitive entities' COBie is a separate container | Auto | Register |
| SEC-06 | An information sharing agreement with each third party (DNO, waste plant operator) exists before their first exchange | Auto (date) + Manual (content) | Register |
| SEC-07 | Drawings don't reveal sensitive detail through annotations or backgrounds | Manual | Review |
| SEC-08 | Network addresses, device credentials and network diagrams for connected systems are OFFICIAL-SENSITIVE. They go only to ICB IT/OT security, in their own container. They never appear in COBie, models, the points schedule or general documents. | Auto (scan for IP addresses and credential patterns) | COBie, IFC, points schedule, register |
| SEC-09 | Connected devices have no default passwords; firmware versions are listed; the building network is segregated from the ICB corporate network; remote access is only through the ICB-approved method. The design follows IEC 62443 principles. | Assisted | Integration specification, commissioning records |

### 15.5 Information sharing agreements

Needed wherever the information protocol doesn't already bind a party:
- **DNO:** substation as-builts and test data (IR-12)
- **Waste plant operator:** process and monitoring data (IR-13)
- **Environment Agency:** permit returns only

---

# Part D: Delivery, acceptance and benefits

## 16. Exchange dates, milestones and MIDP

### 16.1 Types of exchange date

Exchange dates point to programme milestones, not fixed dates where possible. Then a programme change moves the deadlines automatically. These milestone IDs are **provisional** until the P6 programme is built.

| Type | Example | How a rule handles it |
|---|---|---|
| Fixed date | Last working day of each quarter (IR-07) | Due dates generated from the calendar |
| Relative (milestone) | M-203-S4 technical design complete; M-203-IE2 pre-handover; M-203-PC practical completion; M-203-REC record information; M-204-EN substation energisation | Due date read from the programme each time the check runs |
| Frequency | Monthly meter data (IR-06); 6-monthly inspections (IR-02) | Time since the last exchange vs the interval |
| Trigger event | Within 10 working days of a TMV replacement (IR-01); before sharing sensitive information (IR-11) | Due date set by an event in another system (CAFM work order, CDE share request) |

The difference matters for maintenance: scheduled (PPM) exchanges are *frequency* type, and reactive work creates *trigger* exchanges.

### 16.2 MIDP extract

| Exchange | Milestone | Meaning | Planned date |
|---|---|---|---|
| IE1 | M-203-S4 | Stage 4 technical design complete | 2027-01-15 |
| IE2 | M-203-IE2 | Pre-handover | 2027-04-16 |
| IE3 | M-203-PC | Practical completion and handover | 2027-06-04 |
| IE4 | M-203-REC | Record information (four weeks after handover) | 2027-07-02 |

The dates are the planned dates of the milestones. When the programme moves, the due dates move with it. The MIDP extract below shows them as dates so the checks can run before the programme link exists.

| Deliverable | Container | Exchange | Due date | Status required by due date |
|---|---|---|---|---|
| Architectural model | LRHC-FLD-ZZ-00-M3-A-000001 | IE1 | 2027-01-15 | S4 |
| Mechanical model | LRHC-KBS-ZZ-00-M3-M-000001 | IE1 | 2027-01-15 | S4 |
| Electrical model | LRHC-KBS-ZZ-00-M3-E-000001 | IE1 | 2027-01-15 | S4 |
| Public health model | LRHC-KBS-ZZ-00-M3-P-000001 | IE1 | 2027-01-15 | S4 |
| Door schedule | LRHC-FLD-ZZ-ZZ-SH-A-000001 | IE1 | 2027-01-15 | S4 |
| COBie (draft) | LRHC-BMC-ZZ-ZZ-IE-W-000001 | IE2 | 2027-04-16 | S3 |
| COBie (handover) | LRHC-BMC-ZZ-ZZ-IE-W-000001 | IE3 | 2027-06-04 | S4 |
| COBie (record) | LRHC-BMC-ZZ-ZZ-IE-W-000001 | IE4 | 2027-07-02 | CR |
| As-constructed federated model (IFC) | LRHC-BMC-ZZ-00-M3-W-000001 | IE3 | 2027-06-04 | S4 |
| As-constructed federated model (IFC) | LRHC-BMC-ZZ-00-M3-W-000001 | IE4 | 2027-07-02 | CR |
| O&M manual | LRHC-BMC-ZZ-ZZ-RP-W-000001 | IE3 | 2027-06-04 | S4 |
| O&M manual | LRHC-BMC-ZZ-ZZ-RP-W-000001 | IE4 | 2027-07-02 | CR |
| TMV commissioning report | LRHC-KBS-ZZ-ZZ-RP-P-000001 | IE3 | 2027-06-04 | S4 |
| Fire damper drop-test report | LRHC-KBS-ZZ-ZZ-RP-M-000001 | IE3 | 2027-06-04 | S4 |
| Integration specification (IR-16) | LRHC-KBS-03-ZZ-SP-M-000001 | IE1 | 2027-01-15 | S4 |
| Points schedule (draft) | LRHC-KBS-03-ZZ-SH-M-000001 | IE2 | 2027-04-16 | S3 |
| Points schedule (final) | LRHC-KBS-03-ZZ-SH-M-000001 | IE3 | 2027-06-04 | S4 |
| Data soak test report | LRHC-KBS-03-ZZ-RP-M-000001 | IE3 | 2027-06-04 | S4 |
| Network and device schedule (OFFICIAL-SENSITIVE) | LRHC-KBS-03-ZZ-SH-E-000001 | IE3 | 2027-06-04 | S4 |

| ID | Requirement | Checked in |
|---|---|---|
| MID-01 | Every MIDP container is in the document register by its due date. | REG |
| MID-02 | No container is in the register that is not in the MIDP (warning only). | REG |

The five connected-systems containers are new in P03. They use volume code `03`, as new containers do (Section 13.1).

---

## 17. Authorisation and acceptance (CRAV)

Every information container goes through four steps: **Check, Review, Approve, Verify (CRAV)**. The first three happen in the delivery team before anything reaches the ICB. Verify is the ICB's acceptance.

| Step | Who | What they do | Status after | Recorded in CDE |
|---|---|---|---|---|
| **Check** | Originator (task team) | Self-check against this EIR using the published rules and IDS (REF-12, REF-13). Fix fails before review. Attach the check report. | S0 (work in progress) | Check report attached |
| **Review** | Task team lead or discipline reviewer | Technical content, coordination with other disciplines, Assisted items | S0 | Reviewer, date, outcome |
| **Approve** | Task information manager, then the lead appointed party IM | Task IM approves sharing within the delivery team (S1–S3). The lead appointed party IM authorises submission to the ICB at an information exchange (S4). | S1–S4 | Approver, date |
| **Verify** | Appointing party IM with requirement owners | Run the acceptance checks; owners decide Assisted and Manual items; for asset data, trial-load into CAFM. Then accept, or reject with comments. | A*n* or CR if accepted; returned for a new P revision if rejected | Decision, date, check report |

| ID | Requirement | Verification |
|---|---|---|
| PRC-01 | No container reaches the ICB without Check, Review and Approve recorded in the CDE. | Auto (CDE metadata) |
| PRC-02 | Each submission includes the originator's self-check report from the published checking rules (REF-13). | Auto (report present) |
| PRC-03 | Reviewer and approver are named people, not the originator. | Auto (CDE metadata) |
| PRC-04 | Only the lead appointed party IM can authorise a submission to the ICB. | Auto (CDE permissions) |
| PRC-05 | The ICB decides (accept or reject) within 5 working days of a submission (KPI-04). This is the contract's period for reply for information (CON-05). | Auto (CDE timestamps) |
| PRC-06 | Asset data (COBie, points schedule) is accepted only after a trial load into the CAFM and data platform test environments completes with no rejected records. | Auto (load logs) |
| PRC-07 | A rejected container comes back with every failed requirement ID listed, so the fix can be targeted. | Auto (check report) |

### 17.1 Where accepted information goes

| Information | Destination system | How it gets there | Owner |
|---|---|---|---|
| Documents and drawings | ICB CDE, *Published* area, then the ICB document management system | CDE publish workflow | Appointing party IM |
| Models (IFC) | ICB asset information model viewer | CDE publish | Appointing party IM |
| Asset data (COBie) | CAFM asset register and PPM schedules; finance fixed-asset register (cost, life) | CAFM import template (REF-08) | Asset information manager |
| Points schedule | ICB data platform; CAFM (alarm-to-work-order mapping) | Platform interface (REF-11) | Estates Digital Lead |
| Live data | ICB data platform | Integration gateway (Section 6) | Estates Digital Lead |
| Sensitive information | Restricted CDE area | Approval by the Senior Security Risk Owner | Senior Security Risk Owner |

---

## 18. Acceptance criteria

The appointing party reviews each submission against this EIR. Automated checks report **fail**, **warn** or **flag**.

| ID | What happens | Result |
|---|---|---|
| ACC-01 | The IFC is not IFC4, either file will not open, or a required COBie sheet is missing (FMT-01 to FMT-03). | **Whole submission rejected** |
| ACC-02 | Any asset is in the IFC but not the COBie file, or the reverse, or the GUIDs do not match (FMT-04). | **Whole submission rejected** |
| ACC-03 | Any fail on a safety-critical asset (FD, FDM, TMV, NCU, EAC, emergency LF), or a fail on LOC-03 to LOC-05. | **Whole submission rejected** |
| ACC-04 | A container fails naming, status or revision rules (NAM-01, STA-01 to STA-04). | **That container rejected** |
| ACC-05 | Fails on other asset types: more than 5% of required-attribute checks fail. | **Whole submission rejected** |
| ACC-06 | Fails on other asset types: 5% or fewer. | Accepted with a correction list, due by the next exchange |
| ACC-07 | Warnings. | Do not fail a submission. The lead appointed party responds to each one. |
| ACC-08 | Flags from the free-text review (AIR-28). | **Never pass or fail anything.** A named person in the estates team reviews each flag and records the decision. |
| ACC-09 | A container fails a security rule (SEC-01 to SEC-05, or SEC-08). | **That container rejected and its sharing withdrawn** until the Senior Security Risk Owner confirms it's fixed |
| ACC-10 | A connected system fails INT-11 (point-to-point, end-to-end or soak test). | **That system is not accepted.** Its handover is deferred, and any KPI depending on it is reported as not measured until it passes |

A rejected submission returns to the lead appointed party and is resubmitted with the next P revision. Section 22 sets out the contract consequences.

---

## 19. KPIs and benefits

The KPIs show whether the information is doing its job. There are two sets:
- **Delivery KPIs** measure the information management itself. Most are calculated by the acceptance checks.
- **Outcome KPIs** measure the building in use, against the OIR outcomes in Section 4.1.

The benefits (19.3) explain why the ICB is asking for the information. They're reviewed at handover, at + 12 months and at + 24 months (IR-15).

Baselines marked *estimate* are set for this exercise. On a real project they'd come from the ICB's recent schemes.

### 19.1 Delivery KPIs (information management)

| ID | KPI | Measure | Target | Baseline | Data source | When measured | Owner |
|---|---|---|---|---|---|---|---|
| KPI-01 | First-time acceptance | Containers accepted at their first submission for an exchange ÷ all containers submitted (definition: CON-13) | ≥ 80% at IE2 to IE4 | Not measured on past schemes | Acceptance check decisions (Section 18) | Each exchange | Appointing party IM |
| KPI-02 | Safety-critical data right at handover | Safety-critical assets with no failed checks ÷ all safety-critical assets | 100% at IE3 | Not measured | Acceptance checks | IE3 | Appointing party IM |
| KPI-03 | Deliverables on time | MIDP deliverables at the required status by their due date ÷ all due | ≥ 95% | Not measured | Register vs MIDP (L2-01, L2-02) | Monthly | Project Sponsor |
| KPI-04 | Speed of acceptance | Working days from submission to accept/reject decision | ≤ 5 | 15 (*estimate*: manual review) | CDE timestamps (PRC-05) | Each submission | Appointing party IM |
| KPI-05 | Share of checks automated | Atomic requirements verified Auto ÷ all (Annex A) | ≥ 70% | 0% | Requirements register | Each EIR revision | Appointing party IM |
| KPI-06 | CAFM ready at handover | Maintainable assets and PPM schedules live in CAFM on the day of practical completion ÷ all | 100% | 12 weeks after handover (*estimate*) | CAFM load log (PRC-06) | M-203-PC | Maintenance Manager |
| KPI-07 | Data defects after acceptance | Assets needing a data correction in the first 3 months ÷ all assets | ≤ 2% | Not measured | CAFM change requests | Handover + 3 months | Maintenance Manager |
| KPI-08 | Live data completeness | Readings received ÷ readings expected, per month | ≥ 95% | No live data on past schemes | Data platform (INT-11, INT-12) | Soak test, then monthly | Estates Digital Lead |

Section 22.3 says which delivery KPIs are in the contract's Incentive Schedule (CON-12).

### 19.2 Outcome KPIs (building in use)

| ID | KPI | Outcome | Target | Data source | Frequency | Owner |
|---|---|---|---|---|---|---|
| KPI-11 | Energy intensity | OIR-ENV-01 | ≤ 110 kWh/m²/year | Energy meters (IR-16) | Monthly | Energy and Sustainability Manager |
| KPI-12 | Water intensity | OIR-ENV-03 | ≤ 0.6 m³/m²/year | Water meters (IR-16) | Monthly | Energy and Sustainability Manager |
| KPI-13 | Clinical room availability | OIR-SOC-01 | ≥ 98% of session hours | CAFM downtime records | Monthly | Maintenance Manager |
| KPI-14 | Room utilisation | OIR-SOC-02 | ≥ 75% of session hours occupied | Occupancy sensors (IR-16) | Monthly | Space Planner |
| KPI-15 | Safety-critical PPM on time | OIR-SOC-03 | 100% | CAFM; emergency lighting self-test data | Monthly | Maintenance Manager |
| KPI-16 | Scald-risk response | OIR-SOC-03 | Water temperature alarm to work order raised: ≤ 5 minutes; to attended: ≤ 4 hours | Data platform + CAFM timestamps | Each alarm | Responsible Person (Water) |
| KPI-17 | Facilities operating cost | OIR-ECO-02 | ≤ business case budget (£/m²/year) | Finance and CAFM | Annually | Capital Accountant |

### 19.3 Benefits

Each benefit runs from an **enabler** (the information asked for), through a **change** (what people do differently), to the **benefit**, which serves an **objective** (the OIR outcome).

| ID | Enabler | Change | Benefit | Objective | Measured by | Owner | When |
|---|---|---|---|---|---|---|---|
| BEN-01 | Checked COBie and PPM data (IR-03) | CAFM is loaded before handover instead of surveying assets afterwards | FM is ready on day one. About 12 weeks of post-handover data collection avoided (*estimate*: 240 hours of FM administration) | OIR-SOC-01 | KPI-06, KPI-07 | Maintenance Manager | Handover |
| BEN-02 | Atomic, rule-checked requirements (Annex A, B) | The appointing party IM reviews only fails, warnings and flags | Faster, consistent acceptance: decision in 5 working days, not 15 (*estimate*) | OIR-ECO-01 | KPI-01, KPI-04, KPI-05 | Appointing party IM | Each exchange |
| BEN-03 | Safety-critical asset data and live monitoring (IR-01, IR-02, IR-16) | Compliance tasks are scheduled from correct data; monitoring replaces some manual testing | No overdue safety-critical maintenance; fewer manual temperature and emergency lighting tests | OIR-SOC-03 | KPI-02, KPI-15 | Responsible Person (Water); Fire Safety Manager | Year 1 |
| BEN-04 | Metered energy and water data (IR-06, IR-16) | Faults and waste found from data within weeks, not at the annual bill | The building meets its design energy target; any gap is explained in year 2 | OIR-ENV-01, OIR-ENV-03 | KPI-11, KPI-12 | Energy and Sustainability Manager | Year 1 and 2 |
| BEN-05 | Water temperature alarms linked to CAFM (IR-16) | Alarms raise work orders automatically | Scald risk is dealt with in hours, not found at the next routine test | OIR-SOC-03 | KPI-16 | Responsible Person (Water) | Year 1 |
| BEN-06 | Occupancy data (IR-16) | Sessions are planned from measured room use | Better use of clinical rooms; evidence for future space decisions on the campus | OIR-SOC-02 | KPI-14 | Space Planner | Year 1 and 2 |

### 19.4 Dis-benefits and risks to the benefits

| Dis-benefit or risk | Affects | How it's managed |
|---|---|---|
| More connected devices means more cyber exposure | BEN-03 to BEN-06 | SEC-08, SEC-09; segregated building network |
| Someone has to look after the live data | BEN-04 to BEN-06 | Estates Digital Lead named; monthly data quality report during defects (INT-12) |
| Automated checks can be trusted too much | BEN-02 | Assisted and Manual items still go to named reviewers; checks are tested against known errors before each use |
| Baselines are estimates | All | Replace with measured values from the next ICB scheme before the business case review |

---

## 20. What the lead appointed party submits at each exchange

1. The IFC4 model(s) and the COBie 2.4 file named in the MIDP.
2. A document register (`.csv` or `.xlsx`) listing every container with name, title, status, revision, date and security marking (SEC-01).
3. Their own check report against this EIR (self-check before submission).
4. For sensitive entities: the access list for each OFFICIAL-SENSITIVE container (SEC-03).
5. For connected systems: the points schedule, integration specification and test records (INT-01). The network and device schedule goes separately to ICB IT/OT security (SEC-08).
6. A CRAV record for every container (PRC-01).

---

## 21. Tender response requirements

The pre-appointment BEP must respond to each item below. Information management is 15% of the quality score (*project target*).

| ID | The BEP must set out | Weight within information management |
|---|---|---|
| TND-01 | How CRAV will run in the delivery team's tools, and who holds each role (Section 17) | 20% |
| TND-02 | The approach to connected systems: proposed protocols, gateways, Brick or Haystack tagging, how INT-11 testing will be run (Section 6) | 25% |
| TND-03 | How models will be set up to the spatial coordination requirements (Section 11) | 10% |
| TND-04 | The security approach for sensitive and connected-system information (Section 15) | 15% |
| TND-05 | How the delivery team will self-check against the published rules before each submission, and how it will report KPI-01 to KPI-08 | 15% |
| TND-06 | Proposed improvements: for example, automated transmittals, direct CDE-to-CAFM integration, earlier soak testing. Agreed improvements go into the confirmed BEP and information protocol. | 15% |

---

## 22. Contractual mechanisms (NEC4)

This section says how the requirements in this EIR are enforced through the contract. It's written for the ICB's commercial and legal advisers, who own the contract wording. Nothing here changes a requirement elsewhere in this EIR.

### 22.1 Assumed contract

| Item | Assumption |
|---|---|
| Route | NHS ProCure23 (P23) framework, NEC4 project agreement |
| Main contract | NEC4 Engineering and Construction Contract (ECC), Option C (target contract with activity schedule) |
| Secondary options used | X7 delay damages; X10 information modelling; X20 key performance indicators. X5 sectional completion is not used (single building) |
| Information protocol | Not used separately. X10 carries the requirements through the Scope (CON-01) |
| Dispute resolution | As stated in the contract (W2 where the Housing Grants Act applies) |

The clause numbers below are NEC4 ECC June 2017 with amendments. The P23 project agreement may amend them. Open point 17 (Annex C).

### 22.2 Contract requirements

| ID | Requirement | Verification |
|---|---|---|
| CON-01 | X10 is used. The Information Model Requirements in the Scope are this EIR and the annexes issued with it (REF-01, REF-12, REF-13), at the revision stated in Contract Data part one. They change only through an instruction changing the Scope, which is a compensation event (60.1(1)). | Manual |
| CON-02 | The Scope states that the information containers in the MIDP are part of the works. Information that doesn't meet the acceptance criteria (Section 18) is therefore a Defect (11.2(6)). | Manual |
| CON-03 | The confirmed BEP is the Information Execution Plan. If it isn't identified in Contract Data part two, the first one is submitted for acceptance within 2 weeks of the Contract Date. It's revised with each revised programme and before each exchange, and its MIDP dates match the Accepted Programme. | Auto (REG; MIDP against programme) |
| CON-04 | The Project Manager holds the client's information management actions under X10. Before IE1 the Project Manager notifies the Contractor (14.2) that these are delegated: acceptance of the Information Execution Plan and of information submissions to the appointing party information manager; acceptance of sensitive information to the Senior Security Risk Owner. The Supervisor witnesses the INT-11 tests and notifies Defects found in them. | Manual |
| CON-05 | The period for reply for information submissions is 1 week, matching PRC-05 and KPI-04. A late reply is a compensation event (60.1(6)). | Auto (CDE timestamps) |
| CON-06 | A rejection under Section 18 is the Project Manager's non-acceptance (13.4). The reason given is that the information doesn't comply with the Scope, and the check report lists every failed requirement ID (PRC-07). | Auto (check report) |
| CON-07 | Rejected information, and each item on an ACC-06 correction list, is a notified Defect. The defect correction period for information is 2 weeks (*project target*). If a Defect isn't corrected in time, the Project Manager assesses the cost of having it corrected by others and the Contractor pays it (46.1). Under Option C, correcting Defects after Completion is Disallowed Cost. | Auto (REG: resubmission date against notification) |
| CON-08 | Two Key Dates are set. KD-1: IE1 information accepted with no rejection under ACC-01 to ACC-05, by the planned date of M-203-S4. KD-2: the same for IE2, by M-203-IE2. If a Condition isn't met by its Key Date, the Contractor pays the additional cost the Client incurs on the project (25.3). | Auto (decision log against Key Dates) |
| CON-09 | The Scope states that Completion requires: IE3 information accepted with no rejection under ACC-01 to ACC-05, ACC-09 or ACC-10; the CAFM and data platform trial loads passed (PRC-06); and the connected system tests passed (INT-11). | Auto (decision log; load logs; test records) |
| CON-10 | X7 is used at the rate in Contract Data part one (set by the ICB's commercial team; not stated in this exercise). Because of CON-09, late or rejected handover information delays Completion and delay damages run. | Manual |
| CON-11 | The activity schedule has one information management activity per exchange (IE1 to IE4). Each is complete only when its exchange is accepted. IE4 comes after Completion, so this is the main lever for record information. | Auto (decision log) |
| CON-12 | The Incentive Schedule (X20) holds KPI-01, KPI-03, KPI-07 and KPI-08. The other KPIs stay out of it, for the reasons in 22.3. | Manual |
| CON-13 | KPI-01 is measured per container. A container counts once per exchange (IE2 to IE4). It counts as first-time accepted if its first submission for that exchange is accepted, including acceptance with a correction list (ACC-06). Warnings and flags never count against it. A rejection overturned under CON-14 is removed. Security rejections (ACC-09) count. The figure comes from the checker decision log and CDE timestamps, and is reported monthly with a forecast of the final result. | Auto (decision log) |
| CON-14 | The Contractor may notify, within 5 working days of a rejection, that it believes the rejection is wrong. The Project Manager (or delegate) decides within 5 working days. If the Contractor is right, the rule is corrected (CHK-05) and the rejection is removed from KPI-01. A disagreement goes through the contract's dispute resolution procedure. | Assisted |
| CON-15 | The Contractor has the same checking rules and checker version as the ICB throughout (CHK-01, PRC-02). Each check report states the rules revision used. A change to the rules comes only with a revision of this EIR, so it's a change to the Scope. | Auto (rules revision in check report) |
| CON-16 | Either party gives an early warning (15.1) of anything that could delay an exchange, stop an X20 KPI reaching its target or impair the information in use. Early warning register entries cite the requirement IDs affected. If the forecast for an X20 KPI misses its target, the Contractor submits proposals for improving performance (X20.3) and revises the Information Execution Plan to match. | Assisted |
| CON-17 | If the same requirement ID fails at two submissions in a row after a Defect has been notified, it's discussed at the next early warning meeting and the actions are recorded. If the failure continues, the Project Manager may, after advice, notify a default for substantial failure to comply (91.2, R11). The Contractor then has 4 weeks to put it right. | Manual |
| CON-18 | Option Z is kept to a minimum. It's used only to align X10 terms with BS EN ISO 19650 where needed. KPI damages are not used: consequences come from CON-02 to CON-11. | Manual |

### 22.3 Which lever applies to each item

| Item | Contract lever | What happens if it's missed | Clauses |
|---|---|---|---|
| ACC-01 to ACC-05 (submission rejected) | Non-acceptance; Defect | Corrected at the Contractor's cost. At IE1 or IE2 the Key Date may be missed. At IE3 Completion can't be reached | CON-06 to CON-09 |
| ACC-06 (accepted with correction list) | Defect | Corrected within the defect correction period | CON-07 |
| ACC-07, ACC-08 (warnings, flags) | None | Response recorded; no contract consequence | — |
| ACC-09 (security fail) | Non-acceptance; Defect; sharing withdrawn | As ACC-01 to ACC-05. Repeated fails escalate | CON-06, CON-07, CON-17 |
| ACC-10 (connected system fails tests) | Completion | No Completion, so delay damages run | CON-09, CON-10 |
| MID-01 (container late) | Key Date; Completion; activity schedule | Client's extra cost (IE1, IE2); delay damages (IE3); not paid until accepted (all) | CON-08 to CON-11 |
| MID-02 (container not in MIDP) | None | Warning only | — |
| PRC-05 (ICB decision time) | Period for reply | A late reply is a compensation event for the Contractor | CON-05 |
| KPI-01, KPI-03, KPI-07, KPI-08 | X20 | No incentive payment; improvement proposals if forecast to miss | CON-12, CON-13, CON-16 |
| KPI-02 (safety-critical data 100%) | Scope (ACC-03) | It's mandatory, so it's a rejection, not an incentive | CON-06 |
| KPI-04, KPI-05 | None | They measure the ICB, not the Contractor | — |
| KPI-06 (CAFM ready at handover) | Completion, for the Contractor's part | The trial load is a Completion condition. The live load depends on the ICB's own team, so the KPI isn't contractual | CON-09 |
| KPI-11 to KPI-17 (building in use) | None in this contract | Depend on how the building is run. Reviewed in the benefits reviews (IR-15) | — |
| IE4 record information | Activity schedule; Defects | Not paid until accepted; correction after Completion is Disallowed Cost | CON-07, CON-11 |

### 22.4 What happens when information fails

1. **Check result.** The acceptance checks reject a container. The check report lists every failed requirement ID (PRC-07).
2. **Non-acceptance and Defect.** The delegate notifies non-acceptance within the period for reply (CON-05, CON-06). The failed items are notified Defects (CON-07).
3. **Challenge (optional).** The Contractor can challenge a rejection it believes is wrong (CON-14).
4. **Correction.** The Contractor fixes the information and resubmits at the next P revision, within the defect correction period.
5. **Early warning.** If the fix threatens an exchange, a Key Date, Completion or an X20 KPI, it goes on the early warning register. Improvement proposals follow for a KPI forecast to miss (CON-16).
6. **Money.** These follow automatically:
   - unpaid activity (CON-11);
   - the Client's extra cost for a missed Key Date (CON-08);
   - delay damages if Completion is late (CON-10);
   - lost incentive payment (CON-12);
   - the cost of others correcting a Defect that isn't fixed (CON-07).
7. **Persistent failure.** The same failure repeats after notification. It's escalated, and only as a last step a default notice is given (CON-17).

**Note on the checker.** Because rejections now have contract consequences, the checking rules become contract evidence. That's why CON-13 to CON-15 exist: one definition of the measure, one set of rules shared by both parties, and a route to correct a rule that's wrong.

---

# Annexes

## Annex A: Requirements register

`eir_requirements_register.csv` (issued with REF-01) lists every atomic requirement in Section 5: 135 rows, of which 125 are requirements and 10 are components marked *none required*. Each row has its ID, owner, component, requirement text, verification, what verifies it, and the outcomes and KPIs it supports. The tables in Section 5 are generated from it.

---

## Annex B: Checking configuration

The ICB checks submissions automatically against this EIR. Checking rules **implement** the EIR and never add to it.

| ID | Requirement | Verification |
|---|---|---|
| CHK-01 | The rules used for acceptance are published as REF-13 at the **same revision as this EIR**. The rules file states which EIR revision it implements. | Auto |
| CHK-02 | Every rule cites the clause or requirement ID it checks. A rule with no ID isn't used. | Auto |
| CHK-03 | When this EIR is revised, the changed clauses are listed (by comparing the old and new revisions), and every rule citing them is reviewed before the next exchange. | Assisted |
| CHK-04 | Before each use, the checks are run on a sample with known errors and on a clean sample. Any missed error or false alarm is fixed before acceptance checks run. | Auto |
| CHK-05 | Where a check result and this EIR disagree, the EIR prevails, and the rule is corrected. | Manual |

The checks run in four layers:
1. Metadata against the data dictionary
2. Status against the programme
3. Content and consistency across files
4. Free-text flagging, where a person decides

The table below shows how the 125 atomic requirements in Annex A are verified.

| Component | Auto | Assisted | Manual | Total |
|---|---|---|---|---|
| LOIN – graphical | 9 | 2 | 3 | 14 |
| LOIN – non-graphical | 24 | 2 | 0 | 26 |
| LOIN – documentation | 9 | 12 | 4 | 25 |
| Acceptance criteria | 12 | 5 | 6 | 23 |
| Supporting information | 12 | 0 | 1 | 13 |
| Exchange date | 24 | 0 | 0 | 24 |
| **All except supporting information** | **78 (70%)** | **21 (19%)** | **13 (12%)** | **112** |

28 of the 112 are already covered by a rule in the current checking rules; the rest name a planned rule (in brackets) or a role.

---

## Annex C: Open points

| # | Raised | Point | Status |
|---|---|---|---|
| 1 | P01 | Staff room and plant room use Uniclass group codes (SL_90_20, SL_90_90): no leaf code found | Open: check against the October 2026 release (REF-02) |
| 2 | P01 | Maintenance intervals (AIR-19) and the 41 °C set point (AIR-23) are project requirements | Accepted; revisit with the Responsible Person (Water) |
| 3 | P01 | 5% threshold for non-critical fails (ACC-05) | Accepted |
| 4 | P01 | COBie Job and Attribute sheets required (FMT-03) | Closed |
| 5 | P01 | Document register as a separate input | Closed |
| 6 | P02 | Campus entity list, including MA 4920.200 | Open |
| 7 | P02 | *Project target* values in Section 4.1 | Open |
| 8 | P02 | Volume codes `00`–`07` | Open |
| 9 | P02 | Security threats and risk scores | Open |
| 10 | P02 | Milestone IDs: fix before the P6 programme is built | Open |
| 11 | P02 | ACC-09 (security fails reject the container) | Open |
| 12 | P03 | CRAV defined as Check, Review, Approve, Verify (Section 17) | Closed |
| 13 | P03 | KPI baselines marked *estimate* to be replaced with measured values from a recent ICB scheme | Open |
| 14 | P03 | Brick or Haystack for point tagging (INT-05): Brick set as default, BEP may propose Haystack | Open |
| 15 | P03 | SP-01 height (50.000 m AOD) is a placeholder until the topographical survey | Open |
| 16 | P03 | Information management weighting 15% of quality score (Section 21) | Open |
| 17 | P04 | Contract form assumed: NEC4 ECC Option C under P23 (22.1). Clause numbers to be confirmed against the P23 project agreement by the ICB's legal advisers | Open |
| 18 | P04 | Whether the Scope can define information containers as part of the works (CON-02). The Defect route depends on it | Open |
| 19 | P04 | Delay damages rate (CON-10) and the 2-week defect correction period for information (CON-07) | Open |
| 20 | P04 | Incentive Schedule: payment amounts and any tiers for KPI-01, KPI-03, KPI-07, KPI-08 (CON-12) | Open |

---

*NEC4 clause references checked against published NEC guidance on 19 November 2026; they are not legal advice. Uniclass codes checked against uniclass.thenbs.com on 16 November 2026. Status codes follow BS EN ISO 19650-2 National Annex Table NA.1.*
