#!/usr/bin/env python3
"""Compile the complete pinned board set against the ARM platform declarations.

Diagnostic inventory only: successful compilation is not linking, mapper
registration, correct cartridge metadata, or gameplay compatibility.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report', type=Path, default=Path('.context/fceux-full/audit.json'))
    a = p.parse_args()
    subprocess.run(['python3', ROOT / 'scripts/prepare_fceux_full.py', '--verify'], check=True)
    vendor = ROOT / 'development/fceux-full/vendor/src'
    stage = ROOT / '.context/fceux-full/source'
    shutil.copytree(vendor, stage, dirs_exist_ok=True)
    # Preserve board source verbatim; substitute only the frontend umbrella.
    (stage / 'boards/mapinc.h').write_text('#include "platform.h"\n#include "../unif.h"\n')
    snap = ROOT / 'development/beta-20261015/source'
    flags = ['--target=arm-none-eabi', '-mcpu=cortex-a9', '-marm', '-mfloat-abi=soft',
             '-ffreestanding', '-fno-builtin', '-fno-exceptions', '-fno-rtti',
             '-nostdinc++', '-std=c++14', '-DFC_ARM', '-DDINGUX', '-DFC_STATES',
             '-fwrapv', '-ferror-limit=5', '-Wno-deprecated-register',
             '-Wno-writable-strings', '-Wno-non-c-typedef-for-linkage',
             '-I' + str(snap / 'amiga/fceux_bench'), '-I' + str(snap / 'core')]
    results = []
    for source in sorted((stage / 'boards').glob('*.cpp')):
        r = subprocess.run([os.environ.get('CLANG', 'clang'), *flags, '-fsyntax-only', source],
                           capture_output=True, text=True)
        results.append(dict(source='src/boards/' + source.name, compiles=r.returncode == 0,
                            diagnostics=r.stderr.replace(str(ROOT) + '/', '')))
    report = dict(scope='ARM translation-unit audit only; no mapper is enabled by this tool',
                  compiler=subprocess.check_output([os.environ.get('CLANG', 'clang'), '--version'], text=True),
                  compiled=sum(r['compiles'] for r in results), total=len(results), boards=results)
    out = ROOT / a.report
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + '\n')
    print(f"ARM board audit: {report['compiled']}/{report['total']} compile; report: {a.report}")


if __name__ == '__main__':
    main()
