/* GPL-3.0-or-later. Included after player audio setup. Frame-boundary transfers. */
static int save_recovered;
static UBYTE *save_verify;
static int battery_remove(const char *path){
 if(DeleteFile(path))return 1;
 errno=IoErr()==ERROR_OBJECT_NOT_FOUND?ENOENT:EIO;return 0;
}
#define FC_BATTERY_REMOVE(path) battery_remove(path)
#define FC_BATTERY_RENAME(from,to) Rename(from,to)
#include "battery_files.h"
static int player_load_save(void){
 int found;
 save_size=ad_get(shared+MB_REPLY,44);if(!save_size||!rom_path)return 1;
 if(save_size>FC_BATTERY_LIMIT||strlen(rom_path)>1023)return 0;
 strcpy(save_path,rom_path);strcat(save_path,".sav");
 save_data=AllocVec(save_size+1,MEMF_PUBLIC|MEMF_CLEAR);
 save_verify=AllocVec(save_size+1,MEMF_PUBLIC|MEMF_CLEAR);
 if(!save_data||!save_verify)return 0;
 found=fc_battery_file_load(save_path,save_data,save_size,&save_recovered);
 if(found<0){puts("BATTERY unreadable, wrong-size or unfinished save; files retained");return 0;}
 if(found){
  memcpy((void *)(shared+NES_SAVE),save_data,save_size);syncio->push(shared+NES_SAVE,save_size,NULL);
  if(!request(NES_SAVE_LOAD,save_size))return 0;
  printf("BATTERY loaded %u bytes%s\n",save_size,save_recovered?" from backup":"");
 }else puts("BATTERY new cartridge RAM");
 /* Read the actual initialized RAM, including trainer bytes. A missing file
  * must not zero mapper RAM or overwrite the trainer installed at power-on. */
 if(!request(NES_SAVE_STORE,save_size))return 0;
 syncio->pull(shared+NES_SAVE,save_size,NULL);CopyMem((APTR)(shared+NES_SAVE),save_data,save_size);
 return 1;
}
static int player_store_save(void){
 int ok;
 if(!save_data||!save_size)return 1;
 if(!request(NES_SAVE_STORE,save_size))return 0;
 syncio->pull(shared+NES_SAVE,save_size,NULL);CopyMem((APTR)(shared+NES_SAVE),save_verify,save_size);
 if(!save_recovered&&!memcmp(save_data,save_verify,save_size))return 1;
 /* Keep the current bytes separate from the verification scratch buffer. */
 CopyMem(save_verify,save_data,save_size);
 ok=fc_battery_file_store(save_path,save_data,save_verify,save_size);
 if(ok){save_recovered=0;printf("BATTERY wrote %u bytes to %s\n",save_size,save_path);}
 return ok;
}
