"""Перенос анимаций Mixamo на скелет тел Tripo (кости те же по именам, но в позе покоя смотрят по-другому).

  python3 tools/anims_retarget.py <анимации.glb> <тело_idle.glb> <выход.glb>

Для каждой кости: поворот в мире = поворот кости-источника в мире × поправка (разница поз покоя), записывается как
обычный ключ кости тела. Корень (Hips) двигается так же, как у источника, в масштабе роста (высота Hips в покое).
Итог — скелет тела + все действия (без сетки; крошечный треугольник на Hips — чтобы кости вышли скелетом).
Подходит ко всем телам Tripo со скелетом (у них одна поза покоя и кости).
"""
import os
import sys

import bpy
from mathutils import Matrix, Vector


def import_glb(path):
    before_o, before_a = set(bpy.data.objects), set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=path)
    objs = [o for o in bpy.data.objects if o not in before_o]
    arm = next(o for o in objs if o.type == "ARMATURE")
    for o in objs:                                        # сетки и формы показа костей не нужны
        if o.type == "MESH":
            bpy.data.objects.remove(o)
    return arm, [a for a in bpy.data.actions if a not in before_a]


def order(arm):
    out = []

    def walk(b):
        out.append(b.name)
        for c in b.children:
            walk(c)
    for b in arm.data.bones:
        if b.parent is None:
            walk(b)
    return out


PREFER = ("Spine", "Neck", "Head", "Arm", "ForeArm", "Hand", "HandMiddle1", "Leg", "Foot", "ToeBase")


def main_child(bone, srcarm):
    """Следующий сустав по цепочке (у развилок — по позвоночнику / среднему пальцу); есть и у источника."""
    kids = [c for c in bone.children if c.name in srcarm.data.bones]
    if not kids:
        return None
    if len(kids) == 1:
        return kids[0].name
    for p in PREFER:
        for c in kids:
            if c.name.split(":")[-1].startswith(p) and "Shoulder" not in c.name:
                return c.name
    return kids[0].name


def key_all(act, arm, data_path, n_idx, frames, values):
    """values: [[v_idx0, v_idx1, …] по кадрам] → кривые действия."""
    for i in range(n_idx):
        try:
            fc = act.fcurve_ensure_for_datablock(arm, data_path, index=i)
        except AttributeError:
            fc = act.fcurves.new(data_path, index=i)
        fc.keyframe_points.add(len(frames))
        co = []
        for f, v in zip(frames, values):
            co += [f, v[i]]
        fc.keyframe_points.foreach_set("co", co)
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
        fc.update()


