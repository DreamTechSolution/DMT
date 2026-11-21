# Original synthesized soundtrack: dark pulse bed + whoosh/impact on every cut.
import numpy as np, wave, sys
sr=48000; dur=35.0; n=int(sr*dur); t=np.arange(n)/sr
cuts=[1.6,3.4,6.3,9.4,12.0,15.4,17.4,23.0,25.4,27.6,31.2]
pops=[1.65,2.0,4.55,7.35,9.75,14.4,18.5,24.15,26.0,28.05,31.9]
out=np.zeros(n)
bpm=84; beat=60/bpm
# drone (Am-ish) with slow swell
for f,a in [(55,.22),(110,.10),(164.8,.05),(220,.035)]:
    out+=a*np.sin(2*np.pi*f*t+0.3*np.sin(2*np.pi*.1*t))
out*=np.clip(t/2,0,1)*(0.75+0.25*np.sin(2*np.pi*t/8))
# kick-ish pulse from 1.6s
for k in np.arange(1.6,34,beat):
    i=int(k*sr); L=int(.35*sr); tt=np.arange(L)/sr
    s=np.sin(2*np.pi*(45+80*np.exp(-tt*30))*tt)*np.exp(-tt*9)*.55
    out[i:i+L]+=s[:n-i]
# hats on off-beats
rng=np.random.default_rng(1)
for k in np.arange(1.6+beat/2,34,beat):
    i=int(k*sr); L=int(.06*sr); s=rng.standard_normal(L)*np.exp(-np.arange(L)/sr*60)*.06
    s=np.diff(np.concatenate([[0],s])); out[i:i+L]+=s[:n-i]
# whoosh into each cut
for c in cuts:
    L=int(.45*sr); i=int(c*sr)-L; tt=np.arange(L)/sr
    w=rng.standard_normal(L); w=np.convolve(w,np.ones(12)/12,'same')
    env=(tt/tt[-1])**2.5; out[i:i+L]+=w*env*.5
# pop/impact on text slams
for p in pops:
    i=int(p*sr); L=int(.25*sr); tt=np.arange(L)/sr
    s=(np.sin(2*np.pi*900*tt*np.exp(-tt*8))*np.exp(-tt*25)*.25+np.sin(2*np.pi*60*tt)*np.exp(-tt*14)*.5)
    out[i:i+L]+=s[:n-i]
# fade out
out*=np.clip((dur-t)/1.5,0,1)
out=out/np.max(np.abs(out))*0.89
st=np.stack([out,np.roll(out,90)],1)
with wave.open(sys.argv[1],'w') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((st*32767).astype('<i2').tobytes())
