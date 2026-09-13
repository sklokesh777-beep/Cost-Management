# -*- coding: utf-8 -*-
"""MODULE 4 - RELEVANT COSTING  (15 problems)"""
from build import (esc, rs, money, frac, prob_head, question, read, method, wn,
                   trap, why, steps, bullets, fml, calc, ans, table, src,
                   arrow_panel, module_opener)

R = "&#8377;"
D = "$"


# ----------------------------------------------------------------------
# THE signature Module 4 table:  Particulars | Nature & computation | Amt
# ----------------------------------------------------------------------
def rc(caption, rows, total=None, cur=None, note=None):
    """
    rows  : list of (particulars, nature_and_computation, amount)
            amount may be a number, a pre-formatted string, or None (blank).
            Prefix particulars with '!' to mark an IRRELEVANT row (greyed).
    total : (label, amount) drawn as the double-ruled total line.
    """
    cur = cur or R
    head = [("Particulars", ""), ("Nature and computation", ""),
            (f"Amount ({cur})", "r")]
    body = []
    for p, nat, amt in rows:
        cls = ""
        if p.startswith("!"):
            p, cls = p[1:], "irr"
        val = "Nil" if amt == 0 else (money(amt) if not isinstance(amt, str) else amt)
        body.append({"cls": cls,
                     "cells": [f"<b>{p}</b>", nat, (val, "r")]})
    if total:
        lab, amt = total
        body.append({"cls": "tot",
                     "cells": [f"<b>{lab}</b>", "",
                               (f"<b>{money(amt) if not isinstance(amt,str) else amt}</b>", "r")]})
    t = table(caption, head, body, widths=["21%", "60%", "19%"])
    if note:
        t += f"<div class='small'>{note}</div>"
    return t


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
# decision trees
# ----------------------------------------------------------------------
NAVY, RED, GREEN, GREY = "#10314f", "#c0392b", "#1e7a37", "#777"
FILL_Q, FILL_B, FILL_O = "#eaf1f8", "#ffffff", "#eaf6ee"


def _tree(title_box, q1_box, left_lab, right_lab, out1, q2_box,
          q2_left_lab, q2_right_lab, out2, out3, caption, h=214):
    """
    Generic two-question decision tree used for materials and for labour.
    Geometry is fixed so both trees look identical on the page.
    """
    items = [
        {"box": (200, 6, 100, 22, title_box, "#10314f"), "fg": "#ffffff", "fs": 9.4},
        {"box": (150, 44, 200, 22, q1_box, FILL_Q), "fs": 8.6},
        {"box": (56, 88, 108, 20, left_lab, FILL_B), "fs": 8.2},
        {"box": (336, 88, 108, 20, right_lab, FILL_B), "fs": 8.2},
        {"box": (34, 126, 152, 44, out1, FILL_O), "stroke": GREEN, "fg": NAVY, "fs": 8.2},
        {"box": (296, 122, 190, 22, q2_box, FILL_Q), "fs": 8.6},
        {"box": (232, 164, 116, 42, out2, FILL_O), "stroke": GREEN, "fg": NAVY, "fs": 8.0},
        {"box": (364, 164, 130, 42, out3, FILL_O), "stroke": GREEN, "fg": NAVY, "fs": 8.0},
        # connectors
        {"line": (250, 28, 250, 42), "col": NAVY},
        {"line": (250, 66, 112, 86), "col": NAVY},
        {"line": (250, 66, 388, 86), "col": NAVY},
        {"line": (110, 108, 110, 124), "col": NAVY},
        {"line": (390, 108, 390, 120), "col": NAVY},
        {"line": (390, 144, 292, 162), "col": NAVY},
        {"line": (390, 144, 428, 162), "col": NAVY},
        # placed at the midpoint of each diagonal connector, clear of the boxes below
        {"txt": (330, 152, q2_left_lab, 7.4, RED, "middle")},
        {"txt": (420, 152, q2_right_lab, 7.4, RED, "middle")},
    ]
    return arrow_panel(500, h, items, caption)


def tree_materials():
    return _tree(
        "MATERIAL",
        "Is the material already in STOCK?",
        "NO &mdash; must be bought",
        "YES &mdash; lying in stock",
        "&#9312; RELEVANT COST =|Replacement / purchase|price (out-of-pocket)",
        "Is it used REGULARLY in production?",
        "YES", "NO",
        "&#9313; RELEVANT =|Replacement|cost|(it gets replaced)",
        "&#9314; RELEVANT =|Opportunity cost|= HIGHER of NRV or|saving as a substitute",
        "Decision tree for MATERIAL. Every material row in every problem of this module lands in "
        "one of the three boxes &#9312; &#9313; &#9314;.")


def tree_labour():
    return _tree(
        "LABOUR",
        "Is spare labour capacity available?",
        "NO &mdash; must hire",
        "YES &mdash; already on payroll",
        "&#9312; RELEVANT COST =|Wages of the extra|labour hired (out-of-pocket)",
        "Is that labour in SHORT supply?",
        "YES", "NO",
        "&#9313; RELEVANT =|Wages PLUS|contribution|forgone elsewhere",
        "&#9314; RELEVANT = NIL|Committed cost &mdash;|paid anyway, so|irrelevant",
        "Decision tree for LABOUR. Box &#9314; is the one students miss: permanent staff who are "
        "simply re-deployed cost the decision nothing.")


# ----------------------------------------------------------------------
def opener():
    intro = f"""
<h2 class="sec">What Module 4 is really about</h2>
<p>Modules 2 and 3 gave you a cost sheet and asked for a decision. Module 4 does something harder and
more useful: it hands you a cost sheet that is <b>deliberately misleading</b> and asks you to throw
most of it away.</p>
<p>Every figure printed in a Module 4 question is there for one of two reasons &mdash; either it
changes because of the decision, or it is a decoy. Your entire job is to sort them.</p>

<div class="blk read"><span class="lab">The one test that decides every figure in this module</span>
{fml("Will this amount be DIFFERENT if I say yes rather than no?",
     "If yes, it is relevant &mdash; bring it in. If no, it is irrelevant &mdash; strike it out. "
     "Nothing else matters: not whether it is large, not whether it appears in the cost sheet, "
     "not whether the accountant has charged it to the job.")}
<p>Two consequences follow, and between them they explain almost every mark in this module:</p>
{bullets([
 '<b>Money already spent can never be relevant.</b> It is gone. Book value, original cost, the cost '
 'of goods already manufactured &mdash; all sunk, all struck out. This feels wrong the first time, '
 'because the amounts are usually the biggest on the page. That is exactly why they are printed.',
 '<b>Money not spent can still be relevant.</b> If accepting the job means giving up a sale, a '
 'hire charge, or a saving, that sacrifice is a real cost of the job. This is <b>opportunity '
 'cost</b>, and it is the single most heavily examined idea in Module 4.'])}
</div>

<h2 class="sec" style="margin-top:6mm">The two decision trees &mdash; learn these and the module is done</h2>
<p>Nearly every line item you will be asked to classify is either a material or a labour cost. There
is one tree for each. Walk the tree, land in a box, write that box&rsquo;s rule in the
&ldquo;Nature and computation&rdquo; column. That is the whole method.</p>
{tree_materials()}
{tree_labour()}

<h2 class="sec" style="margin-top:6mm">Everything else, in one table</h2>
{table(None, [("Item in the question", ""), ("Relevant?", "c"), ("Why", "")],
 [["Original cost / purchase price already paid", "<b class='no'>NO</b>",
   "Sunk. The cash has left. Nothing you decide now can bring it back."],
  ["Book value, written-down value, net book value", "<b class='no'>NO</b>",
   "An accounting record of a sunk cost. It is not a cash flow and not a sacrifice."],
  ["Depreciation", "<b class='no'>NO</b>",
   "Non-cash, and merely the sunk cost spread over years. <i>Exception:</i> tax saved on "
   "depreciation is a real cash flow and is relevant."],
  ["Apportioned / allocated / absorbed overhead", "<b class='no'>NO</b>",
   "An internal book-keeping share of a cost the firm incurs anyway. Look for the words "
   "&ldquo;allocated&rdquo;, &ldquo;apportioned&rdquo;, &ldquo;charged at &hellip;% of labour&rdquo;."],
  ["General fixed cost, absorbed at a normal rate", "<b class='no'>NO</b>",
   "Unchanged by the decision."],
  ["<b>Specific</b> or <b>incremental</b> fixed cost", "<b class='yes'>YES</b>",
   "A fixed cost caused <i>by this decision alone</i> &mdash; a machine bought for this job, an "
   "extra supervisor, a rented warehouse. It changes, so it counts."],
  ["Variable / out-of-pocket cost of doing the job", "<b class='yes'>YES</b>",
   "Fresh cash outflow caused by saying yes."],
  ["Realisable value given up (NRV)", "<b class='yes'>YES</b>",
   "You could have sold it. Using it on the job sacrifices that money."],
  ["Contribution / hire charge / saving forgone", "<b class='yes'>YES</b>",
   "Opportunity cost. The best alternative you gave up."],
  ["Residual or scrap value at the end", "<b class='yes'>YES</b>",
   "A cash inflow caused by the decision &mdash; net it off the cost."]],
 headcls="lite", widths=["30%", "13%", "57%"])}

<h2 class="sec" style="margin-top:6mm">The five problem types in this module</h2>
{table(None, [("Type", ""), ("The question sounds like &hellip;", ""), ("What you produce", ""),
              ("Problems", "c")],
 [["<b>1. Relevant cost of materials</b>",
   "A table of book value, realisable value and replacement cost for materials A, B, C, D.",
   "One <i>Nature and computation</i> row per material, walking the material tree.",
   "<b>2, 10</b>"],
  ["<b>2. Relevant cost of a machine or asset</b>",
   "&ldquo;Bought 4 years ago for &hellip; now has a book value of &hellip; could be sold for &hellip;&rdquo;",
   "Out-of-pocket running cost <b>plus</b> the fall in resale value as opportunity cost.",
   "<b>3, 4, 8, 12</b>"],
  ["<b>3. Minimum price / accept-or-reject</b>",
   "&ldquo;Estimate the minimum price so the company is not worse off.&rdquo;",
   "Total relevant cost. That total <i>is</i> the minimum price.",
   "<b>7, 14, 15</b>"],
  ["<b>4. Make or buy, with an alternative use</b>",
   "&ldquo;&hellip; or the machine can be hired out at &hellip;&rdquo;",
   "A column per alternative; pick the lowest <i>net</i> relevant cost.",
   "<b>6, 13</b>"],
  ["<b>5. Further processing / rectification</b>",
   "&ldquo;Rejected because of defects &hellip; if rectified by spending &hellip;&rdquo;",
   "Incremental revenue against incremental cost. The manufacturing cost is sunk.",
   "<b>9, 11</b>"],
  ["<b>6. Opportunity cost of choosing one product</b>",
   "&ldquo;Compute the opportunity cost for each of the products.&rdquo;",
   "Contribution of the <b>best forgone</b> alternative, product by product.",
   "<b>1, 5</b>"]],
 headcls="lite", widths=["22%", "31%", "33%", "14%"])}

<div class="blk trap"><span class="lab">The trap / where marks are lost</span>
{bullets([
 '<b>Answering with the total cost instead of the relevant cost.</b> If you find yourself using '
 'every number in the question, you have almost certainly made a mistake &mdash; Module 4 questions '
 'always contain decoys.',
 '<b>Leaving the &ldquo;Nature and computation&rdquo; column blank.</b> In this module the '
 '<i>reasoning</i> carries most of the marks. A bare figure of ' + R + '1,750 earns little; '
 '&ldquo;no other use, so opportunity cost at realisable value 700 &times; ' + R + '2.50&rdquo; '
 'earns full marks.',
 '<b>Forgetting to state the decision.</b> Every problem ends with a recommendation in words. '
 'Write it, and give the amount by which one option beats the other.',
 '<b>Taking the lower of two opportunity costs.</b> When a material has two possible alternative '
 'uses, the sacrifice is the <b>better</b> one you gave up &mdash; so take the HIGHER. This is '
 'Q2 material D, and it is worth a mark on its own.'])}
</div>
"""
    return module_opener("Module 4", "Relevant Costing",
                         "15 problems &middot; workbook pages 39&ndash;44", intro)



# ======================================================================
# Q1
# ======================================================================
def q1():
    q = f"""<p>I travel from HSR to Hebbal, twenty-five kilometres from my house, for my regular work,
spending {R}250 per day. On the way I pick up my employee Mr. M from Marathahalli, which is 5
kilometres from HSR. What is the cost of the pick-up of my employee Mr. M?</p>"""

    rd = f"""<p>This looks like a trick question and it is &mdash; but the trick is the whole point of
the module. Read it twice and one phrase decides everything.</p>
{bullets([
 '<b>&ldquo;On the way&rdquo;</b> &mdash; these three words are the answer. Marathahalli lies on a '
 'journey that is already being made. No extra kilometre is driven.',
 '<b>&ldquo;for my regular work&rdquo;</b> &mdash; the trip happens whether or not Mr. M is picked '
 'up. The ' + R + '250 is therefore <b>committed</b>, and unchanged by the decision.',
 'The 25 km and the 5 km are given only so that you can confirm the pick-up point is <i>en '
 'route</i>. They are not there to be apportioned.',
 'Apply the test: <i>will the ' + R + '250 be different if I stop picking him up?</i> No. '
 'Therefore it is irrelevant.'])}"""

    tbl = rc("Computation of the relevant cost of picking up Mr. M",
      [("Daily travel cost",
        f"{R}250 per day is incurred for the proprietor&rsquo;s own regular work. It is a "
        f"<b>committed cost</b> &mdash; it does not change whether or not Mr. M is picked up. "
        f"{src('given ' + R + '250 &mdash; sunk / committed')}", 0),
       ("!Apportionment on distance",
        f"The tempting answer is {R}250 &times; {frac('5', '25')} = {R}50. This is <b>wrong</b>. "
        f"Apportioning a committed cost does not make it relevant &mdash; the total cash paid is "
        f"still {R}250 either way. {src('a decoy &mdash; do not use')}", "&mdash;"),
       ("Additional distance travelled",
        "Marathahalli is <b>on the way</b>, so no extra kilometre is covered and no extra fuel, "
        "toll or time is incurred.", 0)],
      total=("Total relevant cost of the pick-up", "NIL"))

    return ("<div class='prob'>"
            + prob_head("Q1", "Relevant cost when nothing changes", "Opportunity cost &middot; p.39")
            + question(q) + read(rd) + tbl
            + why(f"""<p>Relevant cost is about <b>the difference between two futures</b> &mdash; one
where you pick him up and one where you do not. Those two futures cost exactly the same
{R}250. The difference is zero, so the relevant cost is zero.</p>
<p><b>Now change one word and the answer changes completely.</b> Suppose Marathahalli were <i>5 km
off</i> the route instead of on it. Then the decision causes 10 extra kilometres a day (there and
back), and the running cost of those 10 km <i>would</i> be relevant. This is the examiner&rsquo;s
favourite variation, so read the words &ldquo;on the way&rdquo; carefully every time.</p>""")
            + ans([("Cost of picking up Mr. M", "<b>NIL</b>"),
                   (f"Why the {R}250 is excluded",
                    "Committed cost &mdash; unchanged by the decision"),
                   (f"Why {R}50 is <i>not</i> the answer",
                    "Apportioning a sunk cost does not create a relevant cost")])
            + "</div>")


