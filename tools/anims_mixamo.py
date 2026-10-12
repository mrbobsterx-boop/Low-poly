"""Анимации людей из Mixamo (FBX) → один файл export/anim/anims_mixamo.glb (скелет + все действия, без сетки, 30 кадров/с).
Порядок и имена — docs/ANIMATIONS.md.

  python3 tools/anims_mixamo.py <папка с FBX> [<папка наборов zip, распакованных>] [--out export/anim/anims_mixamo.glb]

Для каждого FBX: импорт, сетка удаляется, действие получает имя из таблицы NAMES. Ходьба, бег, ползание (LOCO) —
«на месте»: если корень (Hips) уезжает по горизонтали больше 0,2 м, движение Hips по горизонтали обнуляется (высота
остаётся). Сантиметры FBX → метры. Все действия — дорожками NLA одного скелета (у всех Mixamo кости одни: mixamorig:…). В файле — крошечный
треугольник на Hips, иначе glTF пишет кости обычными узлами, а не скелетом.
"""
import json
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# файл (без .fbx; из наборов — «Набор/файл») → имя действия
NAMES = {
    "Idle (1)": "idle", "Unarmed Idle Looking Ver. 2": "idle_look",
    "Walking": "walk", "Walking (1)": "walk_b", "Walking (2)": "walk_c", "Walk Forward Arc Right": "walk_turn",
    "Jogging": "jog", "Fast Run": "run", "Strafe": "strafe", "Crouched Sneaking Left": "sneak",
    "Crouch To Stand": "crouch_to_stand", "Standing Up": "stand_up", "Kneeling Down": "kneel", "Crawling": "crawl",
    "Picking Up Object": "pick_up", "Unarmed Grab Torch From Floor": "pick_up_floor", "Pick Fruit": "harvest",
    "Carrying Turn": "carry_turn", "Digging": "dig", "Working On Device": "work_table",
    "Bartending": "work_counter", "Bartending (1)": "work_counter_b",
    "Looking Through Files Low": "search_low", "Rummaging": "search", "Open Door Outwards": "open_door",
    "Opening": "open_box", "Push": "push", "Drinking": "drink", "Sleeping Idle": "sleep",
    "Sitting Talking": "sit_talk", "Sitting Rubbing Arm": "sit_injured", "Talking": "talk", "Talking (1)": "talk_b",
    "Taunt": "taunt", "Climbing Ladder": "climb", "Climbing Down": "climb_down", "Climbing": "climb_wall",
    "Freehang Climb": "hang_climb", "Jump": "jump", "Jumping Down": "jump_down", "Swimming": "swim",
    "Floating": "float", "Injured Walk": "injured_walk", "Injured Walk (1)": "injured_walk_b",
    "Injured Walking": "injured_walk_c", "Injured Run": "injured_run", "Head Hit": "hit_head", "Rib Hit": "hit",
    "Standing React Large From Front": "hit_big", "Dying": "death", "Standing Death Left 01": "death_b",
    "Illegal Elbow Punch": "punch", "Punching Bag": "punch_combo", "Standing Melee Attack Downward": "melee",
    "Double Dagger Stab": "stab", "Shooting Gun": "pistol_shoot", "Gunplay": "gunplay",
    "Walk With Rifle": "rifle_walk", "Shooting Arrow": "bow_shoot", "Entry": "entry",
    "Zombie Neck Bite": "zombie_neck_bite",
    "Scary Zombie Pack/zombie idle": "zombie_idle", "Scary Zombie Pack/zombie walk": "zombie_walk",
    "Scary Zombie Pack/zombie run": "zombie_run", "Scary Zombie Pack/zombie attack": "zombie_attack",
    "Scary Zombie Pack/zombie biting": "zombie_bite", "Scary Zombie Pack/zombie biting (2)": "zombie_bite_b",
    "Scary Zombie Pack/zombie crawl": "zombie_crawl", "Scary Zombie Pack/running crawl": "zombie_crawl_run",
    "Scary Zombie Pack/zombie death": "zombie_death", "Scary Zombie Pack/zombie dying": "zombie_dying",
    "Scary Zombie Pack/zombie scream": "zombie_scream",
    "Creature NPC Pack/mutant idle": "mutant_idle", "Creature NPC Pack/mutant breathing idle": "mutant_idle_b",
    "Creature NPC Pack/mutant walking": "mutant_walk", "Creature NPC Pack/mutant run": "mutant_run",
    "Creature NPC Pack/mutant swiping": "mutant_swipe", "Creature NPC Pack/mutant jumping": "mutant_jump",
    "Creature NPC Pack/mutant dying": "mutant_death", "Creature NPC Pack/mutant flexing muscles": "mutant_roar",
    "Creature NPC Pack/mutant left turn 45": "mutant_turn_l", "Creature NPC Pack/mutant right turn 45": "mutant_turn_r",
    "Creature NPC Pack/left turn 45": "mutant_turn_l_b", "Creature NPC Pack/mutant right turn 45 (2)": "mutant_turn_r_b",
    "Action Adventure Pack/idle": "aa_idle_1", "Action Adventure Pack/idle (2)": "aa_idle_2",
    "Action Adventure Pack/idle (3)": "aa_idle_3", "Action Adventure Pack/idle (4)": "aa_idle_4",
    "Action Adventure Pack/idle (5)": "aa_idle_5", "Action Adventure Pack/walking": "aa_walk",
    "Action Adventure Pack/running": "aa_run", "Action Adventure Pack/run to stop": "run_stop",
    "Action Adventure Pack/crouched sneaking left": "sneak_l", "Action Adventure Pack/crouched sneaking right": "sneak_r",
    "Action Adventure Pack/left cover sneak": "cover_sneak_l", "Action Adventure Pack/right cover sneak": "cover_sneak_r",
    "Action Adventure Pack/stand to cover": "to_cover", "Action Adventure Pack/stand to cover (2)": "to_cover_b",
    "Action Adventure Pack/cover to stand": "from_cover", "Action Adventure Pack/cover to stand (2)": "from_cover_b",
    "Action Adventure Pack/falling idle": "fall", "Action Adventure Pack/falling to roll": "fall_roll",
    "Action Adventure Pack/hard landing": "land_hard", "Action Adventure Pack/jumping up": "jump_up",
    "Action Adventure Pack/left turn": "turn_l", "Action Adventure Pack/right turn": "turn_r",
}
SKIP = {"Idle": "второй idle со скином (больше) — взят «Idle (1)»",
        "Scary Zombie Pack/zombie neck bite": "уже есть отдельным файлом (Zombie Neck Bite)",
        "Scary Zombie Pack/X Bot": "манекен Mixamo, не анимация", "Action Adventure Pack/X Bot": "манекен Mixamo, не анимация"}
