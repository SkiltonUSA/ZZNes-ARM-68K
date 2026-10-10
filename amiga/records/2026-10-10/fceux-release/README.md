# 0.2.0-rc1: profiling, input and distribution

10 October 2026, physical A4000TX/TF4060, XX19c / XACP 1.7, AHI unit 0.
The owner requested all five next steps: profile, scheduling investigation,
ZZ9000AX exploration, joystick/Workbench selection, compatibility and release.

Selected executable: **275,216 bytes**, MD5 `f0b62ec828adf96d0b905f8b9f3e6560`.
Build mode `release-profile`. This retains the accepted fast renderer and
cadence/audio batching. It adds timing histograms, standard lowlevel joystick
input, a ROMs initial drawer, deterministic INPUT diagnostic and Workbench
icons. No new emulator core, shared-memory layout, cache policy or firmware.

## Measurements and scheduling decision

| Workload | Frames | Displayed FPS including readback/drain |
|---|---:|---:|
| Profiled accepted pacing, Mario startup | 300 | 53.69 |
| Deferred-flip-only pacing, Mario startup | 300 | 53.64 |
| Profiled pacing, audio output disabled, Mario startup | 300 | 57.27 |
| **Release candidate, Mario with scripted Start** | **1,800** | **55.47** |
| Release candidate, SMW startup | 300 | 54.26 |
| Original audio/controller fixture, VERIFY readbacks | 300 | 45.69 |

Do not compare the VERIFY workload with ordinary playback: it reads every
pixel on six frames. The no-output test still emulates the APU; it is diagnostic,
not a playable replacement. Flip-only pacing produced no benefit and is not
selected. There is **no established new throughput gain or sustained 60 FPS**.
The earlier accepted fast build remains available and is not overwritten.

The Mario INPUT test presses Start on emulated frames 90–99, independent of
host scheduling, matching the existing native oracle. It is a reproducible
Start-triggered workload, not a claim of 30 seconds of active owner gameplay.
All 31 sampled native hashes/cycle counts matched; 1,800 flips and all 958,349
PCM samples completed. No AHI error, RET1 failure, register mismatch, bad cache
witness or leaked owned allocation. This is not an audible acceptance result.

After the first 60 frames, Mario mean host stages were:

| Stage | Mean |
|---|---:|
| FRAME command, including overlapped audio worker scheduling | 7.887 ms |
| Remaining prior-flip drain | 4.589 ms |
| Audio preparation | 0.425 ms |
| Complete host presentation transaction | 3.100 ms |
| Complete loop | 17.835 ms |
| Observed flip-ACK interval | 17.897 ms |

ARM packing itself remains ~1.15 ms. AHI SendIO wall time totalled 5.724 s
across the 1,800-frame run. This includes scheduling/driver work and overlaps
other stages; it is not exclusive CPU time. 84/1,740 loop samples exceeded
34 ms. Host ACK observation is delayed by scheduling; these are not exact
scanout timestamps. Histograms use <=1/8/17/20/34 ms and >34 ms buckets.
No per-frame file I/O was added. Final counters print after the run.

## ZZ9000AX exploration

`ax_probe.c` enumerated the installed AHI database and successfully allocated
then freed both **cafe0000 (Stereo++)** and **cafe0001 (Stereo)** with requested
32 kHz, one channel and two sound slots. No playback was started; requested
frequency is not proof of the driver's actual mix frequency. Preferences
were not changed, and the player continues using unit 0 / Paula.

[AHI's primary documentation](https://www.lysator.liu.se/ahi/v4-site/files/ahi/doc/ahi.html)
supports application-specific mode selection through AHI_AllocAudio. Unit 255
is the low-level library interface, not a CMD_WRITE shortcut to Music Unit
hardware. A future stream needs immutable buffer ownership, interrupt-safe
SoundFunc/PlayerFunc handoff, underrun accounting and drain/stop tests.

The reviewed [XACP 1.7 notes](https://github.com/Xanxi-Amiga/XACP-ZZ9000/blob/main/docs/XACP_V1_7_DEVELOPER_NOTES.md),
[XX19c firmware](https://github.com/Xanxi-Amiga/XACP-ZZ9000/tree/main/firmware/source/XX19c)
and [PicoDrive frontend](https://github.com/Xanxi-Amiga/XACP-ZZ9000/tree/main/applications/emulators/ZZPicodrive/ZZPicodriveMD)
do not establish a general app-owned Core1-to-AX PCM playback interface.
PicoDrive drains generated PCM through its 68k AHI/Paula frontend. Decoder PCM
rings and firmware AX DMA memory are not interchangeable allocations. Our
private Core1 mapping masks interrupts and cannot simply invoke firmware
callbacks or reach shared peripherals. Direct AX remains a separate interface
and ownership investigation; no direct-AX or HDMI audio claim is made.

## Controls, Workbench and compatibility

Physical port 2 (lowlevel port 1) uses standard ReadJoyPort flags. Directions,
red=A and blue=B; CD32 green=Select, play=Start. Keyboard and joystick are ORed
without a key release erasing joystick state. Mouse/unknown types are ignored;
no force-detection changes or custom-chip writes. Sample after flip drain,
outside the bitmap lock, consume next frame. On this machine lowlevel opened
and returned UNKNOWN with no active buttons. Owner physical mapping acceptance
is pending. USB/DB9 adapters are not implicitly supported by this result.

The real Workbench icon launched the executable with a 65,536-byte stack,
then opened the ASL ROM requester. Clicking Cancel removed the requester and
released the owner port; Escape/left-Amiga-B did not cancel this requester.
A second Workbench launch selected Controller-Test.nes through the actual file
field, opened the fullscreen and returned to Workbench with Q; the owner port
was absent afterward. Icons were created by our controller-art generator and read back to verify
tool/drawer type and stack size. ROMs are selected from PROGDIR:ROMs.

Four original tone/controller fixtures cover NROM 16/32 KiB PRG and both
mirroring modes; each ran 120 frames with/without scripted input through native
and sanitizer adapters. Existing cartridge rejection tests also pass. Physical
SMW mapper 90 matched six sampled native states; the original NROM tone fixture
matched six states and six complete framebuffers with all audio completed.
No arbitrary mapper, battery, save-state or SNES support was added.

## Verification and evidence caveats

- Actual generated audio-worker tests: ordered PCM, flush, wrap, failures,
  cancel and cleanup; exhaustive palette equivalence; 200,000 flip handoffs.
- Joystick mapping all 256 button combinations across valid and invalid device
  types; profile warmup/bin boundaries and 32-bit timestamp wrap.
- A9 instruction model: six frames, all four pixel formats, guards, challenge,
  cancellation and mapping revocation. Not a cache-coherence simulation.
- ARM/debug integration and MCP smoke suite passed; live physical results
  above separately establish target execution and cleanup.
- Standalone build/test and reproducibility results are saved alongside.

The first log fetches failed because the large Amiga directory listing omitted
new entries. Logs existed and were recovered by exact-file List sizes plus
2048-byte reads. The no-output run initially hit the normal analyzer's required
audio assertion; explicit --no-audio-output validation now preserves that
boundary. A fixture launch was blocked by our owner check while the Workbench
requester was still open; it was run only after cancellation. No reset/crash.

`variants/` preserves build-time provenance; documentation changes after a
build are not retroactively folded into those hashes. `run.py` is the local
orchestrator, using private owner ROM paths and the existing inventory fetch
helper; it is not a portable ROM distribution or turnkey standalone runner.
