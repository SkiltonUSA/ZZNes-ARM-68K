#!/usr/bin/env python3
"""Pin the complete FCEUX source and inventory its mapper registrations.

Imports git objects, never a checkout's uncommitted changes. This prepares
source for the staged port; it does not enable unported features or deploy.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
COMMIT = '4d01530b6689b06a6d7cf0679b63625e3270ae9a'
DEST = ROOT / 'development/fceux-full/vendor'


def inventory(files):
    text = files['src/ines.cpp'].decode('latin1')
    table = text.split('static BMAPPINGLocal bmap[] = {', 1)[1].split('\n};', 1)[0]
    rows = re.findall(r'^\s*\{\s*"([^"]*)",\s*(\d+),\s*(\w+)\}', table, re.M)
    sources = {}
    for name, data in files.items():
        if name.startswith('src/boards/') and name.endswith('.cpp'):
            for symbol in re.findall(r'\bvoid\s+(\w+)\s*\(\s*CartInfo\s*\*', data.decode('latin1')):
                sources.setdefault(symbol, []).append(name)
    records = []
    for name, number, symbol in rows:
        if symbol == 'NULL':
            continue
        if symbol not in sources:
            raise ValueError('No source for ' + symbol)
        records.append(dict(mapper=int(number), name=name, init=symbol,
                            sources=sources[symbol]))
    ids = [r['mapper'] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate mapper registrations')
    return records


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--upstream', type=Path, help='Local pinned FCEUX git repository')
    p.add_argument('--verify', action='store_true')
    a = p.parse_args()
    manifest = DEST.parent / 'upstream.json'
    if a.verify:
        record = json.loads(manifest.read_text())
        files = {name: (DEST / name).read_bytes() for name in record['files']}
        actual = {n: hashlib.sha256(b).hexdigest() for n, b in files.items()}
        if record['commit'] != COMMIT or actual != record['files']:
            raise SystemExit('FCEUX source verification failed')
        if inventory(files) != record['mappers']:
            raise SystemExit('FCEUX mapper inventory mismatch')
        print('PASS: pinned FCEUX source and', len(record['mappers']), 'mapper registrations')
        return
    if a.upstream is None:
        p.error('--upstream is required for import')
    archive = subprocess.check_output(['git', '-C', str(a.upstream), 'archive', COMMIT,
                                       'src', 'COPYING', 'Authors', 'README', 'changelog.txt'])
    files = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        for item in tar:
            if not item.isfile():
                continue
            path = Path(item.name)
            if path.is_absolute() or '..' in path.parts:
                raise ValueError('Invalid upstream path')
            # Desktop runtime binaries are not Amiga dependencies or source.
            if path.suffix.lower() in {'.dll', '.lib', '.exe', '.o', '.a'}:
                continue
            files[item.name] = tar.extractfile(item).read()
    records = inventory(files)
    for name, data in files.items():
        dest = DEST / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    record = dict(repo='https://github.com/Rezzy-dev/fceux', commit=COMMIT,
                  scope='Complete upstream source, including desktop drivers; excludes compiled desktop binaries',
                  files={n: hashlib.sha256(b).hexdigest() for n, b in sorted(files.items())},
                  mappers=records)
    manifest.write_text(json.dumps(record, indent=2) + '\n')
    print('Imported', len(files), 'files;', len(records), 'mapper registrations')


if __name__ == '__main__':
    main()
