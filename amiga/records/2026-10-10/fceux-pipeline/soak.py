import asyncio,json,sys,time,importlib.util,subprocess,re
from pathlib import Path
from datetime import timedelta
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
name,binary,romkey,frames,*options=sys.argv[1:]
assert re.fullmatch('[a-z0-9-]+',name) and re.fullmatch('[A-Za-z0-9-]+',binary)
rom={'mario':'011 Mario Bros.nes','smw':'002 Super Mario World.nes'}[romkey]
local={'mario':'.context/attachments/yuC3Ij/011 Mario Bros.nes','smw':'.context/attachments/h2NhME/002 Super Mario World.nes'}[romkey]
out=Path('.context/amiga/fceux-pipeline');events=[]
async def main():
 async with streamablehttp_client('http://127.0.0.1:55010/mcp') as (r,w,_):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def call(n,a={}):
    res=await s.call_tool(n,a,read_timeout_seconds=timedelta(seconds=40));t='\n'.join(getattr(c,'text','') for c in res.content)
    events.append({'tool':n,'args':a,'result':t});(out/(name+'-events.json')).write_text(json.dumps(events,indent=2));assert not res.isError and 'ERROR:' not in t,t;return t
   screens=await call('amiga_list_screens');ports=await call('amiga_list_ports')
   assert 'Screens (1)' in screens and 'Workbench' in screens and 'Sixies.ARM.Debug.Owner' not in ports,(screens,ports)
   nonce=f'{time.time_ns()&0xffffffff:08x}'
   extra=' VERIFY' if options==['VERIFY'] else '';assert not options or extra
   command=f'Stack 65536\nRun >NIL: SD032G:Dev/ZZFceuxPlayer/{binary} {nonce} RUN "SD032G:Dev/ZZNesPlayer/ROMs/{rom}" {int(frames)}{extra} >SD032G:Dev/ZZFceuxPlayer/opt-{name}.log\n'
   print(await call('amiga_run_script',{'script':command,'timeout':15}),flush=True)
   await asyncio.sleep(4)
   screen=await call('amiga_list_screens');assert 'ZZFceux fullscreen' in screen
   await call('amiga_input_key',{'rawkey':'44','direction':'down'})
   await asyncio.sleep(.15)
   await call('amiga_input_key',{'rawkey':'44','direction':'up'})
   began=time.monotonic()
   for i in range(160):
    ports=await call('amiga_list_ports')
    if 'Public Message Ports' in ports and 'Sixies.ARM.Debug.Owner' not in ports:break
    if i%6==0:print(f'Start-triggered soak running: {time.monotonic()-began:.0f}s',flush=True)
    await asyncio.sleep(5)
   else:raise RuntimeError('Core1 still active; stop testing')
   screens=await call('amiga_list_screens');assert 'Screens (1)' in screens and 'Workbench' in screens,screens
   await call('amiga_ping')
asyncio.run(main())
s=importlib.util.spec_from_file_location('fetch','amiga/records/2026-10-07/inventory/fetch.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
p=out/(name+'.log');m.fetch(f'SD032G:Dev/ZZFceuxPlayer/opt-{name}.log',p)
s=p.read_text()
def values(pattern):
 m=re.search(pattern,s);assert m,pattern;return [int(x) for x in m.groups()]
f,elapsed=values(r'ZZFCEUX END exit=0 frames=(\d+) elapsed_us=(\d+)');assert f==int(frames)
queued,flips=values(r'FULLSCREEN_END queued=(\d+) flips=(\d+) pending=-1 ack_wait_us=\d+ fault=0');assert queued==flips==f
q,sub,done,high=values(r'AUDIO_TASK queued=(\d+) submitted=(\d+) completed=(\d+) highwater=(\d+) error=0 stopped=1');assert q==sub==done and q>0
assert 'MAPPING PASS (eight nonce-derived words)' in s and 'EXIT epilogue=52455431' in s and 'LAUNCHER exit=0; owned memory released' in s
assert re.search(r'MMU_RESTORE phase=3 register_mismatches=00000000 .* witness_bad=0 ',s)
regs=re.findall(r'REGISTER n=(\d+) original=([0-9a-f]+) restored=([0-9a-f]+)',s);assert len(regs)==14 and all(a==b for _,a,b in regs)
r={'frames':f,'elapsed_us':elapsed,'displayed_fps':f*1e6/elapsed,'samples_completed':done,'audio_highwater':high,'clean_return':True,'workload':'Start injected once after 4s; gameplay progression not supervised. Native no-input hash comparison is inapplicable. Not continuous active gameplay proof.'}
(out/(name+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
for line in p.read_text().splitlines():
 if 'PROFILE' in line:print(line)
