"""Short vertical în stil „Talking Flashcards” (formatul care merge la canalul model):
câte un cartonaș pe obiect, clipul decupat pe obiect, numele mare, vocea naratorului + sunetul real.

Folosire: python3 shorts_flashcards.py <cfg.json> <iesire.mp4> "TITLU RAND 1|TITLU RAND 2" nr nr nr ...
"""
import subprocess, os, json, sys, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FF = __import__("imageio_ffmpeg").get_ffmpeg_exe()
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff")
cfg = json.load(open(sys.argv[1])); OUT = sys.argv[2]; TITLE = sys.argv[3].split("|")
want = [int(x) for x in sys.argv[4:]]
TMP = os.path.join(cfg["tmp"], "flashcards"); os.makedirs(TMP, exist_ok=True)
YEL, BROWN, WHITE, CORAL, CREAM = (255, 210, 63, 255), (59, 42, 32, 255), (255, 255, 255, 255), (240, 98, 85, 255), (255, 240, 205, 255)
CARD = (70, 380, 1010, 1320)   # cartonașul alb; clipul intră cu 20 px margine
IN = 900                         # latura clipului pe cartonaș
SFX = 1.4                        # cât din sunetul real
ENC = ["-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
       "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]

def run(a): subprocess.run([FF, "-loglevel", "error", "-y"] + a, check=True)
def dur(f):
    o = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", o).groups(); return int(h) * 3600 + int(m) * 60 + float(s)
def level(f, tr=None):
    af = (f"atrim={tr[0]}:{tr[1]}," if tr else "") + "volumedetect"
    o = subprocess.run([FF, "-i", f, "-af", af, "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", o).group(1)), float(re.search(r"max_volume: (-?[\d.]+)", o).group(1))

def text(d, im, xy, s, size, col, stroke=None):
    f = ImageFont.truetype(FONT, size); st = stroke or size // 9
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0], xy[1] + size // 14), s, font=f, fill=(0, 0, 0, 110), anchor="mm", stroke_width=st, stroke_fill=(0, 0, 0, 110))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(size // 28)))
    ImageDraw.Draw(im).text(xy, s, font=f, fill=col, anchor="mm", stroke_width=st, stroke_fill=BROWN)

def fit(s, maxw, size):
    while ImageFont.truetype(FONT, size).getlength(s) > maxw and size > 60: size -= 6
    return size

