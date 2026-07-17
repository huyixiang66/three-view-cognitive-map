import json
import argparse
import sys
import os
import re
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prompts_3pass import (
    TOP_VIEW_PROMPT,
    FRONT_VIEW_PROMPT_SHARED,
    SIDE_VIEW_PROMPT_SHARED,
    ANSWER_PROMPT_ABS_DISTANCE,
    ANSWER_PROMPT_REL_DISTANCE,
    ANSWER_PROMPT_REL_DIRECTION,
)

# === MODEL REGISTRY ===
MODEL_REGISTRY = {
    'deepseek-v3': {
        'provider': 'openai',
        'api_key': os.environ.get('WELLAPI_API_KEY', ''),
        'base_url': 'https://wellapi.ai/v1',
        'model': 'deepseek-v3',
    },
    'qwen-plus': {
        'provider': 'openai',
        'api_key': os.environ.get('DASHSCOPE_API_KEY', ''),
        'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        'model': 'qwen-plus',
    },
    'qwen-turbo': {
        'provider': 'openai',
        'api_key': os.environ.get('DASHSCOPE_API_KEY', ''),
        'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        'model': 'qwen-turbo',
    },
    'gpt-4o': {
        'provider': 'openai',
        'api_key': os.environ.get('OPENAI_API_KEY', ''),
        'base_url': 'https://api.openai.com/v1',
        'model': 'gpt-4o',
    },
    'gemini-3.5-flash': {
        'provider': 'openai',
        'api_key': os.environ.get('WELLAPI_API_KEY', ''),
        'base_url': 'https://wellapi.ai/v1',
        'model': 'gemini-3.5-flash',
    },
}


def call_api(model_name, messages, timeout=120.0, sleep_time=2.0):
    """Call LLM API with rate limit handling and multi-provider support.

    Uses a consistent OpenAI-compatible interface for all providers.
    Adds sleep_time delay between calls to avoid 429 Too Many Requests.
    """
    if sleep_time > 0:
        time.sleep(sleep_time)

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
            model=model, messages=messages, temperature=0.1, max_tokens=500
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


SYSTEM_PROMPT = (
    'You are a spatial reasoning assistant. '
    'Always end your response with ANSWER: followed by your final answer. '
    'Do not include any text after ANSWER:'
)


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
    """Extract JSON (array or object) from mixed VLM output.

    Strategy:
    1. Try direct json.loads
    2. Try bracket-matched [...] or {...} extraction
    3. Try extraction of inline {...} objects from bullet text
       (common with Gemini output pattern: '- name: `{"x":1,...}`')
    """
    t = text.strip()
    if not t:
        return None

    # Strategy 1: direct parse
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        pass

    # Strategy 2: bracket-matched extraction (handles code blocks)
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
            obj = json.loads(snippet)
            if isinstance(obj, dict):
                objs.append(obj)
        except json.JSONDecodeError:
            pass
        idx = end + 1

    if objs:
        return objs

    return None


def parse_cogmap(text):
    """Parse VLM output into standardized cogmap dict {gridSize, objects}.

    Robust to conversational text around JSON (common with Gemini, Qwen).
    """
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


def get_answer_prompt_template(question_type):
    if 'abs_distance' in question_type:
        return ANSWER_PROMPT_ABS_DISTANCE
    elif 'rel_distance' in question_type:
        return ANSWER_PROMPT_REL_DISTANCE
    else:
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
# Main Experiment Pipeline with True Memory Sharing
# ============================================================

