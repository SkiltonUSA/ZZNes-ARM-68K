#include "ui_model.h"
#include <assert.h>
static struct ui_model a,b;
int main(void){FILE *f;char quoted[1100];unsigned i;ui_defaults(&a);
 assert(ui_add(&a,"SD032G:ROMs/A *\"quoted\" game.nes")==0);a.entry[0].favorite=1;a.entry[0].played=17;a.clock=18;a.theme=4;a.vmask=2;a.slot=4;
 assert(ui_add(&a,a.entry[0].path)==0);assert(a.count==1);assert(ui_add(&a,"bad\nfile")==-1);
 for(i=1;i<UI_MAX;i++){char p[60];snprintf(p,sizeof(p),"ROMs/game-%u.nes",i);assert(ui_add(&a,p)==(int)i);}assert(ui_add(&a,"too-many.nes")==-1);
 f=tmpfile();assert(f);assert(ui_write(f,&a));rewind(f);assert(ui_read(f,&b));assert(!memcmp(&a,&b,sizeof(a)));fclose(f);
 assert(ui_quote(quoted,sizeof(quoted),"A *\"B\".nes"));assert(!strcmp(quoted,"\"A ***\"B*\".nes\""));assert(!ui_quote(quoted,3,"toolong"));
 f=tmpfile();fputs("ZZNESUI1\n0 9 0 0 0 0 0 0\n",f);rewind(f);assert(!ui_read(f,&b));fclose(f);
 puts("PASS library limit, duplicate, favourites/history/settings round-trip, hostile paths, malformed preferences");
}
