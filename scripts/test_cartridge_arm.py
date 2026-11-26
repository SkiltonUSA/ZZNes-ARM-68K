#!/usr/bin/env python3
"""Original bank-switching guests, fresh-state replay in the exact ARM player."""
import argparse,json,struct
from pathlib import Path
from test_console_jit_core import Machine
from model_neon import correct_cpacr_read
from unicorn.arm_const import UC_ARM_REG_C1_C0_2,UC_ARM_REG_FPEXC
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)

def cartridge(mapper,pal):
 prg=131072;chr=0 if mapper==7 else 32768
 rom=bytearray(16+prg+chr);rom[:4]=b'NES\x1a';rom[4]=prg//16384;rom[5]=chr//8192;rom[6]=(mapper<<4)&255;rom[7]=(mapper&240)|8;rom[8]=0 if mapper==66 else 0x20;rom[11]=0 if chr else 7;rom[12]=pal
 # Identical executable code in each bank continues after the switch. The
 # selected bank's marker controls the green/pass or red/fail background.
 code=bytearray([0x78,0xd8,0xa2,0xff,0x9a,0xa9,0,0x8d,0,0x20,0x8d,1,0x20,
   0xa9,1 if mapper==7 else 0x11,0x8d,1,0x81,0xad,0,0x81,0xc9,1,0xd0,4,
   0xa9,0x2a,0xd0,2,0xa9,0x16,0x85,2,
   0xa9,0x3f,0x8d,6,0x20,0xa9,0,0x8d,6,0x20,0xa5,2,0x8d,7,0x20])
 loop=0x8000+len(code);code+=bytes([0x4c,loop&255,loop>>8])
 for bank in range(prg//32768):
  offset=16+bank*32768;rom[offset:offset+len(code)]=code;rom[offset+256]=bank;rom[offset+257]=255
  for vector in (0x7ffa,0x7ffc,0x7ffe):rom[offset+vector:offset+vector+2]=b'\0\x80'
 return bytes(rom)

def setup(rom,base,pal):
 m=Machine(a.build/'player/fceux.elf',a.build/'core/elf.py',48*1024**2,base);correct_cpacr_read(m)
 m.u.reg_write(UC_ARM_REG_C1_C0_2,0xf00000);m.u.reg_write(UC_ARM_REG_FPEXC,0x40000000);m.u.ctl_flush_tb()
 m.call('_Z13fc_set_regionj',pal);m.u.mem_write(base+0x100000,rom)
 assert m.call('_Z8nes_initPKhjPtS1_',base+0x100000,len(rom),base+0x90000,base+0xb0000)==0
 return m

def frame(m):
 assert m.call('_Z9nes_framehPFivE',0,0)==0
 return {n:m.call(s) for n,s in [('cycles','_Z9fc_cyclesv'),('pixels','_Z8nes_hashv'),('audio','_Z13fc_audio_hashv'),('samples','_Z10fc_samplesv')]}

rows=[]
for mapper in (7,11,66):
 for pal in (0,1):
  name=f'mapper{mapper}-'+('pal' if pal else 'ntsc');rom=cartridge(mapper,pal);(a.output/(name+'.nes')).write_bytes(rom)
  m=setup(rom,0x12000040,pal);first=[frame(m) for _ in range(3)]
  ram=struct.unpack('<I',m.u.mem_read(m.syms['RAM'],4))[0];assert m.u.mem_read(ram+2,1)==b'\x2a',name
  pointer=m.base+0x600000;n=m.call('_Z14fc_state_storePhj',pointer,122880);assert n
  state=bytes(m.u.mem_read(pointer,n));(a.output/(name+'.state')).write_bytes(state)
  resumed=[frame(m) for _ in range(3)];expected=resumed[0]
  m.u.mem_write(pointer,state);assert m.call('_Z13fc_state_loadPKhj',pointer,n)==1;assert frame(m)==expected
  fresh=setup(rom,0x150020c0,pal);pointer=fresh.base+0x600000;fresh.u.mem_write(pointer,state)
  assert fresh.call('_Z13fc_state_loadPKhj',pointer,n)==1;assert frame(fresh)==expected
  row={'case':name,'mapper':mapper,'pal':pal,'frames':first,'state_bytes':n,'resumed_frames':resumed,'fresh_replay':True};rows.append(row)
  (a.output/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
  print('PASS',name,'guest bank switch, green pass screen, live/fresh relocated state, exact video/audio/cycles',flush=True)
