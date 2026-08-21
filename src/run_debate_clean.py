# -*- coding: utf-8 -*-
"""Clean debate harness: unified prompt family + canonical cameras.

Strategy 1 (v2-style): three view agents build with the same camera-aware
prompt, then one structured shared-axis-offset critique round.
Strategy 2 (v5-style): same build prompt, then a fused-reference critique
round that uses the real 4x4 camera matrix (canonical cameras, so matrix
projection equals the standard axis convention).
The three arms used in the six-arm plan are named:
  ref_no_debate      (legacy strategy 6): independent reference build, no debate
  ref_simple_debate  (legacy strategy 7): + shared-axis-offset critique round
  ref_matrix_debate  (legacy strategy 5): + fused-reference matrix critique round
Legacy numeric strategies 1-7 are still accepted for compatibility.

All arms answer with the SAME protocol: a fresh conversation that receives
the video AND the three-view map text (video memory), using
run_clean_answer.MAP_PREAMBLE.
"""
import argparse
import json
import os
import sys
import glob
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np

from camera_utils import build_view_matrix
from run_clean_answer import MAP_PREAMBLE, build_answer_text, is_correct_ans, unified_map_text
from run_debate import FORMAT_HINTS, VIEWS, parse_view
from run_debate_v2 import axis_offsets
from run_tis_compare import answer_template, options_text
from tis_prompts import TIS_ROOM_SUFFIX
from tis_compare import (
    SYSTEM_PROMPT,
    VIDEO_CACHE_DIR,
    build_gt_map,
    build_video_message,
    call_api,
    compute_metrics,
    extract_answer,
    extract_categories,
    extract_json,
    load_meta,
    load_video_base64,
    legacy_cogmap_objects,
    reconcile_views,
    categories_text,
    estimate_appearance,
    estimate_room,
    estimate_route,
    extract_room,
)

SCENE_MIN = 0.0
SCENE_MAX = 9.0
CAM_MARGIN = 1.0

ARM_NAMES = {
    1: 'parallel_simple_debate',
    2: 'parallel_matrix_debate',
    3: 'sequential_matrix_debate',
    4: 'parallel_no_debate',
    5: 'ref_matrix_debate',
    6: 'ref_no_debate',
    7: 'ref_simple_debate',
}

STRATEGY_ALIASES = {
    'parallel_simple_debate': 1, 'parallel_matrix_debate': 2, 'sequential_matrix_debate': 3,
    'parallel_no_debate': 4, 'ref_matrix_debate': 5, 'ref_no_debate': 6, 'ref_simple_debate': 7,
    'matrix_debate': 5, 'simple_debate': 7, 'no_debate': 6,
}


def parse_strategy(value):
    if isinstance(value, int) or str(value).isdigit():
        v = int(value)
        if v in ARM_NAMES:
            return v
    name = str(value).strip().lower()
    if name in STRATEGY_ALIASES:
        return STRATEGY_ALIASES[name]
    raise argparse.ArgumentTypeError(
        'strategy must be one of %s or %s' % (
            sorted(ARM_NAMES), sorted(STRATEGY_ALIASES)))


def derive_cameras():
    center = np.array([(SCENE_MIN + SCENE_MAX) / 2.0] * 3, dtype=float)
    dist = (SCENE_MAX - SCENE_MIN) / 2.0 + CAM_MARGIN
    c = center.tolist()
    return {
        'top': {'name': 'TOP', 'position': (center + [0, 0, dist]).tolist(),
                'look_at': c, 'look_up': [0.0, 1.0, 0.0]},
        'front': {'name': 'FRONT', 'position': (center + [0, dist, 0]).tolist(),
                  'look_at': c, 'look_up': [0.0, 0.0, 1.0]},
        'side': {'name': 'SIDE', 'position': (center + [dist, 0, 0]).tolist(),
                 'look_at': c, 'look_up': [0.0, 0.0, 1.0]},
    }


