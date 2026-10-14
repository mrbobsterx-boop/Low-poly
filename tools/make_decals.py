"""Партия 2 (автор 2026-10-14): плакаты, надписи, граффити и мелочи на стену — рисуются кодом (PIL), потом плоская модель
на стену (Blender как модуль bpy). Надписи — на английском и немецком (решение автора): у каждой вещи с текстом два
варианта, `<имя>_en` и `<имя>_de`; без текста (череп, рожица, рисунок…) — один.

Запуск (из корня репозитория, Python с bpy и Pillow):
    python3 tools/make_decals.py            # все → export/<имя>_idle.glb + лист renders/_review/decals_<дата>.jpg
    python3 tools/make_decals.py имя1 имя2  # только эти (имя без _en/_de — оба языка)

Модель — на стену: спина в Y = 0 (вещь чуть впереди стены, к камере −Y), низ в Z = 0, по центру X.
Бумага — непрозрачная с рваными краями (вырез по прозрачности), краска — прозрачная вокруг букв (alpha clip).
Стиль — как у моделей Tripo: тёплые выцветшие цвета, грязь, пятна, потёртости.
"""
import datetime
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FONTS = os.path.join(ROOT, "tools", "fonts")
TMP = os.path.join(ROOT, "renders", "_review", "_decals")


def font(name, size):
    files = {"oswald": "Oswald.ttf", "bebas": "BebasNeue-Regular.ttf", "stencil": "StardosStencil-Bold.ttf",
             "army": "BlackOpsOne-Regular.ttf", "type": "SpecialElite-Regular.ttf", "marker": "PermanentMarker-Regular.ttf",
             "scrawl": "RockSalt-Regular.ttf", "hand": "Caveat.ttf"}
    f = ImageFont.truetype(os.path.join(FONTS, files[name]), size)
    if name == "oswald":
        try:
            f.set_variation_by_axes([700])
        except Exception:
            pass
    if name == "hand":
        try:
            f.set_variation_by_axes([600])
        except Exception:
            pass
    return f


# ───────────────────────── кисти ─────────────────────────

