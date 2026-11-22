"""Part 1: scene windows from per-scene voice durations -> p1timing.js + starts json. Usage: durations.json out.js starts.json"""
import json, sys
d = json.load(open(sys.argv[1])); ids = [f"s{i}" for i in range(1, 12)]
GAP, PRE, TAIL = 0.4, 0.2, 1.6
S = [["s0", 0, 0.75]]; starts = {}; t = 0.75
for i, k in enumerate(ids):
    starts[k] = t; a = 0.75 if k == "s1" else t - PRE
    S.append([k, round(a, 3), None]); t += d[k] + GAP
for i in range(1, len(S)):
    S[i][2] = round(S[i+1][1] if i+1 < len(S) else starts[S[i][0]] + d[S[i][0]] + TAIL, 3)
dur = S[-1][2]
open(sys.argv[2], "w").write("window.P1=" + json.dumps({"S": S, "dur": dur}) + ";\n")
json.dump(starts, open(sys.argv[3], "w")); print(S, dur)
