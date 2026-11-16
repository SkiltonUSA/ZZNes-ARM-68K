# HQ noise spans: additional hardware coverage

The opt-in noise-span candidate was compared with the unchanged release on
XX19d-RIX / XACP 1.8, with Paula output and 2x windows. All runs complete PCM
retirement, display handoff, register/MMU/cache restoration and memory release.

| Workload | Frames/run | Reference core time | Candidate core time | Reduction |
|---|---:|---:|---:|---:|
| Castlevania III, reference/candidate/candidate/reference | 1,200 | 13.691224s mean | 13.548003s mean | 1.05% |
| Contra PAL, one pair | 1,200 | 14.094016s | 13.589241s | 3.58% |

These are ARM core-time reductions, not guest FPS increases. A first automatic
thumbnail and variable host scheduling affect wall time; they are not included
in the gain calculation. Device starvation remains (see every raw log); there
is no unattended listening result or claim that crackling is resolved.

The 60,000-case ASan/UBSan noise comparison passes. Castlevania III legacy-state
continuation, fresh relocation, re-save identity and malformed-state checks
pass. Contra PAL HQ state restoration also passes. The state-test harness now
asserts that modeled NEON access really succeeds: writing Unicorn CPACR alone
was insufficient. This corrects test coverage; target SIMD detection is unchanged.

Installed binaries and release versions remain unchanged. No commercial ROMs
or save-state contents are included. The table above covers windowed operation; fullscreen results follow below.

Additional native regression: settings migration and scan cancellation pass;
20,000-entry duplicate compaction, ZIP/plain input guards and launcher layout
pass under their test harnesses. The relocated ARM display comparison passes
all tested formats/views, SIMD restoration and cancellation (2,640 NEON row
calls). The first invocation needed the workspace Python and LLVM paths;
that setup failure is not counted as an emulator failure.

## Fullscreen follow-up

One reference/candidate pair: 1200 frames each; ARM core time
13.608575s → 13.513393s (0.70% reduction).
Audio starvation observations were 192 → 250. Both runs
retired 638,940 PCM frames, passed the display handoff and teardown
checks, and restored register/MMU/cache witnesses. This is additional coverage,
not proof of audible improvement. The experiment remains opt-in.

Further [physical lifecycle checks](lifecycle/README.md) cover save/load,
screenshot, window/fullscreen transitions and fresh-process resume.
