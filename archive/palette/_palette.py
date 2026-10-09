"""Собирает общую палитру: palette/palette.png (текстура для моделей) и palette/palette_preview.png (для автора).
Запуск: python3 palette/_palette.py. Цвета меняются только здесь, потом — пересобрать.
Сетка 8 × N квадратов по 32 px. В скриптах моделей цвет берётся ПО ИМЕНИ: uv("rust") — так палитру можно
расширять и переставлять, а модели после пересборки сами найдут свои цвета.
Каждый квадрат — три полосы: слева чуть темнее (−8 %), посередине сам цвет, справа чуть светлее (+8 %).
uv(name, shade=-1/0/+1) — для лёгкого разнобоя оттенков на соседних гранях (только цвета палитры).
"""
import os
from PIL import Image, ImageDraw, ImageFont

CELL = 32
COLS = 8
# (имя, hex, для чего). Строки: бетон/камень, металл, дерево/ткань/хаки, живое и свет, разное.
# Имя не менять, если цвет уже используется в моделях (иначе поправить скрипты); пустое место — None.
COLORS = [
    [("concrete_light", "#9b958b", "бетон светлый, сколы"),
     ("concrete", "#7a756c", "бетон — стены, полы"),
     ("concrete_dark", "#56524c", "бетон тёмный, перекрытия"),
     ("stone_dark", "#3d3a36", "тёмный камень, резина, шины"),
     ("soot", "#242220", "сажа, чёрный пластик, провода"),
     ("offwhite", "#d6cfbf", "эмаль, бумага, кафель, бинт"),
     ("brick", "#8c4934", "кирпич"),
     ("dirt", "#6a5040", "земля, глина, пятна грязи")],
    [("steel_light", "#90969a", "светлый металл, хром, лезвия"),
     ("steel", "#6a7074", "металл — шкафчики, трубы"),
     ("steel_dark", "#454a4e", "тёмный металл, чугун, буржуйка"),
     ("rust_light", "#a6653b", "светлая ржавчина, медь"),
     ("rust", "#7d4527", "ржавчина"),
     ("rust_dark", "#4e2c1c", "тёмная ржавчина"),
     ("paint_blue", "#4b6a80", "крашеный металл — синий, вода"),
     ("paint_red", "#983a30", "крашеный — красный, огнетушитель, крест")],
    [("wood_light", "#a87e52", "светлое дерево, доски, ящики"),
     ("wood", "#7c5a3a", "дерево — мебель"),
     ("wood_dark", "#543b27", "тёмное дерево, старая мебель"),
     ("khaki_light", "#8b8a5c", "хаки светлый, брезент"),
     ("khaki", "#66683f", "хаки — военное, ящики, одежда"),
     ("olive_dark", "#44462c", "тёмная олива, тени складок формой"),
     ("cloth_beige", "#b7a686", "ткань светлая, мешковина, матрас"),
     ("cloth_red", "#8b3f3a", "ткань красная, одеяло")],
    [("plant", "#5c7a3a", "зелень, листья"),
     ("plant_dark", "#3b5128", "тёмная зелень, хвоя"),
     ("skin_light", "#d1a183", "кожа светлая"),
     ("skin_mid", "#a77555", "кожа средняя"),
     ("skin_dark", "#6d4a35", "кожа тёмная, волосы"),
     ("glow_lamp", "#ffd88a", "СВЕТИТСЯ: лампа (emission)"),
     ("glow_fire", "#ff8a2a", "СВЕТИТСЯ: огонь, угли (emission)"),
     ("glow_screen", "#8ef0a0", "СВЕТИТСЯ: экран, индикатор (emission)")],
    [("hazard_yellow", "#d6a227", "жёлтый — полосы опасности, знаки"),
     ("army_green", "#4b5d36", "армейский зелёный — шкафчики, ящики"),
     ("glass", "#9db3b5", "стекло (непрозрачный цвет; блики — Godot)"),
     ("blood", "#6b1d1c", "кровь"),
     ("hair_blond", "#c6a463", "волосы светлые"),
     ("hair_grey", "#a8a49c", "волосы седые"),
     ("plastic_white", "#e4e2db", "белый пластик, фаянс"),
     ("cloth_blue", "#3d4870", "ткань тёмно-синяя — одеяло, роба")],
    [("concrete_warm", "#5a4e43", "тёплый тёмный бетон — стены бункера"),
     ("glow_grow", "#c070ff", "СВЕТИТСЯ: фитолампа (фиолетовая, emission)"),
     None, None, None, None, None, None],
]
ROWS = len(COLORS)

HERE = os.path.dirname(os.path.abspath(__file__))


def _cells():
    for r, row in enumerate(COLORS):
        for c, cell in enumerate(row):
            if cell:
                yield r, c, cell


SHADE = 0.08                        # ±8 % яркости у боковых полос квадрата
STRIPS = ((0, 10), (10, 22), (22, 32))   # полосы квадрата (px): темнее, сам цвет, светлее


