# -*- coding: utf-8 -*-
"""Single-sample prompt iteration for a failure case in the 200 run.

Loads one sample from vsi_subset_200.json, runs the three-view single-pass
prompt with an optional appended instruction, then answers in shared mode and
writes the record with GT map, predicted map, metrics and QA correctness.
"""
import argparse
import json
import os
import sys

from tis_compare import (
    SYSTEM_PROMPT,
    VIDEO_CACHE_DIR,
    build_gt_map,
    build_video_message,
    call_api,
    compute_metrics,
    evaluate_answer,
    extract_answer,
    extract_categories,
    load_meta,
    load_video_base64,
    mra,
    parse_map,
)
from run_tis_compare import answer_template, numeric_ok, options_text
from tis_prompts import TIS_THREE_VIEW_PROMPT

COUNT_ALL = (
    '\n\nAdditional instruction: Every category in the focus list must appear in '
    'your JSON. If you cannot see an instance clearly, estimate its most likely '
    'location from the video instead of omitting it.'
)
ANCHOR_CHECK = (
    '\n\nAdditional instruction: After estimating all coordinates, take the '
    'reference object mentioned in the question as an anchor. Re-verify the '
    'relative near/far order and left/right layout of every candidate object '
    'against that anchor. Fix any coordinate that contradicts the video.'
)
VARIANTS = {
    'countall': COUNT_ALL,
    'anchor': ANCHOR_CHECK,
    'both': COUNT_ALL + ANCHOR_CHECK,
}


def run_variant(sample, variant, model_name, sleep):
    cats = extract_categories(sample)
    cats_text = ', '.join(cats) if cats else 'all objects visible in the scene'
    video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
    video_b64 = load_video_base64(video_path)
    prompt = TIS_THREE_VIEW_PROMPT.format(categories_of_interest=cats_text)
    prompt += VARIANTS[variant]
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': build_video_message(prompt, video_b64)}]
    raw_map = call_api(model_name, messages, sleep_time=sleep)
    if not raw_map:
        return None, 'MAP_API_FAIL', None, None
    parsed = parse_map(raw_map, 'threeview')
    if parsed is None:
        return raw_map, 'MAP_PARSE_FAIL', None, None
    messages.append({'role': 'assistant', 'content': raw_map})
    template = answer_template(sample['question_type'])
    opts = options_text(sample)
    preamble = (
        'Earlier you built a cognitive map of this room from the video. '
        'Based on the cognitive map you built above in our conversation, answer the question.\n'
    )
    messages.append({'role': 'user', 'content': preamble + template.format(
        question=sample['question'], options=opts)})
    raw_answer = call_api(model_name, messages, sleep_time=sleep)
    if not raw_answer:
        return raw_map, 'ANSWER_API_FAIL', parsed, None
    answer = extract_answer(raw_answer, sample['question_type'])
    return raw_map, None, parsed, (raw_answer, answer)


def main():
    parser = argparse.ArgumentParser(description='Single-sample prompt iteration')
    parser.add_argument('--sample-index', type=int, default=108)
    parser.add_argument('--variant', choices=list(VARIANTS), default='both')
    parser.add_argument('--model', type=str, default='gemini-3.5-flash')
    parser.add_argument('--sleep', type=float, default=1.0)
    parser.add_argument('--output', default='results_prompt_iter_108.json')
    args = parser.parse_args()

    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, 'vsi_subset_200.json'), encoding='utf-8') as f:
        samples = json.load(f)
    sample = samples[args.sample_index]
    print('[%d] %s %s %s' % (args.sample_index, sample['dataset'],
                             sample['scene_name'], sample['question_type']), flush=True)

    meta_scene = load_meta(sample['dataset']).get(sample['scene_name'], {})
    gt_map, matched = build_gt_map(sample, meta_scene)
    raw_map, error, parsed, ans = run_variant(sample, args.variant, args.model, args.sleep)
    if error:
        rec = {'sample_idx': args.sample_index, 'variant': args.variant,
               'scene': sample['scene_name'], 'dataset': sample['dataset'],
               'question': sample['question'], 'ground_truth': sample['ground_truth'],
               'raw_map': raw_map, 'error': error}
    else:
        raw_answer, answer = ans
        qt = sample['question_type']
        if qt in ('object_abs_distance', 'object_size_estimation', 'room_size_estimation'):
            is_correct = mra(answer, sample['ground_truth']) > 0
        elif qt == 'object_counting':
            is_correct = numeric_ok(answer, sample['ground_truth'], qt)
        else:
            is_correct = evaluate_answer(answer, sample['ground_truth'])
        metrics = compute_metrics(gt_map, parsed, 'threeview')
        rec = {
            'sample_idx': args.sample_index,
            'variant': args.variant,
            'scene': sample['scene_name'],
            'dataset': sample['dataset'],
            'question_type': qt,
            'question': sample['question'],
            'ground_truth': sample['ground_truth'],
            'categories': sample.get('categories'),
            'categories_matched': sorted(set(matched.values())) if matched else [],
            'gt_map': gt_map,
            'raw_map': raw_map,
            'pred_map': parsed,
            'map_metrics': metrics,
            'raw_answer': raw_answer,
            'extracted_answer': answer,
            'correct': is_correct,
            'error': None,
        }
        print('[%s] answer=%s correct=%s missed=%s pairs=%s/%s' % (
            args.variant, answer, is_correct,
            metrics.get('missed_instances'), metrics.get('pairs_correct'), metrics.get('pairs')), flush=True)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(rec, f, indent=2, ensure_ascii=False)
    print('Done. Output: %s' % args.output)


if __name__ == '__main__':
    main()
