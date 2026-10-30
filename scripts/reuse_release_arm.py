"""Preserve the recorded 0.8.7 ARM payload for a host-only rebuild.

Offsets come from the release Hunk's memcpy/relocation loop disassembly.
The whole-executable digest pins those offsets; arbitrary binaries are rejected.
This is not a substitute for compiling changed ARM sources.
"""
import hashlib
import struct

SHA256 = 'ef1fadfc88cf0f1c07bbb8f9ec2b317e6a2a47e030b95d643799fa9b4437243c'


def header(binary):
    if len(binary) != 581828 or hashlib.sha256(binary).hexdigest() != SHA256:
        raise ValueError('Expected the recorded ZZNES 0.8.7 release player')
    image = binary[256:256 + 261024]
    mapping = binary[0x3fca0:0x3fdd8]
    relocations = struct.unpack_from('>498I', binary, 0x3fdd8)
    if len(set(relocations)) != len(relocations):
        raise ValueError('Duplicate relocation')
    for offset in relocations:
        if offset % 4 or offset + 4 > len(image):
            raise ValueError('Relocation outside the preserved image')
        if struct.pack('<II', offset, 23) not in image:
            raise ValueError('Relocation missing from embedded ARM ELF table')
    def array(name, kind, values):
        return f'static const {kind} {name}[]={{' + ','.join(map(str, values)) + '};\n'
    return ('#define ZZ_ENTRY 0u\n' + array('zz_image', 'unsigned char', image)
            + array('zz_mapping_probe', 'unsigned char', mapping)
            + array('zz_relocations', 'unsigned long', relocations))
