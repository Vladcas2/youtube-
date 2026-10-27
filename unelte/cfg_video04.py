"""Face montaj-cfg.json pentru Video 4 (fișierele din canal/video-04)."""
import json, os, sys
import librosa, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.abspath(os.path.join(HERE, "..", "canal", "video-04"))
M = f"{V4}/materiale"
VEH = ["school-bus", "big-truck", "bullet-train", "tram", "speedboat", "propeller-plane", "subway-train", "tow-truck",
       "fighter-jet", "monster-truck", "scooter", "horse-carriage", "jet-ski", "lawn-mower", "go-kart", "pirate-ship",
       "snowmobile", "roller-coaster", "street-sweeper", "fire-boat"]
# întrebările lui Pip (fără întrebare la rundele rapide 1-3); „tricky” la rundele grele
Q = {n: (5 if n in (16, 18, 20) else (n - 4) % 4 + 1) for n in range(4, 21)}
P = {n: (7 if n >= 19 else (n - 1) % 6 + 1) for n in range(1, 21)}

def fereastra(f, L):
    """Bucata de L secunde cu cea mai multă energie (RMS pe 50 ms)."""
    y, sr = librosa.load(f, sr=22050); d = len(y) / sr
    r = librosa.feature.rms(y=y, frame_length=1102, hop_length=1102)[0]
    n = int(L / 0.05)
    a = round(int(np.argmax(np.convolve(r ** 2, np.ones(n), "valid"))) * 0.05, 2) if len(r) > n else 0.0
    return [a, round(min(d, a + L), 2)]

rounds = []
for n, v in enumerate(VEH, 1):
    sfx = f"{V4}/sunete/16-pirate-ship.mp3" if v == "pirate-ship" else f"{M}/sunete/{n:02d}-{v}.mp3"
    r = {"nr": n, "label": f"{n:02d}-{v}", "clip": f"{M}/clipuri/{n:02d}-{v}.mp4", "sfx": sfx,
         "s1": fereastra(sfx, 2.2 if n <= 3 else 2.6), "s3": fereastra(sfx, 2.2),
         "voice": {"round": f"{M}/voci-noi/runde/N-{n:02d}-round.mp3", "answer": f"{M}/voci-noi/raspunsuri/N-{n:02d}-answer.mp3",
                   "praise": f"{M}/voci-noi/pip/P-lauda-{P[n]}.mp3"}}
    if n in Q: r["voice"]["question"] = f"{M}/voci-noi/pip/P-intrebare-{Q[n]}.mp3"
    if v == "tram": r["clip_len"] = 5.5  # după 5,5 s tramvaiul pleacă din cadru
    rounds.append(r)

cfg = {
    "tmp": sys.argv[1] if len(sys.argv) > 1 else "/tmp/build4",
    "out": f"{V4}/../who-said-honk-video-04-1080p.mp4",
    "intro": f"{M}/clipuri/00-intro.mp4",
    "intro_text": f"{V4}/imagini/suprapuneri/intro-who-said-honk.png",
    "music": f"{M}/muzica/Baby_Animals_Playing_-_Joel_Cummins.mp3",
    "runde_dir": f"{V4}/imagini", "animale_dir": f"{V4}/imagini/suprapuneri/animale",
    "fast_rounds": 3,
    "trailer": {"rounds": [10, 9, 16, 5], "slot": 1.25, "from": 0.8},
    "voice": {"trailer": f"{M}/voci-noi/pip/P-can-you-guess-them-all.mp3", "intro-1": f"{M}/voci-noi/pip/P-who-said-honk-honk.mp3",
              "intro-2": f"{M}/voci-noi/pip/P-put-on-your-ears.mp3", "countdown": f"{M}/voci-noi/N-00-countdown-321.mp3"},
    "countdown_words": [[0.05, 0.8], [0.88, 1.65], [1.84, 2.87]],
    "rounds": rounds,
    "final": {"clip": f"{M}/clipuri/99-final.mp4", "text": f"{V4}/../video-03/imagini/suprapuneri/final-you-did-it.png",
              "lines": [f"{M}/voci-noi/pip/P-you-did-it.mp3", f"{M}/voci-noi/pip/P-super-listener.mp3", f"{M}/voci-noi/pip/P-see-you-next-time.mp3"]},
}
for r in rounds:
    for f in [r["clip"], r["sfx"]] + list(r["voice"].values()):
        assert os.path.exists(f), f
json.dump(cfg, open(f"{V4}/montaj-cfg.json", "w"), indent=1)
print("gata", f"{V4}/montaj-cfg.json")
