#!/usr/bin/env python3
"""Build bounded Mesen CPU/PPU NROM preview; no automatic hardware deployment."""
import argparse, difflib, hashlib, json, re, subprocess
from pathlib import Path
import build_mesen_bench as cpu
ROOT=cpu.ROOT
SRC=ROOT/'amiga/mesen_nes'
OUT=ROOT/'.context/amiga/mesen-nes'

def remove_function(text, name, replacement=''):
    match=re.search(r'^\w[^\n]*\bPPU::'+name+r'\([^\n]*\)\n\{',text,re.M)
    assert match,name
    end=match.end();depth=1
    while depth:
        depth+=(text[end]=='{')-(text[end]=='}');end+=1
    return text[:match.start()]+replacement+text[end:]

def prepare(player=False):
    cpu.OUT=OUT;cpu.prepare()
    # CPU-only compatibility header is replaced by real PPU integration.
    types=(cpu.SRC/'vendor/Types.h').read_text()
    types=(types[:types.index('struct CartridgeState')] if player else types.split('enum class PrgMemoryType')[0])+types[types.index('struct PPUControlFlags'):types.index('struct ApuLengthCounterState')]
    (OUT/'Types.h').write_text(types.replace('#include "stdafx.h"','#include <stdint.h>'))
    manifest=json.loads((SRC/'vendor/upstream.json').read_text())
    for name,sha in manifest['files'].items():
        assert hashlib.sha256((SRC/'vendor'/name).read_bytes()).hexdigest()==sha
    header=(SRC/'vendor/PPU.h').read_text()
    header=re.sub(r'^#include .*\n','',header,flags=re.M)
    header='#include "platform.h"\n'+header
    header=header.replace(' : public IMemoryHandler, public Snapshotable','').replace('shared_ptr<Console>','Console*').replace(' override','').replace('virtual ','')
    for name in ['StreamState','DebugSendFrame','DebugCopyOutputBuffer','DebugUpdateFrameBuffer','GetState','SetState','PeekRAM','GetPixelBrightness','GetOverclockRate']:
        header=re.sub(r'^.*\b'+name+r'\([^\n]*\);\n','',header,flags=re.M)
    start=header.index('\t\tvoid GetMemoryRanges(');end=header.index('\n\t\tuint8_t ReadPaletteRAM',start)
    header=header[:start]+header[end:]
    source=(SRC/'vendor/PPU.cpp').read_text()
    source=re.sub(r'^#include .*\n','',source,flags=re.M)
    source='#include "platform.h"\n#include "PPU.h"\n#include "CPU.h"\n'+source
    source=source.replace('shared_ptr<Console>','Console*')
    source=source.replace('new uint16_t[256 * 240]','console->buffers[0]',1).replace('new uint16_t[256 * 240]','console->buffers[1]',1)
    source=source.replace('delete[] _outputBuffers[0];','').replace('delete[] _outputBuffers[1];','')
    for name in ['StreamState','DebugSendFrame','DebugCopyOutputBuffer','DebugUpdateFrameBuffer','GetState','SetState','PeekRAM','GetPixelBrightness','GetOverclockRate']:
        source=remove_function(source,name)
    source=remove_function(source,'SendFrame','void PPU::SendFrame() { UpdateGrayscaleAndIntensifyBits(); _console->FrameReady(_currentOutputBuffer); }')
    source=re.sub(r'^\s*shared_ptr<Debugger> debugger[^\n]*\n\s*if\(debugger[^\n]*\n(?:[^\n]*\n)*?\s*\}', '',source,flags=re.M)
    source=re.sub(r'^\s*_console->Debug[^\n]*;','',source,flags=re.M)
    source=source.replace('std::min<uint8_t>(3, (_cycle - 256) & 0x07)','(((_cycle - 256) & 7) < 3 ? ((_cycle - 256) & 7) : 3)')
    patch=''
    for name,content in [('PPU.h',header),('PPU.cpp',source)]:
        (OUT/name).write_text(content)
        patch+=''.join(difflib.unified_diff((SRC/'vendor'/name).read_text().splitlines(True),content.splitlines(True),'upstream/'+name,'generated/'+name))
    (OUT/'ppu-integration.patch').write_text(patch)
    # CPU includes PPU Run inline definition when compiling its clock path.
    path=OUT/'CPU.cpp';path.write_text(path.read_text().replace('#include "CPU.h"','#include "CPU.h"\n#include "PPU.h"'))
    from make_nes_demo import build
    if player:(OUT/'ZZNesSoundTest.nes').write_bytes(build(player_test=True))
    rom=build();(OUT/'ZZNesDemo.nes').write_bytes(rom)
    (OUT/'demo.h').write_text('static const uint8_t demo_rom[]={'+','.join(map(str,rom))+'};\n')

