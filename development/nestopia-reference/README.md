# Offline Nestopia audio reference

This harness compares the pinned Nestopia JG 2.0.0 core with an existing ZZNES
ARM payload. It does not install or launch anything on the Amiga. Supply your
own ROMs; keep captures and register traces outside the tracked source tree.

Source: https://gitlab.com/jgemu/nestopia
Commit: `27246144887c78154584515f530c61497e92cd05`.
Upstream licensing and notices remain in that checkout. The harness uses the
core API directly; Qt and the JG frontend are not needed.

```sh
python3 development/nestopia-reference/build.py /path/to/nestopia /tmp/nst-build
/tmp/nst-build/capture /path/to/game.nes /tmp/nst-capture 1200 48000 1 0
```

Arguments after the output prefix are frames, sample rate, output-filter enable
and DMC-pop-reducer enable. Output is signed-16 little-endian mono PCM, CSV frame
counts/video hashes, and PPM snapshots every 300 frames. NTSC and no input are
fixed for this investigation. The core's output count is respected; missing
samples are not fabricated to fill a nominal frame buffer.

For APU writes, build in a separate output directory with `--trace` and run with
`NESTOPIA_APU_TRACE=1`. Instrumentation is added to a generated copy of NstApu.cpp;
the pinned checkout must remain unchanged. Verify traced/untraced PCM equality
before using the trace. Frames numbered zero are initialization writes.

`capture_arm.py ROM BUILD OUTPUT_PREFIX --frames 1200` uses the existing
Unicorn environment and LLVM nm. It captures the ARM payload's PCM and APU
writes and checks that the signed-16 adapter output equals the core output.
This is an instruction model, not a cache-coherence or hardware-speed test.

`compare.py CAPTURE_DIRECTORY EARLIER_AMIGA_WAV RESULT_JSON` reproduces the
recorded comparison. Its input filenames correspond to the experiments in
[the report](../../docs/audio-synthesis.md#nestopia-reference-and-transfer-diagnosis).
It checks the matching register-write prefix, filter/control video equality,
trace invariance and stale samples in the earlier physical recording.

To test the isolated shared-PCM mapping:

```sh
python3 scripts/build_current.py --release-ax --audio-core-quality 1 \
  --audio-fir-neon --audio-word-clear --audio-square-spans --audio-shared-uncached
c++ -std=c++14 -DMB_ALLOCATION=0x3000000u -DCJ_BEGIN=0x600000 \
  -I.context/audio-core-q1-build-neon-clear-spans-shared-pcm/core \
  development/nestopia-reference/test_audio_pages.cpp -o /tmp/test-audio-pages
/tmp/test-audio-pages
```

Use the generated **core** headers: core/mmu.c includes its local mmu.h and
mmu_plan.h. Editing only the historical player copy does not change its map.
The tested candidate remains separate from the installed release.


## HQ states

Add `--audio-hq-states` to the build command above. The matching player and
launcher are emitted under the same build drawer with a `-states` suffix.
Legacy quality-0 states retain their original synthesis mode; see [the format](../../docs/audio-states.md).

```sh
MODEL_PYTHON development/nestopia-reference/test_hq_states.py BUILD \
  --rom /private/game.nes --warmup 240 --frames 90 --output /tmp/replay.json \
  --state /tmp/private-state.zzs
clang -std=c99 -Wall -Wextra -Werror -Wno-unused-function \
  -fsanitize=address,undefined -IBUILD/library \
  development/nestopia-reference/test_state_envelope.c -o /tmp/state-envelope
/tmp/state-envelope /tmp/private-state.zzs
python3 development/output-quality-20261030/test_worker.py
```

Replace `MODEL_PYTHON` with the Unicorn environment's Python and `BUILD` with the
candidate drawer. Omit `--rom` to use a generated square-wave NROM; add `--pal`
to exercise PAL resampling. Replay tests compare every PCM sample and video/
cycle endpoint, including a fresh allocation base. They also reject corrupt,
truncated and invalid version/schema combinations before mutation. State files contain private game
state: keep them outside the tracked tree.


`test_legacy_states.py OLD_Q0_BUILD NEW_BUILD --rom /private/game.nes` verifies
legacy PCM/video/cycles, fresh-process loads, unchanged re-saves and switching
back to HQ. Add `--pal` for PAL or omit `--rom` for generated test data. The
release uses these same routines through `scripts/build_current.py --release-ax`.
