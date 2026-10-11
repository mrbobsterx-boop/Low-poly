"""Чистка моделей от «ошмётков»: мелкие оторванные кусочки сетки ВНЕ основного тела (Tripo иногда оставляет их
под моделью — из-за них ванна «висит» в воздухе: игра считает низом модели самый нижний кусочек).

  python3 tools/glb_clean.py export/                 # проверить все, исправить, отчёт
  python3 tools/glb_clean.py export/x_idle.glb --dry # только показать

Кусок удаляется, если он маленький (меньше 1,5 % треугольников модели) И лежит снаружи коробки основного тела
(расширенной на 2 % размера). Мелкие детали НА модели (стикеры, кнопки) не трогаются.
"""
import json, struct, sys, os
import numpy as np

CT = {5126: np.float32, 5123: np.uint16, 5125: np.uint32, 5121: np.uint8, 5122: np.int16, 5120: np.int8}
NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}


def load(p):
    b = open(p, 'rb').read()
    n = struct.unpack('<I', b[12:16])[0]
    j = json.loads(b[20:20 + n])
    off = 20 + n
    bl = struct.unpack('<I', b[off:off + 4])[0]
    return j, bytearray(b[off + 8:off + 8 + bl])


def acc(j, binb, i):
    a = j['accessors'][i]
    bv = j['bufferViews'][a['bufferView']]
    ct = CT[a['componentType']]
    k = NC[a['type']]
    isz = np.dtype(ct).itemsize
    off = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
    st = bv.get('byteStride', 0)
    if st and st != k * isz:
        raw = np.frombuffer(bytes(binb), np.uint8, a['count'] * st, off).reshape(-1, st)[:, :k * isz]
        return raw.copy().view(ct).reshape(-1, k)
    return np.frombuffer(bytes(binb), ct, a['count'] * k, off).reshape(-1, k).copy()


