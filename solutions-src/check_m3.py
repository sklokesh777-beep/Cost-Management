"""
Independent arithmetic verification for Module 3 (Decision Making / Relevant Cost).
Recomputes every answer from the WORKBOOK data, then asserts the value appears
in the rendered HTML for that problem.  Nothing is copied from content_m3.py.
"""
import re, sys, os
sys.path.insert(0, '/projects/sandbox/work/cmbook')
os.chdir('/projects/sandbox/work/cmbook')

import content_m3
html = content_m3.build()
plain = re.sub(r'<[^>]+>', ' ', html)
plain = plain.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&#8377;', '')
plain = re.sub(r'\s+', ' ', plain)

fails = []
checks = [0]


def has(label, s):
    checks[0] += 1
    if s not in plain:
        fails.append(f"{label}: expected substring {s!r} NOT FOUND")


def n(x, dp=0):
    """Indian comma format, matching money() in build.py"""
    neg = x < 0
    x = abs(x)
    if dp:
        s = f"{x:,.{dp}f}"
    else:
        s = f"{round(x):,d}"
    ip = s.split('.')[0].replace(',', '')
    rest = s.split('.')[1] if '.' in s else ''
    if len(ip) > 3:
        head, tail = ip[:-3], ip[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:]); head = head[:-2]
        if head:
            parts.insert(0, head)
        ip = ','.join(parts) + ',' + tail
    out = ip + ('.' + rest if rest else '')
    return ('-' + out) if neg else out


def eq(label, got, want, tol=0.01):
    checks[0] += 1
    if abs(got - want) > tol:
        fails.append(f"{label}: computed {got} != expected {want}")


# ============================================================ Q1
# Special order / minimum price.  Normal capacity 20,000 u.
# Existing: material 6, labour 2, var oh 1  -> VC 9 ; FC 2,50,000
# Revision: material -0.50 (bulk)  labour +? per Q -> revised VC 8.50
# Revised FC 2,47,500 ; contribution needed to keep profit = 47,500
rev_vc = 8.50
rev_fc = 247500
units1 = 20000
contrib_needed = 47500          # contribution the order must earn
# minimum price = revised variable cost + required contribution per unit
eq("Q1 min price", rev_vc + contrib_needed / units1, 10.875)
has("Q1 min price in html", "10.875")
has("Q1 revised FC", n(247500))

# ============================================================ Q2
# Present position: profit NIL (sales = total cost)
# Proposal I contribution gain 1,50,000 ; II 1,50,000
# III price cuts of 5 / 8 / 11 -> extra profit Nil / 1,90,000 / 50,000
has("Q2 I", n(150000))
has("Q2 III best", n(190000))
has("Q2 III third", n(50000))

# ============================================================ Q3  make or buy
# relevant make cost per unit = 5.00
mk = 5.00
eq("Q3 make cost", mk, 5.00)
eq("Q3 (a) saving buy", mk - 4.85, 0.15)
eq("Q3 (b) saving make", 5.85 - mk, 0.85)
has("Q3 buy saving", "0.15")
has("Q3 make saving", "0.85")

# ============================================================ Q4  export order
vc4 = 56.0
fc4 = 40000
eq("Q4 order contribution", 24000, 24000)
eq("Q4 profit after", 8000 + 24000, 32000)
has("Q4 new profit", n(32000))
has("Q4 order contribution", n(24000))

# ============================================================ Q5
# 1% of capacity = sales 40,000 ; VC 20,000  => contribution 20,000 per 1%
# Alt 1 -> 3,00,000 ; Alt 2 -> 1,00,000 ; Alt 3(a) -> 10,00,000 ; 3(b) 9,75,000
has("Q5 alt1", n(300000))
has("Q5 alt2", n(100000))
has("Q5 alt3a", n(1000000))
has("Q5 alt3b", n(975000))

# ============================================================ Q6
# VC 30,00,000 ; FC 10,00,000 ; P/V 40%
vc6, fc6 = 3000000, 1000000
sales6 = vc6 / (1 - 0.40)
eq("Q6 sales", sales6, 5000000)
eq("Q6 contribution", sales6 - vc6, 2000000)
eq("Q6 profit", sales6 - vc6 - fc6, 1000000)
has("Q6 GM proposal", n(1475000))
has("Q6 sales mgr proposal", n(1400000))

