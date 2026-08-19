# Debate v4 设计：每个 Agent 是一套相机帧

> 目标：把 debate 真正做到学长说的样子——每个 agent 有自己的 position / look_at / look_up（等价相机），各自建图，agent 间通过变换矩阵对齐后多轮互评收敛。

## 1. 核心思想

- 每个 agent 是**一套完整相机帧**，不是“只画 TOP/FRONT/SIDE 其中一个视图”。
- 不同 agent 的 look_at / look_up 不一定严格 90° 对齐（可能 80°/70°），所以同一物体在不同 agent 地图里的坐标不同。
- 两个 agent 的坐标系之间应有**刚性变换** `y = R·x + t`（可选镜像/尺度），即学长说的“变换矩阵”。
- 用共享物体（实例级匹配）估计这个变换，再把 agent 地图对齐到同一参考帧，才能公平互评与融合。

## 2. 流程

1. **独立建图**：N 个 agent 各自用视频 + 自己的相机位姿 prompt 建完整三视图（TOP/FRONT/SIDE），输出带 size 的坐标；同时用自己的三视图重建每个实例的 3D 点 `(x,y,z)`。
2. **实例级跨 agent 匹配**：按类别做最近邻/Hungarian 匹配，得到 agent A 与 B 的对应实例点集。
3. **变换矩阵估计**：用 `camera_utils.estimate_rigid_transform`（Umeyama/Kabsch）估计 `R,t`（可选 mirror），把 B 对齐到 A（或都对齐到 GT）。
4. **带视频的结构化互评**：agent 看到对齐后的对方地图 + 视频，输出结构化修正视图（可合并），不删实例。
5. **多轮收敛**：把本轮修正后的地图再对齐、再互评，直到跨视图/跨 agent 残差低于阈值或达到最大轮数。
6. **融合**：在统一参考帧下按实例做 union/加权平均融合，输出最终 cogmap。
7. **评估**：用 scene reconstruction metric（逐物体位置误差）+ QA（回答阶段统一带视频）双重评估。

## 3. 与当前代码的关系

- `src/camera_utils.py` 已有：look_at/look_up → view matrix、view matrix → position/rotation、`estimate_rigid_transform`（3D Umeyama）。**已可复用。**
- `src/run_debate_v2.py` 已有：带视频的结构化互评、不删实例、axis_diffs 贪心配对。**可迁移。**
- 缺：agent 独立相机位姿 prompt；三视图 → 3D 点重建；跨 agent 实例匹配；多轮收敛与融合器。

## 4. 待实现清单

- [ ] agent 建图 prompt：每 agent 给定 `position / look_at / look_up`（预设不同视角或随机），输出自己的三视图 JSON
- [ ] 三视图 → 3D 点重建（top.x/front.x 一致性约束 + 实例匹配）
- [ ] 跨 agent 实例匹配（类别内 greedy/Hungarian）
- [ ] 变换矩阵估计与对齐（复用 `estimate_rigid_transform` / `rigid_align`）
- [ ] 多轮结构化互评（带视频）与收敛判定
- [ ] 融合器（union + 加权平均）与 scene reconstruction 评估

## 5. 评价口径

- 地图质量：scene reconstruction metric（TOP/FRONT/SIDE 逐物体位置误差，failure vs correct gap）
- QA：回答阶段统一带视频，和 single 3-pass 公平对比
- 不跑全量 200；先在 strat20 上验证再扩
