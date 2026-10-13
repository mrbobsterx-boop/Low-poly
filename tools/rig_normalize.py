"""Выровнять позу покоя скелета персонажа по эталону (тело body_m_rig), чтобы общие анимации
(export/anim/anims_mixamo.glb) ложились одинаково на всех.

  python3 tools/rig_normalize.py <персонаж_idle.glb> [<ещё…>] [--ref export/body_m_rig_idle.glb]

Tripo строит каждому персонажу свой скелет Mixamo: кости те же, но в позе покоя руки, ноги и пальцы чуть под другим
углом. Анимация хранит повороты костей в готовом виде, поэтому на «чужой» позе покоя рука, например, задирается.
Здесь каждая кость персонажа поворачивается так, чтобы смотреть в мире ровно как у эталона (длина костей — своя),
сетка деформируется вместе со скелетом, и это становится новой позой покоя. Файл перезаписывается.
"""
import os
import sys

import bpy
from mathutils import Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def ref_rest(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
    return {b.name: (arm.matrix_world @ b.matrix_local).to_quaternion() for b in arm.data.bones}


def order(arm):
    out = []

    def walk(b):
        out.append(b)
        for c in b.children:
            walk(c)
    for b in arm.data.bones:
        if b.parent is None:
            walk(b)
    return out


def normalize(path, ref):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    sc = bpy.context.scene
    arm = next(o for o in sc.objects if o.type == "ARMATURE")
    for pb in arm.pose.bones:                                  # форма показа костей (Icosphere) — не часть модели
        if pb.custom_shape:
            bpy.data.objects.remove(pb.custom_shape)
            break
    meshes = [o for o in sc.objects if o.type == "MESH" and o.find_armature() == arm]
    aw_inv = arm.matrix_world.to_quaternion().inverted()
    pose, n = {}, 0
    for b in order(arm):
        rel = b.parent.matrix_local.inverted() @ b.matrix_local if b.parent else b.matrix_local
        parent_m = pose.get(b.parent.name, b.parent.matrix_local) if b.parent else Matrix.Identity(4)
        base = parent_m @ rel
        if b.name in ref:
            want = (aw_inv @ ref[b.name]).to_matrix().to_4x4()
            want.translation = base.translation
            n += 1
        else:
            want = base
        pose[b.name] = want
        pb = arm.pose.bones[b.name]
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = (base.inverted() @ want).to_quaternion()
        pb.location = (0, 0, 0)
    bpy.context.view_layer.update()
    # сетку — в новую позу, затем поза → покой
    for m in meshes:
        mod = next(md for md in m.modifiers if md.type == "ARMATURE")
        name = mod.name
        bpy.context.view_layer.objects.active = m
        bpy.ops.object.modifier_apply(modifier=name)
        md = m.modifiers.new(name, "ARMATURE")
        md.object = arm
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="POSE")
    bpy.ops.pose.armature_apply(selected=False)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True)
    for m in meshes:
        m.select_set(True)
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_yup=True,
                              export_animations=False, export_skins=True, export_image_format="JPEG",
                              export_jpeg_quality=85)
    print(f"[{os.path.basename(path)}] выровнено костей: {n}, {os.path.getsize(path) / 1e6:.2f} МБ", flush=True)


def main(argv):
    ref_path = os.path.join(ROOT, "export", "body_m_rig_idle.glb")
    if "--ref" in argv:
        ref_path = argv[argv.index("--ref") + 1]
    files = [a for a in argv if not a.startswith("--") and a != ref_path]
    ref = ref_rest(ref_path)
    for f in files:
        normalize(f, ref)


if __name__ == "__main__":
    main(sys.argv[1:])