# ======================================================================
# Q2
# ======================================================================
def q2():
    q = f"""<p>ABC Ltd. has been approached by a customer who would like a special job to be done for
him, and who is willing to pay {R}22,000 for it. The job would require the following materials:</p>
{table(None, [("Material", "c"), ("Total units required", "r"), ("Units already in stock", "r"),
              ("Book value of units in stock", "r"), ("Realisable value", "r"),
              ("Replacement cost", "r")],
 [["<b>A</b>", "1,000", "0", "&mdash;", "&mdash;", f"{R}6 p.u."],
  ["<b>B</b>", "1,000", "600", f"{R}2 p.u.", f"{R}2.50 p.u.", f"{R}5 p.u."],
  ["<b>C</b>", "1,000", "700", f"{R}3 p.u.", f"{R}2.50 p.u.", f"{R}4 p.u."],
  ["<b>D</b>", "200", "200", f"{R}4 p.u.", f"{R}6.00 p.u.", f"{R}9 p.u."]], headcls="lite")}
<p>Material B is used regularly by ABC Ltd. and if units of B are used for this job, they would need
to be replaced to meet other production demand.</p>
<p>Materials C and D are in stock as the result of previous over-buying and they have a restricted
use. No other use could be found for material C, but the units of material D could be used in another
job as a substitute for 300 units of material E, which currently costs {R}5 per unit (of which the
company has no units in stock at the moment).</p>
<p>Compute the relevant costs of materials for deciding whether or not to accept the offer.</p>"""

    rd = f"""<p>Five columns of figures are given and <b>only one of them is used for each
material</b>. Book value is never used. Walk the material tree once per material.</p>
{bullets([
 '<b>Material A</b> &mdash; nothing in stock, so all 1,000 units must be bought. Box &#9312;: '
 'replacement cost.',
 '<b>Material B</b> &mdash; the words <i>&ldquo;used regularly &hellip; would need to be '
 'replaced&rdquo;</i> put this in box &#9313;. Take replacement cost on the <b>full 1,000 '
 'units</b>, not on the 400 short. Using stock triggers a purchase to refill it, so the cash '
 'outflow is the same as buying all 1,000.',
 '<b>Material C</b> &mdash; <i>&ldquo;no other use could be found&rdquo;</i> means the 700 in '
 'stock are in box &#9314;, and the only sacrifice is the scrap sale at ' + R + '2.50. The 300 '
 'short are in box &#9312; at replacement cost. <b>Two rows for one material.</b>',
 '<b>Material D</b> &mdash; box &#9314; again, but there are now <b>two</b> alternative uses: sell '
 'it, or substitute it for material E. Value both and take the <b>higher</b>.',
 'Note the quantities in the D substitution: 200 units of D replace <b>300</b> units of E. Use 300, '
 'not 200. The workbook changes the quantity deliberately.'])}"""

    d_wn = f"""<h4 class="mini">W1 &nbsp;Material D &mdash; valuing the two alternative uses</h4>
<p class="small">D is in stock, not regularly used, and has two possible fates if it is not used on
this job. The relevant cost is whichever benefit is <b>larger</b>, because that is what is actually
being sacrificed.</p>
{table(None, [("Alternative use of the 200 units of D", ""), ("Computation", ""),
              ("Benefit forgone", "r")],
 [["Sell it at its realisable value", f"200 units &times; {R}6.00", f"{R}1,200"],
  {"cls": "sub",
   "cells": ["Use it on another job in place of material E, which would otherwise have to be bought",
             f"300 units of E &times; {R}5.00", f"<b>{R}1,500</b>"]},
  {"cls": "tot",
   "cells": ["<b>Relevant cost = the HIGHER of the two</b>",
             "the larger benefit is the one truly given up", f"<b>{R}1,500</b>"]}],
 headcls="lite", widths=["52%", "28%", "20%"])}
<p class="small"><b>Why the higher figure?</b> A rational company would have chosen the best available
alternative. By taking D for this job you deprive it of {R}1,500, not {R}1,200. Taking the lower
figure is a standard one-mark error.</p>"""

    tbl = rc("Calculation of the relevant cost of materials for the special order",
      [("Material A",
        f"1,000 units to be purchased. Nothing is in stock, so the whole quantity is a fresh cash "
        f"outflow &mdash; out-of-pocket cost at the replacement price. "
        f"{src('1,000 units &times; ' + R + '6 &nbsp;&larr;&nbsp; replacement cost column')}", 6000),
       ("Material B",
        f"Used regularly, so the 600 units drawn from stock must be bought back. Replacement cost is "
        f"relevant on the <b>full</b> 1,000 units. "
        f"{src('1,000 units &times; ' + R + '5 &nbsp;&larr;&nbsp; replacement cost column')}", 5000),
       ("Material C<br/><span class='small'>&mdash; 700 in stock</span>",
        f"In stock, not regularly used and no other use exists. It will not be replaced, so the only "
        f"sacrifice is the scrap proceeds &mdash; opportunity cost at net realisable value. "
        f"{src('700 units &times; ' + R + '2.50 &nbsp;&larr;&nbsp; realisable value column')}", 1750),
       ("Material C<br/><span class='small'>&mdash; 300 short</span>",
        f"The balance of 300 units must be bought. Out-of-pocket cost at the replacement price. "
        f"{src('300 units &times; ' + R + '4 &nbsp;&larr;&nbsp; replacement cost column')}", 1200),
       ("Material D",
        f"In stock, not regularly used, but it has two alternative uses. Sell at NRV = {R}1,200; or "
        f"substitute for 300 units of E = {R}1,500. The <b>higher</b> opportunity cost is relevant. "
        f"{src('W1 &nbsp;&larr;&nbsp; higher of ' + R + '1,200 and ' + R + '1,500')}", 1500),
       ("!Book value of stock",
        f"{R}2, {R}3 and {R}4 per unit are historical costs already paid. Sunk, and never relevant.",
        "&mdash;")],
      total=("Total relevant cost of materials", 15450))

    dec = stmt("Decision", ["Amount " + R],
      [("Price the customer is willing to pay", ["22,000"]),
       ("<i>Less:</i> Total relevant cost of materials " + src("from the statement above"),
        ["(15,450)"]),
       ("<b>Net benefit from accepting the job</b>", ["<b>6,550</b>"], "tot")])

    return ("<div class='prob long'>"
            + prob_head("Q2", "Relevant cost of materials &mdash; the full four-material case",
                        "Materials &middot; p.39")
            + question(q) + read(rd) + tbl + wn(d_wn) + dec
            + why(f"""<p>Notice that the answer used the <b>replacement cost</b> column for A and B,
the <b>realisable value</b> column for C, and <b>neither</b> column for D &mdash; and never once used
book value. That is the whole discipline of relevant costing: the right column depends on what
happens next, not on what the accountant recorded.</p>
<p>The logic behind each choice is always the same question: <i>what does the company actually lose by
putting this material into this job?</i></p>
{bullets([
 'For A and B it loses <b>cash</b>, because a purchase is triggered. Replacement cost.',
 'For C it loses a <b>scrap sale</b>, because nothing else will ever use it. Realisable value.',
 'For D it loses <b>the best of its alternatives</b>, which happens to be a saving rather than a '
 'sale. Higher of the two.'])}
<p><b>Recommendation:</b> accept the order. It brings in {R}22,000 against a relevant material cost
of {R}15,450, a surplus of {R}6,550 &mdash; <i>provided</i> labour and overheads are unaffected, which
is the assumption the question invites by giving no labour data.</p>""")
            + ans([("Material A", f"{R} 6,000"),
                   ("Material B", f"{R} 5,000"),
                   ("Material C &nbsp;(1,750 + 1,200)", f"{R} 2,950"),
                   ("Material D", f"{R} 1,500"),
                   ("<b>Total relevant cost of materials</b>", f"<b>{R} 15,450</b>"),
                   ("<b>Decision</b>",
                    f"<b>ACCEPT &mdash; surplus of {R} 6,550</b>")])
            + "</div>")


# ======================================================================
# Q3
# ======================================================================
def q3():
    q = f"""<p>ABC Ltd. is tendering for a six-month contract which would require the use of a
specialised machine. The machine was purchased 4 years ago for {R}90,000 and now has a net book value
of {R}35,000. The company was about to sell the machine for {R}40,000, but if they used it on this
contract, they can sell it after 6 months for {R}25,000. The variable cost of operating the machine
for 6 months would be {R}60,000. Ignoring interest costs, identify the relevant cost of using the
machine on the contract.</p>"""

    rd = f"""<p>Four amounts are given. <b>Two are decoys.</b> Sort them before writing anything.</p>
{table(None, [("Figure in the question", ""), ("Relevant?", "c"), ("Reason", "")],
 [[f"{R}90,000 &mdash; purchased 4 years ago", "<b class='no'>NO</b>",
   "Sunk. Paid four years ago; nothing decided today can change it."],
  [f"{R}35,000 &mdash; net book value", "<b class='no'>NO</b>",
   "A book record of that sunk cost. Not cash, not a sacrifice."],
  [f"{R}60,000 &mdash; variable operating cost", "<b class='yes'>YES</b>",
   "Fresh cash outflow, caused only by taking the contract."],
  [f"{R}40,000 now vs {R}25,000 later", "<b class='yes'>YES</b>",
   "Using the machine delays the sale and destroys " + R + "15,000 of resale value. That fall is "
   "the opportunity cost."]], headcls="lite", widths=["34%", "13%", "53%"])}
{bullets([
 '<b>The trap is to write ' + R + '25,000 as the opportunity cost.</b> It is not. The company still '
 'gets that ' + R + '25,000 &mdash; only six months later. What it <b>loses</b> is the difference, ' +
 R + '40,000 &minus; ' + R + '25,000.',
 '&ldquo;Ignoring interest costs&rdquo; is the examiner telling you not to discount the delayed '
 'receipt. Without that instruction you would also have to charge for six months of lost interest.'])}"""

    tbl = rc("Computation of the relevant cost of the machine",
      [("Variable operating cost",
        f"Cash spent only because the contract is taken. Out-of-pocket cost, therefore relevant. "
        f"{src('given, for the 6-month contract')}", 60000),
       ("Reduction in net realisable value",
        f"The machine could be sold today for {R}40,000. If it is used on the contract it can only "
        f"be sold for {R}25,000 in six months&rsquo; time. The {R}15,000 of resale value destroyed "
        f"by using the machine is an <b>opportunity cost</b> and is relevant. "
        f"{src(R + '40,000 &minus; ' + R + '25,000')}", 15000),
       ("!Original cost of the machine",
        f"{R}90,000 was paid four years ago. Sunk cost &mdash; irrelevant.", "&mdash;"),
       ("!Net book value",
        f"{R}35,000 is an accounting figure derived from that sunk cost. It is neither a cash flow "
        f"nor a sacrifice &mdash; irrelevant.", "&mdash;")],
      total=("Total relevant cost of using the machine", 75000))

    return ("<div class='prob'>"
            + prob_head("Q3", "Relevant cost of a machine already owned",
                        "Machine &middot; p.39&ndash;40")
            + question(q) + read(rd) + tbl
            + why(f"""<p>Compare the two futures side by side and the {R}75,000 falls out on its
own:</p>
{table(None, [("", ""), ("Do NOT take the contract " + R, "r"), ("Take the contract " + R, "r")],
 [["Sell the machine", "40,000 (today)", "25,000 (in 6 months)"],
  ["Operating cost of the machine", "&mdash;", "(60,000)"],
  {"cls": "tot", "cells": ["<b>Net cash from the machine</b>", "<b>40,000</b>", "<b>(35,000)</b>"]},
  {"cls": "sub", "cells": ["<b>Difference &mdash; the relevant cost</b>", "",
                           "<b>75,000</b>"]}], headcls="lite")}
<p>The {R}90,000 and the {R}35,000 appear nowhere in that comparison, which is precisely why they are
irrelevant. They are identical in both columns, so they cannot influence the choice.</p>
<p><b>How to use the answer:</b> {R}75,000 is the floor for the tender. Any price above {R}75,000
(plus the contract&rsquo;s other relevant costs) leaves the company better off than selling the
machine today and walking away.</p>""")
            + ans([("Variable operating cost", f"{R} 60,000"),
                   (f"Opportunity cost &mdash; fall in resale value", f"{R} 15,000"),
                   ("<b>Total relevant cost of the machine</b>", f"<b>{R} 75,000</b>"),
                   ("Excluded as sunk",
                    f"{R} 90,000 original cost &middot; {R} 35,000 NBV")])
            + "</div>")


