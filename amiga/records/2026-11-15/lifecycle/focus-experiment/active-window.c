#include <proto/exec.h>
#include <proto/intuition.h>
#include <intuition/intuitionbase.h>
#include <stdio.h>
struct IntuitionBase *IntuitionBase;
int main(void){
 char title[160];unsigned i=0;ULONG token;struct Window *w;
 IntuitionBase=(struct IntuitionBase*)OpenLibrary("intuition.library",39);
 if(!IntuitionBase)return 20;
 token=LockIBase(0);w=IntuitionBase->ActiveWindow;
 if(w&&w->Title)while(i<sizeof(title)-1&&w->Title[i]){title[i]=w->Title[i];i++;}
 title[i]=0;UnlockIBase(token);
 printf("ACTIVE_WINDOW %s\n",title);CloseLibrary((struct Library*)IntuitionBase);return w?0:5;
}
