# -*- coding: utf-8 -*-
"""MODULE 6 - STANDARD COSTING AND VARIANCE ANALYSIS  (17 problems)

Every variance in this module is COMPUTED, never typed by hand.  The engines
below (material_engine, labour_engine, ...) do the arithmetic once and the
per-problem functions only present it, so all seventeen answers are guaranteed
internally consistent and every reconciliation closes exactly.
"""
from build import (esc, rs, money, frac, prob_head, question, read, method, wn,
                   trap, why, steps, bullets, fml, calc, ans, table, src,
                   arrow_panel, module_opener)

R = "&#8377;"
NAVY, RED, GREEN, GREY = "#10314f", "#c0392b", "#1e7a37", "#777"


# ----------------------------------------------------------------------
# formatting helpers
# ----------------------------------------------------------------------
def vt(v, dp=None):
    """A variance, tagged (F) favourable or (A) adverse."""
    if v is None:
        return "&mdash;"
    if abs(v) < 0.005:
        return "<b>Nil</b>"
    cls, tag = ("vf", "F") if v > 0 else ("va", "A")
    return f"<span class='{cls}'>{money(abs(v), dp)} ({tag})</span>"


def num(v, dp=None):
    """A plain quantity or amount, negatives in brackets."""
    if v is None:
        return "&mdash;"
    if isinstance(v, str):
        return v
    if abs(v) < 0.005:
        return "&mdash;"
    s = money(abs(v), dp)
    return f"({s})" if v < 0 else s


def q(v, dp=None):
    """A quantity - shown to 2 dp only when it is not whole."""
    if v is None:
        return "&mdash;"
    if abs(v - round(v)) < 0.005:
        return money(round(v))
    return money(v, 2 if dp is None else dp)


def stmt(caption, cols, rows, note=None, widths=None, first="Particulars"):
    head = [(first, "")] + [(c, "r") for c in cols]
    body = []
    for r in rows:
        cls = r[2] if len(r) > 2 else ""
        body.append({"cls": cls, "cells": [r[0]] + [(v, "r") for v in r[1]]})
    t = table(caption, head, body, widths=widths)
    if note:
        t += f"<div class='small'>{note}</div>"
    return t


def vbox(title, formula, rows, total, headers, widths=None, note=None):
    """One variance worked out in its own little table, formula in the caption."""
    cap = f"{title} &nbsp;=&nbsp; {formula}"
    head = [(h[0], h[1]) for h in headers]
    body = list(rows)
    # the label spans every column except the amount, so long variance names
    # do not wrap into a three-line cell
    body.append({"cls": "tot",
                 "cells": [{"t": f"<b>{title}</b>", "cs": len(headers) - 1},
                           (f"<b>{vt(total)}</b>", "r")]})
    t = table(cap, head, body, widths=widths)
    if note:
        t += f"<div class='small'>{note}</div>"
    return t


# ----------------------------------------------------------------------
# variance trees
# ----------------------------------------------------------------------
def vtree(root, left, right, children=None, h=None, caption=""):
    """
    root/left/right : (line1, line2) tuples - name and formula
    children        : list of (name, formula_line1, formula_line2) hung under RIGHT
    """
    kids = children or []
    height = h or (112 if not kids else 186)
    items = [
        {"box": (135, 6, 230, 32, root[0] + "|" + root[1], "#10314f"),
         "fg": "#ffffff", "fs": 8.4},
        {"box": (14, 68, 212, 32, left[0] + "|" + left[1], "#eaf1f8"), "fs": 8.2},
        {"box": (274, 68, 212, 32, right[0] + "|" + right[1], "#eaf1f8"), "fs": 8.2},
        {"line": (250, 38, 122, 66), "col": NAVY},
        {"line": (250, 38, 378, 66), "col": NAVY},
    ]
    if kids:
        n = len(kids)
        span, gap = 500 - 210, 6
        w = (span - gap * (n - 1)) / n
        x0 = 205
        for i, k in enumerate(kids):
            cx = x0 + i * (w + gap)
            items.append({"box": (cx, 130, w, 46,
                                  k[0] + "|" + k[1] + ("|" + k[2] if len(k) > 2 else ""),
                                  "#eaf6ee"), "stroke": GREEN, "fs": 7.8})
            items.append({"line": (380, 100, cx + w / 2, 128), "col": NAVY})
    return arrow_panel(500, height, items, caption)


def tree_material():
    return vtree(("MATERIAL COST VARIANCE", "SC &minus; AC &nbsp;=&nbsp; (SQ &times; SP) &minus; (AQ &times; AP)"),
                 ("MATERIAL PRICE VARIANCE", "AQ &times; (SP &minus; AP)"),
                 ("MATERIAL USAGE VARIANCE", "SP &times; (SQ &minus; AQ)"),
                 [("MIX VARIANCE", "SP &times;", "(RSQ &minus; AQ)"),
                  ("YIELD VARIANCE", "SP &times;", "(SQ &minus; RSQ)")],
                 caption="Material variances. Price is a purchasing responsibility; usage is a "
                         "production responsibility. Usage then splits into mix and yield.")


def tree_labour():
    return vtree(("LABOUR COST VARIANCE", "SC &minus; AC &nbsp;=&nbsp; (SH &times; SR) &minus; (AH &times; AR)"),
                 ("LABOUR RATE VARIANCE", "AH &times; (SR &minus; AR)"),
                 ("LABOUR EFFICIENCY VARIANCE", "SR &times; (SH &minus; AH)"),
                 [("MIX / GANG", "SR &times;", "(RSH &minus; AH)"),
                  ("YIELD", "SR &times;", "(SH &minus; RSH<sub>worked</sub>)"),
                  ("IDLE TIME", "Idle hours &times; SR", "(always adverse)")],
                 caption="Labour variances. Note that labour has one extra branch that material does "
                         "not have &mdash; idle time, because labour is paid for hours it does not work.")


def tree_vo():
    return vtree(("VARIABLE OVERHEAD COST VARIANCE",
                  "SC &minus; AC &nbsp;=&nbsp; (SH &times; SR) &minus; Actual VOH"),
                 ("VO EXPENDITURE VARIANCE", "(AH &times; SR) &minus; Actual VOH"),
                 ("VO EFFICIENCY VARIANCE", "SR &times; (SH &minus; AH)"),
                 caption="Variable overhead has only two branches, because variable overhead is "
                         "assumed to move with hours.")


def tree_fo():
    return vtree(("FIXED OVERHEAD COST VARIANCE",
                  "SC &minus; AC &nbsp;=&nbsp; (SH &times; SR) &minus; Actual FOH"),
                 ("FO EXPENDITURE VARIANCE", "Budgeted FOH &minus; Actual FOH"),
                 ("FO VOLUME VARIANCE", "SR &times; (SH &minus; BH)"),
                 [("CALENDAR", "SR &times;", "(RSH &minus; BH)"),
                  ("CAPACITY", "SR &times;", "(AH &minus; RSH)"),
                  ("EFFICIENCY", "SR &times;", "(SH &minus; AH)")],
                 caption="Fixed overhead variances. The volume variance exists only because fixed "
                         "overhead is absorbed per hour although the total does not change with hours.")


def tree_sales():
    return vtree(("TOTAL SALES VALUE VARIANCE", "Actual sales value &minus; Budgeted sales value"),
                 ("SALES PRICE VARIANCE", "AQ &times; (AP &minus; SP)"),
                 ("SALES VOLUME VARIANCE", "SP &times; (AQ &minus; BQ)"),
                 [("SALES MIX VARIANCE", "SP &times;", "(AQ &minus; RBQ)"),
                  ("SALES QUANTITY VARIANCE", "SP &times;", "(RBQ &minus; BQ)")],
                 caption="Sales variances. Note the subtraction is reversed &mdash; ACTUAL minus "
                         "BUDGET &mdash; because more revenue is favourable, whereas more cost is not.")


# ----------------------------------------------------------------------
def opener():
    intro = f"""
<h2 class="sec">What Module 6 is really about</h2>
<p>A standard cost is what a thing <i>ought</i> to cost. Actual cost is what it <i>did</i> cost. The
difference is a <b>variance</b>, and this module is entirely about splitting that one difference into
its causes, so that each cause can be put in front of the manager responsible for it.</p>

<div class="blk read"><span class="lab">The two conventions that must be right before anything else</span>
{fml("For COSTS: &nbsp; Variance &nbsp;=&nbsp; STANDARD &nbsp;&minus;&nbsp; ACTUAL",
     "A positive answer means actual cost was LOWER than standard, which is good &mdash; mark it "
     "<b>(F) favourable</b>. A negative answer means actual cost was higher &mdash; mark it "
     "<b>(A) adverse</b>.")}
{fml("For SALES and PROFIT: &nbsp; Variance &nbsp;=&nbsp; ACTUAL &nbsp;&minus;&nbsp; BUDGET",
     "The subtraction reverses, because more revenue is good whereas more cost is not. Q16 and Q17 "
     "use this convention; Q1 to Q15 use the one above.")}
<p><b>Every single figure you write must carry an (F) or an (A).</b> An untagged variance is
meaningless &mdash; and in an examination it earns no marks, because the sign is the answer.</p>
</div>

<h2 class="sec" style="margin-top:6mm">The seven symbols &mdash; learn these and the formulas write themselves</h2>
{table(None, [("Symbol", "c"), ("Stands for", ""), ("How to compute it", "")],
 [["<b>SQ</b> / <b>SH</b>", "Standard Quantity / Hours <b>for the actual output</b>",
   "Standard per unit &times; <b>actual</b> units produced. <b>Never</b> the standard for the "
   "standard output &mdash; this is the single most common error in the module."],
  ["<b>SP</b> / <b>SR</b>", "Standard Price / Rate", "Given"],
  ["<b>AQ</b> / <b>AH</b>", "Actual Quantity / Hours", "Given. For labour, hours <b>paid</b>."],
  ["<b>AP</b> / <b>AR</b>", "Actual Price / Rate",
   "Given, or actual cost &divide; actual quantity"],
  ["<b>RSQ</b> / <b>RSH</b>", "Revised Standard Quantity / Hours",
   "<b>Total actual input</b> re-split in the <b>standard proportion</b>. It answers: "
   "&ldquo;if we had used this much input but in the right mix, how much of each would it be?&rdquo;"],
  ["<b>BH</b>", "Budgeted Hours", "Only for fixed overhead &mdash; the hours in the original budget"],
  ["<b>RBQ</b>", "Revised Budgeted Quantity",
   "Sales version of RSQ &mdash; total actual quantity sold, re-split in the budgeted mix"]],
 headcls="lite", widths=["13%", "30%", "57%"])}
<p><b>RSQ is the one that has to be understood rather than memorised</b>, because it is what makes mix
and yield separable:</p>
{fml("RSQ for a material &nbsp;=&nbsp; Total actual quantity of ALL materials &nbsp;&times;&nbsp; "
     + frac("Standard quantity of THIS material", "Total standard quantity of ALL materials"),
     "The total of the RSQ column always equals the total of the AQ column. If it does not, "
     "you have made an arithmetic error - and that is a free self-check on every mix problem.")}

<h2 class="sec" style="margin-top:6mm">The variance trees</h2>
<p>Each tree is read the same way: the box at the top is the total, and it always equals the sum of
the boxes below it. Those identities are the <b>reconciliation</b> that every question in this module
asks for.</p>
<h3 class="sub">Material variances &mdash; Q1 to Q7</h3>
{tree_material()}
<h3 class="sub">Labour variances &mdash; Q8 to Q10</h3>
{tree_labour()}
<h3 class="sub">Variable overhead variances &mdash; Q11 to Q13</h3>
{tree_vo()}
<h3 class="sub">Fixed overhead variances &mdash; Q14 and Q15</h3>
{tree_fo()}
<h3 class="sub">Sales variances &mdash; Q16 and Q17</h3>
{tree_sales()}

<h2 class="sec" style="margin-top:6mm">The reconciliations you must be able to write from memory</h2>
{table(None, [("Family", ""), ("Reconciliation", ""), ("And then", "")],
 [["<b>Material</b>", "MCV = MPV + MUV", "MUV = MMV + MYV"],
  ["<b>Labour</b>", "LCV = LRV + LEV", "LEV = LMV + LYV + LITV"],
  ["<b>Variable overhead</b>", "VOCV = VOEXPV + VOEFFV", "&mdash;"],
  ["<b>Fixed overhead</b>", "FOCV = FOEXPV + FOVV",
   "FOVV = Calendar + Capacity + Efficiency"],
  ["<b>Sales value</b>", "Total = Price + Volume", "Volume = Mix + Quantity"],
  ["<b>Sales margin</b>", "Total = Margin price + Margin volume",
   "Margin volume = Margin mix + Margin quantity"]],
 headcls="lite", widths=["21%", "38%", "41%"])}
<p class="small"><b>Use the reconciliation as your checking tool, not as an afterthought.</b> Compute
the total variance first and the branches second; if the branches do not add to the total you have made
an error, and you will know before the examiner does.</p>

<h2 class="sec" style="margin-top:6mm">The five problem types</h2>
{table(None, [("Type", ""), ("How to recognise it", ""), ("Problems", "c")],
 [["<b>Material variances</b>",
   "Materials in a mix, with a standard loss or a standard yield.", "<b>1&ndash;7</b>"],
  ["<b>Labour variances</b>",
   "A &ldquo;gang&rdquo; of skilled / semi-skilled / unskilled workers, usually with idle time.",
   "<b>8&ndash;10</b>"],
  ["<b>Variable overhead variances</b>",
   "Budgeted and actual variable overhead, with a standard time per unit.", "<b>11&ndash;13</b>"],
  ["<b>Fixed overhead variances</b>",
   "Budgeted and actual fixed overhead; working days or man-hours per day.", "<b>14, 15</b>"],
  ["<b>Sales variances</b>",
   "Budgeted and actual quantities and selling prices by product.", "<b>16, 17</b>"]],
 headcls="lite", widths=["24%", "60%", "16%"])}

<div class="blk trap"><span class="lab">The trap / where marks are lost</span>
{bullets([
 '<b>Using the standard quantity for the STANDARD output instead of for the ACTUAL output.</b> If the '
 'standard is 1,100 kg of input for 1,000 kg of output and actual output was 20,000 kg, then SQ is '
 '22,000 kg &mdash; twenty times the standard. Everything downstream is wrong if this is wrong.',
 '<b>Forgetting the (F) / (A) tag, or getting it backwards.</b> Remember: for costs, a positive '
 'answer is favourable because standard exceeded actual.',
 '<b>Rounding RSQ too early.</b> RSQ is often a recurring decimal. Carry at least two decimals, or '
 'the mix and yield variances will not add back to the usage variance. This is the reason some '
 'published solutions to Q1 show ' + R + '26,365 instead of the correct ' + R + '26,363.64.',
 '<b>Confusing hours PAID with hours WORKED in labour problems.</b> AH is hours <b>paid</b>. Hours '
 'worked = hours paid &minus; idle hours, and it is used only for the yield variance and to show that '
 'the idle-time variance closes the reconciliation.',
 '<b>Treating an idle-time variance as favourable.</b> It is <b>always adverse</b> &mdash; the '
 'company paid for hours in which nothing was produced. Even when the arithmetic yields a positive '
 'number, the situation is adverse; say so.',
 '<b>Keeping the cost convention for sales variances.</b> Q16 and Q17 reverse it to actual minus '
 'budget. A favourable sales price variance means you charged MORE than standard.'])}
</div>
"""
    return module_opener("Module 6", "Standard Costing and Variance Analysis",
                         "17 problems &middot; workbook pages 79&ndash;84", intro)



# ======================================================================
# MATERIAL VARIANCE ENGINE  -  used by Q1 to Q7
# ======================================================================
def material_engine(mats, std_out, act_out):
    """
    mats    : list of dicts {n, sq, sp, aq, ap}
              sq = standard quantity for the STANDARD output std_out
    std_out : standard output produced by that standard input
    act_out : actual output achieved
    Returns a dict of every computed figure.  Nothing is rounded internally.
    """
    k = act_out / std_out                      # scale-up factor for actual output
    tot_sq_std = sum(m["sq"] for m in mats)
    tot_aq = sum(m["aq"] for m in mats)
    rows = []
    for m in mats:
        sq = m["sq"] * k                       # standard qty FOR ACTUAL OUTPUT
        rsq = tot_aq * (m["sq"] / tot_sq_std)  # actual input re-split in standard mix
        rows.append(dict(
            n=m["n"], sq_std=m["sq"], sq=sq, sp=m["sp"], aq=m["aq"], ap=m["ap"], rsq=rsq,
            sc=sq * m["sp"], ac=m["aq"] * m["ap"],
            mpv=m["aq"] * (m["sp"] - m["ap"]),
            muv=m["sp"] * (sq - m["aq"]),
            mmv=m["sp"] * (rsq - m["aq"]),
            myv=m["sp"] * (sq - rsq)))
    d = dict(rows=rows, k=k, tot_sq_std=tot_sq_std, tot_aq=tot_aq,
             tot_sq=sum(r["sq"] for r in rows), tot_rsq=sum(r["rsq"] for r in rows),
             sc=sum(r["sc"] for r in rows), ac=sum(r["ac"] for r in rows),
             mpv=sum(r["mpv"] for r in rows), muv=sum(r["muv"] for r in rows),
             mmv=sum(r["mmv"] for r in rows), myv=sum(r["myv"] for r in rows),
             std_out=std_out, act_out=act_out)
    d["mcv"] = d["sc"] - d["ac"]
    # standard cost per unit of OUTPUT, for the alternative yield check
    d["std_cost_per_out"] = sum(m["sq"] * m["sp"] for m in mats) / std_out
    d["std_yield_of_actual_input"] = d["tot_aq"] * std_out / tot_sq_std
    return d


def material_tables(d, cur=None, qdp=None):
    """Render the standard set of six tables from an engine result."""
    cur = cur or R
    rr = d["rows"]

    basic = table("Basic Calculation",
      [("Material", ""), ("SQ<br/><span class='small'>standard mix</span>", "r"),
       ("SQ for actual output", "r"), ("SP", "r"), ("AQ", "r"), ("AP", "r"),
       ("RSQ for actual input", "r")],
      [[f"<b>{r['n']}</b>", q(r["sq_std"]), q(r["sq"], qdp), money(r["sp"]),
        q(r["aq"]), money(r["ap"]), q(r["rsq"], 2)] for r in rr]
      + [{"cls": "tot",
          "cells": ["<b>Total</b>", f"<b>{q(d['tot_sq_std'])}</b>", f"<b>{q(d['tot_sq'], qdp)}</b>",
                    "", f"<b>{q(d['tot_aq'])}</b>", "", f"<b>{q(d['tot_rsq'], 2)}</b>"]}],
      headcls="lite", widths=["13%", "12%", "16%", "10%", "13%", "10%", "16%"])
    basic += (f"<div class='small'><b>Two checks before going on.</b> "
              f"The RSQ column totals {q(d['tot_rsq'], 2)}, which equals the AQ total of "
              f"{q(d['tot_aq'])} &mdash; it must, because RSQ is the same total input in a different "
              f"mix. And SQ for actual output = standard quantity &times; "
              f"{money(d['k'], 2 if abs(d['k'] - round(d['k'])) > 0.005 else 0)}, the ratio of actual "
              f"output {q(d['act_out'])} to standard output {q(d['std_out'])}.</div>")

    mcv = table(f"1. &nbsp;MATERIAL COST VARIANCE &nbsp;=&nbsp; SC &minus; AC &nbsp;=&nbsp; "
                f"(SQ &times; SP) &minus; (AQ &times; AP)",
      [("Material", ""), ("SQ for actual output", "r"), ("SP", "r"),
       ("SC = SQ &times; SP", "r"), ("AQ", "r"), ("AP", "r"), ("AC = AQ &times; AP", "r")],
      [[f"<b>{r['n']}</b>", q(r["sq"], qdp), money(r["sp"]), money(r["sc"]),
        q(r["aq"]), money(r["ap"]), money(r["ac"])] for r in rr]
      + [{"cls": "tot",
          "cells": ["<b>Total</b>", "", "", f"<b>{money(d['sc'])}</b>", "", "",
                    f"<b>{money(d['ac'])}</b>"]}],
      headcls="lite", widths=["12%", "16%", "10%", "17%", "13%", "10%", "22%"])
    mcv += (f"<div class='calc'><div><b>MCV &nbsp;=&nbsp; {cur}{money(d['sc'])} &minus; "
            f"{cur}{money(d['ac'])} &nbsp;=&nbsp; {vt(d['mcv'])}</b></div></div>")

    mpv = vbox("MATERIAL PRICE VARIANCE", "AQ &times; (SP &minus; AP)",
      [[f"<b>{r['n']}</b>", money(r["sp"]), money(r["ap"]),
        num(r["sp"] - r["ap"]), q(r["aq"]), (vt(r["mpv"]), "r")] for r in rr],
      d["mpv"],
      [("Material", ""), ("SP", "r"), ("AP", "r"), ("SP &minus; AP", "r"), ("AQ", "r"),
       ("Amount " + cur, "r")],
      widths=["17%", "13%", "13%", "17%", "18%", "22%"])

    muv = vbox("MATERIAL USAGE VARIANCE", "SP &times; (SQ &minus; AQ)",
      [[f"<b>{r['n']}</b>", q(r["sq"], qdp), q(r["aq"]),
        num(r["sq"] - r["aq"]), money(r["sp"]), (vt(r["muv"]), "r")] for r in rr],
      d["muv"],
      [("Material", ""), ("SQ", "r"), ("AQ", "r"), ("SQ &minus; AQ", "r"), ("SP", "r"),
       ("Amount " + cur, "r")],
      widths=["17%", "15%", "15%", "17%", "13%", "23%"])

    mmv = vbox("MATERIAL MIX VARIANCE", "SP &times; (RSQ &minus; AQ)",
      [[f"<b>{r['n']}</b>", q(r["rsq"], 2), q(r["aq"]),
        num(r["rsq"] - r["aq"], 2), money(r["sp"]), (vt(r["mmv"]), "r")] for r in rr],
      d["mmv"],
      [("Material", ""), ("RSQ", "r"), ("AQ", "r"), ("RSQ &minus; AQ", "r"), ("SP", "r"),
       ("Amount " + cur, "r")],
      widths=["17%", "15%", "15%", "17%", "13%", "23%"])

    myv = vbox("MATERIAL YIELD VARIANCE", "SP &times; (SQ &minus; RSQ)",
      [[f"<b>{r['n']}</b>", q(r["sq"], qdp), q(r["rsq"], 2),
        num(r["sq"] - r["rsq"], 2), money(r["sp"]), (vt(r["myv"]), "r")] for r in rr],
      d["myv"],
      [("Material", ""), ("SQ", "r"), ("RSQ", "r"), ("SQ &minus; RSQ", "r"), ("SP", "r"),
       ("Amount " + cur, "r")],
      widths=["17%", "15%", "15%", "17%", "13%", "23%"])

    return basic, mcv, mpv, muv, mmv, myv


def material_recon(d, cur=None):
    cur = cur or R
    return table("Reconciliation of the material variances",
      [("Identity", ""), ("Working", ""), ("Result", "r")],
      [{"cls": "recon",
        "cells": ["<b>MCV = MPV + MUV</b>",
                  f"{vt(d['mpv'])} &nbsp;+&nbsp; {vt(d['muv'])}",
                  f"<b>{vt(d['mpv'] + d['muv'])}</b>"]},
       {"cls": "recon",
        "cells": ["&nbsp;&nbsp;&nbsp;<i>and MCV computed directly was</i>", "",
                  f"<b>{vt(d['mcv'])}</b> &nbsp;&#10003;"]},
       {"cls": "recon",
        "cells": ["<b>MUV = MMV + MYV</b>",
                  f"{vt(d['mmv'])} &nbsp;+&nbsp; {vt(d['myv'])}",
                  f"<b>{vt(d['mmv'] + d['myv'])}</b>"]},
       {"cls": "recon",
        "cells": ["&nbsp;&nbsp;&nbsp;<i>and MUV computed directly was</i>", "",
                  f"<b>{vt(d['muv'])}</b> &nbsp;&#10003;"]}],
      headcls="lite", widths=["34%", "40%", "26%"])


