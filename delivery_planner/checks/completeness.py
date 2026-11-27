"""C checks: is everything there, once, with every required field filled?"""
from .common import check, issue

MIDP_REQUIRED = ["midp_id", "container_name", "title", "project", "originator", "volume", "spatial_breakdown",
                 "type", "discipline", "number", "linked_p6_activity", "stage", "required_suitability", "exchange"]
CDE_REQUIRED = ["container_name", "file_name", "title_cde", "title_attr", "revision", "suitability",
                "workflow_state", "status_date", "updated_by", "exported"]


@check("C01", "Due deliverables are in the CDE", "Completeness")
def c01(d):
    in_cde = set(d["cde"].container_name)
    for f in d["facts"].itertuples(index=False):
        if f.due_baseline == f.due_baseline and f.due_baseline < d["data_date"] and f.container not in in_cde:
            yield issue("MIDP", f"due {f.due_baseline:%d %b %Y} ({f.exchange}) but not in the CDE", f.midp_id,
                        f.container, found="no versions", expected=f"{f.required_suitability} by {f.due_baseline:%Y-%m-%d}")


@check("C02", "Every container in the CDE is planned in the MIDP", "Integrity")
def c02(d):
    planned = set(d["midp"].container_name)
    for name, g in d["cde"].groupby("container_name"):
        if name not in planned:
            yield issue("CDE", f"{len(g)} version(s) in the CDE but not in the MIDP", container=name,
                        found="not in MIDP", expected="planned in the MIDP")


@check("C03", "No duplicate MIDP rows", "Uniqueness")
def c03(d):
    m = d["midp"]
    for keys, label in ((["container_name", "exchange"], "container and exchange"), (["midp_id"], "MIDP ID")):
        dup = m[m.duplicated(keys, keep="first")]
        for r in dup.itertuples(index=False):
            yield issue("MIDP", f"duplicate {label}", r.midp_id, r.container_name, "+".join(keys),
                        " / ".join(getattr(r, k) for k in keys), "unique")


@check("C04", "Required MIDP fields are filled", "Completeness")
def c04(d):
    for r in d["midp"].itertuples(index=False):
        for col in MIDP_REQUIRED:
            if getattr(r, col) == "":
                yield issue("MIDP", f"{col} is blank", r.midp_id, r.container_name, col, "", "a value")


@check("C05", "Required CDE fields are filled", "Completeness")
def c05(d):
    for v in d["cde"].itertuples(index=False):
        for col in CDE_REQUIRED:
            val = getattr(v, col)
            if val == "" or val != val:                    # blank text or a missing date
                yield issue("CDE", f"version {v.version}: {col} is blank or unreadable", container=v.container_name,
                            field=col, found="", expected="a value")


@check("C06", "No duplicate CDE version records", "Uniqueness")
def c06(d):
    c = d["cde"]
    for v in c[c.duplicated(["container_name", "version"], keep="first")].itertuples(index=False):
        yield issue("CDE", f"version {v.version} appears more than once", container=v.container_name,
                    field="version", found=v.version, expected="one record per version")
