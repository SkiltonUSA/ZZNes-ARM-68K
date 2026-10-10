# Saved Amiga executables

These are exact cached artifacts from the development workspace. They are not
fresh standalone builds. Check `SHA256SUMS` from the repository root using
`shasum -a 256 -c artifacts/SHA256SUMS`. Original build manifests and historical
logs retain their original filenames and paths.

| Directory | Status |
| --- | --- |
| `fceux-player/` | Latest installed ZZFceux; physical 300-frame runs and owner-confirmed Mario Bros picture/sound. |
| `fceux-bench/` | Headless FCEUX hardware benchmark; does not open a game screen or play audio. |
| `mesen-installed-baseline/` | Saved original installed ZZNes 0.3.2-dev baseline; predates the source snapshot's audio Process changes. |
| `mesen-audio-process-candidate/` | Later Mesen 0.3.3-dev experiment; not the default installed player. |

The failed Exec Task binary that caused a Guru is deliberately omitted. Its
failure records remain in `amiga/records/2026-10-09/mesen-audio-task/`.
This snapshot contains the current sources, not an exact checkout of every
historical baseline. Do not assume a current Mesen build reproduces the older
installed baseline. The main README identifies the recommended saved FCEUX
candidate for continued development.

FCEUX startup scripts retain owner-specific volume and ROM paths. ROM files
are excluded. The source license and runtime notices are in the repository
root, vendored directories and `licenses/`. Keep them with redistributed copies.


## 10 October scheduling candidate

`fceux-player-optimized/ZZFceux` is the separately installed candidate:
270,208 bytes, MD5 `bf14d8e7dc20970d95fcd110cc9e6754`. Copy to the Amiga under
name `ZZFceux-optimized` for the supplied launchers. Sources build with
`--scheduling optimized` (alias `deadline-cadence3`). It is not the baseline.
Mario Bros / SMW startup tests: 53.71 / 51.92 displayed FPS with AHI;
owner confirmed optimised Mario Bros picture and sound are good. SMW and
measured latency remain separately unconfirmed. See 10 October records. The original
`fceux-player/` executable and source-provenance snapshot remain preserved.
