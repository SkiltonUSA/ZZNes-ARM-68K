#!/usr/bin/env python3
"""Trainer execution and HQ state replay in the actual relocated ARM payload."""
import argparse,struct
from pathlib import Path
from test_console_jit_core import Machine
from model_neon import correct_cpacr_read
from unicorn.arm_const import UC_ARM_REG_C1_C0_2,UC_ARM_REG_FPEXC
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--build',type=Path,default=Path('.context/trainer-build'))
p.add_argument('--fixtures',type=Path,default=Path('.context/trainer-native/fixed'))
a=p.parse_args()
for mapper in (0,1,2,3,4,5,78,90):
 for base in (0x12000040,0x150020c0):
  m=Machine(a.build/'player/fceux.elf',a.build/'core/elf.py',48*1024**2,base)
  correct_cpacr_read(m);m.u.reg_write(UC_ARM_REG_C1_C0_2,0xf00000);m.u.reg_write(UC_ARM_REG_FPEXC,0x40000000);m.u.ctl_flush_tb()
  rom=(a.fixtures/(str(mapper)+'.nes')).read_bytes();m.u.mem_write(base+0x100000,rom)
  assert m.call('_Z8nes_initPKhjPtS1_',base+0x100000,len(rom),base+0x90000,base+0xb0000)==0
  for _ in range(3):assert m.call('_Z9nes_framehPFivE',0,0)==0
  ram=struct.unpack('<I',m.u.mem_read(m.syms['RAM'],4))[0];assert m.u.mem_read(ram,1)==b'\x5a'
  address=base+0x500000 # model-only scratch, beyond linked BSS and before JIT arena
  n=m.call('_Z14fc_state_storePhj',address,122880);assert n
  state=bytes(m.u.mem_read(address,n));assert struct.unpack_from('<I',state,4)[0]==2,'not HQ state'
  assert m.call('_Z9nes_framehPFivE',0,0)==0
  expected=[m.call(k) for k in ('_Z13fc_video_hashv','_Z13fc_audio_hashv','_Z10fc_samplesv')]
  m.u.mem_write(ram,b'\x00');m.u.mem_write(address,state)
  assert m.call('_Z13fc_state_loadPKhj',address,n)==1
  assert m.u.mem_read(ram,1)==b'\x5a'
  assert m.call('_Z9nes_framehPFivE',0,0)==0
  assert expected==[m.call(k) for k in ('_Z13fc_video_hashv','_Z13fc_audio_hashv','_Z10fc_samplesv')]
  print('PASS ARM trainer',mapper,hex(base),'CPU execution and HQ video/audio state replay',flush=True)
print('PASS Cortex-A9 instruction model; no physical timing claim')
