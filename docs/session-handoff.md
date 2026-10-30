## 0.8.3 Beta installed — 29 October 2026

Installed matching 0.8.3-dev launcher/player package in SD032G:Emulator/ZZNES
using the signed offline installer. Normal regional cadence, controls, snapshots,
save/load and window/fullscreen switching are retained. Automatic per-app AX AHI
output uses three immutable buffers and falls back to configured unit 0.
Includes limited register dispatch and a 32 MiB executable reserve; total owned
ZZ9000 allocation is 48 MiB, plus display and OS memory.

Builds, native audio tests, archive/signature checks and four physical player runs
across both emulators passed. Both installed launcher versions were visually
checked. Existing configurations remained byte-identical; ROMs and saves were
not changed. No global AHI, firmware or saved Workbench screenmode changes.
Core1 is idle, the bridge responds, and the private test drawer was removed.
The prior unexplained NES freeze and listening/long-session validation remain
open. Release functional checks are not new FPS measurements.

See [release validation](release-validation.md) and
[actions/evidence](../amiga/records/2026-10-29/ax-release/actions.md).
Private rollback files: workspace `.context/amiga/ax-release-1029/backup`.

## Whole ZZNES ROM directory audit — 19 October 2026

All 27 files in SD032G:Emulator/ZZNES/ROMs inventoried, source-copy MD5 matched
and launched on physical hardware with installed 0.7.4-dev player. 22 loaded:
13 games reached gameplay, one diagnostic ran, eight games reached only menus,
introductions or overworld in this audit. Do not call all 22 gameplay-verified.
Five originals rejected: Rockman3/4/5/7 each have a 524,304-byte whitespace
trailer; Lolo3 has MJR in reserved header bytes. Mac-only normalized copies
passed native run/state replay, but were not installed or hardware-tested.
All original attempts restored registers/cache witness and released owned RAM.
Final check: all 27 ROM MD5s and both installed executables unchanged; Core1
free. No ROM, save, settings or executable changes. See docs/rom-validation-20261019.md
and private .context/amiga/nes-validation-1019 receipts. No release/GitHub push.

## Cartridge compatibility and full-FCEUX staging — 19 October 2026

Installed matched 0.7.4-dev ZZNES/ZZFceux-ui with checksums; rollback copies are
in the installed drawer's Rollback-mapper1019. Library.cfg was byte-identical
through deployment. The launcher is reopened; no Core1 task remains after tests.

Mapper 3/CNROM and mapper 78/Holy Diver wiring now run the supplied games.
Exact DiskDude header recognition occurs in memory only. ROMs were not rewritten.
Native bank/bus/mirror/state tests, scrolling and relocated ARM presenter checks
passed. Both physical games reached gameplay and passed state, screenshot,
window/fullscreen and cleanup checks. Audio gaps are recorded, not hidden;
these runs are not performance measurements. A final 120-frame installed run
passed. See cartridge-compatibility-20261019.md and 19 October records.

The complete pinned FCEUX source is imported at development/fceux-full/vendor.
It has 219 iNES mapper registrations; 156/162 board files compile in the initial
ARM audit. This is source readiness, not full mapper or feature support.
Current executable gate: 0/1/2/3/4/5/78/90; still no battery, trainer or NES2.
Follow docs/fceux-integration.md for the accepted full-feature staged plan.
Do not enable the rest without metadata, allocation, persistence and state work.
Tagged releases and package ZIPs remain unchanged; the new matched pair is in
artifacts/development/cartridge-20261019. Earlier 0.7.3-dev packages are older.

## FPGA fullscreen / Soft window scanlines — 18 October 2026 UTC

Current installed development players use Xanxi FPGA controls in fullscreen,
Soft software filtering in a window. F7 cycles fullscreen modes / toggles window
Off/Soft. Alt+Return switches; normal exit disables global hardware scanlines.
No prior global mode is restored; no firmware capability readback exists.
Legacy Thin migrates to Soft. Controls/installer/source are bundled; the installer
adds missing tools and preserves existing SYS:Utilities/ZZScanlines or C: tools.
No firmware, startup or saved Workbench mode changes.

All three player host paths passed physical F7/pause/display-switch/readback/exit
checks with register/cache restoration. Optical acceptance of the FPGA effect
still requires the user or an HDMI capture. ARM payloads are unchanged. Installer
fresh/repeat/partial/existing-tool/error checks passed. Preferences and games are
untouched. Backups: Rollback-fpga-1018. Tagged releases remain unchanged.
[Report](fpga-scanlines-20261018.md) and
[installed hashes](../amiga/records/2026-10-18/fpga-scanlines/installed-build.json).

## F7 software scanlines — 18 October 2026 UTC

Installed the host/launcher update with F7 Off → Soft → Gradient → Classic → Off.
F7 is listed on the loading panel and controls page. Tested during play/pause,
window/fullscreen; SNES Thin exits with a surface resize. Key repeats ignored.
ARM payloads unchanged; session-only effect selection preserves saved defaults.
All physical tests returned exit0 with zero display faults and normal register/
cache witness restoration. Readback/interactive runs recorded audio gaps, so
these are functional checks, not speed or uninterrupted-audio claims.

