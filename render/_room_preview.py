"""Комната-пример: оболочка + расставленные ОТДЕЛЬНЫЕ предметы (мебель в оболочку не впекается).
Делает:
  1) renders/_review/room_<имя>_lit.png — Blender, со светом (как должно выглядеть);
  2) layouts/<имя>.json — расстановка: для каждого предмета картинка, x_m (середина от левого края комнаты)
     и bottom_m (насколько низ картинки выше линии пола, м) — посчитано из 3D точно, игра ставит по ним.
Запуск: python3 render/_room_preview.py
"""
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "models"))
import _lib as L  # noqa: E402

import bpy  # noqa: E402

ROOT = L.ROOT
TAN = math.tan(math.radians(12))
NAME = "shelter_living_workshop"


def load(rel):
    spec = importlib.util.spec_from_file_location(rel.replace("/", "_"), os.path.join(ROOT, "models", rel + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def place(parts, name, loc, rot=None):
    obj = L.join(parts, name)
    L.transform([obj], loc, rot)
    return obj


def main():
    L.new_scene()
    room = load("room/shelter_living")
    X0, X1 = room.X0, room.X1
    objs = {}
    # оболочка, края, перекрытия
    shell = [place(room.shell_mid(), "shell", (0, 0, 0))]
    for sign in (-1, 1):
        parts, _ = room.side_wall(sign)
        shell.append(place(parts, f"edge{sign}", (X0 - 0.0 if sign < 0 else X1, 0, 0)))
    shell[-2].data.transform(__import__("mathutils").Matrix.Translation((0, 0, 0)))
    shell.append(place(room.slab(), "slab_top", (0, 0, room.H)))
    shell.append(place(room.slab(), "slab_bottom", (0, 0, -room.SLAB)))

    # предметы: (картинка, модуль, функция, x середины от левого края, y передней кромки, z низа, поворот)
    W = lambda s: s  # noqa: E731
    items = [
        ("locker_metal_armeyskiy_idle", "container/locker_metal", "locker_idle", 0.36, 2.47, 0.0),
        ("table_wood_pismennyy_idle", "furniture/table_wood_pismennyy", "desk_idle", 1.45, 2.32, 0.0),
        ("shelf_wood_derevyannaya_metal_ugolok_idle", "container/shelf_wood", "shelf_idle", 1.45, 2.76, 1.15),
        ("toolbox_metallicheskiy_idle", "container/toolbox", "toolbox_idle", 1.80, 2.50, 0.75),
        ("chair_wood_derevyannyy_idle", "furniture/chair_wood", "chair_idle", 1.15, 1.95, 0.0),
        ("crate_wood_voennyy_idle", "container/crate_wood", "crate_voennyy", 2.42, 2.50, 0.0),
        ("bed_single_derevyannaya_samodelnaya_idle", "furniture/bed_single", "bed_idle", 3.95, 1.95, 0.0),
        ("crate_wood_sredniy_idle", "container/crate_wood", "crate_sredniy", 2.55, 1.05, 0.0),
        ("lamp_ceiling_lyuminestsentnaya_idle", "machine/lamp_ceiling", "lamp_idle", 2.56, 0.55, 2.70),
    ]
    layout = {"room": "shelter_living", "shell": "shelter_living_concrete_normal", "width_m": room.SEG,
              "comment": "x_m — середина картинки от левого края комнаты; bottom_m — низ картинки над линией пола "
                         "(м, в игре ×100 px). Порядок — как рисовать: сзади вперёд, стоящее на предмете — после него.", "items": []}
    for img, mod, fn, xm, yf, zb in items:
        parts = getattr(load(mod), fn)()
        tmp = L.join(parts, img)
        pts = [v.co for v in tmp.data.vertices]
        cx = (min(p.x for p in pts) + max(p.x for p in pts)) / 2
        ymin = min(p.y for p in pts)
        zmin = min(p.z for p in pts)
        L.transform([tmp], (X0 + xm - cx, yf - ymin, zb - zmin))
        objs[img] = tmp
        bottom = min(v.co.z + v.co.y * TAN for v in tmp.data.vertices)
        id_, rest = img.split("_idle")[0], None
        layout["items"].append({"image": img, "x_m": round(xm, 3), "bottom_m": round(bottom, 3),
                                "depth_m": round(yf, 2)})
    # порядок рисования — как в списке выше (сзади вперёд; то, что стоит НА предмете, — после него)
    os.makedirs(os.path.join(ROOT, "layouts"), exist_ok=True)
    json.dump(layout, open(os.path.join(ROOT, "layouts", NAME + ".json"), "w"), ensure_ascii=False, indent=1)

    if "--no-render" in sys.argv:
        print("готово (без рендера): layouts/" + NAME + ".json")
        return
    # свет: лампа под потолком (тёплая), слабая подсветка, свечение лампы
    scene = bpy.context.scene
    lamp = objs["lamp_ceiling_lyuminestsentnaya_idle"]
    lx = X0 + 2.56
    for i, (x, e) in enumerate(((lx, 300.0), (X0 + 1.2, 45.0), (X0 + 4.0, 55.0))):
        ld = bpy.data.lights.new(f"room_light{i}", "POINT")
        ld.energy, ld.shadow_soft_size, ld.color = e, 0.25, (1.0, 0.70, 0.40)
        lo = bpy.data.objects.new(f"room_light{i}", ld)
        lo.location = (x, 0.9 if i == 0 else 1.8, 2.45 if i == 0 else 2.2)
        scene.collection.objects.link(lo)
    scene.world.color = (0.004, 0.005, 0.008)
    # холодный слабый свет снаружи — чтобы читались грани камня рамки
    ld = bpy.data.lights.new("outside", "AREA")
    ld.energy, ld.size, ld.color = 60.0, 6.0, (0.45, 0.55, 0.95)
    lo = bpy.data.objects.new("outside", ld)
    lo.location = (0, -4.0, 3.6)
    lo.rotation_euler = (math.radians(60), 0, 0)
    scene.collection.objects.link(lo)
    for mat in bpy.data.materials:
        if mat.node_tree:
            for n in mat.node_tree.nodes:
                if n.type == "EMISSION" and mat.name != L.rt.NORMAL_MAT_NAME:
                    n.inputs["Strength"].default_value = 3.0
    c = scene.cycles
    c.samples, c.max_bounces = 128, 4
    try:
        c.use_denoising, c.denoiser = True, "OPENIMAGEDENOISE"
    except Exception:
        c.use_denoising = False
    frame = [(X0 - 0.5, 0, -0.35), (X1 + 0.5, 0, -0.35), (X0 - 0.5, 0, 4.0), (X1 + 0.5, 0, 4.0)]
    L.rt.frame_objects(list(objs.values()) + shell, 0, frame)
    scene.view_settings.view_transform = "AgX"
    scene.render.film_transparent = True
    out = os.path.join(ROOT, "renders", "_review", f"room_{NAME}_lit.png")
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    from PIL import Image
    im = Image.open(out).convert("RGBA")
    bg = Image.new("RGBA", im.size, (14, 15, 20, 255))
    bg.alpha_composite(im)
    bg.convert("RGB").save(out)
    print("готово:", scene.render.filepath, "и layouts/" + NAME + ".json")


if __name__ == "__main__":
    main()
