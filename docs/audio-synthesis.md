# NES high-quality audio synthesis experiment

The optimized high-quality core reduces measured core processing time by **26%**
relative to the unoptimized high-quality build. It preserves that build's audio
samples exactly. These changes are included in 0.8.8 Beta.
The earlier instrument distortion was traced to stale shared PCM, not the
synthesis core; the corrected candidate sounds clean. The Nestopia comparison
below records that diagnosis. [HQ save-state support](audio-states.md) now
passes exact replay and physical save/load tests; legacy states resume in their original synthesis mode.

## Changes

- **NEON integer FIR:** four filter taps per iteration, calculating the two
  adjacent convolution results together. Preserve the scalar low-32-bit product,
  signed shift and wrapping sum. No floating-point approximation or altered taps.
- **ARM word stores:** clear the same HQ wave-buffer range with multiple word
  stores instead of the freestanding runtime's byte-by-byte `memset`.
- **Square-wave event spans:** advance up to the next timer transition. Add a
  constant amplitude in batches, and skip silent duty-span writes. Preserve every
  output sample, duty phase and timer value, including zero/negative counters.

NEON is used only when the existing capability check succeeds. SIMD registers
and FPSCR are saved/restored once per filter call; the scalar fallback remains.
There are no changes to clocks, firmware, global AHI settings, mappings, runtime
allocation, register translation or presentation/audio queue policy.

## Physical A4000TX results

Same Super Mario World cartridge, fullscreen, Paula HiFi 22,030 Hz, 32 kHz mono
source, no input. Each short row is one 3,000-frame run; this is a serial
comparison, not a statistical benchmark. Core time excludes most host servicing.
Elapsed time includes startup/drain and frame pacing. Percentages are cumulative
core-time reductions from the HQ scalar reference; do not add them.

| Build | Core time | Elapsed | Core time reduction | Audio starvation transitions |
| --- | ---: | ---: | ---: | ---: |
| HQ scalar reference | 47.205 s | 60.567 s | — | 474 |
| NEON FIR | 38.672 s | 51.863 s | 18.08% | 36 |
| + word clearing | 37.242 s | 51.121 s | 21.11% | 0 |
| + square-wave spans | 34.926 s | 51.154 s | 26.01% | 0 |

All four completed 1,597,361 source sample frames and restored registers/MMU,
cache witnesses and owned memory. Completing all PCM alone does not exclude
audible gaps: the starvation count matters. Two silence buffers in the zero-gap
runs are startup/drain accounting, not starvation events.

The FIR + clearing build also completed **6,000 frames in 101.019 s** with zero
starvation and all 3,194,731 sample frames delivered. Extra speed in the span
version provides headroom; it does not increase the guest's target frame rate.
These are emulated frames, not a claim that every frame was displayed.
Contra also completed 3,000 frames with zero starvation, all 1,597,361 PCM
frames delivered and clean restoration/release. Listening confirmed Contra
sounds clean. Super Mario World still has reported instrument corruption;
compare that exact cartridge with desktop FCEUX before attributing it to the
common synthesis path.

## Verification

- 200 relocated ARM-model FIR cases, including 484/668/1,024 taps, arbitrary
  32-bit products, exact rounding/wrap, guard bounds and preserved registers.
- 280 clear ranges: empty, small, large, varied word alignment and canaries.
- 10,000 square spans compared against the original per-cycle loop under
  AddressSanitizer/UndefinedBehaviorSanitizer: phase, counters, samples and bounds.
- Full-core checks compare CPU/video endpoints and every audio sample. The final
  speed candidate matches the HQ scalar reference on 180-frame Super Mario World
  and Contra runs; PAL and disabled-NEON fallback checks pass as well.
- The original interpreter opcode bodies and translated-register path match
  CPU/video and every audio sample over 480 Super Mario World frames. This
  comparison found no register-translator cause for the remaining distortion.
- An instruction-model profile of three frames after 120 warm-up frames counted
  roughly 31% in the FIR and 7% in `memset`. These are executed instruction counts,
  not hardware cycle percentages.

## Remaining distortion and rejected filter experiment

Listening found the original HQ path cleaner than quality 0, but optimized HQ
still has some distorted instruments on the Amiga. A 1,200-frame capture after
the shared-memory copy and before AHI reproduces the distortion on the Mac.
No full-scale clipping was present. Private ROMs and audio recordings are
excluded from this repository.

