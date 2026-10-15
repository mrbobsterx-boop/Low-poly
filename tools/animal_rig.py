"""Скелет и анимации животных (без Tripo/Mixamo — у них нет рига для зверей).

  python3 tools/animal_rig.py [имена…] [--preview]      (без имён — все животные из ANIMALS)

По форме сетки находятся лапы (по следам на полу), туловище, шея с головой, хвост, у птиц — крылья; ставятся кости,
каждой вершине даются веса ближайших костей. Анимации делаются по формулам (походка, бег, атака…) и пишутся в тот же
`export/<имя>_idle.glb`: в покое модель стоит как раньше, анимации — внутри файла (по именам).
Исходник без костей хранится в `tripo/static/<имя>_idle.glb` (не в git; при первом запуске копируется из export/).
Скорость «на месте» для каждой ходьбы/бега — в `export/anim/animals_info.json` (`speed_mps`).
--preview — лист кадров со светом: renders/_review/animals_<дата>.jpg.
"""
import json
import math
import os
import shutil
import sys

import bpy
import numpy as np
from mathutils import Matrix, Quaternion, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FPS = 30

QUAD = ["dog_feral_odinochnaya", "dog_husky", "dog_raider", "dog_rottweiler", "dog_shepherd", "dog_terrier",
        "dog_thin", "dog_zombie", "wolf", "bear_black", "bear_brown", "bear_mutant", "deer_red", "deer_roe",
        "deer_white", "moose_bull", "moose_cow", "moose_mutant", "rat_grey", "rat_pest_krysa"]
HOP = ["rabbit_grey", "rabbit_hare", "rabbit_white", "rabbit_wild_krolik"]
BIRDS = ["crow", "pigeon", "seagull", "vulture", "owl", "duck"]
ANIMALS = QUAD + HOP + BIRDS


# ───────────────────────── загрузка ─────────────────────────

def load(name):
    src = os.path.join(ROOT, "tripo", "static", f"{name}_idle.glb")
    if not os.path.exists(src):
        os.makedirs(os.path.dirname(src), exist_ok=True)
        shutil.copy(os.path.join(ROOT, "export", f"{name}_idle.glb"), src)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=src)
    ms = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    for o in ms:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
    bpy.ops.object.select_all(action="DESELECT")
    for o in ms:
        o.select_set(True)
    bpy.context.view_layer.objects.active = ms[0]
    if len(ms) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for o in list(bpy.context.scene.objects):
        if o != obj:
            bpy.data.objects.remove(o)
    return obj


def verts(obj):
    a = np.empty(len(obj.data.vertices) * 3)
    obj.data.vertices.foreach_get("co", a)
    return a.reshape(-1, 3)


def V(*a):
    return Vector(tuple(float(x) for x in a))


# ───────────────────────── разметка: четвероногие ─────────────────────────

def quad_layout(P):
    mn, mx = P.min(0), P.max(0)
    H, L, W = mx[2] - mn[2], mx[1] - mn[1], mx[0] - mn[0]
    xc, z0 = (mn[0] + mx[0]) / 2, mn[2]
    g = P[P[:, 2] < z0 + 0.08 * H]
    ymid = (g[:, 1].min() + g[:, 1].max()) / 2
    feet = {}
    for side, sx in (("L", 1), ("R", -1)):
        for part, cond in (("F", g[:, 1] < ymid), ("B", g[:, 1] >= ymid)):
            m = cond & ((g[:, 0] - xc) * sx > 0)
            feet[part + side] = g[m].mean(0) if m.sum() > 3 else np.array([xc + sx * 0.2 * W, ymid, z0])
    yF = (feet["FL"][1] + feet["FR"][1]) / 2
    yB = (feet["BL"][1] + feet["BR"][1]) / 2
    sel = (P[:, 1] > yF + 0.25 * (yB - yF)) & (P[:, 1] < yB - 0.25 * (yB - yF)) & (abs(P[:, 0] - xc) < 0.25 * W)
    zz = P[sel, 2] if sel.sum() > 20 else P[:, 2]
    belly, back = np.percentile(zz, 2), np.percentile(zz, 98)
    belly = max(belly, z0 + 0.12 * H)
    jz = belly + 0.35 * (back - belly)           # плечо / тазобедренный сустав
    cz = belly + 0.55 * (back - belly)           # ось позвоночника
    lay = {"xc": xc, "z0": z0, "H": H, "L": L, "W": W, "yF": yF, "yB": yB, "belly": belly, "back": back,
           "jz": jz, "cz": cz, "legs": {}}
    for k, f in feet.items():
        sx = 1 if k[1] == "L" else -1
        front = k[0] == "F"
        quad = ((P[:, 0] - xc) * sx > 0.03 * W) & ((P[:, 1] < (yF + yB) / 2) if front else (P[:, 1] >= (yF + yB) / 2))
        pts = []
        for h in (0.45, 0.9):
            hz = z0 + h * (belly - z0)
            s = quad & (abs(P[:, 2] - hz) < 0.06 * (belly - z0) + 1e-4)
            pts.append(P[s].mean(0) if s.sum() > 3 else np.array([f[0], f[1], hz]))
        knee, up = pts
        top = np.array([up[0], up[1], jz])
        lay["legs"][k] = [top, knee, np.array([f[0], f[1], z0 + 0.15 * (knee[2] - z0)]), np.array([f[0], f[1] - (0.02 * L if front else -0.02 * L) * 0, z0])]
    # голова: всё, что впереди передних лап и выше живота
    hs = (P[:, 1] < yF - 0.06 * L) & (P[:, 2] > belly)
    if hs.sum() < 30:
        hs = (P[:, 1] < yF) & (P[:, 2] > belly)
    Hd = P[hs]
    y_tip = np.percentile(Hd[:, 1], 1)
    ch = Hd.mean(0)
    hl = max(ch[1] - y_tip, 0.05 * L)
    zs = np.median(Hd[Hd[:, 1] < y_tip + 0.35 * hl, 2])
    lay["head"] = (np.array([xc, ch[1] + 0.5 * hl, 0.5 * (ch[2] + zs)]), np.array([xc, y_tip, zs]))
    lay["neck0"] = np.array([xc, yF, cz + 0.3 * (back - cz)])
    # хвост: позади задних лап
    ts = (P[:, 1] > yB + 0.08 * L) & (P[:, 2] > belly - 0.1 * (back - belly))
    if ts.sum() > 15:
        T = P[ts]
        tip = T[np.argmax(T[:, 1])]
        base = np.array([xc, T[:, 1].min(), np.median(T[T[:, 1] < T[:, 1].min() + 0.05 * L, 2])])
        lay["tail"] = (base, tip)
    else:
        lay["tail"] = (np.array([xc, yB + 0.05 * L, cz]), np.array([xc, yB + 0.12 * L, cz + 0.05 * H]))
    return lay


def quad_bones(lay):
    xc, cz = lay["xc"], lay["cz"]
    yF, yB = lay["yF"], lay["yB"]
    B = []                                          # (имя, начало, конец, родитель)
    hip = np.array([xc, yB, cz])
    mid = np.array([xc, (yF + yB) / 2, cz])
    sh = np.array([xc, yF, cz])
    B += [("Hips", hip, mid, None), ("Spine", mid, sh, "Hips")]
    n0 = lay["neck0"]
    h0, h1 = lay["head"]
    if np.linalg.norm(h0 - n0) < 0.05 * lay["L"]:
        h0 = n0 + (h1 - n0) * 0.4
    B += [("Neck", n0, h0, "Spine"), ("Head", h0, h1, "Neck")]
    t0, t1 = lay["tail"]
    tm = (t0 + t1) / 2
    B += [("Tail1", t0, tm, "Hips"), ("Tail2", tm, t1, "Tail1")]
    for k, (top, knee, ank, foot) in lay["legs"].items():
        par = "Spine" if k[0] == "F" else "Hips"
        B += [(f"Leg{k}1", top, knee, par), (f"Leg{k}2", knee, ank, f"Leg{k}1"), (f"Leg{k}3", ank, foot, f"Leg{k}2")]
    return B


