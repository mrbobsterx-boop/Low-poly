"""Персонажи из Tripo со скелетом (Mixamo) и анимациями → export/<имя>_idle.glb (docs/TRIPO_CHARACTERS.md).
Скелет и все анимации сохраняются: меняется только корневой объект (поворот, масштаб, положение), сетка облегчается
(≤ 15 000 треугольников на модель), текстуры 1024, без блеска.

  python3 tools/char_process.py tripo/char_m_police.glb [ещё…] [--rot 270] [--height 1.8] [--out export]

Поворот — как у остальных моделей Tripo (перед вбок → обычно 270°; поправка — tripo/rotate.json по имени файла).
"""
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tripo_process as T  # noqa: E402

LIMIT = 15000


def world_bbox(meshes):
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for m in meshes:
        ev = m.evaluated_get(dg)
        pts += [ev.matrix_world @ v.co for v in ev.data.vertices]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


def process(path, out_dir, rot, height, limit=LIMIT):
    name = os.path.basename(path)[:-4]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    sc = bpy.context.scene
    arms = [o for o in sc.objects if o.type == "ARMATURE"]
    meshes = [o for o in sc.objects if o.type == "MESH"]
    roots = [o for o in sc.objects if o.parent is None]
    n_anim = len(bpy.data.actions)
    for a in arms:
        a.data.pose_position = "REST"             # мерить в позе покоя (T-поза), не в кадре анимации
    bpy.context.view_layer.update()
    t0 = sum(T.tris(m) for m in meshes)
    # облегчить: на каждую сетку — пропорционально её доле (веса костей Decimate сохраняет)
    for m in meshes:
        share = T.tris(m) / max(t0, 1)
        T.decimate(m, max(200, int(limit * share * 0.98)))
    t1 = sum(T.tris(m) for m in meshes)
    for m in meshes:
        T.fix_materials(m, 1024)
    # поворот, масштаб, положение — только у корней (скелет и анимации не трогаем)
    lo, hi = world_bbox(meshes)
    k = height / float(hi.z - lo.z)
    R = Matrix.Rotation(math.radians(rot), 4, "Z")
    for r in roots:
        r.matrix_world = R @ Matrix.Scale(k, 4) @ r.matrix_world
    bpy.context.view_layer.update()
    lo, hi = world_bbox(meshes)
    shift = Matrix.Translation(Vector((-(lo.x + hi.x) / 2, -(lo.y + hi.y) / 2, -lo.z)))
    for r in roots:
        r.matrix_world = shift @ r.matrix_world
    bpy.context.view_layer.update()
    lo, hi = world_bbox(meshes)
    for a in arms:
        a.data.pose_position = "POSE"
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, name + "_idle.glb")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", use_selection=True, export_yup=True,
                              export_animations=True, export_skins=True, export_image_format="JPEG",
                              export_jpeg_quality=85)
    mb = os.path.getsize(out) / 1e6
    dims = hi - lo
    print(f"[{name}_idle] скелет: {'да' if arms else 'НЕТ'}, анимаций {n_anim}, треугольников {t0} → {t1}, "
          f"{dims.x * 100:.0f}×{dims.y * 100:.0f}×{dims.z * 100:.0f} см, поворот {rot}°, {mb:.2f} МБ", flush=True)
    return {"src": name + ".glb", "rig": bool(arms), "animations": n_anim, "tris_before": t0, "tris_after": t1,
            "size_cm": [dims.x * 100, dims.y * 100, dims.z * 100], "rotate": rot, "mb": mb}


def main(argv):
    rot_cfg = T.load_json("rotate.json", {})
    out_dir = os.path.join(T.ROOT, "export")
    height, rot_force, files, i = 1.8, None, [], 0
    while i < len(argv):
        a = argv[i]
        if a == "--rot":
            rot_force, i = float(argv[i + 1]), i + 2
        elif a == "--height":
            height, i = float(argv[i + 1]), i + 2
        elif a == "--out":
            out_dir, i = argv[i + 1], i + 2
        else:
            files.append(a)
            i += 1
    for f in files:
        stem = os.path.basename(f)[:-4]
        rot = rot_force if rot_force is not None else rot_cfg.get(stem, 270)
        process(f, out_dir, rot, height)


if __name__ == "__main__":
    main(sys.argv[1:])
