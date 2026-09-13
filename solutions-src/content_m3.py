# -*- coding: utf-8 -*-
"""MODULE 3 - COST-VOLUME-PROFIT ANALYSIS / DECISION MAKING  (18 problems)"""
from build import (esc, rs, money, frac, prob_head, question, read, method, wn,
                   trap, why, steps, bullets, fml, calc, ans, table, src,
                   arrow_panel, module_opener)

R = "&#8377;"
D = "$"


def stmt(caption, cols, rows, note=None):
    head = [("Particulars", "")] + [(c, "r") for c in cols]
    body = []
    for r in rows:
        cls = r[2] if len(r) > 2 else ""
        body.append({"cls": cls, "cells": [r[0]] + [(v, "r") for v in r[1]]})
    t = table(caption, head, body)
    if note:
        t += f"<div class='small'>{note}</div>"
    return t


# ----------------------------------------------------------------------
# break-even chart helper
# ----------------------------------------------------------------------
def be_chart(w, h, xmax, ymax, fc, vc_rate, sp_rate, xlabel, ylabel,
             bep_x, bep_y, caption, extra_line=None, extra_label=None):
    """Draw a proper break-even chart in SVG."""
    # Rr must be wide enough to hold the line labels in the right margin,
    # otherwise "Sales" / "Sales at Rs.18" clip against the frame and collide.
    L, B, T, Rr = 52, 34, 14, 56
    pw, ph = w - L - Rr, h - B - T

    def X(v): return L + (v / xmax) * pw
    def Y(v): return T + ph - (v / ymax) * ph

    s = [f'<div class="dia"><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
         'xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans">']
    # grid
    for i in range(1, 6):
        gy = T + ph * i / 5
        s.append(f'<line x1="{L}" y1="{gy:.1f}" x2="{L+pw}" y2="{gy:.1f}" stroke="#e4e4e4" '
                 'stroke-width="0.6"/>')
        s.append(f'<text x="{L-4}" y="{gy+2.6:.1f}" font-size="6.6" fill="#777" '
                 f'text-anchor="end">{int(ymax*(5-i)/5):,}</text>')
    s.append(f'<text x="{L-4}" y="{T+2.6}" font-size="6.6" fill="#777" text-anchor="end">'
             f'{int(ymax):,}</text>')
    for i in range(1, 6):
        gx = L + pw * i / 5
        s.append(f'<text x="{gx:.1f}" y="{T+ph+11}" font-size="6.6" fill="#777" '
                 f'text-anchor="middle">{int(xmax*i/5):,}</text>')
    # axes
    s.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{T+ph}" stroke="#333" stroke-width="1"/>')
    s.append(f'<line x1="{L}" y1="{T+ph}" x2="{L+pw}" y2="{T+ph}" stroke="#333" stroke-width="1"/>')
    # fixed cost line
    s.append(f'<line x1="{L}" y1="{Y(fc):.1f}" x2="{L+pw}" y2="{Y(fc):.1f}" stroke="#8a6d3b" '
             'stroke-width="1.2" stroke-dasharray="4,2"/>')
    s.append(f'<text x="{L+pw+4}" y="{Y(fc)+2.4:.1f}" font-size="6.8" fill="#8a6d3b" '
             'text-anchor="start">Fixed cost</text>')
    # total cost line
    s.append(f'<line x1="{L}" y1="{Y(fc):.1f}" x2="{L+pw}" y2="{Y(fc+vc_rate*xmax):.1f}" '
             'stroke="#c0392b" stroke-width="1.5"/>')
    s.append(f'<text x="{L+pw+4}" y="{Y(fc+vc_rate*xmax)+2.4:.1f}" font-size="6.8" fill="#c0392b" '
             'text-anchor="start">Total cost</text>')
    # sales line
    s.append(f'<line x1="{L}" y1="{Y(0):.1f}" x2="{L+pw}" y2="{Y(sp_rate*xmax):.1f}" '
             'stroke="#14837a" stroke-width="1.5"/>')
    s.append(f'<text x="{L+pw+4}" y="{Y(sp_rate*xmax)+2.4:.1f}" font-size="6.8" fill="#14837a" '
             'text-anchor="start">Sales</text>')
    if extra_line:
        s.append(f'<line x1="{L}" y1="{Y(0):.1f}" x2="{L+pw}" y2="{Y(extra_line*xmax):.1f}" '
                 'stroke="#5b4a9e" stroke-width="1.2" stroke-dasharray="3,2"/>')
        s.append(f'<text x="{L+pw+4}" y="{Y(extra_line*xmax)+2.4:.1f}" font-size="6.6" '
                 f'fill="#5b4a9e" text-anchor="start">{extra_label}</text>')
    # BEP marker
    s.append(f'<circle cx="{X(bep_x):.1f}" cy="{Y(bep_y):.1f}" r="3.4" fill="none" '
             'stroke="#10314f" stroke-width="1.6"/>')
    s.append(f'<line x1="{X(bep_x):.1f}" y1="{Y(bep_y):.1f}" x2="{X(bep_x):.1f}" '
             f'y2="{T+ph}" stroke="#10314f" stroke-width="0.7" stroke-dasharray="2,2"/>')
    s.append(f'<line x1="{L}" y1="{Y(bep_y):.1f}" x2="{X(bep_x):.1f}" y2="{Y(bep_y):.1f}" '
             'stroke="#10314f" stroke-width="0.7" stroke-dasharray="2,2"/>')
    s.append(f'<text x="{X(bep_x)+6:.1f}" y="{Y(bep_y)-6:.1f}" font-size="7.4" fill="#10314f" '
             'font-weight="bold">BEP</text>')
    # region labels -- placed at the vertical midpoint of each wedge, so they can
    # never drift onto a line or outside the shaded area
    def wedge(frac_x):
        xv = frac_x * xmax
        return X(xv), (Y(sp_rate * xv) + Y(fc + vc_rate * xv)) / 2 + 2.4

    lx, ly = wedge((bep_x / xmax) * 0.45)
    s.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="7" fill="#c0392b" '
             'text-anchor="middle">LOSS</text>')
    px, py = wedge((bep_x / xmax) + (1 - bep_x / xmax) * 0.55)
    s.append(f'<text x="{px:.1f}" y="{py:.1f}" font-size="7" fill="#1e7a37" '
             'text-anchor="middle">PROFIT</text>')
    # axis titles
    s.append(f'<text x="{L+pw/2:.1f}" y="{h-4}" font-size="7.2" fill="#333" '
             f'text-anchor="middle">{xlabel}</text>')
    s.append(f'<text x="12" y="{T+ph/2:.1f}" font-size="7.2" fill="#333" text-anchor="middle" '
             f'transform="rotate(-90 12 {T+ph/2:.1f})">{ylabel}</text>')
    s.append("</svg>")
    s.append(f'<div class="cap">{caption}</div></div>')
    return "".join(s)


# ======================================================================
def opener():
    intro = f"""
<h2 class="sec">What Module 3 is really about</h2>
<p>Module 2 taught you the formulas. Module 3 asks you to <b>make a decision</b> with them. Almost
every problem here is a manager saying &ldquo;should I do this or not?&rdquo;, and your job is to
answer with a number and a recommendation.</p>

<div class="blk read"><span class="lab">The single rule that decides every problem in this module</span>
{fml("Ignore fixed cost. Compare CONTRIBUTION.",
     "Fixed cost is going to be incurred whether you accept the order or not, so it cannot help you "
     "choose. Only the amounts that CHANGE between the alternatives matter. In this module that is "
     "almost always contribution.")}
<p>There are only two exceptions, and both are flagged where they arise:</p>
{bullets([
 '<b>When fixed cost itself changes</b> because of the decision &mdash; new machinery, an extra sales '
 'office, a shut-down saving. Then the change in fixed cost is relevant and must be brought in.',
 '<b>When capacity runs out.</b> Then you are not choosing whether to produce, but WHAT to produce, '
 'and the answer is contribution per unit of the scarce resource &mdash; not contribution per unit '
 'of product.'])}
</div>

<h2 class="sec" style="margin-top:6mm">The four decision types &mdash; recognise which one you are in</h2>
{table(None, [("Type",""),("The question sounds like &hellip;",""),("What you compare",""),
              ("Problems","c")],
 [["<b>1. Special order<br/>&amp; pricing</b>",
   "&ldquo;An export order at a reduced price &hellip; should we accept?&rdquo; "
   "&ldquo;What minimum price?&rdquo;",
   "Extra contribution from the order against any extra fixed cost it causes. "
   "<b>Spare capacity is the key condition.</b>",
   "<b>1, 2, 4, 5, 6, 11</b>"],
  ["<b>2. Make or buy</b>",
   "&ldquo;It costs us " + R + "6.25 to make; the market price is " + R + "4.85.&rdquo;",
   "The <b>variable</b> cost of making against the buying price. Fixed cost continues either way, "
   "so exclude it.",
   "<b>3</b>"],
  ["<b>3. Key factor /<br/>product mix</b>",
   "&ldquo;Material is restricted to 18,400 kg&rdquo; &nbsp;&ldquo;the limiting factor is "
   "labour&rdquo;",
   "<b>Contribution per unit of the limiting factor</b>, then rank and allocate.",
   "<b>7, 8, 9, 10</b>"],
  ["<b>4. Shut-down</b>",
   "&ldquo;Management plans to shut down the plant &hellip; should it?&rdquo;",
   "Loss if you continue against loss if you shut. Shut only if the shut-down loss is smaller.",
   "<b>12, 13, 14</b>"],
  ["<b>5. Charts</b>",
   "&ldquo;Draw the break-even chart&rdquo; &nbsp;&ldquo;draw the profit-volume graph&rdquo;",
   "Nothing &mdash; but you must plot correctly and read the BEP off the graph, then verify by "
   "calculation.",
   "<b>15&ndash;18</b>"]],
 headcls="lite", widths=["15%","30%","40%","15%"])}

<div class="blk method"><span class="lab">How to answer ANY decision question and not lose marks</span>
{steps([
 "<b>Separate fixed from variable</b> in whatever the question gives you. Nothing can start until "
 "this is done.",
 "<b>Find the contribution per unit</b> &mdash; selling price minus <i>all</i> variable costs "
 "including variable selling expenses.",
 "<b>Check the capacity.</b> Is there spare capacity for the new order, or must something be given "
 "up? This single check changes the whole answer.",
 "<b>Build a comparative statement</b> with one column per alternative, including the present "
 "position as a column. Never answer a decision question with loose calculations.",
 "<b>Write the recommendation in words</b>, with the amount. &ldquo;Accept the order, as it increases "
 "profit by " + R + "24,000.&rdquo; The sentence carries marks of its own.",
 "<b>Mention the non-financial point</b> if there is an obvious one &mdash; effect on the existing "
 "market, reliability of the supplier, the workforce. One line is enough and it is often the "
 "difference between a good answer and a full-mark one."])}
</div>
"""
    return module_opener("Module Three", "Cost&ndash;Volume&ndash;Profit Analysis",
                         "18 problems &nbsp;&middot;&nbsp; workbook pages 31 to 37", intro)


# ======================================================================
# Q1
# ======================================================================
def q1():
    q = f"""<p>A manufacturer makes an average profit of {R}2.5 on a selling price of {R}14.5. He
produces and sells 60,000 units at 60% capacity. His cost of sales per unit is: Direct Materials
{R}4; Direct Wages {R}1; Factory overheads (Variable) {R}3; Selling overheads (Variable) 25 paise.
Total fixed cost {R}2,25,000.</p>
<p>During the current year he anticipates that (a) fixed cost will increase by 10% and
(b) material and labour cost will increase by 5% each. Under these circumstances he obtains an offer
for a further 20% utilisation of his capacity. What minimum price would you recommend to accept the
offer so as to ensure an overall profit of {R}1,60,000?</p>"""

    rd = f"""{bullets([
 '<b>Verify the given data first.</b> Variable cost = 4 + 1 + 3 + 0.25 = ' + R + '8.25; fixed per '
 'unit = 2,25,000 &divide; 60,000 = ' + R + '3.75; total ' + R + '12.00; profit = 14.50 &minus; '
 '12.00 = ' + R + '2.50 &#10003;. That tie-up proves you have read the question correctly.',
 '<b>60,000 units is 60% capacity</b>, so 100% = 1,00,000 units and the further 20% = '
 '<b>20,000 units</b>.',
 'The two cost increases apply to <b>everything</b>, existing units as well as the new order.',
 'This is a <b>working-backwards</b> problem: the profit is given and the price is unknown. So build '
 'the required total contribution first, take away what the existing 60,000 units provide, and '
 'whatever is left must come from the 20,000 new units.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Revised variable cost per unit</h4>
{table(None, [("Element",""),("Present " + R,"r"),("Change",""),("Revised " + R,"r")],
 [["Direct materials","4.00","+5%","4.20"],
  ["Direct wages","1.00","+5%","1.05"],
  ["Factory overheads (variable)","3.00","no change","3.00"],
  ["Selling overheads (variable)","0.25","no change","0.25"],
  {"cls":"tot","cells":["<b>Variable cost per unit</b>","<b>8.25</b>","","<b>8.50</b>"]}],
 headcls="lite")}

<h4 class="mini">W2 &nbsp;Revised fixed cost and capacity</h4>
{calc([f'Revised fixed cost &nbsp;=&nbsp; 2,25,000 + 10% &nbsp;=&nbsp; <b>{R}2,47,500</b>',
       '60,000 units = 60% capacity &nbsp;&rarr;&nbsp; 100% = 1,00,000 units',
       'Further 20% of capacity &nbsp;=&nbsp; <b>20,000 units</b>'])}

<h4 class="mini">W3 &nbsp;Working backwards to the minimum price</h4>
{calc([f'Required profit &nbsp;=&nbsp; 1,60,000',
       f'Add: Revised fixed cost &nbsp;=&nbsp; 2,47,500',
       f'<b>Total contribution required &nbsp;=&nbsp; {R}4,07,500</b>',
       'Less: Contribution from existing 60,000 units &nbsp;=&nbsp; 60,000 &times; '
       f'(14.50 &minus; 8.50) &nbsp;=&nbsp; 60,000 &times; 6 &nbsp;=&nbsp; (3,60,000)',
       f'<b>Contribution needed from the new 20,000 units &nbsp;=&nbsp; {R}47,500</b>'])}
{fml("Contribution per unit on the offer &nbsp;=&nbsp; " + frac("47,500", "20,000")
     + f" &nbsp;=&nbsp; {R}2.375")}
{fml("Minimum price &nbsp;=&nbsp; Variable cost + Required contribution &nbsp;=&nbsp; "
     f"8.50 + 2.375 &nbsp;=&nbsp; <b>{R}10.875 per unit</b>",
     "Round up to " + R + "10.88 in practice &mdash; rounding down would leave the profit target "
     "just short.")}"""

    proof = stmt("Proof &mdash; profit statement at the recommended price",
      ["Amount " + R],
      [("Sales &mdash; existing 60,000 &times; " + R + "14.50", ["8,70,000"]),
       ("Sales &mdash; offer 20,000 &times; " + R + "10.875", ["2,17,500"]),
       ("<b>Total sales</b>", ["<b>10,87,500</b>"], "sub"),
       ("<i>Less:</i> Variable cost 80,000 &times; " + R + "8.50", ["(6,80,000)"]),
       ("<b>Contribution</b>", ["<b>4,07,500</b>"], "sub"),
       ("<i>Less:</i> Fixed cost (revised)", ["(2,47,500)"]),
       ("<b>Profit</b> &nbsp;<span class='src' style='display:inline'>exactly the target "
        "&#10003;</span>", ["<b>1,60,000</b>"], "tot")])

    return ("<div class='prob long'>"
            + prob_head("Q1", "Minimum price for a special order",
                        "Special order &middot; p.31")
            + question(q) + read(rd) + wn(wnh) + proof
            + trap(bullets([
                'Applying the 5% increase only to the new order. The cost rise affects the whole '
                'year&rsquo;s production.',
                'Increasing the factory and selling overheads by 5% too. The question says '
                '<b>material and labour</b> only.',
                f'Adding the old fixed cost per unit of {R}3.75 to the minimum price. The fixed cost '
                'is already covered by the existing 60,000 units, which is why the offer can be '
                f'accepted at {R}10.875 &mdash; far below the normal {R}14.50 &mdash; and still '
                'increase profit.']))
            + ans([("Revised variable cost per unit", f"{R} 8.50"),
                   ("Revised fixed cost", f"{R} 2,47,500"),
                   ("Units in the offer (20% of capacity)", "20,000"),
                   ("Total contribution required", f"{R} 4,07,500"),
                   ("Contribution needed per offer unit", f"{R} 2.375"),
                   ("<b>Minimum price recommended</b>", f"<b>{R} 10.875 (say {R} 10.88) per unit</b>")])
            + "</div>")


