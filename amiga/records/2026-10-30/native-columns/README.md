# Native-column evidence

`col-*`: explicit VERIFY, four pixel readbacks per run. Its extra bus readback
work causes audio shortages; it is not normal play timing.
`play-*`: 600 normal frames, with the existing 8-pixel edge masks retained.
The first run creates a thumbnail and deliberately pauses for capture.
Native and relocated-model results do not substitute for physical scanout or
visual acceptance. No ROM/save data is included.

The first build stopped on an unnecessary generator edit to a historical player
model header. That unused edit was removed; the current launcher model and player
session parser are tested separately. The first settings test resolved a stale
library session header; the test now names the actual player header explicitly.
