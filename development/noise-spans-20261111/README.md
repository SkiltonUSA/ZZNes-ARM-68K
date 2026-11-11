# Exact HQ noise spans — experimental

The original HQ noise renderer decrements its timer for every audio tick and
updates the LFSR on expiry. This candidate processes the constant-output span
up to that expiry. It skips zero additions but still advances timers and the
LFSR while muted. Both feedback taps, phase, volume and PAL/NTSC period tables
are retained. The FIR, sample rate, state format and AHI path are unchanged.

`prepare_noise_spans.py` patches only the HQ `RDoNoise` loop. The default build
is unchanged. Build separately with:

```sh
python3 scripts/build_current.py --release-ax --audio-noise-spans
clang++ -O2 -fsanitize=address,undefined development/noise-spans-20261111/test.cpp -o /tmp/zznes-noise-test
/tmp/zznes-noise-test
```

The candidate is in `.context/noise-spans-build`. `test.cpp` compares every
sample, timer and LFSR endpoint with a scalar reference over 60,000 deterministic
cases, including buffer guards, muted output, zero/negative counters, both taps
and varying periods. Unsigned additions/subtractions retain 32-bit wrap.

Full-core comparison uses `development/output-quality-20261030/test_core_quality.py`
with `--exact --baseline .context/ax-release-build --candidate .context/noise-spans-build`
and a supplied `--rom`. Private ROMs are not included.

The ARM model's CPACR read needs the same correction already used by presentation
tests; `scripts/model_neon.py` supplies it. Exact SIMD tests now assert the
availability probe succeeds, rather than assuming that writing CPACR enables
the FIR path. The real hardware availability routine is unchanged.

Profiler `--neon` enables and verifies SIMD in the model. Without it, results
are explicitly scalar-fallback counts. Neither is a hardware speed measurement.
