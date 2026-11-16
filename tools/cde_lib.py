"""Plumbing for cde_checks.ipynb: loading files, looking up values, writing reports.

The rules themselves live in the notebook. This module turns the IFC, COBie
and register into plain Python data so each rule stays short.
"""
import re
from datetime import date
from pathlib import Path

import pandas as pd

PLACEHOLDERS = {"n/a", "tbc", "-", "unknown"}


# ============================================================ reference data
class Project:
    """Everything the checker reads, in one object."""

    def __init__(self, base, check_date):
        base = Path(base)
        self.base = base
        self.check_date = check_date
        read = lambda p: pd.read_csv(base / p, dtype=str, keep_default_na=False)
        self.dd = read("data_dictionary.csv")
        self.rules = read("rules.csv")
        self.asset_types = read("reference/asset_types.csv")
        self.spaces_ref = read("reference/space_schedule.csv")
        self.codes = read("reference/code_lists.csv")
        self.midp = read("reference/midp.csv")
        self.ifc = None
        self.cobie = None
        self.register = None
        self.load_errors = {}

    def code_list(self, name):
        return self.codes[self.codes.list_name == name].code.tolist()

    def code_value(self, name, code):
        row = self.codes[(self.codes.list_name == name) & (self.codes.code == code)]
        return float(row.value.iloc[0]) if len(row) else None

    # ---- asset type lookups
    def type_row_for_pr(self, pr_code):
        rows = self.asset_types[self.asset_types.uniclass_pr == pr_code]
        return rows.iloc[0] if len(rows) else None

    def is_safety_critical(self, asset_code, pr_code=None):
        row = self.type_row_for_pr(pr_code) if pr_code else None
        if row is not None:
            return row.safety_critical == "Y"
        rows = self.asset_types[self.asset_types.asset_code == asset_code]
        return bool((rows.safety_critical == "Y").any())  # unknown variant: assume critical


def code_of(name):
    m = re.match(r"^([A-Z]{2,3})-", str(name))
    return m.group(1) if m else ""


def class_code(value):
    """'Pr_65_54_95_88 : Thermostatic mixing valves' -> 'Pr_65_54_95_88'."""
    return str(value).split(" : ")[0].strip()


def is_empty(value, data_type="text"):
    v = "" if value is None else str(value).strip()
    if v == "" or v.lower() in PLACEHOLDERS:
        return True
    return v == "0" and data_type in ("text", "code")


def applies(dd_row, asset_code):
    return dd_row.applies_to == "ALL" or asset_code in dd_row.applies_to.split("|")


# ============================================================ COBie + register
def load_cobie(path):
    return pd.read_excel(path, sheet_name=None, dtype=str, keep_default_na=False)


def load_register(path):
    return pd.read_csv(path, dtype=str, keep_default_na=False)


COBIE_NAME_COL = {"Component": "Name", "Type": "Name", "Space": "Name", "Floor": "Name", "Contact": "Email",
                  "System": "Name", "Job": "TypeName", "Document": "Name"}


def cobie_values(p, dd_row):
    """Yield (object_name, asset_code, value) for one data dictionary row, from COBie or the register."""
    table, field = dd_row.table, dd_row.field
    if table == "Register":
        for _, r in p.register.iterrows():
            yield r.container_name, "", r.get(field, "")
        return
    m = re.match(r"^Attribute \((\w+)\)$", table)
    sheet = m.group(1) if m else table
    if p.cobie is None or sheet not in p.cobie:
        return
    df = p.cobie[sheet]
    name_col = COBIE_NAME_COL.get(sheet, "Name")
    if m:
        att = p.cobie.get("Attribute", pd.DataFrame(columns=["SheetName", "RowName", "Name", "Value"]))
        att = att[(att.SheetName == sheet) & (att.Name == field)]
        lookup = dict(zip(att.RowName, att.Value))
    seen = set()
    for _, r in df.iterrows():
        obj = r[name_col]
        if sheet == "System" and dd_row.field != "ComponentNames":
            if obj in seen:
                continue
            seen.add(obj)
        code = code_of(obj) if sheet in ("Component", "Type", "Job") else ""
        if code and not applies(dd_row, code):
            continue
        if sheet == "System" and dd_row.field == "ComponentNames":
            code = code_of(r.ComponentNames)
            if not applies(dd_row, code):
                continue
        value = lookup.get(obj, "") if m else r.get(field, "")
        yield obj, code, value


# ============================================================ IFC: plain model
# Every reader returns the same shape:
# {"schema": "IFC4", "storeys": [names], "assets": [...], "spaces": [...], "types": {name: {...}}, "systems": [...]}

