"""Face YouTube Shorts verticale (1080x1920) din rundele videoclipului lung.

Folosire: python3 shorts.py <cfg.json> <director_iesire> [nr_runda ...]
Structura (~22 s): silueta + sunet x2 → întrebarea lui Pip → numărătoarea → dezvăluirea + răspuns + laudă → îndemn la videoclipul lung.
"""
import subprocess, os, json, sys, re
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "canal", "imagini")
OVL = os.path.join(IMG, "suprapuneri")
FONT = os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff")
cfg = json.load(open(sys.argv[1])); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
want = {int(x) for x in sys.argv[3:]}
TMP = os.path.join(cfg["tmp"], "shorts"); os.makedirs(TMP, exist_ok=True)
V = "scale=1920:1080,fps=30,format=yuv420p,setsar=1"
SIL, CD, CLIP, END = 8.0, 5.0, 10.0, 2.5
TOTAL = SIL + CD + CLIP - 0.5 + END

def run(a): subprocess.run([FF, "-loglevel", "error", "-y"] + a, check=True)
def dur(f):
    o = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", o).groups(); return int(h) * 3600 + int(m) * 60 + float(s)
def level(f, tr):
    af = (f"atrim={tr[0]}:{tr[1]}," if tr else "") + "volumedetect"
    o = subprocess.run([FF, "-i", f, "-af", af, "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", o).group(1)), float(re.search(r"max_volume: (-?[\d.]+)", o).group(1))

