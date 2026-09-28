"""Montează intro + rundele disponibile într-un clip de previzualizare (voce + muzică)."""
import subprocess, os, json, sys
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "canal", "imagini")
OVL = os.path.join(IMG, "suprapuneri")
cfg = json.load(open(sys.argv[1]))
TMP = cfg["tmp"]; os.makedirs(TMP, exist_ok=True)
V = "scale=1920:1080,fps=30,format=yuv420p,setsar=1"
RLEN = 24.5
def run(args): subprocess.run([FF, "-loglevel", "error", "-y"] + args, check=True)

# intro (3 s)
run(["-i", cfg["intro"], "-loop", "1", "-framerate", "30", "-i", f"{OVL}/intro-who-said-moo.png",
     "-filter_complex", f"[0:v]trim=0:3,setpts=PTS-STARTPTS,{V}[i];[1:v]format=rgba,scale=1920:1080[t];[i][t]overlay=0:0:shortest=1:enable='lt(t,1.3)',format=yuv420p",
     "-t", "3", "-an", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", f"{TMP}/00.mp4"])
segs = [f"{TMP}/00.mp4"]
for r in cfg["rounds"]:
    n = r["nr"]; d = f"{IMG}/runda-{n:02d}"
    ins = []
    for f, t in [("1-round.png", 2), ("2-silueta.png", 8)] + [(f"3-numaratoare-{k}.png", 1) for k in range(5, 0, -1)]:
        ins += ["-loop", "1", "-framerate", "30", "-t", str(t), "-i", f"{d}/{f}"]
    ins += ["-i", r["clip"], "-loop", "1", "-framerate", "30", "-i", f"{OVL}/animale/{r['label']}.png"]
    fc = "".join(f"[{i}:v]{V}[s{i}];" for i in range(7)) + "".join(f"[s{i}]" for i in range(7)) + \
         "concat=n=7:v=1:a=0,fps=30,settb=AVTB[sil];" + \
         f"[7:v]trim=0:10,setpts=PTS-STARTPTS,{V},settb=AVTB[c];[sil][c]xfade=transition=fade:duration=0.5:offset=14.5[q];" + \
         "[8:v]format=rgba,scale=1920:1080[nm];" + \
         "[q][nm]overlay=0:0:shortest=1:enable='gte(t,15.2)',format=yuv420p"
    out = f"{TMP}/{n:02d}.mp4"
    run(ins + ["-filter_complex", fc, "-t", str(RLEN), "-an", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", out])
    segs.append(out)
open(f"{TMP}/list.txt", "w").write("".join(f"file '{s}'\n" for s in segs))
run(["-f", "concat", "-safe", "0", "-i", f"{TMP}/list.txt", "-c", "copy", f"{TMP}/video.mp4"])
total = 3 + RLEN * len(cfg["rounds"])

ev = [(cfg["voice"]["P-00-intro-1"], 0.1, 0, None), (cfg["voice"]["P-00-intro-2"], 1.35, 2, None)]
dips = []
for k, r in enumerate(cfg["rounds"]):
    R = 3 + RLEN * k; v = r["voice"]
    ev += [(v["round"], R + (1.15 if k == 0 else 0.2), r.get("round_gain", 0), None),
           (v["question"], R + 8.4, r.get("question_gain", 0), None),
           (cfg["voice"]["N-00-countdown"], R + 10, 0, None)]
    if "sfx" in r:  # sunet real (Pixabay): 2x pe siluetă + 1x după răspuns; sunetul clipului e oprit
        ev += [(r["sfx"], R + 2.6, r.get("sfx_gain", 0), r["s1"]), (r["sfx"], R + 5.5, r.get("sfx_gain", 0), r["s2"]),
               (r["sfx"], R + 16.6, r.get("sfx_gain", 0), r["s3"])]
    else:           # provizoriu: sunetul din clipul Higgsfield
        ev += [(r["clip"], R + 2.6, 6, r["sound"]), (r["clip"], R + 5.5, 6, r["sound"]), (r["clip"], R + 14.5, 4, None)]
    ev += [
           (v["answer"], R + 15.0, r.get("answer_gain", 0), None),
           (v["praise"], R + 21.6, 0, None)]
    dips.append(R)
ins = []; fc = ""; labels = []
for i, (f, st, g, tr) in enumerate(ev):
    ins += ["-i", f]
    t = f"atrim={tr[0]}:{tr[1]},asetpts=PTS-STARTPTS," if tr else ""
    ms = int(st * 1000)
    fc += f"[{i}:a]{t}aformat=sample_rates=48000:channel_layouts=stereo,volume={g}dB,adelay={ms}|{ms}[e{i}];"
    labels.append(f"[e{i}]")
def T(a, b, c, d): return f"clip((t-{a})/({b}-{a}),0,1)*clip(({d}-t)/({d}-{c}),0,1)"
env = "0.1"
for R in dips:
    env += f"-0.1*{T(R+2.3, R+2.6, R+11.2, R+11.6)}-0.05*{T(R+11.6, R+12, R+14.3, R+14.6)}-0.07*{T(R+14.3, R+14.6, R+21.2, R+21.5)}+0.06*{T(R+21.3, R+21.7, R+23.5, R+24.2)}"
env = f"min(t/1,1)*({env})*clip(({total}-t)/2,0,1)"
mi = len(ev)
ins += ["-stream_loop", "-1", "-i", cfg["music"]]
fc += f"[{mi}:a]atrim=0:{total},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume='{env}':eval=frame[mu];"
fc += "".join(labels) + f"[mu]amix=inputs={len(labels)+1}:normalize=0:duration=longest,atrim=0:{total},volume=-3dB,alimiter=limit=0.89[a]"
run(ins + ["-filter_complex", fc, "-map", "[a]", "-c:a", "aac", "-b:a", "160k", f"{TMP}/audio.m4a"])
run(["-i", f"{TMP}/video.mp4", "-i", f"{TMP}/audio.m4a", "-map", "0:v", "-map", "1:a", "-c", "copy", "-shortest", "-movflags", "+faststart", cfg["out"]])
print("gata:", cfg["out"], "durata:", total)