# «на месте»: ходьба, бег, ползание и т. п. — корень не должен уезжать
LOCO = {"walk", "walk_b", "walk_c", "walk_turn", "jog", "run", "strafe", "sneak", "sneak_l", "sneak_r", "crawl",
        "injured_walk", "injured_walk_b", "injured_walk_c", "injured_run", "rifle_walk", "swim", "zombie_walk",
        "zombie_run", "zombie_crawl", "zombie_crawl_run", "mutant_walk", "mutant_run", "aa_walk", "aa_run",
        "cover_sneak_l", "cover_sneak_r"}
TRAVEL_MAX = 0.2


def hips_travel(arm, act, hips):
    """Сдвиг Hips по горизонтали (м, в мире) от первого до последнего кадра."""
    arm.animation_data.action = act
    if arm.animation_data.action_slot is None and len(act.slots):
        arm.animation_data.action_slot = act.slots[0]
    f0, f1 = (int(x) for x in act.frame_range)
    sc = bpy.context.scene
    pts = []
    for f in (f0, f1):
        sc.frame_set(f)
        pts.append(arm.matrix_world @ arm.pose.bones[hips].head)
    d = pts[1] - pts[0]
    return Vector((d.x, d.y)).length


def fcurves(act):
    try:
        return [fc for l in act.layers for s in l.strips for cb in s.channelbags for fc in cb.fcurves]
    except AttributeError:
        return list(act.fcurves)


def in_place(arm, act, hips):
    """Обнулить движение Hips по горизонтали: каналы location, чья ось кости в мире — не вертикаль."""
    rest = (arm.matrix_world @ arm.data.bones[hips].matrix_local).to_3x3()
    vert = max(range(3), key=lambda i: abs(rest.col[i].z))
    for fc in fcurves(act):
        if fc.data_path == f'pose.bones["{hips}"].location' and fc.array_index != vert:
            v0 = fc.keyframe_points[0].co[1] if len(fc.keyframe_points) else 0.0
            for kp in fc.keyframe_points:
                kp.co[1] = v0
                kp.handle_left[1] = kp.handle_right[1] = v0
            fc.update()


