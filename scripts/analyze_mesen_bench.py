#!/usr/bin/env python3
"""Validate recorded CPU-only runs and reproduce the timing comparison."""
import argparse
import json
from pathlib import Path
import re
import statistics

ROOT=Path(__file__).resolve().parents[1]

def analyze(path,icache,running_sctlr=None):
    log=path.read_text()
    assert 'MAPPING PASS (eight nonce-derived words)' in log
    assert 'MIDR=413fc090 MPIDR=80000001' in log
    assert 'VERIFY checked=8991 mismatch=0 cycles=26553 hash=f86dd990 errors=0 unsupported=0' in log
    assert 'MESEN_CPU PASS;' in log and 'EXIT epilogue=52455431' in log
    assert 'LAUNCHER exit=0; owned memory released' in log
    if running_sctlr:
        assert f'CACHE original=08c50878 running={running_sctlr} restored=08c50878' in log
        assert 'MMU_RESTORE phase=3 register_mismatches=00000000' in log
        assert 'witness_bad=0' in log
        registers=re.findall(r'REGISTER n=(\d+) original=([0-9a-f]+) restored=([0-9a-f]+)',log)
        assert len(registers)==14 and [int(r[0]) for r in registers]==list(range(14))
        assert all(before==after for n,before,after in registers if n!='6')
        control=re.search(r'cpsr_control=([0-9a-f]+) expected=([0-9a-f]+)',log)
        assert control and control[1]==control[2]
    elif icache:
        assert 'CACHE original=08c50878 running=08c51878 restored=08c50878' in log
    else:
        assert 'ARM ready=41524d31 SCTLR=08c50878' in log
    rate=int(re.search(r'TIMER estimated_hz=(\d+)',log)[1])
    assert 320000000<rate<345000000
    rows=[dict(re.findall(r'(\w+)=([\da-f]+)',line)) for line in log.splitlines() if line.startswith('SAMPLE ')]
    assert len(rows)==11 and [int(r['n']) for r in rows]==list(range(11))
    assert rows[0]['warmup']=='1' and all(r['warmup']=='0' for r in rows[1:])
    for row in rows:
        assert row['cycles']=='26553' and row['instructions']=='8991' and row['hash']=='f86dd990'
        assert int(row['cpu_us'])==int(row['ticks'])*1000000//rate
    times=[int(r['cpu_us']) for r in rows[1:]]
    median=statistics.median(times)
    return {'median_cpu_us':median,'min_cpu_us':min(times),'max_cpu_us':max(times),
        'measured_samples':len(times),'instructions_per_sample':8991,'nes_cycles_per_sample':26553,
        'nes_time_represented_us':26553/1789773*1000000,
        'nes_cpu_cycles_per_host_second':26553*1000000/median,
        'fraction_of_ntsc_cpu_realtime':(26553/1789773*1000000)/median,
        'timer_estimated_hz':rate}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path,nargs='?',default=ROOT/'amiga/records/2026-10-09/mesen-cpu')
    a=p.parse_args()
    off=analyze(a.directory/'uncached.log',False);on=analyze(a.directory/'icache.log',True)
    print(json.dumps({'scope':'CPU-only synthetic diagnostic; no game FPS measured',
        'uncached':off,'instruction_cache':on,'speedup':off['median_cpu_us']/on['median_cpu_us'],
        'cpu_time_reduction_percent':100*(1-on['median_cpu_us']/off['median_cpu_us'])},indent=2))