def run_experiment_true_session(sample, mode, model_name, sleep_between_calls=3.0):
    """Run one sample using a true conversation session.

    In 'vlm_shared' mode, all steps are done in a single conversation history.
    In 'vlm_noshared' mode, Phase 1 is done in one session, and Phase 2 is done
    in a completely fresh session (only cogmap text + question as context).

    Both modes use 3-pass shared cogmap building (Pass 2 depends on Pass 1,
    Pass 3 depends on Pass 1+2 for axis alignment).
    """
    video_input = sample['scene_name']
    qtype = sample['question_type']
    question = sample['question']
    template = get_answer_prompt_template(qtype)

    # --- Phase 1: 3-Pass Shared CogMap Generation ---
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]

    # Pass 1: Top View
    prompt1 = TOP_VIEW_PROMPT.format(video_input=video_input)
    messages.append({'role': 'user', 'content': prompt1})
    resp1 = call_api(model_name, messages, sleep_time=sleep_between_calls)
    if not resp1:
        return resp1, 'NO_TOP_VIEW', None, 1
    messages.append({'role': 'assistant', 'content': resp1})

    top_parsed = parse_cogmap(resp1)
    if not top_parsed:
        return resp1, 'TOP_PARSE_FAIL', None, 1

    # Pass 2: Front View (builds on Top View x-axis)
    prompt2 = FRONT_VIEW_PROMPT_SHARED.format(
        video_input=video_input,
        top_view_result=json.dumps(top_parsed, ensure_ascii=False)
    )
    messages.append({'role': 'user', 'content': prompt2})
    resp2 = call_api(model_name, messages, sleep_time=sleep_between_calls)
    if not resp2:
        return resp2, 'NO_FRONT_VIEW', None, 2
    messages.append({'role': 'assistant', 'content': resp2})

    front_parsed = parse_cogmap(resp2)
    if not front_parsed:
        return resp2, 'FRONT_PARSE_FAIL', None, 2

    # Pass 3: Side View (builds on Top View y-axis + Front View z-axis)
    prompt3 = SIDE_VIEW_PROMPT_SHARED.format(
        video_input=video_input,
        top_view_result=json.dumps(top_parsed, ensure_ascii=False),
        front_view_result=json.dumps(front_parsed, ensure_ascii=False)
    )
    messages.append({'role': 'user', 'content': prompt3})
    resp3 = call_api(model_name, messages, sleep_time=sleep_between_calls)
    if not resp3:
        return resp3, 'NO_SIDE_VIEW', None, 3
    messages.append({'role': 'assistant', 'content': resp3})

    side_parsed = parse_cogmap(resp3)
    if not side_parsed:
        return resp3, 'SIDE_PARSE_FAIL', None, 3

    # Build cogmap text for display
    cogmap_dict = {
        'top_view': top_parsed,
        'front_view': front_parsed,
        'side_view': side_parsed
    }
    cogmap_text = build_cogmap_text(cogmap_dict)

    # --- Phase 2: Answer the Question ---
    if mode == 'vlm_shared':
        # True shared memory: append question to the ongoing multi-turn chat history
        # The model "remembers" the full conversation of building the map
        preamble = (
            'Earlier you built a three-view cognitive map of this room from the video. '
            'Based on the cognitive map you built above in our conversation, answer the question.\n'
        )
        user_msg = preamble + template.format(
            front_view='', top_view='', side_view='',
            question=question
        )
        messages.append({'role': 'user', 'content': user_msg})
        raw_answer = call_api(model_name, messages, sleep_time=sleep_between_calls)
        total_calls = 4

    elif mode == 'vlm_noshared':
        # True no shared memory: start a brand-new clean session
        # Only the final cogmap text is provided as context, no chat history
        new_messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
        preamble = (
            'You are given a three-view cognitive map of a room:\n\n'
            '%s\n\n'
            'Based on the cognitive map above, answer the question.\n'
        ) % cogmap_text
        user_msg = preamble + template.format(
            front_view='', top_view='', side_view='',
            question=question
        )
        new_messages.append({'role': 'user', 'content': user_msg})
        raw_answer = call_api(model_name, new_messages, sleep_time=sleep_between_calls)
        total_calls = 4

    else:
        return None, 'UNKNOWN_MODE', None, 0

    return raw_answer, None, cogmap_text, total_calls


# ============================================================
# Extract & evaluate
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
        if text[0] in 'ABCD':
            return text[0]
        m = re.match(r'^[A-D]', text)
        if m:
            return m.group()

    ans_marker = 'ANSWER:'
    if ans_marker in text:
        after = text[text.index(ans_marker) + len(ans_marker):].strip()
        nums = re.findall(r'-?\d+\.?\d*', after)
        if nums:
            return nums[0]

    nums = re.findall(r'-?\d+\.?\d*', text)
    if nums:
        return nums[-1]

    return text