# texte fixe pentru format vertical
from PIL import Image, ImageDraw, ImageFont, ImageFilter
def card(path, lines):
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    for txt, y, size, col in lines:
        f = ImageFont.truetype(FONT, size)
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((540, y + size // 12), txt, font=f, fill=(0, 0, 0, 140), anchor="mm", stroke_width=size // 9, stroke_fill=(0, 0, 0, 140))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(size // 25)))
        ImageDraw.Draw(im).text((540, y), txt, font=f, fill=col, anchor="mm", stroke_width=size // 9, stroke_fill=(59, 42, 32))
    im.save(path)
W, Y = (255, 255, 255), (255, 210, 63)
card(f"{TMP}/top.png", [("WHO SAID", 330, 120, W), ("THAT?", 470, 150, Y)])
card(f"{TMP}/ask.png", [("Can you guess?", 1430, 90, W)])
card(f"{TMP}/end.png", [("Play all 20!", 1400, 100, Y), ("Full video on our channel", 1530, 62, W)])

for r in cfg["rounds"]:
    n = r["nr"]
    if want and n not in want: continue
    d = f"{IMG}/runda-{n:02d}"; v = r["voice"]
    # 1) partea orizontală: siluetă → numărătoare → clip cu numele animalului
    ins = ["-loop", "1", "-framerate", "30", "-t", str(SIL), "-i", f"{d}/2-silueta.png"]
    for k in range(5, 0, -1): ins += ["-loop", "1", "-framerate", "30", "-t", "1", "-i", f"{d}/3-numaratoare-{k}.png"]
    ins += ["-i", r["clip"], "-loop", "1", "-framerate", "30", "-i", f"{OVL}/animale/{r['label']}.png"]
    fc = "".join(f"[{i}:v]{V}[s{i}];" for i in range(6)) + "".join(f"[s{i}]" for i in range(6)) + "concat=n=6:v=1:a=0,fps=30,settb=AVTB[sil];" + \
         f"[6:v]trim=0:{CLIP},setpts=PTS-STARTPTS,{V},tpad=stop_mode=clone:stop_duration={END},settb=AVTB[c];" + \
         f"[sil][c]xfade=transition=fade:duration=0.5:offset={SIL + CD - 0.5}[q];[7:v]format=rgba,scale=1920:1080[nm];" + \
         f"[q][nm]overlay=0:0:shortest=1:enable='gte(t,{SIL + CD + 0.2})',format=yuv420p"
    run(ins + ["-filter_complex", fc, "-t", str(TOTAL), "-an", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", f"{TMP}/h{n:02d}.mp4"])
    # 2) vertical: fundal blurat + videoclipul la mijloc + texte
    T0 = SIL + CD - 0.5
    # fundal: decorul rundei cu animalul în siluetă, blurat (nu dezvăluie răspunsul, nu dublează textele)
    fc = "[4:v]scale=-2:1920,crop=1080:1920,boxblur=30:2,eq=brightness=-0.1,format=yuv420p,setsar=1[bg];[0:v]scale=1080:-2,setsar=1[fg];" + \
         "[bg][fg]overlay=0:(H-h)/2,setsar=1[v0];[1:v]format=rgba[t];[2:v]format=rgba[k];[3:v]format=rgba[e];" + \
         "[v0][t]overlay=0:0:shortest=1[v1];" + f"[v1][k]overlay=0:0:shortest=1:enable='lt(t,{SIL + CD - 0.5})'[v2];" + \
         f"[v2][e]overlay=0:0:shortest=1:enable='gte(t,{TOTAL - END - 0.5})',format=yuv420p[v]"
    # 3) sunet
    ev = [(r["sfx"], 0.4, r["s1"]), (r["sfx"], 3.3, r["s2"]),
          (v["question"], SIL - dur(v["question"]) - 0.4, None), (cfg["voice"]["N-00-countdown"], SIL, None),
          (v["answer"], SIL + CD, None), (r["sfx"], SIL + CD + 1.6, r["s3"])]
    if v.get("praise"): ev.append((v["praise"], SIL + CD + 6.6, None))
    ain = []; afc = ""; lab = []
    for i, (f, st, tr) in enumerate(ev):
        mean, peak = level(f, tr); g = (-16 - mean) if tr is None else (-3 - peak)
        t = f"atrim={tr[0]}:{tr[1]},asetpts=PTS-STARTPTS," if tr else ""
        ain += ["-i", f]; ms = int(st * 1000)
        afc += f"[{i + 5}:a]{t}aformat=sample_rates=48000:channel_layouts=stereo,volume={g:.1f}dB,adelay={ms}|{ms}[e{i}];"; lab.append(f"[e{i}]")
    def Tz(a, b, c, e): return f"clip((t-{a})/({b}-{a}),0,1)*clip(({e}-t)/({e}-{c}),0,1)"
    env = f"min(t/0.8,1)*(0.1-0.1*{Tz(0.1, 0.4, 6.0, 6.4)}-0.05*{Tz(SIL - 0.3, SIL, T0, T0 + 0.3)}-0.07*{Tz(T0, T0 + 0.3, T0 + 6.5, T0 + 7)}+0.05*{Tz(T0 + 7, T0 + 7.5, TOTAL - 1, TOTAL)})*clip(({TOTAL}-t)/1.2,0,1)"
    mi = len(ev) + 5
    afc += f"[{mi}:a]atrim=0:{TOTAL},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume='{env}':eval=frame[mu];"
    afc += "".join(lab) + f"[mu]amix=inputs={len(lab) + 1}:normalize=0:duration=longest,atrim=0:{TOTAL},volume=-2dB,alimiter=limit=0.89[a]"
    out = f"{OUT}/short-{n:02d}-{r['label'].split('-', 1)[1]}.mp4"
    run(["-i", f"{TMP}/h{n:02d}.mp4", "-loop", "1", "-i", f"{TMP}/top.png", "-loop", "1", "-i", f"{TMP}/ask.png", "-loop", "1", "-i", f"{TMP}/end.png",
        "-loop", "1", "-i", f"{d}/silueta-fara-semn.png"]
        + ain + ["-stream_loop", "-1", "-i", cfg["music"], "-filter_complex", fc + ";" + afc,
        "-map", "[v]", "-map", "[a]", "-r", "30", "-t", str(TOTAL), "-c:v", "libx264", "-crf", "23", "-preset", "veryfast", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out])
    print("gata:", out)
