#!/usr/bin/env python3
"""Original GPL-3.0-or-later NROM: eight-phase horizontal-scrolling diagnostic and controller sprite.
Tiny purpose-built assembler; no commercial ROM or assets required.
"""
def build(player_test=False):
    code=bytearray();labels={};fix=[]
    def label(s):labels[s]=0x8000+len(code)
    def emit(*v):code.extend(v)
    def jump(op,s):emit(op,0,0);fix.append((len(code)-2,s,False))
    def branch(op,s):emit(op,0);fix.append((len(code)-1,s,True))
    def sta(a):emit(0x8d,a&255,a>>8)
    def lda(v):emit(0xa9,v)
    label('reset');emit(0x78,0xd8,0xa2,0xff,0x9a);lda(0);sta(0x2000);sta(0x2001)
    for s in ('wait1','wait2'):
        label(s);emit(0x2c,0x02,0x20);branch(0x10,s)
    # Hide all sprites, then reveal one patterned sprite at (120,112).
    emit(0xa2,0);lda(255);label('oam');emit(0x9d,0,2,0xe8);branch(0xd0,'oam')
    for addr,v in [(0x200,112),(0x201,2),(0x202,0),(0x203,120)]:lda(v);sta(addr)
    lda(0x3f);sta(0x2006);lda(0);sta(0x2006);emit(0xa2,0)
    label('pal');jump(0xbd,'palette');sta(0x2007);emit(0xe8,0xe0,32);branch(0xd0,'pal')
    lda(0x20);sta(0x2006);lda(0);sta(0x2006);emit(0xa0,4,0xa2,0)
    label('nametable');emit(0x8a,0x29,1);sta(0x2007);emit(0xe8);branch(0xd0,'nametable');emit(0x88);branch(0xd0,'nametable')
    # Clear attribute table after the 960 pattern cells.
    lda(0x23);sta(0x2006);lda(0xc0);sta(0x2006);emit(0xa2,64);lda(0)
    label('attrs');sta(0x2007);emit(0xca);branch(0xd0,'attrs')
    lda(0);sta(2);sta(0x2005);sta(0x2005);lda(0x80);sta(0x2000);lda(0x1e);sta(0x2001)
    if player_test:
        for addr,v in [(0x4017,0xc0),(0x4015,1),(0x4000,0xb3),(0x4001,0),(0x4002,0xfd),(0x4003,0x08)]:lda(v);sta(addr)
    label('idle');jump(0x4c,'idle')
    label('nmi');emit(0x48,0x8a,0x48,0x98,0x48)
    if player_test:emit(0xee,0x00,0x60) # persistent frame counter in battery RAM
    # Latch and serially shift A,B,Select,Start,Up,Down,Left,Right into zero page.
    lda(1);sta(0x4016);lda(0);sta(0x4016);sta(0);emit(0xa2,8)
    label('input');emit(0xad,0x16,0x40,0x4a,0x26,0,0xca);branch(0xd0,'input')
    for mask,op,addr,s in [(1,0xee,0x203,'right'),(2,0xce,0x203,'left'),(4,0xee,0x200,'down'),(8,0xce,0x200,'up')]:
        emit(0xa5,0,0x29,mask);branch(0xf0,s);emit(op,addr&255,addr>>8);label(s)
    lda(0);sta(0x2003);lda(2);sta(0x4014);emit(0xe6,2,0xa5,2,0x29,7);sta(0x2005);lda(0);sta(0x2005)
    emit(0x68,0xa8,0x68,0xaa,0x68,0x40)
    label('irq');emit(0x40)
    label('palette');emit(*([0x0f,0x12,0x21,0x30]*4+[0x0f,0x16,0x27,0x30]*4))
    for pos,s,rel in fix:
        addr=labels[s]
        if rel:
            delta=addr-(0x8000+pos+1);assert -128<=delta<128;code[pos]=delta&255
        else:code[pos:pos+2]=addr.to_bytes(2,'little')
    prg=code+bytes(16384-len(code));prg=bytearray(prg)
    for i,s in enumerate(['nmi','reset','irq']):prg[0x3ffa+i*2:0x3ffc+i*2]=labels[s].to_bytes(2,'little')
    chr=bytearray(8192)
    chr[0:16]=bytes([0x55,0xaa]*4+[0]*8)
    chr[16:32]=bytes([0xff]*8+[0xff,0x81,0x81,0x81,0x81,0x81,0x81,0xff])
    chr[32:48]=bytes([0x3c,0x7e,0xff,0xdb,0xff,0x7e,0x24,0x66]+[0]*8)
    return b'NES\x1a'+bytes([1,1,3 if player_test else 1,0])+bytes(8)+prg+chr
if __name__=='__main__':
    import sys
    from pathlib import Path
    Path(sys.argv[1]).write_bytes(build())
