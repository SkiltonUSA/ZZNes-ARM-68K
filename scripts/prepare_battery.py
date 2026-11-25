"""Isolated mapper 1/4/5 battery integration; no archived/vendor source edits."""
from pathlib import Path
from prepare_trainers import once
ROOT=Path(__file__).resolve().parents[1]

def gate(path):
 p=Path(path);s=p.read_text()
 s=once(s,'||(r[6]&2))return -1;',')return -1;')
 s=once(s,' /* Mapper 78 uses', ' if((r[6]&2)&&id!=1&&id!=4&&id!=5)return -1;\n /* Mapper 78 uses')
 p.write_text(s)

def core(path):
 p=Path(path)/'compat_core.cpp';s=p.read_text()
 s=once(s,'cart.battery=0;','cart.battery=!!(rom[6]&2);')
 # Reapply the existing trainer after the host imports battery RAM, matching
 # upstream load-save-before-power/trainer ordering without rerunning the CPU.
 start=s.index(' // Pinned FCEUX iNES_ExecPower:')
 end=s.index(' FCEUI_Sound(32000);',start)
 trainer=s[start:end]
 s=s[:start]+' fc_battery_loaded();\n'+s[end:]
 api='''unsigned fc_battery(uint8 **p){
 *p=nullptr;
 if(!loaded||!cart.battery)return 0;
 *p=cart.SaveGame[0];return cart.SaveGameLen[0];
}
void fc_battery_loaded(){
'''+trainer+'''}
'''
 s=once(s,'int fc_init(',api+'int fc_init(')
 marker=' if(FC_Error)return FC_Error;'
 check='''
 if(cart.battery&&(!cart.SaveGame[0]||!cart.SaveGameLen[0]||cart.SaveGameLen[0]>32768||
    cart.SaveGame[1]||cart.SaveGame[2]||cart.SaveGame[3]))return 12;'''
 s=once(s,marker,marker+check);p.write_text(s)

def prepare(core_path,stage,library,common,source):
 core(core_path)
 for folder in (stage,library,common):gate(folder/'cartridge.h')
 adapter=(source/'amiga/fceux_player/adapter.cpp').read_text()
 adapter=adapter.replace('../fceux_bench/core.h','fceux_core_api.h').replace('../mesen_nes/core.h','nes_api.h')
 adapter=once(adapter,'unsigned nes_save(uint8_t **p){*p=nullptr;return 0;} // Supported cartridges have no battery.',
              'extern unsigned fc_battery(uint8_t **);\nunsigned nes_save(uint8_t **p){return fc_battery(p);}')
 (stage/'battery_adapter.cpp').write_text(adapter)
 (stage/'fceux_core_api.h').write_text((source/'amiga/fceux_bench/core.h').read_text())
 p=core_path/'worker.cpp';s=p.read_text()
 s='extern void fc_battery_loaded();\n'+s
 s=once(s,'for(unsigned i=0;i<n;i++)p[i]=base[NES_SAVE+i];',
             'for(unsigned i=0;i<n;i++)p[i]=base[NES_SAVE+i];\n    fc_battery_loaded();')
 p.write_text(s)
 for name in ('battery_host.h','battery_files.h'):(stage/name).write_text((ROOT/'development/battery-save'/name).read_text())
 p=stage/'player_frontend.h';s=p.read_text();s=s.replace('save_size,save_hash,','save_size,');s=s[:s.index('static int player_load_save(void)')]+ '#include "battery_host.h"\n';p.write_text(s)
 p=stage/'host.c';s=p.read_text();s=once(s,'if(save_data){FreeVec(save_data);save_data=NULL;}','if(save_verify){FreeVec(save_verify);save_verify=NULL;}if(save_data){FreeVec(save_data);save_data=NULL;}')
 s=s.replace('no battery/trainer; four-screen flag only for mapper 78','battery only for mappers 1/4/5; four-screen flag only for mapper 78');p.write_text(s)
 p=library/'library_mui.h';s=p.read_text().replace('no battery or NES 2.0.','battery: mappers 1/4/5; no NES 2.0.');p.write_text(s)
