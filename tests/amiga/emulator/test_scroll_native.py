"""Original fine-scroll fixture against the pinned core; no commercial ROMs."""
from pathlib import Path
import subprocess,sys,os
root=Path(__file__).resolve().parents[3];out=root/'.context/scrolling-test';out.mkdir(parents=True,exist_ok=True)
core=root/'development/beta-20261015/source/core';source=root/'development/beta-20261015/source/amiga'
subprocess.run([sys.executable,root/'scripts/make_scrolling_fixture.py',out/'Scroll.nes'],check=True)
files=[core/(n+'.cpp')for n in ['x6502','ppu','sound','filter','cart','90','mmc1','mmc3','mmc5','datalatch','compat_core']]
subprocess.run([os.environ.get('CXX','clang++'),'-std=c++14','-DDINGUX','-DNES_PLAYER','-DFC_STATES','-O2','-g','-fwrapv','-fno-exceptions','-fno-rtti','-Wno-deprecated-register','-Wno-writable-strings','-Wno-non-c-typedef-for-linkage','-fsanitize=address,undefined','-fno-sanitize=array-bounds,pointer-overflow','-fno-sanitize-recover=all','-I'+str(core),'-I'+str(source/'fceux_bench'),*map(str,files),source/'fceux_player/compat/memory.cpp',root/'tests/amiga/emulator/scrolling.cpp','-o',out/'scroll-native'],check=True)
for region in ['NTSC','PAL']:
 subprocess.run([out/'scroll-native',out/'Scroll.nes',out/(region+'.raw'),*(['PAL']if region=='PAL'else[])],check=True)
 print('PASS',region,'fine scroll with native ASan/selected UBSan',flush=True)
