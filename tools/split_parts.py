"""Разрезать одну модель Tripo на отдельные (ряд букв → letter_a…, набор дверей → door_1…).
Куски — связные части сетки, сгруппированные слева направо по X (что перекрывается по X — один знак: точка над i,
дырки в A/B). Каждый — отдельный export/<имя>_idle.glb: низ на полу (Z = 0), по центру, перед к −Y.

  python3 tools/split_parts.py tripo/letters_a_j.glb --names letter_a,letter_b,…,letter_j --height 1.0 --rot 270
  python3 tools/split_parts.py tripo/doors_set.glb --names door_1,…,door_6 --height 2.1 --rot 270

--box — вещи стоят друг над другом или в два ряда: группы по пересечению коробок в 3D, порядок — ряды сверху вниз,
в ряду слева направо. --k — вещи касаются друг друга (птицы крыльями): делить точки на N кучек по близости.

Высота: у букв — у самого высокого знака (все в одном масштабе); у дверей — у каждой своя (--each);
--height 0.08,0.6,0.36 — своя высота каждому куску по порядку имён.
"""
import math
import os
import sys

import bpy
import bmesh  # noqa: E402 — после bpy
import numpy as np
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tripo_process as T  # noqa: E402


def vertex_islands(obj):
    me = obj.data
    n = len(me.vertices)
    parent = np.arange(n)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    ev = np.empty(len(me.edges) * 2, dtype=np.int64)
    me.edges.foreach_get("vertices", ev)
    for a, b in ev.reshape(-1, 2):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    return np.array([find(i) for i in range(n)])


def groups_by_x(obj, want, min_share=0.002):
    """Кластеры островов по X: острова, чьи X-отрезки перекрываются, — один знак. Мелочь (< min_share вершин)
    приклеивается к ближайшему знаку."""
    lab = vertex_islands(obj)
    co = np.empty(len(obj.data.vertices) * 3)
    obj.data.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    isl = []
    for r in np.unique(lab):
        m = lab == r
        isl.append((r, co[m, 0].min(), co[m, 0].max(), int(m.sum())))
    big = [i for i in isl if i[3] >= min_share * len(co)]
    big.sort(key=lambda t: t[1])
    groups = []
    for r, a, b, n in big:
        if groups and a <= groups[-1]["b"] - 0.15 * (b - a):
            g = groups[-1]
            g["ids"].append(r)
            g["b"] = max(g["b"], b)
        else:
            groups.append({"ids": [r], "a": a, "b": b})
    # если знаков больше нужного — слить ближайшие по зазору
    while len(groups) > want:
        gaps = [groups[i + 1]["a"] - groups[i]["b"] for i in range(len(groups) - 1)]
        i = int(np.argmin(gaps))
        groups[i]["ids"] += groups[i + 1]["ids"]
        groups[i]["b"] = max(groups[i]["b"], groups[i + 1]["b"])
        del groups[i + 1]
    for r, a, b, n in isl:
        if n < min_share * len(co):
            c = (a + b) / 2
            j = min(range(len(groups)), key=lambda k: abs((groups[k]["a"] + groups[k]["b"]) / 2 - c))
            groups[j]["ids"].append(r)
    return lab, groups


def groups_by_box(obj, want, min_share=0.002, pad=0.01):
    """Кластеры островов по пересечению коробок в 3D (вещи друг над другом, ряды в два этажа).
    Порядок — сверху вниз по Z (рядами), в ряду слева направо по X."""
    lab = vertex_islands(obj)
    co = np.empty(len(obj.data.vertices) * 3)
    obj.data.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    isl = [(r, co[lab == r].min(0), co[lab == r].max(0), int((lab == r).sum())) for r in np.unique(lab)]
    big = [i for i in isl if i[3] >= min_share * len(co)]
    groups = [{"ids": [r], "lo": lo.copy(), "hi": hi.copy()} for r, lo, hi, n in big]
    merged = True
    while merged:
        merged = False
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                a, b = groups[i], groups[j]
                if np.all(a["lo"] - pad <= b["hi"]) and np.all(b["lo"] - pad <= a["hi"]):
                    a["ids"] += b["ids"]
                    a["lo"], a["hi"] = np.minimum(a["lo"], b["lo"]), np.maximum(a["hi"], b["hi"])
                    del groups[j]
                    merged = True
                    break
            if merged:
                break
    while len(groups) > want:                       # лишние — слить с ближайшим по центру
        c = [(g["lo"] + g["hi"]) / 2 for g in groups]
        s = min(range(len(groups)), key=lambda k: float(np.prod(groups[k]["hi"] - groups[k]["lo"])))
        j = min((k for k in range(len(groups)) if k != s), key=lambda k: float(np.linalg.norm(c[k] - c[s])))
        groups[j]["ids"] += groups[s]["ids"]
        groups[j]["lo"], groups[j]["hi"] = np.minimum(groups[j]["lo"], groups[s]["lo"]), np.maximum(groups[j]["hi"], groups[s]["hi"])
        del groups[s]
    for r, lo, hi, n in isl:
        if n < min_share * len(co):
            c = (lo + hi) / 2
            j = min(range(len(groups)), key=lambda k: float(np.linalg.norm((groups[k]["lo"] + groups[k]["hi"]) / 2 - c)))
            groups[j]["ids"].append(r)
    zs = sorted(groups, key=lambda g: -g["hi"][2])
    rows = []
    for g in zs:                                    # ряды: перекрываются по Z — один ряд
        for row in rows:
            if g["lo"][2] < row[0]["hi"][2] and g["hi"][2] > row[0]["lo"][2]:
                row.append(g)
                break
        else:
            rows.append([g])
    return lab, [g for row in rows for g in sorted(row, key=lambda g: g["lo"][0])]


