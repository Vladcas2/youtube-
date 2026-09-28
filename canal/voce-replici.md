# Vocea: cine spune ce

Două voci:
- **N = Naratorul**: adult cald, clar. Anunță runda, numără și spune răspunsul.
- **P = Pip**: vocea personajului. Salută, pune întrebarea, laudă copilul.
- Plus efect sonor „kids cheering / yay” (Pixabay) după fiecare laudă.

Numărătoarea **o generezi o singură dată** (`N-00-countdown`) și o folosești în toate cele 20 de runde.

---

## Cum creezi vocile (ElevenLabs → Voices → Voice Design)

**Naratorul:**
```
Warm, friendly adult female preschool teacher, American English, clear and
slow pronunciation, cheerful and gentle, smiling tone, calm energy, perfect
for toddler learning videos
```
(sau masculin: „warm, friendly adult male storyteller…”)

**Pip:**
```
Cute cartoon owl character, playful and bubbly, slightly high-pitched but
clearly an animated character, very clear pronunciation, excited and
friendly, American English
```

Setări de pornire pentru amândouă: **Stability 45 · Similarity 75 · Style 30 · Speed 0.9**
(copiii de 2–4 ani au nevoie de vorbire mai lentă).
Salvează ambele voci și folosește-le pe **aceleași** în toate videoclipurile.

**Sfat pentru numărătoare:** scrie-o cu puncte de suspensie, cum e mai jos. Dacă iese prea repede,
generează fiecare cifră separat și pune-le pe timeline la câte 1 secundă.

---

## Pe runde (ordinea din videoclip)

| Timp | Cine | Fișier | Text |
|---|---|---|---|
| 0:00 | Pip | P-00-intro-1 | Who said MOO? |
| 0:01 | Pip | P-00-intro-2 | Put on your ears… can you name all twenty? |

