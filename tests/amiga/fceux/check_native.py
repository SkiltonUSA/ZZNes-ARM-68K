#!/usr/bin/env python3
"""Compare original floating initialization, fixed tables and instrumented core.
Pass a privately held NTSC mapper 0/90 ROM and frame count; no ROM is bundled.
"""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[3];out=ROOT/'.context/amiga/fceux-bench'
rom=Path(sys.argv[1]);frames=int(sys.argv[2]);assert 1<=frames<=3600
reference=None
for name in ['native','native-fixed','native-sanitize']:
 r=subprocess.run([out/name,rom,str(frames)],text=True,capture_output=True,check=True)
 assert not r.stderr,r.stderr
 (out/(rom.stem+'-'+name+'.log')).write_text(r.stdout)
 lines=r.stdout.splitlines();assert len(lines)==frames+1
 if reference is None:reference=lines[:-1]
 assert lines[:-1]==reference,name
 assert all(int(line.split('cycles=')[1].split()[0])>0 for line in reference)
 print(name,lines[-1])
print('PASS exact cycles, video/emphasis, PCM hash/count equivalence; ASan + selected UBSan')
