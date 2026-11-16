#!/usr/bin/env python3
"""Generate an original NROM fixture alternating muted/audible noise and taps."""
import struct,sys
code=bytearray.fromhex('78 d8 a2 ff 9a')
def store(address,value):code.extend([0xa9,value,0x8d,address&255,address>>8])
store(0x2000,0);store(0x2001,0);store(0x4015,8)
store(0x400c,0x30);store(0x400e,3);store(0x400f,0xf8)
code.extend([0xa9,3,0x85,0])
loop=0xc000+len(code)
# Fixed volume zero, then fifteen, with independent timer progress between writes.
for volume in (0x30,0x3f):
 store(0x400c,volume)
 code.extend(bytes.fromhex('a2 ff ca d0 fd'))
code.extend(bytes.fromhex('a5 00 49 80 85 00 8d 0e 40'))
code.extend([0x4c,loop&255,loop>>8])
prg=bytearray(16384);prg[:len(code)]=code
prg[-6:]=struct.pack('<HHH',0xc000,0xc000,0xc000)
sys.stdout.buffer.write(b'NES\x1a\x01\x01'+bytes(10)+prg+bytes(8192))
