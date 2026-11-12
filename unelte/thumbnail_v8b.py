"""Thumbnail Video 8, varianta 2: aspiratorul mare devine siluetă cu „?”; cu și fără „WHO SAID DING DONG?” sus."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage as nd
from rembg import remove, new_session
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(HERE, "..", "canal", "video-08", "thumbnail")
FONT = os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff"); BROWN = (59, 42, 32, 255)
src = Image.open(f"{T}/sursa-aspirator.jpg").convert("RGB"); w, h = src.size
p = [{"type": "rectangle", "data": [1250, 210, 1900, 1060], "label": 1}, {"type": "point", "data": [1600, 700], "label": 1}]  # un singur punct: forma cea mai curată
m = np.array(remove(src, session=new_session("sam"), only_mask=True, sam_prompt=p)) > 127
m = nd.binary_fill_holes(nd.binary_closing(m, np.ones((5, 5))))
lab, k = nd.label(m); m = lab == (np.argmax(nd.sum(m, lab, range(1, k + 1))) + 1)
m = nd.gaussian_filter(m.astype(float), 2) > 0.5
q = Image.open(os.path.join(HERE, "..", "canal", "imagini", "suprapuneri", "semn-intrebare.png")); q = q.crop(q.getbbox())
ys, xs = np.nonzero(m); cx, cy = 1610, 690  # pe corpul aspiratorului
def make(text, name):
    g = np.array(src).astype(float)
    gl = nd.gaussian_filter(nd.binary_dilation(m, iterations=22).astype(float), 16)[..., None]
    g = g * (1 - 0.85 * gl) + np.array([255, 236, 120.]) * 0.85 * gl
    g[m] = [22, 20, 24]
    im = Image.fromarray(g.clip(0, 255).astype("uint8")).convert("RGBA")
    qh = 400; qq = q.resize((int(q.width * qh / q.height), qh), Image.LANCZOS)
    im.alpha_composite(qq, (cx - qq.width // 2, cy - qq.height // 2))
    im = im.resize((1280, 720), Image.LANCZOS); d = ImageDraw.Draw(im)
    r = 62; bx, by = 1280 - r - 22, r + 22
    if text:
        f = ImageFont.truetype(FONT, 92); s = "WHO SAID DING DONG?"
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((52, 30), s, font=f, fill=(0, 0, 0, 130), stroke_width=11, stroke_fill=(0, 0, 0, 130))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(im)
        d.text((46, 22), s, font=f, fill=(255, 255, 255, 255), stroke_width=11, stroke_fill=BROWN)
    d.ellipse((bx - r - 6, by - r - 6, bx + r + 6, by + r + 6), fill=(255, 255, 255, 255))
    d.ellipse((bx - r, by - r, bx + r, by + r), fill=(229, 45, 39, 255))
    d.text((bx, by), "20", font=ImageFont.truetype(FONT, 72), fill="white", anchor="mm", stroke_width=6, stroke_fill=BROWN)
    im.convert("RGB").save(f"{T}/{name}", quality=92)
make(True, "aspirator-text.jpg"); make(False, "aspirator.jpg"); print("gata")