def quad_allow(lay):
    """Какие вершины может тянуть кость (чтобы лапа не тянула соседнюю лапу или спину)."""
    xc, W, yF, yB = lay["xc"], lay["W"], lay["yF"], lay["yB"]
    ym = (yF + yB) / 2
    ztop = lay["jz"] + 0.3 * (lay["back"] - lay["belly"])

    def f(name, P):
        if name.startswith("Leg"):
            k = name[3:5]
            sx = 1 if k[1] == "L" else -1
            ok = (P[:, 0] - xc) * sx > -0.03 * W
            ok &= (P[:, 1] < ym) if k[0] == "F" else (P[:, 1] >= ym)
            return ok & (P[:, 2] < ztop)
        if name.startswith("Tail"):
            return P[:, 1] > yB - 0.05 * lay["L"]
        if name in ("Neck", "Head"):
            return P[:, 1] < yF + 0.1 * lay["L"]
        return np.ones(len(P), bool)
    return f


# ───────────────────────── разметка: птицы ─────────────────────────

def bird_layout(P):
    mn, mx = P.min(0), P.max(0)
    H = mx[2] - mn[2]
    xc, z0 = (mn[0] + mx[0]) / 2, mn[2]
    span = np.abs(P[:, 0] - xc).max()
    xr = 0.2 * span
    body = P[np.abs(P[:, 0] - xc) < xr]
    bl, bh = np.percentile(body[:, 2], 3), np.percentile(body[:, 2], 97)
    body = body[body[:, 2] > z0 + 0.25 * (bl - z0) + 0.15 * (bh - bl) * 0]
    by0, by1 = body[:, 1].min(), body[:, 1].max()
    Lb = by1 - by0
    c = body[(body[:, 2] > bl + 0.1 * (bh - bl))].mean(0)
    hd = body[body[:, 1] < by0 + 0.3 * Lb]
    ht = hd[np.argmin(hd[:, 1])]
    tl = body[body[:, 1] > by1 - 0.3 * Lb]
    tt = tl[np.argmax(tl[:, 1])]
    lay = {"xc": xc, "z0": z0, "H": H, "L": Lb, "W": 2 * span, "xr": xr, "c": c, "belly": bl, "back": bh,
           "head": (np.array([xc, by0 + 0.3 * Lb, hd[:, 2].mean()]), np.array([xc, ht[1], ht[2]])),
           "tail": (np.array([xc, c[1] + 0.15 * Lb, c[2]]), tt), "wings": {}, "legs": {}}
    for side, sx in (("L", 1), ("R", -1)):
        w = P[(P[:, 0] - xc) * sx > xr]
        root = w[(w[:, 0] - xc) * sx < 1.4 * xr]
        sh = np.array([xc + sx * 0.7 * xr, root[:, 1].mean(), root[:, 2].mean()])
        m = w[np.abs((w[:, 0] - xc) * sx - 0.55 * span) < 0.08 * span]
        midp = m.mean(0) if len(m) > 3 else (sh + w[np.argmax((w[:, 0] - xc) * sx)]) / 2
        tip = w[np.argmax((w[:, 0] - xc) * sx)]
        lay["wings"][side] = (sh, midp, tip)
        g = P[(P[:, 2] < z0 + 0.1 * H) & ((P[:, 0] - xc) * sx > 0) & (np.abs(P[:, 0] - xc) < xr)]
        f = g.mean(0) if len(g) > 3 else np.array([xc + sx * 0.3 * xr, c[1], z0])
        lay["legs"][side] = (np.array([f[0], f[1], max(bl, z0 + 0.3 * H)]), np.array([f[0], f[1], z0]))
    return lay


def bird_bones(lay):
    c, xc = lay["c"], lay["xc"]
    root0 = np.array([xc, c[1] + 0.15 * lay["L"], c[2]])
    root1 = np.array([xc, c[1] - 0.15 * lay["L"], c[2]])
    h0, h1 = lay["head"]
    t0, t1 = lay["tail"]
    B = [("Body", root0, root1, None), ("Head", h0, h1, "Body"), ("Tail1", t0, t1, "Body")]
    for s, (sh, m, tip) in lay["wings"].items():
        B += [(f"Wing{s}1", sh, m, "Body"), (f"Wing{s}2", m, tip, f"Wing{s}1")]
    for s, (top, foot) in lay["legs"].items():
        B += [(f"Leg{s}", top, foot, "Body")]
    return B


def bird_allow(lay):
    xc, xr = lay["xc"], lay["xr"]
    zl = lay["belly"] + 0.15 * (lay["back"] - lay["belly"])

    def f(name, P):
        dx = P[:, 0] - xc
        if name.startswith("Wing"):
            sx = 1 if name[4] == "L" else -1
            return dx * sx > 0.6 * xr
        if name.startswith("Leg"):
            sx = 1 if name[3] == "L" else -1
            return (dx * sx > -0.1 * xr) & (P[:, 2] < zl) & (np.abs(dx) < 1.2 * xr)
        return np.abs(dx) < 1.4 * xr
    return f


# ───────────────────────── кости и веса ─────────────────────────

def build_armature(obj, bones, allow):
    sc = bpy.context.scene
    ad = bpy.data.armatures.new("Armature")
    arm = bpy.data.objects.new("Armature", ad)
    sc.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    for name, h, t, par in bones:
        eb = ad.edit_bones.new(name)
        eb.head, eb.tail = V(*h), V(*t)
        if (eb.tail - eb.head).length < 1e-3:
            eb.tail = eb.head + Vector((0, 0, -0.01))
        d = (eb.tail - eb.head).normalized()
        z = Vector((1, 0, 0)).cross(d)
        eb.align_roll(z if z.length > 0.2 else Vector((0, 0, 1)))
        if par:
            eb.parent = ad.edit_bones[par]
    bpy.ops.object.mode_set(mode="OBJECT")
    P = verts(obj)
    names = [b[0] for b in bones]
    D = np.full((len(P), len(names)), np.inf)
    for j, (name, h, t, _) in enumerate(bones):
        h, t = np.asarray(h, float), np.asarray(t, float)
        v = t - h
        u = np.clip(((P - h) @ v) / max(v @ v, 1e-9), 0, 1)
        d = np.linalg.norm(P - (h + u[:, None] * v), axis=1)
        ok = allow(name, P)
        D[ok, j] = d[ok]
    bad = ~np.isfinite(D).any(1)                    # вершина ни к кому не подошла — к ближайшей любой
    if bad.any():
        for j, (name, h, t, _) in enumerate(bones):
            h, t = np.asarray(h, float), np.asarray(t, float)
            v = t - h
            u = np.clip(((P[bad] - h) @ v) / max(v @ v, 1e-9), 0, 1)
            D[bad, j] = np.linalg.norm(P[bad] - (h + u[:, None] * v), axis=1)
    scale = np.ptp(P, 0).max()
    Wt = 1.0 / (D / scale + 0.01) ** 4
    Wt[~np.isfinite(D)] = 0
    top = np.argsort(-Wt, 1)[:, 3:]
    np.put_along_axis(Wt, top, 0, 1)
    Wt /= Wt.sum(1, keepdims=True)
    # сгладить по рёбрам (и склеить вершины в одной точке — швы текстуры)
    key = np.round(P / (scale * 1e-4)).astype(np.int64)
    _, grp = np.unique(key, axis=0, return_inverse=True)
    grp = grp.ravel()
    e = np.empty(len(obj.data.edges) * 2, int)
    obj.data.edges.foreach_get("vertices", e)
    e = grp[e.reshape(-1, 2)]
    ng = grp.max() + 1
    G = np.zeros((ng, len(names)))
    np.add.at(G, grp, Wt)
    G /= np.bincount(grp, minlength=ng)[:, None]
    deg = np.bincount(e.ravel(), minlength=ng)[:, None] + 1e-9
    for _ in range(3):
        S = np.zeros_like(G)
        np.add.at(S, e[:, 0], G[e[:, 1]])
        np.add.at(S, e[:, 1], G[e[:, 0]])
        G = np.where(deg > 0.5, 0.5 * G + 0.5 * S / deg, G)
    Wt = G[grp]
    top = np.argsort(-Wt, 1)[:, 4:]
    np.put_along_axis(Wt, top, 0, 1)
    Wt /= Wt.sum(1, keepdims=True)
    for j, name in enumerate(names):
        vg = obj.vertex_groups.new(name=name)
        idx = np.nonzero(Wt[:, j] > 0.01)[0]
        for i in idx:
            vg.add([int(i)], float(Wt[i, j]), "REPLACE")
    obj.parent = arm
    obj.modifiers.new("Armature", "ARMATURE").object = arm
    return arm


