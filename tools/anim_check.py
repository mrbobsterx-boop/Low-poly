"""Проверка анимаций на персонаже «как в игре» (Godot): кадр собирается прямо из glTF, без пересчёта Blender.

  python3 tools/anim_check.py --char export/char_gr_m_idle.glb --anims export/anim/anims_mixamo.glb \
      --act walk run idle --t 0.0 0.25 0.5 --out renders/_review/x.jpg [--mode godot|rot]

Godot при проигрывании ставит кости ровно как записано в анимации (положение, поворот, размер каждой кости).
Здесь так же: локальное положение кости = из анимации (если там есть дорожка), иначе — своё; дальше обычная «шкура»
(вершины по весам костей). --mode rot — из анимации берутся только повороты (+ положение Hips), положения остальных
костей — свои (так анимация не меняет пропорции персонажа).
Несколько файлов анимаций можно сравнить: --anims a.glb b.glb (каждый — свой ряд).
"""
import json
import math
import os
import struct
import sys

import bpy
import numpy as np
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
CT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


class GLB:
    def __init__(self, path):
        b = open(path, "rb").read()
        jl = struct.unpack("<I", b[12:16])[0]
        self.j = json.loads(b[20:20 + jl])
        self.bin = b[20 + jl + 8:]
        self.name = os.path.basename(path)

    def acc(self, i):
        a = self.j["accessors"][i]
        bv = self.j["bufferViews"][a["bufferView"]]
        dt = CT[a["componentType"]]
        n = NC[a["type"]]
        off = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
        stride = bv.get("byteStride", 0)
        isz = np.dtype(dt).itemsize * n
        if stride and stride != isz:
            raw = np.frombuffer(self.bin, np.uint8, a["count"] * stride, off).reshape(-1, stride)[:, :isz]
            arr = np.frombuffer(raw.tobytes(), dt).reshape(a["count"], n)
        else:
            arr = np.frombuffer(self.bin, dt, a["count"] * n, off).reshape(a["count"], n)
        arr = arr.astype(np.float64)
        if a.get("normalized"):
            arr /= np.iinfo(dt).max
        return arr

    def image(self, i, out):
        im = self.j["images"][i]
        bv = self.j["bufferViews"][im["bufferView"]]
        data = self.bin[bv.get("byteOffset", 0): bv.get("byteOffset", 0) + bv["byteLength"]]
        ext = ".png" if "png" in im.get("mimeType", "") else ".jpg"
        open(out + ext, "wb").write(data)
        return out + ext


def q2m(q):
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def trs(t, r, s):
    m = np.eye(4)
    m[:3, :3] = q2m(r) * np.asarray(s)
    m[:3, 3] = t
    return m


def node_trs(n):
    if "matrix" in n:
        M = np.array(n["matrix"]).reshape(4, 4).T
        t = M[:3, 3]
        s = np.linalg.norm(M[:3, :3], axis=0)
        from mathutils import Matrix as BM
        q = BM((M[:3, :3] / s).tolist()).to_quaternion()
        return list(t), [q.x, q.y, q.z, q.w], list(s)
    return n.get("translation", [0, 0, 0]), n.get("rotation", [0, 0, 0, 1]), n.get("scale", [1, 1, 1])


def sample(g, anim, t):
    """{имя узла: {path: значение}} в момент t (доля длины 0..1)."""
    out, tmax = {}, 0.0
    for s in anim["samplers"]:
        tmax = max(tmax, g.acc(s["input"])[-1, 0])
    T = t * tmax
    for ch in anim["channels"]:
        s = anim["samplers"][ch["sampler"]]
        ti = g.acc(s["input"])[:, 0]
        v = g.acc(s["output"])
        path = ch["target"]["path"]
        k = int(np.searchsorted(ti, T, "right") - 1)
        k = min(max(k, 0), len(ti) - 1)
        if s.get("interpolation") == "STEP" or k == len(ti) - 1:
            val = v[k]
        else:
            u = (T - ti[k]) / max(ti[k + 1] - ti[k], 1e-9)
            a, b = v[k], v[k + 1]
            if path == "rotation":
                if np.dot(a, b) < 0:
                    b = -b
                val = a * (1 - u) + b * u
                val /= np.linalg.norm(val)
            else:
                val = a * (1 - u) + b * u
        out.setdefault(g.j["nodes"][ch["target"]["node"]]["name"], {})[path] = val
    return out


def hips_y(g):
    """Высота Hips в покое (glTF, Y вверх) — по цепочке родителей."""
    nodes = g.j["nodes"]
    parent = {c: i for i, n in enumerate(nodes) for c in n.get("children", [])}
    i = next(k for k, n in enumerate(nodes) if n.get("name", "").endswith("Hips"))
    M = np.eye(4)
    while True:
        M = trs(*node_trs(nodes[i])) @ M
        if i not in parent:
            break
        i = parent[i]
    return M[1, 3]


