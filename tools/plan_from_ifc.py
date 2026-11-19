"""Draw a plan from the IFC file itself, to check the geometry. Usage: plan_from_ifc.py <ifc> <seeded_errors.csv> <out.png>"""
import re, sys, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.path.insert(0, "tools")
from cde_lib import _split, _val

text = open(sys.argv[1]).read()
E = {int(m[1]): (m[2], [_val(t) for t in _split(m[3])]) for m in re.finditer(r"^#(\d+)=([A-Z0-9]+)\((.*)\);\s*$", text, re.M)}
ref = lambda v: v[1] if isinstance(v, tuple) else None

def world(plc):
    x = y = z = 0.0
    while plc:
        _, (rel, axis) = E[plc]
        loc = E[ref(E[ref(axis)][1][0])][1][0]
        x, y, z = x + loc[0], y + loc[1], z + (loc[2] if len(loc) > 2 else 0)
        plc = ref(rel)
    return x, y, z

def dims(shape):
    rep = E[ref(E[shape][1][2][0])]
    solid = E[ref(rep[1][3][0])]
    prof = E[ref(solid[1][0])][1]
    return prof[3], prof[4], solid[1][3]

bad = {}
for r in csv.DictReader(open(sys.argv[2])):
    for name in re.findall(r"[A-Z]{2,3}-00-\d{3}", r["object"]):
        bad.setdefault(name, []).append(r["error_id"])

fig, ax = plt.subplots(figsize=(16, 6.5))
colours = {"IFCUNITARYEQUIPMENT": "#7f7f7f", "IFCDOOR": "#8c564b", "IFCDAMPER": "#9467bd", "IFCVALVE": "#1f77b4",
           "IFCSANITARYTERMINAL": "#17becf", "IFCCOMMUNICATIONSAPPLIANCE": "#2ca02c", "IFCLIGHTFIXTURE": "#bcbd22"}
for n, (ent, a) in E.items():
    if ent == "IFCSPACE":
        x, y, _ = world(ref(a[5])); w, d, _ = dims(ref(a[6]))
        ax.add_patch(Rectangle((x, y), w, d, fill=False, lw=1.2, ec="#333"))
        ax.text(x + 0.1, y + d - 0.35, f"{a[2]}\n{a[7]}", fontsize=6.5, va="top")
for n, (ent, a) in E.items():
    if ent in colours:
        x, y, z = world(ref(a[5])); w, d, h = dims(ref(a[6]))
        hit = a[2] in bad
        ax.add_patch(Rectangle((x, y), w, d, color="red" if hit else colours[ent], alpha=0.9))
        if hit:
            ax.annotate(f"{a[2]} ({','.join(sorted(set(bad[a[2]])))})", (x + w / 2, y + d / 2), xytext=(0, -14 if y < 10 else 14),
                        textcoords="offset points", fontsize=6.5, color="red", ha="center",
                        arrowprops=dict(arrowstyle="-", color="red", lw=0.6))
ax.set_xlim(-0.5, 37); ax.set_ylim(5.3, 16.6); ax.set_aspect("equal")
ax.set_title("Larch Road Health Centre: plan drawn from the IFC file (red = asset with a seeded error)", fontsize=10)
ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
handles = [Rectangle((0, 0), 1, 1, color=c) for c in colours.values()] + [Rectangle((0, 0), 1, 1, color="red")]
ax.legend(handles, ["AHU", "Fire door", "Fire damper", "TMV", "WC / basin", "Call point", "Light", "Seeded error"],
          loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=8, fontsize=7, frameon=False)
plt.tight_layout(); plt.savefig(sys.argv[3], dpi=150)
print("saved", sys.argv[3])
