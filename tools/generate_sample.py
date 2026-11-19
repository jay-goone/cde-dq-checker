#!/usr/bin/env python3
"""Generate the Stage 3 sample for Larch Road Health Centre.

Writes:
  sample/LRHC-BMC-ZZ-00-M3-W-000001.ifc   IFC4 model (plain STEP text, no ifcopenshell needed)
  sample/LRHC-BMC-ZZ-ZZ-IE-W-000001.xlsx  COBie 2.4 workbook
  sample/document_register.csv            document register (one row per issue)
  seeded_errors.csv                       the known errors, for scoring in Stage 5

How it works: the clean data is defined once below. Each seeded error is a
small, named edit applied to the IFC copy, the COBie copy, or both. Delete an
entry from SEEDED_ERRORS and re-run to get a clean file.

Usage: python generate_sample.py <repo_folder> <output_folder> [--clean]
       --clean writes the same files with no seeded errors (for false-alarm testing)
"""
import copy
import csv
import sys
import uuid
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

STAGE2 = Path(sys.argv[1])
OUT = Path(sys.argv[2])
CLEAN = "--clean" in sys.argv
(OUT / "sample").mkdir(parents=True, exist_ok=True)

SUBMISSION_DATE = "2027-06-04"          # IE3 handover submission = the check date
CREATED_ON = "2027-06-02T09:00:00"
AUTHOR = "im@brookmason.example"
IFC_NAME = "LRHC-BMC-ZZ-00-M3-W-000001.ifc"
COBIE_NAME = "LRHC-BMC-ZZ-ZZ-IE-W-000001.xlsx"


def read(name):
    return list(csv.DictReader(open(STAGE2 / "reference" / name, newline="")))


SPACES = read("space_schedule.csv")
ASSET_TYPES = read("asset_types.csv")
NET_AREA = {"00-001": 20, "00-002": 40, "00-003": 15, "00-004": 16, "00-005": 16, "00-006": 16,
            "00-007": 16, "00-008": 18, "00-009": 18, "00-010": 18, "00-011": 16, "00-012": 4.5,
            "00-013": 4.5, "00-014": 4.0, "00-015": 15, "00-016": 2.5, "00-017": 20, "00-018": 8,
            "00-019": 45}

# Simple plan: rooms either side of a central corridor (x, y, width, depth in metres).
# Illustrative only: room sizes are not checked against NetArea.
ROOM_HEIGHT = 3.0
ROOMS = {
    "00-001": (0, 12, 5, 4), "00-002": (5, 12, 10, 4), "00-003": (15, 12, 4, 4), "00-004": (19, 12, 4, 4),
    "00-005": (23, 12, 4, 4), "00-006": (27, 12, 4, 4), "00-007": (31, 12, 4, 4),
    "00-008": (0, 6, 4.5, 4), "00-009": (4.5, 6, 4.5, 4), "00-010": (9, 6, 4.5, 4), "00-011": (13.5, 6, 4, 4),
    "00-012": (17.5, 6, 2.25, 4), "00-013": (19.75, 6, 2.25, 4), "00-014": (22, 6, 2, 4), "00-015": (24, 6, 4, 4),
    "00-016": (28, 6, 1.5, 4), "00-017": (29.5, 6, 5, 4), "00-018": (34.5, 6, 2, 4), "00-019": (0, 10, 36.5, 2),
}


def asset_box(code, space, n):
    """Where an asset sits in its room (local x, y, z) and its size (w, d, h). n = how many of this code are already in the room."""
    x0, y0, w, d = ROOMS[space]
    north = y0 >= 12                       # north rooms open onto the corridor at local y = 0
    door_y = -0.05 if north else d - 0.05  # corridor wall
    back_y = d - 0.5 if north else 0.05    # wall away from the corridor
    if space == "00-019":                  # corridor: items spaced along it
        xs = {"FD": [12, 24], "FDM": [12.3, 24.3], "LF": [6, 18]}
        x = xs.get(code, [2 + 4 * n])[n]
        return {"FD": (x, 0, 0, 0.1, 2.0, 2.1), "FDM": (x, 0.8, 2.6, 0.4, 0.4, 0.4),
                "LF": (x, 0.7, 2.9, 0.6, 0.6, 0.1)}[code]
    basin_x = max(w - 1.0, 0.8)
    return {
        "AHU": (1.0, 1.0, 0.0, 2.0, 1.0, 1.5),
        "FD": (0.5, door_y, 0.0, 1.0, 0.1, 2.1),
        "FDM": (2.5 + 1.0 * n, 0.3 if north else d - 0.7, 2.6, 0.4, 0.4, 0.4),
        "WHB": (basin_x, back_y, 0.8, 0.6, 0.45, 0.2),
        "TMV": (basin_x + 0.2, back_y + 0.1, 0.45, 0.15, 0.15, 0.15),
        "WC": (0.2, back_y if not north else d - 0.65, 0.0, 0.4, 0.6, 0.4),
        "NCU": (0.2, back_y, 1.3, 0.1, 0.05, 0.15),
        "EAC": (0.4, d / 2, 2.7, 0.08, 0.08, 0.08),
        "LF": (w / 2 - 0.3, d / 2 - 0.3, 2.9, 0.6, 0.6, 0.1),
    }[code]


# ---------------------------------------------------------------- clean data
CONTACTS = [  # email, company, category
    (AUTHOR, "Brook & Mason Construction Ltd", "Contractor"),
    ("estates@larchvalley.example", "Larch Valley ICB", "Client"),
    ("sales@aircore.example", "Aircore Air Systems Ltd", "Manufacturer"),
    ("sales@oakline.example", "Oakline Doorsets Ltd", "Manufacturer"),
    ("sales@firestop.example", "Firestop Dampers Ltd", "Manufacturer"),
    ("sales@thermasafe.example", "Thermasafe Valves Ltd", "Manufacturer"),
    ("sales@callpoint.example", "CallPoint Systems Ltd", "Manufacturer"),
    ("sales@brightway.example", "Brightway Lighting Ltd", "Manufacturer"),
    ("sales@claymore.example", "Claymore Sanitaryware Ltd", "Manufacturer"),
]
COMPANY = {e: c for e, c, _ in CONTACTS}

