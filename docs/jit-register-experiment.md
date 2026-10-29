# Register translation through the original switch — 0.8.2-dev

The experimental player generates ten A32 register handlers once and calls them
from the existing FCEUX opcode switch. It removes the per-instruction eligibility
classifier and per-guest-address cache lookup. Fetches, mapper hooks, cycle
accounting, audio hooks and interrupt checks retain their original order.
This is single-instruction translation, not a full JIT or a multi-instruction trace.

The 32 MiB executable reservation and 48 MiB owned runtime remain. Ten handlers
use 1,280 bytes of reserved slots; the old 2 MiB tag table is no longer linked.
The larger reservation does not establish a speed benefit. Local publication,
rewritten-code witness, runtime mapping and reset-before-free checks remain.

## Matched physical results

Two 300-frame Mario Bros. startup runs per variant, in reference/old/new/new/old/
reference order. Same ROM, window, audio and verification settings:

| Build | Mean ARM core time | Change |
| --- | ---: | --- |
| Interpreter | 1.715438 s | Reference |
| Previous address-lookup translator | 1.749432 s | 1.98% more core time |
| Original-switch translator | 1.707739 s | **2.38% less than old; 0.45% less than interpreter** |

All six runs match output `3bd96c26`, complete 159,725 PCM samples and pass
register/MMU/cache restoration, exit 0 and owned-memory release. Audio-gap
observations remain (9–14 per run). These are core-time measurements for one
startup workload, not gameplay FPS, audible-quality or broad compatibility claims.
The small difference from the interpreter does not justify changing the release.

## Validation and limits

- 20,480 linked-handler comparisons at two runtime addresses: all byte values,
  wrapping, NZ flags, TXS flag preservation and unchanged surrounding CPU state.
- 9,576 independent emitter cases and 16,384 allocation alignment checks.
- 600 linked interpreter/candidate frames match complete CPU state, cycles,
  video and PCM hashes; 24,721 generated-handler entries observed.
- Native presentation/library regression checks pass.
- A later 600-frame window run froze the Amiga before its log could be retrieved.
  It used the new switch translator with the original audio scheduling. No audio
  candidate had run. The machine was rebooted; the cause remains under investigation.
  After reboot, four 600-frame diagnostics passed: interpreter and candidate
  core-only, then interpreter and candidate with window/audio progress logging.
  Four further 600-frame audio comparisons also passed. This does not explain
  the original freeze or establish long-run stability.

Historical failures and measurements remain in
[the lookup report](jit-register-lookup-history.md). Installed players and release
packages are unchanged.

## Build

`make jit-registers` builds matching 0.8.2-dev launcher/player binaries in
`.context/jit-switch32-build`. `make test-jit-layout` checks that layout.
`scripts/test_nes_dispatch_core.py` exercises the linked handlers.
Use `scripts/test_console_jit_core.py --switch-dispatch` with explicit baseline,
candidate and a local ROM for full-core comparisons.

The separate `--audio-early` build switch wakes the existing AHI worker once a
three-frame batch is ready, before presentation. It retains the same ARM payload,
buffer sizes, prebuffer and pause/state/stop flush behavior. It remains opt-in: the matched windowed tests below show a presentation tradeoff. `scripts/test_audio_early.py`
checks actual producer copy/mute/wrap behavior and batch-ready notification.

[Run evidence](../amiga/records/2026-10-29/switch-dispatch/).

## Batch-ready audio comparison

Two 600-frame runs per variant, reference/candidate/candidate/reference order,
with byte-identical ARM payloads and the same window and verification settings.
Only the 68k audio notification point changes.

| Scheduling | Mean elapsed | Audio gaps per run | Presented frames per run |
| --- | ---: | --- | --- |
| Original | 20.457 s | 20 / 20 | 600 / 600 |
| Batch ready, before presentation | 20.254 s | 12 / 11 | 593 / 588 |

Both deliver all 319,450 PCM samples per run and exit cleanly with register/MMU/
cache restoration and owned-memory release. Core time is effectively unchanged.
The roughly 1% shorter elapsed time includes fewer presentations; it is not an
ARM-speed improvement. Earlier wakeups reduce observed gaps but pre-empt display
work on the 68k. Keep the normal release scheduling; fullscreen results below retain the
presentation tradeoff, and audible quality has not been checked.

[Audio and reboot diagnostics](../amiga/records/2026-10-29/audio-handoff/).

### Fullscreen follow-up

Same 600-frame, reference/candidate/candidate/reference comparison at 320×240,
with scanlines and the FPS overlay off:

| Scheduling | Mean elapsed | Audio gaps per run | Presented frames per run |
| --- | ---: | --- | --- |
| Original | 20.863 s | 66 / 77 | 554 / 549 |
| Batch ready, before presentation | 17.907 s | 56 / 50 | 490 / 504 |

Elapsed time is 14.17% lower, while mean presentations fall from 551.5 to 497.
The automatic presentation policy drops more frames as the 68k services audio
earlier. Core time remains 3.417 s and all PCM samples complete. All four runs
pass verification, restoration and clean exit. This is evidence of a scheduling
tradeoff, not a 14% faster ARM core or proof of smooth audio. It stays opt-in.

An initial controller check at 35 seconds occurred before teardown finished;
that run later exited cleanly. It is excluded from this repeated comparison,
which waits 55 seconds before checking completion.
