import json
import argparse
import sys
import os
import re
import numpy as np
import time
import base64
import io

# Load .env file from project root
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
if os.path.exists(_env_path):
    with open(_env_path, "r", encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

from prompts_3pass import (
    TOP_VIEW_PROMPT, FRONT_VIEW_PROMPT_SHARED, FRONT_VIEW_PROMPT_NOSHARED,
    SIDE_VIEW_PROMPT_SHARED, SIDE_VIEW_PROMPT_NOSHARED,
    SINGLE_PASS_THREE_VIEW_PROMPT,
    ANSWER_PROMPT_ABS_DISTANCE, ANSWER_PROMPT_REL_DISTANCE, ANSWER_PROMPT_REL_DIRECTION,
    ANSWER_PROMPT_ABS_DISTANCE_SELFCHECK, ANSWER_PROMPT_REL_DISTANCE_SELFCHECK, ANSWER_PROMPT_REL_DIRECTION_SELFCHECK,
    TOP_VIEW_PROMPT_TASK_AWARE, FRONT_VIEW_PROMPT_SHARED_TASK_AWARE, SIDE_VIEW_PROMPT_SHARED_TASK_AWARE,
)

# Add viz directory to path for grid_visualizer import
import sys
_viz_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'viz')
if _viz_dir not in sys.path:
    sys.path.insert(0, _viz_dir)
from matplotlib_visualizer import visualize_three_view

# ============================================================
# Model Registry — all now use OpenAI-compatible /v1/chat/completions
# ============================================================
MODEL_REGISTRY = {
    'gemini-3.5-flash': {
        'api_key': os.environ.get('BOYUE_API_KEY', ''),
        'base_url': 'http://35.220.164.252:3888/v1',
        'model': 'gemini-3.5-flash',
    },
}


# ============================================================
# API Call
# ============================================================
SYSTEM_PROMPT = (
    'You are a spatial reasoning assistant. '
    'Always end your response with ANSWER: followed by your final answer. '
    'Do not include any text after ANSWER:'
)

VIDEO_CACHE_DIR = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'vsibench')