def yield_check(d, cur=None):
    """The clean, rounding-free way to verify the yield variance."""
    cur = cur or R
    return (f"""{calc([
      f"Standard cost per unit of output &nbsp;=&nbsp; "
      f"{frac('standard cost of one standard batch', 'standard output of that batch')}"
      f" &nbsp;=&nbsp; <b>{cur}{money(d['std_cost_per_out'])}</b>",
      f"Output the actual input SHOULD have yielded &nbsp;=&nbsp; {q(d['tot_aq'])} &times; "
      f"{frac(q(d['std_out']), q(d['tot_sq_std']))} &nbsp;=&nbsp; "
      f"<b>{q(d['std_yield_of_actual_input'], 2)} units</b>",
      f"Actual output &nbsp;=&nbsp; <b>{q(d['act_out'])} units</b>",
      f"<b>MYV &nbsp;=&nbsp; {cur}{money(d['std_cost_per_out'])} &times; "
      f"({q(d['act_out'])} &minus; {q(d['std_yield_of_actual_input'], 2)}) &nbsp;=&nbsp; "
      f"{vt(d['std_cost_per_out'] * (d['act_out'] - d['std_yield_of_actual_input']))}</b>"])}
<p class="small">This route never touches RSQ, so it is free of rounding error and is the best way to
<b>check</b> the yield variance computed material by material above. The two agree exactly.</p>""")


def material_answer(d, extra=None, cur=None):
    cur = cur or R
    rows = [("Standard cost of actual output", f"{cur} {money(d['sc'])}"),
            ("Actual cost", f"{cur} {money(d['ac'])}"),
            ("<b>Material Cost Variance</b>", f"<b>{vt(d['mcv'])}</b>"),
            ("<b>Material Price Variance</b>", f"<b>{vt(d['mpv'])}</b>"),
            ("<b>Material Usage Variance</b>", f"<b>{vt(d['muv'])}</b>"),
            ("<b>Material Mix Variance</b>", f"<b>{vt(d['mmv'])}</b>"),
            ("<b>Material Yield Variance</b>", f"<b>{vt(d['myv'])}</b>"),
            ("Reconciliation", "MCV = MPV + MUV &nbsp;&middot;&nbsp; MUV = MMV + MYV &nbsp;&#10003;")]
    if extra:
        rows = extra + rows
    return ans(rows)


# ======================================================================
# Q1
# ======================================================================
def q1():
    d = material_engine(
        [dict(n="P", sq=450, sp=20, aq=10000, ap=19),
         dict(n="Q", sq=400, sp=40, aq=8500, ap=42),
         dict(n="R", sq=250, sp=60, aq=4500, ap=65)],
        std_out=1000, act_out=20000)
    basic, mcv, mpv, muv, mmv, myv = material_tables(d)

    qq = f"""<p>The standard material inputs required for 1,000 kg of a finished product are given
below:</p>
{table(None, [("Material", ""), ("Quantity in kg", "r"), ("Standard rate per kg " + R, "r")],
 [["<b>P</b>", "450", "20"], ["<b>Q</b>", "400", "40"], ["<b>R</b>", "250", "60"],
  {"cls": "sub", "cells": ["<b>Total</b>", "<b>1,100</b>", ""]},
  ["Standard loss", "100", ""],
  {"cls": "tot", "cells": ["<b>Standard output</b>", "<b>1,000</b>", ""]}],
 headcls="lite", widths=["30%", "35%", "35%"])}
<p>Actual production in a period was 20,000 kg of the finished product, for which the actual quantities
of material used and the prices paid thereof are as under:</p>
{table(None, [("Material", ""), ("Quantity in kg", "r"), ("Purchase price per kg " + R, "r")],
 [["<b>P</b>", "10,000", "19"], ["<b>Q</b>", "8,500", "42"], ["<b>R</b>", "4,500", "65"],
  {"cls": "tot", "cells": ["<b>Total</b>", "<b>23,000</b>", ""]}],
 headcls="lite", widths=["30%", "35%", "35%"])}
<p>Calculate the: <b>(a)</b> Material Cost Variance <b>(b)</b> Material Price Variance
<b>(c)</b> Material Usage Variance <b>(d)</b> Material Mix Variance <b>(e)</b> Material Yield
Variance.</p>"""

    rd = f"""<p>Before any formula, build the <b>Basic Calculation</b> table. Every one of the five
variances is then read straight out of it.</p>
{bullets([
 '<b>The standard is for 1,000 kg of output but actual output was 20,000 kg</b>, so every standard '
 'quantity must be multiplied by 20. SQ is 9,000, 8,000 and 5,000 &mdash; <b>not</b> 450, 400 and '
 '250. Getting this wrong invalidates the whole answer, and it is the reason the column is headed '
 '&ldquo;SQ <i>for actual output</i>&rdquo;.',
 '<b>The standard loss of 100 kg is already built into the numbers.</b> 1,100 kg of input gives '
 '1,000 kg of output, so the standard is 1.1 kg of input per kg of output. Do not adjust for the loss '
 'a second time.',
 '<b>Total AQ is 23,000 kg against total SQ of 22,000 kg.</b> A thousand kilos more input was used '
 'than the standard allows, so the usage variance will be adverse before you compute anything.',
 '<b>RSQ splits the 23,000 kg actually used in the standard ratio 450 : 400 : 250.</b> It answers '
 '&ldquo;if we had used 23,000 kg but in the correct proportions, how much of each?&rdquo; The '
 'answers are recurring decimals &mdash; keep two places.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q1", "All five material variances, with a standard loss",
                        "Material &middot; p.79")
            + question(qq) + read(rd) + basic + mcv + mpv + muv + mmv + myv
            + wn("<h4 class='mini'>Independent check on the yield variance</h4>" + yield_check(d))
            + material_recon(d)
            + why(f"""<p>Read the five answers together and they tell a single connected story about
the period.</p>
{table(None, [("Variance", ""), ("Result", "r"), ("What it says", "")],
 [["Price", vt(d['mpv']),
   "Materials cost more than standard overall. P was bought " + R + "1 cheaper, but Q was " + R
   + "2 dearer and R was " + R + "5 dearer, and those two swamped the saving on P."],
  ["Mix", vt(d['mmv']),
   "<b>Favourable.</b> The mix was shifted towards the cheap material &mdash; more P at " + R
   + "20 and less R at " + R + "60 than the standard proportions require. Substituting cheap "
   "material for expensive saves money."],
  ["Yield", vt(d['myv']),
   "<b>Adverse, and larger than the mix gain.</b> 23,000 kg of input produced only 20,000 kg of "
   "output, whereas the standard yield would be " + q(d['std_yield_of_actual_input'], 2) + " kg."],
  ["Usage", vt(d['muv']), "The net of the two above &mdash; the mix saving did not cover the yield "
   "loss."],
  ["<b>Cost</b>", "<b>" + vt(d['mcv']) + "</b>",
   "<b>Price plus usage. The overall verdict on materials for the period.</b>"]],
 headcls="lite", widths=["12%", "18%", "70%"])}
<p><b>The mix and yield variances point at the same decision.</b> Someone economised by using more of
the cheap material P and less of the expensive material R, saving {R}{money(abs(d['mmv']))}. But the
resulting mixture yielded badly, and the shortfall in output cost
{R}{money(abs(d['myv']))} &mdash; nearly {R}{money(abs(d['myv']) - abs(d['mmv']))} more than
the saving. <b>That is the finding to report:</b> the cheaper mix was a false economy, and the standard
proportions should be restored.</p>
<p class="small"><b>A note on the arithmetic.</b> Some published solutions to this problem give the mix
variance as {R}26,365.60 (F) and the yield variance as {R}36,365.60 (A), because they round RSQ for
Q to 8,363.69 instead of 8,363.64. The correct figures are
<b>{money(abs(d['mmv']), 2)} (F)</b> and <b>{money(abs(d['myv']), 2)} (A)</b>, and you can prove it:
they must differ by exactly the usage variance of {R}10,000, and only the unrounded pair does.</p>""")
            + material_answer(d, extra=[
                ("SQ for actual output &mdash; P / Q / R", "9,000 / 8,000 / 5,000 kg"),
                ("RSQ for actual input &mdash; P / Q / R",
                 f"{q(d['rows'][0]['rsq'],2)} / {q(d['rows'][1]['rsq'],2)} / "
                 f"{q(d['rows'][2]['rsq'],2)} kg")])
            + "</div>")


# ======================================================================
# Q2
# ======================================================================
def q2():
    # 5,600 kg of ABC; 125 kg of materials per 100 kg of ABC
    # standard mix % of the 125 kg input ; actual mix % of the actual input
    # actual input for 5,600 kg output = 5,600 x 125/100 = 7,000 kg
    act_in = 7000.0
    d = material_engine(
        [dict(n="X", sq=125 * 0.50, sp=40, aq=act_in * 0.60, ap=42),
         dict(n="Y", sq=125 * 0.30, sp=20, aq=act_in * 0.20, ap=16),
         dict(n="Z", sq=125 * 0.20, sp=10, aq=act_in * 0.20, ap=12)],
        std_out=100, act_out=5600)
    basic, mcv, mpv, muv, mmv, myv = material_tables(d)

    qq = f"""<p>XYZ Company manufactures a product ABC by mixing three raw materials. For every 100 kg
of ABC, 125 kg of materials are used. In April 2017 there was an output of 5,600 kg of ABC. The standard
and actual particulars of April 2017 are as under:</p>
{table(None, [("Raw material", ""), ("Standard &mdash; mix %", "r"),
              ("Standard &mdash; price per kg " + R, "r"), ("Actual &mdash; mix %", "r"),
              ("Actual &mdash; price per kg " + R, "r")],
 [["<b>X</b>", "50", "40", "60", "42"], ["<b>Y</b>", "30", "20", "20", "16"],
  ["<b>Z</b>", "20", "10", "20", "12"]], headcls="lite")}
<p>Calculate all the material variances.</p>"""

    rd = f"""<p>The quantities are given as <b>percentages</b>, not kilograms. Convert them before