Previous executables retained in Rollback-f7-1018 in each installed drawer.
ROMs, saves and library settings untouched; executable checksums verified.
See [report](scanline-key-20261018.md) and
[installed hashes](../amiga/records/2026-10-18/scanline-key/installed-build.json).
Versions remain 0.7.2-dev (NES) / 0.6.2-dev (SNES); tagged downloads unchanged.

## Display defaults and stability follow-up — 18 October 2026 UTC

Installed fullscreen/Soft defaults and the F9 Screenshot loading reminder.
Sharp remains the default pixel scaling; saved choices still take priority.
The player is unchanged from the optimisation commit. Extended NTSC/PAL ZIP
runs and repeated save/load/capture/display-switch/exit/resume passed. Visual
confirmation of the originally reported scrolling game remains outstanding.

See [follow-up report](stability-20261018.md) and
[build hashes](../amiga/records/2026-10-18/followup/tested-build.json).
Audio gap counts are retained; completion is not a claim of uninterrupted audio.
The earlier isolated SNES startup failure was not reproduced, not proven fixed.
Tagged releases are unchanged. Core1 is free and the library is closed after
checks; no firmware, global AHI or saved Workbench mode changes.

## Optimisation candidate — 18 October 2026 (UTC)

Installed and checksum-verified **0.7.2-dev**, with rollback copies of executables
and preferences. Tagged releases and default release rebuilds are unchanged.
See [measurements, failures and reproduction](optimisation-20261018.md) and
[tested binary/source hashes](../amiga/records/2026-10-18/optimisation/tested-build.json).

NES uses native palette caching, optional NEON table-lookup smoothing and
four-frame audio priming. The Display selector defaults to Sharp; existing
settings are preserved. Opening/saving the new launcher upgrades Library.cfg
to ZZNESUI4, so restore the backed-up config together with older executables.
The specific user-reported game scrolling issue awaits visual confirmation.

Both launchers opened and closed on hardware with library entries/settings
preserved. Final pause/save/load/snapshot/switch/exit and fresh-process resume
passed. The isolated early SNES interactive startup failure is retained in the
report; do not present this candidate as a tagged release or a universal FPS gain.
Core1 is free and the bridge/network remain running. No saved Workbench mode,
firmware or global AHI changes. Private receipts are in the workspace handoff.

## Red Launch and manual ROM scans — 16 October 2026

Launcher-only update installed in SD032G:Emulator/ZZNES/ZZNES.
MD5: `7b492fc035b9807ea95f235bd724a524` (213240 bytes).
The permanent bottom bar contains red Launch, Save settings and Quit.
Disks has a directory field, Browse requester and Scan once / Stop scan.
No startup, periodic or newly mounted-volume discovery remains. Legacy autoscan
preferences are ignored and saved as zero; the file format stays compatible.
Directory aliases are resolved before duplicate lookup. ROMs and players are
unchanged; the SNES Thin mode remains selected. Initial files/preferences are
retained in Rollback-launch-1016; the intermediate build is in Rollback-launch2-1016.
Published release assets have not been replaced.

Both pinned m68k builds, 20,000-entry and legacy-library sanitizer tests,
settings/presentation arithmetic tests, and explicit-scan sanitizer tests pass.
The scan tests cover idle inactivity, selected roots, recursion, aliases,
ZIP candidates, cancellation and DOS resource cleanup. Hash verification passes.

Physical UI checks: red Launch visible on Games and Display, Disks controls
visible, explicit ROM-directory scans complete without new duplicates. NES
Super Mario World (mapper 90) and SNES Aladdin launched from Display and returned
through F10 with Core1 released. The first SNES F10 was sent before the fullscreen
window appeared; waiting for its window and focusing it resolved the test.
The first scan test exposed a PROGDIR alias mismatch; fixed and regression-tested.
Only its 11 appended duplicate entries were removed, preserving the prior library.
No save-state or ROM deletion, player replacement or firmware changes.
Private evidence: workspace .context/amiga/launcher-controls/.

# ZZNES 0.7.1 Beta — EmuELEC border

Matching rebuilt launcher/player installed with checksums. Original files and
current settings retained in Rollback-border-1016. Preferences, ROMs, saves and
icon metadata retained. EmuELEC occupies existing theme ID 7, with a 9,632-byte
packed palette table. Allocation bounds and standard cartridge gate unchanged.

Native theme/geometry tests and relocated ARM presenter regression passed.
Physical ZIP session, pause/save/load/snapshot and display switching passed.
NES window focus needed a click before injected F10; exit then completed cleanly.
Current source/payload overlay: development/borders-20261016/.

---

# ZZNES 0.7.0 Beta — direct ZIP loading

Installed the new launcher/player pair with checksum checks. Existing Library.cfg,
Library.bak, ROMs, saves and icon metadata were retained. Previous executables
and settings are in the application drawer's Rollback-zip-1016 directory.
Only the 68k launcher/player changed; ARM payload bytes are unchanged.

Plain/ZIP bounded runs, invalid-CRC rejection, paused save/load/snapshot and MUI
launch/return passed on A4000TX. Native ZIP, large-library, scanner and relocated
presenter checks passed. See zip-validation.md for evidence and limitations.
Current launcher/host sources: development/zip-20261016/. Use make current and
make test-zip. Expanded SNES hardware remains a separate task, pending cartridge.

