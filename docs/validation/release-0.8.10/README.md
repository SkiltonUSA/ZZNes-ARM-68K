# 0.8.10 release validation

Native sanitizer checks and exact candidate ARM trainer/state tests pass. Eight
mapper fixtures run at two relocation addresses. Ten states saved on the Amiga
with the prior candidate load in this build and match the physical fresh-resume
cycles/video hash. Super Mario World and Castlevania III cover non-trainer states.
These checks do not establish listening acceptance or every modified game.

The signed AmiPkg candidate passes archive round-trip, signature, version, exact
README/credits/licence and replacement-hash checks. Final-build physical cleanup checks pass as recorded below. No ROMs/states are included.

See native.txt, arm.txt, physical-state-model.txt and build.json for results.

## Final candidate hardware checks

Ten fresh-process saved-state loads cover all eight trainer mappers, Super Mario World and Castlevania III, alternating fullscreen/windowed output.

Each run verifies normal return, register/cache-witness restoration and owned-memory release. See [results](hardware/summary.json); audio queue counts remain recorded, including failures to sustain delivery. These are not full-game or listening claims. Hardware retained 800 MHz KEEP.

## Installer and installed-player checks

Fresh and repeat signed AmiPkg installs pass dependency checks, archive signatures,
binary hashes and exact README matching. The production update preserves the
recorded library, audio and controller settings; ROMs and saves are not replaced.
The installed player completes a 120-frame Castlevania III HQ state resume in a window
with zero starvation/device errors and clean register/cache/memory teardown.
See [installation records](installation/) and [installed-player log](hardware/installed-nes-cv3.log).
Core1 is idle and Core0 AGA inactive; KEEP 800 MHz is unchanged.
Listening acceptance was deferred by request. These short checks do not establish
long-session or every-game audio quality. Package receipts describe archive-build
validation; the physical installation evidence is recorded separately here.