# name: code, variant, description, manufacturer, model, warranty years, expected life, type attributes, job
TYPES = {
    "AHU-Type01": ("AHU", "", "Supply and extract air handling unit with heat recovery", "sales@aircore.example", "AC-SR-2500", 2, 20, {},
                   (6, "month", "Replace panel and bag filters; check fan bearings and belts; clean heat recovery coil and drip tray; check dampers, controls and alarms; record filter pressure drops.")),
    "FD-Type01": ("FD", "", "FD60S single-leaf timber fire doorset", "sales@oakline.example", "OD-60S-SL", 10, 30, {"FireRating": "FD60S"},
                  (6, "month", "Check the door closes fully from any angle; check intumescent and smoke seals; check gaps are 2-4 mm; check hinges, closer, signage and certification label.")),
    "FD-Type02": ("FD", "", "FD30S single-leaf timber fire doorset", "sales@oakline.example", "OD-30S-SL", 10, 30, {"FireRating": "FD30S"},
                  (6, "month", "Check the door closes fully from any angle; check intumescent and smoke seals; check gaps are 2-4 mm; check hinges, closer, signage and certification label.")),
    "FDM-Type01": ("FDM", "", "Fusible-link fire damper, 60 minutes", "sales@firestop.example", "FS-60-FL", 2, 25,
                   {"FireResistanceMinutes": 60, "ActuationType": "FusibleLink"},
                   (12, "month", "Drop test: release the fusible link and confirm the blade closes fully; inspect blade, seals and link; reset the damper and record the result.")),
    "TMV-Type01": ("TMV", "", "TMV3 under-basin thermostatic mixing valve", "sales@thermasafe.example", "TS-15-T3", 2, 10, {"TMVApproval": "TMV3"},
                   (6, "month", "Measure the mixed water temperature at the basin outlet; carry out a fail-safe test by isolating the cold supply; clean strainers and check valves; record results.")),
    "NCU-Type01": ("NCU", "", "Patient pull-cord nurse call unit", "sales@callpoint.example", "CP-NC-200", 2, 15, {"CallType": "PatientCall"},
                   (6, "month", "Operate each call point; confirm the call shows at the indicator panel and overdoor light; reset and record.")),
    "EAC-Type01": ("EAC", "", "Accessible WC emergency assistance pull cord", "sales@callpoint.example", "CP-EA-100", 2, 15, {"CallType": "EmergencyAssistance"},
                   (6, "month", "Pull the cord; confirm the overdoor indicator and sounder operate; check the cord reaches floor level; reset and record.")),
    "LF-Type01": ("LF", "GEN", "LED recessed downlight", "sales@brightway.example", "BW-DL-18", 5, 20, {"EmergencyLighting": "N"}, None),
    "LF-Type02": ("LF", "EM", "Self-contained LED emergency luminaire, 3 hour", "sales@brightway.example", "BW-EM-3H", 5, 15, {"EmergencyLighting": "Y"},
                  (1, "month", "Monthly function test by simulating mains failure; check the lamp lights and the charge indicator; record the result.")),
    "WC-Type01": ("WC", "", "Wall-hung WC pan", "sales@claymore.example", "CS-WC-55", None, 25, {}, None),
    "WHB-Type01": ("WHB", "CLIN", "Clinical washbasin, no overflow, no plug", "sales@claymore.example", "CS-CB-50", None, 25, {}, None),
    "WHB-Type02": ("WHB", "GEN", "General washbasin", "sales@claymore.example", "CS-GB-45", None, 25, {}, None),
}

# name, type, space, serial, install date, component attributes
C = []
def comp(name, typ, space, serial=None, installed=None, **attrs):
    C.append({"Name": name, "TypeName": typ, "Space": space, "SerialNumber": serial or "",
              "InstallationDate": installed or "", "Attributes": attrs})

comp("AHU-00-001", "AHU-Type01", "00-017", "ACR-24-001187", "2027-03-15", AirflowRate=2.5)
for i, (sp, t, cert) in enumerate([("00-017", "FD-Type01", "OL-CERT-60412"), ("00-018", "FD-Type02", "OL-CERT-30881"),
                                   ("00-019", "FD-Type02", "OL-CERT-30882"), ("00-019", "FD-Type02", "OL-CERT-30883")], 1):
    comp(f"FD-00-{i:03d}", t, sp, None, "2027-04-20", CertificationNumber=cert)
for i, sp in enumerate(["00-017", "00-017", "00-019", "00-019"], 1):
    comp(f"FDM-00-{i:03d}", "FDM-Type01", sp, f"FS-77{810 + i}", "2027-03-22")
clinical = ["00-004", "00-005", "00-006", "00-007", "00-008", "00-009", "00-010", "00-011"]
general = ["00-012", "00-013", "00-014", "00-016"]
for i, sp in enumerate(clinical + general, 1):
    comp(f"WHB-00-{i:03d}", "WHB-Type01" if sp in clinical else "WHB-Type02", sp)
patient_basins = [c for c in C if c["Name"].startswith("WHB") and c["Space"] != "00-016"]
for i, whb in enumerate(patient_basins, 1):
    comp(f"TMV-00-{i:03d}", "TMV-Type01", whb["Space"], f"TS-T3-{4400 + i}", "2027-04-08",
         SetTemperature=41, ServesComponent=whb["Name"])
for i, sp in enumerate(["00-012", "00-013", "00-016"], 1):
    comp(f"WC-00-{i:03d}", "WC-Type01", sp)
for i, sp in enumerate(["00-008", "00-009", "00-010", "00-011"], 1):
    comp(f"NCU-00-{i:03d}", "NCU-Type01", sp, f"CPN-{20500 + i}", "2027-04-28")