def groups_by_k(obj, want, min_share=0.002):
    """Вещи касаются друг друга (птицы крыльями): точки делятся на want кучек по близости (k-средних),
    кусок сетки целиком идёт в кучку, где больше его точек. Порядок — ряды сверху вниз, в ряду слева направо."""
    lab = vertex_islands(obj)
    co = np.empty(len(obj.data.vertices) * 3)
    obj.data.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    best = None                                     # лучший из 8 случайных стартов
    for seed in range(8):
        c = co[np.random.default_rng(seed).choice(len(co), want, replace=False)]
        for _ in range(30):
            a = np.argmin(((co[:, None, :] - c[None]) ** 2).sum(-1), 1)
            c = np.array([co[a == k].mean(0) if (a == k).any() else c[k] for k in range(want)])
        err = float(((co - c[a]) ** 2).sum())
        if best is None or err < best[0]:
            best = (err, a)
    a = best[1]
    groups = [{"ids": [], "lo": None, "hi": None} for _ in range(want)]
    for r in np.unique(lab):
        m = lab == r
        k = int(np.bincount(a[m], minlength=want).argmax())
        groups[k]["ids"].append(r)
    for g in groups:
        m = np.isin(lab, g["ids"])
        g["lo"], g["hi"] = co[m].min(0), co[m].max(0)
    groups = [g for g in groups if g["ids"]]
    rows = []
    for g in sorted(groups, key=lambda g: -g["hi"][2]):
        for row in rows:
            if g["lo"][2] < row[0]["hi"][2] and g["hi"][2] > row[0]["lo"][2]:
                row.append(g)
                break
        else:
            rows.append([g])
    return lab, [g for row in rows for g in sorted(row, key=lambda g: g["lo"][0])]


def split(path, names, height, rot, each=False, out_dir=None, mode="x"):
    out_dir = out_dir or os.path.join(T.ROOT, "export")
    obj, _ = T.import_joined(path)
    T.clear_custom_normals(obj)
    if rot:
        obj.data.transform(Matrix.Rotation(math.radians(rot), 4, "Z"))
    lab, groups = {"box": groups_by_box, "k": groups_by_k}.get(mode, groups_by_x)(obj, len(names))
    if len(groups) != len(names):
        print(f"  ⚠ {os.path.basename(path)}: нашлось {len(groups)} кусков, а имён {len(names)} — проверить по превью")
    lo, hi = T.bbox(obj)
    hs = list(height) if isinstance(height, (list, tuple)) else None    # своя высота у каждого куска
    k_all = (hs[0] if hs else height) / float(hi[2] - lo[2])
    results = []
    for i, (g, name) in enumerate(zip(groups, names)):
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        keep = np.isin(lab, g["ids"])
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not keep[v.index]], context="VERTS")
        me = bpy.data.meshes.new(name)
        bm.to_mesh(me)
        bm.free()
        for m in obj.data.materials:
            me.materials.append(m)
        part = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(part)
        plo, phi = T.bbox(part)
        k = (hs[i] if hs else height) / float(phi[2] - plo[2]) if (each or hs) else k_all
        me.transform(Matrix.Scale(k, 4))
        plo, phi = T.bbox(part)
        me.transform(Matrix.Translation(Vector((-(plo[0] + phi[0]) / 2, -(plo[1] + phi[1]) / 2, -plo[2]))))
        me.update()
        t1 = T.decimate(part, 3000)
        T.smooth_by_angle(part)
        T.fix_materials(part, 1024)
        mb, _ = T.export(part, os.path.join(out_dir, name + "_idle.glb"))
        plo, phi = T.bbox(part)
        d = phi - plo
        print(f"[{name}_idle] {t1} треуг., {d[0] * 100:.0f}×{d[1] * 100:.0f}×{d[2] * 100:.0f} см, {mb:.2f} МБ", flush=True)
        results.append((name, part))
        part.hide_render = True
    obj.hide_render = True
    return results


def main(argv):
    path = argv[0]
    names = argv[argv.index("--names") + 1].split(",")
    height = [float(x) for x in argv[argv.index("--height") + 1].split(",")] if "--height" in argv else [1.0]
    height = height[0] if len(height) == 1 else height
    rot = float(argv[argv.index("--rot") + 1]) if "--rot" in argv else 0
    split(path, names, height, rot, each="--each" in argv, mode="box" if "--box" in argv else "k" if "--k" in argv else "x")


if __name__ == "__main__":
    main(sys.argv[1:])
