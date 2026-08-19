# Session 2026-07-31 — Unity 方向切换交接

## 本次目标 (Session Goal)
- 交接三视图路线的工作成果
- 记录新方向：Unity 空间表示 + 相机位姿重放闭环

## 关键操作 (Key Actions)
- 读取项目记忆文件（PROJECT.md / session-handoff.md / TODO.md / UPDATE_LOG.md / DOCS.md / STRUCTURE.md / CLAUDE.md / project-profile.json）
- 复盘三视图路线结果（50 样本、task-aware、viz/facts 消融）
- 更新交接文档与项目状态，记录 Unity 闭环方向

## 决策与理由 (Decisions & Rationale)

| 决策 | 理由 |
|---|---|
| 三视图认知图封存 | 坐标精度是瓶颈，viz/facts 被证明无效，纯 prompting 路线到顶 |
| 切换到 Unity 空间表示 | 提供精确几何/位姿环境，支持“重走相机路径”做反馈验证 |
| 保留 VSI-Bench 评测资产 | 评测 harness、50 样本子集、结果格式可直接复用 |

## 产出文件 (Output Files)
- session-handoff.md / PROJECT.md / TODO.md / UPDATE_LOG.md 更新
- docs/unity-closed-loop-direction.md 新增
- log/session-2026-07-31-unity-pivot.md 本文件

## 未完事项 (Unfinished Items)
- 确认 VSI-Bench 数据是否含相机位姿/深度/3D 元数据
- 搭建 Unity 最小闭环 MVP
- 与导师确认场景生成与反馈信号的设计