---

# Release 0.6.3 Beta

Packaged the blank-title-bar update with the colour logo. Standalone rebuild
passed. Exact title-bar behavior was checked on hardware before this version
bump; the new package itself has not been redeployed. The installed launcher
still reports 0.6.2 Beta with the same title-bar change. ARM/player unchanged.

---

# Title-bar cleanup — 16 October 2026

Current launcher source removes the window title text. Version remains in the
footer and About. The published logo beta ZIP remains unchanged; this is a
subsequent local/source update. Previous installed launcher and settings are
in Rollback-title-1016. Player, icons and libraries are unchanged.
Both builds passed; the physical windows have blank title bars and close cleanly.

---

# Colour logo update: ZZNES 0.6.2 Beta

Current launcher sources/artwork: development/logo-20261016/. New supplied
colour logo in the sidebar, startup/loading panels and Workbench icon.
Physical launcher appearance checked; icon.library colour-image round trip
and existing icon launch metadata checks passed. Standalone make current and
make verify-current passed. Player and ARM payload unchanged.

Installed with launcher/MakeIcon checksum checks and unchanged Library.cfg.
Previous files and icon retained in Rollback-logo-1016. Initial installed
library opening was slow; do not infer startup performance from this visual
update. The isolated empty-library launchers opened normally.

---

# Large-library update: ZZNES 0.6.1 Beta

Launcher-only update: dynamic library storage, path indexes and sorting.
No fixed ROM-count cap. Player binary/ARM payload unchanged. Source and prepared
launcher inputs: `development/library-20261016/`. `make test-library-large`
validates large collections and failure recovery. Physical 20,000-entry MUI
load/save and live-search checks passed; see the 16 October records.
Installed under the existing Emulator drawer with executable checksum checks.
Previous launcher and preferences retained in `Rollback-1016`; existing library
bytes were unchanged by installation. No player, ROM or save files replaced.

---

# Current beta: ZZNES 0.6.0

Current editable sources and exact build inputs: `development/beta-20261015/`.
Artifacts: `artifacts/beta-0.6.0/`. `make current-arm` rebuilds the complete
pair; `make test-current` runs native/model checks. Physical results are in
`amiga/records/2026-10-15/refresh/`. See `current-development.md` for the selected
optimisations and rejected alternatives. Native/model tests are not hardware proof.

The shared sidebar, mounted-drive discovery, asynchronous startup/loading panels,
window/fullscreen switching, FPS and software scanlines are enabled. Preserve
existing ROM paths and library/save files when upgrading. Only one Core1 task;
retain runtime mapping, cache witnesses and reset-before-free on every path.

Installed and checksum-verified on the A4000TX. Previous executables, icon and
library preferences are retained in `Rollback-1015` under the application drawer.
The installer preserved the existing library files; no original ROM/state files
were changed. Test ROM copies were used in a separate development drawer.

---

# Current Beta handoff — 12 October 2026

Current: ZZNES 0.5.0 Beta, `SD032G:Emulator/ZZNES/ZZNES`;
player `ZZFceux-ui`. Exact installed binaries in `artifacts/beta-0.5.0/`.
Current sources/build inputs in `development/beta-20261012/`. This supersedes
the installation and performance statements in the historical entries below.

See the main README for steady versus whole-loop frame rates, picture omission
and audio scheduling results. The installed Beta includes accepted cadence,
PAL handling, current MUI tabs, simplified About credits and per-game saves.
Both libraries were visually checked and closed cleanly after migration.
Old Dev folders are recovery copies; final observed machine state was Workbench,
with no library/player/Core1 task. During backup review, three NES ROM filenames were corrected to retain `(E)`
PAL tags; current settings and ROM bytes were preserved. No emulator was
launched and no new FPS measurement was performed. See the PAL path-fix record.

[Build/backup scope](beta-backup.md) and
[installed validation](../amiga/records/2026-10-12/emulator-beta/).

---

# Latest ARM presentation handoff — 10 October 2026

## Later 10 October: ARM pixel packing and pipeline experiments

Selected `--scheduling optimized-fast` build: 270,212 bytes, MD5
`4398f22b8de76db50aad845a384b8749`. Installed separately as
`SD032G:Dev/ZZFceuxPlayer/ZZFceux-fast`, with `Start-MarioBros-Fast`,
`Start-SuperMarioWorld-Fast` and requester `Start-ZZFceux-Fast` scripts.
Previous default and user-accepted optimized binaries/launchers remain available.

Specialised 32-bit palette stores reduce ARM presentation 3.32 -> 1.15 ms.
No emulator CPU/PPU/APU, audio batching, allocation/MMU/cache or firmware change.
300-frame startup runs: Mario 53.99 FPS, SMW 53.80 FPS. Mario's tiny difference
from 53.71 is within plausible noise. A Start-triggered 18,000-frame stability
run completed in 318.48 s, 56.52 FPS, all flips and 9,583,486 samples completed,
zero AHI errors and clean RET1/MMU/register/cache-witness/memory release. It is
not proof of continuous active gameplay, end-to-end audio synchronisation or
60 FPS. Native exhaustive pixels, actual audio worker, A9 presentation models
and standalone build/test checks passed. Standalone binary matches exactly.

