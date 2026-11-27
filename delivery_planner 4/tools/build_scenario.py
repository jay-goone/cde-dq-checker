"""Build the perfect scenario files: programme (baseline and update, .xer and .csv) and the MIDP.

Run from the repo root:  python delivery_planner/tools/build_scenario.py
"""
import csv, sys
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scenario as S
from scheduler import schedule

DATA = HERE.parent / "data"
PROG = DATA / "programme"
PROG.mkdir(parents=True, exist_ok=True)

schedule(S.ACTS, S.CALS, S.START)
BY = {a["code"]: a for a in S.ACTS}


def stage_of(wbs):
    top = wbs.split(".")[0]
    return top if top.isdigit() else ""


def dt(d, end):
    return f"{d.isoformat()} {'17:00' if end else '08:00'}" if d else ""


def a_start(a):
    return dt(a["es"], a["type"] == "TT_FinMile")


def a_finish(a):
    return dt(a["ef"], a["type"] != "TT_Mile")


def progress(a, data_date):
    """Perfect progress: everything happened exactly as planned up to the data date."""
    cal = S.CALS[a["cal"]]
    if data_date is None or a["es"] >= data_date:
        return "TK_NotStart", None, None, a["dur"]
    if a["ef"] < data_date:
        return "TK_Complete", a["es"], a["ef"], 0
    remain = cal.count(cal.prev_work(data_date - timedelta(days=1)), a["ef"])
    return "TK_Active", a["es"], None, remain


CSTR = {"SNET": "CS_MSOA", "FON": "CS_MEO"}
TYPE_LABEL = {"TT_Task": "Task", "TT_Mile": "Start milestone", "TT_FinMile": "Finish milestone"}
STATUS_LABEL = {"TK_NotStart": "Not started", "TK_Active": "In progress", "TK_Complete": "Completed"}


def rows_for(data_date):
    out = []
    for a in S.ACTS:
        st, ast, aen, rem = progress(a, data_date)
        pct = 100 if st == "TK_Complete" else (round(100 * (a["dur"] - rem) / a["dur"]) if a["dur"] else 0)
        act_start = dt(ast, a["type"] == "TT_FinMile") if ast else ""
        act_end = dt(aen, a["type"] != "TT_Mile") if aen else ""
        out.append(dict(a=a, status=st, act_start=act_start, act_end=act_end, remain=rem, pct=pct,
                        start=act_start or a_start(a), finish=act_end or a_finish(a)))
    return out


# ------------------------------------------------------------------ XER
def xer_table(name, fields, rows):
    lines = [f"%T\t{name}", "%F\t" + "\t".join(fields)]
    for r in rows:
        lines.append("%R\t" + "\t".join(str(r.get(f, "")) for f in fields))
    return lines


def clndr_data(cal):
    days = []
    for p6day in range(1, 8):                    # P6: 1 = Sunday
        py = (p6day - 2) % 7                     # Python: 0 = Monday
        if py in cal.workdays:
            days.append(f"(0||{p6day}()((0||0(s|08:00|f|12:00)())(0||1(s|13:00|f|17:00)())))")
        else:
            days.append(f"(0||{p6day}()())")
    exc = "".join(f"(0||{i}(d|{(h - date(1899, 12, 30)).days})())" for i, h in enumerate(sorted(cal.holidays)))
    return ("(0||CalendarData()((0||DaysOfWeek()(" + "".join(days) + "))(0||VIEW(ShowTotal|Y)())"
            "(0||Exceptions()(" + exc + "))))")


