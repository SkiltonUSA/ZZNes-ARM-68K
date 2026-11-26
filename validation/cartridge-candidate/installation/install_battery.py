import asyncio,json,sys,time,hashlib,re
from pathlib import Path
sys.path.insert(0,'.context/next-floppy-acceptance');from link import connect
sys.path.insert(0,'.context/amiga/c64/trainyard-review');from bridge import upload
P=Path('.context/nes-release-0812/package');D='SD032G:Dev/NESInstall0812'
async def go(call,shell):
 async def idle():
  assert 'Sixies.ARM.Debug.Owner' not in await call('amiga_list_ports')
  q=await shell('Stack 65536\nSD032G:Dev/AGA-Core0/ZZAGA-Status\nSD032G:Dev/Clock-Test/ZZClock-Keep STATUS');assert 'active=0' in q and 'core1_idle=1' in q and 'held=1' in q;return q
 async def execute(text,label):
  script='Stack 262144\nFailAt 21\n'+text+'\nEcho DONE >'+D+'/install.done\n'
  await call('amiga_write_file',{'path':D+'/install.run','offset':0,'hex_data':script.encode().hex()})
  assert hashlib.md5(script.encode()).hexdigest() in await shell(f'C:MD5Sum {D}/install.run')
  await shell(f'Delete {D}/install.done QUIET\nRun >NIL: Execute {D}/install.run >{D}/install.log')
  end=time.monotonic()+300
  while time.monotonic()<end:
   await asyncio.sleep(4)
   if 'FINISHED' in await shell(f'If EXISTS {D}/install.done\nEcho FINISHED\nEndIf'):break
  else:raise RuntimeError('Installer completion unverified')
  local=P/(label+'.log');await call('amiga_pull_file',{'amiga_path':D+'/install.log','local_path':str(local.resolve())});q=local.read_text(encoding='latin1');print(label,q[-1400:],flush=True);return q
 await idle()
 if sys.argv[1]=='test':assert 'EXISTS-ALREADY' not in await shell(f'If EXISTS {D}/ZZNES\nEcho EXISTS-ALREADY\nEndIf'),'Fresh target already exists'
 await shell(f'If NOT EXISTS {D}\nMakeDir {D}\nEndIf')
 for app,repo,v in [('ZZNES','ZZNes-ARM-68K','0.8.12')]:
  r=Path('.context')/repo;b=r/'.context'/(f'release-{v}-rows' if app=='ZZSNES' else f'release-{v}-final');package=P/f'{app}-{v}-dev-amipkg.lha'
  await upload(call,shell,[(package,D+'/'+app+'.lha')])
  q=await execute(f'C:lha xq {D}/{app}.lha {D}/\nEcho "EXTRACT_RC=$RC"',app+'-extract');assert 'EXTRACT_RC=0' in q
  files={n:b/n for n in [app,'ZZClock',*(['ZZFceux-ui'] if app=='ZZNES' else ['ZZSnes-ui','ZZSnes-FX'])]}
  targets=[(D+'/'+app,'fresh'),(D+'/'+app,'repeat')] if sys.argv[1]=='test' else [('SD032G:Emulator/'+app,'production')]
  for target,label in targets:
   await idle()
   if label=='production':
    preserve='\n'.join(f'If EXISTS {target}/{n}\nC:MD5Sum {target}/{n}\nElse\nEcho MISSING-{n}\nEndIf' for n in ['Library.cfg','Audio.cfg','InputRoute.cfg','Controls.cfg']);before=await shell(preserve);assert re.search(r'\b[0-9a-fA-F]{32}\b',before),before;(P/(app+'-preserved-before.txt')).write_text(before)
    await shell('\n'.join(f'If NOT EXISTS {D}/{name}.old\nCopy {target}/{name} {D}/{name}.old\nEndIf' for name in files))
   elif label=='repeat':await shell(f'Echo "preserve-check" >{target}/Preserve.test')
   q=await execute(f'CD {D}/{app}-Install\nExecute Install DEST {target}\nEcho "INSTALL_RC=$RC"',app+'-'+label)
   assert all(x in q for x in ['INSTALL_RC=0','Installation complete','Catalogue signature verified','Dependencies passed']),q
   checks=[*files.items(),('ReadMe.txt',r/'README.md')]
   for name,local in checks:assert hashlib.md5(local.read_bytes()).hexdigest() in await shell(f'C:MD5Sum {target}/{name}'),name
   if label=='repeat':assert 'preserve-check' in await shell(f'Type {target}/Preserve.test')
   if label=='production':
    after=await shell(preserve);assert before==after;(P/(app+'-preserved-after.txt')).write_text(after)
   print('PASS',app,label,'binary hashes and README',flush=True)
 status=await idle();(P/('install-'+sys.argv[1]+'-status.txt')).write_text(status)
asyncio.run(connect(go))
