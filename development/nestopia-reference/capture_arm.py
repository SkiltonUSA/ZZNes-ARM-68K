"""Capture the existing ARM payload in Unicorn, including APU writes."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import struct
import sys
from unicorn import UC_HOOK_BLOCK
from unicorn.arm_const import *

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from test_console_jit_core import Machine

p = argparse.ArgumentParser()
p.add_argument('rom', type=Path)
p.add_argument('build', type=Path)
p.add_argument('output', type=Path)
p.add_argument('--frames', type=int, default=1200)
a = p.parse_args()
base = 0x11000040
m = Machine(a.build / 'player/fceux.elf', a.build / 'core/elf.py', 48 * 1024**2, base)
m.u.reg_write(UC_ARM_REG_C1_C0_2, 0xf00000)
m.u.ctl_flush_tb()
m.u.reg_write(UC_ARM_REG_FPEXC, 0x40000000)
frame = 0
trace_file = a.output.with_suffix('.apu.csv').open('w')
trace = csv.writer(trace_file)
trace.writerow(['frame', 'cycle', 'address', 'value'])
def written(u, address, size, data):
    cycle = struct.unpack('<I', u.mem_read(m.syms['timestamp'], 4))[0]
    trace.writerow([frame, cycle, u.reg_read(UC_ARM_REG_R0), u.reg_read(UC_ARM_REG_R1) & 255])
rom = a.rom.read_bytes()
m.u.mem_write(base + 0x100000, rom)
assert m.call('_Z8nes_initPKhjPtS1_', base + 0x100000, len(rom), base + 0x90000, base + 0xb0000) == 0
for name in ['Write_PSG', 'Write_DMCRegs', 'StatusWrite', 'Write_IRQFM']:
    matches = [v for k, v in m.syms.items() if name in k]
    assert len(matches) == 1, (name, matches)
    m.u.hook_add(UC_HOOK_BLOCK, written, begin=matches[0], end=matches[0] + 3)
m.u.ctl_flush_tb()
total = 0
with a.output.with_suffix('.pcm').open('wb') as pcm, a.output.with_suffix('.csv').open('w') as frames:
    rows = csv.writer(frames)
    rows.writerow(['frame', 'samples', 'video_fnv1a', 'cycles'])
    for frame in range(1, a.frames + 1):
        assert m.call('_Z9nes_framehPFivE', 0, 0) == 0
        n = m.call('_Z10fc_samplesv')
        assert 0 <= n <= 1024
        data = struct.unpack('<' + 'i' * n, m.u.mem_read(m.syms['WaveFinal'], n * 4))
        assert m.call('_Z9nes_audioPPKs', base + 0x85000) == n
        pointer = struct.unpack('<I', m.u.mem_read(base + 0x85000, 4))[0]
        assert struct.unpack('<' + 'h' * n, m.u.mem_read(pointer, n * 2)) == data
        pcm.write(struct.pack('<' + 'h' * n, *data))
        total += n
        rows.writerow([frame, n, m.call('_Z13fc_video_hashv'), m.call('_Z10nes_cyclesv')])
        if frame % 100 == 0:
            trace_file.flush()
            print('captured ARM frame', frame, 'samples', total, flush=True)
trace_file.close()
a.output.with_suffix('.json').write_text(json.dumps({
    'frames': a.frames, 'samples': total, 'rate': 32000,
    'rom_sha256': hashlib.sha256(rom).hexdigest(),
    'elf_sha256': hashlib.sha256((a.build / 'player/fceux.elf').read_bytes()).hexdigest(),
    'pcm_sha256': hashlib.sha256(a.output.with_suffix('.pcm').read_bytes()).hexdigest(),
    'execution': 'Unicorn Cortex-A9 instruction model; not a hardware speed measurement'
}, indent=2) + '\n')
print('PASS ARM capture', total, flush=True)
