"""Поиск колёс у транспорта (для tools/open_parts.py): центр, радиус, ширина — по сетке модели.

Колёса — то, что касается земли. Точки касания группируются по X (ось) и по борту (знак Y; у мотоцикла и
велосипеда колесо одно посередине). Радиус и центр — по нижней дуге профиля (самая низкая точка сетки вдоль X):
у круга она поднимается как r − √(r² − (x − cx)²). Ширина — по точкам ниже ступицы.
"""
import numpy as np


def _groups(v, gap):
    order = np.argsort(v)
    out, cur = [], [order[0]]
    for a, b in zip(order[:-1], order[1:]):
        if v[b] - v[a] > gap:
            out.append(cur)
            cur = []
        cur.append(b)
    out.append(cur)
    return out


def _fit(xs, zs, z0, cx0, rmax):
    best = (1e9, cx0, 0.3)
    for r in np.arange(0.06, rmax, 0.01):
        for cx in np.arange(cx0 - 0.12, cx0 + 0.121, 0.01):
            dx = xs - cx
            m = np.abs(dx) < r * 0.95
            if m.sum() < 3:
                continue
            pred = z0 + r - np.sqrt(r * r - dx[m] ** 2)
            err = np.mean((pred - zs[m]) ** 2) - 0.00002 * m.sum()
            if err < best[0]:
                best = (err, cx, r)
    return best[1], best[2]


def _ring(co, ym, cx0, z0, rmax):
    """Протектор — вершины на расстоянии r от оси: ищем r (и cx), где их больше всего (нижние 3/4 круга —
    сверху мешает крыло)."""
    side = co[np.abs(co[:, 1] - ym) < 0.14]
    side = side[np.abs(side[:, 0] - cx0) < rmax + 0.1]
    best = (-1, cx0, 0.3)
    for r in np.arange(0.12, rmax, 0.01):
        for cx in np.arange(cx0 - 0.08, cx0 + 0.081, 0.02):
            cz = z0 + r
            d = np.hypot(side[:, 0] - cx, side[:, 2] - cz)
            low = side[:, 2] < cz + 0.5 * r
            on = (np.abs(d - r) < 0.015 + 0.02 * r) & low
            inside = (d < r * 0.97) & low
            # круг: много точек на ободе, а снаружи (кольцо чуть больше) — заметно меньше
            ring_out = (np.abs(d - r * 1.12) < 0.015 + 0.02 * r) & low
            score = (on.sum() - 0.7 * ring_out.sum()) / r
            if score > best[0]:
                best = (score, cx, r)
    return best[1], best[2]


def detect(co, center_band=0.12, rmax=0.75, contact=0.03, low=0.12):
    """co — вершины (N×3, Blender, Z вверх, низ на Z≈0). → [{"c": [x, y, z], "r": r, "y": [y0, y1]}]."""
    z0 = co[:, 2].min()
    cont = co[co[:, 2] < z0 + contact]
    wheels = []
    for g in _groups(cont[:, 0], 0.2):
        pts = cont[g]
        cx0 = float(np.median(pts[:, 0]))
        sides = [pts[pts[:, 1] < -center_band], pts[pts[:, 1] > center_band], pts[np.abs(pts[:, 1]) <= center_band]]
        for sp in sides:
            if len(sp) < 2:
                continue
            ym = float(np.median(sp[:, 1]))
            # профиль низа вдоль X в полосе этого борта
            band = co[(np.abs(co[:, 1] - ym) < 0.12) & (np.abs(co[:, 0] - cx0) < rmax + 0.15)]
            bins = np.round(band[:, 0] / 0.015).astype(int)
            xs, zs = [], []
            for k in np.unique(bins):
                xs.append(k * 0.015)
                zs.append(band[bins == k, 2].min())
            xs, zs = np.array(xs), np.array(zs)
            keep = zs < z0 + low
            cx, r = _fit(xs[keep], zs[keep], z0, cx0, rmax)
            cx, r = _ring(co, ym, cx0, z0, rmax)
            sel = co[(np.abs(co[:, 0] - cx) < r * 0.8) & (co[:, 2] < z0 + r * 0.45)]
            if abs(ym) > center_band:
                sel = sel[np.sign(sel[:, 1]) == np.sign(ym)]
            else:
                sel = sel[np.abs(sel[:, 1]) < 0.3]
            ys = sel[:, 1]
            y0, y1 = float(np.percentile(ys, 2)), float(np.percentile(ys, 98))
            wheels.append({"c": [round(float(cx), 3), round((y0 + y1) / 2, 3), round(float(z0 + r), 3)],
                           "r": round(float(r), 3), "y": [round(y0, 3), round(y1, 3)]})
    # одинаковые колёса одной оси — один радиус (берём больший)
    return wheels
