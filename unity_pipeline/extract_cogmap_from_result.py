#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract a yaw-enabled cogmap for one scene from a task1 result file.

The result stores flattened per-view objects in `cogmap_objects` (with yaw)
and sizes inside the `raw_map` JSON string. This script rebuilds the standard
cogmap format (top_view/front_view/side_view + gridSize).
"""
import argparse
import json
import pathlib


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("result")
    ap.add_argument("scene_id")
    ap.add_argument("out")
    args = ap.parse_args()

    results = json.loads(pathlib.Path(args.result).read_text(encoding="utf-8"))
    rec = next(r for r in results if r.get("scene") == args.scene_id)
    cogmap_objects = rec.get("cogmap_objects") or []
    raw_map = json.loads(rec.get("raw_map") or "{}")
    sizes = raw_map.get("sizes") or {}

    views = {"top_view": {}, "front_view": {}, "side_view": {}}
    view_key = {"top_view": "top", "front_view": "front", "side_view": "side"}
    for obj in cogmap_objects:
        view = obj["view"]
        if view not in views:
            continue
        name = str(obj["name"]).strip()
        entry = {
            "name": name,
            "yaw": float(obj.get("yaw", 0.0)),
        }
        if view == "top_view":
            entry["x"] = float(obj["x"])
            entry["y"] = float(obj["y"])
        elif view == "front_view":
            entry["x"] = float(obj["x"])
            entry["z"] = float(obj["z"])
        else:
            entry["y"] = float(obj["y"])
            entry["z"] = float(obj["z"])

        sz = (sizes.get(view_key[view]) or {}).get(name)
        if sz:
            entry["size"] = [float(v) for v in sz[0]]
        views[view].setdefault(name, []).append(entry)

    cogmap = {"gridSize": 10}
    for view in ("top_view", "front_view", "side_view"):
        objects = []
        for name in views[view]:
            objects.extend(views[view][name])
        cogmap[view] = {"gridSize": 10, "objects": objects}

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cogmap, indent=2, ensure_ascii=False), encoding="utf-8")
    print("saved:", out)
    for view in ("top_view", "front_view", "side_view"):
        print(view, [(o["name"], o.get("yaw")) for o in cogmap[view]["objects"]])


if __name__ == "__main__":
    main()
