# Unity 空间重放闭环 — 具体实现方案（v1）

> 2026-08-04 · 基于现有资产与 Unity 学习成果的落地设计

## 1. 目标与成功标准

目标不变：提升 VLM 在 VSI-Bench 空间 QA 上的表现。

本方案把“Unity 表示空间 + 重放相机路径 + 反馈验证”落成可运行的 pipeline，验收标准：

1. 至少 1 个 VSI-Bench 场景跑通“场景 JSON → Unity 渲染 → 与原视频对比 → 修正 → 再渲染”全流程
2. 同一相机位姿下，渲染帧与原始视频帧的定性对齐可用（M0 标定通过）
3. 在 50 样本子集上产出 QA 结果，并对比三视图基线（shared 52.7% / direct 39.4% / noshared task-aware 40%）
4. 反馈迭代能可复现地改善场景表示误差或 QA 分数

## 2. 总览架构

## 1.5 研究边界（Oracle vs 方法）

GT bbox 元数据不是研究对象，而是工具：
- 标定用：确认坐标轴/尺度/位姿约定时，需要一份“确定正确的场景”
- 上界用：GT 表示 + 真值位姿 → QA，衡量“如果空间完全正确，分数能到多少”

真正要研究的是：从视频出发，系统自己生成“bbox 类布局 + 相机轨迹/内参”，并用 Unity 重放验证修正：
- 布局生成：VLM task-aware 3D layout（主方法），重建/检测器作对照
- 位姿恢复：DUSt3R/COLMAP 估计（工程组件），真值仅用于验证估计质量
- 闭环：渲染帧 vs 原帧的差异同时反馈布局和位姿误差（方法核心）

实验上必须把这三类分开报告：oracle 上界 / 无反馈方法 / 闭环反馈后方法。

```
VSI-Bench 样本 (video + question + GT bbox)
        │
        ▼
[1] 数据准备：抽帧 + 相机位姿/内参（真值或估计）
        │
        ▼
[2] 场景表示生成（三路）：
        A. Oracle：meta_info GT bbox → scene.json
        B. VLM：task-aware prompt → 3D layout JSON → scene.json
        C. 重建：DUSt3R/深度估计 → 简化几何 → scene.json
        │
        ▼
[3] Unity 渲染：scene.json + cameras.json → RGB / depth / object-mask 帧
        │
        ▼
[4] 反馈：渲染帧 vs 原视频帧（像素/掩码/物体级误差）
        │
        ▼
[5] 迭代：按误差修正 scene.json（v1 手工/启发式，v2 VLM 指错）
        │
        ▼
[6] QA：Unity 渲染帧/几何事实 + 问题 → VLM → 评测（复用 reevaluate.py）
```

## 3. 数据层

### 3.1 已有资产（已确认）

