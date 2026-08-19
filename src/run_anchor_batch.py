# -*- coding: utf-8 -*-
"""Run the anchor prompt variant over a list of sample indices.

Wrapper around try_prompt_variant.run_variant for small batch validation.
Auto-saves every 5 completed records and supports --resume.
"""
import argparse
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from tis_compare import (
    build_gt_map,
    compute_metrics,
    evaluate_answer,
    extract_answer,
    load_meta,
    mra,
)
from run_tis_compare import numeric_ok
from try_prompt_variant import VARIANTS, run_variant


def build_record(index, sample, variant, model_name, sleep):
    meta_scene = load_meta(sample['dataset']).get(sample['scene_name'], {})
    gt_map, matched = build_gt_map(sample, meta_scene)
    raw_map, error, parsed, ans = run_variant(sample, variant, model_name, sleep)
    if error:
        return {
            'sample_idx': index,
            'variant': variant,
            'scene': sample['scene_name'],
            'dataset': sample['dataset'],
            'question': sample['question'],
            'ground_truth': sample['ground_truth'],
            'raw_map': raw_map,
            'error': error,
        }
    raw_answer, answer = ans
    qt = sample['question_type']
    if qt in ('object_abs_distance', 'object_size_estimation', 'room_size_estimation'):
        is_correct = mra(answer, sample['ground_truth']) > 0
    elif qt == 'object_counting':
        is_correct = numeric_ok(answer, sample['ground_truth'], qt)
    else:
        is_correct = evaluate_answer(answer, sample['ground_truth'])
    metrics = compute_metrics(gt_map, parsed, 'threeview')
    return {
        'sample_idx': index,
        'variant': variant,
        'scene': sample['scene_name'],
        'dataset': sample['dataset'],
        'question_type': qt,
        'question': sample['question'],
        'ground_truth': sample['ground_truth'],
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


def main():
    parser = argparse.ArgumentParser(description='Anchor variant batch runner')
    parser.add_argument('--indices', type=str, required=True,
                        help='Comma-separated sample indices into vsi_subset_200.json')
    parser.add_argument('--variant', choices=list(VARIANTS), default='anchor')
    parser.add_argument('--model', type=str, default='gemini-3.5-flash')
    parser.add_argument('--sleep', type=float, default=1.0)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--output', required=True)
    parser.add_argument('--resume', type=str, default=None)
    args = parser.parse_args()

    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, 'vsi_subset_200.json'), encoding='utf-8') as f:
        samples = json.load(f)
    indices = [int(x) for x in args.indices.split(',') if x.strip()]

    results = []
    if args.resume and os.path.exists(args.resume):
        with open(args.resume, encoding='utf-8') as f:
            existing = json.load(f)
        results = [r for r in existing if '__summary__' not in r]
        done = {r['sample_idx'] for r in results}
        print('Resuming: %d records loaded' % len(results))
    else:
        done = set()

    lock = threading.Lock()
    completed = [len(done)]

    def process(index):
        if index in done:
            return index, None
        sample = samples[index]
        print('[%d] start %s %s %s' % (
            index, sample['dataset'], sample['scene_name'], sample['question_type']), flush=True)
        return index, build_record(index, sample, args.variant, args.model, args.sleep)

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futures = {ex.submit(process, i): i for i in indices}
        for fut in as_completed(futures):
            i, rec = fut.result()
            if rec is None:
                continue
            with lock:
                results = [r for r in results if r.get('sample_idx') != i]
                results.append(rec)
                completed[0] += 1
                if completed[0] % 5 == 0:
                    partial = args.output.replace('.json', '_partial_%d.json' % completed[0])
                    with open(partial, 'w', encoding='utf-8') as f:
                        json.dump(results, f, indent=2, ensure_ascii=False)
                    print('[Auto-save] %d -> %s' % (completed[0], partial), flush=True)

    ok = [r for r in results if not r.get('error')]
    correct = sum(1 for r in ok if r.get('correct'))
    results.append({'__summary__': {
        'variant': args.variant, 'total': len(ok), 'correct': correct,
        'accuracy_pct': round(100 * correct / len(ok), 1) if ok else None,
    }})
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print('Done. records=%d ok=%d correct=%d (%.0f%%)' % (
        len(results) - 1, len(ok), correct, 100 * correct / len(ok) if ok else 0))


if __name__ == '__main__':
    main()
