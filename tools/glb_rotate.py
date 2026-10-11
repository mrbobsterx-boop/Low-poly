"""Повернуть готовую модель вокруг вертикали (Y) — если перед смотрит вбок (у Tripo бывает по оси X).

  python3 tools/glb_rotate.py export/x_idle.glb -90   # градусы: −90 — перед с +X на +Z (к камере), 90 — с −X, 180 — задом

Поворачивает вершины и нормали прямо в файле (узлы и текстуры не трогает), пересчитывает min/max.
"""
import sys, json, struct, math
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from glb_clean import load, acc, CT, NC


def rotate(path, deg):
    j, binb = load(path)
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    # поворот вокруг Y на deg: x' = x·cos + z·sin, z' = −x·sin + z·cos
    R = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    done = set()
    for m in j.get('meshes', []):
        for p in m['primitives']:
            for name in ('POSITION', 'NORMAL', 'TANGENT'):
                ai = p['attributes'].get(name)
                if ai is None or ai in done:
                    continue
                done.add(ai)
                ac = j['accessors'][ai]
                bv = j['bufferViews'][ac['bufferView']]
                if ac['componentType'] != 5126 or bv.get('byteStride', 0) not in (0, NC[ac['type']] * 4):
                    raise SystemExit('не поддерживается: %s у %s' % (name, path))
                arr = acc(j, binb, ai).astype(np.float64)
                arr[:, :3] = arr[:, :3] @ R.T
                arr = arr.astype(np.float32)
                off = bv.get('byteOffset', 0) + ac.get('byteOffset', 0)
                binb[off:off + arr.nbytes] = arr.tobytes()
                if 'min' in ac:
                    ac['min'] = arr.min(0).tolist()
                    ac['max'] = arr.max(0).tolist()
    js = json.dumps(j, separators=(',', ':')).encode()
    while len(js) % 4:
        js += b' '
    out = bytes(binb)
    data = b'glTF' + struct.pack('<II', 2, 12 + 8 + len(js) + 8 + len(out)) + struct.pack('<I', len(js)) + b'JSON' + js \
        + struct.pack('<I', len(out)) + b'BIN\x00' + out
    open(path, 'wb').write(data)


if __name__ == '__main__':
    rotate(sys.argv[1], float(sys.argv[2]))
    print('повёрнуто:', sys.argv[1], sys.argv[2], '°')
