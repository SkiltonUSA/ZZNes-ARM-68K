# Muted-noise experiment

**Offline candidate only.** Installed binaries, defaults and release packages
are unchanged. Physical testing is deferred while another workspace uses the
Amiga, as requested. No audio listening or hardware speed claim is made.

## Instruction measurements

| Workload | Reference | Candidate | Reduction |
| --- | ---: | ---: | ---: |
| Linked ARM noise fixture, 32,768 muted ticks, period 4, tap 13 | 139,304 slots | 8,274 slots | 94.06% |
| Same fixture, period 96 | 5,837 slots | 402 slots | 93.11% |
| Castlevania III, whole core, three frames after 120-frame warmup | 17,802,359 instructions | 17,467,653 instructions | 1.88% |

The fixture uses translation-block instruction slots. The whole-core result
uses individual ARM instruction callbacks with NEON verified. Both are model
counts, **not cycles or FPS**. This short whole-core sample is not representative
of every game or scene. Audible fixture calls add one modeled slot; only muted
noise advancement is optimized. The matched core profile leaves the listed
CPU, PPU, FIR and other audio-function counts unchanged.

An initial comparison used an older reference binary and produced different
counts in unrelated functions. That comparison was discarded for attribution.
Both reported builds use the same current Clang and flags. Build hashes,
compiler and source hashes are in [manifest.json](manifest.json).

## Correctness and build checks

- All 65,536 combinations of 15-bit state and the two taps match eight scalar events.
- 60,000 native PCM/timer/LFSR cases, buffer guards, and long muted spans at all PAL/NTSC noise periods pass ASan/UBSan.
- 72 linked ARM32 fixture comparisons match every PCM word and state byte.
- Matched whole-core runs: 120 frames each of Castlevania III, PAL Contra and an original alternating-muted/audible-noise fixture. Identical CPU/video endpoints and PCM; 63,887 NTSC or 76,780 PAL output samples per run.
- HQ save/replay, fresh relocated-process replay and malformed-state nonmutation pass.
- Legacy save load/re-save, fresh legacy resume and subsequent HQ state use pass.
- Complete ARM/68k build, `make test`, `make test-arm` and `make test-current` pass. The last uses the candidate ARM payload and covers relocated pixels, scanlines, SIMD restoration, cancellation and mapping revocation.

The first generic native-test invocation selected Homebrew Clang with a missing
Mac SDK. Repeating with Apple Clang for native checks passed; ARM candidate and
matched reference both use the recorded Homebrew compiler. This was a local
toolchain setup failure, not an emulator failure.

Raw `.out` files preserve the successful checks; JSON state records include ROM
hashes without distributing game or save contents. The previous-reference
comparisons also passed but are not used for the performance table.

## Next acceptance gate

On an otherwise idle Amiga, alternate reference/candidate runs with identical
ROM, input, display and sound settings. Compare ARM core time, PCM completion
and starvation, then check listening, save/resume, view switching and clean
teardown. Keep the candidate opt-in unless those checks establish a useful gain.

[Implementation and commands](../../../../development/noise-muted-20261115/README.md).
