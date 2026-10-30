"""Versioned, frame-boundary HQ audio states for the generated NES core.

Quality-0 states resume in their original synthesis mode; new games use HQ.
No counter conversion or file migration is needed.
"""

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def edit(path, before, after):
    text = path.read_text()
    assert text.count(before) == 1, (path, before)
    path.write_text(text.replace(before, after))


def prepare(core, stage, library):
    # FlushEmulateSound retains exactly NCOEFFS+1 samples at the beginning of
    # WaveHi and clears its tail. Save only that live history, not 160 KiB.
    coeffs = (core / 'fcoeffs.h').read_text()
    assert '#define NCOEFFS 484' in coeffs
    edit(core / 'sound.cpp', 'SFORMAT FC_SOUND_EXTRA[]={', '''
static const unsigned FC_HQ_HISTORY = 485;
void FC_HQ_ClearTail() {
 memset(WaveHi + FC_HQ_HISTORY, 0, sizeof(WaveHi) - FC_HQ_HISTORY * sizeof(*WaveHi));
}
SFORMAT FC_SOUND_HQ[]={
 {WaveHi, FC_HQ_HISTORY * sizeof(*WaveHi), "HQWH"},
 {0}};
SFORMAT FC_SOUND_EXTRA[]={''')
    edit(core / 'filter.cpp', 'SFORMAT FC_FILTER_EXTRA[]={', '''
SFORMAT FC_FILTER_HQ[]={
 {&mrindex, sizeof(mrindex), "HQPH"},
 {0}};
SFORMAT FC_FILTER_EXTRA[]={''')
    state = core / 'state_core.h'
    edit(state, 'static SFORMAT *state_groups[]={', '''extern SFORMAT FC_SOUND_HQ[], FC_FILTER_HQ[];
void FC_HQ_ClearTail();
static SFORMAT *state_groups[]={''')
    edit(state, 'FC_FILTER_EXTRA,state_extra};',
         'FC_FILTER_EXTRA,state_extra,FC_SOUND_HQ,FC_FILTER_HQ};')
    # Keep v1 byte-for-byte for LQ; append the live HQ data only in v2.
    text = state.read_text()
    offset = text.index('static unsigned state_payload(')
    state.write_text(text[:offset] + (ROOT / 'development/output-quality-20261030/hq_state_io.h').read_text())
    edit(state, 'pinned old-PPU/LQ core.', 'pinned old-PPU/LQ and HQ core.')
    checks = library / 'library_saves.h'
    edit(checks, 'le32(p+4)==1&&',
         '((le32(p+4)==1&&le32(p+24)==0x20261011u)||(le32(p+4)==2&&le32(p+24)==0x20261030u))&&')
    edit(checks, '&&le32(p+24)==0x20261011u&&le32(p+28)<=1', '&&le32(p+28)<=1')
    edit(stage / 'state_host.h', 'rejected (ROM/version/checksum)',
         'rejected (ROM/audio version/checksum)')
    edit(stage / 'host.c', '32kHz quality1;', '32kHz HQ default; saves retain synthesis;')
    edit(stage / 'state_host.h', 'ok=ad_get(shared+MB_REPLY,52);printf(',
         'ok=ad_get(shared+MB_REPLY,52);if(ok)printf("STATE synthesis=%s\\n",p[4]==2?"HQ":"legacy");printf(')
