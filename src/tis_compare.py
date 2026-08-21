"""Shared library for the TIS baseline vs three-view comparison.

Handles question-category extraction, GT cognitive-map building from meta_info,
prediction parsing, map metrics, and small API/answer helpers.
"""
import base64
import ast
import json
import math
import os
import re
import time

META_DIR = os.environ.get(
    'TIS_META_DIR',
    os.path.join(
        os.path.expanduser('~'),
        'Documents', 'Thinking in Space\u590d\u73b0', 'thinking-in-space', 'data', 'meta_info',
    ),
)
DATASET_META = {
    'arkitscenes': 'arkitscenes_meta_info_val.json',
    'scannet': 'scannet_meta_info_val.json',
    'scannetpp': 'scannetpp_meta_info_val.json',
}
VIDEO_CACHE_DIR = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'vsibench')

# Load .env from project root before reading API keys.
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
if os.path.exists(_env_path):
    with open(_env_path, 'r', encoding='utf-8') as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith('#') and '=' in _line:
                _k, _v = _line.split('=', 1)
                os.environ.setdefault(_k.strip(), _v.strip())
GRID = 10

# Synonym groups shared by question mentions and meta category names.
SYNONYM_GROUPS = [
    ['tv', 'television', 'monitor screen'],
    ['washer', 'washing machine'],
    ['trash can', 'trash bin', 'bin', 'trash'],
    ['fridge', 'refrigerator'],
    ['couch', 'sofa'],
    ['ceiling light', 'ceiling lamp'],
    ['computer mouse', 'mouse'],
    ['table lamp', 'lamp'],
    ['cup', 'mug'],
    ['potted plant', 'plant'],
    ['bed frame', 'bed'],
    ['coat rack', 'coat hanger'],
]

_meta_cache = {}


def load_meta(dataset):
    if dataset not in _meta_cache:
        path = os.path.join(META_DIR, DATASET_META[dataset])
        with open(path, 'r', encoding='utf-8') as f:
            _meta_cache[dataset] = json.load(f)
    return _meta_cache[dataset]


