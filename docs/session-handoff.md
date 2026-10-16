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
existing ROM paths and library/save files when upgrading. Only one Core1 owner;
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
with no library/player/Core1 owner. During backup review, three NES ROM filenames were corrected to retain `(E)`
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
Previous default and owner-accepted optimized binaries/launchers remain available.

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

SNES was added to `docs/nes-roadmap.md` at the owner's request: future core
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
unchanged. Mario Bros Optimized was left running for owner picture/sound testing;
the owner subsequently confirmed both are good (option 1, 10 October). This
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
backup was requested. The owner confirmed picture and sound work. Backup work
does not connect to the Amiga or alter that state. Check actual current screens
and Core1 ownership before any future launch; this note is a historical handoff.

Launchers: `Start-MarioBros`, `Start-SuperMarioWorld`, `Start-ZZFceux`.
Use `Execute` in Amiga Shell; the generic launcher opens the ROM requester.
ROMs are the owner's private files under `SD032G:Dev/ZZNesPlayer/ROMs` and are
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
World: 44.30 FPS. Audio gap counters remain in the logs; owner acceptance covers
Mario Bros' picture and sound, not general compatibility or full speed.

Next work: profile host scheduling, flip pacing and audio delivery without
weakening ownership, timeout, cancellation or cleanup checks. No 60 FPS claim.
The new standalone backup preserves the current work before further changes.


Final deployment: Fast launchers installed with executable/script protection;
installed `ZZFceux-fast` MD5 checked as `4398f22b8de76db50aad845a384b8749`, and
prior `ZZFceux-optimized` checked unchanged as `bf14d8e7dc20970d95fcd110cc9e6754`.
Mario Bros Fast was left running; fullscreen was confirmed after launch. On
10 October 2026, the owner selected option 1 and confirmed its picture and sound
are good. Acceptance covers this Mario Bros build, not SMW, measured latency,
exact A/V sync or 60 FPS. Q/Esc exits. Check live Core1 ownership before launching
another application. The temporary transfer server was stopped.


## ZZFceux 0.2.0-rc1 — profiling/input/release pass (10 October 2026)

Installed separately at `SD032G:Dev/ZZFceuxPlayer/Release-0.2.0-rc1/ZZFceux`,
275,216 bytes, MD5 `f0b62ec828adf96d0b905f8b9f3e6560`. Workbench drawer/tool
icons supply 65536-byte stack. Adjacent ROMs contains copies of the owner's
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
Core1. Final state Workbench only, owner port absent, Roadie/bridge/xSysInfo
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
both owner games (mapper0/90), exact PCM and bad-state rejection. A9 instruction
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
