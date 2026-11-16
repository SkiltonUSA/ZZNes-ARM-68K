/* GPL-3.0-or-later. Exact muted HQ noise advancement; no sample writes. */
#ifndef FC_AUDIO_NOISE_MUTED_H
#define FC_AUDIO_NOISE_MUTED_H
#include "audio_noise.h"
/* The first eight feedback bits depend only on the incoming 15-bit state
 * for either NES tap (8 or 13). Bit 7 is the first feedback bit emitted. */
static unsigned fc_noise_step8(unsigned state, unsigned tap)
{
 return ((state << 8) | (((state >> (tap - 7)) ^ (state >> 7)) & 255u)) & 0x7fffu;
}
static void fc_audio_noise_muted_span(int32_t *dst, unsigned count, uint32_t amplitude,
 unsigned period, unsigned tap, int32_t *counter, uint16_t *reg)
{
 if(amplitude){fc_audio_noise_span(dst,count,amplitude,period,tap,counter,reg);return;}
 uint32_t remaining=(uint32_t)*counter;
 unsigned state=*reg;
 if(count && remaining && count>=remaining){
  count-=remaining;
  state=((state<<1)+(((state>>tap)^(state>>14))&1u))&0x7fffu;
  /* The NES period tables are at most 4068 ticks. No division or lookup table
   * is needed, and a partial period retains exactly its original phase. */
  unsigned eight=period*8u;
  while(count>=eight){state=fc_noise_step8(state,tap);count-=eight;}
  while(count>=period){state=((state<<1)+(((state>>tap)^(state>>14))&1u))&0x7fffu;count-=period;}
  remaining=period;
 }
 *counter=(int32_t)(remaining-count);*reg=(uint16_t)state;
}
#endif
