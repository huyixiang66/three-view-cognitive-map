# Three-View Cognitive Map: 3-Pass BEV-Aligned Prompts

# === PASS 1: Top View (BEV) - establishes x-axis anchor ===
TOP_VIEW_PROMPT = '''You are a spatial reasoning assistant. Watch the video input below and build a COGNITIVE MAP.

VIDEO INPUT:
{video_input}

STEP 1 OF 3: Generate the TOP VIEW (Bird's-Eye View) cognitive map.
- The top view shows the scene from above
- X axis: horizontal (left-right in the scene)
- Y axis: depth (near-far in the scene)
- Grid size: 10x10 (coordinates 0-9)

List all significant objects with their (x, y) positions and names.
Use standard object names (table, chair, door, window, sofa, bed, lamp, etc.)

Output format as JSON array:
[{{"x": 3, "y": 5, "name": "table"}}, ...]

RULES:
- Place objects proportionally to their real-world positions
- Use integer coordinates 0-9
- Include ALL notable objects in the scene
- Output ONLY the JSON array, nothing else'''

# === PASS 2: Front View - uses top view as x-axis reference ===
FRONT_VIEW_PROMPT_SHARED = '''You are a spatial reasoning assistant. Continue building the cognitive map.

VIDEO INPUT:
{video_input}

PREVIOUS STEP - TOP VIEW (already generated):
{top_view_result}

STEP 2 OF 3: Generate the FRONT VIEW (elevation) cognitive map.
- The front view shows the scene from the front
- X axis: horizontal (SAME as top view x-axis)
- Z axis: height (floor-ceiling)
- Grid size: 10x10 (coordinates 0-9)

Use the top view X positions as anchors. Objects at x=3 in top view should also be at x=3 in front view.
List all significant objects with their (x, z) positions.

Output format as JSON array:
[{{"x": 3, "z": 2, "name": "table"}}, ...]

RULES:
- X coordinates MUST match the top view for the same object
- Z coordinate represents height (0=floor, 9=ceiling)
- Output ONLY the JSON array, nothing else'''

FRONT_VIEW_PROMPT_NOSHARED = '''You are a spatial reasoning assistant. Watch the video description and generate the FRONT VIEW cognitive map.

VIDEO INPUT:
{video_input}

STEP 2 OF 3: Generate the FRONT VIEW (elevation) cognitive map.
- The front view shows the scene from the front
- X axis: horizontal (left-right)
- Z axis: height (floor-ceiling)
- Grid size: 10x10 (coordinates 0-9)

List all significant objects with their (x, z) positions.

Output format as JSON array:
[{{"x": 3, "z": 2, "name": "table"}}, ...]

RULES:
- Use integer coordinates 0-9
- Z coordinate represents height (0=floor, 9=ceiling)
- Output ONLY the JSON array, nothing else'''

# === PASS 3: Side View - uses top view as y-axis reference ===
SIDE_VIEW_PROMPT_SHARED = '''You are a spatial reasoning assistant. Complete the cognitive map.

VIDEO INPUT:
{video_input}

PREVIOUS STEPS:
TOP VIEW (x-y plane):
{top_view_result}

FRONT VIEW (x-z plane):
{front_view_result}

STEP 3 OF 3: Generate the SIDE VIEW (profile) cognitive map.
- The side view shows the scene from the right side
- Y axis: depth (near-far, SAME as top view y-axis)
- Z axis: height (SAME as front view z-axis)
- Grid size: 10x10 (coordinates 0-9)

Use the top view Y positions AND front view Z positions as anchors.
List all significant objects with their (y, z) positions.

Output format as JSON array:
[{{"y": 5, "z": 2, "name": "table"}}, ...]

RULES:
- Y coordinates MUST match top view for the same object
- Z coordinates MUST match front view for the same object
- Output ONLY the JSON array, nothing else'''

SIDE_VIEW_PROMPT_NOSHARED = '''You are a spatial reasoning assistant. Generate the SIDE VIEW cognitive map.

VIDEO INPUT:
{video_input}

STEP 3 OF 3: Generate the SIDE VIEW (profile) cognitive map.
- The side view shows the scene from the right side
- Y axis: depth (near-far)
- Z axis: height (floor-ceiling)
- Grid size: 10x10 (coordinates 0-9)

List all significant objects with their (y, z) positions.

Output format as JSON array:
[{{"y": 5, "z": 2, "name": "table"}}, ...]

RULES:
- Use integer coordinates 0-9
- Output ONLY the JSON array, nothing else'''

# === ANSWER PROMPTS for each metric type ===

ANSWER_PROMPT_ABS_DISTANCE = '''Based on the three-view cognitive map below, answer the question.

FRONT VIEW (x-z plane):
{front_view}

TOP VIEW (x-y plane):
{top_view}

SIDE VIEW (y-z plane):
{side_view}

QUESTION: {question}

Estimate the distance and provide your answer as a number in meters.
Answer with a single number (e.g., 2.5).'''

ANSWER_PROMPT_REL_DISTANCE = '''Based on the three-view cognitive map below, answer the question.

FRONT VIEW (x-z plane):
{front_view}

TOP VIEW (x-y plane):
{top_view}

SIDE VIEW (y-z plane):
{side_view}

QUESTION: {question}

Compare the distances and provide your answer.
Answer with A or B.'''

ANSWER_PROMPT_REL_DIRECTION = '''Based on the three-view cognitive map below, answer the question.

FRONT VIEW (x-z plane):
{front_view}

TOP VIEW (x-y plane):
{top_view}

SIDE VIEW (y-z plane):
{side_view}

QUESTION: {question}

Determine the relative direction and provide your answer.
Answer with the option letter (A, B, C, or D).'''

# === BASELINE PROMPTS (no cognitive map) ===

BASELINE_ABS_DISTANCE = '''QUESTION: {question}

Estimate the distance directly from the video description.
Answer with a single number in meters.'''

BASELINE_REL_DISTANCE = '''QUESTION: {question}

Compare the distances directly from the video description.
Answer with A or B.'''

BASELINE_REL_DIRECTION = '''QUESTION: {question}

Determine the relative direction directly from the video description.
Answer with the option letter (A, B, C, or D).'''
