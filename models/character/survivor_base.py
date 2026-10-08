"""Выживший `survivor_base` (шаблон человека). ОС: 100 × 180 см. Смотрит ВПРАВО (+X).
Кадры анимации — лист в строку (docs/IMAGES.md, раздел 5), кадр 120 × 200 см (240 × 400 px):
  renders/character/survivor_base_idle.png  (4 кадра) + _n.png
  renders/character/survivor_base_walk.png  (8 кадров) + _n.png
Человек стоит серединой на глубине 0: линия земли — на 3 см (6 px) выше низа кадра, носки ботинок не обрезаются.
Скелета пока нет (для пути А не нужен): части тела поворачиваются в суставах прямо в скрипте.
Для пути Б будет общий скелет `_rig_human` — потом.
Запуск: python3 models/character/survivor_base.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402  (загружает bpy)

import bpy  # noqa: E402
from mathutils import Matrix  # noqa: E402

FRAME_W, FRAME_H, GROUND = 1.20, 2.00, 0.03
# кадр: точки на глубине −GROUND/tan12, чтобы низ кадра был на 3 см ниже земли под серединой человека
_Y = -GROUND / math.tan(math.radians(12))
FRAME = [(-FRAME_W / 2, _Y, 0), (FRAME_W / 2, _Y, 0), (-FRAME_W / 2, _Y, FRAME_H), (FRAME_W / 2, _Y, FRAME_H)]

# Пропорции (м), рост 1,80
FOOT_Z, SHIN, THIGH = 0.08, 0.42, 0.42
HIP_Z = FOOT_Z + SHIN + THIGH            # 0,92
TORSO, NECK, HEAD = 0.50, 0.06, 0.24
UPPER, FORE, HAND = 0.29, 0.26, 0.09
HIP_Y, SHOULDER_Y = 0.10, 0.20           # от середины — вбок (по глубине)
TURN = 20                                # доворот к камере, градусы (чтобы читалась фигура)

SKIN, HAIR = "skin_mid", "wood_dark"
JACKET, JACKET2, PANTS, BOOTS = "khaki", "olive_dark", "steel_dark", "stone_dark"


def ry(deg):
    """Поворот в суставе: + — вперёд (к +X)."""
    return Matrix.Rotation(math.radians(-deg), 4, "Y")


def limb(parts, m, length, thick, color, depth=None):
    """Кусок, висящий вниз от сустава (матрица m), длиной length."""
    o = L.box((thick, depth or thick, length), (0, 0, -length), color)
    o.data.transform(m)
    parts.append(o)


def leg(parts, root, hip, knee, ankle=0.0):
    m = root @ ry(hip)
    limb(parts, m, THIGH, 0.15, PANTS, 0.14)
    m = m @ Matrix.Translation((0, 0, -THIGH)) @ ry(-knee)
    limb(parts, m, SHIN, 0.12, PANTS, 0.12)
    m = m @ Matrix.Translation((0, 0, -SHIN)) @ ry(ankle)
    boot = L.box((0.27, 0.11, FOOT_Z + 0.04), (0.05, 0, -FOOT_Z), BOOTS)
    boot.data.transform(m)
    parts.append(boot)
    return m


def arm(parts, root, shoulder, elbow):
    m = root @ ry(shoulder)
    limb(parts, m, UPPER, 0.11, JACKET, 0.11)
    m = m @ Matrix.Translation((0, 0, -UPPER)) @ ry(elbow)
    limb(parts, m, FORE, 0.09, JACKET, 0.09)
    m = m @ Matrix.Translation((0, 0, -FORE))
    limb(parts, m, HAND, 0.07, SKIN, 0.08)


def body(pose):
    """pose: hip_l/r, knee_l/r, sh_l/r, el_l/r, lean, bob — градусы/метры. Возвращает список кусков."""
    p = []
    base = Matrix.Rotation(math.radians(-TURN), 4, "Z")          # доворот к камере
    hip = base @ Matrix.Translation((0, 0, HIP_Z + pose.get("bob", 0)))
    # ноги: дальняя (+Y, левая) и ближняя (−Y, правая)
    leg(p, hip @ Matrix.Translation((0, HIP_Y, 0)), pose["hip_l"], pose["knee_l"])
    leg(p, hip @ Matrix.Translation((0, -HIP_Y, 0)), pose["hip_r"], pose["knee_r"])
    # таз и корпус (с наклоном)
    pel = L.box((0.22, 0.34, 0.16), (0, 0, -0.08), PANTS)
    pel.data.transform(hip)
    p.append(pel)
    chest = hip @ ry(pose.get("lean", 0))
    jacket = L.box((0.25, 0.40, TORSO), (0, 0, 0.0), JACKET)
    jacket.data.transform(chest)
    p.append(jacket)
    belt = L.box((0.26, 0.41, 0.05), (0, 0, 0.0), JACKET2)
    belt.data.transform(chest)
    p.append(belt)
    pocket = L.box((0.03, 0.12, 0.10), (0.13, -0.10, 0.22), JACKET2)
    pocket.data.transform(chest)
    p.append(pocket)
    collar = L.box((0.18, 0.26, 0.05), (0, 0, TORSO), JACKET2)
    collar.data.transform(chest)
    p.append(collar)
    # шея, голова, волосы, нос
    neck = chest @ Matrix.Translation((0.01, 0, TORSO))
    p.append(_t(L.box((0.10, 0.10, NECK + 0.02), (0, 0, 0), SKIN), neck))
    head = neck @ Matrix.Translation((0.02, 0, NECK))
    p.append(_t(L.box((0.21, 0.19, HEAD), (0, 0, 0), SKIN, bevel=0.03), head))
    p.append(_t(L.box((0.20, 0.20, 0.07), (-0.02, 0, HEAD - 0.05), HAIR, bevel=0.025), head))     # макушка
    p.append(_t(L.box((0.07, 0.20, 0.16), (-0.08, 0, HEAD - 0.17), HAIR, bevel=0.02), head))      # затылок
    p.append(_t(L.box((0.04, 0.035, 0.05), (0.115, 0, 0.09), SKIN, bevel=0.01), head))            # нос
    p.append(_t(L.box((0.01, 0.025, 0.02), (0.105, -0.05, 0.13), "soot", bevel=0), head))          # глаз
    # руки: дальняя рисуется за корпусом, ближняя — перед ним
    sh = chest @ Matrix.Translation((0, 0, TORSO - 0.06))
    arm(p, sh @ Matrix.Translation((0, SHOULDER_Y, 0)), pose["sh_l"], pose["el_l"])
    arm(p, sh @ Matrix.Translation((0, -SHOULDER_Y, 0)), pose["sh_r"], pose["el_r"])
    return p


def _t(o, m):
    o.data.transform(m)
    return o


def ground(parts):
    """Опустить/поднять фигуру, чтобы нижняя точка стояла на земле (z = 0)."""
    zmin = min((o.matrix_world @ v.co).z for o in parts for v in o.data.vertices)
    for o in parts:
        o.data.transform(Matrix.Translation((0, 0, -zmin)))


def walk_pose(i, n=8):
    t = 2 * math.pi * i / n
    s = math.sin(t)
    return {
        "hip_r": 26 * s, "hip_l": -26 * s,
        "knee_r": 8 + 26 * max(0.0, -math.cos(t - 0.6)) * (1 if s < 0.3 else 0.4),
        "knee_l": 8 + 26 * max(0.0, math.cos(t - 0.6)) * (1 if -s < 0.3 else 0.4),
        "sh_r": -22 * s, "sh_l": 22 * s, "el_r": 18 + 8 * max(0, s), "el_l": 18 + 8 * max(0, -s),
        "lean": 4,
    }


def idle_pose(i, n=4):
    b = math.sin(2 * math.pi * i / n)
    return {"hip_r": 3, "hip_l": -3, "knee_r": 4, "knee_l": 4, "sh_r": 4 + 2 * b, "sh_l": -3 - 2 * b,
            "el_r": 10 + 2 * b, "el_l": 8 + 2 * b, "lean": 1 + b, "bob": 0.006 * b}


def strip(name, frames):
    """Склеить кадры в лист: renders/character/<name>.png и _n.png."""
    from PIL import Image
    for suffix in ("", "_n"):
        ims = [Image.open(os.path.join(L.ROOT, f + suffix + ".png")) for f in frames]
        w, h = ims[0].size
        sheet = Image.new("RGBA", (w * len(ims), h))
        for k, im in enumerate(ims):
            sheet.paste(im, (k * w, 0))
        sheet.save(os.path.join(L.ROOT, "renders", "character", name + suffix + ".png"))
    for f in frames:
        for suffix in ("", "_n"):
            os.remove(os.path.join(L.ROOT, f + suffix + ".png"))
    print(f"[{name}] {len(frames)} кадров, лист {w * len(frames)} × {h} px")


def render_anim(name, pose_fn, n):
    frames = []
    for i in range(n):
        parts = body(pose_fn(i, n))
        ground(parts)
        obj = L.join(parts, f"{name}_{i}")
        if i == 0:
            print(f"  треугольников {L.tris(obj)} / лимит {L.TRI_LIMITS['human']}, рост {L.dims(obj)[0][2] * 100:.0f} см")
        f = f"renders/character/_tmp_{name}_{i}"
        L.rt.render_pair([obj], f, frame_points=FRAME)
        frames.append(f)
        if i == 0 and name.endswith("idle"):
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            bpy.ops.export_scene.gltf(filepath=os.path.join(L.ROOT, "export", "survivor_base_default_idle.glb"),
                                      export_format="GLB", use_selection=True, export_apply=True)
            obj.name = "survivor_base_idle_pose"
            L._saved.append(obj)
            obj.hide_render = True
        else:
            bpy.data.objects.remove(obj)
    strip(name, frames)


if __name__ == "__main__":
    L.new_scene()
    os.makedirs(os.path.join(L.ROOT, "renders", "character"), exist_ok=True)
    render_anim("survivor_base_idle", idle_pose, 4)
    render_anim("survivor_base_walk", walk_pose, 8)
    L.save_blend("character", "survivor_base")
