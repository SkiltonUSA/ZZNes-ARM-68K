/* GPL-3.0-or-later. Bounded cartridge metadata shared by launcher and player.
 * Limits describe the integrated boards, not the capacity of NES 2.0 itself. */
#pragma once
#include <stdint.h>
struct fc_cartridge_info {
 uint32_t prg,chr,payload,wram,nvram,vram;
 unsigned mapper,submapper,nes2,battery,mirror,timing;
};
static inline int fc_diskdude(const uint8_t*r,uint32_t n){
 static const char mark[]="DiskDude!";if(!r||n<16)return 0;
 for(unsigned i=0;i<9;i++)if(r[7+i]!=(uint8_t)mark[i])return 0;return 1;
}
static inline unsigned fc_ram_size(unsigned shift){return shift?64u<<shift:0;}
static inline uint32_t fc_rom_size(unsigned low,unsigned high,unsigned unit){
 if(high!=15)return (low|(high<<8))*unit;
 unsigned exponent=low>>2,multiplier=2*(low&3)+1;
 if(exponent>=20)return 0;return (1u<<exponent)*multiplier;
}
static inline int fc_cartridge_parse(const uint8_t*r,uint32_t n,struct fc_cartridge_info*c){
 uint8_t clean[16];
 if(fc_diskdude(r,n)){for(unsigned i=0;i<16;i++)clean[i]=i<7?r[i]:0;r=clean;}
 if(!r||n<16||r[0]!='N'||r[1]!='E'||r[2]!='S'||r[3]!=26)return 0;
 struct fc_cartridge_info v={0};v.nes2=(r[7]&12)==8;v.mapper=(r[6]>>4)|(r[7]&240);
 v.battery=!!(r[6]&2);v.mirror=r[6]&1;v.payload=16+((r[6]&4)?512:0);
 if(v.nes2){
  if((r[7]&3)||r[13]||r[14]||r[15]||(r[12]&~3u)||(r[12]&3)==3)return 0;
  v.mapper|=(r[8]&15)<<8;v.submapper=r[8]>>4;v.timing=r[12];
  v.prg=fc_rom_size(r[4],r[9]&15,16384);v.chr=fc_rom_size(r[5],r[9]>>4,8192);
  if(!v.chr&&(r[5]||(r[9]&240)))return 0;
  v.wram=fc_ram_size(r[10]&15);v.nvram=fc_ram_size(r[10]>>4);v.vram=fc_ram_size(r[11]&15);
  if((r[11]&240)||v.battery!=!!v.nvram||(v.wram&&v.nvram))return 0;
 }else{
  if((r[7]&15)||r[8]||(r[9]&~1u)||r[10]||r[11]||r[12]||r[13]||r[14]||r[15])return 0;
  v.prg=r[4]*16384u;v.chr=r[5]*8192u;v.vram=v.chr?0:8192;v.timing=r[9]&1;
 }
 unsigned id=v.mapper;
 if(id!=0&&id!=1&&id!=2&&id!=3&&id!=4&&id!=5&&id!=7&&id!=11&&id!=66&&id!=78&&id!=90)return 0;
 if(!v.prg||v.prg>524288||v.chr>262144||v.prg<16384||(v.prg&(v.prg-1))||(v.chr&&(v.chr<8192||(v.chr&(v.chr-1)))))return 0;
 if(n!=v.payload+v.prg+v.chr)return 0;
 if(v.battery&&id!=1&&id!=4&&id!=5)return 0;
 if((r[6]&8)&&id!=78)return 0;
 if(v.nes2){
  if(r[6]&8)return 0;
  if(id==2||id==3||id==7||id==11){if(v.submapper>2)return 0;}
  else if(id==78){if(v.submapper!=1&&v.submapper!=3)return 0;}
  else if(v.submapper)return 0;
  if(v.chr?v.vram!=0:v.vram!=8192)return 0;
  unsigned expected=(id==1||id==4)?8192:id==5?32768:0;
  if(v.wram+v.nvram!=expected)return 0;
 }
 if(id==0&&(v.prg>32768||(!v.nes2&&v.chr!=8192)||v.chr>8192))return 0;
 if(id==3&&(!v.chr||v.prg>32768||v.chr>32768))return 0;
 if(id==7&&(v.chr||v.prg<32768))return 0;
 if(id==11&&(!v.chr||v.prg<32768||v.chr>131072))return 0;
 if(id==66&&(!v.chr||v.prg<32768||v.prg>131072||v.chr>32768))return 0;
 if(id==78&&(!v.chr||v.prg>131072||v.chr>131072))return 0;
 if((id==5||id==90)&&!v.chr)return 0;
 /* Preserve mapper 78's legacy discriminator, with explicit NES 2.0 variants. */
 if(id==78&&(v.nes2?v.submapper==3:!!(r[6]&8)))v.mirror=2;
 *c=v;return 1;
}
static inline int nes_cartridge(const uint8_t*r,uint32_t n){struct fc_cartridge_info c;return fc_cartridge_parse(r,n,&c)?(int)c.mapper:-1;}
static inline int fc_tag(const char*s,const char*tag){if(!s)return 0;for(;*s;s++){unsigned i=0;while(tag[i]&&s[i]&&((s[i]>='A'&&s[i]<='Z')?s[i]+32:s[i])==tag[i])i++;if(!tag[i])return 1;}return 0;}
static inline unsigned fc_rom_pal(const uint8_t*r,unsigned n,const char*path){
 const char*name=path?path:"";for(const char*p=name;*p;p++)if(*p=='/'||*p==':'||*p=='\\')name=p+1;
 if(n>=16&&!fc_diskdude(r,n)&&(r[7]&12)==8&&(r[12]&3)!=2)return (r[12]&3)==1;
 return n>=16&&((!fc_diskdude(r,n)&&((r[7]&12)!=8)&&(r[9]&1))||fc_tag(name,"(europe)")||fc_tag(name,"(australia)")||fc_tag(name,"(e)"));
}
static inline unsigned fc_period_us(unsigned pal){return pal?19998u:16639u;}
