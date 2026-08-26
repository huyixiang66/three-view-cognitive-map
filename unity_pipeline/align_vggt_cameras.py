#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Align VGGT cameras to the cogmap grid with a true 3D similarity.

The scene_3d.json (grid units) is never modified. Only the VGGT extrinsics
are converted: the camera center is mapped by the similarity and the camera
orientation is re-expressed as an orthonormal world-to-camera rotation, so
Unity's position = -R^T t formula is valid again.

Usage:
  python align_vggt_cameras.py vggt_out.npz scene0353_00 out.json
"""
import argparse
import json
import math
import pathlib
import sys

import numpy as np
from scipy.spatial import ConvexHull

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from vggt_vs_gt import fit_floor, resample_perimeter, umeyama  # noqa: E402

GRID_PERIM = np.array([[0.0, 0.0], [9.0, 0.0], [9.0, 9.0], [0.0, 9.0]])
GT_POLYGONS = pathlib.Path(__file__).resolve().parent / "examples" / "gt_polygons.json"


def load_gt(scene_id):
    data = json.loads(GT_POLYGONS.read_text(encoding="utf-8"))
    return np.array(data[scene_id]["scene_area_2d_polygon"], dtype=float)


def floor_rotation(normal):
    """Rotation matrix R such that R @ p has z pointing up (normal aligned)."""
    z = np.array([0.0, 0.0, 1.0])
    axis = np.cross(normal, z)
    na = np.linalg.norm(axis)
    if na < 1e-9:
        return np.eye(3)
    axis = axis / na
    angle = math.acos(max(-1.0, min(1.0, float(np.dot(normal, z)))))
    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0],
    ])
    return np.eye(3) + math.sin(angle) * K + (1 - math.cos(angle)) * (K @ K)


def best_2d_similarity(src_perim, dst_perim):
    best = None
    for shift in (0, 32, 64, 96):
        src = np.roll(src_perim, shift, axis=0)
        scale, rot, trans = umeyama(src, dst_perim, with_scale=True)
        aligned = scale * (src @ rot.T) + trans
        err = float(np.mean(np.linalg.norm(aligned - dst_perim, axis=1)))
        if best is None or err < best[0]:
            best = (err, scale, rot, trans, shift)
    return best


def build_vggt_similarity(points, gt_poly):
    normal, _ = fit_floor(points)
    r_floor = floor_rotation(normal)
    rot_pts = points @ r_floor.T
    z = rot_pts[:, 2].copy()
    z0 = float(np.percentile(z, 5))
    z = z - z0
    zmax = float(np.percentile(z, 98))
    floor = z < 0.5 * zmax
    xy = rot_pts[:, :2]

    hull = ConvexHull(xy[floor])
    src_perim = resample_perimeter(xy[floor][hull.vertices], 128)
    dst_perim = resample_perimeter(gt_poly, 128)
    err, s, rot2, trans, shift = best_2d_similarity(src_perim, dst_perim)

    # p_gt = s * (R_v2g @ p_vggt) + b_v, with z0 removed and re-scaled.
    r_v2g = np.eye(3)
    r_v2g[:2, :] = rot2 @ r_floor[:2, :]
    r_v2g[2, :] = r_floor[2, :]
    b_v = np.array([trans[0], trans[1], -s * z0])
    return {"rmse": err, "scale": s, "R": r_v2g, "b": b_v, "shift": shift}


def build_grid_similarity(gt_poly):
    src_perim = resample_perimeter(GRID_PERIM, 128)
    dst_perim = resample_perimeter(gt_poly, 128)
    err, s, rot2, trans, shift = best_2d_similarity(src_perim, dst_perim)
    r_g2g = np.eye(3)
    r_g2g[:2, :2] = rot2
    b_g = np.array([trans[0], trans[1], 0.0])
    return {"rmse": err, "scale": s, "R": r_g2g, "b": b_g, "shift": shift}


def combine(v, g):
    # p_grid = (1/s_g) R_g^T (p_gt - b_g), p_gt = s_v R_v p + b_v.
    s = v["scale"] / g["scale"]
    r_c = g["R"].T @ v["R"]
    b_c = (g["R"].T @ (v["b"] - g["b"])) / g["scale"]
    return {"scale": s, "R": r_c, "b": b_c}


def fixed_k(k):
    h = int(round(2.0 * k[1, 2]))
    w = int(round(2.0 * k[0, 2]))
    fy = 1.1 * h
    fx = fy * w / h
    return [fx, 0.0, w / 2.0, 0.0, fy, h / 2.0, 0.0, 0.0, 1.0]


def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("npz")
    ap.add_argument("scene_id")
    ap.add_argument("out")
    ap.add_argument("--fixed-k", action="store_true", help="use fy=1.1*H official-demo approximation instead of VGGT K")
    args = ap.parse_args()

    d = np.load(args.npz)
    pm = d["point_map"]
    pts = pm.reshape(-1, 3)
    pts = pts[np.isfinite(pts).all(1)]
    lo, hi = np.percentile(pts, 1, axis=0), np.percentile(pts, 99, axis=0)
    pts = pts[(pts >= lo).all(1) & (pts <= hi).all(1)]

    gt_poly = load_gt(args.scene_id)
    v = build_vggt_similarity(pts, gt_poly)
    g = build_grid_similarity(gt_poly)
    c = combine(v, g)

    print("vggt->gt rmse(m):", round(v["rmse"], 3), "scale:", round(v["scale"], 3))
    print("grid->gt rmse(m):", round(g["rmse"], 3), "scale:", round(g["scale"], 3))
    print("combined scale:", round(c["scale"], 3), "det(R):", round(float(np.linalg.det(c["R"])), 3))

    A = c["scale"] * c["R"]
    b = c["b"]
    ext = d["extrinsic"]
    intr = d["intrinsic"]
    frames = [str(x) for x in d["frames"]]

    cameras = []
    centers = []
    for i in range(len(ext)):
        r0 = ext[i][:, :3]
        t0 = ext[i][:, 3]
        p0 = -r0.T @ t0
        p_grid = A @ p0 + b
        r_new = r0 @ c["R"].T
        # Cogmap grid order is (x, depth, height); Unity world is (x, height, depth).
        perm = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]])
        p_unity = perm @ p_grid
        r_unity = r_new @ perm.T
        # perm is a reflection (det=-1); flip camera x to keep a proper rotation.
        if np.linalg.det(r_unity) < 0:
            r_unity = r_unity @ np.diag([-1.0, 1.0, 1.0])
        # Keep the camera upright like a hand-held phone: remove roll around forward.
        fwd = r_unity.T @ np.array([0.0, 0.0, 1.0])
        world_up = np.array([0.0, 1.0, 0.0])
        up = world_up - fwd * float(np.dot(world_up, fwd))
        if np.linalg.norm(up) > 1e-4:
            up = up / np.linalg.norm(up)
            right = np.cross(up, fwd)
            right = right / np.linalg.norm(right)
            # Keep OpenCV y-down convention: renderer flips y once in SetPose.
            r_unity = np.vstack([right, -up, fwd])
        t_unity = -r_unity @ p_unity
        centers.append(p_unity)
        cameras.append({
            "R": [float(x) for row in r_unity for x in row],
            "t": [float(x) for x in t_unity],
            "K": fixed_k(intr[i]) if args.fixed_k else [float(x) for row in intr[i] for x in row],
            "width": int(round(2.0 * intr[i][0, 2])),
            "height": int(round(2.0 * intr[i][1, 2])),
        })

    centers = np.array(centers)
    print("camera centers (unity):")
    for i, p in enumerate(centers):
        print(f"  {i}: {np.round(p, 3)}")
    print("min:", np.round(centers.min(0), 3), "max:", np.round(centers.max(0), 3),
          "std:", np.round(centers.std(0), 3))

    payload = {"frames": frames, "cameras": cameras}
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    tf_out = out.with_suffix(".transform.json")
    tf_out.write_text(json.dumps({
        "A": A.tolist(),
        "b": b.tolist(),
        "scale": c["scale"],
        "R": c["R"].tolist(),
        "vggt_gt_rmse_m": v["rmse"],
        "grid_gt_rmse_m": g["rmse"],
        "vggt_scale": v["scale"],
        "grid_scale": g["scale"],
    }, indent=2), encoding="utf-8")
    print("saved:", out, "cameras:", len(cameras))


if __name__ == "__main__":
    main()
