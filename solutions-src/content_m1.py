# -*- coding: utf-8 -*-
"""MODULE 1 - PROCESS COSTING  (24 problems)"""
from build import (esc, rs, money, frac, prob_head, question, read, method, wn,
                   trap, why, steps, bullets, fml, calc, ans, table, src,
                   arrow_panel, module_opener)

R = "&#8377;"          # rupee sign


# ======================================================================
# helper: two-sided ledger account  (Dr | Cr)
# ======================================================================
def acct(caption, dr, cr, note=None, units=True):
    """
    dr / cr : list of rows. Each row is a tuple:
        (particulars, units, rate, amount)   -- units/rate may be "" or None
      or the marker ("TOT", units, rate, amount) to style as total row.
    Values that are numbers get Indian-formatted; strings pass through.
    """
    def fmt(v, dp=None):
        if v is None or v == "":
            return "&mdash;"
        if isinstance(v, str):
            return v
        return money(v, dp)

    n = max(len(dr), len(cr))
    h = f"<table class='acct'><caption>{caption}</caption><thead><tr>"
    if units:
        h += ("<th>Particulars</th><th class='r'>Units</th><th class='r'>Rate</th>"
              f"<th class='r'>Amount {R}</th>"
              "<th class='mid'>Particulars</th><th class='r'>Units</th>"
              f"<th class='r'>Rate</th><th class='r'>Amount {R}</th>")
    else:
        h += (f"<th>Particulars</th><th class='r'>Amount {R}</th>"
              f"<th class='mid'>Particulars</th><th class='r'>Amount {R}</th>")
    h += "</tr></thead><tbody>"
    for i in range(n):
        a = dr[i] if i < len(dr) else None
        b = cr[i] if i < len(cr) else None
        cls = ""
        if (a and a[0] == "TOT") or (b and b[0] == "TOT"):
            cls = "tot"
        h += f"<tr class='{cls}'>"
        for side, row in (("", a), ("mid", b)):
            if row is None:
                if units:
                    h += (f"<td class='{side}'></td><td></td><td></td><td></td>")
                else:
                    h += f"<td class='{side}'></td><td></td>"
                continue
            lab = "<b>Total</b>" if row[0] == "TOT" else row[0]
            if units:
                h += (f"<td class='{side}'>{lab}</td>"
                      f"<td class='r'>{fmt(row[1],0)}</td>"
                      f"<td class='r'>{fmt(row[2])}</td>"
                      f"<td class='r'>{fmt(row[3])}</td>")
            else:
                h += (f"<td class='{side}'>{lab}</td>"
                      f"<td class='r'>{fmt(row[1])}</td>")
        h += "</tr>"
    h += "</tbody></table>"
    if note:
        h += f"<div class='small'>{note}</div>"
    return h


# ======================================================================
# MODULE OPENER  +  PLAYBOOK
# ======================================================================
def opener():
    intro = f"""
<h2 class="sec">What this module actually is</h2>
<p>Process costing is used where a product is made in a <b class="k">continuous chain of
stages</b> &mdash; sugar, chemicals, oil, paper, cement. You cannot point at one unit and say
&ldquo;this one cost <span class="rs">{R}</span>40&rdquo;, because every unit goes through the
same pipe. So we do the only thing possible: <b class="k">total the cost of a process and
divide by the units it produced</b>. That single sentence is the whole module.</p>

<p>Everything else in these 24 problems is one of four complications layered on top of that
idea:</p>

{table(None,
  [("Complication","" ),("What changes","" ),("Problems","c")],
  [["<b>Nothing &mdash; plain chain</b>",
    "Total each process, divide by units, carry the total forward to the next process.",
    "<b>1&ndash;4</b>"],
   ["<b>Some units are lost</b>",
    "Part of the input disappears (evaporation, spoilage). Expected loss is <i>normal</i> and its "
    "cost is absorbed by the good units. Anything worse is <i>abnormal loss</i>; anything better "
    "is <i>abnormal gain</i>. Both are taken out of the process at the good-unit rate.",
    "<b>5&ndash;9</b>"],
   ["<b>Two or more products emerge</b>",
    "One process throws out several saleable products. The joint cost has to be split between "
    "them &mdash; usually by working <i>backwards</i> from selling price.",
    "<b>10&ndash;14</b>"],
   ["<b>Each process adds profit</b>",
    "A process sells to the next at cost + profit. The profit inside unsold stock is not real "
    "yet, so a <i>reserve for unrealised profit</i> must be removed.",
    "<b>15&ndash;16</b>"],
   ["<b>Some units are half-finished</b>",
    "Closing work-in-progress is 60% done. You convert part-finished units into "
    "<i>equivalent</i> finished units before dividing.",
    "<b>17&ndash;24</b>"]],
  headcls="lite", widths=["22%","62%","16%"])}

<h2 class="sec" style="margin-top:7mm">The one habit that solves every problem in this module</h2>
<p>Before you write a single figure, do this on your rough sheet. It takes forty seconds and it
is the difference between a full-marks answer and a mess.</p>

{arrow_panel(500, 152, [
  {"box": (6, 8, 108, 30, "STEP 1|Count the units in", "#fdf6e6"), "fs": 8.2},
  {"box": (128, 8, 108, 30, "STEP 2|Count the units out", "#fdf6e6"), "fs": 8.2},
  {"box": (250, 8, 108, 30, "STEP 3|Do they match?", "#fdf6e6"), "fs": 8.2},
  {"box": (372, 8, 122, 30, "STEP 4|Name the difference", "#fdf6e6"), "fs": 8.2},
  {"line": (114, 23, 126, 23)},
  {"line": (236, 23, 248, 23)},
  {"line": (358, 23, 370, 23)},
  {"box": (6, 62, 232, 26, "Opening WIP + units introduced/received", "#eaf5f4"), "fs": 8.2},
  {"box": (262, 62, 232, 26, "Transferred out + closing WIP + loss", "#eaf5f4"), "fs": 8.2},
  {"txt": (250, 79, "=", 13, "#0d6058", "middle")},
  {"box": (6, 104, 488, 38,
    "If the two sides do not agree, you have missed a loss or a gain.|"
    "Find it NOW. Every later figure depends on this line balancing.",
    "#fdeeec"), "fs": 8.2, "stroke": "#c0392b", "fg": "#98271b"},
], "The units reconciliation. Write it for every process, every time.")}

<div class="blk read"><span class="lab">The three rate formulas &mdash; this is all the arithmetic there is</span>
{fml("Cost per unit (no loss) &nbsp;=&nbsp; "
     + frac("Total cost of the process", "Units produced"))}
{fml("Cost per good unit (with loss) &nbsp;=&nbsp; "
     + frac("Total cost &minus; Scrap value of normal loss",
            "Input units &minus; Normal loss units"),
     "Learn this one properly. Normal loss is removed from BOTH the top and the bottom. "
     "Abnormal loss and abnormal gain are then valued at this same rate &mdash; never at a "
     "different one.")}
{fml("Cost per unit (part-finished stock) &nbsp;=&nbsp; "
     + frac("Cost of that element", "Equivalent units of that element"),
     "Material, labour and overhead each get their own rate, because they are each at a "
     "different stage of completion.")}
</div>
"""
    return module_opener("Module One", "Process Costing",
                         "24 problems &nbsp;&middot;&nbsp; workbook pages 8 to 16", intro)


