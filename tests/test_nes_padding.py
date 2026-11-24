#!/usr/bin/env python3
"""Exercise the production loader with plain/ZIP inputs and hostile trailers."""
from pathlib import Path
import argparse,tempfile,subprocess,zipfile,hashlib,sys
p=argparse.ArgumentParser(description=__doc__);p.add_argument("--trainers",action="store_true");args=p.parse_args()
R=Path(__file__).resolve().parents[1];lib=R/'.context/launcher-build/library'
with tempfile.TemporaryDirectory() as td:
 d=Path(td)
 if args.trainers:
  sys.path.insert(0,str(R/'scripts'))
  from prepare_trainers import prepare_gate
  (d/'cartridge.h').write_bytes((lib/'cartridge.h').read_bytes());prepare_gate(d/'cartridge.h')
 (d/'test.c').write_text('''#include "zip/rom_archive.h"
#include "nes_padding.h"
int main(int argc,char**argv){unsigned n;unsigned char*out=malloc(INPUT_LIMIT);int e=zzn_rom_load(argv[1],out,INPUT_LIMIT,&n,0,NULL,0);if(!e&&nes_cartridge(out,n)<0)e=99;
 if(!e&&!zzn_write_clean(argv[2],out,n))return 98;printf("%d %u %u\\n",e,n,zzn_trimmed);free(out);return 0;}
''')
 subprocess.run(['cc','-std=c99','-DINPUT_LIMIT='+('0xc0210' if args.trainers else '0xc0010'),'-fsanitize=address,undefined','-I'+str(d),'-I'+str(R/'src'),'-I'+str(lib),str(d/'test.c'),str(lib/'zip/puff.c'),'-o',str(d/'test')],check=True)
 header=b'NES\x1a'+bytes([2,1,0x40,0,0,0,0,0,0,0,0,0]);rom=header+bytes(range(256))*160
 assert len(rom)==16+32768+8192
 def check(data,valid,zipmode=None):
  src=d/('rom.zip'if zipmode is not None else 'rom.nes');dst=d/'clean.nes'
  if zipmode is None:src.write_bytes(data)
  else:
   with zipfile.ZipFile(src,'w',compression=zipmode)as z:z.writestr('nested/game.nes',data)
  before=src.read_bytes();result=subprocess.check_output([str(d/'test'),str(src),str(dst)],text=True).split();assert (int(result[0])==0)==valid,result
  assert src.read_bytes()==before
  if valid:assert dst.read_bytes()==rom
 for mode in [None,zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED]:
  check(rom,True,mode);check(rom+b' \r\n'*174768,True,mode)
  check(rom+b'\0',False,mode);check(rom+b' \t',False,mode);check(rom+b'NES\x1a',False,mode)
  check(rom[:-1],False,mode)
  bad=bytearray(rom);bad[7]=8;check(bytes(bad)+b' ',False,mode)
  bad=bytearray(rom);bad[6]|=4;check(bytes(bad)+b' ',False,mode)
  bad=bytearray(rom);bad[6]=0xf0;bad[7]=0xf0;check(bytes(bad)+b' ',False,mode)
  check(rom+b' '*(0x200000-len(rom)+1),False,mode)
 # Corrupted stored ZIP data must fail CRC before trimming.
 src=d/'bad.zip'
 with zipfile.ZipFile(src,'w',compression=zipfile.ZIP_STORED)as z:z.writestr('game.nes',rom+b' ')
 b=bytearray(src.read_bytes());i=b.index(b'NES\x1a');b[i+16]^=1;src.write_bytes(b)
 result=subprocess.check_output([str(d/'test'),str(src),str(d/'clean.nes')],text=True).split();assert int(result[0])==9,result
 if args.trainers:
  h=bytearray(header);h[6]|=4;rom=bytes(h)+bytes(range(256))*2+rom[16:]
  for mode in (None,zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED):
   check(rom,True,mode);check(rom+b' \r\n'*31,True,mode);check(rom[:-1],False,mode);check(rom+b'\0',False,mode)
  h[4]=32;h[5]=32;rom=bytes(h)+bytes(range(256))*2+bytes(768*1024)
  for mode in (None,zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED):
   check(rom,True,mode);check(rom+b' \r\n',True,mode)
  print('PASS trainer raw/stored/deflated recovery preserves all 512 trainer bytes')
 print('PASS raw/stored/deflated padding, original-byte preservation, clean-copy readback, strict header/size/tail checks, ZIP CRC')
