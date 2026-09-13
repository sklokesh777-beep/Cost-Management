# -*- coding: utf-8 -*-
"""MODULE 2 - MARGINAL COSTING AND ABSORPTION COSTING  (20 problems)"""
from build import (esc, rs, money, frac, prob_head, question, read, method, wn,
                   trap, why, steps, bullets, fml, calc, ans, table, src,
                   arrow_panel, module_opener)

R = "&#8377;"
D = "$"


# ----------------------------------------------------------------------
# helper: marginal / absorption columnar statement
# ----------------------------------------------------------------------
def stmt(caption, cols, rows, cur=R, note=None):
    """rows: (label, [values], cls)   values already formatted strings"""
    head = [("Particulars", "")] + [(c, "r") for c in cols]
    body = []
    for r in rows:
        cls = r[2] if len(r) > 2 else ""
        body.append({"cls": cls, "cells": [r[0]] + [(v, "r") for v in r[1]]})
    t = table(caption, head, body)
    if note:
        t += f"<div class='small'>{note}</div>"
    return t


# ======================================================================
# MODULE OPENER
# ======================================================================
def opener():
    intro = f"""
<h2 class="sec">The one difference that creates this whole module</h2>
<p>There is exactly <b>one</b> disagreement between marginal costing and absorption costing, and
every problem in this module is a consequence of it:</p>

{arrow_panel(500, 128, [
  {"box": (8, 8, 232, 44, "MARGINAL COSTING|Fixed cost is a PERIOD cost.|Charge the whole of it "
           "against this period.", "#eaf5f4"), "fs": 7.8},
  {"box": (260, 8, 232, 44, "ABSORPTION COSTING|Fixed cost is a PRODUCT cost.|Load it into each "
           "unit made.", "#fdf6e6"), "fs": 7.8},
  {"box": (8, 66, 484, 24, "CONSEQUENCE: stock is valued at VARIABLE cost only  vs  "
           "stock is valued at VARIABLE + FIXED cost", "#e8eef4"), "fs": 8.0},
  {"box": (8, 98, 484, 24, "So the two methods give DIFFERENT profit whenever stock levels CHANGE "
           "and identical profit when they do not.", "#fdeeec"), "fs": 8.0,
   "stroke": "#c0392b", "fg": "#98271b"},
  {"line": (124, 52, 124, 64)}, {"line": (376, 52, 376, 64)},
], "Fix this picture in your head. It answers every 'why is the profit different?' question.")}

{table(None, [("If &hellip;",""),("Then &hellip;","")],
 [["<b>Production = Sales</b> (no change in stock)","Both methods give the <b>same</b> profit."],
  ["<b>Production &gt; Sales</b> (stock going up)",
   "<b>Absorption profit is HIGHER</b>, because some of this period&rsquo;s fixed cost has been "
   "parked inside the closing stock instead of being charged."],
  ["<b>Production &lt; Sales</b> (stock coming down)",
   "<b>Absorption profit is LOWER</b>, because last period&rsquo;s fixed cost comes out of opening "
   "stock and gets charged now, on top of this period&rsquo;s."]],
 headcls="lite", widths=["32%","68%"])}

{fml("Absorption profit &minus; Marginal profit &nbsp;=&nbsp; Fixed overhead in closing stock "
     "&minus; Fixed overhead in opening stock",
     "This is the reconciliation. Every marginal-versus-absorption problem in this module can be "
     "checked with this one line. If your two profits differ by anything else, you have made an error.")}

<h2 class="sec" style="margin-top:6mm">The two families of problem in Module 2</h2>
{table(None, [("Family",""),("What you are asked to do",""),("Problems","c")],
 [["<b>A. Profit statements</b>",
   "Prepare a profit statement under marginal costing, under absorption costing, or both, and "
   "reconcile them. Watch stock movements and the under / over absorption of fixed overhead.",
   "<b>1, 15&ndash;20</b>"],
  ["<b>B. Cost-Volume-Profit</b>",
   "Contribution, P/V ratio, break-even point, margin of safety, required sales for a target "
   "profit. Pure formula work &mdash; the same six formulas every time.",
   "<b>2&ndash;14</b>"]],
 headcls="lite", widths=["18%","66%","16%"])}
"""
    return module_opener("Module Two", "Marginal Costing and<br/>Absorption Costing",
                         "20 problems &nbsp;&middot;&nbsp; workbook pages 21 to 27", intro)


# ======================================================================
# PLAYBOOK A - profit statements
# ======================================================================
def playbook_a():
    return f"""
<div class="modopen" style="page-break-before:always">
<div class="modopen-band" style="padding:22mm 18mm 12mm 18mm">
<div class="modopen-kicker">Module Two &middot; Playbook A</div>
<div class="modopen-title" style="font-size:21pt">Profit statements</div>
<span class="modopen-count">Use these steps for Q1, 15, 16, 17, 18, 19 and 20</span>
</div>
<div class="modopen-body">

<h3 class="sub">The two statement formats &mdash; learn the skeletons, fill in the numbers</h3>
{table(None, [("MARGINAL COSTING statement",""),("ABSORPTION COSTING statement","")],
 [["Sales", "Sales"],
  ["<i>Less:</i> Opening stock &nbsp;<span class='src' style='display:inline'>at VARIABLE cost "
   "per unit</span>", "<i>Less:</i> Opening stock &nbsp;<span class='src' style='display:inline'>"
   "at FULL cost per unit</span>"],
  ["<i>Add:</i> Variable cost of production", "<i>Add:</i> Full cost of production "
   "&nbsp;<span class='src' style='display:inline'>variable + fixed absorbed</span>"],
  ["<i>Less:</i> Closing stock &nbsp;<span class='src' style='display:inline'>at VARIABLE cost"
   "</span>", "<i>Less:</i> Closing stock &nbsp;<span class='src' style='display:inline'>at FULL "
   "cost</span>"],
  ["<b>= Variable cost of sales</b>", "<b>= Cost of sales</b>"],
  ["<b>CONTRIBUTION</b> = Sales &minus; variable cost of sales",
   "<b>GROSS PROFIT</b> = Sales &minus; cost of sales"],
  ["<i>Less:</i> <b>ALL</b> fixed costs &nbsp;<span class='src' style='display:inline'>the actual "
   "amount for the period</span>",
   "<i>Less / Add:</i> <b>Under / over absorption</b> of fixed production overhead"],
  ["", "<i>Less:</i> Fixed selling, admin and distribution costs"],
  ["<b>= PROFIT</b>", "<b>= PROFIT</b>"]],
 headcls="lite", widths=["50%","50%"])}

<div class="blk method"><span class="lab">The seven steps, every time</span>
{steps([
 "<b>Work out the stock movement in units first.</b> Opening + Production &minus; Sales = Closing. "
 "Write this line down before anything else &mdash; it tells you immediately which method will show "
 "the higher profit.",
 "<b>Variable cost per unit</b> = direct material + direct labour + variable overheads. "
 "(Variable <i>selling</i> overhead is a cost of <i>selling</i>, so it never goes into stock value.)",
 "<b>Fixed overhead absorption rate</b> = " + frac("Budgeted fixed production overhead",
                                                   "Budgeted / normal output in units") +
 ". Use <b>normal or budgeted</b> output, never actual.",
 "<b>Full cost per unit</b> = variable production cost + that absorption rate.",
 "Build the marginal statement. Charge the <b>whole actual fixed cost</b> for the period.",
 "Build the absorption statement. Then compute <b>absorbed = actual production &times; rate</b> "
 "and compare with the <b>actual fixed overhead</b>. Absorbed more than actual = <b>over</b>"
 "-absorption (add it back); absorbed less = <b>under</b>-absorption (deduct it).",
 "<b>Reconcile.</b> The difference between the two profits must equal the fixed overhead inside the "
 "change in stock. If it does not, find your error before writing the answer."])}
</div>

<div class="blk trap"><span class="lab">The three errors that cost the most marks</span>
{bullets([
 '<b>Valuing stock at full cost in the marginal statement.</b> Under marginal costing stock carries '
 'variable cost only. This is the definition of the method.',
 '<b>Dividing fixed overhead by actual output to get the absorption rate.</b> The rate is fixed in '
 'advance from <i>budgeted</i> or <i>normal</i> output. That is precisely why under and over '
 'absorption exist &mdash; if you used actual output there would never be any.',
 '<b>Including variable selling overhead in the stock value.</b> Unsold goods have not been sold, '
 'so no selling cost has been incurred on them. It is deducted after contribution, not before.'])}
</div>
</div></div>"""


# ======================================================================
# PLAYBOOK B - CVP
# ======================================================================
def playbook_b():
    return f"""
<div class="modopen" style="page-break-before:always">
<div class="modopen-band" style="padding:22mm 18mm 12mm 18mm">
<div class="modopen-kicker">Module Two &middot; Playbook B</div>
<div class="modopen-title" style="font-size:21pt">Cost&ndash;Volume&ndash;Profit</div>
<span class="modopen-count">Use these formulas for Q2 to Q14</span>
</div>
<div class="modopen-body">

<div class="blk read"><span class="lab">Everything starts from one equation</span>
{fml("Sales &minus; Variable cost &nbsp;=&nbsp; <b>CONTRIBUTION</b> &nbsp;=&nbsp; "
     "Fixed cost + Profit",
     "Read it both ways. Left to right it tells you what contribution IS. Right to left it tells "
     "you what contribution DOES: it first pays off the fixed cost, and whatever is left over is "
     "profit. Break-even is simply the point where contribution has exactly paid the fixed cost "
     "and nothing remains.")}
<p>Every one of the thirteen problems in this family is that equation rearranged. There is nothing
else to learn.</p>
</div>

<h3 class="sub">The six formulas &mdash; and what each one is really asking</h3>
{table(None, [("You want &hellip;",""),("Formula",""),("In plain words","")],
 [["Contribution", "Sales &minus; Variable cost &nbsp;<i>or</i>&nbsp; Fixed cost + Profit",
   "What is left from the selling price after paying the costs that grow with volume."],
  ["P/V ratio", frac("Contribution", "Sales") + " &times; 100",
   "How many paise out of every rupee of sales survives to help pay the fixed cost. "
   "It does <b>not</b> change when volume changes &mdash; only when price or variable cost changes."],
  ["<b>BEP</b> in units", frac("Fixed cost", "Contribution per unit"),
   "How many units must be sold before the fixed cost is fully paid."],
  ["<b>BEP</b> in rupees", frac("Fixed cost", "P/V ratio"),
   "The same point expressed as a sales value. Use this when the question gives you totals and no "
   "unit figures."],
  ["Margin of safety", "Actual sales &minus; BEP sales &nbsp;<i>or</i>&nbsp; " +
   frac("Profit", "P/V ratio"),
   "How far sales can fall before you start making a loss. The cushion."],
  ["Sales for a target profit", frac("Fixed cost + Target profit", "P/V ratio"),
   "Treat the target profit exactly like an extra slice of fixed cost that also has to be paid for."]],
 headcls="lite", widths=["17%","28%","55%"])}

<div class="blk method"><span class="lab">When the question gives you two periods and no costs</span>
<p>Q7 and Q8 give only sales and profit for two periods. You cannot see the fixed cost or the
variable cost at all. There is a standard route out, and it works because <b>fixed cost does not
change between the two periods</b>, so every extra rupee of contribution shows up as an extra
rupee of profit.</p>
{fml("P/V ratio &nbsp;=&nbsp; " + frac("Change in profit", "Change in sales") + " &times; 100")}
{steps([
 "Find the P/V ratio from the change in profit over the change in sales.",
 "Take any one period. Contribution = Sales &times; P/V ratio.",
 "<b>Fixed cost = Contribution &minus; Profit</b> for that same period.",
 "Now you have everything &mdash; compute BEP and margin of safety normally.",
 "<b>Check</b> your fixed cost against the <i>other</i> period. If it does not give that "
 "period&rsquo;s profit too, you have gone wrong."])}
</div>

<div class="blk trap"><span class="lab">Rounding the P/V ratio &mdash; a real warning</span>
<p>When the P/V ratio is a recurring decimal such as 44.44% or 54.55%, <b>do not round it to 44% or
54% before dividing</b>. In Q11 parts (v) and (vi) that rounding shifts the break-even figure by
several hundred rupees. Keep the ratio as a fraction &mdash; 8,000/18,000 rather than 0.44 &mdash;
and divide once at the end.</p>
</div>
</div></div>"""


