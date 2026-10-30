"""Exact ARM SIMD FIR arithmetic, bounds and ABI; no hardware required."""
from pathlib import Path
import random,struct,subprocess,tempfile
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM
from unicorn.arm_const import *
ROOT=Path(__file__).resolve().parents[2]
def signed(v):
    return (v & 0x7fffffff)-(v & 0x80000000)
def oracle(samples,coeffs):
    n=len(coeffs)
    return [sum(signed(samples[n-i+k]*c)>>6 for i,c in enumerate(coeffs))&0xffffffff for k in (0,1)]
def main():
    with tempfile.TemporaryDirectory() as tmp:
        obj=Path(tmp)/'fir.o';raw=Path(tmp)/'fir.bin'
        subprocess.run(['clang','--target=arm-none-eabi','-mcpu=cortex-a9','-c',ROOT/'development/output-quality-20261030/audio_fir_neon.S','-o',obj],check=True)
        subprocess.run(['/opt/homebrew/opt/llvm/bin/llvm-objcopy','-O','binary','--only-section=.text',obj,raw],check=True)
        rng=random.Random(1030);cases=0
        for base in (0x11000000,0x15002000):
            u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.ctl_set_cpu_model(UC_CPU_ARM_CORTEX_A9)
            u.mem_map(base,4096);u.mem_write(base,raw.read_bytes())
            u.mem_map(base+0x10000,16384);u.mem_map(base+0x20000,8192)
            u.mem_map(base+0x30000,4096)
            u.reg_write(UC_ARM_REG_C1_C0_2,0xf00000);u.ctl_flush_tb();u.reg_write(UC_ARM_REG_FPEXC,0x40000000)
            for n in (4,8,484,668,1024):
                for pattern in range(20):
                    # End at a guard page: the final sample must never be overread.
                    start=base+0x14000-(n+2)*4
                    samples=[rng.getrandbits(32) if pattern%2 else rng.randrange(32768) for _ in range(n+2)]
                    coeffs=[rng.getrandbits(32) if pattern%2 else rng.randrange(-100000,100000) & 0xffffffff for _ in range(n)]
                    u.mem_write(start,struct.pack('<'+'I'*len(samples),*samples));u.mem_write(base+0x20000,struct.pack('<'+'I'*n,*coeffs))
                    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
                    for r in regs:u.reg_write(r,0x12345678)
                    for r in range(UC_ARM_REG_D8,UC_ARM_REG_D15+1):u.reg_write(r,0x0123456789abcdef)
                    for r,v in [(UC_ARM_REG_R0,start+n*4),(UC_ARM_REG_R1,base+0x20000),(UC_ARM_REG_R2,n),(UC_ARM_REG_R3,base+0x30000),(UC_ARM_REG_LR,base+0xffc)]:u.reg_write(r,v)
                    u.emu_start(base,base+0xffc,count=100000)
                    assert u.reg_read(UC_ARM_REG_PC)==base+0xffc
                    assert list(struct.unpack('<II',u.mem_read(base+0x30000,8)))==oracle(samples,coeffs),(n,pattern)
                    assert all(u.reg_read(r)==0x12345678 for r in regs)
                    assert all(u.reg_read(r)==0x0123456789abcdef for r in range(UC_ARM_REG_D8,UC_ARM_REG_D15+1))
                    cases+=1
    print(f'PASS {cases} FIR cases: exact wrap/multiply/shift/sum, guard bounds, relocations and preserved registers')
if __name__=='__main__':main()
