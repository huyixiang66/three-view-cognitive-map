import argparse
import base64
import json
import os
import sys
import time

"""MMSI-Video-Bench runner.

Reference repo: https://github.com/InternRobotics/MMSI-Video-Bench
Paper: MMSI-Video-Bench: A Holistic Benchmark for Video-Based Spatial Intelligence
(arXiv 2512.10863). Dataset: https://huggingface.co/datasets/rbler/MMSI-Video-Bench

This runner follows the official native codebase path:
- loads mmsivideo.json from --data-root;
- samples frames proportionally (Uniform-50 default, Sufficient-Coverage option);
- assembles system_prompt + task_prompt + user_prompt + format_prompt exactly as
  the official dataset.py, and converts <video> placeholders into per-frame
  <image> placeholders as the official models/api.py does;
- sends text + frame/ref images via our OpenAI-compatible endpoint;
- extracts the answer with the official evaluation.py logic and scores exact
  letter match per benchmark split (main / robot_bench / ground_bench /
  indoor_perception_bench / easy2hard_bench).
"""

_ROOT = os.path.dirname(os.path.abspath(__file__))
_ENV_PATH = os.path.join(_ROOT, '..', '.env')
if os.path.exists(_ENV_PATH):
    with open(_ENV_PATH, 'r', encoding='utf-8') as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith('#') and '=' in _line:
                _k, _v = _line.split('=', 1)
                os.environ.setdefault(_k.strip(), _v.strip())

MODEL_REGISTRY = {
    'gemini-3.5-flash': {
        'api_key': os.environ.get('BOYUE_API_KEY', ''),
        'base_url': 'http://35.220.164.252:3888/v1',
        'model': 'gemini-3.5-flash',
    },
}

MAIN_ORDER = [
    '(Cross-Video) Memoery Update',
    '(Cross-Video) Multi-View Integration',
    'Planning',
    'Prediction',
    '(Motion Understanding) Camera Motion',
    '(Motion Understanding) Instance Motion',
    '(Motion Understanding) Interactive Motion',
    '(Spatial Construction) Instance-Instance Spatial Relationship',
    '(Spatial Construction) Instance-Scene Spatial Relationship',
    '(Spatial Construction) Scene-Scene Spatial Relationship',
    '(Spatial Construction) Instance/Scene Attribute',
    '(Spatial Construction) Camera-Instance Spatial Relationship',
    '(Spatial Construction) Camera-Scene Spatial Relationship',
]

SPATIAL_CONSTRUCTION_PREFIX = '(Spatial Construction)'
MOTION_PREFIX = '(Motion Understanding)'
CROSS_VIDEO_PREFIX = '(Cross-Video)'

def compat_group(qtype):
    """Group MMSI task types by whether a static three-view map can answer them."""
    qtype = qtype or ''
    if qtype.startswith(SPATIAL_CONSTRUCTION_PREFIX):
        return 'spatial_construction'
    if qtype.startswith(MOTION_PREFIX):
        return 'motion'
    if qtype.startswith(CROSS_VIDEO_PREFIX):
        return 'cross_video'
    if qtype in ('Planning', 'Prediction'):
        return 'planning_prediction'
    return 'other'


# ---------------------------------------------------------------------------
# Official sampling helpers (copied from repo dataset.py)
# ---------------------------------------------------------------------------
def interval_sampling_list(a, b):
    step = (a - 1) / (b - 1) if b > 1 else 0
    return [int(i * step) for i in range(b)]


def proportional_sample_from_lists(num_list, k):
    total_indices = interval_sampling_list(sum(num_list), k)
    sum_list = [sum(num_list[:i + 1]) for i in range(len(num_list))]
    sum_list = [0] + sum_list
    indices_list = []
    for i in range(len(sum_list) - 1):
        raw = [k - sum_list[i] for k in total_indices
               if k >= sum_list[i] and k < sum_list[i + 1]]
        indices_list.append(raw)
    return indices_list