# ======================================================================
# Q1
# ======================================================================
def q1():
    q = f"""<p>The basic production data of ABC Ltd are as follows: Normal volume of production =
19,500 units per period. Sale price {D}4 per unit. Variable cost {D}2 per unit. Fixed cost
{D}1 per unit. Total fixed cost = {D}19,500 ({D}1 &times; 19,500 units, normal). Selling and
distribution costs have been omitted. The opening and closing stocks consist of both finished goods
and equivalent units of work-in-progress.</p>
<p>Present the profit and loss statement under Absorption and Marginal costing method.</p>"""

    rd = f"""{bullets([
 '<b>Read the question again and notice what is missing.</b> You are given the normal volume, the '
 'three unit costs and the price &mdash; but <b>no actual production figure and no actual sales '
 'figure</b> for any period. Without those, no stock movement can be computed.',
 'So the only statement that can be prepared from the data as printed is the one at '
 '<b>normal volume</b>, where production = sales = 19,500 units and there is no change in stock.',
 'That turns out to be a useful answer rather than a wasted one, because it demonstrates the '
 'headline rule of the module: <b>when stock does not change, the two methods give exactly the '
 'same profit.</b>',
 'The sentence about opening and closing stocks is telling you what <i>would</i> happen if figures '
 'were supplied. The illustration at the end shows it.'])}"""

    m = stmt("(a) Marginal Costing Profit Statement &mdash; at normal volume of 19,500 units",
      ["Per unit " + D, "Total " + D],
      [("Sales", ["4.00", "78,000"]),
       ("<i>Less:</i> Variable cost", ["(2.00)", "(39,000)"]),
       ("<b>Contribution</b>", ["<b>2.00</b>", "<b>39,000</b>"], "sub"),
       ("<i>Less:</i> Fixed cost &nbsp;<span class='src' style='display:inline'>charged in full as "
        "a period cost</span>", ["", "(19,500)"]),
       ("<b>Profit</b>", ["", "<b>19,500</b>"], "tot")], cur=D)

    a = stmt("(b) Absorption Costing Profit Statement &mdash; at normal volume of 19,500 units",
      ["Per unit " + D, "Total " + D],
      [("Sales", ["4.00", "78,000"]),
       ("<i>Less:</i> Cost of sales", ["", ""], "sub"),
       ("&nbsp;&nbsp;&nbsp;Variable production cost", ["2.00", "39,000"]),
       ("&nbsp;&nbsp;&nbsp;Fixed production overhead absorbed "
        "&nbsp;<span class='src' style='display:inline'>19,500 &times; " + D + "1</span>",
        ["1.00", "19,500"]),
       ("&nbsp;&nbsp;&nbsp;<b>Total cost of sales</b>", ["<b>3.00</b>", "<b>(58,500)</b>"], "sub"),
       ("<b>Profit</b>", ["<b>1.00</b>", "<b>19,500</b>"], "tot")], cur=D,
      note="Absorbed overhead = 19,500 units &times; " + D + "1 = " + D + "19,500 = the actual "
           "fixed cost, so there is <b>no under or over absorption</b> at normal volume.")

    illus = table("What would happen if production and sales differed &mdash; an illustration",
      [("", ""), ("Production = Sales<br/>19,500 / 19,500", "r"),
       ("Production &gt; Sales<br/>19,500 / 17,500", "r"),
       ("Production &lt; Sales<br/>17,500 / 19,500", "r")],
      [["Closing stock (units)", "Nil", "2,000", "Nil (2,000 opening used up)"],
       ["Marginal costing profit", "19,500", f"{D}15,500", f"{D}19,500"],
       ["Absorption costing profit", "19,500", f"{D}17,500", f"{D}17,500"],
       {"cls": "tot", "cells": ["<b>Difference</b>", "<b>Nil</b>", "<b>+2,000</b>",
                                 "<b>&minus;2,000</b>"]},
       {"cls": "sub", "cells": ["Explanation", "no stock change",
                                 "2,000 units &times; " + D + "1 fixed cost parked in stock",
                                 "2,000 units &times; " + D + "1 released from stock"]}],
      headcls="lite")

    return ("<div class='prob long'>"
            + prob_head("Q1", "Both statements at normal volume", "Statements &middot; p.21")
            + question(q) + read(rd) + m + a
            + why(f"""<p>Both methods give {D}19,500. That is not a coincidence and it is the point
of the problem: at normal volume the fixed overhead absorbed into production exactly equals the
fixed overhead incurred, so nothing is left sitting in stock and the two profits must agree.</p>
<p>The illustration below shows the two cases where they diverge. Learn the direction: <b>stock up
&rarr; absorption profit higher</b>; <b>stock down &rarr; absorption profit lower</b>.</p>""")
            + illus
            + trap(f"""<p><b>Note on the data.</b> The question gives no actual production or sales
figures, so a full multi-period comparison cannot be prepared from it. If your professor expects a
version with stock movements, he will supply the production and sales for each period &mdash; the
method is exactly the one shown in Q16 and Q20. Say in one line that you have prepared the statement
at normal volume, and you protect the marks.</p>""")
            + ans([("Contribution per unit", f"{D} 2.00"),
                   ("Marginal costing profit", f"{D} 19,500"),
                   ("Absorption costing profit", f"{D} 19,500"),
                   ("Difference", "Nil &mdash; production equals sales, so no fixed cost is held in stock")])
            + "</div>")


# ======================================================================
# Q2
# ======================================================================
def q2():
    q = f"""<p>From the following information, find out the amount of profit earned during the year
using marginal cost technique: Fixed Cost <span class="rs">{R}</span>5,00,000; Variable Cost
<span class="rs">{R}</span>10 per unit; Selling Price <span class="rs">{R}</span>15 per unit;
Output level 1,50,000 units.</p>"""

    s = stmt("Marginal Cost Statement",
      ["Per unit " + R, "Total " + R],
      [("Sales &nbsp;<span class='src' style='display:inline'>1,50,000 &times; " + R + "15</span>",
        ["15", "22,50,000"]),
       ("<i>Less:</i> Variable cost &nbsp;<span class='src' style='display:inline'>1,50,000 &times; "
        + R + "10</span>", ["(10)", "(15,00,000)"]),
       ("<b>Contribution</b>", ["<b>5</b>", "<b>7,50,000</b>"], "sub"),
       ("<i>Less:</i> Fixed cost", ["", "(5,00,000)"]),
       ("<b>Profit</b>", ["", "<b>2,50,000</b>"], "tot")])

    return ("<div class='prob'>"
            + prob_head("Q2", "Straight marginal cost statement", "CVP &middot; p.21&ndash;22")
            + question(q)
            + read(bullets([
                'Everything is per unit except the fixed cost, so multiply the two unit figures by '
                'the output of 1,50,000 and put the fixed cost in as a single lump.',
                '&ldquo;Using marginal cost technique&rdquo; means <b>present it as a statement '
                'ending in contribution then profit</b> &mdash; not just the final number. The '
                'layout carries marks.',
                'Always show the <b>per-unit column beside the total column</b>. It is free marks '
                'and it makes checking trivial.']))
            + s
            + ans([("Contribution per unit", f"{R} 5"),
                   ("Total contribution", f"{R} 7,50,000"),
                   ("<b>Profit</b>", f"<b>{R} 2,50,000</b>")],
                  "Cross-check with the marginal cost equation: Contribution = Fixed cost + Profit "
                  "&rarr; 7,50,000 = 5,00,000 + 2,50,000 &#10003;")
            + "</div>")


# ======================================================================
# Q3
# ======================================================================
def q3():
    q = f"""<p>Find the profit from the following data: Sales <span class="rs">{R}</span>80,000;
Marginal Cost <span class="rs">{R}</span>60,000; Break-even point
<span class="rs">{R}</span>60,000.</p>"""

    rd = f"""{bullets([
 '&ldquo;Marginal cost&rdquo; is just another name for <b>variable cost</b>. So contribution = '
 '80,000 &minus; 60,000 = ' + R + '20,000.',
 'The fixed cost is <b>not given</b> &mdash; you have to extract it from the break-even point. '
 'That is the whole trick of this problem.',
 'Work the BEP formula <b>backwards</b>: if BEP = Fixed cost &divide; P/V ratio, then '
 'Fixed cost = BEP &times; P/V ratio.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Contribution and P/V ratio</h4>
{calc([f'Contribution &nbsp;=&nbsp; Sales &minus; Marginal cost &nbsp;=&nbsp; 80,000 &minus; '
       f'60,000 &nbsp;=&nbsp; <b>{R}20,000</b>',
       'P/V ratio &nbsp;=&nbsp; 20,000 &divide; 80,000 &nbsp;=&nbsp; <b>25%</b>'])}

<h4 class="mini">W2 &nbsp;Recovering the fixed cost from the break-even point</h4>
{fml("BEP (in " + R + ") &nbsp;=&nbsp; " + frac("Fixed cost", "P/V ratio")
     + " &nbsp;&nbsp;&rarr;&nbsp;&nbsp; Fixed cost &nbsp;=&nbsp; BEP &times; P/V ratio")}
{calc([f'Fixed cost &nbsp;=&nbsp; 60,000 &times; 25% &nbsp;=&nbsp; <b>{R}15,000</b>'])}"""

    s = stmt("Marginal Cost Statement",
      ["Amount " + R],
      [("Sales", ["80,000"]),
       ("<i>Less:</i> Marginal (variable) cost", ["(60,000)"]),
       ("<b>Contribution</b>", ["<b>20,000</b>"], "sub"),
       ("<i>Less:</i> Fixed cost &nbsp;<span class='src' style='display:inline'>W2</span>",
        ["(15,000)"]),
       ("<b>Profit</b>", ["<b>5,000</b>"], "tot")])

    return ("<div class='prob'>"
            + prob_head("Q3", "Fixed cost hidden inside the BEP", "CVP &middot; p.22")
            + question(q) + read(rd) + wn(wnh) + s
            + ans([("Contribution", f"{R} 20,000"), ("P/V ratio", "25%"),
                   ("Fixed cost (derived)", f"{R} 15,000"),
                   ("<b>Profit</b>", f"<b>{R} 5,000</b>")],
                  "Check: margin of safety = 80,000 &minus; 60,000 = 20,000; "
                  "profit = MOS &times; P/V ratio = 20,000 &times; 25% = 5,000 &#10003; "
                  "&mdash; a second route to the same answer, worth showing.")
            + "</div>")


# ======================================================================
# Q4
# ======================================================================
def q4():
    q = f"""<p>From the following particulars, calculate the break-even point: Variable cost per
unit <span class="rs">{R}</span>12; Fixed Expenses <span class="rs">{R}</span>60,000; Selling Price
per unit <span class="rs">{R}</span>18.</p>"""

    return ("<div class='prob'>"
            + prob_head("Q4", "Break-even point in units and in rupees", "CVP &middot; p.22")
            + question(q)
            + read(bullets([
                'Unit figures are given, so use the <b>units</b> form of the BEP formula: '
                'Fixed cost &divide; contribution per unit.',
                'Give <b>both</b> answers &mdash; units and sales value. The question says '
                '&ldquo;break-even point&rdquo;, and a complete answer states it both ways.']))
            + wn(f"""{calc([f'Contribution per unit &nbsp;=&nbsp; 18 &minus; 12 &nbsp;=&nbsp; <b>{R}6</b>'])}
{fml("BEP (units) &nbsp;=&nbsp; " + frac("Fixed cost", "Contribution per unit") + " &nbsp;=&nbsp; "
     + frac("60,000", "6") + " &nbsp;=&nbsp; <b>10,000 units</b>")}
{calc([f'BEP (sales value) &nbsp;=&nbsp; 10,000 units &times; {R}18 &nbsp;=&nbsp; '
       f'<b>{R}1,80,000</b>'])}
<p class="small">Alternative route to the same value: P/V ratio = 6 &divide; 18 = 33.33%, so
BEP = 60,000 &divide; 0.3333 = {R}1,80,000 &#10003;</p>""")
            + ans([("Contribution per unit", f"{R} 6"),
                   ("<b>BEP in units</b>", "<b>10,000 units</b>"),
                   ("<b>BEP in sales value</b>", f"<b>{R} 1,80,000</b>"),
                   ("P/V ratio", "33.33%")])
            + "</div>")


# ======================================================================
# Q5
# ======================================================================
def q5():
    q = f"""<p>From the following particulars, find out the selling price per unit if B.E.P. is to
be brought down to 9,000 units. Variable cost per unit <span class="rs">{R}</span>75; Fixed
Expenses <span class="rs">{R}</span>2,70,000; Selling Price per unit
<span class="rs">{R}</span>100.</p>"""

    rd = f"""{bullets([
 'This is the BEP formula run <b>backwards</b>. You are told the answer (9,000 units) and asked '
 'for the selling price that produces it.',
 'First find where you currently stand: at ' + R + '100 the contribution is ' + R + '25 and the '
 'BEP is 2,70,000 &divide; 25 = <b>10,800 units</b>. The company wants it down to 9,000, which '
 'means each unit must contribute <b>more</b>.',
 'Let the new selling price be <i>x</i>. Then contribution per unit = <i>x</i> &minus; 75, and '
 '9,000 = 2,70,000 &divide; (<i>x</i> &minus; 75). Solve for <i>x</i>.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;The present position</h4>
{calc([f'Present contribution &nbsp;=&nbsp; 100 &minus; 75 &nbsp;=&nbsp; {R}25 per unit',
       f'Present BEP &nbsp;=&nbsp; 2,70,000 &divide; 25 &nbsp;=&nbsp; <b>10,800 units</b>',
       'Target BEP &nbsp;=&nbsp; 9,000 units &nbsp;&rarr;&nbsp; the price must rise'])}

<h4 class="mini">W2 &nbsp;Solving for the new selling price</h4>
{calc(['Required contribution per unit &nbsp;=&nbsp; ' + frac("Fixed cost", "Target BEP units")
       + f' &nbsp;=&nbsp; ' + frac("2,70,000", "9,000") + f' &nbsp;=&nbsp; <b>{R}30</b>',
       'New selling price &nbsp;=&nbsp; Variable cost + Required contribution',
       f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp; 75 + 30 &nbsp;=&nbsp; <b>{R}105 per unit</b>'])}
<p class="small"><b>Proof:</b> at {R}105 the contribution is {R}30, so BEP = 2,70,000 &divide; 30 =
9,000 units &#10003; exactly as required.</p>"""

    return ("<div class='prob'>"
            + prob_head("Q5", "Working the BEP formula backwards", "CVP &middot; p.22")
            + question(q) + read(rd) + wn(wnh)
            + ans([("Present contribution / BEP", f"{R} 25 per unit / 10,800 units"),
                   ("Required contribution per unit", f"{R} 30"),
                   ("<b>New selling price</b>", f"<b>{R} 105 per unit</b>"),
                   ("Increase needed", f"{R} 5 per unit, i.e. 5%")])
            + "</div>")


