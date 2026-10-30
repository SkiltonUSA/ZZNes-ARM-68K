/* GPL-3.0-or-later. Matching launcher's checks against a real core state. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include "library_saves.h"
int main(int argc,char **argv){
 assert(argc==2);
 FILE *f=fopen(argv[1],"rb");assert(f);
 unsigned char *p=malloc(LIB_STATE_CAP+1);assert(p);
 unsigned n=fread(p,1,LIB_STATE_CAP+1,f);assert(!ferror(f));fclose(f);
 assert(n>32&&n<=LIB_STATE_CAP);
 unsigned rom=le32(p+8),bytes=le32(p+12);
 assert(library_state_valid(p,n,rom,0,bytes));
 for(unsigned length=0;length<32;length++)assert(!library_state_valid(p,length,rom,0,bytes));
 assert(!library_state_valid(p,n-1,rom,0,bytes));
 const unsigned fields[]={0,4,8,12,16,20,24,28,32};
 for(unsigned i=0;i<sizeof(fields)/sizeof(fields[0]);i++){
  p[fields[i]]^=0x80;assert(!library_state_valid(p,n,rom,0,bytes));p[fields[i]]^=0x80;
 }
 p[4]=3;assert(!library_state_valid(p,n,rom,0,bytes));
 free(p);puts("PASS HQ launcher envelope: core state accepted; unknown version/corrupt/truncated rejected");
}
