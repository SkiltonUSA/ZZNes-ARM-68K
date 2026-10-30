"""Keep the host-facing PCM window out of the ARM private write-back cache.

Applies only to an isolated generated NES build. The allocation, source PCM,
host synchronization and ownership/teardown protocol remain unchanged.
"""
def prepare(core):
    wire = (core / 'wire.h').read_text()
    assert '#define NES_AUDIO 0xd0000u' in wire
    plan = core / 'mmu_plan.h'
    text = plan.read_text()
    marker = '#define MB_PUBLIC_END 0x84000u'
    assert text.count(marker) == 1
    text = text.replace(marker, marker + '''
/* 1024 mono signed-16 samples, published to the 68k once per frame.
 * Include every intersecting page: the Exec allocation need not be page-aligned.
 * This is shared IPC storage; core synthesis buffers remain cached/private. */
#define MB_AUDIO_BEGIN 0xd0000u
#define MB_AUDIO_END (MB_AUDIO_BEGIN + 2048u)''')
    marker = 'mb_overlap(page,base+MB_PUBLIC_BEGIN,base+MB_PUBLIC_END))'
    assert text.count(marker) == 1
    text = text.replace(marker, '''mb_overlap(page,base+MB_PUBLIC_BEGIN,base+MB_PUBLIC_END) ||
       mb_overlap(page,base+MB_AUDIO_BEGIN,base+MB_AUDIO_END))''')
    plan.write_text(text)
