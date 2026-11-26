"""Opt-in, isolated NES 2.0 / UNIF / discrete-board candidate."""
from pathlib import Path
import shutil
from prepare_trainers import once
ROOT=Path(__file__).resolve().parents[1]

def core(path):
 p=Path(path)/'compat_core.cpp';s=p.read_text()
 s=once(s,'static unsigned chosen_pal;', 'void ANROM_Init(CartInfo*);void Mapper11_Init(CartInfo*);void MHROM_Init(CartInfo*);\nstatic unsigned chosen_pal;')
 s=once(s,' unsigned payload=16+((rom[6]&4)?512u:0u);',' struct fc_cartridge_info meta;if(!fc_cartridge_parse(rom,size,&meta))return 1;\n unsigned payload=meta.payload;')
 s=once(s,'unsigned prg=rom[4]*16384u,chr=rom[5]*8192u;', 'unsigned prg=meta.prg,chr=meta.chr;')
 s=once(s,'cart.mirror=(id==78&&(rom[6]&8))?2:(rom[6]&1);cart.battery=!!(rom[6]&2);', '''cart.mirror=meta.mirror;cart.battery=meta.battery;
 cart.ines2=meta.nes2;cart.submapper=meta.submapper;cart.wram_size=meta.wram;
 cart.battery_wram_size=meta.nvram;cart.vram_size=meta.vram;cart.battery_vram_size=0;''')
 s=once(s,'else if(id==78)Mapper78_Init(&cart);','else if(id==7)ANROM_Init(&cart);else if(id==11)Mapper11_Init(&cart);else if(id==66)MHROM_Init(&cart);else if(id==78)Mapper78_Init(&cart);')
 s=once(s,' fc_battery_loaded();', ''' // NES 2.0 CNROM can explicitly specify no CPU RAM.
 if(meta.nes2&&id==3&&!meta.wram){SetReadHandler(0x6000,0x7fff,readnull);SetWriteHandler(0x6000,0x7fff,writenull);}
 fc_battery_loaded();''')
 p.write_text(s)
 # Explicit NES 2.0 RAM sizes override the legacy CRC database heuristics.
 for name,old,new in (
  ('mmc1.cpp','int ws = DetectMMC1WRAMSize(info->CRC32);','int ws = info->ines2 ? (info->wram_size+info->battery_wram_size)/1024 : DetectMMC1WRAMSize(info->CRC32);'),
  ('mmc5.cpp','WRAMSIZE = DetectMMC5WRAMSize(info->CRC32);','WRAMSIZE = info->ines2 ? (info->wram_size+info->battery_wram_size)/1024 : DetectMMC5WRAMSize(info->CRC32);')):
  p=Path(path)/name;p.write_text(once(p.read_text(),old,new))
 p=Path(path)/'datalatch.cpp';s=p.read_text()
 s=once(s,'bus_conflict = busc;', '''bus_conflict = busc;
 if(info->ines2&&(info->submapper==1||info->submapper==2))
  bus_conflict = info->submapper==2;''')
 # AxROM registers start at cartridge ROM, not expansion I/O.
 s=once(s,'ANROMSync, 0, 0x4020, 0xFFFF','ANROMSync, 0, 0x8000, 0xFFFF')
 # GNROM/MHROM discrete logic has AND bus conflicts.
 s=once(s,'MHROMSync, 0, 0x8000, 0xFFFF, 0, 0','MHROMSync, 0, 0x8000, 0xFFFF, 0, 1')
 p.write_text(s)

def prepare(core_path,stage,library,common):
 core(core_path)
 for folder in (Path(core_path),stage,library,common):shutil.copy2(ROOT/'development/cartridge-formats/cartridge.h',folder/'cartridge.h')
 p=stage/'host.c';s=p.read_text()
 start=s.index(' {int id=nes_cartridge(rom,size);')
 end=s.index('\n',start)
 s=s[:start]+''' {struct fc_cartridge_info meta;if(!fc_cartridge_parse(rom,size,&meta)){puts("Unsupported NES board or cartridge layout. Import UNIF through the launcher.");goto done;}printf("CARTRIDGE mapper=%u submapper=%u PRG=%u CHR=%u battery=%u\\n",meta.mapper,meta.submapper,meta.prg,meta.chr,meta.battery);}'''+s[end:]
 p.write_text(s)
 # Normalize in the launcher after ZIP CRC checking. A prepared cartridge uses
 # the existing temporary-cache lifecycle; the user's UNIF file stays intact.
 shutil.copy2(ROOT/'development/cartridge-formats/unif.h',library/'unif.h')
 p=library/'nes_padding.h';s=p.read_text()
 s=once(s,'#include "cartridge.h"','#include "cartridge.h"\n#include "unif.h"')
 s=once(s,'static unsigned zzn_trimmed;','static unsigned zzn_trimmed,zzn_normalized;')
 s=once(s,'zzn_trimmed=0;*used=0;','zzn_trimmed=zzn_normalized=0;*used=0;')
 s=once(s,'if(!error){size=zzn_nes_size(input,n);', '''if(!error&&n>=4&&!memcmp(input,"UNIF",4)){
  if(fc_unif_import(input,n,out,limit,used))zzn_normalized=1;else error=EM_ROM_IO;
  free(input);return error;
 }
 if(!error){size=zzn_nes_size(input,n);''')
 # NES 2.0 exponent/extended sizes are not legacy iNES byte counts.
 s=once(s,'unsigned size=16u+((p[6]&4)?512u:0u)+p[4]*16384u+p[5]*8192u;', '''unsigned prg=p[4]*16384u,chr=p[5]*8192u;
 if((p[7]&12)==8){prg=fc_rom_size(p[4],p[9]&15,16384);chr=fc_rom_size(p[5],p[9]>>4,8192);}
 unsigned size=16u+((p[6]&4)?512u:0u)+prg+chr;''')
 p.write_text(s)
 p=library/'library_mui.h';s=p.read_text().replace('if(zzn_trimmed){BPTR dir=', 'if(zzn_trimmed||zzn_normalized){BPTR dir=')
 s=once(s,'#define LIB_PATTERN "#?.(nes|zip)"',
        '#define LIB_PATTERN "#?.(nes|unf|unif|zip)"')
 s=s.replace('requires supported iNES\\nmapper 0/1/2/3/4/5/78/90; battery: mappers 1/4/5; no NES 2.0.',
             'board or cartridge layout not integrated.\\nSee the cartridge compatibility guide.')
 p.write_text(s)
 p=library/'ui_model.h';s=p.read_text()
 s=once(s,'if(n>4&&(!strcasecmp(out+n-4,".nes")',
        'if(n>5&&!strcasecmp(out+n-5,".unif"))out[n-5]=0;\n else if(n>4&&(!strcasecmp(out+n-4,".unf")||!strcasecmp(out+n-4,".nes")')
 p.write_text(s)
 for folder in (library,stage):
  p=folder/'zip/rom_archive.h';s=p.read_text()
  s=once(s,':!strcasecmp(p+n-4,".nes"));}', ':(!strcasecmp(p+n-4,".nes")||!strcasecmp(p+n-4,".unf")||(n>5&&!strcasecmp(p+n-5,".unif"))));}')
  p.write_text(s)
