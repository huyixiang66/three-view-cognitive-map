# -*- coding: utf-8 -*-
"""Debate v6: CoCoSI-style atomic commit + conflict-triggered pairwise debate.

Three view agents (TOP / FRONT / SIDE) each build one view with their own
camera. A global map is reconstructed in the TOP frame. Before committing, the
summary logic detects cross-view conflicts (shared-axis mismatches). Each
conflict triggers a pairwise debate between the two involved agents (with
video), and the corrected views are re-integrated. The final committed map is
produced by projecting the fused 3D points through each agent's real 4x4
camera matrix.

Answer stage keeps the shared/noshared branches: TOP memory vs fresh
map-only conversation.
"""
import argparse
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np

from run_debate import FORMAT_HINTS, VIEWS, parse_view
from run_debate_v5 import (
    CAMERAS,
    build_view,
    call_critique,
    camera_text,
    combined_map,
    fused_3d,
    fused_reference,
    project_fused_to_view,
    view_transform,
)
from run_tis_compare import answer_template, numeric_ok, options_text
from tis_compare import (
    SYSTEM_PROMPT,
    build_gt_map,
    call_api,
    compute_metrics,
    evaluate_answer,
    extract_answer,
    load_meta,
    mra,
)

DEBATE_PROMPT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
The summary agent found a cross-view conflict with Agent {other_name}:
- axis: {axis}
- category: {cat}
- your value: {my_val}
- other value: {other_val}
Compare the video with the other agent's observation and output your FINAL {view_upper} VIEW directly.
Do NOT delete instances to force equal counts: keep every instance you are confident about.
Output ONLY JSON: {format_hint}

YOUR VIEW:
{my_view}

OTHER VIEW:
{other_view}"""

CONFLICT_TOL = 2.0


def match_pairs_on(a, b, ia, ib):
    a = [list(p) for p in a]
    b = [list(p) for p in b]
    out = []
    while a and b:
        best = min(((abs(x[ia] - y[ib]), i, j)
                    for i, x in enumerate(a) for j, y in enumerate(b)), key=lambda t: t[0])
        _, i, j = best
        out.append((a[i], b[j], best[0]))
        a.pop(i)
        b.pop(j)
    return out


def detect_conflicts(parsed, tol=CONFLICT_TOL):
    conflicts = []
    cats = (set(parsed['top']['coords']) | set(parsed['front']['coords'])
            | set(parsed['side']['coords']))
    for cat in cats:
        t = parsed['top']['coords'].get(cat, [])
        f = parsed['front']['coords'].get(cat, [])
        s = parsed['side']['coords'].get(cat, [])
        for tp, fp, d in match_pairs_on(t, f, 0, 0):
            if d > tol:
                conflicts.append({'pair': ('top', 'front'), 'axis': 'x', 'cat': cat,
                                  'my_val': tp[0], 'other_val': fp[0]})
        for tp, sp, d in match_pairs_on(t, s, 1, 0):
            if d > tol:
                conflicts.append({'pair': ('top', 'side'), 'axis': 'y', 'cat': cat,
                                  'my_val': tp[1], 'other_val': sp[0]})
        for fp, sp, d in match_pairs_on(f, s, 1, 1):
            if d > tol:
                conflicts.append({'pair': ('front', 'side'), 'axis': 'z', 'cat': cat,
                                  'my_val': fp[1], 'other_val': sp[1]})
    return conflicts


def debate_text(agent, other, conflict, my_view, other_view):
    cam = camera_text(agent)
    return DEBATE_PROMPT.format(
        name=CAMERAS[agent]['name'], view_upper=agent.upper(),
        format_hint=FORMAT_HINTS[agent], other_name=CAMERAS[other]['name'],
        axis=conflict['axis'], cat=conflict['cat'],
        my_val=conflict['my_val'], other_val=conflict['other_val'],
        my_view=my_view, other_view=other_view, **cam)


def commit_global_map(final_parsed):
    """Committed global map: fused 3D reconstructed in TOP frame, projected
    through each agent's real camera matrix."""
    ref = fused_reference(final_parsed)
    f3d = fused_3d(ref)
    proj = {v: project_fused_to_view(f3d, v) for v in VIEWS}
    committed = {
        'top': proj['top'],
        'front': proj['front'],
        'side': proj['side'],
        'sizes': {v: final_parsed[v]['sizes'] for v in VIEWS},
        'room': None,
    }
    if sum(len(v) for v in proj.values()) == 0:
        return combined_map(final_parsed)
    return committed


