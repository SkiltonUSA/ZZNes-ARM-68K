#include "audio_noise_muted.h"
#include <assert.h>
#include <initializer_list>
#include <stdio.h>
#include <string.h>
static uint32_t rng=17;
static uint32_t next(){rng=rng*1664525u+1013904223u;return rng;}
static unsigned step(unsigned s,unsigned tap){return ((s<<1)+(((s>>tap)^(s>>14))&1u))&0x7fff;}
int main(){
 for(unsigned tap: {8u,13u})for(unsigned s=0;s<32768;s++){
  unsigned want=s;for(unsigned n=0;n<8;n++)want=step(want,tap);
  assert(fc_noise_step8(s,tap)==want);
 }
 for(unsigned trial=0;trial<60000;trial++){
  int32_t a[4098],b[4098];for(unsigned j=0;j<4098;j++)a[j]=(int32_t)next();memcpy(b,a,sizeof a);
  unsigned count=trial%4097,period=1+next()%4069,tap=trial&1?8:13;
  uint32_t amplitude=trial%3?0:((next()%31)<<16);
  int32_t counter=trial%7?(int32_t)(next()%4100):(int32_t)next(),expected_counter=counter;
  uint16_t reg=next()&0x7fff,expected=reg;
  for(unsigned j=0;j<count;j++){
   ((uint32_t*)a)[j+1]+=(expected&0x4000)?0:amplitude;
   expected_counter=(int32_t)((uint32_t)expected_counter-1);
   if(!expected_counter){expected_counter=period;expected=step(expected,tap);}
  }
  fc_audio_noise_muted_span(b+1,count,amplitude,period,tap,&counter,&reg);
  assert(counter==expected_counter&&reg==expected&&!memcmp(a,b,sizeof a));
 }
 // Long muted flushes and exact eight-event boundaries, all NES noise periods.
 const unsigned periods[]={4,8,14,16,30,32,60,64,88,96,118,128,148,160,188,202,236,254,354,380,472,508,708,762,944,1016,1890,2034,3778,4068};
 for(unsigned period:periods)for(unsigned tap:{8u,13u})for(unsigned count:{0u,1u,32768u,65535u}){
  for(unsigned phase=1;phase<=period;phase++){
   int32_t counter=phase,expected_counter=phase;uint16_t reg=0x5a35,expected=reg;
   static int32_t reference_buffer[65536];
   fc_audio_noise_span(reference_buffer,count,0,period,tap,&expected_counter,&expected);
   int32_t scratch=123;
   fc_audio_noise_muted_span(&scratch,count,0,period,tap,&counter,&reg);
   assert(counter==expected_counter&&reg==expected&&scratch==123);
  }
 }
 puts("PASS all 65536 eight-event states, 60000 PCM/phase/guard cases and long muted phase boundaries");
}