def load_ifc(path, asset_entities):
    """Use ifcopenshell when it's installed; otherwise the small text reader below."""
    try:
        import ifcopenshell  # noqa: F401
        return load_ifc_ifcopenshell(path, asset_entities), "ifcopenshell"
    except ImportError:
        return load_ifc_text(path, asset_entities), "fallback text reader"


def load_ifc_ifcopenshell(path, asset_entities):
    import ifcopenshell
    import ifcopenshell.util.element as ue

    f = ifcopenshell.open(str(path))

    def codes(obj):
        out = []
        for rel in getattr(obj, "HasAssociations", None) or []:
            if rel.is_a("IfcRelAssociatesClassification") and rel.RelatingClassification.is_a("IfcClassificationReference"):
                out.append(rel.RelatingClassification.Identification)
        return out

    def psets(obj):
        raw = ue.get_psets(obj) or {}
        return {k: {pk: pv for pk, pv in v.items() if pk != "id"} for k, v in raw.items()}

    model = {"schema": f.schema, "storeys": [s.Name for s in f.by_type("IfcBuildingStorey")],
             "assets": [], "spaces": [], "types": {}, "systems": []}
    for t in f.by_type("IfcTypeObject"):
        model["types"][t.Name] = {"name": t.Name, "entity": t.is_a(), "predefined": getattr(t, "PredefinedType", None),
                                  "element_type": getattr(t, "ElementType", None), "class_codes": codes(t),
                                  "psets": psets(t)}
    for sp in f.by_type("IfcSpace"):
        storey = next((r.RelatingObject.Name for r in sp.Decomposes or [] if r.RelatingObject.is_a("IfcBuildingStorey")), None)
        model["spaces"].append({"name": sp.Name, "longname": sp.LongName, "storey": storey,
                                "class_codes": codes(sp), "psets": psets(sp)})
    seen = set()
    for entity in asset_entities:
        for el in f.by_type(entity):
            if el.id() in seen:
                continue
            seen.add(el.id())
            t = ue.get_type(el)
            containers = [r.RelatingStructure for r in el.ContainedInStructure or []]
            containers += [r.RelatingStructure for r in getattr(el, "ReferencedInStructures", None) or []]
            systems = [r.RelatingGroup.Name for r in el.HasAssignments or []
                       if r.is_a("IfcRelAssignsToGroup") and r.RelatingGroup.is_a("IfcSystem")]
            model["assets"].append({
                "name": el.Name, "guid": el.GlobalId, "entity": el.is_a(), "description": el.Description,
                "predefined": getattr(el, "PredefinedType", None), "object_type": el.ObjectType,
                "type_name": t.Name if t else None,
                "spaces": [c.Name for c in containers if c.is_a("IfcSpace")],
                "in_storey": any(c.is_a("IfcBuildingStorey") for c in containers),
                "class_codes": codes(el) + (codes(t) if t else []), "psets": psets(el), "systems": systems})
    for s in f.by_type("IfcSystem"):
        members = [o.Name for r in s.IsGroupedBy or [] for o in r.RelatedObjects]
        model["systems"].append({"name": s.Name, "class_codes": codes(s), "members": members})
    return model


def _split(s):
    out, depth, cur, q, i = [], 0, "", False, 0
    while i < len(s):
        ch = s[i]
        if q:
            cur += ch
            if ch == "'":
                if i + 1 < len(s) and s[i + 1] == "'":
                    cur += "'"
                    i += 1
                else:
                    q = False
        elif ch == "'":
            q, cur = True, cur + ch
        elif ch == "(":
            depth, cur = depth + 1, cur + ch
        elif ch == ")":
            depth, cur = depth - 1, cur + ch
        elif ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
        i += 1
    out.append(cur)
    return [x.strip() for x in out]


def _val(tok):
    """Turn one STEP token into a Python value."""
    if tok in ("$", "*"):
        return None
    if tok.startswith("'"):
        return tok[1:-1].replace("''", "'")
    if tok.startswith("#"):
        return ("ref", int(tok[1:]))
    if tok.startswith("."):
        return tok.strip(".")
    if tok.startswith("("):
        inner = tok[1:-1]
        return [_val(x) for x in _split(inner)] if inner else []
    m = re.match(r"^([A-Z0-9]+)\((.*)\)$", tok)
    if m:
        return _val(m.group(2))
    try:
        return float(tok) if "." in tok or "E" in tok else int(tok)
    except ValueError:
        return tok


