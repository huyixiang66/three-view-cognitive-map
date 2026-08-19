# -*- coding: utf-8 -*-
"""Three-agent one-round debate baseline.

Agent TOP / Agent FRONT / Agent SIDE each independently build one view from the
video (each with its own camera frame / look_at / look_up), exchange views,
critique each other for cross-view consistency, then output final views which
are combined into one three-view cognitive map.

Usage:
  python run_debate.py --samples vsi_subset_200.json --n 20 --workers 3 --sleep 1
"""
import argparse
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    normalize_sizes,
)
from cogmap_direct_metrics import rigid_align, apply_rigid
from run_tis_compare import numeric_ok, answer_template, options_text

VIEWS = ('top', 'front', 'side')

VIEW_PROMPTS = {
    'top': """You are Agent TOP. You are watching the room from your own camera position with your own look_at and look_up directions. Build the TOP VIEW (bird's-eye) cognitive map: category -> [[x, y, w, d], ...] on a 10x10 grid (x horizontal, y depth, w width, d depth in grid cells).
Focus on the categories: {categories_of_interest}. Include ALL instances.
Output ONLY JSON: {{"category name": [[x_1, y_1, w_1, d_1], ...], ...}}""",
    'front': """You are Agent FRONT. You are watching the room from your own camera position with your own look_at and look_up directions. Build the FRONT VIEW (elevation) cognitive map: category -> [[x, z, w, h], ...] on a 10x10 grid (x horizontal, z height 0=floor 9=ceiling, w width, h height in grid cells).
Focus on the categories: {categories_of_interest}. Include ALL instances.
Output ONLY JSON: {{"category name": [[x_1, z_1, w_1, h_1], ...], ...}}""",
    'side': """You are Agent SIDE. You are watching the room from your own camera position with your own look_at and look_up directions. Build the SIDE VIEW (profile) cognitive map: category -> [[y, z, d, h], ...] on a 10x10 grid (y depth, z height 0=floor 9=ceiling, d depth, h height in grid cells).
Focus on the categories: {categories_of_interest}. Include ALL instances.
Output ONLY JSON: {{"category name": [[y_1, z_1, d_1, h_1], ...], ...}}""",
}

DEBATE_PROMPT = """You are Agent {view}. Your current {view_upper} VIEW is below. The other two agents built their own views with their own camera frames. Check cross-view consistency:
- top.x must equal front.x
- top.y must equal side.y
- front.z must equal side.z
- instance counts should match across views
List concrete corrections to YOUR OWN view (which objects to add/remove/move/resize) as JSON: {{"fixes": ["...", ...]}}. Do NOT output the full view yet.

YOUR VIEW:
{my_view}

OTHER VIEWS:
{other_views}"""

FINALIZE_PROMPT = """You are Agent {view}. Produce your FINAL {view_upper} VIEW incorporating the corrections you agree with.
Output ONLY JSON: {format_hint}

YOUR ORIGINAL VIEW:
{my_view}

CRITIQUE:
{critique}"""

FORMAT_HINTS = {
    'top': '{{"category name": [[x, y, w, d], ...], ...}}',
    'front': '{{"category name": [[x, z, w, h], ...], ...}}',
    'side': '{{"category name": [[y, z, d, h], ...], ...}}',
}


def build_view(sample, view, model_name, sleep):
    categories = extract_categories(sample)
    cats = ', '.join(categories) if categories else 'all objects visible in the scene'
    video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
    video_b64 = load_video_base64(video_path)
    if video_b64 is None:
        return None, 'NO_VIDEO', categories
    prompt = VIEW_PROMPTS[view].format(categories_of_interest=cats)
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': build_video_message(prompt, video_b64)}]
    raw = call_api(model_name, messages, sleep_time=sleep)
    if not raw:
        return raw, 'MAP_API_FAIL', categories
    return raw, None, categories


def parse_view(raw, view):
    data = extract_json(raw)
    if data is None:
        return None
    try:
        return {'coords': normalize_view(data, view), 'sizes': normalize_sizes(data, view)}
    except Exception:
        return None


def debate_view(model_name, view, my_raw, other_raws, sleep):
    others = '\n\n'.join('%s VIEW:\n%s' % (v.upper(), other_raws[v]) for v in VIEWS if v != view)
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': DEBATE_PROMPT.format(
                    view=view, view_upper=view.upper(), my_view=my_raw, other_views=others)}]
    return call_api(model_name, messages, sleep_time=sleep)


def finalize_view(model_name, view, my_raw, critique, sleep):
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': FINALIZE_PROMPT.format(
                    view=view, view_upper=view.upper(), format_hint=FORMAT_HINTS[view],
                    my_view=my_raw, critique=critique)}]
    raw = call_api(model_name, messages, sleep_time=sleep)
    if not raw:
        return None, 'FINAL_API_FAIL'
    if parse_view(raw, view) is None:
        return raw, 'FINAL_PARSE_FAIL'
    return raw, None


def axis_diffs(list_a, list_b, idx_a, idx_b):
    """Greedy-match instances by the shared axis and return signed diffs."""
    a = [list(p) for p in list_a]
    b = [list(p) for p in list_b]
    diffs = []
    while a and b:
        best = min(((abs(x[idx_a] - y[idx_b]), i, j)
                    for i, x in enumerate(a) for j, y in enumerate(b)), key=lambda t: t[0])
        _, i, j = best
        diffs.append(a[i][idx_a] - b[j][idx_b])
        a.pop(i)
        b.pop(j)
    return diffs