# ======================================================================
# Q2
# ======================================================================
def q2():
    q = f"""<p>ABC Company produces a single product sold at {R}75 per unit. Present production and
sale is 40,000 units per month, representing 50% of capacity. Variable cost per unit {R}50; fixed
costs per month {R}10 lakhs. Three proposals are on hand:</p>
<p><b>I.</b> Accept an export supply order for 30,000 units per month at a reduced price of {R}60 per
unit, incurring an additional variable cost of {R}5 per unit towards export packing, duties etc.<br/>
<b>II.</b> Increase domestic market sales by selling to a domestic chain store 30,000 units at {R}55
per unit, retaining the existing sales at the existing price.<br/>
<b>III.</b> Reduce the selling price for increased domestic sale as advised by the sales
department:</p>
{table(None, [("Reduce selling price per unit (" + R + ")","r"),
              ("Increase in sales expected (units)","r")],
 [["5","10,000"],["8","30,000"],["11","35,000"]], headcls="lite")}
<p>Prepare a table to present the results of the above proposals and give your comments and advice.</p>"""

    rd = f"""{bullets([
 '<b>Capacity check first.</b> 40,000 units = 50%, so 100% = 80,000 units per month and there are '
 '<b>40,000 units of spare capacity</b>. Every proposal must be tested against this ceiling.',
 '<b>The present position is break-even.</b> Contribution 40,000 &times; 25 = ' + R + '10,00,000, '
 'which exactly equals the fixed cost. Profit is nil. Say this in your answer &mdash; it explains '
 'why the management is looking at proposals at all.',
 '<b>Proposals I and II add sales without touching the existing price.</b> So compute only the extra '
 'contribution and add it to the present profit of nil.',
 '<b>Proposal III cuts the price on ALL units</b>, existing and new. That is the crucial difference '
 '&mdash; you must recompute the whole contribution, not just the increment. Most students get this '
 'wrong.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Present position and capacity</h4>
{calc([f'Contribution per unit &nbsp;=&nbsp; 75 &minus; 50 &nbsp;=&nbsp; <b>{R}25</b>',
       f'Present contribution &nbsp;=&nbsp; 40,000 &times; 25 &nbsp;=&nbsp; {R}10,00,000',
       f'Less fixed cost &nbsp;=&nbsp; (10,00,000) &nbsp;&rarr;&nbsp; <b>present profit = NIL '
       '(break-even)</b>',
       '40,000 units = 50% capacity &nbsp;&rarr;&nbsp; 100% = 80,000 units; '
       '<b>spare capacity 40,000 units</b>'])}

<h4 class="mini">W2 &nbsp;Proposal III &mdash; the whole price is cut, so recompute everything</h4>
{table(None, [("Price cut " + R,"r"),("New selling price","r"),("Total units","r"),
              ("Contribution per unit","r"),("Total contribution","r"),("Within capacity?","c")],
 [["5","70","50,000","20","10,00,000","Yes"],
  ["8","67","70,000","17","11,90,000","Yes"],
  ["11","64","75,000","14","10,50,000","Yes"]], headcls="lite")}
<p class="small">Total units = 40,000 existing + the stated increase. Contribution per unit = new
price &minus; {R}50 variable cost.</p>"""

    big = table("Comparative Statement of the Present Position and All Proposals",
      [("Particulars", ""), ("Present", "r"), ("Proposal I<br/>(export)", "r"),
       ("Proposal II<br/>(chain store)", "r"), ("III &mdash; cut " + R + "5", "r"),
       ("III &mdash; cut " + R + "8", "r"), ("III &mdash; cut " + R + "11", "r")],
      [["Units sold", "40,000", "70,000", "70,000", "50,000", "70,000", "75,000"],
       ["Selling price on existing units", "75", "75", "75", "70", "67", "64"],
       ["Selling price on additional units", "&mdash;", "60", "55", "70", "67", "64"],
       {"cls": "sub", "cells": ["<b>Contribution &mdash; existing 40,000 units</b>", "10,00,000",
                                 "10,00,000", "10,00,000", "8,00,000", "6,80,000", "5,60,000"]},
       {"cls": "sub", "cells": ["<b>Contribution &mdash; additional units</b>", "&mdash;",
                                 "1,50,000", "1,50,000", "2,00,000", "5,10,000", "4,90,000"]},
       {"cls": "tot", "cells": ["<b>Total contribution</b>", "<b>10,00,000</b>", "<b>11,50,000</b>",
                                 "<b>11,50,000</b>", "<b>10,00,000</b>", "<b>11,90,000</b>",
                                 "<b>10,50,000</b>"]},
       ["<i>Less:</i> Fixed cost", "(10,00,000)", "(10,00,000)", "(10,00,000)", "(10,00,000)",
        "(10,00,000)", "(10,00,000)"],
       {"cls": "tot", "cells": ["<b>PROFIT</b>", "<b>Nil</b>", "<b>1,50,000</b>",
                                 "<b>1,50,000</b>", "<b>Nil</b>", "<b>1,90,000</b>",
                                 "<b>50,000</b>"]}])

    return ("<div class='prob long'>"
            + prob_head("Q2", "Five alternatives compared", "Special order &middot; p.31")
            + question(q) + read(rd) + wn(wnh) + big
            + why(f"""<p><b>Advice: accept Proposal III with a price reduction of {R}8, giving a
profit of {R}1,90,000 per month.</b> It is the best of the six columns.</p>
<p>Two things are worth commenting on, and both earn marks:</p>
<ul class="tight">
<li><b>Proposals I and II give identical profit</b> of {R}1,50,000. The export order sells at {R}60
but carries {R}5 of extra cost; the chain store sells at {R}55 with no extra cost. Both leave a
contribution of {R}5 per unit. On financial grounds there is nothing to choose &mdash; so decide on
non-financial grounds. The export order does not disturb the home market, whereas selling to a
domestic chain at {R}55 risks existing customers demanding the same price. <b>On that basis
Proposal I is safer than Proposal II.</b></li>
<li><b>Cutting the price by {R}11 is worse than cutting it by {R}8</b>, even though it sells 5,000
more units. The extra volume does not make up for the contribution given away on all 75,000 units.
This is the danger of chasing volume through price cuts.</li>
</ul>""")
            + trap(bullets([
                'Treating Proposal III as an <i>increment</i> and adding only the new '
                'units&rsquo; contribution. The price cut applies to the existing 40,000 units too, '
                'which is why the ' + R + '5 cut leaves profit at nil rather than improving it.',
                'Forgetting to check capacity. All the options here fit inside 80,000 units, but had '
                'any exceeded it you would have had to turn away domestic sales &mdash; a completely '
                'different calculation.']))
            + ans([("Contribution per unit (present)", f"{R} 25"),
                   ("Present profit", "Nil &mdash; the company is at break-even"),
                   ("Proposal I &mdash; export at " + R + "60", f"Profit {R} 1,50,000"),
                   ("Proposal II &mdash; chain store at " + R + "55", f"Profit {R} 1,50,000"),
                   ("Proposal III &mdash; cut " + R + "5 / " + R + "8 / " + R + "11",
                    f"Nil / <b>{R} 1,90,000</b> / {R} 50,000"),
                   ("<b>Recommendation</b>",
                    f"<b>Proposal III with an {R} 8 cut &mdash; profit {R} 1,90,000</b>")])
            + "</div>")


# ======================================================================
# Q3
# ======================================================================
def q3():
    q = f"""<p>A radio manufacturing company finds that while it costs {R}6.25 to make each component
X 2730, the same is available in the market at {R}4.85 each, with an assurance of continued supply.
The breakdown of cost is: Materials {R}2.75 each; Labour {R}1.75 each; Other variables {R}0.50 each;
Depreciation and other fixed costs {R}1.25 each &mdash; total {R}6.25 each.</p>
<p><b>(a)</b> Should you make or buy? <b>(b)</b> What would be your decision if the supplier offered
the component at {R}5.85 each?</p>"""

    rd = f"""{bullets([
 'The whole problem turns on one question: <b>which costs disappear if you stop making?</b>',
 'Materials, labour and other variables disappear &mdash; they are only incurred when you make. '
 '<b>Depreciation and other fixed costs do not.</b> The machine still depreciates whether you use it '
 'or not.',
 'So the relevant cost of making is 2.75 + 1.75 + 0.50 = <b>' + R + '5.00</b>, not ' + R + '6.25. '
 'Comparing 6.25 with the market price is the trap the question is built around.'])}"""

    cmpt = table("Relevant cost comparison",
      [("Particulars", ""), ("Per component " + R, "r"), ("Relevant?", "")],
      [["Materials", "2.75", "<b>Yes</b> &mdash; avoided if bought"],
       ["Labour", "1.75", "<b>Yes</b> &mdash; avoided if bought"],
       ["Other variables", "0.50", "<b>Yes</b> &mdash; avoided if bought"],
       {"cls": "tot", "cells": ["<b>Relevant (marginal) cost of making</b>", "<b>5.00</b>", ""]},
       ["Depreciation and other fixed costs", "1.25",
        "<b>No</b> &mdash; incurred anyway, so it is irrelevant to the decision"],
       {"cls": "sub", "cells": ["Total cost as shown in the books", "6.25",
                                 "&mdash; misleading for this decision"]}])

    dec = table("The decision under each supplier price",
      [("", ""), ("(a) Supplier at " + R + "4.85", "r"), ("(b) Supplier at " + R + "5.85", "r")],
      [["Relevant cost of making", "5.00", "5.00"],
       ["Cost of buying", "4.85", "5.85"],
       {"cls": "tot", "cells": ["<b>Saving by buying / (by making)</b>", "<b>0.15 by buying</b>",
                                 "<b>(0.85) &mdash; make instead</b>"]},
       {"cls": "sub", "cells": ["<b>Decision</b>", "<b>BUY</b>", "<b>MAKE</b>"]}])

    return ("<div class='prob'>"
            + prob_head("Q3", "Make or buy", "Make or buy &middot; p.32")
            + question(q) + read(rd) + cmpt + dec
            + why(f"""<p><b>(a) Buy.</b> At {R}4.85 the supplier is cheaper than the {R}5.00 it costs
in avoidable terms, so buying saves {R}0.15 per component.</p>
<p><b>(b) Make.</b> At {R}5.85 the supplier is dearer than {R}5.00, so making saves {R}0.85 per
component. Note that the company should <i>still make</i> even though the book cost of {R}6.25 looks
higher than {R}5.85 &mdash; because {R}1.25 of that book cost will be incurred whether the component
is made or not.</p>
<p><b>Non-financial points worth one line:</b> the question mentions &ldquo;an assurance of continued
supply&rdquo;, which removes the usual worry about depending on an outside supplier. Against that,
buying leaves the company&rsquo;s own capacity idle &mdash; if that freed capacity can be used for
something else, its contribution should be added to the case for buying.</p>""")
            + ans([("Relevant (avoidable) cost of making", f"{R} 5.00 per component"),
                   ("Irrelevant fixed cost excluded", f"{R} 1.25 per component"),
                   ("<b>(a) At {} 4.85</b>".format(R),
                    f"<b>BUY</b> &mdash; saves {R} 0.15 per component"),
                   ("<b>(b) At {} 5.85</b>".format(R),
                    f"<b>MAKE</b> &mdash; saves {R} 0.85 per component")])
            + "</div>")


# ======================================================================
# Q4
# ======================================================================
def q4():
    q = f"""<p>Indo-British Company has capacity to produce 5,000 articles but actually produces only
2,000 articles for the home market at the following costs: Materials {R}40,000; Wages {R}36,000;
Factory overheads &mdash; Fixed {R}12,000, Variable {R}20,000; Administration overhead &mdash; Fixed
{R}18,000; Selling and Distribution overheads &mdash; Fixed {R}10,000, Variable {R}16,000. Total cost
{R}1,52,000.</p>
<p>The home market can consume only 2,000 articles at a selling price of {R}80 per article. An
additional order for the supply of 3,000 articles is received from a foreign country at {R}65 per
article. Should this order be accepted or not, if execution of this order entails an additional
packing cost of {R}3,000?</p>"""

    rd = f"""{bullets([
 '<b>Split the costs.</b> Variable: materials 40,000 + wages 36,000 + factory variable 20,000 + '
 'selling variable 16,000 = ' + R + '1,12,000 for 2,000 units, i.e. <b>' + R + '56 per unit</b>. '
 'Fixed: 12,000 + 18,000 + 10,000 = <b>' + R + '40,000</b>.',
 '<b>Capacity is exactly right.</b> 2,000 + 3,000 = 5,000 = full capacity. So no domestic sales have '
 'to be sacrificed &mdash; the order uses idle capacity only.',
 'Because fixed cost is already fully covered by the home market, the only test is whether the '
 f'{R}65 price beats the {R}56 variable cost plus the {R}3,000 packing cost.',
 'The packing cost of ' + R + '3,000 is a <b>lump sum specific to this order</b>, so it is relevant '
 'even though it is not a per-unit cost.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Splitting the present cost</h4>
{table(None, [("Element",""),("Total " + R,"r"),("Nature",""),("Per unit " + R,"r")],
 [["Materials","40,000","Variable","20"],["Wages","36,000","Variable","18"],
  ["Factory overheads &mdash; variable","20,000","Variable","10"],
  ["Selling and distribution &mdash; variable","16,000","Variable","8"],
  {"cls":"tot","cells":["<b>Total variable cost (2,000 units)</b>","<b>1,12,000</b>","",
                        "<b>56</b>"]},
  ["Factory overheads &mdash; fixed","12,000","Fixed","&mdash;"],
  ["Administration overhead &mdash; fixed","18,000","Fixed","&mdash;"],
  ["Selling and distribution &mdash; fixed","10,000","Fixed","&mdash;"],
  {"cls":"tot","cells":["<b>Total fixed cost</b>","<b>40,000</b>","","&mdash;"]},
  {"cls":"sub","cells":["<b>Total cost</b>","<b>1,52,000</b>","","<b>76</b>"]}],
 headcls="lite")}"""

    cmp2 = stmt("Comparative Statement of Profitability",
      ["Present<br/>2,000 units " + R, "Foreign order<br/>3,000 units " + R,
       "Total<br/>5,000 units " + R],
      [("Sales &nbsp;<span class='src' style='display:inline'>2,000&times;80 &nbsp;|&nbsp; "
        "3,000&times;65</span>", ["1,60,000", "1,95,000", "3,55,000"]),
       ("<i>Less:</i> Variable cost at " + R + "56 per unit", ["(1,12,000)", "(1,68,000)",
                                                               "(2,80,000)"]),
       ("<i>Less:</i> Additional packing cost", ["&mdash;", "(3,000)", "(3,000)"]),
       ("<b>Contribution</b>", ["<b>48,000</b>", "<b>24,000</b>", "<b>72,000</b>"], "sub"),
       ("<i>Less:</i> Fixed cost &nbsp;<span class='src' style='display:inline'>unchanged &mdash; "
        "already borne by the home market</span>", ["(40,000)", "&mdash;", "(40,000)"]),
       ("<b>PROFIT</b>", ["<b>8,000</b>", "<b>24,000</b>", "<b>32,000</b>"], "tot")])

    return ("<div class='prob long'>"
            + prob_head("Q4", "Foreign order using idle capacity",
                        "Special order &middot; p.32")
            + question(q) + read(rd) + wn(wnh) + cmp2
            + why(f"""<p><b>Accept the order.</b> It adds {R}24,000 of contribution and, because the
fixed cost of {R}40,000 is already fully recovered from the home market, the whole of that {R}24,000
drops straight into profit. Profit rises from {R}8,000 to {R}32,000 &mdash; a fourfold increase.</p>
<p>Notice that the order price of {R}65 is <b>below the full cost of {R}76 per unit</b>. A student who
compares 65 with 76 will reject the order and lose the entire question. The correct comparison is 65
against the {R}56 variable cost plus the {R}1 per unit of packing.</p>
<p><b>One non-financial line:</b> the order is from a foreign country, so it does not undercut the
home market where the price stays at {R}80. That is what makes accepting it safe.</p>""")
            + ans([("Variable cost per unit", f"{R} 56"),
                   ("Total fixed cost", f"{R} 40,000"),
                   ("Contribution from the order", f"{R} 1,95,000 &minus; {R} 1,71,000 = {R} 24,000"),
                   ("Present profit / profit after acceptance", f"{R} 8,000 / {R} 32,000"),
                   ("<b>Decision</b>", f"<b>ACCEPT &mdash; profit increases by {R} 24,000</b>")])
            + "</div>")



