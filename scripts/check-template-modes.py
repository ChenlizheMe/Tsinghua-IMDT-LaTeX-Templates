"""Compile both report modes and entry switches using one shared latexmk job.

The user's options file is restored byte for byte, even on failure.
Requires Python's standard library plus the project's TeX toolchain.
"""
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
options = root / 'config/user.tex'
original = options.read_bytes()
out = root / 'build/mode-check'
for folder in [out, out / 'chapters', out / 'appendices']:
    folder.mkdir(parents=True, exist_ok=True)

def set_mode(reference, submission=False):
    text = original.decode('utf-8')
    mode = 'reference' if reference else 'writing'
    text += '\n\\imdtsetup{mode='+mode+',hints=show,examples=show}\n'
    if submission:
        text += r'''
\imdtsetup{title={配置接口验证},author={接口测试},student-id={2099000001},
  supervisor={测试导师},report-date={2026年10月21日},secrecy=public,
  cross-discipline-check=no,experiment=yes,safety-training=yes,safety-report=yes,
  thesis-type=product,work-plan={第一阶段完成调研。\par 第二阶段实现系统。}}
\imdtsubmission
'''
    options.write_bytes(text.encode('utf-8'))

try:
    sequence = [
        ('reference-first', True, 'imdt-proposal-report.tex', 12, False),
        ('form-first', True, 'imdt-topic-work-plan.tex', 4, False),
        ('writing', False, 'imdt-proposal-report.tex', 7, False),
        ('submission', False, 'imdt-proposal-report.tex', 6, True),
        ('form-filled', False, 'imdt-topic-work-plan.tex', 4, True),
        ('reference-final', True, 'imdt-proposal-report.tex', 12, False),
        ('writing-final', False, 'imdt-proposal-report.tex', 7, False),
    ]
    for name, reference, entry, expected_pages, submission in sequence:
        set_mode(reference, submission)
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
