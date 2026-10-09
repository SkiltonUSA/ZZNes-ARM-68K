// GPL-3.0-or-later. Optional private-ROM smoke run; ROM bytes are never bundled.
#include "core.h"
#include "platform.h"
#include "cartridge.h"
#include "player_palette.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
static uint8_t rom[1048593];static uint16_t pixels[2][61440];
static int cancel(){return 1;}
int main(int argc,char **argv){
 assert(argc>=2&&argc<=3);FILE *f=fopen(argv[1],"rb");assert(f);unsigned size=fread(rom,1,sizeof(rom),f);assert(!ferror(f));fclose(f);
 printf("ROM bytes=%u mapper=%d\n",size,nes_cartridge(rom,size));assert(!nes_init(rom,size,pixels[0],pixels[1]));
 unsigned audio=0,changed=0;uint32_t last=0,pcmHash=2166136261u,frameHash=2166136261u;
 for(unsigned i=1;i<=900;i++){
  uint8_t keys=((i>=181&&i<=192)||(i>=421&&i<=432))?8:(i>=541&&i<=552)?1:(i>=601&&i<=720)?128:0;
  assert(!nes_frame(keys,nullptr));const int16_t *pcm;unsigned samples=nes_audio(&pcm);assert(samples&&samples<600);audio+=samples;for(unsigned j=0;j<samples;j++)pcmHash=(pcmHash^(uint16_t)pcm[j])*16777619u;
  unsigned colors[512]={};for(unsigned p=0;p<61440;p++){assert(nes_pixels()[p]<512);colors[nes_pixels()[p]]++;}
  unsigned distinct=0;for(unsigned n:colors)distinct+=n!=0;
  uint32_t h=nes_hash();changed+=i>1&&h!=last;last=h;frameHash=(frameHash^h)*16777619u;
  if(i==1||i%60==0)printf("FRAME n=%u cycles=%u hash=%08x colors=%u audio=%u\n",i,nes_cycles(),h,distinct,audio);
 }
 printf("TRACE frames=%08x pcm=%08x\n",frameHash,pcmHash);
 assert(changed>10);assert(nes_frame(0,cancel)==2);printf("PASS 900 frames, input sequence, cancellation; changed_frames=%u\n",changed);
 if(argc==3){f=fopen(argv[2],"wb");assert(f);fprintf(f,"P6\n256 240\n255\n");for(unsigned i=0;i<61440;i++){uint32_t color=nes_player_palette[nes_pixels()[i]];uint8_t rgb[3]={(uint8_t)(color>>16),(uint8_t)(color>>8),(uint8_t)color};assert(fwrite(rgb,1,3,f)==3);}assert(!fclose(f));}
}
