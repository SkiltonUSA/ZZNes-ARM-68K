ZZNes Library 0.3.0 development candidate
======================================

Double-click ZZNesLibrary to open the native MUI interface.
Requires AmigaOS 3.x, MUI 3.8, ZZ9000 XX19c / XACP 1.7 and the
existing 320x240 32-bit RTG screen mode used by ZZFceux.
Keep ZZFceux-ui beside ZZNesLibrary. The supplied icon sets a 64K stack.
Close other ZZ9000 ARM applications before playing.

LIBRARY
Add ROM selects a .nes file. Add folder imports .nes files directly inside
the selected folder (not subfolders). Up to 128 files. Toggle favourite
marks a game with *. The top filter selects all, recently played or favourites.
Removing a game from the list does not delete its file or saved states.
Play starts a new game; Resume slot loads the selected saved game.
Q or Escape returns to the library. The library hides while a game runs.

DISPLAY
Choose your monitor's physical shape: 4:3 or 16:9 widescreen. The game keeps
a 4:3 shape. Set the monitor to fill its panel; if it already adds 4:3 side
bars, choose 4:3 in the app to avoid adding a second set of bars.
Left/right and top/bottom masks independently hide 0, 8 or 16 NES pixels per
edge without zooming. Default: 8 left/right, none top/bottom.
Choose black, white, console grey/red, cream/burgundy or starfield borders.
These are original procedural designs, not a CRT shader or Nintendo art pack.

CONTROLLERS
The live test reads the physical Amiga joystick port 2 (lowlevel port 1).
Move the stick or press fire to allow automatic type detection.
A standard C64 stick has one button: choose Fire = A or Fire = B.
Keyboard: arrows = directions; Z = A; X = B; Enter = Start;
left Shift = Select; P = pause; M = mute; Q/Escape = quit.
A supported multi-button controller also maps blue to the other face button,
green to Select and Play to Start. The mouse port is not reconfigured.

SAVE SLOTS
Choose one of five slots before playing. F5 saves that slot, F8 restores it.
Saving replaces that slot but keeps the previous file with a .bak suffix.
Save operations also work while paused. Resume slot starts a new process
from the saved state. The tab shows each slot's date and size after exit.
The date is the Amiga's own clock, not a network timestamp.
States live in States/, keyed by the ROM's library path. Moving/renaming a
ROM gives it a different slot set; the internal header also checks ROM content.
Private .zzs format: only this state ABI and ROM. Desktop Mesen .mst and
FCEUX .fcs states are not supported. These are game snapshots, not battery saves.

SUPPORTED CORE
This fast player runs pinned FCEUX on Cortex-A9 Core1, not Mesen.
Currently NTSC iNES mapper 0 and mapper 90, CHR ROM only; no battery, trainer
or four-screen cartridges. ZIP and SNES files are not supported.
AHI unit 0 supplies sound. No firmware or global AHI preferences are changed.
The earlier accepted player remains a separate installation.

FILES
Library.cfg: settings, favourites and play history; Library.bak: prior copy.
Session.cfg: settings for the current launch. Last-session.log: diagnostics.
States/: five snapshots per ROM path. Keep this drawer writable.
Only the original Controller-Test cartridge is included; supply your own games.

CREDITS
Native MUI structure based on xSysInfo (BSD-2-Clause, LICENSE-xSysInfo).
Emulation: Rezzy-dev/fceux, pinned 4d01530b6689b06a6d7cf0679b63625e3270ae9a,
GPL-2.0-or-later. Integration: GPL-3.0-or-later.
XANI's XACP-ZZ9000 platform and fullscreen/PAN examples made this possible.
See overscan.md for the requested Mesen-S #122 discussion and its credited
comparison images. Those are SNES reference screenshots, not bundled bezels.

Source: https://github.com/SkiltonUSA/ZZNes-ARM-68K