def main():
    global OUT
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--arm',action='store_true');p.add_argument('--player',action='store_true',help='Accuracy-first CPU/PPU/APU and cartridge player');p.add_argument('--container-command');p.add_argument('--optimize',action='store_true',help='Compile CPU/PPU together at O3');p.add_argument('--direct',action='store_true',help='ARM copy to locked P96 off-screen bitmap');p.add_argument('--fullscreen',action='store_true',help='XX19c fullscreen deferred-PAN with three frame slots');p.add_argument('--legacy-host',action='store_true',help='Profile original 20 ms polling/byte-at-a-time conversion');a=p.parse_args()
    if a.legacy_host and (a.direct or a.optimize or a.fullscreen):p.error('--legacy-host cannot be combined with --direct/--optimize')
    if a.player:a.fullscreen=True
    if a.fullscreen:a.direct=True
    if a.direct:a.optimize=True
    if a.optimize:OUT=ROOT/'.context/amiga/mesen-nes-fast'
    if a.legacy_host:OUT=ROOT/'.context/amiga/mesen-nes-legacy'
    if a.direct:OUT=ROOT/'.context/amiga/mesen-nes-direct'
    if a.fullscreen:OUT=ROOT/'.context/amiga/mesen-nes-fullscreen'
    if a.player:OUT=ROOT/'.context/amiga/mesen-player'
    prepare(a.player)
    if a.player:
        from prepare_mesen_player import prepare as prepare_player
        prepare_player(SRC,OUT)
    sources=[OUT/'CPU.cpp',OUT/'PPU.cpp',SRC/('player_core.cpp' if a.player else 'core.cpp')]
    if a.player:sources += [OUT/'APU.cpp',OUT/'DeltaModulationChannel.cpp',OUT/'blip_buf.cpp',SRC/'mixer.cpp',SRC/'player_alloc.cpp']
    if a.optimize:
        (OUT/'unified.cpp').write_text(''.join('#include "'+str(p)+'"\n' for p in sources))
        sources=[OUT/'unified.cpp']
    flags=([ '-DNES_PLAYER','-DNES_NATIVE_TEST'] if a.player else [])+['-std=c++14','-DLIBRETRO','-O3' if a.optimize else '-O2','-fno-exceptions','-fno-rtti','-I'+str(OUT),'-I'+str(SRC)]
    subprocess.run(['clang++',*flags,'-g','-fsanitize=address,undefined',*sources,SRC/'native.cpp','-o',OUT/'nes-native'],check=True)
    run=subprocess.run([OUT/'nes-native',OUT/'ZZNesDemo.nes',OUT/'preview.ppm'],check=True,text=True,capture_output=True)
    (OUT/'native.log').write_text(run.stdout);print(run.stdout,end='')
    if a.arm:build_arm(json.loads(a.container_command) if a.container_command else None,sources,a.optimize,a.legacy_host,a.direct,a.fullscreen,a.player)

