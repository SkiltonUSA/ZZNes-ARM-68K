"""Check a physical checkpoint's first resumed frame against the ARM model."""
import argparse
import json
import re
from pathlib import Path
from test_hq_states import machine, load

p=argparse.ArgumentParser()
p.add_argument('build',type=Path)
p.add_argument('rom',type=Path)
p.add_argument('state',type=Path)
p.add_argument('log',type=Path)
p.add_argument('--output',type=Path)
a=p.parse_args()
state=a.state.read_bytes()
pal=int.from_bytes(state[28:32],'little')
assert pal in (0,1)
m=machine(a.build,a.rom.read_bytes(),0x17003080,pal)
assert load(m,state)==1
assert m.call('_Z9nes_framehPFivE',0,0)==0
row=re.search(r'FRAME n=1 cycles=(\d+) core_hash=([0-9a-f]+)',a.log.read_text())
assert row
actual=[int(row[1]),int(row[2],16)]
expected=[m.call('_Z10nes_cyclesv'),m.call('_Z8nes_hashv')]
assert actual==expected,(actual,expected)
result=dict(physical_checkpoint_loaded=True,first_resume_cycles=actual[0],first_resume_video_hash=f'{actual[1]:08x}',matches_relocated_model=True,scope='first resumed video/cycle endpoint; no physical PCM capture in this test')
if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
print('PASS physical checkpoint/model',json.dumps(result))
