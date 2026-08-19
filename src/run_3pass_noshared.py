# -*- coding: utf-8 -*-
"""Answer-only noshared control for the threeview_3pass arm.

Reuses the exact 3-pass maps already stored in a run_tis_compare result file
(e.g. src/results_tis_200.json) and only re-runs the answer stage in a fresh
conversation. This keeps shared vs noshared comparable: the only difference is
whether the answer conversation carries the map-building memory.
"""
import argparse
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from run_tis_compare import answer_template, numeric_ok, options_text
from tis_compare import (
    SYSTEM_PROMPT,
    call_api,
    error_tags,
    evaluate_answer,
    extract_answer,
    reconcile_views,
)


def load_source_maps(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    out = {}
    for r in data:
        if r.get('arm') != 'threeview_3pass' or r.get('error'):
            continue
        key = (r['dataset'], r['scene'], r['question'])
        out.setdefault(key, []).append(r)
    return out


def run_answer(sample, src, model_name, sleep, dry_run):
    qtype = sample['question_type']
    template = answer_template(qtype)
    opts = options_text(sample)
    reconciled = reconcile_views(src['pred_map'])
    preamble = (
        'You are given a cognitive map of a room:\n\n%s\n\n'
        'Based on the cognitive map above, answer the question.\n'
    ) % json.dumps(reconciled, ensure_ascii=False)
    text = preamble + template.format(question=sample['question'], options=opts)
    if dry_run:
        raw_answer = str(sample['ground_truth']) if 'abs_distance' in qtype else 'A'
    else:
        raw_answer = call_api(model_name, [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': text},
        ], sleep_time=sleep)
    if not raw_answer:
        return raw_answer, 'ANSWER_API_FAIL', None
    answer = extract_answer(raw_answer, qtype)
    return raw_answer, None, answer


def make_record(i, sample, src, raw_answer, answer, is_correct, error):
    qtype = sample['question_type']
    if error:
        return {
            'sample_idx': i,
            'arm': 'threeview_3pass',
            'mode': 'noshared',
            'answer_only': True,
            'scene': sample['scene_name'],
            'dataset': sample['dataset'],
            'question_type': qtype,
            'question': sample['question'],
            'ground_truth': sample['ground_truth'],
            'raw_answer': raw_answer,
            'correct': False,
            'error': error,
        }
    tags = error_tags(src['map_metrics'], 'threeview') if src.get('map_metrics') else ['MAP_PARSE_FAIL']
    if not is_correct:
        tags.append('QA_wrong')
    elif not [t for t in tags if t.startswith(('A1', 'A2', 'B3', 'B4', 'B5', 'C6', 'C7', 'C8'))]:
        tags.append('QA_map_clean')
    return {
        'sample_idx': i,
        'arm': 'threeview_3pass',
        'mode': 'noshared',
        'answer_only': True,
        'map_source_idx': src['sample_idx'],
        'scene': src['scene'],
        'dataset': src['dataset'],
        'question_type': src['question_type'],
        'question': src['question'],
        'ground_truth': src['ground_truth'],
        'categories': src.get('categories'),
        'categories_matched': src.get('categories_matched'),
        'gt_map': src['gt_map'],
        'raw_map': json.dumps(reconcile_views(src['pred_map']), ensure_ascii=False),
        'pred_map': src['pred_map'],
        'map_metrics': src['map_metrics'],
        'raw_answer': raw_answer,
        'extracted_answer': answer,
        'correct': is_correct,
        'error': None,
        'error_tags': tags,
    }


def main():
    parser = argparse.ArgumentParser(description='3-pass noshared answer-only control')
    parser.add_argument('--samples', type=str, default='vsi_debate_strat_20.json')
    parser.add_argument('--n', type=int, default=20)
    parser.add_argument('--map-source', type=str, default='results_tis_200.json')
    parser.add_argument('--output', default='results_tis_3pass_noshared_strat20.json')
    parser.add_argument('--model', type=str, default='gemini-3.5-flash')
    parser.add_argument('--sleep', type=float, default=3.0)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--resume', type=str, default=None)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, args.samples), encoding='utf-8') as f:
        samples = json.load(f)
    test_samples = samples[:args.n]
    source_maps = load_source_maps(os.path.join(base, args.map_source))

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

    def process(i, sample):
        if i in done:
            return i, None
        key = (sample['dataset'], sample['scene_name'], sample['question'])
        src_list = source_maps.get(key)
        if not src_list:
            return i, make_record(i, sample, None, None, None, False, 'NO_SOURCE_MAP')
        src = src_list[0]
        raw_answer, error, answer = run_answer(sample, src, args.model, args.sleep, args.dry_run)
        if error:
            return i, make_record(i, sample, src, raw_answer, None, False, error)
        qtype = sample['question_type']
        if any(k in qtype for k in ('counting', 'size', 'room')):
            is_correct = numeric_ok(answer, sample['ground_truth'], qtype)
        else:
            is_correct = evaluate_answer(answer, sample['ground_truth'])
        rec = make_record(i, sample, src, raw_answer, answer, is_correct, None)
        if args.verbose:
            print('[%d] answer=%s correct=%s' % (i + 1, answer, is_correct), flush=True)
        return i, rec

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futures = {ex.submit(process, i, sample): i for i, sample in enumerate(test_samples)}
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
    summary = {'__summary__': {
        'arm': 'threeview_3pass', 'mode': 'noshared', 'total': len(ok),
        'correct': correct,
        'accuracy_pct': round(100 * correct / len(ok), 1) if ok else None,
    }}
    results.append(summary)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print('Done. records=%d ok=%d correct=%d (%.0f%%)' % (
        len(results) - 1, len(ok), correct, 100 * correct / len(ok) if ok else 0))


if __name__ == '__main__':
    main()