def rz(deg):
    a = math.radians(deg)
    return np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])


def posed(char, pose, mode, ms=1.0, spread=0.0, parts=False):
    j = char.j
    nodes = j["nodes"]
    parent = {}
    for i, n in enumerate(nodes):
        for c in n.get("children", []):
            parent[c] = i
    local = []
    for i, n in enumerate(nodes):
        t, r, s = node_trs(n)
        p = pose.get(n.get("name"), {})
        if "rotation" in p:
            r = p["rotation"]
        if mode == "godot" or n.get("name", "").endswith("Hips"):
            t = p.get("translation", t)
            if "translation" in p and n.get("name", "").endswith("Hips"):
                t = np.asarray(t) * ms                     # Skeleton3D.motion_scale
            s = p.get("scale", s)
        local.append(trs(t, r, s))
    glob = [None] * len(nodes)

    def G(i):
        if glob[i] is None:
            pg = G(parent[i]) if i in parent else np.eye(4)
            nm = nodes[i].get("name", "")
            if spread and (nm.endswith("LeftArm") or nm.endswith("RightArm")):
                R = pg[:3, :3] / np.linalg.norm(pg[:3, :3], axis=0)   # отвести плечо наружу (ось «вперёд» = +Z)
                local[i] = local[i].copy()
                local[i][:3, :3] = R.T @ rz(spread if nm.endswith("LeftArm") else -spread) @ R @ local[i][:3, :3]
            glob[i] = pg @ local[i]
        return glob[i]
    skin = j["skins"][0]
    ibm = char.acc(skin["inverseBindMatrices"]).reshape(-1, 4, 4).transpose(0, 2, 1)
    J = np.array([G(ji) @ ibm[k] for k, ji in enumerate(skin["joints"])])
    meshes = []
    for ni, n in enumerate(nodes):
        if "mesh" not in n or "skin" not in n:
            continue
        for prim in j["meshes"][n["mesh"]]["primitives"]:
            at = prim["attributes"]
            P = char.acc(at["POSITION"])
            JI = char.acc(at["JOINTS_0"]).astype(int)
            W = char.acc(at["WEIGHTS_0"])
            M = np.einsum("vk,vkij->vij", W, J[JI])
            Ph = np.c_[P, np.ones(len(P))]
            Q = np.einsum("vij,vj->vi", M, Ph)[:, :3]
            if parts:
                jn = [nodes[k].get("name", "").split(":")[-1] for k in skin["joints"]]
                meshes.append((Q, np.array(jn)[JI[np.arange(len(JI)), W.argmax(1)]]))
                continue
            idx = char.acc(prim["indices"]).astype(int).ravel()
            uv = char.acc(at["TEXCOORD_0"]) if "TEXCOORD_0" in at else None
            meshes.append((Q, idx, uv, prim.get("material")))
    return meshes


def to_blender(meshes, char, tex_cache):
    objs = []
    for Q, idx, uv, mi in meshes:
        V = [(x, -z, y) for x, y, z in Q]                 # glTF (Y вверх) → Blender (Z вверх)
        F = idx.reshape(-1, 3).tolist()
        me = bpy.data.meshes.new("p")
        me.from_pydata(V, [], F)
        if uv is not None:
            ul = me.uv_layers.new()
            loops = np.array([l.vertex_index for l in me.loops])
            ul.data.foreach_set("uv", np.c_[uv[loops, 0], 1 - uv[loops, 1]].ravel())
        mat = bpy.data.materials.new("m")
        bs = mat.node_tree.nodes["Principled BSDF"]
        bs.inputs["Roughness"].default_value = 0.8
        try:
            ti = char.j["materials"][mi]["pbrMetallicRoughness"]["baseColorTexture"]["index"]
            src = char.j["textures"][ti]["source"]
            if src not in tex_cache:
                p = char.image(src, os.path.join(bpy.app.tempdir or "/tmp", f"tex_{id(char)}_{src}"))
                tex_cache[src] = bpy.data.images.load(p)
            tn = mat.node_tree.nodes.new("ShaderNodeTexImage")
            tn.image = tex_cache[src]
            mat.node_tree.links.new(tn.outputs["Color"], bs.inputs["Base Color"])
        except (KeyError, TypeError, IndexError):
            bs.inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1)
        me.materials.append(mat)
        o = bpy.data.objects.new("p", me)
        bpy.context.scene.collection.objects.link(o)
        objs.append(o)
    return objs


