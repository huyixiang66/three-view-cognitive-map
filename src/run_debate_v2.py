# -*- coding: utf-8 -*-
"""Three-agent debate v2: structured corrections + axis-offset alignment.

v1 used free-text critiques. v2 asks each agent to directly output a corrected
view JSON (mergeable), and explicitly computes shared-axis offsets
(top.x-front.x, top.y-side.y, front.z-side.z) before/after the debate as the
baseline transformation between agent frames.

Usage:
  python run_debate_v2.py --samples vsi_debate_strat_20.json --n 20 --workers 5 --sleep 0
"""
import argparse
import json
import os
import statistics
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from tis_compare import (
    SYSTEM_PROMPT,
    build_gt_map,
    call_api,
    compute_metrics,
    evaluate_answer,
    extract_answer,
    extract_categories,
    load_meta,
    mra,
    VIDEO_CACHE_DIR,
    build_video_message,
    load_video_base64,
)
from run_tis_compare import numeric_ok, answer_template, options_text
from run_debate import VIEWS, VIEW_PROMPTS, FORMAT_HINTS, build_view, parse_view, cross_view_axes, axis_diffs

STRUCT_CRITIQUE_PROMPT = """You are Agent {view}. The other agents' views are below. Consistency checks found these signed axis offsets (other - you), which you should apply to your own coordinates:
- top.x - front.x median: {off_fx}
- top.y - side.y median: {off_sy}
- front.z - side.z median: {off_z}
Produce your FINAL {view_upper} VIEW directly. If the other views have fewer instances, do NOT delete instances from your view to force equal counts: keep every instance you are confident about and note count mismatches in your output. Also correct the axes using the offsets.
Output ONLY JSON: {format_hint}

YOUR VIEW:
{my_view}

OTHER VIEWS:
{other_views}"""


def axis_offsets(parsed):
    """Signed median shared-axis offsets: top.x-front.x, top.y-side.y, front.z-side.z."""
    d_fx, d_sy, d_z = [], [], []
    cats = set(parsed['top']) | set(parsed['front']) | set(parsed['side'])
    for cat in cats:
        d_fx += axis_diffs(parsed['top'].get(cat, []), parsed['front'].get(cat, []), 0, 0)
        d_sy += axis_diffs(parsed['top'].get(cat, []), parsed['side'].get(cat, []), 1, 0)
        d_z += axis_diffs(parsed['front'].get(cat, []), parsed['side'].get(cat, []), 1, 1)
    return {
        'top_front_x': statistics.median(d_fx) if d_fx else 0.0,
        'top_side_y': statistics.median(d_sy) if d_sy else 0.0,
        'front_side_z': statistics.median(d_z) if d_z else 0.0,
    }


def structured_critique(model_name, view, my_text, other_texts, offsets, video_b64, sleep):
    others = '\n\n'.join('%s VIEW:\n%s' % (v.upper(), other_texts[v]) for v in VIEWS if v != view)
    text = STRUCT_CRITIQUE_PROMPT.format(
        view=view, view_upper=view.upper(), format_hint=FORMAT_HINTS[view],
        off_fx=offsets['top_front_x'], off_sy=offsets['top_side_y'],
        off_z=offsets['front_side_z'], my_view=my_text, other_views=others)
    content = build_video_message(text, video_b64) if video_b64 else text
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': content}]
    raw = call_api(model_name, messages, sleep_time=sleep)
    if not raw:
        return None, 'CRITIQUE_API_FAIL'
    if parse_view(raw, view) is None:
        return raw, 'CRITIQUE_PARSE_FAIL'
    return raw, None


def fuse_views(final_parsed):
    """Deterministic axis alignment: align front/side into TOP frame."""
    top = final_parsed['top']['coords']
    front = final_parsed['front']['coords']
    side = final_parsed['side']['coords']
    off = axis_offsets({'top': top, 'front': front, 'side': side})
    front2 = {cat: [[p[0] + off['top_front_x'], p[1]] for p in pts] for cat, pts in front.items()}
    side2 = {cat: [[p[0] + off['top_side_y'], p[1] + off['front_side_z']] for p in pts] for cat, pts in side.items()}
    fused = {'top': top, 'front': front2, 'side': side2,
            'sizes': {'top': final_parsed['top']['sizes'], 'front': final_parsed['front']['sizes'],
                      'side': final_parsed['side']['sizes']}, 'room': None}
    return fused, off


