# -*- coding: utf-8 -*-
"""Preliminary VGGT point cloud vs ReVSI GT comparison for scene0353_00."""
import json
import math

import numpy as np
from scipy.spatial import ConvexHull, cKDTree


def umeyama(src, dst, with_scale=True):
    n, m = src.shape
    mu_s = src.mean(0)
    mu_d = dst.mean(0)
    src_c = src - mu_s
    dst_c = dst - mu_d
    cov = dst_c.T @ src_c / n
    U, D, Vt = np.linalg.svd(cov)
    S = np.eye(m)
    if np.linalg.det(U) * np.linalg.det(Vt) < 0:
        S[-1, -1] = -1
    R = U @ S @ Vt
    if with_scale:
        var_s = np.sum(src_c ** 2) / n
        scale = np.trace(np.diag(D) @ S) / var_s if var_s > 1e-12 else 1.0
    else:
        scale = 1.0
    t = mu_d - scale * R @ mu_s
    return scale, R, t


def resample_perimeter(pts, n=128):
    pts = np.asarray(pts, dtype=float)
    pts = np.concatenate([pts, pts[:1]], axis=0)
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    total = cum[-1]
    if total <= 0:
        return pts[:n]
    ts = np.linspace(0, total, n)
    out = []
    j = 0
    for t in ts:
        while j < len(cum) - 2 and cum[j + 1] < t:
            j += 1
        u = (t - cum[j]) / max(cum[j + 1] - cum[j], 1e-12)
        out.append(pts[j] + u * (pts[j + 1] - pts[j]))
    return np.array(out)


def poly_area(poly):
    p = np.asarray(poly, dtype=float)
    x, y = p[:, 0], p[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def fit_floor(points, iters=3000, thresh_ratio=0.025):
    rng = np.random.default_rng(0)
    diag = float(np.linalg.norm(points.max(0) - points.min(0)))
    thresh = max(diag * thresh_ratio, 1e-6)
    best = None
    n = len(points)
    for _ in range(iters):
        idx = rng.choice(n, 3, replace=False)
        p = points[idx]
        v1, v2 = p[1] - p[0], p[2] - p[0]
        normal = np.cross(v1, v2)
        norm = np.linalg.norm(normal)
        if norm < 1e-9:
            continue
        normal = normal / norm
        d = -np.dot(normal, p[0])
        dist = np.abs(points @ normal + d)
        inliers = int((dist < thresh).sum())
        if best is None or inliers > best[0]:
            best = (inliers, normal, d)
    _, normal, d = best
    if normal[2] < 0:
        normal = -normal
        d = -d
    return normal, d


def rotate_to_floor(points, normal):
    z = np.array([0.0, 0.0, 1.0])
    axis = np.cross(normal, z)
    na = np.linalg.norm(axis)
    if na < 1e-9:
        return points.copy()
    axis = axis / na
    angle = math.acos(max(-1.0, min(1.0, float(np.dot(normal, z)))))
    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0],
    ])
    R = np.eye(3) + math.sin(angle) * K + (1 - math.cos(angle)) * (K @ K)
    return points @ R.T


def main():
    with open(r'tmp\revsi_3d_annotation.json', encoding='utf-8') as f:
        rev = json.load(f)
    gt = next(r for r in rev if r['scene_id'] == 'scene0353_00')
    gt_poly = np.array(gt['scene_area_2d_polygon'], dtype=float)
    gt_objects = gt['objects']

    d = np.load(r'tmp\vggt_out_scene0353_8f.npz')
    pm = d['point_map']
    pts = pm.reshape(-1, 3)
    pts = pts[np.isfinite(pts).all(1)]
    lo, hi = np.percentile(pts, 1, axis=0), np.percentile(pts, 99, axis=0)
    pts = pts[(pts >= lo).all(1) & (pts <= hi).all(1)]
    print('vggt points after filter', len(pts))

    normal, d_plane = fit_floor(pts)
    print('floor normal', np.round(normal, 3), 'd', round(d_plane, 4))
    pts = rotate_to_floor(pts, normal)
    pts[:, 2] -= pts[:, 2].min()
    zmax = np.percentile(pts[:, 2], 98)
    floor = pts[pts[:, 2] < 0.25 * zmax]
    print('floor-band points', len(floor), 'zmax', round(zmax, 4))
    xy = floor[:, :2]
    hull = ConvexHull(xy)
    hull_pts = xy[hull.vertices]
    vggt_perim = resample_perimeter(hull_pts, 128)
    gt_perim = resample_perimeter(gt_poly, 128)

    best = None
    for shift in (0, 32, 64, 96):
        src = np.roll(vggt_perim, shift, axis=0)
        scale, R, t = umeyama(src, gt_perim, with_scale=True)
        aligned = scale * (src @ R.T) + t
        err = float(np.mean(np.linalg.norm(aligned - gt_perim, axis=1)))
        if best is None or err < best[0]:
            best = (err, scale, R, t, shift)
    err, scale, R2, t2, shift = best
    print('perimeter alignment rmse m', round(err, 3), 'scale m/unit', round(scale, 3), 'shift', shift)

    def apply3(p):
        xy2 = scale * (p[:, :2] @ R2.T) + t2
        z2 = scale * p[:, 2]
        return np.column_stack([xy2, z2])

    pts_aligned = apply3(pts)
    print('aligned bbox', np.round(pts_aligned.min(0), 2), np.round(pts_aligned.max(0), 2))
    print('gt room area', round(poly_area(gt_poly), 2),
          'vggt hull area', round(poly_area(apply3(np.column_stack([hull_pts, np.zeros(len(hull_pts))]))[:, :2]), 2))

    tree = cKDTree(pts_aligned)
    print('\nobject-level nearest VGGT point distance (meters)')
    rows = []
    for o in gt_objects:
        c = np.array(o['obb']['center'], dtype=float)
        dist = float(tree.query(c)[0])
        size = float(np.linalg.norm(o['obb']['extent']))
        rows.append((o['name'], o['id'], round(dist, 2), round(size, 2), dist <= 0.6))
        print('%-24s id=%-3d nearest=%.2fm extent=%.2fm within=0.6m:%s' % (o['name'], o['id'], dist, size, dist <= 0.6))
    ok = sum(1 for r in rows if r[4])
    print('\nobjects within 0.6m of VGGT cloud: %d/%d' % (ok, len(rows)))
    print('SCALE', round(scale, 3))


if __name__ == '__main__':
    main()
