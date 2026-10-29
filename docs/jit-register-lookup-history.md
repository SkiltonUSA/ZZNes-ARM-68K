# Experimental register translation — 0.8.1-dev

The released interpreter remains the default. This candidate reserves a **32 MiB
executable cache** in a **48 MiB Exec-owned allocation** on ZZ9000 Core1.
It is a small A32 register translator, not a complete CPU JIT. There are 262,144
128-byte code slots plus 2 MiB of tag metadata. Cache bounds are shared by the
emitter and MMU; page-table storage is enlarged and the witness is relocated.

The previous 8 MiB build and its evidence remain available. The measurements
below describe that older build, not the new 32 MiB candidate.

## Earlier 8 MiB measurements

A physical 300-frame comparison completed with matching output and clean
MMU/register/cache restoration. Core time was 1,714,667 us for the interpreter
and 1,747,987 us for the candidate: **1.94% slower**. This is not a speed
improvement, so the candidate has not replaced the installed player or release.
Wall time includes presentation and verification work and is not a CPU benchmark.

The translator handles register transfers and X/Y increment/decrement.
Everything else falls back to the interpreter. Each instruction returns to the
original scheduler, preserving opcode reads, cycles, audio and interrupt/event
boundaries. Auxiliary cartridge processors are unchanged. Multi-instruction
traces are future work and require event-timing comparisons before use.

Cache lookup validates the current opcode and CPU width. Register values are
loaded at execution time; no guest memory values are cached. Generated code uses
ARMv7 UBFX for wrapping. There are no arbitrary 32-bit constants in these small
fragments, so adding MOVW/MOVT would add no benefit. The existing core cycle table
already provides precomputed timing; variable event costs must remain intact.

Code publication cleans local L1 data lines, invalidates local instruction lines
and synchronizes execution. It never changes shared L2. A rewritten-code witness
runs before guest execution. Only fully owned code-cache pages are executable;
stack/shared regions remain non-executable. The NES key remains a 16-bit program address, so this translator currently
uses only the first 65,536 slots (8 MiB). The full 32 MiB region is reserved
and executable for future translation work; increasing it does not add hits.
The allocated cache capacity exceeds
the tiny amount of code used by this initial experiment.

## Earlier verification

- 9,576 Cortex-A9 instruction-model cases: 8/16-bit arithmetic, flag representation
  and unchanged surrounding state.
- 16,384 allocation alignments: cache bounds, executable pages and table capacity.
- 180 linked interpreter/JIT frames: matching Mario Bros. video and PCM output.
- Physical 300-frame run: matching output, exit 0 and owned-memory release.
- Original register-loop fixture: matching complete CPU structure and cycle counts.

Build separately with `make jit-registers` using the existing cross-toolchain
setup. Outputs go to `.context/jit-registers32-build`; normal artifacts are retained.
Launcher/player versions both read 0.8.1-dev for this candidate. It is not a
release package. The shared emitter test is `tests/amiga/test_console_jit.py`;
full-core comparisons use `scripts/test_console_jit_core.py` with explicit
`--baseline`, `--candidate`, `--baseline-packer`, plus a local ROM.
ROM data is not included in the evidence.

[Build hashes and physical logs](../amiga/records/2026-10-28/jit-registers/).

## 32 MiB revision — 29 October 2026

The final launcher/player build passes the native regressions, 9,576 emitter
cases, all 16,384 MMU alignment cases and a 180-frame linked interpreter
comparison. The layout test also checks witness separation from video, audio,
ROM, saves, control memory and actual page tables.

A physical 300-frame run used a 50,331,648-byte owned allocation, matched the
reference output hash, completed audio delivery and restored registers/cache
with witness_bad=0 and launcher exit 0. Nine audio-gap observations remain;
this is a lifecycle check, not a gap-free audio or performance claim.
Core time was 1,746,801 us. No new speed improvement is established.

Build and test evidence is recorded separately from the earlier measurements.
[32 MiB records](../amiga/records/2026-10-29/jit-registers32/).
