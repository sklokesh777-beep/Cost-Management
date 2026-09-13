# -*- coding: utf-8 -*-
"""FRONT MATTER - cover, how to read any question, master formula sheet"""
from build import (esc, rs, money, frac, question, read, method, wn, trap, why,
                   steps, bullets, fml, calc, ans, table, src, arrow_panel,
                   module_opener)

R = "&#8377;"


def cover():
    return f"""<div class="cover">
<div class="cover-band">
  <div class="cover-kicker">B.Com &middot; Third Year &middot; Master Solutions</div>
  <div class="cover-title">Cost Management &ndash; I</div>
  <div class="cover-sub">Every problem in the workbook, solved and explained</div>
</div>
<div class="cover-body">
  <p><span class="chip">109 problems</span>
     <span class="chip">6 modules</span>
     <span class="chip">Method playbook for every problem type</span>
     <span class="chip">Provenance on every figure</span>
     <span class="chip">All arithmetic machine-verified</span></p>

  <div class="cover-note">
  <p>This book solves <b>all 109 problems</b> in the workbook &mdash; the ones worked in class and the
  ones that were never worked. Each solution is set out in the same format as the handwritten notes, so
  that the method you practise here is the method you will write in the examination.</p>
  </div>

  {table(None, [("Module", ""), ("Topic", ""), ("Problems", "c"), ("Workbook pages", "c")],
   [["<b>1</b>", "Process Costing &mdash; normal and abnormal loss, joint and by-products, "
     "inter-process profit, equivalent production", "<b>24</b>", "1&ndash;20"],
    ["<b>2</b>", "Marginal and Absorption Costing &mdash; contribution, P/V ratio, break-even, "
     "margin of safety", "<b>20</b>", "21&ndash;31"],
    ["<b>3</b>", "Decision Making &mdash; special orders, make or buy, key factor, shut-down, "
     "break-even charts", "<b>18</b>", "32&ndash;38"],
    ["<b>4</b>", "Relevant Costing &mdash; sunk cost, opportunity cost, minimum price",
     "<b>15</b>", "39&ndash;44"],
    ["<b>5</b>", "Budgetary Control &mdash; flexible, cash, production, purchase and master budgets",
     "<b>15</b>", "49&ndash;55"],
    ["<b>6</b>", "Standard Costing &mdash; material, labour, overhead and sales variances",
     "<b>17</b>", "79&ndash;84"],
    {"cls": "tot", "cells": ["", "<b>Total</b>", "<b>109</b>", ""]}],
   headcls="lite", widths=["10%", "62%", "13%", "15%"])}

  <p class="small" style="margin-top:8mm"><b>How every solution is laid out.</b> Each problem follows
  the same five parts, always in this order, so that you can find what you need without re-reading:</p>
  {table(None, [("Part", ""), ("What it gives you", "")],
   [["<b>The question</b>", "Reproduced exactly as printed in your workbook"],
    ["<b>Read the question first</b>",
     "Which words matter, which figures are decoys, and what to compute before touching a formula"],
    ["<b>The working</b>",
     "Working notes, then the statement or account, with a red note under every figure showing "
     "<i>where it came from</i>"],
    ["<b>Why this works</b>",
     "The reasoning, the management conclusion, and the sentence that earns the last mark"],
    ["<b>Final answer</b>", "Boxed, so you can check yourself in seconds"]],
   headcls="lite", widths=["24%", "76%"])}

  <p class="small" style="margin-top:6mm"><b>A note on accuracy.</b> The figures in this book are
  checked by programs that recompute each answer independently from the workbook data &mdash;
  <b>1,333 checks in all</b>, covering every variance reconciliation, every ledger account balance and
  every column total. Where the handwritten notes contain a rounding slip, or the workbook itself
  contains data that cannot be reconciled, this is stated openly in the solution rather than quietly
  smoothed over.</p>
  <p class="small">Two such corrections are worth knowing about before an examination, because the
  published figures are wrong and yours will not match them:</p>
  {bullets([
   '<b>Module 6 Q1</b> &mdash; the mix and yield variances are ' + R + '26,363.64 (F) and '
   + R + '36,363.64 (A). Solutions that give ' + R + '26,365.60 and ' + R + '36,365.60 have rounded '
   'the revised standard quantity too early; only the exact pair differs by the usage variance of '
   + R + '10,000, as it must.',
   '<b>Module 6 Q14</b> &mdash; the fixed overhead cost variance is ' + R + '1,680 (A), not '
   + R + '1,848 (A). The actual overhead is <i>given</i> as ' + R + '1,68,000, so the actual rate is '
   + R + '0.9091 and not ' + R + '0.91. The correct figure is the only one that equals the '
   'expenditure variance plus the volume variance.'])}
</div>
</div>"""