# ───────────────────────── анимации ─────────────────────────

def rx(a):
    return Quaternion((1, 0, 0), a)


def rz(a):
    return Quaternion((0, 0, 1), a)


def ry(a):
    return Quaternion((0, 1, 0), a)


class Anim:
    def __init__(self, arm):
        self.arm = arm
        self.rest = {b.name: b.matrix_local.to_3x3() for b in arm.data.bones}

    def world_rot(self, bone, q_world):
        """Поворот в осях мира → в осях кости."""
        R = self.rest[bone].to_quaternion()
        return R.inverted() @ q_world @ R

    def world_loc(self, bone, v):
        return self.rest[bone].inverted() @ Vector(v)

    def make(self, name, n, pose_fn, loop=True):
        arm = self.arm
        act = bpy.data.actions.new(name)
        act.use_fake_user = True
        arm.animation_data.action = act
        for pb in arm.pose.bones:
            pb.rotation_mode = "QUATERNION"
        prev = {}
        for f in range(n + 1):
            t = (f % n if loop else f) / n
            for pb in arm.pose.bones:
                pb.rotation_quaternion = (1, 0, 0, 0)
                pb.location = (0, 0, 0)
            for b, val in pose_fn(t).items():
                pb = arm.pose.bones[b]
                if isinstance(val, tuple):
                    q, loc = val
                else:
                    q, loc = val, None
                if q is not None:
                    q = q.normalized()
                    if b in prev and q.dot(prev[b]) < 0:
                        q = -q
                    prev[b] = q
                    pb.rotation_quaternion = q
                if loc is not None:
                    pb.location = loc
            for pb in arm.pose.bones:
                pb.keyframe_insert("rotation_quaternion", frame=f)
                pb.keyframe_insert("location", frame=f)
        arm.animation_data.action = None
        tr = arm.animation_data.nla_tracks.new()
        tr.name = name
        st = tr.strips.new(name, 0, act)
        try:
            st.action_slot = act.slots[0]
        except (AttributeError, IndexError):
            pass
        tr.mute = True
        return act


def sn(x):
    return math.sin(2 * math.pi * x)


