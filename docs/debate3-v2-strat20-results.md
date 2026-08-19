# 三 Agent Debate v2（结构化修正 + 轴偏移）— 分层 20 条

> 数据：`src/results_debate3_v2_strat20.json`（20 条，19 有效，1 条 ANSWER_API_FAIL）。对比同 19 条 single threeview（`results_tis_200.json`）。题型：rel_distance / direction / route / counting。

## 1. QA

| 方法 | 有效样本 | QA 正确 |
|---|---|---|
| debate v1（自由文本） | 19 | 7/19 (37%) |
| debate v2（结构化+轴偏移） | 19 | 11/19 (58%) |
| single threeview | 19 | 8/19 (42%) |

v2 比 single 高 3 条（+16pp），比 v1 高 4 条（+21pp）。

## 2. 地图指标

| 方法 | 漏画率 | 对偶距离正确 | 跨视图 top_front_x / top_side_y / front_side_z 中位 |
|---|---|---|---|
| debate v2 | 17/66 (26%) | 20/61 (33%) | 0.33 / 0.58 / 0.0 |
| single threeview | 18/66 (27%) | 20/62 (32%) | 0.0 / 0.0 / 0.0 |

- 漏画和对偶距离和 single 基本持平。
- 跨视图轴残差 v2 略高（0.33/0.58），说明结构化互评提升了 QA，但还没有把三视图坐标完全对齐；这部分留给后续变换矩阵/融合器。

## 3. 结论

- 结构化互评 + 轴偏移提示有效：QA 明显提升，地图指标不倒退。
- 当前 1 轮 + fallback 已经可以全量跑；跨视图残差仍有改进空间（融合器/第二轮）。
