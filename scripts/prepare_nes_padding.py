"""Launcher recovery only; the released player remains strict and unchanged."""
from pathlib import Path
import shutil
def once(s,a,b):
    if s.count(a)!=1:raise ValueError("Source mismatch: "+a[:100])
    return s.replace(a,b,1)

def prepare_padding(lib):
 root=Path(__file__).resolve().parents[1]
 shutil.copy2(root/'src/nes_padding.h',lib/'nes_padding.h')
 p=lib/'library_mui.h';s=p.read_text()
 if '#include "nes_padding.h"' in s:return
 s=once(s,'#include "zip/rom_archive.h"','#include "zip/rom_archive.h"\n#include "nes_padding.h"')
 s=s.replace('em_rom_load(', 'zzn_rom_load(').replace('em_rom_probe(p,LIB_LIMIT,LIB_SNES)','em_rom_probe(p,ZZN_NES_INPUT_LIMIT,LIB_SNES)')
 s=once(s,'static char cartridge_name[512];', '''static char cartridge_name[512];
static char launch_rom[UI_PATH];
static const char *trim_cache="PROGDIR:Cache/Trimmed.nes",*trim_pal_cache="PROGDIR:Cache/Trimmed (Europe).nes";
static void trim_cleanup(void){DeleteFile(trim_cache);DeleteFile(trim_pal_cache);}
static int prepare_launch_rom(void){
 unsigned n;unsigned char*p=malloc(LIB_LIMIT);int ok=0;
 if(!p)return 0;
 int error=zzn_rom_load(model.entry[selected].path,p,LIB_LIMIT,&n,0,cartridge_name,sizeof(cartridge_name));
 if(!error&&nes_cartridge(p,n)>=0){
  snprintf(launch_rom,sizeof(launch_rom),"%s",model.entry[selected].path);
  if(zzn_trimmed){BPTR dir=CreateDir("PROGDIR:Cache");if(dir)UnLock(dir);
   snprintf(launch_rom,sizeof(launch_rom),"%s",fc_rom_pal(p,n,cartridge_name)?trim_pal_cache:trim_cache);
   ok=zzn_write_clean(launch_rom,p,n);
  }else ok=1;
 }
 free(p);return ok;
}''')
 s=once(s,' FreeVec(p);\n}\nstatic void slotpath', ''' if(rom_valid&&zzn_trimmed)snprintf(details,sizeof(details),"Supported cartridge; %u trailing whitespace bytes ignored.\\nOriginal file unchanged.",zzn_trimmed);
 FreeVec(p);
}
static void slotpath''')
 s=once(s,'ui_hex(f,model.entry[selected].path);fputc(\'\\n\',f);slotpath', 'ui_hex(f,launch_rom);fputc(\'\\n\',f);slotpath')
 s=once(s,' if(!session_write(resume))', ' if(!prepare_launch_rom()){message("Cannot prepare cartridge. Check the ROM and available disk space.");return;}\n if(!session_write(resume))')
 p.write_text(s)
 p=lib/'library_manager.h';p.write_text(p.read_text().replace('em_rom_load(', 'zzn_rom_load('))
 p=lib/'library_launch.h';p.write_text(p.read_text().replace('child_running=0;splash_close();','child_running=0;trim_cleanup();splash_close();'))

def prepare_test_selector(lib):
 p=lib/'library_mui.h';s=p.read_text()
 # Private diagnostic chooses an existing library entry and exits; no normal UI impact.
 s=once(s,'static int next_console=-1,test_play,test_started,test_failed;', 'static int next_console=-1,test_play,test_started,test_failed;\nstatic const char *test_title="Super Mario World";')
 s=once(s,' test_play=argc==2&&!strcmp(argv[1],"--test-play");',' test_play=argc>=2&&!strcmp(argv[1],"--test-play");if(test_play&&argc==3)test_title=argv[2];')
 s=once(s,'strstr(title,"Super Mario World")','strstr(title,test_title)')
 p.write_text(s)