CAMERAS = derive_cameras()
VIEW_AXES = {'top': (0, 1), 'front': (0, 2), 'side': (1, 2)}

CLEAN_BUILD_PROMPT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
Watch the video and build the {view_upper} VIEW cognitive map on a 10x10 grid.
We provide the categories to care about in this scene: {cats}. Focus ONLY on these categories. If a category contains multiple instances, include all of them.
Output ONLY JSON: {format_hint}"""

REF_BUILD_PROMPT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
Watch the video and build the {view_upper} VIEW cognitive map on a 10x10 grid.
Focus on the categories: {cats}. Include ALL instances.
Reference views built by other agents from the same video (use them ONLY for shared-axis consistency, do NOT copy them exactly):
{prev_views}
Now build YOUR OWN view from the video.
Output ONLY JSON: {format_hint}"""

REF_BUILD_PROMPT_STRICT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
Watch the video and build the {view_upper} VIEW cognitive map on a 10x10 grid.
Axis conventions (STRICT):
- TOP view: [x, y], where y is DEPTH in the room.
- FRONT view: [x, z], where z is HEIGHT above the floor (small values, typically 0-3).
- SIDE view: [y, z], where z is the SAME HEIGHT as in FRONT.
NEVER copy a depth coordinate into z. z must come from how high the object is in the video.
We provide the categories to care about in this scene: {cats}. Focus ONLY on these categories. If a category contains multiple instances, include all of them.
Reference views built by other agents from the same video (use them ONLY for shared-axis consistency, do NOT copy them exactly):
{prev_views}
Now build YOUR OWN view from the video.
Output ONLY JSON: {format_hint}"""

REF_BUILD_PROMPT_STRICT_V2 = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
Watch the video and build the {view_upper} VIEW cognitive map on a 10x10 grid.
Axis conventions (STRICT):
- TOP view: [x, y], where y is DEPTH in the room.
- FRONT view: [x, z], where z is HEIGHT above the floor; z spans the full 0-9 grid (0=floor, 9=ceiling).
- SIDE view: [y, z], where z is the SAME HEIGHT as in FRONT.
Objects that stand on the floor or are mounted high (door, window, furniture, wall objects) must have clearly non-zero z; do not compress everything to the bottom rows.
NEVER copy a depth coordinate into z. z must come from how high the object is in the video.
Focus on the categories: {cats}. Include ALL instances.
Reference views built by other agents from the same video (use them ONLY for shared-axis consistency, do NOT copy them exactly):
{prev_views}
Now build YOUR OWN view from the video.
Output ONLY JSON: {format_hint}"""

