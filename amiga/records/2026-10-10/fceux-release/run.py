import asyncio,json,sys,time,importlib.util,subprocess,re
from pathlib import Path
from datetime import timedelta
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
name,binary,romkey,frames,*options=sys.argv[1:]
assert re.fullmatch('[a-z0-9-]+',name) and re.fullmatch('[A-Za-z0-9-]+',binary)
rom={'mario':'011 Mario Bros.nes','smw':'002 Super Mario World.nes','demo':'Controller-Test.nes'}[romkey]
local={'mario':'.context/attachments/yuC3Ij/011 Mario Bros.nes','smw':'.context/attachments/h2NhME/002 Super Mario World.nes','demo':'.context/amiga/fceux-release/transfer/Controller-Test.nes'}[romkey]
out=Path('.context/amiga/fceux-release');events=[];log_size=0
async def main():
 global log_size
 async with streamablehttp_client('http://127.0.0.1:55010/mcp') as (r,w,_):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def call(n,a={}):
    res=await s.call_tool(n,a,read_timeout_seconds=timedelta(seconds=40));t='\n'.join(getattr(c,'text','') for c in res.content)
    events.append({'tool':n,'args':a,'result':t});(out/(name+'-events.json')).write_text(json.dumps(events,indent=2));assert not res.isError and 'ERROR:' not in t,t;return t
   screens=await call('amiga_list_screens');ports=await call('amiga_list_ports')
   assert 'Screens (1)' in screens and 'Workbench' in screens and 'Sixies.ARM.Debug.Owner' not in ports,(screens,ports)
   nonce=f'{time.time_ns()&0xffffffff:08x}'
   extra=' '+options[0] if options in (['VERIFY'],['INPUT']) else '';assert not options or extra
   romdir='SD032G:Dev/ZZFceuxPlayer/Release-0.2.0-rc1/ROMs' if romkey=='demo' else 'SD032G:Dev/ZZNesPlayer/ROMs'
   command=f'Stack 65536\nRun >NIL: SD032G:Dev/ZZFceuxPlayer/{binary} {nonce} RUN "{romdir}/{rom}" {int(frames)}{extra} >SD032G:Dev/ZZFceuxPlayer/opt-{name}.log\n'
   print(await call('amiga_run_script',{'script':command,'timeout':15}),flush=True)
   await asyncio.sleep(3)
   for i in range(40):
    ports=await call('amiga_list_ports')
    if 'Public Message Ports' in ports and 'Sixies.ARM.Debug.Owner' not in ports:break
    await asyncio.sleep(2)
   else:raise RuntimeError('Core1 still active; stop testing')
   screens=await call('amiga_list_screens');assert 'Screens (1)' in screens and 'Workbench' in screens,screens
   await call('amiga_ping')
   log_size=int((await call('amiga_dos_command',{'command':f'List SD032G:Dev/ZZFceuxPlayer/opt-{name}.log LFORMAT "%L"','timeout':10})).strip())
asyncio.run(main())
s=importlib.util.spec_from_file_location('fetch','amiga/records/2026-10-07/inventory/fetch.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
p=out/(name+'.log');m.fetch(f'SD032G:Dev/ZZFceuxPlayer/opt-{name}.log',p,log_size)
r=subprocess.check_output([sys.executable,'scripts/analyze_fceux_player.py',str(p),local,*(['--input'] if options==['INPUT'] else []),*(['--no-audio-output'] if 'noaudio' in binary else [])],text=True);(out/(name+'.json')).write_text(r);print(r)
for line in p.read_text().splitlines():
 if 'PROFILE' in line:print(line)
