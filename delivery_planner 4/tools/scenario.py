"""The perfect scenario: Larch Road Health Centre, design and build, offsite modular.

Defines the programme (WBS, activities, logic) and the MIDP in one place, because every MIDP row
links to an 'issue' activity in the programme. build_scenario.py turns this into the data files.
"""
from datetime import date
from scheduler import Calendar

START = date(2026, 11, 25)          # contract award; reference library issued
DATA_DATE = date(2027, 5, 1)        # status date for the update

BANK_HOLIDAYS = [date(2026, 12, 25), date(2026, 12, 28), date(2027, 1, 1), date(2027, 3, 26),
                 date(2027, 3, 29), date(2027, 5, 3), date(2027, 5, 31), date(2027, 8, 30)]
SHUTDOWN = [date(2026, 12, 24), date(2026, 12, 29), date(2026, 12, 30), date(2026, 12, 31)]
CALS = {
    "5D": Calendar(1, "LRHC 5-day (England, Christmas shutdown)", range(5), BANK_HOLIDAYS + SHUTDOWN),
    "7D": Calendar(2, "LRHC 7-day (continuous tests)", range(7)),
}

# WBS: code -> (name, parent). Level 1 under the project is the RIBA stage (or KEY).
WBS = {
    "LRHC": ("Larch Road Health Centre: design and build (offsite modular)", None),
    "KEY": ("Key dates and milestones", "LRHC"),
    "4": ("RIBA Stage 4 Technical Design", "LRHC"),
    "4.GEN": ("Design management", "4"),
    "4.ARC": ("Architecture (FLD)", "4"),
    "4.STR": ("Structure and civils (CKE)", "4"),
    "4.MEP": ("Building services (KBS)", "4"),
    "4.MOD": ("Module design (HXM)", "4"),
    "4.COO": ("Coordination and information management (BMC)", "4"),
    "4.APP": ("Statutory approvals", "4"),
    "5": ("RIBA Stage 5 Manufacturing and Construction", "LRHC"),
    "5.PRC": ("Procurement", "5"),
    "5.FAB": ("Factory production (HXM)", "5"),
    "5.ENB": ("Enabling works", "5"),
    "5.SUB": ("Substructure and below-ground drainage", "5"),
    "5.MOD": ("Module delivery and installation", "5"),
    "5.ENV": ("Roof and envelope completion", "5"),
    "5.INT": ("Internal completion by zone", "5"),
    "5.MEP": ("Building services installation", "5"),
    "5.EXT": ("External works", "5"),
    "5.COM": ("Testing and commissioning", "5"),
    "5.INF": ("Construction information", "5"),
    "6": ("RIBA Stage 6 Handover", "LRHC"),
    "6.INF": ("Handover information (IE3)", "6"),
    "6.HND": ("Handover and practical completion", "6"),
    "6.REC": ("Record information (IE4)", "6"),
}

ACTS = []
ISSUE = {}      # deliverable key -> code of its issue activity


def T(code, name, wbs, dur, preds=(), cal="5D", cstr=None):
    ACTS.append(dict(code=code, name=name, wbs=wbs, dur=dur, cal=cal, type="TT_Task",
                     preds=[p if isinstance(p, tuple) else (p, "FS", 0) for p in preds], cstr=cstr))
    return code


def MS(code, name, wbs, preds=(), cstr=None, start=False):
    ACTS.append(dict(code=code, name=name, wbs=wbs, dur=0, cal="5D", type="TT_Mile" if start else "TT_FinMile",
                     preds=[p if isinstance(p, tuple) else (p, "FS", 0) for p in preds], cstr=cstr))
    return code


def deliverable(key, prefix, title, wbs, dev, after, check=2, review=None):
    """Develop -> check -> (review) -> issue. Returns the issue activity code."""
    d = T(f"{prefix}0", f"Develop {title}", wbs, dev, after)
    c = T(f"{prefix}1", f"Check and approve {title}", wbs, check, [d])
    last = c
    if review:
        last = T(f"{prefix}2", f"{review} {title}", wbs, 1, [c])
    i = T(f"{prefix}5", f"Issue {title}", wbs, 1, [last])
    ISSUE[key] = i
    return i


# ---------------------------------------------------------------- key dates
MS("M-203-AW", "Contract award and start on site possession date", "KEY", cstr=("SNET", START), start=True)

# ---------------------------------------------------------------- Stage 4
k = T("4-GEN-1010", "Design kick-off and Stage 3 design review", "4.GEN", 3, ["M-203-AW"])
T("4-GEN-1020", "Confirm BEP and design responsibility matrix", "4.GEN", 5, ["M-203-AW"])
T("4-GEN-1030", "Site investigation and survey review", "4.GEN", 3, ["M-203-AW"])

