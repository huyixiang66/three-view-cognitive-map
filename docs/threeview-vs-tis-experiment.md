# 三视图 vs TIS 认知图 — 对照实验设计

> 2026-08-04 · 由 grill-me 收敛出的实验方案

## 1. 目标

证明三视图认知图（top/front/side）相对 TIS 原版单俯视认知图的增量价值，并定位三视图建图的失败类型。

## 2. 对照设计

- Baseline arm：TIS 原版 10×10 俯视认知图（论文 B.4 prompt 原样），单次生成。
- Three-view arm：同款措辞，单次输出 top/front/side 三张视图。
- 单变量：地图维度（1 个俯视图 vs 3 个正交视图）。
- 控制变量：
  - 同一模型、同一视频、同一 50 样本子集
  - 同一类别集合（仅问题提到的类别），GT 地图用同一集合裁剪
  - 同一回答 prompt、同一 greedy 解码
- 输出 schema：只输出中心坐标，不含 size；size 作为独立扩展实验。
- 3-pass 三视图作为“生产变体”单独报告，pass 数差异不做主归因。

## 3. Prompt 草案

### TIS 原版（照抄论文 B.4）

```text
[Task] This video captures an indoor scene. Your objective is to identify specific objects within the video, understand the spatial arrangement of the scene, and estimate the center point of each object, assuming the entire scene is represented by a 10x10 grid.
[Rule]
1. We provide the categories to care about in this scene: {categories_of_interest}. Focus ONLY on these categories.
2. Estimate the center location of each instance within the provided categories, assuming the entire scene is represented by a 10x10 grid.
3. If a category contains multiple instances, include all of them.
4. Each object's estimated location should accurately reflect its real position in the scene, preserving the relative spatial relationships among all objects.
[Output] Present the estimated center locations for each object as a list within a dictionary. STRICTLY follow this JSON format: {"category name": [(x_1, y_1), ...], ...}
```

### Three-view 单次版（同措辞扩展）

```text
[Task] This video captures an indoor scene. Your objective is to identify specific objects within the video, understand the spatial arrangement of the scene, and estimate the center point of each object in three orthogonal views, assuming each view is represented by a 10x10 grid.
[Rule]
1. We provide the categories to care about in this scene: {categories_of_interest}. Focus ONLY on these categories.
2. Estimate the center location of each instance in each view:
   - top view: (x, y) horizontal plane
   - front view: (x, z) horizontal x and height z
   - side view: (y, z) depth y and height z
3. If a category contains multiple instances, include all of them.
4. Each object's estimated location should accurately reflect its real position in the scene, preserving the relative spatial relationships among all objects.
5. Keep the same object consistent across views: top.x must match front.x, top.y must match side.y, front.z must match side.z.
[Output] Present the estimated center locations as a dictionary with three view keys. STRICTLY follow this JSON format:
{"top": {"category name": [(x_1, y_1), ...], ...}, "front": {"category name": [(x_1, z_1), ...], ...}, "side": {"category name": [(y_1, z_1), ...], ...}}
```

## 4. 数据与模型

- 样本：`src/vsi_subset_50.json`（50 样本）
- 模型：gemini-3.5-flash（与现有结果一致）
- 视频：`~/.cache/huggingface/vsibench/{dataset}/{scene}.mp4`
- GT：`Thinking in Space复现/.../data/meta_info/*.json`，按问题类别集合裁剪后归一化到 10×10 网格

## 5. 地图级指标

| 类别 | 指标 | 判定 |
|---|---|---|
| A1 | 漏实例率 | 输出实例数 < GT 实例数 |
| A2 | 多/误实例率 | 输出实例数 > GT，或写出类别集合外物体 |
| B3 | 对偶距离准确率 | 类别间欧氏距离与 GT 差 ≤1 格，按 8 个距离 bin 分局部/全局 |
| B4 | 全局尺度漂移 | 对偶距离系统性偏小/偏大（距离比值分布） |
| B5 | 紧邻对准确率 | 最短距离 bin 的对偶距离正确率 |
| C6 | 跨视图坐标冲突率 | top.x≠front.x、top.y≠side.y、front.z≠side.z（±1 格容差） |
| C7 | 跨视图实例缺失率 | 物体只出现在 1–2 个视图 |
| C8 | 高度排序准确率 | front/side 的 z 排序与 GT 高度排序一致 |

注：左右/镜像混淆不单列，因坐标系未对齐时无法判定；并入 C6 检测。

## 6. QA 协议

- 主协议 shared：建图 + 回答同一上下文（视频仍在上下文）
- 附加协议 noshared：只给地图文本 + 问题
- 指标复用 `src/reevaluate.py`：MCA 用 accuracy，NA 用 MRA

## 7. Failure case 分析

按地图误差类型统计 A1/A2/B3/B4/B5/C6/C7/C8，再做回答关联交叉分析：

- 地图对、答错 → 回答阶段问题
- 地图错、答错 → 建图阶段问题（回查上表）
- 地图错、答对 → 该误差类型对答案不敏感

## 8. 输出

- 地图指标对比表：baseline vs three-view（vs GT 上界）
- QA 分数对比表：shared / noshared × baseline / three-view
- failure case 分布表 + 典型案例列表