for i, sp in enumerate(["00-012", "00-013"], 1):
    comp(f"EAC-00-{i:03d}", "EAC-Type01", sp, f"CPE-{10200 + i}", "2027-04-28")
for i, (sp, t) in enumerate([("00-001", "LF-Type01"), ("00-002", "LF-Type01"), ("00-003", "LF-Type01"),
                             ("00-019", "LF-Type02"), ("00-019", "LF-Type02"), ("00-017", "LF-Type02")], 1):
    comp(f"LF-00-{i:03d}", t, sp, None, "2027-05-05")

WARRANTY_START = "2027-06-04"  # practical completion
for c in C:
    if c["InstallationDate"]:
        c["WarrantyStartDate"] = WARRANTY_START
    else:
        c["WarrantyStartDate"] = ""
    c["_key"] = c["Name"]  # fixed key, so renamed or duplicated assets keep their own GUID
ORIG_SPACE = {c["_key"]: c["Space"] for c in C}

DOCUMENTS = [  # name, category, sheet, row, description
    ("LRHC-BMC-ZZ-ZZ-RP-W-000001", "O&M manual", "Facility", "Larch Road Health Centre", "Operation and maintenance manual"),
    ("LRHC-KBS-ZZ-ZZ-RP-P-000001", "Commissioning report", "Type", "TMV-Type01", "TMV commissioning report"),
    ("LRHC-KBS-ZZ-ZZ-RP-M-000001", "Test report", "Type", "FDM-Type01", "Fire damper drop-test report"),
    ("LRHC-KBS-ZZ-ZZ-RP-M-000002", "Manufacturer manual", "Type", "AHU-Type01", "AHU installation and maintenance manual"),
]

REGISTER = []  # container, title, originator, status, revision, status_date
for cont, title in [("LRHC-FLD-ZZ-00-M3-A-000001", "Architectural model"), ("LRHC-KBS-ZZ-00-M3-M-000001", "Mechanical model"),
                    ("LRHC-KBS-ZZ-00-M3-E-000001", "Electrical model"), ("LRHC-KBS-ZZ-00-M3-P-000001", "Public health model"),
                    ("LRHC-FLD-ZZ-ZZ-SH-A-000001", "Door schedule")]:
    for st, rev, d in [("S2", "P01", "2026-12-04"), ("S4", "P02", "2027-01-13"), ("A4", "C01", "2027-01-29")]:
        REGISTER.append([cont, title, cont.split("-")[1], st, rev, d])
for cont, title in [("LRHC-BMC-ZZ-ZZ-IE-W-000001", "COBie"), ("LRHC-BMC-ZZ-00-M3-W-000001", "As-constructed federated model")]:
    REGISTER += [[cont, title, "BMC", "S3", "P01", "2027-04-14"], [cont, title, "BMC", "S4", "P02", "2027-06-02"]]
REGISTER += [["LRHC-BMC-ZZ-ZZ-RP-W-000001", "O&M manual", "BMC", "S3", "P01", "2027-05-10"],
             ["LRHC-BMC-ZZ-ZZ-RP-W-000001", "O&M manual", "BMC", "S4", "P02", "2027-06-01"],
             ["LRHC-KBS-ZZ-ZZ-RP-P-000001", "TMV commissioning report", "KBS", "S4", "P01", "2027-06-01"],
             ["LRHC-KBS-ZZ-ZZ-RP-M-000001", "Fire damper drop-test report", "KBS", "S4", "P01", "2027-06-02"]]

# ---------------------------------------------------------------- two copies
ifc = {"components": copy.deepcopy(C), "types": copy.deepcopy(TYPES), "guid_override": {}}
cob = {"components": copy.deepcopy(C), "types": copy.deepcopy(TYPES), "documents": list(DOCUMENTS),
       "guid_override": {}, "job_override": {}}
reg = [list(r) for r in REGISTER]


def find(side, name, nth=0):
    return [c for c in side["components"] if c["Name"] == name][nth]


def set_type(side, name, **changes):
    t = list(side["types"][name])
    fields = ["code", "variant", "desc", "maker", "model", "warranty", "life", "attrs", "job"]
    for k, v in changes.items():
        t[fields.index(k)] = v
    side["types"][name] = tuple(t)


# ---------------------------------------------------------------- seeded errors
# id, layer, description, file, object, field, seeded value, correct value, expected rules, may also trigger, clause, severity
SEEDED_ERRORS = []

def seed(eid, layer, desc, file, obj, field, bad, good, rules, also, clause, sev, apply):
    if CLEAN:
        return
    apply()
    SEEDED_ERRORS.append([eid, layer, desc, file, obj, field, bad, good, rules, also, clause, sev])

seed("E01", 1, "Missing serial number on a TMV (safety-critical)", "IFC+COBie", "TMV-00-007", "SerialNumber", "(blank)", "TS-T3-4407",
     "L1-04", "", "AIR-08", "fail",
     lambda: [find(s, "TMV-00-007").update(SerialNumber="") for s in (ifc, cob)])
seed("E02", 1, "Withdrawn Uniclass code used for a fire door type", "IFC+COBie", "FD-Type02", "Category", "Pr_30_59_24_28 : Fire doorsets",
     "Pr_30_59_24_97 : Wood doorsets", "L1-15;L1-16", "L1-14", "CLS-01;CLS-04", "fail",
     lambda: None)  # applied in the classification step below
seed("E03", 1, "Malformed document name in COBie (underscores instead of hyphens)", "COBie", "Document sheet", "Name",
     "LRHC_KBS_ZZ_ZZ_RP_M_000002", "LRHC-KBS-ZZ-ZZ-RP-M-000002", "L1-10", "L1-07", "NAM-01", "fail",
     lambda: cob.__setitem__("documents", [("LRHC_KBS_ZZ_ZZ_RP_M_000002",) + d[1:] if d[0].endswith("000002") else d for d in cob["documents"]]))
