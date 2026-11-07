"""Thumbnail cu siluetă precisă (SAM): imaginea sursă → utilajul devine siluetă neagră cu „?”.
Folosire: thumbnail_sam.py <director> <sursa.jpg> x0,y0,x1,y1 "x,y;x,y" "x,y;..." <prefix>   (coordonate în pixelii sursei)
Face <prefix>.jpg (curat) și <prefix>-2.jpg (halou galben + cercul „20”)."""
import sys, os, numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from scipy import ndimage as nd
from rembg import remove, new_session
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff")
T, SRC, BOX, POS, NEG, PRE = sys.argv[1:7]
pts = lambda s: [[int(v) for v in p.split(",")] for p in s.split(";") if p]
src = Image.open(f"{T}/{SRC}").convert("RGB")
prompt = [{"type": "rectangle", "data": [int(v) for v in BOX.split(",")], "label": 1}] + \
         [{"type": "point", "data": p, "label": 1} for p in pts(POS)] + [{"type": "point", "data": p, "label": 0} for p in pts(NEG)]
m = np.array(remove(src, session=new_session("sam"), only_mask=True, sam_prompt=prompt)) > 127
m = nd.binary_closing(m, structure=np.ones((5, 5)))
if not os.environ.get("FARA_GOLURI"): m = nd.binary_fill_holes(m)  # FARA_GOLURI=1 păstrează golurile (cerul dintre brațe și cabluri)
lab, k = nd.label(m); m = lab == (np.argmax(nd.sum(m, lab, range(1, k + 1))) + 1)
m = nd.gaussian_filter(m.astype(float), 2.5) > 0.5
im = src.resize((1920, 1080), Image.LANCZOS)
full = np.array(Image.fromarray((m * 255).astype("uint8")).resize((1920, 1080))) > 127
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
    base.alpha_composite(qc, (int(cx) - qc.width // 2, int(cy) + 40 - qc.height // 2))
    if badge:
        d = ImageDraw.Draw(base); bx, by, r = 1790, 120, 86
        d.ellipse((bx - r - 8, by - r - 8, bx + r + 8, by + r + 8), fill=(255, 255, 255, 255)); d.ellipse((bx - r, by - r, bx + r, by + r), fill=(232, 52, 48, 255))
        d.text((bx, by - 4), "20", font=ImageFont.truetype(FONT, 98), fill=(255, 255, 255, 255), anchor="mm", stroke_width=8, stroke_fill=(59, 42, 32))
    out = base.convert("RGB").resize((1280, 720), Image.LANCZOS)
    out = ImageEnhance.Color(out).enhance(1.12); out = ImageEnhance.Contrast(out).enhance(1.04)
    out.save(f"{T}/{name}", quality=93)
make(False, False, f"{PRE}.jpg"); make(True, True, f"{PRE}-2.jpg")
print("gata", int(cx), int(cy))