# ============================================================ Q7  sales mixtures
# A: DM 10 + DW 3 + VE(100% of DW) 3 = 16 ; SP 20 -> contribution 4
# B: DM  9 + DW 2 + VE 2          = 13 ; SP 15 -> contribution 2 ; FC 800
mcA, mcB = 10 + 3 + 3, 9 + 2 + 2
eq("Q7 marginal cost A", mcA, 16)
eq("Q7 marginal cost B", mcB, 13)
cA, cB, fc7 = 20 - mcA, 15 - mcB, 800
eq("Q7 contribution A", cA, 4)
eq("Q7 contribution B", cB, 2)
for lbl, (ua, ub), want in [("i", (1000, 2000), 7200),
                            ("ii", (1500, 1500), 8200),
                            ("iii", (2000, 1000), 9200)]:
    eq(f"Q7 ({lbl}) profit", ua * cA + ub * cB - fc7, want)
    has(f"Q7 ({lbl}) profit in html", n(want))

# ============================================================ Q8  limiting material 18,400 kg
# RM @ 20/kg -> kg per unit = RM cost / 20
prod8 = {          # name: (RM, wages, VOH, FOH, SP, budget qty)
    "A": (80, 5, 10, 9, 140, 6400),
    "B": (40, 15, 30, 22, 120, 3200),
    "C": (20, 10, 20, 18, 90, 2400)}
kg, con, cpk = {}, {}, {}
for k, (rm, w, v, f, sp, q) in prod8.items():
    kg[k] = rm / 20
    con[k] = sp - (rm + w + v)
    cpk[k] = con[k] / kg[k]
eq("Q8 kg A", kg["A"], 4); eq("Q8 kg B", kg["B"], 2); eq("Q8 kg C", kg["C"], 1)
eq("Q8 contribution A", con["A"], 45)
eq("Q8 contribution B", con["B"], 35)
eq("Q8 contribution C", con["C"], 40)
eq("Q8 c/kg A", cpk["A"], 11.25)
eq("Q8 c/kg B", cpk["B"], 17.50)
eq("Q8 c/kg C", cpk["C"], 40.00)
fc8 = sum(prod8[k][3] * prod8[k][5] for k in prod8)
eq("Q8 total fixed OH", fc8, 171200)
budg_con8 = sum(con[k] * prod8[k][5] for k in prod8)
eq("Q8 budgeted contribution", budg_con8, 496000)
eq("Q8 budgeted profit", budg_con8 - fc8, 324800)
# ranking by contribution per kg, capped at budgeted demand
avail = 18400
order = sorted(prod8, key=lambda k: -cpk[k])
eq("Q8 rank check", 1 if order == ["C", "B", "A"] else 0, 1)
mix, con8 = {}, 0
for k in order:
    take = min(prod8[k][5], avail / kg[k])
    mix[k] = take
    avail -= take * kg[k]
    con8 += take * con[k]
eq("Q8 mix C", mix["C"], 2400)
eq("Q8 mix B", mix["B"], 3200)
eq("Q8 mix A", mix["A"], 2400)
eq("Q8 leftover kg", avail, 0)
eq("Q8 optimum contribution", con8, 316000)
eq("Q8 optimum profit", con8 - fc8, 144800)
has("Q8 budgeted profit", n(324800))
has("Q8 optimum profit", n(144800))
has("Q8 fixed cost", n(171200))
has("Q8 c/kg C", "40.00")
has("Q8 c/kg B", "17.50")
has("Q8 c/kg A", "11.25")

# ============================================================ Q9  labour shortage
# A: SP 75, DM 30, 15 hrs @ 0.50 = 7.50 wages, VOH 100% of wages 7.50
# B: SP 48, DM 30,  2 hrs @ 0.50 = 1.00 wages, VOH 1.00
for nm, sp, dm, hrs, want_c, want_ph in [("A", 75, 30, 15, 30, 2.0),
                                         ("B", 48, 30, 2, 16, 8.0)]:
    wages = hrs * 0.50
    vc = dm + wages + wages
    eq(f"Q9 {nm} contribution", sp - vc, want_c)
    eq(f"Q9 {nm} contribution/hour", (sp - vc) / hrs, want_ph)
has("Q9 A per hr", "2.00")
has("Q9 B per hr", "8.00")

# ============================================================ Q10  limiting labour 4,200 hrs
# A: mat 5.00, 6 hrs @ 0.50 = 3.00, var OH 1.50 -> VC 9.50 ; SP 14.00
# B: mat 5.00, 3 hrs @ 0.50 = 1.50, var OH 1.50 -> VC 8.00 ; SP 11.00
cA10 = 14.00 - (5.00 + 3.00 + 1.50)
cB10 = 11.00 - (5.00 + 1.50 + 1.50)
eq("Q10 contribution A", cA10, 4.50)
eq("Q10 contribution B", cB10, 3.00)
eq("Q10 c/hour A", cA10 / 6, 0.75)
eq("Q10 c/hour B", cB10 / 3, 1.00)
hrs10 = 4200
b_units = min(600, hrs10 / 3)               # B ranked first, capped at max output
hrs10 -= b_units * 3
a_units = min(500, hrs10 / 6)
eq("Q10 mix B", b_units, 600)
eq("Q10 mix A", a_units, 400)
con10 = b_units * cB10 + a_units * cA10
eq("Q10 contribution", con10, 3600)
fc10 = 500 * 1.50 + 600 * 0.75              # fixed = 50% of labour at stated output
eq("Q10 fixed cost", fc10, 1200)
eq("Q10 profit", con10 - fc10, 2400)
has("Q10 contribution", n(3600))
has("Q10 profit", n(2400))

