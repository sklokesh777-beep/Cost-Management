"""
Independent arithmetic verification for Module 6 (Standard Costing).

content_m6 computes its variances with shared "engines".  This checker does NOT
use them: it recomputes every variance from the workbook data with plain
inline arithmetic, then (a) compares against the engine output and (b) asserts
the figure actually appears in the rendered HTML.  It also proves every
reconciliation identity closes exactly.
"""
import re, sys, os
sys.path.insert(0, '/projects/sandbox/work/cmbook')
os.chdir('/projects/sandbox/work/cmbook')

import content_m6 as M

html = M.build()
plain = re.sub(r'<[^>]+>', ' ', html)
plain = plain.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&#8377;', '')
plain = plain.replace('&minus;', '-').replace('&times;', 'x').replace('&mdash;', '-')
plain = re.sub(r'\s+', ' ', plain)

fails, checks = [], [0]
TOL = 0.005


def eq(label, got, want, tol=TOL):
    checks[0] += 1
    if abs(got - want) > tol:
        fails.append(f"{label}: computed {got} != expected {want}")


def has(label, s):
    checks[0] += 1
    if s not in plain:
        fails.append(f"{label}: expected substring {s!r} NOT FOUND")


def ind(x, dp=0):
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


def tagged(v, dp=None):
    """The rendered form '12,345 (A)' so the (F)/(A) sign is verified too."""
    if dp is None:
        dp = 0 if abs(v - round(v)) < TOL else 2
    return f"{ind(v, dp)} ({'F' if v > 0 else 'A'})"


# =====================================================================
# MATERIAL  -  independent recomputation
# =====================================================================
def mat_check(tag, mats, std_out, act_out, want, engine_kwargs=None):
    """
    mats: list of (name, sq_std, sp, aq, ap)
    want: dict with mcv/mpv/muv/mmv/myv expected values
    """
    k = act_out / std_out
    tot_sq_std = sum(m[1] for m in mats)
    tot_aq = sum(m[3] for m in mats)
    mcv = mpv = muv = mmv = myv = 0.0
    tot_rsq = 0.0
    for n, sqs, sp, aq, ap in mats:
        sq = sqs * k
        rsq = tot_aq * sqs / tot_sq_std
        tot_rsq += rsq
        mcv += sq * sp - aq * ap
        mpv += aq * (sp - ap)
        muv += sp * (sq - aq)
        mmv += sp * (rsq - aq)
        myv += sp * (sq - rsq)
    # structural invariants
    eq(f"{tag} RSQ total = AQ total", tot_rsq, tot_aq)
    eq(f"{tag} MCV = MPV + MUV", mpv + muv, mcv)
    eq(f"{tag} MUV = MMV + MYV", mmv + myv, muv)
    # alternative rounding-free yield route
    std_cost_per_out = sum(m[1] * m[2] for m in mats) / std_out
    std_yield = tot_aq * std_out / tot_sq_std
    eq(f"{tag} MYV via output route", std_cost_per_out * (act_out - std_yield), myv)
    # expected values
    for key, val in want.items():
        eq(f"{tag} {key}", {"mcv": mcv, "mpv": mpv, "muv": muv,
                            "mmv": mmv, "myv": myv}[key], val)
    # cross-check the engine agrees with this independent arithmetic
    e = M.material_engine([dict(n=n, sq=s, sp=p, aq=a, ap=ap) for n, s, p, a, ap in mats],
                          std_out, act_out)
    for key, val in (("mcv", mcv), ("mpv", mpv), ("muv", muv), ("mmv", mmv), ("myv", myv)):
        eq(f"{tag} engine {key} matches independent", e[key], val)
    # and that each tagged figure is present in the document
    for key, val in (("MCV", mcv), ("MPV", mpv), ("MUV", muv), ("MMV", mmv), ("MYV", myv)):
        has(f"{tag} {key} rendered", tagged(val))
    return dict(mcv=mcv, mpv=mpv, muv=muv, mmv=mmv, myv=myv)


# Q1 : 450/400/250 @ 20/40/60 ; actual 10000/8500/4500 @ 19/42/65 ; 1,100->1,000, out 20,000
mat_check("Q1", [("P", 450, 20, 10000, 19), ("Q", 400, 40, 8500, 42), ("R", 250, 60, 4500, 65)],
          1000, 20000,
          dict(mcv=-39500, mpv=-29500, muv=-10000,
               mmv=26363.6363636, myv=-36363.6363636))

