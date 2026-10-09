"""Fail closed if high-BSS pointers are confused with firmware/shared storage."""
import sys,struct,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'amiga/fceux_bench'))
from elf import unpack
class ElfSafety(unittest.TestCase):
 def setUp(self):
  self.data=bytearray((ROOT/'.context/amiga/fceux-bench/fceux.elf').read_bytes())
  self.image,self.rel,self.entry=unpack(self.data)
  h=struct.unpack_from('<HHIIIIIHHHHHH',self.data,16)
  self.sections=[(h[5]+i*h[10],struct.unpack_from('<10I',self.data,h[5]+i*h[10])) for i in range(h[11])]
  self.off=next(struct.unpack_from('<8I',self.data,h[4]+i*h[8])[1] for i in range(h[9]) if struct.unpack_from('<I',self.data,h[4]+i*h[8])[0]==1)
 def test_reserved_targets_rejected(self):
  for target in [0x40000,0x60000,0x80000,0x100000,0x3d0000,0xf8f00200]:
   with self.subTest(target=hex(target)):
    data=self.data.copy();struct.pack_into('<I',data,self.off+self.rel[0],target)
    with self.assertRaises(ValueError):unpack(data)
 def test_bss_stack_overlap_rejected(self):
  at,s=next((at,s) for at,s in self.sections if s[1]==8)
  struct.pack_into('<I',self.data,at+20,0x1b0000)
  with self.assertRaises(ValueError):unpack(self.data)
 def test_nonrelative_rejected(self):
  _,s=next((at,s) for at,s in self.sections if s[1]==9)
  struct.pack_into('<I',self.data,s[4]+4,2)
  with self.assertRaises(ValueError):unpack(self.data)
 def test_outside_image_relocation_rejected(self):
  _,s=next((at,s) for at,s in self.sections if s[1]==9)
  struct.pack_into('<I',self.data,s[4],0x220000)
  with self.assertRaises(ValueError):unpack(self.data)
if __name__=='__main__':unittest.main()
