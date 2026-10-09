# ZZNes-ARM-68K

Experimental NES emulation for an Amiga with a **ZZ9000 Cortex-A9**, using
**XANI's XACP firmware interface**. The ARM runs the NES CPU, PPU and APU and
writes completed pictures into the card's framebuffer. The 68k handles AmigaOS,
keyboard input, display ownership, buffer flips and AHI audio delivery.

This repository backs up both development paths: the original **Mesen-based
ZZNes** and the newer, faster **FCEUX-based ZZFceux**. It includes sources,
build scripts, tests, hardware evidence and the exact saved Amiga executables.
It does not contain commercial ROMs, Amiga system software or firmware.

## Current result

On the owner's A4000TX, ZZFceux displays about **44 FPS with audio enabled**.
The owner confirmed that Mario Bros' picture and sound work. **60 FPS has not
been achieved.** These are short startup tests, not whole-game compatibility
or an assertion of perfect audio timing.

| 300-frame hardware workload | Mario Bros, mapper 0 | Super Mario World, mapper 90 |
| --- | ---: | ---: |
| ZZFceux displayed FPS, AHI enabled | **44.19** | **44.30** |
| ARM emulation + player adapter | 5.813 ms/frame | 7.084 ms/frame |
| ARM presentation | 3.324 ms/frame | 3.323 ms/frame |
| FCEUX headless core time | 4.946 ms/frame | 6.104 ms/frame |
| Earlier Mesen core time | 28.961 ms/frame | 31.141 ms/frame |
| Ratio of measured core times | 5.86× | 5.10× |

The core-time gain comes from a different, lighter emulation model and settings,
not NEON or SDL. Headless throughput is not displayed FPS. Earlier Mesen player
measurements were 23.75/22.58 FPS, but had six full framebuffer readbacks versus
one in normal ZZFceux play; that is not an identical instrumentation comparison.

The frontend improved from 36.41 to 42.50 FPS by reducing diagnostic transfers,
then to 44.19 FPS by bounded polling during the short locked presentation request.
Other requests still yield. Every-frame mapping, ownership, command and flip
checks remain. The measured runs completed all audio samples with no AHI errors,
but both recorded 299 completed-predecessor audio gap observations. That counter
alone neither proves nor rules out audible gaps. See the
[player findings](amiga/fceux_player/README.md),
[headless comparison](amiga/fceux_bench/README.md) and
[original logs and owner acceptance](amiga/records/2026-10-09/fceux-player/).

## Hardware and XACP

Verified on A4000TX / TF4060 / AmigaOS 3.2.3, with ZZ9000 Cortex-A9 Core1
(nominal 666 MHz), **XX19c firmware and XACP 1.7**. The ZZ9000AX is installed,
but this player uses **AHI unit 0, configured as Paula on the test machine**.
Direct ARM-to-AX or HDMI audio is not implemented.

XACP provides the firmware-side facilities used to start and coordinate Core1
and perform deferred display panning. XANI's fullscreen buffer-flipping example
guided the presentation path. ARM writes the owned P96 bitmap on the card;
the 68k does not copy every displayed RGB frame over Zorro. Audio currently
passes through the 68k AHI frontend.

The launcher reserves a real 4 MiB Exec allocation and validates its mapping at
runtime. Private MMU/L1 mappings, noncacheable control state, bounded framebuffer
access and return/reset/cache checks are part of the contract. No unowned DDR
range is assumed free. **Only one Core1 application may run at a time.** Close
ZZQuake, PicoDrive, other XACP applications and earlier NES players before launch.
Support for other firmware versions has not been established.

## Run the saved player

The exact owner-tested executable is [artifacts/fceux-player/ZZFceux](artifacts/fceux-player/ZZFceux):
265,660 bytes, MD5 `ce77a7b5fd6a453d50a9a697b86d3ae9`.
Copy it into a directory on the Amiga, then in that directory run:

```text
Protect ZZFceux +e
Stack 65536
ZZFceux
```

The file requester selects your own uncompressed `.nes` ROM. Current FCEUX
scope is **NTSC iNES mapper 0 or 90 with CHR ROM**, without battery saves,
trainers, four-screen mode or NES 2.0. It is a limited development port, not
the complete desktop FCEUX application. It uses the old PPU, eight-sprite limit
and quality-0 32 kHz mono audio; no emulated frames are skipped.