def evaluate_answer(predicted, ground_truth, question_type):
    if predicted is None:
        return False, 'NO_OUTPUT'

    predicted = str(predicted).strip().upper()
    ground_truth = str(ground_truth).strip().upper()

    if predicted == ground_truth:
        return True, 'EXACT'

    if 'direction' in question_type or 'route' in question_type or 'appearance' in question_type:
        gt_clean = ground_truth.split('.')[0].split()[0]
        pred_clean = predicted.split('.')[0].split()[0]
        if pred_clean == gt_clean:
            return True, 'FUZZY'

    pred_nums = re.findall(r'-?\d+\.?\d*', predicted)
    gt_nums = re.findall(r'-?\d+\.?\d*', ground_truth)

    if pred_nums and gt_nums:
        try:
            pred_val = float(pred_nums[0])
            gt_val = float(gt_nums[0])
            if gt_val > 0:
                ratio = abs(pred_val - gt_val) / gt_val
                if ratio <= 0.3:
                    return True, 'CLOSE'
            elif abs(pred_val - gt_val) <= 0.5:
                return True, 'CLOSE'
        except ValueError:
            pass

    return False, 'MISMATCH'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples', default='vsi_subset_50.json')
    parser.add_argument('--n', type=int, default=50)
    parser.add_argument('--model', default='deepseek-v3',
                        help='Model name from MODEL_REGISTRY')
    parser.add_argument('--mode', choices=['vlm_shared', 'vlm_noshared'],
                        default='vlm_shared',
                        help='vlm_shared: True multi-turn conversation memory session. '
                             'vlm_noshared: Fresh conversation session for answering.')
    parser.add_argument('--output', default='results.json')
    parser.add_argument('--sleep', type=float, default=3.0,
                        help='Time to sleep between requests in seconds to avoid 429 rate limit')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    if args.model not in MODEL_REGISTRY:
        print(f'ERROR: Unknown model "{args.model}". Available: {list(MODEL_REGISTRY.keys())}')
        sys.exit(1)

    cfg = MODEL_REGISTRY[args.model]

    with open(args.samples, 'r', encoding='utf-8') as f:
        samples = json.load(f)

    test_samples = samples[:args.n]

    print(f'Running {len(test_samples)} samples')
    print(f'  model={args.model} ({cfg.get("model", "n/a")})')
    print(f'  mode={args.mode}')
    print(f'  sleep={args.sleep}s between API calls')
    print('=' * 60)

    results = []
    correct = 0
    skipped = 0
    total_calls = 0

    for i, sample in enumerate(test_samples):
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

        raw_response, error, cogmap_text, calls = run_experiment_true_session(
            sample, args.mode, args.model, sleep_between_calls=args.sleep
        )
        total_calls += calls

        if error:
            print(f'SKIPPED: {error}')
            skipped += 1
            results.append({
                'sample_idx': i, 'scene': scene, 'dataset': dataset,
                'question_type': qtype, 'question': question,
                'ground_truth': gt, 'predicted': None,
                'raw_response': raw_response, 'correct': False,
                'match_type': error, 'mode': args.mode,
                'model': args.model,
            })
            continue

        predicted = extract_answer(raw_response, qtype)

        if predicted:
            is_correct, match_type = evaluate_answer(predicted, gt, qtype)
            print(f'Pred: {predicted} ({match_type})')
            if is_correct:
                correct += 1
                print('STATUS: CORRECT')
            else:
                print('STATUS: WRONG')
        else:
            print('STATUS: NO OUTPUT')

        if args.verbose and raw_response:
            safe_raw = raw_response.encode('ascii', errors='replace').decode('ascii')
            print(f'Raw: {safe_raw[:300]}')
        if args.verbose and cogmap_text:
            safe_cog = cogmap_text.encode('ascii', errors='replace').decode('ascii')
            print(f'CogMap: {safe_cog[:200]}...')

        results.append({
            'sample_idx': i, 'scene': scene, 'dataset': dataset,
            'question_type': qtype, 'question': question,
            'ground_truth': gt, 'predicted': predicted,
            'raw_response': raw_response,
            'correct': is_correct if predicted else False,
            'match_type': match_type if predicted else 'NO_OUTPUT',
            'mode': args.mode,
            'model': args.model,
            'api_calls': calls,
        })

    total_run = len(test_samples) - skipped
    acc = correct / total_run * 100 if total_run > 0 else 0
    print(f'\n' + '=' * 60)
    print(f'RESULTS: {correct}/{total_run} correct ({acc:.1f}%) [{skipped} skipped]')
    print(f'model={args.model} mode={args.mode}')
    print(f'Total API calls: {total_calls}')

    type_stats = {}
    for r in results:
        qt = r['question_type']
        if qt not in type_stats:
            type_stats[qt] = {'total': 0, 'correct': 0}
        type_stats[qt]['total'] += 1
        if r['correct']:
            type_stats[qt]['correct'] += 1

    print(f'\nPer-type breakdown:')
    for qt in sorted(type_stats.keys()):
        stats = type_stats[qt]
        pct = stats['correct'] / stats['total'] * 100 if stats['total'] > 0 else 0
        print(f'  {qt}: {stats["correct"]}/{stats["total"]} ({pct:.1f}%)')

    out = {
        'results': results,
        'accuracy': acc / 100,
        'mode': args.mode,
        'model': args.model,
        'total_run': total_run,
        'skipped': skipped,
        'correct': correct,
        'total_api_calls': total_calls,
        'per_type': type_stats,
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f'\nResults saved to {args.output}')


if __name__ == '__main__':
    main()
