# -*- coding: utf-8 -*-
"""Scene reconstruction accuracy metric.

For each model arm, after instance-level alignment to GT, compute per-object
Euclidean position error in each view (TOP: x,y / FRONT: x,z / SIDE: y,z),
average per sample, and compare failure vs correct samples.

Usage:
  python src/scene_reconstruction_metrics.py
"""
import importlib.util
import json
import math
import os
import statistics
import sys
from collections import defaultdict
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

spec = importlib.util.spec_from_file_location(
    'gcb', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'gen_casebycase_sidebyside.py'))
gcb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gcb)

from tis_compare import mra  # noqa: E402

SRC = os.path.dirname(os.path.abspath(__file__))
ARMS = ('baseline', 'threeview', 'threeview_3pass')


def correct(r):
    qt = r['question_type']
    ans = r.get('extracted_answer')
    gt = r['ground_truth']
    if ans is None:
        return False
    if qt in ('object_abs_distance', 'object_size_estimation', 'room_size_estimation'):
        return mra(ans, gt) > 0
    if qt == 'object_counting':
        try:
            return abs(float(ans) - float(gt)) < 1e-6
        except (TypeError, ValueError):
            return False
    return str(ans).strip().upper() == str(gt).strip().upper()


def greedy_dists(gt_pts, model_pts):
    gp = [list(p) for p in gt_pts]
    mp = [list(p) for p in model_pts]
    dists = []
    while gp and mp:
        best = min(((math.hypot(g[0] - m[0], g[1] - m[1]), i, j)
                    for i, g in enumerate(gp) for j, m in enumerate(mp)), key=lambda x: x[0])
        _, i, j = best
        dists.append(best[0])
        gp.pop(i)
        mp.pop(j)
    return dists


def sample_errors(r):
    gt_map = r.get('gt_map') or {}
    pred = r.get('pred_map') or {}
    pred_top = pred.get('top', {})
    gt_top = gt_map.get('top', {})
    T = gcb.rigid_align(pred_top, gt_top)
    pairs = gcb._match_instance_pairs(pred_top, gt_top)
    if not T:
        if len(pairs) < 1:
            return None
        P = np.array([p for p, _ in pairs])
        G = np.array([g for _, g in pairs])
        dx, dy = G.mean(0) - P.mean(0)
        T = {'R': np.eye(2), 'dx': float(dx), 'dy': float(dy)}
    top_v, f_v, s_v, _, _ = gcb.build_views(pred, T['R'], T['dx'], T['dy'], 1.0)
    out = {}
    for view, mvl in (('top', top_v), ('front', f_v), ('side', s_v)):
        gv = gt_map.get(view, {})
        dists = []
        for cat in set(gv) & set(mvl):
            dists.extend(greedy_dists(gv.get(cat, []), mvl.get(cat, [])))
        out[view] = (statistics.mean(dists) if dists else None, len(dists))
    return out


def main():
    recs = [r for r in json.load(open(os.path.join(SRC, 'results_tis_200.json'), encoding='utf-8'))
            if '__summary__' not in r and not r.get('error')]

    agg = defaultdict(lambda: {v: {'all': [], 'ok': [], 'bad': []} for v in ('top', 'front', 'side')})
    for r in recs:
        errs = sample_errors(r)
        if not errs:
            continue
        ok = correct(r)
        for view, (mean, n) in errs.items():
            if mean is None or n == 0:
                continue
            agg[r['arm']][view]['all'].append(mean)
            (agg[r['arm']][view]['ok'] if ok else agg[r['arm']][view]['bad']).append(mean)

    lines = ['# 场景重建准确率度量（200 条，对齐后逐物体位置误差）', '']
    lines.append('> 单位：10x10 网格格；误差 = 对齐后模型实例与 GT 实例的欧氏距离（greedy 匹配），逐样本取平均。')
    lines.append('')
    lines.append('| arm | 视图 | 平均误差 | 中位误差 | 样本数 | failure 平均 | correct 平均 | 差距(failure-correct) |')
    lines.append('|---|---|---|---|---|---|---|---|')
    for arm in ARMS:
        for view in ('top', 'front', 'side'):
            a = agg[arm][view]
            if not a['all']:
                continue
            lines.append('| %s | %s | %.2f | %.2f | %d | %.2f | %.2f | %+.2f |' % (
                arm, view, statistics.mean(a['all']), statistics.median(a['all']), len(a['all']),
                statistics.mean(a['bad']) if a['bad'] else float('nan'),
                statistics.mean(a['ok']) if a['ok'] else float('nan'),
                (statistics.mean(a['bad']) if a['bad'] else 0) - (statistics.mean(a['ok']) if a['ok'] else 0)))
    lines.append('')
    lines.append('结论：failure 样本的逐物体位置误差应明显高于 correct 样本；差距越大，说明位置误差与 QA 错误越相关。')

    out = os.path.join(os.path.dirname(SRC), 'docs', 'scene-reconstruction-accuracy.md')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('wrote', out)
    print('\n'.join(lines[:20]))


if __name__ == '__main__':
    main()