# Q2 : 125 kg input -> 100 kg output ; std mix 50/30/20 ; actual mix 60/20/20 of 7,000 kg
mat_check("Q2", [("X", 62.5, 40, 4200, 42), ("Y", 37.5, 20, 1400, 16), ("Z", 25, 10, 1400, 12)],
          100, 5600,
          dict(mcv=-19600, mpv=-5600, muv=-14000, mmv=-14000, myv=0))

# Q3 : 40% A @20 + 60% B @30 of a 100 t batch, 10% loss -> 90 t out ; actual 180/220, out 364
mat_check("Q3", [("A", 40, 20, 180, 18), ("B", 60, 30, 220, 34)], 90, 364,
          dict(mcv=-204.4444444, mpv=-520, muv=315.5555556,
               mmv=200, myv=115.5555556))

# Q4 : 75% A @2 + 25% B @10 of 100 kg, yield 90% -> 90 kg ; actual 2200/800, out 2850
mat_check("Q4", [("A", 75, 2, 2200, 4650 / 2200), ("B", 25, 10, 800, 7850 / 800)], 90, 2850,
          dict(mcv=166.6666667, mpv=-100, muv=266.6666667,
               mmv=-400, myv=666.6666667))

# Q5 : no loss, no separate output -> k = 1
mat_check("Q5", [("Zee", 3500, 10, 3700, 12), ("Wee", 1500, 21, 1650, 20),
                 ("Tee", 1000, 33, 1250, 36)], 6000, 6000,
          dict(mcv=-22900, mpv=-9500, muv=-13400, mmv=-3450, myv=-9950))

# Q6 : 45/25/30 of 100 kg @ 6/4.50/9.50, 10% loss -> 90 kg ; actual 4200/1700/2600, out 7425
mat_check("Q6", [("X", 45, 6.00, 4200, 6.50), ("Y", 25, 4.50, 1700, 4.25),
                 ("Z", 30, 9.50, 2600, 9.75)], 90, 7425,
          dict(mcv=-4806.25, mpv=-2325, muv=-2481.25, mmv=-812.50, myv=-1668.75))

# Q7 : 60 A @10 + 140 B @2 -> 180 kg out ; actual output 144 at 80% yield -> input 180, B=108, A=72
eq("Q7 actual input from yield", 144 / 0.80, 180)
eq("Q7 actual quantity of A", 180 - 108, 72)
mat_check("Q7", [("A", 60, 10, 72, 12), ("B", 140, 2, 108, 8)], 180, 144,
          dict(mcv=-1024, mpv=-792, muv=-232, mmv=-144, myv=-88))

# a few key rendered quantities
has("Q1 SQ P", "9,000")
has("Q1 RSQ P", "9,409.09")
has("Q2 total input", "7,000")
has("Q3 SQ A", "161.78")
has("Q4 SQ A", "2,375")
has("Q6 scale factor", "82.5")
has("Q7 deduced A", "72")


# =====================================================================
# LABOUR  -  independent recomputation
# =====================================================================
def lab_check(tag, grades, std_out, act_out, idle_pw, want):
    """grades: list of (name, sw, sr, aw, ar, hrs)"""
    tot_sh_std = sum(g[1] * g[5] for g in grades)
    tot_ah = sum(g[3] * g[5] for g in grades)
    tot_idle = sum(g[3] * idle_pw for g in grades)
    tot_worked = tot_ah - tot_idle
    k = act_out / std_out
    lcv = lrv = lev = lmv = lyv = litv = 0.0
    for n, sw, sr, aw, ar, hrs in grades:
        sh_std = sw * hrs
        prop = sh_std / tot_sh_std
        sh = sh_std * k
        ah = aw * hrs
        rsh_in = tot_ah * prop
        rsh_wk = tot_worked * prop
        idle_std = tot_idle * prop
        lcv += sh * sr - ah * ar
        lrv += ah * (sr - ar)
        lev += sr * (sh - ah)
        lmv += sr * (rsh_in - ah)
        lyv += sr * (sh - rsh_wk)
        litv += -idle_std * sr
    eq(f"{tag} LCV = LRV + LEV", lrv + lev, lcv)
    eq(f"{tag} LEV = LMV + LYV + LITV", lmv + lyv + litv, lev)
    eq(f"{tag} idle time is adverse", 1 if litv <= 0 else 0, 1)
    eq(f"{tag} hours worked = paid - idle", tot_worked, tot_ah - tot_idle)
    for key, val in want.items():
        eq(f"{tag} {key}", {"lcv": lcv, "lrv": lrv, "lev": lev,
                            "lmv": lmv, "lyv": lyv, "litv": litv}[key], val)
    e = M.labour_engine([dict(n=n, sw=sw, sr=sr, aw=aw, ar=ar, hrs=h)
                         for n, sw, sr, aw, ar, h in grades], std_out, act_out, idle_pw)
    for key, val in (("lcv", lcv), ("lrv", lrv), ("lev", lev),
                     ("lmv", lmv), ("lyv", lyv), ("litv", litv)):
        eq(f"{tag} engine {key} matches independent", e[key], val)
    for key, val in (("LCV", lcv), ("LRV", lrv), ("LEV", lev),
                     ("LMV", lmv), ("LYV", lyv), ("LITV", litv)):
        has(f"{tag} {key} rendered", tagged(val))


