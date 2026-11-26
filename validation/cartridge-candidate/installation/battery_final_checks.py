import asyncio,sys,json,time,hashlib,re
from pathlib import Path
sys.path.insert(0,'.context/next-floppy-acceptance');from link import connect
sys.path.insert(0,'.context/amiga/c64/trainyard-review');from bridge import upload
P=Path('.context/nes-release-0812/package');D='SD032G:Dev/NESInstall0812';R=Path('.context/ZZNes-ARM-68K')
async def go(call,shell):
 assert 'Sixies.ARM.Debug.Owner' not in await call('amiga_list_ports')
 production=len(sys.argv)>1 and sys.argv[1]=='production'
 player='SD032G:Emulator/ZZNES/ZZFceux-ui'if production else D+'/ZZNES/ZZFceux-ui'
 assert hashlib.md5((R/'.context/release-0.8.12-final/ZZFceux-ui').read_bytes()).hexdigest()in await shell('C:MD5Sum '+player)
 cases=[]
 if not production:
  await upload(call,shell,[(R/'.context/battery-native/battery-5-1.nes',D+'/battery.nes')])
  cases=[('battery-first',D+'/battery.nes',1,0,1),('battery-second',D+'/battery.nes',1,0,2)]
 cases +=[(('installed-' if production else '')+'cv3','SD032G:Dev/ConsoleValidation/cv3.nes',1,1,None),(('installed-' if production else '')+'smw','SD032G:Dev/ConsoleValidation/smw.nes',0,1,None)]
 cases +=[(('installed-' if production else '')+f'mapper{m}-restore','SD032G:Dev/NESCart12/'+f'mapper{m}-ntsc.nes',1,1,None) for m in (7,11,66)]
 rows=[]
 for label,rom,window,resume,counter in cases:
  assert 'Sixies.ARM.Debug.Owner' not in await call('amiga_list_ports')
  state=rom.rsplit('.',1)[0]+'.state'
  m=re.search(r'mapper(\d+)-restore',label)
  if m:state='SD032G:Dev/NESCart12/live'+m[1]+'.state'
  session='ZZSESSION1\n0 0 0 '+str(resume)+'\n'+rom.encode().hex()+'\n'+state.encode().hex()+'\n'+(D+'/preview.shot').encode().hex()+f'\nDISPLAY {window} 0 0 1\n'
  await call('amiga_write_file',{'path':D+'/final.session','offset':0,'hex_data':session.encode().hex()})
  script=f'Stack 262144\nFailAt 21\n{player} --session {D}/final.session --frames 120 >{D}/final.log\nEcho DONE >{D}/final.done\n'
  await call('amiga_write_file',{'path':D+'/final.run','offset':0,'hex_data':script.encode().hex()})
  assert hashlib.md5(script.encode()).hexdigest()in await shell(f'C:MD5Sum {D}/final.run')
  print('START',label,flush=True);await shell(f'Delete {D}/final.done QUIET\nRun >NIL: Execute {D}/final.run')
  end=time.monotonic()+160
  while time.monotonic()<end:
   await asyncio.sleep(3)
   if 'Sixies.ARM.Debug.Owner'not in await call('amiga_list_ports')and 'FINISHED'in await shell(f'If EXISTS {D}/final.done\nEcho FINISHED\nEndIf'):break
  else:raise RuntimeError('Completion unknown; retain lease')
  log=P/(label+'.log');await call('amiga_pull_file',{'amiga_path':D+'/final.log','local_path':str(log.resolve())});t=log.read_text()
  req=['ZZFCEUX END exit=0','frames=120','register_mismatches=00000000','witness_bad=0','owned memory released','fault=0']
  req+=['STATE load OK','STATE synthesis=HQ']if resume else['BATTERY wrote 32768']
  assert all(x in t for x in req),[x for x in req if x not in t]
  if counter:
   f=P/(label+'.sav');await call('amiga_pull_file',{'amiga_path':rom+'.sav','local_path':str(f.resolve())});expected=(R/'.context/battery-native/arm'/('battery-5-1-'+('first'if counter==1 else'second')+'.sav')).read_bytes();assert f.read_bytes()==expected
  row={'case':label,'frames':120,'window':window,'resume':resume,'pass':True}
  for field in ('starvations','error'):
   m=re.search(r'\b'+field+r'=(\d+)',t)
   if m:row[field]=int(m[1])
  rows.append(row);(P/('production-checks.json'if production else'candidate-checks.json')).write_text(json.dumps(rows,indent=2)+'\n');print('PASS',row,flush=True)
 status=await shell('Stack 65536\nSD032G:Dev/AGA-Core0/ZZAGA-Status\nSD032G:Dev/Clock-Test/ZZClock-Keep STATUS');assert 'active=0'in status and 'core1_idle=1'in status and 'held=1'in status
 (P/('production-checks-status.txt'if production else'candidate-checks-status.txt')).write_text(status)
asyncio.run(connect(go))
