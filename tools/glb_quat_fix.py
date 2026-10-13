"""Выровнять знак кватернионов в анимациях готового .glb (на месте): q и −q — один и тот же поворот, но если знак
меняется между соседними кадрами, игра между кадрами крутит кость «длинным путём» — анимация дёргается.

  python3 tools/glb_quat_fix.py export/anim/anims_mixamo.glb [ещё.glb …]
"""
import json
import struct
import sys

import numpy as np


def fix(path):
    b = bytearray(open(path, "rb").read())
    jlen = struct.unpack("<I", b[12:16])[0]
    j = json.loads(b[20:20 + jlen])
    bin0 = 20 + jlen + 8
    n = 0
    seen = set()
    for an in j.get("animations", []):
        for ch in an["channels"]:
            if ch["target"]["path"] != "rotation":
                continue
            ai = an["samplers"][ch["sampler"]]["output"]
            if ai in seen:
                continue
            seen.add(ai)
            a = j["accessors"][ai]
            bv = j["bufferViews"][a["bufferView"]]
            if a["componentType"] != 5126 or bv.get("byteStride", 16) != 16:
                continue
            off = bin0 + bv.get("byteOffset", 0) + a.get("byteOffset", 0)
            q = np.frombuffer(bytes(b[off:off + a["count"] * 16]), np.float32).reshape(-1, 4).copy()
            for i in range(1, len(q)):
                if float(np.dot(q[i], q[i - 1])) < 0:
                    q[i] = -q[i]
                    n += 1
            b[off:off + a["count"] * 16] = q.astype(np.float32).tobytes()
    open(path, "wb").write(bytes(b))
    print(f"[{path}] исправлено кадров со сменой знака: {n}", flush=True)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        fix(p)
