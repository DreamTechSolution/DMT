# Word-by-word check of new voice clips against the script.
# Usage (venv with faster-whisper): python tools/check_voice.py map.tsv   (TSV: dir, video, section, higgsfield file id, text)
# Prints OK or DIFF with the words that do not match. Whisper tends to "correct" words, so OK is necessary, not sufficient: listen to English names and acronyms.
import sys,subprocess,numpy as np,difflib,re,unicodedata,os,urllib.request
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
B="https://d8j0ntlcm91z4.cloudfront.net/user_3CU9WWB8j10xBgW5vzXZFWFrVTO/hf_20261122_"
NUM=re.compile(r'\d|^(uno|due|tre|quattro|cinque|sei|sette|otto|nove|dieci|venti|trenta|quaranta|cento|mila|mille|virgola|per)$|^(vent|trent|quarant|cinquant|sessant|settant|ottant|novant|duemila|cent|dodic|tredic|quattordic|quindic|sedic|diciass|diciott|dician|novemila|settemila)')
def norm(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.findall(r"[a-z0-9&]+",re.sub(r"[’'\-]"," ",s))
for line in open(sys.argv[1]):
    d,v,k,u,txt=line.rstrip('\n').split('\t'); w=f"{d}_{v}_{k}.wav"
    if not os.path.exists(w):
        urllib.request.urlretrieve(B+u+".mp3","t.mp3")
        subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-i","t.mp3","-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo=1.12","-ar","48000","-ac","2",w],check=True)
    a=subprocess.run(["ffmpeg","-v","error","-i",w,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout
    segs,_=m.transcribe(np.frombuffer(a,dtype=np.float32).copy(),language="it",beam_size=5,condition_on_previous_text=False)
    t=" ".join(s.text.strip() for s in segs); A,Bw=norm(txt),norm(t); bad=[]
    for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,A,Bw,autojunk=False).get_opcodes():
        if op!='equal':
            x=[q for q in A[i1:i2] if not NUM.search(q)]; y=[q for q in Bw[j1:j2] if not NUM.search(q)]
            if x or y: bad.append(f'"{" ".join(A[i1:i2])}"→"{" ".join(Bw[j1:j2])}"')
    print(("OK   " if not bad else "DIFF ")+f"{d} {v} {k} | "+("; ".join(bad) if bad else t[:90]),flush=True)
