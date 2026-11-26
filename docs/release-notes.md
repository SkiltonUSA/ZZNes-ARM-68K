# ZZNES 0.8.12 Beta

Application/launcher and AmiPkg version: **0.8.12-dev**.

- Bounded NES 2.0 header, region, RAM and submapper support.
- UNIF import for selected boards, including stored/deflated ZIPs. Originals
  remain unchanged; unknown boards and malformed files are refused.
- Add AxROM (7), Color Dreams (11) and GxROM (66).
- Preserve legacy saves, trainer handling and mapper 1/4/5 battery persistence.
- No change to audio synthesis, clock settings or firmware.

[Supported formats and limits](cartridge-formats.md) ·
[Validation](../validation/cartridge-candidate/README.md).

## Installation

Extract the LHA and open Install. Choose a writable destination. Close the
emulator before updating; settings, ROMs and saves are preserved. Dependency
checks are retained. MUI is required; audio follows the configured Paula/AHI
choice. Clock controls require the optional service; emulation does not.
The installer and component archives include the main README, credits and licence.
