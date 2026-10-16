"""Задний план (фон за улицей) по биомам: вещи с тремя уровнями подробности, ленты дальнего рельефа, птицы.

    python3 tools/make_backdrop.py [биом …] [--only id …] [--no-preview]

Вещи — по возможности из готовых моделей Tripo (export/<имя>_idle.glb): тот же стиль, что у всей игры; кодом —
только то, чего в Tripo нет (кактусы, стог, кочки, мостки, ЛЭП, труба, цистерны — запросы для Tripo на замену в
docs/TRIPO_OBJECTS.md, раздел 12). Для каждой вещи:
    export/backdrop/bg_<биом>_<вид>_<n>_lod0.glb — близко (до −12 м): до 1 500 треугольников (дом — до 3 000), текстуры 512;
    …_lod1.glb — −12…−20 м: до 500, текстуры 256;
    …_lod2.glb — дальше −20 м: до 150, без текстур — цвет вершин.
Узлы: body; sway — что качается от ветра (кроны, кусты, камыш); пустые smoke_<n> — выход трубы (дым делает игра);
материал window_lit — окна (ночью игра включает свечение). Ленты рельефа: bg_<биом>_ridge_<n>_idle.glb (40 м,
края совпадают). Птицы: bg_bird_<вид>_idle.glb с анимацией bird_flap. Всё — в export/backdrop/backdrop.json.
Листы: renders/_review/backdrop_<биом>.png (вещи и три уровня), backdrop_scene_<биом>.png (сцена-проба).
"""
import json
import math
import os
import random
import sys

import bpy
import bmesh  # noqa: E402 — после bpy
import numpy as np
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import open_decor as D  # noqa: E402
import tripo_process as T  # noqa: E402

OUT = os.path.join(ROOT, "export", "backdrop")
LOD_TRIS = (1500, 500, 150)
LOD_TRIS_BIG = (3000, 500, 150)
LOD_TEX = (512, 256, 0)

# ───────────────────────── список вещей ─────────────────────────
# Нужен пакет opencv-python-headless (контуры силуэтов дальнего уровня).
# src: имя модели export/<src>_idle.glb или "code:<функция>"; h — высота (м) или None — как есть; sx — растянуть по
# ширине; tint — оттенок (умножить цвет); snow — снег сверху; sway/smoke/win — жизнь; dens — штук на 10 м²;
# near — ближе этой глубины (м, вглубь от улицы) не ставить; rot — можно поворачивать вокруг вертикали.


def I(kind, src, h=None, **kw):
    d = {"kind": kind, "src": src, "h": h, "sx": 1.0, "tint": None, "snow": False, "sway": False, "smoke": False,
         "win": False, "dens": 0.3, "near": 1.0, "rot": True, "big": False}
    d.update(kw)
    d.setdefault("card", kind in ("dead", "bush_dry", "crane", "pine", "leaf", "birch", "bush", "reeds", "fern"))
    return d


GREEN = "green"   # sway: что качается — зелень (по цвету) выше ствола
ITEMS = {
    "forest": [
        I("pine", "plant_tree_sosna", 6.0, sway=GREEN, dens=0.45, near=2.3),
        I("pine", "plant_tree_sosna", 8.0, sx=0.85, tint=(0.85, 0.95, 0.85), sway=GREEN, dens=0.35, near=2.3),
        I("pine", "plant_tree_sosna", 4.5, sx=1.15, tint=(0.95, 1.0, 0.85), sway=GREEN, dens=0.3, near=2.3),
        I("pine", "plant_tree_sosna", 7.0, tint=(0.75, 0.85, 0.8), sway=GREEN, dens=0.3, near=2.3),
        I("leaf", "tree_oak", 6.5, sway=GREEN, dens=0.25, near=2.3),
        I("leaf", "tree_maple", 6.0, sway=GREEN, dens=0.25, near=2.3),
        I("leaf", "tree_oak", 5.0, sx=1.2, tint=(1.0, 0.95, 0.75), sway=GREEN, dens=0.2, near=2.3),
        I("leaf", "tree_maple", 7.5, sx=0.9, tint=(0.85, 0.95, 0.85), sway=GREEN, dens=0.2, near=2.3),
        I("birch", "tree_birch", 7.0, sway=GREEN, dens=0.25, near=2.3),
        I("birch", "tree_birch", 5.5, sx=0.9, sway=GREEN, dens=0.2, near=2.3),
        I("bush", "bush_berry_malina", 1.3, sx=1.3, sway=GREEN, dens=0.5),
        I("bush", "bush_willow", 1.6, sway="all", dens=0.4),
        I("fern", "fern", 0.8, sx=1.4, sway="all", dens=0.5),
        I("log", "log_fallen", None, dens=0.15),
        I("stump", "tree_dead_stump", 1.4, dens=0.15),
        I("rock", "rock_boulder", 1.1, sx=1.2, tint=(0.8, 0.95, 0.75), dens=0.2),
    ],
    "field": [
        I("leaf", "tree_oak", 7.0, sway=GREEN, dens=0.08, near=2.3),
        I("leaf", "tree_maple", 6.5, sway=GREEN, dens=0.06, near=2.3),
        I("bush", "bush_berry_malina", 1.3, sx=1.4, sway=GREEN, dens=0.3),
        I("bush", "bush_willow", 1.5, sway="all", dens=0.25),
        I("haystack", "code:haystack", None, dens=0.08, near=3.0),
        I("fence", "ext_fence_wood", 1.3, dens=0.1, rot=False),
        I("pole", "code:pole_wires", None, dens=0.06, near=1.8, rot=False),
        I("barn", "farm_barn", 7.5, dens=0.02, near=10.8, big=True),
    ],
    "desert": [
        I("cactus", "code:cactus1", None, dens=0.1),
        I("cactus", "code:cactus2", None, dens=0.08),
        I("cactus", "code:cactus3", None, dens=0.08),
        I("cactus", "code:cactus4", None, dens=0.06),
        I("rock", "rock_boulder", 1.4, sx=1.5, tint=(1.15, 0.95, 0.7), dens=0.15),
        I("rock", "rock_boulder", 3.0, sx=1.8, tint=(1.1, 0.85, 0.65), dens=0.06, near=6.0),
        I("bush_dry", "tree_dead_bare", 1.6, sx=1.6, tint=(1.1, 0.95, 0.75), sway="all", dens=0.15),
        I("bones", "bones_pile", None, dens=0.05),
        I("sign", "decor_sign_weathered", 3.0, dens=0.02, rot=False, near=4.0),
    ],
    "swamp": [
        I("reeds", "bush_water_reeds", 1.5, sx=1.5, sway="all", dens=0.6),
        I("reeds", "bush_water_sedge", 1.0, sx=1.5, sway="all", dens=0.5),
        I("dead", "tree_dead_bare", 4.5, tint=(0.8, 0.85, 0.75), dens=0.15, near=1.8),
        I("dead", "tree_dead_bare_b", 5.0, tint=(0.8, 0.85, 0.75), dens=0.12, near=1.8),
        I("dead", "tree_dead_burnt", 4.0, dens=0.1, near=1.8),
        I("hummock", "code:hummock", None, dens=0.4, sway="top"),
        I("boardwalk", "code:boardwalk", None, dens=0.03, rot=False, near=2.0),
    ],
    "snow": [
        I("pine", "plant_tree_sosna", 6.0, snow=True, sway=GREEN, dens=0.4, near=2.3),
        I("pine", "plant_tree_sosna", 8.0, sx=0.85, tint=(0.8, 0.9, 0.85), snow=True, sway=GREEN, dens=0.3, near=2.3),
        I("pine", "plant_tree_sosna", 4.5, sx=1.15, snow=True, sway=GREEN, dens=0.3, near=2.3),
        I("drift", "snow_pile", None, sx=1.6, dens=0.3),
        I("rock", "rock_boulder", 1.2, sx=1.3, snow=True, dens=0.2),
        I("bush", "bush_berry_malina", 1.2, sx=1.3, snow=True, tint=(0.75, 0.8, 0.85), sway=GREEN, dens=0.2),
    ],
    "wasteland": [
        I("dead", "tree_dead_bare", 4.0, dens=0.12, near=1.8),
        I("dead", "tree_dead_burnt", 3.5, dens=0.1, near=1.8),
        I("rock", "rock_boulder", 1.2, sx=1.4, tint=(0.95, 0.85, 0.75), dens=0.2),
        I("ruin", "building_ruin_2", 6.0, dens=0.04, near=7.8, big=True),
        I("ruin", "ruin_column", None, dens=0.05, near=4.0),
        I("wreck", "car_wreck_razobrannaya", None, dens=0.03, near=3.0),
        I("barrels", "decor_barrels_rusty", None, dens=0.06),
        I("fence", "fence_wire_setka", None, dens=0.06, rot=False),
        I("pole", "code:pole_bare", None, dens=0.05, near=1.8, rot=False),
    ],
    "city": [
        I("building", "apartments_b", 16.0, win=True, dens=0.05, near=10.8, big=True, rot=False),
        I("building", "apartments", 14.0, win=True, dens=0.05, near=10.8, big=True, rot=False),
        I("building", "house_brick2", 9.0, win=True, dens=0.05, near=10.8, big=True, rot=False),
        I("building", "mall", 12.0, win=True, dens=0.04, near=10.8, big=True, rot=False),
        I("building", "construction_site", 10.0, dens=0.03, near=10.8, big=True, rot=False),
        I("ruin", "building_ruin_1", 10.0, dens=0.05, near=7.8, big=True, rot=False),
        I("ruin", "building_ruin_2", 9.0, dens=0.05, near=7.8, big=True, rot=False),
        I("crane", "crane_tower", 22.0, dens=0.01, near=12.0, big=True, rot=False),
        I("pole", "street_lamp_tselyy", None, dens=0.1, near=1.8, rot=False),
        I("billboard", "billboard_road_tselyy", 6.0, dens=0.03, near=4.0, rot=False),
        I("water_tower", "water_tower_kirpichnaya", 14.0, dens=0.01, near=12.0, big=True),
    ],
    "industrial": [
        I("factory", "warehouse", 8.0, win=True, dens=0.05, near=10.8, big=True, rot=False),
        I("factory", "power_plant", 18.0, win=True, smoke=True, dens=0.03, near=10.8, big=True, rot=False),
        I("factory", "power_plant_b", 16.0, win=True, smoke=True, dens=0.03, near=10.8, big=True, rot=False),
        I("cooling", "nuclear_plant", 18.0, win=True, smoke=True, dens=0.015, near=14.0, big=True, rot=False),
        I("hangar", "hangar", 9.0, win=True, dens=0.03, near=10.8, big=True, rot=False),
        I("crane", "crane_tower", 22.0, dens=0.015, near=12.0, big=True, rot=False),
        I("chimney", "code:chimney", None, smoke=True, dens=0.03, near=10.8, big=True),
        I("tanks", "code:tanks", None, dens=0.04, near=8.0, big=True),
        I("pylon", "code:pylon", None, dens=0.03, near=6.0, big=True, rot=False),
        I("pole", "pole_power", None, dens=0.08, near=1.8, rot=False),
    ],
}
BIRDS = {"crow": "crow", "seagull": "seagull", "pigeon": "pigeon"}


