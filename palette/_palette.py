"""Собирает общую палитру: palette/palette.png (текстура для моделей) и palette/palette_preview.png (для автора).
Запуск: python3 palette/_palette.py. Цвета меняются только здесь, потом — пересобрать.
Сетка 8 × 4 квадрата по 32 px. Квадрат (столбец c, строка r) — UV-центр: u = (c + 0,5) / 8, v = 1 − (r + 0,5) / 4.
"""
import os
from PIL import Image, ImageDraw, ImageFont

CELL = 32
COLS, ROWS = 8, 4
# (имя, hex, для чего). Строка 0 — бетон/камень, 1 — металл, 2 — дерево/ткань/хаки, 3 — живое и свет.
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
]

HERE = os.path.dirname(os.path.abspath(__file__))


def hex2rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def build_texture():
    im = Image.new("RGB", (COLS * CELL, ROWS * CELL))
    d = ImageDraw.Draw(im)
    for r, row in enumerate(COLORS):
        for c, (_, hx, _) in enumerate(row):
            d.rectangle([c * CELL, r * CELL, (c + 1) * CELL - 1, (r + 1) * CELL - 1], fill=hex2rgb(hx))
    im.save(os.path.join(HERE, "palette.png"))


def build_preview():
    W, H, PAD = 190, 150, 10
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 13)
        bold = ImageFont.truetype("DejaVuSans-Bold.ttf", 14)
    except OSError:
        font = bold = ImageFont.load_default()
    rows_title = ["Бетон и камень", "Металл", "Дерево, хаки, ткань", "Живое и свет"]
    im = Image.new("RGB", (COLS * W + PAD, ROWS * (H + 24) + PAD), (235, 232, 226))
    d = ImageDraw.Draw(im)
    for r, row in enumerate(COLORS):
        y0 = r * (H + 24) + PAD
        d.text((PAD, y0), f"Строка {r + 1}: {rows_title[r]}", font=bold, fill=(30, 30, 30))
        for c, (name, hx, use) in enumerate(row):
            x0, y1 = c * W + PAD, y0 + 20
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
             "Общая палитра всех моделей: `palette.png` — 8 × 4 квадрата по 32 px. Собирается скриптом `_palette.py`",
             "(цвета меняются только там). Превью для глаз — `palette_preview.png`.", "",
             "**Статус: черновик, ждёт утверждения автора.**", "",
             "- Цвета — «чистые» (правило 10): без света и тени. Темнее/светлее делает Godot своим светом.",
             "- Износ, грязь, ржавые пятна — отдельной гранью другого цвета палитры, не текстурой.",
             "- Строка 4, квадраты 6–8 — **светящееся** (материал emission): лампа, огонь, экран.",
             "- В модели UV грани ставится в центр нужного квадрата: u = (столбец − 0,5) / 8, v = 1 − (строка − 0,5) / 4.",
             "  Текстура без сглаживания (Closest), поэтому цвета не смешиваются.", "",
             "| № (строка.столбец) | Имя | Цвет | Для чего |", "|---|---|---|---|"]
    for r, row in enumerate(COLORS):
        for c, (name, hx, use) in enumerate(row):
            lines.append(f"| {r + 1}.{c + 1} | `{name}` | `{hx}` | {use} |")
    open(os.path.join(HERE, "palette.md"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    build_texture()
    build_preview()
    build_md()
    print("palette.png, palette_preview.png, palette.md — готово")
