"""
Independent arithmetic verification for Module 5 (Budgetary Control).
Every figure recomputed from the WORKBOOK data, then asserted present in the
rendered HTML.  Nothing is taken from content_m5's own numbers.
"""
import re, sys, os
sys.path.insert(0, '/projects/sandbox/work/cmbook')
os.chdir('/projects/sandbox/work/cmbook')

import content_m5
html = content_m5.build()
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
# per-unit at 5,000 units; splits: admin 5% var, selling 20% fixed, distn 10% fixed
u1, u2 = 5000, 7000
lines = {              # name: (per unit, fixed_fraction)
    "materials": (50, 0.0), "labour": (20, 0.0), "var_oh": (15, 0.0),
    "fixed_oh": (10, 1.0),
    "admin": (10, 0.95),          # 5% variable -> 95% fixed
    "selling": (6, 0.20),         # "20% Fixed"    -> fixed fraction 0.20
    "distn": (5, 0.10)}           # "10% Fixed"    -> fixed fraction 0.10
tot_fixed1 = 0.0
tot_varrate1 = 0.0
for nm, (pu, ff) in lines.items():
    total5 = pu * u1
    fx = total5 * ff
    vr = (total5 - fx) / u1
    tot_fixed1 += fx
    tot_varrate1 += vr
eq("Q1 fixed OH total", 10 * u1 * 1.0, 50000)
eq("Q1 admin fixed", 10 * u1 * 0.95, 47500)
eq("Q1 admin variable rate", (10 * u1 * 0.05) / u1, 0.50)
eq("Q1 selling fixed", 6 * u1 * 0.20, 6000)
eq("Q1 selling variable rate", (6 * u1 * 0.80) / u1, 4.80)
eq("Q1 distn fixed", 5 * u1 * 0.10, 2500)
eq("Q1 distn variable rate", (5 * u1 * 0.90) / u1, 4.50)
eq("Q1 total fixed", tot_fixed1, 106000)
eq("Q1 total variable rate", tot_varrate1, 94.80)
eq("Q1 total cost at 5,000", tot_varrate1 * u1 + tot_fixed1, 580000)
eq("Q1 per unit at 5,000", (tot_varrate1 * u1 + tot_fixed1) / u1, 116.00)
t1_7 = tot_varrate1 * u2 + tot_fixed1
eq("Q1 total cost at 7,000", t1_7, 769600)
eq("Q1 per unit at 7,000", t1_7 / u2, 109.94, tol=0.005)
eq("Q1 fixed OH per unit at 7,000", 50000 / u2, 7.142857, tol=0.005)
for v in (106000, 580000, 769600, 350000, 140000, 105000, 47500, 33600, 31500):
    has(f"Q1 {v}", ind(v))
has("Q1 pu 7000", "109.94")
has("Q1 fixed oh pu", "7.14")

# ============================================================ Q2
fixed2 = 50000 + 40000 + 60000 + 70000
eq("Q2 total fixed", fixed2, 220000)
var50 = {"materials": 200000, "labour": 250000, "others": 40000}
semi50 = {"repairs": 100000, "ind_labour": 150000, "others": 90000}
mult = {60: 1.00, 70: 1.10, 90: 1.10 * 1.05}
eq("Q2 90% multiplier compounds", mult[90], 1.155)
sales2 = {60: 1100000, 70: 1300000, 90: 1500000}
want_tot = {50: 1050000, 60: 1148000, 70: 1280000, 90: 1494700}
want_pl = {60: -48000, 70: 20000, 90: 5300}
for cap in (50, 60, 70, 90):
    v = sum(x * cap / 50 for x in var50.values())
    s = sum(x * (1.0 if cap == 50 else mult[cap]) for x in semi50.values())
    eq(f"Q2 total cost at {cap}%", fixed2 + v + s, want_tot[cap])
    if cap in sales2:
        eq(f"Q2 profit at {cap}%", sales2[cap] - (fixed2 + v + s), want_pl[cap])
eq("Q2 repairs at 90%", 100000 * 1.155, 115500)
eq("Q2 ind labour at 90%", 150000 * 1.155, 173250)
eq("Q2 semi others at 90%", 90000 * 1.155, 103950)
eq("Q2 profit peaks at 70 not 90", 1 if want_pl[70] > want_pl[90] else 0, 1)
eq("Q2 profit fall 70->90", want_pl[70] - want_pl[90], 14700)
for v in (220000, 1050000, 1148000, 1280000, 1494700, 48000, 20000, 5300,
          115500, 173250, 103950):
    has(f"Q2 {v}", ind(v))

