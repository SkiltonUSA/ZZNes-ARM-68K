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
   MMC1/MMC5 battery variants. The released 0.8.11 player does not support
   NES 2.0 or UNIF. The isolated candidate now has bounded support and three
   additional mapper IDs; [scope and tests](cartridge-formats.md). Trainers
   are supported on the eight mapper IDs in the release. Compiling upstream board code does not
   establish cartridge compatibility.
   The requested expansion now explicitly includes NES 2.0 header/submapper/RAM
   handling, UNIF chunk and board-name loading, and additional mapper integration.
   Start with the pinned FCEUX latch boards (AxROM/7, Color Dreams/11 and
   GxROM/66), then expand after banking, mirroring, trainer, battery and
   save-state replay checks. Unknown boards and unsupported submapper variants
   must remain explicit refusals; converting a header alone is not support.
   ARM and bounded hardware bank/state tests now pass, including two legacy
   game-state regressions. Keep this work isolated until broader game/UI and
   release-installation acceptance is complete.
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