def build_arm(command,sources,optimize=False,legacy=False,direct=False,fullscreen=False,player=False):
    from build_zz9000_debug import unpack_elf
    from amiga import PIN,container_command
    bench=cpu.SRC
    flags=['--target=arm-none-eabi','-mcpu=cortex-a9','-marm','-mfloat-abi=soft','-mno-unaligned-access',
      '-ffreestanding','-fno-builtin','-fPIC','-fvisibility=hidden','-fno-stack-protector','-O2','-g',
      '-DZZ_BLOCK_SIZE=0x100000','-DZZ_CONTROL=0x80000','-DMB_MMU','-DMB_DCACHE',
      '-I'+str(OUT),'-I'+str(SRC),'-I'+str(bench),'-Iamiga/arm_debug','-Iamiga/arm_debug/zz9000']
    if player:flags+=['-DNES_PLAYER','-DMB_ALLOCATION=0x400000u'];flags=[x.replace('ZZ_BLOCK_SIZE=0x100000','ZZ_BLOCK_SIZE=0x400000') for x in flags]
    if direct:flags+=['-DNES_DIRECT'];sources=[*sources,SRC/'direct.cpp']
    objects=[]
    for source in [bench/'mmu_asm.S',bench/'mmu.c',bench/'runtime.c',SRC/'worker.cpp',*sources]:
        obj=OUT/(source.stem+'.arm.o');objects.append(obj)
        extra=['-std=c++14','-DLIBRETRO','-fno-exceptions','-fno-rtti','-nostdinc++'] if source.suffix=='.cpp' else []
        subprocess.run(['clang',*flags,*extra,*(['-O3'] if optimize and source.name=='unified.cpp' else []),'-c',source,'-o',obj],cwd=ROOT,check=True)
    ld='/opt/homebrew/opt/lld/bin/ld.lld';elf=OUT/'nes.elf'
    subprocess.run([ld,'-shared','-Bsymbolic','--no-undefined','-T',bench/'mmu_payload.ld',*objects,'-o',elf],cwd=ROOT,check=True)
    payload,relocations,entry=unpack_elf(elf.read_bytes(),0x40000)
    subprocess.run(['clang',*flags,'-c','amiga/arm_debug/zz9000/mapping_probe.S','-o',OUT/'mapping.o'],cwd=ROOT,check=True)
    subprocess.run([ld,'-shared','-Bsymbolic','--no-undefined','-T','amiga/arm_debug/zz9000/payload.ld',OUT/'mapping.o','-o',OUT/'mapping.elf'],cwd=ROOT,check=True)
    mapping,rel,point=unpack_elf((OUT/'mapping.elf').read_bytes());assert not rel and not point and len(mapping)<=1024
    def array(name,data):return 'static const unsigned char '+name+'[]={'+','.join(str(x) for x in data)+'};\n'
    (OUT/'zz_payload.h').write_text(f'#define ZZ_ENTRY {entry}u\n'+array('zz_image',payload)+array('zz_mapping_probe',mapping)+
       'static const unsigned long zz_relocations[]={'+','.join(str(x) for x in relocations)+'};\n')
    relative=OUT.relative_to(ROOT);command=command or container_command()
    subprocess.run([*command,'run','--rm','--platform','linux/amd64','-v',f'{ROOT}:/work','-w','/work',PIN['image'],
      'm68k-amigaos-gcc','-std=c99','-noixemul','-m68020','-O2','-g','-Wall','-Wextra','-Werror',
      '-DZZ_HEADLESS_BENCH','-DZZ_RELEASE','-DZZ_NES',('-DZZ_BLOCK_SIZE=0x400000' if player else '-DZZ_BLOCK_SIZE=0x100000'),'-DZZ_CONTROL=0x80000',
      '-DZZ_APP_NAME="ZZNes"',('-DZZ_APP_VERSION="0.3.3-dev"' if player else '-DZZ_APP_VERSION="0.2-dev"'),'-DZZ_MIN_STACK=65536',
      *(['-DNES_PLAYER','-DMB_ALLOCATION=0x400000u'] if player else []),*(['-DNES_LEGACY_HOST'] if legacy else []),*(['-DNES_DIRECT'] if direct else []),*(['-DNES_FULLSCREEN'] if fullscreen else []),'-DMB_MMU','-DMB_DCACHE','-DZZ_HEADLESS_MMU','-DZZ_HEADLESS_ICACHE',
      '-Iamiga/mesen_nes','-Iamiga/mesen_bench','-Iamiga/arm_debug','-Iamiga/arm_debug/zz9000','-I'+str(relative),
      'amiga/arm_debug/zz9000/launcher.c','amiga/mesen_nes/host.c','-lamiga','-o',str(relative/'ZZNes')],cwd=ROOT,check=True)
    binary=OUT/'ZZNes';assert binary.read_bytes()[:4]==b'\0\0\x03\xf3'
    recorded=[*SRC.rglob('*'),*bench.glob('mmu*'),bench/'runtime.c',ROOT/'scripts/build_mesen_nes.py',ROOT/'scripts/build_mesen_bench.py',
      ROOT/'scripts/make_nes_demo.py',ROOT/'scripts/prepare_mesen_player.py',ROOT/'amiga/arm_debug/zz9000/launcher.c',ROOT/'amiga/arm_debug/zz9000/layout.h',
      ROOT/'amiga/arm_debug/zz9000/mapping_probe.S',ROOT/'amiga/arm_debug/protocol.h',*bench.joinpath('vendor').glob('*')]
    record={'scope':('Accuracy-first NTSC Mesen CPU/PPU/APU; mapper 0/1/2/3/4/7/90 player candidate' if player else 'Mesen CPU+PPU NTSC NROM, silent preview'),
      'cache_policy':'private MMU/L1; outer NC; output clean-to-PoC before ACK; host reads only while ARM idle',
      'core_optimization':'unified O3' if optimize else 'separate O2','legacy_host':legacy,'direct':direct,'fullscreen':fullscreen,'player':player,'image_bytes':len(payload),'relocations':len(relocations),'compiler':subprocess.check_output(['clang','--version'],text=True),
      'flags':[x for x in flags if not x.startswith('-I')],
      'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in recorded if p.is_file()},
      'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [elf,binary,OUT/'ppu-integration.patch',OUT/'native.log',OUT/'ZZNesDemo.nes']},
      'executable_md5':hashlib.md5(binary.read_bytes()).hexdigest()}
    (OUT/'build.json').write_text(json.dumps(record,indent=2)+'\n')
    print(f'Built {binary}: {binary.stat().st_size} bytes; ARM image {len(payload)} bytes; {len(relocations)} relocations')

if __name__=='__main__':main()