Combined ARM command experiments passed correctness but were slower (50.02 /
47.99 FPS); moving pacing before flip queuing was also slower (52.98). These
remain explicit diagnostic modes. Fast keeps the accepted separate commands.
Do not launch `ZZFceux-pipeline*` or `ZZFceux-display-paced` as the selected build.
The prior accepted live session also ended cleanly: 37,191 frames / 677.5 s,
54.89 FPS, but inputs/pauses were not captured for a controlled comparison.

SNES was added to `docs/nes-roadmap.md` at the user's request: future core
feasibility benchmark first; no SNES implementation or performance claim.
Evidence: `amiga/records/2026-10-10/fceux-pipeline/`.

The following scheduling handoff is historical.

# Latest handoff — 10 October 2026

ZZFceux optimisation completed: fresh baseline 42.79/43.89 FPS (Mario Bros/SMW),
new candidate 53.71/51.92 FPS with audio and all frames displayed. Build with
`make player SCHEDULING=optimized`; default build remains baseline. Saved
candidate is `artifacts/fceux-player-optimized/ZZFceux`, 270,208 bytes, MD5
`bf14d8e7dc20970d95fcd110cc9e6754`. All changes are 68k scheduling/audio;
loaded ARM payload/relocations/entry are unchanged. See the 10 October
experiment record for failed variants, tests, timing limits and buffering cost.

Installed as `SD032G:Dev/ZZFceuxPlayer/ZZFceux-optimized` with separate
`Start-MarioBros-Optimized`, `Start-SuperMarioWorld-Optimized` and
`Start-ZZFceux-Optimized` launchers. Original default and its launchers are
unchanged. Mario Bros Optimized was left running for user picture/sound testing;
the user subsequently confirmed both are good (option 1, 10 October). This
does not establish SMW acceptance or measured latency. Q/Esc exits. Check live Core1 ownership and screens
before launching any other ARM application. Roadie, bridge and xSysInfo remain
present. Temporary transfer server was stopped. No global AHI/firmware changes.

Both ROM benchmark runs and a 432-frame interactive controls run returned
cleanly. Completed samples, native frame checks, flips and RET1/MMU/cache
witness/14-register restoration passed. Audio unit 0 remains Paula Fast 8-bit
mono / 8 kHz despite 32 kHz signed-16 input; Music Unit 255 selects ZZ9000AX but
is not used. Device is AHI 4.180 68060. No audible-gap or 60 FPS claim.

The earlier handoff below is retained as history, not current live state.

# NES development handoff — 9 October 2026

The latest working player is ZZFceux, installed at
`SD032G:Dev/ZZFceuxPlayer/ZZFceux` (265,660 bytes, MD5
`ce77a7b5fd6a453d50a9a697b86d3ae9`). Mario Bros was left running when this
backup was requested. The user confirmed picture and sound work. Backup work
does not connect to the Amiga or alter that state. Check actual current screens
and Core1 ownership before any future launch; this note is a historical handoff.

Launchers: `Start-MarioBros`, `Start-SuperMarioWorld`, `Start-ZZFceux`.
Use `Execute` in Amiga Shell; the generic launcher opens the ROM requester.
ROMs are the user's private files under `SD032G:Dev/ZZNesPlayer/ROMs` and are
not backed up here. Q/Escape exits, Return starts, arrows move, Z/X are A/B,
left Shift selects, P pauses and M mutes.

The target is A4000TX / TF4060 / AmigaOS 3.2.3 / ZZ9000 / XX19c / XACP 1.7.
AHI unit 0 uses Paula despite the physically installed ZZ9000AX. No global AHI,
firmware, network, Roadie or AmigaBridge changes were made for the new player.
Core1 must be exclusive, including stock Xanxi applications that may not publish
our `Sixies.ARM.Debug.Owner` port. That legacy identifier remains unchanged
because it is part of runtime coordination, not repository branding.

Original Mesen ZZNes remains installed at `SD032G:Dev/ZZNesPlayer/ZZNes`,
420,832 bytes, MD5 `d54d086434df49e7f5ece528316a6f29`. Current Mesen sources
contain the later DOS Process audio experiment (0.3.3-dev), which builds the
426,584-byte candidate with MD5 `d5a4bd29ff0a6158a777a8e8312d9785` in the
original workspace. It is not the installed default. The preceding failed
Exec Task experiment caused a Guru and is retained only as historical evidence;
its failed executable is excluded from this backup.

Both final ZZFceux 300-frame tests passed sampled native comparisons, full
first-frame readback, all-frame flips, completed audio, RET1/MMU/register/cache
witness checks and memory release. Mario Bros: 44.19 FPS; mapper-90 Super Mario
World: 44.30 FPS. Audio gap counters remain in the logs; user acceptance covers
Mario Bros' picture and sound, not general compatibility or full speed.

Next work: profile host scheduling, flip pacing and audio delivery without
weakening ownership, timeout, cancellation or cleanup checks. No 60 FPS claim.
The new standalone backup preserves the current work before further changes.


