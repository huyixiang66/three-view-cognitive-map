# Session Handoff — 2026-08-04

## 项目状态

目标不变：在 VSI-Bench 这类空间 QA 上提升 VLM 的表现。当前主线是 Unity 空间表示 + 相机位姿重放闭环（详见 docs/unity-pipeline-design.md）。

## 当前 Unity 房间状态（M0 试点）

- Unity 项目：`C:/UnityProjects/room1`（编辑器当前打开，MCP 在线；文档里的 `My project` 已过时）
- 场景：`Assets/Scenes/SampleScene.unity`（2026-08-04 已保存）
- 样本：VSI-Bench `arkitscenes / 41069025`
- 场景 JSON：`tmp/gt_room_41069025.json`（GT bbox，z-up → Unity y-up 映射）
- 家具：已换成 Asset Store 资产包 `UnityTechnologies/Basic Asset Pack Interior` 的现成 prefab：
  - 2 椅：`ChairDinningA` / `ChairDinningB`
  - 1 沙发：`SofaDouble`（含 2 个 SofaCusion 子件）
  - 4 桌：`TableSquareMedium` / `TableRectangleMedium` / `TableRectangleShort` / `TableNarrowSingleDraw`
- 灶台/电视：资产包里没有现成模型，先用简单方体占位（`stove`、`tv`，位置/尺寸按 GT bbox）
- 墙：无墙体
- 位置：家具中心按 GT bbox centroid 摆放，并按 bbox 尺寸缩放
- 材质：资产包原 shader 为 URP，与 Built-in 工程不兼容导致紫色；已将 27 个材质改为内置 Standard（已修复）
- 相机：当前是俯视调试位姿，尚未对齐原视频真实位姿

## 原视频

- 路径：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\41069025.mp4`
- 对应抽帧：`tmp/41069025_frame000.png`

## 本周实验（三视图 vs TIS，2026-08-04 新增）

- 设计文档：`docs/threeview-vs-tis-experiment.md`
- 实现：`src/tis_prompts.py`（TIS 原版 + 三视图单次 prompt）、`src/tis_compare.py`（类别抽取/GT 地图/地图指标）、`src/run_tis_compare.py`（跑批）
- 跑批命令：`python run_tis_compare.py --arm both --mode shared --output results_tis_compare.json`（每 5 样本自动保存 partial，支持 --resume / --dry-run）
- 3-pass 版已实现：`--arm threeview_3pass`，front/side 强制实例数与坐标一致，回答阶段注入取平均后的统一地图；由用户手动跑，每 5 样本自动保存
- failure case 报告已完成：`docs/failure-case-analysis.md`（聚合模式 + 典型案例，地图为主，QA 交叉参考）
- 2026-08-06：新增 `docs/map-compare-detailed.md`（3 arms × 50 样本逐视图 GT→模型坐标对照）；`docs/failure-case-analysis.md` 重写为详细版（量化诊断 + 分错误类型案例）
- 2026-08-06：新增 `threeview_2stage` arm（先数实例数、再按数量摆三视图），针对漏画实例 A1/C7；待用户手动跑，每 5 样本自动保存
- 2026-08-06：新增 `docs/experiment-plan-improve.md`（两阶段实验计划 + 决策树 + E2 长距离/E3 abs 尺度/E4 检测器计数草案）；分析脚本已自动支持 threeview_2stage
- 2026-08-07：新增 `docs/map-compare-aligned.md`（TOP 旋转对齐逐样本对照，yaw/镜像/RMSE）；确认 ReVSI 场景覆盖 33/44（hf-mirror 核对）
- 2026-08-07：完成对齐后建图分析（cogmap-dictionary / analysis / direction-bias / aligned-absolute-metrics）；桶1 人工核对 7/7
- 2026-08-07：计划文档 `docs/plan-2026-08-07.md`：扩样 200 条全用 VSI-Bench（8 类×25 分层随机），ReVSI 暂缓；分析口径=整体+分题型，重点系统性偏置
- 2026-08-07：执行推进——vsi_subset_200.json 已生成（含 ext 扩展字段）、cogmap_direct_metrics.py / cogmap_issues.py 已实现；问题级输出 docs/cogmap-issues.md
- 样本运行由用户手动执行

## 待决策

1. 灶台/电视：如需真实模型，用户在 Asset Store 再找对应资源导入后替换占位方体
2. M0 标定下一步：获取 41069025 相机位姿（真值或估计），做渲染帧 vs 原视频帧对齐

## 下一步

1. （可选）补充灶台/电视资产后替换占位方体
2. 获取相机位姿，渲染并与原视频对比，确认轴向/尺度/FOV
3. 跑通后进入 M1 工具链（scene.json/cameras.json + UnityReplay 批量渲染 RGB/depth/mask）

## 可复用资产

| 资产 | 说明 |
|---|---|
| tmp/gt_room_41069025.json | 41069025 的 Unity 场景 JSON（无墙） |
| C:/UnityProjects/room1 | 当前 Unity 工程（场景内已用现成家具 prefab） |
| Assets/UnityTechnologies/Basic Asset Pack Interior | 用户导入的家具资产包 |
| src/reevaluate.py、src/run_vsibench.py | VSI-Bench 评测 harness |
| src/vsi_subset_50.json | 50 样本评测集 |