def how_to_read():
    body = f"""
<h2 class="sec">The six questions to ask before you write anything</h2>
<p>Cost accounting problems are not comprehension tests, but they are written as though they were. The
data you need is scattered through the sentences, and some of it is there to mislead you. This procedure
works on <b>any</b> problem in any of the six modules.</p>

{table(None, [("", "c"), ("Ask yourself", ""), ("Why it matters", "")],
 [["<b>1</b>", "<b>What is the question actually asking me to produce?</b><br/>"
   "<span class='small'>A statement? An account? A decision? A price? A number of units?</span>",
   "Underline the requirement before reading the data. Half of all lost marks are for answering a "
   "different question &mdash; computing total cost when the question asked for relevant cost, or "
   "giving a break-even point when it asked for a margin of safety."],
  ["<b>2</b>", "<b>What is the OUTPUT figure, and does it match the standard?</b><br/>"
   "<span class='small'>Actual units produced, actual units sold, actual output in kg</span>",
   "Almost every formula in this syllabus is scaled to <b>actual</b> output. If the standard is for "
   "1,000 kg and actual output was 20,000 kg, every standard figure must be multiplied by 20. This "
   "single step decides Modules 1, 5 and 6."],
  ["<b>3</b>", "<b>Which costs are FIXED and which are VARIABLE?</b><br/>"
   "<span class='small'>Look for &ldquo;(60% variable)&rdquo;, &ldquo;40% fixed&rdquo;, "
   "&ldquo;50% of labour cost&rdquo;</span>",
   "Modules 2 to 6 all turn on this split. Do it in a working note <b>before</b> you start the main "
   "statement, and never scale a fixed cost with volume."],
  ["<b>4</b>", "<b>Which figures will CHANGE because of the decision?</b><br/>"
   "<span class='small'>and which are sunk, apportioned, allocated or absorbed?</span>",
   "This is the whole of Module 4 and most of Module 3. Book value, original cost, depreciation and "
   "apportioned overhead are almost always decoys. If you find yourself using every number in the "
   "question, you have probably made a mistake."],
  ["<b>5</b>", "<b>Is anything SCARCE?</b><br/>"
   "<span class='small'>limited materials, limited hours, limited capacity</span>",
   "If a resource runs out you are no longer choosing <i>whether</i> to produce but <i>what</i> to "
   "produce, and the answer becomes contribution per unit of the <b>scarce resource</b>, not per unit "
   "of product."],
  ["<b>6</b>", "<b>What period does each figure relate to?</b><br/>"
   "<span class='small'>per unit, per hour, per month, per year, per quarter</span>",
   "Mixing periods is the most expensive careless error in the syllabus. &ldquo;15 workers at "
   + R + "12,000 per month&rdquo; in an annual budget needs &times; 12; a yearly profit target in a "
   "monthly budget needs &divide; 12; annual fixed overhead in a quarterly shut-down decision needs "
   "&divide; 4."]],
 headcls="lite", widths=["5%", "35%", "60%"])}

<h2 class="sec" style="margin-top:6mm">Five habits that earn marks in every module</h2>
{steps([
 '<b>Write working notes, and number them W1, W2, W3.</b> Then reference them in the statement. An '
 'examiner who can see where a figure came from will give you the mark even if a later step is wrong; '
 'an unexplained figure earns nothing. This is why every solution in this book carries a red note '
 'under its figures.',
 '<b>Put the units on every heading.</b> &ldquo;kg&rdquo;, &ldquo;units&rdquo;, &ldquo;hours&rdquo;, '
 '&ldquo;' + R + '&rdquo;. It costs three seconds and it prevents the commonest arithmetic slip of '
 'all &mdash; multiplying a quantity by a quantity.',
 '<b>Cross-total everything.</b> If a statement has row totals and column totals, they must agree. If '
 'a variance splits into parts, the parts must add back. If a process account has two sides, they must '
 'balance. <b>Every one of these is a free check</b>, and this book performs them all explicitly.',
 '<b>Show negatives in brackets, and label every variance (F) or (A).</b> An untagged variance is '
 'not an answer, because the sign <i>is</i> the answer.',
 '<b>Finish with a sentence in words.</b> &ldquo;Accept the order; it increases profit by '
 + R + '4,000.&rdquo; &ldquo;Shut the plant; it saves ' + R + '15,000.&rdquo; Almost every problem in '
 'Modules 3, 4 and 5 carries a mark for the recommendation, and it is the easiest mark on the paper to '
 'earn and the most frequently forgotten.'])}

<div class="blk trap"><span class="lab">The seven decoys the workbook uses again and again</span>
{table(None, [("The decoy", ""), ("Where it appears", ""), ("What to do with it", "")],
 [["<b>Book value / written-down value</b>", "Module 4 Q3, Q4, Q7, Q15",
   "Ignore. Sunk cost."],
  ["<b>Original purchase price already paid</b>", "Module 4 Q3, Q8, Q12",
   "Ignore for the decision. It reappears only in a break-even-of-the-asset calculation."],
  ["<b>Apportioned / allocated / absorbed overhead</b>",
   "Module 3 Q3, Module 4 Q4, Q7, Q13, Q14, Q15", "Ignore. It is incurred either way."],
  ["<b>Depreciation</b>", "Module 5 cash budgets, Module 4",
   "Exclude from cash budgets entirely. Include in flexible and master budgets."],
  ["<b>The standard quantity for the STANDARD output</b>", "Module 6, every problem",
   "Scale it to the ACTUAL output first."],
  ["<b>A percentage applied to the wrong base</b>",
   "Module 5 Q14 (10% of <i>wages</i>, not sales), Module 5 Q1 (&ldquo;5% variable&rdquo; means 95% "
   "fixed)", "Read which base each percentage attaches to. The workbook alternates deliberately."],
  ["<b>An extra period of data</b>",
   "Module 5 Q8 (7 months for a 6-month budget), Module 5 Q5 (February purchases)",
   "It is not surplus. You have missed a lag or a closing-stock rule."]],
 headcls="lite", widths=["26%", "38%", "36%"])}
</div>
"""
    return module_opener("Before you start", "How to read any question in this syllabus",
                         "Works on all 109 problems", body)


