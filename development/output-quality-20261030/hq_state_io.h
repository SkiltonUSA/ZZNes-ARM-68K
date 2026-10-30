/* GPL-3.0-or-later. Preserve the synthesis mode encoded by each state.
 * Validate the full envelope and mode-specific payload before switching modes.
 * v1 is the original LQ layout; v2 appends HQ FIR history and phase. */
static unsigned state_payload(uint8 *p,int mode,bool hq){unsigned n=0;
 const unsigned count=sizeof(state_groups)/sizeof(*state_groups)-(hq?0:2);
 for(unsigned i=0;i<count;i++){
  unsigned k=state_table(state_groups[i],p?p+n:nullptr,mode);
  if(k>122880-n)return 122881;n+=k;
 }return n;
}
unsigned fc_state_store(uint8 *p,unsigned capacity){
 if(!loaded||!p)return 0;const bool hq=FSettings.soundq==1;
 unsigned n=state_payload(nullptr,0,hq);
 if(n>122848||capacity<n+32)return 0;
 FCEUPPU_SaveState();FCEUSND_SaveState();if(state_pre)state_pre();
 state_payload(p+32,0,hq);if(state_post)state_post();
 memcpy(p,"ZZS1",4);state_put(p+4,hq?2:1);
 state_put(p+8,state_rom_hash);state_put(p+12,state_rom_size);
 state_put(p+16,n);state_put(p+20,state_hash(p+32,n));
 state_put(p+24,hq?0x20261030u:0x20261011u);state_put(p+28,PAL);
 return n+32;
}
void FCEUI_SetSoundQuality(int quality);
int fc_state_load(const uint8 *p,unsigned n){
 if(!loaded||!p||n<32||n>122880||memcmp(p,"ZZS1",4))return 0;
 const bool hq=state_get(p+4)==2&&state_get(p+24)==0x20261030u;
 const bool legacy=state_get(p+4)==1&&state_get(p+24)==0x20261011u;
 if((!hq&&!legacy)||state_get(p+8)!=state_rom_hash||state_get(p+12)!=state_rom_size||
 state_get(p+16)!=n-32||state_get(p+20)!=state_hash(p+32,n-32)||
 state_get(p+28)!=PAL||state_payload(nullptr,0,hq)!=n-32)return 0;
 // Rebuild the mode's tables and callbacks before restoring saved counters.
 // No fractional counter conversion or guessed FIR history for legacy saves.
 FCEUI_SetSoundQuality(hq?1:0);
 FC_HQ_ClearTail();
 state_payload((uint8 *)p+32,1,hq);
 if(GameStateRestore)GameStateRestore(22020);
 FCEUPPU_LoadState(22020);FCEUSND_LoadState(22020);
 samples=nonzero=0;return 1;
}