# ======================================================================
# Q5
# ======================================================================
def q5():
    q = f"""<p>A company currently operating at 80% capacity has the following particulars: Sales
{R}32,00,000; Direct materials {R}10,00,000; Direct labour {R}4,00,000; Variable overheads
{R}2,00,000; Fixed overheads {R}13,00,000.</p>
<p>An export order has been received that would utilise half the capacity of the factory. This order
cannot be split &mdash; it has to be taken in full and executed at 10% below the normal domestic
prices, or rejected totally. The alternatives available are:</p>
<p><b>(1)</b> Reject the order and continue with domestic sales only (as at present); or<br/>
<b>(2)</b> Accept the order, split capacity between overseas and domestic sales and turn away excess
domestic demand; or<br/>
<b>(3)</b> Increase capacity to accept the export order and maintain present domestic sales by
<b>(a)</b> buying equipment that will increase capacity, resulting in an increase of {R}1,00,000 in
fixed cost, or <b>(b)</b> increasing the normal wage rate by 1&frac12; times to increase output.</p>
<p>Prepare a comparative statement of profitability and suggest the best alternative.</p>"""

    rd = f"""{bullets([
 '<b>Scale everything to a per-1% basis first.</b> The figures are at 80% capacity, so divide by 80 '
 'to get the value of 1% and then build any level you need. Sales are ' + R + '40,000 per 1%; '
 'variable cost is ' + R + '20,000 per 1%.',
 '<b>The export order needs 50% of capacity</b> and cannot be split. Present domestic use is 80%. '
 'So 80 + 50 = 130% &mdash; more than the factory has. That conflict is the whole problem.',
 'Alternative 2 keeps total capacity at 80%: 50% export + only 30% domestic. You <b>give up</b> 50 '
 'percentage points of domestic sales.',
 'Alternative 3 runs at 130% by either buying equipment (extra fixed cost) or paying 1&frac12; times '
 'the wage rate on the extra output.',
 '<b>Fixed overhead of ' + R + '13,00,000 stays the same in alternatives 1, 2 and 3(b)</b> &mdash; only '
 '3(a) changes it.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Value of 1% of capacity</h4>
{table(None, [("Element",""),("At 80% capacity " + R,"r"),("Per 1% " + R,"r"),("At 50% " + R,"r"),
              ("At 30% " + R,"r")],
 [["Sales","32,00,000","40,000","20,00,000","12,00,000"],
  ["Direct materials","10,00,000","12,500","6,25,000","3,75,000"],
  ["Direct labour","4,00,000","5,000","2,50,000","1,50,000"],
  ["Variable overheads","2,00,000","2,500","1,25,000","75,000"],
  {"cls":"tot","cells":["<b>Total variable cost</b>","<b>16,00,000</b>","<b>20,000</b>",
                        "<b>10,00,000</b>","<b>6,00,000</b>"]},
  {"cls":"sub","cells":["<b>Contribution</b>","<b>16,00,000</b>","<b>20,000</b>",
                        "<b>10,00,000</b>","<b>6,00,000</b>"]}], headcls="lite")}

<h4 class="mini">W2 &nbsp;The export order at 50% capacity, priced 10% below normal</h4>
{calc([f'Sales at normal price &nbsp;=&nbsp; {R}20,00,000',
       f'Less 10% &nbsp;=&nbsp; <b>export sales value {R}18,00,000</b>',
       f'Variable cost at 50% &nbsp;=&nbsp; {R}10,00,000',
       f'<b>Export contribution &nbsp;=&nbsp; {R}8,00,000</b>'])}

<h4 class="mini">W3 &nbsp;Alternative 3(b) &mdash; wages at 1&frac12; times on the extra 50%</h4>
{calc([f'Direct materials at 50% &nbsp;=&nbsp; 6,25,000',
       f'Direct labour at 50% &times; 1.5 &nbsp;=&nbsp; 2,50,000 &times; 1.5 &nbsp;=&nbsp; 3,75,000',
       f'Variable overheads at 50% &nbsp;=&nbsp; 1,25,000',
       f'<b>Variable cost of the export order &nbsp;=&nbsp; {R}11,25,000</b>',
       f'Export contribution &nbsp;=&nbsp; 18,00,000 &minus; 11,25,000 &nbsp;=&nbsp; '
       f'<b>{R}6,75,000</b>'])}"""

    big = table("Comparative Statement of Profitability",
      [("Particulars", ""), ("Alt 1<br/>Reject", "r"), ("Alt 2<br/>Split 50+30", "r"),
       ("Alt 3(a)<br/>Buy equipment", "r"), ("Alt 3(b)<br/>Overtime wages", "r")],
      [{"cls": "sub", "cells": ["<b>Capacity used</b>", "80% domestic",
                                 "50% export<br/>30% domestic",
                                 "80% domestic<br/>50% export", "80% domestic<br/>50% export"]},
       ["Domestic sales", "32,00,000", "12,00,000", "32,00,000", "32,00,000"],
       ["Export sales &nbsp;<span class='src' style='display:inline'>W2</span>", "&mdash;",
        "18,00,000", "18,00,000", "18,00,000"],
       {"cls": "sub", "cells": ["<b>Total sales</b>", "<b>32,00,000</b>", "<b>30,00,000</b>",
                                 "<b>50,00,000</b>", "<b>50,00,000</b>"]},
       ["<i>Less:</i> Variable cost &mdash; domestic", "(16,00,000)", "(6,00,000)", "(16,00,000)",
        "(16,00,000)"],
       ["<i>Less:</i> Variable cost &mdash; export", "&mdash;", "(10,00,000)", "(10,00,000)",
        "(11,25,000)"],
       {"cls": "sub", "cells": ["<b>Total contribution</b>", "<b>16,00,000</b>", "<b>14,00,000</b>",
                                 "<b>24,00,000</b>", "<b>22,75,000</b>"]},
       ["<i>Less:</i> Fixed overheads", "(13,00,000)", "(13,00,000)", "(13,00,000)", "(13,00,000)"],
       ["<i>Less:</i> Additional fixed cost for equipment", "&mdash;", "&mdash;", "(1,00,000)",
        "&mdash;"],
       {"cls": "tot", "cells": ["<b>PROFIT</b>", "<b>3,00,000</b>", "<b>1,00,000</b>",
                                 "<b>10,00,000</b>", "<b>9,75,000</b>"]},
       {"cls": "sub", "cells": ["<b>Ranking</b>", "3rd", "4th &mdash; worst",
                                 "<b>1st &mdash; BEST</b>", "2nd"]}])

    return ("<div class='prob long'>"
            + prob_head("Q5", "Export order needing more capacity than exists",
                        "Special order &middot; p.32&ndash;33")
            + question(q) + read(rd) + wn(wnh) + big
            + why(f"""<p><b>Recommendation: Alternative 3(a) &mdash; buy the equipment and accept the
export order while keeping domestic sales at 80%. Profit {R}10,00,000.</b></p>
<ul class="tight">
<li><b>Alternative 2 is the worst of all</b>, at {R}1,00,000 &mdash; worse even than rejecting the
order. Giving up 50 percentage points of full-price domestic business to take on 50 points of
discounted export business destroys contribution. This is the trap the question is built around: an
export order at a discount is only worth having if it uses <b>spare</b> capacity.</li>
<li>3(a) beats 3(b) by {R}25,000 because the extra fixed cost of {R}1,00,000 is cheaper than the
{R}1,25,000 of extra wages. But note that 3(a) commits the company permanently while overtime can be
stopped &mdash; worth one sentence if the order is a one-off.</li>
</ul>""")
            + ans([("Value of 1% capacity &mdash; sales / variable cost", f"{R} 40,000 / {R} 20,000"),
                   ("Export contribution at normal wages", f"{R} 8,00,000"),
                   ("Alt 1 &mdash; reject", f"Profit {R} 3,00,000"),
                   ("Alt 2 &mdash; split capacity", f"Profit {R} 1,00,000 &mdash; worst"),
                   ("<b>Alt 3(a) &mdash; buy equipment</b>", f"<b>Profit {R} 10,00,000 &mdash; BEST</b>"),
                   ("Alt 3(b) &mdash; overtime at 1&frac12; times", f"Profit {R} 9,75,000")])
            + "</div>")


# ======================================================================
# Q6
# ======================================================================
def q6():
    q = f"""<p>Prestige Company Private Limited, manufacturing pressure cookers, has drawn up the
following budget for the year 20X5-X6: Raw materials {R}20,00,000; Labour, stores, power and other
variable costs {R}6,00,000; Manufacturing overheads (Fixed) {R}7,00,000; Variable distribution costs
{R}4,00,000; General overheads including selling (Fixed) {R}3,00,000 &mdash; total {R}40,00,000.
Income from sales {R}50,00,000; Budgeted profit {R}10,00,000.</p>
<p><b>The general manager</b> suggests reducing selling price by 5% and expects to achieve an
additional volume of 50%. There is sufficient manufacturing capacity. A more intensive manufacturing
programme will involve additional costs of {R}50,000 for production planning. It will also be
necessary to open an additional sales office at a cost of {R}1,00,000 per annum.</p>
<p><b>The sales manager</b> suggests increasing selling price by 10%, which is estimated to reduce
sales volume by 10%. At the same time, savings in manufacturing overheads and general overheads of
{R}50,000 and {R}1,00,000 per annum respectively are expected on this reduced volume.</p>
<p>Which of these two proposals would you accept and why?</p>"""

    rd = f"""{bullets([
 '<b>Split the budget into variable and fixed first.</b> Variable = raw materials 20,00,000 + labour '
 'and other variable 6,00,000 + variable distribution 4,00,000 = <b>' + R + '30,00,000</b>. '
 'Fixed = 7,00,000 + 3,00,000 = <b>' + R + '10,00,000</b>.',
 '<b>Handle volume and price separately.</b> Variable cost changes with <b>volume only</b>; sales '
 'value changes with <b>both</b> volume and price. Doing them in one step is where errors creep in.',
 'GM: volume &times;1.50 and price &times;0.95, so sales = 50,00,000 &times; 1.50 &times; 0.95. '
 'Variable cost = 30,00,000 &times; 1.50 (the price cut does not change costs).',
 'Sales manager: volume &times;0.90 and price &times;1.10, so sales = 50,00,000 &times; 0.90 &times; '
 '1.10. Variable cost = 30,00,000 &times; 0.90.',
 'Then adjust fixed cost: GM <b>adds</b> 1,50,000; sales manager <b>saves</b> 1,50,000.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Splitting the budget</h4>
{table(None, [("Element",""),("Amount " + R,"r"),("Nature","")],
 [["Raw materials","20,00,000","Variable"],
  ["Labour, stores, power and other variable costs","6,00,000","Variable"],
  ["Variable distribution costs","4,00,000","Variable"],
  {"cls":"tot","cells":["<b>Total variable cost</b>","<b>30,00,000</b>",""]},
  ["Manufacturing overheads","7,00,000","Fixed"],
  ["General overheads including selling","3,00,000","Fixed"],
  {"cls":"tot","cells":["<b>Total fixed cost</b>","<b>10,00,000</b>",""]}], headcls="lite")}
{calc([f'Budgeted contribution &nbsp;=&nbsp; 50,00,000 &minus; 30,00,000 &nbsp;=&nbsp; '
       f'{R}20,00,000 &nbsp;&rarr;&nbsp; P/V ratio <b>40%</b>',
       f'Budgeted profit &nbsp;=&nbsp; 20,00,000 &minus; 10,00,000 &nbsp;=&nbsp; {R}10,00,000 '
       '&#10003; agrees with the question'])}

<h4 class="mini">W2 &nbsp;Building each proposal</h4>
{calc(['<b>General manager:</b> sales &nbsp;=&nbsp; 50,00,000 &times; 1.50 &times; 0.95 '
       f'&nbsp;=&nbsp; <b>{R}71,25,000</b>',
       f'&nbsp;&nbsp;&nbsp;variable cost &nbsp;=&nbsp; 30,00,000 &times; 1.50 &nbsp;=&nbsp; '
       f'<b>{R}45,00,000</b>',
       f'&nbsp;&nbsp;&nbsp;fixed cost &nbsp;=&nbsp; 10,00,000 + 50,000 + 1,00,000 &nbsp;=&nbsp; '
       f'<b>{R}11,50,000</b>',
       '<b>Sales manager:</b> sales &nbsp;=&nbsp; 50,00,000 &times; 0.90 &times; 1.10 '
       f'&nbsp;=&nbsp; <b>{R}49,50,000</b>',
       f'&nbsp;&nbsp;&nbsp;variable cost &nbsp;=&nbsp; 30,00,000 &times; 0.90 &nbsp;=&nbsp; '
       f'<b>{R}27,00,000</b>',
       f'&nbsp;&nbsp;&nbsp;fixed cost &nbsp;=&nbsp; 10,00,000 &minus; 50,000 &minus; 1,00,000 '
       f'&nbsp;=&nbsp; <b>{R}8,50,000</b>'])}"""

    big = stmt("Comparative Statement of Profitability",
      ["Original budget " + R, "General manager " + R, "Sales manager " + R],
      [("Volume index", ["100%", "150%", "90%"], "sub"),
       ("Price index", ["100%", "95%", "110%"], "sub"),
       ("Sales", ["50,00,000", "71,25,000", "49,50,000"]),
       ("<i>Less:</i> Variable cost", ["(30,00,000)", "(45,00,000)", "(27,00,000)"]),
       ("<b>Contribution</b>", ["<b>20,00,000</b>", "<b>26,25,000</b>", "<b>22,50,000</b>"], "sub"),
       ("P/V ratio", ["40.00%", "36.84%", "45.45%"], "sub"),
       ("<i>Less:</i> Fixed cost", ["(10,00,000)", "(11,50,000)", "(8,50,000)"]),
       ("<b>PROFIT</b>", ["<b>10,00,000</b>", "<b>14,75,000</b>", "<b>14,00,000</b>"], "tot"),
       ("Increase over budget", ["&mdash;", "<b>+4,75,000</b>", "+4,00,000"], "sub")])

    return ("<div class='prob long'>"
            + prob_head("Q6", "Two rival proposals from two managers",
                        "Pricing decision &middot; p.33")
            + question(q) + read(rd) + wn(wnh) + big
            + why(f"""<p><b>Accept the general manager&rsquo;s proposal. It gives {R}14,75,000 against
the sales manager&rsquo;s {R}14,00,000 &mdash; {R}75,000 better, and {R}4,75,000 above the original
budget.</b></p>
<p>But the reasoning matters more than the {R}75,000, and a full-mark answer says so:</p>
<ul class="tight">
<li>The GM wins on <b>volume</b>: his P/V ratio actually <i>falls</i> from 40% to 36.84% because he
cut the price, yet 50% more volume more than makes up for it.</li>
<li>The sales manager wins on <b>margin</b>: his P/V ratio <i>rises</i> to 45.45% and he even saves
fixed cost &mdash; but on 10% less volume.</li>
<li><b>Risk cuts the other way.</b> The GM&rsquo;s plan depends on actually selling 50% more, which
is a large assumption, and it commits {R}1,50,000 of new fixed cost that cannot easily be reversed.
The sales manager&rsquo;s plan needs no extra spending and earns nearly as much. If you doubt the
50% volume increase, the sales manager&rsquo;s proposal is the safer choice &mdash; say so.</li>
</ul>""")
            + ans([("Variable cost / fixed cost in the budget",
                    f"{R} 30,00,000 / {R} 10,00,000"),
                   ("Budgeted P/V ratio", "40%"),
                   ("<b>General manager &mdash; profit</b>",
                    f"<b>{R} 14,75,000</b> (P/V 36.84%)"),
                   ("Sales manager &mdash; profit", f"{R} 14,00,000 (P/V 45.45%)"),
                   ("<b>Recommendation</b>",
                    f"<b>General manager&rsquo;s proposal &mdash; {R} 75,000 better</b>")])
            + "</div>")