# ======================================================================
# Q4
# ======================================================================
def q4():
    q = f"""<p>Noida Camera Company has received a special order for photographic equipment it does not
normally produce. The company has excess capacity, and the order could be manufactured without
reducing production of the firm&rsquo;s regular products. Discuss the relevance of each of the
following items in computing the cost of the special order:</p>
<p><b>(a)</b> Equipment to be used in producing the order has a book value of {R}2,000. The equipment
has no other use for Noida Camera Company. If the order is not accepted, the equipment will be sold
for {R}1,500. If the equipment is used in producing the order, it can be sold in three months for
{R}800.</p>
<p><b>(b)</b> If the special order is accepted, the operation will require some of the storage space
in the company&rsquo;s plant. If the space is used for this purpose, the company will rent storage
space temporarily in a nearby warehouse at a cost of {R}18,000. The building depreciation allocated to
the storage space to be used in producing the special order is {R}12,000.</p>
<p><b>(c)</b> If the special order is accepted, it will require a sub-assembly. Noida Camera can
purchase the sub-assembly for {R}24 per unit from outside, or make it for {R}30 per unit. The {R}30
per unit was determined as follows:</p>
{table(None, [("Particulars", ""), ("" + R, "r")],
 [["Direct material", "10.00"], ["Direct labour", "6.00"], ["Variable overheads", "6.00"],
  ["Apportioned fixed overhead", "8.00"],
  {"cls": "tot", "cells": ["<b>Total unit cost of sub-assembly</b>", "<b>30.00</b>"]}],
 headcls="lite", widths=["76%", "24%"])}"""

    rd = f"""<p>The word <b>&ldquo;discuss&rdquo;</b> tells you the marks are in the reasoning, not
the arithmetic. Answer each part with a classification and a figure.</p>
{bullets([
 '<b>&ldquo;The company has excess capacity&rdquo;</b> &mdash; the standard signal that no existing '
 'contribution is sacrificed. Without it, part (c) would need an opportunity cost too.',
 '<b>Part (a) is Q3 again in miniature.</b> Book value ' + R + '2,000 is sunk. The relevant amount '
 'is the <b>fall</b> in resale value, ' + R + '1,500 &minus; ' + R + '800.',
 '<b>Part (b) pairs a real cost with a fake one on purpose.</b> The ' + R + '18,000 warehouse rent '
 'is new cash caused by the order. The ' + R + '12,000 depreciation is allocated, non-cash, and '
 'incurred whether or not the order is taken.',
 '<b>Part (c) is a make-or-buy.</b> Strip the apportioned fixed overhead of ' + R + '8 out of the ' +
 R + '30 before comparing with the ' + R + '24 buying price. That single step reverses the '
 'decision, which is exactly why the question is set.'])}"""

    a_tbl = rc("(a) Equipment",
      [("Equipment",
        f"Reduction in net realisable value is an <b>opportunity cost</b> and is relevant: the "
        f"equipment could be sold for {R}1,500 today, but only for {R}800 after being used on the "
        f"order. {src(R + '1,500 &minus; ' + R + '800')}", 700),
       ("!Book value of equipment",
        f"{R}2,000 is a sunk historical cost. Irrelevant.", "&mdash;")],
      total=("Relevant cost of the equipment", 700))

    b_tbl = rc("(b) Storage space",
      [("Storage &mdash; warehouse rent",
        f"Additional rent that will be paid only if the order is accepted. An <b>out-of-pocket "
        f"cost</b>, therefore relevant. {src('given &mdash; new cash outflow')}", 18000),
       ("!Building depreciation allocated",
        f"{R}12,000 is a non-cash allocation of the cost of a building the company already owns. It "
        f"will be charged whether or not the order is accepted. Irrelevant.", "&mdash;")],
      total=("Relevant cost of storage space", 18000))

    c_tbl = table("(c) Sub-assembly &mdash; make or buy, per unit",
      [("Particulars", ""), ("Nature", ""), ("Make " + R, "r")],
      [["Direct material", "Variable &mdash; relevant", "10.00"],
       ["Direct labour", "Variable &mdash; relevant", "6.00"],
       ["Variable overheads", "Variable &mdash; relevant", "6.00"],
       {"cls": "irr",
        "cells": ["<b>Apportioned fixed overhead</b>",
                  "Apportioned share of a cost incurred anyway &mdash; <b>irrelevant</b>",
                  "&mdash;"]},
       {"cls": "tot",
        "cells": ["<b>Relevant cost of MAKING</b>", "10 + 6 + 6", "<b>22.00</b>"]},
       {"cls": "sub", "cells": ["<b>Cost of BUYING</b>", "quoted by the outside supplier",
                                "<b>24.00</b>"]},
       {"cls": "tot", "cells": ["<b>Saving by making &mdash; so MAKE</b>",
                                f"{R}24 &minus; {R}22", "<b>2.00</b>"]}],
      headcls="lite", widths=["30%", "50%", "20%"])

    return ("<div class='prob long'>"
            + prob_head("Q4", "Discussing the relevance of each item of a special order",
                        "Special order &middot; p.40")
            + question(q) + read(rd) + a_tbl + b_tbl + c_tbl
            + why(f"""<p>Each part turns on a different one of the three ideas in this module, which
is why this problem is worth learning as a set:</p>
{bullets([
 '<b>(a) is opportunity cost.</b> No cash is spent on the equipment, yet ' + R + '700 of value is '
 'destroyed. A cost need not be a payment.',
 '<b>(b) is the sunk-versus-incremental distinction.</b> Both figures relate to storage; one is new '
 'cash and one is book-keeping. Only the first can change.',
 '<b>(c) is the fixed-overhead trap.</b> At ' + R + '30 making looks dearer than buying at ' + R
 + '24, and a careless answer buys. Once the ' + R + '8 apportioned overhead is removed &mdash; it '
 'is incurred either way &mdash; making costs ' + R + '22 and is the cheaper option by ' + R + '2 '
 'per unit.'])}
<p><b>Summary of the relevant cost of the special order:</b> {R}700 for the equipment plus {R}18,000
for storage, and the sub-assembly should be <b>made</b> in-house at a relevant cost of {R}22 per unit.
The order&rsquo;s price must cover {R}18,700 plus {R}22 for every unit of sub-assembly required.</p>""")
            + ans([("(a) Equipment &mdash; fall in resale value", f"{R} 700 &nbsp;<b>relevant</b>"),
                   ("&nbsp;&nbsp;&nbsp;&nbsp;Book value " + R + " 2,000", "irrelevant &mdash; sunk"),
                   ("(b) Warehouse rent", f"{R} 18,000 &nbsp;<b>relevant</b>"),
                   ("&nbsp;&nbsp;&nbsp;&nbsp;Building depreciation " + R + " 12,000",
                    "irrelevant &mdash; allocated, non-cash"),
                   ("(c) Relevant cost of making", f"{R} 22 per unit"),
                   ("&nbsp;&nbsp;&nbsp;&nbsp;Cost of buying", f"{R} 24 per unit"),
                   ("<b>(c) Decision</b>",
                    f"<b>MAKE &mdash; saves {R} 2 per unit</b>"),
                   ("<b>Total identifiable relevant cost</b>",
                    f"<b>{R} 18,700 + {R} 22 per sub-assembly</b>")])
            + "</div>")



# ======================================================================
# Q5
# ======================================================================
def q5():
    q = f"""<p>A company can make any one of the 3 products X, Y or Z in a year. It can exercise its
option only at the beginning of each year. Relevant information about the products for the next year
is given below:</p>
{table(None, [("Particulars", ""), ("X", "r"), ("Y", "r"), ("Z", "r")],
 [["Selling price", f"{R}10 p.u.", f"{R}12 p.u.", f"{R}12 p.u."],
  ["Variable cost", f"{R}6 p.u.", f"{R}9 p.u.", f"{R}7 p.u."],
  ["Market demand (units)", "3,000", "2,000", "1,000"],
  ["Production capacity (units)", "2,000", "3,000", "900"],
  ["Fixed cost", {"t": f"{R}30,000 (common to all three)", "a": "r", "cls": "c"}, "", ""]],
 headcls="lite")}
<p>You are required to compute the opportunity costs for each of the products.</p>"""

    rd = f"""<p>&ldquo;Opportunity cost <b>for each</b> of the products&rdquo; means three separate
answers, not one. The opportunity cost <i>of choosing a product</i> is the contribution of the best
alternative you had to give up.</p>
{bullets([
 '<b>&ldquo;Can make any one of the 3&rdquo;</b> &mdash; the options are mutually exclusive. Choose '
 'one and both others are forgone.',
 '<b>Effective production is the LOWER of market demand and production capacity.</b> There is no '
 'point making 3,000 units of X if only 2,000 can be produced, and no point having capacity for '
 '3,000 units of Y if only 2,000 can be sold. This one line is where most marks are lost.',
 'The fixed cost of ' + R + '30,000 is <b>common to all three</b> options. It cannot help you '
 'choose, so it plays no part in the opportunity cost. Do not deduct it product by product.',
 'The opportunity cost of X is the best of {Y, Z}; of Y the best of {X, Z}; of Z the best of '
 '{X, Y}. Because X is the overall best, it appears as the opportunity cost of both Y and Z.'])}"""

    main = table("Computation of opportunity cost",
      [("Particulars", ""), ("X", "r"), ("Y", "r"), ("Z", "r")],
      [["Selling price per unit", "10", "12", "12"],
       ["<i>Less:</i> Variable cost per unit", "(6)", "(9)", "(7)"],
       {"cls": "sub", "cells": ["<b>Contribution per unit</b>", "<b>4</b>", "<b>3</b>", "<b>5</b>"]},
       ["Market demand (units)", "3,000", "2,000", "1,000"],
       ["Production capacity (units)", "2,000", "3,000", "900"],
       {"cls": "sub",
        "cells": ["<b>Effective production (units)</b><br/>"
                  + src("whichever is LOWER of demand and capacity"),
                  "<b>2,000</b>", "<b>2,000</b>", "<b>900</b>"]},
       {"cls": "tot",
        "cells": ["<b>Total contribution</b> " + R + "<br/>"
                  + src("effective units &times; contribution per unit"),
                  "<b>8,000</b><br/>" + src("2,000 &times; 4"),
                  "<b>6,000</b><br/>" + src("2,000 &times; 3"),
                  "<b>4,500</b><br/>" + src("900 &times; 5")]},
       {"cls": "tot",
        "cells": ["<b>Opportunity cost</b> " + R + "<br/>"
                  + src("best contribution GIVEN UP by choosing this product"),
                  "<b>6,000</b><br/>" + src("&larr; Y, the next best"),
                  "<b>8,000</b><br/>" + src("&larr; X, the best forgone"),
                  "<b>8,000</b><br/>" + src("&larr; X, the best forgone")]}],
      widths=["40%", "20%", "20%", "20%"])

    flow = arrow_panel(500, 168, [
        {"box": (16, 14, 148, 30, "X|contribution " + R + "8,000", "#eaf6ee"),
         "stroke": GREEN, "fs": 8.4},
        {"box": (176, 14, 148, 30, "Y|contribution " + R + "6,000", "#ffffff"), "fs": 8.4},
        {"box": (336, 14, 148, 30, "Z|contribution " + R + "4,500", "#ffffff"), "fs": 8.4},
        {"box": (16, 118, 148, 34, "Opportunity cost|" + R + "6,000", "#fdf1ef"),
         "stroke": RED, "fg": RED, "fs": 8.4},
        {"box": (176, 118, 148, 34, "Opportunity cost|" + R + "8,000", "#fdf1ef"),
         "stroke": RED, "fg": RED, "fs": 8.4},
        {"box": (336, 118, 148, 34, "Opportunity cost|" + R + "8,000", "#fdf1ef"),
         "stroke": RED, "fg": RED, "fs": 8.4},
        {"arc": (176, 46, 108, 116, "if you choose X you lose Y", 26), "col": RED},
        {"arc": (90, 48, 240, 116, "if you choose Y you lose X", -30), "col": RED},
        {"arc": (90, 48, 400, 116, "if you choose Z you lose X", -46), "col": RED},
        {"txt": (250, 78, "the arrow always starts at the BEST option you gave up",
                 7.4, GREY, "middle")},
    ], "Reading the opportunity cost. Choose X and the best thing forgone is Y (" + R + "6,000). "
       "Choose Y or Z and the best thing forgone is X (" + R + "8,000) in both cases.")

    return ("<div class='prob long'>"
            + prob_head("Q5", "Opportunity cost of three mutually exclusive products",
                        "Opportunity cost &middot; p.40&ndash;41")
            + question(q) + read(rd) + main + flow
            + why(f"""<p>Opportunity cost answers the question &ldquo;what did this choice cost me in
things I could have had instead?&rdquo; It is not a cost the accountant will ever record, which is why
it has to be computed deliberately.</p>
<p>The three answers together tell management exactly what it needs to know:</p>
{bullets([
 '<b>Make X.</b> Its opportunity cost of ' + R + '6,000 is the <i>lowest</i> of the three, which is '
 'the same thing as saying its own contribution of ' + R + '8,000 is the highest.',
 'The rule to remember: <b>the best option is always the one with the lowest opportunity '
 'cost.</b> You can use either test and you will get the same answer.',
 'Y and Z share an opportunity cost of ' + R + '8,000 because both sacrifice the same thing '
 '&mdash; X. Identical opportunity costs do not make them equally good; Y still earns ' + R
 + '6,000 and Z only ' + R + '4,500.'])}
<div class="blk trap" style="margin-top:3mm"><span class="lab">Worth adding for the extra mark</span>
<p>Even the best option earns a contribution of only {R}8,000 against a fixed cost of {R}30,000
&mdash; a loss of {R}22,000 whichever product is chosen. Opportunity cost analysis <b>ranks</b>
alternatives; it does not tell you the business is worth being in. Saying so shows the examiner you
understand the limits of the technique.</p></div>""")
            + ans([("Contribution per unit &mdash; X / Y / Z", f"{R} 4 / {R} 3 / {R} 5"),
                   ("Effective production &mdash; X / Y / Z", "2,000 / 2,000 / 900 units"),
                   ("Total contribution &mdash; X / Y / Z",
                    f"{R} 8,000 / {R} 6,000 / {R} 4,500"),
                   ("<b>Opportunity cost of X</b>", f"<b>{R} 6,000</b>"),
                   ("<b>Opportunity cost of Y</b>", f"<b>{R} 8,000</b>"),
                   ("<b>Opportunity cost of Z</b>", f"<b>{R} 8,000</b>"),
                   ("<b>Decision</b>",
                    "<b>Make X &mdash; lowest opportunity cost</b>")])
            + "</div>")