| Key | Action |
| --- | --- |
| Arrows | Direction |
| Z / X | A / B |
| Return / Left Shift | Start / Select |
| P / M | Pause / mute |
| Q / Escape | Quit to Workbench |

The supplied `Start-*` scripts retain the test Amiga's `SD032G:Dev/...` paths;
edit those paths for another installation. See [artifact status](artifacts/README.md)
before choosing a Mesen binary. Running the standalone player does not require
the Mac, Ethernet or AmigaBridge.

## Build on macOS

Install Python 3, Clang, Homebrew `llvm` and `lld`, and a working Docker or
Podman engine capable of running the pinned Linux/amd64 cross-toolchain image.
The current scripts use Homebrew's Apple Silicon paths for LLVM tools:
`/opt/homebrew/opt/lld/bin/ld.lld` and `/opt/homebrew/opt/llvm/bin/llvm-nm`.
Other host layouts need those paths adapted. Sources for both selected cores
are vendored with upstream revisions and SHA-256 checks.

```sh
make                         # ZZFceux, native reference and ARM/68k builds
make bench                   # standalone headless FCEUX benchmark
make test                    # generated original test ROM + native checks
make mesen                   # current Mesen development candidate
```

Docker is the default. For Podman, set its actual connection name:

```sh
export AMIGA_CONTAINER_COMMAND='["podman","--connection","YOUR_CONNECTION"]'
make
```

Outputs stay under `.context/amiga/`. `make mesen` also downloads pinned public
CPU test fixtures into that ignored directory. Nothing is deployed or launched
on the Amiga by a build or host test.

For ARM instruction-model checks, install Unicorn in a virtual environment:

```sh
python3 -m venv .context/venv
.context/venv/bin/pip install unicorn==2.1.4
make test-arm MODEL_PYTHON=.context/venv/bin/python
```

The model checks alignment, adapter/native agreement and guarded presentation;
it does not prove real cache coherence or AmigaOS execution. Recorded physical
results are separate. Native FCEUX tests use ASan and selected UBSan checks;
array-bounds and pointer-overflow checks are disabled for upstream biased bank
pointers. This is not a claim of fully defined ISO C++ pointer arithmetic.

## Backup and development status

This is a **9 October 2026 development snapshot**, including previously
uncommitted sources. [Backup provenance](docs/backup-origin.json) records their
origin and hashes; [session handoff](docs/session-handoff.md) records which
executables were installed versus experimental. Historical logs retain their
original paths and states. Current status in this README takes precedence over
earlier milestones' next-step notes.

Only the toolchain helper and shared ELF helper were reduced for standalone
use; emulator, launcher, MMU and frontend implementation sources were copied
unchanged. New repository documentation, Makefile and test runner support this
backup. [Verification](docs/backup-verification.md) distinguishes the original
hardware-tested binaries from a fresh build in this checkout.

The next target is profiling the remaining 68k scheduling, flip pacing and
audio-delivery overhead. A specific 60 FPS fix is not yet proven.

## Credits and licenses

- **XANI / Xanxi-Amiga:** [XACP-ZZ9000](https://github.com/Xanxi-Amiga/XACP-ZZ9000)
  and the [ZZPicoDriveMD fullscreen example](https://github.com/Xanxi-Amiga/XACP-ZZ9000/tree/main/applications/emulators/ZZPicodrive/ZZPicodriveMD).
  XACP is the platform this project builds on; no PicoDrive source is copied.
- **FCEUX contributors and Rezzy-dev:** [FCEUX fork](https://github.com/Rezzy-dev/fceux),
  commit `4d01530b6689b06a6d7cf0679b63625e3270ae9a`, GPL-2.0-or-later.
- **SourMesen and contributors:** [Mesen](https://github.com/SourMesen/Mesen),
  commit `e1180957b31979d4b82d613af9263fcb9442a685`, GPL-3.0-or-later.
- **Shay Green:** blip_buf, retained with its LGPL notice and license.
- **[Amiga-MCP-Debugger](https://github.com/SkiltonUSA/Amiga-MCP-Debugger):**
  the runtime-verified launcher and debugging work from which this project grew.
  Hardware development used [geekychris/amiga_mcp](https://github.com/geekychris/amiga_mcp).

Our integration is GPL-3.0-or-later; upstream notices remain in their source
directories. See [LICENSE](LICENSE) and [third-party notices](THIRD_PARTY.md).
