# Noise-span optimisation checks

The candidate is opt-in (`--release-ax --audio-noise-spans`). Installed releases,
AHI preferences, firmware and saved display modes are unchanged.

[Implementation and reproduction](../../../../development/noise-spans-20261111/README.md).

## Model correction

The earlier 35.49% filter profile exercised scalar fallback. Writing the modeled
CPACR register was insufficient because Unicorn's MRC read returned a different
value. The existing presentation-test workaround now also applies to the audio
profiler and exact-sample test, with an availability assertion. This changes only
test tooling; hardware SIMD detection is unchanged. Earlier exact-audio runs
remain evidence for scalar fallback, not for execution of the SIMD FIR.

With verified SIMD, reference/candidate instruction totals for 30 Super Mario
World opening frames after 120 warm-up frames are 186269155/180915444: 2.87%
fewer modeled slots. FIR slots remain identical. These are not A9 cycles or FPS.

## Checks

60,000 native cases match every buffer word, noise register and timer, including
guards, both taps, mute and unusual counters. ASan/UBSan report no errors.
The historical native/ARM regression suite passes with Podman. The initial
attempt used the unavailable default Docker command and failed before testing;
this was corrected with AMIGA_CONTAINER_COMMAND.

600-frame full-core comparisons for Super Mario World, Contra and Castlevania III
pass on the scalar fallback path. Verified-SIMD checks also pass for all three games (600 frames each),
including unchanged FP registers, plus 180 PAL Contra frames. Logs named `*-arm.log` predate the availability
assertion; their `fallback=False` option does not prove SIMD was active.

## Hardware method

Same Super Mario World ROM, 1200 frames, Paula AHI mode 0002000e, window scale2,
software scanlines2. Reference/candidate/candidate/reference order. The private
new test drawer creates its first snapshot during the initial reference run;
do not use its wall time or startup silence to infer a speedup. Compare ARM
core time and preserve all audio starvation counts. No game data is published.

## Physical result

| Variant | Core time (s) | Starvations |
|---|---:|---:|
| reference | 13.976063 | 65 |
| reference | 13.975055 | 69 |
| noise | 13.570445 | 42 |
| noise | 13.570997 | 40 |

Mean ARM core time falls from 13.975559s to 13.570721s: **2.897% less**.
All four runs complete 638940 PCM sample frames, restore register/MMU/cache
witnesses, release memory and report no display fault. Starvation remains;
this is not a claim of perfect audio or increased guest target FPS. The
installed release remains unchanged pending broader hardware workloads.
