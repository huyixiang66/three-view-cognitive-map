# Prompts for the TIS-baseline vs three-view controlled comparison.

# Verbatim Cognitive Map prompt from Thinking in Space paper, Appendix B.4.
# Literal JSON braces in the example are escaped for str.format().
TIS_TOP_VIEW_PROMPT = """[Task] This video captures an indoor scene. Your objective is to identify specific objects within the video, understand the spatial arrangement of the scene, and estimate the center point of each object, assuming the entire scene is represented by a 10x10 grid.
[Rule]
1. We provide the categories to care about in this scene: {categories_of_interest}. Focus ONLY on these categories.
2. Estimate the center location of each instance within the provided categories, assuming the entire scene is represented by a 10x10 grid.
3. If a category contains multiple instances, include all of them.
4. Each object's estimated location should accurately reflect its real position in the scene, preserving the relative spatial relationships among all objects.
[Output] Present the estimated center locations for each object as a list within a dictionary. STRICTLY follow this JSON format: {{"category name": [(x_1, y_1), ...], ...}}"""

# Three-view extension: same wording, single pass, three orthogonal views, with size + room.
TIS_THREE_VIEW_PROMPT = """[Task] This video captures an indoor scene. Your objective is to identify specific objects within the video, understand the spatial arrangement of the scene, estimate the center point AND SIZE of each object in three orthogonal views, and estimate the room size, assuming each view is represented by a 10x10 grid.
[Rule]
1. We provide the categories to care about in this scene: {categories_of_interest}. Focus ONLY on these categories.
2. Estimate the center location and size (width x depth / width x height / depth x height in grid cells) of each instance in each view:
   - top view: [x, y, w, d] horizontal plane
   - front view: [x, z, w, h] horizontal x and height z
   - side view: [y, z, d, h] depth y and height z
3. If a category contains multiple instances, include all of them.
4. Each object's estimated location should accurately reflect its real position in the scene, preserving the relative spatial relationships among all objects.
5. Keep the same object consistent across views: top.x must match front.x, top.y must match side.y, front.z must match side.z.
6. Also estimate the room width/depth in grid cells and the approximate room area in square meters.
[Output] Present the estimated centers and sizes as a dictionary with three view keys plus a room key. STRICTLY follow this JSON format:
{{"top": {{"category name": [[x_1, y_1, w_1, d_1], ...], ...}}, "front": {{"category name": [[x_1, z_1, w_1, h_1], ...], ...}}, "side": {{"category name": [[y_1, z_1, d_1, h_1], ...], ...}}, "room": {{"width": w, "depth": d, "area_m2": a}}}}"""

# Three-pass extension: pass 2 front view, conditioned on the top view.
TIS_FRONT_VIEW_PASS2_PROMPT = """[Task] This video captures an indoor scene. You have already produced the TOP VIEW cognitive map below. Continue by producing the FRONT VIEW of the scene, estimating the center point and size of each object, assuming the front view is represented by a 10x10 grid.
TOP VIEW (already generated):
{top_view_result}
[Rule]
1. We provide the categories to care about in this scene: {categories_of_interest}. Focus ONLY on these categories.
2. Estimate the center location and size of each instance in the FRONT VIEW: [x, z, w, h], where x is the horizontal axis (SAME as the top view x) and z is the height (0=floor, 9=ceiling).
3. If a category contains multiple instances, include ALL of them, and the number of instances must MATCH the top view exactly.
4. For every object in the top view, its x in the front view must be the SAME as its x in the top view.
5. Each object's estimated location should accurately reflect its real position in the scene, preserving the relative spatial relationships among all objects.
[Output] Present the estimated centers and sizes as a dictionary. STRICTLY follow this JSON format: {{"category name": [[x_1, z_1, w_1, h_1], ...], ...}}"""

