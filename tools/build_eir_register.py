"""EIR P03: information requirements as atomic, uniquely numbered rows.

ID tree:  IR-04 (requirement) -> IR-04.AC (component) -> IR-04.AC.03 (one atomic requirement)
Components: G graphical, NG non-graphical, D documentation (the three LOIN parts),
            AC acceptance criteria, SI supporting information, EX exchange date.
Verification: Auto = a rule passes/fails it; Assisted = a rule finds candidates or checks form, a person decides;
              Manual = judgement, inspection or a third party.
"Verified by" names the rule (rules.csv), the planned rule (in brackets) or the role.

Writes: eir_requirements_register.csv, _ir_tables.md, _ir_stats.md
"""
import csv
import sys
from collections import Counter
from pathlib import Path

OUT = Path(sys.argv[1])
COMP = {"G": "LOIN – graphical", "NG": "LOIN – non-graphical", "D": "LOIN – documentation",
        "AC": "Acceptance criteria", "SI": "Supporting information", "EX": "Exchange date"}

# (id, title, owner, story, outcomes, kpis, {comp: [(text, verification, verified_by), ...]})
IRS = [
 ("IR-01", "Scald protection (TMVs)", "ICB Estates – Responsible Person (Water)",
  "As the Responsible Person (Water), I need to test and maintain every thermostatic mixing valve that serves a patient basin, so that patients, especially children, are not scalded and the water safety plan can be audited.",
  "OIR-SOC-03", "KPI-02, KPI-15, KPI-16",
  {"G": [("Each TMV is modelled as a symbolic object inside its room, within 1 m of the basin it serves.", "Auto", "(geometry rule)")],
   "NG": [("Each TMV carries the attributes in AIR-08 to AIR-23.", "Auto", "L1-04, L1-08"),
          ("Each basin in a patient area is served by exactly one TMV in the same room.", "Auto", "L3-13")],
   "D": [("One commissioning certificate per TMV, linked to that TMV in the COBie Document sheet.", "Auto", "(document link rule)"),
         ("Each certificate records the measured outlet temperature at commissioning.", "Assisted", "RP (Water); layer 4 flag")],
   "AC": [("TMV3 approval and a 41 °C set point at washbasins.", "Auto", "L1-08"),
          ("Water temperature monitoring at each TMV outlet is live and linked to the TMV (IR-16).", "Auto", "(INT rules)")],
   "SI": [("ICB water safety plan template (REF-06).", "Auto", "appointing party issues before tender"),
          ("HTM 04-01 (reference standard).", "Manual", "designer")],
   "EX": [("At M-203-PC.", "Auto", "L2-02"),
          ("In operation: within 10 working days of any TMV replacement (trigger).", "Auto", "(CAFM event rule)")]}),
 ("IR-02", "Fire safety (doors and dampers)", "ICB Estates – Fire Safety Manager",
  "As the Fire Safety Manager, I need to inspect and maintain every fire door and fire damper on the compartment lines, so that the fire strategy works as designed and the fire risk assessment stays valid.",
  "OIR-SOC-03", "KPI-02, KPI-15",
  {"G": [("Each fire door and damper sits in a wall between two spaces.", "Auto", "(geometry rule)"),
         ("That wall is a compartment line in the fire strategy.", "Assisted", "Fire Safety Manager")],
   "NG": [("Fire rating, certification number, actuation type and PPM interval (AIR-20 to AIR-22).", "Auto", "L1-04, L1-08, L1-22")],
   "D": [("Fire strategy report and plans.", "Assisted", "Fire Safety Manager"),
         ("Damper drop-test record and doorset certificate per asset, linked to the asset.", "Auto", "(document link rule)")],
   "AC": [("Data conforms to the data dictionary.", "Auto", "layer 1 rules"),
          ("Design complies with HTM 05-02 and BS 9999.", "Manual", "fire engineer")],
   "SI": [("Existing MA 4920 site fire plan (REF-05).", "Auto", "appointing party issues before tender")],
   "EX": [("At M-203-PC.", "Auto", "L2-02"),
          ("In operation: inspection records every 6 months.", "Auto", "(frequency rule)")]}),
 ("IR-03", "Planned maintenance in CAFM", "ICB Estates – Maintenance Manager",
  "As the Maintenance Manager, I need every maintainable asset and its PPM schedule loaded into CAFM before the building opens, so that nothing is missed in the first year and clinical rooms stay available.",
  "OIR-SOC-01, OIR-SOC-03", "KPI-06, KPI-07, KPI-13",
  {"G": [("Each maintainable asset is in exactly one room.", "Auto", "L3-04")],
   "NG": [("Asset register fields AIR-01 to AIR-19, plus the ICB classification code (AIR-29).", "Auto", "L1-04, L1-05, (AIR-29 rule)"),
          ("The same assets, with the same GUIDs, in IFC and COBie.", "Auto", "L3-01, L3-02, L3-03"),
          ("A PPM job for every maintainable type, within the maximum interval.", "Auto", "L3-16, L1-22")],
   "D": [("An O&M manual section linked to every asset type.", "Auto", "(document link rule)"),
         ("The O&M content is correct for the installed product.", "Assisted", "Maintenance Manager")],
   "AC": [("A trial load into the CAFM test environment completes with no rejected records (PRC-06).", "Auto", "CAFM load log")],
   "SI": [("CAFM import template (REF-08); SFG20 schedule list.", "Auto", "appointing party issues before tender")],
   "EX": [("Draft at M-203-IE2; final at M-203-PC.", "Auto", "L2-01, L2-02"),
          ("Quarterly updates during the 12-month defects period.", "Auto", "(frequency rule)")]}),
 ("IR-04", "Space management", "ICB Estates – Space Planner",
  "As the Space Planner, I need an accurate room list with areas, classification and patient-area flags, so that I can plan clinical sessions, cleaning and infection control, and report space use to the ICB.",
  "OIR-SOC-02", "KPI-14",
  {"G": [("Space boundaries modelled to ±50 mm.", "Assisted", "survey comparison"),
         ("Net area from the space geometry is within 2% of the stated NetArea.", "Auto", "(geometry rule)")],
   "NG": [("Room name, SL code, net area and patient-area flag match the space schedule.", "Auto", "L1-17, L1-18, L1-19, L3-05")],
   "D": [("One room data sheet per space.", "Auto", "(document link rule)"),
         ("Room data sheet content is complete.", "Assisted", "Space Planner")],
   "AC": [("Space schedule in Section 8.1.", "Auto", "L3-05"),
          ("HBN 11-01 space standards are met.", "Manual", "architect")],
   "SI": [("Schedule of accommodation; room data sheet template (REF-07).", "Auto", "appointing party issues before tender")],
   "EX": [("At M-203-S4 (design) and M-203-PC (as built).", "Auto", "L2-02")]}),
 ("IR-05", "Capital asset register", "ICB Finance – Capital Accountant",
  "As the Capital Accountant, I need the replacement cost and expected life of each asset, so that I can set up depreciation and plan lifecycle replacement funding.",
  "OIR-ECO-01, OIR-ECO-02", "KPI-17",
  {"NG": [("Replacement cost (GBP) and expected life (years) for every asset type.", "Auto", "L1-04, L1-09")],
   "D": [("Cost reconciliation against the final account.", "Manual", "Capital Accountant")],
   "AC": [("Replacement cost within 10% of the final account line for the same asset type.", "Assisted", "rule compares if the final account is supplied as data")],
   "SI": [("ICB asset valuation guidance.", "Auto", "appointing party issues before tender")],
   "EX": [("At M-203-REC, with the final account.", "Auto", "L2-02")]}),
 ("IR-06", "Energy and water performance", "ICB Estates – Energy and Sustainability Manager",
  "As the Energy and Sustainability Manager, I need metered energy and water data against the design targets, so that I can show the building meets its operational targets in year 1 and explain any shortfall in year 2.",
  "OIR-ENV-01, OIR-ENV-02, OIR-ENV-03", "KPI-08, KPI-11, KPI-12",
  {"G": [("Each meter is located in a room.", "Auto", "L3-04")],
   "NG": [("Meter register: what each meter measures, units and point ID (via the points schedule, INT-02).", "Auto", "(INT rules)")],
   "D": [("Energy model report and metering strategy.", "Assisted", "Energy Manager"),
         ("Year 1 and year 2 performance reports.", "Assisted", "Energy Manager")],
   "AC": [("Meter data at least 95% complete each month.", "Auto", "data platform check"),
          ("Measured performance against the OIR targets.", "Auto", "KPI-11, KPI-12 calculation")],
   "SI": [("Design energy targets; NHS Net Zero Building Standard; point naming standard (REF-09).", "Auto", "appointing party issues before tender")],
   "EX": [("Monthly meter data from handover.", "Auto", "(frequency rule)"),
          ("Performance reports at handover + 12 and + 24 months.", "Auto", "(milestone rule)")]}),
 ("IR-07", "Business continuity", "ICB – Business Continuity Manager",
  "As the Business Continuity Manager, I need details of all emergency plans and escape routes, so that I can prepare, maintain and implement the business continuity plan.",
  "OIR-SOC-04", "",
  {"G": [("Escape routes and assembly points on plans.", "Manual", "Business Continuity Manager")],
   "NG": [("A critical-services link for every critical asset (which service it supports, which supply feeds it).", "Assisted", "rule checks the link exists; manager checks it's right")],
   "D": [("Emergency plan and escape route document using the ICB template headings.", "Assisted", "rule checks headings; manager checks content")],
   "AC": [("ICB emergency plan template (REF-10).", "Assisted", "template structure check")],
   "SI": [("Existing MA 4920 business continuity plan.", "Auto", "appointing party issues before tender")],
   "EX": [("Last working day of each quarter (fixed).", "Auto", "(calendar rule)")]}),
 ("IR-08", "Infection prevention and control", "Clinical – Infection Prevention and Control Lead",
  "As the IPC Lead, I need to confirm that clinical rooms have the right basins and finishes, so that cross-infection risk is controlled before the building opens to patients.",
  "OIR-SOC-01", "",
  {"NG": [("Every clinical room has a clinical washbasin (Pr_40_20_96_35).", "Auto", "(room-to-product rule)"),
          ("Finish type recorded per room.", "Auto", "(data dictionary row)")],
   "D": [("IPC sign-off record before occupation.", "Assisted", "IPC Lead signs")],
   "AC": [("HBN 00-09 and HBN 00-03.", "Manual", "IPC Lead")],
   "SI": [("HBN 00-09; room data sheet template (REF-07).", "Auto", "appointing party issues before tender")],
   "EX": [("At M-203-S4 (design review) and M-203-PC (before occupation).", "Auto", "L2-02")]}),
 ("IR-09", "Accessibility", "ICB Estates – Equality and Access Lead",
  "As the Equality and Access Lead, I need evidence that accessible WCs and assistance calls are provided and working, so that the practice meets its Equality Act duties and patients can call for help.",
  "OIR-SOC-01", "",
  {"G": [("Accessible WC dimensions at or above the Approved Document M minimum.", "Auto", "(geometry rule)"),
         ("Accessible WC layout (transfer space, grab rails).", "Manual", "access consultant")],
   "NG": [("An emergency assistance call in each accessible WC (AIR-24).", "Auto", "L3-14")],
   "D": [("Access statement; commissioning test of each assistance call.", "Assisted", "Access Lead")],
   "AC": [("Approved Document M; BS 8300-2.", "Manual", "access consultant")],
   "EX": [("At M-203-S4 and M-203-PC.", "Auto", "L2-02")]}),
 ("IR-10", "Delivery assurance (MIDP and programme)", "ICB – Project Sponsor (MA 4920.203)",
  "As the Project Sponsor, I need to see each deliverable's status against the programme, so that I can spot information that will delay construction or handover before it does.",
  "OIR-ECO-01", "KPI-01, KPI-03, KPI-04",
  {"NG": [("Document register with status, revision, date and security marking.", "Auto", "L1-24, L1-25, SEC-01"),
          ("Each MIDP deliverable linked to a programme activity or milestone ID.", "Auto", "(programme link rule)"),
          ("Each deliverable due before the activity that needs it starts.", "Auto", "(programme logic rule)")],
   "D": [("Monthly information delivery report.", "Auto", "generated from check results")],
   "AC": [("Status and revision rules (Section 14) and MIDP dates.", "Auto", "L2-01 to L2-04")],
   "SI": [("MA 4920 programme (P6 export) and MIDP template (REF-14).", "Auto", "appointing party issues before tender")],
   "EX": [("Register weekly; programme update monthly.", "Auto", "(freshness rule)")]}),
 ("IR-11", "Security of sensitive information", "ICB – Senior Security Risk Owner",
  "As the Senior Security Risk Owner, I need sensitive information about the substation, clinical waste plant, controlled drugs store and building control networks to be marked and shared only with named parties, so that the campus's critical services aren't exposed to attack or misuse.",
  "OIR-SOC-04", "",
  {"G": [("Shared site models show .204, .205 and the .202 store as envelope only.", "Auto", "SEC-04")],
   "NG": [("Every container carries a security marking (SEC-01, SEC-02).", "Auto", "SEC rules"),
          ("No network addresses or credentials in COBie, models or general documents (SEC-08).", "Auto", "(pattern scan rule)")],
   "D": [("Security management plan; information sharing agreements.", "Assisted", "Senior Security Risk Owner")],
   "AC": [("BS EN ISO 19650-5; the security management plan.", "Assisted", "Senior Security Risk Owner")],
   "SI": [("Security triage outcome; NPSA guidance.", "Auto", "appointing party issues before tender")],
   "EX": [("Before any sensitive information is shared outside the appointing party (trigger).", "Auto", "(event rule)"),
          ("Plan reviewed every 6 months.", "Auto", "(frequency rule)")]}),
 ("IR-12", "Substation adoption (third party)", "Distribution Network Operator – Adoptions Engineer",
  "As the DNO's Adoptions Engineer, I need as-built records and test certificates for the substation, so that I can adopt and energise it safely.",
  "OIR-SOC-04", "",
  {"G": [("As-built cable routes and substation layout (restricted under IR-11).", "Manual", "DNO")],
   "NG": [("Equipment schedule: switchgear and transformer ratings and serial numbers.", "Auto", "(data dictionary rows)")],
   "D": [("ENA G81 adoption pack items present.", "Auto", "(document checklist rule)"),
         ("Test certificates acceptable to the DNO.", "Manual", "DNO")],
   "AC": [("ENA G81 and the DNO's own standards.", "Manual", "DNO")],
   "EX": [("4 weeks before M-204-EN (energisation).", "Auto", "(milestone rule)")]}),
 ("IR-13", "Clinical waste plant permit compliance", "ICB Estates – Environmental Compliance Manager",
  "As the Environmental Compliance Manager, I need emissions and throughput records for the clinical waste plant, so that we comply with the environmental permit and can report to the regulator.",
  "OIR-ENV-04", "",
  {"NG": [("Monitoring point register with permit limit per parameter.", "Auto", "(data dictionary rows)")],
   "D": [("Monthly monitoring returns present.", "Auto", "(frequency rule)"),
         ("Return content.", "Manual", "Environmental Compliance Manager")],
   "AC": [("Readings within permit limits (Environmental Permitting Regulations 2016; HTM 07-01).", "Auto", "data platform check")],
   "EX": [("Monthly from commissioning of .205.", "Auto", "(frequency rule)")]}),
 ("IR-14", "Health and safety file", "ICB – Client (CDM 2015)",
  "As the client under CDM 2015, I need the health and safety file, so that future maintenance, alteration and demolition can be done safely.",
  "OIR-SOC-03", "",
  {"G": [("Each residual hazard has a location.", "Auto", "(data rule)")],
   "NG": [("Residual hazard register with required fields.", "Auto", "(data dictionary rows)")],
   "D": [("H&S file with the ICB template sections.", "Assisted", "rule checks sections; client checks content")],
   "AC": [("CDM 2015.", "Manual", "Principal Designer")],
   "EX": [("At M-203-PC.", "Auto", "L2-02")]}),
 ("IR-15", "Post-occupancy evaluation and lessons learned", "ICB – Programme Sponsor (MA 4920)",
  "As the Programme Sponsor, I need year 1 and year 2 performance evaluations and lessons learned, so that later campus buildings and future ICB projects are briefed better.",
  "all OIR outcomes", "KPI-11 to KPI-17; BEN-01 to BEN-06",
  {"NG": [("Measured value of every KPI against target (Section 19).", "Auto", "KPI calculation")],
   "D": [("POE report and lessons learned log.", "Manual", "Programme Sponsor")],
   "AC": [("Each benefit (BEN-xx) reported with baseline, target and measured value.", "Auto", "(benefit register check)")],
   "EX": [("Handover + 12 months and + 24 months.", "Auto", "(milestone rule)")]}),
 ("IR-16", "Connected systems and live data", "ICB Estates – Estates Digital Lead",
  "As the Estates Digital Lead, I need every sensor, meter and control point to arrive named, linked to its asset and streaming into the ICB data platform, so that alarms raise work orders automatically and the energy, water temperature and room use KPIs are measured from the first day of operation.",
  "OIR-ENV-01, OIR-SOC-01, OIR-SOC-02, OIR-SOC-03", "KPI-08, KPI-11, KPI-12, KPI-14, KPI-16",
  {"G": [("Each field device (sensor, meter, controller) is located in a room.", "Auto", "L3-04")],
   "NG": [("A points schedule with one row per point, in the format of INT-02.", "Auto", "(INT-02 rule)"),
          ("Every point links to an asset that exists in COBie, with a matching GUID (INT-03).", "Auto", "(INT-03 rule)"),
          ("Point IDs follow the naming convention (INT-04).", "Auto", "(INT-04 rule)"),
          ("Each point tagged with a Brick schema class (INT-05).", "Assisted", "rule checks the class exists; Digital Lead checks it's right")],
   "D": [("Integration specification: systems, interfaces, protocols, data flows, security (INT-07).", "Assisted", "Digital Lead and IT/OT security"),
         ("Point-to-point test records for 100% of points (INT-11).", "Auto", "(completeness rule)"),
         ("14-day data soak test report (INT-11).", "Auto", "data platform metrics")],
   "AC": [("Open protocols only: BACnet/IP for building controls; Modbus TCP or M-Bus for meters (INT-06).", "Auto", "(points schedule rule)"),
          ("At least 95% of expected readings received during the soak test, with UTC timestamps and values in range (INT-11).", "Auto", "data platform check"),
          ("End-to-end test: a simulated TMV over-temperature alarm creates a CAFM work order within 5 minutes (INT-11).", "Assisted", "witnessed by Digital Lead"),
          ("Operational technology security requirements met (SEC-08, SEC-09).", "Assisted", "IT/OT security")],
   "SI": [("ICB point naming and integration standard (REF-09).", "Auto", "appointing party issues before tender"),
          ("ICB data platform interface specification and test environment (REF-11).", "Auto", "appointing party issues before tender")],
   "EX": [("Integration specification at M-203-S4.", "Auto", "L2-02"),
          ("Draft points schedule at M-203-IE2; final at M-203-PC.", "Auto", "L2-02"),
          ("Soak test report before M-203-PC.", "Auto", "L2-02"),
          ("Monthly data quality report during the 12-month defects period.", "Auto", "(frequency rule)")]}),
]

