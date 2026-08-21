"""Run the TIS baseline vs three-view controlled comparison.

Usage examples:
  python run_tis_compare.py --arm both --mode shared --output results_tis_compare.json
  python run_tis_compare.py --arm baseline --mode shared --output results_tis_baseline.json
  python run_tis_compare.py --arm threeview --mode shared --output results_tis_threeview.json
  python run_tis_compare.py --arm threeview_3pass --mode shared --output results_tis_threeview_3pass.json

Progress is auto-saved every 5 samples as {output}_partial_{N}.json and can be
resumed with --resume.
"""
import argparse
import json
import os
import sys
import glob
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

from prompts_3pass import (
    ANSWER_PROMPT_ABS_DISTANCE,
    ANSWER_PROMPT_REL_DISTANCE,
    ANSWER_PROMPT_REL_DIRECTION,
)
from tis_compare import (
    SYSTEM_PROMPT,
    VIDEO_CACHE_DIR,
    build_gt_map,
    build_video_message,
    call_api,
    compute_metrics,
    error_tags,
    evaluate_answer,
    extract_answer,
    extract_categories,
    extract_json,
    load_meta,
    load_video_base64,
    mra,
    normalize_view,
    parse_map,
    normalize_sizes,
    parse_counts,
    reconcile_views,
    legacy_cogmap_objects,
)
from tis_prompts import (
    TIS_FRONT_VIEW_PASS2_PROMPT,
    TIS_COUNT_PROMPT,
    TIS_THREE_VIEW_WITH_COUNTS_PROMPT,
    TIS_SIDE_VIEW_PASS3_PROMPT,
    TIS_THREE_VIEW_PROMPT,
    TIS_TOP_VIEW_PROMPT,
    TIS_ROOM_SUFFIX,
    ANSWER_PROMPT_COUNTING,
    ANSWER_PROMPT_SIZE,
    ANSWER_PROMPT_ROOM,
    ANSWER_PROMPT_ROUTE,
    ANSWER_PROMPT_APPEARANCE,
)


def answer_template(question_type):
    if 'abs_distance' in question_type:
        return ANSWER_PROMPT_ABS_DISTANCE
    if 'rel_distance' in question_type:
        return ANSWER_PROMPT_REL_DISTANCE
    if 'counting' in question_type:
        return ANSWER_PROMPT_COUNTING
    if 'size' in question_type:
        return ANSWER_PROMPT_SIZE
    if 'room' in question_type:
        return ANSWER_PROMPT_ROOM
    if 'route' in question_type:
        return ANSWER_PROMPT_ROUTE
    if 'appearance' in question_type:
        return ANSWER_PROMPT_APPEARANCE
    return ANSWER_PROMPT_REL_DIRECTION


def numeric_ok(answer, gt, qtype):
    try:
        a = float(answer)
        g = float(gt)
    except (TypeError, ValueError):
        return False
    if 'counting' in qtype:
        return abs(a - g) < 1e-6
    if g == 0:
        return False
    r = a / g
    return 0.5 <= r <= 2.0


def options_text(sample):
    opts = sample.get('options') or []
    return '\n'.join(str(o) for o in opts)


def map_prompt(arm, categories):
    cats = ', '.join(categories)
    if arm == 'baseline':
        return TIS_TOP_VIEW_PROMPT.format(categories_of_interest=cats) + TIS_ROOM_SUFFIX
    return TIS_THREE_VIEW_PROMPT.format(categories_of_interest=cats)


