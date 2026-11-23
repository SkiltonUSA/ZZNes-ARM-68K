# ZZNES 0.8.9 Beta

Application/launcher version: **0.8.9-dev**. AmiPkg version: **0.8.9-dev**.

## Changes

- Rebuild the launcher with the next numbered release; remove the dated package suffix.
- Include Settings → ZZOverclock, with 666.7 MHz and experimental 800 MHz controls.
- Retain the recorded emulator players and their build identifiers. This release does not rebuild or relabel those cores.
- Update the main README and linked feature documentation.

Includes the compact launcher, ROM padding handling, 22.05 kHz Paula default and clock-aware player. Native core synthesis and legacy save-state support are retained.

## Installation and compatibility

Extract the LHA, open its drawer and double-click Install. Choose a writable
destination and close emulators before updating. Dependency checks and existing
settings/saves are preserved. Clock control requires the optional ABI 3 firmware
service; its absence disables clock controls only. The clock affects the whole
board. No firmware is installed and no clock change happens automatically.
Use suitable cooling for 800 MHz; temperature preflight is not a continuous
thermal watchdog. No new performance gain is claimed here.

## Verification

All launchers were cross-compiled into separate release directories. Recorded
player hashes are retained. Installer signatures, payload hashes, extraction,
component references and application version strings are checked before publication.
Prior hardware evidence remains separate from these package checks.

## Archive documentation refresh

Installers and component LHAs include readme.txt copied from the main README,
about.txt with credits and licence.txt. Existing component notices are retained.
This documentation-only refresh leaves executable hashes and application
versions unchanged.

## Cartridge documentation correction

The README and roadmap now distinguish the eight enabled mapper IDs from
future trainer, battery and NES 2.0 integration. Save-state support does not
imply battery-cartridge support. See [current support](current-cartridge-support.md).
Installer documents are refreshed; executable hashes and versions are unchanged.
