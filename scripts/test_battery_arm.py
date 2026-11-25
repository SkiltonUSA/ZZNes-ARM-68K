#!/usr/bin/env python3
"""Exercise exact battery RAM/state replay in relocated Cortex-A9 players."""
import argparse,struct,hashlib
from pathlib import Path
from test_console_jit_core import Machine
from model_neon import correct_cpacr_read
from unicorn.arm_const import UC_ARM_REG_C1_C0_2,UC_ARM_REG_FPEXC
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build',type=Path,required=True);p.add_argument('--fixtures',type=Path,default=Path('.context/battery-native'));a=p.parse_args()
out=a.fixtures/'arm';out.mkdir(exist_ok=True)
def setup(rom,base):
 m=Machine(a.build/'player/fceux.elf',a.build/'core/elf.py',48*1024**2,base)
 correct_cpacr_read(m);m.u.reg_write(UC_ARM_REG_C1_C0_2,0xf00000);m.u.reg_write(UC_ARM_REG_FPEXC,0x40000000);m.u.ctl_flush_tb()
 m.u.mem_write(base+0x100000,rom);assert m.call('_Z8nes_initPKhjPtS1_',base+0x100000,len(rom),base+0x90000,base+0xb0000)==0
 n=m.call('_Z8nes_savePPh',base+0x500000);ptr=struct.unpack('<I',m.u.mem_read(base+0x500000,4))[0]
 return m,n,ptr

def frame(m):
 assert m.call('_Z9nes_framehPFivE',0,0)==0
 return tuple(m.call(k)for k in ('_Z13fc_video_hashv','_Z13fc_audio_hashv','_Z10fc_samplesv','_Z9fc_cyclesv'))
for mapper in (1,4,5):
 for trainer in (0,1):
  name=f'battery-{mapper}-{trainer}';rom=(a.fixtures/(name+'.nes')).read_bytes();previous=None
  for base in (0x12000040,0x150020c0):
   m,n,ptr=setup(rom,base);assert n==(32768 if mapper==5 else 8192)
   for _ in range(3):frame(m)
   first=bytes(m.u.mem_read(ptr,n));assert first[:2]==b'\x01\x5a';(out/(name+'-first.sav')).write_bytes(first)
   state_address=base+0x600000;count=m.call('_Z14fc_state_storePhj',state_address,122880);assert count
   state=bytes(m.u.mem_read(state_address,count));expected=frame(m)
   m.u.mem_write(ptr,b'\xcc'*n);m.u.mem_write(state_address,state);assert m.call('_Z13fc_state_loadPKhj',state_address,count)==1
   assert bytes(m.u.mem_read(ptr,n))==first and frame(m)==expected
   # Fresh process uses the bytes exported by the old process, then trainer order.
   fresh,n2,p2=setup(rom,base);assert n2==n;fresh.u.mem_write(p2,first);fresh.call('_Z17fc_battery_loadedv')
   for _ in range(3):frame(fresh)
   second=bytes(fresh.u.mem_read(p2,n));assert second[:2]==b'\x02\x5a'
   assert second[2:]==first[2:];(out/(name+'-second.sav')).write_bytes(second)
   # An imported battery cannot suppress the trainer's power-on bytes.
   if trainer:
    fresh.u.mem_write(p2,b'\xcc'*n);fresh.call('_Z17fc_battery_loadedv')
    # MMC5 trainer falls back to a read handler because reset protects RAM.
    # The native fixture explicitly checks CPU reads; physical saves test SRAM.
    if mapper!=5:assert bytes(fresh.u.mem_read(p2+0x1000,512))==rom[16:528]
   hashes=(hashlib.sha256(first).hexdigest(),hashlib.sha256(second).hexdigest(),expected)
   if previous is not None:assert hashes==previous
   previous=hashes
   print('PASS ARM battery',mapper,'trainer',trainer,hex(base),'fresh process, exact SRAM, HQ state/video/PCM/cycles',flush=True)
print('PASS Cortex-A9 instruction model; file I/O and physical coherency checked separately')