# ---------------------------------------------------------------------------
# Data loading / processing (mirrors official MMSILOADER.process_sample)
# ---------------------------------------------------------------------------
def load_annotation(data_root):
    path = os.path.join(data_root, 'mmsivideo.json')
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def process_sample(sample, data_root, max_frame=50, task_specific=True):
    sample = dict(sample)
    total_latency = 0.0
    base_fps = sample['video_list'][0]['base_fps']
    for i, video_info in enumerate(sample['video_list']):
        video_info = dict(video_info)
        video_info['path'] = os.path.join(data_root, 'videos', video_info['path'])
        sample['video_list'][i] = video_info
        total_latency += video_info['end'] - video_info['start']
    input_fps = max_frame / total_latency if total_latency > 0 else 0
    sample['input_fps'] = min(input_fps, base_fps) if base_fps else input_fps

    sample['max_frame'] = max_frame
    total_frames = sum(len(f) for f in sample['frames_list'])
    sampled_frames_list = []
    if total_frames > max_frame:
        num_list = [len(f) for f in sample['frames_list']]
        indices_list = proportional_sample_from_lists(num_list, max_frame)
        for i in range(len(indices_list)):
            if len(indices_list[i]) < 1:
                indices_list[i] = [0]
            sampled_frames_list.append(
                [sample['frames_list'][i][j] for j in indices_list[i]])
    else:
        sampled_frames_list = sample['frames_list']
    sample['frames_list'] = [[os.path.join(data_root, 'frames', f)
                              for f in frames] for frames in sampled_frames_list]

    ref_count = len(sample['ref_images'])
    if sample.get('ori_question'):
        assert ref_count == sample['ori_question'].count('<image>'), \
            'ref_images count mismatch for %s' % sample.get('id')
    sample['ref_images'] = [os.path.join(data_root, 'ref_images', img)
                            for img in sample['ref_images']]

    if task_specific:
        sample['input_prompt'] = (sample['system_prompt'] + '\n' +
                                  sample['task_prompt'] + sample['user_prompt'] +
                                  sample['format_prompt'])
        sample['input_prompt_wo_sys'] = (sample['task_prompt'] +
                                         sample['user_prompt'] +
                                         sample['format_prompt'])
    else:
        sample['input_prompt'] = (sample['system_prompt'] + '\n' +
                                  sample['user_prompt'] +
                                  sample['format_prompt'])
        sample['input_prompt_wo_sys'] = (sample['user_prompt'] +
                                         sample['format_prompt'])
    return sample


# ---------------------------------------------------------------------------
# Prompt / message construction (mirrors official models/api.py)
# ---------------------------------------------------------------------------
def build_user_source_groups(sample):
    """Return (split_text, image_paths) with <video> replaced by frame <image>s."""
    split_text = sample['input_prompt_wo_sys']
    split_images = []
    assert split_text.count('<video>') == len(sample['frames_list'])
    for frames in sample['frames_list']:
        split_text = split_text.replace('<video>', '<image>' * len(frames), 1)
        split_images.extend(frames)
    split_images.extend(sample['ref_images'])
    assert split_text.count('<image>') == len(split_images)
    return split_text, split_images