Final deployment: Fast launchers installed with executable/script protection;
installed `ZZFceux-fast` MD5 checked as `4398f22b8de76db50aad845a384b8749`, and
prior `ZZFceux-optimized` checked unchanged as `bf14d8e7dc20970d95fcd110cc9e6754`.
Mario Bros Fast was left running; fullscreen was confirmed after launch. On
10 October 2026, the user selected option 1 and confirmed its picture and sound
are good. Acceptance covers this Mario Bros build, not SMW, measured latency,
exact A/V sync or 60 FPS. Q/Esc exits. Check live Core1 ownership before launching
another application. The temporary transfer server was stopped.


## ZZFceux 0.2.0-rc1 — profiling/input/release pass (10 October 2026)

Installed separately at `SD032G:Dev/ZZFceuxPlayer/Release-0.2.0-rc1/ZZFceux`,
275,216 bytes, MD5 `f0b62ec828adf96d0b905f8b9f3e6560`. Workbench drawer/tool
icons supply 65536-byte stack. Adjacent ROMs contains copies of the user's
two cartridges and an original Controller-Test.nes; no commercial ROM goes
in the GitHub release. Old fast/optimized checksums unchanged.

Mario scripted Start: 1800 frames, 55.47 FPS, 31 native hashes/cycles and all
958349 samples; SMW startup 300 frames 54.26 FPS; original tone fixture 300
VERIFY frames, six full framebuffer checks. Flips/RET1/MMU/registers/cache
witness/release passed. Flip-only pacing brought no gain; accepted pacing
retained. New per-stage histograms and lowlevel port-1 joystick support.
Physical controller mapping remains unconfirmed (UNKNOWN/no button input).

AX cafe0000/cafe0001 AHI allocation/free verified without playback or preference
changes. Player still AHI unit 0 / Paula; AX streaming needs a separate backend.
No direct Core1-to-AX interface assumed. Workbench icon -> Start -> ASL requester
-> original fixture -> fullscreen -> Q worked; requester Cancel also released
Core1. Final state Workbench only, coordination port absent, Roadie/bridge/xSysInfo
and ZZTemperature present. No crash/reboot.

Evidence: `amiga/records/2026-10-10/fceux-release/`. Standalone native/ARM model
tests pass and generated executable is byte-identical to the deployed binary.

Published prerelease `v0.2.0-rc1` at
https://github.com/SkiltonUSA/ZZNes-ARM-68K/releases/tag/v0.2.0-rc1 .
ZIP, executable, corresponding source, ReadMe and checksums uploaded; all five
GitHub asset SHA-256 digests and sizes matched local files. Release source
commit `ff6d481b33a00bf313b6a7034661f853e7028a4f`. Temporary transfer server
55031 stopped after installation; Amiga left at Workbench, no Core1 app active.


## ZZNes MUI Library candidate — 10 October 2026

Installed separately at `SD032G:Dev/ZZFceuxPlayer/Library-0.3/`:
`ZZNesLibrary` MD5 `571d796cb818a426f1b99f48b192f619` and `ZZFceux-ui`
MD5 `e056592277459fdf784c1f4c1fefe388` (293,048 bytes). Icon stack 65536.
The 0.2.0-rc1/fast/optimized executables and existing ROM files remain unchanged.
Native MUI 3.8 tabs follow xSysInfo; Library.cfg/.bak holds history/favourites
and display/input settings. ROM entries point to the previous release's drawer.
No firmware, AHI, Roadie or startup settings changed.

Opt-in build `--scheduling release-ui`. Five private FCEUX save-state slots
per ROM path, F5 save/F8 load, Resume slot into a fresh process, .bak retention.
Physical original-cartridge save/load, overwrite, cold resume and paused
save/load passed, with clean ARM/bitmap/AHI teardown. Cold resume also matches
native cycles and pixel hashes at three sampled frames. Native replay includes
both user games (mapper0/90), exact PCM and bad-state rejection. A9 instruction
model and standalone native tests passed; independent build binaries identical.

Display keeps 4:3 on either 4:3 or 16:9 monitors (monitor set to fill), masks
0/8/16 source pixels on each axis, and offers five original procedural borders.
Final Mario 300-frame startup validation: 47.74 FPS including first readback
and audio drain, ARM presentation 2.266 ms. Not a controlled performance gain
or 60 FPS claim. See records for the intrusive 26.25 FPS VERIFY run and the
initial, safely cleaned-up audio-drain failure that was fixed.

The user selected 'test joystick later'. Physical directions/fire and final
visual/audio acceptance remain pending. Controller tab is a read-only live
lowlevel port-1 test; idle type was UNKNOWN, not a confirmed failure.
The library is left open on Workbench; no Core1 app remains active. Check
live ownership before any subsequent ARM launch. Temporary transfer server
55031 stopped after deployment. Package remains a development candidate,
not a new GitHub release. Evidence: `amiga/records/2026-10-10/nes-library/`.

## ROM Manager and package-manager pilot — 18 October 2026

