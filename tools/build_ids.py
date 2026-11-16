#!/usr/bin/env python3
"""Build a buildingSMART IDS 1.0 file from the data dictionary.

One source, two outputs: the same data_dictionary.csv drives the rules
and this IDS. Only IFC-side, single-file requirements can go in an IDS.
Cross-file checks (IFC vs COBie), COBie-only fields, the document register
and the programme checks stay in rules.csv.

Usage: python build_ids.py <stage2_folder> <output.ids>
"""
import csv
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

stage2 = Path(sys.argv[1])
out = Path(sys.argv[2])
dd = list(csv.DictReader(open(stage2 / "data_dictionary.csv", newline="")))
types = list(csv.DictReader(open(stage2 / "reference" / "asset_types.csv", newline="")))

PSET_FIELD = re.compile(r"^((?:Pset|LRHC|Qto)_\w+)\.(\w+)$")
IFC_DATATYPE = {"date": "IFCDATE", "decimal": "IFCREAL", "integer": "IFCINTEGER"}
COBIE_ONLY_FORMAT = {"DD-042"}  # COBie holds an email here; IFC holds the company name


def simple(v):
    return f"<ids:simpleValue>{escape(v)}</ids:simpleValue>"


def restriction(base, inner):
    return f'<xs:restriction base="{base}">{inner}</xs:restriction>'


def value_xml(row):
    """Return an <ids:value> for allowed values, a minimum, or a pattern, else ''."""
    if row["dd_id"] in COBIE_ONLY_FORMAT:
        return ""
    numeric = row["data_type"] in ("decimal", "integer")
    base = "xs:double" if row["data_type"] == "decimal" else "xs:integer" if numeric else "xs:string"
    if row["allowed_values"]:
        vals = row["allowed_values"].split("|")
        if len(vals) == 1 and not numeric:
            return f"<ids:value>{simple(vals[0])}</ids:value>"
        inner = "".join(f'<xs:enumeration value="{escape(v)}"/>' for v in vals)
        return f"<ids:value>{restriction(base, inner)}</ids:value>"
    if row["min_value"].startswith(">"):
        return f'<ids:value>{restriction(base, f"<xs:minExclusive value=\"{row["min_value"][1:]}\"/>")}</ids:value>'
    if row["pattern"] and row["entity"] == "Component" and row["dd_id"] == "DD-030":
        # XSD patterns are anchored already, so drop ^ and $
        return f'<ids:value>{restriction(base, f"<xs:pattern value=\"{escape(row["pattern"].strip("^$").replace(r"\d", "[0-9]"))}\"/>")}</ids:value>'
    return ""


def property_xml(row, pset, prop):
    dt = IFC_DATATYPE.get(row["data_type"])
    dt_attr = f' dataType="{dt}"' if dt and pset.startswith("LRHC_") else ""
    return (f'<ids:property{dt_attr} cardinality="required">'
            f"<ids:propertySet>{simple(pset)}</ids:propertySet>"
            f"<ids:baseName>{simple(prop)}</ids:baseName>{value_xml(row)}</ids:property>")


def applies(row, code):
    return row["applies_to"] == "ALL" or code in row["applies_to"].split("|")


specs = []

# ---- One specification per asset code ----
codes = []
for t in types:
    if t["asset_code"] not in codes:
        codes.append(t["asset_code"])

for code in codes:
    variants = [t for t in types if t["asset_code"] == code]
    t0 = variants[0]
    ent = f"<ids:name>{simple(t0['ifc_entity'].upper())}</ids:name>"
    if t0["ifc_predefined_type"]:
        ent += f"<ids:predefinedType>{simple(t0['ifc_predefined_type'])}</ids:predefinedType>"
    applic = f"<ids:entity>{ent}</ids:entity>"
    if t0["ifc_object_type"]:
        applic += (f"<ids:attribute><ids:name>{simple('ObjectType')}</ids:name>"
                   f"<ids:value>{simple(t0['ifc_object_type'])}</ids:value></ids:attribute>")

    pr_codes = "".join(f'<xs:enumeration value="{v["uniclass_pr"]}"/>' for v in variants)
    reqs = [
        # facet order follows the IDS 1.0 schema: partOf, classification, attribute, property
        '<ids:partOf relation="IFCRELCONTAINEDINSPATIALSTRUCTURE" cardinality="required">'
        f"<ids:entity><ids:name>{simple('IFCSPACE')}</ids:name></ids:entity></ids:partOf>",
        '<ids:classification cardinality="required">'
        f"<ids:value>{restriction('xs:string', pr_codes)}</ids:value>"
        f"<ids:system>{simple('Uniclass 2015')}</ids:system></ids:classification>",
        '<ids:attribute cardinality="required">'
        f"<ids:name>{simple('Name')}</ids:name>"
        f"<ids:value>{restriction('xs:string', f'<xs:pattern value=\"{code}-00-[0-9]{{3}}\"/>')}</ids:value>"
        "</ids:attribute>",
        f'<ids:attribute cardinality="required"><ids:name>{simple("Description")}</ids:name></ids:attribute>',
    ]
    clauses = {"LOC-01", "CLS-01", "NAM-03", "AIR-03"}
    for row in dd:
        m = PSET_FIELD.match(row["ifc_source"])
        if not m or row["entity"] not in ("Component", "Type") or not applies(row, code):
            continue
        if row["dd_id"] == "DD-054":
            continue  # emergency flag depends on the variant, handled below
        reqs.append(property_xml(row, *m.groups()))
        clauses.update(row["eir_clause"].split(";"))
    specs.append((f"{code}: {t0['name'].split(' (')[0]}", f"LRHC-{code}", sorted(clauses), applic, reqs))

    # Variant-specific rule: emergency flag must match the Pr code (AIR-25)
    if code == "LF":
        for v in variants:
            row = next(r for r in dd if r["dd_id"] == "DD-054")
            applic_v = applic + ('<ids:classification>'
                                 f"<ids:value>{simple(v['uniclass_pr'])}</ids:value>"
                                 f"<ids:system>{simple('Uniclass 2015')}</ids:system></ids:classification>")
            req = ('<ids:property cardinality="required">'
                   f"<ids:propertySet>{simple('LRHC_AssetData')}</ids:propertySet>"
                   f"<ids:baseName>{simple('EmergencyLighting')}</ids:baseName>"
                   f"<ids:value>{simple(v['emergency'])}</ids:value></ids:property>")
            specs.append((f"LF: {v['name']} has EmergencyLighting = {v['emergency']}",
                          f"LRHC-LF-{v['variant']}", ["AIR-25"], applic_v, [req]))