# ======================================================================
# Q6
# ======================================================================
def q6():
    q = f"""<p>From the following data, calculate break-even point expressed in terms of units and
also the new B.E.P., if the selling price is reduced by 10%.</p>
{table(None, [("Particulars",""),("Amount","r")],
 [["<b>Fixed Expenses</b>",""],["&nbsp;&nbsp;&nbsp;Depreciation", R + " 1,00,000"],
  ["&nbsp;&nbsp;&nbsp;Salaries", R + " 1,00,000"],
  ["<b>Variable Expenses</b>",""],
  ["&nbsp;&nbsp;&nbsp;Materials", R + " 3 per unit"],
  ["&nbsp;&nbsp;&nbsp;Labour", R + " 2 per unit"],
  ["Selling Price", R + " 10 per unit"]], headcls="lite", widths=["62%","38%"])}"""

    rd = f"""{bullets([
 'Add the two fixed items into one figure and the two variable items into one per-unit figure. '
 'Do this before you touch the formula.',
 '<b>A 10% cut in selling price does not change the fixed cost or the variable cost.</b> Only the '
 'contribution shrinks &mdash; and because contribution is the denominator, the break-even point '
 'rises. Expect a bigger answer for the second part.',
 'Notice how sharp the effect is: a 10% price cut here raises the break-even by 25%. That is the '
 'lesson of the problem, and worth one closing sentence in your answer.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Present break-even point</h4>
{calc([f'Fixed expenses &nbsp;=&nbsp; 1,00,000 + 1,00,000 &nbsp;=&nbsp; <b>{R}2,00,000</b>',
       f'Variable cost per unit &nbsp;=&nbsp; 3 + 2 &nbsp;=&nbsp; <b>{R}5</b>',
       f'Contribution per unit &nbsp;=&nbsp; 10 &minus; 5 &nbsp;=&nbsp; <b>{R}5</b>'])}
{fml("BEP &nbsp;=&nbsp; " + frac("2,00,000", "5") + " &nbsp;=&nbsp; <b>40,000 units</b>")}

<h4 class="mini">W2 &nbsp;New break-even point after a 10% price cut</h4>
{calc([f'New selling price &nbsp;=&nbsp; 10 &minus; 10% &nbsp;=&nbsp; <b>{R}9</b>',
       f'Variable cost is unchanged at {R}5',
       f'New contribution per unit &nbsp;=&nbsp; 9 &minus; 5 &nbsp;=&nbsp; <b>{R}4</b>'])}
{fml("New BEP &nbsp;=&nbsp; " + frac("2,00,000", "4") + " &nbsp;=&nbsp; <b>50,000 units</b>")}"""

    comp = table("The effect of the price cut, side by side",
      [("", ""), ("Present", "r"), ("After 10% price cut", "r"), ("Change", "r")],
      [["Selling price per unit", "10", "9", "&minus;10%"],
       ["Variable cost per unit", "5", "5", "no change"],
       ["Contribution per unit", "5", "4", "&minus;20%"],
       ["P/V ratio", "50%", "44.44%", "&minus;5.56 points"],
       {"cls": "tot", "cells": ["<b>Break-even point (units)</b>", "<b>40,000</b>",
                                 "<b>50,000</b>", "<b>+25%</b>"]}], headcls="lite")

    return ("<div class='prob'>"
            + prob_head("Q6", "How a price cut moves the break-even point", "CVP &middot; p.22")
            + question(q) + read(rd) + wn(wnh) + comp
            + why("<p>A 10% cut in price caused a 20% fall in contribution and a 25% rise in the "
                  "break-even point. The reason is that the whole of the price cut comes out of "
                  "contribution &mdash; the variable cost does not fall to share the pain. This is "
                  "why price cuts are so much more dangerous than they look, and saying so in one "
                  "line turns a numerical answer into an interpreted one.</p>")
            + ans([("Contribution per unit &mdash; present / new", f"{R} 5 / {R} 4"),
                   ("<b>Present BEP</b>", "<b>40,000 units</b>"),
                   ("<b>New BEP after 10% price cut</b>", "<b>50,000 units</b>"),
                   ("BEP in value &mdash; present / new",
                    f"{R} 4,00,000 / {R} 4,50,000")])
            + "</div>")



# ======================================================================
# Q7
# ======================================================================
def q7():
    q = f"""<p>The sales turnover and profits during two periods are as under:</p>
{table(None, [("Period",""),("Sales","r"),("Profit","r")],
 [["Period I", R + " 20 lakhs", R + " 2 lakhs"],
  ["Period II", R + " 30 lakhs", R + " 4 lakhs"]], headcls="lite")}
<p>Calculate the P/V ratio, fixed cost, break-even point and margin of safety.</p>"""

    rd = f"""{bullets([
 'You are given <b>no costs at all</b> &mdash; only sales and profit. This is the two-period type '
 'from Playbook B.',
 'The key insight: <b>fixed cost is the same in both periods</b>. So the extra ' + R + '2 lakhs of '
 'profit in Period II came entirely from the extra ' + R + '10 lakhs of sales. Every rupee of that '
 'increase is pure contribution.',
 'Once you have the P/V ratio you can work out the contribution of either period, and fixed cost '
 'falls out as contribution minus profit.',
 '<b>Always verify with the other period.</b> If your fixed cost does not also reproduce Period '
 'I&rsquo;s profit, you have made an error.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;P/V ratio from the change</h4>
{fml("P/V ratio &nbsp;=&nbsp; " + frac("Change in profit", "Change in sales") + " &times; 100 "
     "&nbsp;=&nbsp; " + frac(R + "2,00,000", R + "10,00,000") + " &times; 100 &nbsp;=&nbsp; "
     "<b>20%</b>")}

<h4 class="mini">W2 &nbsp;Fixed cost</h4>
{calc(['Take Period I: Contribution &nbsp;=&nbsp; Sales &times; P/V ratio &nbsp;=&nbsp; '
       f'20,00,000 &times; 20% &nbsp;=&nbsp; {R}4,00,000',
       'Fixed cost &nbsp;=&nbsp; Contribution &minus; Profit &nbsp;=&nbsp; 4,00,000 &minus; '
       f'2,00,000 &nbsp;=&nbsp; <b>{R}2,00,000</b>'])}
<p class="small"><b>Verification on Period II:</b> contribution = 30,00,000 &times; 20% =
{R}6,00,000; profit = 6,00,000 &minus; 2,00,000 = {R}4,00,000 &#10003; matches the given figure.</p>

<h4 class="mini">W3 &nbsp;Break-even point and margin of safety</h4>
{fml("BEP &nbsp;=&nbsp; " + frac("Fixed cost", "P/V ratio") + " &nbsp;=&nbsp; "
     + frac("2,00,000", "0.20") + f" &nbsp;=&nbsp; <b>{R}10,00,000</b>")}
{calc([f'MOS Period I &nbsp;=&nbsp; 20,00,000 &minus; 10,00,000 &nbsp;=&nbsp; <b>{R}10,00,000</b> '
       '(50% of sales)',
       f'MOS Period II &nbsp;=&nbsp; 30,00,000 &minus; 10,00,000 &nbsp;=&nbsp; <b>{R}20,00,000</b> '
       '(66.67% of sales)'])}"""

    s = stmt("Marginal Cost Statement for both periods",
      ["Period I " + R, "Period II " + R],
      [("Sales", ["20,00,000", "30,00,000"]),
       ("<i>Less:</i> Variable cost &nbsp;<span class='src' style='display:inline'>80% of sales"
        "</span>", ["(16,00,000)", "(24,00,000)"]),
       ("<b>Contribution</b> &nbsp;<span class='src' style='display:inline'>20% of sales</span>",
        ["<b>4,00,000</b>", "<b>6,00,000</b>"], "sub"),
       ("<i>Less:</i> Fixed cost &nbsp;<span class='src' style='display:inline'>W2 &mdash; same in "
        "both periods</span>", ["(2,00,000)", "(2,00,000)"]),
       ("<b>Profit</b>", ["<b>2,00,000</b>", "<b>4,00,000</b>"], "tot")])

    return ("<div class='prob long'>"
            + prob_head("Q7", "Two periods, no costs given", "CVP &middot; p.22")
            + question(q) + read(rd) + wn(wnh) + s
            + ans([("<b>P/V ratio</b>", "<b>20%</b>"),
                   ("<b>Fixed cost</b>", f"<b>{R} 2,00,000</b>"),
                   ("<b>Break-even sales</b>", f"<b>{R} 10,00,000</b>"),
                   ("Margin of safety &mdash; Period I", f"{R} 10,00,000 (50%)"),
                   ("Margin of safety &mdash; Period II", f"{R} 20,00,000 (66.67%)")])
            + "</div>")


# ======================================================================
# Q8
# ======================================================================
def q8():
    q = f"""<p>The following data are obtained from the records of a company:</p>
{table(None, [("Particulars",""),("First Year " + R,"r"),("Second Year " + R,"r")],
 [["Sales","80,000","90,000"],["Profit","10,000","14,000"]], headcls="lite")}
<p>Calculate the break-even point.</p>"""

    wnh = f"""<h4 class="mini">W1 &nbsp;P/V ratio</h4>
{fml("P/V ratio &nbsp;=&nbsp; " + frac("Change in profit", "Change in sales") + " &times; 100 "
     "&nbsp;=&nbsp; " + frac("14,000 &minus; 10,000", "90,000 &minus; 80,000") + " &times; 100 "
     "&nbsp;=&nbsp; " + frac("4,000", "10,000") + " &times; 100 &nbsp;=&nbsp; <b>40%</b>")}

<h4 class="mini">W2 &nbsp;Fixed cost</h4>
{calc(['First year contribution &nbsp;=&nbsp; 80,000 &times; 40% &nbsp;=&nbsp; '
       f'<b>{R}32,000</b>',
       f'Fixed cost &nbsp;=&nbsp; 32,000 &minus; 10,000 &nbsp;=&nbsp; <b>{R}22,000</b>'])}
<p class="small"><b>Verification:</b> second year contribution = 90,000 &times; 40% = {R}36,000;
36,000 &minus; 22,000 = {R}14,000 &#10003; matches.</p>

<h4 class="mini">W3 &nbsp;Break-even point</h4>
{fml("BEP &nbsp;=&nbsp; " + frac("22,000", "0.40") + f" &nbsp;=&nbsp; <b>{R}55,000</b>")}"""

    s = stmt("Marginal Cost Statement for both years",
      ["First Year " + R, "Second Year " + R],
      [("Sales", ["80,000", "90,000"]),
       ("<i>Less:</i> Variable cost (60% of sales)", ["(48,000)", "(54,000)"]),
       ("<b>Contribution</b> (40% of sales)", ["<b>32,000</b>", "<b>36,000</b>"], "sub"),
       ("<i>Less:</i> Fixed cost", ["(22,000)", "(22,000)"]),
       ("<b>Profit</b>", ["<b>10,000</b>", "<b>14,000</b>"], "tot")])

    return ("<div class='prob'>"
            + prob_head("Q8", "Break-even from two years' results", "CVP &middot; p.22")
            + question(q)
            + read(bullets([
                'Exactly the same shape as Q7. Change in profit ' + R + '4,000 over change in '
                'sales ' + R + '10,000 gives the P/V ratio straight away.',
                'The question asks only for the break-even point, but <b>show the fixed cost and '
                'the P/V ratio on the way</b> &mdash; those are the working marks.']))
            + wn(wnh) + s
            + ans([("P/V ratio", "40%"), ("Fixed cost", f"{R} 22,000"),
                   ("<b>Break-even point</b>", f"<b>{R} 55,000</b>"),
                   ("Margin of safety &mdash; first year", f"{R} 25,000"),
                   ("Margin of safety &mdash; second year", f"{R} 35,000")])
            + "</div>")


# ======================================================================
# Q9
# ======================================================================
def q9():
    q = f"""<p>A company earned a profit of <span class="rs">{R}</span>30,000 during a particular
year. If the marginal cost and selling price of a product are <span class="rs">{R}</span>8 and
<span class="rs">{R}</span>10 per unit respectively, find out the amount of Margin of Safety.</p>"""

    rd = f"""{bullets([
 'You are not given sales or fixed cost, so you cannot find the BEP and subtract. You need the '
 '<b>other</b> margin-of-safety formula.',
 'Because profit is the part of contribution left over <i>after</i> the fixed cost is paid, the '
 'sales that generated that profit are pure margin of safety. So MOS = profit &divide; P/V ratio.',
 'In units it is even simpler: MOS units = profit &divide; contribution per unit.'])}"""

    wnh = f"""{calc([f'Contribution per unit &nbsp;=&nbsp; 10 &minus; 8 &nbsp;=&nbsp; <b>{R}2</b>',
       'P/V ratio &nbsp;=&nbsp; 2 &divide; 10 &nbsp;=&nbsp; <b>20%</b>'])}
{fml("MOS (in units) &nbsp;=&nbsp; " + frac("Profit", "Contribution per unit") + " &nbsp;=&nbsp; "
     + frac("30,000", "2") + " &nbsp;=&nbsp; <b>15,000 units</b>")}
{fml("MOS (in " + R + ") &nbsp;=&nbsp; 15,000 &times; " + R + "10 &nbsp;=&nbsp; "
     + f"<b>{R}1,50,000</b>",
     "Or directly: MOS = Profit &divide; P/V ratio = 30,000 &divide; 0.20 = " + R + "1,50,000. "
     "Both routes, same answer.")}"""

    return ("<div class='prob'>"
            + prob_head("Q9", "Margin of safety from profit alone", "CVP &middot; p.23")
            + question(q) + read(rd) + wn(wnh)
            + why("<p>Think about what margin of safety means physically. Break-even sales pay the "
                  "fixed cost exactly and leave nothing. Every rupee of sales <i>beyond</i> that "
                  "point contributes only profit. So if you know the profit and you know how much "
                  "profit each rupee of sales produces &mdash; the P/V ratio &mdash; you can work "
                  "backwards to how many rupees of sales sat above break-even. That is the margin "
                  "of safety, and it is why you never needed the fixed cost.</p>")
            + ans([("Contribution per unit", f"{R} 2"), ("P/V ratio", "20%"),
                   ("<b>Margin of safety in units</b>", "<b>15,000 units</b>"),
                   ("<b>Margin of safety in value</b>", f"<b>{R} 1,50,000</b>")])
            + "</div>")


# ======================================================================
# Q10
# ======================================================================
def q10():
    q = f"""<p>From the following details find out (a) Profit Volume Ratio (b) BEP (c) Margin of
Safety.</p>
{table(None, [("Particulars",""),("" + R,"r")],
 [["Sales","1,00,000"],["Total cost","80,000"],["Fixed Cost","20,000"],
  ["Net profit","20,000"]], headcls="lite", widths=["70%","30%"])}"""

    rd = f"""{bullets([
 'The <b>variable cost is not given directly</b> &mdash; you must strip it out: '
 'Variable cost = Total cost &minus; Fixed cost = 80,000 &minus; 20,000 = ' + R + '60,000.',
 'Once you have that, build the marginal cost statement and the three answers drop out of it.',
 'The net profit of ' + R + '20,000 is given, so use it to <b>check</b> your statement rather than '
 'to compute anything.'])}"""

    s = stmt("Marginal Cost Statement",
      ["Amount " + R],
      [("Sales", ["1,00,000"]),
       ("<i>Less:</i> Variable cost &nbsp;<span class='src' style='display:inline'>80,000 total "
        "cost &minus; 20,000 fixed</span>", ["(60,000)"]),
       ("<b>Contribution</b>", ["<b>40,000</b>"], "sub"),
       ("<i>Less:</i> Fixed cost", ["(20,000)"]),
       ("<b>Profit</b> &nbsp;<span class='src' style='display:inline'>agrees with the given "
        "figure &#10003;</span>", ["<b>20,000</b>"], "tot")])

    wnh = f"""{fml("(a) &nbsp; P/V ratio &nbsp;=&nbsp; " + frac("Contribution", "Sales")
     + " &times; 100 &nbsp;=&nbsp; " + frac("40,000", "1,00,000") + " &times; 100 &nbsp;=&nbsp; "
     "<b>40%</b>")}
{fml("(b) &nbsp; BEP &nbsp;=&nbsp; " + frac("Fixed cost", "P/V ratio") + " &nbsp;=&nbsp; "
     + frac("20,000", "0.40") + f" &nbsp;=&nbsp; <b>{R}50,000</b>")}
{fml("(c) &nbsp; MOS &nbsp;=&nbsp; Actual sales &minus; BEP sales &nbsp;=&nbsp; 1,00,000 &minus; "
     f"50,000 &nbsp;=&nbsp; <b>{R}50,000</b>",
     "Check by the other route: MOS = Profit &divide; P/V ratio = 20,000 &divide; 0.40 = "
     + R + "50,000 &#10003;")}"""

    return ("<div class='prob'>"
            + prob_head("Q10", "Extracting variable cost from total cost", "CVP &middot; p.23")
            + question(q) + read(rd) + s + wn(wnh)
            + ans([("Variable cost (derived)", f"{R} 60,000"),
                   ("Contribution", f"{R} 40,000"),
                   ("<b>(a) P/V ratio</b>", "<b>40%</b>"),
                   ("<b>(b) Break-even point</b>", f"<b>{R} 50,000</b>"),
                   ("<b>(c) Margin of safety</b>", f"<b>{R} 50,000 &mdash; 50% of sales</b>")])
            + "</div>")