def noise(w, h, rng, scale=8, lo=0, hi=255):
    """Мягкий шум: мелкая случайная картинка, растянутая с размытием."""
    small = Image.new("L", (max(2, w // scale), max(2, h // scale)))
    small.putdata([rng.randint(lo, hi) for _ in range(small.width * small.height)])
    return small.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale / 3))


def tint(im, col, mask):
    """Наложить цвет col по маске (L) поверх im."""
    layer = Image.new("RGBA", im.size, col + (255,))
    im.paste(layer, (0, 0), mask)


def fit_text(d, xy_box, text, fname, fill, max_size=200, align="center", spacing=0.1, stroke=0, stroke_fill=None):
    """Текст по центру прямоугольника, размер — наибольший, чтобы влез (строки через \\n)."""
    x0, y0, x1, y1 = xy_box
    size = max_size
    while size > 8:
        f = font(fname, size)
        bb = d.multiline_textbbox((0, 0), text, font=f, align=align, spacing=int(size * spacing), stroke_width=stroke)
        if bb[2] - bb[0] <= x1 - x0 and bb[3] - bb[1] <= y1 - y0:
            break
        size -= 2
    tx = x0 + (x1 - x0 - (bb[2] - bb[0])) / 2 - bb[0]
    ty = y0 + (y1 - y0 - (bb[3] - bb[1])) / 2 - bb[1]
    d.multiline_text((tx, ty), text, font=f, fill=fill, align=align, spacing=int(size * spacing), stroke_width=stroke,
                     stroke_fill=stroke_fill)
    return f


def paper(w, h, col, rng, torn=True, stains=True):
    """Лист бумаги: цвет, зерно, пятна, выцветшие края, сгибы; рваные края — через прозрачность."""
    im = Image.new("RGBA", (w, h), col + (255,))
    g = noise(w, h, rng, 3, 90, 165)
    im = Image.composite(Image.new("RGBA", (w, h), tuple(int(c * 0.9) for c in col) + (255,)), im,
                         g.point(lambda v: 60 if v > 128 else 0))
    if stains:
        for _ in range(rng.randint(2, 5)):
            m = Image.new("L", (w, h), 0)
            dm = ImageDraw.Draw(m)
            cx, cy, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(0.08, 0.25) * w
            dm.ellipse((cx - r, cy - r * rng.uniform(0.5, 1.2), cx + r, cy + r * rng.uniform(0.5, 1.2)), fill=rng.randint(30, 70))
            m = m.filter(ImageFilter.GaussianBlur(r / 3))
            tint(im, (120, 90, 50), m)
    return im


def age(im, rng, fade=0.12, dirt=0.35, folds=True, torn=True):
    """Состарить: выцвести, грязь по краям, сгибы, рваные края (прозрачность)."""
    w, h = im.size
    rgb = im.convert("RGB")
    grey = Image.new("RGB", (w, h), (200, 190, 170))
    rgb = Image.blend(rgb, grey, fade)
    edge = Image.new("L", (w, h), 0)
    de = ImageDraw.Draw(edge)
    for k in range(18):
        de.rectangle((k * 3, k * 3, w - k * 3, h - k * 3), outline=int(120 * (1 - k / 18) * dirt * 2.2))
    edge = edge.filter(ImageFilter.GaussianBlur(14))
    dirtn = noise(w, h, rng, 20, 0, 255)
    edge = ImageChops.multiply(edge, dirtn.point(lambda v: min(255, v + 60)))
    rgb.paste(Image.new("RGB", (w, h), (70, 55, 35)), (0, 0), edge)
    out = rgb.convert("RGBA")
    if folds:
        d = ImageDraw.Draw(out)
        for fx in (w // 2,):
            d.line((fx, 0, fx + rng.randint(-4, 4), h), fill=(0, 0, 0, 0), width=0)
            line = Image.new("L", (w, h), 0)
            ImageDraw.Draw(line).line((fx, 0, fx + rng.randint(-4, 4), h), fill=70, width=3)
            out.paste(Image.new("RGBA", (w, h), (60, 50, 40, 255)), (0, 0), line.filter(ImageFilter.GaussianBlur(1.5)))
        line = Image.new("L", (w, h), 0)
        ImageDraw.Draw(line).line((0, h // 2, w, h // 2 + rng.randint(-4, 4)), fill=60, width=3)
        out.paste(Image.new("RGBA", (w, h), (60, 50, 40, 255)), (0, 0), line.filter(ImageFilter.GaussianBlur(1.5)))
    a = Image.new("L", (w, h), 255)
    if torn:
        da = ImageDraw.Draw(a)
        pts = []
        steps = 40
        for side in range(4):   # рваный край: по периметру с маленькими зубцами, один уголок оторван
            for k in range(steps):
                t = k / steps
                j = rng.uniform(0, 7)
                if side == 0:
                    pts.append((t * w, j))
                elif side == 1:
                    pts.append((w - j, t * h))
                elif side == 2:
                    pts.append((w - t * w, h - j))
                else:
                    pts.append((j, h - t * h))
        da.rectangle((0, 0, w, h), fill=0)
        da.polygon(pts, fill=255)
        c = rng.choice([(0, 0), (w, 0), (w, h), (0, h)])
        r = rng.uniform(0.08, 0.16) * w
        da.polygon([(c[0], c[1]), (c[0] + (r if c[0] == 0 else -r), c[1]), (c[0], c[1] + (r if c[1] == 0 else -r))], fill=0)
    out.putalpha(ImageChops.multiply(a, out.getchannel("A")))
    return out


def pins(im, rng, tape=False):
    """Кнопки по углам (или скотч)."""
    w, h = im.size
    d = ImageDraw.Draw(im)
    for cx, cy in ((0.07, 0.04), (0.93, 0.04)):
        x, y = cx * w, cy * h + 8
        if tape:
            d.polygon([(x - 34, y - 14), (x + 34, y - 20), (x + 38, y + 10), (x - 30, y + 16)], fill=(225, 215, 170, 200))
        else:
            d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(160, 40, 30, 255), outline=(90, 20, 15, 255), width=2)
            d.ellipse((x - 4, y - 5, x + 1, y), fill=(230, 140, 120, 255))


def spray(w, h, draw_fn, col, rng, drips=True, over=True, rough=0.25):
    """Краска из баллончика: рисунок draw_fn(d) маской → цвет, туманная кромка, подтёки, потёртости."""
    m = Image.new("L", (w, h), 0)
    draw_fn(ImageDraw.Draw(m))
    if drips:
        px = m.load()
        dm = ImageDraw.Draw(m)
        for _ in range(int(w / 25)):
            x = rng.randint(0, w - 1)
            ys = [y for y in range(h - 1, 0, -3) if px[x, y] > 128]
            if ys:
                y0 = ys[0]
                L = rng.uniform(0.04, 0.18) * h
                wd = rng.randint(2, 5)
                dm.line((x, y0, x, y0 + L), fill=230, width=wd)
                dm.ellipse((x - wd, y0 + L - wd, x + wd, y0 + L + wd), fill=230)
    halo = m.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.45)) if over else Image.new("L", (w, h), 0)
    wear = noise(w, h, rng, 6, 0, 255).point(lambda v: 0 if v < 255 * rough else 255)
    core = ImageChops.multiply(m, wear)
    alpha = ImageChops.lighter(core, ImageChops.multiply(halo, wear))
    im = Image.new("RGBA", (w, h), col + (255,))
    shade = noise(w, h, rng, 30, 200, 255)
    im = Image.merge("RGBA", [ImageChops.multiply(im.getchannel(c), shade) for c in "RGB"] + [alpha])
    return im


def over(base, top):
    out = base.copy()
    out.alpha_composite(top)
    return out


# ───────────────────────── картинки ─────────────────────────

PAPER = (226, 214, 184)
INK = (40, 36, 32)
RED = (170, 45, 35)
BLUE = (50, 85, 130)
GREEN = (60, 105, 70)
YEL = (220, 170, 50)

T = {   # тексты: en / de
    "water": (("SAVE WATER", "EVERY DROP COUNTS"), ("WASSER SPAREN", "JEDER TROPFEN ZÄHLT")),
    "gasmask": (("YOUR GAS MASK\nIS YOUR FRIEND", "KEEP IT CLOSE. KEEP IT CLEAN."),
                ("DEINE GASMASKE\nIST DEIN FREUND", "IMMER GRIFFBEREIT. IMMER SAUBER.")),
    "map": (("DISTRICT 7", "SHELTER", "DANGER"), ("BEZIRK 7", "BUNKER", "GEFAHR")),
    "duty": (("DUTY ROSTER", ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"], ["WATER", "GUARD", "COOK"]),
             ("DIENSTPLAN", ["MO", "DI", "MI", "DO", "FR", "SA", "SO"], ["WASSER", "WACHE", "KOCHEN"])),
    "rules": (("SHELTER RULES", ["1. CLOSE THE DOOR", "2. NO LIGHT AT NIGHT", "3. SHARE THE FOOD", "4. REPORT BITES",
                                 "5. NOBODY LEAVES ALONE"]),
              ("BUNKERREGELN", ["1. TÜR SCHLIESSEN", "2. NACHTS KEIN LICHT", "3. ESSEN TEILEN", "4. BISSE MELDEN",
                                "5. NIEMAND GEHT ALLEIN"])),
    "aid": (("FIRST AID", ["STOP THE BLEEDING", "CLEAN THE WOUND", "BANDAGE TIGHT", "KEEP WARM"]),
            ("ERSTE HILFE", ["BLUTUNG STOPPEN", "WUNDE REINIGEN", "FEST VERBINDEN", "WARM HALTEN"])),
    "ad": (("FIZZ COLA", "ICE COLD REFRESHMENT!"), ("FIZZ COLA", "EISKALTE ERFRISCHUNG!")),
    "wanted": (("WANTED", "DEAD OR ALIVE", "REWARD: 500 CAPS"), ("GESUCHT", "TOT ODER LEBENDIG", "BELOHNUNG: 500 KRONKORKEN")),
    "iron": (("JOIN THE\nIRON WHEEL", "STRENGTH • ORDER • STEEL"), ("TRITT DEM\nEISERNEN RAD BEI", "STÄRKE • ORDNUNG • STAHL")),
    "well": (("WELLSPRING", "CLEAN WATER FOR ALL"), ("WELLSPRING", "SAUBERES WASSER FÜR ALLE")),
    "exit": ("EXIT", "AUSGANG"),
    "keep_out": ("KEEP OUT", "BETRETEN\nVERBOTEN"),
    "food": ("FOOD HERE", "HIER ESSEN"),
    "infected": (("INFECTED", "DO NOT ENTER"), ("INFIZIERT", "NICHT BETRETEN")),
    "alive": ("WE ARE\nSTILL ALIVE", "WIR LEBEN\nNOCH"),
    "note": (("Gone to the river.\nBack before dark.\nDon't open the door!\n- M.", "Water filter\nis broken again"),
             ("Bin am Fluss.\nZurück vor Dunkelheit.\nTür nicht öffnen!\n- M.", "Wasserfilter\nschon wieder kaputt")),
    "cal": (("OCTOBER", ["M", "T", "W", "T", "F", "S", "S"]), ("OKTOBER", ["M", "D", "M", "D", "F", "S", "S"])),
}


def drop(d, cx, cy, r, fill):
    d.polygon([(cx, cy - r * 1.6), (cx - r * 0.9, cy - r * 0.1), (cx + r * 0.9, cy - r * 0.1)], fill=fill)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)


def poster_water(lang, rng):
    t = T["water"][lang]
    im = paper(512, 720, PAPER, rng)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 512, 200), fill=BLUE + (255,))
    fit_text(d, (30, 30, 482, 175), t[0], "oswald", (240, 232, 210))
    drop(d, 256, 420, 95, (70, 130, 180))
    d.ellipse((215, 380, 245, 410), fill=(190, 220, 235))
    d.rectangle((40, 585, 472, 590), fill=INK)
    fit_text(d, (40, 600, 472, 680), t[1], "oswald", INK)
    im = age(im, rng)
    pins(im, rng)
    return im


