#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build scene_3d.json from a yaw-enabled cogmap, preserving object yaw.

Reuses the senior fuse script with --z-anchor center semantics, then attaches
a circular-mean yaw per object name from the three views.
"""
import argparse
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fuse_views_to_3d import fuse  # noqa: E402


def mean_angle(angles):
    xs = sum(math.cos(math.radians(a)) for a in angles)
    ys = sum(math.sin(math.radians(a)) for a in angles)
    return math.degrees(math.atan2(ys, xs))


def view_yaws(cogmap):
    out = {}
    for view in ("top_view", "front_view", "side_view"):
        for obj in (cogmap.get(view) or {}).get("objects", []):
            name = str(obj.get("name", "")).strip()
            yaw = obj.get("yaw")
            if yaw is not None:
                out.setdefault(name, []).append(float(yaw))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cogmap")
    ap.add_argument("out")
    args = ap.parse_args()

    cogmap = json.loads(pathlib.Path(args.cogmap).read_text(encoding="utf-8"))
    scene = fuse(cogmap, z_anchor="center")
    yaws = view_yaws(cogmap)

    for obj in scene.get("objects", []):
        name = obj["name"]
        if name in yaws:
            obj["yaw"] = round(mean_angle(yaws[name]), 1)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(scene, indent=2, ensure_ascii=False), encoding="utf-8")
    print("saved:", out)
    for obj in scene["objects"]:
        print(f"  {obj['name']:<14} center=({obj['x']}, {obj['y']}, {obj['z']}) "
              f"size=({obj['sizeX']}, {obj['sizeY']}, {obj['sizeZ']}) yaw={obj.get('yaw')}")


if __name__ == "__main__":
    main()