seed("E04", 3, "Light fitting not in any space (COBie Space blank; IFC contained in the storey, not a space)", "IFC+COBie", "LF-00-002", "Space",
     "(blank) / IfcBuildingStorey", "00-002", "L3-04", "L1-04", "LOC-01;AIR-04", "fail",
     lambda: [find(s, "LF-00-002").update(Space="") for s in (ifc, cob)])
seed("E05", 3, "Asset in COBie but missing from the IFC", "IFC", "WHB-00-012", "(whole element)", "missing from IFC", "present in both",
     "L3-02", "L3-17", "FMT-04", "fail",
     lambda: ifc.__setitem__("components", [c for c in ifc["components"] if c["Name"] != "WHB-00-012"]))
seed("E06", 3, "Warranty starts before installation", "IFC+COBie", "AHU-00-001", "WarrantyStartDate", "2027-02-01", "2027-06-04",
     "L3-11", "", "AIR-17", "fail",
     lambda: [find(s, "AHU-00-001").update(WarrantyStartDate="2027-02-01") for s in (ifc, cob)])
seed("E07", 1, "TMV maintenance job has no interval", "COBie", "TMV-Type01 (Job sheet)", "Frequency / FrequencyUnit", "(blank)", "6 month",
     "L1-05", "L1-22", "AIR-13;AIR-19", "fail",
     lambda: cob["job_override"].__setitem__("TMV-Type01", {"Frequency": "", "FrequencyUnit": ""}))
seed("E08", 2, "Document at the wrong status for its milestone (S3 at IE3 due date; S4 required)", "Register", "LRHC-KBS-ZZ-ZZ-RP-P-000001",
     "status", "S3", "S4", "L2-02", "", "STA-04", "fail",
     lambda: [r.__setitem__(3, "S3") for r in reg if r[0] == "LRHC-KBS-ZZ-ZZ-RP-P-000001"])
seed("E09", 1, "Duplicate asset name (NCU-00-003 in the paediatric room was named NCU-00-002)", "IFC+COBie", "NCU-00-002 (x2)", "Name",
     "NCU-00-002", "NCU-00-003", "L1-12", "L3-03", "NAM-04", "fail",
     lambda: [find(s, "NCU-00-003").update(Name="NCU-00-002") for s in (ifc, cob)])
seed("E10", 3, "TMV in the nurse room serves the paediatric room basin; nurse room basin left unprotected", "IFC+COBie", "TMV-00-008",
     "ServesComponent", "WHB-00-007", "WHB-00-008", "L3-13", "", "LOC-03;AIR-23", "fail",
     lambda: [find(s, "TMV-00-008")["Attributes"].update(ServesComponent="WHB-00-007") for s in (ifc, cob)])
seed("E11", 3, "COBie GUID does not match the IFC GlobalId", "COBie", "FDM-00-003", "ExtIdentifier", "GUID of a different object",
     "IFC GlobalId of FDM-00-003", "L3-03", "", "FMT-04", "fail",
     lambda: cob["guid_override"].__setitem__("FDM-00-003", "FDM-00-003-wrong"))
seed("E12", 2, "Revision goes backwards (P01 issued after P02)", "Register", "LRHC-BMC-ZZ-ZZ-RP-W-000001", "revision", "P02 then P01",
     "P02 then P03", "L2-04", "", "STA-03", "fail",
     lambda: reg.append(["LRHC-BMC-ZZ-ZZ-RP-W-000001", "O&M manual", "BMC", "S4", "P01", "2027-06-03"]))
seed("E13", 4, "Generic maintenance description on fire door type", "COBie", "FD-Type02 (Job sheet)", "Description",
     "Inspect as per manufacturer's recommendations.", "Named tasks (closer, seals, gaps, hinges, signage)", "L4-01", "", "AIR-28", "flag",
     lambda: cob["job_override"].__setitem__("FD-Type02", {"Description": "Inspect as per manufacturer's recommendations."}))

WITHDRAWN_FD = ("Pr_30_59_24_28", "Fire doorsets")

# ---------------------------------------------------------------- lookups
def pr_for(code, variant):
    t = next(a for a in ASSET_TYPES if a["asset_code"] == code and a["variant"] == variant)
    return t["uniclass_pr"], t["uniclass_pr_title"], t


def type_class(name, tdef):
    if name == "FD-Type02" and not CLEAN:  # seeded error E02
        return WITHDRAWN_FD
    pr, title, _ = pr_for(tdef[0], tdef[1])
    return pr, title


B64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_$"
NS = uuid.uuid5(uuid.NAMESPACE_URL, "lrhc-cde-data-quality")


def guid(key):
    """Deterministic IFC GlobalId (22 characters, base 64)."""
    n = uuid.uuid5(NS, key).int
    return "".join(B64[(n >> (6 * i)) & 63] for i in reversed(range(22)))


def component_guid(c, side):
    over = side["guid_override"].get(c["_key"])
    return guid(over) if over else guid("comp:" + c["_key"])


# ---------------------------------------------------------------- IFC writer
class Ref:
    def __init__(self, n): self.n = n
class Enum(str): pass
class Typed:
    def __init__(self, t, v): self.t, self.v = t, v
STAR = object()


def fmt(a):
    if a is None: return "$"
    if a is STAR: return "*"
    if isinstance(a, Ref): return f"#{a.n}"
    if isinstance(a, Enum): return f".{a}."
    if isinstance(a, bool): return ".T." if a else ".F."
    if isinstance(a, Typed): return f"{a.t}({fmt(a.v)})"
    if isinstance(a, float): return repr(a)
    if isinstance(a, int): return str(a)
    if isinstance(a, str):
        if not a.isascii():
            raise ValueError(f"non-ASCII text in IFC: {a!r}")
        return "'" + a.replace("\\", "\\\\").replace("'", "''") + "'"
    if isinstance(a, (list, tuple)): return "(" + ",".join(fmt(x) for x in a) + ")"
    raise TypeError(a)


