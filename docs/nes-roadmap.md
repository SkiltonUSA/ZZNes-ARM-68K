# ZZNES remaining work

Current features and installation are in [the README](../README.md). Historical
0.2.x measurements are retained in their original records; they do not describe
the current player. ZZSNES is now a separate released application, not a future
NES feature.

1. **Audio continuity:** measure sustained delivery and worst-case frame cost on
   current players. Keep synthesis corruption, transport coherency and device
   starvation separate. Per-app AHI/Paula and explicit AX options already exist;
   broader AX/driver and long-session acceptance remain necessary.
2. **Compatibility:** expand tested mapper/board, trainer and NES 2.0 coverage
   against the enabled loader/core paths. Compiling upstream board code does not
   establish cartridge compatibility.
3. **State and persistence:** preserve legacy save compatibility while extending
   coverage to additional mappers, battery-backed cartridges and interrupted saves.
4. **Presentation/input:** retain regional cadence and whole-image scaling;
   broaden scrolling, USB/CD32/Sega mapping and window/fullscreen regression tests.
5. **Release provenance:** keep launcher/player hashes, build inputs, README and
   signed installers aligned. [Published-source audit](release-source-audit.md).

The 22.05 kHz Paula choice and optional clock controls are integrated. The ARM
clock remains optional; no Core0 audio dependency is introduced for NES.
See [audio synthesis](audio-synthesis.md), [legacy states](audio-states.md) and
[AX tests](ax-audio.md) for completed work and remaining limits.

[Current released-player audio checks](audio-release-check.md).
