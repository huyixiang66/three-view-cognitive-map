# -*- coding: utf-8 -*-
"""MMSI-Video-Bench three-view adapter (all MMSI task types).

We run every MMSI question type through map + map-enhanced answering: even
for Motion / Planning / Prediction / Cross-Video, an explicit three-view
cognitive map provides spatial context that may help the answer stage.

Pipeline per sample:
1. input mode: direct mp4 like VSI-Bench (--input video, default) or sampled
   frames (--input frames), plus optional ref images from the data;
2. build a question-driven TOP/FRONT/SIDE cognitive map from the visual input
   (10x10 grid, shared axes), letting the model decide the relevant objects;
3. answer the MMSI multiple-choice question using the map text + the same
   visual input ("video memory"), choose the option letter A-F;
4. record map/answer and score exact letter match against ground_truth.

Map prompt mirrors the TIS three-view protocol used for VSI, but takes the
MMSI question instead of a fixed category list.
"""
import argparse
import json
import os
import re
import sys
import time
import base64

_ROOT = os.path.dirname(os.path.abspath(__file__))
_ENV_PATH = os.path.join(_ROOT, '..', '.env')
if os.path.exists(_ENV_PATH):
    with open(_ENV_PATH, 'r', encoding='utf-8') as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith('#') and '=' in _line:
                _k, _v = _line.split('=', 1)
                os.environ.setdefault(_k.strip(), _v.strip())

from run_mmsi import (
    MODEL_REGISTRY,
    load_annotation,
    process_sample,
)

MAP_SYSTEM = (
    'You are a spatial layout assistant. Estimate object positions in three '
    'orthogonal views of the scene.'
)

MAP_PROMPT = """[Task] The attached visual input shows a scene. Identify the objects and spatial layout needed to answer the spatial question below, then estimate the center of every relevant instance in three orthogonal views, each represented by a 10x10 grid with coordinates from 0 to 9. Keep shared axes consistent: top.x = front.x, top.y = side.y, front.z = side.z (z is height, 0 = ground).
Question: {question}
Options:
{options}
[Output] Return ONLY valid JSON without markdown fences. Use JSON arrays [x, y], NOT parentheses. STRICTLY follow this format: {{"top": {{"category name": [[x_1, y_1], ...], ...}}, "front": {{"category name": [[x_1, z_1], ...], ...}}, "side": {{"category name": [[y_1, z_1], ...], ...}}}}"""

ANSWER_SYSTEM = (
    'You are a spatial reasoning assistant. '
    'Always end your response with ANSWER: followed by the option letter.'
)

ANSWER_PROMPT = """You watched the visual input and built a three-view cognitive map of it (10x10 grid). Answer the question using BOTH the visual input and the cognitive map.
Three-view cognitive map:
{map_text}
Question:
{question}
Options:
{options}
Answer with the option's letter from the given choices directly."""


def question_text(sample):
    raw = sample.get('ori_question') or ''
    if not raw:
        raw = sample.get('user_prompt', '')
        m = re.search(r'My question is:\s*(.*)', raw, re.S)
        if m:
            return m.group(1).strip()
    return raw.strip()


def options_block(sample):
    opts = sample.get('options') or []
    lines = []
    for i, opt in enumerate(opts):
        lines.append('%s. %s' % (chr(ord('A') + i), str(opt).strip()))
    return '\n'.join(lines)


def all_image_paths(sample):
    paths = []
    for frames in sample['frames_list']:
        paths.extend(frames)
    paths.extend(sample['ref_images'])
    return paths

def all_media_paths(sample, input_mode):
    """Return frame/image paths (frames mode) or direct video + ref images (video mode)."""
    if input_mode == 'frames':
        return all_image_paths(sample)
    paths = [v['path'] for v in sample['video_list']]
    paths.extend(sample['ref_images'])
    return paths


