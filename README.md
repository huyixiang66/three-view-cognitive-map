# Three-View Cognitive Map

Extends Thinking-in-Space 1D CogMap to orthogonal three views (Top/Front/Side) with object size output.

## File Structure

```
.
+-- viz/grid_visualizer.py      # 3-view visualization (emoji grid)
+-- src/prompts_3pass.py        # 3-pass BEV-aligned prompt templates
+-- src/vsi_subset_50.json      # 50 VSI-Bench samples
+-- README.md
```

## Requirements

- Python 3.10+
- No external dependencies

## How to Run

### 1. Visualize Three-View Cognitive Map

```bash
python viz/grid_visualizer.py
```

Accepts JSON-formatted three-view input, outputs emoji grid.

### 2. Prompt Templates

```python
from src.prompts_3pass import TOP_VIEW_PROMPT

prompt = TOP_VIEW_PROMPT.format(video_input="scene description")
print(prompt)
```

4-pass prompt system with object size (grid cell coverage) for each object.

### 3. VSI-Bench Samples

src/vsi_subset_50.json contains 50 samples covering 5 question types:
- object_abs_distance (10 samples)
- object_rel_distance (10 samples)
- object_rel_direction_easy/medium/hard (30 samples)
