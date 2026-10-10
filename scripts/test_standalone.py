#!/usr/bin/env python3
"""Run the existing native checks using an original generated ROM; no hardware."""
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.context/amiga/fceux-player'

def run(*args):
    subprocess.run(args, cwd=ROOT, check=True,
                   env=os.environ | {'UBSAN_OPTIONS': 'halt_on_error=1'})

run(sys.executable, 'scripts/make_nes_demo.py', OUT / 'standalone-demo.nes')
run(sys.executable, 'tests/amiga/fceux_player/check_native.py',
    OUT / 'standalone-demo.nes', '120')
run(sys.executable, '-m', 'unittest', 'discover', '-s', 'tests/amiga/fceux', '-v')
common = ['clang', '-std=c99', '-O2', '-g', '-fsanitize=address,undefined']
for name, source, flags in [
    ('flip', 'tests/amiga/mesen_nes/flip_plan.c', ['-Iamiga/mesen_nes']),
    ('direct', 'tests/amiga/mesen_nes/direct_plan.c',
     ['-DNES_PLAYER', '-Iamiga/mesen_nes', '-I' + str(OUT)]),
    ('mmu', 'tests/amiga/mesen/mmu_plan.c',
     ['-DMB_ALLOCATION=0x400000u', '-Iamiga/mesen_bench']),
]:
    executable = OUT / (name + '-test')
    run(*common, *flags, source, '-o', executable)
    run(executable)

audio = (ROOT / 'amiga/mesen_nes/player_audio.h').read_text()
audio = audio.split('static void player_audio_close')[0]
(OUT / 'audio-worker-under-test.h').write_text(
    audio.replace('#include <dos/dostags.h>', ''))
run(*common, '-I' + str(OUT), 'tests/amiga/mesen_nes/audio_worker.c',
    '-o', OUT / 'audio-worker-test')
run(OUT / 'audio-worker-test')
run(sys.executable, 'tests/amiga/fceux_player/check_host.py')
print('PASS standalone native checks; no hardware was accessed.')