# Architecture (FLD)
am = deliverable("ARC_MODEL", "4-ARC-101", "architectural model (Stage 4)", "4.ARC", 13, [k])
for n, (z, zname) in enumerate([("Z1", "public zone"), ("Z2", "clinical zone"), ("Z3", "staff and support zone"),
                                 ("Z4", "plant zone")]):
    deliverable(f"GA_{z}", f"4-ARC-1{n+1}0", f"GA plan, {zname}", "4.ARC", 11, [("4-ARC-1010", "SS", 4 + n)],
                review="Client review of")
deliverable("ROOF", "4-ARC-160", "roof plan", "4.ARC", 9, [("4-ARC-1010", "SS", 6)])
deliverable("ELEV", "4-ARC-170", "elevations", "4.ARC", 9, [("4-ARC-1010", "SS", 7)])
deliverable("SECT", "4-ARC-180", "sections", "4.ARC", 9, [("4-ARC-1010", "SS", 8)])
deliverable("RDS_Z2", "4-ARC-190", "room data sheets, clinical zone", "4.ARC", 10, [("4-ARC-1200", "SS", 3)])
deliverable("DOORS", "4-ARC-200", "door schedule", "4.ARC", 9, [("4-ARC-1010", "SS", 8)])
deliverable("ARC_SPEC", "4-ARC-210", "architectural specification", "4.ARC", 16, [("4-GEN-1010", "SS", 4)])
deliverable("FIRE", "4-ARC-220", "fire strategy report", "4.ARC", 11, [("4-ARC-1010", "SS", 3)])
deliverable("EXT_LAYOUT", "4-ARC-230", "external works and landscape layout", "4.ARC", 14, [("4-GEN-1030", "FS", 0)])

# Structure and civils (CKE)
deliverable("STR_MODEL", "4-STR-101", "structural model (foundations and module interfaces)", "4.STR", 11,
            [("4-ARC-1010", "SS", 3), "4-GEN-1030"])
deliverable("FDN", "4-STR-110", "foundation layout", "4.STR", 9, [("4-STR-1010", "SS", 3)])
deliverable("STR_CALC", "4-STR-120", "structural calculations", "4.STR", 12, [("4-STR-1010", "SS", 2)])
deliverable("DRAIN", "4-STR-130", "below-ground drainage layout", "4.STR", 12, ["4-GEN-1030"])
deliverable("DRAIN_CALC", "4-STR-140", "drainage and SuDS calculations", "4.STR", 10, [("4-STR-1300", "SS", 2)])

# Building services (KBS)
T("4-MEP-1000", "Heating, cooling and ventilation load calculations", "4.MEP", 5, [k])
T("4-MEP-1001", "Plant selection (AHU, air source heat pumps, LV switchgear)", "4.MEP", 5, ["4-MEP-1000"])
deliverable("MECH_MODEL", "4-MEP-101", "mechanical model", "4.MEP", 13, ["4-MEP-1000", ("4-ARC-1010", "SS", 3)])
deliverable("ELEC_MODEL", "4-MEP-102", "electrical model", "4.MEP", 13, ["4-MEP-1000", ("4-ARC-1010", "SS", 3)])
deliverable("PH_MODEL", "4-MEP-103", "public health model", "4.MEP", 13, ["4-MEP-1000", ("4-ARC-1010", "SS", 3)])
deliverable("VENT_SCH", "4-MEP-110", "ventilation schematic", "4.MEP", 7, ["4-MEP-1001"])
deliverable("ELEC_SCH", "4-MEP-120", "electrical distribution schematic", "4.MEP", 7, ["4-MEP-1001"])
deliverable("HCW_SCH", "4-MEP-130", "hot and cold water schematic (TMVs)", "4.MEP", 7, ["4-MEP-1001"])
deliverable("INT_SPEC", "4-MEP-140", "integration specification (connected systems)", "4.MEP", 12,
            ["4-MEP-1001"], review="IT/OT security review of")
deliverable("BS_SPEC", "4-MEP-150", "building services specification", "4.MEP", 15, [("4-MEP-1000", "SS", 2)])

# Module design (HXM)
T("4-MOD-1000", "Module grid, transport envelope and interface design", "4.MOD", 5, [("4-ARC-1010", "SS", 2)])
deliverable("MOD_MODEL", "4-MOD-101", "module fabrication model", "4.MOD", 7, ["4-MOD-1000"])
deliverable("MOD_LAYOUT", "4-MOD-110", "module layout and setting-out drawing", "4.MOD", 6, ["4-MOD-1000"])
deliverable("MOD_SCHED", "4-MOD-120", "module schedule", "4.MOD", 5, ["4-MOD-1000"])
MS("4-MOD-1900", "Module design freeze", "4.MOD", ["4-MOD-1015", "4-MOD-1105", "4-MOD-1205", "4-STR-1105"])

