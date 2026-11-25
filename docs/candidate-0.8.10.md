# ZZNES 0.8.10 Beta candidate

Built and tested locally; not yet published or installed as the default.
Final physical installation and clean-exit validation are pending after a bridge
screenshot timeout. The current public release remains unchanged.

The release build enables iNES trainers on the eight supported mapper IDs.
Trainer bytes are loaded at $7000–$71FF using the pinned FCEUX power-on behaviour;
PRG/CHR offsets, ROM identity and archive loading account for the 512-byte prefix.
Original input files remain unchanged. Battery cartridges, NES 2.0 and UNIF are
still rejected. This does not add mapper IDs or promise every modified game works.

Native sanitizer tests cover all eight mapper fixtures and raw/stored/deflated ZIP
loading. The exact candidate ARM payload passes trainer execution and HQ
video/audio save-state replay at two relocations. Prior candidate physical tests
cover twenty save/load and fresh-process runs. Actual modified trainer-bearing
commercial games remain unavailable; those compatibility claims are not made.

Both launcher and player are rebuilt with matching versions. Fresh output hashes
are recorded after success, stale snapshot manifests are excluded, and the
measured 666/800 MHz timer policy is retained. No firmware or clock is changed.

[Recorded candidate checks](validation/release-0.8.10/README.md).
