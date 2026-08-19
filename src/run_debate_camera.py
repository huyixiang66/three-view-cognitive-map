# -*- coding: utf-8 -*-
"""Debate v4 skeleton: every agent is a full camera frame.

Agent i builds a complete three-view map from the video with its own
position / look_at / look_up. Each agent's three views are reconstructed into
3D instance points; matched instances between agents are used to estimate a
rigid transform (R, t, optional mirror) via camera_utils. Agents then critique
each other's aligned map WITH the video, output corrected full maps, and the
loop repeats for --rounds. The final fused map lives in agent 0's frame.

--dry-run uses GT maps as the agent outputs so the pipeline can be validated
without any API calls.
"""
import argparse
import json
import math
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np

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
from run_tis_compare import numeric_ok, answer_template, options_text
from camera_utils import estimate_rigid_transform, apply_transform

FORMAT_HINT = ('{"top": {"category name": [[x, y, w, d], ...], ...}, '
               '"front": {"category name": [[x, z, w, h], ...], ...}, '
               '"side": {"category name": [[y, z, d, h], ...], ...}, '
               '"room": {"width": w, "depth": d, "area_m2": a}}')

CAMERA_BUILD_PROMPT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
Watch the video from YOUR camera frame and build a complete three-view cognitive map (TOP / FRONT / SIDE) with object sizes and room size.
Focus on the categories: {categories_of_interest}. Include ALL instances.
Output ONLY JSON:
{format_hint}"""

CAMERA_CRITIQUE_PROMPT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
The other agent's map has been aligned into your frame. Compare it with your own map and the video, then output your FINAL three-view map.
Do NOT delete instances to force equal counts: keep every instance you are confident about.
Output ONLY JSON:
{format_hint}

YOUR MAP:
{my_map}

OTHER MAP (aligned into your frame):
{other_map}"""

CAMERAS = [
    {'name': 'A', 'position': [0.0, 0.0, 3.0], 'look_at': [0.0, 0.0, 0.0], 'look_up': [0.0, 1.0, 0.0]},
    {'name': 'B', 'position': [2.0, -1.0, 2.5], 'look_at': [0.0, 0.0, 0.0], 'look_up': [0.0, 1.0, 0.0]},
]


def agent_names(agents):
    return [CAMERAS[i]['name'] for i in range(agents)]


def camera_text(i):
    c = CAMERAS[i]
    return {'position': c['position'], 'look_at': c['look_at'], 'look_up': c['look_up']}


def build_agent_map(sample, i, model_name, sleep, dry_run=False):
    categories = extract_categories(sample)
    cats = ', '.join(categories) if categories else 'all objects visible in the scene'
    if dry_run:
        meta_scene = load_meta(sample['dataset']).get(sample['scene_name'], {})
        gt_map, _ = build_gt_map(sample, meta_scene)
        raw = json.dumps(gt_map, ensure_ascii=False)
        return raw, [], None
    video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
    video_b64 = load_video_base64(video_path)
    if video_b64 is None:
        return None, [], 'NO_VIDEO'
    cam = camera_text(i)
    prompt = CAMERA_BUILD_PROMPT.format(
        name=CAMERAS[i]['name'], position=cam['position'], look_at=cam['look_at'],
        look_up=cam['look_up'], categories_of_interest=cats, format_hint=FORMAT_HINT)
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': build_video_message(prompt, video_b64)}]
    raw = call_api(model_name, messages, sleep_time=sleep)
    if not raw:
        return raw, messages, 'MAP_API_FAIL'
    return raw, messages, None


def critique_agent(sample, i, my_raw, other_raw, model_name, sleep, dry_run=False):
    if dry_run:
        return my_raw, None
    video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
    video_b64 = load_video_base64(video_path)
    cam = camera_text(i)
    text = CAMERA_CRITIQUE_PROMPT.format(
        name=CAMERAS[i]['name'], position=cam['position'], look_at=cam['look_at'],
        look_up=cam['look_up'], format_hint=FORMAT_HINT, my_map=my_raw, other_map=other_raw)
    content = build_video_message(text, video_b64) if video_b64 else text
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': content}]
    raw = call_api(model_name, messages, sleep_time=sleep)
    if not raw:
        return raw, 'CRITIQUE_API_FAIL'
    if parse_map(raw, 'threeview') is None:
        return raw, 'CRITIQUE_PARSE_FAIL'
    return raw, None


def critique_agent_memory(messages, my_raw, other_raw, i, model_name, sleep):
    """Append critique to an existing agent conversation (video already in memory)."""
    cam = camera_text(i)
    text = CAMERA_CRITIQUE_PROMPT.format(
        name=CAMERAS[i]['name'], position=cam['position'], look_at=cam['look_at'],
        look_up=cam['look_up'], format_hint=FORMAT_HINT, my_map=my_raw, other_map=other_raw)
    messages.append({'role': 'user', 'content': text})
    raw = call_api(model_name, messages, sleep_time=sleep)
    if raw:
        messages.append({'role': 'assistant', 'content': raw})
    if not raw:
        return raw, 'CRITIQUE_API_FAIL'
    if parse_map(raw, 'threeview') is None:
        return raw, 'CRITIQUE_PARSE_FAIL'
    return raw, None


