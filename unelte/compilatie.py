"""Compilație: lipește videoclipuri întregi (fără finalul celor din mijloc) într-unul lung.

Folosire: compilatie.py iesire.mp4 video1.mp4:taie_la video2.mp4:taie_la ... ultimul.mp4
(„taie_la” = secunda unde începe finalul „You did it!”; ultimul rămâne întreg)
Se poate da și o bucată: video.mp4:a-b (de la secunda a la b), ca să sari o replică.
"""
import subprocess, sys
FF = __import__("imageio_ffmpeg").get_ffmpeg_exe()
out, parts = sys.argv[1], sys.argv[2:]
ins, fc = [], ""
for i, p in enumerate(parts):
    f, _, t = p.partition(":")
    a, _, b = t.rpartition("-") if "-" in t else ("0", "", t)
    ins += ["-i", f]
    tv = f"trim={a}:{b}," if t else ""
    ta = f"atrim={a}:{b}," if t else ""
    fo = f"afade=t=out:st={float(b) - float(a) - 0.25}:d=0.25," if t else ""
    fc += f"[{i}:v]{tv}setpts=PTS-STARTPTS,scale=1920:1080,fps=30,format=yuv420p,setsar=1[v{i}];" \
          f"[{i}:a]{ta}asetpts=PTS-STARTPTS,afade=t=in:d=0.15,{fo}aformat=sample_rates=48000:channel_layouts=stereo[a{i}];"
fc += "".join(f"[v{i}][a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=1[v][a]"
subprocess.run([FF, "-loglevel", "error", "-y"] + ins + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "24", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
print("gata", out)