# ======================================================================
# PROBLEM 1
# ======================================================================
def q1():
    q = f"""<p>There are three distinct processes A, B and C. During the four-week period
1,000 units are produced and the following information is available.</p>
{table(None, [("Particulars",""),("Process A","r"),("Process B","r"),("Process C","r")],
 [["Direct materials","2,000","1,000","&mdash;"],
  ["Direct wages","1,500","700","800"],
  ["Direct expenses","300","100","&mdash;"]], headcls="lite")}
<p>The indirect production cost were <span class="rs">{R}</span>4,500 and these are to be
apportioned on the basis of direct wage cost. Prepare the process accounts.</p>"""

    rd = f"""<p>Three things to notice, and they decide the whole answer:</p>
{bullets([
 '<b>&ldquo;1,000 units are produced&rdquo;</b> &mdash; one figure for all three processes. '
 'So there is <b>no loss anywhere</b>. 1,000 units go in, 1,000 come out of every process. '
 'That means no normal loss working, no abnormal loss &mdash; the easiest kind.',
 '<b>&ldquo;apportioned on the basis of direct wage cost&rdquo;</b> &mdash; the question hands you '
 'the basis. You do not have to guess it. Whenever a question gives you a lump overhead and a '
 'basis, your first working note is always the same: find the ratio, then split.',
 '<b>Process C has no materials and no direct expenses.</b> Do not panic and do not leave the '
 'row out &mdash; write a dash. An examiner wants to see that you looked and found nothing.'])}"""

    mt = steps([
        "Add up the given basis across all processes (here: total direct wages).",
        "Overhead rate = Total indirect cost &divide; Total basis. Keep it as a plain number "
        "or a percentage &mdash; whichever divides cleanly.",
        "Multiply each process's basis by that rate. <b>Check the three pieces add back to the "
        "original lump sum</b> before you go on.",
        "Open Process A. Debit its own four costs. Total it. That total transfers out to B.",
        "Open Process B. <b>First debit is the transfer from A</b>, then B's own costs. Total, "
        "transfer to C.",
        "Open Process C the same way. Its total goes to Finished Stock.",
        "Divide each process total by 1,000 to show cost per unit. The last one is the answer "
        "the examiner is looking for."])

    wnh = f"""<h4 class="mini">W1 &nbsp;Apportionment of indirect production cost</h4>
{calc([f'Total direct wages &nbsp;=&nbsp; 1,500 + 700 + 800 &nbsp;=&nbsp; <b>{R}3,000</b>',
       f'Overhead rate &nbsp;=&nbsp; {R}4,500 &divide; {R}3,000 &nbsp;=&nbsp; '
       f'<b>1.5 times the wages</b> &nbsp;(i.e. 150% of direct wages)'])}
{table(None, [("Process",""),("Direct wages","r"),("&times; 1.5","r"),("Overhead absorbed","r")],
 [["A","1,500","1,500 &times; 1.5","<b>2,250</b>"],
  ["B","700","700 &times; 1.5","<b>1,050</b>"],
  ["C","800","800 &times; 1.5","<b>1,200</b>"],
  {"cls":"tot","cells":["<b>Total</b>","<b>3,000</b>","","<b>4,500</b>"]}],
 headcls="lite")}
<p class="small"><b>Cross-check:</b> 2,250 + 1,050 + 1,200 = 4,500 &nbsp;&#10003;&nbsp; equals the
indirect cost given. If this does not tally, stop and re-divide.</p>"""

    pa = acct("Process A Account",
      [("To Direct materials", 1000, "", 2000),
       ("To Direct wages", "", "", 1500),
       ("To Direct expenses", "", "", 300),
       ("To Indirect production cost" + src("W1: 1,500 &times; 1.5"), "", "", 2250),
       ("TOT", 1000, "", 6050)],
      [("By Transfer to Process B" + src("6,050 &divide; 1,000 units = " + R + "6.05 per unit"),
        1000, 6.05, 6050),
       None, None, None,
       ("TOT", 1000, "", 6050)])

    pb = acct("Process B Account",
      [("To Transfer from Process A" + src("&#8592; total of Process A a/c"), 1000, 6.05, 6050),
       ("To Direct materials", "", "", 1000),
       ("To Direct wages", "", "", 700),
       ("To Direct expenses", "", "", 100),
       ("To Indirect production cost" + src("W1: 700 &times; 1.5"), "", "", 1050),
       ("TOT", 1000, "", 8900)],
      [("By Transfer to Process C" + src("8,900 &divide; 1,000 units = " + R + "8.90 per unit"),
        1000, 8.90, 8900),
       None, None, None, None,
       ("TOT", 1000, "", 8900)])

    pc = acct("Process C Account",
      [("To Transfer from Process B" + src("&#8592; total of Process B a/c"), 1000, 8.90, 8900),
       ("To Direct materials", "", "", "&mdash;"),
       ("To Direct wages", "", "", 800),
       ("To Direct expenses", "", "", "&mdash;"),
       ("To Indirect production cost" + src("W1: 800 &times; 1.5"), "", "", 1200),
       ("TOT", 1000, "", 10900)],
      [("By Transfer to Finished Stock" + src("10,900 &divide; 1,000 = " + R + "10.90 per unit"),
        1000, 10.90, 10900),
       None, None, None, None,
       ("TOT", 1000, "", 10900)])

    flow = arrow_panel(500, 118, [
        {"box": (8, 26, 96, 40, "PROCESS A|6,050|" + "6.05/unit", "#eaf5f4"), "fs": 8.0},
        {"box": (146, 26, 96, 40, "PROCESS B|8,900|8.90/unit", "#eaf5f4"), "fs": 8.0},
        {"box": (284, 26, 96, 40, "PROCESS C|10,900|10.90/unit", "#eaf5f4"), "fs": 8.0},
        {"box": (416, 26, 78, 40, "FINISHED|STOCK|10,900", "#f4f8fb"), "fs": 8.0},
        {"arc": (104, 40, 144, 40, "carries 6,050", -16)},
        {"arc": (242, 40, 282, 40, "carries 8,900", -16)},
        {"arc": (380, 40, 414, 40, "10,900", -16)},
        {"txt": (250, 100, "Each box adds only its OWN cost; the arrow carries the whole "
                 "running total forward.", 7.6, "#666", "middle")},
    ], "The chain. Notice the cost per unit can only go up as you move right.")

    tp = f"""{bullets([
 'Students write Process B&rsquo;s cost per unit as 2,850 &divide; 1,000 = '
 f'<span class="rs">{R}</span>2.85, using only B&rsquo;s own costs. Wrong. '
 'The unit leaving B has A&rsquo;s cost inside it too. <b>The transfer-in is a debit like any '
 'other</b>.',
 'Forgetting to show <b>units</b> in the account. Marks are given for the units column, and '
 'it is free &mdash; every figure is 1,000.',
 'Apportioning the overhead on the wrong basis (materials, or equally between three '
 'processes). The question said direct wage cost. Read it, underline it, use it.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q1", "Three processes, overhead on wages", "Plain chain &middot; p.8")
            + question(q) + read(rd) + method(mt) + wn(wnh)
            + pa + pb + pc + flow + trap(tp)
            + ans([("Cost per unit &mdash; Process A", f"{R} 6.05"),
                   ("Cost per unit &mdash; Process B", f"{R} 8.90"),
                   ("Cost per unit &mdash; Process C (final)", f"{R} 10.90"),
                   ("Total cost of 1,000 units", f"{R} 10,900")],
                  "State the final cost per unit in words as your closing line: "
                  "&ldquo;The cost of production is "
                  f"<span class='rs'>{R}</span>10,900 for 1,000 units, i.e. "
                  f"<span class='rs'>{R}</span>10.90 per unit.&rdquo;")
            + "</div>")


# ======================================================================
# PROBLEM 2
# ======================================================================
def q2():
    q = f"""<p>The following details show the cost of the three processes of manufacturing.
The production of each process is passed on to the next till completion.</p>
{table(None, [("Particulars",""),("Process A","r"),("Process B","r"),("Process C","r")],
 [["Wages and materials","60,800","24,000","58,500"],
  ["Works overheads","11,200","10,500","12,000"],
  ["Production in units","72,000","75,000","96,000"],
  ["Opening stock (units from preceding process on 1st July)","&mdash;","8,000","33,000"],
  ["Closing stock (units from preceding process on 31st July)","&mdash;","2,000","11,000"]],
 headcls="lite")}"""

    rd = f"""<p>This problem looks like Q1 but it is not, and one phrase tells you so:
<b>&ldquo;units from preceding process&rdquo;</b>.</p>
{bullets([
 'The opening and closing stock in Process B is <b>not half-finished work</b>. It is a pile of '
 'finished A-units waiting to be worked on. So it is valued at <b>A&rsquo;s rate</b>, not '
 'B&rsquo;s. Same for C &mdash; its stock is B-units, valued at B&rsquo;s rate.',
 'Because there is stock lying on both sides, the units B actually <i>consumed</i> are not the '
 'units it <i>received</i>. You must work the consumption out.',
 '&ldquo;Production in units&rdquo; is the <b>output</b> of that process. Divide by this figure '
 'to get the rate &mdash; never by the units consumed.'])}"""

    mt = steps([
        "<b>Process A first</b> &mdash; it has no stock, so rate = total cost &divide; production.",
        "For B and C, find the units consumed: "
        "<b>Opening stock + Received from previous process &minus; Closing stock</b>.",
        "Value those consumed units at the <b>previous process's rate</b>. That is the "
        "transfer-in cost.",
        "Add the process's own wages, materials and works overheads.",
        "Rate for this process = that grand total &divide; <b>its own production in units</b>.",
        "Now write the account. Debit side: opening stock, transfer-in, own costs. "
        "Credit side: closing stock (at the <i>previous</i> rate) and transfer-out "
        "(at <i>this</i> rate). The two sides must balance to the rupee."])

    wnh = f"""<h4 class="mini">W1 &nbsp;Process A rate (no stock, so straight division)</h4>
{calc([f'Total cost &nbsp;=&nbsp; 60,800 + 11,200 &nbsp;=&nbsp; <b>{R}72,000</b>',
       f'Rate &nbsp;=&nbsp; 72,000 &divide; 72,000 units &nbsp;=&nbsp; <b>{R}1.00 per unit</b>'])}

<h4 class="mini">W2 &nbsp;Units consumed by Process B and Process C</h4>
{table(None, [("Particulars",""),("Process B","r"),("Process C","r")],
 [["Opening stock of previous-process units","8,000","33,000"],
  ["Add: Received from previous process","72,000","75,000"],
  {"cls":"sub","cells":["Units available","80,000","1,08,000"]},
  ["Less: Closing stock of previous-process units","(2,000)","(11,000)"],
  {"cls":"tot","cells":["<b>Units consumed in the process</b>","<b>78,000</b>","<b>97,000</b>"]}],
 headcls="lite")}
<p class="small">Received by B = A&rsquo;s production 72,000. Received by C = B&rsquo;s
production 75,000.</p>

<h4 class="mini">W3 &nbsp;Rate for Process B</h4>
{calc([f'Cost of units consumed &nbsp;=&nbsp; 78,000 &times; {R}1.00 &nbsp;=&nbsp; 78,000',
       f'Add own cost &nbsp;=&nbsp; 24,000 + 10,500 &nbsp;=&nbsp; 34,500',
       f'Total &nbsp;=&nbsp; <b>{R}1,12,500</b>',
       f'Rate &nbsp;=&nbsp; 1,12,500 &divide; 75,000 units produced &nbsp;=&nbsp; '
       f'<b>{R}1.50 per unit</b>'])}

