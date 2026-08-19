# -*- coding: utf-8 -*-
"""Debate v5: three view agents (TOP / FRONT / SIDE) with camera frames.

Each agent owns a camera (position / look_at / look_up) and builds exactly one
view. Round 1 uses v2-style structured axis offsets to pull the views close.
Round 2 reconstructs a fused 3D reference from the corrected views, estimates
per-view rigid transforms into the TOP frame, re-projects the fused reference
into each agent's own view, and asks for a final corrected view.

The TOP agent's conversation is carried through build -> critiques -> final
fused map -> answer (--answer-mode shared), so debate is comparable with
threeview_3pass shared. --answer-mode noshared answers from a fresh
conversation using only the fused map.
"""
import argparse
import json
import math
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np

from camera_utils import estimate_rigid_transform
from run_debate import FORMAT_HINTS, VIEWS, cross_view_axes, parse_view
from run_debate_v2 import axis_offsets
from run_tis_compare import answer_template, numeric_ok, options_text
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
    reconcile_views,
)

SCENE_MIN = 0.0
SCENE_MAX = 9.0  # 10x10 grid, coordinates 0..9
CAM_MARGIN = 1.0
FRONT_YAW_DEG = -5.0
SIDE_YAW_DEG = 3.0


def derive_cameras():
    """Derive camera frames from the three-view axis convention.

    World axes: x=width, y=depth, z=height. TOP sees (x,y), FRONT sees (x,z),
    SIDE sees (y,z); each camera looks at the scene center from the missing
    axis. Position uses the largest possible scene interval: cameras sit just
    outside the [SCENE_MIN, SCENE_MAX] box so every view covers the whole
    scene. Orientation comes from the view definitions; replace with real
    pose estimates later if available.
    """
    center = np.array([(SCENE_MIN + SCENE_MAX) / 2.0] * 3, dtype=float)
    dist = (SCENE_MAX - SCENE_MIN) / 2.0 + CAM_MARGIN
    c = center.tolist()

    def rot_z(v, deg):
        a = math.radians(deg)
        cs, sn = math.cos(a), math.sin(a)
        return [v[0] * cs - v[1] * sn, v[0] * sn + v[1] * cs, v[2]]

    front_off = rot_z([0.0, dist, 0.0], FRONT_YAW_DEG)
    side_off = rot_z([dist, 0.0, 0.0], SIDE_YAW_DEG)
    return {
        'top': {
            'name': 'TOP',
            'position': (center + [0.0, 0.0, dist]).tolist(),
            'look_at': c, 'look_up': [0.0, 1.0, 0.0],
        },
        'front': {
            'name': 'FRONT',
            'position': (center + front_off).tolist(),
            'look_at': c, 'look_up': [0.0, 0.0, 1.0],
        },
        'side': {
            'name': 'SIDE',
            'position': (center + side_off).tolist(),
            'look_at': c, 'look_up': [0.0, 0.0, 1.0],
        },
    }


CAMERAS = derive_cameras()

BUILD_PROMPT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
Watch the video from YOUR camera frame and build the {view_upper} VIEW cognitive map on a 10x10 grid.
Focus on the categories: {cats}. Include ALL instances.
Output ONLY JSON: {format_hint}"""

CRITIQUE_R1_PROMPT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
The other agents built their own views with their own cameras. Cross-view consistency checks found signed axis offsets (other - you):
- top.x - front.x median: {off_fx}
- top.y - side.y median: {off_sy}
- front.z - side.z median: {off_z}
Produce your FINAL {view_upper} VIEW directly. Apply the offsets where they help, but do NOT delete instances to force equal counts: keep every instance you are confident about.
Output ONLY JSON: {format_hint}

YOUR VIEW:
{my_view}

OTHER VIEWS:
{other_views}"""

CRITIQUE_R2_PROMPT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
A fused three-view map was reconstructed from all agents' corrected views and re-projected into YOUR view below. The estimated transform from your view into the TOP reference frame is also given.
Produce your FINAL {view_upper} VIEW directly. Keep every instance you are confident about; do NOT delete instances to force equal counts.
Output ONLY JSON: {format_hint}

