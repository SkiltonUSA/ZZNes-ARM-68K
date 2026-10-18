# Display defaults and follow-up checks

The 0.7.2-dev candidate starts with **Fullscreen**, **Soft software scanlines**
and **Sharp pixels**. Smooth scrolling remains optional. The loading panel now
labels **F9 — Screenshot** explicitly. Existing saved choices still load normally;
the installed library was changed to the requested fullscreen/Soft settings
without removing its entries. This does not replace the tagged release.

The player is unchanged from the [optimisation candidate](optimisation-20261018.md).
Only the launcher/defaults changed. Native library checks cover fresh defaults,
20,000 entries and retaining an explicitly saved windowed/scanlines-off choice.

## Physical follow-up

| Run | Emulated frames | Elapsed seconds | Audio gap events |
| --- | ---: | ---: | ---: |
| Super Mario World, first capture | 3,000 | 51.054 | 14 |
| Super Mario World, existing capture | 3,000 | 50.838 | 0 |
| Asterix, PAL ZIP | 3,000 | 61.143 | 1 |

These are bounded title/demo runs, not a guarantee for every gameplay scene.
The existing-capture run avoids the first automatic snapshot write; one pair
suggests a useful source of interruption but does not isolate its whole cost.
The PAL test loaded the original Europe-labelled ROM directly from its ZIP.

An interactive run completed three paused save/load cycles, F9 capture, four
window/fullscreen switches and F10 exit. A fresh process then resumed the saved
state for 300 frames. The interactive run recorded two audio gap events.
Every recorded run completed its queued PCM, restored registers and cache/MMU
witnesses, and released the owned allocation with exit zero. Completed PCM does
not imply uninterrupted playback.

Raw logs, counts and launcher hash are in
[follow-up evidence](../amiga/records/2026-10-18/followup/). ROMs, saves and private
library settings are excluded. The original report of visible scrolling columns
still needs visual confirmation in the affected game; these checks do not
establish that it is resolved.

## Rollback

Keep the previous launcher and Library.cfg together when reverting: this
development launcher uses the v4 preferences format. The player and ROM/save
formats are unchanged by this defaults update. No firmware, global audio or
Workbench resolution preferences were changed.
