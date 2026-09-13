#!/usr/bin/env python3
"""
Cost Management - I : Master Solutions Book
Builds a single PDF from module content files.

Usage:  python3 build.py [--only m1] [--out ../CM-Master-Solutions.pdf]
"""
import argparse, importlib, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# ----------------------------------------------------------------------
# small HTML helpers used by every module file
# ----------------------------------------------------------------------

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def rs(v, dp=0):
    """Indian-format a number: 1234567 -> 12,34,567"""
    if v is None or v == "":
        return "&mdash;"
    if isinstance(v, str):
        return v
    neg = v < 0
    v = abs(v)
    # Round to the requested precision FIRST, then split.  Doing it the other
    # way round lets binary floating-point artefacts leak a wrong integer part:
    # 182.9999999999999 would split into whole=182 and frac="00" -> "182.00".
    ip, _, frac = ("%.*f" % (dp, v)).partition(".")
    s = ip
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts + [tail])
    if frac:
        s = s + "." + frac
    return ("(" + s + ")") if neg else s


def prob_head(no, title, tag):
    """no/title/tag may contain intentional HTML entities - do NOT escape."""
    return (f'<div class="prob-head"><span class="prob-no">{no} &nbsp; {title}</span>'
            f'<span class="prob-tag">{tag}</span></div>')


def frac(num, den, col="#0d4b45"):
    """A real stacked fraction, so formulas cannot be misread."""
    return ('<span class="fr">'
            f'<span class="fr-n" style="border-bottom:0.7pt solid {col}">{num}</span>'
            f'<span class="fr-d">{den}</span></span>')


def money(v, dp=None):
    """Smart amount: no decimals when the value is whole, 2 when it is not."""
    if v is None or v == "":
        return "&mdash;"
    if isinstance(v, str):
        return v
    if dp is None:
        dp = 0 if abs(v - round(v)) < 0.005 else 2
    return rs(v, dp)


def question(html):
    return f'<div class="q"><span class="qlab">The question, as printed in your workbook</span>{html}</div>'


def blk(kind, label, html):
    return f'<div class="blk {kind}"><span class="lab">{esc(label)}</span>{html}</div>'


def read(html):
    return blk("read", "Read the question first — what to spot", html)


def method(html):
    return blk("method", "The method for this type — always these steps", html)


def wn(html):
    return blk("wn", "Working notes", html)


def trap(html):
    return blk("trap", "The trap / where marks are lost", html)


def why(html):
    return blk("why", "Why this works", html)


def steps(items):
    return "<ol class='steps'>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def bullets(items):
    return "<ul class='tight'>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def fml(main, small=None):
    s = f'<div class="fml">{main}'
    if small:
        s += f'<span class="small">{small}</span>'
    return s + "</div>"


def calc(lines):
    return '<div class="calc">' + "".join(f"<div>{l}</div>" for l in lines) + "</div>"


def ans(rows, note=None):
    """rows = list of (label, value) ; value already formatted"""
    body = "<table class='mini'>"
    for lab, val in rows:
        body += f"<tr><td>{lab}</td><td class='v'>{val}</td></tr>"
    body += "</table>"
    if note:
        body += f'<div class="small" style="margin-top:1.6mm">{note}</div>'
    return f'<div class="ans"><span class="lab">Final answer</span>{body}</div>'


def table(caption, head, rows, cls="t", headcls="", widths=None):
    """
    head  : list of (label, align) or list of labels
    rows  : list of list of cells; a cell may be a str, or (text, align),
            or dict(t=..., a=..., cls=...)
    A row may also be the string "TOT" marker via rows entry ('__cls__','tot')
    """
    h = f"<table class='{cls}'>"
    if caption:
        h += f"<caption>{caption}</caption>"
    if widths:
        h += "<colgroup>" + "".join(f"<col style='width:{w}'>" for w in widths) + "</colgroup>"
    if head:
        h += f"<thead class='{headcls}'><tr>"
        for c in head:
            if isinstance(c, (tuple, list)):
                lab, al = c[0], c[1]
                extra = c[2] if len(c) > 2 else ""
                h += f"<th class='{al} {extra}'>{lab}</th>"
            else:
                h += f"<th>{c}</th>"
        h += "</tr></thead>"
    h += "<tbody>"
    for r in rows:
        rcls = ""
        cells = r
        if isinstance(r, dict):
            rcls = r.get("cls", "")
            cells = r["cells"]
        h += f"<tr class='{rcls}'>"
        for c in cells:
            if isinstance(c, dict):
                cs = f" colspan='{c['cs']}'" if "cs" in c else ""
                h += (f"<td class='{c.get('a','')} {c.get('cls','')}'{cs}>"
                      f"{c['t']}</td>")
            elif isinstance(c, (tuple, list)):
                h += f"<td class='{c[1]}'>{c[0]}</td>"
            else:
                h += f"<td>{c}</td>"
        h += "</tr>"
    h += "</tbody></table>"
    return h


