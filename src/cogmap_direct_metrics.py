# -*- coding: utf-8 -*-
"""Direct map-construction metrics (discrete/topology/identity), aligned to GT.

Metrics:
1. relative order accuracy (x/y)
2. 8-direction classification accuracy
3. kNN adjacency edge match (k=1,3)
4. instance mismatch rate
5. mirror evidence score
6. z absolute bias
7. internal artifacts (stacking / grid preference / entropy)
"""
import io
import json
import math
import os
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, r"C:\Users\贝贝\Documents\Three-view Cognitive Map\src")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import numpy as np

SRC = r"C:\Users\贝贝\Documents\Three-view Cognitive Map\src"
OUT = r"C:\Users\贝贝\Documents\Three-view Cognitive Map\docs\cogmap-direct-metrics.md"


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [r for r in data if "__summary__" not in r]


def centroids(view):
    out = {}
    for cat, items in view.items():
        if items:
            out[cat] = np.array([sum(p[0] for p in items) / len(items),
                                 sum(p[1] for p in items) / len(items)])
    return out


def _match_instance_pairs(pred_top, gt_top):
    """Match model instances to GT instances within each category (greedy NN)."""
    pairs = []
    for cat in sorted(set(pred_top) & set(gt_top)):
        mp = [list(p) for p in pred_top[cat]]
        gp = [list(p) for p in gt_top[cat]]
        while mp and gp:
            best = (1e9, None, None)
            for i, m in enumerate(mp):
                for j, g in enumerate(gp):
                    d = math.hypot(m[0] - g[0], m[1] - g[1])
                    if d < best[0]:
                        best = (d, i, j)
            if best[1] is None:
                break
            pairs.append((np.array(mp[best[1]]), np.array(gp[best[2]])))
            mp.pop(best[1])
            gp.pop(best[2])
    return pairs


def rigid_align(pred_top, gt_top, allow_mirror=True):
    """Instance-level rigid alignment: yaw + translation (+ optional mirror).

    Matches instances within each category by nearest distance, then solves
    Kabsch on the matched points. Works for >=2 matched pairs; scale and z are
    intentionally not fitted so they remain model errors."""
    pairs = _match_instance_pairs(pred_top, gt_top)
    if len(pairs) < 2:
        return None
    P = np.array([p for p, _ in pairs])
    G = np.array([g for _, g in pairs])

    def solve(use_mirror):
        pc, gc = P.mean(0), G.mean(0)
        X, Y = P - pc, G - gc
        H = X.T @ Y
        U, _, Vt = np.linalg.svd(H)
        R = Vt.T @ U.T
        mirror = False
        if not use_mirror and np.linalg.det(R) < 0:
            Vt[-1] *= -1
            R = Vt.T @ U.T
        else:
            mirror = bool(use_mirror and np.linalg.det(R) < 0)
        dx, dy = gc - pc @ R.T
        rmse = float(np.sqrt(np.mean(((X @ R.T) - Y) ** 2)))
        yaw = float(math.degrees(math.atan2(R[1, 0], R[0, 0])))
        return {"R": R, "dx": float(dx), "dy": float(dy), "mirror": mirror,
                "rmse": rmse, "yaw": yaw}

    T0 = solve(False)
    if not allow_mirror:
        T0.update({"mirror_confirmed": False, "low_confidence": False,
                   "mode": "full", "n_pairs": len(pairs)})
        return T0
    T1 = solve(True)

    def x_violations(T):
        R, dx, dy = T["R"], T["dx"], T["dy"]
        Q = P @ R.T + np.array([dx, dy])
        v = 0
        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                if abs(G[i][0] - G[j][0]) < 0.5:
                    continue
                if (G[i][0] - G[j][0]) * (Q[i][0] - Q[j][0]) < 0:
                    v += 1
        return v

    v0 = x_violations(T0)
    v1 = x_violations(T1)
    mirror_confirmed = bool(v0 > 0 and v1 < v0 * 0.5)
    use_mirror = bool(T1["mirror"] and (mirror_confirmed or T1["rmse"] < T0["rmse"] - 0.3))
    T = dict(T1) if use_mirror else dict(T0)
    T["mirror"] = bool(use_mirror and T1["mirror"])
    T["mirror_confirmed"] = bool(use_mirror and mirror_confirmed)
    T["low_confidence"] = False
    T["mode"] = "full"
    T["n_pairs"] = len(pairs)
    return T


def apply_rigid(view, T):
    out = {}
    R, dx, dy = T["R"], T["dx"], T["dy"]
    for cat, items in view.items():
        pts = []
        for p in items:
            v = np.array([p[0], p[1]]) @ R.T + np.array([dx, dy])
            pts.append([float(v[0]), float(v[1])])
        out[cat] = pts
    return out


