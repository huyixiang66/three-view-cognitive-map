# Three-View Cognitive Map: 3-Pass BEV-Aligned Prompts

# === PASS 1: Top View (BEV) - establishes x-axis anchor ===
TOP_VIEW_PROMPT = '''You are a spatial reasoning assistant. Watch the video input below and build a COGNITIVE MAP.

[Video frames are attached as images below]

STEP 1 OF 3: Generate the TOP VIEW (Bird's-Eye View) cognitive map.
- The top view shows the scene from above
- X axis: horizontal (left-right in the scene)
- Y axis: depth (near-far in the scene)
- Grid size: 10x10 (coordinates 0-9)

List all significant objects with their (x, y) positions, names, and SIZE (how many grid cells the object occupies in width x depth).
Use standard object names (table, chair, door, window, sofa, bed, lamp, etc.)

Output format as JSON array:
[{{"x": 3, "y": 5, "name": "table", "size": [2, 2]}}, ...]

RULES:
- Place objects proportionally to their real-world positions
- Include estimated size for each object (width x depth in grid cells, e.g. [2, 2] for a table)
- Use integer coordinates 0-9
- Include ALL notable objects in the scene
- Output ONLY the JSON array, nothing else'''

# === PASS 2: Front View - uses top view as x-axis reference ===
FRONT_VIEW_PROMPT_SHARED = '''You are a spatial reasoning assistant. Continue building the cognitive map.

[Video frames are attached as images below]

PREVIOUS STEP - TOP VIEW (already generated):
{top_view_result}

STEP 2 OF 3: Generate the FRONT VIEW (elevation) cognitive map.
- The front view shows the scene from the front
- X axis: horizontal (SAME as top view x-axis)
- Z axis: height (floor-ceiling)
- Grid size: 10x10 (coordinates 0-9)

Use the first frame as the x-axis reference. The x-coordinate in the front view should be consistent with the first frame direction.
List all significant objects with their (x, z) positions, names, and SIZE (how many grid cells the object occupies in width x height).

Output format as JSON array:
[{{"x": 3, "z": 2, "name": "table", "size": [2, 1]}}, ...]

RULES:
- X axis MUST be consistent with the first frame of the video (right direction = positive x)
- Z coordinate represents height (0=floor, 9=ceiling)
- Output ONLY the JSON array, nothing else'''

FRONT_VIEW_PROMPT_NOSHARED = '''You are a spatial reasoning assistant. Watch the video description and generate the FRONT VIEW cognitive map.

[Video frames are attached as images below]

STEP 2 OF 3: Generate the FRONT VIEW (elevation) cognitive map.
- The front view shows the scene from the front
- X axis: horizontal (left-right)
- Z axis: height (floor-ceiling)
- Grid size: 10x10 (coordinates 0-9)

List all significant objects with their (x, z) positions, names, and SIZE (how many grid cells the object occupies in width x height).

Output format as JSON array:
[{{"x": 3, "z": 2, "name": "table", "size": [2, 1]}}, ...]

RULES:
- Use integer coordinates 0-9
- Z coordinate represents height (0=floor, 9=ceiling)
- Output ONLY the JSON array, nothing else'''

# === PASS 3: Side View - uses top view as y-axis reference ===
SIDE_VIEW_PROMPT_SHARED = '''You are a spatial reasoning assistant. Complete the cognitive map.

[Video frames are attached as images below]

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

Y axis is consistent with the first frame depth direction. Z axis is consistent with vertical direction.
List all significant objects with their (y, z) positions, names, and SIZE (how many grid cells the object occupies in depth x height).

Output format as JSON array:
[{{"y": 5, "z": 2, "name": "table", "size": [2, 1]}}, ...]

RULES:
- Y axis MUST be consistent with the first frame depth direction
- Z axis MUST be consistent with the vertical direction
- Output ONLY the JSON array, nothing else'''