def components(pos, tri):
    """Связные куски по треугольникам (вершины с одинаковой позицией — одна точка, швы UV не рвут кусок)."""
    q = np.round(pos / max(float(np.ptp(pos, axis=0).max()), 1e-6) * 1e5).astype(np.int64)
    _, weld = np.unique(q, axis=0, return_inverse=True)
    weld = weld.ravel()
    parent = np.arange(weld.max() + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    t = weld[tri]
    for a, b, c in t:
        ra, rb, rc = find(a), find(b), find(c)
        parent[rb] = ra
        parent[find(rc)] = ra
    roots = np.array([find(x) for x in t[:, 0]])
    return roots


def clean(path, dry=False):
    j, binb = load(path)
    changed = []
    all_pos = []
    prims = []
    for mi, m in enumerate(j.get('meshes', [])):
        for pi, p in enumerate(m['primitives']):
            if 'indices' not in p:
                continue
            pos = acc(j, binb, p['attributes']['POSITION']).astype(np.float64)
            tri = acc(j, binb, p['indices']).astype(np.int64).reshape(-1, 3)
            prims.append((p, pos, tri))
            all_pos.append(pos)
    if not prims:
        return []
    total = sum(len(t) for _, _, t in prims)
    newdata = {}
    for p, pos, tri in prims:
        roots = components(pos, tri)
        ids, counts = np.unique(roots, return_counts=True)
        main = ids[counts >= max(1, total * 0.015)]
        if len(main) == 0:
            main = ids[[counts.argmax()]]
        keep_mask = np.isin(roots, main)
        mv = pos[np.unique(tri[keep_mask])]
        lo, hi = mv.min(0), mv.max(0)
        pad = (hi - lo) * 0.02 + 1e-4
        drop = []
        for cid, cnt in zip(ids, counts):
            if cid in main:
                continue
            cv = pos[np.unique(tri[roots == cid])]
            inside = np.all(cv.min(0) >= lo - pad) and np.all(cv.max(0) <= hi + pad)
            if not inside:
                drop.append(cid)
        if not drop:
            continue
        keep = ~np.isin(roots, drop)
        changed.append((int((~keep).sum()), len(tri)))
        newdata[id(p)] = (p, tri[keep])
    if not changed or dry:
        return changed
    # пересобрать вершины выбранных примитивов (лишние вершины убрать — по ним считается коробка модели)
    rebuilt = {}
    for key, (p, tri) in newdata.items():
        used = np.unique(tri)
        remap = -np.ones(int(tri.max()) + 1 if len(tri) else 1, np.int64)
        remap[used] = np.arange(len(used))
        attrs = {}
        for name, ai in p['attributes'].items():
            a = acc(j, binb, ai)
            attrs[name] = (a[used], j['accessors'][ai])
        rebuilt[key] = (p, remap[tri].astype(np.uint32), attrs)
    # новый буфер: все старые bufferViews, кроме тех, что относятся только к заменяемым accessor-ам
    replaced = set()
    for key, (p, _, _) in rebuilt.items():
        replaced.add(p['indices'])
        replaced.update(p['attributes'].values())
    still_used = set()
    for i, a in enumerate(j['accessors']):
        if i not in replaced and 'bufferView' in a:
            still_used.add(a['bufferView'])
    for im in j.get('images', []):
        if 'bufferView' in im:
            still_used.add(im['bufferView'])
    out = bytearray()
    newbv = []
    bvmap = {}
    for i, bv in enumerate(j['bufferViews']):
        if i not in still_used:
            continue
        while len(out) % 4:
            out.append(0)
        o = bv.get('byteOffset', 0)
        data = binb[o:o + bv['byteLength']]
        nb = dict(bv)
        nb['byteOffset'] = len(out)
        out.extend(data)
        bvmap[i] = len(newbv)
        newbv.append(nb)
    for a in j['accessors']:
        if 'bufferView' in a and a['bufferView'] in bvmap:
            a['bufferView'] = bvmap[a['bufferView']]
    for im in j.get('images', []):
        if 'bufferView' in im:
            im['bufferView'] = bvmap[im['bufferView']]

    def add(arr, src_acc, target):
        nonlocal out
        arr = np.ascontiguousarray(arr)
        while len(out) % 4:
            out.append(0)
        off = len(out)
        out.extend(arr.tobytes())
        newbv.append({'buffer': 0, 'byteOffset': off, 'byteLength': arr.nbytes, 'target': target})
        a = {k: v for k, v in src_acc.items() if k not in ('bufferView', 'byteOffset', 'count', 'min', 'max', 'sparse')}
        a['bufferView'] = len(newbv) - 1
        a['count'] = len(arr)
        if src_acc.get('min') is not None:
            a['min'] = arr.min(0).tolist()
            a['max'] = arr.max(0).tolist()
        j['accessors'].append(a)
        return len(j['accessors']) - 1

    for key, (p, idx, attrs) in rebuilt.items():
        for name, (arr, src) in attrs.items():
            arr = arr.astype(CT[src['componentType']])
            p['attributes'][name] = add(arr, src, 34962)
        p['indices'] = add(idx.ravel(), {'componentType': 5125, 'type': 'SCALAR'}, 34963)
    j['bufferViews'] = newbv
    while len(out) % 4:
        out.append(0)
    j['buffers'] = [{'byteLength': len(out)}]
    js = json.dumps(j, separators=(',', ':')).encode()
    while len(js) % 4:
        js += b' '
    data = b'glTF' + struct.pack('<II', 2, 12 + 8 + len(js) + 8 + len(out)) + struct.pack('<I', len(js)) + b'JSON' + js \
        + struct.pack('<I', len(out)) + b'BIN\x00' + bytes(out)
    open(path, 'wb').write(data)
    return changed


def main(argv):
    dry = '--dry' in argv
    paths = [a for a in argv if not a.startswith('--')]
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += sorted(os.path.join(p, f) for f in os.listdir(p) if f.endswith('.glb'))
        else:
            files.append(p)
    n = 0
    for f in files:
        ch = clean(f, dry)
        if ch:
            n += 1
            print(os.path.basename(f), ', '.join(f'убрано {a} из {b} треуг.' for a, b in ch))
    print(f'моделей с ошмётками: {n} из {len(files)}' + (' (только проверка)' if dry else ''))


if __name__ == '__main__':
    main(sys.argv[1:])
