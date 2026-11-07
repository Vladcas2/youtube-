"""Shorts verticale „pe tot ecranul” (format de test, ~11 s): benzi colorate sus/jos în loc de fundal blurat,
sunetul din prima secundă, 3-2-1 mare, dezvăluire cu numele mare, fără cartonaș de final (se reia lin).

Folosire: python3 shorts_vert.py <cfg.json> <director_iesire> nr_runda [nr_runda ...]
"""
import subprocess, os, json, sys, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FF = __import__("imageio_ffmpeg").get_ffmpeg_exe()
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff")
cfg = json.load(open(sys.argv[1])); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
want = [int(x) for x in sys.argv[3:]]
TMP = os.path.join(cfg["tmp"], "shorts-vert"); os.makedirs(TMP, exist_ok=True)
V = "scale=1920:1080,fps=30,format=yuv420p,setsar=1"
LISTEN, CD, REVEAL = 3.0, 3.0, 5.0
TOTAL = LISTEN + CD + REVEAL
CW = 1300                      # cât din lățimea cadrului 1920 păstrăm (vehiculul întreg)
IH = round(1080 * 1080 / CW / 2) * 2  # înălțimea imaginii în Short
BAND = (1920 - IH) // 2
YEL, BROWN, WHITE = (255, 210, 63, 255), (59, 42, 32, 255), (255, 255, 255, 255)

def run(a): subprocess.run([FF, "-loglevel", "error", "-y"] + a, check=True)
def dur(f):
    o = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", o).groups(); return int(h) * 3600 + int(m) * 60 + float(s)
def level(f, tr):
    af = (f"atrim={tr[0]}:{tr[1]}," if tr else "") + "volumedetect"
    o = subprocess.run([FF, "-i", f, "-af", af, "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", o).group(1)), float(re.search(r"max_volume: (-?[\d.]+)", o).group(1))

