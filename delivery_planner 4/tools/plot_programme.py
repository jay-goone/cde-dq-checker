"""Summary Gantt of the programme (one bar per WBS package, EIR milestones, data date).

Run from the repo root:  python delivery_planner/tools/plot_programme.py
"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from adapters import p6

SURFACE, INK, INK2, GRID, BAR = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df", "#2a78d6"
src = ROOT / "data/programme/LRHC_programme_update_2027-05-01.xer"
acts = p6.from_xer(src)
tasks = acts[acts.activity_type == "Task"]
wbs = (tasks.groupby("wbs_code").agg(start=("start", "min"), finish=("finish", "max"), n=("activity_id", "size"))
       .sort_values("start"))
w = p6.read_xer_tables(src)["PROJWBS"]
names = dict(zip(w.wbs_id.map(p6._wbs_paths(w)), w.wbs_name))

fig, ax = plt.subplots(figsize=(13, 8.5), dpi=150)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
y = range(len(wbs))
ax.barh(list(y), (wbs.finish - wbs.start).dt.total_seconds() / 86400, left=wbs.start, height=0.55,
        color=BAR, edgecolor=SURFACE, linewidth=2)
labels = [f"{c.split('.', 1)[1]}  {names.get(c, '')}  ({n})" for c, n in zip(wbs.index, wbs.n)]
ax.set_yticks(list(y), labels, fontsize=8.5, color=INK)
ax.invert_yaxis()

ms = acts[acts.activity_id.str.startswith("M-2")]
for k, (_, m) in enumerate(ms.sort_values("finish").iterrows()):
    ax.axvline(m.finish, color=GRID, linewidth=1, zorder=0)
    ax.plot(m.finish, -0.9, marker="D", markersize=8, color=INK, clip_on=False)
    ax.annotate(m.activity_id, (m.finish, -0.9), xytext=(0, 9 + 11 * (k % 2)), textcoords="offset points", ha="center",
                fontsize=7.5, color=INK2, rotation=0, annotation_clip=False)
dd = acts.data_date.iloc[0]
ax.axvline(dd, color=INK2, linewidth=1.5, linestyle=(0, (4, 3)))
ax.annotate("Data date 1 May 2027", (dd, len(wbs) - 0.4), xytext=(4, 0), textcoords="offset points",
            fontsize=8, color=INK2, va="bottom")

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.tick_params(axis="x", colors=INK2, labelsize=8)
ax.tick_params(axis="y", length=0)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.grid(axis="x", color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
ax.set_ylim(len(wbs) - 0.4, -1.6)
fig.suptitle("Larch Road Health Centre: programme summary by WBS package (number of activities)",
             x=0.01, ha="left", fontsize=12, color=INK)
fig.tight_layout()
out = ROOT / "data/programme/LRHC_programme_summary.png"
fig.savefig(out, facecolor=SURFACE)
print("written", out)