# ============================================================ Q3   base is 60%
var3 = {"ind_labour": 10500, "ind_materials": 8400}
semi3 = {"repairs": (7000, 0.70), "electricity": (25200, 0.50)}   # (total, fixed fraction)
fixed3 = 70000 + 4000 + 20000
eq("Q3 total fixed", fixed3, 94000)
want3 = {50: 139500, 60: 145100, 70: 150700}
hours3 = {50: 100000, 60: 120000, 70: 140000}
want_rate = {50: 1.395, 60: 1.209, 70: 1.076}
for cap in (50, 60, 70):
    v = sum(x * cap / 60 for x in var3.values())
    s = 0.0
    for nm, (tot, ff) in semi3.items():
        s += tot * ff + (tot * (1 - ff)) * cap / 60
    total = fixed3 + v + s
    eq(f"Q3 total overhead at {cap}%", total, want3[cap])
    eq(f"Q3 labour hours at {cap}%", 120000 * cap / 60, hours3[cap])
    eq(f"Q3 recovery rate at {cap}%", total / hours3[cap], want_rate[cap], tol=0.001)
eq("Q3 repairs fixed half", 7000 * 0.70, 4900)
eq("Q3 electricity fixed half", 25200 * 0.50, 12600)
eq("Q3 repairs at 50%", 4900 + 2100 * 50 / 60, 6650)
eq("Q3 electricity at 70%", 12600 + 12600 * 70 / 60, 27300)
for v in (94000, 139500, 145100, 150700, 8750, 12250, 6650, 23100, 27300):
    has(f"Q3 {v}", ind(v))
for s in ("1.395", "1.209", "1.076"):
    has(f"Q3 rate {s}", s)

# ============================================================ Q4
units4 = {60: 600, 80: 800, 100: 1000}
eq("Q4 units at 80%", 600 / 0.60 * 0.80, 800)
eq("Q4 units at 100%", 600 / 0.60 * 1.00, 1000)
fac_fx, fac_var = 40000 * 0.40, 40000 * 0.60
adm_fx, adm_var = 30000 * 0.60, 30000 * 0.40
eq("Q4 factory fixed", fac_fx, 16000)
eq("Q4 factory variable rate", fac_var / 600, 40.0)
eq("Q4 admin fixed", adm_fx, 18000)
eq("Q4 admin variable rate", adm_var / 600, 20.0)
vr4 = 100 + 40 + 10 + fac_var / 600 + adm_var / 600
fx4 = fac_fx + adm_fx
eq("Q4 total variable rate", vr4, 210)
eq("Q4 total fixed", fx4, 34000)
want4 = {60: 160000, 80: 202000, 100: 244000}
want4pu = {60: 266.67, 80: 252.50, 100: 244.00}
for cap in (60, 80, 100):
    t = vr4 * units4[cap] + fx4
    eq(f"Q4 total cost at {cap}%", t, want4[cap])
    eq(f"Q4 per unit at {cap}%", t / units4[cap], want4pu[cap], tol=0.005)
for v in (160000, 202000, 244000, 34000):
    has(f"Q4 {v}", ind(v))
for s in ("266.67", "252.50", "244.00", "26.67", "22.50"):
    has(f"Q4 {s}", s)

# ============================================================ Q13  high-low
vols = (120000, 150000)
items13 = {"ind_mat": (264000, 330000), "ind_lab": (150000, 187500),
           "maint": (84000, 102000), "superv": (198000, 234000),
           "engg": (94000, 94000)}
res13, tot13 = {}, 0.0
for nm, (lo, hi) in items13.items():
    vr = (hi - lo) / (vols[1] - vols[0])
    fx = lo - vr * vols[0]
    fx_hi = hi - vr * vols[1]
    eq(f"Q13 {nm} fixed consistent from both points", fx, fx_hi)
    res13[nm] = (vr, fx)
    tot13 += fx + vr * 140000
