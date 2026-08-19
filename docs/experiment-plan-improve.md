# Code Experiment Plan — 三视图漏画修复（两阶段计数）与后续改进路线

## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: plan
- Origin Date: 2026-08-06
- Verification Status: UNVERIFIED
- Version Label: code_plan_v2

## Experiment Overview

- **Title**: 两阶段计数约束是否解决三视图漏画实例（A1/C7）并提升 QA
- **Objective**: 验证“先数实例数、再按数量摆坐标”能否把漏画率压下来，且不伤害回答正确率
- **Hypothesis**: 漏画主要是 VLM 的“计数/记账”问题，不是感知看不到；给显式实例数约束后 A1/C7 显著下降，QA 持平或提升
- **Type**: analysis（LLM 实验，非训练）

## Setup

- **Language/Framework**: Python 3.13，openai
- **Entry Command**:
  ```bash
  python run_tis_compare.py --arm threeview_2stage --mode shared --output results_tis_threeview_2stage.json
  ```
- **Working Directory**: `C:\Users\贝贝\Documents\Three-view Cognitive Map\src`
- **Dependencies**: 现有 `tis_compare.py` / `tis_prompts.py` / `run_tis_compare.py`，无需新增
- **Environment**: 本机；每 5 样本自动保存 partial，可 `--resume`

## Inputs

| Input | Path | Description |
|-------|------|-------------|
| 50 样本 | `src/vsi_subset_50.json` | VSI-Bench 评测集 |
| GT 地图 | `Thinking in Space复现/thinking-in-space/data/meta_info/*.json` | 三视图 GT |
| 对照组结果 | `src/results_tis_compare.json` | baseline / threeview 单次 |
| 对照组结果 | `src/results_tis_threeview_3pass.json` | threeview 3-pass |

## Expected Outputs

| Output | Path | Format | Success Criterion |
|--------|------|--------|------------------|
| 两阶段结果 | `src/results_tis_threeview_2stage.json` | JSON | 文件存在，50 条无 error 记录 |
| 中间保存 | `src/results_tis_threeview_2stage_partial_*.json` | JSON | 每 5 样本一份 |

## Monitoring Configuration

- **Timeout**: 90 分钟
- **Monitor files**: `src/results_tis_threeview_2stage_partial_*.json`
- **Metric file**: 结果 JSON 末尾 `__summary__`
- **Metric key**: `map_metrics.missed_rate` / `cross_view_missing_rate` / `accuracy_pct`

## Analysis Plan

- **Primary metric**: A1 漏实例率（threeview 单次 39.1% → 目标显著下降）、C7 跨视图缺失率（39.1% → 下降）
- **Secondary metric**: 总体正确率（threeview 单次 30.0%，目标不倒退）
- **Comparison**: 与 `threeview` 单次版同 50 样本逐项对比；同时看每类别计数准确率（模型 count vs GT count）
- **Success threshold**: A1/C7 任一明显下降（≥5pp）且 QA ≥30.0%；两个都掉 → 失败

## 决策树（跑完后按此推进）

1. A1/C7 下降且 QA 提升或持平 → 两阶段有效。下一步：把“先数后摆”机制移植到 3-pass（`threeview_3pass_2stage`），并单独报告 count 准确率。
2. A1/C7 下降但 QA 不变/下降 → 漏画不是唯一瓶颈。切换到 E2 长距离/全局结构。
3. A1/C7 没降（计数阶段本身错）→ 证明 VLM 从视频数不清实例。切换 E4：外部检测器（GroundingDINO）给每类数量，再喂给两阶段 prompt。

## 后续实验草案（按优先级）

### E2 长距离 / 全局结构（平移盲区 + 长距离 bin）

- 问题：B3 长距离 bin 崩、door-window/stove-tv 系统性偏、整体平移盲区 18 例
- 方案 A（prompt）：先让模型估计房间边界/墙角作为全局锚，再相对锚点摆物体（“锚点版”）
- 方案 B（指标）：把整体平移/尺度 sanity 加入每样本指标（中位数偏移 ≥1 格、尺度中位数 ≤0.7/≥1.4 直接报警）
- 成功标准：长距离 bin（≥4）准确率提升，盲区报警样本的 QA 有改善

### E3 abs_distance 尺度标定

- 问题：abs 精确 0/10（3-pass 也只 1/10），MRA 33%
- 方案：用已知尺寸物体（如门高约 2m）标定 grid→米尺度，再做数值回答
- 成功标准：abs MRA 相对 threeview_2stage 提升，且不作为 oracle 泄漏单独标注

### E4 检测器计数（两阶段失效时的 fallback）

- 问题：两阶段计数如果不可靠
- 方案：GroundingDINO 对每类实例计数 → 结果注入两阶段 prompt 的第二轮
- 注意：引入非 VLM 组件，实验报告需明确“计数来源”这一变量

## 分析工具准备

- `tmp/deep_review.py` 与 `tmp/gen_detailed_analysis.py` 已支持把 `threeview_2stage` 自动纳入汇总（结果文件存在时）
- 结果出来后在 failure-case-analysis.md 第 4 节补两阶段对比数字

## 两阶段结果（2026-08-06）

两阶段 50/50 完成：QA 32.0%（+1 vs 单次），但 A1 41.9%、C7 41.6%（反而比单次高）；摆位遵守计数 96.2%，计数阶段 chair 精确命中 4/12、stool 1/8，高频类别系统性少数。

决策树状态：命中分支 3（计数阶段本身错）→ 下一步 E4 外部检测器计数；同时补“GT 全场景计数 vs 视频可见实例”口径分析，避免冤枉模型数了镜头外物体。

## 结论与下一步分析（2026-08-06）

**结论（写入文档作提醒）**

1. 漏画实例的根因是 **VLM 本身数不清物体数量**，不是摆位/视图机制：两阶段摆位对计数阶段的遵守率 96.2%，但计数阶段 chair 精确命中 4/12、stool 1/8，高频类别系统性少数。外部检测器（E4）方案暂缓，后面再讨论。
2. 口径提醒：GT 实例数是整场景 bbox 数量，视频不一定拍全；后续若做严格计数归因，需要对齐“视频可见实例”口径，避免把镜头外物体计入模型错误。
3. 新证据：两阶段地图质量明显变好（对偶距离 44.1%、紧邻对 54.2%，均为四版最高），但 QA 只从 30% 到 32%——**地图质量提升没有转化为回答提升**，地图→回答的转换环节是当前最可疑的瓶颈。

**下一步候选（按现有数据排序）**

1. [推荐] E2b 回答阶段注入：复用已保存的 3-pass 地图（总体 34% 最佳），回答时显式注入统一地图坐标 + 预计算空间事实（物体相对距离/方向），只重跑回答阶段（约 100 次 API），直接验证“地图够了但答案没跟上”的假设。成本低、单变量、不碰建图。
2. E2 长距离/全局结构：针对 door-window 5/5 全错、stove/tv 相对家具系统性偏、18 个整体平移盲区样本，做锚点（房间边界/墙角）摆位；属于建图阶段改进，收益要等 E2b 结果出来再判断。
3. E3 abs 尺度标定：用已知尺寸物体（如门高 2m）把 grid 距离标定成米，改善 abs MRA；两阶段/3-pass 的 MRA 已到 33%，标定后有望继续涨。
4. E4 外部检测器计数：VLM 数不清的结论已定，检测器方案留作后续候选，不在本轮实现。
