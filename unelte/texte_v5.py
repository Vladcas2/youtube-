"""Suprapunerile cu text pentru Video 5 (construcții) + butonul „Subscribe” de după hook."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import texte_v2, texte_v4
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "canal", "video-05", "imagini", "suprapuneri")
os.makedirs(os.path.join(OUT, "animale"), exist_ok=True)
texte_v2.OUT = texte_v4.OUT = OUT
W, H = 1920, 1080

def subscribe(name):
    """Buton roșu „SUBSCRIBE” cu clopoțel, în colțul din dreapta jos."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bw, bh, x0, y0 = 470, 120, W - 470 - 60, H - 120 - 60
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0 + 6, y0 + 10, x0 + bw + 6, y0 + bh + 10), 30, fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), 30, fill=(229, 45, 39, 255), outline=(255, 255, 255, 255), width=6)
    f = ImageFont.truetype(texte_v2.FONT, 62)
    d.text((x0 + 40, y0 + 22), "SUBSCRIBE", font=f, fill=(255, 255, 255, 255))
    # clopoțel
    cx, cy = x0 + bw - 62, y0 + bh // 2
    d.pieslice((cx - 26, cy - 34, cx + 26, cy + 18), 180, 360, fill=(255, 210, 63, 255))
    d.rectangle((cx - 26, cy - 8, cx + 26, cy + 14), fill=(255, 210, 63, 255))
    d.rounded_rectangle((cx - 34, cy + 10, cx + 34, cy + 20), 4, fill=(255, 210, 63, 255))
    d.ellipse((cx - 9, cy + 18, cx + 9, cy + 34), fill=(255, 210, 63, 255))
    im.save(os.path.join(OUT, name))

MACHINES = ["excavator", "dump truck", "cement mixer", "jackhammer", "forklift", "crane", "bulldozer", "hammer", "power drill",
            "mining truck", "pile driver", "wrecking ball", "chainsaw", "circular saw", "nail gun", "road roller", "wood chipper",
            "angle grinder", "wheelbarrow", "shovel"]
if __name__ == "__main__":
    texte_v4.text_la(["Who Said", "Rumble Rumble?"], 140, (255, 255, 255, 255), 1390, 30, "intro-who-said-rumble.png")
    texte_v4.text_la(["BONUS ROUND!"], 190, (255, 210, 63, 255), W // 2, 90, "bonus-round.png", stroke=16)
    texte_v4.text_la(["You did it!"], 190, (255, 210, 63, 255), W // 2, 640, "final-you-did-it.png", stroke=16)
    f = Image.open(os.path.join(OUT, "final-you-did-it.png"))
    texte_v4.text_la(["All 20 machines!"], 120, (255, 255, 255, 255), W // 2, 870, "_tmp.png")
    f.alpha_composite(Image.open(os.path.join(OUT, "_tmp.png"))); f.save(os.path.join(OUT, "final-you-did-it.png"))
    os.remove(os.path.join(OUT, "_tmp.png"))
    subscribe("subscribe.png")
    for i, a in enumerate(MACHINES, 1):
        texte_v2.text(a.upper(), 170 if len(a) <= 13 else 150, (255, 210, 63, 255), 838, f"animale/{i:02d}-{a.replace(' ', '-')}.png")
    print("gata")
