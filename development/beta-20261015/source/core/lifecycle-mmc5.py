import asyncio,json,re,hashlib,importlib.util,time,sys
from pathlib import Path
from datetime import timedelta
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
out=Path('.context/amiga/fceux-compat');remote='SD032G:Dev/ZZNes-Compat'
spec=importlib.util.spec_from_file_location('fetch','amiga/records/2026-10-07/inventory/fetch.py');fetch=importlib.util.module_from_spec(spec);spec.loader.exec_module(fetch)
manifest=json.loads(Path('.context/amiga/nes-rom-import/manifest.json').read_text());events=[]

async def main(idx):
 async with streamablehttp_client('http://127.0.0.1:55010/mcp') as (r,w,_):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def call(n,a={}):
    res=await s.call_tool(n,a,read_timeout_seconds=timedelta(seconds=50));t='\n'.join(getattr(x,'text','') for x in res.content);events.append({'tool':n,'args':a,'text':t});(out/'lifecycle-events.json').write_text(json.dumps(events,indent=2));assert not res.isError;return t
   async def key(k):
    await call('amiga_input_key',{'rawkey':k,'direction':'down'});await asyncio.sleep(.2);await call('amiga_input_key',{'rawkey':k,'direction':'up'})
   assert 'Sixies.ARM.Debug.Owner' not in await call('amiga_list_ports')
   for name in [f'Session{idx}-0.cfg',f'Session{idx}-1.cfg']:
    t=await call('amiga_run_script',{'script':f'C:wget -q -T 20 -O {remote}/{name} http://10.0.0.21:55032/{name}\nC:MD5Sum {remote}/{name}\n','timeout':40});assert hashlib.md5((out/name).read_bytes()).hexdigest() in t.lower()
   await call('amiga_run_script',{'script':f'Stack 65536\nRun >NIL: {remote}/ZZFceux-ui --session {remote}/Session{idx}-0.cfg --frames 1800 >{remote}/Lifecycle{idx}.log\n','timeout':10})
   for _ in range(40):
    if 'ZZFceux fullscreen' in await call('amiga_list_screens'):break
    await asyncio.sleep(1)
   else:raise RuntimeError('No fullscreen')
   await asyncio.sleep(8)
   await key('19')
   try:
    await asyncio.sleep(.5)
    for _ in range(3):await key('54');await asyncio.sleep(1)
    await asyncio.sleep(3)
    for _ in range(3):await key('57');await asyncio.sleep(1)
    await asyncio.sleep(3)
    await key('58');await asyncio.sleep(2)
   finally:await key('19');await key('10')
   for _ in range(30):
    if 'Sixies.ARM.Debug.Owner' not in await call('amiga_list_ports'):break
    await asyncio.sleep(1)
   else:raise RuntimeError('Owner did not release')
   log=fetch.fetch(remote+f'/Lifecycle{idx}.log',out/f'lifecycle{idx}.log').decode('latin1')
   for expected in ['STATE save OK','STATE load OK','SNAPSHOT saved','witness_bad=0','register_mismatches=00000000','LAUNCHER exit=0; owned memory released']:assert expected in log,expected
   print('PASS paused save/load/F9/resume/quit and restoration',flush=True)
   await call('amiga_run_script',{'script':f'Stack 65536\nRun >NIL: {remote}/ZZFceux-ui --session {remote}/Session{idx}-1.cfg --frames 120 >{remote}/Resume{idx}.log\n','timeout':10})
   for _ in range(40):
    if 'Sixies.ARM.Debug.Owner' in await call('amiga_list_ports'):break
    await asyncio.sleep(1)
   else:raise RuntimeError('No owner')
   for _ in range(60):
    if 'Sixies.ARM.Debug.Owner' not in await call('amiga_list_ports'):break
    await asyncio.sleep(1)
   else:raise RuntimeError('Owner did not release')
   log=fetch.fetch(remote+f'/Resume{idx}.log',out/f'resume{idx}.log').decode('latin1');assert 'STATE load OK' in log and 'LAUNCHER exit=0; owned memory released' in log
   print('PASS fresh-process state resume and clean quit',flush=True)
   print(await call('amiga_ping'),flush=True)
for idx in [4]:asyncio.run(main(idx))