# ======================================================================
# Q11
# ======================================================================
def q11():
    q = f"""<p>The following information is obtained from a company for 2016: Sales
<span class="rs">{R}</span>20,000; Variable Cost <span class="rs">{R}</span>10,000; Fixed Cost
<span class="rs">{R}</span>6,000.</p>
<p><b>(a)</b> Find P/V Ratio, Break-even point and Margin of safety at this level, and
<b>(b)</b> the effect on P/V Ratio, Break-even point and Margin of safety if:
(i) 20% decrease in fixed cost; (ii) 10% increase in fixed cost; (iii) 10% decrease in variable
cost; (iv) 10% increase in variable cost; (v) 10% increase in selling price together with an
increase of fixed overheads by <span class="rs">{R}</span>1,200; (vi) 10% decrease in selling price;
(vii) 10% decrease in sales price accompanied by 10% decrease in variable costs.</p>"""

    rd = f"""{bullets([
 'Eight columns of the same four-line statement. <b>Do it as one wide table</b>, exactly as your '
 'classmate&rsquo;s notes do &mdash; never as eight separate little sums, or you will lose track.',
 'Work out which line each change touches <b>before</b> you compute anything: a fixed-cost change '
 'touches only the FC line and leaves the P/V ratio alone; a variable-cost or selling-price change '
 'moves contribution and therefore <b>does</b> change the P/V ratio.',
 'In (v) the selling price rises 10% so sales become 22,000, but the <b>variable cost stays at '
 '10,000</b> &mdash; volume has not changed, only price. Same logic in (vi).',
 '<b>In (vii) both fall 10%</b>, so contribution falls 10% too and the <b>P/V ratio is unchanged '
 'at 50%</b>. That is the interesting result of the whole question.'])}"""

    guide = table("Which line does each change touch?",
      [("Case", ""), ("Sales", "c"), ("Variable cost", "c"), ("Fixed cost", "c"),
       ("Does the P/V ratio change?", "")],
      [["(i) FC down 20%", "&mdash;", "&mdash;", "&darr; 4,800", "<b>No</b> &mdash; contribution untouched"],
       ["(ii) FC up 10%", "&mdash;", "&mdash;", "&uarr; 6,600", "<b>No</b>"],
       ["(iii) VC down 10%", "&mdash;", "&darr; 9,000", "&mdash;", "<b>Yes</b> &mdash; rises to 55%"],
       ["(iv) VC up 10%", "&mdash;", "&uarr; 11,000", "&mdash;", "<b>Yes</b> &mdash; falls to 45%"],
       ["(v) SP up 10%, FC up 1,200", "&uarr; 22,000", "&mdash;", "&uarr; 7,200",
        "<b>Yes</b> &mdash; rises to 54.55%"],
       ["(vi) SP down 10%", "&darr; 18,000", "&mdash;", "&mdash;",
        "<b>Yes</b> &mdash; falls to 44.44%"],
       ["(vii) SP down 10% and VC down 10%", "&darr; 18,000", "&darr; 9,000", "&mdash;",
        "<b>No</b> &mdash; stays exactly 50%"]], headcls="lite",
      widths=["24%","13%","15%","13%","35%"])

    big = table("Complete solution &mdash; all eight situations in one statement",
      [("Particulars", ""), ("(a) Present", "r"), ("(i)", "r"), ("(ii)", "r"), ("(iii)", "r"),
       ("(iv)", "r"), ("(v)", "r"), ("(vi)", "r"), ("(vii)", "r")],
      [["Sales", "20,000", "20,000", "20,000", "20,000", "20,000", "22,000", "18,000", "18,000"],
       ["<i>Less:</i> Variable cost", "(10,000)", "(10,000)", "(10,000)", "(9,000)", "(11,000)",
        "(10,000)", "(10,000)", "(9,000)"],
       {"cls": "sub", "cells": ["<b>Contribution</b>", "<b>10,000</b>", "<b>10,000</b>",
                                 "<b>10,000</b>", "<b>11,000</b>", "<b>9,000</b>", "<b>12,000</b>",
                                 "<b>8,000</b>", "<b>9,000</b>"]},
       ["<i>Less:</i> Fixed cost", "(6,000)", "(4,800)", "(6,600)", "(6,000)", "(6,000)",
        "(7,200)", "(6,000)", "(6,000)"],
       {"cls": "tot", "cells": ["<b>Profit</b>", "<b>4,000</b>", "<b>5,200</b>", "<b>3,400</b>",
                                 "<b>5,000</b>", "<b>3,000</b>", "<b>4,800</b>", "<b>2,000</b>",
                                 "<b>3,000</b>"]},
       {"cls": "sub", "cells": ["<b>P/V ratio</b>", "50.00%", "50.00%", "50.00%", "55.00%",
                                 "45.00%", "54.55%", "44.44%", "50.00%"]},
       {"cls": "sub", "cells": ["<b>BEP sales</b>", "12,000", "9,600", "13,200", "10,909",
                                 "13,333", "13,200", "13,500", "12,000"]},
       {"cls": "sub", "cells": ["<b>Margin of safety</b>", "8,000", "10,400", "6,800", "9,091",
                                 "6,667", "8,800", "4,500", "6,000"]}])

    wk = f"""<h4 class="mini">How the BEP row was computed in each column</h4>
{table(None, [("Case",""),("Fixed cost","r"),("P/V ratio","r"),("BEP = FC &divide; P/V","r"),
              ("MOS = Sales &minus; BEP","r")],
 [["(a)","6,000","50.00%","12,000","8,000"],
  ["(i)","4,800","50.00%","9,600","10,400"],
  ["(ii)","6,600","50.00%","13,200","6,800"],
  ["(iii)","6,000","55.00%","10,909","9,091"],
  ["(iv)","6,000","45.00%","13,333","6,667"],
  ["(v)","7,200","12,000/22,000 = 54.5455%","13,200","8,800"],
  ["(vi)","6,000","8,000/18,000 = 44.4444%","13,500","4,500"],
  ["(vii)","6,000","9,000/18,000 = 50.00%","12,000","6,000"]], headcls="lite")}"""

    return ("<div class='prob long'>"
            + prob_head("Q11", "Eight situations in one statement", "CVP &middot; p.23")
            + question(q) + read(rd) + guide + big + wn(wk)
            + trap(f"""<p><b>Important &mdash; two figures where care is needed.</b> In cases (v) and
(vi) the P/V ratio is a recurring decimal. If you round it to 0.54 and 0.44 before dividing you get
BEP figures of {R}13,333 and {R}13,636 instead of the correct {R}13,200 and {R}13,500. Your
classmate&rsquo;s handwritten notes contain exactly this rounding, so <b>if your answer differs from
those notes in columns (v) and (vi), you are right and the notes are rounded.</b></p>
<p>Keep the ratio as a fraction &mdash; 12,000/22,000 and 8,000/18,000 &mdash; and divide only once,
at the end.</p>""")
            + why("<p>Look across the P/V ratio row. It does not budge for (i) and (ii) because a "
                  "change in fixed cost cannot affect contribution. It moves for (iii) to (vi) "
                  "because each of those changes either the price or the variable cost. And in "
                  "(vii) it returns to exactly 50% because price and variable cost fell by the same "
                  "percentage, so their <i>ratio</i> is unchanged &mdash; the profit falls, but the "
                  "efficiency of each rupee of sales does not.</p>")
            + ans([("(a) Present &mdash; P/V / BEP / MOS", f"50% / {R} 12,000 / {R} 8,000"),
                   ("(i) FC down 20%", f"50% / {R} 9,600 / {R} 10,400 &mdash; profit {R} 5,200"),
                   ("(ii) FC up 10%", f"50% / {R} 13,200 / {R} 6,800 &mdash; profit {R} 3,400"),
                   ("(iii) VC down 10%", f"55% / {R} 10,909 / {R} 9,091 &mdash; profit {R} 5,000"),
                   ("(iv) VC up 10%", f"45% / {R} 13,333 / {R} 6,667 &mdash; profit {R} 3,000"),
                   ("(v) SP up 10%, FC up 1,200",
                    f"54.55% / {R} 13,200 / {R} 8,800 &mdash; profit {R} 4,800"),
                   ("(vi) SP down 10%", f"44.44% / {R} 13,500 / {R} 4,500 &mdash; profit {R} 2,000"),
                   ("(vii) SP and VC both down 10%",
                    f"50% / {R} 12,000 / {R} 6,000 &mdash; profit {R} 3,000")],
                  "The best single-sentence conclusion: a fixed-cost change moves the break-even "
                  "point but never the P/V ratio; a price or variable-cost change moves both.")
            + "</div>")


# ======================================================================
# Q12
# ======================================================================
def q12():
    q = f"""<p>You are given the following data: Variable Cost <span class="rs">{R}</span>6,00,000;
Fixed Cost <span class="rs">{R}</span>3,00,000; Net Profit <span class="rs">{R}</span>1,00,000;
Sales <span class="rs">{R}</span>10,00,000.</p>
<p>Find (a) P/V Ratio (b) B.E.P. (c) Profit when sales amounted to
<span class="rs">{R}</span>12,00,000 (d) Sales required to earn a profit of
<span class="rs">{R}</span>2,00,000.</p>"""

    s = stmt("Marginal Cost Statement (present position)",
      ["Amount " + R],
      [("Sales", ["10,00,000"]),
       ("<i>Less:</i> Variable cost", ["(6,00,000)"]),
       ("<b>Contribution</b>", ["<b>4,00,000</b>"], "sub"),
       ("<i>Less:</i> Fixed cost", ["(3,00,000)"]),
       ("<b>Profit</b> &nbsp;<span class='src' style='display:inline'>agrees with the given "
        f"{R}1,00,000 &#10003;</span>", ["<b>1,00,000</b>"], "tot")])

    wnh = f"""{fml("(a) &nbsp; P/V ratio &nbsp;=&nbsp; " + frac("4,00,000", "10,00,000")
     + " &times; 100 &nbsp;=&nbsp; <b>40%</b>")}
{fml("(b) &nbsp; BEP &nbsp;=&nbsp; " + frac("3,00,000", "0.40") + f" &nbsp;=&nbsp; "
     f"<b>{R}7,50,000</b>")}
<h4 class="mini">(c) Profit when sales are {R}12,00,000</h4>
{calc(['Contribution &nbsp;=&nbsp; 12,00,000 &times; 40% &nbsp;=&nbsp; 4,80,000',
       'Less: Fixed cost &nbsp;=&nbsp; (3,00,000)',
       f'<b>Profit &nbsp;=&nbsp; {R}1,80,000</b>'])}
<p class="small">Faster route: extra sales of {R}2,00,000 &times; 40% = {R}80,000 extra profit, so
1,00,000 + 80,000 = {R}1,80,000. Fixed cost does not change, so every extra rupee of contribution is
extra profit.</p>
<h4 class="mini">(d) Sales required for a profit of {R}2,00,000</h4>
{fml("Required sales &nbsp;=&nbsp; " + frac("Fixed cost + Target profit", "P/V ratio")
     + " &nbsp;=&nbsp; " + frac("3,00,000 + 2,00,000", "0.40") + " &nbsp;=&nbsp; "
     + frac("5,00,000", "0.40") + f" &nbsp;=&nbsp; <b>{R}12,50,000</b>")}"""

    return ("<div class='prob'>"
            + prob_head("Q12", "The four standard CVP questions", "CVP &middot; p.23")
            + question(q)
            + read(bullets([
                'All four parts come from the same statement, so <b>build the statement first</b> '
                'and answer from it.',
                'For (c) and (d) remember the fixed cost does <b>not</b> change with volume. That '
                'is what makes both parts one-line calculations.',
                'For (d), treat the target profit exactly like extra fixed cost that must also be '
                'covered.']))
            + s + wn(wnh)
            + ans([("<b>(a) P/V ratio</b>", "<b>40%</b>"),
                   ("<b>(b) Break-even point</b>", f"<b>{R} 7,50,000</b>"),
                   ("<b>(c) Profit at sales of {} 12,00,000</b>".format(R),
                    f"<b>{R} 1,80,000</b>"),
                   ("<b>(d) Sales to earn {} 2,00,000</b>".format(R), f"<b>{R} 12,50,000</b>"),
                   ("Margin of safety at present", f"{R} 2,50,000")])
            + "</div>")