def process_sample(i, sample, args):
    print('[%d] start %s %s %s' % (
        i + 1, sample['dataset'], sample['scene_name'], sample['question_type']), flush=True)
    raw_views = {}
    parsed = {}
    for view in VIEWS:
        raw, err, cats = build_view(sample, view, args.model, args.sleep)
        if err:
            return i, {'sample_idx': i, 'error': err, 'categories': cats}
        raw_views[view] = raw
        parsed[view] = parse_view(raw, view)
    if any(parsed[v] is None for v in VIEWS):
        return i, {'sample_idx': i, 'error': 'BUILD_PARSE_FAIL', 'categories': cats}

    offsets_before = axis_offsets({v: parsed[v]['coords'] for v in VIEWS})
    video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
    video_b64 = load_video_base64(video_path)
    view_texts = {v: json.dumps({'coords': parsed[v]['coords'], 'sizes': parsed[v]['sizes']}, ensure_ascii=False) for v in VIEWS}

    finals = {}
    for view in VIEWS:
        raw, err = structured_critique(
            args.model, view, view_texts[view], view_texts,
            offsets_before, video_b64, args.sleep)
        if err:
            # Fallback: keep the original view so the sample still completes.
            finals[view] = raw_views[view]
        else:
            finals[view] = raw

    final_parsed = {v: parse_view(finals[v], v) for v in VIEWS}
    combined = {
        'top': final_parsed['top']['coords'],
        'front': final_parsed['front']['coords'],
        'side': final_parsed['side']['coords'],
        'sizes': {'top': final_parsed['top']['sizes'], 'front': final_parsed['front']['sizes'],
                  'side': final_parsed['side']['sizes']},
        'room': None,
    }
    axes_after = cross_view_axes(combined)

    meta_scene = load_meta(sample['dataset']).get(sample['scene_name'], {})
    gt_map, matched = build_gt_map(sample, meta_scene)
    fused_map = None
    fusion_offsets = None
    answer_map = combined
    if getattr(args, 'fusion', False):
        fused_map, fusion_offsets = fuse_views(final_parsed)
        answer_map = fused_map
        axes_after = cross_view_axes(fused_map)
    metrics = compute_metrics(gt_map, answer_map, 'threeview')

    template = answer_template(sample['question_type'])
    opts = options_text(sample)
    text_part = ('Here is the final three-view cognitive map of the room (combined after debate):\n%s\n\n' %
                 json.dumps(answer_map, ensure_ascii=False)) + template.format(question=sample['question'], options=opts)
    video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
    video_b64 = load_video_base64(video_path)
    if video_b64:
        user_content = build_video_message(text_part, video_b64)
    else:
        user_content = text_part
    raw_answer = call_api(args.model, [{'role': 'system', 'content': SYSTEM_PROMPT},
                                       {'role': 'user', 'content': user_content}], sleep_time=args.sleep)
    if not raw_answer:
        return i, {'sample_idx': i, 'error': 'ANSWER_API_FAIL', 'categories': cats}
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
        'arm': 'debate3_v2',
        'scene': sample['scene_name'],
        'dataset': sample['dataset'],
        'question_type': qt,
        'question': sample['question'],
        'ground_truth': sample['ground_truth'],
        'categories': cats,
        'categories_matched': sorted(set(matched.values())) if matched else [],
        'gt_map': gt_map,
        'raw_views': raw_views,
        'final_views': finals,
        'pred_map': combined,
        'fused_map': fused_map,
        'fusion_offsets': fusion_offsets,
        'offsets_before': offsets_before,
        'cross_view_axes': axes_after,
        'map_metrics': metrics,
        'raw_answer': raw_answer,
        'extracted_answer': answer,
        'correct': correct,
        'error': None,
    }
    if args.verbose:
        print('[%d] answer=%s correct=%s offsets=%s axes=%s' % (
            i + 1, answer, correct, offsets_before, axes_after), flush=True)
    return i, rec


def main():
    parser = argparse.ArgumentParser(description='Three-agent debate v2')
    parser.add_argument('--model', type=str, default='gemini-3.5-flash')
    parser.add_argument('--samples', type=str, default='vsi_debate_strat_20.json')
    parser.add_argument('--output', default='results_debate3_v2_strat20.json')
    parser.add_argument('--n', type=int, default=20)
    parser.add_argument('--sleep', type=float, default=1.0)
    parser.add_argument('--workers', type=int, default=5)
    parser.add_argument('--fusion', action='store_true', help='Enable deterministic axis-aligned fusion (v3)')
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
