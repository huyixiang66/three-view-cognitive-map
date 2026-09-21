# -*- coding: utf-8 -*-
"""Answer VSI-Bench questions from the original video plus reconstructed 3D JSON."""

import argparse
import json
import re
from pathlib import Path

import run_vsibench as vsi

from prompts_external_map import (
    ANSWER_PROMPT_ABS_DISTANCE_EXT,
    ANSWER_PROMPT_APPEARANCE_EXT,
    ANSWER_PROMPT_COUNTING_EXT,
    ANSWER_PROMPT_REL_DISTANCE_EXT,
    ANSWER_PROMPT_REL_DIRECTION_EXT,
    ANSWER_PROMPT_ROOM_EXT,
    ANSWER_PROMPT_ROUTE_EXT,
    ANSWER_PROMPT_SIZE_EXT,
)


vsi.USE_SELFCHECK = False
vsi.USE_FACTS = False
vsi.USE_TASKAWARE = False


SYSTEM_PROMPT = """You answer VSI-Bench spatial questions.
You receive the original room video and a reconstructed three-view cognitive map on a 10x10 grid.
The reconstruction comes from an external system and is not guaranteed to be correct: it may be
incomplete, contain duplicate instances, use a non-metric scale, or have an arbitrary horizontal
orientation. Weigh it against the video, which decides whenever the two disagree or the map does
not contain the asked object, and follow the requested answer format exactly. Always commit to a
best estimate instead of reporting that objects are absent or that the answer cannot be
determined."""


MAP_SCHEMA_NOTE = """Three-view cognitive map (grid units on a 10x10 grid).
Each view maps a category name to a list of instances; each instance is
[x, y, width, height, yaw_degrees], where the first two numbers are the center, the next two are
the extent along the view's two axes, and yaw_degrees is the object's horizontal rotation in
degrees (null when it could not be determined).
- top view (x, y): x = left-to-right, y = depth, width/height = footprint
- front view (x, z): x matches the top view, z = height above the floor
- side view (y, z): y matches the top view, z matches the front view
- room: width/depth are the grid extents; area_m2 is null when the map has no metric scale."""


ANSWER_TEMPLATES = {
    "object_counting": ("counting", ANSWER_PROMPT_COUNTING_EXT),
    "object_abs_distance": ("abs_distance", ANSWER_PROMPT_ABS_DISTANCE_EXT),
    "object_rel_distance": ("rel_distance", ANSWER_PROMPT_REL_DISTANCE_EXT),
    "object_size_estimation": ("size", ANSWER_PROMPT_SIZE_EXT),
    "room_size_estimation": ("room", ANSWER_PROMPT_ROOM_EXT),
    "route_planning": ("route", ANSWER_PROMPT_ROUTE_EXT),
    "obj_appearance_order": ("appearance", ANSWER_PROMPT_APPEARANCE_EXT),
    "object_rel_direction_easy": ("rel_direction", ANSWER_PROMPT_REL_DIRECTION_EXT),
    "object_rel_direction_medium": ("rel_direction", ANSWER_PROMPT_REL_DIRECTION_EXT),
    "object_rel_direction_hard": ("rel_direction", ANSWER_PROMPT_REL_DIRECTION_EXT),
}


def answer_template(question_type):
    """Exact question-type lookup: an unknown type must fail rather than borrow another template."""
    if question_type not in ANSWER_TEMPLATES:
        raise KeyError(
            f"no answer template for question type {question_type!r}; known types: "
            f"{sorted(ANSWER_TEMPLATES)}"
        )
    return ANSWER_TEMPLATES[question_type]


LETTER_QUESTION_TYPES = ("direction", "route", "appearance", "rel_distance")
OPTION_HEAD = re.compile(r"^([A-D])[.)]\)?\s*(.*)$")