# ======================================================================
# Q13
# ======================================================================
def q13():
    q = f"""<p>From the following, find out (i) Profit Volume Ratio (ii) Break-even point
(iii) Sales for 40% P/V Ratio (iv) Margin of Safety if actual sales were
<span class="rs">{R}</span>3,00,000 (v) Net Profit if actual sales were
<span class="rs">{R}</span>3,00,000 (vi) Required Sales to earn a profit of
<span class="rs">{R}</span>70,000 (vii) Required sales to earn a net profit of
<span class="rs">{R}</span>70,000 after tax, given tax rate = 60%.</p>
{table(None, [("Position of the Co. for the year 2025",""),("" + R,"r")],
 [["Sales","2,00,000"],["Variable Cost","1,50,000"],["Contribution","50,000"],
  ["Fixed Cost","15,000"],["Profit","35,000"]], headcls="lite", widths=["70%","30%"])}"""

    rd = f"""{bullets([
 'Seven parts, and the last two are the ones that separate students.',
 '<b>Part (iii) needs interpreting.</b> The P/V ratio does not depend on volume, so &ldquo;sales '
 'for 40% P/V ratio&rdquo; must mean: what sales value would give a 40% P/V ratio if the '
 'variable cost stays at ' + R + '1,50,000? If contribution is to be 40% of sales, variable cost '
 'must be 60% of sales &mdash; so sales = 1,50,000 &divide; 0.60.',
 '<b>Part (vii) is about tax.</b> ' + R + '70,000 is wanted <i>after</i> 60% tax, so the profit '
 'before tax must be bigger. Gross it up first: pre-tax profit = 70,000 &divide; (1 &minus; 0.60). '
 'Only then use the sales formula. Forgetting to gross up is the classic error.'])}"""

    wnh = f"""{fml("(i) &nbsp; P/V ratio &nbsp;=&nbsp; " + frac("50,000", "2,00,000")
     + " &times; 100 &nbsp;=&nbsp; <b>25%</b>")}
{fml("(ii) &nbsp; BEP &nbsp;=&nbsp; " + frac("15,000", "0.25") + f" &nbsp;=&nbsp; "
     f"<b>{R}60,000</b>")}

<h4 class="mini">(iii) Sales that would give a 40% P/V ratio</h4>
{calc(['If contribution is 40% of sales, then variable cost is 60% of sales',
       'Variable cost is unchanged at 1,50,000',
       f'Sales &nbsp;=&nbsp; ' + frac("1,50,000", "0.60") + f' &nbsp;=&nbsp; <b>{R}2,50,000</b>'])}
<p class="small"><b>Check:</b> at sales of 2,50,000 the contribution is 2,50,000 &minus; 1,50,000 =
{R}1,00,000, which is exactly 40% of 2,50,000 &#10003;</p>

<h4 class="mini">(iv) and (v) &mdash; if actual sales were {R}3,00,000</h4>
{calc([f'MOS &nbsp;=&nbsp; 3,00,000 &minus; 60,000 (BEP) &nbsp;=&nbsp; <b>{R}2,40,000</b>',
       'Contribution &nbsp;=&nbsp; 3,00,000 &times; 25% &nbsp;=&nbsp; 75,000',
       f'Net profit &nbsp;=&nbsp; 75,000 &minus; 15,000 &nbsp;=&nbsp; <b>{R}60,000</b>'])}
<p class="small">Or: profit = MOS &times; P/V ratio = 2,40,000 &times; 25% = {R}60,000 &#10003;</p>

<h4 class="mini">(vi) Sales to earn a profit of {R}70,000</h4>
{fml("Required sales &nbsp;=&nbsp; " + frac("15,000 + 70,000", "0.25") + " &nbsp;=&nbsp; "
     + frac("85,000", "0.25") + f" &nbsp;=&nbsp; <b>{R}3,40,000</b>")}

<h4 class="mini">(vii) Sales to earn {R}70,000 <i>after</i> 60% tax</h4>
{calc(['Step 1 &mdash; gross the profit up to a pre-tax figure:',
       f'Profit before tax &nbsp;=&nbsp; ' + frac("70,000", "1 &minus; 0.60") + ' &nbsp;=&nbsp; '
       + frac("70,000", "0.40") + f' &nbsp;=&nbsp; <b>{R}1,75,000</b>',
       'Step 2 &mdash; now use the ordinary formula on the pre-tax profit:'])}
{fml("Required sales &nbsp;=&nbsp; " + frac("15,000 + 1,75,000", "0.25") + " &nbsp;=&nbsp; "
     + frac("1,90,000", "0.25") + f" &nbsp;=&nbsp; <b>{R}7,60,000</b>")}
<p class="small"><b>Check:</b> sales 7,60,000 &times; 25% = contribution 1,90,000; less fixed cost
15,000 = pre-tax profit 1,75,000; less tax at 60% = 1,05,000; net profit = {R}70,000 &#10003;</p>"""

    return ("<div class='prob long'>"
            + prob_head("Q13", "Seven parts including tax", "CVP &middot; p.24")
            + question(q) + read(rd) + wn(wnh)
            + trap(bullets([
                '<b>Part (vii):</b> dividing 70,000 by 0.25 straight away, without grossing up for '
                f'tax. That gives {R}3,40,000 &mdash; the answer to part (vi), not part (vii). '
                'Tax always comes out <i>after</i> profit, so the profit you need to <i>earn</i> is '
                'always bigger than the profit you want to <i>keep</i>.',
                '<b>Part (iii):</b> trying to change the P/V ratio by changing volume. Volume '
                'cannot change a ratio of contribution to sales &mdash; only price or variable cost '
                'can. State your assumption that variable cost is unchanged.']))
            + ans([("<b>(i) P/V ratio</b>", "<b>25%</b>"),
                   ("<b>(ii) Break-even point</b>", f"<b>{R} 60,000</b>"),
                   ("<b>(iii) Sales for 40% P/V ratio</b>", f"<b>{R} 2,50,000</b>"),
                   ("<b>(iv) MOS at sales of {} 3,00,000</b>".format(R), f"<b>{R} 2,40,000</b>"),
                   ("<b>(v) Net profit at sales of {} 3,00,000</b>".format(R), f"<b>{R} 60,000</b>"),
                   ("<b>(vi) Sales for profit of {} 70,000</b>".format(R), f"<b>{R} 3,40,000</b>"),
                   ("<b>(vii) Sales for {} 70,000 after 60% tax</b>".format(R),
                    f"<b>{R} 7,60,000</b>")])
            + "</div>")


# ======================================================================
# Q14
# ======================================================================
def q14():
    q = f"""<p>Two manufacturing companies which have the following operating details decided to
merge:</p>
{table(None, [("Particulars",""),("Company I","r"),("Company II","r")],
 [["Capacity utilisation (%)","90","60"],
  ["Sales (" + R + " in lakhs)","540","300"],
  ["Variable costs (" + R + " in lakhs)","396","225"],
  ["Fixed costs (" + R + " in lakhs)","80","50"]], headcls="lite")}
<p>Assuming that the proposal is implemented, calculate:
<b>(a)</b> Break-even sales of the merged plant and the capacity utilisation at that stage;
<b>(b)</b> Profitability of the merged plant at 80% capacity utilisation;
<b>(c)</b> Sales turnover of the merged plant to earn a profit of <span class="rs">{R}</span>75
lakh; <b>(d)</b> When the merged plant is working at a capacity to earn a profit of
<span class="rs">{R}</span>75 lakh, what percentage increase in selling price is required to
sustain an increase of 5% in fixed overheads?</p>"""

    rd = f"""<p>This is the hardest problem in the module and it is worth learning properly, because
the same structure appears in every merger question.</p>
{bullets([
 '<b>The two companies are running at different capacities</b> &mdash; 90% and 60%. You cannot add '
 '540 and 300 and call it the merged sales, because those are sales at <i>different</i> levels of '
 'activity.',
 '<b>So step one is always: restate both companies at 100% capacity.</b> Divide sales and variable '
 'cost by the capacity percentage. Only then can you add them.',
 '<b>Fixed cost is NOT scaled up.</b> Fixed cost does not depend on capacity &mdash; that is what '
 'makes it fixed. Add 80 + 50 = 130 lakh and leave it alone. This is the single most common error.',
 'Once you have the merged plant at 100%, everything else is ordinary CVP work.',
 'Part (d) is different in kind: volume stays the same and you must recover extra fixed cost '
 'purely by raising price. So the price rise, in rupees, equals the extra fixed cost; express it '
 'as a percentage of the sales at that level.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Restate both companies at 100% capacity &mdash; the essential first step</h4>
{table(None, [("Particulars",""),("Company I at 90%","r"),("Company I at 100%","r"),
              ("Company II at 60%","r"),("Company II at 100%","r")],
 [["Sales","540","540 &divide; 0.90 = <b>600</b>","300","300 &divide; 0.60 = <b>500</b>"],
  ["Variable cost","396","396 &divide; 0.90 = <b>440</b>","225","225 &divide; 0.60 = <b>375</b>"],
  {"cls":"sub","cells":["<b>Contribution</b>","144","<b>160</b>","75","<b>125</b>"]},
  ["Fixed cost","80","<b>80</b> &nbsp;<span class='src' style='display:inline'>NOT scaled</span>",
   "50","<b>50</b> &nbsp;<span class='src' style='display:inline'>NOT scaled</span>"]],
 headcls="lite")}

<h4 class="mini">W2 &nbsp;The merged plant at 100% capacity</h4>
{table(None, [("Particulars",""),(R + " in lakhs","r")],
 [["Sales &nbsp;<span class='src' style='display:inline'>600 + 500</span>","1,100"],
  ["<i>Less:</i> Variable cost &nbsp;<span class='src' style='display:inline'>440 + 375</span>",
   "(815)"],
  {"cls":"sub","cells":["<b>Contribution</b>","<b>285</b>"]},
  ["<i>Less:</i> Fixed cost &nbsp;<span class='src' style='display:inline'>80 + 50, unchanged</span>",
   "(130)"],
  {"cls":"tot","cells":["<b>Profit at 100% capacity</b>","<b>155</b>"]}],
 headcls="lite", widths=["70%","30%"])}
{fml("P/V ratio of the merged plant &nbsp;=&nbsp; " + frac("285", "1,100") + " &times; 100 "
     "&nbsp;=&nbsp; <b>25.9091%</b>",
     "Keep this as the fraction 285/1,100 in every later division. Rounding it to 26% will move "
     "your break-even figure by several lakh.")}

<h4 class="mini">(a) Break-even sales and the capacity at that point</h4>
{fml("BEP sales &nbsp;=&nbsp; " + frac("Fixed cost", "P/V ratio") + " &nbsp;=&nbsp; "
     + frac("130", "285/1,100") + " &nbsp;=&nbsp; " + frac("130 &times; 1,100", "285")
     + " &nbsp;=&nbsp; <b>" + R + "501.75 lakh</b>")}
{calc(['Capacity utilisation at BEP &nbsp;=&nbsp; ' + frac("501.75", "1,100")
       + ' &times; 100 &nbsp;=&nbsp; <b>45.61%</b>'])}

<h4 class="mini">(b) Profitability at 80% capacity utilisation</h4>
{table(None, [("Particulars",""),(R + " in lakhs","r")],
 [["Sales &nbsp;<span class='src' style='display:inline'>80% of 1,100</span>","880.00"],
  ["<i>Less:</i> Variable cost &nbsp;<span class='src' style='display:inline'>80% of 815</span>",
   "(652.00)"],
  {"cls":"sub","cells":["<b>Contribution</b> &nbsp;<span class='src' style='display:inline'>80% of "
                        "285</span>","<b>228.00</b>"]},
  ["<i>Less:</i> Fixed cost","(130.00)"],
  {"cls":"tot","cells":["<b>Profit</b>","<b>98.00</b>"]}], headcls="lite", widths=["70%","30%"])}

<h4 class="mini">(c) Sales needed to earn a profit of {R}75 lakh</h4>
{fml("Required sales &nbsp;=&nbsp; " + frac("130 + 75", "285/1,100") + " &nbsp;=&nbsp; "
     + frac("205 &times; 1,100", "285") + " &nbsp;=&nbsp; <b>" + R + "791.23 lakh</b>")}
{calc(['Capacity at that level &nbsp;=&nbsp; 791.23 &divide; 1,100 &nbsp;=&nbsp; <b>71.93%</b>'])}

<h4 class="mini">(d) Price increase needed to absorb a 5% rise in fixed overheads</h4>
{calc([f'Increase in fixed cost &nbsp;=&nbsp; 5% of 130 &nbsp;=&nbsp; <b>{R}6.50 lakh</b>',
       'Volume is unchanged, so the whole 6.50 lakh must come from a higher selling price.',
       'Sales at that level (from part c) &nbsp;=&nbsp; ' + R + '791.23 lakh'])}
{fml("Required increase in selling price &nbsp;=&nbsp; " + frac("6.50", "791.23")
     + " &times; 100 &nbsp;=&nbsp; <b>0.82%</b>")}
<p class="small"><b>Check:</b> new sales = 791.23 &times; 1.0082 = {R}797.73 lakh. Contribution
rises by the full 6.50 (variable cost is unchanged because volume is unchanged) to 211.50; less new
fixed cost of 136.50 = {R}75 lakh profit &#10003;</p>"""

    return ("<div class='prob long'>"
            + prob_head("Q14", "Merger of two plants at different capacities",
                        "CVP &middot; p.24")
            + question(q) + read(rd) + wn(wnh)
            + trap(bullets([
                '<b>Scaling up the fixed cost along with sales.</b> Fixed cost stays at 130 lakh at '
                'every capacity. If you scale it you will get every one of the four answers wrong.',
                '<b>Adding 540 + 300 = 840 and treating that as merged sales.</b> Those are sales at '
                '90% and 60% respectively. Restate to 100% first &mdash; 600 + 500 = 1,100.',
                '<b>Rounding the P/V ratio to 26%.</b> It is 25.9091%. Use the fraction 285/1,100 '
                'throughout.',
                '<b>In part (d), also raising the variable cost.</b> Volume has not changed, so '
                'variable cost has not changed. Only the price moves.']))
            + ans([("Merged plant at 100% &mdash; sales / contribution / fixed cost",
                    f"{R} 1,100 L / {R} 285 L / {R} 130 L"),
                   ("P/V ratio of the merged plant", "25.9091%"),
                   ("<b>(a) Break-even sales</b>", f"<b>{R} 501.75 lakh</b>"),
                   ("<b>(a) Capacity utilisation at BEP</b>", "<b>45.61%</b>"),
                   ("<b>(b) Profit at 80% capacity</b>", f"<b>{R} 98 lakh</b>"),
                   ("<b>(c) Sales for a profit of {} 75 lakh</b>".format(R),
                    f"<b>{R} 791.23 lakh</b> (71.93% capacity)"),
                   ("<b>(d) Price increase for 5% higher fixed cost</b>", "<b>0.82%</b>")])
            + "</div>")