eq("Q13 ind mat variable rate", res13["ind_mat"][0], 2.20)
eq("Q13 ind mat fixed", res13["ind_mat"][1], 0)
eq("Q13 ind lab variable rate", res13["ind_lab"][0], 1.25)
eq("Q13 ind lab fixed", res13["ind_lab"][1], 0)
eq("Q13 maintenance variable rate", res13["maint"][0], 0.60)
eq("Q13 maintenance fixed", res13["maint"][1], 12000)
eq("Q13 supervision variable rate", res13["superv"][0], 1.20)
eq("Q13 supervision fixed", res13["superv"][1], 54000)
eq("Q13 engineering variable rate", res13["engg"][0], 0)
eq("Q13 engineering fixed", res13["engg"][1], 94000)
eq("Q13 total at 1,40,000 units", tot13, 895000)
eq("Q13 total variable rate", sum(v for v, f in res13.values()), 5.25)
eq("Q13 total fixed", sum(f for v, f in res13.values()), 160000)
eq("Q13 rebuild at 1,20,000 = column total", 5.25 * 120000 + 160000,
   264000 + 150000 + 84000 + 198000 + 94000)
eq("Q13 maintenance at 1,40,000", 12000 + 0.60 * 140000, 96000)
eq("Q13 supervision at 1,40,000", 54000 + 1.20 * 140000, 222000)
for v in (308000, 175000, 12000, 84000, 54000, 168000, 94000, 895000, 160000):
    has(f"Q13 {v}", ind(v))
for s in ("2.20", "1.25", "0.70", "0.68", "1.65", "1.56", "0.60", "1.20", "5.25"):
    has(f"Q13 {s}", s)

# ============================================================ Q5  cash budget
sales5 = {"feb": 70000, "mar": 80000, "apr": 96000, "may": 100000, "jun": 120000}
purch5 = {"feb": 44000, "mar": 56000, "apr": 60000, "may": 68000, "jun": 62000}
wages5 = {"feb": 6000, "mar": 9000, "apr": 9000, "may": 11000, "jun": 14000}
exp5 = {"feb": 5000, "mar": 6000, "apr": 7000, "may": 9000, "jun": 9000}
prev = {"apr": "mar", "may": "apr", "jun": "may"}
prev2 = {"apr": "feb", "may": "mar", "jun": "apr"}
bal = 32000
want5 = {"apr": 57000, "may": 82000, "jun": 79000}
for m in ("apr", "may", "jun"):
    cash_s = 0.25 * sales5[m]
    debt = 0.75 * sales5[prev[m]]
    receipts = cash_s + debt
    pay = purch5[prev2[m]] + wages5[prev[m]] + exp5[prev[m]] + (28000 if m == "jun" else 0)
    a = bal + receipts
    closing = a - pay
    eq(f"Q5 {m} cash sales", cash_s, {"apr": 24000, "may": 25000, "jun": 30000}[m])
    eq(f"Q5 {m} collections", debt, {"apr": 60000, "may": 72000, "jun": 75000}[m])
    eq(f"Q5 {m} total A", a, {"apr": 116000, "may": 154000, "jun": 187000}[m])
    eq(f"Q5 {m} total B", pay, {"apr": 59000, "may": 72000, "jun": 108000}[m])
    eq(f"Q5 {m} closing", closing, want5[m])
    bal = closing
eq("Q5 positive throughout", 1 if min(want5.values()) > 0 else 0, 1)
for v in (32000, 57000, 82000, 79000, 116000, 154000, 187000, 59000, 72000, 108000):
    has(f"Q5 {v}", ind(v))

# ============================================================ Q6  overdraft
sales6 = {"feb": 180000, "mar": 192000, "apr": 108000, "may": 174000, "jun": 126000}
purch6 = {"feb": 124800, "mar": 144000, "apr": 243000, "may": 246000, "jun": 268000}
wages6 = {"feb": 12000, "mar": 14000, "apr": 11000, "may": 10000, "jun": 15000}
bal = 25000
want6 = {"apr": 56000, "may": -47000, "jun": -167000}
want_coll6 = {"apr": 186000, "may": 150000, "jun": 141000}
for m in ("apr", "may", "jun"):
    coll = 0.50 * sales6[prev[m]] + 0.50 * sales6[prev2[m]]
    eq(f"Q6 {m} collections", coll, want_coll6[m])
    pay = purch6[prev[m]] + wages6[m]
    a = bal + coll
    closing = a - pay
    eq(f"Q6 {m} total A", a, {"apr": 211000, "may": 206000, "jun": 94000}[m])
    eq(f"Q6 {m} total B", pay, {"apr": 155000, "may": 253000, "jun": 261000}[m])
    eq(f"Q6 {m} closing", closing, want6[m])
    bal = closing                                   # negative MUST carry forward
