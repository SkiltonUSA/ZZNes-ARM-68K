# NES and future SNES development roadmap

## Current priority: NES performance and timing

The 0.2.0-rc1 pass completed timing histograms, a rejected flip-only scheduling
experiment, joystick input, Workbench ROM selection, four original compatibility
fixtures and release packaging. Keep the owner-accepted fast build available.
The candidate measured 55.47 FPS on a reproducible 1,800-frame Mario Start
sequence and 54.26 FPS for 300 SMW startup frames; no new speed gain or 60 FPS
claim. See [release findings](../amiga/records/2026-10-10/fceux-release/).

Next performance work should isolate AHI driver scheduling and the occasional
long host stalls. Audio-disabled diagnostics reached 57.27 FPS, so audio is
one contributor, not the only limiter. Preserve every frame/sample and all
ownership/cache/teardown checks; measure latency and audible continuity.

ZZ9000AX per-application AHI mode allocation passed for cafe0000/cafe0001
without preference changes. Actual PCM streaming and physical audio acceptance
remain to implement/test. Direct Core1-to-AX needs an explicit supported
ownership/streaming interface; decoder PCM rings do not supply that contract.
Joystick code and OS polling passed; physical controller mapping acceptance
is pending. Broader mapper support remains a separate compatibility project.

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
