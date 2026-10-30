"""Isolated HQ FIR acceleration; default release synthesis stays unchanged."""
from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parents[1]

def prepare(core, stage):
    shutil.copy2(ROOT/'development/output-quality-20261030/audio_fir_neon.S',stage/'audio_fir_neon.S')
    p=core/'filter.cpp';s=p.read_text()
    declaration='''extern "C" unsigned db_neon_available(uint32*);
extern "C" void db_neon_snapshot(uint32*),db_neon_restore(const uint32*);
extern "C" void fc_audio_fir_neon(const int32*,const int32*,unsigned,int32*);
'''
    # platform.h defines uint32/int32, so declarations follow the include.
    s=s.replace('#include "platform.h"','#include "platform.h"\n'+declaration,1)
    marker='\tint32 count=0;'
    assert s.count(marker)==1
    s=s.replace(marker,marker+'''
    uint32 saved[66] __attribute__((aligned(16))),probe[4]={0};
    const unsigned simd=db_neon_available(probe);
    if(simd)db_neon_snapshot(saved);
''',1)
    for count,coeff in [('SQ2NCOEFFS','sq2coeffs'),('NCOEFFS','coeffs')]:
        old=f'''\t\t\tfor(c={count},S=&in[(x>>16)-{count}],D={coeff};c;c--,D++)
\t\t\t{{
\t\t\t\tacc+=(S[c]**D)>>6;
\t\t\t\tacc2+=(S[1+c]**D)>>6;
\t\t\t}}'''
        assert s.count(old)==1,(count,'FIR shape changed')
        new=f'''            if(simd){{
                int32 sums[2];
                fc_audio_fir_neon(&in[x>>16],{coeff},{count},sums);
                acc=sums[0];acc2=sums[1];
            }}else{{
{old}
            }}'''
        s=s.replace(old,new)
    marker='\treturn(count);\n}\n\nvoid MakeFilters'
    assert s.count(marker)==1
    s=s.replace(marker,'    if(simd)db_neon_restore(saved);\n'+marker)
    p.write_text(s)

def prepare_clear(core, stage):
    shutil.copy2(ROOT/'development/output-quality-20261030/audio_clear.S',stage/'audio_clear.S')
    p=core/'sound.cpp';s=p.read_text()
    old='memset(WaveHi+left,0,sizeof(WaveHi)-left*sizeof(uint32));'
    assert s.count(old)==1
    s='extern "C" void fc_audio_clear_words(void*,unsigned);\n'+s
    s=s.replace(old,'fc_audio_clear_words(WaveHi+left,sizeof(WaveHi)/sizeof(WaveHi[0])-left);')
    p.write_text(s)

def prepare_square(core):
    shutil.copy2(ROOT/'development/output-quality-20261030/audio_square.h',core/'audio_square.h')
    p=core/'sound.cpp';s=p.read_text()
    begin=s.index('   while(V>0)\n',s.index('static INLINE void RDoSQ(int x)'))
    end=s.index('\n   RectDutyCount[x]=currdc;',begin)
    s=s[:begin]+'   fc_audio_square_span(D,V,amp,rthresh,cf,&rc,&currdc);\n'+s[end:]
    p.write_text('#include "audio_square.h"\n'+s)

def prepare_filter32(core):
    from generate_audio_filter32 import render
    (core/'audio_filter32.h').write_text(render())
    p=core/'filter.cpp';s=p.read_text()
    s=s.replace('#include "fcoeffs.h"','#include "fcoeffs.h"\n#include "audio_filter32.h"')
    s=s.replace('static int32 coeffs[NCOEFFS];','static int32 coeffs[FC_AUDIO_32_TAPS];\nstatic unsigned hq_taps=NCOEFFS;')
    begin=s.index('int32 NeoFilterSound(');end=s.index('void MakeFilters(',begin)
    # Only quality-1 tap references; SQ2NCOEFFS remains the quality-2 contract.
    import re
    s=s[:begin]+re.sub(r'\bNCOEFFS\b','hq_taps',s[begin:end])+s[end:]
    s=s.replace('  nco=NCOEFFS;','  nco=rate==32000?FC_AUDIO_32_TAPS:NCOEFFS;\n\n hq_taps=nco;')
    old='tmp=tabs[(PAL?1:0)|(rate==48000?2:0)|(rate==96000?4:0)];'
    assert s.count(old)==1
    s=s.replace(old,'tmp=rate==32000?(PAL?fc_audio_32_pal:fc_audio_32_ntsc):tabs[(PAL?1:0)|(rate==48000?2:0)|(rate==96000?4:0)];')
    s=s.replace('for(x=0;x<NCOEFFS>>1;x++)\n   coeffs[x]=coeffs[NCOEFFS-1-x]=tmp[x];','for(x=0;x<hq_taps>>1;x++)\n   coeffs[x]=coeffs[hq_taps-1-x]=tmp[x];')
    p.write_text(s)