# ======================================================================
# KEY FACTOR PLAYBOOK
# ======================================================================
def keyfactor_playbook():
    return f"""
<div class="modopen" style="page-break-before:always">
<div class="modopen-band" style="padding:22mm 18mm 12mm 18mm">
<div class="modopen-kicker">Module Three &middot; Playbook</div>
<div class="modopen-title" style="font-size:21pt">Key Factor and Product Mix</div>
<span class="modopen-count">Use these steps for Q7, Q8, Q9 and Q10</span>
</div>
<div class="modopen-body">

<div class="blk read"><span class="lab">The idea, and why the obvious answer is wrong</span>
<p>When something runs short &mdash; material, labour hours, machine hours &mdash; you cannot make
everything. You must choose. And the instinct is to make the product with the <b>highest
contribution per unit</b>.</p>
<p><b>That instinct is wrong.</b> If product A earns {R}30 of contribution but eats 15 labour hours,
while product B earns only {R}16 but needs just 2 hours, then in the 15 hours that one A takes you
could have made seven and a half B&rsquo;s and earned {R}120. B is four times better, even though its
contribution per unit is half.</p>
{fml("Rank by &nbsp; " + frac("Contribution per unit", "Units of the scarce resource per unit"),
     "This is called contribution per unit of key factor, or contribution per limiting factor. "
     "It is the entire topic in one line.")}
</div>

{arrow_panel(500, 116, [
  {"box": (10, 6, 148, 26, "1. Find contribution|per unit of each product", "#eaf5f4"), "fs": 7.6},
  {"box": (176, 6, 148, 26, "2. Identify the SCARCE|resource and how much|each product uses",
           "#fdf6e6"), "fs": 7.2},
  {"box": (342, 6, 148, 26, "3. Divide contribution|by resource used", "#eaf5f4"), "fs": 7.6},
  {"line": (158, 19, 174, 19)}, {"line": (324, 19, 340, 19)},
  {"box": (10, 48, 148, 26, "4. RANK &mdash; highest|per-resource first", "#e8eef4"), "fs": 7.6},
  {"box": (176, 48, 148, 26, "5. Allocate the resource|down the ranking", "#e8eef4"), "fs": 7.6},
  {"box": (342, 48, 148, 26, "6. Last product gets|whatever is left", "#e8eef4"), "fs": 7.6},
  {"line": (158, 61, 174, 61)}, {"line": (324, 61, 340, 61)},
  {"box": (10, 86, 480, 24, "7. Fixed cost does NOT change. Total contribution of the optimal mix "
           "minus the SAME fixed cost = profit.", "#eef7ee"), "fs": 8.0,
   "stroke": "#2c7a34", "fg": "#1f5b26"},
], "The six steps. Step 3 is the one that decides the answer; step 7 is the one students forget.")}

<div class="blk trap"><span class="lab">Three things to be careful about</span>
{bullets([
 '<b>Work out the resource per unit from the money figure.</b> If materials cost ' + R + '80 per unit '
 'at ' + R + '20 per kg, then the product uses 4 kg. Questions almost never give you the quantity '
 'directly.',
 '<b>Fixed cost stays the same in the optimal mix.</b> It was fixed before the shortage and it is '
 'fixed after. Do not recompute it per unit &mdash; carry the same total across.',
 '<b>Check whether demand also limits you.</b> You cannot make more of a product than can be sold, '
 'even if it ranks first. In Q8 and Q10 the budgeted quantity is the demand ceiling.'])}
</div>
</div></div>"""


# ======================================================================
# Q7
# ======================================================================
def q7():
    q = f"""<p>Present the following information to show to the management (a) the marginal product
cost and the contribution per unit and (b) the total contribution and profits resulting from each of
the following sales mixtures.</p>
{table(None, [("Particulars",""),("Product A","r"),("Product B","r")],
 [["Direct materials per unit", R + " 10", R + " 9"],
  ["Direct wages per unit", R + " 3", R + " 2"],
  ["Sales price per unit", R + " 20", R + " 15"]], headcls="lite")}
<p>Fixed expenses {R}800. Variable expenses are allocated to products as 100% of direct wages.</p>
<p>Sales mixtures: <b>(i)</b> 1,000 units of A and 2,000 units of B; <b>(ii)</b> 1,500 units of A and
1,500 units of B; <b>(iii)</b> 2,000 units of A and 1,000 units of B.</p>"""

    rd = f"""{bullets([
 '&ldquo;Variable expenses are 100% of direct wages&rdquo; means variable overhead = the same amount '
 'as wages: A gets ' + R + '3, B gets ' + R + '2. Add it as a third variable element.',
 'There is <b>no scarce resource here</b> &mdash; the total is 3,000 units in every mixture. So this '
 'is not a ranking problem; you simply evaluate three given mixes and pick the best.',
 'Because total units are the same in all three, the best mix is automatically the one with more of '
 'the <b>higher-contribution</b> product. A earns ' + R + '4 and B earns ' + R + '2, so expect '
 'mixture (iii) to win.'])}"""

    a = table("(a) Marginal cost and contribution per unit",
      [("Particulars", ""), ("Product A " + R, "r"), ("Product B " + R, "r")],
      [["Selling price", "20", "15"],
       ["<i>Less:</i> Direct materials", "(10)", "(9)"],
       ["<i>Less:</i> Direct wages", "(3)", "(2)"],
       ["<i>Less:</i> Variable expenses &nbsp;<span class='src' style='display:inline'>100% of "
        "direct wages</span>", "(3)", "(2)"],
       {"cls": "sub", "cells": ["<b>Marginal (variable) cost per unit</b>", "<b>16</b>",
                                 "<b>13</b>"]},
       {"cls": "tot", "cells": ["<b>Contribution per unit</b>", "<b>4</b>", "<b>2</b>"]},
       {"cls": "sub", "cells": ["P/V ratio", "20%", "13.33%"]}])

    b = table("(b) Total contribution and profit under each sales mixture",
      [("Particulars", ""), ("(i) 1,000 A + 2,000 B", "r"), ("(ii) 1,500 A + 1,500 B", "r"),
       ("(iii) 2,000 A + 1,000 B", "r")],
      [["Contribution from A &nbsp;<span class='src' style='display:inline'>units &times; " + R
        + "4</span>", "4,000", "6,000", "8,000"],
       ["Contribution from B &nbsp;<span class='src' style='display:inline'>units &times; " + R
        + "2</span>", "4,000", "3,000", "2,000"],
       {"cls": "sub", "cells": ["<b>Total contribution</b>", "<b>8,000</b>", "<b>9,000</b>",
                                 "<b>10,000</b>"]},
       ["<i>Less:</i> Fixed expenses", "(800)", "(800)", "(800)"],
       {"cls": "tot", "cells": ["<b>PROFIT</b>", "<b>7,200</b>", "<b>8,200</b>", "<b>9,200</b>"]},
       {"cls": "sub", "cells": ["<b>Ranking</b>", "3rd", "2nd", "<b>1st &mdash; BEST</b>"]}])

    return ("<div class='prob long'>"
            + prob_head("Q7", "Three sales mixtures compared", "Product mix &middot; p.33&ndash;34")
            + question(q) + read(rd) + a + b
            + why(f"""<p><b>Mixture (iii) is best, giving a profit of {R}9,200.</b></p>
<p>The reason is simple once you see it: all three mixes sell exactly 3,000 units, and A contributes
{R}4 against B&rsquo;s {R}2. So every unit of B swapped for a unit of A adds {R}2. Moving from
mixture (i) to (iii) swaps 1,000 units of B for 1,000 units of A and gains exactly
{R}2,000 &mdash; which is the difference between {R}7,200 and {R}9,200.</p>
<p><b>Recommendation:</b> sell as much of A as the market will absorb. The only reason to keep B in
the mix at all is if demand for A is limited to 2,000 units.</p>""")
            + ans([("Marginal cost per unit &mdash; A / B", f"{R} 16 / {R} 13"),
                   ("Contribution per unit &mdash; A / B", f"{R} 4 / {R} 2"),
                   ("(i) Contribution / profit", f"{R} 8,000 / {R} 7,200"),
                   ("(ii) Contribution / profit", f"{R} 9,000 / {R} 8,200"),
                   ("<b>(iii) Contribution / profit</b>",
                    f"<b>{R} 10,000 / {R} 9,200 &mdash; BEST</b>")])
            + "</div>")


# ======================================================================
# Q8
# ======================================================================
def q8():
    q = f"""<p>A company manufactures three products. The budgeted quantity, selling prices and unit
costs are as under:</p>
{table(None, [("Particulars",""),("A","r"),("B","r"),("C","r")],
 [["Raw materials (@ " + R + "20 per kg)","80","40","20"],
  ["Direct wages (@ " + R + "5 per hour)","5","15","10"],
  ["Variable overheads","10","30","20"],
  ["Fixed overheads","9","22","18"],
  ["Budgeted production (in units)","6,400","3,200","2,400"],
  ["Selling price per unit (" + R + ")","140","120","90"]], headcls="lite")}
<p><b>(i)</b> Present a statement of budgeted profit. <b>(ii)</b> Set the optimal product mix and
determine the profit if the supply of raw materials is restricted to 18,400 kgs.</p>"""

    rd = f"""{bullets([
 '<b>Convert the material cost into kilograms.</b> At ' + R + '20 per kg: A uses 80&divide;20 = '
 '<b>4 kg</b>, B uses 40&divide;20 = <b>2 kg</b>, C uses 20&divide;20 = <b>1 kg</b>. This is the '
 'step the whole of part (ii) depends on.',
 '<b>Fixed overhead per unit is given</b>, so total fixed cost = (6,400&times;9) + (3,200&times;22) + '
 '(2,400&times;18) = ' + R + '1,71,200. That total <b>does not change</b> in part (ii).',
 '<b>Check the shortage.</b> Budget needs (6,400&times;4) + (3,200&times;2) + (2,400&times;1) = '
 '25,600 + 6,400 + 2,400 = <b>34,400 kg</b>, but only 18,400 kg is available &mdash; a severe '
 'shortage of 16,000 kg.',
 'So rank by <b>contribution per kg</b>, and remember the budgeted production is the '
 '<b>demand ceiling</b> &mdash; you cannot make more of C than 2,400 units even though it ranks '
 'first.'])}"""

    p1 = table("(i) Statement of Budgeted Profit",
      [("Particulars", ""), ("A", "r"), ("B", "r"), ("C", "r"), ("Total " + R, "r")],
      [["Selling price per unit", "140", "120", "90", "&mdash;"],
       ["<i>Less:</i> Raw materials", "(80)", "(40)", "(20)", "&mdash;"],
       ["<i>Less:</i> Direct wages", "(5)", "(15)", "(10)", "&mdash;"],
       ["<i>Less:</i> Variable overheads", "(10)", "(30)", "(20)", "&mdash;"],
       {"cls": "sub", "cells": ["<b>Variable cost per unit</b>", "<b>95</b>", "<b>85</b>",
                                 "<b>50</b>", "&mdash;"]},
       {"cls": "sub", "cells": ["<b>Contribution per unit</b>", "<b>45</b>", "<b>35</b>",
                                 "<b>40</b>", "&mdash;"]},
       ["Budgeted units", "6,400", "3,200", "2,400", "&mdash;"],
       {"cls": "tot", "cells": ["<b>Total contribution</b>", "<b>2,88,000</b>", "<b>1,12,000</b>",
                                 "<b>96,000</b>", "<b>4,96,000</b>"]},
       ["Fixed overheads &nbsp;<span class='src' style='display:inline'>units &times; rate</span>",
        "(57,600)", "(70,400)", "(43,200)", "(1,71,200)"],
       {"cls": "tot", "cells": ["<b>BUDGETED PROFIT</b>", "", "", "", "<b>3,24,800</b>"]}])

    rank = table("(ii) Step 1 &mdash; Ranking by contribution per kg of raw material",
      [("Particulars", ""), ("A", "r"), ("B", "r"), ("C", "r")],
      [["Contribution per unit " + R, "45", "35", "40"],
       ["Raw material per unit &nbsp;<span class='src' style='display:inline'>cost &divide; " + R
        + "20</span>", "4 kg", "2 kg", "1 kg"],
       {"cls": "tot", "cells": ["<b>Contribution per kg</b>", "<b>11.25</b>", "<b>17.50</b>",
                                 "<b>40.00</b>"]},
       {"cls": "sub", "cells": ["<b>Rank</b>", "<b>3rd</b>", "<b>2nd</b>", "<b>1st</b>"]}])

    alloc = table("(ii) Step 2 &mdash; Allocating the 18,400 kg down the ranking",
      [("Rank", ""), ("Product", ""), ("Units made", "r"), ("kg per unit", "r"),
       ("kg used", "r"), ("kg remaining", "r")],
      [["1st", "C &mdash; full demand 2,400 units", "2,400", "1", "2,400", "16,000"],
       ["2nd", "B &mdash; full demand 3,200 units", "3,200", "2", "6,400", "9,600"],
       ["3rd", "A &mdash; only what is left", "<b>2,400</b>", "4", "9,600", "<b>Nil</b>"],
       {"cls": "tot", "cells": ["", "<b>Total</b>", "", "", "<b>18,400</b>", "<b>Nil</b>"]}])
    alloc += (f"<div class='small'>A&rsquo;s output falls from the budgeted 6,400 units to "
              f"{money(2400)} units &mdash; 9,600 kg &divide; 4 kg per unit. A is cut back because it "
              f"has the lowest contribution per kg.</div>")

    p2 = table("(ii) Step 3 &mdash; Profit under the optimal mix",
      [("Product", ""), ("Units", "r"), ("Contribution per unit " + R, "r"),
       ("Total contribution " + R, "r")],
      [["C", "2,400", "40", "96,000"],
       ["B", "3,200", "35", "1,12,000"],
       ["A", "2,400", "45", "1,08,000"],
       {"cls": "sub", "cells": ["<b>Total contribution</b>", "", "", "<b>3,16,000</b>"]},
       ["<i>Less:</i> Fixed overheads &nbsp;<span class='src' style='display:inline'>unchanged from "
        "part (i)</span>", "", "", "(1,71,200)"],
       {"cls": "tot", "cells": ["<b>PROFIT under the optimal mix</b>", "", "", "<b>1,44,800</b>"]}])

    return ("<div class='prob long'>"
            + prob_head("Q8", "Material shortage &mdash; optimal mix",
                        "Key factor &middot; p.34")
            + question(q) + read(rd) + p1 + rank + alloc + p2
            + why(f"""<p>Look at what the ranking did. Product A has the <b>highest contribution per
unit</b> at {R}45 &mdash; and it is the one cut back hardest, from 6,400 units to 2,400. Product C has
the <b>lowest</b> selling price and only {R}40 of contribution, yet it is protected in full.</p>
<p>The reason is that A swallows 4 kg per unit while C needs only 1 kg. Per kilogram of the scarce
material, C returns {R}40 and A returns just {R}11.25. When a resource is scarce, what matters is the
return per unit of that resource &mdash; never the return per unit of product.</p>
<p>Profit falls from {R}3,24,800 to {R}1,44,800 because of the shortage. But had you kept the
budgeted proportions instead of re-ranking, it would have fallen much further &mdash; the ranking
saves the company money.</p>""")
            + ans([("Contribution per unit &mdash; A / B / C", f"{R} 45 / {R} 35 / {R} 40"),
                   ("Raw material per unit &mdash; A / B / C", "4 kg / 2 kg / 1 kg"),
                   ("Contribution per kg &mdash; A / B / C",
                    f"{R} 11.25 / {R} 17.50 / {R} 40.00"),
                   ("Ranking", "C first, B second, A third"),
                   ("<b>(i) Budgeted profit</b>", f"<b>{R} 3,24,800</b>"),
                   ("Optimal mix", "C 2,400 units, B 3,200 units, A 2,400 units"),
                   ("<b>(ii) Profit under optimal mix</b>", f"<b>{R} 1,44,800</b>")])
            + "</div>")


