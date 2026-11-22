"""Generate a voiceover section by section with OmniVoice, cloning a reference voice.
Usage: python gen_voice.py sections.json ref.wav "ref transcript" out_dir
sections.json: [{"id": "A", "text": "..."}, ...]
Writes out_dir/<id>.wav and out_dir/durations.json
"""
import json, sys, os, torch
from omnivoice.models.omnivoice import OmniVoice
from omnivoice.utils.audio import save_audio
from omnivoice.utils.dtype import tts_dtype_name

secs, ref, ref_text, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
os.makedirs(out, exist_ok=True)
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cpu",
                                  dtype=getattr(torch, tts_dtype_name("cpu")), allow_tokenizer_fallback=True)
prompt = model.create_voice_clone_prompt(ref_audio=ref, ref_text=ref_text) if hasattr(model, "create_voice_clone_prompt") else None
durs = {}
for s in json.load(open(secs)):
    kw = dict(text=s["text"], language="it", num_step=48, seed=7)
    if prompt is not None: kw["voice_clone_prompt"] = prompt
    else: kw.update(ref_audio=ref, ref_text=ref_text)
    a = model.generate(**kw)[0]
    p = f"{out}/{s['id']}.wav"; save_audio(p, a, model.sampling_rate)
    durs[s["id"]] = a.shape[-1] / model.sampling_rate
    print(s["id"], round(durs[s["id"]], 2), flush=True)
json.dump(durs, open(f"{out}/durations.json", "w"), indent=1)
