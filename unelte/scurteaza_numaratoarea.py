"""Transformă numărătoarea 5-4-3-2-1 dintr-un video gata montat în 3-2-1: taie „5” și „4” (2 s) din fiecare rundă.

Folosire: scurteaza_numaratoarea.py intrare.mp4 iesire.mp4 c1,c2,...  (secundele unde apare „5” în fiecare rundă)
Vocea „five, four” cade odată cu imaginile, iar „three, two, one” rămâne pe cifrele lor.
"""
import subprocess, sys
FF = __import__("imageio_ffmpeg").get_ffmpeg_exe()
src, out, cs = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(",")]
o = subprocess.run([FF, "-i", src], capture_output=True, text=True).stderr
import re
h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", o).groups(); D = int(h) * 3600 + int(m) * 60 + float(s)
keep, t = [], 0.0
for c in cs:
    keep.append((t, c)); t = c + 2.0
keep.append((t, D))
fc = ""
for i, (a, b) in enumerate(keep):
    fc += f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={max(0, b - a - 0.02)}:d=0.02[a{i}];"
fc += "".join(f"[v{i}][a{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=1:a=1[v][a]"
subprocess.run([FF, "-loglevel", "error", "-y", "-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "22", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
print("gata", out, "durata nouă:", round(D - 2 * len(cs), 2))
