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
    res=await s.call_tool(n,a,read_timeout_seconds=timedelta(seconds=55));t='\n'.join(getattr(x,'text','') for x in res.content);events.append({'tool':n,'args':a,'text':t});(out/'hardware-events.json').write_text(json.dumps(events,indent=2));assert not res.isError,t;return t
   async def run(script):return await call('amiga_run_script',{'script':script,'timeout':40})
   ports=await call('amiga_list_ports');assert 'Sixies.ARM.Debug.Owner' not in ports
   await run(f'If NOT EXISTS {remote}\nMakeDir {remote}\nEndIf\n')
   for name in ['ZZFceux-ui','ZZNesLibrary']:
    data=(out/name).read_bytes();t=await run(f'C:wget -q -T 20 -O {remote}/{name} http://10.0.0.21:55032/{name}\nC:MD5Sum {remote}/{name}\nProtect {remote}/{name} +e\n');assert hashlib.md5(data).hexdigest() in t.lower(),t
   print('Staged matching player/library, MD5 verified',flush=True)
   results=[]
   for index in range(1,9):
    item=manifest[index-1];path=f'{remote}/rom{index}-600.log';frames=600
    assert 'Sixies.ARM.Debug.Owner' not in await call('amiga_list_ports')
    print('START',item['filename'],flush=True)
    print(await run(f'Stack 65536\nRun >NIL: {remote}/ZZFceux-ui {int(time.time())&0xffffffff:08x} RUN "{item["destination"]}" {frames} INPUT >{path}\n'),flush=True)
    for _ in range(45):
     if 'Sixies.ARM.Debug.Owner' in await call('amiga_list_ports'):break
     await asyncio.sleep(1)
    else:raise RuntimeError('No owner acquisition')
    for _ in range(120):
     await asyncio.sleep(1)
     if 'Sixies.ARM.Debug.Owner' not in await call('amiga_list_ports'):break
    else:raise RuntimeError('Bounded test did not exit; do not free or reset while active')
    log=fetch.fetch(path,out/f'rom{index}-600.log').decode('latin1')
    def match(p):
     m=re.search(p,log);assert m,(p,log[-2500:]);return m
    end=match(r'ZZFCEUX END exit=0 frames=(\d+) elapsed_us=(\d+)');assert int(end[1])==frames
    a=match(r'AUDIO_TASK queued=(\d+) submitted=(\d+) completed=(\d+) highwater=(\d+) error=0 stopped=1');assert a[1]==a[2]==a[3]
    f=match(r'FULLSCREEN_END queued=(\d+) flips=(\d+) pending=-1 ack_wait_us=(\d+) fault=0');assert int(f[1])==int(f[2])==frames
    assert 'register_mismatches=00000000' in log and 'witness_bad=0' in log and 'LAUNCHER exit=0; owned memory released' in log and 'EXIT epilogue=52455431' in log
    region='PAL' if index in [2,3,8] else 'NTSC';assert f'REGION {region} period_us='+('19998' if region=='PAL' else '16639') in log
    assert abs(int(a[1])-(384000 if region=='PAL' else 319500))<200
    result={'rom':item['filename'],'region':region,'frames':frames,'elapsed_us':int(end[2]),'test_fps':frames*1e6/int(end[2]),'audio_samples':int(a[1]),'verified_frames':int(match(r'DIRECT_END challenges=\d+ verified_frames=(\d+)')[1]),'clean_exit':True,'log':path};results.append(result)
    (out/'hardware-results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(result),flush=True)
   print(await call('amiga_list_ports'),flush=True)
asyncio.run(main())
