# Current NES cartridge support

This describes the retained player packaged with **0.8.9 Beta**, not the entire
imported FCEUX source tree. The executable identity is recorded in
[the installer manifest](installer-refresh-inputs.json).

| Item | Current behaviour |
| --- | --- |
| Header | Bounded iNES; PAL/NTSC detection and exact legacy DiskDude signature handling |
| Mapper IDs | 0, 1, 2, 3, 4, 5, 78, 90; additional board-specific size/mirroring limits apply |
| PRG / CHR | Up to 512 KiB PRG and 256 KiB CHR; power-of-two sizing; CHR RAM only where the mapper gate permits |
| Battery flag / trainer | Rejected by the cartridge gate; importing mapper source does not enable battery persistence |
| NES 2.0 / UNIF / other mappers | Not accepted by the current loader |
| Four-screen flag | Rejected except mapper 78, which uses it for the legacy board distinction |
| Save states | Supported for accepted cartridges; this is separate from battery-backed cartridge support |
| ZIP / padded ROMs | Supported within the existing cartridge contract; [trailing-padding handling](rom-padding.md) never adds mapper support |

The current build prepares its cartridge gate from
`development/mapper78-20261019/common/cartridge.h` through
`scripts/build_current.py`. The older standalone probe under
`amiga/fceux_player` has a narrower gate and does not describe this release.

Holy Diver and Cybernoid have [recorded gameplay checks](cartridge-compatibility-20261019.md).
A supported header does not establish compatibility with every game or board
variant. Broader cartridge integration remains [planned work](fceux-integration.md).
Generic ROM-manager backup/delete code can handle existing battery-save files;
that does not enable battery-flagged cartridges in this player.
