# 50 样本逐样本并排对照（GT | TIS | 三视图，纯坐标对齐）

> TOP 用旋转+平移（必要时镜像）对齐；FRONT/SIDE 横向复用 TOP 变换，z 保持原始；不拟合尺度/z。偏差阈值 ≤2 格。

## 汇总

| arm | 正确 / 总数 | TOP ≤2 | FRONT ≤2 | SIDE ≤2 |
|---|---|---|---|---|
| baseline | 12 / 50 | 116/160 | - | - |
| threeview | 15 / 50 | 115/157 | 98/157 | 93/157 |
| threeview_3pass | 17 / 50 | 132/164 | 123/164 | 118/164 |

## 逐样本对照

### 样本 1 `09c1414f1b`（scannetpp · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the cutting board and the suitcase (in meters)?

- QA：GT 1.8 | baseline 1.3（错） | threeview 0.9（错） | threeview_3pass 1.65（错）
- 对齐：baseline: 2点 yaw=-60° mirror=否 平移=(-6.1,3.2) RMSE=0.48；threeview: 2点 yaw=-53° mirror=否 平移=(-5.2,4.0) RMSE=0.24；threeview_3pass: 2点 yaw=-60° mirror=否 平移=(-6.1,3.2) RMSE=0.48

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cutting board | (1.0,2.0) | (0.7,1.4)✓ | (1.2,2.3)✓ | (0.7,1.4)✓ |
| suitcase | (2.0,4.0) | (2.3,4.6)✓ | (1.9,3.7)✓ | (2.3,4.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cutting board | (1.0,5.0) | - | (1.2,6.2)✓ | (0.7,4.0)✓ |
| suitcase | (2.0,1.0) | - | (1.9,3.5)✗2.5 | (2.3,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cutting board | (2.0,5.0) | - | (2.3,6.2)✓ | (1.4,4.0)✓ |
| suitcase | (4.0,1.0) | - | (3.7,3.5)✗2.5 | (4.6,2.0)✓ |

- **baseline 问题**：cutting board-suitcase 距离画错（GT 2.2，模型 3.6）
- **threeview 问题**：z 整体偏高（平均 +1.9 格）
- **threeview_3pass 问题**：cutting board-suitcase 距离画错（GT 2.2，模型 3.6）

### 样本 2 `47334103`（arkitscenes · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the table and the stool (in meters)?

- QA：GT 3.7 | baseline 0.3（错） | threeview 0.3（错） | threeview_3pass 0.4（错）
- 对齐：baseline: 2点 yaw=-11° mirror=否 平移=(-0.9,-2.5) RMSE=1.45；threeview: 2点 yaw=-40° mirror=否 平移=(-2.3,0.7) RMSE=1.44；threeview_3pass: 2点 yaw=-11° mirror=否 平移=(-0.9,-2.5) RMSE=1.45

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (2.0,2.0) | (4.0,1.6)✗2.0, (6.0,1.2)多, 多1 | (4.0,1.6)✗2.0, (5.2,0.6)多, 多1 | (4.0,1.6)✗2.0, (6.0,1.2)多, 多1 |
| table | (7.0,1.0) | (5.0,1.4)✗2.0 | (5.0,1.4)✗2.0 | (5.0,1.4)✗2.0 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (2.0,1.0) | - | (4.0,3.2)✗3.0, (5.2,3.2)多, 多1 | (4.0,3.0)✗2.8, (6.0,3.0)多, 多1 |
| table | (7.0,2.0) | - | (5.0,4.2)✗3.0 | (5.0,4.0)✗2.8 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (2.0,1.0) | - | (1.6,3.2)✗2.2, (0.6,3.2)多, 多1 | (1.6,3.0)✗2.0, (1.2,3.0)多, 多1 |
| table | (1.0,2.0) | - | (1.4,4.2)✗2.2 | (1.4,4.0)✗2.0 |

- **baseline 问题**：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 5.1，模型 1.0）；stool→table 方向错（GT W，模型 N）
- **threeview 问题**：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 5.1，模型 0.9）；stool→table 方向错（GT W，模型 SW）；z 整体偏高（平均 +2.2 格）
- **threeview_3pass 问题**：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 5.1，模型 1.0）；stool→table 方向错（GT W，模型 N）；z 整体偏高（平均 +2.0 格）

### 样本 3 `42897538`（arkitscenes · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the stool and the refrigerator (in meters)?

- QA：GT 2.6 | baseline 1.5（错） | threeview 1.2（错） | threeview_3pass 1.7（错）
- 对齐：baseline: 2点 yaw=-34° mirror=否 平移=(-3.1,1.3) RMSE=0.14；threeview: 2点 yaw=-40° mirror=否 平移=(-4.7,2.1) RMSE=0.54；threeview_3pass: 2点 yaw=-143° mirror=否 平移=(2.2,11.9) RMSE=0.35

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (3.0,7.0) | (3.0,6.8)✓ | (3.0,6.2)✓ | (3.0,7.5)✓ |
| stool | (3.0,3.0) | (3.0,3.2)✓, (3.8,2.6)多, 多1 | (3.0,3.8)✓ | (3.0,2.5)✓, (1.4,1.3)多, 多1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (3.0,4.0) | - | (3.0,5.5)✓ | (3.0,4.0)✓ |
| stool | (3.0,1.0) | - | (3.0,2.8)✓ | (3.0,1.0)✓, (1.4,1.0)多, 多1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (7.0,4.0) | - | (6.2,5.5)✓ | (7.5,4.0)✓ |
| stool | (3.0,1.0) | - | (3.8,2.8)✓ | (2.5,1.0)✓, (1.3,1.0)多, 多1 |

- **baseline 问题**：多画 stool ×1（GT 1，模型 2）
- **threeview 问题**：refrigerator-stool 距离画错（GT 4.0，模型 2.5）；z 整体偏高（平均 +1.6 格）
- **threeview_3pass 问题**：多画 stool ×1（GT 1，模型 2）

### 样本 4 `scene0550_00`（scannet · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the door and the window (in meters)?

- QA：GT 2.5 | baseline 3.5（错） | threeview 3.1（错） | threeview_3pass 2.5（对）
- 对齐：baseline: 2点 yaw=-37° mirror=否 平移=(0.3,3.9) RMSE=0.50；threeview: 2点 yaw=-88° mirror=否 平移=(-4.9,7.5) RMSE=1.25；threeview_3pass: 2点 yaw=-127° mirror=否 平移=(0.7,11.1) RMSE=0.50

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (4.0,8.0) | (4.1,7.3)✓ | (4.3,6.2)✓ | (4.1,7.3)✓ |
| window | (5.0,1.0) | (4.9,1.7)✓ | (4.7,2.8)✓ | (4.9,1.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (4.0,4.0) | - | (4.3,4.5)✓ | (4.1,4.0)✓ |
| window | (5.0,5.0) | - | (4.7,5.5)✓ | (4.9,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (8.0,4.0) | - | (6.2,4.5)✓ | (7.3,4.0)✓ |
| window | (1.0,5.0) | - | (2.8,5.5)✓ | (1.7,5.0)✓ |

- **baseline 问题**：door-window 距离画错（GT 7.1，模型 5.7）
- **threeview 问题**：door-window 距离画错（GT 7.1，模型 3.5）；z 整体偏高（平均 +0.5 格）
- **threeview_3pass 问题**：door-window 距离画错（GT 7.1，模型 5.7）

### 样本 5 `scene0378_01`（scannet · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the door and the clock (in meters)?

- QA：GT 1.6 | baseline 2.0（错） | threeview 3.5（错） | threeview_3pass 3（错）
- 对齐：baseline: 2点 yaw=-172° mirror=否 平移=(6.9,5.9) RMSE=0.46；threeview: 2点 yaw=-150° mirror=否 平移=(5.8,5.7) RMSE=0.76；threeview_3pass: 2点 yaw=-153° mirror=否 平移=(5.8,5.5) RMSE=0.88

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| clock | (3.0,2.0) | (2.4,2.2)✓ | (2.0,2.3)✓ | (1.8,2.4)✓ |
| door | (6.0,1.0) | (6.6,0.8)✓ | (7.0,0.7)✓ | (7.2,0.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| clock | (3.0,7.0) | - | (2.0,7.5)✓ | (1.8,7.0)✓ |
| door | (6.0,4.0) | - | (7.0,4.5)✓ | (7.2,4.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| clock | (2.0,7.0) | - | (2.3,7.5)✓ | (2.4,7.0)✓ |
| door | (1.0,4.0) | - | (0.7,4.5)✓ | (0.6,4.0)✓ |

- **baseline 问题**：clock-door 距离画错（GT 3.2，模型 4.5）
- **threeview 问题**：clock-door 距离画错（GT 3.2，模型 5.3）；z 整体偏高（平均 +0.5 格）
- **threeview_3pass 问题**：clock-door 距离画错（GT 3.2，模型 5.7）

### 样本 6 `c49a8c6cff`（scannetpp · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the trash can and the bed (in meters)?

- QA：GT 0.7 | baseline 1.5（错） | threeview 1.5（错） | threeview_3pass 1.5（错）
- 对齐：baseline: 2点 yaw=121° mirror=否 平移=(12.9,3.3) RMSE=0.04；threeview: 2点 yaw=36° mirror=否 平移=(4.5,-1.6) RMSE=0.08；threeview_3pass: 2点 yaw=20° mirror=否 平移=(3.1,-2.3) RMSE=0.18

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,5.0) | (6.1,5.0)✓ | (5.9,5.0)✓ | (5.7,5.1)✓ |
| trash can | (2.0,6.0) | (1.9,6.0)✓ | (2.1,6.0)✓ | (2.3,5.9)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,2.0) | - | (5.9,3.5)✓ | (5.7,3.0)✓ |
| trash can | (2.0,1.0) | - | (2.1,2.0)✓ | (2.3,1.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,2.0) | - | (5.0,3.5)✓ | (5.1,3.0)✓ |
| trash can | (6.0,1.0) | - | (6.0,2.0)✓ | (5.9,1.0)✓ |

- **threeview 问题**：z 整体偏高（平均 +1.2 格）
- **threeview_3pass 问题**：z 整体偏高（平均 +0.5 格）

### 样本 7 `3db0a1c8f3`（scannetpp · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the blanket and the computer mouse (in meters)?

- QA：GT 0.8 | baseline 1.2（错） | threeview 1.1（错） | threeview_3pass 1.0（错）
- 对齐：baseline: 2点 yaw=90° mirror=否 平移=(6.0,-4.0) RMSE=0.00；threeview: 2点 yaw=90° mirror=否 平移=(6.5,-3.5) RMSE=0.30；threeview_3pass: 2点 yaw=72° mirror=否 平移=(4.4,-5.1) RMSE=0.21

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blanket | (1.0,1.0) | (1.0,1.0)✓ | (1.3,1.3)✓ | (1.2,1.2)✓ |
| computer mouse | (3.0,3.0) | (3.0,3.0)✓ | (2.7,2.7)✓ | (2.8,2.8)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blanket | (1.0,2.0) | - | (1.3,3.8)✓ | (1.2,4.0)✗2.0 |
| computer mouse | (3.0,2.0) | - | (2.7,4.2)✗2.2 | (2.8,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| blanket | (1.0,2.0) | - | (1.3,3.8)✓ | (1.2,4.0)✗2.0 |
| computer mouse | (3.0,2.0) | - | (2.7,4.2)✗2.2 | (2.8,3.0)✓ |

- **threeview 问题**：z 整体偏高（平均 +2.0 格）
- **threeview_3pass 问题**：z 整体偏高（平均 +1.5 格）

### 样本 8 `c50d2d1d42`（scannetpp · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the door and the telephone (in meters)?

- QA：GT 4.6 | baseline 2.0（错） | threeview 4.5（错） | threeview_3pass 2.1（错）
- 对齐：baseline: 2点 yaw=14° mirror=否 平移=(1.7,-2.1) RMSE=1.02；threeview: 2点 yaw=53° mirror=否 平移=(7.3,-3.2) RMSE=0.71；threeview_3pass: 2点 yaw=14° mirror=否 平移=(1.7,-2.1) RMSE=1.02

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (0.0,3.0) | (1.4,3.0)✓ | (1.0,3.0)✓ | (1.4,3.0)✓ |
| telephone | (7.0,3.0) | (5.6,3.0)✓ | (6.0,3.0)✓ | (5.6,3.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (0.0,3.0) | - | (1.0,5.2)✗2.4 | (1.4,5.0)✗2.5 |
| telephone | (7.0,3.0) | - | (6.0,3.8)✓ | (5.6,4.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (3.0,3.0) | - | (3.0,5.2)✗2.2 | (3.0,5.0)✓ |
| telephone | (3.0,3.0) | - | (3.0,3.8)✓ | (3.0,4.0)✓ |

- **baseline 问题**：door-telephone 距离画错（GT 7.0，模型 4.1）
- **threeview 问题**：door-telephone 距离画错（GT 7.0，模型 5.0）；z 整体偏高（平均 +1.5 格）
- **threeview_3pass 问题**：door-telephone 距离画错（GT 7.0，模型 4.1）；z 整体偏高（平均 +1.5 格）

### 样本 9 `scene0474_04`（scannet · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the table and the trash bin (in meters)?

- QA：GT 1.9 | baseline 1.1（错） | threeview 0.4（错） | threeview_3pass 1.3（错）
- 对齐：baseline: 2点 yaw=169° mirror=否 平移=(10.3,10.6) RMSE=0.27；threeview: 2点 yaw=124° mirror=否 平移=(11.4,3.9) RMSE=0.57；threeview_3pass: 2点 yaw=-180° mirror=否 平移=(9.0,11.0) RMSE=0.00

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (4.0,6.0) | (4.2,5.7)✓ | (4.4,5.3)✓ | (4.0,6.0)✓ |
| trash bin | (6.0,3.0) | (5.8,3.3)✓ | (5.6,3.7)✓ | (6.0,3.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (4.0,2.0) | - | (4.4,4.0)✗2.0 | (4.0,3.0)✓ |
| trash bin | (6.0,1.0) | - | (5.6,2.0)✓ | (6.0,1.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| table | (6.0,2.0) | - | (5.3,4.0)✗2.1 | (6.0,3.0)✓ |
| trash bin | (3.0,1.0) | - | (3.7,2.0)✓ | (3.0,1.0)✓ |

- **threeview 问题**：table-trash bin 距离画错（GT 3.6，模型 2.0）；z 整体偏高（平均 +1.5 格）
- **threeview_3pass 问题**：z 整体偏高（平均 +0.5 格）

### 样本 10 `47333899`（arkitscenes · object_abs_distance）

Q：Measuring from the closest point of each object, what is the distance between the table and the stove (in meters)?

- QA：GT 0.9 | baseline 1.2（错） | threeview 1.5（错） | threeview_3pass 2.5（错）
- 对齐：baseline: 2点 yaw=-108° mirror=否 平移=(-2.1,9.1) RMSE=1.00；threeview: 2点 yaw=-37° mirror=否 平移=(-5.7,1.2) RMSE=0.93；threeview_3pass: 2点 yaw=-127° mirror=否 平移=(0.8,9.9) RMSE=0.35

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (2.0,7.0) | (2.0,5.6)✓ | (2.0,5.7)✓ | (2.0,6.5)✓ |
| table | (2.0,1.0) | (2.0,2.4)✓ | (2.0,2.3)✓ | (2.0,1.5)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (2.0,4.0) | - | (2.0,4.5)✓ | (2.0,3.0)✓ |
| table | (2.0,2.0) | - | (2.0,3.5)✓ | (2.0,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (7.0,4.0) | - | (5.7,4.5)✓ | (6.5,3.0)✓ |
| table | (1.0,2.0) | - | (2.3,3.5)✓ | (1.5,3.0)✓ |

- **baseline 问题**：stove-table 距离画错（GT 6.0，模型 3.2）
- **threeview 问题**：stove-table 距离画错（GT 6.0，模型 3.4）；z 整体偏高（平均 +1.0 格）
- **threeview_3pass 问题**：stove-table 距离画错（GT 6.0，模型 5.0）

### 样本 11 `scene0221_01`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (chair, bed, pillow, lamp) is the closest to the microwave?

- QA：GT B | baseline A（错） | threeview A（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=72° mirror=否 平移=(6.9,-3.5) RMSE=1.85；threeview: yaw=-2° mirror=否 平移=(-0.6,-1.3) RMSE=0.58；threeview_3pass: yaw=56° mirror=否 平移=(5.5,-4.9) RMSE=1.10

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (4.0,3.0), (2.0,3.0) | (3.1,0.9)✗2.3, 漏1 | (4.5,3.6)✓, 漏1 | (2.4,3.2)✓, 漏1 |
| chair | (3.0,6.0), (1.0,6.0), (2.0,7.0) | (5.3,4.4)✗2.8, 漏2 | (2.1,6.2)✓, 漏2 | (4.1,5.7)✓, 漏2 |
| lamp | (3.0,1.0), (3.0,0.0) | (0.9,0.6)✗2.2, 漏1 | (2.0,1.2)✓, 漏1 | (3.3,-1.0)✓, 漏1 |
| microwave | (6.0,1.0) | (6.6,5.0)✗4.0 | 漏1 | 漏1 |
| pillow | (2.0,1.0), (4.0,1.0), (4.0,1.0), (4.0,1.0), (2.0,1.0) | (2.1,1.2)✓, 漏4 | (4.5,1.1)✓, 漏4 | (3.5,1.2)✓, (3.5,1.2)✗2.0, (4.7,2.9)多, 漏3 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (4.0,2.0), (2.0,3.0) | - | (4.5,3.0)✓, 漏1 | (2.4,3.0)✓, 漏1 |
| chair | (3.0,3.0), (1.0,5.0), (2.0,4.0) | - | (2.1,3.5)✓, 漏2 | (4.1,3.0)✓, 漏2 |
| lamp | (3.0,4.0), (3.0,5.0) | - | (2.0,5.0)✓, 漏1 | (3.3,5.0)✓, 漏1 |
| microwave | (6.0,5.0) | - | 漏1 | 漏1 |
| pillow | (2.0,4.0), (4.0,4.0), (4.0,4.0), (4.0,4.0), (2.0,4.0) | - | (4.5,4.0)✓, 漏4 | (3.5,4.0)✓, (3.5,4.0)✓, (4.7,4.0)多, 漏3 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (3.0,2.0), (3.0,3.0) | - | (3.6,3.0)✓, 漏1 | (3.2,3.0)✓, 漏1 |
| chair | (6.0,3.0), (6.0,5.0), (7.0,4.0) | - | (6.2,3.5)✓, 漏2 | (5.7,3.0)✓, 漏2 |
| lamp | (1.0,4.0), (0.0,5.0) | - | (1.2,5.0)✓, 漏1 | (-1.0,5.0)✓, 漏1 |
| microwave | (1.0,5.0) | - | 漏1 | 漏1 |
| pillow | (1.0,4.0), (1.0,4.0), (1.0,4.0), (1.0,4.0), (1.0,4.0) | - | (1.1,4.0)✓, 漏4 | (1.2,4.0)✓, (1.2,4.0)✓, (2.9,4.0)多, 漏3 |

- **baseline 问题**：漏画 bed ×1（GT 2，模型 1）；漏画 pillow ×4（GT 5，模型 1）；漏画 lamp ×1（GT 2，模型 1）；漏画 chair ×2（GT 3，模型 1）；bed→chair 方向错（GT S，模型 SW）；bed→lamp 方向错（GT N，模型 E）；bed-microwave 距离画错（GT 2.8，模型 5.4）；bed→microwave 方向错（GT NW，模型 SW）
- **threeview 问题**：漏画 microwave ×1（GT 1，模型 0）；漏画 bed ×1（GT 2，模型 1）；漏画 pillow ×4（GT 5，模型 1）；漏画 lamp ×1（GT 2，模型 1）；漏画 chair ×2（GT 3，模型 1）；bed→chair 方向错（GT S，模型 SE）；bed-lamp 距离画错（GT 2.2，模型 3.5）；bed→lamp 方向错（GT N，模型 NE）
- **threeview_3pass 问题**：漏画 microwave ×1（GT 1，模型 0）；漏画 bed ×1（GT 2，模型 1）；漏画 pillow ×3（GT 5，模型 2）；漏画 lamp ×1（GT 2，模型 1）；漏画 chair ×2（GT 3，模型 1）；bed→chair 方向错（GT S，模型 SW）；bed-lamp 距离画错（GT 2.2，模型 4.2）；bed→pillow 方向错（GT N，模型 NW）

### 样本 12 `scene0307_02`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (window, chair, door, washing machine) is the closest to the radiator?

- QA：GT C | baseline A（错） | threeview A（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=-32° mirror=否 平移=(-3.9,3.6) RMSE=2.09；threeview: yaw=98° mirror=否 平移=(9.2,2.5) RMSE=2.01；threeview_3pass: yaw=74° mirror=否 平移=(7.3,-0.0) RMSE=2.11

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,6.0) | (3.5,6.0)✓ | (4.1,6.3)✓ | (3.9,6.2)✓ |
| door | (3.0,5.0), (4.0,7.0), (3.0,5.0), (1.0,7.0), (7.0,3.0) | (-0.4,7.3)✓, 漏4 | (6.5,3.7)✓, 漏4 | (6.6,1.2)✓, 漏4 |
| radiator | (1.0,5.0) | (4.5,1.8)✗4.7 | (-0.3,8.7)✗4.0 | (-0.2,6.3)✓ |
| washing machine | (2.0,7.0) | (2.9,8.7)✓ | (2.2,5.1)✓ | (1.9,9.9)✗2.9 |
| window | (4.0,1.0), (2.0,7.0), (4.0,1.0) | (3.4,0.2)✓, 漏2 | (-0.5,6.2)✗2.6, 漏2 | (-0.2,6.3)✗2.3, 漏2 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,2.0) | - | (4.1,3.5)✓ | (3.9,3.0)✓ |
| door | (3.0,4.0), (4.0,4.0), (3.0,4.0), (1.0,4.0), (7.0,4.0) | - | (6.5,5.0)✓, 漏4 | (6.6,4.0)✓, 漏4 |
| radiator | (1.0,3.0) | - | (-0.3,4.0)✓ | (-0.2,3.0)✓ |
| washing machine | (2.0,2.0) | - | (2.2,4.5)✗2.5 | (1.9,3.0)✓ |
| window | (4.0,6.0), (2.0,6.0), (4.0,6.0) | - | (-0.5,6.5)✗2.5, 漏2 | (-0.2,6.0)✗2.2, 漏2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (6.0,2.0) | - | (6.3,3.5)✓ | (6.2,3.0)✓ |
| door | (5.0,4.0), (7.0,4.0), (5.0,4.0), (7.0,4.0), (3.0,4.0) | - | (3.7,5.0)✓, 漏4 | (1.2,4.0)✓, 漏4 |
| radiator | (5.0,3.0) | - | (8.7,4.0)✗3.9 | (6.3,3.0)✓ |
| washing machine | (7.0,2.0) | - | (5.1,4.5)✗3.2 | (9.9,3.0)✗3.1 |
| window | (1.0,6.0), (7.0,6.0), (1.0,6.0) | - | (6.2,6.5)✓, 漏2 | (6.3,6.0)✓, 漏2 |

- **baseline 问题**：漏画 door ×4（GT 5，模型 1）；漏画 window ×2（GT 3，模型 1）；chair-door 距离画错（GT 1.0，模型 4.1）；chair→door 方向错（GT NE，模型 E）；chair-radiator 距离画错（GT 3.2，模型 4.2）；chair→radiator 方向错（GT E，模型 N）；chair→washing machine 方向错（GT SE，模型 S）；chair-window 距离画错（GT 2.2，模型 5.8）
- **threeview 问题**：漏画 door ×4（GT 5，模型 1）；漏画 window ×2（GT 3，模型 1）；chair-door 距离画错（GT 1.0，模型 3.6）；chair→door 方向错（GT NE，模型 NW）；chair-radiator 距离画错（GT 3.2，模型 5.0）；chair→radiator 方向错（GT E，模型 SE）；chair→washing machine 方向错（GT SE，模型 NE）；chair-window 距离画错（GT 2.2，模型 4.5）
- **threeview_3pass 问题**：漏画 door ×4（GT 5，模型 1）；漏画 window ×2（GT 3，模型 1）；chair-door 距离画错（GT 1.0，模型 5.7）；chair→door 方向错（GT NE，模型 NW）；chair-washing machine 距离画错（GT 2.2，模型 4.2）；chair-window 距离画错（GT 2.2，模型 4.1）；chair→window 方向错（GT N，模型 E）；door-radiator 距离画错（GT 2.0，模型 8.5）

### 样本 13 `47429977`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (stove, chair, refrigerator, table) is the closest to the tv?

- QA：GT D | baseline B（错） | threeview B（错） | threeview_3pass D（对）
- 对齐：baseline: yaw=-87° mirror=否 平移=(-1.3,8.1) RMSE=1.35；threeview: yaw=-72° mirror=否 平移=(-2.2,6.5) RMSE=1.68；threeview_3pass: yaw=-35° mirror=是(未证实) 平移=(2.7,9.3) RMSE=1.31

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,1.0), (3.0,2.0), (3.0,1.0) | (4.0,2.3)✓, (5.1,1.4)✓, (5.0,3.4)✗3.1, (6.0,2.4)多, 多1 | (4.4,2.4)✓, (5.1,3.7)✗2.6, (5.1,3.7)✗2.8, (5.7,1.8)多, (6.3,3.0)多, 多1 | (3.3,1.5)✓, (4.7,1.8)✓, (3.0,2.9)✓, (4.4,3.2)多, 多1 |
| refrigerator | (2.0,7.0) | (0.8,6.2)✓ | (1.3,5.6)✓ | (3.1,6.5)✓ |
| stove | (1.0,3.0) | (0.9,4.2)✓ | (1.0,3.4)✓ | (-0.3,1.6)✓ |
| table | (6.0,4.0), (3.0,1.0) | (5.0,2.4)✓, 漏1 | (5.4,2.7)✓, 漏1 | (3.8,2.3)✓, 漏1 |
| tv | (6.0,1.0) | (4.2,-0.7)✗2.5 | (2.2,-0.4)✗4.1 | (6.3,0.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,3.0), (3.0,3.0), (3.0,3.0) | - | (4.4,3.0)✓, (5.1,3.0)✗2.1, (5.1,3.0)✗2.7, (5.7,3.0)多, (6.3,3.0)多, 多1 | (3.0,2.0)✓, (4.4,2.0)✓, (4.7,2.0)✓, (3.3,2.0)多, 多1 |
| refrigerator | (2.0,4.0) | - | (1.3,6.0)✗2.1 | (3.1,4.0)✓ |
| stove | (1.0,5.0) | - | (1.0,4.0)✓ | (-0.3,3.0)✗2.4 |
| table | (6.0,2.0), (3.0,3.0) | - | (5.4,4.0)✗2.1, 漏1 | (3.8,3.0)✓, 漏1 |
| tv | (6.0,6.0) | - | (2.2,5.0)✗3.9 | (6.3,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (1.0,3.0), (2.0,3.0), (1.0,3.0) | - | (1.8,3.0)✓, (1.8,3.0)✓, (1.8,3.0)✗2.0, (3.7,3.0)多, (2.4,3.0)多, (3.0,3.0)多, 多1 | (1.8,2.0)✓, (3.2,2.0)✓, (2.9,2.0)✗2.2, (1.5,2.0)多, 多1 |
| refrigerator | (7.0,4.0) | - | (5.6,6.0)✗2.5 | (6.5,4.0)✓ |
| stove | (3.0,5.0) | - | (3.4,4.0)✓ | (1.6,3.0)✗2.4 |
| table | (4.0,2.0), (1.0,3.0) | - | (2.7,4.0)✓, 漏1 | (2.3,3.0)✓, 漏1 |
| tv | (1.0,6.0) | - | (-0.4,5.0)✓ | (0.6,5.0)✓ |

- **baseline 问题**：漏画 table ×1（GT 2，模型 1）；多画 chair ×1（GT 3，模型 4）；chair→refrigerator 方向错（GT S，模型 SE）；chair-stove 距离画错（GT 2.2，模型 3.6）；chair→table 方向错（GT SW，模型 S）；chair→tv 方向错（GT W，模型 N）；refrigerator-stove 距离画错（GT 4.1，模型 2.0）；stove-table 距离画错（GT 2.8，模型 4.5）
- **threeview 问题**：漏画 table ×1（GT 2，模型 1）；多画 chair ×1（GT 3，模型 4）；chair→refrigerator 方向错（GT S，模型 SE）；chair-stove 距离画错（GT 2.2，模型 3.6）；chair→stove 方向错（GT SE，模型 E）；chair→table 方向错（GT SW，模型 E）；chair-tv 距离画错（GT 2.0，模型 3.6）；chair→tv 方向错（GT W，模型 NE）
- **threeview_3pass 问题**：漏画 table ×1（GT 2，模型 1）；多画 chair ×1（GT 3，模型 4）；chair-refrigerator 距离画错（GT 5.1，模型 3.6）；chair-stove 距离画错（GT 2.2，模型 3.6）；chair→stove 方向错（GT SE，模型 E）；chair→table 方向错（GT SW，模型 E）；chair→tv 方向错（GT W，模型 NW）；refrigerator-stove 距离画错（GT 4.1，模型 6.0）

### 样本 14 `scene0653_00`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (window, monitor, table, keyboard) is the closest to the door?

- QA：GT C | baseline B（错） | threeview D（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=-121° mirror=否 平移=(3.5,11.1) RMSE=1.25；threeview: yaw=-177° mirror=是(未证实) 平移=(10.5,-0.9) RMSE=1.12；threeview_3pass: yaw=54° mirror=是(未证实) 平移=(-1.6,3.0) RMSE=1.28

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (7.0,7.0) | (7.3,7.6)✓ | (8.6,7.0)✓ | (6.9,7.9)✓ |
| keyboard | (2.0,3.0), (6.0,2.0) | (6.1,3.7)✓, 漏1 | (5.2,4.3)✗2.4, 漏1 | (6.2,3.5)✓, 漏1 |
| monitor | (1.0,6.0), (2.0,3.0), (2.0,3.0), (6.0,1.0), (7.0,1.0), (6.0,4.0), (6.0,6.0) | (4.3,4.7)✓, 漏6 | (5.3,3.3)✓, 漏6 | (4.6,4.7)✓, 漏6 |
| table | (1.0,6.0), (2.0,3.0), (6.0,4.0), (2.0,4.0), (7.0,1.0), (6.0,6.0) | (6.9,3.2)✓, 漏5 | (5.2,3.8)✓, 漏5 | (7.0,2.9)✓, 漏5 |
| window | (1.0,5.0), (1.0,2.0) | (1.4,1.8)✓, 漏1 | (1.7,3.6)✓, 漏1 | (1.4,2.0)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (7.0,5.0) | - | (8.6,5.0)✓ | (6.9,4.0)✓ |
| keyboard | (2.0,2.0), (6.0,2.0) | - | (5.2,4.2)✗2.3, 漏1 | (6.2,4.0)✗2.0, 漏1 |
| monitor | (1.0,3.0), (2.0,3.0), (2.0,3.0), (6.0,3.0), (7.0,3.0), (6.0,3.0), (6.0,3.0) | - | (5.3,5.5)✗2.6, 漏6 | (4.6,5.0)✗2.5, 漏6 |
| table | (1.0,2.0), (2.0,2.0), (6.0,2.0), (2.0,1.0), (7.0,2.0), (6.0,2.0) | - | (5.2,3.5)✓, 漏5 | (7.0,3.0)✓, 漏5 |
| window | (1.0,5.0), (1.0,5.0) | - | (1.7,6.0)✓, 漏1 | (1.4,5.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (7.0,5.0) | - | (7.0,5.0)✓ | (7.9,4.0)✓ |
| keyboard | (3.0,2.0), (2.0,2.0) | - | (4.3,4.2)✗2.6, 漏1 | (3.5,4.0)✗2.1, 漏1 |
| monitor | (6.0,3.0), (3.0,3.0), (3.0,3.0), (1.0,3.0), (1.0,3.0), (4.0,3.0), (6.0,3.0) | - | (3.3,5.5)✗2.5, 漏6 | (4.7,5.0)✗2.1, 漏6 |
| table | (6.0,2.0), (3.0,2.0), (4.0,2.0), (4.0,1.0), (1.0,2.0), (6.0,2.0) | - | (3.8,3.5)✓, 漏5 | (2.9,3.0)✓, 漏5 |
| window | (5.0,5.0), (2.0,5.0) | - | (3.6,6.0)✓, 漏1 | (2.0,5.0)✓, 漏1 |

- **baseline 问题**：漏画 keyboard ×1（GT 2，模型 1）；漏画 monitor ×6（GT 7，模型 1）；漏画 table ×5（GT 6，模型 1）；漏画 window ×1（GT 2，模型 1）；door→keyboard 方向错（GT NE，模型 N）；door-monitor 距离画错（GT 1.4，模型 4.1）；door-table 距离画错（GT 1.4，模型 4.5）；door→table 方向错（GT NE，模型 N）
- **threeview 问题**：漏画 keyboard ×1（GT 2，模型 1）；漏画 monitor ×6（GT 7，模型 1）；漏画 table ×5（GT 6，模型 1）；漏画 window ×1（GT 2，模型 1）；door-monitor 距离画错（GT 1.4，模型 4.9）；door-table 距离画错（GT 1.4，模型 4.6）；door-window 距离画错（GT 6.3，模型 7.6）；keyboard→monitor 方向错（GT S，模型 N）
- **threeview_3pass 问题**：漏画 keyboard ×1（GT 2，模型 1）；漏画 monitor ×6（GT 7，模型 1）；漏画 table ×5（GT 6，模型 1）；漏画 window ×1（GT 2，模型 1）；door→keyboard 方向错（GT NE，模型 N）；door-monitor 距离画错（GT 1.4，模型 4.0）；door-table 距离画错（GT 1.4，模型 5.0）；door→table 方向错（GT NE，模型 N）

### 样本 15 `38d58a7a31`（scannetpp · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (telephone, heater, chair, ceiling light) is the closest to the trash can?

- QA：GT C | baseline A（错） | threeview C（对） | threeview_3pass C（对）
- 对齐：baseline: yaw=-168° mirror=是(未证实) 平移=(10.2,-0.9) RMSE=1.52；threeview: yaw=160° mirror=是(证据支持) 平移=(7.7,-1.8) RMSE=1.00；threeview_3pass: yaw=16° mirror=否 平移=(1.8,-2.7) RMSE=1.33

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (4.0,1.0), (1.0,2.0), (4.0,6.0), (1.0,3.0), (4.0,5.0), (4.0,3.0), (6.0,1.0), (7.0,6.0), (6.0,4.0), (6.0,3.0) | (5.1,-1.0)✗2.2, 漏9 | (4.7,4.6)✓, 漏9 | (6.3,-0.3)✓, 漏9 |
| chair | (1.0,6.0), (3.0,6.0), (4.0,4.0), (5.0,5.0), (6.0,4.0), (2.0,5.0), (2.0,7.0), (5.0,3.0), (4.0,3.0), (4.0,6.0), (6.0,6.0), (6.0,1.0), (1.0,6.0), (6.0,2.0), (3.0,6.0), (4.0,6.0), (1.0,7.0), (2.0,5.0), (5.0,6.0), (3.0,3.0), (5.0,4.0), (6.0,4.0), (6.0,2.0), (5.0,2.0), (7.0,3.0), (7.0,6.0), (6.0,6.0), (3.0,5.0), (2.0,2.0), (3.0,5.0), (2.0,3.0), (1.0,7.0), (1.0,7.0), (1.0,6.0), (1.0,6.0), (1.0,6.0) | (5.1,4.1)✓, 漏35 | (4.0,4.3)✓, 漏35 | (2.7,4.9)✓, (2.7,4.9)✓, (6.5,6.0)多, 漏34 |
| heater | (7.0,4.0), (8.0,6.0), (7.0,1.0) | (7.8,5.7)✓, 漏2 | (8.5,6.4)✓, 漏2 | (8.7,5.6)✓, 漏2 |
| telephone | (7.0,2.0) | (4.3,2.9)✗2.9 | (5.1,2.9)✗2.1 | (4.2,3.2)✗3.0 |
| trash can | (1.0,4.0) | (0.7,5.2)✓ | (2.7,3.7)✓ | (1.5,5.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (4.0,7.0), (1.0,7.0), (4.0,8.0), (1.0,8.0), (4.0,7.0), (4.0,7.0), (6.0,8.0), (7.0,7.0), (6.0,8.0), (6.0,7.0) | - | (4.7,9.0)✓, 漏9 | (6.3,9.0)✓, 漏9 |
| chair | (1.0,2.0), (3.0,2.0), (4.0,2.0), (5.0,2.0), (6.0,2.0), (2.0,2.0), (2.0,2.0), (5.0,2.0), (4.0,2.0), (4.0,2.0), (6.0,2.0), (6.0,1.0), (1.0,2.0), (6.0,2.0), (3.0,2.0), (4.0,1.0), (1.0,2.0), (2.0,1.0), (5.0,2.0), (3.0,1.0), (5.0,2.0), (6.0,1.0), (6.0,2.0), (5.0,2.0), (7.0,2.0), (7.0,2.0), (6.0,2.0), (3.0,2.0), (2.0,2.0), (3.0,2.0), (2.0,2.0), (1.0,2.0), (1.0,2.0), (1.0,2.0), (1.0,2.0), (1.0,1.0) | - | (4.0,3.5)✓, 漏35 | (2.7,3.0)✓, (2.7,3.0)✓, (6.5,3.0)多, 漏34 |
| heater | (7.0,1.0), (8.0,1.0), (7.0,1.0) | - | (8.5,3.0)✗2.1, 漏2 | (8.7,3.0)✗2.1, 漏2 |
| telephone | (7.0,3.0) | - | (5.1,5.0)✗2.8 | (4.2,4.0)✗2.9 |
| trash can | (1.0,1.0) | - | (2.7,2.0)✗2.0 | (1.5,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (1.0,7.0), (2.0,7.0), (6.0,8.0), (3.0,8.0), (5.0,7.0), (3.0,7.0), (1.0,8.0), (6.0,7.0), (4.0,8.0), (3.0,7.0) | - | (4.6,9.0)✓, 漏9 | (-0.3,9.0)✓, 漏9 |
| chair | (6.0,2.0), (6.0,2.0), (4.0,2.0), (5.0,2.0), (4.0,2.0), (5.0,2.0), (7.0,2.0), (3.0,2.0), (3.0,2.0), (6.0,2.0), (6.0,2.0), (1.0,1.0), (6.0,2.0), (2.0,2.0), (6.0,2.0), (6.0,1.0), (7.0,2.0), (5.0,1.0), (6.0,2.0), (3.0,1.0), (4.0,2.0), (4.0,1.0), (2.0,2.0), (2.0,2.0), (3.0,2.0), (6.0,2.0), (6.0,2.0), (5.0,2.0), (2.0,2.0), (5.0,2.0), (3.0,2.0), (7.0,2.0), (7.0,2.0), (6.0,2.0), (6.0,2.0), (6.0,1.0) | - | (4.3,3.5)✓, 漏35 | (6.0,3.0)✓, (4.9,3.0)✓, 漏34 |
| heater | (4.0,1.0), (6.0,1.0), (1.0,1.0) | - | (6.4,3.0)✗2.0, 漏2 | (5.6,3.0)✗2.0, 漏2 |
| telephone | (2.0,3.0) | - | (2.9,5.0)✗2.2 | (3.2,4.0)✓ |
| trash can | (4.0,1.0) | - | (3.7,2.0)✓ | (5.6,2.0)✓ |

- **baseline 问题**：漏画 ceiling light ×9（GT 10，模型 1）；漏画 heater ×2（GT 3，模型 1）；漏画 chair ×35（GT 36，模型 1）；ceiling light-chair 距离画错（GT 0.0，模型 5.1）；ceiling light→chair 方向错（GT SE，模型 S）；ceiling light-heater 距离画错（GT 1.0，模型 7.2）；ceiling light→heater 方向错（GT W，模型 S）；ceiling light-telephone 距离画错（GT 1.4，模型 4.0）
- **threeview 问题**：漏画 ceiling light ×9（GT 10，模型 1）；漏画 heater ×2（GT 3，模型 1）；漏画 chair ×35（GT 36，模型 1）；ceiling light→chair 方向错（GT SE，模型 NE）；ceiling light-heater 距离画错（GT 1.0，模型 4.2）；ceiling light→heater 方向错（GT W，模型 SW）；ceiling light→telephone 方向错（GT NW，模型 N）；ceiling light-trash can 距离画错（GT 1.0，模型 2.1）
- **threeview_3pass 问题**：漏画 ceiling light ×9（GT 10，模型 1）；漏画 heater ×2（GT 3，模型 1）；漏画 chair ×34（GT 36，模型 2）；ceiling light-chair 距离画错（GT 0.0，模型 6.3）；ceiling light→chair 方向错（GT SE，模型 S）；ceiling light-heater 距离画错（GT 1.0，模型 6.4）；ceiling light→heater 方向错（GT W，模型 S）；ceiling light-telephone 距离画错（GT 1.4，模型 4.1）

### 样本 16 `42899461`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (chair, sofa, fireplace, stove) is the closest to the tv?

- QA：GT A | baseline C（错） | threeview C（错） | threeview_3pass C（错）
- 对齐：baseline: yaw=56° mirror=是(未证实) 平移=(-2.5,4.9) RMSE=1.18；threeview: yaw=45° mirror=否 平移=(4.8,-1.0) RMSE=1.18；threeview_3pass: yaw=31° mirror=是(未证实) 平移=(-2.6,7.4) RMSE=1.37

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (7.0,4.0), (7.0,3.0), (2.0,4.0), (1.0,4.0) | (3.3,4.6)✓, 漏3 | (3.3,3.2)✓, 漏3 | (3.1,3.7)✓, (3.1,3.7)✓, (6.5,5.8)多, 漏2 |
| fireplace | (4.0,8.0) | (1.9,7.9)✗2.1 | (2.6,8.2)✓ | (2.8,8.2)✓ |
| sofa | (7.0,6.0) | (6.1,5.1)✓ | (5.5,5.4)✓ | (5.3,3.9)✗2.7 |
| stove | (1.0,1.0) | 漏1 | 漏1 | 漏1 |
| tv | (1.0,7.0) | (2.8,7.4)✓ | (2.6,8.2)✓ | (3.3,7.3)✗2.3 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (7.0,3.0), (7.0,3.0), (2.0,4.0), (1.0,4.0) | - | (3.3,3.0)✓, 漏3 | (6.5,2.0)✓, (3.1,2.0)✗2.3, 漏2 |
| fireplace | (4.0,4.0) | - | (2.6,4.0)✓ | (2.8,2.0)✗2.3 |
| sofa | (7.0,4.0) | - | (5.5,3.0)✓ | (5.3,2.0)✗2.6 |
| stove | (1.0,7.0) | - | 漏1 | 漏1 |
| tv | (1.0,5.0) | - | (2.6,7.0)✗2.6 | (3.3,5.0)✗2.3 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,3.0), (3.0,3.0), (4.0,4.0), (4.0,4.0) | - | (3.2,3.0)✓, 漏3 | (3.7,2.0)✓, (3.7,2.0)✗2.7, (5.8,2.0)多, 漏2 |
| fireplace | (8.0,4.0) | - | (8.2,4.0)✓ | (8.2,2.0)✗2.0 |
| sofa | (6.0,4.0) | - | (5.4,3.0)✓ | (3.9,2.0)✗2.9 |
| stove | (1.0,7.0) | - | 漏1 | 漏1 |
| tv | (7.0,5.0) | - | (8.2,7.0)✗2.3 | (7.3,5.0)✓ |

- **baseline 问题**：漏画 stove ×1（GT 1，模型 0）；漏画 chair ×3（GT 4，模型 1）；chair→sofa 方向错（GT SW，模型 W）；chair→tv 方向错（GT SE，模型 S）；fireplace-sofa 距离画错（GT 3.6，模型 5.0）；fireplace-tv 距离画错（GT 3.2，模型 1.0）；fireplace→tv 方向错（GT E，模型 NW）；sofa-tv 距离画错（GT 6.1，模型 4.0）
- **threeview 问题**：漏画 stove ×1（GT 1，模型 0）；漏画 chair ×3（GT 4，模型 1）；chair-sofa 距离画错（GT 2.0，模型 3.0）；chair-tv 距离画错（GT 3.0，模型 5.0）；chair→tv 方向错（GT SE，模型 S）；fireplace-tv 距离画错（GT 3.2，模型 0.0）；sofa-tv 距离画错（GT 6.1，模型 4.0）；sofa→tv 方向错（GT E，模型 SE）
- **threeview_3pass 问题**：漏画 stove ×1（GT 1，模型 0）；漏画 chair ×2（GT 4，模型 2）；chair→fireplace 方向错（GT S，模型 SE）；chair→sofa 方向错（GT SW，模型 NW）；fireplace-sofa 距离画错（GT 3.6，模型 5.0）；fireplace-tv 距离画错（GT 3.2，模型 1.0）；fireplace→tv 方向错（GT E，模型 NW）；sofa-tv 距离画错（GT 6.1，模型 4.0）

### 样本 17 `42899461`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (table, tv, sofa, stove) is the closest to the fireplace?

- QA：GT A | baseline B（错） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=81° mirror=否 平移=(8.8,0.9) RMSE=0.69；threeview: yaw=72° mirror=否 平移=(9.3,0.2) RMSE=0.93；threeview_3pass: yaw=74° mirror=否 平移=(8.8,0.5) RMSE=0.83

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| fireplace | (4.0,8.0) | 漏1 | (2.2,7.7)✓ | (2.6,7.6)✓ |
| sofa | (7.0,6.0) | (7.6,6.2)✓ | (7.5,6.1)✓ | (7.4,6.2)✓ |
| stove | (1.0,1.0) | 漏1 | 漏1 | 漏1 |
| table | (6.0,7.0), (1.0,7.0), (6.0,3.0) | (4.7,6.7)✓, 漏2 | (5.6,6.7)✓, 漏2 | (5.5,6.7)✓, 漏2 |
| tv | (1.0,7.0) | (1.7,7.2)✓ | (2.7,7.6)✓ | (2.6,7.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| fireplace | (4.0,4.0) | - | (2.2,3.0)✗2.0 | (2.6,3.0)✓ |
| sofa | (7.0,4.0) | - | (7.5,3.5)✓ | (7.4,2.0)✗2.0 |
| stove | (1.0,7.0) | - | 漏1 | 漏1 |
| table | (6.0,2.0), (1.0,2.0), (6.0,3.0) | - | (5.6,2.5)✓, 漏2 | (5.5,2.0)✓, 漏2 |
| tv | (1.0,5.0) | - | (2.7,6.5)✗2.3 | (2.6,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| fireplace | (8.0,4.0) | - | (7.7,3.0)✓ | (7.6,3.0)✓ |
| sofa | (6.0,4.0) | - | (6.1,3.5)✓ | (6.2,2.0)✗2.0 |
| stove | (1.0,7.0) | - | 漏1 | 漏1 |
| table | (7.0,2.0), (7.0,2.0), (3.0,3.0) | - | (6.7,2.5)✓, 漏2 | (6.7,2.0)✓, 漏2 |
| tv | (7.0,5.0) | - | (7.6,6.5)✓ | (7.6,6.0)✓ |

- **baseline 问题**：漏画 table ×2（GT 3，模型 1）；漏画 fireplace ×1（GT 1，模型 0）；漏画 stove ×1（GT 1，模型 0）；sofa-table 距离画错（GT 1.4，模型 3.0）；table-tv 距离画错（GT 0.0，模型 3.0）
- **threeview 问题**：漏画 stove ×1（GT 1，模型 0）；漏画 table ×2（GT 3，模型 1）；fireplace-sofa 距离画错（GT 3.6，模型 5.5）；fireplace→sofa 方向错（GT NW，模型 W）；fireplace-table 距离画错（GT 2.2，模型 3.5）；fireplace→table 方向错（GT N，模型 W）；fireplace-tv 距离画错（GT 3.2，模型 0.5）；fireplace→tv 方向错（GT E，模型 W）
- **threeview_3pass 问题**：漏画 stove ×1（GT 1，模型 0）；漏画 table ×2（GT 3，模型 1）；fireplace-sofa 距离画错（GT 3.6，模型 5.0）；fireplace→sofa 方向错（GT NW，模型 W）；fireplace→table 方向错（GT N，模型 W）；fireplace-tv 距离画错（GT 3.2，模型 0.0）；sofa-tv 距离画错（GT 6.1，模型 5.0）；table-tv 距离画错（GT 0.0，模型 3.0）

### 样本 18 `47430034`（arkitscenes · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (chair, stool, table, bed) is the closest to the tv?

- QA：GT C | baseline D（错） | threeview D（错） | threeview_3pass C（对）
- 对齐：baseline: yaw=10° mirror=否 平移=(2.1,-1.0) RMSE=1.89；threeview: yaw=-29° mirror=否 平移=(-0.7,1.6) RMSE=0.99；threeview_3pass: yaw=-22° mirror=否 平移=(-1.2,0.6) RMSE=0.45

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,2.0) | (6.2,4.8)✗3.0 | (5.8,3.2)✓ | (5.0,2.4)✓ |
| chair | (5.0,7.0), (6.0,7.0), (1.0,2.0) | (3.7,7.4)✓, 漏2 | (4.1,5.2)✓, 漏2 | (4.6,6.9)✓, 漏2 |
| stool | (4.0,3.0) | 漏1 | 漏1 | 漏1 |
| table | (4.0,3.0), (6.0,7.0), (1.0,2.0) | (3.9,6.4)✗2.2, 漏2 | (3.4,3.9)✓, 漏2 | (6.4,6.1)✓, 漏2 |
| tv | (7.0,7.0) | (9.3,4.4)✗3.5 | (7.7,6.7)✓ | (7.0,7.5)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (5.0,4.0) | - | (5.8,3.0)✓ | (5.0,2.5)✓ |
| chair | (5.0,3.0), (6.0,3.0), (1.0,2.0) | - | (4.1,3.5)✓, 漏2 | (4.6,3.0)✓, 漏2 |
| stool | (4.0,1.0) | - | 漏1 | 漏1 |
| table | (4.0,2.0), (6.0,2.0), (1.0,2.0) | - | (3.4,3.0)✓, 漏2 | (6.4,3.0)✓, 漏2 |
| tv | (7.0,6.0) | - | (7.7,5.5)✓ | (7.0,5.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (2.0,4.0) | - | (3.2,3.0)✓ | (2.4,2.5)✓ |
| chair | (7.0,3.0), (7.0,3.0), (2.0,2.0) | - | (5.2,3.5)✓, 漏2 | (6.9,3.0)✓, 漏2 |
| stool | (3.0,1.0) | - | 漏1 | 漏1 |
| table | (3.0,2.0), (7.0,2.0), (2.0,2.0) | - | (3.9,3.0)✓, 漏2 | (6.1,3.0)✓, 漏2 |
| tv | (7.0,6.0) | - | (6.7,5.5)✓ | (7.5,5.5)✓ |

- **baseline 问题**：漏画 table ×2（GT 3，模型 1）；漏画 stool ×1（GT 1，模型 0）；漏画 chair ×2（GT 3，模型 1）；bed→chair 方向错（GT S，模型 SE）；bed-table 距离画错（GT 1.4，模型 2.8）；bed-tv 距离画错（GT 5.4，模型 3.2）；bed→tv 方向错（GT S，模型 W）；chair-table 距离画错（GT 0.0，模型 1.0）
- **threeview 问题**：漏画 table ×2（GT 3，模型 1）；漏画 stool ×1（GT 1，模型 0）；漏画 chair ×2（GT 3，模型 1）；bed-chair 距离画错（GT 4.0，模型 2.7）；bed→chair 方向错（GT S，模型 SE）；bed-table 距离画错（GT 1.4，模型 2.5）；bed→table 方向错（GT SE，模型 E）；bed-tv 距离画错（GT 5.4，模型 4.0）
- **threeview_3pass 问题**：漏画 table ×2（GT 3，模型 1）；漏画 stool ×1（GT 1，模型 0）；漏画 chair ×2（GT 3，模型 1）；bed-table 距离画错（GT 1.4，模型 4.0）；bed→table 方向错（GT SE，模型 S）；chair-table 距离画错（GT 0.0，模型 2.0）；chair→table 方向错（GT N，模型 W）；chair-tv 距离画错（GT 1.0，模型 2.5）

### 样本 19 `scene0616_01`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (table, trash bin, chair, lamp) is the closest to the window?

- QA：GT A | baseline A（对） | threeview D（错） | threeview_3pass A（对）
- 对齐：baseline: yaw=-100° mirror=是(未证实) 平移=(9.5,7.3) RMSE=1.33；threeview: yaw=123° mirror=否 平移=(11.0,2.1) RMSE=1.26；threeview_3pass: yaw=50° mirror=是(证据支持) 平移=(-2.5,2.6) RMSE=1.72

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,2.0), (4.0,2.0), (4.0,3.0), (3.0,5.0), (3.0,4.0), (5.0,6.0), (6.0,5.0) | (4.5,2.1)✓, (4.8,4.1)✓, 漏5 | (5.4,4.4)✓, 漏6 | (3.9,2.4)✓, (3.9,2.4)✓, (5.2,3.9)多, 漏5 |
| lamp | (5.0,1.0) | (6.1,-0.2)✓ | (4.2,2.5)✓ | (4.9,-1.0)✗2.0 |
| table | (5.0,1.0), (3.0,3.0) | (3.7,3.3)✓, 漏1 | (4.1,3.6)✓, 漏1 | (4.5,3.2)✓, 漏1 |
| trash bin | (7.0,4.0), (7.0,4.0) | (7.2,5.7)✓, 漏1 | (5.6,2.2)✗2.3, 漏1 | (4.9,6.8)✗3.4, 漏1 |
| window | (1.0,3.0) | (-0.3,4.0)✓ | (0.7,1.4)✓ | (1.5,5.7)✗2.8 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,2.0), (4.0,2.0), (4.0,2.0), (3.0,2.0), (3.0,2.0), (5.0,2.0), (6.0,2.0) | - | (5.4,3.5)✓, 漏6 | (3.9,3.0)✓, (3.9,3.0)✓, (5.2,3.0)多, 漏5 |
| lamp | (5.0,4.0) | - | (4.2,6.0)✗2.1 | (4.9,6.0)✗2.0 |
| table | (5.0,2.0), (3.0,2.0) | - | (4.1,4.0)✗2.2, 漏1 | (4.5,3.0)✓, 漏1 |
| trash bin | (7.0,2.0), (7.0,2.0) | - | (5.6,2.0)✓, 漏1 | (4.9,1.0)✗2.3, 漏1 |
| window | (1.0,5.0) | - | (0.7,7.0)✗2.0 | (1.5,6.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (2.0,2.0), (2.0,2.0), (3.0,2.0), (5.0,2.0), (4.0,2.0), (6.0,2.0), (5.0,2.0) | - | (4.4,3.5)✓, 漏6 | (3.9,3.0)✓, (2.4,3.0)✓, 漏5 |
| lamp | (1.0,4.0) | - | (2.5,6.0)✗2.5 | (-1.0,6.0)✗2.9 |
| table | (1.0,2.0), (3.0,2.0) | - | (3.6,4.0)✗2.1, 漏1 | (3.2,3.0)✓, 漏1 |
| trash bin | (4.0,2.0), (4.0,2.0) | - | (2.2,2.0)✓, 漏1 | (6.8,1.0)✗2.9, 漏1 |
| window | (3.0,5.0) | - | (1.4,7.0)✗2.6 | (5.7,6.0)✗2.9 |

- **baseline 问题**：漏画 trash bin ×1（GT 2，模型 1）；漏画 table ×1（GT 2，模型 1）；漏画 chair ×5（GT 7，模型 2）；chair-lamp 距离画错（GT 1.4，模型 2.8）；chair→lamp 方向错（GT N，模型 NW）；chair→table 方向错（GT N，模型 E）；chair-trash bin 距离画错（GT 1.4，模型 2.8）；chair→trash bin 方向错（GT W，模型 SW）
- **threeview 问题**：漏画 trash bin ×1（GT 2，模型 1）；漏画 table ×1（GT 2，模型 1）；漏画 chair ×6（GT 7，模型 1）；chair→lamp 方向错（GT N，模型 NE）；chair→table 方向错（GT N，模型 NE）；chair→trash bin 方向错（GT W，模型 N）；chair-window 距离画错（GT 2.2，模型 5.5）；chair→window 方向错（GT E，模型 NE）
- **threeview_3pass 问题**：漏画 trash bin ×1（GT 2，模型 1）；漏画 table ×1（GT 2，模型 1）；漏画 chair ×5（GT 7，模型 2）；chair-lamp 距离画错（GT 1.4，模型 3.6）；chair→table 方向错（GT N，模型 E）；chair-trash bin 距离画错（GT 1.4，模型 2.8）；chair→trash bin 方向错（GT W，模型 S）；chair-window 距离画错（GT 2.2，模型 4.1）

### 样本 20 `scene0651_02`（scannet · object_rel_distance）

Q：Measuring from the closest point of each object, which of these objects (counter, chair, table, trash bin) is the closest to the sofa?

- QA：GT C | baseline C（对） | threeview C（对） | threeview_3pass B（错）
- 对齐：baseline: yaw=4° mirror=否 平移=(1.1,-1.9) RMSE=0.84；threeview: yaw=7° mirror=否 平移=(0.9,-2.2) RMSE=0.80；threeview_3pass: yaw=3° mirror=否 平移=(0.8,-1.8) RMSE=0.86

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (7.0,4.0), (5.0,3.0), (5.0,4.0), (6.0,3.0) | (7.7,3.6)✓, (3.7,3.3)✓, 漏2 | (3.3,3.2)✓, 漏3 | (4.5,4.4)✓, (4.5,4.4)✓, (4.6,2.4)✓, (4.6,2.4)✓, (6.6,2.5)多, (6.5,4.5)多 |
| counter | (3.0,6.0) | (1.5,6.1)✓ | 漏1 | (2.4,6.3)✓ |
| sofa | (5.0,1.0) | (5.9,0.4)✓ | (5.5,1.4)✓ | (5.7,0.4)✓ |
| table | (3.0,2.0), (5.0,3.0) | (5.7,3.4)✓, 漏1 | (5.3,3.4)✓, 漏1 | (5.5,3.4)✓, 漏1 |
| trash bin | (1.0,6.0) | (1.4,7.1)✓ | (1.9,6.0)✓ | (1.4,6.2)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (7.0,2.0), (5.0,3.0), (5.0,3.0), (6.0,3.0) | - | (3.3,4.0)✓, 漏3 | (4.6,3.0)✓, (4.5,3.0)✓, (6.6,3.0)✓, (4.6,3.0)✓, (6.5,3.0)多 |
| counter | (3.0,5.0) | - | 漏1 | (2.4,4.0)✓ |
| sofa | (5.0,3.0) | - | (5.5,4.0)✓ | (5.7,3.0)✓ |
| table | (3.0,1.0), (5.0,2.0) | - | (5.3,3.0)✓, 漏1 | (5.5,3.0)✓, 漏1 |
| trash bin | (1.0,1.0) | - | (1.9,2.0)✓ | (1.4,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,2.0), (3.0,3.0), (4.0,3.0), (3.0,3.0) | - | (3.2,4.0)✓, 漏3 | (4.4,3.0)✓, (2.5,3.0)✓, (2.4,3.0)✓, (2.4,3.0)✓, (4.5,3.0)多 |
| counter | (6.0,5.0) | - | 漏1 | (6.3,4.0)✓ |
| sofa | (1.0,3.0) | - | (1.4,4.0)✓ | (0.4,3.0)✓ |
| table | (2.0,1.0), (3.0,2.0) | - | (3.4,3.0)✓, 漏1 | (3.4,3.0)✓, 漏1 |
| trash bin | (6.0,1.0) | - | (6.0,2.0)✓ | (6.2,2.0)✓ |

- **baseline 问题**：漏画 table ×1（GT 2，模型 1）；漏画 chair ×2（GT 4，模型 2）；chair-sofa 距离画错（GT 2.0，模型 3.6）；chair-table 距离画错（GT 0.0，模型 2.0）；chair→table 方向错（GT NE，模型 E）；counter-sofa 距离画错（GT 5.4，模型 7.2）；counter→sofa 方向错（GT N，模型 NW）；counter-table 距离画错（GT 3.6，模型 5.0）
- **threeview 问题**：漏画 table ×1（GT 2，模型 1）；漏画 counter ×1（GT 1，模型 0）；漏画 chair ×3（GT 4，模型 1）；chair→sofa 方向错（GT N，模型 NW）；chair-table 距离画错（GT 0.0，模型 2.0）；chair→table 方向错（GT NE，模型 W）；chair-trash bin 距离画错（GT 4.5，模型 3.2）；sofa→table 方向错（GT SE，模型 S）
- **threeview_3pass 问题**：漏画 table ×1（GT 2，模型 1）；chair-table 距离画错（GT 0.0，模型 1.4）；chair→table 方向错（GT NE，模型 W）；counter-sofa 距离画错（GT 5.4，模型 6.7）；counter→sofa 方向错（GT N，模型 NW）；counter→table 方向错（GT N，模型 NW）；sofa→table 方向错（GT SE，模型 S）

### 样本 21 `31a2c91c43`（scannetpp · object_rel_direction_easy）

Q：If I am standing by the ceiling light and facing the toilet, is the door to the left or the right of the toilet?

- QA：GT A | baseline B（错） | threeview A（对） | threeview_3pass B（错）
- 对齐：baseline: yaw=13° mirror=是(证据支持) 平移=(0.1,8.2) RMSE=0.33；threeview: yaw=34° mirror=否 平移=(4.2,-1.1) RMSE=1.40；threeview_3pass: yaw=9° mirror=是(证据支持) 平移=(-0.0,8.7) RMSE=0.30

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (5.0,8.0) | (5.2,8.3)✓ | (5.5,5.9)✗2.2 | (5.1,8.5)✓ |
| door | (2.0,4.0) | (2.2,3.5)✓ | (2.2,3.6)✓ | (1.8,3.9)✓ |
| toilet | (6.0,2.0) | (5.6,2.2)✓ | (5.3,4.5)✗2.6 | (6.2,1.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (5.0,8.0) | - | (5.5,9.0)✓ | (5.1,9.0)✓ |
| door | (2.0,4.0) | - | (2.2,5.0)✓ | (1.8,4.0)✓ |
| toilet | (6.0,1.0) | - | (5.3,2.0)✓ | (6.2,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (8.0,8.0) | - | (5.9,9.0)✗2.3 | (8.5,9.0)✓ |
| door | (4.0,4.0) | - | (3.6,5.0)✓ | (3.9,4.0)✓ |
| toilet | (2.0,1.0) | - | (4.5,2.0)✗2.7 | (1.6,2.0)✓ |

- **baseline 问题**：door→toilet 方向错（GT NW，模型 W）
- **threeview 问题**：ceiling light-toilet 距离画错（GT 6.1，模型 1.4）；door-toilet 距离画错（GT 4.5，模型 3.2）；door→toilet 方向错（GT NW，模型 W）；z 整体偏高（平均 +1.0 格）
- **threeview_3pass 问题**：z 整体偏高（平均 +0.7 格）

### 样本 22 `scene0353_00`（scannet · object_rel_direction_easy）

Q：If I am standing by the bookshelf and facing the door, is the refrigerator to the left or the right of the door?

- QA：GT A | baseline B（错） | threeview A（对） | threeview_3pass B（错）
- 对齐：baseline: yaw=-106° mirror=是(证据支持) 平移=(12.8,5.0) RMSE=1.49；threeview: yaw=-112° mirror=是(证据支持) 平移=(13.1,4.8) RMSE=1.25；threeview_3pass: yaw=-111° mirror=是(证据支持) 平移=(12.6,4.5) RMSE=1.57

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bookshelf | (7.0,1.0) | (6.8,-1.6)✗2.6 | (6.2,-0.5)✓ | (7.0,-1.9)✗2.9 |
| door | (7.0,3.0) | (7.7,5.4)✗2.5 | (7.9,5.2)✗2.4 | (7.6,5.4)✗2.4 |
| refrigerator | (5.0,5.0) | (4.5,5.2)✓ | (4.9,4.3)✓ | (4.4,5.5)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bookshelf | (7.0,3.0) | - | (6.2,5.0)✗2.2 | (7.0,4.0)✓ |
| door | (7.0,4.0) | - | (7.9,5.5)✓ | (7.6,4.0)✓ |
| refrigerator | (5.0,2.0) | - | (4.9,4.5)✗2.5 | (4.4,4.0)✗2.1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bookshelf | (1.0,3.0) | - | (-0.5,5.0)✗2.5 | (-1.9,4.0)✗3.1 |
| door | (3.0,4.0) | - | (5.2,5.5)✗2.7 | (5.4,4.0)✗2.4 |
| refrigerator | (5.0,2.0) | - | (4.3,4.5)✗2.6 | (5.5,4.0)✗2.1 |

- **baseline 问题**：bookshelf-door 距离画错（GT 2.0，模型 7.1）；bookshelf-refrigerator 距离画错（GT 4.5，模型 7.2）；bookshelf→refrigerator 方向错（GT SE，模型 S）；door→refrigerator 方向错（GT SE，模型 E）
- **threeview 问题**：bookshelf-door 距离画错（GT 2.0，模型 6.0）；bookshelf→refrigerator 方向错（GT SE，模型 S）；door→refrigerator 方向错（GT SE，模型 E）；z 整体偏高（平均 +2.0 格）
- **threeview_3pass 问题**：bookshelf-door 距离画错（GT 2.0，模型 7.3）；bookshelf-refrigerator 距离画错（GT 4.5，模型 7.8）；bookshelf→refrigerator 方向错（GT SE，模型 S）；door→refrigerator 方向错（GT SE，模型 E）；z 整体偏高（平均 +1.0 格）

### 样本 23 `41159525`（arkitscenes · object_rel_direction_easy）

Q：If I am standing by the stove and facing the table, is the refrigerator to the left or the right of the table?

- QA：GT B | baseline A（错） | threeview A（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=106° mirror=是(证据支持) 平移=(0.5,-3.6) RMSE=1.89；threeview: yaw=140° mirror=是(证据支持) 平移=(3.8,-3.9) RMSE=1.10；threeview_3pass: yaw=130° mirror=是(证据支持) 平移=(3.6,-4.0) RMSE=0.95

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (6.0,1.0) | (5.0,-1.3)✗2.5 | (5.1,-0.0)✓ | (5.3,0.1)✓ |
| stove | (1.0,1.0) | (3.9,2.6)✗3.3 | (2.9,1.8)✗2.1 | (2.6,1.8)✓ |
| table | (6.0,5.0) | (4.0,5.7)✗2.1 | (5.0,5.2)✓ | (5.0,5.1)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (6.0,4.0) | - | (5.1,5.8)✗2.0 | (5.3,4.0)✓ |
| stove | (1.0,4.0) | - | (2.9,4.3)✓ | (2.6,3.0)✓ |
| table | (6.0,2.0) | - | (5.0,3.4)✓ | (5.0,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (1.0,4.0) | - | (-0.0,5.8)✗2.1 | (0.1,4.0)✓ |
| stove | (1.0,4.0) | - | (1.8,4.3)✓ | (1.8,3.0)✓ |
| table | (5.0,2.0) | - | (5.2,3.4)✓ | (5.1,3.0)✓ |

- **baseline 问题**：refrigerator-stove 距离画错（GT 5.0，模型 4.0）；refrigerator→stove 方向错（GT E，模型 S）；refrigerator-table 距离画错（GT 4.0，模型 7.1）；stove-table 距离画错（GT 6.4，模型 3.2）；stove→table 方向错（GT SW，模型 S）
- **threeview 问题**：refrigerator-stove 距离画错（GT 5.0，模型 2.8）；refrigerator→stove 方向错（GT E，模型 SE）；refrigerator-table 距离画错（GT 4.0，模型 5.2）；stove-table 距离画错（GT 6.4，模型 4.0）；z 整体偏高（平均 +1.2 格）
- **threeview_3pass 问题**：refrigerator-stove 距离画错（GT 5.0，模型 3.2）；refrigerator→stove 方向错（GT E，模型 SE）；stove-table 距离画错（GT 6.4，模型 4.1）

### 样本 24 `d755b3d9d8`（scannetpp · object_rel_direction_easy）

Q：If I am standing by the cup and facing the whiteboard, is the shoes to the left or the right of the whiteboard?

- QA：GT A | baseline A（对） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=-134° mirror=否 平移=(4.4,9.9) RMSE=1.70；threeview: yaw=-132° mirror=否 平移=(4.3,10.6) RMSE=1.29；threeview_3pass: yaw=-139° mirror=否 平移=(4.4,10.4) RMSE=1.52

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cup | (5.0,1.0) | (4.4,4.2)✗3.3 | (4.7,3.5)✗2.5 | (4.7,4.0)✗3.0 |
| shoes | (7.0,4.0) | (8.0,2.2)✗2.1 | (6.9,2.9)✓ | (7.4,2.4)✓ |
| whiteboard | (2.0,7.0) | (1.6,5.6)✓ | (2.5,5.5)✓ | (2.0,5.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cup | (5.0,2.0) | - | (4.7,4.0)✗2.0 | (4.7,4.0)✗2.0 |
| shoes | (7.0,0.0) | - | (6.9,1.0)✓ | (7.4,1.0)✓ |
| whiteboard | (2.0,4.0) | - | (2.5,6.0)✗2.1 | (2.0,6.0)✗2.0 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cup | (1.0,2.0) | - | (3.5,4.0)✗3.2 | (4.0,4.0)✗3.6 |
| shoes | (4.0,0.0) | - | (2.9,1.0)✓ | (2.4,1.0)✓ |
| whiteboard | (7.0,4.0) | - | (5.5,6.0)✗2.5 | (5.6,6.0)✗2.4 |

- **baseline 问题**：cup→shoes 方向错（GT SW，模型 NW）；cup-whiteboard 距离画错（GT 6.7，模型 3.2）；shoes-whiteboard 距离画错（GT 5.8，模型 7.3）
- **threeview 问题**：cup-shoes 距离画错（GT 3.6，模型 2.2）；cup→shoes 方向错（GT SW，模型 W）；cup-whiteboard 距离画错（GT 6.7，模型 3.0）；z 整体偏高（平均 +1.7 格）
- **threeview_3pass 问题**：cup→shoes 方向错（GT SW，模型 NW）；cup-whiteboard 距离画错（GT 6.7，模型 3.2）；z 整体偏高（平均 +1.7 格）

### 样本 25 `47204578`（arkitscenes · object_rel_direction_easy）

Q：If I am standing by the tv and facing the table, is the stool to the left or the right of the table?

- QA：GT A | baseline A（对） | threeview B（错） | threeview_3pass A（对）
- 对齐：baseline: yaw=45° mirror=是(证据支持) 平移=(-5.5,3.9) RMSE=1.86；threeview: yaw=-4° mirror=否 平移=(-3.0,-3.8) RMSE=1.90；threeview_3pass: yaw=36° mirror=否 平移=(0.6,-2.6) RMSE=1.56

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (1.0,1.0) | (0.1,3.9)✗3.1, (1.5,5.4)多, 多1 | (0.8,0.9)✓ | (0.4,3.5)✗2.6, (2.8,5.3)多, 多1 |
| table | (2.0,7.0) | (1.5,3.9)✗3.1 | (2.6,3.8)✗3.3 | (1.6,4.4)✗2.7 |
| tv | (3.0,1.0) | (4.4,1.1)✓ | (2.6,4.3)✗3.3 | (4.0,1.1)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (1.0,1.0) | - | (0.8,2.5)✓ | (0.4,2.5)✓, (2.8,2.5)多, 多1 |
| table | (2.0,2.0) | - | (2.6,3.5)✓ | (1.6,3.5)✓ |
| tv | (3.0,6.0) | - | (2.6,6.0)✓ | (4.0,6.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (1.0,1.0) | - | (0.9,2.5)✓ | (3.5,2.5)✗2.9, (5.3,2.5)多, 多1 |
| table | (7.0,2.0) | - | (3.8,3.5)✗3.5 | (4.4,3.5)✗3.0 |
| tv | (1.0,6.0) | - | (4.3,6.0)✗3.3 | (1.1,6.5)✓ |

- **baseline 问题**：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 6.1，模型 1.4）；stool→table 方向错（GT S，模型 NW）；stool-tv 距离画错（GT 2.0，模型 5.1）；stool→tv 方向错（GT W，模型 NW）；table-tv 距离画错（GT 6.1，模型 4.0）；table→tv 方向错（GT N，模型 NW）
- **threeview 问题**：stool-table 距离画错（GT 6.1，模型 3.4）；stool→table 方向错（GT S，模型 SW）；stool-tv 距离画错（GT 2.0，模型 3.8）；stool→tv 方向错（GT W，模型 SW）；table-tv 距离画错（GT 6.1，模型 0.5）；table→tv 方向错（GT N，模型 S）；z 整体偏高（平均 +1.0 格）
- **threeview_3pass 问题**：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 6.1，模型 1.5）；stool→table 方向错（GT S，模型 W）；stool-tv 距离画错（GT 2.0，模型 4.3）；stool→tv 方向错（GT W，模型 NW）；table-tv 距离画错（GT 6.1，模型 4.0）；table→tv 方向错（GT N，模型 NW）；z 整体偏高（平均 +1.2 格）

### 样本 26 `scene0458_00`（scannet · object_rel_direction_easy）

Q：If I am standing by the window and facing the door, is the mirror to the left or the right of the door?

- QA：GT B | baseline B（对） | threeview A（错） | threeview_3pass B（对）
- 对齐：baseline: yaw=-89° mirror=否 平移=(-0.7,9.3) RMSE=2.13；threeview: yaw=-144° mirror=否 平移=(7.1,10.0) RMSE=2.28；threeview_3pass: yaw=-141° mirror=否 平移=(4.7,10.5) RMSE=0.59

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (8.0,6.0) | (7.3,8.4)✗2.5 | (6.3,7.6)✗2.3 | (7.1,6.0)✓ |
| mirror | (1.0,6.0) | (4.3,4.3)✗3.7 | (5.1,4.2)✗4.5 | (2.1,5.8)✓ |
| window | (6.0,1.0) | (3.4,0.3)✗2.7 | (3.6,1.2)✗2.4 | (5.8,1.2)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (8.0,5.0) | - | (6.3,5.0)✓ | (7.1,4.0)✓ |
| mirror | (1.0,4.0) | - | (5.1,6.0)✗4.6 | (2.1,5.0)✓ |
| window | (6.0,5.0) | - | (3.6,6.5)✗2.9 | (5.8,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (6.0,5.0) | - | (7.6,5.0)✓ | (6.0,4.0)✓ |
| mirror | (6.0,4.0) | - | (4.2,6.0)✗2.7 | (5.8,5.0)✓ |
| window | (1.0,5.0) | - | (1.2,6.5)✓ | (1.2,5.0)✓ |

- **baseline 问题**：door-mirror 距离画错（GT 7.0，模型 5.0）；door→mirror 方向错（GT E，模型 NE）；door-window 距离画错（GT 5.4，模型 8.9）；door→window 方向错（GT N，模型 NE）；mirror-window 距离画错（GT 7.1，模型 4.1）；mirror→window 方向错（GT NW，模型 N）
- **threeview 问题**：door-mirror 距离画错（GT 7.0，模型 3.6）；door→mirror 方向错（GT E，模型 N）；door-window 距离画错（GT 5.4，模型 6.9）；door→window 方向错（GT N，模型 NE）；mirror-window 距离画错（GT 7.1，模型 3.4）；mirror→window 方向错（GT NW，模型 NE）；z 整体偏高（平均 +1.2 格）
- **threeview_3pass 问题**：door-mirror 距离画错（GT 7.0，模型 5.0）；mirror-window 距离画错（GT 7.1，模型 6.0）

### 样本 27 `scene0426_00`（scannet · object_rel_direction_easy）

Q：If I am standing by the tv and facing the lamp, is the table to the left or the right of the lamp?

- QA：GT A | baseline A（对） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=62° mirror=否 平移=(6.0,-1.6) RMSE=0.87；threeview: yaw=0° mirror=否 平移=(-0.3,-1.3) RMSE=2.29；threeview_3pass: yaw=-112° mirror=是(证据支持) 平移=(10.0,8.0) RMSE=1.17

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (5.0,1.0) | (4.3,1.6)✓ | (4.7,3.7)✗2.7 | (4.2,1.7)✓ |
| table | (2.0,7.0) | (3.1,5.6)✓ | (4.7,3.7)✗4.3 | (3.5,5.2)✗2.3 |
| tv | (7.0,3.0) | (6.6,3.8)✓ | (4.7,3.7)✗2.4 | (6.3,4.1)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (5.0,4.0) | - | (4.7,7.0)✗3.0 | (4.2,5.0)✓ |
| table | (2.0,2.0) | - | (4.7,3.0)✗2.8 | (3.5,3.0)✓ |
| tv | (7.0,4.0) | - | (4.7,5.0)✗2.5 | (6.3,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (1.0,4.0) | - | (3.7,7.0)✗4.0 | (1.7,5.0)✓ |
| table | (7.0,2.0) | - | (3.7,3.0)✗3.5 | (5.2,3.0)✗2.0 |
| tv | (3.0,4.0) | - | (3.7,5.0)✓ | (4.1,5.0)✓ |

- **baseline 问题**：lamp-table 距离画错（GT 6.7，模型 4.2）；lamp→table 方向错（GT SE，模型 S）；table-tv 距离画错（GT 6.4，模型 4.0）
- **threeview 问题**：lamp-table 距离画错（GT 6.7，模型 0.0）；lamp→table 方向错（GT SE，模型 E）；lamp-tv 距离画错（GT 2.8，模型 0.0）；lamp→tv 方向错（GT SW，模型 E）；table-tv 距离画错（GT 6.4，模型 0.0）；table→tv 方向错（GT NW，模型 E）；z 整体偏高（平均 +1.7 格）
- **threeview_3pass 问题**：lamp-table 距离画错（GT 6.7，模型 3.6）；lamp→table 方向错（GT SE，模型 S）；table-tv 距离画错（GT 6.4，模型 3.0）；table→tv 方向错（GT NW，模型 W）；z 整体偏高（平均 +1.0 格）

### 样本 28 `scene0144_00`（scannet · object_rel_direction_medium）

Q：If I am standing by the window and facing the lamp, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT C | baseline C（对） | threeview None（错） | threeview_3pass C（对）
- 对齐：baseline: yaw=123° mirror=否 平移=(11.1,4.1) RMSE=1.27；threeview: yaw=150° mirror=否 平移=(11.5,6.2) RMSE=1.38；threeview_3pass: yaw=153° mirror=否 平移=(11.1,6.0) RMSE=0.76

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (8.0,1.0) | (6.4,2.3)✗2.1 | (7.7,2.6)✓ | (7.9,1.9)✓ |
| lamp | (5.0,7.0) | (6.7,7.3)✓ | (4.7,4.3)✗2.7 | (5.3,5.5)✓ |
| window | (1.0,5.0) | (0.9,3.5)✓ | (1.6,6.1)✓ | (0.8,5.5)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (8.0,3.0) | - | (7.7,4.5)✓ | (7.9,4.0)✓ |
| lamp | (5.0,5.0) | - | (4.7,8.5)✗3.5 | (5.3,7.0)✗2.0 |
| window | (1.0,6.0) | - | (1.6,5.5)✓ | (0.8,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,3.0) | - | (2.6,4.5)✗2.2 | (1.9,4.0)✓ |
| lamp | (7.0,5.0) | - | (4.3,8.5)✗4.4 | (5.5,7.0)✗2.5 |
| window | (5.0,6.0) | - | (6.1,5.5)✓ | (5.5,5.0)✓ |

- **baseline 问题**：door-lamp 距离画错（GT 6.7，模型 5.0）；door→lamp 方向错（GT SE，模型 S）；door-window 距离画错（GT 8.1，模型 5.7）；door→window 方向错（GT SE，模型 E）；lamp-window 距离画错（GT 4.5，模型 7.0）
- **threeview 问题**：door-lamp 距离画错（GT 6.7，模型 3.5）；door-window 距离画错（GT 8.1，模型 7.0）；lamp→window 方向错（GT NE，模型 SE）；z 整体偏高（平均 +1.5 格）
- **threeview_3pass 问题**：door-lamp 距离画错（GT 6.7，模型 4.5）；lamp→window 方向错（GT NE，模型 E）；z 整体偏高（平均 +0.7 格）

### 样本 29 `scene0629_01`（scannet · object_rel_direction_medium）

Q：If I am standing by the bed and facing the chair, is the mirror to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT B | baseline C（错） | threeview B（对） | threeview_3pass B（对）
- 对齐：baseline: yaw=-15° mirror=是(未证实) 平移=(3.8,11.3) RMSE=0.30；threeview: yaw=-39° mirror=否 平移=(-0.0,3.8) RMSE=0.33；threeview_3pass: yaw=-43° mirror=否 平移=(-1.2,3.3) RMSE=0.36

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (7.0,4.0) | (7.0,4.2)✓ | (6.7,4.2)✓ | (6.5,4.1)✓ |
| chair | (6.0,7.0) | (5.6,6.6)✓ | (5.7,6.9)✓ | (6.5,7.4)✓ |
| mirror | (3.0,6.0) | (3.4,6.2)✓ | (3.6,6.0)✓ | (3.0,5.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (7.0,3.0) | - | (6.7,3.5)✓ | (6.5,2.8)✓ |
| chair | (6.0,2.0) | - | (5.7,3.0)✓ | (6.5,2.5)✓ |
| mirror | (3.0,4.0) | - | (3.6,6.5)✗2.6 | (3.0,5.5)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (4.0,3.0) | - | (4.2,3.5)✓ | (4.1,2.8)✓ |
| chair | (7.0,2.0) | - | (6.9,3.0)✓ | (7.4,2.5)✓ |
| mirror | (6.0,4.0) | - | (6.0,6.5)✗2.5 | (5.6,5.5)✓ |

- **baseline 问题**：bed→chair 方向错（GT S，模型 SE）
- **threeview 问题**：chair→mirror 方向错（GT E，模型 NE）；z 整体偏高（平均 +1.3 格）
- **threeview_3pass 问题**：chair→mirror 方向错（GT E，模型 NE）；z 整体偏高（平均 +0.6 格）

### 样本 30 `5ee7c22ba0`（scannetpp · object_rel_direction_medium）

Q：If I am standing by the refrigerator and facing the microwave, is the ceiling light to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT B | baseline A（错） | threeview A（错） | threeview_3pass B（对）
- 对齐：baseline: yaw=-127° mirror=是(证据支持) 平移=(8.5,3.4) RMSE=1.69；threeview: yaw=-100° mirror=是(证据支持) 平移=(11.3,6.7) RMSE=1.32；threeview_3pass: yaw=63° mirror=否 平移=(4.8,-2.9) RMSE=1.25

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (4.0,3.0) | (5.2,0.8)✗2.5 | (5.5,2.6)✓ | (6.2,2.0)✗2.4 |
| microwave | (3.0,1.0) | (2.7,4.0)✗3.0 | (2.3,3.0)✗2.1 | (1.7,2.0)✓ |
| refrigerator | (4.0,7.0) | (3.1,6.2)✓ | (3.2,5.3)✓ | (3.1,7.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (4.0,8.0) | - | (5.5,9.2)✓ | (6.2,9.0)✗2.4 |
| microwave | (3.0,3.0) | - | (2.3,5.8)✗2.9 | (1.7,5.0)✗2.4 |
| refrigerator | (4.0,2.0) | - | (3.2,4.5)✗2.6 | (3.1,4.0)✗2.2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| ceiling light | (3.0,8.0) | - | (2.6,9.2)✓ | (2.0,9.0)✓ |
| microwave | (1.0,3.0) | - | (3.0,5.8)✗3.5 | (2.0,5.0)✗2.3 |
| refrigerator | (7.0,2.0) | - | (5.3,4.5)✗3.0 | (7.0,4.0)✗2.0 |

- **baseline 问题**：ceiling light-microwave 距离画错（GT 2.2，模型 4.1）；ceiling light→microwave 方向错（GT NE，模型 SE）；ceiling light-refrigerator 距离画错（GT 4.0，模型 5.8）；microwave-refrigerator 距离画错（GT 6.1，模型 2.2）
- **threeview 问题**：ceiling light→microwave 方向错（GT NE，模型 E）；ceiling light→refrigerator 方向错（GT S，模型 SE）；microwave-refrigerator 距离画错（GT 6.1，模型 2.4）；z 整体偏高（平均 +2.2 格）
- **threeview_3pass 问题**：ceiling light-microwave 距离画错（GT 2.2，模型 4.5）；ceiling light→microwave 方向错（GT NE，模型 E）；ceiling light-refrigerator 距离画错（GT 4.0，模型 5.8）；ceiling light→refrigerator 方向错（GT S，模型 SE）；z 整体偏高（平均 +1.7 格）

### 样本 31 `45261121`（arkitscenes · object_rel_direction_medium）

Q：If I am standing by the table and facing the tv, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT A | baseline C（错） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=27° mirror=否 平移=(3.0,-4.7) RMSE=1.45；threeview: yaw=51° mirror=是(未证实) 平移=(-2.2,2.6) RMSE=0.60；threeview_3pass: yaw=-19° mirror=否 平移=(-1.2,0.6) RMSE=0.51

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (3.0,2.0) | (1.1,3.3)✗2.3 | (2.1,2.3)✓ | (2.2,1.5)✓ |
| table | (5.0,4.0) | (5.2,2.0)✓ | (5.4,3.2)✓ | (5.5,4.6)✓ |
| tv | (7.0,1.0) | (8.7,1.6)✓ | (7.5,1.5)✓ | (7.3,0.8)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (3.0,3.0) | - | (2.1,4.2)✓ | (2.2,3.0)✓ |
| table | (5.0,2.0) | - | (5.4,3.8)✓ | (5.5,3.0)✓ |
| tv | (7.0,7.0) | - | (7.5,6.5)✓ | (7.3,5.0)✗2.0 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stove | (2.0,3.0) | - | (2.3,4.2)✓ | (1.5,3.0)✓ |
| table | (4.0,2.0) | - | (3.2,3.8)✓ | (4.6,3.0)✓ |
| tv | (1.0,7.0) | - | (1.5,6.5)✓ | (0.8,5.0)✗2.0 |

- **baseline 问题**：stove-table 距离画错（GT 2.8，模型 4.2）；stove→table 方向错（GT SW，模型 W）；stove-tv 距离画错（GT 4.1，模型 7.8）；table→tv 方向错（GT NW，模型 W）
- **threeview 问题**：stove→table 方向错（GT SW，模型 W）；stove-tv 距离画错（GT 4.1，模型 5.4）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：stove-table 距离画错（GT 2.8，模型 4.5）

### 样本 32 `45b0dac5e3`（scannetpp · object_rel_direction_medium）

Q：If I am standing by the cup and facing the heater, is the toilet to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT C | baseline A（错） | threeview C（对） | threeview_3pass A（错）
- 对齐：baseline: yaw=159° mirror=是(证据支持) 平移=(7.1,-2.8) RMSE=0.72；threeview: yaw=-11° mirror=否 平移=(0.2,-0.6) RMSE=1.69；threeview_3pass: yaw=136° mirror=是(未证实) 平移=(4.5,-3.5) RMSE=1.02

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cup | (6.0,1.0) | (5.4,1.1)✓ | (4.5,3.1)✗2.6 | (5.8,2.1)✓ |
| heater | (0.0,5.0) | (1.4,4.7)✓ | (2.6,4.0)✗2.8 | (1.5,4.9)✓ |
| toilet | (7.0,6.0) | (6.2,6.1)✓ | (5.9,4.9)✓ | (5.7,5.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cup | (6.0,3.0) | - | (4.5,5.0)✗2.5 | (5.8,5.0)✗2.0 |
| heater | (0.0,3.0) | - | (2.6,6.0)✗4.0 | (1.5,4.0)✓ |
| toilet | (7.0,2.0) | - | (5.9,3.5)✓ | (5.7,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cup | (1.0,3.0) | - | (3.1,5.0)✗2.9 | (2.1,5.0)✗2.3 |
| heater | (5.0,3.0) | - | (4.0,6.0)✗3.2 | (4.9,4.0)✓ |
| toilet | (6.0,2.0) | - | (4.9,3.5)✓ | (5.0,3.0)✓ |

- **baseline 问题**：cup-heater 距离画错（GT 7.2，模型 5.4）；heater-toilet 距离画错（GT 7.1，模型 5.0）
- **threeview 问题**：cup-heater 距离画错（GT 7.2，模型 2.1）；cup-toilet 距离画错（GT 5.1，模型 2.2）；cup→toilet 方向错（GT S，模型 SW）；heater-toilet 距离画错（GT 7.1，模型 3.4）；z 整体偏高（平均 +2.2 格）
- **threeview_3pass 问题**：cup-heater 距离画错（GT 7.2，模型 5.1）；cup-toilet 距离画错（GT 5.1，模型 2.8）；heater-toilet 距离画错（GT 7.1，模型 4.2）；z 整体偏高（平均 +1.3 格）

### 样本 33 `scene0695_00`（scannet · object_rel_direction_medium）

Q：If I am standing by the lamp and facing the pillow, is the table to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT C | baseline C（对） | threeview C（对） | threeview_3pass C（对）
- 对齐：baseline: yaw=35° mirror=否 平移=(-0.1,-3.3) RMSE=1.63；threeview: yaw=79° mirror=否 平移=(6.7,-1.8) RMSE=1.84；threeview_3pass: yaw=99° mirror=否 平移=(7.4,1.3) RMSE=1.76

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (5.0,1.0) | (4.7,3.7)✗2.8 | (3.8,3.9)✗3.1 | (4.1,2.8)✗2.0 |
| pillow | (1.0,2.0) | (0.9,2.3)✓, (0.1,1.7)多, 多1 | (1.4,2.3)✓ | (2.0,3.5)✓, (1.8,4.5)多, 多1 |
| table | (3.0,7.0) | (4.2,4.6)✗2.7 | (3.8,3.9)✗3.2 | (2.9,3.7)✗3.3 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (5.0,4.0) | - | (3.8,5.0)✓ | (4.1,5.0)✓ |
| pillow | (1.0,4.0) | - | (1.4,4.0)✓ | (1.8,4.0)✓, (2.0,4.0)多, 多1 |
| table | (3.0,2.0) | - | (3.8,3.0)✓ | (2.9,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| lamp | (1.0,4.0) | - | (3.9,5.0)✗3.0 | (2.8,5.0)✗2.1 |
| pillow | (2.0,4.0) | - | (2.3,4.0)✓ | (3.5,4.0)✓, (4.5,4.0)多, 多1 |
| table | (7.0,2.0) | - | (3.9,3.0)✗3.3 | (3.7,3.0)✗3.5 |

- **baseline 问题**：多画 pillow ×1（GT 1，模型 2）；lamp→pillow 方向错（GT E，模型 NE）；lamp-table 距离画错（GT 6.3，模型 1.0）；lamp→table 方向错（GT S，模型 SE）；pillow-table 距离画错（GT 5.4，模型 4.0）；pillow→table 方向错（GT S，模型 SW）
- **threeview 问题**：lamp-pillow 距离画错（GT 4.1，模型 2.8）；lamp→pillow 方向错（GT E，模型 NE）；lamp-table 距离画错（GT 6.3，模型 0.0）；lamp→table 方向错（GT S，模型 E）；pillow-table 距离画错（GT 5.4，模型 2.8）；pillow→table 方向错（GT S，模型 SW）；z 整体偏高（平均 +0.7 格）
- **threeview_3pass 问题**：多画 pillow ×1（GT 1，模型 2）；lamp-pillow 距离画错（GT 4.1，模型 2.2）；lamp→pillow 方向错（GT E，模型 SE）；lamp-table 距离画错（GT 6.3，模型 1.4）；lamp→table 方向错（GT S，模型 SE）；pillow-table 距离画错（GT 5.4，模型 1.0）；pillow→table 方向错（GT S，模型 W）；z 整体偏高（平均 +0.7 格）

### 样本 34 `47334096`（arkitscenes · object_rel_direction_medium）

Q：If I am standing by the stool and facing the sofa, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT C | baseline A（错） | threeview B（错） | threeview_3pass C（对）
- 对齐：baseline: yaw=84° mirror=否 平移=(9.7,-2.2) RMSE=1.69；threeview: yaw=89° mirror=是(证据支持) 平移=(-0.4,-1.8) RMSE=0.40；threeview_3pass: yaw=66° mirror=否 平移=(7.9,-2.9) RMSE=1.32

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,4.0) | (2.1,1.7)✗3.0 | (3.8,3.3)✓ | (1.8,3.0)✗2.4 |
| stool | (5.0,1.0) | (5.3,3.3)✗2.4 | (4.9,1.6)✓ | (5.0,0.5)✓, (5.8,2.3)多, 多1 |
| stove | (7.0,6.0) | (8.6,6.0)✓ | (7.3,6.1)✓ | (8.4,5.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,2.0) | - | (3.8,3.8)✓ | (1.8,3.0)✗2.4 |
| stool | (5.0,2.0) | - | (4.9,2.8)✓ | (5.0,2.0)✓, (5.8,2.0)多, 多1 |
| stove | (7.0,5.0) | - | (7.3,4.5)✓ | (8.4,3.0)✗2.4 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,2.0) | - | (3.3,3.8)✓ | (3.0,3.0)✓ |
| stool | (1.0,2.0) | - | (1.6,2.8)✓ | (0.5,2.0)✓, (2.3,2.0)多, 多1 |
| stove | (6.0,5.0) | - | (6.1,4.5)✓ | (5.6,3.0)✗2.0 |

- **baseline 问题**：sofa→stool 方向错（GT N，模型 SW）；sofa-stove 距离画错（GT 3.6，模型 7.8）；stool-stove 距离画错（GT 5.4，模型 4.2）；stool→stove 方向错（GT S，模型 SW）
- **threeview 问题**：sofa-stool 距离画错（GT 3.2，模型 2.0）；sofa→stool 方向错（GT N，模型 NW）；stool→stove 方向错（GT S，模型 SW）；z 整体偏高（平均 +0.7 格）
- **threeview_3pass 问题**：多画 stool ×1（GT 1，模型 2）；sofa→stool 方向错（GT N，模型 NW）；sofa-stove 距离画错（GT 3.6，模型 7.1）；sofa→stove 方向错（GT SW，模型 W）；stool-stove 距离画错（GT 5.4，模型 4.1）；stool→stove 方向错（GT S，模型 SW）

### 样本 35 `42446103`（arkitscenes · object_rel_direction_medium）

Q：If I am standing by the stove and facing the tv, is the stool to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT A | baseline C（错） | threeview A（对） | threeview_3pass C（错）
- 对齐：baseline: yaw=-2° mirror=是(未证实) 平移=(-0.5,8.5) RMSE=0.94；threeview: yaw=-1° mirror=否 平移=(-0.7,-1.3) RMSE=0.74；threeview_3pass: yaw=-62° mirror=是(未证实) 平移=(6.9,11.2) RMSE=0.66

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (3.0,3.0) | (3.3,2.4)✓, (2.3,2.4)多, 多1 | (4.3,3.7)✓ | (2.1,3.1)✓ |
| stove | (3.0,7.0) | (4.4,6.3)✓ | (2.4,6.7)✓ | (3.9,6.2)✓ |
| tv | (8.0,2.0) | (7.3,3.3)✓ | (7.3,1.6)✓ | (8.0,2.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (3.0,1.0) | - | (4.3,3.0)✗2.4 | (2.1,2.0)✓ |
| stove | (3.0,4.0) | - | (2.4,4.0)✓ | (3.9,3.0)✓ |
| tv | (8.0,7.0) | - | (7.3,6.0)✓ | (8.0,5.0)✗2.0 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| stool | (3.0,1.0) | - | (3.7,3.0)✗2.1 | (3.1,2.0)✓ |
| stove | (7.0,4.0) | - | (6.7,4.0)✓ | (6.2,3.0)✓ |
| tv | (2.0,7.0) | - | (1.6,6.0)✓ | (2.7,5.0)✗2.1 |

- **baseline 问题**：多画 stool ×1（GT 1，模型 2）；stove-tv 距离画错（GT 7.1，模型 4.2）
- **threeview 问题**：stool→stove 方向错（GT S，模型 SE）；stool-tv 距离画错（GT 5.1，模型 3.6）；stool→tv 方向错（GT W，模型 NW）
- **threeview_3pass 问题**：stool→stove 方向错（GT S，模型 SW）；stove-tv 距离画错（GT 7.1，模型 5.4）；z 整体偏低（平均 -0.7 格）

### 样本 36 `42446049`（arkitscenes · object_rel_direction_medium）

Q：If I am standing by the washer and facing the refrigerator, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT C | baseline B（错） | threeview C（对） | threeview_3pass C（对）
- 对齐：baseline: yaw=14° mirror=是(未证实) 平移=(-1.6,9.3) RMSE=0.97；threeview: yaw=13° mirror=否 平移=(0.3,-0.4) RMSE=1.70；threeview_3pass: yaw=5° mirror=否 平移=(0.1,-0.7) RMSE=1.48

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (1.0,6.0) | (1.5,4.9)✓ | (1.8,4.5)✓ | (1.7,4.4)✓ |
| stove | (6.0,1.0) | (5.1,2.7)✓ | (4.9,4.2)✗3.4 | (4.7,3.7)✗2.9 |
| washer | (7.0,7.0) | (7.3,6.3)✓ | (7.3,5.2)✓ | (7.6,5.9)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (1.0,4.0) | - | (1.8,5.5)✓ | (1.7,5.0)✓ |
| stove | (6.0,4.0) | - | (4.9,3.5)✓ | (4.7,3.0)✓ |
| washer | (7.0,2.0) | - | (7.3,3.5)✓ | (7.6,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (6.0,4.0) | - | (4.5,5.5)✗2.1 | (4.4,5.0)✓ |
| stove | (1.0,4.0) | - | (4.2,3.5)✗3.3 | (3.7,3.0)✗2.9 |
| washer | (7.0,2.0) | - | (5.2,3.5)✗2.3 | (5.9,3.0)✓ |

- **baseline 问题**：refrigerator-stove 距离画错（GT 7.1，模型 4.2）；stove-washer 距离画错（GT 6.1，模型 4.2）；stove→washer 方向错（GT S，模型 SW）
- **threeview 问题**：refrigerator-stove 距离画错（GT 7.1，模型 3.2）；refrigerator→stove 方向错（GT NW，模型 W）；stove-washer 距离画错（GT 6.1，模型 2.5）；stove→washer 方向错（GT S，模型 SW）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：refrigerator-stove 距离画错（GT 7.1，模型 3.2）；refrigerator→stove 方向错（GT NW，模型 W）；stove-washer 距离画错（GT 6.1，模型 3.6）；stove→washer 方向错（GT S，模型 SW）

### 样本 37 `scene0144_00`（scannet · object_rel_direction_medium）

Q：If I am standing by the lamp and facing the printer, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT C | baseline C（对） | threeview C（对） | threeview_3pass C（对）
- 对齐：baseline: yaw=166° mirror=否 平移=(9.9,6.9) RMSE=1.05；threeview: yaw=-168° mirror=否 平移=(6.8,10.0) RMSE=1.33；threeview_3pass: yaw=142° mirror=否 平移=(11.9,3.8) RMSE=0.94

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (8.0,1.0) | (7.8,2.3)✓ | (7.3,1.4)✓ | (8.0,0.5)✓ |
| lamp | (5.0,7.0) | (5.3,5.0)✗2.1 | (3.9,5.1)✗2.2 | (3.7,6.4)✓ |
| printer | (2.0,3.0), (2.0,3.0) | (1.9,3.7)✓, 漏1 | (3.7,4.5)✗2.3, 漏1 | (3.3,4.2)✓, 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (8.0,3.0) | - | (7.3,5.0)✗2.1 | (8.0,5.0)✗2.0 |
| lamp | (5.0,5.0) | - | (3.9,5.2)✓ | (3.7,5.0)✓ |
| printer | (2.0,4.0), (2.0,4.0) | - | (3.7,3.8)✓, 漏1 | (3.3,4.0)✓, 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,3.0) | - | (1.4,5.0)✗2.0 | (0.5,5.0)✗2.1 |
| lamp | (7.0,5.0) | - | (5.1,5.2)✓ | (6.4,5.0)✓ |
| printer | (3.0,4.0), (3.0,4.0) | - | (4.5,3.8)✓, 漏1 | (4.2,4.0)✓, 漏1 |

- **baseline 问题**：漏画 printer ×1（GT 2，模型 1）；door-lamp 距离画错（GT 6.7，模型 3.6）；lamp-printer 距离画错（GT 5.0，模型 3.6）；lamp→printer 方向错（GT NE，模型 E）
- **threeview 问题**：漏画 printer ×1（GT 2，模型 1）；door-lamp 距离画错（GT 6.7，模型 5.0）；door-printer 距离画错（GT 6.3，模型 4.7）；door→printer 方向错（GT E，模型 SE）；lamp-printer 距离画错（GT 5.0，模型 0.7）；lamp→printer 方向错（GT NE，模型 N）；z 整体偏高（平均 +0.7 格）
- **threeview_3pass 问题**：漏画 printer ×1（GT 2，模型 1）；door→printer 方向错（GT E，模型 SE）；lamp-printer 距离画错（GT 5.0，模型 2.2）；lamp→printer 方向错（GT NE，模型 N）；z 整体偏高（平均 +0.7 格）

### 样本 38 `f9f95681fd`（scannetpp · object_rel_direction_medium）

Q：If I am standing by the door and facing the kettle, is the microwave to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees in order to face it.

- QA：GT C | baseline A（错） | threeview A（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=-20° mirror=否 平移=(-1.0,-0.1) RMSE=1.65；threeview: yaw=56° mirror=否 平移=(5.5,-2.9) RMSE=1.77；threeview_3pass: yaw=50° mirror=否 平移=(5.7,-2.4) RMSE=1.72

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,3.0) | (1.7,4.3)✓ | (-0.7,3.1)✓ | (0.3,3.5)✓ |
| kettle | (7.0,3.0) | (4.8,4.2)✗2.5 | (5.8,4.7)✗2.1 | (5.2,4.6)✗2.4 |
| microwave | (2.0,6.0) | (3.5,3.6)✗2.9 | (4.9,4.2)✗3.4 | (4.5,3.9)✗3.3 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (1.0,4.0) | - | (-0.7,5.0)✓ | (0.3,5.0)✓ |
| kettle | (7.0,3.0) | - | (5.8,4.0)✓ | (5.2,4.0)✗2.1 |
| microwave | (2.0,3.0) | - | (4.9,4.5)✗3.2 | (4.5,4.0)✗2.7 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (3.0,4.0) | - | (3.1,5.0)✓ | (3.5,5.0)✓ |
| kettle | (3.0,3.0) | - | (4.7,4.0)✗2.0 | (4.6,4.0)✓ |
| microwave | (6.0,3.0) | - | (4.2,4.5)✗2.4 | (3.9,4.0)✗2.4 |

- **baseline 问题**：door-kettle 距离画错（GT 6.0，模型 3.2）；door-microwave 距离画错（GT 3.2，模型 2.0）；door→microwave 方向错（GT S，模型 W）；kettle-microwave 距离画错（GT 5.8，模型 1.4）；kettle→microwave 方向错（GT SE，模型 NE）
- **threeview 问题**：door-microwave 距离画错（GT 3.2，模型 5.7）；door→microwave 方向错（GT S，模型 W）；kettle-microwave 距离画错（GT 5.8，模型 1.1）；kettle→microwave 方向错（GT SE，模型 NE）；z 整体偏高（平均 +1.2 格）
- **threeview_3pass 问题**：door-microwave 距离画错（GT 3.2，模型 4.2）；door→microwave 方向错（GT S，模型 W）；kettle-microwave 距离画错（GT 5.8，模型 1.0）；kettle→microwave 方向错（GT SE，模型 NE）；z 整体偏高（平均 +1.0 格）

### 样本 39 `47331668`（arkitscenes · object_rel_direction_hard）

Q：If I am standing by the tv and facing the bed, is the chair to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT A | baseline C（错） | threeview A（对） | threeview_3pass C（错）
- 对齐：baseline: yaw=15° mirror=是(证据支持) 平移=(-2.1,8.0) RMSE=1.38；threeview: yaw=60° mirror=否 平移=(7.2,-2.3) RMSE=0.43；threeview_3pass: yaw=20° mirror=是(证据支持) 平移=(-2.3,7.6) RMSE=1.08

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,4.0) | (4.1,4.5)✗2.0 | (5.8,4.2)✓ | (4.1,4.6)✗2.0 |
| chair | (2.0,3.0) | (2.9,1.1)✗2.1 | (1.9,3.5)✓ | (2.9,2.0)✓ |
| tv | (2.0,7.0) | (3.0,8.4)✓ | (2.3,6.2)✓ | (3.1,7.4)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,2.0) | - | (5.8,3.5)✓ | (4.1,3.0)✗2.2 |
| chair | (2.0,3.0) | - | (1.9,4.0)✓ | (2.9,3.0)✓ |
| tv | (2.0,6.0) | - | (2.3,6.0)✓ | (3.1,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (4.0,2.0) | - | (4.2,3.5)✓ | (4.6,3.0)✓ |
| chair | (3.0,3.0) | - | (3.5,4.0)✓ | (2.0,3.0)✓ |
| tv | (7.0,6.0) | - | (6.2,6.0)✓ | (7.4,5.0)✓ |

- **baseline 问题**：bed→chair 方向错（GT E，模型 N）；bed→tv 方向错（GT SE，模型 S）；chair-tv 距离画错（GT 4.0，模型 7.3）
- **threeview 问题**：bed-tv 距离画错（GT 5.0，模型 4.0）；chair-tv 距离画错（GT 4.0，模型 2.7）；z 整体偏高（平均 +0.8 格）
- **threeview_3pass 问题**：bed-chair 距离画错（GT 4.1，模型 2.8）；bed→chair 方向错（GT E，模型 NE）；bed-tv 距离画错（GT 5.0，模型 3.0）；bed→tv 方向错（GT SE，模型 S）；chair-tv 距离画错（GT 4.0，模型 5.4）

### 样本 40 `42897528`（arkitscenes · object_rel_direction_hard）

Q：If I am standing by the washer and facing the refrigerator, is the sofa to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT D | baseline D（对） | threeview D（对） | threeview_3pass B（错）
- 对齐：baseline: yaw=153° mirror=否 平移=(9.4,6.6) RMSE=2.25；threeview: yaw=65° mirror=否 平移=(6.3,-3.1) RMSE=1.44；threeview_3pass: yaw=71° mirror=是(未证实) 平移=(-3.1,1.0) RMSE=1.37

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (2.0,4.0) | (4.0,0.3)✗4.2 | (-0.0,2.1)✗2.8 | (0.4,1.9)✗2.6 |
| sofa | (5.0,2.0) | (2.7,4.3)✗3.3 | (5.5,3.4)✓ | (5.2,3.5)✓ |
| washer | (1.0,7.0) | (1.3,8.4)✓ | (2.5,7.5)✓ | (2.4,7.6)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (2.0,4.0) | - | (-0.0,6.0)✗2.9 | (0.4,5.0)✓ |
| sofa | (5.0,2.0) | - | (5.5,4.0)✗2.1 | (5.2,2.0)✓ |
| washer | (1.0,2.0) | - | (2.5,4.5)✗2.9 | (2.4,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (4.0,4.0) | - | (2.1,6.0)✗2.8 | (1.9,5.0)✗2.3 |
| sofa | (2.0,2.0) | - | (3.4,4.0)✗2.4 | (3.5,2.0)✓ |
| washer | (7.0,2.0) | - | (7.5,4.5)✗2.6 | (7.6,2.0)✓ |

- **baseline 问题**：refrigerator→sofa 方向错（GT NW，模型 S）；refrigerator-washer 距离画错（GT 3.2，模型 8.5）；sofa-washer 距离画错（GT 6.4，模型 4.2）；sofa→washer 方向错（GT SE，模型 S）
- **threeview 问题**：refrigerator-sofa 距离画错（GT 3.6，模型 5.7）；refrigerator→sofa 方向错（GT NW，模型 W）；refrigerator-washer 距离画错（GT 3.2，模型 6.0）；refrigerator→washer 方向错（GT S，模型 SW）；sofa-washer 距离画错（GT 6.4，模型 5.1）；z 整体偏高（平均 +2.2 格）
- **threeview_3pass 问题**：refrigerator-sofa 距离画错（GT 3.6，模型 5.0）；refrigerator→sofa 方向错（GT NW，模型 W）；refrigerator-washer 距离画错（GT 3.2，模型 6.0）；sofa-washer 距离画错（GT 6.4，模型 5.0）

### 样本 41 `scene0307_02`（scannet · object_rel_direction_hard）

Q：If I am standing by the chair and facing the refrigerator, is the washing machine to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT D | baseline A（错） | threeview C（错） | threeview_3pass D（对）
- 对齐：baseline: yaw=121° mirror=否 平移=(11.7,4.6) RMSE=0.81；threeview: yaw=-2° mirror=是(证据支持) 平移=(0.4,11.9) RMSE=1.60；threeview_3pass: yaw=160° mirror=否 平移=(9.4,8.1) RMSE=1.09

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,6.0) | (4.9,6.3)✓, (5.4,5.5)多, 多1 | (5.7,7.2)✗2.1 | (4.0,4.8)✓, (2.7,4.2)多, 多1 |
| refrigerator | (4.0,2.0) | (3.9,2.2)✓ | (2.6,3.4)✓ | (4.8,1.3)✓ |
| washing machine | (2.0,7.0) | (0.8,7.3)✓ | (1.6,4.4)✗2.6 | (1.2,9.0)✗2.1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (4.0,2.0) | - | (5.7,3.5)✗2.3 | (4.0,3.0)✓, (2.7,3.0)多, 多1 |
| refrigerator | (4.0,3.0) | - | (2.6,5.5)✗2.9 | (4.8,5.0)✗2.2 |
| washing machine | (2.0,2.0) | - | (1.6,4.0)✗2.0 | (1.2,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| chair | (6.0,2.0) | - | (7.2,3.5)✓ | (4.8,3.0)✓, (4.2,3.0)多, 多1 |
| refrigerator | (2.0,3.0) | - | (3.4,5.5)✗2.8 | (1.3,5.0)✗2.1 |
| washing machine | (7.0,2.0) | - | (4.4,4.0)✗3.3 | (9.0,3.0)✗2.2 |

- **baseline 问题**：多画 chair ×1（GT 1，模型 2）；chair-washing machine 距离画错（GT 2.2，模型 4.2）；chair→washing machine 方向错（GT SE，模型 E）；refrigerator→washing machine 方向错（GT S，模型 SE）
- **threeview 问题**：chair-refrigerator 距离画错（GT 4.0，模型 5.0）；chair→refrigerator 方向错（GT N，模型 NE）；chair-washing machine 距离画错（GT 2.2，模型 5.0）；chair→washing machine 方向错（GT SE，模型 NE）；refrigerator-washing machine 距离画错（GT 5.4，模型 1.4）；refrigerator→washing machine 方向错（GT S，模型 SE）；z 整体偏高（平均 +2.0 格）
- **threeview_3pass 问题**：多画 chair ×1（GT 1，模型 2）；chair→refrigerator 方向错（GT N，模型 NW）；chair-washing machine 距离画错（GT 2.2，模型 5.0）；refrigerator-washing machine 距离画错（GT 5.4，模型 8.5）；refrigerator→washing machine 方向错（GT S，模型 SE）；z 整体偏高（平均 +1.3 格）

### 样本 42 `scene0164_02`（scannet · object_rel_direction_hard）

Q：If I am standing by the towel and facing the microwave, is the backpack to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT D | baseline C（错） | threeview B（错） | threeview_3pass C（错）
- 对齐：baseline: yaw=168° mirror=否 平移=(10.1,9.1) RMSE=1.11；threeview: yaw=-35° mirror=否 平移=(-1.9,1.7) RMSE=0.62；threeview_3pass: yaw=-107° mirror=否 平移=(2.4,10.5) RMSE=1.13

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (6.0,1.0) | (6.5,1.7)✓ | (6.0,1.6)✓ | (6.7,0.8)✓ |
| microwave | (5.0,7.0) | (6.3,5.8)✓ | (5.3,5.8)✓ | (6.2,6.1)✓ |
| towel | (5.0,5.0) | (3.2,5.5)✓ | (4.7,5.6)✓ | (3.1,6.1)✗2.2 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (6.0,2.0) | - | (6.0,2.5)✓ | (6.7,2.0)✓ |
| microwave | (5.0,5.0) | - | (5.3,5.5)✓ | (6.2,5.0)✓ |
| towel | (5.0,3.0) | - | (4.7,6.5)✗3.5 | (3.1,4.0)✗2.2 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| backpack | (1.0,2.0) | - | (1.6,2.5)✓ | (0.8,2.0)✓ |
| microwave | (7.0,5.0) | - | (5.8,5.5)✓ | (6.1,5.0)✓ |
| towel | (5.0,3.0) | - | (5.6,6.5)✗3.5 | (6.1,4.0)✓ |

- **baseline 问题**：backpack-microwave 距离画错（GT 6.1，模型 4.1）；backpack→towel 方向错（GT S，模型 SE）；microwave-towel 距离画错（GT 2.0，模型 3.2）；microwave→towel 方向错（GT N，模型 E）
- **threeview 问题**：backpack-microwave 距离画错（GT 6.1，模型 4.2）；microwave-towel 距离画错（GT 2.0，模型 0.6）；microwave→towel 方向错（GT N，模型 NE）；z 整体偏高（平均 +1.5 格）
- **threeview_3pass 问题**：backpack-towel 距离画错（GT 4.1，模型 6.4）；backpack→towel 方向错（GT S，模型 SE）；microwave-towel 距离画错（GT 2.0，模型 3.2）；microwave→towel 方向错（GT N，模型 E）

### 样本 43 `47331668`（arkitscenes · object_rel_direction_hard）

Q：If I am standing by the bed and facing the tv, is the chair to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT B | baseline D（错） | threeview B（对） | threeview_3pass D（错）
- 对齐：baseline: yaw=15° mirror=是(证据支持) 平移=(-2.1,8.0) RMSE=1.38；threeview: yaw=53° mirror=否 平移=(6.0,-2.6) RMSE=0.37；threeview_3pass: yaw=15° mirror=是(证据支持) 平移=(-2.1,8.0) RMSE=1.38

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,4.0) | (4.1,4.5)✗2.0 | (5.4,4.1)✓ | (4.1,4.5)✗2.0 |
| chair | (2.0,3.0) | (2.9,1.1)✗2.1 | (2.3,3.3)✓ | (2.9,1.1)✗2.1 |
| tv | (2.0,7.0) | (3.0,8.4)✓ | (2.3,6.5)✓ | (3.0,8.4)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (6.0,2.0) | - | (5.4,3.5)✓ | (4.1,3.0)✗2.2 |
| chair | (2.0,3.0) | - | (2.3,3.0)✓ | (2.9,3.0)✓ |
| tv | (2.0,6.0) | - | (2.3,5.5)✓ | (3.0,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| bed | (4.0,2.0) | - | (4.1,3.5)✓ | (4.5,3.0)✓ |
| chair | (3.0,3.0) | - | (3.3,3.0)✓ | (1.1,3.0)✓ |
| tv | (7.0,6.0) | - | (6.5,5.5)✓ | (8.4,5.0)✓ |

- **baseline 问题**：bed→chair 方向错（GT E，模型 N）；bed→tv 方向错（GT SE，模型 S）；chair-tv 距离画错（GT 4.0，模型 7.3）
- **threeview_3pass 问题**：bed→chair 方向错（GT E，模型 N）；bed→tv 方向错（GT SE，模型 S）；chair-tv 距离画错（GT 4.0，模型 7.3）

### 样本 44 `c50d2d1d42`（scannetpp · object_rel_direction_hard）

Q：If I am standing by the telephone and facing the door, is the whiteboard to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT C | baseline D（错） | threeview C（对） | threeview_3pass D（错）
- 对齐：baseline: yaw=2° mirror=是(未证实) 平移=(-0.2,8.9) RMSE=0.81；threeview: yaw=49° mirror=否 平移=(7.1,-3.1) RMSE=0.83；threeview_3pass: yaw=22° mirror=是(证据支持) 平移=(-0.9,7.4) RMSE=1.07

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (0.0,3.0) | (1.0,3.9)✓ | (1.2,3.9)✓ | (2.0,3.1)✓ |
| telephone | (7.0,3.0) | (7.0,3.1)✓ | (6.9,2.9)✓ | (5.5,2.4)✓ |
| whiteboard | (5.0,7.0) | (3.9,6.0)✓ | (3.9,6.2)✓ | (4.5,7.4)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (0.0,3.0) | - | (1.2,5.0)✗2.3 | (2.0,5.0)✗2.8 |
| telephone | (7.0,3.0) | - | (6.9,3.5)✓ | (5.5,4.0)✓ |
| whiteboard | (5.0,4.0) | - | (3.9,6.0)✗2.3 | (4.5,5.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (3.0,3.0) | - | (3.9,5.0)✗2.2 | (3.1,5.0)✗2.0 |
| telephone | (3.0,3.0) | - | (2.9,3.5)✓ | (2.4,4.0)✓ |
| whiteboard | (7.0,4.0) | - | (6.2,6.0)✗2.1 | (7.4,5.0)✓ |

- **baseline 问题**：door-whiteboard 距离画错（GT 6.4，模型 3.6）
- **threeview 问题**：door-telephone 距离画错（GT 7.0，模型 5.8）；door-whiteboard 距离画错（GT 6.4，模型 3.5）；z 整体偏高（平均 +1.5 格）
- **threeview_3pass 问题**：door-telephone 距离画错（GT 7.0，模型 3.6）；door-whiteboard 距离画错（GT 6.4，模型 5.0）；telephone→whiteboard 方向错（GT SE，模型 S）；z 整体偏高（平均 +1.3 格）

### 样本 45 `47430468`（arkitscenes · object_rel_direction_hard）

Q：If I am standing by the stove and facing the stool, is the refrigerator to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT D | baseline B（错） | threeview C（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=80° mirror=是(证据支持) 平移=(-4.2,3.0) RMSE=0.85；threeview: yaw=97° mirror=否 平移=(9.3,2.2) RMSE=0.98；threeview_3pass: 2点 yaw=-37° mirror=否 平移=(-5.0,2.4) RMSE=0.75

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (2.0,4.0) | (0.9,3.1)✓ | (0.5,3.6)✓ | (1.2,3.2)✓ |
| stool | (3.0,5.0) | (4.4,5.6)✓ | (4.3,6.1)✓ | (3.7,5.8)✓ |
| stove | (1.0,7.0) | (0.6,7.3)✓ | (1.2,6.2)✓ | 漏1 |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (2.0,4.0) | - | (0.5,5.5)✗2.1 | (1.2,4.5)✓ |
| stool | (3.0,1.0) | - | (4.3,2.5)✓ | (3.7,2.0)✓ |
| stove | (1.0,3.0) | - | (1.2,4.0)✓ | 漏1 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (4.0,4.0) | - | (3.6,5.5)✓ | (3.2,4.5)✓ |
| stool | (5.0,1.0) | - | (6.1,2.5)✓ | (5.8,2.0)✓ |
| stove | (7.0,3.0) | - | (6.2,4.0)✓ | 漏1 |

- **baseline 问题**：refrigerator-stool 距离画错（GT 1.4，模型 4.2）；stool-stove 距离画错（GT 2.8，模型 4.1）
- **threeview 问题**：refrigerator-stool 距离画错（GT 1.4，模型 4.5）；stool→stove 方向错（GT SE，模型 E）；z 整体偏高（平均 +1.3 格）
- **threeview_3pass 问题**：漏画 stove ×1（GT 1，模型 0）；refrigerator-stool 距离画错（GT 1.4，模型 3.5）；z 整体偏高（平均 +0.8 格）

### 样本 46 `47334380`（arkitscenes · object_rel_direction_hard）

Q：If I am standing by the refrigerator and facing the stove, is the table to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT D | baseline D（对） | threeview D（对） | threeview_3pass D（对）
- 对齐：baseline: yaw=-56° mirror=否 平移=(-3.4,4.5) RMSE=0.57；threeview: yaw=-32° mirror=否 平移=(-2.6,2.2) RMSE=1.22；threeview_3pass: yaw=22° mirror=否 平移=(1.9,-2.9) RMSE=0.99

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (1.0,6.0) | (1.0,5.1)✓ | (0.5,4.4)✓ | (0.7,5.2)✓ |
| stove | (2.0,1.0) | (1.9,2.0)✓ | (2.2,3.3)✗2.3 | (2.8,2.8)✓ |
| table | (6.0,5.0) | (6.0,4.9)✓ | (6.3,4.3)✓ | (5.5,4.0)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (1.0,4.0) | - | (0.5,6.0)✗2.1 | (0.7,5.0)✓ |
| stove | (2.0,4.0) | - | (2.2,4.5)✓ | (2.8,3.0)✓ |
| table | (6.0,2.0) | - | (6.3,3.5)✓ | (5.5,3.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| refrigerator | (6.0,4.0) | - | (4.4,6.0)✗2.6 | (5.2,5.0)✓ |
| stove | (1.0,4.0) | - | (3.3,4.5)✗2.4 | (2.8,3.0)✗2.1 |
| table | (5.0,2.0) | - | (4.3,3.5)✓ | (4.0,3.0)✓ |

- **baseline 问题**：refrigerator-stove 距离画错（GT 5.1，模型 3.2）
- **threeview 问题**：refrigerator-stove 距离画错（GT 5.1，模型 2.0）；refrigerator→stove 方向错（GT N，模型 NW）；stove-table 距离画错（GT 5.7，模型 4.2）；stove→table 方向错（GT SW，模型 W）；z 整体偏高（平均 +1.3 格）
- **threeview_3pass 问题**：refrigerator-stove 距离画错（GT 5.1，模型 3.2）；refrigerator→stove 方向错（GT N，模型 NW）；stove-table 距离画错（GT 5.7，模型 3.0）；stove→table 方向错（GT SW，模型 W）

### 样本 47 `7b6477cb95`（scannetpp · object_rel_direction_hard）

Q：If I am standing by the telephone and facing the cup, is the trash can to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT A | baseline D（错） | threeview D（错） | threeview_3pass D（错）
- 对齐：baseline: yaw=21° mirror=否 平移=(3.5,-2.1) RMSE=0.56；threeview: yaw=-98° mirror=否 平移=(1.1,8.7) RMSE=1.27；threeview_3pass: yaw=11° mirror=否 平移=(1.7,-1.4) RMSE=0.35

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cup | (5.0,3.0) | (4.9,2.7)✓ | (4.6,3.4)✓ | (5.1,2.4)✓ |
| telephone | (6.0,3.0) | (5.5,3.9)✓ | (5.0,4.6)✓ | (5.8,3.5)✓ |
| trash can | (3.0,7.0) | (3.5,6.4)✓ | (4.4,5.0)✗2.4 | (3.1,7.1)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cup | (5.0,2.0) | - | (4.6,5.2)✗3.2 | (5.1,4.0)✗2.0 |
| telephone | (6.0,2.0) | - | (5.0,5.5)✗3.6 | (5.8,4.0)✗2.0 |
| trash can | (3.0,1.0) | - | (4.4,2.5)✗2.0 | (3.1,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| cup | (3.0,2.0) | - | (3.4,5.2)✗3.2 | (2.4,4.0)✗2.1 |
| telephone | (3.0,2.0) | - | (4.6,5.5)✗3.9 | (3.5,4.0)✗2.1 |
| trash can | (7.0,1.0) | - | (5.0,2.5)✗2.5 | (7.1,2.0)✓ |

- **baseline 问题**：cup→telephone 方向错（GT W，模型 SW）；cup→trash can 方向错（GT SE，模型 S）；telephone-trash can 距离画错（GT 5.0，模型 3.2）
- **threeview 问题**：cup→telephone 方向错（GT W，模型 S）；cup-trash can 距离画错（GT 4.5，模型 1.6）；cup→trash can 方向错（GT SE，模型 S）；telephone-trash can 距离画错（GT 5.0，模型 0.8）；z 整体偏高（平均 +2.7 格）
- **threeview_3pass 问题**：cup→telephone 方向错（GT W，模型 SW）；z 整体偏高（平均 +1.7 格）

### 样本 48 `47334096`（arkitscenes · object_rel_direction_hard）

Q：If I am standing by the stool and facing the tv, is the sofa to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT C | baseline A（错） | threeview B（错） | threeview_3pass A（错）
- 对齐：baseline: yaw=92° mirror=是(未证实) 平移=(-1.2,-0.8) RMSE=1.10；threeview: yaw=90° mirror=否 平移=(9.3,-1.2) RMSE=1.25；threeview_3pass: yaw=-135° mirror=否 平移=(3.6,9.2) RMSE=1.51

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,4.0) | (5.7,3.4)✓ | (5.8,3.8)✓ | (5.0,2.2)✗2.1 |
| stool | (5.0,1.0) | (3.7,2.3)✓ | (3.3,2.3)✗2.1 | (3.6,3.6)✗2.9 |
| tv | (1.0,5.0) | (0.6,4.3)✓ | (0.8,3.8)✓ | (1.4,4.3)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,2.0) | - | (5.8,4.5)✗3.1 | (5.0,2.0)✓ |
| stool | (5.0,2.0) | - | (3.3,3.0)✓ | (3.6,1.0)✓ |
| tv | (1.0,6.0) | - | (0.8,6.5)✓ | (1.4,4.0)✗2.0 |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| sofa | (4.0,2.0) | - | (3.8,4.5)✗2.5 | (2.2,2.0)✓ |
| stool | (1.0,2.0) | - | (2.3,3.0)✓ | (3.6,1.0)✗2.8 |
| tv | (5.0,6.0) | - | (3.8,6.5)✓ | (4.3,4.0)✗2.1 |

- **baseline 问题**：sofa→stool 方向错（GT N，模型 NE）；sofa-tv 距离画错（GT 3.2，模型 5.1）；stool-tv 距离画错（GT 5.7，模型 3.6）
- **threeview 问题**：sofa→stool 方向错（GT N，模型 NE）；sofa-tv 距离画错（GT 3.2，模型 5.0）；stool-tv 距离画错（GT 5.7，模型 2.9）；z 整体偏高（平均 +1.3 格）
- **threeview_3pass 问题**：sofa-stool 距离画错（GT 3.2，模型 2.0）；sofa→stool 方向错（GT N，模型 SE）；sofa→tv 方向错（GT E，模型 SE）；stool-tv 距离画错（GT 5.7，模型 2.2）；stool→tv 方向错（GT SE，模型 E）；z 整体偏低（平均 -1.0 格）

### 样本 49 `47331970`（arkitscenes · object_rel_direction_hard）

Q：If I am standing by the dishwasher and facing the refrigerator, is the table to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT A | baseline C（错） | threeview B（错） | threeview_3pass B（错）
- 对齐：baseline: yaw=74° mirror=否 平移=(5.3,-2.8) RMSE=0.87；threeview: yaw=135° mirror=是(证据支持) 平移=(2.0,-2.5) RMSE=1.01；threeview_3pass: yaw=163° mirror=否 平移=(7.4,6.6) RMSE=1.09

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| dishwasher | (1.0,3.0) | (1.6,2.4)✓ | (1.3,1.7)✓ | (2.1,3.0)✓ |
| refrigerator | (3.0,1.0) | (3.0,-0.0)✓ | (2.7,0.3)✓ | (3.1,-0.5)✓ |
| table | (2.0,4.0) | (1.5,5.6)✓ | (2.0,6.0)✓ | (0.8,5.5)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| dishwasher | (1.0,2.0) | - | (1.3,3.5)✓ | (2.1,2.0)✓ |
| refrigerator | (3.0,4.0) | - | (2.7,5.5)✓ | (3.1,5.0)✓ |
| table | (2.0,2.0) | - | (2.0,3.0)✓ | (0.8,2.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| dishwasher | (3.0,2.0) | - | (1.7,3.5)✓ | (3.0,2.0)✓ |
| refrigerator | (1.0,4.0) | - | (0.3,5.5)✓ | (-0.5,5.0)✓ |
| table | (4.0,2.0) | - | (6.0,3.0)✗2.2 | (5.5,2.0)✓ |

- **baseline 问题**：dishwasher-table 距离画错（GT 1.4，模型 3.2）；dishwasher→table 方向错（GT SW，模型 S）；refrigerator-table 距离画错（GT 3.2，模型 5.8）
- **threeview 问题**：dishwasher-table 距离画错（GT 1.4，模型 4.3）；dishwasher→table 方向错（GT SW，模型 S）；refrigerator-table 距离画错（GT 3.2，模型 5.7）；z 整体偏高（平均 +1.3 格）
- **threeview_3pass 问题**：dishwasher→refrigerator 方向错（GT NW，模型 N）；dishwasher-table 距离画错（GT 1.4，模型 2.8）；dishwasher→table 方向错（GT SW，模型 SE）；refrigerator-table 距离画错（GT 3.2，模型 6.4）

### 样本 50 `scene0664_02`（scannet · object_rel_direction_hard）

Q：If I am standing by the mirror and facing the door, is the trash bin to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a Cartesian plane (if I am standing at the origin and facing along the positive y-axis).

- QA：GT D | baseline D（对） | threeview C（错） | threeview_3pass D（对）
- 对齐：baseline: yaw=-146° mirror=否 平移=(2.4,10.6) RMSE=0.76；threeview: yaw=175° mirror=是(证据支持) 平移=(5.8,-0.4) RMSE=1.43；threeview_3pass: yaw=-151° mirror=否 平移=(2.9,10.2) RMSE=1.17

**TOP 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (4.0,7.0) | (4.4,5.9)✓ | (5.0,7.7)✓ | (4.4,5.3)✓ |
| mirror | (1.0,5.0) | (-0.0,5.3)✓ | (1.0,2.5)✗2.5 | (-0.5,6.0)✓ |
| trash bin | (3.0,1.0) | (3.6,1.8)✓ | (2.0,2.9)✗2.1 | (4.1,1.7)✓ |

**FRONT 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (4.0,4.0) | - | (5.0,5.0)✓ | (4.4,5.0)✓ |
| mirror | (1.0,4.0) | - | (1.0,6.5)✗2.5 | (-0.5,6.0)✗2.5 |
| trash bin | (3.0,1.0) | - | (2.0,2.0)✓ | (4.1,1.0)✓ |

**SIDE 视图**

| 类别 | GT | baseline | threeview | threeview_3pass |
|---|---|---|---|---|
| door | (7.0,4.0) | - | (7.7,5.0)✓ | (5.3,5.0)✓ |
| mirror | (5.0,4.0) | - | (2.5,6.5)✗3.6 | (6.0,6.0)✗2.2 |
| trash bin | (1.0,1.0) | - | (2.9,2.0)✗2.1 | (1.7,1.0)✓ |

- **baseline 问题**：door→mirror 方向错（GT NE，模型 E）；door-trash bin 距离画错（GT 6.1，模型 4.2）
- **threeview 问题**：door-mirror 距离画错（GT 3.6，模型 6.5）；door→trash bin 方向错（GT N，模型 NE）；mirror-trash bin 距离画错（GT 4.5，模型 1.1）；mirror→trash bin 方向错（GT NW，模型 W）；z 整体偏高（平均 +1.5 格）
- **threeview_3pass 问题**：door-mirror 距离画错（GT 3.6，模型 5.0）；door→mirror 方向错（GT NE，模型 E）；door-trash bin 距离画错（GT 6.1，模型 3.6）；mirror-trash bin 距离画错（GT 4.5，模型 6.3）；z 整体偏高（平均 +1.0 格）
