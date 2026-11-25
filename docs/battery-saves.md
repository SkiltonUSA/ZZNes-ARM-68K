# Cartridge battery saves

ZZNES 0.8.11 Beta supports battery RAM on accepted iNES mapper 1 (MMC1),
4 (MMC3) and 5 (MMC5) cartridges. The mapper must expose one persistent region
of at most 32 KiB. Other battery boards, NES 2.0 and UNIF remain rejected.
The existing ROM-size, mirroring and header constraints still apply; nonzero
iNES byte 8 is not accepted. This does not enable every MMC1/MMC3/MMC5 board.

## Using saves

Keep the ROM directory writable. A cartridge's saved RAM loads automatically
before its first frame. On clean exit, changed RAM is written beside the ROM:
`Game.nes.sav`, or `Game.zip.sav` when launching a ZIP. These are raw mapper RAM,
not save states. Unchanged RAM does not trigger another write.

Save states retain their existing format and include mapper RAM. Loading an
older state rolls that RAM back; a later clean exit can therefore update the
battery file to the restored state. Moving or renaming a ROM outside the launcher
requires moving its associated save files too.

ROM Manager's backup and confirmed deletion cover battery sidecars. Existing
settings and game files are preserved during installation.

## Interrupted or invalid saves

The player writes `.sav.tmp`, closes it and verifies its full contents before
rotating the old `.sav` to `.sav.bak`. If the final rename fails, it attempts to
restore the old file. If the main file is missing but a complete backup exists,
the next launch recovers that backup and recommits it on clean exit.

A wrong-sized/unreadable main save or a lone unfinished temporary file stops
launch and retains the files. Close the emulator and back up those files before
repairing or replacing a damaged save. A valid primary file takes precedence.

This is application-level replacement and recovery, not a journaled filesystem
or an autosave during gameplay. A reset or power loss can lose the current
session and filesystem caching still applies.

## Implementation

The FCEUX mapper supplies `CartInfo.SaveGame[0]` and `SaveGameLen[0]`; no RAM
address is guessed. Core1 exports/imports it through the existing bounded shared
save buffer, with host cache synchronization. Fresh cartridges retain initialized
mapper RAM. After importing an existing save, trainer bytes are reapplied to match
FCEUX's battery-load-before-power/trainer ordering.

MMC1/MMC3 fixtures exercise 8 KiB and MMC5 exercises 32 KiB. Single-region mapper
variants are selected by the pinned core; multiple persistent regions are refused.
Audio synthesis, guest CPU timing and the save-state schema are unchanged.

[Tests and build identities](validation/battery-save/README.md).
