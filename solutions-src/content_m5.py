# -*- coding: utf-8 -*-
"""MODULE 5 - BUDGETARY CONTROL  (15 problems)"""
from build import (esc, rs, money, frac, prob_head, question, read, method, wn,
                   trap, why, steps, bullets, fml, calc, ans, table, src,
                   arrow_panel, module_opener)

R = "&#8377;"
NAVY, RED, GREEN, GREY = "#10314f", "#c0392b", "#1e7a37", "#777"


def stmt(caption, cols, rows, note=None, widths=None, first="Particulars"):
    """Columnar budget statement: Particulars | one column per period/level."""
    head = [(first, "")] + [(c, "r") for c in cols]
    body = []
    for r in rows:
        cls = r[2] if len(r) > 2 else ""
        body.append({"cls": cls, "cells": [r[0]] + [(v, "r") for v in r[1]]})
    t = table(caption, head, body, widths=widths)
    if note:
        t += f"<div class='small'>{note}</div>"
    return t


def flex(caption, cols, rows, note=None):
    """
    Flexible budget with a Per Unit / Total pair under each activity level -
    the exact layout used in the handwritten notes for Q1 and Q4.
    cols : list of level captions, e.g. ["Output 5,000 units", "Output 7,000 units"]
    rows : list of (particulars, [pu1, tot1, pu2, tot2, ...], cls)
    """
    h = f"<table class='t'><caption>{caption}</caption><thead><tr>"
    h += "<th rowspan='2'>Particulars</th>"
    for c in cols:
        h += f"<th colspan='2' class='c'>{c}</th>"
    h += "</tr><tr>"
    for _ in cols:
        h += "<th class='r'>Per unit " + R + "</th><th class='r'>Total " + R + "</th>"
    h += "</tr></thead><tbody>"
    for r in rows:
        cls = r[2] if len(r) > 2 else ""
        h += f"<tr class='{cls}'><td>{r[0]}</td>"
        for v in r[1]:
            h += f"<td class='r'>{v}</td>"
        h += "</tr>"
    h += "</tbody></table>"
    if note:
        h += f"<div class='small'>{note}</div>"
    return h


# ----------------------------------------------------------------------
def budget_map():
    return arrow_panel(500, 248, [
        {"box": (168, 6, 164, 24, "SALES BUDGET", "#10314f"), "fg": "#ffffff", "fs": 9.0},
        {"box": (168, 48, 164, 24, "PRODUCTION BUDGET", "#eaf1f8"), "fs": 8.8},
        {"box": (12, 98, 150, 30, "Materials / Parts|Purchase Budget", "#ffffff"), "fs": 8.2},
        {"box": (175, 98, 150, 30, "Man Power /|Labour Budget", "#ffffff"), "fs": 8.2},
        {"box": (338, 98, 150, 30, "Overhead Budget|(flexible budget)", "#ffffff"), "fs": 8.2},
        {"box": (168, 158, 164, 24, "CASH BUDGET", "#eaf1f8"), "fs": 8.8},
        {"box": (140, 200, 220, 30, "MASTER BUDGET|Budgeted Profit &amp; Loss", "#eaf6ee"),
         "stroke": GREEN, "fs": 8.8},
        # connectors
        {"line": (250, 30, 250, 46), "col": NAVY},
        {"line": (250, 72, 90, 96), "col": NAVY},
        {"line": (250, 72, 250, 96), "col": NAVY},
        {"line": (250, 72, 410, 96), "col": NAVY},
        {"line": (90, 128, 218, 156), "col": NAVY},
        {"line": (250, 128, 250, 156), "col": NAVY},
        {"line": (410, 128, 284, 156), "col": NAVY},
        {"line": (250, 182, 250, 198), "col": NAVY},
        # which problems live in each box
        {"txt": (344, 20, "Q9", 7.6, RED, "start")},
        {"txt": (344, 62, "Q8  Q10", 7.6, RED, "start")},
        {"txt": (87, 143, "Q11  Q12  Q15", 7.6, RED, "middle")},
        {"txt": (250, 143, "Q15", 7.6, RED, "middle")},
        {"txt": (413, 143, "Q1 Q2 Q3 Q4 Q13", 7.6, RED, "middle")},
        {"txt": (344, 172, "Q5  Q6  Q7", 7.6, RED, "start")},
        {"txt": (372, 218, "Q14  Q15", 7.6, RED, "start")},
        {"txt": (160, 62, "= Sales + Closing stock", 7.0, GREY, "end")},
        {"txt": (160, 71, "&minus; Opening stock", 7.0, GREY, "end")},
    ], "The budget hierarchy, and where each problem in this module sits. Everything begins with the "
       "sales budget, because sales is normally the limiting factor.")


# ----------------------------------------------------------------------
def opener():
    intro = f"""
<h2 class="sec">What Module 5 is really about</h2>
<p>A budget is a plan expressed in numbers. Module 5 asks you to build those plans, and every problem
is one of a small number of shapes. Once you can name the shape, the arithmetic is easy &mdash; and
naming the shape is what this opening page is for.</p>

<div class="blk read"><span class="lab">The three formulas that carry this whole module</span>
{fml("PRODUCTION BUDGET &nbsp;=&nbsp; Budgeted Sales &nbsp;+&nbsp; Desired Closing Stock "
     "&nbsp;&minus;&nbsp; Opening Stock",
     "Read it as: how much must I MAKE, given what I want to SELL and the stock I want to be left "
     "holding? Used in Q8, Q10, Q11, Q12 and Q15.")}
{fml("PURCHASE BUDGET &nbsp;=&nbsp; Materials Consumed &nbsp;+&nbsp; Closing Stock "
     "&nbsp;&minus;&nbsp; Opening Stock",
     "The same shape one level down &mdash; and &ldquo;materials consumed&rdquo; comes from the "
     "production budget, never from the sales budget. Used in Q11, Q12 and Q15.")}
{fml("CLOSING BALANCE &nbsp;=&nbsp; Opening Balance &nbsp;+&nbsp; Receipts &nbsp;&minus;&nbsp; Payments",
     "The cash budget. Its whole difficulty is deciding WHICH MONTH each receipt and payment falls "
     "in. Used in Q5, Q6 and Q7.")}
<p><b>Notice that the first two are the same formula.</b> Both say: <i>what I need to obtain equals
what I will use up, plus what I want left over, less what I already have.</i> Learn it once and it
covers finished goods, raw materials and parts alike.</p>
</div>

<h2 class="sec" style="margin-top:6mm">How the budgets fit together</h2>
{budget_map()}

<h2 class="sec" style="margin-top:6mm">The five problem types in this module</h2>
{table(None, [("Type", ""), ("How to recognise it", ""), ("What you produce", ""),
              ("Problems", "c")],
 [["<b>1. Flexible budget</b>",
   "&ldquo;Prepare a budget at 60%, 70% and 90% capacity&rdquo;, or costs given at one level and "
   "wanted at another.",
   "A column per activity level. Split every cost into fixed and variable <b>first</b>.",
   "<b>1, 2, 3, 4</b>"],
  ["<b>2. Cost segregation<br/>(high&ndash;low)</b>",
   "Costs given at <b>two</b> volumes, and a third volume asked for.",
   "Variable rate per unit from the two points, then the fixed element by back-substitution.",
   "<b>13</b>"],
  ["<b>3. Cash budget</b>",
   "A table of monthly sales, purchases and wages plus credit terms.",
   "Working notes for collections first, then a receipts-and-payments statement month by month.",
   "<b>5, 6, 7</b>"],
  ["<b>4. Production &amp; purchase budget</b>",
   "Opening and closing stock figures are given in <b>units</b>.",
   "Sales + closing &minus; opening, in quantity. Then the same again for materials.",
   "<b>8, 10, 11, 12</b>"],
  ["<b>5. Sales &amp; master budget</b>",
   "&ldquo;Prepare a quantitative-cum-financial budget&rdquo;, or &ldquo;prepare a master "
   "budget&rdquo;.",
   "Quantity &times; price by product and zone; or a full budgeted profit statement.",
   "<b>9, 14, 15</b>"]],
 headcls="lite", widths=["19%", "30%", "36%", "15%"])}

<h2 class="sec" style="margin-top:6mm">The behaviour of costs &mdash; the idea behind every flexible budget</h2>
{table(None, [("Type of cost", ""), ("Total amount when output rises", ""),
              ("Amount PER UNIT when output rises", ""), ("Examples in this module", "")],
 [["<b>Fixed</b>", "<b class='no'>Stays the same</b>", "<b class='yes'>Falls</b>",
   "Salaries, rent, depreciation, insurance, works manager&rsquo;s salary"],
  ["<b>Variable</b>", "<b class='yes'>Rises in proportion</b>", "<b class='no'>Stays the same</b>",
   "Materials, direct labour, indirect materials, stores and spares"],
  ["<b>Semi-variable</b>", "Rises, but <b>not</b> in proportion",
   "Falls, but not to a simple pattern",
   "Repairs, maintenance, supervision, electricity, indirect labour"]],
 headcls="lite", widths=["14%", "24%", "22%", "40%"])}
<p><b>Write the two lines from your notes at the foot of every flexible budget</b> &mdash; they are
worth a mark and they prove you understand what you have just prepared:</p>
{calc(["Fixed cost <b>remains the same</b> in total; fixed cost <b>per unit changes</b>.",
       "Variable cost <b>changes</b> in total; variable cost <b>per unit remains the same</b>."])}

<div class="blk trap"><span class="lab">The trap / where marks are lost</span>
{bullets([
 '<b>Scaling a fixed cost.</b> The single commonest error in the module. If fixed overhead is ' +
 R + '50,000 at 5,000 units it is still ' + R + '50,000 at 7,000 units &mdash; only the per-unit '
 'figure moves, from ' + R + '10 to ' + R + '7.14.',
 '<b>Splitting a semi-variable cost by guesswork.</b> Use the percentages if the question gives them '
 '(Q3), the stated step-rules if it gives those (Q2), or the high&ndash;low method if it gives two '
 'volumes (Q13). Never invent a split.',
 '<b>Basing the purchase budget on SALES units.</b> Materials are consumed by <b>production</b>, not '
 'by sales. Always compute the production budget first, then feed it into the materials budget.',
 '<b>Putting a receipt in the wrong month.</b> In cash budgets, write out the collection working note '
 'in full before touching the budget itself. Every cash-budget problem in this module is decided by '
 'that working note.',
 '<b>Bringing depreciation into a cash budget.</b> It is not a cash flow. It belongs in a flexible '
 'budget and in the master budget, but never in a cash budget.'])}
</div>
"""
    return module_opener("Module 5", "Budgetary Control",
                         "15 problems &middot; workbook pages 49&ndash;55", intro)


