# 200 条扩样完整分析（TIS 口径）

> 数据来源：`src/results_tis_200.json`（200 样本 × 3 arm = 600 条，全部成功）。判定口径与 TIS/VSI-Bench 一致：abs/size/room 用 MRA，counting 用精确整数，其余 A-D 精确匹配。

## 1. 覆盖情况

- 200 样本 × baseline / threeview / threeview_3pass = 600 条记录，无 MAP_API_FAIL。
- appearance_order 已补齐（75 条全部成功）。

## 2. QA 分题型（正确/总数）

| 题型 | baseline | threeview | 3-pass |
|---|---|---|---|
| abs_distance (MRA) | 14/25 | 11/25 | 12/25 |
| rel_distance | 8/25 | 12/25 | 10/25 |
| direction_easy | 3/7 | 4/7 | 5/7 |
| direction_medium | 3/11 | 3/11 | 6/11 |
| direction_hard | 3/7 | 2/7 | 1/7 |
| counting (精确) | 4/25 | 4/25 | 3/25 |
| size_estimation (MRA) | 22/25 | 19/25 | 22/25 |
| room_size (MRA) | 16/25 | 17/25 | 17/25 |
| route_planning | 12/25 | 11/25 | 11/25 |
| appearance_order | 6/25 | 9/25 | 7/25 |
| 总体 | 91/200 (46%) | 92/200 (46%) | 94/200 (47%) |

## 3. 地图指标

| arm | 漏画率 | 对偶距离正确 | 尺度中位 |
|---|---|---|---|
| baseline | 292/714 (41%) | 159/477 (33%) | 1.17 |
| threeview | 310/714 (43%) | 146/442 (33%) | 1.09 |
| 3-pass | 290/714 (41%) | 153/480 (32%) | 1.20 |

## 4. 错误案例规律（错误 vs 正确样本中出现率）

| 问题 | baseline 错误/正确 | threeview 错误/正确 | 3-pass 错误/正确 |
|---|---|---|---|
| 漏画实例 | 48% / 21% | 48% / 25% | 51% / 20% |
| 多画实例 | 26% / 32% | 20% / 30% | 28% / 32% |
| 相对距离画错 | 54% / 29% | 53% / 40% | 54% / 36% |
| 相对方向错 | 47% / 23% | 41% / 29% | 44% / 30% |
| z 整体偏高 | - | 49% / 35% | 38% / 28% |

规律：漏画、距离错、方向错在错误案例里明显更常见（错误 41~54% vs 正确 20~40%）；z 偏高三视图里错误案例也更高。

## 4.5 相对距离 / 方向错误细分

**相对距离定义**：两个类别之间取最近实例的欧氏距离（模型 vs GT），差值 >1 格算错。

- 偏远/偏近：baseline 偏远 67% / 偏近 33%；threeview 59% / 41%；3-pass 67% / 33%。整体是模型把物体对画得**比 GT 远**。
- 按 GT 距离桶的错误率：0-1 格（紧邻）69~86%；2-3 格 65~69%；4-5 格 54~55%；6-7 格 72~82%；8-10 格样本少。两头（紧邻和远距离）错得多，中间 4-5 格相对好。
- 方向错按 45° 步长：三个 arm 都以 ±1 步（相邻方向混淆）为主，完全相反（±4）只有 9~14 对；顺时针/逆时针基本对称，没有整体反转或整体偏一侧的系统性规律。

## 5. 初步结论

1. 漏画仍是核心问题：三个 arm 41~43%，且错误案例中 48~51% 伴随漏画，正确案例只有 20~25%。
2. counting 最差（12~16%）：模型数不清实例。
3. size/room 用 MRA 后表现中等（size 19~22/25，room 16~17/25）。
4. direction medium/hard 仍差；3-pass 的 medium 明显好于单次（6/11 vs 3/11）。
5. appearance 是弱项（6~9/25），但也说明有数据可改进。
6. 距离整体偏远、方向是相邻混淆：改进方向是尺度锚定 + 相对布局约束，而不是纠整体反转。

## 6. 逐样本 case-by-case

- 补偿版：[docs/cogmap-casebycase-200.md](/C:/Users/贝贝/Documents/Three-view Cognitive Map/docs/cogmap-casebycase-200.md)
- 纯对齐版：[docs/cogmap-casebycase-200-raw.md](/C:/Users/贝贝/Documents/Three-view Cognitive Map/docs/cogmap-casebycase-200-raw.md)
- 200 个样本全量，每样本含 TOP/FRONT/SIDE 的 GT | baseline | threeview | 3-pass 坐标对照与问题标签。

## 7. 下一步（见 plan.md）

- 场景重建准确率度量脚本（分视图相对位置误差、failure vs correct gap）
- Debate 1 轮 baseline + agent 间变换矩阵/相机矩阵对齐
- Failure-case 驱动的 prompt 迭代
