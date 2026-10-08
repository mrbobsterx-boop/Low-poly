"""Предпросмотр для автора: рендер + «как примерно будет в игре» (свет по карте нормалей) + образец из ОС.
Запуск: python3 render/_preview.py <выход.png> renders/<кат>/<имя>.png [ещё…]
Свет — условный (тёплая лампа слева сверху + слабый общий), только для глаз; в игре свет делает Godot.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LIGHT = (-0.55, 0.6, 0.58)       # слева, сверху, к зрителю
AMBIENT = 0.38
COLW = 190                        # минимальная ширина колонки (чтобы подписи не наезжали)


def lit(color_path):
    col = Image.open(color_path).convert("RGBA")
    nrm = Image.open(color_path[:-4] + "_n.png").convert("RGB")
    lx, ly, lz = LIGHT
    ln = (lx * lx + ly * ly + lz * lz) ** 0.5
    lx, ly, lz = lx / ln, ly / ln, lz / ln
    out = Image.new("RGBA", col.size)
    cp, npx, op = col.load(), nrm.load(), out.load()
    for y in range(col.size[1]):
        for x in range(col.size[0]):
            r, g, b, a = cp[x, y]
            if a == 0:
                continue
            nr, ng, nb = npx[x, y]
            nx, ny, nz = nr / 127.5 - 1, ng / 127.5 - 1, nb / 127.5 - 1
            k = AMBIENT + (1 - AMBIENT) * max(0.0, nx * lx + ny * ly + nz * lz)
            op[x, y] = (min(255, int(r * k * 1.05)), min(255, int(g * k)), min(255, int(b * k * 0.92)), a)
    return col, out


def ref_for(color_path):
    name = os.path.basename(color_path)
    cat = os.path.basename(os.path.dirname(color_path))
    d = os.path.join(ROOT, "docs", "ref", cat)
    if not os.path.isdir(d):
        return None
    best = max((f for f in os.listdir(d) if name.startswith(f[:-4] + "_")), key=len, default=None)
    return Image.open(os.path.join(d, best)).convert("RGBA") if best else None


def main(out, paths):
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 15)
    except OSError:
        font = ImageFont.load_default()
    rows = []
    for p in paths:
        p = os.path.join(ROOT, p) if not os.path.isabs(p) else p
        col, l = lit(p)
        ref = ref_for(p)
        rows.append((os.path.basename(p)[:-4], [("чистый цвет (в игру)", col), ("со светом (примерно)", l)]
                     + ([("образец ОС", ref)] if ref else [])))
    PAD, TH = 16, 22
    W = max(sum(max(im.width, COLW) for _, im in r[1]) + PAD * (len(r[1]) + 1) for r in rows)
    H = sum(max(im.height for _, im in r[1]) + TH * 2 + PAD for r in rows) + PAD
    sheet = Image.new("RGBA", (W, H), (58, 58, 62, 255))
    d = ImageDraw.Draw(sheet)
    y = PAD
    for title, ims in rows:
        d.text((PAD, y), title, font=font, fill=(240, 240, 240))
        x, hmax = PAD, max(im.height for _, im in ims)
        for cap, im in ims:
            d.text((x, y + TH), cap, font=font, fill=(170, 170, 170))
            sheet.alpha_composite(im, (x, y + TH * 2 + hmax - im.height))
            x += max(im.width, COLW) + PAD
        y += hmax + TH * 2 + PAD
    sheet.convert("RGB").save(out)
    print("предпросмотр:", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
