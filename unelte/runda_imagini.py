"""Face silueta + imaginile cu text pentru o rundă, din primul cadru al clipului.

Folosire: python3 runda_imagini.py <clip.mp4> <nr_runda> <x0,y0,x1,y1 cutie animal pe cadrul 1280x720>
"""
import sys, subprocess, os
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from rembg import remove, new_session

FFMPEG = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
ROOT = os.path.join(os.path.dirname(__file__), "..", "canal", "imagini")
OVL = os.path.join(ROOT, "suprapuneri")
W, H = 1920, 1080

clip, nr, box = sys.argv[1], int(sys.argv[2]), tuple(int(v) for v in sys.argv[3].split(","))
out = os.path.join(ROOT, f"runda-{nr:02d}")
os.makedirs(out, exist_ok=True)
f0 = os.path.join(out, "cadru-0.png")
subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", clip, "-vf", r"select=eq(n\,0)", "-frames:v", "1", f0], check=True)

im = Image.open(f0).convert("RGB")
w, h = im.size
m = np.array(remove(im.crop(box), session=new_session("isnet-general-use"), only_mask=True)) > 25
m = nd.binary_fill_holes(nd.binary_closing(m, structure=np.ones((5, 5))))
lab, n = nd.label(m)
m = lab == (np.argmax(nd.sum(m, lab, range(1, n + 1))) + 1)
full = np.zeros((h, w), bool)
full[box[1]:box[3], box[0]:box[2]] = m
cy, cx = nd.center_of_mass(full)

mask = Image.fromarray((full * 255).astype("uint8"))
sil = Image.composite(Image.new("RGB", (w, h), (22, 20, 24)), im, mask)
sil.save(os.path.join(out, "silueta-fara-semn.png"))

base = sil.convert("RGBA").resize((W, H), Image.LANCZOS)
q = Image.open(os.path.join(OVL, "semn-intrebare.png"))
qq = Image.new("RGBA", (W, H), (0, 0, 0, 0))
qq.alpha_composite(q, (int(cx * W / w) - W // 2, int(cy * H / h) - H // 2))

def save(extra, name):
    b = base.copy(); b.alpha_composite(qq)
    if extra: b.alpha_composite(Image.open(extra))
    b.convert("RGB").save(os.path.join(out, name))

save(os.path.join(OVL, "runde", f"round-{nr:02d}.png"), "1-round.png")
save(None, "2-silueta.png")
for n_ in range(5, 0, -1):
    save(os.path.join(OVL, "numaratoare", f"{n_}.png"), f"3-numaratoare-{n_}.png")
print("gata:", out, "centru animal:", int(cx), int(cy))
