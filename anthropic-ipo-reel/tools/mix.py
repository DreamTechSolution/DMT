"""Place per-section voice files at given start times, add SFX + looped/ducked music, write final mix.
Usage: mix.py voice_dir starts.json(ids->start) dur sfx_cfg.json music.mp3 out.wav"""
import json, sys, subprocess
vd, starts, dur, cfg, music, out = sys.argv[1], json.load(open(sys.argv[2])), float(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6]
tmp = out + ".sfx.wav"
subprocess.run(["python3", __file__.replace("mix.py", "../soundtrack.py"), tmp], check=True,
               env={"CFG": open(cfg).read(), "SFX_ONLY": "1", "PATH": "/usr/bin:/bin"})
ids = list(starts); inp = []; f = []
for i, k in enumerate(ids):
    inp += ["-i", f"{vd}/{k}.wav"]; ms = int(starts[k] * 1000)
    f.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]")
n = len(ids); inp += ["-i", music, "-i", music, "-i", music, "-i", tmp]
f.append("".join(f"[v{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0:duration=longest,apad=whole_dur={dur},highpass=f=70,"
         "acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,loudnorm=I=-15:TP=-1.5,aresample=48000,asplit=2[vo][sc]")
f.append(f"[{n}:a][{n+1}:a]acrossfade=d=3[m01];[m01][{n+2}:a]acrossfade=d=3,aresample=48000,atempo=0.95,atrim=0:{dur},"
         f"afade=t=out:st={dur-1.8}:d=1.8,volume=0.40[mu]")
f.append("[mu][sc]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=350[duck]")
f.append(f"[{n+3}:a]volume=0.3[fx];[duck][fx][vo]amix=inputs=3:normalize=0:duration=longest,atrim=0:{dur},alimiter=limit=0.95[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(f), "-map", "[o]", "-ac", "2", "-ar", "48000", out], check=True)
print("mixed", out, dur)
