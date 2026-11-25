# Battery-save validation

The isolated `--battery-test` candidate used the 0.8.10-dev label; its actual
artifact/source hashes are recorded in [candidate-build.json](candidate-build.json).
It is distinct from the released 0.8.10 player, which rejects battery cartridges.
The subsequent 0.8.11 release integration has a separate build identity.

## Native and Cortex-A9 checks

- MMC1/MMC3: 8 KiB; MMC5: 32 KiB. Each with and without a 512-byte trainer.
- Original guest programs read an existing counter, increment it and write RAM.
  MMC5 tests all four persistent banks. Unsupported battery mapper IDs are rejected.
- Sanitized native tests check power/import/trainer ordering, guest execution and
  state restoration. File tests inject open/write/close/readback/remove/rename and
  rollback failures at both save sizes.
- Exact candidate ARM code executes at two relocated addresses. A fresh instance
  imports the previous instance's RAM, increments its counter, and reproduces
  the expected full SRAM. State replay matches video, PCM and cycles.
- Legacy quality-0 and HQ state replay passes for PAL and NTSC. Ten existing
  physical saves load in the model and match their recorded first-resume video
  and CPU cycles. These are model checks, not new physical state-replay runs.
- Required `make test test-arm` regressions pass.

[Native](native.txt) · [ARM](arm.txt) · [Regressions](regression.txt) ·
[Legacy NTSC](legacy-ntsc.json) · [Legacy PAL](legacy-pal.json) ·
[Existing physical saves in model](existing-states.json).

## Physical Amiga matrix

Seventeen isolated tests completed on XX19d-RIX/XACP 1.8 with 800 MHz KEEP:
12 mapper/trainer fresh-and-restart runs, two deflated-ZIP runs, one missing-main
backup recovery, one wrong-size refusal and one orphan-temporary refusal.
Successful runs completed 120 frames and wrote SRAM matching the ARM model
byte-for-byte. Restart increments prove the saved bytes reached the guest.
The refusal cases retained their input files; recovery retained its backup.
All runs restored registers, MMU/cache witnesses and released owned memory.
Final status confirms Core1 idle, Core0 AGA inactive and the existing clock held.

[Results](hardware/results.json) · [Final status](hardware/status.txt).
Logs are included beside those results. Original generated fixtures and tests
are under `tests/amiga/emulator/battery.cpp`, `battery_files.c` and
`scripts/test_battery*.py`; no commercial ROMs or personal saves are included.

These synthetic cartridges validate persistence, not full-game compatibility
or listening quality. MMC1/MMC5 CRC-selected board variants still need wider
game coverage. No FPS or audio-quality gain is claimed.

## Reproduce

```sh
make test-battery
python3 scripts/build_current.py --release-ax --output-dir .context/battery-check
python3 scripts/test_battery_arm.py --build .context/battery-check
```

The ARM test needs Unicorn and LLVM tools. File failure tests run natively;
real Amiga filesystem/cache behaviour is covered separately by the physical matrix.

## Release integration

The normal `--release-ax` build now includes battery persistence.
[0.8.11 build](release-build.json) · [Candidate/release comparison](release-equivalence.json).
The embedded ARM payload is byte-identical to the matrix-tested candidate.
The ELF files differ in build paths; relevant host/launcher sources match after
substituting the product version. Fresh/repeat installation and final installed
player checks are recorded under `installation/`.

The fresh-installed 0.8.11 player passed two MMC5 battery runs with exact SRAM
comparison and two legacy HQ state resumes (Castlevania III windowed, Super Mario
World fullscreen). All restored host state and released memory. One short battery
restart reported one starvation; the other three reported zero. These are
persistence/lifecycle checks, not an audio listening or performance result.
[Final candidate checks](installation/candidate-checks.json).

The production installation at `SD032G:Emulator/ZZNES` matches the packaged
launcher/player hashes and preserves library/audio/input configuration hashes.
Installed Castlevania III and Super Mario World HQ saves resume for 120 frames
each, with zero reported starvations/device errors and clean teardown.
[Installed checks](installation/production-checks.json). Fresh, repeat and
production installer logs include successful signatures and dependency checks.
Missing-driver fallback policy is unchanged; no drivers were removed for this round.