YOUR VIEW:
{my_view}

FUSED PROJECTION (in your view):
{fused_proj}

TRANSFORM TO TOP FRAME:
{transform}"""


def camera_text(view):
    c = CAMERAS[view]
    return {'position': c['position'], 'look_at': c['look_at'], 'look_up': c['look_up']}


def build_view(sample, view, model_name, sleep, dry_run=False):
    categories = extract_categories(sample)
    cats = ', '.join(categories) if categories else 'all objects visible in the scene'
    if dry_run:
        meta_scene = load_meta(sample['dataset']).get(sample['scene_name'], {})
        gt_map, _ = build_gt_map(sample, meta_scene)
        raw = json.dumps(gt_map.get(view, {}), ensure_ascii=False)
        return raw, [], None, categories
    video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
    video_b64 = load_video_base64(video_path)
    if video_b64 is None:
        return None, [], 'NO_VIDEO', categories
    cam = camera_text(view)
    prompt = BUILD_PROMPT.format(
        name=CAMERAS[view]['name'], view_upper=view.upper(), format_hint=FORMAT_HINTS[view],
        cats=cats, **cam)
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': build_video_message(prompt, video_b64)}]
    raw = call_api(model_name, messages, sleep_time=sleep)
    if not raw:
        return raw, messages, 'MAP_API_FAIL', categories
    messages.append({'role': 'assistant', 'content': raw})
    return raw, messages, None, categories


def r1_text(view, my_raw, parsed, offsets):
    cam = camera_text(view)
    others = '\n\n'.join(
        '%s VIEW:\n%s' % (v.upper(), json.dumps(parsed[v]['coords'], ensure_ascii=False))
        for v in VIEWS if v != view)
    return CRITIQUE_R1_PROMPT.format(
        name=CAMERAS[view]['name'], view_upper=view.upper(),
        format_hint=FORMAT_HINTS[view], my_view=my_raw, other_views=others,
        off_fx=offsets['top_front_x'], off_sy=offsets['top_side_y'],
        off_z=offsets['front_side_z'], **cam)


def r2_text(view, my_raw, fused_proj, transforms):
    cam = camera_text(view)
    tf = transforms.get(view)
    tf_text = json.dumps(tf, ensure_ascii=False) if tf else 'none'
    return CRITIQUE_R2_PROMPT.format(
        name=CAMERAS[view]['name'], view_upper=view.upper(),
        format_hint=FORMAT_HINTS[view], my_view=my_raw,
        fused_proj=json.dumps(fused_proj, ensure_ascii=False),
        transform=tf_text, **cam)


def call_critique(messages, text, view, model_name, sleep, video_b64=None, memory=False, dry_run=False):
    """Run one critique; returns raw text or None on API failure."""
    if dry_run:
        return None
    if memory:
        messages.append({'role': 'user', 'content': text})
        raw = call_api(model_name, messages, sleep_time=sleep)
        if raw:
            messages.append({'role': 'assistant', 'content': raw})
        return raw
    content = build_video_message(text, video_b64) if video_b64 else text
    raw = call_api(model_name, [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': content},
    ], sleep_time=sleep)
    return raw


def match_pairs(a, b):
    a = [list(p) for p in a]
    b = [list(p) for p in b]
    pairs = []
    while a and b:
        best = min(((math.dist(p, q), i, j)
                    for i, p in enumerate(a) for j, q in enumerate(b)), key=lambda x: x[0])
        _, i, j = best
        pairs.append((a[i], b[j]))
        a.pop(i)
        b.pop(j)
    return pairs


def fused_reference(parsed):
    views = {v: parsed[v]['coords'] for v in VIEWS}
    return reconcile_views(views)

def combined_map(parsed):
    return {
        'top': parsed['top']['coords'],
        'front': parsed['front']['coords'],
        'side': parsed['side']['coords'],
        'sizes': {v: parsed[v]['sizes'] for v in VIEWS},
        'room': None,
    }


def view_transform(j, i):
    """Analytic B(j)->A(i) transform from derived camera view matrices."""
    from camera_utils import build_view_matrix
    ca, cb = CAMERAS[i], CAMERAS[j]
    MA = build_view_matrix(ca['position'], ca['look_at'], ca['look_up'], unity=True)
    MB = build_view_matrix(cb['position'], cb['look_at'], cb['look_up'], unity=True)
    T = MA @ np.linalg.inv(MB)
    return {
        'R': T[:3, :3].tolist(), 't': T[:3, 3].tolist(),
        'mirror': bool(np.linalg.det(T[:3, :3]) < 0), 'rmse': None,
    }


def fused_3d(ref):
    """Build per-category 3D points from the reconciled three-view reference."""
    out = {}
    cats = set(ref['top']) | set(ref['front']) | set(ref['side'])
    for cat in cats:
        t = ref['top'].get(cat, [])
        f = ref['front'].get(cat, [])
        s = ref['side'].get(cat, [])
        n = max(len(t), len(f), len(s))
        pts = []
        for k in range(n):
            t_k = t[k] if k < len(t) else None
            f_k = f[k] if k < len(f) else None
            s_k = s[k] if k < len(s) else None
            if t_k is None and (f_k is None or s_k is None):
                continue
            x = t_k[0] if t_k is not None else f_k[0]
            y = t_k[1] if t_k is not None else s_k[0]
            z = f_k[1] if f_k is not None else s_k[1]
            if x is not None and y is not None and z is not None:
                pts.append([float(x), float(y), float(z)])
        if pts:
            out[cat] = pts
    return out


def project_fused_to_view(fused3d, view):
    """Project fused 3D points through the agent's real 4x4 view matrix.

    The scene box [SCENE_MIN, SCENE_MAX]^3 is projected through the camera and
    the resulting image coordinates are normalized to the 10x10 grid, so the
    projected view matches how the agent's own grid is defined.
    """
    from camera_utils import build_view_matrix
    cam = CAMERAS[view]
    M = build_view_matrix(cam['position'], cam['look_at'], cam['look_up'], unity=True)
    corners = [(x, y, z)
               for x in (SCENE_MIN, SCENE_MAX)
               for y in (SCENE_MIN, SCENE_MAX)
               for z in (SCENE_MIN, SCENE_MAX)]
    qs = [M @ np.array([x, y, z, 1.0]) for x, y, z in corners]
    min0, max0 = min(q[0] for q in qs), max(q[0] for q in qs)
    min1, max1 = min(q[1] for q in qs), max(q[1] for q in qs)
    out = {}
    for cat, pts in fused3d.items():
        proj = []
        for p in pts:
            q = M @ np.array([p[0], p[1], p[2], 1.0])
            u = (q[0] - min0) / (max0 - min0) * 9.0 if max0 > min0 else 4.5
            v = (q[1] - min1) / (max1 - min1) * 9.0 if max1 > min1 else 4.5
            proj.append([float(u), float(v)])
        if proj:
            out[cat] = proj
    return out


def estimate_view_transforms(parsed):
    """Return fused reference, instance-based 2D transforms, analytic 3D transforms,
    and fused 3D projected into each view."""
    ref = fused_reference(parsed)
    fused_proj = {v: project_fused_to_view(fused_3d(ref), v) for v in VIEWS}
    transforms = {'top': None}
    analytic = {'top': None}
    for v in ('front', 'side'):
        analytic[v] = view_transform(v, 'top')
        src, dst = [], []
        cats = set(parsed[v]['coords']) | set(ref[v])
        for cat in cats:
            for pa, pb in match_pairs(parsed[v]['coords'].get(cat, []), ref[v].get(cat, [])):
                src.append(pa)
                dst.append(pb)
        est = estimate_rigid_transform(np.array(src, dtype=float), np.array(dst, dtype=float)) \
            if len(src) >= 2 else None
        transforms[v] = None if est is None else {
            'R': est['R'].tolist(), 't': est['t'].tolist(),
            'rmse': est['rmse'], 'mirror': est['mirror'],
        }
    return ref, transforms, analytic, fused_proj


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
        video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
        video_b64 = load_video_base64(video_path)

    meta_scene = load_meta(sample['dataset']).get(sample['scene_name'], {})
    gt_map, matched = build_gt_map(sample, meta_scene)
    metrics_round0 = compute_metrics(gt_map, combined_map(parsed), 'threeview')

    offsets_before = axis_offsets({v: parsed[v]['coords'] for v in VIEWS})
    round1 = {}
    if getattr(args, 'skip_round1', False):
        round1 = dict(raw_views)
    else:
        for view in VIEWS:
            text = r1_text(view, raw_views[view], parsed, offsets_before)
            memory = (view == 'top' and messages_top and not args.dry_run)
            raw = call_critique(messages_top if memory else None, text, view,
                                args.model, args.sleep, video_b64=video_b64, memory=memory, dry_run=args.dry_run)
            if args.dry_run:
                raw = raw_views[view]
            parsed_r1 = parse_view(raw, view)
            if raw is None or parsed_r1 is None or not any(parsed_r1['coords'].values()):
                round1[view] = raw_views[view]
            else:
                round1[view] = raw

    round1_parsed = {v: parse_view(round1[v], v) for v in VIEWS}
    metrics_round1 = compute_metrics(gt_map, combined_map(round1_parsed), 'threeview')
    fused, transforms, analytic_transforms, fused_proj = estimate_view_transforms(round1_parsed)

    finals = {}
    for view in VIEWS:
        text = r2_text(view, round1[view], fused_proj[view], analytic_transforms)
        memory = (view == 'top' and messages_top and not args.dry_run)
        raw = call_critique(messages_top if memory else None, text, view,
                            args.model, args.sleep, video_b64=video_b64, memory=memory, dry_run=args.dry_run)
        if args.dry_run:
            raw = round1[view]
        parsed_r2 = parse_view(raw, view)
        if raw is None or parsed_r2 is None or not any(parsed_r2['coords'].values()):
            finals[view] = round1[view]
        else:
            finals[view] = raw

    final_parsed = {v: parse_view(finals[v], v) for v in VIEWS}
    round2_map = combined_map(final_parsed)
    metrics_round2 = compute_metrics(gt_map, round2_map, 'threeview')
    final_fused = fused_reference(final_parsed)
    fused_answer = {
        'top': final_fused['top'],
        'front': final_fused['front'],
        'side': final_fused['side'],
        'sizes': {v: final_parsed[v]['sizes'] for v in VIEWS},
        'room': None,
    }
    metrics_fused = compute_metrics(gt_map, fused_answer, 'threeview')
    answer_map = round2_map if args.answer_map == 'round2' else fused_answer
    axes = cross_view_axes(answer_map)
    metrics = metrics_round2 if args.answer_map in ('round2', 'both') else metrics_fused

    template = answer_template(sample['question_type'])
    opts = options_text(sample)

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
    answers_both = None
    answers_memory = None
    if args.answer_map == 'both':
        text_fused = ('Here is the final fused three-view cognitive map of the room (agents aligned + debate):\n%s\n\n' %
                      json.dumps(fused_answer, ensure_ascii=False)) + template.format(
                          question=sample['question'], options=opts)
        text_round2 = ('Here is the final corrected three-view cognitive map of the room (agents aligned + debate):\n%s\n\n' %
                       json.dumps(round2_map, ensure_ascii=False)) + template.format(
                           question=sample['question'], options=opts)
        conv_f = list(conv) if conv else None
        conv_r = list(conv) if conv else None
        raw_f, ans_f = answer_one(text_fused, conv_f)
        raw_r, ans_r = answer_one(text_round2, conv_r)
        if not raw_f or not raw_r:
            return i, {'sample_idx': i, 'error': 'ANSWER_API_FAIL', 'categories': cats}
        correct_f = is_correct_ans(ans_f)
        correct_r = is_correct_ans(ans_r)
        raw_answer, answer = raw_r, ans_r
        correct = correct_r
        answers_both = {
            'fused': {'raw_answer': raw_f, 'extracted_answer': ans_f, 'correct': correct_f},
            'round2': {'raw_answer': raw_r, 'extracted_answer': ans_r, 'correct': correct_r},
        }
    elif args.answer_mode == 'both':
        label = 'fused' if args.answer_map == 'fused' else 'corrected'
        text_part = ('Here is the final %s three-view cognitive map of the room (agents aligned + debate):\n%s\n\n' %
                     (label, json.dumps(answer_map, ensure_ascii=False))) + template.format(
                         question=sample['question'], options=opts)
        conv_shared = list(messages_top) if messages_top else None
        raw_s, ans_s = answer_one(text_part, conv_shared)
        raw_n, ans_n = answer_one(text_part, None)
        if not raw_s or not raw_n:
            return i, {'sample_idx': i, 'error': 'ANSWER_API_FAIL', 'categories': cats}
        correct_s = is_correct_ans(ans_s)
        correct_n = is_correct_ans(ans_n)
        raw_answer, answer = raw_s, ans_s
        correct = correct_s
        answers_memory = {
            'shared': {'raw_answer': raw_s, 'extracted_answer': ans_s, 'correct': correct_s},
            'noshared': {'raw_answer': raw_n, 'extracted_answer': ans_n, 'correct': correct_n},
        }
    else:
        label = 'fused' if args.answer_map == 'fused' else 'corrected'
        text_part = ('Here is the final %s three-view cognitive map of the room (agents aligned + debate):\n%s\n\n' %
                     (label, json.dumps(answer_map, ensure_ascii=False))) + template.format(
                         question=sample['question'], options=opts)
        raw_answer, answer = answer_one(text_part, conv)
        if not raw_answer:
            return i, {'sample_idx': i, 'error': 'ANSWER_API_FAIL', 'categories': cats}
        correct = is_correct_ans(answer)

    qt = sample['question_type']

    rec = {
        'sample_idx': i,
        'arm': 'debate5',
        'answer_mode': args.answer_mode,
        'answer_map_type': args.answer_map,
        'skip_round1': bool(getattr(args, 'skip_round1', False)),
        'agents': len(VIEWS),
        'cameras': CAMERAS,
        'camera_perturb': {'front_yaw_deg': FRONT_YAW_DEG, 'side_yaw_deg': SIDE_YAW_DEG},
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
        'offsets_before': offsets_before,
        'transforms_round2': transforms,
        'transforms_analytic': analytic_transforms,
        'fused_map': answer_map,
        'pred_map': answer_map,
        'cross_view_axes': axes,
        'map_metrics': metrics,
        'metrics_fused': metrics_fused,
        'metrics_round2': metrics_round2,
        'round_metrics': {
            'round0': metrics_round0,
            'round1': metrics_round1,
            'round2': metrics_round2,
            'final': metrics,
        },
        'raw_answer': raw_answer,
        'extracted_answer': answer,
        'answers_both': answers_both,
        'answers_memory': answers_memory,
        'correct': correct,
        'error': None,
    }
    if args.verbose:
        print('[%d] answer=%s correct=%s offsets=%s' % (
            i + 1, answer, correct, offsets_before), flush=True)
    return i, rec


def main():
    parser = argparse.ArgumentParser(description='Debate v5: three view agents + camera alignment')
    parser.add_argument('--model', type=str, default='gemini-3.5-flash')
    parser.add_argument('--samples', type=str, default='vsi_debate_strat_20.json')
    parser.add_argument('--output', default='results_debate5_strat20.json')
    parser.add_argument('--n', type=int, default=20)
    parser.add_argument('--answer-mode', choices=['shared', 'noshared', 'both'], default='shared')
    parser.add_argument('--answer-map', choices=['fused', 'round2', 'both'], default='round2')
    parser.add_argument('--skip-round1', action='store_true', help='Skip round1 structured critique')
    parser.add_argument('--sleep', type=float, default=1.0)
    parser.add_argument('--workers', type=int, default=4)
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