# Q8 : 10 men @.625 / 5 women @.400 / 5 boys @.350 ; 40 hr week, std out 1,000
#      actual 13/4/3 @ .600/.425/.325 ; 2 idle hours each ; output 960
lab_check("Q8", [("Men", 10, 0.625, 13, 0.600, 40),
                 ("Women", 5, 0.400, 4, 0.425, 40),
                 ("Boys", 5, 0.350, 3, 0.325, 40)], 1000, 960, 2,
          dict(lcv=-35, lrv=12, lev=-47, lmv=-31, lyv=4, litv=-20))
eq("Q8 total idle hours", (13 + 4 + 3) * 2, 40)
eq("Q8 SH for actual output", (10 + 5 + 5) * 40 * 960 / 1000, 768)
has("Q8 idle hours", "40")
has("Q8 SH", "768")

# Q9 : 2 skilled @20 / 4 semi @12 / 4 unskilled @8 ; 200 hrs ; std 4 units/hr -> 800 units
#      actual 2/3/5 @ 20/14/10 ; 12 idle hours each ; output 810
lab_check("Q9", [("Skilled", 2, 20, 2, 20, 200),
                 ("Semi-skilled", 4, 12, 3, 14, 200),
                 ("Unskilled", 4, 8, 5, 10, 200)], 800, 810, 12,
          dict(lcv=-2100, lrv=-3200, lev=1100, lmv=800, lyv=1740, litv=-1440))
eq("Q9 standard output", 4 * 200, 800)
eq("Q9 SH for actual output", 10 * 200 * 810 / 800, 2025)
eq("Q9 total idle hours", 10 * 12, 120)
has("Q9 SH", "2,025")
has("Q9 idle hours", "120")

# Q10 : 30/10/10 @ 5/3/2 ; 200 hrs ; std 50 units/hr -> 10,000 units
#       actual 24/15/12 @ 6/2.50/2 ; 15 idle hours each ; output 9,600
lab_check("Q10", [("Skilled", 30, 5.0, 24, 6.0, 200),
                  ("Semi-skilled", 10, 3.0, 15, 2.5, 200),
                  ("Unskilled", 10, 2.0, 12, 2.0, 200)], 10000, 9600, 15,
          dict(lcv=-2700, lrv=-3300, lev=600, lmv=3000,
               lyv=660, litv=-3060))
eq("Q10 standard output", 50 * 200, 10000)
eq("Q10 SH for actual output", 50 * 200 * 9600 / 10000, 9600)
eq("Q10 AH paid", (24 + 15 + 12) * 200, 10200)
eq("Q10 total idle hours", 51 * 15, 765)
has("Q10 AH", "10,200")
has("Q10 idle hours", "765")


