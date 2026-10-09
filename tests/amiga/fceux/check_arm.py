#!/usr/bin/env python3
"""Relocated A9 instruction model, not a physical MMU/cache test."""
from pathlib import Path
import struct,subprocess,sys
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_CORTEX_A9,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'amiga/fceux_bench'))
from elf import unpack
out=ROOT/'.context/amiga/fceux-bench';base=0x12000040;block=0x400000
image,rel,_=unpack((out/'fceux.elf').read_bytes())
for offset in rel:struct.pack_into('<I',image,offset,struct.unpack_from('<I',image,offset)[0]+base)
symbols={p[2]:int(p[0],16)+base for line in subprocess.check_output(['/opt/homebrew/opt/llvm/bin/llvm-nm',out/'fceux.elf'],text=True).splitlines() if len(p:=line.split())==3}
u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.ctl_set_cpu_model(UC_CPU_ARM_CORTEX_A9);u.mem_map(base&~4095,block+0x2000);u.mem_write(base,bytes(image))
rom=Path(sys.argv[1]).read_bytes();u.mem_write(base+0x100000,rom)
def access(u,kind,address,size,value,user):
 if size>1 and address%size:raise AssertionError(f'unaligned {address:x} size={size} PC={u.reg_read(UC_ARM_REG_PC):x}')
u.hook_add(UC_HOOK_MEM_READ|UC_HOOK_MEM_WRITE,access)
def call(symbol,*args):
 u.reg_write(UC_ARM_REG_SP,base+block-4096-16);u.reg_write(UC_ARM_REG_LR,base+0xf0000)
 for r,v in zip([UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3],args):u.reg_write(r,v)
 u.emu_start(symbols[symbol],base+0xf0000,count=50000000)
 assert u.reg_read(UC_ARM_REG_PC)==base+0xf0000,(symbol,hex(u.reg_read(UC_ARM_REG_PC)))
 return u.reg_read(UC_ARM_REG_R0)
assert call('_Z7fc_initPKhj',base+0x100000,len(rom))==0
native=subprocess.check_output([out/'native-fixed',sys.argv[1],sys.argv[2]],text=True).splitlines()
for i in range(int(sys.argv[2])):
 assert call('_Z8fc_frameh',0)==0
 actual=f'FRAME n={i+1} cycles={call("_Z9fc_cyclesv")} video={call("_Z13fc_video_hashv"):08x} audio={call("_Z13fc_audio_hashv"):08x} samples={call("_Z10fc_samplesv")} nonzero={call("_Z10fc_nonzerov")}'
 assert actual==native[i],(actual,native[i]);print(actual,flush=True)
print('PASS ARM model/native cycles, pixels/emphasis, PCM and sample counts; aligned data access')
