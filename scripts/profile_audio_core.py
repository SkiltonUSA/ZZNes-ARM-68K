#!/usr/bin/env python3
"""Count executed ARM-model instructions by function, not hardware cycles."""
import argparse,bisect,collections,subprocess
from pathlib import Path
from unicorn import UC_HOOK_BLOCK
from unicorn.arm_const import UC_ARM_REG_C1_C0_2, UC_ARM_REG_FPEXC
from test_console_jit_core import Machine

def main():
    p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('build',type=Path)
    p.add_argument('--warmup',type=int,default=120);p.add_argument('--frames',type=int,default=3)
    p.add_argument('--neon',action='store_true',help='Enable modeled VFP/NEON access; default profiles scalar fallback')
    a=p.parse_args();elf=a.build/'player/fceux.elf'
    m=Machine(elf,a.build/'core/elf.py',48*1024**2,0x11000040)
    if a.neon:
        from model_neon import correct_cpacr_read
        correct_cpacr_read(m)
        m.u.reg_write(UC_ARM_REG_C1_C0_2,0xf00000)
        m.u.reg_write(UC_ARM_REG_FPEXC,0x40000000)
        m.u.ctl_flush_tb()
    if a.neon:assert m.call("db_neon_available",m.base+0x80000)==1
    rom=a.rom.read_bytes();m.u.mem_write(m.base+0x100000,rom)
    assert m.call('_Z8nes_initPKhjPtS1_',m.base+0x100000,len(rom),m.base+0x90000,m.base+0xb0000)==0
    for _ in range(a.warmup):assert m.call('_Z9nes_framehPFivE',0,0)==0
    rows=[]
    for line in subprocess.check_output(['llvm-nm','-n','-S',elf],text=True).splitlines():
        fields=line.split()
        if len(fields)==4 and fields[2].lower()=='t':rows.append((m.base+int(fields[0],16),int(fields[1],16),fields[3]))
    starts=[r[0]for r in rows];counts=collections.Counter()
    def hit(u,address,size,data):
        i=bisect.bisect_right(starts,address)-1
        name=rows[i][2]if i>=0 and address<rows[i][0]+rows[i][1]else'generated/other'
        counts[name]+=size//4
    m.u.hook_add(UC_HOOK_BLOCK,hit);m.u.ctl_flush_tb()
    for _ in range(a.frames):assert m.call('_Z9nes_framehPFivE',0,0)==0
    total=sum(counts.values());assert total
    print('ARM-model instruction slots (not cycles):',total,'NEON enabled:',a.neon)
    for name,count in counts.most_common(16):print(f'{100*count/total:6.2f}% {count:10d} {name}')
if __name__=='__main__':main()
