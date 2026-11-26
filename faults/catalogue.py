"""The fault catalogue: 28 deliberate mistakes, each aimed at one check.

Every fault edits the raw input files (as the source systems would export them), never the checker's
internal tables, so the adapters are tested too. Each fault names the checks that should catch it.
A fault is caught when all its expected checks fire; any other check firing is a false alarm.

`raw` is a dict of DataFrames (all text): library, midp, update (P6 activities CSV), cde (ProjectWise export).
"""
from datetime import datetime, timedelta

PW = "%d/%m/%Y %H:%M"          # ProjectWise date format
P6 = "%Y-%m-%d %H:%M"          # P6 CSV date format


def _cde(raw, name, version=None):
    m = raw["cde"]["Name"] == name
    if version is not None:
        m &= raw["cde"]["Version"] == str(version)
    assert m.any(), f"fault target not found: {name} v{version}"
    return m


def _midp(raw, title):
    m = raw["midp"]["title"] == title
    assert m.any(), f"fault target not found: {title}"
    return m


def _shift(text, fmt, days):
    return (datetime.strptime(text, fmt) + timedelta(days=days)).strftime(fmt)


FAULTS = []


def fault(fid, name, expected, target=""):
    def add(fn):
        FAULTS.append(dict(fault_id=fid, fault=name, expected=set(expected), target=target, apply=fn))
        return fn
    return add


# ------------------------------------------------------------------ R: reference data
@fault("F01", "MIDP asks for suitability S5, which is not a code", ["R01"], "LRHC-KBS-ZZ-ZZ-RP-P-000001")
def f01(raw):
    raw["midp"].loc[_midp(raw, "TMV commissioning report"), "required_suitability"] = "S5"


@fault("F02", "MIDP number has 5 digits", ["R01"], "LRHC-KBS-ZZ-ZZ-RP-M-00001")
def f02(raw):
    m = _midp(raw, "Fire damper drop-test report")
    raw["midp"].loc[m, "number"] = "00001"
    raw["midp"].loc[m, "container_name"] = "LRHC-KBS-ZZ-ZZ-RP-M-00001"


@fault("F03", "Client has not approved zone Z4 (still 'proposed')", ["R01", "R02"], "LRHC-FLD-Z4-00-DR-A-000104")
def f03(raw):
    lib = raw["library"]
    m = (lib.list_name == "volume") & (lib.code == "Z4")
    lib.loc[m, ["status", "approved_date"]] = ["proposed", ""]


@fault("F04", "CDE version carries suitability S5", ["R02"], "LRHC-FLD-ZZ-RF-DR-A-000105")
def f04(raw):
    raw["cde"].loc[_cde(raw, "LRHC-FLD-ZZ-RF-DR-A-000105", 1), "ATTR_Suitability"] = "S5"


@fault("F05", "Zone Z3 used on 2 Dec, before the client approved it on 4 Dec", ["R03"], "LRHC-FLD-Z3-00-DR-A-000103")
def f05(raw):
    raw["cde"].loc[_cde(raw, "LRHC-FLD-Z3-00-DR-A-000103", 1), "State Changed"] = "02/12/2026 10:00"


@fault("F06", "MIDP volume says Z1 but the container name says ZZ", ["R04"], "LRHC-KBS-ZZ-ZZ-DR-M-000001")
def f06(raw):
    raw["midp"].loc[_midp(raw, "Ventilation schematic"), "volume"] = "Z1"


# ------------------------------------------------------------------ P: programme link
@fault("F07", "MIDP links to an activity that does not exist", ["P01"], "LRHC-KBS-ZZ-00-M3-P-000001")
def f07(raw):
    raw["midp"].loc[_midp(raw, "Public health model"), "linked_p6_activity"] = "4-MEP-9999"


@fault("F08", "MIDP says Stage 5 for a Stage 4 deliverable", ["P02"], "LRHC-KBS-ZZ-ZZ-DR-P-000001")
def f08(raw):
    raw["midp"].loc[_midp(raw, "Hot and cold water schematic (TMVs)"), "stage"] = "5"