def gasmask_icon(d, cx, cy, s, col, glass):
    d.rounded_rectangle((cx - s, cy - s * 1.1, cx + s, cy + s * 0.9), radius=s * 0.6, fill=col)
    for sx in (-1, 1):
        d.ellipse((cx + sx * s * 0.45 - s * 0.32, cy - s * 0.55, cx + sx * s * 0.45 + s * 0.32, cy + s * 0.05), fill=glass)
    d.rounded_rectangle((cx - s * 0.35, cy + s * 0.3, cx + s * 0.35, cy + s * 1.25), radius=s * 0.15, fill=col)
    for k in range(4):
        y = cy + s * (0.45 + 0.2 * k)
        d.line((cx - s * 0.3, y, cx + s * 0.3, y), fill=glass, width=4)


def poster_gasmask(lang, rng):
    t = T["gasmask"][lang]
    im = paper(512, 720, (214, 196, 150), rng)
    d = ImageDraw.Draw(im)
    fit_text(d, (30, 25, 482, 200), t[0], "oswald", RED)
    gasmask_icon(d, 256, 380, 120, (60, 70, 60), (180, 200, 190))
    fit_text(d, (30, 600, 482, 680), t[1], "oswald", INK)
    im = age(im, rng)
    pins(im, rng, tape=True)
    return im


def poster_map(lang, rng):
    t = T["map"][lang]
    im = paper(720, 540, (220, 210, 180), rng)
    d = ImageDraw.Draw(im)
    fit_text(d, (20, 10, 700, 70), t[0], "type", INK)
    for _ in range(6):   # дороги
        if rng.random() < 0.5:
            y = rng.randint(90, 520)
            d.line((10, y, 710, y + rng.randint(-40, 40)), fill=(120, 110, 95), width=rng.randint(6, 14))
        else:
            x = rng.randint(20, 700)
            d.line((x, 80, x + rng.randint(-60, 60), 530), fill=(120, 110, 95), width=rng.randint(6, 14))
    d.line((0, 470, 720, 380), fill=(90, 140, 180), width=26)   # река
    for _ in range(14):   # кварталы
        x, y = rng.randint(30, 660), rng.randint(90, 480)
        d.rectangle((x, y, x + rng.randint(25, 60), y + rng.randint(20, 45)), outline=(100, 90, 75), width=2)
    sx, sy = 250, 250
    d.ellipse((sx - 22, sy - 22, sx + 22, sy + 22), outline=GREEN, width=6)
    fit_text(d, (sx - 90, sy + 25, sx + 90, sy + 60), t[1], "hand", GREEN)
    for _ in range(3):
        x, y = rng.randint(400, 680), rng.randint(110, 330)
        d.line((x - 18, y - 18, x + 18, y + 18), fill=RED, width=7)
        d.line((x - 18, y + 18, x + 18, y - 18), fill=RED, width=7)
    fit_text(d, (440, 340, 700, 380), t[2] + "!", "hand", RED)
    d.line((sx + 30, sy - 10, 420, 150), fill=RED, width=3)
    im = age(im, rng, fade=0.08)
    pins(im, rng)
    return im


def poster_duty(lang, rng):
    t = T["duty"][lang]
    im = paper(560, 720, (238, 234, 222), rng, stains=True)
    d = ImageDraw.Draw(im)
    fit_text(d, (50, 40, 510, 100), t[0], "type", INK)
    x0, y0, cw, rh = 40, 115, 120, 78
    names = ["Anna", "Max", "Jonas", "Lea", "Tom", "Mia", "Paul", "Eva", "Ben", "Lina"]
    for i, task in enumerate(t[2]):
        fit_text(d, (x0 + cw * (i + 1) + 6, y0 + 8, x0 + cw * (i + 2) - 6, y0 + rh - 8), task, "type", INK, max_size=30)
    for r, day in enumerate(t[1]):
        y = y0 + rh * (r + 1) * 0.9 + 10
        fit_text(d, (x0, y, x0 + cw, y + rh * 0.8), day, "type", INK, max_size=34)
        for c in range(3):
            fit_text(d, (x0 + cw * (c + 1) + 10, y + 6, x0 + cw * (c + 2) - 10, y + rh * 0.75), rng.choice(names), "hand", BLUE, max_size=40)
    for k in range(9):
        y = y0 + rh * k * 0.9 + 10 if k else y0
        d.line((x0, y, x0 + cw * 4, y), fill=INK, width=2)
    for k in range(5):
        d.line((x0 + cw * k, y0, x0 + cw * k, y0 + rh * 8 * 0.9 + 10), fill=INK, width=2)
    im = age(im, rng, fade=0.06, folds=False)
    pins(im, rng, tape=True)
    return im


def poster_list(key, col_head, icon):
    def make(lang, rng):
        t = T[key][lang]
        im = paper(512, 720, PAPER, rng)
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 512, 150), fill=col_head + (255,))
        fit_text(d, (30, 20, 482, 130), t[0], "oswald", (245, 238, 220))
        if icon == "cross":
            d.rectangle((226, 175, 286, 315), fill=RED)
            d.rectangle((186, 215, 326, 275), fill=RED)
            ytop = 345
        else:
            ytop = 180
        step = (680 - ytop) / len(t[1])
        for i, line in enumerate(t[1]):
            fit_text(d, (40, ytop + i * step, 472, ytop + (i + 0.85) * step), line, "bebas", INK, max_size=60)
        im = age(im, rng)
        pins(im, rng)
        return im
    return make


def poster_ad(lang, rng):
    t = T["ad"][lang]
    im = paper(512, 720, (200, 70, 55), rng)
    d = ImageDraw.Draw(im)
    fit_text(d, (30, 30, 482, 200), t[0], "bebas", (250, 240, 215))
    d.rounded_rectangle((200, 240, 312, 560), radius=40, fill=(60, 30, 25))   # бутылка
    d.rectangle((235, 205, 277, 250), fill=(60, 30, 25))
    d.rectangle((228, 195, 284, 210), fill=(200, 200, 190))
    d.rectangle((200, 360, 312, 440), fill=(245, 235, 210))
    fit_text(d, (205, 370, 307, 430), "FIZZ", "bebas", (200, 60, 50))
    for k in range(10):   # пузырьки и лучи
        a = 2 * math.pi * k / 10
        d.line((256 + math.cos(a) * 180, 400 + math.sin(a) * 180, 256 + math.cos(a) * 240, 400 + math.sin(a) * 240), fill=(240, 200, 90), width=10)
    fit_text(d, (30, 600, 482, 690), t[1], "bebas", (250, 240, 215))
    im = age(im, rng, fade=0.32, dirt=0.5)   # старая — сильно выцвела
    return im