# ======================================================================
# Q1
# ======================================================================
def q1():
    q = f"""<p>The expenses for the production of 5,000 units in a factory are given as follows:</p>
{table(None, [("Particulars", ""), ("Per unit (" + R + ")", "r")],
 [["Materials", "50"], ["Labour", "20"], ["Variable overheads", "15"],
  ["Fixed overheads (" + R + "50,000)", "10"], ["Administrative expenses (5% variable)", "10"],
  ["Selling expenses (20% fixed)", "6"], ["Distribution expenses (10% fixed)", "5"],
  {"cls": "tot", "cells": ["<b>Total cost of sales per unit</b>", "<b>116</b>"]}],
 headcls="lite", widths=["72%", "28%"])}
<p>You are required to prepare a budget for the production of 7,000 units.</p>"""

    rd = f"""<p>Everything is given <b>per unit at 5,000 units</b>, and three of the seven lines are
semi-variable. Convert each line into total money at 5,000 units first &mdash; that is the only safe
way to keep the fixed elements fixed.</p>
{bullets([
 '<b>The bracketed notes are instructions.</b> &ldquo;(5% variable)&rdquo; means 5% of that line is '
 'variable and <b>95% is fixed</b>. &ldquo;(20% fixed)&rdquo; means 20% fixed and <b>80% '
 'variable</b>. Read which way round each one is written &mdash; the workbook alternates '
 'deliberately.',
 '<b>Fixed overhead is given twice over</b> &mdash; as ' + R + '10 per unit <i>and</i> as a total of ' +
 R + '50,000. The total is the real figure; ' + R + '10 is merely 50,000 &divide; 5,000 and will '
 'change to ' + R + '7.14 at 7,000 units.',
 '<b>Method: split, then scale.</b> For every line, work out the fixed rupees and the variable rupees '
 'per unit at 5,000 units. Carry the fixed rupees across unchanged; multiply the variable rate by '
 '7,000.',
 'The total cost per unit will <b>fall</b> from ' + R + '116 to ' + R + '109.94, because the same '
 'fixed cost is being spread over 2,000 more units. That fall is the whole point of the exercise.'])}"""

    wn1 = f"""<h4 class="mini">W1 &nbsp;Splitting the three semi-variable lines at 5,000 units</h4>
{table(None, [("Line", ""), ("Total at 5,000 units", "r"), ("Given split", ""),
              ("Fixed " + R, "r"), ("Variable " + R, "r"), ("Variable rate per unit", "r")],
 [["Administrative expenses", "50,000<br/>" + src("5,000 &times; " + R + "10"),
   "5% variable, so 95% fixed", "47,500", "2,500", "0.50"],
  ["Selling expenses", "30,000<br/>" + src("5,000 &times; " + R + "6"),
   "20% fixed, so 80% variable", "6,000", "24,000", "4.80"],
  ["Distribution expenses", "25,000<br/>" + src("5,000 &times; " + R + "5"),
   "10% fixed, so 90% variable", "2,500", "22,500", "4.50"]],
 headcls="lite", widths=["20%", "17%", "23%", "13%", "13%", "14%"])}
<p class="small">Each variable rate is the variable rupees divided by 5,000 units &mdash; for example
{R}24,000 &divide; 5,000 = {R}4.80 for selling. That rate stays the same at 7,000 units; it is the
fixed rupees beside it that stay the same in <i>total</i>.</p>"""

    main = flex("Flexible Budget", ["Output 5,000 units", "Output 7,000 units"],
      [("Materials", ["50.00", "2,50,000", "50.00", "3,50,000"]),
       ("Labour", ["20.00", "1,00,000", "20.00", "1,40,000"]),
       ("Variable overheads", ["15.00", "75,000", "15.00", "1,05,000"]),
       ("<b>Fixed overheads</b> " + src("total unchanged; per unit 50,000 &divide; 7,000 = 7.14"),
        ["10.00", "50,000", "<b>7.14</b>", "<b>50,000</b>"]),
       ("<i>Administrative expenses</i>", ["", "", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Variable (5%)", ["0.50", "2,500", "0.50", "3,500"]),
       ("&nbsp;&nbsp;&nbsp;Fixed (95%)", ["9.50", "47,500", "<b>6.79</b>", "<b>47,500</b>"]),
       ("<i>Selling expenses</i>", ["", "", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Fixed (20%)", ["1.20", "6,000", "<b>0.86</b>", "<b>6,000</b>"]),
       ("&nbsp;&nbsp;&nbsp;Variable (80%)", ["4.80", "24,000", "4.80", "33,600"]),
       ("<i>Distribution expenses</i>", ["", "", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Fixed (10%)", ["0.50", "2,500", "<b>0.36</b>", "<b>2,500</b>"]),
       ("&nbsp;&nbsp;&nbsp;Variable (90%)", ["4.50", "22,500", "4.50", "31,500"]),
       ("<b>TOTAL COST OF SALES</b>", ["<b>116.00</b>", "<b>5,80,000</b>",
                                       "<b>109.94</b>", "<b>7,69,600</b>"], "tot")],
      note="Every figure in bold is one that <b>changed its per-unit amount</b> while its total "
           "stayed the same. Those are exactly the fixed elements.")

    return ("<div class='prob long'>"
            + prob_head("Q1", "Flexible budget from a per-unit cost sheet",
                        "Flexible budget &middot; p.49")
            + question(q) + read(rd) + wn(wn1) + main
            + why(f"""<p>Look down the two &ldquo;per unit&rdquo; columns and the logic of a flexible
budget is visible at a glance. Materials stayed at {R}50, labour at {R}20, variable overhead at
{R}15 &mdash; and every fixed line fell. Nothing became cheaper to buy; the fixed cost is simply
spread thinner.</p>
{calc([f'Total fixed cost &nbsp;=&nbsp; 50,000 + 47,500 + 6,000 + 2,500 &nbsp;=&nbsp; '
       f'<b>{R}1,06,000</b> at either level',
       f'Total variable cost per unit &nbsp;=&nbsp; 50 + 20 + 15 + 0.50 + 4.80 + 4.50 &nbsp;=&nbsp; '
       f'<b>{R}94.80</b> at either level',
       f'Check at 7,000 units &nbsp;=&nbsp; (7,000 &times; 94.80) + 1,06,000 &nbsp;=&nbsp; '
       f'6,63,600 + 1,06,000 &nbsp;=&nbsp; <b>{R}7,69,600</b> &nbsp;&#10003;'])}
<p>That two-line check &mdash; total variable rate plus total fixed &mdash; will verify any flexible
budget in seconds, and it is the fastest way to catch a scaled fixed cost.</p>
<p class="small"><b>On the rounding:</b> {R}7,69,600 &divide; 7,000 = {R}109.94 exactly. Some
solutions round the column to {R}110. Show 109.94, because the total of {R}7,69,600 is what the
marks are on and 109.94 &times; 7,000 reproduces it.</p>""")
            + ans([("Total fixed cost (unchanged at both levels)", f"{R} 1,06,000"),
                   ("Total variable cost per unit", f"{R} 94.80"),
                   ("Total cost at 5,000 units", f"{R} 5,80,000 &nbsp;({R} 116.00 p.u.)"),
                   ("<b>Total cost at 7,000 units</b>",
                    f"<b>{R} 7,69,600 &nbsp;({R} 109.94 p.u.)</b>")])
            + "</div>")


# ======================================================================
# Q2
# ======================================================================
def q2():
    q = f"""<p>The following information at 50% capacity is given. Prepare a flexible budget and
forecast the profit or loss at 60%, 70% and 90% capacity.</p>
{table(None, [("Particulars", ""), ("Expenses at 50% capacity (" + R + ")", "r")],
 [{"cls": "sub", "cells": ["<b>Fixed expenses</b>", ""]},
  ["&nbsp;&nbsp;&nbsp;Salaries", "50,000"], ["&nbsp;&nbsp;&nbsp;Rent and taxes", "40,000"],
  ["&nbsp;&nbsp;&nbsp;Depreciation", "60,000"], ["&nbsp;&nbsp;&nbsp;Administrative expenses", "70,000"],
  {"cls": "sub", "cells": ["<b>Variable expenses</b>", ""]},
  ["&nbsp;&nbsp;&nbsp;Materials", "2,00,000"], ["&nbsp;&nbsp;&nbsp;Labour", "2,50,000"],
  ["&nbsp;&nbsp;&nbsp;Others", "40,000"],
  {"cls": "sub", "cells": ["<b>Semi-variable expenses</b>", ""]},
  ["&nbsp;&nbsp;&nbsp;Repairs", "1,00,000"], ["&nbsp;&nbsp;&nbsp;Indirect labour", "1,50,000"],
  ["&nbsp;&nbsp;&nbsp;Others", "90,000"]], headcls="lite", widths=["70%", "30%"])}
<p>It is estimated that fixed expenses will remain constant at all capacities. Semi-variable expenses
will not change between 45% and 61% capacity, will rise by 10% between 61% and 75% capacity, and a
further increase of 5% when capacity crosses 75%.</p>
<p>Estimated sales at various levels of capacity are: 60% &mdash; {R}11,00,000; 70% &mdash;
{R}13,00,000; 90% &mdash; {R}15,00,000.</p>"""

    rd = f"""<p>The question has already classified every cost for you. The only thinking needed is on
the semi-variable step rules, and they are stated in words that must be read very precisely.</p>
{table(None, [("Capacity asked for", "c"), ("Which band it falls in", ""),
              ("Cumulative uplift on the 50% figures", "c")],
 [["<b>60%</b>", "Inside &ldquo;will not change between 45% and 61%&rdquo;",
   "<b>no change</b> &mdash; use the 50% amounts as they stand"],
  ["<b>70%</b>", "Inside &ldquo;rise by 10% between 61% and 75%&rdquo;", "<b>&times; 1.10</b>"],
  ["<b>90%</b>", "Above 75%, so the 10% rise <b>and</b> the further 5%",
   "<b>&times; 1.10 &times; 1.05 = &times; 1.155</b>"]], headcls="lite",
 widths=["16%", "44%", "40%"])}
{bullets([
 '<b>The 90% uplift compounds.</b> &ldquo;A <i>further</i> increase of 5%&rdquo; means 5% on top of '
 'the 10% already applied, not 15% on the original. So the multiplier is 1.10 &times; 1.05 = '
 '<b>1.155</b>, giving ' + R + '1,15,500 for repairs rather than ' + R + '1,15,000.',
 '<b>Semi-variable does not mean it needs splitting here.</b> The question replaces the usual '
 'fixed/variable split with a step rule, so apply the step rule and nothing else.',
 '<b>Variable expenses scale on capacity, not on the step rule.</b> Divide the 50% figure by 50 to '
 'get the cost per 1% of capacity, then multiply by 60, 70 and 90.',
 'Sales are given only at the three higher levels, so the profit line begins at 60%. Leave the 50% '
 'profit cell blank rather than inventing a sales figure.'])}"""

    wn2 = f"""<h4 class="mini">W1 &nbsp;Variable expenses &mdash; cost per 1% of capacity</h4>
{table(None, [("Variable expense", ""), ("At 50% capacity " + R, "r"),
              ("Per 1% of capacity " + R, "r"), ("At 60%", "r"), ("At 70%", "r"), ("At 90%", "r")],
 [["Materials", "2,00,000", "4,000<br/>" + src("2,00,000 &divide; 50"),
   "2,40,000", "2,80,000", "3,60,000"],
  ["Labour", "2,50,000", "5,000<br/>" + src("2,50,000 &divide; 50"),
   "3,00,000", "3,50,000", "4,50,000"],
  ["Others", "40,000", "800<br/>" + src("40,000 &divide; 50"), "48,000", "56,000", "72,000"]],
 headcls="lite", widths=["20%", "17%", "19%", "14%", "14%", "16%"])}

<h4 class="mini">W2 &nbsp;Semi-variable expenses &mdash; applying the step rules</h4>
{table(None, [("Semi-variable expense", ""), ("At 50% " + R, "r"),
              ("At 60%<br/><span class='small'>no change</span>", "r"),
              ("At 70%<br/><span class='small'>&times; 1.10</span>", "r"),
              ("At 90%<br/><span class='small'>&times; 1.155</span>", "r")],
 [["Repairs", "1,00,000", "1,00,000", "1,10,000", "1,15,500"],
  ["Indirect labour", "1,50,000", "1,50,000", "1,65,000", "1,73,250"],
  ["Others", "90,000", "90,000", "99,000", "1,03,950"],
  {"cls": "tot", "cells": ["<b>Total semi-variable</b>", "<b>3,40,000</b>", "<b>3,40,000</b>",
                           "<b>3,74,000</b>", "<b>3,92,700</b>"]}],
 headcls="lite", widths=["24%", "19%", "19%", "19%", "19%"])}"""

    main = stmt("Flexible Budget and forecast of profit / loss",
      ["50% " + R, "60% " + R, "70% " + R, "90% " + R],
      [("<b>Fixed expenses</b>", ["", "", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Salaries", ["50,000", "50,000", "50,000", "50,000"]),
       ("&nbsp;&nbsp;&nbsp;Rent and taxes", ["40,000", "40,000", "40,000", "40,000"]),
       ("&nbsp;&nbsp;&nbsp;Depreciation", ["60,000", "60,000", "60,000", "60,000"]),
       ("&nbsp;&nbsp;&nbsp;Administrative expenses", ["70,000", "70,000", "70,000", "70,000"]),
       ("<b>Total fixed</b> " + src("constant at all capacities"),
        ["<b>2,20,000</b>", "<b>2,20,000</b>", "<b>2,20,000</b>", "<b>2,20,000</b>"], "sub"),
       ("<b>Variable expenses</b> " + src("W1"), ["", "", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Materials", ["2,00,000", "2,40,000", "2,80,000", "3,60,000"]),
       ("&nbsp;&nbsp;&nbsp;Labour", ["2,50,000", "3,00,000", "3,50,000", "4,50,000"]),
       ("&nbsp;&nbsp;&nbsp;Others", ["40,000", "48,000", "56,000", "72,000"]),
       ("<b>Total variable</b>",
        ["<b>4,90,000</b>", "<b>5,88,000</b>", "<b>6,86,000</b>", "<b>8,82,000</b>"], "sub"),
       ("<b>Semi-variable expenses</b> " + src("W2"), ["", "", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Repairs", ["1,00,000", "1,00,000", "1,10,000", "1,15,500"]),
       ("&nbsp;&nbsp;&nbsp;Indirect labour", ["1,50,000", "1,50,000", "1,65,000", "1,73,250"]),
       ("&nbsp;&nbsp;&nbsp;Others", ["90,000", "90,000", "99,000", "1,03,950"]),
       ("<b>Total semi-variable</b>",
        ["<b>3,40,000</b>", "<b>3,40,000</b>", "<b>3,74,000</b>", "<b>3,92,700</b>"], "sub"),
       ("<b>TOTAL COST</b>",
        ["<b>10,50,000</b>", "<b>11,48,000</b>", "<b>12,80,000</b>", "<b>14,94,700</b>"], "tot"),
       ("<b>SALES</b> " + src("given"),
        ["&mdash;", "<b>11,00,000</b>", "<b>13,00,000</b>", "<b>15,00,000</b>"], "sub"),
       ("<b>PROFIT / (LOSS)</b>",
        ["&mdash;", "<b>(48,000)</b>", "<b>20,000</b>", "<b>5,300</b>"], "tot")],
      widths=["36%", "16%", "16%", "16%", "16%"])

    return ("<div class='prob long'>"
            + prob_head("Q2", "Flexible budget across four capacity levels with step-rule semi-variables",
                        "Flexible budget &middot; p.49")
            + question(q) + read(rd) + wn(wn2) + main
            + why(f"""<p>The profit line is the interesting part of this answer, because it does
<b>not</b> rise steadily with capacity:</p>
{table(None, [("Capacity", "c"), ("Sales " + R, "r"), ("Total cost " + R, "r"),
              ("Profit / (Loss) " + R, "r"), ("What happened", "")],
 [["60%", "11,00,000", "11,48,000", "<b>(48,000)</b>",
   "Fixed and semi-variable costs are not yet covered"],
  ["70%", "13,00,000", "12,80,000", "<b>20,000</b>",
   "Sales rose " + R + "2,00,000 while cost rose only " + R + "1,32,000 &mdash; the firm moves into "
   "profit"],
  ["90%", "15,00,000", "14,94,700", "<b>5,300</b>",
   "Sales rose only " + R + "2,00,000 but cost rose " + R + "2,14,700 &mdash; profit "
   "<b>falls</b>"]], headcls="lite", widths=["10%", "16%", "16%", "16%", "42%"])}
<p><b>Profit peaks somewhere around 70% and then declines.</b> That is the finding management needs,
and stating it earns the last mark. Two things cause it:</p>
{bullets([
 '<b>The semi-variable step at 75%.</b> Crossing three-quarters capacity adds a further 5% to '
 'repairs, indirect labour and other semi-variable costs &mdash; ' + R + '18,700 of extra cost that '
 'arrives all at once, whether or not the extra output is worth having.',
 '<b>Sales are not keeping pace.</b> From 70% to 90% is twenty points of extra capacity for only ' +
 R + '2,00,000 more revenue, whereas the previous ten points brought in the same ' + R + '2,00,000. '
 'The selling price is evidently being cut to move the extra volume.'])}
<p><b>Recommendation:</b> operate at about 70% capacity. Pushing to 90% adds a fifth again to output
and yet <i>reduces</i> profit by {R}14,700. Nothing in the cost structure rewards the extra
volume.</p>""")
            + ans([("Total fixed cost &mdash; all levels", f"{R} 2,20,000"),
                   ("Total cost &mdash; 50% / 60%",
                    f"{R} 10,50,000 / {R} 11,48,000"),
                   ("Total cost &mdash; 70% / 90%",
                    f"{R} 12,80,000 / {R} 14,94,700"),
                   ("<b>Loss at 60% capacity</b>", f"<b>({R} 48,000)</b>"),
                   ("<b>Profit at 70% capacity</b>", f"<b>{R} 20,000</b>"),
                   ("<b>Profit at 90% capacity</b>", f"<b>{R} 5,300</b>"),
                   ("<b>Best level of operation</b>",
                    "<b>70% &mdash; profit falls beyond it</b>")])
            + "</div>")



# ======================================================================
# Q3
# ======================================================================
def q3():
    q = f"""<p>The following information relates to a flexible budget at 60% capacity. Find out the
overhead costs at 50% and 70% capacity and also determine the overhead rates:</p>
{table(None, [("Particulars", ""), ("Expenses at 60% capacity (" + R + ")", "r")],
 [{"cls": "sub", "cells": ["<b>Variable overheads</b>", ""]},
  ["&nbsp;&nbsp;&nbsp;Indirect labour", "10,500"], ["&nbsp;&nbsp;&nbsp;Indirect materials", "8,400"],
  {"cls": "sub", "cells": ["<b>Semi-variable overheads</b>", ""]},
  ["&nbsp;&nbsp;&nbsp;Repairs and maintenance (70% fixed, 30% variable)", "7,000"],
  ["&nbsp;&nbsp;&nbsp;Electricity (50% fixed, 50% variable)", "25,200"],
  {"cls": "sub", "cells": ["<b>Fixed overheads</b>", ""]},
  ["&nbsp;&nbsp;&nbsp;Office expenses including salaries", "70,000"],
  ["&nbsp;&nbsp;&nbsp;Insurance", "4,000"], ["&nbsp;&nbsp;&nbsp;Depreciation", "20,000"],
  ["&nbsp;&nbsp;&nbsp;Estimated direct labour hours", "1,20,000"]],
 headcls="lite", widths=["70%", "30%"])}"""

    rd = f"""<p>Two things make this problem different from Q2. The base level is <b>60%</b>, not 50%,
so every scaling is a fraction of sixty. And the semi-variable costs come with <b>explicit
percentages</b>, so they must be split into a fixed half and a variable half before scaling.</p>
{bullets([
 '<b>Scale on ' + frac("required %", "60") + ', not on ' + frac("required %", "50") + '.</b> To go '
 'from 60% to 50% multiply by ' + frac("50", "60") + '; to reach 70% multiply by ' + frac("70", "60")
 + '. Getting this base wrong corrupts every figure in the answer.',
 '<b>Split the semi-variables at the 60% level, then scale only the variable half.</b> Repairs: 70% '
 'of ' + R + '7,000 = ' + R + '4,900 fixed and ' + R + '2,100 variable. Electricity: 50/50, so ' +
 R + '12,600 each way.',
 '<b>The 1,20,000 direct labour hours is not an expense.</b> It sits in the middle of the cost list, '
 'which is a deliberate trap. It is the <b>base for the overhead rate</b>, and it scales with '
 'capacity: 1,00,000 hours at 50% and 1,40,000 at 70%.',
 '<b>&ldquo;Determine the overhead rates&rdquo;</b> means the recovery rate per direct labour hour '
 '&mdash; total overhead divided by labour hours, at each of the three levels.'])}"""

    wn3 = f"""<h4 class="mini">W1 &nbsp;Splitting the semi-variable overheads at 60% capacity</h4>
{table(None, [("Semi-variable overhead", ""), ("At 60% " + R, "r"), ("Split given", ""),
              ("Fixed portion " + R, "r"), ("Variable portion " + R, "r")],
 [["Repairs and maintenance", "7,000", "70% fixed / 30% variable",
   "4,900<br/>" + src("70% of 7,000"), "2,100<br/>" + src("30% of 7,000")],
  ["Electricity", "25,200", "50% fixed / 50% variable",
   "12,600<br/>" + src("50% of 25,200"), "12,600<br/>" + src("50% of 25,200")]],
 headcls="lite", widths=["24%", "14%", "24%", "19%", "19%"])}
<p class="small">Only the <b>variable portion</b> is then scaled. For repairs at 50% capacity:
{R}4,900 fixed + ({R}2,100 &times; {frac("50", "60")}) = {R}4,900 + {R}1,750 =
<b>{R}6,650</b>. At 70%: {R}4,900 + ({R}2,100 &times; {frac("70", "60")}) = {R}4,900 +
{R}2,450 = <b>{R}7,350</b>.</p>

<h4 class="mini">W2 &nbsp;Direct labour hours at each capacity</h4>
{calc([f'At 60% capacity &nbsp;=&nbsp; 1,20,000 hours &nbsp;(given)',
       f'At 50% capacity &nbsp;=&nbsp; 1,20,000 &times; {frac("50", "60")} &nbsp;=&nbsp; '
       f'<b>1,00,000 hours</b>',
       f'At 70% capacity &nbsp;=&nbsp; 1,20,000 &times; {frac("70", "60")} &nbsp;=&nbsp; '
       f'<b>1,40,000 hours</b>'])}"""

    main = stmt("Flexible Budget of overheads and overhead recovery rates",
      ["50% " + R, "60% " + R, "70% " + R],
      [("<b>Variable overheads</b>", ["", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Indirect labour " + src("10,500 &times; 50/60 and 70/60"),
        ["8,750", "10,500", "12,250"]),
       ("&nbsp;&nbsp;&nbsp;Indirect materials " + src("8,400 &times; 50/60 and 70/60"),
        ["7,000", "8,400", "9,800"]),
       ("<b>Semi-variable overheads</b> " + src("W1 &mdash; fixed half held, variable half scaled"),
        ["", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Repairs and maintenance", ["6,650", "7,000", "7,350"]),
       ("&nbsp;&nbsp;&nbsp;Electricity", ["23,100", "25,200", "27,300"]),
       ("<b>Fixed overheads</b>", ["", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Office expenses including salaries", ["70,000", "70,000", "70,000"]),
       ("&nbsp;&nbsp;&nbsp;Insurance", ["4,000", "4,000", "4,000"]),
       ("&nbsp;&nbsp;&nbsp;Depreciation", ["20,000", "20,000", "20,000"]),
       ("<b>TOTAL OVERHEAD COST</b>",
        ["<b>1,39,500</b>", "<b>1,45,100</b>", "<b>1,50,700</b>"], "tot"),
       ("Estimated direct labour hours " + src("W2"),
        ["1,00,000", "1,20,000", "1,40,000"], "sub"),
       ("<b>OVERHEAD RECOVERY RATE PER HOUR</b> " + src("total overhead &divide; labour hours"),
        ["<b>1.395</b>", "<b>1.209</b>", "<b>1.076</b>"], "tot")],
      widths=["40%", "20%", "20%", "20%"])

    return ("<div class='prob long'>"
            + prob_head("Q3", "Flexible budget of overheads and the overhead recovery rate",
                        "Flexible budget &middot; p.50")
            + question(q) + read(rd) + wn(wn3) + main
            + why(f"""<p>The three recovery rates are the real answer to this question, and they fall
as capacity rises &mdash; {R}1.395, {R}1.209, {R}1.076 per hour. That is the flexible-budget idea
expressed as a rate rather than as a total.</p>
{calc([f'Total overhead rises from {R}1,39,500 to {R}1,50,700 &mdash; an increase of only '
       f'<b>8.0%</b>',
       f'Direct labour hours rise from 1,00,000 to 1,40,000 &mdash; an increase of <b>40%</b>',
       f'So overhead <i>per hour</i> must fall, from {R}1.395 to {R}1.076 &mdash; a drop of '
       f'<b>22.9%</b>'])}
<p><b>Why this matters in practice.</b> If the company sets its absorption rate using the 50% figure
of {R}1.395 and then actually operates at 70%, it will over-absorb overhead and overstate its product
costs by nearly 30%. Quotations based on that rate would be too high, and the company would lose
tenders it could profitably have won. Choosing the right activity level for the absorption rate is one
of the practical reasons flexible budgets exist &mdash; worth a sentence in the answer.</p>""")
            + ans([("Total overhead &mdash; 50% capacity",
                    f"{R} 1,39,500 &nbsp;(rate {R} 1.395 / hour)"),
                   ("Total overhead &mdash; 60% capacity",
                    f"{R} 1,45,100 &nbsp;(rate {R} 1.209 / hour)"),
                   ("Total overhead &mdash; 70% capacity",
                    f"{R} 1,50,700 &nbsp;(rate {R} 1.076 / hour)"),
                   ("Direct labour hours &mdash; 50% / 60% / 70%",
                    "1,00,000 / 1,20,000 / 1,40,000")])
            + "</div>")


# ======================================================================
# Q4
# ======================================================================
def q4():
    q = f"""<p>With the following data for a 60% activity, prepare a budget for production at 80% and
100% capacity:</p>
{table(None, [("Particulars", ""), ("Amount", "r")],
 [["Production at 60% activity", "600 units"], ["Materials", R + "100 per unit"],
  ["Labour", R + "40 per unit"], ["Direct expenses", R + "10 per unit"],
  ["Factory overheads", R + "40,000 (40% fixed)"],
  ["Administrative expenses", R + "30,000 (60% fixed)"]], headcls="lite", widths=["60%", "40%"])}"""

    rd = f"""<p>Start by converting capacity into <b>units</b>, because every per-unit figure has to be
multiplied by a quantity.</p>
{calc([f'60% activity &nbsp;=&nbsp; 600 units, so 1% &nbsp;=&nbsp; 10 units',
       f'80% activity &nbsp;=&nbsp; <b>800 units</b> &nbsp;&nbsp;&nbsp;'
       f'100% activity &nbsp;=&nbsp; <b>1,000 units</b>'])}
{bullets([
 '<b>Materials, labour and direct expenses are given per unit</b>, so they are variable in full. '
 'Multiply straight through: ' + R + '100, ' + R + '40 and ' + R + '10 stay constant per unit at '
 'every level.',
 '<b>Factory overhead: 40% fixed</b> &rarr; ' + R + '16,000 fixed and ' + R + '24,000 variable at '
 '600 units, which is ' + R + '40 per unit variable.',
 '<b>Administrative expenses: 60% fixed</b> &rarr; ' + R + '18,000 fixed and ' + R + '12,000 '
 'variable at 600 units, which is ' + R + '20 per unit variable.',
 'Present both a <b>total</b> and a <b>per unit</b> column at each level, as the notes do. The '
 'per-unit column is where the falling fixed cost becomes visible, and it is what makes the answer '
 'a flexible budget rather than three separate budgets.'])}"""

    wn4 = f"""<h4 class="mini">W1 &nbsp;Splitting the two overhead lines at 600 units</h4>
{table(None, [("Overhead", ""), ("Total at 600 units " + R, "r"), ("Split given", ""),
              ("Fixed " + R, "r"), ("Variable " + R, "r"), ("Variable per unit " + R, "r")],
 [["Factory overheads", "40,000", "40% fixed, 60% variable",
   "16,000<br/>" + src("40% of 40,000"),
   "24,000<br/>" + src("60% of 40,000"), "40.00<br/>" + src("24,000 &divide; 600")],
  ["Administrative expenses", "30,000", "60% fixed, 40% variable",
   "18,000<br/>" + src("60% of 30,000"),
   "12,000<br/>" + src("40% of 30,000"), "20.00<br/>" + src("12,000 &divide; 600")]],
 headcls="lite", widths=["21%", "15%", "22%", "14%", "14%", "14%"])}"""

    main = flex("Flexible Budget",
      ["60% &mdash; 600 units", "80% &mdash; 800 units", "100% &mdash; 1,000 units"],
      [("Materials", ["100.00", "60,000", "100.00", "80,000", "100.00", "1,00,000"]),
       ("Labour", ["40.00", "24,000", "40.00", "32,000", "40.00", "40,000"]),
       ("Direct expenses", ["10.00", "6,000", "10.00", "8,000", "10.00", "10,000"]),
       ("<i>Factory overheads</i> " + src("W1"), ["", "", "", "", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Fixed (40%)",
        ["<b>26.67</b>", "16,000", "<b>20.00</b>", "16,000", "<b>16.00</b>", "16,000"]),
       ("&nbsp;&nbsp;&nbsp;Variable (60%)", ["40.00", "24,000", "40.00", "32,000", "40.00", "40,000"]),
       ("<i>Administrative expenses</i> " + src("W1"), ["", "", "", "", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Fixed (60%)",
        ["<b>30.00</b>", "18,000", "<b>22.50</b>", "18,000", "<b>18.00</b>", "18,000"]),
       ("&nbsp;&nbsp;&nbsp;Variable (40%)", ["20.00", "12,000", "20.00", "16,000", "20.00", "20,000"]),
       ("<b>TOTAL COST</b>", ["<b>266.67</b>", "<b>1,60,000</b>", "<b>252.50</b>", "<b>2,02,000</b>",
                              "<b>244.00</b>", "<b>2,44,000</b>"], "tot")],
      note="The four bold per-unit figures are the fixed elements. Their totals never move; their "
           "per-unit amounts fall as output rises.")

    return ("<div class='prob long'>"
            + prob_head("Q4", "Flexible budget at three activity levels, in total and per unit",
                        "Flexible budget &middot; p.50")
            + question(q) + read(rd) + wn(wn4) + main
            + why(f"""<p>Verify the answer with the two-line check, which works on any flexible
budget:</p>
{calc([f'Total variable cost per unit &nbsp;=&nbsp; 100 + 40 + 10 + 40 + 20 &nbsp;=&nbsp; '
       f'<b>{R}210</b>',
       f'Total fixed cost &nbsp;=&nbsp; 16,000 + 18,000 &nbsp;=&nbsp; <b>{R}34,000</b>',
       f'Check at 800 units &nbsp;=&nbsp; (800 &times; 210) + 34,000 &nbsp;=&nbsp; 1,68,000 + '
       f'34,000 &nbsp;=&nbsp; <b>{R}2,02,000</b> &nbsp;&#10003;',
       f'Check at 1,000 units &nbsp;=&nbsp; (1,000 &times; 210) + 34,000 &nbsp;=&nbsp; 2,10,000 + '
       f'34,000 &nbsp;=&nbsp; <b>{R}2,44,000</b> &nbsp;&#10003;'])}
<p><b>The falling unit cost is the finding to report:</b> {R}266.67 at 600 units, {R}252.50 at 800,
{R}244.00 at 1,000. Cost per unit falls by {R}22.67 &mdash; a little over 8% &mdash; purely from
spreading {R}34,000 of fixed cost across more units. No supplier gave a discount and no worker became
faster.</p>
<p class="small">This is also the arithmetic behind every &ldquo;economies of scale&rdquo; argument, and
it is why a firm quoting a price must always be asked <i>at what volume?</i> A quotation built on the
{R}266.67 figure and delivered at 1,000 units carries {R}22,670 of hidden margin.</p>""")
            + ans([("Units at 60% / 80% / 100%", "600 / 800 / 1,000 units"),
                   ("Total variable cost per unit", f"{R} 210"),
                   ("Total fixed cost (all levels)", f"{R} 34,000"),
                   ("<b>Total cost at 60% &mdash; 600 units</b>",
                    f"<b>{R} 1,60,000 &nbsp;({R} 266.67 p.u.)</b>"),
                   ("<b>Total cost at 80% &mdash; 800 units</b>",
                    f"<b>{R} 2,02,000 &nbsp;({R} 252.50 p.u.)</b>"),
                   ("<b>Total cost at 100% &mdash; 1,000 units</b>",
                    f"<b>{R} 2,44,000 &nbsp;({R} 244.00 p.u.)</b>")])
            + "</div>")


# ======================================================================
# Q13
# ======================================================================
def q13():
    q = f"""<p>The budget manager of Cosmetics Ltd. is preparing a budget for the accounting year
starting from 1st July. As part of the budget operations, some items of factory overhead costs have been
estimated by him under specified conditions of volume as follows:</p>
{table(None, [("Volume of production (units)", ""), ("1,20,000", "r"), ("1,50,000", "r")],
 [["Indirect materials", "2,64,000", "3,30,000"], ["Indirect labour", "1,50,000", "1,87,500"],
  ["Maintenance", "84,000", "1,02,000"], ["Supervision", "1,98,000", "2,34,000"],
  ["Engineering service", "94,000", "94,000"]], headcls="lite", widths=["52%", "24%", "24%"])}
<p>Calculate the cost of factory overhead items given above at 1,40,000 units of production.</p>"""

    rd = f"""<p>Costs at <b>two</b> volumes and a third volume asked for &mdash; that combination
always means the <b>high&ndash;low method</b>. But before reaching for it, classify each line, because
three of the five need no high&ndash;low work at all.</p>
{steps([
 '<b>Compute the cost per unit at each of the two volumes.</b> This one step classifies every line '
 'for you, and it is the step students skip.',
 '<b>If cost per unit is the SAME at both volumes &rarr; purely VARIABLE.</b> Just multiply by '
 '1,40,000.',
 '<b>If the TOTAL is the same at both volumes &rarr; purely FIXED.</b> Carry it across unchanged.',
 '<b>If cost per unit FALLS but the total rises &rarr; SEMI-VARIABLE.</b> Now use high&ndash;low:'
 + fml("Variable rate per unit &nbsp;=&nbsp; " + frac("Change in total cost", "Change in volume"))
 + fml("Fixed element &nbsp;=&nbsp; Total cost at either volume &nbsp;&minus;&nbsp; "
       "(Variable rate &times; that volume)")])}
{bullets([
 'The change in volume is always 1,50,000 &minus; 1,20,000 = <b>30,000 units</b> in this problem, so '
 'every variable rate is the cost difference divided by 30,000.',
 '<b>Check the fixed element from both volumes.</b> If it does not come out the same from the high '
 'point and the low point, the arithmetic is wrong. That is a free self-check.'])}"""

    cls_tbl = table("W1 &nbsp;Classifying the five overhead lines from the cost per unit",
      [("Overhead item", ""), ("Total at 1,20,000 " + R, "r"), ("Cost p.u. " + R, "r"),
       ("Total at 1,50,000 " + R, "r"), ("Cost p.u. " + R, "r"), ("Classification", "")],
      [["Indirect materials", "2,64,000", "2.20", "3,30,000", "2.20",
        "<b class='yes'>VARIABLE</b> &mdash; rate identical"],
       ["Indirect labour", "1,50,000", "1.25", "1,87,500", "1.25",
        "<b class='yes'>VARIABLE</b> &mdash; rate identical"],
       ["Maintenance", "84,000", "0.70", "1,02,000", "0.68",
        "<b>SEMI-VARIABLE</b> &mdash; rate falls"],
       ["Supervision", "1,98,000", "1.65", "2,34,000", "1.56",
        "<b>SEMI-VARIABLE</b> &mdash; rate falls"],
       ["Engineering service", "94,000", "0.783", "94,000", "0.627",
        "<b class='no'>FIXED</b> &mdash; total identical"]],
      headcls="lite", widths=["19%", "16%", "11%", "16%", "11%", "27%"])

    hl = f"""<h4 class="mini">W2 &nbsp;High&ndash;low segregation of the two semi-variable items</h4>
<p class="small"><b>Maintenance</b></p>
{calc([f'Variable rate &nbsp;=&nbsp; {frac(R + "1,02,000 &minus; " + R + "84,000", "1,50,000 &minus; 1,20,000")}'
       f' &nbsp;=&nbsp; {frac(R + "18,000", "30,000")} &nbsp;=&nbsp; <b>{R}0.60 per unit</b>',
       f'Fixed element &nbsp;=&nbsp; 84,000 &minus; (0.60 &times; 1,20,000) &nbsp;=&nbsp; '
       f'84,000 &minus; 72,000 &nbsp;=&nbsp; <b>{R}12,000</b>',
       f'Check from the high point &nbsp;=&nbsp; 1,02,000 &minus; (0.60 &times; 1,50,000) &nbsp;=&nbsp; '
       f'1,02,000 &minus; 90,000 &nbsp;=&nbsp; {R}12,000 &nbsp;&#10003;'])}
<p class="small"><b>Supervision</b></p>
{calc([f'Variable rate &nbsp;=&nbsp; {frac(R + "2,34,000 &minus; " + R + "1,98,000", "1,50,000 &minus; 1,20,000")}'
       f' &nbsp;=&nbsp; {frac(R + "36,000", "30,000")} &nbsp;=&nbsp; <b>{R}1.20 per unit</b>',
       f'Fixed element &nbsp;=&nbsp; 1,98,000 &minus; (1.20 &times; 1,20,000) &nbsp;=&nbsp; '
       f'1,98,000 &minus; 1,44,000 &nbsp;=&nbsp; <b>{R}54,000</b>',
       f'Check from the high point &nbsp;=&nbsp; 2,34,000 &minus; (1.20 &times; 1,50,000) &nbsp;=&nbsp; '
       f'2,34,000 &minus; 1,80,000 &nbsp;=&nbsp; {R}54,000 &nbsp;&#10003;'])}"""

    main = table("Factory Overhead Budget at 1,40,000 units of production",
      [("Particulars", ""), ("Basis of computation", ""), ("Amount " + R, "r")],
      [["Indirect materials", f"Variable at {R}2.20 per unit &nbsp;&rarr;&nbsp; 1,40,000 &times; 2.20",
        "3,08,000"],
       ["Indirect labour", f"Variable at {R}1.25 per unit &nbsp;&rarr;&nbsp; 1,40,000 &times; 1.25",
        "1,75,000"],
       {"cls": "sub", "cells": ["<b><i>Maintenance</i></b>", "semi-variable &mdash; W2", ""]},
       ["&nbsp;&nbsp;&nbsp;Fixed element", "constant at every volume", "12,000"],
       ["&nbsp;&nbsp;&nbsp;Variable element", f"{R}0.60 &times; 1,40,000", "84,000"],
       {"cls": "sub", "cells": ["<b><i>Supervision</i></b>", "semi-variable &mdash; W2", ""]},
       ["&nbsp;&nbsp;&nbsp;Fixed element", "constant at every volume", "54,000"],
       ["&nbsp;&nbsp;&nbsp;Variable element", f"{R}1.20 &times; 1,40,000", "1,68,000"],
       ["Engineering service", "Wholly fixed &mdash; unchanged at any volume", "94,000"],
       {"cls": "tot", "cells": ["<b>TOTAL FACTORY OVERHEAD at 1,40,000 units</b>", "",
                                "<b>8,95,000</b>"]}],
      widths=["27%", "50%", "23%"])

    return ("<div class='prob long'>"
            + prob_head("Q13", "High&ndash;low method &mdash; segregating semi-variable overheads",
                        "Cost segregation &middot; p.53")
            + question(q) + read(rd) + cls_tbl + wn(hl) + main
            + why(f"""<p>The high&ndash;low method rests on one observation: between two volumes, the
<b>only</b> thing that can make the total change is the variable element, because the fixed element by
definition did not move. So the whole of the cost increase must be variable, and dividing it by the
volume increase gives the rate per unit. Everything left over is fixed.</p>
{fml("The change in cost is entirely variable &nbsp;&rarr;&nbsp; "
     + frac("Change in cost", "Change in volume") + " &nbsp;=&nbsp; variable rate per unit",
     "Then substitute that rate back at either volume; whatever the variable element does not "
     "explain must be the fixed element. Doing it at BOTH volumes is a free check on your arithmetic.")}
<p><b>Cross-check the whole answer</b> by rebuilding it as fixed plus variable:</p>
{calc([f'Total variable rate &nbsp;=&nbsp; 2.20 + 1.25 + 0.60 + 1.20 &nbsp;=&nbsp; '
       f'<b>{R}5.25 per unit</b>',
       f'Total fixed cost &nbsp;=&nbsp; 12,000 + 54,000 + 94,000 &nbsp;=&nbsp; <b>{R}1,60,000</b>',
       f'At 1,40,000 units &nbsp;=&nbsp; (1,40,000 &times; 5.25) + 1,60,000 &nbsp;=&nbsp; '
       f'7,35,000 + 1,60,000 &nbsp;=&nbsp; <b>{R}8,95,000</b> &nbsp;&#10003;',
       f'And at 1,20,000 units &nbsp;=&nbsp; (1,20,000 &times; 5.25) + 1,60,000 &nbsp;=&nbsp; '
       f'{R}7,90,000, which is exactly the sum of the first column of the question &nbsp;&#10003;'])}
<p class="small"><b>A limitation worth stating.</b> High&ndash;low uses only two observations and
assumes the cost behaves in a straight line between them. It says nothing about what happens outside
the 1,20,000&ndash;1,50,000 range, and 1,40,000 units falls safely inside it &mdash; which is why the
answer can be relied on here. Extrapolating the same equation to, say, 2,50,000 units would not be
safe, because a step in supervision cost would almost certainly occur first.</p>""")
            + ans([("Indirect materials &mdash; variable", f"{R} 2.20 p.u. &rarr; {R} 3,08,000"),
                   ("Indirect labour &mdash; variable", f"{R} 1.25 p.u. &rarr; {R} 1,75,000"),
                   ("Maintenance &mdash; semi-variable",
                    f"Fixed {R} 12,000 + {R} 0.60 p.u. &rarr; {R} 96,000"),
                   ("Supervision &mdash; semi-variable",
                    f"Fixed {R} 54,000 + {R} 1.20 p.u. &rarr; {R} 2,22,000"),
                   ("Engineering service &mdash; fixed", f"{R} 94,000"),
                   ("<b>Total factory overhead at 1,40,000 units</b>", f"<b>{R} 8,95,000</b>")])
            + "</div>")


# ======================================================================
# Cash budget playbook, used by Q5, Q6, Q7
# ======================================================================
def cash_playbook():
    body = f"""
<p>A cash budget is not a profit statement. It records <b>only money actually moving</b>, and it
records it in the month it moves. Nothing else about these problems is difficult; everything depends
on getting the timing right.</p>

<div class="blk read"><span class="lab">The rule that makes cash budgets easy</span>
{fml("Never write a figure straight from the question into the cash budget.",
     "Build a WORKING NOTE for every item that has a credit period, get the month right there, and "
     "only then transfer the monthly totals into the budget. Every cash-budget mark in this module "
     "is won or lost in the working notes.")}
</div>

{steps([
 '<b>Working Note 1 &mdash; collections from customers.</b> Draw a grid with the sales months down '
 'the side and the budget months across the top. Take each month&rsquo;s sales, split it by the '
 'credit terms, and write each piece under the month it will be <b>received</b>. Then total each '
 'column.',
 '<b>Working Note 2 &mdash; any other item with a lag</b>, typically wages when part is &ldquo;paid '
 'in arrears&rdquo;. Same grid, same idea.',
 '<b>Payments to suppliers.</b> A credit period of one month means April pays for March&rsquo;s '
 'purchases; two months means April pays for February&rsquo;s. Just shift the row.',
 '<b>Now build the budget</b> in this fixed order &mdash; and keep it in this order every time, '
 'because the examiner is looking for it:'
 + calc(["Opening balance",
         "<i>Add:</i> Receipts &mdash; cash sales, collections from debtors, other income "
         "&nbsp;&rarr;&nbsp; <b>Total (A)</b>",
         "<i>Less:</i> Payments &mdash; suppliers, wages, expenses, tax, capital items "
         "&nbsp;&rarr;&nbsp; <b>Total (B)</b>",
         "<b>Closing balance = (A) &minus; (B)</b>, which becomes next month&rsquo;s opening balance"]),
 '<b>Carry the closing balance forward &mdash; including a negative one.</b> If April closes at '
 '(' + R + '47,000), May opens at (' + R + '47,000). This is where Q6 catches people out.'])}

<div class="blk why"><span class="lab">What goes in, and what never does</span>
{table(None, [("Item", ""), ("In a cash budget?", "c"), ("Note", "")],
 [["Cash sales", "<b class='yes'>YES</b>", "In the month of sale, less any cash discount allowed"],
  ["Collections from debtors", "<b class='yes'>YES</b>",
   "In the month received &mdash; use the working note"],
  ["Payments to creditors", "<b class='yes'>YES</b>", "In the month paid, per the credit period"],
  ["Wages and expenses", "<b class='yes'>YES</b>",
   "Watch for &ldquo;paid a month in arrears&rdquo; and for part-payment splits"],
  ["Income tax, advance tax", "<b class='yes'>YES</b>", "In the single month it falls due"],
  ["Rent paid quarterly in advance", "<b class='yes'>YES</b>",
   "The <b>whole quarter</b> in the due month &mdash; not one month&rsquo;s worth"],
  ["Income from investments", "<b class='yes'>YES</b>", "Only in the months it is actually received"],
  ["<b>Depreciation</b>", "<b class='no'>NEVER</b>", "Not a cash flow. The commonest error."],
  ["<b>Provisions, write-offs, bad debt provisions</b>", "<b class='no'>NEVER</b>",
   "Book entries only"],
  ["<b>Credit sales not yet collected</b>", "<b class='no'>NO</b>",
   "It is a debtor, not cash, until the month it is received"],
  ["<b>Opening / closing stock</b>", "<b class='no'>NO</b>",
   "Stock movements are not cash; the purchase that created the stock is"]],
 headcls="lite", widths=["31%", "16%", "53%"])}
</div>

<div class="blk trap"><span class="lab">The trap / where marks are lost</span>
{bullets([
 '<b>Forgetting the cash discount.</b> If 20% of sales are collected immediately &ldquo;discount '
 'allowed 2%&rdquo;, the cash received is 20% &times; 98%, not 20%. Q7 turns on this.',
 '<b>Treating a quarterly advance payment as monthly.</b> Rent of ' + R + '1,000 a month payable '
 'quarterly in advance in April means <b>' + R + '3,000 in April</b> and nothing in May or June.',
 '<b>Losing the sign on a negative closing balance.</b> Show it in brackets and carry it forward as '
 'a negative opening balance.',
 '<b>Not answering the actual question.</b> Q6 asks for the <i>extent of the bank facilities '
 'required</i>. The answer is the largest negative closing balance &mdash; say so explicitly, in '
 'words, at the end.'])}
</div>
"""
    return module_opener("Method", "Cash budgets &mdash; get the timing right and the rest is addition",
                         "Use these steps for Q5, Q6 and Q7", body)



# ======================================================================
# Q5
# ======================================================================
def q5():
    q = f"""<p>A company is expecting to have {R}32,000 cash in hand on 1.4.2008 and it requests you to
prepare a cash budget for the three months, April to June 2008. The following information is supplied
to you:</p>
{table(None, [("Month", ""), ("Sales " + R, "r"), ("Purchases " + R, "r"), ("Wages " + R, "r"),
              ("Expenses " + R, "r")],
 [["February", "70,000", "44,000", "6,000", "5,000"],
  ["March", "80,000", "56,000", "9,000", "6,000"],
  ["April", "96,000", "60,000", "9,000", "7,000"],
  ["May", "1,00,000", "68,000", "11,000", "9,000"],
  ["June", "1,20,000", "62,000", "14,000", "9,000"]], headcls="lite")}
<p>Other information:</p>
{bullets([
 '<b>a)</b> Period of credit allowed by suppliers is two months.',
 '<b>b)</b> 25% of sales are for cash and the period of credit allowed to customers for credit sales '
 'is one month.',
 '<b>c)</b> Delay in payment of wages and expenses one month.',
 '<b>d)</b> Income tax ' + R + '28,000 is to be paid in June 2008.'])}"""

    rd = f"""<p>Four credit terms, and each one shifts a different row by a different number of months.
Tabulate them before starting &mdash; this little table <i>is</i> the solution.</p>
{table(None, [("Item", ""), ("Term given", ""), ("So April&rsquo;s figure comes from &hellip;", "")],
 [["Cash sales (25%)", "received immediately", "<b>April&rsquo;s own sales</b> &times; 25%"],
  ["Credit sales (75%)", "one month&rsquo;s credit", "<b>March&rsquo;s sales</b> &times; 75%"],
  ["Purchases", "two months&rsquo; credit", "<b>February&rsquo;s purchases</b>"],
  ["Wages", "one month&rsquo;s delay", "<b>March&rsquo;s wages</b>"],
  ["Expenses", "one month&rsquo;s delay", "<b>March&rsquo;s expenses</b>"],
  ["Income tax", "due in June", "<b>June only</b> &mdash; nothing in April or May"]],
 headcls="lite", widths=["22%", "26%", "52%"])}
{bullets([
 '<b>Sales split into two rows, not one.</b> 25% arrives in the month of sale and 75% one month '
 'later, so April receives money from two different months&rsquo; sales. Keep them on separate lines '
 'in the budget &mdash; it is clearer and it earns the marks.',
 '<b>Two months&rsquo; credit on purchases is why February data is given.</b> If a month appears in '
 'the question but seems unused, you have missed a lag.',
 'February and March sales are needed only for their credit portion; February purchases only for the '
 'April payment. Nothing else from those two months is used.'])}"""

    wn5 = f"""<h4 class="mini">W1 &nbsp;Collection from debtors &mdash; 75% of sales, one month later</h4>
{table(None, [("Month of sale", ""), ("Sales " + R, "r"), ("Credit portion 75% " + R, "r"),
              ("Received in", "c"), ("April " + R, "r"), ("May " + R, "r"), ("June " + R, "r")],
 [["February", "70,000", "52,500", "March", "&mdash;", "&mdash;", "&mdash;"],
  ["March", "80,000", "60,000", "April", "<b>60,000</b>", "&mdash;", "&mdash;"],
  ["April", "96,000", "72,000", "May", "&mdash;", "<b>72,000</b>", "&mdash;"],
  ["May", "1,00,000", "75,000", "June", "&mdash;", "&mdash;", "<b>75,000</b>"],
  ["June", "1,20,000", "90,000", "July", "&mdash;", "&mdash;", "&mdash;"],
  {"cls": "tot", "cells": ["<b>Collected from debtors</b>", "", "", "",
                           "<b>60,000</b>", "<b>72,000</b>", "<b>75,000</b>"]}],
 headcls="lite", widths=["15%", "13%", "16%", "12%", "14%", "14%", "16%"])}
<p class="small">February&rsquo;s {R}52,500 is collected in March, which is before the budget period,
and June&rsquo;s {R}90,000 in July, which is after it. Both are shown so that the grid is complete and
the examiner can see the logic.</p>

<h4 class="mini">W2 &nbsp;Cash sales &mdash; 25% of the same month&rsquo;s sales</h4>
{calc([f'April &nbsp;=&nbsp; 25% of {R}96,000 &nbsp;=&nbsp; <b>{R}24,000</b>',
       f'May &nbsp;=&nbsp; 25% of {R}1,00,000 &nbsp;=&nbsp; <b>{R}25,000</b>',
       f'June &nbsp;=&nbsp; 25% of {R}1,20,000 &nbsp;=&nbsp; <b>{R}30,000</b>'])}"""

    main = stmt("Cash Budget for the three months from April to June 2008",
      ["April " + R, "May " + R, "June " + R],
      [("<b>Opening cash balance</b> " + src("32,000 given; thereafter the previous closing balance"),
        ["<b>32,000</b>", "<b>57,000</b>", "<b>82,000</b>"], "sub"),
       ("<i>Receipts</i>", ["", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Cash sales (25%) " + src("W2 &mdash; 25% of the same month's sales"),
        ["24,000", "25,000", "30,000"]),
       ("&nbsp;&nbsp;&nbsp;Collection from debtors (75%) " + src("W1 &mdash; last month's sales"),
        ["60,000", "72,000", "75,000"]),
       ("<b>TOTAL (A)</b>", ["<b>1,16,000</b>", "<b>1,54,000</b>", "<b>1,87,000</b>"], "tot"),
       ("<i>Payments</i>", ["", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Payment to suppliers " + src("2 months' credit &rarr; Feb, Mar, Apr purchases"),
        ["(44,000)", "(56,000)", "(60,000)"]),
       ("&nbsp;&nbsp;&nbsp;Wages " + src("1 month's delay &rarr; Mar, Apr, May wages"),
        ["(9,000)", "(9,000)", "(11,000)"]),
       ("&nbsp;&nbsp;&nbsp;Expenses " + src("1 month's delay &rarr; Mar, Apr, May expenses"),
        ["(6,000)", "(7,000)", "(9,000)"]),
       ("&nbsp;&nbsp;&nbsp;Income tax " + src("payable in June only"),
        ["&mdash;", "&mdash;", "(28,000)"]),
       ("<b>TOTAL (B)</b>", ["<b>(59,000)</b>", "<b>(72,000)</b>", "<b>(1,08,000)</b>"], "tot"),
       ("<b>CLOSING BALANCE (A &minus; B)</b>",
        ["<b>57,000</b>", "<b>82,000</b>", "<b>79,000</b>"], "tot")],
      widths=["40%", "20%", "20%", "20%"])

    return ("<div class='prob long'>"
            + prob_head("Q5", "Cash budget with four different credit periods",
                        "Cash budget &middot; p.50")
            + question(q) + read(rd) + wn(wn5) + main
            + why(f"""<p>The company is comfortably liquid throughout, closing at {R}57,000,
{R}82,000 and {R}79,000. No overdraft is needed.</p>
<p><b>The June dip is worth commenting on.</b> Cash grew for two months and then fell by
{R}3,000 in June &mdash; and it fell in the month with the <i>highest</i> sales of the whole period,
{R}1,20,000. That apparent contradiction is the most useful thing a cash budget shows:</p>
{bullets([
 'June collected only 25% of its own record sales, because 75% will not arrive until July. Sales '
 'growth <b>consumes</b> cash before it produces any.',
 'The ' + R + '28,000 income tax fell entirely in June. A single lumpy payment can reverse a healthy '
 'trend, and knowing the month in advance is exactly why the budget is prepared.'])}
<p><b>Recommendation:</b> no borrowing is required for April&ndash;June. But the pattern shows that
each further rise in sales will absorb cash for a month before releasing it, so if the growth in sales
continues beyond June the position should be re-tested for July onwards, when the
{R}90,000 owing from June is collected but a still larger sales figure may again outrun it.</p>""")
            + ans([("Opening balance, 1 April", f"{R} 32,000"),
                   ("Total receipts &mdash; April / May / June",
                    f"{R} 84,000 / {R} 97,000 / {R} 1,05,000"),
                   ("Total payments &mdash; April / May / June",
                    f"{R} 59,000 / {R} 72,000 / {R} 1,08,000"),
                   ("<b>Closing balance &mdash; April</b>", f"<b>{R} 57,000</b>"),
                   ("<b>Closing balance &mdash; May</b>", f"<b>{R} 82,000</b>"),
                   ("<b>Closing balance &mdash; June</b>", f"<b>{R} 79,000</b>"),
                   ("Overdraft required", "<b>None</b> &mdash; positive throughout")])
            + "</div>")


# ======================================================================
# Q6
# ======================================================================
def q6():
    q = f"""<p>XY Co. wishes to arrange overdraft facilities with its bankers during the period April to
June of a particular year, when it will be manufacturing mostly for stock. Prepare a cash budget for the
above period from the following data, indicating the extent of the bank facilities the company will
require at the end of each month:</p>
{table(None, [("Month", ""), ("Sales " + R, "r"), ("Purchases " + R, "r"), ("Wages " + R, "r")],
 [["February", "1,80,000", "1,24,800", "12,000"],
  ["March", "1,92,000", "1,44,000", "14,000"],
  ["April", "1,08,000", "2,43,000", "11,000"],
  ["May", "1,74,000", "2,46,000", "10,000"],
  ["June", "1,26,000", "2,68,000", "15,000"]], headcls="lite")}
{bullets([
 '<b>b)</b> 50% of the credit sales are realised in the month following the sales and the remaining '
 'sales in the second month following.',
 '<b>c)</b> Creditors are paid in the following month of purchase.',
 '<b>d)</b> Cash at bank on 1st April ' + R + '25,000.'])}"""

    rd = f"""<p>Read the story the numbers tell before you compute anything. <b>&ldquo;Manufacturing
mostly for stock&rdquo;</b> means purchases are rising steeply while sales fall &mdash; purchases go
from {R}1,44,000 to {R}2,68,000 as sales drop from {R}1,92,000 to {R}1,26,000. A cash crisis is
being built deliberately, and the question is how large it becomes.</p>
{bullets([
 '<b>There are no cash sales in this problem.</b> Every rupee of sales is on credit, collected 50% in '
 'the next month and 50% the month after. So each budget month collects from <b>two</b> earlier '
 'months.',
 '<b>Wages are paid in the same month</b> &mdash; no lag is mentioned, so do not invent one.',
 '<b>Creditors paid in the following month</b>, so April pays March&rsquo;s purchases of ' + R
 + '1,44,000, not April&rsquo;s ' + R + '2,43,000.',
 '<b>The closing balance will go negative and must be carried forward as a negative.</b> May opens '
 'with April&rsquo;s ' + R + '56,000 but June opens with May&rsquo;s <b>minus</b> ' + R + '47,000. '
 'This is the step that decides the problem.',
 '<b>Answer the question asked.</b> It wants the extent of the bank facility required at the end of '
 'each month &mdash; so state the overdraft figures in words at the end, not just the closing '
 'balances.'])}"""

    wn6 = f"""<h4 class="mini">W1 &nbsp;Collection from debtors &mdash; 50% in the next month, 50% in the second month</h4>
{table(None, [("Month of sale", ""), ("Sales " + R, "r"),
              ("50% received in the next month", ""), ("50% received two months later", ""),
              ("April " + R, "r"), ("May " + R, "r"), ("June " + R, "r")],
 [["February", "1,80,000", "March &mdash; 90,000", "<b>April &mdash; 90,000</b>",
   "<b>90,000</b>", "&mdash;", "&mdash;"],
  ["March", "1,92,000", "<b>April &mdash; 96,000</b>", "<b>May &mdash; 96,000</b>",
   "<b>96,000</b>", "<b>96,000</b>", "&mdash;"],
  ["April", "1,08,000", "<b>May &mdash; 54,000</b>", "<b>June &mdash; 54,000</b>",
   "&mdash;", "<b>54,000</b>", "<b>54,000</b>"],
  ["May", "1,74,000", "<b>June &mdash; 87,000</b>", "July &mdash; 87,000",
   "&mdash;", "&mdash;", "<b>87,000</b>"],
  ["June", "1,26,000", "July &mdash; 63,000", "August &mdash; 63,000",
   "&mdash;", "&mdash;", "&mdash;"],
  {"cls": "tot", "cells": ["<b>Total collected from debtors</b>", "", "", "",
                           "<b>1,86,000</b>", "<b>1,50,000</b>", "<b>1,41,000</b>"]}],
 headcls="lite", widths=["13%", "13%", "19%", "19%", "12%", "12%", "12%"])}
<p class="small">Read a column downwards to see the answer: April collects {R}90,000 from February
and {R}96,000 from March. June collects {R}54,000 from April and {R}87,000 from May.</p>"""

    main = stmt("Cash Budget for April to June",
      ["April " + R, "May " + R, "June " + R],
      [("<b>Opening balance</b> " + src("25,000 given; then the previous closing balance, negative included"),
        ["<b>25,000</b>", "<b>56,000</b>", "<b>(47,000)</b>"], "sub"),
       ("<i>Receipts</i>", ["", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Collection from debtors " + src("W1 &mdash; 50% + 50% from the two prior months"),
        ["1,86,000", "1,50,000", "1,41,000"]),
       ("<b>TOTAL (A)</b>", ["<b>2,11,000</b>", "<b>2,06,000</b>", "<b>94,000</b>"], "tot"),
       ("<i>Payments</i>", ["", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Payment to suppliers " + src("following month &rarr; Mar, Apr, May purchases"),
        ["(1,44,000)", "(2,43,000)", "(2,46,000)"]),
       ("&nbsp;&nbsp;&nbsp;Wages paid " + src("same month, no lag given"),
        ["(11,000)", "(10,000)", "(15,000)"]),
       ("<b>TOTAL (B)</b>", ["<b>(1,55,000)</b>", "<b>(2,53,000)</b>", "<b>(2,61,000)</b>"], "tot"),
       ("<b>CLOSING BALANCE (A &minus; B)</b>",
        ["<b>56,000</b>", "<b>(47,000)</b>", "<b>(1,67,000)</b>"], "tot")],
      widths=["40%", "20%", "20%", "20%"],
      note="A negative closing balance is an <b>overdraft</b>. Note carefully that May&rsquo;s "
           "closing balance of (" + R + "47,000) becomes June&rsquo;s <b>opening</b> balance, which "
           "is why June's total receipts of only " + R + "94,000 are less than the " +
           R + "1,41,000 collected.")

    facility = table("Extent of the bank facilities required &mdash; the answer to the question asked",
      [("End of month", ""), ("Closing balance " + R, "r"), ("Overdraft required " + R, "r"),
       ("Position", "")],
      [["April", "56,000", "<b>Nil</b>", "Cash surplus &mdash; no facility needed"],
       ["May", "(47,000)", "<b>47,000</b>", "Overdraft required"],
       {"cls": "tot",
        "cells": ["<b>June</b>", "<b>(1,67,000)</b>", "<b>1,67,000</b>",
                  "<b>Maximum facility needed</b>"]}],
      headcls="lite", widths=["16%", "22%", "22%", "40%"])

    return ("<div class='prob long'>"
            + prob_head("Q6", "Cash budget to establish the overdraft facility required",
                        "Cash budget &middot; p.51")
            + question(q) + read(rd) + wn(wn6) + main + facility
            + why(f"""<p><b>The company must arrange an overdraft facility of at least
{R}1,67,000</b>, and it should be in place before the end of May. That is the answer the question
asks for, and it should be stated in exactly those words.</p>
<p><b>Why the position deteriorates so fast.</b> Follow the two forces working against each other:</p>
{table(None, [("", ""), ("March", "r"), ("April", "r"), ("May", "r"), ("June", "r")],
 [["Purchases &mdash; cash goes out one month later", "1,44,000", "2,43,000", "2,46,000", "2,68,000"],
  ["Sales &mdash; cash comes in over the next two months", "1,92,000", "1,08,000", "1,74,000",
   "1,26,000"],
  {"cls": "tot", "cells": ["<b>Purchases in excess of sales</b>", "(48,000)", "<b>1,35,000</b>",
                           "<b>72,000</b>", "<b>1,42,000</b>"]}], headcls="lite",
 widths=["44%", "14%", "14%", "14%", "14%"])}
<p>The company is buying far more than it is selling &mdash; exactly what &ldquo;manufacturing mostly
for stock&rdquo; means. Cash is being converted into inventory. Worse, the timing compounds it: each
month&rsquo;s purchases are paid for in <b>one</b> month, while each month&rsquo;s sales are collected
over <b>two</b>. Money leaves twice as fast as it returns.</p>
<p class="small"><b>What to advise management.</b> The overdraft is the treatment, not the cure. If the
stock being built is genuinely needed for a seasonal peak, {R}1,67,000 of borrowing is a reasonable
cost of doing business and should be negotiated early &mdash; a facility arranged in advance is always
cheaper than one requested in crisis. If it is not, the buying programme should be slowed, or the
collection period shortened by offering a cash discount, which is the remedy Q7 illustrates.</p>""")
            + ans([("Opening balance, 1 April", f"{R} 25,000"),
                   ("Collections &mdash; April / May / June",
                    f"{R} 1,86,000 / {R} 1,50,000 / {R} 1,41,000"),
                   ("<b>Closing balance &mdash; April</b>", f"<b>{R} 56,000</b> &nbsp;surplus"),
                   ("<b>Closing balance &mdash; May</b>", f"<b>({R} 47,000)</b> &nbsp;overdrawn"),
                   ("<b>Closing balance &mdash; June</b>", f"<b>({R} 1,67,000)</b> &nbsp;overdrawn"),
                   ("<b>Bank facility required</b>",
                    f"<b>Nil in April, {R} 47,000 in May, {R} 1,67,000 in June</b>"),
                   ("<b>Maximum facility to arrange</b>", f"<b>{R} 1,67,000</b>")])
            + "</div>")


# ======================================================================
# Q7
# ======================================================================
def q7():
    q = f"""<p>From the following budget data, forecast the cash position at the end of April, May and
June 2016:</p>
{table(None, [("Month", ""), ("Sales " + R, "r"), ("Purchases " + R, "r"), ("Wages " + R, "r"),
              ("Misc. expenses " + R, "r")],
 [["February", "1,20,000", "84,000", "10,000", "7,000"],
  ["March", "1,30,000", "1,00,000", "12,000", "8,000"],
  ["April", "80,000", "1,04,000", "8,000", "6,000"],
  ["May", "1,16,000", "1,06,000", "10,000", "12,000"],
  ["June", "88,000", "80,000", "8,000", "6,000"]], headcls="lite")}
<p><b>Additional information:</b></p>
{bullets([
 '<b>Sales:</b> 20% realised in the month of sales, discount allowed 2%. Balance realised equally in '
 'two subsequent months.',
 '<b>Purchases:</b> paid in the month following the month of supply.',
 '<b>Wages:</b> 25% paid in arrears in the following month.',
 '<b>Miscellaneous expenses:</b> paid a month in arrears.',
 '<b>Rent:</b> ' + R + '1,000 per month, paid quarterly in advance, due in April.',
 '<b>Income tax:</b> first instalment of advance tax ' + R + '25,000 due on or before 15th June.',
 '<b>Income from investments:</b> ' + R + '5,000 received quarterly in April, July, etc.',
 '<b>Cash in hand:</b> ' + R + '5,000 on 1st April 2016.'])}"""

    rd = f"""<p>This is the hardest cash budget of the three because <b>seven</b> different timing
rules apply at once, and two of them are easy to get subtly wrong.</p>
{table(None, [("Item", ""), ("The rule", ""), ("The subtlety", "")],
 [["Cash sales", "20% in the month of sale, <b>less 2% discount</b>",
   "Cash received is 20% &times; 98% = <b>19.6%</b> of sales. Deducting the discount is the point of "
   "the sub-question."],
  ["Credit sales", "80% split <b>equally</b> over the two following months",
   "&ldquo;Equally&rdquo; means <b>40% each</b>, not 80% in one month."],
  ["Purchases", "paid the following month", "April pays March&rsquo;s " + R + "1,00,000"],
  ["Wages", "25% in arrears &rarr; <b>75% in the same month</b>",
   "Two wage lines are needed in the budget: 75% of this month plus 25% of last month."],
  ["Misc. expenses", "a month in arrears", "April pays March&rsquo;s " + R + "8,000"],
  ["Rent", "quarterly in advance, due April",
   "<b>" + R + "3,000 in April</b> for the whole quarter, and nothing in May or June."],
  ["Advance tax", "due by 15 June", "<b>June only</b>"],
  ["Investment income", "quarterly, in April", "<b>" + R + "5,000 in April</b> only"]],
 headcls="lite", widths=["16%", "37%", "47%"])}"""

    wn7 = f"""<h4 class="mini">W1 &nbsp;Collection from debtors &mdash; 80% split 40% and 40%</h4>
{table(None, [("Month of sale", ""), ("Sales " + R, "r"), ("Credit 80% " + R, "r"),
              ("40% in the next month", ""), ("40% two months later", ""),
              ("April " + R, "r"), ("May " + R, "r"), ("June " + R, "r")],
 [["February", "1,20,000", "96,000", "March &mdash; 48,000", "<b>April &mdash; 48,000</b>",
   "<b>48,000</b>", "&mdash;", "&mdash;"],
  ["March", "1,30,000", "1,04,000", "<b>April &mdash; 52,000</b>", "<b>May &mdash; 52,000</b>",
   "<b>52,000</b>", "<b>52,000</b>", "&mdash;"],
  ["April", "80,000", "64,000", "<b>May &mdash; 32,000</b>", "<b>June &mdash; 32,000</b>",
   "&mdash;", "<b>32,000</b>", "<b>32,000</b>"],
  ["May", "1,16,000", "92,800", "<b>June &mdash; 46,400</b>", "July &mdash; 46,400",
   "&mdash;", "&mdash;", "<b>46,400</b>"],
  ["June", "88,000", "70,400", "July &mdash; 35,200", "August &mdash; 35,200",
   "&mdash;", "&mdash;", "&mdash;"],
  {"cls": "tot", "cells": ["<b>Collected from debtors</b>", "", "", "", "",
                           "<b>1,00,000</b>", "<b>84,000</b>", "<b>78,400</b>"]}],
 headcls="lite", widths=["12%", "12%", "12%", "17%", "17%", "10%", "10%", "10%"])}

<h4 class="mini">W2 &nbsp;Cash sales &mdash; 20% of sales less 2% cash discount</h4>
{table(None, [("Month", ""), ("Sales " + R, "r"), ("20% " + R, "r"),
              ("<i>Less</i> 2% discount " + R, "r"), ("Cash received " + R, "r")],
 [["April", "80,000", "16,000", "(320)", "<b>15,680</b>"],
  ["May", "1,16,000", "23,200", "(464)", "<b>22,736</b>"],
  ["June", "88,000", "17,600", "(352)", "<b>17,248</b>"]],
 headcls="lite", widths=["16%", "21%", "21%", "21%", "21%"])}
<p class="small">Effectively 19.6% of sales is received in cash. The 2% discount is the price of
getting the money early &mdash; it never appears as a payment, it simply reduces the receipt.</p>

<h4 class="mini">W3 &nbsp;Wages &mdash; 75% in the month, 25% in the following month</h4>
{table(None, [("Month", ""), ("Wages " + R, "r"), ("75% paid in the month " + R, "r"),
              ("25% paid the next month " + R, "r"), ("Paid in", "c")],
 [["February", "10,000", "7,500", "2,500", "March"],
  ["March", "12,000", "9,000", "<b>3,000</b>", "<b>April</b>"],
  ["April", "8,000", "<b>6,000</b>", "<b>2,000</b>", "<b>April / May</b>"],
  ["May", "10,000", "<b>7,500</b>", "<b>2,500</b>", "<b>May / June</b>"],
  ["June", "8,000", "<b>6,000</b>", "2,000", "<b>June</b> / July"],
  {"cls": "tot", "cells": ["<b>Total wages paid</b>",
                           "<b>April 9,000</b>", "<b>May 9,500</b>", "<b>June 8,500</b>", ""]}],
 headcls="lite", widths=["14%", "16%", "24%", "24%", "22%"])}
<p class="small">April pays {R}6,000 (75% of April) + {R}3,000 (25% of March) = {R}9,000.
May pays {R}7,500 + {R}2,000 = {R}9,500. June pays {R}6,000 + {R}2,500 = {R}8,500.</p>"""

    main = stmt("Cash Budget for April to June 2016",
      ["April " + R, "May " + R, "June " + R],
      [("<b>Opening balance</b> " + src("5,000 given; then previous closing, negatives carried forward"),
        ["<b>5,000</b>", "<b>5,680</b>", "<b>(7,084)</b>"], "sub"),
       ("<i>Receipts</i>", ["", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Cash sales, net of 2% discount " + src("W2"),
        ["15,680", "22,736", "17,248"]),
       ("&nbsp;&nbsp;&nbsp;Collection from debtors " + src("W1 &mdash; 40% + 40%"),
        ["1,00,000", "84,000", "78,400"]),
       ("&nbsp;&nbsp;&nbsp;Income from investments " + src("quarterly &mdash; April only"),
        ["5,000", "&mdash;", "&mdash;"]),
       ("<b>TOTAL (A)</b>", ["<b>1,25,680</b>", "<b>1,12,416</b>", "<b>88,564</b>"], "tot"),
       ("<i>Payments</i>", ["", "", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Payment to creditors " + src("following month &rarr; Mar, Apr, May purchases"),
        ["(1,00,000)", "(1,04,000)", "(1,06,000)"]),
       ("&nbsp;&nbsp;&nbsp;Miscellaneous expenses " + src("one month in arrears &rarr; Mar, Apr, May"),
        ["(8,000)", "(6,000)", "(12,000)"]),
       ("&nbsp;&nbsp;&nbsp;Wages &mdash; 75% of the current month " + src("W3"),
        ["(6,000)", "(7,500)", "(6,000)"]),
       ("&nbsp;&nbsp;&nbsp;Wages &mdash; 25% outstanding from last month " + src("W3"),
        ["(3,000)", "(2,000)", "(2,500)"]),
       ("&nbsp;&nbsp;&nbsp;Rent " + src("quarterly in advance &mdash; " + R + "1,000 &times; 3 in April"),
        ["(3,000)", "&mdash;", "&mdash;"]),
       ("&nbsp;&nbsp;&nbsp;Advance income tax " + src("first instalment due by 15 June"),
        ["&mdash;", "&mdash;", "(25,000)"]),
       ("<b>TOTAL (B)</b>", ["<b>(1,20,000)</b>", "<b>(1,19,500)</b>", "<b>(1,51,500)</b>"], "tot"),
       ("<b>CLOSING BALANCE (A &minus; B)</b>",
        ["<b>5,680</b>", "<b>(7,084)</b>", "<b>(62,936)</b>"], "tot")],
      widths=["40%", "20%", "20%", "20%"])

    return ("<div class='prob long'>"
            + prob_head("Q7", "Cash budget with cash discount, split wages and quarterly items",
                        "Cash budget &middot; p.51&ndash;52")
            + question(q) + read(rd) + wn(wn7) + main
            + why(f"""<p>The forecast cash position is <b>{R}5,680 at the end of April, an overdraft
of {R}7,084 at the end of May, and an overdraft of {R}62,936 at the end of June</b>.</p>
<p><b>June is the month that breaks the position</b>, and three things arrive together:</p>
{bullets([
 '<b>The ' + R + '25,000 advance tax</b>, a single unavoidable payment that alone exceeds a '
 'third of the month&rsquo;s receipts.',
 '<b>April&rsquo;s poor sales of ' + R + '80,000 finally reach the cash book.</b> Because 40% of '
 'each month&rsquo;s sales arrives two months later, the weak April is still depressing June '
 'collections &mdash; only ' + R + '32,000 of the ' + R + '78,400 comes from April.',
 '<b>May&rsquo;s purchases of ' + R + '1,06,000 are paid in June</b> against June sales of only ' +
 R + '88,000. The company pays for a strong month out of the receipts of a weak one.'])}
<p><b>Recommendation:</b> arrange a facility of at least {R}65,000 before the end of May. Three
things would ease the position, and any of them is worth mentioning:</p>
{steps([
 'Negotiate two months&rsquo; credit from suppliers instead of one. That single change would defer ' +
 R + '1,06,000 out of June and turn the closing balance positive on its own.',
 'Extend the 2% cash discount to a larger share of sales. It costs 2% but converts a 40%/40% '
 'two-month wait into immediate cash, and the ' + R + '1,136 of discount given in June is trivial '
 'against a ' + R + '62,936 shortfall.',
 'Ask whether the advance tax can be met from a short-term facility rather than working capital, '
 'since it is a known, dated, one-off payment &mdash; precisely the kind of item a cash budget exists '
 'to give warning of.'])}""")
            + ans([("Opening balance, 1 April", f"{R} 5,000"),
                   ("Cash sales net of discount &mdash; Apr / May / Jun",
                    f"{R} 15,680 / {R} 22,736 / {R} 17,248"),
                   ("Collections from debtors &mdash; Apr / May / Jun",
                    f"{R} 1,00,000 / {R} 84,000 / {R} 78,400"),
                   ("Total payments &mdash; Apr / May / Jun",
                    f"{R} 1,20,000 / {R} 1,19,500 / {R} 1,51,500"),
                   ("<b>Closing balance &mdash; April</b>", f"<b>{R} 5,680</b>"),
                   ("<b>Closing balance &mdash; May</b>", f"<b>({R} 7,084)</b> &nbsp;overdrawn"),
                   ("<b>Closing balance &mdash; June</b>", f"<b>({R} 62,936)</b> &nbsp;overdrawn"),
                   ("<b>Facility to arrange</b>", f"<b>At least {R} 65,000 by end-May</b>")])
            + "</div>")



# ======================================================================
# Production / purchase budget playbook
# ======================================================================
def prod_playbook():
    body = f"""
<p>Four problems in this module (Q8, Q10, Q11, Q12) and two parts of Q15 use the <b>same single
formula</b>, applied first to finished goods and then to materials. Learn it once.</p>

<div class="blk read"><span class="lab">One formula, used twice</span>
{fml("What I must OBTAIN &nbsp;=&nbsp; What I will USE UP &nbsp;+&nbsp; What I want LEFT OVER "
     "&nbsp;&minus;&nbsp; What I ALREADY HAVE")}
{table(None, [("Applied to &hellip;", ""), ("What I will use up", ""), ("The formula becomes", "")],
 [["<b>Finished goods</b><br/>&rarr; the PRODUCTION budget",
   "Budgeted <b>sales</b> in units",
   "<b>Production = Sales + Closing stock of finished goods &minus; Opening stock</b>"],
  ["<b>Raw materials / parts</b><br/>&rarr; the PURCHASE budget",
   "Materials <b>consumed</b>, which comes from the production budget",
   "<b>Purchases = Consumption + Closing stock of materials &minus; Opening stock</b>"]],
 headcls="lite", widths=["27%", "30%", "43%"])}
<p><b>The order is compulsory.</b> You cannot compute the material budget until the production budget
is finished, because consumption depends on units <i>produced</i>, never on units <i>sold</i>.</p>
</div>

{steps([
 '<b>Production budget, in units.</b> Sales + closing stock &minus; opening stock, one column per '
 'product (or one column per month, if the question is month-wise).',
 '<b>Determine the closing stock properly.</b> The question always tells you how, and it is never the '
 'same twice: a flat figure (Q10, Q11, Q12), <b>50% of next month&rsquo;s sales</b> (Q8), or '
 '<b>90% of opening stock</b> (Q15). Read it carefully; this is the marked step.',
 '<b>Consumption of each material.</b> Units produced &times; the quantity of that material per '
 'unit, summed across all products.',
 '<b>Purchase budget, in units.</b> Consumption + closing stock of the material &minus; opening '
 'stock. If the question also gives <b>materials on order</b>, extend it:'
 + fml("Quantity to be ORDERED &nbsp;=&nbsp; Consumption &nbsp;+&nbsp; Closing stock "
       "&nbsp;+&nbsp; Closing orders outstanding &nbsp;&minus;&nbsp; Opening stock "
       "&nbsp;&minus;&nbsp; Opening orders outstanding",
       "Stock in hand is material you HAVE; material on order is material you have already "
       "ARRANGED to have. Both reduce what you must order afresh. Only Q11 needs this version."),
 '<b>Value it, if asked.</b> Multiply the purchase quantity by the price per unit to get the purchase '
 'budget in value.'])}

<div class="blk trap"><span class="lab">The trap / where marks are lost</span>
{bullets([
 '<b>Adding the opening stock and subtracting the closing.</b> It is the other way round. Sense-check '
 'it: if you want to <i>end</i> with more stock than you started with, you must produce <b>more</b> '
 'than you sell.',
 '<b>Using sales units to compute material consumption.</b> Always production units.',
 '<b>In a month-wise budget, forgetting that this month&rsquo;s closing stock is next month&rsquo;s '
 'opening stock.</b> They must chain, and if they do not, the columns will not add up.',
 '<b>In Q8, needing October&rsquo;s sales to finish September.</b> The closing stock for September is '
 '50% of <i>October&rsquo;s</i> sales. The question gives seven months of data for a six-month budget '
 'precisely for this reason &mdash; if a figure looks surplus, you have missed a step.'])}
</div>
"""
    return module_opener("Method", "Production and purchase budgets &mdash; one formula, applied twice",
                         "Use these steps for Q8, Q10, Q11, Q12 and Q15", body)


# ======================================================================
# Q8
# ======================================================================
def q8():
    q = f"""<p>A company is drawing its production plan for the year 2002&ndash;03 in respect of two of
its products &lsquo;Gamma&rsquo; and &lsquo;Delta&rsquo;. The company&rsquo;s policy is not to carry any
closing WIP at the end of any month. However, its policy is to hold a closing stock of finished goods at
50% of the anticipated quantity of sales of the succeeding month. For the year 2002&ndash;03 the
company&rsquo;s budgeted production is 20,000 units of &lsquo;Gamma&rsquo; and 25,000 of
&lsquo;Delta&rsquo;. The following is the estimated cost data:</p>
{table(None, [("Particulars", ""), ("Gamma", "r"), ("Delta", "r")],
 [["Direct material per unit", R + "50", R + "80"],
  ["Direct labour per unit", R + "20", R + "30"],
  ["Other manufacturing expenses apportionable to each type of product based on production",
   R + "2,00,000", R + "3,75,000"]], headcls="lite", widths=["58%", "21%", "21%"])}
<p>The estimated units to be sold in the first 7 months of the year 2002&ndash;03 are as under:</p>
{table(None, [("", ""), ("April", "r"), ("May", "r"), ("June", "r"), ("July", "r"), ("Aug", "r"),
              ("Sept", "r"), ("Oct", "r")],
 [["<b>Gamma</b>", "900", "1,100", "1,400", "1,800", "2,200", "2,200", "1,800"],
  ["<b>Delta</b>", "2,900", "2,900", "2,500", "2,100", "1,700", "1,700", "1,900"]],
 headcls="lite")}
<p><b>(a)</b> Prepare a production budget showing month-wise number of units to be manufactured.
<b>(b)</b> Present a summarised production cost budget for the half-year ending 30-09-2002.</p>"""

    rd = f"""<p>Two subtleties, and both are signposted by figures that look surplus.</p>
{bullets([
 '<b>Seven months of sales are given for a six-month budget.</b> October is needed because '
 'September&rsquo;s closing stock is 50% of <b>October&rsquo;s</b> sales. Whenever a question gives '
 'one extra period, that is why.',
 '<b>The opening stock of April is 50% of April&rsquo;s own sales</b> &mdash; because March&rsquo;s '
 'closing stock was set at 50% of the succeeding month&rsquo;s (that is, April&rsquo;s) sales. For '
 'Gamma that is 50% &times; 900 = 450 units. Students often leave April&rsquo;s opening stock blank.',
 '<b>Each month&rsquo;s closing stock is the next month&rsquo;s opening stock.</b> Write the closing '
 'row first, then copy it down one column to form the opening row. That chaining is a free '
 'self-check.',
 '<b>The 20,000 and 25,000 annual budgeted production figures are used only for part (b)</b>, to '
 'convert the lump-sum manufacturing expenses into a rate per unit:'
 + calc([f'Gamma &nbsp;=&nbsp; {frac(R + "2,00,000", "20,000 units")} &nbsp;=&nbsp; '
         f'<b>{R}10 per unit</b>',
         f'Delta &nbsp;=&nbsp; {frac(R + "3,75,000", "25,000 units")} &nbsp;=&nbsp; '
         f'<b>{R}15 per unit</b>']),
 '&ldquo;No closing WIP&rdquo; simply removes a complication &mdash; every unit started is finished, '
 'so units produced equals units completed.'])}"""

    gamma = stmt("(a) Production Budget &mdash; GAMMA, in units",
      ["April", "May", "June", "July", "Aug", "Sept"],
      [("Budgeted sales " + src("given"),
        ["900", "1,100", "1,400", "1,800", "2,200", "2,200"]),
       ("<i>Add:</i> Desired closing stock " + src("50% of NEXT month's sales"),
        ["550", "700", "900", "1,100", "1,100", "900"]),
       ("<b>Total requirement</b>",
        ["<b>1,450</b>", "<b>1,800</b>", "<b>2,300</b>", "<b>2,900</b>", "<b>3,300</b>",
         "<b>3,100</b>"], "sub"),
       ("<i>Less:</i> Opening stock " + src("= previous month's closing stock"),
        ["(450)", "(550)", "(700)", "(900)", "(1,100)", "(1,100)"]),
       ("<b>BUDGETED PRODUCTION</b>",
        ["<b>1,000</b>", "<b>1,250</b>", "<b>1,600</b>", "<b>2,000</b>", "<b>2,200</b>",
         "<b>2,000</b>"], "tot")],
      widths=["31%", "11.5%", "11.5%", "11.5%", "11.5%", "11.5%", "11.5%"],
      note="Closing stock working: April 50% &times; 1,100 (May) = 550 &middot; May 50% &times; 1,400 "
           "= 700 &middot; June 50% &times; 1,800 = 900 &middot; July 50% &times; 2,200 = 1,100 "
           "&middot; Aug 50% &times; 2,200 = 1,100 &middot; <b>Sept 50% &times; 1,800 (October) = "
           "900</b>. &nbsp;Total production for the half-year = <b>10,050 units</b>.")

    delta = stmt("(a) Production Budget &mdash; DELTA, in units",
      ["April", "May", "June", "July", "Aug", "Sept"],
      [("Budgeted sales " + src("given"),
        ["2,900", "2,900", "2,500", "2,100", "1,700", "1,700"]),
       ("<i>Add:</i> Desired closing stock " + src("50% of NEXT month's sales"),
        ["1,450", "1,250", "1,050", "850", "850", "950"]),
       ("<b>Total requirement</b>",
        ["<b>4,350</b>", "<b>4,150</b>", "<b>3,550</b>", "<b>2,950</b>", "<b>2,550</b>",
         "<b>2,650</b>"], "sub"),
       ("<i>Less:</i> Opening stock " + src("= previous month's closing stock"),
        ["(1,450)", "(1,450)", "(1,250)", "(1,050)", "(850)", "(850)"]),
       ("<b>BUDGETED PRODUCTION</b>",
        ["<b>2,900</b>", "<b>2,700</b>", "<b>2,300</b>", "<b>1,900</b>", "<b>1,700</b>",
         "<b>1,800</b>"], "tot")],
      widths=["31%", "11.5%", "11.5%", "11.5%", "11.5%", "11.5%", "11.5%"],
      note="Closing stock working: April 50% &times; 2,900 = 1,450 &middot; May 50% &times; 2,500 = "
           "1,250 &middot; June 50% &times; 2,100 = 1,050 &middot; July 50% &times; 1,700 = 850 "
           "&middot; Aug 50% &times; 1,700 = 850 &middot; <b>Sept 50% &times; 1,900 (October) = "
           "950</b>. &nbsp;Total production for the half-year = <b>13,300 units</b>.")

    cost = table("(b) Summarised Production Cost Budget for the half-year ending 30-09-2002",
      [("Particulars", ""), ("Gamma &mdash; 10,050 units", "c"), ("", "r"),
       ("Delta &mdash; 13,300 units", "c"), ("", "r")],
      [{"cls": "sub",
        "cells": ["", "<b>Cost p.u. " + R + "</b>", "<b>Total " + R + "</b>",
                  "<b>Cost p.u. " + R + "</b>", "<b>Total " + R + "</b>"]},
       ["Direct material", "50", "5,02,500<br/>" + src("10,050 &times; 50"),
        "80", "10,64,000<br/>" + src("13,300 &times; 80")],
       ["Direct labour", "20", "2,01,000<br/>" + src("10,050 &times; 20"),
        "30", "3,99,000<br/>" + src("13,300 &times; 30")],
       ["Other manufacturing expenses",
        "10<br/>" + src("2,00,000 &divide; 20,000"), "1,00,500<br/>" + src("10,050 &times; 10"),
        "15<br/>" + src("3,75,000 &divide; 25,000"), "1,99,500<br/>" + src("13,300 &times; 15")],
       {"cls": "tot", "cells": ["<b>TOTAL PRODUCTION COST</b>", "<b>80</b>", "<b>8,04,000</b>",
                                "<b>125</b>", "<b>16,62,500</b>"]},
       {"cls": "sub", "cells": ["<b>GRAND TOTAL &mdash; both products</b>", "", "", "",
                                "<b>" + R + "24,66,500</b>"]}],
      widths=["28%", "15%", "20%", "15%", "22%"])

    return ("<div class='prob long'>"
            + prob_head("Q8", "Month-wise production budget and production cost budget",
                        "Production budget &middot; p.51&ndash;52")
            + question(q) + read(rd) + gamma + delta + cost
            + why(f"""<p>Compare the two products and the production budget shows something the sales
budget alone cannot:</p>
{table(None, [("", ""), ("Gamma", "r"), ("Delta", "r")],
 [["Sales trend over the half-year", "900 &rarr; 2,200 &nbsp;<b>rising</b>",
   "2,900 &rarr; 1,700 &nbsp;<b>falling</b>"],
  ["Total sales for the half-year", "9,600 units", "13,700 units"],
  ["Total production for the half-year", "<b>10,050 units</b>", "<b>13,300 units</b>"],
  {"cls": "tot", "cells": ["<b>Production compared with sales</b>",
                           "<b>450 units MORE</b>", "<b>400 units LESS</b>"]}], headcls="lite")}
<p>Gamma must be over-produced and Delta under-produced, and the reason is the stock policy working in
opposite directions. Because closing stock is tied to <i>next</i> month&rsquo;s sales, a product with
rising sales has to keep building stock, while a product with falling sales can be allowed to run its
stock down.</p>
{calc([f'Gamma &nbsp;=&nbsp; sales 9,600 + closing stock 900 &minus; opening stock 450 &nbsp;=&nbsp; '
       f'<b>10,050 units</b> &nbsp;&#10003;',
       f'Delta &nbsp;=&nbsp; sales 13,700 + closing stock 950 &minus; opening stock 1,450 '
       f'&nbsp;=&nbsp; <b>13,300 units</b> &nbsp;&#10003;'])}
<p>That two-line check is worth doing every time: the six monthly columns must reconcile to the same
answer as the half-year taken as a whole. If they do not, a closing stock has been mis-chained.</p>
<p class="small"><b>A practical observation.</b> Total production of 23,350 units is fairly steady
month to month (Gamma rising, Delta falling), which is exactly what a factory wants &mdash; level
loading of labour and machinery. The stock policy, whatever its cost in working capital, is smoothing
production. Noting that shows you understand what a production budget is <i>for</i>.</p>""")
            + ans([("<b>(a) Gamma production</b> &mdash; Apr to Sept",
                    "<b>1,000 / 1,250 / 1,600 / 2,000 / 2,200 / 2,000</b>"),
                   ("&nbsp;&nbsp;&nbsp;&nbsp;Total Gamma", "<b>10,050 units</b>"),
                   ("<b>(a) Delta production</b> &mdash; Apr to Sept",
                    "<b>2,900 / 2,700 / 2,300 / 1,900 / 1,700 / 1,800</b>"),
                   ("&nbsp;&nbsp;&nbsp;&nbsp;Total Delta", "<b>13,300 units</b>"),
                   ("Other manufacturing expenses per unit", f"Gamma {R} 10 &middot; Delta {R} 15"),
                   ("<b>(b) Production cost &mdash; Gamma</b>",
                    f"<b>{R} 8,04,000 &nbsp;({R} 80 p.u.)</b>"),
                   ("<b>(b) Production cost &mdash; Delta</b>",
                    f"<b>{R} 16,62,500 &nbsp;({R} 125 p.u.)</b>"),
                   ("<b>(b) Grand total</b>", f"<b>{R} 24,66,500</b>")])
            + "</div>")


# ======================================================================
# Q10
# ======================================================================
def q10():
    q = f"""<p>From the following particulars, prepare a Production Budget of a company for the year
ended June 30, 2010.</p>
{table(None, [("Product", ""), ("Sales in units (as per sales budget)", "r"),
              ("Estimated stock 1 July 2009", "r"), ("Estimated stock 30 June 2010", "r")],
 [["<b>A</b>", "1,50,000", "14,000", "15,000"],
  ["<b>B</b>", "1,00,000", "5,000", "14,500"],
  ["<b>C</b>", "70,000", "8,000", "8,000"]], headcls="lite", widths=["16%", "30%", "27%", "27%"])}"""

    rd = f"""<p>The most direct application of the formula in the whole module. One line of arithmetic
per product &mdash; but be sure which stock figure is which.</p>
{bullets([
 '<b>1 July 2009 is the OPENING stock</b> (the year begins) and <b>30 June 2010 is the CLOSING '
 'stock</b> (the year ends). Sort the dates before you sort the numbers.',
 '<b>Add the closing, subtract the opening.</b> Product B must build stock from 5,000 to 14,500, so '
 'it has to produce 9,500 units <i>more</i> than it sells.',
 '<b>Product C is the check on your understanding:</b> opening and closing stock are both 8,000, so '
 'they cancel and production equals sales exactly. If you get anything other than 70,000 for C, the '
 'signs are the wrong way round.'])}"""

    main = stmt("Production Budget for the year ended 30 June 2010 (in units)",
      ["Product A", "Product B", "Product C"],
      [("Budgeted sales " + src("as per the sales budget"),
        ["1,50,000", "1,00,000", "70,000"]),
       ("<i>Add:</i> Desired closing stock " + src("estimated stock at 30 June 2010"),
        ["15,000", "14,500", "8,000"]),
       ("<b>Total requirement</b>", ["<b>1,65,000</b>", "<b>1,14,500</b>", "<b>78,000</b>"], "sub"),
       ("<i>Less:</i> Opening stock " + src("estimated stock at 1 July 2009"),
        ["(14,000)", "(5,000)", "(8,000)"]),
       ("<b>BUDGETED PRODUCTION</b>",
        ["<b>1,51,000</b>", "<b>1,09,500</b>", "<b>70,000</b>"], "tot")],
      widths=["40%", "20%", "20%", "20%"])

    return ("<div class='prob'>"
            + prob_head("Q10", "Production budget for three products",
                        "Production budget &middot; p.52&ndash;53")
            + question(q) + read(rd) + main
            + why(f"""<p>The three products illustrate the three possible relationships between
production and sales, which is almost certainly why the question was set this way:</p>
{table(None, [("Product", "c"), ("Stock movement", ""), ("Production vs sales", ""), ("Why", "")],
 [["<b>A</b>", "14,000 &rarr; 15,000, a rise of 1,000",
   "<b>1,000 units more</b>", "A small stock build must be produced in addition to sales"],
  ["<b>B</b>", "5,000 &rarr; 14,500, a rise of 9,500",
   "<b>9,500 units more</b>",
   "A large stock build &mdash; production must exceed sales by nearly 10%"],
  ["<b>C</b>", "8,000 &rarr; 8,000, no change", "<b>exactly equal</b>",
   "With no change in stock, everything produced is sold"]], headcls="lite",
 widths=["10%", "27%", "20%", "43%"])}
{fml("Production &minus; Sales &nbsp;=&nbsp; Closing stock &minus; Opening stock",
     "This is just the main formula rearranged, and it is the fastest way to check any production "
     "budget: the amount by which production differs from sales must equal the change in stock, "
     "nothing else.")}
<p class="small"><b>Worth adding for the extra mark:</b> Product B&rsquo;s stock is being taken from
5,000 units to 14,500 &mdash; nearly tripled. That is a substantial commitment of working capital and
storage space, and a budget manager would ask why. If it is preparation for an expected rise in demand
it is sound; if it is simply the result of over-production it should be challenged. A production budget
is a plan to be interrogated, not an arithmetic exercise.</p>""")
            + ans([("Product A &nbsp;(1,50,000 + 15,000 &minus; 14,000)",
                    "<b>1,51,000 units</b>"),
                   ("Product B &nbsp;(1,00,000 + 14,500 &minus; 5,000)", "<b>1,09,500 units</b>"),
                   ("Product C &nbsp;(70,000 + 8,000 &minus; 8,000)", "<b>70,000 units</b>"),
                   ("<b>Total budgeted production</b>", "<b>3,30,500 units</b>")])
            + "</div>")


# ======================================================================
# Q11
# ======================================================================
def q11():
    q = f"""<p>Draw a material procurement budget (quantitative) from the following information:</p>
<p>Estimated sales of a product are 40,000 units. Each unit of the product requires 3 units of material
A and 4 units of material B.</p>
{table("Estimated opening balances at the commencement of the next year",
 [("Particulars", ""), ("Units", "r")],
 [["Finished products", "5,000"], ["Material A", "12,000"], ["Material B", "20,000"],
  {"cls": "sub", "cells": ["<i>Materials on order</i>", ""]},
  ["&nbsp;&nbsp;&nbsp;Material A", "7,000"], ["&nbsp;&nbsp;&nbsp;Material B", "11,000"]],
 headcls="lite", widths=["72%", "28%"])}
{table("The desirable closing balances at the end of the next year",
 [("Particulars", ""), ("Units", "r")],
 [["Finished products", "7,000"], ["Material A", "15,000"], ["Material B", "25,000"],
  {"cls": "sub", "cells": ["<i>Materials on order</i>", ""]},
  ["&nbsp;&nbsp;&nbsp;Material A", "8,000"], ["&nbsp;&nbsp;&nbsp;Material B", "10,000"]],
 headcls="lite", widths=["72%", "28%"])}"""

    rd = f"""<p>The word <b>&ldquo;procurement&rdquo;</b> is the key. This is not asking how much
material to <i>receive</i>; it is asking how much to <b>order</b>. That is why the question gives
&ldquo;materials on order&rdquo; as well as materials in hand, and it is the only problem in the module
that does.</p>
{bullets([
 '<b>Three steps, in this order.</b> Production budget in units of finished product &rarr; material '
 'consumption &rarr; procurement budget. You cannot skip to the third.',
 '<b>Materials on order are material you have already arranged to have.</b> The 7,000 units of A on '
 'order at the start will arrive during the year without any fresh order being placed, so they reduce '
 'what must be ordered &mdash; exactly like opening stock. And the 8,000 you wish to have on order at '
 'the year end must be ordered during the year, so they increase it &mdash; exactly like closing '
 'stock.',
 '<b>Hence four adjustments, not two:</b>'
 + fml("Quantity to be PROCURED &nbsp;=&nbsp; Consumption &nbsp;+&nbsp; Closing stock in hand "
       "&nbsp;+&nbsp; Closing quantity on order &nbsp;&minus;&nbsp; Opening stock in hand "
       "&nbsp;&minus;&nbsp; Opening quantity on order"),
 '<b>Note that material B&rsquo;s orders on hand FALL</b>, from 11,000 to 10,000. So B&rsquo;s '
 'procurement is reduced by 1,000, while A&rsquo;s is increased by 1,000. The question changes the '
 'direction deliberately to test whether you have understood the sign rather than memorised a layout.'])}"""

    wnp = f"""<h4 class="mini">W1 &nbsp;Budgeted production of the finished product</h4>
{calc([f'Budgeted production &nbsp;=&nbsp; Budgeted sales + Closing stock &minus; Opening stock',
       f'&nbsp;=&nbsp; 40,000 + 7,000 &minus; 5,000 &nbsp;=&nbsp; <b>42,000 units</b>'])}

<h4 class="mini">W2 &nbsp;Materials consumed by that production</h4>
{calc([f'Material A &nbsp;=&nbsp; 42,000 units &times; 3 units per unit &nbsp;=&nbsp; '
       f'<b>1,26,000 units</b>',
       f'Material B &nbsp;=&nbsp; 42,000 units &times; 4 units per unit &nbsp;=&nbsp; '
       f'<b>1,68,000 units</b>'])}
<p class="small">Note the multiplication is by <b>42,000 units produced</b>, not by the 40,000 units
sold. Materials are consumed in the factory, not in the sales office.</p>"""

    main = stmt("Material Procurement Budget (quantitative), in units",
      ["Material A", "Material B"],
      [("Materials consumed " + src("W2 &mdash; 42,000 &times; 3 and 42,000 &times; 4"),
        ["1,26,000", "1,68,000"]),
       ("<i>Add:</i> Closing stock of material in hand", ["15,000", "25,000"]),
       ("<i>Add:</i> Closing quantity on order " + src("must be ordered during the year"),
        ["8,000", "10,000"]),
       ("<b>Total to be arranged</b>", ["<b>1,49,000</b>", "<b>2,03,000</b>"], "sub"),
       ("<i>Less:</i> Opening stock of material in hand", ["(12,000)", "(20,000)"]),
       ("<i>Less:</i> Opening quantity on order " + src("already ordered, will arrive anyway"),
        ["(7,000)", "(11,000)"]),
       ("<b>MATERIALS TO BE PROCURED</b>", ["<b>1,30,000</b>", "<b>1,72,000</b>"], "tot")],
      widths=["52%", "24%", "24%"])

    return ("<div class='prob long'>"
            + prob_head("Q11", "Material procurement budget, allowing for materials on order",
                        "Purchase budget &middot; p.53")
            + question(q) + read(rd) + wn(wnp) + main
            + why(f"""<p>The distinction this problem is really testing is between material
<b>received</b> during the year and material <b>ordered</b> during the year. They are different
numbers, and only one of them is a procurement budget:</p>
{table(None, [("", ""), ("Material A", "r"), ("Material B", "r"), ("Comment", "")],
 [["Consumption + closing stock &minus; opening stock",
   "1,29,000", "1,73,000", "the quantity that must be <b>received</b> during the year"],
  ["<i>Add:</i> closing orders outstanding", "8,000", "10,000",
   "ordered this year but arriving next year"],
  ["<i>Less:</i> opening orders outstanding", "(7,000)", "(11,000)",
   "ordered last year but arriving this year"],
  {"cls": "tot", "cells": ["<b>Quantity to be ORDERED &mdash; the procurement budget</b>",
                           "<b>1,30,000</b>", "<b>1,72,000</b>",
                           "<b>what the purchase department must actually do</b>"]}],
 headcls="lite", widths=["36%", "15%", "15%", "34%"])}
<p>Notice that the two adjustments push in opposite directions for the two materials. A ends the year
with <i>more</i> on order than it began with, so 1,000 extra units must be ordered. B ends with
<i>fewer</i>, so 1,000 fewer need be ordered. Both answers differ from the &ldquo;received&rdquo;
figure, and both differ in a different direction.</p>
<p class="small"><b>Why a firm holds orders outstanding at all.</b> Material on order is a buffer
against lead time. If material A takes six weeks to arrive, the company must always have roughly six
weeks&rsquo; consumption in the pipeline, or the factory stops. The procurement budget therefore has to
plan the pipeline as well as the shelf &mdash; which is precisely what the four adjustments above
do.</p>""")
            + ans([("Budgeted production &nbsp;(40,000 + 7,000 &minus; 5,000)",
                    "<b>42,000 units</b>"),
                   ("Material A consumed &nbsp;(42,000 &times; 3)", "1,26,000 units"),
                   ("Material B consumed &nbsp;(42,000 &times; 4)", "1,68,000 units"),
                   ("<b>Material A to be procured</b>", "<b>1,30,000 units</b>"),
                   ("<b>Material B to be procured</b>", "<b>1,72,000 units</b>")])
            + "</div>")


# ======================================================================
# Q12
# ======================================================================
def q12():
    q = f"""<p>The Sales Director of a manufacturing company reports that next year he expects to sell
50,000 units of a particular product. The Production Manager consults the store-keeper and casts his
figures as follows.</p>
<p>Two kinds of raw materials A and B are required for manufacturing the product. Each unit of the
product requires 2 units of A and 3 units of B. The estimated opening balances at the commencement of
the next year are:</p>
{table(None, [("Particulars", ""), ("Units", "r")],
 [["Finished products", "10,000"], ["Material A", "12,000"], ["Material B", "15,000"]],
 headcls="lite", widths=["72%", "28%"])}
<p>The desirable closing balances at the end of the next year are:</p>
{table(None, [("Particulars", ""), ("Units", "r")],
 [["Finished products", "14,000"], ["Material A", "13,000"], ["Material B", "16,000"]],
 headcls="lite", widths=["72%", "28%"])}
<p>Draw up a quantitative chart showing the materials purchase budget for the next year.</p>"""

    rd = f"""<p>Q11 without the &ldquo;materials on order&rdquo; complication &mdash; so the formula
has two adjustments, not four. Same three steps in the same order.</p>
{bullets([
 '<b>Production first.</b> 50,000 + 14,000 &minus; 10,000 = 54,000 units. The stock of finished goods '
 'is being increased by 4,000 units, so production must exceed sales by 4,000.',
 '<b>Then consumption</b>, at 2 units of A and 3 units of B for every unit produced &mdash; 54,000, '
 'not 50,000.',
 '<b>Then purchases</b>, adjusting only for the opening and closing stocks of the materials '
 'themselves.',
 'Both materials need a small stock increase of 1,000 units, so both purchase figures are 1,000 above '
 'consumption. That symmetry makes the answer easy to check.'])}"""

    wn12 = f"""<h4 class="mini">W1 &nbsp;Budgeted production</h4>
{calc([f'Budgeted production &nbsp;=&nbsp; Budgeted sales + Closing stock &minus; Opening stock',
       f'&nbsp;=&nbsp; 50,000 + 14,000 &minus; 10,000 &nbsp;=&nbsp; <b>54,000 units</b>'])}

<h4 class="mini">W2 &nbsp;Materials consumed</h4>
{calc([f'Material A &nbsp;=&nbsp; 54,000 &times; 2 &nbsp;=&nbsp; <b>1,08,000 units</b>',
       f'Material B &nbsp;=&nbsp; 54,000 &times; 3 &nbsp;=&nbsp; <b>1,62,000 units</b>'])}"""

    main = stmt("Materials Purchase Budget (quantitative), in units",
      ["Material A", "Material B"],
      [("Materials consumed " + src("W2 &mdash; 54,000 &times; 2 and 54,000 &times; 3"),
        ["1,08,000", "1,62,000"]),
       ("<i>Add:</i> Desired closing stock of material", ["13,000", "16,000"]),
       ("<b>Total requirement</b>", ["<b>1,21,000</b>", "<b>1,78,000</b>"], "sub"),
       ("<i>Less:</i> Opening stock of material", ["(12,000)", "(15,000)"]),
       ("<b>MATERIALS TO BE PURCHASED</b>", ["<b>1,09,000</b>", "<b>1,63,000</b>"], "tot")],
      widths=["52%", "24%", "24%"])

    return ("<div class='prob'>"
            + prob_head("Q12", "Materials purchase budget from a sales forecast",
                        "Purchase budget &middot; p.53&ndash;54")
            + question(q) + read(rd) + wn(wn12) + main
            + why(f"""<p>Trace the chain from the Sales Director&rsquo;s single figure to the
purchase order, because that chain <i>is</i> budgetary control:</p>
{calc([f'Sales Director says &nbsp;&rarr;&nbsp; <b>50,000 units</b> will be sold',
       f'Stock policy adds 4,000 &nbsp;&rarr;&nbsp; <b>54,000 units</b> must be produced',
       f'Bill of materials multiplies by 2 and 3 &nbsp;&rarr;&nbsp; <b>1,08,000 A</b> and '
       f'<b>1,62,000 B</b> will be consumed',
       f'Material stock policy adds 1,000 each &nbsp;&rarr;&nbsp; <b>1,09,000 A</b> and '
       f'<b>1,63,000 B</b> must be bought'])}
<p><b>Notice how the error would propagate.</b> If you had used the 50,000 sales figure instead of the
54,000 production figure, material A would come out at 1,01,000 instead of 1,09,000 &mdash; a shortfall
of 8,000 units, enough to stop production of 4,000 finished units. This is the single most common error
in the topic, and the reason the two figures are never allowed to be confused.</p>
<p class="small"><b>The link worth stating in the answer:</b> every figure above traces back to one
sales forecast. That is the strength of budgetary control &mdash; one plan, consistently followed
through every department &mdash; and also its weakness, because an error in the sales forecast is
faithfully reproduced in the purchase order. This is why sales budgets are prepared with the most care
and revised most often.</p>""")
            + ans([("Budgeted production &nbsp;(50,000 + 14,000 &minus; 10,000)",
                    "<b>54,000 units</b>"),
                   ("Material A consumed &nbsp;(54,000 &times; 2)", "1,08,000 units"),
                   ("Material B consumed &nbsp;(54,000 &times; 3)", "1,62,000 units"),
                   ("<b>Material A to be purchased</b>", "<b>1,09,000 units</b>"),
                   ("<b>Material B to be purchased</b>", "<b>1,63,000 units</b>")])
            + "</div>")



# ======================================================================
# Q9
# ======================================================================
def q9():
    q = f"""<p>A company produces and sells three items: (a) Snow Cream, (b) Talcum Powder and (c) Cold
Cream. The company has divided its market into two zones: Zone A and Zone B. The actual figures for the
previous year&rsquo;s sales were as under:</p>
{table(None, [("Product", ""), ("Zone A &mdash; Units", "r"), ("Zone A &mdash; Unit price " + R, "r"),
              ("Zone B &mdash; Units", "r"), ("Zone B &mdash; Unit price " + R, "r")],
 [["<b>Snow Cream</b>", "4,00,000", "12.00", "2,50,000", "12.00"],
  ["<b>Talcum Powder</b>", "2,50,000", "15.00", "3,50,000", "15.00"],
  ["<b>Cold Cream</b>", "3,00,000", "16.00", "3,00,000", "16.00"]], headcls="lite")}
<p>For the current year, it is estimated that sales of Snow Cream will go up by 10% in Zone B and of
Cold Cream by 25,000 units in Zone A. The company plans to introduce a publicity film for Talcum Powder
on the T.V. network. The budgeted figures for Talcum Powder are to be increased by 20% in both zones.</p>
<p>The prices of the two creams are to be maintained but for Talcum Powder a bonus cut of {R}1 will be
announced.</p>
<p>You are required to prepare a quantitative-cum-financial budget for sales in the current year.</p>"""

    rd = f"""<p>&ldquo;Quantitative-cum-financial&rdquo; means show <b>both</b> the units and the value
&mdash; two columns for every product. The difficulty is that each of the three products changes in a
<i>different way</i>, and one of the changes applies to only one zone.</p>
{table(None, [("Product", ""), ("Quantity change", ""), ("Which zone", ""), ("Price change", "")],
 [["<b>Snow Cream</b>", "<b>up 10%</b>", "<b>Zone B only</b> &mdash; Zone A unchanged",
   "none &mdash; &ldquo;prices of the two creams are to be maintained&rdquo;"],
  ["<b>Talcum Powder</b>", "<b>up 20%</b>", "<b>both zones</b>",
   "<b>down " + R + "1</b> &mdash; the bonus cut, so " + R + "15 becomes " + R + "14"],
  ["<b>Cold Cream</b>", "<b>up 25,000 units</b> (not a percentage)",
   "<b>Zone A only</b> &mdash; Zone B unchanged", "none &mdash; a cream, so price maintained"]],
 headcls="lite", widths=["17%", "24%", "27%", "32%"])}
{bullets([
 '<b>&ldquo;The two creams&rdquo;</b> means Snow Cream and Cold Cream. Only Talcum Powder gets the '
 'price cut &mdash; and the phrase is the examiner&rsquo;s way of telling you so without saying it '
 'directly.',
 '<b>Cold Cream rises by an absolute 25,000 units, not by 25%.</b> Read the units of measurement; '
 'the workbook mixes percentages and absolutes on purpose.',
 '<b>A &ldquo;bonus cut&rdquo; is a price reduction.</b> ' + R + '15 &minus; ' + R + '1 = ' + R
 + '14, applied in <b>both</b> zones.',
 'Set out the answer zone by zone, with a total row. The zone totals are what a sales manager is '
 'actually held responsible for.'])}"""

    main = table("Quantitative-cum-Financial Budget for Sales &mdash; current year",
      [("Zone", ""),
       ("Snow Cream &nbsp;<span class='small'>at " + R + "12</span>", "c"), ("", "r"),
       ("Talcum Powder &nbsp;<span class='small'>at " + R + "14</span>", "c"), ("", "r"),
       ("Cold Cream &nbsp;<span class='small'>at " + R + "16</span>", "c"), ("", "r")],
      [{"cls": "sub",
        "cells": ["", "<b>Units</b>", "<b>Value " + R + "</b>", "<b>Units</b>",
                  "<b>Value " + R + "</b>", "<b>Units</b>", "<b>Value " + R + "</b>"]},
       ["<b>Zone A</b>",
        "4,00,000<br/>" + src("no change"), "48,00,000",
        "3,00,000<br/>" + src("2,50,000 &times; 1.20"), "42,00,000",
        "3,25,000<br/>" + src("3,00,000 + 25,000"), "52,00,000"],
       ["<b>Zone B</b>",
        "2,75,000<br/>" + src("2,50,000 &times; 1.10"), "33,00,000",
        "4,20,000<br/>" + src("3,50,000 &times; 1.20"), "58,80,000",
        "3,00,000<br/>" + src("no change"), "48,00,000"],
       {"cls": "tot",
        "cells": ["<b>TOTAL</b>", "<b>6,75,000</b>", "<b>81,00,000</b>", "<b>7,20,000</b>",
                  "<b>1,00,80,000</b>", "<b>6,25,000</b>", "<b>1,00,00,000</b>"]}],
      widths=["10%", "14%", "16%", "14%", "16%", "14%", "16%"])

    grand = stmt("Summary of the sales budget", ["Units", "Value " + R],
      [("Snow Cream", ["6,75,000", "81,00,000"]),
       ("Talcum Powder", ["7,20,000", "1,00,80,000"]),
       ("Cold Cream", ["6,25,000", "1,00,00,000"]),
       ("<b>TOTAL BUDGETED SALES</b>", ["<b>20,20,000</b>", "<b>2,81,80,000</b>"], "tot"),
       ("<i>Zone A total</i>", ["<i>10,25,000</i>", "<i>1,42,00,000</i>"], "sub"),
       ("<i>Zone B total</i>", ["<i>9,95,000</i>", "<i>1,39,80,000</i>"], "sub")],
      widths=["56%", "22%", "22%"])

    return ("<div class='prob long'>"
            + prob_head("Q9", "Quantitative-cum-financial sales budget by product and zone",
                        "Sales budget &middot; p.52")
            + question(q) + read(rd) + main + grand
            + why(f"""<p><b>The Talcum Powder decision deserves comment, because that is where the
management question lies.</b> The company is spending money on a television campaign <i>and</i> cutting
the price by {R}1. Was it worth it?</p>
{table(None, [("Talcum Powder", ""), ("Previous year", "r"), ("Current year budget", "r"),
              ("Change", "r")],
 [["Units &mdash; both zones", "6,00,000", "7,20,000", "<b>+1,20,000 &nbsp;(+20%)</b>"],
  ["Price per unit", "15.00", "14.00", "<b>&minus;1.00 &nbsp;(&minus;6.7%)</b>"],
  {"cls": "tot", "cells": ["<b>Sales value</b>", "<b>90,00,000</b>", "<b>1,00,80,000</b>",
                           "<b>+10,80,000 &nbsp;(+12%)</b>"]}], headcls="lite",
 widths=["34%", "22%", "22%", "22%"])}
<p>Sales value rises by {R}10,80,000, so on the face of it the plan works. But two cautions belong in
the answer:</p>
{bullets([
 '<b>The revenue gain is not the profit gain.</b> Against the ' + R + '10,80,000 the company must set '
 'the cost of the television film and the variable cost of making 1,20,000 extra units. Only if '
 'contribution exceeds the publicity cost is the plan sound &mdash; and this budget does not tell us, '
 'because a sales budget stops at revenue.',
 '<b>The price cut applies to ALL units, not only the extra ones.</b> The 6,00,000 units that would '
 'have sold anyway now yield ' + R + '1 less each &mdash; ' + R + '6,00,000 of revenue given away to '
 'win ' + R + '16,80,000 of new business. That is the real trade the ' + R + '10,80,000 conceals.'])}
<p class="small"><b>Also worth observing:</b> the two zones are now almost exactly balanced &mdash;
{R}1,42,00,000 against {R}1,39,80,000 &mdash; whereas the products are not. Cold Cream sells 3,25,000
units in Zone A but only 3,00,000 in Zone B, while Talcum Powder sells 4,20,000 in Zone B against
3,00,000 in Zone A. A zone-wise budget of this kind exists precisely to expose such differences, so
that selling effort can be directed where a product is weak.</p>""")
            + ans([("Snow Cream &mdash; Zone A / Zone B",
                    "4,00,000 / 2,75,000 units"),
                   ("Talcum Powder &mdash; Zone A / Zone B",
                    "3,00,000 / 4,20,000 units at " + R + " 14"),
                   ("Cold Cream &mdash; Zone A / Zone B", "3,25,000 / 3,00,000 units"),
                   ("<b>Snow Cream total</b>", f"<b>6,75,000 units = {R} 81,00,000</b>"),
                   ("<b>Talcum Powder total</b>", f"<b>7,20,000 units = {R} 1,00,80,000</b>"),
                   ("<b>Cold Cream total</b>", f"<b>6,25,000 units = {R} 1,00,00,000</b>"),
                   ("<b>Total budgeted sales</b>",
                    f"<b>20,20,000 units = {R} 2,81,80,000</b>")])
            + "</div>")


# ======================================================================
# Q14
# ======================================================================
def q14():
    q = f"""<p>A company requires you to prepare a Master Budget from the following:</p>
<p><b>Sales per annum:</b> Product A &mdash; {R}40,00,000; Product B &mdash; {R}60,00,000.</p>
<p><b>Other information:</b></p>
{bullets([
 'Direct material cost = 40% of sales',
 'Direct wages: 15 workers @ ' + R + '12,000 per month per worker',
 'Factory overheads: works manager&rsquo;s salary at ' + R + '20,000 per month, foreman&rsquo;s '
 'salary at ' + R + '15,000 per month',
 'Stores and spares: 2&frac12;% on sales; depreciation on machinery ' + R + '1,26,000 per annum',
 'Light and power: ' + R + '50,000 p.a.; Repairs and maintenance: ' + R + '80,000 per annum; '
 'Miscellaneous expenses: 10% of direct wages',
 'Administration, selling and distribution expenses: ' + R + '1,40,000 p.a.'])}"""

    rd = f"""<p>A master budget is simply a <b>budgeted profit and loss account</b>. Every item is
given; the work is in converting each one to an annual figure on the right base.</p>
{table(None, [("Item as given", ""), ("Base", ""), ("Annual computation", "")],
 [["Sales", "given annually", R + "40,00,000 + " + R + "60,00,000 = <b>" + R + "1,00,00,000</b>"],
  ["Direct material", "<b>% of sales</b>", "40% &times; 1,00,00,000 = <b>" + R + "40,00,000</b>"],
  ["Direct wages", "<b>per worker per MONTH</b>",
   "15 &times; 12,000 &times; <b>12</b> = <b>" + R + "21,60,000</b>"],
  ["Works manager&rsquo;s salary", "<b>per month</b>",
   "20,000 &times; 12 = <b>" + R + "2,40,000</b>"],
  ["Foreman&rsquo;s salary", "<b>per month</b>", "15,000 &times; 12 = <b>" + R + "1,80,000</b>"],
  ["Stores and spares", "<b>% of sales</b>",
   "2.5% &times; 1,00,00,000 = <b>" + R + "2,50,000</b>"],
  ["Miscellaneous expenses", "<b>% of direct WAGES</b>",
   "10% &times; 21,60,000 = <b>" + R + "2,16,000</b>"],
  ["Depreciation, light and power, repairs, admin", "already annual",
   "take as given &mdash; 1,26,000 + 50,000 + 80,000 + 1,40,000"]],
 headcls="lite", widths=["27%", "20%", "53%"])}
{bullets([
 '<b>The two &times;12 conversions are where the marks are lost.</b> Both salaries and the wages are '
 'quoted per month; everything else is already annual. Mixing them understates cost by lakhs.',
 '<b>Miscellaneous expenses are 10% of direct WAGES, not of sales.</b> Read the base attached to '
 'every percentage &mdash; this question uses three different bases (sales, sales, wages) in three '
 'consecutive lines.',
 '<b>Depreciation belongs in a master budget</b>, unlike in a cash budget. A master budget measures '
 'profit, and depreciation is a charge against profit.',
 'Product A and B are given only as sales values, with no separate cost data, so the master budget is '
 'prepared for the company as a whole. Show the two products in the sales line and then work with the '
 'total.'])}"""

    main = table("MASTER BUDGET &mdash; Budgeted Profit and Loss Account for the year",
      [("Particulars", ""), ("Basis", ""), (R, "r"), (R, "r")],
      [{"cls": "sub", "cells": ["<b>Sales</b>", "", "", ""]},
       ["&nbsp;&nbsp;&nbsp;Product A", "given", "40,00,000", ""],
       ["&nbsp;&nbsp;&nbsp;Product B", "given", "60,00,000", ""],
       {"cls": "sub", "cells": ["<b>Total Sales</b>", "", "", "<b>1,00,00,000</b>"]},
       {"cls": "sub", "cells": ["<b><i>Less:</i> Cost of Goods Sold</b>", "", "", ""]},
       ["&nbsp;&nbsp;&nbsp;Direct materials", "40% of sales", "40,00,000", ""],
       ["&nbsp;&nbsp;&nbsp;Direct wages", "15 workers &times; 12,000 &times; 12 months",
        "21,60,000", ""],
       {"cls": "sub", "cells": ["&nbsp;&nbsp;&nbsp;<i>Factory overheads</i>", "", "", ""]},
       ["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Works manager&rsquo;s salary",
        "20,000 &times; 12", "2,40,000", ""],
       ["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Foreman&rsquo;s salary", "15,000 &times; 12",
        "1,80,000", ""],
       ["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Stores and spares", "2&frac12;% of sales",
        "2,50,000", ""],
       ["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Depreciation on machinery", "given, per annum",
        "1,26,000", ""],
       ["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Light and power", "given, per annum", "50,000", ""],
       ["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Repairs and maintenance", "given, per annum",
        "80,000", ""],
       ["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Miscellaneous expenses", "10% of direct wages",
        "2,16,000", ""],
       ["&nbsp;&nbsp;&nbsp;Administration, selling and distribution", "given, per annum",
        "1,40,000", ""],
       {"cls": "sub", "cells": ["<b>Total Cost</b>", "", "", "<b>(74,42,000)</b>"]},
       {"cls": "tot", "cells": ["<b>BUDGETED PROFIT</b>", "", "", "<b>25,58,000</b>"]}],
      widths=["36%", "30%", "17%", "17%"])

    return ("<div class='prob long'>"
            + prob_head("Q14", "Master budget &mdash; the budgeted profit and loss account",
                        "Master budget &middot; p.54")
            + question(q) + read(rd) + main
            + why(f"""<p>The master budget is the point at which every other budget in the module comes
together. It answers the question the board actually asks: <b>if all these plans are carried out, what
profit will we make?</b> Here the answer is {R}25,58,000, a margin of 25.58% on sales.</p>
{table(None, [("Analysis of the budgeted cost", ""), (R, "r"), ("% of sales", "r")],
 [["Direct materials", "40,00,000", "40.00%"],
  ["Direct wages", "21,60,000", "21.60%"],
  {"cls": "sub", "cells": ["<b>Prime cost</b>", "<b>61,60,000</b>", "<b>61.60%</b>"]},
  ["Factory overheads", "11,42,000", "11.42%"],
  ["Administration, selling and distribution", "1,40,000", "1.40%"],
  {"cls": "sub", "cells": ["<b>Total cost</b>", "<b>74,42,000</b>", "<b>74.42%</b>"]},
  {"cls": "tot", "cells": ["<b>Budgeted profit</b>", "<b>25,58,000</b>", "<b>25.58%</b>"]}],
 headcls="lite", widths=["56%", "22%", "22%"])}
<p><b>What the percentage column is for.</b> Once the budget is expressed as a percentage of sales it
becomes a control document rather than a forecast. If the actual results come in with materials at 43%
of sales instead of 40%, that is a {R}3,00,000 problem which can be investigated in the month it
arises &mdash; and Module 6 is entirely about measuring such differences.</p>
<p class="small"><b>One structural observation worth a mark.</b> Only two of the eleven cost lines vary
with sales &mdash; direct materials and stores and spares, together 42.5% of sales. Everything else,
including all the wages, is fixed for the year. So a 10% shortfall in sales would cut revenue by
{R}10,00,000 but costs by only {R}4,25,000, taking profit down by {R}5,75,000 &mdash; more than a
fifth. A high proportion of fixed cost makes budgeted profit very sensitive to the sales forecast, which
is exactly the risk the master budget exists to make visible.</p>""")
            + ans([("Total sales", f"{R} 1,00,00,000"),
                   ("Direct materials &nbsp;(40% of sales)", f"{R} 40,00,000"),
                   ("Direct wages &nbsp;(15 &times; 12,000 &times; 12)", f"{R} 21,60,000"),
                   ("Factory overheads", f"{R} 11,42,000"),
                   ("Administration, selling and distribution", f"{R} 1,40,000"),
                   ("<b>Total budgeted cost</b>", f"<b>{R} 74,42,000</b>"),
                   ("<b>BUDGETED PROFIT</b>", f"<b>{R} 25,58,000</b>"),
                   ("Profit as a percentage of sales", "<b>25.58%</b>")])
            + "</div>")



# ======================================================================
# Q15
# ======================================================================
def q15():
    q = f"""<p>A company manufactures three products A, B and C and sells at {R}450, {R}550 and
{R}650 per unit respectively. The ratio of sales in quantity of A, B and C is <b>1 : 2 : 4</b>. Other
information for the three products:</p>
{table(None, [("Product", ""), ("D", "r"), ("E", "r"), ("F", "r"), ("G", "r"),
              ("Skilled hours", "r"), ("Unskilled hours", "r"),
              ("Variable overheads p.u. " + R, "r")],
 [["<b>A</b>", "1", "10", "2", "8", "6", "8", "9"],
  ["<b>B</b>", "1", "2", "14", "10", "4", "6", "11"],
  ["<b>C</b>", "1", "6", "10", "2", "3", "6", "7"]], headcls="lite")}
<p>The present purchase price per part is {R}45, {R}15, {R}15 and {R}5 for D, E, F and G
respectively. The wage rate per hour is skilled worker {R}6 and unskilled {R}5.</p>
<p>The opening stock is 500, 1,000, 3,000, 1,500, 1,000, 20,000 and 10,000 for A, B, C, D, E, F and G.
The closing stock of the product and the parts is <b>90% of the opening stock</b>.</p>
<p>The workers work for 8 hours a day for 25 days in a month. The share of fixed overhead per month for
A, B and C comes to {R}15,75,000, {R}5,80,000 and {R}8,45,000 respectively. The yearly profit
projected is {R}1,20,00,000.</p>
<p>Prepare the following budgets for the next fiscal month: <b>(a)</b> Sales budget in quantity and
value; <b>(b)</b> Production budget; <b>(c)</b> Parts usage budget; <b>(d)</b> Purchase budget in
quantity and value; <b>(e)</b> Man power budget showing labour hours and wages payable;
<b>(f)</b> Master budget.</p>"""

    rd = f"""<p>The hardest problem in the module, but only because of its length. The trick is that
<b>you are not told the sales quantity</b> &mdash; you must work it out backwards from the profit
target. Do that first and the remaining five budgets fall out in order.</p>
{steps([
 '<b>Build the cost per unit of each product</b> from the parts and the labour hours. Three small '
 'tables: raw material cost, labour cost, then total variable cost.',
 '<b>Find the sales quantity from the profit target.</b> Let A = <i>x</i>, so B = 2<i>x</i> and '
 'C = 4<i>x</i>. Compute total contribution in terms of <i>x</i>, set it equal to monthly fixed '
 'overhead plus monthly profit, and solve.',
 '<b>Then the five budgets in strict order:</b> sales &rarr; production &rarr; parts usage &rarr; '
 'purchases &rarr; man power &rarr; master budget. Each one feeds the next.'])}
{bullets([
 '<b>&ldquo;The yearly profit projected&rdquo; but &ldquo;budgets for the next fiscal MONTH&rdquo;.</b> '
 'Divide ' + R + '1,20,00,000 by 12 to get a monthly profit of ' + R + '10,00,000. The fixed overhead '
 'figures are already monthly. Mixing the two periods is the single biggest trap in the question.',
 '<b>Closing stock is 90% of OPENING stock</b> &mdash; so stock is being run down by 10%, and '
 'production will be slightly <i>less</i> than sales for every product.',
 '<b>8 hours &times; 25 days = 200 hours per worker per month.</b> Needed only for part (e), to '
 'convert hours into a number of workers.',
 '<b>Every product uses exactly 1 unit of part D</b>, which is a useful check: total D consumption '
 'must equal total units produced.'])}"""

    rmc = table("W1 &nbsp;Raw material (parts) cost per unit of product",
      [("Part", ""), ("Price " + R, "r"),
       ("A &mdash; nos.", "r"), ("A &mdash; " + R, "r"),
       ("B &mdash; nos.", "r"), ("B &mdash; " + R, "r"),
       ("C &mdash; nos.", "r"), ("C &mdash; " + R, "r")],
      [["<b>D</b>", "45", "1", "45", "1", "45", "1", "45"],
       ["<b>E</b>", "15", "10", "150", "2", "30", "6", "90"],
       ["<b>F</b>", "15", "2", "30", "14", "210", "10", "150"],
       ["<b>G</b>", "5", "8", "40", "10", "50", "2", "10"],
       {"cls": "tot", "cells": ["<b>Raw material cost per unit</b>", "", "", "<b>265</b>", "",
                                "<b>335</b>", "", "<b>295</b>"]}],
      headcls="lite", widths=["12%", "11%", "13%", "13%", "13%", "13%", "12%", "13%"])

    lab = table("W2 &nbsp;Labour cost per unit of product",
      [("Labour", ""), ("Rate per hour " + R, "r"),
       ("A &mdash; hrs", "r"), ("A &mdash; " + R, "r"),
       ("B &mdash; hrs", "r"), ("B &mdash; " + R, "r"),
       ("C &mdash; hrs", "r"), ("C &mdash; " + R, "r")],
      [["<b>Skilled</b>", "6", "6", "36", "4", "24", "3", "18"],
       ["<b>Unskilled</b>", "5", "8", "40", "6", "30", "6", "30"],
       {"cls": "tot", "cells": ["<b>Labour cost per unit</b>", "", "<b>14</b>", "<b>76</b>",
                                "<b>10</b>", "<b>54</b>", "<b>9</b>", "<b>48</b>"]}],
      headcls="lite", widths=["14%", "14%", "12%", "12%", "12%", "12%", "12%", "12%"])

    vc = stmt("W3 &nbsp;Total variable cost and contribution per unit",
      ["A " + R, "B " + R, "C " + R],
      [("Raw material cost " + src("W1"), ["265", "335", "295"]),
       ("Labour cost " + src("W2"), ["76", "54", "48"]),
       ("Variable overheads " + src("given"), ["9", "11", "7"]),
       ("<b>Total variable cost per unit</b>", ["<b>350</b>", "<b>400</b>", "<b>350</b>"], "sub"),
       ("Selling price per unit " + src("given"), ["450", "550", "650"]),
       ("<b>CONTRIBUTION PER UNIT</b>", ["<b>100</b>", "<b>150</b>", "<b>300</b>"], "tot")],
      widths=["46%", "18%", "18%", "18%"])

    solve = f"""<h4 class="mini">W4 &nbsp;Finding the sales quantity from the profit target</h4>
<p class="small">Let the sales quantity of A be <i>x</i>. The ratio 1 : 2 : 4 then gives B = 2<i>x</i>
and C = 4<i>x</i>.</p>
{table(None, [("Product", ""), ("Quantity", "r"), ("Contribution per unit " + R, "r"),
              ("Total contribution " + R, "r")],
 [["A", "<i>x</i>", "100", "100<i>x</i>"],
  ["B", "2<i>x</i>", "150", "300<i>x</i>"],
  ["C", "4<i>x</i>", "300", "1,200<i>x</i>"],
  {"cls": "tot", "cells": ["<b>Total</b>", "7<i>x</i>", "", "<b>1,600<i>x</i></b>"]}],
 headcls="lite", widths=["16%", "20%", "30%", "34%"])}
{calc([f'Total fixed overhead per month &nbsp;=&nbsp; 15,75,000 + 5,80,000 + 8,45,000 &nbsp;=&nbsp; '
       f'<b>{R}30,00,000</b>',
       f'Profit required per month &nbsp;=&nbsp; {frac(R + "1,20,00,000", "12 months")} '
       f'&nbsp;=&nbsp; <b>{R}10,00,000</b>',
       f'Contribution needed &nbsp;=&nbsp; Fixed overhead + Profit &nbsp;=&nbsp; 30,00,000 + '
       f'10,00,000 &nbsp;=&nbsp; <b>{R}40,00,000</b>'])}
{fml("1,600<i>x</i> &nbsp;=&nbsp; " + R + "40,00,000 &nbsp;&nbsp;&rarr;&nbsp;&nbsp; <i>x</i> "
     "&nbsp;=&nbsp; " + frac("40,00,000", "1,600") + " &nbsp;=&nbsp; <b>2,500 units</b>",
     "So A = 2,500 units, B = 5,000 units and C = 10,000 units for the month.")}"""

    sales = stmt("(a) SALES BUDGET in quantity and value", ["A", "B", "C", "Total"],
      [("Sales ratio " + src("given, 1 : 2 : 4"), ["<i>x</i>", "2<i>x</i>", "4<i>x</i>", "7<i>x</i>"]),
       ("<b>Sales quantity (units)</b> " + src("W4 &mdash; x = 2,500"),
        ["<b>2,500</b>", "<b>5,000</b>", "<b>10,000</b>", "<b>17,500</b>"], "sub"),
       ("Selling price per unit " + R, ["450", "550", "650", "&mdash;"]),
       ("<b>TOTAL BUDGETED SALES</b> " + R,
        ["<b>11,25,000</b>", "<b>27,50,000</b>", "<b>65,00,000</b>", "<b>1,03,75,000</b>"], "tot")],
      widths=["36%", "16%", "16%", "16%", "16%"])

    prod = stmt("(b) PRODUCTION BUDGET, in units", ["A", "B", "C"],
      [("Budgeted sales " + src("from the sales budget"), ["2,500", "5,000", "10,000"]),
       ("<i>Add:</i> Closing stock " + src("90% of opening stock"),
        ["450", "900", "2,700"]),
       ("<b>Total requirement</b>", ["<b>2,950</b>", "<b>5,900</b>", "<b>12,700</b>"], "sub"),
       ("<i>Less:</i> Opening stock " + src("given"), ["(500)", "(1,000)", "(3,000)"]),
       ("<b>BUDGETED PRODUCTION</b>", ["<b>2,450</b>", "<b>4,900</b>", "<b>9,700</b>"], "tot")],
      widths=["46%", "18%", "18%", "18%"],
      note="Closing stock = 90% of opening: A = 90% &times; 500 = 450 &middot; B = 90% &times; 1,000 "
           "= 900 &middot; C = 90% &times; 3,000 = 2,700. Because stock is being reduced, production "
           "is <b>below</b> sales for every product.")

    parts = table("(c) PARTS USAGE BUDGET, in numbers of parts",
      [("Product", ""), ("Units produced", "r"),
       ("D &mdash; nos.", "r"), ("D &mdash; total", "r"),
       ("E &mdash; nos.", "r"), ("E &mdash; total", "r"),
       ("F &mdash; nos.", "r"), ("F &mdash; total", "r"),
       ("G &mdash; nos.", "r"), ("G &mdash; total", "r")],
      [["<b>A</b>", "2,450", "1", "2,450", "10", "24,500", "2", "4,900", "8", "19,600"],
       ["<b>B</b>", "4,900", "1", "4,900", "2", "9,800", "14", "68,600", "10", "49,000"],
       ["<b>C</b>", "9,700", "1", "9,700", "6", "58,200", "10", "97,000", "2", "19,400"],
       {"cls": "tot", "cells": ["<b>TOTAL PARTS REQUIRED</b>", "<b>17,050</b>", "",
                                "<b>17,050</b>", "", "<b>92,500</b>", "", "<b>1,70,500</b>", "",
                                "<b>88,000</b>"]}],
      headcls="lite",
      widths=["16%", "11%", "7%", "11%", "7%", "11%", "7%", "11%", "7%", "12%"])

    purch = table("(d) PURCHASE BUDGET in quantity and value",
      [("Particulars", ""), ("Part D", "r"), ("Part E", "r"), ("Part F", "r"), ("Part G", "r")],
      [["Parts consumed " + src("from the parts usage budget"),
        "17,050", "92,500", "1,70,500", "88,000"],
       ["<i>Add:</i> Closing stock " + src("90% of opening stock"),
        "1,350", "900", "18,000", "9,000"],
       {"cls": "sub", "cells": ["<b>Total requirement</b>", "<b>18,400</b>", "<b>93,400</b>",
                                "<b>1,88,500</b>", "<b>97,000</b>"]},
       ["<i>Less:</i> Opening stock " + src("given: 1,500 / 1,000 / 20,000 / 10,000"),
        "(1,500)", "(1,000)", "(20,000)", "(10,000)"],
       {"cls": "tot", "cells": ["<b>PARTS TO BE PURCHASED (nos.)</b>", "<b>16,900</b>",
                                "<b>92,400</b>", "<b>1,68,500</b>", "<b>87,000</b>"]},
       ["Purchase price per part " + R, "45", "15", "15", "5"],
       {"cls": "tot", "cells": ["<b>PURCHASE VALUE</b> " + R, "<b>7,60,500</b>", "<b>13,86,000</b>",
                                "<b>25,27,500</b>", "<b>4,35,000</b>"]},
       {"cls": "sub", "cells": ["<b>Total purchase value &mdash; all four parts</b>", "", "", "",
                                "<b>" + R + "51,09,000</b>"]}],
      widths=["36%", "16%", "16%", "16%", "16%"])

    manpower = table("(e) MAN POWER BUDGET &mdash; labour hours and wages payable",
      [("Product", ""), ("Units produced", "r"),
       ("Skilled &mdash; hrs p.u.", "r"), ("Skilled &mdash; total hrs", "r"),
       ("Unskilled &mdash; hrs p.u.", "r"), ("Unskilled &mdash; total hrs", "r")],
      [["<b>A</b>", "2,450", "6", "14,700", "8", "19,600"],
       ["<b>B</b>", "4,900", "4", "19,600", "6", "29,400"],
       ["<b>C</b>", "9,700", "3", "29,100", "6", "58,200"],
       {"cls": "tot", "cells": ["<b>TOTAL LABOUR HOURS</b>", "", "", "<b>63,400</b>", "",
                                "<b>1,07,200</b>"]},
       ["Wage rate per hour " + R, "", "", "6", "", "5"],
       {"cls": "tot", "cells": ["<b>WAGES PAYABLE</b> " + R, "", "", "<b>3,80,400</b>", "",
                                "<b>5,36,000</b>"]},
       ["Hours available per worker per month " + src("8 hours &times; 25 days"),
        "", "", "200", "", "200"],
       {"cls": "sub", "cells": ["<b>Number of workers required</b>", "", "", "<b>317</b>", "",
                                "<b>536</b>"]}],
      headcls="lite", widths=["20%", "14%", "13%", "17%", "16%", "20%"])
    manpower += ("<div class='small'>Total wages payable = " + R + "3,80,400 + " + R
                 + "5,36,000 = <b>" + R + "9,16,400</b>. &nbsp;Total workers required = 317 skilled "
                 "+ 536 unskilled = <b>853</b>. &nbsp;Skilled workers: 63,400 &divide; 200 = 317; "
                 "unskilled: 1,07,200 &divide; 200 = 536.</div>")

    master = stmt("(f) MASTER BUDGET for the month", ["A " + R, "B " + R, "C " + R, "Total " + R],
      [("<b>Sales</b> " + src("(a) &mdash; quantity &times; selling price"),
        ["11,25,000", "27,50,000", "65,00,000", "<b>1,03,75,000</b>"], "sub"),
       ("<i>Less:</i> Variable cost of sales " + src("sales quantity &times; W3 variable cost"),
        ["(8,75,000)", "(20,00,000)", "(35,00,000)", "<b>(63,75,000)</b>"]),
       ("<b>CONTRIBUTION</b> " + src("2,500&times;100, 5,000&times;150, 10,000&times;300"),
        ["<b>2,50,000</b>", "<b>7,50,000</b>", "<b>30,00,000</b>", "<b>40,00,000</b>"], "sub"),
       ("<i>Less:</i> Fixed overheads " + src("given, per month"),
        ["(15,75,000)", "(5,80,000)", "(8,45,000)", "<b>(30,00,000)</b>"]),
       ("<b>BUDGETED PROFIT FOR THE MONTH</b>",
        ["<b>(13,25,000)</b>", "<b>1,70,000</b>", "<b>21,55,000</b>", "<b>10,00,000</b>"], "tot"),
       ("<b>Budgeted profit for the year</b> " + src("10,00,000 &times; 12"),
        ["", "", "", "<b>1,20,00,000</b>"], "sub")],
      widths=["32%", "17%", "17%", "17%", "17%"],
      note="The annual profit of " + R + "1,20,00,000 is reproduced exactly, which confirms that the "
           "sales quantity of 2,500 : 5,000 : 10,000 derived in W4 is correct. <b>That is the "
           "check to state.</b>")

    return ("<div class='prob long'>"
            + prob_head("Q15", "The complete set of functional budgets, worked back from a profit target",
                        "Master budget &middot; p.55")
            + question(q) + read(rd)
            + wn(rmc + lab) + vc + wn(solve)
            + sales + prod + parts + purch + manpower + master
            + why(f"""<p>Everything in this problem hangs on W4, and it is worth seeing why the
question had to be built that way. A budget normally starts with a sales forecast; here the company has
instead fixed a <b>profit target</b> and asked what sales are needed to reach it. So the usual chain is
run in reverse for one step, and then forwards for five.</p>
{fml("Required contribution &nbsp;=&nbsp; Fixed cost &nbsp;+&nbsp; Target profit",
     "This is the Module 2 formula reappearing in a Module 5 setting. Contribution must cover the "
     "fixed cost before it can produce any profit, so the contribution needed is simply the two "
     "added together &mdash; here " + R + "30,00,000 + " + R + "10,00,000 = " + R + "40,00,000.")}
<p><b>The master budget by product is the finding management most needs to see</b>, and it is
uncomfortable:</p>
{table(None, [("", ""), ("A", "r"), ("B", "r"), ("C", "r")],
 [["Contribution " + R, "2,50,000", "7,50,000", "30,00,000"],
  ["Fixed overhead charged " + R, "(15,75,000)", "(5,80,000)", "(8,45,000)"],
  {"cls": "tot", "cells": ["<b>Profit / (Loss)</b> " + R, "<b>(13,25,000)</b>", "<b>1,70,000</b>",
                           "<b>21,55,000</b>"]},
  ["Contribution per unit " + R, "100", "150", "<b>300</b>"],
  ["Share of total contribution", "6.25%", "18.75%", "<b>75.00%</b>"]], headcls="lite",
 widths=["34%", "22%", "22%", "22%"])}
<p>Product A shows a loss of {R}13,25,000, and it is carrying more than half of the total fixed
overhead while generating only 6.25% of the contribution. Two things must be said about this, and saying
both is what separates a full-mark answer:</p>
{steps([
 '<b>Do not conclude that A should be dropped.</b> A still earns a positive contribution of ' +
 R + '2,50,000 a month. The ' + R + '15,75,000 of fixed overhead is an <i>apportionment</i>, and '
 'most of it would simply be re-charged to B and C if A were discontinued &mdash; wiping out '
 'B&rsquo;s profit entirely. This is the Module 4 lesson applied to a Module 5 statement.',
 '<b>But do ask why A absorbs so much fixed overhead</b> for so little return. Either the '
 'apportionment basis is wrong, or A genuinely consumes a great deal of capacity &mdash; it uses 14 '
 'labour hours per unit against C&rsquo;s 9, and ' + R + '265 of parts to earn ' + R + '100 of '
 'contribution. If the ratio 1 : 2 : 4 could be shifted further towards C, profit would rise sharply '
 'without any change in cost structure.'])}
<p class="small"><b>Finally, note the manpower figure.</b> 853 workers are needed for a single month
&mdash; 317 skilled and 536 unskilled. A budget of this kind is what allows a personnel department to
recruit and train in time, and it is the reason the man power budget is prepared in <i>hours</i> first
and converted to <i>people</i> second: hours come from production, but people come from hours divided
by the 200 hours each worker can offer.</p>""")
            + ans([("Contribution per unit &mdash; A / B / C",
                    f"{R} 100 / {R} 150 / {R} 300"),
                   ("<b>Sales quantity (W4)</b> &mdash; A / B / C",
                    "<b>2,500 / 5,000 / 10,000 units</b>"),
                   ("<b>(a) Sales budget</b>", f"<b>17,500 units = {R} 1,03,75,000</b>"),
                   ("<b>(b) Production budget</b> &mdash; A / B / C",
                    "<b>2,450 / 4,900 / 9,700 units</b>"),
                   ("<b>(c) Parts usage</b> &mdash; D / E / F / G",
                    "<b>17,050 / 92,500 / 1,70,500 / 88,000</b>"),
                   ("<b>(d) Purchases (nos.)</b> &mdash; D / E / F / G",
                    "<b>16,900 / 92,400 / 1,68,500 / 87,000</b>"),
                   ("<b>(d) Purchase value</b>", f"<b>{R} 51,09,000</b>"),
                   ("<b>(e) Labour hours</b> &mdash; skilled / unskilled",
                    "<b>63,400 / 1,07,200 hours</b>"),
                   ("<b>(e) Wages payable</b>",
                    f"<b>{R} 9,16,400 &nbsp;(317 + 536 = 853 workers)</b>"),
                   ("<b>(f) Contribution / Fixed / Profit</b>",
                    f"<b>{R} 40,00,000 &minus; {R} 30,00,000 = {R} 10,00,000</b>"),
                   ("<b>(f) Profit for the year</b>", f"<b>{R} 1,20,00,000</b> &nbsp;&#10003;")])
            + "</div>")


# ======================================================================
def build():
    return (opener()
            + q1() + q2() + q3() + q4() + q13()
            + cash_playbook() + q5() + q6() + q7()
            + prod_playbook() + q8() + q10() + q11() + q12()
            + q9() + q14() + q15())