def normalize_response(text):
    """Strip markdown emphasis and collapse whitespace before parsing an answer."""
    if not text:
        return ""
    text = text.replace("\u2212", "-")
    text = re.sub(r"[*`]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def option_listing(text):
    """True when the response spells the options out, so a bare letter is a listing, not a choice."""
    cue = re.search(r"\boptions?\b\s*(?:are|were|again|listed)?\s*:", text, flags=re.I)
    if not cue:
        return False
    return len(re.findall(r"(?<![A-Za-z0-9])([A-D])[.)]", text[cue.start():])) >= 2


def looks_answered(text):
    """Decide whether a response reads like a finished statement.

    Responses cut off mid-derivation end on a dangling operator, an unbalanced bracket, or a
    trailing word, so their last number is a step of the working rather than an answer.
    """
    if re.search(r"\d\.$", text):
        return False
    if re.search(r"[=≈×+\-/]\s*\$?\d[\d.,\s]*$", text):
        return False
    if re.search(r"""[.!?)}\]"'`]$""", text):
        return True
    if not re.search(r"\d$", text):
        return False
    return all(text.count(opener) == text.count(closer) for opener, closer in (("(", ")"), ("[", "]"), ("{", "}")))


def option_enumeration(prefix):
    """Two or more option letters just before a match mean the model is listing options, not answering."""
    return len(re.findall(r"(?<![A-Za-z0-9])([A-D])[.)]", prefix[-60:])) >= 2


def recover_letter(text, options):
    """Return the option letter when exactly one option body appears in the response.

    Models often answer multiple-choice questions in prose ("The table is to the front-left.")
    without writing the letter; the response still names exactly one option, so it is read as
    that option instead of being counted as unanswered.
    """
    if not text or not options:
        return None
    lowered = text.lower()
    hits = []
    for option in options:
        match = OPTION_HEAD.match(str(option).strip())
        if not match:
            continue
        body = match.group(2).strip().lower()
        if len(body) < 3:
            continue
        if re.search(r"(?<![a-z0-9])" + re.escape(body) + r"(?![a-z0-9])", lowered):
            hits.append(match.group(1))
    hits = sorted(set(hits))
    return hits[0] if len(hits) == 1 else None


def extract_answer(text, question_type, options=None):
    """Parse the final answer out of a response, returning (answer, rule).

    run_vsibench.extract_answer falls back to the first A-D character in the last 200 characters,
    which reads the "C" of "Correct Answer:" as the chosen option. This parser reads the last
    explicit answer statement instead, and reports which rule produced the answer. When no
    statement is found, a prose response that names exactly one option is read as that option.
    """
    clean = normalize_response(text)
    if not clean:
        return None, "empty"
    if any(keyword in question_type for keyword in LETTER_QUESTION_TYPES):
        hits = re.findall(
            r"(?:answer|option|choice)\s*(?:is)?\s*:?\s*\(?([A-D])\b", clean, flags=re.I
        )
        if hits:
            return hits[-1].upper(), "answer_marker"
        if not option_listing(clean):
            hits = [
                match.group(1)
                for match in re.finditer(r"(?<![A-Za-z0-9])([A-D])[.)]", clean)
                if not option_enumeration(clean[: match.start()])
            ]
            if hits:
                return hits[-1], "option_index"
            hits = re.findall(r"(?<![A-Za-z0-9])([A-D])(?![A-Za-z])", clean[-120:])
            if hits:
                return hits[-1], "tail_letter"
        recovered = recover_letter(clean, options)
        if recovered:
            return recovered, "option_text"
        return None, "none"
    if re.fullmatch(r"-?\d+(?:\.\d+)?", clean):
        return clean, "bare_number"
    hits = re.findall(r"answer\s*(?:is)?\s*:?\s*\$?\\?(?:approx\.?\s*)?(-?\d+(?:\.\d+)?)", clean, flags=re.I)
    if hits:
        return hits[-1], "answer_marker"
    hits = re.findall(r"-?\d+(?:\.\d+)?", clean)
    if hits and looks_answered(clean):
        return hits[-1], "last_number"
    return None, "none"

ALIASES = {"trash can": "trash bin", "television": "tv"}


def normalized_category(value):
    value = str(value).strip().lower().replace("_", " ")
    value = re.sub(r"\s+", " ", value)
    return ALIASES.get(value, value)


def load_category_vocabulary(path):
    return {
        normalized_category(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def required_categories(sample, vocabulary):
    found = {
        normalized_category(value)
        for value in sample.get("ext", {}).get("target_categories", [])
        if normalized_category(value) in vocabulary
    }
    text = sample["question"].lower().replace("_", " ")
    for category in sorted(vocabulary, key=len, reverse=True):
        pattern = r"(?<!\w)" + re.escape(category) + r"(?:s)?(?!\w)"
        if re.search(pattern, text):
            found.add(category)
    for option in sample.get("options") or []:
        value = normalized_category(re.sub(r"^[A-D][.\)-]\s*", "", option))
        if value in vocabulary:
            found.add(value)
    return sorted(found)


def is_cognitive_map(scene_json):
    return all(key in scene_json for key in ("top", "front", "side", "room"))


def cognitive_map_category_counts(scene_json):
    return {
        normalized_category(category): len(instances)
        for category, instances in scene_json["top"].items()
    }


def gate_scene_json(sample, scene_json, required, metadata=None, policy="on"):
    metadata = metadata or scene_json
    counts = (
        cognitive_map_category_counts(scene_json)
        if is_cognitive_map(scene_json)
        else scene_json["category_counts"]
    )
    present = {normalized_category(value) for value in counts}
    missing = sorted(set(required) - present)
    reasons = []
    if missing:
        reasons.append("missing_required_categories")
    question_type = sample["question_type"]
    if question_type == "object_counting":
        if not metadata.get("quality", {}).get("instance_coverage_reliable", False):
            reasons.append("instance_coverage_unreliable")
    if question_type in {"object_abs_distance", "object_size_estimation", "room_size_estimation"}:
        if not metadata.get("coordinate_system", {}).get("metric_reliable", False):
            reasons.append("metric_scale_unreliable")
    if question_type.startswith("object_rel_direction"):
        if not metadata.get("coordinate_system", {}).get("orientation_reliable", False):
            reasons.append("horizontal_orientation_unreliable")
    room_geometry_missing = (
        scene_json["room"].get("area_m2") is None
        if is_cognitive_map(scene_json)
        else scene_json["room"] is None
    )
    if question_type == "room_size_estimation" and room_geometry_missing:
        reasons.append("room_geometry_missing")

    applicable = not reasons
    relevance = {
        "json_applicable": applicable,
        "required_categories": required,
        "missing_categories": missing,
        "reasons": reasons,
        "gate_policy": policy,
        "gate_would_block": not applicable,
    }
    if policy == "off":
        relevance["json_applicable"] = True
        return scene_json, relevance
    if applicable:
        gated = scene_json
    elif is_cognitive_map(scene_json):
        gated = {
            "top": {},
            "front": {},
            "side": {},
            "room": {"width": 10, "depth": 10, "area_m2": None},
        }
    else:
        gated = {
            "scene_id": scene_json["scene_id"],
            "source_model": scene_json["source_model"],
            "source_variant": scene_json.get("source_variant"),
            "category_counts": scene_json["category_counts"],
            "quality": scene_json["quality"],
            "qa_relevance": relevance,
            "instruction": "The reconstruction is not applicable to this question. Ignore its geometry and answer from the video.",
        }
    return gated, relevance


def make_prompt(sample, scene_json):
    options_text = "\n".join(sample.get("options") or [])
    answer_prompt = answer_template(sample["question_type"])[1].format(
        question=sample["question"], options=options_text
    )
    compact_scene = json.dumps(scene_json, ensure_ascii=False, separators=(",", ":"))
    return f"{MAP_SCHEMA_NOTE}\nCognitive map JSON:\n{compact_scene}\n\n{answer_prompt}"


def run_scene(samples, scene_json, video_b64, source_model, vocabulary, model, sleep, policy,
              output=None, dry_run=False):
    rows = []
    for index, sample in enumerate(samples, 1):
        required = required_categories(sample, vocabulary)
        scene_payload, relevance = gate_scene_json(sample, scene_json, required, policy=policy)
        template_id = answer_template(sample["question_type"])[0]
        if dry_run:
            prompt = make_prompt(sample, scene_payload)
            print(
                f"{index}/{len(samples)} id={sample['id']} {sample['question_type']} "
                f"template={template_id} gate_would_block={relevance['gate_would_block']} "
                f"missing={relevance['missing_categories']} prompt_chars={len(prompt)}"
            )
            continue
        content = vsi.build_video_message(make_prompt(sample, scene_payload), video_b64)
        response = None
        for attempt in range(3):
            response = vsi.call_api(
                model,
                [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": content}],
                sleep_time=sleep,
            )
            if response:
                break
            print(f"empty response for id={sample['id']}, retry {attempt + 1}/2", flush=True)
        extracted, rule = extract_answer(
            response, sample["question_type"], sample.get("options")
        )
        correct = vsi.evaluate_answer(extracted, sample["ground_truth"])
        rows.append({
            "id": sample["id"],
            "scene_name": sample["scene_name"],
            "dataset": sample["dataset"],
            "source_model": source_model,
            "question_type": sample["question_type"],
            "question": sample["question"],
            "ground_truth": sample["ground_truth"],
            "answer_template": template_id,
            **relevance,
            "raw_response": response,
            "extracted_answer": extracted,
            "extraction_rule": rule,
            "correct": correct,
        })
        if output is not None:
            Path(output).write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{index}/{len(samples)} id={sample['id']} template={template_id} answer={extracted} correct={correct}")
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--samples",
        default=str(Path(__file__).resolve().parent / "vsi_four_system_200qa.json"),
    )
    parser.add_argument("--scene-json", required=True)
    parser.add_argument("--scene-metadata", help="quality/provenance sidecar emitted by scene_to_vlm_json.py")
    parser.add_argument("--video-root", required=True)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--source-model", help="system name recorded in the results")
    parser.add_argument("--model", default="gemini-3.5-flash")
    parser.add_argument("--output", required=True)
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--sleep", type=float, default=3.0)
    parser.add_argument("--gate-policy", choices=["on", "off"], default="off")
    parser.add_argument(
        "--category-list",
        default=str(Path(__file__).resolve().parent.parent / "docs" / "vsi_used_qa_asset_list.txt"),
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    samples_path = Path(args.samples)
    scene_path = Path(args.scene_json)
    samples = [
        row for row in json.loads(samples_path.read_text(encoding="utf-8"))
        if row["scene_name"] == args.scene_id
    ][: args.n]
    if not samples:
        raise ValueError(f"No samples found for {args.scene_id}")
    scene_json = json.loads(scene_path.read_text(encoding="utf-8"))
    metadata = (
        json.loads(Path(args.scene_metadata).read_text(encoding="utf-8"))
        if args.scene_metadata
        else None
    )
    recorded_scene_id = (metadata or scene_json).get("scene_id")
    if recorded_scene_id is not None and recorded_scene_id != args.scene_id:
        raise ValueError("scene JSON and requested scene id do not match")
    source_model = args.source_model or (metadata or scene_json).get("source_model", "unknown")
    vocabulary = load_category_vocabulary(args.category_list)

    dataset = samples[0]["dataset"]
    video_path = Path(args.video_root) / dataset / f"{args.scene_id}.mp4"
    if not video_path.is_file():
        raise FileNotFoundError(video_path)

    if args.dry_run:
        print(f"DRY RUN: {len(samples)} questions, source={source_model}, video={video_path}")
        run_scene(
            samples, scene_json, None, source_model, vocabulary, args.model, args.sleep,
            args.gate_policy, dry_run=True,
        )
        return

    video_b64 = vsi.load_video_base64(str(video_path))
    if not video_b64:
        raise RuntimeError(f"Could not load {video_path}")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = run_scene(
        samples, scene_json, video_b64, source_model, vocabulary, args.model, args.sleep,
        args.gate_policy, output=output,
    )
    correct = sum(row["correct"] for row in rows)
    print(f"result: {correct}/{len(rows)}; wrote {output}")


if __name__ == "__main__":
    main()
