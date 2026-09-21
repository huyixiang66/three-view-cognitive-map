# -*- coding: utf-8 -*-
"""Answer the fixed 200 QA with the original video plus each system's cognitive map."""

import argparse
import json
from pathlib import Path

import run_vsi_3d_json as qa
import run_vsibench as vsi


SYSTEMS = {"RAS": "ras", "HoloScene": "holoscene", "SimFoundry": "simfoundry", "OVOW": "ovow"}


def load_samples(path, per_scene_limit):
    per_scene = {}
    for row in json.loads(Path(path).read_text(encoding="utf-8")):
        per_scene.setdefault(row["scene_name"], []).append(row)
    return {scene: rows[:per_scene_limit] for scene, rows in per_scene.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--samples",
        default=str(Path(__file__).resolve().parent / "vsi_four_system_200qa.json"),
    )
    parser.add_argument("--maps-root", required=True)
    parser.add_argument("--results-root", required=True)
    parser.add_argument("--video-root", required=True)
    parser.add_argument(
        "--category-list",
        default=str(Path(__file__).resolve().parent.parent / "docs" / "vsi_used_qa_asset_list.txt"),
    )
    parser.add_argument("--systems", nargs="+", default=list(SYSTEMS))
    parser.add_argument("--scenes", nargs="+")
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--model", default="gemini-3.5-flash")
    parser.add_argument("--sleep", type=float, default=3.0)
    parser.add_argument("--gate-policy", choices=["on", "off"], default="off")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    per_scene = load_samples(args.samples, args.n)
    scenes = args.scenes or list(per_scene)
    maps_root = Path(args.maps_root)
    results_root = Path(args.results_root)
    vocabulary = qa.load_category_vocabulary(args.category_list)

    skipped = []
    for scene in scenes:
        scene_samples = per_scene[scene]
        dataset = scene_samples[0]["dataset"]
        video_path = Path(args.video_root) / dataset / f"{scene}.mp4"

        pending = []
        for system in args.systems:
            output = results_root / system / f"{scene}.json"
            if output.is_file() and not args.overwrite and not args.dry_run:
                if len(json.loads(output.read_text(encoding="utf-8"))) == len(scene_samples):
                    print(f"skip (done): {system} {scene}", flush=True)
                    continue
            map_path = maps_root / system / f"{scene}_{SYSTEMS[system]}.json"
            if not map_path.is_file():
                skipped.append({"system": system, "scene": scene, "reason": "no validated map JSON"})
                print(f"skip (no map): {system} {scene}", flush=True)
                continue
            pending.append((system, map_path, output))

        if not pending:
            continue
        if args.dry_run:
            for system, map_path, output in pending:
                print(f"--- DRY RUN {system} {scene}", flush=True)
                qa.run_scene(
                    scene_samples,
                    json.loads(map_path.read_text(encoding="utf-8")),
                    None,
                    system,
                    vocabulary,
                    args.model,
                    args.sleep,
                    args.gate_policy,
                    dry_run=True,
                )
            continue

        video_b64 = vsi.load_video_base64(str(video_path))
        if not video_b64:
            raise RuntimeError(f"Could not load {video_path}")
        for system, map_path, output in pending:
            output.parent.mkdir(parents=True, exist_ok=True)
            print(f"--- {system} {scene}: {len(scene_samples)} questions", flush=True)
            rows = qa.run_scene(
                scene_samples,
                json.loads(map_path.read_text(encoding="utf-8")),
                video_b64,
                system,
                vocabulary,
                args.model,
                args.sleep,
                args.gate_policy,
                output=output,
            )
            print(f"--- {system} {scene}: {sum(row['correct'] for row in rows)}/{len(rows)}", flush=True)

    results_root.mkdir(parents=True, exist_ok=True)
    (results_root / "_skipped.json").write_text(
        json.dumps(skipped, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (results_root / "_run_config.json").write_text(
        json.dumps(
            {
                "samples": str(args.samples),
                "maps_root": str(maps_root),
                "video_root": str(args.video_root),
                "model": args.model,
                "sleep": args.sleep,
                "gate_policy": args.gate_policy,
                "systems": list(args.systems),
                "scenes": scenes,
                "questions_per_scene": args.n,
                "skipped": skipped,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"done; {len(skipped)} system/scene pairs skipped", flush=True)


if __name__ == "__main__":
    main()