The pinned FCEUX filter selects 44.1/48/96 kHz coefficient tables, with the 44.1
kHz table used at our 32 kHz source rate. Its measured FIR response is only about
-6.1 dB at 16 kHz. This creates an aliasing risk but does not prove the cause of
this game's instrument distortion. [Upstream filter selection](https://github.com/Rezzy-dev/fceux/blob/4d01530b6689b06a6d7cf0679b63625e3270ae9a/src/filter.cpp).

An isolated 668-tap 32 kHz filter uses an 11 kHz Kaiser-windowed sinc, unity DC
and quantized stopband attenuation below -58 dB NTSC / -61 dB PAL on the sampled
response grid. This changes the waveform intentionally; CPU/video endpoints
remain equal, and scalar/NEON implementations match exactly. Its extra filter
history delays startup output by four samples, not a different steady clock.

**Do not promote this filter:** listening reported the same corruption, and its
6,000-frame physical run had 29 starvation transitions. The speed-only candidate
retains the existing HQ coefficients. Filter design remains a separate topic.

At this stage, HQ states were unfinished: FIR history/position were absent.
The later [HQ state adapter](audio-states.md) addresses this. Legacy states
now resume in their original synthesis mode instead of being interpreted as HQ.
Default releases and installed launchers/players remain unchanged.

## Reproduce

From this repository, with the existing ARM/68k toolchains:

```sh
python3 scripts/build_current.py --release-ax --audio-core-quality 1 \
  --audio-fir-neon --audio-word-clear --audio-square-spans
```

Output: `.context/audio-core-q1-build-neon-clear-spans`. Omit the three optimization
flags for the scalar HQ reference. Each variant has its own build drawer.
`--audio-filter32` adds the rejected waveform experiment; `--audio-interpreter`
uses the original opcode bodies for diagnosis. Neither is a release default.

Native ARM-model tests require Unicorn; the square-span test uses host clang++
with address/undefined sanitizers. The source and tests are in
`development/output-quality-20261030/`. `scripts/generate_audio_filter32.py --check`
verifies generated coefficients. `scripts/profile_audio_core.py ROM BUILD`
reproduces the instruction profile; `llvm-nm` must be on PATH.

[Measurements and build fingerprints](../amiga/records/2026-10-30/audio-synthesis/).

## Nestopia reference and transfer diagnosis