# ───────────────────────── вещи кодом (нет в Tripo) ─────────────────────────

def _seg(d, n):
    return max(4, [n, max(5, n * 2 // 3), max(4, n // 2)][d])


def haystack(b, d):
    s = _seg(d, 12)
    b.cyl((0, 0, 0.75), 1.25, 1.5, "straw", seg=s)
    b.cyl((0, 0, 1.75), 1.05, 0.5, "straw", seg=s)
    b.cyl((0, 0, 2.15), 0.65, 0.35, (0.72, 0.6, 0.32), seg=s)
    b.cyl((0, 0, 2.45), 0.25, 0.3, (0.7, 0.58, 0.3), seg=max(4, s // 2))
    if d < 2:
        b.box((-0.03, -0.03, 0), (0.03, 0.03, 2.9), "wood")


def _cactus(b, d, arms, h):
    s = _seg(d, 8)
    col = (0.32, 0.5, 0.26)
    b.cyl((0, 0, h / 2), 0.22, h, col, seg=s)
    b.ball((0, 0, h), 0.22, col, 0.7)
    for side, z, ln in arms:
        b.cyl((side * 0.32, 0, z), 0.13, 0.22, col, axis="x", seg=s)
        b.cyl((side * 0.43, 0, z + ln / 2), 0.14, ln, col, seg=s)
        b.ball((side * 0.43, 0, z + ln), 0.14, col, 0.7)
    if d == 0:
        for k in range(10):
            a = k * 2.4
            b.box((math.cos(a) * 0.22 - 0.005, math.sin(a) * 0.22 - 0.005, 0.3 + (k * 0.37) % (h - 0.4)),
                  (math.cos(a) * 0.22 + 0.005, math.sin(a) * 0.22 + 0.005, 0.32 + (k * 0.37) % (h - 0.4)), "cream")


def cactus1(b, d):
    _cactus(b, d, [(1, 1.0, 0.7), (-1, 1.4, 0.5)], 2.6)


def cactus2(b, d):
    _cactus(b, d, [(1, 0.8, 0.5)], 1.8)


def cactus3(b, d):
    _cactus(b, d, [], 1.2)
    b.ball((0.35, 0.1, 0.25), 0.25, (0.36, 0.52, 0.28), 0.8)


def cactus4(b, d):
    _cactus(b, d, [(1, 1.3, 0.9), (-1, 1.1, 0.8), (1, 2.0, 0.4)], 3.3)


def hummock(b, d):
    b.ball((0, 0, 0.1), 0.55, (0.32, 0.36, 0.2), 0.45)
    if d < 2:
        for k in range(7 if d == 0 else 4):
            a = k * 0.9
            b.cyl((math.cos(a) * 0.25, math.sin(a) * 0.25, 0.4), 0.03, 0.5, (0.5, 0.52, 0.28), seg=4,
                  rot=Matrix.Rotation(0.3 * math.cos(a), 4, "Y") @ Matrix.Rotation(0.3 * math.sin(a), 4, "X"))


def boardwalk(b, d):
    if d == 2:
        b.box((-2.5, -0.5, 0.26), (2.5, 0.5, 0.32), "wood_d")
        for x in (-2.3, 2.3):
            for y in (-0.45, 0.45):
                b.box((x - 0.05, y - 0.05, 0), (x + 0.05, y + 0.05, 0.28), "wood_d")
        return
    for i, x in enumerate(np.arange(-2.4, 2.41, 0.3 if d == 0 else 0.6)):
        b.box((x - 0.13, -0.5, 0.28 + (0.02 * ((i * 7) % 3))), (x + 0.13, 0.5, 0.32), "wood_d", rz=0.04 * ((i * 5) % 3 - 1))
    for x in (-2.3, -0.8, 0.8, 2.3):
        for y in (-0.45, 0.45):
            b.cyl((x, y, 0.15), 0.06, 0.35 if d < 2 else 0.3, "wood_d", seg=_seg(d, 6))
    b.box((-2.5, -0.45, 0.22), (2.5, -0.38, 0.28), "wood")
    b.box((-2.5, 0.38, 0.22), (2.5, 0.45, 0.28), "wood")


def pole_wires(b, d):
    s = _seg(d, 8)
    b.cyl((0, 0, 3.75), 0.13, 7.5, "wood_d", seg=s)
    b.box((-0.9, -0.06, 7.0), (0.9, 0.06, 7.12), "wood_d")
    for x in (-0.75, 0, 0.75):
        b.cyl((x, 0, 7.17), 0.035, 0.1, "white", seg=4)
        if d < 2:   # провода уходят к соседним столбам (провисают)
            for k in range(8):
                y0, y1 = -5 + k * 1.25, -5 + (k + 1) * 1.25
                sag = lambda t: 7.2 - 0.6 * (1 - ((t / 5.0) ** 2))
                b.box((x - 0.008, y0, sag(y0) - 0.008), (x + 0.008, y1, sag(y0) + 0.008), "black")


def pole_bare(b, d):
    b.cyl((0, 0, 3.5), 0.13, 7.0, (0.36, 0.3, 0.25), seg=_seg(d, 8), rot=Matrix.Rotation(0.06, 4, "Y"))
    b.box((-0.8, -0.06, 6.4), (0.8, 0.06, 6.52), (0.36, 0.3, 0.25), rz=0.0, ry=0.1)


def chimney(b, d):
    s = _seg(d, 12)
    b.cyl((0, 0, 9), 1.1, 18, (0.48, 0.3, 0.22), seg=s)
    for z in (4, 9, 14):
        b.cyl((0, 0, z), 1.13, 0.4, (0.4, 0.25, 0.18), seg=s)
    b.cyl((0, 0, 18.2), 1.2, 0.5, (0.25, 0.22, 0.2), seg=s)
    for z in (17.0, 17.3):
        b.cyl((0, 0, z), 1.12, 0.25, "white" if z == 17.0 else "red", seg=s)
    b.box((-1.8, -1.8, 0), (1.8, 1.8, 1.2), (0.42, 0.4, 0.38))


def tanks(b, d):
    s = _seg(d, 16)
    for x, r, h in ((-3.2, 2.2, 6.0), (2.0, 2.6, 7.5), (6.6, 1.6, 4.5)):
        b.cyl((x, 0, h / 2), r, h, (0.72, 0.72, 0.68), seg=s)
        b.cyl((x, 0, h + 0.25), r * 0.95, 0.5, (0.62, 0.62, 0.6), seg=s)
        if d < 2:
            b.cyl((x, 0, h * 0.5), r + 0.02, 0.15, "rust", seg=s)
            b.box((x + r - 0.05, -0.2, 0), (x + r + 0.05, 0.2, h), "metal_d")
    if d < 2:
        b.cyl((-0.5, 0, 4.5), 0.25, 3.5, "metal", axis="x", seg=_seg(d, 8))


def pylon(b, d):
    """ЛЭП-вышка: решётчатая, сужается кверху, траверсы с гирляндами."""
    H, W0, W1 = 24.0, 3.2, 0.8
    legs = [(sx, sy) for sx in (-1, 1) for sy in (-1, 1)]
    col = (0.5, 0.52, 0.52)
    import math as m
    for sx, sy in legs:
        p0 = Vector((sx * W0 / 2, sy * W0 / 2, 0))
        p1 = Vector((sx * W1 / 2, sy * W1 / 2, H * 0.82))
        v = p1 - p0
        ln = v.length
        q = Vector((0, 0, 1)).rotation_difference(v.normalized()).to_matrix().to_4x4()
        b.box((-0.08, -0.08, 0), (0.08, 0.08, ln), col)
        b.bm.verts.ensure_lookup_table()
        geom = b.bm.verts[-8:]
        bmesh.ops.transform(b.bm, matrix=Matrix.Translation(p0) @ q, verts=list(geom))
    lv = 6 if d == 0 else (4 if d == 1 else 2)
    for k in range(1, lv + 1):
        z = H * 0.82 * k / (lv + 1)
        w = (W0 + (W1 - W0) * k / (lv + 1)) / 2
        for sx in (-1, 1):
            b.box((-w, sx * w - 0.04, z - 0.04), (w, sx * w + 0.04, z + 0.04), col)
            b.box((sx * w - 0.04, -w, z - 0.04), (sx * w + 0.04, w, z + 0.04), col)
    b.box((-0.4, -0.4, H * 0.82), (0.4, 0.4, H), col)
    for z, half in ((H * 0.82, 4.0), (H * 0.92, 3.0)):
        b.box((-half, -0.12, z), (half, 0.12, z + 0.25), col)
        if d < 2:
            for x in (-half + 0.3, half - 0.3):
                b.cyl((x, 0, z - 0.6), 0.08, 1.2, "white", seg=6)


CODE = {f.__name__: f for f in (haystack, cactus1, cactus2, cactus3, cactus4, hummock, boardwalk, pole_wires,
                                 pole_bare, chimney, tanks, pylon)}


# ───────────────────────── загрузка и подготовка ─────────────────────────

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def normalize(obj, h, sx):
    """Низ на Z = 0, центр по X/Y, высота h (м), ширина ×sx."""
    co = np.array([v.co[:] for v in obj.data.vertices])
    lo, hi = co.min(0), co.max(0)
    k = (h / (hi[2] - lo[2])) if h else 1.0
    M = Matrix.Diagonal((k * sx, k * sx, k, 1.0)) @ Matrix.Translation((-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]))
    obj.data.transform(M)
    obj.data.update()


def load_source(it, d):
    """Объект-источник (одна сетка) для уровня d."""
    reset()
    src = it["src"]
    if src.startswith("code:"):
        b = D.Builder("body", seed=3)
        CODE[src[5:]](b, d)
        obj = b.obj()
        normalize(obj, None, it["sx"])
        return obj, False
    obj, _ = T.import_joined(os.path.join(ROOT, "export", f"{src}_idle.glb"))
    T.clear_custom_normals(obj)
    normalize(obj, it["h"], it["sx"])
    return obj, True


def image_of(obj):
    for s in obj.material_slots:
        m = s.material
        if m and m.use_nodes:
            img = T._upstream_image(m.node_tree.nodes["Principled BSDF"].inputs["Base Color"])
            if img is not None:
                return img
    return None


def face_colors(obj):
    """Цвет каждой грани (sRGB 0…1): по текстуре в точках UV граней или по цвету материала."""
    me = obj.data
    n = len(me.polygons)
    out = np.zeros((n, 3))
    img = image_of(obj)
    if img is not None and me.uv_layers.active:
        a = T._pixels(img)[..., :3]
        H, W = a.shape[:2]
        uv = np.zeros(len(me.loops) * 2)
        me.uv_layers.active.data.foreach_get("uv", uv)
        uv = uv.reshape(-1, 2)
        for i, f in enumerate(me.polygons):
            u = uv[f.loop_start:f.loop_start + f.loop_total]
            pts = np.vstack([u, u.mean(0, keepdims=True)])
            xs = np.clip((pts[:, 0] % 1.0) * (W - 1), 0, W - 1).astype(int)
            ys = np.clip((pts[:, 1] % 1.0) * (H - 1), 0, H - 1).astype(int)
            out[i] = a[ys, xs].mean(0)
    else:
        cols = []
        for s in obj.material_slots:
            c = s.material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value if s.material else (0.5,) * 4
            cols.append(np.array(c[:3]) ** (1 / 2.2))
        for i, f in enumerate(me.polygons):
            out[i] = cols[f.material_index] if cols else 0.5
    return out


def tint_obj(obj, tint):
    """Оттенок: для текстуры — перекрасить картинку, для цветов — материалы."""
    if not tint:
        return
    t = np.array(tint)
    img = image_of(obj)
    if img is not None:
        a = T._pixels(img)
        a[..., :3] = np.clip(a[..., :3] * t, 0, 1)
        T._set_pixels(img, a)
    else:
        for s in obj.material_slots:
            b = s.material.node_tree.nodes["Principled BSDF"].inputs["Base Color"]
            b.default_value = (*[min(1.0, c * k) for c, k in zip(b.default_value[:3], t)], 1.0)


def snow_mat():
    m = bpy.data.materials.get("snow") or bpy.data.materials.new("snow")
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.86, 0.9, 0.95, 1)
    b.inputs["Roughness"].default_value = 1.0
    return m


def add_snow(obj):
    """Снег на гранях, смотрящих вверх, — отдельный белый материал."""
    m = snow_mat()
    obj.data.materials.append(m)
    k = len(obj.data.materials) - 1
    co_z = np.array([v.co.z for v in obj.data.vertices])
    h = co_z.max()
    for f in obj.data.polygons:
        if f.normal.z > 0.45 and f.center.z > 0.15 * h:
            f.material_index = k


def window_faces(obj, cols):
    """Окна: тёмные почти вертикальные грани (у домов Tripo окна нарисованы тёмными)."""
    lum = cols @ np.array([0.3, 0.55, 0.15])
    nz = np.array([abs(f.normal.z) for f in obj.data.polygons])
    return (lum < 0.16) & (nz < 0.35)


def assign_windows(obj, cols):
    sel = window_faces(obj, cols)
    if not sel.any():
        return 0
    base = obj.data.materials[0]
    w = base.copy()
    w.name = "window_lit"
    obj.data.materials.append(w)
    k = len(obj.data.materials) - 1
    for f, s in zip(obj.data.polygons, sel):
        if s:
            f.material_index = k
    return int(sel.sum())


def sway_faces(obj, cols, mode):
    co_z = np.array([f.center.z for f in obj.data.polygons])
    h = max(co_z.max(), 1e-3)
    if mode == "all":
        return co_z > 0.08 * h
    if mode == "top":
        return co_z > 0.35 * h
    g = (cols[:, 1] > cols[:, 0] * 0.95) & (cols[:, 1] > cols[:, 2] * 1.05)   # зелень
    snow = np.array([obj.material_slots[f.material_index].material.name == "snow" if obj.material_slots else False
                     for f in obj.data.polygons])
    return (g | snow) & (co_z > 0.25 * h)


def split(obj, sel, name):
    """Выделенные грани — в отдельный объект name (точка опоры та же). → (остаток или None, новый или None)."""
    if not sel.any():
        return obj, None
    if sel.all():
        obj.name = obj.data.name = name
        return None, obj
    other = obj.copy()
    other.data = obj.data.copy()
    bpy.context.scene.collection.objects.link(other)
    for o, keep in ((obj, ~sel), (other, sel)):
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bm.faces.ensure_lookup_table()
        bmesh.ops.delete(bm, geom=[f for f, k in zip(bm.faces, keep) if not k], context="FACES")
        bm.to_mesh(o.data)
        bm.free()
    other.name = other.data.name = name
    return obj, other


def set_face_colors(obj, cols):
    """Один материал на всю сетку, у граней — свой цвет (материалы по цвету, чтобы face_colors / окна работали)."""
    me = obj.data
    me.materials.clear()
    q = np.round(np.clip(cols, 0, 1) * 24) / 24
    keys = {}
    for i, f in enumerate(me.polygons):
        k = tuple(q[i])
        if k not in keys:
            m = bpy.data.materials.new("c")
            m.use_nodes = True
            m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*[c ** 2.2 for c in k], 1.0)
            me.materials.append(m)
            keys[k] = len(me.materials) - 1
        f.material_index = keys[k]


def to_vertex_colors(obj, pal=False):
    """Без текстур: цвет грани — в цвет вершин (плоско), материал читает цвет вершин; окна/снег — свои материалы."""
    cols = face_colors(obj)
    if pal:
        cols = palette(cols)
    me = obj.data
    attr = me.color_attributes.new("Col", "FLOAT_COLOR", "CORNER")
    lin = np.clip(cols, 0, 1) ** 2.2
    data = np.zeros((len(me.loops), 4))
    for i, f in enumerate(me.polygons):
        data[f.loop_start:f.loop_start + f.loop_total, :3] = lin[i]
        data[f.loop_start:f.loop_start + f.loop_total, 3] = 1.0
    attr.data.foreach_set("color", data.ravel())
    names = [s.material.name if s.material else "" for s in obj.material_slots]
    new = {}
    for n in set(names) | {"body"}:
        key = "window_lit" if n == "window_lit" else "vc"
        if key in new:
            continue
        m = bpy.data.materials.new(key)
        m.use_nodes = True
        nt = m.node_tree
        ca = nt.nodes.new("ShaderNodeVertexColor")
        ca.layer_name = "Col"
        bsdf = nt.nodes["Principled BSDF"]
        nt.links.new(ca.outputs["Color"], bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 1.0
        bsdf.inputs["Metallic"].default_value = 0.0
        new[key] = m
    idx = [("window_lit" if n == "window_lit" else "vc") for n in names] or ["vc"]
    keys = list(dict.fromkeys(idx))
    remap = [keys.index(k) for k in idx]
    fi = np.array([remap[f.material_index] if remap else 0 for f in me.polygons])
    me.materials.clear()
    for k in keys:
        me.materials.append(new[k])
    for f, i in zip(me.polygons, fi):
        f.material_index = int(i)


def smoke_points(obj, max_n=3):
    """Выходы труб: самые высокие узкие «столбики» — локальные максимумы высоты на сетке 1 м."""
    co = np.array([v.co[:] for v in obj.data.vertices])
    h = co[:, 2].max()
    cell = max(0.6, (co[:, :2].max(0) - co[:, :2].min(0)).max() / 40)
    ij = np.floor(co[:, :2] / cell).astype(int)
    top = {}
    for (i, j), z, p in zip(map(tuple, ij), co[:, 2], co):
        if z > top.get((i, j), (-1, None))[0]:
            top[(i, j)] = (z, p)
    pts = []
    for (i, j), (z, p) in top.items():
        if z < 0.6 * h:
            continue
        nb = [top.get((i + a, j + b), (0, None))[0] for a in (-2, -1, 0, 1, 2) for b in (-2, -1, 0, 1, 2) if a or b]
        if z >= max(nb) and z - np.median(nb) > 0.08 * h:
            pts.append(p)
    pts.sort(key=lambda p: -p[2])
    out = []
    for p in pts:
        if all(np.hypot(*(p[:2] - q[:2])) > 1.5 for q in out):
            out.append(p)
    return [[round(float(p[0]), 3), round(float(p[1]), 3), round(float(p[2]), 3)] for p in out[:max_n]]


def export_objs(objs, path):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    for q in (85, 70):
        bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_yup=True,
                                  export_animations=False, export_image_format="JPEG", export_jpeg_quality=q,
                                  export_vertex_color="MATERIAL")
        if os.path.getsize(path) < 1_000_000:
            break
    return os.path.getsize(path) / 1e6


def islands(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    seen, out = set(), []
    for f in bm.faces:
        if f.index in seen:
            continue
        stack, grp = [f], []
        seen.add(f.index)
        while stack:
            g = stack.pop()
            grp.append(g.index)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen:
                        seen.add(h.index)
                        stack.append(h)
        co = np.array([v.co[:] for i in grp for v in bm.faces[i].verts])
        out.append((float(np.linalg.norm(co.max(0) - co.min(0))), grp))
    bm.free()
    return out


def drop_small(obj, frac):
    """Убрать мелкие отдельные кусочки (диагональ меньше frac размера вещи) — вдали их не видно."""
    co = np.array([v.co[:] for v in obj.data.vertices])
    size = float(np.linalg.norm(co.max(0) - co.min(0)))
    bad = [i for dg, grp in islands(obj) if dg < frac * size for i in grp]
    if not bad or len(bad) >= len(obj.data.polygons) * 0.9:
        return
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[bm.faces[i] for i in bad], context="FACES")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bm.to_mesh(obj.data)
    bm.free()


def voxel_reduce(obj, limit, d):
    """Последний способ: пересобрать в одну оболочку (voxel), облегчить, цвет — с оригинала в цвет вершин."""
    from mathutils.bvhtree import BVHTree
    src = obj.copy()
    src.data = obj.data.copy()
    bpy.context.scene.collection.objects.link(src)
    src_cols = face_colors(src)
    co = np.array([v.co[:] for v in obj.data.vertices])
    size = float((co.max(0) - co.min(0)).max())
    md = obj.modifiers.new("vox", "REMESH")
    md.mode = "VOXEL"
    md.voxel_size = size / 22
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=md.name)
    T.decimate(obj, limit)
    bvh = BVHTree.FromObject(src, bpy.context.evaluated_depsgraph_get())
    cols = np.zeros((len(obj.data.polygons), 3))
    for i, f in enumerate(obj.data.polygons):
        hit = bvh.find_nearest(f.center)
        cols[i] = src_cols[hit[2]] if hit[2] is not None else 0.5
    bpy.data.objects.remove(src)
    obj.data.materials.clear()
    return cols


def bake_proxy(obj, limit, d):
    """Сложная модель (дом, завод — сотни мелких кусков): простая оболочка той же формы + картинка оригинала,
    перенесённая на неё (запекание цвета, как наклейка) — окна, кирпич, краска остаются на месте."""
    src = obj.copy()
    src.data = obj.data.copy()
    bpy.context.scene.collection.objects.link(src)
    co = np.array([v.co[:] for v in obj.data.vertices])
    size = float((co.max(0) - co.min(0)).max())
    md = obj.modifiers.new("vox", "REMESH")
    md.mode = "VOXEL"
    md.voxel_size = size / (48 if d == 0 else 30)     # грубо: проёмы закрываются, стены — ровные плоскости
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=md.name)
    pd = obj.modifiers.new("plan", "DECIMATE")             # ровные места — крупными гранями
    pd.decimate_type = "DISSOLVE"
    pd.angle_limit = math.radians(6)
    bpy.ops.object.modifier_apply(modifier=pd.name)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    T.decimate(obj, limit)
    obj.data.materials.clear()
    for f in obj.data.polygons:
        f.use_smooth = False
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    while obj.data.uv_layers:
        obj.data.uv_layers.remove(obj.data.uv_layers[0])
    obj.data.uv_layers.new(name="UV")
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=0.01)
    bpy.ops.object.mode_set(mode="OBJECT")
    px = LOD_TEX[d]
    img = bpy.data.images.new(f"bake_{d}", px, px)
    m = bpy.data.materials.new("baked")
    m.use_nodes = True
    nt = m.node_tree
    tn = nt.nodes.new("ShaderNodeTexImage")
    tn.image = img
    nt.links.new(tn.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    nt.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    nt.nodes.active = tn
    obj.data.materials.append(m)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 1
    src.select_set(True)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"}, use_selected_to_active=True,
                        cage_extrusion=size * 0.015, max_ray_distance=size * 0.06, margin=4)
    img.pack()
    bpy.data.objects.remove(src)


