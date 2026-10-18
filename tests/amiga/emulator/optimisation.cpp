// GPL-3.0-or-later. Independent per-channel oracle for horizontal sampling.
#include <stdint.h>
#include <stdio.h>
#include <assert.h>
#include <math.h>
#include <initializer_list>
#include "player_palette.h"
#include "view.h"
static uint32_t oracle(const uint16_t*src,unsigned x,unsigned y,unsigned opt){
 int sx=fv_source(x,opt);unsigned my=((opt>>6)&3)*8;
 if(sx<0||y<my||y>=240-my)return fv_border(x,y,opt);
 if(!(opt&256))return nes_player_palette[src[sx]&511]|0xff000000u;
 unsigned w=fv_width(opt),left=(320-w)/2,m=((opt>>4)&3)*8;
 double p=((double)(x-left)+0.5)*256.0/w-0.5;
 if(p<m)p=m;if(p>255-m)p=255-m;
 unsigned fp=(unsigned)floor(p*256.0+1e-8),a=fp/256,b=a<255-m?a+1:a,weight=fp%256;
 uint32_t c=0xff000000u;
 for(unsigned shift=0;shift<24;shift+=8){unsigned va=(nes_player_palette[src[a]&511]>>shift)&255,vb=(nes_player_palette[src[b]&511]>>shift)&255;c|=((va*(256-weight)+vb*weight+128)/256)<<shift;}
 return c;
}
int main(){uint16_t src[256];uint32_t dst[322];
 for(unsigned i=0;i<256;i++)src[i]=(i*37+i/3)&511;
 unsigned count=0;
 for(unsigned opt=0;opt<512;opt++)if(fv_valid(opt))for(unsigned fmt=3;fmt<=4;fmt++)for(unsigned y: {0u,8u,15u,16u,39u,119u,223u,231u,239u}){
  dst[0]=dst[321]=0x12345678;fv_row(dst+1,src,y,opt,fmt);
  assert(dst[0]==0x12345678&&dst[321]==0x12345678);
  for(unsigned x=0;x<320;x++){uint32_t c=oracle(src,x,y,opt);assert(fv_color(src,x,y,opt)==c);if(fmt==4)c=__builtin_bswap32(c);assert(dst[x+1]==c);count++;}
 }
 // Exercise every possible weight including saturated channels/rounding carries.
 for(unsigned a=0;a<512;a++)for(unsigned b=0;b<512;b+=7)for(unsigned w=0;w<256;w+=3){uint32_t expected=0xff000000;for(unsigned s=0;s<24;s+=8)expected|=(((((nes_player_palette[a]>>s)&255)*(256-w))+(((nes_player_palette[b]>>s)&255)*w)+128)/256)<<s;assert(fv_blend(nes_player_palette[a],nes_player_palette[b],w)==expected);}
 printf("PASS %u sampled output pixels: sharp/smooth, all options, both byte orders, masks, borders and guards\n",count);
}