def cs(x):
    return math.cos(2 * math.pi * x)


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def quad_anims(arm, lay, kind, name=""):
    A = Anim(arm)
    legs = [k for k in ("FL", "FR", "BL", "BR")]
    Lleg = float(lay["jz"] - lay["z0"])
    size = Lleg / 0.4
    info = {}

    def leg_pose(p, k, t, amp, bend, ph):
        x = t + ph
        a = amp * sn(x)                                     # + — лапа вперёд
        lift = max(0.0, cs(x)) ** 1.5                       # перенос лапы (идёт вперёд) — сгиб
        p[f"Leg{k}1"] = rx(-a - (0.15 * bend * lift if k[0] == "B" else 0))
        p[f"Leg{k}2"] = rx(bend * lift)
        p[f"Leg{k}3"] = rx(0.5 * bend * lift - 0.3 * a)

    hop = kind == "hop"

    # стоит: дыхание, голова оглядывается, хвост
    n = 75
    def idle(t):
        p = {"Spine": rx(0.025 * sn(3 * t)), "Neck": rz(0.25 * sn(t)) @ rx(0.06 * sn(2 * t)),
             "Head": rx(-0.05 * sn(2 * t + 0.2)), "Tail1": rz(0.18 * sn(2 * t)) @ rx(-0.05),
             "Tail2": rz(0.2 * sn(2 * t - 0.15))}
        p["Hips"] = (None, A.world_loc("Hips", (0, 0, 0.006 * Lleg * sn(3 * t))))
        return p
    A.make("idle", n, idle)
    info["idle"] = {"frames": n + 1, "seconds": n / FPS, "loop": True}

    def gait(name, T, amp, bend, phases, bob, flex, tail):
        n = max(8, int(round(T * FPS)))

        def fn(t):
            p = {}
            for k in legs:
                leg_pose(p, k, t, amp, bend, phases[k])
            if hop:
                up = max(0.0, sn(t + 0.05)) * bob * Lleg
            else:
                up = bob * Lleg * cs(2 * t)
            hips_q = A.world_rot("Hips", Quaternion((0, 1, 0), 0.03 * sn(t) * (0 if flex else 1)))
            hips_q = hips_q @ rx(-flex * sn(t + 0.1))
            p["Hips"] = (hips_q, A.world_loc("Hips", (0, 0, up)))
            p["Spine"] = rx(flex * 1.4 * sn(t + 0.1))
            p["Neck"] = rx(0.05 * cs(2 * t) - 0.05 - flex * 0.6 * sn(t))
            p["Head"] = rx(-0.04 * cs(2 * t))
            p["Tail1"] = rz(tail * sn(t)) @ rx(-0.1 + flex * sn(t))
            p["Tail2"] = rz(tail * sn(t - 0.15))
            return p
        A.make(name, n, fn)
        speed = 4 * Lleg * math.sin(amp) / (n / FPS)
        info[name] = {"frames": n + 1, "seconds": round(n / FPS, 3), "loop": True, "speed_mps": round(speed, 2)}

    if hop:
        hp = {"BL": 0.0, "BR": 0.03, "FL": 0.5, "FR": 0.53}
        gait("walk", 0.55 * math.sqrt(size), 0.3, 0.6, hp, 0.08, 0.10, 0.0)
        gait("run", 0.40 * math.sqrt(size), 0.55, 0.9, hp, 0.25, 0.18, 0.0)
    else:
        walk_ph = {"BL": 0.0, "FL": 0.25, "BR": 0.5, "FR": 0.75}
        run_ph = {"BL": 0.0, "BR": 0.1, "FL": 0.45, "FR": 0.55}
        Tw = min(max(0.75 * math.sqrt(size), 0.5), 1.5)
        Tr = min(max(0.42 * math.sqrt(size), 0.3), 0.8)
        gait("walk", Tw, 0.3, 0.55, walk_ph, 0.015, 0.0, 0.12)
        gait("run", Tr, 0.5, 0.95, run_ph, 0.05, 0.10, 0.08)

    # ест: голова к земле, жуёт
    head_h = float(lay["head"][1][2] - lay["z0"])
    neck_len = float(np.linalg.norm(np.asarray(lay["head"][1]) - np.asarray(lay["neck0"])))
    a_eat = min(1.3, math.asin(min(0.95, max(0.1, (head_h - 0.08 * Lleg) / max(neck_len, 1e-3) * 0.8)))) + 0.2
    if hop:                                                  # заяц: голова к траве чуть-чуть, уши не в землю
        a_eat = 0.35
    n = 60
    def eat(t):
        return {"Neck": rx(a_eat + 0.06 * sn(2 * t)), "Head": rx(0.25 + 0.12 * max(0, sn(4 * t))),
                "Spine": rx(0.08), "Tail1": rz(0.12 * sn(t)),
                "LegFL1": rx(-0.12), "LegFR1": rx(-0.12)}
    A.make("eat", n, eat)
    info["eat"] = {"frames": n + 1, "seconds": n / FPS, "loop": True}

    # атака: присел назад → бросок вперёд → назад (у зайца — короткий выпад)
    if True:
        n = 30 if not hop else 20
        reach = 0.25 * float(lay["L"]) * (0.6 if hop else 1.0)
        def attack(t):
            back_ = ease(t / 0.3) * (1 - ease((t - 0.3) / 0.15))
            fwd = ease((t - 0.3) / 0.15) * (1 - ease((t - 0.6) / 0.4))
            p = {}
            p["Hips"] = (rx(0.1 * back_ - 0.12 * fwd),
                         A.world_loc("Hips", (0, 0.06 * Lleg * back_ - reach * fwd, -0.12 * Lleg * back_ + 0.05 * Lleg * fwd)))
            p["Spine"] = rx(-0.15 * fwd)
            p["Neck"] = rx(0.35 * back_ - 0.25 * fwd)
            p["Head"] = rx(-0.15 * back_ + 0.35 * fwd)
            for k in ("FL", "FR"):
                p[f"Leg{k}1"] = rx(-0.6 * fwd + 0.25 * back_)
                p[f"Leg{k}2"] = rx(0.3 * fwd + 0.3 * back_)
            for k in ("BL", "BR"):
                p[f"Leg{k}1"] = rx(0.35 * fwd - 0.2 * back_)
                p[f"Leg{k}2"] = rx(0.4 * back_)
            p["Tail1"] = rx(0.4 * back_ + 0.2 * fwd)
            return p
        A.make("attack", n, attack, loop=False)
        info["attack"] = {"frames": n + 1, "seconds": n / FPS, "loop": False, "hit_at_s": round(0.42 * n / FPS, 2)}

    # получил удар
    n = 15
    def hit(t):
        k = math.sin(math.pi * min(1, t / 0.9)) * (1 - t) ** 0.5
        return {"Hips": (rx(-0.12 * k), A.world_loc("Hips", (0, 0.08 * Lleg * k, -0.04 * Lleg * k))),
                "Spine": rx(-0.1 * k), "Neck": rx(-0.35 * k) @ rz(0.2 * k), "Head": rx(-0.2 * k),
                "Tail1": rx(-0.4 * k)}
    A.make("hit", n, hit, loop=False)
    info["hit"] = {"frames": n + 1, "seconds": n / FPS, "loop": False}


    canine = name.startswith(("dog_", "wolf"))
    bear = name.startswith("bear_")
    hoofed = name.startswith(("deer_", "moose_"))
    body_len = float(lay["yB"] - lay["yF"])
    belly_h = float(lay["belly"] - lay["z0"])

    # убегает: быстрый галоп, голова и хвост прижаты (быстрее бега)
    if hop:
        T_f = 0.34 * math.sqrt(size)
        ph_f = {"BL": 0.0, "BR": 0.03, "FL": 0.5, "FR": 0.53}
        amp_f, bend_f, bob_f, flex_f = 0.6, 0.95, 0.3, 0.2
    else:
        T_f = min(max(0.36 * math.sqrt(size), 0.26), 0.7)
        ph_f = {"BL": 0.0, "BR": 0.1, "FL": 0.45, "FR": 0.55}
        amp_f, bend_f, bob_f, flex_f = 0.58, 1.0, 0.06, 0.13
    n = max(8, int(round(T_f * FPS)))
    def flee(t):
        p = {}
        for k in legs:
            leg_pose(p, k, t, amp_f, bend_f, ph_f[k])
        up = (max(0.0, sn(t + 0.05)) * bob_f if hop else bob_f * cs(2 * t)) * Lleg
        p["Hips"] = (rx(-flex_f * sn(t + 0.1)), A.world_loc("Hips", (0, 0, up)))
        p["Spine"] = rx(flex_f * 1.4 * sn(t + 0.1))
        p["Neck"] = rx(0.2 - flex_f * 0.5 * sn(t))
        p["Head"] = rx(0.1)
        p["Tail1"] = rx(-0.45)
        p["Tail2"] = rx(-0.2)
        return p
    A.make("flee", n, flee)
    info["flee"] = {"frames": n + 1, "seconds": round(n / FPS, 3), "loop": True,
                    "speed_mps": round(4 * Lleg * math.sin(amp_f) / (n / FPS), 2)}

    # ── позы «сидит / лежит / просит»: лапы ставятся в точки на полу (обратная кинематика), суставы гнутся сами ──
    Bn = arm.data.bones
    hip0 = Vector(Bn["Hips"].head_local)
    z0 = float(lay["z0"])
    upright = name == "rabbit_wild_krolik"                    # модель уже сидит столбиком — позы мягче

    def L_of(b):
        return (Vector(Bn[b].tail_local) - Vector(Bn[b].head_local)).length

    def xf(pnt, D, T):
        return hip0 + D @ (Vector(pnt) - hip0) + T

    def swing(b, d):
        r = Vector(Bn[b].tail_local) - Vector(Bn[b].head_local)
        return r.normalized().rotation_difference(Vector(d).normalized())

    def ik2(H, Aim, L1, L2, bend):
        d = Aim - H
        dist = min(d.length, (L1 + L2) * 0.999)
        u = d.normalized()
        a_ = (L1 * L1 - L2 * L2 + dist * dist) / (2 * dist)
        h = math.sqrt(max(L1 * L1 - a_ * a_, 0.0))
        v = Vector(bend) - u * Vector(bend).dot(u)
        v = v.normalized() if v.length > 1e-6 else Vector((0, 0, 1))
        return H + u * a_ + v * h, H + u * dist

    def leg_to(p, k, Dp, D_body, T, wrist_or_ankle, toe, bend):
        """Лапа k: сустав 1 из тела, сустав «запястье/скакательный» — в точку, кончик — в toe."""
        b1, b2, b3 = f"Leg{k}1", f"Leg{k}2", f"Leg{k}3"
        H = xf(Bn[b1].head_local, D_body, T)
        K, W = ik2(H, Vector(wrist_or_ankle), L_of(b1), L_of(b2), bend)
        D1, D2, D3 = swing(b1, K - H), swing(b2, W - K), swing(b3, Vector(toe) - W)
        p[b1] = A.world_rot(b1, Dp.inverted() @ D1)
        p[b2] = A.world_rot(b2, D1.inverted() @ D2)
        p[b3] = A.world_rot(b3, D2.inverted() @ D3)

    def body(p, D, T, neck_up=0.0, tail_dir=(0.35, 1.0, -0.12)):
        p["Hips"] = (A.world_rot("Hips", D), A.world_loc("Hips", T))
        p["Neck"] = A.world_rot("Neck", D.inverted() @ Quaternion((1, 0, 0), -neck_up))   # голова ровно (+ чуть вверх)
        p["Tail1"] = A.world_rot("Tail1", D.inverted() @ swing("Tail1", tail_dir))          # хвост лежит на полу
        p["Tail2"] = rx(0.0)

    def blend(p, k):
        """k = 0 — стоит как в покое, 1 — полная поза (для «ложится»)."""
        out = {}
        for bname, v in p.items():
            q, loc = v if isinstance(v, tuple) else (v, None)
            q = Quaternion().slerp(q, k) if q is not None else None
            loc = loc * k if loc is not None else None
            out[bname] = (q, loc) if bname == "Hips" else q
        return out

    LF = L_of("LegFL1") + L_of("LegFL2")
    LB = L_of("LegBL1") + L_of("LegBL2")
    L3F, L3B = L_of("LegFL3"), L_of("LegBL3")

    def hind_folded(p, D, T):
        """Задние лапы подогнуты: скакательный сустав и стопа лежат на полу, стопа вперёд, колено вперёд-вверх."""
        for s_ in ("L", "R"):
            k = "B" + s_
            H = xf(Bn[f"Leg{k}1"].head_local, D, T)
            ank = Vector((H.x, H.y - 0.15 * LB, z0 + 0.05 * L3B + 0.01))
            leg_to(p, k, D, D, T, ank, ank + Vector((0, -L3B, -0.04 * L3B)), (0, -1, 0.6))

    def sit_pose():
        """Сидит: таз на полу, перед поднят на прямых передних лапах. Наклон и опускание подбираются сами."""
        best = None
        for i in range(25):
            a_ = 0.25 + i * 0.04
            D = Quaternion((1, 0, 0), -a_)
            Sh = xf(Bn["LegFL1"].head_local, D, Vector())
            dz = (z0 + 0.97 * (LF + L3F)) - Sh.z               # опустить/поднять, чтобы передние лапы стояли
            Hp = xf(Bn["LegBL1"].head_local, D, Vector((0, 0, dz)))
            err = abs(Hp.z - (z0 + 0.32 * LB))                 # таз — низко, у пола
            if best is None or err < best[0]:
                best = (err, a_, dz)
        _, a_, dz = best
        D, T = Quaternion((1, 0, 0), -a_), Vector((0, 0, dz))
        p = {}
        body(p, D, T, neck_up=0.1)
        for s_ in ("L", "R"):
            Sh = xf(Bn[f"LegF{s_}1"].head_local, D, T)
            paw = Vector((Sh.x, Sh.y - 0.06 * LF, z0))
            leg_to(p, "F" + s_, D, D, T, paw + Vector((0, 0.02 * L3F, L3F)), paw + Vector((0, -0.25 * L3F, 0)), (0, 1, 0))
        hind_folded(p, D, T)
        return p, D, T

    def lie_pose(breath=0.0):
        """Лежит на животе: тело горизонтально, живот на полу, задние подогнуты; передние — вперёд (хищники,
        зайцы) или подогнуты под грудь (копытные)."""
        D = Quaternion((1, 0, 0), 0.0)
        T = Vector((0, 0, -(belly_h - 0.03 * Lleg) + 0.004 * Lleg * breath))
        p = {}
        body(p, D, T, neck_up=0.05, tail_dir=(0.5, 1.0, -0.05))
        p["Spine"] = rx(0.02 * breath)
        for s_ in ("L", "R"):
            Sh = xf(Bn[f"LegF{s_}1"].head_local, D, T)
            if hoofed:
                W = Vector((Sh.x, Sh.y - 0.3 * LF, z0 + 0.06 * L3F))
                leg_to(p, "F" + s_, D, D, T, W, W + Vector((0, L3F * 0.95, 0)), (0, 0.6, 1))
            else:
                W = Vector((Sh.x, Sh.y - 0.8 * LF, z0 + 0.06 * L3F))
                leg_to(p, "F" + s_, D, D, T, W, W + Vector((0, -L3F, -0.03 * L3F)), (0, 0.4, 1))
        hind_folded(p, D, T)
        return p

    if upright:
        def lie_pose(breath=0.0):
            return {"Hips": (rx(0.25), A.world_loc("Hips", (0, 0, -0.12 * belly_h + 0.004 * Lleg * breath))),
                    "Spine": rx(0.2 + 0.03 * breath)}

        def sit_pose():
            return {"Hips": (None, A.world_loc("Hips", (0, 0, -0.04 * Lleg))), "Neck": rx(0.0)}, Quaternion(), Vector()

    n = 36
    LIE = lie_pose()
    def lie_down(t):
        return blend(LIE, ease(t / 0.9))
    A.make("lie_down", n, lie_down, loop=False)
    info["lie_down"] = {"frames": n + 1, "seconds": n / FPS, "loop": False, "note": "стоял → лёг; дальше sleep"}

    n = 120
    def sleep(t):
        p = lie_pose(sn(2 * t))
        if not upright:
            D = Quaternion()
            p["Neck"] = A.world_rot("Neck", Quaternion((1, 0, 0), 0.5 + 0.02 * sn(2 * t)) @ Quaternion((0, 0, 1), 0.3))
            p["Head"] = rx(0.2)
            p["Tail1"] = A.world_rot("Tail1", swing("Tail1", (0.9, 0.6, -0.05)))
            p["Tail2"] = rz(0.4)
        return p
    A.make("sleep", n, sleep)
    info["sleep"] = {"frames": n + 1, "seconds": n / FPS, "loop": True}

    # сидит (у копытных — лежит, голова поднята)
    SIT, D_sit, T_sit = sit_pose()

    def sitting(k=1.0):
        if hoofed and not upright:
            p = lie_pose()
            p["Neck"] = A.world_rot("Neck", Quaternion((1, 0, 0), -0.15))
            return p
        return dict(SIT)

    n = 75
    def sit(t):
        p = sitting()
        p["Neck"] = p["Neck"] @ rz(0.15 * sn(t))
        p["Spine"] = rx(0.015 * sn(3 * t))
        return p
    A.make("sit", n, sit)
    info["sit"] = {"frames": n + 1, "seconds": n / FPS, "loop": True}

    # просит еду: заяц — встаёт столбиком, передние лапки поджаты (собакам подачу лапы убрали — решение автора)
    if hop:
        n = 60
        if hop and not upright:
            a_b = 1.05
            D_b = Quaternion((1, 0, 0), -a_b)
            Hp = xf(Bn["LegBL1"].head_local, D_b, Vector())
            T_b = Vector((0, 0, (z0 + 0.3 * LB) - Hp.z))
        def beg(t):
            if upright:
                return {"LegFL1": rx(-0.7 - 0.1 * sn(2 * t)), "LegFR1": rx(-0.7 - 0.1 * sn(2 * t)),
                        "LegFL2": rx(0.8), "LegFR2": rx(0.8), "Neck": rx(-0.2 + 0.06 * sn(2 * t)),
                        "Head": rx(0.1 * sn(4 * t))}
            if hop:
                p = {}
                body(p, D_b, T_b, neck_up=0.05 + 0.05 * sn(2 * t))
                hind_folded(p, D_b, T_b)
                for s_ in ("L", "R"):                     # лапки висят перед грудью, согнуты
                    Sh = xf(Bn[f"LegF{s_}1"].head_local, D_b, T_b)
                    W = Sh + Vector((0, -0.35 * LF, -0.55 * LF + 0.03 * LF * sn(2 * t)))
                    leg_to(p, "F" + s_, D_b, D_b, T_b, W, W + Vector((0, 0.15 * L3F, -L3F)), (0, -1, 0))
                p["Head"] = rx(0.08 * sn(4 * t))
                return p
            p = sitting()
            lift = 0.5 + 0.5 * sn(2 * t)
            Sh = xf(Bn["LegFR1"].head_local, D_sit, T_sit)    # правая передняя — подаёт лапу, кисть свисает
            W = Sh + Vector((0, -(0.55 + 0.1 * lift) * LF, -(0.45 - 0.15 * lift) * LF))
            leg_to(p, "FR", D_sit, D_sit, T_sit, W, W + Vector((0, -0.25 * L3F, -0.95 * L3F)), (0, 1, -0.3))
            p["Neck"] = p["Neck"] @ rz(0.25 * sn(t))
            p["Head"] = rz(0.2 * sn(t))
            p["Tail1"] = p["Tail1"] @ rz(0.4 * sn(4 * t))
            p["Tail2"] = rz(0.4 * sn(4 * t - 0.2))
            return p
        A.make("beg", n, beg)
        info["beg"] = {"frames": n + 1, "seconds": n / FPS, "loop": True, "note": "ручное животное просит еду"}

    # воет (собаки, волк): садится, морда вверх
    if canine:
        n = 90
        def howl(t):
            up = ease(t / 0.2) * (1 - ease((t - 0.8) / 0.2))
            p = sitting()
            p["Neck"] = p["Neck"] @ rx(-0.55 * up + 0.03 * up * sn(12 * t))
            p["Head"] = rx(-0.25 * up)
            return p
        A.make("howl", n, howl, loop=False)
        info["howl"] = {"frames": n + 1, "seconds": n / FPS, "loop": False}

    # рычит (собаки, волк, медведи): пригнулся, голова низко, дрожь
    if canine or bear:
        n = 45
        def growl(t):
            tr = 0.012 * sn(9 * t)
            p = {"Hips": (rx(-0.1), A.world_loc("Hips", (0, 0.05 * Lleg, -0.15 * Lleg))),
                 "Spine": rx(0.12 + tr), "Neck": rx(0.35 + tr), "Head": rx(-0.3 + tr),
                 "Tail1": rx(-0.35 if canine else 0.0)}
            for s_ in ("L", "R"):
                p[f"LegF{s_}1"] = rx(-0.35)
                p[f"LegF{s_}2"] = rx(0.6)
                p[f"LegB{s_}1"] = rx(-0.3)
                p[f"LegB{s_}2"] = rx(0.6)
            return p
        A.make("growl", n, growl)
        info["growl"] = {"frames": n + 1, "seconds": n / FPS, "loop": True}

    # смерть: заваливается на бок
    n = 36
    drop = float(lay["cz"] - lay["z0"]) - 0.38 * float(lay["W"]) * (0.6 if kind != "hop" else 0.8)
    def death(t):
        a = ease(t / 0.75)
        b = 1 - abs(1 - min(1, t / 0.75)) ** 2
        roll = A.world_rot("Hips", Quaternion((0, 1, 0), 1.45 * a))
        p = {"Hips": (roll, A.world_loc("Hips", (0.1 * float(lay["W"]) * a, 0, -max(0, drop) * a + 0.05 * Lleg * b * (1 - a)))),
             "Neck": rx(-0.3 * a) @ rz(0.2 * a), "Head": rx(-0.2 * a), "Tail1": rz(0.3 * a) @ rx(-0.2 * a)}
        for i, k in enumerate(("FL", "FR", "BL", "BR")):
            s = 1 if k[0] == "F" else -1
            p[f"Leg{k}1"] = rx(s * (0.25 + 0.1 * i) * a)
            p[f"Leg{k}2"] = rx((0.5 + 0.15 * i) * a)
        return p
    A.make("death", n, death, loop=False)
    info["death"] = {"frames": n + 1, "seconds": n / FPS, "loop": False}
    return info


