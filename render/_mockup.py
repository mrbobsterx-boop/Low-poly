"""Сборка комнаты из отдельных картинок — так, как это будет делать игра (для проверки глазами).
Запуск: python3 render/_mockup.py layouts/<файл>.json <выход.png> [--person X_M]
Порядок рисования: оболочка (сегмент повторяется) → края → предметы (back → mid → front) → перекрытия.
Висящее под потолком (row = ceiling) — верх картинки на линии потолка 300 см (под перекрытием).
Результат — в масштабе игры (100 px на метр) и со светом «примерно» (по карте нормалей), чтобы видеть объём.
"""
import json
import math
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _preview as P  # noqa: E402

ROOT = P.ROOT
PX = 200                                   # рендер: px на метр
TAN = math.tan(math.radians(12))
ROW_DEPTH = {"front": 0.5, "mid": 1.5, "back": 2.5}
EDGE = 0.5


def img(cat, name, lit=True):
    path = os.path.join(ROOT, "renders", cat, name + ".png")
    col, l = P.lit(path)
    return l if lit else col


def find(name):
    for cat in os.listdir(os.path.join(ROOT, "renders")):
        if os.path.exists(os.path.join(ROOT, "renders", cat, name + ".png")):
            return cat
    raise FileNotFoundError(name)


def main(layout_path, out, person_x=None, lit=True):
    lay = json.load(open(os.path.join(ROOT, layout_path)))
    width = lay["width_m"]
    W = int((width + 2 * EDGE) * PX)
    floor_y = int(5.0 * PX)               # линия пола (передний край) от верха холста: сверху 4 м + снизу 1 м
    H = floor_y + 1 * PX
    canvas = Image.new("RGBA", (W, H), (20, 20, 22, 255))

    shell = lay["shell"]
    mid = img("room", shell + "_mid", lit)
    x = int(EDGE * PX)
    while x < int((EDGE + width) * PX):
        canvas.alpha_composite(mid.crop((0, 0, min(mid.width, int((EDGE + width) * PX) - x), mid.height)),
                               (x, floor_y - mid.height))
        x += mid.width
    canvas.alpha_composite(img("room", shell + "_left", lit), (0, floor_y - mid.height))
    canvas.alpha_composite(img("room", shell + "_right", lit), (int((EDGE + width) * PX), floor_y - mid.height))

    order = {"back": 0, "mid": 1, "front": 2, "ceiling": 3}
    items = sorted(lay["items"], key=lambda it: order[it["row"]])
    if person_x is not None:
        items.insert(sum(1 for it in items if it["row"] in ("back", "mid")),
                     {"id": "survivor_base", "anim": "idle", "x_m": person_x, "row": "front"})
    for it in items:
        if it.get("anim"):
            sheet = img("character", f"{it['id']}_{it['anim']}", lit)
            im = sheet.crop((0, 0, 240, 400))
            dy = -int(0.03 * PX)          # линия земли персонажа — 3 см выше низа кадра
        else:
            name = f"{it['id']}_{it['variation']}_{it['state']}"
            im = img(find(name), name, lit)
            dy = 0
        cx = int((EDGE + it["x_m"]) * PX)
        if it["row"] == "ceiling":
            top = floor_y - int(3.0 * PX)
            canvas.alpha_composite(im, (cx - im.width // 2, top))
        else:
            bottom = floor_y - int(ROW_DEPTH[it["row"]] * TAN * PX) - dy
            canvas.alpha_composite(im, (cx - im.width // 2, bottom - im.height))

    slab = img("room", "slab_bunker_concrete_normal", lit)
    for y in (floor_y - int(4.0 * PX), floor_y):          # перекрытие сверху (300–400 см) и снизу (пол этажа)
        x = 0
        while x < W:
            canvas.alpha_composite(slab.crop((0, 0, min(slab.width, W - x), slab.height)), (x, y))
            x += slab.width
    canvas = canvas.resize((W // 2, H // 2), Image.LANCZOS)   # масштаб игры
    canvas.convert("RGB").save(out)
    print("макет:", out, canvas.size)


if __name__ == "__main__":
    args = sys.argv[1:]
    px = None
    if "--person" in args:
        i = args.index("--person")
        px = float(args[i + 1])
        del args[i:i + 2]
    flat = "--flat" in args
    args = [a for a in args if a != "--flat"]
    main(args[0], args[1], px, lit=not flat)
