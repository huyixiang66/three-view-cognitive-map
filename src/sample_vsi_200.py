# -*- coding: utf-8 -*-
"""Sample 200 VSI-Bench questions: 8 type groups x 25, stratified by dataset.

Reads tmp/vsi_full_test.jsonl, writes src/vsi_subset_200.json.
"""
import io
import re
import json
import os
import random
import sys
from collections import Counter, defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
FULL = os.path.join(SRC_DIR, "..", "tmp", "vsi_full_test.jsonl")
OUT = os.path.join(SRC_DIR, "vsi_subset_200.json")
SEED = 42
N_PER_GROUP = 25

GROUPS = {
    "object_counting": ["object_counting"],
    "object_abs_distance": ["object_abs_distance"],
    "object_size_estimation": ["object_size_estimation"],
    "room_size_estimation": ["room_size_estimation"],
    "object_rel_distance": ["object_rel_distance"],
    "object_rel_direction": [
        "object_rel_direction_easy",
        "object_rel_direction_medium",
        "object_rel_direction_hard",
    ],
    "route_planning": ["route_planning"],
    "obj_appearance_order": ["obj_appearance_order"],
}

def normalize_name(name):
    n = str(name).strip().lower().replace('_', ' ')
    n = re.sub(r'[.,;:!?\'\"]+$', '', n)
    return re.sub(r'\s+', ' ', n).strip()

def ext_for(r):
    """Extension fields for question types the map pipeline does not natively cover."""
    qt = r["question_type"]
    q = r["question"] or ""
    opts = r.get("options") or []
    cats = []
    needs_size = False
    room = False
    if qt == "object_counting":
        m = re.search(r"How many (.+?)\(?s?\)? (?:are|is) in", q)
        if m:
            cats = [normalize_name(m.group(1))]
    elif qt.startswith("object_size_estimation"):
        m = re.search(r"size of (?:the )?(.+?)(?:\?| in)", q)
        if m:
            cats = [normalize_name(m.group(1))]
        needs_size = True
    elif qt.startswith("room_size"):
        room = True
    else:
        for o in opts:
            for p in re.split(r"[-,]", o):
                c = normalize_name(re.sub(r"^[A-D][.\\)-]\s*", "", p))
                if c and c not in cats:
                    cats.append(c)
    return {"target_categories": cats, "needs_size": needs_size, "room": room}


def main():
    with open(FULL, encoding="utf-8") as f:
        recs = [json.loads(l) for l in f if l.strip()]
    print("full:", len(recs), Counter(r["question_type"] for r in recs))

    rng = random.Random(SEED)
    sampled = []
    for group, types in GROUPS.items():
        pool = [r for r in recs if r["question_type"] in types]
        by_ds = defaultdict(list)
        for r in pool:
            by_ds[r["dataset"]].append(r)
        for ds in by_ds:
            rng.shuffle(by_ds[ds])
        # distribute quota round-robin over datasets
        out = []
        nds = len(by_ds)
        idx = {ds: 0 for ds in by_ds}
        while len(out) < N_PER_GROUP:
            progressed = False
            for ds in list(by_ds):
                if len(out) >= N_PER_GROUP:
                    break
                if idx[ds] < len(by_ds[ds]):
                    out.append(by_ds[ds][idx[ds]])
                    idx[ds] += 1
                    progressed = True
            if not progressed:
                break  # pool exhausted
        for r in out[:N_PER_GROUP]:
            sampled.append({
                "id": r["id"],
                "dataset": r["dataset"],
                "scene_name": r["scene_name"],
                "question_type": r["question_type"],
                "type_group": group,
                "question": r["question"],
                "ground_truth": r["ground_truth"],
                "options": r.get("options"),
                "ext": ext_for(r),
            })
    print("sampled:", len(sampled), Counter(x["type_group"] for x in sampled))
    print("by dataset:", Counter(x["dataset"] for x in sampled))

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(sampled, f, indent=2, ensure_ascii=False)
    print("wrote", OUT)

    # video cache coverage
    cache = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "vsibench")
    missing = []
    for r in sampled:
        p = os.path.join(cache, r["dataset"], r["scene_name"] + ".mp4")
        if not os.path.exists(p):
            missing.append((r["dataset"], r["scene_name"]))
    print("missing videos:", len(missing), "of", len(sampled))
    print("missing scenes:", missing[:40])


if __name__ == "__main__":
    main()
