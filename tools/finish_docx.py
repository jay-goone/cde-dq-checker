"""Finish a pandoc-made .docx: A4 landscape, sensible column widths, repeat header rows, footer with container ID.

Usage: python finish_docx.py in.docx out.docx "footer text"
"""
import sys
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, Twips

src, dst, footer = sys.argv[1], sys.argv[2], sys.argv[3]
doc = Document(src)

for s in doc.sections:
    s.orientation = WD_ORIENT.LANDSCAPE
    s.page_width, s.page_height = Mm(297), Mm(210)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(s, side, Mm(17))
    p = s.footer.paragraphs[0]
    p.text = footer
    p.runs[0].font.size = Pt(8)

usable = Mm(297 - 34).twips if hasattr(Mm(1), "twips") else int((297 - 34) / 25.4 * 1440)


def set_width(cell, tw):
    tcPr = cell._tc.get_or_add_tcPr()
    w = tcPr.find(qn("w:tcW"))
    if w is None:
        w = OxmlElement("w:tcW")
        tcPr.insert(0, w)
    w.set(qn("w:w"), str(tw))
    w.set(qn("w:type"), "dxa")


for t in doc.tables:
    ncols = len(t.columns)
    # Each column is at least as wide as its longest single word (so words never break mid-word);
    # the remaining width is shared by typical text length.
    CHAR_TW, PAD_TW = 118, 260
    cols = [[c.text for c in col.cells] for col in t.columns]
    min_w = [max((len(w) for txt in col for w in txt.split()), default=1) * CHAR_TW + PAD_TW for col in cols]
    lens = [sorted(len(txt) for txt in col) for col in cols]
    weights = [max(ls[int(len(ls) * 0.8)], 4) if ls else 4 for ls in lens]
    widths = list(min_w)
    spare = usable - sum(widths)
    if spare > 0:
        total = sum(weights)
        widths = [mw + int(spare * w / total) for mw, w in zip(min_w, weights)]
    else:                                   # too many columns: scale everything down evenly
        widths = [int(usable * mw / sum(min_w)) for mw in min_w]
    widths[-1] += usable - sum(widths)
    tblPr = t._tbl.tblPr
    for tag in ("w:tblW", "w:tblLayout"):
        old = tblPr.find(qn(tag))
        if old is not None:
            tblPr.remove(old)
    tblW = OxmlElement("w:tblW"); tblW.set(qn("w:w"), str(usable)); tblW.set(qn("w:type"), "dxa"); tblPr.append(tblW)
    layout = OxmlElement("w:tblLayout"); layout.set(qn("w:type"), "fixed"); tblPr.append(layout)
    grid = t._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(w))
    for row in t.rows:
        for cell, w in zip(row.cells, widths):
            set_width(cell, w)
    # keep each row on one page
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        if trPr.find(qn("w:cantSplit")) is None:
            cs = OxmlElement("w:cantSplit"); trPr.append(cs)
    # repeat the header row on each page
    trPr = t.rows[0]._tr.get_or_add_trPr()
    if trPr.find(qn("w:tblHeader")) is None:
        h = OxmlElement("w:tblHeader"); h.set(qn("w:val"), "true"); trPr.append(h)

doc.save(dst)
print(f"{len(doc.tables)} tables formatted -> {dst}")
