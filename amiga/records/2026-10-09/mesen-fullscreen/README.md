# ZZNes fullscreen acceptance, 9 October 2026

`firmware-contract.json` pins the reviewed XX19c deferred-PAN handlers.
`preflight-initial.log` and `preflight-layout.log` record clean rejection before
flipping when P96's actual screen bitmap differed from the supplied bitmap.
`display6.log` and `display120.log` are the corrected, successful physical runs.
Run `python3 scripts/analyze_mesen_fullscreen.py` to regenerate `results.json`.

`interactive.log`: owner confirmed the picture and arrow-key control; 2,262
frames/flips, 38 NES-pixel readbacks and clean exit in 74.419783 seconds.
This run had already ended before the first attempted remote exit check.
`quit.log`: fresh installed launch, Q injected after confirming fullscreen
focus; 232 frames/flips and clean return. Result JSONs distinguish these runs.

`install.txt` and `install-md5.json` verify all five persistent installed files.
`final-state.txt` confirms Workbench, no Core1 owner, network services and both
installed executable identities. The original windowed preview is unchanged.

Native slot tests, core/model logs, build manifest and SDK/MCP regression log
are included. Regression log workspace/home paths are normalized. The header
source contains the independent implementation; XANI's design is acknowledged
in `amiga/mesen_nes/zzpicodrive-review.md`. No firmware update or screenshot.
No GitHub publication was performed.