eq("Q6 max overdraft required", -min(want6.values()), 167000)
for v in (186000, 150000, 141000, 211000, 206000, 94000, 56000, 47000, 167000):
    has(f"Q6 {v}", ind(v))

# ============================================================ Q7  discount + split wages
sales7 = {"feb": 120000, "mar": 130000, "apr": 80000, "may": 116000, "jun": 88000}
purch7 = {"feb": 84000, "mar": 100000, "apr": 104000, "may": 106000, "jun": 80000}
wages7 = {"feb": 10000, "mar": 12000, "apr": 8000, "may": 10000, "jun": 8000}
misc7 = {"feb": 7000, "mar": 8000, "apr": 6000, "may": 12000, "jun": 6000}
bal = 5000
want7 = {"apr": 5680, "may": -7084, "jun": -62936}
for m in ("apr", "may", "jun"):
    cash_s = sales7[m] * 0.20 * 0.98               # 20% less 2% discount
    coll = 0.40 * sales7[prev[m]] + 0.40 * sales7[prev2[m]]
    inv = 5000 if m == "apr" else 0
    a = bal + cash_s + coll + inv
    pay = (purch7[prev[m]] + misc7[prev[m]]
           + 0.75 * wages7[m] + 0.25 * wages7[prev[m]]
           + (3000 if m == "apr" else 0)           # rent, quarterly in advance
           + (25000 if m == "jun" else 0))         # advance tax
    closing = a - pay
    eq(f"Q7 {m} cash sales net of discount", cash_s,
       {"apr": 15680, "may": 22736, "jun": 17248}[m])
    eq(f"Q7 {m} collections", coll, {"apr": 100000, "may": 84000, "jun": 78400}[m])
    eq(f"Q7 {m} total A", a, {"apr": 125680, "may": 112416, "jun": 88564}[m])
    eq(f"Q7 {m} total B", pay, {"apr": 120000, "may": 119500, "jun": 151500}[m])
    eq(f"Q7 {m} closing", closing, want7[m])
    bal = closing
eq("Q7 effective cash-sale rate", 0.20 * 0.98, 0.196)
eq("Q7 wages paid in April", 0.75 * 8000 + 0.25 * 12000, 9000)
eq("Q7 wages paid in May", 0.75 * 10000 + 0.25 * 8000, 9500)
eq("Q7 wages paid in June", 0.75 * 8000 + 0.25 * 10000, 8500)
for v in (15680, 22736, 17248, 100000, 84000, 78400, 125680, 112416, 88564,
          120000, 119500, 151500, 5680, 7084, 62936):
    has(f"Q7 {v}", ind(v))

# ============================================================ Q8  production budget
gam = {"apr": 900, "may": 1100, "jun": 1400, "jul": 1800, "aug": 2200, "sep": 2200, "oct": 1800}
dlt = {"apr": 2900, "may": 2900, "jun": 2500, "jul": 2100, "aug": 1700, "sep": 1700, "oct": 1900}
months = ["apr", "may", "jun", "jul", "aug", "sep"]
nxt = {"apr": "may", "may": "jun", "jun": "jul", "jul": "aug", "aug": "sep", "sep": "oct"}
want_g = [1000, 1250, 1600, 2000, 2200, 2000]
want_d = [2900, 2700, 2300, 1900, 1700, 1800]
for tag, sal, want in (("Gamma", gam, want_g), ("Delta", dlt, want_d)):
    opening = 0.50 * sal["apr"]          # March closing = 50% of April sales
    total = 0
    for i, m in enumerate(months):
        closing = 0.50 * sal[nxt[m]]
        prod = sal[m] + closing - opening
        eq(f"Q8 {tag} {m} production", prod, want[i])
        opening = closing
        total += prod
    eq(f"Q8 {tag} half-year total", total, {"Gamma": 10050, "Delta": 13300}[tag])
    # whole-period reconciliation
    tot_sales = sum(sal[m] for m in months)
    eq(f"Q8 {tag} reconciliation",
       tot_sales + 0.50 * sal["oct"] - 0.50 * sal["apr"], total)