# Coordination and information management (BMC)
deliverable("PROG", "4-COO-100", "first contract programme", "4.COO", 10, ["M-203-AW"], check=1)
deliverable("CPP", "4-COO-110", "construction phase plan", "4.COO", 15, ["M-203-AW"])
prev = "4-ARC-1010"
for r, lag in [(1, 7), (2, 12), (3, 17)]:
    f = T(f"4-COO-2{r}00", f"Federate models, clash round {r}", "4.COO", 1, [("4-ARC-1010", "SS", lag)])
    c = T(f"4-COO-2{r}10", f"Run clash detection, round {r}", "4.COO", 1, [f])
    w = T(f"4-COO-2{r}20", f"Coordination workshop, round {r}", "4.COO", 1, [c])
    T(f"4-COO-2{r}30", f"Resolve clashes, round {r}", "4.COO", 3 if r < 3 else 2, [w])
fed_after = ["4-COO-2330", "4-ARC-1015", "4-STR-1015", "4-MEP-1015", "4-MEP-1025", "4-MEP-1035"]
deliverable("FED_S4", "4-COO-300", "federated model (Stage 4)", "4.COO", 1, fed_after, check=1)
deliverable("CLASH_RPT", "4-COO-310", "clash detection report (Stage 4)", "4.COO", 1, ["4-COO-2330"], check=1)

# Statutory approvals
T("4-APP-1000", "Building control full plans submission", "4.APP", 1, ["4-ARC-1015", "4-ARC-2205", "4-STR-1205"])
T("4-APP-1010", "Building control plan check", "4.APP", 20, ["4-APP-1000"])
MS("4-APP-1020", "Building control full plans approval", "4.APP", ["4-APP-1010"])
for n, cond in enumerate(["materials and external appearance", "drainage and SuDS", "landscaping"]):
    s = T(f"4-APP-11{n}0", f"Submit planning condition discharge: {cond}", "4.APP", 1,
          ["4-ARC-1705" if n == 0 else "4-STR-1405" if n == 1 else "4-ARC-2305"])
    T(f"4-APP-11{n}5", f"Planning authority determination: {cond}", "4.APP", 25, [s])
T("4-APP-1200", "Client Stage 4 sign-off", "4.APP", 3, ["M-203-S4"])

S4_ISSUES = [ISSUE[k] for k in ISSUE]
MS("M-203-S4", "M-203-S4 Stage 4 technical design complete (IE1)", "KEY", S4_ISSUES, cstr=("FON", date(2027, 1, 15)))

# ---------------------------------------------------------------- Stage 5: procurement
PKGS = [("AHU", "Air handling unit", 40, "VENT_SCH"), ("ASHP", "Air source heat pumps", 35, "VENT_SCH"),
        ("LV", "LV switchgear and distribution boards", 30, "ELEC_SCH"), ("BMS", "BMS controls and integration gateway", 20, "INT_SPEC"),
        ("FA", "Fire detection and alarm", 20, "BS_SPEC"), ("NC", "Nurse call and assistance call", 20, "BS_SPEC"),
        ("EL", "Emergency lighting", 15, "BS_SPEC"), ("LUM", "Luminaires", 15, "BS_SPEC"),
        ("TMV", "TMVs and sanitaryware", 15, "HCW_SCH"), ("ROOF", "Roof membrane", 10, "ARC_SPEC"),
        ("CLAD", "Cladding junction kits", 15, "ARC_SPEC"), ("DOOR", "External doors and entrance canopy", 20, "ARC_SPEC"),
        ("EXTL", "External lighting", 15, "EXT_LAYOUT")]
DELIVERED = {}
for n, (c, name, lead, dep) in enumerate(PKGS):
    base = f"5-PRC-{1000 + n*10}"
    t = T(base, f"Tender and award: {name}", "5.PRC", 10, [ISSUE[dep]])
    s = T(f"{base[:-1]}1", f"Submittals and approval: {name}", "5.PRC", 5, [t])
    m = T(f"{base[:-1]}2", f"Manufacture: {name}", "5.PRC", lead, [s])
    DELIVERED[c] = T(f"{base[:-1]}3", f"Deliver: {name}", "5.PRC", 1, [m])

# ---------------------------------------------------------------- Stage 5: factory
T("5-FAB-1000", "Factory production slot and jig set-up", "5.FAB", 5, ["4-MOD-1900"])
T("5-FAB-1001", "Factory first-fix materials delivered", "5.FAB", 3, ["4-MOD-1900", "4-MEP-1505"])
MODULES = [("M01", "Z1"), ("M02", "Z1"), ("M03", "Z1"), ("M04", "Z2"), ("M05", "Z2"), ("M06", "Z2"),
           ("M07", "Z2"), ("M08", "Z2"), ("M09", "Z2"), ("M10", "Z3"), ("M11", "Z3"), ("M12", "Z4")]
STEPS = [("Chassis and floor cassette", 4), ("Walls, roof and windows", 4), ("First-fix M&E and linings", 5),
         ("Factory QA inspection and ready to dispatch", 2)]
