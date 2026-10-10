# A4000TX ZZFceux scheduling experiments — 10 October 2026

The selected candidate is `--scheduling optimized` (alias of
`deadline-cadence3`), installed as `SD032G:Dev/ZZFceuxPlayer/ZZFceux-optimized`,
MD5 `bf14d8e7dc20970d95fcd110cc9e6754`. The previous default and its launchers
remain unchanged. The ARM loaded image is identical to the baseline profiling
build: SHA-256 `044a501aa79996b29336310f1bb43a5380afe94e5b78f75611082fcad1642f83`;
relocations and entry also match. These gains come from the 68k frontend.

## Method and results

Same A4000TX/TF4060, XX19c/XACP, 320×240 fullscreen deferred flips, private
MMU/cache contract, 300 no-input startup frames and first-frame framebuffer
readback. Full-player elapsed time includes readback and final audio drain.
Fresh default runs were taken after the owner's reboot. There were no crashes
or reboots during these experiments. No firmware or global AHI changes.

| Build/run | Mario Bros displayed FPS | Result |
|---|---:|---|
| Unchanged default (`baseline300.log`) | 42.79 | Fresh reference |
| Timer instrumentation (`profile300.log`) | 43.86 | Timer waits include substantial scheduling delay |
| Avoid timer under bitmap lock (`locked300.log`) | 43.81 | No material gain |
| Busy frame wait / accurate per-frame pacing (`deadline300.log`) | 35.02 | Starves priority-0 audio worker; queue reaches eight slots |
| Raise audio worker to priority 5 (`priority300.log`) | 38.63 | Worker preempts frontend before presentation |
| Wake audio after issuing next ARM frame (`overlap300.log`) | 47.61 | Useful concurrency |
| Clone whole opened AHI request (`copy300.log`) | 47.55 | Request initialisation correction, not a speed gain |
| Submit pair under short Forbid (`batch300.log`) | 47.57 | Moves measured delay, no throughput gain; not selected |
| Coalesce two PCM blocks (`coalesce300.log`) | 47.10 | Fewer AHI calls alone insufficient |
| Two blocks + bounded cadence recovery (`cadence300.log`) | 49.51 | Recovers small scheduling delays |
| **Three blocks + bounded cadence recovery** (`cadence3-mario300.log`) | **53.71** | **Selected candidate** |
| No AHI output (`noaudio300.log`) | 56.83 | Diagnostic only; APU still emulated; not a sound-capable result |

Super Mario World: unchanged default **43.89 FPS**, selected candidate
**51.92 FPS**, in `smw-baseline300` / `cadence3-smw300` logs and JSON. Gains are
25.5% and 18.3% respectively. ARM emulation/adapter remains about 5.81 / 7.08 ms
per frame and ARM presentation about 3.32 ms. These are short startup workloads,
not sustained whole-game results. 60 FPS has not been established.

## What changed

1. Profile requested/actual timer waits and AHI submission wall time. These
   include OS preemption; they are not exclusive CPU-time measurements.
2. Poll bounded ARM FRAME/PRESENT and flip acknowledgements without timer
   sleeps while locked. Keep mailbox deadlines, 100 ms flip timeout,
   cancellation, exclusivity and reset-before-unlock/free unchanged.
3. Use priority 5 for the DOS audio Process. Publish immutable PCM blocks, but
   wake the worker after publishing the following ARM FRAME command so audio
   handling overlaps useful ARM work.
4. Clone the complete opened AHI request for the second buffer, as in the
   [AHI author's device-interface guide](https://www.lysator.liu.se/ahi/v4-site/files/ahi/doc/ahidev_14.html).
   Preserve the linked request until its successor is submitted.
5. Coalesce three ordered blocks into each of two 6144-byte worker-owned AHI
   buffers. Each block is bounded at 1024 signed-16 samples. Do not drop,
   resample or rewrite PCM. Flush partial groups on pause/exit; clear the flush
   condition after the queue drains so batching resumes.
6. Carry a 16,639 µs deadline across frames. Recover small delays rather than
   restarting a full interval after every late frame. Reset after lateness
   above two frame intervals or pause; never skip emulation or presentation.

The batch size spans about 50 ms of emulated sound and changes latency. It is
not proof of perfect audio/video synchronisation. The unchanged three-frame
startup prebuffer and eight-slot producer ring remain. AHI device completion
proves request completion, not that a listener heard uninterrupted output.

Current `ENV:Sys/ahi.prefs` matched the previous inventory byte-for-byte.
AHI unit 0 is Paula Fast 8-bit mono at 8000 Hz; Music Unit 255 is ZZ9000AX
16-bit stereo at 32000 Hz. The app submits 32000 Hz signed-16 mono to unit 0.
Device reports `ahi.device 4.180 (10/31/1997)`, 68060 version. No preference or
sampling-quality shortcut was used. This candidate does not use AX or HDMI.

The pair-submission diagnostic reduced measured SendIO wall time from about
4 seconds to 17 ms per 300 frames without changing total FPS. This demonstrates
why attributing those 4 seconds to CPU work inside SendIO would be misleading:
preemption moved to Permit. The experiment is retained, not selected.

## Validation and limits

- Both selected 300-frame ROM tests: all 300 flips, six sampled native
  frame/cycle matches, first complete framebuffer readback, completed samples
  159,725 / 159,724, zero AHI errors, RET1, all 14 registers restored,
  MMU/cache witness and owned-memory release.
- Gap observations: baseline 299/299; selected 63/73. Coalescing reduces request
  count, so this is not a like-for-like measure of audible gaps.
- Interactive run: Start changes frame hashes; 15-second pause outlasts the
  normal 600-frame limit duration; resume, M twice and Q end after 432 frames.
  All 230,003 samples and flips complete; clean Workbench return.
- ASan/UBSan deterministic tests exercise the actual generated worker: 1838
  ordered blocks including mixed sizes, ring wrap, short/forced flushes,
  allocation/device failures, cancellation and cleanup. Pacing tests cover
  overshoot, long stalls, pause reset and 32-bit clock wrap. Existing flip
  model passes 200,000 handoffs. Models do not reproduce OS task scheduling.
- No core/ARM changes: loaded payload/relocations/entry equality checked;
  existing runtime mapping, cache, nonce and teardown contracts preserved.
- The owner subsequently selected “Picture and sound are good” for the live
  optimised Mario Bros build on 10 October. This is subjective acceptance of
  that ROM/build; SMW, measured latency and audible mute behaviour remain
  separately unconfirmed.

Detailed evidence is in the adjacent closed logs, JSON summaries, controls
records and `validation.json`. `variants/*/build.json` and `frontend.patch`
record historical builds; they intentionally describe earlier source states.
`selected-build.json` records the final source/provenance. No ROMs are included.

Next work should measure longer interactive workloads and audio timing, then
profile overlap between emulation, presentation and AHI. Increasing batches
further trades latency for overhead; it is not a free route to 60 FPS.
