# Mesen NES presentation performance, 9 October 2026

Four sequential 120-frame physical A4000TX runs of the same original NROM demo.
`legacy`, `host`, `fast` retain per-frame 68k index checksums; `direct` moves colour
conversion to ARM and checks full bitmap snapshots at frames 1/60/120 instead.
Do not describe the overall gain as an isolated one-variable benchmark.

Run `python3 scripts/analyze_mesen_performance.py` to regenerate `results.json`.
Raw logs include frame hashes, cycle counts, timings, restoration and exit status.
`direct6.log` is the prerequisite short physical check. Native/model logs and
build manifests record validation and binary identities. `direct-transfer.json`
records CRC transfer and matching native Amiga MD5. `final-state.txt` verifies
Roadie/bridge, Core1 ownership absence and the unchanged installed preview MD5.
Local workspace/home paths in regression/build logs are normalized.

Source review/attribution: `amiga/mesen_nes/zzpicodrive-review.md`.
Implementation, measured gains, validation-policy differences and memory contract:
`amiga/mesen_nes/README.md`. No firmware changes, screenshot capture or publication.
