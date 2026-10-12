"""Suprapunerile cu text pentru Video 2 (numele animalelor + titlul din intro), în stilul de la Video 1."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff")
OUT = os.path.join(HERE, "..", "canal", "video-02", "imagini", "suprapuneri")
W, H = 1920, 1080
BROWN = (59, 42, 32, 255)

def text(s, size, fill, y, name, stroke=14):
    f = ImageFont.truetype(FONT, size)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w = d.textbbox((0, 0), s, font=f, stroke_width=stroke)[2]
    x = (W - w) // 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((x + 6, y + 8), s, font=f, fill=(0, 0, 0, 110), stroke_width=stroke, stroke_fill=(0, 0, 0, 110))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(im).text((x, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=BROWN)
    im.save(os.path.join(OUT, name))

ANIMALS = ["lion", "elephant", "monkey", "tiger", "wolf", "bear", "snake", "hippo", "parrot", "zebra",
           "gorilla", "hyena", "crocodile", "woodpecker", "fox", "deer", "rhino", "camel", "flamingo", "eagle"]
if __name__ == "__main__":
    text("Who Said Roar?", 150, (255, 255, 255, 255), 60, "intro-who-said-roar.png")
    for i, a in enumerate(ANIMALS, 1):
        text(a.upper(), 170, (255, 210, 63, 255), 838, f"animale/{i:02d}-{a}.png")
    print("gata")