def poster_wanted(lang, rng):
    t = T["wanted"][lang]
    im = paper(512, 720, (222, 198, 150), rng)
    d = ImageDraw.Draw(im)
    fit_text(d, (30, 20, 482, 140), t[0], "type", INK)
    d.rectangle((126, 160, 386, 440), fill=(200, 180, 140), outline=INK, width=4)
    d.ellipse((206, 200, 306, 310), fill=(70, 60, 50))                     # силуэт
    d.rounded_rectangle((166, 320, 346, 440), radius=50, fill=(70, 60, 50))
    fit_text(d, (30, 460, 482, 540), t[1], "type", INK)
    fit_text(d, (30, 560, 482, 660), t[2], "type", RED)
    im = age(im, rng, fade=0.1)
    pins(im, rng)
    return im


def gear(d, cx, cy, r, col, teeth=10):
    pts = []
    for k in range(teeth * 2):
        a = math.pi * k / teeth
        rr = r if k % 2 == 0 else r * 0.8
        for da in (-0.12, 0.12):
            pts.append((cx + math.cos(a + da) * rr, cy + math.sin(a + da) * rr))
    d.polygon(pts, fill=col)
    d.ellipse((cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35), fill=0 if d.mode == "L" else (0, 0, 0, 0))


def poster_iron(lang, rng):
    t = T["iron"][lang]
    im = paper(512, 720, (60, 58, 56), rng)
    d = ImageDraw.Draw(im)
    gear(d, 256, 300, 150, (190, 120, 50))
    d.ellipse((206, 250, 306, 350), fill=(60, 58, 56))
    fit_text(d, (30, 470, 482, 620), t[0], "army", (230, 220, 200))
    fit_text(d, (30, 640, 482, 690), t[1], "army", (190, 120, 50))
    im = age(im, rng, fade=0.1, dirt=0.4)
    return im


def poster_well(lang, rng):
    t = T["well"][lang]
    im = paper(512, 720, (210, 225, 220), rng)
    d = ImageDraw.Draw(im)
    for k in range(5):   # волны
        y = 470 + k * 22
        d.line([(x, y + 8 * math.sin(x / 30 + k)) for x in range(0, 512, 8)], fill=(70, 130, 160), width=8)
    drop(d, 256, 300, 105, (70, 130, 170))
    d.ellipse((215, 255, 250, 290), fill=(200, 230, 240))
    fit_text(d, (30, 25, 482, 140), t[0], "oswald", (40, 80, 110))
    fit_text(d, (30, 620, 482, 690), t[1], "oswald", (40, 80, 110))
    im = age(im, rng)
    pins(im, rng)
    return im


# ── краска на стене ──

def text_fn(text, fname, box, align="center"):
    return lambda d: fit_text(d, box, text, fname, 255, max_size=400, align=align)


def arrow_shape(d, x0, y, x1, th, head):
    d.rectangle((x0, y - th, x1 - head, y + th), fill=255)
    d.polygon([(x1 - head, y - th * 2.6), (x1, y), (x1 - head, y + th * 2.6)], fill=255)


def paint_exit(lang, rng):
    t = T["exit"][lang]

    def fn(d):
        fit_text(d, (20, 40, 700, 300), t, "stencil", 255, max_size=300)
        arrow_shape(d, 730, 170, 1000, 30, 100)
    return spray(1024, 340, fn, (230, 230, 220), rng, drips=False, rough=0.2)


def paint_keep_out(lang, rng):
    return spray(1024, 420, text_fn(T["keep_out"][lang], "marker", (30, 30, 994, 360)), (180, 30, 25), rng)


def paint_food(lang, rng):
    t = T["food"][lang]

    def fn(d):
        fit_text(d, (20, 20, 760, 300), t, "marker", 255, max_size=300)
        arrow_shape(d, 770, 170, 1010, 22, 80)
    return spray(1024, 340, fn, (230, 190, 60), rng)


def paint_infected(lang, rng):
    t = T["infected"][lang]

    def fn(d):
        d.ellipse((30, 30, 330, 330), outline=255, width=26)
        d.line((75, 75, 285, 285), fill=255, width=26)
        fit_text(d, (370, 40, 1000, 200), t[0], "marker", 255, max_size=300)
        fit_text(d, (370, 210, 1000, 330), t[1], "marker", 255, max_size=200)
    return spray(1024, 360, fn, (190, 35, 30), rng)


def paint_arrows(lang, rng):
    def fn(d):
        arrow_shape(d, 30, 110, 470, 26, 110)
        d.polygon([(600, 40), (660, 40), (660, 230), (720, 230), (630, 330), (540, 230), (600, 230)], fill=255)
        arrow_shape(d, 790, 110, 1000, 18, 70)
    return spray(1024, 360, fn, (235, 235, 225), rng, drips=False, rough=0.18)


def paint_room_number(lang, rng):
    def fn(d):
        d.rectangle((40, 40, 472, 300), outline=255, width=18)
        fit_text(d, (70, 60, 442, 280), "B-07", "stencil", 255, max_size=300)
    return spray(512, 340, fn, (230, 200, 60), rng, drips=False, rough=0.2)


def graffiti_skull(lang, rng):
    def fn(d):
        d.ellipse((96, 40, 416, 330), fill=255)
        d.rounded_rectangle((170, 280, 342, 420), radius=30, fill=255)
        for ex in (190, 322):
            d.ellipse((ex - 50, 150, ex + 50, 260), fill=0)
        d.polygon([(256, 270), (232, 320), (280, 320)], fill=0)
        for k in range(5):
            d.rectangle((190 + k * 28, 360, 204 + k * 28, 420), fill=0)
        for a, b in (((40, 380), (472, 470)), ((40, 470), (472, 380))):   # кости
            d.line((a, b), fill=255, width=34)
    return spray(512, 512, fn, (235, 235, 230), rng)


def graffiti_alive(lang, rng):
    return spray(1024, 512, text_fn(T["alive"][lang], "marker", (30, 30, 994, 480)), (60, 150, 90), rng)


def graffiti_tag(lang, rng):
    def fn(d):
        fit_text(d, (30, 40, 994, 330), "RUST", "scrawl", 255, max_size=400)
        d.arc((60, 250, 960, 420), 10, 170, fill=255, width=14)
    a = spray(1024, 420, fn, (210, 90, 40), rng)
    b = spray(1024, 420, lambda d: fit_text(d, (60, 70, 964, 300), "RUST", "scrawl", 255, max_size=400), (40, 40, 45), rng, drips=False)
    return over(b, a)


def graffiti_smile(lang, rng):
    def fn(d):
        d.ellipse((40, 40, 472, 472), outline=255, width=30)
        d.ellipse((160, 160, 210, 250), fill=255)
        d.ellipse((302, 160, 352, 250), fill=255)
        d.arc((130, 180, 382, 400), 20, 160, fill=255, width=30)
    return spray(512, 512, fn, (240, 200, 50), rng)


