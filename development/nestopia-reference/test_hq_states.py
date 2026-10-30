"""Replay linked ARM states in the instruction model, including fresh relocation.
Private ROMs are optional; the default is a generated square-wave NROM.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'development/output-quality-20261030')]
from test_console_jit_core import Machine
from test_core_quality import square_rom
from unicorn.arm_const import UC_ARM_REG_C1_C0_2, UC_ARM_REG_FPEXC

CAP = 122880
STORE = '_Z14fc_state_storePhj'
LOAD = '_Z13fc_state_loadPKhj'


def machine(build, rom, base, pal):
    m = Machine(build / 'player/fceux.elf', build / 'core/elf.py', 48 * 1024**2, base)
    m.u.reg_write(UC_ARM_REG_C1_C0_2, 0xf00000)
    m.u.ctl_flush_tb()
    m.u.reg_write(UC_ARM_REG_FPEXC, 0x40000000)
    m.u.mem_write(base + 0x100000, rom)
    m.call('_Z13fc_set_regionj', int(pal))
    assert m.call('_Z8nes_initPKhjPtS1_', base + 0x100000, len(rom), base + 0x90000, base + 0xb0000) == 0
    return m


def frame(m, i):
    assert m.call('_Z9nes_framehPFivE', 8 if i % 31 == 0 else 0, 0) == 0
    n = m.call('_Z10fc_samplesv')
    pcm = bytes(m.u.mem_read(m.syms['WaveFinal'], 4 * n))
    return (m.call('_Z10nes_cyclesv'), m.call('_Z13fc_video_hashv'), n, pcm)


def save(m):
    n = m.call(STORE, m.base + 0xe0000, CAP)
    assert 32 < n <= CAP
    return bytes(m.u.mem_read(m.base + 0xe0000, n))


def load(m, data):
    m.u.mem_write(m.base + 0xe0000, data)
    return m.call(LOAD, m.base + 0xe0000, len(data))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('build', type=Path)
    p.add_argument('--rom', type=Path)
    p.add_argument('--pal', action='store_true')
    p.add_argument('--warmup', type=int, default=120)
    p.add_argument('--frames', type=int, default=60)
    p.add_argument('--output', type=Path)
    p.add_argument('--state', type=Path)
    a = p.parse_args()
    rom = a.rom.read_bytes() if a.rom else square_rom()
    m = machine(a.build, rom, 0x11000040, a.pal)
    for i in range(a.warmup):frame(m, i)
    saved = save(m)
    assert m.call(STORE, m.base + 0xe0000, len(saved)-1) == 0
    reference = [frame(m, i) for i in range(a.frames)]
    assert load(m, saved) == 1
    for i, expected in enumerate(reference):
        assert frame(m, i) == expected, ('same-process replay', i)
    after = save(m)
    assert struct.unpack_from('<II', after, 24) == (0x20261030, int(a.pal))
    # Corrupt header/payload and a real legacy envelope: all reject before mutation.
    for pos in (0, 4, 8, 12, 16, 20, 24, 28, 32, len(saved)-1):
        bad = bytearray(saved);bad[pos] ^= 0x80
        assert load(m, bytes(bad)) == 0, pos
        assert save(m) == after, ('mutated on rejection', pos)
    legacy = bytearray(saved)
    struct.pack_into('<I', legacy, 4, 1)
    struct.pack_into('<I', legacy, 24, 0x20261011)
    assert load(m, bytes(legacy)) == 0 and save(m) == after
    assert load(m, saved[:-1]) == 0 and save(m) == after
    fresh = machine(a.build, rom, 0x150020c0, a.pal)
    assert load(fresh, saved) == 1
    for i, expected in enumerate(reference):
        assert frame(fresh, i) == expected, ('fresh relocated replay', i)
    result = dict(test='ARM instruction model, not physical hardware',
        rom_sha256=hashlib.sha256(rom).hexdigest(),
        elf_sha256=hashlib.sha256((a.build/'player/fceux.elf').read_bytes()).hexdigest(),
        pal=a.pal, warmup=a.warmup, replay_frames=a.frames, state_bytes=len(saved),
        pcm_sha256=hashlib.sha256(b''.join(x[3] for x in reference)).hexdigest(),
        same_process=True, fresh_relocated_process=True, invalid_states_unchanged=True)
    if a.output:a.output.write_text(json.dumps(result, indent=2)+'\n')
    if a.state:a.state.write_bytes(saved)
    print('PASS HQ state replay', json.dumps(result), flush=True)


if __name__ == '__main__':main()
