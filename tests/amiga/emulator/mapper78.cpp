// Original synthetic cartridge, no commercial ROM data.
#include "platform.h"
#include "core.h"
#include "cartridge.h"
#include <cassert>
#include <vector>
extern unsigned fc_state_store(uint8*,unsigned);
extern int fc_state_load(const uint8*,unsigned);
static void mirroring(bool hv,unsigned v){
 if(hv){assert(vnapage[0]==vnapage[(v&8)?2:1]);assert(vnapage[0]!=vnapage[(v&8)?1:2]);}
 else for(unsigned i=1;i<4;i++)assert(vnapage[i]==vnapage[0]);
}
int main(int argc,char**argv){
 bool cn=argc==2&&argv[1][0]=='3';
 if(cn){
  std::vector<uint8>r(16+32768+32768,0xff);memset(r.data(),0,16);memcpy(r.data(),"NES\x1a",4);r[4]=2;r[5]=4;r[6]=0x31;
  for(unsigned i=0;i<4;i++)r[16+32768+i*8192]=i;
  memcpy(r.data()+7,"DiskDude!",9);assert(nes_cartridge(r.data(),r.size())==3);assert(!fc_rom_pal(r.data(),r.size(),"Cybernoid.nes"));
  r[15]^=1;assert(nes_cartridge(r.data(),r.size())<0);r[15]^=1;
  assert(!fc_init(r.data(),r.size()));
  for(unsigned v=0;v<256;v++){BWrite[0x8001](0x8001,v);assert(VPageR[0][0]==(v&3));assert(vnapage[0]==vnapage[2]&&vnapage[0]!=vnapage[1]);}
  r[16+2]=1;BWrite[0x8002](0x8002,3);assert(VPageR[0][0]==1);
  std::vector<uint8>state(122880);unsigned n=fc_state_store(state.data(),state.size());assert(n);BWrite[0x8001](0x8001,2);assert(fc_state_load(state.data(),n)&&VPageR[0][0]==1);
  assert(!memcmp(r.data()+7,"DiskDude!",9));puts("PASS CNROM: CHR banks, bus conflict, fixed mirroring, state, DiskDude recognition and unmodified ROM");return 0;
 }
 bool hv=argc==2&&argv[1][0]=='h';
 std::vector<uint8> r(16+131072+131072,0xff);
 memset(r.data(),0,16);memcpy(r.data(),"NES\x1a",4);r[4]=8;r[5]=16;r[6]=0xe0|(hv?8:0);r[7]=0x40;
 for(unsigned i=0;i<8;i++)r[16+i*16384]=i;
 for(unsigned i=0;i<16;i++)r[16+131072+i*8192]=i;
 assert(nes_cartridge(r.data(),r.size())==78);
 for(unsigned bad:{2u,4u}){r[6]|=bad;assert(nes_cartridge(r.data(),r.size())<0);r[6]&=~bad;}
 assert(nes_cartridge(r.data(),r.size()-1)<0);
 assert(!fc_init(r.data(),r.size()));mirroring(hv,0);
 for(unsigned v=0;v<256;v++){
  BWrite[0x8001](0x8001,v);assert(ARead[0x8000](0x8000)==(v&7));assert(ARead[0xc000](0xc000)==7);assert(VPageR[0][0]==v>>4);mirroring(hv,v);
 }
 // Writes contend with ROM data before banking changes.
 r[16+7*16384+2]=0x15;BWrite[0xc002](0xc002,0xff);
 assert(ARead[0x8000](0x8000)==5&&VPageR[0][0]==1);mirroring(hv,0x15);
 BWrite[0x8001](0x8001,0xab);std::vector<uint8> state(122880);unsigned size=fc_state_store(state.data(),state.size());assert(size);
 BWrite[0x8001](0x8001,0x24);assert(fc_state_load(state.data(),size));
 assert(ARead[0x8000](0x8000)==3&&VPageR[0][0]==10);mirroring(hv,0xab);
 printf("PASS mapper78 %s: all 256 banks/mirror values, fixed bank, bus conflicts and state restore\n",hv?"Holy Diver":"Cosmo Carrier");
}
