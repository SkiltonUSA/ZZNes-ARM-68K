#!/usr/bin/env python3
"""Exercise the built candidate's real launcher loader, including ZIP CRC."""
from pathlib import Path
import argparse, struct, subprocess, tempfile, zipfile, zlib
p=argparse.ArgumentParser();p.add_argument('build',type=Path);a=p.parse_args()
lib=a.build.resolve()/'library'
with tempfile.TemporaryDirectory() as folder:
 d=Path(folder)
 (d/'loader.c').write_text('''#include "zip/rom_archive.h"
#include "nes_padding.h"
int main(int argc,char**argv){unsigned n=0;unsigned char*out=malloc(0xc0210);int e=zzn_rom_load(argv[1],out,0xc0210,&n,0,NULL,0);
 if(!e&&nes_cartridge(out,n)<0)e=99;
 if(!e&&!zzn_write_clean(argv[2],out,n))e=98;
 printf("%d %u %u %u\\n",e,n,zzn_trimmed,zzn_normalized);free(out);return 0;}
''')
 subprocess.run(['clang','-std=c99','-fsanitize=address,undefined','-I'+str(lib),str(d/'loader.c'),str(lib/'zip/puff.c'),'-o',str(d/'loader')],check=True)
 def chunk(tag,data):return tag+struct.pack('<I',len(data))+data
 payload=bytes(range(256))*512
 header=bytearray(b'NES\x1a'+bytes(12));header[4]=8;header[6]=0x70;header[7]=8;header[8]=0x10;header[11]=7
 expected=bytes(header)+payload
 unif=b'UNIF'+struct.pack('<I',7)+bytes(24)+chunk(b'MAPR',b'NES-ANROM\0')+chunk(b'PRG0',payload)+chunk(b'PCK0',struct.pack('<I',zlib.crc32(payload)))
 split=b'UNIF'+struct.pack('<I',7)+bytes(24)+chunk(b'MAPR',b'NES-ANROM\0')+chunk(b'PRG1',payload[65536:])+chunk(b'PRG0',payload[:65536])+chunk(b'PCK1',struct.pack('<I',zlib.crc32(payload[65536:])))
 def check(data,member,expected_bytes,mode=None,error=None):
  source=d/('source.zip' if mode is not None else member);dest=d/'prepared.nes'
  if mode is None:source.write_bytes(data)
  else:
   with zipfile.ZipFile(source,'w',compression=mode)as f:f.writestr('nested/'+member,data)
  before=source.read_bytes();result=list(map(int,subprocess.check_output([str(d/'loader'),str(source),str(dest)],text=True).split()))
  assert source.read_bytes()==before
  if expected_bytes is None:assert result[0]!=0,(member,result)
  else:assert result[0]==0 and dest.read_bytes()==expected_bytes,(member,result)
  if error is not None:assert result[0]==error,result
  return source
 for mode in (None,zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED):
  check(unif,'board.unif',expected,mode);check(unif,'BOARD.UNF',expected,mode)
  check(split,'split.unif',expected,mode)
  check(expected,'board.nes',expected,mode);check(expected+b' \r\n','board.nes',expected,mode)
  check(expected+b'\0','board.nes',None,mode)
  bad=bytearray(unif);bad[-1]^=1;check(bad,'board.unif',None,mode)
  check(unif[:-1],'board.unif',None,mode)
  check(unif+chunk(b'MAPR',b'NES-ANROM\0'),'board.unif',None,mode)
 source=check(unif,'board.unif',expected,zipfile.ZIP_STORED)
 bad=bytearray(source.read_bytes());bad[bad.index(b'UNIF')+80]^=1;source.write_bytes(bad)
 result=subprocess.check_output([str(d/'loader'),str(source),str(d/'unused.nes')],text=True).split();assert int(result[0])==9,result
 with zipfile.ZipFile(source,'w')as f:
  f.writestr('one.unif',unif);f.writestr('two.nes',expected)
 result=subprocess.check_output([str(d/'loader'),str(source),str(d/'unused.nes')],text=True).split();assert int(result[0])==7,result
 print('PASS launcher plain/stored/deflated NES 2.0 and UNIF; original preservation, trailer rules, inner/outer CRC, multi-cartridge refusal')
