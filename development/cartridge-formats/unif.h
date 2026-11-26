/* GPL-3.0-or-later. UNIF import for explicitly integrated discrete boards.
 * Produces a NES 2.0 image in separate caller storage; input is never changed.
 * Sequential ROM chips are concatenated in chip order, never file order.
 * Battery-backed and VROR boards need separate integration. */
#pragma once
#include <stdint.h>
#include <string.h>
#include "cartridge.h"
static uint32_t fc_unif_u32(const uint8_t *p){return p[0]|(uint32_t)p[1]<<8|(uint32_t)p[2]<<16|(uint32_t)p[3]<<24;}
static uint32_t fc_unif_crc(const uint8_t*p,unsigned n){uint32_t crc=~0u;for(unsigned i=0;i<n;i++){crc^=p[i];for(unsigned j=0;j<8;j++)crc=(crc>>1)^((0u-(crc&1))&0xedb88320u);}return ~crc;}
struct fc_unif_board {const char*name;unsigned mapper,sub,prg_max,chr_max,prg_exact;};
struct fc_unif_parts {const uint8_t*data[16];unsigned size[16],present,checks;uint32_t crc[16];};
static int fc_unif_index(unsigned c){return c>='0'&&c<='9'?(int)c-'0':c>='A'&&c<='F'?(int)c-'A'+10:-1;}
static int fc_unif_parts_size(const struct fc_unif_parts*p,unsigned limit,unsigned*total){
 *total=0;
 if((p->checks&~p->present)||(p->present&(p->present+1)))return 0;
 for(unsigned i=0;i<16;i++)if(p->present&(1u<<i)){
  if(p->size[i]>limit-*total||((p->checks&(1u<<i))&&fc_unif_crc(p->data[i],p->size[i])!=p->crc[i]))return 0;
  *total+=p->size[i];
 }
 return 1;
}
static int fc_unif_import(const uint8_t *p,unsigned n,uint8_t *out,unsigned cap,unsigned *used){
 static const struct fc_unif_board boards[]={
  {"NROM",0,0,32768,8192,0},{"NROM-128",0,0,16384,8192,16384},{"NROM-256",0,0,32768,8192,32768},
  {"UNROM",2,2,131072,0,0},{"UOROM",2,2,262144,0,0},{"CNROM",3,2,32768,32768,0},
  {"ANROM",7,1,131072,0,0},{"AOROM",7,2,262144,0,0},{"AMROM",7,2,131072,0,0},
  {"GNROM",66,0,131072,32768,0},{"MHROM",66,0,65536,16384,0}
 };
 *used=0;if(!p||!out||n<32||memcmp(p,"UNIF",4))return 0;
 unsigned revision=fc_unif_u32(p+4);if(revision<1||revision>7)return 0;
 struct fc_unif_parts parts[2]={0};unsigned ps=0,cs=0,seen=0,mirror=0,timing=0;
 char board[64]={0};
 for(unsigned at=32;at<n;){
  if(n-at<8)return 0;const uint8_t*id=p+at;unsigned size=fc_unif_u32(id+4);at+=8;if(size>n-at)return 0;
  const uint8_t*d=p+at;unsigned bit=0;
  if(!memcmp(id,"MAPR",4)){
   bit=1;if(!size||size>sizeof board||d[size-1])return 0;
   for(unsigned i=0;i+1<size;i++)if(d[i]<32||d[i]>126)return 0;
   memcpy(board,d,size);
  }else if(!memcmp(id,"PRG",3)||!memcmp(id,"CHR",3)){
   int i=fc_unif_index(id[3]);if(i<0||!size)return 0;
   struct fc_unif_parts*q=&parts[id[0]=='C'];if(q->present&(1u<<i))return 0;
   q->present|=1u<<i;q->data[i]=d;q->size[i]=size;
  }else if(!memcmp(id,"MIRR",4)){bit=8;if(size!=1||d[0]>5)return 0;mirror=d[0];}
  else if(!memcmp(id,"TVCI",4)){bit=16;if(size!=1||d[0]>2)return 0;timing=d[0];}
  else if(!memcmp(id,"PCK",3)||!memcmp(id,"CCK",3)){
   int i=fc_unif_index(id[3]);if(i<0||size!=4)return 0;
   struct fc_unif_parts*q=&parts[id[0]=='C'];if(q->checks&(1u<<i))return 0;
   q->checks|=1u<<i;q->crc[i]=fc_unif_u32(d);
  }else if(!memcmp(id,"BATR",4)||!memcmp(id,"VROR",4))return 0;
  else if(!memcmp(id,"CTRL",4)){bit=128;if(size!=1||d[0]!=1)return 0;}
  if(bit&&(seen&bit))return 0;seen|=bit;at+=size;
 }
 if(!(seen&1)||!parts[0].present||!fc_unif_parts_size(&parts[0],524288,&ps)||!fc_unif_parts_size(&parts[1],262144,&cs))return 0;
 const char*name=board;
 if(!strncmp(name,"NES-",4)||!strncmp(name,"HVC-",4)||!strncmp(name,"UNL-",4)||!strncmp(name,"BMC-",4))name+=4;
 const struct fc_unif_board*b=NULL;
 for(unsigned i=0;i<sizeof boards/sizeof boards[0];i++)if(!strcmp(name,boards[i].name)){b=&boards[i];break;}
 if(!b||ps>b->prg_max||cs>b->chr_max||(b->prg_exact&&ps!=b->prg_exact))return 0;
 if(b->mapper==7){if((seen&8)&&mirror!=5)return 0;mirror=0;}else if(mirror>1)return 0;
 if((b->chr_max&&!cs)||ps%16384||cs%8192||cap<16||ps>cap-16||cs>cap-16-ps)return 0;
 memset(out,0,16);memcpy(out,"NES\032",4);out[4]=ps/16384;out[5]=cs/8192;
 out[6]=(b->mapper<<4)|mirror;out[7]=(b->mapper&240)|8;out[8]=b->sub<<4;out[11]=cs?0:7;out[12]=timing;
 unsigned at=16;for(unsigned k=0;k<2;k++)for(unsigned i=0;i<16;i++)if(parts[k].present&(1u<<i)){
  memcpy(out+at,parts[k].data[i],parts[k].size[i]);at+=parts[k].size[i];
 }
 unsigned length=16+ps+cs;if(nes_cartridge(out,length)<0)return 0;*used=length;return 1;
}
