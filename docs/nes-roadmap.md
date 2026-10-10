# NES and future SNES development roadmap

## Current priority: NES performance and timing

Keep the accepted FCEUX build available. Measure longer play, investigate a
combined ARM emulation/presentation command, and preserve every-frame display,
PCM sample order, bounded requests and clean Workbench return. Verify audio
latency and synchronisation separately from AHI completion. Target sustained
60 FPS; the accepted build measured 53.71/51.92 FPS in startup tests.

After performance/stability: joystick support and an application-local
ZZ9000AX audio backend, without changing global AHI preferences.

## Future project: SNES on the ZZ9000 ARM

Added at the owner's request on 10 October 2026. This is planned work, not
support included in the current emulator. ZZNes/ZZFceux currently runs NES only.

1. Review a standalone SNES core. Mesen 2 supports SNES, but its SNES core is
   separate from the NES-only extraction used here. Consider integration cost
   and performance before selecting a core; do not promise full speed.
2. Build a minimal Cortex-A9 benchmark with CPU, video and sound emulation,
   using an original/homebrew fixture or an owner-supplied ROM. Compare hashes
   and timing against native execution before physical Core1 testing.
3. Decide feasibility using measured complete-frame costs. Start with ordinary
   cartridges; enhancement-chip support needs separate testing.
4. If practical, reuse the proven XACP launcher, bounded framebuffer ownership,
   Amiga input frontend and audio queue. Preserve firmware/MMU/cache/teardown
   checks. This would be a separate SNES integration and executable.

[Mesen 2 upstream](https://github.com/SourMesen/Mesen2) lists SNES support; its
archived repository points to [Mesen CE](https://github.com/nesdev-org/MesenCE)
for ongoing development. No SNES ARM performance measurements have been made.
