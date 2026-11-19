"""Read the EIR Word document back into machine-readable data.

Every table row whose first cell is a clause ID (AIR-07, NAM-01, SEC-02, ...) becomes one record.
Rows in an information requirement table (under an "IR-xx" heading) become records keyed IR-xx/<component>.
Headings tell us which section each record came from.

Usage: python docx_to_clauses.py EIR.docx clauses.csv
"""
import csv
import json
import re
import sys

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

CLAUSE = re.compile(r"^((PUR|FMT|CLS|LOC|AIR|NAM|STA|MID|ACC|SEC|INT|GEO|PRC|REF|CHK|TND|KPI|BEN|CON)-\d{2}|OIR-[A-Z]{3}-\d{2}|IR-\d{2}\.[A-Z]{1,2}\.\d{2})$")
IR_HEAD = re.compile(r"^(IR-\d{2})\s+(.*)$")


def blocks(doc):
    """Paragraphs and tables in document order."""
    for child in doc.element.body.iterchildren():
        if child.tag.endswith("}p"):
            yield Paragraph(child, doc)
        elif child.tag.endswith("}tbl"):
            yield Table(child, doc)


def main(src, dst):
    doc = Document(src)
    section, ir, ir_meta, records = "", None, {}, []
    for b in blocks(doc):
        if isinstance(b, Paragraph):
            text = b.text.strip()
            if b.style.name.startswith("Heading"):
                m = IR_HEAD.match(text)
                if m:
                    ir, ir_meta = m.group(1), {"title": m.group(2)}
                else:
                    section, ir = text, None
            elif ir and text.startswith("Requirement owner:"):
                for line in text.split("\n"):
                    k, _, v = line.partition(":")
                    ir_meta[k.strip()] = v.strip()
            continue
        rows = [[c.text.strip() for c in r.cells] for r in b.rows]
        header, body = rows[0], rows[1:]
        for r in body:
            if CLAUSE.match(r[0]):
                fields = dict(zip(header[1:], r[1:]))
                if ir and r[0].startswith(ir + "."):
                    fields.update(ir_meta)
                records.append({"clause_id": r[0], "section": section, "fields": json.dumps(fields, ensure_ascii=False)})
            elif ir and header[0] == "Component":  # P02 layout (no atomic IDs)
                fields = dict(zip(header[1:], r[1:]), **ir_meta)
                records.append({"clause_id": f"{ir}/{r[0]}", "section": section, "fields": json.dumps(fields, ensure_ascii=False)})
    with open(dst, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["clause_id", "section", "fields"])
        w.writeheader()
        w.writerows(records)
    ids = [r["clause_id"] for r in records]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    print(f"{len(records)} records from {src} ({sum(not i.startswith('IR-') for i in ids)} clauses, {sum(i.startswith('IR-') for i in ids)} IR items)")
    if dupes:
        print("WARNING: clause IDs used more than once:", ", ".join(dupes))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
