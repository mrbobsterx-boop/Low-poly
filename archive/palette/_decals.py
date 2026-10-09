"""Атлас декалей palette/decals.png: таблички, трафареты, наклейки, полосы опасности (docs/QUALITY.md).
Запуск: python3 palette/_decals.py. В модели: L.decal("caution", (x, y, z), ширина).
Текст — английский (мир западный), крупный и контрастный. Без света и теней — только краска.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SIZE = (1024, 1024)
# имя: (x, y, ширина, высота) в px атласа
DECALS = {
    "caution": (0, 0, 256, 128),
    "danger": (256, 0, 256, 128),
    "hazard": (512, 0, 256, 64),
    "hazard_v": (512, 64, 256, 64),
    "skull_poster": (768, 0, 128, 176),
    "num_07": (0, 128, 128, 128),
    "num_12": (128, 128, 128, 128),
    "b2": (256, 128, 128, 128),
    "volt": (384, 128, 128, 128),
    "cross": (512, 128, 128, 128),
    "note": (640, 128, 128, 160),
    "star": (896, 0, 128, 128),
    "tape_red": (0, 256, 256, 48),
    "tape_grey": (0, 304, 256, 48),
    "stencil_box": (256, 256, 256, 128),
    "label_white": (768, 256, 192, 96),
}

YELLOW, BLACK, RED, WHITE, PAPER = (214, 162, 39), (30, 28, 26), (168, 50, 40), (226, 220, 206), (214, 204, 180)


def _font(sz):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", sz)
    except OSError:
        return ImageFont.load_default()


def _center_text(d, box, text, sz, fill):
    f = _font(sz)
    x0, y0, x1, y1 = box
    l, t, r, b = d.textbbox((0, 0), text, font=f)
    d.text(((x0 + x1 - (r - l)) / 2 - l, (y0 + y1 - (b - t)) / 2 - t), text, font=f, fill=fill)


def build():
    im = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def R(n):
        x, y, w, h = DECALS[n]
        return x, y, x + w - 1, y + h - 1

    # табличка CAUTION: чёрная рамка, жёлтое поле
    x0, y0, x1, y1 = R("caution")
    d.rectangle((x0 + 4, y0 + 8, x1 - 4, y1 - 8), fill=BLACK)
    d.rectangle((x0 + 12, y0 + 16, x1 - 12, y1 - 16), fill=YELLOW)
    _center_text(d, (x0, y0, x1, y1), "CAUTION", 44, BLACK)
    # DANGER: красная плашка сверху, белое поле
    x0, y0, x1, y1 = R("danger")
    d.rectangle((x0 + 4, y0 + 8, x1 - 4, y1 - 8), fill=WHITE)
    d.rectangle((x0 + 4, y0 + 8, x1 - 4, y0 + 70), fill=RED)
    _center_text(d, (x0, y0 + 8, x1, y0 + 70), "DANGER", 40, WHITE)
    _center_text(d, (x0, y0 + 72, x1, y1 - 8), "KEEP OUT", 26, BLACK)
    # полосы опасности (горизонтальная лента и для вертикали)
    for n in ("hazard", "hazard_v"):
        x, y, w, h = DECALS[n]
        t = Image.new("RGBA", (w, h), YELLOW)
        td = ImageDraw.Draw(t)
        for k in range(-3, w // 32 + 3):
            xs = k * 32
            td.polygon([(xs, h), (xs + 16, h), (xs + 16 + h, 0), (xs + h, 0)], fill=BLACK)
        im.paste(t, (x, y))
    # плакат с черепом
    x0, y0, x1, y1 = R("skull_poster")
    d.rectangle((x0 + 4, y0 + 4, x1 - 4, y1 - 4), fill=PAPER)
    cx = (x0 + x1) // 2
    d.ellipse((cx - 30, y0 + 24, cx + 30, y0 + 80), fill=BLACK)
    d.rectangle((cx - 18, y0 + 70, cx + 18, y0 + 92), fill=BLACK)
    d.ellipse((cx - 20, y0 + 42, cx - 6, y0 + 58), fill=PAPER)
    d.ellipse((cx + 6, y0 + 42, cx + 20, y0 + 58), fill=PAPER)
    for k in (-10, 0, 10):
        d.line((cx + k, y0 + 82, cx + k, y0 + 92), fill=PAPER, width=3)
    d.line((cx - 40, y0 + 96, cx + 40, y0 + 112), fill=BLACK, width=8)
    d.line((cx - 40, y0 + 112, cx + 40, y0 + 96), fill=BLACK, width=8)
    for k, w in enumerate((70, 90, 60)):
        d.rectangle((cx - w // 2, y0 + 126 + k * 14, cx + w // 2, y0 + 132 + k * 14), fill=RED)
    # трафаретные номера (белая краска)
    for n, t in (("num_07", "07"), ("num_12", "12"), ("b2", "B-2")):
        _center_text(d, R(n), t, 72 if len(t) == 2 else 56, WHITE)
    # знак «ток»: жёлтый треугольник, чёрная молния
    x0, y0, x1, y1 = R("volt")
    d.polygon([((x0 + x1) / 2, y0 + 8), (x1 - 6, y1 - 12), (x0 + 6, y1 - 12)], fill=BLACK)
    d.polygon([((x0 + x1) / 2, y0 + 22), (x1 - 20, y1 - 20), (x0 + 20, y1 - 20)], fill=YELLOW)
    cx = (x0 + x1) / 2
    d.polygon([(cx + 6, y0 + 44), (cx - 14, y0 + 84), (cx, y0 + 84), (cx - 8, y1 - 26), (cx + 16, y0 + 74),
               (cx + 2, y0 + 74)], fill=BLACK)
    # красный крест на белом круге
    x0, y0, x1, y1 = R("cross")
    d.ellipse((x0 + 6, y0 + 6, x1 - 6, y1 - 6), fill=WHITE)
    d.rectangle((x0 + 50, y0 + 24, x1 - 50, y1 - 24), fill=RED)
    d.rectangle((x0 + 24, y0 + 50, x1 - 24, y1 - 50), fill=RED)
    # записка (бумага с «строчками»)
    x0, y0, x1, y1 = R("note")
    d.rectangle((x0 + 6, y0 + 6, x1 - 6, y1 - 6), fill=PAPER)
    for k in range(7):
        d.rectangle((x0 + 18, y0 + 26 + k * 17, x1 - 18 - (k % 3) * 14, y0 + 30 + k * 17), fill=(90, 80, 70))
    d.rectangle((x0 + 50, y0, x1 - 50, y0 + 14), fill=(200, 196, 170, 220))       # скотч
    # трафаретная звезда
    import math
    x0, y0, x1, y1 = R("star")
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    pts = [(cx + (56 if i % 2 == 0 else 22) * math.sin(i * math.pi / 5), cy - (56 if i % 2 == 0 else 22) * math.cos(i * math.pi / 5))
           for i in range(10)]
    d.polygon(pts, fill=WHITE)
    # изолента (красная, серая) — полоска с неровными концами
    for n, c in (("tape_red", RED), ("tape_grey", (120, 122, 118))):
        x0, y0, x1, y1 = R(n)
        d.polygon([(x0 + 6, y0 + 8), (x1 - 4, y0 + 6), (x1 - 10, y1 - 6), (x0 + 2, y1 - 8)], fill=c)
    # трафарет на ящик
    x0, y0, x1, y1 = R("stencil_box")
    _center_text(d, (x0, y0, x1, y0 + 80), "SUPPLY", 44, WHITE)
    _center_text(d, (x0, y0 + 70, x1, y1), "NO. 4-117", 26, WHITE)
    # белая бирка с текстом
    x0, y0, x1, y1 = R("label_white")
    d.rectangle((x0 + 4, y0 + 4, x1 - 4, y1 - 4), fill=WHITE)
    d.rectangle((x0 + 4, y0 + 4, x1 - 4, y0 + 26), fill=BLACK)
    _center_text(d, (x0, y0 + 26, x1, y1 - 4), "L-07", 40, BLACK)
    im.save(os.path.join(HERE, "decals.png"))


def rect(name):
    """(u0, v0, u1, v1) картинки в атласе и её пропорции (ширина / высота)."""
    x, y, w, h = DECALS[name]
    W, H = SIZE
    return (x / W, 1 - (y + h) / H, (x + w) / W, 1 - y / H), w / h


if __name__ == "__main__":
    build()
    print("decals.png — готово")
