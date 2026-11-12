# NES trailing-padding compatibility

The launcher automatically handles supported iNES cartridges with trailing spaces,
CR or LF bytes. Add or import the original `.nes` file or a ZIP containing one
ROM, then Launch normally. No manual repair is needed.

The iNES header must describe a supported cartridge. Only bytes **after** its
complete PRG/CHR data may be ignored, and every extra byte must be space, CR or
LF. Truncated data, unsupported headers/mappers, other trailers and damaged ZIP
checksums are still rejected. Input is bounded to 2 MiB, including decompressed
ZIP data; the player's cartridge limits remain unchanged.

Original files are never rewritten. Padded cartridges use a verified temporary
copy in the application's `Cache` drawer. It is removed after the player returns;
after an interrupted session it may remain until replaced by the next padded
launch. The library retains the original path. Save-state paths remain tied to
the original entry, while cartridge/snapshot hashes use the clean data. PAL
filename hints are retained. The released emulation player is unchanged.

Identification and duplicate comparison use the same normalized data. This is
file-format recovery, not new mapper support or proof of gameplay compatibility.