REF_BUILD_PROMPT_STRICT_V3 = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
Watch the video and build the {view_upper} VIEW cognitive map on a 10x10 grid.
Axis conventions (STRICT):
- TOP view: [x, y], where y is DEPTH in the room.
- FRONT view: [x, z], where z is HEIGHT above the floor; z spans the full 0-9 grid (0=floor, 9=ceiling).
- SIDE view: [y, z], where z is the SAME HEIGHT as in FRONT.
Objects that stand on the floor or are mounted high (door, window, furniture, wall objects) must have clearly non-zero z; do not compress everything to the bottom rows.
NEVER copy a depth coordinate into z. z must come from how high the object is in the video.
Preserve the exact LEFT-RIGHT and NEAR-FAR order from the video; do NOT mirror the room. If an object appears on the left in the video, it must stay on the left in the TOP view.
If the question gives a standing point and a facing point, locate both in the TOP view first, then check every other object's direction (left/right/back) against that facing direction.
Focus on the categories: {cats}. Include ALL instances.
Reference views built by other agents from the same video (use them ONLY for shared-axis consistency, do NOT copy them exactly):
{prev_views}
Now build YOUR OWN view from the video.
Output ONLY JSON: {format_hint}"""

REF_BUILD_PROMPT_STRICT_V4 = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
Watch the video and build the {view_upper} VIEW cognitive map on a 10x10 grid.
Axis conventions (STRICT):
- TOP view: [x, y], where y is DEPTH in the room.
- FRONT view: [x, z], where z is HEIGHT above the floor; z spans the full 0-9 grid (0=floor, 9=ceiling).
- SIDE view: [y, z], where z is the SAME HEIGHT as in FRONT.
Objects that stand on the floor or are mounted high (door, window, furniture, wall objects) must have clearly non-zero z; do not compress everything to the bottom rows.
NEVER copy a depth coordinate into z. z must come from how high the object is in the video.
Preserve the exact LEFT-RIGHT and NEAR-FAR order from the video; do NOT mirror the room. If an object appears on the left in the video, it must stay on the left in the TOP view.
If the question gives a standing point and a facing point, do a two-step self-check before finalizing TOP coordinates:
Step 1: place the standing object S and facing object F, then compute F_vec = F - S and T_vec = target - S in the TOP view.
Step 2: the target is LEFT of your facing direction if cross(F_vec, T_vec) = Fx*Ty - Fy*Tx is positive, RIGHT if negative, and BACK if the dot product F_vec . T_vec is negative. Adjust the target's coordinates until this matches the video.
Focus on the categories: {cats}. Include ALL instances.
Reference views built by other agents from the same video (use them ONLY for shared-axis consistency, do NOT copy them exactly):
{prev_views}
Now build YOUR OWN view from the video.
Output ONLY JSON: {format_hint}"""

R1_PROMPT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
Cross-view consistency checks found signed axis offsets (other - you):
- top.x - front.x median: {off_fx}
- top.y - side.y median: {off_sy}
- front.z - side.z median: {off_z}
Produce your FINAL {view_upper} VIEW directly. Keep every instance you are confident about.
Output ONLY JSON: {format_hint}

YOUR VIEW:
{my_view}

OTHER VIEWS:
{other_views}"""

R2_PROMPT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
A fused three-view map was re-projected into YOUR view below. The analytic transform from your view to the TOP frame is also given.
Produce your FINAL {view_upper} VIEW directly. Keep every instance you are confident about.
Output ONLY JSON: {format_hint}

YOUR VIEW:
{my_view}

FUSED PROJECTION (in your view):
{fused_proj}

TRANSFORM TO TOP FRAME:
{transform}"""

R2_FIXES_PROMPT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
Compare YOUR VIEW with the FUSED PROJECTION object by object.
For EVERY object where your coordinates differ from the fused projection by more than 0.5 grid cells on a shared axis, include a fix.
FRONT/SIDE agents: z is HEIGHT above the floor; NEVER copy depth (y) from TOP into z.
Output ONLY JSON: {{"fixes": [{{"category": "...", "index": 0, "instance": [x, y, w, h]}}, ...]}}
Use YOUR view's axis order. If nothing needs fixing, output {{"fixes": []}}.

YOUR VIEW:
{my_view}

FUSED PROJECTION (in your view):
{fused_proj}

TRANSFORM TO TOP FRAME:
{transform}"""

R2_STRICT_PROMPT = """You are Agent {name}. Your camera: position={position}, look_at={look_at}, look_up={look_up}.
A fused three-view map was re-projected into YOUR view below. The analytic transform from your view to the TOP frame is also given.
Your previous view may contain errors. Compare YOUR VIEW with the FUSED PROJECTION object by object:
- Add objects you missed.
- Remove objects you invented.
- Fix shared-axis coordinates so they agree with the fused projection.
- FRONT/SIDE agents: z is HEIGHT above the floor; NEVER copy depth (y) from TOP into z.
Produce your FINAL {view_upper} VIEW directly. Output ONLY JSON: {format_hint}

YOUR VIEW:
{my_view}

FUSED PROJECTION (in your view):
{fused_proj}

