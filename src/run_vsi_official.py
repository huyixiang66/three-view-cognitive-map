# -*- coding: utf-8 -*-
"""Official VSI-Bench direct evaluation runner (video -> answer, 8 task types).

This is the "official protocol" baseline: per TIS (arXiv 2412.14171)
Appendix B.1 / Table 4 / Table 10, each of the 8 VSI task families gets its own
answer instruction and scoring:
- MCA types (rel_distance / rel_direction / appearance_order / route_planning):
  option-letter accuracy;
- NA types (counting / abs_distance / size / room_size): numeric answer,
  summary with mean relative accuracy (MRA); per-question correct uses the
  relative-error tolerance implemented in vsi_protocol.

Usage:
  python src/run_vsi_official.py --samples src/vsi_subset_200.json --n 50
  python src/run_vsi_official.py --samples ... --resume out.json
"""
import argparse
import json
import os
import sys
import time

_ROOT = os.path.dirname(os.path.abspath(__file__))
_ENV_PATH = os.path.join(_ROOT, '..', '.env')
if os.path.exists(_ENV_PATH):
    with open(_ENV_PATH, 'r', encoding='utf-8') as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith('#') and '=' in _line:
                _k, _v = _line.split('=', 1)
                os.environ.setdefault(_k.strip(), _v.strip())

from vsi_protocol import (
    build_direct_prompt,
    extract_answer,
    is_correct,
    is_na,
    mra,
    metric,
)

MODEL_REGISTRY = {
    'gemini-3.5-flash': {
        'api_key': os.environ.get('BOYUE_API_KEY', ''),
        'base_url': 'http://35.220.164.252:3888/v1',
        'model': 'gemini-3.5-flash',
    },
}

VIDEO_CACHE_DIR = os.path.join(
    os.path.expanduser('~'), '.cache', 'huggingface', 'vsibench')

SYSTEM_PROMPT = (
    'You are a spatial reasoning assistant. '
    'Always end your response with ANSWER: followed by your final answer. '
    'Do not include any text after ANSWER:'
)


def load_video_base64(video_path):
    if not os.path.exists(video_path):
        return None
    with open(video_path, 'rb') as f:
        import base64
        return base64.b64encode(f.read()).decode('utf-8')


def build_video_message(text, video_b64):
    return [
        {'type': 'text', 'text': text},
        {'type': 'video_url',
         'video_url': {'url': 'data:video/mp4;base64,%s' % video_b64}},
    ]


def call_api(model_name, messages, timeout=600.0):
    cfg = MODEL_REGISTRY[model_name]
    import openai
    client = openai.OpenAI(
        api_key=cfg['api_key'], base_url=cfg['base_url'], timeout=timeout)
    resp = client.chat.completions.create(
        model=cfg['model'], messages=messages, temperature=0.1, max_tokens=2000)
    return resp.choices[0].message.content.strip()


def family(qtype):
    if qtype.startswith('object_rel_direction'):
        return 'object_rel_direction'
    return qtype


