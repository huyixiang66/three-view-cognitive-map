# 更新日志 (Update Log)

> 记录项目的重大更新（AI 在 end session 时自动判断是否写入）。

<!-- version-style: date -->

## 2026-07-31

### Major: 方向切换 — Unity 空间表示 + 相机位姿重放闭环

- 目标不变：提升 VLM 在 VSI-Bench 空间 QA 上的表现
- 空间表示主路线从“三视图认知图”切换到 Unity
- 闭环思路：Unity 表示空间 → 模拟相机位姿重走原视频路径 → 渲染反馈验证 → 迭代 → 回答问题
- 三视图路线结论封存：task-aware 100% 召回、viz 有害、facts 脆弱、坐标精度是瓶颈
- 新增 docs/unity-closed-loop-direction.md，更新 PROJECT.md / session-handoff.md / TODO.md

---

## 2026.07.23 (2026-07-23)

### Minor: Pipeline v2 — 视频帧集成

- 视频帧采样 (opencv, 5帧, JPEG base64) + multimodal content builder
- 移除 {video_input} placeholder，统一标记为 [Video frames attached]
- max_tokens 500 → 4000（多模态推理）
- 增量 auto-save（每5样本）
- grid_visualizer wcwidth 重写 + Windows UTF-8 兼容

---

## 2026.07.2 (2026-07-21)

### Minor: 功能更新

- 添加 project-butler 项目记忆系统
- 初始化 CLAUDE.md / PROJECT.md / TODO.md / session-handoff.md / STRUCTURE.md / DOCS.md / UPDATE_LOG.md
- 创建 .claude/ 配置文件目录
- 迁移长对话上下文到新的项目记忆文件

---

## 2026.07.1 (2026-07-21)

### Minor: 初始发布

- 项目管理系统初始化

---
