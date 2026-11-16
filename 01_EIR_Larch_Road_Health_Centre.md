# Exchange Information Requirements (EIR)
**Project:** Larch Road Health Centre (project code **LRHC**)
**Document:** LRHC-LRV-ZZ-ZZ-SP-K-000001 · Status S2 · Revision P01 · Draft for review
**Standard:** BS EN ISO 19650-2:2018 and its UK National Annex

> This is a fictional project made for a test exercise. All organisation names are invented.

Each requirement has an ID (e.g. `AIR-07`). The rules file in Stage 2 points back to these IDs. The **Checked in** column says where an automated check will look: **IFC** (model), **COBie** (spreadsheet) or **REG** (document register).

---

## 1. Project and parties

| Role (UK NA term) | Organisation | Originator code |
|---|---|---|
| Appointing party | Larch Valley ICB, Estates team | LRV |
| Lead appointed party | Brook & Mason Construction Ltd (main contractor) | BMC |
| Appointed party (architect) | Field Architects | FLD |
| Appointed party (building services) | Kestrel Building Services | KBS |

**Facility:** single-storey GP practice and clinic with paediatric care. 19 spaces and about 47 maintainable assets (see Section 4).

**Level of information need:** this EIR covers alphanumerical information only (attributes, classification, names). It does not set geometry requirements.

---

## 2. Information purposes

| ID | Purpose | What the estates team will do with the information |
|---|---|---|
| PUR-01 | **Operation and maintenance (O)** | Load assets and planned maintenance into the CAFM system on day one. Raise reactive jobs against the right asset and location. Track warranties. |
| PUR-02 | **Compliance (C)** | Plan statutory and safety testing: fire doors, fire dampers, thermostatic mixing valves (scald risk), nurse call and emergency assistance call, emergency lighting. |
| PUR-03 | **Space management (S)** | Hold a correct room list with classification, area and patient-area flag for planning, cleaning and infection control. |

Every attribute in Section 5 is tagged with the purpose(s) it serves.

---

## 3. Exchange formats

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

## 4. Spaces and assets in scope

### 4.1 Space schedule

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
| 00-015 | Staff room | SL_90_20 Common spaces *(group code, see Section 11)* | N |
| 00-016 | Staff WC | SL_35_80_89 Toilets | N |
| 00-017 | Plant room | SL_90_90 Plant and control spaces *(group code, see Section 11)* | N |
| 00-018 | Store | SL_90_50_35 General storerooms | N |
| 00-019 | Corridor | SL_90_10_15 Corridors | N |

One floor: **00** (ground).

### 4.2 Asset types

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

### 4.3 Where assets must be

| ID | Requirement | Checked in |
|---|---|---|
| LOC-01 | Every asset sits in exactly one space: contained in or referenced by one `IfcSpace`, with the same space in COBie `Component.Space`. | IFC + COBie |
| LOC-02 | Every space belongs to floor 00 (`IfcBuildingStorey` / COBie `Space.FloorName`). | IFC + COBie |
| LOC-03 | Every washbasin in a space with Patient area = Y is served by a TMV in the same space (see AIR-23). | COBie |
| LOC-04 | Each treatment room, the paediatric clinic room and the nurse room has at least one NCU. Each accessible WC has at least one EAC. | COBie |
| LOC-05 | The corridor and the plant room each have at least one emergency light fitting. | COBie |

---

## 5. Asset information requirements (AIR)

### 5.1 Common attributes

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

### 5.2 Value rules for common attributes

| ID | Requirement | Checked in |
|---|---|---|
| AIR-15 | `Type.Manufacturer` is an email address that exists in the COBie Contact sheet (COBie links manufacturers through Contact). | COBie |
| AIR-16 | Required fields are not blank and not a placeholder (`n/a`, `TBC`, `-`, `0`, `unknown`). | IFC + COBie |
| AIR-17 | Warranty start date is on or after the installation date. | COBie |
| AIR-18 | Installation date is not later than the date of the submission. | COBie |
| AIR-19 | Maximum maintenance intervals (project requirement, set by the appointing party): AHU 6 months · FD 6 months · FDM 12 months · TMV 6 months · NCU/EAC 6 months · emergency LF 1 month. | COBie |

