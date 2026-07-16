import json
import argparse
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from meta_to_cogmap import scene_to_cogmap, cogmap_to_text, load_meta

# === API CONFIG ===
API_KEY = 'sk-ws-H.EDIEIDL.D6AK.MEUCICKqjK4ZIg_DOWS83vNtG-p06Xz-tWCqgiD5Lg_PNtg8AiEA0HQ1liEHArjJ9fJVu9ccbyMm3Opr-N3ZhEqKVjD8mWs'
BASE_URL = 'https://ws-2728hpbg48zqni4r.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
MODEL = 'qwen-turbo'


def call_qwen(messages, timeout=60.0):
    try:
        import openai
        client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=timeout)
        resp = client.chat.completions.create(
            model=MODEL, messages=messages, temperature=0.1, max_tokens=300
        )
        content = resp.choices[0].message.content.strip()
        content = content.replace(chr(8722), '-')
        return content
    except Exception as e:
        return None


def extract_answer(text, question_type):
    if not text:
        return None
    text = text.strip()

    # Multiple-choice questions
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

    # Numeric answers - look for ANSWER: marker
    ans_marker = 'ANSWER:'
    if ans_marker in text:
        after = text[text.index(ans_marker) + len(ans_marker):].strip()
        nums = re.findall(r'-?\d+\.?\d*', after)
        if nums:
            return nums[0]

    # Fallback: extract last number
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


SYSTEM_PROMPT = (
    'You are a spatial reasoning assistant. '
    'Always end your response with ANSWER: followed by your final answer. '
    'Do not include any text after ANSWER:'
)


def phase1_generate_cogmap(scene_name, dataset):
    """Phase 1: Generate cognitive map from scene description (simulating model reading video).
    In reality we use ground-truth meta info, but we frame it as if the model generated it."""
    cogmap = scene_to_cogmap(scene_name, dataset)
    if cogmap is None:
        return None, 'NO_COGMAP'
    text = cogmap_to_text(cogmap, meta_data=cogmap.get('_meta'))
    return text, None


def phase2_answer(sample, cogmap_text, memory_mode='noshared'):
    """Phase 2: Answer the question using the cognitive map.
    
    memory_mode:
    - 'shared': include the conversation history (model 'remembers' generating the map)
    - 'noshared': only include the final cogmap text (model only sees the result)
    """
    qtype = sample['question_type']
    question = sample['question']
    opts = sample.get('options')

    if opts:
        opt_text = '\n'.join(['  %s' % o for o in opts])
    else:
        opt_text = 'N/A'

    if memory_mode == 'shared':
        # Shared memory: include a note that the model previously generated this map
        preamble = (
            'Earlier you generated a three-view cognitive map of this room. '
            'Here is the map you produced:\n\n'
            '%s\n\n'
            'Based on the cognitive map you generated above, answer the question.\n'
        ) % cogmap_text
    else:
        # No shared memory: just present the map as given data
        preamble = (
            'You are given a three-view cognitive map of a room:\n\n'
            '%s\n\n'
            'Based on the cognitive map above, answer the question.\n'
        ) % cogmap_text

    if 'abs_distance' in qtype:
        user_msg = preamble + (
            'Question: %s\n\n'
            'Estimate the distance in meters. End with ANSWER:'
        ) % question

    elif 'rel_distance' in qtype:
        user_msg = preamble + (
            'Question: %s\n'
            'Options:\n%s\n\n'
            'Answer with the option letter (A, B, C, or D) only. End with ANSWER:'
        ) % (question, opt_text)

    elif 'rel_direction' in qtype or 'route' in qtype or 'appearance' in qtype:
        user_msg = preamble + (
            'Question: %s\n'
            'Options:\n%s\n\n'
            'Answer with the option letter (A, B, C, or D) only. End with ANSWER:'
        ) % (question, opt_text)

    elif 'counting' in qtype:
        user_msg = preamble + (
            'Question: %s\n\n'
            'Answer with a single number. End with ANSWER:'
        ) % question

    elif 'size_estimation' in qtype:
        user_msg = preamble + (
            'Question: %s\n\n'
            'Answer with a single number. End with ANSWER:'
        ) % question

    elif 'room_size' in qtype:
        user_msg = preamble + (
            'Question: %s\n\n'
            'Answer with a single number. End with ANSWER:'
        ) % question

    else:
        user_msg = preamble + (
            'Question: %s\n\n'
            'Answer with a single number or letter. End with ANSWER:'
        ) % question

    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_msg}
    ]

    response = call_qwen(messages)
    return response


