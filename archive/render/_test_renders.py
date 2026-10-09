"""Проверочный набор для карты нормалей и палитры (шаг 0). Запуск: python3 render/_test_renders.py

Рендерит в renders/_test/ (каждый — цвет + _n.png):
  test_cube_1m_idle     — куб 1×1×1 м прямо: перед и верх;
  test_cube_45_idle     — тот же куб, повёрнут на 45°: левый и правый бок;
  test_ico_idle         — многогранник ⌀1 м: грани во все стороны — удобнее всего проверять лампу в игре;
  test_palette_idle     — все цвета палитры плитками — проверка, что цвета доходят без искажений.
И сам сверяет пиксели с расчётом. В конце пишет «ВСЁ ВЕРНО» или список ошибок.
"""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _template as rt  # noqa: E402

sys.path.insert(0, os.path.join(rt.ROOT, "palette"))
import _palette  # noqa: E402

from PIL import Image  # noqa: E402

OUT = "renders/_test"
T = math.radians(rt.TILT_DEG)
errors = []


def expect_normal(n):
    """Ожидаемый цвет карты нормалей для нормали n (мир) — камера наклонена на 12° вниз."""
    x, y, z = n
    cx = x
    cy = z * math.cos(T) + y * math.sin(T)      # вверх на экране
    cz = -y * math.cos(T) + z * math.sin(T)     # на камеру
    return tuple(round((v * 0.5 + 0.5) * 255) for v in (cx, cy, cz))


def check(name, got, want, tol=2):
    ok = all(abs(a - b) <= tol for a, b in zip(got, want))
    print(f"  {'ок ' if ok else 'ОШИБКА'} {name}: {tuple(got)} (ожидается {tuple(want)})")
    if not ok:
        errors.append(name)


def palette_obj():
    mat = rt.palette_material()
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    o = bpy.context.active_object
    o.data.materials.append(mat)
    rt.paint(o, "concrete")
    bpy.ops.object.shade_flat()
    return o


def clear():
    for o in list(bpy.data.objects):
        if o.type == "MESH":
            bpy.data.objects.remove(o)


def render(name, objs):
    base = f"{OUT}/{name}"
    rt.render_pair(objs, base)
    return (Image.open(os.path.join(rt.ROOT, base + ".png")).convert("RGBA"),
            Image.open(os.path.join(rt.ROOT, base + "_n.png")).convert("RGBA"))


def main():
    rt.setup_scene()

    print("1) Куб прямо")
    cube = palette_obj()
    col, nrm = render("test_cube_1m_idle", [cube])
    w, h = nrm.size
    check("размер, px", (w, h), (200, math.ceil((1 + math.tan(T)) * rt.PX_PER_M)), tol=0)
    check("перед", nrm.getpixel((w // 2, h - 20))[:3], expect_normal((0, -1, 0)))
    check("верх", nrm.getpixel((w // 2, 10))[:3], expect_normal((0, 0, 1)))
    check("цвет бетона", col.getpixel((w // 2, h // 2))[:3], _palette.hex2rgb("#7a756c"), tol=1)

    print("2) Куб под 45°")
    cube.rotation_euler[2] = math.radians(45)
    col, nrm = render("test_cube_45_idle", [cube])
    w, h = nrm.size
    s = math.sqrt(0.5)
    check("левый бок", nrm.getpixel((w // 4, h * 3 // 4))[:3], expect_normal((-s, -s, 0)))
    check("правый бок", nrm.getpixel((w * 3 // 4, h * 3 // 4))[:3], expect_normal((s, -s, 0)))
    clear()

    print("3) Многогранник")
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.5, location=(0, 0, 0.5))
    ico = bpy.context.active_object
    ico.data.materials.append(rt.palette_material())
    rt.paint(ico, "concrete_light")
    bpy.ops.object.shade_flat()
    col, nrm = render("test_ico_idle", [ico])
    print(f"  размер {nrm.size} — граней {len(ico.data.polygons)}, проверка глазами/в игре")
    clear()

    print("4) Палитра плитками")
    mat = rt.palette_material()
    tiles = []
    cells = list(_palette._cells())
    for r, c, (name, hx, _) in cells:
        bpy.ops.mesh.primitive_plane_add(size=0.2, location=(c * 0.25, 0, -r * 0.3))
        p = bpy.context.active_object
        p.rotation_euler[0] = math.radians(90)  # лицом к камере (−Y)
        p.data.materials.append(mat)
        rt.paint(p, name)
        tiles.append((p, r, c, name, hx))
    col, nrm = render("test_palette_idle", [t[0] for t in tiles])
    # центр каждой плитки на картинке: проецируем центр плоскости
    rot = rt.camera_rotation().to_3x3().transposed()
    pts = [rot @ t[0].matrix_world.translation for t in tiles]
    allp = [rot @ (t[0].matrix_world @ v.co) for t in tiles for v in t[0].data.vertices]
    xmin = min(p.x for p in allp); ymin = min(p.y for p in allp)
    W, H = col.size
    bad = 0
    for (p, r, c, name, hx), pc in zip(tiles, pts):
        px = int((pc.x - xmin) * rt.PX_PER_M)
        py = H - 1 - int((pc.y - ymin) * rt.PX_PER_M * rt.V_STRETCH)
        got = col.getpixel((px, py))[:3]
        if any(abs(a - b) > 1 for a, b in zip(got, _palette.hex2rgb(hx))):
            bad += 1
            print(f"  ОШИБКА {name}: {got} вместо {hx}")
    if bad:
        errors.append("палитра")
    print(f"  цветов проверено: {len(tiles)}, неверных: {bad}")

    print("\nВСЁ ВЕРНО" if not errors else f"\nОШИБКИ: {', '.join(errors)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
