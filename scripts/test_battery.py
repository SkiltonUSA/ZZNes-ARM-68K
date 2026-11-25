#!/usr/bin/env python3
"""Native mapper battery and failure-recovery tests, without hardware access."""
import os,shutil,subprocess
from pathlib import Path
from prepare_trainers import prepare_core,prepare_gate
from prepare_battery import core as battery_core,gate
r=Path(__file__).resolve().parents[1];out=r/'.context/battery-native';c=out/'core';source=r/'development/beta-20261015/source/amiga'
shutil.copytree(r/'development/beta-20261015/source/core',c,dirs_exist_ok=True)
shutil.copytree(r/'development/mapper78-20261019/core',c,dirs_exist_ok=True)
shutil.copytree(r/'development/mapper78-20261019/common',out/'common',dirs_exist_ok=True)
prepare_core(c);prepare_gate(out/'common/cartridge.h');battery_core(c);gate(out/'common/cartridge.h')
files=[c/(n+'.cpp')for n in ['x6502','ppu','sound','filter','cart','90','mmc1','mmc3','mmc5','datalatch','compat_core']]
cmd=['clang++','-std=c++14','-DDINGUX','-DNES_PLAYER','-DFC_STATES','-O2','-g','-fwrapv','-fno-exceptions','-fno-rtti','-Wno-deprecated-register','-Wno-writable-strings','-Wno-non-c-typedef-for-linkage','-fsanitize=address,undefined','-fno-sanitize=array-bounds,pointer-overflow','-fno-sanitize-recover=all','-I'+str(out/'common'),'-I'+str(c),'-I'+str(source/'fceux_bench'),*map(str,files),str(source/'fceux_player/compat/memory.cpp'),str(r/'tests/amiga/emulator/battery.cpp'),'-o',str(out/'battery')]
subprocess.run(cmd,check=True)
for mapper in (1,4,5):
 for trainer in (0,1):subprocess.run([str(out/'battery'),str(mapper),str(trainer),str(out/f'battery-{mapper}-{trainer}')],check=True,env=dict(os.environ,ASAN_OPTIONS='detect_leaks=0'))
subprocess.run(['clang','-O2','-g','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I'+str(r/'development/battery-save'),str(r/'tests/amiga/emulator/battery_files.c'),'-o',str(out/'files')],check=True)
subprocess.run([str(out/'files')],check=True)
