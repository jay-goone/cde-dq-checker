"""P6 adapter: reads a programme from an .xer file or from the CSV export, and returns the same
standard 'activities' table either way. The checks only ever see the standard table.

Standard columns:
  activity_id, activity_name, wbs_code, stage, activity_type, status,
  planned_start, planned_finish, start, finish, actual_start, actual_finish, total_float_d, data_date
"""
import pandas as pd

COLUMNS = ["activity_id", "activity_name", "wbs_code", "stage", "activity_type", "status",
           "planned_start", "planned_finish", "start", "finish", "actual_start", "actual_finish",
           "total_float_d", "data_date"]
TYPE = {"TT_Task": "Task", "TT_Mile": "Start milestone", "TT_FinMile": "Finish milestone"}
STATUS = {"TK_NotStart": "Not started", "TK_Active": "In progress", "TK_Complete": "Completed"}
DATES = ["planned_start", "planned_finish", "start", "finish", "actual_start", "actual_finish", "data_date"]


def read_xer_tables(path):
    """Split an .xer file into one DataFrame per table (%T name, %F fields, %R rows)."""
    tables, name, fields, rows = {}, None, None, []
    with open(path, encoding="cp1252") as f:
        for line in f:
            parts = line.rstrip("\r\n").split("\t")
            tag = parts[0]
            if tag == "%T":
                if name:
                    tables[name] = pd.DataFrame(rows, columns=fields)
                name, fields, rows = parts[1], None, []
            elif tag == "%F":
                fields = parts[1:]
            elif tag == "%R":
                vals = parts[1:] + [""] * (len(fields) - len(parts) + 1)
                rows.append(vals[:len(fields)])
            elif tag == "%E" and name:
                tables[name] = pd.DataFrame(rows, columns=fields)
                name = None
    return tables


def _wbs_paths(wbs):
    by_id = wbs.set_index("wbs_id")
    paths = {}
    for wid, r in by_id.iterrows():
        parts, cur = [], wid
        while cur:
            row = by_id.loc[cur]
            parts.append(row["wbs_short_name"])
            cur = row["parent_wbs_id"]
        paths[wid] = ".".join(reversed(parts))
    return paths


def from_xer(path):
    t = read_xer_tables(path)
    task, proj = t["TASK"], t["PROJECT"].iloc[0]
    paths = _wbs_paths(t["PROJWBS"])
    df = pd.DataFrame({
        "activity_id": task["task_code"],
        "activity_name": task["task_name"],
        "wbs_code": task["wbs_id"].map(paths),
        "activity_type": task["task_type"].map(TYPE),
        "status": task["status_code"].map(STATUS),
        "planned_start": task["target_start_date"],
        "planned_finish": task["target_end_date"],
        "actual_start": task["act_start_date"],
        "actual_finish": task["act_end_date"],
        "total_float_d": pd.to_numeric(task["total_float_hr_cnt"]) / 8,
        "data_date": proj["last_recalc_date"],
    })
    # P6 'Start' and 'Finish': actual if there is one, otherwise the forecast (remaining early) date
    df["start"] = task["act_start_date"].where(task["act_start_date"] != "", task["early_start_date"])
    df["finish"] = task["act_end_date"].where(task["act_end_date"] != "", task["early_end_date"])
    return _standard(df)


def from_csv(path):
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    df["total_float_d"] = pd.to_numeric(df["total_float_d"])
    return _standard(df)


def _standard(df):
    df = df.copy()
    df["stage"] = df["wbs_code"].str.split(".").str[1].where(lambda s: s.str.isdigit(), "")
    for c in DATES:
        df[c] = pd.to_datetime(df[c].replace("", None), format="%Y-%m-%d %H:%M", errors="coerce")
    df["total_float_d"] = df["total_float_d"].astype(float)
    return df[COLUMNS].sort_values("activity_id").reset_index(drop=True)
