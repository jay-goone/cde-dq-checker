"""Build the perfect CDE export: a ProjectWise-style saved-search export, one row per version.

Rules for the perfect example (every version is on time and matches the MIDP):
- Each MIDP row produces two versions:
    a work-in-progress share during 'Develop' (S1 for models and drawings, S2 for everything else),
    and the issue at the MIDP's required suitability on the finish date of the linked P6 activity.
- Stage 4 deliverables (IE1) are then authorised: A4 on the day the client signs off Stage 4.
- Revisions run per container in date order: P01, P02 … for S codes; C01, C02 … for A codes and CR.
- Only versions with a state change on or before the export date appear in the export.

Run from the repo root:  python delivery_planner/tools/build_cde.py
"""
import csv, random, sys, uuid
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from adapters import p6

DATA = ROOT / "data"
OUT = DATA / "cde"
OUT.mkdir(exist_ok=True)
EXPORT_AT = datetime(2027, 5, 1, 6, 0)           # nightly export, morning of the data date
rnd = random.Random(4920203)                     # fixed seed: the same file every run

acts = p6.from_xer(DATA / "programme/LRHC_programme_update_2027-05-01.xer").set_index("activity_id")
midp = list(csv.DictReader(open(DATA / "midp.csv", encoding="utf-8")))

PEOPLE = {
    "FLD": ["a.okafor@fld-architects.example", "r.chen@fld-architects.example"],
    "CKE": ["m.davies@corbelkeel.example"],
    "KBS": ["s.patel@kestrel-bs.example", "t.nowak@kestrel-bs.example"],
    "HXM": ["j.lindqvist@hexmodule.example"],
    "BMC": ["l.hughes@brookmason.example", "k.mensah@brookmason.example"],
}
EXT = {"M3": "ifc", "CM": "nwd", "DR": "pdf", "SH": "xlsx", "IE": "xlsx", "PR": "xer"}
SIGN_OFF = acts.loc["4-APP-1200", "finish"]      # client Stage 4 sign-off


def stamp(day, latest_hour=16):
    """A working-hours time on the given day, no later than the activity's 17:00 finish."""
    return datetime(day.year, day.month, day.day, rnd.randint(9, latest_hour), rnd.randint(0, 59))


events = {}          # container -> list of (time, suitability, midp row)
for r in midp:
    issue = acts.loc[r["linked_p6_activity"]]
    develop = acts.loc[r["linked_p6_activity"][:-1] + "0"]
    mid = develop.start + (develop.finish - develop.start) / 2
    wip = "S1" if r["type"] in ("M3", "CM", "DR") else "S2"
    ev = events.setdefault(r["container_name"], [])
    ev.append((stamp(mid), wip, r))
    ev.append((stamp(issue.finish), r["required_suitability"], r))
    if r["exchange"] == "IE1":
        ev.append((stamp(SIGN_OFF), "A4", r))

COLS = ["Name", "Description", "File Name", "Version", "State", "State Changed", "Updated By", "Folder",
        "Document GUID", "File Size (KB)", "ATTR_Project", "ATTR_Originator", "ATTR_Volume", "ATTR_Level",
        "ATTR_Type", "ATTR_Role", "ATTR_Number", "ATTR_Title", "ATTR_Revision", "ATTR_Suitability", "Exported"]
rows = []
for name, ev in events.items():
    ev.sort(key=lambda e: e[0])
    guid = str(uuid.uuid5(uuid.NAMESPACE_URL, "lrhc/" + name))
    size = rnd.randint(300, 4000) if ev[0][2]["type"] != "M3" else rnd.randint(20000, 90000)
    p = c = 0
    for n, (when, suit, r) in enumerate(ev, 1):
        if suit.startswith("S"):
            p += 1
            rev = f"P{p:02d}"
        else:
            c += 1
            rev = f"C{c:02d}"
        if when > EXPORT_AT:
            continue
        published = not suit.startswith("S")
        size = int(size * rnd.uniform(1.02, 1.25))
        rows.append({
            "Name": name, "Description": r["title"], "File Name": f"{name}.{EXT.get(r['type'], 'pdf')}",
            "Version": n, "State": "Published" if published else "Shared",
            "State Changed": when.strftime("%d/%m/%Y %H:%M"), "Updated By": rnd.choice(PEOPLE[r["originator"]]),
            "Folder": f"pw:\\\\LRHC\\{'04 Published' if published else '02 Shared'}\\{r['originator']}\\{r['type']}",
            "Document GUID": guid, "File Size (KB)": size,
            "ATTR_Project": r["project"], "ATTR_Originator": r["originator"], "ATTR_Volume": r["volume"],
            "ATTR_Level": r["spatial_breakdown"], "ATTR_Type": r["type"], "ATTR_Role": r["discipline"],
            "ATTR_Number": r["number"], "ATTR_Title": r["title"], "ATTR_Revision": rev, "ATTR_Suitability": suit,
            "Exported": EXPORT_AT.strftime("%d/%m/%Y %H:%M"),
        })

rows.sort(key=lambda x: (x["Name"], x["Version"]))
path = OUT / "projectwise_export_2027-05-01.csv"
with open(path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)
print(f"{len(rows)} versions of {len({r['Name'] for r in rows})} containers written to {path.relative_to(ROOT.parent)}")
