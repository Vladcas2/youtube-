"""Siluetă precisă cu SAM: marchezi cu puncte animalul (+) și fundalul lipit de el (-).

Folosire: python3 runda_sam.py <nr_runda> "x,y;x,y;..." "x,y;..." [doar-sam]   (coordonate pe cadru-0.png al rundei)
"""
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from rembg import remove, new_session

ROOT = os.path.join(os.path.dirname(__file__), "..", "canal", "imagini")
OVL = os.path.join(ROOT, "suprapuneri")
W, H = 1920, 1080
nr = int(sys.argv[1])
pts = lambda s: [[int(v) for v in p.split(",")] for p in s.split(";") if p]
pos, neg = pts(sys.argv[2]), pts(sys.argv[3]) if len(sys.argv) > 3 else []
out = os.path.join(ROOT, f"runda-{nr:02d}")
im = Image.open(os.path.join(out, "cadru-0.png")).convert("RGB")
w, h = im.size
prompt = [{"type": "point", "data": p, "label": 1} for p in pos] + [{"type": "point", "data": p, "label": 0} for p in neg]
m = np.array(remove(im, session=new_session("sam"), only_mask=True, sam_prompt=prompt)) > 127
# completăm cu modelele obișnuite în zona animalului (capul/fața le scapă uneori lui SAM);
# dacă fundalul se lipește de animal (acoperiș, frunză), rulează cu al 4-lea argument „doar-sam”
ys, xs = np.where(m); pad = 25
x0, y0, x1, y1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(w, xs.max() + pad), min(h, ys.max() + 1)
crop = im.crop((x0, y0, x1, y1)); extra = np.zeros(crop.size[::-1], bool)
for name in (() if len(sys.argv) > 4 and sys.argv[4] == "doar-sam" else ("isnet-general-use", "isnet-anime")):
    extra |= np.array(remove(crop, session=new_session(name), only_mask=True)) > 60
m[y0:y1, x0:x1] |= extra
m = nd.binary_fill_holes(nd.binary_closing(m, structure=np.ones((5, 5))))
lab, n = nd.label(m)
m = lab == (np.argmax(nd.sum(m, lab, range(1, n + 1))) + 1)
cy, cx = nd.center_of_mass(m)
sil = Image.composite(Image.new("RGB", (w, h), (22, 20, 24)), im, Image.fromarray((m * 255).astype("uint8")))
sil.save(os.path.join(out, "silueta-fara-semn.png"))
base = sil.convert("RGBA").resize((W, H), Image.LANCZOS)
qq = Image.new("RGBA", (W, H), (0, 0, 0, 0))
qq.alpha_composite(Image.open(os.path.join(OVL, "semn-intrebare.png")), (int(cx * W / w) - W // 2, int(cy * H / h) - H // 2))
def save(extra, name):
    b = base.copy(); b.alpha_composite(qq)
    if extra: b.alpha_composite(Image.open(extra))
    b.convert("RGB").save(os.path.join(out, name))
save(os.path.join(OVL, "runde", f"round-{nr:02d}.png"), "1-round.png")
save(None, "2-silueta.png")
for k in range(5, 0, -1):
    save(os.path.join(OVL, "numaratoare", f"{k}.png"), f"3-numaratoare-{k}.png")
print("gata:", out)
