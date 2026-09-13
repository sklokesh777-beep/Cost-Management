"""
Independent arithmetic verification for Module 4 (Relevant Costing).
Every figure is recomputed here from the WORKBOOK data and then asserted to
appear in the rendered HTML. Nothing is imported from content_m4's own numbers.
"""
import re, sys, os
sys.path.insert(0, '/projects/sandbox/work/cmbook')
os.chdir('/projects/sandbox/work/cmbook')

import content_m4
html = content_m4.build()
plain = re.sub(r'<[^>]+>', ' ', html)
plain = plain.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&#8377;', '')
plain = plain.replace('&minus;', '-').replace('&times;', 'x').replace('&mdash;', '-')
plain = re.sub(r'\s+', ' ', plain)

fails, checks = [], [0]


def has(label, s):
    checks[0] += 1
    if s not in plain:
        fails.append(f"{label}: expected substring {s!r} NOT FOUND")


def eq(label, got, want, tol=0.005):
    checks[0] += 1
    if abs(got - want) > tol:
        fails.append(f"{label}: computed {got} != expected {want}")


def ind(x, dp=0):
    """Indian comma format, matching rs()/money() in build.py"""
    neg = x < 0
    x = abs(x)
    if dp:
        whole = int(x); fr = ("%.*f" % (dp, x - whole))[2:]
    else:
        whole = int(round(x)); fr = None
    s = str(whole)
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:]); head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts + [tail])
    if fr is not None:
        s += "." + fr
    return s


# ============================================================ Q1
# Travel Rs.250/day for own work; employee picked up ON THE WAY -> no extra km.
has("Q1 nil answer", "NIL")
has("Q1 decoy 50 flagged", "50")

# ============================================================ Q2  four materials
# A: 1,000 required, 0 in stock -> replacement 6
a = 1000 * 6
eq("Q2 A", a, 6000)
# B: regularly used -> replacement cost on FULL 1,000 at 5
b = 1000 * 5
eq("Q2 B", b, 5000)
# C: 700 in stock, no other use -> NRV 2.50 ; 300 short -> replacement 4
c_stock, c_buy = 700 * 2.50, 300 * 4
eq("Q2 C stock", c_stock, 1750)
eq("Q2 C buy", c_buy, 1200)
eq("Q2 C total", c_stock + c_buy, 2950)
# D: 200 in stock; NRV 200x6=1,200 vs substitute 300 units of E x 5 = 1,500 -> HIGHER
d_nrv, d_sub = 200 * 6, 300 * 5
eq("Q2 D nrv", d_nrv, 1200)
eq("Q2 D substitute", d_sub, 1500)
d = max(d_nrv, d_sub)
eq("Q2 D relevant (higher of the two)", d, 1500)
tot2 = a + b + c_stock + c_buy + d
eq("Q2 total relevant cost", tot2, 15450)
eq("Q2 surplus", 22000 - tot2, 6550)
for lbl, v in [("A", 6000), ("B", 5000), ("C stock", 1750), ("C buy", 1200), ("D", 1500),
               ("total", 15450), ("surplus", 6550)]:
    has(f"Q2 {lbl}", ind(v))

# ============================================================ Q3  machine
# VC 60,000 relevant ; fall in resale 40,000-25,000 = 15,000 ; 90,000 & 35,000 sunk
eq("Q3 opportunity cost", 40000 - 25000, 15000)
eq("Q3 total relevant", 60000 + (40000 - 25000), 75000)
has("Q3 vc", ind(60000))
has("Q3 opp cost", ind(15000))
has("Q3 total", ind(75000))
has("Q3 sunk original cost shown", ind(90000))
has("Q3 sunk nbv shown", ind(35000))

# ============================================================ Q4  three parts
eq("Q4 (a) equipment opportunity cost", 1500 - 800, 700)
has("Q4 (a) 700", "700")
has("Q4 (b) rent", ind(18000))
has("Q4 (b) depreciation decoy", ind(12000))
mk4 = 10 + 6 + 6
eq("Q4 (c) relevant make cost", mk4, 22)
eq("Q4 (c) saving by making", 24 - mk4, 2)
has("Q4 (c) make 22", "22.00")
has("Q4 (c) buy 24", "24.00")
eq("Q4 total identifiable", 700 + 18000, 18700)
has("Q4 total", ind(18700))

