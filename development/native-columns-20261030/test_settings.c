#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define UI_CONFIG_PREFIX "ZZNESUI"
#include "ui_model.h"
static unsigned fc_windowed,fc_scanlines,fc_fps,fc_optimise;
static const char*rom_path;static int player_muted;
#include PLAYER_SESSION
int main(void){
 for(unsigned choice=0;choice<4;choice++){
  struct ui_model a={0},b={0};ui_defaults(&a);a.smooth=choice;FILE*f=tmpfile();assert(f&&ui_write(f,&a));rewind(f);
  int ok=ui_read(f,&b);assert(ok==(choice<3));if(ok)assert(b.smooth==choice);fclose(f);ui_dispose(&a);ui_dispose(&b);
  f=fopen("columns.session","w");assert(f);fprintf(f,"ZZSESSION1\n%u 0 0 0\n726f6d2e6e6573\n7374617465\n2d\nDISPLAY 3 2 0 1\n",choice<<8);fclose(f);
  assert(fc_session("columns.session")== (int)(choice<3));
 }
 remove("columns.session");puts("PASS Sharp/Smooth/Native settings and session round trips; invalid scale rejected");
}
