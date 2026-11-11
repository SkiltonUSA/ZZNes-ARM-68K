#include "audio_noise.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
static uint32_t random_state=17;
static uint32_t next(){random_state=random_state*1664525u+1013904223u;return random_state;}
int main(){
 for(unsigned trial=0;trial<60000;trial++){
  int32_t a[1026],b[1026];for(unsigned j=0;j<1026;j++)a[j]=(int32_t)next();memcpy(b,a,sizeof a);
  unsigned count=trial%1025,period=1+next()%4069,tap=trial&1?8:13;
  uint32_t amplitude=trial%3?((next()%31)<<16):0;
  int32_t counter=trial%7?(int32_t)(next()%4100):(int32_t)next(),reference=counter;
  uint16_t reg=next()&0x7fff,expected=reg;
  for(unsigned j=0;j<count;j++){
   ((uint32_t*)a)[j+1]+=(expected&0x4000)?0:amplitude;
   reference=(int32_t)((uint32_t)reference-1);
   if(!reference){reference=period;expected=((expected<<1)+(((expected>>tap)^(expected>>14))&1))&0x7fff;}
  }
  fc_audio_noise_span(b+1,count,amplitude,period,tap,&counter,&reg);
  assert(counter==reference && reg==expected && !memcmp(a,b,sizeof a));
 }
 puts("PASS 60000 exact noise-span cases: samples, counters, LFSR, both taps, mute, zero/negative counters and guards");
}
