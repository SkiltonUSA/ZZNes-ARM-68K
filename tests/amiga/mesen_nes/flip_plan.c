#include <assert.h>
#include <stdio.h>
#include "flip_plan.h"
int main(void){
 struct nf_slots s;nf_init(&s);
 for(unsigned n=0;n<200000;n++){
  unsigned old=s.front,render=s.render;uint16_t ack=(uint16_t)n;
  assert(nf_queue(&s,ack));assert(s.pending==(int)render);
  assert(s.render!=old && s.render!=render);
  assert(!nf_queue(&s,ack)); /* never overwrite pending */
  assert(nf_ack(&s,ack)==0 && s.front==old);
  assert(nf_ack(&s,(uint16_t)(ack+2))==-1 && s.front==old);
  assert(nf_ack(&s,(uint16_t)(ack+1))==1);
  assert(s.front==render && s.front!=s.render && s.pending==-1);
  assert(s.flips==n+1);assert(nf_ack(&s,ack)==-1);
 }
 puts("PASS 200000 triple-slot handoffs, ACK wrap, pending protection, unexpected ACK rejection");
}
