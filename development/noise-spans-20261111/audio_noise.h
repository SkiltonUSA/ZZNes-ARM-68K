/* GPL-3.0-or-later. Exact HQ noise spans; advance even when muted. */
#ifndef FC_AUDIO_NOISE_H
#define FC_AUDIO_NOISE_H
#include <stdint.h>
static void fc_audio_noise_span(int32_t *dst, unsigned count, uint32_t amplitude,
 unsigned period, unsigned tap, int32_t *counter, uint16_t *reg)
{
 uint32_t remaining=(uint32_t)*counter;
 unsigned shift=*reg;
 while(count){
  unsigned n=remaining && remaining<count?remaining:count;
  uint32_t value=(shift&0x4000)?0:amplitude;
  if(value){
   uint32_t *p=(uint32_t*)dst;unsigned left=n;
   while(left>=4){p[0]+=value;p[1]+=value;p[2]+=value;p[3]+=value;p+=4;left-=4;}
   while(left--)*p+++=value;
  }
  dst+=n;count-=n;remaining-=n;
  if(!remaining){
   remaining=period;
   shift=((shift<<1)+(((shift>>tap)^(shift>>14))&1))&0x7fff;
  }
 }
 *counter=(int32_t)remaining;*reg=(uint16_t)shift;
}
#endif