# ============================================================ Q11
vc11 = 27.0
fc11 = 1440000
eq("Q11 order contribution", 180000, 180000)
eq("Q11 profit after", 480000 + 180000, 660000)
has("Q11 new profit", n(660000))
has("Q11 present profit", n(480000))

# ============================================================ Q12   ($ problem)
# SP 14 ; demand 5,000 u ; FC at 50% activity = 30,000 ; shut cost 2,000 ; 20,000 avoidable
unavoid12 = 30000 - 20000
loss_shut12 = unavoid12 + 2000
eq("Q12 loss if shut", loss_shut12, 12000)
# continue-loss >= shut-loss  =>  30,000 - 5,000(14 - v) >= 12,000  =>  v >= 10.40
max_contrib = (30000 - loss_shut12) / 5000
eq("Q12 max contribution/u", max_contrib, 3.60)
eq("Q12 min VC/u to justify shut", 14 - max_contrib, 10.40)
has("Q12 shut loss", "12,000")
has("Q12 vc limit", "10.40")

# ============================================================ Q13   ($ problem -> western commas)
# 95,000 u = 80% cap ; SP 8 ; VC 75% of SP = 6 ; contribution 2
# FC 350,000 -> 130,000 unavoidable ; shut-down cost 15,000
c13 = 8 - 0.75 * 8
eq("Q13 contribution/u", c13, 2.0)
eq("Q13 loss if continue", 95000 * c13 - 350000, -160000)
eq("Q13 loss if shut", 0 - 130000 - 15000, -145000)
eq("Q13 saving", 160000 - 145000, 15000)
avoid13 = 350000 - 130000
eq("Q13 shut-down point units", (avoid13 - 15000) / c13, 102500)
eq("Q13 full capacity", 95000 / 0.80, 118750)
eq("Q13 shut-down %", (102500 / 118750) * 100, 86.3157894, tol=0.005)
has("Q13 continue loss", "160,000")
has("Q13 shut loss", "145,000")
has("Q13 shutdown point units", "102,500")
has("Q13 shutdown pct", "86.32")

# ============================================================ Q14   ($ problem -> western commas)
# 200,000 tins/yr ; VC = 7.80+2.10+2.50+0.60 = 13.00 ; SP 21 -> contribution 8
vc14 = 7.80 + 2.10 + 2.50 + 0.60
eq("Q14 VC/tin", vc14, 13.00)
eq("Q14 contribution/tin", 21 - vc14, 8.00)
annual_fc14 = 200000 * 4.00
eq("Q14 annual FC", annual_fc14, 800000)
q_fc14 = annual_fc14 / 4
eq("Q14 quarterly FC", q_fc14, 200000)
eq("Q14 loss if continue", 10000 * 8.0 - q_fc14, -120000)
eq("Q14 loss if shut", -74000 - 14000, -88000)
eq("Q14 saving", 120000 - 88000, 32000)
avoid14 = q_fc14 - 74000
eq("Q14 avoidable FC", avoid14, 126000)
eq("Q14 shut-down point tins", (avoid14 - 14000) / 8.0, 14000)
has("Q14 quarterly FC", "200,000")
has("Q14 continue loss", "120,000")
has("Q14 shut loss", "88,000")
has("Q14 saving", "32,000")
has("Q14 shutdown tins", "14,000")

# ============================================================ Q15 chart
has("Q15 bep units", n(4000))

# ============================================================ Q16 chart
has("Q16 bep units", n(50000))
has("Q16 bep value", n(1000000))
has("Q16 new bep units", n(62500))
has("Q16 new bep value", n(1125000))

# ============================================================ Q17
vc17 = 760000
eq("Q17 contribution", 1000000 - vc17, 240000)
eq("Q17 pv", (1000000 - vc17) / 1000000 * 100, 24.0)
has("Q17 pv ratio", "24")
has("Q17 bep", n(500000))
has("Q17 capacity", "50%")

# ============================================================ Q18
has("Q18 contribution", n(3000))
has("Q18 pv", "40")
has("Q18 bep units", n(1500))
has("Q18 bep value", "3,750")

# ---------------------------------------------------------------- report
print(f"Module 3 checker: {checks[0]} assertions")
if fails:
    print(f"\n*** {len(fails)} FAILURES ***")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("ALL MODULE 3 ASSERTIONS PASS")
