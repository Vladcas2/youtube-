"""Video 7: „Learn Construction Vehicles” (fără ghicit). Refolosește clipurile și sunetele de la Video 5 și 6.

Fiecare utilaj: clipul + numele pe ecran → naratorul („This is a … ! It …!”) → sunetul real → următorul.
Intro: imaginea de thumbnail + Pip „Let's learn…” + butonul Subscribe; apoi recapitulare scurtă („Let's see them again!”);
final: parada de la Video 6 + „Which one is your favorite?” + „See you next time!”.
Folosire: monteaza_invatam.py <tmp>
"""
import subprocess, os, json, sys, re
FF = __import__("imageio_ffmpeg").get_ffmpeg_exe()
HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.abspath(os.path.join(HERE, "..", "canal"))
V7 = f"{C}/video-07"; M7 = f"{V7}/materiale"
TMP = sys.argv[1] if len(sys.argv) > 1 else "/tmp/build7"; os.makedirs(TMP, exist_ok=True)
V = "scale=1920:1080,fps=30,format=yuv420p,setsar=1"
ENC = ["-an", "-r", "30", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-video_track_timescale", "15360"]
def run(a): subprocess.run([FF, "-loglevel", "error", "-y"] + a, check=True)
def dur(f):
    o = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", o).groups(); return int(h) * 3600 + int(m) * 60 + float(s)

ORDER = ["excavator", "dump-truck", "cement-mixer", "bulldozer", "crane", "tower-crane", "wheel-loader", "road-roller", "forklift",
         "mining-truck", "wrecking-ball", "jackhammer", "rock-breaker", "pile-driver", "semi-truck", "recycling-truck", "snowplow",
         "plate-compactor", "concrete-saw", "wood-chipper", "chainsaw", "power-drill", "hammer", "giant-digger"]
src = {}
for v in ("video-05", "video-06"):  # pentru utilajele din ambele (nu e cazul acum), câștigă Video 6
    cfg = json.load(open(f"{C}/{v}/montaj-cfg.json"))
    for r in cfg["rounds"]:
        name = r["label"].split("-", 1)[1]
        src[name] = dict(r, animale=cfg["animale_dir"])
items = []
for i, n in enumerate(ORDER, 1):
    r = src[n]
    items.append({"n": n, "clip": r["clip"], "boomerang": r.get("boomerang"), "label": f"{r['animale']}/{r['label']}.png",
                  "sfx": r["sfx"], "snd": r["s3"], "voice": f"{M7}/voci-noi/raspunsuri/N-{i:02d}-{n}.mp3",
                  "answer": r["voice"]["answer"]})  # „It's a …!” de la Video 5/6, pentru recapitulare
P = f"{M7}/voci-noi/pip"; R4 = f"{C}/video-04/materiale/voci-noi/pip"

# ---------- segmente video ----------
segs, ev = [], []   # ev: (fișier, start, bucată, e_sunet)
T = 0.0
# intro: imaginea de thumbnail cu zoom lent + „LET'S LEARN!” + Subscribe
ILEN = round(0.3 + dur(f"{P}/P-lets-learn.mp3") + 0.6, 2)
run(["-loop", "1", "-framerate", "30", "-t", str(ILEN), "-i", f"{V7}/thumbnail/thumbnail-text.jpg",
     "-loop", "1", "-framerate", "30", "-t", str(ILEN), "-i", f"{C}/video-05/imagini/suprapuneri/subscribe.png",
     "-filter_complex", f"[0:v]scale=3840:2160,zoompan=z='1+0.0008*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30,format=yuv420p,setsar=1[b];"
     f"[1:v]format=rgba,scale=1920:1080,fade=t=in:st=0.3:d=0.25:alpha=1[s];[b][s]overlay=0:0:shortest=1,format=yuv420p",
     "-t", str(ILEN)] + ENC + [f"{TMP}/00.mp4"])
segs.append(f"{TMP}/00.mp4"); ev.append((f"{P}/P-lets-learn.mp3", 0.3, None, False)); T += ILEN

def item_seg(k, it, voice, slmax=2.6, pad=0.7, start=0.0, tag=""):
    """Un utilaj: clip + nume; vocea la 0,3 s, sunetul după voce; durata = cât e nevoie."""
    vd = dur(voice); s0, s1 = it["snd"]; sl = min(slmax, s1 - s0)
    L = round(0.3 + vd + 0.25 + sl + pad, 2)
    clip = it["clip"]
    if it["boomerang"]:
        clip = f"{TMP}/boom-{k:02d}.mp4"
        if not os.path.exists(clip):
            run(["-i", it["clip"], "-filter_complex", f"[0:v]trim=0:{it['boomerang']},setpts=PTS-STARTPTS,{V},split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0", "-an", clip])
    out = f"{TMP}/{tag}{k:02d}.mp4"
    run(["-stream_loop", "-1", "-i", clip, "-loop", "1", "-framerate", "30", "-t", str(L), "-i", it["label"],
         "-filter_complex", f"[0:v]trim={start}:{start + L},setpts=PTS-STARTPTS,{V},fade=t=in:st=0:d=0.25[c];[1:v]format=rgba,scale=1920:1080,fade=t=in:st=0.2:d=0.2:alpha=1[t];"
         f"[c][t]overlay=0:0:shortest=1,fade=t=out:st={L - 0.25}:d=0.25,format=yuv420p", "-t", str(L)] + ENC + [out])
    return out, L, vd, sl

for k, it in enumerate(items, 1):
    out, L, vd, sl = item_seg(k, it, it["voice"])
    segs.append(out)
    ev.append((it["voice"], T + 0.3, None, False))
    ev.append((it["sfx"], T + 0.3 + vd + 0.25, [it["snd"][0], it["snd"][0] + sl], True))
    it["T"] = T; T += L

# partea a 2-a: „MORE VEHICLES!” cu cele 20 de vehicule de la Video 4 („It's a …!” + sunetul)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = ImageFont.truetype(os.path.join(HERE, "fonturi", "fredoka-latin-700-normal.woff"), 150)
def card_img(text, out):
    card = Image.open(f"{V7}/thumbnail/thumbnail-curat.jpg").convert("RGBA").resize((1920, 1080))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((960, 108), text, font=F, fill=(0, 0, 0, 130), anchor="mm", stroke_width=16, stroke_fill=(0, 0, 0, 130))
    card.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(card).text((960, 100), text, font=F, fill=(255, 210, 63, 255), anchor="mm", stroke_width=16, stroke_fill=(59, 42, 32))
    card.convert("RGB").save(out)
def card_seg(text, voice, name):
    global T
    card_img(text, f"{TMP}/{name}.jpg")
    L = round(0.3 + dur(voice) + 0.6, 2)
    run(["-loop", "1", "-framerate", "30", "-t", str(L), "-i", f"{TMP}/{name}.jpg", "-vf", f"{V},fade=t=in:st=0:d=0.3,fade=t=out:st={L - 0.3}:d=0.3", "-t", str(L)] + ENC + [f"{TMP}/{name}.mp4"])
    segs.append(f"{TMP}/{name}.mp4"); ev.append((voice, T + 0.3, None, False)); start = T; T += L
    return start
c4 = json.load(open(f"{C}/video-04/montaj-cfg.json"))
more = [{"n": r["label"].split("-", 1)[1], "clip": r["clip"], "boomerang": r.get("clip_len") and r["clip_len"] - 0.1,
         "label": f"{c4['animale_dir']}/{r['label']}.png", "sfx": r["sfx"], "snd": r["s3"], "answer": r["voice"]["answer"]} for r in c4["rounds"]]
MORE = card_seg("MORE VEHICLES!", f"{R4}/P-lauda-2.mp3", "45")
for k, it in enumerate(more, 1):
    out, L, vd, sl = item_seg(100 + k, it, it["answer"], slmax=2.2, pad=0.5, tag="m")
    segs.append(out)
    ev.append((it["answer"], T + 0.3, None, False))
    ev.append((it["sfx"], T + 0.3 + vd + 0.25, [it["snd"][0], it["snd"][0] + sl], True))
    T += L

# recapitulare: „LET'S SEE THEM AGAIN!” → fiecare utilaj scurt: „It's a …!” + sunetul
RECAP = card_seg("LET'S SEE THEM AGAIN!", f"{P}/P-doing-great.mp3", "50")
for k, it in enumerate(items, 1):
    out, L, vd, sl = item_seg(k, it, it["answer"], slmax=1.8, pad=0.35, start=2.0, tag="r")
    segs.append(out)
    ev.append((it["answer"], T + 0.3, None, False))
    ev.append((it["sfx"], T + 0.3 + vd + 0.25, [it["snd"][0], it["snd"][0] + sl], True))
    T += L

# final: parada de la Video 6
fin = f"{C}/video-06/materiale/clipuri/99-final.mp4"
lines = [f"{P}/P-favorite.mp3", f"{R4}/P-see-you-next-time.mp3"]
FLEN = round(0.5 + sum(dur(f) + 0.5 for f in lines) + 1.5, 2)
run(["-i", fin, "-filter_complex", f"[0:v]trim=0:{min(FLEN, 7.9)},setpts=PTS-STARTPTS,{V},tpad=stop_mode=clone:stop_duration=6,trim=0:{FLEN},setpts=PTS-STARTPTS,fade=t=out:st={FLEN - 1.2}:d=1.2,format=yuv420p",
     "-t", str(FLEN)] + ENC + [f"{TMP}/99.mp4"])
segs.append(f"{TMP}/99.mp4")
t = T + 0.5
for f in lines:
    ev.append((f, t, None, False)); t += dur(f) + 0.5
total = T + FLEN
open(f"{TMP}/list.txt", "w").write("".join(f"file '{s}'\n" for s in segs))
ins_v = sum((["-i", f] for f in segs), [])  # filtrul concat decodează fiecare bucată separat (demuxerul concat dădea cadre negre)
run(ins_v + ["-filter_complex", "".join(f"[{i}:v]fps=30,format=yuv420p,setsar=1[v{i}];" for i in range(len(segs))) + "".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0[v]",
             "-map", "[v]"] + ENC + [f"{TMP}/video.mp4"])

# ---------- audio ----------
def level(f, tr):
    af = (f"atrim={tr[0]}:{tr[1]}," if tr else "") + "volumedetect"
    o = subprocess.run([FF, "-i", f, "-af", af, "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", o).group(1)), float(re.search(r"max_volume: (-?[\d.]+)", o).group(1))
ins, fc, lab = [], "", []
for i, (f, st, tr, sfx) in enumerate(ev):
    mean, peak = level(f, tr); g = (-3 - peak) if sfx else (-16 - mean)
    tt = f"atrim={tr[0]}:{tr[1]},asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st={max(0, tr[1] - tr[0] - 0.3):.2f}:d=0.3," if tr else ""
    ins += ["-i", f]; ms = int(st * 1000)
    fc += f"[{i}:a]{tt}aformat=sample_rates=48000:channel_layouts=stereo,volume={g:.1f}dB,adelay={ms}|{ms}[e{i}];"; lab.append(f"[e{i}]")
# muzica: încet sub voce, aproape oprită cât se aude utilajul
dips = "+".join(f"clip((t-{st - 0.2})/0.2,0,1)*clip(({st + tr[1] - tr[0] + 0.2}-t)/0.2,0,1)" for f, st, tr, sfx in ev if sfx)
env = f"min(t/1,1)*(0.09-0.07*min(1,{dips}))*clip(({total}-t)/2,0,1)"
mi = len(ev)
ins += ["-stream_loop", "-1", "-i", f"{C}/video-04/materiale/muzica/Baby_Animals_Playing_-_Joel_Cummins.mp3"]
fc += f"[{mi}:a]atrim=0:{total},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume='{env}':eval=frame[mu];"
fc += "".join(lab) + f"[mu]amix=inputs={len(lab) + 1}:normalize=0:duration=longest,atrim=0:{total},volume=-3dB,alimiter=limit=0.89[a]"
run(ins + ["-filter_complex", fc, "-map", "[a]", "-c:a", "aac", "-b:a", "160k", f"{TMP}/audio.m4a"])
out = f"{C}/learn-construction-video-07-1080p.mp4"
run(["-i", f"{TMP}/video.mp4", "-i", f"{TMP}/audio.m4a", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "24", "-preset", "medium",
     "-c:a", "copy", "-shortest", "-movflags", "+faststart", out])
def mmss(s): return f"{int(s // 60)}:{int(s % 60):02d}"
print("capitole:\n" + "".join(f"{mmss(it['T'] if k > 1 else 0)} {it['n'].replace('-', ' ').title()}\n" for k, it in enumerate(items, 1)) + f"{mmss(MORE)} More vehicles!\n{mmss(RECAP)} Let's see them again!\n{mmss(T)} Bye bye!")
print("gata:", out, "durata:", round(total, 2))
