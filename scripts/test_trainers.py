#!/usr/bin/env python3
"""Run trainer cartridges through the actual pinned core with sanitizers."""
import argparse, os, shutil, subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--baseline',action='store_true')
a=p.parse_args()
r=Path(__file__).resolve().parents[1];out=r/'.context/trainer-native'/('baseline' if a.baseline else 'fixed')
core=out/'core';source=r/'development/beta-20261015/source/amiga';overlay=r/'development/mapper78-20261019'
shutil.copytree(r/'development/beta-20261015/source/core',core,dirs_exist_ok=True)
shutil.copytree(overlay/'core',core,dirs_exist_ok=True)
shutil.copytree(overlay/'common',out/'common',dirs_exist_ok=True)
if not a.baseline:
 from prepare_trainers import prepare_core,prepare_gate
 prepare_core(core);prepare_gate(out/'common/cartridge.h')
files=[core/(n+'.cpp') for n in ['x6502','ppu','sound','filter','cart','90','mmc1','mmc3','mmc5','datalatch','compat_core']]
cmd=[os.environ.get('CXX','clang++'),'-std=c++14','-DDINGUX','-DNES_PLAYER','-DFC_STATES','-O2','-g','-fwrapv','-fno-exceptions','-fno-rtti','-Wno-deprecated-register','-Wno-writable-strings','-Wno-non-c-typedef-for-linkage','-fsanitize=address,undefined','-fno-sanitize=array-bounds,pointer-overflow','-fno-sanitize-recover=all','-I'+str(out/'common'),'-I'+str(core),'-I'+str(source/'fceux_bench'),*map(str,files),str(source/'fceux_player/compat/memory.cpp'),str(r/'tests/amiga/emulator/trainers.cpp'),'-o',str(out/'trainers')]
subprocess.run(cmd,check=True)
for mapper in (0,1,2,3,4,5,78,90):
 subprocess.run([str(out/'trainers'),str(mapper),str(out/(str(mapper)+'.nes'))],check=True,env=dict(os.environ,ASAN_OPTIONS='detect_leaks=0'))
