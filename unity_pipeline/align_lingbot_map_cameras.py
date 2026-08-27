#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert LingBot-Map predictions (c2w + intrinsic + world_points) to Unity cameras.

Input: a single predictions.npz with:
  extrinsic  (N, 3, 4)  camera-to-world in OpenCV convention
  intrinsic  (N, 3, 3)
  depth (N, H, W, 1) preferred; world_points (N, H, W, 3) fallback

Output: the same Unity camera JSON used by CogMapVGGTRenderer.
Depth is unprojected to a point cloud (the published checkpoint has no point_head weights); --width/--height
rescale K to the original video frame size for direct V vs V' comparison.
"""
import argparse
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from align_vggt_cameras import (  # noqa: E402
    build_grid_similarity,
    build_vggt_similarity,
    combine,
    load_gt,
)




def unproject_depth_to_world(depth, intrinsic, c2w):
    """Unproject predicted depth with each frame's K and camera-to-world pose."""
    n, h, w, _ = depth.shape
    ys, xs = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")
    ones = np.ones_like(xs)
    pixels = np.stack([xs, ys, ones], axis=-1).astype(np.float32)
    pts = np.zeros((n, h, w, 3), dtype=np.float32)
    for i in range(n):
        cam = pixels @ np.linalg.inv(intrinsic[i]).T * depth[i].astype(np.float32)
        pts[i] = cam @ c2w[i, :, :3].T + c2w[i, :, 3]
    return pts

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
    ap.add_argument("--fixed-k", action="store_true")
    ap.add_argument("--width", type=int, default=0, help="rescale output K to this width")
    ap.add_argument("--height", type=int, default=0, help="rescale output K to this height")
    ap.add_argument("--loop-pairs", default="", help="comma-separated same-view frame pairs, e.g. 0=7,1=4")
    ap.add_argument("--use-camera-up", action="store_true",
                    help="estimate floor normal from mean camera up instead of RANSAC")
    ap.add_argument("--transform-json", default="",
                    help="use an existing A/b/R transform JSON instead of fitting depth")
    args = ap.parse_args()

    d = np.load(args.npz)
    if "extrinsic" not in d or "intrinsic" not in d:
        raise ValueError("npz must contain extrinsic/intrinsic; got " + str(d.files))
    c2w = d["extrinsic"]
    intr = d["intrinsic"]

    frames = []
    info = pathlib.Path(args.npz).with_name("info.json")
    if info.exists():
        frames = json.loads(info.read_text(encoding="utf-8")).get("frames", [])
    elif "frames" in d:
        frames = [str(x) for x in d["frames"]]

    # Depth unprojection is the validated path for the published checkpoint; the
    # checkpoint has no point_head weights, so world_points should not be trusted.
    if "depth" in d:
        pts = unproject_depth_to_world(d["depth"], intr, c2w).reshape(-1, 3)
    elif "world_points" in d:
        pts = d["world_points"].reshape(-1, 3)
    else:
        raise ValueError("npz must contain depth or world_points")
    pts = pts[np.isfinite(pts).all(1)]
    lo, hi = np.percentile(pts, 1, axis=0), np.percentile(pts, 99, axis=0)
    pts = pts[(pts >= lo).all(1) & (pts <= hi).all(1)]

    gt_poly = load_gt(args.scene_id)
    floor_normal = None
    if args.use_camera_up:
        ups = np.array([c2w[i, :3, :3].T @ np.array([0.0, -1.0, 0.0]) for i in range(len(c2w))])
        floor_normal = ups.mean(0)
        floor_normal = floor_normal / np.linalg.norm(floor_normal)
        print("camera-up floor normal:", np.round(floor_normal, 3), flush=True)
    if args.transform_json:
        tf = json.loads(pathlib.Path(args.transform_json).read_text(encoding="utf-8"))
        A = np.array(tf["A"], dtype=float)
        b = np.array(tf["b"], dtype=float)
        cR = np.array(tf["R"], dtype=float)
        scale_out = float(tf.get("scale", 1.0))
        rmse_out = float(tf.get("lingbot_gt_rmse_m", tf.get("vggt_gt_rmse_m", 0.0)))
        grid_rmse_out = float(tf.get("grid_gt_rmse_m", 0.0))
        ling_scale_out = float(tf.get("lingbot_scale", tf.get("vggt_scale", 0.0)))
        grid_scale_out = float(tf.get("grid_scale", 0.0))
        print("using external transform:", args.transform_json, flush=True)
    else:
        v = build_vggt_similarity(pts, gt_poly, floor_normal=floor_normal)
        g = build_grid_similarity(gt_poly)
        c = combine(v, g)
        print("lingbot->gt rmse(m):", round(v["rmse"], 3), "scale:", round(v["scale"], 3))
        print("grid->gt rmse(m):", round(g["rmse"], 3), "scale:", round(g["scale"], 3))
        print("combined scale:", round(c["scale"], 3), "det(R):", round(float(np.linalg.det(c["R"])), 3))
        A = c["scale"] * c["R"]
        b = c["b"]
        cR = c["R"]
        scale_out = c["scale"]
        rmse_out = v["rmse"]
        grid_rmse_out = g["rmse"]
        ling_scale_out = v["scale"]
        grid_scale_out = g["scale"]

    perm = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]])
    cameras = []
    centers = []
    for i in range(len(c2w)):
        R = c2w[i, :, :3]
        t = c2w[i, :, 3]
        p0 = -R.T @ t
        p_gt = A @ p0 + b
        p_unity = perm @ p_gt
        r_new = R @ cR.T
        r_unity = r_new @ perm.T
        if np.linalg.det(r_unity) < 0:
            r_unity = r_unity @ np.diag([-1.0, 1.0, 1.0])
        fwd = r_unity.T @ np.array([0.0, 0.0, 1.0])
        world_up = np.array([0.0, 1.0, 0.0])
        up = world_up - fwd * float(np.dot(world_up, fwd))
        if np.linalg.norm(up) > 1e-4:
            up = up / np.linalg.norm(up)
            right = np.cross(up, fwd)
            right = right / np.linalg.norm(right)
            r_unity = np.vstack([right, -up, fwd])
        t_unity = -r_unity @ p_unity
        centers.append(p_unity)
        k = intr[i]
        w0 = int(round(2.0 * k[0, 2]))
        h0 = int(round(2.0 * k[1, 2]))
        if args.width > 0 and args.height > 0:
            w0, h0 = args.width, args.height
            if args.fixed_k:
                fy = 1.1 * h0
                k_out = [fy * w0 / h0, 0.0, w0 / 2.0,
                         0.0, fy, h0 / 2.0, 0.0, 0.0, 1.0]
            else:
                sx = w0 / float(2.0 * k[0, 2])
                sy = h0 / float(2.0 * k[1, 2])
                k0 = [float(x) for row in k for x in row]
                k_out = [k0[0] * sx, 0.0, w0 / 2.0,
                         0.0, k0[4] * sy, h0 / 2.0, 0.0, 0.0, 1.0]
        else:
            k_out = fixed_k(k) if args.fixed_k else [float(x) for row in k for x in row]
        cameras.append({
            "R": [float(x) for row in r_unity for x in row],
            "t": [float(x) for x in t_unity],
            "K": k_out,
            "width": w0,
            "height": h0,
        })

    if args.loop_pairs:
        for part in args.loop_pairs.split(","):
            part = part.strip()
            if not part:
                continue
            a_str, b_str = part.split("=")
            ia, ib = int(a_str), int(b_str)
            p = (centers[ia] + centers[ib]) / 2.0
            for idx in (ia, ib):
                Rm = np.array(cameras[idx]["R"]).reshape(3, 3)
                cameras[idx]["t"] = [float(x) for x in (-Rm @ p)]
                centers[idx] = p
    centers = np.array(centers)
    print("camera centers (unity):")
    for i, p in enumerate(centers):
        print(f"  {i}: {np.round(p, 3)}")
    print("min:", np.round(centers.min(0), 3), "max:", np.round(centers.max(0), 3))

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"frames": frames,
                               "cameras": cameras}, indent=2), encoding="utf-8")
    print("saved:", out)

    tf_out = out.with_suffix(".transform.json")
    tf_out.write_text(json.dumps({
        "A": A.tolist(),
        "b": b.tolist(),
        "scale": scale_out,
        "R": cR.tolist(),
        "lingbot_gt_rmse_m": rmse_out,
        "grid_gt_rmse_m": grid_rmse_out,
        "lingbot_scale": ling_scale_out,
        "grid_scale": grid_scale_out,
    }, indent=2), encoding="utf-8")
    print("saved transform:", tf_out)


if __name__ == "__main__":
    main()