| 资产 | 位置 | 用途 |
|---|---|---|
| 50 样本评测集 | src/vsi_subset_50.json | QA 样本与真值 |
| 视频缓存 | ~/.cache/huggingface/vsibench/{dataset}/{scene}.mp4 | 原始观测 |
| GT 物体 bbox | Thinking in Space 复现/data/meta_info/*.json | Oracle 场景表示 |
| 位姿提取脚本 | Thinking in Space 复现/other_scripts/image_poses/*.py | 真值位姿获取参考 |
| Unity 渲染脚本 | C:/UnityProjects/My project/Assets/Script/{SceneBuilder,BatchRenderer,BatchExecutor}.cs | 渲染基础 |

meta_info 字段：`object_bbox`（centroid / axesLengths / min / max，单位米）、`room_center`、`room_size`。
**注意：meta_info 没有相机位姿**，位姿需要单独获取。

### 3.2 相机位姿：三选一

- A. 原数据集真值：按 image_poses 脚本从 ScanNet / ARKitScenes / ScanNet++ 原始数据提取。最准，但需要下载对应场景（重，建议只用于 1-3 个标定/试点场景）
- B. 视频估计（主推）：DUSt3R 或 COLMAP 从 VSI-Bench 视频估计位姿 + 内参，可扩展到全部 50 场景，且不依赖原数据集下载
- C. 模拟路径：先用手工位姿跑通渲染链路，仅用于调试，不作为正式实验

### 3.3 相机内参

- 有真值：ARKitScenes / ScanNet++ 原始数据里带内参；ScanNet 用 color_intrinsic
- 估计路线：DUSt3R / COLMAP 输出 fx/fy/cx/cy
- 转到 Unity：用 fx/fy/width/height 换算垂直 FOV，`fov = 2 * atan(h / (2 * fy))`

### 3.4 数据格式（新约定）

scene.json（扩展你现有的格式，单位米）：

```json
{
  "unit": "meters",
  "room": {"center": [0, 1.5, 0], "size": [5, 3, 5]},
  "objects": [
    {
      "name": "table", "category": "table",
      "position": [1.2, 0.0, 0.4],
      "rotation": [0, 45, 0],
      "scale": [1.8, 0.9, 1.2],
      "color": "#A0826D",
      "primitive": "box"
    }
  ]
}
```

cameras.json：

```json
{
  "width": 640, "height": 480,
  "intrinsics": {"fx": 577.0, "fy": 577.0, "cx": 320.0, "cy": 240.0},
  "frames": [
    {"frame": 0, "timestamp": 0.0, "position": [1, 1.5, 2], "rotation": [0, 0, 0], "fov_deg": 45.2}
  ]
}
```

坐标系约定：先用 M0 标定确认数据集轴向与 Unity（左手系 Y-up）的映射；设计上保留一个 `dataset_to_unity` 转换函数，避免在每个脚本里各写一套。

## 4. 场景表示生成

### A. Oracle（GT bbox）
- meta_info `object_bbox` 的 centroid → position，axesLengths → scale（直接作三轴尺寸），normalizedAxes → 3x3 朝向矩阵转 Unity 旋转
- 产出：确定性表示，作为“上界”和渲染标定用

### B. VLM layout（主研究路线）
- 沿用 task-aware 思路：把问题注入 prompt，让 VLM 从视频输出 3D layout JSON（类别、中心、尺寸、朝向）
- 关键改动：不再输出 10x10 网格坐标，直接输出米制 3D 坐标；可给“以第一帧为原点”的坐标系说明
- 风险：绝对尺度/深度估计难，所以反馈闭环的价值在这里

### C. 重建（可选）
- DUSt3R 输出稠密点云 → 简化成地面 + 墙面 + 物体包围盒（或直接导入 mesh）
- 作为 VLM 路线的对照/初始化

## 5. Unity 渲染层

复用 BatchExecutor，扩展成 `UnityReplay.Run()`：

1. 读 `scene.json` 建场景（已有）
2. 读 `cameras.json` 逐帧设位姿并渲染（已有基础）
3. 每帧输出三张：RGB、depth（16bit）、object-mask（每个物体一个纯色 ID）
4. 支持 `-executeMethod UnityReplay.Run -batchmode -quit` 批处理
5. 保留 MCP 用于交互调试（拖相机、临时改物体），批量实验走批处理

## 6. 反馈闭环

### 6.1 误差信号（按成本递增）

1. 像素级：渲染帧 vs 原视频帧（先 SSIM / 边缘，后续 LPIPS）
2. 物体级：在渲染帧上投影每个物体的 mask，在原帧上用检测器（GroundingDINO 等）定位同名物体，算 2D box IoU
3. 几何级：VLM 对比渲染帧与原帧，指出“哪些物体位置/大小/遮挡不对”（可解释）

### 6.2 修正策略

- v1：对误差大的物体做局部搜索（沿 x/y/z 平移、缩放扰动，选指标最优），每次迭代只改少数物体
- v2：把渲染帧+原帧+误差指标喂给 VLM，让它输出修正后的 scene.json
- 收敛条件：关键帧的物体级 IoU 连续两轮不再提升，或 QA 答案不再变化

## 7. QA 评测

三种输入形态（都复用现有 answer prompt 与 extract/reevaluate 逻辑）：

| 形态 | 输入 | 作用 |
|---|---|---|
| unity_only | 渲染帧 + 问题 | 验证 Unity 表示是否自足（noshared 等价） |
| unity_plus_video | 渲染帧 + 原视频 + 问题 | 验证渲染是否增强（shared 对比 52.7%） |
| unity_facts | 从 Unity 几何算出的距离/方位文本 + 问题 | 验证“精确表示 → 精确事实”能否救 abs_distance |

结果 JSON 沿用现有格式，新增字段：`representation`（oracle/vlm/recon）、`feedback_iters`、`scene_error`（物体级 IoU 等）。

## 8. 里程碑

| 里程碑 | 内容 | 验证 |
|---|---|---|
| M0 标定 | 1 个场景：GT bbox 建场景 + 拿到位姿（真值或估计） | 渲染帧与原视频帧侧边对比基本对齐 |
| M1 工具链 | scene.json/cameras.json 生成脚本 + UnityReplay 渲染 RGB/depth/mask | 批处理一键出 N 帧 |
| M2 Oracle 闭环 | 10 样本：GT 表示 + 位姿 → 渲染 → QA | 产出结果并对比三视图基线 |
| M3 VLM 表示 | VLM layout prompt + Unity 渲染 + 人工/启发式修正 | 1 个场景闭环跑通 |
| M4 自动反馈 | 指标 + 修正循环 | 物体级 IoU 或 QA 分数可复现提升 |
| M5 50 样本 | 完整评测 + 消融表 | 结果 JSON + 报告 |

## 9. 待确认决策（建议先和导师对齐）

1. 位姿：先下载 1-3 个原场景真值做标定，还是直接走 DUSt3R/COLMAP 估计
2. 表示：Oracle 只做上界，还是也作为论文对照组；VLM layout 是否允许手工修正后进 QA
3. 反馈信号：像素 / 物体 mask / VLM 指错，第一版用哪个
4. abs_distance 是否允许“从 Unity 几何直接算答案”作为实验条件（可能被视为 oracle 泄漏，需要写明）

## 10. 建议的下一步（M0）

1. 选 1 个样本（如 scene0550_00 / scannet），用 meta_info 生成 Oracle scene.json
2. 用 DUSt3R 或现有位姿脚本试拿相机位姿；若暂不可行，先用手工位姿
3. 用 UnityReplay 渲染并与原视频第一帧做并排对比，确认轴向/尺度/位姿约定
4. 跑通后再扩展成 M1 工具链