def bird_anims(arm, lay):
    A = Anim(arm)
    info = {}
    span = float(lay["W"]) / 2
    size = span / 0.3
    H = float(lay["c"][2] - lay["z0"])

    F = [float(x) for x in os.environ.get("FOLD", "1.4,0.3,1.4,0.0").split(",")]

    def wing(side, back, down):
        """back — крыло назад (вдоль тела), down — кончик вниз; углы в осях мира."""
        sx = 1 if side == "L" else -1
        return Quaternion((0, 0, 1), sx * back) @ Quaternion((0, 1, 0), sx * down)

    def fold(p, k=1.0):
        for sd in ("L", "R"):
            p[f"Wing{sd}1"] = A.world_rot(f"Wing{sd}1", wing(sd, F[0] * k, F[1] * k))
            p[f"Wing{sd}2"] = A.world_rot(f"Wing{sd}2", wing(sd, F[2] * k, F[3] * k))
        return p

    def flap(p, a1, a2):
        for sd in ("L", "R"):
            p[f"Wing{sd}1"] = A.world_rot(f"Wing{sd}1", wing(sd, 0, -a1))
            p[f"Wing{sd}2"] = A.world_rot(f"Wing{sd}2", wing(sd, 0, -a2))
        return p

    n = 75
    def idle(t):
        p = fold({})
        p["Head"] = rz(0.5 * sn(t) * (1 if (t % 0.5) < 0.25 else 0.6)) @ rx(0.06 * sn(2 * t))
        p["Body"] = (rx(0.03 * sn(3 * t)), None)
        p["Tail1"] = rx(0.08 * sn(3 * t))
        return p
    A.make("idle", n, idle)
    info["idle"] = {"frames": n + 1, "seconds": n / FPS, "loop": True}

    n = max(10, int(round(0.45 * math.sqrt(size) * FPS)))
    def walk(t):
        p = fold({})
        up = max(0.0, sn(2 * t)) * 0.12 * H
        p["Body"] = (rx(0.08 * sn(2 * t + 0.25)), A.world_loc("Body", (0, 0, up)))
        p["Head"] = rx(-0.12 * sn(2 * t))
        p["LegL"] = rx(-0.35 * sn(t))
        p["LegR"] = rx(0.35 * sn(t))
        p["Tail1"] = rx(0.1 * sn(2 * t))
        return p
    A.make("walk", n, walk)
    info["walk"] = {"frames": n + 1, "seconds": round(n / FPS, 3), "loop": True,
                    "speed_mps": round(2 * 0.7 * H * math.sin(0.35) * 2 / (n / FPS), 2)}

    n = max(10, int(round(0.38 * math.sqrt(size) * FPS)))
    def fly(t):
        a = 0.75 * sn(t)
        p = flap({"LegL": rx(0.9), "LegR": rx(0.9), "Tail1": rx(0.05 * sn(t))}, a + 0.1, 0.45 * sn(t - 0.12))
        p["Body"] = (rx(-0.1), A.world_loc("Body", (0, 0, -0.06 * span * sn(t))))
        p["Head"] = rx(0.15)
        return p
    A.make("fly", n, fly)
    info["fly"] = {"frames": n + 1, "seconds": round(n / FPS, 3), "loop": True,
                   "note": "крылья машут на месте; полёт (высота, путь) задаёт игра"}

    n = 45
    def eat(t):
        x = (t * 3) % 1
        k = math.sin(math.pi * min(1, x / 0.6)) if x < 0.6 else 0
        p = fold({})
        p["Body"] = (rx(0.35 * k + 0.1), None)
        p["Head"] = rx(0.6 * k)
        p["Tail1"] = rx(-0.3 * k)
        return p
    A.make("eat", n, eat)
    info["eat"] = {"frames": n + 1, "seconds": n / FPS, "loop": True}


    # взлетает: присел → прыжок вверх с сильными взмахами (подъём — 1,5 высоты птицы; дальше игра ведёт полёт)
    n = 30
    def takeoff(t):
        crouch = ease(t / 0.2) * (1 - ease((t - 0.2) / 0.1))
        rise = ease((t - 0.25) / 0.75)
        open_ = ease((t - 0.1) / 0.2)
        p = fold({}, 1 - open_) if open_ < 1 else {}
        if open_ > 0:
            a = 0.85 * sn(3 * t)
            for sd in ("L", "R"):
                q1 = A.world_rot(f"Wing{sd}1", wing(sd, F[0] * (1 - open_), F[1] * (1 - open_) - a * open_))
                q2 = A.world_rot(f"Wing{sd}2", wing(sd, F[2] * (1 - open_), -0.4 * sn(3 * t - 0.12) * open_))
                p[f"Wing{sd}1"], p[f"Wing{sd}2"] = q1, q2
        p["Body"] = (rx(0.2 * crouch - 0.25 * rise), A.world_loc("Body", (0, 0, -0.25 * H * crouch + 1.5 * H * rise)))
        p["LegL"] = p["LegR"] = rx(0.9 * rise)
        p["Head"] = rx(-0.2 * crouch + 0.15 * rise)
        return p
    A.make("takeoff", n, takeoff, loop=False)
    info["takeoff"] = {"frames": n + 1, "seconds": n / FPS, "loop": False, "rise_m": round(1.5 * H, 2),
                       "note": "дальше — fly / glide; подъём на rise_m уже внутри анимации"}

    # парит: крылья раскрыты, лёгкое покачивание
    n = 90
    def glide(t):
        p = flap({"LegL": rx(0.9), "LegR": rx(0.9)}, 0.12 + 0.05 * sn(t), 0.05 * sn(t - 0.1))
        p["Body"] = (Quaternion((0, 1, 0), 0.08 * sn(t)) @ rx(-0.05), A.world_loc("Body", (0, 0, 0.04 * span * sn(t))))
        p["Tail1"] = rz(0.1 * sn(t))
        p["Head"] = rz(0.15 * sn(t + 0.25))
        return p
    A.make("glide", n, glide)
    info["glide"] = {"frames": n + 1, "seconds": n / FPS, "loop": True}

    # сидит (нахохлился) и спит (голова под крыло)
    n = 75
    def sit(t):
        p = fold({})
        p["Body"] = (rx(-0.05), A.world_loc("Body", (0, 0, -0.35 * H + 0.01 * H * sn(3 * t))))
        p["LegL"] = p["LegR"] = rx(-0.6)
        p["Head"] = rz(0.4 * sn(t)) @ rx(0.1)
        return p
    A.make("sit", n, sit)
    info["sit"] = {"frames": n + 1, "seconds": n / FPS, "loop": True}

    n = 120
    def sleep(t):
        p = fold({})
        p["Body"] = (rx(0.02 * sn(2 * t)), A.world_loc("Body", (0, 0, -0.38 * H + 0.012 * H * sn(2 * t))))
        p["LegL"] = p["LegR"] = rx(-0.6)
        p["Head"] = rz(2.3) @ rx(0.5)                       # голова повёрнута назад, к крылу
        return p
    A.make("sleep", n, sleep)
    info["sleep"] = {"frames": n + 1, "seconds": n / FPS, "loop": True}

    # атакует: крылья вверх, бросок вперёд и клевок
    n = 24
    reach = 0.4 * float(lay["L"])
    def attack(t):
        up = ease(t / 0.3) * (1 - ease((t - 0.7) / 0.3))
        fwd = ease((t - 0.3) / 0.15) * (1 - ease((t - 0.55) / 0.3))
        p = flap({}, 0.6 * up + 0.3 * up * sn(4 * t), 0.3 * up)
        if up < 0.05:
            p = fold({})
        p["Body"] = (rx(0.35 * fwd), A.world_loc("Body", (0, -reach * fwd, 0.2 * H * up)))
        p["Head"] = rx(0.6 * fwd - 0.2 * up)
        p["Tail1"] = rx(0.3 * up)
        return p
    A.make("attack", n, attack, loop=False)
    info["attack"] = {"frames": n + 1, "seconds": n / FPS, "loop": False, "hit_at_s": round(0.42 * n / FPS, 2)}

    # убегает по земле: быстрые прыжки с полураскрытыми, машущими крыльями
    n = max(8, int(round(0.28 * math.sqrt(size) * FPS)))
    def flee(t):
        p = flap({}, 0.35 + 0.45 * sn(2 * t), 0.25 * sn(2 * t - 0.12))
        up = max(0.0, sn(2 * t)) * 0.25 * H
        p["Body"] = (rx(0.15), A.world_loc("Body", (0, 0, up)))
        p["LegL"] = rx(-0.5 * sn(t))
        p["LegR"] = rx(0.5 * sn(t))
        p["Head"] = rx(-0.1)
        return p
    A.make("flee", n, flee)
    info["flee"] = {"frames": n + 1, "seconds": round(n / FPS, 3), "loop": True,
                    "speed_mps": round(2 * 2 * 0.7 * H * math.sin(0.5) * 2 / (n / FPS), 2)}

    n = 15
    def hit(t):
        k = math.sin(math.pi * min(1, t / 0.9)) * (1 - t) ** 0.5
        p = fold({}, 1 - 0.6 * k)
        p["Body"] = (rx(-0.25 * k), A.world_loc("Body", (0, 0.1 * span * k, 0)))
        p["Head"] = rx(-0.3 * k)
        return p
    A.make("hit", n, hit, loop=False)
    info["hit"] = {"frames": n + 1, "seconds": n / FPS, "loop": False}

    n = 30
    def death(t):
        a = ease(t / 0.7)
        p = fold({})
        roll = A.world_rot("Body", Quaternion((0, 1, 0), 1.5 * a))
        p["Body"] = (roll, A.world_loc("Body", (0, 0, -0.55 * H * a)))
        p["Head"] = rx(0.6 * a)
        p["LegL"] = rx(0.7 * a)
        p["LegR"] = rx(0.5 * a)
        return p
    A.make("death", n, death, loop=False)
    info["death"] = {"frames": n + 1, "seconds": n / FPS, "loop": False}
    return info