| 0:03 | N | N-01-round | Round one! |
| 0:11 | **Pip** | P-01-question | Who's making that noise? |
| 0:13 | N | N-00-countdown | *(aceeași numărătoare)* |
| 0:18 | N | N-01-answer | It's a COW! Moo! |
| 0:25 | **Pip** | P-01-praise | Great job! + „yay” |
| 0:25 | N | N-02-round | Round two! |
| 0:33 | **Pip** | P-02-question | Who could that be? |
| 0:35 | N | N-00-countdown | *(aceeași numărătoare)* |
| 0:40 | N | N-02-answer | It's a DOG! Woof woof! |
| 0:47 | **Pip** | P-02-praise | You got it! + „yay” |
| 0:50 | N | N-03-round | Round three! |
| 0:58 | **Pip** | P-03-question | Hmm… who says that? |
| 1:00 | N | N-00-countdown | *(aceeași numărătoare)* |
| 1:05 | N | N-03-answer | It's a CAT! Meow! |
| 1:12 | **Pip** | P-03-praise | Awesome listening! + „yay” |
| 1:15 | N | N-04-round | Round four! |
| 1:23 | **Pip** | P-04-question | Do you know this one? |
| 1:25 | N | N-00-countdown | *(aceeași numărătoare)* |
| 1:30 | N | N-04-answer | It's a DUCK! Quack quack! |
| 1:37 | **Pip** | P-04-praise | High five! + „yay” |
| 1:40 | N | N-05-round | Round five! |
| 1:48 | **Pip** | P-05-question | Who's waking up the farm? |
| 1:50 | N | N-00-countdown | *(aceeași numărătoare)* |
| 1:55 | N | N-05-answer | It's a ROOSTER! Cock-a-doodle-doo! |
| 2:02 | **Pip** | P-05-praise | Super ears! + „yay” |
| 2:05 | N | N-06-round | Round six! Now it gets a little trickier! |
| 2:13 | **Pip** | P-06-question | Who's making that noise? |
| 2:15 | N | N-00-countdown | *(aceeași numărătoare)* |
| 2:20 | N | N-06-answer | It's a SHEEP! Baa! |
| 2:27 | **Pip** | P-06-praise | Well done! + „yay” |
| 2:30 | N | N-07-round | Round seven! |
| 2:38 | **Pip** | P-07-question | Who could that be? |
| 2:40 | N | N-00-countdown | *(aceeași numărătoare)* |
| 2:45 | N | N-07-answer | It's a PIG! Oink oink! |
| 2:52 | **Pip** | P-07-praise | Yes! You're so smart! + „yay” |
| 2:55 | N | N-08-round | Round eight! |
| 3:03 | **Pip** | P-08-question | Listen again… who is it? |
| 3:05 | N | N-00-countdown | *(aceeași numărătoare)* |
| 3:10 | N | N-08-answer | It's a HORSE! Neigh! |
| 3:17 | **Pip** | P-08-praise | Great job! + „yay” |
| 3:20 | N | N-09-round | Round nine! |
| 3:28 | **Pip** | P-09-question | Hmm… who says that? |
| 3:30 | N | N-00-countdown | *(aceeași numărătoare)* |
| 3:35 | N | N-09-answer | It's a GOAT! Maaa! |
| 3:42 | **Pip** | P-09-praise | You got it! + „yay” |
| 3:45 | N | N-10-round | Round ten! |
| 3:53 | **Pip** | P-10-question | Do you know this one? |
| 3:55 | N | N-00-countdown | *(aceeași numărătoare)* |
| 4:00 | N | N-10-answer | It's a CHICKEN! Cluck cluck! |
| 4:07 | **Pip** | P-10-praise | Awesome listening! + „yay” |
| 4:10 | N | N-11-round | Round eleven! Halfway there! Ten more to go! |
| 4:18 | **Pip** | P-11-question | Who's making that funny noise? |
| 4:20 | N | N-00-countdown | *(aceeași numărătoare)* |
| 4:25 | N | N-11-answer | It's a TURKEY! Gobble gobble! |
| 4:32 | **Pip** | P-11-praise | High five! + „yay” |
| 4:35 | N | N-12-round | Round twelve! |
| 4:43 | **Pip** | P-12-question | Who could that be? |
| 4:45 | N | N-00-countdown | *(aceeași numărătoare)* |
| 4:50 | N | N-12-answer | It's a DONKEY! Hee-haw! |
| 4:57 | **Pip** | P-12-praise | Super ears! + „yay” |
| 5:00 | N | N-13-round | Round thirteen! |
| 5:08 | **Pip** | P-13-question | Listen again… who is it? |
| 5:10 | N | N-00-countdown | *(aceeași numărătoare)* |
| 5:15 | N | N-13-answer | It's a GOOSE! Honk honk! |
| 5:22 | **Pip** | P-13-praise | Well done! + „yay” |
| 5:30 | N | N-14-round | Round fourteen! |
| 5:38 | **Pip** | P-14-question | Who's hiding by the pond? |
| 5:40 | N | N-00-countdown | *(aceeași numărătoare)* |
| 5:45 | N | N-14-answer | It's a FROG! Ribbit! |
| 5:52 | **Pip** | P-14-praise | Yes! You're so smart! + „yay” |
| 5:55 | N | N-15-round | Round fifteen! |
| 6:03 | **Pip** | P-15-question | Hmm… who's buzzing around? |
| 6:05 | N | N-00-countdown | *(aceeași numărătoare)* |
| 6:10 | N | N-15-answer | It's a BEE! Bzzzz! |
| 6:17 | **Pip** | P-15-praise | Great job! + „yay” |
| 6:19 | N | N-16-round | Round sixteen! Last five! These are the hardest ones! |
| 6:27 | **Pip** | P-16-question | Who's awake at night? |
| 6:29 | N | N-00-countdown | *(aceeași numărătoare)* |
| 6:34 | N | N-16-answer | It's an OWL! Hoo-hoo! |
| 6:41 | **Pip** | P-16-praise | You got it! + „yay” |
| 6:44 | N | N-17-round | Round seventeen! |
| 6:52 | **Pip** | P-17-question | Shh… who's that tiny sound? |
| 6:54 | N | N-00-countdown | *(aceeași numărătoare)* |
| 6:59 | N | N-17-answer | It's a MOUSE! Squeak squeak! |
| 7:06 | **Pip** | P-17-praise | Awesome listening! + „yay” |
| 7:08 | N | N-18-round | Round eighteen! |
| 7:16 | **Pip** | P-18-question | Who's sitting on the roof? |
| 7:18 | N | N-00-countdown | *(aceeași numărătoare)* |
| 7:23 | N | N-18-answer | It's a PIGEON! Coo-coo! |
| 7:30 | **Pip** | P-18-praise | High five! + „yay” |
| 7:33 | N | N-19-round | Round nineteen! |
| 7:41 | **Pip** | P-19-question | Who's singing in the grass? |
| 7:43 | N | N-00-countdown | *(aceeași numărătoare)* |
| 7:48 | N | N-19-answer | It's a CRICKET! Chirp chirp! |
| 7:55 | **Pip** | P-19-praise | Super ears! + „yay” |
| 7:58 | N | N-20-round | Round twenty! Final round! |
| 8:06 | **Pip** | P-20-question | This is the hardest one… who is it? |
| 8:08 | N | N-00-countdown | *(aceeași numărătoare)* |
| 8:13 | N | N-20-answer | It's a PEACOCK! Ay-AW! |
| 8:20 | **Pip** | P-20-praise | WOW! You're a super listener! + „yay” |
| 8:28 | Pip | P-99-final-1 | You did it! All twenty animals! |
| 8:32 | Pip | P-99-final-2 | You are a SUPER listener! |
| 8:35 | Pip | P-99-final-3 | Want more? Let's go to the ocean next! See you there! |