def load_video_base64(video_path):
    """Load entire video file and return base64-encoded string."""
    if not os.path.exists(video_path):
        print(f'Video not found: {video_path}')
        return None
    with open(video_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def build_video_message(text, video_b64, mime_type='video/mp4'):
    """Build OpenAI-compatible message with video_url content.

    Returns [{"type": "text", ...}, {"type": "video_url", "video_url": {"url": "data:...;base64,..."}}]
    """
    return [
        {"type": "text", "text": text},
        {"type": "video_url", "video_url": {"url": f"data:{mime_type};base64,{video_b64}"}}
    ]


def call_api(model_name, messages, timeout=120.0, sleep_time=2.0):
    """Call LLM via OpenAI-compatible API with rate limit handling."""
    if model_name not in MODEL_REGISTRY:
        print(f'ERROR: Unknown model "{model_name}". Available: {list(MODEL_REGISTRY.keys())}')
        return None

    cfg = MODEL_REGISTRY[model_name]
    api_key = cfg['api_key']
    base_url = cfg['base_url']
    model = cfg['model']

    try:
        import openai
        client = openai.OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
        resp = client.chat.completions.create(
            model=model, messages=messages, temperature=0.1, max_tokens=4000
        )
        content = resp.choices[0].message.content.strip()
        content = content.replace(chr(8722), '-')
        return content

    except Exception as e:
        err_str = str(e)
        print(f'API call failed ({model_name}): {err_str}')
        if '429' in err_str or 'rate_limit' in err_str.lower():
            print('Detected rate limit. Sleeping for 15 seconds before retry...')
            time.sleep(15.0)
            try:
                return call_api(model_name, messages, timeout, sleep_time)
            except Exception as retry_e:
                print(f'Retry failed: {retry_e}')
        return None


# ============================================================
# Helpers: parse, extract, build text
# ============================================================
def strip_backticks(text):
    bt = chr(96) * 3
    text = text.strip()
    if text.startswith(bt):
        text = text[len(bt):]
        nl = text.find(chr(10))
        if nl >= 0:
            text = text[nl + 1:]
        else:
            text = text.lstrip()
    if text.endswith(bt):
        text = text[:-len(bt)]
    return text.strip()


def _extract_json(text):
    """Extract JSON (array or object) from mixed VLM output."""
    t = text.strip()
    if not t:
        return None

    # Strategy 1: direct parse
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        pass

    # Strategy 2: bracket-matched extraction
    for opener, closer in [("[", "]"), ("{", "}")]:
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
                escape = False; continue
            if ch == "\\":
                escape = True; continue
            if ch == '"':
                in_str = not in_str; continue
            if in_str:
                continue
            if ch == opener:
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end < 0:
            last_close = t.rfind(closer)
            if last_close > start:
                end = last_close
        if end >= 0:
            snippet = t[start:end + 1]
            try:
                return json.loads(snippet)
            except json.JSONDecodeError:
                continue

    # Strategy 3: extract inline {...} objects from bullet text
    objs = []
    idx = 0
    while True:
        start = t.find("{", idx)
        if start < 0:
            break
        depth = 0
        end = -1
        in_str = False
        escape = False
        for i in range(start, len(t)):
            ch = t[i]
            if escape:
                escape = False; continue
            if ch == "\\":
                escape = True; continue
            if ch == '"':
                in_str = not in_str; continue
            if in_str:
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end < 0:
            break
        snippet = t[start:end + 1]
        try:
            objs.append(json.loads(snippet))
        except json.JSONDecodeError:
            pass
        idx = end + 1

    if objs:
        return objs if len(objs) > 1 else objs[0]
    return None


def parse_cogmap(text):
    """Parse VLM output into standardized cogmap dict {gridSize, objects}."""
    text = strip_backticks(text)
    if not text:
        return None
    data = _extract_json(text)
    if data is None:
        return None
    if isinstance(data, dict) and 'objects' in data and 'gridSize' in data:
        return data
    if isinstance(data, list):
        return {'gridSize': 10, 'objects': data}
    return None


def extract_categories(sample):
    """Extract question-mentioned categories from a VSI-Bench sample."""
    def _norm(name):
        n = str(name).strip().lower().replace('_', ' ')
        n = re.sub(r"[.,;:!?'\"]+$", '', n)
        return n.strip()
    cats = set()
    q = sample['question']
    qtype = sample['question_type']
    if 'abs_distance' in qtype:
        m = re.search(r'between the (.+?) and the (.+?)\s*\(', q)
        if m:
            cats.add(_norm(m.group(1)))
            cats.add(_norm(m.group(2)))
    elif 'rel_distance' in qtype:
        m = re.search(r'closest to the (.+?)[?\.]', q)
        if m:
            cats.add(_norm(m.group(1)))
        for opt in (sample.get('options') or []):
            o = re.sub(r'^[A-D][\.\-\)]\s*', '', str(opt)).strip()
            if o:
                cats.add(_norm(o))
    else:
        m = re.search(r'standing by the (.+?) and facing the (.+?), is the (.+?) to', q)
        if m:
            cats.add(_norm(m.group(1)))
            cats.add(_norm(m.group(2)))
            cats.add(_norm(m.group(3)))
    return sorted(c for c in cats if c)


VIEW_KEY_MAP = {
    'top': 'top_view', 'front': 'front_view', 'side': 'side_view',
    'top_view': 'top_view', 'front_view': 'front_view', 'side_view': 'side_view',
}
VIEW_COORD_MAP = {
    'top_view': ('x', 'y'),
    'front_view': ('x', 'z'),
    'side_view': ('y', 'z'),
}


def _extract_singlepass_json(text):
    """Extract the first complete {...} object, ignoring earlier arrays/fences."""
    t = strip_backticks(text)
    start = t.find('{')
    if start < 0:
        return None
    depth = 0
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
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(t[start:i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def parse_singlepass_views(text):
    """Parse one-shot output {"top": {"cat": [(x, y), ...]}, ...} into cogmap_dict."""
    data = _extract_singlepass_json(text)
    if not isinstance(data, dict):
        return None
    out = {}
    for raw_key, view_key in VIEW_KEY_MAP.items():
        view = data.get(raw_key)
        if view is None:
            continue
        if not isinstance(view, dict):
            return None
        objects = []
        c1, c2 = VIEW_COORD_MAP[view_key]
        for name, coords in view.items():
            if not isinstance(coords, list):
                continue
            for coord in coords:
                if isinstance(coord, (list, tuple)) and len(coord) >= 2:
                    objects.append({'name': str(name).strip(), c1: coord[0], c2: coord[1]})
        out[view_key] = {'gridSize': 10, 'objects': objects}
    if len(out) < 3:
        return None
    return out


def get_answer_prompt_template(question_type):
    if 'abs_distance' in question_type:
        if USE_SELFCHECK:
            return ANSWER_PROMPT_ABS_DISTANCE_SELFCHECK
        return ANSWER_PROMPT_ABS_DISTANCE
    elif 'rel_distance' in question_type:
        if USE_SELFCHECK:
            return ANSWER_PROMPT_REL_DISTANCE_SELFCHECK
        return ANSWER_PROMPT_REL_DISTANCE
    else:
        if USE_SELFCHECK:
            return ANSWER_PROMPT_REL_DIRECTION_SELFCHECK
        return ANSWER_PROMPT_REL_DIRECTION


def build_cogmap_text(cogmap_parsed):
    """Convert 3-pass result dict to readable text."""
    lines = ['Three-View Cognitive Map (generated by model):', '']
    view_mapping = [
        ('top_view', 'TOP VIEW (x-y plane)'),
        ('front_view', 'FRONT VIEW (x-z plane)'),
        ('side_view', 'SIDE VIEW (y-z plane)'),
    ]
    for key, label in view_mapping:
        view_data = cogmap_parsed.get(key)
        if view_data is None:
            continue
        objects = view_data if isinstance(view_data, list) else view_data.get('objects', [])
        lines.append(label + ':')
        for obj in objects:
            if isinstance(obj, dict):
                name = obj.get('name', '?')
                x = obj.get('x', 0)
                y = obj.get('y', 0)
                z = obj.get('z', 0)
                size = obj.get('size', [])
                if 'x' in obj and 'y' in obj:
                    lines.append(f"  {name}: pos=({x},{y}), size={size}")
                elif 'x' in obj and 'z' in obj:
                    lines.append(f"  {name}: pos=({x},{z}), size={size}")
                elif 'y' in obj and 'z' in obj:
                    lines.append(f"  {name}: pos=({y},{z}), size={size}")
        lines.append('')
    return '\n'.join(lines)


# ============================================================
# Main Experiment Pipeline
# ============================================================


def _cogmap_to_viz(cogmap_dict):
    """Convert cogmap_dict to matplotlib PNG base64 image."""
    import io
    import matplotlib.pyplot as plt
    fig = visualize_three_view(cogmap_dict)
    if fig is None:
        return None
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')




def _extract_objects(question):
    """Extract objects from question: standing_obj, facing_obj, target_obj."""
    import re
    q = question.lower()
    m = re.search(r'standing by the (.+?) and facing the (.+?)[,.]\s+is the (.+?) ', q)
    if m:
        return m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
    # Fallback for rel_distance: try to extract from options
    return None, None, None


def _find_in_view(view_data, obj_name, cx='x', cy='y'):
    """Find object in a view by name. Returns (c1_coord, c2_coord)."""
    if isinstance(view_data, dict):
        items = view_data.get('objects', [])
    elif isinstance(view_data, list):
        items = view_data
    else:
        return None, None
    key = obj_name.strip().lower().replace(' ', '_').replace('-', '_')
    candidates = []
    for o in items:
        if isinstance(o, dict):
            okey = o.get('name', '').strip().lower().replace(' ', '_').replace('-', '_')
            if key == okey:
                return o.get(cx, None), o.get(cy, None)
            # Partial/substring match
            if key in okey or okey in key:
                candidates.append((o.get(cx, None), o.get(cy, None), abs(len(key) - len(okey))))
            # Semantic mapping for common mismatches
            semantic = {'ceiling_light': 'lamp', 'ceiling_lamp': 'lamp',
                'bookshelf': 'cabinet', 'refrigerator': 'fridge',
                'stool': 'chair', 'seat': 'chair', 'toilet': 'toilet'}
            if key in semantic:
                skey = semantic[key]
                if skey == okey:
                    return o.get(cx, None), o.get(cy, None)
    if candidates:
        candidates.sort(key=lambda c: c[2])
        return candidates[0][0], candidates[0][1]
    return None, None


def compute_spatial_facts(cogmap_dict, question):
    """Pre-compute spatial facts from cogmap. Returns formatted evidence string."""
    obj_a, obj_b, obj_t = _extract_objects(question)
    if not obj_a or not obj_b:
        return ''
    
    raw_top = cogmap_dict.get('top_view', [])
    x1, y1 = _find_in_view(raw_top, obj_a, 'x', 'y')
    x2, y2 = _find_in_view(raw_top, obj_b, 'x', 'y')
    x3, y3 = _find_in_view(raw_top, obj_t, 'x', 'y')
    
    facts = []
    
    # Top view coordinates
    if x1 is not None and x2 is not None:
        facts.append('[Spatial Facts from your cognitive map]')
        coord1_y = str(y1) if y1 is not None else '?'
        coord2_y = str(y2) if y2 is not None else '?'
        facts.append('- User at ' + obj_a + ' (' + str(x1) + ',' + coord1_y + '), facing ' + obj_b + ' (' + str(x2) + ',' + coord2_y + ')')
    
    # Compute left/right of target via cross product
    if all(v is not None for v in [x1, y1, x2, y2, x3, y3]):
        # Facing vector: (dx, dy) = obj_b - obj_a
        # Target vector: (tx, ty) = obj_t - obj_a
        dx = x2 - x1; dy = y2 - y1
        tx = x3 - x1; ty = y3 - y1
        cross = dx * ty - dy * tx
        dist = abs(cross) / (dx*dx + dy*dy)**0.5 if (dx*dx + dy*dy) > 0 else 0
        
        if abs(cross) < 1:
            dir_str = 'straight ahead or behind'
        elif cross > 0:
            dir_str = 'to the LEFT'
        else:
            dir_str = 'to the RIGHT'
        
        confidence = 'High'
        if dist < 1: confidence = 'Low (target close to facing line)'
        elif dist < 2: confidence = 'Medium'
        
        facts.append('- Computation: ' + obj_t + ' is ' + dir_str + ' when facing ' + obj_b + ' [Confidence: ' + confidence + ']')
    
    if facts:
        facts.append('[End]')
    return chr(10).join(facts)

def run_sample(sample, mode, model_name, sleep_between_calls=3.0, use_viz=False):
    """Run one sample using full video via video_url field.

    Video sent once in Pass 1; subsequent passes reuse conversation history.
    If use_viz=True, the answer phase uses visualizer output instead of raw JSON text.
    Both Gemini and other models go through OpenAI-compatible /v1/chat/completions.
    """
    scene = sample['scene_name']
    dataset = sample['dataset']
    qtype = sample['question_type']
    question = sample['question']
    template = get_answer_prompt_template(qtype)

    # Load full video as base64
    video_path = os.path.join(VIDEO_CACHE_DIR, dataset, scene + '.mp4')
    video_b64 = load_video_base64(video_path)
    if video_b64 is None:
        return None, 'NO_VIDEO', None, 0, None

    # --- Phase 1: 3-Pass CogMap ---
    # Video only sent in Pass 1; subsequent passes reuse conversation history
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    total_calls = 0

    # Pass 1: Top View
    if USE_TASKAWARE:
        prompt1 = TOP_VIEW_PROMPT_TASK_AWARE.format(question=question)
    else:
        prompt1 = TOP_VIEW_PROMPT.format()
    content1 = build_video_message(prompt1, video_b64)
    messages.append({'role': 'user', 'content': content1})
    resp1 = call_api(model_name, messages, sleep_time=sleep_between_calls)
    total_calls += 1
    if not resp1:
        return resp1, 'NO_TOP_VIEW', None, total_calls, None
    messages.append({'role': 'assistant', 'content': resp1})

    top_parsed = parse_cogmap(resp1)
    if not top_parsed:
        return resp1, 'TOP_PARSE_FAIL', None, total_calls, None

    # Pass 2: Front View
    if USE_TASKAWARE:
        prompt2 = FRONT_VIEW_PROMPT_SHARED_TASK_AWARE.format(
            question=question,
            top_view_result=json.dumps(top_parsed, ensure_ascii=False)
        )
    else:
        prompt2 = FRONT_VIEW_PROMPT_SHARED.format(
            top_view_result=json.dumps(top_parsed, ensure_ascii=False)
        )
    messages.append({'role': 'user', 'content': prompt2})
    resp2 = call_api(model_name, messages, sleep_time=sleep_between_calls)
    total_calls += 1
    if not resp2:
        return resp2, 'NO_FRONT_VIEW', None, total_calls, None
    messages.append({'role': 'assistant', 'content': resp2})

    front_parsed = parse_cogmap(resp2)
    if not front_parsed:
        return resp2, 'FRONT_PARSE_FAIL', None, total_calls, None

    # Pass 3: Side View
    if USE_TASKAWARE:
        prompt3 = SIDE_VIEW_PROMPT_SHARED_TASK_AWARE.format(
            question=question,
            top_view_result=json.dumps(top_parsed, ensure_ascii=False),
            front_view_result=json.dumps(front_parsed, ensure_ascii=False)
        )
    else:
        prompt3 = SIDE_VIEW_PROMPT_SHARED.format(
            top_view_result=json.dumps(top_parsed, ensure_ascii=False),
            front_view_result=json.dumps(front_parsed, ensure_ascii=False)
        )
    messages.append({'role': 'user', 'content': prompt3})
    resp3 = call_api(model_name, messages, sleep_time=sleep_between_calls)
    total_calls += 1
    if not resp3:
        return resp3, 'NO_SIDE_VIEW', None, total_calls, None
    messages.append({'role': 'assistant', 'content': resp3})

    side_parsed = parse_cogmap(resp3)
    if not side_parsed:
        return resp3, 'SIDE_PARSE_FAIL', None, total_calls, None

    # Build cogmap text
    cogmap_dict = {
        'top_view': top_parsed,
        'front_view': front_parsed,
        'side_view': side_parsed,
    }
    cogmap_text = build_cogmap_text(cogmap_dict)

    # --- Phase 2: Answer ---
    if mode == 'vlm_shared':
        opts = sample.get("options", [])
        options_text = chr(10).join(opts) if opts else ""
        if use_viz:
            viz_b64 = _cogmap_to_viz(cogmap_dict)
            if viz_b64:
                facts_text = compute_spatial_facts(cogmap_dict, question) if USE_FACTS else ''
                preamble = (
                    'Here is a visual representation of the cognitive map you built. '
                    'Based on the cognitive map you built above, answer the question.\n'
                )
                if facts_text:
                    preamble = facts_text + '\n\n' + preamble
                text_part = preamble + template.format(question=question, options=options_text)
                img_part = {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{viz_b64}"}}
                user_msg = [{"type": "text", "text": text_part}, img_part]
            else:
                # fallback: text-only
                preamble = (
                    'Based on the cognitive map you built above in our conversation, answer the question.\n'
                )
                user_msg = preamble + template.format(question=question, options=options_text)
        else:
            facts_text = compute_spatial_facts(cogmap_dict, question) if USE_FACTS else ''
            preamble = (
                'Earlier you built a three-view cognitive map of this room from the video. '
                'Based on the cognitive map you built above in our conversation, answer the question.\n'
            )
            if facts_text:
                preamble = facts_text + '\n\n' + preamble
            user_msg = preamble + template.format(question=question, options=options_text)
        messages.append({'role': 'user', 'content': user_msg})
        raw_answer = call_api(model_name, messages, sleep_time=sleep_between_calls)
        total_calls += 1

    elif mode == 'vlm_noshared':
        opts = sample.get("options", [])
        options_text = chr(10).join(opts) if opts else ""
        if use_viz:
            viz_b64 = _cogmap_to_viz(cogmap_dict)
            if viz_b64:
                preamble = (
                    'You are given a three-view cognitive map of a room (shown as an image below). '
                    'Based on the cognitive map, answer the question.\n'
                )
                text_part = preamble + template.format(question=question, options=options_text)
                img_part = {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{viz_b64}"}}
                user_msg = [{"type": "text", "text": text_part}, img_part]
            else:
                context = cogmap_text
                preamble = (
                    'You are given a three-view cognitive map of a room:\n\n'
                    '%s\n\n'
                    'Based on the cognitive map above, answer the question.\n'
                ) % context
                user_msg = preamble + template.format(question=question, options=options_text)
        else:
            context = cogmap_text
            preamble = (
                'You are given the video of a room and a three-view cognitive map of the same room:\n\n'
                '%s\n\n'
                'Based on the video and the cognitive map, answer the question.\n'
            ) % context
            user_msg = preamble + template.format(question=question, options=options_text)
        new_messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
        if use_viz:
            new_messages.append({'role': 'user', 'content': user_msg})
        else:
            new_messages.append({'role': 'user', 'content': build_video_message(user_msg, video_b64)})
        raw_answer = call_api(model_name, new_messages, sleep_time=sleep_between_calls)
        total_calls += 1

    elif mode == 'vlm_noshared_video':
        opts = sample.get("options", [])
        options_text = chr(10).join(opts) if opts else ""
        preamble = (
            'You have watched a video of a room and built a three-view cognitive map of it.\n\n'
            '%s\n\n'
            'Based on the cognitive map above, answer the question.\n'
        ) % cogmap_text
        user_msg = preamble + template.format(question=question, options=options_text)
        new_messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
        vid_content = build_video_message(user_msg, video_b64)
        new_messages.append({'role': 'user', 'content': vid_content})
        raw_answer = call_api(model_name, new_messages, sleep_time=sleep_between_calls)
        total_calls += 1

    else:
        return None, 'UNKNOWN_MODE', None, total_calls, None

    return raw_answer, None, cogmap_text, total_calls, cogmap_dict


def run_sample_singlepass(sample, model_name, sleep_between_calls=3.0, use_viz=False):
    """One-shot three-view: one call builds top/front/side, then answer in same session."""
    scene = sample['scene_name']
    dataset = sample['dataset']
    qtype = sample['question_type']
    question = sample['question']
    template = get_answer_prompt_template(qtype)

    video_path = os.path.join(VIDEO_CACHE_DIR, dataset, scene + '.mp4')
    video_b64 = load_video_base64(video_path)
    if video_b64 is None:
        return None, 'NO_VIDEO', None, 0, None

    categories = extract_categories(sample)
    categories_text = ', '.join(categories) if categories else 'all objects visible in the scene'
    prompt = SINGLE_PASS_THREE_VIEW_PROMPT.format(categories_of_interest=categories_text)
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    messages.append({'role': 'user', 'content': build_video_message(prompt, video_b64)})
    resp = call_api(model_name, messages, sleep_time=sleep_between_calls)
    total_calls = 1
    if not resp:
        return resp, 'NO_MAP', None, total_calls, None
    messages.append({'role': 'assistant', 'content': resp})

    cogmap_dict = parse_singlepass_views(resp)
    if not cogmap_dict:
        return resp, 'SINGLEPASS_PARSE_FAIL', None, total_calls, None
    cogmap_text = build_cogmap_text(cogmap_dict)

    opts = sample.get('options') or []
    options_text = chr(10).join(opts) if opts else ''
    if use_viz:
        viz_b64 = _cogmap_to_viz(cogmap_dict)
        if viz_b64:
            facts_text = compute_spatial_facts(cogmap_dict, question) if USE_FACTS else ''
            preamble = ('Here is a visual representation of the cognitive map you built. '
                        'Based on the cognitive map you built above, answer the question.\n')
            if facts_text:
                preamble = facts_text + '\n\n' + preamble
            text_part = preamble + template.format(question=question, options=options_text)
            img_part = {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{viz_b64}'}}
            messages.append({'role': 'user', 'content': [{'type': 'text', 'text': text_part}, img_part]})
        else:
            preamble = ('Based on the cognitive map you built above in our conversation, answer the question.\n')
            messages.append({'role': 'user', 'content': preamble + template.format(question=question, options=options_text)})
    else:
        facts_text = compute_spatial_facts(cogmap_dict, question) if USE_FACTS else ''
        preamble = ('Earlier you built a three-view cognitive map of this room from the video. '
                    'Based on the cognitive map you built above in our conversation, answer the question.\n')
        if facts_text:
            preamble = facts_text + '\n\n' + preamble
        messages.append({'role': 'user', 'content': preamble + template.format(question=question, options=options_text)})

    raw_answer = call_api(model_name, messages, sleep_time=sleep_between_calls)
    total_calls += 1
    return raw_answer, None, cogmap_text, total_calls, cogmap_dict


# ============================================================
# Extract & evaluate answers
# ============================================================

def extract_answer(text, question_type):
    if not text:
        return None
    text = text.strip()

    if any(kw in question_type for kw in ['direction', 'route', 'appearance', 'rel_distance']):
        ans_marker = 'ANSWER:'
        if ans_marker in text:
            after = text[text.index(ans_marker) + len(ans_marker):].strip()
            if after and after[0] in 'ABCD':
                return after[0]
        tail = text[-200:]
        for ch in tail:
            if ch in 'ABCD':
                return ch
        return None

    elif 'abs_distance' in question_type:
        ans_marker = 'ANSWER:'
        if ans_marker in text:
            after = text[text.index(ans_marker) + len(ans_marker):].strip()
        else:
            after = text
        nums = re.findall(r'-?\d+\.?\d*', after.replace(',', ''))
        if nums:
            return nums[0]
        return None

    else:
        ans_marker = 'ANSWER:'
        if ans_marker in text:
            after = text[text.index(ans_marker) + len(ans_marker):].strip()
        else:
            after = text
        nums = re.findall(r'-?\d+\.?\d*', after.replace(',', ''))
        if nums:
            return nums[0]
        return None


def evaluate_answer(extracted, ground_truth):
    if extracted is None or ground_truth is None:
        return False
    if ground_truth in 'ABCD':
        return extracted.strip().upper() == ground_truth.strip().upper()
    try:
        return abs(float(extracted) - float(ground_truth)) < 1e-6
    except (ValueError, TypeError):
        return extracted.strip().lower() == ground_truth.strip().lower()


# ============================================================
# Main Entry Point
# ============================================================


def run_sample_direct(sample, model_name, sleep_between_calls=3.0):
    """Direct video to answer baseline. No cogmap, just video + question."""
    scene = sample['scene_name']
    dataset = sample['dataset']
    qtype = sample['question_type']
    question = sample['question']
    template = get_answer_prompt_template(qtype)

    video_path = os.path.join(VIDEO_CACHE_DIR, dataset, scene + '.mp4')
    video_b64 = load_video_base64(video_path)
    if video_b64 is None:
        return None, 'NO_VIDEO', None, 0, None

    opts = sample.get('options', [])
    options_text = chr(10).join(opts) if opts else ''
    user_msg = template.format(question=question, options=options_text)

    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    content = build_video_message(user_msg, video_b64)
    messages.append({'role': 'user', 'content': content})

    raw_answer = call_api(model_name, messages, sleep_time=sleep_between_calls)
    if not raw_answer:
        return raw_answer, 'API_FAIL', None, 1
    return raw_answer, None, None, 1


def main():
    parser = argparse.ArgumentParser(description='VSI-Bench Three-View Cognitive Map Experiment')
    parser.add_argument('--model', type=str, default='gemini-3.5-flash',
                        help='Model name from MODEL_REGISTRY')
    parser.add_argument('--mode', choices=['vlm_shared', 'vlm_noshared', 'vlm_noshared_video', 'direct_video', 'vlm_singlepass'],
                        default='vlm_shared',
                        help='vlm_shared: True multi-turn conversation memory session. '
                             'vlm_noshared: Fresh conversation session for answering. '
                             'vlm_singlepass: one call builds top/front/side, answer in same session.')
    parser.add_argument('--samples', type=str, default='vsi_subset_50.json')
    parser.add_argument('--output', default='results.json')
    parser.add_argument('--n', type=int, default=50,
                        help='Number of samples to run')
    parser.add_argument('--sleep', type=float, default=3.0,
                        help='Time to sleep between requests in seconds to avoid 429 rate limit')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--viz', action='store_true',
                        help='Use grid visualizer output instead of raw JSON in answer phase')
    parser.add_argument('--taskaware', action='store_true',
                        help='Inject question into Pass 1-3 prompts to focus on task-relevant objects')
    parser.add_argument('--selfcheck', action='store_true',
                        help='Use self-check prompts that ask model to verify consistency')
    parser.add_argument('--facts', action='store_true',
                        help='Inject pre-computed spatial facts from cogmap into answer prompt')
    parser.add_argument('--resume', type=str, default=None,
                        help='Resume from a partial JSON results file')
    args = parser.parse_args()
    global USE_SELFCHECK, USE_FACTS, USE_TASKAWARE
    USE_SELFCHECK = args.selfcheck
    USE_FACTS = args.facts
    USE_TASKAWARE = args.taskaware

    if args.model not in MODEL_REGISTRY:
        print(f'ERROR: Unknown model "{args.model}". Available: {list(MODEL_REGISTRY.keys())}')
        sys.exit(1)

    cfg = MODEL_REGISTRY[args.model]

    samples_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.samples)
    with open(samples_path, 'r', encoding='utf-8') as f:
        samples = json.load(f)

    test_samples = samples[:args.n]

    print(f'Running {len(test_samples)} samples')
    print(f'  model={args.model} ({cfg.get("model", "n/a")})')
    print(f'  mode={args.mode}')
    print(f'  sleep={args.sleep}s between API calls')
    print(f'  [Full video via video_url]')
    print('=' * 60)

    results = []
    correct = 0
    skipped = 0
    total_calls = 0

    # Resume support
    resume_from = 0
    if args.resume and os.path.exists(args.resume):
        import json as _json
        existing = _json.load(open(args.resume, 'r', encoding='utf-8'))
        completed = [e for e in existing if '__summary__' not in e]
        results = completed.copy()
        correct = sum(1 for e in completed if e.get('correct'))
        skipped = sum(1 for e in completed if e.get('error'))
        total_calls = sum(e.get('api_calls', 0) for e in completed)
        resume_from = len(completed)
        print(f'Resuming from sample {resume_from}/{len(test_samples)} ({correct}/{resume_from - skipped} correct, {skipped} skipped)')

    for i, sample in enumerate(test_samples):
        if i < resume_from:
            continue
        qtype = sample['question_type']
        gt = sample['ground_truth']
        question = sample['question']
        scene = sample['scene_name']
        dataset = sample['dataset']

        print(f'\n--- Sample {i+1}/{len(test_samples)} ---')
        print(f'Scene: {scene} ({dataset})')
        print(f'Type: {qtype}')
        print(f'Q: {question[:80]}')
        print(f'GT: {gt}')

        if args.mode == 'direct_video':
            raw_response, error, cogmap_text, calls = run_sample_direct(
                sample, args.model, sleep_between_calls=args.sleep
            )
        elif args.mode == 'vlm_singlepass':
            raw_response, error, cogmap_text, calls, cogmap_dict = run_sample_singlepass(
                sample, args.model, sleep_between_calls=args.sleep, use_viz=args.viz
            )
        else:
            raw_response, error, cogmap_text, calls, cogmap_dict = run_sample(
                sample, args.mode, args.model, sleep_between_calls=args.sleep, use_viz=args.viz
            )
        total_calls += calls

        if error:
            print(f'SKIPPED: {error}')
            skipped += 1
            results.append({
                'sample_idx': i, 'scene': scene, 'dataset': dataset,
                'error': error, 'correct': False,
            })
            continue

        answer = extract_answer(raw_response, qtype)
        is_correct = evaluate_answer(answer, gt)

        if is_correct:
            correct += 1

        if args.verbose or not is_correct:
            print(f'Raw: {str(raw_response)[:200] if raw_response else "N/A"}')
            print(f'Extracted: {answer}')
            print(f'Expected: {gt}')
            print(f'{"CORRECT" if is_correct else "WRONG"}')
            if args.verbose and cogmap_text:
                try:
                    print(cogmap_text[:300])
                except UnicodeEncodeError:
                    print('[cogmap contains emoji - see result file]')

        cogmap_objects = []
        if cogmap_dict:
            for view_key in ['top_view', 'front_view', 'side_view']:
                raw = cogmap_dict.get(view_key, [])
                if isinstance(raw, dict):
                    items = raw.get('objects', [])
                elif isinstance(raw, list):
                    items = raw
                else:
                    items = []
                for o in items:
                    if isinstance(o, dict):
                        cogmap_objects.append({'view': view_key, 'name': o.get('name','?'),
                            'x': o.get('x', None), 'y': o.get('y', None), 'z': o.get('z', None)})
        results.append({
            'sample_idx': i, 'scene': scene, 'dataset': dataset,
            'question_type': qtype, 'question': question,
            'ground_truth': gt, 'extracted_answer': answer,
            'correct': is_correct, 'error': None,
            'api_calls': calls,
            'cogmap_objects': cogmap_objects,
        })

        # Incremental save every 5 samples
        if (i + 1) % 5 == 0:
            print(f'[Auto-save] {i+1}/{len(test_samples)} samples completed')
            _out_path = args.output.replace('.json', f'_partial_{i+1}.json')
            with open(_out_path, 'w', encoding='utf-8') as _f:
                json.dump(results, _f, indent=2, ensure_ascii=False)

    total_run = len(test_samples) - skipped
    acc = correct / total_run * 100 if total_run > 0 else 0
    print(f'\n' + '=' * 60)
    print(f'Results: {correct}/{total_run} correct ({acc:.1f}%)')
    print(f'Skipped: {skipped}')
    print(f'Total API calls: {total_calls}')
    print(f'Output: {args.output}')
    print('=' * 60)

    summary = {
        'model': args.model,
        'mode': args.mode,
        'total_samples': len(test_samples),
        'correct': correct,
        'total_run': total_run,
        'skipped': skipped,
        'accuracy_pct': round(acc, 1),
        'total_api_calls': total_calls,
    }
    results.append({'__summary__': summary})

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f'Done. Results saved to {args.output}')


if __name__ == '__main__':
    main()
