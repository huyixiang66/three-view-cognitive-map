# 三视图 vs GT

> 覆盖 `threeview`（单次三视图）和 `threeview_3pass`（3-pass），对比 TOP/FRONT/SIDE 三张图；FRONT/SIDE 横向坐标经跨视图实例匹配后复用 TOP 变换。

## 1. QA

| arm | 总体 | abs_distance (MRA) | rel_distance | rel_direction |
|---|---|---|---|---|
| threeview | 30.0% (15/50) | 19% | 2/10 | 13/30 |
| threeview_3pass | 34.0% (17/50) | 33% | 4/10 | 12/30 |

## 2. 地图问题概览

- 漏画：跨视图漏画与漏画同源。
- z 整体偏高：threeview +1.19 格（71% 偏高）、3-pass +0.43 格（52% 偏高）。
- 小物体摆放错误更明显。
- 单物体摆放错误集中在 tv、lamp、table、stool、microwave。

## 3. 典型案例

### 样本 2 `47334103`（arkitscenes · object_abs_distance）

- QA：模型 0.3 vs GT 3.7（错）。
- TOP：stool 多画 1 个，table 偏移 2.0 格。
- FRONT/SIDE：stool、table 横向偏差 2.2~3.0 格，z 也整体偏高。
- 诊断：多画 stool ×1；stool-table 距离画错；z 整体偏高。

### 样本 11 `scene0221_01`（scannet · object_rel_distance）

- QA：模型 A vs GT B（错）。
- 画出来的 chair/lamp/bed 位置基本对（单次大多 ✓），但 bed 漏 1、chair 漏 2、lamp 漏 1、pillow 漏 4、microwave 漏画。
- 诊断：主要问题是漏画，不是位置；microwave 三个视图都漏。

### 样本 12 `scene0307_02`（scannet · object_rel_distance）

- QA：模型 A vs GT C（错）。
- door 漏 4、window 漏 2；radiator 单物体摆放错误（threeview 偏移 4.0 格，3-pass 相对好一些）。
- 诊断：贴墙结构漏画 + radiator 单物体摆放错误。

### 样本 14 `scene0653_00`（scannet · object_rel_distance）

- QA：模型 D/B vs GT C（错）。
- monitor 漏 6、table 漏 5、keyboard 漏 1；threeview FRONT 里 keyboard/monitor 分别偏移 2.3/2.6 格。
- 诊断：办公室多实例/小物体漏画 + FRONT 高度偏高。

## 4. 单次 vs 3-pass 小结

- 3-pass QA 略好（17 vs 15），abs MRA 明显更好（33% vs 19%）。
- z 偏高 3-pass 更小（+0.43 vs +1.19），说明 3-pass 对高度约束有效。
- 漏画问题两者都严重，3-pass 没有解决计数问题。
- 补偿后两版地图差距不大，3-pass 没有带来明显的整体地图增益。
