"""Video 4: trailer de 5 s + intro + 20 runde (siluetă 5 s la primele 3, numărătoare 3-2-1, runda 10 = bonus) + final.

Folosire: monteaza_v4.py cfg.json   (cfg-ul îl face cfg_video04.py)
"""
import subprocess, os, json, sys, re
FF = __import__("imageio_ffmpeg").get_ffmpeg_exe()
cfg = json.load(open(sys.argv[1]))
TMP = cfg["tmp"]; os.makedirs(TMP, exist_ok=True)
RUNDE, ANIMALE = cfg["runde_dir"], cfg["animale_dir"]
V = "scale=1920:1080,fps=30,format=yuv420p,setsar=1"
ENC = ["-an", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast"]
CD = 3  # numărătoarea 3-2-1
def run(args): subprocess.run([FF, "-loglevel", "error", "-y"] + args, check=True)
def dur(f):
    o = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    h, m, sec = re.search(r"Duration: (\d+):(\d+):([\d.]+)", o).groups()
    return int(h) * 3600 + int(m) * 60 + float(sec)
def clip_in(r):  # clipul de răspuns: tăiat (tramvaiul pleacă), apoi ultimul cadru ținut
    return f"trim=0:{r.get('clip_len', 10)},setpts=PTS-STARTPTS,{V},tpad=stop_mode=clone:stop_duration=8,trim=0:10,setpts=PTS-STARTPTS"

# ---------- trailer: 4 dezvăluiri rapide ----------
TR = cfg["trailer"]; TS = TR["slot"]; TLEN = TS * len(TR["rounds"])
byn = {r["nr"]: r for r in cfg["rounds"]}
ins, fc = [], ""
for i, n in enumerate(TR["rounds"]):
    r = byn[n]
    ins += ["-i", r["clip"], "-loop", "1", "-framerate", "30", "-i", f"{ANIMALE}/{r['label']}.png"]
    fc += f"[{2*i}:v]trim={TR['from']}:{TR['from'] + TS},setpts=PTS-STARTPTS,{V}[c{i}];[{2*i+1}:v]format=rgba,scale=1920:1080[n{i}];" \
          f"[c{i}][n{i}]overlay=0:0:shortest=1,format=yuv420p[t{i}];"
fc += "".join(f"[t{i}]" for i in range(len(TR["rounds"]))) + f"concat=n={len(TR['rounds'])}:v=1:a=0"
run(ins + ["-filter_complex", fc, "-t", str(TLEN)] + ENC + [f"{TMP}/00a.mp4"])

# ---------- intro ----------
IV = cfg["voice"]
ILEN = round(0.15 + dur(IV["intro-1"]) + 0.15 + dur(IV["intro-2"]) + 0.2, 2)
run(["-i", cfg["intro"], "-loop", "1", "-framerate", "30", "-i", cfg["intro_text"],
     "-filter_complex", f"[0:v]trim=0:{ILEN},setpts=PTS-STARTPTS,{V}[i];[1:v]format=rgba,scale=1920:1080[t];[i][t]overlay=0:0:shortest=1,format=yuv420p",
     "-t", str(ILEN)] + ENC + [f"{TMP}/00b.mp4"])

# ---------- runde ----------
for r in cfg["rounds"]:
    fast = r["nr"] <= cfg.get("fast_rounds", 3)
    L = 2.2 if fast else 2.6                       # lungimea unui sunet pe siluetă
    r["_snd"] = (2.2, 4.6) if fast else (2.6, 5.5)  # când pornesc cele 2 sunete (fără prelungire)
    e = max(0.0, 0.2 + dur(r["voice"]["round"]) + 0.4 - r["_snd"][0])  # replică lungă → prelungim
    sil = 5.0 if fast else 8.0
    if r["voice"].get("question"):  # întrebarea după al doilea sunet, înainte de numărătoare
        e = max(e, r["_snd"][1] + L + 0.3 + dur(r["voice"]["question"]) + 0.4 - (2 + sil))
    r["_e"], r["_sil"], r["_L"] = round(e, 2), sil, L
    r["_X"] = round(2 + sil + e + CD, 2)            # momentul dezvăluirii
    r["_len"] = round(r["_X"] + 9.5, 2)

segs = [f"{TMP}/00a.mp4", f"{TMP}/00b.mp4"]
for r in cfg["rounds"]:
    n = r["nr"]; d = f"{RUNDE}/runda-{n:02d}"; X = r["_X"]
    parts = [("1-round.png", 2), ("2-silueta.png", r["_sil"] + r["_e"])] + [(f"3-numaratoare-{k}.png", 1) for k in range(CD, 0, -1)]
    ins = []
    for f, t in parts:
        ins += ["-loop", "1", "-framerate", "30", "-t", str(t), "-i", f"{d}/{f}"]
    k = len(parts)
    ins += ["-i", r["clip"], "-loop", "1", "-framerate", "30", "-i", f"{ANIMALE}/{r['label']}.png"]
    fc = "".join(f"[{i}:v]{V}[s{i}];" for i in range(k)) + "".join(f"[s{i}]" for i in range(k)) + \
         f"concat=n={k}:v=1:a=0,fps=30,settb=AVTB[sil];" + \
         f"[{k}:v]{clip_in(r)},settb=AVTB[c];[sil][c]xfade=transition=fade:duration=0.5:offset={X - 0.5}[q];" + \
         f"[{k+1}:v]format=rgba,scale=1920:1080[nm];[q][nm]overlay=0:0:shortest=1:enable='gte(t,{X + 0.2})',format=yuv420p"
    out = f"{TMP}/{n:02d}.mp4"
    run(ins + ["-filter_complex", fc, "-t", str(r["_len"])] + ENC + [out])
    segs.append(out)

FLEN = 11.0
fin = cfg["final"]
run(["-i", fin["clip"], "-loop", "1", "-framerate", "30", "-i", fin["text"],
     "-filter_complex", f"[0:v]trim=0:10,setpts=PTS-STARTPTS,{V},tpad=stop_mode=clone:stop_duration=1[c];[1:v]format=rgba,scale=1920:1080[t];"
     f"[c][t]overlay=0:0:shortest=1:enable='between(t,0.4,8.5)',fade=t=out:st={FLEN-1.5}:d=1.5,format=yuv420p",
     "-t", str(FLEN)] + ENC + [f"{TMP}/99.mp4"])
segs.append(f"{TMP}/99.mp4")
open(f"{TMP}/list.txt", "w").write("".join(f"file '{s}'\n" for s in segs))
run(["-f", "concat", "-safe", "0", "-i", f"{TMP}/list.txt", "-c", "copy", f"{TMP}/video.mp4"])

# ---------- audio ----------
ev = []  # (fișier, start, câștig dB, bucată, fade)
for i, n in enumerate(TR["rounds"]):
    r = byn[n]; a = r["s3"][0]
    ev.append((r["sfx"], i * TS, -4 if i == len(TR["rounds"]) - 1 else 0, [a, a + TS - 0.05], True))
ev.append((IV["trailer"], TLEN - dur(IV["trailer"]) - 0.1, 2, None, False))
ev += [(IV["intro-1"], TLEN + 0.15, 0, None, False), (IV["intro-2"], TLEN + 0.3 + dur(IV["intro-1"]), 0, None, False)]
cw = cfg["countdown_words"]  # „three / two / one” pe câte o cifră
R0 = TLEN + ILEN
starts, chapters = [], []
for r in cfg["rounds"]:
    R = R0; e, X, L, v = r["_e"], r["_X"], r["_L"], r["voice"]; R0 += r["_len"]
    starts.append(R); C = R + X - CD
    s1, s2 = r["_snd"]
    ev += [(v["round"], R + 0.2, 0, None, False),
           (r["sfx"], R + s1 + e, 0, r["s1"], True), (r["sfx"], R + s2 + e, 0, r["s1"], True)]
    if v.get("question"):
        ev.append((v["question"], R + s2 + e + L + 0.3, 0, None, False))
    for k, (a, b) in enumerate(cw):
        ev.append((cfg["voice"]["countdown"], C + k + 0.05, 0, [a, b], False))
    ev += [(v["answer"], R + X, 0, None, False), (r["sfx"], R + X + 1.6 + max(0, dur(v["answer"]) - 1.6), 0, r["s3"], True)]
    if v.get("praise"): ev.append((v["praise"], R + X + 6.6, 0, None, False))
    r["_R"] = R
total = R0 + FLEN
t = R0 + 0.5
for f in fin["lines"]:
    ev.append((f, t, 0, None, False)); t += dur(f) + 0.35

def level(f, tr):
    af = (f"atrim={tr[0]}:{tr[1]}," if tr else "") + "volumedetect"
    o = subprocess.run([FF, "-i", f, "-af", af, "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", o).group(1)), float(re.search(r"max_volume: (-?[\d.]+)", o).group(1))
cache = {}
def auto_gain(f, tr, g, sfx):
    # vocile aduse la aceeași medie; sunetele vehiculelor (bucăți) la același vârf
    k = (f, tuple(tr) if tr else None)
    if k not in cache: cache[k] = level(f, tr)
    mean, peak = cache[k]
    return g + (-3 - peak if sfx else -16 - mean)
ins, fc, labels = [], "", []
for i, (f, st, g, tr, sfx) in enumerate(ev):
    g = round(auto_gain(f, tr, g, sfx), 1)
    ins += ["-i", f]
    tt = f"atrim={tr[0]}:{tr[1]},asetpts=PTS-STARTPTS," if tr else ""
    if sfx and tr: tt += f"afade=t=in:d=0.05,afade=t=out:st={max(0, tr[1] - tr[0] - 0.25)}:d=0.25,"
    ms = int(st * 1000)
    fc += f"[{i}:a]{tt}aformat=sample_rates=48000:channel_layouts=stereo,volume={g}dB,adelay={ms}|{ms}[e{i}];"
    labels.append(f"[e{i}]")
def T(a, b, c, d): return f"clip((t-{a})/({b}-{a}),0,1)*clip(({d}-t)/({d}-{c}),0,1)"
env = "0.1"
for r in cfg["rounds"]:
    R, X, e = r["_R"], r["_X"], r["_e"]; S = R + r["_snd"][0] + e; C = R + X - CD
    env += f"-0.1*{T(S-0.3, S, C+0.6, C+1.0)}-0.05*{T(C+1.0, C+1.4, R+X-0.7, R+X-0.4)}-0.07*{T(R+X-0.7, R+X-0.4, R+X+6.2, R+X+6.5)}+0.06*{T(R+X+6.3, R+X+6.7, R+X+8.5, R+X+9.2)}"
env = f"min(t/1,1)*({env})*clip(({total}-t)/2,0,1)"
mi = len(ev)
ins += ["-stream_loop", "-1", "-i", cfg["music"]]
fc += f"[{mi}:a]atrim=0:{total},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume='{env}':eval=frame[mu];"
fc += "".join(labels) + f"[mu]amix=inputs={len(labels)+1}:normalize=0:duration=longest,atrim=0:{total},volume=-3dB,alimiter=limit=0.89[a]"
run(ins + ["-filter_complex", fc, "-map", "[a]", "-c:a", "aac", "-b:a", "160k", f"{TMP}/audio.m4a"])
run(["-i", f"{TMP}/video.mp4", "-i", f"{TMP}/audio.m4a", "-map", "0:v", "-map", "1:a", "-c", "copy", "-shortest", "-movflags", "+faststart", cfg["out"]])
def mmss(s): return f"{int(s // 60)}:{int(s % 60):02d}"
print("capitole:\n0:00 Intro\n" + "".join(f"{mmss(r['_R'])} Round {r['nr']}{' (Bonus!)' if r['nr'] == 10 else ''}\n" for r in cfg["rounds"]) + f"{mmss(R0)} You did it!")
json.dump({str(r["nr"]): {"R": r["_R"], "X": r["_X"], "len": r["_len"], "e": r["_e"]} for r in cfg["rounds"]}, open(f"{TMP}/timpi.json", "w"), indent=1)
print("gata:", cfg["out"], "durata:", round(total, 2))
