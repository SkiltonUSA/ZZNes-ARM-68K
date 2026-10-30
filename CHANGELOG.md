# Changelog

## 0.8.7-dev — native columns

- Add Native columns beside Sharp/Smooth: centre all 256 source columns without uneven repetition or reduction. Existing edge masks still apply.
- Keep all 240 rows and repeat pixels evenly in 2×/3× windows. The native picture is narrower; monitor aspect correction remains available through Sharp/Smooth.
- Preserve existing settings; a native-column preference requires matching launcher/player versions.
- [Tests and limitations](docs/native-columns.md). Published 0.8.6 Beta remains unchanged.

## 0.8.6 Beta

- Per-app Paula 14-bit output at 22.05 or 28 kHz; explicit configured AHI and ZZ9000AX choices. Auto preserves the configured output device.
- Three-buffer callback audio, nine-frame priming, twelve producer slots and starvation diagnostics; no global audio preference changes.
- Drain queued audio before automatic/manual screenshots and re-prime afterwards; capture deliberately pauses playback.
- Includes 1×/2×/3× Workbench windows and the previous audio scheduling improvements.
- [Investigation, upstream comparison and tests](docs/output-quality.md). Listening confirmation remains pending.

## 0.8.5-dev — audio scheduling and window sizes

- Add 1× (320×240), 2× (640×480) and 3× (960×720) Workbench windows; fit smaller screens automatically and remember the window size across fullscreen switches.
- Scale on the ARM into an allocated, locked Picasso96 bitmap; retain 320×240 library snapshots.
- Remove repeated Workbench copies of unchanged pictures. Allow up to three omitted display updates at 2× and five at 3×; emulation and audio frames are retained.
- Notify the AHI worker as soon as a complete batch is ready; keep configured unit 0 output.
- Increase NES startup prebuffer from four to six frames.
- Keep complete enlarged pixel readbacks in explicit verification mode; ownership and mapping checks remain active during play.
- [Hardware measurements and remaining listening check](docs/audio-window.md).

## 0.8.4-dev — configured audio output

- Restore configured AHI unit 0 for normal playback; an installed ZZ9000AX driver no longer redirects audio away from Paula.
- Keep the current ARM payload and core fixes unchanged. AX remains an explicit development experiment.

## 0.8.3 Beta — ZZ9000AX audio and register dispatch

- Select ZZ9000AX 16-bit stereo through per-app AHI; use configured unit 0 if AX is unavailable. Global preferences remain unchanged.
- Include the tested limited ARM register dispatch with a 32 MiB executable reserve (48 MiB total runtime allocation).
- Keep normal regional pacing, ROM input, save/load, screenshots and fullscreen/window switching.
- Package matching launcher/player versions and the offline amipkg installer with bundled scanline tools.
- Matched short audio tests measured NES +3.2% / SNES +4.6% FPS; these are not all-title or long-session audio-quality claims.

## 0.8.2-dev — experimental register dispatch

- Add opt-in per-app ZZ9000AX AHI output with unit-0 fallback, immutable buffers and hardware timing/lifecycle evidence; global audio preferences unchanged.
- Call ten generated register handlers through the original opcode switch; remove per-instruction classification and guest-address lookup.
- Add isolated AHI/bitmap-call profiling and four-frame batch tests; preserve original audio defaults after matched hardware comparisons.
- Add isolated serial/overlap presentation tests with pinned render locks; hardware checks pass, but no performance gain. Defaults unchanged.
- Add opt-in 250 µs fullscreen ACK polling and phase profiling; roughly 90% fewer register reads, no useful counter-free FPS gain.
- Separate timing from recurring pixel verification; complete 16 fixed-presentation hardware comparisons without a repeatable earlier-audio gain.
- Retain the requested 32 MiB executable reservation and 48 MiB owned runtime.
- Add opt-in batch-ready audio notification and matched hardware/model evidence.
- Keep releases unchanged; the earlier freeze is recorded and remains unexplained.
- [Results and limitations](docs/jit-register-experiment.md).

## 0.7.4 Beta — packaged release

- Publish the matched, physically tested 0.7.4-dev launcher and player.
- Include compact layouts, ROM Manager, temperature and fullscreen FPGA/windowed software scanlines.
- Add a complete offline amipkg installer with MUI/Picasso96/AHI/ZZ9000 checks and automatic install-missing scanline tools.
- Include a manual ZIP alternative, checksums and current feature/specification documentation.
- Incorporate the development changes below; no additional FPS gain is claimed by packaging.

## 0.7.4-dev — cartridge compatibility

- Add mapper 78 with Holy Diver H/V and Cosmo Carrier single-screen wiring.
- Add CNROM/mapper 3 with bus conflicts; recognize exact DiskDude legacy headers without changing ROM files.
- Verify Holy Diver and Cybernoid gameplay, states, display switching and cleanup on the Amiga.
- Include duplicate-scan progress and cancellation in the matched launcher/player build.
- Import the complete pinned FCEUX source and mapper inventory for the staged full-feature port.
  Imported boards and desktop tools are not automatically enabled.

