"""Compare matched q0/q1 ARM cores; no hardware or commercial ROM required."""
import argparse
import hashlib
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from test_console_jit_core import Machine
from unicorn.arm_const import *


def square_rom():
    # NROM, one 440 Hz square channel, fixed volume, length counter halted.
    code = bytearray.fromhex('78 d8 a2 ff 9a')
    for address, value in [(0x2000, 0), (0x2001, 0), (0x4015, 1),
                           (0x4000, 0xbf), (0x4001, 0),
                           (0x4002, 0xfd), (0x4003, 0)]:
        code.extend([0xa9, value, 0x8d, address & 255, address >> 8])
    loop = 0xc000 + len(code)
    code.extend([0x4c, loop & 255, loop >> 8])
    prg = bytearray(16384)
    prg[:len(code)] = code
    prg[-6:] = struct.pack('<HHH', 0xc000, 0xc000, 0xc000)
    return b'NES\x1a\x01\x01' + bytes(10) + prg + bytes(8192)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--rom', type=Path)
    p.add_argument('--frames', type=int, default=24)
    p.add_argument('--exact', action='store_true', help='Compare HQ scalar versus SIMD samples exactly')
    p.add_argument('--fallback', action='store_true', help='Keep NEON disabled in exact comparison')
    p.add_argument('--candidate', type=Path)
    p.add_argument('--baseline', type=Path)
    p.add_argument('--scalar-reference', action='store_true')
    p.add_argument('--allow-audio-change', action='store_true')
    p.add_argument('--pal', action='store_true')
    a = p.parse_args()
    rom = a.rom.read_bytes() if a.rom else square_rom()
    machines = []
    for quality, base in [(0, 0x11000040), (1, 0x150020c0)]:
        build = ROOT / ('.context/audio-core-q1-build' + ('-neon' if quality else '') if a.exact else f'.context/audio-core-q{quality}-build')
        if quality and a.candidate:build=a.candidate
        if not quality and a.baseline:build=a.baseline
        m = Machine(build / 'player/fceux.elf', build / 'core/elf.py',
                    48 * 1024**2, base)
        if a.exact and not a.fallback and (quality or not a.scalar_reference):
            m.u.reg_write(UC_ARM_REG_C1_C0_2, 0xf00000)
            m.u.ctl_flush_tb()
            m.u.reg_write(UC_ARM_REG_FPEXC, 0x40000000)
            m.u.reg_write(UC_ARM_REG_FPSCR, 0xa0000000)
            for r in range(UC_ARM_REG_D0, UC_ARM_REG_D31+1):
                m.u.reg_write(r, 0x0123456789abcdef)
        m.u.mem_write(base + 0x100000, bytes(rom))
        if a.pal:m.call('_Z13fc_set_regionj',1)
        assert m.call('_Z8nes_initPKhjPtS1_', base + 0x100000, len(rom),
                      base + 0x90000, base + 0xb0000) == 0
        machines.append(m)
    different = 0
    counts = [0, 0]
    peaks = [0, 0]
    for frame in range(a.frames):
        endpoints = []
        sounds = []
        for i, m in enumerate(machines):
            assert m.call('_Z9nes_framehPFivE', 0, 0) == 0
            endpoints.append((m.call('_Z10nes_cyclesv'),
                              m.call('_Z13fc_video_hashv'),
                              bytes(m.u.mem_read(m.syms['X'], 32))))
            n = m.call('_Z10fc_samplesv')
            assert 0 < n <= 1024
            pcm = struct.unpack('<' + str(n) + 'i', m.u.mem_read(m.syms['WaveFinal'], n * 4))
            assert all(-32768 <= v <= 32767 for v in pcm)
            counts[i] += n
            peaks[i] = max(peaks[i], max(abs(v) for v in pcm))
            sounds.append(pcm)
        assert endpoints[0] == endpoints[1], frame
        if a.exact:
            if not a.allow_audio_change:assert sounds[0] == sounds[1], ('audio differs', frame)
            if not a.fallback:
                assert all(machines[1].u.reg_read(r)==0x0123456789abcdef for r in range(UC_ARM_REG_D0, UC_ARM_REG_D31+1)), ('FP state', frame)
                assert machines[1].u.reg_read(UC_ARM_REG_FPSCR)==0xa0000000
                assert machines[1].u.reg_read(UC_ARM_REG_C1_C0_2)==0xf00000
                assert machines[1].u.reg_read(UC_ARM_REG_FPEXC)==0x40000000
        different += sounds[0] != sounds[1]
    if not a.rom and not a.exact:
        assert different and all(peaks), (different, peaks)
    if a.allow_audio_change:assert different
    # The FIR has an initial history delay, not a different steady sample rate.
    assert abs(counts[0] - counts[1]) < 64, counts
    print(f'PASS {a.frames} frames: exact={a.exact} fallback={a.fallback}; identical CPU/video endpoints; '
          f'samples={counts}, peaks={peaks}, audio differences={different}; PAL={a.pal}; ROM SHA256={hashlib.sha256(rom).hexdigest()}')


if __name__ == '__main__':
    main()
