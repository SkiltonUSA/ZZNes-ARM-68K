/* GPL-3.0-or-later. Bounded iNES contract for the expanded player. */
#pragma once
#include <stdint.h>
/* Some old dump tools overwrite bytes 7..15 with this exact signature.
 * Interpret it in memory only; never rewrite the user's ROM or invent high mapper bits. */
static inline int fc_diskdude(const uint8_t*r,uint32_t n){
 static const char mark[]="DiskDude!";
 if(!r||n<16)return 0;
 for(unsigned i=0;i<9;i++)if(r[7+i]!=(uint8_t)mark[i])return 0;
 return 1;
}
static inline int nes_cartridge(const uint8_t*r,uint32_t n){
 uint8_t clean[16];
 if(fc_diskdude(r,n)){for(unsigned i=0;i<16;i++)clean[i]=i<7?r[i]:0;r=clean;}
 if(!r||n<16||(r[0]!='N'||r[1]!='E'||r[2]!='S'||r[3]!=26)||(r[7]&15)||r[8]||(r[9]&~1u)||r[10]||r[11]||r[12]||r[13]||r[14]||r[15]||(r[6]&6))return -1;
 unsigned id=(r[6]>>4)|(r[7]&240),prg=r[4]*16384u,chr=r[5]*8192u;
 if((id!=0&&id!=1&&id!=2&&id!=3&&id!=4&&id!=5&&id!=78&&id!=90)||!prg||n!=16+prg+chr||prg>524288||chr>262144||(prg&(prg-1))||(chr&&(chr&(chr-1))))return -1;
 /* Mapper 78 uses the legacy four-screen flag to distinguish Holy Diver. */
 if((r[6]&8)&&id!=78)return -1;
 if(id==3&&(!chr||prg>32768||chr>32768))return -1;
 if(id==78&&(!chr||prg>131072||chr>131072))return -1;
 if(id==0&&(prg>32768||chr!=8192))return -1;
 if((id==5||id==90)&&!chr)return -1;
 return (int)id;
}
static inline int fc_tag(const char*s,const char*tag){if(!s)return 0;for(;*s;s++){unsigned i=0;while(tag[i]&&s[i]&&((s[i]>='A'&&s[i]<='Z')?s[i]+32:s[i])==tag[i])i++;if(!tag[i])return 1;}return 0;}
/* Older dumps often omit the PAL flag. Only examine the basename's tags. */
static inline unsigned fc_rom_pal(const uint8_t*r,unsigned n,const char*path){
 const char*name=path?path:"";for(const char*p=name;*p;p++)if(*p=='/'||*p==':'||*p=='\\')name=p+1;
 return n>=16&&((!fc_diskdude(r,n)&&(r[9]&1))||fc_tag(name,"(europe)")||fc_tag(name,"(australia)")||fc_tag(name,"(e)"));
}
static inline unsigned fc_period_us(unsigned pal){return pal?19998u:16639u;}