def load_ifc_text(path, asset_entities):
    """Minimal STEP reader for simple IFC4 files. Good enough for the sample; use ifcopenshell for real models."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    schema = re.search(r"FILE_SCHEMA\(\('([^']+)'\)\)", text)
    E = {}
    for m in re.finditer(r"^#(\d+)=([A-Z0-9]+)\((.*)\);\s*$", text, re.M):
        E[int(m.group(1))] = (m.group(2), [_val(t) for t in _split(m.group(3))])
    deref = lambda v: E[v[1]] if isinstance(v, tuple) and v[0] == "ref" else None
    ids = lambda lst: [x[1] for x in lst or [] if isinstance(x, tuple)]

    def pset_dict(pid):
        ent, a = E[pid]
        if ent == "IFCPROPERTYSET":
            return a[2], {E[r][1][0]: E[r][1][2] for r in ids(a[4])}
        if ent == "IFCELEMENTQUANTITY":
            return a[2], {E[r][1][0]: E[r][1][3] for r in ids(a[5])}
        return None, {}

    psets, codes, type_of, contained, referenced, systems_of, storey_of = {}, {}, {}, {}, {}, {}, {}
    for n, (ent, a) in E.items():
        if ent == "IFCRELDEFINESBYPROPERTIES":
            name, props = pset_dict(a[5][1])
            for o in ids(a[4]):
                psets.setdefault(o, {}).setdefault(name, {}).update(props)
        elif ent == "IFCRELASSOCIATESCLASSIFICATION":
            ref = deref(a[5])
            for o in ids(a[4]):
                codes.setdefault(o, []).append(ref[1][1])
        elif ent == "IFCRELDEFINESBYTYPE":
            for o in ids(a[4]):
                type_of[o] = a[5][1]
        elif ent == "IFCRELCONTAINEDINSPATIALSTRUCTURE":
            for o in ids(a[4]):
                contained.setdefault(o, []).append(a[5][1])
        elif ent == "IFCRELREFERENCEDINSPATIALSTRUCTURE":
            for o in ids(a[4]):
                referenced.setdefault(o, []).append(a[5][1])
        elif ent == "IFCRELASSIGNSTOGROUP":
            for o in ids(a[4]):
                systems_of.setdefault(o, []).append(a[6][1])
        elif ent == "IFCRELAGGREGATES" and E[a[4][1]][0] == "IFCBUILDINGSTOREY":
            for o in ids(a[5]):
                storey_of[o] = a[4][1]

    model = {"schema": schema.group(1) if schema else None, "assets": [], "spaces": [], "types": {}, "systems": [],
             "storeys": [a[2] for ent, a in E.values() if ent == "IFCBUILDINGSTOREY"]}
    type_ent = {}
    for n, (ent, a) in E.items():
        if ent.endswith("TYPE") and ent.startswith("IFC") and len(a) >= 10 and isinstance(a[0], str) and len(a[0]) == 22:
            tp = {}
            for pid in ids(a[5]):
                name, props = pset_dict(pid)
                tp.setdefault(name, {}).update(props)
            type_ent[n] = {"name": a[2], "entity": ent, "predefined": a[9], "element_type": a[8],
                           "class_codes": codes.get(n, []), "psets": tp}
            model["types"][a[2]] = type_ent[n]
    wanted = {e.upper() for e in asset_entities}
    for n, (ent, a) in E.items():
        if ent == "IFCSPACE":
            st = storey_of.get(n)
            model["spaces"].append({"name": a[2], "longname": a[7], "storey": E[st][1][2] if st else None,
                                    "class_codes": codes.get(n, []), "psets": psets.get(n, {})})
        elif ent in wanted:
            t = type_ent.get(type_of.get(n))
            merged = {k: dict(v) for k, v in (t["psets"] if t else {}).items()}
            for k, v in psets.get(n, {}).items():
                merged.setdefault(k, {}).update(v)
            conts = contained.get(n, []) + referenced.get(n, [])
            model["assets"].append({
                "name": a[2], "guid": a[0], "entity": ent, "description": a[3],
                "predefined": a[8] if ent != "IFCDOOR" else a[10], "object_type": a[4],
                "type_name": t["name"] if t else None,
                "spaces": [E[c][1][2] for c in conts if E[c][0] == "IFCSPACE"],
                "in_storey": any(E[c][0] == "IFCBUILDINGSTOREY" for c in conts),
                "class_codes": codes.get(n, []) + (t["class_codes"] if t else []), "psets": merged,
                "systems": [E[s][1][2] for s in systems_of.get(n, [])]})
        elif ent == "IFCDISTRIBUTIONSYSTEM" or ent == "IFCSYSTEM":
            members = [E[o][1][2] for rel in E.values() if rel[0] == "IFCRELASSIGNSTOGROUP" and rel[1][6][1] == n
                       for o in ids(rel[1][4])]
            model["systems"].append({"name": a[2], "class_codes": codes.get(n, []), "members": members})
    return model


def ifc_field(obj, source, kind):
    """Read one data dictionary 'ifc_source' from a plain IFC object. None = can't read it from IFC."""
    if source in ("IfcElement.Name", "IfcSpace.Name", "IfcTypeObject.Name", "IfcBuildingStorey.Name",
                  "IfcDistributionSystem.Name"):
        return obj.get("name")
    if source == "IfcElement.Description":
        return obj.get("description")
    if source == "IfcSpace.LongName":
        return obj.get("longname")
    if source == "IfcElement.GlobalId":
        return obj.get("guid")
    if source.startswith("IfcRelDefinesByType"):
        return obj.get("type_name")
    if source.startswith("IfcRelAggregates to IfcBuildingStorey"):
        return obj.get("storey")
    if source.startswith("IfcClassificationReference"):
        cc = [c for c in obj.get("class_codes", []) if re.match(r"^(Pr|SL|Ss)_", str(c))]
        return cc[0] if cc else ""
    m = re.match(r"^((?:Pset|LRHC|Qto)_\w+)\.(\w+)$", source)
    if m:
        v = obj.get("psets", {}).get(m.group(1), {}).get(m.group(2))
        return "" if v is None else v
    return None


