"""Opt-in eight-event muted noise advancement; preserve the audible renderer."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
def prepare(core):
    path=core/'sound.cpp';source=path.read_text()
    old='fc_audio_noise_span(WaveHi+ChannelBC[3]'
    if source.count(old)!=1:
        raise ValueError('Muted noise experiment requires the exact noise-span overlay')
    source=source.replace(old,'fc_audio_noise_muted_span(WaveHi+ChannelBC[3]',1)
    path.write_text('#include "audio_noise_muted.h"\n'+source)
    shutil.copy2(ROOT/'development/noise-muted-20261115/audio_noise_muted.h',core/'audio_noise_muted.h')