def pairs_from(points):
    cats = sorted(points)
    out = []
    for i in range(len(cats)):
        for j in range(i + 1, len(cats)):
            out.append((cats[i], cats[j]))
    return out


def order_accuracy(g, p):
    """Pairwise x/y order accuracy between aligned maps (category centroids)."""
    common = sorted(set(g) & set(p))
    g = {c: g[c] for c in common}
    p = {c: p[c] for c in common}
    ok_x = ok_y = tot_x = tot_y = 0
    for a, b in pairs_from(g):
        gx = g[a][0] - g[b][0]
        px = p[a][0] - p[b][0]
        if abs(gx) >= 0.5:
            tot_x += 1
            ok_x += int((gx > 0) == (px > 0))
        gy = g[a][1] - g[b][1]
        py = p[a][1] - p[b][1]
        if abs(gy) >= 0.5:
            tot_y += 1
            ok_y += int((gy > 0) == (py > 0))
    return ok_x, tot_x, ok_y, tot_y


DIRS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def direction_bin(vec):
    ang = math.atan2(vec[1], vec[0])  # -pi..pi
    idx = int(round(math.degrees(ang) / 45.0)) % 8
    return idx


def direction_accuracy(g, p):
    common = sorted(set(g) & set(p))
    g = {c: g[c] for c in common}
    p = {c: p[c] for c in common}
    exact = tot = near = 0
    for a, b in pairs_from(g):
        gv = np.array([g[a][0] - g[b][0], g[a][1] - g[b][1]])
        pv = np.array([p[a][0] - p[b][0], p[a][1] - p[b][1]])
        if np.linalg.norm(gv) < 0.5:
            continue
        gb = direction_bin(gv)
        pb = direction_bin(pv)
        tot += 1
        exact += int(gb == pb)
        near += int(((gb - pb) % 8) <= 1 or ((pb - gb) % 8) <= 1)
    return exact, tot, near


def knn_edges(points, k):
    cats = sorted(points)
    P = np.array([points[c] for c in cats])
    n = len(P)
    edges = set()
    for i in range(n):
        d = np.sum((P - P[i]) ** 2, axis=1)
        order = np.argsort(d)
        for j in order[1:k + 1]:
            edges.add(tuple(sorted((cats[i], cats[j]))))
    return edges


def knn_match(g, p, k):
    common = sorted(set(g) & set(p))
    g = {c: g[c] for c in common}
    p = {c: p[c] for c in common}
    eg = knn_edges(g, k)
    ep = knn_edges(p, k)
    inter = len(eg & ep)
    union = len(eg | ep)
    return inter, union


def instance_mismatch(gt_cats, pred_cats):
    """Within-category nearest-neighbor identity mismatch (rank vs NN)."""
    mism = tot = 0
    for cat in set(gt_cats) & set(pred_cats):
        G = sorted(gt_cats[cat], key=lambda x: (x[0], x[1]))
        P = pred_cats[cat]
        if len(G) < 2 or len(P) != len(G):
            continue
        for gi, gpt in enumerate(G):
            nn = min(range(len(P)), key=lambda pi: math.hypot(P[pi][0] - gpt[0], P[pi][1] - gpt[1]))
            tot += 1
            if nn != gi:
                mism += 1
    return mism, tot


def z_bias(gt_views, pred_views):
    dz = []
    for view in ("front", "side"):
        gv, pv = gt_views.get(view, {}), pred_views.get(view, {})
        for cat in set(gv) & set(pv):
            for gp, mp in zip(sorted(gv[cat]), sorted(pv[cat])):
                dz.append(mp[1] - gp[1])
    return dz


def internal_artifacts(pred_top):
    # stacking: same-category instances closer than 0.5 grid
    stacked = pairs = 0
    for cat, items in pred_top.items():
        if len(items) < 2:
            continue
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                pairs += 1
                if math.hypot(items[i][0] - items[j][0], items[i][1] - items[j][1]) < 0.5:
                    stacked += 1
    # grid preference: fraction of coords near integers or at edges 0/9
    n = 0
    int_near = 0
    edge = 0
    for items in pred_top.values():
        for p in items:
            for v in p:
                n += 1
                if abs(v - round(v)) < 0.2:
                    int_near += 1
                if v <= 0.2 or v >= 8.8:
                    edge += 1
    return stacked, pairs, int_near, edge, n