def graffiti_faction_signs(lang, rng):
    def fn(d):
        gear(d, 170, 180, 120, 255)
        drop(d, 512, 210, 85, 255)
        d.polygon([(780, 80), (900, 140), (960, 260), (840, 230), (760, 300), (700, 200)], fill=255)   # собачья голова (Rust Dogs)
        d.polygon([(780, 80), (810, 20), (840, 100)], fill=255)
    return spray(1024, 380, fn, (230, 230, 220), rng)


def tally_days(lang, rng):
    def fn(d):
        x = 30
        for grp in range(7):
            for k in range(4):
                xx = x + k * 26
                d.line((xx + rng.randint(-3, 3), 40 + rng.randint(-6, 6), xx + rng.randint(-5, 5), 230 + rng.randint(-6, 6)), fill=255, width=9)
            d.line((x - 15, 200, x + 100, 70), fill=255, width=9)
            x += 140
    im = spray(1024, 280, fn, (235, 235, 230), rng, drips=False, over=False, rough=0.3)
    return im


def kid_drawing(lang, rng):
    im = paper(600, 440, (245, 242, 232), rng, stains=False)
    d = ImageDraw.Draw(im)

    def crayon(pts, col, w=8):
        for a, b in zip(pts, pts[1:]):
            d.line((a[0] + rng.randint(-2, 2), a[1] + rng.randint(-2, 2), b[0], b[1]), fill=col, width=w)
    d.ellipse((470, 30, 560, 120), fill=(240, 190, 40))
    for k in range(8):
        a = 2 * math.pi * k / 8
        crayon([(515 + math.cos(a) * 55, 75 + math.sin(a) * 55), (515 + math.cos(a) * 85, 75 + math.sin(a) * 85)], (240, 190, 40), 6)
    crayon([(80, 330), (80, 200), (200, 200), (200, 330), (80, 330)], (190, 60, 50))
    crayon([(65, 205), (140, 120), (215, 205)], (150, 70, 40))
    d.rectangle((120, 260, 160, 330), fill=(120, 80, 50))
    for i, x in enumerate((280, 350, 410)):
        h = 1.0 if i < 2 else 0.7
        d.ellipse((x - 18 * h, 330 - 150 * h, x + 18 * h, 330 - 114 * h), outline=INK, width=5)
        crayon([(x, 330 - 114 * h), (x, 330 - 50 * h), (x - 22, 330), ], INK, 5)
        crayon([(x, 330 - 50 * h), (x + 22, 330)], INK, 5)
        crayon([(x - 30 * h, 330 - 95 * h), (x + 30 * h, 330 - 95 * h)], INK, 5)
    crayon([(0, 345), (600, 345)], (80, 150, 60), 14)
    im = age(im, rng, fade=0.06, folds=True)
    pins(im, rng, tape=True)
    return im


def notes_nail(lang, rng):
    t = T["note"][lang]
    im = Image.new("RGBA", (600, 600), (0, 0, 0, 0))
    a = paper(420, 360, (240, 232, 200), rng, stains=True)
    da = ImageDraw.Draw(a)
    fit_text(da, (25, 30, 395, 330), t[0], "hand", BLUE, align="left")
    a = age(a, rng, fade=0.05, folds=False).rotate(rng.uniform(-6, -2), expand=True, resample=Image.BICUBIC)
    b = paper(300, 240, (235, 220, 150), rng, stains=False)
    fit_text(ImageDraw.Draw(b), (20, 30, 280, 210), t[1], "hand", RED)
    b = age(b, rng, fade=0.05, folds=False).rotate(rng.uniform(5, 10), expand=True, resample=Image.BICUBIC)
    im.alpha_composite(b, (300, 340))
    im.alpha_composite(a, (10, 10))
    d = ImageDraw.Draw(im)
    for x, y in ((220, 34), (450, 360)):   # гвозди
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(110, 105, 100, 255), outline=(60, 55, 50, 255), width=2)
    return im


def calendar_crossed(lang, rng):
    t = T["cal"][lang]
    im = paper(480, 640, (240, 236, 226), rng, stains=True)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 480, 260), fill=(120, 150, 170))
    for k in range(4):   # картинка — горы
        x = k * 140 - 40
        d.polygon([(x, 260), (x + 110, 90 + 30 * (k % 2)), (x + 220, 260)], fill=(80 + 15 * k, 100 + 10 * k, 110))
    fit_text(d, (20, 270, 460, 330), t[0], "oswald", INK)
    cw = 440 / 7
    for i, dn in enumerate(t[1]):
        fit_text(d, (20 + i * cw, 335, 20 + (i + 1) * cw, 365), dn, "oswald", RED if i == 6 else INK, max_size=26)
    day = 1
    start = 3
    for r in range(5):
        for c in range(7):
            n = r * 7 + c - start + 1
            if 1 <= n <= 31:
                x, y = 20 + c * cw, 375 + r * 50
                fit_text(d, (x + 6, y + 6, x + cw - 6, y + 44), str(n), "oswald", INK, max_size=30)
                if n <= 22:
                    d.line((x + 6, y + 6, x + cw - 6, y + 44), fill=RED, width=4)
                    d.line((x + cw - 6, y + 6, x + 6, y + 44), fill=RED, width=4)
    im = age(im, rng, fade=0.06, folds=False, torn=False)
    d = ImageDraw.Draw(im)
    d.ellipse((230, -2, 250, 18), fill=(110, 105, 100, 255))
    return im


def clock_face(rng):
    im = Image.new("RGBA", (512, 512), (230, 222, 200, 255))
    d = ImageDraw.Draw(im)
    for k in range(12):
        a = 2 * math.pi * k / 12 - math.pi / 2
        r0 = 200 if k % 3 else 175
        d.line((256 + math.cos(a) * r0, 256 + math.sin(a) * r0, 256 + math.cos(a) * 225, 256 + math.sin(a) * 225), fill=INK, width=10 if k % 3 == 0 else 6)
    for k, n in ((0, "12"), (3, "3"), (6, "6"), (9, "9")):
        a = 2 * math.pi * k / 12 - math.pi / 2
        fit_text(d, (256 + math.cos(a) * 145 - 35, 256 + math.sin(a) * 145 - 30, 256 + math.cos(a) * 145 + 35, 256 + math.sin(a) * 145 + 30), n, "oswald", INK, max_size=60)
    for ang, ln, w in ((math.radians(-60 - 90), 110, 14), (math.radians(80 - 90), 170, 8)):   # стрелки стоят
        d.line((256, 256, 256 + math.cos(ang) * ln, 256 + math.sin(ang) * ln), fill=INK, width=w)
    d.ellipse((244, 244, 268, 268), fill=RED)
    d.line((120, 330, 330, 150), fill=(60, 60, 60, 120), width=3)   # трещина на стекле
    d.line((330, 150, 380, 120), fill=(60, 60, 60, 120), width=2)
    return age(im, rng, fade=0.1, dirt=0.25, folds=False, torn=False)