# fundalul comun: crem cu buline, titlul sus, cartonașul alb
bg = Image.new("RGBA", (1080, 1920), CREAM); d = ImageDraw.Draw(bg)
for y in range(0, 1920, 120):
    for x in range(-60 if (y // 120) % 2 else 0, 1080, 120):
        d.ellipse((x + 40, y + 40, x + 70, y + 70), fill=(255, 225, 160, 255))
d.rectangle((0, 0, 1080, 330), fill=CORAL)
for k in range(0, 1080, 60): d.ellipse((k - 30, 300, k + 30, 360), fill=CORAL)   # margine ondulată
text(d, bg, (540, 105), TITLE[0], fit(TITLE[0], 1000, 120), WHITE)
if len(TITLE) > 1: text(d, bg, (540, 235), TITLE[1], fit(TITLE[1], 1000, 120), YEL)
sh = Image.new("RGBA", bg.size, (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle((CARD[0] + 8, CARD[1] + 14, CARD[2] + 8, CARD[3] + 14), 48, fill=(0, 0, 0, 90))
bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
ImageDraw.Draw(bg).rounded_rectangle(CARD, 48, fill=WHITE)
bg.save(f"{TMP}/bg.png")

def box(n):
    """Pătratul de decupat din clip (pixeli 1280x720), centrat pe obiect, din silueta rundei."""
    d = f"{cfg['runde_dir']}/runda-{n:02d}"
    s = np.array(Image.open(f"{d}/silueta-fara-semn.png").convert("RGB")).astype(int)
    c = np.array(Image.open(f"{d}/cadru-0.png").convert("RGB")).astype(int)
    ys, xs = np.nonzero(np.abs(s - c).sum(2) > 30)  # doar pixelii înnegriți (obiectul), nu contururile închise la culoare
    side = int(min(720, max(460, max(xs.max() - xs.min(), ys.max() - ys.min()) * 1.25 + 40))); side -= side % 2  # min 460: obiectele mici (soneria) cu puțin context
    cx = min(max((xs.min() + xs.max()) // 2, side // 2), s.shape[1] - side // 2)
    cy = min(max((ys.min() + ys.max()) // 2, side // 2), s.shape[0] - side // 2)
    return side, cx - side // 2, cy - side // 2

def window(f, L):
    import librosa
    y, sr = librosa.load(f, sr=22050)
    r = librosa.feature.rms(y=y, frame_length=1102, hop_length=1102)[0]; k = int(L / 0.05)
    a = round(int(np.argmax(np.convolve(r ** 2, np.ones(k), "valid"))) * 0.05, 2) if len(r) > k else 0.0
    return a, min(len(y) / sr, a + L)

byn = {r["nr"]: r for r in cfg["rounds"]}
segs = []
for i, n in enumerate(want, 1):
    r = byn[n]; ans = r["voice"]["answer"]
    name = r["label"].split("-", 1)[1].replace("-", " ").upper()
    lay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    text(dl, lay, (540, 1440), name, fit(name, 980, 150), YEL)
    dl.ellipse((CARD[2] - 120, CARD[1] - 40, CARD[2] + 10, CARD[1] + 90), fill=CORAL, outline=WHITE, width=8)
    text(dl, lay, (CARD[2] - 55, CARD[1] + 25), str(i), 70, WHITE, 7)
    lay.save(f"{TMP}/name-{n:02d}.png")
    side, x0, y0 = box(n)
    a0, a1 = window(r["sfx"], SFX)
    da = dur(ans); t_sfx = 0.2 + da + 0.1; T = round(t_sfx + (a1 - a0) + 0.35, 2)
    ga = -15 - level(ans)[0]; gs = -4 - level(r["sfx"], (a0, a1))[1]
    seg = f"{TMP}/seg-{i:02d}.mp4"
    fc = (f"[1:v]trim=0:{T},setpts=PTS-STARTPTS,fps=30,crop={side}:{side}:{x0}:{y0},scale={IN}:{IN},setsar=1,"
          f"fade=t=in:st=0:d=0.2[c];[0:v][c]overlay={(1080 - IN) // 2}:{CARD[1] + 20}[v1];"
          f"[2:v]format=rgba,fade=t=in:st=0.15:d=0.2:alpha=1[t];[v1][t]overlay=0:0,format=yuv420p[v];"
          f"[3:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={ga:.1f}dB,adelay=200|200[a1];"
          f"[4:a]atrim={a0}:{a1},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={max(0, a1 - a0 - 0.25):.2f}:d=0.25,"
          f"aformat=sample_rates=48000:channel_layouts=stereo,volume={gs:.1f}dB,adelay={int(t_sfx * 1000)}|{int(t_sfx * 1000)}[a2];"
          f"[a1][a2]amix=inputs=2:normalize=0:duration=longest,apad,atrim=0:{T}[a]")
    run(["-loop", "1", "-framerate", "30", "-t", str(T), "-i", f"{TMP}/bg.png", "-i", r["clip"],
         "-loop", "1", "-framerate", "30", "-t", str(T), "-i", f"{TMP}/name-{n:02d}.png", "-i", ans, "-i", r["sfx"],
         "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", str(T)] + ENC + [seg])
    segs.append(seg); print(i, name, T)

# lipim cu filtrul concat (demuxerul a dat cadre negre la Video 7) și punem muzica încet dedesubt
ins = sum((["-i", s] for s in segs), [])
k = len(segs); total = sum(dur(s) for s in segs)
fc = "".join(f"[{j}:v][{j}:a]" for j in range(k)) + f"concat=n={k}:v=1:a=1[v][a0];"
fc += f"[{k}:a]atrim=0:{total},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.06[mu];"
fc += "[a0][mu]amix=inputs=2:normalize=0:duration=first,volume=-1dB,alimiter=limit=0.89[a]"
run(ins + ["-stream_loop", "-1", "-i", cfg["music"], "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-movflags", "+faststart"] + ENC + [OUT])
print("gata:", OUT, round(total, 1), "s")
