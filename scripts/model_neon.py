"""Unicorn A9 CPACR-read workaround used by existing presentation tests.
Only the modeled MRC result is corrected. No hardware register is changed.
"""
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R1, UC_ARM_REG_C1_C0_2, UC_ARM_REG_PC

def correct_cpacr_read(machine):
    address=machine.syms['db_neon_available']
    def read(uc,pc,*args):
        uc.reg_write(UC_ARM_REG_R1,uc.reg_read(UC_ARM_REG_C1_C0_2))
        uc.reg_write(UC_ARM_REG_PC,pc+4)
    machine.u.hook_add(UC_HOOK_CODE,read,begin=address,end=address)
