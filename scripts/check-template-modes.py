"""Compile both report modes and entry switches using one shared latexmk job.

The user's options file is restored byte for byte, even on failure.
Requires Python's standard library plus the project's TeX toolchain.
"""
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
options = root / 'config/project-options.tex'
original = options.read_bytes()
out = root / 'build/mode-check'
for folder in [out, out / 'chapters', out / 'appendices']:
    folder.mkdir(parents=True, exist_ok=True)

def set_mode(reference):
    text = original.decode('utf-8')
    flag = 'true' if reference else 'false'
    text, count = re.subn(r'(?m)^(\\IMDTReferenceReport)(?:true|false)\b',
                          lambda match: match.group(1) + flag, text, count=1)
    if count != 1:
        raise RuntimeError('Cannot locate the explicit report mode switch')
    options.write_text(text, encoding='utf-8')

try:
    sequence = [
        ('reference-first', True, 'imdt-proposal-report.tex', 12),
        ('form-first', True, 'imdt-topic-work-plan.tex', 4),
        ('writing', False, 'imdt-proposal-report.tex', 7),
        ('form-second', False, 'imdt-topic-work-plan.tex', 4),
        ('reference-final', True, 'imdt-proposal-report.tex', 12),
    ]
    for name, reference, entry, expected_pages in sequence:
        set_mode(reference)
        subprocess.run(['latexmk', '-xelatex', '-jobname=output',
                        '-outdir=build/mode-check', entry], cwd=root, check=True)
        log = (out / 'output.log').read_text(encoding='utf-8', errors='replace')
        match = re.search(r'Output written on .*?\((\d+) pages?[,)]', log, re.S)
        if not match or int(match.group(1)) != expected_pages:
            raise RuntimeError(f'{name}: expected {expected_pages} pages')
        snapshot = out / (name + '.log')
        snapshot.write_text(log, encoding='utf-8')
        subprocess.run([sys.executable, str(root / 'scripts/check-build.py'), str(snapshot)], check=True)
        (out / (name + '.pdf')).write_bytes((out / 'output.pdf').read_bytes())
finally:
    options.write_bytes(original)
