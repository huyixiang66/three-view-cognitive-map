import json
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prompts_3pass import (
    TOP_VIEW_PROMPT,
    FRONT_VIEW_PROMPT_SHARED,
    FRONT_VIEW_PROMPT_NOSHARED,
    SIDE_VIEW_PROMPT_SHARED,
    SIDE_VIEW_PROMPT_NOSHARED,
    ANSWER_PROMPT_ABS_DISTANCE,
    ANSWER_PROMPT_REL_DISTANCE,
    ANSWER_PROMPT_REL_DIRECTION,
    BASELINE_ABS_DISTANCE,
    BASELINE_REL_DISTANCE,
    BASELINE_REL_DIRECTION,
)


def load_samples(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_gemini_api(api_key):
    try:
        import openai
        client = openai.OpenAI(
            api_key=api_key,
            base_url='https://ws-2728hpbg48zqni4r.cn-beijing.maas.aliyuncs.com/compatible-mode/v1',
            timeout=30.0
        )
        resp = client.chat.completions.create(
            model='qwen-turbo',
            messages=[{'role':'user','content':'Say hello in one word.'}]
        )
        print(f'Qwen API OK: {resp.choices[0].message.content.strip()}')
        return True
    except ImportError:
        print('ERROR: openai not installed. Run: pip install openai')
        return False
    except Exception as e:
        print(f'ERROR: API failed: {e}')
        return False
    except Exception as e:
        print(f'ERROR: Gemini API failed: {e}')
        return False


def strip_backticks(text):
    bt = chr(96) * 3
    text = text.strip()
    # Remove opening fence: ` or `json or `python etc
    if text.startswith(bt):
        text = text[len(bt):]
        # Skip language hint like 'json', 'python'
        nl = text.find(chr(10))
        if nl >= 0:
            text = text[nl + 1:]
        else:
            text = text.lstrip()
    # Remove closing fence
    if text.endswith(bt):
        text = text[:-len(bt)]
    return text.strip()
def parse_cogmap(text):
    text = strip_backticks(text)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    # New format: {gridSize, objects}
    if isinstance(data, dict) and 'objects' in data and 'gridSize' in data:
        return data
    # Legacy format: list of objects
    if isinstance(data, list):
        return {'gridSize': 10, 'objects': data}
    return None
def load_samples(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_gemini_api(api_key):
    try:
        import openai
        client = openai.OpenAI(
            api_key=api_key,
            base_url='https://ws-2728hpbg48zqni4r.cn-beijing.maas.aliyuncs.com/compatible-mode/v1',
            timeout=30.0
        )
        resp = client.chat.completions.create(
            model='qwen-turbo',
            messages=[{'role':'user','content':'Say hello in one word.'}]
        )
        print(f'Qwen API OK: {resp.choices[0].message.content.strip()}')
        return True
    except ImportError:
        print('ERROR: openai not installed. Run: pip install openai')
        return False
    except Exception as e:
        print(f'ERROR: API failed: {e}')
        return False
    except Exception as e:
        print(f'ERROR: Gemini API failed: {e}')
        return False


def strip_backticks(text):
    bt = chr(96) * 3
    text = text.strip()
    # Remove opening fence: ` or `json or `python etc
    if text.startswith(bt):
        text = text[len(bt):]
        # Skip language hint like 'json', 'python'
        nl = text.find(chr(10))
        if nl >= 0:
            text = text[nl + 1:]
        else:
            text = text.lstrip()
    # Remove closing fence
    if text.endswith(bt):
        text = text[:-len(bt)]
    return text.strip()



def get_answer_prompt_template(question_type):
    if 'abs_distance' in question_type:
        return ANSWER_PROMPT_ABS_DISTANCE
    elif 'rel_distance' in question_type:
        return ANSWER_PROMPT_REL_DISTANCE
    else:
        return ANSWER_PROMPT_REL_DIRECTION


def get_baseline_prompt_template(question_type):
    if 'abs_distance' in question_type:
        return BASELINE_ABS_DISTANCE
    elif 'rel_distance' in question_type:
        return BASELINE_REL_DISTANCE
    else:
        return BASELINE_REL_DIRECTION


def run_baseline(model, video_input, question, question_type):
    template = get_baseline_prompt_template(question_type)
    prompt = template.format(video_input=video_input, question=question)
    resp = model.chat.completions.create(model="qwen-turbo", messages=[{"role":"user","content":prompt}]).choices[0].message.content
    return resp.strip()


def run_three_pass_shared(model, video_input, question, question_type):
    results = {}
    results['top_view'] = None
    results['front_view'] = None
    results['side_view'] = None
    results['answer'] = None
    results['errors'] = []

    # Pass 1: Top View
    prompt1 = TOP_VIEW_PROMPT.format(video_input=video_input)
    try:
        resp1 = model.chat.completions.create(model="qwen-turbo", messages=[{"role":"user","content":prompt1}]).choices[0].message.content
        top_data = parse_cogmap(resp1)
        if top_data is not None:
            results['top_view'] = json.dumps(top_data, ensure_ascii=False)
        else:
            results['errors'].append('TOP_PARSE_FAIL')
    except Exception as e:
        results['errors'].append(f'TOP_EXCEPTION: {e}')

    if results['top_view'] is None:
        results['answer'] = 'SKIP_NO_TOP_VIEW'
        return results

    # Pass 2: Front View (shared with top view x-axis)
    prompt2 = FRONT_VIEW_PROMPT_SHARED.format(
        video_input=video_input,
        top_view_result=results['top_view']
    )
    try:
        resp2 = model.chat.completions.create(model="qwen-turbo", messages=[{"role":"user","content":prompt2}]).choices[0].message.content
        front_data = parse_cogmap(resp2)
        if front_data is not None:
            results['front_view'] = json.dumps(front_data, ensure_ascii=False)
        else:
            results['errors'].append('FRONT_PARSE_FAIL')
    except Exception as e:
        results['errors'].append(f'FRONT_EXCEPTION: {e}')

    if results['front_view'] is None:
        results['answer'] = 'SKIP_NO_FRONT_VIEW'
        return results

    # Pass 3: Side View (shared with top view y-axis and front view z-axis)
    prompt3 = SIDE_VIEW_PROMPT_SHARED.format(
        video_input=video_input,
        top_view_result=results['top_view'],
        front_view_result=results['front_view']
    )
    try:
        resp3 = model.chat.completions.create(model="qwen-turbo", messages=[{"role":"user","content":prompt3}]).choices[0].message.content
        side_data = parse_cogmap(resp3)
        if side_data is not None:
            results['side_view'] = json.dumps(side_data, ensure_ascii=False)
        else:
            results['errors'].append('SIDE_PARSE_FAIL')
    except Exception as e:
        results['errors'].append(f'SIDE_EXCEPTION: {e}')

    if results['side_view'] is None:
        results['answer'] = 'SKIP_NO_SIDE_VIEW'
        return results

    # Answer step
    template = get_answer_prompt_template(question_type)
    prompt4 = template.format(
        front_view=results['front_view'],
        top_view=results['top_view'],
        side_view=results['side_view'],
        question=question
    )
    try:
        resp4 = model.chat.completions.create(model="qwen-turbo", messages=[{"role":"user","content":prompt4}]).choices[0].message.content
        results['answer'] = resp4.strip()
    except Exception as e:
        results['errors'].append(f'ANSWER_EXCEPTION: {e}')
        results['answer'] = None

    return results


def run_three_pass_noshared(model, video_input, question, question_type):
    results = {}
    results['top_view'] = None
    results['front_view'] = None
    results['side_view'] = None
    results['answer'] = None
    results['errors'] = []

    # Pass 1: Top View (same as shared)
    prompt1 = TOP_VIEW_PROMPT.format(video_input=video_input)
    try:
        resp1 = model.chat.completions.create(model="qwen-turbo", messages=[{"role":"user","content":prompt1}]).choices[0].message.content
        top_data = parse_cogmap(resp1)
        if top_data is not None:
            results['top_view'] = json.dumps(top_data, ensure_ascii=False)
        else:
            results['errors'].append('TOP_PARSE_FAIL')
    except Exception as e:
        results['errors'].append(f'TOP_EXCEPTION: {e}')

    if results['top_view'] is None:
        results['answer'] = 'SKIP_NO_TOP_VIEW'
        return results

    # Pass 2: Front View (NO shared top view info)
    prompt2 = FRONT_VIEW_PROMPT_NOSHARED.format(video_input=video_input)
    try:
        resp2 = model.chat.completions.create(model="qwen-turbo", messages=[{"role":"user","content":prompt2}]).choices[0].message.content
        front_data = parse_cogmap(resp2)
        if front_data is not None:
            results['front_view'] = json.dumps(front_data, ensure_ascii=False)
        else:
            results['errors'].append('FRONT_PARSE_FAIL')
    except Exception as e:
        results['errors'].append(f'FRONT_EXCEPTION: {e}')

    if results['front_view'] is None:
        results['answer'] = 'SKIP_NO_FRONT_VIEW'
        return results

    # Pass 3: Side View (NO shared top/front view info)
    prompt3 = SIDE_VIEW_PROMPT_NOSHARED.format(video_input=video_input)
    try:
        resp3 = model.chat.completions.create(model="qwen-turbo", messages=[{"role":"user","content":prompt3}]).choices[0].message.content
        side_data = parse_cogmap(resp3)
        if side_data is not None:
            results['side_view'] = json.dumps(side_data, ensure_ascii=False)
        else:
            results['errors'].append('SIDE_PARSE_FAIL')
    except Exception as e:
        results['errors'].append(f'SIDE_EXCEPTION: {e}')

    if results['side_view'] is None:
        results['answer'] = 'SKIP_NO_SIDE_VIEW'
        return results

    # Answer step
    template = get_answer_prompt_template(question_type)
    prompt4 = template.format(
        front_view=results['front_view'],
        top_view=results['top_view'],
        side_view=results['side_view'],
        question=question
    )
    try:
        resp4 = model.chat.completions.create(model="qwen-turbo", messages=[{"role":"user","content":prompt4}]).choices[0].message.content
        results['answer'] = resp4.strip()
    except Exception as e:
        results['errors'].append(f'ANSWER_EXCEPTION: {e}')
        results['answer'] = None

    return results


def evaluate_answer(predicted, ground_truth, question_type):
    if not predicted:
        return False, 'NO_OUTPUT'
    predicted = predicted.strip().upper()
    ground_truth = ground_truth.strip().upper()

    # Exact match first for all types
    if predicted == ground_truth:
        return True, 'MATCH'

    # Direction questions - allow prefix match
    if 'direction' in question_type:
        if predicted.startswith(ground_truth):
            return True, 'MATCH'
        return False, 'MISMATCH'

    # Distance questions - allow tolerance
    if 'distance' in question_type:
        try:
            pred_num = float(predicted.split()[0])
            gt_num = float(ground_truth)
            if gt_num > 0:
                ratio = abs(pred_num - gt_num) / gt_num
                if ratio <= 0.3:
                    return True, 'CLOSE'
            elif abs(pred_num - gt_num) <= 0.5:
                return True, 'CLOSE'
        except (ValueError, IndexError):
            pass

    return False, 'MISMATCH'
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-key', required=True)
    parser.add_argument('--samples', default='vsi_subset_50.json')
    parser.add_argument('--mode', choices=['baseline', '3pass_shared', '3pass_noshared'],
                        default='3pass_shared')
    parser.add_argument('--n', type=int, default=5)
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    if not test_gemini_api(args.api_key):
        sys.exit(1)

    import openai
    model = openai.OpenAI(
        api_key=args.api_key,
        base_url='https://ws-2728hpbg48zqni4r.cn-beijing.maas.aliyuncs.com/compatible-mode/v1',
        timeout=30.0
    )

    samples = load_samples(args.samples)
    test_samples = samples[:args.n]

    print(f'\\nTesting {len(test_samples)} samples in {args.mode} mode')
    print('=' * 60)

    results = []
    correct = 0
    total_calls = 0

    for i, s in enumerate(test_samples):
        scene = s['scene_name']
        qtype = s['question_type']
        question = s['question']
        gt = s['ground_truth']

        print(f'\\n--- Sample {i+1}/{len(test_samples)} ---')
        print(f'Type: {qtype}')
        print(f'Q: {question[:80]}...')
        print(f'GT: {gt}')

        if args.mode == 'baseline':
            predicted = run_baseline(model, scene, question, qtype)
            total_calls += 1
            cmap = None
        elif args.mode == '3pass_shared':
            r = run_three_pass_shared(model, scene, question, qtype)
            predicted = r['answer']
            cmap = r['top_view']
            total_calls += 4  # 3 view passes + 1 answer
        elif args.mode == '3pass_noshared':
            r = run_three_pass_noshared(model, scene, question, qtype)
            predicted = r['answer']
            cmap = r['top_view']
            total_calls += 4

        if predicted == 'SKIP_NO_TOP_VIEW' or predicted == 'SKIP_NO_FRONT_VIEW' or predicted == 'SKIP_NO_SIDE_VIEW':
            print(f'Status: SKIP ({predicted})')
            results.append({'sample': i, 'predicted': None, 'gt': gt, 'correct': False,
                            'error': predicted, 'api_calls': total_calls})
            continue

        if r.get('errors'):
            print(f'View errors: {r["errors"]}')

        if cmap and args.verbose:
            print(f'Top View: {cmap[:200]}...')

        if predicted:
            is_correct, match_type = evaluate_answer(predicted, gt, qtype)
            print(f'Predicted: {predicted}')
            status = 'CORRECT' if is_correct else 'WRONG'
            print(f'Status: {status} ({match_type})')
            if is_correct:
                correct += 1
            results.append({'sample': i, 'predicted': predicted, 'gt': gt, 'correct': is_correct,
                            'match': match_type, 'api_calls': total_calls})
        else:
            print('Status: NO OUTPUT')
            results.append({'sample': i, 'predicted': None, 'gt': gt, 'correct': False,
                            'error': 'NO_OUTPUT', 'api_calls': total_calls})

    print(f'\\n' + '=' * 60)
    acc = correct / len(test_samples) * 100 if test_samples else 0
    print(f'RESULTS: {correct}/{len(test_samples)} correct ({acc:.1f}%)')
    print(f'Mode: {args.mode}')
    print(f'Total API calls: {total_calls}')

    out_path = f'results_{args.mode}_{args.n}samples.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({
            'results': results,
            'accuracy': correct / len(test_samples) if test_samples else 0,
            'mode': args.mode,
            'total': len(test_samples),
            'api_calls': total_calls,
        }, f, indent=2, ensure_ascii=False)
    print(f'Results saved to {out_path}')


if __name__ == '__main__':
    main()
