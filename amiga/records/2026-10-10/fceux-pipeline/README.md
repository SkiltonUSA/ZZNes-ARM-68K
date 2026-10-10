# ARM presentation and pipeline experiments — 10 October 2026

Selected candidate: `--scheduling optimized-fast`, MD5
`4398f22b8de76db50aad845a384b8749`, 270,212 bytes. It changes ARM pixel packing
and retains the accepted scheduling/audio path. It is installed separately as
`SD032G:Dev/ZZFceuxPlayer/ZZFceux-fast`; previous executables are preserved.

## Measurements

| 300-frame, no-input, AHI-enabled workload | Mario Bros | SMW |
|---|---:|---:|
| Earlier accepted scheduling candidate | 53.71 FPS | 51.92 FPS |
| **Specialised ARM pixel packing** | **53.99 FPS** | **53.80 FPS** |
| Combined FRAME/PRESENT command, generic packing | 50.02 FPS | Not tested |
| Combined command, specialised packing | 47.99 FPS | Not tested |
| Specialised packing, pacing before flip queue | 52.98 FPS | Not tested |

Elapsed time includes the complete first-frame readback and final audio drain.
Mario's ~0.5% FPS difference is not a demonstrated speedup beyond measurement
variation. SMW gains ~3.6% in these runs. Presentation itself is consistently
**1.15 ms rather than 3.32 ms**: ~65% shorter and ~2.9× throughput for that
stage. Emulation/adapter time remains ~5.81 / 7.08 ms. No 60 FPS claim.

The new `fast_pixels.h` specialises BGRA32 to a palette lookup/store and ARGB32
to a palette lookup plus byte swap. The generic routine assembled each word
through byte packing. The 24-bit paths remain generic. Alpha stays opaque,
9-bit palette/emphasis indices and all RGB values remain identical. This is
ordinary integer ARM code, not NEON or a different emulation model.

The fast path's shorter drawing time largely becomes additional flip waiting;
CPU work saved is not automatically an equal full-player FPS improvement.
The next pipeline work should investigate safely overlapping writes to a free
slot with the preceding pending flip, preserving bitmap lifetime and ACK rules.

## Rejected pipeline approaches

The combined-command experiment starts emulation and presentation in one ARM
mailbox transaction (private opcode 10). The host obtains a fresh bitmap lock
first, supplies the validated address/format/pitch and both-end challenge, and
retains the lock through the request/flip. Private emulation completes before
any framebuffer mapping; mappings are revoked before reply. The whole command
has a 50 ms deadline, with synchronous reset before unlock/free on failure.

The host reserves a PCM queue slot before locking. With a single producer and
a worker that only frees slots, the following PCM copy cannot block under the
lock. Worker wake occurs after publishing the ARM command. No allocation,
cache policy, firmware or device preference changes were involved.

This passed physical sampled frame/cycle hashes, first-frame pixel validation,
audio completion and full teardown. It nonetheless waits for the preceding
flip before it can start emulating, reducing the overlap that the accepted
separate-command path already provides. More work in a single command was not
an improvement. These modes remain explicit experiments, not default launchers.
Moving the pacing delay before flip queuing also failed to improve performance.

## Validation

- Native ASan/UBSan comparison covers all 65,536 possible source indices in
  all four formats, including alpha/emphasis and output guards.
- A9 instruction-model runs match native emulation samples and check all four
  real ARM presentation formats, nonce rejection, cancellation, guards and
  mapping revocation. This does not model physical cache coherence.
- Combined-command native tests use the actual generated worker with explicit
  architectural stubs, covering dispatch, frame-before-draw order, PCM byte
  order, sparse/VERIFY publication, wrong token, stop and presenter errors.
- Physical 300-frame runs match six native sampled frame/cycle hashes, display
  every frame, complete all 159,725 / 159,724 samples without AHI errors, and
  pass RET1, all 14 registers, MMU/cache witness and owned-memory release.
- A physical `VERIFY` run checked complete framebuffer pixels at frames 1 and
  60, including a later rendered frame, and passed native samples, all 60
  flips, 31,945 completed samples and clean teardown.
- Existing generated audio-worker tests and 200,000 flip-state handoffs pass.
- No physical crashes, reboot, firmware update or global AHI changes occurred.

## Longer running and audio interpretation

The preceding owner-accepted build was stopped cleanly after **37,191 frames
in 677.5 seconds**, averaging **54.89 displayed FPS**. All 19,801,079 samples
completed. Inputs/pauses were not logged; this is a live-session observation,
not a controlled benchmark or proof of uninterrupted active gameplay.

At the requested 32 kHz, those samples represent 618.8 seconds of PCM. The
wall-clock interval was longer. Completion counters alone do not establish
continuous real-time sound or end-to-end audio/video synchronisation. Title
silence, game state and user pauses may affect what a listener notices. No
loopback latency measurement was performed. The owner accepted picture/sound
for that preceding build; the fast candidate requires its own acceptance.

The selected candidate completed **18,000 frames in 318.48 seconds (5.3 minutes),
56.52 FPS**, after Start was injected. All 18,000 flips and 9,583,486 samples
completed, with zero AHI errors, RET1, all 14 registers restored, MMU/cache
witness and clean memory release. See `fast-soak18000.log/json`. Progression after Start
is not supervised; this is a stability test, not five minutes of verified
continuous active gameplay. Any pauses/user input are not a deterministic
native replay. Short no-input tests provide the independent native comparison.

ROMs remain private and are not included. `variants/` contains historical
build provenance and generated patches. The final source/build record is
`selected-build.json`. SNES is a future roadmap item, not newly added support.