<h4 class="mini">W4 &nbsp;Rate for Process C</h4>
{calc([f'Cost of units consumed &nbsp;=&nbsp; 97,000 &times; {R}1.50 &nbsp;=&nbsp; 1,45,500',
       f'Add own cost &nbsp;=&nbsp; 58,500 + 12,000 &nbsp;=&nbsp; 70,500',
       f'Total &nbsp;=&nbsp; <b>{R}2,16,000</b>',
       f'Rate &nbsp;=&nbsp; 2,16,000 &divide; 96,000 units produced &nbsp;=&nbsp; '
       f'<b>{R}2.25 per unit</b>'])}"""

    pa = acct("Process A Account",
      [("To Wages and materials", 72000, "", 60800),
       ("To Works overheads", "", "", 11200),
       ("TOT", 72000, "", 72000)],
      [("By Transfer to Process B" + src("W1: rate " + R + "1.00"), 72000, 1.00, 72000),
       None, ("TOT", 72000, "", 72000)])

    pb = acct("Process B Account",
      [("To Opening stock" + src("8,000 A-units @ " + R + "1.00 &#8592; A's rate"), 8000, 1.00, 8000),
       ("To Transfer from Process A", 72000, 1.00, 72000),
       ("To Wages and materials", "", "", 24000),
       ("To Works overheads", "", "", 10500),
       ("TOT", 80000, "", 114500)],
      [("By Closing stock" + src("2,000 A-units @ " + R + "1.00 &mdash; still A's rate"),
        2000, 1.00, 2000),
       ("By Transfer to Process C" + src("W3: 75,000 @ " + R + "1.50"), 75000, 1.50, 112500),
       ("<i>(3,000 units consumed but not yielded &mdash; process shrinkage, no scrap value given)</i>",
        3000, "", "&mdash;"),
       None,
       ("TOT", 80000, "", 114500)])

    pc = acct("Process C Account",
      [("To Opening stock" + src("33,000 B-units @ " + R + "1.50 &#8592; B's rate"),
        33000, 1.50, 49500),
       ("To Transfer from Process B", 75000, 1.50, 112500),
       ("To Wages and materials", "", "", 58500),
       ("To Works overheads", "", "", 12000),
       ("TOT", 108000, "", 232500)],
      [("By Closing stock" + src("11,000 B-units @ " + R + "1.50"), 11000, 1.50, 16500),
       ("By Transfer to Finished Stock" + src("W4: 96,000 @ " + R + "2.25"), 96000, 2.25, 216000),
       ("<i>(1,000 units shrinkage)</i>", 1000, "", "&mdash;"),
       None,
       ("TOT", 108000, "", 232500)])

    dia = arrow_panel(500, 150, [
        {"box": (10, 10, 130, 24, "OPENING STOCK 8,000|valued at A's rate 1.00", "#fdf6e6"), "fs": 7.6},
        {"box": (10, 44, 130, 24, "RECEIVED 72,000|at A's rate 1.00", "#fdf6e6"), "fs": 7.6},
        {"box": (178, 27, 116, 24, "AVAILABLE 80,000", "#e8eef4"), "fs": 8.0},
        {"box": (178, 66, 116, 24, "less CLOSING 2,000|(still A's rate)", "#fdeeec"), "fs": 7.6,
         "stroke": "#c0392b", "fg": "#98271b"},
        {"box": (332, 40, 158, 30, "CONSUMED 78,000 &times; 1.00|= 78,000 transferred-in cost",
          "#eaf5f4"), "fs": 7.8},
        {"arc": (140, 22, 176, 34, "", -10)},
        {"arc": (140, 56, 176, 42, "", 10)},
        {"line": (294, 39, 330, 50)},
        {"box": (332, 84, 158, 26, "+ own cost 34,500|= 1,12,500", "#eaf5f4"), "fs": 7.8},
        {"box": (332, 118, 158, 24, "&divide; 75,000 produced = 1.50", "#f4f8fb"), "fs": 8.0},
        {"txt": (411, 82, "", 8, "#000", "middle")},
        {"txt": (150, 130, "Stock stays at the OLD rate.", 7.8, "#c0392b", "middle")},
        {"txt": (150, 141, "Only output gets the NEW rate.", 7.8, "#c0392b", "middle")},
    ], "Why Process B's stock is valued at A's rate, not B's.")

    tp = f"""{bullets([
 'Valuing B&rsquo;s opening/closing stock at B&rsquo;s own rate of '
 f'<span class="rs">{R}</span>1.50. It has not been through B yet &mdash; it is worth '
 f'<span class="rs">{R}</span>1.00. This single error breaks both sides of the account.',
 'Dividing by units consumed (78,000) instead of units produced (75,000). The rate must '
 'describe a unit that came <i>out</i>.',
 'Panicking when the units do not balance. Here 78,000 are consumed but only 75,000 emerge. '
 'That gap is real shrinkage. No scrap value is given, so it carries no cost &mdash; simply show '
 'it and move on. Do not invent a normal-loss working the question never asked for.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q2", "Stock of previous-process units", "Chain + stock &middot; p.8")
            + question(q) + read(rd) + method(mt) + wn(wnh)
            + pa + pb + pc + dia + trap(tp)
            + ans([("Cost per unit &mdash; Process A", f"{R} 1.00"),
                   ("Cost per unit &mdash; Process B", f"{R} 1.50"),
                   ("Cost per unit &mdash; Process C (final)", f"{R} 2.25"),
                   ("Cost transferred to Finished Stock", f"{R} 2,16,000")],
                  "Both B and C accounts balance exactly &mdash; 1,14,500 and 2,32,500. "
                  "Always show the totals; a balancing account is self-proving.")
            + "</div>")


# ======================================================================
# PROBLEM 3
# ======================================================================
def q3():
    q = f"""<p>From the following information relating to an article which undergoes three
processes for manufacture, show the cost of each process and the cost per article.</p>
{table(None, [("Particulars",""),("Process A","r"),("Process B","r"),("Process C","r")],
 [["Materials consumed","37,500","12,500","50,000"],
  ["Labour","20,000","50,000","15,000"],
  ["Direct expenses","6,500","18,000","6,250"]], headcls="lite")}
<p>The indirect expenses amounted to <span class="rs">{R}</span>21,250 and the number of
articles produced during the month was 240 units.</p>"""

    rd = f"""{bullets([
 'Same shape as Q1 &mdash; one output figure (240 articles), so <b>no losses</b>.',
 '<b>The basis for splitting the indirect expenses is NOT stated.</b> This is deliberate. '
 'The accepted convention when no basis is given is to apportion on <b>direct labour</b>. '
 'Say so in one line in your answer &mdash; &ldquo;indirect expenses apportioned on the basis of '
 'direct labour in the absence of any other basis&rdquo; &mdash; and you protect the marks.',
 'Test whether your assumed basis is right by checking the split comes out in round figures. '
 'Here labour gives exactly 25%. That is the examiner confirming your choice.',
 'Two answers are wanted: <b>cost of each process</b> and <b>cost per article</b>. Give both, '
 'clearly labelled.'])}"""

    mt = steps([
        "Total the chosen basis &mdash; labour: 20,000 + 50,000 + 15,000.",
        "Rate = 21,250 &divide; that total. Express as a percentage if it is clean.",
        "Split, then cross-check the pieces add back to 21,250.",
        "Build the three process accounts in a chain, transferring the running total.",
        "Divide each process total by 240 to get cost per article at that stage.",
        "Final line: cost per article = Process C total &divide; 240."])

    wnh = f"""<h4 class="mini">W1 &nbsp;Apportionment of indirect expenses (basis: direct labour)</h4>
{calc([f'Total labour &nbsp;=&nbsp; 20,000 + 50,000 + 15,000 &nbsp;=&nbsp; <b>{R}85,000</b>',
       f'Rate &nbsp;=&nbsp; 21,250 &divide; 85,000 &nbsp;=&nbsp; 0.25 &nbsp;=&nbsp; '
       f'<b>25% of direct labour</b>'])}
{table(None, [("Process",""),("Labour","r"),("&times; 25%","r"),("Indirect expenses","r")],
 [["A","20,000","20,000 &times; 0.25","<b>5,000</b>"],
  ["B","50,000","50,000 &times; 0.25","<b>12,500</b>"],
  ["C","15,000","15,000 &times; 0.25","<b>3,750</b>"],
  {"cls":"tot","cells":["<b>Total</b>","<b>85,000</b>","","<b>21,250</b>"]}], headcls="lite")}
<p class="small"><b>Cross-check:</b> 5,000 + 12,500 + 3,750 = 21,250 &#10003; &mdash; and every
figure is a round number, which confirms labour was the intended basis.</p>"""

    stmt = table("Statement of Cost of Each Process and Cost per Article",
      [("Particulars",""),("Process A","r"),("Process B","r"),("Process C","r")],
      [["Cost of previous process (transferred in)","&mdash;","69,000","1,62,000"],
       ["Materials consumed","37,500","12,500","50,000"],
       ["Labour","20,000","50,000","15,000"],
       ["Direct expenses","6,500","18,000","6,250"],
       ["Indirect expenses &nbsp;<span class='src' style='display:inline'>(W1)</span>",
        "5,000","12,500","3,750"],
       {"cls":"tot","cells":["<b>Total cost of the process</b>","<b>69,000</b>",
                             "<b>1,62,000</b>","<b>2,37,000</b>"]},
       {"cls":"sub","cells":["Cost per article (&divide; 240)","287.50","675.00","<b>987.50</b>"]}])

    pa = acct("Process A Account",
      [("To Materials consumed", 240, "", 37500),
       ("To Labour", "", "", 20000),
       ("To Direct expenses", "", "", 6500),
       ("To Indirect expenses" + src("W1"), "", "", 5000),
       ("TOT", 240, "", 69000)],
      [("By Transfer to Process B" + src("69,000 &divide; 240 = " + R + "287.50"),
        240, 287.50, 69000),
       None, None, None, ("TOT", 240, "", 69000)])

    pb = acct("Process B Account",
      [("To Transfer from Process A", 240, 287.50, 69000),
       ("To Materials consumed", "", "", 12500),
       ("To Labour", "", "", 50000),
       ("To Direct expenses", "", "", 18000),
       ("To Indirect expenses" + src("W1"), "", "", 12500),
       ("TOT", 240, "", 162000)],
      [("By Transfer to Process C" + src("1,62,000 &divide; 240 = " + R + "675.00"),
        240, 675.00, 162000),
       None, None, None, None, ("TOT", 240, "", 162000)])

    pc = acct("Process C Account",
      [("To Transfer from Process B", 240, 675.00, 162000),
       ("To Materials consumed", "", "", 50000),
       ("To Labour", "", "", 15000),
       ("To Direct expenses", "", "", 6250),
       ("To Indirect expenses" + src("W1"), "", "", 3750),
       ("TOT", 240, "", 237000)],
      [("By Transfer to Finished Stock" + src("2,37,000 &divide; 240 = " + R + "987.50"),
        240, 987.50, 237000),
       None, None, None, None, ("TOT", 240, "", 237000)])

    return ("<div class='prob long'>"
            + prob_head("Q3", "Three processes, cost per article", "Plain chain &middot; p.8")
            + question(q) + read(rd) + method(mt) + wn(wnh) + stmt + pa + pb + pc
            + why("<p>The statement and the three accounts say exactly the same thing. "
                  "If the question says <i>&ldquo;show the cost of each process&rdquo;</i> the "
                  "statement alone is enough; if it says <i>&ldquo;prepare process accounts&rdquo;</i> "
                  "you must draw the accounts. When in doubt give the statement first &mdash; it is "
                  "faster to write and it makes the accounts almost automatic.</p>")
            + ans([("Cost of Process A", f"{R} 69,000"),
                   ("Cost of Process B", f"{R} 1,62,000"),
                   ("Cost of Process C", f"{R} 2,37,000"),
                   ("Cost per article", f"{R} 987.50")]))


# ======================================================================
# PROBLEM 4
# ======================================================================
def q4():
    q = f"""<p>A particular brand of chemical passed through three processes during the week
ended 15th January. 600 tins were produced. The following information is disclosed by each
process.</p>
{table(None, [("Particulars",""),("Process A","r"),("Process B","r"),("Process C","r")],
 [["Materials","4,000","2,000","1,500"],
  ["Labour expenses","3,000","2,500","2,300"],
  ["Direct expenses","6,000","200","500"],
  ["Cost of tins","&mdash;","&mdash;","2,030"],
  ["Packing charges","&mdash;","&mdash;","325"]], headcls="lite")}
<p>The indirect expenses were <span class="rs">{R}</span>1,600. The by-product is sold for
<span class="rs">{R}</span>240 (Process B). The residue was sold for
<span class="rs">{R}</span>125.50 (Process C).</p>
<p>Prepare the process A/c with cost of production of the product per tin.</p>"""

    rd = f"""{bullets([
 'Again 600 tins throughout &mdash; <b>no process loss</b>.',
 'Two new items: a <b>by-product sold for 240</b> and a <b>residue sold for 125.50</b>. '
 'Both are <b>deducted</b> from the cost of the process in which they arise. They are not '
 'income and they do not go to Profit &amp; Loss &mdash; they reduce the cost that the good '
 'output has to carry.',
 '&ldquo;Cost of tins&rdquo; and &ldquo;packing charges&rdquo; belong to Process C only. They are '
 'ordinary debits &mdash; do not treat them as anything special.',
 'The indirect expense basis is again not stated, so apportion on labour and say so.'])}"""

    mt = steps([
        "Apportion the indirect expenses on labour (state the assumption).",
        "Build Process A normally.",
        "In Process B, debit everything, then <b>credit the by-product sale of 240</b>. "
        "The amount that transfers to C is the total <i>after</i> that deduction.",
        "In Process C, debit everything including tins and packing, then "
        "<b>credit the residue sale of 125.50</b>.",
        "Cost of production = final balance of Process C. Divide by 600 tins."])

    wnh = f"""<h4 class="mini">W1 &nbsp;Apportionment of indirect expenses (basis: labour)</h4>
{calc([f'Total labour &nbsp;=&nbsp; 3,000 + 2,500 + 2,300 &nbsp;=&nbsp; <b>{R}7,800</b>',
       f'Rate &nbsp;=&nbsp; 1,600 &divide; 7,800 &nbsp;=&nbsp; <b>0.205128 per rupee of labour</b>'])}
{table(None, [("Process",""),("Labour","r"),("Working","r"),("Indirect expenses","r")],
 [["A","3,000","3,000 &times; 0.205128","<b>615.38</b>"],
  ["B","2,500","2,500 &times; 0.205128","<b>512.82</b>"],
  ["C","2,300","2,300 &times; 0.205128","<b>471.80</b>"],
  {"cls":"tot","cells":["<b>Total</b>","<b>7,800</b>","","<b>1,600.00</b>"]}], headcls="lite")}
<p class="small">The rate does not divide neatly here, so carry two decimals and force the last
figure to make the total exactly 1,600. Write &ldquo;difference of
<span class="rs">{R}</span>0.01 adjusted in Process C&rdquo; if you like &mdash; examiners accept
it and it shows you checked.</p>"""

    pa = acct("Process A Account",
      [("To Materials", 600, "", 4000),
       ("To Labour expenses", "", "", 3000),
       ("To Direct expenses", "", "", 6000),
       ("To Indirect expenses" + src("W1"), "", "", 615.38),
       ("TOT", 600, "", 13615.38)],
      [("By Transfer to Process B", 600, 22.69, 13615.38),
       None, None, None, ("TOT", 600, "", 13615.38)])

    pb = acct("Process B Account",
      [("To Transfer from Process A", 600, 22.69, 13615.38),
       ("To Materials", "", "", 2000),
       ("To Labour expenses", "", "", 2500),
       ("To Direct expenses", "", "", 200),
       ("To Indirect expenses" + src("W1"), "", "", 512.82),
       ("TOT", 600, "", 18828.20)],
      [("By Sale of by-product" + src("deducted from cost, NOT income"), "", "", 240.00),
       ("By Transfer to Process C" + src("18,828.20 &minus; 240 = 18,588.20"),
        600, 30.98, 18588.20),
       None, None, None,
       ("TOT", 600, "", 18828.20)])

    pc = acct("Process C Account",
      [("To Transfer from Process B", 600, 30.98, 18588.20),
       ("To Materials", "", "", 1500),
       ("To Labour expenses", "", "", 2300),
       ("To Direct expenses", "", "", 500),
       ("To Cost of tins", "", "", 2030),
       ("To Packing charges", "", "", 325),
       ("To Indirect expenses" + src("W1"), "", "", 471.80),
       ("TOT", 600, "", 25715.00)],
      [("By Sale of residue" + src("deducted from cost"), "", "", 125.50),
       ("By Cost of production transferred" + src("25,715.00 &minus; 125.50 = 25,589.50"),
        600, 42.65, 25589.50),
       None, None, None, None, None,
       ("TOT", 600, "", 25715.00)])

    tp = f"""{bullets([
 'Adding the by-product sale to the credit of Profit &amp; Loss instead of deducting it inside '
 'the process. In a <b>by-product of small value</b> the standard treatment is to credit the '
 'process. That is what &ldquo;(Process B)&rdquo; in the question is telling you.',
 'Deducting the residue from Process B or from the total instead of from Process C. '
 'The question names the process for each &mdash; use it.',
 'Rounding the per-tin figure too early. Carry the paise through and round only at the last '
 'line.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q4", "By-product and residue", "Chain + by-product &middot; p.8&ndash;9")
            + question(q) + read(rd) + method(mt) + wn(wnh) + pa + pb + pc + trap(tp)
            + ans([("Total cost of production", f"{R} 25,589.50"),
                   ("Number of tins", "600"),
                   ("Cost of production per tin", f"{R} 42.65")],
                  "Closing line: &ldquo;Cost of production is "
                  f"<span class='rs'>{R}</span>25,589.50 for 600 tins, i.e. "
                  f"<span class='rs'>{R}</span>42.65 per tin.&rdquo;"))


# ======================================================================
# PROBLEM 5
# ======================================================================
def q5():
    q = f"""<p>Prepare a Process Account and Abnormal Loss Account from the following
information.</p>
{table(None, [("Particulars",""),("","r")],
 [["Input of raw material","1,000 units @ " + R + "20 per unit"],
  ["Direct material", R + "4,200"],
  ["Direct wages", R + "6,000"],
  ["Production overheads", R + "6,000"],
  ["Actual output transferred to Process II","900 units"],
  ["Normal loss","5%"],
  ["Value of scrap per unit", R + "8"]], headcls="lite", widths=["58%","42%"])}"""

    rd = f"""<p>This is the first problem with a loss, and it is the template for Q5&ndash;Q9.
Four figures decide everything:</p>
{bullets([
 '<b>Input 1,000 units.</b> Normal loss is a percentage <i>of input</i> &mdash; so 5% of 1,000 = '
 '50 units. Not 5% of output.',
 '<b>Expected output = 1,000 &minus; 50 = 950 units.</b> Write this down. It is the figure you '
 'compare the actual against.',
 '<b>Actual output is 900,</b> which is <i>less</i> than expected 950. So 50 units have gone '
 'missing beyond what was allowed &mdash; that is <b>abnormal loss</b>. If actual had been more '
 'than 950 it would have been abnormal gain.',
 '<b>Scrap is worth 8 per unit.</b> Normal loss units are sold as scrap, so they do carry a '
 'value &mdash; and that value is removed from the cost before you divide.'])}"""

    mt = steps([
        "Total the debits &mdash; every cost that entered the process.",
        "Normal loss in <b>units</b> = given % &times; input units. "
        "Normal loss in <b>rupees</b> = those units &times; scrap rate.",
        "Expected output = Input &minus; Normal loss units.",
        "Compare actual output with expected output. Shortfall = abnormal loss; "
        "excess = abnormal gain.",
        "<b>Cost per good unit</b> = (Total cost &minus; Scrap value of normal loss) "
        "&divide; (Input units &minus; Normal loss units). Show this fraction in full.",
        "Value the transfer-out AND the abnormal loss at that <b>same</b> rate.",
        "Write the process account &mdash; it must balance. Then open the Abnormal Loss account: "
        "debit the process value, credit the scrap realised, and the balance goes to "
        "Profit &amp; Loss."])

    rate = 35800 / 950
    wnh = f"""<h4 class="mini">W1 &nbsp;Total cost debited to the process</h4>
{calc([f'Raw material &nbsp; 1,000 &times; {R}20 &nbsp;=&nbsp; 20,000',
       'Direct material &nbsp;=&nbsp; 4,200',
       'Direct wages &nbsp;=&nbsp; 6,000',
       'Production overheads &nbsp;=&nbsp; 6,000',
       f'<b>Total &nbsp;=&nbsp; {R}36,200</b>'])}

<h4 class="mini">W2 &nbsp;The units reconciliation</h4>
{calc([f'Normal loss &nbsp;=&nbsp; 5% of 1,000 &nbsp;=&nbsp; <b>50 units</b>, '
       f'scrap value 50 &times; {R}8 &nbsp;=&nbsp; <b>{R}400</b>',
       'Expected output &nbsp;=&nbsp; 1,000 &minus; 50 &nbsp;=&nbsp; <b>950 units</b>',
       'Actual output &nbsp;=&nbsp; 900 units',
       'Abnormal loss &nbsp;=&nbsp; 950 &minus; 900 &nbsp;=&nbsp; <b>50 units</b>'])}

<h4 class="mini">W3 &nbsp;Cost per good unit &mdash; the formula that matters most</h4>
{fml(f"<b>{R}36,200 &minus; {R}400</b> &nbsp;&divide;&nbsp; <b>1,000 &minus; 50</b> "
     f"&nbsp;=&nbsp; {R}35,800 &divide; 950 &nbsp;=&nbsp; <b>{R}37.6842 per unit</b>",
     "Normal loss is taken out of the top (its scrap value) and out of the bottom (its units). "
     "That is how the cost of the normal loss gets loaded onto the good units.")}
{calc([f'Transferred out &nbsp; 900 &times; 37.6842 &nbsp;=&nbsp; <b>{R}33,915.79</b>',
       f'Abnormal loss &nbsp; 50 &times; 37.6842 &nbsp;=&nbsp; <b>{R}1,884.21</b>'])}"""

    dia = arrow_panel(500, 165, [
        {"box": (168, 6, 164, 26, "INPUT 1,000 units|Total cost 36,200", "#e8eef4"), "fs": 8.0},
        {"line": (250, 32, 250, 46)},
        {"box": (10, 46, 140, 34, "NORMAL LOSS 50 u|scrap 50 &times; 8 = 400", "#fdf6e6"), "fs": 7.8},
        {"box": (176, 46, 148, 34, "EXPECTED OUTPUT|950 units", "#eaf5f4"), "fs": 7.8},
        {"arc": (168, 30, 100, 44, "5% of input", 14)},
        {"arc": (300, 32, 260, 44, "", 8)},
        {"box": (176, 96, 148, 30, "ACTUAL OUTPUT|900 units", "#eaf5f4"), "fs": 7.8},
        {"box": (352, 96, 140, 30, "ABNORMAL LOSS|50 units", "#fdeeec"), "fs": 7.8,
         "stroke": "#c0392b", "fg": "#98271b"},
        {"line": (250, 80, 250, 94)},
        {"arc": (324, 105, 350, 105, "the shortfall", -12)},
        {"box": (10, 134, 482, 26,
          "Cost per unit = (36,200 &minus; 400) &divide; (1,000 &minus; 50) = 37.6842  "
          "&#8594;  applied to BOTH the 900 good units and the 50 abnormal-loss units",
          "#f4f8fb"), "fs": 8.0},
    ], "Normal loss is expected and free. Abnormal loss is the shortfall against expectation.")

    pa = acct("Process I Account",
      [("To Raw material", 1000, 20.00, 20000),
       ("To Direct material", "", "", 4200),
       ("To Direct wages", "", "", 6000),
       ("To Production overheads", "", "", 6000),
       ("TOT", 1000, "", 36200)],
      [("By Normal loss" + src("50 units &times; " + R + "8 scrap"), 50, 8.00, 400),
       ("By Abnormal loss" + src("W3: 50 &times; 37.6842"), 50, 37.6842, 1884.21),
       ("By Transfer to Process II" + src("W3: 900 &times; 37.6842"), 900, 37.6842, 33915.79),
       None,
       ("TOT", 1000, "", 36200)])

    al = acct("Abnormal Loss Account",
      [("To Process I A/c" + src("&#8592; from the process account"), 50, 37.6842, 1884.21),
       ("TOT", 50, "", 1884.21)],
      [("By Sale of scrap" + src("50 units &times; " + R + "8 &mdash; abnormal loss units are "
                                 "also sold as scrap"), 50, 8.00, 400.00),
       ("By Profit &amp; Loss A/c" + src("balance &mdash; the real loss to the business"),
        "", "", 1484.21),
       ("TOT", 50, "", 1884.21)])

    nl = acct("Normal Loss Account",
      [("To Process I A/c", 50, 8.00, 400),
       ("TOT", 50, "", 400)],
      [("By Cost Ledger Control A/c (cash from scrap)", 50, 8.00, 400),
       ("TOT", 50, "", 400)])

    tp = f"""{bullets([
 f'Dividing by 1,000 instead of 950. You would get {R}35.80 and every later figure would be '
 'wrong. <b>The denominator is always input minus normal loss units.</b>',
 'Forgetting to deduct the 400 scrap value from the numerator.',
 'Valuing the abnormal loss at the scrap rate of 8. No &mdash; abnormal loss is valued at the '
 '<b>good-unit rate</b>. It only realises 8 when sold, and the difference is the loss you take '
 'to Profit &amp; Loss.',
 'Taking the whole 1,884.21 to Profit &amp; Loss. Only the <b>net</b> figure of 1,484.21 goes '
 'there, after crediting the 400 the scrap actually fetched.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q5", "Normal loss and abnormal loss", "Loss &amp; gain &middot; p.9")
            + question(q) + read(rd) + method(mt) + wn(wnh) + dia
            + pa + al + nl + trap(tp)
            + ans([("Cost per good unit", f"{R} 37.6842"),
                   ("Transferred to Process II (900 units)", f"{R} 33,915.79"),
                   ("Abnormal loss (50 units, at cost)", f"{R} 1,884.21"),
                   ("Scrap realised on abnormal loss", f"{R} 400.00"),
                   ("Net abnormal loss charged to Profit &amp; Loss", f"{R} 1,484.21")],
                  "Note how the Process account, the Abnormal Loss account and the Normal Loss "
                  "account all close cleanly. Show all three unless the question asks for fewer.")
            + "</div>")


# ======================================================================



# ======================================================================
# PROBLEM 6
# ======================================================================
def q6():
    q = f"""<p>The product of a company passes through 3 distinct processes. The following
information is obtained from the accounts for the month ending January 31, 2024.</p>
{table(None, [("Particulars",""),("Process A","r"),("Process B","r"),("Process C","r")],
 [["Direct material","7,800","5,940","8,886"],
  ["Direct wages","6,000","9,000","12,000"],
  ["Production overheads","6,000","9,000","12,000"]], headcls="lite")}
<p>3,000 units @ <span class="rs">{R}</span>3 each were introduced to Process I. There was no
stock of materials or work in progress. The output of each process passes directly to the next
process and finally to Finished Stock A/c. The following additional data is obtained:</p>
{table(None, [("Process",""),("Output","r"),("Normal loss %","r"),("Realisable value of scrap","r")],
 [["Process 1","2,850","5%","2"],["Process 2","2,520","10%","4"],
  ["Process 3","2,250","15%","5"]], headcls="lite")}
<p>Prepare Process Cost Account, Normal Loss Account and Abnormal Gain or Loss Account.</p>"""

    rd = f"""<p>This is <b>the</b> model problem of the module. It contains all three
possibilities in one question, which is exactly why examiners like it.</p>
{bullets([
 '<b>Process 1 ends with no abnormal item at all</b> &mdash; actual output equals expected. '
 'Do not force an abnormal figure just because the other processes have one.',
 '<b>Process 2 has an abnormal loss</b> (output less than expected).',
 '<b>Process 3 has an abnormal gain</b> (output MORE than expected). An abnormal gain is '
 'entered on the <b>debit</b> side of the process account &mdash; the opposite side from a loss. '
 'This single fact is the most commonly dropped mark in the whole module.',
 'Normal loss % is always applied to <b>the units entering that process</b>, which is the '
 'previous process&rsquo;s output &mdash; not the original 3,000.'])}"""

    mt = steps([
        "Work the processes strictly in order. Each one needs the previous one's output "
        "<i>and</i> its rate.",
        "For each process: total the debits, compute normal loss units and scrap value, "
        "find expected output, compare with actual.",
        "Rate = (Total cost &minus; normal loss scrap) &divide; (Input units &minus; normal loss units).",
        "<b>Loss</b> &rarr; credit the process with the shortfall at that rate. "
        "<b>Gain</b> &rarr; <u>debit</u> the process with the excess at that rate.",
        "Open one Normal Loss A/c for all three processes together. Debit each process's scrap "
        "value into it.",
        "If there is an abnormal gain, the normal loss did not fully happen &mdash; so "
        "<b>credit Normal Loss A/c and debit Abnormal Gain A/c</b> with the gain units "
        "&times; that process's scrap rate.",
        "Close Abnormal Loss and Abnormal Gain to Profit &amp; Loss."])

    wnh = f"""<h4 class="mini">W1 &nbsp;Process 1</h4>
{calc([f'Total cost &nbsp;=&nbsp; (3,000 &times; {R}3 = 9,000) + 7,800 + 6,000 + 6,000 &nbsp;=&nbsp; <b>{R}28,800</b>',
       f'Normal loss &nbsp;=&nbsp; 5% of 3,000 &nbsp;=&nbsp; <b>150 units</b>; scrap 150 &times; {R}2 &nbsp;=&nbsp; <b>{R}300</b>',
       'Expected output &nbsp;=&nbsp; 3,000 &minus; 150 &nbsp;=&nbsp; 2,850 units. Actual = 2,850 units.',
       '<b>Difference = NIL &mdash; no abnormal loss or gain in Process 1.</b>'])}
{fml("Rate &nbsp;=&nbsp; " + frac(f"28,800 &minus; 300", "3,000 &minus; 150")
     + f" &nbsp;=&nbsp; " + frac("28,500", "2,850") + f" &nbsp;=&nbsp; <b>{R}10.00 per unit</b>")}

<h4 class="mini">W2 &nbsp;Process 2</h4>
{calc([f'Total cost &nbsp;=&nbsp; (2,850 &times; {R}10 = 28,500) + 5,940 + 9,000 + 9,000 &nbsp;=&nbsp; <b>{R}52,440</b>',
       f'Normal loss &nbsp;=&nbsp; 10% of <b>2,850</b> &nbsp;=&nbsp; <b>285 units</b>; scrap 285 &times; {R}4 &nbsp;=&nbsp; <b>{R}1,140</b>',
       'Expected output &nbsp;=&nbsp; 2,850 &minus; 285 &nbsp;=&nbsp; 2,565 units. Actual = 2,520 units.',
       '<b>Abnormal LOSS = 2,565 &minus; 2,520 = 45 units</b>'])}
{fml("Rate &nbsp;=&nbsp; " + frac("52,440 &minus; 1,140", "2,850 &minus; 285")
     + " &nbsp;=&nbsp; " + frac("51,300", "2,565") + f" &nbsp;=&nbsp; <b>{R}20.00 per unit</b>")}
{calc([f'Abnormal loss &nbsp; 45 &times; 20 &nbsp;=&nbsp; <b>{R}900</b>',
       f'Transfer to Process 3 &nbsp; 2,520 &times; 20 &nbsp;=&nbsp; <b>{R}50,400</b>'])}

<h4 class="mini">W3 &nbsp;Process 3</h4>
{calc([f'Total cost &nbsp;=&nbsp; (2,520 &times; {R}20 = 50,400) + 8,886 + 12,000 + 12,000 &nbsp;=&nbsp; <b>{R}83,286</b>',
       f'Normal loss &nbsp;=&nbsp; 15% of <b>2,520</b> &nbsp;=&nbsp; <b>378 units</b>; scrap 378 &times; {R}5 &nbsp;=&nbsp; <b>{R}1,890</b>',
       'Expected output &nbsp;=&nbsp; 2,520 &minus; 378 &nbsp;=&nbsp; 2,142 units. Actual = 2,250 units.',
       '<b>Abnormal GAIN = 2,250 &minus; 2,142 = 108 units</b> &nbsp;(actual is MORE than expected)'])}
{fml("Rate &nbsp;=&nbsp; " + frac("83,286 &minus; 1,890", "2,520 &minus; 378")
     + " &nbsp;=&nbsp; " + frac("81,396", "2,142") + f" &nbsp;=&nbsp; <b>{R}38.00 per unit</b>",
     "Note the rate is still built on EXPECTED output (2,142), not on the actual 2,250. "
     "The gain is then valued at this rate and added back.")}
{calc([f'Abnormal gain &nbsp; 108 &times; 38 &nbsp;=&nbsp; <b>{R}4,104</b> &nbsp;(debit side)',
       f'Transfer to Finished Stock &nbsp; 2,250 &times; 38 &nbsp;=&nbsp; <b>{R}85,500</b>'])}"""

    dia = arrow_panel(500, 176, [
        {"box": (14, 4, 190, 22, "3,000 units introduced at " + R + "3", "#e8eef4"), "fs": 8.0},
        # process 1
        {"box": (14, 36, 138, 34, "PROCESS 1|expected 2,850 = actual 2,850", "#eaf5f4"), "fs": 7.6},
        {"box": (14, 78, 138, 20, "NO abnormal item", "#eef7ee"), "fs": 7.6, "stroke": "#2c7a34",
         "fg": "#1f5b26"},
        # process 2
        {"box": (176, 36, 138, 34, "PROCESS 2|expected 2,565 vs actual 2,520", "#eaf5f4"), "fs": 7.6},
        {"box": (176, 78, 138, 20, "ABNORMAL LOSS 45 u &#8594; CREDIT", "#fdeeec"), "fs": 7.4,
         "stroke": "#c0392b", "fg": "#98271b"},
        # process 3
        {"box": (338, 36, 148, 34, "PROCESS 3|expected 2,142 vs actual 2,250", "#eaf5f4"), "fs": 7.6},
        {"box": (338, 78, 148, 20, "ABNORMAL GAIN 108 u &#8594; DEBIT", "#eef7ee"), "fs": 7.4,
         "stroke": "#2c7a34", "fg": "#1f5b26"},
        {"line": (152, 53, 174, 53)},
        {"line": (314, 53, 336, 53)},
        {"line": (83, 26, 83, 34)},
        {"box": (14, 116, 472, 24,
          "Rate 1 = " + R + "10.00 &nbsp;&#8594;&nbsp; Rate 2 = " + R + "20.00 &nbsp;&#8594;&nbsp; "
          "Rate 3 = " + R + "38.00", "#f4f8fb"), "fs": 8.6},
        {"box": (14, 148, 472, 24,
          "LOSS goes on the CREDIT side (units leaving).  GAIN goes on the DEBIT side "
          "(units arriving).", "#fdf6e6"), "fs": 8.0, "stroke": "#c8901a", "fg": "#96690b"},
    ], "One question, all three outcomes. Learn this picture and Q5 to Q9 all become the same problem.")

    p1 = acct("Process 1 Account",
      [("To Units introduced", 3000, 3.00, 9000),
       ("To Direct material", "", "", 7800),
       ("To Direct wages", "", "", 6000),
       ("To Production overheads", "", "", 6000),
       ("TOT", 3000, "", 28800)],
      [("By Normal loss" + src("150 u &times; " + R + "2"), 150, 2.00, 300),
       ("By Transfer to Process 2" + src("W1: 2,850 &times; " + R + "10"), 2850, 10.00, 28500),
       None, None,
       ("TOT", 3000, "", 28800)])

    p2 = acct("Process 2 Account",
      [("To Transfer from Process 1", 2850, 10.00, 28500),
       ("To Direct material", "", "", 5940),
       ("To Direct wages", "", "", 9000),
       ("To Production overheads", "", "", 9000),
       ("TOT", 2850, "", 52440)],
      [("By Normal loss" + src("285 u &times; " + R + "4"), 285, 4.00, 1140),
       ("By Abnormal loss" + src("W2: 45 &times; " + R + "20"), 45, 20.00, 900),
       ("By Transfer to Process 3" + src("W2: 2,520 &times; " + R + "20"), 2520, 20.00, 50400),
       None,
       ("TOT", 2850, "", 52440)])

    p3 = acct("Process 3 Account",
      [("To Transfer from Process 2", 2520, 20.00, 50400),
       ("To Direct material", "", "", 8886),
       ("To Direct wages", "", "", 12000),
       ("To Production overheads", "", "", 12000),
       ("To Abnormal gain" + src("W3: 108 &times; " + R + "38 &mdash; DEBIT side"),
        108, 38.00, 4104),
       ("TOT", 2628, "", 87390)],
      [("By Normal loss" + src("378 u &times; " + R + "5"), 378, 5.00, 1890),
       ("By Transfer to Finished Stock" + src("W3: 2,250 &times; " + R + "38"), 2250, 38.00, 85500),
       None, None, None,
       ("TOT", 2628, "", 87390)])

    nl = acct("Normal Loss Account",
      [("To Process 1 A/c", 150, 2.00, 300),
       ("To Process 2 A/c", 285, 4.00, 1140),
       ("To Process 3 A/c", 378, 5.00, 1890),
       ("TOT", 813, "", 3330)],
      [("By Abnormal Gain A/c" + src("108 u &times; " + R + "5 &mdash; the Process 3 normal loss "
                                     "that never happened"), 108, 5.00, 540),
       ("By Cost Ledger Control A/c (scrap actually sold)", 705, "", 2790),
       None,
       ("TOT", 813, "", 3330)])

    ala = acct("Abnormal Loss Account",
      [("To Process 2 A/c", 45, 20.00, 900),
       ("TOT", 45, "", 900)],
      [("By Cost Ledger Control A/c" + src("45 u &times; " + R + "4 scrap"), 45, 4.00, 180),
       ("By Profit &amp; Loss A/c" + src("balance = the real loss"), "", "", 720),
       ("TOT", 45, "", 900)])

    aga = acct("Abnormal Gain Account",
      [("To Normal Loss A/c" + src("108 u &times; " + R + "5 &mdash; scrap income forgone"),
        108, 5.00, 540),
       ("To Profit &amp; Loss A/c" + src("balance = the real gain"), "", "", 3564),
       ("TOT", 108, "", 4104)],
      [("By Process 3 A/c", 108, 38.00, 4104),
       None,
       ("TOT", 108, "", 4104)])

    tp = f"""{bullets([
 '<b>Putting the abnormal gain on the credit side.</b> Think about it physically: extra units '
 'have <i>arrived</i> in the process, so they must be debited like any other input. '
 'If your Process 3 account will not balance, this is why.',
 'Applying the 15% normal loss to 3,000 instead of 2,520. Each percentage applies to that '
 'process&rsquo;s own input.',
 'Forgetting the entry <b>Abnormal Gain A/c &#8594; Normal Loss A/c 540</b>. Because 108 units '
 'did not perish, the company also did not earn scrap on them &mdash; so the gain must be reduced '
 f'by 108 &times; {R}5. Without this the Normal Loss account will not close.',
 'Using the actual output 2,250 as the denominator for the rate. The denominator is always '
 '<b>input minus normal loss</b> = 2,142.'])}"""

    return ("<div class='prob long'>"
            + prob_head("Q6", "Loss, gain and neither &mdash; all in one",
                        "Loss &amp; gain &middot; p.9")
            + question(q) + read(rd) + method(mt) + wn(wnh) + dia
            + p1 + p2 + p3 + nl + ala + aga + trap(tp)
            + ans([("Cost per unit &mdash; Process 1", f"{R} 10.00"),
                   ("Cost per unit &mdash; Process 2", f"{R} 20.00"),
                   ("Cost per unit &mdash; Process 3", f"{R} 38.00"),
                   ("Abnormal loss (Process 2, 45 units)", f"{R} 900"),
                   ("Abnormal gain (Process 3, 108 units)", f"{R} 4,104"),
                   ("Transferred to Finished Stock (2,250 units)", f"{R} 85,500"),
                   ("Net loss to P&amp;L on abnormal loss", f"{R} 720"),
                   ("Net gain to P&amp;L on abnormal gain", f"{R} 3,564")],
                  "Every one of the six accounts closes exactly. If yours do not, check the "
                  "abnormal gain is on the debit side and that the 540 entry is present.")
            + "</div>")


# ======================================================================
# PROBLEM 7
# ======================================================================
def q7():
    q = f"""<p>Product A is obtained after it passes through three distinct processes.
2,000 kgs of material at <span class="rs">{R}</span>5 per kg were issued to Process 1, direct
wages amounted to <span class="rs">{R}</span>900 and other production overheads incurred was
<span class="rs">{R}</span>500. Normal loss is estimated at 10% of input. The wastage is sold at
<span class="rs">{R}</span>3 per kg. The actual output is 1,850 kgs. Prepare Process 1 A/c,
Normal Loss A/c and Abnormal Gain A/c.</p>"""

    rd = f"""{bullets([
 'Only <b>Process 1</b> is asked for. The question mentions three processes to set the scene &mdash; '
 'ignore the other two. Answer exactly what is asked.',
 'Expected output = 2,000 &minus; 200 = 1,800 kg. Actual is <b>1,850 kg &mdash; higher</b>. '
 'The question even names the account it wants: <b>Abnormal Gain A/c</b>. That is your '
 'confirmation before you calculate anything.',
 'Because there is a gain, remember the two-part consequence: debit the process with the gain '
 'at cost, and transfer the forgone scrap value to Normal Loss A/c.'])}"""

    mt = steps([
        "Total the debits.",
        "Normal loss = 10% of 2,000 = 200 kg; scrap value = 200 &times; 3.",
        "Expected output 1,800 kg vs actual 1,850 kg &rarr; abnormal gain 50 kg.",
        "Rate = (11,400 &minus; 600) &divide; (2,000 &minus; 200).",
        "Debit the process with 50 kg at that rate; credit the transfer of 1,850 kg at that rate.",
        "Normal Loss A/c: debit 200 kg at scrap rate; credit 50 kg to Abnormal Gain A/c; "
        "the rest is scrap sold.",
        "Abnormal Gain A/c: debit the forgone scrap and the balance to P&amp;L; credit the "
        "process figure."])

    wnh = f"""<h4 class="mini">W1 &nbsp;Cost and units</h4>
{calc([f'Material &nbsp; 2,000 &times; {R}5 &nbsp;=&nbsp; 10,000',
       'Direct wages &nbsp;=&nbsp; 900 &nbsp;&nbsp;|&nbsp;&nbsp; Production overheads &nbsp;=&nbsp; 500',
       f'<b>Total cost &nbsp;=&nbsp; {R}11,400</b>',
       f'Normal loss &nbsp;=&nbsp; 10% of 2,000 &nbsp;=&nbsp; <b>200 kg</b>; scrap 200 &times; {R}3 &nbsp;=&nbsp; <b>{R}600</b>',
       'Expected output &nbsp;=&nbsp; 1,800 kg &nbsp;&nbsp;|&nbsp;&nbsp; Actual output &nbsp;=&nbsp; 1,850 kg',
       '<b>Abnormal gain &nbsp;=&nbsp; 1,850 &minus; 1,800 &nbsp;=&nbsp; 50 kg</b>'])}
{fml("Rate &nbsp;=&nbsp; " + frac("11,400 &minus; 600", "2,000 &minus; 200")
     + " &nbsp;=&nbsp; " + frac("10,800", "1,800") + f" &nbsp;=&nbsp; <b>{R}6.00 per kg</b>")}
{calc([f'Abnormal gain &nbsp; 50 &times; 6 &nbsp;=&nbsp; <b>{R}300</b>',
       f'Transfer out &nbsp; 1,850 &times; 6 &nbsp;=&nbsp; <b>{R}11,100</b>'])}"""

    p1 = acct("Process 1 Account",
      [("To Material", 2000, 5.00, 10000),
       ("To Direct wages", "", "", 900),
       ("To Production overheads", "", "", 500),
       ("To Abnormal gain" + src("W1: 50 kg &times; " + R + "6"), 50, 6.00, 300),
       ("TOT", 2050, "", 11700)],
      [("By Normal loss" + src("200 kg &times; " + R + "3"), 200, 3.00, 600),
       ("By Transfer to Process 2" + src("W1: 1,850 &times; " + R + "6"), 1850, 6.00, 11100),
       None, None,
       ("TOT", 2050, "", 11700)])

    nl = acct("Normal Loss Account",
      [("To Process 1 A/c", 200, 3.00, 600),
       ("TOT", 200, "", 600)],
      [("By Abnormal Gain A/c" + src("50 kg &times; " + R + "3 &mdash; loss that did not occur"),
        50, 3.00, 150),
       ("By Cost Ledger Control A/c (scrap sold)", 150, 3.00, 450),
       ("TOT", 200, "", 600)])

    ag = acct("Abnormal Gain Account",
      [("To Normal Loss A/c" + src("scrap income forgone on 50 kg"), 50, 3.00, 150),
       ("To Profit &amp; Loss A/c" + src("balance = net gain"), "", "", 150),
       ("TOT", 50, "", 300)],
      [("By Process 1 A/c", 50, 6.00, 300),
       None,
       ("TOT", 50, "", 300)])

    return ("<div class='prob long'>"
            + prob_head("Q7", "Abnormal gain only", "Loss &amp; gain &middot; p.10")
            + question(q) + read(rd) + method(mt) + wn(wnh) + p1 + nl + ag
            + why(f"<p>The net gain reaching Profit &amp; Loss is only "
                  f"<span class='rs'>{R}</span>150, not "
                  f"<span class='rs'>{R}</span>300. The process saved "
                  f"<span class='rs'>{R}</span>300 of cost by producing 50 extra kg, but it also "
                  f"lost the <span class='rs'>{R}</span>150 of scrap money those 50 kg would have "
                  f"fetched. Gain is always <b>cost saved minus scrap forgone</b>.</p>")
            + ans([("Cost per kg", f"{R} 6.00"),
                   ("Transferred out (1,850 kg)", f"{R} 11,100"),
                   ("Abnormal gain at cost (50 kg)", f"{R} 300"),
                   ("Scrap value forgone", f"{R} 150"),
                   ("Net abnormal gain to Profit &amp; Loss", f"{R} 150")])
            + "</div>")


# ======================================================================
# PROBLEM 8
# ======================================================================
def q8():
    q = f"""<p>A product passes through 2 distinct processes A and B. The normal wastage of each
process is as follows: Process A &ndash; 3% of products entering the process;
Process B &ndash; 5% of products entering the process.</p>
<p>The wastage of Process A was sold at 50 paise per unit and that of Process B at
<span class="rs">{R}</span>1 per unit. 10,000 units were issued to Process A at
<span class="rs">{R}</span>2 per unit. The other expenses were as follows:</p>
{table(None, [("Particulars",""),("Process A","r"),("Process B","r")],
 [["Materials","2,000","3,000"],["Wages","10,000","16,000"],
  ["Overheads","2,100","2,375"],["Actual output (units)","9,500","9,100"]], headcls="lite")}
<p>Prepare process accounts and other ledger accounts.</p>"""

    rd = f"""{bullets([
 '&ldquo;<b>3% of products entering the process</b>&rdquo; &mdash; so Process B&rsquo;s 5% is on the '
 '9,500 units it receives, not on the original 10,000.',
 'Process A: expected 9,700, actual 9,500 &rarr; <b>abnormal loss 200 units</b>.',
 'Process B: expected 9,025, actual 9,100 &rarr; <b>abnormal gain 75 units</b>.',
 'Two different scrap rates &mdash; 50 paise in A and ' + R + '1 in B. Keep them apart; using one '
 'rate for both is a common slip.',
 '&ldquo;and other ledger accounts&rdquo; means: Normal Loss A/c, Abnormal Loss A/c and '
 'Abnormal Gain A/c. Draw all three.'])}"""

    mt = steps([
        "Process A: total debits, normal loss 3% of 10,000, expected output, compare, rate, "
        "then value the loss and the transfer.",
        "Carry A's output <i>and</i> A's rate into Process B as the transfer-in.",
        "Process B: normal loss 5% of the units received (9,500), then the same sequence.",
        "Build the three ledger accounts, remembering the Abnormal Gain &rarr; Normal Loss entry."])

    wnh = f"""<h4 class="mini">W1 &nbsp;Process A</h4>
{calc([f'Total cost &nbsp;=&nbsp; (10,000 &times; {R}2 = 20,000) + 2,000 + 10,000 + 2,100 &nbsp;=&nbsp; <b>{R}34,100</b>',
       f'Normal loss &nbsp;=&nbsp; 3% of 10,000 &nbsp;=&nbsp; <b>300 units</b>; scrap 300 &times; {R}0.50 &nbsp;=&nbsp; <b>{R}150</b>',
       'Expected output 9,700 &nbsp;|&nbsp; Actual 9,500 &nbsp;&rarr;&nbsp; <b>abnormal loss 200 units</b>'])}
{fml("Rate &nbsp;=&nbsp; " + frac("34,100 &minus; 150", "10,000 &minus; 300")
     + " &nbsp;=&nbsp; " + frac("33,950", "9,700") + f" &nbsp;=&nbsp; <b>{R}3.50 per unit</b>")}
{calc([f'Abnormal loss &nbsp; 200 &times; 3.50 &nbsp;=&nbsp; <b>{R}700</b>',
       f'Transfer to B &nbsp; 9,500 &times; 3.50 &nbsp;=&nbsp; <b>{R}33,250</b>'])}

<h4 class="mini">W2 &nbsp;Process B</h4>
{calc([f'Total cost &nbsp;=&nbsp; 33,250 + 3,000 + 16,000 + 2,375 &nbsp;=&nbsp; <b>{R}54,625</b>',
       f'Normal loss &nbsp;=&nbsp; 5% of <b>9,500</b> &nbsp;=&nbsp; <b>475 units</b>; scrap 475 &times; {R}1 &nbsp;=&nbsp; <b>{R}475</b>',
       'Expected output 9,025 &nbsp;|&nbsp; Actual 9,100 &nbsp;&rarr;&nbsp; <b>abnormal gain 75 units</b>'])}
{fml("Rate &nbsp;=&nbsp; " + frac("54,625 &minus; 475", "9,500 &minus; 475")
     + " &nbsp;=&nbsp; " + frac("54,150", "9,025") + f" &nbsp;=&nbsp; <b>{R}6.00 per unit</b>")}
{calc([f'Abnormal gain &nbsp; 75 &times; 6 &nbsp;=&nbsp; <b>{R}450</b> (debit side)',
       f'Transfer to Finished Stock &nbsp; 9,100 &times; 6 &nbsp;=&nbsp; <b>{R}54,600</b>'])}"""

    pa = acct("Process A Account",
      [("To Units introduced", 10000, 2.00, 20000),
       ("To Materials", "", "", 2000),
       ("To Wages", "", "", 10000),
       ("To Overheads", "", "", 2100),
       ("TOT", 10000, "", 34100)],
      [("By Normal loss" + src("300 u &times; " + R + "0.50"), 300, 0.50, 150),
       ("By Abnormal loss" + src("W1: 200 &times; " + R + "3.50"), 200, 3.50, 700),
       ("By Transfer to Process B" + src("W1: 9,500 &times; " + R + "3.50"), 9500, 3.50, 33250),
       None,
       ("TOT", 10000, "", 34100)])

    pb = acct("Process B Account",
      [("To Transfer from Process A", 9500, 3.50, 33250),
       ("To Materials", "", "", 3000),
       ("To Wages", "", "", 16000),
       ("To Overheads", "", "", 2375),
       ("To Abnormal gain" + src("W2: 75 &times; " + R + "6 &mdash; DEBIT"), 75, 6.00, 450),
       ("TOT", 9575, "", 55075)],
      [("By Normal loss" + src("475 u &times; " + R + "1"), 475, 1.00, 475),
       ("By Transfer to Finished Stock" + src("W2: 9,100 &times; " + R + "6"), 9100, 6.00, 54600),
       None, None, None,
       ("TOT", 9575, "", 55075)])

    nl = acct("Normal Loss Account",
      [("To Process A A/c", 300, 0.50, 150),
       ("To Process B A/c", 475, 1.00, 475),
       ("TOT", 775, "", 625)],
      [("By Abnormal Gain A/c" + src("75 u &times; " + R + "1 (B's scrap rate)"), 75, 1.00, 75),
       ("By Cost Ledger Control A/c (scrap sold)", 700, "", 550),
       ("TOT", 775, "", 625)])

    al = acct("Abnormal Loss Account",
      [("To Process A A/c", 200, 3.50, 700),
       ("TOT", 200, "", 700)],
      [("By Cost Ledger Control A/c" + src("200 &times; " + R + "0.50"), 200, 0.50, 100),
       ("By Profit &amp; Loss A/c", "", "", 600),
       ("TOT", 200, "", 700)])

    ag = acct("Abnormal Gain Account",
      [("To Normal Loss A/c", 75, 1.00, 75),
       ("To Profit &amp; Loss A/c", "", "", 375),
       ("TOT", 75, "", 450)],
      [("By Process B A/c", 75, 6.00, 450),
       None,
       ("TOT", 75, "", 450)])

    return ("<div class='prob long'>"
            + prob_head("Q8", "Loss in A, gain in B, two scrap rates",
                        "Loss &amp; gain &middot; p.10")
            + question(q) + read(rd) + method(mt) + wn(wnh)
            + pa + pb + nl + al + ag
            + trap(bullets([
                'Using ' + R + '0.50 as the scrap rate in Process B. B&rsquo;s wastage sells for '
                + R + '1. Two processes, two rates.',
                'Taking 5% of 10,000 in Process B. It receives only 9,500.',
                'Netting the abnormal loss of Process A against the abnormal gain of Process B. '
                'They are separate accounts and separate P&amp;L entries &mdash; never set one off '
                'against the other.']))
            + ans([("Cost per unit &mdash; Process A", f"{R} 3.50"),
                   ("Cost per unit &mdash; Process B", f"{R} 6.00"),
                   ("Abnormal loss (A, 200 units)", f"{R} 700 &mdash; net to P&amp;L {R} 600"),
                   ("Abnormal gain (B, 75 units)", f"{R} 450 &mdash; net to P&amp;L {R} 375"),
                   ("Transferred to Finished Stock (9,100 units)", f"{R} 54,600")])
            + "</div>")


# ======================================================================
# PROBLEM 9
# ======================================================================
def q9():
    q = f"""<p>The following details are extracted from the costing records of an oil mill for
the year ended 31st March, 2015. Purchase of 5,400 tonnes of coconut
<span class="rs">{R}</span>2,20,000.</p>
{table(None, [("Particulars",""),("Crushing","r"),("Refining","r"),("Finishing","r")],
 [["Cost of labour","2,750","1,100","1,650"],
  ["Electric power","660","396","264"],
  ["Sundry material","110","2,200","&mdash;"],
  ["Repairs to machinery","308","363","154"],
  ["Steam","600","495","495"],
  ["Factory expenses","1,452","726","242"]], headcls="lite")}
<p>Cost of sacks <span class="rs">{R}</span>8,250. 3,200 tonnes of crude oil were produced.
2,600 tonnes of oil produced by the refining process. 2,550 tonnes of refined oil were finished
for delivery. Coconut sacks sold <span class="rs">{R}</span>440. 1,925 tonnes of coconut residue
sold <span class="rs">{R}</span>12,100. Loss in weight in crushing 275 tonnes. 500 tonnes of
by-products obtained from refining process <span class="rs">{R}</span>7,425.</p>
<p>Show the accounts for (a) coconut crushing process, (b) refining process, (c) finishing
process, to arrive at the cost per tonne of each process and the total cost per tonne of the
finished oil.</p>"""

    rd = f"""<p>A long question, but it is only Q1 with three deductions. The one thing that makes
it easy is the <b>units reconciliation</b> &mdash; do it first and the whole answer falls out.</p>
{bullets([
 '<b>Crushing:</b> 5,400 t in. Out: crude oil 3,200 + residue 1,925 + loss in weight 275 = '
 '5,400 &#10003;. Perfect &mdash; no abnormal item.',
 '<b>Refining:</b> 3,200 t in. Out: refined oil 2,600 + by-product 500 = 3,100, so loss in '
 'weight = <b>100 t</b> (you have to work this out; the question does not give it).',
 '<b>Finishing:</b> 2,600 t in, 2,550 t out, so loss in weight = <b>50 t</b>.',
 'Three items are <b>credited</b> to their process because they are saleable: sacks 440 and '
 'residue 12,100 in crushing, by-product 7,425 in refining.',
 'Loss in weight is pure evaporation. It has <b>no scrap value</b>, so it carries no rupee '
 'figure &mdash; only tonnes. Show the tonnes and put a dash in the amount column.'])}"""

    mt = steps([
        "Reconcile tonnes for each stage first. Work out any loss in weight the question has "
        "not given you.",
        "Debit the process with the material coming in plus all its own expenses.",
        "Credit any saleable output that is <i>not</i> the main product (sacks, residue, "
        "by-product) at its sale value.",
        "Credit the loss in weight in tonnes only, amount nil.",
        "The balance is the cost of the main output. Divide by its tonnage for cost per tonne.",
        "Carry that balance forward as the debit of the next process."])

    wnh = f"""<h4 class="mini">W1 &nbsp;Tonnage reconciliation &mdash; do this before anything else</h4>
{table(None, [("Stage",""),("In (t)","r"),("Main output (t)","r"),("Other output (t)","r"),
              ("Loss in weight (t)","r")],
 [["Crushing","5,400","3,200 crude oil","1,925 residue","275 &nbsp;<i>(given)</i>"],
  ["Refining","3,200","2,600 refined oil","500 by-product","<b>100</b> &nbsp;<i>(derived)</i>"],
  ["Finishing","2,600","2,550 finished oil","&mdash;","<b>50</b> &nbsp;<i>(derived)</i>"]],
 headcls="lite")}
{calc(['Refining loss &nbsp;=&nbsp; 3,200 &minus; 2,600 &minus; 500 &nbsp;=&nbsp; <b>100 tonnes</b>',
       'Finishing loss &nbsp;=&nbsp; 2,600 &minus; 2,550 &nbsp;=&nbsp; <b>50 tonnes</b>'])}

<h4 class="mini">W2 &nbsp;Cost per tonne at each stage</h4>
{calc([f'Crushing &nbsp;=&nbsp; ' + frac("2,21,590", "3,200 t") + f' &nbsp;=&nbsp; <b>{R}69.25</b>',
       f'Refining &nbsp;=&nbsp; ' + frac("2,19,445", "2,600 t") + f' &nbsp;=&nbsp; <b>{R}84.40</b>',
       f'Finishing &nbsp;=&nbsp; ' + frac("2,22,250", "2,550 t") + f' &nbsp;=&nbsp; <b>{R}87.16</b>'])}"""

    c1 = acct("(a) Coconut Crushing Process Account",
      [("To Coconut purchased", 5400, "", 220000),
       ("To Cost of sacks", "", "", 8250),
       ("To Cost of labour", "", "", 2750),
       ("To Electric power", "", "", 660),
       ("To Sundry material", "", "", 110),
       ("To Repairs to machinery", "", "", 308),
       ("To Steam", "", "", 600),
       ("To Factory expenses", "", "", 1452),
       ("TOT", 5400, "", 234130)],
      [("By Sale of sacks", "", "", 440),
       ("By Sale of coconut residue", 1925, "", 12100),
       ("By Loss in weight" + src("evaporation &mdash; tonnes only, no value"), 275, "", "&mdash;"),
       ("By Crude oil to Refining" + src("W2: 2,34,130 &minus; 440 &minus; 12,100"),
        3200, 69.25, 221590),
       None, None, None, None,
       ("TOT", 5400, "", 234130)])

    c2 = acct("(b) Refining Process Account",
      [("To Crude oil from Crushing", 3200, 69.25, 221590),
       ("To Cost of labour", "", "", 1100),
       ("To Electric power", "", "", 396),
       ("To Sundry material", "", "", 2200),
       ("To Repairs to machinery", "", "", 363),
       ("To Steam", "", "", 495),
       ("To Factory expenses", "", "", 726),
       ("TOT", 3200, "", 226870)],
      [("By Sale of by-products", 500, "", 7425),
       ("By Loss in weight" + src("W1: derived as 100 t"), 100, "", "&mdash;"),
       ("By Refined oil to Finishing" + src("W2: 2,26,870 &minus; 7,425"), 2600, 84.40, 219445),
       None, None, None, None,
       ("TOT", 3200, "", 226870)])

    c3 = acct("(c) Finishing Process Account",
      [("To Refined oil from Refining", 2600, 84.40, 219445),
       ("To Cost of labour", "", "", 1650),
       ("To Electric power", "", "", 264),
       ("To Repairs to machinery", "", "", 154),
       ("To Steam", "", "", 495),
       ("To Factory expenses", "", "", 242),
       ("TOT", 2600, "", 222250)],
      [("By Loss in weight" + src("W1: derived as 50 t"), 50, "", "&mdash;"),
       ("By Finished oil (cost of delivery)" + src("W2: 2,22,250 &divide; 2,550 t"),
        2550, 87.16, 222250),
       None, None, None, None,
       ("TOT", 2600, "", 222250)])

    return ("<div class='prob long'>"
            + prob_head("Q9", "Oil mill &mdash; three stages, three deductions",
                        "Loss &amp; gain &middot; p.10&ndash;11")
            + question(q) + read(rd) + method(mt) + wn(wnh) + c1 + c2 + c3
            + trap(bullets([
                'Treating the sacks, residue and by-product as income in Profit &amp; Loss. '
                'They reduce the cost of the process that produced them.',
                'Giving the loss in weight a rupee value. It evaporated &mdash; there is nothing to '
                'sell. Tonnes only.',
                'Not deriving the refining and finishing losses. If you skip them the tonnage '
                'columns will not add up and the examiner will see it immediately.',
                'Dividing the crushing cost by 5,400 tonnes. The cost belongs to the 3,200 '
                'tonnes of crude oil that actually came out.']))
            + ans([("Cost per tonne &mdash; Crushing (crude oil)", f"{R} 69.25"),
                   ("Cost per tonne &mdash; Refining (refined oil)", f"{R} 84.40"),
                   ("Cost per tonne &mdash; Finishing (finished oil)", f"{R} 87.16"),
                   ("Total cost of 2,550 tonnes delivered", f"{R} 2,22,250")],
                  "Closing line: &ldquo;The total cost per tonne of the finished oil is "
                  f"<span class='rs'>{R}</span>87.16.&rdquo;")
            + "</div>")


# ======================================================================
def build():
    return (opener() + q1() + q2() + q3() + q4() + q5()
            + q6() + q7() + q8() + q9())
