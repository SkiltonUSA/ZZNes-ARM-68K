from pathlib import Path
import argparse,struct,zlib,zipfile,json,hashlib
a=argparse.ArgumentParser();a.add_argument('--guest',type=Path,required=True);a.add_argument('--output',type=Path,required=True);args=a.parse_args()
p=args.output;p.mkdir(parents=True,exist_ok=True)
rom=args.guest.read_bytes()
h=bytearray(rom[:16]);h[8]=0x10
expected=bytes(h)+rom[16:]
def c(t,b):return t+struct.pack('<I',len(b))+b
unif=b'UNIF'+struct.pack('<I',7)+bytes(24)+c(b'MAPR',b'NES-ANROM\0')+c(b'PRG0',rom[16:])+c(b'PCK0',struct.pack('<I',zlib.crc32(rom[16:])))
(p/'expected.nes').write_bytes(expected)
(p/'board.unif').write_bytes(unif)
(p/'BOARD.UNF').write_bytes(unif)
# Fixed ZIP metadata reproduces the exact files checked on the Amiga.
def entry(name):
 info=zipfile.ZipInfo(name,(2026,11,26,15,57,40));info.external_attr=0o600<<16;return info
for name,mode in [('stored.zip',zipfile.ZIP_STORED),('deflated.zip',zipfile.ZIP_DEFLATED)]:
 with zipfile.ZipFile(p/name,'w',compression=mode) as z:z.writestr(entry('nested/game.unif'),unif,compress_type=mode)
bad=bytearray(unif);bad[-1]^=1;(p/'bad-crc.unif').write_bytes(bad)
with zipfile.ZipFile(p/'ambiguous.zip','w') as z:z.writestr(entry('a.unif'),unif);z.writestr(entry('b.nes'),expected)
(p/'fixtures.json').write_text(json.dumps({'expected_sha256':hashlib.sha256(expected).hexdigest(),'cases':[{ 'file':n,'success':ok,'source_md5':hashlib.md5((p/n).read_bytes()).hexdigest()} for n,ok in [('board.unif',True),('BOARD.UNF',True),('stored.zip',True),('deflated.zip',True),('bad-crc.unif',False),('ambiguous.zip',False)]]},indent=2)+'\n')
