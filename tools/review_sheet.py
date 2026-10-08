"""Лист для просмотра раздела: все варианты idle объектов (со светом по карте нормалей, как примерно в игре).
Запуск: python3 tools/review_sheet.py renders/_review/<имя>.png <id> [<id> …]
Масштаб: крупное уменьшается, мелкое увеличивается, чтобы всё было видно на одном листе.
"""
import glob
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "render"))
import _preview as P  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

out, ids = sys.argv[1], sys.argv[2:]
f = ImageFont.truetype("DejaVuSans-Bold.ttf", 13)
f2 = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
rows = []
for oid in ids:
    fs = sorted(x for x in glob.glob(os.path.join(ROOT, f"renders/*/{oid}_*_idle.png")))
    lits = [(os.path.basename(x)[len(oid) + 1:-9], P.lit(x)[1]) for x in fs]
    if not lits:
        continue
    # один масштаб на строку (объект): варианты сравнимы по размеру между собой
    mh = max(i.height for _, i in lits)
    mw = max(i.width for _, i in lits)
    k = min(220 / mh, 300 / mw) if max(mh, mw) > 220 else min(3.0, 90 / max(mh, mw))
    ims = [(n, i.resize((max(1, int(i.width * k)), max(1, int(i.height * k))))) for n, i in lits]
    if ims:
        rows.append((oid, ims))
W = max(sum(max(i.width, 170) + 16 for _, i in r) + 20 for _, r in rows)
H = sum(max(i.height for _, i in r) + 62 for _, r in rows) + 20
sh = Image.new("RGBA", (W, H), (36, 37, 44, 255))
d = ImageDraw.Draw(sh)
y = 10
for oid, r in rows:
    d.text((10, y), oid, font=f2, fill=(240, 200, 140))
    hm = max(i.height for _, i in r)
    x = 10
    for n, i in r:
        d.text((x, y + 24), n[:24], font=f, fill=(200, 200, 200))
        sh.alpha_composite(i, (x, y + 44 + hm - i.height))
        x += max(i.width, 170) + 16
    y += hm + 62
sh.convert("RGB").save(os.path.join(ROOT, out))
print(out, sh.size)
