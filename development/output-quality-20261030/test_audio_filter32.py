"""Check quantized response, gain, symmetry and fixed-point product bounds."""
from pathlib import Path
import sys,cmath,math
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from generate_audio_filter32 import coefficients,CLOCKS,TAPS
for name,clock in CLOCKS.items():
    h=coefficients(clock);dc=sum(h)
    def db(freq):return 20*math.log10(max(1e-12,abs(sum(c*cmath.exp(-2j*math.pi*freq*k/clock)for k,c in enumerate(h)))/dc))
    assert len(h)==668 and len(h)%4==0 and h==h[::-1]
    assert dc==1<<20
    assert max(abs(c)*32767 for c in h)<2**31
    assert max(abs(db(f)) for f in range(0,8001,250))<0.8
    # Dense near the alias boundary, sampled across the remaining stopband.
    stop=max(db(f) for f in [*range(16000,64001,250),*[clock*i/2048 for i in range(74,1025)]])
    assert stop < -48,(name,stop)
    print(f'PASS {name}: unity DC; passband 0-8 kHz within 0.8 dB; stopband {stop:.2f} dB; safe products')
