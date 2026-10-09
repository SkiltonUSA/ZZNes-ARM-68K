# ZZFceux — experimental ZZ9000 NES player

FCEUX CPU/PPU/APU on ZZ9000 Cortex-A9 Core1, with the existing ZZNes 68k
frontend: fullscreen ARM framebuffer conversion, XACP XX19c deferred-PAN
triple buffering, keyboard input, pause/mute and AHI audio. This is a separate
candidate; installed Mesen-based ZZNes and the FCEUX headless benchmark remain
available.

Upstream: [Rezzy-dev/fceux](https://github.com/Rezzy-dev/fceux), pinned commit
`4d01530b6689b06a6d7cf0679b63625e3270ae9a`, GPL-2.0-or-later. Selected original
sources and license are in `../fceux_bench/vendor/`. Our integration is
GPL-3.0-or-later. Credit to [XANI's XACP platform and PicoDrive example](https://github.com/Xanxi-Amiga/XACP-ZZ9000)
for the documented XX19c firmware interface and fullscreen handoff approach.
No PicoDrive source was copied. SDL is not used.

## Physical results — 9 October 2026

Final candidate: **265,660 bytes**, MD5 `ce77a7b5fd6a453d50a9a697b86d3ae9`.
300 no-input startup frames, AHI enabled, every frame presented:

| ROM | Displayed FPS | Mean ARM emulation + adapter | ARM presentation |
|---|---:|---:|---:|
| Mario Bros (mapper 0) | **44.19** | 5.813 ms | 3.324 ms |
| Super Mario World (mapper 90) | **44.30** | 7.084 ms | 3.323 ms |

Elapsed time includes initial framebuffer verification and final audio drain.
These are actual full-player rates, not the headless core's 164–202 FPS
throughput. **60 FPS has not been achieved.** Startup workload only; no
whole-game compatibility claim. Earlier Mesen player tests measured 23.75 and
22.58 FPS, but they performed six framebuffer readbacks versus one in normal
ZZFceux play, so that is not an identical instrumentation comparison.

Both final runs displayed all 300 frames, matched six sampled native FCEUX
frame hashes/cycle counts, completed all 159,725 / 159,724 audio samples, and
passed RET1, MMU/register restoration, cache witness and memory-release checks.
There were **299 completed-predecessor audio gap observations** in each run.
Zero AHI errors and completed samples do not establish smooth audible playback;
**The owner subsequently confirmed that the picture and sound work** in the
live Mario Bros test. The counter remains a diagnostic observation, not proof
of an audible gap. This acceptance does not establish full-speed playback or
compatibility of other games.

A controls run accepted Start (frame hash changed from the no-input title),
paused beyond the normal duration of its 600-frame limit, resumed and exited
with Q after 360 frames. All flips and 191,669 audio samples completed and
cleanup passed. Mute/unmute keys were dispatched, but audible muting was not
independently confirmed. Live log reads failed while the app held the file
open; final validation used the closed log. No crash/reboot occurred.

Left Mario Bros running for owner testing, `ZZFceux fullscreen` plus Core1
owner port verified. Q/Esc exits. Original ZZNes is unchanged.
Evidence: [logs, provenance and comparisons](../records/2026-10-09/fceux-player/).

### Frontend findings

- Initial integration: Mario Bros 36.41 FPS with periodic full readbacks.
- Sparse diagnostic publication plus first-frame-only readback: 42.50 FPS.
- Shorter 250 microsecond timer waits: 41.78 FPS; reverted.
- Profiling separated ARM presentation (~3.9 ms including reply work) from
  the ~10 ms the 68k observed while yielding with the bitmap locked.
- Bounded polling for `PRESENT` reduced the observed handoff to ~4.4 ms.
  Other requests and frame pacing still yield; the 50 ms presentation deadline
  and reset-before-unlock cleanup remain. Final rates are the table above.

Remaining overhead involves host scheduling, flip pacing and audio delivery.
Do not attribute all of it to decoding or Zorro pixel bandwidth. Further
profiling is needed before claiming a specific AHI/OS cause or a 60 FPS fix.

## Launch and controls

Installed directory: `SD032G:Dev/ZZFceuxPlayer`.

```text
Execute SD032G:Dev/ZZFceuxPlayer/Start-MarioBros
Execute SD032G:Dev/ZZFceuxPlayer/Start-SuperMarioWorld
Execute SD032G:Dev/ZZFceuxPlayer/Start-ZZFceux
```

The last command opens a ROM requester. The first two use the owner's existing
ROMs in `SD032G:Dev/ZZNesPlayer/ROMs`; no commercial ROMs are distributed.
Launchers set a 65536-byte Shell stack and save a log in the player directory.
Close other Core1 applications before launch.

| Key | Action |
|---|---|
| Arrows | NES directions |
| Z / X | A / B |
| Return | Start |
| Left Shift | Select |
| P | Pause/resume |
| M | Mute/unmute |
| Q / Escape | Exit to Workbench |

Current scope: NTSC iNES mapper 0 or 90, CHR ROM, no battery/trainer/four-screen.
Old PPU, hardware eight-sprite limit, quality-0 32 kHz mono audio, every emulated
frame presented. Uses the existing player's RGB palette/emphasis approximation.
This has accuracy tradeoffs compared with Mesen and is not a general FCEUX port.
No battery saves, save states, rewind, joystick support or arbitrary mapper support.

AHI uses **unit 0**, currently Paula on this A4000TX. The fitted ZZ9000AX is not
selected by this player; no HDMI/AX audio or global AHI configuration changes.
The AHI owner is the previously tested DOS Process, with an eight-block queue,
three-frame prebuffer, ordered immutable PCM slots and explicit drain/cleanup.

## Presentation and validation

The adapter packs FCEUX's separate pixel/emphasis buffers into the existing
9-bit pixel-index format and converts 32-bit PCM container values to signed
16-bit samples. The ARM converts completed pixels directly into the owned P96
screen bitmap. The 68k coordinates commands/flips and feeds AHI; it does not
copy each displayed RGB frame across Zorro.

Normal play checks the complete first framebuffer. Every frame still uses
bounded temporary mappings, both-end nonce challenges, mailbox sequencing,
private-frame hash consistency and deferred-PAN acknowledgement. Raw diagnostic
pixel publication/readback is skipped after the initial verified frame.
Diagnostic `VERIFY` restores full readback on frame 1 and every 60th:

```text
Stack 65536
SD032G:Dev/ZZFceuxPlayer/ZZFceux 9fc10110 RUN "SD032G:Dev/ZZNesPlayer/ROMs/011 Mario Bros.nes" 300 VERIFY >SD032G:Dev/ZZFceuxPlayer/audit.log
```

The initial integration copied diagnostic indices every frame and checked the
complete framebuffer every 60 frames. It measured 36.41 FPS for 300 Mario Bros
startup frames, with six successful readbacks and all audio samples completed.
This exposed frontend overhead after the much faster core was integrated.

## Memory and cleanup

Uses the existing runtime mapping probe and private L1/outer-NC MMU contract.
The entire 4 MiB block belongs to a real Exec allocation. FCEUX BSS stays at
allocation-relative `0x220000` below the stack reserve. Frontend pixels/PCM and
ROM occupy the existing disjoint player ranges below that. No firmware shared
DDR allocation is invented. The strict FCEUX ELF packer validates relocations.

A locked bitmap outlives outstanding ARM writes; framebuffer mappings are
revoked before ACK. Core1 RET1, synchronous reset, register restoration and cache
witness checks precede memory release. AHI drains and its DOS Process exits
before unloading code. Default ZZNes, firmware, drivers and Roadie are untouched.

## Build and checks

```sh
python3 scripts/build_fceux_player.py \
  --container-command '["podman","--connection","nuflix-converter-root"]'
python3 tests/amiga/fceux_player/check_native.py /private/game.nes 300
.context/amiga/mesen-bench/venv/bin/python tests/amiga/fceux_player/check_arm.py /private/game.nes 120
make test-amiga-arm test-amiga
```

Outputs live in `.context/amiga/fceux-player`. `frontend.patch` records generated
adaptations of the existing frontend/worker; shared production sources remain
unchanged. Native tests compare every pixel/emphasis and PCM sample, scripted
Start input and cancellation. ASan/UBSan exclusions for upstream biased bank
pointers are documented in `../fceux_bench/README.md`.

ARM instruction-model checks compare native frame hashes/cycles and verify four
framebuffer byte formats, challenges, padding guards, stop handling and mapping
revocation. Host tests cover triple-buffer handoff, AHI queue ownership and
shutdown. Model/native tests do not establish physical display, audible quality
or physical cache coherence; hardware results are recorded separately.
