# Full FCEUX integration

The target is the full FCEUX feature set, delivered in stages through ZZNES's
Amiga MUI interface. This is ongoing work, not a claim that the current player
has desktop FCEUX feature parity.

The complete source for our existing FCEUX lineage is now imported under
`development/fceux-full/vendor`, including its licence and desktop frontend
reference code. It is pinned to Rezzy-dev/fceux commit
`4d01530b6689b06a6d7cf0679b63625e3270ae9a`, not the latest desktop release.
`development/fceux-full/upstream.json` records every file hash and all **219
registered iNES mapper IDs**, with their initializer and source file. Separate
UNIF board names are also present in the source; 219 is not a count of every
board or a promise of compatibility.

## Stages

| Stage | Deliverable | Acceptance |
| --- | --- | --- |
| 1. Existing cartridge fixes | CNROM/mapper 3, mapper 78 board variants, legacy-header recognition | Real bank/mirroring/bus-conflict tests; supplied games; states; hardware cleanup |
| 2. Complete cartridge layer | Full mapper registry; iNES/NES 2.0 and UNIF metadata; trainer and four-screen handling; PRG/CHR RAM and battery persistence; expansion audio | Bounded allocations, mapper fixtures and representative games for each board family; no silent fallback to NROM |
| 3. Other systems and input | FDS with user-supplied BIOS and writable disk overlays; NSF playback; VS/other supported system modes; additional controllers | Per-format loading, persistence and input tests; performance measured on A9 |
| 4. Player tools | Cheats and Game Genie, speed controls, frame advance, rewind, recording/replay and capture options | Deterministic replay; stable saves; clear MUI controls |
| 5. Developer tools | Memory/PPU/name-table viewers, disassembly, breakpoints, tracing, RAM search and watch, code/data logging | Cooperative ARM pause/read/resume without unowned DDR access; tools disabled during normal play |
| 6. Advanced tools and parity audit | Lua scripting, TAS editing, netplay, remaining upstream options and file-format interoperability | Separate runtime/dependency review; end-to-end tests; explicit status for every upstream feature |

The MUI launcher, Workbench/window display path, XACP Core1 ownership and AHI
handoff remain the platform layer. Qt, Win32 and SDL frontend source is retained
as reference, not linked into the Amiga application.

## Cartridge audit

The initial Cortex-A9 translation-unit audit compiles **156 of 162 board source
files** using the current platform declarations. Compilation does not establish
linking, mapper registration, memory safety, audio correctness or gameplay.
Nothing is enabled automatically by this audit.

The six remaining files expose concrete integration work:

- `datalatch.cpp`, `fk23c.cpp`, `unrom512.cpp`: the upstream iNES header imports
  host C/C++ library dependencies. FK23C also needs ROM-database parameters;
  UNROM512 needs cartridge size and persistent flash data.
- `ks7016.cpp`: missing `u16` platform typedef.
- `mmc1.cpp`: a missing semicolon in the pinned upstream source. The existing
  port already corrects this in its prepared MMC1 source.
- `rt-01.cpp`: libc `rand()` used for simulated weak ROM bits. A replacement
  must have explicit saved RNG state for deterministic replay.

Before enabling the remaining boards, replace the current 128 KiB mapper arena,
64-entry state registration table and 120 KiB state envelope with a measured,
bounded layout and versioned state format. Audit mapper allocation failure paths:
many upstream initializers assume allocation succeeds. The current 4 MiB Core1
allocation and fixed control/MMU regions must not be enlarged by guessing at
free ZZ9000 memory. Continue to allocate through Exec and verify mappings.

Battery-backed and trainer cartridges remain rejected by the current candidate;
the imported source does not change that. Existing save files must remain intact
when the new state implementation is introduced. Region, submapper and board
wiring must be passed into the mapper, not inferred from its numeric ID alone.

## Reproduce

```sh
# Import exact git objects from a local upstream checkout (one-time source update).
python3 scripts/prepare_fceux_full.py --upstream /path/to/fceux
make verify-fceux-full
python3 scripts/audit_fceux_boards.py
make test-mapper78
make optimisation
```

The audit writes `.context/fceux-full/audit.json`. It does not deploy or launch
anything. Normal beta builds remain separate from the development candidate.

References: [FCEUX project](https://github.com/TASEmulators/fceux),
[FCEUX feature documentation](https://fceux.com/web/help/Introduction.html),
[pinned source lineage](https://github.com/Rezzy-dev/fceux/tree/4d01530b6689b06a6d7cf0679b63625e3270ae9a).