def cross_view_axes(combined):
    out = {'top_front_x': [], 'top_side_y': [], 'front_side_z': []}
    cats = (set(combined['top']) | set(combined['front']) | set(combined['side']))
    for cat in cats:
        t = combined['top'].get(cat, [])
        f = combined['front'].get(cat, [])
        s = combined['side'].get(cat, [])
        out['top_front_x'] += [abs(d) for d in axis_diffs(t, f, 0, 0)]
        out['top_side_y'] += [abs(d) for d in axis_diffs(t, s, 1, 0)]
        out['front_side_z'] += [abs(d) for d in axis_diffs(f, s, 1, 1)]
    return {k: (sum(v) / len(v) if v else None) for k, v in out.items()}


def process_sample(i, sample, args):
    print('[%d] start %s %s %s' % (
        i + 1, sample['dataset'], sample['scene_name'], sample['question_type']), flush=True)
    raw_views = {}
    for view in VIEWS:
        raw, err, cats = build_view(sample, view, args.model, args.sleep)
        if err:
            return i, {'sample_idx': i, 'error': err, 'categories': cats}
        raw_views[view] = raw

    critiques = {}
    for view in VIEWS:
        c = debate_view(args.model, view, raw_views[view], raw_views, args.sleep)
        if not c:
            return i, {'sample_idx': i, 'error': 'CRITIQUE_API_FAIL'}
        critiques[view] = c

    finals = {}
    for view in VIEWS:
        raw, err = finalize_view(args.model, view, raw_views[view], critiques[view], args.sleep)
        if err:
            return i, {'sample_idx': i, 'error': err}
        finals[view] = raw

    parsed = {v: parse_view(finals[v], v) for v in VIEWS}
    combined = {
        'top': parsed['top']['coords'],
        'front': parsed['front']['coords'],
        'side': parsed['side']['coords'],
        'sizes': {'top': parsed['top']['sizes'], 'front': parsed['front']['sizes'], 'side': parsed['side']['sizes']},
        'room': None,
    }
    axes = cross_view_axes(combined)

    meta_scene = load_meta(sample['dataset']).get(sample['scene_name'], {})
    gt_map, matched = build_gt_map(sample, meta_scene)
    metrics = compute_metrics(gt_map, combined, 'threeview')

    template = answer_template(sample['question_type'])
    opts = options_text(sample)
    user = ('Here is the final three-view cognitive map of the room (combined after debate):\n%s\n\n' %
            json.dumps(combined, ensure_ascii=False)) + template.format(question=sample['question'], options=opts)
    raw_answer = call_api(args.model, [{'role': 'system', 'content': SYSTEM_PROMPT},
                                       {'role': 'user', 'content': user}], sleep_time=args.sleep)
    if not raw_answer:
        return i, {'sample_idx': i, 'error': 'ANSWER_API_FAIL'}
    answer = extract_answer(raw_answer, sample['question_type'])
    qt = sample['question_type']
    if qt in ('object_abs_distance', 'object_size_estimation', 'room_size_estimation'):
        correct = mra(answer, sample['ground_truth']) > 0
    elif qt == 'object_counting':
        correct = numeric_ok(answer, sample['ground_truth'], qt)
    else:
        correct = evaluate_answer(answer, sample['ground_truth'])

    rec = {
        'sample_idx': i,
        'arm': 'debate3',
        'scene': sample['scene_name'],
        'dataset': sample['dataset'],
        'question_type': qt,
        'question': sample['question'],
        'ground_truth': sample['ground_truth'],
        'categories': cats,
        'categories_matched': sorted(set(matched.values())) if matched else [],
        'gt_map': gt_map,
        'raw_views': raw_views,
        'critiques': critiques,
        'final_views': finals,
        'pred_map': combined,
        'cross_view_axes': axes,
        'map_metrics': metrics,
        'raw_answer': raw_answer,
        'extracted_answer': answer,
        'correct': correct,
        'error': None,
    }
    if args.verbose:
        print('[%d] answer=%s correct=%s axes=%s' % (i + 1, answer, correct, axes), flush=True)
    return i, rec


def main():
    parser = argparse.ArgumentParser(description='Three-agent one-round debate baseline')
    parser.add_argument('--model', type=str, default='gemini-3.5-flash')
    parser.add_argument('--samples', type=str, default='vsi_subset_200.json')
    parser.add_argument('--output', default='results_debate3.json')
    parser.add_argument('--n', type=int, default=20)
    parser.add_argument('--sleep', type=float, default=1.0)
    parser.add_argument('--workers', type=int, default=3)
    parser.add_argument('--resume', type=str, default=None)
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    samples_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.samples)
    with open(samples_path, encoding='utf-8') as f:
        samples = json.load(f)
    test_samples = samples[:args.n]

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
    completed = [len({r['sample_idx'] for r in results})]

    def process(i, sample):
        if i in done:
            return i, None
        return process_sample(i, sample, args)

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
    print('Done. records=%d ok=%d correct=%d (%.0f%%)' % (
        len(results), len(ok), correct, 100 * correct / len(ok) if ok else 0))
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
