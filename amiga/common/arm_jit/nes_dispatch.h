/* GPL-3.0-or-later. Prebuilt register handlers selected by FCEUX's switch.
 * Fetch, cycles, mapper IRQ and sound hooks remain in the original loop. */
#include <stddef.h>
#include "cache.h"
static void (*cj_nes_handlers[10])(void *,void *);
extern "C" int console_jit_init(uintptr_t base){
 if(!cj_init(base))return 0;
 const unsigned src[]={offsetof(X6502,A),offsetof(X6502,X),offsetof(X6502,A),offsetof(X6502,Y),offsetof(X6502,S),offsetof(X6502,X),offsetof(X6502,X),offsetof(X6502,Y),offsetof(X6502,X),offsetof(X6502,Y)};
 const unsigned dst[]={offsetof(X6502,X),offsetof(X6502,A),offsetof(X6502,Y),offsetof(X6502,A),offsetof(X6502,X),offsetof(X6502,S),offsetof(X6502,X),offsetof(X6502,Y),offsetof(X6502,X),offsetof(X6502,Y)};
 for(unsigned i=0;i<10;i++){
  uint32_t *code=cj_code+i*32;
  unsigned words=cj_emit(code,src[i],dst[i],i<6?0:i<8?1:-1,8,i==5?0:1,offsetof(X6502,P),0,0);
  cj_commit(code,words);
  cj_nes_handlers[i]=(void(*)(void*,void*))code;
 }
 return 1;
}
