"""P checks: is every MIDP row properly linked to the programme?"""
from .common import check, issue


@check("P01", "MIDP row links to an activity that exists in the programme", "Integrity")
def p01(d):
    for r in d["midp"].itertuples(index=False):
        link = r.linked_p6_activity
        if link == "":
            continue                                       # blank: C04
        for name, idx in (("baseline", d["base_idx"]), ("current update", d["upd_idx"])):
            if link not in idx.index:
                yield issue("MIDP", f"activity {link} is not in the {name} programme", r.midp_id,
                            r.container_name, "linked_p6_activity", link, f"an activity in the {name}")


@check("P02", "MIDP stage matches the stage of the linked activity", "Consistency")
def p02(d):
    for r in d["midp"].itertuples(index=False):
        if r.linked_p6_activity in d["base_idx"].index and r.stage:
            act_stage = d["base_idx"].loc[r.linked_p6_activity, "stage"]
            if act_stage != r.stage:
                yield issue("MIDP", f"MIDP says Stage {r.stage}, but {r.linked_p6_activity} sits in Stage {act_stage}",
                            r.midp_id, r.container_name, "stage", r.stage, act_stage)


@check("P03", "Linked activity finishes on or before its exchange milestone", "Reasonability")
def p03(d):
    base = d["base_idx"]
    for r in d["midp"].itertuples(index=False):
        ms = d["exchange_milestone"].get(r.exchange)
        if r.linked_p6_activity not in base.index or ms not in base.index:
            continue
        due, ie = base.loc[r.linked_p6_activity, "planned_finish"], base.loc[ms, "planned_finish"]
        if due > ie:
            yield issue("MIDP", f"due {due:%d %b %Y}, after {r.exchange} ({ms}) on {ie:%d %b %Y}", r.midp_id,
                        r.container_name, "linked_p6_activity", f"{due:%Y-%m-%d}", f"on or before {ie:%Y-%m-%d}")