rows, md = [], []
for ir, title, owner, story, outcomes, kpis, comps in IRS:
    md.append(f"### {ir} {title}\n")
    md.append(f"**Requirement owner:** {owner}  ")
    md.append(f"**Requirement description:** {story}  ")
    md.append(f"**Supports:** {outcomes}" + (f" · {kpis}" if kpis else "") + "\n")
    md.append("| ID | Component | Requirement | Verification | Verified by |")
    md.append("|---|---|---|---|---|")
    for key in ["G", "NG", "D", "AC", "SI", "EX"]:
        items = comps.get(key, [])
        if not items:
            rid = f"{ir}.{key}.00"
            md.append(f"| {rid} | {COMP[key]} | None required. | – | – |")
            rows.append({"req_id": rid, "ir_id": ir, "title": title, "owner": owner, "component": COMP[key],
                         "requirement": "None required.", "verification": "n/a", "verified_by": "", "supports": outcomes, "kpis": kpis})
            continue
        for n, (text, ver, by) in enumerate(items, 1):
            rid = f"{ir}.{key}.{n:02d}"
            md.append(f"| {rid} | {COMP[key]} | {text} | {ver} | {by} |")
            rows.append({"req_id": rid, "ir_id": ir, "title": title, "owner": owner, "component": COMP[key],
                         "requirement": text, "verification": ver, "verified_by": by, "supports": outcomes, "kpis": kpis})
    md.append("")

