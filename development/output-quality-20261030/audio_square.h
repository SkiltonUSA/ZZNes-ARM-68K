/* GPL-3.0-or-later. Preserve every HQ square-wave sample and phase transition.
 * Runs stop at the next timer event; silent duty spans need no buffer writes. */
#ifndef FC_AUDIO_SQUARE_H
#define FC_AUDIO_SQUARE_H
#include <stdint.h>
static void fc_audio_square_span(int32_t *dst,int count,int32_t amplitude,
                                int threshold,int period,int32_t *counter,
                                int32_t *duty)
{
 int32_t rc=*counter,dc=*duty;
 while(count>0){
  int n=(rc>0&&rc<count)?rc:count;
  if(dc<threshold&&amplitude){
   uint32_t *p=(uint32_t*)dst;int left=n;
   while(left>=4){
    p[0]+=(uint32_t)amplitude;p[1]+=(uint32_t)amplitude;
    p[2]+=(uint32_t)amplitude;p[3]+=(uint32_t)amplitude;
    p+=4;left-=4;
   }
   while(left--){*p+=(uint32_t)amplitude;p++;}
  }
  dst+=n;count-=n;rc=(int32_t)((uint32_t)rc-(uint32_t)n);
  if(!rc){rc=period;dc=(dc+1)&7;}
 }
 *counter=rc;*duty=dc;
}
#endif
