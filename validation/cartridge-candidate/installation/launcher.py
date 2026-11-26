import asyncio,sys,re,shutil,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'next-floppy-acceptance'));from link import connect
D='SD032G:Dev/NESInstall0812/ZZNES';F='SD032G:Dev/NESCart12'
async def go(call,shell):
 ports=await call('amiga_list_ports');assert 'ZZNES_LIBRARY' not in ports and 'Sixies.ARM.Debug.Owner' not in ports
 cfg='ZZNESUI4\n0 0 0 0 0 0 1 0 1 0 1 0 0 1 0 0\n'+''.join('0 0 '+(F+'/'+n).encode().hex()+' - -\n' for n in ['board.unif','BOARD.UNF','stored.zip','deflated.zip'])
 await call('amiga_write_file',{'path':D+'/Library.cfg','offset':0,'hex_data':cfg.encode().hex()})
 print(await shell(f'Stack 262144\nRun >NIL: {D}/ZZNES'),flush=True);await asyncio.sleep(7)
 assert 'ZZNES_LIBRARY' in await call('amiga_list_ports');print('PASS candidate MUI library opened with UNIF/ZIP entries',flush=True)
 shot=await call('amiga_screenshot');m=re.search(r'Screenshot saved: (.+?\.ppm)',shot);assert m,shot
 subprocess.run(['sips','-s','format','png',m[1],'--out',str(P/'launcher.png')],check=True,stdout=subprocess.DEVNULL)
 print(await shell('RX "ADDRESS ZZNES.1 QUIT"'),flush=True)
 for i in range(15):
  await asyncio.sleep(1)
  if 'ZZNES_LIBRARY' not in await call('amiga_list_ports'):break
 else:raise RuntimeError('Launcher did not close')
 output=await shell(f'Type {D}/Library.cfg');assert (F+'/board.unif').encode().hex() in output
 print('PASS MUI clean exit and library persistence',flush=True)
 print(await shell('Stack 65536\nSD032G:Dev/Clock-Test/ZZClock-Keep STATUS'),flush=True)
asyncio.run(connect(go))
