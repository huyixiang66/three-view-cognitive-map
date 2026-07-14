# Three-View Cognitive Map

Three-view cognitive map: extends Thinking-in-Space's 1D CogMap to orthogonal three views (Top/Front/Side), with object size output.

## File Structure

`
.
├── viz/grid_visualizer.py      # 3-view visualization (emoji grid)
├── src/prompts_3pass.py        # 3-pass BEV-aligned prompt templates
├── src/vsi_subset_50.json      # 50 VSI-Bench samples
└── README.md
`

## Requirements

- Python 3.10+
- No external dependencies (uses only Python standard library)

## How to Run

### 1. Visualize Three-View Cognitive Map

`powershell
cd C:\Users\贝贝\Documents\Three-view Cognitive Map
python viz\grid_visualizer.py
`

Accepts JSON-formatted three-view input, outputs emoji grid:
- New format: {"gridSize": 10, "objects": [{"x":3,"y":5,"name":"table","size":[2,2]}]}
- Legacy format: [{"x":3,"y":5,"name":"table"}] (defaults to 10x10)

### 2. Prompt Templates

`python
from src.prompts_3pass import TOP_VIEW_PROMPT, FRONT_VIEW_PROMPT_SHARED, SIDE_VIEW_PROMPT_SHARED

# Generate Top View prompt
prompt = TOP_VIEW_PROMPT.format(video_input="scene description")
print(prompt)
`

4-pass prompt system:
- Pass 1: Top View (x-y plane, x-axis aligned with first frame of video)
- Pass 2: Front View (x-z plane, x-axis consistent with first frame)
- Pass 3: Side View (y-z plane)
- Pass 4: Answer (answer question based on three-view cognitive map)

Each object includes a size field representing grid cell coverage, e.g. {"name":"table","size":[2,2]}.

### 3. VSI-Bench Samples

src/vsi_subset_50.json contains 50 samples covering 5 question types:
- object_abs_distance (10 samples)
- object_rel_distance (10 samples)
- object_rel_direction_easy/medium/hard (30 samples)