class Step:
    def __init__(self): self.rows = []
    def add(self, entity, *args):
        self.rows.append(f"#{len(self.rows) + 1}={entity}({','.join(fmt(a) for a in args)});")
        return Ref(len(self.rows))


def ifc_value(v, kind="label"):
    if kind == "date": return Typed("IFCDATE", v)
    if kind == "id": return Typed("IFCIDENTIFIER", v)
    if isinstance(v, bool): return Typed("IFCBOOLEAN", v)
    if isinstance(v, int) and kind == "int": return Typed("IFCINTEGER", v)
    if isinstance(v, (int, float)): return Typed("IFCREAL", float(v))
    return Typed("IFCLABEL", str(v))


DIST_TYPES = {"IfcUnitaryEquipment", "IfcDamper", "IfcValve", "IfcCommunicationsAppliance", "IfcLightFixture", "IfcSanitaryTerminal"}


def write_ifc(path):
    s = Step()
    origin = s.add("IFCCARTESIANPOINT", (0.0, 0.0, 0.0))
    place = s.add("IFCAXIS2PLACEMENT3D", origin, None, None)
    ctx = s.add("IFCGEOMETRICREPRESENTATIONCONTEXT", None, "Model", 3, 1.0e-5, place, None)
    units = [s.add("IFCSIUNIT", STAR, Enum(u), None, Enum(n)) for u, n in
             [("LENGTHUNIT", "METRE"), ("AREAUNIT", "SQUARE_METRE"), ("VOLUMEUNIT", "CUBIC_METRE"),
              ("THERMODYNAMICTEMPERATUREUNIT", "DEGREE_CELSIUS")]]
    ua = s.add("IFCUNITASSIGNMENT", units)
    project = s.add("IFCPROJECT", guid("project"), None, "LRHC", "Larch Road Health Centre", None,
                    "Larch Road Health Centre", "IE3 handover", [ctx], ua)

    def plc(rel):
        return s.add("IFCLOCALPLACEMENT", rel, s.add("IFCAXIS2PLACEMENT3D", origin, None, None))

    z_dir = s.add("IFCDIRECTION", (0.0, 0.0, 1.0))

    def plc_at(rel, x, y, z):
        return s.add("IFCLOCALPLACEMENT", rel,
                     s.add("IFCAXIS2PLACEMENT3D", s.add("IFCCARTESIANPOINT", (float(x), float(y), float(z))), None, None))

    def box(w, d, h):
        """A w x d x h block: a rectangle extruded upwards, as an IFC 'Body' representation."""
        pos2d = s.add("IFCAXIS2PLACEMENT2D", s.add("IFCCARTESIANPOINT", (w / 2, d / 2)), None)
        profile = s.add("IFCRECTANGLEPROFILEDEF", Enum("AREA"), None, pos2d, float(w), float(d))
        solid = s.add("IFCEXTRUDEDAREASOLID", profile, place, z_dir, float(h))
        rep = s.add("IFCSHAPEREPRESENTATION", ctx, "Body", "SweptSolid", [solid])
        return s.add("IFCPRODUCTDEFINITIONSHAPE", None, None, [rep])

    site_p = plc(None)
    site = s.add("IFCSITE", guid("site"), None, "Site", None, None, site_p, None, None, Enum("ELEMENT"),
                 None, None, None, None, None)
    bld_p = plc(site_p)
    bld = s.add("IFCBUILDING", guid("building"), None, "Larch Road Health Centre", None, None, bld_p, None, None,
                Enum("ELEMENT"), None, None, None)
    st_p = plc(bld_p)
    storey = s.add("IFCBUILDINGSTOREY", guid("floor:00"), None, "00", "Ground", None, st_p, None, "Ground floor",
                   Enum("ELEMENT"), 0.0)
    s.add("IFCRELAGGREGATES", guid("agg:project"), None, None, None, project, [site])
    s.add("IFCRELAGGREGATES", guid("agg:site"), None, None, None, site, [bld])
    s.add("IFCRELAGGREGATES", guid("agg:building"), None, None, None, bld, [storey])

    # Uniclass
    uniclass = s.add("IFCCLASSIFICATION", "NBS", "Uniclass 2015 (codes checked November 2026)", None, "Uniclass 2015",
                     None, "https://uniclass.thenbs.com", None)
    class_targets = {}  # (code, title) -> [objects]

    def classify(code, title, obj):
        class_targets.setdefault((code, title), []).append(obj)

    def pset(name, props, key):
        refs = [s.add("IFCPROPERTYSINGLEVALUE", k, None, v, None) for k, v in props]
        return s.add("IFCPROPERTYSET", guid(f"pset:{name}:{key}"), None, name, None, refs)

    def attach(objs, ps, key):
        s.add("IFCRELDEFINESBYPROPERTIES", guid(f"rdp:{key}"), None, None, None, objs, ps)

    # Spaces
    space_ref, space_plc = {}, {}
    for sp in SPACES:
        x0, y0, w, d = ROOMS[sp["space_name"]]
        p = plc_at(st_p, x0, y0, 0)
        r = s.add("IFCSPACE", guid("space:" + sp["space_name"]), None, sp["space_name"], None, None, p, box(w, d, ROOM_HEIGHT),
                  sp["room_name"], Enum("ELEMENT"), Enum("SPACE"), None)
        space_ref[sp["space_name"]], space_plc[sp["space_name"]] = r, p
        classify(sp["uniclass_sl"], sp["uniclass_sl_title"], r)
        attach([r], pset("LRHC_AssetData", [("PatientArea", ifc_value(sp["patient_area"]))], sp["space_name"]),
               "space-pset:" + sp["space_name"])
        qa = s.add("IFCQUANTITYAREA", "NetFloorArea", None, None, float(NET_AREA[sp["space_name"]]), None)
        eq = s.add("IFCELEMENTQUANTITY", guid("qto:" + sp["space_name"]), None, "Qto_SpaceBaseQuantities", None, None, [qa])
        attach([r], eq, "space-qto:" + sp["space_name"])
    s.add("IFCRELAGGREGATES", guid("agg:storey"), None, None, None, storey, list(space_ref.values()))

    # Types
    type_ref = {}
    for name, t in ifc["types"].items():
        code, variant, desc, maker, model, wy, life, attrs, _job = t
        _, _, at = pr_for(code, variant)
        psets = [pset("Pset_ManufacturerTypeInformation",
                      [("Manufacturer", ifc_value(COMPANY[maker])), ("ModelReference", ifc_value(model))], name)]
        data = []
        if wy is not None:
            data += [("WarrantyDurationParts", ifc_value(float(wy))), ("WarrantyDurationUnit", ifc_value("year"))]
        data += [("ExpectedLife", ifc_value(float(life))), ("DurationUnit", ifc_value("year"))]
        for k, v in attrs.items():
            if k == "FireRating":
                continue
            data.append((k, ifc_value(v, "int" if isinstance(v, int) else "label")))
        psets.append(pset("LRHC_AssetData", data, name))
        if "FireRating" in attrs:
            psets.append(pset("Pset_DoorCommon", [("FireRating", ifc_value(attrs["FireRating"]))], name))
        entity = at["ifc_entity"]
        predef = Enum(at["ifc_predefined_type"] or "NOTDEFINED")
        if entity == "IfcDoor":
            r = s.add("IFCDOORTYPE", guid("type:" + name), None, name, desc, None, psets, None, None, None,
                      Enum("DOOR"), Enum("SINGLE_SWING_LEFT"), None, None)
        else:
            r = s.add(entity.upper() + "TYPE", guid("type:" + name), None, name, desc, None, psets, None, None,
                      at["ifc_object_type"] or None, predef)
        type_ref[name] = r
        classify(*type_class(name, t), r)

    # Components
    by_type, by_space, storey_only = {}, {}, []
    comp_ref, placed = {}, {}
    for c in ifc["components"]:
        t = ifc["types"][c["TypeName"]]
        _, _, at = pr_for(t[0], t[1])
        entity = at["ifc_entity"]
        sp = c["Space"]
        room = ORIG_SPACE[c["_key"]]              # where it physically is, even if the space link is missing (E04)
        n = placed.get((room, t[0]), 0)
        placed[(room, t[0])] = n + 1
        lx, ly, lz, bw, bd, bh = asset_box(t[0], room, n)
        if sp:
            p = plc_at(space_plc[sp], lx, ly, lz)
        else:                                     # not linked to a space: place relative to the storey
            p = plc_at(st_p, ROOMS[room][0] + lx, ROOMS[room][1] + ly, lz)
        shape = box(bw, bd, bh)
        desc = t[2]
        g = component_guid(c, ifc)
        if entity == "IfcDoor":
            r = s.add("IFCDOOR", g, None, c["Name"], desc, None, p, shape, None, 2.1, 0.926,
                      Enum("DOOR"), Enum("SINGLE_SWING_LEFT"), None)
        else:
            predef = Enum(at["ifc_predefined_type"]) if at["ifc_predefined_type"] else None
            r = s.add(entity.upper(), g, None, c["Name"], desc, at["ifc_object_type"] or None, p, shape, None, predef)
        comp_ref[c["_key"]] = r
        by_type.setdefault(c["TypeName"], []).append(r)
        (by_space.setdefault(sp, []) if sp else storey_only).append(r)
        if c["SerialNumber"]:
            attach([r], pset("Pset_ManufacturerOccurrence", [("SerialNumber", ifc_value(c["SerialNumber"], "id"))],
                             c["_key"]), "occ:" + c["_key"])
        data = []
        if c["InstallationDate"]:
            data.append(("InstallationDate", ifc_value(c["InstallationDate"], "date")))
        if c["WarrantyStartDate"]:
            data.append(("WarrantyStartDate", ifc_value(c["WarrantyStartDate"], "date")))
        for k, v in c["Attributes"].items():
            data.append((k, ifc_value(v)))
        if data:
            attach([r], pset("LRHC_AssetData", data, "occ:" + c["_key"]), "data:" + c["_key"])

    for tname, objs in by_type.items():
        s.add("IFCRELDEFINESBYTYPE", guid("rdt:" + tname), None, None, None, objs, type_ref[tname])
    for sp, objs in by_space.items():
        s.add("IFCRELCONTAINEDINSPATIALSTRUCTURE", guid("cont:" + sp), None, None, None, objs, space_ref[sp])
    if storey_only:
        s.add("IFCRELCONTAINEDINSPATIALSTRUCTURE", guid("cont:storey"), None, None, None, storey_only, storey)

    # Systems
    for sysname, ss, ss_title, members, predef in systems(ifc):
        refs = [comp_ref[c["_key"]] for c in members]
        r = s.add("IFCDISTRIBUTIONSYSTEM", guid("sys:" + sysname), None, sysname, ss_title, None, ss_title, Enum(predef))
        s.add("IFCRELASSIGNSTOGROUP", guid("grp:" + sysname), None, None, None, refs, None, r)
        classify(ss, ss_title, r)

    for (code, title), objs in class_targets.items():
        ref = s.add("IFCCLASSIFICATIONREFERENCE", f"https://uniclass.thenbs.com/taxon/{code.lower()}", code, title,
                    uniclass, None, None)
        s.add("IFCRELASSOCIATESCLASSIFICATION", guid("cls:" + code), None, "Uniclass 2015", None, objs, ref)

    header = ["ISO-10303-21;", "HEADER;",
              "FILE_DESCRIPTION(('ViewDefinition [ReferenceView_V1.2]'),'2;1');",
              f"FILE_NAME('{IFC_NAME}','{CREATED_ON}',('Brook and Mason Construction'),('BMC'),"
              "'cde-data-quality generate_sample.py','generate_sample.py','');",
              "FILE_SCHEMA(('IFC4'));", "ENDSEC;", "DATA;"]
    path.write_text("\n".join(header + s.rows + ["ENDSEC;", "END-ISO-10303-21;", ""]), encoding="ascii")
    return len(s.rows)


