# Three-View Cognitive Map

基于 Gemini-3.5-flash 从视频构建三视图认知地图（Top/Front/Side），在 VSI-Bench 上做空间推理。

## 输入输出

- 输入: 视频 + VSI-Bench 空间问题
- 输出: 三视图 JSON 坐标 + 答案
- QA 阶段: 同时输入视频 + 三视图 map（视频记忆）

Pipeline:

1. Pass 1: 视频 -> Top View JSON (x, y, size)
2. Pass 2: Top View -> Front View JSON (x, z, size)
3. Pass 3: Top + Front -> Side View JSON (y, z, size)
4. Pass 4: 视频 + cogmap -> 回答空间问题（视频记忆）

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
| `--mode vlm_noshared` | 新会话（给 cogmap 文本 + 视频） |
| `--mode vlm_noshared_video` | 等价别名：cogmap + 视频 |
| `--taskaware` | 建图 prompt 注入题目，提升目标物体召回 |
| `--viz` | Pass 4 添加 matplotlib PNG 可视化图 |
| `--facts` | Pass 4 注入脚本计算的空间事实（坐标/方向） |
| `--resume file.json` | 从 partial 结果断点续跑 |
| `--samples file.json` | 指定样本文件（默认 vsi_subset_50.json） |
| `--sleep 3` | API 调用间隔秒数 |
| `--verbose` | 打印详细输出 |

示例：

```bash
# 完整 50 样本（shared + taskaware + facts）
python run_vsibench.py --model gemini-3.5-flash --mode vlm_shared --taskaware --facts --n 50

# 断点续跑
python run_vsibench.py --model gemini-3.5-flash --mode vlm_shared --resume results_xxx_partial_30.json --n 50
```

## 可视化

```bash
cd viz
python matplotlib_visualizer.py output.png
```

生成三视图（Top/Front/Side）网格图，物体使用 PNG 图标渲染（`viz/icons/`）。

## TIS 对照实验（200 样本）

对比 TIS baseline / three-view / three-view 3-pass 三种建图方式：

```bash
cd src
python run_tis_compare.py --arm all --mode shared --samples vsi_subset_200.json --n 200
```

| 参数 | 作用 |
|------|------|
| `--arm baseline` | 只跑 TIS TOP 单视图 |
| `--arm threeview` | 单次三视图（含 size/room） |
| `--arm threeview_3pass` | 三次调用分别建 TOP/FRONT/SIDE |
| `--mode shared` | 回答复用建图会话 |
| `--mode noshared` | 新会话回答，给视频 + 地图文本 |
| `--n 200` | 样本数 |

GT 地图需要 `TIS_META_DIR` 指向 TIS 复现仓库的 meta_info 目录；meta JSON 不随仓库上传。

统一 clean 回答阶段（`run_clean_answer.py`）和 debate 的回答阶段都会同时提供视频与三视图 map；
输出保留 Unity 兼容字段 `cogmap_objects`（`view/name/x/y/z` 扁平列表）和 `api_calls`。
所有 arm 统一口径：建图只画题目相关的 QA 物体（TIS 风格 `Focus ONLY on these categories`）；
`room` 随三视图同一次调用生成；`appearance` / `route` 只在对应题型通过额外视频调用生成字段。

## 多 agent debate（干净协议）

三视图多 agent 变体：独立 agent + 顺序参考建图，回答统一走 clean 协议（新会话给视频 + 地图文本）。矩阵 debate 使用融合投影 + 变换矩阵互评，简单 debate 使用共享轴偏移互评。

```bash
cd src
# 简单 debate
python run_debate_clean.py --strategy ref_simple_debate --samples vsi_debate_50.json --n 50 --output results_debate_clean_s7_50.json
# 矩阵 debate
python run_debate_clean.py --strategy ref_matrix_debate --samples vsi_debate_50.json --n 50 --output results_debate_clean_s5_50.json
```

| 参数 | 作用 |
|------|------|
| `--strategy ref_matrix_debate` | 矩阵 debate：融合参考重投影 + 变换矩阵互评 |
| `--strategy ref_no_debate` | 独立建图无 debate（对照） |
| `--strategy ref_simple_debate` | 简单 debate：共享轴偏移互评 |
| `--strategy` 也兼容旧数字 5/6/7 | 便于旧脚本迁移 |
| `--samples vsi_debate_50.json` | 50 个 VSI-Bench 样本 |
| `--n 50` | 样本数 |
| `--output xxx.json` | 结果文件 |

GT 指标需要 `TIS_META_DIR`；未配置 meta 时仍可跑建图与回答，只跳过 GT 地图指标。

## 数据

`src/vsi_subset_50.json` 包含 50 个 VSI-Bench 样本，5 种题型：

| 题型 | 数量 | 答案格式 |
|------|------|----------|
| object_abs_distance | 10 | 数值（米） |
| object_rel_distance | 10 | 选择题 (A-D) |
| object_rel_direction_easy | 7 | 选择题 (A-D) |
| object_rel_direction_medium | 11 | 选择题 (A-D) |
| object_rel_direction_hard | 12 | 选择题 (A-D) |

`src/vsi_subset_200.json` 包含 200 个 VSI-Bench 样本，8 类题型各 25 条（含 size/room）。

`src/vsi_debate_50.json` 为多 agent debate 使用的 50 个 VSI-Bench 样本（8 类题型）。

完整 VSI-Bench: https://huggingface.co/datasets/nyu-visionx/VSI-Bench

## 文件结构

```
.
+-- src/
|   +-- run_vsibench.py        # 主实验 pipeline
|   +-- run_tis_compare.py     # TIS baseline vs 三视图对照（200 样本）
|   +-- run_debate_clean.py    # 多 agent debate（简单/矩阵）runner
|   +-- run_clean_answer.py    # 统一 clean 回答阶段
|   +-- camera_utils.py        # 相机矩阵工具
|   +-- prompts_3pass.py       # 3-pass prompt 模板
|   +-- tis_compare.py         # 核心库（GT 地图/指标/API）
|   +-- tis_prompts.py         # 单次三视图 size/room prompt
|   +-- vsi_subset_50.json     # 50 个 VSI-Bench 样本
|   +-- vsi_subset_200.json    # 200 个 VSI-Bench 样本
|   +-- vsi_debate_50.json     # 50 个 debate 样本
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
pip install openai numpy matplotlib
```
