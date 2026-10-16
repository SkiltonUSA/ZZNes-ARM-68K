#include <stdint.h>
#include <assert.h>
#include <stdio.h>
typedef uint32_t ULONG;typedef uint8_t UBYTE;
#define JP_TYPE_MASK (15u<<28)
#define JP_TYPE_JOYSTK (3u<<28)
#define JP_TYPE_GAMECTLR (1u<<28)
#define JPF_JOY_UP (1u<<3)
#define JPF_JOY_DOWN (1u<<2)
#define JPF_JOY_LEFT (1u<<1)
#define JPF_JOY_RIGHT (1u<<0)
#define JPF_BUTTON_RED (1u<<22)
#define JPF_BUTTON_BLUE (1u<<23)
#define JPF_BUTTON_GREEN (1u<<20)
#define JPF_BUTTON_PLAY (1u<<17)
static ULONG clock_us;
static ULONG us(void){return clock_us;}
static UBYTE fc_joy_decode(ULONG state){
 ULONG type=state&JP_TYPE_MASK;UBYTE b=0;
 if(type!=JP_TYPE_JOYSTK&&type!=JP_TYPE_GAMECTLR)return 0;
 if(state&JPF_JOY_UP)b|=16;
 if(state&JPF_JOY_DOWN)b|=32;
 if(state&JPF_JOY_LEFT)b|=64;
 if(state&JPF_JOY_RIGHT)b|=128;
 if(state&JPF_BUTTON_RED)b|=1;
 if(state&JPF_BUTTON_BLUE)b|=2;
 if(type==JP_TYPE_GAMECTLR){if(state&JPF_BUTTON_GREEN)b|=4;
 if(state&JPF_BUTTON_PLAY)b|=8;}
 return b;
}
/* GPL-3.0-or-later. Host durations; no I/O in frame/flip sampling. */
struct fc_stage { uint64_t sum; ULONG n,max,bins[6]; };
static struct fc_stage fc_stages[6];
static ULONG fc_profile_frame,fc_last_flip,fc_input_changes;
static void fc_sample(unsigned stage,ULONG dt){
 struct fc_stage *s=&fc_stages[stage];unsigned b;
 if(fc_profile_frame<60)return; /* Exclude initial readback/startup. */
 s->sum+=dt;s->n++;if(dt>s->max)s->max=dt;
 b=dt<=1000?0:dt<=8000?1:dt<=17000?2:dt<=20000?3:dt<=34000?4:5;
 s->bins[b]++;
}
static void fc_flip_sample(void){ULONG now=us();if(fc_last_flip)fc_sample(5,now-fc_last_flip);fc_last_flip=now;}
static void fc_profile_print(void){
 unsigned i;for(i=0;i<6;i++){struct fc_stage *s=&fc_stages[i];
 printf("FRAME_TIMING stage=%u count=%u mean_us=%u max_us=%u bins=%u,%u,%u,%u,%u,%u\n",i,s->n,s->n?(ULONG)(s->sum/s->n):0,s->max,s->bins[0],s->bins[1],s->bins[2],s->bins[3],s->bins[4],s->bins[5]);}
 printf("INPUT_PROFILE changes=%u\n",fc_input_changes);
}

int main(void){
 const ULONG flags[8]={JPF_BUTTON_RED,JPF_BUTTON_BLUE,JPF_BUTTON_GREEN,JPF_BUTTON_PLAY,JPF_JOY_UP,JPF_JOY_DOWN,JPF_JOY_LEFT,JPF_JOY_RIGHT};
 for(unsigned n=0;n<256;n++){
  ULONG flags_in=0;for(unsigned i=0;i<8;i++)if(n&(1u<<i))flags_in|=flags[i];
  assert(fc_joy_decode(JP_TYPE_GAMECTLR|flags_in)==n);
  assert(fc_joy_decode(JP_TYPE_JOYSTK|flags_in)==(n&~12u));
  for(unsigned type=0;type<16;type++)if(type!=1&&type!=3)assert(!fc_joy_decode((type<<28)|flags_in));
 }
 fc_sample(0,30000);assert(!fc_stages[0].n);
 fc_profile_frame=60;
 const ULONG times[6]={1000,8000,17000,20000,34000,34001};
 for(unsigned i=0;i<6;i++)fc_sample(0,times[i]);
 for(unsigned i=0;i<6;i++)assert(fc_stages[0].bins[i]==1);
 assert(fc_stages[0].n==6&&fc_stages[0].max==34001&&fc_stages[0].sum==114001);
 clock_us=0xfffffff0u;fc_flip_sample();clock_us=16;fc_flip_sample();
 assert(fc_stages[5].n==1&&fc_stages[5].sum==32);
 fc_profile_print();
 puts("PASS all pad combinations, reject mouse/unknown, timing bins/startup exclusion/timer wrap");
}
