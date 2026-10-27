"""Suprapunerile cu text pentru Video 4: numele vehiculelor, titlul din intro (în dreapta, Pip e în stânga) și cartonașul BONUS ROUND."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import texte_v2
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "canal", "video-04", "imagini", "suprapuneri")
os.makedirs(os.path.join(OUT, "animale"), exist_ok=True)
texte_v2.OUT = OUT
W, H = 1920, 1080

def text_la(lines, size, fill, cx, y, name, stroke=14):
    """Ca texte_v2.text, dar pe mai multe rânduri, centrat pe cx."""
    f = ImageFont.truetype(texte_v2.FONT, size)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for k, s in enumerate(lines):
        w = ImageDraw.Draw(im).textbbox((0, 0), s, font=f, stroke_width=stroke)[2]
        x, yy = cx - w // 2, y + k * int(size * 1.1)
        ImageDraw.Draw(sh).text((x + 6, yy + 8), s, font=f, fill=(0, 0, 0, 110), stroke_width=stroke, stroke_fill=(0, 0, 0, 110))
        lines[k] = (x, yy, s)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    for x, yy, s in lines:
        ImageDraw.Draw(im).text((x, yy), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=texte_v2.BROWN)
    im.save(os.path.join(OUT, name))

VEHICLES = ["school bus", "big truck", "bullet train", "tram", "speedboat", "propeller plane", "subway train", "tow truck",
            "fighter jet", "monster truck", "scooter", "horse carriage", "jet ski", "lawn mower", "go-kart", "pirate ship",
            "snowmobile", "roller coaster", "street sweeper", "fire boat"]
if __name__ == "__main__":
    text_la(["Who Said", "Honk Honk?"], 150, (255, 255, 255, 255), 1390, 40, "intro-who-said-honk.png")
    text_la(["BONUS ROUND!"], 190, (255, 210, 63, 255), W // 2, 90, "bonus-round.png", stroke=16)
    for i, a in enumerate(VEHICLES, 1):
        texte_v2.text(a.upper(), 170 if len(a) <= 13 else 150, (255, 210, 63, 255), 838, f"animale/{i:02d}-{a.replace(' ', '-')}.png")
    print("gata")
