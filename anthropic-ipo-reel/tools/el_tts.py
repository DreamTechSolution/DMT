"""ElevenLabs TTS per section, with previous/next text for natural continuity.
Usage: python3 el_tts.py sections.json VOICE_ID out_dir
The API key is injected by the network proxy (header xi-api-key)."""
import json, sys, os, subprocess, urllib.request
secs, voice, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True); durs = {}
for i, s in enumerate(secs):
    body = {"text": s["text"], "model_id": "eleven_v3", "language_code": "it",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.3}}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), headers={"xi-api-key": "proxy-injected", "Content-Type": "application/json"})
    p = f"{out}/{s['id']}.mp3"; open(p, "wb").write(urllib.request.urlopen(req, timeout=120).read())
    # trim leading/trailing silence so timing follows the actual speech
    q = f"{out}/{s['id']}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-af",
        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
        "-ar", "48000", "-ac", "2", q], check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", q],
                             capture_output=True, text=True).stdout); durs[s["id"]] = d
    print(s["id"], round(d, 2), flush=True)
json.dump(durs, open(f"{out}/durations.json", "w"), indent=1)