prev_mod = None
for i, (m, z) in enumerate(MODULES):
    for j, (step, dur) in enumerate(STEPS):
        code = f"5-FAB-{m}{j}"
        preds = ["5-FAB-1000"] if j == 0 else [f"5-FAB-{m}{j-1}"]
        if j == 2:
            preds.append("5-FAB-1001")
        if prev_mod:
            preds.append((f"5-FAB-{prev_mod}{j}", "SS", 2))
        T(code, f"Module {m} ({z}): {step}", "5.FAB", dur, preds)
    prev_mod = m

# ---------------------------------------------------------------- Stage 5: site
T("5-ENB-1000", "Site set-up and welfare", "5.ENB", 5, ["4-COO-1105"], cstr=("SNET", date(2027, 1, 4)))
T("5-ENB-1010", "Hoarding and site security", "5.ENB", 3, [("5-ENB-1000", "SS", 1)])
T("5-ENB-1020", "Temporary services", "5.ENB", 4, [("5-ENB-1000", "SS", 2)])
T("5-ENB-1030", "Setting out from survey control SP-01", "5.ENB", 2, ["5-ENB-1000"])
T("5-ENB-1040", "Utilities diversions within the plot", "5.ENB", 8, ["5-ENB-1030"])
T("5-ENB-1050", "Haul road and crane hardstanding", "5.ENB", 4, ["5-ENB-1030"])

prev = None
for n, z in enumerate(["Z1", "Z2", "Z3", "Z4"]):
    e = T(f"5-SUB-1{n}00", f"Excavate foundations, {z}", "5.SUB", 5,
          ["5-ENB-1030", "4-STR-1105"] + ([(prev, "SS", 3)] if prev else []))
    f = T(f"5-SUB-1{n}10", f"Pad foundations and ground beams, {z}", "5.SUB", 10, [e])
    T(f"5-SUB-1{n}20", f"Backfill and module bearing check, {z}", "5.SUB", 2, [f])
    prev = e
T("5-SUB-1500", "Plant base and roof plant support steelwork", "5.SUB", 4, ["5-SUB-1310"])
T("5-SUB-1600", "Below-ground drainage", "5.SUB", 20, ["5-ENB-1040", "4-STR-1305"])
T("5-SUB-1610", "Service ducts and building entry points", "5.SUB", 5, [("5-SUB-1600", "SS", 4)])
T("5-SUB-1620", "Drainage CCTV survey", "5.SUB", 2, ["5-SUB-1600"])

T("5-MOD-1000", "Crane mobilisation and lift plan", "5.MOD", 2,
  ["5-ENB-1050", "5-SUB-1020", "5-SUB-1120", "5-SUB-1220", "5-SUB-1320", "4-APP-1020"],
  cstr=("SNET", date(2027, 3, 4)))   # delivery window agreed with the factory
prev = "5-MOD-1000"
for m, z in MODULES:
    d = T(f"5-MOD-{m}0", f"Deliver and set module {m} ({z})", "5.MOD", 1, [prev, f"5-FAB-{m}3"])
    T(f"5-MOD-{m}1", f"Structural connections and seal joints, module {m}", "5.MOD", 1, [d])
    prev = d
T("5-MOD-1900", "Crane demobilisation", "5.MOD", 1, ["5-MOD-M121"])
MS("5-MOD-1910", "Modules weathertight", "5.MOD", ["5-MOD-M121"])

for n, z in enumerate(["Z1", "Z2", "Z3", "Z4"]):
    last_mod = {"Z1": "M03", "Z2": "M09", "Z3": "M11", "Z4": "M12"}[z]
    T(f"5-ENV-1{n}00", f"Roof membrane over modules, {z}", "5.ENV", 4, [f"5-MOD-{last_mod}1", DELIVERED["ROOF"]])
    T(f"5-ENV-1{n}10", f"Cladding junctions and module joint covers, {z}", "5.ENV", 4,
      [f"5-MOD-{last_mod}1", DELIVERED["CLAD"]])
T("5-ENV-1500", "Roof plant platform and guarding", "5.ENV", 3, ["5-ENV-1300", "5-SUB-1500"])
T("5-ENV-1510", "Rainwater goods", "5.ENV", 3, ["5-ENV-1300"])
T("5-ENV-1520", "External doors and entrance canopy", "5.ENV", 4, ["5-ENV-1010", DELIVERED["DOOR"]])

