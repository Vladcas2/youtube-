"""Face planul pentru Video 10 (animale, formatul de la Video 9: imagine desenată + video real la dezvăluire)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
PIP = "Pip, a small round coral-orange baby owl with a cream face, big mint-green eyes, a tiny orange beak and oversized teal headphones"
STYLE = "2D cartoon children's illustration, soft cel shading, subtle feather texture, clean dark-brown outlines, bright warm palette of sunny yellow, coral, mint green, teal and cream, rounded cute shapes"
G = ["holding one wing to its ear, listening with a curious smile", "clapping its wings happily", "waving one wing",
     "sitting calmly with both wings folded, big smile", "bouncing happily", "pointing at the animal with one wing, beak open in surprise"]
FARM = "sunny cartoon farm with a red barn, a wooden fence, green grass and a clear light blue sky, bright warm light"
SEA = "sunny cartoon seaside with blue water, a sandy beach and a clear light blue sky, bright warm light"
ICE = "bright cartoon icy shore with white snow, blue icebergs and a pale blue sky, soft light"
FOREST = "sunny cartoon forest with tall green trees, ferns and soft sunbeams, warm light"
SAVANNA = "sunny cartoon African savanna with golden grass, acacia trees and a clear sky, bright warm light"
RIVER = "sunny cartoon riverbank with reeds, green water and lily pads, bright warm light"
LAKE = "calm cartoon lake with reeds and water lilies, soft morning light"
BAMBOO = "cartoon bamboo forest with soft green light, peaceful"
AUSTRALIA = "sunny cartoon Australian bush with red earth, eucalyptus trees and a clear sky, bright warm light"
HOME = "cozy cartoon living room with a sofa, a rug and a window with sunshine, warm soft light"
# nr, en, ro, art, sunet (Pixabay), video real (Pexels/Pixabay), desen, unde stă Pip, fundal
A = [
(1, "cow", "vacă", "a", "cow moo", "cow / cow mooing", "A friendly black-and-white cartoon cow standing in the grass, side view facing right", "sitting on a wooden fence post on the left", FARM),
(2, "penguin", "pinguin", "a", "penguin call / penguin colony", "penguin / penguins walking", "A cute cartoon penguin standing on the ice with its flippers out, front view", "sitting on a little block of ice on the left, wearing a tiny teal scarf", ICE),
(3, "bear", "urs", "a", "bear growl / bear roar", "brown bear", "A big brown cartoon bear standing on all fours, side view facing right", "sitting on a tree stump on the left", FOREST),
(4, "dog", "câine", "a", "dog bark", "dog barking", "A happy golden cartoon dog sitting with its tongue out, side view facing right", "sitting on a sofa cushion on the left", HOME),
(5, "dolphin", "delfin", "a", "dolphin sounds / dolphin whistle", "dolphin / dolphins jumping", "A smiling blue-gray cartoon dolphin jumping out of the water with a little splash, side view facing right", "sitting on a rock at the shore on the left", SEA),
(6, "snake", "șarpe", "a", "snake hiss", "snake", "A long green cartoon snake coiled on the ground with its head up and tongue out, side view", "sitting on a tree stump on the left", FOREST),
(7, "pig", "porc", "a", "pig oink", "pig / pigs farm", "A pink cartoon pig standing in a little puddle of mud, side view facing right", "sitting on a wooden fence post on the left", FARM),
(8, "seal", "focă", "a", "seal bark / sea lion", "seal / sea lion", "A shiny gray cartoon seal lying on a rock by the sea with its head up, side view facing right", "sitting on a rock at the shore on the left", SEA),
(9, "seagull", "pescăruș", "a", "seagull", "seagull / seagulls", "A white-and-gray cartoon seagull standing on a wooden pier post, side view facing right", "sitting on a wooden pier post on the left", SEA),
(10, "whale", "balenă", "a", "whale song / humpback whale", "humpback whale / whale breaching", "A HUGE friendly blue cartoon humpback whale jumping out of the ocean with a big splash, side view facing right", "sitting on a rock at the shore on the left", SEA),
(11, "cat", "pisică", "a", "cat meow", "cat meowing", "A cute orange cartoon cat sitting on a rug, front view", "sitting on a sofa cushion on the left", HOME),
(12, "crocodile", "crocodil", "a", "crocodile growl / alligator", "crocodile / alligator", "A long green cartoon crocodile lying on the riverbank with its mouth a little open, side view facing right", "sitting on a rock on the left", RIVER),
(13, "swan", "lebădă", "a", "swan / swan hiss", "swan / swans", "An elegant white cartoon swan swimming on the lake, side view facing right", "sitting on a little rock in the reeds on the left", LAKE),
(14, "bull", "taur", "a", "bull snort / bull", "bull", "A big strong brown cartoon bull with short horns standing in the grass, side view facing right", "sitting on a wooden fence post on the left", FARM),
(15, "rooster", "cocoș", "a", "rooster crow", "rooster crowing", "A proud cartoon rooster with a red comb and colorful tail standing on a hay bale, side view facing right", "sitting on a wooden fence post on the left", FARM),
(16, "monkey", "maimuță", "a", "monkey sound / chimpanzee", "monkey / chimpanzee", "A cute brown cartoon monkey hanging from a jungle vine with one arm, mouth open shouting oo-oo-aa-aa, side view facing right", "sitting on a little rock on the left", "sunny cartoon jungle with big green leaves, vines and soft sunbeams, warm light"),
(17, "rhino", "rinocer", "a", "rhino / rhinoceros", "rhino / rhinoceros", "A big gray cartoon rhino with a big horn standing in the grass, side view facing right", "sitting on a rock on the left", SAVANNA),
(18, "squirrel", "veveriță", "a", "squirrel chatter", "squirrel", "A cute red-brown cartoon squirrel with a big fluffy tail sitting on a tree branch holding an acorn, side view facing right", "sitting on a tree stump on the left", FOREST),
(19, "crow", "cioară", "a", "crow caw", "crow / raven", "A shiny black cartoon crow standing on a tree branch with its beak open cawing, side view facing right", "sitting on a tree stump on the left", FOREST),
(20, "donkey", "măgar", "a", "donkey bray / donkey hee haw", "donkey / donkey braying", "A friendly gray cartoon donkey with long ears and its mouth open braying, standing in the grass, side view facing right", "sitting on a wooden fence post on the left", FARM),
]
def answer(a):
    art, en = a[3], a[1].upper()
    return f"They're {en}!" if art == "they" else f"It's {art} {en}!"

out = []; w = out.append
w("# Video 10 — „Who Said MOO MOO?” Animal Sounds Quiz (engleză)\n")
w("> Tema cea mai mare la canalul model (Little Dreamers: „Guess The Animal Sounds” = 5,7 milioane de vizionări).")
w("> **Formatul de la Video 9:** silueta din **imagine desenată** + **un singur sunet lung** + la dezvăluire **video REAL** cu animalul, într-un cartonaș, cu Pip în colț.")
w("> Animale: 5 din Video 1, 4 din Video 2, 11 noi.\n")
w("---\n\n## Cum arată o rundă\n")
w("1. Imaginea desenată, animalul = **siluetă neagră cu „?”**; se aude **sunetul o dată, lung (~5 s)**.")
w("2. **3-2-1**.")
w("3. Flash → **cartonașul cu video-ul real** crește din siluetă; Pip (poza ta decupată) în colț; numele mare dedesubt.")
w("4. Naratorul: „It's a COW!” → **sunetul real** pe video → Pip laudă.\n")
w("Rămân: hook-ul de 5 s, intro scurt + Subscribe, runda 10 = **BONUS** (balena), finalul cu Pip.")
w("Vocile pentru „Round 1…20”, numărătoare, întrebări și laude le refolosesc. **Voci noi: 22** (20 de răspunsuri + 2 ale lui Pip).\n")
w("---\n\n## Ce trebuie pentru fiecare rundă (3 lucruri)\n")
w("| Ce | De unde | Nume fișier |\n|---|---|---|")
w("| **Imagine desenată** (Pip + animalul) | promptul de mai jos | `01-cow.jpg` |")
w("| **Video real** cu animalul | **pexels.com/videos** sau **pixabay.com/videos** | `01-cow-real.mp4` |")
w("| **Sunetul** | **pixabay.com/sound-effects** (rezervă: freesound.org, CC0) | `01-cow.mp3` |\n")
w("**Video-ul real — cum alegi:** orizontal, Full HD; **animalul se vede clar și mare în cadru**; camera cât mai liniștită; măcar 8 s. Nu contează dacă e mut (cele mai multe de pe Pexels sunt) — sunetul îl pun eu din fișierul de sunet.\n")
w("**Sunetul — cum alegi:** doar animalul (fără muzică, fără voci de oameni), **4–6 s** în care animalul scoate sunetul de câteva ori.\n")
w("---\n\n## Lista\n")
w("| # | Animal | Română | Sunet (Pixabay) | Video real (Pexels) | Narator |\n|---|---|---|---|---|---|")
for a in A:
    w(f"| {a[0]} | {a[1]}{' ⭐ BONUS' if a[0] == 10 else ''} | {a[2]} | `{a[4]}` | `{a[5]}` | {answer(a)} |")
w("\n**Rezerve:** `goat`, `donkey`, `owl`, `elephant`, `lion`, `frog`.\n")
w("---\n\n## Vocile (22)\n")
w("**Narator** (WST – Narator), în ordinea rundelor:\n```")
for a in A: w(answer(a))
w("```\n**Pip** (WST – Pip):\n```\nWho said MOO MOO?\nYou did it! All twenty animals!\n```")
w("Setări ca până acum: **Multilingual v2**, Speed 0.9, Stability 45, Similarity 75, Style 30. Generează-le **în ordine** (1 → 20), ca să le potrivesc ușor.\n")
w("---\n\n## Imaginile desenate (20)\n")
w("Folosește `canal/pip-intreg.png` ca referință pentru Pip. **Animalul întreg, cu spațiu liber în jur, nu atinge marginile** — din el fac silueta. **Fără text.** Doar imagine, **fără clip**.\n")
for i, a in enumerate(A):
    nr, en, ro, art, snd, vid, desc, place, bg = a
    w(f"### {nr}. {en.upper()} ({ro}){' — BONUS' if nr == 10 else ''}\n```")
    be = "are" if art == "they" else "is"
    w(f"Wide horizontal 16:9 landscape composition. {desc}, the whole {en} clearly visible with empty space around it, not touching the frame edges, not overlapping anything, the {en} {be} the main subject in the center-right of the frame, little cartoon sound lines near it. {PIP}, {place}, {G[i % len(G)]}. Background: {bg}, medium-wide shot. {STYLE}. Landscape orientation, 16:9, 1920x1080. The owl wears its oversized teal headphones and no hat. No text, no letters, no words, no numbers in the image.")
    w("```\n")
w("---\n\n## Intro și final (imagine + clip de 5 s, ca până acum)\n")
w("### INTRO\n**Imagine:**\n```")
w(f"Wide horizontal 16:9 landscape composition. {PIP}, standing on a fluffy rug in a sunny cartoon meadow by the sea and waving one wing at the viewer, a cow, a penguin, a dolphin jumping in the water and a giraffe in the distance around, empty wall space on the upper right for a title, warm sunny light, medium shot. {STYLE}. Landscape orientation, 16:9, 1920x1080. No text, no letters, no words in the image.")
w("```\n**Clip:**\n```\n5-second video. Static camera. The owl bounces gently on the rug, waves one wing twice and looks at the camera, keeping its headphones on. Everything else stays in place. Smooth cartoon animation, no morphing, the owl stays in the frame the whole time, keep the style unchanged.\n```\n")
w("### FINAL\n**Imagine:**\n```")
w(f"Wide horizontal 16:9 landscape composition. {PIP}, BIG in the center, wearing a shiny gold medal, standing on a grassy hill, surrounded by happy cartoon animals: a cow, a penguin, a bear, a panda, a koala and a giraffe, colorful confetti in the air, sunny sky. {STYLE}. Landscape orientation, 16:9, 1920x1080. No text, no letters, no words in the image.")
w("```\n**Clip:**\n```\n5-second video. Static camera. The owl claps its wings happily, bounces and smiles at the camera, keeping its headphones and medal on, confetti falls slowly. The animals stay in place. Smooth cartoon animation, no morphing, the owl stays in the frame the whole time, keep the style unchanged.\n```\n")
w("---\n\n## Thumbnail\n\nStilul cu **14,7% CTR**: Pip mare, animalul colorat (silueta + „?” le fac eu).\n```")
w(f"YouTube thumbnail for a toddler sound quiz, wide 16:9, 2D cartoon children's illustration, bold and super colorful, high contrast, very simple composition readable at small size. LEFT (35% of the frame): {PIP}, BIG and close to the camera, beak wide open in excitement, one wing cupped to its ear, the other wing pointing at the cow. RIGHT (60%): ONE big friendly black-and-white cartoon cow with its mouth open saying moo and cartoon sound waves, side view facing left, fully visible, not touching the frame edges. BACKGROUND: sunny cartoon farm with a red barn, simple and lighter than the characters, simple and lighter than the characters. {STYLE}. No text, no letters, no numbers, no logos, no question marks. The owl and the cow do not touch.")
w("```\n\n---\n\n## Ordinea în care să le trimiți\n")
w("1. Sunetele (20) → 2. Vocile (22) → 3. Imaginile desenate (20) + intro + final → 4. Video-urile reale (20) → 5. Imaginea de thumbnail.")
w("Cu „nu fă nik” le salvez; când sunt toate, fac montajul.\n")
w("**Deja avem:** poza decupată a lui Pip (`canal/imagini/pip/pip-decupat.png`).")
open(os.path.join(HERE, "..", "canal", "video-10-animale.md"), "w").write("\n".join(out) + "\n")
print("gata")
