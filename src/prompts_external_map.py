# -*- coding: utf-8 -*-
"""Answer prompts for the four-system QA: the video plus a map built by an external system.

The TIS arm (`tis_prompts.py` / `prompts_3pass.py`) keeps its wording: the model builds the
cognitive map itself, so its prompts stay untouched.  The four-system runs are a different arm --
the map comes from RAS / SimFoundry / HoloScene / OVOW and may be incomplete -- so their answer
prompts live here.

Each template keeps the published sentence of its TIS counterpart (the map-centric instruction
that the pipeline of record uses) and adds only what the external map makes necessary:

* MAP_RULE -- the map may be incomplete, so the video decides when they disagree or when the
  asked object is missing from the map.
* COMMIT_RULE -- the model must answer instead of reporting that the objects are absent.

Formatting follows the official VSI-Bench post-prompts (lmms_eval/tasks/vsibench/vsibench.yaml):
"Answer with the option's letter from the given choices directly." for the multiple-choice types
and a single-number instruction for the numerical ones.

AUDIT 2026-09-20: the previous wording ("Based on the cognitive map provided above, ...") made
qwen25vl answer "There are none." for 146-156 questions per system whenever the map lacked the
queried object, while internvl3 answered 602/604 of the same questions.  See
docs/mesh-json-audit-scaleup50-2026-09-20.md section 7.3.
"""

MAP_RULE = (
    "The three-view cognitive map above was reconstructed by an external system and may be "
    "incomplete, duplicated, or non-metric. Use it only as a cross-check; the video decides. "
    "If the map does not contain an object the question asks about, ignore the map for that "
    "object and answer from the video."
)

COMMIT_RULE = (
    "Never answer that the objects are absent or that the answer cannot be determined: always "
    "commit to your best estimate."
)

ANSWER_PROMPT_COUNTING_EXT = """Based on the cognitive map provided above, how many instances of the asked category appear in the scene? Count every instance in the map.
""" + MAP_RULE + """
""" + COMMIT_RULE + """
Question: {question}
Do not answer anything other than a single integer number.
Always end your response with ANSWER: followed by the number."""

ANSWER_PROMPT_ABS_DISTANCE_EXT = '''QUESTION: {question}

''' + MAP_RULE + '''
''' + COMMIT_RULE + '''
Estimate the distance and provide your answer as a number in meters.
Answer with a single number (e.g., 2.5).
Always end your response with ANSWER: followed by the number.'''

ANSWER_PROMPT_REL_DISTANCE_EXT = '''QUESTION: {question}

{options}

''' + MAP_RULE + '''
''' + COMMIT_RULE + '''
Compare the distances and provide your answer.
Answer with the option letter (A, B, C, or D).
Always end your response with ANSWER: followed by the letter.'''

ANSWER_PROMPT_REL_DIRECTION_EXT = '''QUESTION: {question}

{options}

''' + MAP_RULE + '''
''' + COMMIT_RULE + '''
Determine the relative direction and provide your answer.
Answer with the option letter (A, B, C, or D).
Always end your response with ANSWER: followed by the letter.'''

ANSWER_PROMPT_SIZE_EXT = """Based on the cognitive map provided above, estimate the physical size of the asked object in the same units as the question (centimeters or meters as asked). Use the object sizes in the map (grid cells) and common reference sizes (e.g., a door is about 2m tall) to convert grid units to real units.
""" + MAP_RULE + """
""" + COMMIT_RULE + """
Question: {question}
Do not answer anything other than a single number.
Always end your response with ANSWER: followed by the number."""

ANSWER_PROMPT_ROOM_EXT = """Based on the cognitive map provided above, estimate the room size in the same units as the question (square meters or other units as asked), using the room width/depth and common reference sizes (e.g., a door is about 1m wide) to convert grid units to real units.
""" + MAP_RULE + """
""" + COMMIT_RULE + """
Question: {question}
Do not answer anything other than a single number.
Always end your response with ANSWER: followed by the number."""

ANSWER_PROMPT_ROUTE_EXT = """Based on the cognitive map provided above, choose the best answer for the navigation question using the object positions and directions in the map.
""" + MAP_RULE + """
""" + COMMIT_RULE + """
Question: {question}
Options:
{options}
Answer with the option's letter from the given choices directly.
Always end your response with ANSWER: followed by the letter."""

ANSWER_PROMPT_APPEARANCE_EXT = """Based on the video and the cognitive map provided above, determine the order in which the asked categories first appear in the video.
""" + MAP_RULE + """
""" + COMMIT_RULE + """
Question: {question}
Options:
{options}
Answer with the option's letter from the given choices directly.
Always end your response with ANSWER: followed by the letter."""