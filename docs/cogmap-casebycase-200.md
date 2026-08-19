# 50 样本逐样本并排对照（GT | TIS | 三视图，尺度+z 补偿）

> 在纯对齐基础上额外拟合统一尺度与全局 z 偏移（FRONT/SIDE 共用同一个值），用于暴露纯对齐下被尺度/z 盖住的相对布局问题；尺度与 z 偏移同时单独记录。偏差阈值 ≤2 格。

## 汇总

| arm | 正确 / 总数 | TOP ≤2 | FRONT ≤2 | SIDE ≤2 |
|---|---|---|---|---|
| baseline | 78 / 200 | 296/370 | - | - |
| threeview | 91 / 200 | 297/352 | 306/352 | 310/352 |
| threeview_3pass | 83 / 200 | 292/371 | 294/370 | 299/370 |

### 尺度 / z 偏移诊断（补偿版记录，仍算建图问题）

| arm | 尺度中位 | z偏移中位（FRONT/SIDE 共用） |
|---|---|---|
| baseline | 0.79 | +0.00 |
| threeview | 0.90 | -1.00 |
| threeview_3pass | 0.73 | +0.00 |

## 逐样本对照

### 样本 1 `42445984`（arkitscenes · object_counting）

Q：How many chair(s) are in this room?

- QA：GT 12 | baseline 4（错） | threeview 2（错） | threeview_3pass 2（错）
- 对齐：baseline: yaw=-53° mirror=否 平移=(-5.0,5.7) RMSE=1.24；threeview: 2点 yaw=-90° mirror=否 平移=(-1.5,9.8) RMSE=0.46；threeview_3pass: 2点 yaw=-90° mirror=否 平移=(-3.0,10.5) RMSE=0.35
- 补偿：baseline: 尺度=0.41 z偏移=+0.00；threeview: 尺度=0.43 z偏移=-1.00；threeview_3pass: 尺度=0.67 z偏移=+1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (3.0,2.0), (3.0,3.0), (2.0,4.0), (2.0,5.0), (2.0,6.0), (4.0,2.0), (5.0,2.0), (4.0,4.0), (4.0,5.0), (1.0,2.0), (1.0,1.0), (4.0,7.0) | (2.4,5.7)✓, (3.4,4.4)✓, (3.6,6.1)✓, (2.4,5.7)✓, (4.6,4.8)多, 漏8 | (4.0,4.0)✓, (4.0,5.0)✓, 漏10 | (4.0,5.0)✓, (4.0,7.0)✓, 漏10 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (3.0,3.0), (3.0,3.0), (2.0,3.0), (2.0,3.0), (2.0,3.0), (4.0,3.0), (5.0,3.0), (4.0,3.0), (4.0,3.0), (1.0,3.0), (1.0,3.0), (4.0,3.0) | - | (4.0,3.0)✓, (4.0,3.0)✓, (4.0,3.0)多, 漏10 | (4.0,3.0)✓, (4.0,3.0)✓, (4.0,3.0)多, 漏10 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (2.0,3.0), (3.0,3.0), (4.0,3.0), (5.0,3.0), (6.0,3.0), (2.0,3.0), (2.0,3.0), (4.0,3.0), (5.0,3.0), (2.0,3.0), (1.0,3.0), (7.0,3.0) | - | (4.0,3.0)✓, (5.0,3.0)✓, 漏10 | (5.0,3.0)✓, (7.0,3.0)✓, 漏10 |

- **baseline 问题**：漏画 chair ×8（GT 12，模型 4）
- **threeview 问题**：漏画 chair ×10（GT 12，模型 2）；z 整体偏高（平均 +1.0 格）
- **threeview_3pass 问题**：漏画 chair ×10（GT 12，模型 2）；z 整体偏低（平均 -1.0 格）

### 样本 2 `d755b3d9d8`（scannetpp · object_counting）

Q：How many computer mouse(s) are in this room?

- QA：GT 3 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (5.0,2.0), (4.0,7.0), (6.0,7.0) | (6.0,7.0)✓, 漏2 | (6.1,4.8)✗2.2, 漏2 | (6.0,7.0)✓, 漏2 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (5.0,2.0), (4.0,2.0), (6.0,2.0) | - | (6.1,4.2)✗2.2, 漏2 | (6.0,3.0)✓, 漏2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (2.0,2.0), (7.0,2.0), (7.0,2.0) | - | (4.8,4.2)✗3.1, 漏2 | (7.0,3.0)✓, 漏2 |

- **baseline 问题**：漏画 computer mouse ×2（GT 3，模型 1）
- **threeview 问题**：漏画 computer mouse ×2（GT 3，模型 1）
- **threeview_3pass 问题**：漏画 computer mouse ×2（GT 3，模型 1）

### 样本 3 `scene0574_01`（scannet · object_counting）

Q：How many towel(s) are in this room?

- QA：GT 4 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| towel | (4.0,2.0), (7.0,1.0), (7.0,2.0), (7.0,2.0) | (5.0,5.0)✗3.2, 漏3 | (4.8,4.5)✗2.6, 漏3 | (3.0,5.0)✗3.2, 漏3 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| towel | (4.0,4.0), (7.0,5.0), (7.0,5.0), (7.0,5.0) | - | (4.8,5.2)✓, 漏3 | (3.0,5.0)✓, 漏3 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| towel | (2.0,4.0), (1.0,5.0), (2.0,5.0), (2.0,5.0) | - | (4.5,5.2)✗2.5, 漏3 | (5.0,5.0)✗3.0, 漏3 |

- **baseline 问题**：漏画 towel ×3（GT 4，模型 1）
- **threeview 问题**：漏画 towel ×3（GT 4，模型 1）
- **threeview_3pass 问题**：漏画 towel ×3（GT 4，模型 1）

### 样本 4 `45260905`（arkitscenes · object_counting）

Q：How many table(s) are in this room?

- QA：GT 2 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (4.0,5.0), (2.0,1.0) | (5.0,7.0)✗2.2, 漏1 | (5.0,5.2)✓, 漏1 | (5.0,6.0)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (4.0,1.0), (2.0,3.0) | - | (5.0,3.6)✗2.8, 漏1 | (5.0,2.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (5.0,1.0), (1.0,3.0) | - | (5.2,3.6)✗2.6, 漏1 | (6.0,2.0)✓, 漏1 |

- **baseline 问题**：漏画 table ×1（GT 2，模型 1）
- **threeview 问题**：漏画 table ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 table ×1（GT 2，模型 1）

### 样本 5 `5f99900f09`（scannetpp · object_counting）

Q：How many chair(s) are in this room?

- QA：GT 14 | baseline 2（错） | threeview 2（错） | threeview_3pass 3（错）
- 对齐：baseline: 2点 yaw=-8° mirror=否 平移=(0.1,0.2) RMSE=0.33；threeview: 2点 yaw=0° mirror=否 平移=(0.3,0.8) RMSE=0.25；threeview_3pass: yaw=-0° mirror=否 平移=(-0.0,-0.0) RMSE=1.15
- 补偿：baseline: 尺度=0.71 z偏移=+0.00；threeview: 尺度=0.67 z偏移=-1.50；threeview_3pass: 尺度=0.32 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (2.0,3.0), (1.0,5.0), (6.0,7.0), (1.0,1.0), (0.0,2.0), (5.0,5.0), (1.0,4.0), (1.0,3.0), (5.0,1.0), (1.0,2.0), (6.0,6.0), (7.0,1.0), (5.0,1.0), (5.0,6.0) | (5.0,5.0)✓, (5.0,5.0)✓, (6.0,7.0)多, 漏12 | (5.0,5.0)✓, (5.0,5.0)✓, (6.0,6.0)多, 漏12 | (5.1,5.7)✓, (5.5,6.6)✓, (5.1,5.7)✓, (6.4,5.7)多, 漏11 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (2.0,2.0), (1.0,2.0), (6.0,2.0), (1.0,2.0), (0.0,2.0), (5.0,2.0), (1.0,2.0), (1.0,2.0), (5.0,1.0), (1.0,2.0), (6.0,2.0), (7.0,1.0), (5.0,1.0), (5.0,2.0) | - | (6.0,2.0)✓, (5.0,2.0)✓, 漏12 | (5.1,2.0)✓, (5.5,3.0)✓, (5.1,2.0)✓, (6.4,2.0)多, 漏11 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (3.0,2.0), (5.0,2.0), (7.0,2.0), (1.0,2.0), (2.0,2.0), (5.0,2.0), (4.0,2.0), (3.0,2.0), (1.0,1.0), (2.0,2.0), (6.0,2.0), (1.0,1.0), (1.0,1.0), (6.0,2.0) | - | (5.0,2.0)✓, (5.0,2.0)✓, (6.0,2.0)多, 漏12 | (5.7,2.0)✓, (6.6,3.0)✓, (5.7,2.0)✓, (5.7,2.0)多, 漏11 |

- **baseline 问题**：漏画 chair ×12（GT 14，模型 2）
- **threeview 问题**：漏画 chair ×12（GT 14，模型 2）；z 整体偏高（平均 +2.0 格）
- **threeview_3pass 问题**：漏画 chair ×11（GT 14，模型 3）；z 整体偏高（平均 +1.8 格）

### 样本 6 `scene0648_00`（scannet · object_counting）

Q：How many backpack(s) are in this room?

- QA：GT 2 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (5.0,3.0), (4.0,5.0) | (4.0,6.0)✓, 漏1 | (4.8,5.2)✓, 漏1 | (4.0,6.0)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (5.0,1.0), (4.0,1.0) | - | (4.8,4.5)✗3.5, 漏1 | (4.0,4.0)✗3.0, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (3.0,1.0), (5.0,1.0) | - | (5.2,4.5)✗3.5, 漏1 | (6.0,4.0)✗3.2, 漏1 |

- **baseline 问题**：漏画 backpack ×1（GT 2，模型 1）
- **threeview 问题**：漏画 backpack ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 backpack ×1（GT 2，模型 1）

### 样本 7 `45663154`（arkitscenes · object_counting）

Q：How many sofa(s) are in this room?

- QA：GT 2 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (1.0,4.0), (5.0,7.0) | (5.0,6.0)✓, 漏1 | (5.0,5.5)✓, 漏1 | (5.0,6.0)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (1.0,2.0), (5.0,2.0) | - | (5.0,3.5)✓, 漏1 | (5.0,3.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,2.0), (7.0,2.0) | - | (5.5,3.5)✗2.1, 漏1 | (6.0,3.0)✓, 漏1 |

- **baseline 问题**：漏画 sofa ×1（GT 2，模型 1）
- **threeview 问题**：漏画 sofa ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 sofa ×1（GT 2，模型 1）

### 样本 8 `3e8bba0176`（scannetpp · object_counting）

Q：How many keyboard(s) are in this room?

- QA：GT 2 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| keyboard | (5.0,5.0), (5.0,4.0) | (5.0,7.0)✓, 漏1 | (5.1,4.2)✓, 漏1 | (5.0,7.0)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| keyboard | (5.0,2.0), (5.0,2.0) | - | (5.1,3.8)✓, 漏1 | (5.0,4.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| keyboard | (5.0,2.0), (4.0,2.0) | - | (4.2,3.8)✓, 漏1 | (7.0,4.0)✗2.8, 漏1 |

- **baseline 问题**：漏画 keyboard ×1（GT 2，模型 1）
- **threeview 问题**：漏画 keyboard ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 keyboard ×1（GT 2，模型 1）

### 样本 9 `scene0648_00`（scannet · object_counting）

Q：How many table(s) are in this room?

- QA：GT 2 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (6.0,2.0), (2.0,5.0) | (5.0,6.0)✗3.2, 漏1 | (5.1,5.3)✗3.1, 漏1 | (5.0,7.0)✗3.6, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (6.0,3.0), (2.0,2.0) | - | (5.1,3.8)✓, 漏1 | (5.0,2.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (2.0,3.0), (5.0,2.0) | - | (5.3,3.8)✓, 漏1 | (7.0,2.0)✓, 漏1 |

- **baseline 问题**：漏画 table ×1（GT 2，模型 1）
- **threeview 问题**：漏画 table ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 table ×1（GT 2，模型 1）

### 样本 10 `42899461`（arkitscenes · object_counting）

Q：How many table(s) are in this room?

- QA：GT 3 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (6.0,7.0), (1.0,7.0), (6.0,3.0) | (5.0,6.0)✓, 漏2 | (5.0,5.0)✗2.2, 漏2 | (5.0,6.0)✓, 漏2 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (6.0,2.0), (1.0,2.0), (6.0,3.0) | - | (5.0,3.5)✓, 漏2 | (5.0,2.0)✓, 漏2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (7.0,2.0), (7.0,2.0), (3.0,3.0) | - | (5.0,3.5)✗2.1, 漏2 | (6.0,2.0)✓, 漏2 |

- **baseline 问题**：漏画 table ×2（GT 3，模型 1）
- **threeview 问题**：漏画 table ×2（GT 3，模型 1）
- **threeview_3pass 问题**：漏画 table ×2（GT 3，模型 1）

### 样本 11 `ac48a9b736`（scannetpp · object_counting）

Q：How many heater(s) are in this room?

- QA：GT 4 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| heater | (2.0,1.0), (6.0,2.0), (7.0,2.0), (5.0,1.0) | (5.0,8.0)✗6.1, 漏3 | (5.0,8.5)✗6.6, 漏3 | (5.0,9.0)✗7.1, 漏3 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| heater | (2.0,1.0), (6.0,1.0), (7.0,1.0), (5.0,1.0) | - | (5.0,3.5)✗2.5, 漏3 | (5.0,1.0)✓, 漏3 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| heater | (1.0,1.0), (2.0,1.0), (2.0,1.0), (1.0,1.0) | - | (8.5,3.5)✗7.0, 漏3 | (9.0,1.0)✗7.0, 漏3 |

- **baseline 问题**：漏画 heater ×3（GT 4，模型 1）
- **threeview 问题**：漏画 heater ×3（GT 4，模型 1）
- **threeview_3pass 问题**：漏画 heater ×3（GT 4，模型 1）

### 样本 12 `scene0580_01`（scannet · object_counting）

Q：How many pillow(s) are in this room?

- QA：GT 2 | baseline 2（对） | threeview 2（对） | threeview_3pass 2（对）
- 对齐：baseline: 2点 yaw=-45° mirror=否 平移=(-0.8,6.6) RMSE=0.15；threeview: 2点 yaw=135° mirror=否 平移=(10.5,4.4) RMSE=0.07；threeview_3pass: 2点 yaw=-45° mirror=否 平移=(-2.6,4.1) RMSE=0.21
- 补偿：baseline: 尺度=1.41 z偏移=+0.00；threeview: 尺度=0.88 z偏移=-1.50；threeview_3pass: 尺度=0.71 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| pillow | (4.0,6.0), (5.0,5.0) | (4.0,6.0)✓, (4.0,6.0)✓, (5.0,5.0)多 | (4.0,6.0)✓, (5.0,5.0)✓ | (4.0,6.0)✓, (4.0,6.0)✓, (5.0,5.0)多 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| pillow | (4.0,3.0), (5.0,3.0) | - | (4.0,3.0)✓, (5.0,3.0)✓ | (4.0,3.0)✓, (4.0,3.0)✓, (5.0,3.0)多 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| pillow | (6.0,3.0), (5.0,3.0) | - | (6.0,3.0)✓, (5.0,3.0)✓ | (6.0,3.0)✓, (6.0,3.0)✓, (5.0,3.0)多 |

- **threeview 问题**：z 整体偏高（平均 +1.5 格）
- **threeview_3pass 问题**：z 整体偏高（平均 +1.0 格）

### 样本 13 `45662943`（arkitscenes · object_counting）

Q：How many table(s) are in this room?

- QA：GT 2 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (1.0,6.0), (1.0,3.0) | (5.0,6.0)✗4.0, 漏1 | (5.0,5.0)✗4.1, 漏1 | (5.0,6.0)✗4.0, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (1.0,2.0), (1.0,2.0) | - | (5.0,3.5)✗4.3, 漏1 | (5.0,3.0)✗4.1, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (6.0,2.0), (3.0,2.0) | - | (5.0,3.5)✓, 漏1 | (6.0,3.0)✓, 漏1 |

- **baseline 问题**：漏画 table ×1（GT 2，模型 1）
- **threeview 问题**：漏画 table ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 table ×1（GT 2，模型 1）

### 样本 14 `09c1414f1b`（scannetpp · object_counting）

Q：How many refrigerator(s) are in this room?

- QA：GT 1 | baseline 1（对） | threeview 1（对） | threeview_3pass 1（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (2.0,0.0), (3.0,1.0) | (2.0,6.0)✗5.1, 漏1 | (3.5,7.5)✗6.5, 漏1 | (2.0,8.0)✗7.1, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (2.0,6.0), (3.0,4.0) | - | (3.5,5.0)✓, 漏1 | (2.0,4.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (0.0,6.0), (1.0,4.0) | - | (7.5,5.0)✗6.6, 漏1 | (8.0,4.0)✗7.0, 漏1 |

- **baseline 问题**：漏画 refrigerator ×1（GT 2，模型 1）
- **threeview 问题**：漏画 refrigerator ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 refrigerator ×1（GT 2，模型 1）

### 样本 15 `scene0663_00`（scannet · object_counting）

Q：How many table(s) are in this room?

- QA：GT 2 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (6.0,4.0), (2.0,5.0) | (5.0,6.0)✗2.2, 漏1 | (5.0,5.0)✓, 漏1 | (5.0,6.0)✗2.2, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (6.0,2.0), (2.0,2.0) | - | (5.0,3.5)✓, 漏1 | (5.0,2.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (4.0,2.0), (5.0,2.0) | - | (5.0,3.5)✓, 漏1 | (6.0,2.0)✓, 漏1 |

- **baseline 问题**：漏画 table ×1（GT 2，模型 1）
- **threeview 问题**：漏画 table ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 table ×1（GT 2，模型 1）

### 样本 16 `47332918`（arkitscenes · object_counting）

Q：How many table(s) are in this room?

- QA：GT 2 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (1.0,3.0), (4.0,1.0) | (5.0,6.0)✗5.0, 漏1 | (5.0,5.0)✗4.1, 漏1 | (5.0,6.0)✗5.0, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (1.0,1.0), (4.0,2.0) | - | (5.0,3.5)✓, 漏1 | (5.0,3.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (3.0,1.0), (1.0,2.0) | - | (5.0,3.5)✗3.2, 漏1 | (6.0,3.0)✗3.6, 漏1 |

- **baseline 问题**：漏画 table ×1（GT 2，模型 1）
- **threeview 问题**：漏画 table ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 table ×1（GT 2，模型 1）

### 样本 17 `7831862f02`（scannetpp · object_counting）

Q：How many ceiling light(s) are in this room?

- QA：GT 3 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (3.0,6.0), (2.0,2.0), (5.0,3.0) | (5.0,1.0)✓, 漏2 | (5.0,5.0)✓, 漏2 | (5.0,1.0)✓, 漏2 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (3.0,6.0), (2.0,6.0), (5.0,6.0) | - | (5.0,9.0)✗3.0, 漏2 | (5.0,9.0)✗3.0, 漏2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (6.0,6.0), (2.0,6.0), (3.0,6.0) | - | (5.0,9.0)✗3.2, 漏2 | (1.0,9.0)✗3.2, 漏2 |

- **baseline 问题**：漏画 ceiling light ×2（GT 3，模型 1）
- **threeview 问题**：漏画 ceiling light ×2（GT 3，模型 1）
- **threeview_3pass 问题**：漏画 ceiling light ×2（GT 3，模型 1）

### 样本 18 `scene0700_02`（scannet · object_counting）

Q：How many backpack(s) are in this room?

- QA：GT 2 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (5.0,2.0), (5.0,1.0) | (5.0,6.0)✗4.0, 漏1 | (4.6,5.2)✗3.2, 漏1 | (5.0,6.0)✗4.0, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (5.0,3.0), (5.0,2.0) | - | (4.6,3.8)✓, 漏1 | (5.0,3.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (2.0,3.0), (1.0,2.0) | - | (5.2,3.8)✗3.3, 漏1 | (6.0,3.0)✗4.0, 漏1 |

- **baseline 问题**：漏画 backpack ×1（GT 2，模型 1）
- **threeview 问题**：漏画 backpack ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 backpack ×1（GT 2，模型 1）

### 样本 19 `47429904`（arkitscenes · object_counting）

Q：How many stool(s) are in this room?

- QA：GT 2 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (5.0,5.0), (2.0,5.0) | (5.0,6.0)✓, 漏1 | (5.0,5.0)✓, 漏1 | (5.0,6.0)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (5.0,2.0), (2.0,2.0) | - | (5.0,3.5)✓, 漏1 | (5.0,2.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (5.0,2.0), (5.0,2.0) | - | (5.0,3.5)✓, 漏1 | (6.0,2.0)✓, 漏1 |

- **baseline 问题**：漏画 stool ×1（GT 2，模型 1）
- **threeview 问题**：漏画 stool ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 stool ×1（GT 2，模型 1）

### 样本 20 `1ada7a0617`（scannetpp · object_counting）

Q：How many bucket(s) are in this room?

- QA：GT 2 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bucket | (2.0,6.0), (3.0,6.0) | (5.0,8.0)✗2.8, 漏1 | (5.5,4.5)✗2.9, 漏1 | (5.0,8.0)✗2.8, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bucket | (2.0,1.0), (3.0,1.0) | - | (5.5,3.5)✗3.5, 漏1 | (5.0,2.0)✗2.2, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bucket | (6.0,1.0), (6.0,1.0) | - | (4.5,3.5)✗2.9, 漏1 | (8.0,2.0)✗2.2, 漏1 |

- **baseline 问题**：漏画 bucket ×1（GT 2，模型 1）
- **threeview 问题**：漏画 bucket ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 bucket ×1（GT 2，模型 1）

### 样本 21 `scene0222_01`（scannet · object_counting）

Q：How many pillow(s) are in this room?

- QA：GT 3 | baseline 2（错） | threeview 2（错） | threeview_3pass 2（错）
- 对齐：baseline: 2点 yaw=0° mirror=否 平移=(-0.5,2.0) RMSE=1.06；threeview: 2点 yaw=56° mirror=否 平移=(3.8,-1.9) RMSE=1.98；threeview_3pass: 2点 yaw=56° mirror=否 平移=(4.0,-1.4) RMSE=2.20
- 补偿：baseline: 尺度=4.00 z偏移=+0.00；threeview: 尺度=4.51 z偏移=-0.50；threeview_3pass: 尺度=7.21 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| pillow | (6.0,7.0), (2.0,1.0), (2.0,7.0) | (6.0,7.0)✓, (2.0,7.0)✓, 漏1 | (2.0,1.0)✓, (2.0,1.0)✓, (6.0,7.0)多, 漏1 | (6.0,7.0)✓, (2.0,1.0)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| pillow | (6.0,4.0), (2.0,4.0), (2.0,1.0) | - | (6.0,4.0)✓, (2.0,4.0)✓, 漏1 | (6.0,4.0)✓, (2.0,4.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| pillow | (7.0,4.0), (1.0,4.0), (7.0,1.0) | - | (1.0,4.0)✓, (1.0,4.0)✓, (7.0,4.0)多, 漏1 | (7.0,4.0)✓, (1.0,4.0)✓, 漏1 |

- **baseline 问题**：漏画 pillow ×1（GT 3，模型 2）
- **threeview 问题**：漏画 pillow ×1（GT 3，模型 2）；z 整体偏高（平均 +2.0 格）
- **threeview_3pass 问题**：漏画 pillow ×1（GT 3，模型 2）；z 整体偏高（平均 +1.5 格）

### 样本 22 `47334380`（arkitscenes · object_counting）

Q：How many chair(s) are in this room?

- QA：GT 2 | baseline 2（对） | threeview 2（对） | threeview_3pass 1（错）
- 对齐：baseline: 2点 yaw=-0° mirror=否 平移=(1.5,0.5) RMSE=0.50；threeview: 2点 yaw=45° mirror=否 平移=(6.1,-1.1) RMSE=0.43；threeview_3pass: 对齐失败(匹配实例<2)
- 补偿：baseline: 尺度=2.00 z偏移=+0.00；threeview: 尺度=1.77 z偏移=-1.80

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (5.0,5.0), (7.0,7.0) | (5.0,5.0)✓, (5.0,5.0)✓, (7.0,7.0)多 | (5.0,5.0)✓, (5.0,5.0)✓, (7.0,7.0)多 | (5.0,6.0)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (5.0,2.0), (7.0,2.0) | - | (5.0,2.0)✓, (5.0,2.0)✓, (7.0,2.0)多 | (5.0,3.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (5.0,2.0), (7.0,2.0) | - | (5.0,2.0)✓, (5.0,2.0)✓, (7.0,2.0)多 | (6.0,3.0)✓, 漏1 |

- **threeview 问题**：z 整体偏高（平均 +1.8 格）
- **threeview_3pass 问题**：漏画 chair ×1（GT 2，模型 1）

### 样本 23 `acd95847c5`（scannetpp · object_counting）

Q：How many ceiling light(s) are in this room?

- QA：GT 4 | baseline 2（错） | threeview 1（错） | threeview_3pass 2（错）
- 对齐：baseline: 2点 yaw=45° mirror=否 平移=(2.4,-1.2) RMSE=0.56；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 2点 yaw=0° mirror=否 平移=(-0.5,1.0) RMSE=0.35
- 补偿：baseline: 尺度=2.12 z偏移=+0.00；threeview_3pass: 尺度=0.75 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (3.0,3.0), (3.0,6.0), (6.0,6.0), (6.0,3.0) | (3.0,3.0)✓, (6.0,3.0)✓, 漏2 | (5.0,5.0)✓, 漏3 | (3.0,3.0)✓, (3.0,3.0)✓, (6.0,3.0)多, 漏2 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (3.0,7.0), (3.0,8.0), (6.0,7.0), (6.0,8.0) | - | (5.0,8.5)✓, 漏3 | (3.0,8.0)✓, (3.0,8.0)✓, (6.0,8.0)多, 漏2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (3.0,7.0), (6.0,8.0), (6.0,7.0), (3.0,8.0) | - | (5.0,8.5)✓, 漏3 | (3.0,8.0)✓, (3.0,8.0)✓, (3.0,8.0)多, 漏2 |

- **baseline 问题**：漏画 ceiling light ×2（GT 4，模型 2）
- **threeview 问题**：漏画 ceiling light ×3（GT 4，模型 1）
- **threeview_3pass 问题**：漏画 ceiling light ×2（GT 4，模型 2）；z 整体偏高（平均 +1.5 格）

### 样本 24 `scene0518_00`（scannet · object_counting）

Q：How many table(s) are in this room?

- QA：GT 2 | baseline 1（错） | threeview 1（错） | threeview_3pass 1（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (4.0,7.0), (3.0,3.0) | (5.0,6.0)✓, 漏1 | (5.1,5.3)✗2.0, 漏1 | (5.0,6.0)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (4.0,3.0), (3.0,2.0) | - | (5.1,3.8)✓, 漏1 | (5.0,3.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (7.0,3.0), (3.0,2.0) | - | (5.3,3.8)✓, 漏1 | (6.0,3.0)✓, 漏1 |

- **baseline 问题**：漏画 table ×1（GT 2，模型 1）
- **threeview 问题**：漏画 table ×1（GT 2，模型 1）
- **threeview_3pass 问题**：漏画 table ×1（GT 2，模型 1）

### 样本 25 `47333940`（arkitscenes · object_counting）

Q：How many chair(s) are in this room?

- QA：GT 2 | baseline 2（对） | threeview 2（对） | threeview_3pass 2（对）
- 对齐：baseline: 2点 yaw=90° mirror=否 平移=(12.0,-2.5) RMSE=1.06；threeview: 2点 yaw=73° mirror=否 平移=(10.7,-4.2) RMSE=0.50；threeview_3pass: 2点 yaw=90° mirror=否 平移=(14.0,-2.5) RMSE=0.35
- 补偿：baseline: 尺度=0.25 z偏移=+0.00；threeview: 尺度=0.42 z偏移=-0.50；threeview_3pass: 尺度=0.50 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (7.0,3.0), (7.0,2.0) | (7.0,3.0)✓, (7.0,2.0)✓ | (7.0,3.0)✓, (7.0,2.0)✓ | (7.0,3.0)✓, (7.0,2.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (7.0,3.0), (7.0,3.0) | - | (7.0,3.0)✓, (7.0,3.0)✓, (7.0,3.0)多 | (7.0,3.0)✓, (7.0,3.0)✓, (7.0,3.0)多 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (3.0,3.0), (2.0,3.0) | - | (3.0,3.0)✓, (2.0,3.0)✓ | (3.0,3.0)✓, (2.0,3.0)✓ |

- **threeview 问题**：z 整体偏高（平均 +0.5 格）

### 样本 26 `47429922`（arkitscenes · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the chair and the sofa (in meters)?

- QA：GT 0.9 | baseline 1.5（错） | threeview 0.3（错） | threeview_3pass 0.5（错）
- 对齐：baseline: 2点 yaw=-63° mirror=否 平移=(-3.7,6.1) RMSE=0.19；threeview: 2点 yaw=-135° mirror=否 平移=(2.4,9.7) RMSE=0.77；threeview_3pass: 2点 yaw=-56° mirror=否 平移=(-3.6,5.5) RMSE=0.49
- 补偿：baseline: 尺度=1.12 z偏移=+0.00；threeview: 尺度=1.77 z偏移=-1.00；threeview_3pass: 尺度=1.39 z偏移=+0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (6.0,3.0) | (6.0,3.0)✓, (4.0,7.0)多, 多1 | (6.0,3.0)✓ | (6.0,3.0)✓, (2.9,7.6)多, 多1 |
| sofa | (1.0,3.0) | (1.0,3.0)✓ | (1.0,3.0)✓ | (1.0,3.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (6.0,3.0) | - | (6.0,2.5)✓ | (6.0,2.5)✓, (2.9,2.5)多, 多1 |
| sofa | (1.0,2.0) | - | (1.0,2.5)✓ | (1.0,2.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (3.0,3.0) | - | (3.0,2.5)✓ | (3.0,2.5)✓, (7.6,2.5)多, 多1 |
| sofa | (3.0,2.0) | - | (3.0,2.5)✓ | (3.0,2.5)✓ |

- **baseline 问题**：多画 chair ×1（GT 1，模型 2）；chair→sofa 方向错（GT E，模型 NE）
- **threeview 问题**：chair-sofa 距离画错（GT 5.0，模型 2.8）；z 整体偏高（平均 +1.0 格）
- **threeview_3pass 问题**：多画 chair ×1（GT 1，模型 2）；chair-sofa 距离画错（GT 5.0，模型 3.6）；chair→sofa 方向错（GT E，模型 NE）；z 整体偏低（平均 -0.5 格）

### 样本 27 `e398684d27`（scannetpp · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the monitor and the ceiling light (in meters)?

- QA：GT 1.4 | baseline 2.3（错） | threeview 1.4（对） | threeview_3pass 3.5（错）
- 对齐：baseline: 2点 yaw=59° mirror=否 平移=(3.5,-0.3) RMSE=0.65；threeview: 2点 yaw=-121° mirror=否 平移=(2.0,12.2) RMSE=1.88；threeview_3pass: 2点 yaw=-121° mirror=否 平移=(2.2,12.1) RMSE=1.71
- 补偿：baseline: 尺度=1.46 z偏移=+0.00；threeview: 尺度=11.66 z偏移=+0.00；threeview_3pass: 尺度=5.83 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (6.0,4.0) | (6.0,4.0)✓ | (6.0,4.0)✓ | (6.0,4.0)✓, (-14.0,16.0)多, 多1 |
| monitor | (1.0,7.0) | (1.0,7.0)✓ | (1.0,7.0)✓ | (1.0,7.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (6.0,8.0) | - | (6.0,8.5)✓ | (6.0,9.0)✓, (-14.0,9.0)多, 多1 |
| monitor | (1.0,5.0) | - | (1.0,4.5)✓ | (1.0,4.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (4.0,8.0) | - | (4.0,8.5)✓ | (4.0,9.0)✓, (16.0,9.0)多, 多1 |
| monitor | (7.0,5.0) | - | (7.0,4.5)✓ | (7.0,4.0)✓ |

- **baseline 问题**：ceiling light-monitor 距离画错（GT 5.8，模型 4.0）
- **threeview 问题**：ceiling light-monitor 距离画错（GT 5.8，模型 0.5）
- **threeview_3pass 问题**：多画 ceiling light ×1（GT 1，模型 2）；ceiling light-monitor 距离画错（GT 5.8，模型 1.0）；ceiling light→monitor 方向错（GT SE，模型 NW）

### 样本 28 `scene0246_00`（scannet · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the table and the bed (in meters)?

- QA：GT 1.0 | baseline 1.5（错） | threeview 0.1（错） | threeview_3pass 0.5（错）
- 对齐：baseline: 2点 yaw=90° mirror=否 平移=(9.5,0.5) RMSE=0.50；threeview: 2点 yaw=11° mirror=否 平移=(0.3,-0.1) RMSE=0.73；threeview_3pass: 2点 yaw=90° mirror=否 平移=(9.5,0.5) RMSE=0.50
- 补偿：baseline: 尺度=1.33 z偏移=+0.00；threeview: 尺度=1.57 z偏移=-0.75；threeview_3pass: 尺度=1.33 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,6.0) | (5.0,6.0)✓ | (5.0,6.0)✓ | (5.0,6.0)✓ |
| table | (1.0,2.0) | (1.0,2.0)✓ | (1.0,2.0)✓ | (1.0,2.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,2.0) | - | (5.0,2.2)✓ | (5.0,2.0)✓ |
| table | (1.0,2.0) | - | (1.0,1.8)✓ | (1.0,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,2.0) | - | (6.0,2.2)✓ | (6.0,2.0)✓ |
| table | (2.0,2.0) | - | (2.0,1.8)✓ | (2.0,2.0)✓ |

- **baseline 问题**：bed-table 距离画错（GT 5.7，模型 4.2）
- **threeview 问题**：bed-table 距离画错（GT 5.7，模型 3.6）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：bed-table 距离画错（GT 5.7，模型 4.2）

### 样本 29 `47333441`（arkitscenes · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the stool and the toilet (in meters)?

- QA：GT 0.8 | baseline 0.6（错） | threeview 0.2（错） | threeview_3pass 0.25（错）
- 对齐：baseline: 2点 yaw=125° mirror=否 平移=(11.4,5.0) RMSE=0.65；threeview: 2点 yaw=98° mirror=否 平移=(8.3,1.4) RMSE=1.02；threeview_3pass: 2点 yaw=-18° mirror=否 平移=(-1.6,0.9) RMSE=0.65
- 补偿：baseline: 尺度=1.58 z偏移=+0.00；threeview: 尺度=2.36 z偏移=-1.25；threeview_3pass: 尺度=1.58 z偏移=-0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (2.0,3.0) | (2.0,3.0)✓ | (2.0,3.0)✓ | (2.0,3.0)✓ |
| toilet | (5.0,7.0) | (5.0,7.0)✓ | (5.0,7.0)✓ | (5.0,7.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (2.0,1.0) | - | (2.0,1.2)✓ | (2.0,1.5)✓ |
| toilet | (5.0,3.0) | - | (5.0,2.8)✓ | (5.0,2.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (3.0,1.0) | - | (3.0,1.2)✓ | (3.0,1.5)✓ |
| toilet | (7.0,3.0) | - | (7.0,2.8)✓ | (7.0,2.5)✓ |

- **baseline 问题**：stool-toilet 距离画错（GT 5.0，模型 3.2）
- **threeview 问题**：stool-toilet 距离画错（GT 5.0，模型 2.1）；z 整体偏高（平均 +1.2 格）
- **threeview_3pass 问题**：stool-toilet 距离画错（GT 5.0，模型 3.2）；z 整体偏高（平均 +0.5 格）

### 样本 30 `40aec5fffa`（scannetpp · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the door and the refrigerator (in meters)?

- QA：GT 3.3 | baseline 3.0（错） | threeview 1.2（错） | threeview_3pass 0.5（错）
- 对齐：baseline: 2点 yaw=-127° mirror=否 平移=(0.8,12.4) RMSE=0.00；threeview: 2点 yaw=90° mirror=否 平移=(9.5,2.0) RMSE=0.79；threeview_3pass: 2点 yaw=98° mirror=否 平移=(9.6,3.9) RMSE=1.25
- 补偿：baseline: 尺度=1.00 z偏移=+0.00；threeview: 尺度=1.50 z偏移=-0.75；threeview_3pass: 尺度=2.12 z偏移=+0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (0.0,3.0) | (-0.0,3.0)✓ | (0.0,3.0)✓ | (0.0,3.0)✓ |
| refrigerator | (6.0,6.0) | (6.0,6.0)✓ | (6.0,6.0)✓ | (6.0,6.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (0.0,4.0) | - | (0.0,3.8)✓ | (0.0,4.5)✓ |
| refrigerator | (6.0,4.0) | - | (6.0,4.2)✓ | (6.0,3.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (3.0,4.0) | - | (3.0,3.8)✓ | (3.0,4.5)✓ |
| refrigerator | (6.0,4.0) | - | (6.0,4.2)✓ | (6.0,3.5)✓ |

- **threeview 问题**：door-refrigerator 距离画错（GT 6.7，模型 4.5）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：door-refrigerator 距离画错（GT 6.7，模型 3.2）；z 整体偏低（平均 -0.5 格）

### 样本 31 `scene0580_01`（scannet · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the lamp and the window (in meters)?

- QA：GT 2.1 | baseline 2.5（错） | threeview 1.5（错） | threeview_3pass 1.5（错）
- 对齐：baseline: 2点 yaw=-10° mirror=否 平移=(1.0,2.7) RMSE=0.19；threeview: 2点 yaw=-124° mirror=否 平移=(1.5,11.9) RMSE=0.24；threeview_3pass: 2点 yaw=0° mirror=否 平移=(1.0,2.0) RMSE=0.00
- 补偿：baseline: 尺度=0.89 z偏移=+0.00；threeview: 尺度=0.87 z偏移=-1.00；threeview_3pass: 尺度=1.00 z偏移=-0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (4.0,7.0) | (4.0,7.0)✓ | (4.0,7.0)✓ | (4.0,7.0)✓ |
| window | (6.0,3.0) | (6.0,3.0)✓ | (6.0,3.0)✓ | (6.0,3.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (4.0,4.0) | - | (4.0,3.0)✓ | (4.0,3.5)✓ |
| window | (6.0,4.0) | - | (6.0,5.0)✓ | (6.0,4.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (7.0,4.0) | - | (7.0,3.0)✓ | (7.0,3.5)✓ |
| window | (3.0,4.0) | - | (3.0,5.0)✓ | (3.0,4.5)✓ |

- **threeview 问题**：z 整体偏高（平均 +1.0 格）
- **threeview_3pass 问题**：z 整体偏高（平均 +0.5 格）

### 样本 32 `47334103`（arkitscenes · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the table and the stool (in meters)?

- QA：GT 3.7 | baseline 0.3（错） | threeview 0.3（错） | threeview_3pass 0.5（错）
- 对齐：baseline: 2点 yaw=60° mirror=否 平移=(7.9,-5.6) RMSE=0.68；threeview: 2点 yaw=-11° mirror=否 平移=(-0.6,-2.6) RMSE=1.27；threeview_3pass: 2点 yaw=-11° mirror=否 平移=(-0.4,-2.6) RMSE=1.10
- 补偿：baseline: 尺度=1.61 z偏移=+0.00；threeview: 尺度=3.40 z偏移=-1.25；threeview_3pass: 尺度=2.55 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (2.0,2.0) | (2.0,2.0)✓, (3.6,4.8)多, 多1 | (2.0,2.0)✓, (12.0,0.0)多, 多1 | (2.0,2.0)✓, (12.0,0.0)多, 多1 |
| table | (7.0,1.0) | (7.0,1.0)✓ | (7.0,1.0)✓ | (7.0,1.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (2.0,1.0) | - | (2.0,1.2)✓, (12.0,1.2)多, 多1 | (2.0,1.0)✓, (12.0,1.0)多, 多1 |
| table | (7.0,2.0) | - | (7.0,1.8)✓ | (7.0,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (2.0,1.0) | - | (2.0,1.2)✓, (0.0,1.2)多, 多1 | (2.0,1.0)✓, (0.0,1.0)多, 多1 |
| table | (1.0,2.0) | - | (1.0,1.8)✓ | (1.0,2.0)✓ |

- **baseline 问题**：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 5.1，模型 3.2）；stool→table 方向错（GT W，模型 NW）
- **threeview 问题**：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 5.1，模型 1.5）；stool→table 方向错（GT W，模型 E）；z 整体偏高（平均 +1.2 格）
- **threeview_3pass 问题**：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 5.1，模型 2.0）；stool→table 方向错（GT W，模型 N）；z 整体偏高（平均 +1.0 格）

### 样本 33 `1ada7a0617`（scannetpp · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the door and the heater (in meters)?

- QA：GT 4.5 | baseline 2.5（错） | threeview 2.8（错） | threeview_3pass 1.8（错）
- 对齐：baseline: 2点 yaw=-43° mirror=否 平移=(-3.1,2.1) RMSE=0.87；threeview: 2点 yaw=-75° mirror=否 平移=(-1.7,6.2) RMSE=0.27；threeview_3pass: 2点 yaw=-45° mirror=否 平移=(-3.6,2.2) RMSE=0.47
- 补偿：baseline: 尺度=1.55 z偏移=+0.00；threeview: 尺度=0.90 z偏移=-1.25；threeview_3pass: 尺度=1.24 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (0.0,5.0) | (-0.0,5.0)✓ | (0.0,5.0)✓ | (0.0,5.0)✓ |
| heater | (7.0,5.0) | (7.0,5.0)✓ | (7.0,5.0)✓ | (7.0,5.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (0.0,4.0) | - | (0.0,3.2)✓ | (0.0,4.0)✓ |
| heater | (7.0,1.0) | - | (7.0,1.8)✓ | (7.0,1.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (5.0,4.0) | - | (5.0,3.2)✓ | (5.0,4.0)✓ |
| heater | (5.0,1.0) | - | (5.0,1.8)✓ | (5.0,1.0)✓ |

- **baseline 问题**：door-heater 距离画错（GT 7.0，模型 4.5）
- **threeview 问题**：z 整体偏高（平均 +1.2 格）
- **threeview_3pass 问题**：door-heater 距离画错（GT 7.0，模型 5.7）

### 样本 34 `scene0100_00`（scannet · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the trash bin and the window (in meters)?

- QA：GT 1.0 | baseline 3.5（错） | threeview 2.3（错） | threeview_3pass 2.1（错）
- 对齐：baseline: 2点 yaw=-169° mirror=否 平移=(4.6,7.2) RMSE=1.78；threeview: 2点 yaw=-171° mirror=否 平移=(4.8,6.4) RMSE=1.61；threeview_3pass: 2点 yaw=48° mirror=否 平移=(3.7,-5.3) RMSE=1.11
- 补偿：baseline: 尺度=0.31 z偏移=+0.00；threeview: 尺度=0.33 z偏移=-0.50；threeview_3pass: 尺度=0.42 z偏移=+0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash bin | (2.0,1.0) | (2.0,1.0)✓ | (2.0,1.0)✓ | (2.0,1.0)✓ |
| window | (1.0,3.0) | (1.0,3.0)✓ | (1.0,3.0)✓ | (1.0,3.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash bin | (2.0,1.0) | - | (2.0,1.5)✓ | (2.0,1.5)✓ |
| window | (1.0,6.0) | - | (1.0,5.5)✓ | (1.0,5.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash bin | (1.0,1.0) | - | (1.0,1.5)✓ | (1.0,1.5)✓ |
| window | (3.0,6.0) | - | (3.0,5.5)✓ | (3.0,5.5)✓ |

- **baseline 问题**：trash bin-window 距离画错（GT 2.2，模型 7.3）
- **threeview 问题**：trash bin-window 距离画错（GT 2.2，模型 6.8）；z 整体偏高（平均 +0.5 格）
- **threeview_3pass 问题**：trash bin-window 距离画错（GT 2.2，模型 5.4）；z 整体偏低（平均 -0.5 格）

### 样本 35 `45261142`（arkitscenes · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the tv and the washer (in meters)?

- QA：GT 2.7 | baseline 3.0（错） | threeview 0.7（错） | threeview_3pass 0（错）
- 对齐：baseline: 2点 yaw=-108° mirror=否 平移=(0.8,12.3) RMSE=0.11；threeview: 2点 yaw=152° mirror=否 平移=(10.6,7.9) RMSE=1.16；threeview_3pass: 对齐失败(匹配实例<2)
- 补偿：baseline: 尺度=1.05 z偏移=+0.00；threeview: 尺度=2.08 z偏移=-0.75

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| tv | (1.0,7.0) | (1.0,7.0)✓ | (1.0,7.0)✓ | 漏1 |
| washer | (7.0,5.0) | (7.0,5.0)✓ | (7.0,5.0)✓ | (5.0,8.0)✗3.6 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| tv | (1.0,6.0) | - | (1.0,5.2)✓ | 漏1 |
| washer | (7.0,2.0) | - | (7.0,2.8)✓ | (5.0,3.0)✗2.2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| tv | (7.0,6.0) | - | (7.0,5.2)✓ | 漏1 |
| washer | (5.0,2.0) | - | (5.0,2.8)✓ | (8.0,3.0)✗3.2 |

- **threeview 问题**：tv-washer 距离画错（GT 6.3，模型 3.0）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：漏画 tv ×1（GT 1，模型 0）

### 样本 36 `21d970d8de`（scannetpp · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the door and the telephone (in meters)?

- QA：GT 7.1 | baseline 2.5（错） | threeview 1.3（错） | threeview_3pass 1.25（错）
- 对齐：baseline: 2点 yaw=74° mirror=否 平移=(10.0,-0.8) RMSE=1.16；threeview: 2点 yaw=82° mirror=否 平移=(10.3,0.1) RMSE=1.32；threeview_3pass: 2点 yaw=88° mirror=否 平移=(10.4,0.4) RMSE=1.12
- 补偿：baseline: 尺度=1.82 z偏移=+0.00；threeview: 尺度=2.06 z偏移=-1.50；threeview_3pass: 尺度=1.77 z偏移=-2.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (5.0,0.0) | (5.0,0.0)✓ | (5.0,0.0)✓ | (5.0,0.0)✓ |
| telephone | (7.0,7.0) | (7.0,7.0)✓ | (7.0,7.0)✓ | (7.0,7.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (5.0,3.0) | - | (5.0,3.0)✓ | (5.0,3.0)✓ |
| telephone | (7.0,2.0) | - | (7.0,2.0)✓ | (7.0,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (0.0,3.0) | - | (0.0,3.0)✓ | (0.0,3.0)✓ |
| telephone | (7.0,2.0) | - | (7.0,2.0)✓ | (7.0,2.0)✓ |

- **baseline 问题**：door-telephone 距离画错（GT 7.3，模型 4.0）
- **threeview 问题**：door-telephone 距离画错（GT 7.3，模型 3.5）；z 整体偏高（平均 +1.5 格）
- **threeview_3pass 问题**：door-telephone 距离画错（GT 7.3，模型 4.1）；z 整体偏高（平均 +2.0 格）

### 样本 37 `scene0518_00`（scannet · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the tv and the sofa (in meters)?

- QA：GT 1.5 | baseline 2.5（错） | threeview 1.4（错） | threeview_3pass 2.0（错）
- 对齐：baseline: 2点 yaw=-101° mirror=否 平移=(-0.4,9.4) RMSE=0.39；threeview: 2点 yaw=79° mirror=否 平移=(7.9,-2.5) RMSE=0.39；threeview_3pass: 2点 yaw=-101° mirror=否 平移=(-0.4,9.4) RMSE=0.32
- 补偿：baseline: 尺度=1.27 z偏移=+0.00；threeview: 尺度=1.27 z偏移=+0.00；threeview_3pass: 尺度=0.85 z偏移=+1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (6.0,3.0) | (6.0,3.0)✓ | (6.0,3.0)✓ | (6.0,3.0)✓ |
| tv | (1.0,4.0) | (1.0,4.0)✓ | (1.0,4.0)✓ | (1.0,4.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (6.0,3.0) | - | (6.0,3.5)✓ | (6.0,3.0)✓ |
| tv | (1.0,6.0) | - | (1.0,5.5)✓ | (1.0,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (3.0,3.0) | - | (3.0,3.5)✓ | (3.0,3.0)✓ |
| tv | (4.0,6.0) | - | (4.0,5.5)✓ | (4.0,6.0)✓ |

- **baseline 问题**：sofa-tv 距离画错（GT 5.1，模型 4.0）
- **threeview 问题**：sofa-tv 距离画错（GT 5.1，模型 4.0）
- **threeview_3pass 问题**：z 整体偏低（平均 -1.0 格）

### 样本 38 `42899461`（arkitscenes · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the stove and the tv (in meters)?

- QA：GT 4.8 | baseline 3.5（错） | threeview 1.9（错） | threeview_3pass 2.5（错）
- 对齐：baseline: 2点 yaw=180° mirror=否 平移=(6.0,9.5) RMSE=0.35；threeview: 2点 yaw=59° mirror=否 平移=(3.6,-3.4) RMSE=0.06；threeview_3pass: 2点 yaw=130° mirror=否 平移=(8.4,3.7) RMSE=0.64
- 补偿：baseline: 尺度=1.20 z偏移=+0.00；threeview: 尺度=1.03 z偏移=+1.75；threeview_3pass: 尺度=0.77 z偏移=+2.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (1.0,1.0) | (1.0,1.0)✓ | (1.0,1.0)✓ | (1.0,1.0)✓ |
| tv | (1.0,7.0) | (1.0,7.0)✓ | (1.0,7.0)✓ | (1.0,7.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (1.0,7.0) | - | (1.0,4.8)✗2.2 | (1.0,4.5)✗2.5 |
| tv | (1.0,5.0) | - | (1.0,7.2)✗2.2 | (1.0,7.5)✗2.5 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (1.0,7.0) | - | (1.0,4.8)✗2.2 | (1.0,4.5)✗2.5 |
| tv | (7.0,5.0) | - | (7.0,7.2)✗2.2 | (7.0,7.5)✗2.5 |

- **threeview 问题**：z 整体偏低（平均 -1.8 格）
- **threeview_3pass 问题**：stove-tv 距离画错（GT 6.0，模型 7.8）；z 整体偏低（平均 -2.5 格）

### 样本 39 `f9f95681fd`（scannetpp · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the kettle and the door (in meters)?

- QA：GT 1.5 | baseline 2.5（错） | threeview 1.5（对） | threeview_3pass 2.5（错）
- 对齐：baseline: 2点 yaw=0° mirror=否 平移=(1.0,-2.0) RMSE=0.71；threeview: 2点 yaw=45° mirror=否 平移=(6.8,-4.1) RMSE=0.62；threeview_3pass: 2点 yaw=-14° mirror=否 平移=(-0.2,-1.6) RMSE=0.66
- 补偿：baseline: 尺度=1.50 z偏移=+0.00；threeview: 尺度=1.41 z偏移=-1.10；threeview_3pass: 尺度=1.46 z偏移=-0.75

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,3.0) | (1.0,3.0)✓ | (1.0,3.0)✓ | (1.0,3.0)✓ |
| kettle | (7.0,3.0) | (7.0,3.0)✓ | (7.0,3.0)✓ | (7.0,3.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,4.0) | - | (1.0,3.9)✓ | (1.0,3.8)✓ |
| kettle | (7.0,3.0) | - | (7.0,3.1)✓ | (7.0,3.2)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (3.0,4.0) | - | (3.0,3.9)✓ | (3.0,3.8)✓ |
| kettle | (3.0,3.0) | - | (3.0,3.1)✓ | (3.0,3.2)✓ |

- **baseline 问题**：door-kettle 距离画错（GT 6.0，模型 4.0）
- **threeview 问题**：door-kettle 距离画错（GT 6.0，模型 4.2）；z 整体偏高（平均 +1.1 格）
- **threeview_3pass 问题**：door-kettle 距离画错（GT 6.0，模型 4.1）；z 整体偏高（平均 +0.8 格）

### 样本 40 `scene0693_00`（scannet · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the door and the window (in meters)?

- QA：GT 1.9 | baseline 4.0（错） | threeview 1.5（错） | threeview_3pass 2.8（错）
- 对齐：baseline: 2点 yaw=-143° mirror=否 平移=(4.1,6.7) RMSE=0.50；threeview: 2点 yaw=127° mirror=否 平移=(10.9,4.3) RMSE=0.50；threeview_3pass: 2点 yaw=127° mirror=否 平移=(10.9,4.3) RMSE=0.50
- 补偿：baseline: 尺度=1.25 z偏移=+0.00；threeview: 尺度=1.25 z偏移=-0.25；threeview_3pass: 尺度=1.25 z偏移=+1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (7.0,2.0) | (7.0,2.0)✓ | (7.0,2.0)✓ | (7.0,2.0)✓ |
| window | (0.0,3.0) | (-0.0,3.0)✓ | (-0.0,3.0)✓ | (-0.0,3.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (7.0,3.0) | - | (7.0,4.2)✓ | (7.0,4.0)✓ |
| window | (0.0,7.0) | - | (-0.0,5.8)✓ | (-0.0,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (2.0,3.0) | - | (2.0,4.2)✓ | (2.0,4.0)✓ |
| window | (3.0,7.0) | - | (3.0,5.8)✓ | (3.0,6.0)✓ |

- **baseline 问题**：door-window 距离画错（GT 7.1，模型 5.7）
- **threeview 问题**：door-window 距离画错（GT 7.1，模型 5.7）
- **threeview_3pass 问题**：door-window 距离画错（GT 7.1，模型 5.7）；z 整体偏低（平均 -1.0 格）

### 样本 41 `47331063`（arkitscenes · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the refrigerator and the bed (in meters)?

- QA：GT 2.2 | baseline 3.5（错） | threeview 0.6（错） | threeview_3pass 1.0（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 2点 yaw=-173° mirror=否 平移=(9.8,9.2) RMSE=0.92；threeview_3pass: 2点 yaw=168° mirror=否 平移=(10.2,7.8) RMSE=0.65
- 补偿：threeview: 尺度=1.56 z偏移=+0.00；threeview_3pass: 尺度=1.34 z偏移=-0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (7.0,3.0) | (5.0,6.0)✗3.6 | (7.0,3.0)✓ | (7.0,3.0)✓ |
| refrigerator | (1.0,7.0) | 漏1 | (1.0,7.0)✓ | (1.0,7.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (7.0,1.0) | - | (7.0,2.0)✓ | (7.0,1.5)✓ |
| refrigerator | (1.0,4.0) | - | (1.0,3.0)✓ | (1.0,3.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (3.0,1.0) | - | (3.0,2.0)✓ | (3.0,1.5)✓ |
| refrigerator | (7.0,4.0) | - | (7.0,3.0)✓ | (7.0,3.5)✓ |

- **baseline 问题**：漏画 refrigerator ×1（GT 1，模型 0）
- **threeview 问题**：bed-refrigerator 距离画错（GT 7.2，模型 4.6）
- **threeview_3pass 问题**：bed-refrigerator 距离画错（GT 7.2，模型 5.4）；z 整体偏高（平均 +0.5 格）

### 样本 42 `acd95847c5`（scannetpp · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the laptop and the whiteboard (in meters)?

- QA：GT 2.5 | baseline 1.5（错） | threeview 1.25（错） | threeview_3pass 1.0（错）
- 对齐：baseline: 2点 yaw=-27° mirror=否 平移=(-2.2,0.8) RMSE=0.96；threeview: 2点 yaw=-27° mirror=否 平移=(-1.3,2.6) RMSE=1.31；threeview_3pass: 2点 yaw=-8° mirror=否 平移=(-0.6,-0.8) RMSE=1.25
- 补偿：baseline: 尺度=1.68 z偏移=+0.00；threeview: 尺度=2.24 z偏移=-1.75；threeview_3pass: 尺度=2.12 z偏移=-2.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| laptop | (6.0,6.0) | (6.0,6.0)✓ | (6.0,6.0)✓ | (6.0,6.0)✓ |
| whiteboard | (3.0,0.0) | (3.0,0.0)✓ | (3.0,0.0)✓ | (3.0,-0.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| laptop | (6.0,2.0) | - | (6.0,1.8)✓ | (6.0,2.0)✓ |
| whiteboard | (3.0,4.0) | - | (3.0,4.2)✓ | (3.0,4.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| laptop | (6.0,2.0) | - | (6.0,1.8)✓ | (6.0,2.0)✓ |
| whiteboard | (0.0,4.0) | - | (0.0,4.2)✓ | (-0.0,4.0)✓ |

- **baseline 问题**：laptop-whiteboard 距离画错（GT 6.7，模型 4.0）
- **threeview 问题**：laptop-whiteboard 距离画错（GT 6.7，模型 3.0）；z 整体偏高（平均 +1.8 格）
- **threeview_3pass 问题**：laptop-whiteboard 距离画错（GT 6.7，模型 3.2）；z 整体偏高（平均 +2.0 格）

### 样本 43 `scene0593_00`（scannet · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the fan and the sofa (in meters)?

- QA：GT 2.5 | baseline 1.8（错） | threeview 1.9（错） | threeview_3pass 2.1（错）
- 对齐：baseline: 2点 yaw=-117° mirror=否 平移=(1.9,12.2) RMSE=0.87；threeview: 2点 yaw=63° mirror=否 平移=(7.0,-1.6) RMSE=1.40；threeview_3pass: 2点 yaw=-117° mirror=否 平移=(3.2,11.5) RMSE=0.19
- 补偿：baseline: 尺度=2.24 z偏移=+0.00；threeview: 尺度=8.94 z偏移=-3.50；threeview_3pass: 尺度=0.89 z偏移=-3.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| fan | (3.0,6.0) | (3.0,6.0)✓ | (3.0,6.0)✓ | (3.0,6.0)✓ |
| sofa | (7.0,4.0) | (7.0,4.0)✓ | (7.0,4.0)✓ | (7.0,4.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| fan | (3.0,2.0) | - | (3.0,4.5)✗2.5 | (3.0,5.0)✗3.0 |
| sofa | (7.0,2.0) | - | (7.0,-0.5)✗2.5 | (7.0,-1.0)✗3.0 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| fan | (6.0,2.0) | - | (6.0,4.5)✗2.5 | (6.0,5.0)✗3.0 |
| sofa | (4.0,2.0) | - | (4.0,-0.5)✗2.5 | (4.0,-1.0)✗3.0 |

- **baseline 问题**：fan-sofa 距离画错（GT 4.5，模型 2.0）
- **threeview 问题**：fan-sofa 距离画错（GT 4.5，模型 0.5）；z 整体偏高（平均 +3.5 格）
- **threeview_3pass 问题**：z 整体偏高（平均 +3.0 格）

### 样本 44 `42444976`（arkitscenes · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the dishwasher and the refrigerator (in meters)?

- QA：GT 1.8 | baseline 1.2（错） | threeview 0.7（错） | threeview_3pass 1.1（错）
- 对齐：baseline: 2点 yaw=124° mirror=否 平移=(11.8,2.2) RMSE=0.30；threeview: 2点 yaw=-146° mirror=否 平移=(5.3,9.3) RMSE=0.30；threeview_3pass: 2点 yaw=124° mirror=否 平移=(11.8,2.2) RMSE=0.30
- 补偿：baseline: 尺度=1.20 z偏移=+0.00；threeview: 尺度=1.20 z偏移=-0.50；threeview_3pass: 尺度=1.20 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| dishwasher | (2.0,2.0) | (2.0,2.0)✓ | (2.0,2.0)✓ | (2.0,2.0)✓ |
| refrigerator | (7.0,1.0) | (7.0,1.0)✓ | (7.0,1.0)✓ | (7.0,1.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| dishwasher | (2.0,2.0) | - | (2.0,2.0)✓ | (2.0,2.0)✓ |
| refrigerator | (7.0,4.0) | - | (7.0,4.0)✓ | (7.0,4.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| dishwasher | (2.0,2.0) | - | (2.0,2.0)✓ | (2.0,2.0)✓ |
| refrigerator | (1.0,4.0) | - | (1.0,4.0)✓ | (1.0,4.0)✓ |

- **threeview 问题**：z 整体偏高（平均 +0.5 格）

### 样本 45 `45b0dac5e3`（scannetpp · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the door and the ceiling light (in meters)?

- QA：GT 0.9 | baseline 3.0（错） | threeview 1.72（错） | threeview_3pass 1.15（错）
- 对齐：baseline: 2点 yaw=16° mirror=否 平移=(2.5,1.6) RMSE=0.00；threeview: 2点 yaw=-90° mirror=否 平移=(2.0,9.0) RMSE=0.00；threeview_3pass: 2点 yaw=16° mirror=否 平移=(2.5,1.6) RMSE=0.00
- 补偿：baseline: 尺度=1.00 z偏移=+0.00；threeview: 尺度=1.00 z偏移=-1.00；threeview_3pass: 尺度=1.00 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (7.0,4.0) | (7.0,4.0)✓ | (7.0,4.0)✓ | (7.0,4.0)✓ |
| door | (3.0,7.0) | (3.0,7.0)✓ | (3.0,7.0)✓ | (3.0,7.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (7.0,8.0) | - | (7.0,8.0)✓ | (7.0,8.0)✓ |
| door | (3.0,3.0) | - | (3.0,3.0)✓ | (3.0,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (4.0,8.0) | - | (4.0,8.0)✓ | (4.0,8.0)✓ |
| door | (7.0,3.0) | - | (7.0,3.0)✓ | (7.0,3.0)✓ |

- **threeview 问题**：z 整体偏高（平均 +1.0 格）
- **threeview_3pass 问题**：z 整体偏高（平均 +1.0 格）

### 样本 46 `scene0616_01`（scannet · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the lamp and the window (in meters)?

- QA：GT 2.2 | baseline 2.5（错） | threeview 1.9（错） | threeview_3pass 1.5（错）
- 对齐：baseline: 2点 yaw=-153° mirror=否 平移=(4.8,6.2) RMSE=0.19；threeview: 2点 yaw=90° mirror=否 平移=(10.0,-1.8) RMSE=0.40；threeview_3pass: 2点 yaw=-143° mirror=否 平移=(3.8,7.6) RMSE=0.00
- 补偿：baseline: 尺度=0.89 z偏移=+0.00；threeview: 尺度=0.80 z偏移=-0.50；threeview_3pass: 尺度=1.00 z偏移=-0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (5.0,1.0) | (5.0,1.0)✓ | (5.0,1.0)✓ | (5.0,1.0)✓ |
| window | (1.0,3.0) | (1.0,3.0)✓ | (1.0,3.0)✓ | (1.0,3.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (5.0,4.0) | - | (5.0,3.5)✓ | (5.0,3.5)✓ |
| window | (1.0,5.0) | - | (1.0,5.5)✓ | (1.0,5.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (1.0,4.0) | - | (1.0,3.5)✓ | (1.0,3.5)✓ |
| window | (3.0,5.0) | - | (3.0,5.5)✓ | (3.0,5.5)✓ |

- **threeview 问题**：lamp-window 距离画错（GT 4.5，模型 5.6）；z 整体偏高（平均 +0.5 格）
- **threeview_3pass 问题**：z 整体偏高（平均 +0.5 格）

### 样本 47 `47334096`（arkitscenes · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the tv and the sofa (in meters)?

- QA：GT 1.9 | baseline 2.5（错） | threeview 1.8（错） | threeview_3pass 1.58（错）
- 对齐：baseline: 2点 yaw=72° mirror=否 平移=(7.6,-2.5) RMSE=0.30；threeview: 2点 yaw=72° mirror=否 平移=(6.4,-2.1) RMSE=0.47；threeview_3pass: 2点 yaw=-108° mirror=否 平移=(-0.2,10.7) RMSE=0.65
- 补偿：baseline: 尺度=0.79 z偏移=+0.00；threeview: 尺度=0.70 z偏移=-1.00；threeview_3pass: 尺度=0.63 z偏移=+0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,4.0) | (4.0,4.0)✓ | (4.0,4.0)✓ | (4.0,4.0)✓ |
| tv | (1.0,5.0) | (1.0,5.0)✓ | (1.0,5.0)✓ | (1.0,5.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,2.0) | - | (4.0,3.0)✓ | (4.0,2.5)✓ |
| tv | (1.0,6.0) | - | (1.0,5.0)✓ | (1.0,5.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,2.0) | - | (4.0,3.0)✓ | (4.0,2.5)✓ |
| tv | (5.0,6.0) | - | (5.0,5.0)✓ | (5.0,5.5)✓ |

- **threeview 问题**：sofa-tv 距离画错（GT 3.2，模型 4.5）；z 整体偏高（平均 +1.0 格）
- **threeview_3pass 问题**：sofa-tv 距离画错（GT 3.2，模型 5.0）；z 整体偏低（平均 -0.5 格）

### 样本 48 `3864514494`（scannetpp · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the microwave and the heater (in meters)?

- QA：GT 1.9 | baseline 2.0（错） | threeview 1.44（错） | threeview_3pass 1.2（错）
- 对齐：baseline: 2点 yaw=-98° mirror=否 平移=(1.5,12.8) RMSE=0.27；threeview: 2点 yaw=-162° mirror=否 平移=(8.1,11.8) RMSE=0.08；threeview_3pass: 2点 yaw=-76° mirror=否 平移=(-0.2,9.5) RMSE=0.56
- 补偿：baseline: 尺度=0.85 z偏移=+0.00；threeview: 尺度=0.95 z偏移=-0.50；threeview_3pass: 尺度=0.73 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| heater | (8.0,4.0) | (8.0,4.0)✓ | (8.0,4.0)✓ | (8.0,4.0)✓ |
| microwave | (5.0,7.0) | (5.0,7.0)✓ | (5.0,7.0)✓ | (5.0,7.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| heater | (8.0,1.0) | - | (8.0,2.0)✓ | (8.0,2.0)✓ |
| microwave | (5.0,6.0) | - | (5.0,5.0)✓ | (5.0,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| heater | (4.0,1.0) | - | (4.0,2.0)✓ | (4.0,2.0)✓ |
| microwave | (7.0,6.0) | - | (7.0,5.0)✓ | (7.0,5.0)✓ |

- **threeview 问题**：z 整体偏高（平均 +0.5 格）
- **threeview_3pass 问题**：heater-microwave 距离画错（GT 4.2，模型 5.8）

### 样本 49 `scene0645_00`（scannet · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the telephone and the towel (in meters)?

- QA：GT 3.4 | baseline 1.8（错） | threeview 0.3（错） | threeview_3pass 1.8（错）
- 对齐：baseline: 2点 yaw=153° mirror=否 平移=(11.3,7.6) RMSE=0.17；threeview: 2点 yaw=-143° mirror=否 平移=(6.5,10.8) RMSE=0.53；threeview_3pass: 2点 yaw=-127° mirror=否 平移=(2.8,11.9) RMSE=0.35
- 补偿：baseline: 尺度=0.89 z偏移=+0.00；threeview: 尺度=1.60 z偏移=+1.00；threeview_3pass: 尺度=0.80 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| telephone | (5.0,6.0) | (5.0,6.0)✓ | (5.0,6.0)✓ | (5.0,6.0)✓ |
| towel | (5.0,2.0) | (5.0,2.0)✓ | (5.0,2.0)✓ | (5.0,2.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| telephone | (5.0,4.0) | - | (5.0,5.0)✓ | (5.0,5.0)✓ |
| towel | (5.0,5.0) | - | (5.0,4.0)✓ | (5.0,4.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| telephone | (6.0,4.0) | - | (6.0,5.0)✓ | (6.0,5.0)✓ |
| towel | (2.0,5.0) | - | (2.0,4.0)✓ | (2.0,4.0)✓ |

- **threeview 问题**：telephone-towel 距离画错（GT 4.0，模型 2.5）；z 整体偏低（平均 -1.0 格）

### 样本 50 `42899696`（arkitscenes · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the tv and the stool (in meters)?

- QA：GT 2.7 | baseline 2.0（错） | threeview 2.25（错） | threeview_3pass 1.35（错）
- 对齐：baseline: 2点 yaw=108° mirror=否 平移=(9.4,2.2) RMSE=0.65；threeview: 2点 yaw=-65° mirror=否 平移=(-4.2,7.2) RMSE=0.48；threeview_3pass: 2点 yaw=94° mirror=否 平移=(8.8,1.4) RMSE=0.34
- 补偿：baseline: 尺度=0.63 z偏移=+0.00；threeview: 尺度=0.70 z偏移=+0.25；threeview_3pass: 尺度=0.77 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (2.0,5.0) | (2.0,5.0)✓ | (2.0,5.0)✓ | (2.0,5.0)✓, (1.9,6.5)多, 多1 |
| tv | (5.0,6.0) | (5.0,6.0)✓ | (5.0,6.0)✓ | (5.0,6.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (2.0,1.0) | - | (2.0,2.2)✓ | (2.0,2.0)✓, (1.9,2.0)多, 多1 |
| tv | (5.0,7.0) | - | (5.0,5.8)✓ | (5.0,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (5.0,1.0) | - | (5.0,2.2)✓ | (5.0,2.0)✓, (6.5,2.0)多, 多1 |
| tv | (6.0,7.0) | - | (6.0,5.8)✓ | (6.0,6.0)✓ |

- **baseline 问题**：stool-tv 距离画错（GT 3.2，模型 5.0）
- **threeview 问题**：stool-tv 距离画错（GT 3.2，模型 4.5）
- **threeview_3pass 问题**：多画 stool ×1（GT 1，模型 2）

### 样本 51 `42897692`（arkitscenes · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the bed, measured in centimeters?

- QA：GT 215 | baseline 200（对） | threeview 180（对） | threeview_3pass 200（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,5.0) | (5.0,6.0)✓ | (5.0,5.5)✓ | (5.0,6.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,4.0) | - | (5.0,3.5)✓ | (5.0,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,4.0) | - | (5.5,3.5)✓ | (6.0,2.0)✗2.2 |


### 样本 52 `3864514494`（scannetpp · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the heater, measured in centimeters?

- QA：GT 139 | baseline 60（错） | threeview 60（错） | threeview_3pass 75（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| heater | (8.0,4.0) | (5.0,9.0)✗5.8 | (4.8,8.8)✗5.8 | (5.0,8.0)✗5.0 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| heater | (8.0,1.0) | - | (4.8,3.5)✗4.1 | (5.0,3.0)✗3.6 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| heater | (4.0,1.0) | - | (8.8,3.5)✗5.4 | (8.0,3.0)✗4.5 |


### 样本 53 `scene0277_02`（scannet · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the bed, measured in centimeters?

- QA：GT 221 | baseline 200（对） | threeview 192（对） | threeview_3pass 200（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (2.0,2.0) | (5.0,6.0)✗5.0 | (5.0,5.2)✗4.4 | (5.0,6.0)✗5.0 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (2.0,3.0) | - | (5.0,3.5)✗3.0 | (5.0,3.0)✗3.0 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (2.0,3.0) | - | (5.2,3.5)✗3.2 | (6.0,3.0)✗4.0 |


### 样本 54 `42446529`（arkitscenes · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the table, measured in centimeters?

- QA：GT 92 | baseline 120（对） | threeview 180（对） | threeview_3pass 150（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (1.0,3.0) | (5.0,7.0)✗5.7 | (5.0,5.5)✗4.7 | (5.0,7.0)✗5.7 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (1.0,4.0) | - | (5.0,3.5)✗4.0 | (5.0,2.0)✗4.5 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (3.0,4.0) | - | (5.5,3.5)✗2.5 | (7.0,2.0)✗4.5 |


### 样本 55 `d755b3d9d8`（scannetpp · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the door, measured in centimeters?

- QA：GT 199 | baseline 200（对） | threeview 200（对） | threeview_3pass 200（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (0.0,4.0) | (1.0,5.0)✓ | (1.1,5.2)✓ | (1.0,5.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (0.0,3.0) | - | (1.1,4.8)✗2.1 | (1.0,4.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (4.0,3.0) | - | (5.2,4.8)✗2.2 | (5.0,4.5)✓ |


### 样本 56 `scene0246_00`（scannet · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the table, measured in centimeters?

- QA：GT 130 | baseline 120（对） | threeview 200（对） | threeview_3pass 120（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (1.0,2.0) | (5.0,6.0)✗5.7 | (5.0,5.0)✗5.0 | (5.0,6.0)✗5.7 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (1.0,2.0) | - | (5.0,3.5)✗4.3 | (5.0,3.0)✗4.1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (2.0,2.0) | - | (5.0,3.5)✗3.4 | (6.0,3.0)✗4.1 |


### 样本 57 `42899612`（arkitscenes · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the bed, measured in centimeters?

- QA：GT 215 | baseline 200（对） | threeview 200（对） | threeview_3pass 200（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,6.0) | (5.0,6.0)✓ | (5.0,5.5)✓ | (5.0,6.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,3.0) | - | (5.0,3.5)✓ | (5.0,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,3.0) | - | (5.5,3.5)✓ | (6.0,3.0)✓ |


### 样本 58 `0d2ee665be`（scannetpp · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the trash can, measured in centimeters?

- QA：GT 35 | baseline 40（对） | threeview 60（对） | threeview_3pass 75（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash can | (3.0,6.0) | (9.0,8.0)✗6.3 | (4.5,6.5)✓ | (8.0,8.0)✗5.4 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash can | (3.0,1.0) | - | (4.5,3.5)✗2.9 | (8.0,2.0)✗5.1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash can | (6.0,1.0) | - | (6.5,3.5)✗2.5 | (8.0,2.0)✗2.2 |


### 样本 59 `scene0575_01`（scannet · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the trash bin, measured in centimeters?

- QA：GT 51 | baseline 40（对） | threeview 51（对） | threeview_3pass 40（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash bin | (7.0,3.0) | (5.0,8.0)✗5.4 | (4.8,5.2)✗3.1 | (3.0,8.0)✗6.4 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash bin | (7.0,1.0) | - | (4.8,3.5)✗3.3 | (3.0,2.0)✗4.1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash bin | (3.0,1.0) | - | (5.2,3.5)✗3.3 | (8.0,2.0)✗5.1 |


### 样本 60 `47332918`（arkitscenes · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the tv, measured in centimeters?

- QA：GT 144 | baseline 110（对） | threeview 85（对） | threeview_3pass 120（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| tv | (1.0,3.0) | (5.0,5.0)✗4.5 | (5.0,3.5)✗4.0 | (5.0,5.0)✗4.5 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| tv | (1.0,6.0) | - | (5.0,5.5)✗4.0 | (5.0,5.0)✗4.1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| tv | (3.0,6.0) | - | (3.5,5.5)✓ | (5.0,5.0)✗2.2 |


### 样本 61 `c5439f4607`（scannetpp · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the door, measured in centimeters?

- QA：GT 291 | baseline 200（对） | threeview 200（对） | threeview_3pass 200（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (2.0,0.0) | (1.0,5.0)✗5.1 | (1.0,5.0)✗5.1 | (1.0,5.0)✗5.1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (2.0,4.0) | - | (1.0,4.5)✓ | (1.0,4.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (0.0,4.0) | - | (5.0,4.5)✗5.0 | (5.0,4.5)✗5.0 |


### 样本 62 `scene0196_00`（scannet · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the trash bin, measured in centimeters?

- QA：GT 87 | baseline 40（错） | threeview 51（对） | threeview_3pass 50（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash bin | (7.0,1.0) | (3.0,8.0)✗8.1 | (4.8,8.1)✗7.4 | (3.0,8.0)✗8.1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash bin | (7.0,3.0) | - | (4.8,3.4)✗2.2 | (3.0,1.0)✗4.5 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash bin | (1.0,3.0) | - | (8.1,3.4)✗7.1 | (8.0,1.0)✗7.3 |


### 样本 63 `41254402`（arkitscenes · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the bed, measured in centimeters?

- QA：GT 196 | baseline 200（对） | threeview 200（对） | threeview_3pass 200（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,4.0) | (5.0,6.0)✓ | (5.0,5.5)✓ | (5.0,6.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,3.0) | - | (5.0,3.5)✓ | (5.0,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (4.0,3.0) | - | (5.5,3.5)✓ | (6.0,3.0)✓ |


### 样本 64 `09c1414f1b`（scannetpp · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the sofa, measured in centimeters?

- QA：GT 282 | baseline 210（对） | threeview 212（对） | threeview_3pass 180（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,6.0) | (5.0,6.0)✓ | (5.0,5.5)✓ | (5.0,7.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,2.0) | - | (5.0,4.0)✗2.2 | (5.0,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (6.0,2.0) | - | (5.5,4.0)✗2.1 | (7.0,3.0)✓ |


### 样本 65 `scene0164_02`（scannet · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the counter, measured in centimeters?

- QA：GT 286 | baseline 180（对） | threeview 300（对） | threeview_3pass 200（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| counter | (4.0,5.0) | (5.0,7.0)✗2.2 | (5.0,5.0)✓ | (5.0,6.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| counter | (4.0,5.0) | - | (5.0,3.5)✓ | (5.0,4.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| counter | (5.0,5.0) | - | (5.0,3.5)✓ | (6.0,4.0)✓ |


### 样本 66 `47333436`（arkitscenes · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the bed, measured in centimeters?

- QA：GT 223 | baseline 200（对） | threeview 200（对） | threeview_3pass 200（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,5.0) | (5.0,6.0)✓ | (5.0,5.5)✓ | (5.0,6.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,2.0) | - | (5.0,3.5)✓ | (5.0,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,2.0) | - | (5.5,3.5)✓ | (6.0,3.0)✓ |


### 样本 67 `0d2ee665be`（scannetpp · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the bed, measured in centimeters?

- QA：GT 231 | baseline 200（对） | threeview 216（对） | threeview_3pass 200（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (2.0,2.0) | (5.0,6.0)✗5.0 | (4.8,5.2)✗4.3 | (5.0,6.0)✗5.0 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (2.0,2.0) | - | (4.8,2.6)✗2.9 | (5.0,3.0)✗3.2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (2.0,2.0) | - | (5.2,2.6)✗3.3 | (6.0,3.0)✗4.1 |


### 样本 68 `scene0593_00`（scannet · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the backpack, measured in centimeters?

- QA：GT 54 | baseline 45（对） | threeview 40（对） | threeview_3pass 45（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (7.0,4.0) | (5.0,7.0)✗3.6 | (5.2,5.5)✗2.3 | (5.0,6.0)✗2.8 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (7.0,2.0) | - | (5.2,4.2)✗2.8 | (5.0,3.0)✗2.2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (4.0,2.0) | - | (5.5,4.2)✗2.7 | (6.0,3.0)✗2.2 |


### 样本 69 `42897629`（arkitscenes · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the stove, measured in centimeters?

- QA：GT 119 | baseline 90（对） | threeview 91（对） | threeview_3pass 90（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (7.0,7.0) | (5.0,5.0)✗2.8 | (5.0,4.5)✗3.2 | (5.0,7.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (7.0,4.0) | - | (5.0,4.0)✓ | (5.0,3.0)✗2.2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (7.0,4.0) | - | (4.5,4.0)✗2.5 | (7.0,3.0)✓ |


### 样本 70 `27dd4da69e`（scannetpp · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the pan, measured in centimeters?

- QA：GT 31 | baseline 45（对） | threeview 42（对） | threeview_3pass 45（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| pan | (2.0,5.0) | (5.0,5.0)✗3.0 | (4.8,5.2)✗2.8 | (5.0,6.0)✗3.2 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| pan | (2.0,4.0) | - | (4.8,4.5)✗2.8 | (5.0,4.0)✗3.0 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| pan | (5.0,4.0) | - | (5.2,4.5)✓ | (6.0,4.0)✓ |


### 样本 71 `scene0651_02`（scannet · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the trash bin, measured in centimeters?

- QA：GT 43 | baseline 40（对） | threeview 46（对） | threeview_3pass 50（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash bin | (1.0,6.0) | (4.0,9.0)✗4.2 | (4.8,5.2)✗3.9 | (3.0,8.0)✗2.8 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash bin | (1.0,1.0) | - | (4.8,3.5)✗4.5 | (3.0,2.0)✗2.2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| trash bin | (6.0,1.0) | - | (5.2,3.5)✗2.6 | (8.0,2.0)✗2.2 |


### 样本 72 `44358436`（arkitscenes · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the tv, measured in centimeters?

- QA：GT 44 | baseline 120（错） | threeview 72（对） | threeview_3pass 90（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| tv | (3.0,8.0) | (5.0,4.0)✗4.5 | (5.0,7.5)✗2.1 | (5.0,5.0)✗3.6 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| tv | (3.0,7.0) | - | (5.0,5.5)✗2.5 | (5.0,5.0)✗2.8 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| tv | (8.0,7.0) | - | (7.5,5.5)✓ | (5.0,5.0)✗3.6 |


### 样本 73 `f9f95681fd`（scannetpp · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the refrigerator, measured in centimeters?

- QA：GT 228 | baseline 180（对） | threeview 180（对） | threeview_3pass 180（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (4.0,1.0) | (3.0,8.0)✗7.1 | (3.5,4.5)✗3.5 | (2.0,8.0)✗7.3 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (4.0,4.0) | - | (3.5,5.0)✓ | (2.0,4.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (1.0,4.0) | - | (4.5,5.0)✗3.6 | (8.0,4.0)✗7.0 |


### 样本 74 `scene0648_00`（scannet · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the lamp, measured in centimeters?

- QA：GT 53 | baseline 60（对） | threeview 88（对） | threeview_3pass 50（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (2.0,5.0) | (3.0,8.0)✗3.2 | (4.8,5.2)✗2.8 | (4.0,5.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (2.0,5.0) | - | (4.8,4.5)✗2.8 | (4.0,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (5.0,5.0) | - | (5.2,4.5)✓ | (5.0,5.0)✓ |


### 样本 75 `41069025`（arkitscenes · object_size_estimation）

Q：What is the length of the longest dimension (length, width, or height) of the stove, measured in centimeters?

- QA：GT 62 | baseline 90（对） | threeview 60（对） | threeview_3pass 90（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (7.0,1.0) | (8.0,8.0)✗7.1 | (5.0,4.5)✗4.0 | (5.0,6.0)✗5.4 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (7.0,4.0) | - | (5.0,4.0)✓ | (5.0,3.0)✗2.2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (1.0,4.0) | - | (4.5,4.0)✗3.5 | (6.0,3.0)✗5.1 |


### 样本 76 `42899696`（arkitscenes · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 30.6 | baseline 24（对） | threeview 15（错） | threeview_3pass 12（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,4.5)多, 多1 | - |
| chair | - | (3.0,5.0)多, (4.0,6.0)多, (7.0,5.0)多, 多3 | (7.5,5.5)多, 多1 | (5.0,7.0)多, 多1 |
| desk | - | - | (7.5,7.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | (5.0,5.0)多, 多1 | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,2.5)多, 多1 | - |
| chair | - | - | (7.5,2.0)多, 多1 | (5.0,3.0)多, 多1 |
| desk | - | - | (7.5,2.5)多, 多1 | - |
| nightstand | - | - | (2.5,2.0)多, 多1 | - |
| table | - | - | - | (5.0,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (4.5,2.5)多, 多1 | - |
| chair | - | - | (5.5,2.0)多, 多1 | (7.0,3.0)多, 多1 |
| desk | - | - | (7.0,2.5)多, 多1 | - |
| nightstand | - | - | (2.5,2.0)多, 多1 | - |
| table | - | - | - | (5.0,3.0)多, 多1 |

- **baseline 问题**：多画 chair ×3（GT 0，模型 3）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×1（GT 0，模型 1）；多画 table ×1（GT 0，模型 1）

### 样本 77 `fb5a96b1a2`（scannetpp · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 34.6 | baseline 20（对） | threeview 15（错） | threeview_3pass 12（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | (3.0,5.0)多, (7.0,5.0)多, 多2 | (5.0,3.5)多, 多1 | (3.0,5.0)多, (7.0,5.0)多, 多2 |
| desk | - | - | (5.0,5.0)多, 多1 | - |
| table | - | (5.0,5.0)多, 多1 | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | (5.0,3.5)多, 多1 | (3.0,3.0)多, (7.0,3.0)多, 多2 |
| desk | - | - | (5.0,4.0)多, 多1 | - |
| table | - | - | - | (5.0,2.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | (3.5,3.5)多, 多1 | (5.0,3.0)多, (5.0,3.0)多, 多2 |
| desk | - | - | (5.0,4.0)多, 多1 | - |
| table | - | - | - | (5.0,2.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）

### 样本 78 `scene0633_00`（scannet · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 8.2 | baseline 16（对） | threeview 16（对） | threeview_3pass 12（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | (3.0,5.0)多, (7.0,5.0)多, 多2 | (3.0,5.5)多, 多1 | (5.0,5.0)多, 多1 |
| sofa | - | - | (5.0,3.0)多, 多1 | - |
| table | - | (5.0,5.0)多, 多1 | (5.0,5.5)多, 多1 | (5.0,6.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | (3.0,3.5)多, 多1 | (5.0,3.0)多, 多1 |
| sofa | - | - | (5.0,4.0)多, 多1 | - |
| table | - | - | (5.0,3.0)多, 多1 | (5.0,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | (5.5,3.5)多, 多1 | (5.0,3.0)多, 多1 |
| sofa | - | - | (3.0,4.0)多, 多1 | - |
| table | - | - | (5.5,3.0)多, 多1 | (6.0,3.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 chair ×1（GT 0，模型 1）；多画 table ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×1（GT 0，模型 1）；多画 table ×1（GT 0，模型 1）

### 样本 79 `41069048`（arkitscenes · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 7.1 | baseline 25（错） | threeview 15.0（错） | threeview_3pass 25（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | (3.0,5.0)多, (7.0,5.0)多, 多2 | (4.5,5.2)多, 多1 | (3.0,5.0)多, (8.0,4.0)多, 多2 |
| desk | - | - | (4.5,6.8)多, 多1 | - |
| sofa | - | (5.0,8.0)多, 多1 | - | (5.0,2.0)多, 多1 |
| table | - | (5.0,5.0)多, 多1 | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | (4.5,3.8)多, 多1 | (3.0,2.0)多, (8.0,2.0)多, 多2 |
| desk | - | - | (4.5,3.5)多, 多1 | - |
| sofa | - | - | - | (5.0,2.0)多, 多1 |
| table | - | - | - | (5.0,2.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | (5.2,3.8)多, 多1 | (5.0,2.0)多, (4.0,2.0)多, 多2 |
| desk | - | - | (6.8,3.5)多, 多1 | - |
| sofa | - | - | - | (2.0,2.0)多, 多1 |
| table | - | - | - | (5.0,2.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）
- **threeview 问题**：多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）

### 样本 80 `c49a8c6cff`（scannetpp · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 10.5 | baseline 25（错） | threeview 16（对） | threeview_3pass 15（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cabinet | - | (8.0,2.0)多, 多1 | - | - |
| chair | - | (3.0,5.0)多, (4.0,6.0)多, 多2 | (5.0,3.0)多, 多1 | - |
| desk | - | - | (5.0,5.0)多, 多1 | - |
| sofa | - | (2.0,3.0)多, 多1 | - | - |
| table | - | (5.0,5.0)多, 多1 | - | - |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cabinet | - | - | - | - |
| chair | - | - | (5.0,3.5)多, 多1 | - |
| desk | - | - | (5.0,4.0)多, 多1 | - |
| sofa | - | - | - | - |
| table | - | - | - | - |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cabinet | - | - | - | - |
| chair | - | - | (3.0,3.5)多, 多1 | - |
| desk | - | - | (5.0,4.0)多, 多1 | - |
| sofa | - | - | - | - |
| table | - | - | - | - |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）；多画 cabinet ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）
- **threeview 问题**：多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）

### 样本 81 `scene0378_01`（scannet · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 12.3 | baseline 25（错） | threeview 16.0（对） | threeview_3pass 9（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | (3.0,5.0)多, (7.0,6.0)多, 多2 | (4.5,5.0)多, 多1 | (3.0,5.0)多, (7.0,5.0)多, 多2 |
| desk | - | - | (4.5,6.5)多, 多1 | - |
| table | - | (5.0,5.0)多, 多1 | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | (4.5,4.0)多, 多1 | (3.0,3.0)多, (7.0,3.0)多, 多2 |
| desk | - | - | (4.5,4.5)多, 多1 | - |
| table | - | - | - | (5.0,2.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | (5.0,4.0)多, 多1 | (5.0,3.0)多, (5.0,3.0)多, 多2 |
| desk | - | - | (6.5,4.5)多, 多1 | - |
| table | - | - | - | (5.0,2.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）

### 样本 82 `42446116`（arkitscenes · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 14.8 | baseline 20（对） | threeview 15（对） | threeview_3pass 15（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,4.5)多, 多1 | - |
| chair | - | (3.0,5.0)多, (7.0,5.0)多, 多2 | (7.5,5.5)多, 多1 | - |
| desk | - | - | (7.5,7.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | (5.0,5.0)多, 多1 | - | - |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.0)多, 多1 | - |
| chair | - | - | (7.5,2.5)多, 多1 | - |
| desk | - | - | (7.5,3.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | - | - | - |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (4.5,3.0)多, 多1 | - |
| chair | - | - | (5.5,2.5)多, 多1 | - |
| desk | - | - | (7.0,3.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | - | - | - |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）

### 样本 83 `99fa5c25e1`（scannetpp · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 27.2 | baseline 25（对） | threeview 15（对） | threeview_3pass 16（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cabinet | - | - | - | (1.0,2.0)多, 多1 |
| chair | - | (3.0,5.0)多, (8.0,5.0)多, 多2 | (5.0,3.5)多, 多1 | (5.0,6.0)多, (6.0,7.0)多, 多2 |
| desk | - | - | (5.0,5.5)多, 多1 | - |
| sofa | - | - | - | (3.0,4.0)多, 多1 |
| table | - | (5.0,5.0)多, 多1 | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cabinet | - | - | - | (1.0,4.0)多, 多1 |
| chair | - | - | (5.0,3.0)多, 多1 | (5.0,2.0)多, (6.0,2.0)多, 多2 |
| desk | - | - | (5.0,3.5)多, 多1 | - |
| sofa | - | - | - | (3.0,2.0)多, 多1 |
| table | - | - | - | (5.0,2.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cabinet | - | - | - | (2.0,4.0)多, 多1 |
| chair | - | - | (3.5,3.0)多, 多1 | (6.0,2.0)多, (7.0,2.0)多, 多2 |
| desk | - | - | (5.5,3.5)多, 多1 | - |
| sofa | - | - | - | (4.0,2.0)多, 多1 |
| table | - | - | - | (5.0,2.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）；多画 cabinet ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）

### 样本 84 `scene0222_01`（scannet · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 17.5 | baseline 15（对） | threeview 15.0（对） | threeview_3pass 12（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,4.0)多, 多1 | - |
| chair | - | (5.0,6.0)多, 多1 | (7.0,6.0)多, 多1 | (4.0,5.0)多, (7.0,6.0)多, 多2 |
| desk | - | - | (8.0,6.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.0)多, 多1 | - |
| table | - | (4.0,5.0)多, 多1 | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.0)多, 多1 | - |
| chair | - | - | (7.0,3.0)多, 多1 | (4.0,2.0)多, (7.0,2.0)多, 多2 |
| desk | - | - | (8.0,3.5)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | - | - | (5.0,2.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (4.0,3.0)多, 多1 | - |
| chair | - | - | (6.0,3.0)多, 多1 | (5.0,2.0)多, (6.0,2.0)多, 多2 |
| desk | - | - | (6.0,3.5)多, 多1 | - |
| nightstand | - | - | (2.0,2.5)多, 多1 | - |
| table | - | - | - | (5.0,2.0)多, 多1 |

- **baseline 问题**：多画 chair ×1（GT 0，模型 1）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）

### 样本 85 `47332901`（arkitscenes · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 11.2 | baseline 25（错） | threeview 15（对） | threeview_3pass 12（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | (3.0,5.0)多, (7.0,5.0)多, 多2 | (5.0,3.0)多, 多1 | (3.0,5.0)多, (7.0,5.0)多, 多2 |
| desk | - | - | (5.0,5.0)多, 多1 | - |
| table | - | (5.0,5.0)多, 多1 | - | (5.0,6.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | (5.0,3.0)多, 多1 | (3.0,3.0)多, (7.0,3.0)多, 多2 |
| desk | - | - | (5.0,4.0)多, 多1 | - |
| table | - | - | - | (5.0,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | (3.0,3.0)多, 多1 | (5.0,3.0)多, (5.0,3.0)多, 多2 |
| desk | - | - | (5.0,4.0)多, 多1 | - |
| table | - | - | - | (6.0,3.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）

### 样本 86 `ac48a9b736`（scannetpp · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 128.5 | baseline 12（错） | threeview 15（错） | threeview_3pass 10（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,4.5)多, 多1 | - |
| chair | - | (4.0,6.0)多, (7.0,6.0)多, 多2 | (7.5,5.5)多, 多1 | (5.0,7.0)多, 多1 |
| desk | - | (5.0,5.0)多, 多1 | (7.5,7.0)多, 多1 | - |
| monitor | - | - | - | (5.0,4.0)多, 多1 |
| nightstand | - | - | (2.5,3.0)多, 多1 | - |
| table | - | - | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,2.5)多, 多1 | - |
| chair | - | - | (7.5,2.0)多, 多1 | (5.0,2.0)多, 多1 |
| desk | - | - | (7.5,2.5)多, 多1 | - |
| monitor | - | - | - | (5.0,5.0)多, 多1 |
| nightstand | - | - | (2.5,2.0)多, 多1 | - |
| table | - | - | - | (5.0,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (4.5,2.5)多, 多1 | - |
| chair | - | - | (5.5,2.0)多, 多1 | (7.0,2.0)多, 多1 |
| desk | - | - | (7.0,2.5)多, 多1 | - |
| monitor | - | - | - | (4.0,5.0)多, 多1 |
| nightstand | - | - | (3.0,2.0)多, 多1 | - |
| table | - | - | - | (5.0,3.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 desk ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×1（GT 0，模型 1）；多画 table ×1（GT 0，模型 1）；多画 monitor ×1（GT 0，模型 1）

### 样本 87 `scene0095_01`（scannet · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 24.7 | baseline 20（对） | threeview 15.0（对） | threeview_3pass 9（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,4.5)多, 多1 | - |
| chair | - | (4.0,5.0)多, (6.0,5.0)多, 多2 | (7.5,5.5)多, 多1 | (4.0,5.0)多, (6.0,5.0)多, 多2 |
| desk | - | - | (7.5,7.5)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | (5.0,5.0)多, 多1 | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.0)多, 多1 | - |
| chair | - | - | (7.5,2.5)多, 多1 | (4.0,3.0)多, (6.0,3.0)多, 多2 |
| desk | - | - | (7.5,3.5)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | - | - | (5.0,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (4.5,3.0)多, 多1 | - |
| chair | - | - | (5.5,2.5)多, 多1 | (5.0,3.0)多, (5.0,3.0)多, 多2 |
| desk | - | - | (7.5,3.5)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | - | - | (5.0,3.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）

### 样本 88 `47333932`（arkitscenes · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 17.7 | baseline 20（对） | threeview 15（对） | threeview_3pass 25（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (7.5,4.0)多, 多1 | - |
| chair | - | - | (4.5,5.5)多, 多1 | (4.0,5.0)多, (5.0,6.0)多, 多2 |
| desk | - | - | (4.5,7.0)多, 多1 | - |
| sofa | - | - | - | (3.0,2.0)多, 多1 |
| table | - | - | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (7.5,3.0)多, 多1 | - |
| chair | - | - | (4.5,4.0)多, 多1 | (4.0,2.0)多, (5.0,2.0)多, 多2 |
| desk | - | - | (4.5,4.2)多, 多1 | - |
| sofa | - | - | - | (3.0,2.0)多, 多1 |
| table | - | - | - | (5.0,2.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (4.0,3.0)多, 多1 | - |
| chair | - | - | (5.5,4.0)多, 多1 | (5.0,2.0)多, (6.0,2.0)多, 多2 |
| desk | - | - | (7.0,4.2)多, 多1 | - |
| sofa | - | - | - | (2.0,2.0)多, 多1 |
| table | - | - | - | (5.0,2.0)多, 多1 |

- **threeview 问题**：多画 chair ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）

### 样本 89 `5eb31827b7`（scannetpp · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 14.2 | baseline 16（对） | threeview 15.0（对） | threeview_3pass 10（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cabinet | - | - | (2.0,7.5)多, 多1 | - |
| chair | - | (3.0,5.0)多, (7.0,5.0)多, 多2 | (5.0,4.8)多, 多1 | (5.0,3.0)多, 多1 |
| desk | - | - | (5.0,6.5)多, 多1 | (5.0,5.0)多, 多1 |
| table | - | (5.0,5.0)多, 多1 | - | - |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cabinet | - | - | (2.0,5.0)多, 多1 | - |
| chair | - | - | (5.0,3.5)多, 多1 | (5.0,2.0)多, 多1 |
| desk | - | - | (5.0,4.0)多, 多1 | (5.0,2.0)多, 多1 |
| table | - | - | - | - |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cabinet | - | - | (7.5,5.0)多, 多1 | - |
| chair | - | - | (4.8,3.5)多, 多1 | (3.0,2.0)多, 多1 |
| desk | - | - | (6.5,4.0)多, 多1 | (5.0,2.0)多, 多1 |
| table | - | - | - | - |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 chair ×1（GT 0，模型 1）；多画 cabinet ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）

### 样本 90 `scene0565_00`（scannet · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 22.2 | baseline 25（对） | threeview 15（对） | threeview_3pass 12（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,4.5)多, 多1 | - |
| cabinet | - | (2.0,8.0)多, (8.0,8.0)多, 多2 | - | - |
| chair | - | (3.0,5.0)多, (7.0,5.0)多, 多2 | (7.5,5.0)多, 多1 | (3.0,5.0)多, (7.0,5.0)多, 多2 |
| desk | - | - | (7.5,7.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| sofa | - | (5.0,2.0)多, 多1 | - | - |
| table | - | (5.0,5.0)多, 多1 | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.5)多, 多1 | - |
| cabinet | - | - | - | - |
| chair | - | - | (7.5,3.0)多, 多1 | (3.0,3.0)多, (7.0,3.0)多, 多2 |
| desk | - | - | (7.5,3.5)多, 多1 | - |
| nightstand | - | - | (2.5,3.0)多, 多1 | - |
| sofa | - | - | - | - |
| table | - | - | - | (5.0,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (4.5,3.5)多, 多1 | - |
| cabinet | - | - | - | - |
| chair | - | - | (5.0,3.0)多, 多1 | (5.0,3.0)多, (5.0,3.0)多, 多2 |
| desk | - | - | (7.0,3.5)多, 多1 | - |
| nightstand | - | - | (2.5,3.0)多, 多1 | - |
| sofa | - | - | - | - |
| table | - | - | - | (5.0,3.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）；多画 cabinet ×2（GT 0，模型 2）；多画 sofa ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）

### 样本 91 `41159555`（arkitscenes · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 28.4 | baseline 20（对） | threeview 16.0（对） | threeview_3pass 12（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,4.5)多, 多1 | - |
| chair | - | (3.0,5.0)多, (7.0,5.0)多, 多2 | (7.5,5.5)多, 多1 | (5.0,5.0)多, 多1 |
| desk | - | - | (7.5,7.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | (5.0,5.0)多, 多1 | - | (5.0,6.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.0)多, 多1 | - |
| chair | - | - | (7.5,2.5)多, 多1 | (5.0,3.0)多, 多1 |
| desk | - | - | (7.5,3.5)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | - | - | (5.0,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (4.5,3.0)多, 多1 | - |
| chair | - | - | (5.5,2.5)多, 多1 | (5.0,3.0)多, 多1 |
| desk | - | - | (7.0,3.5)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | - | - | (6.0,3.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×1（GT 0，模型 1）；多画 table ×1（GT 0，模型 1）

### 样本 92 `f3685d06a9`（scannetpp · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 6.2 | baseline 20（错） | threeview 15（错） | threeview_3pass 20（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,5.0)多, 多1 | - |
| chair | - | (3.0,5.0)多, (7.0,5.0)多, 多2 | - | (3.0,5.0)多, (7.0,5.0)多, 多2 |
| nightstand | - | - | (3.0,3.0)多, 多1 | - |
| sofa | - | - | - | (5.0,4.0)多, 多1 |
| table | - | (5.0,5.0)多, 多1 | - | (5.0,7.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.0)多, 多1 | - |
| chair | - | - | - | (3.0,2.0)多, (7.0,2.0)多, 多2 |
| nightstand | - | - | (3.0,2.0)多, 多1 | - |
| sofa | - | - | - | (5.0,2.0)多, 多1 |
| table | - | - | - | (5.0,2.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.0)多, 多1 | - |
| chair | - | - | - | (5.0,2.0)多, (5.0,2.0)多, 多2 |
| nightstand | - | - | (3.0,2.0)多, 多1 | - |
| sofa | - | - | - | (4.0,2.0)多, 多1 |
| table | - | - | - | (7.0,2.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）

### 样本 93 `scene0088_01`（scannet · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 18.7 | baseline 25（对） | threeview 15.5（对） | threeview_3pass 16（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,4.5)多, 多1 | - |
| cabinet | - | (1.0,2.0)多, 多1 | - | - |
| chair | - | (3.0,5.0)多, (7.0,5.0)多, 多2 | (7.5,6.5)多, 多1 | (3.0,5.0)多, (7.0,5.0)多, 多2 |
| desk | - | - | (7.5,8.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| sofa | - | (5.0,8.0)多, 多1 | - | - |
| table | - | (5.0,5.0)多, 多1 | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.0)多, 多1 | - |
| cabinet | - | - | - | - |
| chair | - | - | (7.5,2.5)多, 多1 | (3.0,2.0)多, (7.0,2.0)多, 多2 |
| desk | - | - | (7.5,3.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| sofa | - | - | - | - |
| table | - | - | - | (5.0,2.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (4.5,3.0)多, 多1 | - |
| cabinet | - | - | - | - |
| chair | - | - | (6.5,2.5)多, 多1 | (5.0,2.0)多, (5.0,2.0)多, 多2 |
| desk | - | - | (8.0,3.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| sofa | - | - | - | - |
| table | - | - | - | (5.0,2.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）；多画 cabinet ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）

### 样本 94 `42445981`（arkitscenes · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 19.9 | baseline 12（对） | threeview 18.5（对） | threeview_3pass 20（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,4.5)多, 多1 | - |
| chair | - | (5.0,7.0)多, 多1 | (7.5,6.0)多, 多1 | - |
| desk | - | (5.0,5.0)多, 多1 | (7.5,7.5)多, 多1 | - |
| keyboard | - | (5.0,6.0)多, 多1 | - | - |
| monitor | - | (5.0,4.0)多, 多1 | - | - |
| mouse | - | (6.0,6.0)多, 多1 | - | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.0)多, 多1 | - |
| chair | - | - | (7.5,3.0)多, 多1 | - |
| desk | - | - | (7.5,3.5)多, 多1 | - |
| keyboard | - | - | - | - |
| monitor | - | - | - | - |
| mouse | - | - | - | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (4.5,3.0)多, 多1 | - |
| chair | - | - | (6.0,3.0)多, 多1 | - |
| desk | - | - | (7.5,3.5)多, 多1 | - |
| keyboard | - | - | - | - |
| monitor | - | - | - | - |
| mouse | - | - | - | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |

- **baseline 问题**：多画 keyboard ×1（GT 0，模型 1）；多画 monitor ×1（GT 0，模型 1）；多画 mouse ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）

### 样本 95 `38d58a7a31`（scannetpp · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 52.3 | baseline 15（错） | threeview 30（对） | threeview_3pass 12（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | (5.0,6.0)多, 多1 | - | (3.0,5.0)多, (7.0,5.0)多, 多2 |
| sofa | - | - | - | (5.0,2.0)多, 多1 |
| table | - | (5.0,4.0)多, 多1 | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | - | (3.0,2.0)多, (7.0,2.0)多, 多2 |
| sofa | - | - | - | (5.0,2.0)多, 多1 |
| table | - | - | - | (5.0,1.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | - | (5.0,2.0)多, (5.0,2.0)多, 多2 |
| sofa | - | - | - | (2.0,2.0)多, 多1 |
| table | - | - | - | (5.0,1.0)多, 多1 |

- **baseline 问题**：多画 chair ×1（GT 0，模型 1）；多画 table ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）

### 样本 96 `scene0462_00`（scannet · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 13.9 | baseline 16（对） | threeview 15.0（对） | threeview_3pass 12（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,5.0)多, 多1 | - |
| chair | - | (4.0,5.0)多, (6.0,5.0)多, 多2 | (7.5,5.0)多, 多1 | (3.0,5.0)多, (7.0,5.0)多, 多2 |
| desk | - | - | (7.5,6.5)多, 多1 | - |
| nightstand | - | - | (2.5,3.5)多, 多1 | - |
| table | - | (5.0,6.0)多, 多1 | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.5)多, 多1 | - |
| chair | - | - | (7.5,3.0)多, 多1 | (3.0,2.0)多, (7.0,2.0)多, 多2 |
| desk | - | - | (7.5,3.5)多, 多1 | - |
| nightstand | - | - | (2.5,3.0)多, 多1 | - |
| table | - | - | - | (5.0,2.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.5)多, 多1 | - |
| chair | - | - | (5.0,3.0)多, 多1 | (5.0,2.0)多, (5.0,2.0)多, 多2 |
| desk | - | - | (6.5,3.5)多, 多1 | - |
| nightstand | - | - | (3.5,3.0)多, 多1 | - |
| table | - | - | - | (5.0,2.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）

### 样本 97 `45261575`（arkitscenes · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 13.8 | baseline 20（对） | threeview 15.0（对） | threeview_3pass 9（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,4.5)多, 多1 | - |
| chair | - | - | (7.5,7.0)多, 多1 | (3.0,5.0)多, (7.0,5.0)多, 多2 |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | - | - | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.0)多, 多1 | - |
| chair | - | - | (7.5,2.5)多, 多1 | (3.0,3.0)多, (7.0,3.0)多, 多2 |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | - | - | (5.0,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (4.5,3.0)多, 多1 | - |
| chair | - | - | (7.0,2.5)多, 多1 | (5.0,3.0)多, (5.0,3.0)多, 多2 |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| table | - | - | - | (5.0,3.0)多, 多1 |

- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）

### 样本 98 `9071e139d9`（scannetpp · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 42.8 | baseline 25（对） | threeview 25（对） | threeview_3pass 25（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | (3.0,5.0)多, (7.0,5.0)多, 多2 | (2.5,6.0)多, 多1 | (3.0,7.0)多, (7.0,7.0)多, 多2 |
| sofa | - | (5.0,2.0)多, 多1 | (5.0,3.5)多, 多1 | (5.0,3.0)多, 多1 |
| table | - | (5.0,5.0)多, 多1 | (5.0,6.0)多, 多1 | (5.0,7.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | (2.5,3.5)多, 多1 | (3.0,3.0)多, (7.0,3.0)多, 多2 |
| sofa | - | - | (5.0,4.0)多, 多1 | (5.0,3.0)多, 多1 |
| table | - | - | (5.0,3.0)多, 多1 | (5.0,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | - | - | (6.0,3.5)多, 多1 | (7.0,3.0)多, (7.0,3.0)多, 多2 |
| sofa | - | - | (3.5,4.0)多, 多1 | (3.0,3.0)多, 多1 |
| table | - | - | (6.0,3.0)多, 多1 | (7.0,3.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）
- **threeview 问题**：多画 chair ×1（GT 0，模型 1）；多画 table ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）

### 样本 99 `scene0663_00`（scannet · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 14.1 | baseline 16（对） | threeview 15.0（对） | threeview_3pass 16（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,4.5)多, 多1 | - |
| chair | - | (4.0,5.0)多, (6.0,5.0)多, 多2 | (7.5,6.5)多, 多1 | (3.0,7.0)多, (7.0,7.0)多, 多2 |
| desk | - | - | (7.5,8.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| sofa | - | - | - | (5.0,3.0)多, 多1 |
| table | - | (5.0,6.0)多, 多1 | - | (5.0,7.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.0)多, 多1 | - |
| chair | - | - | (7.5,2.5)多, 多1 | (3.0,3.0)多, (7.0,3.0)多, 多2 |
| desk | - | - | (7.5,3.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| sofa | - | - | - | (5.0,3.0)多, 多1 |
| table | - | - | - | (5.0,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (4.5,3.0)多, 多1 | - |
| chair | - | - | (6.5,2.5)多, 多1 | (7.0,3.0)多, (7.0,3.0)多, 多2 |
| desk | - | - | (8.0,3.0)多, 多1 | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| sofa | - | - | - | (3.0,3.0)多, 多1 |
| table | - | - | - | (7.0,3.0)多, 多1 |

- **baseline 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）

### 样本 100 `47332908`（arkitscenes · room_size_estimation）

Q：What is the size of this room (in square meters)? 
If multiple rooms are shown, estimate the size of the combined space.

- QA：GT 10.4 | baseline 30（错） | threeview 16.0（对） | threeview_3pass 12（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,5.0)多, 多1 | - |
| cabinet | - | (8.0,2.0)多, 多1 | - | - |
| chair | - | (3.0,5.0)多, (4.0,6.0)多, 多2 | (7.5,6.5)多, 多1 | (5.0,5.0)多, 多1 |
| desk | - | - | (7.5,8.0)多, 多1 | - |
| door | - | (9.0,8.0)多, 多1 | - | - |
| nightstand | - | - | (2.5,3.5)多, 多1 | - |
| sofa | - | (2.0,3.0)多, 多1 | - | - |
| table | - | (5.0,5.0)多, 多1 | - | (5.0,4.0)多, 多1 |
| window | - | (1.0,5.0)多, 多1 | - | - |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.0)多, 多1 | - |
| cabinet | - | - | - | - |
| chair | - | - | (7.5,2.5)多, 多1 | (5.0,3.0)多, 多1 |
| desk | - | - | (7.5,3.0)多, 多1 | - |
| door | - | - | - | - |
| nightstand | - | - | (2.5,2.5)多, 多1 | - |
| sofa | - | - | - | - |
| table | - | - | - | (5.0,3.0)多, 多1 |
| window | - | - | - | - |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | - | - | (5.0,3.0)多, 多1 | - |
| cabinet | - | - | - | - |
| chair | - | - | (6.5,2.5)多, 多1 | (5.0,3.0)多, 多1 |
| desk | - | - | (8.0,3.0)多, 多1 | - |
| door | - | - | - | - |
| nightstand | - | - | (3.5,2.5)多, 多1 | - |
| sofa | - | - | - | - |
| table | - | - | - | (4.0,3.0)多, 多1 |
| window | - | - | - | - |

- **baseline 问题**：多画 window ×1（GT 0，模型 1）；多画 cabinet ×1（GT 0，模型 1）；多画 sofa ×1（GT 0，模型 1）；多画 door ×1（GT 0，模型 1）；多画 chair ×2（GT 0，模型 2）；多画 table ×1（GT 0，模型 1）
- **threeview 问题**：多画 nightstand ×1（GT 0，模型 1）；多画 bed ×1（GT 0，模型 1）；多画 desk ×1（GT 0，模型 1）；多画 chair ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 chair ×1（GT 0，模型 1）；多画 table ×1（GT 0，模型 1）

### 样本 101 `45261121`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (stool, tv, table, refrigerator) is the closest to the stove?

- QA：GT C | baseline D（错） | threeview C（对） | threeview_3pass D（错）
- 对齐：baseline: yaw=-57° mirror=否 平移=(-2.0,5.4) RMSE=1.07；threeview: yaw=-85° mirror=是(证据支持) 平移=(9.8,9.5) RMSE=0.75；threeview_3pass: yaw=-83° mirror=是(未证实) 平移=(9.1,9.0) RMSE=0.85
- 补偿：baseline: 尺度=0.98 z偏移=+0.00；threeview: 尺度=1.01 z偏移=-0.30；threeview_3pass: 尺度=0.95 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (1.0,7.0) | (1.6,5.3)✓ | (2.0,6.9)✓ | (1.6,5.9)✓ |
| stool | (7.0,2.0) | (7.6,3.3)✓, (6.5,4.9)多, 多1 | (6.3,3.2)✓, (6.2,5.2)多, 多1 | (5.8,2.6)✓, (5.6,4.5)多, 多1 |
| stove | (3.0,2.0) | (1.9,3.1)✓ | (2.5,0.8)✓ | (1.9,3.1)✓ |
| table | (5.0,4.0) | (6.2,3.6)✓ | (5.2,4.1)✓ | (5.7,3.5)✓ |
| tv | (7.0,1.0) | (5.6,0.9)✓ | 漏1 | (7.9,0.9)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (1.0,3.0) | - | (2.0,2.8)✓ | (1.6,4.0)✓ |
| stool | (7.0,1.0) | - | (6.3,1.7)✓, (6.2,1.7)多, 多1 | (5.8,2.0)✓, (5.6,2.0)多, 多1 |
| stove | (3.0,3.0) | - | (2.5,2.3)✓ | (1.9,2.0)✓ |
| table | (5.0,2.0) | - | (5.2,2.2)✓ | (5.7,2.0)✓ |
| tv | (7.0,7.0) | - | 漏1 | (7.9,4.0)✗3.1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (7.0,3.0) | - | (6.9,2.8)✓ | (5.9,4.0)✓ |
| stool | (2.0,1.0) | - | (3.2,1.7)✓, (5.2,1.7)多, 多1 | (2.6,2.0)✓, (4.5,2.0)多, 多1 |
| stove | (2.0,3.0) | - | (0.8,2.3)✓ | (3.1,2.0)✓ |
| table | (4.0,2.0) | - | (4.1,2.2)✓ | (3.5,2.0)✓ |
| tv | (1.0,7.0) | - | 漏1 | (0.9,4.0)✗3.0 |

- **baseline 问题**：多画 stool ×1（GT 1，模型 2）；refrigerator-stool 距离画错（GT 7.8，模型 5.0）；refrigerator→stool 方向错（GT NW，模型 W）；refrigerator-stove 距离画错（GT 5.4，模型 2.2）；refrigerator→table 方向错（GT NW，模型 W）；refrigerator-tv 距离画错（GT 8.5，模型 6.1）；stool-stove 距离画错（GT 4.0，模型 5.1）；stool-table 距离画错（GT 2.8，模型 1.4）
- **threeview 问题**：多画 stool ×1（GT 1，模型 2）；漏画 tv ×1（GT 1，模型 0）；refrigerator-stool 距离画错（GT 7.8，模型 4.5）；stool→stove 方向错（GT E，模型 NE）；stool-table 距离画错（GT 2.8，模型 1.4）；stool→table 方向错（GT SE，模型 E）；stove-table 距离画错（GT 2.8，模型 4.2）
- **threeview_3pass 问题**：多画 stool ×1（GT 1，模型 2）；refrigerator-stool 距离画错（GT 7.8，模型 4.5）；refrigerator-stove 距离画错（GT 5.4，模型 3.0）；stool-table 距离画错（GT 2.8，模型 1.0）；stool→table 方向错（GT SE，模型 E）；stool-tv 距离画错（GT 1.0，模型 2.8）；stool→tv 方向错（GT N，模型 NW）；stove-table 距离画错（GT 2.8，模型 4.0）

### 样本 102 `acd95847c5`（scannetpp · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (laptop, power strip, computer tower, heater) is the closest to the door?

- QA：GT B | baseline C（错） | threeview C（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=20° mirror=是(未证实) 平移=(-2.0,10.3) RMSE=1.62；threeview: yaw=25° mirror=否 平移=(1.9,-1.1) RMSE=1.66；threeview_3pass: yaw=-105° mirror=否 平移=(-1.4,11.6) RMSE=2.71
- 补偿：baseline: 尺度=0.89 z偏移=+0.00；threeview: 尺度=0.79 z偏移=-2.00；threeview_3pass: 尺度=0.32 z偏移=-2.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer tower | (7.0,3.0), (5.0,6.0) | (3.3,4.8)✗2.1, 漏1 | (3.5,4.3)✗2.3, 漏1 | (3.6,4.3)✗2.2, 漏1 |
| door | (0.0,6.0) | (1.0,5.9)✓ | (0.1,6.6)✓ | (3.3,6.7)✗3.4 |
| heater | (7.0,7.0), (8.0,1.0) | (7.7,5.5)✓, 漏1 | (6.7,6.7)✓, 漏1 | (4.5,6.1)✗2.7, 漏1 |
| laptop | (6.0,6.0) | (3.5,6.8)✗2.6 | (4.4,5.1)✓ | (3.3,5.4)✗2.8 |
| power strip | (1.0,2.0), (1.0,1.0) | (3.6,4.0)✗3.2, 漏1 | (4.3,4.3)✗4.0, 漏1 | (4.3,4.5)✗4.1, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer tower | (7.0,1.0), (5.0,1.0) | - | (3.5,1.0)✓, 漏1 | (3.6,1.0)✓, 漏1 |
| door | (0.0,3.0) | - | (0.1,3.0)✓ | (3.3,3.0)✗3.3 |
| heater | (7.0,1.0), (8.0,1.0) | - | (6.7,0.5)✓, 漏1 | (4.5,0.0)✗2.7, 漏1 |
| laptop | (6.0,2.0) | - | (4.4,2.0)✓ | (3.3,3.0)✗2.9 |
| power strip | (1.0,2.0), (1.0,2.0) | - | (4.3,0.0)✗3.9, 漏1 | (4.3,-1.0)✗4.5, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer tower | (3.0,1.0), (6.0,1.0) | - | (4.3,1.0)✓, 漏1 | (4.3,1.0)✓, 漏1 |
| door | (6.0,3.0) | - | (6.6,3.0)✓ | (6.7,3.0)✓ |
| heater | (7.0,1.0), (1.0,1.0) | - | (6.7,0.5)✓, 漏1 | (6.1,0.0)✓, 漏1 |
| laptop | (6.0,2.0) | - | (5.1,2.0)✓ | (5.4,3.0)✓ |
| power strip | (2.0,2.0), (1.0,2.0) | - | (4.3,0.0)✗3.0, 漏1 | (4.5,-1.0)✗3.9, 漏1 |

- **baseline 问题**：漏画 heater ×1（GT 2，模型 1）；漏画 power strip ×1（GT 2，模型 1）；漏画 computer tower ×1（GT 2，模型 1）；computer tower-door 距离画错（GT 5.0，模型 2.8）；computer tower→door 方向错（GT E，模型 SE）；computer tower-heater 距离画错（GT 2.2，模型 5.1）；computer tower-laptop 距离画错（GT 1.0，模型 2.2）；computer tower-power strip 距离画错（GT 5.7，模型 1.0）
- **threeview 问题**：漏画 heater ×1（GT 2，模型 1）；漏画 power strip ×1（GT 2，模型 1）；漏画 computer tower ×1（GT 2，模型 1）；computer tower→door 方向错（GT E，模型 SE）；computer tower-heater 距离画错（GT 2.2，模型 5.1）；computer tower→heater 方向错（GT W，模型 SW）；computer tower→laptop 方向错（GT S，模型 SW）；computer tower-power strip 距离画错（GT 5.7，模型 1.1）
- **threeview_3pass 问题**：漏画 heater ×1（GT 2，模型 1）；漏画 power strip ×1（GT 2，模型 1）；漏画 computer tower ×1（GT 2，模型 1）；computer tower-door 距离画错（GT 5.0，模型 7.6）；computer tower→door 方向错（GT E，模型 S）；computer tower-heater 距离画错（GT 2.2，模型 6.1）；computer tower→heater 方向错（GT W，模型 SW）；computer tower-laptop 距离画错（GT 1.0，模型 3.6）

### 样本 103 `scene0700_02`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (window, trash bin, table, radiator) is the closest to the door?

- QA：GT B | baseline B（对） | threeview C（错） | threeview_3pass C（错）
- 对齐：baseline: yaw=-33° mirror=否 平移=(-1.7,0.6) RMSE=1.16；threeview: yaw=149° mirror=是(未证实) 平移=(5.2,-3.5) RMSE=1.44；threeview_3pass: yaw=-32° mirror=否 平移=(-1.5,0.4) RMSE=1.11
- 补偿：baseline: 尺度=0.76 z偏移=+0.00；threeview: 尺度=0.62 z偏移=-1.00；threeview_3pass: 尺度=0.83 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,2.0) | (1.2,2.1)✓ | (0.7,2.3)✓ | (1.1,1.9)✓ |
| radiator | (7.0,4.0) | (6.7,5.0)✓ | (6.8,4.1)✓ | (6.6,4.3)✓ |
| table | (5.0,5.0) | (5.0,2.4)✗2.6 | (3.8,3.3)✗2.0 | (4.5,2.7)✗2.4 |
| trash bin | (3.0,1.0), (3.0,1.0) | (3.3,2.6)✓, 漏1 | (4.5,2.6)✗2.2, 漏1 | (3.8,3.1)✗2.3, 漏1 |
| window | (7.0,5.0) | (6.7,5.0)✓ | (7.1,4.6)✓ | (7.0,5.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,4.0) | - | (0.7,3.5)✓ | (1.1,4.0)✓ |
| radiator | (7.0,2.0) | - | (6.8,2.0)✓ | (6.6,2.0)✓ |
| table | (5.0,2.0) | - | (3.8,2.5)✓ | (4.5,2.0)✓ |
| trash bin | (3.0,1.0), (3.0,1.0) | - | (4.5,1.0)✓, 漏1 | (3.8,1.0)✓, 漏1 |
| window | (7.0,5.0) | - | (7.1,5.0)✓ | (7.0,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (2.0,4.0) | - | (2.3,3.5)✓ | (1.9,4.0)✓ |
| radiator | (4.0,2.0) | - | (4.1,2.0)✓ | (4.3,2.0)✓ |
| table | (5.0,2.0) | - | (3.3,2.5)✓ | (2.7,2.0)✗2.3 |
| trash bin | (1.0,1.0), (1.0,1.0) | - | (2.6,1.0)✓, 漏1 | (3.1,1.0)✗2.1, 漏1 |
| window | (5.0,5.0) | - | (4.6,5.0)✓ | (5.0,6.0)✓ |

- **baseline 问题**：漏画 trash bin ×1（GT 2，模型 1）；door-radiator 距离画错（GT 6.3，模型 8.1）；door→radiator 方向错（GT W，模型 SW）；door→table 方向错（GT SW，模型 W）；door→trash bin 方向错（GT NW，模型 W）；door-window 距离画错（GT 6.7，模型 8.1）；radiator-table 距离画错（GT 2.2，模型 4.0）；radiator→table 方向错（GT SE，模型 NE）
- **threeview 问题**：漏画 trash bin ×1（GT 2，模型 1）；door-radiator 距离画错（GT 6.3，模型 10.3）；door→table 方向错（GT SW，模型 W）；door-trash bin 距离画错（GT 2.2，模型 6.1）；door→trash bin 方向错（GT NW，模型 W）；door-window 距离画错（GT 6.7，模型 11.0）；door→window 方向错（GT SW，模型 W）；radiator-table 距离画错（GT 2.2，模型 4.9）
- **threeview_3pass 问题**：漏画 trash bin ×1（GT 2，模型 1）；door→radiator 方向错（GT W，模型 SW）；door→table 方向错（GT SW，模型 W）；door-trash bin 距离画错（GT 2.2，模型 3.6）；door→trash bin 方向错（GT NW，模型 SW）；door-window 距离画错（GT 6.7，模型 8.1）；radiator→table 方向错（GT SE，模型 NE）；radiator-trash bin 距离画错（GT 5.0，模型 3.6）

### 样本 104 `47429977`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (stove, tv, sofa, chair) is the closest to the refrigerator?

- QA：GT A | baseline A（对） | threeview A（对） | threeview_3pass A（对）
- 对齐：baseline: yaw=-7° mirror=是(证据支持) 平移=(2.0,7.8) RMSE=0.92；threeview: yaw=-11° mirror=是(证据支持) 平移=(2.2,8.9) RMSE=0.68；threeview_3pass: yaw=-95° mirror=否 平移=(0.7,7.1) RMSE=1.73
- 补偿：baseline: 尺度=0.67 z偏移=+0.00；threeview: 尺度=0.91 z偏移=+2.00；threeview_3pass: 尺度=0.65 z偏移=+1.00
- 跨视图未匹配：threeview_3pass: side 未匹配×1

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,1.0), (3.0,2.0), (3.0,1.0) | (4.0,2.5)✓, 漏2 | (4.1,2.4)✓, 漏2 | (4.0,0.9)✓, (4.2,3.5)✓, 漏1 |
| refrigerator | (2.0,7.0) | 漏1 | 漏1 | (2.4,5.0)✗2.1 |
| sofa | (6.0,6.0), (7.0,4.0) | (6.2,4.2)✓, 漏1 | (6.3,4.3)✓, 漏1 | (3.4,2.3)✗3.9, 漏1 |
| stove | (1.0,3.0) | 漏1 | 漏1 | (2.3,4.3)✓ |
| tv | (6.0,1.0) | (5.8,0.3)✓ | (5.6,0.3)✓ | (6.7,2.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,3.0), (3.0,3.0), (3.0,3.0) | - | (4.1,3.0)✓, 漏2 | (4.2,3.0)✓, 漏2 |
| refrigerator | (2.0,4.0) | - | 漏1 | (2.4,5.0)✓ |
| sofa | (6.0,2.0), (7.0,2.0) | - | (6.3,3.2)✓, 漏1 | (3.4,3.0)✗2.7, 漏1 |
| stove | (1.0,5.0) | - | 漏1 | (2.3,3.0)✗2.4 |
| tv | (6.0,6.0) | - | (5.6,4.5)✓ | (6.7,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (1.0,3.0), (2.0,3.0), (1.0,3.0) | - | (2.4,3.0)✓, 漏2 | (3.5,3.0)✓, 漏2 |
| refrigerator | (7.0,4.0) | - | 漏1 | (5.0,5.0)✗2.3 |
| sofa | (6.0,2.0), (4.0,2.0) | - | (4.3,3.2)✓, 漏1 | (2.3,3.0)✓, 漏1 |
| stove | (3.0,5.0) | - | 漏1 | (4.3,3.0)✗2.4 |
| tv | (1.0,6.0) | - | (0.3,4.5)✓ | (2.0,6.0)✓ |

- **baseline 问题**：漏画 stove ×1（GT 1，模型 0）；漏画 sofa ×1（GT 2，模型 1）；漏画 chair ×2（GT 3，模型 1）；漏画 refrigerator ×1（GT 1，模型 0）；chair-tv 距离画错（GT 2.0，模型 4.2）；chair→tv 方向错（GT W，模型 NW）；sofa-tv 距离画错（GT 3.2，模型 6.0）
- **threeview 问题**：漏画 stove ×1（GT 1，模型 0）；漏画 sofa ×1（GT 2，模型 1）；漏画 chair ×2（GT 3，模型 1）；漏画 refrigerator ×1（GT 1，模型 0）；chair-sofa 距离画错（GT 4.2，模型 3.2）；chair→tv 方向错（GT W，模型 NW）；sofa-tv 距离画错（GT 3.2，模型 4.5）；z 整体偏低（平均 -2.1 格）
- **threeview_3pass 问题**：漏画 sofa ×1（GT 2，模型 1）；漏画 chair ×1（GT 3，模型 2）；chair-refrigerator 距离画错（GT 5.1，模型 3.6）；chair→refrigerator 方向错（GT S，模型 SE）；chair-sofa 距离画错（GT 4.2，模型 2.2）；chair→sofa 方向错（GT SW，模型 E）；chair-tv 距离画错（GT 2.0，模型 4.5）；refrigerator→sofa 方向错（GT NW，模型 N）

### 样本 105 `fb5a96b1a2`（scannetpp · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (ceiling light, bookshelf, telephone, sofa) is the closest to the power strip?

- QA：GT D | baseline D（对） | threeview C（错） | threeview_3pass D（对）
- 对齐：baseline: yaw=84° mirror=否 平移=(7.3,-0.9) RMSE=1.78；threeview: yaw=85° mirror=否 平移=(6.8,0.4) RMSE=1.74；threeview_3pass: yaw=52° mirror=否 平移=(5.4,-1.7) RMSE=1.92
- 补偿：baseline: 尺度=0.69 z偏移=+0.00；threeview: 尺度=1.14 z偏移=-1.50；threeview_3pass: 尺度=0.73 z偏移=-2.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bookshelf | (6.0,1.0) | (3.3,1.6)✗2.8 | (4.1,2.4)✗2.4 | (2.3,2.7)✗4.0 |
| ceiling light | (6.0,2.0), (3.0,1.0), (5.0,3.0), (3.0,1.0), (2.0,4.0), (1.0,6.0), (4.0,7.0), (5.0,5.0), (5.0,7.0), (5.0,6.0), (7.0,4.0), (3.0,2.0) | (5.6,4.1)✓, 漏11 | (2.1,6.0)✓, 漏11 | (5.8,3.6)✓, 漏11 |
| power strip | (1.0,6.0) | (1.1,6.7)✓ | (3.1,4.2)✗2.8 | (1.1,4.6)✓ |
| sofa | (1.0,5.0) | (2.2,4.5)✓ | (2.1,6.0)✓ | (3.6,5.4)✗2.6 |
| telephone | (1.0,6.0) | (2.8,3.1)✗3.4 | (2.5,4.3)✗2.3 | (2.2,3.7)✗2.6 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bookshelf | (6.0,3.0) | - | (4.1,3.0)✓ | (2.3,3.0)✗3.7 |
| ceiling light | (6.0,7.0), (3.0,7.0), (5.0,7.0), (3.0,7.0), (2.0,7.0), (1.0,7.0), (4.0,7.0), (5.0,7.0), (5.0,7.0), (5.0,7.0), (7.0,7.0), (3.0,7.0) | - | (2.1,7.0)✓, 漏11 | (5.8,7.0)✓, 漏11 |
| power strip | (1.0,1.0) | - | (3.1,-0.5)✗2.6 | (1.1,-1.0)✗2.0 |
| sofa | (1.0,1.0) | - | (2.1,1.0)✓ | (3.6,1.0)✗2.6 |
| telephone | (1.0,4.0) | - | (2.5,0.0)✗4.3 | (2.2,2.0)✗2.3 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bookshelf | (1.0,3.0) | - | (2.4,3.0)✓ | (2.7,3.0)✓ |
| ceiling light | (2.0,7.0), (1.0,7.0), (3.0,7.0), (1.0,7.0), (4.0,7.0), (6.0,7.0), (7.0,7.0), (5.0,7.0), (7.0,7.0), (6.0,7.0), (4.0,7.0), (2.0,7.0) | - | (6.0,7.0)✓, 漏11 | (3.6,7.0)✓, 漏11 |
| power strip | (6.0,1.0) | - | (4.2,-0.5)✗2.3 | (4.6,-1.0)✗2.4 |
| sofa | (5.0,1.0) | - | (6.0,1.0)✓ | (5.4,1.0)✓ |
| telephone | (6.0,4.0) | - | (4.3,0.0)✗4.4 | (3.7,2.0)✗3.0 |

- **baseline 问题**：漏画 ceiling light ×11（GT 12，模型 1）；bookshelf-ceiling light 距离画错（GT 1.0，模型 5.0）；bookshelf→ceiling light 方向错（GT SE，模型 SW）；bookshelf-sofa 距离画错（GT 6.4，模型 4.5）；bookshelf→sofa 方向错（GT SE，模型 S）；bookshelf-telephone 距离画错（GT 7.1，模型 2.2）；bookshelf→telephone 方向错（GT SE，模型 S）；ceiling light-power strip 距离画错（GT 0.0，模型 7.6）
- **threeview 问题**：漏画 ceiling light ×11（GT 12，模型 1）；bookshelf-ceiling light 距离画错（GT 1.0，模型 3.6）；bookshelf-power strip 距离画错（GT 7.1，模型 1.8）；bookshelf-sofa 距离画错（GT 6.4，模型 3.6）；bookshelf-telephone 距离画错（GT 7.1，模型 2.1）；ceiling light-power strip 距离画错（GT 0.0，模型 1.8）；ceiling light→power strip 方向错（GT SE，模型 NW）；ceiling light-telephone 距离画错（GT 0.0，模型 1.6）
- **threeview_3pass 问题**：漏画 ceiling light ×11（GT 12，模型 1）；bookshelf-ceiling light 距离画错（GT 1.0，模型 5.0）；bookshelf→ceiling light 方向错（GT SE，模型 W）；bookshelf-power strip 距离画错（GT 7.1，模型 3.2）；bookshelf-sofa 距离画错（GT 6.4，模型 4.1）；bookshelf→sofa 方向错（GT SE，模型 SW）；bookshelf-telephone 距离画错（GT 7.1，模型 1.4）；bookshelf→telephone 方向错（GT SE，模型 S）

### 样本 106 `scene0608_00`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (tv, plant, chair, pillow) is the closest to the door?

- QA：GT D | baseline C（错） | threeview A（错） | threeview_3pass C（错）
- 对齐：baseline: yaw=-149° mirror=是(未证实) 平移=(9.0,1.3) RMSE=1.47；threeview: yaw=-92° mirror=否 平移=(-0.5,9.7) RMSE=1.27；threeview_3pass: yaw=16° mirror=是(未证实) 平移=(-2.7,6.9) RMSE=1.73
- 补偿：baseline: 尺度=0.58 z偏移=+0.00；threeview: 尺度=0.71 z偏移=+0.00；threeview_3pass: 尺度=0.56 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (5.0,3.0), (4.0,2.0), (6.0,5.0) | (3.2,4.2)✗2.1, 漏2 | (4.5,4.5)✓, 漏2 | (4.5,4.0)✓, (2.3,3.4)✗2.2, 漏1 |
| door | (1.0,1.0) | (1.1,0.9)✓ | (0.9,2.2)✓ | (1.7,1.5)✓ |
| pillow | (2.0,4.0), (1.0,3.0) | (3.2,4.2)✓, 漏1 | (4.4,4.5)✗2.5, 漏1 | (2.3,3.4)✓, (2.3,3.4)✗3.6, (4.5,4.0)多 |
| plant | (4.0,7.0), (2.0,7.0), (6.0,6.0) | (3.3,6.2)✓, 漏2 | (1.8,7.1)✓, 漏2 | (5.1,5.9)✓, 漏2 |
| tv | (2.0,6.0) | (1.1,5.6)✓ | (1.4,4.6)✓ | (2.8,5.8)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (5.0,2.0), (4.0,3.0), (6.0,2.0) | - | (4.5,3.0)✓, 漏2 | (4.5,3.0)✓, (2.3,3.0)✗2.9, 漏1 |
| door | (1.0,5.0) | - | (0.9,4.5)✓ | (1.7,5.0)✓ |
| pillow | (2.0,3.0), (1.0,4.0) | - | (4.4,3.5)✗2.5, 漏1 | (2.3,3.0)✓, (2.3,3.0)✗3.6, (4.5,3.0)多 |
| plant | (4.0,3.0), (2.0,6.0), (6.0,4.0) | - | (1.8,4.0)✗2.0, 漏2 | (5.1,3.0)✓, 漏2 |
| tv | (2.0,4.0) | - | (1.4,5.5)✓ | (2.8,6.0)✗2.1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (3.0,2.0), (2.0,3.0), (5.0,2.0) | - | (4.5,3.0)✓, 漏2 | (3.4,3.0)✓, (3.4,3.0)✓, (4.0,3.0)多, 漏1 |
| door | (1.0,5.0) | - | (2.2,4.5)✓ | (1.5,5.0)✓ |
| pillow | (4.0,3.0), (3.0,4.0) | - | (4.5,3.5)✓, 漏1 | (4.0,3.0)✓, (3.4,3.0)✓ |
| plant | (7.0,3.0), (7.0,6.0), (6.0,4.0) | - | (7.1,4.0)✓, 漏2 | (5.9,3.0)✓, 漏2 |
| tv | (6.0,4.0) | - | (4.6,5.5)✗2.0 | (5.8,6.0)✗2.0 |

- **baseline 问题**：漏画 pillow ×1（GT 2，模型 1）；漏画 chair ×2（GT 3，模型 1）；漏画 plant ×2（GT 3，模型 1）；chair-door 距离画错（GT 3.2，模型 6.7）；chair-pillow 距离画错（GT 2.8，模型 0.0）；chair-plant 距离画错（GT 1.0，模型 3.6）；door-pillow 距离画错（GT 2.0，模型 6.7）；door→pillow 方向错（GT S，模型 SW）
- **threeview 问题**：漏画 pillow ×1（GT 2，模型 1）；漏画 chair ×2（GT 3，模型 1）；漏画 plant ×2（GT 3，模型 1）；chair-door 距离画错（GT 3.2，模型 6.1）；chair-pillow 距离画错（GT 2.8，模型 0.2）；chair-plant 距离画错（GT 1.0，模型 5.3）；chair→plant 方向错（GT S，模型 SE）；chair→tv 方向错（GT SE，模型 E）
- **threeview_3pass 问题**：漏画 chair ×1（GT 3，模型 2）；漏画 plant ×2（GT 3，模型 1）；chair-pillow 距离画错（GT 2.8，模型 0.0）；chair-plant 距离画错（GT 1.0，模型 3.6）；chair→plant 方向错（GT S，模型 SW）；chair→tv 方向错（GT SE，模型 S）；door-pillow 距离画错（GT 2.0，模型 3.6）；door→pillow 方向错（GT S，模型 SW）

### 样本 107 `42899461`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (tv, stove, chair, fireplace) is the closest to the sofa?

- QA：GT C | baseline C（对） | threeview C（对） | threeview_3pass C（对）
- 对齐：baseline: yaw=28° mirror=是(未证实) 平移=(-2.2,7.2) RMSE=1.41；threeview: yaw=44° mirror=否 平移=(4.8,-1.4) RMSE=1.22；threeview_3pass: yaw=31° mirror=否 平移=(2.6,-1.2) RMSE=1.37
- 补偿：baseline: 尺度=1.13 z偏移=+0.00；threeview: 尺度=0.95 z偏移=+0.00；threeview_3pass: 尺度=0.96 z偏移=+1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (7.0,4.0), (7.0,3.0), (2.0,4.0), (1.0,4.0) | (2.6,4.0)✓, (2.6,4.0)✗2.1, (6.6,6.0)多, 漏2 | (3.5,3.7)✓, 漏3 | (3.1,3.8)✓, (3.1,3.8)✓, (6.4,5.8)多, 漏2 |
| fireplace | (4.0,8.0) | (3.1,8.0)✓ | (2.6,8.1)✓ | (2.8,8.1)✓ |
| sofa | (7.0,6.0) | (5.1,4.0)✗2.7 | (5.2,5.3)✓ | (5.3,4.0)✗2.7 |
| stove | (1.0,1.0) | 漏1 | 漏1 | 漏1 |
| tv | (1.0,7.0) | (3.6,7.0)✗2.6 | (2.8,7.9)✓ | (3.3,7.3)✗2.3 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (7.0,3.0), (7.0,3.0), (2.0,4.0), (1.0,4.0) | - | (3.5,3.5)✓, 漏3 | (6.4,3.0)✓, (3.1,3.0)✓, 漏2 |
| fireplace | (4.0,4.0) | - | (2.6,3.0)✓ | (2.8,3.0)✓ |
| sofa | (7.0,4.0) | - | (5.2,3.5)✓ | (5.3,3.0)✓ |
| stove | (1.0,7.0) | - | 漏1 | 漏1 |
| tv | (1.0,5.0) | - | (2.8,5.5)✓ | (3.3,6.0)✗2.5 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,3.0), (3.0,3.0), (4.0,4.0), (4.0,4.0) | - | (3.7,3.5)✓, 漏3 | (3.8,3.0)✓, (3.8,3.0)✗2.1, (5.8,3.0)多, 漏2 |
| fireplace | (8.0,4.0) | - | (8.1,3.0)✓ | (8.1,3.0)✓ |
| sofa | (6.0,4.0) | - | (5.3,3.5)✓ | (4.0,3.0)✗2.3 |
| stove | (1.0,7.0) | - | 漏1 | 漏1 |
| tv | (7.0,5.0) | - | (7.9,5.5)✓ | (7.3,6.0)✓ |

- **baseline 问题**：漏画 stove ×1（GT 1，模型 0）；漏画 chair ×2（GT 4，模型 2）；chair→fireplace 方向错（GT S，模型 SE）；chair→sofa 方向错（GT SW，模型 NW）；fireplace-tv 距离画错（GT 3.2，模型 1.0）；fireplace→tv 方向错（GT E，模型 NW）；sofa-tv 距离画错（GT 6.1，模型 3.0）；sofa→tv 方向错（GT E，模型 SE）
- **threeview 问题**：漏画 stove ×1（GT 1，模型 0）；漏画 chair ×3（GT 4，模型 1）；chair-tv 距离画错（GT 3.0，模型 4.5）；chair→tv 方向错（GT SE，模型 S）；fireplace-tv 距离画错（GT 3.2，模型 0.3）；fireplace→tv 方向错（GT E，模型 NW）；sofa-tv 距离画错（GT 6.1，模型 3.7）；sofa→tv 方向错（GT E，模型 SE）
- **threeview_3pass 问题**：漏画 stove ×1（GT 1，模型 0）；漏画 chair ×2（GT 4，模型 2）；chair→fireplace 方向错（GT S，模型 SE）；chair→sofa 方向错（GT SW，模型 NW）；fireplace-sofa 距离画错（GT 3.6，模型 5.0）；fireplace-tv 距离画错（GT 3.2，模型 1.0）；fireplace→tv 方向错（GT E，模型 NW）；sofa-tv 距离画错（GT 6.1，模型 4.0）

### 样本 108 `578511c8a9`（scannetpp · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (keyboard, printer, monitor, kettle) is the closest to the exhaust fan?

- QA：GT C | baseline B（错） | threeview D（错） | threeview_3pass C（对）
- 对齐：baseline: yaw=112° mirror=是(证据支持) 平移=(2.2,-1.1) RMSE=1.55；threeview: yaw=-145° mirror=否 平移=(6.2,13.1) RMSE=1.76；threeview_3pass: yaw=-65° mirror=否 平移=(-1.4,8.0) RMSE=2.03
- 补偿：baseline: 尺度=0.74 z偏移=+0.00；threeview: 尺度=0.75 z偏移=-1.80；threeview_3pass: 尺度=0.56 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| exhaust fan | (3.0,0.0) | (4.2,1.7)✗2.0 | (4.2,2.2)✗2.5 | (4.0,2.2)✗2.4 |
| kettle | (7.0,7.0) | (5.6,7.8)✓ | (3.6,4.5)✗4.3 | (5.8,3.6)✗3.6 |
| keyboard | (2.0,4.0), (2.0,2.0), (4.0,3.0), (3.0,4.0), (3.0,5.0), (3.0,5.0), (3.0,5.0), (4.0,5.0), (7.0,6.0), (7.0,4.0) | (7.2,6.1)✓, 漏9 | (4.7,6.2)✓, 漏9 | (6.1,5.6)✓, 漏9 |
| monitor | (7.0,5.0), (7.0,6.0), (7.0,5.0), (8.0,4.0), (3.0,4.0), (1.0,3.0), (2.0,2.0), (3.0,5.0), (3.0,5.0), (3.0,5.0), (3.0,4.0), (1.0,4.0), (4.0,3.0), (4.0,4.0), (4.0,4.0), (4.0,5.0) | (4.4,5.0)✓, 漏15 | (5.3,5.2)✓, 漏15 | (4.6,4.9)✓, 漏15 |
| printer | (7.0,7.0) | (6.6,3.5)✗3.6 | (7.1,6.0)✓ | (4.4,6.7)✗2.6 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| exhaust fan | (3.0,7.0) | - | (4.2,6.7)✓ | (4.0,7.0)✓ |
| kettle | (7.0,1.0) | - | (3.6,2.8)✗3.9 | (5.8,3.0)✗2.3 |
| keyboard | (2.0,3.0), (2.0,3.0), (4.0,3.0), (3.0,3.0), (3.0,3.0), (3.0,3.0), (3.0,3.0), (4.0,3.0), (7.0,3.0), (7.0,3.0) | - | (4.7,2.4)✓, 漏9 | (6.1,2.0)✓, 漏9 |
| monitor | (7.0,3.0), (7.0,3.0), (7.0,3.0), (8.0,3.0), (3.0,3.0), (1.0,3.0), (2.0,3.0), (3.0,3.0), (3.0,3.0), (3.0,3.0), (3.0,3.0), (1.0,3.0), (4.0,3.0), (4.0,3.0), (4.0,3.0), (4.0,3.0) | - | (5.3,3.7)✓, 漏15 | (4.6,4.0)✓, 漏15 |
| printer | (7.0,3.0) | - | (7.1,3.0)✓ | (4.4,3.0)✗2.6 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| exhaust fan | (0.0,7.0) | - | (2.2,6.7)✗2.2 | (2.2,7.0)✗2.2 |
| kettle | (7.0,1.0) | - | (4.5,2.8)✗3.1 | (3.6,3.0)✗3.9 |
| keyboard | (4.0,3.0), (2.0,3.0), (3.0,3.0), (4.0,3.0), (5.0,3.0), (5.0,3.0), (5.0,3.0), (5.0,3.0), (6.0,3.0), (4.0,3.0) | - | (6.2,2.4)✓, 漏9 | (5.6,2.0)✓, 漏9 |
| monitor | (5.0,3.0), (6.0,3.0), (5.0,3.0), (4.0,3.0), (4.0,3.0), (3.0,3.0), (2.0,3.0), (5.0,3.0), (5.0,3.0), (5.0,3.0), (4.0,3.0), (4.0,3.0), (3.0,3.0), (4.0,3.0), (4.0,3.0), (5.0,3.0) | - | (5.2,3.7)✓, 漏15 | (4.9,4.0)✓, 漏15 |
| printer | (7.0,3.0) | - | (6.0,3.0)✓ | (6.7,3.0)✓ |

- **baseline 问题**：漏画 keyboard ×9（GT 10，模型 1）；漏画 monitor ×15（GT 16，模型 1）；exhaust fan→kettle 方向错（GT SW，模型 S）；exhaust fan-keyboard 距离画错（GT 2.2，模型 7.2）；exhaust fan→keyboard 方向错（GT S，模型 SW）；exhaust fan-monitor 距离画错（GT 2.2，模型 4.5）；exhaust fan-printer 距离画错（GT 8.1，模型 4.1）；kettle-keyboard 距离画错（GT 1.0，模型 3.2）
- **threeview 问题**：漏画 keyboard ×9（GT 10，模型 1）；漏画 monitor ×15（GT 16，模型 1）；exhaust fan-kettle 距离画错（GT 8.1，模型 3.2）；exhaust fan→kettle 方向错（GT SW，模型 S）；exhaust fan-keyboard 距离画错（GT 2.2，模型 5.3）；exhaust fan-monitor 距离画错（GT 2.2，模型 4.3）；exhaust fan-printer 距离画错（GT 8.1，模型 6.3）；kettle-keyboard 距离画错（GT 1.0，模型 2.7）
- **threeview_3pass 问题**：漏画 keyboard ×9（GT 10，模型 1）；漏画 monitor ×15（GT 16，模型 1）；exhaust fan-kettle 距离画错（GT 8.1，模型 4.1）；exhaust fan-keyboard 距离画错（GT 2.2，模型 7.2）；exhaust fan→keyboard 方向错（GT S，模型 SW）；exhaust fan-monitor 距离画错（GT 2.2，模型 5.0）；exhaust fan→printer 方向错（GT SW，模型 S）；kettle-keyboard 距离画错（GT 1.0，模型 3.6）

### 样本 109 `scene0353_00`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (refrigerator, bed, window, trash bin) is the closest to the door?

- QA：GT D | baseline B（错） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=53° mirror=否 平移=(5.1,-2.8) RMSE=2.35；threeview: yaw=-116° mirror=否 平移=(1.3,10.8) RMSE=1.72；threeview_3pass: yaw=37° mirror=否 平移=(4.2,-4.0) RMSE=2.76
- 补偿：baseline: 尺度=0.40 z偏移=+0.00；threeview: 尺度=0.61 z偏移=-0.50；threeview_3pass: 尺度=0.26 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (2.0,4.0) | (4.1,3.2)✗2.3 | (3.8,4.0)✓ | (4.2,3.4)✗2.2 |
| door | (7.0,3.0) | (3.3,2.8)✗3.7 | (7.0,4.8)✓ | (3.1,4.0)✗4.0 |
| refrigerator | (5.0,5.0) | (5.6,4.6)✓ | 漏1 | (5.0,4.4)✓ |
| trash bin | (7.0,2.0) | (5.9,4.3)✗2.6 | (4.8,1.1)✗2.4 | (5.7,3.6)✗2.1 |
| window | (1.0,6.0) | (3.0,5.0)✗2.2 | (1.4,5.2)✓ | (4.0,4.6)✗3.3 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (2.0,4.0) | - | (3.8,2.5)✗2.4 | (4.2,2.0)✗3.0 |
| door | (7.0,4.0) | - | (7.0,4.0)✓ | (3.1,4.0)✗3.9 |
| refrigerator | (5.0,2.0) | - | 漏1 | (5.0,4.0)✗2.0 |
| trash bin | (7.0,1.0) | - | (4.8,1.0)✗2.2 | (5.7,1.0)✓ |
| window | (1.0,5.0) | - | (1.4,5.5)✓ | (4.0,6.0)✗3.1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (4.0,4.0) | - | (4.0,2.5)✓ | (3.4,2.0)✗2.1 |
| door | (3.0,4.0) | - | (4.8,4.0)✓ | (4.0,4.0)✓ |
| refrigerator | (5.0,2.0) | - | 漏1 | (4.4,4.0)✗2.1 |
| trash bin | (2.0,1.0) | - | (1.1,1.0)✓ | (3.6,1.0)✓ |
| window | (6.0,5.0) | - | (5.2,5.5)✓ | (4.6,6.0)✓ |

- **baseline 问题**：bed-door 距离画错（GT 5.1，模型 2.2）；bed→door 方向错（GT W，模型 NE）；bed-refrigerator 距离画错（GT 3.2，模型 5.1）；bed→refrigerator 方向错（GT W，模型 SW）；bed→trash bin 方向错（GT W，模型 SW）；bed-window 距离画错（GT 2.2，模型 5.4）；door-refrigerator 距离画错（GT 2.8，模型 7.3）；door→refrigerator 方向错（GT SE，模型 SW）
- **threeview 问题**：漏画 refrigerator ×1（GT 1，模型 0）；bed→trash bin 方向错（GT W，模型 N）；bed-window 距离画错（GT 2.2，模型 4.5）；door-trash bin 距离画错（GT 1.0，模型 7.0）；door→trash bin 方向错（GT N，模型 NE）；door-window 距离画错（GT 6.7，模型 9.2）；door→window 方向错（GT SE，模型 E）；trash bin-window 距离画错（GT 7.2，模型 8.7）
- **threeview_3pass 问题**：bed→door 方向错（GT W，模型 SE）；bed-refrigerator 距离画错（GT 3.2，模型 5.1）；bed→refrigerator 方向错（GT W，模型 SW）；bed-window 距离画错（GT 2.2，模型 4.5）；bed→window 方向错（GT SE，模型 S）；door-refrigerator 距离画错（GT 2.8，模型 7.6）；door→refrigerator 方向错（GT SE，模型 W）；door-trash bin 距离画错（GT 1.0，模型 9.9）

### 样本 110 `45261121`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (table, refrigerator, chair, stove) is the closest to the stool?

- QA：GT A | baseline C（错） | threeview A（对） | threeview_3pass D（错）
- 对齐：baseline: yaw=38° mirror=否 平移=(5.3,-2.6) RMSE=1.03；threeview: yaw=-90° mirror=否 平移=(0.5,8.7) RMSE=1.70；threeview_3pass: yaw=-99° mirror=是(未证实) 平移=(10.8,7.7) RMSE=1.27
- 补偿：baseline: 尺度=0.87 z偏移=+0.00；threeview: 尺度=0.58 z偏移=-2.25；threeview_3pass: 尺度=0.76 z偏移=+0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (6.0,4.0), (5.0,5.0) | (5.3,5.0)✓, (6.4,3.7)✓ | (6.2,3.8)✓, (3.9,3.8)✓ | (5.7,3.6)✓, (5.1,4.4)✓, (4.8,2.9)多, (4.2,3.8)多, 多2 |
| refrigerator | (1.0,7.0) | (1.0,4.9)✗2.1 | (3.3,5.5)✗2.8 | (3.1,6.3)✗2.2 |
| stool | (7.0,2.0) | (5.6,1.9)✓ | (5.1,5.0)✗3.5 | (6.7,4.9)✗3.0 |
| stove | (3.0,2.0) | (2.8,4.1)✗2.1 | (3.3,2.1)✓ | (2.4,1.8)✓ |
| table | (5.0,4.0) | (5.9,4.4)✓ | (5.1,3.8)✓ | (5.0,3.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (6.0,2.0), (5.0,2.0) | - | (6.2,2.2)✓, (3.9,2.2)✓ | (5.1,2.0)✓, (4.8,2.0)✓, (5.7,2.0)多, (4.2,2.0)多, 多2 |
| refrigerator | (1.0,3.0) | - | (3.3,2.8)✗2.4 | (3.1,4.5)✗2.6 |
| stool | (7.0,1.0) | - | (5.1,1.2)✓ | (6.7,1.5)✓ |
| stove | (3.0,3.0) | - | (3.3,1.8)✓ | (2.4,2.5)✓ |
| table | (5.0,2.0) | - | (5.1,1.8)✓ | (5.0,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,2.0), (5.0,2.0) | - | (3.8,2.2)✓, (3.8,2.2)✓, (3.8,2.2)多 | (3.8,2.0)✓, (4.4,2.0)✓, (2.9,2.0)多, (3.6,2.0)多, 多2 |
| refrigerator | (7.0,3.0) | - | (5.5,2.8)✓ | (6.3,4.5)✓ |
| stool | (2.0,1.0) | - | (5.0,1.2)✗3.0 | (4.9,1.5)✗3.0 |
| stove | (2.0,3.0) | - | (2.1,1.8)✓ | (1.8,2.5)✓ |
| table | (4.0,2.0) | - | (3.8,1.8)✓ | (3.7,2.0)✓ |

- **baseline 问题**：chair→refrigerator 方向错（GT SE，模型 E）；chair→stool 方向错（GT NW，模型 N）；chair→stove 方向错（GT NE，模型 E）；chair→table 方向错（GT NE，模型 E）；refrigerator-stool 距离画错（GT 7.8，模型 6.3）；refrigerator-stove 距离画错（GT 5.4，模型 2.2）；refrigerator→stove 方向错（GT N，模型 NW）；refrigerator→table 方向错（GT NW，模型 W）
- **threeview 问题**：chair-refrigerator 距离画错（GT 4.5，模型 3.2）；chair→stool 方向错（GT NW，模型 S）；chair→table 方向错（GT NE，模型 SE）；refrigerator-stool 距离画错（GT 7.8，模型 3.2）；refrigerator→stool 方向错（GT NW，模型 W）；stool-stove 距离画错（GT 4.0，模型 5.8）；stool→stove 方向错（GT E，模型 NE）；stool→table 方向错（GT SE，模型 N）
- **threeview_3pass 问题**：多画 chair ×2（GT 2，模型 4）；chair→stool 方向错（GT NW，模型 SW）；chair→table 方向错（GT NE，模型 E）；refrigerator-stool 距离画错（GT 7.8，模型 5.1）；refrigerator→stool 方向错（GT NW，模型 W）；stool-stove 距离画错（GT 4.0，模型 7.1）；stool→stove 方向错（GT E，模型 NE）；stool→table 方向错（GT SE，模型 NE）

### 样本 111 `c49a8c6cff`（scannetpp · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (door, chair, heater, plant) is the closest to the cup?

- QA：GT B | baseline B（对） | threeview B（对） | threeview_3pass B（对）
- 对齐：baseline: yaw=151° mirror=是(未证实) 平移=(5.1,-2.8) RMSE=1.58；threeview: yaw=-152° mirror=是(证据支持) 平移=(8.6,2.0) RMSE=0.84；threeview_3pass: yaw=-173° mirror=否 平移=(5.7,9.8) RMSE=1.73
- 补偿：baseline: 尺度=0.64 z偏移=+0.00；threeview: 尺度=0.81 z偏移=-1.50；threeview_3pass: 尺度=0.63 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (2.0,5.0) | (2.5,4.4)✓, (3.6,3.8)多, 多1 | (2.2,4.6)✓ | (2.4,3.6)✓, (1.2,3.5)多, 多1 |
| cup | (1.0,5.0) | (2.7,3.5)✗2.3 | (2.4,4.3)✓ | (1.7,4.2)✓ |
| door | (7.0,2.0) | (5.3,2.9)✓ | (6.4,2.8)✓ | (4.2,4.5)✗3.7 |
| heater | (1.0,2.0) | (0.4,3.3)✓ | (-0.1,2.0)✓ | (0.1,2.1)✓ |
| plant | (3.0,7.0), (1.0,6.0) | (2.0,7.5)✓, 漏1 | (3.0,7.3)✓, 漏1 | (3.5,5.6)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (2.0,2.0) | - | (2.2,2.0)✓ | (2.4,1.0)✓, (1.2,1.0)多, 多1 |
| cup | (1.0,3.0) | - | (2.4,3.0)✓ | (1.7,3.0)✓ |
| door | (7.0,3.0) | - | (6.4,3.5)✓ | (4.2,3.0)✗2.8 |
| heater | (1.0,1.0) | - | (-0.1,1.0)✓ | (0.1,1.0)✓ |
| plant | (3.0,5.0), (1.0,5.0) | - | (3.0,3.0)✗2.0, 漏1 | (3.5,2.0)✗3.0, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (5.0,2.0) | - | (4.6,2.0)✓ | (3.6,1.0)✓, (3.5,1.0)多, 多1 |
| cup | (5.0,3.0) | - | (4.3,3.0)✓ | (4.2,3.0)✓ |
| door | (2.0,3.0) | - | (2.8,3.5)✓ | (4.5,3.0)✗2.5 |
| heater | (2.0,1.0) | - | (2.0,1.0)✓ | (2.1,1.0)✓ |
| plant | (7.0,5.0), (6.0,5.0) | - | (7.3,3.0)✗2.0, 漏1 | (5.6,2.0)✗3.0, 漏1 |

- **baseline 问题**：多画 chair ×1（GT 1，模型 2）；漏画 plant ×1（GT 2，模型 1）；chair→cup 方向错（GT E，模型 NE）；chair-door 距离画错（GT 5.8，模型 3.0）；chair→heater 方向错（GT N，模型 E）；chair-plant 距离画错（GT 1.4，模型 5.0）；cup-door 距离画错（GT 6.7，模型 4.1）；cup→door 方向错（GT NW，模型 W）
- **threeview 问题**：漏画 plant ×1（GT 2，模型 1）；chair→cup 方向错（GT E，模型 NW）；chair-heater 距离画错（GT 3.2，模型 4.3）；chair→heater 方向错（GT N，模型 NE）；chair-plant 距离画错（GT 1.4，模型 3.5）；cup-door 距离画错（GT 6.7，模型 5.3）；cup→door 方向错（GT NW，模型 W）；cup-heater 距离画错（GT 3.0，模型 4.1）
- **threeview_3pass 问题**：多画 chair ×1（GT 1，模型 2）；漏画 plant ×1（GT 2，模型 1）；chair→cup 方向错（GT E，模型 S）；chair-door 距离画错（GT 5.8，模型 3.2）；chair→door 方向错（GT NW，模型 W）；chair→heater 方向错（GT N，模型 NE）；chair-plant 距离画错（GT 1.4，模型 3.6）；chair→plant 方向错（GT S，模型 SW）

### 样本 112 `scene0221_01`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (lamp, pillow, bed, trash bin) is the closest to the microwave?

- QA：GT C | baseline A（错） | threeview D（错） | threeview_3pass C（对）
- 对齐：baseline: yaw=39° mirror=否 平移=(4.6,-5.0) RMSE=1.34；threeview: yaw=0° mirror=否 平移=(-0.7,-2.4) RMSE=1.03；threeview_3pass: yaw=14° mirror=否 平移=(0.5,-4.7) RMSE=1.00
- 补偿：baseline: 尺度=0.46 z偏移=+0.00；threeview: 尺度=0.54 z偏移=+0.00；threeview_3pass: 尺度=0.54 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (4.0,3.0), (2.0,3.0) | (4.6,2.4)✓, 漏1 | (4.2,2.5)✓, 漏1 | (4.0,2.2)✓, 漏1 |
| lamp | (3.0,1.0), (3.0,0.0) | (3.9,1.2)✓, 漏1 | (2.6,1.1)✓, 漏1 | (2.7,0.8)✓, 漏1 |
| microwave | (6.0,1.0) | (4.4,0.4)✓ | 漏1 | 漏1 |
| pillow | (2.0,1.0), (4.0,1.0), (4.0,1.0), (4.0,1.0), (2.0,1.0) | (4.9,2.0)✓, 漏4 | (4.3,1.4)✓, 漏4 | (3.7,1.5)✓, (3.7,1.5)✓, (4.7,1.8)多, 漏3 |
| trash bin | (6.0,4.0) | (5.1,4.0)✓ | (5.9,4.1)✓ | (5.9,3.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (4.0,2.0), (2.0,3.0) | - | (4.2,3.0)✓, 漏1 | (4.0,3.0)✓, 漏1 |
| lamp | (3.0,4.0), (3.0,5.0) | - | (2.6,5.0)✓, 漏1 | (2.7,4.0)✓, 漏1 |
| microwave | (6.0,5.0) | - | 漏1 | 漏1 |
| pillow | (2.0,4.0), (4.0,4.0), (4.0,4.0), (4.0,4.0), (2.0,4.0) | - | (4.3,4.0)✓, 漏4 | (3.7,4.0)✓, (3.7,4.0)✓, (4.7,4.0)多, 漏3 |
| trash bin | (6.0,2.0) | - | (5.9,2.0)✓ | (5.9,1.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (3.0,2.0), (3.0,3.0) | - | (2.5,3.0)✓, 漏1 | (2.2,3.0)✓, 漏1 |
| lamp | (1.0,4.0), (0.0,5.0) | - | (1.1,5.0)✓, 漏1 | (0.8,4.0)✓, 漏1 |
| microwave | (1.0,5.0) | - | 漏1 | 漏1 |
| pillow | (1.0,4.0), (1.0,4.0), (1.0,4.0), (1.0,4.0), (1.0,4.0) | - | (1.4,4.0)✓, 漏4 | (1.5,4.0)✓, (1.5,4.0)✓, (1.8,4.0)多, 漏3 |
| trash bin | (4.0,2.0) | - | (4.1,2.0)✓ | (3.7,1.0)✓ |

- **baseline 问题**：漏画 bed ×1（GT 2，模型 1）；漏画 pillow ×4（GT 5，模型 1）；漏画 lamp ×1（GT 2，模型 1）；bed→lamp 方向错（GT N，模型 NE）；bed-microwave 距离画错（GT 2.8，模型 4.2）；bed→microwave 方向错（GT NW，模型 N）；bed→pillow 方向错（GT N，模型 NW）；bed-trash bin 距离画错（GT 2.2，模型 3.6）
- **threeview 问题**：漏画 bed ×1（GT 2，模型 1）；漏画 pillow ×4（GT 5，模型 1）；漏画 microwave ×1（GT 1，模型 0）；漏画 lamp ×1（GT 2，模型 1）；bed-lamp 距离画错（GT 2.2，模型 3.9）；bed→lamp 方向错（GT N，模型 NE）；bed-trash bin 距离画错（GT 2.2，模型 4.2）；bed→trash bin 方向错（GT W，模型 SW）
- **threeview_3pass 问题**：漏画 bed ×1（GT 2，模型 1）；漏画 pillow ×3（GT 5，模型 2）；漏画 microwave ×1（GT 1，模型 0）；漏画 lamp ×1（GT 2，模型 1）；bed-lamp 距离画错（GT 2.2，模型 3.6）；bed→lamp 方向错（GT N，模型 NE）；bed-trash bin 距离画错（GT 2.2，模型 4.5）；bed→trash bin 方向错（GT W，模型 SW）

### 样本 113 `47429977`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (refrigerator, stove, stool, sofa) is the closest to the tv?

- QA：GT C | baseline A（错） | threeview C（对） | threeview_3pass D（错）
- 对齐：baseline: yaw=-25° mirror=是(证据支持) 平移=(3.5,10.8) RMSE=1.46；threeview: yaw=-36° mirror=是(证据支持) 平移=(5.5,11.1) RMSE=1.21；threeview_3pass: yaw=-106° mirror=是(未证实) 平移=(10.0,6.6) RMSE=1.20
- 补偿：baseline: 尺度=1.11 z偏移=+0.00；threeview: 尺度=1.04 z偏移=+0.50；threeview_3pass: 尺度=0.93 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (2.0,7.0) | (2.6,4.6)✗2.5 | 漏1 | (2.0,6.7)✓ |
| sofa | (6.0,6.0), (7.0,4.0) | (7.1,6.2)✓, 漏1 | (7.6,5.4)✓, 漏1 | (5.7,2.8)✓, 漏1 |
| stool | (7.0,2.0), (4.0,7.0) | (4.1,5.1)✓, 漏1 | (4.6,5.0)✗2.1, 漏1 | (3.5,5.3)✓, 漏1 |
| stove | (1.0,3.0) | (1.6,5.0)✗2.1 | 漏1 | (1.5,4.9)✓ |
| tv | (6.0,1.0) | (4.7,1.1)✓ | (4.8,1.6)✓ | (7.4,2.3)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (2.0,4.0) | - | 漏1 | (2.0,5.0)✓ |
| sofa | (6.0,2.0), (7.0,2.0) | - | (7.6,2.5)✓, 漏1 | (5.7,2.0)✓, 漏1 |
| stool | (7.0,2.0), (4.0,2.0) | - | (4.6,2.0)✓, 漏1 | (3.5,2.0)✓, 漏1 |
| stove | (1.0,5.0) | - | 漏1 | (1.5,3.0)✗2.1 |
| tv | (6.0,6.0) | - | (4.8,5.0)✓ | (7.4,4.0)✗2.5 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (7.0,4.0) | - | 漏1 | (6.7,5.0)✓ |
| sofa | (6.0,2.0), (4.0,2.0) | - | (5.4,2.5)✓, 漏1 | (2.8,2.0)✓, 漏1 |
| stool | (2.0,2.0), (7.0,2.0) | - | (5.0,2.0)✗2.0, 漏1 | (5.3,2.0)✓, 漏1 |
| stove | (3.0,5.0) | - | 漏1 | (4.9,3.0)✗2.8 |
| tv | (1.0,6.0) | - | (1.6,5.0)✓ | (2.3,4.0)✗2.4 |

- **baseline 问题**：漏画 stool ×1（GT 2，模型 1）；漏画 sofa ×1（GT 2，模型 1）；refrigerator→sofa 方向错（GT NW，模型 W）；refrigerator→stool 方向错（GT NW，模型 W）；refrigerator-stove 距离画错（GT 4.1，模型 1.0）；refrigerator→stove 方向错（GT N，模型 SE）；refrigerator-tv 距离画错（GT 7.2，模型 3.6）；sofa→stool 方向错（GT NE，模型 E）
- **threeview 问题**：漏画 stool ×1（GT 2，模型 1）；漏画 stove ×1（GT 1，模型 0）；漏画 sofa ×1（GT 2，模型 1）；漏画 refrigerator ×1（GT 1，模型 0）；sofa→stool 方向错（GT NE，模型 E）；sofa-tv 距离画错（GT 3.2，模型 4.5）；sofa→tv 方向错（GT N，模型 NE）；stool-tv 距离画错（GT 1.4，模型 3.2）
- **threeview_3pass 问题**：漏画 stool ×1（GT 2，模型 1）；漏画 sofa ×1（GT 2，模型 1）；refrigerator-sofa 距离画错（GT 4.1，模型 5.8）；refrigerator-stove 距离画错（GT 4.1，模型 2.0）；sofa-stool 距离画错（GT 2.0，模型 3.6）；sofa→stool 方向错（GT NE，模型 SE）；sofa→stove 方向错（GT E，模型 SE）；sofa-tv 距离画错（GT 3.2，模型 2.0）

### 样本 114 `bde1e479ad`（scannetpp · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (whiteboard, ceiling light, power strip, door) is the closest to the clock?

- QA：GT A | baseline B（错） | threeview A（对） | threeview_3pass B（错）
- 对齐：baseline: yaw=-9° mirror=否 平移=(-1.2,2.1) RMSE=2.56；threeview: yaw=-48° mirror=否 平移=(-1.9,5.7) RMSE=2.02；threeview_3pass: yaw=-13° mirror=否 平移=(-1.1,2.2) RMSE=2.44
- 补偿：baseline: 尺度=0.32 z偏移=+0.00；threeview: 尺度=0.42 z偏移=-1.00；threeview_3pass: 尺度=0.45 z偏移=-0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (5.0,7.0), (5.0,4.0), (2.0,4.0), (2.0,1.0), (3.0,4.0), (7.0,4.0), (3.0,6.0), (7.0,2.0) | (4.5,4.6)✓, 漏7 | (3.8,4.9)✓, 漏7 | (3.3,3.8)✓, (3.3,3.8)✓, (5.1,3.4)多, 漏6 |
| clock | (4.0,7.0) | (5.5,4.7)✗2.7 | (2.5,3.8)✗3.5 | (5.6,3.7)✗3.7 |
| door | (3.0,0.0), (2.0,7.0) | (3.5,6.3)✓, 漏1 | (2.7,6.1)✓, 漏1 | (3.0,6.2)✓, 漏1 |
| power strip | (7.0,5.0), (2.0,1.0) | (5.8,6.9)✗2.2, 漏1 | (2.4,4.5)✗3.5, 漏1 | (4.6,7.1)✗3.2, 漏1 |
| whiteboard | (1.0,4.0), (1.0,4.0), (4.0,7.0) | (4.7,5.5)✓, 漏2 | (2.5,3.8)✓, 漏2 | (4.5,4.9)✗2.2, 漏2 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (5.0,7.0), (5.0,7.0), (2.0,7.0), (2.0,7.0), (3.0,7.0), (7.0,8.0), (3.0,7.0), (7.0,7.0) | - | (3.8,8.5)✓, 漏7 | (5.1,8.5)✓, (3.3,8.5)✓, 漏6 |
| clock | (4.0,7.0) | - | (2.5,7.0)✓ | (5.6,5.5)✗2.2 |
| door | (3.0,3.0), (2.0,3.0) | - | (2.7,3.0)✓, 漏1 | (3.0,3.5)✓, 漏1 |
| power strip | (7.0,1.0), (2.0,2.0) | - | (2.4,1.0)✓, 漏1 | (4.6,0.5)✗2.5, 漏1 |
| whiteboard | (1.0,5.0), (1.0,2.0), (4.0,4.0) | - | (2.5,4.0)✓, 漏2 | (4.5,3.5)✓, 漏2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (7.0,7.0), (4.0,7.0), (4.0,7.0), (1.0,7.0), (4.0,7.0), (4.0,8.0), (6.0,7.0), (2.0,7.0) | - | (4.9,8.5)✓, 漏7 | (3.8,8.5)✓, (3.8,8.5)✓, (3.4,8.5)多, 漏6 |
| clock | (7.0,7.0) | - | (3.8,7.0)✗3.2 | (3.7,5.5)✗3.6 |
| door | (0.0,3.0), (7.0,3.0) | - | (6.1,3.0)✓, 漏1 | (6.2,3.5)✓, 漏1 |
| power strip | (5.0,1.0), (1.0,2.0) | - | (4.5,1.0)✓, 漏1 | (7.1,0.5)✗2.2, 漏1 |
| whiteboard | (4.0,5.0), (4.0,2.0), (7.0,4.0) | - | (3.8,4.0)✓, 漏2 | (4.9,3.5)✓, 漏2 |

- **baseline 问题**：漏画 ceiling light ×7（GT 8，模型 1）；漏画 power strip ×1（GT 2，模型 1）；漏画 door ×1（GT 2，模型 1）；漏画 whiteboard ×2（GT 3，模型 1）；ceiling light-clock 距离画错（GT 1.0，模型 3.2）；ceiling light→clock 方向错（GT S，模型 W）；ceiling light-door 距离画错（GT 1.4，模型 6.4）；ceiling light→door 方向错（GT E，模型 SE）
- **threeview 问题**：漏画 ceiling light ×7（GT 8，模型 1）；漏画 power strip ×1（GT 2，模型 1）；漏画 door ×1（GT 2，模型 1）；漏画 whiteboard ×2（GT 3，模型 1）；ceiling light-clock 距离画错（GT 1.0，模型 4.0）；ceiling light→clock 方向错（GT S，模型 NE）；ceiling light-door 距离画错（GT 1.4，模型 4.0）；ceiling light→door 方向错（GT E，模型 SE）
- **threeview_3pass 问题**：漏画 ceiling light ×6（GT 8，模型 2）；漏画 power strip ×1（GT 2，模型 1）；漏画 door ×1（GT 2，模型 1）；漏画 whiteboard ×2（GT 3，模型 1）；ceiling light→clock 方向错（GT S，模型 W）；ceiling light-door 距离画错（GT 1.4，模型 5.4）；ceiling light→door 方向错（GT E，模型 SE）；ceiling light-power strip 距离画错（GT 0.0，模型 8.1）

### 样本 115 `scene0231_00`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (clock, chair, backpack, lamp) is the closest to the pillow?

- QA：GT D | baseline D（对） | threeview B（错） | threeview_3pass D（对）
- 对齐：baseline: yaw=36° mirror=否 平移=(3.1,-3.1) RMSE=1.99；threeview: yaw=115° mirror=否 平移=(8.5,1.4) RMSE=1.44；threeview_3pass: yaw=47° mirror=否 平移=(4.1,-1.3) RMSE=1.86
- 补偿：baseline: 尺度=0.16 z偏移=+0.00；threeview: 尺度=0.23 z偏移=-1.50；threeview_3pass: 尺度=0.20 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (3.0,5.0) | (3.1,4.3)✓ | (2.7,4.3)✓ | (2.4,4.6)✓ |
| chair | (3.0,4.0), (4.0,4.0), (4.0,3.0), (4.0,3.0), (1.0,2.0), (1.0,4.0) | (2.5,4.1)✓, (2.5,4.1)✓, (3.2,4.6)多, 漏4 | (2.7,3.9)✓, 漏5 | (2.4,4.3)✓, 漏5 |
| clock | (4.0,5.0) | (3.5,3.6)✓ | (3.6,4.3)✓ | (3.6,3.8)✓ |
| lamp | (3.0,2.0), (2.0,4.0) | (2.7,3.6)✓, 漏1 | (3.3,3.6)✓, 漏1 | (2.8,3.5)✓, 漏1 |
| pillow | (2.0,2.0) | (2.9,3.8)✗2.0, (3.1,3.9)多, 多1 | (2.7,3.9)✗2.0 | (2.7,3.8)✓, (2.9,3.9)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (3.0,1.0) | - | (2.7,0.7)✓ | (2.4,1.0)✓ |
| chair | (3.0,2.0), (4.0,2.0), (4.0,2.0), (4.0,2.0), (1.0,2.0), (1.0,3.0) | - | (2.7,2.3)✓, 漏5 | (2.4,2.0)✓, 漏5 |
| clock | (4.0,6.0) | - | (3.6,6.0)✓ | (3.6,6.0)✓ |
| lamp | (3.0,1.0), (2.0,3.0) | - | (3.3,4.0)✓, 漏1 | (2.8,4.0)✓, 漏1 |
| pillow | (2.0,2.0) | - | (2.7,2.7)✓ | (2.7,3.0)✓, (2.9,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (5.0,1.0) | - | (4.3,0.7)✓ | (4.6,1.0)✓ |
| chair | (4.0,2.0), (4.0,2.0), (3.0,2.0), (3.0,2.0), (2.0,2.0), (4.0,3.0) | - | (3.9,2.3)✓, 漏5 | (4.3,2.0)✓, 漏5 |
| clock | (5.0,6.0) | - | (4.3,6.0)✓ | (3.8,6.0)✓ |
| lamp | (2.0,1.0), (4.0,3.0) | - | (3.6,4.0)✓, 漏1 | (3.5,4.0)✓, 漏1 |
| pillow | (2.0,2.0) | - | (3.9,2.7)✗2.0 | (3.8,3.0)✗2.0, (3.9,3.0)多, 多1 |

- **baseline 问题**：多画 pillow ×1（GT 1，模型 2）；漏画 lamp ×1（GT 2，模型 1）；漏画 chair ×4（GT 6，模型 2）；backpack→chair 方向错（GT N，模型 E）；backpack-clock 距离画错（GT 1.0，模型 5.1）；backpack→clock 方向错（GT W，模型 NW）；backpack-lamp 距离画错（GT 1.4，模型 5.4）；backpack→lamp 方向错（GT N，模型 NE）
- **threeview 问题**：漏画 lamp ×1（GT 2，模型 1）；漏画 chair ×5（GT 6，模型 1）；backpack-clock 距离画错（GT 1.0，模型 3.8）；backpack-lamp 距离画错（GT 1.4，模型 4.1）；backpack→lamp 方向错（GT N，模型 NW）；backpack-pillow 距离画错（GT 3.2，模型 1.8）；chair-clock 距离画错（GT 1.0，模型 4.2）；chair-lamp 距离画错（GT 1.0，模型 2.9）
- **threeview_3pass 问题**：多画 pillow ×1（GT 1，模型 2）；漏画 lamp ×1（GT 2，模型 1）；漏画 chair ×5（GT 6，模型 1）；backpack-clock 距离画错（GT 1.0，模型 7.1）；backpack→clock 方向错（GT W，模型 NW）；backpack-lamp 距离画错（GT 1.4，模型 5.8）；backpack→pillow 方向错（GT N，模型 NW）；chair-clock 距离画错（GT 1.0，模型 6.3）

### 样本 116 `42898849`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (tv, fireplace, table, chair) is the closest to the stove?

- QA：GT C | baseline A（错） | threeview C（对） | threeview_3pass B（错）
- 对齐：baseline: yaw=89° mirror=否 平移=(9.3,0.7) RMSE=1.34；threeview: yaw=79° mirror=否 平移=(7.9,-0.3) RMSE=1.30；threeview_3pass: yaw=71° mirror=否 平移=(7.6,-0.9) RMSE=1.93
- 补偿：baseline: 尺度=0.55 z偏移=+0.00；threeview: 尺度=0.51 z偏移=-1.10；threeview_3pass: 尺度=0.52 z偏移=+0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (6.0,1.0), (6.0,0.0), (3.0,5.0), (3.0,4.0), (3.0,5.0), (2.0,5.0), (2.0,5.0), (1.0,5.0) | (4.1,4.7)✓, (4.1,4.7)✗2.2, (4.2,6.9)多, 漏6 | (3.8,4.6)✓, (3.8,4.6)✓, (4.2,6.6)多, 漏6 | (2.7,4.8)✓, (2.7,4.8)✓, (3.4,6.8)多, 漏6 |
| fireplace | (7.0,5.0) | (6.9,5.8)✓ | (6.0,5.2)✓ | (6.0,4.8)✓ |
| stove | (2.0,1.0) | 漏1 | 漏1 | (5.0,3.5)✗3.9 |
| table | (6.0,3.0), (5.0,7.0), (2.0,4.0), (0.0,7.0) | (4.1,5.8)✓, 漏3 | (4.0,5.6)✓, 漏3 | (3.5,5.6)✗2.0, 漏3 |
| tv | (7.0,7.0) | (5.8,5.8)✓ | 漏1 | (6.5,4.6)✗2.5 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (6.0,2.0), (6.0,2.0), (3.0,2.0), (3.0,2.0), (3.0,2.0), (2.0,2.0), (2.0,2.0), (1.0,3.0) | - | (3.8,2.1)✓, (3.8,2.1)✓, (4.2,2.1)多, 漏6 | (2.7,2.5)✓, (2.7,2.5)✓, (3.4,2.5)多, 漏6 |
| fireplace | (7.0,3.0) | - | (6.0,3.4)✓ | (6.0,2.5)✓ |
| stove | (2.0,4.0) | - | 漏1 | (5.0,2.5)✗3.3 |
| table | (6.0,2.0), (5.0,2.0), (2.0,2.0), (0.0,1.0) | - | (4.0,1.9)✓, 漏3 | (3.5,2.5)✓, 漏3 |
| tv | (7.0,7.0) | - | 漏1 | (6.5,5.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (1.0,2.0), (0.0,2.0), (5.0,2.0), (4.0,2.0), (5.0,2.0), (5.0,2.0), (5.0,2.0), (5.0,3.0) | - | (4.6,2.1)✓, (4.6,2.1)✓, (6.6,2.1)多, 漏6 | (4.8,2.5)✓, (4.8,2.5)✓, (6.8,2.5)多, 漏6 |
| fireplace | (5.0,3.0) | - | (5.2,3.4)✓ | (4.8,2.5)✓ |
| stove | (1.0,4.0) | - | 漏1 | (3.5,2.5)✗2.9 |
| table | (3.0,2.0), (7.0,2.0), (4.0,2.0), (7.0,1.0) | - | (5.6,1.9)✓, 漏3 | (5.6,2.5)✓, 漏3 |
| tv | (7.0,7.0) | - | 漏1 | (4.6,5.5)✗2.8 |

- **baseline 问题**：漏画 stove ×1（GT 1，模型 0）；漏画 table ×3（GT 4，模型 1）；漏画 chair ×6（GT 8，模型 2）；chair-fireplace 距离画错（GT 4.0，模型 5.4）；chair→table 方向错（GT S，模型 E）；chair→tv 方向错（GT SW，模型 W）；fireplace-table 距离画错（GT 2.2，模型 5.0）；fireplace→tv 方向错（GT S，模型 E）
- **threeview 问题**：漏画 stove ×1（GT 1，模型 0）；漏画 tv ×1（GT 1，模型 0）；漏画 chair ×6（GT 8，模型 2）；漏画 table ×3（GT 4，模型 1）；chair→table 方向错（GT S，模型 W）；fireplace-table 距离画错（GT 2.2，模型 4.0）；z 整体偏高（平均 +1.2 格）
- **threeview_3pass 问题**：漏画 table ×3（GT 4，模型 1）；漏画 chair ×6（GT 8，模型 2）；chair-fireplace 距离画错（GT 4.0，模型 6.3）；chair-stove 距离画错（GT 3.2，模型 5.1）；chair→stove 方向错（GT NE，模型 NW）；chair-table 距离画错（GT 1.0，模型 2.2）；chair→table 方向错（GT S，模型 W）；chair-tv 距离画错（GT 4.5，模型 7.3）

### 样本 117 `3db0a1c8f3`（scannetpp · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (bowl, blanket, chair, ceiling light) is the closest to the printer?

- QA：GT C | baseline A（错） | threeview A（错） | threeview_3pass C（对）
- 对齐：baseline: yaw=87° mirror=否 平移=(7.9,-0.1) RMSE=1.66；threeview: yaw=-53° mirror=是(证据支持) 平移=(4.4,10.5) RMSE=1.31；threeview_3pass: yaw=-99° mirror=是(证据支持) 平移=(9.4,8.6) RMSE=1.14
- 补偿：baseline: 尺度=0.58 z偏移=+0.00；threeview: 尺度=1.77 z偏移=-1.00；threeview_3pass: 尺度=0.74 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blanket | (1.0,1.0) | (1.2,3.5)✗2.5 | (2.9,3.2)✗2.9 | (0.9,2.8)✓ |
| bowl | (4.0,7.0) | (3.1,5.8)✓ | (3.0,6.6)✓ | (3.7,6.1)✓ |
| ceiling light | (7.0,4.0), (1.0,3.0), (4.0,4.0) | (5.4,5.1)✓, 漏2 | (3.7,2.7)✓, 漏2 | (5.6,4.3)✓, 漏2 |
| chair | (3.0,7.0), (4.0,4.0), (3.0,2.0), (3.0,7.0) | (1.8,4.7)✗2.3, 漏3 | (2.9,3.2)✓, 漏3 | (2.1,5.6)✓, 漏3 |
| printer | (2.0,7.0) | (2.5,7.0)✓ | (2.5,7.3)✓ | (1.6,7.2)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blanket | (1.0,2.0) | - | (2.9,3.0)✗2.1 | (0.9,1.0)✓ |
| bowl | (4.0,3.0) | - | (3.0,2.5)✓ | (3.7,3.0)✓ |
| ceiling light | (7.0,7.0), (1.0,7.0), (4.0,8.0) | - | (3.7,7.8)✓, 漏2 | (5.6,8.0)✓, 漏2 |
| chair | (3.0,2.0), (4.0,2.0), (3.0,2.0), (3.0,2.0) | - | (2.9,2.8)✓, 漏3 | (2.1,2.0)✓, 漏3 |
| printer | (2.0,2.0) | - | (2.5,2.0)✓ | (1.6,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blanket | (1.0,2.0) | - | (3.2,3.0)✗2.4 | (2.8,1.0)✗2.1 |
| bowl | (7.0,3.0) | - | (6.6,2.5)✓ | (6.1,3.0)✓ |
| ceiling light | (4.0,7.0), (3.0,7.0), (4.0,8.0) | - | (2.7,7.8)✓, 漏2 | (4.3,8.0)✓, 漏2 |
| chair | (7.0,2.0), (4.0,2.0), (2.0,2.0), (7.0,2.0) | - | (3.2,2.8)✓, 漏3 | (5.6,2.0)✓, 漏3 |
| printer | (7.0,2.0) | - | (7.3,2.0)✓ | (7.2,3.0)✓ |

- **baseline 问题**：漏画 ceiling light ×2（GT 3，模型 1）；漏画 chair ×3（GT 4，模型 1）；blanket-bowl 距离画错（GT 6.7，模型 5.0）；blanket-ceiling light 距离画错（GT 2.0，模型 7.6）；blanket→ceiling light 方向错（GT SW，模型 W）；bowl-ceiling light 距离画错（GT 3.0，模型 4.1）；bowl→ceiling light 方向错（GT N，模型 W）；bowl-chair 距离画错（GT 1.0，模型 2.8）
- **threeview 问题**：漏画 ceiling light ×2（GT 3，模型 1）；漏画 chair ×3（GT 4，模型 1）；blanket-bowl 距离画错（GT 6.7，模型 1.9）；blanket→bowl 方向错（GT SW，模型 S）；blanket-ceiling light 距离画错（GT 2.0，模型 0.5）；blanket→ceiling light 方向错（GT SW，模型 NW）；blanket-chair 距离画错（GT 2.2，模型 0.0）；blanket→chair 方向错（GT SW，模型 E）
- **threeview_3pass 问题**：漏画 ceiling light ×2（GT 3，模型 1）；漏画 chair ×3（GT 4，模型 1）；blanket-ceiling light 距离画错（GT 2.0，模型 6.7）；blanket→ceiling light 方向错（GT SW，模型 W）；blanket-chair 距离画错（GT 2.2，模型 4.1）；bowl→ceiling light 方向错（GT N，模型 NW）；bowl-chair 距离画错（GT 1.0，模型 2.2）；bowl→chair 方向错（GT N，模型 E）

### 样本 118 `scene0699_00`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (window, chair, table, closet) is the closest to the nightstand?

- QA：GT A | baseline D（错） | threeview D（错） | threeview_3pass D（错）
- 对齐：baseline: yaw=-88° mirror=否 平移=(-0.8,8.6) RMSE=1.67；threeview: yaw=-42° mirror=否 平移=(-3.5,2.4) RMSE=2.38；threeview_3pass: yaw=-104° mirror=是(证据支持) 平移=(10.8,6.6) RMSE=1.93
- 补偿：baseline: 尺度=0.64 z偏移=+0.00；threeview: 尺度=0.37 z偏移=-0.50；threeview_3pass: 尺度=0.53 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (5.0,3.0) | (5.8,3.0)✓ | (3.9,2.9)✓ | (3.4,2.3)✓ |
| closet | (7.0,7.0) | (4.4,5.5)✗3.0 | (3.4,5.1)✗4.1 | (5.1,4.6)✗3.1 |
| nightstand | (1.0,3.0) | (3.8,4.2)✗3.0 | (2.6,3.8)✓ | (3.4,4.5)✗2.8 |
| table | (5.0,2.0) | (5.8,2.3)✓ | (4.3,3.3)✓ | (4.4,2.0)✓ |
| window | (1.0,5.0), (5.0,1.0) | (3.3,1.0)✓, 漏1 | (4.8,4.8)✗3.8, 漏1 | (6.7,2.6)✗2.3, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (5.0,2.0) | - | (3.9,2.0)✓ | (3.4,2.0)✓ |
| closet | (7.0,5.0) | - | (3.4,4.5)✗3.7 | (5.1,5.0)✓ |
| nightstand | (1.0,2.0) | - | (2.6,2.0)✓ | (3.4,2.0)✗2.4 |
| table | (5.0,2.0) | - | (4.3,2.5)✓ | (4.4,3.0)✓ |
| window | (1.0,5.0), (5.0,4.0) | - | (4.8,6.0)✗2.0, 漏1 | (6.7,6.0)✗2.6, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (3.0,2.0) | - | (2.9,2.0)✓ | (2.3,2.0)✓ |
| closet | (7.0,5.0) | - | (5.1,4.5)✓ | (4.6,5.0)✗2.4 |
| nightstand | (3.0,2.0) | - | (3.8,2.0)✓ | (4.5,2.0)✓ |
| table | (2.0,2.0) | - | (3.3,2.5)✓ | (2.0,3.0)✓ |
| window | (5.0,5.0), (1.0,4.0) | - | (4.8,6.0)✓, 漏1 | (2.6,6.0)✗2.5, 漏1 |

- **baseline 问题**：漏画 window ×1（GT 2，模型 1）；chair→closet 方向错（GT SW，模型 SE）；chair→nightstand 方向错（GT E，模型 SE）；chair-window 距离画错（GT 2.0，模型 5.0）；chair→window 方向错（GT E，模型 NE）；closet-nightstand 距离画错（GT 7.2，模型 2.2）；closet→table 方向错（GT N，模型 NW）；closet→window 方向错（GT NE，模型 N）
- **threeview 问题**：漏画 window ×1（GT 2，模型 1）；chair-closet 距离画错（GT 4.5，模型 6.1）；chair→closet 方向错（GT SW，模型 S）；chair→nightstand 方向错（GT E，模型 SE）；chair→table 方向错（GT N，模型 SW）；chair-window 距离画错（GT 2.0，模型 5.7）；chair→window 方向错（GT E，模型 SW）；closet-nightstand 距离画错（GT 7.2，模型 4.1）
- **threeview_3pass 问题**：漏画 window ×1（GT 2，模型 1）；chair→nightstand 方向错（GT E，模型 S）；chair→table 方向错（GT N，模型 W）；chair-window 距离画错（GT 2.0，模型 6.3）；chair→window 方向错（GT E，模型 W）；closet-nightstand 距离画错（GT 7.2，模型 3.2）；closet→nightstand 方向错（GT NE，模型 E）；closet-window 距离画错（GT 6.3，模型 5.0）

### 样本 119 `45260928`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (sofa, stool, table, tv) is the closest to the fireplace?

- QA：GT C | baseline D（错） | threeview D（错） | threeview_3pass D（错）
- 对齐：baseline: yaw=97° mirror=否 平移=(9.8,1.0) RMSE=1.39；threeview: yaw=87° mirror=否 平移=(8.4,0.3) RMSE=1.49；threeview_3pass: yaw=93° mirror=否 平移=(9.0,0.6) RMSE=1.55
- 补偿：baseline: 尺度=0.93 z偏移=+0.00；threeview: 尺度=1.04 z偏移=+0.50；threeview_3pass: 尺度=0.99 z偏移=+1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| fireplace | (7.0,4.0) | (7.0,5.7)✓ | (7.2,5.4)✓ | (6.8,5.5)✓ |
| sofa | (1.0,4.0) | (1.4,4.9)✓ | (1.5,5.7)✓ | (1.8,5.2)✓ |
| stool | (2.0,3.0) | (3.5,3.3)✓ | (4.0,3.0)✓ | (3.9,3.4)✓ |
| table | (7.0,7.0), (4.0,1.0) | (4.2,5.3)✗3.3, 漏1 | (4.1,5.6)✗3.2, 漏1 | (3.8,5.3)✗3.6, 漏1 |
| tv | (7.0,7.0) | (7.9,5.8)✓ | (7.2,5.4)✓ | (7.8,5.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| fireplace | (7.0,4.0) | - | (7.2,3.0)✓ | (6.8,3.0)✓ |
| sofa | (1.0,3.0) | - | (1.5,4.0)✓ | (1.8,3.0)✓ |
| stool | (2.0,2.0) | - | (4.0,2.5)✗2.0 | (3.9,2.5)✓ |
| table | (7.0,3.0), (4.0,3.0) | - | (4.1,2.5)✓, 漏1 | (3.8,2.5)✓, 漏1 |
| tv | (7.0,6.0) | - | (7.2,6.0)✓ | (7.8,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| fireplace | (4.0,4.0) | - | (5.4,3.0)✓ | (5.5,3.0)✓ |
| sofa | (4.0,3.0) | - | (5.7,4.0)✓ | (5.2,3.0)✓ |
| stool | (3.0,2.0) | - | (3.0,2.5)✓ | (3.4,2.5)✓ |
| table | (7.0,3.0), (1.0,3.0) | - | (5.6,2.5)✓, 漏1 | (5.3,2.5)✓, 漏1 |
| tv | (7.0,6.0) | - | (5.4,6.0)✓ | (5.6,6.0)✓ |

- **baseline 问题**：漏画 table ×1（GT 2，模型 1）；fireplace→stool 方向错（GT E，模型 NE）；fireplace-tv 距离画错（GT 3.0，模型 1.0）；fireplace→tv 方向错（GT S，模型 W）；sofa-stool 距离画错（GT 1.4，模型 2.8）；sofa-table 距离画错（GT 4.2，模型 3.0）；sofa→tv 方向错（GT SW，模型 W）；stool→table 方向错（GT W，模型 S）
- **threeview 问题**：漏画 table ×1（GT 2，模型 1）；fireplace-stool 距离画错（GT 5.1，模型 3.9）；fireplace→stool 方向错（GT E，模型 NE）；fireplace-tv 距离画错（GT 3.0，模型 0.0）；fireplace→tv 方向错（GT S，模型 E）；sofa-stool 距离画错（GT 1.4，模型 3.5）；sofa-table 距离画错（GT 4.2，模型 2.5）；sofa-tv 距离画错（GT 6.7，模型 5.5）
- **threeview_3pass 问题**：漏画 table ×1（GT 2，模型 1）；fireplace-stool 距离画错（GT 5.1，模型 3.6）；fireplace→stool 方向错（GT E，模型 NE）；fireplace-tv 距离画错（GT 3.0，模型 1.0）；fireplace→tv 方向错（GT S，模型 W）；sofa-stool 距离画错（GT 1.4，模型 2.8）；sofa-table 距离画错（GT 4.2，模型 2.0）；sofa→tv 方向错（GT SW，模型 W）

### 样本 120 `c50d2d1d42`（scannetpp · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (computer tower, door, trash can, ceiling light) is the closest to the telephone?

- QA：GT A | baseline A（对） | threeview A（对） | threeview_3pass B（错）
- 对齐：baseline: yaw=13° mirror=否 平移=(0.4,-3.9) RMSE=2.56；threeview: yaw=45° mirror=否 平移=(5.3,-2.6) RMSE=1.11；threeview_3pass: yaw=15° mirror=否 平移=(1.0,-3.9) RMSE=2.77
- 补偿：baseline: 尺度=0.36 z偏移=+0.00；threeview: 尺度=1.18 z偏移=-1.50；threeview_3pass: 尺度=0.28 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (3.0,6.0), (6.0,6.0), (6.0,2.0), (2.0,3.0) | (4.8,1.2)✓, 漏3 | (5.5,4.7)✓, 漏3 | (4.9,1.5)✓, 漏3 |
| computer tower | (5.0,3.0), (7.0,3.0), (7.0,5.0) | (5.3,3.5)✓, 漏2 | (4.7,3.0)✓, 漏2 | (5.3,3.4)✓, 漏2 |
| door | (0.0,3.0) | (3.0,2.2)✗3.1 | (-0.3,3.9)✓ | (3.5,2.3)✗3.6 |
| telephone | (7.0,3.0) | (4.7,3.0)✗2.3 | (5.5,3.0)✓ | (4.2,2.8)✗2.8 |
| trash can | (2.0,1.0), (3.0,1.0) | (5.2,4.2)✗3.8, 漏1 | (5.5,1.4)✗2.6, 漏1 | (5.1,3.9)✗3.6, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (3.0,8.0), (6.0,8.0), (6.0,7.0), (2.0,8.0) | - | (5.5,7.5)✓, 漏3 | (4.9,8.0)✓, 漏3 |
| computer tower | (5.0,1.0), (7.0,1.0), (7.0,1.0) | - | (4.7,2.0)✓, 漏2 | (5.3,2.0)✓, 漏2 |
| door | (0.0,3.0) | - | (-0.3,3.0)✓ | (3.5,3.0)✗3.5 |
| telephone | (7.0,3.0) | - | (5.5,3.0)✓ | (4.2,3.0)✗2.8 |
| trash can | (2.0,1.0), (3.0,1.0) | - | (5.5,0.0)✗2.7, 漏1 | (5.1,0.0)✗2.3, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (6.0,8.0), (6.0,8.0), (2.0,7.0), (3.0,8.0) | - | (4.7,7.5)✓, 漏3 | (1.5,8.0)✓, 漏3 |
| computer tower | (3.0,1.0), (3.0,1.0), (5.0,1.0) | - | (3.0,2.0)✓, 漏2 | (3.4,2.0)✓, 漏2 |
| door | (3.0,3.0) | - | (3.9,3.0)✓ | (2.3,3.0)✓ |
| telephone | (3.0,3.0) | - | (3.0,3.0)✓ | (2.8,3.0)✓ |
| trash can | (1.0,1.0), (1.0,1.0) | - | (1.4,0.0)✓, 漏1 | (3.9,0.0)✗3.1, 漏1 |

- **baseline 问题**：漏画 ceiling light ×3（GT 4，模型 1）；漏画 computer tower ×2（GT 3，模型 1）；漏画 trash can ×1（GT 2，模型 1）；ceiling light-computer tower 距离画错（GT 1.4，模型 6.7）；ceiling light→computer tower 方向错（GT W，模型 S）；ceiling light-door 距离画错（GT 2.0，模型 5.7）；ceiling light→door 方向错（GT E，模型 SE）；ceiling light-telephone 距离画错（GT 1.4，模型 5.1）
- **threeview 问题**：漏画 ceiling light ×3（GT 4，模型 1）；漏画 computer tower ×2（GT 3，模型 1）；漏画 trash can ×1（GT 2，模型 1）；ceiling light→computer tower 方向错（GT W，模型 NE）；ceiling light-door 距离画错（GT 2.0，模型 5.0）；ceiling light→telephone 方向错（GT NW，模型 N）；ceiling light→trash can 方向错（GT NE，模型 N）；computer tower→telephone 方向错（GT NW，模型 W）
- **threeview_3pass 问题**：漏画 ceiling light ×3（GT 4，模型 1）；漏画 computer tower ×2（GT 3，模型 1）；漏画 trash can ×1（GT 2，模型 1）；ceiling light-computer tower 距离画错（GT 1.4，模型 6.7）；ceiling light→computer tower 方向错（GT W，模型 S）；ceiling light-door 距离画错（GT 2.0，模型 5.7）；ceiling light→door 方向错（GT E，模型 SE）；ceiling light-telephone 距离画错（GT 1.4，模型 5.1）

### 样本 121 `scene0593_00`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (printer, window, table, sofa) is the closest to the fan?

- QA：GT A | baseline B（错） | threeview B（错） | threeview_3pass C（错）
- 对齐：baseline: yaw=-84° mirror=否 平移=(-1.0,8.1) RMSE=1.49；threeview: yaw=-55° mirror=是(未证实) 平移=(6.1,11.5) RMSE=2.28；threeview_3pass: yaw=-79° mirror=否 平移=(-1.3,8.1) RMSE=2.41
- 补偿：baseline: 尺度=0.95 z偏移=+0.00；threeview: 尺度=0.54 z偏移=-1.00；threeview_3pass: 尺度=0.47 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| fan | (3.0,6.0) | (2.5,3.5)✗2.6 | (4.5,4.7)✓ | (3.1,2.8)✗3.2 |
| printer | (2.0,7.0), (2.0,7.0) | (4.2,6.5)✗2.2, 漏1 | (4.3,6.8)✗2.3, 漏1 | (3.1,5.7)✓, 漏1 |
| sofa | (7.0,4.0) | (7.3,4.0)✓ | (4.9,5.0)✗2.3 | (5.6,4.7)✓ |
| table | (7.0,1.0) | (5.4,3.8)✗3.2 | (3.8,4.2)✗4.5 | (4.3,4.5)✗4.4 |
| window | (1.0,6.0), (1.0,3.0) | (0.7,3.3)✓, 漏1 | (2.5,3.3)✓, 漏1 | (3.9,6.3)✗2.9, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| fan | (3.0,2.0) | - | (4.5,7.5)✗5.7 | (3.1,4.0)✗2.0 |
| printer | (2.0,4.0), (2.0,4.0) | - | (4.3,1.5)✗3.4, 漏1 | (3.1,3.0)✓, 漏1 |
| sofa | (7.0,2.0) | - | (4.9,2.0)✗2.1 | (5.6,2.0)✓ |
| table | (7.0,2.0) | - | (3.8,0.5)✗3.5 | (4.3,2.0)✗2.7 |
| window | (1.0,5.0), (1.0,4.0) | - | (2.5,5.0)✓, 漏1 | (3.9,5.0)✗2.9, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| fan | (6.0,2.0) | - | (4.7,7.5)✗5.7 | (2.8,4.0)✗3.7 |
| printer | (7.0,4.0), (7.0,4.0) | - | (6.8,1.5)✗2.5, 漏1 | (5.7,3.0)✓, 漏1 |
| sofa | (4.0,2.0) | - | (5.0,2.0)✓ | (4.7,2.0)✓ |
| table | (1.0,2.0) | - | (4.2,0.5)✗3.5 | (4.5,2.0)✗3.5 |
| window | (6.0,5.0), (3.0,4.0) | - | (3.3,5.0)✓, 漏1 | (6.3,5.0)✓, 漏1 |

- **baseline 问题**：漏画 window ×1（GT 2，模型 1）；漏画 printer ×1（GT 2，模型 1）；fan-printer 距离画错（GT 1.4，模型 3.6）；fan→printer 方向错（GT SE，模型 SW）；fan→sofa 方向错（GT NW，模型 W）；fan-table 距离画错（GT 6.4，模型 3.0）；fan→table 方向错（GT NW，模型 W）；fan→window 方向错（GT NE，模型 E）
- **threeview 问题**：漏画 window ×1（GT 2，模型 1）；漏画 printer ×1（GT 2，模型 1）；fan-printer 距离画错（GT 1.4，模型 4.0）；fan→printer 方向错（GT SE，模型 S）；fan-sofa 距离画错（GT 4.5，模型 1.0）；fan→sofa 方向错（GT NW，模型 SW）；fan-table 距离画错（GT 6.4，模型 1.5）；fan→table 方向错（GT NW，模型 NE）
- **threeview_3pass 问题**：漏画 window ×1（GT 2，模型 1）；漏画 printer ×1（GT 2，模型 1）；fan-printer 距离画错（GT 1.4，模型 6.1）；fan→printer 方向错（GT SE，模型 S）；fan-sofa 距离画错（GT 4.5，模型 6.7）；fan→sofa 方向错（GT NW，模型 SW）；fan-table 距离画错（GT 6.4，模型 4.2）；fan→table 方向错（GT NW，模型 SW）

### 样本 122 `42899685`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (table, stool, tv, sofa) is the closest to the washer?

- QA：GT D | baseline C（错） | threeview D（对） | threeview_3pass None（错）
- 对齐：baseline: yaw=-82° mirror=是(未证实) 平移=(8.5,10.2) RMSE=1.25；threeview: yaw=-0° mirror=否 平移=(0.6,-0.5) RMSE=0.61；threeview_3pass: yaw=-1° mirror=否 平移=(0.6,0.1) RMSE=0.59
- 补偿：baseline: 尺度=0.65 z偏移=+0.00；threeview: 尺度=0.64 z偏移=+0.00；threeview_3pass: 尺度=0.65 z偏移=+0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (6.0,4.0), (7.0,5.0), (3.0,5.0) | (3.6,5.7)✓, 漏2 | (5.7,3.8)✓, 漏2 | (5.5,3.8)✓, 漏2 |
| stool | (4.0,5.0) | (3.0,5.0)✓ | 漏1 | (4.3,5.1)✓ |
| table | (5.0,5.0), (6.0,7.0), (1.0,7.0) | (4.4,4.5)✓, 漏2 | (5.7,5.3)✓, 漏2 | (5.6,5.1)✓, 漏2 |
| tv | (6.0,7.0), (1.0,7.0) | (6.3,4.8)✗2.2, 漏1 | (5.7,6.8)✓, 漏1 | (5.6,7.0)✓, 漏1 |
| washer | (6.0,1.0) | (6.6,2.9)✓ | 漏1 | 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (6.0,3.0), (7.0,3.0), (3.0,3.0) | - | (5.7,3.5)✓, 漏2 | (5.5,2.5)✓, 漏2 |
| stool | (4.0,2.0) | - | 漏1 | (4.3,2.5)✓ |
| table | (5.0,2.0), (6.0,2.0), (1.0,3.0) | - | (5.7,2.0)✓, 漏2 | (5.6,2.5)✓, 漏2 |
| tv | (6.0,6.0), (1.0,7.0) | - | (5.7,5.5)✓, 漏1 | (5.6,5.5)✓, 漏1 |
| washer | (6.0,3.0) | - | 漏1 | 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,3.0), (5.0,3.0), (5.0,3.0) | - | (3.8,3.5)✓, 漏2 | (3.8,2.5)✓, 漏2 |
| stool | (5.0,2.0) | - | 漏1 | (5.1,2.5)✓ |
| table | (5.0,2.0), (7.0,2.0), (7.0,3.0) | - | (5.3,2.0)✓, 漏2 | (5.1,2.5)✓, 漏2 |
| tv | (7.0,6.0), (7.0,7.0) | - | (6.8,5.5)✓, 漏1 | (7.0,5.5)✓, 漏1 |
| washer | (1.0,3.0) | - | 漏1 | 漏1 |

- **baseline 问题**：漏画 sofa ×2（GT 3，模型 1）；漏画 table ×2（GT 3，模型 1）；漏画 tv ×1（GT 2，模型 1）；sofa→stool 方向错（GT E，模型 NE）；sofa→table 方向错（GT SE，模型 NW）；sofa-tv 距离画错（GT 2.2，模型 4.5）；sofa→tv 方向错（GT SE，模型 W）；sofa-washer 距离画错（GT 3.0，模型 6.4）
- **threeview 问题**：漏画 stool ×1（GT 1，模型 0）；漏画 sofa ×2（GT 3，模型 1）；漏画 tv ×1（GT 2，模型 1）；漏画 table ×2（GT 3，模型 1）；漏画 washer ×1（GT 1，模型 0）；sofa→table 方向错（GT SE，模型 S）；sofa-tv 距离画错（GT 2.2，模型 4.7）；sofa→tv 方向错（GT SE，模型 S）
- **threeview_3pass 问题**：漏画 sofa ×2（GT 3，模型 1）；漏画 table ×2（GT 3，模型 1）；漏画 tv ×1（GT 2，模型 1）；漏画 washer ×1（GT 1，模型 0）；sofa-stool 距离画错（GT 1.0，模型 2.8）；sofa→stool 方向错（GT E，模型 SE）；sofa→table 方向错（GT SE，模型 S）；sofa-tv 距离画错（GT 2.2，模型 5.0）

### 样本 123 `bcd2436daf`（scannetpp · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (plant, ceiling light, heater, bed) is the closest to the chair?

- QA：GT D | baseline A（错） | threeview D（对） | threeview_3pass D（对）
- 对齐：baseline: yaw=-115° mirror=是(证据支持) 平移=(10.3,6.4) RMSE=1.60；threeview: yaw=-86° mirror=否 平移=(-2.1,9.0) RMSE=1.26；threeview_3pass: yaw=55° mirror=否 平移=(5.0,-2.1) RMSE=1.52
- 补偿：baseline: 尺度=0.54 z偏移=+0.00；threeview: 尺度=0.68 z偏移=-0.50；threeview_3pass: 尺度=0.57 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,5.0) | (3.0,4.5)✗2.1 | (3.2,4.5)✓ | (2.6,5.5)✗2.5 |
| ceiling light | (5.0,4.0) | (5.4,3.4)✓ | (3.2,4.5)✓ | (5.4,3.6)✓ |
| chair | (1.0,6.0) | (2.7,6.5)✓ | (1.8,6.1)✓ | (1.5,4.9)✓ |
| heater | (1.0,2.0) | (2.1,2.6)✓ | (2.7,2.0)✓ | (1.8,3.3)✓ |
| plant | (4.0,7.0) | (2.9,7.0)✓ | (5.1,7.0)✓ | (4.8,6.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,2.0) | - | (3.2,2.5)✓ | (2.6,2.0)✗2.4 |
| ceiling light | (5.0,8.0) | - | (3.2,8.0)✓ | (5.4,8.0)✓ |
| chair | (1.0,2.0) | - | (1.8,2.0)✓ | (1.5,2.0)✓ |
| heater | (1.0,2.0) | - | (2.7,1.5)✓ | (1.8,3.0)✓ |
| plant | (4.0,4.0) | - | (5.1,2.5)✓ | (4.8,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,2.0) | - | (4.5,2.5)✓ | (5.5,2.0)✓ |
| ceiling light | (4.0,8.0) | - | (4.5,8.0)✓ | (3.6,8.0)✓ |
| chair | (6.0,2.0) | - | (6.1,2.0)✓ | (4.9,2.0)✓ |
| heater | (2.0,2.0) | - | (2.0,1.5)✓ | (3.3,3.0)✓ |
| plant | (7.0,4.0) | - | (7.0,2.5)✓ | (6.7,3.0)✓ |

- **baseline 问题**：bed-ceiling light 距离画错（GT 1.0，模型 5.0）；bed→ceiling light 方向错（GT N，模型 NW）；bed→chair 方向错（GT E，模型 S）；bed-heater 距离画错（GT 5.0，模型 4.0）；bed-plant 距离画错（GT 2.2，模型 4.5）；bed→plant 方向错（GT SE，模型 S）；ceiling light-chair 距离画错（GT 4.5，模型 7.6）；ceiling light-heater 距离画错（GT 4.5，模型 6.4）
- **threeview 问题**：bed→ceiling light 方向错（GT N，模型 E）；bed→chair 方向错（GT E，模型 SE）；bed-heater 距离画错（GT 5.0，模型 3.6）；bed→heater 方向错（GT NE，模型 N）；bed-plant 距离画错（GT 2.2，模型 4.6）；bed→plant 方向错（GT SE，模型 SW）；ceiling light-chair 距离画错（GT 4.5，模型 3.2）；ceiling light→heater 方向错（GT NE，模型 N）
- **threeview_3pass 问题**：bed-ceiling light 距离画错（GT 1.0，模型 6.0）；bed→ceiling light 方向错（GT N，模型 NW）；bed-chair 距离画错（GT 4.1，模型 2.2）；bed→chair 方向错（GT E，模型 NE）；bed→heater 方向错（GT NE，模型 N）；bed-plant 距离画错（GT 2.2，模型 4.5）；bed→plant 方向错（GT SE，模型 SW）；ceiling light-chair 距离画错（GT 4.5，模型 7.3）

### 样本 124 `scene0608_00`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (tv, pillow, guitar, lamp) is the closest to the door?

- QA：GT B | baseline C（错） | threeview D（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=-120° mirror=否 平移=(1.5,10.9) RMSE=2.56；threeview: yaw=50° mirror=是(证据支持) 平移=(-3.2,4.0) RMSE=1.15；threeview_3pass: yaw=-141° mirror=否 平移=(3.4,9.7) RMSE=1.62
- 补偿：baseline: 尺度=0.24 z偏移=+0.00；threeview: 尺度=0.70 z偏移=-1.00；threeview_3pass: 尺度=0.59 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,1.0) | (2.0,3.4)✗2.6 | (1.6,2.0)✓ | (0.9,1.7)✓ |
| guitar | (5.0,6.0) | (2.7,3.2)✗3.6 | (4.4,6.4)✓ | (5.0,4.2)✓ |
| lamp | (5.0,2.0) | (4.1,4.1)✗2.3 | (3.6,1.7)✓ | (3.8,4.7)✗3.0 |
| pillow | (2.0,4.0), (1.0,3.0) | (3.5,4.2)✓, 漏1 | (3.7,2.9)✗2.0, 漏1 | (3.7,3.9)✓, 漏1 |
| tv | (2.0,6.0) | (2.7,4.1)✗2.0 | (1.7,6.0)✓ | (1.7,4.5)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,5.0) | - | (1.6,3.5)✓ | (0.9,3.0)✗2.0 |
| guitar | (5.0,2.0) | - | (4.4,3.5)✓ | (5.0,3.0)✓ |
| lamp | (5.0,4.0) | - | (3.6,4.0)✓ | (3.8,4.0)✓ |
| pillow | (2.0,3.0), (1.0,4.0) | - | (3.7,2.5)✓, 漏1 | (3.7,2.0)✓, 漏1 |
| tv | (2.0,4.0) | - | (1.7,5.0)✓ | (1.7,4.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,5.0) | - | (2.0,3.5)✓ | (1.7,3.0)✗2.1 |
| guitar | (6.0,2.0) | - | (6.4,3.5)✓ | (4.2,3.0)✗2.1 |
| lamp | (2.0,4.0) | - | (1.7,4.0)✓ | (4.7,4.0)✗2.7 |
| pillow | (4.0,3.0), (3.0,4.0) | - | (2.9,2.5)✓, 漏1 | (3.9,2.0)✓, 漏1 |
| tv | (6.0,4.0) | - | (6.0,5.0)✓ | (4.5,4.0)✓ |

- **baseline 问题**：漏画 pillow ×1（GT 2，模型 1）；door-guitar 距离画错（GT 6.4，模型 3.2）；door→guitar 方向错（GT SW，模型 W）；door-lamp 距离画错（GT 4.1，模型 9.2）；door-pillow 距离画错（GT 2.0，模型 7.2）；door→pillow 方向错（GT S，模型 SW）；door→tv 方向错（GT S，模型 SW）；guitar-lamp 距离画错（GT 4.0，模型 6.7）
- **threeview 问题**：漏画 pillow ×1（GT 2，模型 1）；door-guitar 距离画错（GT 6.4，模型 7.6）；door-lamp 距离画错（GT 4.1，模型 2.9）；door-pillow 距离画错（GT 2.0，模型 3.4）；door→pillow 方向错（GT S，模型 SW）；guitar-lamp 距离画错（GT 4.0，模型 6.9）；guitar-pillow 距离画错（GT 3.6，模型 5.1）；guitar→pillow 方向错（GT NE，模型 N）
- **threeview_3pass 问题**：漏画 pillow ×1（GT 2，模型 1）；door-guitar 距离画错（GT 6.4，模型 8.1）；door-lamp 距离画错（GT 4.1，模型 7.1）；door→lamp 方向错（GT W，模型 SW）；door-pillow 距离画错（GT 2.0，模型 6.0）；door→pillow 方向错（GT S，模型 SW）；guitar-lamp 距离画错（GT 4.0，模型 2.2）；guitar→lamp 方向错（GT N，模型 SE）

### 样本 125 `47334096`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (stool, table, chair, sofa) is the closest to the tv?

- QA：GT B | baseline B（对） | threeview B（对） | threeview_3pass B（对）
- 对齐：baseline: yaw=-79° mirror=否 平移=(-1.7,9.8) RMSE=1.45；threeview: yaw=-97° mirror=是(未证实) 平移=(9.4,9.4) RMSE=1.21；threeview_3pass: yaw=45° mirror=否 平移=(3.6,-1.3) RMSE=1.56
- 补偿：baseline: 尺度=0.44 z偏移=+0.00；threeview: 尺度=0.60 z偏移=-0.65；threeview_3pass: 尺度=0.38 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (5.0,6.0), (5.0,7.0), (6.0,7.0), (6.0,7.0), (3.0,7.0) | (3.7,6.7)✓, (3.7,6.7)✓, (4.0,5.0)多, 漏3 | (3.5,6.8)✓, 漏4 | (4.1,6.3)✓, (3.1,5.3)✓, 漏3 |
| sofa | (4.0,4.0) | (4.7,6.0)✗2.2 | (4.8,5.2)✓ | (4.4,5.0)✓ |
| stool | (5.0,1.0) | 漏1 | 漏1 | 漏1 |
| table | (5.0,7.0), (1.0,5.0) | (3.4,5.8)✗2.0, 漏1 | (3.3,5.4)✗2.3, 漏1 | (3.6,5.8)✓, 漏1 |
| tv | (1.0,5.0) | (2.1,5.5)✓ | (1.5,5.6)✓ | (2.8,6.6)✗2.4 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (5.0,3.0), (5.0,3.0), (6.0,3.0), (6.0,3.0), (3.0,5.0) | - | (3.5,3.1)✓, 漏4 | (4.1,2.0)✓, (3.1,2.0)✗2.2, 漏3 |
| sofa | (4.0,2.0) | - | (4.8,3.4)✓ | (4.4,2.0)✓ |
| stool | (5.0,2.0) | - | 漏1 | 漏1 |
| table | (5.0,2.0), (1.0,1.0) | - | (3.3,1.9)✓, 漏1 | (3.6,2.0)✓, 漏1 |
| tv | (1.0,6.0) | - | (1.5,5.3)✓ | (2.8,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (6.0,3.0), (7.0,3.0), (7.0,3.0), (7.0,3.0), (7.0,5.0) | - | (6.8,3.1)✓, 漏4 | (6.3,2.0)✓, (5.3,2.0)✗2.0, 漏3 |
| sofa | (4.0,2.0) | - | (5.2,3.4)✓ | (5.0,2.0)✓ |
| stool | (1.0,2.0) | - | 漏1 | 漏1 |
| table | (7.0,2.0), (5.0,1.0) | - | (5.4,1.9)✓, 漏1 | (5.8,2.0)✓, 漏1 |
| tv | (5.0,6.0) | - | (5.6,5.3)✓ | (6.6,6.0)✓ |

- **baseline 问题**：漏画 stool ×1（GT 1，模型 0）；漏画 table ×1（GT 2，模型 1）；漏画 chair ×3（GT 5，模型 2）；chair→sofa 方向错（GT N，模型 W）；chair-table 距离画错（GT 0.0，模型 2.2）；chair-tv 距离画错（GT 2.8，模型 4.5）；chair→tv 方向错（GT NE，模型 E）；sofa→table 方向错（GT SE，模型 E）
- **threeview 问题**：漏画 stool ×1（GT 1，模型 0）；漏画 table ×1（GT 2，模型 1）；漏画 chair ×4（GT 5，模型 1）；chair-sofa 距离画错（GT 2.2，模型 3.5）；chair→sofa 方向错（GT N，模型 NW）；chair-table 距离画错（GT 0.0，模型 2.5）；chair→table 方向错（GT E，模型 N）；chair-tv 距离画错（GT 2.8，模型 3.9）
- **threeview_3pass 问题**：漏画 stool ×1（GT 1，模型 0）；漏画 table ×1（GT 2，模型 1）；漏画 chair ×3（GT 5，模型 2）；chair-sofa 距离画错（GT 2.2，模型 3.6）；chair→sofa 方向错（GT N，模型 NW）；chair-table 距离画错（GT 0.0，模型 2.0）；chair→tv 方向错（GT NE，模型 SE）；sofa-tv 距离画错（GT 3.2，模型 6.0）

### 样本 126 `47331970`（arkitscenes · object_rel_direction_easy）

Q：If I am standing by the refrigerator and facing the table, is the dishwasher to the left or the right of the table?

- QA：GT A | baseline B（错） | threeview B（错） | threeview_3pass A（对）
- 对齐：baseline: yaw=95° mirror=否 平移=(7.6,-0.2) RMSE=0.94；threeview: yaw=144° mirror=是(证据支持) 平移=(3.5,-2.6) RMSE=0.95；threeview_3pass: yaw=116° mirror=否 平移=(8.4,1.7) RMSE=1.08
- 补偿：baseline: 尺度=0.55 z偏移=+0.00；threeview: 尺度=0.54 z偏移=-0.50；threeview_3pass: 尺度=0.49 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| dishwasher | (1.0,3.0) | (2.2,2.5)✓ | (1.5,2.1)✓ | (0.7,2.2)✓ |
| refrigerator | (3.0,1.0) | (2.3,1.4)✓ | (2.4,1.5)✓ | (2.5,2.0)✓ |
| table | (2.0,4.0) | (1.5,4.1)✓ | (2.1,4.4)✓ | (2.7,3.8)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| dishwasher | (1.0,2.0) | - | (1.5,2.0)✓ | (0.7,2.0)✓ |
| refrigerator | (3.0,4.0) | - | (2.4,4.5)✓ | (2.5,5.0)✓ |
| table | (2.0,2.0) | - | (2.1,1.5)✓ | (2.7,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| dishwasher | (3.0,2.0) | - | (2.1,2.0)✓ | (2.2,2.0)✓ |
| refrigerator | (1.0,4.0) | - | (1.5,4.5)✓ | (2.0,5.0)✓ |
| table | (4.0,2.0) | - | (4.4,1.5)✓ | (3.8,2.0)✓ |

- **baseline 问题**：dishwasher→refrigerator 方向错（GT NW，模型 N）；dishwasher-table 距离画错（GT 1.4，模型 3.2）；dishwasher→table 方向错（GT SW，模型 SE）；refrigerator-table 距离画错（GT 3.2，模型 5.1）
- **threeview 问题**：dishwasher-table 距离画错（GT 1.4，模型 4.3）；dishwasher→table 方向错（GT SW，模型 S）；refrigerator-table 距离画错（GT 3.2，模型 5.3）；z 整体偏高（平均 +0.5 格）
- **threeview_3pass 问题**：dishwasher→refrigerator 方向错（GT NW，模型 W）；dishwasher-table 距离画错（GT 1.4，模型 5.1）

### 样本 127 `bcd2436daf`（scannetpp · object_rel_direction_easy）

Q：If I am standing by the heater and facing the pillow, is the ceiling light to the left or the right of the pillow?

- QA：GT A | baseline A（对） | threeview B（错） | threeview_3pass A（对）
- 对齐：baseline: yaw=-111° mirror=是(未证实) 平移=(10.7,7.3) RMSE=1.63；threeview: yaw=38° mirror=是(未证实) 平移=(-2.7,4.6) RMSE=0.39；threeview_3pass: yaw=-110° mirror=否 平移=(2.2,10.6) RMSE=0.36
- 补偿：baseline: 尺度=0.54 z偏移=+0.00；threeview: 尺度=0.96 z偏移=-0.50；threeview_3pass: 尺度=1.17 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (5.0,4.0) | (6.0,3.5)✓ | (4.3,3.7)✓ | (5.4,4.2)✓ |
| heater | (1.0,2.0) | (1.9,3.4)✓ | (1.4,2.0)✓ | (0.9,2.1)✓ |
| pillow | (5.0,6.0) | (3.4,5.7)✓, (3.2,5.2)多, 多1 | (5.3,6.3)✓ | (4.7,5.7)✓, (5.1,6.8)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (5.0,8.0) | - | (4.3,9.0)✓ | (5.4,9.0)✓ |
| heater | (1.0,2.0) | - | (1.4,2.0)✓ | (0.9,2.0)✓ |
| pillow | (5.0,3.0) | - | (5.3,2.5)✓ | (5.1,3.0)✓, (4.7,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (4.0,8.0) | - | (3.7,9.0)✓ | (4.2,9.0)✓ |
| heater | (2.0,2.0) | - | (2.0,2.0)✓ | (2.1,2.0)✓ |
| pillow | (6.0,3.0) | - | (6.3,2.5)✓ | (5.7,3.0)✓, (6.8,3.0)多, 多1 |

- **baseline 问题**：多画 pillow ×1（GT 1，模型 2）；ceiling light-heater 距离画错（GT 4.5，模型 7.6）；ceiling light→heater 方向错（GT NE，模型 E）；ceiling light-pillow 距离画错（GT 2.0，模型 6.1）；ceiling light→pillow 方向错（GT S，模型 SE）；heater-pillow 距离画错（GT 5.7，模型 4.1）
- **threeview 问题**：z 整体偏高（平均 +0.7 格）
- **threeview_3pass 问题**：多画 pillow ×1（GT 1，模型 2）；heater-pillow 距离画错（GT 5.7，模型 4.5）

### 样本 128 `scene0629_01`（scannet · object_rel_direction_easy）

Q：If I am standing by the chair and facing the bed, is the mirror to the left or the right of the bed?

- QA：GT A | baseline B（错） | threeview A（对） | threeview_3pass A（对）
- 对齐：baseline: yaw=-33° mirror=否 平移=(-0.2,2.1) RMSE=0.41；threeview: yaw=-172° mirror=否 平移=(9.7,10.7) RMSE=1.32；threeview_3pass: yaw=-36° mirror=否 平移=(-0.4,2.8) RMSE=0.47
- 补偿：baseline: 尺度=0.92 z偏移=+0.00；threeview: 尺度=0.57 z偏移=-0.50；threeview_3pass: 尺度=0.86 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (7.0,4.0) | (6.6,3.7)✓ | (5.4,5.3)✗2.1 | (6.4,4.2)✓ |
| chair | (6.0,7.0) | (5.8,7.5)✓ | (6.9,6.7)✓ | (6.5,7.3)✓ |
| mirror | (3.0,6.0) | (3.5,5.7)✓ | (3.7,5.0)✓ | (3.1,5.5)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (7.0,3.0) | - | (5.4,2.5)✓ | (6.4,2.0)✓ |
| chair | (6.0,2.0) | - | (6.9,2.0)✓ | (6.5,2.0)✓ |
| mirror | (3.0,4.0) | - | (3.7,5.5)✓ | (3.1,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (4.0,3.0) | - | (5.3,2.5)✓ | (4.2,2.0)✓ |
| chair | (7.0,2.0) | - | (6.7,2.0)✓ | (7.3,2.0)✓ |
| mirror | (6.0,4.0) | - | (5.0,5.5)✓ | (5.5,5.0)✓ |

- **baseline 问题**：bed-chair 距离画错（GT 3.2，模型 4.2）；chair→mirror 方向错（GT E，模型 NE）
- **threeview 问题**：bed→chair 方向错（GT S，模型 SW）；bed-mirror 距离画错（GT 4.5，模型 3.0）；bed→mirror 方向错（GT SE，模型 E）；chair-mirror 距离画错（GT 3.2，模型 6.3）；chair→mirror 方向错（GT E，模型 NE）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：bed→mirror 方向错（GT SE，模型 E）；chair-mirror 距离画错（GT 3.2，模型 4.5）；chair→mirror 方向错（GT E，模型 NE）

### 样本 129 `42899696`（arkitscenes · object_rel_direction_medium）

Q：If I am standing by the bed and facing the stool, is the tv to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT A | baseline B（错） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=-41° mirror=是(未证实) 平移=(4.5,11.5) RMSE=1.30；threeview: yaw=-43° mirror=是(未证实) 平移=(4.5,10.9) RMSE=1.24；threeview_3pass: yaw=137° mirror=否 平移=(11.9,4.0) RMSE=1.46
- 补偿：baseline: 尺度=0.58 z偏移=+0.00；threeview: 尺度=0.59 z偏移=-0.50；threeview_3pass: 尺度=0.51 z偏移=+1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,3.0) | (4.4,4.1)✓ | (4.6,4.2)✓ | (4.6,4.2)✓ |
| stool | (2.0,5.0) | (2.8,4.0)✓ | (2.5,4.1)✓ | (2.4,4.1)✓ |
| tv | (5.0,6.0) | (5.9,5.9)✓ | (6.0,5.7)✓ | (6.0,5.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,3.0) | - | (4.6,3.0)✓ | (4.6,3.0)✓ |
| stool | (2.0,1.0) | - | (2.5,1.5)✓ | (2.4,2.0)✓ |
| tv | (5.0,7.0) | - | (6.0,5.5)✓ | (6.0,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (3.0,3.0) | - | (4.2,3.0)✓ | (4.2,3.0)✓ |
| stool | (5.0,1.0) | - | (4.1,1.5)✓ | (4.1,2.0)✓ |
| tv | (6.0,7.0) | - | (5.7,5.5)✓ | (5.7,6.0)✓ |

- **baseline 问题**：bed-stool 距离画错（GT 4.5，模型 2.8）；bed→stool 方向错（GT SE，模型 E）；bed→tv 方向错（GT S，模型 SW）；stool-tv 距离画错（GT 3.2，模型 6.3）；stool→tv 方向错（GT W，模型 SW）
- **threeview 问题**：bed→stool 方向错（GT SE，模型 E）；bed→tv 方向错（GT S，模型 SW）；stool-tv 距离画错（GT 3.2，模型 6.5）；stool→tv 方向错（GT W，模型 SW）
- **threeview_3pass 问题**：bed→stool 方向错（GT SE，模型 E）；bed→tv 方向错（GT S，模型 SW）；stool-tv 距离画错（GT 3.2，模型 7.6）；stool→tv 方向错（GT W，模型 SW）；z 整体偏低（平均 -1.0 格）

### 样本 130 `e398684d27`（scannetpp · object_rel_direction_medium）

Q：If I am standing by the ceiling light and facing the monitor, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT A | baseline A（对） | threeview C（错） | threeview_3pass A（对）
- 对齐：baseline: yaw=66° mirror=否 平移=(4.9,-0.6) RMSE=0.38；threeview: yaw=50° mirror=是(证据支持) 平移=(-3.3,4.6) RMSE=1.40；threeview_3pass: yaw=71° mirror=否 平移=(4.9,-0.3) RMSE=0.66
- 补偿：baseline: 尺度=1.08 z偏移=+0.00；threeview: 尺度=1.27 z偏移=-1.00；threeview_3pass: 尺度=1.13 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (6.0,4.0) | (6.2,4.4)✓ | (4.1,5.4)✗2.3 | (6.0,4.8)✓ |
| door | (1.0,2.0) | (0.5,2.1)✓ | (0.8,1.5)✓ | (0.2,2.0)✓ |
| monitor | (1.0,7.0) | (1.3,6.5)✓ | (3.1,6.2)✗2.3 | (1.8,6.2)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (6.0,8.0) | - | (4.1,8.0)✓ | (6.0,8.0)✓ |
| door | (1.0,2.0) | - | (0.8,3.5)✓ | (0.2,3.0)✓ |
| monitor | (1.0,5.0) | - | (3.1,2.5)✗3.3 | (1.8,4.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (4.0,8.0) | - | (5.4,8.0)✓ | (4.8,8.0)✓ |
| door | (2.0,2.0) | - | (1.5,3.5)✓ | (2.0,3.0)✓ |
| monitor | (7.0,5.0) | - | (6.2,2.5)✗2.6 | (6.2,4.0)✓ |

- **threeview 问题**：ceiling light-door 距离画错（GT 5.4，模型 4.0）；ceiling light→door 方向错（GT E，模型 NE）；ceiling light-monitor 距离画错（GT 5.8，模型 1.0）；door→monitor 方向错（GT S，模型 SW）；z 整体偏高（平均 +0.7 格）
- **threeview_3pass 问题**：ceiling light→door 方向错（GT E，模型 NE）；ceiling light-monitor 距离画错（GT 5.8，模型 4.0）；ceiling light→monitor 方向错（GT SE，模型 E）；door-monitor 距离画错（GT 5.0，模型 4.0）；z 整体偏高（平均 +1.0 格）

### 样本 131 `scene0700_02`（scannet · object_rel_direction_medium）

Q：If I am standing by the window and facing the telephone, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT A | baseline A（对） | threeview B（错） | threeview_3pass A（对）
- 对齐：baseline: yaw=62° mirror=否 平移=(5.8,-0.6) RMSE=0.75；threeview: yaw=67° mirror=是(未证实) 平移=(-3.2,3.4) RMSE=0.92；threeview_3pass: yaw=54° mirror=否 平移=(5.3,-1.7) RMSE=0.95
- 补偿：baseline: 尺度=1.06 z偏移=+0.00；threeview: 尺度=1.01 z偏移=-0.50；threeview_3pass: 尺度=0.90 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,2.0) | (1.7,2.5)✓ | (2.0,2.8)✓ | (2.1,2.2)✓ |
| telephone | (5.0,6.0) | (3.7,6.2)✓ | (3.4,6.0)✓ | (4.5,7.2)✓ |
| window | (7.0,5.0) | (7.5,4.2)✓ | (7.6,4.2)✓ | (6.4,3.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,4.0) | - | (2.0,4.0)✓ | (2.1,4.0)✓ |
| telephone | (5.0,4.0) | - | (3.4,3.0)✓ | (4.5,4.0)✓ |
| window | (7.0,5.0) | - | (7.6,5.5)✓ | (6.4,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (2.0,4.0) | - | (2.8,4.0)✓ | (2.2,4.0)✓ |
| telephone | (6.0,4.0) | - | (6.0,3.0)✓ | (7.2,4.0)✓ |
| window | (5.0,5.0) | - | (4.2,5.5)✓ | (3.6,5.0)✓ |

- **baseline 问题**：door-telephone 距离画错（GT 5.7，模型 4.0）；door-window 距离画错（GT 6.7，模型 5.7）；door→window 方向错（GT SW，模型 W）；telephone-window 距离画错（GT 2.2，模型 4.0）
- **threeview 问题**：door-telephone 距离画错（GT 5.7，模型 3.5）；door-window 距离画错（GT 6.7，模型 5.7）；door→window 方向错（GT SW，模型 W）；telephone-window 距离画错（GT 2.2，模型 4.5）
- **threeview_3pass 问题**：door-window 距离画错（GT 6.7，模型 5.0）；door→window 方向错（GT SW，模型 W）；telephone-window 距离画错（GT 2.2，模型 4.5）

### 样本 132 `47430038`（arkitscenes · object_rel_direction_medium）

Q：If I am standing by the refrigerator and facing the table, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT B | baseline C（错） | threeview B（对） | threeview_3pass B（对）
- 对齐：baseline: yaw=-33° mirror=否 平移=(-2.8,2.8) RMSE=0.79；threeview: yaw=-26° mirror=否 平移=(-2.2,2.4) RMSE=0.89；threeview_3pass: yaw=-36° mirror=否 平移=(-2.5,3.7) RMSE=0.74
- 补偿：baseline: 尺度=1.24 z偏移=+0.00；threeview: 尺度=1.08 z偏移=-0.50；threeview_3pass: 尺度=1.07 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (1.0,6.0) | (0.5,5.2)✓ | (0.4,4.9)✓ | (0.7,4.9)✓ |
| stove | (3.0,1.0) | (2.9,2.2)✓ | (2.9,2.6)✓ | (2.6,2.2)✓ |
| table | (6.0,6.0) | (6.6,5.6)✓ | (6.7,5.5)✓ | (6.7,5.9)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (1.0,4.0) | - | (0.4,4.5)✓ | (0.7,4.0)✓ |
| stove | (3.0,4.0) | - | (2.9,2.5)✓ | (2.6,2.0)✗2.0 |
| table | (6.0,2.0) | - | (6.7,2.0)✓ | (6.7,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (6.0,4.0) | - | (4.9,4.5)✓ | (4.9,4.0)✓ |
| stove | (1.0,4.0) | - | (2.6,2.5)✗2.2 | (2.2,2.0)✗2.3 |
| table | (6.0,2.0) | - | (5.5,2.0)✓ | (5.9,2.0)✓ |

- **baseline 问题**：refrigerator-stove 距离画错（GT 5.4，模型 3.2）；refrigerator→stove 方向错（GT N，模型 NW）；stove-table 距离画错（GT 5.8，模型 4.1）
- **threeview 问题**：refrigerator-stove 距离画错（GT 5.4，模型 3.2）；refrigerator→stove 方向错（GT N，模型 NW）；stove-table 距离画错（GT 5.8，模型 4.5）
- **threeview_3pass 问题**：refrigerator-stove 距离画错（GT 5.4，模型 3.2）；refrigerator→stove 方向错（GT N，模型 NW）；z 整体偏低（平均 -0.7 格）

### 样本 133 `5942004064`（scannetpp · object_rel_direction_hard）

Q：If I am standing by the chair and facing the sofa, is the tv to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT D | baseline None（错） | threeview D（对） | threeview_3pass None（错）
- 对齐：baseline: yaw=-104° mirror=否 平移=(2.5,12.5) RMSE=0.61；threeview: yaw=77° mirror=否 平移=(9.5,0.8) RMSE=0.94；threeview_3pass: yaw=-104° mirror=否 平移=(2.5,12.5) RMSE=0.61
- 补偿：baseline: 尺度=0.61 z偏移=+0.00；threeview: 尺度=0.48 z偏移=-0.50；threeview_3pass: 尺度=0.61 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (6.0,5.0) | (5.5,5.1)✓, (6.1,7.5)多, 多1 | (5.5,5.1)✓ | (5.5,5.1)✓, (6.1,7.5)多, 多1 |
| sofa | (6.0,6.0) | (6.4,6.1)✓ | (6.4,6.2)✓ | (6.4,6.1)✓ |
| tv | (4.0,7.0) | (4.1,6.7)✓ | (4.1,6.7)✓ | (4.1,6.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (6.0,2.0) | - | (5.5,2.0)✓ | (6.1,2.0)✓, (5.5,2.0)多, 多1 |
| sofa | (6.0,2.0) | - | (6.4,2.0)✓ | (6.4,2.0)✓ |
| tv | (4.0,3.0) | - | (4.1,4.5)✓ | (4.1,5.0)✗2.0 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (5.0,2.0) | - | (5.1,2.0)✓ | (5.1,2.0)✓, (7.5,2.0)多, 多1 |
| sofa | (6.0,2.0) | - | (6.2,2.0)✓ | (6.1,2.0)✓ |
| tv | (7.0,3.0) | - | (6.7,4.5)✓ | (6.7,5.0)✗2.0 |

- **baseline 问题**：多画 chair ×1（GT 1，模型 2）；chair-sofa 距离画错（GT 1.0，模型 2.2）；chair→sofa 方向错（GT S，模型 W）；chair→tv 方向错（GT SE，模型 E）；sofa-tv 距离画错（GT 2.2，模型 4.0）；sofa→tv 方向错（GT SE，模型 E）
- **threeview 问题**：chair-sofa 距离画错（GT 1.0，模型 2.9）；chair→sofa 方向错（GT S，模型 SW）；chair-tv 距离画错（GT 2.8，模型 4.3）；sofa-tv 距离画错（GT 2.2，模型 5.0）；sofa→tv 方向错（GT SE，模型 E）；z 整体偏高（平均 +1.0 格）
- **threeview_3pass 问题**：多画 chair ×1（GT 1，模型 2）；chair-sofa 距离画错（GT 1.0，模型 2.2）；chair→sofa 方向错（GT S，模型 W）；chair→tv 方向错（GT SE，模型 E）；sofa-tv 距离画错（GT 2.2，模型 4.0）；sofa→tv 方向错（GT SE，模型 E）；z 整体偏高（平均 +0.7 格）

### 样本 134 `scene0328_00`（scannet · object_rel_direction_medium）

Q：If I am standing by the refrigerator and facing the window, is the oven to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT B | baseline A（错） | threeview A（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=-176° mirror=否 平移=(8.0,8.9) RMSE=0.45；threeview: yaw=-149° mirror=是(未证实) 平移=(10.9,1.3) RMSE=0.71；threeview_3pass: yaw=-177° mirror=否 平移=(8.0,8.9) RMSE=0.94
- 补偿：baseline: 尺度=0.97 z偏移=+0.00；threeview: 尺度=0.85 z偏移=-0.50；threeview_3pass: 尺度=0.72 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| oven | (3.0,2.0) | (3.5,1.7)✓ | (4.0,2.6)✓ | (3.8,1.6)✓ |
| refrigerator | (7.0,4.0) | (6.3,3.8)✓ | (6.6,3.2)✓ | (5.8,3.8)✓ |
| window | (3.0,6.0) | (3.2,6.5)✓ | (2.4,6.1)✓ | (3.5,6.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| oven | (3.0,2.0) | - | (4.0,2.0)✓ | (3.8,2.0)✓ |
| refrigerator | (7.0,3.0) | - | (6.6,4.5)✓ | (5.8,4.0)✓ |
| window | (3.0,6.0) | - | (2.4,6.0)✓ | (3.5,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| oven | (2.0,2.0) | - | (2.6,2.0)✓ | (1.6,2.0)✓ |
| refrigerator | (4.0,3.0) | - | (3.2,4.5)✓ | (3.8,4.0)✓ |
| window | (6.0,6.0) | - | (6.1,6.0)✓ | (6.6,6.0)✓ |

- **threeview 问题**：oven-refrigerator 距离画错（GT 4.5，模型 3.2）；oven→refrigerator 方向错（GT SW，模型 W）；oven→window 方向错（GT S，模型 SE）；refrigerator-window 距离画错（GT 4.5，模型 6.0）；z 整体偏高（平均 +1.0 格）
- **threeview_3pass 问题**：oven-window 距离画错（GT 4.0，模型 7.0）

### 样本 135 `42898527`（arkitscenes · object_rel_direction_hard）

Q：If I am standing by the washer and facing the stove, is the refrigerator to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT B | baseline B（对） | threeview B（对） | threeview_3pass D（错）
- 对齐：baseline: yaw=-133° mirror=否 平移=(3.0,10.3) RMSE=1.16；threeview: 2点 yaw=-99° mirror=否 平移=(-0.3,8.7) RMSE=1.09；threeview_3pass: yaw=-102° mirror=是(未证实) 平移=(9.9,7.6) RMSE=1.09
- 补偿：baseline: 尺度=0.91 z偏移=+0.00；threeview: 尺度=2.03 z偏移=+0.00；threeview_3pass: 尺度=0.85 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (4.0,7.0) | (4.3,5.9)✓ | (4.0,7.0)✓ | (4.3,6.2)✓ |
| stove | (3.0,1.0) | (3.1,3.2)✗2.3 | (3.0,1.0)✓ | (2.8,3.1)✗2.1 |
| washer | (1.0,3.0) | (0.6,1.9)✓ | 漏1 | (0.8,1.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (4.0,4.0) | - | (4.0,5.0)✓ | (4.3,5.0)✓ |
| stove | (3.0,4.0) | - | (3.0,3.0)✓ | (2.8,2.0)✗2.0 |
| washer | (1.0,2.0) | - | 漏1 | (0.8,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (7.0,4.0) | - | (7.0,5.0)✓ | (6.2,5.0)✓ |
| stove | (1.0,4.0) | - | (1.0,3.0)✓ | (3.1,2.0)✗2.9 |
| washer | (3.0,2.0) | - | 漏1 | (1.7,2.0)✓ |

- **baseline 问题**：refrigerator-stove 距离画错（GT 6.1，模型 3.2）；refrigerator→stove 方向错（GT N，模型 NE）；refrigerator-washer 距离画错（GT 5.0，模型 6.0）；stove→washer 方向错（GT SE，模型 NE）
- **threeview 问题**：漏画 washer ×1（GT 1，模型 0）；refrigerator-stove 距离画错（GT 6.1，模型 3.0）
- **threeview_3pass 问题**：refrigerator-stove 距离画错（GT 6.1，模型 4.1）；refrigerator→stove 方向错（GT N，模型 NE）；refrigerator-washer 距离画错（GT 5.0，模型 6.7）；stove→washer 方向错（GT SE，模型 NE）

### 样本 136 `25f3b7a318`（scannetpp · object_rel_direction_hard）

Q：If I am standing by the table and facing the door, is the bed to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT D | baseline C（错） | threeview C（错） | threeview_3pass D（对）
- 对齐：baseline: yaw=-125° mirror=否 平移=(3.0,11.9) RMSE=1.63；threeview: yaw=-68° mirror=是(未证实) 平移=(8.4,9.3) RMSE=0.73；threeview_3pass: yaw=46° mirror=否 平移=(5.0,-2.9) RMSE=1.19
- 补偿：baseline: 尺度=0.77 z偏移=+0.00；threeview: 尺度=1.33 z偏移=-1.00；threeview_3pass: 尺度=0.89 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,2.0) | (4.1,4.9)✗3.0 | (5.6,2.0)✓ | (4.8,4.3)✗2.3 |
| door | (0.0,5.0) | (0.5,3.7)✓ | (-0.1,5.4)✓ | (-0.2,4.2)✓ |
| table | (7.0,7.0) | (7.4,5.4)✓ | (6.5,6.7)✓ | (7.3,5.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,1.0) | - | (5.6,2.0)✓ | (4.8,2.0)✓ |
| door | (0.0,4.0) | - | (-0.1,4.0)✓ | (-0.2,4.0)✓ |
| table | (7.0,3.0) | - | (6.5,1.5)✓ | (7.3,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (2.0,1.0) | - | (2.0,2.0)✓ | (4.3,2.0)✗2.5 |
| door | (5.0,4.0) | - | (5.4,4.0)✓ | (4.2,4.0)✓ |
| table | (7.0,3.0) | - | (6.7,1.5)✓ | (5.6,2.0)✓ |

- **baseline 问题**：bed→door 方向错（GT SE，模型 E）；bed-table 距离画错（GT 5.4，模型 4.2）；bed→table 方向错（GT S，模型 W）；door-table 距离画错（GT 7.3，模型 9.2）
- **threeview 问题**：bed-table 距离画错（GT 5.4，模型 3.6）；door-table 距离画错（GT 7.3，模型 5.1）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：bed→door 方向错（GT SE，模型 E）；bed-table 距离画错（GT 5.4，模型 3.2）；bed→table 方向错（GT S，模型 SW）；door-table 距离画错（GT 7.3，模型 8.6）

### 样本 137 `scene0356_00`（scannet · object_rel_direction_easy）

Q：If I am standing by the bed and facing the radiator, is the telephone to the left or the right of the radiator?

- QA：GT B | baseline A（错） | threeview A（错） | threeview_3pass B（对）
- 对齐：baseline: yaw=-153° mirror=是(未证实) 平移=(10.9,1.7) RMSE=1.37；threeview: yaw=-168° mirror=是(证据支持) 平移=(9.7,0.8) RMSE=1.03；threeview_3pass: yaw=-158° mirror=否 平移=(6.2,12.0) RMSE=1.28
- 补偿：baseline: 尺度=1.08 z偏移=+0.00；threeview: 尺度=0.89 z偏移=-0.50；threeview_3pass: 尺度=1.08 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (3.0,6.0) | (3.6,4.7)✓ | (4.0,4.7)✓ | (3.7,4.5)✓ |
| radiator | (6.0,7.0) | (7.4,6.7)✓ | (6.5,7.9)✓ | (7.3,7.1)✓ |
| telephone | (8.0,3.0) | (6.0,4.7)✗2.6 | (6.5,3.4)✓ | (6.1,4.3)✗2.3 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (3.0,2.0) | - | (4.0,2.5)✓ | (3.7,3.0)✓ |
| radiator | (6.0,3.0) | - | (6.5,3.0)✓ | (7.3,3.0)✓ |
| telephone | (8.0,5.0) | - | (6.5,4.0)✓ | (6.1,4.0)✗2.2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,2.0) | - | (4.7,2.5)✓ | (4.5,3.0)✓ |
| radiator | (7.0,3.0) | - | (7.9,3.0)✓ | (7.1,3.0)✓ |
| telephone | (3.0,5.0) | - | (3.4,4.0)✓ | (4.3,4.0)✓ |

- **baseline 问题**：bed→radiator 方向错（GT W，模型 SW）；bed-telephone 距离画错（GT 5.8，模型 2.2）；bed→telephone 方向错（GT NW，模型 W）；radiator-telephone 距离画错（GT 4.5，模型 2.2）；radiator→telephone 方向错（GT NW，模型 NE）
- **threeview 问题**：bed-radiator 距离画错（GT 3.2，模型 4.6）；bed→radiator 方向错（GT W，模型 SW）；bed-telephone 距离画错（GT 5.8，模型 3.2）；radiator→telephone 方向错（GT NW，模型 N）
- **threeview_3pass 问题**：bed→radiator 方向错（GT W，模型 SW）；bed-telephone 距离画错（GT 5.8，模型 2.2）；bed→telephone 方向错（GT NW，模型 W）；radiator-telephone 距离画错（GT 4.5，模型 2.8）；radiator→telephone 方向错（GT NW，模型 NE）

### 样本 138 `42445026`（arkitscenes · object_rel_direction_hard）

Q：If I am standing by the tv and facing the sofa, is the table to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT A | baseline B（错） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=101° mirror=否 平移=(9.6,0.1) RMSE=1.92；threeview: yaw=94° mirror=否 平移=(9.8,-0.6) RMSE=1.82；threeview_3pass: yaw=101° mirror=否 平移=(10.5,0.3) RMSE=1.92
- 补偿：baseline: 尺度=0.85 z偏移=+0.00；threeview: 尺度=1.08 z偏移=-1.00；threeview_3pass: 尺度=0.85 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (5.0,6.0) | (6.2,4.5)✓ | (6.2,4.2)✗2.2 | (6.2,4.5)✓ |
| table | (6.0,1.0) | (3.7,4.0)✗3.8 | (4.0,4.0)✗3.6 | (3.7,4.0)✗3.8 |
| tv | (0.0,5.0) | (1.2,3.5)✓ | (0.8,3.8)✓ | (1.2,3.5)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (5.0,3.0) | - | (6.2,3.0)✓ | (6.2,2.0)✓ |
| table | (6.0,2.0) | - | (4.0,2.0)✓ | (3.7,2.0)✗2.3 |
| tv | (0.0,6.0) | - | (0.8,4.5)✓ | (1.2,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (6.0,3.0) | - | (4.2,3.0)✓ | (4.5,2.0)✓ |
| table | (1.0,2.0) | - | (4.0,2.0)✗3.0 | (4.0,2.0)✗3.0 |
| tv | (5.0,6.0) | - | (3.8,4.5)✓ | (3.5,6.0)✓ |

- **baseline 问题**：sofa-table 距离画错（GT 5.1，模型 3.0）；sofa→table 方向错（GT N，模型 E）；table-tv 距离画错（GT 7.2，模型 3.0）；table→tv 方向错（GT SE，模型 E）
- **threeview 问题**：sofa-table 距离画错（GT 5.1，模型 2.0）；sofa→table 方向错（GT N，模型 E）；table-tv 距离画错（GT 7.2，模型 3.0）；table→tv 方向错（GT SE，模型 E）；z 整体偏高（平均 +0.5 格）
- **threeview_3pass 问题**：sofa-table 距离画错（GT 5.1，模型 3.0）；sofa→table 方向错（GT N，模型 E）；table-tv 距离画错（GT 7.2，模型 3.0）；table→tv 方向错（GT SE，模型 E）

### 样本 139 `5ee7c22ba0`（scannetpp · object_rel_direction_medium）

Q：If I am standing by the microwave and facing the ceiling light, is the refrigerator to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT C | baseline A（错） | threeview B（错） | threeview_3pass C（对）
- 对齐：baseline: yaw=55° mirror=否 平移=(3.6,-2.8) RMSE=1.03；threeview: yaw=-124° mirror=是(证据支持) 平移=(11.2,3.4) RMSE=1.20；threeview_3pass: yaw=63° mirror=否 平移=(4.8,-2.9) RMSE=1.25
- 补偿：baseline: 尺度=0.76 z偏移=+0.00；threeview: 尺度=1.30 z偏移=-2.00；threeview_3pass: 尺度=0.69 z偏移=-2.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (4.0,3.0) | (5.2,2.3)✓ | (4.4,1.6)✓ | (5.4,2.5)✓ |
| microwave | (3.0,1.0) | (2.4,2.4)✓ | (3.1,3.2)✗2.3 | (2.3,2.5)✓ |
| refrigerator | (4.0,7.0) | (3.4,6.3)✓ | (3.5,6.1)✓ | (3.3,5.9)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (4.0,8.0) | - | (4.4,7.0)✓ | (5.4,7.0)✓ |
| microwave | (3.0,3.0) | - | (3.1,3.0)✓ | (2.3,3.0)✓ |
| refrigerator | (4.0,2.0) | - | (3.5,2.5)✓ | (3.3,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (3.0,8.0) | - | (1.6,7.0)✓ | (2.5,7.0)✓ |
| microwave | (1.0,3.0) | - | (3.2,3.0)✗2.2 | (2.5,3.0)✓ |
| refrigerator | (7.0,2.0) | - | (6.1,2.5)✓ | (5.9,2.0)✓ |

- **baseline 问题**：ceiling light-microwave 距离画错（GT 2.2，模型 3.6）；ceiling light→microwave 方向错（GT NE，模型 E）；ceiling light-refrigerator 距离画错（GT 4.0，模型 5.8）；ceiling light→refrigerator 方向错（GT S，模型 SE）
- **threeview 问题**：ceiling light→microwave 方向错（GT NE，模型 SE）；microwave-refrigerator 距离画错（GT 6.1，模型 2.2）；z 整体偏高（平均 +1.8 格）
- **threeview_3pass 问题**：ceiling light-microwave 距离画错（GT 2.2，模型 4.5）；ceiling light→microwave 方向错（GT NE，模型 E）；ceiling light-refrigerator 距离画错（GT 4.0，模型 5.8）；ceiling light→refrigerator 方向错（GT S，模型 SE）；z 整体偏高（平均 +1.7 格）

### 样本 140 `scene0458_00`（scannet · object_rel_direction_easy）

Q：If I am standing by the mirror and facing the window, is the door to the left or the right of the window?

- QA：GT A | baseline A（对） | threeview A（对） | threeview_3pass A（对）
- 对齐：baseline: yaw=-111° mirror=否 平移=(2.9,10.1) RMSE=1.77；threeview: yaw=-174° mirror=否 平移=(9.2,11.4) RMSE=0.44；threeview_3pass: yaw=-112° mirror=否 平移=(3.2,10.5) RMSE=1.39
- 补偿：baseline: 尺度=0.95 z偏移=+0.00；threeview: 尺度=1.05 z偏移=-0.50；threeview_3pass: 尺度=0.91 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (8.0,6.0) | (7.1,7.2)✓ | (8.5,6.3)✓ | (7.2,7.4)✓ |
| mirror | (1.0,6.0) | (4.0,4.4)✗3.4 | (1.2,5.5)✓ | (3.3,5.0)✗2.5 |
| window | (6.0,1.0) | (3.9,1.4)✗2.2 | (5.4,1.2)✓ | (4.5,0.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (8.0,5.0) | - | (8.5,4.0)✓ | (7.2,4.0)✓ |
| mirror | (1.0,4.0) | - | (1.2,4.5)✓ | (3.3,5.0)✗2.5 |
| window | (6.0,5.0) | - | (5.4,5.0)✓ | (4.5,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (6.0,5.0) | - | (6.3,4.0)✓ | (7.4,4.0)✓ |
| mirror | (6.0,4.0) | - | (5.5,4.5)✓ | (5.0,5.0)✓ |
| window | (1.0,5.0) | - | (1.2,5.0)✓ | (0.6,5.0)✓ |

- **baseline 问题**：door-mirror 距离画错（GT 7.0，模型 4.5）；door→mirror 方向错（GT E，模型 NE）；door-window 距离画错（GT 5.4，模型 7.1）；door→window 方向错（GT N，模型 NE）；mirror-window 距离画错（GT 7.1，模型 3.2）；mirror→window 方向错（GT NW，模型 N）
- **threeview 问题**：door→window 方向错（GT N，模型 NE）；mirror-window 距离画错（GT 7.1，模型 5.7）
- **threeview_3pass 问题**：door-mirror 距离画错（GT 7.0，模型 5.0）；door→mirror 方向错（GT E，模型 NE）；door-window 距离画错（GT 5.4，模型 8.0）；mirror-window 距离画错（GT 7.1，模型 5.0）；mirror→window 方向错（GT NW，模型 N）

### 样本 141 `47333899`（arkitscenes · object_rel_direction_easy）

Q：If I am standing by the refrigerator and facing the washer, is the table to the left or the right of the washer?

- QA：GT B | baseline A（错） | threeview B（对） | threeview_3pass None（错）
- 对齐：baseline: yaw=-41° mirror=是(证据支持) 平移=(2.5,9.5) RMSE=0.38；threeview: yaw=-49° mirror=是(证据支持) 平移=(4.8,10.1) RMSE=0.83；threeview_3pass: yaw=-0° mirror=否 平移=(-1.0,-1.3) RMSE=1.86
- 补偿：baseline: 尺度=1.05 z偏移=+0.00；threeview: 尺度=1.40 z偏移=-1.00；threeview_3pass: 尺度=0.67 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (3.0,7.0) | (2.6,6.8)✓ | (3.7,6.8)✓ | (2.0,5.7)✓ |
| table | (2.0,1.0) | (2.1,1.6)✓ | (1.8,0.5)✓ | (4.0,3.7)✗3.3 |
| washer | (7.0,3.0) | (7.3,2.6)✓ | (6.5,3.7)✓ | (6.0,1.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (3.0,4.0) | - | (3.7,4.0)✓ | (2.0,4.0)✓ |
| table | (2.0,2.0) | - | (1.8,1.5)✓ | (4.0,2.0)✓ |
| washer | (7.0,2.0) | - | (6.5,2.0)✓ | (6.0,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (7.0,4.0) | - | (6.8,4.0)✓ | (5.7,4.0)✓ |
| table | (1.0,2.0) | - | (0.5,1.5)✓ | (3.7,2.0)✗2.7 |
| washer | (3.0,2.0) | - | (3.7,2.0)✓ | (1.7,2.0)✓ |

- **baseline 问题**：refrigerator-table 距离画错（GT 6.1，模型 5.0）
- **threeview 问题**：refrigerator-table 距离画错（GT 6.1，模型 4.7）；refrigerator-washer 距离画错（GT 5.7，模型 3.0）；table-washer 距离画错（GT 5.4，模型 4.0）；table→washer 方向错（GT W，模型 SW）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：refrigerator-table 距离画错（GT 6.1，模型 4.2）；refrigerator→table 方向错（GT N，模型 NW）；refrigerator-washer 距离画错（GT 5.7，模型 8.5）；table-washer 距离画错（GT 5.4，模型 4.2）；table→washer 方向错（GT W，模型 NW）

### 样本 142 `5eb31827b7`（scannetpp · object_rel_direction_medium）

Q：If I am standing by the computer tower and facing the telephone, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT B | baseline C（错） | threeview A（错） | threeview_3pass C（错）
- 对齐：baseline: yaw=74° mirror=否 平移=(8.0,-2.2) RMSE=1.61；threeview: yaw=-18° mirror=是(证据支持) 平移=(1.2,8.7) RMSE=1.74；threeview_3pass: yaw=79° mirror=否 平移=(7.8,-1.6) RMSE=1.77
- 补偿：baseline: 尺度=0.78 z偏移=+0.00；threeview: 尺度=0.66 z偏移=-1.50；threeview_3pass: 尺度=0.64 z偏移=-2.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer tower | (1.0,3.0) | (3.8,2.0)✗3.0 | (3.8,3.0)✗2.8 | (3.9,2.1)✗3.0 |
| door | (1.0,1.0) | (0.4,1.4)✓ | (0.9,0.5)✓ | (0.5,1.4)✓ |
| telephone | (7.0,2.0) | (4.8,2.6)✗2.3 | (4.3,2.5)✗2.7 | (4.6,2.6)✗2.4 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer tower | (1.0,1.0) | - | (3.8,1.0)✗2.8 | (3.9,1.0)✗2.9 |
| door | (1.0,4.0) | - | (0.9,3.5)✓ | (0.5,3.0)✓ |
| telephone | (7.0,0.0) | - | (4.3,2.0)✗3.3 | (4.6,1.0)✗2.6 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer tower | (3.0,1.0) | - | (3.0,1.0)✓ | (2.1,1.0)✓ |
| door | (1.0,4.0) | - | (0.5,3.5)✓ | (1.4,3.0)✓ |
| telephone | (2.0,0.0) | - | (2.5,2.0)✗2.1 | (2.6,1.0)✓ |

- **baseline 问题**：computer tower-door 距离画错（GT 2.0，模型 4.5）；computer tower→door 方向错（GT N，模型 E）；computer tower-telephone 距离画错（GT 6.1，模型 1.4）；computer tower→telephone 方向错（GT W，模型 SW）
- **threeview 问题**：computer tower-door 距离画错（GT 2.0，模型 5.8）；computer tower→door 方向错（GT N，模型 NE）；computer tower-telephone 距离画错（GT 6.1，模型 1.1）；computer tower→telephone 方向错（GT W，模型 NW）；door→telephone 方向错（GT W，模型 SW）；z 整体偏高（平均 +2.0 格）
- **threeview_3pass 问题**：computer tower-door 距离画错（GT 2.0，模型 5.4）；computer tower→door 方向错（GT N，模型 E）；computer tower-telephone 距离画错（GT 6.1，模型 1.4）；computer tower→telephone 方向错（GT W，模型 SW）；z 整体偏高（平均 +2.0 格）

### 样本 143 `scene0648_00`（scannet · object_rel_direction_medium）

Q：If I am standing by the bookshelf and facing the fan, is the closet to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT B | baseline B（对） | threeview B（对） | threeview_3pass B（对）
- 对齐：baseline: yaw=-48° mirror=否 平移=(-0.4,5.6) RMSE=0.58；threeview: yaw=118° mirror=否 平移=(11.3,1.3) RMSE=0.37；threeview_3pass: yaw=-48° mirror=否 平移=(-0.4,5.6) RMSE=0.58
- 补偿：baseline: 尺度=0.75 z偏移=+0.00；threeview: 尺度=1.04 z偏移=-1.00；threeview_3pass: 尺度=0.75 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bookshelf | (5.0,7.0) | (4.9,6.7)✓ | (5.1,6.6)✓ | (4.9,6.7)✓ |
| closet | (7.0,3.0) | (7.4,2.8)✓ | (7.5,3.1)✓ | (7.4,2.8)✓ |
| fan | (5.0,3.0) | (4.7,3.5)✓ | (4.5,3.3)✓ | (4.7,3.5)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bookshelf | (5.0,5.0) | - | (5.1,3.5)✓ | (4.9,4.0)✓ |
| closet | (7.0,4.0) | - | (7.5,4.0)✓ | (7.4,4.0)✓ |
| fan | (5.0,2.0) | - | (4.5,7.5)✗5.5 | (4.7,8.0)✗6.0 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bookshelf | (7.0,5.0) | - | (6.6,3.5)✓ | (6.7,4.0)✓ |
| closet | (3.0,4.0) | - | (3.1,4.0)✓ | (2.8,4.0)✓ |
| fan | (3.0,2.0) | - | (3.3,7.5)✗5.5 | (3.5,8.0)✗6.0 |

- **baseline 问题**：bookshelf-closet 距离画错（GT 4.5，模型 6.1）；closet-fan 距离画错（GT 2.0，模型 3.6）
- **threeview 问题**：z 整体偏高（平均 +2.3 格）
- **threeview_3pass 问题**：bookshelf-closet 距离画错（GT 4.5，模型 6.1）；closet-fan 距离画错（GT 2.0，模型 3.6）；z 整体偏高（平均 +1.7 格）

### 样本 144 `42897538`（arkitscenes · object_rel_direction_hard）

Q：If I am standing by the refrigerator and facing the tv, is the stool to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT C | baseline B（错） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=-30° mirror=是(未证实) 平移=(2.1,11.1) RMSE=0.92；threeview: yaw=-37° mirror=是(未证实) 平移=(1.8,10.4) RMSE=0.52；threeview_3pass: yaw=-36° mirror=是(未证实) 平移=(3.3,12.5) RMSE=0.76
- 补偿：baseline: 尺度=0.69 z偏移=+0.00；threeview: 尺度=0.83 z偏移=-0.50；threeview_3pass: 尺度=0.70 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (3.0,7.0) | (2.5,6.1)✓ | (2.6,6.6)✓ | (2.6,6.6)✓ |
| stool | (3.0,3.0) | (3.6,3.9)✓, (3.0,4.2)多, 多1 | (3.0,3.7)✓ | (3.6,3.3)✓, (3.0,3.7)多, 多1 |
| tv | (6.0,5.0) | (6.5,4.7)✓ | (6.4,4.7)✓ | (6.4,4.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (3.0,4.0) | - | (2.6,4.0)✓ | (2.6,4.0)✓ |
| stool | (3.0,1.0) | - | (3.0,1.0)✓ | (3.0,1.0)✓, (3.6,1.0)多, 多1 |
| tv | (6.0,4.0) | - | (6.4,5.0)✓ | (6.4,4.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (7.0,4.0) | - | (6.6,4.0)✓ | (6.6,4.0)✓ |
| stool | (3.0,1.0) | - | (3.7,1.0)✓ | (3.3,1.0)✓, (3.7,1.0)多, 多1 |
| tv | (5.0,4.0) | - | (4.7,5.0)✓ | (4.7,4.0)✓ |

- **baseline 问题**：多画 stool ×1（GT 1，模型 2）；refrigerator-stool 距离画错（GT 4.0，模型 2.8）；refrigerator-tv 距离画错（GT 3.6，模型 6.1）；refrigerator→tv 方向错（GT NW，模型 W）；stool→tv 方向错（GT SW，模型 W）
- **threeview 问题**：refrigerator-tv 距离画错（GT 3.6，模型 5.1）；stool→tv 方向错（GT SW，模型 W）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：多画 stool ×1（GT 1，模型 2）；refrigerator-tv 距离画错（GT 3.6，模型 6.1）；stool→tv 方向错（GT SW，模型 W）

### 样本 145 `45b0dac5e3`（scannetpp · object_rel_direction_medium）

Q：If I am standing by the heater and facing the toilet, is the cup to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT B | baseline A（错） | threeview B（对） | threeview_3pass B（对）
- 对齐：baseline: yaw=134° mirror=是(未证实) 平移=(4.0,-3.3) RMSE=0.74；threeview: yaw=17° mirror=否 平移=(2.0,-3.3) RMSE=1.62；threeview_3pass: yaw=-17° mirror=否 平移=(0.1,-0.6) RMSE=1.49
- 补偿：baseline: 尺度=1.24 z偏移=+0.00；threeview: 尺度=1.32 z偏移=-1.50；threeview_3pass: 尺度=1.60 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cup | (6.0,1.0) | (5.8,1.9)✓ | (7.3,1.7)✓ | (4.0,1.3)✓ |
| heater | (0.0,5.0) | (-0.3,4.6)✓ | (1.2,6.0)✓ | (1.5,3.8)✓ |
| toilet | (7.0,6.0) | (7.6,5.4)✓ | (4.5,4.3)✗3.1 | (7.5,6.9)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cup | (6.0,3.0) | - | (7.3,3.0)✓ | (4.0,3.0)✓ |
| heater | (0.0,3.0) | - | (1.2,4.0)✓ | (1.5,3.0)✓ |
| toilet | (7.0,2.0) | - | (4.5,2.0)✗2.5 | (7.5,1.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cup | (1.0,3.0) | - | (1.7,3.0)✓ | (1.3,3.0)✓ |
| heater | (5.0,3.0) | - | (6.0,4.0)✓ | (3.8,3.0)✓ |
| toilet | (6.0,2.0) | - | (4.3,2.0)✓ | (6.9,1.0)✓ |

- **baseline 问题**：cup-heater 距离画错（GT 7.2，模型 5.4）；cup-toilet 距离画错（GT 5.1，模型 3.2）；cup→toilet 方向错（GT S，模型 SW）
- **threeview 问题**：cup-heater 距离画错（GT 7.2，模型 5.7）；cup-toilet 距离画错（GT 5.1，模型 2.9）；cup→toilet 方向错（GT S，模型 SE）；heater-toilet 距离画错（GT 7.1，模型 2.8）；heater→toilet 方向错（GT W，模型 NW）；z 整体偏高（平均 +1.8 格）
- **threeview_3pass 问题**：cup-heater 距离画错（GT 7.2，模型 2.2）；cup→toilet 方向错（GT S，模型 SW）；heater-toilet 距离画错（GT 7.1，模型 4.2）；heater→toilet 方向错（GT W，模型 SW）；z 整体偏高（平均 +0.7 格）

### 样本 146 `scene0645_00`（scannet · object_rel_direction_medium）

Q：If I am standing by the sofa and facing the nightstand, is the tv to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT A | baseline C（错） | threeview C（错） | threeview_3pass C（错）
- 对齐：baseline: yaw=55° mirror=否 平移=(5.0,-2.6) RMSE=0.96；threeview: yaw=55° mirror=是(未证实) 平移=(-2.8,3.1) RMSE=1.01；threeview_3pass: yaw=53° mirror=是(未证实) 平移=(-3.0,3.6) RMSE=0.84
- 补偿：baseline: 尺度=0.79 z偏移=+0.00；threeview: 尺度=0.70 z偏移=-1.00；threeview_3pass: 尺度=0.77 z偏移=+1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| nightstand | (2.0,2.0) | (2.2,3.4)✓ | (2.1,3.3)✓ | (1.9,3.0)✓ |
| sofa | (4.0,6.0) | (3.1,4.7)✓ | (3.1,4.8)✓ | (3.3,4.9)✓ |
| tv | (5.0,3.0) | (5.7,2.9)✓ | (5.7,2.9)✓ | (5.8,3.1)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| nightstand | (2.0,3.0) | - | (2.1,2.5)✓ | (1.9,3.0)✓ |
| sofa | (4.0,3.0) | - | (3.1,3.0)✓ | (3.3,3.0)✓ |
| tv | (5.0,5.0) | - | (5.7,5.0)✓ | (5.8,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| nightstand | (2.0,3.0) | - | (3.3,2.5)✓ | (3.0,3.0)✓ |
| sofa | (6.0,3.0) | - | (4.8,3.0)✓ | (4.9,3.0)✓ |
| tv | (3.0,5.0) | - | (2.9,5.0)✓ | (3.1,6.0)✓ |

- **baseline 问题**：nightstand-sofa 距离画错（GT 4.5，模型 2.0）；nightstand-tv 距离画错（GT 3.2，模型 4.5）；sofa→tv 方向错（GT N，模型 NW）
- **threeview 问题**：nightstand-sofa 距离画错（GT 4.5，模型 2.5）；nightstand-tv 距离画错（GT 3.2，模型 5.1）；sofa-tv 距离画错（GT 3.2，模型 4.5）；sofa→tv 方向错（GT N，模型 NW）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：nightstand-sofa 距离画错（GT 4.5，模型 3.0）；nightstand-tv 距离画错（GT 3.2，模型 5.0）；sofa→tv 方向错（GT N，模型 NW）；z 整体偏低（平均 -0.7 格）

### 样本 147 `47429977`（arkitscenes · object_rel_direction_medium）

Q：If I am standing by the tv and facing the refrigerator, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT C | baseline A（错） | threeview A（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=-94° mirror=是(未证实) 平移=(9.3,8.3) RMSE=0.65；threeview: yaw=-153° mirror=是(证据支持) 平移=(9.2,0.1) RMSE=0.99；threeview_3pass: yaw=-80° mirror=是(证据支持) 平移=(7.7,9.6) RMSE=0.27
- 补偿：baseline: 尺度=0.97 z偏移=+0.00；threeview: 尺度=1.12 z偏移=+1.50；threeview_3pass: 尺度=1.03 z偏移=+1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (2.0,7.0) | (1.3,6.7)✓ | (2.6,5.3)✓ | (2.1,6.6)✓ |
| stove | (1.0,3.0) | (2.0,3.7)✓ | (0.1,4.0)✓ | (0.6,3.3)✓ |
| tv | (6.0,1.0) | (5.7,0.6)✓ | (6.4,1.6)✓ | (6.2,1.1)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (2.0,4.0) | - | (2.6,6.5)✗2.6 | (2.1,4.0)✓ |
| stove | (1.0,5.0) | - | (0.1,4.5)✓ | (0.6,3.0)✗2.0 |
| tv | (6.0,6.0) | - | (6.4,6.0)✓ | (6.2,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (7.0,4.0) | - | (5.3,6.5)✗3.0 | (6.6,4.0)✓ |
| stove | (3.0,5.0) | - | (4.0,4.5)✓ | (3.3,3.0)✗2.0 |
| tv | (1.0,6.0) | - | (1.6,6.0)✓ | (1.1,6.0)✓ |

- **baseline 问题**：stove→tv 方向错（GT W，模型 NW）
- **threeview 问题**：refrigerator-stove 距离画错（GT 4.1，模型 2.5）；refrigerator→stove 方向错（GT N，模型 NE）；refrigerator-tv 距离画错（GT 7.2，模型 4.7）；z 整体偏低（平均 -0.8 格）
- **threeview_3pass 问题**：refrigerator→stove 方向错（GT N，模型 NE）；z 整体偏低（平均 -1.7 格）

### 样本 148 `45b0dac5e3`（scannetpp · object_rel_direction_hard）

Q：If I am standing by the ceiling light and facing the door, is the cup to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT A | baseline A（对） | threeview D（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=-2° mirror=否 平移=(1.9,-1.2) RMSE=0.33；threeview: yaw=-22° mirror=否 平移=(-0.6,0.1) RMSE=0.84；threeview_3pass: yaw=-58° mirror=是(证据支持) 平移=(6.6,9.5) RMSE=0.94
- 补偿：baseline: 尺度=1.11 z偏移=+0.00；threeview: 尺度=1.01 z偏移=-1.20；threeview_3pass: 尺度=0.88 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (7.0,4.0) | (7.2,3.6)✓ | (5.9,2.9)✓ | (8.0,4.6)✓ |
| cup | (6.0,1.0) | (6.0,1.4)✓ | (6.8,1.9)✓ | (4.8,1.6)✓ |
| door | (3.0,7.0) | (2.8,7.0)✓ | (3.3,7.2)✓ | (3.2,5.8)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (7.0,8.0) | - | (5.9,8.0)✓ | (8.0,8.0)✓ |
| cup | (6.0,3.0) | - | (6.8,2.0)✓ | (4.8,3.0)✓ |
| door | (3.0,3.0) | - | (3.3,3.3)✓ | (3.2,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (4.0,8.0) | - | (2.9,8.0)✓ | (4.6,8.0)✓ |
| cup | (1.0,3.0) | - | (1.9,2.0)✓ | (1.6,3.0)✓ |
| door | (7.0,3.0) | - | (7.2,3.3)✓ | (5.8,3.0)✓ |

- **baseline 问题**：ceiling light→cup 方向错（GT N，模型 NE）
- **threeview 问题**：ceiling light-cup 距离画错（GT 3.2，模型 1.3）；ceiling light→cup 方向错（GT N，模型 NW）；z 整体偏高（平均 +1.0 格）
- **threeview_3pass 问题**：ceiling light-cup 距离画错（GT 3.2，模型 5.1）；ceiling light→cup 方向错（GT N，模型 NE）；ceiling light→door 方向错（GT SE，模型 E）；cup-door 距离画错（GT 6.7，模型 5.1）；cup→door 方向错（GT SE，模型 S）；z 整体偏高（平均 +1.0 格）

### 样本 149 `scene0645_00`（scannet · object_rel_direction_hard）

Q：If I am standing by the sofa and facing the towel, is the nightstand to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT A | baseline A（对） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=14° mirror=否 平移=(1.7,-2.3) RMSE=0.86；threeview: yaw=72° mirror=否 平移=(6.9,-1.0) RMSE=0.91；threeview_3pass: yaw=-8° mirror=是(证据支持) 平移=(-0.4,10.0) RMSE=0.90
- 补偿：baseline: 尺度=0.79 z偏移=+0.00；threeview: 尺度=1.28 z偏移=+0.60；threeview_3pass: 尺度=0.66 z偏移=+1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| nightstand | (2.0,2.0) | (3.0,1.5)✓ | (3.5,2.0)✓ | (1.5,2.3)✓ |
| sofa | (4.0,6.0) | (4.4,6.0)✓ | (4.0,6.0)✓ | (3.9,5.3)✓ |
| towel | (5.0,2.0) | (3.6,2.5)✓ | (3.5,2.0)✓ | (5.5,2.4)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| nightstand | (2.0,3.0) | - | (3.5,3.0)✓ | (1.5,3.0)✓ |
| sofa | (4.0,3.0) | - | (4.0,3.8)✓ | (3.9,3.0)✓ |
| towel | (5.0,5.0) | - | (3.5,3.8)✓ | (5.5,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| nightstand | (2.0,3.0) | - | (2.0,3.0)✓ | (2.3,3.0)✓ |
| sofa | (6.0,3.0) | - | (6.0,3.8)✓ | (5.3,3.0)✓ |
| towel | (2.0,5.0) | - | (2.0,3.8)✓ | (2.4,5.0)✓ |

- **baseline 问题**：nightstand-sofa 距离画错（GT 4.5，模型 5.8）；nightstand→sofa 方向错（GT SW，模型 S）；nightstand-towel 距离画错（GT 3.0，模型 1.4）；nightstand→towel 方向错（GT W，模型 SW）
- **threeview 问题**：nightstand-sofa 距离画错（GT 4.5，模型 3.2）；nightstand→sofa 方向错（GT SW，模型 S）；nightstand-towel 距离画错（GT 3.0，模型 0.0）；nightstand→towel 方向错（GT W，模型 E）；z 整体偏低（平均 -0.7 格）
- **threeview_3pass 问题**：nightstand-sofa 距离画错（GT 4.5，模型 5.8）；nightstand-towel 距离画错（GT 3.0，模型 6.1）；sofa→towel 方向错（GT N，模型 NW）；z 整体偏低（平均 -1.0 格）

### 样本 150 `47430048`（arkitscenes · object_rel_direction_easy）

Q：If I am standing by the bathtub and facing the toilet, is the washer to the left or the right of the toilet?

- QA：GT B | baseline B（对） | threeview B（对） | threeview_3pass A（错）
- 对齐：baseline: yaw=-151° mirror=否 平移=(4.4,11.1) RMSE=1.68；threeview: 2点 yaw=-88° mirror=否 平移=(-1.4,8.3) RMSE=0.73；threeview_3pass: yaw=-73° mirror=否 平移=(-3.5,7.0) RMSE=2.32
- 补偿：baseline: 尺度=0.56 z偏移=+0.00；threeview: 尺度=1.48 z偏移=+0.75；threeview_3pass: 尺度=0.34 z偏移=+2.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bathtub | (4.0,7.0) | (4.0,5.0)✗2.0 | (4.0,7.0)✓ | (3.4,5.2)✓ |
| toilet | (2.0,1.0) | (3.4,2.7)✗2.2 | (2.0,1.0)✓ | (2.6,4.2)✗3.3 |
| washer | (2.0,4.0) | (0.6,4.3)✓ | 漏1 | (2.0,2.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bathtub | (4.0,3.0) | - | (4.0,3.2)✓ | (3.4,3.0)✓ |
| toilet | (2.0,4.0) | - | (2.0,3.8)✓ | (2.6,4.0)✓ |
| washer | (2.0,4.0) | - | 漏1 | (2.0,4.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bathtub | (7.0,3.0) | - | (7.0,3.2)✓ | (5.2,3.0)✓ |
| toilet | (1.0,4.0) | - | (1.0,3.8)✓ | (4.2,4.0)✗3.2 |
| washer | (4.0,4.0) | - | 漏1 | (2.6,4.0)✓ |

- **baseline 问题**：bathtub-toilet 距离画错（GT 6.3，模型 4.2）；bathtub-washer 距离画错（GT 3.6，模型 6.3）；bathtub→washer 方向错（GT NE，模型 E）；toilet-washer 距离画错（GT 3.0，模型 5.8）；toilet→washer 方向错（GT S，模型 SE）
- **threeview 问题**：漏画 washer ×1（GT 1，模型 0）；bathtub-toilet 距离画错（GT 6.3，模型 4.3）；z 整体偏低（平均 -0.8 格）
- **threeview_3pass 问题**：bathtub-toilet 距离画错（GT 6.3，模型 3.6）；bathtub→toilet 方向错（GT N，模型 NE）；bathtub-washer 距离画错（GT 3.6，模型 8.5）；toilet-washer 距离画错（GT 3.0，模型 5.0）；toilet→washer 方向错（GT S，模型 N）；z 整体偏低（平均 -2.0 格）

### 样本 151 `41125700`（arkitscenes · route_planning）

Q：You are a robot beginning at the tv and facing the sofa. You want to navigate to the microwave. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the sink 3. [please fill in] 4. Go forward until the microwave. You have reached the final destination.

- QA：GT D | baseline D（对） | threeview D（对） | threeview_3pass D（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| microwave | - | (2.0,4.0)多, 多1 | (1.5,6.0)多, 多1 | (1.0,4.0)多, 多1 |
| sofa | (4.0,6.0), (5.0,7.0) | (5.0,8.0)✓, 漏1 | (5.0,3.0)✗3.2, 漏1 | (5.0,7.0)✓, 漏1 |
| tv | - | (5.0,2.0)多, 多1 | (5.0,8.0)多, 多1 | (5.0,2.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| microwave | - | - | (1.5,4.5)多, 多1 | (1.0,4.0)多, 多1 |
| sofa | (4.0,3.0), (5.0,2.0) | - | (5.0,3.0)✓, 漏1 | (5.0,2.0)✓, 漏1 |
| tv | - | - | (5.0,5.0)多, 多1 | (5.0,5.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| microwave | - | - | (6.0,4.5)多, 多1 | (4.0,4.0)多, 多1 |
| sofa | (6.0,3.0), (7.0,2.0) | - | (3.0,3.0)✗3.0, 漏1 | (7.0,2.0)✓, 漏1 |
| tv | - | - | (8.0,5.0)多, 多1 | (2.0,5.0)多, 多1 |

- **baseline 问题**：多画 tv ×1（GT 0，模型 1）；多画 microwave ×1（GT 0，模型 1）；漏画 sofa ×1（GT 2，模型 1）
- **threeview 问题**：多画 tv ×1（GT 0，模型 1）；多画 microwave ×1（GT 0，模型 1）；漏画 sofa ×1（GT 2，模型 1）
- **threeview_3pass 问题**：多画 tv ×1（GT 0，模型 1）；多画 microwave ×1（GT 0，模型 1）；漏画 sofa ×1（GT 2，模型 1）

### 样本 152 `c49a8c6cff`（scannetpp · route_planning）

Q：You are a robot beginning at the door and facing the window. You want to navigate to the monitor. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. Go forward until the heater 2. [please fill in] 3. Go forward until the monitor. You have reached the final destination.

- QA：GT C | baseline B（错） | threeview B（错） | threeview_3pass A（错）
- 对齐：baseline: 2点 yaw=-57° mirror=否 平移=(-3.6,6.5) RMSE=1.15；threeview: 2点 yaw=109° mirror=否 平移=(8.6,2.2) RMSE=0.60；threeview_3pass: 2点 yaw=-53° mirror=否 平移=(-2.5,7.4) RMSE=0.81
- 补偿：baseline: 尺度=2.02 z偏移=+0.00；threeview: 尺度=1.36 z偏移=-1.75；threeview_3pass: 尺度=1.55 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (7.0,2.0) | (7.0,2.0)✓ | (7.0,2.0)✓ | (7.0,2.0)✓ |
| monitor | (1.0,6.0), (2.0,6.0) | (2.0,6.0)✓, 漏1 | (2.0,6.0)✓, 漏1 | (2.0,6.0)✓, 漏1 |
| window | - | (-3.0,10.0)多, 多1 | (-3.8,4.0)多, 多1 | (3.2,14.7)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (7.0,3.0) | - | (7.0,2.8)✓ | (7.0,3.0)✓ |
| monitor | (1.0,3.0), (2.0,3.0) | - | (2.0,3.2)✓, 漏1 | (2.0,3.0)✓, 漏1 |
| window | - | - | (-3.8,4.2)多, 多1 | (3.2,4.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (2.0,3.0) | - | (2.0,2.8)✓ | (2.0,3.0)✓ |
| monitor | (6.0,3.0), (6.0,3.0) | - | (6.0,3.2)✓, 漏1 | (6.0,3.0)✓, 漏1 |
| window | - | - | (4.0,4.2)多, 多1 | (14.7,4.0)多, 多1 |

- **baseline 问题**：多画 window ×1（GT 0，模型 1）；漏画 monitor ×1（GT 2，模型 1）；door-monitor 距离画错（GT 6.4，模型 3.2）
- **threeview 问题**：多画 window ×1（GT 0，模型 1）；漏画 monitor ×1（GT 2，模型 1）；door-monitor 距离画错（GT 6.4，模型 4.7）；z 整体偏高（平均 +1.8 格）
- **threeview_3pass 问题**：多画 window ×1（GT 0，模型 1）；漏画 monitor ×1（GT 2，模型 1）；door-monitor 距离画错（GT 6.4，模型 4.1）；z 整体偏高（平均 +1.0 格）

### 样本 153 `scene0461_00`（scannet · route_planning）

Q：You are a robot beginning at the side table and facing the window. You want to navigate to the coffee table. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the table. You have reached the final destination.

- QA：GT A | baseline C（错） | threeview C（错） | threeview_3pass C（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| coffee table | - | (5.0,6.0)多, 多1 | (5.0,5.0)多, 多1 | (5.0,6.0)多, 多1 |
| side table | - | (2.0,5.0)多, 多1 | (2.5,4.5)多, 多1 | (2.0,4.0)多, 多1 |
| table | (3.0,4.0), (7.0,6.0) | 漏2 | 漏2 | 漏2 |
| window | (1.0,5.0) | (5.0,1.0)✗5.7 | (5.0,9.5)✗6.0 | (5.0,1.0)✗5.7 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| coffee table | - | - | (5.0,2.0)多, 多1 | (5.0,2.0)多, 多1 |
| side table | - | - | (2.5,2.5)多, 多1 | (2.0,2.0)多, 多1 |
| table | (3.0,1.0), (7.0,1.0) | - | 漏2 | 漏2 |
| window | (1.0,5.0) | - | (5.0,6.0)✗4.1 | (5.0,6.0)✗4.1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| coffee table | - | - | (5.0,2.0)多, 多1 | (6.0,2.0)多, 多1 |
| side table | - | - | (4.5,2.5)多, 多1 | (4.0,2.0)多, 多1 |
| table | (4.0,1.0), (6.0,1.0) | - | 漏2 | 漏2 |
| window | (5.0,5.0) | - | (9.5,6.0)✗4.6 | (1.0,6.0)✗4.1 |

- **baseline 问题**：多画 side table ×1（GT 0，模型 1）；多画 coffee table ×1（GT 0，模型 1）；漏画 table ×2（GT 2，模型 0）
- **threeview 问题**：多画 side table ×1（GT 0，模型 1）；多画 coffee table ×1（GT 0，模型 1）；漏画 table ×2（GT 2，模型 0）
- **threeview_3pass 问题**：多画 side table ×1（GT 0，模型 1）；多画 coffee table ×1（GT 0，模型 1）；漏画 table ×2（GT 2，模型 0）

### 样本 154 `47333899`（arkitscenes · route_planning）

Q：You are a robot beginning at the red chair facing the other chair. You want to navigate to the dishwasher. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the dishwasher. You have reached the final destination.

- QA：GT B | baseline A（错） | threeview A（错） | threeview_3pass A（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | (5.0,8.0)多, 多1 | (5.0,8.0)多, 多1 | (5.0,8.0)多, 多1 |
| turn left | - | (3.0,5.0)多, 多1 | (3.5,4.5)多, 多1 | (3.0,5.0)多, 多1 |
| turn right | - | (7.0,5.0)多, 多1 | (6.5,4.5)多, 多1 | (7.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | (5.0,5.0)多, 多1 | (5.0,4.0)多, 多1 |
| turn left | - | - | (3.5,5.0)多, 多1 | (3.0,2.0)多, 多1 |
| turn right | - | - | (6.5,5.0)多, 多1 | (7.0,2.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | (8.0,5.0)多, 多1 | (8.0,4.0)多, 多1 |
| turn left | - | - | (4.5,5.0)多, 多1 | (5.0,2.0)多, 多1 |
| turn right | - | - | (4.5,5.0)多, 多1 | (5.0,2.0)多, 多1 |

- **baseline 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）
- **threeview 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）

### 样本 155 `acd95847c5`（scannetpp · route_planning）

Q：You are a robot beginning at the laptop and facing the telephone next to it. You want to navigate to the headphone on the table opposite. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the coat rack on the wall 3. [please fill in] 4. Go forward until the whiteboard 5. [please fill in] 6. Go forward until the headphone on your left. You have reached the final destination.

- QA：GT C | baseline C（对） | threeview D（错） | threeview_3pass C（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| headphone on the table opposite | - | (5.0,2.0)多, 多1 | (6.5,5.0)多, 多1 | (5.0,8.0)多, 多1 |
| laptop | (6.0,6.0) | (5.0,5.0)✓ | (5.0,5.0)✓ | (5.0,5.0)✓ |
| table | (4.0,4.0), (6.0,3.0), (6.0,5.0) | 漏3 | 漏3 | 漏3 |
| telephone | (7.0,4.0), (7.0,5.0) | 漏2 | 漏2 | 漏2 |
| telephone next to it | - | (3.0,5.0)多, 多1 | (3.5,5.0)多, 多1 | (3.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| headphone on the table opposite | - | - | (6.5,4.2)多, 多1 | (5.0,5.0)多, 多1 |
| laptop | (6.0,2.0) | - | (5.0,4.5)✗2.7 | (5.0,5.0)✗3.2 |
| table | (4.0,1.0), (6.0,1.0), (6.0,1.0) | - | 漏3 | 漏3 |
| telephone | (7.0,2.0), (7.0,2.0) | - | 漏2 | 漏2 |
| telephone next to it | - | - | (3.5,4.3)多, 多1 | (3.0,5.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| headphone on the table opposite | - | - | (5.0,4.2)多, 多1 | (8.0,5.0)多, 多1 |
| laptop | (6.0,2.0) | - | (5.0,4.5)✗2.7 | (5.0,5.0)✗3.2 |
| table | (4.0,1.0), (3.0,1.0), (5.0,1.0) | - | 漏3 | 漏3 |
| telephone | (4.0,2.0), (5.0,2.0) | - | 漏2 | 漏2 |
| telephone next to it | - | - | (5.0,4.3)多, 多1 | (5.0,5.0)多, 多1 |

- **baseline 问题**：多画 telephone next to it ×1（GT 0，模型 1）；多画 headphone on the table opposite ×1（GT 0，模型 1）；漏画 telephone ×2（GT 2，模型 0）；漏画 table ×3（GT 3，模型 0）
- **threeview 问题**：多画 telephone next to it ×1（GT 0，模型 1）；多画 headphone on the table opposite ×1（GT 0，模型 1）；漏画 telephone ×2（GT 2，模型 0）；漏画 table ×3（GT 3，模型 0）
- **threeview_3pass 问题**：多画 telephone next to it ×1（GT 0，模型 1）；多画 headphone on the table opposite ×1（GT 0，模型 1）；漏画 telephone ×2（GT 2，模型 0）；漏画 table ×3（GT 3，模型 0）

### 样本 156 `scene0697_01`（scannet · route_planning）

Q：You are a robot beginning at the dollhouse nearby the window and facing the window. You want to navigate to the hanging picture. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the cabinet with a mirror on top of that. 3. [please fill in] 4. Go forward until the hanging picture. You have reached the final destination.

- QA：GT B | baseline B（对） | threeview B（对） | threeview_3pass D（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| dollhouse nearby the window | - | (4.0,7.0)多, 多1 | (4.0,8.0)多, 多1 | (5.0,4.0)多, 多1 |
| hanging picture | - | (2.0,8.0)多, 多1 | (1.0,5.0)多, 多1 | (2.0,1.0)多, 多1 |
| window | (3.0,1.0), (2.0,2.0) | (5.0,8.0)✗6.7, 漏1 | (5.0,9.0)✗7.6, 漏1 | (5.0,1.0)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| dollhouse nearby the window | - | - | (4.0,3.0)多, 多1 | (5.0,3.0)多, 多1 |
| hanging picture | - | - | (1.0,6.0)多, 多1 | (2.0,6.0)多, 多1 |
| window | (3.0,4.0), (2.0,4.0) | - | (5.0,6.0)✗2.8, 漏1 | (5.0,5.0)✗2.2, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| dollhouse nearby the window | - | - | (8.0,3.0)多, 多1 | (4.0,3.0)多, 多1 |
| hanging picture | - | - | (5.0,6.0)多, 多1 | (1.0,6.0)多, 多1 |
| window | (1.0,4.0), (2.0,4.0) | - | (9.0,6.0)✗7.3, 漏1 | (1.0,5.0)✓, 漏1 |

- **baseline 问题**：漏画 window ×1（GT 2，模型 1）；多画 hanging picture ×1（GT 0，模型 1）；多画 dollhouse nearby the window ×1（GT 0，模型 1）
- **threeview 问题**：漏画 window ×1（GT 2，模型 1）；多画 hanging picture ×1（GT 0，模型 1）；多画 dollhouse nearby the window ×1（GT 0，模型 1）
- **threeview_3pass 问题**：漏画 window ×1（GT 2，模型 1）；多画 hanging picture ×1（GT 0，模型 1）；多画 dollhouse nearby the window ×1（GT 0，模型 1）

### 样本 157 `42897528`（arkitscenes · route_planning）

Q：You are a robot beginning at the doorway and facing the window. You want to navigate to the washer. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. Go forward until the sink 2. [please fill in] 3. Go forward until the washer. You have reached the final destination.

- QA：GT A | baseline A（对） | threeview C（错） | threeview_3pass A（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| doorway | - | (1.0,5.0)多, 多1 | (1.0,8.5)多, 多1 | (1.0,5.0)多, 多1 |
| washer | (1.0,7.0) | (4.0,6.0)✗3.2 | (3.5,4.5)✗3.5 | (5.0,8.0)✗4.1 |
| window | - | (8.0,3.0)多, 多1 | (8.5,5.0)多, 多1 | (5.0,9.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| doorway | - | - | (1.0,4.5)多, 多1 | (1.0,4.0)多, 多1 |
| washer | (1.0,2.0) | - | (3.5,2.5)✗2.5 | (5.0,2.0)✗4.0 |
| window | - | - | (8.5,6.0)多, 多1 | (5.0,6.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| doorway | - | - | (8.5,4.5)多, 多1 | (5.0,4.0)多, 多1 |
| washer | (7.0,2.0) | - | (4.5,2.5)✗2.5 | (8.0,2.0)✓ |
| window | - | - | (5.0,6.0)多, 多1 | (9.0,6.0)多, 多1 |

- **baseline 问题**：多画 window ×1（GT 0，模型 1）；多画 doorway ×1（GT 0，模型 1）
- **threeview 问题**：多画 window ×1（GT 0，模型 1）；多画 doorway ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 window ×1（GT 0，模型 1）；多画 doorway ×1（GT 0，模型 1）

### 样本 158 `5f99900f09`（scannetpp · route_planning）

Q：You are a robot beginning at the refrigerator and facing the refrigerator. You want to navigate to the recycling bin. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the suitcase 3. [please fill in] 4. Go forward until the printer 5. [please fill in] 6. Go forward until the recycling bin. You have reached the final destination.

- QA：GT A | baseline D（错） | threeview D（错） | threeview_3pass D（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| recycling bin | - | (4.0,9.0)多, 多1 | (6.5,4.0)多, 多1 | (4.0,8.0)多, 多1 |
| refrigerator | (4.0,7.0) | (1.0,5.0)✗3.6 | (8.0,3.5)✗5.3 | (2.0,5.0)✗2.8 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| recycling bin | - | - | (6.5,2.0)多, 多1 | (4.0,1.0)多, 多1 |
| refrigerator | (4.0,2.0) | - | (8.0,5.0)✗5.0 | (2.0,4.0)✗2.8 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| recycling bin | - | - | (4.0,2.0)多, 多1 | (8.0,1.0)多, 多1 |
| refrigerator | (7.0,2.0) | - | (3.5,5.0)✗4.6 | (5.0,4.0)✗2.8 |

- **baseline 问题**：多画 recycling bin ×1（GT 0，模型 1）
- **threeview 问题**：多画 recycling bin ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 recycling bin ×1（GT 0，模型 1）

### 样本 159 `scene0435_02`（scannet · route_planning）

Q：You are a robot beginning at the standing by the window and facing the window. You want to navigate to the white shoes. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward passing the bed 3. [please fill in] 4. Go forward until the white shoes. You have reached the final destination.

- QA：GT B | baseline B（对） | threeview A（错） | threeview_3pass B（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| standing by the window | - | (5.0,5.0)多, 多1 | (5.0,7.5)多, 多1 | (5.0,5.0)多, 多1 |
| white shoes | - | (5.0,8.0)多, 多1 | (5.0,7.5)多, 多1 | (5.0,8.0)多, 多1 |
| window | - | (5.0,4.0)多, 多1 | (5.0,8.5)多, 多1 | (5.0,3.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| standing by the window | - | - | (5.0,4.5)多, 多1 | (5.0,4.0)多, 多1 |
| white shoes | - | - | (5.0,1.5)多, 多1 | (5.0,0.0)多, 多1 |
| window | - | - | (5.0,6.0)多, 多1 | (5.0,5.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| standing by the window | - | - | (7.5,4.5)多, 多1 | (5.0,4.0)多, 多1 |
| white shoes | - | - | (7.5,1.5)多, 多1 | (8.0,0.0)多, 多1 |
| window | - | - | (8.5,6.0)多, 多1 | (3.0,5.0)多, 多1 |

- **baseline 问题**：多画 standing by the window ×1（GT 0，模型 1）；多画 window ×1（GT 0，模型 1）；多画 white shoes ×1（GT 0，模型 1）
- **threeview 问题**：多画 standing by the window ×1（GT 0，模型 1）；多画 window ×1（GT 0，模型 1）；多画 white shoes ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 standing by the window ×1（GT 0，模型 1）；多画 window ×1（GT 0，模型 1）；多画 white shoes ×1（GT 0，模型 1）

### 样本 160 `47204552`（arkitscenes · route_planning）

Q：You are a robot beginning at the tv facing the tv. You want to navigate to the sofa. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the sofa. You have reached the final destination.

- QA：GT C | baseline B（错） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | (5.0,8.0)多, 多1 | (5.0,3.0)多, 多1 | (5.0,8.0)多, 多1 |
| turn left | - | (3.0,5.0)多, 多1 | (3.5,6.0)多, 多1 | (3.0,5.0)多, 多1 |
| turn right | - | (7.0,5.0)多, 多1 | (6.5,6.0)多, 多1 | (7.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | (5.0,4.0)多, 多1 | (5.0,5.0)多, 多1 |
| turn left | - | - | (3.5,5.0)多, 多1 | (3.0,5.0)多, 多1 |
| turn right | - | - | (6.5,5.0)多, 多1 | (7.0,5.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | (3.0,4.0)多, 多1 | (8.0,5.0)多, 多1 |
| turn left | - | - | (6.0,5.0)多, 多1 | (5.0,5.0)多, 多1 |
| turn right | - | - | (6.0,5.0)多, 多1 | (5.0,5.0)多, 多1 |

- **baseline 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）
- **threeview 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）

### 样本 161 `3f15a9266d`（scannetpp · route_planning）

Q：You are a robot beginning at the yellow bookshelf facing the yellow bookshelf. You want to navigate to the the table with two monitors. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the table with two monitors. You have reached the final destination.

- QA：GT B | baseline B（对） | threeview B（对） | threeview_3pass B（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | (5.0,8.0)多, 多1 | (5.0,7.5)多, 多1 | (5.0,8.0)多, 多1 |
| turn left | - | (2.0,5.0)多, 多1 | (3.5,4.5)多, 多1 | (3.0,5.0)多, 多1 |
| turn right | - | (8.0,5.0)多, 多1 | (6.5,4.5)多, 多1 | (7.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | (5.0,4.0)多, 多1 | (5.0,5.0)多, 多1 |
| turn left | - | - | (3.5,5.0)多, 多1 | (3.0,5.0)多, 多1 |
| turn right | - | - | (6.5,5.0)多, 多1 | (7.0,5.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | (7.5,4.0)多, 多1 | (8.0,5.0)多, 多1 |
| turn left | - | - | (4.5,5.0)多, 多1 | (5.0,5.0)多, 多1 |
| turn right | - | - | (4.5,5.0)多, 多1 | (5.0,5.0)多, 多1 |

- **baseline 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）
- **threeview 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）

### 样本 162 `scene0412_00`（scannet · route_planning）

Q：You are a robot beginning at the orange traffic cone and facing the sink. You want to navigate to the elevator. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the metal rack 3. [please fill in] 4. Go forward until the cardboard boxes 5. [please fill in] 6. Go forward until the trash bin 7. [please fill in] 8. Go forward until the elevator. You have reached the final destination.

- QA：GT B | baseline D（错） | threeview D（错） | threeview_3pass D（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| elevator | - | (2.0,5.0)多, 多1 | (5.0,1.5)多, 多1 | (5.0,3.0)多, 多1 |
| orange traffic cone | - | (5.0,8.0)多, 多1 | (3.0,6.0)多, 多1 | (4.0,7.0)多, 多1 |
| sink | - | (8.0,6.0)多, 多1 | (8.0,5.0)多, 多1 | (8.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| elevator | - | - | (5.0,5.0)多, 多1 | (5.0,5.0)多, 多1 |
| orange traffic cone | - | - | (3.0,1.5)多, 多1 | (4.0,1.0)多, 多1 |
| sink | - | - | (8.0,4.0)多, 多1 | (8.0,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| elevator | - | - | (1.5,5.0)多, 多1 | (3.0,5.0)多, 多1 |
| orange traffic cone | - | - | (6.0,1.5)多, 多1 | (7.0,1.0)多, 多1 |
| sink | - | - | (5.0,4.0)多, 多1 | (5.0,3.0)多, 多1 |

- **baseline 问题**：多画 orange traffic cone ×1（GT 0，模型 1）；多画 sink ×1（GT 0，模型 1）；多画 elevator ×1（GT 0，模型 1）
- **threeview 问题**：多画 orange traffic cone ×1（GT 0，模型 1）；多画 sink ×1（GT 0，模型 1）；多画 elevator ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 orange traffic cone ×1（GT 0，模型 1）；多画 sink ×1（GT 0，模型 1）；多画 elevator ×1（GT 0，模型 1）

### 样本 163 `47430475`（arkitscenes · route_planning）

Q：You are a robot beginning at the door and facing the window. You want to navigate to the window. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the bookshelf 3. [please fill in] 4. Go forward until the wall 5. [please fill in] 6. Go forward until the window. You have reached the final destination.

- QA：GT B | baseline B（对） | threeview B（对） | threeview_3pass B（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | - | (1.0,5.0)多, 多1 | (1.5,5.0)多, 多1 | (1.0,5.0)多, 多1 |
| window | - | (8.0,4.0)多, 多1 | (5.0,8.5)多, 多1 | (5.0,1.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | - | - | (1.5,4.5)多, 多1 | (1.0,4.0)多, 多1 |
| window | - | - | (5.0,6.0)多, 多1 | (5.0,5.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | - | - | (5.0,4.5)多, 多1 | (5.0,4.0)多, 多1 |
| window | - | - | (8.5,6.0)多, 多1 | (1.0,5.0)多, 多1 |

- **baseline 问题**：多画 door ×1（GT 0，模型 1）；多画 window ×1（GT 0，模型 1）
- **threeview 问题**：多画 door ×1（GT 0，模型 1）；多画 window ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 door ×1（GT 0，模型 1）；多画 window ×1（GT 0，模型 1）

### 样本 164 `9071e139d9`（scannetpp · route_planning）

Q：You are a robot beginning at the whiteboard facing the whiteboard. You want to navigate to the bookshelf. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the blue trash bin 3. [please fill in] 4. Go forward until the bookshelf. You have reached the final destination.

- QA：GT C | baseline A（错） | threeview A（错） | threeview_3pass A（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | (5.0,5.0)多, 多1 | (5.0,5.0)多, 多1 | (5.0,5.0)多, 多1 |
| turn left | - | (2.0,3.0)多, (4.0,5.0)多, (5.0,7.0)多, (7.0,8.0)多, (8.0,2.0)多, 多5 | (3.0,4.0)多, (4.0,6.0)多, 多2 | (2.0,3.0)多, (3.0,7.0)多, (5.0,2.0)多, (7.0,8.0)多, (8.0,4.0)多, 多5 |
| turn right | - | (3.0,6.0)多, (6.0,4.0)多, 多2 | (7.0,3.0)多, 多1 | (4.0,6.0)多, (6.0,5.0)多, 多2 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | (5.0,5.0)多, 多1 | (5.0,5.0)多, 多1 |
| turn left | - | - | (3.0,4.0)多, (4.0,6.0)多, 多2 | (2.0,5.0)多, (3.0,5.0)多, (5.0,4.0)多, (7.0,5.0)多, (8.0,5.0)多, 多5 |
| turn right | - | - | (7.0,3.0)多, 多1 | (4.0,5.0)多, (6.0,5.0)多, 多2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | (5.0,5.0)多, 多1 | (5.0,5.0)多, 多1 |
| turn left | - | - | (4.0,4.0)多, (6.0,6.0)多, 多2 | (3.0,5.0)多, (7.0,5.0)多, (2.0,4.0)多, (8.0,5.0)多, (4.0,5.0)多, 多5 |
| turn right | - | - | (3.0,3.0)多, 多1 | (6.0,5.0)多, (5.0,5.0)多, 多2 |

- **baseline 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×2（GT 0，模型 2）；多画 turn left ×5（GT 0，模型 5）
- **threeview 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×2（GT 0，模型 2）
- **threeview_3pass 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×2（GT 0，模型 2）；多画 turn left ×5（GT 0，模型 5）

### 样本 165 `scene0696_01`（scannet · route_planning）

Q：You are a robot beginning at the microwave and facing the table. You want to navigate to the sofa. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the sofa. You have reached the final destination.

- QA：GT B | baseline B（对） | threeview A（错） | threeview_3pass A（错）
- 对齐：baseline: 2点 yaw=0° mirror=否 平移=(-1.0,-0.5) RMSE=0.35；threeview: 2点 yaw=180° mirror=否 平移=(9.0,10.2) RMSE=0.18；threeview_3pass: 2点 yaw=-63° mirror=否 平移=(-2.7,6.6) RMSE=0.27
- 补偿：baseline: 尺度=1.50 z偏移=+0.00；threeview: 尺度=1.20 z偏移=-0.25；threeview_3pass: 尺度=1.34 z偏移=+1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| microwave | - | (-0.5,1.0)多, 多1 | (8.2,1.6)多, 多1 | (2.2,-1.4)多, 多1 |
| sofa | (4.0,7.0) | (4.0,7.0)✓ | (4.0,7.0)✓ | (4.0,7.0)✓ |
| table | (4.0,4.0) | (4.0,4.0)✓ | (4.0,4.0)✓ | (4.0,4.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| microwave | - | - | (8.2,6.2)多, 多1 | (2.2,6.0)多, 多1 |
| sofa | (4.0,3.0) | - | (4.0,3.8)✓ | (4.0,3.0)✓ |
| table | (4.0,3.0) | - | (4.0,2.2)✓ | (4.0,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| microwave | - | - | (1.6,6.2)多, 多1 | (-1.4,6.0)多, 多1 |
| sofa | (7.0,3.0) | - | (7.0,3.8)✓ | (7.0,3.0)✓ |
| table | (4.0,3.0) | - | (4.0,2.2)✓ | (4.0,3.0)✓ |

- **baseline 问题**：多画 microwave ×1（GT 0，模型 1）
- **threeview 问题**：多画 microwave ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 microwave ×1（GT 0，模型 1）；z 整体偏低（平均 -1.0 格）

### 样本 166 `42446056`（arkitscenes · route_planning）

Q：You are a robot beginning at the foot of the bed facing the open door. You want to navigate to the red table. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. Go forward until the door 2. [please fill in] 3. Go forward until the red table. You have reached the final destination.

- QA：GT C | baseline C（对） | threeview C（对） | threeview_3pass C（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | (5.0,8.0)多, 多1 | (5.0,2.5)多, 多1 | (5.0,8.0)多, 多1 |
| turn left | - | (3.0,5.0)多, 多1 | (3.2,5.8)多, 多1 | (4.0,5.0)多, 多1 |
| turn right | - | (7.0,5.0)多, 多1 | (6.8,5.8)多, 多1 | (6.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | (5.0,4.5)多, 多1 | (5.0,4.0)多, 多1 |
| turn left | - | - | (3.2,4.5)多, 多1 | (4.0,3.0)多, 多1 |
| turn right | - | - | (6.8,4.5)多, 多1 | (6.0,3.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | (2.5,4.5)多, 多1 | (8.0,4.0)多, 多1 |
| turn left | - | - | (5.8,4.5)多, 多1 | (5.0,3.0)多, 多1 |
| turn right | - | - | (5.8,4.5)多, 多1 | (5.0,3.0)多, 多1 |

- **baseline 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）
- **threeview 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）

### 样本 167 `d755b3d9d8`（scannetpp · route_planning）

Q：You are a robot beginning at the blue chair and facing the nearest monitor. You want to navigate to the brown door. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the cabinet 3. [please fill in]. 4. Go forward until the brown door. You have reached the final destination.

- QA：GT D | baseline A（错） | threeview D（对） | threeview_3pass C（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blue chair | - | (4.0,7.0)多, 多1 | (5.5,5.8)多, 多1 | (5.0,6.0)多, 多1 |
| brown door | - | (1.0,4.0)多, 多1 | (1.0,8.0)多, 多1 | (1.0,5.0)多, 多1 |
| chair | (3.0,5.0), (5.0,6.0), (6.0,3.0) | 漏3 | 漏3 | 漏3 |
| door | (0.0,4.0) | 漏1 | 漏1 | 漏1 |
| monitor | (6.0,1.0), (4.0,7.0), (5.0,7.0) | 漏3 | 漏3 | 漏3 |
| nearest monitor | - | (5.0,5.0)多, 多1 | (5.5,4.5)多, 多1 | (6.0,4.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blue chair | - | - | (5.5,3.5)多, 多1 | (5.0,2.0)多, 多1 |
| brown door | - | - | (1.0,4.5)多, 多1 | (1.0,5.0)多, 多1 |
| chair | (3.0,2.0), (5.0,2.0), (6.0,2.0) | - | 漏3 | 漏3 |
| door | (0.0,3.0) | - | 漏1 | 漏1 |
| monitor | (6.0,3.0), (4.0,3.0), (5.0,3.0) | - | 漏3 | 漏3 |
| nearest monitor | - | - | (5.5,5.0)多, 多1 | (6.0,4.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blue chair | - | - | (5.8,3.5)多, 多1 | (6.0,2.0)多, 多1 |
| brown door | - | - | (8.0,4.5)多, 多1 | (5.0,5.0)多, 多1 |
| chair | (5.0,2.0), (6.0,2.0), (3.0,2.0) | - | 漏3 | 漏3 |
| door | (4.0,3.0) | - | 漏1 | 漏1 |
| monitor | (1.0,3.0), (7.0,3.0), (7.0,3.0) | - | 漏3 | 漏3 |
| nearest monitor | - | - | (4.5,5.0)多, 多1 | (4.0,4.0)多, 多1 |

- **baseline 问题**：漏画 monitor ×3（GT 3，模型 0）；多画 nearest monitor ×1（GT 0，模型 1）；多画 brown door ×1（GT 0，模型 1）；漏画 door ×1（GT 1，模型 0）；漏画 chair ×3（GT 3，模型 0）；多画 blue chair ×1（GT 0，模型 1）
- **threeview 问题**：漏画 monitor ×3（GT 3，模型 0）；多画 nearest monitor ×1（GT 0，模型 1）；多画 brown door ×1（GT 0，模型 1）；漏画 door ×1（GT 1，模型 0）；漏画 chair ×3（GT 3，模型 0）；多画 blue chair ×1（GT 0，模型 1）
- **threeview_3pass 问题**：漏画 monitor ×3（GT 3，模型 0）；多画 nearest monitor ×1（GT 0，模型 1）；多画 brown door ×1（GT 0，模型 1）；漏画 door ×1（GT 1，模型 0）；漏画 chair ×3（GT 3，模型 0）；多画 blue chair ×1（GT 0，模型 1）

### 样本 168 `scene0316_00`（scannet · route_planning）

Q：You are a robot beginning at the door facing the brown single-seat sofa. You want to navigate to the chair next to water fountain . You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. Go forward until the brown single-seat sofa. 2. [please fill in] 3. Go forward until passing by the brown two-seats sofa. 4. [please fill in] 5. Go forward until the chair. You have reached the final destination.

- QA：GT A | baseline C（错） | threeview C（错） | threeview_3pass C（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | (5.0,2.0)多, 多1 | - | (5.0,5.0)多, 多1 |
| turn left | - | (2.0,2.0)多, (8.0,2.0)多, (2.0,8.0)多, (8.0,8.0)多, 多4 | - | (3.0,2.0)多, (4.0,4.0)多, (7.0,6.0)多, (9.0,1.0)多, 多4 |
| turn right | - | (3.0,5.0)多, (8.0,5.0)多, (5.0,8.0)多, 多3 | - | (2.0,7.0)多, (5.0,8.0)多, (8.0,3.0)多, 多3 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | - | (5.0,5.0)多, 多1 |
| turn left | - | - | - | (3.0,2.0)多, (4.0,4.0)多, (7.0,6.0)多, (9.0,1.0)多, 多4 |
| turn right | - | - | - | (2.0,7.0)多, (5.0,8.0)多, (8.0,3.0)多, 多3 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | - | (5.0,5.0)多, 多1 |
| turn left | - | - | - | (2.0,2.0)多, (4.0,4.0)多, (6.0,6.0)多, (1.0,1.0)多, 多4 |
| turn right | - | - | - | (7.0,7.0)多, (8.0,8.0)多, (3.0,3.0)多, 多3 |

- **baseline 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×3（GT 0，模型 3）；多画 turn left ×4（GT 0，模型 4）
- **threeview_3pass 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×3（GT 0，模型 3）；多画 turn left ×4（GT 0，模型 4）

### 样本 169 `47332005`（arkitscenes · route_planning）

Q：You are a robot beginning at the sink and facing the heater. You want to navigate to the doorframe. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the doorframe. You have reached the final destination.

- QA：GT A | baseline B（错） | threeview A（对） | threeview_3pass B（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| doorframe | - | (1.0,5.0)多, 多1 | (8.5,1.5)多, 多1 | (1.0,5.0)多, 多1 |
| heater | - | (4.0,8.0)多, 多1 | (2.5,8.0)多, 多1 | (8.0,8.0)多, 多1 |
| sink | - | (5.0,5.0)多, 多1 | (4.8,3.5)多, 多1 | (5.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| doorframe | - | - | (8.5,5.0)多, 多1 | (1.0,5.0)多, 多1 |
| heater | - | - | (2.5,3.0)多, 多1 | (8.0,2.0)多, 多1 |
| sink | - | - | (4.8,4.5)多, 多1 | (5.0,4.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| doorframe | - | - | (1.5,5.0)多, 多1 | (5.0,5.0)多, 多1 |
| heater | - | - | (8.0,3.0)多, 多1 | (8.0,2.0)多, 多1 |
| sink | - | - | (3.5,4.5)多, 多1 | (5.0,4.0)多, 多1 |

- **baseline 问题**：多画 doorframe ×1（GT 0，模型 1）；多画 sink ×1（GT 0，模型 1）；多画 heater ×1（GT 0，模型 1）
- **threeview 问题**：多画 heater ×1（GT 0，模型 1）；多画 doorframe ×1（GT 0，模型 1）；多画 sink ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 doorframe ×1（GT 0，模型 1）；多画 sink ×1（GT 0，模型 1）；多画 heater ×1（GT 0，模型 1）

### 样本 170 `c5439f4607`（scannetpp · route_planning）

Q：You are a robot beginning at the computer and facing the computer. You want to navigate to the first aid cabinet. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the first aid cabinet. You have reached the final destination.

- QA：GT B | baseline C（错） | threeview B（对） | threeview_3pass C（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer | - | (5.0,4.0)多, 多1 | (4.5,4.5)多, 多1 | (5.0,4.0)多, 多1 |
| first aid cabinet | - | (2.0,3.0)多, 多1 | (2.5,1.5)多, 多1 | (2.0,8.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer | - | - | (4.5,4.0)多, 多1 | (5.0,4.0)多, 多1 |
| first aid cabinet | - | - | (2.5,6.5)多, 多1 | (2.0,7.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer | - | - | (4.5,4.0)多, 多1 | (4.0,4.0)多, 多1 |
| first aid cabinet | - | - | (1.5,6.5)多, 多1 | (8.0,7.0)多, 多1 |

- **baseline 问题**：多画 computer ×1（GT 0，模型 1）；多画 first aid cabinet ×1（GT 0，模型 1）
- **threeview 问题**：多画 computer ×1（GT 0，模型 1）；多画 first aid cabinet ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 computer ×1（GT 0，模型 1）；多画 first aid cabinet ×1（GT 0，模型 1）

### 样本 171 `scene0645_00`（scannet · route_planning）

Q：You are a robot beginning at the TV and facing the TV. You want to navigate to the glass coffee table. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in]. 2. Go forward until the coffee table. You have reached the final destination.

- QA：GT A | baseline A（对） | threeview A（对） | threeview_3pass A（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| glass coffee table | - | (5.0,5.0)多, 多1 | (5.0,5.0)多, 多1 | (5.0,5.0)多, 多1 |
| table | (5.0,5.0), (2.0,7.0), (4.0,5.0) | 漏3 | 漏3 | 漏3 |
| tv | (5.0,3.0) | (5.0,2.0)✓ | (5.0,8.5)✗5.5 | (5.0,9.0)✗6.0 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| glass coffee table | - | - | (5.0,2.0)多, 多1 | (5.0,1.0)多, 多1 |
| table | (5.0,3.0), (2.0,3.0), (4.0,2.0) | - | 漏3 | 漏3 |
| tv | (5.0,5.0) | - | (5.0,5.5)✓ | (5.0,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| glass coffee table | - | - | (5.0,2.0)多, 多1 | (5.0,1.0)多, 多1 |
| table | (5.0,3.0), (7.0,3.0), (5.0,2.0) | - | 漏3 | 漏3 |
| tv | (3.0,5.0) | - | (8.5,5.5)✗5.5 | (9.0,6.0)✗6.1 |

- **baseline 问题**：漏画 table ×3（GT 3，模型 0）；多画 glass coffee table ×1（GT 0，模型 1）
- **threeview 问题**：漏画 table ×3（GT 3，模型 0）；多画 glass coffee table ×1（GT 0，模型 1）
- **threeview_3pass 问题**：漏画 table ×3（GT 3，模型 0）；多画 glass coffee table ×1（GT 0，模型 1）

### 样本 172 `47332901`（arkitscenes · route_planning）

Q：You are a robot beginning at the fridge facing the fridge. You want to navigate to the oven . You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until window is on your right 3. [please fill in] 4. Go forward until oven is on your right. You have reached the final destination.

- QA：GT D | baseline D（对） | threeview C（错） | threeview_3pass D（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | (5.0,2.0)多, 多1 | (5.0,5.0)多, 多1 | (5.0,2.0)多, 多1 |
| turn left | - | (3.0,5.0)多, (7.0,2.0)多, (2.0,8.0)多, 多3 | (3.0,4.0)多, 多1 | (3.0,4.0)多, (4.0,8.0)多, (2.0,6.0)多, 多3 |
| turn right | - | (8.0,6.0)多, (4.0,1.0)多, (1.0,5.0)多, (6.0,9.0)多, 多4 | (7.0,6.0)多, 多1 | (7.0,4.0)多, (8.0,8.0)多, (6.0,6.0)多, (8.0,3.0)多, 多4 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | (5.0,4.5)多, 多1 | (5.0,4.0)多, 多1 |
| turn left | - | - | (3.0,4.0)多, 多1 | (3.0,3.0)多, (4.0,1.0)多, (2.0,2.0)多, 多3 |
| turn right | - | - | (7.0,4.0)多, 多1 | (7.0,3.0)多, (8.0,1.0)多, (6.0,2.0)多, (8.0,3.5)多, 多4 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| turn back | - | - | (5.0,4.5)多, 多1 | (2.0,4.0)多, 多1 |
| turn left | - | - | (4.0,4.0)多, 多1 | (4.0,3.0)多, (8.0,1.0)多, (6.0,2.0)多, 多3 |
| turn right | - | - | (6.0,4.0)多, 多1 | (4.0,3.0)多, (8.0,1.0)多, (6.0,2.0)多, (3.0,3.5)多, 多4 |

- **baseline 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×4（GT 0，模型 4）；多画 turn left ×3（GT 0，模型 3）
- **threeview 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×1（GT 0，模型 1）；多画 turn left ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 turn back ×1（GT 0，模型 1）；多画 turn right ×4（GT 0，模型 4）；多画 turn left ×3（GT 0，模型 3）

### 样本 173 `6115eddb86`（scannetpp · route_planning）

Q：You are a robot beginning at the chair and facing the table. You want to navigate to the apartment door. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the door. You have reached the final destination.

- QA：GT A | baseline A（对） | threeview C（错） | threeview_3pass A（对）
- 对齐：baseline: 2点 yaw=0° mirror=否 平移=(-3.5,-3.0) RMSE=0.35；threeview: 2点 yaw=0° mirror=否 平移=(-3.2,-3.0) RMSE=0.53；threeview_3pass: 2点 yaw=0° mirror=否 平移=(-3.5,-3.0) RMSE=0.35
- 补偿：baseline: 尺度=0.00 z偏移=+0.00；threeview: 尺度=0.00 z偏移=-1.50；threeview_3pass: 尺度=0.00 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| apartment door | - | (1.0,2.0)多, 多1 | (1.0,2.0)多, 多1 | (1.0,2.0)多, 多1 |
| chair | (1.0,2.0) | (1.0,2.0)✓, (1.0,2.0)多, 多1 | (1.0,2.0)✓, (1.0,2.0)多, 多1 | (1.0,2.0)✓, (1.0,2.0)多, 多1 |
| door | (6.0,1.0), (8.0,2.0) | 漏2 | 漏2 | 漏2 |
| table | (1.0,2.0) | (1.0,2.0)✓ | (1.0,2.0)✓ | (1.0,2.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| apartment door | - | - | (1.0,3.5)多, 多1 | (1.0,4.0)多, 多1 |
| chair | (1.0,2.0) | - | (1.0,2.0)✓, (1.0,2.0)多, 多1 | (1.0,2.0)✓, (1.0,2.0)多, 多1 |
| door | (6.0,4.0), (8.0,4.0) | - | 漏2 | 漏2 |
| table | (1.0,2.0) | - | (1.0,2.0)✓ | (1.0,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| apartment door | - | - | (2.0,3.5)多, 多1 | (2.0,4.0)多, 多1 |
| chair | (2.0,2.0) | - | (2.0,2.0)✓, (2.0,2.0)多, 多1 | (2.0,2.0)✓, (2.0,2.0)多, 多1 |
| door | (1.0,4.0), (2.0,4.0) | - | 漏2 | 漏2 |
| table | (2.0,2.0) | - | (2.0,2.0)✓ | (2.0,2.0)✓ |

- **baseline 问题**：漏画 door ×2（GT 2，模型 0）；多画 chair ×1（GT 1，模型 2）；多画 apartment door ×1（GT 0，模型 1）
- **threeview 问题**：漏画 door ×2（GT 2，模型 0）；多画 chair ×1（GT 1，模型 2）；多画 apartment door ×1（GT 0，模型 1）；chair-table 距离画错（GT 0.0，模型 1.5）；z 整体偏高（平均 +1.5 格）
- **threeview_3pass 问题**：漏画 door ×2（GT 2，模型 0）；多画 chair ×1（GT 1，模型 2）；多画 apartment door ×1（GT 0，模型 1）

### 样本 174 `scene0643_00`（scannet · route_planning）

Q：You are a robot beginning at the refrigerator and facing the refrigerator. You want to navigate to the recycling bin. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward about half a meter 3. [please fill in] 4. Go forward until the recycling bin. You have reached the final destination.

- QA：GT D | baseline C（错） | threeview D（对） | threeview_3pass C（错）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| recycling bin | - | (5.0,8.0)多, 多1 | (6.2,5.8)多, 多1 | (4.0,8.0)多, 多1 |
| refrigerator | (4.0,2.0) | (3.0,5.0)✗3.2 | (3.6,4.2)✗2.2 | (2.0,5.0)✗3.6 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| recycling bin | - | - | (6.2,2.2)多, 多1 | (4.0,2.0)多, 多1 |
| refrigerator | (4.0,2.0) | - | (3.6,4.5)✗2.5 | (2.0,4.0)✗2.8 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| recycling bin | - | - | (5.8,2.2)多, 多1 | (8.0,2.0)多, 多1 |
| refrigerator | (2.0,2.0) | - | (4.2,4.5)✗3.3 | (5.0,4.0)✗3.6 |

- **baseline 问题**：多画 recycling bin ×1（GT 0，模型 1）
- **threeview 问题**：多画 recycling bin ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 recycling bin ×1（GT 0，模型 1）

### 样本 175 `45662924`（arkitscenes · route_planning）

Q：You are a robot beginning at the lamp and facing the windows. You want to navigate to the painting seen in the other room. You will perform the following actions (Note: for each [please fill in], choose either 'turn back,' 'turn left,' or 'turn right.'): 1. [please fill in] 2. Go forward until the wall 3. [please fill in]. 4. Go forward through the doorway until the painting. You have reached the final destination.

- QA：GT A | baseline C（错） | threeview A（对） | threeview_3pass A（对）
- 对齐：baseline: 对齐失败(匹配实例<2)；threeview: 对齐失败(匹配实例<2)；threeview_3pass: 对齐失败(匹配实例<2)

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | - | (8.0,6.0)多, 多1 | (2.0,3.0)多, 多1 | (4.0,6.0)多, 多1 |
| painting seen in the other room | - | (5.0,9.0)多, 多1 | (8.5,8.0)多, 多1 | (5.0,9.0)多, 多1 |
| windows | - | (1.0,5.0)多, 多1 | (3.0,9.5)多, 多1 | (1.0,5.0)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | - | - | (2.0,4.5)多, 多1 | (4.0,5.0)多, 多1 |
| painting seen in the other room | - | - | (8.5,5.5)多, 多1 | (5.0,5.0)多, 多1 |
| windows | - | - | (3.0,6.0)多, 多1 | (1.0,5.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | - | - | (3.0,4.5)多, 多1 | (6.0,5.0)多, 多1 |
| painting seen in the other room | - | - | (8.0,5.5)多, 多1 | (9.0,5.0)多, 多1 |
| windows | - | - | (9.5,6.0)多, 多1 | (5.0,5.0)多, 多1 |

- **baseline 问题**：多画 windows ×1（GT 0，模型 1）；多画 painting seen in the other room ×1（GT 0，模型 1）；多画 lamp ×1（GT 0，模型 1）
- **threeview 问题**：多画 windows ×1（GT 0，模型 1）；多画 painting seen in the other room ×1（GT 0，模型 1）；多画 lamp ×1（GT 0，模型 1）
- **threeview_3pass 问题**：多画 windows ×1（GT 0，模型 1）；多画 painting seen in the other room ×1（GT 0，模型 1）；多画 lamp ×1（GT 0，模型 1）

### 样本 176 `27dd4da69e`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: sofa, trash can, power strip, tv?

- QA：GT C | baseline A（错） | threeview C（对） | threeview_3pass A（错）
- 对齐：baseline: yaw=-118° mirror=否 平移=(3.5,9.9) RMSE=1.88；threeview: yaw=38° mirror=否 平移=(5.0,-4.4) RMSE=1.59；threeview_3pass: yaw=-77° mirror=是(证据支持) 平移=(7.4,9.4) RMSE=1.84
- 补偿：baseline: 尺度=0.46 z偏移=+0.00；threeview: 尺度=0.64 z偏移=+0.00；threeview_3pass: 尺度=0.47 z偏移=+0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| power strip | (2.0,5.0) | (3.9,4.2)✗2.0 | (4.0,3.9)✗2.3 | (4.7,4.5)✗2.8 |
| sofa | (6.0,3.0) | (6.1,2.5)✓ | (5.9,2.1)✓ | (3.5,3.2)✗2.5 |
| trash can | (2.0,2.0), (2.0,1.0) | (3.4,2.4)✓, 漏1 | (3.0,2.7)✓, 漏1 | (3.4,1.7)✓, 漏1 |
| tv | (7.0,3.0) | (3.6,3.8)✗3.5 | (4.1,4.3)✗3.2 | (5.4,3.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| power strip | (2.0,5.0) | - | (4.0,1.0)✗4.5 | (4.7,1.5)✗4.4 |
| sofa | (6.0,2.0) | - | (5.9,3.0)✓ | (3.5,3.5)✗2.9 |
| trash can | (2.0,1.0), (2.0,2.0) | - | (3.0,1.5)✓, 漏1 | (3.4,1.5)✓, 漏1 |
| tv | (7.0,6.0) | - | (4.1,5.5)✗2.9 | (5.4,5.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| power strip | (5.0,5.0) | - | (3.9,1.0)✗4.1 | (4.5,1.5)✗3.5 |
| sofa | (3.0,2.0) | - | (2.1,3.0)✓ | (3.2,3.5)✓ |
| trash can | (2.0,1.0), (1.0,2.0) | - | (2.7,1.5)✓, 漏1 | (1.7,1.5)✓, 漏1 |
| tv | (3.0,6.0) | - | (4.3,5.5)✓ | (3.6,5.5)✓ |

- **baseline 问题**：漏画 trash can ×1（GT 2，模型 1）；power strip-sofa 距离画错（GT 4.5，模型 6.1）；power strip-trash can 距离画错（GT 3.0，模型 4.1）；power strip-tv 距离画错（GT 5.4，模型 1.0）；power strip→tv 方向错（GT W，模型 NE）；sofa-trash can 距离画错（GT 4.1，模型 5.8）；sofa-tv 距离画错（GT 1.0，模型 6.0）；sofa→tv 方向错（GT W，模型 SE）
- **threeview 问题**：漏画 trash can ×1（GT 2，模型 1）；power strip→trash can 方向错（GT N，模型 NE）；power strip-tv 距离画错（GT 5.4，模型 0.7）；power strip→tv 方向错（GT W，模型 S）；sofa-tv 距离画错（GT 1.0，模型 4.5）；sofa→tv 方向错（GT W，模型 SE）；trash can-tv 距离画错（GT 5.1，模型 3.2）；trash can→tv 方向错（GT W，模型 SW）
- **threeview_3pass 问题**：漏画 trash can ×1（GT 2，模型 1）；power strip→sofa 方向错（GT NW，模型 NE）；power strip-trash can 距离画错（GT 3.0，模型 6.4）；power strip→trash can 方向错（GT N，模型 NE）；power strip-tv 距离画错（GT 5.4，模型 2.2）；power strip→tv 方向错（GT W，模型 NW）；sofa→trash can 方向错（GT E，模型 N）；sofa-tv 距离画错（GT 1.0，模型 4.0）

### 样本 177 `scene0353_00`（scannet · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: refrigerator, closet, backpack, bed?

- QA：GT B | baseline A（错） | threeview C（错） | threeview_3pass C（错）
- 对齐：baseline: yaw=133° mirror=否 平移=(11.7,4.7) RMSE=1.22；threeview: yaw=-117° mirror=否 平移=(0.5,8.9) RMSE=0.97；threeview_3pass: yaw=-140° mirror=否 平移=(3.7,10.8) RMSE=0.88
- 补偿：baseline: 尺度=0.63 z偏移=+0.00；threeview: 尺度=0.75 z偏移=-1.50；threeview_3pass: 尺度=0.75 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (4.0,5.0), (2.0,4.0) | (2.7,4.8)✓, 漏1 | (1.7,5.0)✓, 漏1 | (3.0,5.5)✓, 漏1 |
| bed | (2.0,4.0) | (4.0,4.3)✗2.1 | (3.2,3.0)✓ | (3.4,3.9)✓ |
| closet | (7.0,4.0) | (6.2,3.8)✓ | (6.2,4.0)✓ | (6.6,3.6)✓ |
| refrigerator | (5.0,5.0) | 漏1 | 漏1 | 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (4.0,1.0), (2.0,1.0) | - | (1.7,1.0)✓, 漏1 | (3.0,1.0)✓, 漏1 |
| bed | (2.0,4.0) | - | (3.2,1.5)✗2.8 | (3.4,1.0)✗3.3 |
| closet | (7.0,3.0) | - | (6.2,3.5)✓ | (6.6,4.0)✓ |
| refrigerator | (5.0,2.0) | - | 漏1 | 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (5.0,1.0), (4.0,1.0) | - | (5.0,1.0)✓, 漏1 | (5.5,1.0)✓, 漏1 |
| bed | (4.0,4.0) | - | (3.0,1.5)✗2.7 | (3.9,1.0)✗3.0 |
| closet | (4.0,3.0) | - | (4.0,3.5)✓ | (3.6,4.0)✓ |
| refrigerator | (5.0,2.0) | - | 漏1 | 漏1 |

- **baseline 问题**：漏画 backpack ×1（GT 2，模型 1）；漏画 refrigerator ×1（GT 1，模型 0）；backpack-bed 距离画错（GT 0.0，模型 2.2）；backpack→bed 方向错（GT NE，模型 W）；backpack-closet 距离画错（GT 3.2，模型 5.8）；bed-closet 距离画错（GT 5.0，模型 3.6）
- **threeview 问题**：漏画 backpack ×1（GT 2，模型 1）；漏画 refrigerator ×1（GT 1，模型 0）；backpack-bed 距离画错（GT 0.0，模型 3.4）；backpack→bed 方向错（GT NE，模型 NW）；backpack-closet 距离画错（GT 3.2，模型 6.2）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：漏画 backpack ×1（GT 2，模型 1）；漏画 refrigerator ×1（GT 1，模型 0）；backpack-bed 距离画错（GT 0.0，模型 2.2）；backpack→bed 方向错（GT NE，模型 N）；backpack-closet 距离画错（GT 3.2，模型 5.4）；backpack→closet 方向错（GT W，模型 NW）

### 样本 178 `09c1414f1b`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: blanket, trash can, microwave, plant?

- QA：GT C | baseline B（错） | threeview B（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=43° mirror=否 平移=(3.4,-3.8) RMSE=1.48；threeview: yaw=45° mirror=否 平移=(3.9,-4.5) RMSE=1.24；threeview_3pass: yaw=-111° mirror=是(未证实) 平移=(9.9,5.7) RMSE=2.43
- 补偿：baseline: 尺度=0.71 z偏移=+0.00；threeview: 尺度=0.84 z偏移=-0.50；threeview_3pass: 尺度=0.45 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blanket | (5.0,7.0), (5.0,6.0), (4.0,5.0) | (3.2,3.6)✓, 漏2 | (3.8,3.8)✓, 漏2 | (2.8,3.3)✗2.1, 漏2 |
| microwave | (2.0,0.0) | (3.0,0.6)✓ | (3.2,1.4)✓ | (3.5,4.0)✗4.3 |
| plant | (1.0,7.0), (1.0,6.0), (1.0,5.0), (6.0,3.0), (2.0,0.0) | (6.6,3.0)✓, 漏4 | (6.8,3.2)✓, 漏4 | (2.0,5.0)✓, 漏4 |
| trash can | (1.0,2.0) | (1.2,3.7)✓ | (0.2,2.6)✓ | (0.6,2.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blanket | (5.0,4.0), (5.0,4.0), (4.0,3.0) | - | (3.8,2.5)✓, 漏2 | (2.8,3.0)✓, 漏2 |
| microwave | (2.0,5.0) | - | (3.2,5.0)✓ | (3.5,5.0)✓ |
| plant | (1.0,7.0), (1.0,3.0), (1.0,4.0), (6.0,2.0), (2.0,6.0) | - | (6.8,4.0)✗2.1, 漏4 | (2.0,4.0)✓, 漏4 |
| trash can | (1.0,1.0) | - | (0.2,2.0)✓ | (0.6,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blanket | (7.0,4.0), (6.0,4.0), (5.0,3.0) | - | (3.8,2.5)✓, 漏2 | (3.3,3.0)✓, 漏2 |
| microwave | (0.0,5.0) | - | (1.4,5.0)✓ | (4.0,5.0)✗4.0 |
| plant | (7.0,7.0), (6.0,3.0), (5.0,4.0), (3.0,2.0), (0.0,6.0) | - | (3.2,4.0)✓, 漏4 | (5.0,4.0)✓, 漏4 |
| trash can | (2.0,1.0) | - | (2.6,2.0)✓ | (2.7,2.0)✓ |

- **baseline 问题**：漏画 blanket ×2（GT 3，模型 1）；漏画 plant ×4（GT 5，模型 1）；blanket-microwave 距离画错（GT 5.4，模型 4.2）；blanket→microwave 方向错（GT NE，模型 N）；blanket-plant 距离画错（GT 2.8，模型 5.0）；blanket→plant 方向错（GT NE，模型 W）；blanket-trash can 距离画错（GT 4.2，模型 2.8）；blanket→trash can 方向错（GT NE，模型 E）
- **threeview 问题**：漏画 blanket ×2（GT 3，模型 1）；漏画 plant ×4（GT 5，模型 1）；blanket-microwave 距离画错（GT 5.4，模型 2.9）；blanket→microwave 方向错（GT NE，模型 N）；blanket→plant 方向错（GT NE，模型 W）；blanket→trash can 方向错（GT NE，模型 E）；microwave-plant 距离画错（GT 0.0，模型 4.7）；microwave→plant 方向错（GT S，模型 SW）
- **threeview_3pass 问题**：漏画 blanket ×2（GT 3，模型 1）；漏画 plant ×4（GT 5，模型 1）；blanket-microwave 距离画错（GT 5.4，模型 2.2）；blanket→microwave 方向错（GT NE，模型 SW）；blanket-plant 距离画错（GT 2.8，模型 4.2）；blanket→plant 方向错（GT NE，模型 SE）；blanket→trash can 方向错（GT NE，模型 E）；microwave-plant 距离画错（GT 0.0，模型 4.1）

### 样本 179 `scene0608_00`（scannet · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: lamp, clock, pillow, table?

- QA：GT A | baseline A（对） | threeview B（错） | threeview_3pass A（对）
- 对齐：baseline: yaw=124° mirror=否 平移=(10.9,4.4) RMSE=2.07；threeview: yaw=-45° mirror=否 平移=(-1.7,4.5) RMSE=1.61；threeview_3pass: yaw=147° mirror=否 平移=(10.3,6.5) RMSE=2.03
- 补偿：baseline: 尺度=0.45 z偏移=+0.00；threeview: 尺度=1.18 z偏移=-0.35；threeview_3pass: 尺度=0.54 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| clock | (7.0,7.0) | (5.4,6.1)✓ | (5.0,4.3)✗3.3 | (4.5,6.2)✗2.6 |
| lamp | (5.0,2.0) | (5.0,4.2)✗2.2 | (5.0,4.3)✗2.3 | (4.9,4.0)✓ |
| pillow | (2.0,4.0), (1.0,3.0) | (3.4,5.9)✗2.3, 漏1 | (2.0,4.0)✓, 漏1 | (2.4,5.0)✓, (2.8,4.7)✗2.5 |
| table | (3.0,4.0), (4.0,7.0), (5.0,2.0) | (4.2,3.8)✓, 漏2 | (5.0,4.3)✗2.0, 漏2 | (4.3,3.1)✓, 漏2 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| clock | (7.0,6.0) | - | (5.0,3.7)✗3.0 | (4.5,7.0)✗2.7 |
| lamp | (5.0,4.0) | - | (5.0,4.4)✓ | (4.9,5.0)✓ |
| pillow | (2.0,3.0), (1.0,4.0) | - | (2.0,3.1)✓, 漏1 | (2.4,3.0)✓, (2.8,3.0)✗2.1 |
| table | (3.0,2.0), (4.0,2.0), (5.0,3.0) | - | (5.0,2.9)✓, 漏2 | (4.3,2.0)✓, 漏2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| clock | (7.0,6.0) | - | (4.3,3.7)✗3.5 | (6.2,7.0)✓ |
| lamp | (2.0,4.0) | - | (4.3,4.4)✗2.4 | (4.0,5.0)✗2.2 |
| pillow | (4.0,3.0), (3.0,4.0) | - | (4.0,3.1)✓, 漏1 | (4.7,3.0)✓, (4.7,3.0)✗2.2, (5.0,3.0)多 |
| table | (4.0,2.0), (7.0,2.0), (2.0,3.0) | - | (4.3,2.9)✓, 漏2 | (3.1,2.0)✓, 漏2 |

- **baseline 问题**：漏画 pillow ×1（GT 2，模型 1）；漏画 table ×2（GT 3，模型 1）；clock-lamp 距离画错（GT 5.4，模型 4.2）；clock-pillow 距离画错（GT 5.8，模型 4.5）；clock→pillow 方向错（GT NE，模型 E）；clock-table 距离画错（GT 3.0，模型 5.8）；lamp-pillow 距离画错（GT 3.6，模型 5.1）；lamp-table 距离画错（GT 0.0，模型 2.0）
- **threeview 问题**：漏画 pillow ×1（GT 2，模型 1）；漏画 table ×2（GT 3，模型 1）；clock-lamp 距离画错（GT 5.4，模型 0.0）；clock→lamp 方向错（GT N，模型 E）；clock-pillow 距离画错（GT 5.8，模型 2.6）；clock→pillow 方向错（GT NE，模型 E）；clock-table 距离画错（GT 3.0，模型 0.0）；clock→table 方向错（GT NE，模型 E）
- **threeview_3pass 问题**：漏画 table ×2（GT 3，模型 1）；clock-lamp 距离画错（GT 5.4，模型 4.2）；clock-pillow 距离画错（GT 5.8，模型 4.1）；clock-table 距离画错（GT 3.0，模型 5.8）；clock→table 方向错（GT NE，模型 N）；lamp→pillow 方向错（GT SE，模型 E）；lamp-table 距离画错（GT 0.0，模型 2.0）；lamp→table 方向错（GT SE，模型 NE）

### 样本 180 `25f3b7a318`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: toilet, shoes, laptop, blanket?

- QA：GT C | baseline C（对） | threeview C（对） | threeview_3pass C（对）
- 对齐：baseline: yaw=-109° mirror=是(未证实) 平移=(11.3,7.2) RMSE=1.12；threeview: yaw=22° mirror=是(未证实) 平移=(-1.0,6.7) RMSE=0.96；threeview_3pass: yaw=-138° mirror=是(证据支持) 平移=(10.5,4.4) RMSE=2.17
- 补偿：baseline: 尺度=1.52 z偏移=+0.00；threeview: 尺度=1.63 z偏移=-0.50；threeview_3pass: 尺度=0.58 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blanket | (5.0,2.0) | (5.1,3.6)✓ | (5.2,2.9)✓ | (3.5,4.8)✗3.1 |
| laptop | (7.0,7.0) | (7.6,5.9)✓ | (7.3,6.4)✓ | (4.4,4.7)✗3.5 |
| shoes | (2.0,6.0), (2.0,6.0), (2.0,6.0), (2.0,6.0), (2.0,6.0), (2.0,7.0), (2.0,7.0), (2.0,6.0), (2.0,6.0), (1.0,7.0) | (1.3,6.5)✓, 漏9 | (1.4,5.8)✓, 漏9 | (3.7,7.2)✓, 漏9 |
| toilet | (1.0,3.0) | 漏1 | 漏1 | (3.4,2.3)✗2.5 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blanket | (5.0,2.0) | - | (5.2,3.0)✓ | (3.5,2.0)✓ |
| laptop | (7.0,4.0) | - | (7.3,4.0)✓ | (4.4,3.0)✗2.8 |
| shoes | (2.0,1.0), (2.0,1.0), (2.0,1.0), (2.0,2.0), (2.0,2.0), (2.0,2.0), (2.0,3.0), (2.0,3.0), (2.0,3.0), (1.0,1.0) | - | (1.4,1.0)✓, 漏9 | (3.7,1.0)✓, 漏9 |
| toilet | (1.0,2.0) | - | 漏1 | (3.4,2.0)✗2.4 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blanket | (2.0,2.0) | - | (2.9,3.0)✓ | (4.8,2.0)✗2.8 |
| laptop | (7.0,4.0) | - | (6.4,4.0)✓ | (4.7,3.0)✗2.5 |
| shoes | (6.0,1.0), (6.0,1.0), (6.0,1.0), (6.0,2.0), (6.0,2.0), (7.0,2.0), (7.0,3.0), (6.0,3.0), (6.0,3.0), (7.0,1.0) | - | (5.8,1.0)✓, 漏9 | (7.2,1.0)✓, 漏9 |
| toilet | (3.0,2.0) | - | 漏1 | (2.3,2.0)✓ |

- **baseline 问题**：漏画 shoes ×9（GT 10，模型 1）；漏画 toilet ×1（GT 1，模型 0）；blanket-laptop 距离画错（GT 5.4，模型 2.2）；blanket→laptop 方向错（GT S，模型 SW）；blanket-shoes 距离画错（GT 5.0，模型 3.2）
- **threeview 问题**：漏画 shoes ×9（GT 10，模型 1）；漏画 toilet ×1（GT 1，模型 0）；blanket-laptop 距离画错（GT 5.4，模型 2.5）；blanket→laptop 方向错（GT S，模型 SW）；blanket-shoes 距离画错（GT 5.0，模型 2.9）；laptop-shoes 距离画错（GT 5.0，模型 3.6）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：漏画 shoes ×9（GT 10，模型 1）；blanket-laptop 距离画错（GT 5.4，模型 1.4）；blanket→laptop 方向错（GT S，模型 W）；blanket→shoes 方向错（GT SE，模型 S）；blanket→toilet 方向错（GT E，模型 N）；laptop→shoes 方向错（GT E，模型 S）；laptop-toilet 距离画错（GT 7.2，模型 4.5）；laptop→toilet 方向错（GT NE，模型 N）

### 样本 181 `scene0426_00`（scannet · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: bed, chair, window, tv?

- QA：GT B | baseline B（对） | threeview D（错） | threeview_3pass D（错）
- 对齐：baseline: yaw=-157° mirror=是(证据支持) 平移=(10.9,2.0) RMSE=1.45；threeview: yaw=-93° mirror=否 平移=(-1.2,8.8) RMSE=0.72；threeview_3pass: yaw=57° mirror=否 平移=(5.7,-2.6) RMSE=1.57
- 补偿：baseline: 尺度=0.73 z偏移=+0.00；threeview: 尺度=0.90 z偏移=+0.00；threeview_3pass: 尺度=0.60 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (2.0,3.0) | (4.3,4.6)✗2.7 | (3.2,3.6)✓ | (2.4,4.7)✓ |
| chair | (4.0,1.0), (6.0,7.0), (5.0,1.0) | (4.7,7.1)✓, 漏2 | (6.0,6.2)✓, 漏2 | (3.5,1.9)✓, 漏2 |
| tv | (7.0,3.0) | (5.4,1.9)✓ | (6.8,3.4)✓ | (5.4,2.7)✓ |
| window | (1.0,4.0) | (1.6,3.4)✓ | (0.0,3.8)✓ | (2.6,1.7)✗2.8 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (2.0,3.0) | - | (3.2,2.5)✓ | (2.4,2.0)✓ |
| chair | (4.0,2.0), (6.0,2.0), (5.0,2.0) | - | (6.0,2.0)✓, 漏2 | (3.5,2.0)✓, 漏2 |
| tv | (7.0,4.0) | - | (6.8,5.0)✓ | (5.4,5.0)✓ |
| window | (1.0,6.0) | - | (0.0,6.0)✓ | (2.6,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (3.0,3.0) | - | (3.6,2.5)✓ | (4.7,2.0)✓ |
| chair | (1.0,2.0), (7.0,2.0), (1.0,2.0) | - | (6.2,2.0)✓, 漏2 | (1.9,2.0)✓, 漏2 |
| tv | (3.0,4.0) | - | (3.4,5.0)✓ | (2.7,5.0)✓ |
| window | (4.0,6.0) | - | (3.8,6.0)✓ | (1.7,6.0)✗2.3 |

- **baseline 问题**：漏画 chair ×2（GT 3，模型 1）；bed→chair 方向错（GT W，模型 S）；bed-tv 距离画错（GT 5.0，模型 4.0）；bed→tv 方向错（GT W，模型 NW）；bed-window 距离画错（GT 1.4，模型 4.0）；bed→window 方向错（GT SE，模型 NE）；chair-tv 距离画错（GT 2.8，模型 7.3）；chair→tv 方向错（GT W，模型 N）
- **threeview 问题**：漏画 chair ×2（GT 3，模型 1）；bed-chair 距离画错（GT 2.8，模型 4.2）；bed→chair 方向错（GT W，模型 SW）；bed-window 距离画错（GT 1.4，模型 3.5）；bed→window 方向错（GT SE，模型 E）；chair→tv 方向错（GT W，模型 N）；chair-window 距离画错（GT 4.2，模型 7.2）；tv-window 距离画错（GT 6.1，模型 7.5）
- **threeview_3pass 问题**：漏画 chair ×2（GT 3，模型 1）；bed-chair 距离画错（GT 2.8，模型 5.0）；bed→chair 方向错（GT W，模型 N）；bed→tv 方向错（GT W，模型 NW）；bed-window 距离画错（GT 1.4，模型 5.0）；bed→window 方向错（GT SE，模型 N）；chair→tv 方向错（GT W，模型 SW）；chair-window 距离画错（GT 4.2，模型 1.4）

### 样本 182 `d755b3d9d8`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: monitor, laptop, printer, keyboard?

- QA：GT C | baseline D（错） | threeview D（错） | threeview_3pass D（错）
- 对齐：baseline: yaw=179° mirror=是(未证实) 平移=(9.7,-0.3) RMSE=0.97；threeview: yaw=175° mirror=是(未证实) 平移=(9.2,0.2) RMSE=1.48；threeview_3pass: yaw=175° mirror=是(未证实) 平移=(9.3,0.1) RMSE=1.20
- 补偿：baseline: 尺度=1.23 z偏移=+0.00；threeview: 尺度=1.43 z偏移=-2.35；threeview_3pass: 尺度=1.27 z偏移=-2.25

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| keyboard | (4.0,7.0), (5.0,7.0) | (4.8,7.2)✓, 漏1 | (4.8,5.9)✓, 漏1 | (5.0,6.9)✓, 漏1 |
| laptop | (6.0,6.0) | (7.3,5.9)✓ | (7.6,5.4)✓ | (7.4,5.4)✓ |
| monitor | (6.0,1.0), (4.0,7.0), (5.0,7.0) | (4.8,2.2)✓, 漏2 | (4.6,3.8)✗3.2, 漏2 | (4.6,3.1)✗2.5, 漏2 |
| printer | (1.0,6.0), (1.0,7.0) | (1.1,4.8)✓, 漏1 | (1.1,4.8)✓, 漏1 | (1.0,4.7)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| keyboard | (4.0,2.0), (5.0,2.0) | - | (4.8,1.9)✓, 漏1 | (5.0,1.8)✓, 漏1 |
| laptop | (6.0,2.0) | - | (7.6,2.1)✓ | (7.4,2.2)✓ |
| monitor | (6.0,3.0), (4.0,3.0), (5.0,3.0) | - | (4.6,3.1)✓, 漏2 | (4.6,3.2)✓, 漏2 |
| printer | (1.0,3.0), (1.0,3.0) | - | (1.1,2.4)✓, 漏1 | (1.0,2.2)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| keyboard | (7.0,2.0), (7.0,2.0) | - | (5.9,1.9)✓, 漏1 | (6.9,1.8)✓, 漏1 |
| laptop | (6.0,2.0) | - | (5.4,2.1)✓ | (5.4,2.2)✓ |
| monitor | (1.0,3.0), (7.0,3.0), (7.0,3.0) | - | (3.8,3.1)✗2.8, 漏2 | (3.1,3.2)✗2.1, 漏2 |
| printer | (6.0,3.0), (7.0,3.0) | - | (4.8,2.4)✓, 漏1 | (4.7,2.2)✓, 漏1 |

- **baseline 问题**：漏画 keyboard ×1（GT 2，模型 1）；漏画 printer ×1（GT 2，模型 1）；漏画 monitor ×2（GT 3，模型 1）；keyboard-monitor 距离画错（GT 0.0，模型 4.0）；keyboard→printer 方向错（GT E，模型 NE）；laptop-monitor 距离画错（GT 1.4，模型 3.6）；monitor→printer 方向错（GT E，模型 SE）
- **threeview 问题**：漏画 keyboard ×1（GT 2，模型 1）；漏画 printer ×1（GT 2，模型 1）；漏画 monitor ×2（GT 3，模型 1）；keyboard→laptop 方向错（GT NW，模型 W）；keyboard-monitor 距离画错（GT 0.0，模型 1.5）；z 整体偏高（平均 +2.2 格）
- **threeview_3pass 问题**：漏画 keyboard ×1（GT 2，模型 1）；漏画 printer ×1（GT 2，模型 1）；漏画 monitor ×2（GT 3，模型 1）；keyboard-monitor 距离画错（GT 0.0，模型 3.0）；keyboard→printer 方向错（GT E，模型 NE）；laptop-monitor 距离画错（GT 1.4，模型 2.8）；monitor→printer 方向错（GT E，模型 SE）；z 整体偏高（平均 +2.1 格）

### 样本 183 `scene0207_02`（scannet · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: towel, bed, nightstand, backpack?

- QA：GT D | baseline A（错） | threeview A（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=149° mirror=是(证据支持) 平移=(4.7,-3.5) RMSE=1.00；threeview: yaw=-177° mirror=是(未证实) 平移=(7.9,-1.5) RMSE=1.05；threeview_3pass: yaw=137° mirror=是(证据支持) 平移=(3.4,-3.2) RMSE=1.16
- 补偿：baseline: 尺度=0.65 z偏移=+0.00；threeview: 尺度=0.72 z偏移=-1.35；threeview_3pass: 尺度=0.58 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (6.0,4.0), (5.0,4.0) | (5.6,4.4)✓, 漏1 | (5.2,3.8)✓, 漏1 | (5.7,4.2)✓, 漏1 |
| bed | (4.0,2.0) | (3.4,3.4)✓ | (3.1,3.7)✓ | (3.6,3.7)✓ |
| nightstand | (5.0,2.0) | (4.8,1.9)✓ | (5.3,2.4)✓ | (4.5,2.1)✓ |
| towel | (2.0,5.0), (3.0,6.0) | (3.2,4.3)✓, 漏1 | (3.4,4.1)✓, 漏1 | (3.2,4.1)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (6.0,2.0), (5.0,1.0) | - | (5.2,0.1)✓, 漏1 | (5.7,1.0)✓, 漏1 |
| bed | (4.0,2.0) | - | (3.1,2.1)✓ | (3.6,2.0)✓ |
| nightstand | (5.0,1.0) | - | (5.3,1.1)✓ | (4.5,2.0)✓ |
| towel | (2.0,3.0), (3.0,2.0) | - | (3.4,2.9)✓, 漏1 | (3.2,3.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (4.0,2.0), (4.0,1.0) | - | (3.8,0.1)✓, 漏1 | (4.2,1.0)✓, 漏1 |
| bed | (2.0,2.0) | - | (3.7,2.1)✓ | (3.7,2.0)✓ |
| nightstand | (2.0,1.0) | - | (2.4,1.1)✓ | (2.1,2.0)✓ |
| towel | (5.0,3.0), (6.0,2.0) | - | (4.1,2.9)✓, 漏1 | (4.1,3.0)✓, 漏1 |

- **baseline 问题**：漏画 backpack ×1（GT 2，模型 1）；漏画 towel ×1（GT 2，模型 1）；backpack-bed 距离画错（GT 2.2，模型 3.6）；backpack-nightstand 距离画错（GT 2.0，模型 4.1）；backpack→towel 方向错（GT SE，模型 E）；bed-nightstand 距离画错（GT 1.0，模型 3.2）；bed→nightstand 方向错（GT W，模型 NW）；bed-towel 距离画错（GT 3.6，模型 1.4）
- **threeview 问题**：漏画 backpack ×1（GT 2，模型 1）；漏画 towel ×1（GT 2，模型 1）；backpack→bed 方向错（GT NE，模型 E）；backpack→towel 方向错（GT SE，模型 E）；bed-nightstand 距离画错（GT 1.0，模型 3.6）；bed→nightstand 方向错（GT W，模型 NW）；bed-towel 距离画错（GT 3.6，模型 0.7）；bed→towel 方向错（GT SE，模型 SW）
- **threeview_3pass 问题**：漏画 backpack ×1（GT 2，模型 1）；漏画 towel ×1（GT 2，模型 1）；backpack-bed 距离画错（GT 2.2，模型 3.6）；backpack→bed 方向错（GT NE，模型 E）；backpack-nightstand 距离画错（GT 2.0，模型 4.1）；backpack→nightstand 方向错（GT N，模型 NE）；backpack-towel 距离画错（GT 2.8，模型 4.2）；backpack→towel 方向错（GT SE，模型 E）

### 样本 184 `27dd4da69e`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: door, basket, trash can, microwave?

- QA：GT D | baseline C（错） | threeview C（错） | threeview_3pass C（错）
- 对齐：baseline: yaw=-58° mirror=是(未证实) 平移=(5.9,10.0) RMSE=1.81；threeview: yaw=51° mirror=是(证据支持) 平移=(-1.5,2.1) RMSE=1.24；threeview_3pass: yaw=-61° mirror=是(未证实) 平移=(5.7,9.9) RMSE=1.99
- 补偿：baseline: 尺度=0.61 z偏移=+0.00；threeview: 尺度=0.81 z偏移=-1.00；threeview_3pass: 尺度=0.53 z偏移=-0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (8.0,4.0) | (4.5,3.6)✗3.5 | (6.0,2.5)✗2.5 | (4.1,3.5)✗3.9 |
| door | (1.0,5.0), (5.0,6.0), (6.0,7.0), (0.0,5.0), (4.0,6.0) | (2.7,5.3)✓, 漏4 | (4.4,7.0)✓, 漏4 | (2.6,5.1)✓, 漏4 |
| microwave | (3.0,3.0) | (3.4,4.3)✓ | (4.2,3.5)✓ | (4.3,4.2)✓ |
| trash can | (2.0,2.0), (2.0,1.0) | (3.4,0.8)✓, 漏1 | (3.5,2.0)✓, 漏1 | (3.0,1.1)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (8.0,2.0) | - | (6.0,3.0)✗2.2 | (4.1,3.5)✗4.2 |
| door | (1.0,4.0), (5.0,4.0), (6.0,4.0), (0.0,4.0), (4.0,4.0) | - | (4.4,3.5)✓, 漏4 | (2.6,4.5)✓, 漏4 |
| microwave | (3.0,4.0) | - | (4.2,4.5)✓ | (4.3,3.5)✓ |
| trash can | (2.0,1.0), (2.0,2.0) | - | (3.5,1.5)✓, 漏1 | (3.0,1.5)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (4.0,2.0) | - | (2.5,3.0)✓ | (3.5,3.5)✓ |
| door | (5.0,4.0), (6.0,4.0), (7.0,4.0), (5.0,4.0), (6.0,4.0) | - | (7.0,3.5)✓, 漏4 | (5.1,4.5)✓, 漏4 |
| microwave | (3.0,4.0) | - | (3.5,4.5)✓ | (4.2,3.5)✓ |
| trash can | (2.0,1.0), (1.0,2.0) | - | (2.0,1.5)✓, 漏1 | (1.1,1.5)✓, 漏1 |

- **baseline 问题**：漏画 trash can ×1（GT 2，模型 1）；漏画 door ×4（GT 5，模型 1）；basket→door 方向错（GT E，模型 SE）；basket-microwave 距离画错（GT 5.1，模型 2.2）；basket→microwave 方向错（GT E，模型 SE）；basket-trash can 距离画错（GT 6.3，模型 5.0）；basket→trash can 方向错（GT NE，模型 N）；door→microwave 方向错（GT N，模型 NW）
- **threeview 问题**：漏画 trash can ×1（GT 2，模型 1）；漏画 door ×4（GT 5，模型 1）；basket-door 距离画错（GT 3.6，模型 5.8）；basket→door 方向错（GT E，模型 S）；basket-microwave 距离画错（GT 5.1，模型 2.5）；basket→microwave 方向错（GT E，模型 SE）；basket-trash can 距离画错（GT 6.3，模型 3.2）；basket→trash can 方向错（GT NE，模型 E）
- **threeview_3pass 问题**：漏画 trash can ×1（GT 2，模型 1）；漏画 door ×4（GT 5，模型 1）；basket→door 方向错（GT E，模型 SE）；basket-microwave 距离画错（GT 5.1，模型 1.4）；basket→microwave 方向错（GT E，模型 S）；basket-trash can 距离画错（GT 6.3，模型 5.0）；door→microwave 方向错（GT N，模型 NW）；door-trash can 距离画错（GT 3.2，模型 7.6）

### 样本 185 `scene0653_00`（scannet · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: backpack, window, keyboard, door?

- QA：GT B | baseline A（错） | threeview A（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=-115° mirror=否 平移=(1.3,10.3) RMSE=1.56；threeview: yaw=-92° mirror=是(未证实) 平移=(9.5,8.1) RMSE=1.19；threeview_3pass: yaw=-151° mirror=是(证据支持) 平移=(9.6,1.8) RMSE=1.42
- 补偿：baseline: 尺度=0.84 z偏移=+0.00；threeview: 尺度=0.73 z偏移=-1.00；threeview_3pass: 尺度=0.73 z偏移=-0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (3.0,6.0), (5.0,4.0) | (6.0,4.6)✓, 漏1 | (5.2,4.7)✓, 漏1 | (3.2,6.5)✓, 漏1 |
| door | (7.0,7.0) | (5.2,6.8)✓ | (7.8,6.0)✓ | (5.5,5.3)✗2.2 |
| keyboard | (2.0,3.0), (6.0,2.0) | (4.6,3.4)✗2.0, 漏1 | (4.8,3.6)✓, 漏1 | (2.2,5.2)✗2.2, 漏1 |
| window | (1.0,5.0), (1.0,2.0) | (1.2,2.2)✓, 漏1 | (1.2,3.7)✓, 漏1 | (2.1,0.9)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (3.0,1.0), (5.0,1.0) | - | (5.2,1.0)✓, 漏1 | (3.2,1.5)✓, 漏1 |
| door | (7.0,5.0) | - | (7.8,3.5)✓ | (5.5,3.5)✗2.1 |
| keyboard | (2.0,2.0), (6.0,2.0) | - | (4.8,2.0)✓, 漏1 | (2.2,2.5)✓, 漏1 |
| window | (1.0,5.0), (1.0,5.0) | - | (1.2,5.0)✓, 漏1 | (2.1,4.5)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (6.0,1.0), (4.0,1.0) | - | (4.7,1.0)✓, 漏1 | (6.5,1.5)✓, 漏1 |
| door | (7.0,5.0) | - | (6.0,3.5)✓ | (5.3,3.5)✗2.2 |
| keyboard | (3.0,2.0), (2.0,2.0) | - | (3.6,2.0)✓, 漏1 | (5.2,2.5)✗2.2, 漏1 |
| window | (5.0,5.0), (2.0,5.0) | - | (3.7,5.0)✓, 漏1 | (0.9,4.5)✓, 漏1 |

- **baseline 问题**：漏画 window ×1（GT 2，模型 1）；漏画 backpack ×1（GT 2，模型 1）；漏画 keyboard ×1（GT 2，模型 1）；backpack→door 方向错（GT SW，模型 S）；backpack→keyboard 方向错（GT N，模型 NE）；backpack-window 距离画错（GT 2.2，模型 6.4）；door→keyboard 方向错（GT NE，模型 N）；keyboard-window 距离画错（GT 1.4，模型 4.2）
- **threeview 问题**：漏画 window ×1（GT 2，模型 1）；漏画 backpack ×1（GT 2，模型 1）；漏画 keyboard ×1（GT 2，模型 1）；backpack-window 距离画错（GT 2.2，模型 5.7）；backpack→window 方向错（GT NE，模型 E）；door-window 距离画错（GT 6.3，模型 9.7）；door→window 方向错（GT NE，模型 E）；keyboard-window 距离画错（GT 1.4，模型 5.0）
- **threeview_3pass 问题**：漏画 window ×1（GT 2，模型 1）；漏画 backpack ×1（GT 2，模型 1）；漏画 keyboard ×1（GT 2，模型 1）；backpack→door 方向错（GT SW，模型 NW）；backpack→keyboard 方向错（GT N，模型 NE）；backpack-window 距离画错（GT 2.2，模型 7.8）；backpack→window 方向错（GT NE，模型 N）；door→keyboard 方向错（GT NE，模型 E）

### 样本 186 `5942004064`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: blanket, sofa, basket, toilet?

- QA：GT C | baseline C（对） | threeview C（对） | threeview_3pass A（错）
- 对齐：baseline: yaw=180° mirror=否 平移=(8.0,9.0) RMSE=2.35；threeview: yaw=49° mirror=否 平移=(4.6,-2.2) RMSE=1.19；threeview_3pass: yaw=76° mirror=否 平移=(8.5,-1.3) RMSE=1.30
- 补偿：baseline: 尺度=0.17 z偏移=+0.00；threeview: 尺度=1.15 z偏移=-1.50；threeview_3pass: 尺度=0.69 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (2.0,3.0) | (3.5,3.5)✓ | (1.8,3.2)✓ | (2.0,3.0)✓ |
| blanket | (3.0,3.0) | (3.0,4.0)✓ | (4.7,4.2)✗2.1 | (4.5,4.5)✗2.1 |
| sofa | (6.0,6.0) | (3.0,4.0)✗3.6 | (4.5,4.6)✗2.0 | (4.5,4.5)✗2.1 |
| toilet | (1.0,4.0) | (2.5,4.5)✓ | 漏1 | 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (2.0,1.0) | - | (1.8,1.0)✓ | (2.0,1.0)✓ |
| blanket | (3.0,2.0) | - | (4.7,2.3)✓ | (4.5,2.0)✓ |
| sofa | (6.0,2.0) | - | (4.5,2.0)✓ | (4.5,2.0)✓ |
| toilet | (1.0,2.0) | - | 漏1 | 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (3.0,1.0) | - | (3.2,1.0)✓ | (3.0,1.0)✓ |
| blanket | (3.0,2.0) | - | (4.2,2.3)✓ | (4.5,2.0)✓ |
| sofa | (6.0,2.0) | - | (4.6,2.0)✓ | (4.5,2.0)✓ |
| toilet | (4.0,2.0) | - | 漏1 | 漏1 |

- **baseline 问题**：basket-blanket 距离画错（GT 1.0，模型 4.2）；basket→blanket 方向错（GT W，模型 SE）；basket→sofa 方向错（GT SW，模型 SE）；basket-toilet 距离画错（GT 1.4，模型 8.5）；blanket-sofa 距离画错（GT 4.2，模型 0.0）；blanket→sofa 方向错（GT SW，模型 E）；blanket-toilet 距离画错（GT 2.2，模型 4.2）；sofa-toilet 距离画错（GT 5.4，模型 4.2）
- **threeview 问题**：漏画 toilet ×1（GT 1，模型 0）；basket-blanket 距离画错（GT 1.0，模型 2.6）；basket-sofa 距离画错（GT 5.0，模型 2.7）；blanket-sofa 距离画错（GT 4.2，模型 0.4）；blanket→sofa 方向错（GT SW，模型 S）；z 整体偏高（平均 +1.6 格）
- **threeview_3pass 问题**：漏画 toilet ×1（GT 1，模型 0）；basket-blanket 距离画错（GT 1.0，模型 4.2）；basket→blanket 方向错（GT W，模型 SW）；blanket-sofa 距离画错（GT 4.2，模型 0.0）；blanket→sofa 方向错（GT SW，模型 E）；z 整体偏高（平均 +1.0 格）

### 样本 187 `scene0608_00`（scannet · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: door, guitar, lamp, sofa?

- QA：GT B | baseline C（错） | threeview A（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=-21° mirror=否 平移=(-2.7,0.3) RMSE=2.04；threeview: yaw=97° mirror=否 平移=(8.9,-0.2) RMSE=1.02；threeview_3pass: yaw=39° mirror=否 平移=(3.0,-3.2) RMSE=1.39
- 补偿：baseline: 尺度=0.46 z偏移=+0.00；threeview: 尺度=0.88 z偏移=+0.25；threeview_3pass: 尺度=0.79 z偏移=+0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,1.0) | (1.1,2.6)✓ | (0.7,0.7)✓ | (2.2,0.5)✓ |
| guitar | (5.0,6.0) | (2.5,3.6)✗3.5 | (4.0,5.9)✓ | (4.3,5.4)✓ |
| lamp | (5.0,2.0) | (4.8,3.2)✓ | (4.0,2.4)✓ | (2.4,2.8)✗2.7 |
| sofa | (1.0,4.0) | (3.5,3.7)✗2.6 | (3.3,4.1)✗2.3 | (3.1,4.4)✗2.1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,5.0) | - | (0.7,4.8)✓ | (2.2,4.5)✓ |
| guitar | (5.0,2.0) | - | (4.0,3.2)✓ | (4.3,3.5)✓ |
| lamp | (5.0,4.0) | - | (4.0,4.2)✓ | (2.4,4.5)✗2.7 |
| sofa | (1.0,3.0) | - | (3.3,2.8)✗2.4 | (3.1,2.5)✗2.2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,5.0) | - | (0.7,4.8)✓ | (0.5,4.5)✓ |
| guitar | (6.0,2.0) | - | (5.9,3.2)✓ | (5.4,3.5)✓ |
| lamp | (2.0,4.0) | - | (2.4,4.2)✓ | (2.8,4.5)✓ |
| sofa | (4.0,3.0) | - | (4.1,2.8)✓ | (4.4,2.5)✓ |

- **baseline 问题**：door-guitar 距离画错（GT 6.4，模型 3.6）；door-lamp 距离画错（GT 4.1，模型 8.1）；door-sofa 距离画错（GT 3.0，模型 5.7）；door→sofa 方向错（GT S，模型 SW）；guitar-lamp 距离画错（GT 4.0，模型 5.1）；guitar→lamp 方向错（GT N，模型 W）；guitar-sofa 距离画错（GT 4.5，模型 2.2）；guitar→sofa 方向错（GT NE，模型 W）
- **threeview 问题**：door→lamp 方向错（GT W，模型 SW）；door-sofa 距离画错（GT 3.0，模型 4.9）；door→sofa 方向错（GT S，模型 SW）；guitar-sofa 距离画错（GT 4.5，模型 2.2）；guitar→sofa 方向错（GT NE，模型 N）；lamp-sofa 距离画错（GT 4.5，模型 2.1）；lamp→sofa 方向错（GT SE，模型 S）
- **threeview_3pass 问题**：door-lamp 距离画错（GT 4.1，模型 2.8）；door→lamp 方向错（GT W，模型 S）；door-sofa 距离画错（GT 3.0，模型 5.0）；guitar→lamp 方向错（GT N，模型 NE）；guitar-sofa 距离画错（GT 4.5，模型 2.0）；lamp-sofa 距离画错（GT 4.5，模型 2.2）；lamp→sofa 方向错（GT SE，模型 SW）

### 样本 188 `3db0a1c8f3`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: heater, refrigerator, basket, printer?

- QA：GT A | baseline C（错） | threeview C（错） | threeview_3pass D（错）
- 对齐：baseline: yaw=-14° mirror=否 平移=(-2.0,2.0) RMSE=1.68；threeview: yaw=116° mirror=否 平移=(10.3,2.6) RMSE=2.35；threeview_3pass: yaw=-111° mirror=否 平移=(-0.1,13.9) RMSE=2.51
- 补偿：baseline: 尺度=0.35 z偏移=+0.00；threeview: 尺度=0.34 z偏移=-1.25；threeview_3pass: 尺度=0.11 z偏移=-1.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (5.0,7.0), (8.0,3.0), (7.0,2.0), (7.0,2.0) | (3.9,6.2)✓, 漏3 | (5.1,5.3)✓, 漏3 | (3.6,7.0)✓, 漏3 |
| heater | (3.0,7.0) | (2.7,7.6)✓ | (4.3,6.4)✓ | (4.0,6.2)✓ |
| printer | (2.0,7.0) | (3.3,6.7)✓ | (4.1,5.4)✗2.7 | (3.7,6.7)✓ |
| refrigerator | (5.0,5.0) | (5.1,5.5)✓ | (3.5,3.9)✓ | (3.8,6.1)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (5.0,3.0), (8.0,3.0), (7.0,1.0), (7.0,1.0) | - | (5.1,0.2)✗2.1, 漏3 | (3.6,-0.5)✗3.8, 漏3 |
| heater | (3.0,1.0) | - | (4.3,0.8)✓ | (4.0,0.5)✓ |
| printer | (2.0,2.0) | - | (4.1,2.2)✗2.1 | (3.7,2.5)✓ |
| refrigerator | (5.0,2.0) | - | (3.5,3.2)✓ | (3.8,2.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (7.0,3.0), (3.0,3.0), (2.0,1.0), (2.0,1.0) | - | (5.3,0.2)✗3.2, 漏3 | (7.0,-0.5)✗3.5, 漏3 |
| heater | (7.0,1.0) | - | (6.4,0.8)✓ | (6.2,0.5)✓ |
| printer | (7.0,2.0) | - | (5.4,2.2)✓ | (6.7,2.5)✓ |
| refrigerator | (5.0,2.0) | - | (3.9,3.2)✓ | (6.1,2.5)✓ |

- **baseline 问题**：漏画 basket ×3（GT 4，模型 1）；basket-heater 距离画错（GT 2.0，模型 5.0）；basket-refrigerator 距离画错（GT 2.0，模型 4.1）；basket→refrigerator 方向错（GT SE，模型 NW）；heater-printer 距离画错（GT 1.0，模型 2.8）；heater→printer 方向错（GT E，模型 NW）；heater-refrigerator 距离画错（GT 2.8，模型 8.9）；printer-refrigerator 距离画错（GT 3.6，模型 6.3）
- **threeview 问题**：漏画 basket ×3（GT 4，模型 1）；basket-heater 距离画错（GT 2.0，模型 4.0）；basket→printer 方向错（GT SE，模型 E）；basket-refrigerator 距离画错（GT 2.0，模型 6.2）；basket→refrigerator 方向错（GT SE，模型 NE）；heater-printer 距离画错（GT 1.0，模型 3.2）；heater→printer 方向错（GT E，模型 N）；heater-refrigerator 距离画错（GT 2.8，模型 7.8）
- **threeview_3pass 问题**：漏画 basket ×3（GT 4，模型 1）；basket-heater 距离画错（GT 2.0，模型 7.8）；basket→heater 方向错（GT SE，模型 NW）；basket→printer 方向错（GT SE，模型 NW）；basket-refrigerator 距离画错（GT 2.0，模型 8.6）；basket→refrigerator 方向错（GT SE，模型 N）；heater-printer 距离画错（GT 1.0，模型 5.0）；heater→printer 方向错（GT E，模型 SE）

### 样本 189 `scene0608_00`（scannet · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: sofa, clock, lamp, window?

- QA：GT B | baseline C（错） | threeview B（对） | threeview_3pass C（错）
- 对齐：baseline: yaw=150° mirror=是(证据支持) 平移=(3.9,-3.3) RMSE=1.02；threeview: yaw=-169° mirror=否 平移=(6.6,9.4) RMSE=1.50；threeview_3pass: yaw=124° mirror=否 平移=(9.7,3.7) RMSE=0.73
- 补偿：baseline: 尺度=1.29 z偏移=+0.00；threeview: 尺度=0.93 z偏移=-1.00；threeview_3pass: 尺度=1.13 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| clock | (7.0,7.0) | (5.1,7.0)✓ | (6.4,4.4)✗2.7 | (6.3,7.6)✓ |
| lamp | (5.0,2.0) | (4.8,1.2)✓ | (4.9,4.6)✗2.6 | (4.5,2.3)✓, (0.7,7.9)多, 多1 |
| sofa | (1.0,4.0) | (2.1,4.2)✓ | (2.7,3.7)✓ | (0.7,3.8)✓ |
| window | (3.0,7.0) | (4.0,7.6)✓ | (2.0,7.4)✓ | (4.5,6.3)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| clock | (7.0,6.0) | - | (6.4,6.0)✓ | (6.3,8.0)✗2.1 |
| lamp | (5.0,4.0) | - | (4.9,4.0)✓ | (4.5,4.0)✓, (0.7,4.0)多, 多1 |
| sofa | (1.0,3.0) | - | (2.7,2.5)✓ | (0.7,2.0)✓ |
| window | (3.0,5.0) | - | (2.0,5.0)✓ | (4.5,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| clock | (7.0,6.0) | - | (4.4,6.0)✗2.6 | (7.6,8.0)✗2.1 |
| lamp | (2.0,4.0) | - | (4.6,4.0)✗2.6 | (2.3,4.0)✓, (7.9,4.0)多, 多1 |
| sofa | (4.0,3.0) | - | (3.7,2.5)✓ | (3.8,2.0)✓ |
| window | (7.0,5.0) | - | (7.4,5.0)✓ | (6.3,5.0)✓ |

- **baseline 问题**：clock-sofa 距离画错（GT 6.7，模型 3.2）；clock-window 距离画错（GT 4.0，模型 1.0）；clock→window 方向错（GT E，模型 SE）；lamp-sofa 距离画错（GT 4.5，模型 3.2）
- **threeview 问题**：clock-lamp 距离画错（GT 5.4，模型 1.6）；clock→lamp 方向错（GT N，模型 E）；clock-sofa 距离画错（GT 6.7，模型 4.0）；clock→sofa 方向错（GT NE，模型 E）；clock-window 距离画错（GT 4.0，模型 5.7）；clock→window 方向错（GT E，模型 SE）；lamp-sofa 距离画错（GT 4.5，模型 2.5）；lamp→sofa 方向错（GT SE，模型 E）
- **threeview_3pass 问题**：多画 lamp ×1（GT 1，模型 2）；clock→lamp 方向错（GT N，模型 NE）；clock-window 距离画错（GT 4.0，模型 2.0）；clock→window 方向错（GT E，模型 NE）；lamp→sofa 方向错（GT SE，模型 NE）；lamp-window 距离画错（GT 5.4，模型 3.6）；lamp→window 方向错（GT S，模型 SW）

### 样本 190 `d755b3d9d8`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: plant, printer, keyboard, computer mouse?

- QA：GT D | baseline B（错） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=-34° mirror=否 平移=(-2.0,4.5) RMSE=1.30；threeview: yaw=34° mirror=否 平移=(3.3,0.4) RMSE=0.99；threeview_3pass: yaw=-108° mirror=否 平移=(0.6,13.3) RMSE=1.99
- 补偿：baseline: 尺度=0.52 z偏移=+0.00；threeview: 尺度=0.68 z偏移=-1.50；threeview_3pass: 尺度=0.30 z偏移=-2.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (5.0,2.0), (4.0,7.0), (6.0,7.0) | (5.9,6.6)✓, 漏2 | (5.5,7.6)✓, 漏2 | (4.3,6.1)✓, 漏2 |
| keyboard | (4.0,7.0), (5.0,7.0) | (5.0,7.1)✓, 漏1 | (4.7,7.1)✓, 漏1 | (4.5,6.7)✓, 漏1 |
| plant | (7.0,4.0), (7.0,5.0), (4.0,7.0) | (2.5,7.0)✓, 漏2 | (3.6,5.4)✓, 漏2 | (3.7,8.2)✓, 漏2 |
| printer | (1.0,6.0), (1.0,7.0) | (2.6,6.3)✓, 漏1 | (2.2,6.9)✓, 漏1 | (3.4,6.1)✗2.4, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (5.0,2.0), (4.0,2.0), (6.0,2.0) | - | (5.5,2.3)✓, 漏2 | (4.3,2.0)✓, 漏2 |
| keyboard | (4.0,2.0), (5.0,2.0) | - | (4.7,2.3)✓, 漏1 | (4.5,2.0)✓, 漏1 |
| plant | (7.0,4.0), (7.0,3.0), (4.0,2.0) | - | (3.6,3.7)✓, 漏2 | (3.7,1.0)✓, 漏2 |
| printer | (1.0,3.0), (1.0,3.0) | - | (2.2,2.7)✓, 漏1 | (3.4,3.0)✗2.4, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (2.0,2.0), (7.0,2.0), (7.0,2.0) | - | (7.6,2.3)✓, 漏2 | (6.1,2.0)✓, 漏2 |
| keyboard | (7.0,2.0), (7.0,2.0) | - | (7.1,2.3)✓, 漏1 | (6.7,2.0)✓, 漏1 |
| plant | (4.0,4.0), (5.0,3.0), (7.0,2.0) | - | (5.4,3.7)✓, 漏2 | (8.2,1.0)✓, 漏2 |
| printer | (6.0,3.0), (7.0,3.0) | - | (6.9,2.7)✓, 漏1 | (6.1,3.0)✓, 漏1 |

- **baseline 问题**：漏画 keyboard ×1（GT 2，模型 1）；漏画 computer mouse ×2（GT 3，模型 1）；漏画 printer ×1（GT 2，模型 1）；漏画 plant ×2（GT 3，模型 1）；computer mouse-keyboard 距离画错（GT 0.0，模型 2.0）；computer mouse→keyboard 方向错（GT S，模型 SE）；computer mouse-plant 距离画错（GT 0.0，模型 6.7）；computer mouse→plant 方向错（GT W，模型 E）
- **threeview 问题**：漏画 keyboard ×1（GT 2，模型 1）；漏画 computer mouse ×2（GT 3，模型 1）；漏画 printer ×1（GT 2，模型 1）；漏画 plant ×2（GT 3，模型 1）；computer mouse-keyboard 距离画错（GT 0.0，模型 1.4）；computer mouse→keyboard 方向错（GT S，模型 NE）；computer mouse-plant 距离画错（GT 0.0，模型 4.3）；computer mouse→plant 方向错（GT W，模型 NE）
- **threeview_3pass 问题**：漏画 keyboard ×1（GT 2，模型 1）；漏画 computer mouse ×2（GT 3，模型 1）；漏画 printer ×1（GT 2，模型 1）；漏画 plant ×2（GT 3，模型 1）；computer mouse-keyboard 距离画错（GT 0.0，模型 2.0）；computer mouse-plant 距离画错（GT 0.0，模型 7.2）；computer mouse→plant 方向错（GT W，模型 S）；keyboard-plant 距离画错（GT 0.0，模型 5.7）

### 样本 191 `scene0050_01`（scannet · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: table, door, printer, lamp?

- QA：GT C | baseline C（对） | threeview C（对） | threeview_3pass C（对）
- 对齐：baseline: yaw=22° mirror=否 平移=(2.9,-0.2) RMSE=0.72；threeview: yaw=25° mirror=否 平移=(3.7,-0.1) RMSE=0.98；threeview_3pass: yaw=12° mirror=否 平移=(2.4,-0.3) RMSE=0.89
- 补偿：baseline: 尺度=0.66 z偏移=+0.00；threeview: 尺度=0.55 z偏移=+1.35；threeview_3pass: 尺度=0.62 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (2.0,7.0), (6.0,1.0), (7.0,5.0), (7.0,3.0) | (2.0,7.2)✓, 漏3 | (2.5,7.4)✓, 漏3 | (2.6,7.3)✓, 漏3 |
| lamp | (4.0,7.0) | (4.6,6.1)✓ | (4.2,5.7)✓ | (4.3,5.7)✓ |
| printer | (6.0,6.0), (6.0,6.0) | (5.2,6.3)✓, 漏1 | (5.0,6.4)✓, 漏1 | (4.7,6.4)✓, 漏1 |
| table | (5.0,6.0) | (5.2,6.3)✓ | (5.3,6.5)✓ | (5.4,6.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (2.0,4.0), (6.0,4.0), (7.0,4.0), (7.0,4.0) | - | (2.5,3.4)✓, 漏3 | (2.6,4.0)✓, 漏3 |
| lamp | (4.0,4.0) | - | (4.2,3.4)✓ | (4.3,5.0)✓ |
| printer | (6.0,4.0), (6.0,4.0) | - | (5.0,4.7)✓, 漏1 | (4.7,4.0)✓, 漏1 |
| table | (5.0,2.0) | - | (5.3,3.4)✓ | (5.4,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (7.0,4.0), (1.0,4.0), (5.0,4.0), (3.0,4.0) | - | (7.4,3.4)✓, 漏3 | (7.3,4.0)✓, 漏3 |
| lamp | (7.0,4.0) | - | (5.7,3.4)✓ | (5.7,5.0)✓ |
| printer | (6.0,4.0), (6.0,4.0) | - | (6.4,4.7)✓, 漏1 | (6.4,4.0)✓, 漏1 |
| table | (6.0,2.0) | - | (6.5,3.4)✓ | (6.6,2.0)✓ |

- **baseline 问题**：漏画 printer ×1（GT 2，模型 1）；漏画 door ×3（GT 4，模型 1）；door-lamp 距离画错（GT 2.0，模型 4.2）；door→lamp 方向错（GT SE，模型 NW）；door-printer 距离画错（GT 1.4，模型 5.0）；door→printer 方向错（GT S，模型 W）；door-table 距离画错（GT 2.2，模型 5.0）；door→table 方向错（GT S，模型 W）
- **threeview 问题**：漏画 printer ×1（GT 2，模型 1）；漏画 door ×3（GT 4，模型 1）；door-lamp 距离画错（GT 2.0，模型 4.3）；door→lamp 方向错（GT SE，模型 NW）；door-printer 距离画错（GT 1.4，模型 4.9）；door→printer 方向错（GT S，模型 W）；door-table 距离画错（GT 2.2，模型 5.3）；door→table 方向错（GT S，模型 W）
- **threeview_3pass 问题**：漏画 printer ×1（GT 2，模型 1）；漏画 door ×3（GT 4，模型 1）；door-lamp 距离画错（GT 2.0，模型 3.6）；door→lamp 方向错（GT SE，模型 NW）；door-printer 距离画错（GT 1.4，模型 3.6）；door→printer 方向错（GT S，模型 W）；door-table 距离画错（GT 2.2，模型 4.5）；door→table 方向错（GT S，模型 W）

### 样本 192 `3db0a1c8f3`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: heater, tv, ceiling light, printer?

- QA：GT B | baseline D（错） | threeview D（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=-121° mirror=是(未证实) 平移=(9.4,6.7) RMSE=1.36；threeview: yaw=-107° mirror=否 平移=(-2.0,10.7) RMSE=1.36；threeview_3pass: yaw=-164° mirror=是(证据支持) 平移=(9.1,2.1) RMSE=1.72
- 补偿：baseline: 尺度=0.50 z偏移=+0.00；threeview: 尺度=0.50 z偏移=-1.75；threeview_3pass: 尺度=0.40 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (7.0,4.0), (1.0,3.0), (4.0,4.0) | (4.5,4.1)✓, 漏2 | (2.2,4.9)✗2.0, 漏2 | (3.4,3.8)✓, 漏2 |
| heater | (3.0,7.0) | (2.2,7.2)✓ | (3.9,6.2)✓ | (3.8,6.8)✓ |
| printer | (2.0,7.0) | (2.8,6.2)✓ | (2.1,5.6)✓ | (1.7,5.4)✓ |
| tv | (3.0,3.0) | (2.4,3.6)✓ | (3.8,4.3)✓ | (3.1,5.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (7.0,7.0), (1.0,7.0), (4.0,8.0) | - | (2.2,7.2)✓, 漏2 | (3.4,8.0)✓, 漏2 |
| heater | (3.0,1.0) | - | (3.9,0.8)✓ | (3.8,1.0)✓ |
| printer | (2.0,2.0) | - | (2.1,2.2)✓ | (1.7,2.0)✓ |
| tv | (3.0,2.0) | - | (3.8,3.8)✓ | (3.1,4.0)✗2.0 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (4.0,7.0), (3.0,7.0), (4.0,8.0) | - | (4.9,7.2)✓, 漏2 | (3.8,8.0)✓, 漏2 |
| heater | (7.0,1.0) | - | (6.2,0.8)✓ | (6.8,1.0)✓ |
| printer | (7.0,2.0) | - | (5.6,2.2)✓ | (5.4,2.0)✓ |
| tv | (3.0,2.0) | - | (4.3,3.8)✗2.2 | (5.0,4.0)✗2.8 |

- **baseline 问题**：漏画 ceiling light ×2（GT 3，模型 1）；ceiling light-heater 距离画错（GT 3.2，模型 7.6）；ceiling light→heater 方向错（GT S，模型 SE）；ceiling light-printer 距离画错（GT 3.6，模型 5.4）；ceiling light-tv 距离画错（GT 1.4，模型 4.2）；ceiling light→tv 方向错（GT NE，模型 E）；heater-printer 距离画错（GT 1.0，模型 2.2）；heater→printer 方向错（GT E，模型 NW）
- **threeview 问题**：漏画 ceiling light ×2（GT 3，模型 1）；ceiling light-heater 距离画错（GT 3.2，模型 4.3）；ceiling light→heater 方向错（GT S，模型 SW）；ceiling light-printer 距离画错（GT 3.6，模型 1.6）；ceiling light→printer 方向错（GT SE，模型 S）；ceiling light-tv 距离画错（GT 1.4，模型 3.5）；ceiling light→tv 方向错（GT NE，模型 W）；heater-printer 距离画错（GT 1.0，模型 3.6）
- **threeview_3pass 问题**：漏画 ceiling light ×2（GT 3，模型 1）；ceiling light-heater 距离画错（GT 3.2，模型 7.6）；ceiling light-printer 距离画错（GT 3.6，模型 5.8）；ceiling light-tv 距离画错（GT 1.4，模型 3.0）；ceiling light→tv 方向错（GT NE，模型 S）；heater-printer 距离画错（GT 1.0，模型 6.3）；heater→printer 方向错（GT E，模型 NE）；printer→tv 方向错（GT N，模型 W）

### 样本 193 `scene0653_00`（scannet · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: chair, backpack, clock, window?

- QA：GT A | baseline A（对） | threeview A（对） | threeview_3pass A（对）
- 对齐：baseline: yaw=-20° mirror=否 平移=(-3.8,2.1) RMSE=1.91；threeview: yaw=2° mirror=否 平移=(-0.7,-0.5) RMSE=2.35；threeview_3pass: yaw=98° mirror=是(未证实) 平移=(-0.9,-0.1) RMSE=1.40
- 补偿：baseline: 尺度=0.42 z偏移=+0.00；threeview: 尺度=0.23 z偏移=-1.50；threeview_3pass: 尺度=0.65 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (3.0,6.0), (5.0,4.0) | (2.2,5.5)✓, 漏1 | (3.3,4.5)✓, 漏1 | (4.5,4.7)✓, 漏1 |
| chair | (2.0,2.0), (6.0,2.0), (2.0,7.0), (2.0,5.0), (4.0,1.0), (5.0,2.0), (6.0,3.0), (6.0,5.0) | (2.3,5.9)✓, (2.3,5.9)✗2.2, (3.5,5.4)多, 漏6 | (3.4,4.6)✓, 漏7 | (3.8,5.2)✓, 漏7 |
| clock | (1.0,4.0) | (2.0,3.8)✓ | (2.8,3.5)✓ | (0.6,4.8)✓ |
| window | (1.0,5.0), (1.0,2.0) | (0.6,4.7)✓, (0.6,4.7)✗2.9, (3.3,3.7)多 | (3.4,5.5)✗2.5, 漏1 | (2.2,2.4)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (3.0,1.0), (5.0,1.0) | - | (3.3,1.0)✓, 漏1 | (4.5,1.0)✓, 漏1 |
| chair | (2.0,2.0), (6.0,2.0), (2.0,2.0), (2.0,2.0), (4.0,2.0), (5.0,2.0), (6.0,2.0), (6.0,2.0) | - | (3.4,2.0)✓, 漏7 | (3.8,2.0)✓, 漏7 |
| clock | (1.0,6.0) | - | (2.8,6.0)✓ | (0.6,6.0)✓ |
| window | (1.0,5.0), (1.0,5.0) | - | (3.4,5.0)✗2.4, 漏1 | (2.2,4.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (6.0,1.0), (4.0,1.0) | - | (4.5,1.0)✓, 漏1 | (4.7,1.0)✓, 漏1 |
| chair | (2.0,2.0), (2.0,2.0), (7.0,2.0), (5.0,2.0), (1.0,2.0), (2.0,2.0), (3.0,2.0), (5.0,2.0) | - | (4.6,2.0)✓, 漏7 | (5.2,2.0)✓, 漏7 |
| clock | (4.0,6.0) | - | (3.5,6.0)✓ | (4.8,6.0)✓ |
| window | (5.0,5.0), (2.0,5.0) | - | (5.5,5.0)✓, 漏1 | (2.4,4.0)✓, 漏1 |

- **baseline 问题**：漏画 backpack ×1（GT 2，模型 1）；漏画 chair ×6（GT 8，模型 2）；backpack→chair 方向错（GT N，模型 W）；backpack-clock 距离画错（GT 2.8，模型 4.1）；backpack→clock 方向错（GT E，模型 N）；backpack-window 距离画错（GT 2.2，模型 4.2）；backpack→window 方向错（GT NE，模型 N）；chair-clock 距离画错（GT 1.4，模型 5.1）
- **threeview 问题**：漏画 window ×1（GT 2，模型 1）；漏画 backpack ×1（GT 2，模型 1）；漏画 chair ×7（GT 8，模型 1）；backpack→chair 方向错（GT N，模型 SW）；backpack-clock 距离画错（GT 2.8，模型 5.0）；backpack→clock 方向错（GT E，模型 NE）；backpack-window 距离画错（GT 2.2，模型 4.2）；backpack→window 方向错（GT NE，模型 S）
- **threeview_3pass 问题**：漏画 window ×1（GT 2，模型 1）；漏画 backpack ×1（GT 2，模型 1）；漏画 chair ×7（GT 8，模型 1）；backpack→chair 方向错（GT N，模型 SE）；backpack-clock 距离画错（GT 2.8，模型 6.1）；backpack-window 距离画错（GT 2.2，模型 5.0）；chair-clock 距离画错（GT 1.4，模型 5.0）；chair-window 距离画错（GT 1.0，模型 5.0）

### 样本 194 `25f3b7a318`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: laptop, shoe rack, basket, bed?

- QA：GT B | baseline C（错） | threeview B（对） | threeview_3pass B（对）
- 对齐：baseline: yaw=108° mirror=否 平移=(10.9,2.4) RMSE=2.05；threeview: yaw=-102° mirror=是(证据支持) 平移=(10.5,7.7) RMSE=1.50；threeview_3pass: yaw=-99° mirror=是(未证实) 平移=(10.4,8.8) RMSE=1.77
- 补偿：baseline: 尺度=0.56 z偏移=+0.00；threeview: 尺度=0.74 z偏移=-0.25；threeview_3pass: 尺度=0.72 z偏移=+0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (1.0,4.0) | (3.1,3.1)✗2.3 | (1.7,2.3)✓ | (2.7,2.7)✗2.1 |
| bed | (5.0,2.0) | (4.2,5.2)✗3.3 | (4.4,4.4)✗2.5 | (4.5,4.6)✗2.7 |
| laptop | (7.0,7.0) | (5.1,4.3)✗3.3 | (6.1,5.2)✗2.0 | (5.2,4.5)✗3.1 |
| shoe rack | (2.0,6.0) | (2.6,6.4)✓ | (2.7,7.0)✓ | (2.6,7.1)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (1.0,5.0) | - | (1.7,2.2)✗2.8 | (2.7,1.5)✗3.9 |
| bed | (5.0,1.0) | - | (4.4,3.2)✗2.3 | (4.5,2.5)✓ |
| laptop | (7.0,4.0) | - | (6.1,4.2)✓ | (5.2,3.5)✓ |
| shoe rack | (2.0,2.0) | - | (2.7,1.8)✓ | (2.6,2.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (4.0,5.0) | - | (2.3,2.2)✗3.2 | (2.7,1.5)✗3.7 |
| bed | (2.0,1.0) | - | (4.4,3.2)✗3.3 | (4.6,2.5)✗3.0 |
| laptop | (7.0,4.0) | - | (5.2,4.2)✓ | (4.5,3.5)✗2.5 |
| shoe rack | (6.0,2.0) | - | (7.0,1.8)✓ | (7.1,2.5)✓ |

- **baseline 问题**：basket→bed 方向错（GT NW，模型 SW）；basket-laptop 距离画错（GT 6.7，模型 4.1）；basket-shoe rack 距离画错（GT 2.2，模型 6.1）；basket→shoe rack 方向错（GT SW，模型 S）；bed-laptop 距离画错（GT 5.4，模型 2.2）；bed→laptop 方向错（GT S，模型 NW）；bed-shoe rack 距离画错（GT 5.0，模型 3.6）；laptop→shoe rack 方向错（GT E，模型 SE）
- **threeview 问题**：basket→bed 方向错（GT NW，模型 SW）；basket-shoe rack 距离画错（GT 2.2，模型 6.5）；basket→shoe rack 方向错（GT SW，模型 S）；bed-laptop 距离画错（GT 5.4，模型 2.5）；bed→laptop 方向错（GT S，模型 SW）；laptop→shoe rack 方向错（GT E，模型 SE）
- **threeview_3pass 问题**：basket→bed 方向错（GT NW，模型 SW）；basket-laptop 距离画错（GT 6.7，模型 4.2）；basket-shoe rack 距离画错（GT 2.2，模型 6.1）；basket→shoe rack 方向错（GT SW，模型 S）；bed-laptop 距离画错（GT 5.4，模型 1.0）；bed→laptop 方向错（GT S，模型 W）；laptop→shoe rack 方向错（GT E，模型 SE）；z 整体偏低（平均 -1.0 格）

### 样本 195 `scene0695_00`（scannet · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: monitor, bookshelf, lamp, trash bin?

- QA：GT D | baseline A（错） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=-122° mirror=否 平移=(2.7,9.4) RMSE=2.23；threeview: yaw=-111° mirror=否 平移=(2.0,10.5) RMSE=1.82；threeview_3pass: yaw=-88° mirror=否 平移=(0.1,8.1) RMSE=2.16
- 补偿：baseline: 尺度=0.52 z偏移=+0.00；threeview: 尺度=0.76 z偏移=-0.25；threeview_3pass: 尺度=0.54 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bookshelf | (5.0,7.0) | (5.9,5.0)✗2.2 | (4.6,6.2)✓ | (5.2,5.8)✓ |
| lamp | (5.0,1.0) | (4.4,4.7)✗3.7 | (5.2,4.7)✗3.7 | (4.1,4.6)✗3.7 |
| monitor | (4.0,7.0) | (4.3,3.5)✗3.5 | (4.9,4.0)✗3.1 | (4.7,3.6)✗3.5 |
| trash bin | (7.0,1.0) | (6.4,2.8)✓ | (6.3,1.1)✓ | (6.9,2.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bookshelf | (5.0,2.0) | - | (4.6,4.2)✗2.3 | (5.2,5.0)✗3.0 |
| lamp | (5.0,4.0) | - | (5.2,4.2)✓ | (4.1,4.0)✓ |
| monitor | (4.0,4.0) | - | (4.9,3.8)✓ | (4.7,4.0)✓ |
| trash bin | (7.0,2.0) | - | (6.3,1.2)✓ | (6.9,1.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bookshelf | (7.0,2.0) | - | (6.2,4.2)✗2.4 | (5.8,5.0)✗3.2 |
| lamp | (1.0,4.0) | - | (4.7,4.2)✗3.7 | (4.6,4.0)✗3.6 |
| monitor | (7.0,4.0) | - | (4.0,3.8)✗3.0 | (3.6,4.0)✗3.4 |
| trash bin | (1.0,2.0) | - | (1.1,1.2)✓ | (2.0,1.0)✓ |

- **baseline 问题**：bookshelf-lamp 距离画错（GT 6.0，模型 2.8）；bookshelf→lamp 方向错（GT N，模型 E）；bookshelf-monitor 距离画错（GT 1.0，模型 4.1）；bookshelf→monitor 方向错（GT E，模型 NE）；bookshelf-trash bin 距离画错（GT 6.3，模型 4.2）；lamp-monitor 距离画错（GT 6.1，模型 2.2）；lamp→monitor 方向错（GT S，模型 N）；lamp-trash bin 距离画错（GT 2.0，模型 5.1）
- **threeview 问题**：bookshelf-lamp 距离画错（GT 6.0，模型 2.1）；bookshelf→lamp 方向错（GT N，模型 NW）；bookshelf-monitor 距离画错（GT 1.0，模型 2.9）；bookshelf→monitor 方向错（GT E，模型 N）；lamp-monitor 距离画错（GT 6.1，模型 1.0）；lamp→monitor 方向错（GT S，模型 N）；lamp-trash bin 距离画错（GT 2.0，模型 5.0）；lamp→trash bin 方向错（GT W，模型 N）
- **threeview_3pass 问题**：bookshelf-lamp 距离画错（GT 6.0，模型 2.8）；bookshelf→lamp 方向错（GT N，模型 NE）；bookshelf-monitor 距离画错（GT 1.0，模型 4.1）；bookshelf→monitor 方向错（GT E，模型 N）；bookshelf-trash bin 距离画错（GT 6.3，模型 7.6）；bookshelf→trash bin 方向错（GT N，模型 NW）；lamp-monitor 距离画错（GT 6.1，模型 2.2）；lamp→monitor 方向错（GT S，模型 NW）

### 样本 196 `3db0a1c8f3`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: chair, heater, printer, basket?

- QA：GT C | baseline A（错） | threeview A（错） | threeview_3pass D（错）
- 对齐：baseline: yaw=-120° mirror=否 平移=(1.5,13.5) RMSE=1.84；threeview: yaw=-130° mirror=否 平移=(2.9,12.7) RMSE=1.69；threeview_3pass: yaw=-133° mirror=否 平移=(1.8,14.6) RMSE=1.74
- 补偿：baseline: 尺度=0.23 z偏移=+0.00；threeview: 尺度=0.25 z偏移=-1.75；threeview_3pass: 尺度=0.17 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (5.0,7.0), (8.0,3.0), (7.0,2.0), (7.0,2.0) | (4.0,6.8)✓, 漏3 | (4.1,6.4)✓, 漏3 | (3.6,7.2)✓, 漏3 |
| chair | (3.0,7.0), (4.0,4.0), (3.0,2.0), (3.0,7.0) | (3.5,6.8)✓, 漏3 | (3.6,6.2)✓, 漏3 | (3.2,7.0)✓, 漏3 |
| heater | (3.0,7.0) | (3.0,7.9)✓ | (2.8,5.7)✓ | (3.1,6.4)✓ |
| printer | (2.0,7.0) | (2.5,6.6)✓ | (3.5,6.7)✓ | (3.1,7.5)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (5.0,3.0), (8.0,3.0), (7.0,1.0), (7.0,1.0) | - | (4.1,0.2)✗2.9, 漏3 | (3.6,1.0)✗2.4, 漏3 |
| chair | (3.0,2.0), (4.0,2.0), (3.0,2.0), (3.0,2.0) | - | (3.6,2.2)✓, 漏3 | (3.2,2.0)✓, 漏3 |
| heater | (3.0,1.0) | - | (2.8,0.8)✓ | (3.1,1.0)✓ |
| printer | (2.0,2.0) | - | (3.5,3.8)✗2.3 | (3.1,4.0)✗2.3 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| basket | (7.0,3.0), (3.0,3.0), (2.0,1.0), (2.0,1.0) | - | (6.4,0.2)✗2.8, 漏3 | (7.2,1.0)✗2.0, 漏3 |
| chair | (7.0,2.0), (4.0,2.0), (2.0,2.0), (7.0,2.0) | - | (6.2,2.2)✓, 漏3 | (7.0,2.0)✓, 漏3 |
| heater | (7.0,1.0) | - | (5.7,0.8)✓ | (6.4,1.0)✓ |
| printer | (7.0,2.0) | - | (6.7,3.8)✓ | (7.5,4.0)✗2.1 |

- **baseline 问题**：漏画 basket ×3（GT 4，模型 1）；漏画 chair ×3（GT 4，模型 1）；basket→chair 方向错（GT SE，模型 E）；basket-heater 距离画错（GT 2.0，模型 6.3）；basket-printer 距离画错（GT 3.0，模型 6.4）；basket→printer 方向错（GT SE，模型 E）；chair-heater 距离画错（GT 0.0，模型 5.0）；chair→heater 方向错（GT S，模型 SE）
- **threeview 问题**：漏画 basket ×3（GT 4，模型 1）；漏画 chair ×3（GT 4，模型 1）；basket→chair 方向错（GT SE，模型 NE）；basket-heater 距离画错（GT 2.0，模型 5.9）；basket→heater 方向错（GT SE，模型 NE）；chair-heater 距离画错（GT 0.0，模型 3.6）；chair→heater 方向错（GT S，模型 NE）；chair-printer 距离画错（GT 1.0，模型 2.1）
- **threeview_3pass 问题**：漏画 basket ×3（GT 4，模型 1）；漏画 chair ×3（GT 4，模型 1）；basket-chair 距离画错（GT 2.0，模型 3.2）；basket→chair 方向错（GT SE，模型 NE）；basket-heater 距离画错（GT 2.0，模型 6.1）；basket→heater 方向错（GT SE，模型 NE）；chair-heater 距离画错（GT 0.0，模型 3.6）；chair→heater 方向错（GT S，模型 N）

### 样本 197 `scene0591_01`（scannet · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: telephone, computer mouse, keyboard, door?

- QA：GT B | baseline C（错） | threeview C（错） | threeview_3pass C（错）
- 对齐：baseline: yaw=88° mirror=是(未证实) 平移=(-2.4,0.3) RMSE=1.04；threeview: yaw=86° mirror=否 平移=(9.2,-0.4) RMSE=0.76；threeview_3pass: yaw=2° mirror=否 平移=(0.4,-2.6) RMSE=1.31
- 补偿：baseline: 尺度=0.66 z偏移=+0.00；threeview: 尺度=0.77 z偏移=-0.90；threeview_3pass: 尺度=0.61 z偏移=+0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (5.0,5.0) | (5.3,5.9)✓ | (5.3,5.8)✓ | (6.1,5.0)✓ |
| door | (1.0,2.0) | (1.9,2.1)✓ | (1.6,2.0)✓ | (2.5,2.4)✓ |
| keyboard | (5.0,5.0), (5.0,3.0) | (5.3,4.6)✓, 漏1 | (5.2,4.8)✓, 漏1 | (4.8,4.9)✓, 漏1 |
| telephone | (6.0,4.0) | (4.6,3.3)✓ | (4.8,3.3)✓ | (3.6,3.7)✗2.4 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (5.0,3.0) | - | (5.3,2.9)✓ | (6.1,3.0)✓ |
| door | (1.0,4.0) | - | (1.6,4.1)✓ | (2.5,4.0)✓ |
| keyboard | (5.0,3.0), (5.0,3.0) | - | (5.2,2.9)✓, 漏1 | (4.8,3.0)✓, 漏1 |
| telephone | (6.0,3.0) | - | (4.8,3.3)✓ | (3.6,4.0)✗2.6 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (5.0,3.0) | - | (5.8,2.9)✓ | (5.0,3.0)✓ |
| door | (2.0,4.0) | - | (2.0,4.1)✓ | (2.4,4.0)✓ |
| keyboard | (5.0,3.0), (3.0,3.0) | - | (4.8,2.9)✓, 漏1 | (4.9,3.0)✓, 漏1 |
| telephone | (4.0,3.0) | - | (3.3,3.3)✓ | (3.7,4.0)✓ |

- **baseline 问题**：漏画 keyboard ×1（GT 2，模型 1）；computer mouse-door 距离画错（GT 5.0，模型 7.8）；computer mouse-keyboard 距离画错（GT 0.0，模型 2.0）；computer mouse-telephone 距离画错（GT 1.4，模型 4.1）；computer mouse→telephone 方向错（GT NW，模型 N）；door-keyboard 距离画错（GT 4.1，模型 6.4）；door→telephone 方向错（GT W，模型 SW）；keyboard→telephone 方向错（GT W，模型 NE）
- **threeview 问题**：漏画 keyboard ×1（GT 2，模型 1）；computer mouse-door 距离画错（GT 5.0，模型 6.9）；computer mouse-keyboard 距离画错（GT 0.0，模型 1.3）；computer mouse-telephone 距离画错（GT 1.4，模型 3.3）；computer mouse→telephone 方向错（GT NW，模型 N）；door-keyboard 距离画错（GT 4.1，模型 5.9）；keyboard→telephone 方向错（GT W，模型 N）；z 整体偏高（平均 +0.9 格）
- **threeview_3pass 问题**：漏画 keyboard ×1（GT 2，模型 1）；computer mouse-door 距离画错（GT 5.0，模型 7.2）；computer mouse-keyboard 距离画错（GT 0.0，模型 2.0）；computer mouse→keyboard 方向错（GT N，模型 E）；computer mouse-telephone 距离画错（GT 1.4，模型 4.5）；computer mouse→telephone 方向错（GT NW，模型 NE）；door-keyboard 距离画错（GT 4.1，模型 5.7）；door-telephone 距离画错（GT 5.4，模型 2.8）

### 样本 198 `578511c8a9`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: computer mouse, keyboard, kettle, whiteboard?

- QA：GT B | baseline D（错） | threeview B（对） | threeview_3pass A（错）
- 对齐：baseline: yaw=-60° mirror=否 平移=(-1.3,6.4) RMSE=1.71；threeview: yaw=-56° mirror=否 平移=(-1.1,6.7) RMSE=1.24；threeview_3pass: yaw=-59° mirror=否 平移=(-1.2,6.1) RMSE=1.81
- 补偿：baseline: 尺度=0.34 z偏移=+0.00；threeview: 尺度=0.54 z偏移=-2.00；threeview_3pass: 尺度=0.36 z偏移=-2.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (4.0,3.0), (3.0,3.0), (3.0,4.0), (3.0,5.0), (3.0,5.0), (4.0,5.0), (7.0,4.0), (1.0,4.0) | (6.6,4.5)✓, 漏7 | (6.2,4.9)✓, 漏7 | (6.7,4.4)✓, 漏7 |
| kettle | (7.0,7.0) | (5.3,5.3)✗2.4 | (5.4,6.1)✓ | (5.5,5.7)✓ |
| keyboard | (2.0,4.0), (2.0,2.0), (4.0,3.0), (3.0,4.0), (3.0,5.0), (3.0,5.0), (3.0,5.0), (4.0,5.0), (7.0,6.0), (7.0,4.0) | (6.3,5.1)✓, 漏9 | (5.8,5.4)✓, 漏9 | (6.3,5.0)✓, 漏9 |
| whiteboard | (5.0,3.0), (2.0,1.0), (2.0,1.0), (7.0,7.0) | (4.8,4.2)✓, 漏3 | (7.6,6.6)✓, 漏3 | (4.5,3.9)✓, 漏3 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (4.0,3.0), (3.0,3.0), (3.0,3.0), (3.0,3.0), (3.0,3.0), (4.0,3.0), (7.0,3.0), (1.0,3.0) | - | (6.2,2.0)✓, 漏7 | (6.7,2.0)✓, 漏7 |
| kettle | (7.0,1.0) | - | (5.4,2.5)✗2.2 | (5.5,3.0)✗2.5 |
| keyboard | (2.0,3.0), (2.0,3.0), (4.0,3.0), (3.0,3.0), (3.0,3.0), (3.0,3.0), (3.0,3.0), (4.0,3.0), (7.0,3.0), (7.0,3.0) | - | (5.8,2.0)✓, 漏9 | (6.3,2.0)✓, 漏9 |
| whiteboard | (5.0,3.0), (2.0,2.0), (2.0,3.0), (7.0,2.0) | - | (7.6,4.0)✗2.1, 漏3 | (4.5,4.0)✓, 漏3 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (3.0,3.0), (3.0,3.0), (4.0,3.0), (5.0,3.0), (5.0,3.0), (5.0,3.0), (4.0,3.0), (4.0,3.0) | - | (4.9,2.0)✓, 漏7 | (4.4,2.0)✓, 漏7 |
| kettle | (7.0,1.0) | - | (6.1,2.5)✓ | (5.7,3.0)✗2.4 |
| keyboard | (4.0,3.0), (2.0,3.0), (3.0,3.0), (4.0,3.0), (5.0,3.0), (5.0,3.0), (5.0,3.0), (5.0,3.0), (6.0,3.0), (4.0,3.0) | - | (5.4,2.0)✓, 漏9 | (5.0,2.0)✓, 漏9 |
| whiteboard | (3.0,3.0), (1.0,2.0), (1.0,3.0), (7.0,2.0) | - | (6.6,4.0)✗2.0, 漏3 | (3.9,4.0)✓, 漏3 |

- **baseline 问题**：漏画 keyboard ×9（GT 10，模型 1）；漏画 computer mouse ×7（GT 8，模型 1）；漏画 whiteboard ×3（GT 4，模型 1）；computer mouse-kettle 距离画错（GT 3.0，模型 4.5）；computer mouse→kettle 方向错（GT SW，模型 SE）；computer mouse-keyboard 距离画错（GT 0.0，模型 2.0）；computer mouse-whiteboard 距离画错（GT 1.0，模型 5.4）；computer mouse→whiteboard 方向错（GT NW，模型 E）
- **threeview 问题**：漏画 keyboard ×9（GT 10，模型 1）；漏画 computer mouse ×7（GT 8，模型 1）；漏画 whiteboard ×3（GT 4，模型 1）；computer mouse→kettle 方向错（GT SW，模型 SE）；computer mouse-keyboard 距离画错（GT 0.0，模型 1.2）；computer mouse-whiteboard 距离画错（GT 1.0，模型 4.2）；computer mouse→whiteboard 方向错（GT NW，模型 SW）；kettle→keyboard 方向错（GT NE，模型 NW）
- **threeview_3pass 问题**：漏画 keyboard ×9（GT 10，模型 1）；漏画 computer mouse ×7（GT 8，模型 1）；漏画 whiteboard ×3（GT 4，模型 1）；computer mouse-kettle 距离画错（GT 3.0，模型 5.1）；computer mouse→kettle 方向错（GT SW，模型 SE）；computer mouse-keyboard 距离画错（GT 0.0，模型 2.0）；computer mouse-whiteboard 距离画错（GT 1.0，模型 6.3）；computer mouse→whiteboard 方向错（GT NW，模型 E）

### 样本 199 `scene0580_01`（scannet · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: trash bin, chair, lamp, table?

- QA：GT A | baseline C（错） | threeview A（对） | threeview_3pass A（对）
- 对齐：baseline: yaw=-2° mirror=否 平移=(1.6,-1.1) RMSE=0.83；threeview: yaw=-88° mirror=是(证据支持) 平移=(10.0,9.1) RMSE=0.90；threeview_3pass: yaw=44° mirror=否 平移=(4.9,-3.2) RMSE=1.04
- 补偿：baseline: 尺度=0.86 z偏移=+0.00；threeview: 尺度=1.55 z偏移=-1.50；threeview_3pass: 尺度=0.75 z偏移=-0.50
- 跨视图未匹配：threeview_3pass: side 未匹配×1

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (7.0,5.0) | (7.4,3.7)✓, (5.7,3.8)多, 多1 | (7.6,3.9)✓ | (5.7,4.4)✓, (4.6,3.4)多, 多1 |
| lamp | (4.0,7.0) | (3.2,6.4)✓ | (3.6,6.8)✓ | (5.2,7.0)✓ |
| table | (6.0,3.0) | (6.5,3.7)✓ | (5.3,3.8)✓ | (5.1,3.9)✓ |
| trash bin | (4.0,1.0) | (3.9,2.1)✓ | (4.6,1.5)✓ | (5.1,0.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (7.0,2.0) | - | (7.6,2.0)✓ | (4.6,2.5)✗2.5 |
| lamp | (4.0,4.0) | - | (3.6,3.5)✓ | (5.2,4.5)✓ |
| table | (6.0,2.0) | - | (5.3,2.5)✓ | (5.1,1.5)✓ |
| trash bin | (4.0,1.0) | - | (4.6,1.0)✓ | (5.1,0.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (5.0,2.0) | - | (3.9,2.0)✓ | (3.4,2.5)✓ |
| lamp | (7.0,4.0) | - | (6.8,3.5)✓ | (7.0,4.5)✓ |
| table | (3.0,2.0) | - | (3.8,2.5)✓ | (3.9,1.5)✓ |
| trash bin | (1.0,1.0) | - | (1.5,1.0)✓ | (0.7,0.5)✓ |

- **baseline 问题**：多画 chair ×1（GT 1，模型 2）；chair-table 距离画错（GT 2.2，模型 1.0）；chair→table 方向错（GT NE，模型 N）；chair-trash bin 距离画错（GT 5.0，模型 2.8）
- **threeview 问题**：chair→table 方向错（GT NE，模型 E）；chair-trash bin 距离画错（GT 5.0，模型 2.5）；lamp-table 距离画错（GT 4.5，模型 2.2）；lamp-trash bin 距离画错（GT 6.0，模型 3.5）；table-trash bin 距离画错（GT 2.8，模型 1.6）；table→trash bin 方向错（GT NE，模型 N）；z 整体偏高（平均 +1.5 格）
- **threeview_3pass 问题**：多画 chair ×1（GT 1，模型 2）；chair→lamp 方向错（GT SE，模型 S）；chair-table 距离画错（GT 2.2，模型 1.0）；chair→table 方向错（GT NE，模型 S）；chair-trash bin 距离画错（GT 5.0，模型 3.6）；chair→trash bin 方向错（GT NE，模型 N）；lamp→table 方向错（GT NW，模型 N）；lamp-trash bin 距离画错（GT 6.0，模型 8.5）

### 样本 200 `578511c8a9`（scannetpp · obj_appearance_order）

Q：What will be the first-time appearance order of the following categories in the video: computer mouse, printer, monitor, exhaust fan?

- QA：GT B | baseline A（错） | threeview C（错） | threeview_3pass B（对）
- 对齐：baseline: yaw=-154° mirror=是(证据支持) 平移=(11.4,2.6) RMSE=0.40；threeview: yaw=-80° mirror=是(未证实) 平移=(9.4,10.2) RMSE=1.02；threeview_3pass: yaw=-150° mirror=是(证据支持) 平移=(11.3,3.3) RMSE=0.54
- 补偿：baseline: 尺度=0.91 z偏移=+0.00；threeview: 尺度=0.92 z偏移=-1.40；threeview_3pass: 尺度=0.92 z偏移=-1.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (4.0,3.0), (3.0,3.0), (3.0,4.0), (3.0,5.0), (3.0,5.0), (4.0,5.0), (7.0,4.0), (1.0,4.0) | (3.5,5.3)✓, 漏7 | (6.9,3.2)✓, 漏7 | (3.2,5.4)✓, 漏7 |
| exhaust fan | (3.0,0.0) | (3.0,0.0)✓ | (2.7,0.6)✓ | (3.1,-0.0)✓ |
| monitor | (7.0,5.0), (7.0,6.0), (7.0,5.0), (8.0,4.0), (3.0,4.0), (1.0,3.0), (2.0,2.0), (3.0,5.0), (3.0,5.0), (3.0,5.0), (3.0,4.0), (1.0,4.0), (4.0,3.0), (4.0,4.0), (4.0,4.0), (4.0,5.0) | (4.7,4.9)✓, 漏15 | (6.0,4.4)✓, 漏15 | (4.9,4.2)✓, 漏15 |
| printer | (7.0,7.0) | (6.8,6.9)✓ | (5.4,6.7)✓ | (6.8,6.4)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (4.0,3.0), (3.0,3.0), (3.0,3.0), (3.0,3.0), (3.0,3.0), (4.0,3.0), (7.0,3.0), (1.0,3.0) | - | (6.9,2.7)✓, 漏7 | (3.2,2.0)✓, 漏7 |
| exhaust fan | (3.0,7.0) | - | (2.7,7.1)✓ | (3.1,7.0)✓ |
| monitor | (7.0,3.0), (7.0,3.0), (7.0,3.0), (8.0,3.0), (3.0,3.0), (1.0,3.0), (2.0,3.0), (3.0,3.0), (3.0,3.0), (3.0,3.0), (3.0,3.0), (1.0,3.0), (4.0,3.0), (4.0,3.0), (4.0,3.0), (4.0,3.0) | - | (6.0,3.8)✓, 漏15 | (4.9,4.0)✓, 漏15 |
| printer | (7.0,3.0) | - | (5.4,2.9)✓ | (6.8,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| computer mouse | (3.0,3.0), (3.0,3.0), (4.0,3.0), (5.0,3.0), (5.0,3.0), (5.0,3.0), (4.0,3.0), (4.0,3.0) | - | (3.2,2.7)✓, 漏7 | (5.4,2.0)✓, 漏7 |
| exhaust fan | (0.0,7.0) | - | (0.6,7.1)✓ | (-0.0,7.0)✓ |
| monitor | (5.0,3.0), (6.0,3.0), (5.0,3.0), (4.0,3.0), (4.0,3.0), (3.0,3.0), (2.0,3.0), (5.0,3.0), (5.0,3.0), (5.0,3.0), (4.0,3.0), (4.0,3.0), (3.0,3.0), (4.0,3.0), (4.0,3.0), (5.0,3.0) | - | (4.4,3.8)✓, 漏15 | (4.2,4.0)✓, 漏15 |
| printer | (7.0,3.0) | - | (6.7,2.9)✓ | (6.4,3.0)✓ |

- **baseline 问题**：漏画 computer mouse ×7（GT 8，模型 1）；漏画 monitor ×15（GT 16，模型 1）；computer mouse-exhaust fan 距离画错（GT 3.0，模型 5.8）；computer mouse-monitor 距离画错（GT 0.0，模型 1.4）；computer mouse-printer 距离画错（GT 3.0，模型 4.0）；exhaust fan-monitor 距离画错（GT 2.2，模型 5.7）；monitor-printer 距离画错（GT 1.0，模型 3.2）
- **threeview 问题**：漏画 computer mouse ×7（GT 8，模型 1）；漏画 monitor ×15（GT 16，模型 1）；computer mouse-exhaust fan 距离画错（GT 3.0，模型 5.4）；computer mouse→exhaust fan 方向错（GT N，模型 NE）；computer mouse-monitor 距离画错（GT 0.0，模型 1.6）；computer mouse→monitor 方向错（GT W，模型 SE）；computer mouse-printer 距离画错（GT 3.0，模型 4.1）；computer mouse→printer 方向错（GT SW，模型 SE）
- **threeview_3pass 问题**：漏画 computer mouse ×7（GT 8，模型 1）；漏画 monitor ×15（GT 16，模型 1）；computer mouse-exhaust fan 距离画错（GT 3.0，模型 5.8）；computer mouse-monitor 距离画错（GT 0.0，模型 2.2）；computer mouse→monitor 方向错（GT W，模型 NW）；computer mouse-printer 距离画错（GT 3.0，模型 4.1）；computer mouse→printer 方向错（GT SW，模型 W）；exhaust fan-monitor 距离画错（GT 2.2，模型 5.0）
