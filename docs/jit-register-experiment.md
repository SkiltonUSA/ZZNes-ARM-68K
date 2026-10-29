# Experimental register translation — 0.8.0-dev

The released interpreter remains the default. This experiment reserves an **8 MiB
executable cache** in a **16 MiB Exec-owned allocation** on ZZ9000 Core1.
It is a small A32 register translator, not a complete CPU JIT.

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
stack/shared regions remain non-executable. The allocated cache capacity exceeds
the tiny amount of code used by this initial experiment.

## Verification

- 9,576 Cortex-A9 instruction-model cases: 8/16-bit arithmetic, flag representation
  and unchanged surrounding state.
- 16,384 allocation alignments: cache bounds, executable pages and table capacity.
- 180 linked interpreter/JIT frames: matching Mario Bros. video and PCM output.
- Physical 300-frame run: matching output, exit 0 and owned-memory release.
- Original register-loop fixture: matching complete CPU structure and cycle counts.

Build separately with `make jit-registers` using the existing cross-toolchain
setup. Outputs go to `.context/jit-registers-build`; normal artifacts are retained.
Launcher/player versions both read 0.8.0-dev for this candidate. It is not a
release package. The shared emitter test is `tests/amiga/test_console_jit.py`;
full-core comparisons use `scripts/test_console_jit_core.py` with explicit
`--baseline`, `--candidate`, `--baseline-packer`, plus a local ROM.
ROM data is not included in the evidence.

[Build hashes and physical logs](../amiga/records/2026-10-28/jit-registers/).
