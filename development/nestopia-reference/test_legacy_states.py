"""Replay old quality-0 states in the new player, then switch back to HQ."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
from test_hq_states import machine, frame, save, load
from test_core_quality import square_rom

p=argparse.ArgumentParser()
p.add_argument('baseline',type=Path)
p.add_argument('candidate',type=Path)
p.add_argument('--rom',type=Path)
p.add_argument('--pal',action='store_true')
p.add_argument('--warmup',type=int,default=120)
p.add_argument('--frames',type=int,default=60)
p.add_argument('--output',type=Path)
p.add_argument('--state',type=Path)
a=p.parse_args()
rom=a.rom.read_bytes() if a.rom else square_rom()
old=machine(a.baseline,rom,0x11000040,a.pal)
new=machine(a.candidate,rom,0x150020c0,a.pal)
for i in range(a.warmup):frame(old,i);frame(new,i)
legacy=save(old);hq=save(new)
assert struct.unpack_from('<I',legacy,4)[0]==1
assert struct.unpack_from('<I',hq,4)[0]==2
hq_expected=[frame(new,i) for i in range(a.frames)]
old_expected=[frame(old,i) for i in range(a.frames)]
assert load(new,legacy)==1
assert save(new)==legacy, 'legacy checkpoint changed during load'
for i,expected in enumerate(old_expected):
 assert frame(new,i)==expected,('legacy replay',i)
legacy_again=save(new)
assert load(old,legacy_again)==1, 'new legacy save must remain readable by old core'
assert save(old)==legacy_again
assert load(new,hq)==1
for i,expected in enumerate(hq_expected):
 assert frame(new,i)==expected,('HQ replay after legacy switch',i)
fresh=machine(a.candidate,rom,0x19003080,a.pal)
assert load(fresh,legacy)==1
for i,expected in enumerate(old_expected):assert frame(fresh,i)==expected,('fresh legacy replay',i)
# A malformed legacy state must not switch the synthesis mode or mutate state.
unchanged=save(new)
bad=bytearray(legacy);bad[-1]^=1
assert load(new,bytes(bad))==0 and save(new)==unchanged
result=dict(test='ARM instruction model, not physical hardware',rom_sha256=hashlib.sha256(rom).hexdigest(),
 baseline_elf_sha256=hashlib.sha256((a.baseline/'player/fceux.elf').read_bytes()).hexdigest(),
 candidate_elf_sha256=hashlib.sha256((a.candidate/'player/fceux.elf').read_bytes()).hexdigest(),
 pal=a.pal,warmup=a.warmup,replay_frames=a.frames,legacy_bytes=len(legacy),hq_bytes=len(hq),
 legacy_exact_pcm_video_cycles=True,fresh_legacy=True,legacy_re_save_unchanged=True,
 hq_after_legacy=True,invalid_legacy_no_mutation=True)
if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
if a.state:a.state.write_bytes(legacy)
print('PASS legacy/HQ mode replay',json.dumps(result),flush=True)