def run_arm(sample, arm, mode, model_name, sleep, dry_run):
    scene = sample['scene_name']
    dataset = sample['dataset']
    qtype = sample['question_type']
    question = sample['question']
    categories = extract_categories(sample)

    video_path = os.path.join(VIDEO_CACHE_DIR, dataset, scene + '.mp4')
    video_b64 = load_video_base64(video_path)
    if video_b64 is None and not dry_run:
        return None, None, 'NO_VIDEO', categories, None

    if dry_run:
        meta_scene = load_meta(dataset).get(scene, {})
        gt_map, _ = build_gt_map(sample, meta_scene)
        if arm == 'baseline':
            raw_map = json.dumps(gt_map['top'], ensure_ascii=False)
        else:
            raw_map = json.dumps(gt_map, ensure_ascii=False)
        if 'abs_distance' in qtype:
            raw_answer = str(sample['ground_truth'])
        else:
            raw_answer = 'A'
        parsed = parse_map(raw_map, arm)
        return raw_map, raw_answer, None, categories, parsed

    cats = ', '.join(categories)
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]

    if arm == 'threeview_3pass':
        messages.append({'role': 'user', 'content': build_video_message(
            TIS_TOP_VIEW_PROMPT.format(categories_of_interest=cats) + TIS_ROOM_SUFFIX, video_b64)})
        raw_top = call_api(model_name, messages, sleep_time=sleep)
        if not raw_top:
            return raw_top, None, 'MAP_API_FAIL', categories, None
        messages.append({'role': 'assistant', 'content': raw_top})

        messages.append({'role': 'user', 'content': TIS_FRONT_VIEW_PASS2_PROMPT.format(
            top_view_result=raw_top, categories_of_interest=cats)})
        raw_front = call_api(model_name, messages, sleep_time=sleep)
        if not raw_front:
            return raw_front, None, 'MAP_API_FAIL', categories, None
        messages.append({'role': 'assistant', 'content': raw_front})

        messages.append({'role': 'user', 'content': TIS_SIDE_VIEW_PASS3_PROMPT.format(
            top_view_result=raw_top, front_view_result=raw_front,
            categories_of_interest=cats)})
        raw_side = call_api(model_name, messages, sleep_time=sleep)
        if not raw_side:
            return raw_side, None, 'MAP_API_FAIL', categories, None
        messages.append({'role': 'assistant', 'content': raw_side})

        _top_data = extract_json(raw_top)
        _room = None
        if isinstance(_top_data, dict) and isinstance(_top_data.get('room'), dict):
            try:
                _room = float(_top_data['room'].get('area_m2'))
            except (TypeError, ValueError):
                _room = None

        parsed = {
            'top': normalize_view(extract_json(raw_top), 'top'),
            'front': normalize_view(extract_json(raw_front), 'front'),
            'side': normalize_view(extract_json(raw_side), 'side'),
            'sizes': {
                'top': normalize_sizes(extract_json(raw_top), 'top'),
                'front': normalize_sizes(extract_json(raw_front), 'front'),
                'side': normalize_sizes(extract_json(raw_side), 'side'),
            },
            'room': _room,
        }
        raw_map = json.dumps(parsed, ensure_ascii=False)
    elif arm == 'threeview_2stage':
        messages.append({'role': 'user', 'content': build_video_message(
            TIS_COUNT_PROMPT.format(categories_of_interest=cats), video_b64)})
        raw_counts = call_api(model_name, messages, sleep_time=sleep)
        if not raw_counts:
            return raw_counts, None, 'MAP_API_FAIL', categories, None
        messages.append({'role': 'assistant', 'content': raw_counts})
        counts = parse_counts(raw_counts)
        counts_text = raw_counts if counts is None else json.dumps(counts, ensure_ascii=False)
        messages.append({'role': 'user', 'content': TIS_THREE_VIEW_WITH_COUNTS_PROMPT.format(
            categories_of_interest=cats, instance_counts=counts_text)})
        raw_map = call_api(model_name, messages, sleep_time=sleep)
        if not raw_map:
            return raw_map, None, 'MAP_API_FAIL', categories, None
        messages.append({'role': 'assistant', 'content': raw_map})
        parsed = parse_map(raw_map, 'threeview')
        raw_map = json.dumps({'counts': counts, 'map': parsed}, ensure_ascii=False)
    else:
        prompt = map_prompt(arm, categories)
        messages.append({'role': 'user', 'content': build_video_message(prompt, video_b64)})
        raw_map = call_api(model_name, messages, sleep_time=sleep)
        if not raw_map:
            return raw_map, None, 'MAP_API_FAIL', categories, None
        messages.append({'role': 'assistant', 'content': raw_map})
        parsed = parse_map(raw_map, arm)

    template = answer_template(qtype)
    opts = options_text(sample)
    if mode == 'shared':
        if arm == 'threeview_3pass':
            reconciled = reconcile_views(parsed)
            preamble = (
                'Earlier you built a three-view cognitive map of this room from the video. '
                'Here is the unified map (coordinates averaged across views where they conflicted):\n\n'
                '%s\n\n'
                'Based on the unified map, answer the question.\n'
            ) % json.dumps(reconciled, ensure_ascii=False)
        else:
            preamble = (
                'Earlier you built a cognitive map of this room from the video. '
                'Based on the cognitive map you built above in our conversation, answer the question.\n'
            )
        messages.append({'role': 'user', 'content': preamble + template.format(
            question=question, options=opts)})
        raw_answer = call_api(model_name, messages, sleep_time=sleep)
    else:
        preamble = (
            'You are given the video of a room and a cognitive map of the same room:\n\n%s\n\n'
            'Based on the video and the cognitive map, answer the question.\n'
        ) % (json.dumps(reconcile_views(parsed), ensure_ascii=False) if arm == 'threeview_3pass' else raw_map)
        new_messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
        answer_text = preamble + template.format(question=question, options=opts)
        new_messages.append({'role': 'user', 'content': build_video_message(answer_text, video_b64)})
        raw_answer = call_api(model_name, new_messages, sleep_time=sleep)
    if not raw_answer:
        return raw_map, raw_answer, 'ANSWER_API_FAIL', categories, parsed

    return raw_map, raw_answer, None, categories, parsed


