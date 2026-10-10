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
Core1 must be exclusive, including stock XANI applications that may not publish
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
