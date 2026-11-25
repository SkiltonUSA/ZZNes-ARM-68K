/* Original transaction/fault tests; uses the production battery file helpers. */
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>
static int fail_open,fail_write,fail_close,bad_read,fail_rename,renames,fail_remove,rollback_fail;
static FILE *opened_write;
static FILE *test_open(const char*p,const char*m){
 if(fail_open&&strstr(p,".tmp")&&m[0]=='w'){errno=EIO;return NULL;}
 FILE*f=fopen(p,m);if(m[0]=='w')opened_write=f;return f;
}
static size_t test_write(const void*p,size_t a,size_t b,FILE*f){return fwrite(p,a,fail_write?b/2:b,f);}
static size_t test_read(void*p,size_t a,size_t b,FILE*f){size_t n=fread(p,a,b,f);if(bad_read&&n)((unsigned char*)p)[0]^=1;return n;}
static int test_close(FILE*f){int bad=fail_close&&f==opened_write;int ret=fclose(f);if(bad){errno=EIO;return EOF;}return ret;}
static int test_rename(const char*a,const char*b){
 renames++;if(renames==fail_rename||(rollback_fail&&renames==3)){errno=EIO;return 0;}
 return rename(a,b)==0;
}
static int test_remove(const char*p){if(fail_remove){errno=EACCES;return 0;}return remove(p)==0;}
#define fopen test_open
#define fwrite test_write
#define fread test_read
#define fclose test_close
#define FC_BATTERY_RENAME(a,b) test_rename(a,b)
#define FC_BATTERY_REMOVE(p) test_remove(p)
#include "battery_files.h"
#undef fopen
#undef fwrite
#undef fread
#undef fclose
static unsigned char old[32769],next[32769],buffer[32769];
static void write_file(const char*p,const void*d,unsigned n){FILE*f=fopen(p,"wb");assert(f);assert(fwrite(d,1,n,f)==n);assert(!fclose(f));}
static void expect(const char*p,const void*d,unsigned n){unsigned char temp[32769];FILE*f=fopen(p,"rb");assert(f);assert(fread(temp,1,n+1,f)==n);assert(!fclose(f));assert(!memcmp(temp,d,n));}
static void reset(unsigned size){
 fail_open=fail_write=fail_close=bad_read=fail_rename=renames=fail_remove=rollback_fail=0;opened_write=NULL;
 remove("game.sav");remove("game.sav.bak");remove("game.sav.tmp");write_file("game.sav",old,size);
}
int main(void){
 char dir[]="/tmp/zznes-battery-XXXXXX";assert(mkdtemp(dir));assert(!chdir(dir));
 for(unsigned i=0;i<32768;i++){old[i]=i*7;next[i]=i*13+9;}
 for(unsigned size=8192;size<=32768;size*=4){
  int recovered;
  reset(size);assert(fc_battery_file_load("game.sav",buffer,size,&recovered)==1&&!recovered);assert(!memcmp(buffer,old,size));
  assert(fc_battery_file_store("game.sav",next,buffer,size));expect("game.sav",next,size);expect("game.sav.bak",old,size);
  reset(size);remove("game.sav");assert(fc_battery_file_load("game.sav",buffer,size,&recovered)==0);
  assert(fc_battery_file_store("game.sav",next,buffer,size));expect("game.sav",next,size);
  reset(size);assert(!rename("game.sav","game.sav.bak"));write_file("game.sav.tmp",next,size);
  assert(fc_battery_file_load("game.sav",buffer,size,&recovered)==1&&recovered);assert(!memcmp(buffer,old,size));
  assert(fc_battery_file_store("game.sav",old,buffer,size));expect("game.sav",old,size);expect("game.sav.bak",old,size);
  reset(size);remove("game.sav");write_file("game.sav.tmp",next,size);assert(fc_battery_file_load("game.sav",buffer,size,&recovered)<0);expect("game.sav.tmp",next,size);
  for(int delta=-1;delta<=1;delta+=2){reset(size);write_file("game.sav",old,size+delta);assert(fc_battery_file_load("game.sav",buffer,size,&recovered)<0);assert(!fc_battery_file_store("game.sav",next,buffer,size));expect("game.sav",old,size+delta);}
  reset(size);write_file("game.sav.bak",old,size-1);remove("game.sav");assert(fc_battery_file_load("game.sav",buffer,size,&recovered)<0);
  for(int fault=0;fault<7;fault++){
   reset(size);
   switch(fault){case 0:fail_open=1;break;case 1:fail_write=1;break;case 2:fail_close=1;break;case 3:bad_read=1;break;case 4:fail_remove=1;break;case 5:fail_rename=1;break;case 6:fail_rename=2;break;}
   assert(!fc_battery_file_store("game.sav",next,buffer,size));expect("game.sav",old,size);
  }
  reset(size);fail_rename=2;rollback_fail=1;assert(!fc_battery_file_store("game.sav",next,buffer,size));expect("game.sav.bak",old,size);
  fail_rename=rollback_fail=0;assert(fc_battery_file_load("game.sav",buffer,size,&recovered)==1&&recovered);assert(!memcmp(buffer,old,size));
  printf("PASS %u-byte battery files: new/existing, exact length, backup recovery, orphan refusal, open/write/close/readback/remove/rename/rollback faults\n",size);
 }
 remove("game.sav");remove("game.sav.bak");remove("game.sav.tmp");assert(!chdir("/"));assert(!rmdir(dir));
}
