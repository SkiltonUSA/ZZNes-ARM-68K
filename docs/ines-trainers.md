# iNES trainer candidate

**Development only; not included in 0.8.9 Beta.** The normal release gate still
rejects trainer cartridges. Battery cartridges, NES 2.0 and UNIF remain outside
this candidate too.

The optional build reads the 512-byte trainer before PRG/CHR data, writes it to
$7000–$71FF after mapper power-on, and uses the pinned FCEUX read-handler fallback
when that board cannot read back the writes. PRG/CHR offsets and cartridge CRC
skip the trainer. Save-state ROM identity includes it. Original ROM files are
unchanged, including ZIP inputs and whitespace-tail recovery.

This follows the vendored FCEUX `ines.cpp` `iNES_ExecPower` behaviour. A trainer
is an iNES initialization payload; accepting one does not add new mapper IDs or
promise that every modified cartridge works.

## Validation

- Synthetic ROMs execute code from the trainer on mappers 0, 1, 2, 3, 4, 5, 78 and 90.
- All 512 bytes, PRG/CHR offsets, writable/fallback behaviour and save/load are checked under ASan/UBSan.
- Actual current HQ ARM payload passes execution and video/audio save-state replay on all eight mappers at two relocation addresses in a Cortex-A9 model.
- Plain, stored-ZIP and deflated-ZIP loaders preserve trainer bytes; truncated, invalid and non-whitespace tails remain rejected.

```sh
python3 scripts/test_trainers.py
python3 tests/test_nes_padding.py --trainers
python3 scripts/build_current.py --release-ax --trainer-test
python3 scripts/test_trainers_arm.py
```

The ARM model requires Unicorn. Candidate output is isolated in
`.context/trainer-build`; baseline core/adapter snapshots are not edited.
Both ARM and 68k builds complete. A physical 120-frame run of the original
mapper-0 trainer fixture at 800 MHz completed with three framebuffer checks,
zero display faults, register/cache-witness restoration and owned-memory release.
The player delivered all 63,887 generated samples without an audio-device error;
four queue starvations were recorded, so this is not an audio-quality result.
A further physical matrix completes 240 frames on each of mappers 0, 1, 2, 3,
4, 5, 78 and 90 with framebuffer checks and clean restoration/release. These
synthetic startup tests do not read back the guest trainer execution marker;
that proof comes from the native and ARM-model tests. Real-game compatibility
and interactive state checks remain pending.
[Physical mapper matrix](validation/trainers/mapper-matrix/summary.json).
No released binaries were replaced.

Fresh builds now include the previously validated 666/800 MHz host timer gate.
It measures the timer rather than assuming 333 MHz; this change does not set the
ARM clock or change guest timing. The configured output remains Paula 22 kHz by
default, with the existing alternatives retained.

[Recorded checks](validation/trainers/results.txt).

[Physical smoke test](validation/trainers/hardware.txt).
