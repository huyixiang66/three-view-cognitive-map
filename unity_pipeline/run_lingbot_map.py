#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LingBot-Map inference: video frames -> pose/depth npz.

Mirrors the official streaming demo without viser/rendering. Output is the
same schema used by align_vggt_cameras.py / align_lingbot_map_cameras.py:
  extrinsic  (N, 3, 4) camera-to-world (OpenCV convention)
  intrinsic  (N, 3, 3)
  depth      (N, H, W, 1)

Usage:
  python unity_pipeline/run_lingbot_map.py \
    --model_path /path/to/lingbot-map.pt \
    --image_folder frames_dir \
    --out lingbot_out \
    --lingbot_root /path/to/lingbot-map
"""
import argparse
import contextlib
import json
import math
import pathlib
import sys
import time

import numpy as np
import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))


def _interpolate_pos_embed(pe, target_tokens, dim):
    """Bilinear-interpolate the spatial part of a learned pos_embed."""
    n = pe.shape[1] - 1
    side = int(round(math.sqrt(n)))
    if side * side != n:
        raise ValueError(f"pos_embed spatial tokens {n} is not a square grid")
    tside = int(round(math.sqrt(target_tokens - 1)))
    if tside * tside != target_tokens - 1:
        raise ValueError(f"target pos_embed tokens {target_tokens - 1} is not a square grid")
    spatial = pe[0, 1:].reshape(side, side, dim).permute(2, 0, 1).unsqueeze(0)
    resized = torch.nn.functional.interpolate(
        spatial, size=(tside, tside), mode="bilinear", align_corners=False
    )[0].permute(1, 2, 0).reshape(1, target_tokens - 1, dim)
    return torch.cat([pe[:, :1], resized], dim=1)


def load_model(args, device):
    if args.mode == "windowed":
        from lingbot_map.models.gct_stream_window import GCTStream
    else:
        from lingbot_map.models.gct_stream import GCTStream

    model = GCTStream(
        img_size=args.image_size,
        patch_size=args.patch_size,
        enable_3d_rope=True,
        max_frame_num=1024,
        kv_cache_sliding_window=64,
        kv_cache_scale_frames=args.num_scale_frames,
        kv_cache_cross_frame_special=True,
        kv_cache_include_scale_frames=True,
        use_sdpa=args.use_sdpa,
        camera_num_iterations=args.camera_num_iterations,
    )
    if args.model_path:
        ckpt = torch.load(args.model_path, map_location=device, weights_only=False)
        state = ckpt.get("model", ckpt)
        key = "aggregator.patch_embed.pos_embed"
        if key in state and key in model.state_dict():
            pe = state[key]
            target = model.state_dict()[key]
            if tuple(pe.shape) != tuple(target.shape):
                print(f"interpolating {key}: {tuple(pe.shape)} -> {tuple(target.shape)}", flush=True)
                state[key] = _interpolate_pos_embed(
                    pe.to(torch.float32), target.shape[1], target.shape[-1]
                ).to(pe.dtype)
        missing, unexpected = model.load_state_dict(state, strict=False)
        if missing:
            print(f"  Missing keys: {len(missing)}", flush=True)
        if unexpected:
            print(f"  Unexpected keys: {len(unexpected)}", flush=True)
        print("  Checkpoint loaded.", flush=True)
    return model.to(device).eval()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_path", required=True)
    ap.add_argument("--image_folder", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--lingbot_root", default="tmp/lingbot-map-local")
    ap.add_argument("--image_size", type=int, default=518)
    ap.add_argument("--patch_size", type=int, default=14)
    ap.add_argument("--num_scale_frames", type=int, default=8)
    ap.add_argument("--camera_num_iterations", type=int, default=4)
    ap.add_argument("--mode", default="streaming", choices=["streaming", "windowed"])
    ap.add_argument("--window_size", type=int, default=64)
    ap.add_argument("--overlap_size", type=int, default=16)
    ap.add_argument("--first_k", type=int, default=None)
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--use_sdpa", action="store_true", default=True)
    ap.add_argument("--device", default="cpu")
    args = ap.parse_args()

    root = pathlib.Path(args.lingbot_root).resolve()
    sys.path.insert(0, str(root))
    import demo  # noqa: E402

    if args.device == "cpu":
        torch.compiler.cudagraph_mark_step_begin = lambda: None

    device = torch.device(args.device)
    t0 = time.time()
    images, paths, _ = demo.load_images(
        image_folder=args.image_folder,
        image_size=args.image_size,
        patch_size=args.patch_size,
        first_k=args.first_k,
        stride=args.stride,
    )
    print(f"images {tuple(images.shape)} from {len(paths)} frames", flush=True)

    model = load_model(args, device)
    print(f"model loaded {time.time() - t0:.1f}s", flush=True)

    images = images.to(device)
    with torch.no_grad(), contextlib.nullcontext():
        if args.mode == "streaming":
            predictions = model.inference_streaming(
                images,
                num_scale_frames=args.num_scale_frames,
                keyframe_interval=1,
                output_device=torch.device("cpu"),
            )
        else:
            predictions = model.inference_windowed(
                images,
                window_size=args.window_size,
                overlap_size=args.overlap_size,
                num_scale_frames=args.num_scale_frames,
                keyframe_interval=1,
                output_device=torch.device("cpu"),
            )
    print(f"inference done {time.time() - t0:.1f}s", flush=True)

    predictions, _ = demo.postprocess(predictions, images)
    print("keys:", sorted(predictions.keys()), flush=True)

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    saved = {}
    for k, v in predictions.items():
        if isinstance(v, torch.Tensor):
            v = v.detach().cpu().numpy()
        if isinstance(v, np.ndarray):
            saved[k] = v
    np.savez(out / "predictions.npz", **saved)
    with open(out / "info.json", "w", encoding="utf-8") as f:
        json.dump({"frames": paths, "keys": sorted(saved.keys())}, f, indent=2)
    print("saved", out / "predictions.npz", flush=True)



if __name__ == "__main__":
    main()