Reference: [Nestopia JG 2.0.0](https://gitlab.com/jgemu/nestopia/-/tree/2.0.0),
commit `27246144887c78154584515f530c61497e92cd05`. A native C++ capture harness
uses its core API directly, with NTSC, no input, 48 kHz mono, output filter on,
and DMC pop reduction off. No Qt frontend, database override or ROM alteration
is used. The same private mapper-90 Super Mario World cartridge runs for
1,200 frames. The title screen is visually confirmed.

- Listening confirmed **clean Nestopia audio** and **clean ZZNES ARM-model
  audio**, while the earlier physical Amiga capture has instrument distortion.
- Nestopia produces 958,357 samples at 48 kHz. The ZZNES ARM model produces
  638,940 samples at 32 kHz. These are different synthesis pipelines, not
  bit-identical implementations or measurements of A9 speed.
- 12,089 consecutive APU register address/value writes match. ZZNES labels
  those writes one frame later; within-frame cycle offsets are 106–119 CPU
  cycles. This does not prove cycle equivalence, but finds no different note
  commands in the matched sequence. Nestopia has 11 more trailing writes.
- DMC sample playback remains disabled. Nestopia's pop-reducer on/off captures
  are byte-identical. Its traced/untraced captures also match exactly, and all
  filter/rate variants preserve the same video hashes.
- The ARM executable image used by the earlier physical capture and the model
  is identical: SHA-256
  `a42983961b68d1b66323b44657a7b826a3ffc706f1d8b108ac306445ec2b50d1`.
- Of 638,940 samples, the earlier Amiga capture differs from the model at
  **78,575 positions across 160 frames**. **78,505** of those samples match the
  previous frame at the same offset. The mismatch regions typically start on
  32-byte boundaries. This is evidence of stale audio blocks, not a reason to
  replace the synthesis core.

A physical transfer probe compares the first CopyMem result, a second read
after cache synchronization, and a third byte-wise read against per-frame
model hashes. It completed 1,200 frames with 249/214/176 mismatching blocks
respectively and clean ARM return/restoration/free. It had 13 starvation
transitions: instrumentation makes this unsuitable as a performance run.
A barrier-before-clean experiment still had 305/268/225 mismatches; it is not
a fix. An initial uncached experiment edited an unused header copy and is
invalid as a mapping test. The corrected mapping experiment is tracked
separately; do not interpret the invalid run as evidence against uncached IPC.

**Corrected mapping: 0/0/0 mismatches over 1,200 frames.** Pulling the complete
Amiga recording and converting its byte order confirms **all 638,940 samples
match the ARM model exactly**, not just the per-frame hashes. The PCM SHA-256 is
`13244703ef21328c2d0488b9b3446aa3b1bf8532f42b34b5e9ce0e59175f153e`.
Listening to the normal player confirmed clean audio and a large improvement.

The isolated fix maps the pages intersecting the 2 KiB shared PCM window as
normal, inner/outer noncacheable shared memory. Private synthesis buffers,
code cache, host cache synchronization and return/reset-before-free stay as
before. Tests cover all 64 possible 64-byte allocation offsets within a page;
adjacent private pages, ROM, mailbox and allocation bounds retain their policy.
This fixes the observed stale-publication path; the experiments do not identify
a particular Cortex-A9 silicon erratum.

The rebuilt normal player uses one read, without the probe's repeated reads or
per-block logging. It completed 3,000 frames in 51.120224 s, delivered all
1,597,361 samples, had **zero starvation**, and restored/released its resources.
The longer run ended cleanly at **5,891/6,000 requested frames** in 99.200984 s:
all 3,136,693 samples completed, zero starvation, and clean restoration/free.
It is not a completed 6,000-frame pass; the exit trigger was not established.
The following Contra/windowed attempt was blocked before launch because Core1
was occupied by another application.

Castlevania III (USA, mapper 5) follow-up: the installed player was confirmed
as 0.8.7-dev, CRC32 `EDB7CBDF`, without this fix. The same supplied cartridge
completed 1,200 frames in the native Nestopia reference and corrected ARM model.
The corrected player then completed **1,800 fullscreen frames in 32.041151 s**
on Paula, delivered all **958,414 samples**, and reported zero starvation,
zero display faults and clean restoration/free. Listening confirmed the live
audio was clean. This is an additional title-level acceptance result, not a
claim of full-game or cross-core cycle equivalence.
[Castlevania III evidence](../amiga/records/2026-10-30/nestopia-reference/castlevania3.json).

The subsequent Contra windowed control completed **1,800 frames in 31.602700 s**,
with all **958,414 samples** completed, zero starvation/display faults and clean
register/cache/MMU restoration and memory release. This verifies the windowed
path with the same corrected player; it was not a separate listening assessment.

The rebuilt ARM model matches all original PCM, video/cycle endpoints and APU
writes over 1,200 frames; the adapter's signed-16 output also matches the core.
`make test-current` passes. These validate transfer correctness and stability,
not a new FPS gain or complete HQ save-state support.

Build this isolated candidate with the earlier three speed flags plus
`--audio-shared-uncached`. It is generated in
`.context/audio-core-q1-build-neon-clear-spans-shared-pcm`.
[Physical results](../amiga/records/2026-10-30/nestopia-reference/hardware-runs.json).

Capture/build/comparison tools: `development/nestopia-reference/`.
[Comparison measurements](../amiga/records/2026-10-30/nestopia-reference/comparison.json).
ROMs, audio and register traces remain private. These initial tests preceded the 0.8.8 release; they did not change installed
defaults at the time.


## Further work

- Compare the same cartridge's APU output against a full desktop FCEUX reference,
  then inspect individual channels around the distorted instrument. The shared
  waveform artifact is not proof that every effect is an emulation defect.
- Extend compatibility coverage to more cartridge workloads. Legacy saves now
  retain their synthesis mode; HQ history/phase and fresh-process resume are tested.
- If more headroom is required, profile noise/triangle event spans and constant
  DMC spans. Keep exact timer/APU semantics, and measure each change separately.
- A multistage anti-alias resampler could reduce filtering cost, but the rejected
  filter test does not justify replacing the audio pipeline without comparison.