def palette(cols, k=6):
    """Цвета граней → k основных (k-средних): вдали без пятен."""
    c = np.asarray(cols, float)
    if len(c) <= k:
        return c
    rng = np.random.default_rng(1)
    cen = c[rng.choice(len(c), k, replace=False)]
    for _ in range(12):
        lab = np.argmin(((c[:, None] - cen[None]) ** 2).sum(-1), 1)
        for j in range(k):
            if (lab == j).any():
                cen[j] = c[lab == j].mean(0)
    return cen[lab]


def reduce(obj, limit, d):
    """Облегчить до limit треугольников. → цвета граней (дальний уровень сложной модели), иначе None."""
    T.decimate(obj, limit)
    if T.tris(obj) <= limit * 1.1:
        return None
    if d < 2:
        bake_proxy(obj, limit, d)
        return None
    return palette(voxel_reduce(obj, limit, d))


# ───────────────────────── дома и заводы: «коробка по силуэту» с картинкой оригинала ─────────────────────────

def _flat_render(src, view, px, lo, hi):
    """Картинка модели без света (только цвет) ортографической камерой: front (с −Y), side (с −X), top (сверху)."""
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 8
    sc.cycles.use_denoising = False
    sc.render.film_transparent = True
    sc.view_settings.view_transform = "Standard"
    sc.world = sc.world or bpy.data.worlds.new("w")
    sc.world.color = (0, 0, 0)
    ext = hi - lo
    if view == "front":
        w, h, loc, rot = ext[0], ext[2], ((lo[0] + hi[0]) / 2, lo[1] - 50, (lo[2] + hi[2]) / 2), (math.pi / 2, 0, 0)
    elif view == "side":
        w, h, loc, rot = ext[1], ext[2], (lo[0] - 50, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2), (math.pi / 2, 0, -math.pi / 2)
    else:
        w, h, loc, rot = ext[0], ext[1], ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, hi[2] + 50), (0, 0, 0)
    cam = bpy.data.objects.get("_fc") or bpy.data.objects.new("_fc", bpy.data.cameras.new("_fc"))
    if cam.name not in sc.collection.objects:
        sc.collection.objects.link(cam)
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = max(w, h)
    cam.data.clip_end = 500
    cam.location, cam.rotation_euler = loc, rot
    sc.camera = cam
    rx = px if w >= h else max(8, int(px * w / h))
    ry = px if h >= w else max(8, int(px * h / w))
    sc.render.resolution_x, sc.render.resolution_y = rx, ry
    path = os.path.join(OUT, f"_tmp_{view}.png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    from PIL import Image
    im = np.asarray(Image.open(path).convert("RGBA")).astype(float) / 255
    os.remove(path)
    return im[::-1]          # строка 0 — низ


def _emission_copy(obj):
    """Копия модели, у которой материалы светят своим цветом (картинка без света и теней)."""
    src = obj.copy()
    src.data = obj.data.copy()
    bpy.context.scene.collection.objects.link(src)
    for i, slot in enumerate(src.material_slots):
        m0 = slot.material
        img = T._upstream_image(m0.node_tree.nodes["Principled BSDF"].inputs["Base Color"]) if m0 and m0.use_nodes else None
        m = bpy.data.materials.new("emit")
        m.use_nodes = True
        nt = m.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        em = nt.nodes.new("ShaderNodeEmission")
        if img is not None:
            tn = nt.nodes.new("ShaderNodeTexImage")
            tn.image = img
            nt.links.new(tn.outputs["Color"], em.inputs["Color"])
        else:
            em.inputs["Color"].default_value = m0.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
        src.material_slots[i].material = m
    obj.hide_render = True
    return src


def _profile(alpha, n):
    """Верх силуэта по столбцам (в долях высоты) → упрощённая ломаная из ≈n точек (Дуглас — Пекер)."""
    H, W = alpha.shape
    top = np.array([(np.nonzero(alpha[:, x] > 0.5)[0].max() + 1) / H if (alpha[:, x] > 0.5).any() else 0.0
                    for x in range(W)])
    pts = np.stack([np.arange(W) / (W - 1), top], 1)
    keep = [0, W - 1]

    def dp(i, j, eps):
        if j <= i + 1:
            return
        a, b = pts[i], pts[j]
        ab = b - a
        r = pts[i + 1:j] - a
        d = np.abs(ab[0] * r[:, 1] - ab[1] * r[:, 0]) / (np.linalg.norm(ab) + 1e-9)
        k = int(np.argmax(d))
        if d[k] > eps:
            keep.append(i + 1 + k)
            dp(i, i + 1 + k, eps)
            dp(i + 1 + k, j, eps)
    eps = 0.002
    while True:
        keep[:] = [0, W - 1]
        dp(0, W - 1, eps)
        if len(keep) <= n:
            break
        eps *= 1.4
    return pts[sorted(set(keep))]


def prism_lod(obj, it, d):
    """Тело по силуэту спереди (выдавленное на глубину модели), картинки спереди / сбоку / сверху; окна — плашки
    window_lit по тёмным местам картинки спереди. → [объекты]."""
    from PIL import Image
    co = np.array([v.co[:] for v in obj.data.vertices])
    lo, hi = co.min(0), co.max(0)
    src = _emission_copy(obj)
    px = (512, 256, 128)[d]
    fr = _flat_render(src, "front", px, lo, hi)
    sd = _flat_render(src, "side", px // 2, lo, hi)
    tp = _flat_render(src, "top", px // 2, lo, hi)
    bpy.data.objects.remove(src)
    # вырезать картинку по рамке модели (камера квадратная по большей стороне)
    def crop(im, w, h):
        H, W = im.shape[:2]
        return im
    prof = _profile(fr[..., 3], (64, 24, 12)[d])
    x0, x1, y0, y1, z0, z1 = lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]
    poly = [(x0 + (x1 - x0) * u, z0 + (z1 - z0) * v) for u, v in prof]
    poly = [(x0, z0)] + [(x, max(z, z0 + 0.05)) for x, z in poly] + [(x1, z0)]
    # атлас: слева сверху — спереди (512×256), снизу — сбоку и сверху
    A = px
    atlas = np.zeros((A, A, 4))
    def put(im, u0, v0, uw, vh):
        h_, w_ = im.shape[:2]
        pil = Image.fromarray((np.clip(im[::-1], 0, 1) * 255).astype(np.uint8), "RGBA").resize((int(uw * A), int(vh * A)))
        a = np.asarray(pil).astype(float)[::-1] / 255
        atlas[int(v0 * A):int(v0 * A) + a.shape[0], int(u0 * A):int(u0 * A) + a.shape[1]] = a
    put(fr, 0, 0.5, 1.0, 0.5)
    put(sd, 0, 0, 0.5, 0.5)
    put(tp, 0.5, 0, 0.5, 0.5)
    # дорисовать прозрачное средним цветом (края, щели), чтобы не было чёрного
    mean = atlas[atlas[..., 3] > 0.5][:, :3].mean(0) if (atlas[..., 3] > 0.5).any() else np.array([0.5] * 3)
    atlas[atlas[..., 3] <= 0.5, :3] = mean
    atlas[..., 3] = 1
    me = bpy.data.meshes.new("body")
    bm = bmesh.new()
    uvl = bm.loops.layers.uv.new("UV")
    def fuv(x, z):
        return (x - x0) / (x1 - x0 + 1e-9), 0.5 + 0.5 * (z - z0) / (z1 - z0 + 1e-9)
    def suv(y, z):
        return 0.5 * (y - y0) / (y1 - y0 + 1e-9), 0.5 * (z - z0) / (z1 - z0 + 1e-9)
    def tuv(x, y):
        return 0.5 + 0.5 * (x - x0) / (x1 - x0 + 1e-9), 0.5 * (y - y0) / (y1 - y0 + 1e-9)
    from mathutils.geometry import tessellate_polygon
    tri = tessellate_polygon([[Vector((x, z, 0)) for x, z in poly]])
    for yy, flip in ((y0, False), (y1, True)):
        vs = [bm.verts.new((x, yy, z)) for x, z in poly]
        for t in tri:
            t = t if not flip else t[::-1]
            if not flip:
                t = t[::-1]
            try:
                f = bm.faces.new([vs[i] for i in t])
            except ValueError:
                continue
            for l in f.loops:
                l[uvl].uv = fuv(l.vert.co.x, l.vert.co.z)
    n = len(poly)
    for i in range(n):
        (xa, za), (xb, zb) = poly[i], poly[(i + 1) % n]
        if abs(xa - xb) < 1e-6 and abs(za - zb) < 1e-6:
            continue
        q = [bm.verts.new((xa, y0, za)), bm.verts.new((xa, y1, za)), bm.verts.new((xb, y1, zb)), bm.verts.new((xb, y0, zb))]
        try:
            f = bm.faces.new(q)
        except ValueError:
            continue
        vertical = abs(xb - xa) < abs(zb - za) * 0.5
        for l in f.loops:
            c = l.vert.co
            l[uvl].uv = suv(c.y, c.z) if vertical else tuv(c.x, c.y)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    body = bpy.data.objects.new("body", me)
    bpy.context.scene.collection.objects.link(body)
    objs = [body]
    if d < 2:
        img = bpy.data.images.new("atlas", A, A)
        img.pixels.foreach_set(atlas.astype(np.float32).ravel())
        img.pack()
        m = bpy.data.materials.new("bg_atlas")
        m.use_nodes = True
        nt = m.node_tree
        tn = nt.nodes.new("ShaderNodeTexImage")
        tn.image = img
        nt.links.new(tn.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
        nt.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
        me.materials.append(m)
    else:   # вдали — без картинки: цвет каждой грани — средний по атласу под ней
        me.materials.append(bpy.data.materials.new("tmp"))
        cols = []
        uv = me.uv_layers.active.data
        for f in me.polygons:
            us = np.array([uv[li].uv[:] for li in f.loop_indices]).mean(0)
            cols.append(atlas[min(A - 1, int(us[1] * A)), min(A - 1, int(us[0] * A)), :3])
        set_face_colors(body, np.array(cols))
        to_vertex_colors(body)
    # окна: тёмные пятна на картинке спереди → плашки перед фасадом (window_lit)
    if it["win"]:
        lum = fr[..., :3] @ np.array([0.3, 0.55, 0.15])
        inside = fr[..., 3] > 0.5
        med = np.median(lum[inside]) if inside.any() else 0.5
        dark = (lum < med * 0.62) & inside                 # окно — заметно темнее своей стены
        H, W = dark.shape
        cell = max(0.4, (x1 - x0) / (40 if d == 0 else (20 if d == 1 else 10)))
        nx_, nz_ = int((x1 - x0) / cell), int((z1 - z0) / cell)
        wb = D.Builder("window_lit", 5)
        for j in range(nz_):
            run = None
            for i in range(nx_ + 1):
                ok = False
                if i < nx_:
                    blk = dark[int(j / nz_ * H):int((j + 1) / nz_ * H), int(i / nx_ * W):int((i + 1) / nx_ * W)]
                    ok = blk.size > 0 and blk.mean() > 0.55
                if ok and run is None:
                    run = i
                if not ok and run is not None:
                    xa, xb = x0 + run * cell, x0 + i * cell
                    za, zb = z0 + j * cell, z0 + (j + 1) * cell
                    wb.box((xa + 0.05, y0 - 0.06, za + 0.05), (xb - 0.05, y0 - 0.02, zb - 0.05), (0.08, 0.09, 0.11))
                    run = None
        if wb.bm.faces:
            w = wb.obj()
            for mm in w.data.materials:
                mm.name = "window_lit"
            if d == 2:
                to_vertex_colors(w)
                for mm in w.data.materials:
                    mm.name = "window_lit"
            w.name = w.data.name = "windows"
            objs.append(w)
    return objs


def card_lod(obj, budget=150):
    """Вдали — два скрещённых плоских силуэта (спереди и сбоку): контур по картинке модели (OpenCV), упрощённый
    до нужного числа точек, — острые грани, как у low poly; цвет каждого треугольника — средний под ним (в вершинах).
    Материал двусторонний. Нужен пакет opencv-python-headless."""
    import cv2
    from mathutils.geometry import tessellate_polygon
    co = np.array([v.co[:] for v in obj.data.vertices])
    lo, hi = co.min(0), co.max(0)
    src = _emission_copy(obj)
    ims = {v: _flat_render(src, v, 160, lo, hi) for v in ("front", "side")}
    bpy.data.objects.remove(src)
    eps = 1.0
    while True:
        b = D.Builder("body", 1)
        for view, im in ims.items():
            H, W = im.shape[:2]
            mask = (im[..., 3] > 0.35).astype(np.uint8)
            mask = cv2.dilate(mask, np.ones((3, 3), np.uint8))
            cnts, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            if hier is None:
                continue
            u0, u1 = (lo[0], hi[0]) if view == "front" else (lo[1], hi[1])

            def to3(px, py):
                u = u0 + (u1 - u0) * (px + 0.5) / W
                z = lo[2] + (hi[2] - lo[2]) * (py + 0.5) / H
                return Vector((u, 0.0, z)) if view == "front" else Vector((0.0, u, z))
            for k, c in enumerate(cnts):
                if hier[0][k][3] != -1 or cv2.contourArea(c) < 4:     # только внешние (дыры — ниже)
                    continue
                loops = [cv2.approxPolyDP(c, eps, True).reshape(-1, 2)]
                ch = hier[0][k][2]
                while ch != -1:
                    if cv2.contourArea(cnts[ch]) > 30:
                        loops.append(cv2.approxPolyDP(cnts[ch], eps, True).reshape(-1, 2))
                    ch = hier[0][ch][0]
                loops = [l for l in loops if len(l) >= 3]
                if not loops:
                    continue
                pts3 = [[to3(*p) for p in l] for l in loops]
                flat = [p for l in pts3 for p in l]
                for t in tessellate_polygon([[Vector((p[0], p[1], 0)) for p in l] for l in loops]):
                    tri2 = np.array([[loops_flat[0], loops_flat[1]] for loops_flat in
                                     [np.concatenate(loops)[i] for i in t]])
                    cx, cy = tri2.mean(0)
                    samp = [tri2.mean(0)] + [tri2[q] * 0.7 + tri2.mean(0) * 0.3 for q in range(3)]
                    cols = [im[int(np.clip(y, 0, H - 1)), int(np.clip(x, 0, W - 1))] for x, y in samp]
                    cols = [c_[:3] for c_ in cols if c_[3] > 0.3] or [np.array([0.4, 0.35, 0.3])]
                    col = tuple(np.round(np.mean(cols, 0), 2))
                    vs = [b.bm.verts.new(flat[i]) for i in t]
                    try:
                        f = b.bm.faces.new(vs)
                        f.material_index = b._mat(col)
                    except ValueError:
                        pass
        n = len(b.bm.faces)
        if n <= budget or eps > 12:
            break
        b.bm.free()
        eps *= 1.35
    o = b.obj()
    to_vertex_colors(o)
    for m in o.data.materials:
        m.use_backface_culling = False
    o.name = o.data.name = "body"
    return o


PRISM_KINDS = {"building", "factory", "cooling", "hangar", "barn", "water_tower"}


def build_lod(it, d, base_id):
    obj, textured = load_source(it, d)
    limit = (LOD_TRIS_BIG if it["big"] else LOD_TRIS)[d]
    if textured and d == 2 and it.get("card"):
        tint_obj(obj, it["tint"])
        T.fix_materials(obj, 512)
        c = card_lod(obj)
        bpy.data.objects.remove(obj)
        objs = [c]
        if it["sway"]:
            body, sw = split(c, sway_faces(c, face_colors(c), it["sway"]), "sway")
            objs = [o for o in (body, sw) if o is not None]
        path = os.path.join(OUT, f"{base_id}_lod{d}.glb")
        mb = export_objs(objs, path)
        co = np.array([v.co[:] for o in objs for v in o.data.vertices])
        return {"file": os.path.basename(path), "tris": sum(T.tris(o) for o in objs), "mb": round(mb, 3),
                "size": (co.max(0) - co.min(0)).tolist(), "smoke": [], "windows": 0, "sway": len(objs) > 1 or objs[0].name == "sway"}
    if textured and it["kind"] in PRISM_KINDS:
        T.fix_materials(obj, 1024)
        tint_obj(obj, it["tint"])
        smk = smoke_points(obj) if it["smoke"] else []
        objs = prism_lod(obj, it, d)
        bpy.data.objects.remove(obj)
        for k, p in enumerate(smk):
            e = bpy.data.objects.new(f"smoke_{k + 1}", None)
            bpy.context.scene.collection.objects.link(e)
            e.location = Vector(p)
            objs.append(e)
        path = os.path.join(OUT, f"{base_id}_lod{d}.glb")
        mb = export_objs(objs, path)
        meshes = [o for o in objs if o.type == "MESH"]
        co = np.array([v.co[:] for o in meshes for v in o.data.vertices])
        return {"file": os.path.basename(path), "tris": sum(T.tris(o) for o in meshes), "mb": round(mb, 3),
                "size": (co.max(0) - co.min(0)).tolist(), "smoke": smk, "windows": int(any(o.name == "windows" for o in objs)),
                "sway": False}
    baked = None
    if textured:
        T.fix_materials(obj, LOD_TEX[d] or 64)
        tint_obj(obj, it["tint"])
        baked = reduce(obj, limit, d)
    else:
        tint_obj(obj, it["tint"])
    if baked is not None:                               # пересобрано: цвета граней уже есть — материал «цвет вершин»
        set_face_colors(obj, baked)
        textured = False
    if it["snow"]:
        add_snow(obj)
    cols = face_colors(obj)
    nwin = assign_windows(obj, cols) if it["win"] else 0
    smk = smoke_points(obj) if it["smoke"] else []
    if d == 2 or not textured:
        to_vertex_colors(obj, pal=(d == 2 and textured))
    obj.name = obj.data.name = "body"
    objs = [obj]
    if it["sway"]:
        body, sw = split(obj, sway_faces(obj, face_colors(obj), it["sway"]), "sway")
        objs = [o for o in (body, sw) if o is not None]
        if body is not None:
            body.name = body.data.name = "body"
    if it["src"] == "code:pylon" or it["kind"] == "fence":
        pass
    for k, p in enumerate(smk):
        e = bpy.data.objects.new(f"smoke_{k + 1}", None)
        bpy.context.scene.collection.objects.link(e)
        e.location = Vector(p)
        objs.append(e)
    for o in objs:
        if o.type == "MESH":
            T.smooth_by_angle(o, 30)
    path = os.path.join(OUT, f"{base_id}_lod{d}.glb")
    mb = export_objs(objs, path)
    meshes = [o for o in objs if o.type == "MESH"]
    co = np.array([v.co[:] for o in meshes for v in o.data.vertices])
    size = (co.max(0) - co.min(0)).tolist()
    tris = sum(T.tris(o) for o in meshes)
    return {"file": os.path.basename(path), "tris": tris, "mb": round(mb, 3), "size": size, "smoke": smk,
            "windows": nwin, "sway": any(o.name.startswith("sway") for o in objs)}


def build_item(biome, it, n):
    base_id = f"bg_{biome}_{it['kind']}_{n}"
    lods = [build_lod(it, d, base_id) for d in range(3)]
    sz = lods[0]["size"]
    rec = {"id": base_id, "kind": it["kind"], "source": it["src"],
           "size": [round(sz[0], 2), round(sz[2], 2), round(sz[1], 2)],      # [ш, в, г], м (Godot: X, Y, Z)
           "lods": [l["file"] for l in lods], "tris": [l["tris"] for l in lods],
           "per_10m2": it["dens"], "min_depth": it["near"], "rotate": it["rot"],
           "sway": lods[0]["sway"], "smoke": [[p[0], p[2], -p[1]] for p in lods[0]["smoke"]],
           "window_lit": lods[0]["windows"] > 0}
    print(f"[{base_id}] {rec['tris']} тр, {[l['mb'] for l in lods]} МБ, размер {rec['size']}"
          f"{' sway' if rec['sway'] else ''}{' smoke×%d' % len(rec['smoke']) if rec['smoke'] else ''}"
          f"{' окна' if rec['window_lit'] else ''}", flush=True)
    return rec


# ───────────────────────── ленты дальнего рельефа ─────────────────────────

RIDGE_W, RIDGE_D = 40.0, 30.0
RIDGES = {   # биом: [(цвет низа, цвет верха), высота, рельеф, что на гребне]
    "forest": [((0.24, 0.33, 0.18), (0.2, 0.3, 0.17)), 7.0, "hills", "trees"],
    "field": [((0.45, 0.5, 0.26), (0.36, 0.46, 0.22)), 4.0, "hills", "groves"],
    "desert": [((0.72, 0.6, 0.4), (0.62, 0.46, 0.3)), 9.0, "mesas", None],
    "swamp": [((0.24, 0.28, 0.18), (0.2, 0.24, 0.16)), 2.5, "hills", "dead"],
    "snow": [((0.62, 0.66, 0.72), (0.9, 0.93, 0.96)), 16.0, "mountains", "pines"],
    "wasteland": [((0.42, 0.36, 0.28), (0.36, 0.3, 0.24)), 6.0, "hills", "ruins"],
    "city": [((0.3, 0.3, 0.3), (0.3, 0.3, 0.3)), 1.0, "flat", "skyline"],
    "industrial": [((0.32, 0.31, 0.29), (0.32, 0.31, 0.29)), 1.0, "flat", "plants"],
}


def ridge(biome, n):
    (c0, c1), H, relief, top = RIDGES[biome]
    rng = random.Random(hash((biome, n)) & 0xFFFF)
    b = D.Builder(f"ridge_{biome}_{n}", seed=n)
    nx, ny = 40, 10
    ph = [rng.uniform(0, 6.28) for _ in range(6)]

    def hgt(x, y):
        t = y / RIDGE_D
        u = 2 * math.pi * x / RIDGE_W                        # период 40 м — края совпадают
        if relief == "flat":
            return 0.3 * math.sin(u + ph[0]) * t
        if relief == "mesas":
            v = 0.5 + 0.35 * math.sin(u + ph[0]) + 0.2 * math.sin(2 * u + ph[1]) + 0.12 * math.sin(5 * u + ph[2])
            v = min(1.0, max(0.0, (v - 0.35) * 2.2))
            return H * (v ** 0.4) * min(1, t * 2.5)
        if relief == "mountains":
            v = 0.55 + 0.3 * math.sin(u * 2 + ph[0]) + 0.18 * math.sin(u * 3 + ph[1]) + 0.1 * math.sin(u * 7 + ph[2])
            return H * max(0.05, v) * (t ** 0.8)
        v = 0.6 + 0.25 * math.sin(u + ph[0]) + 0.15 * math.sin(3 * u + ph[1]) + 0.07 * math.sin(6 * u + ph[2])
        return H * v * (t ** 0.7)
    xs = np.linspace(-RIDGE_W / 2, RIDGE_W / 2, nx + 1)
    ys = np.linspace(0, RIDGE_D, ny + 1)
    bm = b.bm
    for i in range(nx):
        for j in range(ny):
            P = [(xs[i], ys[j]), (xs[i + 1], ys[j]), (xs[i + 1], ys[j + 1]), (xs[i], ys[j + 1])]
            vs = [bm.verts.new((x, y, hgt(x, y))) for x, y in P]
            z = np.mean([v.co.z for v in vs])
            k = min(1.0, z / max(H, 1.0))
            col = tuple(np.array(c0) * (1 - k) + np.array(c1) * k)
            if relief == "mountains" and z > H * 0.55:
                col = (0.9, 0.93, 0.96)
            col = tuple(c * rng.uniform(0.92, 1.06) for c in col)
            f = bm.faces.new(vs)
            f.material_index = b._mat(tuple(round(c, 2) for c in col))
    # на гребне
    def on_top(x):
        return hgt(x, RIDGE_D * rng.uniform(0.55, 1.0)), None
    if top in ("trees", "groves", "pines", "dead"):
        cnt = {"trees": 90, "groves": 25, "pines": 50, "dead": 30}[top]
        for _ in range(cnt):
            x = rng.uniform(-RIDGE_W / 2 + 1, RIDGE_W / 2 - 1)
            y = rng.uniform(RIDGE_D * 0.2, RIDGE_D)
            z = hgt(x, y)
            if top == "pines" and z > H * 0.55:
                continue
            s = rng.uniform(0.7, 1.4)
            if top == "dead":
                c_ = (0.25, 0.23, 0.2)
                b.cyl((x, y, z + 1.5 * s), 0.12 * s, 3 * s, c_, seg=4)
                for sgn, zz in ((1, 2.0), (-1, 2.4), (1, 2.8)):
                    b.cyl((x + sgn * 0.35 * s, y, z + zz * s), 0.06 * s, 0.9 * s, c_, seg=4,
                          rot=Matrix.Rotation(sgn * 0.8, 4, "Y"))
                continue
            col = (0.16, 0.26, 0.15) if top != "groves" else (0.24, 0.36, 0.18)
            if top == "groves":
                b.ball((x, y, z + 1.6 * s), 1.4 * s, col, 0.8)
            else:
                g = bmesh.ops.create_cone(bm, cap_ends=False, segments=5, radius1=1.1 * s, radius2=0, depth=4.5 * s)
                b._add(g["verts"], (col if top != "pines" else (0.16, 0.24, 0.18)), Matrix.Translation((x, y, z + 2.2 * s)))
    elif top == "ruins":
        for _ in range(10):
            x = rng.uniform(-18, 18)
            y = rng.uniform(8, 28)
            z = hgt(x, y)
            w, h = rng.uniform(2, 5), rng.uniform(2, 6)
            b.box((x - w / 2, y - 1, z - 0.5), (x + w / 2, y + 1, z + h), (0.38, 0.34, 0.3), rz=rng.uniform(-0.3, 0.3))
    elif top == "skyline":
        x = -RIDGE_W / 2 + 0.5
        while x < RIDGE_W / 2 - 3:
            w = rng.uniform(3, 7)
            h = rng.choice([rng.uniform(8, 18), rng.uniform(15, 35)])
            y = rng.uniform(5, 25)
            col = rng.choice([(0.42, 0.42, 0.44), (0.5, 0.45, 0.4), (0.36, 0.38, 0.42), (0.47, 0.36, 0.3)])
            b.box((x, y, 0), (x + w, y + rng.uniform(4, 8), h), col)
            if rng.random() < 0.4:
                b.box((x + w * 0.2, y + 1, h), (x + w * 0.8, y + 3, h + rng.uniform(2, 6)), col)
            if rng.random() < 0.3:   # обломанный верх
                b.box((x, y, h - 2), (x + w * 0.5, y + 4, h + 1.5), col, ry=0.5)
            x += w + rng.uniform(0.3, 2.0)
    elif top == "plants":
        for _ in range(6):
            x = rng.uniform(-17, 15)
            y = rng.uniform(8, 25)
            w, h = rng.uniform(5, 10), rng.uniform(5, 10)
            b.box((x, y, 0), (x + w, y + 6, h), (0.42, 0.4, 0.38))
        for _ in range(4):
            x, y = rng.uniform(-18, 18), rng.uniform(10, 28)
            b.cyl((x, y, 12), 0.8, 24, (0.45, 0.32, 0.26), seg=6)
        x, y = rng.uniform(-10, 10), rng.uniform(15, 28)
        g = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=6, radius2=4, depth=16)
        b._add(g["verts"], (0.62, 0.62, 0.6), Matrix.Translation((x, y, 8)))
    obj = b.obj()
    to_vertex_colors(obj)
    obj.name = obj.data.name = "ridge"
    path = os.path.join(OUT, f"bg_{biome}_ridge_{n}_idle.glb")
    mb = export_objs([obj], path)
    print(f"[bg_{biome}_ridge_{n}] {T.tris(obj)} тр, {mb:.2f} МБ", flush=True)
    return {"id": f"bg_{biome}_ridge_{n}", "file": os.path.basename(path), "width": RIDGE_W, "depth": RIDGE_D,
            "tris": T.tris(obj), "height": round(float(max(v.co.z for v in obj.data.vertices)), 2)}


# ───────────────────────── птицы ─────────────────────────

def bird(name, src):
    reset()
    bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, "export", f"{src}_idle.glb"))
    keep = [a for a in bpy.data.actions if a.name.lower().startswith("fly")]
    for a in list(bpy.data.actions):
        if a not in keep[:1]:
            bpy.data.actions.remove(a)
    if keep:
        keep[0].name = "bird_flap"
    arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
    if arm.animation_data is None:
        arm.animation_data_create()
    if keep:
        arm.animation_data.action = keep[0]
    for o in bpy.context.scene.objects:
        if o.type == "MESH":
            T.decimate(o, 500)
            T.fix_materials(o, 128)
    path = os.path.join(OUT, f"bg_bird_{name}_idle.glb")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_yup=True,
                              export_animations=True, export_animation_mode="ACTIONS", export_image_format="JPEG",
                              export_jpeg_quality=80)
    print(f"[bg_bird_{name}] {os.path.getsize(path) / 1e6:.2f} МБ, анимация: {[a.name for a in bpy.data.actions]}", flush=True)
    return {"id": f"bg_bird_{name}", "file": os.path.basename(path), "animation": "bird_flap"}