g_rate, d_rate = 200000 / 20000, 375000 / 25000
eq("Q8 Gamma other mfg rate", g_rate, 10)
eq("Q8 Delta other mfg rate", d_rate, 15)
g_cost = 10050 * (50 + 20 + g_rate)
d_cost = 13300 * (80 + 30 + d_rate)
eq("Q8 Gamma total cost", g_cost, 804000)
eq("Q8 Gamma cost p.u.", 50 + 20 + g_rate, 80)
eq("Q8 Delta total cost", d_cost, 1662500)
eq("Q8 Delta cost p.u.", 80 + 30 + d_rate, 125)
eq("Q8 grand total", g_cost + d_cost, 2466500)
for v in (10050, 13300, 502500, 201000, 100500, 804000, 1064000, 399000, 199500,
          1662500, 2466500):
    has(f"Q8 {v}", ind(v))

# ============================================================ Q10
for nm, s, o, c, want in [("A", 150000, 14000, 15000, 151000),
                          ("B", 100000, 5000, 14500, 109500),
                          ("C", 70000, 8000, 8000, 70000)]:
    eq(f"Q10 {nm} production", s + c - o, want)
    eq(f"Q10 {nm} prod-sales = stock change", (s + c - o) - s, c - o)
    has(f"Q10 {nm}", ind(want))
eq("Q10 total production", 151000 + 109500 + 70000, 330500)
has("Q10 total", ind(330500))

# ============================================================ Q11  with materials on order
prod11 = 40000 + 7000 - 5000
eq("Q11 budgeted production", prod11, 42000)
for nm, per, o_stock, c_stock, o_ord, c_ord, want_c, want_p in [
        ("A", 3, 12000, 15000, 7000, 8000, 126000, 130000),
        ("B", 4, 20000, 25000, 11000, 10000, 168000, 172000)]:
    cons = prod11 * per
    eq(f"Q11 {nm} consumption", cons, want_c)
    recv = cons + c_stock - o_stock
    ordered = recv + c_ord - o_ord
    eq(f"Q11 {nm} to be procured", ordered, want_p)
    # the same figure via the single 5-term formula
    eq(f"Q11 {nm} 5-term formula agrees",
       cons + c_stock + c_ord - o_stock - o_ord, ordered)
    has(f"Q11 {nm} consumption", ind(want_c))
    has(f"Q11 {nm} procured", ind(want_p))
eq("Q11 A received vs ordered differ", 126000 + 15000 - 12000, 129000)
eq("Q11 B received vs ordered differ", 168000 + 25000 - 20000, 173000)

# ============================================================ Q12
prod12 = 50000 + 14000 - 10000
eq("Q12 budgeted production", prod12, 54000)
for nm, per, o, c, want_c, want_p in [("A", 2, 12000, 13000, 108000, 109000),
                                      ("B", 3, 15000, 16000, 162000, 163000)]:
    cons = prod12 * per
    eq(f"Q12 {nm} consumption", cons, want_c)
    eq(f"Q12 {nm} purchases", cons + c - o, want_p)
    has(f"Q12 {nm} consumption", ind(want_c))
    has(f"Q12 {nm} purchases", ind(want_p))

# ============================================================ Q9  sales budget
# Snow +10% zone B only; Talcum +20% both zones, price 15-1=14; Cold +25,000 zone A only
snow_a, snow_b = 400000, 250000 * 1.10
talc_a, talc_b = 250000 * 1.20, 350000 * 1.20
cold_a, cold_b = 300000 + 25000, 300000
eq("Q9 snow zone A", snow_a, 400000)
eq("Q9 snow zone B", snow_b, 275000)
eq("Q9 talcum zone A", talc_a, 300000)
eq("Q9 talcum zone B", talc_b, 420000)
eq("Q9 cold zone A", cold_a, 325000)
eq("Q9 cold zone B", cold_b, 300000)
eq("Q9 talcum price after bonus cut", 15 - 1, 14)
eq("Q9 snow value", (snow_a + snow_b) * 12, 8100000)
eq("Q9 talcum value", (talc_a + talc_b) * 14, 10080000)
eq("Q9 cold value", (cold_a + cold_b) * 16, 10000000)
gt_units = snow_a + snow_b + talc_a + talc_b + cold_a + cold_b
gt_value = (snow_a + snow_b) * 12 + (talc_a + talc_b) * 14 + (cold_a + cold_b) * 16
eq("Q9 total units", gt_units, 2020000)
eq("Q9 total value", gt_value, 28180000)
eq("Q9 zone A value", snow_a * 12 + talc_a * 14 + cold_a * 16, 14200000)
eq("Q9 zone B value", snow_b * 12 + talc_b * 14 + cold_b * 16, 13980000)
eq("Q9 talcum previous value", 600000 * 15, 9000000)
eq("Q9 talcum value gain", 10080000 - 9000000, 1080000)
eq("Q9 revenue given away on existing units", 600000 * 1, 600000)
for v in (4800000, 3300000, 4200000, 5880000, 5200000, 4800000, 8100000,
          10080000, 10000000, 28180000, 2020000, 1080000):
    has(f"Q9 {v}", ind(v))