# ======================================================================
# Q9
# ======================================================================
def q9():
    q = f"""<p>The following information in respect of Product A and Product B of a firm is given:</p>
{table(None, [("Particulars",""),("Product A","r"),("Product B","r")],
 [["Selling price per unit", R + " 75", R + " 48"],
  ["Direct materials", R + " 30", R + " 30"],
  ["Direct labour hours (" + R + "0.50 per hour)","15 hours","2 hours"]], headcls="lite")}
<p>Variable overhead = 100% of direct wages. Fixed overheads = {R}3,000. Present the above
information to show the profitability of products during a labour shortage.</p>"""

    rd = f"""{bullets([
 '<b>Compute the wages from the hours.</b> A: 15 hours &times; ' + R + '0.50 = ' + R + '7.50. '
 'B: 2 hours &times; ' + R + '0.50 = ' + R + '1.00. Then variable overhead equals the same amounts.',
 '<b>The key factor is named for you</b> &mdash; &ldquo;during a labour shortage&rdquo;. So rank by '
 'contribution per <b>labour hour</b>.',
 'This problem is the clearest illustration in the module of why contribution per unit misleads. '
 'A earns nearly twice B&rsquo;s contribution per unit, and is <b>four times worse</b> per hour.',
 'No quantities or total hours are given, so you are asked only to <b>show the profitability</b> '
 '&mdash; the ranking &mdash; not to build an optimal mix.'])}"""

    t = table("Statement of Profitability during a Labour Shortage",
      [("Particulars", ""), ("Product A " + R, "r"), ("Product B " + R, "r")],
      [["Selling price per unit", "75", "48"],
       ["<i>Less:</i> Direct materials", "(30)", "(30)"],
       ["<i>Less:</i> Direct wages &nbsp;<span class='src' style='display:inline'>15 &times; 0.50 "
        "&nbsp;|&nbsp; 2 &times; 0.50</span>", "(7.50)", "(1.00)"],
       ["<i>Less:</i> Variable overhead &nbsp;<span class='src' style='display:inline'>100% of "
        "direct wages</span>", "(7.50)", "(1.00)"],
       {"cls": "sub", "cells": ["<b>Marginal cost per unit</b>", "<b>45.00</b>", "<b>32.00</b>"]},
       {"cls": "sub", "cells": ["<b>Contribution per unit</b>", "<b>30.00</b>", "<b>16.00</b>"]},
       {"cls": "sub", "cells": ["P/V ratio", "40.00%", "33.33%"]},
       ["Direct labour hours per unit", "15", "2"],
       {"cls": "tot", "cells": ["<b>Contribution per labour hour</b>", "<b>2.00</b>",
                                 "<b>8.00</b>"]},
       {"cls": "sub", "cells": ["<b>Rank during a labour shortage</b>", "<b>2nd</b>",
                                 "<b>1st &mdash; four times better</b>"]}])

    dia = arrow_panel(500, 108, [
        {"box": (10, 6, 224, 30, "Judged on CONTRIBUTION PER UNIT|A " + R + "30  vs  B " + R + "16|"
                 "A looks nearly twice as good", "#fdf6e6"), "fs": 7.4},
        {"box": (266, 6, 224, 30, "Judged on CONTRIBUTION PER HOUR|A " + R + "2  vs  B " + R + "8|"
                 "B is four times better", "#eaf5f4"), "fs": 7.4},
        {"arc": (234, 21, 264, 21, "the scarce resource changes everything", -14)},
        {"box": (10, 50, 480, 24, "A needs 15 hours per unit; B needs only 2. In the 15 hours one A "
                 "takes, you could make 7.5 B's earning " + R + "120.", "#e8eef4"), "fs": 7.8},
        {"box": (10, 80, 480, 22, "RANK B FIRST. Make B up to the limit of demand, then use any "
                 "spare hours on A.", "#eef7ee"), "fs": 8.0,
         "stroke": "#2c7a34", "fg": "#1f5b26"},
    ], "Why contribution per unit is the wrong ranking when a resource is scarce.")

    return ("<div class='prob'>"
            + prob_head("Q9", "Labour shortage &mdash; ranking two products",
                        "Key factor &middot; p.34")
            + question(q) + read(rd) + t + dia
            + why(f"""<p><b>Product B is the more profitable during a labour shortage</b>, earning
{R}8 per labour hour against A&rsquo;s {R}2 &mdash; four times as much.</p>
<p><b>Recommendation:</b> produce B up to the limit of its demand and use any remaining hours on A.
Note that if labour were <i>not</i> scarce, A would be the better product on a per-unit basis and the
answer would reverse &mdash; which is exactly why identifying the key factor is the first thing you
do.</p>
<p>The fixed overhead of {R}3,000 has deliberately not been used. It is the same whichever product is
made, so it cannot influence the ranking. Mention that you have excluded it and why.</p>""")
            + ans([("Marginal cost per unit &mdash; A / B", f"{R} 45 / {R} 32"),
                   ("Contribution per unit &mdash; A / B", f"{R} 30 / {R} 16"),
                   ("Labour hours per unit &mdash; A / B", "15 / 2"),
                   ("<b>Contribution per labour hour &mdash; A / B</b>", f"<b>{R} 2 / {R} 8</b>"),
                   ("<b>Recommendation</b>",
                    "<b>Product B &mdash; four times more profitable per scarce labour hour</b>")])
            + "</div>")


# ======================================================================
# Q10
# ======================================================================
def q10():
    q = f"""<p>In a factory producing two different kinds of articles, the limiting factor is the
availability of labour. From the following information for 2016, show which product is more
profitable.</p>
{table(None, [("Particulars",""),("Product A (" + R + " per unit)","r"),
              ("Product B (" + R + " per unit)","r")],
 [["Materials","5.00","5.00"],
  ["Labour &mdash; 6 hours @ " + R + "0.50","3.00","&mdash;"],
  ["Labour &mdash; 3 hours @ " + R + "0.50","&mdash;","1.50"],
  ["Overheads &mdash; Fixed (50% of labour)","1.50","0.75"],
  ["Overheads &mdash; Variable","1.50","1.50"],
  {"cls":"tot","cells":["<b>Total Cost</b>","<b>11.00</b>","<b>8.75</b>"]},
  ["Selling Price","14.00","11.00"],
  ["Total production for the month","500 units","600 units"]], headcls="lite")}
<p>Also set the optimal product mix and the profitability if the maximum labour hours per month is
4,200 hours.</p>"""

    rd = f"""{bullets([
 '<b>The fixed overhead is described as 50% of labour</b>, so it is stated per unit but it is still '
 'a fixed cost. Exclude it from the marginal cost and treat the total as a lump sum: '
 '(500&times;1.50) + (600&times;0.75) = ' + R + '1,200.',
 'Marginal cost = materials + labour + variable overhead only. A = 5 + 3 + 1.50 = ' + R + '9.50; '
 'B = 5 + 1.50 + 1.50 = ' + R + '8.00.',
 '<b>Check the shortage.</b> Present production needs (500&times;6) + (600&times;3) = 3,000 + 1,800 = '
 '4,800 hours, but only 4,200 are available &mdash; short by <b>600 hours</b>.',
 'Rank by contribution per labour hour, then allocate. Present production is the <b>demand '
 'ceiling</b> for each product.'])}"""

    t1 = table("Statement of Profitability per unit and per labour hour",
      [("Particulars", ""), ("Product A " + R, "r"), ("Product B " + R, "r")],
      [["Selling price", "14.00", "11.00"],
       ["<i>Less:</i> Materials", "(5.00)", "(5.00)"],
       ["<i>Less:</i> Labour", "(3.00)", "(1.50)"],
       ["<i>Less:</i> Variable overheads", "(1.50)", "(1.50)"],
       {"cls": "sub", "cells": ["<b>Marginal cost per unit</b>", "<b>9.50</b>", "<b>8.00</b>"]},
       {"cls": "sub", "cells": ["<b>Contribution per unit</b>", "<b>4.50</b>", "<b>3.00</b>"]},
       ["Labour hours per unit", "6", "3"],
       {"cls": "tot", "cells": ["<b>Contribution per labour hour</b>", "<b>0.75</b>",
                                 "<b>1.00</b>"]},
       {"cls": "sub", "cells": ["<b>Rank</b>", "<b>2nd</b>", "<b>1st &mdash; more profitable</b>"]}])

    alloc = table("Optimal product mix within 4,200 labour hours",
      [("Rank", ""), ("Product", ""), ("Units", "r"), ("Hours per unit", "r"), ("Hours used", "r"),
       ("Hours left", "r")],
      [["1st", "B &mdash; full demand 600 units", "600", "3", "1,800", "2,400"],
       ["2nd", "A &mdash; only what is left", "<b>400</b>", "6", "2,400", "<b>Nil</b>"],
       {"cls": "tot", "cells": ["", "<b>Total</b>", "", "", "<b>4,200</b>", "<b>Nil</b>"]}])
    alloc += ("<div class='small'>A is cut from 500 units to 400 units &mdash; 2,400 hours &divide; "
              "6 hours per unit. B is protected in full because it earns more per hour.</div>")

    prof = table("Profitability of the optimal mix",
      [("Product", ""), ("Units", "r"), ("Contribution per unit " + R, "r"),
       ("Total contribution " + R, "r")],
      [["B", "600", "3.00", "1,800"],
       ["A", "400", "4.50", "1,800"],
       {"cls": "sub", "cells": ["<b>Total contribution</b>", "", "", "<b>3,600</b>"]},
       ["<i>Less:</i> Fixed overheads &nbsp;<span class='src' style='display:inline'>"
        "(500&times;1.50) + (600&times;0.75)</span>", "", "", "(1,200)"],
       {"cls": "tot", "cells": ["<b>PROFIT</b>", "", "", "<b>2,400</b>"]}])

    return ("<div class='prob long'>"
            + prob_head("Q10", "Labour limit &mdash; optimal mix and profit",
                        "Key factor &middot; p.34&ndash;35")
            + question(q) + read(rd) + t1 + alloc + prof
            + trap(bullets([
                '<b>Including the fixed overhead in the marginal cost.</b> The question calls it '
                '&ldquo;Overheads &mdash; Fixed&rdquo; even though it is shown per unit. It must be '
                'excluded from contribution and deducted once as a total.',
                '<b>Ranking A first because its contribution of ' + R + '4.50 is higher.</b> Per hour '
                'A returns only ' + R + '0.75 against B&rsquo;s ' + R + '1.00.',
                '<b>Making more than 600 units of B</b> because it ranks first. 600 is all the market '
                'takes &mdash; the given production figure is the demand ceiling.']))
            + ans([("Marginal cost per unit &mdash; A / B", f"{R} 9.50 / {R} 8.00"),
                   ("Contribution per unit &mdash; A / B", f"{R} 4.50 / {R} 3.00"),
                   ("<b>Contribution per labour hour &mdash; A / B</b>", f"<b>{R} 0.75 / {R} 1.00</b>"),
                   ("More profitable product", "<b>Product B</b>"),
                   ("Optimal mix within 4,200 hours", "B 600 units + A 400 units"),
                   ("Total contribution / fixed cost", f"{R} 3,600 / {R} 1,200"),
                   ("<b>Profit under the optimal mix</b>", f"<b>{R} 2,400</b>")])
            + "</div>")


