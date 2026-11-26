#include "zip/rom_archive.h"
#include "nes_padding.h"
int main(int argc,char **argv) {
 unsigned n=0; int error; unsigned char *out;
 if(argc!=3)return 20;
 out=malloc(0xc0210);if(!out)return 20;
 error=zzn_rom_load(argv[1],out,0xc0210,&n,0,NULL,0);
 if(!error&&nes_cartridge(out,n)<0)error=99;
 if(!error&&!zzn_write_clean(argv[2],out,n))error=98;
 printf("LOADER error=%d bytes=%u trimmed=%u normalized=%u\n",error,n,zzn_trimmed,zzn_normalized);
 free(out);return error?5:0;
}