anything else, and the conversion needs one number the question hides in a sentence.</p>
{steps([
 '<b>Find the total actual input.</b> &ldquo;For every 100 kg of ABC, 125 kg of materials are '
 'used&rdquo;, and output was 5,600 kg. So input = 5,600 &times; '
 + frac("125", "100") + ' = <b>7,000 kg</b>. This single figure unlocks the problem.',
 '<b>Apply the actual mix percentages to 7,000 kg</b> to get AQ: X = 60% = 4,200 kg, Y = 20% = '
 '1,400 kg, Z = 20% = 1,400 kg.',
 '<b>Apply the standard mix percentages to the standard 125 kg batch</b> to get the standard mix: '
 'X = 62.5, Y = 37.5, Z = 25 kg per 100 kg of output.',
 '<b>Scale that standard up to the actual output of 5,600 kg</b> (a factor of 56) to get SQ: '
 'X = 3,500, Y = 2,100, Z = 1,400 kg &mdash; a total of 7,000 kg.'])}
{bullets([
 '<b>Note what has just happened:</b> total SQ = 7,000 kg and total AQ = 7,000 kg. The yield was '
 'exactly standard, so the <b>yield variance will be nil</b> and the whole of the usage variance is '
 'mix. That is a strong check on your arithmetic before you compute anything.',
 '<b>The standard loss is 25 kg per 125 kg of input</b>, i.e. 20% of input. It is already inside the '
 '125 : 100 relationship &mdash; do not deduct it again.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q2", "Material variances when the mix is given in percentages",
                        "Material &middot; p.79")
            + question(qq) + read(rd)
            + wn(f"""<h4 class="mini">W1 &nbsp;Converting the percentages into kilograms</h4>
{calc([f'Total actual input &nbsp;=&nbsp; 5,600 kg output &times; {frac("125", "100")} '
       f'&nbsp;=&nbsp; <b>7,000 kg</b>',
       f'Scale factor from the standard 100 kg batch to the actual 5,600 kg &nbsp;=&nbsp; '
       f'<b>56 times</b>'])}
{table(None, [("Material", ""), ("Standard mix % of 125 kg", "r"),
              ("Standard kg per 100 kg output", "r"), ("SQ for 5,600 kg &nbsp;(&times; 56)", "r"),
              ("Actual mix % of 7,000 kg", "r"), ("AQ in kg", "r")],
 [["<b>X</b>", "50%", "62.50", "3,500", "60%", "4,200"],
  ["<b>Y</b>", "30%", "37.50", "2,100", "20%", "1,400"],
  ["<b>Z</b>", "20%", "25.00", "1,400", "20%", "1,400"],
  {"cls": "tot", "cells": ["<b>Total</b>", "<b>100%</b>", "<b>125.00</b>", "<b>7,000</b>",
                           "<b>100%</b>", "<b>7,000</b>"]}],
 headcls="lite", widths=["13%", "18%", "19%", "19%", "16%", "15%"])}""")
            + basic + mcv + mpv + muv + mmv + myv + material_recon(d)
            + why(f"""<p>This problem is built to isolate the <b>mix</b> variance, and the way it does
so is worth understanding because it makes the concept unmistakable.</p>
{calc([f'Total SQ for actual output &nbsp;=&nbsp; <b>7,000 kg</b>',
       f'Total AQ actually used &nbsp;=&nbsp; <b>7,000 kg</b>',
       f'So the total input was exactly right &nbsp;&rarr;&nbsp; <b>Yield variance = '
       f'{vt(d["myv"])}</b>',
       f'Therefore the whole usage variance is mix &nbsp;&rarr;&nbsp; MUV = MMV = '
       f'<b>{vt(d["muv"])}</b>'])}
<p>The company used exactly the right <i>amount</i> of material and got exactly the standard output
from it. What it got wrong was the <b>proportions</b>: 60% X instead of 50%, and only 20% Y instead of
30%. Since X costs {R}40 a kg and Y only {R}20, substituting the dearer material for the cheaper one
cost money even though not one extra kilogram was consumed.</p>
{table(None, [("Material", ""), ("Standard mix", "r"), ("Actual mix", "r"), ("Price " + R, "r"),
              ("Effect", "")],
 [["<b>X</b>", "50%", "60%", "40", "<b>10% more</b> of the <b>dearest</b> material &mdash; adverse"],
  ["<b>Y</b>", "30%", "20%", "20", "<b>10% less</b> of a mid-priced material &mdash; favourable"],
  ["<b>Z</b>", "20%", "20%", "10", "unchanged &mdash; no mix effect"]],
 headcls="lite", widths=["11%", "15%", "15%", "13%", "46%"])}
<p><b>The price variance is also adverse, but much smaller</b>, at {vt(d['mpv'])} against
{vt(d['mmv'])} on the mix. X and Z were both bought above standard price, but Y was bought {R}4
<i>below</i> it and 1,400 kg of Y was used, so the saving on Y recovered most of the loss:</p>
{calc([f'X &nbsp;=&nbsp; 4,200 kg &times; ({R}40 &minus; {R}42) &nbsp;=&nbsp; '
       f'{vt(d["rows"][0]["mpv"])}',
       f'Y &nbsp;=&nbsp; 1,400 kg &times; ({R}20 &minus; {R}16) &nbsp;=&nbsp; '
       f'{vt(d["rows"][1]["mpv"])}',
       f'Z &nbsp;=&nbsp; 1,400 kg &times; ({R}10 &minus; {R}12) &nbsp;=&nbsp; '
       f'{vt(d["rows"][2]["mpv"])}',
       f'<b>Net &nbsp;=&nbsp; {vt(d["mpv"])}</b>'])}
<p>So the purchasing department did comparatively well &mdash; only {R}{money(abs(d['mpv']))} adverse
on {R}{money(d['ac'])} of spend &mdash; while the mixing operation lost more than twice as much. That
is exactly the separation of responsibility that variance analysis exists to produce.</p>
<p><b>Overall verdict:</b> a cost variance of {vt(d['mcv'])}. Report the mix variance of
{vt(d['mmv'])} to the production manager and ask why the recipe was altered; report the price variance
of {vt(d['mpv'])} to the purchasing manager as a point in their favour.</p>""")
            + material_answer(d, extra=[
                ("Total actual input &nbsp;(5,600 &times; 125/100)", "7,000 kg"),
                ("SQ &mdash; X / Y / Z", "3,500 / 2,100 / 1,400 kg"),
                ("AQ &mdash; X / Y / Z", "4,200 / 1,400 / 1,400 kg")])
            + "</div>")


# ======================================================================
# Q3
# ======================================================================
def q3():
    # standard: 40% A @ 20, 60% B @ 30 per tonne; standard loss 10% of input
    # take a 100-tonne standard batch -> 40 A + 60 B -> output 90 tonnes
    d = material_engine(
        [dict(n="A", sq=40, sp=20, aq=180, ap=18),
         dict(n="B", sq=60, sp=30, aq=220, ap=34)],
        std_out=90, act_out=364)
    basic, mcv, mpv, muv, mmv, myv = material_tables(d, qdp=2)

    qq = f"""<p>The standard cost of a certain chemical mixture is as under:</p>
{bullets(['40% of Material A at ' + R + '20 per tonne',
          '60% of Material B at ' + R + '30 per tonne',
          'A standard loss of 10% is expected in production'])}
<p>The following actual cost data is given for the period:</p>
{table(None, [("Material", ""), ("Quantity in tonnes", "r"), ("Cost per tonne " + R, "r")],
 [["<b>A</b>", "180", "18"], ["<b>B</b>", "220", "34"],
  {"cls": "tot", "cells": ["<b>Total input</b>", "<b>400</b>", ""]}],
 headcls="lite", widths=["30%", "35%", "35%"])}
<p>The weight produced is 364 tonnes. Calculate the: <b>(a)</b> Material Cost Variance
<b>(b)</b> Material Price Variance <b>(c)</b> Material Usage Variance <b>(d)</b> Material Mix Variance
<b>(e)</b> Material Yield Variance.</p>"""

    rd = f"""<p>The standard is given only as percentages and a loss rate, so you must <b>invent a
convenient standard batch</b> to work with. Take 100 tonnes of input &mdash; it makes every percentage
a whole number.</p>
{calc(['Standard batch of input &nbsp;=&nbsp; <b>100 tonnes</b> &nbsp;&rarr;&nbsp; A = 40 tonnes, '
       'B = 60 tonnes',
       'Standard loss &nbsp;=&nbsp; 10% of input &nbsp;=&nbsp; 10 tonnes',
       '<b>Standard output &nbsp;=&nbsp; 100 &minus; 10 &nbsp;=&nbsp; 90 tonnes</b>',
       f'Scale factor to the actual output of 364 tonnes &nbsp;=&nbsp; {frac("364", "90")} '
       f'&nbsp;=&nbsp; <b>4.0444 times</b>'])}
{bullets([
 '<b>The standard loss is 10% of INPUT, not of output.</b> So 100 tonnes in gives 90 tonnes out, and '
 'the standard is ' + frac("100", "90") + ' = 1.1111 tonnes of input per tonne of output. Reading it '
 'as 10% of output would give 90.9 tonnes and every answer would be wrong.',
 '<b>SQ therefore comes out in decimals</b> &mdash; A = 40 &times; 4.0444 = 161.78 tonnes and '
 'B = 60 &times; 4.0444 = 242.67 tonnes, a total of 404.44 tonnes. Keep two decimals throughout.',
 '<b>Actual input was 400 tonnes for 364 tonnes of output</b>, a loss of 36 tonnes or 9% of input '
 '&mdash; <i>better</i> than the 10% standard. So expect a <b>favourable yield variance</b>.',
 '<b>But the mix was wrong:</b> 180 : 220 is 45% : 55% against a standard 40% : 60%. More of the cheap '
 'A and less of the dear B, so expect a <b>favourable mix variance</b> too.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q3", "Material variances with a standard loss on input",
                        "Material &middot; p.79&ndash;80")
            + question(qq) + read(rd) + basic + mcv + mpv + muv + mmv + myv
            + wn("<h4 class='mini'>Independent check on the yield variance</h4>" + yield_check(d))
            + material_recon(d)
            + why(f"""<p>This is the one problem in the set where <b>both</b> parts of the usage
variance are favourable, and it is instructive to see why.</p>
{table(None, [("", ""), ("Standard", "r"), ("Actual", "r"), ("Verdict", "")],
 [["Proportion of A &mdash; the cheap material at " + R + "20", "40%", "45%",
   "more of the cheap one"],
  ["Proportion of B &mdash; the dear material at " + R + "30", "60%", "55%",
   "less of the dear one"],
  ["Loss as a percentage of input", "10%", "9%",
   "<b>better yield than standard</b>"],
  {"cls": "tot", "cells": ["<b>Input consumed for 364 tonnes of output</b>",
                           "<b>404.44 t</b>", "<b>400.00 t</b>",
                           "<b>4.44 tonnes less input than allowed</b>"]}],
 headcls="lite", widths=["40%", "16%", "16%", "28%"])}
<p>So the works manager did well twice over: a cheaper recipe <i>and</i> less waste. Together the mix
and yield variances are worth {vt(d['muv'])}.</p>
<p><b>The cost variance is nevertheless {vt(d['mcv'])}</b>, because the price variance of
{vt(d['mpv'])} more than cancels the usage gain:</p>
{calc([f'Material A &nbsp;=&nbsp; 180 t &times; ({R}20 &minus; {R}18) &nbsp;=&nbsp; '
       f'{vt(d["rows"][0]["mpv"])}',
       f'Material B &nbsp;=&nbsp; 220 t &times; ({R}30 &minus; {R}34) &nbsp;=&nbsp; '
       f'{vt(d["rows"][1]["mpv"])}',
       f'<b>Net price variance &nbsp;=&nbsp; {vt(d["mpv"])}</b>'])}
<p>B was bought {R}4 a tonne above standard &mdash; a 13% overrun on the material that makes up more
than half the mixture. That single fact turns a well-run production month into an adverse
result overall.</p>
<p class="small"><b>The management point worth making.</b> There may be a connection between the two.
If B became scarce and its price rose {R}4, the works manager may have substituted A deliberately
&mdash; and if so, the favourable mix variance is a <i>response</i> to the adverse price variance, not
an independent achievement. Variances are computed separately but they are not always caused
separately, and saying so is the mark of a real answer rather than an arithmetic one.</p>""")
            + material_answer(d, extra=[
                ("Standard batch assumed", "100 tonnes input &rarr; 90 tonnes output"),
                ("SQ for 364 tonnes &mdash; A / B", "161.78 / 242.67 tonnes"),
                ("Actual loss vs standard loss", "9% of input vs 10% &mdash; better")])
            + "</div>")



# ======================================================================
# Q4
# ======================================================================
def q4():
    d = material_engine(
        [dict(n="A", sq=75, sp=2, aq=2200, ap=4650 / 2200),
         dict(n="B", sq=25, sp=10, aq=800, ap=7850 / 800)],
        std_out=90, act_out=2850)
    basic, mcv, mpv, muv, mmv, myv = material_tables(d, qdp=2)

    qq = f"""<p>The following information has been extracted from the records of a chemical company:</p>
{bullets(['<b>Standard price:</b> Raw Material A = ' + R + '2 per kg; Raw Material B = ' + R
          + '10 per kg',
          '<b>Standard mix:</b> A = 75% and B = 25% (by weight)',
          '<b>Standard yield:</b> 90%'])}
<p>In a period of actual costs, usages and output were as follows:</p>
{table(None, [("Used", ""), ("Quantity", "r"), ("Cost " + R, "r")],
 [["<b>Material A</b>", "2,200 kg", "4,650"], ["<b>Material B</b>", "800 kg", "7,850"],
  {"cls": "tot", "cells": ["<b>Total</b>", "<b>3,000 kg</b>", "<b>12,500</b>"]}],
 headcls="lite", widths=["34%", "33%", "33%"])}
<p><b>Output:</b> 2,850 kg of product. Calculate the material cost variances. Also reconcile the
material cost variances.</p>"""

    rd = f"""<p>Two conversions are needed before the standard tables can be built, and each is a
common stumbling point.</p>
{steps([
 '<b>The actual PRICE is not given &mdash; only the total cost.</b> Divide: '
 + calc([f'A &nbsp;=&nbsp; {frac(R + "4,650", "2,200 kg")} &nbsp;=&nbsp; '
         f'<b>{R}{money(4650/2200, 4)} per kg</b> &nbsp; (against a standard of {R}2)',
         f'B &nbsp;=&nbsp; {frac(R + "7,850", "800 kg")} &nbsp;=&nbsp; '
         f'<b>{R}{money(7850/800, 4)} per kg</b> &nbsp; (against a standard of {R}10)']),
 '<b>&ldquo;Standard yield 90%&rdquo; means 90% of INPUT.</b> Take a standard batch of 100 kg of '
 'input: A = 75 kg, B = 25 kg, and output = 90 kg. So the scale factor to the actual output of '
 '2,850 kg is ' + frac("2,850", "90") + ' = <b>31.6667</b>.'])}
{bullets([
 '<b>SQ therefore comes out in decimals</b> &mdash; A = 2,375 kg and B = 791.67 kg, totalling '
 '3,166.67 kg. Note that this is <b>more</b> than the 3,000 kg actually used, so the overall usage '
 'variance will be favourable.',
 '<b>But look at the mix.</b> Actual was 2,200 : 800, which is 73.33% : 26.67% against a standard of '
 '75% : 25%. More of the <b>expensive</b> B at ' + R + '10 and less of the cheap A at ' + R + '2 '
 '&mdash; so expect an <b>adverse mix variance</b>.',
 '<b>And the yield.</b> 3,000 kg of input should have yielded 2,700 kg; it yielded 2,850 kg, which is '
 '95% against a standard 90%. A clearly <b>favourable yield variance</b>.',
 'So this problem has a favourable yield fighting an adverse mix &mdash; the exact opposite of Q1.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q4", "Material variances when only the total cost is given",
                        "Material &middot; p.80")
            + question(qq) + read(rd) + basic + mcv + mpv + muv + mmv + myv
            + wn("<h4 class='mini'>Independent check on the yield variance</h4>" + yield_check(d))
            + material_recon(d)
            + why(f"""<p>The overall result is <b>{vt(d['mcv'])}</b> &mdash; a rare favourable cost
variance, and it is worth tracing where it comes from because three of the five variances are adverse.</p>
{table(None, [("Variance", ""), ("Result", "r"), ("Cause", "")],
 [["Price", vt(d['mpv']),
   "A cost " + R + money(4650/2200 - 2, 4) + " a kg above standard (" + vt(d['rows'][0]['mpv'])
   + "), but B was bought " + R + money(10 - 7850/800, 4) + " below standard ("
   + vt(d['rows'][1]['mpv']) + "). The net is small."],
  ["Mix", vt(d['mmv']),
   "Too much of the expensive B. Only 73.33% A instead of 75%, and B is five times the price of A."],
  ["Yield", vt(d['myv']),
   "<b>The whole story.</b> 3,000 kg yielded 2,850 kg &mdash; a 95% yield against the 90% standard, "
   "so 150 kg of extra output came free."],
  ["Usage", vt(d['muv']), "Yield gain net of the mix loss"],
  ["<b>Cost</b>", "<b>" + vt(d['mcv']) + "</b>", "<b>Usage gain net of the small price loss</b>"]],
 headcls="lite", widths=["12%", "16%", "72%"])}
{calc([f'Standard yield from 3,000 kg of input &nbsp;=&nbsp; 3,000 &times; 90% &nbsp;=&nbsp; '
       f'<b>2,700 kg</b>',
       f'Actual output &nbsp;=&nbsp; <b>2,850 kg</b> &nbsp;&rarr;&nbsp; an actual yield of '
       f'<b>95%</b>',
       f'Extra output obtained free &nbsp;=&nbsp; <b>150 kg</b>, worth 150 &times; '
       f'{R}{money(d["std_cost_per_out"], 4)} &nbsp;=&nbsp; {vt(d["myv"])}'])}
<p><b>The lesson of this problem is that the yield variance dominates.</b> In a chemical process the
proportion of raw material converted into finished product matters far more than the price paid for it
or the exact recipe used. A five-point improvement in yield was worth {R}{money(abs(d['myv']))},
whereas the entire adverse effect of the mix was only {R}{money(abs(d['mmv']))} and of the price only
{R}{money(abs(d['mpv']))}.</p>
<p class="small"><b>What to recommend.</b> Investigate <i>why</i> the yield improved to 95% and whether
it can be held &mdash; if the improvement is genuine and repeatable, the <b>standard itself should be
revised</b> from 90% to something nearer 95%. A standard that is consistently beaten has stopped being a
control and becomes an excuse. This is the essential maintenance work of any standard costing
system.</p>""")
            + material_answer(d, extra=[
                ("Actual price &mdash; A / B",
                 f"{R} {money(4650/2200, 4)} / {R} {money(7850/800, 4)} per kg"),
                ("SQ for 2,850 kg &mdash; A / B", "2,375.00 / 791.67 kg"),
                ("Actual yield vs standard", "95% vs 90% &mdash; better by 150 kg")])
            + "</div>")


# ======================================================================
# Q5
# ======================================================================
def q5():
    d = material_engine(
        [dict(n="Zee", sq=3500, sp=10, aq=3700, ap=12),
         dict(n="Wee", sq=1500, sp=21, aq=1650, ap=20),
         dict(n="Tee", sq=1000, sp=33, aq=1250, ap=36)],
        std_out=6000, act_out=6000)
    basic, mcv, mpv, muv, mmv, myv = material_tables(d)

    qq = f"""<p>From the following data compute the material cost variances and reconcile the material
variances.</p>
{table(None, [("Materials", ""), ("Standard &mdash; units", "r"),
              ("Standard &mdash; price per unit " + R, "r"), ("Actual &mdash; units", "r"),
              ("Actual &mdash; price per unit " + R, "r")],
 [["<b>Zee</b>", "3,500", "10", "3,700", "12"],
  ["<b>Wee</b>", "1,500", "21", "1,650", "20"],
  ["<b>Tee</b>", "1,000", "33", "1,250", "36"],
  {"cls": "tot", "cells": ["<b>Total</b>", "<b>6,000</b>", "", "<b>6,600</b>", ""]}],
 headcls="lite")}"""

    rd = f"""<p>The simplest material problem in the set, because <b>no loss and no separate output
figure are given</b>. The standard quantities are already the standard for the actual output, so there
is no scaling to do &mdash; SQ is simply 3,500, 1,500 and 1,000.</p>
{bullets([
 '<b>Total AQ of 6,600 units against total SQ of 6,000.</b> Ten per cent more material was consumed '
 'than the standard allows, so the usage variance is going to be substantially adverse.',
 '<b>RSQ splits the 6,600 units actually used in the standard ratio 3,500 : 1,500 : 1,000</b>, which '
 'simplifies to 7 : 3 : 2. So RSQ = 3,850, 1,650 and 1,100 &mdash; all whole numbers, which makes '
 'this a good problem on which to learn the mechanics.',
 '<b>Notice Wee.</b> Actual 1,650 units is exactly its RSQ of 1,650, so Wee contributes '
 '<b>nothing</b> to the mix variance. Its entire usage variance is yield. That is a neat illustration '
 'of what the split actually means.',
 '<b>Two prices rose and one fell.</b> Zee up ' + R + '2, Tee up ' + R + '3, Wee down ' + R + '1.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q5", "Material variances with no loss &mdash; the mechanics in their simplest form",
                        "Material &middot; p.80")
            + question(qq) + read(rd) + basic + mcv + mpv + muv + mmv + myv + material_recon(d)
            + why(f"""<p>Every variance here is adverse except the price variance on Wee. This is a
straightforwardly bad month, and the value of the analysis is that it shows <b>where</b> the damage was
done rather than merely that it happened.</p>
{table(None, [("", ""), ("Amount", "r"), ("Share of the total", "r"), ("Who is answerable", "")],
 [["Price variance", vt(d['mpv']), f"{abs(d['mpv'])/abs(d['mcv'])*100:.0f}%",
   "<b>Purchasing.</b> Zee and Tee were both bought above standard price."],
  ["Mix variance", vt(d['mmv']), f"{abs(d['mmv'])/abs(d['mcv'])*100:.0f}%",
   "<b>Production.</b> Too much Tee, the dearest material at " + R + "33."],
  ["Yield variance", vt(d['myv']), f"{abs(d['myv'])/abs(d['mcv'])*100:.0f}%",
   "<b>Production.</b> 6,600 units of input produced only what 6,000 should have."],
  {"cls": "tot", "cells": ["<b>Total cost variance</b>", "<b>" + vt(d['mcv']) + "</b>",
                           "<b>100%</b>", ""]}], headcls="lite",
 widths=["20%", "18%", "16%", "46%"])}
<p><b>Look at Wee to understand what mix and yield really separate.</b> Wee&rsquo;s usage variance is
{vt(d['rows'][1]['muv'])} in total, and it divides as {vt(d['rows'][1]['mmv'])} mix and
{vt(d['rows'][1]['myv'])} yield &mdash; the mix part is exactly nil.</p>
{calc([f'Wee: RSQ = 1,650 units and AQ = 1,650 units &nbsp;&rarr;&nbsp; the proportion used was '
       f'<b>exactly standard</b>, so no mix effect',
       f'Wee: SQ = 1,500 units but RSQ = 1,650 units &nbsp;&rarr;&nbsp; 150 extra units were needed '
       f'because the batch as a whole over-consumed &mdash; that is <b>pure yield</b>'])}
<p>So mix asks <i>&ldquo;were the proportions right?&rdquo;</i> and yield asks <i>&ldquo;was the total
right?&rdquo;</i>. Wee&rsquo;s proportion was perfect; it simply got dragged along by a batch that used
10% too much material overall.</p>
<p><b>Recommendation:</b> the yield variance of {vt(d['myv'])} is the largest single item and points to
a process problem &mdash; wastage, spoilage, or a specification that is no longer achievable.
Investigate that first. The mix variance of {vt(d['mmv'])} is a secondary matter of using too much Tee
at {R}33 when Zee at {R}10 was available.</p>""")
            + material_answer(d, extra=[
                ("SQ &mdash; Zee / Wee / Tee", "3,500 / 1,500 / 1,000 units"),
                ("RSQ &mdash; Zee / Wee / Tee", "3,850 / 1,650 / 1,100 units"),
                ("Total input &mdash; standard vs actual", "6,000 vs 6,600 units")])
            + "</div>")


# ======================================================================
# Q6
# ======================================================================
def q6():
    d = material_engine(
        [dict(n="X", sq=45, sp=6.00, aq=4200, ap=6.50),
         dict(n="Y", sq=25, sp=4.50, aq=1700, ap=4.25),
         dict(n="Z", sq=30, sp=9.50, aq=2600, ap=9.75)],
        std_out=90, act_out=7425)
    basic, mcv, mpv, muv, mmv, myv = material_tables(d, qdp=2)

    qq = f"""<p>The standard mix of product A2 is as follows:</p>
{table(None, [("Kgs", "r"), ("Materials", ""), ("Price per kg " + R, "r")],
 [["45", "<b>X</b>", "6.00"], ["25", "<b>Y</b>", "4.50"], ["30", "<b>Z</b>", "9.50"],
  {"cls": "tot", "cells": ["<b>100</b>", "<b>Total input</b>", ""]}],
 headcls="lite", widths=["25%", "40%", "35%"])}
<p>The standard loss in production is 10% of input. There is no scrap value. Actual production for a
month was 7,425 kg of A2 from 80 mixes. Actual consumption and purchases of material during the month
were:</p>
{table(None, [("Kgs", "r"), ("Materials", ""), ("Price per kg " + R, "r")],
 [["4,200", "<b>X</b>", "6.50"], ["1,700", "<b>Y</b>", "4.25"], ["2,600", "<b>Z</b>", "9.75"],
  {"cls": "tot", "cells": ["<b>8,500</b>", "<b>Total input</b>", ""]}],
 headcls="lite", widths=["25%", "40%", "35%"])}
<p>You are required to calculate the material variances and reconcile the same.</p>"""

    rd = f"""<p>The standard batch is conveniently 100 kg, so the kilogram figures <i>are</i> the
percentages. One phrase in the question is a distraction and one is essential.</p>
{bullets([
 '<b>Essential: &ldquo;standard loss 10% of input&rdquo;.</b> 100 kg in gives <b>90 kg out</b>. The '
 'scale factor to the actual 7,425 kg of output is ' + frac("7,425", "90") + ' = <b>82.5</b>.',
 '<b>Essential: SQ = 45 &times; 82.5, 25 &times; 82.5, 30 &times; 82.5</b> = 3,712.50, 2,062.50 and '
 '2,475 kg &mdash; a total of <b>8,250 kg</b>, against 8,500 kg actually used.',
 '<b>A distraction: &ldquo;from 80 mixes&rdquo;.</b> Eighty standard mixes would be 8,000 kg of input '
 'and 7,200 kg of output. Neither figure is the one to use &mdash; actual input was 8,500 kg and '
 'actual output 7,425 kg. But the phrase is a useful reality check: <b>8,500 kg was drawn for what '
 'was planned as 80 mixes of 100 kg</b>, so 500 kg of extra material went in.',
 '<b>&ldquo;No scrap value&rdquo;</b> means the loss cannot be credited back. It removes a '
 'complication rather than adding one.',
 'Actual mix is 4,200 : 1,700 : 2,600 on 8,500 kg = 49.4% : 20.0% : 30.6% against a standard of '
 '45% : 25% : 30%. So <b>more X and much less Y</b>.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q6", "Material variances with a standard mix of 100 kg and a 10% loss",
                        "Material &middot; p.80&ndash;81")
            + question(qq) + read(rd)
            + wn(f"""<h4 class="mini">W1 &nbsp;The three quantities, and the 80-mixes check</h4>
{calc([f'Standard output per 100 kg batch &nbsp;=&nbsp; 100 &minus; 10% &nbsp;=&nbsp; '
       f'<b>90 kg</b>',
       f'Scale factor &nbsp;=&nbsp; {frac("actual output 7,425", "standard output 90")} '
       f'&nbsp;=&nbsp; <b>82.5</b>',
       f'Standard input allowed for 7,425 kg of output &nbsp;=&nbsp; 100 &times; 82.5 &nbsp;=&nbsp; '
       f'<b>8,250 kg</b>',
       f'Actual input used &nbsp;=&nbsp; <b>8,500 kg</b> &nbsp;&rarr;&nbsp; <b>250 kg more than '
       f'allowed</b>'])}
<p class="small"><b>The 80-mixes cross-check.</b> 80 mixes should have consumed 8,000 kg and produced
7,200 kg. Actual output of 7,425 kg is 103% of that, but actual input of 8,500 kg is 106% &mdash; so
input rose faster than output, which is another way of seeing that the yield was poor.</p>""")
            + basic + mcv + mpv + muv + mmv + myv
            + wn("<h4 class='mini'>Independent check on the yield variance</h4>" + yield_check(d))
            + material_recon(d)
            + why(f"""<p>Every variance in this problem is adverse except the price of Y and the mix
contribution of Y. The overall result is <b>{vt(d['mcv'])}</b>.</p>
{table(None, [("Material", ""), ("Standard mix", "r"), ("Actual mix", "r"), ("Price " + R, "r"),
              ("Mix effect", "r"), ("Comment", "")],
 [["<b>X</b>", "45.0%", "49.4%", "6.00", vt(d['rows'][0]['mmv']),
   "4.4 points too much of a mid-priced material"],
  ["<b>Y</b>", "25.0%", "20.0%", "4.50", vt(d['rows'][1]['mmv']),
   "<b>5 points too little of the CHEAPEST material</b> &mdash; the only favourable line"],
  ["<b>Z</b>", "30.0%", "30.6%", "9.50", vt(d['rows'][2]['mmv']),
   "slightly too much of the dearest material"],
  {"cls": "tot", "cells": ["<b>Total</b>", "<b>100%</b>", "<b>100%</b>", "",
                           "<b>" + vt(d['mmv']) + "</b>", ""]}], headcls="lite",
 widths=["10%", "14%", "13%", "11%", "18%", "34%"])}
<p><b>The mix variance is favourable only because Y was under-used</b>, and that is the interesting
subtlety. Y is the cheapest material at {R}4.50, so using less of it should be <i>adverse</i> for the
mix &mdash; yet the line shows {vt(d['rows'][1]['mmv'])}. The reason is that the mix variance measures
the deviation of each material from <b>its own</b> revised standard: RSQ for Y is 2,125 kg but only
1,700 kg was used, so 425 kg of the cheapest material was <i>saved</i>, and the formula credits that
saving. What the mix variance cannot see is that the 425 kg of Y had to be replaced by something dearer
&mdash; and that shows up as the adverse lines on X and Z.</p>
<p><b>The yield variance of {vt(d['myv'])} is the real problem.</b> 8,500 kg of input should have
yielded {q(d['std_yield_of_actual_input'])} kg of A2 but produced only 7,425 kg &mdash; a shortfall of
225 kg. The actual loss was {(8500-7425)/8500*100:.1f}% of input against a standard 10%.</p>
<p><b>Recommendation:</b> report the price variance of {vt(d['mpv'])} to purchasing &mdash; X and Z were
both bought above standard, and X at 4,200 kg is the largest single item of spend. Report the yield
shortfall to production, and note that reducing Y from 25% to 20% of the mixture may itself be the cause
of the poor yield. As in Q1, an apparent economy in the recipe has probably cost more than it
saved.</p>""")
            + material_answer(d, extra=[
                ("Scale factor &nbsp;(7,425 &divide; 90)", "82.5"),
                ("SQ &mdash; X / Y / Z", "3,712.50 / 2,062.50 / 2,475.00 kg"),
                ("Standard input allowed vs actual", "8,250 vs 8,500 kg"),
                ("Actual loss vs standard loss",
                 f"{(8500-7425)/8500*100:.1f}% of input vs 10%")])
            + "</div>")


# ======================================================================
# Q7
# ======================================================================
def q7():
    # actual output 144 kg at 80% yield -> actual input 180 kg; B was 108, so A = 72
    d = material_engine(
        [dict(n="A", sq=60, sp=10, aq=72, ap=12),
         dict(n="B", sq=140, sp=2, aq=108, ap=8)],
        std_out=180, act_out=144)
    basic, mcv, mpv, muv, mmv, myv = material_tables(d)

    qq = f"""<p>The standard cost for producing 180 kg of a product whose raw material inputs are A and
B is given below:</p>
{table(None, [("Material", ""), ("Standard", ""), (R, "r")],
 [["<b>A</b>", "60 kg at " + R + "10 per kg", "600"],
  ["<b>B</b>", "140 kg at " + R + "2 per kg", "280"],
  {"cls": "tot", "cells": ["<b>Total cost</b>", "200 kg of input &rarr; 180 kg of output",
                           "<b>880</b>"]}], headcls="lite", widths=["20%", "52%", "28%"])}
<p>The actual prices of A and B were {R}12 and {R}8 per kg respectively. Consumption of B was 108 kg.
The actual output at 80% yield was 144 kg. Calculate all the material variances and reconcile them.</p>"""

    rd = f"""<p>This question deliberately withholds the actual quantity of A. You must deduce it, and
the deduction is the whole difficulty.</p>
{steps([
 '<b>Find the actual input from the yield.</b> &ldquo;Actual output at 80% yield was 144 kg&rdquo; '
 'means 144 kg is 80% of the input:'
 + fml("Actual input &nbsp;=&nbsp; " + frac("144 kg", "80%") + " &nbsp;=&nbsp; <b>180 kg</b>"),
 '<b>Then find A by subtraction.</b> Total input 180 kg less B&rsquo;s 108 kg gives '
 '<b>A = 72 kg</b>.',
 '<b>Now the standard.</b> 200 kg of input gives 180 kg of output, so the standard yield is 90%. '
 'Actual output was 144 kg, so the scale factor is ' + frac("144", "180") + ' = <b>0.8</b> and '
 'SQ = 48 kg of A and 112 kg of B.'])}
{bullets([
 '<b>Standard yield 90%, actual yield 80%.</b> A ten-point fall &mdash; expect a firmly adverse yield '
 'variance.',
 '<b>The mix is badly wrong.</b> Standard is 60 : 140, i.e. 30% A and 70% B. Actual is 72 : 108, i.e. '
 '<b>40% A and 60% B</b> &mdash; ten points more of the material that costs five times as much.',
 '<b>Both prices rose sharply.</b> A from ' + R + '10 to ' + R + '12 (+20%) and B from ' + R + '2 to ' +
 R + '8 &mdash; a <b>fourfold</b> increase. B&rsquo;s price alone will dominate the price variance.',
 'Every single variance in this problem will be adverse. It is the worst month in the set, and a good '
 'one on which to practise writing a critical commentary.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q7", "Material variances when the actual quantity must be deduced",
                        "Material &middot; p.81")
            + question(qq) + read(rd)
            + wn(f"""<h4 class="mini">W1 &nbsp;Deducing the actual quantities</h4>
{calc([f'Actual output &nbsp;=&nbsp; 144 kg, at an actual yield of 80% of input',
       f'Actual input &nbsp;=&nbsp; {frac("144", "0.80")} &nbsp;=&nbsp; <b>180 kg</b>',
       f'Consumption of B &nbsp;=&nbsp; 108 kg &nbsp;(given)',
       f'<b>Therefore consumption of A &nbsp;=&nbsp; 180 &minus; 108 &nbsp;=&nbsp; 72 kg</b>'])}
<h4 class="mini">W2 &nbsp;The standard, scaled to the actual output</h4>
{calc([f'Standard: 200 kg of input &rarr; 180 kg of output, a standard yield of <b>90%</b>',
       f'Scale factor &nbsp;=&nbsp; {frac("actual output 144", "standard output 180")} '
       f'&nbsp;=&nbsp; <b>0.8</b>',
       f'SQ &nbsp;=&nbsp; A: 60 &times; 0.8 = <b>48 kg</b> &nbsp;&nbsp; B: 140 &times; 0.8 = '
       f'<b>112 kg</b> &nbsp;&nbsp; total <b>160 kg</b>',
       f'Actual input <b>180 kg</b> against 160 kg allowed &nbsp;&rarr;&nbsp; <b>20 kg too '
       f'much</b>'])}""")
            + basic + mcv + mpv + muv + mmv + myv
            + wn("<h4 class='mini'>Independent check on the yield variance</h4>" + yield_check(d))
            + material_recon(d)
            + why(f"""<p><b>Every variance is adverse</b>, and the total cost variance of
{vt(d['mcv'])} is enormous relative to a standard cost of only {R}{money(d['sc'])} &mdash; an
overrun of {abs(d['mcv'])/d['sc']*100:.0f}%. Three separate things went wrong.</p>
{table(None, [("What went wrong", ""), ("Evidence", ""), ("Cost", "r")],
 [["<b>1. Prices rose steeply</b>",
   "A up 20% from " + R + "10 to " + R + "12; B up <b>300%</b> from " + R + "2 to " + R + "8",
   vt(d['mpv'])],
  ["<b>2. The mix moved to the dear material</b>",
   "40% A instead of 30% &mdash; and A costs five times B at standard prices",
   vt(d['mmv'])],
  ["<b>3. The yield collapsed</b>",
   "80% against a standard 90%; 180 kg of input yielded 144 kg where "
   + q(d['std_yield_of_actual_input']) + " kg was expected",
   vt(d['myv'])],
  {"cls": "tot", "cells": ["<b>Total material cost variance</b>", "", "<b>" + vt(d['mcv'])
                           + "</b>"]}], headcls="lite", widths=["27%", "50%", "23%"])}
<p><b>The price variance is by far the largest, and it is almost entirely B.</b></p>
{calc([f'Material A &nbsp;=&nbsp; 72 kg &times; ({R}10 &minus; {R}12) &nbsp;=&nbsp; '
       f'{vt(d["rows"][0]["mpv"])}',
       f'Material B &nbsp;=&nbsp; 108 kg &times; ({R}2 &minus; {R}8) &nbsp;=&nbsp; '
       f'{vt(d["rows"][1]["mpv"])} &nbsp;&larr;&nbsp; '
       f'{abs(d["rows"][1]["mpv"])/abs(d["mpv"])*100:.0f}% of the whole price variance',
       f'<b>Total price variance &nbsp;=&nbsp; {vt(d["mpv"])}</b>'])}
<p>A material quadrupling in price is not a purchasing failure; it is a change in market conditions.
<b>The correct response is to revise the standard</b>, not to reprimand the buyer. A standard price of
{R}2 for a material now costing {R}8 makes every subsequent variance meaningless, because the whole
of the reported adverse variance is simply the obsolescence of the standard.</p>
<p><b>There may also be a connection between the three failures</b>, and pointing it out is what a full
answer does. If B quadrupled in price, the works manager had an incentive to substitute A &mdash; which
is exactly what the mix variance shows. And if the substitution was made hurriedly, using 40% A in a
process designed for 30%, the collapse in yield from 90% to 80% may be its direct consequence. On that
reading there is <b>one</b> root cause, the price of B, and the mix and yield variances are its
downstream effects.</p>
<p><b>Recommendation:</b> revise the standard price of B immediately; investigate whether the altered
mix caused the yield loss; and if B is permanently dearer, re-examine whether the 30 : 70 recipe is
still the economically correct one rather than merely the standard one.</p>""")
            + material_answer(d, extra=[
                ("Actual input deduced &nbsp;(144 &divide; 80%)", "180 kg"),
                ("Actual quantity of A &nbsp;(180 &minus; 108)", "<b>72 kg</b>"),
                ("SQ &mdash; A / B", "48 / 112 kg"),
                ("Yield &mdash; standard vs actual", "90% vs 80%")])
            + "</div>")



# ======================================================================
# LABOUR VARIANCE ENGINE  -  used by Q8, Q9, Q10
# ======================================================================
def labour_engine(grades, std_out, act_out, idle_per_worker=0.0):
    """
    grades : list of dicts {n, sw, sr, aw, ar, hrs}
             sw  = standard NUMBER of workers of this grade in the gang
             sr  = standard rate per hour
             aw  = actual number of workers engaged
             ar  = actual rate per hour
             hrs = hours in the period per worker (same for every grade)
    std_out: standard output for the gang over those hours
    act_out: actual output achieved
    idle_per_worker: idle hours per worker in the period
    """
    rows = []
    for g in grades:
        sh_std = g["sw"] * g["hrs"]          # standard hours of this grade for std output
        ah = g["aw"] * g["hrs"]              # hours PAID
        rows.append(dict(n=g["n"], sw=g["sw"], sr=g["sr"], aw=g["aw"], ar=g["ar"],
                         hrs=g["hrs"], sh_std=sh_std, ah=ah,
                         idle=g["aw"] * idle_per_worker))
    tot_sh_std = sum(r["sh_std"] for r in rows)
    tot_ah = sum(r["ah"] for r in rows)
    tot_idle = sum(r["idle"] for r in rows)
    tot_worked = tot_ah - tot_idle
    k = act_out / std_out
    for r in rows:
        prop = r["sh_std"] / tot_sh_std      # standard proportion of the gang
        r["sh"] = r["sh_std"] * k            # standard hours FOR ACTUAL OUTPUT
        r["rsh_in"] = tot_ah * prop          # hours PAID, in standard proportion
        r["rsh_wk"] = tot_worked * prop      # hours WORKED, in standard proportion
        r["idle_std"] = tot_idle * prop      # idle hours apportioned on standard composition
        r["sc"] = r["sh"] * r["sr"]
        r["ac"] = r["ah"] * r["ar"]
        r["lrv"] = r["ah"] * (r["sr"] - r["ar"])
        r["lev"] = r["sr"] * (r["sh"] - r["ah"])
        r["lmv"] = r["sr"] * (r["rsh_in"] - r["ah"])
        r["lyv"] = r["sr"] * (r["sh"] - r["rsh_wk"])
        r["litv"] = -r["idle_std"] * r["sr"]          # always adverse
    d = dict(rows=rows, tot_sh_std=tot_sh_std, tot_ah=tot_ah, tot_idle=tot_idle,
             tot_worked=tot_worked, k=k, std_out=std_out, act_out=act_out,
             tot_sh=sum(r["sh"] for r in rows),
             tot_rsh_in=sum(r["rsh_in"] for r in rows),
             tot_rsh_wk=sum(r["rsh_wk"] for r in rows),
             sc=sum(r["sc"] for r in rows), ac=sum(r["ac"] for r in rows),
             lrv=sum(r["lrv"] for r in rows), lev=sum(r["lev"] for r in rows),
             lmv=sum(r["lmv"] for r in rows), lyv=sum(r["lyv"] for r in rows),
             litv=sum(r["litv"] for r in rows))
    d["lcv"] = d["sc"] - d["ac"]
    return d


def labour_tables(d, cur=None):
    cur = cur or R
    rr = d["rows"]

    basic = table("Basic Calculation &mdash; hours",
      [("Grade", ""), ("Standard workers", "r"), ("SH<br/><span class='small'>std output</span>", "r"),
       ("SH for actual output", "r"), ("SR", "r"), ("Actual workers", "r"),
       ("AH<br/><span class='small'>paid</span>", "r"), ("AR", "r"),
       ("RSH on hours paid", "r"), ("RSH on hours worked", "r")],
      [[f"<b>{r['n']}</b>", q(r["sw"]), q(r["sh_std"]), q(r["sh"]), money(r["sr"], 3),
        q(r["aw"]), q(r["ah"]), money(r["ar"], 3), q(r["rsh_in"]), q(r["rsh_wk"])] for r in rr]
      + [{"cls": "tot",
          "cells": ["<b>Total</b>", f"<b>{q(sum(r['sw'] for r in rr))}</b>",
                    f"<b>{q(d['tot_sh_std'])}</b>", f"<b>{q(d['tot_sh'])}</b>", "",
                    f"<b>{q(sum(r['aw'] for r in rr))}</b>", f"<b>{q(d['tot_ah'])}</b>", "",
                    f"<b>{q(d['tot_rsh_in'])}</b>", f"<b>{q(d['tot_rsh_wk'])}</b>"]}],
      headcls="lite",
      widths=["11%", "9%", "9%", "11%", "8%", "9%", "9%", "8%", "13%", "13%"])
    basic += (f"<div class='small'><b>Checks.</b> RSH on hours paid totals "
              f"{q(d['tot_rsh_in'])} = total AH of {q(d['tot_ah'])}. RSH on hours worked totals "
              f"{q(d['tot_rsh_wk'])} = hours paid {q(d['tot_ah'])} less idle hours "
              f"{q(d['tot_idle'])}. Both must hold.</div>")

    lcv = table("1. &nbsp;LABOUR COST VARIANCE &nbsp;=&nbsp; SC &minus; AC &nbsp;=&nbsp; "
                "(SH &times; SR) &minus; (AH &times; AR)",
      [("Grade", ""), ("SH for actual output", "r"), ("SR", "r"), ("SC", "r"), ("AH", "r"),
       ("AR", "r"), ("AC", "r")],
      [[f"<b>{r['n']}</b>", q(r["sh"]), money(r["sr"], 3), money(r["sc"], 2),
        q(r["ah"]), money(r["ar"], 3), money(r["ac"], 2)] for r in rr]
      + [{"cls": "tot", "cells": ["<b>Total</b>", "", "", f"<b>{money(d['sc'], 2)}</b>", "", "",
                                  f"<b>{money(d['ac'], 2)}</b>"]}],
      headcls="lite", widths=["13%", "17%", "11%", "16%", "13%", "11%", "19%"])
    lcv += (f"<div class='calc'><div><b>LCV &nbsp;=&nbsp; {cur}{money(d['sc'], 2)} &minus; "
            f"{cur}{money(d['ac'], 2)} &nbsp;=&nbsp; {vt(d['lcv'])}</b></div></div>")

    lrv = vbox("LABOUR RATE VARIANCE", "AH &times; (SR &minus; AR)",
      [[f"<b>{r['n']}</b>", money(r["sr"], 3), money(r["ar"], 3),
        num(r["sr"] - r["ar"], 3), q(r["ah"]), (vt(r["lrv"]), "r")] for r in rr],
      d["lrv"],
      [("Grade", ""), ("SR", "r"), ("AR", "r"), ("SR &minus; AR", "r"), ("AH", "r"),
       ("Amount " + cur, "r")], widths=["17%", "13%", "13%", "17%", "18%", "22%"])

    lev = vbox("LABOUR EFFICIENCY VARIANCE", "SR &times; (SH &minus; AH)",
      [[f"<b>{r['n']}</b>", q(r["sh"]), q(r["ah"]), num(r["sh"] - r["ah"]),
        money(r["sr"], 3), (vt(r["lev"]), "r")] for r in rr],
      d["lev"],
      [("Grade", ""), ("SH", "r"), ("AH", "r"), ("SH &minus; AH", "r"), ("SR", "r"),
       ("Amount " + cur, "r")], widths=["17%", "15%", "15%", "17%", "13%", "23%"])

    lmv = vbox("LABOUR MIX (GANG COMPOSITION) VARIANCE", "SR &times; (RSH &minus; AH)",
      [[f"<b>{r['n']}</b>", q(r["rsh_in"]), q(r["ah"]), num(r["rsh_in"] - r["ah"]),
        money(r["sr"], 3), (vt(r["lmv"]), "r")] for r in rr],
      d["lmv"],
      [("Grade", ""), ("RSH on hours paid", "r"), ("AH", "r"), ("RSH &minus; AH", "r"), ("SR", "r"),
       ("Amount " + cur, "r")], widths=["15%", "19%", "14%", "17%", "12%", "23%"])

    lyv = vbox("LABOUR YIELD VARIANCE", "SR &times; (SH &minus; RSH on hours worked)",
      [[f"<b>{r['n']}</b>", q(r["sh"]), q(r["rsh_wk"]), num(r["sh"] - r["rsh_wk"]),
        money(r["sr"], 3), (vt(r["lyv"]), "r")] for r in rr],
      d["lyv"],
      [("Grade", ""), ("SH", "r"), ("RSH on hours worked", "r"), ("SH &minus; RSH", "r"), ("SR", "r"),
       ("Amount " + cur, "r")], widths=["15%", "15%", "20%", "15%", "12%", "23%"])

    litv = vbox("LABOUR IDLE TIME VARIANCE", "Idle hours &times; SR &nbsp;&mdash; always ADVERSE",
      [[f"<b>{r['n']}</b>", q(r["idle_std"]), money(r["sr"], 3), (vt(r["litv"]), "r")] for r in rr],
      d["litv"],
      [("Grade", ""), ("Idle hours on standard composition", "r"), ("SR", "r"),
       ("Amount " + cur, "r")], widths=["22%", "36%", "17%", "25%"],
      note="Total idle hours of " + q(d["tot_idle"]) + " apportioned on the <b>standard</b> gang "
           "composition. Apportioning on the standard rather than the actual composition is what "
           "makes the reconciliation LEV = LMV + LYV + LITV close exactly.")

    return basic, lcv, lrv, lev, lmv, lyv, litv


def labour_recon(d):
    return table("Reconciliation of the labour variances",
      [("Identity", ""), ("Working", ""), ("Result", "r")],
      [{"cls": "recon",
        "cells": ["<b>LCV = LRV + LEV</b>",
                  f"{vt(d['lrv'])} &nbsp;+&nbsp; {vt(d['lev'])}",
                  f"<b>{vt(d['lrv'] + d['lev'])}</b>"]},
       {"cls": "recon",
        "cells": ["&nbsp;&nbsp;&nbsp;<i>and LCV computed directly was</i>", "",
                  f"<b>{vt(d['lcv'])}</b> &nbsp;&#10003;"]},
       {"cls": "recon",
        "cells": ["<b>LEV = LMV + LYV + LITV</b>",
                  f"{vt(d['lmv'])} &nbsp;+&nbsp; {vt(d['lyv'])} &nbsp;+&nbsp; {vt(d['litv'])}",
                  f"<b>{vt(d['lmv'] + d['lyv'] + d['litv'])}</b>"]},
       {"cls": "recon",
        "cells": ["&nbsp;&nbsp;&nbsp;<i>and LEV computed directly was</i>", "",
                  f"<b>{vt(d['lev'])}</b> &nbsp;&#10003;"]}],
      headcls="lite", widths=["28%", "46%", "26%"])


def labour_answer(d, extra=None, cur=None):
    cur = cur or R
    rows = [("Standard cost of actual output", f"{cur} {money(d['sc'], 2)}"),
            ("Actual cost", f"{cur} {money(d['ac'], 2)}"),
            ("<b>(a) Labour Rate Variance</b>", f"<b>{vt(d['lrv'])}</b>"),
            ("<b>(b) Labour Mix / Gang Variance</b>", f"<b>{vt(d['lmv'])}</b>"),
            ("<b>(c) Labour Idle Time Variance</b>", f"<b>{vt(d['litv'])}</b>"),
            ("<b>(d) Labour Yield Variance</b>", f"<b>{vt(d['lyv'])}</b>"),
            ("<b>(e) Labour Efficiency Variance</b>", f"<b>{vt(d['lev'])}</b>"),
            ("<b>(f) Labour Cost Variance</b>", f"<b>{vt(d['lcv'])}</b>"),
            ("Reconciliation",
             "LCV = LRV + LEV &nbsp;&middot;&nbsp; LEV = LMV + LYV + LITV &nbsp;&#10003;")]
    if extra:
        rows = extra + rows
    return ans(rows)


LABOUR_METHOD = """
<div class="blk method"><span class="lab">The method for this type &mdash; always these steps</span>
{steps}
</div>"""


# ======================================================================
# Q8
# ======================================================================
def q8():
    d = labour_engine(
        [dict(n="Men", sw=10, sr=0.625, aw=13, ar=0.600, hrs=40),
         dict(n="Women", sw=5, sr=0.400, aw=4, ar=0.425, hrs=40),
         dict(n="Boys", sw=5, sr=0.350, aw=3, ar=0.325, hrs=40)],
        std_out=1000, act_out=960, idle_per_worker=2)
    basic, lcv, lrv, lev, lmv, lyv, litv = labour_tables(d)

    qq = f"""<p>Following information is given regarding standard composition and standard rates of a
gang of workers:</p>
{table(None, [("Standard composition", ""), ("Standard hourly rate " + R, "r")],
 [["10 Men", "0.625"], ["5 Women", "0.400"], ["5 Boys", "0.350"]],
 headcls="lite", widths=["58%", "42%"])}
<p>According to given specifications, a week consists of 40 hours and standard output for a week is
1,000 units. In a particular week, the gang consisted of 13 men, 4 women and 3 boys and actual wages
were paid as follows: Men at {R}0.600 per hour, Women at {R}0.425 per hour, Boys at {R}0.325 per
hour.</p>
<p><b>Two hours were lost in the week due to abnormal idle time.</b> Actual production was 960 units in
the week.</p>
<p>Find out: <b>(a)</b> Labour Rate Variance <b>(b)</b> Labour Mix Variance <b>(c)</b> Labour Idle Time
Variance <b>(d)</b> Labour Yield Variance <b>(e)</b> Labour Efficiency Variance <b>(f)</b> Labour Cost
Variance. You are also required to reconcile the above variances.</p>"""

    rd = f"""<p>Labour problems have one complication that material problems do not: <b>hours paid are
not the same as hours worked</b>. Set out four different hour figures before starting.</p>
{table(None, [("Figure", ""), ("Meaning", ""), ("Computation", ""), ("Total", "r")],
 [["<b>SH</b> for standard output", "Hours the standard gang works in a week",
   "(10 + 5 + 5) workers &times; 40 hours", "<b>800 hrs</b>"],
  ["<b>SH</b> for actual output", "Hours the standard gang <i>should</i> take for 960 units",
   "800 &times; " + frac("960", "1,000"), "<b>768 hrs</b>"],
  ["<b>AH</b> &mdash; hours PAID", "Hours the actual gang was paid for",
   "(13 + 4 + 3) workers &times; 40 hours", "<b>800 hrs</b>"],
  ["Hours WORKED", "Hours in which production actually happened",
   "800 paid &minus; 40 idle", "<b>760 hrs</b>"]],
 headcls="lite", widths=["20%", "32%", "28%", "20%"])}
{bullets([
 '<b>&ldquo;Two hours were lost&rdquo; means two hours PER WORKER.</b> With 20 workers that is '
 '<b>40 idle hours</b> in total. Reading it as two hours altogether is a standard error and it makes '
 'the reconciliation fail.',
 '<b>By coincidence AH = 800 hours and SH for standard output = 800 hours.</b> The gang is the same '
 'size &mdash; 20 workers &mdash; but composed differently: 13 men instead of 10, and fewer women and '
 'boys. So there is <b>no capacity difference, only a composition difference</b>, which is exactly '
 'what the mix variance measures.',
 '<b>The gang produced 960 units in 800 paid hours</b> where the standard is 1,000 units in 800 hours. '
 'So efficiency is down &mdash; and part of that is the idle time, which is why the efficiency variance '
 'splits three ways.',
 '<b>Men were paid BELOW standard and women and boys ABOVE.</b> ' + R + '0.600 against ' + R
 + '0.625 for men; ' + R + '0.425 against ' + R + '0.400 for women; ' + R + '0.325 against ' + R
 + '0.350 for boys. Mixed signs, so compute each line separately.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q8", "All six labour variances, with abnormal idle time",
                        "Labour &middot; p.81")
            + question(qq) + read(rd)
            + method(steps([
                '<b>Compute the four hour figures</b> in the table above: SH for actual output, AH '
                'paid, hours worked, and total idle hours.',
                '<b>Compute RSH twice</b> &mdash; once on hours <b>paid</b> (for the mix variance) and '
                'once on hours <b>worked</b> (for the yield variance), both in the standard '
                'composition 10 : 5 : 5.',
                '<b>Rate variance</b> = AH &times; (SR &minus; AR), grade by grade.',
                '<b>Efficiency variance</b> = SR &times; (SH &minus; AH), using hours <b>paid</b>.',
                '<b>Split the efficiency variance three ways:</b> mix on hours paid, yield on hours '
                'worked, and idle time on the standard composition.',
                '<b>Reconcile.</b> LCV = LRV + LEV, and LEV = LMV + LYV + LITV. If the second does '
                'not close, the idle hours have been apportioned on the wrong composition.']))
            + wn(f"""<h4 class="mini">W1 &nbsp;Idle hours &mdash; two hours per worker</h4>
{calc([f'Men &nbsp;=&nbsp; 13 workers &times; 2 hours &nbsp;=&nbsp; 26 idle hours',
       f'Women &nbsp;=&nbsp; 4 workers &times; 2 hours &nbsp;=&nbsp; 8 idle hours',
       f'Boys &nbsp;=&nbsp; 3 workers &times; 2 hours &nbsp;=&nbsp; 6 idle hours',
       f'<b>Total idle hours &nbsp;=&nbsp; 40</b> &nbsp;&rarr;&nbsp; hours worked = 800 &minus; 40 '
       f'= <b>760</b>'])}
<p class="small">For the <b>idle time variance</b> these 40 hours are re-apportioned on the
<i>standard</i> composition 10 : 5 : 5, giving 20 : 10 : 10 hours. That is the apportionment which makes
the reconciliation close, and the reason is algebraic: the idle-time variance must equal
SR &times; (RSH on hours worked &minus; RSH on hours paid), and both RSH figures are built on the
standard proportions.</p>""")
            + basic + lcv + lrv + lev + lmv + lyv + litv + labour_recon(d)
            + why(f"""<p>The labour cost variance is <b>{vt(d['lcv'])}</b>, and it divides into a small
favourable rate effect and a larger adverse efficiency effect.</p>
{table(None, [("Variance", ""), ("Result", "r"), ("What it says", "")],
 [["<b>Rate</b>", vt(d['lrv']),
   "<b>Favourable overall.</b> The saving on 520 hours of men at " + R + "0.025 below standard ("
   + vt(d['rows'][0]['lrv']) + ") outweighed the small overpayments to women and boys."],
  ["<b>Mix / gang</b>", vt(d['lmv']),
   "<b>Adverse.</b> 13 men instead of 10 &mdash; 120 more man-hours at the highest rate of " + R
   + "0.625, only partly offset by fewer women and boys."],
  ["<b>Idle time</b>", vt(d['litv']),
   "<b>Adverse, and unavoidably so.</b> 40 hours were paid for in which nothing was produced."],
  ["<b>Yield</b>", vt(d['lyv']),
   "<b>Favourable.</b> In the 760 hours actually worked the gang did slightly better than the "
   "standard rate of production."],
  ["<b>Efficiency</b>", vt(d['lev']), "The three above, netted."],
  ["<b>Cost</b>", "<b>" + vt(d['lcv']) + "</b>", "<b>Rate plus efficiency.</b>"]],
 headcls="lite", widths=["13%", "16%", "71%"])}
<p><b>The idle time variance is the single largest adverse item, and it is the useful one.</b> Note
carefully that it is described as <i>abnormal</i> idle time &mdash; a machine breakdown, a power
failure, a material shortage. It is not the workers&rsquo; fault, and it is not the gang leader&rsquo;s
fault. Isolating it in its own variance is precisely so that the production supervisor is not held
answerable for it.</p>
{calc([f'Idle time as a proportion of hours paid &nbsp;=&nbsp; {frac("40 hours", "800 hours")} '
       f'&nbsp;=&nbsp; <b>5% of the payroll</b>',
       f'Cost of that lost time &nbsp;=&nbsp; {vt(d["litv"])}',
       f'Had there been no idle time, LEV would have been {vt(d["lev"] - d["litv"])} instead of '
       f'{vt(d["lev"])}'])}
<p><b>The mix variance carries a real management message.</b> Substituting men for women and boys costs
money at standard rates, because men are the dearest grade. Unless the extra men were genuinely needed,
the gang should be restored to its 10 : 5 : 5 composition &mdash; that alone is worth
{R}{money(abs(d['lmv']), 2)} a week.</p>
<p class="small"><b>And notice what the favourable yield variance tells us:</b> in the hours they
actually worked, the gang was <i>more</i> productive than standard. The problem in this week was not the
workers&rsquo; effort. It was 40 hours of stoppage and an over-expensive gang composition &mdash; both
management matters.</p>""")
            + labour_answer(d, extra=[
                ("Hours &mdash; SH for actual output", "768 hours"),
                ("Hours &mdash; AH paid", "800 hours"),
                ("Hours &mdash; idle &nbsp;(2 per worker &times; 20)", "<b>40 hours</b>"),
                ("Hours &mdash; actually worked", "760 hours")])
            + "</div>")


# ======================================================================
# Q9
# ======================================================================
def q9():
    # gang engaged for 200 hours; 12 of them lost to breakdown -> idle per worker = 12
    # standard output 4 units per hour of the gang -> for 200 std gang-hours, 800 units
    d = labour_engine(
        [dict(n="Skilled", sw=2, sr=20, aw=2, ar=20, hrs=200),
         dict(n="Semi-skilled", sw=4, sr=12, aw=3, ar=14, hrs=200),
         dict(n="Unskilled", sw=4, sr=8, aw=5, ar=10, hrs=200)],
        std_out=800, act_out=810, idle_per_worker=12)
    basic, lcv, lrv, lev, lmv, lyv, litv = labour_tables(d)

    qq = f"""<p>The following was the composition of a gang of workers in a factory during a particular
month, in one of the production departments. The standard composition of workers and wage rate per hour
were as follows:</p>
{table(None, [("Grade", ""), ("Standard composition", ""), ("Standard rate per hour " + R, "r")],
 [["<b>Skilled</b>", "Two workers", "20"], ["<b>Semi-skilled</b>", "Four workers", "12"],
  ["<b>Unskilled</b>", "Four workers", "8"]], headcls="lite", widths=["24%", "40%", "36%"])}
<p>The standard output of the gang was <b>four units per hour</b> of the product. During the month in
question, however, the actual composition of the gang and hourly rates paid were as under:</p>
{table(None, [("Nature of worker", ""), ("No. of workers", "r"),
              ("Wage rate paid per worker per hour " + R, "r")],
 [["<b>Skilled</b>", "2", "20"], ["<b>Semi-skilled</b>", "3", "14"],
  ["<b>Unskilled</b>", "5", "10"]], headcls="lite", widths=["30%", "30%", "40%"])}
<p>The gang was engaged for <b>200 hours</b> during the month, which included <b>12 hours when no
production was possible due to machine break-down</b>. <b>810 units</b> of the product were recorded as
output of the gang during the month.</p>
<p>You are required to compute the Labour Rate, Mix, Idle Time, Yield, Efficiency and Cost Variances,
and to reconcile them.</p>"""

    rd = f"""<p>Same structure as Q8, but the output standard is expressed differently and that is where
the work lies.</p>
{steps([
 '<b>Convert &ldquo;four units per hour of the gang&rdquo; into a standard output.</b> The gang was '
 'engaged for 200 hours, so the standard output for that engagement is 200 &times; 4 = '
 '<b>800 units</b>. Actual output was 810 units &mdash; slightly <b>above</b> standard.',
 '<b>Standard hours of the gang</b> = 10 workers &times; 200 hours = <b>2,000 hours</b> for those '
 '800 units.',
 '<b>SH for the actual output of 810 units</b> = 2,000 &times; ' + frac("810", "800") + ' = '
 '<b>2,025 hours</b>.',
 '<b>AH paid</b> = 10 workers &times; 200 hours = <b>2,000 hours</b>. Idle hours = 10 workers &times; '
 '12 = <b>120 hours</b>, so hours worked = <b>1,880</b>.'])}
{bullets([
 '<b>The gang is again the same size &mdash; 10 workers &mdash; but differently composed:</b> 2 : 3 : 5 '
 'against a standard 2 : 4 : 4. One semi-skilled worker has been replaced by an unskilled one.',
 '<b>Replacing semi-skilled (' + R + '12) with unskilled (' + R + '8) is FAVOURABLE for the mix</b>, '
 'because the cheaper grade was substituted. Expect a favourable mix variance &mdash; the opposite of '
 'Q8.',
 '<b>But look at the rates paid.</b> Semi-skilled were paid ' + R + '14 against a standard ' + R
 + '12, and unskilled ' + R + '10 against ' + R + '8 &mdash; both 2 rupees over. Only the skilled '
 'grade was paid at standard. Expect a firmly <b>adverse rate variance</b>.',
 '<b>810 units in 200 hours is 4.05 units an hour</b> against a standard 4.00 &mdash; and that was '
 'achieved despite losing 12 hours to breakdown. In the 188 productive hours the rate was 4.31 units '
 'an hour. So the gang worked well; expect a favourable yield variance.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q9", "Labour variances with machine breakdown idle time",
                        "Labour &middot; p.81&ndash;82")
            + question(qq) + read(rd)
            + wn(f"""<h4 class="mini">W1 &nbsp;Converting the output standard into hours</h4>
{calc([f'Standard output of the gang &nbsp;=&nbsp; 4 units per hour &times; 200 hours engaged '
       f'&nbsp;=&nbsp; <b>800 units</b>',
       f'Standard gang hours for those 800 units &nbsp;=&nbsp; 10 workers &times; 200 hours '
       f'&nbsp;=&nbsp; <b>2,000 hours</b>',
       f'SH for the actual 810 units &nbsp;=&nbsp; 2,000 &times; {frac("810", "800")} '
       f'&nbsp;=&nbsp; <b>2,025 hours</b>',
       f'AH paid &nbsp;=&nbsp; 10 &times; 200 &nbsp;=&nbsp; <b>2,000 hours</b>',
       f'Idle hours &nbsp;=&nbsp; 10 workers &times; 12 hours &nbsp;=&nbsp; <b>120 hours</b> '
       f'&nbsp;&rarr;&nbsp; hours worked = <b>1,880</b>'])}
<p class="small"><b>Note the direction of travel.</b> The standard allows 2,025 hours for 810 units but
only 2,000 were paid for &mdash; so on hours alone the gang was <b>efficient</b>. The adverse pressure
in this problem comes from the rates paid, not from the hours taken.</p>""")
            + basic + lcv + lrv + lev + lmv + lyv + litv + labour_recon(d)
            + why(f"""<p>The cost variance is <b>{vt(d['lcv'])}</b>, and this problem is the mirror
image of Q8: there the rate variance was favourable and the mix adverse; here the rate variance is
heavily adverse and the mix favourable.</p>
{table(None, [("Variance", ""), ("Result", "r"), ("Cause", "")],
 [["<b>Rate</b>", vt(d['lrv']),
   "<b>The dominant item.</b> Semi-skilled paid " + R + "14 not " + R + "12 ("
   + vt(d['rows'][1]['lrv']) + ") and unskilled " + R + "10 not " + R + "8 ("
   + vt(d['rows'][2]['lrv']) + "). Skilled were at standard, so contributed nothing."],
  ["<b>Mix / gang</b>", vt(d['lmv']),
   "<b>Favourable.</b> One semi-skilled worker at " + R + "12 replaced by an unskilled one at " + R
   + "8 &mdash; 200 hours moved to a cheaper grade."],
  ["<b>Idle time</b>", vt(d['litv']),
   "<b>Adverse.</b> 120 hours paid for during the machine breakdown."],
  ["<b>Yield</b>", vt(d['lyv']),
   "<b>Favourable.</b> 810 units were produced in 1,880 working hours where the standard rate would "
   "have given fewer."],
  ["<b>Efficiency</b>", vt(d['lev']), "Mix + yield + idle time"],
  ["<b>Cost</b>", "<b>" + vt(d['lcv']) + "</b>", "<b>Rate + efficiency</b>"]],
 headcls="lite", widths=["13%", "16%", "71%"])}
<p><b>Two management conclusions, and they point in opposite directions.</b></p>
{steps([
 '<b>The rate variance of ' + vt(d['lrv']) + ' needs explaining.</b> Paying semi-skilled and '
 'unskilled workers ' + R + '2 an hour above standard is a 17% and 25% overrun respectively. Either '
 'the standard rates are out of date &mdash; in which case they must be revised &mdash; or overtime '
 'or a higher grade of worker was used on lower-grade work. Both are worth investigating, and the '
 'answer determines whether anyone is at fault.',
 '<b>The idle time of ' + vt(d['litv']) + ' is a maintenance failure, not a labour failure.</b> '
 '120 hours &mdash; 6% of the payroll &mdash; were paid for during a machine breakdown. That is a '
 'cost of poor plant maintenance and it should be reported to whoever is responsible for the '
 'machine, not to the gang leader.',
 '<b>The gang itself performed well.</b> Mix and yield together are '
 + vt(d['lmv'] + d['lyv']) + ' favourable: a cheaper composition <i>and</i> above-standard '
 'productivity in the hours available. Had the breakdown not occurred, the efficiency variance would '
 'have been ' + vt(d['lev'] - d['litv']) + ' rather than ' + vt(d['lev']) + '.'])}
<p class="small"><b>The point of the whole exercise is visible here.</b> A single cost variance of
{vt(d['lcv'])} would tell management only that labour cost more than planned. The decomposition tells
them that the workforce did well, the maintenance department did badly, and the wage rates in the
standard are probably obsolete &mdash; three different actions for three different people.</p>""")
            + labour_answer(d, extra=[
                ("Standard output &nbsp;(4 units/hr &times; 200 hrs)", "800 units"),
                ("Actual output", "810 units"),
                ("SH for actual output", "2,025 hours"),
                ("AH paid / idle / worked", "2,000 / <b>120</b> / 1,880 hours")])
            + "</div>")


# ======================================================================
# Q10
# ======================================================================
def q10():
    # 200 working hours, 15 idle; standard output 50 units per hour of the gang
    d = labour_engine(
        [dict(n="Skilled", sw=30, sr=5.0, aw=24, ar=6.0, hrs=200),
         dict(n="Semi-skilled", sw=10, sr=3.0, aw=15, ar=2.5, hrs=200),
         dict(n="Unskilled", sw=10, sr=2.0, aw=12, ar=2.0, hrs=200)],
        std_out=10000, act_out=9600, idle_per_worker=15)
    basic, lcv, lrv, lev, lmv, lyv, litv = labour_tables(d)

    qq = f"""<p>The standard labour complement and the actual labour complement engaged during the month
are given below:</p>
{table(None, [("Particulars", ""), ("Skilled", "r"), ("Semi-skilled", "r"), ("Unskilled", "r")],
 [["Standard number of workers in a group", "30", "10", "10"],
  ["Standard wage rate per hour " + R, "5", "3", "2"],
  ["Actual number of workers employed during the month in the group", "24", "15", "12"],
  ["Actual wage rate per hour " + R, "6", "2.50", "2"]], headcls="lite",
 widths=["46%", "18%", "18%", "18%"])}
<p>During the month of <b>200 working hours</b> (which included <b>15 hours when no production was
possible due to machine break-down</b>), the group produced <b>9,600 units</b>. Standard output of the
gang was <b>50 units per hour</b>.</p>
<p>Calculate all the labour variances and reconcile them.</p>"""

    rd = f"""<p>The largest gang in the module &mdash; 50 standard workers against 51 actual &mdash; so
the arithmetic is bigger but the method is identical.</p>
{steps([
 '<b>Standard output</b> = 50 units per hour &times; 200 hours = <b>10,000 units</b>. Actual output '
 'was 9,600 units, so output was <b>4% short of standard</b>.',
 '<b>Standard gang hours</b> = (30 + 10 + 10) = 50 workers &times; 200 hours = '
 '<b>10,000 hours</b> for those 10,000 units &mdash; conveniently one hour per unit.',
 '<b>SH for the actual 9,600 units</b> = 10,000 &times; ' + frac("9,600", "10,000") + ' = '
 '<b>9,600 hours</b>.',
 '<b>AH paid</b> = (24 + 15 + 12) = 51 workers &times; 200 = <b>10,200 hours</b>. Idle hours = '
 '51 &times; 15 = <b>765 hours</b>, so hours worked = <b>9,435</b>.'])}
{bullets([
 '<b>This gang is BIGGER than standard</b> &mdash; 51 workers instead of 50, and 10,200 hours paid '
 'against 9,600 allowed. So unlike Q8 and Q9 there is a genuine capacity difference as well as a '
 'composition difference.',
 '<b>The composition shifted away from skilled labour:</b> 24 skilled instead of 30, but 15 '
 'semi-skilled instead of 10 and 12 unskilled instead of 10. Fewer of the dearest grade at ' + R
 + '5 and more of the cheaper grades &mdash; expect a <b>favourable mix variance</b>.',
 '<b>Skilled workers were paid ' + R + '6 against a standard ' + R + '5</b>, a 20% overrun on the '
 'dearest grade. Semi-skilled were paid ' + R + '0.50 <i>below</i> standard and unskilled exactly at '
 'standard.',
 '<b>Output fell 4% short while hours paid ran 6% over.</b> That combination guarantees a substantial '
 'adverse efficiency variance.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q10", "Labour variances for a fifty-worker gang",
                        "Labour &middot; p.82")
            + question(qq) + read(rd)
            + wn(f"""<h4 class="mini">W1 &nbsp;The four hour figures</h4>
{calc([f'Standard output &nbsp;=&nbsp; 50 units per hour &times; 200 hours &nbsp;=&nbsp; '
       f'<b>10,000 units</b>',
       f'Standard gang hours &nbsp;=&nbsp; 50 workers &times; 200 hours &nbsp;=&nbsp; '
       f'<b>10,000 hours</b>',
       f'SH for the actual 9,600 units &nbsp;=&nbsp; 10,000 &times; {frac("9,600", "10,000")} '
       f'&nbsp;=&nbsp; <b>9,600 hours</b>',
       f'AH paid &nbsp;=&nbsp; 51 workers &times; 200 hours &nbsp;=&nbsp; <b>10,200 hours</b>',
       f'Idle hours &nbsp;=&nbsp; 51 workers &times; 15 hours &nbsp;=&nbsp; <b>765 hours</b> '
       f'&nbsp;&rarr;&nbsp; hours worked = <b>9,435</b>'])}""")
            + basic + lcv + lrv + lev + lmv + lyv + litv + labour_recon(d)
            + why(f"""<p>The cost variance is <b>{vt(d['lcv'])}</b>. This is the most instructive of the
three labour problems because the mix variance and the yield variance point in <b>opposite</b>
directions, and the reason is a real operational trade-off.</p>
{table(None, [("Variance", ""), ("Result", "r"), ("What happened", "")],
 [["<b>Rate</b>", vt(d['lrv']),
   "Skilled paid " + R + "6 not " + R + "5 on 4,800 hours (" + vt(d['rows'][0]['lrv'])
   + "), partly recovered by paying semi-skilled " + R + "0.50 below standard ("
   + vt(d['rows'][1]['lrv']) + ")."],
  ["<b>Mix / gang</b>", vt(d['lmv']),
   "<b>Favourable.</b> Six skilled workers at " + R + "5 replaced by five semi-skilled at " + R
   + "3 and two unskilled at " + R + "2 &mdash; a cheaper gang."],
  ["<b>Idle time</b>", vt(d['litv']),
   "<b>Adverse.</b> 765 hours paid for during the breakdown &mdash; 7.5% of the payroll."],
  ["<b>Yield</b>", vt(d['lyv']),
   "<b>Favourable.</b> In the 9,435 hours actually worked the gang produced 9,600 units &mdash; "
   "slightly better than the standard rate of production."],
  ["<b>Efficiency</b>", vt(d['lev']), "Mix + yield + idle time"],
  ["<b>Cost</b>", "<b>" + vt(d['lcv']) + "</b>", "<b>Rate + efficiency</b>"]],
 headcls="lite", widths=["13%", "16%", "71%"])}
<p><b>The de-skilling worked.</b> Management took six skilled workers out and put in five semi-skilled
and two unskilled. Mix and yield together come to {vt(d['lmv'] + d['lyv'])} favourable &mdash; the gang
was made cheaper <i>and</i> it held its productivity.</p>
{calc([f'Favourable mix variance from the cheaper gang &nbsp;=&nbsp; {vt(d["lmv"])}',
       f'Favourable yield variance from productivity in the hours worked &nbsp;=&nbsp; '
       f'{vt(d["lyv"])}',
       f'<b>Net gain from the de-skilling decision &nbsp;=&nbsp; '
       f'{vt(d["lmv"] + d["lyv"])}</b>'])}
<p><b>So why is the cost variance {vt(d['lcv'])}?</b> Because of two things that have nothing to do with
the gang&rsquo;s composition or its effort:</p>
{steps([
 '<b>765 hours of machine breakdown, costing ' + vt(d['litv']) + '.</b> That is equivalent to nearly '
 'four workers being paid to do nothing for the whole month. It is a <b>maintenance</b> failure and '
 'must be reported as such, not charged against the gang.',
 '<b>Skilled workers paid ' + R + '6 an hour against a standard ' + R + '5, costing '
 + vt(d['rows'][0]['lrv']) + '.</b> A 20% overrun on every one of 4,800 skilled hours, partly '
 'recovered by paying semi-skilled ' + R + '0.50 below standard (' + vt(d['rows'][1]['lrv'])
 + '), giving a net rate variance of ' + vt(d['lrv']) + '.'])}
<p>Those two items together are {vt(d['litv'] + d['lrv'])} adverse, against
{vt(d['lmv'] + d['lyv'])} favourable from the gang itself. <b>That is the finding to report: the
workforce performed well and was let down by plant breakdown and by wage rates that no longer match the
standard.</b></p>
<div class="blk trap" style="margin-top:3mm"><span class="lab">A subtlety worth the extra mark</span>
<p>The gang used <b>more hours in total</b> than the standard allows &mdash; 10,200 paid against 9,600
allowed for the output achieved, 600 hours over &mdash; and yet the efficiency variance is
<b>{vt(d['lev'])} favourable</b>. That is not a contradiction. The hours <i>saved</i> were in the
expensive skilled grade and the hours <i>overspent</i> were in the cheap grades:</p>
{table(None, [("Grade", ""), ("SH allowed", "r"), ("AH used", "r"), ("Difference", "r"),
              ("SR " + R, "r"), ("Money effect", "r")],
 [[f"<b>{r['n']}</b>", q(r["sh"]), q(r["ah"]), num(r["sh"] - r["ah"]),
   money(r["sr"], 2), vt(r["lev"])] for r in d["rows"]]
 + [{"cls": "tot", "cells": ["<b>Total</b>", "<b>9,600</b>", "<b>10,200</b>", "<b>(600)</b>", "",
                             "<b>" + vt(d["lev"]) + "</b>"]}], headcls="lite",
 widths=["20%", "14%", "14%", "15%", "12%", "25%"])}
<p>960 skilled hours were saved at {R}5 each, which is worth more than the 1,560 cheap hours added at
{R}3 and {R}2. <b>Counting hours and counting money give opposite answers, and money is the one that
matters.</b> This is the best illustration in the module of why variances are expressed in rupees rather
than in hours.</p>
</div>""")
            + labour_answer(d, extra=[
                ("Standard output &nbsp;(50 units/hr &times; 200 hrs)", "10,000 units"),
                ("Actual output", "9,600 units"),
                ("SH for actual output", "9,600 hours"),
                ("AH paid / idle / worked", "10,200 / <b>765</b> / 9,435 hours"),
                ("Workers &mdash; standard vs actual", "50 vs 51")])
            + "</div>")



# ======================================================================
# VARIABLE OVERHEAD ENGINE  -  Q11, Q12, Q13
# ======================================================================
def voh_engine(bud_units, bud_voh, std_hrs_per_unit, act_units, act_voh,
               act_hours, idle_hours=0.0):
    bh = bud_units * std_hrs_per_unit
    sr = bud_voh / bh
    sh = act_units * std_hrs_per_unit
    worked = act_hours - idle_hours
    d = dict(bh=bh, sr=sr, sh=sh, ah=act_hours, worked=worked, idle=idle_hours,
             bud_units=bud_units, bud_voh=bud_voh, act_units=act_units, act_voh=act_voh,
             std_hrs_per_unit=std_hrs_per_unit)
    d["sc"] = sh * sr
    d["vocv"] = d["sc"] - act_voh
    d["exp"] = act_hours * sr - act_voh                 # on TOTAL actual hours
    d["idlev"] = -idle_hours * sr                       # always adverse
    d["eff"] = sr * (sh - worked)                       # on PRODUCTIVE hours
    return d


def voh_tables(d, cur=None):
    cur = cur or R
    has_idle = d["idle"] > 0
    basis = table("Basic Calculation",
      [("Particulars", ""), ("Computation", ""), ("Amount", "r")],
      [["Budgeted hours (BH)", f"{q(d['bud_units'])} units &times; {q(d['std_hrs_per_unit'])} hours",
        f"<b>{q(d['bh'])} hours</b>"],
       ["<b>Standard variable overhead rate (SR)</b>",
        frac(f"budgeted VOH {cur}{money(d['bud_voh'])}", f"budgeted hours {q(d['bh'])}"),
        f"<b>{cur}{money(d['sr'], 2)} per hour</b>"],
       ["Standard hours for actual output (SH)",
        f"{q(d['act_units'])} units &times; {q(d['std_hrs_per_unit'])} hours",
        f"<b>{q(d['sh'])} hours</b>"],
       ["Actual hours (AH)", "given", f"<b>{q(d['ah'])} hours</b>"]]
      + ([["<i>of which</i> abnormal idle time", "given",
           f"<b>{q(d['idle'])} hours</b>"],
          ["<b>Productive hours worked</b>", f"{q(d['ah'])} &minus; {q(d['idle'])}",
           f"<b>{q(d['worked'])} hours</b>"]] if has_idle else [])
      + [{"cls": "tot",
          "cells": ["<b>Standard variable overhead for actual output (SC)</b>",
                    f"{q(d['sh'])} hours &times; {cur}{money(d['sr'], 2)}",
                    f"<b>{cur}{money(d['sc'])}</b>"]},
         {"cls": "sub", "cells": ["<b>Actual variable overhead</b>", "given",
                                  f"<b>{cur}{money(d['act_voh'])}</b>"]}],
      headcls="lite", widths=["38%", "37%", "25%"])

    rows = [["<b>1. Variable Overhead Cost Variance</b><br/>"
             + src("SC &minus; Actual VOH"),
             f"{cur}{money(d['sc'])} &minus; {cur}{money(d['act_voh'])}",
             (f"<b>{vt(d['vocv'])}</b>", "r")],
            ["<b>2. VO Expenditure (Spending) Variance</b><br/>"
             + src("(AH &times; SR) &minus; Actual VOH"),
             f"({q(d['ah'])} &times; {money(d['sr'], 2)}) &minus; {money(d['act_voh'])} "
             f"= {money(d['ah'] * d['sr'])} &minus; {money(d['act_voh'])}",
             (f"<b>{vt(d['exp'])}</b>", "r")]]
    if has_idle:
        rows.append(["<b>3. VO Idle Time Variance</b><br/>"
                     + src("Idle hours &times; SR &mdash; always adverse"),
                     f"{q(d['idle'])} hours &times; {money(d['sr'], 2)}",
                     (f"<b>{vt(d['idlev'])}</b>", "r")])
    rows.append([f"<b>{4 if has_idle else 3}. VO Efficiency Variance</b><br/>"
                 + src("SR &times; (SH &minus; "
                       + ("productive hours)" if has_idle else "AH)")),
                 f"{money(d['sr'], 2)} &times; ({q(d['sh'])} &minus; "
                 f"{q(d['worked'])})",
                 (f"<b>{vt(d['eff'])}</b>", "r")])
    var = table("The variable overhead variances",
      [("Variance", ""), ("Working", ""), ("Result", "r")], rows,
      headcls="lite", widths=["34%", "42%", "24%"])

    parts = [d["exp"], d["eff"]] + ([d["idlev"]] if has_idle else [])
    lbl = "VOCV = Expenditure + Idle time + Efficiency" if has_idle \
        else "VOCV = Expenditure + Efficiency"
    work = " &nbsp;+&nbsp; ".join(
        [vt(d["exp"])] + ([vt(d["idlev"])] if has_idle else []) + [vt(d["eff"])])
    recon = table("Reconciliation",
      [("Identity", ""), ("Working", ""), ("Result", "r")],
      [{"cls": "recon", "cells": [f"<b>{lbl}</b>", work,
                                  f"<b>{vt(sum(parts))}</b>"]},
       {"cls": "recon", "cells": ["&nbsp;&nbsp;&nbsp;<i>and VOCV computed directly was</i>", "",
                                  f"<b>{vt(d['vocv'])}</b> &nbsp;&#10003;"]}],
      headcls="lite", widths=["34%", "42%", "24%"])
    return basis, var, recon


# ======================================================================
# Q11
# ======================================================================
def q11():
    d = voh_engine(600, 15600, 20, 500, 14000, 9000)
    basis, var, recon = voh_tables(d)

    qq = f"""<p>Following information is obtained from M/s Will and Urvish Co. Ltd.</p>
{table(None, [("Particulars", ""), ("Amount", "r")],
 [["Budgeted production for the period", "600 units"],
  ["Budgeted variable overhead", R + "15,600"],
  ["Standard time for one unit", "20 hours"],
  ["Actual production for the period", "500 units"],
  ["Actual variable overhead", R + "14,000"],
  ["Actual hours worked", "9,000"]], headcls="lite", widths=["64%", "36%"])}
<p>Calculate: <b>(a)</b> Variable overhead expenditure variance <b>(b)</b> Variable overhead efficiency
variance <b>(c)</b> Variable overhead variance. You are also required to reconcile the same.</p>"""

    rd = f"""<p>Variable overhead is the easiest of the four cost families, because it has only
<b>two</b> branches. But the standard rate must be derived first, and it must be derived <b>per hour</b>,
not per unit.</p>
{steps([
 '<b>Budgeted hours</b> = 600 units &times; 20 hours = <b>12,000 hours</b>.',
 '<b>Standard rate</b> = ' + frac(R + "15,600", "12,000 hours") + ' = <b>' + R
 + '1.30 per hour</b>. This is the figure every later step uses.',
 '<b>Standard hours for the ACTUAL output</b> = 500 units &times; 20 hours = <b>10,000 hours</b>. '
 'Note this is not the 12,000 budgeted hours &mdash; output fell short, so fewer hours are allowed.',
 '<b>Then the two variances</b>, and the reconciliation.'])}
{bullets([
 '<b>Actual hours of 9,000 against 10,000 allowed for the output achieved.</b> The company produced '
 '500 units in 9,000 hours where the standard permits 10,000 &mdash; so it was <b>efficient</b>, and '
 'the efficiency variance will be favourable.',
 '<b>But actual overhead of ' + R + '14,000 against ' + R + '11,700 that 9,000 hours should have '
 'cost.</b> Spending per hour was far above standard, so the expenditure variance will be adverse '
 'and larger.',
 '<b>No idle time is mentioned</b>, so there are only two branches. Q12 adds the third.'])}"""

    return ("<div class='prob'>"
            + prob_head("Q11", "Variable overhead variances &mdash; the two-branch case",
                        "Variable overhead &middot; p.82&ndash;83")
            + question(qq) + read(rd) + basis + var + recon
            + why(f"""<p>The two variances point in opposite directions, and that is the whole
information content of the answer.</p>
{table(None, [("", ""), ("Result", "r"), ("Meaning", "")],
 [["<b>Efficiency</b>", vt(d['eff']),
   "<b>Good.</b> 500 units were made in 9,000 hours where the standard allows 10,000 &mdash; the "
   "factory saved 1,000 hours, worth " + R + "1.30 each."],
  ["<b>Expenditure</b>", vt(d['exp']),
   "<b>Bad, and worse.</b> Those 9,000 hours should have carried " + R
   + money(9000 * d['sr']) + " of variable overhead but actually carried " + R + "14,000 - "
   + R + money(14000 / 9000, 2) + " an hour instead of " + R + "1.30."],
  {"cls": "tot", "cells": ["<b>Cost variance</b>", "<b>" + vt(d['vocv']) + "</b>",
                           "<b>The overspend outweighed the time saved.</b>"]}],
 headcls="lite", widths=["16%", "18%", "66%"])}
{calc([f'Actual variable overhead per hour &nbsp;=&nbsp; '
       f'{frac(R + "14,000", "9,000 hours")} &nbsp;=&nbsp; <b>{R}{money(14000/9000, 4)}</b>',
       f'Standard variable overhead per hour &nbsp;=&nbsp; <b>{R}1.30</b>',
       f'Overspend per hour &nbsp;=&nbsp; <b>{R}{money(14000/9000 - 1.30, 4)}</b> '
       f'&nbsp;&rarr;&nbsp; {R}{money(14000/9000 - 1.30, 4)} &times; 9,000 hours = '
       f'{vt(d["exp"])}'])}
<p><b>What to report to management.</b> The production department worked efficiently &mdash; it used
1,000 fewer hours than the standard allows &mdash; and should be told so. The problem is entirely on the
spending side: variable overhead cost {R}{money(14000/9000 - 1.30, 2)} an hour more than it should have.
Since variable overhead means power, consumables, indirect materials and the like, the investigation
should look at prices and at consumption per hour, <b>not</b> at the workforce.</p>
<p class="small"><b>A subtlety worth noticing.</b> There is a possible connection: working faster often
means running machines harder, which consumes more power and more consumables per hour. If so, part of
the {vt(d['exp'])} is the price of the {vt(d['eff'])} &mdash; and the net {vt(d['vocv'])} says the
trade was not worth making. Whether that is the explanation can only be settled by investigation, but
raising the question is what a real answer does.</p>""")
            + ans([("Budgeted hours &nbsp;(600 &times; 20)", "12,000 hours"),
                   ("Standard rate &nbsp;(15,600 &divide; 12,000)", f"{R} 1.30 per hour"),
                   ("Standard hours for actual output &nbsp;(500 &times; 20)", "10,000 hours"),
                   ("Standard VOH for actual output", f"{R} {money(d['sc'])}"),
                   ("Actual VOH", f"{R} {money(d['act_voh'])}"),
                   ("<b>(a) VO Expenditure Variance</b>", f"<b>{vt(d['exp'])}</b>"),
                   ("<b>(b) VO Efficiency Variance</b>", f"<b>{vt(d['eff'])}</b>"),
                   ("<b>(c) VO Cost Variance</b>", f"<b>{vt(d['vocv'])}</b>"),
                   ("Reconciliation", "Expenditure + Efficiency = Cost &nbsp;&#10003;")])
            + "</div>")


# ======================================================================
# Q12
# ======================================================================
def q12():
    d = voh_engine(300, 7800, 20, 250, 7000, 4500, idle_hours=300)
    basis, var, recon = voh_tables(d)

    qq = f"""<p>From the following information pertaining to January, calculate the overhead
variances:</p>
{table(None, [("Particulars", ""), ("Production in units", "r"), ("Variable overheads " + R, "r"),
              ("Hours worked", "r")],
 [["<b>Budgeted</b>", "300", "7,800", "<i>see Note 1</i>"],
  ["<b>Actual</b>", "250", "7,000", "4,500 <i>see Note 2</i>"]], headcls="lite")}
{bullets(['<b>Note 1:</b> Standard time for 1 unit is 20 hours.',
          '<b>Note 2:</b> This includes <b>300 hours of abnormal idle time</b>.'])}"""

    rd = f"""<p>Q11 with one addition: <b>abnormal idle time</b>. That turns the two-branch analysis into
three branches, and the way the three fit together needs care.</p>
{steps([
 '<b>Budgeted hours</b> = 300 units &times; 20 hours = <b>6,000 hours</b>; standard rate = '
 + frac(R + "7,800", "6,000") + ' = <b>' + R + '1.30 per hour</b>.',
 '<b>Standard hours for actual output</b> = 250 units &times; 20 = <b>5,000 hours</b>.',
 '<b>Separate the actual hours.</b> 4,500 hours were paid for, of which 300 were abnormal idle time, '
 'so <b>4,200 hours were productive</b>.',
 '<b>Use the two figures in different places</b> &mdash; and this is the point of the problem:'
 + bullets([
     '<b>Expenditure variance uses the TOTAL 4,500 hours</b>, because overhead was incurred on all '
     'of them.',
     '<b>Efficiency variance uses the PRODUCTIVE 4,200 hours</b>, because efficiency means output '
     'per hour actually worked.',
     '<b>Idle time variance bridges the gap</b> &mdash; 300 hours &times; ' + R + '1.30.'])])}
{bullets([
 '<b>If you use the same hours figure in both places the reconciliation still closes</b>, but the '
 'idle-time variance then has nowhere to go and the analysis loses its whole point. Use 4,500 for '
 'expenditure and 4,200 for efficiency.',
 '<b>250 units in 4,200 productive hours</b> is 16.8 hours a unit against a standard 20 &mdash; so '
 'the workforce was efficient once it had work to do.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q12", "Variable overhead variances with abnormal idle time",
                        "Variable overhead &middot; p.83")
            + question(qq) + read(rd) + basis + var + recon
            + why(f"""<p>The total variance of {vt(d['vocv'])} looks trivial. The decomposition shows
that it is the net of three substantial and quite different effects.</p>
{table(None, [("Variance", ""), ("Result", "r"), ("Whose responsibility", ""), ("Action", "")],
 [["<b>Expenditure</b>", vt(d['exp']),
   "The department controlling overhead spending",
   "4,500 hours should have carried " + R + money(4500 * d['sr']) + " but carried " + R
   + "7,000 - investigate prices and consumption"],
  ["<b>Idle time</b>", vt(d['idlev']),
   "Maintenance / production planning",
   "300 hours - 6.7% of the total - were paid for with nothing produced"],
  ["<b>Efficiency</b>", vt(d['eff']),
   "The workforce - <b>credit due</b>",
   "250 units in 4,200 hours = 16.8 hours a unit against a standard 20"],
  {"cls": "tot", "cells": ["<b>Cost variance</b>", "<b>" + vt(d['vocv']) + "</b>", "",
                           "<b>the three above, netted</b>"]}],
 headcls="lite", widths=["15%", "15%", "24%", "46%"])}
<p><b>This is the clearest illustration in the module of why variances are decomposed at all.</b> A
manager told only that variable overhead was {R}500 over budget would reasonably conclude that nothing
much had happened. In fact:</p>
{calc([f'Overhead was overspent by {vt(d["exp"])} &mdash; {abs(d["exp"])/d["act_voh"]*100:.0f}% of the '
       f'actual overhead incurred',
       f'A further {vt(d["idlev"])} was wasted on 300 idle hours',
       f'And the workforce <b>earned back</b> {vt(d["eff"])} by working faster than standard',
       f'<b>Net: {vt(d["vocv"])}</b> &mdash; which conceals all three'])}
<p><b>Recommendation:</b> the {vt(d['exp'])} expenditure variance is the priority &mdash; actual
variable overhead ran at {R}{money(7000/4500, 4)} an hour against a standard {R}1.30, an overrun of
{(7000/4500)/1.30*100 - 100:.0f}%. Then address the 300 hours of abnormal idle time. And tell the
production team that their efficiency saved {R}{money(abs(d['eff']))}, because a variance report that
only ever reports bad news stops being read.</p>""")
            + ans([("Budgeted hours &nbsp;(300 &times; 20)", "6,000 hours"),
                   ("Standard rate &nbsp;(7,800 &divide; 6,000)", f"{R} 1.30 per hour"),
                   ("Standard hours for actual output &nbsp;(250 &times; 20)", "5,000 hours"),
                   ("Actual hours &mdash; total / idle / productive",
                    "4,500 / <b>300</b> / 4,200 hours"),
                   ("Standard VOH for actual output", f"{R} {money(d['sc'])}"),
                   ("<b>VO Expenditure Variance</b>", f"<b>{vt(d['exp'])}</b>"),
                   ("<b>VO Idle Time Variance</b>", f"<b>{vt(d['idlev'])}</b>"),
                   ("<b>VO Efficiency Variance</b>", f"<b>{vt(d['eff'])}</b>"),
                   ("<b>VO Cost Variance</b>", f"<b>{vt(d['vocv'])}</b>"),
                   ("Reconciliation",
                    "Expenditure + Idle time + Efficiency = Cost &nbsp;&#10003;")])
            + "</div>")


# ======================================================================
# Q13
# ======================================================================
def q13():
    d = voh_engine(400, 10000, 8000 / 400, 360, 9150, 7000)
    basis, var, recon = voh_tables(d)

    qq = f"""<p>The following data is given. Calculate variable overhead variances.</p>
{table(None, [("Particulars", ""), ("Production in units", "r"),
              ("Man hours to produce the output", "r"), ("Variable overheads " + R, "r")],
 [["<b>Budgeted</b>", "400", "8,000", "10,000"],
  ["<b>Actual</b>", "360", "7,000", "9,150"]], headcls="lite")}"""

    rd = f"""<p>Here the standard time per unit is <b>not stated</b> &mdash; it must be derived from the
budget, and that is the only real step.</p>
{steps([
 '<b>Standard time per unit</b> = ' + frac("8,000 budgeted hours", "400 budgeted units")
 + ' = <b>20 hours per unit</b>.',
 '<b>Standard rate per hour</b> = ' + frac(R + "10,000", "8,000 hours") + ' = <b>' + R
 + '1.25 per hour</b>.',
 '<b>Standard hours for the actual output</b> = 360 units &times; 20 hours = <b>7,200 hours</b>.',
 '<b>Then the two variances</b>, on 7,000 actual hours.'])}
{bullets([
 '<b>Do not use the ' + R + '25 per unit figure</b> (10,000 &divide; 400) as a rate. Variable '
 'overhead variances are computed <b>per hour</b>, because that is the basis on which variable '
 'overhead is assumed to vary. Per-unit rates give the right cost variance but the wrong split.',
 '<b>7,000 actual hours against 7,200 allowed</b> for the output achieved &mdash; so 200 hours were '
 'saved and the efficiency variance is favourable.',
 '<b>' + R + '9,150 of actual overhead against ' + R + '8,750 that 7,000 hours should have cost</b> '
 '&mdash; so the expenditure variance is adverse and slightly larger.',
 'No idle time is given, so two branches again.'])}"""

    return ("<div class='prob'>"
            + prob_head("Q13", "Variable overhead variances when the standard time must be derived",
                        "Variable overhead &middot; p.83")
            + question(qq) + read(rd) + basis + var + recon
            + why(f"""<p>The pattern is the same as Q11 and Q13 is the smallest of the three in
magnitude: a cost variance of only {vt(d['vocv'])} on {R}9,150 of actual overhead, which is a
{abs(d['vocv'])/d['act_voh']*100:.1f}% overrun.</p>
{calc([f'Efficiency &nbsp;=&nbsp; {R}1.25 &times; (7,200 &minus; 7,000) &nbsp;=&nbsp; '
       f'{vt(d["eff"])} &nbsp;&mdash;&nbsp; 200 hours saved',
       f'Expenditure &nbsp;=&nbsp; (7,000 &times; {R}1.25) &minus; {R}9,150 &nbsp;=&nbsp; '
       f'{R}8,750 &minus; {R}9,150 &nbsp;=&nbsp; {vt(d["exp"])}',
       f'<b>Net &nbsp;=&nbsp; {vt(d["vocv"])}</b>'])}
<p><b>Two observations for the marks.</b></p>
{bullets([
 '<b>Actual overhead per hour was ' + R + money(9150/7000, 4) + ' against a standard ' + R
 + '1.25</b> &mdash; an overrun of ' + f'{(9150/7000)/1.25*100 - 100:.1f}' + '%. Small in '
 'percentage terms, which is why the expenditure variance is modest.',
 '<b>The output shortfall does NOT of itself create an adverse variance.</b> Production was 360 units '
 'against 400 budgeted &mdash; a 10% shortfall &mdash; yet the variances are almost nil. That is '
 'because variable overhead is <i>flexed</i>: the standard allowed is 7,200 hours for 360 units, not '
 'the 8,000 budgeted for 400. This is the flexible budget of Module 5 doing its work inside a '
 'standard costing system, and saying so links the two modules.'])}
<p><b>Recommendation:</b> variable overhead was essentially under control. Note the favourable
efficiency variance of {vt(d['eff'])} and the small adverse expenditure variance of {vt(d['exp'])};
neither warrants investigation on its own, but if the expenditure variance recurs month after month the
standard rate of {R}1.25 an hour should be reviewed.</p>""")
            + ans([("Standard time per unit &nbsp;(8,000 &divide; 400)", "20 hours"),
                   ("Standard rate &nbsp;(10,000 &divide; 8,000)", f"{R} 1.25 per hour"),
                   ("Standard hours for actual output &nbsp;(360 &times; 20)", "7,200 hours"),
                   ("Standard VOH for actual output", f"{R} {money(d['sc'])}"),
                   ("Actual VOH", f"{R} {money(d['act_voh'])}"),
                   ("<b>VO Expenditure Variance</b>", f"<b>{vt(d['exp'])}</b>"),
                   ("<b>VO Efficiency Variance</b>", f"<b>{vt(d['eff'])}</b>"),
                   ("<b>VO Cost Variance</b>", f"<b>{vt(d['vocv'])}</b>"),
                   ("Reconciliation", "Expenditure + Efficiency = Cost &nbsp;&#10003;")])
            + "</div>")



# ======================================================================
# FIXED OVERHEAD ENGINE  -  Q14, Q15
# ======================================================================
def foh_engine(bud_foh, bud_hours, bud_units, act_foh, act_hours, act_units,
               bud_days=None, act_days=None):
    sr = bud_foh / bud_hours                       # per hour
    std_hrs_per_unit = bud_hours / bud_units
    sh = act_units * std_hrs_per_unit              # standard hours for ACTUAL output
    d = dict(sr=sr, bh=bud_hours, sh=sh, ah=act_hours, bud_foh=bud_foh, act_foh=act_foh,
             bud_units=bud_units, act_units=act_units, std_hrs_per_unit=std_hrs_per_unit,
             bud_days=bud_days, act_days=act_days)
    d["sc"] = sh * sr
    d["focv"] = d["sc"] - act_foh
    d["exp"] = bud_foh - act_foh                   # expenditure / spending variance
    d["vol"] = sr * (sh - bud_hours)               # volume variance
    if bud_days and act_days:
        d["rsh"] = bud_hours * (act_days / bud_days)   # revised standard hours
        d["cal"] = sr * (d["rsh"] - bud_hours)
        d["cap"] = sr * (act_hours - d["rsh"])
    else:
        d["rsh"] = None
        d["cal"] = None
        d["cap"] = sr * (act_hours - bud_hours)
    d["eff"] = sr * (sh - act_hours)
    return d


def foh_tables(d, cur=None):
    cur = cur or R
    has_cal = d["cal"] is not None
    rows = [["Budgeted hours (BH)", "given / derived", f"<b>{q(d['bh'])} hours</b>"],
            ["<b>Standard fixed overhead rate (SR)</b>",
             frac(f"budgeted FOH {cur}{money(d['bud_foh'])}", f"budgeted hours {q(d['bh'])}"),
             f"<b>{cur}{money(d['sr'], 2)} per hour</b>"],
            ["Standard hours per unit", frac(q(d['bh']) + " hours", q(d['bud_units']) + " units"),
             f"<b>{q(d['std_hrs_per_unit'], 2)} hours</b>"],
            ["<b>Standard hours for actual output (SH)</b>",
             f"{q(d['act_units'])} units &times; {q(d['std_hrs_per_unit'], 2)} hours",
             f"<b>{q(d['sh'])} hours</b>"],
            ["Actual hours (AH)", "given", f"<b>{q(d['ah'])} hours</b>"]]
    if has_cal:
        rows.append(["<b>Revised standard hours (RSH)</b>",
                     f"{q(d['bh'])} &times; {frac(q(d['act_days']) + ' actual days', q(d['bud_days']) + ' budgeted days')}",
                     f"<b>{q(d['rsh'])} hours</b>"])
    rows += [{"cls": "tot",
              "cells": ["<b>Standard fixed overhead for actual output (SC)</b>",
                        f"{q(d['sh'])} hours &times; {cur}{money(d['sr'], 2)}",
                        f"<b>{cur}{money(d['sc'])}</b>"]},
             {"cls": "sub", "cells": ["<b>Actual fixed overhead</b>", "given",
                                      f"<b>{cur}{money(d['act_foh'])}</b>"]}]
    basis = table("Basic Calculation", [("Particulars", ""), ("Computation", ""), ("Amount", "r")],
                  rows, headcls="lite", widths=["36%", "38%", "26%"])

    var = table("The fixed overhead variances",
      [("Variance", ""), ("Working", ""), ("Result", "r")],
      [["<b>1. Fixed Overhead Cost Variance</b><br/>" + src("SC &minus; Actual FOH"),
        f"{cur}{money(d['sc'])} &minus; {cur}{money(d['act_foh'])}",
        (f"<b>{vt(d['focv'])}</b>", "r")],
       ["<b>2. FO Expenditure Variance</b><br/>" + src("Budgeted FOH &minus; Actual FOH"),
        f"{cur}{money(d['bud_foh'])} &minus; {cur}{money(d['act_foh'])}",
        (f"<b>{vt(d['exp'])}</b>", "r")],
       ["<b>3. FO Volume Variance</b><br/>" + src("SR &times; (SH &minus; BH)"),
        f"{money(d['sr'], 2)} &times; ({q(d['sh'])} &minus; {q(d['bh'])})",
        (f"<b>{vt(d['vol'])}</b>", "r")]],
      headcls="lite", widths=["32%", "42%", "26%"])

    sub_rows = []
    if has_cal:
        sub_rows.append(["<b>3a. Calendar Variance</b><br/>" + src("SR &times; (RSH &minus; BH)"),
                         f"{money(d['sr'], 2)} &times; ({q(d['rsh'])} &minus; {q(d['bh'])})",
                         (f"<b>{vt(d['cal'])}</b>", "r")])
        sub_rows.append(["<b>3b. Capacity Variance</b><br/>" + src("SR &times; (AH &minus; RSH)"),
                         f"{money(d['sr'], 2)} &times; ({q(d['ah'])} &minus; {q(d['rsh'])})",
                         (f"<b>{vt(d['cap'])}</b>", "r")])
    else:
        sub_rows.append(["<b>3a. Capacity Variance</b><br/>" + src("SR &times; (AH &minus; BH)"),
                         f"{money(d['sr'], 2)} &times; ({q(d['ah'])} &minus; {q(d['bh'])})",
                         (f"<b>{vt(d['cap'])}</b>", "r")])
    sub_rows.append([f"<b>3{'c' if has_cal else 'b'}. Efficiency Variance</b><br/>"
                     + src("SR &times; (SH &minus; AH)"),
                     f"{money(d['sr'], 2)} &times; ({q(d['sh'])} &minus; {q(d['ah'])})",
                     (f"<b>{vt(d['eff'])}</b>", "r")])
    sub = table("Analysis of the volume variance", [("Variance", ""), ("Working", ""),
                                                    ("Result", "r")],
                sub_rows, headcls="lite", widths=["32%", "42%", "26%"])

    vol_parts = [d["cap"], d["eff"]] + ([d["cal"]] if has_cal else [])
    vol_lbl = ("Volume = Calendar + Capacity + Efficiency" if has_cal
               else "Volume = Capacity + Efficiency")
    vol_work = " &nbsp;+&nbsp; ".join(
        ([vt(d["cal"])] if has_cal else []) + [vt(d["cap"]), vt(d["eff"])])
    recon = table("Reconciliation",
      [("Identity", ""), ("Working", ""), ("Result", "r")],
      [{"cls": "recon",
        "cells": ["<b>FOCV = Expenditure + Volume</b>",
                  f"{vt(d['exp'])} &nbsp;+&nbsp; {vt(d['vol'])}",
                  f"<b>{vt(d['exp'] + d['vol'])}</b>"]},
       {"cls": "recon",
        "cells": ["&nbsp;&nbsp;&nbsp;<i>and FOCV computed directly was</i>", "",
                  f"<b>{vt(d['focv'])}</b> &nbsp;&#10003;"]},
       {"cls": "recon", "cells": [f"<b>{vol_lbl}</b>", vol_work,
                                  f"<b>{vt(sum(vol_parts))}</b>"]},
       {"cls": "recon",
        "cells": ["&nbsp;&nbsp;&nbsp;<i>and the Volume Variance computed directly was</i>", "",
                  f"<b>{vt(d['vol'])}</b> &nbsp;&#10003;"]}],
      headcls="lite", widths=["34%", "40%", "26%"])
    return basis, var, sub, recon


# ======================================================================
# Q14
# ======================================================================
def q14():
    d = foh_engine(bud_foh=160000, bud_hours=20 * 8000, bud_units=20 * 8000 * 1.0,
                   act_foh=168000, act_hours=22 * 8400, act_units=22 * 8400 * 0.9,
                   bud_days=20, act_days=22)
    basis, var, sub, recon = foh_tables(d)

    qq = f"""<p>From the following cost data, calculate the fixed overhead variances and reconcile the
same.</p>
{table(None, [("Particulars", ""), ("Budgeted", "r"), ("Actual", "r")],
 [["No. of working days", "20", "22"], ["Man-hours per day", "8,000", "8,400"],
  ["Output per man-hour in units", "1.0", "0.9"],
  ["Overhead cost " + R, "1,60,000", "1,68,000"]], headcls="lite",
 widths=["48%", "26%", "26%"])}"""

    rd = f"""<p>Nothing in this question is given directly &mdash; every figure the formulas need must be
built from the four rows. Build all of them first, in a table, before touching a formula.</p>
{table(None, [("Figure needed", ""), ("Budgeted", "r"), ("Actual", "r"), ("How", "")],
 [["Total hours", "1,60,000", "1,84,800", "working days &times; man-hours per day"],
  ["Total output in units", "1,60,000", "1,66,320", "total hours &times; output per man-hour"],
  ["Overhead cost " + R, "1,60,000", "1,68,000", "given"],
  ["Overhead rate per hour " + R, "<b>1.00</b>", "0.9091",
   "overhead cost &divide; total hours"],
  ["<b>SH for actual output</b>", "&mdash;", "<b>1,66,320</b>",
   "1,66,320 units &times; 1 hour per unit"],
  ["<b>RSH &mdash; revised standard hours</b>", "&mdash;", "<b>1,76,000</b>",
   "<b>22 actual days &times; 8,000 budgeted hours per day</b>"]],
 headcls="lite", widths=["24%", "17%", "17%", "42%"])}
{bullets([
 '<b>Output per man-hour is 1.0 budgeted and 0.9 actual.</b> So budgeted output equals budgeted hours '
 '(1,60,000 of each, which is a coincidence that makes the sums easy) but actual output of 1,66,320 '
 'is only 90% of the 1,84,800 hours worked.',
 '<b>The standard rate is ' + R + '1.00 per hour</b> &mdash; and because output per hour is 1.0, it '
 'is also ' + R + '1.00 per unit. Convenient, but do not confuse the two: the formulas work in '
 '<b>hours</b>.',
 '<b>RSH uses ACTUAL days but BUDGETED hours per day.</b> 22 &times; 8,000 = 1,76,000. This is the '
 'figure that isolates the calendar variance &mdash; it asks &ldquo;how many hours would we have '
 'expected simply because the month was longer?&rdquo;',
 '<b>Three quite different reasons the volume changed</b>, and RSH is what separates them: the factory '
 'worked <b>more days</b> (calendar), it worked <b>more hours per day</b> (capacity), and it produced '
 '<b>less per hour</b> (efficiency).'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q14", "Fixed overhead variances including a calendar variance",
                        "Fixed overhead &middot; p.83")
            + question(qq) + read(rd)
            + wn(f"""<h4 class="mini">W1 &nbsp;Building every figure the formulas need</h4>
{calc([f'Budgeted hours &nbsp;=&nbsp; 20 days &times; 8,000 &nbsp;=&nbsp; <b>1,60,000 hours</b>',
       f'Actual hours &nbsp;=&nbsp; 22 days &times; 8,400 &nbsp;=&nbsp; <b>1,84,800 hours</b>',
       f'Budgeted output &nbsp;=&nbsp; 1,60,000 &times; 1.0 &nbsp;=&nbsp; <b>1,60,000 units</b>',
       f'Actual output &nbsp;=&nbsp; 1,84,800 &times; 0.9 &nbsp;=&nbsp; <b>1,66,320 units</b>',
       f'Standard rate &nbsp;=&nbsp; {frac(R + "1,60,000", "1,60,000 hours")} &nbsp;=&nbsp; '
       f'<b>{R}1.00 per hour</b>',
       f'SH for actual output &nbsp;=&nbsp; 1,66,320 units &times; 1 hour &nbsp;=&nbsp; '
       f'<b>1,66,320 hours</b>',
       f'RSH &nbsp;=&nbsp; 22 actual days &times; 8,000 budgeted hours &nbsp;=&nbsp; '
       f'<b>1,76,000 hours</b>'])}""")
            + basis + var + sub + recon
            + why(f"""<p>The cost variance is only {vt(d['focv'])}, which on {R}1,68,000 of overhead
looks like a quiet month. The decomposition shows it was anything but.</p>
{table(None, [("Variance", ""), ("Result", "r"), ("What actually happened", "")],
 [["<b>Expenditure</b>", vt(d['exp']),
   "The company spent " + R + "1,68,000 where it budgeted " + R + "1,60,000 &mdash; a 5% overspend "
   "on a cost that is supposed to be <b>fixed</b>. That is the item to investigate."],
  ["<b>Calendar</b>", vt(d['cal']),
   "The month had 22 working days instead of 20. Two extra days at 8,000 budgeted hours absorbed "
   + R + "16,000 more overhead. <b>Nothing to do with performance</b> &mdash; it is the calendar."],
  ["<b>Capacity</b>", vt(d['cap']),
   "The factory ran 8,400 hours a day instead of 8,000. Working the plant harder absorbed a further "
   + R + "8,800."],
  ["<b>Efficiency</b>", vt(d['eff']),
   "<b>The bad news.</b> Output fell to 0.9 units per hour from 1.0. Those 1,84,800 hours should "
   "have produced 1,84,800 units; they produced 1,66,320."],
  ["<b>Volume</b>", vt(d['vol']), "The three above, netted"],
  ["<b>Cost</b>", "<b>" + vt(d['focv']) + "</b>", "<b>Expenditure plus volume</b>"]],
 headcls="lite", widths=["14%", "16%", "70%"])}
<p><b>The story is that a large efficiency failure was almost entirely hidden by working longer.</b></p>
{calc([f'Output per hour fell from 1.0 to 0.9 &mdash; a <b>10% loss of productivity</b>',
       f'That cost {vt(d["eff"])} in unabsorbed fixed overhead',
       f'It was masked by working 2 extra days ({vt(d["cal"])}) and 400 extra hours a day '
       f'({vt(d["cap"])})',
       f'<b>Net volume variance: {vt(d["vol"])} &mdash; apparently favourable</b>'])}
<p>Had the factory worked its budgeted 20 days of 8,000 hours at the actual 0.9 productivity, output
would have been only 1,44,000 units and the volume variance would have been a heavily adverse
{R}16,000. The favourable {vt(d['vol'])} is bought with overtime and extra working days, not
earned by good performance.</p>
<p><b>Recommendation:</b> report the efficiency variance of {vt(d['eff'])} as the principal finding. It
is by far the largest number in the analysis and it is entirely a performance matter. Report the
expenditure overrun of {vt(d['exp'])} separately, since a fixed cost exceeding its budget by 5% needs
explanation. Do <b>not</b> present the volume variance of {vt(d['vol'])} as an achievement.</p>
<p class="small"><b>A note on the arithmetic.</b> Some solutions to this problem compute the actual
overhead as 1,84,800 hours &times; {R}0.91 = {R}1,68,168 and report the cost variance as
{R}1,848 (A). That is a rounding artefact: the actual overhead is <b>given</b> as {R}1,68,000, and
{R}1,68,000 &divide; 1,84,800 is {R}0.9091, not {R}0.91. The correct cost variance is
<b>{vt(d['focv'])}</b>, and it is provable &mdash; it must equal the expenditure variance of
{vt(d['exp'])} plus the volume variance of {vt(d['vol'])}, and only {R}1,680 does.</p>""")
            + ans([("Budgeted / actual hours", "1,60,000 / 1,84,800 hours"),
                   ("Budgeted / actual output", "1,60,000 / 1,66,320 units"),
                   ("Standard rate", f"{R} 1.00 per hour"),
                   ("SH for actual output", "1,66,320 hours"),
                   ("RSH &nbsp;(22 days &times; 8,000)", "1,76,000 hours"),
                   ("<b>FO Expenditure Variance</b>", f"<b>{vt(d['exp'])}</b>"),
                   ("<b>FO Calendar Variance</b>", f"<b>{vt(d['cal'])}</b>"),
                   ("<b>FO Capacity Variance</b>", f"<b>{vt(d['cap'])}</b>"),
                   ("<b>FO Efficiency Variance</b>", f"<b>{vt(d['eff'])}</b>"),
                   ("<b>FO Volume Variance</b>", f"<b>{vt(d['vol'])}</b>"),
                   ("<b>FO Cost Variance</b>", f"<b>{vt(d['focv'])}</b>"),
                   ("Reconciliation",
                    "Cost = Exp + Volume &nbsp;&middot;&nbsp; Volume = Cal + Cap + Eff &nbsp;&#10003;")])
            + "</div>")


# ======================================================================
# Q15
# ======================================================================
def q15():
    d = foh_engine(bud_foh=10000, bud_hours=5000 * 4, bud_units=5000,
                   act_foh=10200, act_hours=20100, act_units=5200)
    basis, var, sub, recon = foh_tables(d)

    qq = f"""<p>Cost data given for Nishu &amp; Co. for July 1993 is as follows:</p>
{table(None, [("Particulars", ""), ("Budgeted", "r"), ("Actual", "r")],
 [["Fixed overheads", R + "10,000", R + "10,200"],
  ["Units of production", "5,000", "5,200"],
  ["Standard time for one unit", "4 hours", "&mdash;"],
  ["Actual hours worked", "&mdash;", "20,100 hours"]], headcls="lite",
 widths=["48%", "26%", "26%"])}
<p>Find out the fixed overhead variances and reconcile them.</p>"""

    rd = f"""<p>Simpler than Q14 in one important respect: <b>no working-days data is given</b>, so there
is <b>no calendar variance</b>. The volume variance splits two ways instead of three.</p>
{steps([
 '<b>Budgeted hours</b> = 5,000 units &times; 4 hours = <b>20,000 hours</b>.',
 '<b>Standard rate</b> = ' + frac(R + "10,000", "20,000 hours") + ' = <b>' + R
 + '0.50 per hour</b>.',
 '<b>SH for actual output</b> = 5,200 units &times; 4 hours = <b>20,800 hours</b>.',
 '<b>Capacity variance uses BH directly</b>, because there is no RSH: SR &times; (AH &minus; BH).'])}
{bullets([
 '<b>This is a genuinely good month</b> and the only favourable cost variance among the four overhead '
 'problems. Output beat budget by 200 units (4%) using only 100 extra hours (0.5%).',
 '<b>20,800 standard hours allowed against 20,100 actually worked</b> &mdash; 700 hours better than '
 'standard, so a firmly <b>favourable efficiency variance</b>.',
 '<b>Fixed overhead was ' + R + '200 over budget</b>, so the expenditure variance is adverse &mdash; '
 'but only by 2%.',
 '<b>Do not invent a calendar variance.</b> Without working-days data it cannot be computed, and '
 'saying so explicitly is worth a mark: the capacity variance then absorbs the whole difference '
 'between actual and budgeted hours.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q15", "Fixed overhead variances without a calendar variance",
                        "Fixed overhead &middot; p.83")
            + question(qq) + read(rd) + basis + var + sub + recon
            + why(f"""<p>A favourable cost variance of {vt(d['focv'])} &mdash; the only one in the
overhead problems &mdash; and the decomposition shows it was properly earned.</p>
{table(None, [("Variance", ""), ("Result", "r"), ("Reason", "")],
 [["<b>Expenditure</b>", vt(d['exp']),
   "Fixed overhead of " + R + "10,200 against a budget of " + R + "10,000 &mdash; a 2% overspend, "
   "small but real."],
  ["<b>Capacity</b>", vt(d['cap']),
   "20,100 hours were worked against 20,000 budgeted. 100 extra hours absorbed " + R
   + "50 more overhead."],
  ["<b>Efficiency</b>", vt(d['eff']),
   "<b>The main favourable item.</b> 5,200 units were produced in 20,100 hours where the standard "
   "allows 20,800 &mdash; 700 hours better than standard."],
  ["<b>Volume</b>", vt(d['vol']),
   "Capacity plus efficiency &mdash; " + R + "400 of fixed overhead over-absorbed"],
  ["<b>Cost</b>", "<b>" + vt(d['focv']) + "</b>",
   "<b>Volume gain less the small expenditure overrun</b>"]],
 headcls="lite", widths=["14%", "16%", "70%"])}
<p><b>Contrast this with Q14 and the difference is instructive.</b></p>
{table(None, [("", ""), ("Q14", "r"), ("Q15", "r")],
 [["Standard hours allowed for the actual output", "1,66,320", "20,800"],
  ["Actual hours worked", "1,84,800", "20,100"],
  ["Hours saved / (wasted)", "<b>(18,480)</b>", "<b>700</b>"],
  ["Efficiency variance", vt(-18480 * 1.0), vt(d['eff'])],
  ["Volume variance", vt(6320), vt(d['vol'])],
  {"cls": "tot", "cells": ["<b>Why the volume variance was favourable</b>",
                           "<b>extra days and hours, despite bad efficiency</b>",
                           "<b>genuine efficiency</b>"]}], headcls="lite",
 widths=["44%", "28%", "28%"])}
<p>In Q14 the favourable volume variance came from working longer while producing less per hour. Here it
comes from producing <b>more per hour</b>. The two look similar in the summary line and are completely
different in substance &mdash; which is the whole argument for splitting the volume variance rather than
reporting it as one figure.</p>
<p><b>Recommendation:</b> report the efficiency variance of {vt(d['eff'])} as a genuine achievement.
Investigate the {vt(d['exp'])} expenditure variance only if it recurs &mdash; a 2% overrun on a fixed
cost is within normal tolerance. And state clearly that <b>no calendar variance can be computed</b>,
because the number of working days is not given; the whole {vt(d['cap'])} difference between actual and
budgeted hours is therefore reported as capacity.</p>""")
            + ans([("Budgeted hours &nbsp;(5,000 &times; 4)", "20,000 hours"),
                   ("Standard rate &nbsp;(10,000 &divide; 20,000)", f"{R} 0.50 per hour"),
                   ("SH for actual output &nbsp;(5,200 &times; 4)", "20,800 hours"),
                   ("Actual hours", "20,100 hours"),
                   ("Standard FOH for actual output", f"{R} {money(d['sc'])}"),
                   ("<b>FO Expenditure Variance</b>", f"<b>{vt(d['exp'])}</b>"),
                   ("<b>FO Capacity Variance</b>", f"<b>{vt(d['cap'])}</b>"),
                   ("<b>FO Efficiency Variance</b>", f"<b>{vt(d['eff'])}</b>"),
                   ("<b>FO Volume Variance</b>", f"<b>{vt(d['vol'])}</b>"),
                   ("<b>FO Cost Variance</b>", f"<b>{vt(d['focv'])}</b>"),
                   ("Calendar variance", "<b>Not applicable</b> &mdash; no working-days data")])
            + "</div>")



# ======================================================================
# SALES VARIANCE ENGINE  -  Q16 (value basis) and Q17 (margin basis)
# ======================================================================
def sales_engine(prods, margin=False):
    """
    prods : list of dicts {n, bq, sp, aq, ap, sc}
            sc = standard cost per unit (needed only on the margin basis)
    margin=False -> sales VALUE variances (Q16)
    margin=True  -> sales MARGIN / profit variances (Q17)
    Convention throughout: ACTUAL minus BUDGET, so + is favourable.
    """
    tot_bq = sum(p["bq"] for p in prods)
    tot_aq = sum(p["aq"] for p in prods)
    rows = []
    for p in prods:
        rbq = tot_aq * (p["bq"] / tot_bq)       # actual total qty in the BUDGETED mix
        if margin:
            sm = p["sp"] - p["sc"]              # standard margin per unit
            am = p["ap"] - p["sc"]              # actual margin per unit (std cost retained)
            base = sm
            bud_val = p["bq"] * sm
            act_val = p["aq"] * am
            price = p["aq"] * (am - sm)
        else:
            sm = am = None
            base = p["sp"]
            bud_val = p["bq"] * p["sp"]
            act_val = p["aq"] * p["ap"]
            price = p["aq"] * (p["ap"] - p["sp"])
        rows.append(dict(n=p["n"], bq=p["bq"], sp=p["sp"], aq=p["aq"], ap=p["ap"],
                         sc=p.get("sc"), sm=sm, am=am, rbq=rbq,
                         bud_val=bud_val, act_val=act_val, price=price,
                         mix=base * (p["aq"] - rbq),
                         qty=base * (rbq - p["bq"]),
                         vol=base * (p["aq"] - p["bq"])))
    d = dict(rows=rows, tot_bq=tot_bq, tot_aq=tot_aq, margin=margin,
             tot_rbq=sum(r["rbq"] for r in rows),
             bud_val=sum(r["bud_val"] for r in rows),
             act_val=sum(r["act_val"] for r in rows),
             price=sum(r["price"] for r in rows),
             mix=sum(r["mix"] for r in rows),
             qty=sum(r["qty"] for r in rows),
             vol=sum(r["vol"] for r in rows))
    d["total"] = d["act_val"] - d["bud_val"]
    return d


def sales_recon(d, names):
    tot_lbl, price_lbl, vol_lbl, mix_lbl, qty_lbl = names
    return table("Reconciliation of the sales variances",
      [("Identity", ""), ("Working", ""), ("Result", "r")],
      [{"cls": "recon",
        "cells": [f"<b>{tot_lbl} = {price_lbl} + {vol_lbl}</b>",
                  f"{vt(d['price'])} &nbsp;+&nbsp; {vt(d['vol'])}",
                  f"<b>{vt(d['price'] + d['vol'])}</b>"]},
       {"cls": "recon",
        "cells": [f"&nbsp;&nbsp;&nbsp;<i>and {tot_lbl} computed directly was</i>", "",
                  f"<b>{vt(d['total'])}</b> &nbsp;&#10003;"]},
       {"cls": "recon",
        "cells": [f"<b>{vol_lbl} = {mix_lbl} + {qty_lbl}</b>",
                  f"{vt(d['mix'])} &nbsp;+&nbsp; {vt(d['qty'])}",
                  f"<b>{vt(d['mix'] + d['qty'])}</b>"]},
       {"cls": "recon",
        "cells": [f"&nbsp;&nbsp;&nbsp;<i>and {vol_lbl} computed directly was</i>", "",
                  f"<b>{vt(d['vol'])}</b> &nbsp;&#10003;"]}],
      headcls="lite", widths=["36%", "38%", "26%"])


# ======================================================================
# Q16
# ======================================================================
def q16():
    d = sales_engine([dict(n="X", bq=500, sp=5, aq=500, ap=5.00),
                      dict(n="Y", bq=400, sp=6, aq=600, ap=6.25),
                      dict(n="Z", bq=300, sp=7, aq=400, ap=6.75)])
    rr = d["rows"]

    qq = f"""<p>From the following data, calculate: <b>(a)</b> Sales Value Variance <b>(b)</b> Sales Price
Variance <b>(c)</b> Sales Mix Variance <b>(d)</b> Sales Quantity Variance <b>(e)</b> Sales Value Volume
Variance.</p>
{table(None, [("Product", ""), ("Budget &mdash; Qty (kg)", "r"),
              ("Budget &mdash; Std. sales price " + R + " per kg", "r"),
              ("Budget &mdash; Total " + R, "r"), ("Actual &mdash; Qty (kg)", "r"),
              ("Actual &mdash; sales price " + R + " per kg", "r"),
              ("Actual &mdash; Total " + R, "r")],
 [["<b>X</b>", "500", "5.00", "2,500", "500", "5.00", "2,500"],
  ["<b>Y</b>", "400", "6.00", "2,400", "600", "6.25", "3,750"],
  ["<b>Z</b>", "300", "7.00", "2,100", "400", "6.75", "2,700"],
  {"cls": "tot", "cells": ["<b>Total</b>", "<b>1,200</b>", "", "<b>7,000</b>", "<b>1,500</b>", "",
                           "<b>8,950</b>"]}], headcls="lite")}"""

    rd = f"""<p><b>Stop and change the convention.</b> Every problem so far has used STANDARD minus
ACTUAL. Sales variances reverse it.</p>
{fml("Sales variance &nbsp;=&nbsp; ACTUAL &nbsp;&minus;&nbsp; BUDGET",
     "More revenue is favourable, so a positive answer is (F). If you keep the cost convention every "
     "sign in this answer will be wrong.")}
{bullets([
 '<b>RBQ &mdash; revised budgeted quantity &mdash; is the sales twin of RSQ.</b> Take the total actual '
 'quantity of 1,500 kg and re-split it in the <b>budgeted</b> mix of 500 : 400 : 300, which is '
 '5 : 4 : 3. So RBQ = 625, 500 and 375 kg, totalling 1,500 kg.',
 '<b>Product X is the control case.</b> Same quantity, same price &mdash; so X has no price variance '
 'and no volume variance. But it <b>does</b> have a mix variance and a quantity variance, and they '
 'cancel. That is worth understanding: X&rsquo;s share of the total <i>fell</i> even though its own '
 'sales did not change, because Y and Z grew.',
 '<b>Y sold above standard price and Z below.</b> Y at ' + R + '6.25 against ' + R + '6.00, Z at ' +
 R + '6.75 against ' + R + '7.00.',
 '<b>Total quantity rose 25%</b> from 1,200 to 1,500 kg, so the quantity variance will be large and '
 'favourable.'])}"""

    basic = table("Basic Calculation",
      [("Product", ""), ("BQ<br/>budgeted qty", "r"), ("SP<br/>std price", "r"),
       ("Budgeted value", "r"), ("AQ<br/>actual qty", "r"), ("AP<br/>actual price", "r"),
       ("Actual value", "r"), ("RBQ<br/>" + src("actual total in budgeted mix"), "r")],
      [[f"<b>{r['n']}</b>", q(r["bq"]), money(r["sp"], 2), money(r["bud_val"]),
        q(r["aq"]), money(r["ap"], 2), money(r["act_val"]), q(r["rbq"])] for r in rr]
      + [{"cls": "tot",
          "cells": ["<b>Total</b>", f"<b>{q(d['tot_bq'])}</b>", "",
                    f"<b>{money(d['bud_val'])}</b>", f"<b>{q(d['tot_aq'])}</b>", "",
                    f"<b>{money(d['act_val'])}</b>", f"<b>{q(d['tot_rbq'])}</b>"]}],
      headcls="lite", widths=["11%", "12%", "11%", "13%", "12%", "11%", "13%", "17%"])
    basic += (f"<div class='small'><b>RBQ working:</b> the budgeted mix is 500 : 400 : 300 = "
              f"5 : 4 : 3 of 12 parts. X = 1,500 &times; {frac('5', '12')} = 625 &middot; "
              f"Y = 1,500 &times; {frac('4', '12')} = 500 &middot; Z = 1,500 &times; "
              f"{frac('3', '12')} = 375. Total 1,500 kg = total AQ &nbsp;&#10003;</div>")

    a = table("(a) &nbsp;SALES VALUE VARIANCE &nbsp;=&nbsp; Actual sales value &minus; Budgeted sales value",
      [("Product", ""), ("Budgeted value " + R, "r"), ("Actual value " + R, "r"),
       ("Variance " + R, "r")],
      [[f"<b>{r['n']}</b>", money(r["bud_val"]), money(r["act_val"]),
        (vt(r["act_val"] - r["bud_val"]), "r")] for r in rr]
      + [{"cls": "tot", "cells": ["<b>Sales Value Variance</b>", f"<b>{money(d['bud_val'])}</b>",
                                  f"<b>{money(d['act_val'])}</b>",
                                  (f"<b>{vt(d['total'])}</b>", "r")]}],
      headcls="lite", widths=["22%", "26%", "26%", "26%"])

    b = vbox("(b) &nbsp;SALES PRICE VARIANCE", "AQ &times; (AP &minus; SP)",
      [[f"<b>{r['n']}</b>", money(r["ap"], 2), money(r["sp"], 2),
        num(r["ap"] - r["sp"], 2), q(r["aq"]), (vt(r["price"]), "r")] for r in rr],
      d["price"],
      [("Product", ""), ("AP", "r"), ("SP", "r"), ("AP &minus; SP", "r"), ("AQ", "r"),
       ("Amount " + R, "r")], widths=["17%", "13%", "13%", "17%", "18%", "22%"])

    c = vbox("(c) &nbsp;SALES MIX VARIANCE", "SP &times; (AQ &minus; RBQ)",
      [[f"<b>{r['n']}</b>", q(r["aq"]), q(r["rbq"]), num(r["aq"] - r["rbq"]),
        money(r["sp"], 2), (vt(r["mix"]), "r")] for r in rr],
      d["mix"],
      [("Product", ""), ("AQ", "r"), ("RBQ", "r"), ("AQ &minus; RBQ", "r"), ("SP", "r"),
       ("Amount " + R, "r")], widths=["17%", "15%", "15%", "17%", "13%", "23%"])

    e = vbox("(d) &nbsp;SALES QUANTITY VARIANCE", "SP &times; (RBQ &minus; BQ)",
      [[f"<b>{r['n']}</b>", q(r["rbq"]), q(r["bq"]), num(r["rbq"] - r["bq"]),
        money(r["sp"], 2), (vt(r["qty"]), "r")] for r in rr],
      d["qty"],
      [("Product", ""), ("RBQ", "r"), ("BQ", "r"), ("RBQ &minus; BQ", "r"), ("SP", "r"),
       ("Amount " + R, "r")], widths=["17%", "15%", "15%", "17%", "13%", "23%"])

    f = vbox("(e) &nbsp;SALES VALUE VOLUME VARIANCE", "SP &times; (AQ &minus; BQ)",
      [[f"<b>{r['n']}</b>", q(r["aq"]), q(r["bq"]), num(r["aq"] - r["bq"]),
        money(r["sp"], 2), (vt(r["vol"]), "r")] for r in rr],
      d["vol"],
      [("Product", ""), ("AQ", "r"), ("BQ", "r"), ("AQ &minus; BQ", "r"), ("SP", "r"),
       ("Amount " + R, "r")], widths=["17%", "15%", "15%", "17%", "13%", "23%"])

    return ("<div class='prob long'>"
            + prob_head("Q16", "All five sales value variances",
                        "Sales &middot; p.84")
            + question(qq) + read(rd) + basic + a + b + c + e + f
            + sales_recon(d, ("Sales Value Variance", "Price", "Volume", "Mix", "Quantity"))
            + why(f"""<p>Sales beat budget by {vt(d['total'])} &mdash; a
{d['total']/d['bud_val']*100:.1f}% increase on a budget of {R}7,000 &mdash; and the analysis shows
that almost all of it came from selling <b>more</b>, not from charging more.</p>
{table(None, [("Variance", ""), ("Result", "r"), ("Share", "r"), ("What it says", "")],
 [["<b>Price</b>", vt(d['price']), f"{d['price']/d['total']*100:.0f}%",
   "Y sold " + R + "0.25 above standard (" + vt(rr[1]['price']) + ") but Z sold " + R
   + "0.25 below (" + vt(rr[2]['price']) + "). Almost a wash."],
  ["<b>Mix</b>", vt(d['mix']), f"{d['mix']/d['total']*100:.0f}%",
   "The mix moved towards Z at " + R + "7 and away from X at " + R + "5 &mdash; selling a higher "
   "proportion of the dearer products."],
  ["<b>Quantity</b>", vt(d['qty']), f"{d['qty']/d['total']*100:.0f}%",
   "<b>The whole story.</b> Total volume rose from 1,200 to 1,500 kg &mdash; a 25% increase."],
  ["<b>Volume</b>", vt(d['vol']), f"{d['vol']/d['total']*100:.0f}%", "Mix plus quantity"],
  {"cls": "tot", "cells": ["<b>Sales value</b>", "<b>" + vt(d['total']) + "</b>", "<b>100%</b>",
                           "<b>Price plus volume</b>"]}], headcls="lite",
 widths=["12%", "15%", "10%", "63%"])}
<p><b>Product X repays close attention</b>, because it is the one product whose own figures did not
change at all &mdash; 500 kg at {R}5 both budgeted and actual &mdash; and yet it produces two
non-zero variances.</p>
{calc([f'X mix variance &nbsp;=&nbsp; {R}5 &times; (500 &minus; 625) &nbsp;=&nbsp; '
       f'{vt(rr[0]["mix"])}',
       f'X quantity variance &nbsp;=&nbsp; {R}5 &times; (625 &minus; 500) &nbsp;=&nbsp; '
       f'{vt(rr[0]["qty"])}',
       f'<b>X volume variance &nbsp;=&nbsp; {vt(rr[0]["vol"])}</b> &mdash; they cancel exactly'])}
<p>The reason is that mix and quantity measure two different things and X moved on one but not the
other. Total sales grew 25%, so X <i>should</i> have grown to 625 kg to keep its share; it stayed at
500, so it lost mix. But the quantity variance credits X with the share of the overall 25% growth that a
product of its size would have contributed. The two effects are equal and opposite because X&rsquo;s own
sales were flat. <b>Only the total volume variance of {vt(rr[0]['vol'])} is real for X;</b> the split is
an accounting attribution.</p>
<p><b>What to report.</b> A favourable sales value variance of {vt(d['total'])} driven by a 25% volume
increase is good news, and the quantity variance of {vt(d['qty'])} is the item to highlight. Two
cautions belong with it:</p>
{bullets([
 '<b>Sales value variances say nothing about profit.</b> Selling 300 extra kilograms also cost money '
 'to produce. The company may have sold more and earned less &mdash; which is exactly why Q17 uses the '
 '<b>margin</b> basis instead.',
 '<b>Z&rsquo;s price was cut by ' + R + '0.25</b> and its volume rose by a third. That may be cause '
 'and effect, and if so the ' + vt(rr[2]['price']) + ' price variance is the price paid for the '
 + vt(rr[2]['vol']) + ' volume gain &mdash; a good trade on these numbers, but one worth making '
 'consciously rather than discovering afterwards.'])}""")
            + ans([("RBQ &mdash; X / Y / Z", "625 / 500 / 375 kg"),
                   ("Budgeted / actual sales value", f"{R} 7,000 / {R} 8,950"),
                   ("<b>(a) Sales Value Variance</b>", f"<b>{vt(d['total'])}</b>"),
                   ("<b>(b) Sales Price Variance</b>", f"<b>{vt(d['price'])}</b>"),
                   ("<b>(c) Sales Mix Variance</b>", f"<b>{vt(d['mix'])}</b>"),
                   ("<b>(d) Sales Quantity Variance</b>", f"<b>{vt(d['qty'])}</b>"),
                   ("<b>(e) Sales Value Volume Variance</b>", f"<b>{vt(d['vol'])}</b>"),
                   ("Reconciliation",
                    "Value = Price + Volume &nbsp;&middot;&nbsp; Volume = Mix + Quantity &nbsp;&#10003;")])
            + "</div>")


# ======================================================================
# Q17
# ======================================================================
def q17():
    d = sales_engine([dict(n="A", bq=500, sp=2.00, sc=1.75, aq=560, ap=1.95),
                      dict(n="B", bq=700, sp=1.50, sc=1.30, aq=710, ap=1.40)],
                     margin=True)
    rr = d["rows"]

    qq = f"""<p>The following information of Lucky &amp; Co. is given for December 2007.</p>
{table("Budgeted sales", [("Product", ""), ("Units", "r"), ("Selling price " + R, "r"),
                          ("Standard cost " + R, "r")],
 [["<b>A</b>", "500", "2.00", "1.75"], ["<b>B</b>", "700", "1.50", "1.30"]],
 headcls="lite", widths=["28%", "24%", "24%", "24%"])}
{table("Actual sales", [("Product", ""), ("Units", "r"), ("Selling price " + R, "r")],
 [["<b>A</b>", "560", "1.95"], ["<b>B</b>", "710", "1.40"]],
 headcls="lite", widths=["36%", "32%", "32%"])}
<p>Find out: <b>(a)</b> Sales Margin Price Variance <b>(b)</b> Sales Margin Mix Variance
<b>(c)</b> Sales Margin Quantity Variance <b>(d)</b> Total Sales Margin Variance <b>(e)</b> Sales Margin
Volume Variance.</p>"""

    rd = f"""<p>The word <b>margin</b> changes everything. Q16 measured revenue; this question measures
<b>profit</b>. Every formula is the same shape but the multiplier is the margin per unit, not the
selling price.</p>
{fml("Margin per unit &nbsp;=&nbsp; Selling price &nbsp;&minus;&nbsp; STANDARD cost",
     "The standard cost is used in BOTH the budgeted and the actual margin. That is deliberate: it "
     "keeps cost variances out of the sales analysis, so a sales manager is judged only on prices and "
     "volumes and not on the factory's efficiency.")}
{table(None, [("Product", ""), ("Selling price " + R, "r"), ("Standard cost " + R, "r"),
              ("Margin per unit " + R, "r")],
 [["<b>A</b> &mdash; standard margin", "2.00", "(1.75)", "<b>0.25</b>"],
  ["<b>A</b> &mdash; actual margin", "1.95", "(1.75)", "<b>0.20</b>"],
  ["<b>B</b> &mdash; standard margin", "1.50", "(1.30)", "<b>0.20</b>"],
  ["<b>B</b> &mdash; actual margin", "1.40", "(1.30)", "<b>0.10</b>"]],
 headcls="lite", widths=["40%", "20%", "20%", "20%"])}
{bullets([
 '<b>Both products were sold below their standard price</b>, so both actual margins are lower than '
 'standard. A fell from ' + R + '0.25 to ' + R + '0.20; B fell from ' + R + '0.20 to ' + R + '0.10 '
 '&mdash; <b>B lost half its margin</b>.',
 '<b>Note how heavily a small price cut hits the margin.</b> B&rsquo;s price fell 6.7% (from ' + R
 + '1.50 to ' + R + '1.40) but its margin fell <b>50%</b>. That is the whole reason for analysing on '
 'a margin basis: a 6.7% discount does not cost 6.7% of profit.',
 '<b>RBQ = total actual quantity in the budgeted mix.</b> Total actual is 1,270 units and the '
 'budgeted mix is 500 : 700, so RBQ = 1,270 &times; ' + frac("5", "12") + ' = 529.17 and '
 '1,270 &times; ' + frac("7", "12") + ' = 740.83. Keep two decimals.',
 '<b>Volumes rose only slightly</b> &mdash; A up 60 units, B up 10 &mdash; so the volume variances '
 'will be small and the price effect will dominate.'])}"""

    basic = table("Basic Calculation &mdash; on the MARGIN basis",
      [("Product", ""), ("BQ", "r"), ("Standard margin " + R, "r"),
       ("Budgeted margin " + R, "r"), ("AQ", "r"), ("Actual margin " + R, "r"),
       ("Actual margin " + R, "r"), ("RBQ", "r")],
      [[f"<b>{r['n']}</b>", q(r["bq"]), money(r["sm"], 2), money(r["bud_val"], 2),
        q(r["aq"]), money(r["am"], 2), money(r["act_val"], 2), q(r["rbq"], 2)] for r in rr]
      + [{"cls": "tot",
          "cells": ["<b>Total</b>", f"<b>{q(d['tot_bq'])}</b>", "",
                    f"<b>{money(d['bud_val'], 2)}</b>", f"<b>{q(d['tot_aq'])}</b>", "",
                    f"<b>{money(d['act_val'], 2)}</b>", f"<b>{q(d['tot_rbq'], 2)}</b>"]}],
      headcls="lite", widths=["11%", "10%", "14%", "15%", "10%", "13%", "14%", "13%"])
    basic += (f"<div class='small'><b>RBQ working:</b> budgeted mix 500 : 700 = 5 : 7 of 12 parts. "
              f"A = 1,270 &times; {frac('5', '12')} = 529.17 &middot; B = 1,270 &times; "
              f"{frac('7', '12')} = 740.83. Total 1,270 units = total AQ &nbsp;&#10003; &nbsp;&nbsp; "
              f"<b>Budgeted total margin {R}{money(d['bud_val'], 2)}</b> against an <b>actual total "
              f"margin of {R}{money(d['act_val'], 2)}</b>.</div>")

    a = vbox("(a) &nbsp;SALES MARGIN PRICE VARIANCE",
             "AQ &times; (Actual margin &minus; Standard margin)",
      [[f"<b>{r['n']}</b>", money(r["am"], 2), money(r["sm"], 2),
        num(r["am"] - r["sm"], 2), q(r["aq"]), (vt(r["price"]), "r")] for r in rr],
      d["price"],
      [("Product", ""), ("Actual margin", "r"), ("Std margin", "r"), ("Difference", "r"),
       ("AQ", "r"), ("Amount " + R, "r")], widths=["15%", "17%", "15%", "16%", "15%", "22%"])

    b = vbox("(b) &nbsp;SALES MARGIN MIX VARIANCE", "Standard margin &times; (AQ &minus; RBQ)",
      [[f"<b>{r['n']}</b>", q(r["aq"]), q(r["rbq"], 2), num(r["aq"] - r["rbq"], 2),
        money(r["sm"], 2), (vt(r["mix"], 2), "r")] for r in rr],
      d["mix"],
      [("Product", ""), ("AQ", "r"), ("RBQ", "r"), ("AQ &minus; RBQ", "r"), ("Std margin", "r"),
       ("Amount " + R, "r")], widths=["15%", "14%", "15%", "17%", "16%", "23%"])

    c = vbox("(c) &nbsp;SALES MARGIN QUANTITY VARIANCE",
             "Standard margin &times; (RBQ &minus; BQ)",
      [[f"<b>{r['n']}</b>", q(r["rbq"], 2), q(r["bq"]), num(r["rbq"] - r["bq"], 2),
        money(r["sm"], 2), (vt(r["qty"], 2), "r")] for r in rr],
      d["qty"],
      [("Product", ""), ("RBQ", "r"), ("BQ", "r"), ("RBQ &minus; BQ", "r"), ("Std margin", "r"),
       ("Amount " + R, "r")], widths=["15%", "15%", "14%", "17%", "16%", "23%"])

    dd = table("(d) &nbsp;TOTAL SALES MARGIN VARIANCE &nbsp;=&nbsp; Actual margin &minus; Budgeted margin",
      [("Product", ""), ("Budgeted margin " + R, "r"), ("Actual margin " + R, "r"),
       ("Variance " + R, "r")],
      [[f"<b>{r['n']}</b>", money(r["bud_val"], 2), money(r["act_val"], 2),
        (vt(r["act_val"] - r["bud_val"]), "r")] for r in rr]
      + [{"cls": "tot",
          "cells": ["<b>Total Sales Margin Variance</b>", f"<b>{money(d['bud_val'], 2)}</b>",
                    f"<b>{money(d['act_val'], 2)}</b>", (f"<b>{vt(d['total'])}</b>", "r")]}],
      headcls="lite", widths=["28%", "24%", "24%", "24%"])

    e = vbox("(e) &nbsp;SALES MARGIN VOLUME VARIANCE", "Standard margin &times; (AQ &minus; BQ)",
      [[f"<b>{r['n']}</b>", q(r["aq"]), q(r["bq"]), num(r["aq"] - r["bq"]),
        money(r["sm"], 2), (vt(r["vol"]), "r")] for r in rr],
      d["vol"],
      [("Product", ""), ("AQ", "r"), ("BQ", "r"), ("AQ &minus; BQ", "r"), ("Std margin", "r"),
       ("Amount " + R, "r")], widths=["15%", "15%", "14%", "17%", "16%", "23%"])

    return ("<div class='prob long'>"
            + prob_head("Q17", "Sales margin (profit) variances",
                        "Sales &middot; p.84")
            + question(qq) + read(rd) + basic + a + b + c + dd + e
            + sales_recon(d, ("Total Sales Margin Variance", "Margin Price", "Margin Volume",
                              "Margin Mix", "Margin Quantity"))
            + why(f"""<p><b>This is the most important problem in the module, because it contradicts
Q16.</b> Sales volume rose and yet profit fell.</p>
{table(None, [("", ""), ("Budget", "r"), ("Actual", "r"), ("Change", "r")],
 [["Units sold", q(d['tot_bq']), q(d['tot_aq']),
   f"<b>+{d['tot_aq'] - d['tot_bq']:.0f} units &nbsp;(+{(d['tot_aq']/d['tot_bq']-1)*100:.1f}%)</b>"],
  ["Sales value " + R,
   money(500 * 2.00 + 700 * 1.50, 2), money(560 * 1.95 + 710 * 1.40, 2),
   f"<b>+{money(560*1.95+710*1.40 - (500*2.00+700*1.50), 2)}</b>"],
  {"cls": "tot", "cells": ["<b>Total margin (profit) " + R + "</b>",
                           f"<b>{money(d['bud_val'], 2)}</b>", f"<b>{money(d['act_val'], 2)}</b>",
                           f"<b>{vt(d['total'])}</b>"]}], headcls="lite",
 widths=["34%", "22%", "22%", "22%"])}
<p>The company sold {d['tot_aq'] - d['tot_bq']:.0f} more units and took in
{R}{money(560*1.95+710*1.40 - (500*2.00+700*1.50), 2)} more revenue &mdash; and its profit fell by
{R}{money(abs(d['total']), 2)}. On a sales <i>value</i> basis this would have looked like a good month.
On a <b>margin</b> basis it was a bad one.</p>
{table(None, [("Variance", ""), ("Result", "r"), ("What it says", "")],
 [["<b>Margin price</b>", vt(d['price']),
   "<b>The whole problem.</b> Both products were discounted. A lost " + R + "0.05 of margin on 560 "
   "units (" + vt(rr[0]['price']) + "); B lost " + R + "0.10 on 710 units ("
   + vt(rr[1]['price']) + ")."],
  ["<b>Margin mix</b>", vt(d['mix'], 2),
   "Marginally favourable &mdash; the mix moved slightly towards A, which carries the higher standard "
   "margin of " + R + "0.25 against B's " + R + "0.20."],
  ["<b>Margin quantity</b>", vt(d['qty'], 2),
   "Favourable &mdash; 70 more units were sold in total, each carrying a standard margin."],
  ["<b>Margin volume</b>", vt(d['vol']), "Mix plus quantity &mdash; the gain from selling more"],
  {"cls": "tot", "cells": ["<b>Total sales margin</b>", "<b>" + vt(d['total']) + "</b>",
                           "<b>The discounting cost nearly six times what the extra volume "
                           "earned.</b>"]}], headcls="lite", widths=["15%", "15%", "70%"])}
<p><b>The arithmetic of the trade-off, and this is the answer to write out:</b></p>
{calc([f'Gained by selling 70 more units &nbsp;=&nbsp; {vt(d["vol"])}',
       f'Lost by discounting both products &nbsp;=&nbsp; {vt(d["price"])}',
       f'<b>Net &nbsp;=&nbsp; {vt(d["total"])}</b>',
       f'The discount cost <b>{abs(d["price"])/abs(d["vol"]):.1f} times</b> what the extra volume '
       f'earned'])}
<p><b>Why the discount was so expensive.</b> Because the margins are thin, a small cut in price is a
large cut in profit. Product B is the clearest case:</p>
{calc([f'B&rsquo;s price fell from {R}1.50 to {R}1.40 &mdash; a cut of '
       f'<b>{(1.50-1.40)/1.50*100:.1f}%</b>',
       f'But B&rsquo;s margin fell from {R}0.20 to {R}0.10 &mdash; a cut of <b>50%</b>',
       f'To stand still on profit, B&rsquo;s volume would have had to <b>double</b>. It rose by '
       f'<b>{(710/700-1)*100:.1f}%</b>.'])}
<p><b>Recommendation:</b> withdraw the discounts. On these margins the price reductions cannot be
recovered by any realistic increase in volume &mdash; B would need to sell twice as many units simply to
break even on the {R}0.10 cut. If the discounts were a response to competition, the company should
recognise that at a standard cost of {R}1.30 against a price of {R}1.40 it has almost no room to
compete on price, and should look at cost reduction instead.</p>
<p class="small"><b>The examinable point in one sentence:</b> sales <i>value</i> variances measure
revenue and sales <i>margin</i> variances measure profit, and when prices are cut to win volume the two
give <b>opposite</b> answers. That is why margin variances are the ones that matter for
decision-making.</p>""")
            + ans([("Standard margin &mdash; A / B", f"{R} 0.25 / {R} 0.20 per unit"),
                   ("Actual margin &mdash; A / B", f"{R} 0.20 / {R} 0.10 per unit"),
                   ("RBQ &mdash; A / B", "529.17 / 740.83 units"),
                   ("Budgeted total margin", f"{R} {money(d['bud_val'], 2)}"),
                   ("Actual total margin", f"{R} {money(d['act_val'], 2)}"),
                   ("<b>(a) Sales Margin Price Variance</b>", f"<b>{vt(d['price'])}</b>"),
                   ("<b>(b) Sales Margin Mix Variance</b>", f"<b>{vt(d['mix'], 2)}</b>"),
                   ("<b>(c) Sales Margin Quantity Variance</b>", f"<b>{vt(d['qty'], 2)}</b>"),
                   ("<b>(d) Total Sales Margin Variance</b>", f"<b>{vt(d['total'])}</b>"),
                   ("<b>(e) Sales Margin Volume Variance</b>", f"<b>{vt(d['vol'])}</b>"),
                   ("Reconciliation",
                    "Total = Price + Volume &nbsp;&middot;&nbsp; Volume = Mix + Quantity &nbsp;&#10003;")])
            + "</div>")


# ======================================================================
def build():
    return (opener()
            + q1() + q2() + q3() + q4() + q5() + q6() + q7()
            + q8() + q9() + q10()
            + q11() + q12() + q13()
            + q14() + q15()
            + q16() + q17())
