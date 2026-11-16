"""Video 9 (format nou): siluetă din imaginea desenată + UN sunet lung, 3-2-1, apoi dezvăluire într-un cartonaș
care crește din siluetă, cu video real (sau clip desenat), Pip decupat în colț și numele dedesubt.

Folosire: monteaza_v9.py <iesire.mp4> [nr nr ...]   (fără numere = toate cele 20 de runde + trailer + final)
"""
import subprocess, os, sys, re, json
import numpy as np, librosa
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FF = __import__("imageio_ffmpeg").get_ffmpeg_exe()
HERE = os.path.dirname(os.path.abspath(__file__)); C = os.path.abspath(os.path.join(HERE, "..", "canal"))
V9 = f"{C}/video-09"; M = f"{V9}/materiale"; R4 = f"{C}/video-04/materiale/voci-noi"
FONT = os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff")
OUT = sys.argv[1]; WANT = [int(x) for x in sys.argv[2:]] or list(range(1, 21)); FULL = len(sys.argv) <= 2
TMP = "/tmp/claude-0/-home-user-youtube-/57eeb2af-5218-5815-9c30-1db477c1a629/scratchpad/build9"; os.makedirs(TMP, exist_ok=True)
W, H = 1920, 1080; V = "scale=1920:1080,fps=30,format=yuv420p,setsar=1"
ENC = ["-an", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-r", "30", "-video_track_timescale", "15360"]
CD, REV = 3, 8.5
CW, CH = 1240, 698; X0, Y0 = 610, 70   # video-ul în cartonaș
INS = ["drum", "piano", "guitar", "trumpet", "violin", "xylophone", "tambourine", "flute", "maracas", "gong", "saxophone",
       "harmonica", "triangle", "accordion", "cymbals", "harp", "trombone", "banjo", "tuba", "bagpipes"]
DRAWN = {6, 10, 12, 13}                  # dezvăluire cu clip desenat (nu video real)
SND_FROM = {20: 5.0}                     # cimpoiul: sunetul bun începe de la 5 s
Q = {n: (5 if n in (16, 18, 20) else (n - 4) % 4 + 1) for n in range(4, 21)}
P = {n: (7 if n >= 19 else (n - 1) % 6 + 1) for n in range(1, 21)}

def run(a): subprocess.run([FF, "-loglevel", "error", "-y"] + a, check=True)
def dur(f):
    o = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", o).groups(); return int(h) * 3600 + int(m) * 60 + float(s)
def window(f, L, start=0.0):
    y, sr = librosa.load(f, sr=22050); y0 = int(start * sr); y = y[y0:]
    r = librosa.feature.rms(y=y, frame_length=1102, hop_length=1102)[0]; k = int(L / 0.05)
    a = round(int(np.argmax(np.convolve(r ** 2, np.ones(k), "valid"))) * 0.05, 2) if len(r) > k else 0.0
    return [round(start + a, 2), round(start + min(len(y) / sr, a + L), 2)]
def text_png(path, s, y, size, col):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); f = ImageFont.truetype(FONT, size)
    while f.getlength(s) > 1150 and size > 90: size -= 8; f = ImageFont.truetype(FONT, size)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((X0 + CW // 2, y + 12), s, font=f, fill=(0, 0, 0, 120), anchor="mm", stroke_width=size // 9, stroke_fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(im).text((X0 + CW // 2, y), s, font=f, fill=col, anchor="mm", stroke_width=size // 9, stroke_fill=(59, 42, 32, 255))
    im.save(path)

pip = Image.open(f"{C}/imagini/pip/pip-decupat.png").convert("RGBA"); pip = pip.resize((int(pip.width * 470 / pip.height), 470), Image.LANCZOS)
card = Image.new("RGBA", (CW + 32, CH + 32), (0, 0, 0, 0)); ImageDraw.Draw(card).rounded_rectangle((0, 0, CW + 31, CH + 31), 46, fill=(255, 255, 255, 255))
card.save(f"{TMP}/card.png")
mk = Image.new("L", (CW, CH), 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, CW - 1, CH - 1), 32, fill=255); mk.save(f"{TMP}/mask.png")

rounds = []
for n in WANT:
    en = INS[n - 1]; d = f"{V9}/imagini/runda-{n:02d}"
    r = {"nr": n, "en": en, "dir": d, "sfx": f"{M}/sunete/{n:02d}-{en}.mp3", "rev": f"{M}/video-real/{n:02d}-{en}" + ("-aproape" if n == 9 else "") + ".mp4",
         "round": f"{R4}/runde/N-{n:02d}-round.mp3", "answer": f"{M}/voci-noi/raspunsuri/N-{n:02d}-answer.mp3",
         "praise": f"{R4}/pip/P-lauda-{P[n]}.mp3", "question": f"{R4}/pip/P-intrebare-{Q[n]}.mp3" if n in Q else None}
    fast = n <= 3
    r["L"] = 3.5 if fast else 5.0
    r["s1"] = window(r["sfx"], r["L"], SND_FROM.get(n, 0)); r["s3"] = window(r["sfx"], 3.0, SND_FROM.get(n, 0))
    r["SIL"] = round(0.3 + r["L"] + (0.3 + dur(r["question"]) + 0.3 if r["question"] else 0) + 0.4, 2)
    r["X"] = round(2 + r["SIL"] + CD, 2); r["len"] = round(r["X"] + REV, 2)
    for f in [r["sfx"], r["rev"], r["round"], r["answer"], r["praise"]] + ([r["question"]] if r["question"] else []):
        assert os.path.exists(f), f
    # centrul siluetei (de unde crește cartonașul) și fundalul dezvăluirii
    s = np.array(Image.open(f"{d}/silueta-fara-semn.png").convert("RGB")).astype(int); c0 = np.array(Image.open(f"{d}/cadru-0.png").convert("RGB")).astype(int)
    ys, xs = np.nonzero(np.abs(s - c0).sum(2) > 30); r["cx"], r["cy"] = int(xs.mean() * W / s.shape[1]), int(ys.mean() * H / s.shape[0])
    bg = Image.open(f"{d}/cadru-0.png").convert("RGB").resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(30)).convert("RGBA")
    bg.alpha_composite(Image.new("RGBA", (W, H), (255, 240, 205, 120))); bg.alpha_composite(pip, (10, H - 470 - 20))
    bg.convert("RGB").save(f"{TMP}/bg-{n:02d}.png")
    text_png(f"{TMP}/name-{n:02d}.png", en.upper(), 945, 170, (255, 210, 63, 255))
    rounds.append(r)

