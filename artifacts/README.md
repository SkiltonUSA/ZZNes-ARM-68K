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