# ======================================================================
# Q6
# ======================================================================
def q6():
    q = f"""<p>A machine manufactures 10,000 units of a part at a total cost of {R}21 of which {R}18 is
variable. This part is readily available in the market at {R}19 per unit. If the part is purchased from
the market then the machine can either be utilised to manufacture a component of the same quantity
contributing {R}2 per component, or it can be hired out at {R}21,000. Recommend which of the
alternatives is profitable.</p>"""

    rd = f"""<p>There are <b>three</b> alternatives here, not two. Students routinely compare only
&ldquo;make&rdquo; against &ldquo;buy&rdquo; and lose half the marks.</p>
{steps([
 '<b>Alternative I &mdash; Make the part.</b> Relevant cost is the variable cost only: ' + R
 + '18 &times; 10,000. The ' + R + '3 of fixed cost per unit (21 &minus; 18) is incurred whether or '
 'not the part is made, so it is excluded.',
 '<b>Alternative II &mdash; Buy the part and use the freed machine to make the component.</b> Pay ' +
 R + '19 &times; 10,000, then <i>credit</i> the contribution the component earns.',
 '<b>Alternative III &mdash; Buy the part and hire the machine out.</b> Pay ' + R + '19 &times; '
 '10,000, then credit the hire income of ' + R + '21,000.'])}
{bullets([
 '<b>The freed machine is the whole point.</b> Buying the part does not merely cost ' + R + '1 more '
 'per unit &mdash; it releases capacity that can earn money. That benefit must be brought into the '
 'comparison, and it is what reverses the decision.',
 'Present the benefit as a <b>deduction from cost</b> (&ldquo;net relevant cost&rdquo;) and then '
 'choose the <b>lowest</b> column. That is the format in your notes and it avoids sign errors.',
 'Note the ' + R + '2 is <i>per component</i> and the quantity is <i>the same</i> &mdash; so '
 '10,000 &times; ' + R + '2 = ' + R + '20,000, which is <b>less</b> than the ' + R + '21,000 hire '
 'charge. Read this carefully; it is the deciding comparison.'])}"""

    main = table("Statement of net relevant cost under the three alternatives",
      [("Particulars", ""), ("Alternative I<br/><span class='small'>Make</span>", "r"),
       ("Alternative II<br/><span class='small'>Buy &amp; make the component</span>", "r"),
       ("Alternative III<br/><span class='small'>Buy &amp; hire out the machine</span>", "r")],
      [{"cls": "",
        "cells": ["<b>Relevant (variable) cost</b><br/>" + src("fixed " + R + "3 p.u. excluded"),
                  "1,80,000<br/>" + src("10,000 &times; " + R + "18"),
                  "1,90,000<br/>" + src("10,000 &times; " + R + "19"),
                  "1,90,000<br/>" + src("10,000 &times; " + R + "19")]},
       {"cls": "",
        "cells": ["<b><i>Less:</i> Relevant benefit</b><br/>"
                  + src("what the freed machine earns"),
                  "&mdash;",
                  "(20,000)<br/>" + src("10,000 &times; " + R + "2"),
                  "(21,000)<br/>" + src("hire charge, given")]},
       {"cls": "tot",
        "cells": ["<b>Net relevant cost</b> " + R,
                  "<b>1,80,000</b>", "<b>1,70,000</b>", "<b>1,69,000</b>"]},
       {"cls": "sub",
        "cells": ["<b>Ranking</b>", "3rd", "2nd", "<b>1st &mdash; best</b>"]}],
      widths=["31%", "23%", "23%", "23%"])

    return ("<div class='prob'>"
            + prob_head("Q6", "Make or buy when the freed machine has two possible uses",
                        "Make or buy &middot; p.41")
            + question(q) + read(rd) + main
            + why(f"""<p>On the face of it making is obviously right: {R}18 to make against {R}19 to
buy. Making <i>is</i> cheaper &mdash; by {R}10,000 in total. But that comparison quietly assumes the
machine is worth nothing when idle, and the question tells you it is worth {R}21,000.</p>
{calc([f'Extra cost of buying instead of making &nbsp;=&nbsp; 10,000 &times; ({R}19 &minus; {R}18) '
       f'&nbsp;=&nbsp; {R}10,000',
       f'Best earning of the machine once freed &nbsp;=&nbsp; higher of {R}20,000 and {R}21,000 '
       f'&nbsp;=&nbsp; {R}21,000',
       f'<b>Net gain from buying and hiring out &nbsp;=&nbsp; 21,000 &minus; 10,000 &nbsp;=&nbsp; '
       f'{R}11,000</b>'])}
<p>That {R}11,000 is exactly the gap between {R}1,80,000 and {R}1,69,000 in the statement, which is
your arithmetic check.</p>
<p><b>Recommendation:</b> buy the part from the market at {R}19 and hire the machine out for
{R}21,000. This is the cheapest of the three at a net relevant cost of {R}1,69,000 &mdash;
{R}11,000 better than making the part in-house and {R}1,000 better than using the machine for the
component.</p>
<p class="small"><b>A caution worth one mark:</b> the decision depends on the hire income being
dependable. If the hirer might not be found, or if buying the part surrenders control over quality and
delivery, the {R}1,000 margin over Alternative II is too thin to rely on.</p>""")
            + ans([("Alternative I &mdash; Make", f"{R} 1,80,000"),
                   ("Alternative II &mdash; Buy &amp; make the component", f"{R} 1,70,000"),
                   ("Alternative III &mdash; Buy &amp; hire out", f"<b>{R} 1,69,000</b>"),
                   ("<b>Decision</b>",
                    "<b>Alternative III &mdash; lowest net relevant cost</b>"),
                   ("Saving over making in-house", f"{R} 11,000"),
                   (f"Why the {R} 3 fixed cost is excluded",
                    "Incurred whether or not the part is made")])
            + "</div>")


# ======================================================================
# Q7
# ======================================================================
def q7():
    q = f"""<p>S Ltd. is engaged in manufacturing activities. It has received a request from one of its
important customers to supply a product which will require conversion of Material M, which is a
non-moving item. The following details are available:</p>
{table(None, [("Particulars", ""), ("" + R, "r")],
 [["Book value of Material M", "60"], ["Realisable value of Material M", "80"],
  ["Replacement cost of Material M", "100"]], headcls="lite", widths=["76%", "24%"])}
<p>It is estimated that conversion of one unit of M into one unit of the finished product will require
1 labour hour. At present, labour is paid at the rate of {R}20 per hour. Other costs are as follows:</p>
{table(None, [("Particulars", ""), ("" + R, "r")],
 [["Out-of-pocket expenses", "30 per unit"], ["Allocated overheads", "10 per unit"]],
 headcls="lite", widths=["76%", "24%"])}
<p>The labour will be re-deployed from other activities. It is estimated that the temporary
re-deployment will not result in loss of contribution. The employees to be re-deployed are permanent
employees of the company.</p>
<p>Estimate the minimum price to be charged from the customer so that the company is not worse off by
executing the order.</p>"""

    rd = f"""<p>&ldquo;<b>Minimum price so that the company is not worse off</b>&rdquo; is the
examiner&rsquo;s way of saying <i>total relevant cost</i>. Compute the relevant cost and that total
<b>is</b> the answer &mdash; no mark-up, no profit margin.</p>
<p>Five figures are given and <b>three of them are decoys</b>. Each phrase in the question exists to
send one figure to the bin:</p>
{table(None, [("The phrase in the question", ""), ("What it tells you", "")],
 [["&ldquo;Material M &hellip; is a <b>non-moving</b> item&rdquo;",
   "M will <b>not</b> be replaced. So the replacement cost of " + R + "100 is irrelevant, and the "
   "sacrifice is the sale forgone &mdash; realisable value " + R + "80. This is box &#9314; of the "
   "material tree."],
  ["&ldquo;<b>Book value</b> of Material M " + R + "60&rdquo;",
   "Historical cost, already paid. Sunk &mdash; irrelevant."],
  ["&ldquo;<b>permanent</b> employees &hellip; re-deployed &hellip; <b>will not result in loss of "
   "contribution</b>&rdquo;",
   "The wages are paid anyway and nothing is given up elsewhere. Committed cost &mdash; relevant "
   "cost is <b>NIL</b>. This is box &#9314; of the labour tree, and the " + R + "20 per hour is "
   "a decoy."],
  ["&ldquo;<b>Out-of-pocket</b> expenses " + R + "30&rdquo;",
   "The words say it: fresh cash caused by the order. <b>Relevant.</b>"],
  ["&ldquo;<b>Allocated</b> overheads " + R + "10&rdquo;",
   "The word &ldquo;allocated&rdquo; is the giveaway &mdash; an apportioned share of a cost incurred "
   "anyway. Irrelevant."]], headcls="lite", widths=["38%", "62%"])}"""

    tbl = rc("Computation of the minimum price to be charged (per unit)",
      [("Material M",
        f"Material M is a slow-moving / non-moving item, therefore it will not be replaced. The net "
        f"realisable value forgone is the <b>opportunity cost</b> and is relevant. "
        f"{src('realisable value ' + R + '80 &mdash; NOT replacement cost ' + R + '100')}", 80),
       ("Labour",
        f"Permanent employees, and the re-deployment does not result in loss of contribution. Hence "
        f"the wages are a <b>committed cost</b> and are irrelevant. "
        f"{src('1 hour &times; ' + R + '20 = ' + R + '20 &mdash; excluded')}", 0),
       ("Out-of-pocket expenses",
        f"Fresh cash outflow incurred only because the order is executed. Relevant. "
        f"{src('given, ' + R + '30 per unit')}", 30),
       ("!Book value of Material M",
        f"{R}60 was paid in the past. Sunk cost &mdash; irrelevant.", "&mdash;"),
       ("!Replacement cost of M",
        f"{R}100 would matter only if M were regularly used and had to be bought again. It is "
        f"non-moving, so it will not be replaced &mdash; irrelevant.", "&mdash;"),
       ("!Allocated overheads",
        f"{R}10 per unit is an apportioned share of overheads the company incurs anyway. "
        f"Irrelevant.", "&mdash;")],
      total=("Minimum price to be charged to the customer", 110))

    return ("<div class='prob long'>"
            + prob_head("Q7", "Minimum price using relevant cost",
                        "Minimum price &middot; p.42")
            + question(q) + read(rd) + tbl
            + why(f"""<p>&ldquo;Not worse off&rdquo; has a precise meaning: the company must end up
with at least as much cash as if it had refused the order. Refusing the order means selling M for
{R}80 and paying the workers their wages regardless. Accepting means giving up the {R}80 sale and
spending {R}30. So {R}110 is the exact break-even price.</p>
{fml("Minimum price &nbsp;=&nbsp; Total relevant cost &nbsp;=&nbsp; " + R + "80 + Nil + " + R
     + "30 &nbsp;=&nbsp; " + R + "110",
     "At exactly " + R + "110 the company is indifferent. Above " + R + "110 it gains. Below "
     + R + "110 it would do better to sell the material as scrap and turn the order down.")}
<p><b>The labour line is the one to understand properly</b>, because it feels wrong to write
&ldquo;Nil&rdquo; against a cost that is obviously being incurred. The wages of {R}20 <i>are</i> paid
&mdash; but they are paid whether the order is taken or not, and the question expressly says nothing
is given up by moving the workers. Two futures, same wage bill, no difference, no relevant cost.</p>
<p class="small">Change either condition and the answer changes: if the workers had to be hired
specially, {R}20 becomes an out-of-pocket cost and the price rises to {R}130; if re-deployment
sacrificed contribution elsewhere, that contribution would be added as an opportunity cost.</p>""")
            + ans([("Material M &mdash; NRV as opportunity cost", f"{R} 80"),
                   ("Labour &mdash; committed cost", "<b>Nil</b>"),
                   ("Out-of-pocket expenses", f"{R} 30"),
                   ("<b>Minimum price per unit</b>", f"<b>{R} 110</b>"),
                   ("Excluded as irrelevant",
                    f"Book value {R} 60 &middot; Replacement {R} 100 &middot; "
                    f"Allocated OH {R} 10")])
            + "</div>")


