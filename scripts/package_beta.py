#!/usr/bin/env python3
"""Package the archived ZZNES Beta executables without personal game data."""
from pathlib import Path
import hashlib
import json
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / 'docs/beta-build.json').read_text())
SOURCE = ROOT / META['artifact_dir']
HASHES = json.loads((ROOT / 'docs/beta-sha256.json').read_text())
OUTPUT = ROOT / '.context/releases'
OUTPUT.mkdir(parents=True, exist_ok=True)
files = {}
for path in sorted(SOURCE.iterdir()):
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == HASHES[str(path.relative_to(ROOT))], path
    files['ZZNES/' + path.name] = data
for name in ('ZZNES', 'ZZFceux-ui'):
    assert files['ZZNES/' + name][:4] == b'\0\0\x03\xf3', name
files['ZZNES.info'] = (ROOT / 'amiga/fceux_player/distribution/ZZFceux-drawer.info').read_bytes()
files['ZZNES/COPYING.RUNTIME'] = (ROOT / 'amiga/fceux_player/distribution/COPYING.RUNTIME').read_bytes()
files['ZZNES/licenses/FCEUX-COPYING'] = (ROOT / 'amiga/fceux_bench/vendor/COPYING').read_bytes()
files['ZZNES/SHA256SUMS'] = ''.join(
    hashlib.sha256(data).hexdigest() + '  ' + name.removeprefix('ZZNES/') + '\n'
    for name, data in sorted(files.items()) if name.startswith('ZZNES/')
).encode()
for name in ('ROMs', 'States', 'Snapshots'):
    files['ZZNES/' + name + '/'] = b''

archive = OUTPUT / 'ZZNES-0.5.0-Beta.zip'
executables = {'ZZNES/ZZNES', 'ZZNES/ZZFceux-ui'}
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
    for name, data in sorted(files.items()):
        info = zipfile.ZipInfo(name, date_time=(2026, 10, 12, 0, 0, 0))
        info.create_system = 3
        info.compress_type = zipfile.ZIP_DEFLATED
        mode = (stat.S_IFDIR | 0o755) if name.endswith('/') else (
            stat.S_IFREG | (0o755 if name in executables else 0o644))
        info.external_attr = (mode << 16) | (0x10 if name.endswith('/') else 0)
        output.writestr(info, data)
with zipfile.ZipFile(archive) as packaged:
    assert packaged.testzip() is None
    assert set(packaged.namelist()) == set(files)
    for name, data in files.items():
        assert packaged.read(name) == data, name
    for name in executables:
        assert (packaged.getinfo(name).external_attr >> 16) & 0o111 == 0o111
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.zip.sha256').write_text(digest + '  ' + archive.name + '\n')
print(archive)
print('SHA256:', digest)
