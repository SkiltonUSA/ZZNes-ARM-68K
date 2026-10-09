#include "platform.h"
#include "CPU.h"
#include "PPU.h"
#include "core.h"
#include "cartridge.h"
#include <assert.h>
#include <stdio.h>
extern Console *nes_test_console();
static uint8_t rom[1048592];static uint16_t pixels[2][61440];
static unsigned fixture(unsigned mapper,unsigned prg=8,unsigned chr=4){
 unsigned size=16+prg*16384+chr*8192;memset(rom,0,size);rom[0]='N';rom[1]='E';rom[2]='S';rom[3]=26;rom[4]=prg;rom[5]=chr;rom[6]=(mapper<<4)|(mapper==90?0:2);rom[7]=mapper&0xf0;
 for(unsigned i=0;i<prg*2;i++){memset(rom+16+i*8192,0xea,8192);rom[16+i*8192]=i;rom[16+i*8192+8190]=0;rom[16+i*8192+8191]=0xc1;rom[16+i*8192+8188]=0;rom[16+i*8192+8189]=0xc1;}
 for(unsigned i=0;i<chr*8;i++)memset(rom+16+prg*16384+i*1024,i,1024);
 assert(!nes_init(rom,size,pixels[0],pixels[1]));return size;
}
static void serial(uint16_t a,uint8_t v){auto c=nes_test_console();for(unsigned i=0;i<5;i++){c->cpu->Exec();c->memory.Write(a,v&1);v>>=1;}}
static void mapper90(){
 unsigned n=fixture(90,32,32);auto c=nes_test_console();auto &m=c->memory;auto p=c->mapper;
 assert(nes_cartridge(rom,n)==90);uint8_t *save;assert(nes_save(&save)==0);
 // Reset selects the last 32 KiB; low cartridge space is unmapped.
 assert(m.Read(0x8000)==60&&m.Read(0xe000)==63);m.openBus=0x76;assert(m.Read(0x6000)==0x76);
 m.Write(0x5800,19);m.Write(0x5801,23);assert(m.Read(0x5800)==(437&255)&&m.Read(0x5801)==1);
 m.Write(0x5803,0xa7);assert(m.Read(0x5ffb)==0xa7&&m.Read(0x5000)==0);m.openBus=0x65;assert(m.Read(0x5802)==0x65);
 // 32K, 16K, 8K and bit-reversed PRG modes, including fixed/switchable end.
 m.Write(0x8003,8);m.Write(0xd000,4);assert(m.Read(0x8000)==8&&m.Read(0xe000)==11);
 m.Write(0x8001,3);m.Write(0xd000,1);assert(m.Read(0x8000)==6&&m.Read(0xa000)==7&&m.Read(0xc000)==62);
 m.Write(0x8000,9);m.Write(0x8002,10);m.Write(0xd000,6);assert(m.Read(0x8000)==9&&m.Read(0xc000)==10&&m.Read(0xe000)==8);
 m.Write(0x8000,0x20);m.Write(0xd000,3);assert(m.Read(0x8000)==2&&m.Read(0xe000)==63);
 // PRG at $6000 is read-only; disabling it restores open bus.
 m.Write(0xd000,0x82);assert(m.Read(0x6000)==8);m.Write(0x6000,0xfe);assert(m.Read(0x6000)==8);
 m.Write(0xd000,2);m.openBus=0x55;assert(m.Read(0x6000)==0x55);
 // All CHR page granularities and modulo wrapping; mapper 90 has no NT-ROM.
 m.Write(0x9000,3);m.Write(0xd000,0);assert(p->ReadVRAM(0)==24&&p->ReadVRAM(0x1c00)==31);
 m.Write(0x9004,5);m.Write(0xd000,8);assert(p->ReadVRAM(0)==12&&p->ReadVRAM(0x1000)==20);
 m.Write(0x9002,7);m.Write(0xd000,16);assert(p->ReadVRAM(0)==6&&p->ReadVRAM(0x800)==14);
 m.Write(0xd000,24);assert(p->ReadVRAM(0)==3&&p->ReadVRAM(0x800)==7);
 m.Write(0xa000,1);assert(p->ReadVRAM(0)==3); // ROM size masks high bank bits.
 m.Write(0xd003,0);assert(p->ReadVRAM(0)==3);m.Write(0xd003,0x20);
 m.Write(0xd000,0x78);m.Write(0xd001,2);p->WriteVRAM(0x2000,0x4a);assert(p->ReadVRAM(0x2c00)==0x4a);
 // Test IRQ event sources independently, including non-rendering/debug reads.
 auto arm=[&](unsigned source,unsigned prescale=255,unsigned counter=255,unsigned direction=0x40){
  m.Write(0xc002,0);m.Write(0xc006,0);m.Write(0xc001,direction|source);m.Write(0xc004,prescale);m.Write(0xc005,counter);m.Write(0xc003,0);
  assert(!c->cpu->HasIrqSource(IRQSource::External));
 };
 arm(0);p->ProcessCpuClock();assert(c->cpu->HasIrqSource(IRQSource::External));
 arm(1);p->NotifyVRAMAddressChange(0);p->NotifyVRAMAddressChange(0x1000);assert(c->cpu->HasIrqSource(IRQSource::External));
 arm(2);p->DebugReadVRAM(0);p->ReadVRAM(0,MemoryOperationType::Read);assert(!c->cpu->HasIrqSource(IRQSource::External));p->ReadVRAM(0);assert(c->cpu->HasIrqSource(IRQSource::External));
 arm(0,1,0,0x80);p->ProcessCpuClock();assert(c->cpu->HasIrqSource(IRQSource::External)); // decrement underflow
 arm(0,7,255,0x44);p->ProcessCpuClock();assert(c->cpu->HasIrqSource(IRQSource::External)); // 3-bit prescaler
 arm(0,0,0);m.Write(0xc006,0xaa);m.Write(0xc004,0x55);m.Write(0xc005,0x55);p->ProcessCpuClock();assert(c->cpu->HasIrqSource(IRQSource::External));
 // CPU-write mode must see a real CPU bus-write cycle, not a host register poke.
 fixture(90,32,32);c=nes_test_console();auto &mem=c->memory;p=c->mapper;
 mem.Write(0xc001,0x43);mem.Write(0xc004,255);mem.Write(0xc005,255);mem.Write(0xc003,0);
 p->ProcessCpuClock();assert(!c->cpu->HasIrqSource(IRQSource::External));
 c->cpu->Exec();assert(!c->cpu->HasIrqSource(IRQSource::External)); // NOP read cycles
 // Install STA $0000 at the next instruction in the test-only backing ROM.
 for(unsigned bank=0;bank<64;bank++){rom[16+bank*8192+0x101]=0x8d;rom[16+bank*8192+0x102]=0;rom[16+bank*8192+0x103]=0;}
 c->cpu->Exec();assert(c->cpu->HasIrqSource(IRQSource::External));mem.Write(0xc002,0);assert(!c->cpu->HasIrqSource(IRQSource::External));
 rom[6]|=2;assert(nes_cartridge(rom,n)<0);rom[6]&=~2;rom[7]=0xd0;rom[6]=0x10;assert(nes_cartridge(rom,n)<0); // 209 stays unsupported
 puts("PASS mapper 90 PRG/CHR modes, registers/open bus, mirroring, read-only $6000, four IRQ sources, direction/prescaler/XOR, acknowledge, bounded header");
}
int main(){
 unsigned size=fixture(0,1,1);auto c=nes_test_console();assert(c->memory.Read(0x8000)==0&&c->memory.Read(0xc000)==0);
 uint8_t *save;assert(nes_save(&save)==8192);c->memory.Write(0x6123,0x5a);assert(save[0x123]==0x5a);
 uint8_t saved[8192];memcpy(saved,save,8192);assert(!nes_init(rom,size,pixels[0],pixels[1]));assert(nes_save(&save)==8192);memcpy(save,saved,8192);assert(nes_test_console()->memory.Read(0x6123)==0x5a);
 unsigned offsets[]={6,7,9};for(unsigned offset: offsets){uint8_t v=rom[offset];rom[offset]|=offset==6?4:offset==7?8:1;assert(nes_cartridge(rom,size)<0);rom[offset]=v;}
 assert(nes_cartridge(rom,size-1)<0);assert(nes_cartridge(rom,size+1)<0);
 fixture(2,8,0);c=nes_test_console();assert(c->memory.Read(0xc000)==14);c->memory.Write(0x8000,3);assert(c->memory.Read(0x8000)==6&&c->memory.Read(0xc000)==14);
 fixture(3,2,4);c=nes_test_console();c->memory.Write(0x8000,2);assert(c->mapper->ReadVRAM(0)==16);
 fixture(7,8,0);c=nes_test_console();c->memory.Write(0x8000,0x12);assert(c->memory.Read(0x8000)==8);c->mapper->WriteVRAM(0x2000,0x7b);assert(c->mapper->ReadVRAM(0x2c00)==0x7b);
 fixture(1,8,4);c=nes_test_console();assert(c->memory.Read(0xc000)==14);serial(0xe000,3);assert(c->memory.Read(0x8000)==6&&c->memory.Read(0xc000)==14);
 serial(0x8000,0x1f);serial(0xa000,2);serial(0xc000,5);assert(c->mapper->ReadVRAM(0)==8&&c->mapper->ReadVRAM(0x1000)==20);
 fixture(4,8,4);c=nes_test_console();c->memory.Write(0x8000,6);c->memory.Write(0x8001,5);assert(c->memory.Read(0x8000)==5&&c->memory.Read(0xe000)==15);
 c->memory.Write(0xa001,0x80);c->memory.Write(0x6000,123);assert(c->memory.Read(0x6000)==123);c->memory.Write(0xa001,0xc0);c->memory.Write(0x6000,5);assert(c->memory.Read(0x6000)==123);
 mapper90();
 puts("PASS cartridge rejection, mapper 0/1/2/3/4/7 banks, MMC1 serial/CHR, MMC3 WRAM protection, battery RAM round trip");
}