### 5.3 Type-specific attributes

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
| AIR-27 | Space | NetArea (m²); PatientArea | Number greater than 0; `Y`/`N` matching Section 4.1 | S |

### 5.4 Free-text requirement (human review)

| ID | Requirement | Checked in |
|---|---|---|
| AIR-28 | Each maintenance task description (AIR-14) states the actual tasks, not just "service as per manufacturer". For TMVs it must include an **outlet temperature check** and a **fail-safe test (cold supply isolation)**. For fire dampers it must include a **drop test and reset**. | COBie (automated flag only; a person decides, see Section 9) |

---

## 6. Naming

### 6.1 Information containers (documents, models, COBie files)

Pattern: **Project – Originator – Volume – Level – Type – Role – Number**, separated by hyphens.

| Field | Allowed values |
|---|---|
| Project | `LRHC` |
| Originator | `LRV`, `BMC`, `FLD`, `KBS` |
| Volume / system | `ZZ` (all), `XX` (none) |
| Level / location | `00` (ground), `RF` (roof), `ZZ` (multiple), `XX` (none) |
| Type | `M3` 3D model, `M2` 2D model, `DR` drawing, `SH` schedule, `SP` specification, `RP` report, `IE` information exchange file |
| Role | `A` architect, `E` electrical, `M` mechanical, `P` public health, `W` contractor, `K` client, `Z` general |
| Number | 6 digits, e.g. `000001` |

Example: `LRHC-KBS-ZZ-00-M3-M-000001`

| ID | Requirement | Checked in |
|---|---|---|
| NAM-01 | Every container name matches the pattern and uses only the allowed values above. | REG + COBie (Document sheet) |
| NAM-02 | Each container name is unique in the register. | REG |

### 6.2 Assets, types and spaces

| ID | Requirement | Pattern | Example | Checked in |
|---|---|---|---|---|
| NAM-03 | Asset (component) names: asset code, level, 3-digit number | `AAA-00-NNN` | `TMV-00-004` | IFC + COBie |
| NAM-04 | Asset names are unique across the facility. | | | IFC + COBie |
| NAM-05 | Type names: asset code, `Type`, 2-digit number | `AAA-TypeNN` | `TMV-Type01` | IFC + COBie |
| NAM-06 | Space names: level, 3-digit number. Room name goes in Description. | `00-NNN` | `00-010` | IFC + COBie |
| NAM-07 | The asset code at the start of each name matches the asset type's classification in Section 4.2. | | | IFC + COBie |

---

## 7. Status codes and revisions (UK National Annex)

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

## 8. Delivery milestones (MIDP extract)

Information exchanges: **IE1** Stage 4 technical design · **IE2** pre-handover · **IE3** practical completion and handover · **IE4** record information (four weeks after handover).

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

| ID | Requirement | Checked in |
|---|---|---|
| MID-01 | Every MIDP container is in the document register by its due date. | REG |
| MID-02 | No container is in the register that is not in the MIDP (warning only). | REG |

---

## 9. Acceptance criteria

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

A rejected submission returns to the lead appointed party and is resubmitted with the next P revision.

---

## 10. What the lead appointed party submits at each exchange

1. The IFC4 model(s) and the COBie 2.4 file named in the MIDP.
2. A document register (`.csv` or `.xlsx`) listing every container with name, title, status, revision and date.
3. Their own check report against this EIR (self-check before submission).

---

## 11. Open points for review (Fred)

1. **Staff room and plant room SL codes.** I couldn't find a leaf-level Uniclass code for either, so both use group codes (SL_90_20, SL_90_90). Keep them, pick another code, or let the checker accept group codes for these two rooms only?
2. **Maintenance intervals (AIR-19)** and the **41 °C set point (AIR-23)** are written as project requirements for this exercise, not as quotes from guidance. Change any you'd set differently.
3. **5% threshold (ACC-05).** Keep it, or make every fail a rejection?
4. **Job and Attribute sheets** are added to the COBie sheet list. They're needed for maintenance intervals and type-specific attributes. Stage 3 will need to generate them.
5. **Document register** is a separate input (Section 10). Stage 3 will generate a sample one with seeded errors.

---

*Uniclass codes checked against uniclass.thenbs.com on 16 November 2026. Status codes follow BS EN ISO 19650-2 National Annex Table NA.1.*