# ======================================================================
# The machine-replacement playbook, used by Q8 and Q12
# ======================================================================
def machine_playbook():
    body = f"""
<p>Q8 and Q12 are the <b>same problem with different numbers</b>. They have three parts, and part
(iii) deliberately contradicts parts (i) and (ii) &mdash; understanding why is the whole lesson.</p>

{steps([
 '<b>(i) Identify the relevant cost.</b> List what changes if the new machine is bought: its '
 'purchase price, the disposal proceeds of the old machine, and the two operating costs per hour. '
 'The price already paid for the old machine is <b>sunk</b> and is excluded. Then compute the '
 '<b>incremental investment</b>:'
 + fml("Incremental investment &nbsp;=&nbsp; Cost of the new machine &nbsp;&minus;&nbsp; "
       "Disposal value of the old machine"),
 '<b>(ii) Hours the new machine must run to benefit the company.</b> Divide that incremental '
 'investment by the contribution the new machine earns per hour:'
 + fml("Hours required &nbsp;=&nbsp; "
       + frac("Incremental investment", "Revenue per hour &minus; Operating cost per hour of the NEW machine")),
 '<b>(iii) Break-even hours of each machine.</b> Now switch to the <b>full purchase cost</b> of '
 'each machine &mdash; including the sunk cost of the old one &mdash; and divide by that '
 'machine&rsquo;s own contribution per hour:'
 + fml("Break-even hours &nbsp;=&nbsp; "
       + frac("FULL cost of that machine", "Revenue per hour &minus; that machine&rsquo;s operating cost per hour"))])}

<div class="blk trap"><span class="lab">Why (ii) and (iii) use different numerators &mdash; read this twice</span>
<p>This looks like an inconsistency and students often &ldquo;correct&rdquo; it into a wrong answer.
It is not an inconsistency, because the two parts ask <b>different questions</b>:</p>
{table(None, [("", ""), ("Part (ii)", ""), ("Part (iii)", "")],
 [["The question being asked", "Should we <b>switch</b> from the old machine to the new one?",
   "How long must a machine run to <b>recover its own cost</b>?"],
  ["Type of question", "A <b>relevant-cost</b> decision &mdash; comparing two futures",
   "A <b>cost-recovery</b> or break-even calculation for one asset"],
  ["Numerator", "Incremental investment &mdash; sunk cost <b>excluded</b>",
   "Full purchase cost &mdash; sunk cost <b>included</b>"],
  ["Denominator", "Contribution per hour of the NEW machine",
   "Contribution per hour of the machine being examined"]], headcls="lite",
 widths=["22%", "39%", "39%"])}
<p>Break-even is a question about whether an investment <i>as a whole</i> pays for itself, and for
that you must count every rupee it cost. Relevant costing is a question about <i>changing course from
here</i>, and for that money already gone is beside the point.</p>
</div>

<div class="blk why"><span class="lab">The pattern to memorise</span>
{bullets([
 'Contribution per hour = <b>revenue per hour &minus; operating cost per hour</b>. Compute it for '
 'both machines first; every later step uses it.',
 'The new machine has the <b>lower</b> operating cost, so the <b>higher</b> contribution per hour. '
 'That is the entire case for buying it.',
 'The new machine costs more but breaks even <b>sooner</b> in Q8, and <b>later</b> in Q12. Do not '
 'assume the pattern &mdash; compute it, because the two problems genuinely differ here.'])}
</div>
"""
    return module_opener("Method", "Machine replacement &mdash; relevant cost, benefit hours and break-even hours",
                         "Use these steps for Q8 and Q12", body)


# ======================================================================
# Q8
# ======================================================================
def q8():
    q = f"""<p>A machinery was purchased for {R}20,00,000; the operating cost is {R}100 per hour. When
the machine was about to be installed it was found out that another machine which is more efficient was
available in the market for {R}35,00,000. The operating cost of that machine is {R}70 per hour.</p>
<p>If this new machine is purchased for {R}35,00,000 the old machine could be disposed of for
{R}12,00,000. Consider the revenue per hour from both the machines as {R}120.</p>
<p><b>(i)</b> Identify the relevant cost. <b>(ii)</b> How many hours does the new machine have to run
for the benefit of the company? <b>(iii)</b> What is the break-even hour for both these machines?</p>"""

    rd = f"""{bullets([
 '<b>&ldquo;When the machine was about to be installed&rdquo;</b> &mdash; the ' + R + '20,00,000 '
 'has already been paid. It is <b>sunk</b> for parts (i) and (ii). This is uncomfortable because it '
 'is the second-largest number on the page.',
 '<b>The old machine can be sold for ' + R + '12,00,000.</b> That inflow reduces the true cost of '
 'switching, so the incremental investment is ' + R + '35,00,000 &minus; ' + R + '12,00,000, not ' +
 R + '35,00,000.',
 '<b>Revenue is ' + R + '120 per hour from BOTH machines.</b> So the machines differ only in '
 'operating cost &mdash; ' + R + '100 against ' + R + '70 &mdash; and therefore in contribution per '
 'hour: ' + R + '20 against ' + R + '50.',
 '<b>Part (iii) switches to full cost.</b> Read the playbook above before attempting it.'])}"""

    ph = f"""<h4 class="mini">W1 &nbsp;Contribution per hour of each machine</h4>
{table(None, [("Particulars", ""), ("Old machine " + R, "r"), ("New machine " + R, "r")],
 [["Revenue per hour", "120", "120"],
  ["<i>Less:</i> Operating cost per hour", "(100)", "(70)"],
  {"cls": "tot", "cells": ["<b>Contribution per hour</b>", "<b>20</b>", "<b>50</b>"]}],
 headcls="lite", widths=["52%", "24%", "24%"])}

<h4 class="mini">W2 &nbsp;Incremental investment in switching</h4>
{calc([f'Cost of the new machine &nbsp;=&nbsp; {R}35,00,000',
       f'<i>Less:</i> Disposal value of the old machine &nbsp;=&nbsp; ({R}12,00,000)',
       f'<b>Incremental investment &nbsp;=&nbsp; {R}23,00,000</b>'])}"""

    p1 = rc("(i) Identification of the relevant cost",
      [("Operating cost &mdash; old machine",
        f"{R}100 per hour. Differs between the alternatives, so relevant.", f"{R}100 / hr"),
       ("Cost of the new machine",
        f"A fresh cash outflow caused solely by the decision to switch. Relevant. "
        f"{src('given')}", 3500000),
       ("Operating cost &mdash; new machine",
        f"{R}70 per hour. Differs between the alternatives, so relevant.", f"{R}70 / hr"),
       ("Disposal value of the old machine",
        f"A cash inflow that arises only if the new machine is bought. Relevant &mdash; deduct it "
        f"from the investment. {src('given, NRV of the old machine')}", 1200000),
       ("Revenue per hour",
        f"{R}120 from either machine. Needed to compute contribution per hour.", f"{R}120 / hr"),
       ("!Purchase price of the old machine",
        f"{R}20,00,000 has already been committed and cannot be recovered by any decision taken now. "
        f"<b>Sunk</b> &mdash; irrelevant for parts (i) and (ii).", "&mdash;")],
      total=("Incremental investment &nbsp;(35,00,000 &minus; 12,00,000)", 2300000))

    p2 = f"""<h3 class="sub">(ii) Hours the new machine must run for the benefit of the company</h3>
{fml("Hours required &nbsp;=&nbsp; " + frac("Incremental investment", "Contribution per hour of the new machine")
     + " &nbsp;=&nbsp; " + frac(R + "23,00,000", R + "50") + " &nbsp;=&nbsp; <b>46,000 hours</b>")}
<p class="small">Beyond 46,000 hours of running, the extra {R}23,00,000 laid out on the switch has been
fully recovered out of the new machine&rsquo;s contribution, and every hour after that is pure gain.</p>"""

    p3 = f"""<h3 class="sub">(iii) Break-even hours of each machine</h3>
<p class="small">Here the <b>full</b> cost of each machine is recovered out of its own contribution
per hour &mdash; see the method page for why the sunk cost comes back in.</p>
{table(None, [("Machine", ""), ("Computation", ""), ("Break-even hours", "r")],
 [["<b>Machine 1 &mdash; old</b>",
   frac(R + "20,00,000", R + "120 &minus; " + R + "100") + " &nbsp;=&nbsp; "
   + frac(R + "20,00,000", R + "20"), "<b>1,00,000 hours</b>"],
  ["<b>Machine 2 &mdash; new</b>",
   frac(R + "35,00,000", R + "120 &minus; " + R + "70") + " &nbsp;=&nbsp; "
   + frac(R + "35,00,000", R + "50"), "<b>70,000 hours</b>"]],
 headcls="lite", widths=["24%", "50%", "26%"])}"""

    return ("<div class='prob long'>"
            + prob_head("Q8", "Machine replacement &mdash; relevant cost, benefit hours, break-even hours",
                        "Machine &middot; p.41")
            + question(q) + read(rd) + wn(ph) + p1 + p2 + p3
            + why(f"""<p><b>The new machine is better on every count</b>, which is what makes this
problem a clean illustration:</p>
{bullets([
 'It earns ' + R + '50 an hour instead of ' + R + '20 &mdash; two and a half times as much '
 'contribution, purely because it burns ' + R + '30 less an hour in operating cost.',
 'It recovers its <b>full</b> cost in 70,000 hours against the old machine&rsquo;s 1,00,000 hours, '
 'even though it cost 75% more to buy.',
 'The switch itself pays for itself in 46,000 hours &mdash; sooner still, because the ' +
 R + '12,00,000 from selling the old machine funds part of the purchase.'])}
<p><b>Recommendation:</b> buy the new machine, provided it will be run for more than 46,000 hours over
its life. The {R}20,00,000 already spent on the old machine is painful but irrelevant &mdash;
refusing to switch in order to &ldquo;get the value out of&rdquo; the old machine would simply add a
second mistake to the first. That instinct has a name in cost accounting: <b>throwing good money after
bad</b>.</p>""")
            + ans([("Contribution per hour &mdash; old / new", f"{R} 20 / {R} 50"),
                   ("<b>(i) Incremental investment (relevant)</b>", f"<b>{R} 23,00,000</b>"),
                   ("&nbsp;&nbsp;&nbsp;&nbsp;Excluded as sunk",
                    f"{R} 20,00,000 cost of the old machine"),
                   ("<b>(ii) Hours for the benefit of the company</b>", "<b>46,000 hours</b>"),
                   ("<b>(iii) Break-even hours &mdash; old machine</b>", "<b>1,00,000 hours</b>"),
                   ("<b>(iii) Break-even hours &mdash; new machine</b>", "<b>70,000 hours</b>"),
                   ("<b>Decision</b>",
                    "<b>Buy the new machine if it will run &gt; 46,000 hours</b>")])
            + "</div>")



# ======================================================================
# The rectification playbook, used by Q9 and Q11
# ======================================================================
def rectify_playbook():
    body = f"""
<p>Q9 and Q11 are the <b>same problem with different numbers</b>. Goods have already been made, they
are defective, and there is a choice: dump them at a low price now, or spend more and sell them at a
higher price. Both questions ask four sub-parts in the same order.</p>

<div class="blk read"><span class="lab">The one thing that decides these problems</span>
{fml("The cost of manufacturing the goods is SUNK. Ignore it entirely.",
     "The shirts exist. Nothing you decide now can un-spend that money. It is identical under both "
     "options, so it cannot affect the choice &mdash; it only affects how large the loss is, not "
     "which option is better.")}
</div>

{steps([
 '<b>(i) State the relevant costs.</b> Only the <b>rectification cost</b> per unit is relevant, '
 'because it is the only cash that depends on the decision. Say in words that the manufacturing cost '
 'is sunk &mdash; this is a marked point, not a throwaway line.',
 '<b>(ii) Should the rectification be done?</b> Compare the two <i>increments</i>, per unit:'
 + fml("Incremental revenue &nbsp;=&nbsp; Price after rectification &minus; Price as rejects"
       "<br/>Incremental cost &nbsp;=&nbsp; Rectification cost per unit"
       "<br/><b>Rectify if incremental revenue &gt; incremental cost</b>"),
 '<b>(iii) Gain or loss if NOT rectified</b> and <b>(iv) if rectified.</b> Answer these on the '
 '<b>incremental</b> basis, exactly as your class notes do: the net gain per unit multiplied by the '
 'number of units. Then add the absolute figures as a cross-check, because they show <i>why</i> the '
 'recommendation still holds even though the company loses money either way.'])}

<div class="blk why"><span class="lab">Two ways to answer (iii) and (iv) &mdash; give both</span>
{table(None, [("", ""), ("Incremental view &mdash; the relevant one", ""),
              ("Absolute view &mdash; the cross-check", "")],
 [["What it measures",
   "How much better or worse off you are <b>by choosing one option over the other</b>",
   "The actual profit or loss reported, <b>after</b> charging the sunk manufacturing cost"],
  ["Manufacturing cost", "Excluded &mdash; sunk", "Included &mdash; it did happen"],
  ["What it tells management",
   "<b>Which option to pick.</b> This is the answer the question wants.",
   "That the order is a loss-maker either way &mdash; the choice is only about the size of the loss."],
  ["Risk of using it alone",
   "None for decision-making",
   "Tempts you to reject both options because both show a loss, which would be worse still"]],
 headcls="lite", widths=["18%", "41%", "41%"])}
<p>Both views always agree on <b>the difference</b> between the two options &mdash; that is the
arithmetic check to run before you write your conclusion.</p>
</div>

<div class="blk trap"><span class="lab">The trap / where marks are lost</span>
{bullets([
 '<b>Deducting the manufacturing cost from the rectification decision.</b> If you do, both options '
 'look catastrophic and students conclude &ldquo;do not rectify&rdquo;, which is wrong.',
 '<b>Comparing the new price against the manufacturing cost</b> instead of against the reject price. '
 'The alternative to rectifying is <i>selling as rejects</i>, not <i>not having made them</i>.',
 '<b>Forgetting that both prices are per shirt and must be multiplied by the quantity.</b> The '
 'per-unit answer earns part marks; the total earns the rest.'])}
</div>
"""
    return module_opener("Method", "Rectify or sell as rejects &mdash; further processing decisions",
                         "Use these steps for Q9 and Q11", body)


