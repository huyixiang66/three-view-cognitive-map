# 场景重建准确率：strat20 debate 对比

> 单位：10x10 网格；误差 = 对齐后模型实例与 GT 实例的欧氏距离（greedy 匹配，先按 TOP 对齐），逐样本取平均。数据来自 2026-08-13 的 strat20 实验。

| arm | 视图 | 平均误差 | 中位误差 | 样本数 | failure 平均 | correct 平均 | 差距(failure-correct) |
|---|---|---|---|---|---|---|---|
| threeview_3pass shared | top | 1.62 | 1.73 | 17 | 1.84 | 1.20 | +0.64 |
| threeview_3pass shared | front | 1.52 | 1.65 | 17 | 1.53 | 1.50 | +0.03 |
| threeview_3pass shared | side | 1.59 | 1.56 | 17 | 1.70 | 1.38 | +0.33 |
| threeview_3pass noshared | top | 1.62 | 1.73 | 17 | 1.75 | 1.36 | +0.39 |
| threeview_3pass noshared | front | 1.52 | 1.65 | 17 | 1.57 | 1.44 | +0.13 |
| threeview_3pass noshared | side | 1.59 | 1.56 | 17 | 1.68 | 1.43 | +0.24 |
| debate4 agentA_memory | top | 1.49 | 1.79 | 16 | 1.51 | 1.46 | +0.05 |
| debate4 agentA_memory | front | 3.79 | 3.98 | 16 | 3.57 | 4.00 | -0.44 |
| debate4 agentA_memory | side | 3.68 | 3.85 | 16 | 3.27 | 4.09 | -0.82 |
| debate5（3 view agent） | top | 1.52 | 1.89 | 17 | 1.69 | 0.73 | +0.96 |
| debate5（3 view agent） | front | 2.75 | 3.00 | 17 | 2.72 | 2.91 | -0.20 |
| debate5（3 view agent） | side | 2.81 | 3.07 | 17 | 2.78 | 2.95 | -0.17 |

## 发现

1. TOP 误差：v4 memory（1.49）略好于 v5（1.52）和 3-pass（1.62），三者差距不大。
2. FRONT/SIDE 误差：3-pass 最好（约 1.5），v5 居中（约 2.8），v4 memory 最差（约 3.8）。两个 debate 融合地图都在高度/深度轴上明显变差，说明当前融合或对齐没有解决 z 轴校准，反而放大了它。
3. failure vs correct 差距：3-pass 的 TOP 差距 +0.64；v5 的 TOP 差距最大（+0.96），说明 v5 错题的 TOP 位置误差明显更高，位置误差和 QA 错误相关；v4 memory 各视图差距接近 0 甚至为负，它的 QA 好坏主要由回答阶段记忆/融合地图决定，而不是几何误差。
4. shared vs noshared 使用同一张地图，重建误差完全一致，QA 8/20 vs 7/20，说明“回答时带建图记忆”在当前 20 条上只带来约 1 题收益。

## 建议

- 在继续评判 debate 前，先修 v4/v5 的 z 轴（高度）和深度校准：两个融合版 FRONT/SIDE 误差都偏高，属于已知“z 整体偏高/偏低”问题的放大。
- v5 的 TOP failure gap 最大，适合挑 3-5 个“TOP 误差高且答错”的样本做 prompt 迭代。
- Unity 侧可以复用记录的相机参数和变换矩阵，验证 v4/v5 融合地图在自由视角下是否对齐。
