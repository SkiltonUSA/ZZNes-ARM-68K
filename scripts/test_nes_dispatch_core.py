"""Exercise the linked startup-generated handlers at two runtime addresses."""
import argparse,struct
from pathlib import Path
from test_console_jit_core import Machine
p=argparse.ArgumentParser();p.add_argument('candidate',type=Path);a=p.parse_args()
# X6502 pinned ABI: counters/PC, A X Y S P PI, jammed, count/IRQ/DB/preexec.
ops=((6,7,0),(7,6,0),(6,8,0),(8,6,0),(9,7,0),(7,9,0),(7,7,1),(8,8,1),(7,7,-1),(8,8,-1))
cases=0
for base in (0x11000040,0x150020c0):
 m=Machine(a.candidate/'player/fceux.elf',a.candidate/'core/elf.py',48*1024**2,base)
 table=next(v for k,v in m.syms.items() if k.endswith('cj_nes_handlers'))
 for i,(src,dst,delta) in enumerate(ops):
  m.syms['test']=struct.unpack('<I',m.u.mem_read(table+i*4,4))[0]
  for value in range(256):
   for flags in (0,255,0x41,0x82):
    state=bytearray((j*37+value)&255 for j in range(32));state[src]=value;state[10]=flags
    expect=bytearray(state);v=(value+delta)&255;expect[dst]=v
    if i!=5:expect[10]=(flags&~0x82)|(v&0x80)|(2 if v==0 else 0)
    m.u.mem_write(m.syms['X'],bytes(state));m.call('test',m.syms['X'],0)
    assert m.u.mem_read(m.syms['X'],32)==expect,(base,i,value,flags)
    cases+=1
print('PASS',cases,'linked NES handler cases: relocated addresses, 8-bit wrap, NZ/TXS and complete CPU state')
