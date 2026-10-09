"""Auditable adapters for the pinned Mesen core, without desktop dependencies."""
import re, json, hashlib, difflib
from pathlib import Path

def remove(text, name):
    pattern=r'^[ \t]*(?:virtual )?[^\n{};]*\b'+re.escape(name)+r'\([^\n]*\)(?: override)?\s*\{'
    while (m:=re.search(pattern,text,re.M)):
        end=m.end(); depth=1
        while depth:
            depth+=(text[end]=='{')-(text[end]=='}');end+=1
        text=text[:m.start()]+text[end:]
    return re.sub(r'^[ \t]*[^\n{}]*\b'+re.escape(name)+r'\([^\n]*\)(?: override)?;\n','',text,flags=re.M)

def prepare(src,out):
    vendor=src/'vendor/player'; manifest=json.loads((vendor/'upstream.json').read_text()); patch=''
    for name,sha in manifest['files'].items():
        original=(vendor/name).read_text(); assert hashlib.sha256((vendor/name).read_bytes()).hexdigest()==sha,name
        text=original
        if name in ['SoundMixer.cpp','SoundMixer.h']:continue # reference for nonlinear mix; desktop backend replaced
        if name=='blip_buf.h': text=text.replace('#include "stdafx.h"','')
        elif name=='blip_buf.cpp':
            text=text.replace('#include "stdafx.h"','#include "player_alloc.h"')
            text=text.replace('#include <string.h>','').replace('#include <stdlib.h>','')
            text=text.replace('#include <assert.h>','#undef assert\n#define assert(x) do { if(!(x)) __builtin_trap(); } while(0)')
            text=text.replace('malloc(', 'player_alloc(').replace('free( m );','/* arena reset owns lifetime */')
            text=remove(text,'blip_set_rates')
            text=remove(text,'blip_clocks_needed')
            text+='\nvoid player_blip_rate(blip_t *m) { m->factor = 80521489639109ULL; }\n' # ceil(2^52 * 32000 / 1789773)
            # ARM has no libc memmove and this is only used to shift samples left.
            text=text.replace('memmove(', 'player_memmove(')
            text=text.replace('s << (delta_bits - bass_shift)','s * (1 << (delta_bits - bass_shift))')
        else:
            text=re.sub(r'^#include "(?:stdafx|Snapshotable|Console|EmulationSettings|MemoryManager|BaseMapper|IMemoryHandler|IAudioDevice)\.h"\n','',text,flags=re.M)
            text='#include "platform.h"\n'+text
            for fn in ['StreamState','GetState','PeekRAM']:text=remove(text,fn)
            text=text.replace('public Snapshotable, ','').replace(', public Snapshotable','').replace(' : public Snapshotable','')
            text=text.replace('shared_ptr<Console>','Console*').replace('shared_ptr<SoundMixer>','SoundMixer*')
            text=re.sub(r'unique_ptr<(\w+)>',r'PlayerPtr<\1>',text)
            text=text.replace('_mixer.get()','_mixer').replace('abs(_outputLevel','player_abs(_outputLevel')
            text=text.replace('new SquareChannel','new (player_alloc(sizeof(SquareChannel))) SquareChannel')
            for cls in ['TriangleChannel','NoiseChannel','DeltaModulationChannel','ApuFrameCounter']:
                text=text.replace('new '+cls,'new (player_alloc(sizeof('+cls+'))) '+cls)
            text=text.replace('(_romInfo.DatabaseInfo.Board.find("MMC1B") != string::npos ? 0x10 : 0x00)','0x00 /* no cartridge database override */')
            text=text.replace('(_romInfo.DatabaseInfo.Board.compare("MMC1A") == 0)','false /* no database override */')
            text=text.replace('_romInfo.DatabaseInfo.Chip.substr(0, 5).compare("MMC3A") == 0','false /* default MMC3B/C; no database */')
        (out/name).write_text(text)
        patch+=''.join(difflib.unified_diff(original.splitlines(True),text.splitlines(True),'upstream/player/'+name,'generated/'+name))
    (out/'player-integration.patch').write_text(patch)
    (out/'mix_lut.h').write_text('static const uint16_t pulse_lut[]={'+','.join(str(477600*i//(8128+100*i)) for i in range(31))+'};\nstatic const uint16_t tnd_lut[]={'+','.join(str(818350*i//(24329+100*i)) for i in range(203))+'};\n')

    # Mesen EmulationSettings::GenerateFullColorPalette, computed at build time.
    colors=[int(x,16) for x in re.findall(r'0x([0-9A-Fa-f]{8})',(src/'palette.h').read_text())]
    full=[]
    for emphasis in range(8):
        for color in colors:
            rgb=[float((color>>shift)&255) for shift in (16,8,0)]
            for bit in range(3):
                if emphasis&(1<<bit):
                    rgb=[v*(1.1 if ch==bit else 0.9) for ch,v in enumerate(rgb)]
            full.append(0xff000000|(int(min(255,rgb[0]))<<16)|(int(min(255,rgb[1]))<<8)|int(min(255,rgb[2])))
    (out/'player_palette.h').write_text('static const uint32_t nes_player_palette[512]={'+','.join(hex(v) for v in full)+'};\n')
