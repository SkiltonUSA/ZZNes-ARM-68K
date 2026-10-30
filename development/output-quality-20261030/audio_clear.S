/* GPL-3.0-or-later. Clear exactly r1 aligned 32-bit words at r0.
 * Byte memset in the freestanding runtime is expensive for the HQ wave buffer.
 * No NEON, cache operations, global state or writes beyond the requested range. */
.syntax unified
.arm
.text
.global fc_audio_clear_words
.hidden fc_audio_clear_words
.type fc_audio_clear_words,%function
fc_audio_clear_words:
 push {lr}
 mov r2,#0
 mov r3,#0
 mov r12,#0
 mov lr,#0
 cmp r1,#4
 blo 2f
1:
 stmia r0!,{r2,r3,r12,lr}
 sub r1,r1,#4
 cmp r1,#4
 bhs 1b
2:
 cmp r1,#0
 beq 4f
3:
 str r2,[r0],#4
 subs r1,r1,#1
 bne 3b
4:
 pop {pc}
.size fc_audio_clear_words,.-fc_audio_clear_words
