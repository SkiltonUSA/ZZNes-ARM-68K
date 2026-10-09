# ZZFceux integration evidence — 9 October 2026

[Player documentation and results](../../../fceux_player/README.md).
Final tests: `mario-final300.log/json`, `smw-locked300.log/json`. Normal mode
checks the first framebuffer; periodic VERIFY is retained. `mario-audit300.log`
checks six frames on the earlier sparse-publication build. Baseline metadata
records successive frontend experiments. Do not compare differently
instrumented runs as pure core speedups.

Native tests compare conversion, emphasis, PCM, cancellation and scripted
Start for both ROMs. Initial ARM adapter model checks 120 frames/ROM plus
actual framebuffer byte writes. `final-profile-arm-model.log` checks the final
ARM artifact; its ELF is byte-identical to the final executable's embedded ARM
build. The last host-only change uses bounded polling under the bitmap lock.

`controls-test.log` records a test-harness failure reading an open log, not an
Amiga failure. Subsequent resume/mute/exit logs and closed `controls.log`
record recovery and successful target shutdown. See `controls-assessment.json`.

Every final 300-frame run submitted/completed all audio samples, with no AHI
error; each still counted 299 completed-predecessor observations. The owner
subsequently confirmed picture and sound work in the live Mario Bros test
(selected option 1). This does not establish 60 FPS or other-game compatibility.
Mario Bros was left running; `live-state.log` confirms screen and Core1 owner.

No ROM bytes or user save data are included. The installed Mesen ZZNes MD5 is
unchanged. Rebuild sources are identified in `build.json`; generated integration
changes are recorded as patches. Model checks are distinct from physical
MMU/cache/flip/return evidence.