def write_xer(path, proj_id, short_name, name, data_date, rows):
    wbs_ids = {code: 100 + i for i, code in enumerate(S.WBS)}
    task_ids = {a["code"]: 1000 + i for i, a in enumerate(S.ACTS)}
    out = ["ERMHDR\t19.12\t" + data_date.isoformat() + "\tProject\tadmin\tLRHC Planner\tdbxDatabaseNoName\tProject Management\tGBP"]
    out += xer_table("PROJECT", ["proj_id", "proj_short_name", "clndr_id", "plan_start_date", "plan_end_date",
                                 "scd_end_date", "last_recalc_date", "def_complete_pct_type", "def_duration_type"],
                     [dict(proj_id=proj_id, proj_short_name=short_name, clndr_id=1, plan_start_date=dt(S.START, False),
                           plan_end_date=a_finish(BY["M-203-REC"]), scd_end_date=a_finish(BY["M-203-REC"]),
                           last_recalc_date=f"{data_date.isoformat()} 00:00", def_complete_pct_type="CP_Drtn",
                           def_duration_type="DT_FixedDrtn")])
    out += xer_table("CALENDAR", ["clndr_id", "default_flag", "clndr_name", "proj_id", "base_clndr_id", "clndr_type",
                                  "day_hr_cnt", "week_hr_cnt", "month_hr_cnt", "year_hr_cnt", "clndr_data"],
                     [dict(clndr_id=c.id, default_flag="Y" if c.id == 1 else "N", clndr_name=c.name, proj_id="",
                           base_clndr_id="", clndr_type="CA_Base", day_hr_cnt=8, week_hr_cnt=8 * len(c.workdays),
                           month_hr_cnt=172, year_hr_cnt=2000, clndr_data=clndr_data(c)) for c in S.CALS.values()])
    wbs_rows = []
    for i, (code, (wname, parent)) in enumerate(S.WBS.items()):
        wbs_rows.append(dict(wbs_id=wbs_ids[code], proj_id=proj_id, obs_id=1, seq_num=i * 10,
                             proj_node_flag="Y" if parent is None else "N", sum_data_flag="N", status_code="WS_Open",
                             wbs_short_name=code.split(".")[-1], wbs_name=wname,
                             parent_wbs_id=wbs_ids[parent] if parent else ""))
    out += xer_table("PROJWBS", ["wbs_id", "proj_id", "obs_id", "seq_num", "proj_node_flag", "sum_data_flag",
                                 "status_code", "wbs_short_name", "wbs_name", "parent_wbs_id"], wbs_rows)
    task_rows = []
    for r in rows:
        a = r["a"]
        hrs = 8
        cstr = a.get("cstr")
        task_rows.append(dict(
            task_id=task_ids[a["code"]], proj_id=proj_id, wbs_id=wbs_ids[a["wbs"]], clndr_id=S.CALS[a["cal"]].id,
            phys_complete_pct=r["pct"], complete_pct_type="CP_Drtn", task_type=a["type"], duration_type="DT_FixedDrtn",
            status_code=r["status"], task_code=a["code"], task_name=a["name"], total_float_hr_cnt=a["tf"] * hrs,
            remain_drtn_hr_cnt=r["remain"] * hrs, target_drtn_hr_cnt=a["dur"] * hrs,
            cstr_date=dt(cstr[1], cstr[0] == "FON") if cstr else "", cstr_type=CSTR[cstr[0]] if cstr else "",
            act_start_date=r["act_start"], act_end_date=r["act_end"],
            early_start_date="" if r["status"] == "TK_Complete" else a_start(a),
            early_end_date="" if r["status"] == "TK_Complete" else a_finish(a),
            late_start_date=dt(a["ls"], a["type"] == "TT_FinMile"), late_end_date=dt(a["lf"], a["type"] != "TT_Mile"),
            restart_date="" if r["status"] == "TK_Complete" else (
                f"{S.CALS[a['cal']].next_work(data_date).isoformat()} 08:00" if r["status"] == "TK_Active" else a_start(a)),
            reend_date="" if r["status"] == "TK_Complete" else a_finish(a),
            target_start_date=a_start(a), target_end_date=a_finish(a), priority_type="PT_Normal"))
    out += xer_table("TASK", ["task_id", "proj_id", "wbs_id", "clndr_id", "phys_complete_pct", "complete_pct_type",
                              "task_type", "duration_type", "status_code", "task_code", "task_name",
                              "total_float_hr_cnt", "remain_drtn_hr_cnt", "target_drtn_hr_cnt", "cstr_date",
                              "act_start_date", "act_end_date", "late_start_date", "late_end_date",
                              "early_start_date", "early_end_date", "restart_date", "reend_date",
                              "target_start_date", "target_end_date", "cstr_type", "priority_type"], task_rows)
    pred_rows, n = [], 1
    for a in S.ACTS:
        for p, rel, lag in a["preds"]:
            pred_rows.append(dict(task_pred_id=n, task_id=task_ids[a["code"]], pred_task_id=task_ids[p],
                                  proj_id=proj_id, pred_proj_id=proj_id, pred_type="PR_" + rel, lag_hr_cnt=lag * 8))
            n += 1
    out += xer_table("TASKPRED", ["task_pred_id", "task_id", "pred_task_id", "proj_id", "pred_proj_id",
                                  "pred_type", "lag_hr_cnt"], pred_rows)
    out.append("%E")
    path.write_text("\r\n".join(out) + "\r\n", encoding="cp1252")


