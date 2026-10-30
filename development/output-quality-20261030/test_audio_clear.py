"""Bounded word clearing, including empty ranges and non-16-byte alignment."""
from pathlib import Path
import subprocess,tempfile
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM
from unicorn.arm_const import *
ROOT=Path(__file__).resolve().parents[2]
def main():
    with tempfile.TemporaryDirectory() as tmp:
        obj=Path(tmp)/'clear.o';raw=Path(tmp)/'clear.bin'
        subprocess.run(['clang','--target=arm-none-eabi','-mcpu=cortex-a9','-c',ROOT/'development/output-quality-20261030/audio_clear.S','-o',obj],check=True)
        subprocess.run(['/opt/homebrew/opt/llvm/bin/llvm-objcopy','-O','binary','--only-section=.text',obj,raw],check=True)
        u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.mem_map(0x10000000,4096);u.mem_write(0x10000000,raw.read_bytes());u.mem_map(0x11000000,0x30000)
        for n in [*range(68),39515,40000]:
            for offset in range(0,16,4):
                p=0x11000020+offset;stop=0x10000ffc
                u.mem_write(p-16,b'\xa5'*(n*4+32))
                u.reg_write(UC_ARM_REG_R0,p);u.reg_write(UC_ARM_REG_R1,n)
                u.reg_write(UC_ARM_REG_SP,0x1102fff0);u.reg_write(UC_ARM_REG_LR,stop)
                for r in range(UC_ARM_REG_R4,UC_ARM_REG_R11+1):u.reg_write(r,0x12345678)
                u.emu_start(0x10000000,stop,count=100000)
                assert u.reg_read(UC_ARM_REG_PC)==stop
                assert bytes(u.mem_read(p-16,n*4+32))==b'\xa5'*16+bytes(n*4)+b'\xa5'*16,(n,offset)
                assert u.reg_read(UC_ARM_REG_SP)==0x1102fff0
                assert all(u.reg_read(r)==0x12345678 for r in range(UC_ARM_REG_R4,UC_ARM_REG_R11+1))
    print('PASS 280 clear ranges: exact writes, adjacent canaries, empty range, alignment and ABI')
if __name__=='__main__':main()
