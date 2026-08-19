# Baseline（TIS）vs GT

> 原版 Thinking-in-Space 俯视认知图 vs GT；只比较 TOP 视图，无 FRONT/SIDE/z。

## 1. QA

| 指标 | baseline |
|---|---|
| 总体 | 24.0% (12/50) |
| abs_distance (MRA) | 22% |
| rel_distance | 2/10 |
| rel_direction | 10/30 |

## 2. 地图问题概览

- 漏画率 38.0%，多画率 2.7%；漏画集中在 chair、table、microwave、monitor。
- 对偶距离准确率 38.4%，紧邻对准确率 28.0%。
- 尺度中位 1.12（补偿版估计 0.84）：地图整体偏散或偏挤，没有尺度锚。
- 小物体摆放错误：TOP ≤2 可接受率 small 81% vs large 89%。
- 单物体摆放错误集中在 table、stool、microwave、bed、tv。

## 3. 典型案例

### 样本 2 `47334103`（arkitscenes · object_abs_distance）

- QA：模型 0.3 vs GT 3.7（错，且差很远）。
- TOP 视图：GT stool (2.0,2.0)、table (7.0,1.0)；模型 stool 画了 2 个（多画 1 个），table 偏移 2.0 格。
- 诊断：多画 stool ×1；stool-table 距离画错（GT 5.1，模型 1.0）；stool→table 方向错。

### 样本 11 `scene0221_01`（scannet · object_rel_distance）

- QA：模型 A vs GT B（错）。
- TOP 视图：bed 漏 1、chair 漏 2、lamp 漏 1、pillow 漏 4、microwave 直接漏画；画出的 chair/microwave 偏移 2.8/4.0 格。
- 诊断：漏画为主，且漏掉的 chair/pillow 都是高频多实例类别。

### 样本 12 `scene0307_02`（scannet · object_rel_distance）

- QA：模型 A vs GT C（错）。
- TOP 视图：door 漏 4（GT 5）、window 漏 2（GT 3）；radiator 偏移 4.7 格。
- 诊断：door-window 等贴墙结构漏画严重；radiator 单物体摆放错误。

### 样本 14 `scene0653_00`（scannet · object_rel_distance）

- QA：模型 B vs GT C（错）。
- TOP 视图：monitor 漏 6（GT 7）、table 漏 5（GT 6）、keyboard 漏 1、window 漏 1。
- 诊断：办公室场景里多实例/小物体几乎只画了一个代表，计数问题非常突出。

## 4. 规律总结

- baseline 的核心问题是漏画，尤其高频多实例和小物体。
- 少量画出来的物体也常整体偏移，属于单物体摆放错误。
- 只有 TOP 视图，无法提供高度信息。
