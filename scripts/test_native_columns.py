"""Column geometry and persistent settings, using the generated release sources."""
from pathlib import Path
import subprocess
r=Path(__file__).resolve().parents[1];d=r/'development/native-columns-20261030';b=r/'.context/ax-release-build';o=r/'.context/native-columns-tests';o.mkdir(parents=True,exist_ok=True)
for name,compiler,includes in [('columns','clang++',['player']),('settings','clang',['library','player'])]:
 subprocess.run([compiler,'-DPLAYER_SESSION="'+str(b/'player/session.h')+'"','-O2','-g','-fsanitize=address,undefined',*['-I'+str(b/p)for p in includes],str(d/('test_'+name+('.cpp'if name=='columns'else'.c'))),'-o',str(o/name)],check=True)
 subprocess.run([str(o/name)],cwd=o,check=True)
