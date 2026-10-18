# Optimisation candidate

Editable overlay for the current beta source tree. The default release rebuild
and archived release files are unchanged. This candidate is 0.7.2-dev.

Build: `python3 scripts/build_current.py --arm --optimisation`.
Run `make test-optimisation-native`; see `docs/optimisation-20261018.md` for
relocated ARM checks, physical evidence and limits. Builds never deploy.

- Cache palette byte order once, instead of converting each output pixel.
- New-library defaults: fullscreen, Soft software scanlines and Sharp pixels.
  The loading panel explicitly labels F9 Screenshot.
- Add optional horizontal, centre-aligned linear scaling. NEON blends four
  pixels at once using table lookups into a converted source row; scalar
  fallback and partial tails are exact.
- Preserve the existing SIMD guard and capability checks.
- Expose Sharp pixels / Smooth scrolling in Display; persist settings as v4.
  Older v1/v2/v3 settings read with Sharp selected. Back up settings before using
  this candidate: old launchers cannot read v4.
- Add `VERIFY` to bounded session launches for active-frame readbacks.
- Cache display titles for sorting; fall back if temporary allocation fails.
- Batch hex serialization and parse bounded numeric/hex tokens without a
  formatted scan per record. No fixed library count limit is introduced.

The cores, XACP ownership and teardown contracts are retained. These changes do
not import DOSBox's x86 JIT, VFP scheduler or TinyGL matrix routines.