def main():
    recs = load(os.path.join(SRC, "results_tis_compare.json"))
    recs += load(os.path.join(SRC, "results_tis_threeview_3pass.json"))
    by_q = defaultdict(dict)
    for r in recs:
        if not r.get("error"):
            by_q[(r["dataset"], r["scene"], r["question"])][r["arm"]] = r

    agg = defaultdict(lambda: {
        "ox": [], "oy": [], "de": [], "dn": [], "k1": [], "k3": [],
        "im": [], "mirror_ev": [], "z": [], "stack": [], "grid": [], "edge": [],
        "two_pt": [],
    })
    for (ds, scene, q), arms in by_q.items():
        ref = next(iter(arms.values()))
        gt = ref.get("gt_map") or {}
        gt_top = gt.get("top", {})
        for arm in ("baseline", "threeview", "threeview_3pass"):
            r = arms.get(arm)
            if not r:
                continue
            pred = r.get("pred_map") or {}
            pred_top = pred.get("top", {})
            T = rigid_align(pred_top, gt_top)
            if not T:
                continue
            agg[arm]["two_pt"].append(int(T.get("n_pairs", 0) == 2))
            aligned = apply_rigid(pred_top, T)
            g = centroids(gt_top)
            p = centroids(aligned)
            okx, tx, oky, ty = order_accuracy(g, p)
            agg[arm]["ox"].append(okx / tx if tx else None)
            agg[arm]["oy"].append(oky / ty if ty else None)
            de, dt, dn = direction_accuracy(g, p)
            agg[arm]["de"].append(de / dt if dt else None)
            agg[arm]["dn"].append(dn / dt if dt else None)
            i1, u1 = knn_match(g, p, 1)
            i3, u3 = knn_match(g, p, 3)
            agg[arm]["k1"].append(i1 / u1 if u1 else None)
            agg[arm]["k3"].append(i3 / u3 if u3 else None)
            mi, mt = instance_mismatch(gt_top, aligned)
            agg[arm]["im"].append(mi / mt if mt else None)
            agg[arm]["mirror_ev"].append(int(T.get("mirror_confirmed", False)))
            if arm != "baseline":
                dz = z_bias(gt, pred)
                agg[arm]["z"].extend(dz)
            st, sp, ni, edge_n, n = internal_artifacts(pred_top)
            agg[arm]["stack"].append(st / sp if sp else None)
            agg[arm]["grid"].append(ni / n if n else None)
            agg[arm]["edge"].append(edge_n / n if n else None)

    lines = []
    lines.append("# cogmap 直指建图指标（离散/拓扑/身份，50 样本）")
    lines.append("")
    lines.append("> 2026-08-07 · 连续残差已弃用；以下指标对齐后计算但均为离散/顺序/身份/自洽类。")
    lines.append("")

    def med(v):
        vals = [x for x in v if x is not None]
        return statistics.median(vals) if vals else float("nan")

    arms = ("baseline", "threeview", "threeview_3pass")
    lines.append("| 指标 | baseline | threeview | 3-pass |")
    lines.append("|---|---|---|---|")
    rows = [
        ("相对顺序准确率 x", "ox"),
        ("相对顺序准确率 y", "oy"),
        ("方向分类准确率（精确）", "de"),
        ("方向分类准确率（±1）", "dn"),
        ("kNN(k=1) 边匹配", "k1"),
        ("kNN(k=3) 边匹配", "k3"),
        ("实例错位率", "im"),
        ("镜像证据题数", "mirror_ev"),
        ("2点对齐题数", "two_pt"),
        ("实例堆叠率", "stack"),
        ("网格整数偏好", "grid"),
        ("边缘偏好(0/9)", "edge"),
    ]
    for label, key in rows:
        cells = []
        for arm in arms:
            v = agg[arm][key]
            if key == "mirror_ev":
                cells.append(str(sum(v)))
            elif key == "two_pt":
                cells.append(str(sum(v)))
            elif key in ("stack", "grid", "edge"):
                cells.append("%.1f%%" % (100 * med(v)))
            else:
                cells.append("%.1f%%" % (100 * med(v)))
        lines.append("| %s | %s | %s | %s |" % (label, cells[0], cells[1], cells[2]))
    lines.append("")
    for arm in ("threeview", "threeview_3pass"):
        dz = agg[arm]["z"]
        if dz:
            lines.append("- %s：z 平均误差 %+.2f 格，偏高 %.0f%%" % (
                arm, statistics.mean(dz), 100 * sum(1 for v in dz if v > 0.5) / len(dz)))
    lines.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote", OUT)
    print("\n".join(lines[:30]))


if __name__ == "__main__":
    main()
