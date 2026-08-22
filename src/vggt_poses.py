# -*- coding: utf-8 -*-
"""Extract VGGT camera poses/intrinsics/depth/point maps from a video.

Output .npz keys:
    extrinsic (N, 3, 4): OpenCV camera-from-world [R | t]
    intrinsic (N, 3, 3): K = [[fx, 0, cx], [0, fy, cy], [0, 0, 1]]
    depth     (N, H, W, 1)
    point_map (N, H, W, 3)
    frames    (N,)
"""
import argparse
import os
import pathlib
import sys
import time

import cv2
import numpy as np
import torch
import torch.nn.init as init


def _meta_noop(orig):
    def wrapper(tensor, *args, **kwargs):
        if getattr(tensor, "is_meta", False):
            return tensor
        return orig(tensor, *args, **kwargs)
    return wrapper


# VGGT __init__ calls torch.linspace(...).item() and random inits, which have
# no kernels on meta tensors. Patch before importing VGGT so model construction
# can happen on meta (zero memory) and the 5GB checkpoint can be mmap-loaded.
# Without this, Windows maps the checkpoint to a low address after a normal
# model build and torch_cpu.dll crashes with an access violation.
init.trunc_normal_ = _meta_noop(init.trunc_normal_)
init.normal_ = _meta_noop(init.normal_)
init.zeros_ = _meta_noop(init.zeros_)
init.ones_ = _meta_noop(init.ones_)

_orig_linspace = torch.linspace


def _linspace_cpu(*args, **kwargs):
    return _orig_linspace(*args, **kwargs).cpu()


torch.linspace = _linspace_cpu


def build_model(vggt_repo, weights, device="cpu"):
    sys.path.insert(0, str(vggt_repo))
    from vggt.models.vggt import VGGT  # noqa: E402

    with torch.device("meta"):
        model = VGGT()
    try:
        sd = torch.load(weights, map_location="cpu", mmap=True)
    except TypeError:
        sd = torch.load(weights, map_location="cpu")
    model.load_state_dict(sd, assign=True)
    del sd
    return model.to(device).eval()


def extract_frames(video, n, max_side, frame_dir):
    cap = cv2.VideoCapture(str(video))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    if n <= 1:
        idxs = [0]
    else:
        idxs = sorted(set(int(i * (total - 1) / (n - 1)) for i in range(n)))
    frame_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, idx in enumerate(idxs):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, fr = cap.read()
        if not ok:
            continue
        h, w = fr.shape[:2]
        scale = max_side / max(h, w)
        if scale < 1:
            fr = cv2.resize(fr, (int(w * scale), int(h * scale)))
        p = frame_dir / ("f%02d.png" % i)
        cv2.imwrite(str(p), fr)
        paths.append(str(p))
    cap.release()
    return paths


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video", help="input video path")
    ap.add_argument("output", help="output .npz path")
    ap.add_argument("--frames", type=int, default=int(os.environ.get("VGGT_FRAMES", "8")))
    ap.add_argument("--size", type=int, default=98, help="square input size, multiple of 14")
    ap.add_argument("--max-side", type=int, default=384)
    ap.add_argument("--vggt-repo", default=os.environ.get("VGGT_REPO", ""))
    ap.add_argument("--weights", default=os.environ.get("VGGT_WEIGHTS", ""))
    ap.add_argument("--threads", type=int, default=int(os.environ.get("VGGT_THREADS", "4")))
    ap.add_argument("--device", default=os.environ.get("VGGT_DEVICE", "cpu"), choices=["cpu", "cuda"])
    ap.add_argument("--frame-dir", default="", help="frame output dir; default <output_stem>_frames")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parents[1]
    vggt_repo = pathlib.Path(args.vggt_repo) if args.vggt_repo else root / "vggt"
    weights = pathlib.Path(args.weights) if args.weights else root / "vggt_weights" / "model.pt"
    if not vggt_repo.exists():
        ap.error("VGGT repo not found: %s (set VGGT_REPO or --vggt-repo)" % vggt_repo)
    if not weights.exists():
        ap.error("VGGT weights not found: %s (set VGGT_WEIGHTS or --weights)" % weights)

    size = args.size - args.size % 14
    torch.set_num_threads(args.threads)
    t0 = time.time()
    if args.device == "cuda" and not torch.cuda.is_available():
        ap.error("--device cuda requested but CUDA is not available")
    print("start frames=%d size=%d device=%s" % (args.frames, size, args.device), flush=True)

    model = build_model(vggt_repo, weights, args.device)
    print("model ready %.1fs" % (time.time() - t0), flush=True)

    out = pathlib.Path(args.output)
    frame_dir = pathlib.Path(args.frame_dir) if args.frame_dir else out.with_name(out.stem + "_frames")
    paths = extract_frames(args.video, args.frames, args.max_side, frame_dir)
    print("frames:", paths, flush=True)
    if not paths:
        ap.error("no frames extracted from %s" % args.video)

    from vggt.utils.load_fn import load_and_preprocess_images_square  # noqa: E402
    from vggt.utils.pose_enc import pose_encoding_to_extri_intri  # noqa: E402

    images, _ = load_and_preprocess_images_square(paths, target_size=size)
    images = images.to(args.device)

    with torch.no_grad():
        images = images[None]
        print("aggregator start", flush=True)
        agg, ps = model.aggregator(images)
        print("camera head start", flush=True)
        pose_enc = model.camera_head(agg)[-1]
        print("depth head start", flush=True)
        extrinsic, intrinsic = pose_encoding_to_extri_intri(pose_enc, images.shape[-2:])
        depth_map, depth_conf = model.depth_head(agg, images, ps)
        print("point head start", flush=True)
        point_map, point_conf = model.point_head(agg, images, ps)

    extrinsic = extrinsic.squeeze(0).cpu().numpy()
    intrinsic = intrinsic.squeeze(0).cpu().numpy()
    depth = depth_map.squeeze(0).cpu().numpy()
    points = point_map.squeeze(0).cpu().numpy()
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez(out, extrinsic=extrinsic, intrinsic=intrinsic, depth=depth,
             point_map=points, frames=np.asarray(paths))
    print("saved:", out, "extrinsic", extrinsic.shape,
          "intrinsic", intrinsic.shape, "depth", depth.shape,
          "total %.1fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
