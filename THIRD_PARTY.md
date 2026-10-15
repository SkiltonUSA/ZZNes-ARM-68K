# Third-party notices

Our launcher, adapters and integration are GPL-3.0-or-later; see LICENSE.
Selected upstream sources retain their notices and exact pinned hashes:

| Component | Provenance and license |
| --- | --- |
| FCEUX | `amiga/fceux_bench/vendor/upstream.json`; GPL-2.0-or-later, `vendor/COPYING` |
| Mesen CPU | `amiga/mesen_bench/vendor/upstream.json`; GPL-3.0-or-later, `vendor/LICENSE` |
| Mesen PPU and player | `amiga/mesen_nes/vendor/upstream.json` and `vendor/player/upstream.json`; upstream Mesen license |
| blip_buf | Shay Green; notices in `amiga/mesen_nes/vendor/player/blip_buf.*`, `COPYING.LGPL` |

Xanxi's XACP firmware interfaces and ZZPicoDrive fullscreen example informed the
launcher and display work. No firmware or PicoDrive source is distributed here.
Upstream source files are adapted reproducibly by build scripts; generated
patches accompany the recorded builds.

68k executables link the pinned amigadev/crosstools toolchain's libnix C runtime
and Amiga stubs. They do not need external ixemul.library or libnix4.library.
Credit to Matthias Fleischer, Gunther Nikl, Stefan "Bebbo" Franke and contributors;
the [AmigaPorts libnix project](https://github.com/AmigaPorts/libnix) describes
libnix as public domain. The toolchain container digest is in `amiga/upstream.json`.
GCC runtime support is covered by GPLv3 with the GCC Runtime Library Exception
3.1; see LICENSE and `licenses/COPYING.RUNTIME`.

The standalone builds omit the AmigaBridge client. AmigaOS, P96, AHI, firmware,
ROMs and game data are not supplied. Any downloaded public test fixtures stay
in the ignored build directory and retain their upstream provenance manifests.

Native MUI library patterns adapted from SkiltonUSA/xSysInfo (upstream xsysinfo
contributors, BSD-2-Clause); notice in `amiga/fceux_player/LICENSE-xSysInfo`.
The overscan guide links klepp0906's Mesen-S #122 screenshots with attribution;
they are not packaged as player wallpaper. Built-in border designs are original.
