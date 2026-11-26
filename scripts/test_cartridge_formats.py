#!/usr/bin/env python3
"""Synthetic cartridge integration; no copyrighted ROMs or hardware access."""
import os,shutil,subprocess
from pathlib import Path
from prepare_trainers import prepare_core,prepare_gate
from prepare_battery import core as battery_core,gate
from prepare_cartridge_formats import core
r=Path(__file__).resolve().parents[1];out=r/'.context/cartridge-native';c=out/'core';source=r/'development/beta-20261015/source/amiga'
shutil.copytree(r/'development/beta-20261015/source/core',c,dirs_exist_ok=True)
shutil.copytree(r/'development/mapper78-20261019/core',c,dirs_exist_ok=True)
shutil.copytree(r/'development/cartridge-formats',out/'common',dirs_exist_ok=True)
prepare_core(c);battery_core(c);core(c)
files=[c/(n+'.cpp')for n in ['x6502','ppu','sound','filter','cart','90','mmc1','mmc3','mmc5','datalatch','compat_core']]
cmd=['clang++','-std=c++14','-DDINGUX','-DNES_PLAYER','-DFC_STATES','-O2','-g','-fwrapv','-fno-exceptions','-fno-rtti','-Wno-deprecated-register','-Wno-writable-strings','-Wno-non-c-typedef-for-linkage','-fsanitize=address,undefined','-fno-sanitize=array-bounds,pointer-overflow','-fno-sanitize-recover=all','-I'+str(out/'common'),'-I'+str(c),'-I'+str(source/'fceux_bench'),*map(str,files),str(source/'fceux_player/compat/memory.cpp'),str(r/'tests/amiga/emulator/cartridge_formats.cpp'),'-o',str(out/'formats')]
subprocess.run(cmd,check=True)
env=dict(os.environ,ASAN_OPTIONS='detect_leaks=0')
subprocess.run([str(out/'formats')],check=True,env=env)
for mapper in (2,3,7,11,66):
 for version,sub in [(0,0),(1,0)]+([(1,1),(1,2)]if mapper!=66 else []):
  subprocess.run([str(out/'formats'),str(mapper),str(sub),str(version)],check=True,env=env)
# Exercise the same battery/trainer lifecycle against explicit NES 2.0 RAM.
battery=cmd.copy();battery.insert(1,'-DTEST_NES2')
battery[battery.index(str(r/'tests/amiga/emulator/cartridge_formats.cpp'))]=str(r/'tests/amiga/emulator/battery.cpp')
battery[-1]=str(out/'battery-nes2');subprocess.run(battery,check=True)
for mapper in (1,4,5):
 for trainer in (0,1):
  subprocess.run([str(out/'battery-nes2'),str(mapper),str(trainer),str(out/f'nes2-{mapper}-{trainer}')],check=True,env=env)
