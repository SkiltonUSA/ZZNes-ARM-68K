/* GPL-3.0-or-later. Procedural themes plus user-supplied side-panel themes; see amiga/borders/.
 * 320x240 scanout stretched by a 4:3 or 16:9 monitor. Game stays physical 4:3.
 * Option bits: monitor[0], theme[1..3], horizontal mask[4..5], vertical mask[6..7] (0/8/16 pixels), horizontal linear filter[8]. */
#pragma once
#include <stdint.h>
#include "border_art.h"
#if defined(__arm__)
struct fv_group {uint32_t offset,a[4],b[4],weight[4];};
extern "C" void em_blend_neon(uint32_t*,const uint32_t*,const fv_group*,unsigned);
static unsigned fv_neon;
#endif
static inline int fv_valid(unsigned opt){return opt<512 && ((opt>>4)&3)<3 && ((opt>>6)&3)<3;}
static inline unsigned fv_width(unsigned opt){return (opt&1)?240:320;}
static inline int fv_source(unsigned x,unsigned opt){
 unsigned width=fv_width(opt),left=(320-width)/2,sx;
 if(x<left||x>=left+width)return -1;
 /* Constant-ratio divisions compile to multiplies/shifts on Cortex-A9. */
 sx=(opt&1)?(x-left)*16/15:(x-left)*4/5;
 if(sx<((opt>>4)&3)*8||sx>=256-((opt>>4)&3)*8)return -1;
 return (int)sx;
}
static inline uint32_t fv_border(unsigned x,unsigned y,unsigned opt){
 unsigned theme=(opt>>1)&7;
 if(theme>=5)return border_art(x,y,theme,fv_width(opt));
 if(theme==0)return 0xff000000u;
 if(theme==1)return 0xffffffffu;
 if(theme==2){ /* Console grey, vents and red pinstripe. */
  if(y>=190&&y<196)return 0xffc82b32u;
  if(y>28&&y<160&&(x%8)<3)return 0xff282828u;
  return 0xffb8b8b0u;
 }
 if(theme==3){ /* Cream and burgundy. */
  if(y<24||y>212)return 0xff8c2438u;
  if(y>180&&y<185)return 0xffac903cu;
  return 0xffeee4c8u;
 }
 {unsigned h=(x*1973u+y*9277u+89173u);h=(h^(h>>7))*1103515245u;
  return (h%211u==0)?0xffe4e8ffu:0xff101827u;}
}
/* Centre-aligned horizontal linear filter, 8-bit weights, no floating point.
 * Clamp at overscan edges so hidden pixels cannot bleed into the visible image. */
static inline void fv_sample(unsigned x,unsigned opt,unsigned *a,unsigned *b,unsigned *weight){
 unsigned width=fv_width(opt),left=(320-width)/2,m=((opt>>4)&3)*8;
 int pos=(int)(((x-left)*2+1)*32768/width)-128;
 if(pos<(int)(m*256))pos=m*256;
 if(pos>(int)((255-m)*256))pos=(255-m)*256;
 *a=(unsigned)pos>>8;*b=*a<255-m?*a+1:*a;*weight=(unsigned)pos&255;
}
static inline uint32_t fv_blend(uint32_t a,uint32_t b,unsigned w){
 unsigned v=256-w;
 uint32_t rb=(((a&0x00ff00ffu)*v+(b&0x00ff00ffu)*w+0x00800080u)>>8)&0x00ff00ffu;
 uint32_t g=(((a&0x0000ff00u)*v+(b&0x0000ff00u)*w+0x00008000u)>>8)&0x0000ff00u;
 return 0xff000000u|rb|g;
}
static inline uint32_t fv_color(const uint16_t *src,unsigned x,unsigned y,unsigned opt){
 int sx=fv_source(x,opt);unsigned my=((opt>>6)&3)*8;
 if(sx<0||y<my||y>=240-my)return fv_border(x,y,opt);
 if(opt&256){unsigned a,b,w;fv_sample(x,opt,&a,&b,&w);return fv_blend(nes_player_palette[src[a]&511],nes_player_palette[src[b]&511],w);}
 return nes_player_palette[src[sx]&511];
}
static inline void fv_row(uint32_t *dst,const uint16_t *src,unsigned y,unsigned opt,unsigned format){
 /* Prepare scaling once per option change, not once per pixel or scanline. */
 static uint16_t map[320],second[320],weight[320];static unsigned previous=~0u,previous_format=0,begin,end;
 static uint32_t colors[512];
#if defined(__arm__)
 static uint32_t source_colors[263] __attribute__((aligned(16)));
 static fv_group groups[80];
#endif
 if(previous_format!=format){for(unsigned p=0;p<512;p++){uint32_t c=nes_player_palette[p]|0xff000000u;colors[p]=format==3?c:__builtin_bswap32(c);}previous_format=format;}
 static uint32_t panels[240][80];
 unsigned art=((opt>>1)&7)>=5;
 unsigned x,my=((opt>>6)&3)*8;
 if(previous!=opt){begin=320;end=0;for(x=0;x<320;x++){int sx=fv_source(x,opt);
   if(sx>=0){map[x]=(uint16_t)sx;if(opt&256){unsigned a,b,w;fv_sample(x,opt,&a,&b,&w);map[x]=a;second[x]=b;weight[x]=w;}if(begin==320)begin=x;end=x+1;}}
#if defined(__arm__)
  if(opt&256)for(x=begin;x+4<=end;x+=4){fv_group &g=groups[(x-begin)/4];g.offset=map[x]*4;
   for(unsigned i=0;i<4;i++){g.a[i]=0x03020100u+(map[x+i]-map[x])*0x04040404u;
    g.b[i]=0x03020100u+(second[x+i]-map[x])*0x04040404u;g.weight[i]=weight[x+i]*0x01010101u;}}
#endif
  if(art)for(unsigned yy=0;yy<240;yy++)for(unsigned xx=0;xx<80;xx++)
   panels[yy][xx]=fv_border(xx<40?xx:xx+240,yy,opt);
  previous=opt;
 }
 if(y<my||y>=240-my){for(x=0;x<320;x++){uint32_t c=art?(x<40?panels[y][x]:x>=280?panels[y][x-240]:0xff000000u):fv_border(x,y,opt);dst[x]=format==3?c:__builtin_bswap32(c);}return;}
 for(x=0;x<begin;x++){uint32_t c=art?(x<40?panels[y][x]:x>=280?panels[y][x-240]:0xff000000u):fv_border(x,y,opt);dst[x]=format==3?c:__builtin_bswap32(c);}
 if(opt&256){x=begin;
#if defined(__arm__)
  if(fv_neon){for(unsigned xx=0;xx<256;xx++)source_colors[xx]=colors[src[xx]&511];
   for(unsigned xx=256;xx<263;xx++)source_colors[xx]=source_colors[255];
   em_blend_neon(dst+begin,source_colors,groups,end-begin);x=begin+((end-begin)&~3u);}
#endif
  for(;x<end;x++){uint32_t c=fv_blend(nes_player_palette[src[map[x]]&511],nes_player_palette[src[second[x]]&511],weight[x]);dst[x]=format==3?c:__builtin_bswap32(c);}}
 else for(x=begin;x<end;x++)dst[x]=colors[src[map[x]]&511];
 for(x=end;x<320;x++){uint32_t c=art?(x<40?panels[y][x]:x>=280?panels[y][x-240]:0xff000000u):fv_border(x,y,opt);dst[x]=format==3?c:__builtin_bswap32(c);}
}