# ── партия 3: следы на стенах (мягкие края — прозрачность плавная, вид «stain») ──

def _rgba(col, alpha):
    im = Image.new("RGBA", alpha.size, col + (255,))
    im.putalpha(alpha)
    return im


def _shade(im, rng, lo=190):
    sh = noise(im.width, im.height, rng, 24, lo, 255)
    r, g, b, a = im.split()
    return Image.merge("RGBA", [ImageChops.multiply(c, sh) for c in (r, g, b)] + [a])


def wall_crack(lang, rng):
    w, h = 1024, 1024
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    chip = Image.new("L", (w, h), 0)
    dc = ImageDraw.Draw(chip)

    def branch(x, y, ang, L, wd, depth):
        pts = [(x, y)]
        for _ in range(int(L / 18)):
            ang += rng.uniform(-0.45, 0.45)
            x, y = x + math.cos(ang) * 18, y + math.sin(ang) * 18
            pts.append((x, y))
        d.line(pts, fill=255, width=max(1, int(wd)), joint="curve")
        dc.line(pts, fill=150, width=int(wd * 4 + 6))
        if depth < 3:
            for _ in range(rng.randint(1, 3)):
                k = rng.randint(1, len(pts) - 1)
                branch(pts[k][0], pts[k][1], ang + rng.choice((-1, 1)) * rng.uniform(0.5, 1.1), L * 0.55, wd * 0.6, depth + 1)
    for k in range(4):
        branch(w / 2, h / 2, k * math.pi / 2 + rng.uniform(-0.4, 0.4), 420, 7, 0)
    dc.ellipse((w / 2 - 50, h / 2 - 40, w / 2 + 50, h / 2 + 40), fill=200)   # выбитый кусок в центре
    d.ellipse((w / 2 - 22, h / 2 - 16, w / 2 + 22, h / 2 + 16), fill=255)
    chip = chip.filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * 0.5))
    light = _rgba((200, 195, 185), chip)
    dark = _rgba((25, 22, 20), m.filter(ImageFilter.GaussianBlur(0.8)))
    return over(light, dark)


def wall_leak(lang, rng):
    w, h = 1024, 1024
    a = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(a)
    d.rectangle((0, 0, w, 70), fill=170)   # мокрая полоса сверху
    for _ in range(22):
        x = rng.uniform(40, w - 40)
        L = rng.uniform(0.3, 0.95) * h
        wd = rng.uniform(10, 45)
        d.line([(x + math.sin(t / 60) * 6, t) for t in range(0, int(L), 20)], fill=rng.randint(90, 170), width=int(wd))
        d.ellipse((x - wd * 0.6, L - wd * 0.6, x + wd * 0.6, L + wd * 0.6), fill=150)
    a = a.filter(ImageFilter.GaussianBlur(14))
    fade = Image.linear_gradient("L").resize((w, h)).point(lambda v: 255 - int(v * 0.55))
    a = ImageChops.multiply(a, fade)
    a = ImageChops.multiply(a, noise(w, h, rng, 12, 150, 255))
    im = _rgba((70, 62, 40), a)
    rim = a.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(2)).point(lambda v: min(255, v * 3))
    return over(im, _rgba((45, 38, 25), rim))


def wall_mold(lang, rng):
    w, h = 1024, 1024
    a = Image.new("L", (w, h), 0)
    for scale, thr in ((40, 150), (14, 165), (5, 175)):
        n = noise(w, h, rng, scale, 0, 255).point(lambda v, t=thr: max(0, min(255, (v - t) * 6)))
        a = ImageChops.lighter(a, n)
    cx, cy = w / 2, h * 0.6   # гуще к низу-середине, к краям сходит на нет
    yy = Image.radial_gradient("L").resize((w, h)).point(lambda v: max(0, 255 - int(v * 1.25)))
    a = ImageChops.multiply(a, yy).filter(ImageFilter.GaussianBlur(1.5))
    im = _rgba((35, 48, 28), a)
    spots = noise(w, h, rng, 6, 0, 255).point(lambda v: 255 if v > 205 else 0)
    spots = ImageChops.multiply(spots, a)
    return _shade(over(im, _rgba((15, 20, 12), spots)), rng, 160)


def wall_soot(lang, rng):
    w, h = 1024, 1024
    a = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(a)
    for k in range(30):   # шлейф копоти снизу вверх, расширяется
        t = k / 30
        y = h - t * h
        r = 120 + t * 330
        d.ellipse((w / 2 - r + rng.uniform(-40, 40), y - r * 0.6, w / 2 + r + rng.uniform(-40, 40), y + r * 0.6), fill=int(230 * (1 - t) + 40))
    a = a.filter(ImageFilter.GaussianBlur(40))
    a = ImageChops.multiply(a, noise(w, h, rng, 30, 120, 255))
    return _rgba((22, 19, 17), a.point(lambda v: int(v * 0.92)))


def wall_bullets(lang, rng):
    w, h = 1024, 768
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for _ in range(9):
        x, y = rng.uniform(100, w - 100), rng.uniform(100, h - 100)
        r = rng.uniform(14, 24)
        chip = Image.new("L", (w, h), 0)
        dc = ImageDraw.Draw(chip)
        pts = []
        for k in range(12):
            a = 2 * math.pi * k / 12
            rr = r * rng.uniform(2.0, 3.2)
            pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
        dc.polygon(pts, fill=170)
        for k in range(rng.randint(3, 6)):
            a = rng.uniform(0, 2 * math.pi)
            dc.line((x, y, x + math.cos(a) * r * 5, y + math.sin(a) * r * 5), fill=210, width=2)
        im = over(im, _rgba((185, 178, 165), chip.filter(ImageFilter.GaussianBlur(1.5))))
        hole = Image.new("L", (w, h), 0)
        ImageDraw.Draw(hole).ellipse((x - r, y - r, x + r, y + r), fill=255)
        im = over(im, _rgba((18, 15, 13), hole.filter(ImageFilter.GaussianBlur(2))))
        ring = Image.new("L", (w, h), 0)
        ImageDraw.Draw(ring).ellipse((x - r * 1.3, y - r * 1.3, x + r * 1.3, y + r * 1.3), outline=140, width=4)
        im = over(im, _rgba((60, 55, 50), ring.filter(ImageFilter.GaussianBlur(2))))
    return im


