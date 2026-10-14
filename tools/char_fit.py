"""Подгонка общих анимаций под фигуру персонажа → export/anim/char_fit.json (для игры).

  python3 tools/char_fit.py

Анимации Mixamo сняты с худого голого тела. У одетого / полного персонажа те же движения ведут руки сквозь куртку
и живот. Поэтому для каждого персонажа считается:
- arm_spread_deg — на сколько градусов отвести плечо (кость LeftArm / RightArm) в сторону поверх анимации,
  чтобы рука проходила мимо туловища так же, как у голого тела (0 — не нужно);
- motion_scale — Skeleton3D.motion_scale: высота таза персонажа / высота таза в наборе анимаций
  (иначе таз ставится на высоту голого тела: ноги в полу или в воздухе).
Расчёт по позе покоя: ширина туловища на уровне от груди до бёдер против линии висящей руки (с её толщиной).
"""
import glob
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from anim_check import GLB, hips_y, posed, sample  # noqa: E402

TORSO = ("Hips", "Spine", "Spine1", "Spine2")
SOURCES = {"mixamo": "anims_mixamo.glb", "tripo_m": "body_m_rig_anims.glb", "tripo_m_b": "body_m_rig_b_anims.glb",
           "tripo_f": "body_f_rig_anims.glb"}


ARM = ("LeftArm", "LeftForeArm", "LeftHand", "RightArm", "RightForeArm", "RightHand")
POSES = [("idle", 0.0), ("idle", 0.5), ("walk", 0.0), ("walk", 0.25), ("walk", 0.5), ("walk", 0.75),
         ("aa_run", 0.0), ("aa_run", 0.5), ("talk", 0.25), ("talk", 0.75)]


def inside(g, poses, ms, spread):
    """Доля вершин рук (дальше плеча), которые в этих позах оказались внутри туловища."""
    tot, n_in = 0, 0
    for pose in poses:
        parts = posed(g, pose, "rot", ms, spread, parts=True)
        P = np.vstack([q for q, _ in parts])
        B = np.concatenate([b for _, b in parts])
        is_arm = np.array([b.startswith(ARM) for b in B.astype(str)])     # вся рука: плечо, предплечье, кисть
        # туловище — всё, кроме рук и головы (у Tripo живот и полы одежды часто на костях бёдер)
        torso = P[~is_arm & ~np.isin(B, ("Neck", "Head", "HeadTop_End"))]
        arm = P[is_arm]
        lo, hi = torso[:, 1].min(), torso[:, 1].max()
        step = (hi - lo) / 20
        for k in range(20):
            y0 = lo + k * step
            t = torso[(torso[:, 1] >= y0) & (torso[:, 1] < y0 + step)]
            a = arm[(arm[:, 1] >= y0) & (arm[:, 1] < y0 + step)]
            if len(t) < 8 or not len(a):
                continue
            # срез туловища — «звезда»: от центра по 24 направлениям, радиус = край туловища в этом направлении
            #   (рюкзак или щит на спине раздувает только задние направления)
            c = np.median(t[:, [0, 2]], 0)
            dt, da = t[:, [0, 2]] - c, a[:, [0, 2]] - c
            bt = ((np.arctan2(dt[:, 1], dt[:, 0]) + np.pi) / (2 * np.pi) * 24).astype(int) % 24
            ba = ((np.arctan2(da[:, 1], da[:, 0]) + np.pi) / (2 * np.pi) * 24).astype(int) % 24
            rt = np.linalg.norm(dt, axis=1)
            rad = np.array([np.percentile(rt[bt == k], 90) if (bt == k).sum() > 1 else 0.0 for k in range(24)])
            n_in += int((np.linalg.norm(da, axis=1) < 0.85 * rad[ba]).sum())
        tot += len(arm)
    return n_in / max(tot, 1)


def fit_spread(g, anims, ms, target):
    """Наименьший угол, после которого отводить руки дальше почти бесполезно: остаётся четверть от того, что
    вообще можно убрать (часть «сквозь тело» — у подмышек и ремней — не уходит ни при каком угле)."""
    poses = [sample(anims, anims.by[a], t) for a, t in POSES]
    f = {sp: inside(g, poses, ms, float(sp)) for sp in range(0, 25, 2)}
    if f[0] <= target:
        return 0.0, f[0]
    thr = max(target, f[24] + 0.25 * (f[0] - f[24]))
    sp = next(k for k in sorted(f) if f[k] <= thr)
    return float(sp), f[sp]


def main():
    src = {k: hips_y(GLB(os.path.join(ROOT, "export", "anim", v))) for k, v in SOURCES.items()}
    anims = GLB(os.path.join(ROOT, "export", "anim", "anims_mixamo.glb"))
    anims.by = {a["name"]: a for a in anims.j["animations"]}
    body = GLB(os.path.join(ROOT, "export", "body_m_rig_idle.glb"))
    ref = inside(body, [sample(anims, anims.by[a], t) for a, t in POSES], 1.0, 0.0)
    target = max(ref, 0.01) * 1.5                          # сквозь туловище — не больше, чем у голого тела
    print(f"голое тело: внутри туловища {ref:.1%} вершин рук; цель ≤ {target:.1%}", flush=True)
    only = sys.argv[1:]
    animals = set(json.load(open(os.path.join(ROOT, "export", "anim", "animals_info.json"))))
    chars = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "export", "*_idle.glb"))):
        n = os.path.basename(f)[:-9]
        if n in animals or (only and n not in only):
            continue
        g = GLB(f)
        if "skins" not in g.j or not any(x.get("name", "").endswith("Hips") for x in g.j["nodes"]):
            continue
        h = hips_y(g)
        spread, f = fit_spread(g, anims, h / src["mixamo"], target)
        chars[n] = {"arm_spread_deg": spread, "hips_height": round(h, 4),
                    "motion_scale": {k: round(h / v, 4) for k, v in src.items()}}
        print(f"{n:28s} руки +{chars[n]['arm_spread_deg']:4.1f}°  таз ×{chars[n]['motion_scale']['mixamo']:.3f}  (сквозь тело {f:.1%})",
              flush=True)
    out = {"_comment": ("Подгонка общих анимаций под фигуру. arm_spread_deg — после анимации повернуть кости "
                        "mixamorig:LeftArm и mixamorig:RightArm наружу (вокруг оси «вперёд» скелета: Left — "
                        "+угол, Right — −угол), чтобы руки не проходили сквозь одежду и живот. motion_scale — "
                        "Skeleton3D.motion_scale по набору анимаций (таз на своей высоте)."),
           "ref_body": "body_m_rig", "sources_hips_height": {k: round(v, 4) for k, v in src.items()},
           "characters": chars}
    json.dump(out, open(os.path.join(ROOT, "export", "anim", "char_fit.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
