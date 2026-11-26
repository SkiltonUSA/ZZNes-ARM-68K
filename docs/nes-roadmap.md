# ZZNES remaining work

Current features and installation are in [the README](../README.md). Historical
0.2.x measurements are retained in their original records; they do not describe
the current player. ZZSNES is now a separate released application, not a future
NES feature.

The 0.8.12 release integrates the tested cartridge layer.
[Build and validation evidence](../validation/cartridge-candidate/README.md).
The items below remain broader compatibility and acceptance work.

1. **Audio continuity:** measure sustained delivery and worst-case frame cost on
   current players. Keep synthesis corruption, transport coherency and device
   starvation separate. Per-app AHI/Paula and explicit AX options already exist;
   broader AX/driver and long-session acceptance remain necessary.
2. **Compatibility:** broaden supported mapper/board testing, including
   CRC-selected MMC1/MMC5 battery variants. Bounded NES 2.0, UNIF and mapper
   7/11/66 integration are included in 0.8.12; [scope](cartridge-formats.md).
   Native, ARM and physical banking/state checks pass, including legacy saves
   and hardware-created states. Additional boards, unsupported submappers,
   wider mirroring cases and commercial-title coverage remain. Unknown layouts
   are refused; importing upstream code does not establish compatibility.
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