# ============================================================ Q14  master budget
sales14 = 4000000 + 6000000
eq("Q14 total sales", sales14, 10000000)
dm14 = 0.40 * sales14
dw14 = 15 * 12000 * 12
wm14 = 20000 * 12
fm14 = 15000 * 12
ss14 = 0.025 * sales14
misc14 = 0.10 * dw14
eq("Q14 direct materials", dm14, 4000000)
eq("Q14 direct wages", dw14, 2160000)
eq("Q14 works manager", wm14, 240000)
eq("Q14 foreman", fm14, 180000)
eq("Q14 stores and spares", ss14, 250000)
eq("Q14 miscellaneous (10% of WAGES)", misc14, 216000)
fac14 = wm14 + fm14 + ss14 + 126000 + 50000 + 80000 + misc14
eq("Q14 total factory overheads", fac14, 1142000)
tot14 = dm14 + dw14 + fac14 + 140000
eq("Q14 total cost", tot14, 7442000)
eq("Q14 budgeted profit", sales14 - tot14, 2558000)
eq("Q14 profit % of sales", (sales14 - tot14) / sales14 * 100, 25.58)
eq("Q14 prime cost", dm14 + dw14, 6160000)
for v in (10000000, 4000000, 2160000, 240000, 180000, 250000, 126000, 216000,
          1142000, 7442000, 2558000):
    has(f"Q14 {v}", ind(v))
has("Q14 profit pct", "25.58")

# ============================================================ Q15  full chain
parts_price = {"D": 45, "E": 15, "F": 15, "G": 5}
bom = {"A": {"D": 1, "E": 10, "F": 2, "G": 8},
       "B": {"D": 1, "E": 2, "F": 14, "G": 10},
       "C": {"D": 1, "E": 6, "F": 10, "G": 2}}
