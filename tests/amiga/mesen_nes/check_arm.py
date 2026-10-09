#!/usr/bin/env python3
"""CPU+PPU ARM instruction-model check. Does not model physical MMU/cache/RTG."""
from pathlib import Path
import struct,subprocess,sys,json
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_CORTEX_A9,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from build_zz9000_debug import unpack_elf
base=0x12000040;out=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'.context/amiga/mesen-nes'
player=json.loads((out/'build.json').read_text()).get('player',False)
rom_offset=0x100000 if player else 0x70000
block=0x400000 if player else 0x100000
image,rel,_=unpack_elf((out/'nes.elf').read_bytes(),0x40000)
for offset in rel:struct.pack_into('<I',image,offset,struct.unpack_from('<I',image,offset)[0]+base)
symbols={p[2]:int(p[0],16)+base for line in subprocess.check_output(['/opt/homebrew/opt/llvm/bin/llvm-nm',out/'nes.elf'],text=True).splitlines() if len(p:=line.split())==3}
u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.ctl_set_cpu_model(UC_CPU_ARM_CORTEX_A9);u.mem_map(base&~4095,block+0x2000);u.mem_write(base,bytes(image))
rom=(out/'ZZNesDemo.nes').read_bytes();u.mem_write(base+rom_offset,rom)
def access(u,kind,address,size,value,user):
 if size>1 and address%size:raise AssertionError(f'unaligned {address:x} size={size} PC={u.reg_read(UC_ARM_REG_PC):x}')
u.hook_add(UC_HOOK_MEM_READ|UC_HOOK_MEM_WRITE,access)
def call(symbol,*args):
 u.reg_write(UC_ARM_REG_SP,base+block-16);u.reg_write(UC_ARM_REG_LR,base+0xf0000)
 for r,v in zip([UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3],args):u.reg_write(r,v)
 for i,v in enumerate(args[4:]):u.mem_write(base+block-16+i*4,struct.pack('<I',v))
 u.emu_start(symbols[symbol],base+0xf0000,count=50000000)
 assert u.reg_read(UC_ARM_REG_PC)==base+0xf0000,(symbol,hex(u.reg_read(UC_ARM_REG_PC)))
 return u.reg_read(UC_ARM_REG_R0)
assert call('_Z8nes_initPKhjPtS1_',base+rom_offset,len(rom),base+0x90000,base+0xb0000)==0
for i in range(6):
 assert call('_Z9nes_framehPFivE',0,0)==0
 actual=call('_Z8nes_hashv')
 assert actual==[0x48ef4dc5,0x48ef4dc5,0xd8cc1f38,0xed354ee5,0xed354ee5,0xed354ee5][i]
 print('ARM_MODEL frame',i+1,'hash',f"{actual:08x}",flush=True)
assert call('_Z8nes_hashv')==0xed354ee5
print('PASS relocated ARM CPU+PPU complete-frame hash matches native; aligned data accesses')
if 'nes_present' in symbols:
 # Model the temporary table contents and actual ARM pixel stores; Unicorn
 # flat memory does NOT validate physical translation, coherence or P96.
 addr=0x02fff800;mapping=addr&~4095;capacity=0x100000
 u.mem_map(mapping,capacity)
 l1=(base+0x40000+16383)&~16383
 u.mem_write(l1,bytes(16384+8192));u.mem_write(base+0x82000+15*4,struct.pack('<I',l1))
 source=call('_Z10nes_pixelsv')
 palette=[int(x,16) for x in __import__('re').findall(r'0x([0-9a-fA-F]{8})',(ROOT/'amiga/mesen_nes/palette.h').read_text())]
 raw=struct.unpack('<61440H',u.mem_read(source,61440*2))
 for fmt in range(1,5):
  bpp=3 if fmt<3 else 4;pitch=256*bpp+16;span=239*pitch+256*bpp
  expected=bytearray(b'\xa5'*capacity)
  nonce=0x97ab301d
  u.mem_write(mapping,bytes(expected))
  u.mem_write(addr,struct.pack('>I',nonce));u.mem_write(addr+span-4,struct.pack('>I',nonce^0x31415926))
  # A bad challenge must not alter any target memory or retain mappings.
  before=bytes(u.mem_read(mapping,capacity))
  assert call('nes_present',base,addr,pitch,fmt,nonce+1)==7
  assert bytes(u.mem_read(mapping,capacity))==before
  assert bytes(u.mem_read(l1,16384))==bytes(16384)
  assert call('nes_present',base,addr,pitch,fmt,nonce)==0
  for i,v in enumerate(raw):
   c=palette[v&63];r=(c>>16)&255;g=(c>>8)&255;b=c&255
   color=[(r,g,b),(b,g,r),(b,g,r,255),(255,r,g,b)][fmt-1]
   offset=addr-mapping+(i//256)*pitch+(i%256)*bpp
   expected[offset:offset+bpp]=bytes(color)
  assert bytes(u.mem_read(mapping,capacity))==expected
  assert bytes(u.mem_read(l1,16384))==bytes(16384)
  # Stop before copying retains challenge bytes and revokes the map.
  u.mem_write(addr,struct.pack('>I',nonce));u.mem_write(addr+span-4,struct.pack('>I',nonce^0x31415926))
  before=bytes(u.mem_read(mapping,capacity));u.mem_write(base+0x80080,struct.pack('>I',1))
  assert call('nes_present',base,addr,pitch,fmt,nonce)==2
  assert bytes(u.mem_read(mapping,capacity))==before
  assert bytes(u.mem_read(l1,16384))==bytes(16384)
  u.mem_write(base+0x80080,bytes(4))
 print('PASS ARM presentation: four formats, both-end challenges, guard/padding bytes, cancellation, mapping revocation')
