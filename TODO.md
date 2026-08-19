# TODO

## M0 — 标定（下一步）
- [x] 选 1 个样本（arkitscenes / 41069025），用 meta_info 生成 Oracle scene.json 并搭出 Unity 房间（room1）
- [x] 墙已去掉（room1/SampleScene 当前无墙体）
- [x] 复核物体位置：与 meta_info centroid 一致（z-up → y-up 映射）
- [x] 家具已换为 Asset Store Basic Asset Pack Interior 现成 prefab（2 椅 / 1 沙发 / 4 桌）
- [ ] 灶台/电视：资产包无现成模型，当前为占位方体，待补充真实资产
- [ ] 获取相机位姿：DUSt3R/COLMAP 估计 or 原数据集真值（试点）
- [ ] Unity 渲染与原视频第一帧并排对比，确认坐标轴/尺度/FOV 约定

## M1 — 工具链
- [ ] 编写 scripts/unity_render.py：生成 scene.json + cameras.json，调用 Unity 批处理
- [ ] 扩展 UnityReplay：每帧输出 RGB + depth + object-mask
- [ ] 批处理一键渲染 N 帧并通过验证

## M2 — Oracle 闭环
- [ ] 10 样本：GT 表示 + 位姿 → 渲染 → QA
- [ ] 复用 reevaluate.py 对比三视图基线

## M3 — VLM 表示
- [ ] 设计 3D layout prompt（米制坐标，task-aware）
- [ ] VLM layout → Unity → 渲染 → 人工/启发式修正，跑通 1 个场景

## M4 — 自动反馈
- [ ] 误差指标：SSIM / 物体级 IoU / VLM 指错
- [ ] 修正循环：局部搜索 or VLM 重写 scene.json
- [ ] 验证物体级 IoU 或 QA 分数可复现提升

## M5 — 50 样本评测
- [ ] 完整评测 + 消融表（oracle / vlm / unity_only / unity_plus_video / unity_facts）
- [ ] 更新报告与论文素材

## 待对齐（导师）
- [ ] 位姿路线：真值试点 vs DUSt3R/COLMAP 估计
- [ ] Oracle 是否作为对照组；abs_distance 从 Unity 几何直接算是否算泄漏
- [ ] 反馈信号第一版用像素还是物体级 mask

## Done（已封存/已完成）
- [x] Unity MCP 插件安装：uv + com.coplaydev.unity-mcp + Codex config（见 docs/unity-mcp-setup.md）
- [x] Unity 熟悉：SceneBuilder / BatchRenderer / BatchExecutor 可跑通
- [x] 3-Pass CogMap pipeline
- [x] task-aware 建图：100% 物体召回
- [x] viz 被证明有害（shared -3pp / noshared -10pp）
- [x] facts 注入实现并测试
- [x] 50 样本基线跑完

## 扩样 200（2026-08-07 计划）
- [ ] 获取完整 VSI-Bench QA（hf-mirror），解析 8 类题型
- [ ] 写 src/sample_vsi_200.py：8 类×25、按数据集分层随机、固定 seed，导出 vsi_subset_200.json
- [ ] 复跑 4 个 arm（200 条），每 5 样本自动保存
- [ ] 对齐后指标自动覆盖新样本：MAE / cell 命中 / 方向与 z 偏置 / 分题型汇总
- [ ] 输出 200 条分析文档（整体 + 分题型）
