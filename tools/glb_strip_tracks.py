"""Оставить в анимациях только повороты костей (+ положение таза Hips) и ужать файл.

  python3 tools/glb_strip_tracks.py export/anim/anims_mixamo.glb [ещё.glb …]

Зачем: анимации сняты с голого тела body_m_rig, и в них у каждой кости записано ещё и её МЕСТО (длины костей голого тела).
Godot ставит кости ровно как в анимации — у одетого / крупного персонажа плечи, руки и ноги съезжали на места голого
тела (руки уходили в грудь и живот). Повороты подходят всем; место кости у каждого персонажа должно оставаться своё.
Положение Hips остаётся (подъём/приседание/покачивание); разница роста — Skeleton3D.motion_scale в игре.
Файл перезаписывается; неиспользуемые данные выкидываются.
"""
import json
import struct
import sys


def pad4(b, fill=b"\0"):
    return b + fill * ((4 - len(b) % 4) % 4)


def strip(path):
    raw = open(path, "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]
    j = json.loads(raw[20:20 + jl])
    binc = raw[20 + jl + 8:]
    removed = 0
    for an in j.get("animations", []):
        keep = []
        for ch in an["channels"]:
            node = j["nodes"][ch["target"]["node"]].get("name", "")
            p = ch["target"]["path"]
            if p == "scale" or (p == "translation" and not node.endswith("Hips")):
                removed += 1
                continue
            keep.append(ch)
        used = sorted({ch["sampler"] for ch in keep})
        remap = {o: n for n, o in enumerate(used)}
        an["samplers"] = [an["samplers"][o] for o in used]
        for ch in keep:
            ch["sampler"] = remap[ch["sampler"]]
        an["channels"] = keep
    # какие accessors нужны
    need = set()
    for an in j.get("animations", []):
        for s in an["samplers"]:
            need |= {s["input"], s["output"]}
    for m in j.get("meshes", []):
        for pr in m["primitives"]:
            need |= set(pr["attributes"].values())
            if "indices" in pr:
                need.add(pr["indices"])
            for t in pr.get("targets", []):
                need |= set(t.values())
    for s in j.get("skins", []):
        if "inverseBindMatrices" in s:
            need.add(s["inverseBindMatrices"])
    need_bv = {j["accessors"][a]["bufferView"] for a in need if "bufferView" in j["accessors"][a]}
    for im in j.get("images", []):
        if "bufferView" in im:
            need_bv.add(im["bufferView"])
    # пересобрать буфер: только нужные bufferViews (одинаковые куски — один раз)
    acc_map = {o: n for n, o in enumerate(sorted(need))}
    bv_map, out, seen = {}, bytearray(), {}
    for o in sorted(need_bv):
        bv = j["bufferViews"][o]
        data = binc[bv.get("byteOffset", 0): bv.get("byteOffset", 0) + bv["byteLength"]]
        key = (data, bv.get("byteStride"), bv.get("target"))
        if key in seen:
            bv_map[o] = seen[key]
            continue
        while len(out) % 4:
            out.append(0)
        nbv = {k: v for k, v in bv.items() if k not in ("byteOffset", "buffer")}
        nbv["buffer"] = 0
        nbv["byteOffset"] = len(out)
        out += data
        bv_map[o] = seen[key] = len(seen)
        j.setdefault("_new_bv", []).append(nbv)
    j["bufferViews"] = j.pop("_new_bv")
    accs = []
    for o in sorted(need):
        a = dict(j["accessors"][o])
        if "bufferView" in a:
            a["bufferView"] = bv_map[a["bufferView"]]
        accs.append(a)
    j["accessors"] = accs
    for an in j.get("animations", []):
        for s in an["samplers"]:
            s["input"], s["output"] = acc_map[s["input"]], acc_map[s["output"]]
    for m in j.get("meshes", []):
        for pr in m["primitives"]:
            pr["attributes"] = {k: acc_map[v] for k, v in pr["attributes"].items()}
            if "indices" in pr:
                pr["indices"] = acc_map[pr["indices"]]
            if "targets" in pr:
                pr["targets"] = [{k: acc_map[v] for k, v in t.items()} for t in pr["targets"]]
    for s in j.get("skins", []):
        if "inverseBindMatrices" in s:
            s["inverseBindMatrices"] = acc_map[s["inverseBindMatrices"]]
    for im in j.get("images", []):
        if "bufferView" in im:
            im["bufferView"] = bv_map[im["bufferView"]]
    j["buffers"] = [{"byteLength": len(out)}]
    js = pad4(json.dumps(j, separators=(",", ":"), ensure_ascii=False).encode(), b" ")
    bb = pad4(bytes(out))
    total = 12 + 8 + len(js) + 8 + len(bb)
    with open(path, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, total))
        f.write(struct.pack("<II", len(js), 0x4E4F534A) + js)
        f.write(struct.pack("<II", len(bb), 0x004E4942) + bb)
    print(f"[{path}] убрано дорожек: {removed}, {len(raw) / 1e6:.2f} → {total / 1e6:.2f} МБ", flush=True)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        strip(p)