# ───────────────────────── листы превью и сцена-проба ─────────────────────────

def _import(path):
    bpy.ops.import_scene.gltf(filepath=path)
    return [o for o in bpy.context.selected_objects]


def preview(biome):
    """Все вещи биома: в каждой строке — уровни 0, 1, 2 (со светом)."""
    from PIL import Image, ImageDraw, ImageFont
    recs = json.load(open(os.path.join(OUT, f"_{biome}.json")))
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 13)
    tiles = []
    for r in recs["items"]:
        row = []
        for d, f in enumerate(r["lods"]):
            reset()
            objs = _import(os.path.join(OUT, f))
            ms = [o for o in objs if o.type == "MESH"]
            co = np.array([o.matrix_world @ v.co for o in ms for v in o.data.vertices])
            me = bpy.data.meshes.new("f")
            me.from_pydata([tuple(co.min(0)), tuple(co.max(0))], [], [])
            fr = bpy.data.objects.new("f", me)
            bpy.context.scene.collection.objects.link(fr)
            os.environ["TRIPO_FAST"] = "1"
            ims = T.render_views(fr, os.path.join(OUT, f"_pv_{d}"), px=220, fit=1.25)
            os.environ.pop("TRIPO_FAST")
            im = Image.open(ims[0]).convert("RGB")
            ImageDraw.Draw(im).text((4, 4), f"lod{d}: {r['tris'][d]}", font=font, fill=(255, 230, 120))
            row.append(im)
            os.remove(ims[0])
        tiles.append((r, row))
    cols = 3
    per = 4                                                     # вещей в строке листа
    W = per * (cols * 220 + 16)
    rows = (len(tiles) + per - 1) // per
    sheet = Image.new("RGB", (W, rows * 250 + 10), (22, 23, 28))
    d = ImageDraw.Draw(sheet)
    for k, (r, row) in enumerate(tiles):
        x0, y0 = (k % per) * (cols * 220 + 16), (k // per) * 250
        d.text((x0 + 6, y0 + 6), r["id"].replace("bg_", "") + (" · sway" if r["sway"] else "") +
               (" · smoke" if r["smoke"] else "") + (" · окна" if r["window_lit"] else ""), font=font, fill=(235, 235, 235))
        for j, im in enumerate(row):
            sheet.paste(im, (x0 + j * 220, y0 + 26))
    out = os.path.join(ROOT, "renders", "_review", f"backdrop_{biome}.png")
    sheet.save(out)
    print("лист:", out, flush=True)


def _h(x, z, seed):     # как в игре (Backdrop._h)
    s = seed * 0.13
    return 0.5 + 0.5 * (math.sin(x * 0.11 + s) * 0.6 + math.sin(z * 0.19 + x * 0.05 + s * 1.7) * 0.4) * math.cos(x * 0.031 - z * 0.07 + s)


GROUND = {"forest": ((0.25, 0.35, 0.17), 3.0), "field": ((0.49, 0.54, 0.24), 1.4), "desert": ((0.78, 0.66, 0.42), 2.4),
          "swamp": ((0.24, 0.29, 0.16), 0.5), "snow": ((0.9, 0.92, 0.94), 3.0), "wasteland": ((0.48, 0.42, 0.31), 2.0),
          "city": ((0.36, 0.35, 0.33), 0.4), "industrial": ((0.35, 0.34, 0.3), 0.5)}
Z_FROM, Z_TO = -5.2, -30.0


def scene(biome):
    """Сцена-проба как в игре: улица спереди, фон по глубине (уровни по дальности), лента на горизонте, дымка;
    камера — как в игре (40°, наклон 10°). Координаты Blender: вглубь — +Y (в игре −Z)."""
    recs = json.load(open(os.path.join(OUT, f"_{biome}.json")))
    reset()
    sc = bpy.context.scene
    rng = random.Random(7)
    col, hh = GROUND[biome]
    # земля фона (как Backdrop.height) и улица
    b = D.Builder("ground", 2)
    for ix in range(-30, 30):
        for iz in range(int(-Z_FROM), int(-Z_TO) + 40):
            pts = []
            for dx, dz in ((0, 0), (1, 0), (1, 1), (0, 1)):
                x, z = ix + dx, -(iz + dz)
                ramp = min(1.0, max(0.0, (Z_FROM - z) / 6.0))
                hgt = 0.02 + hh * _h(x, z, 3) * ramp * ramp if z > Z_TO else 0.02 + hh * _h(x, Z_TO, 3)
                pts.append(b.bm.verts.new((x, -z, hgt)))
            f = b.bm.faces.new(pts)
            f.material_index = b._mat(tuple(round(c * rng.uniform(0.92, 1.06), 2) for c in col))
    street = (0.42, 0.4, 0.37) if biome in ("city", "industrial") else tuple(c * 0.85 for c in col)
    b.box((-40, -25, -0.05), (40, -Z_FROM, 0.02), street)
    b.box((-30, -0.4, 0.02), (30, -0.2, 0.15), (0.6, 0.6, 0.58))
    g = b.obj()
    ghgt = lambda x, z: (0.02 + hh * _h(x, z, 3) * min(1, max(0, (Z_FROM - z) / 6)) ** 2)
    # вещи по густоте и дальности
    for r in recs["items"]:
        n = int(r["per_10m2"] * 60 * (Z_FROM - Z_TO) / 10 * 0.5) + 1
        for _ in range(n):
            x = rng.uniform(-26, 26)
            z = rng.uniform(Z_FROM - r["min_depth"], Z_TO + 1)
            if z > Z_FROM - r["min_depth"]:
                continue
            d = 0 if z > -12 else (1 if z > -20 else 2)
            objs = _import(os.path.join(OUT, r["lods"][d]))
            roots = [o for o in objs if o.parent is None]
            s_ = rng.uniform(0.85, 1.15)
            for o in roots:
                o.scale = (s_, s_, s_)
                o.location = (x, -z, ghgt(x, z) - 0.05)
                if r["rotate"]:
                    o.rotation_mode = "XYZ"
                    o.rotation_euler[2] = rng.uniform(0, 6.28)
    # лента на горизонте (дальше фона): две подряд и ещё одна дальше
    for k, (xo, yo) in enumerate(((-40, 32), (0, 32), (40, 32), (-20, 52), (20, 52))):
        objs = _import(os.path.join(OUT, recs["ridges"][k % len(recs["ridges"])]["file"]))
        for o in [o for o in objs if o.parent is None]:
            o.location = (xo, yo, 0)
    # дымка (mist) и небо
    sc.world = bpy.data.worlds.new("sky")
    sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.42, 0.55, 0.75, 1)
    bg.inputs["Strength"].default_value = 0.9
    sun = bpy.data.lights.new("sun", "SUN")
    sun.energy, sun.angle = 3.0, 0.2
    so = bpy.data.objects.new("sun", sun)
    so.rotation_euler = (math.radians(50), 0, math.radians(30))
    sc.collection.objects.link(so)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    cam.data.angle_y = math.radians(40)
    cam.data.sensor_fit = "VERTICAL"
    cam.data.clip_end = 400
    cam.location = (0, -15, 1.5 + 15 * 0.176)
    cam.rotation_euler = (math.radians(90 - 10), 0, 0)
    sc.collection.objects.link(cam)
    sc.camera = cam
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 24
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720
    sc.view_settings.view_transform = "AgX"
    sc.view_layers[0].use_pass_mist = True
    sc.world.mist_settings.start = 12
    sc.world.mist_settings.depth = 110
    sc.world.mist_settings.falloff = "LINEAR"
    ng = bpy.data.node_groups.new("comp", "CompositorNodeTree")      # Blender 5: композитор — группа узлов
    sc.compositing_node_group = ng
    sc.render.compositor_device = "CPU"
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    mul = ng.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = 0.55
    mix = ng.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["B"].default_value = (0.62, 0.66, 0.72, 1)        # цвет дымки, как FOG в игре
    go = ng.nodes.new("NodeGroupOutput")
    ng.links.new(rl.outputs["Mist"], mul.inputs[0])
    ng.links.new(mul.outputs[0], mix.inputs["Factor"])
    ng.links.new(rl.outputs["Image"], mix.inputs["A"])
    ng.links.new(mix.outputs["Result"], go.inputs[0])
    out = os.path.join(ROOT, "renders", "_review", f"backdrop_scene_{biome}.png")
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print("сцена:", out, flush=True)