def layer(path, items, bands=False):
    """Strat 1080x1920: benzile galbene (opțional) + texte centrate (text, y, mărime, culoare)."""
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if bands:
        for y0 in (0, 1920 - BAND):
            d.rectangle((0, y0, 1080, y0 + BAND), fill=YEL)
        for k in range(-2, 30):  # dungi de șantier la marginea benzilor, spre imagine
            for y0 in (BAND - 34, 1920 - BAND):
                d.polygon([(k * 60, y0), (k * 60 + 30, y0), (k * 60 + 64, y0 + 34), (k * 60 + 34, y0 + 34)], fill=BROWN)
    for txt, y, size, col in items:
        f = ImageFont.truetype(FONT, size)
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((540, y + size // 12), txt, font=f, fill=(0, 0, 0, 120), anchor="mm", stroke_width=size // 9, stroke_fill=(0, 0, 0, 120))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(size // 25)))
        ImageDraw.Draw(im).text((540, y), txt, font=f, fill=col, anchor="mm", stroke_width=size // 9, stroke_fill=BROWN)
    im.save(path)

top_y, bot_y = BAND // 2 - 10, 1920 - BAND // 2 - 10
layer(f"{TMP}/bands.png", [("WHO SAID", top_y - 75, 130, WHITE), ("THAT?", top_y + 80, 160, WHITE)], bands=True)
layer(f"{TMP}/listen.png", [("LISTEN...", bot_y, 150, WHITE)])
for k in (3, 2, 1):
    layer(f"{TMP}/cd{k}.png", [(str(k), bot_y, 300, WHITE)])

def center_x(n):
    s = np.array(Image.open(f"{cfg['runde_dir']}/runda-{n:02d}/silueta-fara-semn.png").convert("RGB")).astype(int)
    xs = np.nonzero(np.abs(s - [22, 20, 24]).sum(2) < 6)[1] * 1920 / s.shape[1]
    return (xs.min() + xs.max()) / 2

byn = {r["nr"]: r for r in cfg["rounds"]}
for n in want:
    r = byn[n]; v = r["voice"]; d = f"{cfg['runde_dir']}/runda-{n:02d}"
    name = r["label"].split("-", 1)[1].replace("-", " ").upper()
    layer(f"{TMP}/name{n:02d}.png", [(name, bot_y, 175 if len(name) <= 10 else (140 if len(name) <= 12 else 112), YEL)])
    x0 = int(min(max(center_x(n) - CW / 2, 0), 1920 - CW))
    clip, ctrim = r["clip"], 10
    if r.get("boomerang"):  # vezi monteaza_v4: partea bună, înainte-înapoi
        clip = f"{TMP}/boomerang-{n:02d}.mp4"
        run(["-i", r["clip"], "-filter_complex", f"[0:v]trim=0:{r['boomerang']},setpts=PTS-STARTPTS,{V},split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0", "-an", clip])
    crop = f"crop={CW}:1080:{x0}:0,scale=1080:{IH},pad=1080:1920:0:{BAND}:color=0xFFD23F,setsar=1"
    fc = (f"[0:v]{V},{crop}[s];"
          f"[1:v]trim=0:{REVEAL + 1},setpts=PTS-STARTPTS,{V},{crop},tpad=stop_mode=clone:stop_duration=3,trim=0:{REVEAL + 1},setpts=PTS-STARTPTS,fps=30[c];"
          f"[s]settb=AVTB[s2];[c]settb=AVTB[c2];[s2][c2]xfade=transition=fade:duration=0.3:offset={LISTEN + CD - 0.3}[v0];"
          "[2:v]format=rgba[b];[v0][b]overlay=0:0:shortest=1[v1];"
          f"[3:v]format=rgba[l];[v1][l]overlay=0:0:shortest=1:enable='lt(t,{LISTEN})'[v2];")
    last = "v2"
    for i, k in enumerate((3, 2, 1)):
        a = LISTEN + i
        fc += f"[{4 + i}:v]format=rgba[k{k}];[{last}][k{k}]overlay=0:0:shortest=1:enable='between(t,{a},{a + 0.999})'[w{k}];"; last = f"w{k}"
    fc += f"[7:v]format=rgba[nm];[{last}][nm]overlay=0:0:shortest=1:enable='gte(t,{LISTEN + CD + 0.1})',format=yuv420p[v]"
    vin = ["-loop", "1", "-framerate", "30", "-t", str(TOTAL), "-i", f"{d}/2-silueta.png", "-i", clip,
           "-loop", "1", "-framerate", "30", "-t", str(TOTAL), "-i", f"{TMP}/bands.png",
           "-loop", "1", "-framerate", "30", "-t", str(TOTAL), "-i", f"{TMP}/listen.png"] + \
          sum((["-loop", "1", "-framerate", "30", "-t", str(TOTAL), "-i", f"{TMP}/cd{k}.png"] for k in (3, 2, 1)), []) + \
          ["-loop", "1", "-framerate", "30", "-t", str(TOTAL), "-i", f"{TMP}/name{n:02d}.png"]
    # sunet: vehiculul din prima clipă, 3-2-1, răspuns, vehiculul din nou
    L = min(LISTEN - 0.1, r["s1"][1] - r["s1"][0])
    ev = [(r["sfx"], 0.0, [r["s1"][0], r["s1"][0] + L], True)]
    ev += [(cfg["voice"]["countdown"], LISTEN + k + 0.05, w, False) for k, w in enumerate(cfg["countdown_words"])]
    ev += [(v["answer"], LISTEN + CD + 0.1, None, False), (r["sfx"], LISTEN + CD + 0.2 + dur(v["answer"]), r["s3"], True)]
    ain, afc, lab = [], "", []
    nin = sum(1 for x in vin if x == "-i")
    for i, (f, st, tr, sfx) in enumerate(ev):
        mean, peak = level(f, tr)
        g = (-3 - peak) if sfx else (-16 - level(f, None)[0])
        t = f"atrim={tr[0]}:{tr[1]},asetpts=PTS-STARTPTS," if tr else ""
        if sfx: t += f"afade=t=in:d=0.03,afade=t=out:st={max(0, tr[1] - tr[0] - 0.25):.2f}:d=0.25,"
        ain += ["-i", f]; ms = int(st * 1000)
        afc += f"[{nin + i}:a]{t}aformat=sample_rates=48000:channel_layouts=stereo,volume={g:.1f}dB,adelay={ms}|{ms}[e{i}];"; lab.append(f"[e{i}]")
    mi = nin + len(ev)
    afc += f"[{mi}:a]atrim=0:{TOTAL},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume='0.05+0.04*gte(t,{LISTEN + CD + 2.5})':eval=frame[mu];"
    afc += "".join(lab) + f"[mu]amix=inputs={len(lab) + 1}:normalize=0:duration=longest,atrim=0:{TOTAL},volume=-2dB,alimiter=limit=0.89[a]"
    out = f"{OUT}/vert-{n:02d}-{r['label'].split('-', 1)[1]}.mp4"
    run(vin + ain + ["-stream_loop", "-1", "-i", cfg["music"], "-filter_complex", fc + ";" + afc,
        "-map", "[v]", "-map", "[a]", "-r", "30", "-t", str(TOTAL), "-c:v", "libx264", "-crf", "21", "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out])
    print("gata:", out)