# ───────────────────────── выгрузка и превью ─────────────────────────

def export(obj, arm, path):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_yup=True,
                              export_animations=True, export_animation_mode="NLA_TRACKS", export_skins=True,
                              export_image_format="JPEG", export_jpeg_quality=85)
    return os.path.getsize(path) / 1e6


def rig(name):
    obj = load(name)
    P = verts(obj)
    if name in BIRDS:
        lay = bird_layout(P)
        arm = build_armature(obj, bird_bones(lay), bird_allow(lay))
        kind = "bird"
    else:
        lay = quad_layout(P)
        arm = build_armature(obj, quad_bones(lay), quad_allow(lay))
        kind = "hop" if name in HOP else "quad"
    arm.animation_data_create()
    info = bird_anims(arm, lay) if kind == "bird" else quad_anims(arm, lay, kind, name)
    out = os.path.join(ROOT, "export", f"{name}_idle.glb")
    mb = export(obj, arm, out)
    tris = sum(len(p.vertices) - 2 for p in obj.data.polygons)
    print(f"[{name}] {kind}: костей {len(arm.data.bones)}, анимаций {len(info)}, {tris} треуг., {mb:.2f} МБ", flush=True)
    return {"kind": kind, "bones": len(arm.data.bones), "mb": round(mb, 2), "animations": info}, obj, arm


