#!/usr/bin/env python3
"""Package the opt-in MUI candidate; no deployment or upload, no owned ROMs."""
from pathlib import Path
import hashlib,json,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.context/amiga/fceux-player'
SRC=ROOT/'amiga/fceux_player'
sys.path.insert(0,str(ROOT/'scripts'))
from make_nes_demo import build
record=json.loads((OUT/'build.json').read_text())
assert record['scheduling']=='release-ui'
files={
 'ZZNesLibrary':(OUT/'ZZNesLibrary').read_bytes(),
 'ZZFceux-ui':(OUT/'ZZFceux').read_bytes(),
 'ZZNesLibrary.info':(SRC/'distribution/ZZFceux.info').read_bytes(),
 'ReadMe.txt':(SRC/'Library-ReadMe.txt').read_bytes(),
 'LICENSE-xSysInfo':(SRC/'LICENSE-xSysInfo').read_bytes(),
 'COPYING3':(SRC/'distribution/COPYING3').read_bytes(),
 'COPYING.RUNTIME':(SRC/'distribution/COPYING.RUNTIME').read_bytes(),
 'overscan.md':(SRC/'overscan.md').read_bytes(),
 'build.json':(OUT/'build.json').read_bytes(),
}
for name in ('ZZNesLibrary','ZZFceux-ui'):assert files[name][:4]==b'\0\0\x03\xf3'
assert hashlib.sha256(files['ZZFceux-ui']).hexdigest()==record['outputs']['ZZFceux']
assert hashlib.sha256(files['ZZNesLibrary']).hexdigest()==record['outputs']['ZZNesLibrary']
rom=bytearray(build(player_test=True));rom[6]=1
files['ROMs/Controller-Test.nes']=bytes(rom)
path='PROGDIR:ROMs/Controller-Test.nes'
files['Library.cfg']=('ZZNESUI1\n0 0 0 1 0 0 0 0\n0 0 '+path.encode().hex()+'\n').encode()
for p in (ROOT/'amiga/fceux_bench/vendor').glob('*'):
 if p.is_file() and ('COPYING' in p.name or 'LICENSE' in p.name):files['licenses/'+p.name]=p.read_bytes()
files['SHA256SUMS']=(''.join(hashlib.sha256(b).hexdigest()+'  '+p+'\n' for p,b in sorted(files.items()))).encode()
dest=OUT/'ZZNes-Library-0.3.0-dev.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('ZZNes-Library.info',(SRC/'distribution/ZZFceux-drawer.info').read_bytes())
 for name,data in files.items():
  info=zipfile.ZipInfo('ZZNes-Library/'+name,date_time=(2026,10,10,0,0,0))
  info.create_system=3;info.compress_type=zipfile.ZIP_DEFLATED
  info.external_attr=(0o100755 if name in ('ZZNesLibrary','ZZFceux-ui') else 0o100644)<<16
  z.writestr(info,data)
 z.writestr('ZZNes-Library/States/',b'')
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 for name,data in files.items():assert z.read('ZZNes-Library/'+name)==data
print(dest,hashlib.sha256(dest.read_bytes()).hexdigest())