SYS_PREDEF = {"Ss_65_40_33_49": "VENTILATION", "Ss_55_70_38_42": "DOMESTICHOTWATER",
              "Ss_70_80_33_35": "LIGHTING", "Ss_70_80_33_78": "LIGHTING"}
SYS_NAME = {"Ss_65_40_33_49": "SYS-VENT-01", "Ss_55_70_38_42": "SYS-HWS-01", "Ss_75_50_11_57": "SYS-NC-01",
            "Ss_75_50_11_25": "SYS-EAC-01", "Ss_70_80_33_35": "SYS-LTG-01", "Ss_70_80_33_78": "SYS-EML-01"}


def systems(side):
    out = {}
    for c in side["components"]:
        t = side["types"][c["TypeName"]]
        _, _, at = pr_for(t[0], t[1])
        if at["uniclass_ss"]:
            out.setdefault((at["uniclass_ss"], at["uniclass_ss_title"]), []).append(c)
    return [(SYS_NAME[ss], ss, title, members, SYS_PREDEF.get(ss, "NOTDEFINED")) for (ss, title), members in out.items()]


# ---------------------------------------------------------------- COBie writer
def cobie_date(d):
    return f"{d}T00:00:00" if d else "n/a"


def write_cobie(path):
    wb = Workbook()
    wb.remove(wb.active)

    def sheet(name, headers, rows):
        ws = wb.create_sheet(name)
        ws.append(headers)
        for cell in ws[1]:
            cell.font = Font(bold=True)
        for r in rows:
            ws.append([r.get(h, "n/a") if isinstance(r, dict) else r for h in headers] if isinstance(r, dict) else r)
        ws.freeze_panes = "A2"

    base = {"CreatedBy": AUTHOR, "CreatedOn": CREATED_ON, "ExtSystem": "generate_sample.py"}
    sheet("Contact", ["Email", "CreatedBy", "CreatedOn", "Category", "Company", "Phone", "ExtSystem", "ExtObject",
                      "ExtIdentifier", "Department", "OrganizationCode", "GivenName", "FamilyName", "Street",
                      "PostalBox", "Town", "StateRegion", "PostalCode", "Country"],
          [dict(base, Email=e, Category=cat, Company=co, ExtObject="IfcOrganization") for e, co, cat in CONTACTS])
    sheet("Facility", ["Name", "CreatedBy", "CreatedOn", "Category", "ProjectName", "SiteName", "LinearUnits",
                       "AreaUnits", "VolumeUnits", "CurrencyUnit", "AreaMeasurement", "ExternalSystem",
                       "ExternalProjectObject", "ExternalProjectIdentifier", "ExternalSiteObject",
                       "ExternalSiteIdentifier", "ExternalFacilityObject", "ExternalFacilityIdentifier",
                       "Description", "ProjectDescription", "SiteDescription", "Phase"],
          [dict(base, Name="Larch Road Health Centre", Category="n/a", ProjectName="LRHC",
                SiteName="Site", LinearUnits="metres", AreaUnits="square metres", VolumeUnits="cubic metres",
                CurrencyUnit="GBP", AreaMeasurement="NetFloorArea", ExternalSystem="generate_sample.py",
                ExternalProjectObject="IfcProject", ExternalProjectIdentifier=guid("project"),
                ExternalSiteObject="IfcSite", ExternalSiteIdentifier=guid("site"),
                ExternalFacilityObject="IfcBuilding", ExternalFacilityIdentifier=guid("building"),
                Description="Single-storey GP practice and clinic", Phase="IE3 handover")])
    sheet("Floor", ["Name", "CreatedBy", "CreatedOn", "Category", "ExtSystem", "ExtObject", "ExtIdentifier",
                    "Description", "Elevation", "Height"],
          [dict(base, Name="00", Category="Floor", ExtObject="IfcBuildingStorey", ExtIdentifier=guid("floor:00"),
                Description="Ground floor", Elevation=0, Height=3.6)])
    sheet("Space", ["Name", "CreatedBy", "CreatedOn", "Category", "FloorName", "Description", "ExtSystem",
                    "ExtObject", "ExtIdentifier", "RoomTag", "UsableHeight", "GrossArea", "NetArea"],
          [dict(base, Name=sp["space_name"], Category=f"{sp['uniclass_sl']} : {sp['uniclass_sl_title']}",
                FloorName="00", Description=sp["room_name"], ExtObject="IfcSpace",
                ExtIdentifier=guid("space:" + sp["space_name"]), RoomTag=sp["space_name"],
                NetArea=NET_AREA[sp["space_name"]]) for sp in SPACES])

    type_rows = []
    for name, t in cob["types"].items():
        code, variant, desc, maker, model, wy, life, attrs, _ = t
        _, _, at = pr_for(code, variant)
        pr, title = type_class(name, t)
        type_rows.append(dict(base, Name=name, Category=f"{pr} : {title}", Description=desc, AssetType="Fixed",
                              Manufacturer=maker, ModelNumber=model,
                              WarrantyGuarantorParts=maker if wy else "n/a",
                              WarrantyDurationParts=wy if wy else "n/a",
                              WarrantyGuarantorLabor=AUTHOR if wy else "n/a",
                              WarrantyDurationLabor=1 if wy else "n/a",
                              WarrantyDurationUnit="year" if wy else "n/a",
                              ExtObject=at["ifc_entity"] + "Type", ExtIdentifier=guid("type:" + name),
                              ExpectedLife=life, DurationUnit="year", ModelReference=model))
    sheet("Type", ["Name", "CreatedBy", "CreatedOn", "Category", "Description", "AssetType", "Manufacturer",
                   "ModelNumber", "WarrantyGuarantorParts", "WarrantyDurationParts", "WarrantyGuarantorLabor",
                   "WarrantyDurationLabor", "WarrantyDurationUnit", "ExtSystem", "ExtObject", "ExtIdentifier",
                   "ReplacementCost", "ExpectedLife", "DurationUnit", "WarrantyDescription", "NominalLength",
                   "NominalWidth", "NominalHeight", "ModelReference", "Shape", "Size", "Color", "Finish", "Grade",
                   "Material", "Constituents", "Features", "AccessibilityPerformance", "CodePerformance",
                   "SustainabilityPerformance"], type_rows)

    comp_rows = []
    for c in cob["components"]:
        t = cob["types"][c["TypeName"]]
        _, _, at = pr_for(t[0], t[1])
        comp_rows.append(dict(base, Name=c["Name"], TypeName=c["TypeName"], Space=c["Space"] or "",
                              Description=t[2], ExtObject=at["ifc_entity"], ExtIdentifier=component_guid(c, cob),
                              SerialNumber=c["SerialNumber"] if c["SerialNumber"] or at["asset_code"] in
                              ("AHU", "FDM", "TMV", "NCU", "EAC") else "n/a",
                              InstallationDate=cobie_date(c["InstallationDate"]),
                              WarrantyStartDate=cobie_date(c["WarrantyStartDate"]),
                              TagNumber="n/a", BarCode="n/a", AssetIdentifier="n/a"))
    sheet("Component", ["Name", "CreatedBy", "CreatedOn", "TypeName", "Space", "Description", "ExtSystem",
                        "ExtObject", "ExtIdentifier", "SerialNumber", "InstallationDate", "WarrantyStartDate",
                        "TagNumber", "BarCode", "AssetIdentifier"], comp_rows)

    sys_rows = []
    for sysname, ss, title, members, _ in systems(cob):
        for c in members:
            sys_rows.append(dict(base, Name=sysname, Category=f"{ss} : {title}", ComponentNames=c["Name"],
                                 ExtObject="IfcDistributionSystem", ExtIdentifier=guid("sys:" + sysname),
                                 Description=title))
    sheet("System", ["Name", "CreatedBy", "CreatedOn", "Category", "ComponentNames", "ExtSystem", "ExtObject",
                     "ExtIdentifier", "Description"], sys_rows)

    job_rows = []
    for name, t in cob["types"].items():
        if not t[8]:
            continue
        freq, unit, desc = t[8]
        row = dict(base, Name=f"PPM-{name}", Category="PPM", Status="Not yet started", TypeName=name,
                   Description=desc, Duration=1, DurationUnit="hour", Start="n/a", TaskStartUnit="month",
                   Frequency=freq, FrequencyUnit=unit, ExtObject="n/a", ExtIdentifier="n/a", TaskNumber="1",
                   Priors="n/a", ResourceNames="n/a")
        row.update(cob["job_override"].get(name, {}))
        job_rows.append(row)
    sheet("Job", ["Name", "CreatedBy", "CreatedOn", "Category", "Status", "TypeName", "Description", "Duration",
                  "DurationUnit", "Start", "TaskStartUnit", "Frequency", "FrequencyUnit", "ExtSystem", "ExtObject",
                  "ExtIdentifier", "TaskNumber", "Priors", "ResourceNames"], job_rows)

    sheet("Document", ["Name", "CreatedBy", "CreatedOn", "Category", "ApprovalBy", "Stage", "SheetName", "RowName",
                       "Directory", "File", "ExtSystem", "ExtObject", "ExtIdentifier", "Description", "Reference"],
          [dict(base, Name=n, Category=cat, ApprovalBy="Information manager", Stage="IE3", SheetName=sh,
                RowName=row, Directory="/handover/", File=n.replace("_", "-") + ".pdf", Description=d,
                Reference="n/a") for n, cat, sh, row, d in cob["documents"]])

    attr_rows = []
    def attr(sheet_name, row, name, value, unit="n/a"):
        attr_rows.append(dict(base, Name=name, Category="Requirement", SheetName=sheet_name, RowName=row,
                              Value=value, Unit=unit, ExtObject="n/a", ExtIdentifier="n/a",
                              Description="LRHC EIR requirement", AllowedValues="n/a"))
    for sp in SPACES:
        attr("Space", sp["space_name"], "PatientArea", sp["patient_area"])
    for name, t in cob["types"].items():
        for k, v in t[7].items():
            attr("Type", name, k, v, "min" if k == "FireResistanceMinutes" else "n/a")
    units = {"SetTemperature": "degC", "AirflowRate": "m3/s"}
    for c in cob["components"]:
        for k, v in c["Attributes"].items():
            attr("Component", c["Name"], k, v, units.get(k, "n/a"))
    sheet("Attribute", ["Name", "CreatedBy", "CreatedOn", "Category", "SheetName", "RowName", "Value", "Unit",
                        "ExtSystem", "ExtObject", "ExtIdentifier", "Description", "AllowedValues"], attr_rows)
    wb.save(path)
    return len(comp_rows)


# ---------------------------------------------------------------- run
n_ifc = write_ifc(OUT / "sample" / IFC_NAME)
n_comp = write_cobie(OUT / "sample" / COBIE_NAME)
with open(OUT / "sample" / "document_register.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["container_name", "title", "originator", "status", "revision", "status_date"])
    w.writerows(sorted(reg, key=lambda r: (r[0], r[5])))
with open(OUT / "seeded_errors.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["error_id", "layer", "description", "file", "object", "field", "seeded_value", "correct_value",
                "expected_rules", "may_also_trigger", "eir_clause", "expected_severity"])
    w.writerows(SEEDED_ERRORS)
print(f"IFC: {n_ifc} entities | COBie: {n_comp} components | register: {len(reg)} rows | seeded errors: {len(SEEDED_ERRORS)}")
