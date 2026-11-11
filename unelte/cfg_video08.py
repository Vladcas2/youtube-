"""Face montaj-cfg.json pentru Video 8 (fișierele din canal/video-08; vocile comune din video-04)."""
import json, os, sys
import librosa, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.abspath(os.path.join(HERE, "..", "canal", "video-08"))
M = f"{V6}/materiale"
VEH = ["doorbell", "telephone", "alarm-clock", "vacuum-cleaner", "kettle", "toilet", "toaster", "microwave", "hair-dryer", "cuckoo-clock",
       "blender", "washing-machine", "frying-pan", "popcorn", "faucet", "toothbrush", "rubber-duck", "keys", "zipper", "scissors"]
R4 = os.path.abspath(os.path.join(HERE, "..", "canal", "video-04", "materiale", "voci-noi"))  # vocile refolosite de la Video 4
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
    sfx = f"{M}/sunete/{n:02d}-{v}.mp3"
    r = {"nr": n, "label": f"{n:02d}-{v}", "clip": f"{M}/clipuri/{n:02d}-{v}.mp4", "sfx": sfx,
         "s1": fereastra(sfx, 2.2 if n <= 3 else 2.6), "s3": fereastra(sfx, 2.2),
         "voice": {"round": f"{R4}/runde/N-{n:02d}-round.mp3", "answer": f"{M}/voci-noi/raspunsuri/N-{n:02d}-answer.mp3",
                   "praise": f"{R4}/pip/P-lauda-{P[n]}.mp3"}}
    if n in Q: r["voice"]["question"] = f"{R4}/pip/P-intrebare-{Q[n]}.mp3"
    # la final Pip își pierde căștile (sonerie, aspirator de la ~6,5 s; telefon, ceas de la ~7 s)
    B = {"doorbell": 6.0, "vacuum-cleaner": 6.0, "telephone": 6.5, "alarm-clock": 6.5}
    if v in B: r["boomerang"] = B[v]
    rounds.append(r)

cfg = {
    "tmp": sys.argv[1] if len(sys.argv) > 1 else "/tmp/build4",
    "out": f"{V6}/../who-said-ding-dong-video-08-1080p.mp4",
    "intro": f"{M}/clipuri/00-intro.mp4",
    "intro_text": f"{V6}/imagini/suprapuneri/intro-who-said-ding-dong.png",
    "music": f"{R4}/../muzica/Baby_Animals_Playing_-_Joel_Cummins.mp3",
    "runde_dir": f"{V6}/imagini", "animale_dir": f"{V6}/imagini/suprapuneri/animale",
    "fast_rounds": 3,
    "trailer": {"rounds": [10, 3, 7, 1], "slot": 1.25, "from": 0.8},
    "voice": {"trailer": f"{R4}/pip/P-can-you-guess-them-all.mp3", "intro-1": f"{M}/voci-noi/pip/P-who-said-ding-dong.mp3",
              "countdown": f"{R4}/N-00-countdown-321.mp3"},
    "subscribe": {"img": f"{V6}/imagini/suprapuneri/subscribe.png", "start": 0.2, "end": 2.0},
    "countdown_words": [[0.05, 0.8], [0.88, 1.65], [1.84, 2.87]],
    "rounds": rounds,
    "final": {"clip": f"{M}/clipuri/99-final.mp4", "text": f"{V6}/imagini/suprapuneri/final-you-did-it.png",
              "lines": [f"{M}/voci-noi/pip/P-you-did-it-sounds.mp3", f"{R4}/pip/P-super-listener.mp3", f"{R4}/pip/P-see-you-next-time.mp3"]},
}
for r in rounds:
    for f in [r["clip"], r["sfx"]] + list(r["voice"].values()):
        assert os.path.exists(f), f
json.dump(cfg, open(f"{V6}/montaj-cfg.json", "w"), indent=1)
print("gata", f"{V6}/montaj-cfg.json")
