# Three-View Cognitive Map

基于VLM从视频构建三视图认知地图（Top/Front/Side），在 VSI-Bench 上做空间推理。

## 输入输出

- 输入: 视频 + VSI-Bench 空间问题
- 输出: 三视图 JSON 坐标 + 答案

Pipeline:

1. Pass 1: 视频 -> Top View JSON (x, y, size)
2. Pass 2: Top View -> Front View JSON (x, z, size)
3. Pass 3: Top + Front -> Side View JSON (y, z, size)
4. Pass 4: cogmap -> 回答空间问题

## 快速开始

```bash
# 1. 配置 API key
cp .env.example .env   # 填入 BOYUE_API_KEY

# 2. 下载 VSI-Bench 视频（自动下载 50 样本所需）
python scripts/download_videos.py

# 3. 运行
cd src
python run_vsibench.py --model gemini-3.5-flash --mode vlm_shared --n 50
```

## 参数说明

| 参数 | 作用 |
|------|------|
| `--mode vlm_shared` | 同一会话（模型有视频记忆） |
| `--mode vlm_noshared` | 新会话（只给 cogmap 文本，不给视频） |
| `--viz` | Pass 4 添加 matplotlib PNG 可视化图 |
| `--taskaware` | 建图 prompt 注入题目，提升目标物体召回 |
| `--facts` | Pass 4 注入脚本计算的空间事实（坐标/方向） |
| `--sleep 3` | API 调用间隔秒数 |
| `--verbose` | 打印详细输出 |

示例：

```bash
# 完整 50 样本（shared + taskaware + facts）
python run_vsibench.py --model gemini-3.5-flash --mode vlm_shared --taskaware --facts --n 50
```

## 可视化

```bash
cd viz
python matplotlib_visualizer.py output.png
```

生成三视图（Top/Front/Side）网格图，物体使用 PNG 图标渲染（`viz/icons/`）。

## 数据

`src/vsi_subset_50.json` 包含 50 个 VSI-Bench 样本，5 种题型：

| 题型 | 数量 | 答案格式 |
|------|------|----------|
| object_abs_distance | 10 | 数值（米） |
| object_rel_distance | 10 | 选择题 (A-D) |
| object_rel_direction_easy | 7 | 选择题 (A-D) |
| object_rel_direction_medium | 11 | 选择题 (A-D) |
| object_rel_direction_hard | 12 | 选择题 (A-D) |

完整 VSI-Bench: https://huggingface.co/datasets/nyu-visionx/VSI-Bench

## 文件结构

```
.
+-- src/
|   +-- run_vsibench.py        # 主实验 pipeline
|   +-- prompts_3pass.py       # 3-pass prompt 模板
|   +-- vsi_subset_50.json     # 50 个 VSI-Bench 样本
|   +-- reevaluate.py          # VSI-Bench MRA 评估
|   +-- meta_to_cogmap.py      # Oracle 基线转换器
+-- scripts/
|   +-- download_videos.py     # 视频下载脚本
+-- viz/
|   +-- matplotlib_visualizer.py  # 三视图可视化
|   +-- icons/                    # 物体 PNG 图标
+-- .env.example               # API key 模板
+-- README.md
```

## 依赖

```bash
pip install openai matplotlib
```