@fault("F09", "MIDP links an IE1 deliverable to an activity after IE1", ["P03"], "LRHC-BMC-ZZ-ZZ-HS-W-000001")
def f09(raw):
    raw["midp"].loc[_midp(raw, "Construction phase plan"), "linked_p6_activity"] = "4-APP-1200"


# ------------------------------------------------------------------ C: completeness and uniqueness
@fault("F10", "A due deliverable is missing from the CDE", ["C01"], "LRHC-FLD-ZZ-ZZ-DR-A-000202")
def f10(raw):
    raw["cde"] = raw["cde"][~_cde(raw, "LRHC-FLD-ZZ-ZZ-DR-A-000202")].reset_index(drop=True)


@fault("F11", "An unplanned container appears in the CDE", ["C02"], "LRHC-FLD-Z2-00-DR-A-000150")
def f11(raw):
    row = raw["cde"][_cde(raw, "LRHC-FLD-Z2-00-DR-A-000102", 1)].iloc[0].copy()
    row["Name"] = "LRHC-FLD-Z2-00-DR-A-000150"
    row["File Name"] = "LRHC-FLD-Z2-00-DR-A-000150.pdf"
    row["ATTR_Number"] = "000150"
    row["Description"] = row["ATTR_Title"] = "Reflected ceiling plan, clinical zone"
    row["Document GUID"] = "00000000-0000-0000-0000-000000000150"
    raw["cde"].loc[len(raw["cde"])] = row


@fault("F12", "MIDP row entered twice", ["C03"], "LRHC-HXM-ZZ-ZZ-SH-X-000001")
def f12(raw):
    row = raw["midp"][_midp(raw, "Module schedule")].iloc[0].copy()
    row["midp_id"] = "MIDP-051"
    raw["midp"].loc[len(raw["midp"])] = row


@fault("F13", "MIDP title left blank", ["C04"], "LRHC-FLD-ZZ-ZZ-DR-A-000201")
def f13(raw):
    raw["midp"].loc[_midp(raw, "Elevations"), "title"] = ""


@fault("F14", "CDE version has no 'Updated By'", ["C05"], "LRHC-BMC-ZZ-ZZ-RP-W-000002")
def f14(raw):
    raw["cde"].loc[_cde(raw, "LRHC-BMC-ZZ-ZZ-RP-W-000002", 2), "Updated By"] = ""


@fault("F15", "Same CDE version exported twice", ["C06"], "LRHC-CKE-EW-00-DR-C-000001")
def f15(raw):
    row = raw["cde"][_cde(raw, "LRHC-CKE-EW-00-DR-C-000001", 1)].iloc[0].copy()
    raw["cde"].loc[len(raw["cde"])] = row


# ------------------------------------------------------------------ T: timeliness
@fault("F16", "Delivered 2 weeks late (no change to the programme)", ["T01", "T02"], "LRHC-FLD-ZZ-ZZ-RP-A-000001")
def f16(raw):
    name = "LRHC-FLD-ZZ-ZZ-RP-A-000001"
    link = raw["midp"].loc[raw["midp"].container_name == name, "linked_p6_activity"].iloc[0]
    due = raw["update"].loc[raw["update"].activity_id == link, "finish"].iloc[0]
    late = datetime.strptime(due, P6).replace(hour=10, minute=0) + timedelta(days=14)
    c = raw["cde"]
    s4 = _cde(raw, name) & (c["ATTR_Suitability"] == "S4")
    c.loc[s4, "State Changed"] = late.strftime(PW)
    a4 = _cde(raw, name) & (c["ATTR_Suitability"] == "A4")
    if datetime.strptime(c.loc[a4, "State Changed"].iloc[0], PW) <= late:
        c.loc[a4, "State Changed"] = (late + timedelta(days=1)).strftime(PW)


@fault("F17", "Issued at S2 when the MIDP asks for S3", ["T01", "T02"], "LRHC-BMC-ZZ-ZZ-IE-W-000001")
def f17(raw):
    c = raw["cde"]
    m = _cde(raw, "LRHC-BMC-ZZ-ZZ-IE-W-000001") & (c["ATTR_Suitability"] == "S3")
    c.loc[m, "ATTR_Suitability"] = "S2"