def content_with_media(text, paths, missing):
    """Build multimodal content from text plus direct videos and/or images."""
    content = [{'type': 'text', 'text': text}]
    for p in paths:
        if not os.path.exists(p):
            missing.append(p)
            continue
        with open(p, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        low = p.lower()
        if low.endswith(('.mp4', '.webm', '.mov')):
            content.append({'type': 'video_url', 'video_url': {
                'url': 'data:video/mp4;base64,%s' % b64}})
        else:
            content.append({'type': 'image_url', 'image_url': {
                'url': 'data:image/jpeg;base64,%s' % b64, 'detail': 'low'}})
    return content



def call_api(model_name, messages, timeout=420.0, retries=2):
    cfg = MODEL_REGISTRY[model_name]
    import openai
    last = None
    for attempt in range(retries):
        try:
            client = openai.OpenAI(
                api_key=cfg['api_key'], base_url=cfg['base_url'], timeout=timeout)
            resp = client.chat.completions.create(
                model=cfg['model'], messages=messages, temperature=0.1,
                max_tokens=3000)
            return resp.choices[0].message.content.strip()
        except Exception as e:
            last = e
            time.sleep(10 * (attempt + 1))
    raise last



def _extract_json(text):
    if not text:
        return None
    start = text.find('{')
    if start < 0:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        ch = text[i]
        if esc:
            esc = False
            continue
        if ch == '\\':
            esc = True
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
                    return json.loads(text[start:i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def extract_letter(text):
    if not text:
        return None
    m = re.search(r'ANSWER:\s*([A-F])', text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    m = re.search(r'`{1,2}([A-F])`{1,2}', text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    tail = text[-300:]
    for ch in reversed(tail):
        if ch in 'ABCDEF':
            return ch
    return None


def main():
    parser = argparse.ArgumentParser(
        description='MMSI-Video-Bench three-view adapter (all MMSI task types)')
    parser.add_argument('--data-root', default='data')
    parser.add_argument('--model', default='gemini-3.5-flash')
    parser.add_argument('--max-frame', type=int, default=50)
    parser.add_argument('--input', choices=['video', 'frames'], default='video',
                        help='video: send actual mp4 like VSI-Bench; frames: send sampled frames')
    parser.add_argument('--n', type=int, default=20)
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--sleep', type=float, default=1.0)
    parser.add_argument('--output', default='mmsi_threeview_results.json')
    parser.add_argument('--resume', default=None)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if args.model not in MODEL_REGISTRY:
        print('ERROR: unknown model %s' % args.model)
        sys.exit(1)

    annos = load_annotation(args.data_root)
    samples = [process_sample(
        raw, args.data_root, max_frame=args.max_frame, task_specific=True)
        for raw in annos]
    selected = samples[args.start:args.start + args.n]
    print('All MMSI samples: %d, running %d (input=%s)' % (
        len(samples), len(selected), args.input))

    if args.dry_run:
        for i, s in enumerate(selected):
            q = question_text(s)
            media_paths = all_media_paths(s, args.input)
            print('[%d] input=%s id=%s type=%s gt=%s media=%d refs=%d' % (
                i, args.input, s.get('id'), s.get('type'), s.get('ground_truth'),
                len(media_paths), len(s['ref_images'])))
            print('  Q: %s' % q[:180])
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
        qtype = sample.get('type')
        qid = sample.get('id')
        gt = sample.get('ground_truth')
        print('\n--- Sample %d/%d [%s] %s ---' % (i + 1, len(selected), qid, qtype))
        paths = all_media_paths(sample, args.input)
        missing = []
        map_text = MAP_PROMPT.format(
            question=question_text(sample), options=options_block(sample))
        content = content_with_media(map_text, paths, missing)
        if missing:
            print('SKIPPED: missing %d files (first %s)' % (
                len(missing), missing[0]))
            results.append({'sample_idx': i, 'id': qid, 'type': qtype,
                            'error': 'MISSING_FILES', 'correct': False,
                            'api_calls': 0})
            continue
        time.sleep(args.sleep)
        try:
            raw_map = call_api(args.model, [
                {'role': 'system', 'content': MAP_SYSTEM},
                {'role': 'user', 'content': content}])
        except Exception as e:
            print('SKIPPED: MAP_API_FAIL (%s)' % str(e)[:120])
            results.append({'sample_idx': i, 'id': qid, 'type': qtype,
                            'error': 'API_FAIL', 'correct': False,
                            'api_calls': 1})
            continue
        parsed = _extract_json(raw_map)
        if parsed is None:
            print('MAP_PARSE_FAIL; raw: %s' % raw_map[:120])
            results.append({'sample_idx': i, 'id': qid, 'type': qtype,
                            'error': 'MAP_PARSE_FAIL', 'correct': False,
                            'api_calls': 1, 'raw_map': raw_map})
            continue
        map_text_out = json.dumps(parsed, ensure_ascii=False)
        answer_text = ANSWER_PROMPT.format(
            map_text=map_text_out,
            question=question_text(sample),
            options=options_block(sample))
        content2 = content_with_media(answer_text, paths, [])
        time.sleep(args.sleep)
        try:
            raw_answer = call_api(args.model, [
                {'role': 'system', 'content': ANSWER_SYSTEM},
                {'role': 'user', 'content': content2}])
        except Exception as e:
            print('SKIPPED: ANSWER_API_FAIL (%s)' % str(e)[:120])
            results.append({'sample_idx': i, 'id': qid, 'type': qtype,
                            'error': 'API_FAIL', 'correct': False,
                            'api_calls': 2})
            continue
        pred = extract_letter(raw_answer)
        correct = bool(pred) and pred == gt
        print('Extracted: %s Expected: %s %s' % (
            pred, gt, 'CORRECT' if correct else 'WRONG'))
        results.append({'sample_idx': i, 'id': qid, 'type': qtype,
                        'question': question_text(sample),
                        'ground_truth': gt, 'extracted_answer': pred,
                        'correct': correct, 'api_calls': 2,
                        'raw_map': raw_map, 'map': parsed,
                        'raw_answer': raw_answer, 'error': None})
        if (i + 1) % 5 == 0:
            partial = args.output.replace('.json', '_partial_%d.json' % (i + 1))
            with open(partial, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

    ok = [r for r in results if not r.get('error')]
    correct_n = sum(1 for r in ok if r.get('correct'))
    acc = correct_n / len(ok) * 100 if ok else 0.0
    print('\nThree-view adapter: %d/%d correct (%.1f%%)' % (
        correct_n, len(ok), acc))
    by_type = {}
    for r in ok:
        by_type.setdefault(r['type'], []).append(r)
    per_type = {}
    for qt, recs in sorted(by_type.items()):
        c = sum(1 for r in recs if r['correct'])
        per_type[qt] = {'correct': c, 'total': len(recs),
                        'accuracy_pct': round(c / len(recs) * 100, 1)}
        print('%s: %d/%d (%.1f%%)' % (
            qt, c, len(recs), c / len(recs) * 100))
    results.append({'__summary__': {
        'model': args.model,
        'protocol': 'mmsi_threeview_all_types_' + args.input,
        'total_samples': len(selected),
        'correct': correct_n,
        'total_run': len(ok),
        'skipped': len(selected) - len(ok),
        'accuracy_pct': round(acc, 1),
        'per_type': per_type,
    }})
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print('Done. Results saved to %s' % args.output)


if __name__ == '__main__':
    main()
