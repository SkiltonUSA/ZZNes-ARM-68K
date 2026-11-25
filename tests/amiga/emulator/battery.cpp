/* Original mapper battery fixtures; contains no commercial ROM data. */
#include "platform.h"
#include "core.h"
#include "cartridge.h"
#include <cassert>
#include <vector>
#include <cstdlib>
#include <string>
extern unsigned fc_battery(uint8 **);
extern void fc_battery_loaded();
extern unsigned fc_state_store(uint8*,unsigned);
extern int fc_state_load(const uint8*,unsigned);
int main(int argc,char **argv){
 assert(argc==4);unsigned id=atoi(argv[1]),trainer=atoi(argv[2]);const char*base=argv[3];
 unsigned prg=131072,chr=32768,payload=16+(trainer?512:0);
 std::vector<uint8> rom(payload+prg+chr,0);memcpy(rom.data(),"NES\x1a",4);rom[4]=prg/16384;rom[5]=chr/8192;rom[6]=(id<<4)|2|(trainer?4:0);rom[7]=id&240;
 assert(nes_cartridge(rom.data(),rom.size())==int(id));
 // Keep every other header constraint valid so battery rejection is isolated.
 for(unsigned denied: {0u,2u,3u,78u,90u}){
  std::vector<uint8> bad(16+32768+8192,0);memcpy(bad.data(),"NES\x1a",4);
  bad[4]=2;bad[5]=1;bad[6]=denied<<4;bad[7]=denied&240;
  assert(nes_cartridge(bad.data(),bad.size())==int(denied));
  bad[6]|=2;assert(nes_cartridge(bad.data(),bad.size())<0);
 }
 if(trainer)for(unsigned i=0;i<512;i++)rom[16+i]=(i*29+11)&255;
 // Disable interrupts/rendering; configure MMC5/MMC3 RAM; record previous
 // battery counter in CPU RAM, then increment it once per cold launch.
 const uint8 code[]={0x78,0xd8,0xa2,0xff,0x9a,0xa9,0,0x8d,0,0x20,0x8d,1,0x20,
  0xa9,2,0x8d,2,0x51,0xa9,1,0x8d,3,0x51,0xa9,0,0x8d,0x13,0x51,
  0xa9,0x80,0x8d,1,0xa0,0xad,0,0x60,0x85,0,0xee,0,0x60,0xa9,0x5a,0x8d,1,0x60,0x4c,46,0x80};
 for(unsigned bank=0;bank<prg/8192;bank++){
  memcpy(rom.data()+payload+bank*8192,code,sizeof code);
  for(unsigned v=0x1ffa;v<=0x1ffe;v+=2){rom[payload+bank*8192+v]=0;rom[payload+bank*8192+v+1]=0x80;}
 }
 FILE*f=fopen((std::string(base)+".nes").c_str(),"wb");assert(f);assert(fwrite(rom.data(),1,rom.size(),f)==rom.size());assert(!fclose(f));
 auto original=rom;assert(!fc_init(rom.data(),rom.size()));uint8 *ram;unsigned n=fc_battery(&ram);assert(n==(id==5?32768u:8192u)&&ram);
 // Import distinctive bytes in every persistent bank; then follow host ordering.
 for(unsigned i=0;i<n;i++)ram[i]=(i*7+(i>>8)+17)&255;
 fc_battery_loaded();
 if(trainer)for(unsigned i=0;i<512;i++)assert(ARead[0x7000+i](0x7000+i)==rom[16+i]);
 for(unsigned i=0;i<3;i++)assert(!fc_frame(0));
 assert(RAM[0]==17&&ram[0]==18&&ram[1]==0x5a);
 if(id==5){for(unsigned b=0;b<4;b++){BWrite[0x5113](0x5113,b);BWrite[0x6100](0x6100,0x60+b);assert(ram[b*8192+256]==0x60+b);}BWrite[0x5113](0x5113,0);}
 std::vector<uint8> saved(ram,ram+n),state(122880);unsigned count=fc_state_store(state.data(),state.size());assert(count);
 memset(ram,0xcc,n);assert(fc_state_load(state.data(),count));assert(!memcmp(ram,saved.data(),n));
 assert(rom==original);
 f=fopen((std::string(base)+".sav").c_str(),"wb");assert(f);assert(fwrite(ram,1,n,f)==n);assert(!fclose(f));
 printf("PASS mapper %u battery %u bytes trainer=%u: bank writes, power/import ordering, guest execution and state restoration\n",id,n,trainer);
}