T("5-MEP-1000", "Incoming LV supply connection from campus network", "5.MEP", 3, ["M-204-EN", "5-SUB-1610"])
T("5-MEP-1010", "LV switchgear and distribution boards", "5.MEP", 5, [DELIVERED["LV"], "5-MOD-M121"])
T("5-MEP-1020", "Plant room fit-out", "5.MEP", 15, ["5-MOD-M121"])
T("5-MEP-1030", "AHU installation", "5.MEP", 3, [DELIVERED["AHU"], "5-ENV-1500"])
T("5-MEP-1040", "Air source heat pump installation", "5.MEP", 3, [DELIVERED["ASHP"], "5-ENV-1500"])
T("5-MEP-1050", "Ductwork connections between modules", "5.MEP", 12, ["5-MOD-M121", ("5-MEP-1030", "SS", 1)])
T("5-MEP-1060", "Pipework connections between modules", "5.MEP", 12, ["5-MOD-M121", "5-SUB-1610"])
T("5-MEP-1070", "Water supply connection and meter", "5.MEP", 2, ["5-SUB-1610"])
T("5-MEP-1080", "BMS installation and integration gateway", "5.MEP", 15, [DELIVERED["BMS"], ("5-MEP-1020", "SS", 3)])
T("5-MEP-1090", "Fire detection and alarm installation", "5.MEP", 8, [DELIVERED["FA"], "5-MOD-M121"])
T("5-MEP-1100", "Nurse call and assistance call installation", "5.MEP", 5, [DELIVERED["NC"], "5-MOD-M121"])
T("5-MEP-1110", "Emergency lighting installation", "5.MEP", 5, [DELIVERED["EL"], "5-MOD-M121"])
T("5-MEP-1120", "Luminaire installation", "5.MEP", 4, [DELIVERED["LUM"], "5-MOD-M121"])
T("5-MEP-1130", "External lighting installation", "5.MEP", 3, [DELIVERED["EXTL"], "5-EXT-1010"])
MS("M-204-EN", "M-204-EN Campus 11 kV energisation (by others, MA 4920.204)", "KEY",
   cstr=("SNET", date(2027, 4, 6)), start=True)

for n, z in enumerate(["Z1", "Z2", "Z3", "Z4", "ZZ"]):
    zn = "corridor" if z == "ZZ" else z
    j = T(f"5-INT-1{n}00", f"Make good module joints, {zn}", "5.INT", 6, ["5-MOD-M121"])
    s = T(f"5-INT-1{n}10", f"Second-fix M&E connections, {zn}", "5.INT", 10, [j, ("5-MEP-1060", "SS", 3)])
    f = T(f"5-INT-1{n}20", f"Finishes at joints and floor coverings, {zn}", "5.INT", 8, [s])
    last = f
    if z in ("Z1", "Z2"):
        last = T(f"5-INT-1{n}30", f"Install sanitaryware and TMVs, {zn}", "5.INT", 3, [f, DELIVERED["TMV"]])
    T(f"5-INT-1{n}40", f"Builder's clean, {zn}", "5.INT", 2, [last])

T("5-EXT-1000", "Drainage connections to campus network", "5.EXT", 5, ["5-SUB-1620"])
T("5-EXT-1010", "Car park and path sub-base", "5.EXT", 8, ["5-SUB-1600", "5-MOD-1900"])
T("5-EXT-1020", "Car park surfacing", "5.EXT", 5, ["5-EXT-1010"])
T("5-EXT-1030", "Paths and paving", "5.EXT", 6, [("5-EXT-1020", "SS", 2)])
T("5-EXT-1040", "Soft landscaping", "5.EXT", 8, ["5-EXT-1030"])
T("5-EXT-1050", "Fencing and gates", "5.EXT", 5, ["5-EXT-1010"])
T("5-EXT-1060", "Line marking and signage", "5.EXT", 1, ["5-EXT-1020"])

# Testing and commissioning
T("5-COM-1000", "LV electrical testing and certification", "5.COM", 4, ["5-MEP-1000", "5-MEP-1010", "5-INT-1410"])
T("5-COM-1010", "Emergency lighting test (3-hour duration)", "5.COM", 2, ["5-COM-1000", "5-MEP-1110"])
T("5-COM-1020", "Fire alarm commissioning", "5.COM", 4, ["5-COM-1000", "5-MEP-1090"])
T("5-COM-1021", "Fire alarm cause and effect witness test", "5.COM", 1, ["5-COM-1020"])
T("5-COM-1030", "Nurse call and assistance call commissioning", "5.COM", 3, ["5-COM-1000", "5-MEP-1100"])
T("5-COM-1040", "Ventilation commissioning and air balancing", "5.COM", 5, ["5-COM-1000", "5-MEP-1050", "5-MEP-1030"])
T("5-COM-1050", "Heat pump and heating commissioning", "5.COM", 4, ["5-COM-1000", "5-MEP-1040", "5-MEP-1060"])
T("5-COM-1060", "Water system flush and chlorination", "5.COM", 3, ["5-MEP-1070", "5-INT-1130"])
T("5-COM-1061", "Water sampling and laboratory results", "5.COM", 10, ["5-COM-1060"])
T("5-COM-1070", "TMV commissioning and temperature tests", "5.COM", 3, ["5-COM-1060", "5-COM-1050"])
T("5-COM-1080", "Fire damper drop tests", "5.COM", 2, ["5-MEP-1050", "5-COM-1020"])
T("5-COM-1090", "BMS commissioning", "5.COM", 8, ["5-MEP-1080", "5-COM-1040", "5-COM-1050"])
T("5-COM-1100", "Point-to-point test of all BMS and metering points", "5.COM", 5, [("5-COM-1090", "SS", 3)])
T("5-COM-1110", "End-to-end alarm test (TMV over-temperature to CAFM work order)", "5.COM", 1, ["5-COM-1100", "5-COM-1070"])
T("5-COM-1120", "14-day data soak test", "5.COM", 14, ["5-COM-1100"], cal="7D")
T("5-COM-1130", "Air tightness test", "5.COM", 1, ["5-ENV-1520", "5-INT-1040", "5-INT-1140"])
T("5-COM-1140", "Acoustic testing (consulting rooms)", "5.COM", 2, ["5-INT-1140"])
T("5-COM-1150", "Building control completion inspection", "5.COM", 1, ["5-COM-1021", "5-COM-1010", "5-COM-1130"])