with open(OUT / "eir_requirements_register.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
(OUT / "_ir_tables.md").write_text("\n".join(md))

real = [r for r in rows if r["verification"] != "n/a"]
core = [r for r in real if r["component"] != "Supporting information"]
c_all, c_core = Counter(r["verification"] for r in real), Counter(r["verification"] for r in core)
by_comp = {}
for r in real:
    by_comp.setdefault(r["component"], Counter())[r["verification"]] += 1
pct = lambda c, n: f"{100 * c / n:.0f}%"
st = ["| Component | Auto | Assisted | Manual | Total |", "|---|---|---|---|---|"]
for comp in COMP.values():
    c = by_comp.get(comp, Counter())
    st.append(f"| {comp} | {c['Auto']} | {c['Assisted']} | {c['Manual']} | {sum(c.values())} |")
n = len(core)
st.append(f"| **All except supporting information** | **{c_core['Auto']} ({pct(c_core['Auto'], n)})** | **{c_core['Assisted']} ({pct(c_core['Assisted'], n)})** | **{c_core['Manual']} ({pct(c_core['Manual'], n)})** | **{n}** |")
existing = sum(1 for r in core if any(t.startswith(("L1-", "L2-", "L3-", "L4-", "SEC-")) for t in r["verified_by"].replace(",", " ").split()))
st.append(f"\n{existing} of the {n} are already covered by a rule in the current checking rules; the rest name a planned rule (in brackets) or a role.")
(OUT / "_ir_stats.md").write_text("\n".join(st))
print("\n".join(st))
print(f"atomic requirements: {len(rows)} ({len(real)} real, {len(rows) - len(real)} 'none required')")
