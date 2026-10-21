"""Check final LaTeX logs; Python standard library only.

Usage: python scripts/check-build.py build/*.log
Pass final logs after latexmk has finished all reruns.
"""
from pathlib import Path
import glob
import re
import sys

patterns = {
    "TeX error": r"^! |(?:LaTeX|Package \S+) Error:",
    "missing glyph": r"Missing character:",
    "overflow": r"Overfull \\[hv]box",
    "undefined reference": r"(?:Reference|Citation) .+ undefined|There were undefined (?:references|citations)",
    "duplicate label": r"multiply defined",
    "rerun needed": r"Label\(s\) may have changed|Rerun to get cross-references right",
}

files = sorted({Path(p) for arg in sys.argv[1:] for p in glob.glob(arg)})
if not files:
    raise SystemExit("No log files found. Build the documents first.")
failed = False
for path in files:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    count = 0
    for number, line in enumerate(lines, 1):
        for category, pattern in patterns.items():
            if re.search(pattern, line, re.I):
                print(f"{path}:{number}: {category}: {line.strip()}")
                failed = True
                count += 1
                break
    if not count:
        print(f"OK: {path}")
raise SystemExit(1 if failed else 0)
