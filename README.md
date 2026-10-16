# ZZNES — 0.6.3 Beta

<img src="docs/screenshots/logo.png" width="160" alt="ZZNES logo">

A native **MUI** game library for **AmigaOS and ZZ9000**, using **FCEUX / FCE Ultra**
and **[Xanxi’s XACP platform](https://github.com/Xanxi-Amiga/XACP-ZZ9000)**.
The Cortex-A9 runs emulation and fullscreen rendering. The 68k handles AmigaOS,
files, controls, display coordination and batched AHI audio.

**[Download 0.6.3 Beta](https://github.com/SkiltonUSA/ZZNes-ARM-68K/releases/tag/v0.6.3-beta)** ·
[User guide](docs/current-guide.md) · [Changes](CHANGELOG.md) ·
[Build and measurements](docs/current-development.md) · [Interface gallery](docs/current-interface.md)

![ZZNES interface](docs/screenshots/interface.png)

## Features

- ZZDosBox-style sidebar: Games, Display, Controllers, Save states and About.
- Colour logo, Workbench icon, startup panel and loading panel with controls.
- Add ROMs or folders; search, favourites, recent games and captured artwork.
- Rename titles and delete games with confirmation.
- Automatic ROM discovery on mounted Workbench volumes, including USB storage.
- No fixed ROM-count limit; tested with 20,000 entries per library.
- Fullscreen or Workbench window; **Alt+Return** switches during play.
- Optional FPS overlay and **Classic, Soft or Gradient** software scanlines.
- Monitor aspect correction, borders, overscan masks and joystick testing.
- Five save slots per game; save, load, resume and delete.
- Guarded NEON stores and scanline dimming, with an integer fallback.

## Requirements

- **ZZ9000** with compatible **XACP firmware**; tested on **XX19c / XACP 1.7**.
- **Picasso96**, **AHI**, and **MUI 3.8 or compatible**, installed separately.
- A writable application drawer and your own ROMs.
- AmigaOS and a Zorro III Amiga; host executables target the **68020 instruction set**.

**A TF4060 or 68060 accelerator is not required.** The ZZ9000 Cortex-A9 runs
the emulation. A faster 68k helps file access, input, window updates and AHI
audio servicing; it does not increase the ARM clock speed.

**Tested configuration:** A4000TX, TF4060/68060, AmigaOS 3.2.3.
The 68020 build target is not a measured minimum-speed guarantee. These builds
have not yet been validated on a 68030, and the published FPS results apply
to the tested configuration.

The NES core reserves 4 MiB of ZZ9000 RAM, plus display and OS allocations.
Only one Core1 application can run at a time.

## Performance

The established steady emulation measurements remain:

| Game / emulator | Steady emulation FPS |
| --- | ---: |
| Contra — ZZNES | **59.893** |
| Super Mario World — ZZSNES | **59.920** |

Repeated 600-frame comparisons measured **12.3% less ARM presentation time**
with scanlines off, and **33.8% less with Soft scanlines**.
These are presentation-stage savings, not equivalent increases in game FPS.
[Method, raw logs and limitations](docs/current-development.md).

![ZZNES running in a Workbench window](docs/screenshots/window.png)

## Compatibility and credits

Automatic PAL/NTSC timing and mapper 0/1/2/4/5/90 support, subject to
[cartridge restrictions](docs/amiga-zznes-pal-compatibility.md).
Audio: 32 kHz mono through AHI.

Development: **Codex assisted, Amiga-Bridge MCP**. Interface: **MUI**.
Thanks to **Xanxi** for XACP, and the **FCEUX / FCE Ultra** contributors for the core.
The software scanline effects and NEON presentation work are shared with ZZDosBox;
they do not require the separate ZZ9000 scanline application or an FPGA change.

Component licences and notices are included. The FCEUX core is GPL-2.0-or-later.
