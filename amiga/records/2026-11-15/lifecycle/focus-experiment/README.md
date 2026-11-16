# Window activation experiment — not accepted

The baseline 2,400-frame NES run switched window → fullscreen → window, but
an untitled Workbench window held focus after returning. The test deliberately
did not send F10 to that window. The player completed its frame limit and
released Core1 normally.

A private 68k candidate scheduled one ActivateWindow call 100 ms after
returning to windowed mode, following the DOSBox approach. The same focus check
still failed, so this change was removed from the production build pipeline.
Its 2,400-frame run, PCM completion and restoration/release checks passed.
A second diagnostic candidate logged activation calls, but its initial window
already lacked focus. No input was injected; it also completed 2,400 frames
and released cleanly. That run did not exercise the delayed activation path.

These results do not identify which Workbench component changes focus.
AutoPoint, ClickToFront and other applications were running; their presence
alone is not evidence of causation. No global preference or background task
was disabled. F10 exit remains unverified by these unattended tests.

`prepare_window_focus.py` is the rejected experiment, not a production overlay.
The trace build reused the recorded exact-noise ARM payload. First candidate
SHA-256: 653691cca7278f767c78e65b777f057ccdccb442e7993bb7bd7c860b7fac6c8e.
`trace-build.json` identifies the later diagnostic binary. The raw runner
assertion failures are retained to distinguish incomplete tests from passes.
