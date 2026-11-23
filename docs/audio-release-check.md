# Released-player audio check

The released player was tested unchanged on the A4000TX at the standing
800 MHz clock. These checks use a private profile: 2× window, software Soft
scanlines, Paula HiFi at 22.05 kHz (actual mixer 22,030 Hz), and 1,200 frames
from reset with no input. Installed settings and saves were unchanged.

| Game | Elapsed | Audio starvation events | PCM frames completed |
| --- | ---: | ---: | ---: |
| Castlevania III | 20.824 s | 0 | 638,940 |

All submitted PCM completed, with no device error. Register/MMU/cache witnesses
and allocation release passed. The 35 scheduled silence buffers in the
non-starving runs include startup/shutdown handling; they are not 35 underruns.
These are short delivery checks, not listening acceptance, complete gameplay
coverage or a performance comparison against older releases.

[Player hash and extracted counters](audio-release-check.json). ROMs, saves
and captured game audio are not included.
