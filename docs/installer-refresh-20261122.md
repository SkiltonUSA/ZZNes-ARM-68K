# ZZNES — installer refresh, 22 November 2026

Package revision: **0.8.8-dev.20261122**. Application version: **0.8.8-dev**.
The package revision identifies this collection of recorded binaries; it does
not relabel or rebuild their embedded application versions.

## Included changes

Includes the compact launcher, ROM padding handling, 22.05 kHz Paula default and clock-aware player. Native core synthesis and legacy save-state support are retained.

Settings includes **ZZOverclock: 666.7 MHz / 800 MHz (experimental)**, with Apply
and Refresh. Keep the bundled ZZClock beside the launcher. Opening the app or
launching a game does not change the clock. The setting affects the whole board.
Clock control requires the optional ABI 3 firmware service; standard XACP users
can still run the emulator at the standard speed. Missing service disables only
clock control. No firmware is installed by this package.

Use suitable cooling for 800 MHz. The temperature preflight is not a continuous
thermal watchdog. No additional FPS or audio-quality gain is claimed by this
installer refresh.

## Installation

Extract the LHA, open its drawer and double-click Install. Select a writable
destination and close emulators before updating. Existing library settings,
saves and user media are preserved by the existing installer recipes. Dependency
checks remain in place; missing system software is reported, not silently replaced.
Existing audio preferences are preserved; new defaults apply to fresh settings.

## Validation

Replacement executables are checked against recorded build/install hashes.
Catalogue signatures, every nested payload hash and complete LHA extraction
round-trips are verified. These are packaging checks, not a new full-game test
or a fresh physical installation. Earlier hardware evidence is retained in the
project. Some audio gaps and experimental-model limitations remain.
