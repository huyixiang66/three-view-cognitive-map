# -*- coding: utf-8 -*-
"""Emit human-readable, case-level map-construction issues from aligned cogmaps."""
import io
import json
import math
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, r"C:\Users\贝贝\Documents\Three-view Cognitive Map\src")

import numpy as np

from cogmap_direct_metrics import (  # noqa: E402
    apply_rigid,
    centroids,
    direction_bin,
    pairs_from,
    rigid_align,
)

SRC = r"C:\Users\贝贝\Documents\Three-view Cognitive Map\src"
OUT = r"C:\Users\贝贝\Documents\Three-view Cognitive Map\docs\cogmap-issues.md"


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [r for r in data if "__summary__" not in r]


def min_pair(la, lb):
    best = float("inf")
    for a in la:
        for b in lb:
            best = min(best, math.hypot(a[0] - b[0], a[1] - b[1]))
    return best


def sample_issues(r, arm):
    gt = r.get("gt_map") or {}
    pred = r.get("pred_map") or {}
    gt_top, pred_top = gt.get("top", {}), pred.get("top", {})
    issues = []

    # counts
    for cat in set(gt_top) | set(pred_top):
        gn = len(gt_top.get(cat, []))
        pn = len(pred_top.get(cat, []))
        if pn < gn:
            issues.append("漏画 %s ×%d（GT %d，模型 %d）" % (cat, gn - pn, gn, pn))
        elif pn > gn:
            issues.append("多画 %s ×%d（GT %d，模型 %d）" % (cat, pn - gn, gn, pn))

    T = rigid_align(pred_top, gt_top)
    if not T:
        return issues
    aligned = apply_rigid(pred_top, T)
    g = centroids(gt_top)
    p = centroids(aligned)
    common = sorted(set(g) & set(p))

    # pair distance errors and direction classification
    for i in range(len(common)):
        for j in range(i + 1, len(common)):
            a, b = common[i], common[j]
            gd = min_pair(gt_top[a], gt_top[b])
            pd = min_pair(aligned[a], aligned[b])
            if abs(pd - gd) > 1.0:
                issues.append("%s-%s 距离画错（GT %.1f，模型 %.1f）" % (a, b, gd, pd))
            gv = np.array([g[a][0] - g[b][0], g[a][1] - g[b][1]])
            pv = np.array([p[a][0] - p[b][0], p[a][1] - p[b][1]])
            if np.linalg.norm(gv) >= 0.5:
                gb, pb = direction_bin(gv), direction_bin(pv)
                if gb != pb:
                    names = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
                    issues.append("%s→%s 方向错（GT %s，模型 %s）" % (a, b, names[gb], names[pb]))

    # z bias
    if arm != "baseline":
        dz = []
        for view in ("front", "side"):
            gv, pv = gt.get(view, {}), pred.get(view, {})
            for cat in set(gv) & set(pv):
                for gp, mp in zip(sorted(gv[cat]), sorted(pv[cat])):
                    dz.append(mp[1] - gp[1])
        if dz and abs(sum(dz) / len(dz)) >= 0.5:
            m = sum(dz) / len(dz)
            issues.append("z 整体%s（平均 %+.1f 格）" % ("偏高" if m > 0 else "偏低", m))

    # stacking
    stacked = []
    for cat, items in aligned.items():
        if len(items) < 2:
            continue
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if math.hypot(items[i][0] - items[j][0], items[i][1] - items[j][1]) < 0.5:
                    stacked.append(cat)
    if stacked:
        issues.append("实例堆叠：%s" % "/".join(sorted(set(stacked))))

    return issues


def main():
    recs = load(os.path.join(SRC, "results_tis_compare.json"))
    recs += load(os.path.join(SRC, "results_tis_threeview_3pass.json"))

    by_q = defaultdict(dict)
    for r in recs:
        if not r.get("error"):
            by_q[(r["dataset"], r["scene"], r["question"])][r["arm"]] = r

    lines = []
    lines.append("# cogmap 建图问题清单（case-level，50 样本）")
    lines.append("")
    lines.append("> 对齐后离散诊断转成的可检查问题；连续残差不出现。")
    lines.append("")

    arms = ("baseline", "threeview", "threeview_3pass")
    all_issues = defaultdict(list)
    for (ds, scene, q), arm_recs in by_q.items():
        for arm in arms:
            r = arm_recs.get(arm)
            if not r:
                continue
            iss = sample_issues(r, arm)
            all_issues[arm].append((scene, r["question_type"], iss))

    # aggregate
    lines.append("## 1. 各类问题出现样本数（top10 / arm）")
    lines.append("")
    for arm in arms:
        c = Counter()
        for _, _, iss in all_issues[arm]:
            for it in iss:
                key = it.split("（")[0].split("(")[0].strip()
                c[key] += 1
        lines.append("### %s" % arm)
        lines.append("")
        lines.append("| 问题类型 | 样本数 |")
        lines.append("|---|---|")
        for k, v in c.most_common(10):
            lines.append("| %s | %d |" % (k, v))
        lines.append("")

    lines.append("## 2. 逐样本问题清单")
    lines.append("")
    for arm in arms:
        lines.append("### %s" % arm)
        lines.append("")
        for scene, qt, iss in all_issues[arm]:
            if iss:
                lines.append("- `%s`（%s）：%s" % (scene, qt, "；".join(iss[:6])))
        lines.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote", OUT, "lines", len(lines))
    print("\n".join(lines[:26]))


if __name__ == "__main__":
    main()
