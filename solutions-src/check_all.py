#!/usr/bin/env python3
"""
Run every verification that ships with this book and report the total.

  python3 check_all.py
"""
import subprocess, sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ["check_m3.py", "check_m4.py", "check_m5.py", "check_m6.py",
           "check_structural.py"]

total, bad = 0, []
print("=" * 62)
for s in SCRIPTS:
    p = subprocess.run([sys.executable, os.path.join(HERE, s)],
                       capture_output=True, text=True)
    out = p.stdout + p.stderr
    m = re.search(r'(\d+)\s+(?:assertions|structural checks)', out)
    n = int(m.group(1)) if m else 0
    total += n
    ok = p.returncode == 0
    print(f"  {s:22s} {n:5d} checks   {'PASS' if ok else 'FAIL'}")
    if not ok:
        bad.append((s, out))
print("=" * 62)
print(f"  TOTAL {total} checks across {len(SCRIPTS)} verification scripts")
print("=" * 62)
if bad:
    for s, out in bad:
        print(f"\n----- {s} -----\n{out}")
    sys.exit(1)
print("ALL VERIFICATIONS PASS")
