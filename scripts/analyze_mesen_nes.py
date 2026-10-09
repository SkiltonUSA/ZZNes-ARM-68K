#!/usr/bin/env python3
"""Reproduce the bounded CPU/PPU acceptance record; no hardware access."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
d=ROOT/'amiga/records/2026-10-09/mesen-nes'
expected=['48ef4dc5','48ef4dc5','d8cc1f38']+['ed354ee5']*3
runs=[]
for name in ['core.log','display6.log']:
    log=(d/name).read_text()
    rows=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in log.splitlines() if line.startswith('FRAME ')]
    assert len(rows)==6
    assert [r['core_hash'] for r in rows]==expected
    assert [r['output_hash'] for r in rows]==expected
    assert [int(r['n']) for r in rows]==list(range(1,7))
    for required in ['MAPPING PASS','EXIT epilogue=52455431','LAUNCHER exit=0; owned memory released',
        'MMU_RESTORE phase=3 register_mismatches=00000000','witness_bad=0',
        'CACHE original=08c50878 running=08c5187d restored=08c50878']:
        assert required in log,(name,required)
    end=dict(re.findall(r'(\w+)=([^\s]+)',next(x for x in log.splitlines() if x.startswith('ZZNES END'))))
    runs.append({'log':name,'frames':6,'hashes_match':True,'clean_exit':True,
      'populated_frame_core_us':[int(r['cpu_ppu_us']) for r in rows[3:]],'wall_us':int(end['elapsed_us'])})
native=(d/'native.log').read_text();assert 'hash=ed354ee5' in native and 'CONTROLLER right=10_frames hash=9bbb3e9b PASS' in native
report={'scope':'six-frame correctness and shutdown acceptance; no game FPS claim','runs':runs,
  'earlier_unexpected_self_restart':'unresolved; occurred during display/capture sequence; not reproduced by isolated core/display runs',
  'display_depth':24,'physical_monitor_appearance':'not user-confirmed','sound':'absent',
  'ntsc_frame_budget_us':16639,'full_speed_nes_established':False}
interactive=(d/'interactive.log').read_text()
assert 'LAUNCHER exit=0; owned memory released' in interactive
assert 'EXIT epilogue=52455431' in interactive
assert 'MMU_RESTORE phase=3 register_mismatches=00000000' in interactive
assert 'witness_bad=0' in interactive
rows=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in interactive.splitlines() if line.startswith('FRAME ')]
assert all(row['core_hash']==row['output_hash'] for row in rows)
assert len({row['output_hash'] for row in rows if int(row['n'])>=60})>1
end=dict(re.findall(r'(\w+)=([^\s]+)',next(x for x in interactive.splitlines() if x.startswith('ZZNES END'))))
assert end['exit']=='0' and int(end['frames'])==1104
report['physical_monitor_appearance']='user confirmed picture and arrow-key movement'
report['interactive']={'frames':int(end['frames']), 'wall_us':int(end['elapsed_us']),
    'observed_demo_fps':int(end['frames'])*1e6/int(end['elapsed_us']),
    'core_mean_us':int(end['core_total_us'])/int(end['frames']),
    'exit':'Q before frame limit; clean restoration/return', 'screenshot_capture':False}
print(json.dumps(report,indent=2))
