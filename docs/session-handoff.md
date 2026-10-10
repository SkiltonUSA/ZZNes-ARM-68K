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
acceptance remains pending. Q/Esc exits. Check live Core1 ownership and screens
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
