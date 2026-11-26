/* Original fixtures: no game ROM data. */
#include "platform.h"
#include "core.h"
#include "cartridge.h"
#include "unif.h"
#include <cassert>
#include <vector>
#include <cstdlib>
extern unsigned fc_state_store(uint8*,unsigned);
extern int fc_state_load(const uint8*,unsigned);
static std::vector<uint8> image(unsigned id,unsigned sub,unsigned version){
 unsigned prg=id==0||id==3?32768:131072,chr=id==2||id==7?0:32768;if(id==0)chr=8192;
 std::vector<uint8> r(16+prg+chr,0);memcpy(r.data(),"NES\032",4);
 r[4]=prg/16384;r[5]=chr/8192;r[6]=id<<4;r[7]=(id&240)|(version?8:0);
 if(version){r[8]=sub<<4;r[11]=chr?0:7;}
 for(unsigned b=0;b<prg/8192;b++)memset(r.data()+16+b*8192,b,8192);
 for(unsigned b=0;b<chr/8192;b++)memset(r.data()+16+prg+b*8192,0x80+b,8192);
 return r;
}
static void append(std::vector<uint8>&r,const char*id,const uint8*p,unsigned n){
 r.insert(r.end(),id,id+4);for(unsigned i=0;i<4;i++)r.push_back(n>>(8*i));if(n)r.insert(r.end(),p,p+n);
}
static void parser(){
 auto r=image(7,2,1);struct fc_cartridge_info c;
 assert(fc_cartridge_parse(r.data(),r.size(),&c)&&c.mapper==7&&c.submapper==2&&c.vram==8192);
 for(unsigned field: {8u,10u,11u,12u,13u,14u,15u}){auto bad=r;bad[field]=255;assert(nes_cartridge(bad.data(),bad.size())<0);}
 auto exp=r;exp[4]=17<<2;exp[9]=15;assert(nes_cartridge(exp.data(),exp.size())==7);
 exp[4]=255;assert(nes_cartridge(exp.data(),exp.size())<0);
 auto extended=r;extended[9]=1;assert(nes_cartridge(extended.data(),extended.size())<0);
 auto upper=r;upper[8]|=1;assert(nes_cartridge(upper.data(),upper.size())<0);
 auto bad=r;bad[11]=0;assert(nes_cartridge(bad.data(),bad.size())<0);
 bad=r;bad[8]=3<<4;assert(nes_cartridge(bad.data(),bad.size())<0);
 r[12]=0;assert(!fc_rom_pal(r.data(),r.size(),"(Europe).nes"));r[12]=1;assert(fc_rom_pal(r.data(),r.size(),"(USA).nes"));
 r[12]=2;assert(fc_rom_pal(r.data(),r.size(),"(Europe).nes"));
 auto m78=image(78,3,1);assert(fc_cartridge_parse(m78.data(),m78.size(),&c)&&c.mirror==2);
 m78[8]=1<<4;assert(fc_cartridge_parse(m78.data(),m78.size(),&c)&&c.mirror==0);
 std::vector<uint8> u(32,0),out(800000);memcpy(u.data(),"UNIF",4);u[4]=7;
 const uint8 name[]="NES-ANROM";append(u,"MAPR",name,sizeof name);
 auto source=image(7,1,1);append(u,"PRG0",source.data()+16,source.size()-16);
 uint32 crc=fc_unif_crc(source.data()+16,source.size()-16);uint8 checksum[4];for(unsigned i=0;i<4;i++)checksum[i]=crc>>(8*i);
 append(u,"PCK0",checksum,4);unsigned count;assert(fc_unif_import(u.data(),u.size(),out.data(),out.size(),&count));
 assert(count==source.size()&&!memcmp(out.data(),source.data(),count));
 for(unsigned n: {0u,4u,31u,35u,(unsigned)u.size()-1})assert(!fc_unif_import(u.data(),n,out.data(),out.size(),&count));
 auto duplicate=u;append(duplicate,"MAPR",name,sizeof name);assert(!fc_unif_import(duplicate.data(),duplicate.size(),out.data(),out.size(),&count));
 u.back()^=1;assert(!fc_unif_import(u.data(),u.size(),out.data(),out.size(),&count));u.back()^=1;
 assert(!fc_unif_import(u.data(),u.size(),out.data(),16,&count));
 auto unknown=u;unknown[40]='?';assert(!fc_unif_import(unknown.data(),unknown.size(),out.data(),out.size(),&count));
 // Multiple ROM chips can appear out of order in the container. Require
 // contiguous chip IDs and check each checksum before concatenation.
 std::vector<uint8> multi(32,0);memcpy(multi.data(),"UNIF",4);multi[4]=7;
 append(multi,"MAPR",name,sizeof name);unsigned half=(source.size()-16)/2;
 append(multi,"PRG1",source.data()+16+half,half);append(multi,"PRG0",source.data()+16,half);
 crc=fc_unif_crc(source.data()+16+half,half);for(unsigned i=0;i<4;i++)checksum[i]=crc>>(8*i);
 append(multi,"PCK1",checksum,4);assert(fc_unif_import(multi.data(),multi.size(),out.data(),out.size(),&count));
 assert(count==source.size()&&!memcmp(out.data(),source.data(),count));
 auto hole=multi;hole[32+8+sizeof name+3]='2';assert(!fc_unif_import(hole.data(),hole.size(),out.data(),out.size(),&count));
 auto dup=multi;append(dup,"PRG1",source.data()+16,half);assert(!fc_unif_import(dup.data(),dup.size(),out.data(),out.size(),&count));
 multi.back()^=1;assert(!fc_unif_import(multi.data(),multi.size(),out.data(),out.size(),&count));
 puts("PASS NES 2.0 fields, exponent bounds, submappers, authoritative timing; UNIF board/length/CRC/duplicate checks");
}
int main(int argc,char**argv){
 if(argc==1){parser();return 0;}
 unsigned id=atoi(argv[1]),sub=atoi(argv[2]),version=atoi(argv[3]);auto r=image(id,sub,version);
 assert(nes_cartridge(r.data(),r.size())==(int)id);
 assert(!fc_init(r.data(),r.size()));
 unsigned data=id==11?0x21:id==66?0x21:0x12;
 // ROM value 0 at $8000: conflict variants must AND the register write to zero.
 unsigned conflicts=(version&&sub)?sub==2:(id==2||id==3||id==66);
 BWrite[0x8000](0x8000,data);unsigned expected=conflicts?0:data;
 if(id==2)assert(ARead[0x8000](0x8000)==(expected*2)%16);
 if(id==7)assert(ARead[0x8000](0x8000)==((expected&15)*4)%16);
 if(id==11)assert(ARead[0x8000](0x8000)==((expected&15)*4)%16);
 if(id==66)assert(ARead[0x8000](0x8000)==((expected>>4)*4)%16);
 if(id==3)assert(VPage[0][0]==0x80+(expected%4));
 if(id==11)assert(VPage[0][0]==0x80+((expected>>4)%4));
 if(id==66)assert(VPage[0][0]==0x80+(expected%4));
 if(id==7)for(unsigned i=0;i<4;i++)assert(vnapage[i]==NTARAM+((expected>>4)&1)*1024);
 std::vector<uint8> save(122880);unsigned n=fc_state_store(save.data(),save.size());assert(n);
 auto prg=ARead[0x8000](0x8000);auto chr=VPage[0][0];auto mirror=vnapage[0];
 // Write at a ROM address containing all ones to exercise state restoration.
 r[16+0x100]=255;BWrite[0x8100](0x8100,0x33);
 assert(fc_state_load(save.data(),n));assert(ARead[0x8000](0x8000)==prg&&VPage[0][0]==chr&&vnapage[0]==mirror);
 printf("PASS mapper %u NES%u sub%u: PRG/CHR banks, bus conflict and state restoration\n",id,version?2:1,sub);
}