def _hand(d, x, y, s, ang, fill):
    def rot(px, py):
        return (x + (px * math.cos(ang) - py * math.sin(ang)) * s, y + (px * math.sin(ang) + py * math.cos(ang)) * s)
    d.polygon([rot(*p) for p in ((-40, 0), (40, 0), (45, 70), (-38, 75))], fill=fill)   # ладонь
    d.ellipse([*rot(-42, 5), *rot(42, 80)], fill=fill)
    for fx, fl, fa in ((-30, 75, -0.25), (-10, 90, -0.08), (10, 92, 0.05), (30, 80, 0.18)):
        tip = (fx + math.sin(fa) * fl, -fl)
        d.line([rot(fx, 0), rot(*tip)], fill=fill, width=int(20 * s))
        d.ellipse([*rot(tip[0] - 10, tip[1] - 10), *rot(tip[0] + 10, tip[1] + 10)], fill=fill)
    d.line([rot(-40, 40), rot(-85, -5)], fill=fill, width=int(22 * s))   # большой палец


def wall_handprints(lang, rng):
    w, h = 1024, 1024
    a = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(a)
    for _ in range(5):
        x, y = rng.uniform(180, w - 180), rng.uniform(220, h - 260)
        _hand(d, x, y, rng.uniform(1.0, 1.3), rng.uniform(-0.6, 0.6), rng.randint(170, 240))
        if rng.random() < 0.5:   # смазанный вниз
            L = rng.uniform(100, 240)
            d.polygon([(x - 38, y + 60), (x + 38, y + 60), (x + 14 + rng.uniform(-10, 10), y + 60 + L), (x - 18, y + 60 + L * 0.8)], fill=120)
    a = a.filter(ImageFilter.GaussianBlur(2))
    a = ImageChops.multiply(a, noise(w, h, rng, 4, 110, 255))
    return _rgba((105, 20, 15), a)


def wall_blood(lang, rng):
    w, h = 1024, 1024
    a = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(a)
    cx, cy = w / 2, h * 0.38
    d.ellipse((cx - 150, cy - 110, cx + 150, cy + 120), fill=235)
    for _ in range(70):   # брызги
        ang = rng.uniform(0, 2 * math.pi)
        dist = rng.uniform(120, 420)
        r = rng.uniform(4, 22) * (1.2 - dist / 500)
        x, y = cx + math.cos(ang) * dist, cy + math.sin(ang) * dist * 0.8
        d.ellipse((x - r, y - r, x + r, y + r), fill=235)
    for _ in range(10):   # подтёки вниз
        x = cx + rng.uniform(-130, 130)
        L = rng.uniform(150, 520)
        wd = rng.uniform(8, 20)
        d.line((x, cy + 40, x, cy + L), fill=230, width=int(wd))
        d.ellipse((x - wd, cy + L - wd, x + wd, cy + L + wd), fill=230)
    a = a.filter(ImageFilter.GaussianBlur(1.5))
    im = _rgba((110, 12, 10), a)
    dark = ImageChops.multiply(a, noise(w, h, rng, 20, 0, 255).point(lambda v: 255 if v > 150 else 0)).filter(ImageFilter.GaussianBlur(6))
    return over(im, _rgba((55, 6, 5), dark.point(lambda v: int(v * 0.7))))


def wall_peeling(lang, rng):
    w, h = 1024, 1024
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for _ in range(7):
        x, y = rng.uniform(150, w - 150), rng.uniform(150, h - 150)
        pts = []
        R = rng.uniform(70, 170)
        for k in range(16):
            a = 2 * math.pi * k / 16
            rr = R * rng.uniform(0.55, 1.15)
            pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr * 0.8))
        hole = Image.new("L", (w, h), 0)
        ImageDraw.Draw(hole).polygon(pts, fill=255)
        rim = hole.filter(ImageFilter.MaxFilter(15))
        im = over(im, _rgba((205, 200, 185), ImageChops.subtract(rim, hole).filter(ImageFilter.GaussianBlur(1))))   # край краски
        im = over(im, _rgba((120, 110, 95), hole.point(lambda v: int(v * 0.85))))   # под краской — штукатурка
        sh = hole.filter(ImageFilter.GaussianBlur(5)).point(lambda v: int(v * 0.35))
        im = over(im, _rgba((40, 35, 30), ImageChops.subtract(sh, hole.filter(ImageFilter.MinFilter(9)))))
    return _shade(im, rng, 180)


def wall_rust_streaks(lang, rng):
    w, h = 1024, 1024
    a = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(a)
    bolts = []
    for k in range(6):
        x, y = 100 + k * 165 + rng.uniform(-30, 30), rng.uniform(60, 200)
        bolts.append((x, y))
        L = rng.uniform(0.35, 0.8) * h
        for j in range(3):
            xx = x + rng.uniform(-14, 14)
            d.line([(xx + math.sin(t / 40) * 4, t) for t in range(int(y), int(y + L * rng.uniform(0.6, 1.0)), 15)], fill=rng.randint(140, 230), width=rng.randint(10, 26))
    a = a.filter(ImageFilter.GaussianBlur(9))
    fade = Image.linear_gradient("L").resize((w, h)).point(lambda v: 255 - int(v * 0.8))
    a = ImageChops.multiply(a, fade)
    im = _shade(_rgba((118, 52, 20), a.point(lambda v: min(255, int(v * 1.5)))), rng, 170)
    bm = Image.new("L", (w, h), 0)
    db = ImageDraw.Draw(bm)
    for x, y in bolts:
        db.ellipse((x - 16, y - 16, x + 16, y + 16), fill=255)
    return over(im, _rgba((70, 45, 30), bm))


# имя → (функция, ширина м, высота м, есть текст (два языка), вид: paper / paint / clock)
DECALS = {
    "poster_water": (poster_water, 0.5, 0.7, True, "paper"),
    "poster_gasmask": (poster_gasmask, 0.5, 0.7, True, "paper"),
    "poster_district_map": (poster_map, 0.8, 0.6, True, "paper"),
    "poster_duty": (poster_duty, 0.42, 0.54, True, "paper"),
    "poster_shelter_rules": (poster_list("rules", (60, 70, 60), None), 0.5, 0.7, True, "paper"),
    "poster_first_aid": (poster_list("aid", RED, "cross"), 0.5, 0.7, True, "paper"),
    "poster_ad_old": (poster_ad, 0.6, 0.85, True, "paper"),
    "poster_wanted": (poster_wanted, 0.42, 0.6, True, "paper"),
    "poster_iron_wheel": (poster_iron, 0.5, 0.7, True, "paper"),
    "poster_wellspring": (poster_well, 0.5, 0.7, True, "paper"),
    "paint_exit": (paint_exit, 1.2, 0.4, True, "paint"),
    "paint_keep_out": (paint_keep_out, 1.6, 0.66, True, "paint"),
    "paint_food": (paint_food, 1.3, 0.43, True, "paint"),
    "paint_infected": (paint_infected, 1.6, 0.56, True, "paint"),
    "paint_arrows": (paint_arrows, 1.4, 0.5, False, "paint"),
    "paint_room_number": (paint_room_number, 0.6, 0.4, False, "paint"),
    "graffiti_skull": (graffiti_skull, 0.9, 0.9, False, "paint"),
    "graffiti_alive": (graffiti_alive, 1.8, 0.9, True, "paint"),
    "graffiti_tag": (graffiti_tag, 1.6, 0.66, False, "paint"),
    "graffiti_smile": (graffiti_smile, 0.8, 0.8, False, "paint"),
    "graffiti_faction_signs": (graffiti_faction_signs, 1.8, 0.67, False, "paint"),
    "tally_days": (tally_days, 1.1, 0.3, False, "paint"),
    "kid_drawing": (kid_drawing, 0.42, 0.31, False, "paper"),
    "notes_nail": (notes_nail, 0.45, 0.45, True, "paper"),
    "calendar_crossed": (calendar_crossed, 0.36, 0.48, True, "paper"),
    "wallclock_stopped": (None, 0.32, 0.32, False, "clock"),
    "wall_crack": (wall_crack, 1.0, 1.0, False, "stain"),
    "wall_leak": (wall_leak, 1.2, 1.4, False, "stain"),
    "wall_mold": (wall_mold, 1.2, 1.2, False, "stain"),
    "wall_soot": (wall_soot, 1.2, 1.6, False, "stain"),
    "wall_bullets": (wall_bullets, 1.0, 0.75, False, "stain"),
    "wall_handprints": (wall_handprints, 0.9, 0.9, False, "stain"),
    "wall_blood": (wall_blood, 1.0, 1.0, False, "stain"),
    "wall_peeling": (wall_peeling, 1.2, 1.2, False, "stain"),
    "wall_rust_streaks": (wall_rust_streaks, 1.2, 1.2, False, "stain"),
}


