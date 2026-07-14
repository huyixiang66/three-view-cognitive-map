"""Three-View Cognitive Map Debug Pipeline."""

import json
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prompts import build_three_view_prompt, build_answer_prompt, build_baseline_prompt


def load_samples(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_gemini_api(api_key):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        resp = model.generate_content("Say hello in one word.")
        print(f"Gemini API OK: {resp.text.strip()}")
        return True
    except ImportError:
        print("ERROR: google-generativeai not installed. Run: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"ERROR: Gemini API failed: {e}")
        return False


def run_single_step(model, scene_desc, question, options, ground_truth):
    prompt = build_baseline_prompt(question, options)
    resp = model.generate_content(prompt)
    return resp.text.strip()


def strip_backticks(text):
    bt = chr(96)
    return text.strip().replace(bt*3+DQ, DQ).replace(bt*3, DQ).strip()


def run_three_step_with_map(model, scene_desc, question, options, ground_truth):
    map_prompt = build_three_view_prompt(scene_desc)
    map_resp = model.generate_content(map_prompt)
    cognitive_map_text = strip_backticks(map_resp.text)
    try:
        cognitive_map = json.loads(cognitive_map_text)
    except json.JSONDecodeError:
        return None, cognitive_map_text, "JSON_PARSE_ERROR"
    answer_prompt = build_answer_prompt(question, options, cognitive_map_text)
    answer_resp = model.generate_content(answer_prompt)
    answer = answer_resp.text.strip()
    return answer, cognitive_map_text, None


def run_shared_memory(model, scene_desc, question, options, ground_truth):
    map_prompt = build_three_view_prompt(scene_desc)
    map_resp = model.generate_content(map_prompt)
    cognitive_map_text = strip_backticks(map_resp.text)
    prompt = "Here is the cognitive map of the scene:\n" + cognitive_map_text
    prompt += "\n\nNow answer the question based on this cognitive map:\n" + question
    if options:
        prompt += "\nOptions: " + str(options)
        prompt += "\nAnswer with the option letter directly."
    else:
        prompt += "\nAnswer with a single number."
    resp = model.generate_content(prompt)
    return resp.text.strip(), cognitive_map_text


def evaluate_answer(predicted, ground_truth, question_type):
    if not predicted:
        return False, "NO_OUTPUT"
    predicted = predicted.strip().upper()
    ground_truth = ground_truth.strip().upper()
    if predicted == ground_truth or predicted.startswith(ground_truth):
        return True, "MATCH"
    if question_type in ["object_abs_distance", "object_rel_distance", "object_size_estimation", "room_size_estimation"]:
        try:
            pred_num = float(predicted.split()[0])
            gt_num = float(ground_truth)
            if gt_num > 0:
                ratio = abs(pred_num - gt_num) / gt_num
                if ratio <= 0.3:
                    return True, "CLOSE"
        except (ValueError, IndexError):
            pass
    return False, "MISMATCH"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--samples", default="vsi_subset_50.json")
    parser.add_argument("--mode", choices=["single", "threestep", "share_memory"], default="threestep")
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if not test_gemini_api(args.api_key):
        sys.exit(1)
    import google.generativeai as genai
    genai.configure(api_key=args.api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    samples = load_samples(args.samples)
    test_samples = samples[:args.n]
    print(f"\nTesting {len(test_samples)} samples in {args.mode} mode")
    print("=" * 60)
    results = []
    correct = 0
    for i, s in enumerate(test_samples):
        scene = s["scene_name"]
        qtype = s["question_type"]
        question = s["question"]
        options = s["options"]
        gt = s["ground_truth"]
        print(f"\n--- Sample {i+1}/{len(test_samples)} ---")
        print(f"Type: {qtype}")
        print(f"Q: {question[:80]}...")
        print(f"GT: {gt}")
        if args.mode == "single":
            predicted = run_single_step(model, scene, question, options, gt)
            cognitive_map = None
        elif args.mode == "threestep":
            predicted, cognitive_map, err = run_three_step_with_map(model, scene, question, options, gt)
        elif args.mode == "share_memory":
            predicted, cognitive_map = run_shared_memory(model, scene, question, options, gt)
            err = None
        if err == "JSON_PARSE_ERROR":
            print("Status: JSON PARSE ERROR")
            print(f"Map: {cognitive_map[:200]}")
            results.append({"sample": i, "predicted": None, "gt": gt, "correct": False, "error": "JSON_PARSE"})
            continue
        if cognitive_map and args.verbose:
            print(f"Cognitive Map: {cognitive_map[:300]}...")
        if predicted:
            is_correct, match_type = evaluate_answer(predicted, gt, qtype)
            print(f"Predicted: {predicted}")
            status = "CORRECT" if is_correct else "WRONG"
            print(f"Status: {status} ({match_type})")
            if is_correct:
                correct += 1
            results.append({"sample": i, "predicted": predicted, "gt": gt, "correct": is_correct, "match": match_type})
        else:
            print("Status: NO OUTPUT")
            results.append({"sample": i, "predicted": None, "gt": gt, "correct": False, "error": "NO_OUTPUT"})
    print(f"\n" + "=" * 60)
    acc = correct / len(test_samples) * 100 if test_samples else 0
    print(f"RESULTS: {correct}/{len(test_samples)} correct ({acc:.1f}%)")
    print(f"Mode: {args.mode}")
    out_path = f"results_{args.mode}_{args.n}samples.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"results": results, "accuracy": correct / len(test_samples) if test_samples else 0, "mode": args.mode, "total": len(test_samples)}, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {out_path}")


if __name__ == '__main__':
    main()