Current development launcher adds ROM Manager (bulk recursive import, confirmed
duplicate-entry cleanup, verified save/battery/snapshot backups) and read-only
ZZ9000 temperature beside the version. Duplicate matching compares decoded ROM
bytes; first entry retained, favourite/history merged; no ROM/save deletion.
Native sanitizers and 20,000-entry tests passed. Both physical launcher fixtures
removed three duplicates (raw copy, ZIP copy, canonical alias), retained one
different and one missing entry, imported two nested ROMs, and verified all five
backup files. Fixture ROM/save bytes remained identical. NES confirmation Cancel
left Library.cfg byte-identical. Temperature displayed 58.0 C alongside the
separate sensor monitor; independent ONCE sample was 57.7 C later in the session.

Installed launcher 245,856 bytes, SHA256
`bce562be14ee2406f295a8322d7e1af0e499f65b769ef71926bd3136a4377a00`. Previous launcher and Library.cfg are in the local
Rollback-manager-1018 drawer. Deployment preserved live Library.cfg byte-for-byte.
ARM players and firmware unchanged; no game launches in this UI test. Actual
USB media backup was not exercised; mounted paths use normal AmigaDOS I/O.

The amipkg package builder bundles Xanxi tools and automatically runs the
install-missing helper. Physical isolated amipkg pilot passed with the local
0.7.11-zztest1 recipe-origin fix; stock 0.7.11 fails custom-repo recipes. See
docs/package-manager.md. No public feed or new tagged release was created.


## Scalable launcher — 19 October 2026

Installed ZZNES 0.7.3-dev, 253608 bytes, SHA256
`6d41231b310aab9ca645ba77a8687a862adf3bd53ee16d5ea7acb9f137f5f6c6`. Previous launcher and Library.cfg retained in
Rollback-layout-1019 inside the existing emulator drawer. Config checksums match
before/after replacement and startup. Players, ROMs, saves and firmware unchanged.
Launcher reopened; no Core1 player active.

All seven pages, scroll bounds, loading cards and actual window resizes passed
with 640×480 / 800×600 / 1024×768 budgets on the existing physical desktop.
No actual Workbench resolution change. Initial remembered-size regression fixed
by first-open clamp and retested larger-to-smaller on both launchers.
Sources: development/scalable-launcher-20261019. Artifacts, screenshots,
layout logs and complete development ZIP: artifacts/development/scalable-launcher-20261019.
Published beta tags unchanged. See docs/scalable-launcher.md.


## Duplicate-scan progress — 19 October 2026

Installed launcher-only follow-up in SD032G:Emulator/ZZNES; same development
version. Source overlay now includes library_manager.h. Rollback-scan1019 holds
previous executable/settings. Live Library.cfg preserved; launchers reopened.
Progress panel 310x122 passed a compact 640x480 budget test on the current
Workbench, filename-before-read, cancellation/restart and cleanup. SNES ZIPs
read successfully; NES probe exercised unreadable handling. No actual mode change
or game execution. See artifacts/development/duplicate-splash-20261019.
SHA256 ae705ec668c54cded3d575e38e9c91f85660aa0066536874c9241d60a8aa93d1; 256384 bytes. Published packages unchanged.


## 0.7.4 Beta distribution — 19 October 2026

Packaged the recorded 0.7.4-dev executables without changes, with the full offline
amipkg installer and manual ZIP. README/features/specifications and user guide
now describe the current build. Dependency helper checks MUI/P96/AHI/ZZ9000 and
closed launcher/Core1 ownership; no automatic system-library or firmware changes.
Signed archive/member/executable checks passed; see docs/release-validation.md.
No hardware install or launch was performed during this packaging task. Existing
installed state is unchanged. Source and release assets are prepared for GitHub.

## Controlled scheduling follow-up — 29 October 2026

All 16 fixed-presentation console tests pass (660 frames each, 60 warmup/600
measured, ABBA order per console/mode). No repeatable earlier-audio advantage;
keep original defaults. Earlier VERIFY/snapshot-heavy elapsed times were not
normal-play performance. See fixed-presentation.md and its raw records.
No installed player, ROM, save, firmware or saved display preference changed.
The previously reported NES freeze remains unexplained.

## Fullscreen ACK polling — 29 October 2026

Optional --ack-poll-us 250 reduces pending ACK reads by about 90%, but the
counter-free NES/SNES pairs show no useful frame-rate or audio gain. Release
defaults stay unchanged. Existing lock/ACK/timeout/reset rules remain intact.
Twenty physical runs complete cleanly; 16 accepted comparison logs are archived
(the first four NES profiling logs were overwritten by a harness naming error,
then repeated). Native actual-host mocks pass retirement and cancellation cases.
See ack-polling.md for phase/blocking details and the next conversion-overlap
investigation. Private SD test drawer removed; bridge up, Core1 idle, saved
screenmode CRC 9C80FBC5 unchanged. Installed players and user data untouched.

## Pixel conversion overlap — 29 October 2026

Added isolated --presentation-test serial/overlap builds. Old PAN ACKs retain a
render pin; after conversion the host drains, unlocks for input, then relocks and
rejects relocation before queuing the next flip. PCM stays before PRESENT, with
full-ring waits still unlocked. Original ARM image/MMU/audio/ACK contracts remain.

