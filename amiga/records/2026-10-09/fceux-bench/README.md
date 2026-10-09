# FCEUX A9 core benchmark, 9 October 2026

See [experiment, results and limitations](../../../fceux_bench/README.md).
No ROMs included. Hardware logs are unedited fetched Amiga output; native logs
are Mac executions of the isolated FCEUX harness. `*-arm-model.log` validates
ARM instructions, not real cache behavior. `mario300.json` / `smw300.json`
come from `scripts/analyze_fceux_bench.py`, which compares every hardware frame
with native FCEUX and requires successful mapping, RET1, MMU/register/witness
restoration and released memory before reporting speed.

The 186,344-byte executable is independently MD5-verified on the Amiga.
Its final rebuild is byte-identical to the tested binary. `build.json` identifies
source hashes and binary SHA-256; `upstream.json` identifies unchanged vendored
sources. `integration.patch` records generated changes. Sanitizers exclude
biased-pointer array-bounds/pointer-overflow checks; ASan still checks actual
accesses. Neither model/native consistency nor hashes prove NES accuracy.

Prior Mesen timings: sibling `mario-bros/` and
`mesen-audio-task/audio-baseline300.log`. Compare ARM core timings, not
FCEUX headless throughput against Mesen displayed FPS.
