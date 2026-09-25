# Test: intro + runda 1 (primele 30 de secunde)

Scopul: treci o singură dată prin tot procesul, de la imagini până la montaj.
Ce nu merge aici repari o dată, nu de 20 de ori.

---

## 1. Imaginile (3 bucăți)

La fiecare încarci `pip-avatar.jpg` ca referință de personaj.

**A. Intro: Pip la fermă**
```
Pip, a small round coral-orange baby owl with a cream face, big mint-green eyes,
a tiny orange beak and oversized teal headphones, popping up from behind a wooden
farm fence and waving one wing, red barn and rolling mint-green hills behind,
sunny yellow sky, bright morning light, medium shot, 2D cartoon children's
illustration, soft cel shading, subtle feather and fur texture, clean dark-brown
outlines, bright warm palette of sunny yellow, coral, mint green, teal and cream,
rounded cute shapes, 16:9
```

**B. Vaca: dezvăluirea** (o generezi ÎNAINTE de siluetă)
```
Happy cartoon cow standing in a simple farmyard, full body, side view facing
right, mouth open saying moo, small musical notes floating around its head,
Pip, a small round coral-orange baby owl with a cream face, big mint-green eyes,
a tiny orange beak and oversized teal headphones, sitting on a wooden fence in
the left corner cheering with both wings up, red barn behind, bright warm light,
medium shot, 2D cartoon children's illustration, soft cel shading, subtle feather
and fur texture, clean dark-brown outlines, bright warm palette of sunny yellow,
coral, mint green, teal and cream, rounded cute shapes, 16:9
```

**C. Silueta: NU o genera, o faci din B** (așa are exact aceeași formă):
1. Canva → deschide imaginea B → selectează vaca → „Editează” → **Eliminare fundal** pe o copie
   (fără Canva Pro: remove.bg, gratuit).
2. Pe vaca decupată: Ajustare → Luminozitate **−100**, Contrast **+100** → devine neagră.
3. Pune silueta pe imaginea B **peste vaca colorată**, adaugă un „?” alb mare deasupra.
4. Salvează ca imagine separată: `r01-silueta.png`. Imaginea B rămâne `r01-reveal.png`.

Truc: în montaj, trecerea silueta → reveal devine o simplă decolorare (fade) de 0,5 s,
iar vaca „se colorează” pe loc. Efect de dezvăluire perfect, fără animație.

---

## 2. Sunete (gratuite, fără Content ID)
- Pixabay Sounds → caută „cow moo” → descarcă 1 muget clar, de 2–3 secunde
- tic-tac pentru numărătoare, „pop” pentru apariția lui Pip, confetti / „yay” de copii
- muzică de fundal veselă: YouTube Studio → Biblioteca audio (filtru: „Nu necesită atribuire”)

---

## 3. Vocea (ElevenLabs sau vocea ta)

Generează fiecare replică separat. Așa le poți muta ușor pe timeline.
```
01  Who said MOO?
02  Put on your ears… can you name all twenty?
03  Round one!
04  Who's making that noise?
05  Five… four… three… two… one…
06  It's a COW! Moo!
07  Great job!
08  Round two!
```
Setări de pornire ElevenLabs: Stability ~45, Similarity ~75, Style ~30. Alege o voce caldă și
păstreaz-o pe aceeași pentru tot canalul.

---

## 4. Montaj (CapCut desktop, proiect 16:9, 4K / 30 fps)

| Timp | Imagine | Voce | Sunet | Text pe ecran |
|---|---|---|---|---|
| 0:00–0:03 | A, zoom lent | 01 → 02 | „pop” la 0:00 | „Who Said Moo?” sus, 0:00–0:01 |
| 0:03–0:05 | silueta | 03 | — | „Round 1” mare, centrat |
| 0:05–0:11 | silueta | — | **muget ×2**, muzica oprită | — |
| 0:11–0:13 | silueta | 04 | — | — |
| 0:13–0:18 | silueta | 05 | tic-tac | cifre 5-4-3-2-1 mari, în colț |
| 0:18–0:25 | fade → reveal | 06 | muget încă o dată | „COW” mare, jos |
| 0:25–0:28 | reveal, zoom ușor | 07 | confetti / yay | — |
| 0:28–0:30 | — | 08 | — | „Round 2” |

Text: font **Fredoka Bold**, alb cu contur maro #3B2A20. Același stil ca pe banner.
Muzica de fundal: la −25 dB, cu **volumul la 0** cât se aude mugetul.

---

## 5. Export și verificare
Exportă cele 30 de secunde și uită-te la ele **pe telefon, cu volumul la jumătate**:
- [ ] Mugetul se aude clar, fără muzică peste el?
- [ ] Textul „Round 1” și „COW” se citește pe ecranul mic?
- [ ] Pip arată la fel în A și în B?
- [ ] Trecerea silueta → vacă colorată arată ca o dezvăluire?
- [ ] Numărătoarea lasă timp să strigi răspunsul?

Trimite-mi o captură din fiecare imagine (A, silueta, B) sau clipul, și îl verificăm.
