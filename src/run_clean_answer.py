# -*- coding: utf-8 -*-
"""Unified noshared answer stage for any existing results file.

Loads records with pred_map/gt_map and re-answers every sample in a fresh
conversation using the SAME map text format and preamble, so answer-stage
memory/video/format differences between arms are removed. The original records
are copied and only raw_answer / extracted_answer / correct are replaced.
"""
import argparse
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from tis_compare import (
    SYSTEM_PROMPT,
    call_api,
    evaluate_answer,
    extract_answer,
    mra,
)
from run_tis_compare import answer_template, numeric_ok, options_text

MAP_PREAMBLE = (
    'You are given a three-view cognitive map of a room:\n\n%s\n\n'
    'Based on the cognitive map above, answer the question.\n'
)


def unified_map_text(pred):
    return json.dumps({
        'top': pred.get('top', {}),
        'front': pred.get('front', {}),
        'side': pred.get('side', {}),
        'sizes': pred.get('sizes', {}),
        'room': pred.get('room'),
        'appearance_order': pred.get('appearance_order'),
        'route_action': pred.get('route_action'),
    }, ensure_ascii=False)


def is_correct_ans(answer, sample):
    qt = sample['question_type']
    if qt in ('object_abs_distance', 'object_size_estimation', 'room_size_estimation'):
        return mra(answer, sample['ground_truth']) > 0
    if qt == 'object_counting':
        return numeric_ok(answer, sample['ground_truth'], qt)
    return evaluate_answer(answer, sample['ground_truth'])


def answer_one(text, model_name, sleep, dry_run=False):
    if dry_run:
        return 'ANSWER: %s' % text, None
    raw = call_api(model_name, [{'role': 'system', 'content': SYSTEM_PROMPT},
                                {'role': 'user', 'content': text}], sleep_time=sleep)
    return raw, None


def process_record(i, sample, model_name, sleep, dry_run):
    pred = sample.get('pred_map') or sample.get('fused_map')
    if not pred:
        return i, None
    opts = options_text(sample)
    template = answer_template(sample['question_type'])
    text = MAP_PREAMBLE % unified_map_text(pred) + template.format(
        question=sample['question'], options=opts)
    raw, _ = answer_one(text, model_name, sleep, dry_run=dry_run)
    if not raw:
        rec = dict(sample)
        rec['error'] = 'ANSWER_API_FAIL'
        return i, rec
    ans = extract_answer(raw, sample['question_type'])
    if ans is None and not dry_run:
        retry_text = ('Reply with ONLY the final answer as a single letter or number.\nQuestion: %s\n%s' %
                      (sample['question'], opts))
        raw2, _ = answer_one(retry_text, model_name, sleep)
        ans2 = extract_answer(raw2, sample['question_type']) if raw2 else None
        if ans2 is not None:
            raw, ans = raw2, ans2
    rec = dict(sample)
    rec['raw_answer'] = raw
    rec['extracted_answer'] = ans
    rec['correct'] = is_correct_ans(ans, sample)
    rec['clean_answer'] = True
    rec['error'] = None
    return i, rec


def main():
    parser = argparse.ArgumentParser(description='Unified noshared answer re-run')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--model', type=str, default='gemini-3.5-flash')
    parser.add_argument('--sleep', type=float, default=1.0)
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--resume', type=str, default=None)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    with open(args.input, encoding='utf-8') as f:
        data = json.load(f)
    recs = [r for r in data if '__summary__' not in r and not r.get('error')]

    results = []
    if args.resume and os.path.exists(args.resume):
        with open(args.resume, encoding='utf-8') as f:
            existing = json.load(f)
        results = [r for r in existing if '__summary__' not in r]
        done = {r['sample_idx'] for r in results if not r.get('error')}
        print('Resuming: %d records loaded' % len(results))
    else:
        done = set()

    lock = threading.Lock()
    completed = [len(done)]

    def process(i, rec):
        if i in done:
            return i, None
        return process_record(i, rec, args.model, args.sleep, args.dry_run)

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futures = {ex.submit(process, i, rec): i for i, rec in enumerate(recs)}
        for fut in as_completed(futures):
            i, rec = fut.result()
            if rec is None:
                continue
            with lock:
                rid = rec.get('sample_idx')
                results = [r for r in results if r.get('sample_idx') != rid]
                results.append(rec)
                completed[0] += 1
                if completed[0] % 5 == 0:
                    partial = args.output.replace('.json', '_partial_%d.json' % completed[0])
                    with open(partial, 'w', encoding='utf-8') as f:
                        json.dump(results, f, indent=2, ensure_ascii=False)
                    print('[Auto-save] %d -> %s' % (completed[0], partial), flush=True)

    ok = [r for r in results if not r.get('error')]
    correct = sum(1 for r in ok if r.get('correct'))
    print('Done. records=%d ok=%d correct=%d (%.0f%%)' % (
        len(results), len(ok), correct, 100 * correct / len(ok) if ok else 0))
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
