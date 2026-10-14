"""Выровнять оси костей персонажа по эталону (body_m_rig) — БЕЗ изменения сетки.

  python3 tools/rig_roll.py <персонаж_idle.glb> [<ещё…>] [--ref export/body_m_rig_idle.glb] [--out <папка>]

Tripo строит каждому свой скелет: кости те же, но кость повёрнута вокруг своей оси (roll) по-разному — до 180°.
Игра ставит повороты из общей анимации прямо в кости, и при чужом roll рука выворачивалась / задиралась.
Здесь меняется только roll каждой кости (вокруг её же оси): сетка остаётся родной, как сделал Tripo, без «запекания»
позы (прежний rig_normalize.py переставлял руки в позу эталона и сплющивал сетку в плечах и локтях).
Сравнение честное: эталонную кость сначала поворачиваем так, чтобы она смотрела туда же, куда кость персонажа.
"""
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def ref_rest(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
    return {b.name: arm.matrix_world.to_3x3() @ b.matrix_local.to_3x3() for b in arm.data.bones}


def fix(path, ref, out):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    sc = bpy.context.scene
    arm = next(o for o in sc.objects if o.type == "ARMATURE")
    for pb in arm.pose.bones:                                  # форма показа костей (Icosphere) — не часть модели
        if pb.custom_shape:
            bpy.data.objects.remove(pb.custom_shape)
            break
    meshes = [o for o in sc.objects if o.type == "MESH" and o.find_armature() == arm]
    aw = arm.matrix_world.to_3x3()
    aw_inv = aw.inverted()
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    worst = 0.0
    for eb in arm.data.edit_bones:
        if eb.name not in ref:
            continue
        R = ref[eb.name]
        y_ref = R.col[1].normalized()
        y_me = (aw @ eb.matrix.to_3x3()).col[1].normalized()
        z_want = (y_ref.rotation_difference(y_me).to_matrix() @ R).col[2]    # эталон, повёрнутый на мою кость
        z_me = (aw @ eb.matrix.to_3x3()).col[2].normalized()
        worst = max(worst, math.degrees(z_me.angle(z_want.normalized())))
        eb.align_roll(aw_inv @ z_want)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True)
    for m in meshes:
        m.select_set(True)
    dst = os.path.join(out, os.path.basename(path)) if out else path
    bpy.ops.export_scene.gltf(filepath=dst, export_format="GLB", use_selection=True, export_yup=True,
                              export_animations=False, export_skins=True, export_image_format="JPEG",
                              export_jpeg_quality=85)
    print(f"[{os.path.basename(path)}] roll выровнен (было до {worst:.0f}°), сетка не тронута, "
          f"{os.path.getsize(dst) / 1e6:.2f} МБ", flush=True)


def main(argv):
    ref_path = os.path.join(ROOT, "export", "body_m_rig_idle.glb")
    out = None
    if "--ref" in argv:
        ref_path = argv[argv.index("--ref") + 1]
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    files = [a for a in argv if not a.startswith("--") and a not in (ref_path, out)]
    ref = ref_rest(ref_path)
    for f in files:
        fix(f, ref, out)


if __name__ == "__main__":
    main(sys.argv[1:])
