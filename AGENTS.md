# ZZNes-ARM-68K development

Read README.md, docs/session-handoff.md and the relevant core/player README
before changing code. Historical records are evidence, not current live state.

Build/test with `make test`, `make test-arm` and, for Mesen changes, `make mesen`
and its relevant native tests. Generated files and private ROMs stay in ignored
`.context/`; edit source adapters or generators, not generated C/C++ or patches.
Retain pinned upstream hashes, notices and licensing.

Do not deploy or launch hardware as part of a build. Real ZZ9000 work must
preserve runtime mapping verification, Exec-owned allocations, private MMU/cache
contracts, framebuffer bounds, cancellation and return/reset-before-free.
Only one Core1 application may run. Never assume a gap in DDR is available.
Do not change firmware or global AHI preferences as a performance shortcut.

Keep displayed FPS distinct from headless throughput and core-time ratios.
Native/instruction-model tests do not establish hardware coherence, audio
acceptance or real AmigaOS cleanup. Record failures as well as successes.

The original installed Mesen baseline differs from the current source candidate;
see artifacts/README.md. Never present an experimental binary as the default.
Never commit commercial ROMs, credentials, firmware or Amiga system software.

Current beta source/build inputs are in `development/beta-20261015/`; use
`make current-arm`, `make test-current` and `make verify-current` for that path.
The old Mesen experiments and their recorded baselines remain historical.

The current launcher source is `development/zip-20261016/source/`; use
`make test-library-large` after library changes. Current 68k host overlays are in `development/zip-20261016/host/`; the ARM
payload remains from the original snapshot. Run `make test-zip` after archive changes.