def main(src, body, out):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = 30
    tgt, junk = import_glb(body)
    for a in junk:
        bpy.data.actions.remove(a)
    srcarm, acts = import_glb(src)
    tgt.animation_data_create()
    srcarm.animation_data_create()
    for tr in list(srcarm.animation_data.nla_tracks):
        srcarm.animation_data.nla_tracks.remove(tr)
    names = [b for b in order(tgt) if b in srcarm.data.bones]
    hips = next(b for b in names if b.endswith("Hips"))
    Sw, Tw = srcarm.matrix_world, tgt.matrix_world
    Tw_inv = Tw.inverted()
    # поправка поз покоя (в мире, только поворот)
    # + поворот кости тела так, чтобы в покое она смотрела на следующий сустав ровно как у Mixamo: у скелетов Tripo
    #   в покое локти, колени, спина чуть согнуты, и без этого сгиб прибавлялся к каждой анимации (локоть «пережат»)
    off = {}
    for b in names:
        s_rest = (Sw @ srcarm.data.bones[b].matrix_local).to_quaternion()
        t_rest = (Tw @ tgt.data.bones[b].matrix_local).to_quaternion()
        c = main_child(tgt.data.bones[b], srcarm)
        if c and b != hips:
            s_dir = (Sw @ srcarm.data.bones[c].head_local) - (Sw @ srcarm.data.bones[b].head_local)
            t_dir = (Tw @ tgt.data.bones[c].head_local) - (Tw @ tgt.data.bones[b].head_local)
            if s_dir.length > 1e-5 and t_dir.length > 1e-5:
                t_rest = t_dir.normalized().rotation_difference(s_dir.normalized()) @ t_rest
        off[b] = s_rest.inverted() @ t_rest
    s_h0 = (Sw @ srcarm.data.bones[hips].head_local)
    t_h0 = (Tw @ tgt.data.bones[hips].head_local)
    k_h = t_h0.z / s_h0.z                                  # рост: высота Hips в покое
    rel = {b: (tgt.data.bones[b].parent.matrix_local.inverted() @ tgt.data.bones[b].matrix_local
               if tgt.data.bones[b].parent else tgt.data.bones[b].matrix_local) for b in names}
    made = []
    for act in sorted(acts, key=lambda a: a.name):
        name = act.name.split("_Armature")[0] if "_Armature" in act.name else act.name
        act.name = "src_" + name                            # имя освободить для нового действия
        srcarm.animation_data.action = act
        if srcarm.animation_data.action_slot is None and len(act.slots):
            srcarm.animation_data.action_slot = act.slots[0]
        f0, f1 = (int(round(x)) for x in act.frame_range)
        frames = list(range(f0, f1 + 1))
        rot = {b: [] for b in names}
        loc = []
        for f in frames:
            sc.frame_set(f)
            pose = {}
            for b in names:                                # от корня к концам
                want_w = (Sw @ srcarm.pose.bones[b].matrix).to_quaternion() @ off[b]
                want = (Tw_inv.to_quaternion() @ want_w).to_matrix().to_4x4()
                pb = tgt.data.bones[b]
                if pb.parent is None:
                    parent_m = Matrix.Identity(4)
                else:                                      # родитель без ключей (neutral_bone) — в покое
                    parent_m = pose.get(pb.parent.name, pb.parent.matrix_local)
                base = parent_m @ rel[b]
                if b == hips:                              # корень — ещё и смещение
                    s_h = Sw @ srcarm.pose.bones[b].head
                    want.translation = Tw_inv @ (t_h0 + (s_h - s_h0) * k_h)
                else:
                    want.translation = base.translation
                basis = base.inverted() @ want
                pose[b] = want
                q = basis.to_quaternion()
                rot[b].append((q.w, q.x, q.y, q.z))
                if b == hips:
                    loc.append(tuple(basis.translation))
        for b in names:                                    # знак кватерниона — без скачков между кадрами
            qs = rot[b]                                    # (q и −q — один поворот, но игра между кадрами
            for i in range(1, len(qs)):                    #  крутила бы кость «длинным путём» — рывок)
                if sum(x * y for x, y in zip(qs[i], qs[i - 1])) < 0:
                    qs[i] = tuple(-x for x in qs[i])
        new = bpy.data.actions.new(name)
        new.use_fake_user = True
        tgt.animation_data.action = new
        for b in names:
            key_all(new, tgt, f'pose.bones["{b}"].rotation_quaternion', 4, frames, rot[b])
        key_all(new, tgt, f'pose.bones["{hips}"].location', 3, frames, loc)
        tgt.animation_data.action = None
        made.append(new)
        print(f"[{name}] {len(frames)} кадров", flush=True)
    for a in acts:
        bpy.data.actions.remove(a)
    bpy.data.objects.remove(srcarm)
    for a in made:
        tr = tgt.animation_data.nla_tracks.new()
        tr.name = a.name
        st = tr.strips.new(a.name, int(a.frame_range[0]), a)
        try:
            st.action_slot = a.slots[0]
        except (AttributeError, IndexError):
            pass
        tr.mute = True
    hp = Tw @ tgt.data.bones[hips].head_local
    me = bpy.data.meshes.new("skin_anchor")
    me.from_pydata([hp, hp + Vector((0.001, 0, 0)), hp + Vector((0, 0, 0.001))], [], [(0, 1, 2)])
    dummy = bpy.data.objects.new("skin_anchor", me)
    sc.collection.objects.link(dummy)
    dummy.vertex_groups.new(name=hips).add([0, 1, 2], 1.0, "REPLACE")
    dummy.modifiers.new("Armature", "ARMATURE").object = tgt
    dummy.parent = tgt
    dummy.matrix_parent_inverse = tgt.matrix_world.inverted()
    bpy.ops.object.select_all(action="DESELECT")
    tgt.select_set(True)
    dummy.select_set(True)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", use_selection=True, export_yup=True,
                              export_animations=True, export_animation_mode="NLA_TRACKS", export_skins=True)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import glb_quat_fix
    import glb_strip_tracks                                 # только повороты (+ таз) — место костей у каждого своё
    glb_quat_fix.fix(out)
    glb_strip_tracks.strip(out)
    print(f"→ {out}: {len(made)} действий, {os.path.getsize(out) / 1e6:.2f} МБ (рост ×{k_h:.3f})", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:4])