# ======================================================================
# Q11
# ======================================================================
def q11():
    q = f"""<p>The cost of a manufacturing company for the product is: Materials {R}12.00; Labour
{R}9.00; Variable expenses {R}6.00; Fixed expenses {R}18.00 &mdash; total {R}45.00. The unit of
product is sold for {R}51.00.</p>
<p>The company&rsquo;s normal capacity is 1,00,000 units. The figures given above are for 80,000
units. The company has received an offer for 20,000 units @ {R}36 per unit from a foreign customer.</p>
<p>Advise the manufacturer on whether the order should be accepted. Also give your advice if the
order is from a local merchant.</p>"""

    rd = f"""{bullets([
 '<b>Variable cost per unit = 12 + 9 + 6 = ' + R + '27.</b> The ' + R + '18 of fixed expenses is '
 'per unit at 80,000 units, so total fixed cost = 80,000 &times; 18 = <b>' + R + '14,40,000</b>.',
 '<b>Capacity check.</b> 80,000 + 20,000 = 1,00,000 = exactly normal capacity. So the order uses '
 'idle capacity and no existing sales are lost, and <b>fixed cost does not increase</b>.',
 'The offer price of ' + R + '36 is well below the full cost of ' + R + '45 &mdash; which is the '
 'trap. Compare it with the <b>' + R + '27 variable cost</b>, not with ' + R + '45.',
 '<b>The second half of the question is about business judgement, not arithmetic.</b> The numbers are '
 'identical for a local merchant; what changes is the risk to the existing market. Make sure you '
 'answer it in words.'])}"""

    t = stmt("Comparative Statement of Profitability",
      ["Present<br/>80,000 units " + R, "Foreign order<br/>20,000 units " + R,
       "Total<br/>1,00,000 units " + R],
      [("Sales &nbsp;<span class='src' style='display:inline'>80,000&times;51 &nbsp;|&nbsp; "
        "20,000&times;36</span>", ["40,80,000", "7,20,000", "48,00,000"]),
       ("<i>Less:</i> Variable cost at " + R + "27 per unit", ["(21,60,000)", "(5,40,000)",
                                                               "(27,00,000)"]),
       ("<b>Contribution</b>", ["<b>19,20,000</b>", "<b>1,80,000</b>", "<b>21,00,000</b>"], "sub"),
       ("Contribution per unit", ["24", "9", "21"], "sub"),
       ("<i>Less:</i> Fixed expenses &nbsp;<span class='src' style='display:inline'>unchanged &mdash; "
        "spare capacity used</span>", ["(14,40,000)", "&mdash;", "(14,40,000)"]),
       ("<b>PROFIT</b>", ["<b>4,80,000</b>", "<b>1,80,000</b>", "<b>6,60,000</b>"], "tot")])

    return ("<div class='prob long'>"
            + prob_head("Q11", "Export order versus local order &mdash; same figures, different advice",
                        "Special order &middot; p.35")
            + question(q) + read(rd) + t
            + why(f"""<p><b>Advice on the foreign order: ACCEPT.</b> Each unit earns
{R}36 &minus; {R}27 = {R}9 of contribution, and since the fixed cost of {R}14,40,000 is already fully
recovered from the 80,000 domestic units, the whole {R}1,80,000 goes straight to profit. Profit rises
from {R}4,80,000 to {R}6,60,000.</p>
<p><b>Advice if the order is from a local merchant: normally REJECT &mdash; and the arithmetic is not
the reason.</b> The figures are identical, so on paper the order still adds {R}1,80,000. The problem
is what happens next:</p>
<ul class="tight">
<li>The merchant sells in the same market where the company charges {R}51. Goods bought at {R}36 can
be resold below {R}51, undercutting the company&rsquo;s own customers.</li>
<li>Existing customers who learn of the {R}36 price will demand it too. If even a fifth of the 80,000
regular units had to be repriced downward, the loss would swamp the {R}1,80,000 gained.</li>
<li>A foreign market is <b>geographically separate</b>, so the low price cannot leak back. That
separation is the only thing that makes the export order safe.</li>
</ul>
<p>Accept from a local merchant <b>only</b> if the goods can be genuinely segregated &mdash; a
different brand, a different region, or a binding condition on resale. Say that, and you have the
full mark.</p>""")
            + ans([("Variable cost per unit", f"{R} 27"),
                   ("Total fixed cost", f"{R} 14,40,000"),
                   ("Contribution per unit on the offer", f"{R} 36 &minus; {R} 27 = {R} 9"),
                   ("Extra contribution from 20,000 units", f"{R} 1,80,000"),
                   ("Profit before / after", f"{R} 4,80,000 / {R} 6,60,000"),
                   ("<b>Foreign customer</b>",
                    f"<b>ACCEPT &mdash; profit rises by {R} 1,80,000</b>"),
                   ("<b>Local merchant</b>",
                    "<b>REJECT</b> unless the market can be kept separate &mdash; risk of "
                    "undercutting the existing " + R + "51 price")])
            + "</div>")



# ======================================================================
# SHUT-DOWN PLAYBOOK
# ======================================================================
def shutdown_playbook():
    return f"""
<div class="modopen" style="page-break-before:always">
<div class="modopen-band" style="padding:22mm 18mm 12mm 18mm">
<div class="modopen-kicker">Module Three &middot; Playbook</div>
<div class="modopen-title" style="font-size:21pt">Shut-down Decisions</div>
<span class="modopen-count">Use these steps for Q12, Q13 and Q14</span>
</div>
<div class="modopen-body">

<div class="blk read"><span class="lab">The question is not &ldquo;are we losing money?&rdquo;</span>
<p>A factory making a loss should not automatically close. Closing does not make the loss go away
&mdash; some fixed costs continue whether the gates are open or shut (rent, rates, security,
depreciation, key salaries), and closing itself <b>costs money</b> (redundancy, mothballing
machinery, restarting later).</p>
<p>So the real question is: <b>which loss is smaller &mdash; the loss from carrying on, or the loss
from stopping?</b></p>
{fml("Continue if &nbsp; CONTRIBUTION &gt; Avoidable fixed cost &minus; Shut-down cost",
     "In plain words: keep going as long as the contribution you earn is bigger than the money you "
     "would actually save by stopping.")}
</div>

{arrow_panel(500, 150, [
  {"box": (12, 6, 226, 60, "IF YOU CONTINUE|Contribution earned|less ALL the fixed cost|"
           "= loss from operating", "#fdf6e6"), "fs": 7.6},
  {"box": (262, 6, 226, 60, "IF YOU SHUT DOWN|No contribution at all|"
           "Unavoidable fixed cost continues|PLUS shut-down costs", "#fdeeec"), "fs": 7.6,
   "stroke": "#c0392b", "fg": "#98271b"},
  {"box": (12, 80, 476, 22, "COMPARE THE TWO LOSSES. Choose whichever is SMALLER.", "#e8eef4"),
   "fs": 8.4},
  {"box": (12, 112, 476, 32, "SHUT-DOWN POINT (units) = "
           "(Avoidable fixed cost &minus; Shut-down cost) &divide; Contribution per unit|"
           "Below this level of sales, shutting down is cheaper. Above it, keep operating.",
           "#eef7ee"), "fs": 7.8, "stroke": "#2c7a34", "fg": "#1f5b26"},
  {"line": (125, 66, 125, 78)}, {"line": (375, 66, 375, 78)},
], "The comparison, and the formula for the exact break-point between the two.")}

<div class="blk method"><span class="lab">The five steps</span>
{steps([
 "<b>Contribution per unit</b> = selling price &minus; all variable costs (including variable "
 "selling expenses).",
 "<b>Total fixed cost for the period.</b> Watch the period &mdash; if the fixed cost is annual and "
 "the question asks about a quarter, divide by four.",
 "<b>Unavoidable fixed cost</b> = what still has to be paid after shutting. "
 "<b>Avoidable = Total &minus; Unavoidable.</b>",
 "<b>Loss if you continue</b> = Total fixed cost &minus; Contribution. "
 "<b>Loss if you shut</b> = Unavoidable fixed cost + Shut-down cost.",
 "Compare, recommend in words, then compute the <b>shut-down point</b> if asked."])}
</div>

<div class="blk trap"><span class="lab">The two traps</span>
{bullets([
 '<b>Treating the whole fixed cost as avoidable.</b> Read the question carefully: it always tells you '
 'how much continues, either directly ("only " + R + "20,000 can be avoided") or indirectly '
 '("fixed cost will be reduced to " + R + "130,000").',
 '<b>Forgetting the shut-down cost.</b> It works <i>against</i> closing and it is easy to miss. It '
 'reduces the saving, and in the shut-down-point formula it is <b>subtracted</b> from the avoidable '
 'fixed cost.'])}
</div>
</div></div>"""


# ======================================================================
# Q12
# ======================================================================
def q12():
    q = f"""<p>The selling price per unit of a product is {D}14. For the forthcoming period the demand
will be only 5,000 units. The fixed expenses at 50% activity (5,000 units) will be {D}30,000. The
company is thinking of shutting down operations, in which case an additional amount of {D}2,000 will
have to be incurred for shutting down and only {D}20,000 of the above fixed costs can be avoided.</p>
<p>What should be the variable cost per unit to recommend a shut-down?</p>"""

    rd = f"""{bullets([
 'This is the shut-down comparison run <b>backwards</b>. You are not asked which is better &mdash; '
 'you are asked what variable cost would make shutting down the better choice.',
 '<b>Work out the shut-down loss first, because it is a fixed number.</b> Unavoidable fixed cost = '
 '30,000 &minus; 20,000 = ' + D + '10,000, plus shut-down cost ' + D + '2,000 = '
 '<b>' + D + '12,000</b>. That is the loss if the plant closes, whatever the variable cost is.',
 'Then set the loss from continuing equal to ' + D + '12,000 and solve for the variable cost. '
 'That gives the <b>indifference point</b> &mdash; above it, shut down.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Loss if the plant is shut down</h4>
{calc([f'Total fixed expenses &nbsp;=&nbsp; {D}30,000',
       f'Less: Avoidable on shut-down &nbsp;=&nbsp; ({D}20,000)',
       f'<b>Unavoidable fixed cost &nbsp;=&nbsp; {D}10,000</b>',
       f'Add: Shut-down costs &nbsp;=&nbsp; {D}2,000',
       f'<b>LOSS IF SHUT DOWN &nbsp;=&nbsp; {D}12,000</b>'])}

<h4 class="mini">W2 &nbsp;Loss if operations continue, in terms of the variable cost <i>v</i></h4>
{calc(['Contribution &nbsp;=&nbsp; 5,000 &times; (14 &minus; <i>v</i>)',
       'Loss if continue &nbsp;=&nbsp; 30,000 &minus; 5,000(14 &minus; <i>v</i>)'])}

<h4 class="mini">W3 &nbsp;Setting the two equal to find the indifference point</h4>
{calc(['30,000 &minus; 5,000(14 &minus; <i>v</i>) &nbsp;=&nbsp; 12,000',
       '30,000 &minus; 12,000 &nbsp;=&nbsp; 5,000(14 &minus; <i>v</i>)',
       '18,000 &nbsp;=&nbsp; 5,000(14 &minus; <i>v</i>)',
       '14 &minus; <i>v</i> &nbsp;=&nbsp; ' + frac("18,000", "5,000") + ' &nbsp;=&nbsp; 3.60',
       f'<b><i>v</i> &nbsp;=&nbsp; 14 &minus; 3.60 &nbsp;=&nbsp; {D}10.40 per unit</b>'])}"""

    proof = table("Proof and interpretation",
      [("Variable cost per unit", "r"), ("Contribution per unit", "r"),
       ("Total contribution", "r"), ("Loss if continue", "r"), ("Loss if shut", "r"),
       ("Decision", "")],
      [[D + "10.00", D + "4.00", "20,000", "(10,000)", "(12,000)",
        "<b>Continue</b> &mdash; loss is smaller"],
       [D + "10.40", D + "3.60", "18,000", "(12,000)", "(12,000)",
        "<b>Indifferent</b> &mdash; the break-point"],
       [D + "11.00", D + "3.00", "15,000", "(15,000)", "(12,000)",
        "<b>Shut down</b> &mdash; shutting is cheaper"]], headcls="lite")

    return ("<div class='prob long'>"
            + prob_head("Q12", "Working the shut-down decision backwards",
                        "Shut-down &middot; p.35")
            + question(q) + read(rd) + wn(wnh) + proof
            + why(f"""<p><b>Answer: the variable cost per unit would have to be {D}10.40 or more before
a shut-down could be recommended.</b></p>
<p>At exactly {D}10.40 the two losses are both {D}12,000 and management is indifferent. Above
{D}10.40 the contribution falls below the {D}18,000 that operating must generate to justify itself,
and closing becomes the cheaper option.</p>
<p>Note the shape of the answer: the plant is worth running even at a loss, as long as that loss is
smaller than {D}12,000. A contribution of anything above {D}18,000 makes operating worthwhile even
though the company never reaches profit.</p>""")
            + ans([("Unavoidable fixed cost", f"{D} 10,000"),
                   ("Shut-down cost", f"{D} 2,000"),
                   ("<b>Loss if shut down</b>", f"<b>{D} 12,000</b>"),
                   ("Contribution needed to justify operating", f"{D} 18,000"),
                   ("Contribution needed per unit", f"{D} 18,000 &divide; 5,000 = {D} 3.60"),
                   ("<b>Variable cost at which shut-down is recommended</b>",
                    f"<b>{D} 10.40 per unit or more</b>")])
            + "</div>")


# ======================================================================
# Q13
# ======================================================================
def q13():
    q = f"""<p>G Ltd. produces and sells 95,000 units of X in a year at its 80% production capacity.
The selling price of the product is {D}8 per unit. The variable cost is 75% of the sale price per
unit. The fixed cost is {D}350,000. The company is continuously incurring losses and management plans
to shut down the plant. The fixed cost is expected to be reduced to {D}130,000. Additional costs of
plant shut-down are expected at {D}15,000.</p>
<p>Should the plant be shut down? What is the capacity level of production at the shut-down point?</p>"""

    rd = f"""{bullets([
 '&ldquo;Variable cost is 75% of the sale price&rdquo; &rarr; ' + D + '6 per unit, so contribution '
 'is ' + D + '2 per unit. Convert the percentage into money before anything else.',
 '&ldquo;Fixed cost expected to be reduced to ' + D + '130,000&rdquo; means <b>' + D + '130,000 is '
 'unavoidable</b> and 350,000 &minus; 130,000 = <b>' + D + '220,000 is avoidable</b>.',
 '<b>95,000 units = 80% capacity</b>, so 100% capacity = 95,000 &divide; 0.80 = <b>118,750 units</b>. '
 'You need this to answer the second part.',
 'The plant is loss-making either way &mdash; the question is only which loss is smaller.'])}"""

    cmp2 = stmt("Comparative Statement &mdash; continue or shut down",
      ["Continue " + D, "Shut down " + D],
      [("Sales &nbsp;<span class='src' style='display:inline'>95,000 &times; " + D + "8</span>",
        ["760,000", "&mdash;"]),
       ("<i>Less:</i> Variable cost &nbsp;<span class='src' style='display:inline'>95,000 &times; "
        + D + "6</span>", ["(570,000)", "&mdash;"]),
       ("<b>Contribution</b> &nbsp;<span class='src' style='display:inline'>95,000 &times; " + D
        + "2</span>", ["<b>190,000</b>", "<b>Nil</b>"], "sub"),
       ("<i>Less:</i> Fixed cost", ["(350,000)", "(130,000)"]),
       ("<i>Less:</i> Shut-down costs", ["&mdash;", "(15,000)"]),
       ("<b>LOSS</b>", ["<b>(160,000)</b>", "<b>(145,000)</b>"], "tot"),
       ("<b>Decision</b>", ["Loss is larger", "<b>SHUT DOWN &mdash; saves " + D + "15,000</b>"],
        "sub")])

    sdp = f"""<h4 class="mini">Shut-down point</h4>
{calc([f'Avoidable fixed cost &nbsp;=&nbsp; 350,000 &minus; 130,000 &nbsp;=&nbsp; {D}220,000',
       f'Less: Additional shut-down cost &nbsp;=&nbsp; ({D}15,000)',
       f'<b>Net saving from shutting down &nbsp;=&nbsp; {D}205,000</b>'])}
{fml("Shut-down point &nbsp;=&nbsp; " + frac("Avoidable fixed cost &minus; Shut-down cost",
                                            "Contribution per unit")
     + " &nbsp;=&nbsp; " + frac("205,000", "2") + " &nbsp;=&nbsp; <b>102,500 units</b>")}
{calc(['100% capacity &nbsp;=&nbsp; 95,000 &divide; 0.80 &nbsp;=&nbsp; <b>118,750 units</b>',
       'Capacity at the shut-down point &nbsp;=&nbsp; ' + frac("102,500", "118,750")
       + ' &times; 100 &nbsp;=&nbsp; <b>86.32%</b>'])}
<p class="small"><b>Consistency check:</b> the company is operating at 80% (95,000 units), which is
<b>below</b> the shut-down point of 86.32% (102,500 units). So shutting down is correct &mdash; the two
answers agree, which is your proof.</p>"""

    return ("<div class='prob long'>"
            + prob_head("Q13", "Shut down, and the shut-down point in capacity terms",
                        "Shut-down &middot; p.35")
            + question(q) + read(rd) + cmp2 + wn(sdp)
            + why(f"""<p><b>Yes, shut the plant down. It saves {D}15,000</b> &mdash; the loss falls
from {D}160,000 to {D}145,000.</p>
<p>The shut-down point of <b>102,500 units, or 86.32% of capacity</b>, is the more useful answer for
management. It says: if sales can be lifted above 102,500 units the plant is worth running again; below
that it is not. At the current 95,000 units the company is 7,500 units short of the level that would
justify keeping the gates open.</p>
<p>One line worth adding: closing is a serious step with consequences the numbers do not show &mdash;
loss of skilled workers, of customers, and the cost of restarting. If the shortfall is only 7,500
units and demand may recover, management might reasonably keep operating for a while and accept the
extra {D}15,000 as the price of staying in business.</p>""")
            + ans([("Contribution per unit", f"{D} 2 (selling {D} 8 less variable {D} 6)"),
                   ("Avoidable / unavoidable fixed cost", f"{D} 220,000 / {D} 130,000"),
                   ("Loss if continue", f"{D} 160,000"),
                   ("Loss if shut down", f"{D} 145,000"),
                   ("<b>Decision</b>", f"<b>SHUT DOWN &mdash; saves {D} 15,000</b>"),
                   ("<b>Shut-down point</b>",
                    "<b>102,500 units = 86.32% of capacity</b>")])
            + "</div>")