# === SINGLE PASS: one call generates top/front/side views (TIS wording) ===
SINGLE_PASS_THREE_VIEW_PROMPT = """[Task] This video captures an indoor scene. Your objective is to identify specific objects within the video, understand the spatial arrangement of the scene, and estimate the center point of each object in three orthogonal views, assuming each view is represented by a 10x10 grid.
[Rule]
1. We provide the categories to care about in this scene: {categories_of_interest}. Focus ONLY on these categories.
2. Estimate the center location of each instance in each view:
   - top view: (x, y) horizontal plane
   - front view: (x, z) horizontal x and height z
   - side view: (y, z) depth y and height z
3. If a category contains multiple instances, include all of them.
4. Each object's estimated location should accurately reflect its real position in the scene, preserving the relative spatial relationships among all objects.
5. Keep the same object consistent across views: top.x must match front.x, top.y must match side.y, front.z must match side.z.
[Output] Present the estimated center locations as a dictionary with three view keys. STRICTLY follow this JSON format:
{{"top": {{"category name": [(x_1, y_1), ...], ...}}, "front": {{"category name": [(x_1, z_1), ...], ...}}, "side": {{"category name": [(y_1, z_1), ...], ...}}}}"""

SIDE_VIEW_PROMPT_NOSHARED = '''You are a spatial reasoning assistant. Generate the SIDE VIEW cognitive map.

[Video frames are attached as images below]

STEP 3 OF 3: Generate the SIDE VIEW (profile) cognitive map.
- The side view shows the scene from the right side
- Y axis: depth (near-far)
- Z axis: height (floor-ceiling)
- Grid size: 10x10 (coordinates 0-9)

List all significant objects with their (y, z) positions, names, and SIZE (how many grid cells the object occupies in depth x height).

Output format as JSON array:
[{{"y": 5, "z": 2, "name": "table", "size": [2, 1]}}, ...]

RULES:
- Use integer coordinates 0-9
- Output ONLY the JSON array, nothing else'''

# === ANSWER PROMPTS for each metric type ===

ANSWER_PROMPT_ABS_DISTANCE = '''QUESTION: {question}

Estimate the distance and provide your answer as a number in meters.
Answer with a single number (e.g., 2.5).
Always end your response with ANSWER: followed by the number.'''

ANSWER_PROMPT_REL_DISTANCE = '''QUESTION: {question}

{options}

Compare the distances and provide your answer.
Answer with the option letter (A, B, C, or D).
Always end your response with ANSWER: followed by the letter.'''

ANSWER_PROMPT_REL_DIRECTION = '''QUESTION: {question}

{options}

Determine the relative direction and provide your answer.
Use the TOP view coordinates: let S be the standing object and F the facing object, with F_vec = F - S. For each candidate T, the object is to your LEFT if cross(F_vec, T_vec) = Fx*Ty - Fy*Tx is positive, RIGHT if negative, and BACK if the dot product F_vec . T_vec is negative.
Answer with the option letter (A, B, C, or D).
Always end your response with ANSWER: followed by the letter.'''

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


ANSWER_PROMPT_ABS_DISTANCE_SELFCHECK = """Here is a visualization of the three-view cognitive map you built.

STEP 1 (VERIFY): Examine the visualization carefully. Check:
- In the Top View, are all objects placed correctly relative to each other?
- In the Front View, do x-coordinates match those in the Top View for the same objects?
- In the Side View, do y-coordinates match the Top View and z-coordinates match the Front View?
- If any object appears inconsistent across views, mentally correct its position.

STEP 2 (ANSWER): Based on your verified cognitive map, answer the question.

QUESTION: {question}

Estimate the distance and provide your answer as a number in meters.
Always end your response with ANSWER: followed by the number."""


