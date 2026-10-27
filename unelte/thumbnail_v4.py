"""Thumbnail Video 4: imaginea sursă + „WHO SAID HONK HONK?” + cercul „20”, ca la Video 3."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "..", "canal", "video-04", "thumbnail")
FONT = os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff")
BROWN = (59, 42, 32, 255)
im = Image.open(f"{T}/sursa.webp").convert("RGBA").resize((1280, 720), Image.LANCZOS)
def scris(d, xy, s, f, fill, stroke):
    d.text(xy, s, font=f, fill=fill, stroke_width=stroke, stroke_fill=BROWN)
f = ImageFont.truetype(FONT, 86)
sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
ImageDraw.Draw(sh).text((46, 30), "WHO SAID HONK HONK?", font=f, fill=(0, 0, 0, 120), stroke_width=10, stroke_fill=(0, 0, 0, 120))
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
d = ImageDraw.Draw(im)
scris(d, (40, 22), "WHO SAID HONK HONK?", f, (255, 255, 255, 255), 10)
cx, cy, r = 1196, 84, 66
d.ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), fill=(255, 255, 255, 255))
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(240, 98, 85, 255))
f2 = ImageFont.truetype(FONT, 76)
w = d.textbbox((0, 0), "20", font=f2, stroke_width=8)
scris(d, (cx - (w[2] - w[0]) // 2, cy - (w[3] - w[1]) // 2 - 8), "20", f2, (255, 255, 255, 255), 8)
im.convert("RGB").save(f"{T}/who-said-honk.jpg", quality=92)
print("gata")
