import re, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
S='/tmp/claude-0/-home-claude-redthreads/cb7bab53-e637-59f3-9012-615456b3612a/scratchpad/'
md=open('/home/claude/redthreads/channel/scripts/01-why-changing-the-government-changes-so-little.md').read()
sec=md.split('## 1.')[1].split('## 2.')[0]
beats=re.findall(r'\*\*(\d:\d\d)\*\* (.+)',sec)
k=Kokoro(S+'models/kokoro-v1.0.onnx',S+'models/voices-v1.0.bin')
SR=24000; out=[]; meta=[]; t=0.0
def sil(s): return np.zeros(int(SR*s),dtype=np.float32)
for bi,(_,txt) in enumerate(beats):
    txt=txt.replace('*','')
    parts=[p.strip() for p in txt.split(' / ')]
    start=t; caps=[]
    for pi,p in enumerate(parts):
        # caption chunks = sentences
        sents=re.split(r'(?<=[.?!:])\s+(?=[A-Z"“])',p)
        for s in sents:
            say=s.replace('"','').replace('“','').replace('”','')
            a,sr=k.create(say,voice='am_michael',speed=0.94,lang='en-us')
            # trim edges
            nz=np.where(np.abs(a)>0.01)[0]
            if len(nz): a=a[max(0,nz[0]-240):nz[-1]+480]
            caps.append([round(t,3),round(t+len(a)/SR,3),s]); out.append(a); t+=len(a)/SR
            g=0.28; out.append(sil(g)); t+=g
        if pi<len(parts)-1:
            out.append(sil(0.45)); t+=0.45
    extra = 0.9 if bi in (13,16) else 0.5
    out.append(sil(extra)); t+=extra
    meta.append({'beat':bi+1,'start':round(start,3),'end':round(t,3),'caps':caps})
    print(bi+1,round(start,2),round(t,2),flush=True)
sf.write('vo.wav',np.concatenate(out),SR)
json.dump(meta,open('timing.json','w'),indent=1)
