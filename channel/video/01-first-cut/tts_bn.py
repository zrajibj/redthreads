import json, numpy as np, soundfile as sf, sherpa_onnx
from tr_bn import BEATS
M='/tmp/claude-0/-home-claude-redthreads/cb7bab53-e637-59f3-9012-615456b3612a/scratchpad/models/vits-coqui-bn-custom_female/'
tts=sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=M+'model.onnx',tokens=M+'tokens.txt'),num_threads=4)))
toks=set(l.split(' ')[0] for l in open(M+'tokens.txt',encoding='utf-8').read().split('\n') if l)
SR=tts.sample_rate; out=[]; meta=[]; t=0.0
def sil(s): return np.zeros(int(SR*s),dtype=np.float32)
for bi,sents in enumerate(BEATS):
    start=t; caps=[]
    for s in sents:
        if s=='/':
            out.append(sil(0.4)); t+=0.4; continue
        say=s.replace('"','').replace(':',',').replace(';',',')
        say=''.join(ch for ch in say if ch in toks or ch==' ')
        a=np.array(tts.generate(say,sid=0,speed=1.0).samples,dtype=np.float32)
        nz=np.where(np.abs(a)>0.01)[0]
        if len(nz): a=a[max(0,nz[0]-200):nz[-1]+400]
        caps.append([round(t,3),round(t+len(a)/SR,3),s]); out.append(a); t+=len(a)/SR
        out.append(sil(0.25)); t+=0.25
    extra=0.9 if bi in (13,16) else 0.45
    out.append(sil(extra)); t+=extra
    meta.append({'beat':bi+1,'start':round(start,3),'end':round(t,3),'caps':caps}); print(bi+1,round(start,1),round(t,1),flush=True)
sf.write('vo_bn.wav',np.concatenate(out),SR)
json.dump(meta,open('timing_bn.json','w'),indent=1,ensure_ascii=False)
missing=set(ch for b in BEATS for s in b for ch in s if ch not in toks and ch not in ' "/')
print('dropped chars',missing)