# ---- Spaces ----
space_reqs = [
    '<ids:partOf relation="IFCRELAGGREGATES" cardinality="required">'
    f"<ids:entity><ids:name>{simple('IFCBUILDINGSTOREY')}</ids:name></ids:entity></ids:partOf>",
    '<ids:classification cardinality="required">'
    f"<ids:value>{restriction('xs:string', '<xs:pattern value=\"SL_[0-9]{2}_[0-9]{2}(_[0-9]{2}){0,2}\"/>')}</ids:value>"
    f"<ids:system>{simple('Uniclass 2015')}</ids:system></ids:classification>",
    '<ids:attribute cardinality="required">'
    f"<ids:name>{simple('Name')}</ids:name>"
    f"<ids:value>{restriction('xs:string', '<xs:pattern value=\"00-[0-9]{3}\"/>')}</ids:value></ids:attribute>",
    f'<ids:attribute cardinality="required"><ids:name>{simple("LongName")}</ids:name></ids:attribute>',
    '<ids:property cardinality="required">'
    f"<ids:propertySet>{simple('LRHC_AssetData')}</ids:propertySet><ids:baseName>{simple('PatientArea')}</ids:baseName>"
    f"<ids:value>{restriction('xs:string', '<xs:enumeration value=\"Y\"/><xs:enumeration value=\"N\"/>')}</ids:value></ids:property>",
    '<ids:property cardinality="required">'
    f"<ids:propertySet>{simple('Qto_SpaceBaseQuantities')}</ids:propertySet><ids:baseName>{simple('NetFloorArea')}</ids:baseName></ids:property>",
]
specs.append(("Spaces", "LRHC-SPACE", ["LOC-02", "CLS-02", "NAM-06", "AIR-27"],
              f"<ids:entity><ids:name>{simple('IFCSPACE')}</ids:name></ids:entity>", space_reqs))

# ---- Write ----
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<ids:ids xmlns:ids="http://standards.buildingsmart.org/IDS" '
         'xmlns:xs="http://www.w3.org/2001/XMLSchema" '
         'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
         'xsi:schemaLocation="http://standards.buildingsmart.org/IDS http://standards.buildingsmart.org/IDS/1.0/ids.xsd">',
         "  <ids:info>",
         "    <ids:title>Larch Road Health Centre - asset information requirements (IFC side)</ids:title>",
         "    <ids:copyright>Fictional exercise</ids:copyright>",
         "    <ids:version>0.1</ids:version>",
         "    <ids:description>Generated from data_dictionary.csv. Covers the IFC-only requirements of EIR LRHC-LRV-ZZ-ZZ-SP-K-000001. Cross-file, COBie-only, register and programme checks are in rules.csv.</ids:description>",
         "    <ids:date>2026-11-16</ids:date>",
         "    <ids:purpose>Asset information model acceptance at IE3</ids:purpose>",
         "  </ids:info>",
         "  <ids:specifications>"]
for name, ident, clauses, applic, reqs in specs:
    lines.append(f'    <ids:specification name="{escape(name)}" ifcVersion="IFC4" identifier="{ident}" '
                 f'description="Related EIR clauses: {" ".join(clauses)}">')
    lines.append(f'      <ids:applicability minOccurs="0" maxOccurs="unbounded">{applic}</ids:applicability>')
    lines.append("      <ids:requirements>")
    lines += [f"        {r}" for r in reqs]
    lines.append("      </ids:requirements>")
    lines.append("    </ids:specification>")
lines += ["  </ids:specifications>", "</ids:ids>", ""]
out.write_text("\n".join(lines), encoding="utf-8")
print(f"{len(specs)} specifications written to {out}")
