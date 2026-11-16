#!/usr/bin/env python3
"""Compare linked ARM32 state/PCM and instruction slots; not hardware cycles."""
import json,os,struct,subprocess,tempfile
from pathlib import Path
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_BLOCK
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_CPU_ARM_CORTEX_A9
HERE=Path(__file__).resolve().parent
LLVM=Path(os.environ.get('LLVM_BIN','/opt/homebrew/opt/llvm/bin'))
with tempfile.TemporaryDirectory() as d:
 d=Path(d);elf=d/'noise.elf';binary=d/'noise.bin'
 subprocess.run([str(LLVM/'clang'),'--target=arm-none-eabi','-mcpu=cortex-a9','-marm','-mfloat-abi=soft','-O3','-fPIC','-fwrapv','-mno-unaligned-access','-fno-builtin','-ffreestanding','-nostdlib','-fuse-ld=lld','-Wl,-Ttext=0x10000','-Wl,-e,noise_candidate','-I'+str(HERE.parent/'noise-spans-20261111'),str(HERE/'arm_fixture.c'),'-o',str(elf)],check=True)
 subprocess.run([str(LLVM/'llvm-objcopy'),'-O','binary',str(elf),str(binary)],check=True)
 symbols={}
 for line in subprocess.check_output([str(LLVM/'llvm-nm'),str(elf)],text=True).splitlines():
  fields=line.split()
  if len(fields)==3 and fields[2] in ('noise_reference','noise_candidate'):symbols[fields[2]]=int(fields[0],16)
 u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.ctl_set_cpu_model(UC_CPU_ARM_CORTEX_A9);u.mem_map(0x10000,(len(binary.read_bytes())+4095)&~4095);u.mem_write(0x10000,binary.read_bytes());u.mem_map(0x200000,0x80000);u.mem_map(0x300000,0x10000);u.mem_map(0x400000,0x1000)
 slots=[0]
 def hit(u,address,size,_):slots[0]+=size//4
 u.hook_add(UC_HOOK_BLOCK,hit)
 def run(name,data):
  u.mem_write(0x200000,data);u.reg_write(UC_ARM_REG_R0,0x200000);u.reg_write(UC_ARM_REG_SP,0x30fff0);u.reg_write(UC_ARM_REG_LR,0x400000);slots[0]=0
  u.emu_start(symbols[name],0x400000,count=10000000)
  assert u.reg_read(UC_ARM_REG_PC)==0x400000,name
  return bytes(u.mem_read(0x200000,len(data))),slots[0]
 results=[]
 for count in (0,1,128,1024,32768,65535):
  for period in (4,96,4068):
   for tap in (8,13):
    for amplitude in (0,15<<16):
     data=struct.pack('<IIIIiHH',count,amplitude,period,tap,period//2,0x5a35,0x1234)+b'\x21\x32\x43\x54'*(65538)
     a,ref=run('noise_reference',data);b,opt=run('noise_candidate',data);assert a==b,(count,period,tap,amplitude)
     results.append(dict(count=count,period=period,tap=tap,amplitude=amplitude,reference_slots=ref,candidate_slots=opt))
 print(json.dumps(dict(scope='Linked Cortex-A9 ARM32 model instruction slots, not cycles or hardware speed',cases=results),indent=2))
 print('PASS 72 linked ARM32 sample/state comparisons')