def jobs(only):
    out = []
    for nm, (fn, w, h, txt, kind) in DECALS.items():
        if only and nm not in only and not any(o.startswith(nm + "_") for o in only):
            continue
        for lang in ((0, 1) if txt else (None,)):
            full = nm + ("_en" if lang == 0 else "_de" if lang == 1 else "")
            if only and nm not in only and full not in only:
                continue
            out.append((full, fn, w, h, lang, kind))
    return out


# ───────────────────────── модель (bpy) ─────────────────────────

def build_model(name, img_path, w, h, kind):
    import bpy
    import bmesh
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    img = bpy.data.images.load(img_path)
    img.pack()
    m = bpy.data.materials.new(name + "_mat")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 1.0
    b.inputs["Metallic"].default_value = 0.0
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    if kind == "stain":   # следы на стене: прозрачность плавная (подтёки, копоть сходят на нет)
        nt.links.new(tex.outputs["Alpha"], b.inputs["Alpha"])
        m.blend_method = "BLEND"
    elif kind != "clock":   # вырез по прозрачности (alpha clip): рваные края бумаги, краска без фона
        gt = nt.nodes.new("ShaderNodeMath")
        gt.operation = "GREATER_THAN"
        gt.inputs[1].default_value = 0.5
        nt.links.new(tex.outputs["Alpha"], gt.inputs[0])
        nt.links.new(gt.outputs[0], b.inputs["Alpha"])
        m.blend_method = "CLIP"
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new()
    off = {"paint": 0.003, "stain": 0.002}.get(kind, 0.006)
    if kind == "clock":
        side_m = bpy.data.materials.new("clock_rim")
        side_m.use_nodes = True
        side_m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.06, 0.05, 0.045, 1)
        side_m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
        n, r, dep = 24, w / 2, 0.045
        front, back, rim_f = [], [], []
        for k in range(n):
            a = 2 * math.pi * k / n
            x, z = math.cos(a) * r, math.sin(a) * r + r
            front.append(bm.verts.new((x * 0.86, -dep, z * 0.86 + r * 0.14)))
            rim_f.append(bm.verts.new((x, -dep, z)))
            back.append(bm.verts.new((x, 0, z)))
        f = bm.faces.new(front[::-1])
        f.material_index = 0
        for loop in f.loops:
            co = loop.vert.co
            loop[uv].uv = ((co.x / (r * 0.86) + 1) / 2, ((co.z - r) / (r * 0.86) + 1) / 2)
        for k in range(n):
            j = (k + 1) % n
            for q in ([rim_f[k], rim_f[j], front[j], front[k]], [back[k], back[j], rim_f[j], rim_f[k]]):
                ff = bm.faces.new(q)
                ff.material_index = 1
        bm_mats = [m, side_m]
    else:
        vs = [bm.verts.new(p) for p in ((-w / 2, -off, 0), (w / 2, -off, 0), (w / 2, -off, h), (-w / 2, -off, h))]
        f = bm.faces.new(vs)
        for loop, t in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
            loop[uv].uv = t
        bm_mats = [m]
    bm.normal_update()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for mm in bm_mats:
        me.materials.append(mm)
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    path = os.path.join(ROOT, "export", f"{name}_idle.glb")
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_apply=True, export_yup=True,
                              export_image_format="AUTO")
    return path


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    os.makedirs(TMP, exist_ok=True)
    made = []
    for full, fn, w, h, lang, kind in jobs(only):
        rng = random.Random(full)
        im = clock_face(rng) if kind == "clock" else fn(lang, rng)
        if kind == "stain":   # к краям картинки след сходит на нет — не видно прямых краёв
            bw = int(min(im.size) * 0.1)
            edge = Image.new("L", im.size, 0)
            ImageDraw.Draw(edge).rectangle((bw, bw, im.width - bw, im.height - bw), fill=255)
            edge = edge.filter(ImageFilter.GaussianBlur(bw * 0.6))
            im.putalpha(ImageChops.multiply(im.getchannel("A"), edge))
        px = 1024 if max(im.size) > 600 else 512
        if max(im.size) > px:
            k = px / max(im.size)
            im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        p = os.path.join(TMP, full + ".png")
        im.save(p)
        path = build_model(full, p, w, h, kind)
        print(f"{full}: {w:.2f} × {h:.2f} м, {os.path.getsize(path) // 1024} КБ")
        made.append((full, p))
    if made:   # лист: все картинки на тёмном фоне
        cell, cols = 300, 6
        rows = (len(made) + cols - 1) // cols
        sh = Image.new("RGB", (cols * cell, rows * (cell + 24)), (225, 222, 215))
        d = ImageDraw.Draw(sh)
        f = ImageFont.truetype("DejaVuSans-Bold.ttf", 13)
        for i, (nm, p) in enumerate(made):
            im = Image.open(p).convert("RGBA")
            im.thumbnail((cell - 16, cell - 16))
            x, y = (i % cols) * cell, (i // cols) * (cell + 24)
            bg = Image.new("RGBA", (cell, cell), (176, 170, 158, 255))   # «стена» — светлая штукатурка
            bg.alpha_composite(im, ((cell - im.width) // 2, (cell - im.height) // 2))
            sh.paste(bg.convert("RGB"), (x, y + 24))
            d.text((x + 6, y + 5), nm, font=f, fill=(40, 40, 40))
        out = os.path.join(ROOT, "renders", "_review", f"decals_{datetime.date.today().isoformat()}.jpg")
        sh.save(out, quality=88)
        print("лист:", out)


if __name__ == "__main__":
    main()
