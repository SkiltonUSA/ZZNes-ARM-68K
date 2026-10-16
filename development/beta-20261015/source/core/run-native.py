import subprocess,json
from pathlib import Path
out=Path('.context/amiga/fceux-compat');manifest=json.loads(Path('.context/amiga/nes-rom-import/manifest.json').read_text());results=[]
for row in manifest:
 pal=int('(Europe)' in row['filename'] or '(Australia)' in row['filename']);reference=None
 for mode in ['native','fixed','sanitize']:
  r=subprocess.run([out/mode,Path('.context/amiga/nes-rom-import/transfer')/row['transfer'],str(pal)],capture_output=True,text=True)
  result={'rom':row['filename'],'pal':pal,'mode':mode,'returncode':r.returncode,'output':r.stdout+r.stderr};results.append(result);print(row['filename'],mode,r.returncode,r.stdout[-170:],r.stderr[:1200],flush=True)
  if mode=='native':reference=r.stdout
  elif r.returncode==0:assert r.stdout==reference,(mode,r.stdout,reference)
 (out/'native-results.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(r['returncode']==0 for r in results)
