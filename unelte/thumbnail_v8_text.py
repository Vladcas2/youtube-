"""Thumbnail Video 8 cu „WHO SAID DING DONG?” sus, ca la Video 3 și 4 (peste variantele cu siluetă)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "..", "canal", "video-08", "thumbnail")
FONT = os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff")
BROWN = (59, 42, 32, 255)
TXT = "WHO SAID DING DONG?"
for src, out in (("thumbnail-sonerie-2.jpg", "who-said-ding-dong.jpg"), ("thumbnail-usa-2.jpg", "who-said-ding-dong-usa.jpg")):
    im = Image.open(f"{T}/{src}").convert("RGBA")
    f = ImageFont.truetype(FONT, 88)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((46, 26), TXT, font=f, fill=(0, 0, 0, 140), stroke_width=11, stroke_fill=(0, 0, 0, 140))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(im).text((40, 18), TXT, font=f, fill=(255, 255, 255, 255), stroke_width=11, stroke_fill=BROWN)
    im.convert("RGB").save(f"{T}/{out}", quality=92)
print("gata")