def reconstruct_3d(parsed):
    """Build per-category 3D instance points from an agent's three views."""
    out = {}
    cats = set(parsed['top']) | set(parsed['front']) | set(parsed['side'])
    for cat in cats:
        t = parsed['top'].get(cat, [])
        f = parsed['front'].get(cat, [])
        s = parsed['side'].get(cat, [])
        used_f, used_s = set(), set()
        pts = []
        for tp in t:
            best = None
            for fi, fp in enumerate(f):
                if fi in used_f:
                    continue
                for si, sp in enumerate(s):
                    if si in used_s:
                        continue
                    cost = abs(tp[0] - fp[0]) + abs(tp[1] - sp[0]) + abs(fp[1] - sp[1])
                    if best is None or cost < best[0]:
                        best = (cost, fi, si)
            if best:
                _, fi, si = best
                used_f.add(fi)
                used_s.add(si)
                pts.append([tp[0], tp[1], (f[fi][1] + s[si][1]) / 2.0])
        out[cat] = pts
    return out


def match_3d(a_pts, b_pts):
    a = [list(p) for p in a_pts]
    b = [list(p) for p in b_pts]
    pairs = []
    while a and b:
        best = min(((math.dist(p, q), i, j)
                    for i, p in enumerate(a) for j, q in enumerate(b)), key=lambda x: x[0])
        _, i, j = best
        pairs.append((a[i], b[j]))
        a.pop(i)
        b.pop(j)
    return pairs


def estimate_agent_transform(points_a, points_b):
    """Map agent B 3D points into agent A frame: y = R x + t."""
    if len(points_a) < 2 or len(points_a) != len(points_b):
        return None
    est = estimate_rigid_transform(np.array(points_b, dtype=float),
                                   np.array(points_a, dtype=float))
    return est


def hungarian(cost):
    """Min-cost assignment via scipy; returns list of (row, col) 0-based pairs."""
    from scipy.optimize import linear_sum_assignment
    rows, cols = linear_sum_assignment(np.asarray(cost, dtype=float))
    return list(zip(rows.tolist(), cols.tolist()))


def match_3d_hungarian(a_pts, b_pts):
    if not a_pts or not b_pts:
        return []
    cost = np.array([[math.dist(p, q) for q in b_pts] for p in a_pts])
    return [(a_pts[i], b_pts[j]) for i, j in hungarian(cost)]


def analytic_transform(j, i):
    """Analytic B(j)->A(i) transform from known camera view matrices."""
    from camera_utils import build_view_matrix
    ca = CAMERAS[i]
    cb = CAMERAS[j]
    MA = build_view_matrix(ca['position'], ca['look_at'], ca['look_up'], unity=True)
    MB = build_view_matrix(cb['position'], cb['look_at'], cb['look_up'], unity=True)
    T = MA @ np.linalg.inv(MB)
    return {'R': T[:3, :3], 't': T[:3, 3], 'rmse': None, 'mirror': bool(np.linalg.det(T[:3, :3]) < 0)}


def choose_transform(pairs_a, pairs_b, use_prior=False, gate_rmse=None):
    fitted = estimate_agent_transform(pairs_a, pairs_b)
    est = fitted
    if use_prior:
        ana = analytic_transform(1, 0)
        if pairs_a:
            pb = np.array(pairs_b, dtype=float)
            pa = np.array(pairs_a, dtype=float)
            ana['rmse'] = float(np.sqrt(np.mean(np.sum((apply_transform(pb, ana['R'], ana['t']) - pa) ** 2, axis=1))))
        if fitted is None or (ana.get('rmse') is not None and ana['rmse'] < fitted['rmse']):
            est = ana
    gated = est is None or len(pairs_a) < 2 or est.get('rmse') is None
    if not gated and gate_rmse is not None and est['rmse'] > gate_rmse:
        gated = True
    return est, gated


def fuse_3d_maps(pts_a, pts_b, est, thresh=1.0):
    """Union agent A and (aligned) agent B 3D instances, dedup within thresh."""
    cats = set(pts_a) | set(pts_b)
    out = {}
    for cat in cats:
        a = [list(p) for p in pts_a.get(cat, [])]
        b = pts_b.get(cat, [])
        if est is not None and b:
            b = apply_transform(np.array(b, dtype=float), est['R'], est['t']).tolist()
        merged = [list(p) for p in a]
        for q in b:
            if not a or min(math.dist(p, q) for p in a) > thresh:
                merged.append(list(q))
        out[cat] = merged
    return out


