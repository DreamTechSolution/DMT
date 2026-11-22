"""Build the audio mix for one video using the same timing rules as engine.js.
Usage: python3 tools/build_mix.py <serie_dir> <video_n> ORDER(comma) [ID:localPopSeconds ...]
e.g. python3 tools/build_mix.py serie05 1 I,A,B,C,H A:.3 B:2.1
Writes <serie_dir>/tmp_mix<n>.wav and prints the duration."""
import sys, os, json, subprocess, tempfile
sd, n, order = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
if order[0] == 'I' and len(order) > 1: order = [order[1], 'I'] + order[2:]  # hook first, same rule as engine.js
pops_local = {a.split(':')[0]: float(a.split(':')[1]) for a in sys.argv[4:]}
d = json.load(open(os.path.join(sd, f'voce{n}', 'durations.json')))
LEAD, GAP, PRE, TAIL = .35, .45, .25, 1.6; W = {}; st = {}; t = LEAD
for i, k in enumerate(order):
    st[k] = t; W[k] = [0 if i == 0 else t - PRE, None]; t += d[k] + GAP
for i, k in enumerate(order):
    W[k][1] = W[order[i + 1]][0] if i + 1 < len(order) else st[k] + d[k] + TAIL
dur = W[order[-1]][1]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tmp = tempfile.mkdtemp()
json.dump(st, open(f'{tmp}/st.json', 'w'))
json.dump({'dur': dur, 'cuts': [W[k][0] for k in order[1:]], 'pops': [.4] + [W[k][0] + v for k, v in pops_local.items()]}, open(f'{tmp}/cfg.json', 'w'))
out = os.path.join(sd, f'tmp_mix{n}.wav')
subprocess.run(['python3', os.path.join(root, 'anthropic-ipo-reel/tools/mix.py'), os.path.join(sd, f'voce{n}'), f'{tmp}/st.json', str(dur), f'{tmp}/cfg.json',
                os.path.join(root, 'anthropic-ipo-reel/music.mp3'), out], check=True)
print('duration', dur)
