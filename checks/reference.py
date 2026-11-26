"""R checks: does every code come from the client's reference library, approved, and in time?"""
from .common import check, issue, MIDP_CODE_FIELDS, CDE_CODE_FIELDS, MIDP_NAME_PARTS, NUMBER_RE


def _code_problem(lib, lst, value):
    hit = lib.get((lst, value))
    if hit is None:
        return f"{value} is not in the {lst} list"
    if hit["status"] != "approved":
        return f"{value} is {hit['status']} in the {lst} list, not approved"
    return None


@check("R01", "MIDP codes are in the reference library and approved", "Validity")
def r01(d):
    for r in d["midp"].itertuples(index=False):
        for col, lst in MIDP_CODE_FIELDS.items():
            v = getattr(r, col)
            if v == "":
                continue                                   # blanks are reported by C04
            problem = _code_problem(d["lib"], lst, v)
            if problem:
                yield issue("MIDP", problem, r.midp_id, r.container_name, col, v, f"approved {lst} code")
        if r.number and not NUMBER_RE.fullmatch(r.number):
            yield issue("MIDP", f"number {r.number} is not 6 digits", r.midp_id, r.container_name,
                        "number", r.number, "6 digits")


@check("R02", "CDE attribute codes are in the reference library and approved", "Validity")
def r02(d):
    for v in d["cde"].itertuples(index=False):
        for col, lst in CDE_CODE_FIELDS.items():
            val = getattr(v, col)
            if val == "":
                continue
            problem = _code_problem(d["lib"], lst, val)
            if problem:
                yield issue("CDE", f"version {v.version}: {problem}", container=v.container_name, field=col,
                            found=val, expected=f"approved {lst} code")
        if v.number and not NUMBER_RE.fullmatch(v.number):
            yield issue("CDE", f"version {v.version}: number {v.number} is not 6 digits",
                        container=v.container_name, field="number", found=v.number, expected="6 digits")


@check("R03", "Codes used in the CDE only after the client approved them", "Validity")
def r03(d):
    for v in d["cde"].itertuples(index=False):
        if v.status_date != v.status_date:                 # NaT: reported by C05
            continue
        for col, lst in CDE_CODE_FIELDS.items():
            hit = d["lib"].get((lst, getattr(v, col)))
            if hit is None or hit["approved_date"] != hit["approved_date"]:
                continue                                   # unknown or unapproved code: R02
            if v.status_date < hit["approved_date"]:
                yield issue("CDE", f"version {v.version} used {lst} {getattr(v, col)} on "
                            f"{v.status_date:%d %b %Y}, before it was approved on {hit['approved_date']:%d %b %Y}",
                            container=v.container_name, field=col, found=f"{v.status_date:%Y-%m-%d}",
                            expected=f"on or after {hit['approved_date']:%Y-%m-%d}")


@check("R04", "MIDP container name matches its own fields", "Consistency")
def r04(d):
    for r in d["midp"].itertuples(index=False):
        joined = "-".join(getattr(r, c) for c in MIDP_NAME_PARTS)
        if joined != r.container_name:
            yield issue("MIDP", "container name does not match the MIDP's own fields", r.midp_id,
                        r.container_name, "container_name", r.container_name, joined)
