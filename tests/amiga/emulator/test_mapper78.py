"""Mapper 78 tests against the actual core; optional private ROM smoke run."""
from pathlib import Path
import subprocess,os,sys
root=Path(__file__).resolve().parents[3];out=root/'.context/mapper78-native';out.mkdir(parents=True,exist_ok=True)
core=root/'development/beta-20261015/source/core';source=root/'development/beta-20261015/source/amiga';overlay=root/'development/mapper78-20261019'
files=[(overlay/'core'/(n+'.cpp') if (overlay/'core'/(n+'.cpp')).exists() else core/(n+'.cpp')) for n in ['x6502','ppu','sound','filter','cart','90','mmc1','mmc3','mmc5','datalatch','compat_core']]
cmd=[os.environ.get('CXX','clang++'),'-std=c++14','-DDINGUX','-DNES_PLAYER','-DFC_STATES','-O2','-g','-fwrapv','-fno-exceptions','-fno-rtti','-Wno-deprecated-register','-Wno-writable-strings','-Wno-non-c-typedef-for-linkage','-fsanitize=address,undefined','-fno-sanitize=array-bounds,pointer-overflow','-fno-sanitize-recover=all','-I'+str(overlay/'common'),'-I'+str(core),'-I'+str(source/'fceux_bench'),*map(str,files),str(source/'fceux_player/compat/memory.cpp')]
subprocess.run(cmd+[root/'tests/amiga/emulator/mapper78.cpp','-o',out/'mapper78'],check=True)
for variant in ['holy','cosmo','3']:subprocess.run([out/'mapper78',variant],check=True)
# Existing fine-scroll fixture exercises the retained mapper0 path with new adapter.
subprocess.run([sys.executable,root/'scripts/make_scrolling_fixture.py',out/'Scroll.nes'],check=True)
subprocess.run(cmd+[root/'tests/amiga/emulator/scrolling.cpp','-o',out/'scrolling'],check=True)
for region in ['NTSC','PAL']:subprocess.run([out/'scrolling',out/'Scroll.nes',out/(region+'.raw'),*(['PAL']if region=='PAL'else[])],check=True)