def ifc_objects(p, entity):
    m = p.ifc
    if entity == "Component":
        return m["assets"]
    if entity == "Type":
        return list(m["types"].values())
    if entity == "Space":
        return m["spaces"]
    if entity == "Floor":
        return [{"name": s} for s in m["storeys"]]
    if entity == "System":
        return m["systems"]
    return []


def ifc_values(p, dd_row):
    """Yield (object_name, asset_code, value) for one data dictionary row, from the IFC."""
    if p.ifc is None or dd_row.ifc_source.startswith("n/a"):
        return
    for obj in ifc_objects(p, dd_row.entity):
        code = code_of(obj["name"]) if dd_row.entity in ("Component", "Type") else ""
        if code and not applies(dd_row, code):
            continue
        v = ifc_field(obj, dd_row.ifc_source, dd_row.entity)
        if v is None:
            return
        yield obj["name"], code, v


# ============================================================ value checks
def parse_date(v):
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})(T\d{2}:\d{2}:\d{2})?$", str(v).strip())
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def to_number(v):
    try:
        return float(str(v).strip())
    except ValueError:
        return None


TYPE_CHECKS = {
    "date": lambda v: parse_date(v) is not None,
    "decimal": lambda v: to_number(v) is not None,
    "integer": lambda v: to_number(v) is not None and float(v) == int(float(v)),
    "boolean": lambda v: str(v) in ("Y", "N"),
    "email": lambda v: re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", str(v)) is not None,
    "guid": lambda v: re.match(r"^[0-9A-Za-z_$]{22}$", str(v)) is not None,
}


def same(a, b, data_type):
    if data_type == "date":
        return parse_date(str(a)[:10]) == parse_date(str(b)[:10])
    if data_type in ("decimal", "integer"):
        x, y = to_number(a), to_number(b)
        return x is not None and y is not None and abs(x - y) < 1e-6
    if data_type == "code":
        return class_code(a) == class_code(b)
    return str(a).strip() == str(b).strip()


# ============================================================ reports
def write_excel(path, sheets):
    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        for name, df in sheets.items():
            df.to_excel(xw, sheet_name=name[:31], index=False)
            ws = xw.sheets[name[:31]]
            for col in ws.columns:
                width = max(len(str(c.value or "")) for c in col[:200])
                ws.column_dimensions[col[0].column_letter].width = min(max(10, width + 2), 70)
            ws.freeze_panes = "A2"


def write_html(path, title, intro_rows, sheets):
    css = ("body{font-family:Arial,sans-serif;margin:24px;color:#222}table{border-collapse:collapse;margin:8px 0 24px;"
           "font-size:13px}th,td{border:1px solid #ccc;padding:4px 8px;text-align:left;vertical-align:top}"
           "th{background:#f2f2f2}.fail{background:#fde2e1}.warn{background:#fff4d6}.flag{background:#e3ecff}"
           ".box{border:2px solid #333;padding:10px 14px;display:inline-block;margin-bottom:16px}")
    parts = [f"<html><head><meta charset='utf-8'><title>{title}</title><style>{css}</style></head><body>",
             f"<h1>{title}</h1><div class='box'>" + "<br>".join(intro_rows) + "</div>"]
    for name, df in sheets.items():
        html = df.to_html(index=False, escape=True)
        for s in ("fail", "warn", "flag"):
            html = html.replace(f"<td>{s}</td>", f"<td class='{s}'>{s}</td>")
        parts.append(f"<h2>{name}</h2>{html}")
    parts.append("</body></html>")
    Path(path).write_text("".join(parts), encoding="utf-8")
