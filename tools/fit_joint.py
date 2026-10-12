"""Уголки и стыки (docs/TRIPO_BATCH_2026-10-12.md, раздел 2): сечение веток = сечению прямого куска.

  python3 tools/fit_joint.py <уголок> <прямой_гориз> [<прямой_верт>] [--stand] [--caps] [--out <имя>] [--src <папка>]

--src — откуда брать уголок (по умолчанию export/; файл в export/ перезаписывается, поэтому для повтора — копия).

Меряет толщину пучка (трубы) или короба по срезам — без хомутов и фланцев (берётся нижняя четверть толщин по срезам,
хомут и фланец толще), — у прямого куска и у веток уголка, и масштабирует уголок по каждой оси отдельно:
  ширина вертикальной ветки = толщине вертикального прямого (нет его — высоте горизонтального, короб повёрнутый);
  толщина горизонтальной ветки = высоте горизонтального прямого; глубина = глубине горизонтального прямого.
Центр стыка — в начале координат, ветки по X и Y (в игре; в Blender — X и Z), задняя сторона — к стене
(в игре z = 0 сзади, как у прямых кусков). --stand — модель лежит (ветки к зрителю): поставить в плоскость стены.
--caps — заглушки: только горизонтальная ветка, длина в том же масштабе, что высота.
"""
import math
import os
import sys

import bpy
import numpy as np
from mathutils import Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tripo_process as T  # noqa: E402

EXPORT = os.path.join(T.ROOT, "export")
Q = 25          # процентиль толщин по срезам: хомуты и фланцы толще пучка


def verts(obj):
    co = np.empty(len(obj.data.vertices) * 3)
    obj.data.vertices.foreach_get("co", co)
    return co.reshape(-1, 3)


def slices(co, along, across, lo=None, hi=None, n=60):
    """Срезы поперёк оси along: для каждого — (мин, макс) по осям across. Только внутри [lo, hi] по along."""
    a = co[:, along]
    lo = a.min() if lo is None else lo
    hi = a.max() if hi is None else hi
    step = (hi - lo) / n
    out = []
    for k in range(n):
        m = (a >= lo + k * step) & (a < lo + (k + 1) * step)
        if m.sum() < 20:
            continue
        out.append([(co[m, ax].min(), co[m, ax].max()) for ax in across])
    return out


def section(sl, i):
    """Толщина и центр пучка по оси i из срезов: Q-й процентиль толщины, центр — у срезов этой толщины."""
    th = np.array([s[i][1] - s[i][0] for s in sl])
    t = float(np.percentile(th, Q))
    near = [s for s, x in zip(sl, th) if abs(x - t) <= 0.08 * t] or sl
    c = float(np.median([(s[i][0] + s[i][1]) / 2 for s in near]))
    return t, c


def align_yaw(obj):
    """Повернуть вокруг вертикали так, чтобы ветки шли по осям: преобладающее направление рёбер сверху (короб —
    рёбра вдоль веток), углы по модулю 90°, взвешены длиной."""
    co = verts(obj)
    ev = np.empty(len(obj.data.edges) * 2, dtype=np.int64)
    obj.data.edges.foreach_get("vertices", ev)
    d = co[ev[1::2], :2] - co[ev[0::2], :2]
    ln = np.hypot(d[:, 0], d[:, 1])
    ang = np.degrees(np.arctan2(d[:, 1], d[:, 0])) % 90
    hist, edges = np.histogram(ang, bins=360, range=(0, 90), weights=ln)
    hist = np.convolve(np.r_[hist[-4:], hist, hist[:4]], np.ones(9), "valid")      # сгладить по кругу
    best = float(edges[int(np.argmax(hist))] + 0.125)
    best = best - 90 if best > 45 else best
    obj.data.transform(Matrix.Rotation(math.radians(-best), 4, "Z"))
    return best


def load(name, src=EXPORT):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    obj, _ = T.import_joined(os.path.join(src, name + "_idle.glb"))
    return obj