def uv(name, shade=0):
    """UV центра полосы квадрата цвета по имени; shade: −1 темнее, 0 сам цвет, +1 светлее."""
    for r, c, (n, _, _) in _cells():
        if n == name:
            a, b = STRIPS[shade + 1]
            return ((c * CELL + (a + b) / 2) / (COLS * CELL), 1.0 - (r + 0.5) / ROWS)
    raise KeyError(f"Нет цвета «{name}» в палитре (palette/palette.md)")


def name_at(u, v):
    """Обратно: (имя цвета, оттенок) по UV."""
    c, r = int(u * COLS), int((1.0 - v) * ROWS)
    px = u * COLS * CELL - c * CELL
    shade = -1 if px < STRIPS[0][1] else (0 if px < STRIPS[1][1] else 1)
    for rr, cc, (n, _, _) in _cells():
        if rr == r and cc == c:
            return n, shade
    return None, 0


def hex2rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def build_texture():
    # Пустые места — нейтральный серый (запас под новые цвета)
    im = Image.new("RGB", (COLS * CELL, ROWS * CELL), (128, 128, 128))
    d = ImageDraw.Draw(im)
    for r, c, (_, hx, _) in _cells():
        base = hex2rgb(hx)
        for k, (a, b) in zip((-1, 0, 1), STRIPS):
            col = tuple(max(0, min(255, round(ch * (1 + k * SHADE)))) for ch in base)
            d.rectangle([c * CELL + a, r * CELL, c * CELL + b - 1, (r + 1) * CELL - 1], fill=col)
    im.save(os.path.join(HERE, "palette.png"))


def build_preview():
    W, H, PAD = 190, 150, 10
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 13)
        bold = ImageFont.truetype("DejaVuSans-Bold.ttf", 14)
    except OSError:
        font = bold = ImageFont.load_default()
    rows_title = ["Бетон и камень", "Металл", "Дерево, хаки, ткань", "Живое и свет", "Разное", "Бетон бункера"]
    im = Image.new("RGB", (COLS * W + PAD, ROWS * (H + 24) + PAD), (235, 232, 226))
    d = ImageDraw.Draw(im)
    for r, row in enumerate(COLORS):
        y0 = r * (H + 24) + PAD
        d.text((PAD, y0), f"Строка {r + 1}: {rows_title[r]}", font=bold, fill=(30, 30, 30))
        for c, cell in enumerate(row):
            x0, y1 = c * W + PAD, y0 + 20
            if cell is None:
                d.rectangle([x0, y1, x0 + W - PAD, y1 + 80], outline=(150, 150, 150))
                d.text((x0 + 8, y1 + 32), "запас", font=font, fill=(130, 130, 130))
                continue
            name, hx, use = cell
            d.rectangle([x0, y1, x0 + W - PAD, y1 + 80], fill=hex2rgb(hx))
            d.text((x0, y1 + 84), f"{r + 1}.{c + 1} {name}", font=bold, fill=(30, 30, 30))
            d.text((x0, y1 + 101), hx, font=font, fill=(70, 70, 70))
            words, line, yy = use.split(), "", y1 + 116
            for w in words:
                if len(line + " " + w) > 22:
                    d.text((x0, yy), line, font=font, fill=(70, 70, 70)); yy += 15; line = w
                else:
                    line = (line + " " + w).strip()
            d.text((x0, yy), line, font=font, fill=(70, 70, 70))
    im.save(os.path.join(HERE, "palette_preview.png"))


def build_md():
    lines = ["# Палитра", "",
             "Общая палитра всех моделей: `palette.png` — 8 × 6 квадратов по 32 px. Собирается скриптом `_palette.py`",
             "(цвета меняются только там). Превью для глаз — `palette_preview.png`.", "",
             "**Статус: утверждена автором 2026-10-08** (строки 1–4; строка 5 добавлена по его списку).", "",
             "- Цвета — «чистые» (правило 10): без света и тени. Темнее/светлее делает Godot своим светом.",
             "- Износ, грязь, ржавые пятна — отдельной гранью другого цвета палитры, не текстурой.",
             "- Строка 4, квадраты 6–8 — **светящееся** (материал emission): лампа, огонь, экран.",
             "- **В скриптах моделей цвет — только по имени**: `uv(\"rust\")` из `_palette.py` (центр квадрата).",
             "  Палитру можно расширять и переставлять — модели после пересборки найдут свои цвета сами.",
             "- Пустое место (серое) — запас под новый цвет. Имя цвета, который уже есть в моделях, не менять.",
             "- Каждый квадрат — 3 полосы: темнее (−8 %), сам цвет, светлее (+8 %) — лёгкий разнобой соседних граней.",
             "  Текстура без сглаживания (Closest), поэтому цвета не смешиваются.", "",
             "| № (строка.столбец) | Имя | Цвет | Для чего |", "|---|---|---|---|"]
    for r, c, (name, hx, use) in _cells():
        lines.append(f"| {r + 1}.{c + 1} | `{name}` | `{hx}` | {use} |")
    open(os.path.join(HERE, "palette.md"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    build_texture()
    build_preview()
    build_md()
    print("palette.png, palette_preview.png, palette.md — готово")