def main():
    parser = argparse.ArgumentParser(description='TIS baseline vs three-view comparison')
    parser.add_argument('--arm', choices=['baseline', 'threeview', 'threeview_3pass', 'threeview_2stage', 'both', 'all'], default='both')
    parser.add_argument('--mode', choices=['shared', 'noshared'], default='shared')
    parser.add_argument('--model', type=str, default='gemini-3.5-flash')
    parser.add_argument('--samples', type=str, default='vsi_subset_50.json')
    parser.add_argument('--output', default='results_tis_compare.json')
    parser.add_argument('--n', type=int, default=50)
    parser.add_argument('--sleep', type=float, default=3.0)
    parser.add_argument('--workers', type=int, default=1, help='Number of parallel sample workers')
    parser.add_argument('--resume', type=str, default=None)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--max-consecutive-fails', type=int, default=15)
    parser.add_argument('--max-fail-rate', type=float, default=0.6)
    args = parser.parse_args()

    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(line_buffering=True)

    if args.arm == 'both':
        arms = ['baseline', 'threeview']
    elif args.arm == 'all':
        arms = ['baseline', 'threeview', 'threeview_3pass']
    else:
        arms = [args.arm]
    samples_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.samples)
    with open(samples_path, 'r', encoding='utf-8') as f:
        samples = json.load(f)
    test_samples = samples[:args.n]

    results = []
    resume_path = args.resume
    if resume_path and not os.path.exists(resume_path):
        base = args.output.replace('.json', '')
        cands = sorted(glob.glob(base + '_partial_*.json'),
                       key=lambda p: int(p.rsplit('_', 1)[-1].split('.')[0]))
        if cands:
            resume_path = cands[-1]
    if resume_path and os.path.exists(resume_path):
        with open(resume_path, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        results = [e for e in existing if '__summary__' not in e]
        done = {(e['sample_idx'], e['arm']) for e in results if not e.get('error')}
        print('Resuming %d records from %s' % (len(results), resume_path))
    else:
        done = set()

    print('Samples: %d | arms: %s | mode: %s | dry-run: %s' % (
        len(test_samples), arms, args.mode, args.dry_run))

    lock = threading.Lock()
    completed = [len({r.get('sample_idx') for r in results})]
    fail_streak = 0
    recent = deque(maxlen=20)
    stop_reason = None

    def process(i, sample):
        print('[%d/%d] start %s %s %s' % (
            i + 1, len(test_samples), sample['dataset'], sample['scene_name'],
            sample['question_type']), flush=True)
        meta_scene = load_meta(sample['dataset']).get(sample['scene_name'], {})
        gt_map, matched = build_gt_map(sample, meta_scene)
        out = []
        for arm in arms:
            key = (i, arm)
            if key in done:
                continue
            raw_map, raw_answer, error, categories, parsed = run_arm(
                sample, arm, args.mode, args.model, args.sleep, args.dry_run,
            )
            record = {
                'sample_idx': i,
                'mode': args.mode,
                'arm': arm,
                'scene': sample['scene_name'],
                'dataset': sample['dataset'],
                'question_type': sample['question_type'],
                'question': sample['question'],
                'ground_truth': sample['ground_truth'],
                'categories': categories,
                'categories_matched': sorted(set(matched.values())) if matched else [],
                'gt_map': gt_map,
                'raw_map': raw_map,
                'raw_answer': raw_answer,
                'error': error,
                'cogmap_objects': legacy_cogmap_objects(parsed) if parsed else [],
                'api_calls': 4 if arm == 'threeview_3pass' else 3 if arm == 'threeview_2stage' else 2,
            }
            metric_arm = 'threeview' if arm != 'baseline' else 'baseline'
            if error:
                record['correct'] = False
                record['pred_map'] = None
                record['map_metrics'] = None
                record['error_tags'] = ['RUN_ERROR_' + error]
                out.append((key, record, '[%d][%s] SKIP: %s' % (i + 1, arm, error)))
            else:
                answer = extract_answer(raw_answer, sample['question_type'])
                qtype = sample['question_type']
                if any(k in qtype for k in ('counting', 'size', 'room')):
                    is_correct = numeric_ok(answer, sample['ground_truth'], qtype)
                else:
                    is_correct = evaluate_answer(answer, sample['ground_truth'])
                metrics = compute_metrics(gt_map, parsed, metric_arm) if parsed else None
                tags = error_tags(metrics, metric_arm) if metrics else ['MAP_PARSE_FAIL']
                if parsed is None:
                    tags.append('MAP_PARSE_FAIL')
                if not is_correct:
                    tags.append('QA_wrong')
                elif metrics and not [t for t in tags if t.startswith(('A1', 'A2', 'B3', 'B4', 'B5', 'C6', 'C7', 'C8'))]:
                    tags.append('QA_map_clean')
                record['extracted_answer'] = answer
                record['correct'] = is_correct
                record['pred_map'] = parsed
                record['map_metrics'] = metrics
                record['error_tags'] = tags
                vstr = None
                if args.verbose:
                    vstr = '[%d][%s] %s answer=%s correct=%s tags=%s' % (
                        i + 1, arm, sample['question_type'], answer, is_correct, tags)
                out.append((key, record, vstr))
        return out

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futures = {ex.submit(process, i, sample): i for i, sample in enumerate(test_samples)}
        for fut in as_completed(futures):
            recs = fut.result()
            with lock:
                for key, record, vstr in recs:
                    results = [r for r in results if not (r.get('sample_idx') == record['sample_idx'] and r.get('arm') == record['arm'])]
                    results.append(record)
                    done.add(key)
                    if vstr:
                        print(vstr, flush=True)
                completed[0] += 1
                print('[%d/%d] done' % (completed[0], len(test_samples)), flush=True)
                if completed[0] % 5 == 0:
                    partial = args.output.replace('.json', '_partial_%d.json' % completed[0])
                    with open(partial, 'w', encoding='utf-8') as f:
                        json.dump(results, f, indent=2, ensure_ascii=False)
                    print('[Auto-save] %d/%d samples -> %s' % (completed[0], len(test_samples), partial), flush=True)
                if recs and all(r[1].get('error') for r in recs):
                    fail_streak += 1
                    recent.append(1)
                elif recs:
                    fail_streak = 0
                    recent.append(0)
                if fail_streak >= args.max_consecutive_fails or (
                        len(recent) == recent.maxlen and sum(recent) / len(recent) >= args.max_fail_rate):
                    stop_reason = 'streak=%d window_rate=%.2f' % (fail_streak, sum(recent) / len(recent) if recent else 0)
                    for f in futures:
                        f.cancel()
                    break

    summary = summarize(results, arms)
    if stop_reason:
        print('[STOP] failure guard: %s' % stop_reason, flush=True)
    results.append({'__summary__': summary})
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print('Done. Output: %s' % args.output)


def summarize(results, arms):
    summary = {'arms': arms}
    for arm in arms:
        recs = [r for r in results if r['arm'] == arm]
        run = [r for r in recs if not r.get('error')]
        correct = sum(1 for r in run if r.get('correct'))
        total = len(run)
        acc = correct / total * 100 if total else 0.0
        abs_scores = [
            mra(r.get('extracted_answer'), r.get('ground_truth'))
            for r in run
            if 'abs_distance' in r.get('question_type', '')
        ]
        mra_avg = sum(abs_scores) / len(abs_scores) * 100 if abs_scores else None
        metrics = [r['map_metrics'] for r in run if r.get('map_metrics')]
        agg = {}
        if metrics:
            agg['missed_rate'] = sum(m['missed_instances'] for m in metrics) / max(
                1, sum(m['gt_instances'] for m in metrics))
            agg['extra_rate'] = sum(m['extra_instances'] for m in metrics) / max(
                1, sum(m['gt_instances'] for m in metrics))
            agg['pair_accuracy'] = sum(m['pairs_correct'] for m in metrics) / max(
                1, sum(m['pairs'] for m in metrics))
            agg['adjacent_accuracy'] = sum(m['adjacent_correct'] for m in metrics) / max(
                1, sum(m['adjacent_pairs'] for m in metrics))
            ratios = [r2 for m in metrics for r2 in m['scale_ratios']]
            if ratios:
                agg['scale_median'] = sorted(ratios)[len(ratios) // 2]
            if arm in ('threeview', 'threeview_3pass', 'threeview_2stage'):
                agg['cross_view_conflict_rate'] = sum(
                    m['cross_view_conflicts'] for m in metrics) / max(
                    1, sum(m['cross_view_checked'] for m in metrics))
                agg['cross_view_missing_rate'] = sum(
                    m['cross_view_missing'] for m in metrics) / max(
                    1, sum(m['gt_instances'] for m in metrics) * 3)
                agg['height_accuracy'] = sum(m['height_correct'] for m in metrics) / max(
                    1, sum(m['height_pairs'] for m in metrics))
        summary[arm] = {
            'total': total,
            'correct': correct,
            'accuracy_pct': round(acc, 1),
            'abs_mra_pct': round(mra_avg, 1) if mra_avg is not None else None,
            'map_metrics': agg,
        }
    return summary


if __name__ == '__main__':
    main()