# ======================================================================
def _rectify_solution(no, units, mfg, reject_price, rect_cost, new_price, page):
    """Q9 and Q11 are structurally identical; build both from one routine."""
    inc_rev = new_price - reject_price
    net = inc_rev - rect_cost
    total_net = net * units
    sunk = units * mfg
    rev_no = units * reject_price
    rev_yes = units * new_price
    rect_total = units * rect_cost
    loss_no = sunk - rev_no
    loss_yes = sunk + rect_total - rev_yes

    q = f"""<p>{rs(units)} shirts have been manufactured for export at a cost of {R}{rs(mfg)} per
shirt. These shirts were rejected because of defects and can be sold for {R}{rs(reject_price)} per
shirt in the local market. If the defects are rectified by spending {R}{rs(rect_cost)} per shirt, the
same can be sold for {R}{rs(new_price)}.</p>
<p><b>(i)</b> What are the relevant costs? <b>(ii)</b> Should the rectification be done?
<b>(iii)</b> What is the gain or loss if not rectified? <b>(iv)</b> What is the gain or loss if
rectified?</p>"""

    rd = f"""{bullets([
 '<b>The ' + R + rs(mfg) + ' per shirt is already spent.</b> The shirts exist and are defective. '
 'That cost is <b>sunk</b> and takes no part in the decision.',
 '<b>The real choice is between two selling prices</b>, ' + R + rs(reject_price) + ' now and ' + R
 + rs(new_price) + ' after spending ' + R + rs(rect_cost) + '. So compare ' + R + rs(inc_rev)
 + ' of extra revenue against ' + R + rs(rect_cost) + ' of extra cost.',
 '<b>Do not compare ' + R + rs(new_price) + ' with ' + R + rs(mfg) + '.</b> The alternative to '
 'rectifying is selling the shirts as rejects &mdash; not un-making them.',
 'Both options lose money against the ' + R + rs(mfg) + ' already spent. That is unavoidable now; '
 'the only question is which loses <b>less</b>.'])}"""

    p1 = rc("(i) Identification of the relevant costs",
      [("Rectification cost",
        f"{R}{rs(rect_cost)} per shirt is spent only if rectification is undertaken. It is the one "
        f"cash flow that changes with the decision &mdash; <b>relevant</b>. "
        f"{src(rs(units) + ' shirts &times; ' + R + rs(rect_cost))}", rect_total),
       ("Incremental revenue",
        f"Selling price rises from {R}{rs(reject_price)} to {R}{rs(new_price)}, a gain of "
        f"{R}{rs(inc_rev)} per shirt. A relevant <b>benefit</b>. "
        f"{src(rs(units) + ' shirts &times; ' + R + rs(inc_rev))}", inc_rev * units),
       ("!Cost of manufacture",
        f"{R}{rs(mfg)} per shirt, {R}{rs(sunk)} in total, has already been incurred. The shirts are "
        f"made. <b>Sunk cost &mdash; irrelevant.</b>", "&mdash;")],
      total=("Net relevant benefit of rectifying", total_net))

    p2 = table("(ii) Should the rectification be done? &mdash; incremental statement",
      [("Particulars", ""), ("Per shirt " + R, "r"), (f"{rs(units)} shirts " + R, "r")],
      [["Selling price after rectification", rs(new_price), rs(rev_yes)],
       ["<i>Less:</i> Selling price as rejects " + src("the alternative given up"),
        f"({rs(reject_price)})", f"({rs(rev_no)})"],
       {"cls": "sub", "cells": ["<b>Incremental revenue</b>", f"<b>{rs(inc_rev)}</b>",
                                f"<b>{rs(inc_rev*units)}</b>"]},
       ["<i>Less:</i> Rectification cost " + src("the only relevant cost"),
        f"({rs(rect_cost)})", f"({rs(rect_total)})"],
       {"cls": "tot", "cells": ["<b>Net gain from rectifying</b>", f"<b>{rs(net)}</b>",
                                f"<b>{rs(total_net)}</b>"]},
       {"cls": "sub", "cells": ["<b>Decision</b>",
                                {"t": "<b>YES &mdash; rectify the shirts</b>", "a": "r"}, ""]}],
      widths=["52%", "24%", "24%"])

    p34 = f"""<h3 class="sub">(iii) and (iv) &nbsp;Gain or loss under each option</h3>
<p class="small"><b>On the incremental basis</b> &mdash; the answer expected, and the one your class
notes give:</p>
{table(None, [("", ""), ("Per shirt " + R, "r"), ("Total " + R, "r")],
 [[f"<b>(iii) If rectification is NOT done</b> &mdash; the company gives up a net "
   f"{R}{rs(net)} a shirt, so relative to rectifying it is <b>worse off</b> by",
   f"({rs(net)})", f"<b>({rs(total_net)})</b>"],
  [f"<b>(iv) If rectification IS done</b> &mdash; a net gain of",
   f"{rs(net)}", f"<b>{rs(total_net)}</b>"]], headcls="lite", widths=["56%", "20%", "24%"])}
<p class="small" style="margin-top:3mm"><b>Cross-check on the absolute basis</b> &mdash; bringing the
sunk {R}{rs(sunk)} back in, purely to show the size of the loss. Note that the
<i>difference</i> between the two columns is still {R}{rs(total_net)}, which proves the
incremental answer above:</p>
{table(None, [("Particulars", ""), ("Not rectified " + R, "r"), ("Rectified " + R, "r")],
 [["Sales revenue", rs(rev_no), rs(rev_yes)],
  ["<i>Less:</i> Cost of manufacture already incurred " + src("sunk &mdash; shown only for the check"),
   f"({rs(sunk)})", f"({rs(sunk)})"],
  ["<i>Less:</i> Rectification cost", "&mdash;", f"({rs(rect_total)})"],
  {"cls": "tot", "cells": ["<b>Net loss</b>", f"<b>({rs(loss_no)})</b>", f"<b>({rs(loss_yes)})</b>"]},
  {"cls": "sub", "cells": ["<b>Rectifying reduces the loss by</b>", "",
                           f"<b>{rs(total_net)}</b>"]}], headcls="lite",
 widths=["52%", "24%", "24%"])}"""

    return ("<div class='prob long'>"
            + prob_head(no, "Rectify the defectives or sell them as rejects",
                        "Further processing &middot; " + page)
            + question(q) + read(rd) + p1 + p2 + p34
            + why(f"""<p>The whole problem reduces to one line: spending {R}{rs(rect_cost)} brings in
{R}{rs(inc_rev)}, so every shirt rectified is {R}{rs(net)} better off. Multiply by
{rs(units)} shirts and rectification is worth {R}{rs(total_net)}.</p>
<p><b>Why the sunk cost must be ignored, stated for the marks:</b> the {R}{rs(sunk)} spent on
manufacture appears in <i>both</i> columns of the absolute statement above, unchanged. A figure that is
identical under both options cannot possibly discriminate between them. Including it makes both options
look like disasters and tempts you into the wrong conclusion &mdash; that neither should be pursued.
But the shirts cannot be un-made, and refusing to rectify does not recover the money; it merely locks
in the larger loss of {R}{rs(loss_no)} instead of the smaller {R}{rs(loss_yes)}.</p>
<p><b>Recommendation:</b> rectify the defects. The loss on this consignment falls from
{R}{rs(loss_no)} to {R}{rs(loss_yes)} &mdash; an improvement of {R}{rs(total_net)}. The
manufacturing cost is history; the only live question was whether {R}{rs(rect_cost)} could buy more
than {R}{rs(rect_cost)} of extra revenue, and it buys {R}{rs(inc_rev)}.</p>""")
            + ans([("(i) Relevant cost &mdash; rectification",
                    f"{R} {rs(rect_cost)} per shirt = {R} {rs(rect_total)}"),
                   ("&nbsp;&nbsp;&nbsp;&nbsp;Irrelevant &mdash; cost of manufacture",
                    f"{R} {rs(mfg)} per shirt = {R} {rs(sunk)} &nbsp;<i>sunk</i>"),
                   ("Incremental revenue per shirt", f"{R} {rs(inc_rev)}"),
                   ("Net gain per shirt", f"{R} {rs(net)}"),
                   ("<b>(ii) Should rectification be done?</b>",
                    f"<b>YES &mdash; gain of {R} {rs(total_net)}</b>"),
                   ("<b>(iii) If NOT rectified</b>",
                    f"<b>Worse off by {R} {rs(total_net)}</b>"),
                   ("<b>(iv) If rectified</b>", f"<b>Gain of {R} {rs(total_net)}</b>"),
                   ("Absolute loss &mdash; not rectified / rectified",
                    f"{R} {rs(loss_no)} / {R} {rs(loss_yes)}")])
            + "</div>")


def q9():
    return _rectify_solution("Q9", 20000, 150, 120, 30, 160, "p.41&ndash;42")


def q11():
    return _rectify_solution("Q11", 10000, 300, 240, 60, 320, "p.42")


# ======================================================================
# Q10
# ======================================================================
def q10():
    q = f"""<p>A printer has received a special order for the printing of a brochure. A brochure requires
a special type of paper that is not regularly used. A limited quantity of paper (100 reams) is remaining
from a previous job completed in the previous year. The cost of the paper last year was {D}15 per ream.</p>
<p>The brochure requires 250 reams; the current market price is {D}26 per ream. The resale value of the
paper in inventory is {D}10 per ream. Identify the relevant cost of the paper used in the printing of
the brochure.</p>
<p><b>(a)</b> What are the relevant costs in the problem given? <b>(b)</b> Calculate the total
relevant cost.</p>"""

    rd = f"""<p>This is Q2&rsquo;s material C in miniature, and in dollars. Walk the material tree
twice, because the 250 reams required come from two different places.</p>
{bullets([
 '<b>&ldquo;not regularly used&rdquo;</b> &mdash; the 100 reams in stock will <b>not</b> be '
 'replaced. Box &#9314;: the sacrifice is the resale value of ' + D + '10 a ream.',
 '<b>&ldquo;The cost of the paper last year was ' + D + '15&rdquo;</b> &mdash; last year&rsquo;s '
 'money. Sunk, and the largest decoy in the question.',
 '<b>250 required &minus; 100 in stock = 150 reams short.</b> These must be bought at today&rsquo;s ' +
 D + '26. Box &#9312;: out-of-pocket cost.',
 'Do not price all 250 reams at ' + D + '26; and do not price the 100 in stock at ' + D + '15. '
 'Each of those errors is worth a mark.'])}"""

    tbl = rc("Computation of the relevant cost of the paper",
      [("Paper in stock<br/><span class='small'>&mdash; 100 reams</span>",
        f"A special paper that is not regularly used, so it will not be replaced. The only sacrifice "
        f"in using it is the resale proceeds forgone &mdash; <b>opportunity cost at net realisable "
        f"value</b>. {src('100 reams &times; ' + D + '10')}", 1000),
       ("Paper to be purchased<br/><span class='small'>&mdash; 150 reams</span>",
        f"250 reams are required and only 100 are in stock, so 150 reams must be bought at the "
        f"current market price. <b>Out-of-pocket cost.</b> "
        f"{src('(250 &minus; 100) = 150 reams &times; ' + D + '26')}", 3900),
       ("!Historical cost of the paper in stock",
        f"{D}15 per ream was paid last year. <b>Sunk cost &mdash; irrelevant.</b>", "&mdash;")],
      total=("Total relevant cost of the paper", 4900), cur=D)

    return ("<div class='prob'>"
            + prob_head("Q10", "Relevant cost of a material partly held in stock",
                        "Materials &middot; p.42")
            + question(q) + read(rd) + tbl
            + why(f"""<p>Two rows, two different rules, and the reason is simply that the two lots of
paper have different futures:</p>
{bullets([
 'The <b>100 reams already owned</b> cost nothing more to obtain. Using them destroys only the ' +
 D + '1,000 the printer could have raised by selling them. That is the opportunity cost.',
 'The <b>150 reams not owned</b> must be bought with real money at ' + D + '26. That is an '
 'out-of-pocket cost.'])}
<p>The {D}15 historical cost belongs to neither calculation. It measures what the paper <i>cost</i>,
and relevant costing is only ever interested in what a decision <i>changes</i>.</p>
{fml("Total relevant cost &nbsp;=&nbsp; " + D + "1,000 + " + D + "3,900 &nbsp;=&nbsp; " + D + "4,900",
     "This is the floor for quoting the brochure job so far as paper is concerned. Any quotation "
     "must recover at least " + D + "4,900 of paper cost, plus ink, labour and other relevant costs.")}""")
            + ans([("Opportunity cost &mdash; 100 reams at NRV", f"{D} 1,000"),
                   ("Out-of-pocket cost &mdash; 150 reams at market price", f"{D} 3,900"),
                   ("<b>(b) Total relevant cost of the paper</b>", f"<b>{D} 4,900</b>"),
                   ("Excluded as sunk", f"{D} 15 per ream historical cost")])
            + "</div>")


