#!/usr/bin/env python3
"""Reproducible CPU-only Mesen benchmark. Does not deploy or launch hardware."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'amiga/mesen_bench'
OUT = ROOT / '.context/amiga/mesen-bench'

def prepare():
    OUT.mkdir(parents=True, exist_ok=True)
    vendor = SRC / 'vendor'
    manifest = json.loads((vendor / 'upstream.json').read_text())
    for name, sha in manifest['files'].items():
        assert hashlib.sha256((vendor / name).read_bytes()).hexdigest() == sha, name
    fixtures = json.loads((SRC / 'fixtures.json').read_text())
    for name, sha in fixtures['files'].items():
        dest = OUT / name
        if not dest.exists():
            url = f"https://raw.githubusercontent.com/christopherpow/nes-test-roms/{fixtures['commit']}/other/{name}"
            dest.write_bytes(urllib.request.urlopen(url, timeout=30).read())
        assert hashlib.sha256(dest.read_bytes()).hexdigest() == sha, name
    # Keep opcode/address/cycle logic intact. Replace only ownership and
    # desktop headers, fixed reset alignment and unused snapshot integration.
    header = (vendor / 'CPU.h').read_text()
    header = header.replace('#include "stdafx.h"\n#include "Snapshotable.h"\n#include "Types.h"', '#include "platform.h"')
    header = header.replace('class CPU : public Snapshotable', 'class CPU')
    header = header.replace('shared_ptr<Console>', 'Console*')
    header = header.replace('\tvoid StreamState(bool saving) override;', '')
    cpp = (vendor / 'CPU.cpp').read_text()
    cpp = re.sub(r'^#include .*\n', '', cpp, flags=re.M)
    cpp = '#include "platform.h"\n#include "CPU.h"\n#define assert(x) ((void)0)\n' + cpp
    cpp = cpp.replace('shared_ptr<Console>', 'Console*')
    start = cpp.index('\tif(_console->GetSettings()->CheckFlag(EmulationFlags::RandomizeCpuPpuAlignment))')
    end = cpp.index('\n\t_masterClock += cpuDivider + cpuOffset;', start)
    cpp = cpp[:start] + '\t_ppuOffset = 1; // fixed upstream non-randomized alignment\n' + cpp[end:]
    cpp = cpp[:cpp.index('\nvoid CPU::StreamState(bool saving)')]
    types = (vendor / 'Types.h').read_text().split('enum class PrgMemoryType')[0]
    types = types.replace('#include "stdafx.h"', '#include <stdint.h>')
    patch = ''
    for name, text in [('CPU.h', header), ('CPU.cpp', cpp), ('Types.h', types)]:
        (OUT / name).write_text(text)
        patch += ''.join(difflib.unified_diff((vendor / name).read_text().splitlines(True), text.splitlines(True), 'upstream/'+name, 'generated/'+name))
    (OUT / 'integration.patch').write_text(patch)
    rom = (OUT / 'nestest.nes').read_bytes()
    assert rom[:6] == b'NES\x1a\x01\x01' and len(rom) == 24592
    rows = []
    for line in (OUT / 'nestest.log').read_text().splitlines():
        m = re.match(r'([0-9A-F]{4}) .*A:([0-9A-F]{2}) X:([0-9A-F]{2}) Y:([0-9A-F]{2}) P:([0-9A-F]{2}) SP:([0-9A-F]{2}).*CYC:(\d+)$', line)
        assert m, line
        pc, a, x, y, p, sp = [int(s,16) for s in m.groups()[:6]]
        rows.append(f'{{{pc},{sp},{(a<<24)|(x<<16)|(y<<8)|p}u,{int(m[7])}u}}')
    assert len(rows) == 8991
    (OUT / 'fixture.h').write_text('#pragma once\nstruct Trace { uint16_t pc,sp; uint32_t regs,cycles; };\n'
        + f'#define TRACE_COUNT {len(rows)}u\nstatic const Trace reference_trace[]={{\n'
        + ',\n'.join(rows) + '};\nstatic const uint8_t nestest_prg[]={\n'
        + ','.join(str(x) for x in rom[16:16400]) + '};\n')
    return manifest, fixtures

def main():
    global OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--arm', action='store_true')
    parser.add_argument('--icache', action='store_true', help='Explicit local instruction-cache experiment; MMU/D-cache stay off')
    parser.add_argument('--private-mmu', action='store_true', help='Owned pages via private MMU/I-cache; D-cache off')
    parser.add_argument('--private-cache', action='store_true', help='Owned pages via private MMU/I/D; outer cache remains NC')
    parser.add_argument('--container-command', help='JSON container argv override')
    a = parser.parse_args()
    if a.icache:
        OUT=ROOT/'.context/amiga/mesen-bench-icache'
    if sum([a.icache,a.private_mmu,a.private_cache])>1:parser.error('Choose one cache mode')
    if a.private_mmu:OUT=ROOT/'.context/amiga/mesen-bench-mmu'
    if a.private_cache:OUT=ROOT/'.context/amiga/mesen-bench-cache'
    prepare()
    flags = ['-std=c++14','-DLIBRETRO','-O2','-fno-exceptions','-fno-rtti','-I'+str(OUT),'-I'+str(SRC)]
    native = OUT / 'mesen-native'
    subprocess.run(['clang++',*flags,'-g','-fsanitize=address,undefined',OUT/'CPU.cpp',SRC/'bench.cpp',SRC/'native.cpp','-o',native],check=True)
    result = subprocess.run([native],check=True,text=True,capture_output=True)
    (OUT/'native.log').write_text(result.stdout)
    print(result.stdout,end='')
    if a.arm:
        build_arm(json.loads(a.container_command) if a.container_command else None,a.icache,
                  a.private_mmu or a.private_cache,a.private_cache)

def build_arm(command=None,icache=False,mmu=False,dcache=False):
    from build_zz9000_debug import unpack_elf
    from amiga import PIN, container_command
    includes=['-I'+str(OUT),'-I'+str(SRC),'-Iamiga/arm_debug','-Iamiga/arm_debug/zz9000']
    flags=['--target=arm-none-eabi','-mcpu=cortex-a9','-marm','-mfloat-abi=soft','-mno-unaligned-access',
        '-ffreestanding','-fno-builtin','-fPIC','-fvisibility=hidden','-fno-stack-protector',
        '-O2','-g','-DZZ_BLOCK_SIZE=0x100000','-DZZ_CONTROL=0x80000',*includes]
    if icache:flags+=['-DMB_ICACHE']
    if mmu:flags+=['-DMB_MMU']
    if dcache:flags+=['-DMB_DCACHE']
    objects=[]
    entry_source=SRC/'mmu_asm.S' if mmu else SRC/'entry.S' if icache else ROOT/'amiga/arm_debug/zz9000/entry.S'
    sources=[entry_source,SRC/'worker.cpp',OUT/'CPU.cpp',SRC/'bench.cpp',SRC/'runtime.c']
    if mmu:sources.append(SRC/'mmu.c')
    for source in sources:
        obj=OUT/(source.stem+'.arm.o');objects.append(obj)
        extra=['-std=c++14','-DLIBRETRO','-fno-exceptions','-fno-rtti','-nostdinc++'] if source.suffix=='.cpp' else []
        subprocess.run(['clang',*flags,*extra,'-c',source,'-o',obj],cwd=ROOT,check=True)
    ld='/opt/homebrew/opt/lld/bin/ld.lld'
    elf=OUT/'mesen.elf'
    image_limit=0x40000 if mmu else 0x80000
    linker=SRC/'mmu_payload.ld' if mmu else ROOT/'amiga/arm_debug/zz9000/payload.ld'
    subprocess.run([ld,'-shared','-Bsymbolic','--no-undefined',f'--defsym=ZZ_IMAGE_LIMIT={image_limit}',
        '-T',linker,*objects,'-o',elf],cwd=ROOT,check=True)
    payload,relocations,entry=unpack_elf(elf.read_bytes(),image_limit)
    subprocess.run(['clang',*flags,'-c','amiga/arm_debug/zz9000/mapping_probe.S','-o',OUT/'mapping.o'],cwd=ROOT,check=True)
    subprocess.run([ld,'-shared','-Bsymbolic','--no-undefined','-T','amiga/arm_debug/zz9000/payload.ld',
        OUT/'mapping.o','-o',OUT/'mapping.elf'],cwd=ROOT,check=True)
    mapping,rel,point=unpack_elf((OUT/'mapping.elf').read_bytes())
    assert not rel and not point and len(mapping)<=1024
    def array(name,data):
        return 'static const unsigned char '+name+'[]={'+','.join(str(x) for x in data)+'};\n'
    (OUT/'zz_payload.h').write_text(f'#define ZZ_ENTRY {entry}u\n'+array('zz_image',payload)+
        array('zz_mapping_probe',mapping)+'static const unsigned long zz_relocations[]={'+
        ','.join(str(x) for x in relocations)+'};\n')
    log=(OUT/'native.log').read_text()
    cycles=int(re.search(r'cycles=(\d+)',log)[1]);digest=int(re.search(r'hash=([0-9a-f]+)',log)[1],16)
    (OUT/'expected.h').write_text(f'#define MESEN_EXPECT_CYCLES {cycles}u\n#define MESEN_EXPECT_HASH 0x{digest:08x}u\n')
    relative=OUT.relative_to(ROOT)
    command = command or container_command()
    if not isinstance(command,list) or not command or not all(isinstance(x,str) and x for x in command):
        raise ValueError('Nonempty container argv required')
    subprocess.run([*command,'run','--rm','--platform','linux/amd64',
        '-v',f'{ROOT}:/work','-w','/work',PIN['image'],'m68k-amigaos-gcc',
        '-std=c99','-noixemul','-m68020','-O2','-g','-Wall','-Wextra','-Werror',
        '-DZZ_HEADLESS_BENCH','-DZZ_RELEASE','-DZZ_BLOCK_SIZE=0x100000','-DZZ_CONTROL=0x80000',
        '-DZZ_APP_NAME="ZZMesenBench"','-DZZ_APP_VERSION="0.1"','-DZZ_MIN_STACK=65536',
        *(['-DMB_ICACHE','-DZZ_HEADLESS_ICACHE'] if icache else []),
        *(['-DMB_MMU','-DZZ_HEADLESS_MMU','-DZZ_HEADLESS_ICACHE'] if mmu else []),
        *(['-DMB_DCACHE'] if dcache else []),
        '-Iamiga/arm_debug','-Iamiga/arm_debug/zz9000','-Iamiga/mesen_bench',
        '-I'+str(relative),'amiga/arm_debug/zz9000/launcher.c','amiga/mesen_bench/host.c',
        '-lamiga','-o',str(relative/'ZZMesenBench')],cwd=ROOT,check=True)
    binary=OUT/'ZZMesenBench';assert binary.read_bytes()[:4]==b'\0\0\x03\xf3'
    recorded=[*SRC.rglob('*'),ROOT/'scripts/build_mesen_bench.py',ROOT/'amiga/arm_debug/zz9000/entry.S',
        ROOT/'amiga/arm_debug/zz9000/launcher.c',ROOT/'amiga/arm_debug/zz9000/layout.h',
        ROOT/'amiga/arm_debug/zz9000/payload.ld',ROOT/'amiga/arm_debug/zz9000/mapping_probe.S',
        ROOT/'amiga/arm_debug/protocol.h']
    record={'scope':'Mesen CPU ONLY; no PPU/APU/game FPS','cache_policy':'I-cache on, MMU/D-cache off' if icache else 'MMU/I-cache/D-cache off',
        'compiler':subprocess.check_output(['clang','--version'],text=True),
        'flags':[x for x in flags if not x.startswith('-I')], 'upstream':json.loads((SRC/'vendor/upstream.json').read_text()),
        'fixtures':json.loads((SRC/'fixtures.json').read_text()),'image_bytes':len(payload),
        'relocations':len(relocations),'trace_states':8991,'expected_cycles':cycles,'expected_hash':f'{digest:08x}',
        'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in recorded if p.is_file()},
        'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [elf,binary,OUT/'integration.patch',OUT/'native.log']},
        'executable_md5':hashlib.md5(binary.read_bytes()).hexdigest()}
    if mmu:record['cache_policy']='Private MMU/I ON; D '+('ON' if dcache else 'OFF')+'; outer/shared/table NC'
    (OUT/'build.json').write_text(json.dumps(record,indent=2)+'\n')
    print(f'Built {binary}: {binary.stat().st_size} bytes; ARM payload {len(payload)} bytes; {len(relocations)} relocations')

if __name__ == '__main__':
    main()