PREVIEW = {"quad": [("rest", None, 0), ("sit", "sit", 0.25), ("lie_down", "lie_down", 1.0), ("sleep", "sleep", 0.3),
                    ("flee", "flee", 0.3), ("attack", "attack", 0.45), ("growl", "growl", 0.3), ("howl", "howl", 0.5),
                    ("beg", "beg", 0.3)],
           "bird": [("rest", None, 0), ("takeoff", "takeoff", 0.5), ("glide", "glide", 0.25), ("sit", "sit", 0.2),
                    ("sleep", "sleep", 0.3), ("attack", "attack", 0.45), ("flee", "flee", 0.25)]}
PREVIEW["hop"] = PREVIEW["quad"]


def preview(name, kind, obj, arm, tmp):
    sys.path.insert(0, HERE)
    import tripo_process as tp
    sc = bpy.context.scene
    outs = []
    for tag, act, t in PREVIEW[kind]:
        if act and act not in bpy.data.actions:
            continue
        for tr in arm.animation_data.nla_tracks:
            tr.mute = True
        if act:
            a = bpy.data.actions[act]
            arm.animation_data.action = a
            try:
                arm.animation_data.action_slot = a.slots[0]
            except (AttributeError, IndexError):
                pass
            f0, f1 = a.frame_range
            sc.frame_set(int(round(f0 + (f1 - f0) * t)))
        else:
            arm.animation_data.action = None
            for pb in arm.pose.bones:
                pb.rotation_quaternion = (1, 0, 0, 0)
                pb.location = (0, 0, 0)
            sc.frame_set(0)
        bpy.context.view_layer.update()
        base = os.path.join(tmp, f"{name}_{tag}_{t}")
        outs += _render_side(tp, obj, base, kind)
    return outs


