"""Opt-in iNES trainers, following the pinned FCEUX power-on path."""
from pathlib import Path


def once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('Unexpected trainer preparation input: ' + old)
    return text.replace(old, new, 1)


def prepare_gate(path):
    path = Path(path)
    text = once(path.read_text(), '(r[6]&6)', '(r[6]&2)')
    text = once(text, 'n!=16+prg+chr', 'n!=16+((r[6]&4)?512u:0u)+prg+chr')
    path.write_text(text)


def prepare_core(core):
    path = Path(core) / 'compat_core.cpp'
    text = once(path.read_text(), 'static int loaded;',
                'static int loaded;\nstatic const uint8 *trainer;\n'
                'static DECLFR(readtrainer){return trainer[A&511];}')
    text = once(text, 'unsigned prg=rom[4]',
                'unsigned payload=16+((rom[6]&4)?512u:0u);\n trainer=(rom[6]&4)?rom+16:nullptr;\n unsigned prg=rom[4]')
    text = once(text, '(uint8 *)rom+16,prg', '(uint8 *)rom+payload,prg')
    text = once(text, '(uint8 *)rom+16+prg,chr', '(uint8 *)rom+payload+prg,chr')
    text = once(text, 'for(unsigned i=16;i<size;i++)', 'for(unsigned i=payload;i<size;i++)')
    text = once(text, ' FCEUI_Sound(32000);timestampbase=0;X6502_Power();',
                """ // Pinned FCEUX iNES_ExecPower: populate mapper RAM when possible.
 // Boards without writable trainer RAM get the same read-handler fallback.
 if(trainer)for(unsigned i=0;i<512;i++){
  X6502_DMW(0x7000+i,trainer[i]);
  if(X6502_DMR(0x7000+i)!=trainer[i]){
   SetReadHandler(0x7000,0x71ff,readtrainer);break;
  }
 }
 FCEUI_Sound(32000);timestampbase=0;X6502_Power();""")
    path.write_text(text)


def prepare_launcher(library):
    path = Path(library) / 'library_mui.h'
    text = once(path.read_text(), '#define LIB_LIMIT 0xc0010u', '#define LIB_LIMIT 0xc0210u')
    text = text.replace('no trainer or battery.', 'no battery or NES 2.0.')
    path.write_text(text)
    from prepare_nes_padding import prepare_padding
    prepare_padding(Path(library))
