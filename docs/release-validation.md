# ZZNES 0.8.8 Beta validation

The matching launcher/player include corrected shared PCM, optimized HQ synthesis
and legacy-state support. [Executable hashes](release-build.json).

| Asset | Bytes | SHA256 |
| --- | ---: | --- |
| `ZZNES-0.8.8-dev-beta.zip` | 523379 | `c679391fe91fb487f1e28af89533b2e2513b884b9c2f80d7f0e2a663798f6e48` |
| `ZZNES-0.8.8-dev-beta-amipkg.lha` | 1395441 | `76fd9f7123600c888925f1f698945438fd6e82db0ae443b65b62b604426d9a0a` |
| `ZZNES-release.json` | 981 | `25e7c45267aac823dafafa49a3afa805af948cbb19b631345d55da10a5abf4ad` |

## Checks and limits

- HQ and legacy saves reproduce PCM/video/cycles in fresh relocated ARM models;
  legacy re-saves remain byte-identical. Invalid states reject before mutation.
- Castlevania III and Super Mario World each pass 1,800 physical frames with
  pause/save/load, a 120-frame HQ resume and a 120-frame legacy resume. All six
  runs report zero starvation, complete PCM delivery and clean restoration/free.
- ZZ9000AX completes 600 HQ frames and 319,466 samples with zero starvation.
- The final installed player passes a further 300-frame HQ resume and 120-frame
  legacy resume, with the expected synthesis mode, zero starvation and clean exit.
- Current native/ARM display tests, 20,000-entry library and compact layout tests,
  audio-worker/stream tests and state-envelope sanitizer checks pass.
- ZIP/installer byte equivalence, signatures, file hashes, dependency checks,
  corruption rejection and private-data exclusions pass. The exact offline
  installer completed on the Amiga; installed executable checksums match and
  existing library/session/audio settings were preserved. Previous files were backed up.

[Release measurements](../amiga/records/2026-10-30/audio-release-0.8.8/) and
[sound diagnosis](audio-synthesis.md) record the evidence. Fresh games use HQ;
legacy saves keep their original synthesis mode. These bounded tests do not
establish whole-game compatibility or a new FPS gain. Nestopia is a reference,
not a replacement core. Global AHI preferences and firmware remain unchanged.
