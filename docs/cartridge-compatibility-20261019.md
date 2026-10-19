# Cartridge compatibility — 0.7.4-dev

Holy Diver and Cybernoid now reach gameplay on the A4000TX. The fixes are in
the emulator; neither supplied ROM was modified.

- **Holy Diver:** mapper 78 bank switching, with the legacy header flag selecting
  its horizontal/vertical nametable wiring. The other mapper 78 variant retains
  single-screen mirroring. ROM bus conflicts are applied before switching banks.
- **Cybernoid:** CNROM/mapper 3, including ROM bus conflicts. Its supplied header
  contains `DiskDude!` in bytes 7–15, which previously produced mapper 67 and an
  incorrect PAL indication. Only that exact signature is normalized in memory.
  ROM bytes and save-state ROM identity remain unchanged.

The development player accepts **0, 1, 2, 3, 4, 5, 78 and 90** under the existing
bounded iNES contract. Battery, trainer, NES 2.0 and other boards are not enabled
by this change. See the [full FCEUX integration stages](fceux-integration.md).

## Validation

| Check | Result |
| --- | --- |
| Mapper 78 bank and mirror combinations | All 256 latch values for both wiring variants |
| CNROM bank switching and bus conflicts | Passed against actual core handlers |
| State restore | Banks/mirroring restored; private game runs replayed identical video/audio |
| Header handling | Exact legacy signature recognized; malformed near-match rejected; ROM unchanged |
| Existing scrolling fixture | NTSC and PAL passed |
| ARM presenter regression | Both relocations, pixel formats, NEON/fallback, scanlines, cancellation and SIMD/MMU restoration passed |
| Amiga gameplay | Both supplied games reached gameplay |
| Amiga lifecycle | Pause, save, load, screenshot, window/fullscreen switch and F10 exit passed |

Physical interactive runs completed **2,520 frames for Holy Diver** and **1,594
for Cybernoid**. Display verification checked 44 and 27 frames respectively.
Both logs report zero register mismatches, zero cache-witness errors, audio task
error 0 and owned-memory release. Audio gap counters were 165 and 100 during
these interrupted screenshot/pause runs: they are functional tests, not smooth
audio or FPS benchmarks. A further 120-frame run of the final installed player
passed before reopening the launcher.

Earlier Holy Diver checks only reached the title animation. Gameplay was
confirmed in the subsequent runs shown below; title-only checks were not treated
as proof of a working game.

| Holy Diver | Cybernoid |
| --- | --- |
| ![Holy Diver gameplay](../artifacts/development/cartridge-20261019/holy.png) | ![Cybernoid gameplay](../artifacts/development/cartridge-20261019/cyber.png) |

## Build and install

`make optimisation` builds the matched **ZZNES** launcher and **ZZFceux-ui** player;
`make test-mapper78` runs the native mapper and scrolling checks. Both files must
be updated together. The installed pair includes the duplicate-scan progress
panel. The tagged 0.7.1 Beta archive is unchanged.

References: [mapper 78 wiring](https://www.nesdev.org/wiki/INES_Mapper_078),
[CNROM hardware](https://www.nesdev.org/wiki/CNROM),
[pinned FCEUX boards](https://github.com/Rezzy-dev/fceux/tree/4d01530b6689b06a6d7cf0679b63625e3270ae9a/src/boards).