ANSWER_PROMPT_REL_DISTANCE_SELFCHECK = """Here is a visualization of the three-view cognitive map you built.

STEP 1 (VERIFY): Examine the visualization carefully. Check:
- Are all objects placed consistently across the three views?
- In the Front View, do x-coordinates match those in the Top View?
- In the Side View, do y-coordinates match the Top View and z-coordinates match the Front View?
- If any object appears inconsistent across views, mentally correct its position.

STEP 2 (ANSWER): Based on your verified cognitive map, answer the question.

QUESTION: {question}
{options}

Answer with the option letter (A, B, C, or D).
Always end your response with ANSWER: followed by the letter."""


ANSWER_PROMPT_REL_DIRECTION_SELFCHECK = """Here is a visualization of the three-view cognitive map you built.

STEP 1 (VERIFY): Examine the visualization carefully. Check:
- Are all objects placed consistently across the three views?
- In the Front View, do x-coordinates match those in the Top View?
- In the Side View, do y-coordinates match the Top View and z-coordinates match the Front View?
- If any object appears inconsistent across views, mentally correct its position.

STEP 2 (ANSWER): Based on your verified cognitive map, answer the question.

QUESTION: {question}
{options}

Answer with the option letter (A, B, C, or D).
Always end your response with ANSWER: followed by the letter."""


# === TASK-AWARE variants: injects question info into Pass 1-3 ===
TOP_VIEW_PROMPT_TASK_AWARE = '''You are a spatial reasoning assistant. Watch the video input below and build a COGNITIVE MAP.

You will later need to answer this question:
{question}

[Video frames are attached as images below]

STEP 1 OF 3: Generate the TOP VIEW (Bird's-Eye View) cognitive map.
- The top view shows the scene from above
- X axis: horizontal (left-right in the scene)
- Y axis: depth (near-far in the scene)
- Grid size: 10x10 (coordinates 0-9)

Your cognitive map MUST include the objects mentioned in the question above, plus any other significant objects in the scene.
For each object, provide (x, y) positions, names, and SIZE (how many grid cells the object occupies in width x depth).

Output format as JSON array:
[{{"x": 3, "y": 5, "name": "table", "size": [2, 2]}}, ...]

RULES:
- You MUST include the objects relevant to the question, or the answer will be wrong
- Place objects proportionally to their real-world positions
- Include estimated size for each object
- Use integer coordinates 0-9
- Output ONLY the JSON array, nothing else'''


FRONT_VIEW_PROMPT_SHARED_TASK_AWARE = '''You are a spatial reasoning assistant. Continue building the cognitive map.

You will later need to answer this question:
{question}

[Video frames are attached as images below]

PREVIOUS STEP - TOP VIEW (already generated):
{top_view_result}

STEP 2 OF 3: Generate the FRONT VIEW (elevation) cognitive map.
- The front view shows the scene from the front
- X axis: horizontal (SAME as top view x-axis)
- Z axis: height (floor-ceiling)
- Grid size: 10x10 (coordinates 0-9)

You MUST include the same objects from the question that appeared in the Top View, with consistent x-coordinates.
List all significant objects with their (x, z) positions, names, and SIZE (how many grid cells the object occupies in width x height).

Output format as JSON array:
[{{"x": 3, "z": 2, "name": "table", "size": [2, 1]}}, ...]

RULES:
- X axis MUST be consistent with the first frame of the video
- Z coordinate represents height (0=floor, 9=ceiling)
- Output ONLY the JSON array, nothing else'''


SIDE_VIEW_PROMPT_SHARED_TASK_AWARE = '''You are a spatial reasoning assistant. Complete the cognitive map.

You will later need to answer this question:
{question}

[Video frames are attached as images below]

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

You MUST include the objects from the question with consistent y and z coordinates.
List all significant objects with their (y, z) positions, names, and SIZE (how many grid cells the object occupies in depth x height).

Output format as JSON array:
[{{"y": 5, "z": 2, "name": "table", "size": [2, 1]}}, ...]

RULES:
- Y axis MUST be consistent with the first frame depth direction
- Z axis MUST be consistent with the vertical direction
- Output ONLY the JSON array, nothing else'''