# Construction information (Stage 5)
deliverable("FACT_REC", "5-INF-100", "factory inspection and test records", "5.INF", 3, ["5-FAB-M123"])
deliverable("COMM_PLAN", "5-INF-110", "commissioning plan", "5.INF", 8, ["5-MOD-1910"])
deliverable("POINTS_DRAFT", "5-INF-120", "points schedule (draft)", "5.INF", 6, [("5-MEP-1080", "SS", 2), "4-MEP-1405"])
deliverable("COBIE_DRAFT", "5-INF-130", "COBie (draft)", "5.INF", 9, [("5-INT-1100", "SS", 1)])
IE2_ISSUES = [ISSUE[k] for k in ("FACT_REC", "COMM_PLAN", "POINTS_DRAFT", "COBIE_DRAFT")]
MS("M-203-IE2", "M-203-IE2 Pre-handover information (IE2)", "KEY", IE2_ISSUES, cstr=("FON", date(2027, 4, 16)))

# ---------------------------------------------------------------- Stage 6
deliverable("POINTS_FINAL", "6-INF-100", "points schedule (final)", "6.INF", 3, ["5-COM-1100", "5-INF-1205"])
deliverable("SOAK_RPT", "6-INF-110", "data soak test report", "6.INF", 2, ["5-COM-1120"], check=1)
deliverable("NET_SCHED", "6-INF-120", "network and device schedule", "6.INF", 3, ["5-COM-1090"])
deliverable("TMV_RPT", "6-INF-130", "TMV commissioning report", "6.INF", 2, ["5-COM-1070", "5-COM-1061"])
deliverable("FDM_RPT", "6-INF-140", "fire damper drop-test report", "6.INF", 2, ["5-COM-1080"])
deliverable("ELEC_CERT", "6-INF-150", "electrical and emergency lighting test certificates", "6.INF", 2,
            ["5-COM-1000", "5-COM-1010"])
deliverable("COBIE_IE3", "6-INF-160", "COBie (handover)", "6.INF", 10, ["5-INF-1305", ("5-COM-1090", "SS", 0)])
deliverable("ASBUILT_IE3", "6-INF-170", "as-constructed federated model", "6.INF", 15, ["5-MOD-1910", ("5-COM-1000", "SS", 0)])
deliverable("OM_IE3", "6-INF-180", "O&M manual", "6.INF", 20, [("5-COM-1000", "SS", 0)], check=3)
deliverable("HS_FILE", "6-INF-190", "health and safety file", "6.INF", 18, [("5-COM-1000", "SS", 0)])

T("6-HND-1000", "Client and FM training", "6.HND", 5, ["5-COM-1090", "5-COM-1030"])
T("6-HND-1010", "Pre-completion snagging inspection", "6.HND", 3, ["5-INT-1040", "5-INT-1140", "5-INT-1240"])
T("6-HND-1020", "Snag rectification", "6.HND", 5, ["6-HND-1010"])
T("6-HND-1030", "Building control completion certificate", "6.HND", 3, ["5-COM-1150"])
T("6-HND-1040", "Practical completion inspection", "6.HND", 1,
  ["6-HND-1020", "6-HND-1030", "5-COM-1110", "5-EXT-1040", "5-EXT-1060", "5-COM-1140", "5-COM-1021"])
IE3_ISSUES = [ISSUE[k] for k in ("POINTS_FINAL", "SOAK_RPT", "NET_SCHED", "TMV_RPT", "FDM_RPT", "ELEC_CERT",
                                 "COBIE_IE3", "ASBUILT_IE3", "OM_IE3", "HS_FILE")]
MS("M-203-PC", "M-203-PC Practical completion and handover information (IE3)", "KEY",
   IE3_ISSUES + ["6-HND-1040", "6-HND-1000"], cstr=("FON", date(2027, 6, 4)))
T("6-HND-1050", "Handover of keys, access cards and BMS credentials (to IT/OT security)", "6.HND", 1, ["M-203-PC"])