def formula_sheet():
    body = f"""
<p>Everything in the six modules, on four pages. The problems each formula solves are listed beside
it, so you can go straight from a formula you half-remember to a worked example of it.</p>

<h2 class="sec">Module 1 &mdash; Process Costing</h2>
{table(None, [("Formula", ""), ("Notes", ""), ("Problems", "c")],
 [[fml("Cost per unit &nbsp;=&nbsp; " + frac("Total process cost &minus; Scrap value of normal loss",
                                            "Units introduced &minus; Normal loss units")),
   "<b>The central formula of the module.</b> Normal loss is removed from the denominator, so the good "
   "units absorb its cost. This is why normal loss has no cost of its own.", "<b>1&ndash;9</b>"],
  ["<b>Abnormal loss</b> = Actual loss &minus; Normal loss<br/>"
   "<b>Abnormal gain</b> = Normal loss &minus; Actual loss",
   "Both are valued at the <b>cost per unit computed above</b>, never at scrap value. Abnormal loss "
   "is debited to P&amp;L; abnormal gain is credited.", "<b>3&ndash;9</b>"],
  ["<b>Equivalent production</b> = Units completed + (Closing WIP &times; % complete) "
   "&minus; (Opening WIP &times; % already complete)",
   "Compute it <b>separately for material, labour and overhead</b>, because the degrees of completion "
   "differ. The last term applies only under FIFO.", "<b>17&ndash;24</b>"],
  ["<b>Inter-process profit</b>: transfer at cost + a percentage<br/>"
   "Unrealised profit in closing stock = " + frac("Profit in the transfer", "Transfer price")
   + " &times; Closing stock",
   "Needed when one process transfers to the next at a mark-up. The unrealised element must be "
   "eliminated from stock.", "<b>15, 16</b>"],
  ["<b>Joint cost apportionment</b> &mdash; on physical units, on sales value, or by the "
   "<b>reverse cost</b> method",
   "Reverse cost: work back from final sales value by deducting post-separation costs and the "
   "required profit margin.", "<b>10&ndash;14</b>"]],
 headcls="lite", widths=["44%", "42%", "14%"])}

<h2 class="sec" style="margin-top:6mm">Module 2 &mdash; Marginal Costing</h2>
{table(None, [("Formula", ""), ("Notes", ""), ("Problems", "c")],
 [[fml("Contribution &nbsp;=&nbsp; Sales &minus; Variable cost &nbsp;=&nbsp; Fixed cost + Profit"),
   "<b>Learn the second equality.</b> It is what lets you find fixed cost from profit, or profit from "
   "fixed cost, without knowing sales.", "<b>all</b>"],
  [fml("P/V ratio &nbsp;=&nbsp; " + frac("Contribution", "Sales") + " &times; 100")
   + fml("or, from two periods &nbsp;=&nbsp; "
         + frac("Change in profit", "Change in sales") + " &times; 100"),
   "The second form is how you find the P/V ratio from <b>two periods</b> of data without any cost "
   "breakdown at all.", "<b>1&ndash;14</b>"],
  [fml("BEP (units) &nbsp;=&nbsp; " + frac("Fixed cost", "Contribution per unit"))
   + fml("BEP (" + R + ") &nbsp;=&nbsp; " + frac("Fixed cost", "P/V ratio")),
   "At the break-even point contribution exactly equals fixed cost.", "<b>1&ndash;14</b>"],
  [fml("Sales for a target profit &nbsp;=&nbsp; " + frac("Fixed cost + Target profit", "P/V ratio")),
   "The same formula as BEP with the target profit added to fixed cost.", "<b>3&ndash;12</b>"],
  [fml("Margin of safety &nbsp;=&nbsp; Actual sales &minus; Break-even sales")
   + fml("or &nbsp;=&nbsp; " + frac("Profit", "P/V ratio")),
   "The second form is faster and is the one to use when profit is known.", "<b>4&ndash;13</b>"],
  ["<b>Absorption vs marginal profit</b><br/>Difference = Fixed overhead in closing stock "
   "&minus; Fixed overhead in opening stock",
   "Absorption profit is <b>higher</b> when stock rises, because fixed overhead is carried forward in "
   "the stock valuation instead of being charged.", "<b>15&ndash;20</b>"]],
 headcls="lite", widths=["44%", "42%", "14%"])}

<h2 class="sec" style="margin-top:6mm">Module 3 &mdash; Decision Making</h2>
{table(None, [("Situation", ""), ("What to compare", ""), ("Problems", "c")],
 [["<b>Special order / minimum price</b>",
   fml("Minimum price &nbsp;=&nbsp; Variable cost per unit &nbsp;+&nbsp; "
       + frac("Any extra fixed cost + contribution required", "Units in the order")),
   "<b>1, 2, 4, 5, 6, 11</b>"],
  ["<b>Make or buy</b>", "<b>Variable</b> cost of making against the buying price. Fixed cost "
   "continues either way, so exclude it. Add the contribution from any alternative use of the freed "
   "capacity.", "<b>3</b>"],
  ["<b>Key factor / limiting factor</b>",
   fml("Rank by &nbsp; " + frac("Contribution per unit", "Units of the scarce resource per unit"),
       "Then allocate the scarce resource down the ranking, capped at each product's maximum demand."),
   "<b>7&ndash;11</b>"],
  ["<b>Shut down or continue</b>",
   fml("Shut down if &nbsp; Avoidable fixed cost &nbsp;&gt;&nbsp; Contribution + Shut-down costs")
   + fml("Shut-down point &nbsp;=&nbsp; "
         + frac("Avoidable fixed cost &minus; Shut-down cost", "Contribution per unit")),
   "<b>12, 13, 14</b>"],
  ["<b>Break-even chart</b>",
   "Three lines: horizontal fixed cost; total cost starting <b>at the fixed cost, not at zero</b>; "
   "sales from the origin. BEP is where sales crosses total cost.", "<b>15&ndash;18</b>"]],
 headcls="lite", widths=["22%", "64%", "14%"])}

<h2 class="sec" style="margin-top:6mm">Module 4 &mdash; Relevant Costing</h2>
{fml("Will this amount be DIFFERENT if I say yes rather than no?",
     "If yes it is relevant; if no it is irrelevant. That single test settles every line of every "
     "problem in Module 4.")}
{table(None, [("Item", ""), ("Relevant?", "c"), ("Amount to use", "")],
 [["Material in stock, <b>regularly used</b>", "<b class='yes'>YES</b>",
   "Replacement cost &mdash; it will be bought again"],
  ["Material in stock, <b>not</b> regularly used", "<b class='yes'>YES</b>",
   "Opportunity cost = <b>HIGHER</b> of net realisable value or the saving as a substitute"],
  ["Material not in stock", "<b class='yes'>YES</b>", "Purchase / replacement price"],
  ["Labour with spare capacity, permanent staff", "<b class='no'>NO</b>",
   "<b>Nil</b> &mdash; committed cost, paid anyway"],
  ["Labour in short supply", "<b class='yes'>YES</b>", "Wages <b>plus</b> contribution forgone"],
  ["Labour to be newly hired", "<b class='yes'>YES</b>", "Wages &mdash; out-of-pocket cost"],
  ["Asset already owned", "<b class='yes'>YES</b>",
   "The <b>fall</b> in its resale value caused by using it &mdash; not its book value and not its "
   "full resale value"],
  ["Machine bought specially for the job", "<b class='yes'>YES</b>",
   "Cost <b>less</b> residual value at the end"],
  ["Sunk cost, book value, depreciation", "<b class='no'>NO</b>", "&mdash;"],
  ["Apportioned or absorbed overhead", "<b class='no'>NO</b>", "&mdash;"]],
 headcls="lite", widths=["34%", "13%", "53%"])}

<h2 class="sec" style="margin-top:6mm">Module 5 &mdash; Budgetary Control</h2>
{table(None, [("Formula", ""), ("Notes", ""), ("Problems", "c")],
 [[fml("Production budget &nbsp;=&nbsp; Budgeted sales &nbsp;+&nbsp; Closing stock "
       "&nbsp;&minus;&nbsp; Opening stock"),
   "In <b>units</b>. Determine the closing stock exactly as the question specifies &mdash; a flat "
   "figure, or 50% of next month's sales, or 90% of opening stock.", "<b>8, 10, 11, 12, 15</b>"],
  [fml("Purchase budget &nbsp;=&nbsp; Materials consumed &nbsp;+&nbsp; Closing stock "
       "&nbsp;&minus;&nbsp; Opening stock"),
   "Consumption comes from the <b>production</b> budget, never from the sales budget. Add closing "
   "orders and deduct opening orders if the question gives &ldquo;materials on order&rdquo;.",
   "<b>11, 12, 15</b>"],
  [fml("Closing cash &nbsp;=&nbsp; Opening cash &nbsp;+&nbsp; Receipts &nbsp;&minus;&nbsp; Payments"),
   "Build a working note for every item with a credit period <b>before</b> starting the budget. "
   "Exclude depreciation. Carry a negative balance forward as negative.", "<b>5, 6, 7</b>"],
  ["<b>Flexible budget</b>: split every cost into fixed and variable, hold the fixed <b>total</b> "
   "constant and scale only the variable",
   "Check any flexible budget in seconds with<br/>Total cost = (variable rate &times; units) + total "
   "fixed cost.", "<b>1, 2, 3, 4</b>"],
  [fml("High&ndash;low: &nbsp; Variable rate &nbsp;=&nbsp; "
       + frac("Change in total cost", "Change in volume"))
   + fml("Fixed &nbsp;=&nbsp; Total cost at either volume &nbsp;&minus;&nbsp; "
         "(rate &times; that volume)"),
   "Use when costs are given at <b>two</b> volumes and a third is asked for. Compute the fixed element "
   "from <i>both</i> volumes as a free check.", "<b>13</b>"]],
 headcls="lite", widths=["44%", "42%", "14%"])}

<h2 class="sec" style="margin-top:6mm">Module 6 &mdash; Standard Costing</h2>
<p><b>Costs:</b> Standard &minus; Actual, so positive is <b>(F)</b> favourable. &nbsp;&nbsp;
<b>Sales:</b> Actual &minus; Budget, so positive is <b>(F)</b> favourable.</p>
{table(None, [("Family", ""), ("Variances", ""), ("Reconciliation", "")],
 [["<b>Material</b>",
   "<b>Cost</b> = (SQ &times; SP) &minus; (AQ &times; AP)<br/>"
   "<b>Price</b> = AQ &times; (SP &minus; AP)<br/>"
   "<b>Usage</b> = SP &times; (SQ &minus; AQ)<br/>"
   "<b>Mix</b> = SP &times; (RSQ &minus; AQ)<br/>"
   "<b>Yield</b> = SP &times; (SQ &minus; RSQ)",
   "MCV = MPV + MUV<br/>MUV = MMV + MYV<br/><br/>"
   "<span class='small'>RSQ = total actual quantity re-split in the <b>standard</b> mix. Its total "
   "must equal the AQ total.</span>"],
  ["<b>Labour</b>",
   "<b>Cost</b> = (SH &times; SR) &minus; (AH &times; AR)<br/>"
   "<b>Rate</b> = AH &times; (SR &minus; AR)<br/>"
   "<b>Efficiency</b> = SR &times; (SH &minus; AH)<br/>"
   "<b>Mix / gang</b> = SR &times; (RSH<sub>paid</sub> &minus; AH)<br/>"
   "<b>Yield</b> = SR &times; (SH &minus; RSH<sub>worked</sub>)<br/>"
   "<b>Idle time</b> = Idle hours &times; SR &nbsp;<i>always adverse</i>",
   "LCV = LRV + LEV<br/>LEV = LMV + LYV + LITV<br/><br/>"
   "<span class='small'>AH is hours <b>paid</b>. Hours worked = paid &minus; idle. Apportion idle "
   "hours on the <b>standard</b> composition.</span>"],
  ["<b>Variable overhead</b>",
   "<b>Cost</b> = (SH &times; SR) &minus; Actual VOH<br/>"
   "<b>Expenditure</b> = (AH &times; SR) &minus; Actual VOH<br/>"
   "<b>Efficiency</b> = SR &times; (SH &minus; AH)<br/>"
   "<b>Idle time</b> = Idle hours &times; SR",
   "VOCV = Expenditure + Efficiency<br/>(+ Idle time if given)<br/><br/>"
   "<span class='small'>Use <b>total</b> hours for expenditure and <b>productive</b> hours for "
   "efficiency.</span>"],
  ["<b>Fixed overhead</b>",
   "<b>Cost</b> = (SH &times; SR) &minus; Actual FOH<br/>"
   "<b>Expenditure</b> = Budgeted FOH &minus; Actual FOH<br/>"
   "<b>Volume</b> = SR &times; (SH &minus; BH)<br/>"
   "<b>Calendar</b> = SR &times; (RSH &minus; BH)<br/>"
   "<b>Capacity</b> = SR &times; (AH &minus; RSH)<br/>"
   "<b>Efficiency</b> = SR &times; (SH &minus; AH)",
   "FOCV = Expenditure + Volume<br/>Volume = Calendar + Capacity + Efficiency<br/><br/>"
   "<span class='small'>RSH = budgeted hours &times; " + frac("actual days", "budgeted days")
   + ". No days data means no calendar variance.</span>"],
  ["<b>Sales value</b>",
   "<b>Total</b> = Actual value &minus; Budgeted value<br/>"
   "<b>Price</b> = AQ &times; (AP &minus; SP)<br/>"
   "<b>Volume</b> = SP &times; (AQ &minus; BQ)<br/>"
   "<b>Mix</b> = SP &times; (AQ &minus; RBQ)<br/>"
   "<b>Quantity</b> = SP &times; (RBQ &minus; BQ)",
   "Total = Price + Volume<br/>Volume = Mix + Quantity<br/><br/>"
   "<span class='small'>RBQ = total actual quantity re-split in the <b>budgeted</b> mix.</span>"],
  ["<b>Sales margin</b>",
   "Replace every selling price above with the <b>margin per unit</b>:<br/>"
   "Standard margin = SP &minus; standard cost<br/>"
   "Actual margin = AP &minus; <b>standard</b> cost",
   "Total = Margin price + Margin volume<br/>Margin volume = Margin mix + Margin quantity<br/><br/>"
   "<span class='small'>Standard cost is used in both, so factory efficiency stays out of the sales "
   "analysis.</span>"]],
 headcls="lite", widths=["13%", "45%", "42%"])}

<div class="blk why" style="margin-top:5mm"><span class="lab">The one line that links all six modules</span>
{fml("Contribution &nbsp;=&nbsp; Sales &nbsp;&minus;&nbsp; Variable cost",
     "Module 2 defines it. Module 3 uses it to choose between alternatives. Module 4 strips it down to "
     "the costs that actually change. Module 5 forecasts it. Module 6 measures how far the actual "
     "outcome fell short of it. Master this one idea and the syllabus becomes a single subject rather "
     "than six.")}
</div>
"""
    return module_opener("Reference", "Master formula sheet",
                         "All six modules, four pages", body)


def build():
    return cover() + how_to_read() + formula_sheet()