def process_sample(i, sample, args):
    print('[%d] start %s %s %s' % (
        i + 1, sample['dataset'], sample['scene_name'], sample['question_type']), flush=True)
    raw_views = {}
    parsed = {}
    messages_top = None
    cats = []
    for view in VIEWS:
        raw, messages, err, cats = build_view(
            sample, view, args.model, args.sleep, dry_run=args.dry_run)
        if err:
            return i, {'sample_idx': i, 'error': err, 'categories': cats}
        raw_views[view] = raw
        parsed[view] = parse_view(raw, view)
        if parsed[view] is None:
            return i, {'sample_idx': i, 'error': 'BUILD_PARSE_FAIL', 'categories': cats}
        if view == 'top':
            messages_top = messages

    video_b64 = None
    if not args.dry_run:
        from tis_compare import VIDEO_CACHE_DIR, load_video_base64
        video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
        video_b64 = load_video_base64(video_path)

    meta_scene = load_meta(sample['dataset']).get(sample['scene_name'], {})
    gt_map, matched = build_gt_map(sample, meta_scene)
    metrics_round0 = compute_metrics(gt_map, combined_map(parsed), 'threeview')

    finals = dict(raw_views)
    round_metrics = {'round0': metrics_round0}
    for rnd in range(args.rounds):
        rp = {v: parse_view(finals[v], v) for v in VIEWS}
        if any(p is None for p in rp.values()):
            break
        round_metrics['round%d' % (rnd + 1)] = compute_metrics(
            gt_map, combined_map(rp), 'threeview')
        conflicts = detect_conflicts(rp)
        if not conflicts:
            break
        pairs = set(c['pair'] for c in conflicts)
        for pair in pairs:
            for agent in pair:
                other = pair[0] if pair[1] == agent else pair[1]
                conflict = next(c for c in conflicts if c['pair'] == pair)
                text = debate_text(
                    agent, other, conflict,
                    finals[agent],
                    json.dumps(rp[other]['coords'], ensure_ascii=False))
                memory = (agent == 'top' and messages_top and not args.dry_run)
                raw = call_critique(messages_top if memory else None, text, agent,
                                    args.model, args.sleep, video_b64=video_b64,
                                    memory=memory, dry_run=args.dry_run)
                if args.dry_run:
                    raw = finals[agent]
                if raw is not None:
                    parsed_new = parse_view(raw, agent)
                    if parsed_new is not None and any(parsed_new['coords'].values()):
                        finals[agent] = raw

    final_parsed = {v: parse_view(finals[v], v) for v in VIEWS}
    if any(p is None for p in final_parsed.values()):
        return i, {'sample_idx': i, 'error': 'FINAL_PARSE_FAIL', 'categories': cats}
    committed = commit_global_map(final_parsed)
    metrics_final = compute_metrics(gt_map, committed, 'threeview')
    round_metrics['final'] = metrics_final

    template = answer_template(sample['question_type'])
    opts = options_text(sample)
    text_part = ('Here is the committed global three-view cognitive map of the room (agents aligned + verified):\n%s\n\n' %
                 json.dumps(committed, ensure_ascii=False)) + template.format(
                     question=sample['question'], options=opts)

    def answer_one(text, conv_messages):
        if args.dry_run:
            return 'ANSWER: %s' % sample['ground_truth'], None
        if conv_messages is not None:
            conv_messages.append({'role': 'user', 'content': text})
            raw = call_api(args.model, conv_messages, sleep_time=args.sleep)
        else:
            raw = call_api(args.model, [{'role': 'system', 'content': SYSTEM_PROMPT},
                                        {'role': 'user', 'content': text}], sleep_time=args.sleep)
        if not raw:
            return raw, 'ANSWER_API_FAIL'
        ans = extract_answer(raw, sample['question_type'])
        if ans is None:
            retry_text = ('Reply with ONLY the final answer as a single letter or number.\nQuestion: %s\n%s' %
                          (sample['question'], opts))
            if conv_messages is not None:
                conv_messages.append({'role': 'user', 'content': retry_text})
                raw2 = call_api(args.model, conv_messages, sleep_time=args.sleep)
            else:
                raw2 = call_api(args.model, [{'role': 'system', 'content': SYSTEM_PROMPT},
                                             {'role': 'user', 'content': retry_text}],
                                sleep_time=args.sleep)
            ans2 = extract_answer(raw2, sample['question_type']) if raw2 else None
            if ans2 is not None:
                raw, ans = raw2, ans2
        return raw, ans

    def is_correct_ans(ans):
        qt = sample['question_type']
        if qt in ('object_abs_distance', 'object_size_estimation', 'room_size_estimation'):
            return mra(ans, sample['ground_truth']) > 0
        if qt == 'object_counting':
            return numeric_ok(ans, sample['ground_truth'], qt)
        return evaluate_answer(ans, sample['ground_truth'])

    conv = list(messages_top) if (args.answer_mode == 'shared' and messages_top) else None
    answers_memory = None
    if args.answer_mode == 'both':
        conv_shared = list(messages_top) if messages_top else None
        raw_s, ans_s = answer_one(text_part, conv_shared)
        raw_n, ans_n = answer_one(text_part, None)
        if not raw_s or not raw_n:
            return i, {'sample_idx': i, 'error': 'ANSWER_API_FAIL', 'categories': cats}
        correct_s = is_correct_ans(ans_s)
        correct_n = is_correct_ans(ans_n)
        raw_answer, answer, correct = raw_s, ans_s, correct_s
        answers_memory = {
            'shared': {'raw_answer': raw_s, 'extracted_answer': ans_s, 'correct': correct_s},
            'noshared': {'raw_answer': raw_n, 'extracted_answer': ans_n, 'correct': correct_n},
        }
    else:
        raw_answer, answer = answer_one(text_part, conv)
        if not raw_answer:
            return i, {'sample_idx': i, 'error': 'ANSWER_API_FAIL', 'categories': cats}
        correct = is_correct_ans(answer)

    rec = {
        'sample_idx': i,
        'arm': 'debate6',
        'answer_mode': args.answer_mode,
        'scene': sample['scene_name'],
        'dataset': sample['dataset'],
        'question_type': sample['question_type'],
        'question': sample['question'],
        'ground_truth': sample['ground_truth'],
        'categories': cats,
        'categories_matched': sorted(set(matched.values())) if matched else [],
        'gt_map': gt_map,
        'cameras': CAMERAS,
        'rounds_run': len([k for k in round_metrics if k.startswith('round') and k != 'round0']),
        'transforms_analytic': {v: view_transform(v, 'top') for v in ('front', 'side')},
        'raw_views': raw_views,
        'final_views': finals,
        'pred_map': committed,
        'fused_map': committed,
        'round_metrics': round_metrics,
        'map_metrics': metrics_final,
        'raw_answer': raw_answer,
        'extracted_answer': answer,
        'answers_memory': answers_memory,
        'correct': correct,
        'error': None,
    }
    if args.verbose:
        print('[%d] answer=%s correct=%s conflicts_rounds=%s' % (
            i + 1, answer, correct, list(round_metrics)), flush=True)
    return i, rec


def main():
    parser = argparse.ArgumentParser(description='Debate v6: atomic commit + pairwise debate')
    parser.add_argument('--model', type=str, default='gemini-3.5-flash')
    parser.add_argument('--samples', type=str, default='vsi_debate_50.json')
    parser.add_argument('--output', default='results_debate6.json')
    parser.add_argument('--n', type=int, default=50)
    parser.add_argument('--rounds', type=int, default=2)
    parser.add_argument('--answer-mode', choices=['shared', 'noshared', 'both'], default='both')
    parser.add_argument('--sleep', type=float, default=1.0)
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--resume', type=str, default=None)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(line_buffering=True)

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
    completed = [len(done)]

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
