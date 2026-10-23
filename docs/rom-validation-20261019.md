# ZZNES ROM validation — 19 October 2026

Directory: `SD032G:Emulator/ZZNES/ROMs`. Installed player: ZZFceux-ui 0.7.4-dev, MD5 `1231265568124fa17f7ce5ec62344333`.

## Result

- 13 games: gameplay observed on the physical Amiga.
- 1 controller diagnostic: runs.
- 8 games: load, but only menus, introductions or overworld were observed; gameplay is not established by this audit.
- 5 originals: rejected before gameplay.

The audit took approximately one hour including inventory, native checks, physical runs and review. Final checks confirmed all 27 ROM MD5s and both installed executable MD5s unchanged, and no Core1 task remaining.

## Scope and method

All 27 files were inventoried and attempted on the physical A4000TX/ZZ9000. This collection contains 26 games and one controller diagnostic. All matched their local source copies by MD5; this checks transfer integrity, not authenticity against a canonical ROM database.

The current core accepted 22 original files. Each passed a native 3,600-frame run and a deterministic 30-frame save/load replay comparing video and audio. Tests used AddressSanitizer and selected UndefinedBehaviorSanitizer checks (legacy array-bounds and pointer-overflow checks excluded). Native execution is not evidence of hardware compatibility.

Every original was also launched using an isolated session on the Amiga. Accepted files returned success; the five rejected files returned 20. All 27 logged zero register mismatches, a clean cache witness and release of owned memory. Rejected-file cleanup is distinct from successful emulation. Longer follow-ups checked introductions and menus where required.

These are short execution and visual checks, not complete playthroughs. Menu-only results are not a gameplay pass. Audio delivery logs do not establish subjective sound quality. Screenshot FPS is not a controlled performance benchmark. No original ROMs, saves, library entries, installed binaries or Workbench preferences were changed.

## Per-file results

Region is the iNES header timing bit, not an independent identification of the cartridge release.

| File | Mapper | Header timing | Physical observation | Result |
|---|---:|---|---|---|
| 011 Mario Bros.nes | 0 | NTSC | Mario Bros platform phase | Gameplay |
| SuperMarioWorld.nes | 90 | NTSC | First stage entered from world map | Gameplay |
| Controller-Test.nes | 0 | NTSC | Controller test pattern | Diagnostic |
| Airwolf (Japan).nes | 1 | NTSC | Briefing, take-off sequence and weapon selection; flight not confirmed | Menu / intro only |
| Asterix (E).nes | 2 | PAL | Act 1-1 | Gameplay |
| AussieRules (E).nes | 1 | PAL | Team, colour and opponent selection; match not confirmed | Menu only |
| Castlevania3 US.nes | 5 | NTSC | Name entry and animated castle sequence; native run reached gameplay | Intro only |
| Contra (USA).nes | 2 | NTSC | Stage 1 | Gameplay |
| Contra Force US.nes | 4 | NTSC | Player selection/story dialogue, then Neocity title; gameplay unconfirmed | Intro only |
| Donkey Kong 3.nes | 0 | NTSC | Greenhouse stage | Gameplay |
| HammerHarry (E).nes | 4 | PAL | Street stage | Gameplay |
| GhostsNGoblins.nes | 2 | NTSC | Graveyard stage after longer intro | Gameplay |
| Ghostbusters2.nes | 1 | NTSC | Animated sewer/city introduction; controllable level not confirmed on hardware | Intro only |
| HolyDiver.nes | 78 | NTSC | Push Start title; gameplay verified in earlier mapper-78 test of same player | Title only (this audit) |
| RollingThunder.nes | 4 | NTSC | Warehouse stage with enemies | Gameplay |
| Rockman1.nes | 2 | NTSC | Stage entered, character jumping | Gameplay |
| Rockman3.nes | 4 | NTSC | 524,304-byte text-whitespace trailer beyond declared cartridge data | Rejected |
| Rockman4.nes | 4 | NTSC | 524,304-byte text-whitespace trailer beyond declared cartridge data | Rejected |
| Rockman5.nes | 4 | NTSC | 524,304-byte text-whitespace trailer beyond declared cartridge data | Rejected |
| Rockman7.nes | 4 | NTSC | 524,304-byte text-whitespace trailer beyond declared cartridge data | Rejected |
| Tetris.nes | 3 | NTSC | Stage/round/music selection; native run reached gameplay | Menu only |
| Lolo1.nes | 1 | NTSC | Puzzle room reached after opening sequence | Gameplay |
| Lolo2.nes | 1 | NTSC | Overworld movement/castle sequence; puzzle room not verified | Overworld only |
| Lolo3.nes | 1 | NTSC | MJR tag in reserved header bytes 13–15 | Rejected |
| Cybernoid.nes | 3 | NTSC | Cybernoid level with enemies and projectiles | Gameplay |
| EarthwormJim3.nes | 4 | NTSC | Earthworm Jim stage | Gameplay |
| Jackal.nes | 2 | NTSC | Beach stage with jeep | Gameplay |

## Rejected originals

- **Rockman3.nes:** 917,536 bytes; header describes 393,232 bytes.
- **Rockman4.nes, Rockman5.nes, Rockman7.nes:** each 1,048,608 bytes; headers describe 524,304 bytes.
- All four have the same 524,304-byte text-whitespace trailer (spaces and CR/LF), beyond declared cartridge data. Rockman 3 fails cartridge validation; the other three exceed the player file-size limit first.
- **Lolo3.nes:** correct declared data length, but `MJR` occupies reserved iNES header bytes 13–15 and is rejected by the strict parser.

Mac-only diagnostic copies with these trailers removed, or the MJR bytes cleared, each passed native execution and deterministic state replay. They were not installed or hardware-tested. The originals remain unchanged. These five failures do not require new mapper IDs: mapper 4 and mapper 1 are already supported.

## Evidence

Private inventory, hashes, native results, hardware logs, input scripts and screenshots are retained in `.context/amiga/nes-validation-1019/`. Hardware test sessions are isolated in `SD032G:Dev/ROMAudit1019`. ROM data is not included in repository documentation.

The raw first-pass `cleanup` field requires exit 0 and is false for expected rejections; `resources_released` and `registers_restored` correctly record successful teardown for those cases.

## Follow-up priorities

Normalize the four Rockman trailers and the Lolo3 reserved header tag in separate copies before any replacement decision, then test those copies on hardware. For the eight unconfirmed games, use deliberate menu interaction and longer button holds; short injected key pulses may be missed, so these observations do not establish a ROM/core defect. Holy Diver gameplay was separately verified during the preceding mapper-78 deployment test; it remains title-only in this audit.