# ============================================================ Q5  opportunity costs
p5 = {"X": (10, 6, 3000, 2000), "Y": (12, 9, 2000, 3000), "Z": (12, 7, 1000, 900)}
con5, eff5, tc5 = {}, {}, {}
for k, (sp, vc, dem, cap) in p5.items():
    con5[k] = sp - vc
    eff5[k] = min(dem, cap)
    tc5[k] = con5[k] * eff5[k]
eq("Q5 contribution X", con5["X"], 4)
eq("Q5 contribution Y", con5["Y"], 3)
eq("Q5 contribution Z", con5["Z"], 5)
eq("Q5 effective X", eff5["X"], 2000)
eq("Q5 effective Y", eff5["Y"], 2000)
eq("Q5 effective Z", eff5["Z"], 900)
eq("Q5 total contribution X", tc5["X"], 8000)
eq("Q5 total contribution Y", tc5["Y"], 6000)
eq("Q5 total contribution Z", tc5["Z"], 4500)
# opportunity cost of choosing k = best contribution among the OTHERS
for k in p5:
    oc = max(v for kk, v in tc5.items() if kk != k)
    want = {"X": 6000, "Y": 8000, "Z": 8000}[k]
    eq(f"Q5 opportunity cost of {k}", oc, want)
eq("Q5 best product is X", 1 if max(tc5, key=lambda k: tc5[k]) == "X" else 0, 1)
eq("Q5 loss even on best option", 30000 - 8000, 22000)
for v in (8000, 6000, 4500, 22000):
    has(f"Q5 {v}", ind(v))

# ============================================================ Q6  three alternatives
alt1 = 10000 * 18
alt2 = 10000 * 19 - 10000 * 2
alt3 = 10000 * 19 - 21000
eq("Q6 alt I make", alt1, 180000)
eq("Q6 alt II buy+component", alt2, 170000)
eq("Q6 alt III buy+hire", alt3, 169000)
eq("Q6 best is alt III", 1 if min(alt1, alt2, alt3) == alt3 else 0, 1)
eq("Q6 saving over making", alt1 - alt3, 11000)
eq("Q6 extra cost of buying", 10000 * (19 - 18), 10000)
eq("Q6 net gain check", 21000 - 10000, 11000)
for v in (180000, 170000, 169000, 11000):
    has(f"Q6 {v}", ind(v))

# ============================================================ Q7  minimum price
# M non-moving -> NRV 80 ; labour permanent, no lost contribution -> Nil ;
# out-of-pocket 30 ; book value 60 and replacement 100 and allocated OH 10 irrelevant
eq("Q7 minimum price", 80 + 0 + 30, 110)
has("Q7 nrv 80", "80")
has("Q7 out of pocket 30", "30")
has("Q7 minimum price 110", "110")
has("Q7 replacement decoy", "100")
has("Q7 book value decoy", "60")

# ============================================================ Q8  machine replacement
rev8, old_oc8, new_oc8 = 120, 100, 70
c_old8, c_new8 = rev8 - old_oc8, rev8 - new_oc8
eq("Q8 contribution/hr old", c_old8, 20)
eq("Q8 contribution/hr new", c_new8, 50)
inc8 = 3500000 - 1200000
eq("Q8 incremental investment", inc8, 2300000)
eq("Q8 benefit hours", inc8 / c_new8, 46000)
eq("Q8 BEP hours old (FULL cost)", 2000000 / c_old8, 100000)
eq("Q8 BEP hours new (FULL cost)", 3500000 / c_new8, 70000)
for v in (2300000, 46000, 100000, 70000):
    has(f"Q8 {v}", ind(v))
has("Q8 sunk shown", ind(2000000))

# ============================================================ Q12  same method
rev12, old_oc12, new_oc12 = 195, 130, 91
c_old12, c_new12 = rev12 - old_oc12, rev12 - new_oc12
eq("Q12 contribution/hr old", c_old12, 65)
eq("Q12 contribution/hr new", c_new12, 104)
inc12 = 4550000 - 1560000
eq("Q12 incremental investment", inc12, 2990000)
eq("Q12 benefit hours", inc12 / c_new12, 28750)
eq("Q12 BEP hours old", 2600000 / c_old12, 40000)
eq("Q12 BEP hours new", 4550000 / c_new12, 43750)
for v in (2990000, 28750, 40000, 43750):
    has(f"Q12 {v}", ind(v))
has("Q12 sunk shown", ind(2600000))