def src(text):
    """the little red provenance note that sits under a figure inside its cell"""
    return f"<span class='src'>{text}</span>"


# ----------------------------------------------------------------------
# SVG provenance arrow helper
# ----------------------------------------------------------------------

def arrow_panel(width, height, items, caption=None):
    """
    items: list of dicts describing svg primitives:
      {"box":(x,y,w,h,label,fill)}          - a labelled box
      {"arc":(x1,y1,x2,y2,label,bend)}      - curved arrow with label
      {"txt":(x,y,text,size,colour,anchor)}
    """
    s = [f'<div class="dia"><svg width="{width}" height="{height}" '
         f'viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
         'font-family="DejaVu Sans">']
    s.append('<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="3.2" '
             'orient="auto"><path d="M0,0 L0,6.4 L8,3.2 z" fill="#c0392b"/></marker>'
             '<marker id="ab" markerWidth="9" markerHeight="9" refX="7" refY="3.2" '
             'orient="auto"><path d="M0,0 L0,6.4 L8,3.2 z" fill="#10314f"/></marker></defs>')
    for it in items:
        if "box" in it:
            x, y, w, h, label, fill = it["box"]
            stroke = it.get("stroke", "#10314f")
            s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="0.9"/>')
            lines = label.split("|")
            fs = it.get("fs", 8.6)
            ly = y + h / 2 - (len(lines) - 1) * (fs * 0.62)
            for ln in lines:
                s.append(f'<text x="{x+w/2}" y="{ly+fs*0.35}" font-size="{fs}" '
                         f'text-anchor="middle" fill="{it.get("fg","#10314f")}">{ln}</text>')
                ly += fs * 1.24
        if "arc" in it:
            x1, y1, x2, y2, label, bend = it["arc"]
            col = it.get("col", "#c0392b")
            mk = "ar" if col == "#c0392b" else "ab"
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2 - bend
            s.append(f'<path d="M{x1},{y1} Q{cx},{cy} {x2},{y2}" fill="none" '
                     f'stroke="{col}" stroke-width="1.15" marker-end="url(#{mk})"/>')
            if label:
                s.append(f'<text x="{cx}" y="{cy + ((-2) if bend>0 else 8)}" font-size="7.4" '
                         f'text-anchor="middle" fill="{col}">{label}</text>')
        if "line" in it:
            x1, y1, x2, y2 = it["line"]
            col = it.get("col", "#10314f")
            mk = "ab" if col == "#10314f" else "ar"
            s.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{col}" '
                     f'stroke-width="1.05" marker-end="url(#{mk})"/>')
        if "txt" in it:
            x, y, t, size, colour, anchor = it["txt"]
            s.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{colour}" '
                     f'text-anchor="{anchor}">{t}</text>')
    s.append("</svg>")
    if caption:
        s.append(f'<div class="cap">{caption}</div>')
    s.append("</div>")
    return "".join(s)


# ----------------------------------------------------------------------
# page shells
# ----------------------------------------------------------------------

def module_opener(kicker, title, count, intro_html):
    return (f'<div class="modopen"><div class="modopen-band">'
            f'<div class="modopen-kicker">{kicker}</div>'
            f'<div class="modopen-title">{title}</div>'
            f'<span class="modopen-count">{count}</span></div>'
            f'<div class="modopen-body">{intro_html}</div></div>')


def render(body_html, out_pdf):
    css = open(os.path.join(HERE, "style.css")).read()
    html = ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<style>{css}</style></head><body>{body_html}</body></html>")
    tmp = os.path.join(HERE, "_book.html")
    open(tmp, "w").write(html)
    from weasyprint import HTML
    HTML(tmp).write_pdf(out_pdf)
    return out_pdf


# ----------------------------------------------------------------------

MODULES = ["front", "m1", "m2", "m3", "m4", "m5", "m6", "back"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--out", default=os.path.join(HERE, "..", "..",
                                                  "Cost-Management",
                                                  "CM-Master-Solutions.pdf"))
    a = ap.parse_args()
    want = a.only if a.only else MODULES
    parts = []
    for name in want:
        try:
            mod = importlib.import_module(f"content_{name}")
        except ModuleNotFoundError:
            print(f"  .. skip {name} (not written yet)")
            continue
        importlib.reload(mod)
        parts.append(mod.build())
        print(f"  .. {name} ok")
    out = os.path.abspath(a.out)
    render("".join(parts), out)
    from pypdf import PdfReader
    n = len(PdfReader(out).pages)
    print(f"\nWROTE {out}\nPAGES {n}")


if __name__ == "__main__":
    main()