def three_view_from_3d(fused3d, sizes, room):
    top, front, side = {}, {}, {}
    for cat, pts in fused3d.items():
        if not pts:
            continue
        top[cat] = [[p[0], p[1]] for p in pts]
        front[cat] = [[p[0], p[2]] for p in pts]
        side[cat] = [[p[1], p[2]] for p in pts]
    return {'top': top, 'front': front, 'side': side,
            'sizes': sizes, 'room': room}


def process_sample(i, sample, args):
    print('[%d] start %s %s %s' % (
        i + 1, sample['dataset'], sample['scene_name'], sample['question_type']), flush=True)
    n_agents = max(2, min(2, args.agents))  # skeleton supports 2 agents
    raw_views = {}
    finals = {}
    messages_a = None
    for ai in range(n_agents):
        raw, messages, err = build_agent_map(sample, ai, args.model, args.sleep, dry_run=args.dry_run)
        if err:
            return i, {'sample_idx': i, 'error': err}
        raw_views[ai] = raw
        finals[ai] = raw
        if ai == 0:
            messages_a = messages
            if messages:
                messages.append({'role': 'assistant', 'content': raw})
    transforms = []
    for rnd in range(args.rounds):
        parsed = {ai: parse_map(finals[ai], 'threeview') for ai in range(n_agents)}
        if any(p is None for p in parsed.values()):
            return i, {'sample_idx': i, 'error': 'MAP_PARSE_FAIL'}
        pts = {ai: reconstruct_3d(parsed[ai]) for ai in range(n_agents)}
        # Build per-category matched pairs A<-B and estimate transform.
        cats = set(pts[0]) & set(pts[1])
        pairs_a, pairs_b = [], []
        for cat in cats:
            for pa, pb in match_3d(pts[0][cat], pts[1][cat]):
                pairs_a.append(pa)
                pairs_b.append(pb)
        est = estimate_agent_transform(pairs_a, pairs_b)
        transforms.append(est)
        if est is not None:
            transforms[-1] = {'R': est['R'].tolist(), 't': est['t'].tolist(),
                              'rmse': est['rmse'], 'mirror': est['mirror']}
        # Align agent B map into agent A frame (3D), then serialize as JSON for critique.
        other_raw = finals[1]
        if est is not None:
            # Build an aligned 3D-only map text for the critique (keep it simple).
            aligned = {cat: apply_transform(np.array(pts[1][cat], dtype=float), est['R'], est['t']).tolist()
                       for cat in pts[1]}
            other_raw = json.dumps(aligned, ensure_ascii=False)
        new_finals = {}
        for ai in range(n_agents):
            other = other_raw if ai == 0 else finals[0]
            if ai == 0 and messages_a is not None and not args.dry_run:
                raw, err = critique_agent_memory(messages_a, finals[ai], other, ai,
                                                 args.model, args.sleep)
            else:
                raw, err = critique_agent(sample, ai, finals[ai], other, args.model,
                                          args.sleep, dry_run=args.dry_run)
            if err:
                new_finals[ai] = finals[ai]
            else:
                new_finals[ai] = raw
        finals = new_finals

    parsed = {ai: parse_map(finals[ai], 'threeview') for ai in range(n_agents)}
    if any(p is None for p in parsed.values()):
        return i, {'sample_idx': i, 'error': 'FINAL_PARSE_FAIL'}
    # Final 3D reconstruction, agent B -> A transform, then union fusion.
    pts = {ai: reconstruct_3d(parsed[ai]) for ai in range(n_agents)}
    pts = {ai: reconstruct_3d(parsed[ai]) for ai in range(n_agents)}
    matcher = match_3d_hungarian if getattr(args, 'match_mode', 'greedy') == 'hungarian' else match_3d
    cats = set(pts[0]) & set(pts[1])
    pairs_a, pairs_b = [], []
    for cat in cats:
        for pa, pb in matcher(pts[0][cat], pts[1][cat]):
            pairs_a.append(pa)
            pairs_b.append(pb)
    gate_rmse = getattr(args, 'gate_rmse', 1.5) if getattr(args, 'confidence_gate', False) else None
    final_est, fusion_gated = choose_transform(pairs_a, pairs_b,
                                              use_prior=getattr(args, 'transform_prior', False),
                                              gate_rmse=gate_rmse)
    if fusion_gated or final_est is None:
        fused3d = {cat: [list(p) for p in pts[0].get(cat, [])] for cat in set(pts[0])}
        final_est = None
    else:
        fused3d = fuse_3d_maps(pts[0], pts[1], final_est, getattr(args, 'fuse_thresh', 1.0))
    fused = three_view_from_3d(fused3d, parsed[0]['sizes'], parsed[0]['room'])
    fused_instances = sum(len(v) for v in fused3d.values())
    transforms.append({'R': final_est['R'].tolist(), 't': final_est['t'].tolist(),
                       'rmse': final_est['rmse'], 'mirror': final_est['mirror']}
                      if final_est is not None else None)

    meta_scene = load_meta(sample['dataset']).get(sample['scene_name'], {})
    gt_map, matched = build_gt_map(sample, meta_scene)
    metrics = compute_metrics(gt_map, fused, 'threeview')

    template = answer_template(sample['question_type'])
    opts = options_text(sample)
    text_part = ('Here is the fused three-view cognitive map of the room (agents aligned + union):\n%s\n\n' %
                 json.dumps(fused, ensure_ascii=False)) + template.format(question=sample['question'], options=opts)
    if args.dry_run:
        raw_answer = 'ANSWER: %s' % sample['ground_truth']
    elif messages_a is not None:
        messages_a.append({'role': 'user', 'content': text_part})
        raw_answer = call_api(args.model, messages_a, sleep_time=args.sleep)
    else:
        video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
        video_b64 = load_video_base64(video_path)
        content = build_video_message(text_part, video_b64) if video_b64 else text_part
        raw_answer = call_api(args.model, [{'role': 'system', 'content': SYSTEM_PROMPT},
                                           {'role': 'user', 'content': content}], sleep_time=args.sleep)
    if not raw_answer:
        return i, {'sample_idx': i, 'error': 'ANSWER_API_FAIL'}
    answer = extract_answer(raw_answer, sample['question_type'])
    if answer is None and not args.dry_run:
        retry_text = ('Reply with ONLY the final answer as a single letter or number.\nQuestion: %s\n%s' %
                      (sample['question'], opts))
        if messages_a is not None:
            messages_a.append({'role': 'user', 'content': retry_text})
            raw_answer2 = call_api(args.model, messages_a, sleep_time=args.sleep)
        else:
            video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
            vb = load_video_base64(video_path)
            rc = build_video_message(retry_text, vb) if vb else retry_text
            raw_answer2 = call_api(args.model, [{'role': 'system', 'content': SYSTEM_PROMPT},
                                                {'role': 'user', 'content': rc}], sleep_time=args.sleep)
        answer2 = extract_answer(raw_answer2, sample['question_type']) if raw_answer2 else None
        if answer2 is not None:
            raw_answer = raw_answer2
            answer = answer2
    qt = sample['question_type']
    if qt in ('object_abs_distance', 'object_size_estimation', 'room_size_estimation'):
        correct = mra(answer, sample['ground_truth']) > 0
    elif qt == 'object_counting':
        correct = numeric_ok(answer, sample['ground_truth'], qt)
    else:
        correct = evaluate_answer(answer, sample['ground_truth'])

    rec = {
        'answer_mode': 'agentA_memory',
        'sample_idx': i,
        'arm': 'debate4',
        'scene': sample['scene_name'],
        'dataset': sample['dataset'],
        'question_type': qt,
        'question': sample['question'],
        'ground_truth': sample['ground_truth'],
        'categories_matched': sorted(set(matched.values())) if matched else [],
        'gt_map': gt_map,
        'raw_views': raw_views,
        'final_views': finals,
        'transforms': transforms,
        'pred_map': fused,
        'fused_instances': fused_instances,
        'fusion_gated': fusion_gated,
        'map_metrics': metrics,
        'raw_answer': raw_answer,
        'extracted_answer': answer,
        'correct': correct,
        'error': None,
    }
    if args.verbose:
        print('[%d] answer=%s correct=%s transforms=%s' % (i + 1, answer, correct, transforms), flush=True)
    return i, rec


def main():
    parser = argparse.ArgumentParser(description='Debate v4: camera-frame agents + transform alignment')
    parser.add_argument('--model', type=str, default='gemini-3.5-flash')
    parser.add_argument('--samples', type=str, default='vsi_debate_strat_20.json')
    parser.add_argument('--output', default='results_debate4_strat20.json')
    parser.add_argument('--n', type=int, default=20)
    parser.add_argument('--agents', type=int, default=2)
    parser.add_argument('--rounds', type=int, default=2)
    parser.add_argument('--fuse-thresh', type=float, default=1.0, help='Union dedup threshold (grid cells)')
    parser.add_argument('--match-mode', choices=['greedy', 'hungarian'], default='greedy')
    parser.add_argument('--transform-prior', action='store_true', help='Use analytic camera-matrix transform prior')
    parser.add_argument('--confidence-gate', action='store_true', help='Skip B fusion when transform is unreliable')
    parser.add_argument('--gate-rmse', type=float, default=1.5)
    parser.add_argument('--sleep', type=float, default=1.0)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--resume', type=str, default=None)
    parser.add_argument('--dry-run', action='store_true')
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