# =====================================================================
# VARIABLE OVERHEAD  -  independent recomputation
# =====================================================================
def voh_check(tag, bud_u, bud_voh, hpu, act_u, act_voh, act_h, idle, want):
    bh = bud_u * hpu
    sr = bud_voh / bh
    sh = act_u * hpu
    worked = act_h - idle
    sc = sh * sr
    vocv = sc - act_voh
    exp = act_h * sr - act_voh
    idlev = -idle * sr
    eff = sr * (sh - worked)
    eq(f"{tag} VOCV = exp + idle + eff", exp + idlev + eff, vocv)
    for key, val in want.items():
        eq(f"{tag} {key}", {"sr": sr, "sh": sh, "sc": sc, "vocv": vocv,
                            "exp": exp, "idlev": idlev, "eff": eff}[key], val)
    e = M.voh_engine(bud_u, bud_voh, hpu, act_u, act_voh, act_h, idle)
    for key, val in (("vocv", vocv), ("exp", exp), ("idlev", idlev), ("eff", eff)):
        eq(f"{tag} engine {key} matches independent", e[key], val)
    for key, val in (("VOCV", vocv), ("exp", exp), ("eff", eff)):
        has(f"{tag} {key} rendered", tagged(val))
    if idle:
        has(f"{tag} idle rendered", tagged(idlev))


voh_check("Q11", 600, 15600, 20, 500, 14000, 9000, 0,
          dict(sr=1.30, sh=10000, sc=13000, vocv=-1000, exp=-2300, eff=1300))
voh_check("Q12", 300, 7800, 20, 250, 7000, 4500, 300,
          dict(sr=1.30, sh=5000, sc=6500, vocv=-500, exp=-1150, idlev=-390, eff=1040))
voh_check("Q13", 400, 10000, 8000 / 400, 360, 9150, 7000, 0,
          dict(sr=1.25, sh=7200, sc=9000, vocv=-150, exp=-400, eff=250))
eq("Q13 std hours per unit derived", 8000 / 400, 20)


# =====================================================================
# FIXED OVERHEAD  -  independent recomputation
# =====================================================================
def foh_check(tag, bud_foh, bh, bud_u, act_foh, ah, act_u, bud_days, act_days, want):
    sr = bud_foh / bh
    hpu = bh / bud_u
    sh = act_u * hpu
    sc = sh * sr
    focv = sc - act_foh
    exp = bud_foh - act_foh
    vol = sr * (sh - bh)
    eff = sr * (sh - ah)
    if bud_days:
        rsh = bh * act_days / bud_days
        cal = sr * (rsh - bh)
        cap = sr * (ah - rsh)
        eq(f"{tag} vol = cal + cap + eff", cal + cap + eff, vol)
    else:
        rsh, cal = None, None
        cap = sr * (ah - bh)
        eq(f"{tag} vol = cap + eff", cap + eff, vol)
    eq(f"{tag} FOCV = exp + vol", exp + vol, focv)
    got = dict(sr=sr, sh=sh, sc=sc, focv=focv, exp=exp, vol=vol,
               cap=cap, eff=eff, rsh=rsh, cal=cal)
    for key, val in want.items():
        eq(f"{tag} {key}", got[key], val)
    e = M.foh_engine(bud_foh, bh, bud_u, act_foh, ah, act_u, bud_days, act_days)
    for key in ("focv", "exp", "vol", "cap", "eff"):
        eq(f"{tag} engine {key} matches independent", e[key], got[key])
    if bud_days:
        eq(f"{tag} engine cal matches independent", e["cal"], cal)
    for key in ("focv", "exp", "vol", "cap", "eff"):
        has(f"{tag} {key} rendered", tagged(got[key]))
    if cal is not None:
        has(f"{tag} cal rendered", tagged(cal))


# Q14 : 20 days x 8,000 hrs, 1.0 unit/hr, FOH 1,60,000 ; actual 22 x 8,400, 0.9 unit/hr, 1,68,000
eq("Q14 budgeted hours", 20 * 8000, 160000)
eq("Q14 actual hours", 22 * 8400, 184800)
eq("Q14 budgeted output", 160000 * 1.0, 160000)
eq("Q14 actual output", 184800 * 0.9, 166320)
foh_check("Q14", 160000, 160000, 160000, 168000, 184800, 166320, 20, 22,
          dict(sr=1.0, sh=166320, sc=166320, focv=-1680, exp=-8000, vol=6320,
               rsh=176000, cal=16000, cap=8800, eff=-18480))

# Q15 : FOH 10,000 bud / 10,200 actual ; 5,000 units bud / 5,200 actual ; 4 hrs/unit ; 20,100 hrs
foh_check("Q15", 10000, 20000, 5000, 10200, 20100, 5200, None, None,
          dict(sr=0.50, sh=20800, sc=10400, focv=200, exp=-200, vol=400,
               cap=50, eff=350))


