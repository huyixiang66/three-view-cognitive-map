# 三 Agent Debate Baseline — 分层 20 条结果

> 数据：`src/results_debate3_strat20.json`（20 条，19 有效，1 条 `CRITIQUE_API_FAIL`）。对比同 20 条样本的 single threeview（`results_tis_200.json`）。题型：rel_distance 4、route 4、direction 8、counting 3。

## 1. QA

| 方法 | 有效样本 | QA 正确 |
|---|---|---|
| debate3 | 19 | 7/19 (37%) |
| single threeview | 19 | 8/19 (42%) |

debate 没有提升 QA，还略低 1 条。

## 2. 地图指标

| 方法 | 漏画率 | 对偶距离正确 | 跨视图 top_side_y 中位 |
|---|---|---|---|
| debate3 | 21/71 (30%) | 13/64 (20%) | 1.0 |
| single threeview | 23/71 (32%) | 16/62 (26%) | 0.0 |

- 漏画率轻微下降（30% vs 32%）
- 对偶距离正确率更差（20% vs 26%）
- 跨视图 top-side y 一致性更差（中位残差 1.0 vs 0.0）

## 3. 结论

当前“各建一视图 → 自由文本互评 → 各自出最终视图”的 1 轮 baseline 无效：QA 没提升，相对布局和对齐一致性反而变差。说明需要改设计，候选方向：

1. 互评输出必须是**可直接合并的结构化修正**（如每个类别修正后的坐标/尺寸），而不是自由文本建议
2. 在 debate 前后显式做 agent 间变换矩阵估计（`camera_utils.estimate_rigid_transform`），先把坐标系对齐再比较
3. 增加 round 或引入 GT 校准轮
4. 只让 debate 负责“挑错”，最终图由单独融合器合成
