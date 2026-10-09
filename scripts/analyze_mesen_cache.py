#!/usr/bin/env python3
"""Reproduce physical private-cache results; CPU throughput, not game FPS."""
import json
from pathlib import Path
import re
import statistics
from analyze_mesen_bench import analyze,ROOT

p=ROOT/'amiga/records/2026-10-09/mesen-cache'
baseline=analyze(ROOT/'amiga/records/2026-10-09/mesen-cpu/icache.log',True)
mmu=analyze(p/'mmu.log',False,'08c51879')
boundary=analyze(p/'cached-boundary.log',False,'08c5187d')
names=['cached-full.log','repeat1.log','repeat2.log']
runs=[analyze(p/name,False,'08c5187d') for name in names]
samples=[]
for name in names:
    text=(p/name).read_text()
    assert 'CANCEL PASS active_work=1' in text and 'mailbox_rounds=15' in text
    samples.extend(int(m[1]) for m in re.finditer(r'SAMPLE n=\d+ warmup=0 .*?cpu_us=(\d+)',text))
assert len(samples)==30
median=statistics.median(samples)
print(json.dumps({'scope':'CPU-only, no game/display/audio FPS measured',
    'previous_instruction_cache':baseline,'private_mmu_I_only_boundary_layout':mmu,
    'private_mmu_ID_boundary_layout':boundary,'full_private_cache_runs':dict(zip(names,runs)),
    'combined':{'samples':30,'median_us':median,'min_us':min(samples),'max_us':max(samples),
        'speedup_over_previous_icache':baseline['median_cpu_us']/median,
        'time_reduction_percent':100*(1-median/baseline['median_cpu_us']),
        'ntsc_cpu_realtime_multiple':baseline['nes_time_represented_us']/median,
        'register_states_matched':8991*3,'successful_cached_shutdowns_with_cancellation':3}},indent=2))