# ======================================================================
# Q12
# ======================================================================
def q12():
    q = f"""<p>A machinery was purchased for {R}26,00,000. The operating cost is {R}130 per hour. When
the machine was about to be installed it was found out that another machine which is more efficient was
available in the market for {R}45,50,000. The operating cost of that machine is {R}91 per hour.</p>
<p>If this new machine is purchased for {R}45,50,000, the old machine could be disposed of for
{R}15,60,000. Consider revenue per hour from the machine as {R}195.</p>
<p><b>(i)</b> Identify the relevant cost. <b>(ii)</b> How many hours does the new machine have to run
for the benefit of the company? <b>(iii)</b> Calculate the break-even hours of both the machines.</p>"""

    rd = f"""<p>Structurally this is Q8 with every figure multiplied by 1.3. Use exactly the same four
steps &mdash; that is the point of the method page, and it is why the two problems are set together.</p>
{bullets([
 'Contribution per hour: old = ' + R + '195 &minus; ' + R + '130 = ' + R + '65; new = ' + R
 + '195 &minus; ' + R + '91 = ' + R + '104.',
 'Incremental investment = ' + R + '45,50,000 &minus; ' + R + '15,60,000 = ' + R + '29,90,000.',
 'The ' + R + '26,00,000 already paid for the old machine is <b>sunk</b> for parts (i) and (ii), '
 'and comes back in only for part (iii).',
 '<b>Watch the ending of this one.</b> In Q8 the new machine broke even sooner than the old; here it '
 'breaks even <b>later</b> (43,750 hours against 40,000). Compute, do not assume.'])}"""

    ph = f"""<h4 class="mini">W1 &nbsp;Contribution per hour of each machine</h4>
{table(None, [("Particulars", ""), ("Old machine " + R, "r"), ("New machine " + R, "r")],
 [["Revenue per hour", "195", "195"],
  ["<i>Less:</i> Operating cost per hour", "(130)", "(91)"],
  {"cls": "tot", "cells": ["<b>Contribution per hour</b>", "<b>65</b>", "<b>104</b>"]}],
 headcls="lite", widths=["52%", "24%", "24%"])}

<h4 class="mini">W2 &nbsp;Incremental investment in switching</h4>
{calc([f'Cost of the new machine &nbsp;=&nbsp; {R}45,50,000',
       f'<i>Less:</i> Disposal value of the old machine &nbsp;=&nbsp; ({R}15,60,000)',
       f'<b>Incremental investment &nbsp;=&nbsp; {R}29,90,000</b>'])}"""

    p1 = rc("(i) Identification of the relevant cost",
      [("Operating cost &mdash; old machine",
        f"{R}130 per hour. Differs between the alternatives &mdash; relevant.", f"{R}130 / hr"),
       ("Cost of the new machine",
        f"Fresh cash outflow caused only by the decision to switch. Relevant. {src('given')}",
        4550000),
       ("Operating cost &mdash; new machine",
        f"{R}91 per hour. Differs between the alternatives &mdash; relevant.", f"{R}91 / hr"),
       ("NRV of the old machine",
        f"Cash inflow available only if the switch is made. Relevant &mdash; deduct from the "
        f"investment. {src('given, disposal value')}", 1560000),
       ("Revenue per hour",
        f"{R}195 from either machine, needed for contribution per hour.", f"{R}195 / hr"),
       ("!Purchase price of the old machine",
        f"{R}26,00,000 is already committed and unrecoverable by any present decision. <b>Sunk</b> "
        f"&mdash; irrelevant for parts (i) and (ii).", "&mdash;")],
      total=("Incremental investment &nbsp;(45,50,000 &minus; 15,60,000)", 2990000))

    p2 = f"""<h3 class="sub">(ii) Hours the new machine must run for the benefit of the company</h3>
{fml("Hours required &nbsp;=&nbsp; " + frac("Incremental investment", "Contribution per hour of the new machine")
     + " &nbsp;=&nbsp; " + frac(R + "29,90,000", R + "104") + " &nbsp;=&nbsp; <b>28,750 hours</b>")}
<p class="small">Run the new machine for more than 28,750 hours and the {R}29,90,000 net outlay on
switching has been recovered out of its superior contribution.</p>"""

    p3 = f"""<h3 class="sub">(iii) Break-even hours of each machine</h3>
<p class="small">Full purchase cost of each machine, recovered out of its own contribution per hour.</p>
{table(None, [("Machine", ""), ("Computation", ""), ("Break-even hours", "r")],
 [["<b>Machine 1 &mdash; old</b>",
   frac(R + "26,00,000", R + "195 &minus; " + R + "130") + " &nbsp;=&nbsp; "
   + frac(R + "26,00,000", R + "65"), "<b>40,000 hours</b>"],
  ["<b>Machine 2 &mdash; new</b>",
   frac(R + "45,50,000", R + "195 &minus; " + R + "91") + " &nbsp;=&nbsp; "
   + frac(R + "45,50,000", R + "104"), "<b>43,750 hours</b>"]],
 headcls="lite", widths=["24%", "50%", "26%"])}"""

    return ("<div class='prob long'>"
            + prob_head("Q12", "Machine replacement &mdash; the same method, different numbers",
                        "Machine &middot; p.42")
            + question(q) + read(rd) + wn(ph) + p1 + p2 + p3
            + why(f"""<p>Compare the two answers in part (iii) with Q8 and something interesting
appears. Here the new machine takes <b>longer</b> to break even &mdash; 43,750 hours against the old
machine&rsquo;s 40,000 &mdash; yet buying it is still the right decision. Those two facts sit together
uncomfortably, and reconciling them is the real content of this problem:</p>
{bullets([
 '<b>Break-even hours answer a question about one machine in isolation:</b> &ldquo;how long before '
 'this asset has paid for itself?&rdquo; The new machine costs 75% more, so on that test it looks '
 'slower.',
 '<b>The switching decision is about the margin:</b> the extra ' + R + '29,90,000 buys an extra ' +
 R + '39 of contribution every hour (104 &minus; 65), and recovers itself in 28,750 hours &mdash; '
 'well before either machine&rsquo;s own break-even point.',
 '<b>And the ' + R + '26,00,000 is gone regardless.</b> Keeping the old machine does not refund it. '
 'The only live choice is which machine to run from here, and the new one earns ' + R + '39 more '
 'an hour.'])}
<p><b>Recommendation:</b> buy the new machine, provided the expected running time exceeds 28,750
hours. Report the break-even hours of 40,000 and 43,750 as answers to part (iii), but make clear in
one sentence that they are a cost-recovery measure and <b>not</b> the basis of the replacement
decision &mdash; that distinction is what part (iii) is really testing.</p>""")
            + ans([("Contribution per hour &mdash; old / new", f"{R} 65 / {R} 104"),
                   ("<b>(i) Incremental investment (relevant)</b>", f"<b>{R} 29,90,000</b>"),
                   ("&nbsp;&nbsp;&nbsp;&nbsp;Excluded as sunk",
                    f"{R} 26,00,000 cost of the old machine"),
                   ("<b>(ii) Hours for the benefit of the company</b>", "<b>28,750 hours</b>"),
                   ("<b>(iii) Break-even hours &mdash; old machine</b>", "<b>40,000 hours</b>"),
                   ("<b>(iii) Break-even hours &mdash; new machine</b>", "<b>43,750 hours</b>"),
                   ("<b>Decision</b>",
                    "<b>Buy the new machine if it will run &gt; 28,750 hours</b>")])
            + "</div>")


# ======================================================================
# Q13
# ======================================================================
def q13():
    q = f"""<p>The cost of making component Q, which forms part of Product Y, is given below:</p>
{table(None, [("Particulars", ""), ("Cost per unit in " + R, "r")],
 [["Raw materials", "4"], ["Direct labour", "8"], ["Production overheads (60% variable)", "16"],
  {"cls": "tot", "cells": ["<b>Total</b>", "<b>28</b>"]}], headcls="lite", widths=["70%", "30%"])}
<p>Component Q could be bought from an outside supplier for {R}20 per unit. State whether the company
should make or buy component Q.</p>"""

    rd = f"""<p>A three-line question with one instruction hidden in a bracket. Everything depends on
<b>&ldquo;(60% variable)&rdquo;</b>.</p>
{bullets([
 '<b>Split the production overhead before doing anything else:</b> 60% of ' + R + '16 = ' + R
 + '9.60 is variable and relevant; the remaining 40% = ' + R + '6.40 is fixed and continues whether '
 'or not the component is made in-house. Strike it out.',
 '<b>Never compare the ' + R + '28 total with the ' + R + '20 buying price.</b> That comparison says '
 '&ldquo;buy, saving ' + R + '8&rdquo; and it is wrong, because ' + R + '6.40 of that ' + R + '28 '
 'will be incurred anyway.',
 'Raw materials and direct labour are variable in full, so both are relevant.',
 'Here, unusually for a textbook make-or-buy, the answer really is <b>buy</b> &mdash; but for a '
 'saving of ' + R + '1.60, not ' + R + '8.'])}"""

    main = table("Cost of making component Q &mdash; relevant cost only",
      [("Particulars", ""), ("Nature", ""), ("Amount " + R, "r")],
      [["Raw materials", "Variable &mdash; relevant", "4.00"],
       ["Direct labour", "Variable &mdash; relevant", "8.00"],
       ["Production overheads &mdash; variable portion<br/>"
        + src("60% of " + R + "16"),
        "Variable &mdash; relevant", "9.60"],
       {"cls": "irr",
        "cells": ["<b>Production overheads &mdash; fixed portion</b><br/>"
                  + src("40% of " + R + "16 = " + R + "6.40"),
                  "Fixed &mdash; incurred whether the component is made or bought. "
                  "<b>Irrelevant.</b>", "&mdash;"]},
       {"cls": "tot", "cells": ["<b>Relevant cost of MAKING component Q</b>",
                                "4 + 8 + 9.60", "<b>21.60</b>"]},
       {"cls": "sub", "cells": ["<b>Cost of BUYING component Q</b>",
                                "quoted by the outside supplier", "<b>20.00</b>"]},
       {"cls": "tot", "cells": ["<b>Saving per unit by buying</b>",
                                f"{R}21.60 &minus; {R}20.00", "<b>1.60</b>"]}],
      widths=["36%", "42%", "22%"])

    return ("<div class='prob'>"
            + prob_head("Q13", "Make or buy &mdash; splitting a semi-variable overhead",
                        "Make or buy &middot; p.42&ndash;43")
            + question(q) + read(rd) + main
            + why(f"""<p>The whole problem is the bracket &ldquo;(60% variable)&rdquo;, and it works in
the opposite direction from the usual textbook case. Normally stripping out fixed overhead makes
<i>making</i> look cheaper and reverses a naive &ldquo;buy&rdquo; decision. Here the fixed element is
small enough that buying still wins &mdash; but the <b>size</b> of the advantage changes completely,
and that is what is being marked.</p>
{table(None, [("", ""), ("Naive comparison", ""), ("Correct comparison", "")],
 [["Cost of making", f"{R}28.00 &mdash; the full total", f"{R}21.60 &mdash; variable only"],
  ["Cost of buying", f"{R}20.00", f"{R}20.00"],
  ["Apparent saving by buying", f"{R}8.00", f"<b>{R}1.60</b>"],
  ["Decision", "Buy", "Buy"],
  ["Is it safe?", "Overstates the gain five-fold",
   "A thin margin &mdash; report it as such"]], headcls="lite", widths=["26%", "37%", "37%"])}
<p><b>Recommendation:</b> buy component Q from the outside supplier at {R}20, saving {R}1.60 per
unit. But say plainly that the margin is narrow. Two things follow from that, and stating either earns
credit:</p>
{bullets([
 'The ' + R + '6.40 of fixed overhead does not disappear on buying &mdash; it must be reabsorbed by '
 'the remaining products, so the reported cost of Product Y will rise even though the company is '
 'better off in cash terms.',
 'If the released capacity can earn anything at all &mdash; even ' + R + '2 per unit of '
 'contribution from another component &mdash; buying becomes clearly correct rather than marginally '
 'so. Conversely, a small rise in the supplier&rsquo;s price wipes the advantage out.'])}""")
            + ans([("Relevant cost of making &nbsp;(4 + 8 + 9.60)", f"{R} 21.60 per unit"),
                   ("Cost of buying", f"{R} 20.00 per unit"),
                   ("Fixed overhead excluded", f"{R} 6.40 per unit &nbsp;(40% of {R} 16)"),
                   ("<b>Decision</b>", f"<b>BUY component Q</b>"),
                   ("<b>Saving</b>", f"<b>{R} 1.60 per unit</b>")])
            + "</div>")


