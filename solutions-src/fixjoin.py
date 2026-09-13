"""
Fix the Python 3.9 gotcha where a continued implicit-concatenation expression
loses its '+' across a line break, e.g.

    'some text '
    R + '40,000'          ->   'some text ' +
                               R + '40,000'

Usage: python3 fixjoin.py <file.py>
"""
import re, ast, sys

P = sys.argv[1]
lines = open(P).read().split('\n')

fixed = 0
for i in range(len(lines) - 1):
    cur = lines[i].rstrip()
    nxt = lines[i + 1].strip()
    # current line ends in a closing quote, next line starts with a bare
    # single-capital symbol variable followed by '+'
    if re.search(r"['\"]$", cur) and re.match(r"^[A-Z]{1,4}\s*\+", nxt):
        lines[i] = cur + " +"
        fixed += 1

open(P, 'w').write('\n'.join(lines))
print(f"{P}: joined {fixed} line(s)")

try:
    ast.parse(open(P).read())
    print("SYNTAX OK")
except SyntaxError as e:
    print(f"STILL BROKEN at line {e.lineno}: {e.text}")
    sys.exit(1)
