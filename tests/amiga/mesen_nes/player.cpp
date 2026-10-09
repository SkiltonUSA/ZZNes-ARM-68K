#include "platform.h"
#include "CPU.h"
#include "PPU.h"
#include "core.h"
#include "cartridge.h"
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
extern Console *nes_test_console();
static uint16_t pixels[2][61440];
static uint8_t rom[1048593];
int main(int argc,char **argv){
 assert(argc==2);FILE *f=fopen(argv[1],"rb");assert(f);unsigned size=fread(rom,1,sizeof(rom),f);fclose(f);
 if(nes_init(rom,size,pixels[0],pixels[1])){fprintf(stderr,"Rejected %s\n",argv[1]);return 1;}
 bool started=false;unsigned samples=0;int low=32767,high=-32768;
 for(unsigned frame=0;frame<600;frame++){
  assert(!nes_frame(0,nullptr));const int16_t *p;unsigned n=nes_audio(&p);assert(n>0&&n<600);samples+=n;
  for(unsigned i=0;i<n;i++){if(p[i]<low)low=p[i];if(p[i]>high)high=p[i];}
  auto &m=nes_test_console()->memory;
  if(m.Read(0x6001)==0xde&&m.Read(0x6002)==0xb0&&m.Read(0x6003)==0x61){
   unsigned result=m.Read(0x6000);if(result==0x80)started=true;
   if(started&&result<0x80){printf("%s result=%u frames=%u samples=%u range=%d..%d\n",argv[1],result,frame+1,samples,low,high);for(unsigned a=0x6004;a<0x7000;a++){char c=m.Read(a);if(!c)break;putchar(c);}puts("");return result?1:0;}
  }
 }
 char text[1025];for(unsigned i=0;i<1024;i++)text[i]=(char)nes_test_console()->mapper->DebugReadVRAM(0x2000+i);text[1024]=0;
 for(unsigned i=0;i<1024;i++)if(text[i]<32||text[i]>126)text[i]=' ';
 if(strstr(argv[1],"mmc3_test_2/")&&strstr(text,"Passed")&&!strstr(text,"Failed")){printf("%s PASS via PPU nametable (600 frames); MMC3 WRAM disabled by fixture\n",argv[1]);return 0;}
 printf("NAMETABLE %s\n",text);
 fprintf(stderr,"Test timed out: %s\n",argv[1]);return 2;
}
