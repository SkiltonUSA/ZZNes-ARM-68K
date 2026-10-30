/* GPL-3.0-or-later. Two adjacent FCEUX FIR outputs, four taps per step.
 * r0 = last sample in first window; r1 = forward coefficients;
 * r2 = tap count (positive multiple of four); r3 = two int32 sums.
 * Preserve scalar semantics: low 32-bit product, arithmetic >>6, wrapping sum.
 * Caller checks NEON availability and saves/restores the firmware SIMD state.
 * Uses only AAPCS caller-saved d0-d7/d16-d31; no FPSCR changes. */
.syntax unified
.arm
.fpu neon
.text
.global fc_audio_fir_neon
.hidden fc_audio_fir_neon
.type fc_audio_fir_neon,%function
fc_audio_fir_neon:
 sub r0,r0,#12
 veor q8,q8,q8
 veor q9,q9,q9
1:
 add r12,r0,#4
 vld1.32 {d0-d1},[r0]
 vld1.32 {d2-d3},[r12]
 vld1.32 {d4-d5},[r1]!
 vrev64.32 q2,q2
 vswp d4,d5
 vmul.i32 q0,q0,q2
 vmul.i32 q1,q1,q2
 vshr.s32 q0,q0,#6
 vshr.s32 q1,q1,#6
 vadd.i32 q8,q8,q0
 vadd.i32 q9,q9,q1
 sub r0,r0,#16
 subs r2,r2,#4
 bne 1b
 vpadd.i32 d16,d16,d17
 vpadd.i32 d16,d16,d16
 vpadd.i32 d18,d18,d19
 vpadd.i32 d18,d18,d18
 vst1.32 {d16[0]},[r3]!
 vst1.32 {d18[0]},[r3]
 bx lr
.size fc_audio_fir_neon,.-fc_audio_fir_neon