# =====================================================================
# SALES  -  independent recomputation
# =====================================================================
def sales_check(tag, prods, margin, want):
    """prods: list of (name, bq, sp, aq, ap, sc_or_None)"""
    tot_bq = sum(p[1] for p in prods)
    tot_aq = sum(p[3] for p in prods)
    bud = act = price = mix = qty = vol = 0.0
    tot_rbq = 0.0
    for n, bq, sp, aq, ap, sc in prods:
        rbq = tot_aq * bq / tot_bq
        tot_rbq += rbq
        if margin:
            sm, am = sp - sc, ap - sc
            base = sm
            bud += bq * sm
            act += aq * am
            price += aq * (am - sm)
        else:
            base = sp
            bud += bq * sp
            act += aq * ap
            price += aq * (ap - sp)
        mix += base * (aq - rbq)
        qty += base * (rbq - bq)
        vol += base * (aq - bq)
    total = act - bud
    eq(f"{tag} RBQ total = AQ total", tot_rbq, tot_aq)
    eq(f"{tag} total = price + volume", price + vol, total)
    eq(f"{tag} volume = mix + quantity", mix + qty, vol)
    got = dict(bud=bud, act=act, total=total, price=price, mix=mix, qty=qty, vol=vol)
    for key, val in want.items():
        eq(f"{tag} {key}", got[key], val)
    e = M.sales_engine([dict(n=n, bq=bq, sp=sp, aq=aq, ap=ap, sc=sc)
                        for n, bq, sp, aq, ap, sc in prods], margin=margin)
    for key, ek in (("total", "total"), ("price", "price"), ("mix", "mix"),
                    ("qty", "qty"), ("vol", "vol")):
        eq(f"{tag} engine {key} matches independent", e[ek], got[key])
    for key in ("total", "price", "vol"):
        has(f"{tag} {key} rendered", tagged(got[key]))


# Q16 : value basis
sales_check("Q16", [("X", 500, 5, 500, 5.00, None),
                    ("Y", 400, 6, 600, 6.25, None),
                    ("Z", 300, 7, 400, 6.75, None)], False,
            dict(bud=7000, act=8950, total=1950, price=50, mix=150, qty=1750, vol=1900))
has("Q16 RBQ X", "625")
has("Q16 mix", tagged(150))
has("Q16 qty", tagged(1750))

# Q17 : margin basis
sales_check("Q17", [("A", 500, 2.00, 560, 1.95, 1.75),
                    ("B", 700, 1.50, 710, 1.40, 1.30)], True,
            dict(bud=265, act=183, total=-82, price=-99,
                 mix=1.5416666667, qty=15.4583333333, vol=17))
has("Q17 RBQ A", "529.17")
has("Q17 std margins", "0.25")
# the headline contradiction: volume up, margin down
eq("Q17 units rose", 1270 - 1200, 70)
eq("Q17 revenue rose", (560 * 1.95 + 710 * 1.40) - (500 * 2.00 + 700 * 1.50), 36.0)
eq("Q17 but margin FELL", 1 if (183 - 265) < 0 else 0, 1)


# =====================================================================
# regression: rs() must round BEFORE splitting off the decimals, or binary
# floating-point artefacts leak a wrong integer part (183.0 rendered "182.00")
# =====================================================================
from build import rs, money
for v, dp, want in [(182.9999999999999, 2, "183.00"),
                    (183, 2, "183.00"),
                    (99.999, 2, "100.00"),
                    (1234567.891, 2, "12,34,567.89"),
                    (2466500, 0, "24,66,500"),
                    (0.5, 2, "0.50")]:
    checks[0] += 1
    got = rs(v, dp)
    if got != want:
        fails.append(f"rs({v!r}, {dp}) gave {got!r}, expected {want!r}")
# and the figure that exposed the bug must now render correctly
has("Q17 actual total margin renders as 183.00", "183.00")
has("Q17 budgeted total margin renders as 265.00", "265.00")


# =====================================================================
# global sanity: every problem heading is present
# =====================================================================
for i in range(1, 18):
    has(f"Q{i} heading present", f"Q{i} ")

# ---------------------------------------------------------------- report
print(f"Module 6 checker: {checks[0]} assertions")
if fails:
    print(f"\n*** {len(fails)} FAILURES ***")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("ALL MODULE 6 ASSERTIONS PASS")
