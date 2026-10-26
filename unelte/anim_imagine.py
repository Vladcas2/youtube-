# Animatie simpla dintr-o imagine statica (cand Hailuo nu merge):
# decupeaza Pip si vehiculul cu rembg, umple golul din fundal, apoi
# Pip topaie, vehiculul se leagana/vibreaza, toata scena are zoom lent.
# Folosire: anim_imagine.py imagine.jpg iesire.mp4 pip=x0,y0,x1,y1 veh=x0,y0,x1,y1 [mod=leagan|vibrare] [taie=x0,y0,x1,y1 ...]
import sys, math, subprocess, numpy as np, imageio_ffmpeg
from PIL import Image
from scipy.ndimage import gaussian_filter, binary_dilation
from rembg import remove, new_session

src, out = sys.argv[1], sys.argv[2]
a = dict(x.split("=", 1) for x in sys.argv[3:] if not x.startswith("taie="))
taie = [tuple(map(int, x[5:].split(","))) for x in sys.argv[3:] if x.startswith("taie=")]
W, H, FPS, DUR = 1920, 1080, 30, 5.0
img = Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)
sx, sy = W / Image.open(src).width, H / Image.open(src).height
S = new_session("isnet-general-use")

def strat(box):
    x0, y0, x1, y1 = [int(v * (sx if i % 2 == 0 else sy)) for i, v in enumerate(map(int, box.split(",")))]
    al = np.array(remove(img.crop((x0, y0, x1, y1)), session=S))[..., 3].astype(np.float32) / 255
    full = np.zeros((H, W), np.float32); full[y0:y1, x0:x1] = al
    for t in taie:  # zone de scos din masca (bucati de gard, felinar...)
        tx0, ty0, tx1, ty1 = int(t[0] * sx), int(t[1] * sy), int(t[2] * sx), int(t[3] * sy)
        if tx0 < x1 and tx1 > x0 and ty0 < y1 and ty1 > y0: full[ty0:ty1, tx0:tx1] = 0
    rgba = np.dstack([np.array(img), (full * 255).astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA"), full, (x0, y0, x1, y1)

pip, mp, bp = strat(a["pip"])
veh, mv, bv = strat(a["veh"])
mod = a.get("mod", "leagan")

# umple golul din spatele lui Pip (si al vehiculului la leagan) prin convolutie normalizata
gol = mp > 0.1
if mod == "leagan": gol |= mv > 0.1
gol = binary_dilation(gol, iterations=6)
fund = np.array(img).astype(np.float32); cun = (~gol).astype(np.float32)
umplut = fund.copy()
for sig in (64, 24, 8):
    num = np.dstack([gaussian_filter(fund[..., c] * cun, sig) for c in range(3)])
    den = gaussian_filter(cun, sig)[..., None] + 1e-6
    umplut[gol] = (num / den)[gol]
fund = Image.fromarray(umplut.clip(0, 255).astype(np.uint8))

def pune(cadru, strat_, box, ang, dx, dy, sc, ancora):
    x0, y0, x1, y1 = box
    piesa = strat_.crop((x0, y0, x1, y1))
    w, h = piesa.size
    piesa = piesa.resize((int(w * sc), int(h * sc)), Image.BICUBIC)
    ax, ay = ancora  # punct fix (picioare / centru), relativ la box
    piesa = piesa.rotate(ang, Image.BICUBIC, expand=False, center=(ax * sc, ay * sc))
    cadru.alpha_composite(piesa, (int(x0 + ax - ax * sc + dx), int(y0 + ay - ay * sc + dy)))

ff = imageio_ffmpeg.get_ffmpeg_exe()
p = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out], stdin=subprocess.PIPE)
pa = ((bp[2] - bp[0]) / 2, (bp[3] - bp[1]) * 0.97)        # Pip: ancora la picioare
va = ((bv[2] - bv[0]) / 2, (bv[3] - bv[1]) / 2)           # vehicul: ancora in centru
for i in range(int(DUR * FPS)):
    t = i / FPS
    c = fund.convert("RGBA")
    if mod == "leagan":
        pune(c, veh, bv, 2.0 * math.sin(2 * math.pi * 0.9 * t), 0, 5 * math.sin(2 * math.pi * 1.8 * t), 1.0, va)
    else:
        pune(c, veh, bv, 0.4 * math.sin(2 * math.pi * 7 * t), 1.5 * math.sin(2 * math.pi * 11 * t), 3 * math.sin(2 * math.pi * 9 * t), 1.0, va)
    hop = abs(math.sin(math.pi * 1.4 * t))
    pune(c, pip, bp, 3 * math.sin(2 * math.pi * 0.7 * t), 0, -22 * hop, 1.0 + 0.02 * (1 - hop), pa)
    z = 1.0 + 0.04 * t / DUR                                # zoom lent
    zw, zh = W / z, H / z
    c = c.convert("RGB").crop((int((W - zw) / 2), int((H - zh) / 2), int((W + zw) / 2), int((H + zh) / 2))).resize((W, H), Image.BICUBIC)
    p.stdin.write(c.tobytes())
p.stdin.close(); p.wait()
print("ok", out)