---

## Liste de copiat în ElevenLabs (câte o replică pe rând = un fișier)

### Naratorul: 41 replici

```
N-00-countdown  Five… four… three… two… one…
N-01-round  Round one!
N-01-answer  It's a COW! Moo!
N-02-round  Round two!
N-02-answer  It's a DOG! Woof woof!
N-03-round  Round three!
N-03-answer  It's a CAT! Meow!
N-04-round  Round four!
N-04-answer  It's a DUCK! Quack quack!
N-05-round  Round five!
N-05-answer  It's a ROOSTER! Cock-a-doodle-doo!
N-06-round  Round six! Now it gets a little trickier!
N-06-answer  It's a SHEEP! Baa!
N-07-round  Round seven!
N-07-answer  It's a PIG! Oink oink!
N-08-round  Round eight!
N-08-answer  It's a HORSE! Neigh!
N-09-round  Round nine!
N-09-answer  It's a GOAT! Maaa!
N-10-round  Round ten!
N-10-answer  It's a CHICKEN! Cluck cluck!
N-11-round  Round eleven! Halfway there! Ten more to go!
N-11-answer  It's a TURKEY! Gobble gobble!
N-12-round  Round twelve!
N-12-answer  It's a DONKEY! Hee-haw!
N-13-round  Round thirteen!
N-13-answer  It's a GOOSE! Honk honk!
N-14-round  Round fourteen!
N-14-answer  It's a FROG! Ribbit!
N-15-round  Round fifteen!
N-15-answer  It's a BEE! Bzzzz!
N-16-round  Round sixteen! Last five! These are the hardest ones!
N-16-answer  It's an OWL! Hoo-hoo!
N-17-round  Round seventeen!
N-17-answer  It's a MOUSE! Squeak squeak!
N-18-round  Round eighteen!
N-18-answer  It's a PIGEON! Coo-coo!
N-19-round  Round nineteen!
N-19-answer  It's a CRICKET! Chirp chirp!
N-20-round  Round twenty! Final round!
N-20-answer  It's a PEACOCK! Ay-AW!
```

### Pip: 45 replici

```
P-00-intro-1  Who said MOO?
P-00-intro-2  Put on your ears… can you name all twenty?
P-01-question  Who's making that noise?
P-01-praise  Great job!
P-02-question  Who could that be?
P-02-praise  You got it!
P-03-question  Hmm… who says that?
P-03-praise  Awesome listening!
P-04-question  Do you know this one?
P-04-praise  High five!
P-05-question  Who's waking up the farm?
P-05-praise  Super ears!
P-06-question  Who's making that noise?
P-06-praise  Well done!
P-07-question  Who could that be?
P-07-praise  Yes! You're so smart!
P-08-question  Listen again… who is it?
P-08-praise  Great job!
P-09-question  Hmm… who says that?
P-09-praise  You got it!
P-10-question  Do you know this one?
P-10-praise  Awesome listening!
P-11-question  Who's making that funny noise?
P-11-praise  High five!
P-12-question  Who could that be?
P-12-praise  Super ears!
P-13-question  Listen again… who is it?
P-13-praise  Well done!
P-14-question  Who's hiding by the pond?
P-14-praise  Yes! You're so smart!
P-15-question  Hmm… who's buzzing around?
P-15-praise  Great job!
P-16-question  Who's awake at night?
P-16-praise  You got it!
P-17-question  Shh… who's that tiny sound?
P-17-praise  Awesome listening!
P-18-question  Who's sitting on the roof?
P-18-praise  High five!
P-19-question  Who's singing in the grass?
P-19-praise  Super ears!
P-20-question  This is the hardest one… who is it?
P-20-praise  WOW! You're a super listener!
P-99-final-1  You did it! All twenty animals!
P-99-final-2  You are a SUPER listener!
P-99-final-3  Want more? Let's go to the ocean next! See you there!
```

Denumește fiecare fișier descărcat cu codul din stânga (ex. `N-01-round.mp3`), ca să le găsești ușor în CapCut.
