# Native columns — 0.8.7-dev

NES supplies 256×240 pixels. Sharp scaling to a 320-pixel-wide picture repeats
64 columns twice while the other 192 appear once. Scrolling detailed artwork
across that fixed pattern can make vertical bands conspicuous. Widescreen
compensation previously reduced the source to 240 columns instead. These are
horizontal presentation effects, distinct from the SNES vertical row reduction.

**Display → Scaling → Native columns** keeps each source column exactly once,
centred in the 320×240 output: 32 border pixels on each side, with all 240 rows
unchanged. At 2×/3×, every pixel repeats equally. An explicit 8/16-pixel edge
mask still hides that many source pixels per edge; it does not squeeze the rest.
Native width overrides monitor-width compensation. The resulting picture is
narrower than aspect-corrected 4:3; Sharp and Smooth remain available.

The existing settings field now accepts a third value, 2. Session view bits
8–9 encode Sharp=0, Smooth=1, Native=2; value 3 is rejected before allocation
and by the ARM presenter. No emulation, mapper, timing, scanline or audio code
changed. Use a matching launcher/player; older players reject the new value.

The physical test ROM was the supplied Super Mario World NES cartridge.
Its ROM bytes were unchanged.

## Checks

- Reproduced 192 single-width and 64 double-width columns before adding the mode.
  The new native-mode test initially failed because the old renderer rejected it.
- Sanitizer tests cover all 256 scrolling phases, both monitor selections, edge
  masks, byte orders, settings/session round trips and 1×/2×/3× pixel repetition.
- Relocated Cortex-A9 tests compare every pixel against the scalar reference at
  two runtime addresses, including legacy Sharp/Smooth, native masks/themes,
  NEON/fallback and SIMD/MMU restoration.
- Legacy library, border and compact-layout checks pass.
- Physical fullscreen and 3× window VERIFY runs complete 180 frames each,
  including four exact pixel readbacks per run and clean teardown. Verification
  stalls audio, so these runs are not audio performance measurements.
- Normal fullscreen and 3× runs complete 600 frames each with all 319,449 PCM
  samples delivered and no starvation transitions. The first capture deliberately
  pauses/drains as in 0.8.6; the second run reuses the saved thumbnail.

This removes the uneven column mapping. Visual confirmation in the reported
games remains pending; it does not establish tear-free monitor scanout or rule
out a separate core rendering issue.

[Build hashes](native-columns-build.json) ·
[Evidence](../amiga/records/2026-10-30/native-columns/)

Installed as 0.8.7-dev on the test Amiga with Native columns selected. Original
executables and library settings have rollback copies. All other library fields
and global AHI/screenmode preferences were preserved. The published 0.8.6 Beta
remains unchanged.