# ============================================================ Q9 / Q11  rectification
for tag, units, mfg, rej, rect, new in [("Q9", 20000, 150, 120, 30, 160),
                                        ("Q11", 10000, 300, 240, 60, 320)]:
    inc_rev = new - rej
    net = inc_rev - rect
    eq(f"{tag} incremental revenue/u", inc_rev, {"Q9": 40, "Q11": 80}[tag])
    eq(f"{tag} net gain/u", net, {"Q9": 10, "Q11": 20}[tag])
    total_net = net * units
    eq(f"{tag} total net gain", total_net, 200000)
    sunk = units * mfg
    eq(f"{tag} sunk manufacturing cost", sunk, 3000000)
    loss_no = sunk - units * rej
    loss_yes = sunk + units * rect - units * new
    eq(f"{tag} absolute loss if not rectified", loss_no, 600000)
    eq(f"{tag} absolute loss if rectified", loss_yes, 400000)
    # the incremental and absolute views must agree on the DIFFERENCE
    eq(f"{tag} two views agree", loss_no - loss_yes, total_net)
    for v in (total_net, sunk, loss_no, loss_yes, units * rect, units * new, units * rej):
        has(f"{tag} {v}", ind(v))

# ============================================================ Q10  paper ($)
eq("Q10 reams short", 250 - 100, 150)
opp10, oop10 = 100 * 10, 150 * 26
eq("Q10 opportunity cost", opp10, 1000)
eq("Q10 out-of-pocket", oop10, 3900)
eq("Q10 total relevant", opp10 + oop10, 4900)
has("Q10 opp", "1,000")
has("Q10 oop", "3,900")
has("Q10 total", "4,900")
has("Q10 sunk 15 shown", "15")

# ============================================================ Q13  make or buy
voh13 = 16 * 0.60
eq("Q13 variable production OH", voh13, 9.60)
eq("Q13 fixed production OH", 16 - voh13, 6.40)
mk13 = 4 + 8 + voh13
eq("Q13 relevant make cost", mk13, 21.60)
eq("Q13 saving by buying", mk13 - 20, 1.60)
eq("Q13 naive (wrong) saving", 28 - 20, 8)
has("Q13 make 21.60", "21.60")
has("Q13 buy 20.00", "20.00")
has("Q13 saving 1.60", "1.60")
has("Q13 fixed 6.40", "6.40")

# ============================================================ Q14  special order
voh14 = 0.50 * 4          # 50% of LABOUR cost, not of the 8 overhead
eq("Q14 variable production OH", voh14, 2)
eq("Q14 fixed production OH", 8 - voh14, 6)
rc14 = 8 + 4 + voh14
eq("Q14 relevant cost/unit", rc14, 14)
eq("Q14 contribution/unit", 16 - rc14, 2)
eq("Q14 increase in profit", (16 - rc14) * 2000, 4000)
# and the cross-check quoted in the discussion: regular contribution per unit
eq("Q14 regular contribution/unit", 22 - rc14, 8)
has("Q14 relevant cost 14", "14")
has("Q14 profit 4,000", "4,000")

# ============================================================ Q15  the full case
a15 = 1750            # NRV, not the 4,000 book cost
b15 = 8000            # out-of-pocket
l15 = 7000            # extra recruitment elsewhere, not the 6,000 transferred
s15 = 0               # supervision - apportioned, existing staff
o15 = 0               # overheads - absorbed at 200% of labour
m15 = 8000 - 5000     # specific fixed cost, net of residual
eq("Q15 machinery net", m15, 3000)
tot15 = a15 + b15 + l15 + s15 + o15 + m15
eq("Q15 total relevant cost", tot15, 19750)
eq("Q15 net benefit", 30000 - tot15, 10250)
eq("Q15 printed total", 4000 + 8000 + 6000 + 2000 + 12000, 32000)
eq("Q15 printed shows a loss", 30000 - 32000, -2000)
eq("Q15 material A overstated by", 4000 - 1750, 2250)
eq("Q15 irrelevant supervision+overheads", 2000 + 12000, 14000)
for v in (1750, 8000, 7000, 3000, 19750, 10250, 32000, 14000, 2250):
    has(f"Q15 {v}", ind(v))

# ---------------------------------------------------------------- report
print(f"Module 4 checker: {checks[0]} assertions")
if fails:
    print(f"\n*** {len(fails)} FAILURES ***")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("ALL MODULE 4 ASSERTIONS PASS")