TRANSFORM TO TOP FRAME:
{transform}"""


BUILD_RETRY_HINT = ('\n\nYour previous output was not usable (invalid JSON or empty). '
                    'Output ONLY valid JSON with every instance you can see; do not output an empty view.')

def camera_text(view):
    c = CAMERAS[view]
    return {'position': c['position'], 'look_at': c['look_at'], 'look_up': c['look_up']}


def build_view(sample, view, model_name, sleep, dry_run=False, prev_views=None, retry_hint=None):
    cats = extract_categories(sample)
    cats_text = categories_text(sample)
    if dry_run:
        meta_scene = load_meta(sample['dataset']).get(sample['scene_name'], {})
        gt_map, _ = build_gt_map(sample, meta_scene)
        raw = json.dumps(gt_map.get(view, {}), ensure_ascii=False)
        return raw, [], None, cats
    video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
    video_b64 = load_video_base64(video_path)
    if video_b64 is None:
        return None, [], 'NO_VIDEO', cats
    if prev_views:
        prompt = REF_BUILD_PROMPT_STRICT.format(
            name=CAMERAS[view]['name'], view_upper=view.upper(),
            format_hint=FORMAT_HINTS[view], cats=cats_text,
            prev_views=json.dumps(prev_views, ensure_ascii=False), **camera_text(view))
    else:
        prompt = CLEAN_BUILD_PROMPT.format(
            name=CAMERAS[view]['name'], view_upper=view.upper(),
            format_hint=FORMAT_HINTS[view], cats=cats_text, **camera_text(view))
    if view == 'top':
        prompt += TIS_ROOM_SUFFIX
    if retry_hint:
        prompt += retry_hint
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': build_video_message(prompt, video_b64)}]
    raw = call_api(model_name, messages, sleep_time=sleep)
    if not raw:
        return raw, messages, 'MAP_API_FAIL', cats
    messages.append({'role': 'assistant', 'content': raw})
    return raw, messages, None, cats

def build_view_with_retry(sample, view, model_name, sleep, dry_run=False, prev_views=None):
    for attempt in range(2):
        raw, messages, err, cats = build_view(
            sample, view, model_name, sleep, dry_run=dry_run,
            prev_views=prev_views,
            retry_hint=BUILD_RETRY_HINT if attempt else None)
        if err:
            return raw, messages, err, cats
        parsed = parse_view(raw, view)
        if parsed is not None:
            if any(parsed['coords'].values()) or attempt == 1:
                return raw, messages, None, cats
    return raw, messages, 'BUILD_PARSE_FAIL', cats
def combined_map(parsed):
    return {
        'top': parsed['top']['coords'],
        'front': parsed['front']['coords'],
        'side': parsed['side']['coords'],
        'sizes': {v: parsed[v]['sizes'] for v in VIEWS},
        'room': None,
    }


def fused_reference(parsed):
    return reconcile_views({v: parsed[v]['coords'] for v in VIEWS})


def fused_3d(ref):
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


def project_fused_to_view(f3d, view):
    i, j = VIEW_AXES[view]
    out = {}
    for cat, pts in f3d.items():
        out[cat] = [[float(p[i]), float(p[j])] for p in pts]
    return out


def view_transform(j, i):
    ca, cb = CAMERAS[i], CAMERAS[j]
    MA = build_view_matrix(ca['position'], ca['look_at'], ca['look_up'], unity=True)
    MB = build_view_matrix(cb['position'], cb['look_at'], cb['look_up'], unity=True)
    T = MA @ np.linalg.inv(MB)
    return {'R': T[:3, :3].tolist(), 't': T[:3, 3].tolist(),
            'mirror': bool(np.linalg.det(T[:3, :3]) < 0), 'rmse': None}


def estimate_transforms(parsed):
    ref = fused_reference(parsed)
    f3d = fused_3d(ref)
    fused_proj = {v: project_fused_to_view(f3d, v) for v in VIEWS}
    analytic = {'top': None}
    for v in ('front', 'side'):
        analytic[v] = view_transform(v, 'top')
    return ref, analytic, fused_proj


def critique(agent, text, model_name, sleep, video_b64=None):
    content = build_video_message(text, video_b64) if video_b64 else text
    raw = call_api(model_name, [{'role': 'system', 'content': SYSTEM_PROMPT},
                                {'role': 'user', 'content': content}], sleep_time=sleep)
    return raw


def accept_view(raw, view):
    parsed = parse_view(raw, view)
    return parsed is not None and any(parsed['coords'].values()), parsed


def parse_fixes(raw):
    data = extract_json(raw)
    if not isinstance(data, dict):
        return None
    fixes = data.get('fixes')
    if not isinstance(fixes, list):
        return None
    out = []
    for f in fixes:
        if not isinstance(f, dict):
            return None
        cat, inst = f.get('category'), f.get('instance')
        if not isinstance(cat, str) or not isinstance(inst, list) or len(inst) < 2:
            return None
        out.append({'category': cat, 'index': f.get('index', 0), 'instance': inst})
    return out


def apply_fixes(raw_view, fixes, view):
    parsed = parse_view(raw_view, view)
    if parsed is None:
        return None
    coords = {k: [list(p) for p in v] for k, v in parsed['coords'].items()}
    sizes = {k: [list(s) for s in v] for k, v in parsed['sizes'].items()}
    for f in fixes:
        cat = f['category']
        try:
            idx = int(f.get('index', 0))
        except (TypeError, ValueError):
            idx = 0
        inst = [float(x) for x in f['instance'][:4]]
        if cat not in coords:
            coords[cat] = []
            sizes[cat] = []
        if idx < 0 or idx >= len(coords[cat]):
            coords[cat].append([inst[0], inst[1]])
            sizes[cat].append([inst[2] if len(inst) > 2 else 0.0, inst[3] if len(inst) > 3 else 0.0])
        else:
            coords[cat][idx][0] = inst[0]
            coords[cat][idx][1] = inst[1]
            if len(inst) > 2:
                sizes[cat][idx][0] = inst[2]
            if len(inst) > 3:
                sizes[cat][idx][1] = inst[3]
    out = {}
    for cat in coords:
        n = len(coords[cat])
        cat_sizes = sizes.get(cat, [])
        if len(cat_sizes) < n:
            cat_sizes = cat_sizes + [[1.0, 1.0]] * (n - len(cat_sizes))
            sizes[cat] = cat_sizes
        out[cat] = [[coords[cat][i][0], coords[cat][i][1],
                     cat_sizes[i][0], cat_sizes[i][1]] for i in range(n)]
    return json.dumps(out, ensure_ascii=False)

def answer_unified(sample, answer_map, model_name, sleep, dry_run=False, video_b64=None):
    opts = options_text(sample)
    text = build_answer_text(sample, answer_map)
    if dry_run:
        return 'ANSWER: %s' % sample['ground_truth'], None
    content = build_video_message(text, video_b64) if video_b64 else text
    raw = call_api(model_name, [{'role': 'system', 'content': SYSTEM_PROMPT},
                                {'role': 'user', 'content': content}], sleep_time=sleep)
    if not raw:
        return raw, 'ANSWER_API_FAIL'
    ans = extract_answer(raw, sample['question_type'])
    if ans is None:
        retry_text = ('Reply with ONLY the final answer as a single letter or number.\nQuestion: %s\n%s' %
                      (sample['question'], opts))
        retry_content = build_video_message(retry_text, video_b64) if video_b64 else retry_text
        raw2 = call_api(model_name, [{'role': 'system', 'content': SYSTEM_PROMPT},
                                     {'role': 'user', 'content': retry_content}], sleep_time=sleep)
        ans2 = extract_answer(raw2, sample['question_type']) if raw2 else None
        if ans2 is not None:
            raw, ans = raw2, ans2
    return raw, ans


def process_sample(i, sample, args):
    print('[%d] %s %s %s' % (i + 1, ARM_NAMES[args.strategy], sample['dataset'],
                             sample['scene_name']), flush=True)
    raw_views = {}
    parsed = {}
    cats = []
    prev_views = {}
    seq_messages = None
    video_b64 = None
    if not args.dry_run:
        video_path = os.path.join(VIDEO_CACHE_DIR, sample['dataset'], sample['scene_name'] + '.mp4')
        video_b64 = load_video_base64(video_path)

    for view in VIEWS:
        if args.strategy in (3, 5, 6, 7) and not args.dry_run:
            cats_text = categories_text(sample)
            prompt = CLEAN_BUILD_PROMPT.format(
                name=CAMERAS[view]['name'], view_upper=view.upper(),
                format_hint=FORMAT_HINTS[view], cats=cats_text, **camera_text(view))
            if view != 'top':
                prompt += ('\n\nUse the views you already built in this conversation '
                           '(shown above) as reference for the shared axes.')
            if args.strategy == 3:
                if seq_messages is None:
                    seq_messages = [{'role': 'system', 'content': SYSTEM_PROMPT},
                                    {'role': 'user', 'content': build_video_message(prompt, video_b64)}]
                else:
                    seq_messages.append({'role': 'user', 'content': prompt})
                raw = call_api(args.model, seq_messages, sleep_time=args.sleep)
                if raw:
                    seq_messages.append({'role': 'assistant', 'content': raw})
            else:
                # strategies 5/6/7: independent conversation per agent, previous views passed as reference text
                raw, messages, err, cats = build_view_with_retry(
                    sample, view, args.model, args.sleep, dry_run=args.dry_run, prev_views=prev_views or None)
                if err:
                    if err == 'BUILD_PARSE_FAIL':
                        return i, {'sample_idx': i, 'error': err, 'view': view, 'raw': raw, 'categories': cats}
                    return i, {'sample_idx': i, 'error': err, 'categories': cats}
                raw_views[view] = raw
                parsed[view] = parse_view(raw, view)
                prev_views[view] = parsed[view]['coords']
            if args.strategy == 3:
                if not raw:
                    return i, {'sample_idx': i, 'error': 'MAP_API_FAIL', 'categories': cats}
                parsed_v = parse_view(raw, view)
                if parsed_v is None:
                    return i, {'sample_idx': i, 'error': 'BUILD_PARSE_FAIL', 'view': view, 'raw': raw, 'categories': cats}
                raw_views[view] = raw
                parsed[view] = parsed_v
                prev_views[view] = parsed_v['coords']
        else:
            raw, messages, err, cats = build_view_with_retry(
                sample, view, args.model, args.sleep, dry_run=args.dry_run)
            if err:
                if err == 'BUILD_PARSE_FAIL':
                    return i, {'sample_idx': i, 'error': err, 'view': view, 'raw': raw, 'categories': cats}
                return i, {'sample_idx': i, 'error': err, 'categories': cats}
            raw_views[view] = raw
            parsed[view] = parse_view(raw, view)

    try:
        meta_scene = load_meta(sample['dataset']).get(sample['scene_name'], {})
    except Exception:
        meta_scene = {}
    if meta_scene:
        gt_map, matched = build_gt_map(sample, meta_scene)
    else:
        gt_map = {'top': {}, 'front': {}, 'side': {}, 'sizes': {}, 'room': None}
        matched = {}
    metrics_round0 = compute_metrics(gt_map, combined_map(parsed), 'threeview')

    finals = dict(raw_views)
    r2_debug = None
    round_metrics = {'round0': metrics_round0}
    if args.strategy in (1, 7):
        offsets = axis_offsets({v: parsed[v]['coords'] for v in VIEWS})
        for view in VIEWS:
            others = '\n\n'.join('%s VIEW:\n%s' % (v.upper(), json.dumps(parsed[v]['coords'], ensure_ascii=False))
                                 for v in VIEWS if v != view)
            text = R1_PROMPT.format(
                name=CAMERAS[view]['name'], view_upper=view.upper(),
                format_hint=FORMAT_HINTS[view], my_view=raw_views[view], other_views=others,
                off_fx=offsets['top_front_x'], off_sy=offsets['top_side_y'],
                off_z=offsets['front_side_z'], **camera_text(view))
            if not args.dry_run:
                raw = critique(view, text, args.model, args.sleep, video_b64=video_b64)
                ok, _ = accept_view(raw, view) if raw else (False, None)
                if ok:
                    finals[view] = raw
        final_parsed = {v: parse_view(finals[v], v) for v in VIEWS}
        round_metrics['round1'] = compute_metrics(gt_map, combined_map(final_parsed), 'threeview')
        answer_map = combined_map(final_parsed)
    elif args.strategy in (2, 3, 5):
        ref, analytic, fused_proj = estimate_transforms(parsed)
        r2_debug = {}
        for view in VIEWS:
            tf = analytic.get(view)
            if args.strategy == 5:
                text = R2_FIXES_PROMPT.format(
                    name=CAMERAS[view]['name'], view_upper=view.upper(),
                    my_view=raw_views[view],
                    fused_proj=json.dumps(fused_proj[view], ensure_ascii=False),
                    transform=json.dumps(tf, ensure_ascii=False) if tf else 'none',
                    **camera_text(view))
                if not args.dry_run:
                    raw = critique(view, text, args.model, args.sleep, video_b64=video_b64)
                    fixes = parse_fixes(raw) if raw else None
                    r2_debug[view] = {'raw': raw, 'n_fixes': len(fixes) if fixes is not None else None}
                    if fixes is not None:
                        new_raw = apply_fixes(raw_views[view], fixes, view)
                        if new_raw is not None and parse_view(new_raw, view) is not None:
                            finals[view] = new_raw
            else:
                text = R2_PROMPT.format(
                    name=CAMERAS[view]['name'], view_upper=view.upper(),
                    format_hint=FORMAT_HINTS[view], my_view=raw_views[view],
                    fused_proj=json.dumps(fused_proj[view], ensure_ascii=False),
                    transform=json.dumps(tf, ensure_ascii=False) if tf else 'none',
                    **camera_text(view))
                if not args.dry_run:
                    raw = critique(view, text, args.model, args.sleep, video_b64=video_b64)
                    ok, _ = accept_view(raw, view) if raw else (False, None)
                    if ok:
                        finals[view] = raw
        final_parsed = {v: parse_view(finals[v], v) for v in VIEWS}
        round_metrics['round2'] = compute_metrics(gt_map, combined_map(final_parsed), 'threeview')
        answer_map = combined_map(final_parsed)
    elif args.strategy in (4, 6):
        # No debate: merge all three views and answer directly (strategy 6 uses reference build).
        answer_map = combined_map(parsed)
        round_metrics['final'] = compute_metrics(gt_map, answer_map, 'threeview')

    metrics_final = compute_metrics(gt_map, answer_map, 'threeview')
    top_room = extract_room(finals.get('top'))
    if top_room is None:
        top_room = extract_room(raw_views.get('top'))
    extra_calls = 0
    if top_room is not None:
        answer_map['room'] = top_room
    elif args.strategy in (5, 6, 7) and ('room' in sample['question_type'] or 'size' in sample['question_type']):
        answer_map['room'] = estimate_room(
            sample, args.model, args.sleep, video_b64, dry_run=args.dry_run)
        extra_calls += 1
    if args.strategy in (5, 6, 7) and 'appearance' in sample['question_type']:
        answer_map['appearance_order'] = estimate_appearance(
            sample, args.model, args.sleep, video_b64, dry_run=args.dry_run)
        extra_calls += 1
    if args.strategy in (5, 6, 7) and 'route' in sample['question_type']:
        answer_map['route_action'] = estimate_route(
            sample, args.model, args.sleep, video_b64, dry_run=args.dry_run)
        extra_calls += 1
    round_metrics['final'] = metrics_final

    raw_answer, answer = answer_unified(
        sample, answer_map, args.model, args.sleep, dry_run=args.dry_run, video_b64=video_b64)
    if not raw_answer:
        return i, {'sample_idx': i, 'error': 'ANSWER_API_FAIL', 'categories': cats}
    correct = is_correct_ans(answer, sample)

    rec = {
        'sample_idx': i,
        'arm': 'debate_clean_strategy%d' % args.strategy,
        'arm_name': ARM_NAMES[args.strategy],
        'strategy': args.strategy,
        'mode': 'clean',
        'raw_map': json.dumps(answer_map, ensure_ascii=False),
        'cameras': CAMERAS,
        'scene': sample['scene_name'],
        'dataset': sample['dataset'],
        'question_type': sample['question_type'],
        'question': sample['question'],
        'ground_truth': sample['ground_truth'],
        'categories': cats,
        'categories_matched': sorted(set(matched.values())) if matched else [],
        'gt_map': gt_map,
        'raw_views': raw_views,
        'final_views': finals,
        'pred_map': answer_map,
        'fused_map': answer_map,
        'round_metrics': round_metrics,
        'map_metrics': metrics_final,
        'r2_debug': r2_debug,
        'raw_answer': raw_answer,
        'extracted_answer': answer,
        'correct': correct,
        'clean_answer': True,
        'cogmap_objects': legacy_cogmap_objects(answer_map),
        'api_calls': 3 + (3 if args.strategy in (1, 2, 3, 5, 7) else 0) + extra_calls + 1,
        'error': None,
    }
    if args.verbose:
        print('[%d] answer=%s correct=%s' % (i + 1, answer, correct), flush=True)
    return i, rec


def main():
    parser = argparse.ArgumentParser(description='Clean debate harness')
    parser.add_argument('--strategy', type=parse_strategy, required=True,
                        help='strategy name or legacy number (e.g. ref_no_debate / 6)')
    parser.add_argument('--model', type=str, default='gemini-3.5-flash')
    parser.add_argument('--samples', type=str, default='vsi_subset_200.json')
    parser.add_argument('--output', required=True)
    parser.add_argument('--n', type=int, default=200)
    parser.add_argument('--sleep', type=float, default=1.0)
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--resume', type=str, default=None)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--max-consecutive-fails', type=int, default=15)
    parser.add_argument('--max-fail-rate', type=float, default=0.6)
    args = parser.parse_args()

    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(line_buffering=True)

    samples_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.samples)
    with open(samples_path, encoding='utf-8') as f:
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
        with open(resume_path, encoding='utf-8') as f:
            existing = json.load(f)
        results = [r for r in existing if '__summary__' not in r]
        done = {r['sample_idx'] for r in results if not r.get('error')}
        print('Resuming %d records from %s' % (len(results), resume_path))
    else:
        done = set()

    lock = threading.Lock()
    completed = [len(done)]
    fail_streak = 0
    recent = deque(maxlen=20)
    stop_reason = None

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
                if rec.get('error'):
                    fail_streak += 1
                    recent.append(1)
                else:
                    fail_streak = 0
                    recent.append(0)
                if fail_streak >= args.max_consecutive_fails or (
                        len(recent) == recent.maxlen and sum(recent) / len(recent) >= args.max_fail_rate):
                    stop_reason = 'streak=%d window_rate=%.2f' % (fail_streak, sum(recent) / len(recent) if recent else 0)
                    for f in futures:
                        f.cancel()
                    break

    ok = [r for r in results if not r.get('error')]
    if stop_reason:
        print('[STOP] failure guard: %s' % stop_reason, flush=True)
    correct = sum(1 for r in ok if r.get('correct'))
    print('Done. records=%d ok=%d correct=%d (%.0f%%)' % (
        len(results), len(ok), correct, 100 * correct / len(ok) if ok else 0))
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
