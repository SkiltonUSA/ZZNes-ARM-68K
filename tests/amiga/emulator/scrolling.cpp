#include "platform.h"
#include "core.h"
#include <cassert>
#include <vector>
#include <fstream>
extern void fc_set_region(unsigned);
int main(int argc,char**argv){assert(argc==3||argc==4);fc_set_region(argc==4?1:0);std::ifstream f(argv[1],std::ios::binary);std::vector<uint8_t> r((std::istreambuf_iterator<char>(f)),{});assert(!fc_init(r.data(),r.size()));uint8_t prev[256]={0};unsigned shifts=0,resets=0;FILE*o=fopen(argv[2],"wb");assert(o);
for(unsigned frame=0;frame<96;frame++){assert(!fc_frame(0));if(frame>=16){bool shift=true,reset=true;for(unsigned x=16;x<208;x++){unsigned c=XBuf[40*256+x]&63;shift&=c==(prev[x+1]&63);reset&=c==(prev[x-7]&63);}if(frame>16){assert(shift||reset);shifts+=shift;resets+=reset;}fwrite(XBuf,1,61440,o);}memcpy(prev,XBuf+40*256,256);}fclose(o);assert(shifts>50&&resets>5);printf("PASS fine scroll: %u one-pixel transitions, %u eight-phase wraps\n",shifts,resets);}