def _render_side(tp, obj, base, kind):
    """Кадр сбоку-спереди (3/4) со светом — как у tripo_process, но с позой скелета."""
    dg = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev)
    tmp = bpy.data.objects.new("_posed", me)
    bpy.context.scene.collection.objects.link(tmp)
    obj.hide_render = True
    rest = tp.bbox
    try:
        os.environ["TRIPO_FAST"] = "1"
        d = Matrix.Rotation(math.radians(-60), 3, "Z") @ Matrix.Rotation(math.radians(-15), 3, "X") @ Vector((0, -1, 0))
        out = _render(tp, tmp, base, d)
    finally:
        obj.hide_render = False
        bpy.data.objects.remove(tmp)
    return [out]


def _render(tp, obj, base, d):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 16
    try:
        sc.cycles.use_denoising, sc.cycles.denoiser = True, "OPENIMAGEDENOISE"
    except Exception:
        sc.cycles.use_denoising = False
    sc.render.resolution_x = sc.render.resolution_y = 260
    sc.view_settings.view_transform = "AgX"
    if sc.world is None:
        sc.world = bpy.data.worlds.new("w")
    sc.world.color = (0.03, 0.035, 0.06)
    P = np.array([tuple(v.co) for v in obj.data.vertices])
    lo, hi = P.min(0), P.max(0)
    st = getattr(_render, "frame", None)
    if st is None or st[0] != base.split("_")[0]:
        pass
    c = Vector(((lo + hi) / 2).tolist())
    size = float(max(hi - lo))
    ref = getattr(_render, "ref", None)
    if ref is not None:
        c, size, z0 = ref
    else:
        z0 = float(lo[2])
    added = []
    fm = bpy.data.meshes.new("_floor")
    fm.from_pydata([(-500, -500, z0), (500, -500, z0), (500, 500, z0), (-500, 500, z0)], [], [(0, 1, 2, 3)])
    mat = bpy.data.materials.new("_floor")
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.035, 0.035, 0.04, 1)
    fm.materials.append(mat)
    fo = bpy.data.objects.new("_floor", fm)
    sc.collection.objects.link(fo)
    added.append(fo)
    lamp = bpy.data.lights.new("_lamp", "POINT")
    lamp.energy, lamp.shadow_soft_size, lamp.color = 300.0 * size * size, 0.2 * size, (1.0, 0.72, 0.45)
    lo_ = bpy.data.objects.new("_lamp", lamp)
    lo_.location = c + Vector((-0.7 * size, -1.0 * size, 1.1 * size))
    sc.collection.objects.link(lo_)
    added.append(lo_)
    fill = bpy.data.lights.new("_fill", "AREA")
    fill.energy, fill.size, fill.color = 45.0 * size * size, 2.0 * size, (0.5, 0.6, 1.0)
    fl = bpy.data.objects.new("_fill", fill)
    fl.location = c + Vector((1.2 * size, -1.2 * size, 0.6 * size))
    fl.rotation_euler = (math.radians(70), 0, math.radians(45))
    sc.collection.objects.link(fl)
    added.append(fl)
    cam_d = bpy.data.cameras.new("_cam")
    cam_d.type = "ORTHO"
    cam = bpy.data.objects.new("_cam", cam_d)
    sc.collection.objects.link(cam)
    sc.camera = cam
    added.append(cam)
    cam.location = c + d * (size * 4)
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    cam_d.ortho_scale = size * 1.25
    cam_d.clip_end = size * 20
    sc.render.filepath = base + ".png"
    bpy.ops.render.render(write_still=True)
    for o in added:
        bpy.data.objects.remove(o)
    return sc.render.filepath


def main(argv):
    sheet_arg = argv[argv.index("--sheet") + 1] if "--sheet" in argv else None
    names = [a for a in argv if not a.startswith("--") and a != sheet_arg] or ANIMALS
    do_prev = "--preview" in argv
    info_path = os.path.join(ROOT, "export", "anim", "animals_info.json")
    allinfo = json.load(open(info_path)) if os.path.exists(info_path) else {}
    rows = []
    tmp = os.path.join(ROOT, "renders", "_tmp_animals")
    os.makedirs(tmp, exist_ok=True)
    for n in names:
        rec, obj, arm = rig(n)
        allinfo[n] = rec
        if do_prev:
            # общий кадр по позе покоя: чтобы все кадры животного были в одном масштабе
            P = verts(obj)
            lo, hi = P.min(0), P.max(0)
            size = float(max(hi - lo)) * 1.15
            _render.ref = (Vector(((lo + hi) / 2).tolist()), size, float(lo[2]))
            ims = preview(n, rec["kind"], obj, arm, tmp)
            _render.ref = None
            tags = " · ".join(t for t, a, _ in PREVIEW[rec["kind"]] if a is None or a in bpy.data.actions)
            rows.append((f"{n}\n{rec['kind']}, костей {rec['bones']}, {rec['mb']} МБ · {tags}", ims))
    json.dump(dict(sorted(allinfo.items())), open(info_path, "w"), ensure_ascii=False, indent=1)
    if do_prev and rows:
        sys.path.insert(0, HERE)
        import tripo_process as tp
        import datetime
        out = os.path.join(ROOT, "renders", "_review", f"animals_{datetime.date.today()}.jpg")
        if sheet_arg:
            out = sheet_arg
        tp.sheet(rows, out.replace(".jpg", ".png"))
        from PIL import Image
        Image.open(out.replace(".jpg", ".png")).convert("RGB").save(out, quality=85)
        os.remove(out.replace(".jpg", ".png"))
        print("→", out)


if __name__ == "__main__":
    main(sys.argv[1:])
