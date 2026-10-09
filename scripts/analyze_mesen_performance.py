#!/usr/bin/env python3
"""Compare matched Mesen original-demo runs. Reads saved evidence only."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/'amiga/records/2026-10-09/mesen-performance'
def fields(line):return dict(re.findall(r'(\w+)=([^\s]+)',line))
def analyze(name):
    text=(RECORD/(name+'.log')).read_text()
    for marker in ['MAPPING PASS','EXIT epilogue=52455431','LAUNCHER exit=0; owned memory released',
      'MMU_RESTORE phase=3 register_mismatches=00000000','witness_bad=0',
      'CACHE original=08c50878 running=08c5187d restored=08c50878']:
        assert marker in text,(name,marker)
    end=fields(next(l for l in text.splitlines() if l.startswith('ZZNES END')))
    profile=fields(next(l for l in text.splitlines() if l.startswith('PROFILE ')))
    frames=int(end['frames']);assert frames==120 and end['exit']=='0'
    rows=[fields(l) for l in text.splitlines() if l.startswith('FRAME ')]
    assert [int(r['n']) for r in rows]==[1,60,120]
    for row in rows:
        want='48ef4dc5' if row['n']=='1' else 'ed354ee5'
        assert row['core_hash']==row['output_hash']==want,(name,row)
    assert end['output_hash']=='ed354ee5'
    elapsed=int(end['elapsed_us'])
    result={'frames':frames,'wall_us':elapsed,'fps':frames*1e6/elapsed,
      'core_ms':int(end['core_total_us'])/frames/1000,
      **{k+'_ms':int(profile[k+'_us'])/frames/1000 for k in ['request','copy','colour','draw']}}
    if name=='direct':
        direct=fields(next(l for l in text.splitlines() if l.startswith('DIRECT_END ')))
        assert int(direct['challenges'])==frames and int(direct['verified_frames'])==3
        assert 'READBACK FAIL' not in text
        result.update(arm_colour_copy_ms=int(direct['copy_us'])/frames/1000,
          bitmap_verified_frames=3,validation='ARM hashes and address challenges every frame; full bitmap readback frames 1/60/120')
    else:result['validation']='ARM and 68k output hashes every frame'
    return result
runs={name:analyze(name) for name in ['legacy','host','fast','direct']}
report={'scope':'120-frame original silent NROM demo; validation policy differs for direct; not general NES game FPS',
 'runs':runs,'speedup':runs['fast']['fps']/runs['legacy']['fps'],
 'direct_speedup':runs['direct']['fps']/runs['legacy']['fps'],
 'core_speedup':runs['legacy']['core_ms']/runs['fast']['core_ms']}
print(json.dumps(report,indent=2))
