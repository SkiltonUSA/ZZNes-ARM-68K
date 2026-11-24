// Original synthetic iNES fixtures, no commercial ROM data.
#include "platform.h"
#include "core.h"
#include "cartridge.h"
#include <cassert>
#include <vector>
#include <cstdlib>
extern unsigned fc_state_store(uint8*,unsigned);
extern int fc_state_load(const uint8*,unsigned);
int main(int argc,char**argv){
 assert(argc==2||argc==3);unsigned id=atoi(argv[1]);
 unsigned prg=id==0||id==3?32768:131072,chr=id==0?8192:32768;
 std::vector<uint8> rom(16+512+prg+chr,0);
 memcpy(rom.data(),"NES\x1a",4);rom[4]=prg/16384;rom[5]=chr/8192;
 rom[6]=((id&15)<<4)|4;rom[7]=id&240;
 assert(nes_cartridge(rom.data(),rom.size())==int(id));
 assert(nes_cartridge(rom.data(),rom.size()-1)<0);
 assert(nes_cartridge(rom.data(),rom.size()-512)<0);
 assert(nes_cartridge(rom.data(),rom.size()+1)<0);
 rom[6]|=2;assert(nes_cartridge(rom.data(),rom.size())<0);rom[6]&=~2;
 rom[7]|=8;assert(nes_cartridge(rom.data(),rom.size())<0);rom[7]&=~8;
 for(unsigned i=0;i<512;i++)rom[16+i]=(i*29+11)&255;
 const uint8 trainer[]={0xa9,0x5a,0x85,0,0x60}; // LDA #$5A / STA $00 / RTS
 memcpy(rom.data()+16,trainer,sizeof trainer);
 const uint8 program[]={0x78,0xd8,0xa2,0xff,0x9a,0x20,0,0x70,0x4c,8,0x80};
 for(unsigned bank=0;bank<prg/8192;bank++){
  memcpy(rom.data()+528+bank*8192,program,sizeof program);
  for(unsigned v=0x1ffa;v<=0x1ffe;v+=2){rom[528+bank*8192+v]=0;rom[528+bank*8192+v+1]=0x80;}
 }
 for(unsigned i=0;i<chr;i++)rom[528+prg+i]=(i/1024+0x71)&255;
 if(argc==3){FILE*f=fopen(argv[2],"wb");assert(f);assert(fwrite(rom.data(),1,rom.size(),f)==rom.size());assert(!fclose(f));}
 auto original=rom;
 assert(!fc_init(rom.data(),rom.size()));
 for(unsigned i=0;i<512;i++)assert(ARead[0x7000+i](0x7000+i)==rom[16+i]);
 assert(ARead[0x8000](0x8000)==program[0]);assert(VPageR[0][0]>=0x71&&VPageR[0][0]<0x91);
 for(unsigned n=0;n<3;n++)assert(!fc_frame(0));assert(RAM[0]==0x5a);
 // Writable mapper RAM stays writable; fallback trainers remain readable.
 BWrite[0x71ff](0x71ff,0x35);unsigned byte=ARead[0x71ff](0x71ff);
 assert(byte==0x35||byte==rom[16+511]);
 std::vector<uint8> state(122880);unsigned bytes=fc_state_store(state.data(),state.size());assert(bytes);
 BWrite[0x71ff](0x71ff,0x67);RAM[0]=0;
 assert(fc_state_load(state.data(),bytes));assert(RAM[0]==0x5a);
 assert(ARead[0x71ff](0x71ff)==byte);assert(!fc_frame(0));
 assert(rom==original);
 printf("PASS mapper %u trainer: 512-byte load, CPU execution, PRG/CHR offsets, state restore, unchanged input; invalid headers rejected\n",id);
}
