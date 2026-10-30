#include <stdint.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "audio_square.h"
static uint32_t seed=1030;
static uint32_t random32(){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return seed;}
int main(){
 int32_t a[2056],b[2056];
 for(unsigned t=0;t<10000;t++){
  unsigned n=random32()%2049,threshold=1u<<(random32()%3);
  if(t%4==0)threshold=6;
  int32_t amp=(int32_t)random32(),period=18+random32()%4079;
  int32_t rc=t%8==0?0:t%8==1?-10:t%8==2?INT32_MIN:(int32_t)(1+random32()%period);
  int32_t dc=random32()%8,r=rc,d=dc;
  for(unsigned i=0;i<2056;i++)a[i]=b[i]=(int32_t)random32();
  for(unsigned i=0;i<n;i++){
   if(d<(int)threshold)a[i+3]=(int32_t)((uint32_t)a[i+3]+(uint32_t)amp);
   r=(int32_t)((uint32_t)r-1);
   if(!r){r=period;d=(d+1)&7;}
  }
  fc_audio_square_span(b+3,n,amp,threshold,period,&rc,&dc);
  assert(r==rc&&d==dc);assert(!memcmp(a,b,sizeof(a)));
 }
 puts("PASS 10000 square-wave spans: exact samples/phase/counter, zero/negative counters, wrap and bounds");
}