def main(argv):
    out = os.path.join(ROOT, "export", "anim", "anims_mixamo.glb")
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    dirs = [a for a in argv if not a.startswith("--") and a != out]
    files = []
    for d in dirs:
        for dp, _, fs in os.walk(d):
            for f in sorted(fs):
                if f.lower().endswith(".fbx"):
                    rel = os.path.relpath(os.path.join(dp, f), d)[:-4]
                    files.append((rel, os.path.join(dp, f)))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = 30
    base, hips, info = None, None, {"actions": {}, "skipped": {}, "unknown": [], "fixed": {}, "bones_differ": {}}
    for rel, path in files:
        if rel in SKIP:
            info["skipped"][rel] = SKIP[rel]
            continue
        name = NAMES.get(rel)
        if not name:
            info["unknown"].append(rel)
            continue
        before_obj, before_act = set(bpy.data.objects), set(bpy.data.actions)
        bpy.ops.import_scene.fbx(filepath=path, use_anim=True, automatic_bone_orientation=False)
        new = [o for o in bpy.data.objects if o not in before_obj]
        acts = [a for a in bpy.data.actions if a not in before_act]
        arm = next(o for o in new if o.type == "ARMATURE")
        act = max(acts, key=lambda a: len(fcurves(a)))
        for a in acts:
            if a is not act:
                bpy.data.actions.remove(a)
        act.name = name
        act.use_fake_user = True
        bones = {b.name for b in arm.data.bones}
        if base is None:
            base = arm
            base.name = "Armature"
            hips = next(b.name for b in arm.data.bones if b.name.endswith("Hips"))
            info["bones"] = sorted(bones)
            for o in new:
                if o is not base:
                    bpy.data.objects.remove(o)
        else:
            if bones != set(info["bones"]):
                info["bones_differ"][name] = sorted(bones ^ set(info["bones"]))
            for o in new:
                bpy.data.objects.remove(o)
        base.animation_data_create()
        if name in LOCO:
            t = hips_travel(base, act, hips)
            if t > TRAVEL_MAX:
                in_place(base, act, hips)
                info["fixed"][name] = round(t, 2)
        f0, f1 = act.frame_range
        info["actions"][name] = {"src": rel, "frames": int(f1 - f0) + 1, "sec": round((f1 - f0) / 30, 2)}
        print(f"[{name}] ← {rel}: {int(f1 - f0) + 1} кадров" + (f", корень уезжал {info['fixed'][name]} м → на месте"
                                                               if name in info["fixed"] else ""), flush=True)
    # FBX Mixamo — в сантиметрах (у скелета масштаб 0,01) → в метры, как у тел Tripo: масштаб и поворот — в кости,
    # смещения в действиях (location) умножить на тот же масштаб
    base.animation_data.action = None
    k = base.scale[0]
    bpy.ops.object.select_all(action="DESELECT")
    base.select_set(True)
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    for name in info["actions"]:
        for fc in fcurves(bpy.data.actions[name]):
            if fc.data_path.endswith(".location"):
                for kp in fc.keyframe_points:
                    kp.co[1] *= k
                    kp.handle_left[1] *= k
                    kp.handle_right[1] *= k
                fc.update()
    info["scale_fbx"] = k
    # все действия — дорожками NLA одного скелета
    for name in sorted(info["actions"]):
        act = bpy.data.actions[name]
        tr = base.animation_data.nla_tracks.new()
        tr.name = name
        st = tr.strips.new(name, int(act.frame_range[0]), act)
        try:
            st.action_slot = act.slots[0]
        except (AttributeError, IndexError):
            pass
        tr.mute = True
    # крошечный треугольник на Hips — чтобы кости вышли скелетом
    hp = base.matrix_world @ base.data.bones[hips].head_local
    me = bpy.data.meshes.new("skin_anchor")
    me.from_pydata([hp, hp + Vector((0.001, 0, 0)), hp + Vector((0, 0, 0.001))], [], [(0, 1, 2)])
    dummy = bpy.data.objects.new("skin_anchor", me)
    sc.collection.objects.link(dummy)
    dummy.vertex_groups.new(name=hips).add([0, 1, 2], 1.0, "REPLACE")
    dummy.modifiers.new("Armature", "ARMATURE").object = base
    dummy.parent = base
    dummy.matrix_parent_inverse = base.matrix_world.inverted()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    base.select_set(True)
    dummy.select_set(True)
    bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", use_selection=True, export_yup=True,
                              export_animations=True, export_animation_mode="NLA_TRACKS", export_skins=True,
                              export_force_sampling=True, export_frame_step=1)
    info["mb"] = round(os.path.getsize(out) / 1e6, 2)
    json.dump(info, open(out[:-4] + "_info.json", "w"), ensure_ascii=False, indent=1)
    print(f"→ {out}: {len(info['actions'])} действий, {info['mb']} МБ; на месте исправлено: {len(info['fixed'])}; "
          f"неизвестные файлы: {info['unknown']}; кости отличаются: {list(info['bones_differ'])}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
