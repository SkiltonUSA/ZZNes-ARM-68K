"""Isolated noise synthesis optimisation; retain every sample and timer event."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
def prepare(core):
    path=core/'sound.cpp';source=path.read_text()
    begin=source.index(' if(PSG[0xE]&0x80)',source.index('static void RDoNoise(void)\n{'))
    end=source.index(' ChannelBC[3]=SOUNDTS;',begin)
    original=source[begin:end]
    assert original.count('wlcount[3]--;')==2 and original.count('nreg&=0x7fff;')==2
    replacement=''' if(SOUNDTS>ChannelBC[3])
  fc_audio_noise_span(WaveHi+ChannelBC[3],SOUNDTS-ChannelBC[3],amptab[0],
   PAL?NoiseFreqTablePAL[PSG[0xE]&15]:NoiseFreqTableNTSC[PSG[0xE]&15],
   (PSG[0xE]&0x80)?8:13,&wlcount[3],&nreg);
'''
    source=source[:begin]+replacement+source[end:]
    path.write_text('#include "audio_noise.h"\n'+source)
    shutil.copy2(ROOT/'development/noise-spans-20261111/audio_noise.h',core/'audio_noise.h')
