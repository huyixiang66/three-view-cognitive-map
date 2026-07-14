#!/usr/bin/env python
import json, sys, os
sys.path.insert(0, 'C:/Users/贝贝/Documents/Three-view Cognitive Map/src')
from prompts_3pass import TOP_VIEW_PROMPT, FRONT_VIEW_PROMPT_SHARED, SIDE_VIEW_PROMPT_SHARED, ANSWER_PROMPT_ABS_DISTANCE, ANSWER_PROMPT_REL_DISTANCE, ANSWER_PROMPT_REL_DIRECTION, BASELINE_ABS_DISTANCE
from debug_pipeline_3pass import parse_cogmap, evaluate_answer, get_answer_prompt_template, get_baseline_prompt_template
import sys; sys.path.insert(0, '..'); from viz.grid_visualizer import visualize_three_view
passed = 0
failed = 0

def check(name, condition, detail=''):
    global passed, failed
    if condition:
        passed += 1
        print(f'  PASS: {name}')
    else:
        failed += 1
        print(f'  FAIL: {name} -- {detail}')

print('=== 1. Prompt Template Tests ===')
check('Top view has video_input', '{video_input}' in TOP_VIEW_PROMPT)
check('Top view mentions 3 steps', 'STEP 1 OF 3' in TOP_VIEW_PROMPT)
check('Front shared has top_view_result', '{top_view_result}' in FRONT_VIEW_PROMPT_SHARED)
check('Front shared x-axis constraint', 'SAME as top view x-axis' in FRONT_VIEW_PROMPT_SHARED)
check('Side shared has both placeholders', '{top_view_result}' in SIDE_VIEW_PROMPT_SHARED and '{front_view_result}' in SIDE_VIEW_PROMPT_SHARED)
check('Abs distance has 3 views', all(v in ANSWER_PROMPT_ABS_DISTANCE for v in ['FRONT VIEW', 'TOP VIEW', 'SIDE VIEW']))
check('Baseline has question', '{question}' in BASELINE_ABS_DISTANCE)

formatted = TOP_VIEW_PROMPT.format(video_input='test room')
check('Format substitution works', 'test room' in formatted and '{video_input}' not in formatted)

print()
print('=== 2. CogMap Parser Tests ===')
new_fmt = json.dumps(dict(gridSize=10, objects=[dict(x=3, y=5, name='table')]))
result = parse_cogmap(new_fmt)
check('Parse new format', result is not None and result['gridSize'] == 10 and len(result['objects']) == 1)

legacy_fmt = json.dumps([dict(x=3, y=5, name='table')])
result = parse_cogmap(legacy_fmt)
check('Parse legacy format', result is not None and 'gridSize' in result and result['gridSize'] == 10)

with_bt = chr(96)*3 + 'json' + chr(10) + json.dumps(dict(gridSize=5, objects=[])) + chr(10) + chr(96)*3
result = parse_cogmap(with_bt)
check('Strip backticks', result is not None and result['gridSize'] == 5)

result = parse_cogmap('not json at all')
check('Return None on invalid JSON', result is None)

print()
print('=== 3. Visualizer Tests ===')
cmap_new = dict(front=dict(gridSize=10, objects=[dict(x=0, z=0, name='door'), dict(x=3, z=1, name='table')]), top=dict(gridSize=10, objects=[dict(x=0, y=0, name='door'), dict(x=3, y=2, name='table')]), side=dict(gridSize=10, objects=[dict(y=0, z=0, name='door'), dict(y=2, z=1, name='table')]))
output = visualize_three_view(json.dumps(cmap_new))
check('Visualize new format', 'FRONT' in output and 'TOP' in output and 'SIDE' in output)
check('Shows grid size', 'Grid size: 10x10' in output)
check('Shows emoji door', chr(0x1f6aa) in output)
check('Shows emoji table', chr(0x1f9fa) in output)

cmap_legacy = dict(front=[dict(x=0, z=0, objects=['door']), dict(x=3, z=1, objects=['table'])], top=[dict(x=0, y=0, objects=['door']), dict(x=3, y=2, objects=['table'])], side=[dict(y=0, z=0, objects=['door']), dict(y=2, z=1, objects=['table'])])
output = visualize_three_view(json.dumps(cmap_legacy))
check('Visualize legacy format', 'FRONT' in output and 'TOP' in output and 'SIDE' in output)

output = visualize_three_view('not json')
check('Handle invalid input', 'Parse Error' in output)

print()
print('=== 4. Evaluate Answer Tests ===')
ok, mt = evaluate_answer('A', 'A', 'object_rel_direction_hard')
check('Direct match direction', ok and mt == 'MATCH')

ok, mt = evaluate_answer('2.5', '2.5', 'object_abs_distance')
check('Abs distance exact', ok and mt == 'MATCH')

ok, mt = evaluate_answer('2.0', '2.5', 'object_abs_distance')
check('Abs distance close', ok and mt == 'CLOSE')

ok, mt = evaluate_answer('5.0', '2.5', 'object_abs_distance')
check('Abs distance far', not ok and mt == 'MISMATCH')

ok, mt = evaluate_answer('B', 'A', 'object_rel_direction_hard')
check('Wrong direction', not ok and mt == 'MISMATCH')

ok, mt = evaluate_answer('', 'A', 'object_rel_direction_hard')
check('Empty prediction', not ok and mt == 'NO_OUTPUT')

print()
print('=== 5. Prompt Template Selector ===')
check('Select abs answer', get_answer_prompt_template('object_abs_distance') is ANSWER_PROMPT_ABS_DISTANCE)
check('Select rel answer', get_answer_prompt_template('object_rel_distance') is ANSWER_PROMPT_REL_DISTANCE)
check('Select dir answer', get_answer_prompt_template('object_rel_direction_hard') is ANSWER_PROMPT_REL_DIRECTION)
check('Select abs baseline', get_baseline_prompt_template('object_abs_distance') is BASELINE_ABS_DISTANCE)

print()
print('=== RESULTS: ' + str(passed) + ' passed, ' + str(failed) + ' failed ===')
sys.exit(0 if failed == 0 else 1)

