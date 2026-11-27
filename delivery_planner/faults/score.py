"""Score the checker against the fault catalogue, and build the 'all faults at once' broken dataset.

From the delivery_planner folder:   python -m faults.score
Writes the results to outputs/ and the broken input files to data/broken/.
"""
import copy, tempfile
from pathlib import Path
import pandas as pd

from checks.common import load_inputs
from checks.run import run_checks, register, catalogue
from .catalogue import FAULTS

HERE = Path(__file__).resolve().parents[1]
SRC = dict(
    library=HERE / "data/reference_library.csv",
    midp=HERE / "data/midp.csv",
    baseline=HERE / "data/programme/LRHC_programme_baseline_activities.csv",
    update=HERE / "data/programme/LRHC_programme_update_2027-05-01_activities.csv",
    cde=HERE / "data/cde/projectwise_export_2027-05-01.csv",
)
OUT = HERE / "outputs"


def load_raw():
    read = lambda p, enc="utf-8": pd.read_csv(p, dtype=str, keep_default_na=False, encoding=enc)
    return dict(library=read(SRC["library"]), midp=read(SRC["midp"]), update=read(SRC["update"]),
                cde=read(SRC["cde"], "utf-8-sig"))


def write_raw(raw, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    paths = dict(library=folder / "reference_library.csv", midp=folder / "midp.csv", baseline=SRC["baseline"],
                 update=folder / "programme_update_activities.csv", cde=folder / "projectwise_export.csv")
    raw["library"].to_csv(paths["library"], index=False)
    raw["midp"].to_csv(paths["midp"], index=False)
    raw["update"].to_csv(paths["update"], index=False)
    raw["cde"].to_csv(paths["cde"], index=False, encoding="utf-8-sig")
    return paths


def run_on(raw):
    with tempfile.TemporaryDirectory() as tmp:
        d = load_inputs(**write_raw(raw, tmp))
        issues = run_checks(d)
        return d, issues, register(d, issues)


def score():
    clean = load_raw()
    _, base_issues, _ = run_on(copy.deepcopy(clean))
    assert base_issues.empty, f"perfect data should give no issues, got {len(base_issues)}"
    rows = []
    for f in FAULTS:
        raw = copy.deepcopy(clean)
        f["apply"](raw)
        _, issues, _ = run_on(raw)
        fired = set(issues.check_id)
        on_target = (not f["target"]) or issues[issues.check_id.isin(f["expected"])].container.eq(f["target"]).any()
        missed, extra = f["expected"] - fired, fired - f["expected"]
        rows.append(dict(fault_id=f["fault_id"], fault=f["fault"], target=f["target"],
                         expected=", ".join(sorted(f["expected"])), fired=", ".join(sorted(fired)),
                         caught="yes" if not missed and on_target else "NO",
                         missed=", ".join(sorted(missed)), false_alarms=", ".join(sorted(extra)),
                         issues=len(issues)))
    return pd.DataFrame(rows)


def broken():
    raw = load_raw()
    for f in FAULTS:
        f["apply"](raw)
    write_raw(raw, HERE / "data/broken")
    return run_on(raw)


def main():
    OUT.mkdir(exist_ok=True)
    from checks.run import run
    d, p_issues, p_reg = run()
    scores = score()
    _, b_issues, b_reg = broken()
    p_reg.to_csv(OUT / "perfect_register.csv", index=False)
    p_issues.to_csv(OUT / "perfect_issues.csv", index=False)
    scores.to_csv(OUT / "fault_scores.csv", index=False)
    b_reg.to_csv(OUT / "broken_register.csv", index=False)
    b_issues.to_csv(OUT / "broken_issues.csv", index=False)
    with pd.ExcelWriter(OUT / "delivery_check_report.xlsx") as xl:
        summary = pd.DataFrame([
            ("Data date", f"{d['data_date']:%d %b %Y}"),
            ("Checks", len(catalogue())),
            ("Perfect data: issues", len(p_issues)),
            ("Faults caught", f"{(scores.caught == 'yes').sum()} of {len(scores)}"),
            ("Faults with false alarms", int((scores.false_alarms != '').sum())),
            ("Broken data: issues", len(b_issues)),
            ("Broken data: errors", int((b_issues.severity == 'error').sum())),
            ("Broken data: warnings", int((b_issues.severity == 'warning').sum())),
        ], columns=["measure", "value"])
        summary.to_excel(xl, sheet_name="Summary", index=False)
        b_reg.to_excel(xl, sheet_name="Register (broken)", index=False)
        b_issues.to_excel(xl, sheet_name="Issues (broken)", index=False)
        scores.to_excel(xl, sheet_name="Fault scores", index=False)
        catalogue().to_excel(xl, sheet_name="Checks", index=False)
        p_reg.to_excel(xl, sheet_name="Register (perfect)", index=False)
    print(summary.to_string(index=False))
    if (scores.caught != "yes").any() or (scores.false_alarms != "").any():
        print(scores[(scores.caught != "yes") | (scores.false_alarms != "")].to_string(index=False))


if __name__ == "__main__":
    main()
