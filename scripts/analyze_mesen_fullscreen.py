#!/usr/bin/env python3
"""Validate saved fullscreen handoff evidence; no target connection."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/'amiga/records/2026-10-09/mesen-fullscreen'
def fields(line):return dict(re.findall(r'(\w+)=([^\s]+)',line))
def analyze(name,count):
    text=(RECORD/name).read_text()
    for marker in ['MAPPING PASS','EXIT epilogue=52455431','LAUNCHER exit=0; owned memory released',
                   'MMU_RESTORE phase=3 register_mismatches=00000000','witness_bad=0',
                   'CACHE original=08c50878 running=08c5187d restored=08c50878']:
        assert marker in text,(name,marker)
    def row(prefix):return fields(next(l for l in text.splitlines() if l.startswith(prefix)))
    end=row('ZZNES END ');flip=row('FULLSCREEN_END ');direct=row('DIRECT_END ')
    assert end['exit']=='0' and int(end['frames'])==count
    assert int(flip['queued'])==int(flip['flips'])==int(direct['challenges'])==count
    assert flip['pending']=='-1' and flip['fault']=='0'
    assert int(direct['verified_frames'])==1+count//60
    assert 'READBACK FAIL' not in text
    frames=[fields(l) for l in text.splitlines() if l.startswith('FRAME ')]
    expected=[1,2,3,4,5,6] if count==6 else [1,60,120]
    assert [int(f['n']) for f in frames]==expected
    for f in frames:
        n=int(f['n']);want='48ef4dc5' if n<3 else 'd8cc1f38' if n==3 else 'ed354ee5'
        assert f['core_hash']==f['output_hash']==want
    assert int(frames[-1]['cycles'])==(176183 if count==6 else 3571159)
    return {'frames':count,'elapsed_us':int(end['elapsed_us']),
            'fps':count*1e6/int(end['elapsed_us']),
            'cpu_ppu_ms':int(end['core_total_us'])/count/1000,
            'arm_colour_copy_ms':int(direct['copy_us'])/count/1000,
            'acknowledged_flips':int(flip['flips']),
            'verified_pixel_frames':int(direct['verified_frames'])}
short=analyze('display6.log',6);run=analyze('display120.log',120)
old=json.loads((RECORD.parent/'mesen-performance/results.json').read_text())['runs']
print(json.dumps({'scope':'Original silent NROM demo, sampled pixel readback; single short run, not game FPS',
    'short_check':short,'fullscreen':run,'windowed_direct_fps':old['direct']['fps'],
    'relative_to_windowed_direct':run['fps']/old['direct']['fps'],
    'relative_to_original':run['fps']/old['legacy']['fps']},indent=2))
