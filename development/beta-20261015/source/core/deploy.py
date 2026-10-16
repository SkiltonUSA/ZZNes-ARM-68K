import asyncio,json,re,hashlib,importlib.util,time,sys
from pathlib import Path
from datetime import timedelta
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
out=Path('.context/amiga/fceux-compat');remote='SD032G:Dev/ZZNes-Compat'
spec=importlib.util.spec_from_file_location('fetch','amiga/records/2026-10-07/inventory/fetch.py');fetch=importlib.util.module_from_spec(spec);spec.loader.exec_module(fetch)
manifest=json.loads(Path('.context/amiga/nes-rom-import/manifest.json').read_text());events=[]
async def main():
 async with streamablehttp_client('http://127.0.0.1:55010/mcp') as (r,w,_):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def call(n,a={}):
    res=await s.call_tool(n,a,read_timeout_seconds=timedelta(seconds=55));t='\n'.join(getattr(x,'text','') for x in res.content);events.append({'tool':n,'args':a,'text':t});(out/'deploy-events.json').write_text(json.dumps(events,indent=2));assert not res.isError,t;return t
   async def run(script):return await call('amiga_run_script',{'script':script,'timeout':30})
   ports=await call('amiga_list_ports');assert 'Sixies.ARM.Debug.Owner' not in ports and 'ZZNES_LIBRARY_PREVIEW' not in ports
   target='SD032G:Dev/ZZNes-Borders';previous={'ZZFceux-ui':'411dccc6a8d19123fc5a0f2f564b51f0','ZZNesLibrary':'9bfb74face7bca4a2fd767c99500a773'}
   for name,old in previous.items():
    t=await run(f'Copy {remote}/{name} {target}/{name}.new\nC:MD5Sum {target}/{name}.new\nIf NOT EXISTS {target}/{name}.pre-compat-pal-20261011\nCopy {target}/{name} {target}/{name}.pre-compat-pal-20261011\nEndIf\nC:MD5Sum {target}/{name}.pre-compat-pal-20261011\n');assert hashlib.md5((out/name).read_bytes()).hexdigest() in t.lower() and old in t.lower(),t
   for name in previous:
    t=await run(f'Copy {target}/{name}.new {target}/{name}\nC:MD5Sum {target}/{name}\nProtect {target}/{name} +e\n');assert hashlib.md5((out/name).read_bytes()).hexdigest() in t.lower(),t
   t=await run(f'C:MD5Sum {target}/Library.cfg\n');assert 'a5c3416fba25151196dd2ccdb3761013' in t.lower(),t
   print('PASS installed matching player/library, backups verified, Library.cfg unchanged',flush=True)
   print(await run(f'Stack 65536\nRun >NIL: {target}/ZZNesLibrary >{remote}/Library-start.log\n'),flush=True)
   for _ in range(15):
    await asyncio.sleep(1);ports=await call('amiga_list_ports')
    if 'ZZNES_LIBRARY_PREVIEW' in ports:break
   else:raise RuntimeError('Library did not open')
   print(await call('amiga_list_screen_windows'),flush=True)
asyncio.run(main())
