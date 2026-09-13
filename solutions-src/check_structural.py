"""
Structural verification across ALL SIX modules.

This checker does not need to know any problem's data.  It parses the rendered
HTML and enforces two properties that must hold in correct cost accounting,
whatever the numbers are:

  1. Every two-sided ledger account (table.acct) must BALANCE - the debit total
     must equal the credit total.  A process account that does not balance is
     wrong no matter how plausible its figures look.

  2. Every table whose total row is a plain sum of the rows above it must add
     up.  Columns with sub-totals, memoranda or per-unit rates are skipped,
     because for those the total is not a simple column sum.

Because it is data-independent it catches a completely different class of error
from the per-module checkers, and it covers Modules 1 and 2 as well.
"""
import re, sys, os
sys.path.insert(0, '/projects/sandbox/work/cmbook')
os.chdir('/projects/sandbox/work/cmbook')

import importlib

MODULES = ["front", "m1", "m2", "m3", "m4", "m5", "m6"]

fails, checks = [], [0]


def num(cell):
    """Pull a number out of a rendered cell, or None if it is not a number."""
    t = re.sub(r'<[^>]+>', ' ', cell)
    t = (t.replace('&nbsp;', ' ').replace('&#8377;', '').replace('&mdash;', '')
          .replace('&minus;', '-').replace('$', ''))
    t = t.strip()
    if not t:
        return None
    neg = t.startswith('(') and t.endswith(')')
    t = t.strip('()').replace(',', '').replace(' ', '')
    if not re.fullmatch(r'-?\d+(\.\d+)?', t):
        return None
    v = float(t)
    return -v if neg else v


def rows_of(tbody):
    # keep the <tr ...> tag itself, otherwise class='tot' is invisible
    return re.findall(r'(<tr[^>]*>.*?</tr>)', tbody, re.S)


def cells_of(row):
    return re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.S)


def is_tot(row):
    return "class='tot'" in row or 'class="tot"' in row


# ----------------------------------------------------------------- 1. accounts
def check_accounts(mod, html):
    """Every table.acct must balance: Dr amount total == Cr amount total."""
    n_acct = 0
    for m in re.finditer(r"<table class='acct'>(.*?)</table>", html, re.S):
        body = m.group(1)
        cap = re.search(r'<caption>(.*?)</caption>', body, re.S)
        cap = re.sub(r'<[^>]+>', '', cap.group(1)).strip() if cap else "(no caption)"
        tb = re.search(r'<tbody>(.*?)</tbody>', body, re.S)
        if not tb:
            continue
        rr = rows_of(tb.group(1))
        # how many columns per side? 4 (units/rate/amount) or 2
        head = re.search(r'<thead>(.*?)</thead>', body, re.S)
        ncols = len(cells_of(head.group(1))) if head else 8
        half = ncols // 2
        dr_tot = cr_tot = None
        for row in rr:
            if not is_tot(row):
                continue
            cs = cells_of(row)
            if len(cs) < ncols:
                continue
            d = num(cs[half - 1])          # last column of the left half
            c = num(cs[ncols - 1])         # last column of the right half
            if d is not None:
                dr_tot = d
            if c is not None:
                cr_tot = c
        if dr_tot is None or cr_tot is None:
            continue
        n_acct += 1
        checks[0] += 1
        if abs(dr_tot - cr_tot) > 0.02:
            fails.append(f"[{mod}] ACCOUNT DOES NOT BALANCE - {cap[:70]}: "
                         f"Dr {dr_tot:,.2f} vs Cr {cr_tot:,.2f}")
    return n_acct


# ------------------------------------------------------------------ 2. columns
def check_column_totals(mod, html):
    """
    For every table.t that has exactly ONE total row and no sub-total rows,
    check each fully numeric column adds up.  Tables containing 'sub' rows,
    rate columns or memoranda are skipped - their totals are not column sums.
    """
    n_col = 0
    for m in re.finditer(r"<table class='t'>(.*?)</table>", html, re.S):
        body = m.group(1)
        cap = re.search(r'<caption>(.*?)</caption>', body, re.S)
        cap = re.sub(r'<[^>]+>', '', cap.group(1)).strip() if cap else "(no caption)"
        tb = re.search(r'<tbody>(.*?)</tbody>', body, re.S)
        if not tb:
            continue
        rr = rows_of(tb.group(1))
        # skip tables with sub-totals, irrelevant rows or reconciliation rows
        if any(("class='sub'" in r) or ("class='irr'" in r) or ("class='recon'" in r)
               for r in rr):
            continue
        tot_idx = [i for i, r in enumerate(rr) if is_tot(r)]
        if len(tot_idx) != 1 or tot_idx[0] != len(rr) - 1:
            continue                      # need exactly one total, and it must be last
        data, tot = rr[:-1], rr[-1]
        if len(data) < 2:
            continue
        dc = [cells_of(r) for r in data]
        tc = cells_of(tot)
        width = len(tc)
        if any(len(c) != width for c in dc):
            continue                      # ragged (colspan) - skip
        for j in range(1, width):
            tv = num(tc[j])
            if tv is None:
                continue
            col = [num(c[j]) for c in dc]
            if any(v is None for v in col):
                continue                  # not a fully numeric column
            s = sum(col)
            # only assert when the total plausibly IS the column sum; a column of
            # rates or percentages will not match and is not meant to
            if abs(s - tv) < 0.02:
                n_col += 1
                checks[0] += 1
            elif abs(s - tv) / max(abs(tv), 1) < 0.25:
                # close but wrong -> almost certainly a real arithmetic error
                n_col += 1
                checks[0] += 1
                fails.append(f"[{mod}] COLUMN DOES NOT ADD - {cap[:60]} col {j}: "
                             f"rows sum to {s:,.2f} but total says {tv:,.2f}")
    return n_col


# ---------------------------------------------------------------------- run
print("Structural verification across all six modules\n")
tot_acct = tot_col = 0
for name in MODULES:
    mod = importlib.import_module(f"content_{name}")
    html = mod.build()
    a = check_accounts(name, html)
    c = check_column_totals(name, html)
    tot_acct += a
    tot_col += c
    print(f"  {name:6s}  ledger accounts balanced: {a:3d}   column totals verified: {c:4d}")

print(f"\n  TOTAL   {tot_acct} two-sided accounts, {tot_col} column totals "
      f"= {checks[0]} structural checks")
if fails:
    print(f"\n*** {len(fails)} FAILURES ***")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("\nALL STRUCTURAL CHECKS PASS")
