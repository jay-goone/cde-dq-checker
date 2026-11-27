"""Shared pieces for every check: loading the inputs, the issue format, and small helpers.

How a check is written:

    @check("C02", "Containers in the CDE but not in the MIDP", "Integrity")
    def c02(d):
        for name in ...:
            yield issue(source="CDE", container=name, message="...")

Each check reads the prepared inputs `d` and yields zero or more issues. The runner adds the
check ID, name, DAMA dimension and severity, so every issue has the same columns.
"""
import re
from pathlib import Path
import pandas as pd
from adapters import p6, cde_projectwise

ISSUE_COLS = ["check_id", "check_name", "dimension", "severity", "source", "midp_id", "container",
              "field", "found", "expected", "message"]
CHECKS = {}          # check ID -> dict(name, dimension, severity, fn), filled by the @check decorator


def check(cid, name, dimension, severity="error"):
    def register(fn):
        CHECKS[cid] = dict(name=name, dimension=dimension, severity=severity, fn=fn)
        return fn
    return register


def issue(source, message, midp_id="", container="", field="", found="", expected=""):
    return dict(source=source, midp_id=midp_id, container=container, field=field,
                found="" if found is None else str(found), expected=str(expected), message=message)


# Which reference-library list each coded field must come from
MIDP_CODE_FIELDS = {"project": "project", "originator": "originator", "volume": "volume",
                    "spatial_breakdown": "level", "type": "type", "discipline": "role", "stage": "stage",
                    "required_suitability": "suitability", "exchange": "exchange"}
CDE_CODE_FIELDS = {"project": "project", "originator": "originator", "volume": "volume", "level": "level",
                   "type": "type", "role": "role", "suitability": "suitability"}
MIDP_NAME_PARTS = ["project", "originator", "volume", "spatial_breakdown", "type", "discipline", "number"]
CDE_NAME_PARTS = ["project", "originator", "volume", "level", "type", "role", "number"]
NUMBER_RE = re.compile(r"\d{6}")


def rank(suitability):
    """Order of suitability codes, so 'at least S4' can be tested. Unknown codes return None."""
    s = str(suitability)
    if re.fullmatch(r"S[0-4]", s):
        return int(s[1])
    if re.fullmatch(r"A[1-7]", s):
        return 5
    if s == "CR":
        return 6
    return None


def _read_programme(path):
    return p6.from_xer(path) if str(path).lower().endswith(".xer") else p6.from_csv(path)


def load_inputs(library, midp, baseline, update, cde):
    """Read the five inputs (file paths) and prepare everything the checks need."""
    d = dict(
        library=pd.read_csv(library, dtype=str, keep_default_na=False),
        midp=pd.read_csv(midp, dtype=str, keep_default_na=False),
        baseline=_read_programme(baseline),
        update=_read_programme(update),
        cde=cde_projectwise.from_csv(cde),
    )
    return prepare(d)


def prepare(d):
    lib = d["library"].copy()
    lib["approved_date"] = pd.to_datetime(lib["approved_date"], errors="coerce")
    d["lib"] = {(r.list_name, r.code): r._asdict() for r in lib.itertuples(index=False)}
    d["data_date"] = d["update"]["data_date"].dropna().iloc[0]
    d["project_start"] = d["baseline"]["planned_start"].min()
    d["base_idx"] = d["baseline"].drop_duplicates("activity_id").set_index("activity_id")
    d["upd_idx"] = d["update"].drop_duplicates("activity_id").set_index("activity_id")
    # exchange -> milestone activity, read from the library notes ("Milestone M-203-S4")
    d["exchange_milestone"] = {}
    for r in lib[lib.list_name == "exchange"].itertuples(index=False):
        m = re.search(r"Milestone (\S+)", r.notes)
        if m:
            d["exchange_milestone"][r.code] = m.group(1)
    d["facts"] = delivery_facts(d)
    return d


def delivery_facts(d):
    """One row per MIDP row: due dates from the programme and what the CDE shows for that container."""
    base, upd, cde = d["base_idx"], d["upd_idx"], d["cde"]
    rows = []
    for r in d["midp"].itertuples(index=False):
        link = r.linked_p6_activity
        due_b = base.planned_finish.get(link) if link in base.index else pd.NaT
        due_f = upd.finish.get(link) if link in upd.index else pd.NaT
        need = rank(r.required_suitability)
        v = cde[cde.container_name == r.container_name]
        reached = pd.NaT
        if need is not None and len(v):
            ok = v[v.suitability.map(lambda s: (rank(s) is not None) and rank(s) >= need)]
            if len(ok):
                reached = ok.status_date.min()
        last = v.sort_values("version").iloc[-1] if len(v) else None
        rows.append(dict(midp_id=r.midp_id, container=r.container_name, title=r.title, exchange=r.exchange,
                         required_suitability=r.required_suitability, linked_p6_activity=link,
                         due_baseline=due_b, due_forecast=due_f, versions_in_cde=len(v),
                         latest_revision="" if last is None else last.revision,
                         latest_suitability="" if last is None else last.suitability,
                         required_reached_on=reached))
    return pd.DataFrame(rows)


def days(a, b):
    """Whole calendar days from a to b (b later is positive)."""
    return int((b.normalize() - a.normalize()).days)