# ======================================================================
# Q15
# ======================================================================
def q15():
    q = f"""<p>Rain Until September Co makes a product, the Splash, which has a variable production
cost of {D}6 per unit and a sales price of {D}10 per unit. At the beginning of September 20X0 there
were no opening inventories and production during the month was 20,000 units. Fixed costs for the
month were {D}45,000 (production, administration, sales and distribution). There were no variable
marketing costs.</p>
<p>Calculate the contribution and profit for September 20X0, using marginal costing principles, if
sales were (a) 10,000 Splashes (b) 15,000 Splashes (c) 20,000 Splashes.</p>"""

    rd = f"""{bullets([
 '<b>Marginal costing only</b> &mdash; the question says so. That makes it simple: fixed cost of ' +
 D + '45,000 is charged in full in every one of the three cases, no matter how much was sold.',
 'Contribution per unit = 10 &minus; 6 = ' + D + '4. Multiply by <b>units SOLD</b>, not units '
 'produced. Contribution comes from selling, not from making.',
 'Production is 20,000 in all three cases, so the closing inventory differs: 10,000, 5,000 and nil '
 'units. Under marginal costing it is valued at the variable cost of ' + D + '6.',
 'Notice case (a) makes a <b>loss</b>. Do not assume every answer is a profit &mdash; write the '
 'bracket.'])}"""

    s = stmt("Marginal Costing Profit Statement &mdash; September 20X0",
      ["(a) Sales 10,000", "(b) Sales 15,000", "(c) Sales 20,000"],
      [("Sales &nbsp;<span class='src' style='display:inline'>units sold &times; " + D + "10</span>",
        ["1,00,000", "1,50,000", "2,00,000"]),
       ("<i>Less:</i> Variable cost of sales &nbsp;<span class='src' style='display:inline'>units "
        "sold &times; " + D + "6</span>", ["(60,000)", "(90,000)", "(1,20,000)"]),
       ("<b>CONTRIBUTION</b>", ["<b>40,000</b>", "<b>60,000</b>", "<b>80,000</b>"], "sub"),
       ("<i>Less:</i> Fixed costs &nbsp;<span class='src' style='display:inline'>charged in full "
        "every time</span>", ["(45,000)", "(45,000)", "(45,000)"]),
       ("<b>PROFIT / (LOSS)</b>", ["<b>(5,000)</b>", "<b>15,000</b>", "<b>35,000</b>"], "tot"),
       ("<i>Memo:</i> closing inventory in units", ["10,000", "5,000", "Nil"], "sub"),
       ("<i>Memo:</i> closing inventory value at " + D + "6",
        ["60,000", "30,000", "Nil"], "sub")], cur=D)

    bep = f"""{calc([f'Contribution per unit &nbsp;=&nbsp; 10 &minus; 6 &nbsp;=&nbsp; <b>{D}4</b>',
       'Break-even point &nbsp;=&nbsp; ' + frac("45,000", "4") + ' &nbsp;=&nbsp; '
       '<b>11,250 units</b>'])}
<p class="small">That single figure explains all three answers at a glance: 10,000 units is below
break-even so there is a loss; 15,000 and 20,000 are above it so there is a profit.</p>"""

    return ("<div class='prob'>"
            + prob_head("Q15", "Marginal costing at three sales levels",
                        "Statements &middot; p.25")
            + question(q) + read(rd) + s + wn(bep)
            + why("<p>Because the fixed cost is charged in full every time, profit moves in exact "
                  f"step with contribution: each extra 5,000 units sold adds 5,000 &times; {D}4 = "
                  f"{D}20,000 of profit. That straight-line relationship is the whole practical "
                  "value of marginal costing &mdash; a manager can read the effect of a volume "
                  "change immediately, which absorption costing does not allow.</p>")
            + ans([("Contribution per unit", f"{D} 4"),
                   ("Break-even point", "11,250 units"),
                   ("<b>(a) 10,000 units</b>",
                    f"Contribution {D} 40,000 &mdash; <b>Loss {D} 5,000</b>"),
                   ("<b>(b) 15,000 units</b>",
                    f"Contribution {D} 60,000 &mdash; <b>Profit {D} 15,000</b>"),
                   ("<b>(c) 20,000 units</b>",
                    f"Contribution {D} 80,000 &mdash; <b>Profit {D} 35,000</b>")])
            + "</div>")


# ======================================================================
# Q16
# ======================================================================
def q16():
    q = f"""<p>A company makes and sells a single product. At the beginning of period 1 there is no
opening stock of the product, for which the variable production cost is {R}4 and the sale price is
{R}6 per unit. Fixed costs are {R}2,000 per period, of which {R}1,500 are fixed production
costs.</p>
{table(None, [("Particulars",""),("Period 1","r"),("Period 2","r")],
 [["Sales","1,200 units","1,800 units"],["Production","1,500 units","1,500 units"]],
 headcls="lite")}
<p>What would be the profit in each period using (a) Absorption costing (assume normal output is
1,500 units per period) and (b) Marginal costing?</p>"""

    rd = f"""{bullets([
 '<b>Do the stock movement first.</b> Period 1: 0 + 1,500 &minus; 1,200 = <b>300 units closing</b>. '
 'Period 2: 300 + 1,500 &minus; 1,800 = <b>nil closing</b>.',
 'So stock <b>rises</b> in period 1 (absorption profit will be higher) and <b>falls back to zero</b> '
 'in period 2 (absorption profit will be lower). Predict the direction before you calculate &mdash; '
 'then your answer confirms it.',
 'Only ' + R + '1,500 of the ' + R + '2,000 fixed cost is a <b>production</b> cost, so only that '
 'part is absorbed into units. The other ' + R + '500 is a non-production fixed cost and is '
 'deducted below gross profit in the absorption statement.',
 'Production equals normal output (1,500) in both periods, so there is <b>no under or over '
 'absorption</b> anywhere in this problem. That is deliberate &mdash; it isolates the stock effect.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Stock movement and the absorption rate</h4>
{table(None, [("",""),("Period 1","r"),("Period 2","r")],
 [["Opening stock (units)","Nil","300"],["Add: Production","1,500","1,500"],
  ["Less: Sales","(1,200)","(1,800)"],
  {"cls":"tot","cells":["<b>Closing stock (units)</b>","<b>300</b>","<b>Nil</b>"]}],
 headcls="lite")}
{fml("Fixed production overhead rate &nbsp;=&nbsp; " + frac(R + "1,500", "1,500 units normal output")
     + f" &nbsp;=&nbsp; <b>{R}1 per unit</b>")}
{calc([f'Full production cost per unit &nbsp;=&nbsp; variable 4 + fixed 1 &nbsp;=&nbsp; <b>{R}5</b>',
       f'Marginal (variable) cost per unit &nbsp;=&nbsp; <b>{R}4</b>'])}"""

    a = stmt("(a) Absorption Costing Profit Statement",
      ["Period 1 " + R, "Period 2 " + R],
      [("Sales &nbsp;<span class='src' style='display:inline'>units &times; " + R + "6</span>",
        ["7,200", "10,800"]),
       ("Opening stock &nbsp;<span class='src' style='display:inline'>at " + R + "5 full cost</span>",
        ["Nil", "1,500"]),
       ("Add: Cost of production &nbsp;<span class='src' style='display:inline'>1,500 &times; "
        + R + "5</span>", ["7,500", "7,500"]),
       ("Less: Closing stock &nbsp;<span class='src' style='display:inline'>at " + R + "5</span>",
        ["(1,500)", "Nil"]),
       ("<b>Cost of sales</b>", ["<b>(6,000)</b>", "<b>(9,000)</b>"], "sub"),
       ("<b>Gross profit</b>", ["<b>1,200</b>", "<b>1,800</b>"], "sub"),
       ("Less: Non-production fixed costs &nbsp;<span class='src' style='display:inline'>2,000 "
        "&minus; 1,500</span>", ["(500)", "(500)"]),
       ("<b>PROFIT</b>", ["<b>700</b>", "<b>1,300</b>"], "tot")],
      note="No under or over absorption: production of 1,500 units equals normal output, so "
           "absorbed overhead of 1,500 &times; " + R + "1 = " + R + "1,500 exactly equals the "
           "actual fixed production cost.")

    m = stmt("(b) Marginal Costing Profit Statement",
      ["Period 1 " + R, "Period 2 " + R],
      [("Sales", ["7,200", "10,800"]),
       ("Opening stock &nbsp;<span class='src' style='display:inline'>at " + R + "4 variable cost"
        "</span>", ["Nil", "1,200"]),
       ("Add: Variable cost of production &nbsp;<span class='src' style='display:inline'>1,500 "
        "&times; " + R + "4</span>", ["6,000", "6,000"]),
       ("Less: Closing stock &nbsp;<span class='src' style='display:inline'>at " + R + "4</span>",
        ["(1,200)", "Nil"]),
       ("<b>Variable cost of sales</b>", ["<b>(4,800)</b>", "<b>(7,200)</b>"], "sub"),
       ("<b>CONTRIBUTION</b>", ["<b>2,400</b>", "<b>3,600</b>"], "sub"),
       ("Less: Fixed costs &nbsp;<span class='src' style='display:inline'>all " + R + "2,000, in "
        "full</span>", ["(2,000)", "(2,000)"]),
       ("<b>PROFIT</b>", ["<b>400</b>", "<b>1,600</b>"], "tot")])

    rec = stmt("Reconciliation &mdash; the proof",
      ["Period 1 " + R, "Period 2 " + R, "Total " + R],
      [("Marginal costing profit", ["400", "1,600", "2,000"]),
       ("Add: Fixed overhead in closing stock &nbsp;<span class='src' style='display:inline'>"
        "300 &times; " + R + "1 / nil</span>", ["300", "Nil", "&mdash;"]),
       ("Less: Fixed overhead in opening stock &nbsp;<span class='src' style='display:inline'>"
        "nil / 300 &times; " + R + "1</span>", ["Nil", "(300)", "&mdash;"]),
       ("<b>Absorption costing profit</b>", ["<b>700</b>", "<b>1,300</b>", "<b>2,000</b>"], "tot")],
      note="Over the two periods together both methods give " + R + "2,000. The methods differ only "
           "in <b>timing</b>, never in total profit over the life of the stock.")

    return ("<div class='prob long'>"
            + prob_head("Q16", "Both methods, two periods, full reconciliation",
                        "Statements &middot; p.25")
            + question(q) + read(rd) + wn(wnh) + a + m + rec
            + why(f"""<p>Follow the {R}300 through. In period 1, 300 unsold units carry {R}1 of fixed
cost each into the balance sheet instead of the profit and loss account &mdash; so absorption profit
is {R}300 higher. In period 2 those same units are sold, that {R}300 comes back out of stock and is
charged &mdash; so absorption profit is {R}300 lower. Over both periods it cancels exactly.</p>
<p>That is the whole marginal-versus-absorption argument in one number: absorption costing lets
profit be moved between periods by making stock. Marginal costing does not.</p>""")
            + ans([("Closing stock &mdash; Period 1 / Period 2", "300 units / Nil"),
                   ("Fixed production overhead rate", f"{R} 1 per unit"),
                   ("<b>Absorption profit &mdash; Period 1 / Period 2</b>",
                    f"<b>{R} 700 / {R} 1,300</b>"),
                   ("<b>Marginal profit &mdash; Period 1 / Period 2</b>",
                    f"<b>{R} 400 / {R} 1,600</b>"),
                   ("Total over both periods (either method)", f"{R} 2,000")])
            + "</div>")


# ======================================================================
# Q17
# ======================================================================
def q17():
    q = f"""<p>Mill Stream makes two products, the Mill and the Stream. Information relating to each
for April 20X1 is as follows.</p>
{table(None, [("Particulars",""),("Mill","r"),("Stream","r")],
 [["Opening inventory","Nil","Nil"],["Production (units)","15,000","6,000"],
  ["Sales (units)","10,000","5,000"],["Sales price per unit", D + "20", D + "30"],
  {"cls":"sub","cells":["<b>Unit costs</b>","",""]},
  ["Direct materials","8","14"],["Direct labour","4","2"],
  ["Variable production overhead","2","1"],["Variable sales overhead","2","3"],
  {"cls":"sub","cells":["<b>Fixed costs for the month</b>","",""]},
  ["Production costs", D + "40,000",""],["Administration costs", D + "15,000",""],
  ["Sales and distribution costs", D + "25,000",""]], headcls="lite")}
<p><b>(a)</b> Using marginal costing principles, calculate the profit in April 20X1.
<b>(b)</b> Calculate the profit if sales had been 15,000 units of Mill and 6,000 units of
Stream.</p>"""

    rd = f"""{bullets([
 'Marginal costing, so <b>total the fixed costs into one figure</b>: 40,000 + 15,000 + 25,000 = ' +
 D + '80,000. It is charged in full in both parts.',
 '<b>Variable sales overhead is included in the contribution calculation</b> because it varies with '
 'each unit sold &mdash; but it must <b>never</b> go into the value of unsold stock. Here it does '
 'not matter for stock because we only need the profit, but note the principle.',
 'Contribution per unit must be found for each product separately, then multiplied by <b>that '
 'product&rsquo;s</b> sales units.',
 'In part (b), production has not changed &mdash; only sales. Since fixed cost is unchanged too, '
 'the extra profit is simply the extra contribution.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Contribution per unit for each product</h4>
{table(None, [("Particulars",""),("Mill " + D,"r"),("Stream " + D,"r")],
 [["Selling price","20","30"],
  ["Less: Direct materials","(8)","(14)"],
  ["Less: Direct labour","(4)","(2)"],
  ["Less: Variable production overhead","(2)","(1)"],
  ["Less: Variable sales overhead","(2)","(3)"],
  {"cls":"tot","cells":["<b>Contribution per unit</b>","<b>4</b>","<b>10</b>"]},
  {"cls":"sub","cells":["<i>Memo:</i> variable production cost per unit "
                        "<span class='src' style='display:inline'>for stock valuation</span>",
                        "14","17"]}], headcls="lite")}

<h4 class="mini">W2 &nbsp;Total fixed costs for the month</h4>
{calc([f'Production 40,000 + Administration 15,000 + Sales and distribution 25,000 '
       f'&nbsp;=&nbsp; <b>{D}80,000</b>'])}"""

    a = stmt("(a) Marginal Costing Profit Statement &mdash; actual sales",
      ["Mill " + D, "Stream " + D, "Total " + D],
      [("Sales units", ["10,000", "5,000", "&mdash;"], "sub"),
       ("Contribution per unit &nbsp;<span class='src' style='display:inline'>W1</span>",
        ["4", "10", "&mdash;"], "sub"),
       ("<b>Total contribution</b>", ["<b>40,000</b>", "<b>50,000</b>", "<b>90,000</b>"], "sub"),
       ("<i>Less:</i> Fixed costs &nbsp;<span class='src' style='display:inline'>W2</span>",
        ["", "", "(80,000)"]),
       ("<b>PROFIT</b>", ["", "", "<b>10,000</b>"], "tot")], cur=D)

    b = stmt("(b) Marginal Costing Profit Statement &mdash; if all production had been sold",
      ["Mill " + D, "Stream " + D, "Total " + D],
      [("Sales units", ["15,000", "6,000", "&mdash;"], "sub"),
       ("Contribution per unit", ["4", "10", "&mdash;"], "sub"),
       ("<b>Total contribution</b>", ["<b>60,000</b>", "<b>60,000</b>", "<b>1,20,000</b>"], "sub"),
       ("<i>Less:</i> Fixed costs", ["", "", "(80,000)"]),
       ("<b>PROFIT</b>", ["", "", "<b>40,000</b>"], "tot")], cur=D)

    chk = f"""{calc(['Extra units sold &nbsp;=&nbsp; 5,000 Mill + 1,000 Stream',
       f'Extra contribution &nbsp;=&nbsp; (5,000 &times; 4) + (1,000 &times; 10) '
       f'&nbsp;=&nbsp; 20,000 + 10,000 &nbsp;=&nbsp; <b>{D}30,000</b>',
       f'Profit rises from {D}10,000 to {D}40,000 &nbsp;&mdash;&nbsp; an increase of exactly '
       f'{D}30,000 &#10003;'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q17", "Two products, marginal costing", "Statements &middot; p.25&ndash;26")
            + question(q) + read(rd) + wn(wnh) + a + b + wn(chk)
            + trap(bullets([
                'Multiplying contribution per unit by <b>production</b> units (15,000 and 6,000) in '
                f'part (a). Only 10,000 and 5,000 were sold. Contribution comes from sales.',
                'Leaving the variable <b>sales</b> overhead out of the contribution calculation. It '
                'is a variable cost and must be deducted &mdash; Mill&rsquo;s contribution is '
                f'{D}4, not {D}6.',
                'Splitting the fixed costs between the two products. There is no basis given and no '
                'need &mdash; under marginal costing you deduct total fixed cost from total '
                'contribution.']))
            + ans([("Contribution per unit &mdash; Mill / Stream", f"{D} 4 / {D} 10"),
                   ("Total fixed costs", f"{D} 80,000"),
                   ("<b>(a) Profit at actual sales</b>",
                    f"Contribution {D} 90,000 &minus; {D} 80,000 = <b>{D} 10,000</b>"),
                   ("<b>(b) Profit if all output sold</b>",
                    f"Contribution {D} 1,20,000 &minus; {D} 80,000 = <b>{D} 40,000</b>")])
            + "</div>")


# ======================================================================
# Q18
# ======================================================================
def q18():
    q = f"""<p>Big Woof Co manufactures a single product, the Bark: Selling price {D}180.00; Direct
