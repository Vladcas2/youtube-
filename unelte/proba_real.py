"""Probă Video 9: siluetă din imaginea desenată, un singur sunet lung, 3-2-1, apoi dezvăluire cu video-ul REAL
într-un cartonaș cu ramă albă, Pip în colț și numele dedesubt.
Folosire: proba_real.py <imagine.jpg> <video_real.mp4> <sunet.wav|mp3> NUME <iesire.mp4> [raspuns.mp3]"""
import sys, os, subprocess, re, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage as nd
from rembg import remove, new_session
FF = __import__("imageio_ffmpeg").get_ffmpeg_exe()
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "..", "canal")
FONT = os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff")
IMG, REAL, SND, NAME, OUT = sys.argv[1:6]; ANS = sys.argv[6] if len(sys.argv) > 6 else None
TMP = os.path.join(os.path.dirname(OUT), "_tmp"); os.makedirs(TMP, exist_ok=True)
W, H = 1920, 1080
LISTEN, CD, REVEAL = 5.0, 3.0, 7.5
def run(a): subprocess.run([FF, "-loglevel", "error", "-y"] + a, check=True)
def dur(f):
    o = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", o).groups(); return int(h) * 3600 + int(m) * 60 + float(s)
def mean(f):
    o = subprocess.run([FF, "-i", f, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", o).group(1))

im = Image.open(IMG).convert("RGB").resize((W, H), Image.LANCZOS)
sam = new_session("sam")
def mask(box, pos, neg):
    p = [{"type": "rectangle", "data": box, "label": 1}] + [{"type": "point", "data": q, "label": 1} for q in pos] + \
        [{"type": "point", "data": q, "label": 0} for q in neg]
    m = np.array(remove(im, session=sam, only_mask=True, sam_prompt=p)) > 127
    m = nd.binary_fill_holes(nd.binary_closing(m, np.ones((7, 7))))
    lab, k = nd.label(m); return lab == (np.argmax(nd.sum(m, lab, range(1, k + 1))) + 1)
obj = mask([883, 345, 1632, 989], [[1248, 768], [1250, 470]], [])
# 1) silueta cu „?”
a = np.array(im); a[obj] = [22, 20, 24]; sil = Image.fromarray(a).convert("RGBA")
q = Image.open(f"{R}/imagini/suprapuneri/semn-intrebare.png"); q = q.crop(q.getbbox())
ys, xs = np.nonzero(obj); cx, cy = int(xs.mean()), int(ys.mean())
qh = int(min(420, (ys.max() - ys.min()) * 0.75)); q = q.resize((int(q.width * qh / q.height), qh), Image.LANCZOS)
sil.alpha_composite(q, (cx - q.width // 2, cy - q.height // 2)); sil.convert("RGB").save(f"{TMP}/sil.png")
for k in (3, 2, 1):
    c = sil.copy(); c.alpha_composite(Image.open(f"{R}/imagini/suprapuneri/numaratoare/{k}.png").convert("RGBA").resize((W, H)))
    c.convert("RGB").save(f"{TMP}/cd{k}.png")
# 2) fundalul dezvăluirii: desenul estompat, cartonaș alb, Pip decupat în stânga jos
CW, CH = 1240, 698; X0, Y0 = 610, 70                    # video-ul real în cartonaș
bg = im.filter(ImageFilter.GaussianBlur(30)).convert("RGBA")  # estompat tare: Pip din desen nu se mai vede dublu
bg.alpha_composite(Image.new("RGBA", (W, H), (255, 240, 205, 120)))
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
card = Image.new("RGBA", (CW + 32, CH + 32), (0, 0, 0, 0))
ImageDraw.Draw(card).rounded_rectangle((0, 0, CW + 31, CH + 31), 46, fill=(255, 255, 255, 255)); card.save(f"{TMP}/card.png")
pc = Image.open(f"{R}/imagini/pip/pip-decupat.png").convert("RGBA")  # Pip decupat o singură dată, același în toate rundele
s = 470 / pc.height; pc = pc.resize((int(pc.width * s), 470), Image.LANCZOS)
bg.alpha_composite(pc, (10, H - 470 - 20))  # Pip nu atinge cartonașul
bg.convert("RGB").save(f"{TMP}/reveal-bg.png")
mk = Image.new("L", (CW, CH), 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, CW - 1, CH - 1), 32, fill=255); mk.save(f"{TMP}/mask.png")
nm = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(nm); f = ImageFont.truetype(FONT, 170)
s2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(s2).text((X0 + CW // 2, 945 + 12), NAME, font=f, fill=(0, 0, 0, 120), anchor="mm", stroke_width=18, stroke_fill=(0, 0, 0, 120))
nm.alpha_composite(s2.filter(ImageFilter.GaussianBlur(7)))
ImageDraw.Draw(nm).text((X0 + CW // 2, 945), NAME, font=f, fill=(255, 210, 63, 255), anchor="mm", stroke_width=18, stroke_fill=(59, 42, 32, 255))
nm.save(f"{TMP}/name.png")
# 3) video: ascultare -> 3-2-1 -> flash -> dezvăluire (cartonașul „crește” din siluetă)
T0 = LISTEN + CD; TOT = T0 + REVEAL
rd = dur(REAL); off = max(0, min(1.0, rd - REVEAL))
fc = (f"[0:v]fps=30,format=yuv420p[a];[1:v]fps=30,format=yuv420p[b];[2:v]fps=30,format=yuv420p[c];[3:v]fps=30,format=yuv420p[d];"
      f"[a][b][c][d]concat=n=4:v=1:a=0[lc];"
      f"[5:v]trim={off}:{off + REVEAL},setpts=PTS-STARTPTS,fps=30,scale={CW}:{CH}:force_original_aspect_ratio=increase,crop={CW}:{CH},format=rgba[rv];"
      f"[6:v]format=gray,scale={CW}:{CH}[mk];[rv][mk]alphamerge[rvm];"
      f"[8:v]format=rgba[cw];[cw][rvm]overlay=16:16[card];"
      f"[card]scale=w='trunc(iw*(0.3+0.7*min(1,t/0.4))/2)*2':h='trunc(ih*(0.3+0.7*min(1,t/0.4))/2)*2':eval=frame[cs];"
      f"[4:v]fps=30,format=rgba[bg];"
      f"[bg][cs]overlay=x='{cx}+({X0 + CW // 2}-{cx})*min(1,t/0.4)-overlay_w/2':y='{cy}+({Y0 + CH // 2}-{cy})*min(1,t/0.4)-overlay_h/2'[r1];"
      f"[7:v]format=rgba,fade=t=in:st=0.6:d=0.3:alpha=1[nm];[r1][nm]overlay=0:0,"
      f"fade=t=in:st=0:d=0.2:color=white,format=yuv420p[rev];"
      f"[lc][rev]concat=n=2:v=1:a=0,format=yuv420p[v]")
vin = ["-loop", "1", "-framerate", "30", "-t", str(LISTEN), "-i", f"{TMP}/sil.png"] + \
      sum((["-loop", "1", "-framerate", "30", "-t", "1", "-i", f"{TMP}/cd{k}.png"] for k in (3, 2, 1)), []) + \
      ["-loop", "1", "-framerate", "30", "-t", str(REVEAL), "-i", f"{TMP}/reveal-bg.png", "-i", REAL,
       "-loop", "1", "-framerate", "30", "-t", str(REVEAL), "-i", f"{TMP}/mask.png",
       "-loop", "1", "-framerate", "30", "-t", str(REVEAL), "-i", f"{TMP}/name.png",
       "-loop", "1", "-framerate", "30", "-t", str(REVEAL), "-i", f"{TMP}/card.png"]
cd = f"{R}/video-04/materiale/voci-noi/N-00-countdown-321.mp3"
praise = f"{R}/video-04/materiale/voci-noi/pip/P-lauda-1.mp3"
music = f"{R}/video-04/materiale/muzica/Baby_Animals_Playing_-_Joel_Cummins.mp3"
ev = [(SND, 0.2, (0, LISTEN - 0.4), -16), (cd, LISTEN, None, -16)]
t = T0 + 0.6
if ANS: ev.append((ANS, t, None, -16)); t += dur(ANS) + 0.1
ev += [(SND, t, (0, 3.2), -18), (praise, T0 + REVEAL - dur(praise) - 0.4, None, -16)]
ain, afc, lab = [], "", []
for i, (fl, st, tr, lvl) in enumerate(ev):
    g = lvl - mean(fl); tt = f"atrim={tr[0]}:{tr[1]},asetpts=PTS-STARTPTS,afade=t=out:st={tr[1] - tr[0] - 0.4}:d=0.4," if tr else ""
    ain += ["-i", fl]; ms = int(st * 1000)
    afc += f"[{9 + i}:a]{tt}aformat=sample_rates=48000:channel_layouts=stereo,volume={g:.1f}dB,adelay={ms}|{ms}[e{i}];"; lab.append(f"[e{i}]")
mi = 9 + len(ev)
afc += f"[{mi}:a]atrim=0:{TOT},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume='0.05+0.03*gte(t,{T0})':eval=frame[mu];"
afc += "".join(lab) + f"[mu]amix=inputs={len(lab) + 1}:normalize=0:duration=longest,atrim=0:{TOT},alimiter=limit=0.89[a]"
run(vin + ain + ["-stream_loop", "-1", "-i", music, "-filter_complex", fc + ";" + afc, "-map", "[v]", "-map", "[a]", "-t", str(TOT),
    "-c:v", "libx264", "-crf", "21", "-preset", "veryfast", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", OUT])
print("gata:", OUT, TOT)