def render(objs, out, ref):
    sys.path.insert(0, HERE)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 16
    try:
        sc.cycles.use_denoising, sc.cycles.denoiser = True, "OPENIMAGEDENOISE"
    except Exception:
        sc.cycles.use_denoising = False
    sc.render.resolution_x = sc.render.resolution_y = 300 if "--zoom" not in sys.argv else 420
    sc.view_settings.view_transform = "AgX"
    if sc.world is None:
        sc.world = bpy.data.worlds.new("w")
    sc.world.color = (0.05, 0.055, 0.08)
    c, size, z0, yaw = ref
    added = []
    fm = bpy.data.meshes.new("_floor")
    fm.from_pydata([(-50, -50, z0), (50, -50, z0), (50, 50, z0), (-50, 50, z0)], [], [(0, 1, 2, 3)])
    fo = bpy.data.objects.new("_floor", fm)
    sc.collection.objects.link(fo)
    added.append(fo)
    lamp = bpy.data.lights.new("_lamp", "SUN")
    lamp.energy = 3.0
    lo = bpy.data.objects.new("_lamp", lamp)
    lo.rotation_euler = (math.radians(50), 0, math.radians(-30))
    sc.collection.objects.link(lo)
    added.append(lo)
    cam_d = bpy.data.cameras.new("_cam")
    cam_d.type = "ORTHO"
    cam = bpy.data.objects.new("_cam", cam_d)
    sc.collection.objects.link(cam)
    sc.camera = cam
    added.append(cam)
    d = Matrix.Rotation(math.radians(yaw), 3, "Z") @ Matrix.Rotation(math.radians(-8), 3, "X") @ Vector((0, -1, 0))
    cam.location = c + d * (size * 4)
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    cam_d.ortho_scale = size
    cam_d.clip_end = size * 20
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    for o in added + objs:
        bpy.data.objects.remove(o)
    return out


def main(argv):
    def arg(name, many=False, default=None):
        if name not in argv:
            return default
        i = argv.index(name) + 1
        if not many:
            return argv[i]
        out = []
        while i < len(argv) and not argv[i].startswith("--"):
            out.append(argv[i])
            i += 1
        return out
    chars = arg("--char", True)
    anims = arg("--anims", True)
    acts = arg("--act", True)
    ts = [float(x) for x in arg("--t", True, ["0.25"])]
    modes = arg("--mode", True, ["godot"])
    yaw = float(arg("--yaw", default="-90"))
    out = arg("--out")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    tmp = os.path.join(os.path.dirname(os.path.abspath(out)), "_tmp_check")
    os.makedirs(tmp, exist_ok=True)
    rows = []
    for cp in chars:
        char = GLB(cp)
        tex = {}
        rest = posed(char, {}, "godot")
        P = np.vstack([m[0] for m in rest])
        lo, hi = P.min(0), P.max(0)
        h = hi[1] - lo[1]
        ref = (Vector((0, 0, (lo[1] + hi[1]) / 2)), h * 1.25, float(lo[1]), yaw)
        if "--zoom" in argv:                               # крупно: верх тела (плечи, локти)
            ref = (Vector((0, 0, lo[1] + 0.68 * h)), h * 0.55, float(lo[1]), yaw)
        for ap in anims:
            g = GLB(ap)
            by = {a["name"]: a for a in g.j["animations"]}
            for mode in modes:
                for act in acts:
                    if act == "rest":
                        by["rest"] = None
                    elif act not in by:
                        print("нет действия", act, "в", g.name)
                        continue
                    ims = []
                    for t in ts:
                        pose = sample(g, by[act], t) if by[act] else {}
                        ms = hips_y(char) / hips_y(g) if "--ms" in argv else 1.0
                        sp = 0.0
                        if "--fit" in argv:
                            fit = json.load(open(argv[argv.index("--fit") + 1]))["characters"]
                            sp = fit.get(os.path.basename(cp)[:-9], {}).get("arm_spread_deg", 0.0)
                        objs = to_blender(posed(char, pose, mode, ms, sp), char, tex)
                        p = os.path.join(tmp, f"{len(rows)}_{t}.png")
                        ims.append(render(objs, p, ref))
                    rows.append((f"{os.path.basename(cp)} · {act} · {g.name} · {mode}", ims))
                    print("ряд:", rows[-1][0], flush=True)
    sys.path.insert(0, HERE)
    import tripo_process as tp
    tp.sheet(rows, out.replace(".jpg", ".png"))
    from PIL import Image
    Image.open(out.replace(".jpg", ".png")).convert("RGB").save(out, quality=85)
    os.remove(out.replace(".jpg", ".png"))
    print("→", out)


if __name__ == "__main__":
    main(sys.argv[1:])
