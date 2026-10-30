# 0.8.8 audio release validation

Legacy replay is exact against the quality-0 baseline in PCM/video/cycles,
including fresh relocated cores and re-saving. Switching to HQ restores HQ
history/phase. Unknown, damaged or mismatched states reject before mutation.

Both physical cartridges completed 1,800 frames with pause/save/load, 120-frame
HQ fresh-process resume and 120-frame legacy resume. All six runs report zero
starvation, complete PCM delivery and clean resource restoration/release.

The native worker (mono/stereo), AHI lifecycle mocks, release diagnostic guards,
current display/core tests and launcher state-envelope sanitizer checks pass.
The ZIP and signed offline installer pass member checksums, dependency recipe,
private-data exclusions, corruption rejection and executable byte equivalence.

ROMs, PCM and checkpoint contents are not included. Historical logs elsewhere
use redacted test paths; raw-log hashes refer to the private original captures.