hours = {"A": (6, 8), "B": (4, 6), "C": (3, 6)}       # (skilled, unskilled)
voh = {"A": 9, "B": 11, "C": 7}
sp = {"A": 450, "B": 550, "C": 650}
ratio = {"A": 1, "B": 2, "C": 4}
rm = {p: sum(bom[p][k] * parts_price[k] for k in parts_price) for p in bom}
eq("Q15 RM cost A", rm["A"], 265)
eq("Q15 RM cost B", rm["B"], 335)
eq("Q15 RM cost C", rm["C"], 295)
lc = {p: hours[p][0] * 6 + hours[p][1] * 5 for p in hours}
eq("Q15 labour cost A", lc["A"], 76)
eq("Q15 labour cost B", lc["B"], 54)
eq("Q15 labour cost C", lc["C"], 48)
vcu = {p: rm[p] + lc[p] + voh[p] for p in rm}
eq("Q15 variable cost A", vcu["A"], 350)
eq("Q15 variable cost B", vcu["B"], 400)
eq("Q15 variable cost C", vcu["C"], 350)
con = {p: sp[p] - vcu[p] for p in sp}
eq("Q15 contribution A", con["A"], 100)
eq("Q15 contribution B", con["B"], 150)
eq("Q15 contribution C", con["C"], 300)
coeff = sum(con[p] * ratio[p] for p in con)
eq("Q15 contribution coefficient", coeff, 1600)
fixed15 = 1575000 + 580000 + 845000
eq("Q15 monthly fixed overhead", fixed15, 3000000)
profit_m = 12000000 / 12
eq("Q15 monthly profit target", profit_m, 1000000)
x = (fixed15 + profit_m) / coeff
eq("Q15 x solved", x, 2500)
qty = {p: ratio[p] * x for p in ratio}
eq("Q15 sales qty A", qty["A"], 2500)
eq("Q15 sales qty B", qty["B"], 5000)
eq("Q15 sales qty C", qty["C"], 10000)
sales_val = sum(qty[p] * sp[p] for p in qty)
eq("Q15 sales value A", qty["A"] * sp["A"], 1125000)
eq("Q15 sales value B", qty["B"] * sp["B"], 2750000)
eq("Q15 sales value C", qty["C"] * sp["C"], 6500000)
eq("Q15 total sales value", sales_val, 10375000)
op_p = {"A": 500, "B": 1000, "C": 3000}
prod15 = {p: qty[p] + 0.90 * op_p[p] - op_p[p] for p in qty}
eq("Q15 production A", prod15["A"], 2450)
eq("Q15 production B", prod15["B"], 4900)
eq("Q15 production C", prod15["C"], 9700)
usage = {k: sum(prod15[p] * bom[p][k] for p in prod15) for k in parts_price}
eq("Q15 usage D", usage["D"], 17050)
eq("Q15 usage E", usage["E"], 92500)
eq("Q15 usage F", usage["F"], 170500)
eq("Q15 usage G", usage["G"], 88000)
eq("Q15 D usage = total units produced", usage["D"], sum(prod15.values()))
op_parts = {"D": 1500, "E": 1000, "F": 20000, "G": 10000}
purch15 = {k: usage[k] + 0.90 * op_parts[k] - op_parts[k] for k in usage}
eq("Q15 purchase D", purch15["D"], 16900)
eq("Q15 purchase E", purch15["E"], 92400)
eq("Q15 purchase F", purch15["F"], 168500)
eq("Q15 purchase G", purch15["G"], 87000)
pval = {k: purch15[k] * parts_price[k] for k in purch15}
eq("Q15 purchase value D", pval["D"], 760500)
eq("Q15 purchase value E", pval["E"], 1386000)
eq("Q15 purchase value F", pval["F"], 2527500)
eq("Q15 purchase value G", pval["G"], 435000)
eq("Q15 total purchase value", sum(pval.values()), 5109000)
sk = sum(prod15[p] * hours[p][0] for p in prod15)
un = sum(prod15[p] * hours[p][1] for p in prod15)
eq("Q15 skilled hours", sk, 63400)
eq("Q15 unskilled hours", un, 107200)
eq("Q15 skilled wages", sk * 6, 380400)
eq("Q15 unskilled wages", un * 5, 536000)
eq("Q15 total wages", sk * 6 + un * 5, 916400)
eq("Q15 hours per worker per month", 8 * 25, 200)
eq("Q15 skilled workers", sk / 200, 317)
eq("Q15 unskilled workers", un / 200, 536)
eq("Q15 total workers", sk / 200 + un / 200, 853)
vc_sales = sum(qty[p] * vcu[p] for p in qty)
eq("Q15 variable cost of sales", vc_sales, 6375000)
contrib15 = sales_val - vc_sales
eq("Q15 total contribution", contrib15, 4000000)
eq("Q15 contribution = 1600x", contrib15, coeff * x)
eq("Q15 monthly profit", contrib15 - fixed15, 1000000)
eq("Q15 annual profit reproduced", (contrib15 - fixed15) * 12, 12000000)
eq("Q15 product A loss", qty["A"] * con["A"] - 1575000, -1325000)
eq("Q15 product B profit", qty["B"] * con["B"] - 580000, 170000)
eq("Q15 product C profit", qty["C"] * con["C"] - 845000, 2155000)
for v in (265, 335, 295, 1125000, 2750000, 6500000, 10375000, 2450, 4900, 9700,
          17050, 92500, 170500, 88000, 16900, 92400, 168500, 87000,
          760500, 1386000, 2527500, 435000, 5109000, 63400, 107200,
          380400, 536000, 916400, 4000000, 3000000, 1000000, 12000000,
          1325000, 170000, 2155000, 6375000):
    has(f"Q15 {v}", ind(v))
for s in ("317", "536", "853", "1,600", "2,500"):
    has(f"Q15 {s}", s)

# ---------------------------------------------------------------- report
print(f"Module 5 checker: {checks[0]} assertions")
if fails:
    print(f"\n*** {len(fails)} FAILURES ***")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("ALL MODULE 5 ASSERTIONS PASS")