# ───────────────────────── main ─────────────────────────

def main(argv):
    os.makedirs(OUT, exist_ok=True)
    biomes = [a for a in argv if a in ITEMS] or list(ITEMS)
    jpath = os.path.join(OUT, "backdrop.json")
    data = {}
    data["_comment"] = ("Фон за улицей по биомам. items: id, kind (вид), size [ш, в, г] м, lods [близко до −12 м, −12…−20, "
                        "дальше −20], per_10m2 (густота), min_depth (м вглубь от начала фона — ближе не ставить), "
                        "rotate (можно крутить вокруг вертикали), sway (узел sway качать ветром), smoke (точки выхода "
                        "дыма, координаты Godot от точки опоры), window_lit (материал window_lit — ночью светится). "
                        "ridges — ленты дальнего плана: width 40 м, края совпадают (ставить подряд), depth — вглубь "
                        "(−Z Godot), передний край — у точки опоры. birds — птицы с анимацией bird_flap.")
    if "--scene-only" in argv:
        for bm_ in biomes:
            scene(bm_)
        return
    for bm_ in biomes:
        recs, cnt = [], {}
        for it in ITEMS[bm_]:
            cnt[it["kind"]] = cnt.get(it["kind"], 0) + 1
            recs.append(build_item(bm_, it, cnt[it["kind"]]))
        rid = [ridge(bm_, k) for k in (1, 2)]
        json.dump({"items": recs, "ridges": rid}, open(os.path.join(OUT, f"_{bm_}.json"), "w"), ensure_ascii=False, indent=1)
        if "--no-preview" not in argv:
            preview(bm_)
            scene(bm_)
    if "--scene-only" in argv:
        for bm_ in biomes:
            scene(bm_)
        return
    if "--birds" in argv:
        json.dump(bird_all(), open(os.path.join(OUT, "_birds.json"), "w"), ensure_ascii=False, indent=1)
    merge(data, jpath)


def bird_all():
    return [bird(k, v) for k, v in BIRDS.items()]


def merge(data, jpath):
    """Собрать backdrop.json из частей (_<биом>.json, _birds.json) — части пишутся отдельными запусками."""
    for b in ITEMS:
        f = os.path.join(OUT, f"_{b}.json")
        if os.path.exists(f):
            data[b] = json.load(open(f))
    f = os.path.join(OUT, "_birds.json")
    if os.path.exists(f):
        data["birds"] = json.load(open(f))
    json.dump(data, open(jpath, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