# ======================================================================
# Q14
# ======================================================================
def q14():
    q = f"""<p>The selling price of Product X is {R}22 and the production cost for one unit is:</p>
{table(None, [("Particulars", ""), ("Cost per unit in " + R, "r")],
 [["Raw materials", "8"], ["Direct labour", "4"], ["Production overheads", "8"],
  {"cls": "tot", "cells": ["<b>Total</b>", "<b>20</b>"]}], headcls="lite", widths=["70%", "30%"])}
<p>Variable production overhead, which is part of production overhead, is calculated at 50% of labour
cost. There is a possibility of supplying a special order for 2,000 units of Product X at {R}16 each.
If this order is accepted, the normal budgeted sales would not get affected and the company has the
necessary capacity to produce the additional units. State whether the company should accept the special
order.</p>"""

    rd = f"""<p>The special-order price of {R}16 is below the total cost of {R}20, which is precisely
why the question is set. Accepting it is still correct, and the reason is one line of arithmetic buried
in the words.</p>
{bullets([
 '<b>&ldquo;Variable production overhead &hellip; is calculated at 50% of labour cost&rdquo;</b> '
 '&mdash; so variable overhead = 50% &times; ' + R + '4 = <b>' + R + '2</b>, and the fixed part of '
 'the production overhead is ' + R + '8 &minus; ' + R + '2 = <b>' + R + '6</b>. Note the percentage '
 'is applied to <i>labour cost</i>, not to the ' + R + '8 overhead.',
 '<b>&ldquo;the normal budgeted sales would not get affected&rdquo;</b> &mdash; no existing '
 'contribution is sacrificed, so there is no opportunity cost.',
 '<b>&ldquo;the company has the necessary capacity&rdquo;</b> &mdash; spare capacity, so the fixed '
 'overhead of ' + R + '6 per unit will be incurred anyway and does not increase. It is therefore '
 'irrelevant to this order.',
 'With those three phrases in hand, the relevant cost is ' + R + '8 + ' + R + '4 + ' + R + '2 = ' +
 R + '14, comfortably below the ' + R + '16 offered.'])}"""

    main = table("Computation of the relevant cost of the special order",
      [("Particulars", ""), ("Nature", ""), ("Per unit " + R, "r")],
      [["Raw materials", "Variable &mdash; relevant", "8"],
       ["Direct labour", "Variable &mdash; relevant", "4"],
       ["Production overheads &mdash; variable portion<br/>"
        + src("50% of direct labour " + R + "4"),
        "Variable &mdash; relevant", "2"],
       {"cls": "irr",
        "cells": ["<b>Production overheads &mdash; fixed portion</b><br/>"
                  + src(R + "8 &minus; " + R + "2 = " + R + "6"),
                  "Spare capacity exists, so this is incurred anyway. <b>Irrelevant.</b>",
                  "&mdash;"]},
       {"cls": "tot", "cells": ["<b>Total relevant cost per unit</b>", "8 + 4 + 2", "<b>14</b>"]},
       {"cls": "sub", "cells": ["<b>Selling price per unit of the special order</b>",
                                "given", "<b>16</b>"]},
       {"cls": "tot", "cells": ["<b>Additional contribution per unit</b>",
                                f"{R}16 &minus; {R}14", "<b>2</b>"]}],
      widths=["34%", "44%", "22%"])

    tot = stmt("Effect of accepting the order on total profit",
      ["Amount " + R],
      [("Additional contribution per unit " + src("16 &minus; 14"), ["2"]),
       ("Number of units in the special order", ["2,000"]),
       ("<b>Increase in total profit</b> " + src(R + "2 &times; 2,000 units"), ["<b>4,000</b>"],
        "tot")])

    return ("<div class='prob'>"
            + prob_head("Q14", "Accepting a special order priced below total cost",
                        "Special order &middot; p.43")
            + question(q) + read(rd) + main + tot
            + why(f"""<p>At first sight the order is absurd: {R}16 for something that costs {R}20 to
produce. The resolution is that {R}6 of that {R}20 is fixed overhead which the company pays whether
or not it accepts the order. Against the costs that <b>actually change</b> &mdash; {R}14 of
materials, labour and variable overhead &mdash; the {R}16 leaves {R}2 over.</p>
{fml("Additional profit &nbsp;=&nbsp; (" + R + "16 &minus; " + R + "14) &times; 2,000 units "
     "&nbsp;=&nbsp; " + R + "4,000",
     "Total profit rises by exactly this amount, because total fixed cost is unchanged. Nothing else "
     "in the accounts moves.")}
<p><b>Recommendation:</b> accept the special order. It generates an additional contribution of
{R}4,000, and since fixed costs do not change, total profit rises by the same {R}4,000.</p>
<p><b>The two conditions that make this true &mdash; state them.</b> They are given in the question
precisely so that you will quote them back:</p>
{bullets([
 '<b>Spare capacity exists</b>, so no extra fixed cost is incurred and no existing production is '
 'displaced. Without spare capacity the contribution lost on displaced regular sales would be an '
 'opportunity cost, and at ' + R + '22 &minus; ' + R + '14 = ' + R + '8 of contribution per regular '
 'unit the order would be plainly unprofitable.',
 '<b>Normal budgeted sales are unaffected</b>, so there is no risk of the ' + R + '16 price leaking '
 'into the regular market. If regular customers learned of it and demanded the same price, the ' +
 R + '4,000 gain would be dwarfed by the loss on ordinary sales. Segregating the special order '
 '&mdash; typically an export or own-label market &mdash; is what makes it safe.'])}""")
            + ans([("Relevant cost per unit &nbsp;(8 + 4 + 2)", f"{R} 14"),
                   ("Fixed overhead excluded", f"{R} 6 per unit"),
                   ("Special order price", f"{R} 16 per unit"),
                   ("Additional contribution per unit", f"{R} 2"),
                   ("<b>Increase in total profit</b>",
                    f"<b>{R} 4,000 &nbsp;({R} 2 &times; 2,000 units)</b>"),
                   ("<b>Decision</b>", "<b>ACCEPT the special order</b>")])
            + "</div>")


# ======================================================================
# Q15
# ======================================================================
def q15():
    q = f"""<p>The production manager of your organisation has approached you for some costing advice on
project X, a special order from overseas for {R}30,000. The costs associated with the project are as
follows:</p>
{table(None, [("Particulars", ""), ("Cost in " + R, "r")],
 [["Raw Material &mdash; A", "4,000"], ["Raw Material &mdash; B", "8,000"],
  ["Direct Labour", "6,000"], ["Supervision", "2,000"], ["Overheads", "12,000"],
  {"cls": "tot", "cells": ["<b>Total</b>", "<b>32,000</b>"]}], headcls="lite", widths=["70%", "30%"])}
<p>You ascertain the following:</p>
{bullets([
 '<b>i)</b> Material A is in stock and the above was the cost. This material is of no use to the '
 'organisation other than the above project. If this material is not used, it could be realised at ' +
 R + '1,750.',
 '<b>ii)</b> The organisation has no stock of material B. The required material for the project has '
 'to be ordered at the cost shown above.',
 '<b>iii)</b> Direct labour cost of ' + R + '6,000 relates to workers that will be transferred to '
 'this project from another project. Extra labour will need to be recruited to the other project at '
 'a cost of ' + R + '7,000.',
 '<b>iv)</b> Supervision costs have been charged to the project on the basis of 1/3 of labour cost '
 'and will be carried out by existing staff within their normal duties.',
 '<b>v)</b> Overheads have been charged to the project at the rate of 200% on direct labour.',
 '<b>vi)</b> A new machine has to be purchased specially for the project at a cost of ' + R + '8,000 '
 'and then disposed of at ' + R + '5,000 at the end of the project.'])}
<p><b>a)</b> Find out the relevant costs for the special order, whether to accept or to reject the
special order. <b>b)</b> Should the special order be accepted or rejected?</p>"""

    rd = f"""<p>This is the module&rsquo;s summary problem: <b>every rule appears exactly once</b>. The
printed total of {R}32,000 exceeds the {R}30,000 offered, so a careless answer rejects the order. Work
through notes (i) to (vi) in order &mdash; each one is a complete instruction about a single line.</p>
{table(None, [("Line", ""), ("The note tells you", ""), ("Rule applied", "")],
 [["Material A", "In stock, no other use, realisable at " + R + "1,750",
   "Box &#9314; &mdash; opportunity cost at NRV, <b>not</b> the " + R + "4,000 book cost"],
  ["Material B", "No stock, must be ordered",
   "Box &#9312; &mdash; out-of-pocket cost, take the full " + R + "8,000"],
  ["Direct labour", "Workers <b>transferred</b>; replacements cost " + R + "7,000",
   "The " + R + "6,000 is committed; the <b>" + R + "7,000 caused elsewhere</b> is the real "
   "out-of-pocket cost"],
  ["Supervision", "Existing staff, within normal duties, charged as 1/3 of labour",
   "Apportioned and committed &mdash; <b>Nil</b>"],
  ["Overheads", "Charged at 200% of direct labour",
   "Absorption, not incremental cash &mdash; <b>Nil</b>"],
  ["New machine", "Bought for " + R + "8,000, sold for " + R + "5,000 after",
   "A <b>specific</b> fixed cost &mdash; relevant, net of residual value"]],
 headcls="lite", widths=["17%", "38%", "45%"])}
<p><b>The direct labour line is the hardest in the module and it is worth dwelling on.</b> The
{R}6,000 is not relevant, because those workers are already employed and paid. But the decision does
cause a cash outflow &mdash; taking them off the other project forces the recruitment of replacements
at {R}7,000. So the relevant figure is {R}7,000: <i>higher</i> than the amount printed, and located
in a different project altogether. Relevant cost follows the consequences of a decision wherever they
land, not the line in the cost sheet.</p>"""

    tbl = rc("(a) Computation of the relevant cost of the special order",
      [("Raw Material A",
        f"In stock and of no use to the organisation on any other work. It will not be replaced, so "
        f"the sacrifice is the realisable value forgone &mdash; <b>opportunity cost</b>. The "
        f"{R}4,000 already paid is sunk. {src('realisable value ' + R + '1,750, NOT the ' + R + '4,000 cost')}",
        1750),
       ("Raw Material B",
        f"No stock is held, so the whole requirement must be ordered and paid for. "
        f"<b>Out-of-pocket cost</b> &mdash; relevant. {src('given, ' + R + '8,000')}", 8000),
       ("Direct Labour",
        f"The {R}6,000 relates to workers already employed who are merely transferred &mdash; a "
        f"<b>committed cost</b>, hence irrelevant. But the transfer forces the recruitment of extra "
        f"labour for the other project at {R}7,000, and <b>that</b> is an out-of-pocket cost caused "
        f"by accepting this order. {src('extra recruitment ' + R + '7,000, not the ' + R + '6,000 transferred')}",
        7000),
       ("Supervision",
        f"Charged at 1/3 of labour cost as a book apportionment, and will be carried out by existing "
        f"staff within their normal duties. No additional cash &mdash; <b>irrelevant</b>. "
        f"{src(R + '2,000 excluded')}", 0),
       ("Overheads",
        f"Absorbed at 200% of direct labour. A recovery rate, not an incremental cost; total "
        f"overhead expenditure does not change. <b>Irrelevant.</b> {src(R + '12,000 excluded')}", 0),
       ("New machinery",
        f"Bought <b>specially</b> for this project, so it is a specific fixed cost and is relevant. "
        f"Net it against the disposal proceeds at the end of the project. "
        f"{src(R + '8,000 &minus; ' + R + '5,000')}", 3000)],
      total=("Total relevant cost of the special order", 19750))

    dec = stmt("(b) Decision", ["Amount " + R],
      [("Price offered for the special order " + src("given, overseas order"), ["30,000"]),
       ("<i>Less:</i> Total relevant cost " + src("from the statement above"), ["(19,750)"]),
       ("<b>Net benefit from accepting the order</b>", ["<b>10,250</b>"], "tot"),
       ("<b>Decision</b>", ["<b>ACCEPT the special order</b>"], "sub")])

    contrast = table("Why the printed cost sheet gives the wrong answer",
      [("Particulars", ""), ("As printed " + R, "r"), ("Relevant " + R, "r"), ("Why it changed", "")],
      [["Raw Material A", "4,000", "1,750", "Sunk cost replaced by opportunity cost at NRV"],
       ["Raw Material B", "8,000", "8,000", "Genuine out-of-pocket cost &mdash; unchanged"],
       ["Direct Labour", "6,000", "7,000",
        "Committed cost replaced by the <b>higher</b> cost of replacement labour elsewhere"],
       ["Supervision", "2,000", "&mdash;", "Apportioned to the project; existing staff, no extra cash"],
       ["Overheads", "12,000", "&mdash;", "Absorbed at 200% of labour; total overhead does not change"],
       ["New machinery", "&mdash;", "3,000",
        "Omitted from the cost sheet altogether, yet caused entirely by this decision"],
       {"cls": "tot", "cells": ["<b>Total</b>", "<b>32,000</b>", "<b>19,750</b>", ""]},
       {"cls": "sub", "cells": ["<b>Against the price of " + R + "30,000</b>",
                                "<b>REJECT</b>", "<b>ACCEPT</b>",
                                "<b>the two approaches give opposite decisions</b>"]}],
      widths=["19%", "14%", "14%", "53%"])

    return ("<div class='prob long'>"
            + prob_head("Q15", "The complete relevant-cost decision &mdash; every rule in one problem",
                        "Special order &middot; p.43&ndash;44")
            + question(q) + read(rd) + tbl + dec + contrast
            + why(f"""<p>This problem is the best argument in the whole syllabus for learning relevant
costing. The cost sheet the production manager brought says the project costs {R}32,000 and earns
{R}30,000 &mdash; a loss of {R}2,000, so refuse it. The relevant-cost statement says it costs
{R}19,750 and earns {R}30,000 &mdash; a gain of {R}10,250, so take it. <b>The two answers are
opposite, and only one of them is right.</b></p>
<p>Three things went wrong in the printed sheet, and each is a lesson:</p>
{steps([
 '<b>It charged costs that will not change.</b> Supervision and overheads together account for ' +
 R + '14,000 of the ' + R + '32,000, and not one rupee of it is caused by this project. Both are '
 'internal allocations designed for routine product costing, where spreading fixed costs is exactly '
 'right &mdash; and for one-off decisions is exactly wrong.',
 '<b>It used a historical cost where a sacrifice was needed.</b> Material A is valued at the ' +
 R + '4,000 paid for it, when the only thing actually given up is the ' + R + '1,750 it could be '
 'sold for. That overstated the cost by ' + R + '2,250.',
 '<b>It missed a cost entirely.</b> The net ' + R + '3,000 on the machine bought specially for the '
 'project appears nowhere in the cost sheet, although it is the most obviously decision-driven '
 'figure in the whole question. Absorption systems record what has been spent; they do not ask what '
 'a decision will cause.'])}
<p><b>Recommendation:</b> accept the special order. It yields a net benefit of {R}10,250 in cash
terms. Add the standard caution for full marks: the {R}30,000 price should not be allowed to set a
precedent for other customers, since it recovers no share of general fixed overhead and would be
unsustainable as a general price.</p>""")
            + ans([("Raw Material A &mdash; NRV as opportunity cost", f"{R} 1,750"),
                   ("Raw Material B &mdash; out-of-pocket", f"{R} 8,000"),
                   ("Direct Labour &mdash; extra recruitment elsewhere", f"{R} 7,000"),
                   ("Supervision", "<b>Nil</b> &mdash; apportioned, existing staff"),
                   ("Overheads", "<b>Nil</b> &mdash; absorbed at 200% of labour"),
                   ("New machinery &nbsp;(8,000 &minus; 5,000)", f"{R} 3,000"),
                   ("<b>(a) Total relevant cost</b>", f"<b>{R} 19,750</b>"),
                   ("Price offered", f"{R} 30,000"),
                   ("<b>Net benefit</b>", f"<b>{R} 10,250</b>"),
                   ("<b>(b) Decision</b>", "<b>ACCEPT the special order</b>")])
            + "</div>")


# ======================================================================
def build():
    return (opener()
            + q1() + q2() + q3() + q4() + q5() + q6() + q7()
            + machine_playbook() + q8() + q12()
            + rectify_playbook() + q9() + q11()
            + q10() + q13() + q14() + q15())
