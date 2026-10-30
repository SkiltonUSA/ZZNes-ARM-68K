"""Compare private reference captures; emit measurements without ROM/audio data."""
import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import struct
import wave

def rows(path):
    with path.open() as f:
        return [{k: int(v) for k, v in row.items()} for row in csv.DictReader(f)]

def pcm(path):
    data = path.read_bytes()
    assert len(data) % 2 == 0
    return struct.unpack('<' + 'h' * (len(data) // 2), data)

def stats(path, rate):
    samples = pcm(path)
    return dict(samples=len(samples), seconds=len(samples) / rate,
                minimum=min(samples), maximum=max(samples),
                clipped=sum(v in (-32768, 32767) for v in samples),
                rms=math.sqrt(sum(v*v for v in samples) / len(samples)),
                sha256=hashlib.sha256(path.read_bytes()).hexdigest())

p = argparse.ArgumentParser()
p.add_argument('captures', type=Path)
p.add_argument('physical_wav', type=Path)
p.add_argument('output', type=Path)
a = p.parse_args()
b = a.captures
reference = [r for r in rows(b / 'nestopia-trace.apu.csv') if r['frame']]
arm = rows(b / 'zznes-smw.apu.csv')
assert len(reference) >= len(arm) > 0
assert [(r['address'], r['value']) for r in reference[:len(arm)]] == [(r['address'], r['value']) for r in arm]
frame_delta = Counter(z['frame'] - n['frame'] for n, z in zip(reference, arm))
cycle_delta = [z['cycle'] - n['cycle'] for n, z in zip(reference, arm)]
assert frame_delta == {1: len(arm)}
assert (b / 'nestopia-trace.pcm').read_bytes() == (b / 'smw-48000-f1-p0.pcm').read_bytes()
assert (b / 'smw-48000-f1-p1.pcm').read_bytes() == (b / 'smw-48000-f1-p0.pcm').read_bytes()
videos = [r['video_fnv1a'] for r in rows(b / 'smw-48000-f1-p0.csv')]
for name in ['smw-48000-f1-p1', 'smw-48000-f0-p0', 'smw-32000-f1-p0', 'nestopia-trace']:
    assert videos == [r['video_fnv1a'] for r in rows(b / (name + '.csv'))]

expected = pcm(b / 'zznes-smw.pcm')
with wave.open(str(a.physical_wav)) as w:
    assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, 32000)
    physical = struct.unpack('<' + 'h' * w.getnframes(), w.readframes(w.getnframes()))
assert len(expected) == len(physical)
counts = [r['samples'] for r in rows(b / 'zznes-smw.csv')]
assert sum(counts) == len(expected)
different = previous = bad_frames = offset = 0
for frame, count in enumerate(counts):
    bad = [i for i in range(count) if expected[offset+i] != physical[offset+i]]
    different += len(bad)
    bad_frames += bool(bad)
    if frame:
        previous += sum(physical[offset+i] == expected[offset-counts[frame-1]+i]
                        for i in bad if i < counts[frame-1])
    offset += count
result = dict(
    nestopia_commit='27246144887c78154584515f530c61497e92cd05',
    captures={name: stats(b / (name + '.pcm'), rate) for name, rate in [
        ('smw-48000-f1-p0', 48000), ('smw-48000-f0-p0', 48000),
        ('smw-32000-f1-p0', 32000), ('contra-48000-f1-p0', 48000), ('zznes-smw', 32000)]},
    pop_reducer_identical=True, instrumentation_pcm_identical=True,
    filter_variants_video_identical=True,
    writes=dict(matched_prefix=len(arm), reference_total=len(reference),
                frame_delta=dict(frame_delta), cycle_delta_range=[min(cycle_delta), max(cycle_delta)],
                dmc_enabled_writes=sum(r['address'] == 0x4015 and bool(r['value'] & 16) for r in arm)),
    earlier_amiga_capture=dict(samples=len(expected), different_samples=different,
                               previous_frame_matches=previous, affected_frames=bad_frames),
    scope='Native reference and ARM instruction-model captures; no A9 performance claim.'
)
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.write_text(json.dumps(result, indent=2) + '\n')
print('PASS reference comparison; matched APU writes:', len(arm))
print('Earlier Amiga capture: mismatched samples', different, 'previous-frame matches', previous)
