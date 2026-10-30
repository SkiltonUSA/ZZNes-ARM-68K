"""Build the pinned Nestopia core with a small native capture harness."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import subprocess

PIN = '27246144887c78154584515f530c61497e92cd05'
p = argparse.ArgumentParser()
p.add_argument('source', type=Path)
p.add_argument('output', type=Path)
p.add_argument('--trace', action='store_true', help='Instrument an isolated generated APU copy')
a = p.parse_args()
source, output = a.source.resolve(), a.output.resolve()
assert subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip() == PIN
assert not subprocess.check_output(['git', '-C', str(source), 'diff', 'HEAD'], text=True)
output.mkdir(parents=True, exist_ok=True)
harness = Path(__file__).with_name('capture.cpp')
text = (source / 'Makefile').read_text().split('CXXSRCS :=', 1)[1].split('JGSRCS :=', 1)[0]
sources = [source / name for name in re.findall(r'src/[\w/]+\.cpp', text)] + [harness]
if a.trace:
    apu = source / 'src/NstApu.cpp'
    content = apu.read_text()
    content = 'extern void reference_apu_write(unsigned long, unsigned, unsigned);\n' + content
    def instrument(match):
        suffix, address = match.group(1), match.group(2)
        expression = 'address' if suffix == 'AD' else '0x' + address
        return match.group(0) + '\n reference_apu_write(cpu.GetCycles()/cpu.GetClock(), ' + expression + ', data);'
    content, count = re.subn(r'NES_POKE_(AD|D)\(Apu,([0-9A-F]+)\)\s*\{', instrument, content)
    assert count == 15, count
    target = 'void Apu::WriteFrameCtrl(uint data)\n\t\t{'
    assert content.count(target) == 1
    content = content.replace(target, target + '\n reference_apu_write(cpu.GetCycles()/cpu.GetClock(), 0x4017, data);')
    generated = output / 'NstApu-trace.cpp'
    generated.write_text(content)
    sources[sources.index(apu)] = generated
flags = ['clang++', '-std=c++98', '-O2', '-DNDEBUG', '-DNST_NO_ZLIB', '-I' + str(source / 'src')]
def compile_one(src):
    name = src.relative_to(source) if src.is_relative_to(source) else src.name
    obj = output / (str(name).replace('/', '_') + '.o')
    key = hashlib.sha256(src.read_bytes() + ' '.join(flags).encode()).hexdigest()
    stamp = obj.with_suffix('.sha256')
    if not obj.exists() or not stamp.exists() or stamp.read_text() != key:
        subprocess.run(flags + ['-c', str(src), '-o', str(obj)], check=True)
        stamp.write_text(key)
    return obj
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    objects = list(pool.map(compile_one, sources))
subprocess.run(['clang++', *map(str, objects), '-o', str(output / 'capture')], check=True)
(output / 'build.json').write_text(json.dumps({
    'source': 'https://gitlab.com/jgemu/nestopia', 'commit': PIN,
    'compiler': subprocess.check_output(['clang++', '--version'], text=True),
    'flags': flags[:-1], 'source_files': len(sources), 'apu_trace': a.trace,
    'harness_sha256': hashlib.sha256(harness.read_bytes()).hexdigest(),
    'executable_sha256': hashlib.sha256((output / 'capture').read_bytes()).hexdigest()
}, indent=2) + '\n')
print('PASS pinned Nestopia reference build:', output / 'capture')
