# Three-View Cognitive Map

Extends Thinking-in-Space 1D CogMap to orthogonal three views (Top/Front/Side) with object size output. Built for the VSI-Bench spatial reasoning benchmark.

## Quick Start

```bash
# 1. Set API keys (copy .env.example to .env and edit)
export WELLAPI_API_KEY="sk-your-wellapi-key"
export DASHSCOPE_API_KEY="sk-your-dashscope-key"
export OPENAI_API_KEY="sk-your-openai-key"

# 2. Run (default: deepseek-v3 via wellapi, shared memory, 50 samples)
cd src
python run_vsibench.py --model deepseek-v3 --mode vlm_shared --n 50 --sleep 3
```

## Usage

### Setup

1. **Get an API key** from one of the supported providers.
2. **Set environment variables** or create `.env` file in the project root (see `.env.example`).
3. **Install dependencies**: ``pip install openai``

The script auto-loads `.env` from the project root on startup.

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

Configured in `MODEL_REGISTRY` in `run_vsibench.py`. To add a new model, append an entry with provider, api_key env var name, base_url, and model name.

Pre-configured models:

| Model | Env Var | Endpoint |
|-------|---------|----------|
| `deepseek-v3` | `WELLAPI_API_KEY` | wellapi.ai |
| `qwen-plus` | `DASHSCOPE_API_KEY` | dashscope.aliyuncs.com |
| `qwen-turbo` | `DASHSCOPE_API_KEY` | dashscope.aliyuncs.com |
| `gpt-4o` | `OPENAI_API_KEY` | api.openai.com |
| `gemini-3.5-flash` | `WELLAPI_API_KEY` | wellapi.ai (OpenAI-compatible) |

To add a new model, edit `MODEL_REGISTRY`:

```python
MODEL_REGISTRY['my-model'] = {
    'provider': 'openai',
    'api_key': os.environ.get('MY_API_KEY', ''),
    'base_url': 'https://my-api-endpoint.com/v1',
    'model': 'my-model-name',
}
```

### Modes

- **``vlm_shared``**: All 3-pass cogmap generation + question answering in one continuous conversation session. The model "remembers" generating the map.
- **``vlm_noshared``**: Phase 1 (3-pass cogmap generation) and Phase 2 (answering) are separate sessions. Only the generated cogmap text is passed to Phase 2.

### Pipeline

Each sample runs 4 API calls:

1. **Pass 1 - Top View**: Bird's-eye (x-y plane)
2. **Pass 2 - Front View**: Elevation (x-z plane), uses Pass 1 x-axis alignment
3. **Pass 3 - Side View**: Profile (y-z plane), uses Pass 1 y-axis + Pass 2 z-axis
4. **Answer**: Answer VSI-Bench spatial reasoning question using the built cogmap

### Visualizer

```bash
python ../viz/grid_visualizer.py
```

Renders three-view cogmap JSON as emoji grids in the terminal.

## File Structure

```
.
+-- src/
|   +-- run_vsibench.py        # Main experiment pipeline
|   +-- prompts_3pass.py       # 3-pass prompt templates
|   +-- meta_to_cogmap.py      # Oracle baseline (uses GT 3D metadata, unused in VLM pipeline)
|   +-- vsi_subset_50.json     # 50 VSI-Bench samples
+-- viz/
|   +-- grid_visualizer.py     # Emoji grid visualizer
+-- .env.example               # API key template (copy to .env)
+-- README.md
```

## Data

`vsi_subset_50.json` covers 5 question types from VSI-Bench (subset of the full benchmark, 50 samples):

| Type | Samples | Answer Format |
|------|---------|---------------|
| `object_abs_distance` | 10 | Numerical (meters) |
| `object_rel_distance` | 10 | Multiple choice (A-D) |
| `object_rel_direction_easy` | 7 | Multiple choice (A-D) |
| `object_rel_direction_medium` | 11 | Multiple choice (A-D) |
| `object_rel_direction_hard` | 12 | Multiple choice (A-D) |

Full VSI-Bench dataset with videos: https://huggingface.co/datasets/nyu-visionx/VSI-Bench

## Known Limitations

1. **No actual video input**: The pipeline passes only a scene name string to the model (e.g., "09c1414f1b"). The VLM generates a cognitive map from general knowledge of typical room layouts, not from actual video frames. This fundamentally limits spatial accuracy, especially for absolute distance estimation.

2. **No visual grounding**: Unlike the original Thinking-in-Space approach (which samples 32 frames from the actual video and passes them through the vision encoder), our pipeline has zero visual input. The model is effectively guessing plausible layouts, not "seeing" the space.

3. **Small sample size**: 50 samples is a small subset of VSI-Bench (which has 5000+ QA pairs). Results may have high variance, especially for per-type breakdowns with as few as 7 samples per category.

4. **Synthetic cognitive maps**: The model outputs explicit JSON coordinate arrays, but these are generated from text priors alone. Their consistency across three views (top/front/side) has not been systematically validated.

5. **Single model focus**: Current benchmarks focus on gemini-3.5-flash. Results may differ significantly with stronger models (gpt-4o, deepseek-v3) or models with native video support.

## Results (gemini-3.5-flash, vlm_shared mode)

- **Overall accuracy**: 41.9% (18/43 completed, 7 skipped due to cogmap parse failures)
- `object_rel_distance`: 40% (improved from 0% after prompt fix)
- `object_rel_direction_easy`: 57%
- `object_rel_direction_medium`: 36%
- `object_rel_direction_hard`: 33%
- `object_abs_distance`: 20%

## Citation

Based on the Thinking-in-Space framework (CVPR 2025 Oral). Scene data from ScanNet, ScanNet++, and ARKitScenes. VSI-Bench: https://arxiv.org/abs/2412.14171