## 0.7.3-dev — scalable launcher

- Compact layout for smaller Workbench screens, with independently scrollable pages.
- Smaller previews/loading cards, two-column save cards and a compact controller diagram.
- Keep navigation, Launch and settings controls visible during page scrolling.
- Preserve current player binaries, settings format, ROM Manager and scanline integration.

## Development — ROM Manager and temperature

- Bulk import from a selected directory or mounted SD/USB drive, including subfolders.
- Confirmed duplicate library-entry removal using decoded ROM content; files and saves kept.
- Verified save-state, battery-save, snapshot and library backups into new folders.
- Live read-only ZZ9000 Zynq temperature beside the version number.
- Experimental amipkg LHA/recipe builder with automatic install-missing Xanxi controls.
  Custom repositories require the documented local amipkg 0.7.11 recipe fix.

## Scanline backend development update

- Fullscreen: Xanxi FPGA Classic/Soft/Gradient; window: Soft software filtering.
- F7 cycles fullscreen modes or toggles windowed Off/Soft; no double filtering.
- Hardware effect disabled when entering a window and on normal exit.
- Legacy Thin setting migrates to Soft; fullscreen uses the low-resolution mode.
- Both packages bundle Xanxi controls, source/license and an install-missing helper.
- Existing control tools, firmware and startup files are preserved.


## Unreleased — F7 scanline control

- F7 cycles Off, Soft, Gradient (smooth), Classic (hard) during play or pause.
- Show F7 Scanlines on the loading panel and in the controls guide.
- Retain saved defaults; ignore key-repeat and apply changes after pending flips.


## Unreleased — display defaults

- Fullscreen with software scanlines for new libraries.
- Loading panel labels F9 as Screenshot.


## 0.7.2-dev — optimisation candidate (not a tagged release)

- Prime four NES audio frames before playback, retaining three-frame AHI batches.
- Cache output palette byte order and add optional Smooth scrolling scaling.
- NEON horizontal interpolation with exact scalar fallback and SIMD restoration.
- Persist the new scaling option in v4 settings; read previous settings formats.
- Faster large-library sorting, metadata writing and token parsing.
- Add native, relocated ARM and physical validation; see [measurements](docs/optimisation-20261018.md).

## Unreleased launcher navigation

- Label the existing effect Software scanlines; explain that ZZScanlines is not required.

- Add a red Launch button to the permanent bottom bar, visible on every page.
- Replace automatic mounted-drive discovery with Disks / Browse / Scan once.
- Keep Continue and save-state actions separate from starting a game.

## 0.7.1 Beta

- Add EmuELEC side-panel theme to both display modes.
- Keep viewport geometry, overscan and scanlines independent.
- Compact 16-colour artwork table; existing memory layout retained.
- Cartridge support and emulation core unchanged.

## 0.7.0 Beta

- Load single-cartridge ZIPs directly in the library and player.
- Discover ZIP cartridges through Add, Folder and mounted-drive scanning.
- Stored/deflate support, bounded decompression and CRC checks before ARM use.
- Preserve member filenames for NES PAL detection; no temporary ROM files.
- Explicit whole-archive deletion confirmation.
- Existing ARM core, cartridge limits and save formats retained.

## 0.6.3 Beta

- Remove launcher title-bar text; keep version in the footer and About.

## 0.6.2 Beta

- New colour logo in the sidebar, startup and loading screens.
- Matching palette-mapped Workbench icon with transparency.
- Existing icon position and launch settings preserved when updating.

## 0.6.1 Beta

- Remove the 128-ROM cap; library and display storage grow with available memory.
- Hash-based duplicate detection and faster sorting for large collections.
- Live search with a short typing delay on MUI.
- Graceful allocation failure; retain discovered entries and existing settings.
- Existing preferences, favourites, history and save paths remain compatible.

## 0.6.0 Beta

- Sidebar MUI launcher, original branding and Workbench icon.
- Startup/loading panels; loading ends after the first completed frame.
- Fullscreen/window switching, optional FPS and three software scanline styles.
- Guarded NEON row stores and fused byte dimming; scalar fallback and comparison.
- Add, rename and confirmed deletion; incremental mounted-volume ROM discovery.
- Existing cadence, AHI batching, mapper/region handling and save formats retained.

## 0.5.0 Beta

- Regional cadence and batched audio in normal interactive play.
- Expanded mapper compatibility and automatic PAL/NTSC timing.
- MUI library, game snapshots, save slots and About page.

## 0.2.0-rc1

- FCEUX Workbench player, joystick input and frame profiling.

Historical build records retain the detailed intermediate experiments.
