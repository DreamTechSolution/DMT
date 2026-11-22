"""Apply atempo to every section wav in a dir and rewrite durations.json. Usage: speedup.py dir factor"""
import json, sys, subprocess, glob, os
d, f = sys.argv[1], sys.argv[2]; durs = json.load(open(f"{d}/durations.json")); out = {}
for k in durs:
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{d}/{k}.wav","-af",f"atempo={f}",f"{d}/{k}_f.wav"],check=True)
    os.replace(f"{d}/{k}_f.wav", f"{d}/{k}.wav")
    out[k] = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{d}/{k}.wav"],capture_output=True,text=True).stdout)
json.dump(out, open(f"{d}/durations.json","w"), indent=1); print({k: round(v,2) for k,v in out.items()}, round(sum(out.values()),1))