def build_content_parts(sample, dry_run=False):
    split_text, image_paths = build_user_source_groups(sample)
    parts = []
    missing = []
    segments = split_text.split('<image>')
    for i, segment in enumerate(segments):
        if segment:
            parts.append({'type': 'text', 'text': segment})
        if i < len(image_paths):
            path = image_paths[i]
            if not os.path.exists(path):
                missing.append(path)
                if dry_run:
                    parts.append({'type': 'text', 'text': '[missing image: %s]' % path})
                    continue
                continue
            with open(path, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode('utf-8')
            parts.append({'type': 'image_url', 'image_url': {
                'url': 'data:image/jpeg;base64,%s' % b64, 'detail': 'low'}})
    return parts, missing


def build_messages(sample, dry_run=False):
    content, missing = build_content_parts(sample, dry_run=dry_run)
    messages = [{'role': 'system', 'content': sample['system_prompt']},
                {'role': 'user', 'content': content}]
    return messages, missing


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------
def call_api(model_name, messages, timeout=180.0):
    if model_name not in MODEL_REGISTRY:
        print('ERROR: Unknown model "%s". Available: %s' % (
            model_name, list(MODEL_REGISTRY.keys())))
        return None
    cfg = MODEL_REGISTRY[model_name]
    try:
        import openai
        client = openai.OpenAI(
            api_key=cfg['api_key'], base_url=cfg['base_url'], timeout=timeout)
        resp = client.chat.completions.create(
            model=cfg['model'], messages=messages, temperature=0.1,
            max_tokens=2000)
        return resp.choices[0].message.content.strip()
    except Exception as e:
        err_str = str(e)
        print('API call failed (%s): %s' % (model_name, err_str))
        if '429' in err_str or 'rate_limit' in err_str.lower():
            print('Detected rate limit. Sleeping 15s before retry...')
            time.sleep(15.0)
            return call_api(model_name, messages, timeout)
        return None


# ---------------------------------------------------------------------------
# Answer extraction (official evaluation.py logic)
# ---------------------------------------------------------------------------
def clear_words(text):
    return (text.replace(' ', '').replace('"', '').replace("'", '')
            .replace('\n', '').replace(':', ''))


def extract_answer(response):
    if response is None:
        return 'O'
    response = response.replace('<answer>', '').replace('</answer>', '')
    if 'no answer' in response:
        return 'O'
    if 'boxed{' in response:
        split_text = response.split('boxed{')[1].split('}')[0]
        return clear_words(split_text)
    words = ['"answer":', 'answer is', 'answer:', '"Answer":',
             'Answer is', 'Answer:']
    for word in words:
        if word in response:
            split_text = response.split(word)[-1]
            split_text = split_text.split(',')[0].split('.')[0]
            return clear_words(split_text)
    first_sentence = clear_words(response.split('.')[0])
    if first_sentence in ['A', 'B', 'C', 'D', 'E', 'F']:
        return first_sentence
    return 'O'


# ---------------------------------------------------------------------------
# Bench split helpers (official evaluation.py logic)
# ---------------------------------------------------------------------------
def load_bench_mapping(data_root, bench):
    local_candidates = [
        os.path.join(data_root, 'meta_data', '%s.json' % bench),
        os.path.join(_ROOT, '..', 'tmp', 'mmsi_video_bench',
                     'InternRobotics-MMSI-Video-Bench-412f5a4',
                     'meta_data', '%s.json' % bench),
    ]
    for path in local_candidates:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            id_to_type = {}
            for sub_type, ids in data.items():
                for qid in ids:
                    id_to_type[qid] = sub_type
            return id_to_type, list(data.keys())
    raise FileNotFoundError('bench meta not found: %s' % bench)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description='MMSI-Video-Bench runner (official protocol)')
    parser.add_argument('--data-root', default='data',
                        help='Dir containing mmsivideo.json, frames/, ref_images/')
    parser.add_argument('--setting', choices=['Uniform-50', 'Sufficient-Coverage'],
                        default='Uniform-50')
    parser.add_argument('--max-frame', type=int, default=None,
                        help='Override frame cap (Uniform-50 -> 50, '
                             'Sufficient-Coverage -> 300)')
    parser.add_argument('--model', default='gemini-3.5-flash')
    parser.add_argument('--bench', choices=['main', 'robot_bench', 'ground_bench',
                                            'indoor_perception_bench',
                                            'easy2hard_bench'],
                        default='main')
    parser.add_argument('--scope', choices=['all', 'spatial_construction'],
                        default='all',
                        help='spatial_construction keeps only the 6 Spatial Construction'
                             ' subtypes; motion/planning/prediction/cross-video are not'
                             ' answerable from a static three-view map')
    parser.add_argument('--n', type=int, default=50)
    parser.add_argument('--start', type=int, default=0,
                        help='Start sample index (0-based)')
    parser.add_argument('--sleep', type=float, default=3.0)
    parser.add_argument('--output', default='mmsi_results.json')
    parser.add_argument('--resume', default=None)
    parser.add_argument('--no-task', action='store_true',
                        help='Skip task_prompt (non-task-specific setting)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Validate data/prompt without calling the API')
    args = parser.parse_args()

    if args.model not in MODEL_REGISTRY:
        print('ERROR: Unknown model "%s". Available: %s' % (
            args.model, list(MODEL_REGISTRY.keys())))
        sys.exit(1)

    if args.max_frame is None:
        max_frame = 300 if args.setting == 'Sufficient-Coverage' else 50
    else:
        max_frame = args.max_frame

    annos = load_annotation(args.data_root)
    samples = [process_sample(s, args.data_root, max_frame=max_frame,
                              task_specific=not args.no_task)
               for s in annos]
    if args.scope == 'spatial_construction':
        samples = [s for s in samples
                   if compat_group(s.get('type')) == 'spatial_construction']
    selected = samples[args.start:args.start + args.n]
    print('Loaded %d samples, running %d (setting=%s, max_frame=%d, scope=%s)' % (
        len(samples), len(selected), args.setting, max_frame, args.scope))

    if args.dry_run:
        for i, s in enumerate(selected):
            messages, missing = build_messages(s, dry_run=True)
            text_parts = [p['text'] for p in messages[-1]['content']
                          if p.get('type') == 'text']
            image_parts = [p for p in messages[-1]['content']
                           if p.get('type') == 'image_url']
            print('[%d] id=%s type=%s gt=%s frames=%d refs=%d imgs=%d missing=%d' % (
                i, s.get('id'), s.get('type'), s.get('ground_truth'),
                sum(len(f) for f in s['frames_list']), len(s['ref_images']),
                len(image_parts), len(missing)))
            print('  prompt: %s' % ' | '.join(text_parts)[:200].replace('\n', ' '))
        print('DRY-RUN OK')
        return

    bench_mapping, bench_order = None, MAIN_ORDER
    if args.bench != 'main':
        bench_mapping, bench_order = load_bench_mapping(args.data_root, args.bench)

    results = []
    correct = 0
    skipped = 0
    total_calls = 0
    resume_from = 0
    if args.resume and os.path.exists(args.resume):
        with open(args.resume, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        done = [e for e in existing if '__summary__' not in e]
        # API_FAIL entries are retried on resume; other errors count as done.
        done = [e for e in done if e.get('error') != 'API_FAIL']
        results = list(done)
        correct = sum(1 for e in done if e.get('correct'))
        skipped = sum(1 for e in done if e.get('error'))
        total_calls = sum(e.get('api_calls', 0) for e in done)
        resume_from = len(done)
        print('Resuming from sample %d/%d (%d correct, %d skipped)' % (
            resume_from, len(selected), correct, skipped))

    for i, sample in enumerate(selected):
        if i < resume_from:
            continue
        print('\n--- Sample %d/%d [%s] %s ---' % (
            i + 1, len(selected), sample.get('id'), sample.get('type')))
        print('GT: %s' % sample.get('ground_truth'))

        messages, missing = build_messages(sample)
        if missing:
            print('SKIPPED: missing %d files (first: %s)' % (
                len(missing), missing[0]))
            skipped += 1
            results.append({'sample_idx': i, 'id': sample.get('id'),
                            'error': 'MISSING_FILES', 'correct': False,
                            'api_calls': 0})
            continue

        time.sleep(args.sleep)
        raw = call_api(args.model, messages)
        total_calls += 1
        if raw is None:
            print('SKIPPED: API_FAIL')
            skipped += 1
            results.append({'sample_idx': i, 'id': sample.get('id'),
                            'error': 'API_FAIL', 'correct': False,
                            'api_calls': 1})
            continue

        pred = extract_answer(raw)
        gt = sample.get('ground_truth')
        is_correct = pred in ['A', 'B', 'C', 'D', 'E', 'F'] and pred == gt
        if is_correct:
            correct += 1
        print('Extracted: %s Expected: %s %s' % (
            pred, gt, 'CORRECT' if is_correct else 'WRONG'))
        results.append({'sample_idx': i, 'id': sample.get('id'),
                        'type': sample.get('type'),
                        'ground_truth': gt, 'extracted_answer': pred,
                        'correct': is_correct, 'api_calls': 1,
                        'raw_response': raw})
        if (i + 1) % 5 == 0:
            partial = args.output.replace('.json', '_partial_%d.json' % (i + 1))
            with open(partial, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

    total_run = len(selected) - skipped
    acc = correct / total_run * 100 if total_run > 0 else 0.0
    print('\nResults: %d/%d correct (%.1f%%)' % (correct, total_run, acc))
    print('Skipped: %d, API calls: %d' % (skipped, total_calls))

    score_dict = {'Overall': []}
    for e in results:
        if e.get('error'):
            continue
        q_type = e.get('type')
        if bench_mapping is not None:
            q_type = bench_mapping.get(e.get('id'), q_type)
        score_dict.setdefault(q_type, []).append(float(e.get('correct', False)))
        score_dict['Overall'].append(float(e.get('correct', False)))
    for key in ['Overall'] + bench_order:
        if key in score_dict and score_dict[key]:
            vals = score_dict[key]
            print('%s: %.3f (%d)' % (key, sum(vals) / len(vals), len(vals)))

    per_type = {}
    for key, vals in score_dict.items():
        if vals:
            per_type[key] = round(sum(vals) / len(vals) * 100, 1)
    results.append({'__summary__': {
        'model': args.model,
        'setting': args.setting,
        'max_frame': max_frame,
        'bench': args.bench,
        'scope': args.scope,
        'total_samples': len(selected),
        'correct': correct,
        'total_run': total_run,
        'skipped': skipped,
        'accuracy_pct': round(acc, 1),
        'total_api_calls': total_calls,
        'per_type_accuracy_pct': per_type,
    }})
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print('Done. Results saved to %s' % args.output)


if __name__ == '__main__':
    main()
