# ZZNES optimisation follow-up

Current release build, supplied Super Mario World NES cartridge, 120 warm-up
frames and 30 profiled frames with no input. ARM instruction-model block slots,
not physical Cortex-A9 cycles, FPS or gameplay-wide cost percentages.

Correction: this original profile ran the scalar fallback of the NEON-capable
build. It did not exercise the SIMD FIR. `NeoFilterSound` uses 35.49% of slots; `RefreshLine`
uses 14.11%, and `FCEUPPU_Loop` 10.24%. The CPU switch is 7.91%. Noise synthesis
is 3.97%, triangle 1.85% and DMC 1.85%. One NEON instruction can process several
lanes, so these figures cannot be read as equivalent work or elapsed time.

Next candidates are exact-output noise/triangle/DMC event spans and PPU row
work. The filter already has NEON acceleration; changing coefficients or
reducing sample quality is not part of this optimisation plan. Mapper 90 hooks
and mid-scanline behaviour must retain their current ordering. Larger code-cache
reservations alone do not address the profile. SNES tile/GSU routines do not
apply directly to FCEUX.

Reproduce with the model virtual environment and LLVM tools on PATH:

```sh
python scripts/profile_audio_core.py /path/game.nes .context/ax-release-build \
  --warmup 120 --frames 30
```

No NES code, installed files, preferences or release changed in this review.
No ROM or screenshot is included. ELF/player/filter SHA-256 values are recorded.

The follow-up adds an explicit NEON option, corrects the known Unicorn CPACR
read issue, and asserts SIMD availability before measuring. See the noise-span
record for the corrected profiles. Original counts remain scalar-only evidence.
