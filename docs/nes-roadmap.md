# ZZNES remaining work

Current features and installation are in [the README](../README.md). Historical
0.2.x measurements are retained in their original records; they do not describe
the current player. ZZSNES is now a separate released application, not a future
NES feature.

The 0.8.11 release, signed installer and installed-player checks are complete.
[Release evidence](validation/battery-save/README.md). The items below are
remaining compatibility/acceptance work, not unfinished release packaging.

1. **Audio continuity:** measure sustained delivery and worst-case frame cost on
   current players. Keep synthesis corruption, transport coherency and device
   starvation separate. Per-app AHI/Paula and explicit AX options already exist;
   broader AX/driver and long-session acceptance remain necessary.
2. **Compatibility:** expand testing of enabled mappers/boards, including CRC-selected
   MMC1/MMC5 battery variants. NES 2.0, UNIF and additional battery boards remain
   unsupported. Trainers
   are supported on the eight enabled mapper IDs in 0.8.10 Beta. Compiling upstream board code does not
   establish cartridge compatibility.
3. **State and persistence:** preserve legacy save compatibility while extending
   coverage to additional enabled mappers and interrupted saves. Battery persistence is integrated
   for supported mapper 1/4/5 boards; interrupted-save recovery is tested.
4. **Presentation/input:** retain regional cadence and whole-image scaling;
   broaden scrolling, USB/CD32/Sega mapping and window/fullscreen regression tests.
5. **Release provenance:** keep launcher/player hashes, build inputs, README and
   signed installers aligned. [Published-source audit](release-source-audit.md).

The 22.05 kHz Paula choice and optional clock controls are integrated. The ARM
clock remains optional; no Core0 audio dependency is introduced for NES.
See [audio synthesis](audio-synthesis.md), [legacy states](audio-states.md) and
[AX tests](ax-audio.md) for completed work and remaining limits.

[Historical retained-player audio checks](audio-release-check.md).
