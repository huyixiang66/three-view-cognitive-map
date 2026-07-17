# Three-View Cognitive Map

Extends Thinking-in-Space 1D CogMap to orthogonal three views (Top/Front/Side) with object size output. Built for the VSI-Bench spatial reasoning benchmark.

## Quick Start

```bash
# 1. Set API keys (or copy .env.example)
export WELLAPI_API_KEY="sk-your-key"
export DASHSCOPE_API_KEY="sk-your-key"
export OPENAI_API_KEY="sk-your-key"

# 2. Run
cd src
python run_vsibench.py --model deepseek-v3 --mode vlm_shared --n 50 --sleep 3
```

## Usage

### Run VSI-Bench evaluation

```bash
python run_vsibench.py \
    --model <model_name> \
    --mode <vlm_shared|vlm_noshared> \
    --n 50 \
    --sleep 3 \
    --output results.json \
    --verbose
```

### Models

Configured in `MODEL_REGISTRY` in `run_vsibench.py`. API keys are read from environment variables:

| Name | Env Var | Endpoint |
|------|---------|----------|
| `deepseek-v3` | `WELLAPI_API_KEY` | wellapi.ai |
| `qwen-plus` | `DASHSCOPE_API_KEY` | aliyuncs.com |
| `qwen-turbo` | `DASHSCOPE_API_KEY` | aliyuncs.com |
| `gpt-4o` | `OPENAI_API_KEY` | api.openai.com |
| `gemini-3.5-flash` | `WELLAPI_API_KEY` | wellapi.ai |

Add new models by appending to `MODEL_REGISTRY`.

### Modes

- **`vlm_shared`**: All 3-pass cogmap generation + question answering in one continuous conversation. The model "remembers" generating the map.
- **`vlm_noshared`**: Phase 1 (3-pass cogmap generation) and Phase 2 (answering) are separate sessions. Only the cogmap text is passed to Phase 2.

### Pipeline

Each sample runs 4 API calls:

1. **Pass 1 - Top View**: Birds-eye (x-y), first frame anchors x-axis
2. **Pass 2 - Front View**: Elevation (x-z), uses Pass 1 x-axis
3. **Pass 3 - Side View**: Profile (y-z), uses Pass 1 y-axis + Pass 2 z-axis
4. **Answer**: Spatial reasoning question from VSI-Bench

### Visualizer

```bash
python ../viz/grid_visualizer.py
```

Renders three-view cogmap JSON as emoji grids.

## File Structure

```
.
+-- src/
|   +-- run_vsibench.py        # Main experiment pipeline
|   +-- prompts_3pass.py       # 3-pass prompt templates
|   +-- meta_to_cogmap.py      # Oracle baseline (unused in VLM modes)
|   +-- vsi_subset_50.json     # 50 VSI-Bench samples
+-- viz/
|   +-- grid_visualizer.py     # Emoji grid visualizer
+-- README.md
+-- plan.md
```

## Data

`vsi_subset_50.json` covers 5 question types:

| Type | Samples | Example |
|------|---------|---------|
| `object_abs_distance` | 10 | How far between objects A and B? |
| `object_rel_distance` | 10 | Which is closer, A to B or C to D? |
| `object_rel_direction_easy` | 7 | Is A left/right of B? |
| `object_rel_direction_medium` | 11 | In what direction is A from B? |
| `object_rel_direction_hard` | `object_rel_direction_hard` | 12 | Fine-grained directional judgment |

Ground truth: distances in meters, directions as option letters (A/B/C/D).

## Citation

Based on the Thinking-in-Space framework. Scene data from ScanNet, ScanNet++, and ARKitScenes.
