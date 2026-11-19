"""Compare two clause extractions and show which checking rules each change touches.

Usage: python compare_clauses.py old.csv new.csv <repo_folder> [report.md]
"""
import csv
import json
import re
import sys
from pathlib import Path

old_f, new_f, repo = sys.argv[1], sys.argv[2], Path(sys.argv[3])
report = Path(sys.argv[4]) if len(sys.argv) > 4 else None

load = lambda p: {r["clause_id"]: r for r in csv.DictReader(open(p, newline=""))}
old, new = load(old_f), load(new_f)
rules = list(csv.DictReader(open(repo / "rules.csv", newline="")))
dd = list(csv.DictReader(open(repo / "data_dictionary.csv", newline="")))


def users(clause):
    base = clause.split("/")[0]
    r = [x["rule_id"] for x in rules if base in x["eir_clause"].split(";")]
    d = [x["dd_id"] for x in dd if base in x["eir_clause"].split(";")]
    return r, d


lines = [f"# Clause changes: {Path(old_f).name} → {Path(new_f).name}", ""]
added = sorted(set(new) - set(old))
removed = sorted(set(old) - set(new))
changed = sorted(k for k in set(old) & set(new) if old[k]["fields"] != new[k]["fields"])
lines.append(f"**{len(changed)} changed · {len(added)} added · {len(removed)} removed** (of {len(new)} records)\n")

for k in changed:
    o, n = json.loads(old[k]["fields"]), json.loads(new[k]["fields"])
    r, d = users(k)
    lines.append(f"## {k} (changed) · {new[k]['section']}")
    for field in n:
        if o.get(field) != n.get(field):
            lines.append(f"- **{field}**\n  - was: {o.get(field, '')}\n  - now: {n[field]}")
    lines.append(f"- **Rules to review:** {', '.join(r) or 'none'} · **Data dictionary rows:** {', '.join(d) or 'none'}\n")
for k in added:
    r, d = users(k)
    lines.append(f"## {k} (added) · {new[k]['section']}\n- {new[k]['fields']}\n- **Needs a rule?** Existing rules citing it: {', '.join(r) or 'none'}\n")
for k in removed:
    r, d = users(k)
    lines.append(f"## {k} (removed)\n- **Rules that cite it and must change:** {', '.join(r) or 'none'} · data dictionary: {', '.join(d) or 'none'}\n")

text = "\n".join(lines)
print(text)
if report:
    report.write_text(text)