# ======================================================================
# Q14
# ======================================================================
def q14():
    q = f"""<p>A Paint Manufacturing Company manufactures 200,000 medium-sized tins of &lsquo;Spray Lac
Paints&rsquo; annually when working at normal capacity. Its cost of manufacture per unit is {D}16.40
made up as: Direct Materials {D}7.80; Direct Labour {D}2.10; Variable Overheads {D}2.50; Fixed
Overheads {D}4.00.</p>
<p>Each tin is sold for {D}21 with variable selling expenses of {D}0.60 per tin. During the next
quarter only 10,000 units can be produced and sold. Management plans to shut down the plant,
estimating that the fixed manufacturing cost can be reduced to {D}74,000 for the quarter. When the
plant is operating, fixed overheads are incurred at a uniform rate throughout the year. Additional
costs of plant shut-down for the quarter are estimated at {D}14,000.</p>
<p><b>(a)</b> Express your opinion, with calculations, as to whether the plant should be shut down
during the quarter. <b>(b)</b> Calculate the shut-down point for the quarter in tins.</p>"""

    rd = f"""<p>The trap in this problem is the <b>time period</b>. Almost everything given is annual;
the question is about one quarter.</p>
{bullets([
 '<b>Annual fixed overhead</b> = 200,000 tins &times; ' + D + '4.00 = ' + D + '800,000. '
 '&ldquo;Incurred at a uniform rate throughout the year&rdquo; means <b>' + D + '200,000 per '
 'quarter</b>. That is the figure to use, not 800,000.',
 '<b>Do not forget the variable selling expense of ' + D + '0.60.</b> It is listed separately from '
 'the manufacturing cost, so it is easy to miss &mdash; but it is variable and must come out of '
 'contribution.',
 'Variable cost per tin = 7.80 + 2.10 + 2.50 + 0.60 = <b>' + D + '13.00</b>, so contribution = '
 '21 &minus; 13 = <b>' + D + '8.00 per tin</b>.',
 '<b>' + D + '74,000 is the unavoidable fixed cost</b> for the quarter, so avoidable = '
 '200,000 &minus; 74,000 = ' + D + '126,000.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Contribution per tin</h4>
{table(None, [("Element",""),("Per tin " + D,"r")],
 [["Selling price","21.00"],
  ["<i>Less:</i> Direct materials","(7.80)"],
  ["<i>Less:</i> Direct labour","(2.10)"],
  ["<i>Less:</i> Variable overheads","(2.50)"],
  ["<i>Less:</i> Variable selling expenses","(0.60)"],
  {"cls":"sub","cells":["<b>Total variable cost</b>","<b>(13.00)</b>"]},
  {"cls":"tot","cells":["<b>Contribution per tin</b>","<b>8.00</b>"]}], headcls="lite",
 widths=["70%","30%"])}

<h4 class="mini">W2 &nbsp;Fixed overhead for the QUARTER &mdash; the key step</h4>
{calc([f'Annual fixed overhead &nbsp;=&nbsp; 200,000 tins &times; {D}4.00 &nbsp;=&nbsp; '
       f'<b>{D}800,000</b>',
       'Incurred uniformly, so per quarter &nbsp;=&nbsp; 800,000 &divide; 4 &nbsp;=&nbsp; '
       f'<b>{D}200,000</b>',
       f'Unavoidable if shut &nbsp;=&nbsp; {D}74,000 &nbsp;&rarr;&nbsp; '
       f'<b>avoidable = {D}126,000</b>'])}"""

    cmp2 = stmt("(a) Comparative Statement for the quarter",
      ["Continue " + D, "Shut down " + D],
      [("Sales &nbsp;<span class='src' style='display:inline'>10,000 &times; " + D + "21</span>",
        ["210,000", "&mdash;"]),
       ("<i>Less:</i> Variable cost &nbsp;<span class='src' style='display:inline'>10,000 &times; "
        + D + "13</span>", ["(130,000)", "&mdash;"]),
       ("<b>Contribution</b> &nbsp;<span class='src' style='display:inline'>10,000 &times; " + D
        + "8</span>", ["<b>80,000</b>", "<b>Nil</b>"], "sub"),
       ("<i>Less:</i> Fixed overheads for the quarter &nbsp;<span class='src' "
        "style='display:inline'>W2</span>", ["(200,000)", "(74,000)"]),
       ("<i>Less:</i> Additional shut-down costs", ["&mdash;", "(14,000)"]),
       ("<b>LOSS</b>", ["<b>(120,000)</b>", "<b>(88,000)</b>"], "tot"),
       ("<b>Decision</b>", ["Loss is larger by " + D + "32,000",
                            "<b>SHUT DOWN &mdash; saves " + D + "32,000</b>"], "sub")])

    sdp = f"""{calc([f'Avoidable fixed cost for the quarter &nbsp;=&nbsp; 200,000 &minus; 74,000 '
       f'&nbsp;=&nbsp; {D}126,000',
       f'Less: Additional shut-down cost &nbsp;=&nbsp; ({D}14,000)',
       f'<b>Net saving from shutting down &nbsp;=&nbsp; {D}112,000</b>'])}
{fml("Shut-down point &nbsp;=&nbsp; " + frac("112,000", "8") + " &nbsp;=&nbsp; <b>14,000 tins</b>")}
<p class="small"><b>Consistency check:</b> only 10,000 tins can be sold, which is below the shut-down
point of 14,000 tins &mdash; so shutting down is correct. The two parts of the answer confirm each
other.</p>"""

    return ("<div class='prob long'>"
            + prob_head("Q14", "Quarterly shut-down &mdash; watch the time period",
                        "Shut-down &middot; p.36")
            + question(q) + read(rd) + wn(wnh) + cmp2 + wn(sdp)
            + trap(bullets([
                '<b>Using ' + D + '800,000 of fixed overhead in a quarterly statement.</b> That is the '
                'annual figure. The question says the overhead is incurred uniformly, which is a '
                'direct instruction to divide by four.',
                '<b>Omitting the ' + D + '0.60 variable selling expense.</b> It sits outside the ' +
                D + '16.40 manufacturing cost and is easy to overlook, but it reduces contribution '
                'from ' + D + '8.60 to ' + D + '8.00 and changes the shut-down point from 13,023 to '
                '14,000 tins.',
                '<b>Treating the whole ' + D + '200,000 as avoidable.</b> Only ' + D + '126,000 is; ' +
                D + '74,000 continues.']))
            + ans([("Variable cost / contribution per tin", f"{D} 13.00 / {D} 8.00"),
                   ("Fixed overhead for the quarter", f"{D} 200,000"),
                   ("Avoidable / unavoidable", f"{D} 126,000 / {D} 74,000"),
                   ("Loss if continue", f"{D} 120,000"),
                   ("Loss if shut down", f"{D} 88,000"),
                   ("<b>(a) Opinion</b>", f"<b>SHUT DOWN &mdash; saves {D} 32,000</b>"),
                   ("<b>(b) Shut-down point</b>", "<b>14,000 tins for the quarter</b>")])
            + "</div>")


# ======================================================================
# Q15
# ======================================================================
def q15():
    q = f"""<p>From the following information, prepare the break-even chart. Fixed Cost {R}2,000;
Variable Cost {R}0.50 per unit; Sales {R}1 per unit. Units produced and sold 2,000; 4,000; 6,000;
8,000 and 10,000.</p>"""

    rd = f"""{bullets([
 '<b>Build the table before you draw anything.</b> Compute sales, variable cost, total cost and '
 'profit at each of the five volumes. The chart is just those numbers plotted.',
 'Three lines go on the chart: a <b>horizontal</b> fixed-cost line at ' + R + '2,000; a '
 '<b>total-cost</b> line starting at ' + R + '2,000 on the vertical axis; and a <b>sales</b> line '
 'starting at the origin.',
 '<b>The total cost line must start at the fixed cost, not at zero.</b> At zero output you still pay ' +
 R + '2,000. This is the single most common drawing error.',
 'The break-even point is where the sales line crosses the total cost line. Mark it, drop a dotted '
 'line to each axis, and label both readings.'])}"""

    tbl = table("Statement of cost and profit at each volume &mdash; the data for the chart",
      [("Units", "r"), ("Sales @ " + R + "1", "r"), ("Variable cost @ " + R + "0.50", "r"),
       ("Fixed cost", "r"), ("Total cost", "r"), ("Profit / (Loss)", "r")],
      [["2,000", "2,000", "1,000", "2,000", "3,000", "(1,000)"],
       ["<b>4,000</b>", "<b>4,000</b>", "2,000", "2,000", "<b>4,000</b>", "<b>Nil &mdash; BEP</b>"],
       ["6,000", "6,000", "3,000", "2,000", "5,000", "1,000"],
       ["8,000", "8,000", "4,000", "2,000", "6,000", "2,000"],
       ["10,000", "10,000", "5,000", "2,000", "7,000", "3,000"]], headcls="lite")

    ver = f"""{calc([f'Contribution per unit &nbsp;=&nbsp; 1.00 &minus; 0.50 &nbsp;=&nbsp; '
       f'<b>{R}0.50</b>',
       'P/V ratio &nbsp;=&nbsp; 0.50 &divide; 1.00 &nbsp;=&nbsp; <b>50%</b>'])}
{fml("BEP (units) &nbsp;=&nbsp; " + frac("2,000", "0.50") + " &nbsp;=&nbsp; <b>4,000 units</b>"
     " &nbsp;&nbsp;&nbsp; BEP (" + R + ") &nbsp;=&nbsp; " + frac("2,000", "0.50")
     + f" &nbsp;=&nbsp; <b>{R}4,000</b>")}
<p class="small">The table, the formula and the chart all give 4,000 units. Always verify the graph by
calculation &mdash; examiners award marks for the check.</p>"""

    chart = be_chart(470, 250, 10000, 10000, 2000, 0.50, 1.00,
                     "Output (units)", "Sales and cost (" + R + ")",
                     4000, 4000,
                     "Break-even chart. BEP = 4,000 units = " + R + "4,000. Note how the total-cost "
                     "line begins at " + R + "2,000 on the vertical axis, not at the origin.")

    return ("<div class='prob long'>"
            + prob_head("Q15", "Break-even chart", "Charts &middot; p.36")
            + question(q) + read(rd) + tbl + chart + wn(ver)
            + trap(bullets([
                'Starting the total-cost line at the origin. It must start at the fixed cost.',
                'Forgetting to label the axes and state the scale. Both carry marks.',
                'Not marking the profit and loss areas. The wedge left of the BEP is loss, the wedge '
                'right of it is profit &mdash; shade or label them.',
                'Drawing the chart and stopping. <b>Always verify the BEP by formula underneath.</b>']))
            + ans([("Contribution per unit / P/V ratio", f"{R} 0.50 / 50%"),
                   ("<b>Break-even point</b>", f"<b>4,000 units = {R} 4,000</b>"),
                   ("Loss at 2,000 units", f"{R} 1,000"),
                   ("Profit at 10,000 units", f"{R} 3,000"),
                   ("Margin of safety at 10,000 units", f"6,000 units = {R} 6,000")])
            + "</div>")


# ======================================================================
# Q16
# ======================================================================
def q16():
    q = f"""<p>You are given the following data for the costing year of a factory: Budget output
1,00,000 units; Fixed Expenses {R}5,00,000; Variable Expenses {R}10 per unit; Selling Price {R}20 per
unit.</p>
<p>Draw a break-even chart showing the break-even point. If the selling price is reduced to {R}18 per
unit, what will be the new break-even point?</p>"""

    rd = f"""{bullets([
 'Contribution = 20 &minus; 10 = ' + R + '10 per unit, so the P/V ratio is 50% and the BEP is '
 '5,00,000 &divide; 10 = <b>50,000 units</b> &mdash; exactly half the budget.',
 '<b>When the price falls to ' + R + '18 the variable cost does not change.</b> Only contribution '
 'falls, from ' + R + '10 to ' + R + '8, so the BEP rises to 5,00,000 &divide; 8 = <b>62,500 '
 'units</b>.',
 'On the chart, show the second sales line as a <b>dashed line of lower slope</b> from the same '
 'origin. Two sales lines, one total-cost line, two break-even points.'])}"""

    wnh = f"""<h4 class="mini">Present position &mdash; selling price {R}20</h4>
{calc([f'Contribution per unit &nbsp;=&nbsp; 20 &minus; 10 &nbsp;=&nbsp; <b>{R}10</b> '
       '&nbsp;&rarr;&nbsp; P/V ratio <b>50%</b>',
       'BEP &nbsp;=&nbsp; ' + frac("5,00,000", "10") + ' &nbsp;=&nbsp; <b>50,000 units</b>',
       f'BEP sales value &nbsp;=&nbsp; 50,000 &times; 20 &nbsp;=&nbsp; <b>{R}10,00,000</b>',
       f'Profit at budget &nbsp;=&nbsp; (1,00,000 &times; 10) &minus; 5,00,000 &nbsp;=&nbsp; '
       f'<b>{R}5,00,000</b>'])}

<h4 class="mini">Revised position &mdash; selling price reduced to {R}18</h4>
{calc([f'Contribution per unit &nbsp;=&nbsp; 18 &minus; 10 &nbsp;=&nbsp; <b>{R}8</b> '
       '&nbsp;&rarr;&nbsp; P/V ratio <b>44.44%</b>',
       'New BEP &nbsp;=&nbsp; ' + frac("5,00,000", "8") + ' &nbsp;=&nbsp; <b>62,500 units</b>',
       f'New BEP sales value &nbsp;=&nbsp; 62,500 &times; 18 &nbsp;=&nbsp; <b>{R}11,25,000</b>',
       f'Profit at budget &nbsp;=&nbsp; (1,00,000 &times; 8) &minus; 5,00,000 &nbsp;=&nbsp; '
       f'<b>{R}3,00,000</b>'])}"""

    comp = table("The effect of the price reduction",
      [("", ""), ("At " + R + "20", "r"), ("At " + R + "18", "r"), ("Change", "r")],
      [["Selling price per unit", "20", "18", "&minus;10%"],
       ["Variable cost per unit", "10", "10", "no change"],
       ["Contribution per unit", "10", "8", "&minus;20%"],
       ["P/V ratio", "50.00%", "44.44%", "&minus;5.56 points"],
       {"cls": "tot", "cells": ["<b>Break-even point (units)</b>", "<b>50,000</b>", "<b>62,500</b>",
                                 "<b>+25%</b>"]},
       ["Break-even sales value", "10,00,000", "11,25,000", "+12.5%"],
       ["Profit at budgeted 1,00,000 units", "5,00,000", "3,00,000", "&minus;40%"]],
      headcls="lite")

    chart = be_chart(470, 258, 100000, 2000000, 500000, 10, 20,
                     "Output (units)", "Sales and cost (" + R + ")",
                     50000, 1000000,
                     "Break-even chart at " + R + "20 (solid) with the revised sales line at " + R
                     + "18 (dashed). BEP moves right from 50,000 to 62,500 units.",
                     extra_line=18, extra_label="Sales at " + R + "18")

    return ("<div class='prob long'>"
            + prob_head("Q16", "Break-even chart with a revised selling price",
                        "Charts &middot; p.36")
            + question(q) + read(rd) + wn(wnh) + chart + comp
            + why(f"""<p>A 10% cut in the selling price raises the break-even point by <b>25%</b> and
cuts the budgeted profit by <b>40%</b>. The whole of the price reduction comes out of contribution,
because the variable cost does not fall to share it.</p>
<p>On the chart you can see it directly: the dashed sales line is flatter, so it takes longer to climb
above the total cost line and it crosses further to the right. That visual is exactly what a
break-even chart is for &mdash; it shows a manager the consequence of a pricing decision at a
glance.</p>""")
            + ans([("Contribution per unit &mdash; at " + R + "20 / at " + R + "18",
                    f"{R} 10 / {R} 8"),
                   ("P/V ratio &mdash; at " + R + "20 / at " + R + "18", "50% / 44.44%"),
                   ("<b>BEP at {} 20</b>".format(R), f"<b>50,000 units = {R} 10,00,000</b>"),
                   ("<b>New BEP at {} 18</b>".format(R), f"<b>62,500 units = {R} 11,25,000</b>"),
                   ("Profit at budget &mdash; before / after",
                    f"{R} 5,00,000 / {R} 3,00,000")])
            + "</div>")