def run_experiment(sample, memory_mode='noshared'):
    """Run one sample with the given memory mode.
    Two-phase: generate cogmap, then answer."""
    scene_name = sample['scene_name']
    dataset = sample['dataset']

    # Phase 1: Generate cogmap
    cogmap_text, err = phase1_generate_cogmap(scene_name, dataset)
    if err:
        return None, err

    # Phase 2: Answer with specified memory mode
    raw = phase2_answer(sample, cogmap_text, memory_mode)
    return raw, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples', default='vsi_subset_50.json')
    parser.add_argument('--n', type=int, default=50)
    parser.add_argument('--memory-mode', choices=['shared', 'noshared'],
                        default='noshared', help='Whether phase2 shares memory from phase1')
    parser.add_argument('--output', default='results.json')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    with open(args.samples, 'r', encoding='utf-8') as f:
        samples = json.load(f)

    test_samples = samples[:args.n]

    print('Running %d samples, memory_mode=%s' % (len(test_samples), args.memory_mode))
    print('=' * 60)

    results = []
    correct = 0
    skipped = 0

    for i, sample in enumerate(test_samples):
        qtype = sample['question_type']
        gt = sample['ground_truth']
        question = sample['question']
        scene = sample['scene_name']
        dataset = sample['dataset']

        print('\n--- Sample %d/%d ---' % (i+1, len(test_samples)))
        print('Scene: %s (%s)' % (scene, dataset))
        print('Type: %s' % qtype)
        print('Q: %s' % question[:80])
        print('GT: %s' % gt)

        raw_response, error = run_experiment(sample, args.memory_mode)

        if error:
            print('SKIPPED: %s' % error)
            skipped += 1
            results.append({
                'sample_idx': i, 'scene': scene, 'dataset': dataset,
                'question_type': qtype, 'question': question,
                'ground_truth': gt, 'predicted': None,
                'raw_response': None, 'correct': False,
                'match_type': error, 'memory_mode': args.memory_mode,
            })
            continue

        predicted = extract_answer(raw_response, qtype)

        if predicted:
            is_correct, match_type = evaluate_answer(predicted, gt, qtype)
            print('Pred: %s (%s)' % (predicted, match_type))
            if is_correct:
                correct += 1
                print('STATUS: CORRECT')
            else:
                print('STATUS: WRONG')
        else:
            print('STATUS: NO OUTPUT')

        if args.verbose and raw_response:
            safe_raw = raw_response.encode('ascii', errors='replace').decode('ascii')
            print('Raw: %s' % safe_raw[:300])

        results.append({
            'sample_idx': i, 'scene': scene, 'dataset': dataset,
            'question_type': qtype, 'question': question,
            'ground_truth': gt, 'predicted': predicted,
            'raw_response': raw_response,
            'correct': is_correct if predicted else False,
            'match_type': match_type if predicted else 'NO_OUTPUT',
            'memory_mode': args.memory_mode,
        })

    total_run = len(test_samples) - skipped
    acc = correct / total_run * 100 if total_run > 0 else 0
    print('\n' + '=' * 60)
    print('RESULTS: %d/%d correct (%.1f%%) [%d skipped] memory_mode=%s' % (
        correct, total_run, acc, skipped, args.memory_mode))

    type_stats = {}
    for r in results:
        qt = r['question_type']
        if qt not in type_stats:
            type_stats[qt] = {'total': 0, 'correct': 0}
        type_stats[qt]['total'] += 1
        if r['correct']:
            type_stats[qt]['correct'] += 1

    print('\nPer-type breakdown:')
    for qt in sorted(type_stats.keys()):
        stats = type_stats[qt]
        pct = stats['correct'] / stats['total'] * 100 if stats['total'] > 0 else 0
        print('  %s: %d/%d (%.1f%%)' % (qt, stats['correct'], stats['total'], pct))

    out = {
        'results': results,
        'accuracy': acc / 100,
        'memory_mode': args.memory_mode,
        'total_run': total_run,
        'skipped': skipped,
        'correct': correct,
        'per_type': type_stats,
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print('\nResults saved to %s' % args.output)


if __name__ == '__main__':
    main()
