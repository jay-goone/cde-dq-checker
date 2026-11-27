"""M checks: does each CDE record agree with itself, with the MIDP, and with the rules for revisions?"""
import re
import pandas as pd
from .common import check, issue, CDE_NAME_PARTS


@check("M01", "CDE container name matches its attribute fields", "Consistency")
def m01(d):
    for v in d["cde"].itertuples(index=False):
        joined = "-".join(getattr(v, c) for c in CDE_NAME_PARTS)
        if joined != v.container_name:
            yield issue("CDE", f"version {v.version}: name and attributes disagree", container=v.container_name,
                        field="attributes", found=joined, expected=v.container_name)


@check("M02", "File name matches the container name", "Accuracy")
def m02(d):
    for v in d["cde"].itertuples(index=False):
        stem = v.file_name.rsplit(".", 1)[0]
        if v.file_name and stem != v.container_name:
            yield issue("CDE", f"version {v.version}: file name differs from the container name",
                        container=v.container_name, field="file_name", found=v.file_name, expected=v.container_name + ".*")


@check("M03", "CDE description and title attribute agree", "Accuracy")
def m03(d):
    for v in d["cde"].itertuples(index=False):
        if v.title_cde and v.title_attr and v.title_cde != v.title_attr:
            yield issue("CDE", f"version {v.version}: description and title attribute differ",
                        container=v.container_name, field="title", found=v.title_cde, expected=v.title_attr)


@check("M04", "CDE title matches the MIDP title", "Consistency")
def m04(d):
    titles = d["midp"][d["midp"].title != ""].groupby("container_name").title.first()
    for name, g in d["cde"].groupby("container_name"):
        if name not in titles.index:
            continue                                       # unplanned (C02) or MIDP title blank (C04)
        found = sorted(set(g.title_attr) - {""})
        wrong = [t for t in found if t != titles[name]]
        if wrong:
            yield issue("CDE", "title in the CDE differs from the MIDP", container=name, field="title",
                        found="; ".join(wrong), expected=titles[name])


def _prefix_ok(suitability, revision):
    if re.fullmatch(r"S[0-4]", suitability):
        return revision.startswith("P")
    if re.fullmatch(r"A[1-7]|CR", suitability):
        return revision.startswith("C")
    return True                                            # unknown suitability: R02


@check("M05", "Revision type matches suitability (S → P, A/CR → C)", "Consistency")
def m05(d):
    for v in d["cde"].itertuples(index=False):
        if v.suitability and v.revision and not _prefix_ok(v.suitability, v.revision):
            yield issue("CDE", f"version {v.version}: {v.suitability} with revision {v.revision}",
                        container=v.container_name, field="revision", found=v.revision,
                        expected="P.. for S codes, C.. for A codes and CR")


@check("M06", "Workflow state matches suitability (Shared for S, Published for A/CR)", "Consistency")
def m06(d):
    for v in d["cde"].itertuples(index=False):
        want = "Shared" if re.fullmatch(r"S[0-4]", v.suitability) else (
            "Published" if re.fullmatch(r"A[1-7]|CR", v.suitability) else None)
        if want and v.workflow_state and v.workflow_state != want:
            yield issue("CDE", f"version {v.version}: {v.suitability} should be {want}", container=v.container_name,
                        field="workflow_state", found=v.workflow_state, expected=want)


@check("M07", "Revisions run in order with no gaps, and dates go forward", "Reasonability")
def m07(d):
    c = d["cde"].drop_duplicates(["container_name", "version"])        # duplicates: C06
    for name, g in c.groupby("container_name"):
        g = g.sort_values("version")
        for prefix in ("P", "C"):
            nums = [int(r[1:]) for r in g.revision if re.fullmatch(prefix + r"\d{2}", r)]
            if nums and nums != list(range(1, len(nums) + 1)):
                yield issue("CDE", f"{prefix} revisions run {', '.join(f'{prefix}{n:02d}' for n in nums)}",
                            container=name, field="revision", found=" ".join(f"{prefix}{n:02d}" for n in nums),
                            expected=" ".join(f"{prefix}{n:02d}" for n in range(1, len(nums) + 1)))
        dates = g.status_date.dropna()
        if not dates.is_monotonic_increasing:
            yield issue("CDE", "a later version has an earlier status date", container=name, field="status_date",
                        found="out of order", expected="dates rise with version")


@check("M08", "Status dates fall between project start and the data date", "Reasonability")
def m08(d):
    lo, hi = d["project_start"].normalize(), d["data_date"] + pd.Timedelta(days=1)
    for v in d["cde"].itertuples(index=False):
        if v.status_date == v.status_date and not (lo <= v.status_date <= hi):
            yield issue("CDE", f"version {v.version}: status date {v.status_date:%d %b %Y} is outside "
                        f"{lo:%d %b %Y} to {d['data_date']:%d %b %Y}", container=v.container_name,
                        field="status_date", found=f"{v.status_date:%Y-%m-%d}",
                        expected=f"{lo:%Y-%m-%d} to {d['data_date']:%Y-%m-%d}")