def round_video(r):
    n, d, X = r["nr"], r["dir"], r["X"]
    parts = [("1-round.png", 2), ("2-silueta.png", r["SIL"])] + [(f"3-numaratoare-{k}.png", 1) for k in (3, 2, 1)]
    ins = sum((["-loop", "1", "-framerate", "30", "-t", str(t), "-i", f"{d}/{f}"] for f, t in parts), [])
    k = len(parts)
    if n in DRAWN:   # clipul desenat: doar partea cu instrumentul (dreapta), ca să nu apară Pip de două ori
        cx_, cy_ = {6: (0.53, 0.53), 10: (0.42, 0.10), 12: (0.43, 0.30), 13: (0.43, 0.15)}[n]  # doar instrumentul, fără Pip din desen
        cw_ = 0.45 if n == 6 else 0.56; src = f"crop=iw*{cw_}:ih*{cw_}:iw*{cx_}:ih*{cy_},scale={CW}:{CH}"; off = 0.3
    else:
        src = f"scale={CW}:{CH}:force_original_aspect_ratio=increase,crop={CW}:{CH}"; off = min(0.5, max(0, dur(r["rev"]) - REV))
    ins += ["-loop", "1", "-framerate", "30", "-t", str(REV), "-i", f"{TMP}/bg-{n:02d}.png", "-i", r["rev"],
            "-loop", "1", "-framerate", "30", "-t", str(REV), "-i", f"{TMP}/mask.png",
            "-loop", "1", "-framerate", "30", "-t", str(REV), "-i", f"{TMP}/name-{n:02d}.png",
            "-loop", "1", "-framerate", "30", "-t", str(REV), "-i", f"{TMP}/card.png"]
    b, rv, mki, nm, cd = k, k + 1, k + 2, k + 3, k + 4
    p = "min(1,t/0.4)"
    fc = "".join(f"[{i}:v]{V}[s{i}];" for i in range(k)) + "".join(f"[s{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0[A];"
    fc += (f"[{rv}:v]trim={off}:{off + REV},setpts=PTS-STARTPTS,fps=30,{src},tpad=stop_mode=clone:stop_duration={REV},trim=0:{REV},format=rgba[rvv];"
           f"[{mki}:v]format=gray,scale={CW}:{CH}[mk];[rvv][mk]alphamerge[rvm];[{cd}:v]format=rgba[cw];[cw][rvm]overlay=16:16[card];"
           f"[card]scale=w='trunc(iw*(0.3+0.7*{p})/2)*2':h='trunc(ih*(0.3+0.7*{p})/2)*2':eval=frame[cs];[{b}:v]fps=30,format=rgba[bg];"
           f"[bg][cs]overlay=x='{r['cx']}+({X0 + CW // 2}-{r['cx']})*{p}-overlay_w/2':y='{r['cy']}+({Y0 + CH // 2}-{r['cy']})*{p}-overlay_h/2'[r1];"
           f"[{nm}:v]format=rgba,fade=t=in:st=0.5:d=0.3:alpha=1[nmf];[r1][nmf]overlay=0:0,fade=t=in:st=0:d=0.2:color=white,{V}[B];[A][B]concat=n=2:v=1:a=0,format=yuv420p")
    out = f"{TMP}/r{n:02d}.mp4"; run(ins + ["-filter_complex", fc, "-t", str(r["len"])] + ENC + [out]); return out

# ---------- intro (doar „Who said BOOM BOOM?”) + Subscribe ----------
IP = f"{M}/voci-noi/pip/P-who-said-boom-boom.mp3"
ILEN = round(0.15 + dur(IP) + 0.3, 2)
it = Image.new("RGBA", (W, H), (0, 0, 0, 0)); f = ImageFont.truetype(FONT, 150)
for i, (s, y) in enumerate((("Who Said", 40), ("BOOM BOOM?", 200))):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((1390, y + 10), s, font=f, fill=(0, 0, 0, 120), anchor="ma", stroke_width=16, stroke_fill=(0, 0, 0, 120))
    it.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(it).text((1390, y), s, font=f, fill=(255, 255, 255, 255), anchor="ma", stroke_width=16, stroke_fill=(59, 42, 32, 255))
it.save(f"{TMP}/intro-text.png")
SB = f"{V9}/../video-08/imagini/suprapuneri/subscribe.png"
run(["-i", f"{M}/clipuri/00-intro.mp4", "-loop", "1", "-framerate", "30", "-i", f"{TMP}/intro-text.png", "-loop", "1", "-framerate", "30", "-t", str(ILEN), "-i", SB,
     "-filter_complex", f"[0:v]trim=0:{ILEN},setpts=PTS-STARTPTS,{V}[i];[1:v]format=rgba[t];[i][t]overlay=0:0:shortest=1[it];"
     f"[2:v]format=rgba,fade=t=in:st=0.2:d=0.25:alpha=1,fade=t=out:st={ILEN - 0.3}:d=0.3:alpha=1[sb];[it][sb]overlay=0:0:shortest=1,format=yuv420p",
     "-t", str(ILEN)] + ENC + [f"{TMP}/intro.mp4"])
TRN, TS = [10, 4, 9, 15], 1.25
TLEN = TS * len(TRN) if FULL else 0
if FULL:
    ins = sum((["-loop", "1", "-framerate", "30", "-t", str(TS), "-i", f"{V9}/imagini/runda-{n:02d}/2-silueta.png"] for n in TRN), [])
    run(ins + ["-filter_complex", "".join(f"[{i}:v]{V}[t{i}];" for i in range(len(TRN))) + "".join(f"[t{i}]" for i in range(len(TRN))) + f"concat=n={len(TRN)}:v=1:a=0"] + ENC + [f"{TMP}/trailer.mp4"])
segs = ([f"{TMP}/trailer.mp4"] if FULL else []) + [f"{TMP}/intro.mp4"] + [round_video(r) for r in rounds]
FLEN = 11.0
FIN = [f"{M}/voci-noi/pip/P-you-did-it-instruments.mp3", f"{R4}/pip/P-super-listener.mp3", f"{R4}/pip/P-see-you-next-time.mp3"]
if FULL:
    run(["-i", f"{M}/clipuri/99-final.mp4", "-loop", "1", "-framerate", "30", "-i", f"{V9}/imagini/suprapuneri/final-you-did-it.png",
         "-filter_complex", f"[0:v]trim=0:10,setpts=PTS-STARTPTS,{V},tpad=stop_mode=clone:stop_duration=1[c];[1:v]format=rgba,scale=1920:1080[t];"
         f"[c][t]overlay=0:0:shortest=1:enable='between(t,0.4,8.5)',fade=t=out:st={FLEN - 1.5}:d=1.5,format=yuv420p", "-t", str(FLEN)] + ENC + [f"{TMP}/final.mp4"])
    segs.append(f"{TMP}/final.mp4")

# ---------- lipire (filtrul concat) ----------
ins = sum((["-i", s] for s in segs), []); k = len(segs)
run(ins + ["-filter_complex", "".join(f"[{i}:v]" for i in range(k)) + f"concat=n={k}:v=1:a=0[v]", "-map", "[v]"] + ENC + [f"{TMP}/video.mp4"])

# ---------- sunet ----------
ev = []
if FULL:
    byn = {r["nr"]: r for r in rounds}
    for i, n in enumerate(TRN): ev.append((byn[n]["sfx"], i * TS, [byn[n]["s3"][0], byn[n]["s3"][0] + TS - 0.05], True))
    ev.append((f"{R4}/pip/P-can-you-guess-them-all.mp3", TLEN - dur(f"{R4}/pip/P-can-you-guess-them-all.mp3") - 0.1, None, False))
ev.append((IP, TLEN + 0.15, None, False))
cw = [[0.05, 0.8], [0.88, 1.65], [1.84, 2.87]]
R = TLEN + ILEN; chapters = []
for r in rounds:
    chapters.append((R, r["nr"])); X = r["X"]
    ev += [(r["round"], R + 0.2, None, False), (r["sfx"], R + 2.3, r["s1"], True)]
    if r["question"]: ev.append((r["question"], R + 2.3 + r["L"] + 0.3, None, False))
    for i, w in enumerate(cw): ev.append((f"{R4}/N-00-countdown-321.mp3", R + X - CD + i + 0.05, w, False))
    a = dur(r["answer"])
    ev += [(r["answer"], R + X + 0.5, None, False), (r["sfx"], R + X + 0.6 + a + 0.1, r["s3"], True),
           (r["praise"], R + X + REV - dur(r["praise"]) - 0.3, None, False)]
    R += r["len"]
if FULL:
    t = R + 0.5
    for f in FIN: ev.append((f, t, None, False)); t += dur(f) + 0.35
    chapters.append((R, "final")); R += FLEN
total = R
def level(f, tr):
    af = (f"atrim={tr[0]}:{tr[1]}," if tr else "") + "volumedetect"
    o = subprocess.run([FF, "-i", f, "-af", af, "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", o).group(1)), float(re.search(r"max_volume: (-?[\d.]+)", o).group(1))
cache = {}; ins, fc, lab = [], "", []
for i, (fl, st, tr, sfx) in enumerate(ev):
    key = (fl, tuple(tr) if tr else None)
    if key not in cache: cache[key] = level(fl, tr)
    mean, peak = cache[key]; g = round((-15 - mean) if sfx else (-16 - mean), 1)   # instrumentele: după medie (muzică, nu lovituri)
    g = min(g, -2 - peak) if sfx else g
    tt = f"atrim={tr[0]}:{tr[1]},asetpts=PTS-STARTPTS," if tr else ""
    if sfx: tt += f"afade=t=in:d=0.05,afade=t=out:st={max(0, tr[1] - tr[0] - 0.4):.2f}:d=0.4,"
    ins += ["-i", fl]; ms = int(st * 1000)
    fc += f"[{i}:a]{tt}aformat=sample_rates=48000:channel_layouts=stereo,volume={g}dB,adelay={ms}|{ms}[e{i}];"; lab.append(f"[e{i}]")
mi = len(ev)
fc += f"[{mi}:a]atrim=0:{total},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.05[mu];"
fc += "".join(lab) + f"[mu]amix=inputs={len(lab) + 1}:normalize=0:duration=longest,atrim=0:{total},volume=-2dB,alimiter=limit=0.89[a]"
run(ins + ["-stream_loop", "-1", "-i", f"{C}/video-04/materiale/muzica/Baby_Animals_Playing_-_Joel_Cummins.mp3", "-filter_complex", fc,
           "-map", "[a]", "-c:a", "aac", "-b:a", "160k", f"{TMP}/audio.m4a"])
run(["-i", f"{TMP}/video.mp4", "-i", f"{TMP}/audio.m4a", "-c", "copy", "-shortest", "-movflags", "+faststart", OUT])
print("capitole:"); [print(f"{int(t // 60)}:{int(t % 60):02d} " + ("You did it!" if n == "final" else f"Round {n}" + (" (Bonus!)" if n == 10 else ""))) for t, n in chapters]
print("gata:", OUT, round(total, 1))
