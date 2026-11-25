# Physical trainer and save-state matrix

Development trainer candidate; public 0.8.9 Beta is unchanged.

At 800 MHz, ten cartridges each completed a 900-frame run with paused save/load,
then a 120-frame fresh-process resume. The matrix alternates fullscreen/windowed
output and uses Paula AHI at 22 kHz. All twenty runs completed audio delivery with
zero reported queue starvations or device errors, and restored registers/cache
witnesses and released owned memory. Pauses are included in elapsed time; these
are lifecycle tests, not FPS benchmarks or listening acceptance.

Eight synthetic fixtures cover mappers 0, 1, 2, 3, 4, 5, 78 and 90. Each physical
save contains the expected $5A execution marker in guest RAM, confirming execution
of trainer code on the Amiga. Super Mario World and Castlevania III provide
non-trainer regressions. All ten physical saves load in the relocated Cortex-A9
model; first-resume guest cycles and video hashes match the physical fresh runs.
Physical audio samples were not captured for a bitwise comparison.

No supplied real-game ROM had the trainer flag. Modified trainer-game compatibility,
full gameplay and listening acceptance remain unverified. ROMs and save-state
contents are private test inputs and are not included here.

Tested player SHA-256:
`d4bd73004525b679f0dd592ddab5b65683746202c833b408e8c73516350d61c4`

Tested ARM ELF SHA-256:
`0c2b3997526af9b11f63ec8e2e1df17875e18854bf3317b53fe24ecaac2d9e7d`

See [physical results](summary.json), [state/model results](model.json), individual
logs and [final idle status](final-status.txt).