def normalize_name(name):
    n = str(name).strip().lower().replace('_', ' ')
    n = re.sub(r'[.,;:!?\'\"]+$', '', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n


def match_category(name, dataset_categories):
    n = normalize_name(name)
    dataset_categories = [normalize_name(c) for c in dataset_categories]
    if n in dataset_categories:
        return n
    for group in SYNONYM_GROUPS:
        norm_group = [normalize_name(g) for g in group]
        if n in norm_group:
            for c in dataset_categories:
                if c in norm_group:
                    return c
    for c in dataset_categories:
        if n and (n in c or c in n):
            return c
    return None


def extract_categories(sample):
    """Extract question-mentioned categories from a VSI-Bench sample."""
    cats = set()
    q = sample['question']
    qtype = sample['question_type']
    if 'abs_distance' in qtype:
        m = re.search(r'between the (.+?) and the (.+?)\s*\(', q)
        if m:
            cats.add(normalize_name(m.group(1)))
            cats.add(normalize_name(m.group(2)))
    elif 'rel_distance' in qtype:
        m = re.search(r'closest to the (.+?)[?\.]', q)
        if m:
            cats.add(normalize_name(m.group(1)))
        for opt in (sample.get('options') or []):
            o = re.sub(r'^[A-D][\.\-\)]\s*', '', str(opt)).strip()
            if o:
                cats.add(normalize_name(o))
    elif 'counting' in qtype:
        m = re.search(r'How many (.+?)(?:\(s\))?s? (?:are|is) in', q)
        if m:
            cats.add(normalize_name(m.group(1)))
    elif 'room' in qtype:
        return []
    elif 'size' in qtype:
        ms = re.findall(r'of the ([a-zA-Z0-9 _-]+)(?:,| in|\?|$)', q, re.I)
        if ms:
            cats.add(normalize_name(ms[-1]))
    elif 'route' in qtype:
        m = re.search(r'beginning at the (.+?) and facing the (.+?)\.? You want to navigate to the (.+?)[?\.]', q, re.I)
        if m:
            cats.add(normalize_name(m.group(1)))
            cats.add(normalize_name(m.group(2)))
            cats.add(normalize_name(m.group(3)))
        else:
            for opt in (sample.get('options') or []):
                o = re.sub(r'^[A-D][\.\-\)]\s*', '', str(opt)).strip()
                if o:
                    cats.add(normalize_name(o))
    elif 'appearance' in qtype:
        for opt in (sample.get('options') or []):
            o = re.sub(r'^[A-D][\.\-\)]\s*', '', str(opt)).strip()
            for part in re.split(r'[,-]', o):
                p = normalize_name(part)
                if p:
                    cats.add(p)
    else:
        m = re.search(r'standing by the (.+?) and facing the (.+?), is the (.+?) to', q)
        if m:
            cats.add(normalize_name(m.group(1)))
            cats.add(normalize_name(m.group(2)))
            cats.add(normalize_name(m.group(3)))
    return sorted(c for c in cats if c)


def build_gt_map(sample, meta_scene):
    """Build GT three-view map (10x10 grid) restricted to question categories.

    Normalization uses the full scene extents with a 10% margin, matching the
    existing meta_to_cogmap convention. Returns (gt_map, matched_raw_names).
    """
    object_bbox = meta_scene['object_bbox']
    all_min = [float('inf')] * 3
    all_max = [float('-inf')] * 3
    for bboxes in object_bbox.values():
        for bb in bboxes:
            for i in range(3):
                all_min[i] = min(all_min[i], bb['min'][i])
                all_max[i] = max(all_max[i], bb['max'][i])
    margin = [0.1 * max(0.01, all_max[i] - all_min[i]) for i in range(3)]
    for i in range(3):
        all_min[i] -= margin[i]
        all_max[i] += margin[i]

    def to_grid(val, idx):
        rmin, rmax = all_min[idx], all_max[idx]
        if rmax == rmin:
            return GRID // 2
        return int(((val - rmin) / (rmax - rmin)) * (GRID - 1))

    dataset_cats = list(object_bbox.keys())
    categories = extract_categories(sample)
    matched = {}
    for raw in categories:
        mc = match_category(raw, dataset_cats)
        if mc:
            matched[raw] = mc

    range_x = all_max[0] - all_min[0]
    range_y = all_max[1] - all_min[1]
    range_z = all_max[2] - all_min[2]
    gt = {'top': {}, 'front': {}, 'side': {},
          'sizes': {'top': {}, 'front': {}, 'side': {}},
          'room': meta_scene.get('room_size')}
    for mc in sorted(set(matched.values())):
        for bb in object_bbox[mc]:
            c = bb['centroid']
            a = bb['axesLengths']
            gx = to_grid(c[0], 0)
            gy = to_grid(c[1], 1)
            gz = to_grid(c[2], 2)
            gw = max(1, int((a[0] / range_x) * (GRID - 1) + 0.5)) if range_x > 0 else 1
            gd = max(1, int((a[1] / range_y) * (GRID - 1) + 0.5)) if range_y > 0 else 1
            gh = max(1, int((a[2] / range_z) * (GRID - 1) + 0.5)) if range_z > 0 else 1
            gt['top'].setdefault(mc, []).append([gx, gy])
            gt['front'].setdefault(mc, []).append([gx, gz])
            gt['side'].setdefault(mc, []).append([gy, gz])
            gt['sizes']['top'].setdefault(mc, []).append([gw, gd])
            gt['sizes']['front'].setdefault(mc, []).append([gw, gh])
            gt['sizes']['side'].setdefault(mc, []).append([gd, gh])
    return gt, matched


def strip_backticks(text):
    bt = chr(96) * 3
    text = text.strip()
    if text.startswith(bt):
        text = text[len(bt):]
        nl = text.find(chr(10))
        text = text[nl + 1:] if nl >= 0 else text.lstrip()
    if text.endswith(bt):
        text = text[:-len(bt)]
    return text.strip()


def extract_json(text):
    """Extract first JSON object/array from mixed VLM output."""
    t = strip_backticks(text or '')
    if not t:
        return None
    try:
        return json.loads(t)
    except (json.JSONDecodeError, ValueError):
        pass
    for opener, closer in [('{', '}'), ('[', ']')]:
        start = t.find(opener)
        if start < 0:
            continue
        depth = 0
        end = -1
        in_str = False
        escape = False
        for i in range(start, len(t)):
            ch = t[i]
            if escape:
                escape = False
                continue
            if ch == '\\':
                escape = True
                continue
            if ch == '"':
                in_str = not in_str
                continue
            if in_str:
                continue
            if ch == opener:
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end >= 0:
            try:
                return json.loads(t[start:end + 1])
            except (json.JSONDecodeError, ValueError):
                pass
            try:
                return ast.literal_eval(t[start:end + 1])
            except (ValueError, SyntaxError):
                continue
    return None


def parse_pair(item):
    if isinstance(item, (list, tuple)) and len(item) >= 2:
        try:
            return [float(item[0]), float(item[1])]
        except (TypeError, ValueError):
            pass
    if isinstance(item, str):
        nums = re.findall(r'-?\d+\.?\d*', item)
        if len(nums) >= 2:
            return [float(nums[0]), float(nums[1])]
    return None


def normalize_sizes(view_data, view):
    """Extract per-instance sizes: top [w,d], front [w,h], side [d,h]."""
    out = {}
    if not isinstance(view_data, dict):
        return out
    for cat, items in view_data.items():
        if not isinstance(items, (list, tuple)):
            continue
        for it in items:
            if isinstance(it, (list, tuple)) and len(it) >= 4:
                try:
                    vals = [float(v) for v in it[:4]]
                except (TypeError, ValueError):
                    continue
                out.setdefault(normalize_name(cat), []).append(vals[2:4])
            elif isinstance(it, dict) and isinstance(it.get('size'), (list, tuple)) and len(it['size']) >= 2:
                try:
                    out.setdefault(normalize_name(it.get('name', cat)), []).append([float(it['size'][0]), float(it['size'][1])])
                except (TypeError, ValueError):
                    pass
    return out


def normalize_view(view_data, view):
    """Normalize one view into {category: [[c1, c2], ...]}."""
    if view_data is None:
        return {}
    out = {}
    if isinstance(view_data, dict):
        for cat, items in view_data.items():
            if not isinstance(items, (list, tuple)):
                continue
            pairs = []
            for it in items:
                p = parse_pair(it)
                if p:
                    pairs.append(p)
            if pairs:
                out[normalize_name(cat)] = pairs
        return out
    if isinstance(view_data, list):
        # Accept [{name, x, y|z}, ...] as a fallback.
        for o in view_data:
            if isinstance(o, dict) and 'name' in o:
                if view == 'top':
                    c1, c2 = o.get('x'), o.get('y')
                elif view == 'front':
                    c1, c2 = o.get('x'), o.get('z')
                else:
                    c1, c2 = o.get('y'), o.get('z')
                if c1 is not None and c2 is not None:
                    try:
                        out.setdefault(normalize_name(o['name']), []).append([float(c1), float(c2)])
                    except (TypeError, ValueError):
                        pass
        return out
    return {}


def parse_map(text, arm):
    data = extract_json(text)
    if data is None:
        return None
    if arm == 'baseline':
        room = data.get('room') if isinstance(data, dict) else None
        room_val = (float(room['area_m2'])
                    if isinstance(room, dict) and room.get('area_m2') is not None else None)
        return {'top': normalize_view(data, 'top'), 'front': {}, 'side': {},
                'sizes': {}, 'room': room_val}
    if not isinstance(data, dict):
        return None
    room = data.get('room')
    return {
        'top': normalize_view(data.get('top'), 'top'),
        'front': normalize_view(data.get('front'), 'front'),
        'side': normalize_view(data.get('side'), 'side'),
        'sizes': {
            'top': normalize_sizes(data.get('top'), 'top'),
            'front': normalize_sizes(data.get('front'), 'front'),
            'side': normalize_sizes(data.get('side'), 'side'),
        },
        'room': float(room['area_m2']) if isinstance(room, dict) and room.get('area_m2') is not None else None,
    }


def pair_distance(pa, pb):
    return math.hypot(pa[0] - pb[0], pa[1] - pb[1])


def min_pair_distance(list_a, list_b):
    best = float('inf')
    for a in list_a:
        for b in list_b:
            best = min(best, pair_distance(a, b))
    return best


def compute_metrics(gt, pred, arm):
    m = {
        'gt_instances': 0,
        'pred_instances': 0,
        'missed_instances': 0,
        'extra_instances': 0,
        'extra_categories': 0,
        'pairs': 0,
        'pairs_correct': 0,
        'bin_pairs': {},
        'bin_correct': {},
        'scale_ratios': [],
        'adjacent_pairs': 0,
        'adjacent_correct': 0,
        'cross_view_conflicts': 0,
        'cross_view_checked': 0,
        'cross_view_missing': 0,
        'height_pairs': 0,
        'height_correct': 0,
    }
    gt_top = gt['top']
    pred_top = pred['top']
    gt_cats = set(gt_top.keys())
    pred_cats = set(pred_top.keys())

    for cat in gt_cats:
        gt_n = len(gt_top[cat])
        pred_n = len(pred_top.get(cat, []))
        m['gt_instances'] += gt_n
        m['pred_instances'] += pred_n
        m['missed_instances'] += max(0, gt_n - pred_n)
        m['extra_instances'] += max(0, pred_n - gt_n)
    for cat in pred_cats - gt_cats:
        m['extra_instances'] += len(pred_top[cat])
        m['extra_categories'] += 1

    cats = sorted(gt_cats & pred_cats)
    for i in range(len(cats)):
        for j in range(i + 1, len(cats)):
            ca, cb = cats[i], cats[j]
            gt_d = min_pair_distance(gt_top[ca], gt_top[cb])
            pred_d = min_pair_distance(pred_top[ca], pred_top[cb])
            m['pairs'] += 1
            ok = abs(pred_d - gt_d) <= 1.0
            if ok:
                m['pairs_correct'] += 1
            bin_idx = min(7, int(math.floor(gt_d)))
            m['bin_pairs'][bin_idx] = m['bin_pairs'].get(bin_idx, 0) + 1
            if ok:
                m['bin_correct'][bin_idx] = m['bin_correct'].get(bin_idx, 0) + 1
            if gt_d > 0:
                m['scale_ratios'].append(pred_d / gt_d)
            if gt_d <= 1.0:
                m['adjacent_pairs'] += 1
                if ok:
                    m['adjacent_correct'] += 1

    if arm == 'threeview':
        for cat in gt_cats:
            gt_n = len(gt_top[cat])
            for view in ('top', 'front', 'side'):
                m['cross_view_missing'] += max(0, gt_n - len(pred[view].get(cat, [])))
            ft = sorted(pred['top'].get(cat, []), key=lambda p: p[0])
            ff = sorted(pred['front'].get(cat, []), key=lambda p: p[0])
            if len(ft) == len(ff):
                for a, b in zip(ft, ff):
                    m['cross_view_checked'] += 1
                    if abs(a[0] - b[0]) > 1.0:
                        m['cross_view_conflicts'] += 1
            st = sorted(pred['top'].get(cat, []), key=lambda p: p[1])
            ss = sorted(pred['side'].get(cat, []), key=lambda p: p[0])
            if len(st) == len(ss):
                for a, b in zip(st, ss):
                    m['cross_view_checked'] += 1
                    if abs(a[1] - b[0]) > 1.0:
                        m['cross_view_conflicts'] += 1
            sf = sorted(pred['front'].get(cat, []), key=lambda p: p[1])
            sd = sorted(pred['side'].get(cat, []), key=lambda p: p[1])
            if len(sf) == len(sd):
                for a, b in zip(sf, sd):
                    m['cross_view_checked'] += 1
                    if abs(a[1] - b[1]) > 1.0:
                        m['cross_view_conflicts'] += 1

        # Height ordering uses front-view z vs GT z, per category representative.
        for i in range(len(cats)):
            for j in range(i + 1, len(cats)):
                ca, cb = cats[i], cats[j]
                if not pred['front'].get(ca) or not pred['front'].get(cb):
                    continue
                if not gt['front'].get(ca) or not gt['front'].get(cb):
                    continue
                gz_a = gt['front'][ca][0][1]
                gz_b = gt['front'][cb][0][1]
                pz_a = pred['front'][ca][0][1]
                pz_b = pred['front'][cb][0][1]
                if abs(gz_a - gz_b) < 0.5:
                    continue
                m['height_pairs'] += 1
                if (pz_a - pz_b) * (gz_a - gz_b) > 0:
                    m['height_correct'] += 1
    return m


def error_tags(m, arm):
    tags = []
    if m['missed_instances'] > 0:
        tags.append('A1_miss')
    if m['extra_instances'] > 0:
        tags.append('A2_extra')
    if m['pairs'] > 0 and m['pairs_correct'] < m['pairs']:
        tags.append('B3_pair')
    ratios = [r for r in m['scale_ratios'] if r > 0]
    if ratios:
        low = sum(1 for r in ratios if r < 0.5) / len(ratios)
        high = sum(1 for r in ratios if r > 1.5) / len(ratios)
        if low > 0.3 or high > 0.3:
            tags.append('B4_scale')
    if m['adjacent_pairs'] > 0 and m['adjacent_correct'] < m['adjacent_pairs']:
        tags.append('B5_adjacent')
    if arm == 'threeview':
        if m['cross_view_conflicts'] > 0:
            tags.append('C6_conflict')
        if m['cross_view_missing'] > 0:
            tags.append('C7_missing')
        if m['height_pairs'] > 0 and m['height_correct'] < m['height_pairs']:
            tags.append('C8_height')
    return tags


# ============ API / answer helpers (mirrors run_vsibench) ============

MODEL_REGISTRY = {
    'gemini-3.5-flash': {
        'api_key': os.environ.get('BOYUE_API_KEY', ''),
        'base_url': 'http://35.220.164.252:3888/v1',
        'model': 'gemini-3.5-flash',
    },
}

SYSTEM_PROMPT = (
    'You are a spatial reasoning assistant. '
    'Always end your response with ANSWER: followed by your final answer. '
    'Do not include any text after ANSWER:'
)


_VIDEO_B64_CACHE = {}


def load_video_base64(video_path):
    if not os.path.exists(video_path):
        return None
    if video_path in _VIDEO_B64_CACHE:
        return _VIDEO_B64_CACHE[video_path]
    with open(video_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    _VIDEO_B64_CACHE[video_path] = b64
    return b64


def build_video_message(text, video_b64, mime_type='video/mp4'):
    return [
        {"type": "text", "text": text},
        {"type": "video_url", "video_url": {"url": "data:%s;base64,%s" % (mime_type, video_b64)}},
    ]


def call_api(model_name, messages, timeout=600.0, sleep_time=2.0):
    if model_name not in MODEL_REGISTRY:
        return None
    cfg = MODEL_REGISTRY[model_name]
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        t0 = time.time()
        print('[api] %s attempt %d start' % (model_name, attempt), flush=True)
        try:
            import openai
            client = openai.OpenAI(
                api_key=cfg['api_key'], base_url=cfg['base_url'], timeout=timeout,
            )
            resp = client.chat.completions.create(
                model=cfg['model'], messages=messages, temperature=0.1, max_tokens=4000,
            )
            content = resp.choices[0].message.content.strip()
            print('[api] ok in %.1fs' % (time.time() - t0), flush=True)
            return content.replace(chr(8722), '-')
        except Exception as e:
            err_str = str(e)
            print('[api] failed in %.1fs: %s' % (time.time() - t0, err_str), flush=True)
            if attempt < max_retries:
                print('[api] retrying in %.0fs (%s)' % (sleep_time, err_str[:120]), flush=True)
                time.sleep(sleep_time)
                continue
            return None
    return None


def extract_answer(text, question_type):
    if not text:
        return None
    text = text.strip()
    if any(kw in question_type for kw in ['direction', 'route', 'appearance', 'rel_distance']):
        marker = 'ANSWER:'
        if marker in text:
            after = text[text.index(marker) + len(marker):].strip()
            if after and after[0] in 'ABCD':
                return after[0]
        tail = text[-200:]
        for ch in tail:
            if ch in 'ABCD':
                return ch
        return None
    marker = 'ANSWER:'
    after = text[text.index(marker) + len(marker):].strip() if marker in text else text
    nums = re.findall(r'-?\d+\.?\d*', after.replace(',', ''))
    return nums[0] if nums else None


def evaluate_answer(extracted, ground_truth):
    if extracted is None or ground_truth is None:
        return False
    if ground_truth in 'ABCD':
        return extracted.strip().upper() == ground_truth.strip().upper()
    try:
        return abs(float(extracted) - float(ground_truth)) < 1e-6
    except (ValueError, TypeError):
        return extracted.strip().lower() == str(ground_truth).strip().lower()


def mra(pred, gt):
    try:
        pf, gf = float(pred), float(gt)
    except (TypeError, ValueError):
        return 0.0
    if gf == 0:
        return 0.0
    rel_err = abs(pf - gf) / gf
    thetas = [t / 100.0 for t in range(50, 100, 5)]
    return sum(1 for th in thetas if rel_err < 1 - th) / len(thetas)

def parse_counts(text):
    """Parse per-category instance counts from the count-stage output."""
    data = extract_json(text)
    if not isinstance(data, dict):
        return None
    out = {}
    for cat, v in data.items():
        try:
            n = int(float(v))
        except (TypeError, ValueError):
            continue
        if n >= 0:
            out[normalize_name(cat)] = n
    return out if out else None


def reconcile_views(pred):
    """Average conflicting coordinates across views; missing instances are kept when possible."""
    out = {'top': {}, 'front': {}, 'side': {}}
    cats = set(pred['top']) | set(pred['front']) | set(pred['side'])
    for cat in cats:
        t = sorted(pred['top'].get(cat, []), key=lambda p: (p[0], p[1]))
        f = sorted(pred['front'].get(cat, []), key=lambda p: (p[0], p[1]))
        s = sorted(pred['side'].get(cat, []), key=lambda p: (p[0], p[1]))
        n = max(len(t), len(f), len(s))
        for i in range(n):
            t_i = t[i] if i < len(t) else None
            f_i = f[i] if i < len(f) else None
            s_i = s[i] if i < len(s) else None
            if t_i is None and (f_i is None or s_i is None):
                continue
            if t_i is None:
                x, z = f_i[0], (f_i[1] + s_i[1]) / 2.0
                y = s_i[0]
            elif f_i is None and s_i is None:
                x, y, z = t_i[0], t_i[1], None
            elif f_i is None:
                x, y, z = t_i[0], s_i[0], s_i[1]
            elif s_i is None:
                x = (t_i[0] + f_i[0]) / 2.0
                y, z = t_i[1], f_i[1]
            else:
                x = (t_i[0] + f_i[0]) / 2.0
                y = (t_i[1] + s_i[0]) / 2.0
                z = (f_i[1] + s_i[1]) / 2.0
            if z is None:
                continue
            out['top'].setdefault(cat, []).append([round(x, 3), round(y, 3)])
            out['front'].setdefault(cat, []).append([round(x, 3), round(z, 3)])
            out['side'].setdefault(cat, []).append([round(y, 3), round(z, 3)])
    return out

def estimate_top_alignment(pred_top, gt_top, step_deg=2.0):
    """Best yaw (and optional x-mirror) mapping model top view onto GT top view."""
    def centroids(view):
        out = {}
        for cat, items in view.items():
            if items:
                out[normalize_name(cat)] = [
                    sum(p[0] for p in items) / len(items),
                    sum(p[1] for p in items) / len(items),
                ]
        return out
    p_pts = centroids(pred_top)
    g_pts = centroids(gt_top)
    cats = sorted(set(p_pts) & set(g_pts))
    if len(cats) < 2:
        return None
    best = None
    for mirror in (False, True):
        for deg in [d * step_deg for d in range(int(360 / step_deg))]:
            rad = math.radians(deg)
            c, s = math.cos(rad), math.sin(rad)
            err = 0.0
            for cat in cats:
                x, y = p_pts[cat]
                if mirror:
                    x = -x
                rx = c * x - s * y
                ry = s * x + c * y
                gx, gy = g_pts[cat]
                err += (rx - gx) ** 2 + (ry - gy) ** 2
            rmse = math.sqrt(err / max(1, len(cats)))
            if best is None or rmse < best[0] - 1e-9:
                best = (rmse, deg, mirror)
    return best

def apply_top_alignment(view, yaw_deg, mirror):
    """Rotate (and optionally mirror) a top-view dict into the GT frame."""
    rad = math.radians(yaw_deg)
    c, s = math.cos(rad), math.sin(rad)
    out = {}
    for cat, items in view.items():
        mapped = []
        for p in items:
            x, y = p[0], p[1]
            if mirror:
                x = -x
            mapped.append([round(c * x - s * y, 2), round(s * x + c * y, 2)])
        out[normalize_name(cat)] = mapped
    return out


def legacy_cogmap_objects(pred):
    """Flat per-view object list matching the original GitHub schema."""
    out = []
    axes = {'top_view': ('x', 'y'), 'front_view': ('x', 'z'), 'side_view': ('y', 'z')}
    view_keys = {'top_view': 'top', 'front_view': 'front', 'side_view': 'side'}
    for view_name in ('top_view', 'front_view', 'side_view'):
        v = (pred or {}).get(view_keys[view_name], {}) or {}
        for cat, items in v.items():
            for it in items or []:
                try:
                    a, b = float(it[0]), float(it[1])
                except (TypeError, ValueError, IndexError):
                    continue
                rec = {'view': view_name, 'name': cat, 'x': None, 'y': None, 'z': None}
                k1, k2 = axes[view_name]
                rec[k1], rec[k2] = a, b
                out.append(rec)
    return out