deliverable("COBIE_REC", "6-REC-100", "COBie (record)", "6.REC", 8, ["M-203-PC"])
deliverable("ASBUILT_REC", "6-REC-110", "as-constructed federated model (record)", "6.REC", 10, ["M-203-PC"])
deliverable("OM_REC", "6-REC-120", "O&M manual (record)", "6.REC", 8, ["M-203-PC"])
MS("M-203-REC", "M-203-REC Record information (IE4)", "KEY",
   [ISSUE[k] for k in ("COBIE_REC", "ASBUILT_REC", "OM_REC")], cstr=("FON", date(2027, 7, 2)))


# ---------------------------------------------------------------- MIDP (lead appointed party)
# key, originator, volume, level, type, role, number, title, stage, required suitability, exchange
MIDP = [
    ("ARC_MODEL", "FLD", "ZZ", "00", "M3", "A", "000001", "Architectural model", 4, "S4", "IE1"),
    ("DOORS", "FLD", "ZZ", "ZZ", "SH", "A", "000001", "Door schedule", 4, "S4", "IE1"),
    ("GA_Z1", "FLD", "Z1", "00", "DR", "A", "000101", "GA plan, public zone", 4, "S4", "IE1"),
    ("GA_Z2", "FLD", "Z2", "00", "DR", "A", "000102", "GA plan, clinical zone", 4, "S4", "IE1"),
    ("GA_Z3", "FLD", "Z3", "00", "DR", "A", "000103", "GA plan, staff and support zone", 4, "S4", "IE1"),
    ("GA_Z4", "FLD", "Z4", "00", "DR", "A", "000104", "GA plan, plant zone", 4, "S4", "IE1"),
    ("ROOF", "FLD", "ZZ", "RF", "DR", "A", "000105", "Roof plan", 4, "S4", "IE1"),
    ("ELEV", "FLD", "ZZ", "ZZ", "DR", "A", "000201", "Elevations", 4, "S4", "IE1"),
    ("SECT", "FLD", "ZZ", "ZZ", "DR", "A", "000202", "Sections", 4, "S4", "IE1"),
    ("RDS_Z2", "FLD", "Z2", "00", "RD", "A", "000001", "Room data sheets, clinical zone", 4, "S4", "IE1"),
    ("ARC_SPEC", "FLD", "ZZ", "ZZ", "SP", "A", "000001", "Architectural specification", 4, "S4", "IE1"),
    ("FIRE", "FLD", "ZZ", "ZZ", "RP", "A", "000001", "Fire strategy report", 4, "S4", "IE1"),
    ("EXT_LAYOUT", "FLD", "EW", "00", "DR", "A", "000301", "External works and landscape layout", 4, "S4", "IE1"),
    ("STR_MODEL", "CKE", "ZZ", "00", "M3", "S", "000001", "Structural model (foundations and module interfaces)", 4, "S4", "IE1"),
    ("FDN", "CKE", "ZZ", "00", "DR", "S", "000001", "Foundation layout", 4, "S4", "IE1"),
    ("STR_CALC", "CKE", "ZZ", "ZZ", "CA", "S", "000001", "Structural calculations", 4, "S4", "IE1"),
    ("DRAIN", "CKE", "EW", "00", "DR", "C", "000001", "Below-ground drainage layout", 4, "S4", "IE1"),
    ("DRAIN_CALC", "CKE", "EW", "ZZ", "CA", "C", "000001", "Drainage and SuDS calculations", 4, "S4", "IE1"),
    ("MECH_MODEL", "KBS", "ZZ", "00", "M3", "M", "000001", "Mechanical model", 4, "S4", "IE1"),
    ("ELEC_MODEL", "KBS", "ZZ", "00", "M3", "E", "000001", "Electrical model", 4, "S4", "IE1"),
    ("PH_MODEL", "KBS", "ZZ", "00", "M3", "P", "000001", "Public health model", 4, "S4", "IE1"),
    ("VENT_SCH", "KBS", "ZZ", "ZZ", "DR", "M", "000001", "Ventilation schematic", 4, "S4", "IE1"),
    ("ELEC_SCH", "KBS", "ZZ", "ZZ", "DR", "E", "000001", "Electrical distribution schematic", 4, "S4", "IE1"),
    ("HCW_SCH", "KBS", "ZZ", "ZZ", "DR", "P", "000001", "Hot and cold water schematic (TMVs)", 4, "S4", "IE1"),
    ("INT_SPEC", "KBS", "ZZ", "ZZ", "SP", "M", "000001", "Integration specification (connected systems)", 4, "S4", "IE1"),
    ("BS_SPEC", "KBS", "ZZ", "ZZ", "SP", "M", "000002", "Building services specification", 4, "S4", "IE1"),
    ("MOD_MODEL", "HXM", "ZZ", "00", "M3", "X", "000001", "Module fabrication model", 4, "S4", "IE1"),
    ("MOD_LAYOUT", "HXM", "ZZ", "00", "DR", "X", "000001", "Module layout and setting-out drawing", 4, "S4", "IE1"),
    ("MOD_SCHED", "HXM", "ZZ", "ZZ", "SH", "X", "000001", "Module schedule", 4, "S4", "IE1"),
    ("FED_S4", "BMC", "ZZ", "ZZ", "CM", "W", "000001", "Federated model (Stage 4)", 4, "S4", "IE1"),
    ("CLASH_RPT", "BMC", "ZZ", "ZZ", "RP", "W", "000002", "Clash detection report (Stage 4)", 4, "S4", "IE1"),
    ("PROG", "BMC", "ZZ", "ZZ", "PR", "W", "000001", "Contract programme", 4, "S4", "IE1"),
    ("CPP", "BMC", "ZZ", "ZZ", "HS", "W", "000001", "Construction phase plan", 4, "S4", "IE1"),
    ("FACT_REC", "HXM", "ZZ", "ZZ", "RP", "X", "000001", "Factory inspection and test records", 5, "S4", "IE2"),
    ("COMM_PLAN", "BMC", "ZZ", "ZZ", "RP", "W", "000003", "Commissioning plan", 5, "S4", "IE2"),
    ("POINTS_DRAFT", "KBS", "ZZ", "ZZ", "SH", "M", "000001", "Points schedule", 5, "S3", "IE2"),
    ("COBIE_DRAFT", "BMC", "ZZ", "ZZ", "IE", "W", "000001", "COBie", 5, "S3", "IE2"),
    ("POINTS_FINAL", "KBS", "ZZ", "ZZ", "SH", "M", "000001", "Points schedule", 6, "S4", "IE3"),
    ("SOAK_RPT", "KBS", "ZZ", "ZZ", "RP", "M", "000002", "Data soak test report", 6, "S4", "IE3"),
    ("NET_SCHED", "KBS", "ZZ", "ZZ", "SH", "E", "000001", "Network and device schedule (OFFICIAL-SENSITIVE)", 6, "S4", "IE3"),
    ("TMV_RPT", "KBS", "ZZ", "ZZ", "RP", "P", "000001", "TMV commissioning report", 6, "S4", "IE3"),
    ("FDM_RPT", "KBS", "ZZ", "ZZ", "RP", "M", "000001", "Fire damper drop-test report", 6, "S4", "IE3"),
    ("ELEC_CERT", "KBS", "ZZ", "ZZ", "RP", "E", "000001", "Electrical and emergency lighting test certificates", 6, "S4", "IE3"),
    ("COBIE_IE3", "BMC", "ZZ", "ZZ", "IE", "W", "000001", "COBie", 6, "S4", "IE3"),
    ("ASBUILT_IE3", "BMC", "ZZ", "00", "M3", "W", "000001", "As-constructed federated model", 6, "S4", "IE3"),
    ("OM_IE3", "BMC", "ZZ", "ZZ", "RP", "W", "000001", "O&M manual", 6, "S4", "IE3"),
    ("HS_FILE", "BMC", "ZZ", "ZZ", "HS", "W", "000002", "Health and safety file", 6, "S4", "IE3"),
    ("COBIE_REC", "BMC", "ZZ", "ZZ", "IE", "W", "000001", "COBie", 6, "CR", "IE4"),
    ("ASBUILT_REC", "BMC", "ZZ", "00", "M3", "W", "000001", "As-constructed federated model", 6, "CR", "IE4"),
    ("OM_REC", "BMC", "ZZ", "ZZ", "RP", "W", "000001", "O&M manual", 6, "CR", "IE4"),
]


