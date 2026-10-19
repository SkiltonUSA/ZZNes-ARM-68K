# ZZNES 0.7.4-dev cartridge update

Replace ZZNES and ZZFceux-ui together in an existing writable ZZNES drawer.
Keep the existing ROMs, states, library settings, icons and scanline tools.
This is a development pair, not a replacement for the tagged beta archive.

Adds CNROM/mapper 3 and mapper 78, plus duplicate-scan progress. Both supplied
Holy Diver and Cybernoid ROMs reached gameplay on the A4000TX. Save/load,
screenshot, display switching and cleanup passed; no FPS benchmark is claimed.

See ../../../docs/cartridge-compatibility-20261019.md and installed.json.
Source: development/mapper78-20261019 with the existing optimisation/scalable
launcher overlays. Build with make optimisation. Full upstream source import
is separate and does not enable additional boards in these binaries.