def straight_h(name):
    """Горизонтальный прямой кусок (вдоль X): высота (Z) и глубина (Y) пучка."""
    co = verts(load(name))
    sl = slices(co, 0, (2, 1))
    return section(sl, 0)[0], section(sl, 1)[0]


def straight_v(name):
    """Вертикальный прямой кусок (вдоль Z): ширина (X) и глубина (Y)."""
    co = verts(load(name))
    sl = slices(co, 2, (0, 1))
    return section(sl, 0)[0], section(sl, 1)[0]


def fit(joint, h_name, v_name=None, stand=False, caps=False, out=None, src=EXPORT):
    th_h, dp_h = straight_h(h_name)
    tw_v, dp_v = straight_v(v_name) if v_name else (th_h, dp_h)
    obj = load(joint, src)
    if stand:                                   # лежит: выровнять по осям, верх к зрителю → ветки в плоскости стены
        yaw = align_yaw(obj)
        if abs(yaw) > 0.1:
            print(f"  {joint}: повёрнут на {yaw:.1f}° — ветки выровнены по осям", flush=True)
        obj.data.transform(Matrix.Rotation(math.radians(-90), 4, "X"))
    co = verts(obj)
    lo, hi = co.min(0), co.max(0)
    # горизонтальная ветка: срезы по X во внешних частях (без середины, где вертикальная ветка)
    cx_mid = (lo[0] + hi[0]) / 2
    w = hi[0] - lo[0]                       # срезы только через ветку: тоньше 0,6 всей модели (не через другую ветку)
    ht = hi[2] - lo[2]
    hsl = [s for s in slices(co, 0, (2, 1, 0)) if s[0][1] - s[0][0] < 0.6 * ht] if not caps else slices(co, 0, (2, 1, 0))
    t_h, c_z = section(hsl, 0)
    d_h, _ = section(hsl, 1)
    sz, sy = th_h / t_h, dp_h / d_h
    if caps:
        sx, c_x, t_v = sz, cx_mid, None
    else:
        vsl = [s for s in slices(co, 2, (0, 1, 2)) if s[0][1] - s[0][0] < 0.6 * w]   # срезы только через ветку
        t_v, c_x = section(vsl, 0)
        sx = tw_v / t_v
    obj.data.transform(Matrix.Translation((-c_x, 0, -c_z)))
    obj.data.transform(Matrix.Diagonal((sx, sy, sz, 1)))
    co = verts(obj)
    obj.data.transform(Matrix.Translation((0, -co[:, 1].max(), 0)))     # задняя сторона — к стене (y = 0)
    obj.data.update()
    name = out or joint
    mb, _ = T.export(obj, os.path.join(EXPORT, name + "_idle.glb"))
    lo, hi = T.bbox(obj)
    print(f"[{name}] прямой: пучок {th_h * 100:.1f} см, глубина {dp_h * 100:.1f}"
          + (f"; верт. ширина {tw_v * 100:.1f}, глубина {dp_v * 100:.1f}" if v_name else "")
          + f" | уголок до: гориз. {t_h * 100:.1f}, верт. {(t_v or 0) * 100:.1f}, глубина {d_h * 100:.1f}"
          + f" | масштаб X {sx:.3f} Y {sy:.3f} Z {sz:.3f} | итог {(hi - lo)[0] * 100:.0f}×{(hi - lo)[1] * 100:.0f}"
          f"×{(hi - lo)[2] * 100:.0f} см, {mb:.2f} МБ", flush=True)
    return obj


def main(argv):
    flags = {a for a in argv if a.startswith("--")}
    out = argv[argv.index("--out") + 1] if "--out" in argv else None
    src = argv[argv.index("--src") + 1] if "--src" in argv else EXPORT
    pos = [a for a in argv if not a.startswith("--") and a not in (out, src)]
    fit(pos[0], pos[1], pos[2] if len(pos) > 2 else None, stand="--stand" in flags, caps="--caps" in flags, out=out,
        src=src)


if __name__ == "__main__":
    main(sys.argv[1:])