Native fault/lock/audio and existing pixel/SIMD checks pass; both fresh full builds
pass. Two 120-frame hardware readback runs, eight 660-frame ABBA timing runs and
two readiness-gated UI lifecycle checks pass. Two earlier NES UI attempts sent
input too soon but exited cleanly; logs retained. 14 physical runs total.
Mean 600-frame time is 2.64% longer NES / 1.46% longer SNES. No promotion.
See conversion-overlap.md and its raw records; late audio links remain nonzero.
Installed players/releases unchanged. Private test drawer removed; Core1 idle,
bridge alive, saved screenmode CRC 9C80FBC5 unchanged. Earlier NES freeze remains
unexplained. Local MCP remains running.

## AHI servicing and bitmap locks — 29 October 2026

Added --host-service-test profile/batch4, requiring --presentation-test serial
and the register-experiment build. Histogram costs are elapsed calls, not task
CPU usage; do not add overlapping worker/main-task intervals. Mean per 600
frames: NES SendIO 1896 ms, lock/unlock 643 ms, worker copy 51 ms; SNES 1652/465/81.
Six profiling runs, four accepted (initial SNES copy instrumentation missed the
stereo expression, then was corrected and repeated).

Read-only AHI discovery: ENV unit 0 mode 0002000c = Paula Fast 8-bit mono at
8000 Hz. Music unit 255 mode cafe0001 = ZZ9000AX 16-bit stereo at 32000 Hz. Both
players open device unit 0; their input PCM remains NES 32000 mono/SNES 32040 stereo.
No global preferences changed. Next candidate: per-app AX output backend, with
unit 0 fallback; not implemented or benchmarked in this round.

Four-frame batching (six-frame prebuffer, NES 8 KiB / SNES 16 KiB AHI buffers) passes
actual-worker sanitizer tests including state/short flushes. Eight ABBA runs
show mean frame time +1.07% NES/+0.57% SNES; no default promotion. Both candidates
pass readiness-gated pause/window/fullscreen/quit checks. All 16 runs finish PCM,
restore state and release owned memory. Fresh full builds and input equivalence
checks pass. See host-service-profiling.md and raw records.

Removed SD032G:Dev/ZZCost1029; Core1 idle, bridge alive, MCP left running. Saved
screenmode CRC 9C80FBC5 and live AHI preferences CRC 725CE7DB unchanged. Installed
players/releases and ROM/save libraries untouched. Earlier NES freeze unresolved.

## Per-application AX audio — 29 October 2026

Added isolated --ax-audio-test, requiring --presentation-test serial and the
register experiment, incompatible with host-service/batch4/earlier-audio/ACK
variants. Low-level AHI mode discovery selects registered ZZ9000AX16-bit stereo;
allocation failure uses original unit0. No global prefs changes. Same source PCM
and 3-frame batches, but three immutable dynamic buffers plus silence; IRQ hook
only retires/schedules/signals. Bounded indices, worker-only copies and synchronous
controller teardown before memory/signal release. SNES feedback adjusts to active
backend capacity. Release players and installed applications stay unchanged.

Native queue/actual-worker/API-adapter sanitizer tests pass, including fault and
state/short-drain cases. Four silent physical probes (initial two-buffer then
improved three-buffer, mono/stereo) complete96000frames each. Two exploratory
120-frame runs pass; final code is tested in eight matched660-frame ABBA runs
and two save/load/pause/window/fullscreen/quit lifecycles. All12 player runs complete
PCM and restore/release owned ARM resources. Earlier NES freeze remains unresolved.

Mean600-frame time: NES10.492331->10.1625435s, FPS57.1846->59.0403 (+3.245%);
SNES10.6325635->10.1691615s, FPS56.4304->59.0019 (+4.557%). This changes output
configuration AND scheduling; do not attribute all gain to one component or sum
with previous results. Short tests, no listening/latency or long-run-quality claim.
AX silence schedules NES14/16 and SNES8/13 include startup/end; incomparable to
unit0 late-link counts. Normal release defaults unchanged, no package promotion.

Fresh full builds pass and match host/backend and recorded ARM/MMU inputs; current
native/model checks pass after restoring LLVM PATH. See docs/ax-audio.md and raw
records. Private SD032G:Dev/ZZAX1029 removed; Core1 idle, bridge alive, live AHI
CRC725CE7DB and saved screenmodeCRC9C80FBC5 unchanged. Firmware, startup, installed
players, libraries/saves and global preferences untouched. Local MCP left running.
Next gate: listened longer sessions and comparison against unit0 already set toAX.

## Paula audio routing fix — 29 October 2026

ZZNES 0.8.4-dev restores configured AHI unit 0 (Paula on this machine).
Automatic AX routing caused silence at the connected RCA output. ARM payload
unchanged; native generated-worker tests and 180-frame physical routing/cleanup
check pass. Installed in SD032G:Emulator/ZZNES. ROMs/saves/settings and global
AHI unchanged. Listening confirmation pending. Source build flag remains
`--release-ax` for compatibility; only `--ax-audio-test` selects AX directly.
See amiga/records/2026-10-29/paula-routing. Published release unchanged.

## Audio scheduling and integer windows — 29 October 2026

