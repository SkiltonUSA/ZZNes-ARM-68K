# Muted HQ noise advancement — experimental

This opt-in renderer advances eight NES noise LFSR events at once while the
channel amplitude is zero. It still advances the exact timer and shift-register
state, so a later volume or feedback-tap change resumes at the same point.
Audible spans use the existing renderer. PCM format, FIR, sample rate, save-state
format and host audio scheduling are unchanged.

For taps 8 and 13, each of the first eight new feedback bits depends only on
the incoming 15-bit state. The packed recurrence is:

```c
((state << 8) | (((state >> (tap - 7)) ^ (state >> 7)) & 255)) & 0x7fff
```

A scalar event consumes the initial partial period; eight-event groups and a
short scalar remainder follow. Residual ticks stay in the original counter.
This needs no division, lookup table or additional runtime allocation. Inputs
retain the core contract: a valid NES period and feedback tap.

## Build and reproduce

```sh
python3 scripts/build_current.py --release-ax --audio-noise-spans --audio-noise-muted
clang++ -std=c++11 -O2 -fsanitize=address,undefined \
  -Idevelopment/noise-spans-20261111 \
  development/noise-muted-20261115/test.cpp -o /tmp/zznes-muted-test
/tmp/zznes-muted-test
python3 development/noise-muted-20261115/test_arm.py
python3 development/noise-muted-20261115/create_noise_rom.py > /tmp/noise-switch.nes
```

The ARM fixture requires Unicorn and LLVM with the ARM target. Set `LLVM_BIN`
if LLVM is installed elsewhere. The full build also needs the existing Amiga
cross compiler/container; see the repository build instructions. Output is
`.context/noise-muted-build`; the ordinary build remains unchanged.

Build the matched reference with `--release-ax --audio-noise-spans`, using the
same compiler and source revision. Compare both through
`development/output-quality-20261030/test_core_quality.py --exact`, supplying
`--baseline`, `--candidate`, `--rom` and `--frames 120`. Add `--pal` for PAL.
Use the original generated fixture above without a commercial ROM.

For full-core profiles:

```sh
python3 scripts/profile_audio_core.py ROM.nes .context/noise-spans-build --neon --instruction-hooks --warmup 120 --frames 3
python3 scripts/profile_audio_core.py ROM.nes .context/noise-muted-build --neon --instruction-hooks --warmup 120 --frames 3
```

The profiler verifies modeled NEON availability. `--instruction-hooks` counts
individual instruction callbacks rather than translation-block lengths. Neither
method measures Cortex-A9 cycles, cache stalls, audio delivery or displayed FPS.

[Results and raw records](../../amiga/records/2026-11-15/noise-muted/README.md).
