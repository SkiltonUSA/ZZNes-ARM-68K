# High-quality audio save states

ZZNES 0.8.8 saves the FIR history and resampling phase. Loading
its states reproduces the next PCM samples, picture and CPU-cycle endpoints,
including in a fresh, differently relocated ARM instance.

The old adapter saved oscillator state and filter accumulators, but omitted
`WaveHi` and `mrindex`. Its first frame after loading already differed from an
uninterrupted run. The new adapter retains the 485 live history samples left by
`FlushEmulateSound`, plus the fractional resampling position. The cleared tail
of `WaveHi` is reconstructed instead of storing the entire 160 KiB buffer.
This adds **1,944 bytes** and stays within the existing 120 KiB transfer limit.

## Compatibility

HQ states use envelope version **2**, core/audio schema **0x20261030**. The matching
launcher validates the same format. ROM, region, size and checksum checks run
before deserialization; rejected files leave the running state unchanged.

Legacy quality-0 states use different oscillator-counter units. The player
loads them in their original synthesis mode, rebuilding that mode's tables and
callbacks before restoring the saved counters. It neither guesses a conversion
nor resets the game's audio state. Saving again retains the original v1 format,
which remains readable by the previous player. New games default to HQ; loading
an HQ save switches back to HQ. Both modes use the corrected shared-PCM mapping.

Old and HQ states are accepted only with matching version/schema pairs and
mode-specific payload lengths. Invalid states cannot change the synthesis mode.
New HQ saves require 0.8.8 or later.

This format covers quality 1 with the original 484-tap FIR at 32 kHz. The separate
experimental 32 kHz filter design cannot use this build option. No cached ARM
pointers, generated code or hardware state is serialized.

## Verification

- The previous HQ player fails the new replay test at its first resumed frame.
- NTSC and PAL generated square-wave cartridges pass 30-frame exact replay.
- Super Mario World and Castlevania III pass 90-frame exact replay after 240 and
  180 warm-up frames respectively, both in-process and in fresh relocated cores.
- Damaged headers/payloads, truncated files and invalid version/schema pairs reject without
  changing the state. The matching launcher's envelope checks pass under ASan
  and UBSan.
- An uninterrupted 180-frame Castlevania III comparison remains identical to the
  earlier corrected player in CPU/video/PCM; SIMD register preservation passes.
- Physical Castlevania III and Super Mario World tests each completed 1,800 frames
  with paused save/load, then 120 frames from a fresh player loading that state.
  All submitted PCM completed, with clean display, register/MMU/cache restoration
  and memory release. Fresh resumes had zero starvation. The first lifecycle
  runs each counted one intentional pause-to-silence transition as starvation.

The AHI worker now recognises user pause as an intentional drain and re-primes
its buffers on resume. Native mono/stereo tests exercise this alongside ordered
PCM delivery, state drains, fallback, cancellation and partial final batches.
The repeated hardware tests passed for both titles: **1,800 frames with pause/
save/load plus a 120-frame fresh resume**, zero starvation in all four runs, all
PCM completed, and clean restoration/free. The first resumed video/cycle endpoint
from each original physical checkpoint also matches the relocated ARM model.
This does not hide real playback starvation or claim a new synthesis speed gain.

[Measured records](../amiga/records/2026-10-30/nestopia-reference/hq-states/).
See [reproduction instructions](../development/nestopia-reference/README.md).


## Legacy replay checks

Super Mario World, Castlevania III and a PAL square-wave fixture load legacy
states with exact PCM/video/cycle replay against the quality-0 baseline. A fresh
relocated process reproduces the same result. Re-saving retains identical
legacy state bytes; switching back to an HQ checkpoint also replays exactly.
[Release evidence](../amiga/records/2026-10-30/audio-release-0.8.8/).
