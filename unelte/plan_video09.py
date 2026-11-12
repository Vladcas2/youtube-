"""Face planul pentru Video 9 (instrumente, format nou: imagine desenată + video real la dezvăluire)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
PIP = "Pip, a small round coral-orange baby owl with a cream face, big mint-green eyes, a tiny orange beak and oversized teal headphones"
STYLE = "2D cartoon children's illustration, soft cel shading, subtle feather texture, clean dark-brown outlines, bright warm palette of sunny yellow, coral, mint green, teal and cream, rounded cute shapes"
G = ["holding one wing to its ear, listening with a curious smile", "clapping its wings happily", "waving one wing",
     "sitting calmly with both wings folded, big smile", "bouncing happily", "pointing at the instrument with one wing, beak open in surprise"]
MUSIC = "cozy cartoon music room with a rug, a shelf with books and a window with sunshine, warm soft light"
STAGE = "small cozy cartoon concert stage with red curtains, a wooden floor and warm spotlights"
PARK = "sunny cartoon park with green grass, a few trees and a clear light blue sky, bright warm light"
SCHOOL = "bright cartoon music classroom with colorful notes on the wall and a big window, soft light"
# nr, en, ro, art, sunet (Pixabay), video real (Pexels/Pixabay), desen, unde stă Pip, fundal
A = [
(1, "drum", "tobă", "a", "snare drum beat", "drum close up / snare drum", "A big red cartoon snare drum with a white drumhead and two wooden drumsticks resting on top, side view", "sitting on a small wooden stool on the left", MUSIC),
(2, "piano", "pian", "a", "piano melody short", "grand piano playing / piano keys", "A shiny black cartoon grand piano with its lid open and white and black keys, side view facing right", "sitting on the piano bench on the left", STAGE),
(3, "guitar", "chitară", "a", "acoustic guitar strum", "acoustic guitar playing", "A warm brown cartoon acoustic guitar standing on a stand, front view", "sitting on a small wooden stool on the left", MUSIC),
(4, "trumpet", "trompetă", "a", "trumpet fanfare", "trumpet playing / trumpet player", "A shiny golden cartoon trumpet floating at an angle, side view facing right, the bell pointing right", "sitting on a stack of music books on the left", STAGE),
(5, "violin", "vioară", "a", "violin melody short", "violin playing / violinist", "A warm orange-brown cartoon violin with its bow, standing upright, front view", "sitting on a little music stand on the left", MUSIC),
(6, "xylophone", "xilofon", "a", "xylophone", "xylophone playing", "A colorful cartoon xylophone with rainbow bars and two mallets with round tips, on a table, three-quarter view", "sitting on a small table on the left", SCHOOL),
(7, "tambourine", "tamburină", "a", "tambourine shake", "tambourine shaking", "A round cartoon tambourine with a wooden frame and shiny little jingles around the edge, front view, tilted a little", "sitting on a cushion on the left", MUSIC),
(8, "flute", "flaut", "a", "flute melody", "flute playing / flutist", "A long shiny silver cartoon flute floating horizontally, side view", "sitting on a stack of music books on the left", PARK),
(9, "maracas", "maracase", "they", "maracas shaking", "maracas shaking", "Two bright colorful cartoon maracas with round heads and striped handles, crossed, front view", "sitting on a small wooden stool on the left", PARK),
(10, "gong", "gong", "a", "gong hit", "gong hit / gong instrument", "A big shiny golden cartoon gong hanging in a red wooden frame, with a soft mallet next to it, front view", "sitting on a cushion on the left", STAGE),
(11, "saxophone", "saxofon", "a", "saxophone melody", "saxophone player / saxophone playing", "A shiny golden cartoon saxophone standing on a stand, side view facing right", "sitting on a small wooden stool on the left", STAGE),
(12, "harmonica", "muzicuță", "a", "harmonica", "harmonica playing", "A big shiny silver-and-red cartoon harmonica, front view, slightly tilted", "sitting on a tree stump on the left", PARK),
(13, "triangle", "triunghi", "a", "triangle instrument ding", "triangle instrument", "A shiny silver cartoon triangle instrument hanging from a little string with a small metal beater next to it, front view", "sitting on a small table on the left", SCHOOL),
(14, "accordion", "acordeon", "an", "accordion", "accordion player / accordion playing", "A bright red cartoon accordion with white keys and stretched pleated bellows, front view", "sitting on a cushion on the left", MUSIC),
(15, "cymbals", "talgere", "they", "cymbals crash", "cymbals crash / hand cymbals", "Two big shiny golden cartoon cymbals with leather straps, held face to face a little apart, front view", "sitting on a small wooden stool on the left", STAGE),
(16, "harp", "harpă", "a", "harp glissando", "harp playing / harpist", "A tall golden cartoon harp with many strings, side view", "sitting on a cushion on the left", STAGE),
(17, "trombone", "trombon", "a", "trombone slide", "trombone player / trombone playing", "A shiny golden cartoon trombone with its long slide, side view facing right", "sitting on a stack of music books on the left", PARK),
(18, "banjo", "banjo", "a", "banjo", "banjo playing", "A cartoon banjo with a round white drum-like body and a long wooden neck, standing on a stand, front view", "sitting on a hay bale on the left", PARK),
(19, "tuba", "tubă", "a", "tuba", "tuba player / tuba playing", "A very big shiny golden cartoon tuba with a huge bell pointing up, front view", "sitting on a small wooden stool on the left", STAGE),
(20, "bagpipes", "cimpoi", "they", "bagpipes", "bagpipes player / bagpipes", "Cartoon bagpipes with a tartan red-and-green bag and three wooden pipes sticking up, front view", "sitting on a tree stump on the left", PARK),
]
def answer(a):
    art, en = a[3], a[1].upper()
    return f"They're {en}!" if art == "they" else f"It's {art} {en}!"

out = []; w = out.append
w("# Video 9 — „Who Said BOOM BOOM?” Musical Instruments Quiz (engleză)\n")
w("> Tema dovedită la canalul model (Little Dreamers: „Guess The Musical Instrument Sounds” = 512.000 de vizionări; Short-ul cu instrumente = 332.000).")
w("> **Format nou:** silueta din **imagine desenată** (nu mai trebuie clipuri animate pe runde) + **un singur sunet lung** + la dezvăluire **video REAL** cu instrumentul, într-un cartonaș, cu Pip în colț.")
w("> Proba cu toba: `canal/video-09/proba/proba-runda-drum.mp4`.\n")
w("---\n\n## Cum arată o rundă\n")
w("1. Imaginea desenată, instrumentul = **siluetă neagră cu „?”**; se aude **sunetul o dată, lung (~5 s)**.")
w("2. **3-2-1**.")
w("3. Flash → **cartonașul cu video-ul real** crește din siluetă; Pip (poza ta decupată) în colț; numele mare dedesubt.")
w("4. Naratorul: „It's a DRUM!” → **sunetul real** pe video → Pip laudă.\n")
w("Rămân: hook-ul de 5 s, intro scurt + Subscribe, runda 10 = **BONUS** (gong), finalul cu Pip.")
w("Vocile pentru „Round 1…20”, numărătoare, întrebări și laude le refolosesc. **Voci noi: 22** (20 de răspunsuri + 2 ale lui Pip).\n")
w("---\n\n## Ce trebuie pentru fiecare rundă (3 lucruri)\n")
w("| Ce | De unde | Nume fișier |\n|---|---|---|")
w("| **Imagine desenată** (Pip + instrumentul) | promptul de mai jos | `01-drum.jpg` |")
w("| **Video real** cu instrumentul | **pexels.com/videos** sau **pixabay.com/videos** | `01-drum-real.mp4` |")
w("| **Sunetul** | **pixabay.com/sound-effects** (rezervă: freesound.org, CC0) | `01-drum.mp3` |\n")
w("**Video-ul real — cum alegi:** orizontal, Full HD; **instrumentul se vede clar** (mâini și oameni sunt OK); camera cât mai liniștită; măcar 8 s. Nu contează dacă e mut (cele mai multe de pe Pexels sunt) — sunetul îl pun eu din fișierul de sunet.\n")
w("**Sunetul — cum alegi:** doar instrumentul (fără acompaniament, fără voci), **o frază scurtă de 4–6 s** (câteva note / un ritm), nu o singură notă.\n")
w("---\n\n## Lista\n")
w("| # | Instrument | Română | Sunet (Pixabay) | Video real (Pexels) | Narator |\n|---|---|---|---|---|---|")
for a in A:
    w(f"| {a[0]} | {a[1]}{' ⭐ BONUS' if a[0] == 10 else ''} | {a[2]} | `{a[4]}` | `{a[5]}` | {answer(a)} |")
w("\n**Rezerve:** `ukulele`, `recorder`, `bongo drums`, `music box`, `whistle`, `bells / handbells`.\n")
w("---\n\n## Vocile (22)\n")
w("**Narator** (WST – Narator), în ordinea rundelor:\n```")
for a in A: w(answer(a))
w("```\n**Pip** (WST – Pip):\n```\nWho said BOOM BOOM?\nYou did it! All twenty instruments!\n```")
w("Setări ca până acum: **Multilingual v2**, Speed 0.9, Stability 45, Similarity 75, Style 30. Generează-le **în ordine** (1 → 20), ca să le potrivesc ușor.\n")
w("---\n\n## Imaginile desenate (20)\n")
w("Folosește `canal/pip-intreg.png` ca referință pentru Pip. **Instrumentul întreg, cu spațiu liber în jur, nu atinge marginile** — din el fac silueta. **Fără text.** Doar imagine, **fără clip**.\n")
for i, a in enumerate(A):
    nr, en, ro, art, snd, vid, desc, place, bg = a
    w(f"### {nr}. {en.upper()} ({ro}){' — BONUS' if nr == 10 else ''}\n```")
    w(f"Wide horizontal 16:9 landscape composition. {desc}, the whole {en} clearly visible with empty space around it, not touching the frame edges, not overlapping anything, the {en} is the main subject in the center-right of the frame, small musical notes floating near it. {PIP}, {place}, {G[i % len(G)]}. Background: {bg}, medium-wide shot. {STYLE}. Landscape orientation, 16:9, 1920x1080. The owl wears its oversized teal headphones and no hat. No text, no letters, no words, no numbers in the image.")
    w("```\n")
w("---\n\n## Intro și final (imagine + clip de 5 s, ca până acum)\n")
w("### INTRO\n**Imagine:**\n```")
w(f"Wide horizontal 16:9 landscape composition. {PIP}, standing on a fluffy rug in a cozy cartoon music room and waving one wing at the viewer, a red drum, a guitar on a stand, a golden trumpet and a colorful xylophone around, empty wall space on the upper right for a title, warm sunny light, medium shot. {STYLE}. Landscape orientation, 16:9, 1920x1080. No text, no letters, no words in the image.")
w("```\n**Clip:**\n```\n5-second video. Static camera. The owl bounces gently on the rug, waves one wing twice and looks at the camera, keeping its headphones on. Everything else stays in place. Smooth cartoon animation, no morphing, the owl stays in the frame the whole time, keep the style unchanged.\n```\n")
w("### FINAL\n**Imagine:**\n```")
w(f"Wide horizontal 16:9 landscape composition. {PIP}, BIG in the center, wearing a shiny gold medal, standing on a small cartoon concert stage with red curtains, surrounded by a drum, a guitar, a trumpet, a violin, a xylophone and maracas, colorful confetti in the air, warm spotlights. {STYLE}. Landscape orientation, 16:9, 1920x1080. No text, no letters, no words in the image.")
w("```\n**Clip:**\n```\n5-second video. Static camera. The owl claps its wings happily, bounces and smiles at the camera, keeping its headphones and medal on, confetti falls slowly. The instruments stay in place. Smooth cartoon animation, no morphing, the owl stays in the frame the whole time, keep the style unchanged.\n```\n")
w("---\n\n## Thumbnail\n\nStilul cu **14,7% CTR**: Pip mare, instrumentul colorat (silueta + „?” le fac eu).\n```")
w(f"YouTube thumbnail for a toddler sound quiz, wide 16:9, 2D cartoon children's illustration, bold and super colorful, high contrast, very simple composition readable at small size. LEFT (35% of the frame): {PIP}, BIG and close to the camera, beak wide open in excitement, one wing cupped to its ear, the other wing pointing at the drum. RIGHT (60%): ONE big bright red drum with two drumsticks and cartoon sound waves, three-quarter view, fully visible, not touching the frame edges. BACKGROUND: cozy cartoon music room, warm soft light, simple and lighter than the characters. {STYLE}. No text, no letters, no numbers, no logos, no question marks. The owl and the drum do not touch.")
w("```\n\n---\n\n## Ordinea în care să le trimiți\n")
w("1. Sunetele (20) → 2. Vocile (22) → 3. Imaginile desenate (20) + intro + final → 4. Video-urile reale (20) → 5. Imaginea de thumbnail.")
w("Cu „nu fă nik” le salvez; când sunt toate, fac montajul.\n")
w("**Deja avem:** imaginea cu toba (`canal/video-09/proba/01-drum.jpg`), video-ul real cu toba, poza decupată a lui Pip.")
open(os.path.join(HERE, "..", "canal", "video-09-instrumente.md"), "w").write("\n".join(out) + "\n")
print("gata")
