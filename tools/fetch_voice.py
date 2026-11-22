"""Download Higgsfield voice clips, trim silence, speed x1.12, write durations + dursN.js.
Usage: python3 tools/fetch_voice.py <serie_dir> <video_n> ID=URL [ID=URL ...]
The intro 'I' is copied from serie01/voce1/I.wav automatically."""
import sys, os, json, subprocess, shutil, urllib.request, tempfile
sd, n = sys.argv[1], sys.argv[2]; vd = os.path.join(sd, f'voce{n}'); os.makedirs(vd, exist_ok=True)
for arg in sys.argv[3:]:
    k, url = arg.split('=', 1); tmp = tempfile.mktemp(suffix='.mp3'); urllib.request.urlretrieve(url, tmp)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', tmp, '-af',
        'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo=1.12',
        '-ar', '48000', '-ac', '2', os.path.join(vd, f'{k}.wav')], check=True); os.remove(tmp)
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
shutil.copy(os.path.join(root, 'serie01/voce1/I.wav'), os.path.join(vd, 'I.wav'))
d = {}
for f in sorted(os.listdir(vd)):
    if f.endswith('.wav'):
        d[f[:-4]] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(vd, f)], capture_output=True, text=True).stdout)
json.dump(d, open(os.path.join(vd, 'durations.json'), 'w'), indent=1)
open(os.path.join(sd, f'durs{n}.js'), 'w').write('window.DURS=' + json.dumps(d) + ';')
print({k: round(v, 2) for k, v in d.items()}, 'total', round(sum(d.values()), 1))
