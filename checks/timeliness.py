"""T checks: did the information arrive when the programme said it would?

Due dates come from the linked P6 activity, never from the MIDP:
- baseline due = finish of the activity in the baseline (contractual view)
- forecast due = finish of the activity in the current update (planning view)
'Delivered' means the first version at the required suitability or better (e.g. A4 counts for S4).
"""
import pandas as pd
from .common import check, issue, days

STALE_AFTER = pd.Timedelta(days=1)


def _late(d, f, due, label):
    if due != due or f.versions_in_cde == 0:              # no due date (P01) or nothing in the CDE (C01)
        return None
    if f.required_reached_on == f.required_reached_on:
        if f.required_reached_on > due:
            return (f"reached {f.required_suitability} on {f.required_reached_on:%d %b %Y}, "
                    f"{days(due, f.required_reached_on)} days after the {label} due date {due:%d %b %Y}")
    elif due < d["data_date"]:
        return (f"not at {f.required_suitability} yet; {label} due date was {due:%d %b %Y} "
                f"({days(due, d['data_date'])} days overdue at the data date)")
    return None


@check("T01", "Delivered by the baseline due date", "Timeliness")
def t01(d):
    for f in d["facts"].itertuples(index=False):
        msg = _late(d, f, f.due_baseline, "baseline")
        if msg:
            yield issue("CDE", msg, f.midp_id, f.container, "status_date",
                        "" if f.required_reached_on != f.required_reached_on else f"{f.required_reached_on:%Y-%m-%d}",
                        f"{f.required_suitability} by {f.due_baseline:%Y-%m-%d}")


@check("T02", "Delivered by the current forecast due date", "Timeliness", severity="warning")
def t02(d):
    for f in d["facts"].itertuples(index=False):
        msg = _late(d, f, f.due_forecast, "forecast")
        if msg:
            yield issue("CDE", msg, f.midp_id, f.container, "status_date",
                        "" if f.required_reached_on != f.required_reached_on else f"{f.required_reached_on:%Y-%m-%d}",
                        f"{f.required_suitability} by {f.due_forecast:%Y-%m-%d}")


@check("T03", "Early warning: forecast due date has slipped past the baseline", "Timeliness", severity="warning")
def t03(d):
    for f in d["facts"].itertuples(index=False):
        not_yet = f.required_reached_on != f.required_reached_on and f.due_baseline == f.due_baseline \
            and f.due_baseline >= d["data_date"]
        if not_yet and f.due_forecast == f.due_forecast and f.due_forecast > f.due_baseline:
            yield issue("P6", f"forecast due {f.due_forecast:%d %b %Y}, {days(f.due_baseline, f.due_forecast)} days "
                        f"later than the baseline {f.due_baseline:%d %b %Y}", f.midp_id, f.container,
                        "linked_p6_activity", f"{f.due_forecast:%Y-%m-%d}", f"{f.due_baseline:%Y-%m-%d}")


@check("T04", "CDE export is current at the data date", "Timeliness")
def t04(d):
    for exported in d["cde"]["exported"].dropna().unique():
        exported = pd.Timestamp(exported)
        if abs(exported - d["data_date"]) > STALE_AFTER:
            yield issue("CDE", f"CDE export taken {exported:%d %b %Y %H:%M}; the data date is {d['data_date']:%d %b %Y}",
                        field="exported", found=f"{exported:%Y-%m-%d %H:%M}",
                        expected=f"within 1 day of {d['data_date']:%Y-%m-%d}")
