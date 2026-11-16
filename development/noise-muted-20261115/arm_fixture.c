#include "audio_noise_muted.h"
struct noise_case {
 uint32_t count,amplitude,period,tap;
 int32_t counter;
 uint16_t reg,pad;
 int32_t data[65538];
};
void noise_reference(struct noise_case *c){fc_audio_noise_span(c->data+1,c->count,c->amplitude,c->period,c->tap,&c->counter,&c->reg);}
void noise_candidate(struct noise_case *c){fc_audio_noise_muted_span(c->data+1,c->count,c->amplitude,c->period,c->tap,&c->counter,&c->reg);}
