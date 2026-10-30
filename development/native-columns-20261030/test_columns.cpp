#include <cassert>
#include <cstdio>
#include <cstdint>
static uint32_t nes_player_palette[512];
#include "view.h"
#include "window_scale.h"
int main(){
 unsigned counts[256]={0};for(unsigned x=0;x<320;x++)counts[fv_source(x,0)]++;
 unsigned twice=0,once=0;for(unsigned n:counts){twice+=n==2;once+=n==1;}
 assert(once==192&&twice==64);puts("REPRO sharp 256->320: 192 single-width columns, 64 double-width columns");
 assert(fv_valid(512));assert(!fv_valid(768));
 for(unsigned i=0;i<512;i++)nes_player_palette[i]=0xff000000u|i*0x010101u;
 uint16_t source[256];uint32_t row[320],expanded[960*3];
 for(unsigned monitor=0;monitor<2;monitor++)for(unsigned mask=0;mask<3;mask++){
  unsigned opt=512|monitor|(mask<<4),edge=mask*8;assert(fv_width(opt)==256);
  for(unsigned shift=0;shift<256;shift++){
   for(unsigned x=0;x<256;x++)source[x]=(x+shift)&255;
   for(unsigned format=3;format<=4;format++){
    fv_row(row,source,100,opt,format);
    for(unsigned x=0;x<320;x++){
     int sx=x>=32+edge&&x<288-edge?(int)x-32:-1;assert(fv_source(x,opt)==sx);
     uint32_t c=sx<0?fv_border(x,100,opt):nes_player_palette[source[sx]];
     assert(row[x]==(format==3?c:__builtin_bswap32(c)));
    }
    for(unsigned scale=1;scale<=3;scale++){
     em_window_expand(expanded,320*scale,row,scale);
     for(unsigned dy=0;dy<scale;dy++)for(unsigned x=0;x<320*scale;x++)assert(expanded[dy*320*scale+x]==row[x/scale]);
    }
   }
  }
 }
 puts("PASS all 256 scroll phases: native columns, masks, monitor choices, byte orders and 1x/2x/3x repetition");
}
