// GPL-3.0-or-later. Sparse scheduling must be PCM-identical to the dense mixer.
#include "platform.h"
#include "SoundMixer.h"
#include "mix_lut.h"
#include <assert.h>
#include <stdio.h>
void player_blip_rate(blip_t *);
static SoundMixer sparse;
static int16_t delta[5][10000];
static int current[5],previous;
static blip_t *reference;
static void add(unsigned ch,unsigned t,int v){
 sparse.AddDelta((AudioChannel)ch,t,v);delta[ch][t]+=v;
}
static void flush(unsigned cycles){
 sparse.count=0;sparse.PlayAudioBuffer(cycles);assert(!sparse.overflow);
 for(unsigned t=0;t<=cycles;t++){
  bool changed=false;
  for(unsigned c=0;c<5;c++)if(delta[c][t]){current[c]+=delta[c][t];delta[c][t]=0;changed=true;}
  if(changed){int out=pulse_lut[current[0]+current[1]]+tnd_lut[3*current[2]+2*current[3]+current[4]];blip_add_delta(reference,t,out-previous);previous=out;}
 }
 blip_end_frame(reference,cycles);int n=blip_samples_avail(reference);int16_t pcm[1024];
 assert(n>=0&&n<=1024);assert(blip_read_samples(reference,pcm,n,0)==n);
 assert(sparse.count==(unsigned)n);for(int i=0;i<n;i++)assert(sparse.samples[i]==pcm[i]);
}
int main(){
 player_reset_alloc();sparse.Reset();reference=blip_new(1024);assert(reference);player_blip_rate(reference);blip_clear(reference);
 // Word boundaries, simultaneous DAC changes, cancellation, and retained future events.
 add(0,31,7);add(1,31,9);add(0,32,-7);add(1,32,-9);add(2,0,3);add(2,0,-3);
 flush(31);flush(32);flush(9999);
 uint32_t rng=1;int level[5]={};
 for(unsigned block=0;block<100;block++){
  // Channels submit separately: timestamp order across channels is deliberately scrambled.
  for(unsigned ch=0;ch<5;ch++)for(unsigned t=0;t<10000;){
   rng=rng*1664525u+1013904223u;int value=(rng>>16)%(ch==4?128:16);
   add(ch,t,value-level[ch]);level[ch]=value;t+=1+(rng&127);
  }
  flush(9999);
 }
 puts("PASS sparse mixer: 100 dense-reference PCM chunks, simultaneous/out-of-order/end-boundary events");
}