# ---------------------------------------------------------------- close open ends (every activity has a successor)
BY_CODE = {a["code"]: a for a in ACTS}


def link(succ, pred, rel="FS", lag=0):
    BY_CODE[succ]["preds"].append((pred, rel, lag))


link("4-COO-2100", "4-GEN-1020")
link("4-COO-2200", "4-COO-2130")
link("4-COO-2300", "4-COO-2230")
for c in ("4-APP-1105", "4-APP-1115", "4-APP-1125", "4-APP-1200"):
    link("5-MOD-1000", c)
for c in ("5-ENB-1010", "5-ENB-1020"):
    link("5-SUB-1000", c)
ZONE_N = {"Z1": 0, "Z2": 1, "Z3": 2, "Z4": 3}
for m, z in MODULES:
    link(f"5-ENV-1{ZONE_N[z]}00", f"5-MOD-{m}1")
for z, n in ZONE_N.items():
    link(f"5-INT-1{n}00", f"5-ENV-1{n}00")
    link("5-COM-1130", f"5-ENV-1{n}10")
link("6-HND-1010", "5-ENV-1510")
link("5-COM-1000", "5-MEP-1120")
link("6-HND-1040", "5-MEP-1130")
link("6-HND-1010", "5-INT-1340")
link("6-HND-1010", "5-INT-1440")
link("6-HND-1040", "5-EXT-1000")
link("6-HND-1040", "5-EXT-1050")
link("6-INF-1600", "M-203-IE2")
link("M-203-REC", "6-HND-1050")