materials {D}40.00; Direct labour {D}16.00; Variable overheads {D}10.00 per unit.</p>
<p>Annual fixed production overheads are budgeted to be {D}1.6 million and Big Woof expects to
produce 1,280,000 units of the Bark each year. Overheads are absorbed on a per unit basis. Actual
overheads are {D}1.6 million for the year. Budgeted fixed selling costs are {D}320,000 per quarter.
Actual sales and production for the first quarter of 20X8: <b>Sales 240,000 units; Production
280,000 units.</b> There is no opening inventory at the beginning of January.</p>
<p>Prepare statements of profit or loss for the quarter using (a) Marginal costing
(b) Absorption costing.</p>"""

    rd = f"""{bullets([
 '<b>Careful with the time periods.</b> The fixed production overhead of ' + D + '1.6 million is '
 'an <b>annual</b> figure, but you are preparing a <b>quarterly</b> statement. Divide by four: ' +
 D + '400,000 for the quarter. The selling cost of ' + D + '320,000 is already quarterly &mdash; do '
 'not divide it.',
 'The <b>absorption rate is built from the annual budget</b>: 1,600,000 &divide; 1,280,000 units = ' +
 D + '1.25 per unit. Do not use the quarterly figures to build the rate.',
 'Production 280,000 exceeds sales 240,000, so closing inventory is <b>40,000 units</b> and stock is '
 'rising &mdash; therefore <b>absorption profit will be higher</b>. Predict it, then prove it.',
 'Absorbed overhead = 280,000 &times; 1.25 = ' + D + '350,000 against an actual quarterly charge of ' +
 D + '400,000, so there is an <b>under-absorption of ' + D + '50,000</b> to be deducted.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Unit costs and the absorption rate</h4>
{calc([f'Variable cost per unit &nbsp;=&nbsp; 40 + 16 + 10 &nbsp;=&nbsp; <b>{D}66</b>',
       f'Contribution per unit &nbsp;=&nbsp; 180 &minus; 66 &nbsp;=&nbsp; <b>{D}114</b>'])}
{fml("Fixed production overhead absorption rate &nbsp;=&nbsp; "
     + frac(D + "1,600,000 per year", "1,280,000 units per year")
     + f" &nbsp;=&nbsp; <b>{D}1.25 per unit</b>")}
{calc([f'Full production cost per unit &nbsp;=&nbsp; 66 + 1.25 &nbsp;=&nbsp; <b>{D}67.25</b>'])}

<h4 class="mini">W2 &nbsp;Quarterly fixed costs and inventory</h4>
{calc([f'Fixed production overhead for the quarter &nbsp;=&nbsp; 1,600,000 &divide; 4 '
       f'&nbsp;=&nbsp; <b>{D}400,000</b>',
       f'Fixed selling cost for the quarter &nbsp;=&nbsp; <b>{D}320,000</b> (already quarterly)',
       'Closing inventory &nbsp;=&nbsp; 0 + 280,000 &minus; 240,000 &nbsp;=&nbsp; '
       '<b>40,000 units</b>'])}

<h4 class="mini">W3 &nbsp;Under / over absorption</h4>
{calc([f'Overhead absorbed &nbsp;=&nbsp; 280,000 units &times; {D}1.25 &nbsp;=&nbsp; 350,000',
       f'Actual overhead for the quarter &nbsp;=&nbsp; 400,000',
       f'<b>UNDER-absorbed &nbsp;=&nbsp; {D}50,000</b> &nbsp;&mdash;&nbsp; deducted in the '
       'absorption statement'])}"""

    m = stmt("(a) Marginal Costing Statement of Profit or Loss &mdash; quarter to March 20X8",
      ["Amount " + D],
      [("Sales &nbsp;<span class='src' style='display:inline'>240,000 &times; " + D + "180</span>",
        ["43,200,000"]),
       ("<i>Less:</i> Variable cost of sales &nbsp;<span class='src' style='display:inline'>"
        "240,000 &times; " + D + "66</span>", ["(15,840,000)"]),
       ("<b>CONTRIBUTION</b> &nbsp;<span class='src' style='display:inline'>240,000 &times; "
        + D + "114</span>", ["<b>27,360,000</b>"], "sub"),
       ("<i>Less:</i> Fixed production overhead &nbsp;<span class='src' style='display:inline'>"
        "W2</span>", ["(400,000)"]),
       ("<i>Less:</i> Fixed selling costs", ["(320,000)"]),
       ("<b>PROFIT</b>", ["<b>26,640,000</b>"], "tot")], cur=D)

    a = stmt("(b) Absorption Costing Statement of Profit or Loss &mdash; quarter to March 20X8",
      ["Amount " + D],
      [("Sales", ["43,200,000"]),
       ("Cost of production &nbsp;<span class='src' style='display:inline'>280,000 &times; "
        + D + "67.25</span>", ["18,830,000"]),
       ("<i>Less:</i> Closing inventory &nbsp;<span class='src' style='display:inline'>40,000 "
        "&times; " + D + "67.25</span>", ["(2,690,000)"]),
       ("<b>Cost of sales</b> &nbsp;<span class='src' style='display:inline'>240,000 &times; "
        + D + "67.25</span>", ["<b>(16,140,000)</b>"], "sub"),
       ("<b>Gross profit</b>", ["<b>27,060,000</b>"], "sub"),
       ("<i>Less:</i> Under-absorbed fixed production overhead "
        "&nbsp;<span class='src' style='display:inline'>W3</span>", ["(50,000)"]),
       ("<i>Less:</i> Fixed selling costs", ["(320,000)"]),
       ("<b>PROFIT</b>", ["<b>26,690,000</b>"], "tot")], cur=D)

    rec = stmt("Reconciliation",
      ["Amount " + D],
      [("Marginal costing profit", ["26,640,000"]),
       ("Add: Fixed production overhead carried in closing inventory "
        "&nbsp;<span class='src' style='display:inline'>40,000 &times; " + D + "1.25</span>",
        ["50,000"]),
       ("<b>Absorption costing profit</b>", ["<b>26,690,000</b>"], "tot")], cur=D)

    return ("<div class='prob long'>"
            + prob_head("Q18", "Annual budget, quarterly statement",
                        "Statements &middot; p.26")
            + question(q) + read(rd) + wn(wnh) + m + a + rec
            + trap(bullets([
                '<b>Charging the whole ' + D + '1.6 million in a three-month statement.</b> It is '
                'an annual cost &mdash; only a quarter of it belongs to this quarter.',
                '<b>Dividing the ' + D + '320,000 selling cost by four.</b> The question says '
                '&ldquo;per quarter&rdquo;. Read the units on every figure.',
                '<b>Building the absorption rate from 280,000 actual units instead of 1,280,000 '
                'budgeted.</b> That would give ' + D + '1.43 and destroy the whole answer &mdash; and '
                'you would also find no under-absorption, which should ring a warning bell.']))
            + ans([("Contribution per unit", f"{D} 114"),
                   ("Absorption rate / full cost per unit", f"{D} 1.25 / {D} 67.25"),
                   ("Closing inventory", f"40,000 units = {D} 2,690,000"),
                   ("Under-absorbed overhead", f"{D} 50,000"),
                   ("<b>(a) Marginal costing profit</b>", f"<b>{D} 26,640,000</b>"),
                   ("<b>(b) Absorption costing profit</b>", f"<b>{D} 26,690,000</b>"),
                   ("Difference", f"{D} 50,000 = 40,000 units &times; {D} 1.25 &#10003;")])
            + "</div>")


# ======================================================================
# Q19
# ======================================================================
def q19():
    q = f"""<p>Eagle makes one product. Budgeted production and sales for the year just ended were
32,000 units. Actual sales for the year were 34,000 units at a selling price of {D}34 per unit, and
actual production was 36,000 units. Opening inventory was 5,000 units valued at the unit cost for
the preceding year. Using an absorption costing system based on budgeted levels of output, unit
costs for the year and the preceding year were as follows:</p>
{table(None, [("Particulars",""),("Year " + D,"r"),("Preceding year " + D,"r")],
 [["Prime cost","24","22"],["Variable production overhead","3.5","1"],
  ["Fixed production overhead","1.5","3"],
  ["Selling and administrative overhead (fixed)","1","1"],
  {"cls":"tot","cells":["<b>Total cost</b>","<b>30</b>","<b>27</b>"]},
  ["Profit","4","3"],["Selling price","34","30"]], headcls="lite")}
<p>Fixed production overhead for the year just ended was {D}48,000 (budget and actual). Actual
variable costs per unit were the same as budgeted. Prepare statements of profit or loss for the year
just ended on the basis that (i) an absorption costing system is used and (ii) a marginal costing
system is used.</p>"""

    rd = f"""<p>The hardest statement problem in the module, because <b>opening and closing stock are
valued at different rates</b> &mdash; last year&rsquo;s and this year&rsquo;s.</p>
{bullets([
 '<b>Opening inventory of 5,000 units is at the PRECEDING year&rsquo;s cost.</b> For absorption '
 'that is 22 + 1 + 3 = ' + D + '26 per unit. For marginal it is 22 + 1 = ' + D + '23 per unit. '
 'Note the fixed element was ' + D + '3 last year, not ' + D + '1.50.',
 'Closing inventory = 5,000 + 36,000 &minus; 34,000 = <b>7,000 units</b>, valued at <b>this</b> '
 'year&rsquo;s cost: absorption 24 + 3.5 + 1.5 = ' + D + '29; marginal 24 + 3.5 = ' + D + '27.50.',
 '<b>Check the fixed overhead rate:</b> ' + D + '48,000 &divide; 32,000 budgeted units = ' +
 D + '1.50 &#10003; which matches the table. That confirms the rate is built on budgeted output.',
 'Actual production 36,000 exceeds budget 32,000, so overhead is <b>OVER-absorbed</b>: '
 '36,000 &times; 1.50 = ' + D + '54,000 absorbed against ' + D + '48,000 actual, a credit of ' +
 D + '6,000.',
 'Selling and administrative overhead is <b>fixed</b>, so it is ' + D + '1 &times; 32,000 budgeted '
 'units = ' + D + '32,000 for the year &mdash; not ' + D + '1 &times; 34,000.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Inventory in units</h4>
{calc(['Opening 5,000 + Production 36,000 &minus; Sales 34,000 &nbsp;=&nbsp; '
       '<b>Closing 7,000 units</b>'])}

<h4 class="mini">W2 &nbsp;Unit values for stock &mdash; two different years, two different rates</h4>
{table(None, [("",""),("Absorption " + D,"r"),("Marginal " + D,"r")],
 [{"cls":"sub","cells":["<b>Opening stock &mdash; preceding year rates</b>","",""]},
  ["&nbsp;&nbsp;&nbsp;Prime cost","22","22"],
  ["&nbsp;&nbsp;&nbsp;Variable production overhead","1","1"],
  ["&nbsp;&nbsp;&nbsp;Fixed production overhead","3","&mdash;"],
  {"cls":"tot","cells":["&nbsp;&nbsp;&nbsp;<b>Per unit</b>","<b>26</b>","<b>23</b>"]},
  {"cls":"sub","cells":["<b>Closing stock &mdash; this year&rsquo;s rates</b>","",""]},
  ["&nbsp;&nbsp;&nbsp;Prime cost","24","24"],
  ["&nbsp;&nbsp;&nbsp;Variable production overhead","3.5","3.5"],
  ["&nbsp;&nbsp;&nbsp;Fixed production overhead","1.5","&mdash;"],
  {"cls":"tot","cells":["&nbsp;&nbsp;&nbsp;<b>Per unit</b>","<b>29</b>","<b>27.50</b>"]}],
 headcls="lite")}
{calc([f'Opening stock value &mdash; absorption &nbsp;=&nbsp; 5,000 &times; 26 &nbsp;=&nbsp; '
       f'<b>{D}130,000</b> &nbsp;|&nbsp; marginal &nbsp;=&nbsp; 5,000 &times; 23 &nbsp;=&nbsp; '
       f'<b>{D}115,000</b>',
       f'Closing stock value &mdash; absorption &nbsp;=&nbsp; 7,000 &times; 29 &nbsp;=&nbsp; '
       f'<b>{D}203,000</b> &nbsp;|&nbsp; marginal &nbsp;=&nbsp; 7,000 &times; 27.50 &nbsp;=&nbsp; '
       f'<b>{D}192,500</b>'])}

<h4 class="mini">W3 &nbsp;Over-absorption of fixed production overhead</h4>
{calc([f'Absorbed &nbsp;=&nbsp; 36,000 units &times; {D}1.50 &nbsp;=&nbsp; 54,000',
       f'Actual &nbsp;=&nbsp; 48,000',
       f'<b>OVER-absorbed &nbsp;=&nbsp; {D}6,000</b> &nbsp;&mdash;&nbsp; added back'])}"""

    a = stmt("(i) Absorption Costing Statement of Profit or Loss",
      ["Amount " + D],
      [("Sales &nbsp;<span class='src' style='display:inline'>34,000 &times; " + D + "34</span>",
        ["1,156,000"]),
       ("Opening inventory &nbsp;<span class='src' style='display:inline'>W2: 5,000 &times; "
        + D + "26</span>", ["130,000"]),
       ("Add: Cost of production &nbsp;<span class='src' style='display:inline'>36,000 &times; "
        + D + "29</span>", ["1,044,000"]),
       ("Less: Closing inventory &nbsp;<span class='src' style='display:inline'>W2: 7,000 &times; "
        + D + "29</span>", ["(203,000)"]),
       ("<b>Cost of sales</b>", ["<b>(971,000)</b>"], "sub"),
       ("<b>Gross profit</b>", ["<b>185,000</b>"], "sub"),
       ("Add: Over-absorbed fixed production overhead "
        "&nbsp;<span class='src' style='display:inline'>W3</span>", ["6,000"]),
       ("Less: Selling and administrative overhead "
        "&nbsp;<span class='src' style='display:inline'>fixed, " + D + "1 &times; 32,000 budget"
        "</span>", ["(32,000)"]),
       ("<b>PROFIT</b>", ["<b>159,000</b>"], "tot")], cur=D)

    m = stmt("(ii) Marginal Costing Statement of Profit or Loss",
      ["Amount " + D],
      [("Sales", ["1,156,000"]),
       ("Opening inventory &nbsp;<span class='src' style='display:inline'>W2: 5,000 &times; "
        + D + "23</span>", ["115,000"]),
       ("Add: Variable cost of production &nbsp;<span class='src' style='display:inline'>36,000 "
        "&times; " + D + "27.50</span>", ["990,000"]),
       ("Less: Closing inventory &nbsp;<span class='src' style='display:inline'>W2: 7,000 &times; "
        + D + "27.50</span>", ["(192,500)"]),
       ("<b>Variable cost of sales</b>", ["<b>(912,500)</b>"], "sub"),
       ("<b>CONTRIBUTION</b>", ["<b>243,500</b>"], "sub"),
       ("Less: Fixed production overhead &nbsp;<span class='src' style='display:inline'>actual"
        "</span>", ["(48,000)"]),
       ("Less: Selling and administrative overhead", ["(32,000)"]),
       ("<b>PROFIT</b>", ["<b>163,500</b>"], "tot")], cur=D)

    rec = stmt("Reconciliation",
      ["Amount " + D],
      [("Marginal costing profit", ["163,500"]),
       ("Add: Fixed overhead in closing inventory &nbsp;<span class='src' style='display:inline'>"
        "7,000 &times; " + D + "1.50</span>", ["10,500"]),
       ("Less: Fixed overhead in opening inventory &nbsp;<span class='src' style='display:inline'>"
        "5,000 &times; " + D + "3.00</span>", ["(15,000)"]),
       ("<b>Absorption costing profit</b>", ["<b>159,000</b>"], "tot")], cur=D,
      note="Here the absorption profit is <b>lower</b> even though inventory rose in units &mdash; "
           "because the fixed overhead rate <i>halved</i> from " + D + "3.00 to " + D + "1.50. "
           "Always reconcile on the <b>rupee value</b> of fixed overhead in stock, never on units.")

    return ("<div class='prob long'>"
            + prob_head("Q19", "Opening and closing stock at different rates",
                        "Statements &middot; p.26&ndash;27")
            + question(q) + read(rd) + wn(wnh) + a + m + rec
            + why(f"""<p>This problem exists to break a lazy rule. Students learn &ldquo;stock up
&rarr; absorption profit higher&rdquo; and apply it blindly. Here inventory rose from 5,000 to 7,000
units, yet absorption profit is {D}4,500 <b>lower</b>.</p>
<p>The reason is that the fixed overhead rate fell from {D}3.00 to {D}1.50. The 5,000 opening units
released {D}15,000 of last year&rsquo;s fixed cost into this year&rsquo;s charge, while the 7,000
closing units only carried {D}10,500 forward. The rule is really about the <b>value</b> of fixed
overhead held in stock, not the number of units.</p>""")
            + ans([("Closing inventory", "7,000 units"),
                   ("Stock value &mdash; absorption: opening / closing",
                    f"{D} 130,000 / {D} 203,000"),
                   ("Stock value &mdash; marginal: opening / closing",
                    f"{D} 115,000 / {D} 192,500"),
                   ("Over-absorbed overhead", f"{D} 6,000"),
                   ("<b>(i) Absorption costing profit</b>", f"<b>{D} 159,000</b>"),
                   ("<b>(ii) Marginal costing profit</b>", f"<b>{D} 163,500</b>"),
                   ("Difference", f"{D} 4,500 = 10,500 &minus; 15,000 &#10003;")])
            + "</div>")


# ======================================================================
# Q20
# ======================================================================
def q20():
    q = f"""<p>Stoney is drafting a budget on the basis of the following data: Direct material
{D}10 per unit; Direct labour {D}5 per unit; Variable production expenses {D}8 per unit; Fixed
production costs {D}27,000 per month; Normal output 9,000 units per month (90% capacity); Sales
price {D}30 per unit.</p>
<p>In order to build up inventory in anticipation of an increase in demand expected later in the
year, production is to exceed sales in the first three months as follows:</p>
{table(None, [("",""),("Month 1","r"),("Month 2","r"),("Month 3","r")],
 [["Production","6,500","9,000","10,000"],["Sales","5,000","8,500","9,500"]], headcls="lite")}
<p>Prepare two statements of profit or loss, each in comparative columnar form, covering each of the
three months: (i) on a marginal costing basis and (ii) on a full absorption costing basis.</p>"""

    rd = f"""{bullets([
 '<b>Track the inventory across all three months first</b> &mdash; the closing stock of one month is '
 'the opening stock of the next. Get this table right and the rest is mechanical.',
 'Absorption rate = 27,000 &divide; <b>9,000 normal output</b> = ' + D + '3 per unit. Note it is '
 'built on <b>normal</b> output, not on each month&rsquo;s actual production.',
 'That is why <b>each month has a different under/over absorption</b>: month 1 produces only 6,500 '
 '(under-absorbed), month 2 produces exactly 9,000 (nil), month 3 produces 10,000 (over-absorbed). '
 'This is the point of the problem.',
 'Stock rises every month, so <b>absorption profit is higher in every month</b>.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Inventory movement in units &mdash; carry it across the months</h4>
{table(None, [("",""),("Month 1","r"),("Month 2","r"),("Month 3","r")],
 [["Opening stock","Nil","1,500","2,000"],
  ["Add: Production","6,500","9,000","10,000"],
  ["Less: Sales","(5,000)","(8,500)","(9,500)"],
  {"cls":"tot","cells":["<b>Closing stock</b>","<b>1,500</b>","<b>2,000</b>","<b>2,500</b>"]}],
 headcls="lite")}

<h4 class="mini">W2 &nbsp;Unit costs</h4>
{calc([f'Variable production cost per unit &nbsp;=&nbsp; 10 + 5 + 8 &nbsp;=&nbsp; <b>{D}23</b>',
       f'Contribution per unit &nbsp;=&nbsp; 30 &minus; 23 &nbsp;=&nbsp; <b>{D}7</b>'])}
{fml("Fixed overhead absorption rate &nbsp;=&nbsp; "
     + frac(D + "27,000", "9,000 units normal output") + f" &nbsp;=&nbsp; <b>{D}3 per unit</b>")}
{calc([f'Full production cost per unit &nbsp;=&nbsp; 23 + 3 &nbsp;=&nbsp; <b>{D}26</b>'])}

<h4 class="mini">W3 &nbsp;Under / over absorption, month by month</h4>
{table(None, [("",""),("Month 1","r"),("Month 2","r"),("Month 3","r")],
 [["Production (units)","6,500","9,000","10,000"],
  ["Overhead absorbed at " + D + "3","19,500","27,000","30,000"],
  ["Actual fixed overhead","27,000","27,000","27,000"],
  {"cls":"tot","cells":["<b>Under (&minus;) / Over (+) absorbed</b>","<b>(7,500)</b>",
                        "<b>Nil</b>","<b>+3,000</b>"]}], headcls="lite")}"""

    m = stmt("(i) Marginal Costing Statements of Profit or Loss",
      ["Month 1 " + D, "Month 2 " + D, "Month 3 " + D],
      [("Sales &nbsp;<span class='src' style='display:inline'>units sold &times; " + D + "30</span>",
        ["150,000", "255,000", "285,000"]),
       ("Opening stock &nbsp;<span class='src' style='display:inline'>at " + D + "23</span>",
        ["Nil", "34,500", "46,000"]),
       ("Add: Variable cost of production &nbsp;<span class='src' style='display:inline'>&times; "
        + D + "23</span>", ["149,500", "207,000", "230,000"]),
       ("Less: Closing stock &nbsp;<span class='src' style='display:inline'>at " + D + "23</span>",
        ["(34,500)", "(46,000)", "(57,500)"]),
       ("<b>Variable cost of sales</b>", ["<b>(115,000)</b>", "<b>(195,500)</b>",
                                           "<b>(218,500)</b>"], "sub"),
       ("<b>CONTRIBUTION</b> &nbsp;<span class='src' style='display:inline'>units sold &times; "
        + D + "7</span>", ["<b>35,000</b>", "<b>59,500</b>", "<b>66,500</b>"], "sub"),
       ("Less: Fixed production costs &nbsp;<span class='src' style='display:inline'>in full every "
        "month</span>", ["(27,000)", "(27,000)", "(27,000)"]),
       ("<b>PROFIT</b>", ["<b>8,000</b>", "<b>32,500</b>", "<b>39,500</b>"], "tot")], cur=D)

    a = stmt("(ii) Absorption Costing Statements of Profit or Loss",
      ["Month 1 " + D, "Month 2 " + D, "Month 3 " + D],
      [("Sales", ["150,000", "255,000", "285,000"]),
       ("Opening stock &nbsp;<span class='src' style='display:inline'>at " + D + "26</span>",
        ["Nil", "39,000", "52,000"]),
       ("Add: Cost of production &nbsp;<span class='src' style='display:inline'>&times; "
        + D + "26</span>", ["169,000", "234,000", "260,000"]),
       ("Less: Closing stock &nbsp;<span class='src' style='display:inline'>at " + D + "26</span>",
        ["(39,000)", "(52,000)", "(65,000)"]),
       ("<b>Cost of sales</b> &nbsp;<span class='src' style='display:inline'>units sold &times; "
        + D + "26</span>", ["<b>(130,000)</b>", "<b>(221,000)</b>", "<b>(247,000)</b>"], "sub"),
       ("<b>Gross profit</b>", ["<b>20,000</b>", "<b>34,000</b>", "<b>38,000</b>"], "sub"),
       ("Under (&minus;) / Over (+) absorbed overhead "
        "&nbsp;<span class='src' style='display:inline'>W3</span>",
        ["(7,500)", "Nil", "3,000"]),
       ("<b>PROFIT</b>", ["<b>12,500</b>", "<b>34,000</b>", "<b>41,000</b>"], "tot")], cur=D)

    rec = stmt("Reconciliation, month by month",
      ["Month 1 " + D, "Month 2 " + D, "Month 3 " + D],
      [("Marginal costing profit", ["8,000", "32,500", "39,500"]),
       ("Add: Fixed overhead in closing stock &nbsp;<span class='src' style='display:inline'>"
        "closing units &times; " + D + "3</span>", ["4,500", "6,000", "7,500"]),
       ("Less: Fixed overhead in opening stock &nbsp;<span class='src' style='display:inline'>"
        "opening units &times; " + D + "3</span>", ["Nil", "(4,500)", "(6,000)"]),
       ("<b>Absorption costing profit</b>", ["<b>12,500</b>", "<b>34,000</b>", "<b>41,000</b>"],
        "tot"),
       ("<i>Memo:</i> increase in stock (units)", ["1,500", "500", "500"], "sub"),
       ("<i>Memo:</i> difference in profit &nbsp;<span class='src' style='display:inline'>"
        "= increase &times; " + D + "3</span>", ["4,500", "1,500", "1,500"], "sub")], cur=D)

    return ("<div class='prob long'>"
            + prob_head("Q20", "Three months, both methods, columnar form",
                        "Statements &middot; p.27")
            + question(q) + read(rd) + wn(wnh) + m + a + rec
            + why(f"""<p>Month 2 is the instructive one. Production of 9,000 exactly equals normal
output, so there is <b>no under or over absorption at all</b> &mdash; yet the two profits still
differ by {D}1,500, because stock still rose by 500 units. That separates the two effects cleanly:</p>
<ul class="tight">
<li><b>Under/over absorption</b> arises when actual production differs from <i>normal output</i>.</li>
<li><b>The marginal-versus-absorption profit gap</b> arises when production differs from <i>sales</i>.</li>
</ul>
<p>They are different things and a good answer does not confuse them.</p>""")
            + ans([("Contribution per unit / full cost per unit", f"{D} 7 / {D} 26"),
                   ("Absorption rate", f"{D} 3 per unit (27,000 &divide; 9,000 normal)"),
                   ("Closing stock &mdash; months 1 / 2 / 3", "1,500 / 2,000 / 2,500 units"),
                   ("<b>(i) Marginal profit &mdash; M1 / M2 / M3</b>",
                    f"<b>{D} 8,000 / {D} 32,500 / {D} 39,500</b>"),
                   ("<b>(ii) Absorption profit &mdash; M1 / M2 / M3</b>",
                    f"<b>{D} 12,500 / {D} 34,000 / {D} 41,000</b>"),
                   ("Under / over absorption &mdash; M1 / M2 / M3",
                    f"({D} 7,500) / Nil / +{D} 3,000")])
            + "</div>")


# ======================================================================
def build():
    return (opener() + playbook_a() + playbook_b()
            + q1() + q2() + q3() + q4() + q5() + q6() + q7() + q8() + q9()
            + q10() + q11() + q12() + q13() + q14()
            + q15() + q16() + q17() + q18() + q19() + q20())
