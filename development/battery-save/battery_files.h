/* GPL-3.0-or-later. Raw mapper battery files; no emulated state is stored here.
 * Define FC_BATTERY_RENAME and FC_BATTERY_REMOVE as boolean-success operations. */
#ifndef FC_BATTERY_FILES_H
#define FC_BATTERY_FILES_H
#include <stdio.h>
#include <string.h>
#include <errno.h>
#define FC_BATTERY_LIMIT 32768u
/* 0 missing, 1 complete, -1 unreadable/wrong size. Never accept a prefix. */
static int fc_battery_read(const char *path,unsigned char *data,unsigned size){
 FILE *f=fopen(path,"rb");unsigned n;int ok;
 if(!f)return errno==ENOENT?0:-1;
 n=fread(data,1,size+1,f);ok=!ferror(f)&&n==size;
 if(fclose(f))ok=0;
 return ok?1:-1;
}
/* Missing main + valid backup is the interrupted-rename recovery case.
 * An orphan temporary file alone is ambiguous: preserve it and refuse. */
static int fc_battery_file_load(const char *path,unsigned char *data,unsigned size,int *recovered){
 char side[1050];int result;FILE *f;
 *recovered=0;
 if(!size||size>FC_BATTERY_LIMIT||strlen(path)>1040)return -1;
 result=fc_battery_read(path,data,size);if(result)return result;
 snprintf(side,sizeof(side),"%s.bak",path);
 result=fc_battery_read(side,data,size);
 if(result){if(result>0)*recovered=1;return result;}
 snprintf(side,sizeof(side),"%s.tmp",path);
 f=fopen(side,"rb");if(f){fclose(f);return -1;}
 return errno==ENOENT?0:-1;
}
/* data and verify each have size+1 bytes. Read back exactly before rotation.
 * A failed final rename restores the previous main when possible; otherwise
 * its .bak remains recoverable on the next launch. */
static int fc_battery_file_store(const char *path,const unsigned char *data,unsigned char *verify,unsigned size){
 char temp[1050],backup[1050];FILE *f;int ok,had;
 if(!size||size>FC_BATTERY_LIMIT||strlen(path)>1040)return 0;
 snprintf(temp,sizeof(temp),"%s.tmp",path);snprintf(backup,sizeof(backup),"%s.bak",path);
 had=fc_battery_read(path,verify,size);if(had<0)return 0;
 f=fopen(temp,"wb");if(!f)return 0;
 ok=fwrite(data,1,size,f)==size;if(fclose(f))ok=0;if(!ok)return 0;
 if(fc_battery_read(temp,verify,size)!=1||memcmp(data,verify,size))return 0;
 if(had){
  if(!FC_BATTERY_REMOVE(backup)&&errno!=ENOENT)return 0;
  if(!FC_BATTERY_RENAME(path,backup))return 0;
 }
 if(!FC_BATTERY_RENAME(temp,path)){
  if(had)FC_BATTERY_RENAME(backup,path);
  return 0;
 }
 return 1;
}
#endif
