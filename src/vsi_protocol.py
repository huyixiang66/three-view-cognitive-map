# -*- coding: utf-8 -*-
"""Official VSI-Bench QA protocol (single source of truth).

Sources:
- TIS (Thinking in Space, arXiv 2412.14171) Appendix B.1 / Table 4 / Table 10;
- local subset schema in src/vsi_subset_200.json.

VSI-Bench has 8 task families. Metric split per TIS:
- MCA (multiple-choice): rel_distance, rel_direction (easy/medium/hard),
  appearance_order, route_planning -> accuracy on the option letter;
- NA (numerical): counting, abs_distance, size_estimation, room_size_estimation
  -> numeric answer, summary uses mean relative accuracy (MRA); per-question
  "correct" uses a relative-error tolerance.

Prompt instructions follow TIS Table 10:
- MCA: "Answer with the option's letter from the given choices directly."
- NA:  "Do not respond with anything other than a single number!"
"""

import re

MCA_TYPES = {
    'object_rel_distance',
    'object_rel_direction_easy',
    'object_rel_direction_medium',
    'object_rel_direction_hard',
    'obj_appearance_order',
    'route_planning',
}
NA_TYPES = {
    'object_counting',
    'object_abs_distance',
    'object_size_estimation',
    'room_size_estimation',
}

PRE_PROMPT = 'These are frames of a video.'
MCA_INSTRUCTION = "Answer with the option's letter from the given choices directly."
NA_INSTRUCTION_OPEN = 'Please answer the question using a single word or phrase.'
NA_INSTRUCTION = 'Do not respond with anything other than a single number!'
OPTIONS_HEADER = 'Options:'

_MRA_THRESHOLDS = [t / 100.0 for t in range(50, 100, 5)]


def metric(qtype):
    if qtype in NA_TYPES:
        return 'na'
    if qtype in MCA_TYPES:
        return 'mca'
    raise ValueError('unknown VSI question_type: %s' % qtype)


def is_mca(qtype):
    return qtype in MCA_TYPES


def is_na(qtype):
    return qtype in NA_TYPES


def official_suffix(qtype):
    return NA_INSTRUCTION if is_na(qtype) else MCA_INSTRUCTION


COT_SUFFIX = "Let's think step by step."

def build_direct_prompt(sample, na_post='proprietary', include_pre=True, cot=False):
    """Assemble the per-type prompt: [pre] + question [+ options] + post/CoT."""
    qtype = sample.get('question_type', '')
    parts = []
    if include_pre:
        parts.append(PRE_PROMPT)
    parts.append(sample.get('question', ''))
    if is_mca(qtype):
        opts = sample.get('options') or []
        if opts:
            parts.append(OPTIONS_HEADER)
            parts.extend(str(o) for o in opts)
        if not cot:
            parts.append(MCA_INSTRUCTION)
    elif not cot:
        na = NA_INSTRUCTION_OPEN if na_post == 'open' else NA_INSTRUCTION
        parts.append(na)
    if cot:
        parts.append(COT_SUFFIX)
    return '\n'.join(parts)


def extract_answer(text, qtype):
    """Letter for MCA, first number for NA."""
    if not text:
        return None
    text = text.strip()
    if is_mca(qtype):
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
    m = re.search(r'ANSWER:\s*(-?\d+(?:\.\d+)?)', text, re.IGNORECASE)
    if not m:
        m = re.search(r'-?\d+(?:\.\d+)?', text.replace(',', ''))
    return m.group(1) if m and m.lastindex else (m.group(0) if m else None)


def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def mra(pred, gt):
    """Mean relative accuracy over the threshold ladder; returns 0..1."""
    pf, gf = _to_float(pred), _to_float(gt)
    if pf is None or gf is None or gf == 0:
        return 0.0
    rel_err = abs(pf - gf) / abs(gf)
    return sum(1 for t in _MRA_THRESHOLDS if rel_err < 1 - t) / len(_MRA_THRESHOLDS)


def numeric_correct(pred, gt, qtype):
    pf, gf = _to_float(pred), _to_float(gt)
    if pf is None or gf is None:
        return False
    if 'counting' in qtype:
        return abs(pf - gf) < 1e-6
    if gf == 0:
        return False
    r = pf / gf
    return 0.5 <= r <= 2.0


def is_correct(answer, gt, qtype):
    if answer is None or gt is None:
        return False
    if is_mca(qtype):
        return str(answer).strip().upper() == str(gt).strip().upper()
    return numeric_correct(answer, gt, qtype)
