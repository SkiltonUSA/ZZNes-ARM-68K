#!/usr/bin/env python3
"""Pinned independent NES timing fixtures, sanitizer run. Never launches hardware."""
import hashlib,json,os,subprocess,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'.context/amiga/mesen-player'
spec=json.loads((ROOT/'tests/amiga/mesen_nes/player-fixtures.json').read_text())
for name,sha in spec['files'].items():
 p=out/'fixtures'/name;p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():p.write_bytes(urllib.request.urlopen(f"https://raw.githubusercontent.com/christopherpow/nes-test-roms/{spec['commit']}/{name}",timeout=30).read())
 assert hashlib.sha256(p.read_bytes()).hexdigest()==sha,name
subprocess.run(['clang++','-std=c++14','-DLIBRETRO','-DNES_PLAYER','-DNES_NATIVE_TEST','-O2','-fno-exceptions','-fno-rtti','-g','-fsanitize=address,undefined','-I'+str(out),'-Iamiga/mesen_nes',out/'unified.cpp','tests/amiga/mesen_nes/player.cpp','-o',out/'player-test'],cwd=ROOT,check=True)
logs=[]
for name in spec['files']:
 r=subprocess.run([out/'player-test',out/'fixtures'/name],env=os.environ|{'UBSAN_OPTIONS':'halt_on_error=1'},capture_output=True,text=True,timeout=90)
 logs.append(r.stdout+r.stderr);print(logs[-1],end='',flush=True)
 (out/'timing-tests.log').write_text(''.join(logs))
 if r.returncode:raise SystemExit(r.returncode)
print(f"PASS {len(logs)} pinned APU/MMC3 timing ROMs; ASan/UBSan")
# Host adapter tests complement the independent timing-ROM suite.
cmd=['clang++','-std=c++14','-DLIBRETRO','-DNES_PLAYER','-DNES_NATIVE_TEST','-O2','-fno-exceptions','-fno-rtti','-g','-fsanitize=address,undefined','-I'+str(out),'-Iamiga/mesen_nes',str(out/'unified.cpp'),'tests/amiga/mesen_nes/cartridge.cpp','-o',str(out/'cartridge-test')]
subprocess.run(cmd,cwd=ROOT,check=True)
subprocess.run([out/'cartridge-test'],env=os.environ|{'UBSAN_OPTIONS':'halt_on_error=1'},check=True)
for size in ['0x100000u','0x400000u']:
 subprocess.run(['clang','-std=c99','-O2','-fsanitize=address,undefined','-DMB_ALLOCATION='+size,'-Iamiga/mesen_bench','tests/amiga/mesen/mmu_plan.c','-o',out/'mmu-test'],cwd=ROOT,check=True)
 subprocess.run([out/'mmu-test'],check=True)

# Compare sparse event scheduling with the previous dense mixer sample for sample.
cmd[-3:] = ['tests/amiga/mesen_nes/mixer.cpp','-o',str(out/'mixer-test')]
subprocess.run(cmd,cwd=ROOT,check=True)
subprocess.run([out/'mixer-test'],env=os.environ|{'UBSAN_OPTIONS':'halt_on_error=1'},check=True)

# Exercise the production 68k audio worker under deterministic fake Exec/AHI.
# Native scheduling is not claimed to reproduce AmigaOS; hardware acceptance
# remains separate. The tested function is extracted unchanged, not duplicated.
audio=(ROOT/'amiga/mesen_nes/player_audio.h').read_text().split('static void player_audio_close')[0]
(out/'audio-worker-under-test.h').write_text(audio.replace('#include <dos/dostags.h>', ''))
subprocess.run(['clang','-std=c99','-O2','-g','-fsanitize=address,undefined',
 '-I'+str(out),ROOT/'tests/amiga/mesen_nes/audio_worker.c','-o',out/'audio-worker-test'],check=True)
subprocess.run([out/'audio-worker-test'],env=os.environ|{'UBSAN_OPTIONS':'halt_on_error=1'},check=True)