def main():
    parser = argparse.ArgumentParser(description='Official VSI direct runner')
    parser.add_argument('--model', default='gemini-3.5-flash')
    parser.add_argument('--samples', default='vsi_subset_200.json')
    parser.add_argument('--n', type=int, default=50)
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--sleep', type=float, default=2.0)
    parser.add_argument('--output', default='vsi_official_results.json')
    parser.add_argument('--resume', default=None)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if args.model not in MODEL_REGISTRY:
        print('ERROR: unknown model %s' % args.model)
        sys.exit(1)

    path = args.samples if os.path.exists(args.samples) else os.path.join(_ROOT, args.samples)
    with open(path, 'r', encoding='utf-8') as f:
        samples = json.load(f)
    selected = samples[args.start:args.start + args.n]
    print('Loaded %d samples, running %d (model=%s)' % (
        len(samples), len(selected), args.model))

    if args.dry_run:
        for i, s in enumerate(selected):
            prompt = build_direct_prompt(s)
            print('[%d] %s %s gt=%s metric=%s' % (
                i, s['question_type'], s['scene_name'], s['ground_truth'],
                metric(s['question_type'])))
            print('  prompt: %s' % prompt[:200].replace('\n', ' | '))
        print('DRY-RUN OK')
        return

    results = []
    resume_from = 0
    if args.resume and os.path.exists(args.resume):
        with open(args.resume, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        done = [e for e in existing if '__summary__' not in e
                and e.get('error') != 'API_FAIL']
        results = list(done)
        resume_from = len(done)
        print('Resuming from sample %d/%d' % (resume_from, len(selected)))

    for i, sample in enumerate(selected):
        if i < resume_from:
            continue
        scene = sample['scene_name']
        dataset = sample['dataset']
        qtype = sample['question_type']
        print('\n--- Sample %d/%d [%s] %s ---' % (
            i + 1, len(selected), scene, qtype))
        video_b64 = load_video_base64(
            os.path.join(VIDEO_CACHE_DIR, dataset, scene + '.mp4'))
        if video_b64 is None:
            print('SKIPPED: NO_VIDEO')
            results.append({'sample_idx': i, 'scene': scene,
                            'dataset': dataset, 'question_type': qtype,
                            'error': 'NO_VIDEO', 'correct': False,
                            'api_calls': 0})
            continue
        text = build_direct_prompt(sample)
        messages = [{'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user',
                     'content': build_video_message(text, video_b64)}]
        time.sleep(args.sleep)
        try:
            raw = call_api(args.model, messages)
        except Exception as e:
            print('SKIPPED: API_FAIL (%s)' % str(e)[:120])
            results.append({'sample_idx': i, 'scene': scene,
                            'dataset': dataset, 'question_type': qtype,
                            'error': 'API_FAIL', 'correct': False,
                            'api_calls': 1})
            continue
        answer = extract_answer(raw, qtype)
        correct = is_correct(answer, sample['ground_truth'], qtype)
        print('Extracted: %s Expected: %s %s' % (
            answer, sample['ground_truth'],
            'CORRECT' if correct else 'WRONG'))
        results.append({
            'sample_idx': i,
            'scene': scene,
            'dataset': dataset,
            'question_type': qtype,
            'family': family(qtype),
            'metric': metric(qtype),
            'question': sample['question'],
            'options': sample.get('options') or [],
            'ground_truth': sample['ground_truth'],
            'extracted_answer': answer,
            'correct': correct,
            'mra': mra(answer, sample['ground_truth']) if is_na(qtype) else None,
            'api_calls': 1,
            'raw_response': raw,
            'error': None,
        })
        if (i + 1) % 5 == 0:
            partial = args.output.replace(
                '.json', '_partial_%d.json' % (i + 1))
            with open(partial, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

    ok = [r for r in results if not r.get('error')]
    total = len(ok)
    correct_n = sum(1 for r in ok if r.get('correct'))
    print('\nSamples answered: %d, per-sample correct: %d (%.1f%%)' % (
        total, correct_n, correct_n / total * 100 if total else 0.0))

    # Official aggregation (vision-x-nyu/thinking-in-space utils.py):
    # per-type metric mean, rel_direction difficulties merged,
    # overall = unweighted mean of the 8 type-level scores.
    by_type = {}
    for r in ok:
        by_type.setdefault(r['question_type'], []).append(r)
    type_scores = {}
    for qt, recs in sorted(by_type.items()):
        if is_na(qt):
            vals = [r['mra'] or 0.0 for r in recs]
            type_scores[qt] = sum(vals) / len(vals) * 100
        else:
            c = sum(1 for r in recs if r['correct'])
            type_scores[qt] = c / len(recs) * 100
    dir_keys = sorted(k for k in type_scores if k.startswith('object_rel_direction'))
    if dir_keys:
        dir_val = sum(type_scores[k] for k in dir_keys) / len(dir_keys)
        for k in dir_keys:
            type_scores.pop(k)
        type_scores['object_rel_direction'] = dir_val
    overall = (sum(type_scores.values()) / len(type_scores)
               if type_scores else 0.0)
    order = ['object_counting', 'object_abs_distance', 'object_size_estimation',
             'room_size_estimation', 'object_rel_distance',
             'object_rel_direction', 'route_planning', 'obj_appearance_order']
    for qt in order:
        if qt in type_scores:
            print('%s: %.2f%%' % (qt, type_scores[qt]))
    print('Official overall (mean of type scores): %.2f%%' % overall)

    results.append({'__summary__': {
        'model': args.model,
        'protocol': 'vsi_official',
        'total_samples': len(selected),
        'correct': correct_n,
        'total_run': total,
        'skipped': len(selected) - total,
        'overall_official_pct': round(overall, 1),
        'per_type_pct': {k: round(v, 1) for k, v in type_scores.items()},
    }})
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print('Done. Results saved to %s' % args.output)


if __name__ == '__main__':
    main()