Installed ZZNES 0.8.5-dev in SD032G:Emulator/ZZNES, matching launcher/player hashes
in docs/release-build.json. Older executable siblings retained as .pre-window;
prior .before-paula backups retained too. Library/Controls/Session checksums
unchanged. Live AHI CRC725CE7DB, saved screenmode CRC9C80FBC5 unchanged. Existing
open launchers still need reopening to use the new display choices.

Configured AHI unit 0 remains the output (Paula here). Batch-ready notification,
NES six-frame startup prebuffer and SNES short-stall recovery reduce late links
in matched 1x runs (NES14->7, SNES94->16 over two1800-frame runs per variant).
Listening confirmation remains pending. New 2x/3x windows render on ARM into
owned P96 bitmaps; no repeated blit when a picture is omitted. Larger windows
use bounded presentation omission (2x up to3,3x up to5), never skip CPU/APU work.
Final600-frame normal-detail 2x/3x runs on both emulators have zero late links.
No general FPS/audio-quality guarantee. Pause/snapshot/save/load/3x-fullscreen-3x
and clean teardown pass. Native sanitizers, relocated pixel/guard/cancellation
checks, four physical VERIFY frames per size and compact MUI checks pass.

SNES hires3 initially exceeded50ms PRESENT deadline. Coordinate caching outside
the pixel loop now passes all relocated pixel checks and360physical frames with
capture/cleanup, but still81late audio links: not audio-qualified. Keep normal
detail for smooth3x audio. Normalize hires/window captures once; saved pixels
match native snapshot tests. See docs/audio-window.md and raw records/actions.

Chrono Trigger horizontal tear is reported in fullscreen with core options0;
new window scaling is not active. On/off FPGA scanline1800-frame comparisons
finish with zero late links, clean first-frame verification and restoration.
No visible tear-free confirmation. Firmware PAN ACK is not a physical scanout
fence. Earlier blanking-gate variants timed out and remain withdrawn; no firmware
or Workbench mode change. See ZZSNES docs/chrono-trigger-display.md. Published
release assets remain unchanged; these are installed development builds.

## Output quality release — 30 October 2026

Installed ZZNES 0.8.6-dev through the signed offline installer in
SD032G:Emulator/ZZNES. Release tag v0.8.6-beta; source/build hashes and asset
checksums are in docs/release-build.json and docs/release-validation.md.
Same-disk executable/icon rollback copies use .pre-quality; previous backups
remain. Original library/session data and ROMs/saves are unchanged. Launcher
open/quit creates Audio.cfg with Auto (0); other absent optional settings stay
absent. Both installed launchers were closed normally after checking them.

Auto detects configured Paula unit 0 and requests per-app uncalibrated 14-bit
stereo at 22.05 kHz (actual 22030 here). Configured AHI, Paula 28 kHz and explicit
AX are selectable in Display. Nine-frame prime, twelve producer slots, three
immutable callback buffers; source PCM unchanged. Capture drains at an idle,
unlocked frame boundary and re-primes: a deliberate pause, not continuous sound.

Native/relocated pixel tests and physical PAL/NTSC/output/window/lifecycle runs
are recorded in amiga/records/2026-10-30/output-quality. Zero starvation in
steady comparison runs does not establish listening acceptance; pause/switch
stress includes shortages. See docs/output-quality.md for upstream comparisons.
SNES preserves all 224/239 rows and corrects high-detail row alignment; the exact
Chrono Trigger scrolling scene still needs a visual check. Heavy Stunt Race FX
race audio remains below real time with the tested frameskip choices.

Global AHI CRC725CE7DB and saved screenmode CRC9C80FBC5 are unchanged. Core1 is
idle and the bridge responds. An early standalone AHI Probe failed before device
open and was suspended; corrected query ordering is tested. Reboot once before
normal use to clear the suspended Probe. Private SD032G:Dev/ZZQuality1030 staging
is retained until that reboot; do not treat it as an installed app or publish its
ROM/state contents. No firmware or startup changes.

## Native columns — 30 October 2026

Installed 0.8.7-dev launcher/player in SD032G:Emulator/ZZNES. Native columns
selected by changing only the final scaling field of Library.cfg to 2. Original
executables, Library.cfg and Version.txt retained as .pre-columns siblings;
private evidence under .context/amiga/nes-columns-1030 in the parent workspace.
Build hashes in docs/native-columns-build.json. Published 0.8.6 Beta unchanged.
256 columns map one-to-one, centred in320 with32-pixel side borders;240rows
unchanged. Existing edge masks remain. Sharp/Smooth retain old aspect scaling.
Native/model tests and two180-frame four-readback hardware checks pass. Two600-frame
normal Super Mario World runs (fullscreen/3x) complete all PCM, zero starvation,
register/MMU/cache restoration and owned-memory release. VERIFY readback runs
intentionally stall audio and are not performance comparisons. Physical compact
MUI accepts allthree scaling choices. Exact reported scrolling appearance still
needs confirmation. Global AHI/screenmode unchanged; no SNES runtime changes.

## Release packaging — 30 October 2026

ZZNES 0.8.7 Beta packages refreshed with ZIP, signed offline amipkg installer,
build receipt and SHA256SUMS. See docs/release-validation.md. No additional
hardware changes during packaging. Native-column binaries match the installed tested build; scrolling visual confirmation remains pending.
