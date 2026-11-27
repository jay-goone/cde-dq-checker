"""Run every check, then build the two outputs: the issues list and the delivery status register.

From the delivery_planner folder:   python -m checks.run
"""
from pathlib import Path
import pandas as pd

from .common import CHECKS, ISSUE_COLS, load_inputs
from . import reference, programme, completeness, timeliness, metadata   # noqa: F401  (registers the checks)

HERE = Path(__file__).resolve().parents[1]
PERFECT = dict(
    library=HERE / "data/reference_library.csv",
    midp=HERE / "data/midp.csv",
    baseline=HERE / "data/programme/LRHC_programme_baseline.xer",
    update=HERE / "data/programme/LRHC_programme_update_2027-05-01.xer",
    cde=HERE / "data/cde/projectwise_export_2027-05-01.csv",
)


def run_checks(d):
    rows = []
    for cid, c in CHECKS.items():
        for found in c["fn"](d):
            rows.append(dict(check_id=cid, check_name=c["name"], dimension=c["dimension"],
                             severity=c["severity"], **found))
    return pd.DataFrame(rows, columns=ISSUE_COLS)


def register(d, issues):
    """One row per MIDP row: due dates, what the CDE holds, a delivery status, and the issue count."""
    f = d["facts"].copy()
    dd = d["data_date"]

    def status(r):
        if r.due_baseline != r.due_baseline:
            return "No due date"
        if r.required_reached_on == r.required_reached_on:
            return "Delivered on time" if r.required_reached_on <= r.due_baseline else "Delivered late"
        return "Overdue" if r.due_baseline < dd else "Not yet due"

    f["delivery_status"] = f.apply(status, axis=1)
    f["forecast_slip_days"] = (f.due_forecast.dt.normalize() - f.due_baseline.dt.normalize()).dt.days
    by_row = issues[issues.midp_id != ""].groupby(["midp_id", "severity"]).size().unstack(fill_value=0)
    by_cont = issues[issues.midp_id == ""].groupby(["container", "severity"]).size().unstack(fill_value=0)
    for sev in ("error", "warning"):
        a = f.midp_id.map(by_row[sev] if sev in by_row else {}).fillna(0)
        b = f.container.map(by_cont[sev] if sev in by_cont else {}).fillna(0)
        f[sev + "s"] = (a + b).astype(int)
    f["result"] = f.apply(lambda r: "Errors" if r.errors else ("Warnings" if r.warnings else "Clean"), axis=1)
    cols = ["midp_id", "container", "title", "exchange", "required_suitability", "linked_p6_activity",
            "due_baseline", "due_forecast", "forecast_slip_days", "versions_in_cde", "latest_revision",
            "latest_suitability", "required_reached_on", "delivery_status", "errors", "warnings", "result"]
    return f[cols]


def run(paths=PERFECT):
    d = load_inputs(**paths)
    issues = run_checks(d)
    return d, issues, register(d, issues)


def catalogue():
    return pd.DataFrame([dict(check_id=k, check_name=v["name"], dimension=v["dimension"], severity=v["severity"])
                         for k, v in CHECKS.items()])


if __name__ == "__main__":
    d, issues, reg = run()
    print(f"Data date {d['data_date']:%d %b %Y}: {len(issues)} issues")
    print(reg.delivery_status.value_counts().to_string())
