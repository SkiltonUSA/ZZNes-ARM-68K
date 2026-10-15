# ZZPicoDriveMD on the A4000TX

On 9 October 2026, we installed and tested Xanai's unmodified ZZPicoDriveMD 1.1
with the owner's Sonic the Hedgehog ROM. The owner confirmed working picture
and music. The final AHI session was left running.

## Installation and provenance

[Xanxi / Xanai's application](https://github.com/Xanxi-Amiga/XACP-ZZ9000/tree/8bb998e4f9cac88d519ccdf3559c8a404fb6381d/applications/emulators/ZZPicodrive/ZZPicodriveMD)
is pinned to commit `8bb998e4f9cac88d519ccdf3559c8a404fb6381d`.
Credit Xanai for the ZZ9000 integration and notaz/contributors for PicoDrive.
This was an installation of upstream's executable, not our own emulator build.

- Directory: `SD032G:Dev/ZZPicoDriveMD`.
- Executable: `ZZPicodriveMD_v1.1`, 641,988 bytes, native Amiga MD5
  `908c5324c19c04e28cae9d4343b6fb40`.
- Archive SHA-256: `73686e697f54a6f6c5ec30b66942f1d9e0154b6544c94ec53f320f76e6c97f4c`.
- ROM: `ROMs/Sonic1.bin`, 524,288 bytes, CRC32 `f9394e97`, matching on 68k/ARM.
  User-supplied ROM bytes are excluded from Git and distribution.
- Existing XX19c / XACP 1.7 firmware, TF4060, ZZ9000 and Picasso96 retained.
  No firmware, driver or global audio preference updates.

Run `Execute SD032G:Dev/ZZPicoDriveMD/Start-Sonic-ahi`, or use the executable's
Workbench requester. Keyboard: arrows, keypad 1/2/3 for A/B/C, Return for Start,
**Shift+Esc to exit**. Mouse click also exits. Only one Core1 application may run.
Stock PicoDrive does not advertise our debugger's owner port; inspect screens
and current application state before another ARM launch.

## Measured results

Short intro/attract runs used the same Sonic ROM and USA region setting.
Displayed rates below are the stock launcher's acknowledged-flip measurements.

| Test | Duration | Displayed frames | Displayed FPS | Audio diagnostics |
| --- | ---: | ---: | ---: | --- |
| Sonic, AHI unit 0 | approximately 27.6 s | 965 | **34.8** | 0 reported underruns |
| Sonic, direct Paula | approximately 28.2 s | 842 | **29.8** | 0 underruns, 0 resyncs |
| Sonic, silence diagnostic | 37.7 s | 5 | 0.1 | Stalled; not a valid speed comparison |
| ZZNes optimized, NES mapper 90 game | matched 300-frame test | 300 | **22.53** | Different scheduling/diagnostics |

A separate read-only sample of the recovered AHI session measured **900 emulated
frames in 15.019637833 seconds: 59.9216 emulated FPS**. The corresponding
`PicoFrame` accumulated-time delta was 5,678,787 microseconds, or **6.310 ms per
emulated frame**. Two small control-memory reads took approximately 22 and 15 ms;
this is a host-timed live estimate, not a cycle-exact measurement. It is a
different sampling interval from the 34.8 displayed-FPS run.

PicoDrive continues CPU/audio emulation when it skips drawing a frame. Thus
roughly 60 emulated FPS does not mean 60 distinct frames reached the screen.
ZZNes's reported test presented every emulated frame. Different console cores,
games and drawing policies prevent treating this table as a controlled speedup
ratio. Neither the FPS nor the audio diagnostic counters prove sustained
whole-game stability. The owner's picture/music confirmation provides a separate
physical acceptance check.

## How it works and what we can learn

The ARM payload runs PicoDrive, including its Cyclone ARM assembly 68000 core,
video emulation and YM2612/PSG sound generation. It converts pixels directly into
RTG backbuffers and cleans the relevant cache lines. The 68k manages triple-buffer
ownership and the deferred-PAN flip/acknowledgment interface. It does not copy a
whole framebuffer across Zorro III for every frame.

AHI runs in a separate task, draining a 524,288-byte PCM ring with 512-frame
requests at 22,050 Hz stereo. PCM consumption paces emulation. Direct Paula instead
converts to 8-bit stereo DMA output; the log reports 22,030 Hz. Both backends still
involve the 68k. On this machine AHI unit 0 selects Paula. The installed ZZ9000AX
is **not used by these tests**, and this is not direct ARM-to-AX or HDMI audio.

For ZZNes, a dedicated audio task and explicit ring/prebuffer ownership are useful
next experiments. Separating drawing from emulation could preserve game/audio
speed under presentation pressure, but must retain CPU/PPU/APU timing and be
reported as skipped presentation. Private-cache and framebuffer-cache changes
need our own bounded mapping/coherency checks: do not copy PicoDrive's fixed
firmware-reserved addresses into Exec-owned allocations. No PicoDrive code was
copied into Mesen; its historical non-commercial license requires separate review.

## Blank screen recovery and diagnostic limitations

The stock silence path leaves AHI open, returns zero samples and does not advance
the PCM read position. ARM continues waiting for ring drainage and stalls after
the initial frames. CLI audio choices are saved to `ZZPicoDrive.cfg`; our silence
test therefore left `audio=2`, which the owner's next GUI launch inherited.

We exited that blank session using Shift+Esc, saved the old config under
`Logs/ZZPicoDrive.silence.cfg`, restored **`audio=0` (AHI)** and relaunched Sonic.
The owner confirmed picture and music and reported that it was fast. The silence
launcher now lives under `Logs/Start-Sonic-silence.diagnostic`; do not select
Audio=None for normal play in this build. AHI and Paula scripts use absolute ROM
paths. `ReadMe-Local-Tests.txt` records the workaround on the Amiga.

Other caveats found by reading the upstream launcher and Core1 source:

- Conversion timing variables are updated only on drawn frames but consumed on
  skipped draws too. Stale values/unsigned subtraction make those timings invalid.
- Several host flip/wait statistics are explicitly zeroed; a zero missed-vblank
  field is not proof of perfect pacing.
- ARM diagnostic totals persisted across the AHI/Paula launches, then reset on
  a later launch. Use live counter differences, not totals divided by run length.
- AHI underruns and ZZNes's completed-previous-buffer observations are different
  metrics; they cannot be compared as equivalent audio-gap counts.
- The stock stop log alone is insufficient: completed tests were additionally
  checked for stopped status `FF`, equal command/ACK sequence and zero error,
  followed by Workbench restoration. This does not establish our ZZNes-specific
  MMU/register restoration guarantees. A one-second post-exit harness check was
  too short; subsequent inspection confirmed normal return.

The strict screen-opening and screen-buffer-allocation attempts used stock
fallbacks successfully; their failure messages were not fatal. No screenshots
were requested from the hardware during these tests.

## Evidence

[Captured logs, provenance, checksums and live-rate sample](../amiga/records/2026-10-09/zzpicodrive-comparison/)
include `ahi-first.log`, `paula.log`, `silence.log`, `ahi-live-rate.json` and
`final-install.txt`. The recovered session remains running, so its final exit log
is not yet captured. The temporary Mac transfer server was stopped.

See also the earlier [source review](../amiga/mesen_nes/zzpicodrive-review.md) and
the [ZZNes player results](../amiga/mesen_nes/player.md).
