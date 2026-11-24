/* GPL-3.0-or-later. Launcher-only iNES whitespace trailer recovery.
 * Never alter cartridge bytes or the source file. ZIP CRC is checked first. */
#ifndef ZZN_NES_PADDING_H
#define ZZN_NES_PADDING_H
#include "cartridge.h"
#define ZZN_NES_INPUT_LIMIT 0x200000u
static unsigned zzn_trimmed;
static unsigned zzn_nes_size(const unsigned char *p,unsigned n){
 if(n<16||memcmp(p,"NES\032",4))return n;
 unsigned size=16u+((p[6]&4)?512u:0u)+p[4]*16384u+p[5]*8192u;
 if(size>=n||nes_cartridge(p,size)<0)return n;
 for(unsigned i=size;i<n;i++)if(p[i]!=32&&p[i]!=10&&p[i]!=13)return n;
 return size;
}
static int zzn_rom_load(const char *path,unsigned char *out,unsigned limit,unsigned *used,int snes,char *name,unsigned cap){
 unsigned n=0,size;int error;unsigned char *input;
 zzn_trimmed=0;*used=0;
 if(snes)return em_rom_load(path,out,limit,used,snes,name,cap);
 input=malloc(ZZN_NES_INPUT_LIMIT);if(!input)return EM_ROM_MEMORY;
 error=em_rom_load(path,input,ZZN_NES_INPUT_LIMIT,&n,0,name,cap);
 if(!error){size=zzn_nes_size(input,n);if(size>limit)error=EM_ROM_LARGE;
  else{memcpy(out,input,size);*used=size;zzn_trimmed=n-size;}}
 free(input);return error;
}
/* Prefix must be exactly the validated bytes; re-read to catch short writes. */
static int zzn_write_clean(const char *path,const unsigned char *p,unsigned n){
 unsigned char check[4096];unsigned at=0;int ok;FILE*f=fopen(path,"wb");if(!f)return 0;
 ok=fwrite(p,1,n,f)==n;if(fclose(f))ok=0;if(!ok){remove(path);return 0;}
 f=fopen(path,"rb");if(!f){remove(path);return 0;}
 while(at<n){unsigned count=n-at;if(count>sizeof(check))count=sizeof(check);
  if(fread(check,1,count,f)!=count||memcmp(check,p+at,count)){ok=0;break;}at+=count;}
 if(fgetc(f)!=EOF||ferror(f))ok=0;fclose(f);if(!ok)remove(path);return ok;
}
#endif
