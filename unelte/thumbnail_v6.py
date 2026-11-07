"""Thumbnail Video 6 (stilul cu 14,7% CTR de la Video 5): imaginea sursă → utilajul devine siluetă neagră cu „?” mare.
Variante: thumbnail-final.jpg (curat), thumbnail-final-2.jpg (halou galben + cercul „20”)."""
import os, numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from scipy import ndimage as nd
from rembg import remove, new_session
HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "..", "canal", "video-06", "thumbnail")
FONT = os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff")
src = Image.open(f"{T}/sursa.jpg").convert("RGB")
sx, sy = 1920 / src.width, 1080 / src.height
im = src.resize((1920, 1080), Image.LANCZOS)
box = (int(990 * sx), int(30 * sy), 1920, int(1010 * sy))  # excavatorul gigant (dreapta)
crop = im.crop(box)
a = np.maximum(*(np.array(remove(crop, session=new_session(n), only_mask=True)).astype(float) / 255 for n in ("isnet-general-use", "isnet-anime")))
m = nd.binary_fill_holes(a > 0.4); lab, k = nd.label(m); sz = nd.sum(m, lab, range(1, k + 1)); m = lab == (np.argmax(sz) + 1)
m = nd.gaussian_filter(m.astype(float), 2.5) > 0.5
full = np.zeros((1080, 1920), bool); full[box[1]:box[3], box[0]:box[2]] = m
cy, cx = nd.center_of_mass(full)
q = Image.open(os.path.join(HERE, "..", "canal", "imagini", "suprapuneri", "semn-intrebare.png")); qc = q.crop(q.getbbox())
qc = qc.resize((int(qc.width * 1.2), int(qc.height * 1.2)), Image.LANCZOS)

def make(glow, badge, name):
    g = np.array(im).astype(float)
    if glow:
        gl = nd.gaussian_filter(nd.binary_dilation(full, iterations=22).astype(float), 16)[..., None]
        g = g * (1 - 0.9 * gl) + np.array([255, 236, 120.]) * 0.9 * gl
    base = Image.fromarray(g.clip(0, 255).astype("uint8"))
    base = Image.composite(Image.new("RGB", base.size, (22, 20, 24)), base, Image.fromarray((full * 255).astype("uint8"))).convert("RGBA")
    base.alpha_composite(qc, (int(cx) - qc.width // 2, int(cy) + 60 - qc.height // 2))
    if badge:
        d = ImageDraw.Draw(base); bx, by, r = 1790, 120, 86
        d.ellipse((bx - r - 8, by - r - 8, bx + r + 8, by + r + 8), fill=(255, 255, 255, 255)); d.ellipse((bx - r, by - r, bx + r, by + r), fill=(232, 52, 48, 255))
        d.text((bx, by - 4), "20", font=ImageFont.truetype(FONT, 98), fill=(255, 255, 255, 255), anchor="mm", stroke_width=8, stroke_fill=(59, 42, 32))
    out = base.convert("RGB").resize((1280, 720), Image.LANCZOS)
    out = ImageEnhance.Color(out).enhance(1.12); out = ImageEnhance.Contrast(out).enhance(1.04)
    out.save(f"{T}/{name}", quality=93)

make(False, False, "thumbnail-final.jpg")
make(True, True, "thumbnail-final-2.jpg")
print("gata", int(cx), int(cy))