# ------------------------------------------------------------------ CSV (same content, planner-friendly)
ACT_COLS = ["project", "data_date", "activity_id", "activity_name", "wbs_code", "wbs_name", "stage", "activity_type",
            "calendar", "original_duration_d", "remaining_duration_d", "status", "pct_complete", "planned_start",
            "planned_finish", "start", "finish", "actual_start", "actual_finish", "late_start", "late_finish",
            "total_float_d", "constraint_type", "constraint_date"]


def write_csv(stem, short_name, data_date, rows):
    with open(PROG / f"{stem}_activities.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ACT_COLS)
        w.writeheader()
        for r in rows:
            a = r["a"]
            cstr = a.get("cstr")
            w.writerow(dict(project=short_name, data_date=f"{data_date.isoformat()} 00:00", activity_id=a["code"],
                            activity_name=a["name"], wbs_code="LRHC." + a["wbs"], wbs_name=S.WBS[a["wbs"]][0],
                            stage=stage_of(a["wbs"]), activity_type=TYPE_LABEL[a["type"]], calendar=S.CALS[a["cal"]].name,
                            original_duration_d=a["dur"], remaining_duration_d=r["remain"],
                            status=STATUS_LABEL[r["status"]], pct_complete=r["pct"], planned_start=a_start(a),
                            planned_finish=a_finish(a), start=r["start"], finish=r["finish"],
                            actual_start=r["act_start"], actual_finish=r["act_end"],
                            late_start=dt(a["ls"], a["type"] == "TT_FinMile"),
                            late_finish=dt(a["lf"], a["type"] != "TT_Mile"), total_float_d=a["tf"],
                            constraint_type=CSTR[cstr[0]] if cstr else "",
                            constraint_date=dt(cstr[1], cstr[0] == "FON") if cstr else ""))
    with open(PROG / f"{stem}_relationships.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["predecessor", "successor", "type", "lag_d"])
        for a in S.ACTS:
            for p, rel, lag in a["preds"]:
                w.writerow([p, a["code"], rel, lag])


for stem, pid, short, name, dd in [
        ("LRHC_programme_baseline", 1, "LRHC-BL01", "LRHC baseline", S.START),
        ("LRHC_programme_update_2027-05-01", 2, "LRHC-UP06", "LRHC update 6 (data date 1 May 2027)", S.DATA_DATE)]:
    rows = rows_for(None if stem.endswith("baseline") else dd)
    write_xer(PROG / f"{stem}.xer", pid, short, name, dd, rows)
    write_csv(stem, short, dd, rows)

# ------------------------------------------------------------------ MIDP
MIDP_COLS = ["midp_id", "container_name", "title", "project", "originator", "volume", "spatial_breakdown", "type",
             "discipline", "number", "linked_p6_activity", "stage", "required_suitability", "exchange"]
with open(DATA / "midp.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=MIDP_COLS)
    w.writeheader()
    for i, (key, org, vol, lvl, typ, role, num, title, stage, suit, ie) in enumerate(S.MIDP, 1):
        name = "-".join(["LRHC", org, vol, lvl, typ, role, num])
        w.writerow(dict(midp_id=f"MIDP-{i:03d}", container_name=name, title=title, project="LRHC", originator=org,
                        volume=vol, spatial_breakdown=lvl, type=typ, discipline=role, number=num,
                        linked_p6_activity=S.ISSUE[key], stage=stage, required_suitability=suit, exchange=ie))

n_rel = sum(len(a["preds"]) for a in S.ACTS)
print(f"{len(S.ACTS)} activities, {len(S.WBS)} WBS nodes, {n_rel} relationships, {len(S.MIDP)} MIDP rows")
