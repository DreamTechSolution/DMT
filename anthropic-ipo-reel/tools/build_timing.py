"""Build ep2/timing.js from per-section voice durations.
Scene windows follow the voice; cues authored in T0 are remapped proportionally."""
import json, re, sys
durs = json.load(open(sys.argv[1])); out = sys.argv[2]
order = ["A","I","B","C","D","E","F","G","H"]  # hook first, signature intro second
LEAD, GAP, TAIL = 0.35, 0.45, 1.6      # silence before first word, between sections, after last
# T0 windows/cues as authored (without intro shift)
T0 = {"A":[0,5.2],"B":[5.2,22],"C":[22,38],"D":[38,52],"E":[52,69],"F":[69,89],"G":[89,99],"H":[99,105.5]}
cue0 = dict(Ab=1.6,Ac=3.0,Bbar=8.5,B21=12.5,Bc=15.5,Bd=16.5,Be=19,Crev=25.5,Cx=29.5,Closs=31,Cacc=33.5,
 Dn=40.5,Dlock=44,Dq=47,Ephone=53,Eq=57.5,Emeter=60,Ecards=62.5,Ec2=64.5,Ec3=66.5,
 F1=70.5,F2=72,F3=73.5,F4=75,Flock=77.5,Fd=85.5,Gscale=89.5,Gb=93.5,Gc=96.5,Ha=99.5,Htype=101.5)
T, starts, t = {}, {}, LEAD
for k in order:
    starts[k] = t                       # first word of section k
    end = t + durs[k]
    a = 0 if k == order[0] else t - 0.25     # cut slightly before the voice
    T[k] = [round(a, 3), None]; t = end + GAP
for i, k in enumerate(order):
    T[k][1] = round(T[order[i+1]][0] if i+1 < len(order) else starts[k] + durs[k] + TAIL, 3)
cue = {}
for c, v in cue0.items():
    sc = next(k for k, (a, b) in T0.items() if a <= v < b)
    a0, b0 = T0[sc]; a1, b1 = T[sc]
    cue[c] = round(a1 + (v - a0) * (b1 - a1) / (b0 - a0), 3)
json.dump({"T": T, "starts": starts}, open(out.replace(".js", ".json"), "w"), indent=1)
T["cue"] = cue
open(out, "w").write("window.TIMING=" + json.dumps(T) + ";\n")
print(json.dumps(T, indent=0)[:600])