# Three-pass extension: pass 3 side view, conditioned on top and front views.
TIS_SIDE_VIEW_PASS3_PROMPT = """[Task] This video captures an indoor scene. You have already produced the TOP VIEW and FRONT VIEW cognitive maps below. Continue by producing the SIDE VIEW of the scene, estimating the center point and size of each object, assuming the side view is represented by a 10x10 grid.
TOP VIEW (already generated):
{top_view_result}
FRONT VIEW (already generated):
{front_view_result}
[Rule]
1. We provide the categories to care about in this scene: {categories_of_interest}. Focus ONLY on these categories.
2. Estimate the center location and size of each instance in the SIDE VIEW: [y, z, d, h], where y is the depth axis (SAME as the top view y) and z is the height (SAME as the front view z).
3. If a category contains multiple instances, include ALL of them, and the number of instances must MATCH the top view exactly.
4. For every object in the top view, its y in the side view must be the SAME as its y in the top view; its z in the side view must be the SAME as its z in the front view.
5. Each object's estimated location should accurately reflect its real position in the scene, preserving the relative spatial relationships among all objects.
[Output] Present the estimated centers and sizes as a dictionary. STRICTLY follow this JSON format: {{"category name": [[y_1, z_1, d_1, h_1], ...], ...}}"""

# Two-stage extension: stage 1 counts instances per category from the video.
TIS_COUNT_PROMPT = """[Task] This video captures an indoor scene. Your objective is to count how many instances of each provided category appear in the scene.
[Rule]
1. We provide the categories to care about in this scene: {categories_of_interest}. Focus ONLY on these categories.
2. Count ALL visible instances for every category. If a category contains multiple instances, include them all in the count.
3. Do not count objects that are not clearly part of the given categories.
[Output] Present the count for each category as a dictionary. STRICTLY follow this JSON format: {{"category name": count, ...}}"""

# Two-stage extension: stage 2 places exactly the counted instances into three views.
TIS_THREE_VIEW_WITH_COUNTS_PROMPT = """[Task] This video captures an indoor scene. Your objective is to identify specific objects within the video, understand the spatial arrangement of the scene, and estimate the center point of each object in three orthogonal views, assuming each view is represented by a 10x10 grid.
The instance counts below were estimated from the same video:
INSTANCE COUNTS: {instance_counts}
[Rule]
1. We provide the categories to care about in this scene: {categories_of_interest}. Focus ONLY on these categories.
2. For every category, you MUST place EXACTLY the number of instances given in INSTANCE COUNTS, in EVERY view.
3. Estimate the center location of each instance in each view:
   - top view: (x, y) horizontal plane
   - front view: (x, z) horizontal x and height z
   - side view: (y, z) depth y and height z
4. Keep the same object consistent across views: top.x must match front.x, top.y must match side.y, front.z must match side.z.
5. Each object's estimated location should accurately reflect its real position in the scene, preserving the relative spatial relationships among all objects.
[Output] Present the estimated center locations as a dictionary with three view keys. STRICTLY follow this JSON format:
{{"top": {{"category name": [(x_1, y_1), ...], ...}}, "front": {{"category name": [(x_1, z_1), ...], ...}}, "side": {{"category name": [(y_1, z_1), ...], ...}}}}"""

# Answer templates for question types beyond the original abs/rel distance / direction.
ANSWER_PROMPT_COUNTING = """Based on the cognitive map you built above, how many instances of the asked category appear in the scene? Count every instance in the map.
Question: {question}
Answer with a single integer number."""

ANSWER_PROMPT_SIZE = """Based on the cognitive map you built above, estimate the physical size of the asked object in the same units as the question (centimeters or meters as asked). Use the object sizes in the map (grid cells) and common reference sizes (e.g., a door is about 2m tall) to convert grid units to real units.
Question: {question}
Answer with a single number in the units requested by the question."""

ANSWER_PROMPT_ROOM = """Based on the cognitive map you built above, estimate the room size in the same units as the question (square meters or other units as asked), using the room width/depth and common reference sizes (e.g., a door is about 1m wide) to convert grid units to real units.
Question: {question}
Answer with a single number in the units requested by the question."""

ANSWER_PROMPT_ROUTE = """Based on the cognitive map you built above, choose the best answer for the navigation question using the object positions and directions in the map.
Question: {question}
Options:
{options}
Answer with the option letter."""

ANSWER_PROMPT_APPEARANCE = """Based on the video and the cognitive map you built above, determine the order in which the asked categories first appear in the video.
Question: {question}
Options:
{options}
Answer with the option letter."""