@fault("F18", "Issue activity slipped 5 days and the delivery followed it", ["T01"], "LRHC-BMC-ZZ-ZZ-RP-W-000003")
def f18(raw):
    u = raw["update"]
    m = u.activity_id == "5-INF-1105"
    for col in ("finish", "actual_finish"):
        u.loc[m, col] = _shift(u.loc[m, col].iloc[0], P6, 5)
    c = raw["cde"]
    s4 = _cde(raw, "LRHC-BMC-ZZ-ZZ-RP-W-000003") & (c["ATTR_Suitability"] == "S4")
    c.loc[s4, "State Changed"] = _shift(c.loc[s4, "State Changed"].iloc[0], PW, 5)


@fault("F19", "Programme forecast for the O&M manual slipped 10 days", ["T03"], "LRHC-BMC-ZZ-ZZ-RP-W-000001")
def f19(raw):
    u = raw["update"]
    m = u.activity_id == "6-INF-1805"
    u.loc[m, "finish"] = _shift(u.loc[m, "finish"].iloc[0], P6, 10)


@fault("F20", "CDE export is a week old", ["T04"])
def f20(raw):
    raw["cde"]["Exported"] = "24/04/2027 06:00"


# ------------------------------------------------------------------ M: metadata match
@fault("F21", "Originator attribute says FLD on a CKE container", ["M01"], "LRHC-CKE-ZZ-ZZ-CA-S-000001")
def f21(raw):
    raw["cde"].loc[_cde(raw, "LRHC-CKE-ZZ-ZZ-CA-S-000001", 2), "ATTR_Originator"] = "FLD"


@fault("F22", "File name carries the revision", ["M02"], "LRHC-FLD-ZZ-00-M3-A-000001")
def f22(raw):
    raw["cde"].loc[_cde(raw, "LRHC-FLD-ZZ-00-M3-A-000001", 2), "File Name"] = "LRHC-FLD-ZZ-00-M3-A-000001_P02.ifc"


@fault("F23", "Description and title attribute disagree on one version", ["M03"], "LRHC-FLD-ZZ-ZZ-SP-A-000001")
def f23(raw):
    raw["cde"].loc[_cde(raw, "LRHC-FLD-ZZ-ZZ-SP-A-000001", 2), "Description"] = "Architectural spec"


@fault("F24", "CDE title differs from the MIDP title", ["M04"], "LRHC-FLD-ZZ-ZZ-SH-A-000001")
def f24(raw):
    m = _cde(raw, "LRHC-FLD-ZZ-ZZ-SH-A-000001")
    raw["cde"].loc[m, ["Description", "ATTR_Title"]] = "Door and ironmongery schedule"


@fault("F25", "A4 version given a P revision", ["M05"], "LRHC-CKE-ZZ-00-DR-S-000001")
def f25(raw):
    c = raw["cde"]
    m = _cde(raw, "LRHC-CKE-ZZ-00-DR-S-000001") & (c["ATTR_Suitability"] == "A4")
    c.loc[m, "ATTR_Revision"] = "P03"


@fault("F26", "S4 version left in the Published state", ["M06"], "LRHC-KBS-ZZ-ZZ-DR-E-000001")
def f26(raw):
    c = raw["cde"]
    m = _cde(raw, "LRHC-KBS-ZZ-ZZ-DR-E-000001") & (c["ATTR_Suitability"] == "S4")
    c.loc[m, "State"] = "Published"


@fault("F27", "Revision jumps from P01 to P03", ["M07"], "LRHC-KBS-ZZ-00-M3-M-000001")
def f27(raw):
    c = raw["cde"]
    m = _cde(raw, "LRHC-KBS-ZZ-00-M3-M-000001") & (c["ATTR_Revision"] == "P02")
    c.loc[m, "ATTR_Revision"] = "P03"


@fault("F28", "Status date after the data date", ["M08"], "LRHC-KBS-ZZ-ZZ-RP-E-000001")
def f28(raw):
    raw["cde"].loc[_cde(raw, "LRHC-KBS-ZZ-ZZ-RP-E-000001", 1), "State Changed"] = "15/05/2027 11:00"
