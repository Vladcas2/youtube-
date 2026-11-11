"""Thumbnail Video 8: soneria (sau ușa) devine siluetă neagră; „?” potrivit pe mărimea ei; undele rămân colorate.
Folosire: thumbnail_v8.py <director> <sursa.jpg>"""
import sys, os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as nd
from rembg import remove, new_session
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff")
T, SRC = sys.argv[1:3]
src = Image.open(f"{T}/{SRC}").convert("RGB"); w, h = src.size
sam = new_session("sam")
def mask(box, pos, neg):
    p = [{"type": "rectangle", "data": box, "label": 1}] + [{"type": "point", "data": q, "label": 1} for q in pos] + \
        [{"type": "point", "data": q, "label": 0} for q in neg]
    m = np.array(remove(src, session=sam, only_mask=True, sam_prompt=p)) > 127
    m[:, :box[0]] = m[:, box[2]:] = False
    lab, k = nd.label(m); m = lab == (np.argmax(nd.sum(m, lab, range(1, k + 1))) + 1)
    hull = cv2.convexHull(np.argwhere(m)[:, ::-1].astype(np.int32))  # forme convexe: buton rotund, ușă
    out = np.zeros((h, w), np.uint8); cv2.fillPoly(out, [hull], 1)
    return out.astype(bool)
q = Image.open(os.path.join(HERE, "..", "canal", "imagini", "suprapuneri", "semn-intrebare.png")); q = q.crop(q.getbbox())
def make(m, qh, glow, badge, name):
    g = np.array(src).astype(float)
    if glow:
        gl = nd.gaussian_filter(nd.binary_dilation(m, iterations=18).astype(float), 14)[..., None]
        g = g * (1 - 0.85 * gl) + np.array([255, 236, 120.]) * 0.85 * gl
    g[m] = [22, 20, 24]
    im = Image.fromarray(g.clip(0, 255).astype("uint8")).convert("RGBA")
    ys, xs = np.nonzero(m); cx, cy = (xs.min() + xs.max()) // 2, (ys.min() + ys.max()) // 2
    qq = q.resize((int(q.width * qh / q.height), qh), Image.LANCZOS)
    im.alpha_composite(qq, (cx - qq.width // 2, cy - qq.height // 2))
    if badge:
        d = ImageDraw.Draw(im); r = 80; bx, by = w - r - 30, r + 30
        d.ellipse((bx - r, by - r, bx + r, by + r), fill=(229, 45, 39), outline=(255, 255, 255), width=10)
        d.text((bx, by), "20", font=ImageFont.truetype(FONT, 95), fill="white", anchor="mm")
    im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{T}/{name}.jpg", quality=92)
bell = mask([1700, 340, 1910, 600], [[1810, 470]], [])
door = mask([1230, 0, 1655, 1030], [[1440, 300], [1440, 800], [1330, 500]], [[1810, 470], [1700, 300]])
make(bell, 250, False, False, "thumbnail-sonerie"); make(bell, 250, True, True, "thumbnail-sonerie-2")
make(door, 520, False, False, "thumbnail-usa"); make(door, 520, True, True, "thumbnail-usa-2")
print("gata")
