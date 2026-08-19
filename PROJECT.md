# Unity Spatial Replay — Project Wiki（原 Three-View Cognitive Map，名称待定）

> Last synced: 2026-08-07

## One-Line Summary
目标：提升 VLM 在 VSI-Bench 空间 QA 上的表现。
路线：用 Unity 构建空间表示，模拟相机位姿重放原视频路径，通过反馈验证迭代空间理解，最终回答空间问题。

## Current Stage
当前并行两条线：1) Unity 空间重放（M0 待落地，见 docs/unity-pipeline-design.md）；2) 认知图建图分析（已对齐 GT 坐标系并完成 50 样本地图级分析，发现系统性偏右/偏高偏置）。下一步：从 VSI-Bench 扩样 200 条（8 类×25，分层随机），复跑 4 个 arm 并做对齐后分题型分析（见 docs/plan-2026-08-07.md）。

## Core Closed Loop
`Video/观测 → 构建 Unity 空间表示 → 模拟相机位姿重走路径 → 渲染对比/反馈 → 迭代表示 → VSI-Bench QA`

## Legacy Results（三视图路线，gemini-3.5-flash / 50 样本）

| Experiment | Overall | Notes |
|---|---|---|
| shared (no viz, no taskaware) | 52.7% | 基线最好 |
| 3-pass shared | 44.9% | report.md 口径 |
| direct (no map) | 36-39.4% | |
| noshared + taskaware | 40% | 100% 物体召回 |
| shared + taskaware + viz + facts (dir_easy) | 57% | 仅方向 easy 子集 |

核心结论：
- task-aware 建图 = 100% 召回，是三视图路线最大突破
- viz 是噪声；facts 依赖坐标精度
- 瓶颈是坐标精度 → 需要精确 3D/模拟环境，这也是换 Unity 的原因

## What Carries Over
- VSI-Bench 评测 harness、50 样本子集、结果格式
- task-aware 思想：把问题注入表示构建过程
- 模型 API 网关接入
- 相关论文调研（论文对比完整版.txt）

## Module Map

| 模块 | 状态 |
|---|---|
| VSI-Bench 评测 harness | 复用 |
| 视频采样/接入 | 复用 |
| Unity 空间表示 | 设计完成，M0 待落地 |
| 相机位姿恢复/模拟 | 三方案已定，待试点 |
| 渲染-反馈闭环 | 设计完成，待搭建 |
| VLM QA 回答 | 复用 |

## Key Files

| File | Purpose |
|---|---|
| docs/unity-closed-loop-direction.md | 新方向设计文档（交接核心） |
| session-handoff.md | 会话交接 |
| src/run_vsibench.py | 旧三视图主管线 |
| src/reevaluate.py | VSI-Bench 评测 |
| src/vsi_subset_50.json | 50 样本评测集 |
| 论文对比完整版.txt | 相关论文调研 |