# ======================================================================
# Q17
# ======================================================================
def q17():
    q = f"""<p>The following figures relate to a particular year&rsquo;s working at 100% capacity level
in a manufacturing concern: Fixed Overheads {R}1,20,000; Variable overheads {R}2,00,000; Direct wages
{R}1,50,000; Direct Materials {R}4,10,000; Sales {R}10,00,000.</p>
<p>Represent the above figures on a Break-even Chart and determine from the chart the break-even
point. Verify your results by calculations.</p>"""

    rd = f"""{bullets([
 '<b>Only the fixed overhead is fixed.</b> Direct materials, direct wages and variable overheads are '
 'all variable: 4,10,000 + 1,50,000 + 2,00,000 = <b>' + R + '7,60,000</b>.',
 'Because no unit figures are given, plot the chart against <b>sales value or capacity percentage</b> '
 'on the horizontal axis rather than units. Either is acceptable &mdash; state which you have used.',
 'Contribution = 10,00,000 &minus; 7,60,000 = ' + R + '2,40,000, so the P/V ratio is <b>24%</b> and '
 'the BEP is 1,20,000 &divide; 0.24 = <b>' + R + '5,00,000</b>, which is exactly <b>50% of '
 'capacity</b>. A round answer like that is the examiner confirming your method.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;Separating fixed from variable</h4>
{table(None, [("Element",""),("Amount " + R,"r"),("Nature","")],
 [["Direct materials","4,10,000","Variable"],["Direct wages","1,50,000","Variable"],
  ["Variable overheads","2,00,000","Variable"],
  {"cls":"tot","cells":["<b>Total variable cost</b>","<b>7,60,000</b>",""]},
  ["Fixed overheads","1,20,000","Fixed"],
  {"cls":"sub","cells":["<b>Total cost</b>","<b>8,80,000</b>",""]},
  ["Sales","10,00,000",""],
  {"cls":"tot","cells":["<b>Profit</b>","<b>1,20,000</b>",""]}], headcls="lite")}

<h4 class="mini">W2 &nbsp;Verification by calculation</h4>
{calc([f'Contribution &nbsp;=&nbsp; 10,00,000 &minus; 7,60,000 &nbsp;=&nbsp; <b>{R}2,40,000</b>',
       'P/V ratio &nbsp;=&nbsp; ' + frac("2,40,000", "10,00,000") + ' &times; 100 &nbsp;=&nbsp; '
       '<b>24%</b>'])}
{fml("BEP &nbsp;=&nbsp; " + frac("Fixed cost", "P/V ratio") + " &nbsp;=&nbsp; "
     + frac("1,20,000", "0.24") + f" &nbsp;=&nbsp; <b>{R}5,00,000</b>")}
{calc([f'BEP as a percentage of capacity &nbsp;=&nbsp; ' + frac("5,00,000", "10,00,000")
       + ' &times; 100 &nbsp;=&nbsp; <b>50% of capacity</b>',
       f'Margin of safety &nbsp;=&nbsp; 10,00,000 &minus; 5,00,000 &nbsp;=&nbsp; '
       f'<b>{R}5,00,000</b> (50% of sales)',
       f'Profit check &nbsp;=&nbsp; MOS &times; P/V ratio &nbsp;=&nbsp; 5,00,000 &times; 24% '
       f'&nbsp;=&nbsp; <b>{R}1,20,000</b> &#10003; agrees with W1'])}"""

    chart = be_chart(470, 252, 100, 1000000, 120000, 7600, 10000,
                     "Capacity utilisation (%)", "Sales and cost (" + R + ")",
                     50, 500000,
                     "Break-even chart plotted against capacity. The BEP reads off the chart at 50% "
                     "of capacity, i.e. " + R + "5,00,000 of sales &mdash; confirmed by calculation "
                     "in W2.")

    return ("<div class='prob long'>"
            + prob_head("Q17", "Chart plotted against capacity, verified by formula",
                        "Charts &middot; p.36")
            + question(q) + read(rd) + wn(wnh) + chart
            + why(f"""<p>Reading the chart: the sales line and the total-cost line meet at the 50%
capacity mark, which corresponds to {R}5,00,000 of sales on the vertical axis. The calculation in W2
gives exactly the same figure, which is what the question means by &ldquo;verify your results&rdquo;.</p>
<p>The chart also shows the margin of safety directly &mdash; it is the horizontal distance from the
break-even point at 50% to the 100% capacity line, and the vertical gap between the two lines at 100%
capacity is the profit of {R}1,20,000.</p>""")
            + ans([("Total variable cost / fixed cost", f"{R} 7,60,000 / {R} 1,20,000"),
                   ("Contribution", f"{R} 2,40,000"),
                   ("P/V ratio", "24%"),
                   ("<b>Break-even point</b>", f"<b>{R} 5,00,000 = 50% of capacity</b>"),
                   ("Margin of safety", f"{R} 5,00,000 (50% of sales)"),
                   ("Profit at 100% capacity", f"{R} 1,20,000")])
            + "</div>")


# ======================================================================
# Q18
# ======================================================================
def q18():
    q = f"""<p>Draw the profit&ndash;volume graph and find out the P/V Ratio with the following
information: Output 3,000 units; Volume of Sales {R}7,500; Variable Cost {R}4,500; Fixed Cost
{R}1,500.</p>"""

    rd = f"""<p>A <b>profit&ndash;volume graph</b> is not the same as a break-even chart, and the
difference is worth knowing:</p>
{table(None, [("",""),("Break-even chart","" ),("Profit&ndash;volume graph","")],
 [["What is plotted","Sales and total cost, both as lines",
   "<b>Profit or loss only</b>, as one line"],
  ["The vertical axis","Rupees of sales and cost, all positive",
   "Profit above zero, <b>loss below zero</b>"],
  ["Where the line starts","Sales at origin; cost at the fixed cost",
   "At the <b>loss equal to the fixed cost</b>, below the axis"],
  ["Where the BEP appears","Where the two lines cross",
   "Where the single line <b>crosses the horizontal axis</b>"],
  ["Its advantage","Shows sales, cost and volume together",
   "Much clearer for reading profit at any volume"]], headcls="lite",
 widths=["18%","41%","41%"])}
{bullets([
 'To draw it you need only <b>two points</b>: the loss at zero sales, which equals the fixed cost of ' +
 R + '1,500 (plotted <i>below</i> the axis), and the profit at the given sales of ' + R + '7,500, '
 'which is ' + R + '1,500 above it. Join them with a straight line.',
 'Where the line cuts the horizontal axis is the break-even point.'])}"""

    wnh = f"""<h4 class="mini">W1 &nbsp;The figures behind the graph</h4>
{table(None, [("Particulars",""),("Amount " + R,"r"),("Per unit " + R,"r")],
 [["Sales &nbsp;<span class='src' style='display:inline'>3,000 units</span>","7,500","2.50"],
  ["<i>Less:</i> Variable cost","(4,500)","(1.50)"],
  {"cls":"sub","cells":["<b>Contribution</b>","<b>3,000</b>","<b>1.00</b>"]},
  ["<i>Less:</i> Fixed cost","(1,500)","&mdash;"],
  {"cls":"tot","cells":["<b>Profit</b>","<b>1,500</b>","&mdash;"]}], headcls="lite")}
{fml("P/V ratio &nbsp;=&nbsp; " + frac("Contribution", "Sales") + " &times; 100 &nbsp;=&nbsp; "
     + frac("3,000", "7,500") + " &times; 100 &nbsp;=&nbsp; <b>40%</b>")}
{calc(['BEP (units) &nbsp;=&nbsp; ' + frac("1,500", "1.00") + ' &nbsp;=&nbsp; <b>1,500 units</b>',
       f'BEP (value) &nbsp;=&nbsp; ' + frac("1,500", "0.40") + f' &nbsp;=&nbsp; <b>{R}3,750</b> '
       '&nbsp;(= 1,500 units &times; ' + R + '2.50 &#10003;)',
       f'Margin of safety &nbsp;=&nbsp; 7,500 &minus; 3,750 &nbsp;=&nbsp; <b>{R}3,750</b>'])}

<h4 class="mini">W2 &nbsp;The two points to plot</h4>
{table(None, [("Point",""),("Sales " + R,"r"),("Profit / (Loss) " + R,"r"),("Meaning","")],
 [["Start","Nil","(1,500)","At zero sales the loss is the whole fixed cost"],
  ["<b>Crossing</b>","<b>3,750</b>","<b>Nil</b>","<b>Break-even point</b>"],
  ["End","7,500","1,500","The actual position given in the question"]], headcls="lite")}"""

    # PV graph SVG
    W, H = 470, 210
    L, B, T, Rr = 56, 32, 16, 16
    pw, ph = W - L - Rr, H - B - T
    xmax = 8000
    ymax, ymin = 2000, -2000
    def X(v): return L + (v / xmax) * pw
    def Y(v): return T + ph * (ymax - v) / (ymax - ymin)
    g = [f'<div class="dia"><svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         'xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans">']
    for val in (2000, 1000, 0, -1000, -2000):
        gy = Y(val)
        g.append(f'<line x1="{L}" y1="{gy:.1f}" x2="{L+pw}" y2="{gy:.1f}" '
                 f'stroke="{"#333" if val==0 else "#e4e4e4"}" '
                 f'stroke-width="{1.0 if val==0 else 0.6}"/>')
        g.append(f'<text x="{L-4}" y="{gy+2.6:.1f}" font-size="6.6" fill="#777" '
                 f'text-anchor="end">{val:,}</text>')
    for v in (2000, 4000, 6000, 8000):
        g.append(f'<text x="{X(v):.1f}" y="{Y(0)+11:.1f}" font-size="6.6" fill="#777" '
                 f'text-anchor="middle">{v:,}</text>')
    g.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{T+ph}" stroke="#333" stroke-width="1"/>')
    # loss / profit shading labels
    g.append(f'<text x="{L+30}" y="{Y(-1400):.1f}" font-size="7" fill="#c0392b">LOSS</text>')
    g.append(f'<text x="{L+pw-60}" y="{Y(900):.1f}" font-size="7" fill="#1e7a37">PROFIT</text>')
    # the profit line
    g.append(f'<line x1="{X(0):.1f}" y1="{Y(-1500):.1f}" x2="{X(7500):.1f}" y2="{Y(1500):.1f}" '
             'stroke="#5b4a9e" stroke-width="1.8"/>')
    g.append(f'<circle cx="{X(0):.1f}" cy="{Y(-1500):.1f}" r="2.6" fill="#5b4a9e"/>')
    g.append(f'<circle cx="{X(7500):.1f}" cy="{Y(1500):.1f}" r="2.6" fill="#5b4a9e"/>')
    g.append(f'<text x="{X(0)+5:.1f}" y="{Y(-1500)+11:.1f}" font-size="6.8" fill="#5b4a9e">'
             f'loss = fixed cost {R}1,500</text>')
    g.append(f'<text x="{X(7500)-4:.1f}" y="{Y(1500)-5:.1f}" font-size="6.8" fill="#5b4a9e" '
             f'text-anchor="end">profit {R}1,500</text>')
    # BEP
    g.append(f'<circle cx="{X(3750):.1f}" cy="{Y(0):.1f}" r="3.6" fill="none" stroke="#10314f" '
             'stroke-width="1.7"/>')
    g.append(f'<line x1="{X(3750):.1f}" y1="{Y(0):.1f}" x2="{X(3750):.1f}" y2="{Y(-1900):.1f}" '
             'stroke="#10314f" stroke-width="0.7" stroke-dasharray="2,2"/>')
    g.append(f'<text x="{X(3750):.1f}" y="{Y(-1900)+9:.1f}" font-size="7.2" fill="#10314f" '
             f'text-anchor="middle" font-weight="bold">BEP {R}3,750</text>')
    g.append(f'<text x="{L+pw/2:.1f}" y="{H-3}" font-size="7.2" fill="#333" text-anchor="middle">'
             f'Sales ({R})</text>')
    g.append(f'<text x="12" y="{T+ph/2:.1f}" font-size="7.2" fill="#333" text-anchor="middle" '
             f'transform="rotate(-90 12 {T+ph/2:.1f})">Profit / (Loss) ({R})</text>')
    g.append('</svg><div class="cap">Profit&ndash;volume graph. One line only. It starts at a loss '
             'equal to the fixed cost and crosses the axis at the break-even point of '
             + R + '3,750.</div></div>')
    graph = "".join(g)

    return ("<div class='prob long'>"
            + prob_head("Q18", "Profit&ndash;volume graph", "Charts &middot; p.36&ndash;37")
            + question(q) + read(rd) + wn(wnh) + graph
            + trap(bullets([
                'Drawing a break-even chart instead. A P/V graph has <b>one line</b> and the axis '
                'runs below zero.',
                'Starting the line at the origin. At zero sales you are losing the fixed cost, so '
                'the line starts <b>below</b> the axis at ' + R + '1,500.',
                'Forgetting to state the P/V ratio. The question asks for it explicitly &mdash; it is '
                'the <b>slope</b> of the line, 40%.']))
            + ans([("Contribution / contribution per unit", f"{R} 3,000 / {R} 1.00"),
                   ("<b>P/V ratio</b>", "<b>40%</b>"),
                   ("Break-even point", f"1,500 units = {R} 3,750"),
                   ("Margin of safety", f"{R} 3,750 (50% of sales)"),
                   ("Profit at the given sales", f"{R} 1,500"),
                   ("Two points plotted", f"(0, &minus;{R} 1,500) and ({R} 7,500, +{R} 1,500)")])
            + "</div>")


# ======================================================================
def build():
    return (opener()
            + q1() + q2() + q3() + q4() + q5() + q6()
            + keyfactor_playbook() + q7() + q8() + q9() + q10() + q11()
            + shutdown_playbook() + q12() + q13() + q14()
            + q15() + q16() + q17() + q18())
