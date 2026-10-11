import numpy as np, soundfile as sf, json
import os
LG=os.environ.get('RT_LANG','en')
TM=json.load(open('timing_bn.json' if LG=='bn' else 'timing.json')); VO=TM[-1]['end']; TOT=VO+20
SR=44100; n=int(TOT*SR); t=np.arange(n)/SR
def f(m): return 440*2**((m-69)/12)
chords=[[57,60,64],[53,57,60],[48,52,55,60],[55,59,62]]  # Am F C G
pad=np.zeros(n); arp=np.zeros(n)
CL=8.0
for k in range(int(TOT/CL)+1):
    ch=chords[k%4]; s=int(k*CL*SR); e=min(n,int((k+1)*CL*SR+1.5*SR))
    if s>=n: break
    tt=np.arange(e-s)/SR
    env=np.minimum(1,tt/2.0)*np.minimum(1,np.maximum(0,(CL+1.5-tt)/2.0))
    for m in ch:
        for h,amp in ((1,1),(2,0.3),(3,0.12)):
            pad[s:e]+=amp*env*np.sin(2*np.pi*f(m-12)*h*tt+0.3*np.sin(2*np.pi*0.2*tt))
    # soft plucked arpeggio
    for j in range(8):
        m=ch[j%len(ch)]+ (12 if j%4==3 else 0)
        ps=s+int(j*1.0*SR); pe=min(n,ps+int(1.6*SR))
        if ps>=n: break
        pt=np.arange(pe-ps)/SR
        arp[ps:pe]+=np.exp(-pt*3.2)*(np.sin(2*np.pi*f(m)*pt)+0.25*np.sin(2*np.pi*f(m)*2*pt))
mus=0.05*pad/len(chords[0])+0.035*arp
# lift for the end screen, sting at the end of the narration
lift=np.clip((t-VO+0.5)/1.5,0,1)
mus*=1+1.6*lift
ss=int(VO*SR); st=np.arange(int(3*SR))/SR
sting=sum(np.exp(-st*1.5)*np.sin(2*np.pi*f(m)*st) for m in (57,64,69,72))*0.06
mus[ss:ss+len(st)]+=sting[:max(0,min(len(st),n-ss))]
# fade in/out
mus*=np.clip(t/2,0,1)*np.clip((TOT-t)/3,0,1)
sf.write('music_bn.wav' if LG=='bn' else 'music.wav',np.stack([mus,mus],1).astype(np.float32),SR)
print(TOT)
