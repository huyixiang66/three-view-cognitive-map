# 三种认知图 vs GT — 逐样本对照

> 2026-08-06 · 50 样本；TIS baseline 只产出 TOP，三视图产出 TOP/FRONT/SIDE
> 坐标系说明：三视图与 GT 坐标系不一定相同，此表用于人工逐格分析；TIS 的 TOP 与 GT TOP 同构。

## TIS baseline（单次俯视）

### 样本 1 `09c1414f1b`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the cutting board and the suitcase (in meters)?
- QA：模型 1.3 vs GT 1.8（错误）
- 类别：cutting board, suitcase
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- cutting board：GT ['(1.0, 2.0)'] | 模型 ['(5.0, 5.0)']
- suitcase：GT ['(2.0, 4.0)'] | 模型 ['(3.0, 8.0)']
**FRONT 视图**（GT → 模型）
- cutting board：GT ['(1.0, 5.0)'] | 模型 []
- suitcase：GT ['(2.0, 1.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- cutting board：GT ['(2.0, 5.0)'] | 模型 []
- suitcase：GT ['(4.0, 1.0)'] | 模型 []

### 样本 2 `47334103`（arkitscenes · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the table and the stool (in meters)?
- QA：模型 0.3 vs GT 3.7（错误）
- 类别：stool, table
- tags：A2_extra, B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- stool：GT ['(2.0, 2.0)'] | 模型 ['(4.0, 5.0)', '(6.0, 5.0)']
- table：GT ['(7.0, 1.0)'] | 模型 ['(5.0, 5.0)']
**FRONT 视图**（GT → 模型）
- stool：GT ['(2.0, 1.0)'] | 模型 []
- table：GT ['(7.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- stool：GT ['(2.0, 1.0)'] | 模型 []
- table：GT ['(1.0, 2.0)'] | 模型 []

### 样本 3 `42897538`（arkitscenes · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the stool and the refrigerator (in meters)?
- QA：模型 1.5 vs GT 2.6（错误）
- 类别：refrigerator, stool
- tags：A2_extra, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(3.0, 7.0)'] | 模型 ['(2.0, 8.0)']
- stool：GT ['(3.0, 3.0)'] | 模型 ['(4.0, 5.0)', '(5.0, 5.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(3.0, 4.0)'] | 模型 []
- stool：GT ['(3.0, 1.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(7.0, 4.0)'] | 模型 []
- stool：GT ['(3.0, 1.0)'] | 模型 []

### 样本 4 `scene0550_00`（scannet · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the door and the window (in meters)?
- QA：模型 3.5 vs GT 2.5（错误）
- 类别：door, window
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(4.0, 8.0)'] | 模型 ['(1.0, 5.0)']
- window：GT ['(5.0, 1.0)'] | 模型 ['(5.0, 1.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(4.0, 4.0)'] | 模型 []
- window：GT ['(5.0, 5.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- door：GT ['(8.0, 4.0)'] | 模型 []
- window：GT ['(1.0, 5.0)'] | 模型 []

### 样本 5 `scene0378_01`（scannet · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the door and the clock (in meters)?
- QA：模型 2.0 vs GT 1.6（错误）
- 类别：clock, door
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- clock：GT ['(3.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- door：GT ['(6.0, 1.0)'] | 模型 ['(1.0, 5.0)']
**FRONT 视图**（GT → 模型）
- clock：GT ['(3.0, 7.0)'] | 模型 []
- door：GT ['(6.0, 4.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- clock：GT ['(2.0, 7.0)'] | 模型 []
- door：GT ['(1.0, 4.0)'] | 模型 []

### 样本 6 `c49a8c6cff`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the trash can and the bed (in meters)?
- QA：模型 1.5 vs GT 0.7（错误）
- 类别：bed, trash can
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(6.0, 5.0)'] | 模型 ['(5.0, 5.0)']
- trash can：GT ['(2.0, 6.0)'] | 模型 ['(8.0, 8.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(6.0, 2.0)'] | 模型 []
- trash can：GT ['(2.0, 1.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- bed：GT ['(5.0, 2.0)'] | 模型 []
- trash can：GT ['(6.0, 1.0)'] | 模型 []

### 样本 7 `3db0a1c8f3`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the blanket and the computer mouse (in meters)?
- QA：模型 1.2 vs GT 0.8（错误）
- 类别：blanket, computer mouse
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- blanket：GT ['(1.0, 1.0)'] | 模型 ['(5.0, 5.0)']
- computer mouse：GT ['(3.0, 3.0)'] | 模型 ['(7.0, 3.0)']
**FRONT 视图**（GT → 模型）
- blanket：GT ['(1.0, 2.0)'] | 模型 []
- computer mouse：GT ['(3.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- blanket：GT ['(1.0, 2.0)'] | 模型 []
- computer mouse：GT ['(3.0, 2.0)'] | 模型 []

### 样本 8 `c50d2d1d42`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the door and the telephone (in meters)?
- QA：模型 2.0 vs GT 4.6（错误）
- 类别：door, telephone
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 4.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 []
- telephone：GT ['(7.0, 3.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- door：GT ['(3.0, 3.0)'] | 模型 []
- telephone：GT ['(3.0, 3.0)'] | 模型 []

### 样本 9 `scene0474_04`（scannet · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the table and the trash bin (in meters)?
- QA：模型 1.1 vs GT 1.9（错误）
- 类别：table, trash bin
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- table：GT ['(4.0, 6.0)'] | 模型 ['(5.0, 6.0)']
- trash bin：GT ['(6.0, 3.0)'] | 模型 ['(3.0, 8.0)']
**FRONT 视图**（GT → 模型）
- table：GT ['(4.0, 2.0)'] | 模型 []
- trash bin：GT ['(6.0, 1.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- table：GT ['(6.0, 2.0)'] | 模型 []
- trash bin：GT ['(3.0, 1.0)'] | 模型 []

### 样本 10 `47333899`（arkitscenes · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the table and the stove (in meters)?
- QA：模型 1.2 vs GT 0.9（错误）
- 类别：stove, table
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- stove：GT ['(2.0, 7.0)'] | 模型 ['(2.0, 5.0)']
- table：GT ['(2.0, 1.0)'] | 模型 ['(5.0, 6.0)']
**FRONT 视图**（GT → 模型）
- stove：GT ['(2.0, 4.0)'] | 模型 []
- table：GT ['(2.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- stove：GT ['(7.0, 4.0)'] | 模型 []
- table：GT ['(1.0, 2.0)'] | 模型 []

### 样本 11 `scene0221_01`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (chair, bed, pillow, lamp) is the closest to the microwave?
- QA：模型 A vs GT B（错误）
- 类别：bed, chair, lamp, microwave, pillow
- tags：A1_miss, B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(4.0, 3.0)', '(2.0, 3.0)'] | 模型 ['(3.0, 5.0)']
- chair：GT ['(3.0, 6.0)', '(1.0, 6.0)', '(2.0, 7.0)'] | 模型 ['(7.0, 4.0)']
- lamp：GT ['(3.0, 1.0)', '(3.0, 0.0)'] | 模型 ['(2.0, 7.0)']
- microwave：GT ['(6.0, 1.0)'] | 模型 ['(8.0, 3.0)']
- pillow：GT ['(2.0, 1.0)', '(4.0, 1.0)', '(4.0, 1.0)', '(4.0, 1.0)', '(2.0, 1.0)'] | 模型 ['(3.0, 6.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(4.0, 2.0)', '(2.0, 3.0)'] | 模型 []
- chair：GT ['(3.0, 3.0)', '(1.0, 5.0)', '(2.0, 4.0)'] | 模型 []
- lamp：GT ['(3.0, 4.0)', '(3.0, 5.0)'] | 模型 []
- microwave：GT ['(6.0, 5.0)'] | 模型 []
- pillow：GT ['(2.0, 4.0)', '(4.0, 4.0)', '(4.0, 4.0)', '(4.0, 4.0)', '(2.0, 4.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- bed：GT ['(3.0, 2.0)', '(3.0, 3.0)'] | 模型 []
- chair：GT ['(6.0, 3.0)', '(6.0, 5.0)', '(7.0, 4.0)'] | 模型 []
- lamp：GT ['(1.0, 4.0)', '(0.0, 5.0)'] | 模型 []
- microwave：GT ['(1.0, 5.0)'] | 模型 []
- pillow：GT ['(1.0, 4.0)', '(1.0, 4.0)', '(1.0, 4.0)', '(1.0, 4.0)', '(1.0, 4.0)'] | 模型 []

### 样本 12 `scene0307_02`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (window, chair, door, washing machine) is the closest to the radiator?
- QA：模型 A vs GT C（错误）
- 类别：chair, door, radiator, washing machine, window
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 6.0)'] | 模型 ['(5.0, 6.0)']
- door：GT ['(3.0, 5.0)', '(4.0, 7.0)', '(3.0, 5.0)', '(1.0, 7.0)', '(7.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- radiator：GT ['(1.0, 5.0)'] | 模型 ['(8.0, 3.0)']
- washing machine：GT ['(2.0, 7.0)'] | 模型 ['(3.0, 8.0)']
- window：GT ['(4.0, 1.0)', '(2.0, 7.0)', '(4.0, 1.0)'] | 模型 ['(8.0, 1.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)'] | 模型 []
- door：GT ['(3.0, 4.0)', '(4.0, 4.0)', '(3.0, 4.0)', '(1.0, 4.0)', '(7.0, 4.0)'] | 模型 []
- radiator：GT ['(1.0, 3.0)'] | 模型 []
- washing machine：GT ['(2.0, 2.0)'] | 模型 []
- window：GT ['(4.0, 6.0)', '(2.0, 6.0)', '(4.0, 6.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- chair：GT ['(6.0, 2.0)'] | 模型 []
- door：GT ['(5.0, 4.0)', '(7.0, 4.0)', '(5.0, 4.0)', '(7.0, 4.0)', '(3.0, 4.0)'] | 模型 []
- radiator：GT ['(5.0, 3.0)'] | 模型 []
- washing machine：GT ['(7.0, 2.0)'] | 模型 []
- window：GT ['(1.0, 6.0)', '(7.0, 6.0)', '(1.0, 6.0)'] | 模型 []

### 样本 13 `47429977`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (stove, chair, refrigerator, table) is the closest to the tv?
- QA：模型 B vs GT D（错误）
- 类别：chair, refrigerator, stove, table, tv
- tags：A1_miss, A2_extra, B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 1.0)', '(3.0, 2.0)', '(3.0, 1.0)'] | 模型 ['(5.0, 6.0)', '(7.0, 6.0)', '(6.0, 5.0)', '(6.0, 7.0)']
- refrigerator：GT ['(2.0, 7.0)'] | 模型 ['(2.0, 2.0)']
- stove：GT ['(1.0, 3.0)'] | 模型 ['(4.0, 2.0)']
- table：GT ['(6.0, 4.0)', '(3.0, 1.0)'] | 模型 ['(6.0, 6.0)']
- tv：GT ['(6.0, 1.0)'] | 模型 ['(9.0, 5.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 3.0)', '(3.0, 3.0)', '(3.0, 3.0)'] | 模型 []
- refrigerator：GT ['(2.0, 4.0)'] | 模型 []
- stove：GT ['(1.0, 5.0)'] | 模型 []
- table：GT ['(6.0, 2.0)', '(3.0, 3.0)'] | 模型 []
- tv：GT ['(6.0, 6.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- chair：GT ['(1.0, 3.0)', '(2.0, 3.0)', '(1.0, 3.0)'] | 模型 []
- refrigerator：GT ['(7.0, 4.0)'] | 模型 []
- stove：GT ['(3.0, 5.0)'] | 模型 []
- table：GT ['(4.0, 2.0)', '(1.0, 3.0)'] | 模型 []
- tv：GT ['(1.0, 6.0)'] | 模型 []

### 样本 14 `scene0653_00`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (window, monitor, table, keyboard) is the closest to the door?
- QA：模型 B vs GT C（错误）
- 类别：door, keyboard, monitor, table, window
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(7.0, 7.0)'] | 模型 ['(1.0, 5.0)']
- keyboard：GT ['(2.0, 3.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 6.0)']
- monitor：GT ['(1.0, 6.0)', '(2.0, 3.0)', '(2.0, 3.0)', '(6.0, 1.0)', '(7.0, 1.0)', '(6.0, 4.0)', '(6.0, 6.0)'] | 模型 ['(5.0, 4.0)']
- table：GT ['(1.0, 6.0)', '(2.0, 3.0)', '(6.0, 4.0)', '(2.0, 4.0)', '(7.0, 1.0)', '(6.0, 6.0)'] | 模型 ['(5.0, 7.0)']
- window：GT ['(1.0, 5.0)', '(1.0, 2.0)'] | 模型 ['(9.0, 3.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(7.0, 5.0)'] | 模型 []
- keyboard：GT ['(2.0, 2.0)', '(6.0, 2.0)'] | 模型 []
- monitor：GT ['(1.0, 3.0)', '(2.0, 3.0)', '(2.0, 3.0)', '(6.0, 3.0)', '(7.0, 3.0)', '(6.0, 3.0)', '(6.0, 3.0)'] | 模型 []
- table：GT ['(1.0, 2.0)', '(2.0, 2.0)', '(6.0, 2.0)', '(2.0, 1.0)', '(7.0, 2.0)', '(6.0, 2.0)'] | 模型 []
- window：GT ['(1.0, 5.0)', '(1.0, 5.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- door：GT ['(7.0, 5.0)'] | 模型 []
- keyboard：GT ['(3.0, 2.0)', '(2.0, 2.0)'] | 模型 []
- monitor：GT ['(6.0, 3.0)', '(3.0, 3.0)', '(3.0, 3.0)', '(1.0, 3.0)', '(1.0, 3.0)', '(4.0, 3.0)', '(6.0, 3.0)'] | 模型 []
- table：GT ['(6.0, 2.0)', '(3.0, 2.0)', '(4.0, 2.0)', '(4.0, 1.0)', '(1.0, 2.0)', '(6.0, 2.0)'] | 模型 []
- window：GT ['(5.0, 5.0)', '(2.0, 5.0)'] | 模型 []

### 样本 15 `38d58a7a31`（scannetpp · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (telephone, heater, chair, ceiling light) is the closest to the trash can?
- QA：模型 A vs GT C（错误）
- 类别：ceiling light, chair, heater, telephone, trash can
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, QA_wrong
**TOP 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 1.0)', '(1.0, 2.0)', '(4.0, 6.0)', '(1.0, 3.0)', '(4.0, 5.0)', '(4.0, 3.0)', '(6.0, 1.0)', '(7.0, 6.0)', '(6.0, 4.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 1.0)']
- chair：GT ['(1.0, 6.0)', '(3.0, 6.0)', '(4.0, 4.0)', '(5.0, 5.0)', '(6.0, 4.0)', '(2.0, 5.0)', '(2.0, 7.0)', '(5.0, 3.0)', '(4.0, 3.0)', '(4.0, 6.0)', '(6.0, 6.0)', '(6.0, 1.0)', '(1.0, 6.0)', '(6.0, 2.0)', '(3.0, 6.0)', '(4.0, 6.0)', '(1.0, 7.0)', '(2.0, 5.0)', '(5.0, 6.0)', '(3.0, 3.0)', '(5.0, 4.0)', '(6.0, 4.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(7.0, 3.0)', '(7.0, 6.0)', '(6.0, 6.0)', '(3.0, 5.0)', '(2.0, 2.0)', '(3.0, 5.0)', '(2.0, 3.0)', '(1.0, 7.0)', '(1.0, 7.0)', '(1.0, 6.0)', '(1.0, 6.0)', '(1.0, 6.0)'] | 模型 ['(4.0, 6.0)']
- heater：GT ['(7.0, 4.0)', '(8.0, 6.0)', '(7.0, 1.0)'] | 模型 ['(1.0, 7.0)']
- telephone：GT ['(7.0, 2.0)'] | 模型 ['(5.0, 5.0)']
- trash can：GT ['(1.0, 4.0)'] | 模型 ['(8.0, 8.0)']
**FRONT 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 7.0)', '(1.0, 7.0)', '(4.0, 8.0)', '(1.0, 8.0)', '(4.0, 7.0)', '(4.0, 7.0)', '(6.0, 8.0)', '(7.0, 7.0)', '(6.0, 8.0)', '(6.0, 7.0)'] | 模型 []
- chair：GT ['(1.0, 2.0)', '(3.0, 2.0)', '(4.0, 2.0)', '(5.0, 2.0)', '(6.0, 2.0)', '(2.0, 2.0)', '(2.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(4.0, 2.0)', '(6.0, 2.0)', '(6.0, 1.0)', '(1.0, 2.0)', '(6.0, 2.0)', '(3.0, 2.0)', '(4.0, 1.0)', '(1.0, 2.0)', '(2.0, 1.0)', '(5.0, 2.0)', '(3.0, 1.0)', '(5.0, 2.0)', '(6.0, 1.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(7.0, 2.0)', '(7.0, 2.0)', '(6.0, 2.0)', '(3.0, 2.0)', '(2.0, 2.0)', '(3.0, 2.0)', '(2.0, 2.0)', '(1.0, 2.0)', '(1.0, 2.0)', '(1.0, 2.0)', '(1.0, 2.0)', '(1.0, 1.0)'] | 模型 []
- heater：GT ['(7.0, 1.0)', '(8.0, 1.0)', '(7.0, 1.0)'] | 模型 []
- telephone：GT ['(7.0, 3.0)'] | 模型 []
- trash can：GT ['(1.0, 1.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- ceiling light：GT ['(1.0, 7.0)', '(2.0, 7.0)', '(6.0, 8.0)', '(3.0, 8.0)', '(5.0, 7.0)', '(3.0, 7.0)', '(1.0, 8.0)', '(6.0, 7.0)', '(4.0, 8.0)', '(3.0, 7.0)'] | 模型 []
- chair：GT ['(6.0, 2.0)', '(6.0, 2.0)', '(4.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(5.0, 2.0)', '(7.0, 2.0)', '(3.0, 2.0)', '(3.0, 2.0)', '(6.0, 2.0)', '(6.0, 2.0)', '(1.0, 1.0)', '(6.0, 2.0)', '(2.0, 2.0)', '(6.0, 2.0)', '(6.0, 1.0)', '(7.0, 2.0)', '(5.0, 1.0)', '(6.0, 2.0)', '(3.0, 1.0)', '(4.0, 2.0)', '(4.0, 1.0)', '(2.0, 2.0)', '(2.0, 2.0)', '(3.0, 2.0)', '(6.0, 2.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(2.0, 2.0)', '(5.0, 2.0)', '(3.0, 2.0)', '(7.0, 2.0)', '(7.0, 2.0)', '(6.0, 2.0)', '(6.0, 2.0)', '(6.0, 1.0)'] | 模型 []
- heater：GT ['(4.0, 1.0)', '(6.0, 1.0)', '(1.0, 1.0)'] | 模型 []
- telephone：GT ['(2.0, 3.0)'] | 模型 []
- trash can：GT ['(4.0, 1.0)'] | 模型 []

### 样本 16 `42899461`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (chair, sofa, fireplace, stove) is the closest to the tv?
- QA：模型 C vs GT A（错误）
- 类别：chair, fireplace, sofa, stove, tv
- tags：A1_miss, B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(7.0, 4.0)', '(7.0, 3.0)', '(2.0, 4.0)', '(1.0, 4.0)'] | 模型 ['(3.0, 5.0)']
- fireplace：GT ['(4.0, 8.0)'] | 模型 ['(5.0, 2.0)']
- sofa：GT ['(7.0, 6.0)'] | 模型 ['(5.0, 7.0)']
- stove：GT ['(1.0, 1.0)'] | 模型 []
- tv：GT ['(1.0, 7.0)'] | 模型 ['(5.0, 3.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(7.0, 3.0)', '(7.0, 3.0)', '(2.0, 4.0)', '(1.0, 4.0)'] | 模型 []
- fireplace：GT ['(4.0, 4.0)'] | 模型 []
- sofa：GT ['(7.0, 4.0)'] | 模型 []
- stove：GT ['(1.0, 7.0)'] | 模型 []
- tv：GT ['(1.0, 5.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- chair：GT ['(4.0, 3.0)', '(3.0, 3.0)', '(4.0, 4.0)', '(4.0, 4.0)'] | 模型 []
- fireplace：GT ['(8.0, 4.0)'] | 模型 []
- sofa：GT ['(6.0, 4.0)'] | 模型 []
- stove：GT ['(1.0, 7.0)'] | 模型 []
- tv：GT ['(7.0, 5.0)'] | 模型 []

### 样本 17 `42899461`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (table, tv, sofa, stove) is the closest to the fireplace?
- QA：模型 B vs GT A（错误）
- 类别：fireplace, sofa, stove, table, tv
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, QA_wrong
**TOP 视图**（GT → 模型）
- fireplace：GT ['(4.0, 8.0)'] | 模型 []
- sofa：GT ['(7.0, 6.0)'] | 模型 ['(5.0, 2.0)']
- stove：GT ['(1.0, 1.0)'] | 模型 []
- table：GT ['(6.0, 7.0)', '(1.0, 7.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- tv：GT ['(1.0, 7.0)'] | 模型 ['(5.0, 8.0)']
**FRONT 视图**（GT → 模型）
- fireplace：GT ['(4.0, 4.0)'] | 模型 []
- sofa：GT ['(7.0, 4.0)'] | 模型 []
- stove：GT ['(1.0, 7.0)'] | 模型 []
- table：GT ['(6.0, 2.0)', '(1.0, 2.0)', '(6.0, 3.0)'] | 模型 []
- tv：GT ['(1.0, 5.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- fireplace：GT ['(8.0, 4.0)'] | 模型 []
- sofa：GT ['(6.0, 4.0)'] | 模型 []
- stove：GT ['(1.0, 7.0)'] | 模型 []
- table：GT ['(7.0, 2.0)', '(7.0, 2.0)', '(3.0, 3.0)'] | 模型 []
- tv：GT ['(7.0, 5.0)'] | 模型 []

### 样本 18 `47430034`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (chair, stool, table, bed) is the closest to the tv?
- QA：模型 D vs GT C（错误）
- 类别：bed, chair, stool, table, tv
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(5.0, 2.0)'] | 模型 ['(5.0, 5.0)']
- chair：GT ['(5.0, 7.0)', '(6.0, 7.0)', '(1.0, 2.0)'] | 模型 ['(3.0, 8.0)']
- stool：GT ['(4.0, 3.0)'] | 模型 []
- table：GT ['(4.0, 3.0)', '(6.0, 7.0)', '(1.0, 2.0)'] | 模型 ['(3.0, 7.0)']
- tv：GT ['(7.0, 7.0)'] | 模型 ['(8.0, 4.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(5.0, 4.0)'] | 模型 []
- chair：GT ['(5.0, 3.0)', '(6.0, 3.0)', '(1.0, 2.0)'] | 模型 []
- stool：GT ['(4.0, 1.0)'] | 模型 []
- table：GT ['(4.0, 2.0)', '(6.0, 2.0)', '(1.0, 2.0)'] | 模型 []
- tv：GT ['(7.0, 6.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- bed：GT ['(2.0, 4.0)'] | 模型 []
- chair：GT ['(7.0, 3.0)', '(7.0, 3.0)', '(2.0, 2.0)'] | 模型 []
- stool：GT ['(3.0, 1.0)'] | 模型 []
- table：GT ['(3.0, 2.0)', '(7.0, 2.0)', '(2.0, 2.0)'] | 模型 []
- tv：GT ['(7.0, 6.0)'] | 模型 []

### 样本 19 `scene0616_01`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (table, trash bin, chair, lamp) is the closest to the window?
- QA：模型 A vs GT A（正确）
- 类别：chair, lamp, table, trash bin, window
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)', '(4.0, 2.0)', '(4.0, 3.0)', '(3.0, 5.0)', '(3.0, 4.0)', '(5.0, 6.0)', '(6.0, 5.0)'] | 模型 ['(4.0, 4.0)', '(6.0, 4.0)']
- lamp：GT ['(5.0, 1.0)'] | 模型 ['(8.0, 2.0)']
- table：GT ['(5.0, 1.0)', '(3.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- trash bin：GT ['(7.0, 4.0)', '(7.0, 4.0)'] | 模型 ['(2.0, 2.0)']
- window：GT ['(1.0, 3.0)'] | 模型 ['(5.0, 9.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)', '(4.0, 2.0)', '(4.0, 2.0)', '(3.0, 2.0)', '(3.0, 2.0)', '(5.0, 2.0)', '(6.0, 2.0)'] | 模型 []
- lamp：GT ['(5.0, 4.0)'] | 模型 []
- table：GT ['(5.0, 2.0)', '(3.0, 2.0)'] | 模型 []
- trash bin：GT ['(7.0, 2.0)', '(7.0, 2.0)'] | 模型 []
- window：GT ['(1.0, 5.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- chair：GT ['(2.0, 2.0)', '(2.0, 2.0)', '(3.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(6.0, 2.0)', '(5.0, 2.0)'] | 模型 []
- lamp：GT ['(1.0, 4.0)'] | 模型 []
- table：GT ['(1.0, 2.0)', '(3.0, 2.0)'] | 模型 []
- trash bin：GT ['(4.0, 2.0)', '(4.0, 2.0)'] | 模型 []
- window：GT ['(3.0, 5.0)'] | 模型 []

### 样本 20 `scene0651_02`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (counter, chair, table, trash bin) is the closest to the sofa?
- QA：模型 C vs GT C（正确）
- 类别：chair, counter, sofa, table, trash bin
- tags：A1_miss, B3_pair, B5_adjacent
**TOP 视图**（GT → 模型）
- chair：GT ['(7.0, 4.0)', '(5.0, 3.0)', '(5.0, 4.0)', '(6.0, 3.0)'] | 模型 ['(3.0, 5.0)', '(7.0, 5.0)']
- counter：GT ['(3.0, 6.0)'] | 模型 ['(1.0, 8.0)']
- sofa：GT ['(5.0, 1.0)'] | 模型 ['(5.0, 2.0)']
- table：GT ['(3.0, 2.0)', '(5.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- trash bin：GT ['(1.0, 6.0)'] | 模型 ['(1.0, 9.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(7.0, 2.0)', '(5.0, 3.0)', '(5.0, 3.0)', '(6.0, 3.0)'] | 模型 []
- counter：GT ['(3.0, 5.0)'] | 模型 []
- sofa：GT ['(5.0, 3.0)'] | 模型 []
- table：GT ['(3.0, 1.0)', '(5.0, 2.0)'] | 模型 []
- trash bin：GT ['(1.0, 1.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)', '(3.0, 3.0)', '(4.0, 3.0)', '(3.0, 3.0)'] | 模型 []
- counter：GT ['(6.0, 5.0)'] | 模型 []
- sofa：GT ['(1.0, 3.0)'] | 模型 []
- table：GT ['(2.0, 1.0)', '(3.0, 2.0)'] | 模型 []
- trash bin：GT ['(6.0, 1.0)'] | 模型 []

### 样本 21 `31a2c91c43`（scannetpp · object_rel_direction_easy）
- 问题：If I am standing by the ceiling light and facing the toilet, is the door to the left or the right of the toilet?
- QA：模型 B vs GT A（错误）
- 类别：ceiling light, door, toilet
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- ceiling light：GT ['(5.0, 8.0)'] | 模型 ['(5.0, 1.0)']
- door：GT ['(2.0, 4.0)'] | 模型 ['(1.0, 5.0)']
- toilet：GT ['(6.0, 2.0)'] | 模型 ['(4.0, 7.0)']
**FRONT 视图**（GT → 模型）
- ceiling light：GT ['(5.0, 8.0)'] | 模型 []
- door：GT ['(2.0, 4.0)'] | 模型 []
- toilet：GT ['(6.0, 1.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- ceiling light：GT ['(8.0, 8.0)'] | 模型 []
- door：GT ['(4.0, 4.0)'] | 模型 []
- toilet：GT ['(2.0, 1.0)'] | 模型 []

### 样本 22 `scene0353_00`（scannet · object_rel_direction_easy）
- 问题：If I am standing by the bookshelf and facing the door, is the refrigerator to the left or the right of the door?
- QA：模型 B vs GT A（错误）
- 类别：bookshelf, door, refrigerator
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- bookshelf：GT ['(7.0, 1.0)'] | 模型 ['(8.0, 4.0)']
- door：GT ['(7.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- refrigerator：GT ['(5.0, 5.0)'] | 模型 ['(2.0, 8.0)']
**FRONT 视图**（GT → 模型）
- bookshelf：GT ['(7.0, 3.0)'] | 模型 []
- door：GT ['(7.0, 4.0)'] | 模型 []
- refrigerator：GT ['(5.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- bookshelf：GT ['(1.0, 3.0)'] | 模型 []
- door：GT ['(3.0, 4.0)'] | 模型 []
- refrigerator：GT ['(5.0, 2.0)'] | 模型 []

### 样本 23 `41159525`（arkitscenes · object_rel_direction_easy）
- 问题：If I am standing by the stove and facing the table, is the refrigerator to the left or the right of the table?
- QA：模型 A vs GT B（错误）
- 类别：refrigerator, stove, table
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 1.0)'] | 模型 ['(1.0, 5.0)']
- stove：GT ['(1.0, 1.0)'] | 模型 ['(5.0, 5.0)']
- table：GT ['(6.0, 5.0)'] | 模型 ['(8.0, 6.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 4.0)'] | 模型 []
- stove：GT ['(1.0, 4.0)'] | 模型 []
- table：GT ['(6.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 4.0)'] | 模型 []
- stove：GT ['(1.0, 4.0)'] | 模型 []
- table：GT ['(5.0, 2.0)'] | 模型 []

### 样本 24 `d755b3d9d8`（scannetpp · object_rel_direction_easy）
- 问题：If I am standing by the cup and facing the whiteboard, is the shoes to the left or the right of the whiteboard?
- QA：模型 A vs GT A（正确）
- 类别：cup, shoes, whiteboard
- tags：B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- cup：GT ['(5.0, 1.0)'] | 模型 ['(4.0, 4.0)']
- shoes：GT ['(7.0, 4.0)'] | 模型 ['(3.0, 8.0)']
- whiteboard：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 1.0)']
**FRONT 视图**（GT → 模型）
- cup：GT ['(5.0, 2.0)'] | 模型 []
- shoes：GT ['(7.0, 0.0)'] | 模型 []
- whiteboard：GT ['(2.0, 4.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- cup：GT ['(1.0, 2.0)'] | 模型 []
- shoes：GT ['(4.0, 0.0)'] | 模型 []
- whiteboard：GT ['(7.0, 4.0)'] | 模型 []

### 样本 25 `47204578`（arkitscenes · object_rel_direction_easy）
- 问题：If I am standing by the tv and facing the table, is the stool to the left or the right of the table?
- QA：模型 A vs GT A（正确）
- 类别：stool, table, tv
- tags：A2_extra, B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- stool：GT ['(1.0, 1.0)'] | 模型 ['(4.0, 4.0)', '(6.0, 4.0)']
- table：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 5.0)']
- tv：GT ['(3.0, 1.0)'] | 模型 ['(5.0, 9.0)']
**FRONT 视图**（GT → 模型）
- stool：GT ['(1.0, 1.0)'] | 模型 []
- table：GT ['(2.0, 2.0)'] | 模型 []
- tv：GT ['(3.0, 6.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- stool：GT ['(1.0, 1.0)'] | 模型 []
- table：GT ['(7.0, 2.0)'] | 模型 []
- tv：GT ['(1.0, 6.0)'] | 模型 []

### 样本 26 `scene0458_00`（scannet · object_rel_direction_easy）
- 问题：If I am standing by the window and facing the door, is the mirror to the left or the right of the door?
- QA：模型 B vs GT B（正确）
- 类别：door, mirror, window
- tags：B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- door：GT ['(8.0, 6.0)'] | 模型 ['(1.0, 8.0)']
- mirror：GT ['(1.0, 6.0)'] | 模型 ['(5.0, 5.0)']
- window：GT ['(6.0, 1.0)'] | 模型 ['(9.0, 4.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(8.0, 5.0)'] | 模型 []
- mirror：GT ['(1.0, 4.0)'] | 模型 []
- window：GT ['(6.0, 5.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- door：GT ['(6.0, 5.0)'] | 模型 []
- mirror：GT ['(6.0, 4.0)'] | 模型 []
- window：GT ['(1.0, 5.0)'] | 模型 []

### 样本 27 `scene0426_00`（scannet · object_rel_direction_easy）
- 问题：If I am standing by the tv and facing the lamp, is the table to the left or the right of the lamp?
- QA：模型 A vs GT A（正确）
- 类别：lamp, table, tv
- tags：B3_pair
**TOP 视图**（GT → 模型）
- lamp：GT ['(5.0, 1.0)'] | 模型 ['(2.0, 3.0)']
- table：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 6.0)']
- tv：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 2.0)']
**FRONT 视图**（GT → 模型）
- lamp：GT ['(5.0, 4.0)'] | 模型 []
- table：GT ['(2.0, 2.0)'] | 模型 []
- tv：GT ['(7.0, 4.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- lamp：GT ['(1.0, 4.0)'] | 模型 []
- table：GT ['(7.0, 2.0)'] | 模型 []
- tv：GT ['(3.0, 4.0)'] | 模型 []

### 样本 28 `scene0144_00`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the window and facing the lamp, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 1
- QA：模型 C vs GT C（正确）
- 类别：door, lamp, window
- tags：B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- door：GT ['(8.0, 1.0)'] | 模型 ['(1.0, 5.0)']
- lamp：GT ['(5.0, 7.0)'] | 模型 ['(5.0, 2.0)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 9.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(8.0, 3.0)'] | 模型 []
- lamp：GT ['(5.0, 5.0)'] | 模型 []
- window：GT ['(1.0, 6.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- door：GT ['(1.0, 3.0)'] | 模型 []
- lamp：GT ['(7.0, 5.0)'] | 模型 []
- window：GT ['(5.0, 6.0)'] | 模型 []

### 样本 29 `scene0629_01`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the bed and facing the chair, is the mirror to my left, right, or back?
An object is to my back if I would have to turn at least 1
- QA：模型 C vs GT B（错误）
- 类别：bed, chair, mirror
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 6.0)']
- chair：GT ['(6.0, 7.0)'] | 模型 ['(3.0, 4.0)']
- mirror：GT ['(3.0, 6.0)'] | 模型 ['(1.0, 5.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(7.0, 3.0)'] | 模型 []
- chair：GT ['(6.0, 2.0)'] | 模型 []
- mirror：GT ['(3.0, 4.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- bed：GT ['(4.0, 3.0)'] | 模型 []
- chair：GT ['(7.0, 2.0)'] | 模型 []
- mirror：GT ['(6.0, 4.0)'] | 模型 []

### 样本 30 `5ee7c22ba0`（scannetpp · object_rel_direction_medium）
- 问题：If I am standing by the refrigerator and facing the microwave, is the ceiling light to my left, right, or back?
An object is to my back if I would hav
- QA：模型 A vs GT B（错误）
- 类别：ceiling light, microwave, refrigerator
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 3.0)'] | 模型 ['(4.0, 1.0)']
- microwave：GT ['(3.0, 1.0)'] | 模型 ['(3.0, 5.0)']
- refrigerator：GT ['(4.0, 7.0)'] | 模型 ['(1.0, 6.0)']
**FRONT 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 8.0)'] | 模型 []
- microwave：GT ['(3.0, 3.0)'] | 模型 []
- refrigerator：GT ['(4.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- ceiling light：GT ['(3.0, 8.0)'] | 模型 []
- microwave：GT ['(1.0, 3.0)'] | 模型 []
- refrigerator：GT ['(7.0, 2.0)'] | 模型 []

### 样本 31 `45261121`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the table and facing the tv, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 135
- QA：模型 C vs GT A（错误）
- 类别：stove, table, tv
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- stove：GT ['(3.0, 2.0)'] | 模型 ['(2.0, 8.0)']
- table：GT ['(5.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- tv：GT ['(7.0, 1.0)'] | 模型 ['(8.0, 3.0)']
**FRONT 视图**（GT → 模型）
- stove：GT ['(3.0, 3.0)'] | 模型 []
- table：GT ['(5.0, 2.0)'] | 模型 []
- tv：GT ['(7.0, 7.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- stove：GT ['(2.0, 3.0)'] | 模型 []
- table：GT ['(4.0, 2.0)'] | 模型 []
- tv：GT ['(1.0, 7.0)'] | 模型 []

### 样本 32 `45b0dac5e3`（scannetpp · object_rel_direction_medium）
- 问题：If I am standing by the cup and facing the heater, is the toilet to my left, right, or back?
An object is to my back if I would have to turn at least 
- QA：模型 A vs GT C（错误）
- 类别：cup, heater, toilet
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- cup：GT ['(6.0, 1.0)'] | 模型 ['(3.0, 3.0)']
- heater：GT ['(0.0, 5.0)'] | 模型 ['(8.0, 5.0)']
- toilet：GT ['(7.0, 6.0)'] | 模型 ['(4.0, 8.0)']
**FRONT 视图**（GT → 模型）
- cup：GT ['(6.0, 3.0)'] | 模型 []
- heater：GT ['(0.0, 3.0)'] | 模型 []
- toilet：GT ['(7.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- cup：GT ['(1.0, 3.0)'] | 模型 []
- heater：GT ['(5.0, 3.0)'] | 模型 []
- toilet：GT ['(6.0, 2.0)'] | 模型 []

### 样本 33 `scene0695_00`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the lamp and facing the pillow, is the table to my left, right, or back?
An object is to my back if I would have to turn at least 
- QA：模型 C vs GT C（正确）
- 类别：lamp, pillow, table
- tags：A2_extra, B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- lamp：GT ['(5.0, 1.0)'] | 模型 ['(8.0, 3.0)']
- pillow：GT ['(1.0, 2.0)'] | 模型 ['(3.0, 4.0)', '(4.0, 4.0)']
- table：GT ['(3.0, 7.0)'] | 模型 ['(8.0, 4.0)']
**FRONT 视图**（GT → 模型）
- lamp：GT ['(5.0, 4.0)'] | 模型 []
- pillow：GT ['(1.0, 4.0)'] | 模型 []
- table：GT ['(3.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- lamp：GT ['(1.0, 4.0)'] | 模型 []
- pillow：GT ['(2.0, 4.0)'] | 模型 []
- table：GT ['(7.0, 2.0)'] | 模型 []

### 样本 34 `47334096`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the stool and facing the sofa, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 1
- QA：模型 A vs GT C（错误）
- 类别：sofa, stool, stove
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- sofa：GT ['(4.0, 4.0)'] | 模型 ['(3.0, 8.0)']
- stool：GT ['(5.0, 1.0)'] | 模型 ['(5.0, 5.0)']
- stove：GT ['(7.0, 6.0)'] | 模型 ['(8.0, 2.0)']
**FRONT 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 []
- stool：GT ['(5.0, 2.0)'] | 模型 []
- stove：GT ['(7.0, 5.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 []
- stool：GT ['(1.0, 2.0)'] | 模型 []
- stove：GT ['(6.0, 5.0)'] | 模型 []

### 样本 35 `42446103`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the stove and facing the tv, is the stool to my left, right, or back?
An object is to my back if I would have to turn at least 135
- QA：模型 C vs GT A（错误）
- 类别：stool, stove, tv
- tags：A2_extra, B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- stool：GT ['(3.0, 3.0)'] | 模型 ['(3.0, 6.0)', '(4.0, 6.0)']
- stove：GT ['(3.0, 7.0)'] | 模型 ['(5.0, 2.0)']
- tv：GT ['(8.0, 2.0)'] | 模型 ['(8.0, 5.0)']
**FRONT 视图**（GT → 模型）
- stool：GT ['(3.0, 1.0)'] | 模型 []
- stove：GT ['(3.0, 4.0)'] | 模型 []
- tv：GT ['(8.0, 7.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- stool：GT ['(3.0, 1.0)'] | 模型 []
- stove：GT ['(7.0, 4.0)'] | 模型 []
- tv：GT ['(2.0, 7.0)'] | 模型 []

### 样本 36 `42446049`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the washer and facing the refrigerator, is the stove to my left, right, or back?
An object is to my back if I would have to turn a
- QA：模型 B vs GT C（错误）
- 类别：refrigerator, stove, washer
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 6.0)'] | 模型 ['(2.0, 5.0)']
- stove：GT ['(6.0, 1.0)'] | 模型 ['(5.0, 8.0)']
- washer：GT ['(7.0, 7.0)'] | 模型 ['(8.0, 5.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 4.0)'] | 模型 []
- stove：GT ['(6.0, 4.0)'] | 模型 []
- washer：GT ['(7.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 4.0)'] | 模型 []
- stove：GT ['(1.0, 4.0)'] | 模型 []
- washer：GT ['(7.0, 2.0)'] | 模型 []

### 样本 37 `scene0144_00`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the lamp and facing the printer, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 
- QA：模型 C vs GT C（正确）
- 类别：door, lamp, printer
- tags：A1_miss, B3_pair
**TOP 视图**（GT → 模型）
- door：GT ['(8.0, 1.0)'] | 模型 ['(1.0, 5.0)']
- lamp：GT ['(5.0, 7.0)'] | 模型 ['(4.0, 3.0)']
- printer：GT ['(2.0, 3.0)', '(2.0, 3.0)'] | 模型 ['(7.0, 5.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(8.0, 3.0)'] | 模型 []
- lamp：GT ['(5.0, 5.0)'] | 模型 []
- printer：GT ['(2.0, 4.0)', '(2.0, 4.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- door：GT ['(1.0, 3.0)'] | 模型 []
- lamp：GT ['(7.0, 5.0)'] | 模型 []
- printer：GT ['(3.0, 4.0)', '(3.0, 4.0)'] | 模型 []

### 样本 38 `f9f95681fd`（scannetpp · object_rel_direction_medium）
- 问题：If I am standing by the door and facing the kettle, is the microwave to my left, right, or back?
An object is to my back if I would have to turn at le
- QA：模型 A vs GT C（错误）
- 类别：door, kettle, microwave
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(1.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- kettle：GT ['(7.0, 3.0)'] | 模型 ['(4.0, 6.0)']
- microwave：GT ['(2.0, 6.0)'] | 模型 ['(3.0, 5.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(1.0, 4.0)'] | 模型 []
- kettle：GT ['(7.0, 3.0)'] | 模型 []
- microwave：GT ['(2.0, 3.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- door：GT ['(3.0, 4.0)'] | 模型 []
- kettle：GT ['(3.0, 3.0)'] | 模型 []
- microwave：GT ['(6.0, 3.0)'] | 模型 []

### 样本 39 `47331668`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the tv and facing the bed, is the chair to my front-left, front-right, back-left, or back-right?
The directions refer to the quadr
- QA：模型 C vs GT A（错误）
- 类别：bed, chair, tv
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(6.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(3.0, 8.0)']
- tv：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 1.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(6.0, 2.0)'] | 模型 []
- chair：GT ['(2.0, 3.0)'] | 模型 []
- tv：GT ['(2.0, 6.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- bed：GT ['(4.0, 2.0)'] | 模型 []
- chair：GT ['(3.0, 3.0)'] | 模型 []
- tv：GT ['(7.0, 6.0)'] | 模型 []

### 样本 40 `42897528`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the washer and facing the refrigerator, is the sofa to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 D vs GT D（正确）
- 类别：refrigerator, sofa, washer
- tags：B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.0, 8.0)']
- sofa：GT ['(5.0, 2.0)'] | 模型 ['(5.0, 5.0)']
- washer：GT ['(1.0, 7.0)'] | 模型 ['(8.0, 2.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 []
- sofa：GT ['(5.0, 2.0)'] | 模型 []
- washer：GT ['(1.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(4.0, 4.0)'] | 模型 []
- sofa：GT ['(2.0, 2.0)'] | 模型 []
- washer：GT ['(7.0, 2.0)'] | 模型 []

### 样本 41 `scene0307_02`（scannet · object_rel_direction_hard）
- 问题：If I am standing by the chair and facing the refrigerator, is the washing machine to my front-left, front-right, back-left, or back-right?
The directi
- QA：模型 A vs GT D（错误）
- 类别：chair, refrigerator, washing machine
- tags：A2_extra, B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 6.0)'] | 模型 ['(4.0, 5.0)', '(5.0, 5.0)']
- refrigerator：GT ['(4.0, 2.0)'] | 模型 ['(2.0, 8.0)']
- washing machine：GT ['(2.0, 7.0)'] | 模型 ['(8.0, 8.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)'] | 模型 []
- refrigerator：GT ['(4.0, 3.0)'] | 模型 []
- washing machine：GT ['(2.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- chair：GT ['(6.0, 2.0)'] | 模型 []
- refrigerator：GT ['(2.0, 3.0)'] | 模型 []
- washing machine：GT ['(7.0, 2.0)'] | 模型 []

### 样本 42 `scene0164_02`（scannet · object_rel_direction_hard）
- 问题：If I am standing by the towel and facing the microwave, is the backpack to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 C vs GT D（错误）
- 类别：backpack, microwave, towel
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- backpack：GT ['(6.0, 1.0)'] | 模型 ['(2.0, 8.0)']
- microwave：GT ['(5.0, 7.0)'] | 模型 ['(3.0, 4.0)']
- towel：GT ['(5.0, 5.0)'] | 模型 ['(6.0, 5.0)']
**FRONT 视图**（GT → 模型）
- backpack：GT ['(6.0, 2.0)'] | 模型 []
- microwave：GT ['(5.0, 5.0)'] | 模型 []
- towel：GT ['(5.0, 3.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- backpack：GT ['(1.0, 2.0)'] | 模型 []
- microwave：GT ['(7.0, 5.0)'] | 模型 []
- towel：GT ['(5.0, 3.0)'] | 模型 []

### 样本 43 `47331668`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the bed and facing the tv, is the chair to my front-left, front-right, back-left, or back-right?
The directions refer to the quadr
- QA：模型 D vs GT B（错误）
- 类别：bed, chair, tv
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(6.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(3.0, 8.0)']
- tv：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 1.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(6.0, 2.0)'] | 模型 []
- chair：GT ['(2.0, 3.0)'] | 模型 []
- tv：GT ['(2.0, 6.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- bed：GT ['(4.0, 2.0)'] | 模型 []
- chair：GT ['(3.0, 3.0)'] | 模型 []
- tv：GT ['(7.0, 6.0)'] | 模型 []

### 样本 44 `c50d2d1d42`（scannetpp · object_rel_direction_hard）
- 问题：If I am standing by the telephone and facing the door, is the whiteboard to my front-left, front-right, back-left, or back-right?
The directions refer
- QA：模型 D vs GT C（错误）
- 类别：door, telephone, whiteboard
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(7.0, 6.0)']
- whiteboard：GT ['(5.0, 7.0)'] | 模型 ['(4.0, 3.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 []
- telephone：GT ['(7.0, 3.0)'] | 模型 []
- whiteboard：GT ['(5.0, 4.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- door：GT ['(3.0, 3.0)'] | 模型 []
- telephone：GT ['(3.0, 3.0)'] | 模型 []
- whiteboard：GT ['(7.0, 4.0)'] | 模型 []

### 样本 45 `47430468`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the stove and facing the stool, is the refrigerator to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 B vs GT D（错误）
- 类别：refrigerator, stool, stove
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(1.0, 5.0)']
- stool：GT ['(3.0, 5.0)'] | 模型 ['(4.0, 8.0)']
- stove：GT ['(1.0, 7.0)'] | 模型 ['(5.0, 4.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 []
- stool：GT ['(3.0, 1.0)'] | 模型 []
- stove：GT ['(1.0, 3.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(4.0, 4.0)'] | 模型 []
- stool：GT ['(5.0, 1.0)'] | 模型 []
- stove：GT ['(7.0, 3.0)'] | 模型 []

### 样本 46 `47334380`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the refrigerator and facing the stove, is the table to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 D vs GT D（正确）
- 类别：refrigerator, stove, table
- tags：B3_pair
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 6.0)'] | 模型 ['(2.0, 4.0)']
- stove：GT ['(2.0, 1.0)'] | 模型 ['(5.0, 3.0)']
- table：GT ['(6.0, 5.0)'] | 模型 ['(5.0, 8.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 4.0)'] | 模型 []
- stove：GT ['(2.0, 4.0)'] | 模型 []
- table：GT ['(6.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 4.0)'] | 模型 []
- stove：GT ['(1.0, 4.0)'] | 模型 []
- table：GT ['(5.0, 2.0)'] | 模型 []

### 样本 47 `7b6477cb95`（scannetpp · object_rel_direction_hard）
- 问题：If I am standing by the telephone and facing the cup, is the trash can to my front-left, front-right, back-left, or back-right?
The directions refer t
- QA：模型 D vs GT A（错误）
- 类别：cup, telephone, trash can
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- cup：GT ['(5.0, 3.0)'] | 模型 ['(3.0, 4.0)']
- telephone：GT ['(6.0, 3.0)'] | 模型 ['(4.0, 5.0)']
- trash can：GT ['(3.0, 7.0)'] | 模型 ['(3.0, 8.0)']
**FRONT 视图**（GT → 模型）
- cup：GT ['(5.0, 2.0)'] | 模型 []
- telephone：GT ['(6.0, 2.0)'] | 模型 []
- trash can：GT ['(3.0, 1.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- cup：GT ['(3.0, 2.0)'] | 模型 []
- telephone：GT ['(3.0, 2.0)'] | 模型 []
- trash can：GT ['(7.0, 1.0)'] | 模型 []

### 样本 48 `47334096`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the stool and facing the tv, is the sofa to my front-left, front-right, back-left, or back-right?
The directions refer to the quad
- QA：模型 A vs GT C（错误）
- 类别：sofa, stool, tv
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- sofa：GT ['(4.0, 4.0)'] | 模型 ['(4.0, 7.0)']
- stool：GT ['(5.0, 1.0)'] | 模型 ['(3.0, 5.0)']
- tv：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 2.0)']
**FRONT 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 []
- stool：GT ['(5.0, 2.0)'] | 模型 []
- tv：GT ['(1.0, 6.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 []
- stool：GT ['(1.0, 2.0)'] | 模型 []
- tv：GT ['(5.0, 6.0)'] | 模型 []

### 样本 49 `47331970`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the dishwasher and facing the refrigerator, is the table to my front-left, front-right, back-left, or back-right?
The directions r
- QA：模型 C vs GT A（错误）
- 类别：dishwasher, refrigerator, table
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- dishwasher：GT ['(1.0, 3.0)'] | 模型 ['(4.0, 5.0)']
- refrigerator：GT ['(3.0, 1.0)'] | 模型 ['(2.0, 3.0)']
- table：GT ['(2.0, 4.0)'] | 模型 ['(7.0, 6.0)']
**FRONT 视图**（GT → 模型）
- dishwasher：GT ['(1.0, 2.0)'] | 模型 []
- refrigerator：GT ['(3.0, 4.0)'] | 模型 []
- table：GT ['(2.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- dishwasher：GT ['(3.0, 2.0)'] | 模型 []
- refrigerator：GT ['(1.0, 4.0)'] | 模型 []
- table：GT ['(4.0, 2.0)'] | 模型 []

### 样本 50 `scene0664_02`（scannet · object_rel_direction_hard）
- 问题：If I am standing by the mirror and facing the door, is the trash bin to my front-left, front-right, back-left, or back-right?
The directions refer to 
- QA：模型 D vs GT D（正确）
- 类别：door, mirror, trash bin
- tags：B3_pair
**TOP 视图**（GT → 模型）
- door：GT ['(4.0, 7.0)'] | 模型 ['(1.0, 5.0)']
- mirror：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 3.0)']
- trash bin：GT ['(3.0, 1.0)'] | 模型 ['(4.0, 8.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(4.0, 4.0)'] | 模型 []
- mirror：GT ['(1.0, 4.0)'] | 模型 []
- trash bin：GT ['(3.0, 1.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- door：GT ['(7.0, 4.0)'] | 模型 []
- mirror：GT ['(5.0, 4.0)'] | 模型 []
- trash bin：GT ['(1.0, 1.0)'] | 模型 []

## Three-view（单次）

### 样本 1 `09c1414f1b`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the cutting board and the suitcase (in meters)?
- QA：模型 0.9 vs GT 1.8（错误）
- 类别：cutting board, suitcase
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- cutting board：GT ['(1.0, 2.0)'] | 模型 ['(5.2, 4.1)']
- suitcase：GT ['(2.0, 4.0)'] | 模型 ['(4.5, 5.5)']
**FRONT 视图**（GT → 模型）
- cutting board：GT ['(1.0, 5.0)'] | 模型 ['(5.2, 6.2)']
- suitcase：GT ['(2.0, 1.0)'] | 模型 ['(4.5, 3.5)']
**SIDE 视图**（GT → 模型）
- cutting board：GT ['(2.0, 5.0)'] | 模型 ['(4.1, 6.2)']
- suitcase：GT ['(4.0, 1.0)'] | 模型 ['(5.5, 3.5)']

### 样本 2 `47334103`（arkitscenes · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the table and the stool (in meters)?
- QA：模型 0.3 vs GT 3.7（错误）
- 类别：stool, table
- tags：A2_extra, B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- stool：GT ['(2.0, 2.0)'] | 模型 ['(4.2, 4.8)', '(5.8, 4.8)']
- table：GT ['(7.0, 1.0)'] | 模型 ['(5.1, 5.3)']
**FRONT 视图**（GT → 模型）
- stool：GT ['(2.0, 1.0)'] | 模型 ['(4.2, 3.2)', '(5.8, 3.2)']
- table：GT ['(7.0, 2.0)'] | 模型 ['(5.1, 4.2)']
**SIDE 视图**（GT → 模型）
- stool：GT ['(2.0, 1.0)'] | 模型 ['(4.8, 3.2)', '(4.8, 3.2)']
- table：GT ['(1.0, 2.0)'] | 模型 ['(5.3, 4.2)']

### 样本 3 `42897538`（arkitscenes · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the stool and the refrigerator (in meters)?
- QA：模型 1.2 vs GT 2.6（错误）
- 类别：refrigerator, stool
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(3.0, 7.0)'] | 模型 ['(3.2, 8.1)']
- stool：GT ['(3.0, 3.0)'] | 模型 ['(4.8, 6.2)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(3.0, 4.0)'] | 模型 ['(3.2, 5.5)']
- stool：GT ['(3.0, 1.0)'] | 模型 ['(4.8, 2.8)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(7.0, 4.0)'] | 模型 ['(8.1, 5.5)']
- stool：GT ['(3.0, 1.0)'] | 模型 ['(6.2, 2.8)']

### 样本 4 `scene0550_00`（scannet · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the door and the window (in meters)?
- QA：模型 3.1 vs GT 2.5（错误）
- 类别：door, window
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(4.0, 8.0)'] | 模型 ['(1.5, 9.1)']
- window：GT ['(5.0, 1.0)'] | 模型 ['(5.0, 9.5)']
**FRONT 视图**（GT → 模型）
- door：GT ['(4.0, 4.0)'] | 模型 ['(1.5, 4.5)']
- window：GT ['(5.0, 5.0)'] | 模型 ['(5.0, 5.5)']
**SIDE 视图**（GT → 模型）
- door：GT ['(8.0, 4.0)'] | 模型 ['(9.1, 4.5)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(9.5, 5.5)']

### 样本 5 `scene0378_01`（scannet · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the door and the clock (in meters)?
- QA：模型 3.5 vs GT 1.6（错误）
- 类别：clock, door
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- clock：GT ['(3.0, 2.0)'] | 模型 ['(5.0, 1.0)']
- door：GT ['(6.0, 1.0)'] | 模型 ['(1.5, 5.0)']
**FRONT 视图**（GT → 模型）
- clock：GT ['(3.0, 7.0)'] | 模型 ['(5.0, 7.5)']
- door：GT ['(6.0, 4.0)'] | 模型 ['(1.5, 4.5)']
**SIDE 视图**（GT → 模型）
- clock：GT ['(2.0, 7.0)'] | 模型 ['(1.0, 7.5)']
- door：GT ['(1.0, 4.0)'] | 模型 ['(5.0, 4.5)']

### 样本 6 `c49a8c6cff`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the trash can and the bed (in meters)?
- QA：模型 1.5 vs GT 0.7（错误）
- 类别：bed, trash can
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(6.0, 5.0)'] | 模型 ['(5.0, 4.5)']
- trash can：GT ['(2.0, 6.0)'] | 模型 ['(2.5, 7.5)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- trash can：GT ['(2.0, 1.0)'] | 模型 ['(2.5, 2.0)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(5.0, 2.0)'] | 模型 ['(4.5, 3.5)']
- trash can：GT ['(6.0, 1.0)'] | 模型 ['(7.5, 2.0)']

### 样本 7 `3db0a1c8f3`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the blanket and the computer mouse (in meters)?
- QA：模型 1.1 vs GT 0.8（错误）
- 类别：blanket, computer mouse
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- blanket：GT ['(1.0, 1.0)'] | 模型 ['(4.8, 5.2)']
- computer mouse：GT ['(3.0, 3.0)'] | 模型 ['(6.2, 3.8)']
**FRONT 视图**（GT → 模型）
- blanket：GT ['(1.0, 2.0)'] | 模型 ['(4.8, 3.8)']
- computer mouse：GT ['(3.0, 2.0)'] | 模型 ['(6.2, 4.2)']
**SIDE 视图**（GT → 模型）
- blanket：GT ['(1.0, 2.0)'] | 模型 ['(5.2, 3.8)']
- computer mouse：GT ['(3.0, 2.0)'] | 模型 ['(3.8, 4.2)']

### 样本 8 `c50d2d1d42`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the door and the telephone (in meters)?
- QA：模型 4.5 vs GT 4.6（错误）
- 类别：door, telephone
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.2, 8.8)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(4.2, 4.8)']
**FRONT 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.2, 5.2)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(4.2, 3.8)']
**SIDE 视图**（GT → 模型）
- door：GT ['(3.0, 3.0)'] | 模型 ['(8.8, 5.2)']
- telephone：GT ['(3.0, 3.0)'] | 模型 ['(4.8, 3.8)']

### 样本 9 `scene0474_04`（scannet · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the table and the trash bin (in meters)?
- QA：模型 0.4 vs GT 1.9（错误）
- 类别：table, trash bin
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- table：GT ['(4.0, 6.0)'] | 模型 ['(5.0, 5.0)']
- trash bin：GT ['(6.0, 3.0)'] | 模型 ['(3.0, 5.0)']
**FRONT 视图**（GT → 模型）
- table：GT ['(4.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- trash bin：GT ['(6.0, 1.0)'] | 模型 ['(3.0, 2.0)']
**SIDE 视图**（GT → 模型）
- table：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- trash bin：GT ['(3.0, 1.0)'] | 模型 ['(5.0, 2.0)']

### 样本 10 `47333899`（arkitscenes · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the table and the stove (in meters)?
- QA：模型 1.5 vs GT 0.9（错误）
- 类别：stove, table
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- stove：GT ['(2.0, 7.0)'] | 模型 ['(3.5, 8.2)']
- table：GT ['(2.0, 1.0)'] | 模型 ['(5.5, 5.5)']
**FRONT 视图**（GT → 模型）
- stove：GT ['(2.0, 4.0)'] | 模型 ['(3.5, 4.5)']
- table：GT ['(2.0, 2.0)'] | 模型 ['(5.5, 3.5)']
**SIDE 视图**（GT → 模型）
- stove：GT ['(7.0, 4.0)'] | 模型 ['(8.2, 4.5)']
- table：GT ['(1.0, 2.0)'] | 模型 ['(5.5, 3.5)']

### 样本 11 `scene0221_01`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (chair, bed, pillow, lamp) is the closest to the microwave?
- QA：模型 A vs GT B（错误）
- 类别：bed, chair, lamp, microwave, pillow
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(4.0, 3.0)', '(2.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- chair：GT ['(3.0, 6.0)', '(1.0, 6.0)', '(2.0, 7.0)'] | 模型 ['(2.5, 7.5)']
- lamp：GT ['(3.0, 1.0)', '(3.0, 0.0)'] | 模型 ['(2.5, 2.5)']
- microwave：GT ['(6.0, 1.0)'] | 模型 []
- pillow：GT ['(2.0, 1.0)', '(4.0, 1.0)', '(4.0, 1.0)', '(4.0, 1.0)', '(2.0, 1.0)'] | 模型 ['(5.0, 2.5)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(4.0, 2.0)', '(2.0, 3.0)'] | 模型 ['(5.0, 3.0)']
- chair：GT ['(3.0, 3.0)', '(1.0, 5.0)', '(2.0, 4.0)'] | 模型 ['(2.5, 3.5)']
- lamp：GT ['(3.0, 4.0)', '(3.0, 5.0)'] | 模型 ['(2.5, 5.0)']
- microwave：GT ['(6.0, 5.0)'] | 模型 []
- pillow：GT ['(2.0, 4.0)', '(4.0, 4.0)', '(4.0, 4.0)', '(4.0, 4.0)', '(2.0, 4.0)'] | 模型 ['(5.0, 4.0)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(3.0, 2.0)', '(3.0, 3.0)'] | 模型 ['(5.0, 3.0)']
- chair：GT ['(6.0, 3.0)', '(6.0, 5.0)', '(7.0, 4.0)'] | 模型 ['(7.5, 3.5)']
- lamp：GT ['(1.0, 4.0)', '(0.0, 5.0)'] | 模型 ['(2.5, 5.0)']
- microwave：GT ['(1.0, 5.0)'] | 模型 []
- pillow：GT ['(1.0, 4.0)', '(1.0, 4.0)', '(1.0, 4.0)', '(1.0, 4.0)', '(1.0, 4.0)'] | 模型 ['(2.5, 4.0)']

### 样本 12 `scene0307_02`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (window, chair, door, washing machine) is the closest to the radiator?
- QA：模型 A vs GT C（错误）
- 类别：chair, door, radiator, washing machine, window
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 6.0)'] | 模型 ['(4.5, 4.5)']
- door：GT ['(3.0, 5.0)', '(4.0, 7.0)', '(3.0, 5.0)', '(1.0, 7.0)', '(7.0, 3.0)'] | 模型 ['(1.5, 2.5)']
- radiator：GT ['(1.0, 5.0)'] | 模型 ['(7.5, 8.5)']
- washing machine：GT ['(2.0, 7.0)'] | 模型 ['(3.5, 6.5)']
- window：GT ['(4.0, 1.0)', '(2.0, 7.0)', '(4.0, 1.0)'] | 模型 ['(5.0, 9.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)'] | 模型 ['(4.5, 3.5)']
- door：GT ['(3.0, 4.0)', '(4.0, 4.0)', '(3.0, 4.0)', '(1.0, 4.0)', '(7.0, 4.0)'] | 模型 ['(1.5, 5.0)']
- radiator：GT ['(1.0, 3.0)'] | 模型 ['(7.5, 4.0)']
- washing machine：GT ['(2.0, 2.0)'] | 模型 ['(3.5, 4.5)']
- window：GT ['(4.0, 6.0)', '(2.0, 6.0)', '(4.0, 6.0)'] | 模型 ['(5.0, 6.5)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(6.0, 2.0)'] | 模型 ['(4.5, 3.5)']
- door：GT ['(5.0, 4.0)', '(7.0, 4.0)', '(5.0, 4.0)', '(7.0, 4.0)', '(3.0, 4.0)'] | 模型 ['(2.5, 5.0)']
- radiator：GT ['(5.0, 3.0)'] | 模型 ['(8.5, 4.0)']
- washing machine：GT ['(7.0, 2.0)'] | 模型 ['(6.5, 4.5)']
- window：GT ['(1.0, 6.0)', '(7.0, 6.0)', '(1.0, 6.0)'] | 模型 ['(9.0, 6.5)']

### 样本 13 `47429977`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (stove, chair, refrigerator, table) is the closest to the tv?
- QA：模型 B vs GT D（错误）
- 类别：chair, refrigerator, stove, table, tv
- tags：A1_miss, A2_extra, B3_pair, B4_scale, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 1.0)', '(3.0, 2.0)', '(3.0, 1.0)'] | 模型 ['(5.0, 6.0)', '(7.0, 6.0)', '(6.0, 5.0)', '(6.0, 7.0)']
- refrigerator：GT ['(2.0, 7.0)'] | 模型 ['(2.0, 3.0)']
- stove：GT ['(1.0, 3.0)'] | 模型 ['(4.0, 2.0)']
- table：GT ['(6.0, 4.0)', '(3.0, 1.0)'] | 模型 ['(6.0, 6.0)']
- tv：GT ['(6.0, 1.0)'] | 模型 ['(8.0, 2.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 3.0)', '(3.0, 3.0)', '(3.0, 3.0)'] | 模型 ['(5.0, 3.0)', '(7.0, 3.0)', '(6.0, 3.0)', '(6.0, 3.0)']
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.0, 6.0)']
- stove：GT ['(1.0, 5.0)'] | 模型 ['(4.0, 4.0)']
- table：GT ['(6.0, 2.0)', '(3.0, 3.0)'] | 模型 ['(6.0, 4.0)']
- tv：GT ['(6.0, 6.0)'] | 模型 ['(8.0, 5.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(1.0, 3.0)', '(2.0, 3.0)', '(1.0, 3.0)'] | 模型 ['(6.0, 3.0)', '(6.0, 3.0)', '(5.0, 3.0)', '(7.0, 3.0)']
- refrigerator：GT ['(7.0, 4.0)'] | 模型 ['(3.0, 6.0)']
- stove：GT ['(3.0, 5.0)'] | 模型 ['(2.0, 4.0)']
- table：GT ['(4.0, 2.0)', '(1.0, 3.0)'] | 模型 ['(6.0, 4.0)']
- tv：GT ['(1.0, 6.0)'] | 模型 ['(2.0, 5.0)']

### 样本 14 `scene0653_00`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (window, monitor, table, keyboard) is the closest to the door?
- QA：模型 D vs GT C（错误）
- 类别：door, keyboard, monitor, table, window
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(7.0, 7.0)'] | 模型 ['(1.5, 8.0)']
- keyboard：GT ['(2.0, 3.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 5.5)']
- monitor：GT ['(1.0, 6.0)', '(2.0, 3.0)', '(2.0, 3.0)', '(6.0, 1.0)', '(7.0, 1.0)', '(6.0, 4.0)', '(6.0, 6.0)'] | 模型 ['(5.0, 4.5)']
- table：GT ['(1.0, 6.0)', '(2.0, 3.0)', '(6.0, 4.0)', '(2.0, 4.0)', '(7.0, 1.0)', '(6.0, 6.0)'] | 模型 ['(5.0, 5.0)']
- window：GT ['(1.0, 5.0)', '(1.0, 2.0)'] | 模型 ['(8.5, 5.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(7.0, 5.0)'] | 模型 ['(1.5, 5.0)']
- keyboard：GT ['(2.0, 2.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 4.2)']
- monitor：GT ['(1.0, 3.0)', '(2.0, 3.0)', '(2.0, 3.0)', '(6.0, 3.0)', '(7.0, 3.0)', '(6.0, 3.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 5.5)']
- table：GT ['(1.0, 2.0)', '(2.0, 2.0)', '(6.0, 2.0)', '(2.0, 1.0)', '(7.0, 2.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- window：GT ['(1.0, 5.0)', '(1.0, 5.0)'] | 模型 ['(8.5, 6.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(7.0, 5.0)'] | 模型 ['(8.0, 5.0)']
- keyboard：GT ['(3.0, 2.0)', '(2.0, 2.0)'] | 模型 ['(5.5, 4.2)']
- monitor：GT ['(6.0, 3.0)', '(3.0, 3.0)', '(3.0, 3.0)', '(1.0, 3.0)', '(1.0, 3.0)', '(4.0, 3.0)', '(6.0, 3.0)'] | 模型 ['(4.5, 5.5)']
- table：GT ['(6.0, 2.0)', '(3.0, 2.0)', '(4.0, 2.0)', '(4.0, 1.0)', '(1.0, 2.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- window：GT ['(5.0, 5.0)', '(2.0, 5.0)'] | 模型 ['(5.0, 6.0)']

### 样本 15 `38d58a7a31`（scannetpp · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (telephone, heater, chair, ceiling light) is the closest to the trash can?
- QA：模型 C vs GT C（正确）
- 类别：ceiling light, chair, heater, telephone, trash can
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing
**TOP 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 1.0)', '(1.0, 2.0)', '(4.0, 6.0)', '(1.0, 3.0)', '(4.0, 5.0)', '(4.0, 3.0)', '(6.0, 1.0)', '(7.0, 6.0)', '(6.0, 4.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- chair：GT ['(1.0, 6.0)', '(3.0, 6.0)', '(4.0, 4.0)', '(5.0, 5.0)', '(6.0, 4.0)', '(2.0, 5.0)', '(2.0, 7.0)', '(5.0, 3.0)', '(4.0, 3.0)', '(4.0, 6.0)', '(6.0, 6.0)', '(6.0, 1.0)', '(1.0, 6.0)', '(6.0, 2.0)', '(3.0, 6.0)', '(4.0, 6.0)', '(1.0, 7.0)', '(2.0, 5.0)', '(5.0, 6.0)', '(3.0, 3.0)', '(5.0, 4.0)', '(6.0, 4.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(7.0, 3.0)', '(7.0, 6.0)', '(6.0, 6.0)', '(3.0, 5.0)', '(2.0, 2.0)', '(3.0, 5.0)', '(2.0, 3.0)', '(1.0, 7.0)', '(1.0, 7.0)', '(1.0, 6.0)', '(1.0, 6.0)', '(1.0, 6.0)'] | 模型 ['(5.5, 4.5)']
- heater：GT ['(7.0, 4.0)', '(8.0, 6.0)', '(7.0, 1.0)'] | 模型 ['(2.0, 8.0)']
- telephone：GT ['(7.0, 2.0)'] | 模型 ['(4.0, 3.5)']
- trash can：GT ['(1.0, 4.0)'] | 模型 ['(6.5, 3.5)']
**FRONT 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 7.0)', '(1.0, 7.0)', '(4.0, 8.0)', '(1.0, 8.0)', '(4.0, 7.0)', '(4.0, 7.0)', '(6.0, 8.0)', '(7.0, 7.0)', '(6.0, 8.0)', '(6.0, 7.0)'] | 模型 ['(5.0, 9.0)']
- chair：GT ['(1.0, 2.0)', '(3.0, 2.0)', '(4.0, 2.0)', '(5.0, 2.0)', '(6.0, 2.0)', '(2.0, 2.0)', '(2.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(4.0, 2.0)', '(6.0, 2.0)', '(6.0, 1.0)', '(1.0, 2.0)', '(6.0, 2.0)', '(3.0, 2.0)', '(4.0, 1.0)', '(1.0, 2.0)', '(2.0, 1.0)', '(5.0, 2.0)', '(3.0, 1.0)', '(5.0, 2.0)', '(6.0, 1.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(7.0, 2.0)', '(7.0, 2.0)', '(6.0, 2.0)', '(3.0, 2.0)', '(2.0, 2.0)', '(3.0, 2.0)', '(2.0, 2.0)', '(1.0, 2.0)', '(1.0, 2.0)', '(1.0, 2.0)', '(1.0, 2.0)', '(1.0, 1.0)'] | 模型 ['(5.5, 3.5)']
- heater：GT ['(7.0, 1.0)', '(8.0, 1.0)', '(7.0, 1.0)'] | 模型 ['(2.0, 3.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(4.0, 5.0)']
- trash can：GT ['(1.0, 1.0)'] | 模型 ['(6.5, 2.0)']
**SIDE 视图**（GT → 模型）
- ceiling light：GT ['(1.0, 7.0)', '(2.0, 7.0)', '(6.0, 8.0)', '(3.0, 8.0)', '(5.0, 7.0)', '(3.0, 7.0)', '(1.0, 8.0)', '(6.0, 7.0)', '(4.0, 8.0)', '(3.0, 7.0)'] | 模型 ['(5.0, 9.0)']
- chair：GT ['(6.0, 2.0)', '(6.0, 2.0)', '(4.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(5.0, 2.0)', '(7.0, 2.0)', '(3.0, 2.0)', '(3.0, 2.0)', '(6.0, 2.0)', '(6.0, 2.0)', '(1.0, 1.0)', '(6.0, 2.0)', '(2.0, 2.0)', '(6.0, 2.0)', '(6.0, 1.0)', '(7.0, 2.0)', '(5.0, 1.0)', '(6.0, 2.0)', '(3.0, 1.0)', '(4.0, 2.0)', '(4.0, 1.0)', '(2.0, 2.0)', '(2.0, 2.0)', '(3.0, 2.0)', '(6.0, 2.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(2.0, 2.0)', '(5.0, 2.0)', '(3.0, 2.0)', '(7.0, 2.0)', '(7.0, 2.0)', '(6.0, 2.0)', '(6.0, 2.0)', '(6.0, 1.0)'] | 模型 ['(4.5, 3.5)']
- heater：GT ['(4.0, 1.0)', '(6.0, 1.0)', '(1.0, 1.0)'] | 模型 ['(8.0, 3.0)']
- telephone：GT ['(2.0, 3.0)'] | 模型 ['(3.5, 5.0)']
- trash can：GT ['(4.0, 1.0)'] | 模型 ['(3.5, 2.0)']

### 样本 16 `42899461`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (chair, sofa, fireplace, stove) is the closest to the tv?
- QA：模型 C vs GT A（错误）
- 类别：chair, fireplace, sofa, stove, tv
- tags：A1_miss, B3_pair, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(7.0, 4.0)', '(7.0, 3.0)', '(2.0, 4.0)', '(1.0, 4.0)'] | 模型 ['(2.0, 4.0)']
- fireplace：GT ['(4.0, 8.0)'] | 模型 ['(5.0, 8.0)']
- sofa：GT ['(7.0, 6.0)'] | 模型 ['(5.0, 4.0)']
- stove：GT ['(1.0, 1.0)'] | 模型 []
- tv：GT ['(1.0, 7.0)'] | 模型 ['(5.0, 8.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(7.0, 3.0)', '(7.0, 3.0)', '(2.0, 4.0)', '(1.0, 4.0)'] | 模型 ['(2.0, 3.0)']
- fireplace：GT ['(4.0, 4.0)'] | 模型 ['(5.0, 4.0)']
- sofa：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 3.0)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
- tv：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 7.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(4.0, 3.0)', '(3.0, 3.0)', '(4.0, 4.0)', '(4.0, 4.0)'] | 模型 ['(4.0, 3.0)']
- fireplace：GT ['(8.0, 4.0)'] | 模型 ['(8.0, 4.0)']
- sofa：GT ['(6.0, 4.0)'] | 模型 ['(4.0, 3.0)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
- tv：GT ['(7.0, 5.0)'] | 模型 ['(8.0, 7.0)']

### 样本 17 `42899461`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (table, tv, sofa, stove) is the closest to the fireplace?
- QA：模型 B vs GT A（错误）
- 类别：fireplace, sofa, stove, table, tv
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- fireplace：GT ['(4.0, 8.0)'] | 模型 ['(5.0, 9.0)']
- sofa：GT ['(7.0, 6.0)'] | 模型 ['(5.0, 3.5)']
- stove：GT ['(1.0, 1.0)'] | 模型 []
- table：GT ['(6.0, 7.0)', '(1.0, 7.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 5.5)']
- tv：GT ['(1.0, 7.0)'] | 模型 ['(5.0, 8.5)']
**FRONT 视图**（GT → 模型）
- fireplace：GT ['(4.0, 4.0)'] | 模型 ['(5.0, 3.0)']
- sofa：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 3.5)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
- table：GT ['(6.0, 2.0)', '(1.0, 2.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 2.5)']
- tv：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 6.5)']
**SIDE 视图**（GT → 模型）
- fireplace：GT ['(8.0, 4.0)'] | 模型 ['(9.0, 3.0)']
- sofa：GT ['(6.0, 4.0)'] | 模型 ['(3.5, 3.5)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
- table：GT ['(7.0, 2.0)', '(7.0, 2.0)', '(3.0, 3.0)'] | 模型 ['(5.5, 2.5)']
- tv：GT ['(7.0, 5.0)'] | 模型 ['(8.5, 6.5)']

### 样本 18 `47430034`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (chair, stool, table, bed) is the closest to the tv?
- QA：模型 D vs GT C（错误）
- 类别：bed, chair, stool, table, tv
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(5.0, 2.0)'] | 模型 ['(5.0, 4.5)']
- chair：GT ['(5.0, 7.0)', '(6.0, 7.0)', '(1.0, 2.0)'] | 模型 ['(2.5, 5.5)']
- stool：GT ['(4.0, 3.0)'] | 模型 []
- table：GT ['(4.0, 3.0)', '(6.0, 7.0)', '(1.0, 2.0)'] | 模型 ['(2.5, 4.0)']
- tv：GT ['(7.0, 7.0)'] | 模型 ['(5.0, 8.5)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(5.0, 4.0)'] | 模型 ['(5.0, 3.0)']
- chair：GT ['(5.0, 3.0)', '(6.0, 3.0)', '(1.0, 2.0)'] | 模型 ['(2.5, 3.5)']
- stool：GT ['(4.0, 1.0)'] | 模型 []
- table：GT ['(4.0, 2.0)', '(6.0, 2.0)', '(1.0, 2.0)'] | 模型 ['(2.5, 3.0)']
- tv：GT ['(7.0, 6.0)'] | 模型 ['(5.0, 5.5)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(2.0, 4.0)'] | 模型 ['(4.5, 3.0)']
- chair：GT ['(7.0, 3.0)', '(7.0, 3.0)', '(2.0, 2.0)'] | 模型 ['(5.5, 3.5)']
- stool：GT ['(3.0, 1.0)'] | 模型 []
- table：GT ['(3.0, 2.0)', '(7.0, 2.0)', '(2.0, 2.0)'] | 模型 ['(4.0, 3.0)']
- tv：GT ['(7.0, 6.0)'] | 模型 ['(8.5, 5.5)']

### 样本 19 `scene0616_01`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (table, trash bin, chair, lamp) is the closest to the window?
- QA：模型 D vs GT A（错误）
- 类别：chair, lamp, table, trash bin, window
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)', '(4.0, 2.0)', '(4.0, 3.0)', '(3.0, 5.0)', '(3.0, 4.0)', '(5.0, 6.0)', '(6.0, 5.0)'] | 模型 ['(5.0, 3.5)']
- lamp：GT ['(5.0, 1.0)'] | 模型 ['(4.0, 5.5)']
- table：GT ['(5.0, 1.0)', '(3.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- trash bin：GT ['(7.0, 4.0)', '(7.0, 4.0)'] | 模型 ['(3.0, 4.5)']
- window：GT ['(1.0, 3.0)'] | 模型 ['(5.0, 9.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)', '(4.0, 2.0)', '(4.0, 2.0)', '(3.0, 2.0)', '(3.0, 2.0)', '(5.0, 2.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- lamp：GT ['(5.0, 4.0)'] | 模型 ['(4.0, 6.0)']
- table：GT ['(5.0, 2.0)', '(3.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- trash bin：GT ['(7.0, 2.0)', '(7.0, 2.0)'] | 模型 ['(3.0, 2.0)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 7.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(2.0, 2.0)', '(2.0, 2.0)', '(3.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(6.0, 2.0)', '(5.0, 2.0)'] | 模型 ['(3.5, 3.5)']
- lamp：GT ['(1.0, 4.0)'] | 模型 ['(5.5, 6.0)']
- table：GT ['(1.0, 2.0)', '(3.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- trash bin：GT ['(4.0, 2.0)', '(4.0, 2.0)'] | 模型 ['(4.5, 2.0)']
- window：GT ['(3.0, 5.0)'] | 模型 ['(9.0, 7.0)']

### 样本 20 `scene0651_02`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (counter, chair, table, trash bin) is the closest to the sofa?
- QA：模型 C vs GT C（正确）
- 类别：chair, counter, sofa, table, trash bin
- tags：A1_miss, B3_pair, B5_adjacent, C7_missing, C8_height
**TOP 视图**（GT → 模型）
- chair：GT ['(7.0, 4.0)', '(5.0, 3.0)', '(5.0, 4.0)', '(6.0, 3.0)'] | 模型 ['(3.0, 5.0)']
- counter：GT ['(3.0, 6.0)'] | 模型 []
- sofa：GT ['(5.0, 1.0)'] | 模型 ['(5.0, 3.0)']
- table：GT ['(3.0, 2.0)', '(5.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- trash bin：GT ['(1.0, 6.0)'] | 模型 ['(2.0, 8.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(7.0, 2.0)', '(5.0, 3.0)', '(5.0, 3.0)', '(6.0, 3.0)'] | 模型 ['(3.0, 4.0)']
- counter：GT ['(3.0, 5.0)'] | 模型 []
- sofa：GT ['(5.0, 3.0)'] | 模型 ['(5.0, 4.0)']
- table：GT ['(3.0, 1.0)', '(5.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- trash bin：GT ['(1.0, 1.0)'] | 模型 ['(2.0, 2.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)', '(3.0, 3.0)', '(4.0, 3.0)', '(3.0, 3.0)'] | 模型 ['(5.0, 4.0)']
- counter：GT ['(6.0, 5.0)'] | 模型 []
- sofa：GT ['(1.0, 3.0)'] | 模型 ['(3.0, 4.0)']
- table：GT ['(2.0, 1.0)', '(3.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- trash bin：GT ['(6.0, 1.0)'] | 模型 ['(8.0, 2.0)']

### 样本 21 `31a2c91c43`（scannetpp · object_rel_direction_easy）
- 问题：If I am standing by the ceiling light and facing the toilet, is the door to the left or the right of the toilet?
- QA：模型 A vs GT A（正确）
- 类别：ceiling light, door, toilet
- tags：B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- ceiling light：GT ['(5.0, 8.0)'] | 模型 ['(5.0, 5.0)']
- door：GT ['(2.0, 4.0)'] | 模型 ['(1.0, 5.0)']
- toilet：GT ['(6.0, 2.0)'] | 模型 ['(4.0, 4.0)']
**FRONT 视图**（GT → 模型）
- ceiling light：GT ['(5.0, 8.0)'] | 模型 ['(5.0, 9.0)']
- door：GT ['(2.0, 4.0)'] | 模型 ['(1.0, 5.0)']
- toilet：GT ['(6.0, 1.0)'] | 模型 ['(4.0, 2.0)']
**SIDE 视图**（GT → 模型）
- ceiling light：GT ['(8.0, 8.0)'] | 模型 ['(5.0, 9.0)']
- door：GT ['(4.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- toilet：GT ['(2.0, 1.0)'] | 模型 ['(4.0, 2.0)']

### 样本 22 `scene0353_00`（scannet · object_rel_direction_easy）
- 问题：If I am standing by the bookshelf and facing the door, is the refrigerator to the left or the right of the door?
- QA：模型 A vs GT A（正确）
- 类别：bookshelf, door, refrigerator
- tags：B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- bookshelf：GT ['(7.0, 1.0)'] | 模型 ['(7.5, 4.5)']
- door：GT ['(7.0, 3.0)'] | 模型 ['(1.5, 5.0)']
- refrigerator：GT ['(5.0, 5.0)'] | 模型 ['(3.5, 7.5)']
**FRONT 视图**（GT → 模型）
- bookshelf：GT ['(7.0, 3.0)'] | 模型 ['(7.5, 5.0)']
- door：GT ['(7.0, 4.0)'] | 模型 ['(1.5, 5.5)']
- refrigerator：GT ['(5.0, 2.0)'] | 模型 ['(3.5, 4.5)']
**SIDE 视图**（GT → 模型）
- bookshelf：GT ['(1.0, 3.0)'] | 模型 ['(4.5, 5.0)']
- door：GT ['(3.0, 4.0)'] | 模型 ['(5.0, 5.5)']
- refrigerator：GT ['(5.0, 2.0)'] | 模型 ['(7.5, 4.5)']

### 样本 23 `41159525`（arkitscenes · object_rel_direction_easy）
- 问题：If I am standing by the stove and facing the table, is the refrigerator to the left or the right of the table?
- QA：模型 A vs GT B（错误）
- 类别：refrigerator, stove, table
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 1.0)'] | 模型 ['(1.5, 3.8)']
- stove：GT ['(1.0, 1.0)'] | 模型 ['(4.3, 3.8)']
- table：GT ['(6.0, 5.0)'] | 模型 ['(4.9, 7.8)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 4.0)'] | 模型 ['(1.5, 5.8)']
- stove：GT ['(1.0, 4.0)'] | 模型 ['(4.3, 4.3)']
- table：GT ['(6.0, 2.0)'] | 模型 ['(4.9, 3.4)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 4.0)'] | 模型 ['(3.8, 5.8)']
- stove：GT ['(1.0, 4.0)'] | 模型 ['(3.8, 4.3)']
- table：GT ['(5.0, 2.0)'] | 模型 ['(7.8, 3.4)']

### 样本 24 `d755b3d9d8`（scannetpp · object_rel_direction_easy）
- 问题：If I am standing by the cup and facing the whiteboard, is the shoes to the left or the right of the whiteboard?
- QA：模型 B vs GT A（错误）
- 类别：cup, shoes, whiteboard
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- cup：GT ['(5.0, 1.0)'] | 模型 ['(5.0, 5.0)']
- shoes：GT ['(7.0, 4.0)'] | 模型 ['(4.0, 7.0)']
- whiteboard：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 2.0)']
**FRONT 视图**（GT → 模型）
- cup：GT ['(5.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- shoes：GT ['(7.0, 0.0)'] | 模型 ['(4.0, 1.0)']
- whiteboard：GT ['(2.0, 4.0)'] | 模型 ['(5.0, 6.0)']
**SIDE 视图**（GT → 模型）
- cup：GT ['(1.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- shoes：GT ['(4.0, 0.0)'] | 模型 ['(7.0, 1.0)']
- whiteboard：GT ['(7.0, 4.0)'] | 模型 ['(2.0, 6.0)']

### 样本 25 `47204578`（arkitscenes · object_rel_direction_easy）
- 问题：If I am standing by the tv and facing the table, is the stool to the left or the right of the table?
- QA：模型 B vs GT A（错误）
- 类别：stool, table, tv
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- stool：GT ['(1.0, 1.0)'] | 模型 ['(3.5, 5.0)']
- table：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 8.0)']
- tv：GT ['(3.0, 1.0)'] | 模型 ['(5.0, 8.5)']
**FRONT 视图**（GT → 模型）
- stool：GT ['(1.0, 1.0)'] | 模型 ['(3.5, 2.5)']
- table：GT ['(2.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- tv：GT ['(3.0, 6.0)'] | 模型 ['(5.0, 6.0)']
**SIDE 视图**（GT → 模型）
- stool：GT ['(1.0, 1.0)'] | 模型 ['(5.0, 2.5)']
- table：GT ['(7.0, 2.0)'] | 模型 ['(8.0, 3.5)']
- tv：GT ['(1.0, 6.0)'] | 模型 ['(8.5, 6.0)']

### 样本 26 `scene0458_00`（scannet · object_rel_direction_easy）
- 问题：If I am standing by the window and facing the door, is the mirror to the left or the right of the door?
- QA：模型 A vs GT B（错误）
- 类别：door, mirror, window
- tags：B3_pair, B4_scale, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(8.0, 6.0)'] | 模型 ['(2.0, 1.5)']
- mirror：GT ['(1.0, 6.0)'] | 模型 ['(5.0, 3.5)']
- window：GT ['(6.0, 1.0)'] | 模型 ['(8.0, 5.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(8.0, 5.0)'] | 模型 ['(2.0, 5.0)']
- mirror：GT ['(1.0, 4.0)'] | 模型 ['(5.0, 6.0)']
- window：GT ['(6.0, 5.0)'] | 模型 ['(8.0, 6.5)']
**SIDE 视图**（GT → 模型）
- door：GT ['(6.0, 5.0)'] | 模型 ['(1.5, 5.0)']
- mirror：GT ['(6.0, 4.0)'] | 模型 ['(3.5, 6.0)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 6.5)']

### 样本 27 `scene0426_00`（scannet · object_rel_direction_easy）
- 问题：If I am standing by the tv and facing the lamp, is the table to the left or the right of the lamp?
- QA：模型 B vs GT A（错误）
- 类别：lamp, table, tv
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- lamp：GT ['(5.0, 1.0)'] | 模型 ['(5.0, 5.0)']
- table：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 5.0)']
- tv：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 5.0)']
**FRONT 视图**（GT → 模型）
- lamp：GT ['(5.0, 4.0)'] | 模型 ['(5.0, 7.0)']
- table：GT ['(2.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- tv：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 5.0)']
**SIDE 视图**（GT → 模型）
- lamp：GT ['(1.0, 4.0)'] | 模型 ['(5.0, 7.0)']
- table：GT ['(7.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- tv：GT ['(3.0, 4.0)'] | 模型 ['(5.0, 5.0)']

### 样本 28 `scene0144_00`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the window and facing the lamp, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 1
- QA：模型 None vs GT C（错误）
- 类别：door, lamp, window
- tags：B3_pair, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(8.0, 1.0)'] | 模型 ['(1.5, 5.0)']
- lamp：GT ['(5.0, 7.0)'] | 模型 ['(5.0, 5.0)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(8.5, 5.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(8.0, 3.0)'] | 模型 ['(1.5, 4.5)']
- lamp：GT ['(5.0, 5.0)'] | 模型 ['(5.0, 8.5)']
- window：GT ['(1.0, 6.0)'] | 模型 ['(8.5, 5.5)']
**SIDE 视图**（GT → 模型）
- door：GT ['(1.0, 3.0)'] | 模型 ['(5.0, 4.5)']
- lamp：GT ['(7.0, 5.0)'] | 模型 ['(5.0, 8.5)']
- window：GT ['(5.0, 6.0)'] | 模型 ['(5.0, 5.5)']

### 样本 29 `scene0629_01`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the bed and facing the chair, is the mirror to my left, right, or back?
An object is to my back if I would have to turn at least 1
- QA：模型 B vs GT B（正确）
- 类别：bed, chair, mirror
- tags：QA_map_clean
**TOP 视图**（GT → 模型）
- bed：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 4.5)']
- chair：GT ['(6.0, 7.0)'] | 模型 ['(2.5, 6.0)']
- mirror：GT ['(3.0, 6.0)'] | 模型 ['(1.5, 4.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 3.5)']
- chair：GT ['(6.0, 2.0)'] | 模型 ['(2.5, 3.0)']
- mirror：GT ['(3.0, 4.0)'] | 模型 ['(1.5, 6.5)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(4.0, 3.0)'] | 模型 ['(4.5, 3.5)']
- chair：GT ['(7.0, 2.0)'] | 模型 ['(6.0, 3.0)']
- mirror：GT ['(6.0, 4.0)'] | 模型 ['(4.0, 6.5)']

### 样本 30 `5ee7c22ba0`（scannetpp · object_rel_direction_medium）
- 问题：If I am standing by the refrigerator and facing the microwave, is the ceiling light to my left, right, or back?
An object is to my back if I would hav
- QA：模型 A vs GT B（错误）
- 类别：ceiling light, microwave, refrigerator
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- microwave：GT ['(3.0, 1.0)'] | 模型 ['(5.2, 8.2)']
- refrigerator：GT ['(4.0, 7.0)'] | 模型 ['(2.8, 7.8)']
**FRONT 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 8.0)'] | 模型 ['(5.0, 9.2)']
- microwave：GT ['(3.0, 3.0)'] | 模型 ['(5.2, 5.8)']
- refrigerator：GT ['(4.0, 2.0)'] | 模型 ['(2.8, 4.5)']
**SIDE 视图**（GT → 模型）
- ceiling light：GT ['(3.0, 8.0)'] | 模型 ['(5.0, 9.2)']
- microwave：GT ['(1.0, 3.0)'] | 模型 ['(8.2, 5.8)']
- refrigerator：GT ['(7.0, 2.0)'] | 模型 ['(7.8, 4.5)']

### 样本 31 `45261121`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the table and facing the tv, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 135
- QA：模型 B vs GT A（错误）
- 类别：stove, table, tv
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- stove：GT ['(3.0, 2.0)'] | 模型 ['(2.5, 3.5)']
- table：GT ['(5.0, 4.0)'] | 模型 ['(5.2, 5.5)']
- tv：GT ['(7.0, 1.0)'] | 模型 ['(5.2, 8.2)']
**FRONT 视图**（GT → 模型）
- stove：GT ['(3.0, 3.0)'] | 模型 ['(2.5, 4.2)']
- table：GT ['(5.0, 2.0)'] | 模型 ['(5.2, 3.8)']
- tv：GT ['(7.0, 7.0)'] | 模型 ['(5.2, 6.5)']
**SIDE 视图**（GT → 模型）
- stove：GT ['(2.0, 3.0)'] | 模型 ['(3.5, 4.2)']
- table：GT ['(4.0, 2.0)'] | 模型 ['(5.5, 3.8)']
- tv：GT ['(1.0, 7.0)'] | 模型 ['(8.2, 6.5)']

### 样本 32 `45b0dac5e3`（scannetpp · object_rel_direction_medium）
- 问题：If I am standing by the cup and facing the heater, is the toilet to my left, right, or back?
An object is to my back if I would have to turn at least 
- QA：模型 C vs GT C（正确）
- 类别：cup, heater, toilet
- tags：B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- cup：GT ['(6.0, 1.0)'] | 模型 ['(3.5, 4.5)']
- heater：GT ['(0.0, 5.0)'] | 模型 ['(1.5, 5.0)']
- toilet：GT ['(7.0, 6.0)'] | 模型 ['(4.5, 6.5)']
**FRONT 视图**（GT → 模型）
- cup：GT ['(6.0, 3.0)'] | 模型 ['(3.5, 5.0)']
- heater：GT ['(0.0, 3.0)'] | 模型 ['(1.5, 6.0)']
- toilet：GT ['(7.0, 2.0)'] | 模型 ['(4.5, 3.5)']
**SIDE 视图**（GT → 模型）
- cup：GT ['(1.0, 3.0)'] | 模型 ['(4.5, 5.0)']
- heater：GT ['(5.0, 3.0)'] | 模型 ['(5.0, 6.0)']
- toilet：GT ['(6.0, 2.0)'] | 模型 ['(6.5, 3.5)']

### 样本 33 `scene0695_00`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the lamp and facing the pillow, is the table to my left, right, or back?
An object is to my back if I would have to turn at least 
- QA：模型 C vs GT C（正确）
- 类别：lamp, pillow, table
- tags：B3_pair
**TOP 视图**（GT → 模型）
- lamp：GT ['(5.0, 1.0)'] | 模型 ['(5.0, 4.0)']
- pillow：GT ['(1.0, 2.0)'] | 模型 ['(3.0, 6.0)']
- table：GT ['(3.0, 7.0)'] | 模型 ['(5.0, 4.0)']
**FRONT 视图**（GT → 模型）
- lamp：GT ['(5.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- pillow：GT ['(1.0, 4.0)'] | 模型 ['(3.0, 4.0)']
- table：GT ['(3.0, 2.0)'] | 模型 ['(5.0, 3.0)']
**SIDE 视图**（GT → 模型）
- lamp：GT ['(1.0, 4.0)'] | 模型 ['(4.0, 5.0)']
- pillow：GT ['(2.0, 4.0)'] | 模型 ['(6.0, 4.0)']
- table：GT ['(7.0, 2.0)'] | 模型 ['(4.0, 3.0)']

### 样本 34 `47334096`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the stool and facing the sofa, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 1
- QA：模型 B vs GT C（错误）
- 类别：sofa, stool, stove
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- sofa：GT ['(4.0, 4.0)'] | 模型 ['(5.2, 4.1)']
- stool：GT ['(5.0, 1.0)'] | 模型 ['(3.5, 5.2)']
- stove：GT ['(7.0, 6.0)'] | 模型 ['(8.1, 7.5)']
**FRONT 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 ['(5.2, 3.8)']
- stool：GT ['(5.0, 2.0)'] | 模型 ['(3.5, 2.8)']
- stove：GT ['(7.0, 5.0)'] | 模型 ['(8.1, 4.5)']
**SIDE 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 ['(4.1, 3.8)']
- stool：GT ['(1.0, 2.0)'] | 模型 ['(5.2, 2.8)']
- stove：GT ['(6.0, 5.0)'] | 模型 ['(7.5, 4.5)']

### 样本 35 `42446103`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the stove and facing the tv, is the stool to my left, right, or back?
An object is to my back if I would have to turn at least 135
- QA：模型 A vs GT A（正确）
- 类别：stool, stove, tv
- tags：B3_pair
**TOP 视图**（GT → 模型）
- stool：GT ['(3.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- stove：GT ['(3.0, 7.0)'] | 模型 ['(3.0, 8.0)']
- tv：GT ['(8.0, 2.0)'] | 模型 ['(8.0, 3.0)']
**FRONT 视图**（GT → 模型）
- stool：GT ['(3.0, 1.0)'] | 模型 ['(5.0, 3.0)']
- stove：GT ['(3.0, 4.0)'] | 模型 ['(3.0, 4.0)']
- tv：GT ['(8.0, 7.0)'] | 模型 ['(8.0, 6.0)']
**SIDE 视图**（GT → 模型）
- stool：GT ['(3.0, 1.0)'] | 模型 ['(5.0, 3.0)']
- stove：GT ['(7.0, 4.0)'] | 模型 ['(8.0, 4.0)']
- tv：GT ['(2.0, 7.0)'] | 模型 ['(3.0, 6.0)']

### 样本 36 `42446049`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the washer and facing the refrigerator, is the stove to my left, right, or back?
An object is to my back if I would have to turn a
- QA：模型 C vs GT C（正确）
- 类别：refrigerator, stove, washer
- tags：B3_pair, B4_scale, C8_height
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 6.0)'] | 模型 ['(2.5, 4.5)']
- stove：GT ['(6.0, 1.0)'] | 模型 ['(5.5, 3.5)']
- washer：GT ['(7.0, 7.0)'] | 模型 ['(8.0, 4.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 4.0)'] | 模型 ['(2.5, 5.5)']
- stove：GT ['(6.0, 4.0)'] | 模型 ['(5.5, 3.5)']
- washer：GT ['(7.0, 2.0)'] | 模型 ['(8.0, 3.5)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 4.0)'] | 模型 ['(4.5, 5.5)']
- stove：GT ['(1.0, 4.0)'] | 模型 ['(3.5, 3.5)']
- washer：GT ['(7.0, 2.0)'] | 模型 ['(4.0, 3.5)']

### 样本 37 `scene0144_00`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the lamp and facing the printer, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 
- QA：模型 C vs GT C（正确）
- 类别：door, lamp, printer
- tags：A1_miss, B3_pair, B4_scale, C7_missing, C8_height
**TOP 视图**（GT → 模型）
- door：GT ['(8.0, 1.0)'] | 模型 ['(1.2, 8.5)']
- lamp：GT ['(5.0, 7.0)'] | 模型 ['(3.8, 4.2)']
- printer：GT ['(2.0, 3.0)', '(2.0, 3.0)'] | 模型 ['(4.1, 4.8)']
**FRONT 视图**（GT → 模型）
- door：GT ['(8.0, 3.0)'] | 模型 ['(1.2, 5.0)']
- lamp：GT ['(5.0, 5.0)'] | 模型 ['(3.8, 5.2)']
- printer：GT ['(2.0, 4.0)', '(2.0, 4.0)'] | 模型 ['(4.1, 3.8)']
**SIDE 视图**（GT → 模型）
- door：GT ['(1.0, 3.0)'] | 模型 ['(8.5, 5.0)']
- lamp：GT ['(7.0, 5.0)'] | 模型 ['(4.2, 5.2)']
- printer：GT ['(3.0, 4.0)', '(3.0, 4.0)'] | 模型 ['(4.8, 3.8)']

### 样本 38 `f9f95681fd`（scannetpp · object_rel_direction_medium）
- 问题：If I am standing by the door and facing the kettle, is the microwave to my left, right, or back?
An object is to my back if I would have to turn at le
- QA：模型 A vs GT C（错误）
- 类别：door, kettle, microwave
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(1.0, 3.0)'] | 模型 ['(1.5, 8.5)']
- kettle：GT ['(7.0, 3.0)'] | 模型 ['(6.5, 4.0)']
- microwave：GT ['(2.0, 6.0)'] | 模型 ['(5.5, 4.5)']
**FRONT 视图**（GT → 模型）
- door：GT ['(1.0, 4.0)'] | 模型 ['(1.5, 5.0)']
- kettle：GT ['(7.0, 3.0)'] | 模型 ['(6.5, 4.0)']
- microwave：GT ['(2.0, 3.0)'] | 模型 ['(5.5, 4.5)']
**SIDE 视图**（GT → 模型）
- door：GT ['(3.0, 4.0)'] | 模型 ['(8.5, 5.0)']
- kettle：GT ['(3.0, 3.0)'] | 模型 ['(4.0, 4.0)']
- microwave：GT ['(6.0, 3.0)'] | 模型 ['(4.5, 4.5)']

### 样本 39 `47331668`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the tv and facing the bed, is the chair to my front-left, front-right, back-left, or back-right?
The directions refer to the quadr
- QA：模型 A vs GT A（正确）
- 类别：bed, chair, tv
- tags：B3_pair
**TOP 视图**（GT → 模型）
- bed：GT ['(6.0, 4.0)'] | 模型 ['(5.0, 4.5)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(2.5, 7.5)']
- tv：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 8.5)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(2.5, 4.0)']
- tv：GT ['(2.0, 6.0)'] | 模型 ['(5.0, 6.0)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(4.0, 2.0)'] | 模型 ['(4.5, 3.5)']
- chair：GT ['(3.0, 3.0)'] | 模型 ['(7.5, 4.0)']
- tv：GT ['(7.0, 6.0)'] | 模型 ['(8.5, 6.0)']

### 样本 40 `42897528`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the washer and facing the refrigerator, is the sofa to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 D vs GT D（正确）
- 类别：refrigerator, sofa, washer
- tags：B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.0, 8.0)']
- sofa：GT ['(5.0, 2.0)'] | 模型 ['(5.5, 3.5)']
- washer：GT ['(1.0, 7.0)'] | 模型 ['(8.0, 8.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.0, 6.0)']
- sofa：GT ['(5.0, 2.0)'] | 模型 ['(5.5, 4.0)']
- washer：GT ['(1.0, 2.0)'] | 模型 ['(8.0, 4.5)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(4.0, 4.0)'] | 模型 ['(8.0, 6.0)']
- sofa：GT ['(2.0, 2.0)'] | 模型 ['(3.5, 4.0)']
- washer：GT ['(7.0, 2.0)'] | 模型 ['(8.0, 4.5)']

### 样本 41 `scene0307_02`（scannet · object_rel_direction_hard）
- 问题：If I am standing by the chair and facing the refrigerator, is the washing machine to my front-left, front-right, back-left, or back-right?
The directi
- QA：模型 C vs GT D（错误）
- 类别：chair, refrigerator, washing machine
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 6.0)'] | 模型 ['(5.5, 4.5)']
- refrigerator：GT ['(4.0, 2.0)'] | 模型 ['(2.5, 8.5)']
- washing machine：GT ['(2.0, 7.0)'] | 模型 ['(1.5, 7.5)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)'] | 模型 ['(5.5, 3.5)']
- refrigerator：GT ['(4.0, 3.0)'] | 模型 ['(2.5, 5.5)']
- washing machine：GT ['(2.0, 2.0)'] | 模型 ['(1.5, 4.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(6.0, 2.0)'] | 模型 ['(4.5, 3.5)']
- refrigerator：GT ['(2.0, 3.0)'] | 模型 ['(8.5, 5.5)']
- washing machine：GT ['(7.0, 2.0)'] | 模型 ['(7.5, 4.0)']

### 样本 42 `scene0164_02`（scannet · object_rel_direction_hard）
- 问题：If I am standing by the towel and facing the microwave, is the backpack to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 B vs GT D（错误）
- 类别：backpack, microwave, towel
- tags：B3_pair, B4_scale, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- backpack：GT ['(6.0, 1.0)'] | 模型 ['(6.5, 4.5)']
- microwave：GT ['(5.0, 7.0)'] | 模型 ['(3.5, 7.5)']
- towel：GT ['(5.0, 5.0)'] | 模型 ['(3.2, 7.0)']
**FRONT 视图**（GT → 模型）
- backpack：GT ['(6.0, 2.0)'] | 模型 ['(6.5, 2.5)']
- microwave：GT ['(5.0, 5.0)'] | 模型 ['(3.5, 5.5)']
- towel：GT ['(5.0, 3.0)'] | 模型 ['(3.2, 6.5)']
**SIDE 视图**（GT → 模型）
- backpack：GT ['(1.0, 2.0)'] | 模型 ['(4.5, 2.5)']
- microwave：GT ['(7.0, 5.0)'] | 模型 ['(7.5, 5.5)']
- towel：GT ['(5.0, 3.0)'] | 模型 ['(7.0, 6.5)']

### 样本 43 `47331668`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the bed and facing the tv, is the chair to my front-left, front-right, back-left, or back-right?
The directions refer to the quadr
- QA：模型 B vs GT B（正确）
- 类别：bed, chair, tv
- tags：C8_height
**TOP 视图**（GT → 模型）
- bed：GT ['(6.0, 4.0)'] | 模型 ['(5.0, 4.5)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(2.5, 6.5)']
- tv：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 8.5)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(2.5, 3.0)']
- tv：GT ['(2.0, 6.0)'] | 模型 ['(5.0, 5.5)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(4.0, 2.0)'] | 模型 ['(4.5, 3.5)']
- chair：GT ['(3.0, 3.0)'] | 模型 ['(6.5, 3.0)']
- tv：GT ['(7.0, 6.0)'] | 模型 ['(8.5, 5.5)']

### 样本 44 `c50d2d1d42`（scannetpp · object_rel_direction_hard）
- 问题：If I am standing by the telephone and facing the door, is the whiteboard to my front-left, front-right, back-left, or back-right?
The directions refer
- QA：模型 C vs GT C（正确）
- 类别：door, telephone, whiteboard
- tags：B3_pair
**TOP 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.5, 9.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(4.5, 4.0)']
- whiteboard：GT ['(5.0, 7.0)'] | 模型 ['(5.0, 8.5)']
**FRONT 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.5, 5.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(4.5, 3.5)']
- whiteboard：GT ['(5.0, 4.0)'] | 模型 ['(5.0, 6.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(3.0, 3.0)'] | 模型 ['(9.0, 5.0)']
- telephone：GT ['(3.0, 3.0)'] | 模型 ['(4.0, 3.5)']
- whiteboard：GT ['(7.0, 4.0)'] | 模型 ['(8.5, 6.0)']

### 样本 45 `47430468`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the stove and facing the stool, is the refrigerator to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 C vs GT D（错误）
- 类别：refrigerator, stool, stove
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.5, 8.5)']
- stool：GT ['(3.0, 5.0)'] | 模型 ['(4.5, 4.5)']
- stove：GT ['(1.0, 7.0)'] | 模型 ['(5.0, 7.5)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.5, 5.5)']
- stool：GT ['(3.0, 1.0)'] | 模型 ['(4.5, 2.5)']
- stove：GT ['(1.0, 3.0)'] | 模型 ['(5.0, 4.0)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(4.0, 4.0)'] | 模型 ['(8.5, 5.5)']
- stool：GT ['(5.0, 1.0)'] | 模型 ['(4.5, 2.5)']
- stove：GT ['(7.0, 3.0)'] | 模型 ['(7.5, 4.0)']

### 样本 46 `47334380`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the refrigerator and facing the stove, is the table to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 D vs GT D（正确）
- 类别：refrigerator, stove, table
- tags：B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 6.0)'] | 模型 ['(1.5, 3.5)']
- stove：GT ['(2.0, 1.0)'] | 模型 ['(3.5, 3.5)']
- table：GT ['(6.0, 5.0)'] | 模型 ['(6.5, 6.5)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 4.0)'] | 模型 ['(1.5, 6.0)']
- stove：GT ['(2.0, 4.0)'] | 模型 ['(3.5, 4.5)']
- table：GT ['(6.0, 2.0)'] | 模型 ['(6.5, 3.5)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 4.0)'] | 模型 ['(3.5, 6.0)']
- stove：GT ['(1.0, 4.0)'] | 模型 ['(3.5, 4.5)']
- table：GT ['(5.0, 2.0)'] | 模型 ['(6.5, 3.5)']

### 样本 47 `7b6477cb95`（scannetpp · object_rel_direction_hard）
- 问题：If I am standing by the telephone and facing the cup, is the trash can to my front-left, front-right, back-left, or back-right?
The directions refer t
- QA：模型 D vs GT A（错误）
- 类别：cup, telephone, trash can
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- cup：GT ['(5.0, 3.0)'] | 模型 ['(4.8, 4.2)']
- telephone：GT ['(6.0, 3.0)'] | 模型 ['(3.5, 4.5)']
- trash can：GT ['(3.0, 7.0)'] | 模型 ['(3.2, 3.8)']
**FRONT 视图**（GT → 模型）
- cup：GT ['(5.0, 2.0)'] | 模型 ['(4.8, 5.2)']
- telephone：GT ['(6.0, 2.0)'] | 模型 ['(3.5, 5.5)']
- trash can：GT ['(3.0, 1.0)'] | 模型 ['(3.2, 2.5)']
**SIDE 视图**（GT → 模型）
- cup：GT ['(3.0, 2.0)'] | 模型 ['(4.2, 5.2)']
- telephone：GT ['(3.0, 2.0)'] | 模型 ['(4.5, 5.5)']
- trash can：GT ['(7.0, 1.0)'] | 模型 ['(3.8, 2.5)']

### 样本 48 `47334096`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the stool and facing the tv, is the sofa to my front-left, front-right, back-left, or back-right?
The directions refer to the quad
- QA：模型 B vs GT C（错误）
- 类别：sofa, stool, tv
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- sofa：GT ['(4.0, 4.0)'] | 模型 ['(5.0, 3.5)']
- stool：GT ['(5.0, 1.0)'] | 模型 ['(3.5, 6.0)']
- tv：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 8.5)']
**FRONT 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 ['(5.0, 4.5)']
- stool：GT ['(5.0, 2.0)'] | 模型 ['(3.5, 3.0)']
- tv：GT ['(1.0, 6.0)'] | 模型 ['(5.0, 6.5)']
**SIDE 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 ['(3.5, 4.5)']
- stool：GT ['(1.0, 2.0)'] | 模型 ['(6.0, 3.0)']
- tv：GT ['(5.0, 6.0)'] | 模型 ['(8.5, 6.5)']

### 样本 49 `47331970`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the dishwasher and facing the refrigerator, is the table to my front-left, front-right, back-left, or back-right?
The directions r
- QA：模型 B vs GT A（错误）
- 类别：dishwasher, refrigerator, table
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- dishwasher：GT ['(1.0, 3.0)'] | 模型 ['(3.5, 2.5)']
- refrigerator：GT ['(3.0, 1.0)'] | 模型 ['(1.5, 2.5)']
- table：GT ['(2.0, 4.0)'] | 模型 ['(6.0, 6.0)']
**FRONT 视图**（GT → 模型）
- dishwasher：GT ['(1.0, 2.0)'] | 模型 ['(3.5, 3.5)']
- refrigerator：GT ['(3.0, 4.0)'] | 模型 ['(1.5, 5.5)']
- table：GT ['(2.0, 2.0)'] | 模型 ['(6.0, 3.0)']
**SIDE 视图**（GT → 模型）
- dishwasher：GT ['(3.0, 2.0)'] | 模型 ['(2.5, 3.5)']
- refrigerator：GT ['(1.0, 4.0)'] | 模型 ['(2.5, 5.5)']
- table：GT ['(4.0, 2.0)'] | 模型 ['(6.0, 3.0)']

### 样本 50 `scene0664_02`（scannet · object_rel_direction_hard）
- 问题：If I am standing by the mirror and facing the door, is the trash bin to my front-left, front-right, back-left, or back-right?
The directions refer to 
- QA：模型 C vs GT D（错误）
- 类别：door, mirror, trash bin
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(4.0, 7.0)'] | 模型 ['(1.5, 8.0)']
- mirror：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 2.5)']
- trash bin：GT ['(3.0, 1.0)'] | 模型 ['(4.0, 3.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(4.0, 4.0)'] | 模型 ['(1.5, 5.0)']
- mirror：GT ['(1.0, 4.0)'] | 模型 ['(5.0, 6.5)']
- trash bin：GT ['(3.0, 1.0)'] | 模型 ['(4.0, 2.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(7.0, 4.0)'] | 模型 ['(8.0, 5.0)']
- mirror：GT ['(5.0, 4.0)'] | 模型 ['(2.5, 6.5)']
- trash bin：GT ['(1.0, 1.0)'] | 模型 ['(3.0, 2.0)']

## Three-view（3-pass）

### 样本 1 `09c1414f1b`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the cutting board and the suitcase (in meters)?
- QA：模型 1.65 vs GT 1.8（错误）
- 类别：cutting board, suitcase
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- cutting board：GT ['(1.0, 2.0)'] | 模型 ['(5.0, 5.0)']
- suitcase：GT ['(2.0, 4.0)'] | 模型 ['(3.0, 8.0)']
**FRONT 视图**（GT → 模型）
- cutting board：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 4.0)']
- suitcase：GT ['(2.0, 1.0)'] | 模型 ['(3.0, 2.0)']
**SIDE 视图**（GT → 模型）
- cutting board：GT ['(2.0, 5.0)'] | 模型 ['(5.0, 4.0)']
- suitcase：GT ['(4.0, 1.0)'] | 模型 ['(8.0, 2.0)']

### 样本 2 `47334103`（arkitscenes · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the table and the stool (in meters)?
- QA：模型 0.4 vs GT 3.7（错误）
- 类别：stool, table
- tags：A2_extra, B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- stool：GT ['(2.0, 2.0)'] | 模型 ['(4.0, 5.0)', '(6.0, 5.0)']
- table：GT ['(7.0, 1.0)'] | 模型 ['(5.0, 5.0)']
**FRONT 视图**（GT → 模型）
- stool：GT ['(2.0, 1.0)'] | 模型 ['(4.0, 3.0)', '(6.0, 3.0)']
- table：GT ['(7.0, 2.0)'] | 模型 ['(5.0, 4.0)']
**SIDE 视图**（GT → 模型）
- stool：GT ['(2.0, 1.0)'] | 模型 ['(5.0, 3.0)', '(5.0, 3.0)']
- table：GT ['(1.0, 2.0)'] | 模型 ['(5.0, 4.0)']

### 样本 3 `42897538`（arkitscenes · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the stool and the refrigerator (in meters)?
- QA：模型 1.7 vs GT 2.6（错误）
- 类别：refrigerator, stool
- tags：A2_extra, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(3.0, 7.0)'] | 模型 ['(2.0, 4.0)']
- stool：GT ['(3.0, 3.0)'] | 模型 ['(5.0, 8.0)', '(7.0, 8.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(3.0, 4.0)'] | 模型 ['(2.0, 4.0)']
- stool：GT ['(3.0, 1.0)'] | 模型 ['(5.0, 1.0)', '(7.0, 1.0)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(7.0, 4.0)'] | 模型 ['(4.0, 4.0)']
- stool：GT ['(3.0, 1.0)'] | 模型 ['(8.0, 1.0)', '(8.0, 1.0)']

### 样本 4 `scene0550_00`（scannet · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the door and the window (in meters)?
- QA：模型 2.5 vs GT 2.5（正确）
- 类别：door, window
- tags：B3_pair
**TOP 视图**（GT → 模型）
- door：GT ['(4.0, 8.0)'] | 模型 ['(1.0, 5.0)']
- window：GT ['(5.0, 1.0)'] | 模型 ['(5.0, 9.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(4.0, 4.0)'] | 模型 ['(1.0, 4.0)']
- window：GT ['(5.0, 5.0)'] | 模型 ['(5.0, 5.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(8.0, 4.0)'] | 模型 ['(5.0, 4.0)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(9.0, 5.0)']

### 样本 5 `scene0378_01`（scannet · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the door and the clock (in meters)?
- QA：模型 3 vs GT 1.6（错误）
- 类别：clock, door
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- clock：GT ['(3.0, 2.0)'] | 模型 ['(5.0, 1.0)']
- door：GT ['(6.0, 1.0)'] | 模型 ['(1.0, 5.0)']
**FRONT 视图**（GT → 模型）
- clock：GT ['(3.0, 7.0)'] | 模型 ['(5.0, 7.0)']
- door：GT ['(6.0, 4.0)'] | 模型 ['(1.0, 4.0)']
**SIDE 视图**（GT → 模型）
- clock：GT ['(2.0, 7.0)'] | 模型 ['(1.0, 7.0)']
- door：GT ['(1.0, 4.0)'] | 模型 ['(5.0, 4.0)']

### 样本 6 `c49a8c6cff`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the trash can and the bed (in meters)?
- QA：模型 1.5 vs GT 0.7（错误）
- 类别：bed, trash can
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(6.0, 5.0)'] | 模型 ['(5.0, 6.0)']
- trash can：GT ['(2.0, 6.0)'] | 模型 ['(2.0, 8.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- trash can：GT ['(2.0, 1.0)'] | 模型 ['(2.0, 1.0)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(5.0, 2.0)'] | 模型 ['(6.0, 3.0)']
- trash can：GT ['(6.0, 1.0)'] | 模型 ['(8.0, 1.0)']

### 样本 7 `3db0a1c8f3`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the blanket and the computer mouse (in meters)?
- QA：模型 1.0 vs GT 0.8（错误）
- 类别：blanket, computer mouse
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- blanket：GT ['(1.0, 1.0)'] | 模型 ['(5.0, 5.0)']
- computer mouse：GT ['(3.0, 3.0)'] | 模型 ['(7.0, 4.0)']
**FRONT 视图**（GT → 模型）
- blanket：GT ['(1.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- computer mouse：GT ['(3.0, 2.0)'] | 模型 ['(7.0, 3.0)']
**SIDE 视图**（GT → 模型）
- blanket：GT ['(1.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- computer mouse：GT ['(3.0, 2.0)'] | 模型 ['(4.0, 3.0)']

### 样本 8 `c50d2d1d42`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the door and the telephone (in meters)?
- QA：模型 2.1 vs GT 4.6（错误）
- 类别：door, telephone
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 4.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 4.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(3.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- telephone：GT ['(3.0, 3.0)'] | 模型 ['(4.0, 4.0)']

### 样本 9 `scene0474_04`（scannet · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the table and the trash bin (in meters)?
- QA：模型 1.3 vs GT 1.9（错误）
- 类别：table, trash bin
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- table：GT ['(4.0, 6.0)'] | 模型 ['(5.0, 5.0)']
- trash bin：GT ['(6.0, 3.0)'] | 模型 ['(3.0, 8.0)']
**FRONT 视图**（GT → 模型）
- table：GT ['(4.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- trash bin：GT ['(6.0, 1.0)'] | 模型 ['(3.0, 1.0)']
**SIDE 视图**（GT → 模型）
- table：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- trash bin：GT ['(3.0, 1.0)'] | 模型 ['(8.0, 1.0)']

### 样本 10 `47333899`（arkitscenes · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the table and the stove (in meters)?
- QA：模型 2.5 vs GT 0.9（错误）
- 类别：stove, table
- tags：C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- stove：GT ['(2.0, 7.0)'] | 模型 ['(2.0, 3.0)']
- table：GT ['(2.0, 1.0)'] | 模型 ['(6.0, 6.0)']
**FRONT 视图**（GT → 模型）
- stove：GT ['(2.0, 4.0)'] | 模型 ['(2.0, 3.0)']
- table：GT ['(2.0, 2.0)'] | 模型 ['(6.0, 3.0)']
**SIDE 视图**（GT → 模型）
- stove：GT ['(7.0, 4.0)'] | 模型 ['(3.0, 3.0)']
- table：GT ['(1.0, 2.0)'] | 模型 ['(6.0, 3.0)']

### 样本 11 `scene0221_01`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (chair, bed, pillow, lamp) is the closest to the microwave?
- QA：模型 A vs GT B（错误）
- 类别：bed, chair, lamp, microwave, pillow
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(4.0, 3.0)', '(2.0, 3.0)'] | 模型 ['(5.0, 7.0)']
- chair：GT ['(3.0, 6.0)', '(1.0, 6.0)', '(2.0, 7.0)'] | 模型 ['(8.0, 7.0)']
- lamp：GT ['(3.0, 1.0)', '(3.0, 0.0)'] | 模型 ['(2.0, 4.0)']
- microwave：GT ['(6.0, 1.0)'] | 模型 []
- pillow：GT ['(2.0, 1.0)', '(4.0, 1.0)', '(4.0, 1.0)', '(4.0, 1.0)', '(2.0, 1.0)'] | 模型 ['(4.0, 5.0)', '(6.0, 5.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(4.0, 2.0)', '(2.0, 3.0)'] | 模型 ['(5.0, 3.0)']
- chair：GT ['(3.0, 3.0)', '(1.0, 5.0)', '(2.0, 4.0)'] | 模型 ['(8.0, 3.0)']
- lamp：GT ['(3.0, 4.0)', '(3.0, 5.0)'] | 模型 ['(2.0, 5.0)']
- microwave：GT ['(6.0, 5.0)'] | 模型 []
- pillow：GT ['(2.0, 4.0)', '(4.0, 4.0)', '(4.0, 4.0)', '(4.0, 4.0)', '(2.0, 4.0)'] | 模型 ['(4.0, 4.0)', '(6.0, 4.0)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(3.0, 2.0)', '(3.0, 3.0)'] | 模型 ['(7.0, 3.0)']
- chair：GT ['(6.0, 3.0)', '(6.0, 5.0)', '(7.0, 4.0)'] | 模型 ['(7.0, 3.0)']
- lamp：GT ['(1.0, 4.0)', '(0.0, 5.0)'] | 模型 ['(4.0, 5.0)']
- microwave：GT ['(1.0, 5.0)'] | 模型 []
- pillow：GT ['(1.0, 4.0)', '(1.0, 4.0)', '(1.0, 4.0)', '(1.0, 4.0)', '(1.0, 4.0)'] | 模型 ['(5.0, 4.0)', '(5.0, 4.0)']

### 样本 12 `scene0307_02`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (window, chair, door, washing machine) is the closest to the radiator?
- QA：模型 A vs GT C（错误）
- 类别：chair, door, radiator, washing machine, window
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 6.0)'] | 模型 ['(5.0, 5.0)']
- door：GT ['(3.0, 5.0)', '(4.0, 7.0)', '(3.0, 5.0)', '(1.0, 7.0)', '(7.0, 3.0)'] | 模型 ['(1.0, 1.0)']
- radiator：GT ['(1.0, 5.0)'] | 模型 ['(4.0, 9.0)']
- washing machine：GT ['(2.0, 7.0)'] | 模型 ['(8.0, 8.0)']
- window：GT ['(4.0, 1.0)', '(2.0, 7.0)', '(4.0, 1.0)'] | 模型 ['(4.0, 9.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- door：GT ['(3.0, 4.0)', '(4.0, 4.0)', '(3.0, 4.0)', '(1.0, 4.0)', '(7.0, 4.0)'] | 模型 ['(1.0, 4.0)']
- radiator：GT ['(1.0, 3.0)'] | 模型 ['(4.0, 3.0)']
- washing machine：GT ['(2.0, 2.0)'] | 模型 ['(8.0, 3.0)']
- window：GT ['(4.0, 6.0)', '(2.0, 6.0)', '(4.0, 6.0)'] | 模型 ['(4.0, 6.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- door：GT ['(5.0, 4.0)', '(7.0, 4.0)', '(5.0, 4.0)', '(7.0, 4.0)', '(3.0, 4.0)'] | 模型 ['(1.0, 4.0)']
- radiator：GT ['(5.0, 3.0)'] | 模型 ['(9.0, 3.0)']
- washing machine：GT ['(7.0, 2.0)'] | 模型 ['(8.0, 3.0)']
- window：GT ['(1.0, 6.0)', '(7.0, 6.0)', '(1.0, 6.0)'] | 模型 ['(9.0, 6.0)']

### 样本 13 `47429977`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (stove, chair, refrigerator, table) is the closest to the tv?
- QA：模型 D vs GT D（正确）
- 类别：chair, refrigerator, stove, table, tv
- tags：A1_miss, A2_extra, B3_pair, C7_missing, C8_height
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 1.0)', '(3.0, 2.0)', '(3.0, 1.0)'] | 模型 ['(4.0, 5.0)', '(6.0, 5.0)', '(5.0, 4.0)', '(5.0, 6.0)']
- refrigerator：GT ['(2.0, 7.0)'] | 模型 ['(2.0, 2.0)']
- stove：GT ['(1.0, 3.0)'] | 模型 ['(2.0, 8.0)']
- table：GT ['(6.0, 4.0)', '(3.0, 1.0)'] | 模型 ['(5.0, 5.0)']
- tv：GT ['(6.0, 1.0)'] | 模型 ['(8.0, 5.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 3.0)', '(3.0, 3.0)', '(3.0, 3.0)'] | 模型 ['(4.0, 2.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(5.0, 2.0)']
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.0, 4.0)']
- stove：GT ['(1.0, 5.0)'] | 模型 ['(2.0, 3.0)']
- table：GT ['(6.0, 2.0)', '(3.0, 3.0)'] | 模型 ['(5.0, 3.0)']
- tv：GT ['(6.0, 6.0)'] | 模型 ['(8.0, 5.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(1.0, 3.0)', '(2.0, 3.0)', '(1.0, 3.0)'] | 模型 ['(5.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(6.0, 2.0)']
- refrigerator：GT ['(7.0, 4.0)'] | 模型 ['(2.0, 4.0)']
- stove：GT ['(3.0, 5.0)'] | 模型 ['(8.0, 3.0)']
- table：GT ['(4.0, 2.0)', '(1.0, 3.0)'] | 模型 ['(5.0, 3.0)']
- tv：GT ['(1.0, 6.0)'] | 模型 ['(5.0, 5.0)']

### 样本 14 `scene0653_00`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (window, monitor, table, keyboard) is the closest to the door?
- QA：模型 B vs GT C（错误）
- 类别：door, keyboard, monitor, table, window
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(7.0, 7.0)'] | 模型 ['(9.0, 4.0)']
- keyboard：GT ['(2.0, 3.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 6.0)']
- monitor：GT ['(1.0, 6.0)', '(2.0, 3.0)', '(2.0, 3.0)', '(6.0, 1.0)', '(7.0, 1.0)', '(6.0, 4.0)', '(6.0, 6.0)'] | 模型 ['(5.0, 4.0)']
- table：GT ['(1.0, 6.0)', '(2.0, 3.0)', '(6.0, 4.0)', '(2.0, 4.0)', '(7.0, 1.0)', '(6.0, 6.0)'] | 模型 ['(5.0, 7.0)']
- window：GT ['(1.0, 5.0)', '(1.0, 2.0)'] | 模型 ['(1.0, 3.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(7.0, 5.0)'] | 模型 ['(9.0, 4.0)']
- keyboard：GT ['(2.0, 2.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- monitor：GT ['(1.0, 3.0)', '(2.0, 3.0)', '(2.0, 3.0)', '(6.0, 3.0)', '(7.0, 3.0)', '(6.0, 3.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- table：GT ['(1.0, 2.0)', '(2.0, 2.0)', '(6.0, 2.0)', '(2.0, 1.0)', '(7.0, 2.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- window：GT ['(1.0, 5.0)', '(1.0, 5.0)'] | 模型 ['(1.0, 5.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(7.0, 5.0)'] | 模型 ['(4.0, 4.0)']
- keyboard：GT ['(3.0, 2.0)', '(2.0, 2.0)'] | 模型 ['(6.0, 4.0)']
- monitor：GT ['(6.0, 3.0)', '(3.0, 3.0)', '(3.0, 3.0)', '(1.0, 3.0)', '(1.0, 3.0)', '(4.0, 3.0)', '(6.0, 3.0)'] | 模型 ['(4.0, 5.0)']
- table：GT ['(6.0, 2.0)', '(3.0, 2.0)', '(4.0, 2.0)', '(4.0, 1.0)', '(1.0, 2.0)', '(6.0, 2.0)'] | 模型 ['(7.0, 3.0)']
- window：GT ['(5.0, 5.0)', '(2.0, 5.0)'] | 模型 ['(3.0, 5.0)']

### 样本 15 `38d58a7a31`（scannetpp · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (telephone, heater, chair, ceiling light) is the closest to the trash can?
- QA：模型 C vs GT C（正确）
- 类别：ceiling light, chair, heater, telephone, trash can
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, C8_height
**TOP 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 1.0)', '(1.0, 2.0)', '(4.0, 6.0)', '(1.0, 3.0)', '(4.0, 5.0)', '(4.0, 3.0)', '(6.0, 1.0)', '(7.0, 6.0)', '(6.0, 4.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 1.0)']
- chair：GT ['(1.0, 6.0)', '(3.0, 6.0)', '(4.0, 4.0)', '(5.0, 5.0)', '(6.0, 4.0)', '(2.0, 5.0)', '(2.0, 7.0)', '(5.0, 3.0)', '(4.0, 3.0)', '(4.0, 6.0)', '(6.0, 6.0)', '(6.0, 1.0)', '(1.0, 6.0)', '(6.0, 2.0)', '(3.0, 6.0)', '(4.0, 6.0)', '(1.0, 7.0)', '(2.0, 5.0)', '(5.0, 6.0)', '(3.0, 3.0)', '(5.0, 4.0)', '(6.0, 4.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(7.0, 3.0)', '(7.0, 6.0)', '(6.0, 6.0)', '(3.0, 5.0)', '(2.0, 2.0)', '(3.0, 5.0)', '(2.0, 3.0)', '(1.0, 7.0)', '(1.0, 7.0)', '(1.0, 6.0)', '(1.0, 6.0)', '(1.0, 6.0)'] | 模型 ['(3.0, 7.0)', '(7.0, 7.0)']
- heater：GT ['(7.0, 4.0)', '(8.0, 6.0)', '(7.0, 1.0)'] | 模型 ['(9.0, 6.0)']
- telephone：GT ['(7.0, 2.0)'] | 模型 ['(4.0, 5.0)']
- trash can：GT ['(1.0, 4.0)'] | 模型 ['(2.0, 8.0)']
**FRONT 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 7.0)', '(1.0, 7.0)', '(4.0, 8.0)', '(1.0, 8.0)', '(4.0, 7.0)', '(4.0, 7.0)', '(6.0, 8.0)', '(7.0, 7.0)', '(6.0, 8.0)', '(6.0, 7.0)'] | 模型 ['(5.0, 9.0)']
- chair：GT ['(1.0, 2.0)', '(3.0, 2.0)', '(4.0, 2.0)', '(5.0, 2.0)', '(6.0, 2.0)', '(2.0, 2.0)', '(2.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(4.0, 2.0)', '(6.0, 2.0)', '(6.0, 1.0)', '(1.0, 2.0)', '(6.0, 2.0)', '(3.0, 2.0)', '(4.0, 1.0)', '(1.0, 2.0)', '(2.0, 1.0)', '(5.0, 2.0)', '(3.0, 1.0)', '(5.0, 2.0)', '(6.0, 1.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(7.0, 2.0)', '(7.0, 2.0)', '(6.0, 2.0)', '(3.0, 2.0)', '(2.0, 2.0)', '(3.0, 2.0)', '(2.0, 2.0)', '(1.0, 2.0)', '(1.0, 2.0)', '(1.0, 2.0)', '(1.0, 2.0)', '(1.0, 1.0)'] | 模型 ['(3.0, 3.0)', '(7.0, 3.0)']
- heater：GT ['(7.0, 1.0)', '(8.0, 1.0)', '(7.0, 1.0)'] | 模型 ['(9.0, 3.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(4.0, 4.0)']
- trash can：GT ['(1.0, 1.0)'] | 模型 ['(2.0, 2.0)']
**SIDE 视图**（GT → 模型）
- ceiling light：GT ['(1.0, 7.0)', '(2.0, 7.0)', '(6.0, 8.0)', '(3.0, 8.0)', '(5.0, 7.0)', '(3.0, 7.0)', '(1.0, 8.0)', '(6.0, 7.0)', '(4.0, 8.0)', '(3.0, 7.0)'] | 模型 ['(1.0, 9.0)']
- chair：GT ['(6.0, 2.0)', '(6.0, 2.0)', '(4.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(5.0, 2.0)', '(7.0, 2.0)', '(3.0, 2.0)', '(3.0, 2.0)', '(6.0, 2.0)', '(6.0, 2.0)', '(1.0, 1.0)', '(6.0, 2.0)', '(2.0, 2.0)', '(6.0, 2.0)', '(6.0, 1.0)', '(7.0, 2.0)', '(5.0, 1.0)', '(6.0, 2.0)', '(3.0, 1.0)', '(4.0, 2.0)', '(4.0, 1.0)', '(2.0, 2.0)', '(2.0, 2.0)', '(3.0, 2.0)', '(6.0, 2.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(2.0, 2.0)', '(5.0, 2.0)', '(3.0, 2.0)', '(7.0, 2.0)', '(7.0, 2.0)', '(6.0, 2.0)', '(6.0, 2.0)', '(6.0, 1.0)'] | 模型 ['(7.0, 3.0)', '(7.0, 3.0)']
- heater：GT ['(4.0, 1.0)', '(6.0, 1.0)', '(1.0, 1.0)'] | 模型 ['(6.0, 3.0)']
- telephone：GT ['(2.0, 3.0)'] | 模型 ['(5.0, 4.0)']
- trash can：GT ['(4.0, 1.0)'] | 模型 ['(8.0, 2.0)']

### 样本 16 `42899461`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (chair, sofa, fireplace, stove) is the closest to the tv?
- QA：模型 C vs GT A（错误）
- 类别：chair, fireplace, sofa, stove, tv
- tags：A1_miss, B3_pair, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(7.0, 4.0)', '(7.0, 3.0)', '(2.0, 4.0)', '(1.0, 4.0)'] | 模型 ['(3.0, 6.0)', '(7.0, 6.0)']
- fireplace：GT ['(4.0, 8.0)'] | 模型 ['(5.0, 2.0)']
- sofa：GT ['(7.0, 6.0)'] | 模型 ['(5.0, 7.0)']
- stove：GT ['(1.0, 1.0)'] | 模型 []
- tv：GT ['(1.0, 7.0)'] | 模型 ['(5.0, 3.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(7.0, 3.0)', '(7.0, 3.0)', '(2.0, 4.0)', '(1.0, 4.0)'] | 模型 ['(3.0, 2.0)', '(7.0, 2.0)']
- fireplace：GT ['(4.0, 4.0)'] | 模型 ['(5.0, 2.0)']
- sofa：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 2.0)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
- tv：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 5.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(4.0, 3.0)', '(3.0, 3.0)', '(4.0, 4.0)', '(4.0, 4.0)'] | 模型 ['(6.0, 2.0)', '(6.0, 2.0)']
- fireplace：GT ['(8.0, 4.0)'] | 模型 ['(2.0, 2.0)']
- sofa：GT ['(6.0, 4.0)'] | 模型 ['(7.0, 2.0)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
- tv：GT ['(7.0, 5.0)'] | 模型 ['(3.0, 5.0)']

### 样本 17 `42899461`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (table, tv, sofa, stove) is the closest to the fireplace?
- QA：模型 B vs GT A（错误）
- 类别：fireplace, sofa, stove, table, tv
- tags：A1_miss, B3_pair, B5_adjacent, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- fireplace：GT ['(4.0, 8.0)'] | 模型 ['(5.0, 8.0)']
- sofa：GT ['(7.0, 6.0)'] | 模型 ['(5.0, 3.0)']
- stove：GT ['(1.0, 1.0)'] | 模型 []
- table：GT ['(6.0, 7.0)', '(1.0, 7.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- tv：GT ['(1.0, 7.0)'] | 模型 ['(5.0, 8.0)']
**FRONT 视图**（GT → 模型）
- fireplace：GT ['(4.0, 4.0)'] | 模型 ['(5.0, 3.0)']
- sofa：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 2.0)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
- table：GT ['(6.0, 2.0)', '(1.0, 2.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 2.0)']
- tv：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 6.0)']
**SIDE 视图**（GT → 模型）
- fireplace：GT ['(8.0, 4.0)'] | 模型 ['(8.0, 3.0)']
- sofa：GT ['(6.0, 4.0)'] | 模型 ['(3.0, 2.0)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
- table：GT ['(7.0, 2.0)', '(7.0, 2.0)', '(3.0, 3.0)'] | 模型 ['(5.0, 2.0)']
- tv：GT ['(7.0, 5.0)'] | 模型 ['(8.0, 6.0)']

### 样本 18 `47430034`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (chair, stool, table, bed) is the closest to the tv?
- QA：模型 C vs GT C（正确）
- 类别：bed, chair, stool, table, tv
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, C8_height
**TOP 视图**（GT → 模型）
- bed：GT ['(5.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- chair：GT ['(5.0, 7.0)', '(6.0, 7.0)', '(1.0, 2.0)'] | 模型 ['(3.0, 8.0)']
- stool：GT ['(4.0, 3.0)'] | 模型 []
- table：GT ['(4.0, 3.0)', '(6.0, 7.0)', '(1.0, 2.0)'] | 模型 ['(5.0, 8.0)']
- tv：GT ['(7.0, 7.0)'] | 模型 ['(5.0, 9.5)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(5.0, 4.0)'] | 模型 ['(5.0, 2.5)']
- chair：GT ['(5.0, 3.0)', '(6.0, 3.0)', '(1.0, 2.0)'] | 模型 ['(3.0, 3.0)']
- stool：GT ['(4.0, 1.0)'] | 模型 []
- table：GT ['(4.0, 2.0)', '(6.0, 2.0)', '(1.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- tv：GT ['(7.0, 6.0)'] | 模型 ['(5.0, 5.5)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(2.0, 4.0)'] | 模型 ['(4.0, 2.5)']
- chair：GT ['(7.0, 3.0)', '(7.0, 3.0)', '(2.0, 2.0)'] | 模型 ['(8.0, 3.0)']
- stool：GT ['(3.0, 1.0)'] | 模型 []
- table：GT ['(3.0, 2.0)', '(7.0, 2.0)', '(2.0, 2.0)'] | 模型 ['(8.0, 3.0)']
- tv：GT ['(7.0, 6.0)'] | 模型 ['(9.5, 5.5)']

### 样本 19 `scene0616_01`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (table, trash bin, chair, lamp) is the closest to the window?
- QA：模型 A vs GT A（正确）
- 类别：chair, lamp, table, trash bin, window
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, C8_height
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)', '(4.0, 2.0)', '(4.0, 3.0)', '(3.0, 5.0)', '(3.0, 4.0)', '(5.0, 6.0)', '(6.0, 5.0)'] | 模型 ['(4.0, 5.0)', '(6.0, 5.0)']
- lamp：GT ['(5.0, 1.0)'] | 模型 ['(2.0, 8.0)']
- table：GT ['(5.0, 1.0)', '(3.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- trash bin：GT ['(7.0, 4.0)', '(7.0, 4.0)'] | 模型 ['(8.0, 3.0)']
- window：GT ['(1.0, 3.0)'] | 模型 ['(5.0, 1.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)', '(4.0, 2.0)', '(4.0, 2.0)', '(3.0, 2.0)', '(3.0, 2.0)', '(5.0, 2.0)', '(6.0, 2.0)'] | 模型 ['(4.0, 3.0)', '(6.0, 3.0)']
- lamp：GT ['(5.0, 4.0)'] | 模型 ['(2.0, 6.0)']
- table：GT ['(5.0, 2.0)', '(3.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- trash bin：GT ['(7.0, 2.0)', '(7.0, 2.0)'] | 模型 ['(8.0, 1.0)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 6.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(2.0, 2.0)', '(2.0, 2.0)', '(3.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(6.0, 2.0)', '(5.0, 2.0)'] | 模型 ['(5.0, 3.0)', '(5.0, 3.0)']
- lamp：GT ['(1.0, 4.0)'] | 模型 ['(8.0, 6.0)']
- table：GT ['(1.0, 2.0)', '(3.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- trash bin：GT ['(4.0, 2.0)', '(4.0, 2.0)'] | 模型 ['(3.0, 1.0)']
- window：GT ['(3.0, 5.0)'] | 模型 ['(1.0, 6.0)']

### 样本 20 `scene0651_02`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (counter, chair, table, trash bin) is the closest to the sofa?
- QA：模型 B vs GT C（错误）
- 类别：chair, counter, sofa, table, trash bin
- tags：A1_miss, B3_pair, B5_adjacent, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(7.0, 4.0)', '(5.0, 3.0)', '(5.0, 4.0)', '(6.0, 3.0)'] | 模型 ['(4.0, 4.0)', '(6.0, 4.0)', '(4.0, 6.0)', '(6.0, 6.0)']
- counter：GT ['(3.0, 6.0)'] | 模型 ['(2.0, 8.0)']
- sofa：GT ['(5.0, 1.0)'] | 模型 ['(5.0, 2.0)']
- table：GT ['(3.0, 2.0)', '(5.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- trash bin：GT ['(1.0, 6.0)'] | 模型 ['(1.0, 8.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(7.0, 2.0)', '(5.0, 3.0)', '(5.0, 3.0)', '(6.0, 3.0)'] | 模型 ['(4.0, 3.0)', '(6.0, 3.0)', '(4.0, 3.0)', '(6.0, 3.0)']
- counter：GT ['(3.0, 5.0)'] | 模型 ['(2.0, 4.0)']
- sofa：GT ['(5.0, 3.0)'] | 模型 ['(5.0, 3.0)']
- table：GT ['(3.0, 1.0)', '(5.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- trash bin：GT ['(1.0, 1.0)'] | 模型 ['(1.0, 2.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)', '(3.0, 3.0)', '(4.0, 3.0)', '(3.0, 3.0)'] | 模型 ['(4.0, 3.0)', '(4.0, 3.0)', '(6.0, 3.0)', '(6.0, 3.0)']
- counter：GT ['(6.0, 5.0)'] | 模型 ['(8.0, 4.0)']
- sofa：GT ['(1.0, 3.0)'] | 模型 ['(2.0, 3.0)']
- table：GT ['(2.0, 1.0)', '(3.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- trash bin：GT ['(6.0, 1.0)'] | 模型 ['(8.0, 2.0)']

### 样本 21 `31a2c91c43`（scannetpp · object_rel_direction_easy）
- 问题：If I am standing by the ceiling light and facing the toilet, is the door to the left or the right of the toilet?
- QA：模型 B vs GT A（错误）
- 类别：ceiling light, door, toilet
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- ceiling light：GT ['(5.0, 8.0)'] | 模型 ['(5.0, 1.0)']
- door：GT ['(2.0, 4.0)'] | 模型 ['(1.0, 5.0)']
- toilet：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 8.0)']
**FRONT 视图**（GT → 模型）
- ceiling light：GT ['(5.0, 8.0)'] | 模型 ['(5.0, 9.0)']
- door：GT ['(2.0, 4.0)'] | 模型 ['(1.0, 4.0)']
- toilet：GT ['(6.0, 1.0)'] | 模型 ['(5.0, 2.0)']
**SIDE 视图**（GT → 模型）
- ceiling light：GT ['(8.0, 8.0)'] | 模型 ['(1.0, 9.0)']
- door：GT ['(4.0, 4.0)'] | 模型 ['(5.0, 4.0)']
- toilet：GT ['(2.0, 1.0)'] | 模型 ['(8.0, 2.0)']

### 样本 22 `scene0353_00`（scannet · object_rel_direction_easy）
- 问题：If I am standing by the bookshelf and facing the door, is the refrigerator to the left or the right of the door?
- QA：模型 B vs GT A（错误）
- 类别：bookshelf, door, refrigerator
- tags：B3_pair, B4_scale, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- bookshelf：GT ['(7.0, 1.0)'] | 模型 ['(8.0, 3.0)']
- door：GT ['(7.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- refrigerator：GT ['(5.0, 5.0)'] | 模型 ['(2.0, 8.0)']
**FRONT 视图**（GT → 模型）
- bookshelf：GT ['(7.0, 3.0)'] | 模型 ['(8.0, 4.0)']
- door：GT ['(7.0, 4.0)'] | 模型 ['(1.0, 4.0)']
- refrigerator：GT ['(5.0, 2.0)'] | 模型 ['(2.0, 4.0)']
**SIDE 视图**（GT → 模型）
- bookshelf：GT ['(1.0, 3.0)'] | 模型 ['(3.0, 4.0)']
- door：GT ['(3.0, 4.0)'] | 模型 ['(5.0, 4.0)']
- refrigerator：GT ['(5.0, 2.0)'] | 模型 ['(8.0, 4.0)']

### 样本 23 `41159525`（arkitscenes · object_rel_direction_easy）
- 问题：If I am standing by the stove and facing the table, is the refrigerator to the left or the right of the table?
- QA：模型 A vs GT B（错误）
- 类别：refrigerator, stove, table
- tags：B3_pair, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 1.0)'] | 模型 ['(2.0, 4.0)']
- stove：GT ['(1.0, 1.0)'] | 模型 ['(5.0, 3.0)']
- table：GT ['(6.0, 5.0)'] | 模型 ['(6.0, 7.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 4.0)'] | 模型 ['(2.0, 4.0)']
- stove：GT ['(1.0, 4.0)'] | 模型 ['(5.0, 3.0)']
- table：GT ['(6.0, 2.0)'] | 模型 ['(6.0, 3.0)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 4.0)'] | 模型 ['(4.0, 4.0)']
- stove：GT ['(1.0, 4.0)'] | 模型 ['(3.0, 3.0)']
- table：GT ['(5.0, 2.0)'] | 模型 ['(7.0, 3.0)']

### 样本 24 `d755b3d9d8`（scannetpp · object_rel_direction_easy）
- 问题：If I am standing by the cup and facing the whiteboard, is the shoes to the left or the right of the whiteboard?
- QA：模型 B vs GT A（错误）
- 类别：cup, shoes, whiteboard
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- cup：GT ['(5.0, 1.0)'] | 模型 ['(4.0, 5.0)']
- shoes：GT ['(7.0, 4.0)'] | 模型 ['(3.0, 8.0)']
- whiteboard：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 2.0)']
**FRONT 视图**（GT → 模型）
- cup：GT ['(5.0, 2.0)'] | 模型 ['(4.0, 4.0)']
- shoes：GT ['(7.0, 0.0)'] | 模型 ['(3.0, 1.0)']
- whiteboard：GT ['(2.0, 4.0)'] | 模型 ['(5.0, 6.0)']
**SIDE 视图**（GT → 模型）
- cup：GT ['(1.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- shoes：GT ['(4.0, 0.0)'] | 模型 ['(8.0, 1.0)']
- whiteboard：GT ['(7.0, 4.0)'] | 模型 ['(2.0, 6.0)']

### 样本 25 `47204578`（arkitscenes · object_rel_direction_easy）
- 问题：If I am standing by the tv and facing the table, is the stool to the left or the right of the table?
- QA：模型 A vs GT A（正确）
- 类别：stool, table, tv
- tags：A2_extra, B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- stool：GT ['(1.0, 1.0)'] | 模型 ['(3.5, 5.0)', '(6.5, 5.0)']
- table：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 5.0)']
- tv：GT ['(3.0, 1.0)'] | 模型 ['(5.0, 1.0)']
**FRONT 视图**（GT → 模型）
- stool：GT ['(1.0, 1.0)'] | 模型 ['(3.5, 2.5)', '(6.5, 2.5)']
- table：GT ['(2.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- tv：GT ['(3.0, 6.0)'] | 模型 ['(5.0, 6.5)']
**SIDE 视图**（GT → 模型）
- stool：GT ['(1.0, 1.0)'] | 模型 ['(5.0, 2.5)', '(5.0, 2.5)']
- table：GT ['(7.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- tv：GT ['(1.0, 6.0)'] | 模型 ['(1.0, 6.5)']

### 样本 26 `scene0458_00`（scannet · object_rel_direction_easy）
- 问题：If I am standing by the window and facing the door, is the mirror to the left or the right of the door?
- QA：模型 B vs GT B（正确）
- 类别：door, mirror, window
- tags：B3_pair, C8_height
**TOP 视图**（GT → 模型）
- door：GT ['(8.0, 6.0)'] | 模型 ['(1.0, 5.0)']
- mirror：GT ['(1.0, 6.0)'] | 模型 ['(5.0, 2.0)']
- window：GT ['(6.0, 1.0)'] | 模型 ['(5.0, 8.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(8.0, 5.0)'] | 模型 ['(1.0, 4.0)']
- mirror：GT ['(1.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- window：GT ['(6.0, 5.0)'] | 模型 ['(5.0, 5.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(6.0, 5.0)'] | 模型 ['(5.0, 4.0)']
- mirror：GT ['(6.0, 4.0)'] | 模型 ['(2.0, 5.0)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(8.0, 5.0)']

### 样本 27 `scene0426_00`（scannet · object_rel_direction_easy）
- 问题：If I am standing by the tv and facing the lamp, is the table to the left or the right of the lamp?
- QA：模型 B vs GT A（错误）
- 类别：lamp, table, tv
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- lamp：GT ['(5.0, 1.0)'] | 模型 ['(8.0, 3.0)']
- table：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 5.0)']
- tv：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 2.0)']
**FRONT 视图**（GT → 模型）
- lamp：GT ['(5.0, 4.0)'] | 模型 ['(8.0, 5.0)']
- table：GT ['(2.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- tv：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 5.0)']
**SIDE 视图**（GT → 模型）
- lamp：GT ['(1.0, 4.0)'] | 模型 ['(3.0, 5.0)']
- table：GT ['(7.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- tv：GT ['(3.0, 4.0)'] | 模型 ['(2.0, 5.0)']

### 样本 28 `scene0144_00`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the window and facing the lamp, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 1
- QA：模型 C vs GT C（正确）
- 类别：door, lamp, window
- tags：B3_pair, C8_height
**TOP 视图**（GT → 模型）
- door：GT ['(8.0, 1.0)'] | 模型 ['(1.0, 5.0)']
- lamp：GT ['(5.0, 7.0)'] | 模型 ['(5.0, 3.0)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(9.0, 5.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(8.0, 3.0)'] | 模型 ['(1.0, 4.0)']
- lamp：GT ['(5.0, 5.0)'] | 模型 ['(5.0, 7.0)']
- window：GT ['(1.0, 6.0)'] | 模型 ['(9.0, 5.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(1.0, 3.0)'] | 模型 ['(5.0, 4.0)']
- lamp：GT ['(7.0, 5.0)'] | 模型 ['(3.0, 7.0)']
- window：GT ['(5.0, 6.0)'] | 模型 ['(5.0, 5.0)']

### 样本 29 `scene0629_01`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the bed and facing the chair, is the mirror to my left, right, or back?
An object is to my back if I would have to turn at least 1
- QA：模型 B vs GT B（正确）
- 类别：bed, chair, mirror
- tags：QA_map_clean
**TOP 视图**（GT → 模型）
- bed：GT ['(7.0, 4.0)'] | 模型 ['(5.1, 5.8)']
- chair：GT ['(6.0, 7.0)'] | 模型 ['(2.8, 8.2)']
- mirror：GT ['(3.0, 6.0)'] | 模型 ['(1.5, 4.5)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(7.0, 3.0)'] | 模型 ['(5.1, 2.8)']
- chair：GT ['(6.0, 2.0)'] | 模型 ['(2.8, 2.5)']
- mirror：GT ['(3.0, 4.0)'] | 模型 ['(1.5, 5.5)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(4.0, 3.0)'] | 模型 ['(5.8, 2.8)']
- chair：GT ['(7.0, 2.0)'] | 模型 ['(8.2, 2.5)']
- mirror：GT ['(6.0, 4.0)'] | 模型 ['(4.5, 5.5)']

### 样本 30 `5ee7c22ba0`（scannetpp · object_rel_direction_medium）
- 问题：If I am standing by the refrigerator and facing the microwave, is the ceiling light to my left, right, or back?
An object is to my back if I would hav
- QA：模型 B vs GT B（正确）
- 类别：ceiling light, microwave, refrigerator
- tags：B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 3.0)'] | 模型 ['(5.0, 1.0)']
- microwave：GT ['(3.0, 1.0)'] | 模型 ['(3.0, 5.0)']
- refrigerator：GT ['(4.0, 7.0)'] | 模型 ['(8.0, 6.0)']
**FRONT 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 8.0)'] | 模型 ['(5.0, 9.0)']
- microwave：GT ['(3.0, 3.0)'] | 模型 ['(3.0, 5.0)']
- refrigerator：GT ['(4.0, 2.0)'] | 模型 ['(8.0, 4.0)']
**SIDE 视图**（GT → 模型）
- ceiling light：GT ['(3.0, 8.0)'] | 模型 ['(1.0, 9.0)']
- microwave：GT ['(1.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- refrigerator：GT ['(7.0, 2.0)'] | 模型 ['(6.0, 4.0)']

### 样本 31 `45261121`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the table and facing the tv, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 135
- QA：模型 B vs GT A（错误）
- 类别：stove, table, tv
- tags：B3_pair, B4_scale, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- stove：GT ['(3.0, 2.0)'] | 模型 ['(3.0, 2.0)']
- table：GT ['(5.0, 4.0)'] | 模型 ['(5.0, 6.0)']
- tv：GT ['(7.0, 1.0)'] | 模型 ['(8.0, 3.0)']
**FRONT 视图**（GT → 模型）
- stove：GT ['(3.0, 3.0)'] | 模型 ['(3.0, 3.0)']
- table：GT ['(5.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- tv：GT ['(7.0, 7.0)'] | 模型 ['(8.0, 5.0)']
**SIDE 视图**（GT → 模型）
- stove：GT ['(2.0, 3.0)'] | 模型 ['(2.0, 3.0)']
- table：GT ['(4.0, 2.0)'] | 模型 ['(6.0, 3.0)']
- tv：GT ['(1.0, 7.0)'] | 模型 ['(3.0, 5.0)']

### 样本 32 `45b0dac5e3`（scannetpp · object_rel_direction_medium）
- 问题：If I am standing by the cup and facing the heater, is the toilet to my left, right, or back?
An object is to my back if I would have to turn at least 
- QA：模型 A vs GT C（错误）
- 类别：cup, heater, toilet
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- cup：GT ['(6.0, 1.0)'] | 模型 ['(3.0, 5.0)']
- heater：GT ['(0.0, 5.0)'] | 模型 ['(8.0, 4.0)']
- toilet：GT ['(7.0, 6.0)'] | 模型 ['(5.0, 7.0)']
**FRONT 视图**（GT → 模型）
- cup：GT ['(6.0, 3.0)'] | 模型 ['(3.0, 5.0)']
- heater：GT ['(0.0, 3.0)'] | 模型 ['(8.0, 4.0)']
- toilet：GT ['(7.0, 2.0)'] | 模型 ['(5.0, 3.0)']
**SIDE 视图**（GT → 模型）
- cup：GT ['(1.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- heater：GT ['(5.0, 3.0)'] | 模型 ['(4.0, 4.0)']
- toilet：GT ['(6.0, 2.0)'] | 模型 ['(7.0, 3.0)']

### 样本 33 `scene0695_00`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the lamp and facing the pillow, is the table to my left, right, or back?
An object is to my back if I would have to turn at least 
- QA：模型 C vs GT C（正确）
- 类别：lamp, pillow, table
- tags：A2_extra, B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- lamp：GT ['(5.0, 1.0)'] | 模型 ['(2.0, 3.0)']
- pillow：GT ['(1.0, 2.0)'] | 模型 ['(3.0, 5.0)', '(4.0, 5.0)']
- table：GT ['(3.0, 7.0)'] | 模型 ['(3.0, 4.0)']
**FRONT 视图**（GT → 模型）
- lamp：GT ['(5.0, 4.0)'] | 模型 ['(2.0, 5.0)']
- pillow：GT ['(1.0, 4.0)'] | 模型 ['(3.0, 4.0)', '(4.0, 4.0)']
- table：GT ['(3.0, 2.0)'] | 模型 ['(3.0, 3.0)']
**SIDE 视图**（GT → 模型）
- lamp：GT ['(1.0, 4.0)'] | 模型 ['(3.0, 5.0)']
- pillow：GT ['(2.0, 4.0)'] | 模型 ['(5.0, 4.0)', '(5.0, 4.0)']
- table：GT ['(7.0, 2.0)'] | 模型 ['(4.0, 3.0)']

### 样本 34 `47334096`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the stool and facing the sofa, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 1
- QA：模型 C vs GT C（正确）
- 类别：sofa, stool, stove
- tags：A2_extra, B3_pair, B4_scale, C8_height
**TOP 视图**（GT → 模型）
- sofa：GT ['(4.0, 4.0)'] | 模型 ['(3.0, 8.0)']
- stool：GT ['(5.0, 1.0)'] | 模型 ['(2.0, 4.0)', '(4.0, 4.0)']
- stove：GT ['(7.0, 6.0)'] | 模型 ['(8.0, 3.0)']
**FRONT 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 ['(3.0, 3.0)']
- stool：GT ['(5.0, 2.0)'] | 模型 ['(2.0, 2.0)', '(4.0, 2.0)']
- stove：GT ['(7.0, 5.0)'] | 模型 ['(8.0, 3.0)']
**SIDE 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 ['(8.0, 3.0)']
- stool：GT ['(1.0, 2.0)'] | 模型 ['(4.0, 2.0)', '(4.0, 2.0)']
- stove：GT ['(6.0, 5.0)'] | 模型 ['(3.0, 3.0)']

### 样本 35 `42446103`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the stove and facing the tv, is the stool to my left, right, or back?
An object is to my back if I would have to turn at least 135
- QA：模型 C vs GT A（错误）
- 类别：stool, stove, tv
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- stool：GT ['(3.0, 3.0)'] | 模型 ['(5.0, 8.0)']
- stove：GT ['(3.0, 7.0)'] | 模型 ['(3.0, 5.0)']
- tv：GT ['(8.0, 2.0)'] | 模型 ['(8.0, 3.0)']
**FRONT 视图**（GT → 模型）
- stool：GT ['(3.0, 1.0)'] | 模型 ['(5.0, 2.0)']
- stove：GT ['(3.0, 4.0)'] | 模型 ['(3.0, 3.0)']
- tv：GT ['(8.0, 7.0)'] | 模型 ['(8.0, 5.0)']
**SIDE 视图**（GT → 模型）
- stool：GT ['(3.0, 1.0)'] | 模型 ['(8.0, 2.0)']
- stove：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 3.0)']
- tv：GT ['(2.0, 7.0)'] | 模型 ['(3.0, 5.0)']

### 样本 36 `42446049`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the washer and facing the refrigerator, is the stove to my left, right, or back?
An object is to my back if I would have to turn a
- QA：模型 C vs GT C（正确）
- 类别：refrigerator, stove, washer
- tags：B3_pair, B4_scale, C8_height
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 6.0)'] | 模型 ['(2.0, 5.0)']
- stove：GT ['(6.0, 1.0)'] | 模型 ['(5.0, 4.0)']
- washer：GT ['(7.0, 7.0)'] | 模型 ['(8.0, 6.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 4.0)'] | 模型 ['(2.0, 5.0)']
- stove：GT ['(6.0, 4.0)'] | 模型 ['(5.0, 3.0)']
- washer：GT ['(7.0, 2.0)'] | 模型 ['(8.0, 3.0)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- stove：GT ['(1.0, 4.0)'] | 模型 ['(4.0, 3.0)']
- washer：GT ['(7.0, 2.0)'] | 模型 ['(6.0, 3.0)']

### 样本 37 `scene0144_00`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the lamp and facing the printer, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 
- QA：模型 C vs GT C（正确）
- 类别：door, lamp, printer
- tags：A1_miss, B3_pair, B4_scale, C7_missing, C8_height
**TOP 视图**（GT → 模型）
- door：GT ['(8.0, 1.0)'] | 模型 ['(1.0, 5.0)']
- lamp：GT ['(5.0, 7.0)'] | 模型 ['(8.0, 3.0)']
- printer：GT ['(2.0, 3.0)', '(2.0, 3.0)'] | 模型 ['(7.0, 5.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(8.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- lamp：GT ['(5.0, 5.0)'] | 模型 ['(8.0, 5.0)']
- printer：GT ['(2.0, 4.0)', '(2.0, 4.0)'] | 模型 ['(7.0, 4.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(1.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- lamp：GT ['(7.0, 5.0)'] | 模型 ['(3.0, 5.0)']
- printer：GT ['(3.0, 4.0)', '(3.0, 4.0)'] | 模型 ['(5.0, 4.0)']

### 样本 38 `f9f95681fd`（scannetpp · object_rel_direction_medium）
- 问题：If I am standing by the door and facing the kettle, is the microwave to my left, right, or back?
An object is to my back if I would have to turn at le
- QA：模型 A vs GT C（错误）
- 类别：door, kettle, microwave
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(1.0, 3.0)'] | 模型 ['(1.0, 8.0)']
- kettle：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- microwave：GT ['(2.0, 6.0)'] | 模型 ['(4.0, 5.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(1.0, 4.0)'] | 模型 ['(1.0, 5.0)']
- kettle：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 4.0)']
- microwave：GT ['(2.0, 3.0)'] | 模型 ['(4.0, 4.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(3.0, 4.0)'] | 模型 ['(8.0, 5.0)']
- kettle：GT ['(3.0, 3.0)'] | 模型 ['(5.0, 4.0)']
- microwave：GT ['(6.0, 3.0)'] | 模型 ['(5.0, 4.0)']

### 样本 39 `47331668`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the tv and facing the bed, is the chair to my front-left, front-right, back-left, or back-right?
The directions refer to the quadr
- QA：模型 C vs GT A（错误）
- 类别：bed, chair, tv
- tags：B3_pair, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(6.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(3.0, 7.0)']
- tv：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 2.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(3.0, 3.0)']
- tv：GT ['(2.0, 6.0)'] | 模型 ['(5.0, 5.0)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(4.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- chair：GT ['(3.0, 3.0)'] | 模型 ['(7.0, 3.0)']
- tv：GT ['(7.0, 6.0)'] | 模型 ['(2.0, 5.0)']

### 样本 40 `42897528`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the washer and facing the refrigerator, is the sofa to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 B vs GT D（错误）
- 类别：refrigerator, sofa, washer
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.0, 3.0)']
- sofa：GT ['(5.0, 2.0)'] | 模型 ['(5.0, 7.0)']
- washer：GT ['(1.0, 7.0)'] | 模型 ['(8.0, 3.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.0, 5.0)']
- sofa：GT ['(5.0, 2.0)'] | 模型 ['(5.0, 2.0)']
- washer：GT ['(1.0, 2.0)'] | 模型 ['(8.0, 2.0)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(4.0, 4.0)'] | 模型 ['(3.0, 5.0)']
- sofa：GT ['(2.0, 2.0)'] | 模型 ['(7.0, 2.0)']
- washer：GT ['(7.0, 2.0)'] | 模型 ['(3.0, 2.0)']

### 样本 41 `scene0307_02`（scannet · object_rel_direction_hard）
- 问题：If I am standing by the chair and facing the refrigerator, is the washing machine to my front-left, front-right, back-left, or back-right?
The directi
- QA：模型 D vs GT D（正确）
- 类别：chair, refrigerator, washing machine
- tags：A2_extra, B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 6.0)'] | 模型 ['(4.0, 5.0)', '(5.0, 6.0)']
- refrigerator：GT ['(4.0, 2.0)'] | 模型 ['(2.0, 8.0)']
- washing machine：GT ['(2.0, 7.0)'] | 模型 ['(8.0, 2.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)'] | 模型 ['(4.0, 3.0)', '(5.0, 3.0)']
- refrigerator：GT ['(4.0, 3.0)'] | 模型 ['(2.0, 5.0)']
- washing machine：GT ['(2.0, 2.0)'] | 模型 ['(8.0, 3.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 3.0)', '(6.0, 3.0)']
- refrigerator：GT ['(2.0, 3.0)'] | 模型 ['(8.0, 5.0)']
- washing machine：GT ['(7.0, 2.0)'] | 模型 ['(2.0, 3.0)']

### 样本 42 `scene0164_02`（scannet · object_rel_direction_hard）
- 问题：If I am standing by the towel and facing the microwave, is the backpack to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 C vs GT D（错误）
- 类别：backpack, microwave, towel
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- backpack：GT ['(6.0, 1.0)'] | 模型 ['(8.0, 7.0)']
- microwave：GT ['(5.0, 7.0)'] | 模型 ['(3.0, 5.0)']
- towel：GT ['(5.0, 5.0)'] | 模型 ['(4.0, 2.0)']
**FRONT 视图**（GT → 模型）
- backpack：GT ['(6.0, 2.0)'] | 模型 ['(8.0, 2.0)']
- microwave：GT ['(5.0, 5.0)'] | 模型 ['(3.0, 5.0)']
- towel：GT ['(5.0, 3.0)'] | 模型 ['(4.0, 4.0)']
**SIDE 视图**（GT → 模型）
- backpack：GT ['(1.0, 2.0)'] | 模型 ['(7.0, 2.0)']
- microwave：GT ['(7.0, 5.0)'] | 模型 ['(5.0, 5.0)']
- towel：GT ['(5.0, 3.0)'] | 模型 ['(2.0, 4.0)']

### 样本 43 `47331668`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the bed and facing the tv, is the chair to my front-left, front-right, back-left, or back-right?
The directions refer to the quadr
- QA：模型 D vs GT B（错误）
- 类别：bed, chair, tv
- tags：B3_pair, B4_scale, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(6.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(3.0, 8.0)']
- tv：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 1.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(3.0, 3.0)']
- tv：GT ['(2.0, 6.0)'] | 模型 ['(5.0, 5.0)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(4.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- chair：GT ['(3.0, 3.0)'] | 模型 ['(8.0, 3.0)']
- tv：GT ['(7.0, 6.0)'] | 模型 ['(1.0, 5.0)']

### 样本 44 `c50d2d1d42`（scannetpp · object_rel_direction_hard）
- 问题：If I am standing by the telephone and facing the door, is the whiteboard to my front-left, front-right, back-left, or back-right?
The directions refer
- QA：模型 D vs GT C（错误）
- 类别：door, telephone, whiteboard
- tags：B3_pair, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(4.0, 7.0)']
- whiteboard：GT ['(5.0, 7.0)'] | 模型 ['(5.0, 2.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(4.0, 4.0)']
- whiteboard：GT ['(5.0, 4.0)'] | 模型 ['(5.0, 5.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(3.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- telephone：GT ['(3.0, 3.0)'] | 模型 ['(7.0, 4.0)']
- whiteboard：GT ['(7.0, 4.0)'] | 模型 ['(2.0, 5.0)']

### 样本 45 `47430468`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the stove and facing the stool, is the refrigerator to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 B vs GT D（错误）
- 类别：refrigerator, stool, stove
- tags：A1_miss, B3_pair, B4_scale, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(4.5, 4.5)']
- stool：GT ['(3.0, 5.0)'] | 模型 ['(5.0, 8.0)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(4.5, 4.5)']
- stool：GT ['(3.0, 1.0)'] | 模型 ['(5.0, 2.0)']
- stove：GT ['(1.0, 3.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(4.0, 4.0)'] | 模型 ['(4.5, 4.5)']
- stool：GT ['(5.0, 1.0)'] | 模型 ['(8.0, 2.0)']
- stove：GT ['(7.0, 3.0)'] | 模型 []

### 样本 46 `47334380`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the refrigerator and facing the stove, is the table to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 D vs GT D（正确）
- 类别：refrigerator, stove, table
- tags：B3_pair, C8_height
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 6.0)'] | 模型 ['(2.0, 8.0)']
- stove：GT ['(2.0, 1.0)'] | 模型 ['(3.0, 5.0)']
- table：GT ['(6.0, 5.0)'] | 模型 ['(6.0, 5.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 4.0)'] | 模型 ['(2.0, 5.0)']
- stove：GT ['(2.0, 4.0)'] | 模型 ['(3.0, 3.0)']
- table：GT ['(6.0, 2.0)'] | 模型 ['(6.0, 3.0)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 4.0)'] | 模型 ['(8.0, 5.0)']
- stove：GT ['(1.0, 4.0)'] | 模型 ['(5.0, 3.0)']
- table：GT ['(5.0, 2.0)'] | 模型 ['(5.0, 3.0)']

### 样本 47 `7b6477cb95`（scannetpp · object_rel_direction_hard）
- 问题：If I am standing by the telephone and facing the cup, is the trash can to my front-left, front-right, back-left, or back-right?
The directions refer t
- QA：模型 D vs GT A（错误）
- 类别：cup, telephone, trash can
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- cup：GT ['(5.0, 3.0)'] | 模型 ['(4.0, 3.0)']
- telephone：GT ['(6.0, 3.0)'] | 模型 ['(5.0, 4.0)']
- trash can：GT ['(3.0, 7.0)'] | 模型 ['(3.0, 8.0)']
**FRONT 视图**（GT → 模型）
- cup：GT ['(5.0, 2.0)'] | 模型 ['(4.0, 4.0)']
- telephone：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- trash can：GT ['(3.0, 1.0)'] | 模型 ['(3.0, 2.0)']
**SIDE 视图**（GT → 模型）
- cup：GT ['(3.0, 2.0)'] | 模型 ['(3.0, 4.0)']
- telephone：GT ['(3.0, 2.0)'] | 模型 ['(4.0, 4.0)']
- trash can：GT ['(7.0, 1.0)'] | 模型 ['(8.0, 2.0)']

### 样本 48 `47334096`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the stool and facing the tv, is the sofa to my front-left, front-right, back-left, or back-right?
The directions refer to the quad
- QA：模型 A vs GT C（错误）
- 类别：sofa, stool, tv
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- sofa：GT ['(4.0, 4.0)'] | 模型 ['(4.0, 6.0)']
- stool：GT ['(5.0, 1.0)'] | 模型 ['(4.0, 4.0)']
- tv：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 2.0)']
**FRONT 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 ['(4.0, 2.0)']
- stool：GT ['(5.0, 2.0)'] | 模型 ['(4.0, 1.0)']
- tv：GT ['(1.0, 6.0)'] | 模型 ['(5.0, 4.0)']
**SIDE 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 ['(6.0, 2.0)']
- stool：GT ['(1.0, 2.0)'] | 模型 ['(4.0, 1.0)']
- tv：GT ['(5.0, 6.0)'] | 模型 ['(2.0, 4.0)']

### 样本 49 `47331970`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the dishwasher and facing the refrigerator, is the table to my front-left, front-right, back-left, or back-right?
The directions r
- QA：模型 B vs GT A（错误）
- 类别：dishwasher, refrigerator, table
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- dishwasher：GT ['(1.0, 3.0)'] | 模型 ['(4.0, 5.0)']
- refrigerator：GT ['(3.0, 1.0)'] | 模型 ['(2.0, 8.0)']
- table：GT ['(2.0, 4.0)'] | 模型 ['(6.0, 3.0)']
**FRONT 视图**（GT → 模型）
- dishwasher：GT ['(1.0, 2.0)'] | 模型 ['(4.0, 2.0)']
- refrigerator：GT ['(3.0, 4.0)'] | 模型 ['(2.0, 5.0)']
- table：GT ['(2.0, 2.0)'] | 模型 ['(6.0, 2.0)']
**SIDE 视图**（GT → 模型）
- dishwasher：GT ['(3.0, 2.0)'] | 模型 ['(5.0, 2.0)']
- refrigerator：GT ['(1.0, 4.0)'] | 模型 ['(8.0, 5.0)']
- table：GT ['(4.0, 2.0)'] | 模型 ['(3.0, 2.0)']

### 样本 50 `scene0664_02`（scannet · object_rel_direction_hard）
- 问题：If I am standing by the mirror and facing the door, is the trash bin to my front-left, front-right, back-left, or back-right?
The directions refer to 
- QA：模型 D vs GT D（正确）
- 类别：door, mirror, trash bin
- tags：B3_pair
**TOP 视图**（GT → 模型）
- door：GT ['(4.0, 7.0)'] | 模型 ['(1.0, 5.0)']
- mirror：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 2.0)']
- trash bin：GT ['(3.0, 1.0)'] | 模型 ['(3.0, 8.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(4.0, 4.0)'] | 模型 ['(1.0, 5.0)']
- mirror：GT ['(1.0, 4.0)'] | 模型 ['(5.0, 6.0)']
- trash bin：GT ['(3.0, 1.0)'] | 模型 ['(3.0, 1.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- mirror：GT ['(5.0, 4.0)'] | 模型 ['(2.0, 6.0)']
- trash bin：GT ['(1.0, 1.0)'] | 模型 ['(8.0, 1.0)']

## Three-view（两阶段计数）

### 样本 1 `09c1414f1b`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the cutting board and the suitcase (in meters)?
- QA：模型 1.8 vs GT 1.8（正确）
- 类别：cutting board, suitcase
- tags：A1_miss, C7_missing
**TOP 视图**（GT → 模型）
- cutting board：GT ['(1.0, 2.0)'] | 模型 []
- suitcase：GT ['(2.0, 4.0)'] | 模型 ['(5.5, 6.5)']
**FRONT 视图**（GT → 模型）
- cutting board：GT ['(1.0, 5.0)'] | 模型 []
- suitcase：GT ['(2.0, 1.0)'] | 模型 ['(5.5, 3.5)']
**SIDE 视图**（GT → 模型）
- cutting board：GT ['(2.0, 5.0)'] | 模型 []
- suitcase：GT ['(4.0, 1.0)'] | 模型 ['(6.5, 3.5)']

### 样本 2 `47334103`（arkitscenes · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the table and the stool (in meters)?
- QA：模型 0.3 vs GT 3.7（错误）
- 类别：stool, table
- tags：A2_extra, B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- stool：GT ['(2.0, 2.0)'] | 模型 ['(3.5, 5.0)', '(6.5, 5.0)', '(5.0, 3.5)', '(5.0, 6.5)']
- table：GT ['(7.0, 1.0)'] | 模型 ['(5.0, 5.0)']
**FRONT 视图**（GT → 模型）
- stool：GT ['(2.0, 1.0)'] | 模型 ['(3.5, 3.0)', '(6.5, 3.0)', '(5.0, 3.0)', '(5.0, 3.0)']
- table：GT ['(7.0, 2.0)'] | 模型 ['(5.0, 4.0)']
**SIDE 视图**（GT → 模型）
- stool：GT ['(2.0, 1.0)'] | 模型 ['(5.0, 3.0)', '(5.0, 3.0)', '(3.5, 3.0)', '(6.5, 3.0)']
- table：GT ['(1.0, 2.0)'] | 模型 ['(5.0, 4.0)']

### 样本 3 `42897538`（arkitscenes · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the stool and the refrigerator (in meters)?
- QA：模型 1.8 vs GT 2.6（错误）
- 类别：refrigerator, stool
- tags：A2_extra, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(3.0, 7.0)'] | 模型 ['(2.5, 2.0)']
- stool：GT ['(3.0, 3.0)'] | 模型 ['(4.5, 5.0)', '(5.5, 5.0)', '(6.5, 5.0)', '(7.5, 5.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(3.0, 4.0)'] | 模型 ['(2.5, 5.5)']
- stool：GT ['(3.0, 1.0)'] | 模型 ['(4.5, 3.5)', '(5.5, 3.5)', '(6.5, 3.5)', '(7.5, 3.5)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(7.0, 4.0)'] | 模型 ['(2.0, 5.5)']
- stool：GT ['(3.0, 1.0)'] | 模型 ['(5.0, 3.5)', '(5.0, 3.5)', '(5.0, 3.5)', '(5.0, 3.5)']

### 样本 4 `scene0550_00`（scannet · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the door and the window (in meters)?
- QA：模型 2.8 vs GT 2.5（错误）
- 类别：door, window
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(4.0, 8.0)'] | 模型 ['(1.5, 5.0)']
- window：GT ['(5.0, 1.0)'] | 模型 ['(5.0, 8.5)']
**FRONT 视图**（GT → 模型）
- door：GT ['(4.0, 4.0)'] | 模型 ['(1.5, 4.5)']
- window：GT ['(5.0, 5.0)'] | 模型 ['(5.0, 6.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(8.0, 4.0)'] | 模型 ['(5.0, 4.5)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(8.5, 6.0)']

### 样本 5 `scene0378_01`（scannet · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the door and the clock (in meters)?
- QA：模型 1.3 vs GT 1.6（错误）
- 类别：clock, door
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- clock：GT ['(3.0, 2.0)'] | 模型 ['(5.0, 8.0)']
- door：GT ['(6.0, 1.0)'] | 模型 ['(3.0, 8.0)']
**FRONT 视图**（GT → 模型）
- clock：GT ['(3.0, 7.0)'] | 模型 ['(5.0, 7.0)']
- door：GT ['(6.0, 4.0)'] | 模型 ['(3.0, 4.0)']
**SIDE 视图**（GT → 模型）
- clock：GT ['(2.0, 7.0)'] | 模型 ['(8.0, 7.0)']
- door：GT ['(1.0, 4.0)'] | 模型 ['(8.0, 4.0)']

### 样本 6 `c49a8c6cff`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the trash can and the bed (in meters)?
- QA：模型 1.2 vs GT 0.7（错误）
- 类别：bed, trash can
- tags：QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(6.0, 5.0)'] | 模型 ['(5.0, 4.5)']
- trash can：GT ['(2.0, 6.0)'] | 模型 ['(2.5, 6.5)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- trash can：GT ['(2.0, 1.0)'] | 模型 ['(2.5, 2.5)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(5.0, 2.0)'] | 模型 ['(4.5, 3.5)']
- trash can：GT ['(6.0, 1.0)'] | 模型 ['(6.5, 2.5)']

### 样本 7 `3db0a1c8f3`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the blanket and the computer mouse (in meters)?
- QA：模型 1.8 vs GT 0.8（错误）
- 类别：blanket, computer mouse
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- blanket：GT ['(1.0, 1.0)'] | 模型 ['(3.0, 4.0)']
- computer mouse：GT ['(3.0, 3.0)'] | 模型 ['(7.0, 6.0)']
**FRONT 视图**（GT → 模型）
- blanket：GT ['(1.0, 2.0)'] | 模型 ['(3.0, 2.0)']
- computer mouse：GT ['(3.0, 2.0)'] | 模型 ['(7.0, 4.0)']
**SIDE 视图**（GT → 模型）
- blanket：GT ['(1.0, 2.0)'] | 模型 ['(4.0, 2.0)']
- computer mouse：GT ['(3.0, 2.0)'] | 模型 ['(6.0, 4.0)']

### 样本 8 `c50d2d1d42`（scannetpp · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the door and the telephone (in meters)?
- QA：模型 2.0 vs GT 4.6（错误）
- 类别：door, telephone
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 4.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 3.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(3.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- telephone：GT ['(3.0, 3.0)'] | 模型 ['(4.0, 3.0)']

### 样本 9 `scene0474_04`（scannet · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the table and the trash bin (in meters)?
- QA：模型 0.3 vs GT 1.9（错误）
- 类别：table, trash bin
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- table：GT ['(4.0, 6.0)'] | 模型 ['(5.5, 5.5)']
- trash bin：GT ['(6.0, 3.0)'] | 模型 ['(4.0, 5.0)']
**FRONT 视图**（GT → 模型）
- table：GT ['(4.0, 2.0)'] | 模型 ['(5.5, 3.5)']
- trash bin：GT ['(6.0, 1.0)'] | 模型 ['(4.0, 2.5)']
**SIDE 视图**（GT → 模型）
- table：GT ['(6.0, 2.0)'] | 模型 ['(5.5, 3.5)']
- trash bin：GT ['(3.0, 1.0)'] | 模型 ['(5.0, 2.5)']

### 样本 10 `47333899`（arkitscenes · object_abs_distance）
- 问题：Measuring from the closest point of each object, what is the distance between the table and the stove (in meters)?
- QA：模型 1.2 vs GT 0.9（错误）
- 类别：stove, table
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- stove：GT ['(2.0, 7.0)'] | 模型 ['(3.0, 4.0)']
- table：GT ['(2.0, 1.0)'] | 模型 ['(6.0, 6.0)']
**FRONT 视图**（GT → 模型）
- stove：GT ['(2.0, 4.0)'] | 模型 ['(3.0, 4.0)']
- table：GT ['(2.0, 2.0)'] | 模型 ['(6.0, 3.0)']
**SIDE 视图**（GT → 模型）
- stove：GT ['(7.0, 4.0)'] | 模型 ['(4.0, 4.0)']
- table：GT ['(1.0, 2.0)'] | 模型 ['(6.0, 3.0)']

### 样本 11 `scene0221_01`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (chair, bed, pillow, lamp) is the closest to the microwave?
- QA：模型 B vs GT B（正确）
- 类别：bed, chair, lamp, microwave, pillow
- tags：A1_miss, B3_pair, C7_missing
**TOP 视图**（GT → 模型）
- bed：GT ['(4.0, 3.0)', '(2.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- chair：GT ['(3.0, 6.0)', '(1.0, 6.0)', '(2.0, 7.0)'] | 模型 ['(2.5, 7.0)']
- lamp：GT ['(3.0, 1.0)', '(3.0, 0.0)'] | 模型 ['(3.0, 3.0)']
- microwave：GT ['(6.0, 1.0)'] | 模型 []
- pillow：GT ['(2.0, 1.0)', '(4.0, 1.0)', '(4.0, 1.0)', '(4.0, 1.0)', '(2.0, 1.0)'] | 模型 ['(4.5, 3.5)', '(5.5, 3.5)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(4.0, 2.0)', '(2.0, 3.0)'] | 模型 ['(5.0, 3.0)']
- chair：GT ['(3.0, 3.0)', '(1.0, 5.0)', '(2.0, 4.0)'] | 模型 ['(2.5, 3.5)']
- lamp：GT ['(3.0, 4.0)', '(3.0, 5.0)'] | 模型 ['(3.0, 5.0)', '(7.0, 5.0)']
- microwave：GT ['(6.0, 5.0)'] | 模型 []
- pillow：GT ['(2.0, 4.0)', '(4.0, 4.0)', '(4.0, 4.0)', '(4.0, 4.0)', '(2.0, 4.0)'] | 模型 ['(4.5, 4.0)', '(5.5, 4.0)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(3.0, 2.0)', '(3.0, 3.0)'] | 模型 ['(5.0, 3.0)']
- chair：GT ['(6.0, 3.0)', '(6.0, 5.0)', '(7.0, 4.0)'] | 模型 ['(7.0, 3.5)']
- lamp：GT ['(1.0, 4.0)', '(0.0, 5.0)'] | 模型 ['(3.0, 5.0)', '(3.0, 5.0)']
- microwave：GT ['(1.0, 5.0)'] | 模型 []
- pillow：GT ['(1.0, 4.0)', '(1.0, 4.0)', '(1.0, 4.0)', '(1.0, 4.0)', '(1.0, 4.0)'] | 模型 ['(3.5, 4.0)', '(3.5, 4.0)']

### 样本 12 `scene0307_02`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (window, chair, door, washing machine) is the closest to the radiator?
- QA：模型 A vs GT C（错误）
- 类别：chair, door, radiator, washing machine, window
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 6.0)'] | 模型 []
- door：GT ['(3.0, 5.0)', '(4.0, 7.0)', '(3.0, 5.0)', '(1.0, 7.0)', '(7.0, 3.0)'] | 模型 ['(2.0, 8.0)']
- radiator：GT ['(1.0, 5.0)'] | 模型 []
- washing machine：GT ['(2.0, 7.0)'] | 模型 ['(4.0, 4.0)']
- window：GT ['(4.0, 1.0)', '(2.0, 7.0)', '(4.0, 1.0)'] | 模型 ['(8.0, 5.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)'] | 模型 []
- door：GT ['(3.0, 4.0)', '(4.0, 4.0)', '(3.0, 4.0)', '(1.0, 4.0)', '(7.0, 4.0)'] | 模型 ['(2.0, 5.0)']
- radiator：GT ['(1.0, 3.0)'] | 模型 []
- washing machine：GT ['(2.0, 2.0)'] | 模型 ['(4.0, 3.0)']
- window：GT ['(4.0, 6.0)', '(2.0, 6.0)', '(4.0, 6.0)'] | 模型 ['(8.0, 6.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(6.0, 2.0)'] | 模型 []
- door：GT ['(5.0, 4.0)', '(7.0, 4.0)', '(5.0, 4.0)', '(7.0, 4.0)', '(3.0, 4.0)'] | 模型 ['(8.0, 5.0)']
- radiator：GT ['(5.0, 3.0)'] | 模型 []
- washing machine：GT ['(7.0, 2.0)'] | 模型 ['(4.0, 3.0)']
- window：GT ['(1.0, 6.0)', '(7.0, 6.0)', '(1.0, 6.0)'] | 模型 ['(5.0, 6.0)']

### 样本 13 `47429977`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (stove, chair, refrigerator, table) is the closest to the tv?
- QA：模型 B vs GT D（错误）
- 类别：chair, refrigerator, stove, table, tv
- tags：A1_miss, A2_extra, B3_pair, B4_scale, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 1.0)', '(3.0, 2.0)', '(3.0, 1.0)'] | 模型 ['(5.5, 6.5)', '(7.5, 6.5)', '(6.5, 5.5)', '(6.5, 7.5)']
- refrigerator：GT ['(2.0, 7.0)'] | 模型 ['(2.5, 2.5)']
- stove：GT ['(1.0, 3.0)'] | 模型 ['(4.5, 2.0)']
- table：GT ['(6.0, 4.0)', '(3.0, 1.0)'] | 模型 ['(6.5, 6.5)']
- tv：GT ['(6.0, 1.0)'] | 模型 []
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 3.0)', '(3.0, 3.0)', '(3.0, 3.0)'] | 模型 ['(5.5, 4.0)', '(7.5, 4.0)', '(6.5, 4.0)', '(6.5, 4.0)']
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.5, 6.0)']
- stove：GT ['(1.0, 5.0)'] | 模型 ['(4.5, 4.0)']
- table：GT ['(6.0, 2.0)', '(3.0, 3.0)'] | 模型 ['(6.5, 3.5)']
- tv：GT ['(6.0, 6.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- chair：GT ['(1.0, 3.0)', '(2.0, 3.0)', '(1.0, 3.0)'] | 模型 ['(6.5, 4.0)', '(6.5, 4.0)', '(5.5, 4.0)', '(7.5, 4.0)']
- refrigerator：GT ['(7.0, 4.0)'] | 模型 ['(2.5, 6.0)']
- stove：GT ['(3.0, 5.0)'] | 模型 ['(2.0, 4.0)']
- table：GT ['(4.0, 2.0)', '(1.0, 3.0)'] | 模型 ['(6.5, 3.5)']
- tv：GT ['(1.0, 6.0)'] | 模型 []

### 样本 14 `scene0653_00`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (window, monitor, table, keyboard) is the closest to the door?
- QA：模型 B vs GT C（错误）
- 类别：door, keyboard, monitor, table, window
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(7.0, 7.0)'] | 模型 ['(8.0, 2.0)']
- keyboard：GT ['(2.0, 3.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 5.5)']
- monitor：GT ['(1.0, 6.0)', '(2.0, 3.0)', '(2.0, 3.0)', '(6.0, 1.0)', '(7.0, 1.0)', '(6.0, 4.0)', '(6.0, 6.0)'] | 模型 ['(5.0, 4.8)']
- table：GT ['(1.0, 6.0)', '(2.0, 3.0)', '(6.0, 4.0)', '(2.0, 4.0)', '(7.0, 1.0)', '(6.0, 6.0)'] | 模型 ['(5.0, 5.0)']
- window：GT ['(1.0, 5.0)', '(1.0, 2.0)'] | 模型 ['(2.0, 5.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(7.0, 5.0)'] | 模型 ['(8.0, 4.5)']
- keyboard：GT ['(2.0, 2.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- monitor：GT ['(1.0, 3.0)', '(2.0, 3.0)', '(2.0, 3.0)', '(6.0, 3.0)', '(7.0, 3.0)', '(6.0, 3.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- table：GT ['(1.0, 2.0)', '(2.0, 2.0)', '(6.0, 2.0)', '(2.0, 1.0)', '(7.0, 2.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- window：GT ['(1.0, 5.0)', '(1.0, 5.0)'] | 模型 ['(2.0, 6.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(7.0, 5.0)'] | 模型 ['(2.0, 4.5)']
- keyboard：GT ['(3.0, 2.0)', '(2.0, 2.0)'] | 模型 ['(5.5, 4.0)']
- monitor：GT ['(6.0, 3.0)', '(3.0, 3.0)', '(3.0, 3.0)', '(1.0, 3.0)', '(1.0, 3.0)', '(4.0, 3.0)', '(6.0, 3.0)'] | 模型 ['(4.8, 5.0)']
- table：GT ['(6.0, 2.0)', '(3.0, 2.0)', '(4.0, 2.0)', '(4.0, 1.0)', '(1.0, 2.0)', '(6.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- window：GT ['(5.0, 5.0)', '(2.0, 5.0)'] | 模型 ['(5.0, 6.0)']

### 样本 15 `38d58a7a31`（scannetpp · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (telephone, heater, chair, ceiling light) is the closest to the trash can?
- QA：模型 C vs GT C（正确）
- 类别：ceiling light, chair, heater, telephone, trash can
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, C8_height
**TOP 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 1.0)', '(1.0, 2.0)', '(4.0, 6.0)', '(1.0, 3.0)', '(4.0, 5.0)', '(4.0, 3.0)', '(6.0, 1.0)', '(7.0, 6.0)', '(6.0, 4.0)', '(6.0, 3.0)'] | 模型 ['(3.5, 4.0)', '(6.5, 7.0)']
- chair：GT ['(1.0, 6.0)', '(3.0, 6.0)', '(4.0, 4.0)', '(5.0, 5.0)', '(6.0, 4.0)', '(2.0, 5.0)', '(2.0, 7.0)', '(5.0, 3.0)', '(4.0, 3.0)', '(4.0, 6.0)', '(6.0, 6.0)', '(6.0, 1.0)', '(1.0, 6.0)', '(6.0, 2.0)', '(3.0, 6.0)', '(4.0, 6.0)', '(1.0, 7.0)', '(2.0, 5.0)', '(5.0, 6.0)', '(3.0, 3.0)', '(5.0, 4.0)', '(6.0, 4.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(7.0, 3.0)', '(7.0, 6.0)', '(6.0, 6.0)', '(3.0, 5.0)', '(2.0, 2.0)', '(3.0, 5.0)', '(2.0, 3.0)', '(1.0, 7.0)', '(1.0, 7.0)', '(1.0, 6.0)', '(1.0, 6.0)', '(1.0, 6.0)'] | 模型 ['(4.0, 6.0)', '(6.0, 5.0)']
- heater：GT ['(7.0, 4.0)', '(8.0, 6.0)', '(7.0, 1.0)'] | 模型 ['(2.5, 4.5)']
- telephone：GT ['(7.0, 2.0)'] | 模型 ['(4.5, 5.5)']
- trash can：GT ['(1.0, 4.0)'] | 模型 ['(3.5, 6.5)']
**FRONT 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 7.0)', '(1.0, 7.0)', '(4.0, 8.0)', '(1.0, 8.0)', '(4.0, 7.0)', '(4.0, 7.0)', '(6.0, 8.0)', '(7.0, 7.0)', '(6.0, 8.0)', '(6.0, 7.0)'] | 模型 ['(3.5, 9.0)', '(6.5, 9.0)']
- chair：GT ['(1.0, 2.0)', '(3.0, 2.0)', '(4.0, 2.0)', '(5.0, 2.0)', '(6.0, 2.0)', '(2.0, 2.0)', '(2.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(4.0, 2.0)', '(6.0, 2.0)', '(6.0, 1.0)', '(1.0, 2.0)', '(6.0, 2.0)', '(3.0, 2.0)', '(4.0, 1.0)', '(1.0, 2.0)', '(2.0, 1.0)', '(5.0, 2.0)', '(3.0, 1.0)', '(5.0, 2.0)', '(6.0, 1.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(7.0, 2.0)', '(7.0, 2.0)', '(6.0, 2.0)', '(3.0, 2.0)', '(2.0, 2.0)', '(3.0, 2.0)', '(2.0, 2.0)', '(1.0, 2.0)', '(1.0, 2.0)', '(1.0, 2.0)', '(1.0, 2.0)', '(1.0, 1.0)'] | 模型 ['(4.0, 3.5)', '(6.0, 3.5)']
- heater：GT ['(7.0, 1.0)', '(8.0, 1.0)', '(7.0, 1.0)'] | 模型 ['(2.5, 3.5)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(4.5, 5.0)']
- trash can：GT ['(1.0, 1.0)'] | 模型 ['(3.5, 2.5)']
**SIDE 视图**（GT → 模型）
- ceiling light：GT ['(1.0, 7.0)', '(2.0, 7.0)', '(6.0, 8.0)', '(3.0, 8.0)', '(5.0, 7.0)', '(3.0, 7.0)', '(1.0, 8.0)', '(6.0, 7.0)', '(4.0, 8.0)', '(3.0, 7.0)'] | 模型 ['(4.0, 9.0)', '(7.0, 9.0)']
- chair：GT ['(6.0, 2.0)', '(6.0, 2.0)', '(4.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(5.0, 2.0)', '(7.0, 2.0)', '(3.0, 2.0)', '(3.0, 2.0)', '(6.0, 2.0)', '(6.0, 2.0)', '(1.0, 1.0)', '(6.0, 2.0)', '(2.0, 2.0)', '(6.0, 2.0)', '(6.0, 1.0)', '(7.0, 2.0)', '(5.0, 1.0)', '(6.0, 2.0)', '(3.0, 1.0)', '(4.0, 2.0)', '(4.0, 1.0)', '(2.0, 2.0)', '(2.0, 2.0)', '(3.0, 2.0)', '(6.0, 2.0)', '(6.0, 2.0)', '(5.0, 2.0)', '(2.0, 2.0)', '(5.0, 2.0)', '(3.0, 2.0)', '(7.0, 2.0)', '(7.0, 2.0)', '(6.0, 2.0)', '(6.0, 2.0)', '(6.0, 1.0)'] | 模型 ['(6.0, 3.5)', '(5.0, 3.5)']
- heater：GT ['(4.0, 1.0)', '(6.0, 1.0)', '(1.0, 1.0)'] | 模型 ['(4.5, 3.5)']
- telephone：GT ['(2.0, 3.0)'] | 模型 ['(5.5, 5.0)']
- trash can：GT ['(4.0, 1.0)'] | 模型 ['(6.5, 2.5)']

### 样本 16 `42899461`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (chair, sofa, fireplace, stove) is the closest to the tv?
- QA：模型 A vs GT A（正确）
- 类别：chair, fireplace, sofa, stove, tv
- tags：A1_miss, B3_pair, C7_missing, C8_height
**TOP 视图**（GT → 模型）
- chair：GT ['(7.0, 4.0)', '(7.0, 3.0)', '(2.0, 4.0)', '(1.0, 4.0)'] | 模型 ['(3.0, 4.5)', '(7.0, 4.5)', '(2.5, 7.0)', '(7.5, 7.0)']
- fireplace：GT ['(4.0, 8.0)'] | 模型 []
- sofa：GT ['(7.0, 6.0)'] | 模型 ['(5.0, 3.5)']
- stove：GT ['(1.0, 1.0)'] | 模型 []
- tv：GT ['(1.0, 7.0)'] | 模型 ['(5.0, 8.5)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(7.0, 3.0)', '(7.0, 3.0)', '(2.0, 4.0)', '(1.0, 4.0)'] | 模型 ['(3.0, 4.0)', '(7.0, 4.0)', '(2.5, 4.0)', '(7.5, 4.0)']
- fireplace：GT ['(4.0, 4.0)'] | 模型 []
- sofa：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 4.0)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
- tv：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 5.5)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(4.0, 3.0)', '(3.0, 3.0)', '(4.0, 4.0)', '(4.0, 4.0)'] | 模型 ['(4.5, 4.0)', '(4.5, 4.0)', '(7.0, 4.0)', '(7.0, 4.0)']
- fireplace：GT ['(8.0, 4.0)'] | 模型 []
- sofa：GT ['(6.0, 4.0)'] | 模型 ['(3.5, 4.0)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
- tv：GT ['(7.0, 5.0)'] | 模型 ['(8.5, 5.5)']

### 样本 17 `42899461`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (table, tv, sofa, stove) is the closest to the fireplace?
- QA：模型 B vs GT A（错误）
- 类别：fireplace, sofa, stove, table, tv
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- fireplace：GT ['(4.0, 8.0)'] | 模型 []
- sofa：GT ['(7.0, 6.0)'] | 模型 ['(5.0, 2.5)']
- stove：GT ['(1.0, 1.0)'] | 模型 []
- table：GT ['(6.0, 7.0)', '(1.0, 7.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 5.5)']
- tv：GT ['(1.0, 7.0)'] | 模型 ['(5.0, 8.5)']
**FRONT 视图**（GT → 模型）
- fireplace：GT ['(4.0, 4.0)'] | 模型 []
- sofa：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 3.5)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
- table：GT ['(6.0, 2.0)', '(1.0, 2.0)', '(6.0, 3.0)'] | 模型 ['(5.0, 2.5)']
- tv：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 6.0)']
**SIDE 视图**（GT → 模型）
- fireplace：GT ['(8.0, 4.0)'] | 模型 []
- sofa：GT ['(6.0, 4.0)'] | 模型 ['(2.5, 3.5)']
- stove：GT ['(1.0, 7.0)'] | 模型 []
- table：GT ['(7.0, 2.0)', '(7.0, 2.0)', '(3.0, 3.0)'] | 模型 ['(5.5, 2.5)']
- tv：GT ['(7.0, 5.0)'] | 模型 ['(8.5, 6.0)']

### 样本 18 `47430034`（arkitscenes · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (chair, stool, table, bed) is the closest to the tv?
- QA：模型 C vs GT C（正确）
- 类别：bed, chair, stool, table, tv
- tags：A1_miss, B3_pair, B4_scale, C7_missing, C8_height
**TOP 视图**（GT → 模型）
- bed：GT ['(5.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- chair：GT ['(5.0, 7.0)', '(6.0, 7.0)', '(1.0, 2.0)'] | 模型 ['(3.0, 7.0)']
- stool：GT ['(4.0, 3.0)'] | 模型 []
- table：GT ['(4.0, 3.0)', '(6.0, 7.0)', '(1.0, 2.0)'] | 模型 ['(3.0, 8.0)']
- tv：GT ['(7.0, 7.0)'] | 模型 ['(3.0, 9.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(5.0, 4.0)'] | 模型 ['(5.0, 3.0)']
- chair：GT ['(5.0, 3.0)', '(6.0, 3.0)', '(1.0, 2.0)'] | 模型 ['(3.0, 3.0)']
- stool：GT ['(4.0, 1.0)'] | 模型 []
- table：GT ['(4.0, 2.0)', '(6.0, 2.0)', '(1.0, 2.0)'] | 模型 ['(3.0, 3.0)']
- tv：GT ['(7.0, 6.0)'] | 模型 ['(3.0, 6.0)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(2.0, 4.0)'] | 模型 ['(4.0, 3.0)']
- chair：GT ['(7.0, 3.0)', '(7.0, 3.0)', '(2.0, 2.0)'] | 模型 ['(7.0, 3.0)']
- stool：GT ['(3.0, 1.0)'] | 模型 []
- table：GT ['(3.0, 2.0)', '(7.0, 2.0)', '(2.0, 2.0)'] | 模型 ['(8.0, 3.0)']
- tv：GT ['(7.0, 6.0)'] | 模型 ['(9.0, 6.0)']

### 样本 19 `scene0616_01`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (table, trash bin, chair, lamp) is the closest to the window?
- QA：模型 A vs GT A（正确）
- 类别：chair, lamp, table, trash bin, window
- tags：A1_miss, B3_pair, B4_scale, B5_adjacent, C7_missing, C8_height
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)', '(4.0, 2.0)', '(4.0, 3.0)', '(3.0, 5.0)', '(3.0, 4.0)', '(5.0, 6.0)', '(6.0, 5.0)'] | 模型 ['(4.0, 5.0)', '(6.0, 5.0)']
- lamp：GT ['(5.0, 1.0)'] | 模型 ['(3.0, 3.0)']
- table：GT ['(5.0, 1.0)', '(3.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- trash bin：GT ['(7.0, 4.0)', '(7.0, 4.0)'] | 模型 ['(3.0, 5.0)']
- window：GT ['(1.0, 3.0)'] | 模型 ['(5.0, 9.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)', '(4.0, 2.0)', '(4.0, 2.0)', '(3.0, 2.0)', '(3.0, 2.0)', '(5.0, 2.0)', '(6.0, 2.0)'] | 模型 ['(4.0, 4.0)', '(6.0, 4.0)']
- lamp：GT ['(5.0, 4.0)'] | 模型 ['(3.0, 6.0)']
- table：GT ['(5.0, 2.0)', '(3.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- trash bin：GT ['(7.0, 2.0)', '(7.0, 2.0)'] | 模型 ['(3.0, 2.0)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 6.0)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(2.0, 2.0)', '(2.0, 2.0)', '(3.0, 2.0)', '(5.0, 2.0)', '(4.0, 2.0)', '(6.0, 2.0)', '(5.0, 2.0)'] | 模型 ['(5.0, 4.0)', '(5.0, 4.0)']
- lamp：GT ['(1.0, 4.0)'] | 模型 ['(3.0, 6.0)']
- table：GT ['(1.0, 2.0)', '(3.0, 2.0)'] | 模型 ['(5.0, 4.0)']
- trash bin：GT ['(4.0, 2.0)', '(4.0, 2.0)'] | 模型 ['(5.0, 2.0)']
- window：GT ['(3.0, 5.0)'] | 模型 ['(9.0, 6.0)']

### 样本 20 `scene0651_02`（scannet · object_rel_distance）
- 问题：Measuring from the closest point of each object, which of these objects (counter, chair, table, trash bin) is the closest to the sofa?
- QA：模型 B vs GT C（错误）
- 类别：chair, counter, sofa, table, trash bin
- tags：A1_miss, B3_pair, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(7.0, 4.0)', '(5.0, 3.0)', '(5.0, 4.0)', '(6.0, 3.0)'] | 模型 ['(4.5, 5.5)', '(6.5, 5.5)', '(5.5, 4.5)', '(5.5, 6.5)']
- counter：GT ['(3.0, 6.0)'] | 模型 ['(2.0, 7.5)']
- sofa：GT ['(5.0, 1.0)'] | 模型 ['(3.5, 4.5)']
- table：GT ['(3.0, 2.0)', '(5.0, 3.0)'] | 模型 ['(5.5, 5.5)']
- trash bin：GT ['(1.0, 6.0)'] | 模型 ['(1.5, 8.5)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(7.0, 2.0)', '(5.0, 3.0)', '(5.0, 3.0)', '(6.0, 3.0)'] | 模型 ['(4.5, 2.5)', '(6.5, 2.5)', '(5.5, 2.5)', '(5.5, 2.5)']
- counter：GT ['(3.0, 5.0)'] | 模型 ['(2.0, 3.5)']
- sofa：GT ['(5.0, 3.0)'] | 模型 ['(3.5, 2.5)']
- table：GT ['(3.0, 1.0)', '(5.0, 2.0)'] | 模型 ['(5.5, 2.0)']
- trash bin：GT ['(1.0, 1.0)'] | 模型 ['(1.5, 1.5)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)', '(3.0, 3.0)', '(4.0, 3.0)', '(3.0, 3.0)'] | 模型 ['(5.5, 2.5)', '(5.5, 2.5)', '(4.5, 2.5)', '(6.5, 2.5)']
- counter：GT ['(6.0, 5.0)'] | 模型 ['(7.5, 3.5)']
- sofa：GT ['(1.0, 3.0)'] | 模型 ['(4.5, 2.5)']
- table：GT ['(2.0, 1.0)', '(3.0, 2.0)'] | 模型 ['(5.5, 2.0)']
- trash bin：GT ['(6.0, 1.0)'] | 模型 ['(8.5, 1.5)']

### 样本 21 `31a2c91c43`（scannetpp · object_rel_direction_easy）
- 问题：If I am standing by the ceiling light and facing the toilet, is the door to the left or the right of the toilet?
- QA：模型 A vs GT A（正确）
- 类别：ceiling light, door, toilet
- tags：B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- ceiling light：GT ['(5.0, 8.0)'] | 模型 ['(5.0, 5.0)']
- door：GT ['(2.0, 4.0)'] | 模型 ['(2.0, 8.0)']
- toilet：GT ['(6.0, 2.0)'] | 模型 ['(4.0, 3.0)']
**FRONT 视图**（GT → 模型）
- ceiling light：GT ['(5.0, 8.0)'] | 模型 ['(5.0, 9.0)']
- door：GT ['(2.0, 4.0)'] | 模型 ['(2.0, 5.0)']
- toilet：GT ['(6.0, 1.0)'] | 模型 ['(4.0, 2.0)']
**SIDE 视图**（GT → 模型）
- ceiling light：GT ['(8.0, 8.0)'] | 模型 ['(5.0, 9.0)']
- door：GT ['(4.0, 4.0)'] | 模型 ['(8.0, 5.0)']
- toilet：GT ['(2.0, 1.0)'] | 模型 ['(3.0, 2.0)']

### 样本 22 `scene0353_00`（scannet · object_rel_direction_easy）
- 问题：If I am standing by the bookshelf and facing the door, is the refrigerator to the left or the right of the door?
- QA：模型 A vs GT A（正确）
- 类别：bookshelf, door, refrigerator
- tags：A1_miss, C7_missing
**TOP 视图**（GT → 模型）
- bookshelf：GT ['(7.0, 1.0)'] | 模型 []
- door：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 1.5)']
- refrigerator：GT ['(5.0, 5.0)'] | 模型 []
**FRONT 视图**（GT → 模型）
- bookshelf：GT ['(7.0, 3.0)'] | 模型 []
- door：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- refrigerator：GT ['(5.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- bookshelf：GT ['(1.0, 3.0)'] | 模型 []
- door：GT ['(3.0, 4.0)'] | 模型 ['(1.5, 5.0)']
- refrigerator：GT ['(5.0, 2.0)'] | 模型 []

### 样本 23 `41159525`（arkitscenes · object_rel_direction_easy）
- 问题：If I am standing by the stove and facing the table, is the refrigerator to the left or the right of the table?
- QA：模型 A vs GT B（错误）
- 类别：refrigerator, stove, table
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 1.0)'] | 模型 ['(2.5, 3.5)']
- stove：GT ['(1.0, 1.0)'] | 模型 ['(4.5, 3.5)']
- table：GT ['(6.0, 5.0)'] | 模型 ['(5.5, 6.5)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 4.0)'] | 模型 ['(2.5, 5.5)']
- stove：GT ['(1.0, 4.0)'] | 模型 ['(4.5, 4.0)']
- table：GT ['(6.0, 2.0)'] | 模型 ['(5.5, 3.5)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 4.0)'] | 模型 ['(3.5, 5.5)']
- stove：GT ['(1.0, 4.0)'] | 模型 ['(3.5, 4.0)']
- table：GT ['(5.0, 2.0)'] | 模型 ['(6.5, 3.5)']

### 样本 24 `d755b3d9d8`（scannetpp · object_rel_direction_easy）
- 问题：If I am standing by the cup and facing the whiteboard, is the shoes to the left or the right of the whiteboard?
- QA：模型 A vs GT A（正确）
- 类别：cup, shoes, whiteboard
- tags：B3_pair
**TOP 视图**（GT → 模型）
- cup：GT ['(5.0, 1.0)'] | 模型 ['(4.5, 5.5)']
- shoes：GT ['(7.0, 4.0)'] | 模型 ['(3.5, 7.5)']
- whiteboard：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 2.0)']
**FRONT 视图**（GT → 模型）
- cup：GT ['(5.0, 2.0)'] | 模型 ['(4.5, 4.0)']
- shoes：GT ['(7.0, 0.0)'] | 模型 ['(3.5, 1.5)', '(4.5, 1.5)']
- whiteboard：GT ['(2.0, 4.0)'] | 模型 ['(5.0, 6.0)']
**SIDE 视图**（GT → 模型）
- cup：GT ['(1.0, 2.0)'] | 模型 ['(5.5, 4.0)']
- shoes：GT ['(4.0, 0.0)'] | 模型 ['(7.5, 1.5)', '(7.5, 1.5)']
- whiteboard：GT ['(7.0, 4.0)'] | 模型 ['(2.0, 6.0)']

### 样本 25 `47204578`（arkitscenes · object_rel_direction_easy）
- 问题：If I am standing by the tv and facing the table, is the stool to the left or the right of the table?
- QA：模型 A vs GT A（正确）
- 类别：stool, table, tv
- tags：A1_miss, B3_pair, C7_missing
**TOP 视图**（GT → 模型）
- stool：GT ['(1.0, 1.0)'] | 模型 []
- table：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 5.5)']
- tv：GT ['(3.0, 1.0)'] | 模型 ['(5.0, 5.5)']
**FRONT 视图**（GT → 模型）
- stool：GT ['(1.0, 1.0)'] | 模型 []
- table：GT ['(2.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- tv：GT ['(3.0, 6.0)'] | 模型 ['(5.0, 5.5)']
**SIDE 视图**（GT → 模型）
- stool：GT ['(1.0, 1.0)'] | 模型 []
- table：GT ['(7.0, 2.0)'] | 模型 ['(5.5, 3.5)']
- tv：GT ['(1.0, 6.0)'] | 模型 ['(5.5, 5.5)']

### 样本 26 `scene0458_00`（scannet · object_rel_direction_easy）
- 问题：If I am standing by the window and facing the door, is the mirror to the left or the right of the door?
- QA：模型 B vs GT B（正确）
- 类别：door, mirror, window
- tags：B3_pair, B4_scale, C8_height
**TOP 视图**（GT → 模型）
- door：GT ['(8.0, 6.0)'] | 模型 ['(2.5, 1.5)']
- mirror：GT ['(1.0, 6.0)'] | 模型 ['(5.0, 5.0)']
- window：GT ['(6.0, 1.0)'] | 模型 ['(7.5, 8.5)']
**FRONT 视图**（GT → 模型）
- door：GT ['(8.0, 5.0)'] | 模型 ['(2.5, 5.0)']
- mirror：GT ['(1.0, 4.0)'] | 模型 ['(5.0, 6.0)']
- window：GT ['(6.0, 5.0)'] | 模型 ['(7.5, 5.5)']
**SIDE 视图**（GT → 模型）
- door：GT ['(6.0, 5.0)'] | 模型 ['(1.5, 5.0)']
- mirror：GT ['(6.0, 4.0)'] | 模型 ['(5.0, 6.0)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(8.5, 5.5)']

### 样本 27 `scene0426_00`（scannet · object_rel_direction_easy）
- 问题：If I am standing by the tv and facing the lamp, is the table to the left or the right of the lamp?
- QA：模型 B vs GT A（错误）
- 类别：lamp, table, tv
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- lamp：GT ['(5.0, 1.0)'] | 模型 ['(4.5, 5.2)']
- table：GT ['(2.0, 7.0)'] | 模型 ['(5.5, 5.5)']
- tv：GT ['(7.0, 3.0)'] | 模型 ['(5.5, 5.8)']
**FRONT 视图**（GT → 模型）
- lamp：GT ['(5.0, 4.0)'] | 模型 ['(4.5, 4.8)']
- table：GT ['(2.0, 2.0)'] | 模型 ['(5.5, 3.5)']
- tv：GT ['(7.0, 4.0)'] | 模型 ['(5.5, 5.5)']
**SIDE 视图**（GT → 模型）
- lamp：GT ['(1.0, 4.0)'] | 模型 ['(5.2, 4.8)']
- table：GT ['(7.0, 2.0)'] | 模型 ['(5.5, 3.5)']
- tv：GT ['(3.0, 4.0)'] | 模型 ['(5.8, 5.5)']

### 样本 28 `scene0144_00`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the window and facing the lamp, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 1
- QA：模型 C vs GT C（正确）
- 类别：door, lamp, window
- tags：B3_pair, C8_height
**TOP 视图**（GT → 模型）
- door：GT ['(8.0, 1.0)'] | 模型 ['(1.5, 5.0)']
- lamp：GT ['(5.0, 7.0)'] | 模型 ['(5.0, 5.0)']
- window：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 8.5)']
**FRONT 视图**（GT → 模型）
- door：GT ['(8.0, 3.0)'] | 模型 ['(1.5, 4.5)']
- lamp：GT ['(5.0, 5.0)'] | 模型 ['(5.0, 7.5)']
- window：GT ['(1.0, 6.0)'] | 模型 ['(5.0, 5.5)']
**SIDE 视图**（GT → 模型）
- door：GT ['(1.0, 3.0)'] | 模型 ['(5.0, 4.5)']
- lamp：GT ['(7.0, 5.0)'] | 模型 ['(5.0, 7.5)']
- window：GT ['(5.0, 6.0)'] | 模型 ['(8.5, 5.5)']

### 样本 29 `scene0629_01`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the bed and facing the chair, is the mirror to my left, right, or back?
An object is to my back if I would have to turn at least 1
- QA：模型 B vs GT B（正确）
- 类别：bed, chair, mirror
- tags：C8_height
**TOP 视图**（GT → 模型）
- bed：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 4.5)']
- chair：GT ['(6.0, 7.0)'] | 模型 ['(2.5, 6.5)']
- mirror：GT ['(3.0, 6.0)'] | 模型 ['(1.5, 4.0)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 3.0)']
- chair：GT ['(6.0, 2.0)'] | 模型 ['(2.5, 3.5)']
- mirror：GT ['(3.0, 4.0)'] | 模型 ['(1.5, 6.5)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(4.0, 3.0)'] | 模型 ['(4.5, 3.0)']
- chair：GT ['(7.0, 2.0)'] | 模型 ['(6.5, 3.5)']
- mirror：GT ['(6.0, 4.0)'] | 模型 ['(4.0, 6.5)']

### 样本 30 `5ee7c22ba0`（scannetpp · object_rel_direction_medium）
- 问题：If I am standing by the refrigerator and facing the microwave, is the ceiling light to my left, right, or back?
An object is to my back if I would hav
- QA：模型 B vs GT B（正确）
- 类别：ceiling light, microwave, refrigerator
- tags：B3_pair, B4_scale
**TOP 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 3.0)'] | 模型 ['(3.0, 5.0)']
- microwave：GT ['(3.0, 1.0)'] | 模型 ['(4.0, 4.0)']
- refrigerator：GT ['(4.0, 7.0)'] | 模型 ['(2.0, 3.0)']
**FRONT 视图**（GT → 模型）
- ceiling light：GT ['(4.0, 8.0)'] | 模型 ['(3.0, 9.0)', '(7.0, 9.0)']
- microwave：GT ['(3.0, 3.0)'] | 模型 ['(4.0, 5.0)']
- refrigerator：GT ['(4.0, 2.0)'] | 模型 ['(2.0, 4.0)']
**SIDE 视图**（GT → 模型）
- ceiling light：GT ['(3.0, 8.0)'] | 模型 ['(5.0, 9.0)', '(5.0, 9.0)']
- microwave：GT ['(1.0, 3.0)'] | 模型 ['(4.0, 5.0)']
- refrigerator：GT ['(7.0, 2.0)'] | 模型 ['(3.0, 4.0)']

### 样本 31 `45261121`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the table and facing the tv, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 135
- QA：模型 C vs GT A（错误）
- 类别：stove, table, tv
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- stove：GT ['(3.0, 2.0)'] | 模型 ['(2.0, 3.0)']
- table：GT ['(5.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- tv：GT ['(7.0, 1.0)'] | 模型 ['(8.0, 8.0)']
**FRONT 视图**（GT → 模型）
- stove：GT ['(3.0, 3.0)'] | 模型 ['(2.0, 4.0)']
- table：GT ['(5.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- tv：GT ['(7.0, 7.0)'] | 模型 ['(8.0, 6.0)']
**SIDE 视图**（GT → 模型）
- stove：GT ['(2.0, 3.0)'] | 模型 ['(3.0, 4.0)']
- table：GT ['(4.0, 2.0)'] | 模型 ['(5.0, 3.0)']
- tv：GT ['(1.0, 7.0)'] | 模型 ['(8.0, 6.0)']

### 样本 32 `45b0dac5e3`（scannetpp · object_rel_direction_medium）
- 问题：If I am standing by the cup and facing the heater, is the toilet to my left, right, or back?
An object is to my back if I would have to turn at least 
- QA：模型 A vs GT C（错误）
- 类别：cup, heater, toilet
- tags：A1_miss, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- cup：GT ['(6.0, 1.0)'] | 模型 []
- heater：GT ['(0.0, 5.0)'] | 模型 []
- toilet：GT ['(7.0, 6.0)'] | 模型 ['(5.1, 8.2)']
**FRONT 视图**（GT → 模型）
- cup：GT ['(6.0, 3.0)'] | 模型 []
- heater：GT ['(0.0, 3.0)'] | 模型 []
- toilet：GT ['(7.0, 2.0)'] | 模型 ['(5.1, 4.2)']
**SIDE 视图**（GT → 模型）
- cup：GT ['(1.0, 3.0)'] | 模型 []
- heater：GT ['(5.0, 3.0)'] | 模型 []
- toilet：GT ['(6.0, 2.0)'] | 模型 ['(8.2, 4.2)']

### 样本 33 `scene0695_00`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the lamp and facing the pillow, is the table to my left, right, or back?
An object is to my back if I would have to turn at least 
- QA：模型 B vs GT C（错误）
- 类别：lamp, pillow, table
- tags：A2_extra, B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- lamp：GT ['(5.0, 1.0)'] | 模型 ['(2.5, 3.5)', '(7.5, 3.5)']
- pillow：GT ['(1.0, 2.0)'] | 模型 ['(4.0, 4.5)', '(6.0, 4.5)']
- table：GT ['(3.0, 7.0)'] | 模型 ['(2.5, 3.5)', '(7.5, 3.5)']
**FRONT 视图**（GT → 模型）
- lamp：GT ['(5.0, 4.0)'] | 模型 ['(2.5, 5.5)', '(7.5, 5.5)']
- pillow：GT ['(1.0, 4.0)'] | 模型 ['(4.0, 4.0)', '(6.0, 4.0)']
- table：GT ['(3.0, 2.0)'] | 模型 ['(2.5, 3.0)', '(7.5, 3.0)']
**SIDE 视图**（GT → 模型）
- lamp：GT ['(1.0, 4.0)'] | 模型 ['(3.5, 5.5)', '(3.5, 5.5)']
- pillow：GT ['(2.0, 4.0)'] | 模型 ['(4.5, 4.0)', '(4.5, 4.0)']
- table：GT ['(7.0, 2.0)'] | 模型 ['(3.5, 3.0)', '(3.5, 3.0)']

### 样本 34 `47334096`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the stool and facing the sofa, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 1
- QA：模型 A vs GT C（错误）
- 类别：sofa, stool, stove
- tags：A1_miss, B3_pair, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- sofa：GT ['(4.0, 4.0)'] | 模型 ['(3.5, 4.5)']
- stool：GT ['(5.0, 1.0)'] | 模型 []
- stove：GT ['(7.0, 6.0)'] | 模型 ['(7.5, 7.5)']
**FRONT 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 ['(3.5, 3.0)']
- stool：GT ['(5.0, 2.0)'] | 模型 []
- stove：GT ['(7.0, 5.0)'] | 模型 ['(7.5, 4.0)']
**SIDE 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 ['(4.5, 3.0)']
- stool：GT ['(1.0, 2.0)'] | 模型 []
- stove：GT ['(6.0, 5.0)'] | 模型 ['(7.5, 4.0)']

### 样本 35 `42446103`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the stove and facing the tv, is the stool to my left, right, or back?
An object is to my back if I would have to turn at least 135
- QA：模型 C vs GT A（错误）
- 类别：stool, stove, tv
- tags：A1_miss, B3_pair, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- stool：GT ['(3.0, 3.0)'] | 模型 []
- stove：GT ['(3.0, 7.0)'] | 模型 ['(4.0, 8.0)']
- tv：GT ['(8.0, 2.0)'] | 模型 ['(7.0, 4.0)']
**FRONT 视图**（GT → 模型）
- stool：GT ['(3.0, 1.0)'] | 模型 []
- stove：GT ['(3.0, 4.0)'] | 模型 ['(4.0, 4.0)']
- tv：GT ['(8.0, 7.0)'] | 模型 ['(7.0, 6.0)']
**SIDE 视图**（GT → 模型）
- stool：GT ['(3.0, 1.0)'] | 模型 []
- stove：GT ['(7.0, 4.0)'] | 模型 ['(8.0, 4.0)']
- tv：GT ['(2.0, 7.0)'] | 模型 ['(4.0, 6.0)']

### 样本 36 `42446049`（arkitscenes · object_rel_direction_medium）
- 问题：If I am standing by the washer and facing the refrigerator, is the stove to my left, right, or back?
An object is to my back if I would have to turn a
- QA：模型 B vs GT C（错误）
- 类别：refrigerator, stove, washer
- tags：A1_miss, B3_pair, B4_scale, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 6.0)'] | 模型 ['(3.5, 4.5)']
- stove：GT ['(6.0, 1.0)'] | 模型 ['(6.5, 5.5)']
- washer：GT ['(7.0, 7.0)'] | 模型 []
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 4.0)'] | 模型 ['(3.5, 5.0)']
- stove：GT ['(6.0, 4.0)'] | 模型 ['(6.5, 3.5)']
- washer：GT ['(7.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 4.0)'] | 模型 ['(4.5, 5.0)']
- stove：GT ['(1.0, 4.0)'] | 模型 ['(5.5, 3.5)']
- washer：GT ['(7.0, 2.0)'] | 模型 []

### 样本 37 `scene0144_00`（scannet · object_rel_direction_medium）
- 问题：If I am standing by the lamp and facing the printer, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 
- QA：模型 A vs GT C（错误）
- 类别：door, lamp, printer
- tags：A1_miss, B3_pair, B4_scale, C7_missing, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(8.0, 1.0)'] | 模型 ['(1.5, 9.0)']
- lamp：GT ['(5.0, 7.0)'] | 模型 ['(5.0, 4.0)']
- printer：GT ['(2.0, 3.0)', '(2.0, 3.0)'] | 模型 ['(4.5, 4.5)']
**FRONT 视图**（GT → 模型）
- door：GT ['(8.0, 3.0)'] | 模型 ['(1.5, 5.0)']
- lamp：GT ['(5.0, 5.0)'] | 模型 ['(5.0, 5.5)']
- printer：GT ['(2.0, 4.0)', '(2.0, 4.0)'] | 模型 ['(4.5, 3.5)']
**SIDE 视图**（GT → 模型）
- door：GT ['(1.0, 3.0)'] | 模型 ['(9.0, 5.0)']
- lamp：GT ['(7.0, 5.0)'] | 模型 ['(4.0, 5.5)']
- printer：GT ['(3.0, 4.0)', '(3.0, 4.0)'] | 模型 ['(4.5, 3.5)']

### 样本 38 `f9f95681fd`（scannetpp · object_rel_direction_medium）
- 问题：If I am standing by the door and facing the kettle, is the microwave to my left, right, or back?
An object is to my back if I would have to turn at le
- QA：模型 A vs GT C（错误）
- 类别：door, kettle, microwave
- tags：A1_miss, B3_pair, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(1.0, 3.0)'] | 模型 ['(1.0, 8.0)']
- kettle：GT ['(7.0, 3.0)'] | 模型 []
- microwave：GT ['(2.0, 6.0)'] | 模型 ['(4.0, 5.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(1.0, 4.0)'] | 模型 ['(1.0, 5.0)']
- kettle：GT ['(7.0, 3.0)'] | 模型 []
- microwave：GT ['(2.0, 3.0)'] | 模型 ['(4.0, 4.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(3.0, 4.0)'] | 模型 ['(8.0, 5.0)']
- kettle：GT ['(3.0, 3.0)'] | 模型 []
- microwave：GT ['(6.0, 3.0)'] | 模型 ['(5.0, 4.0)']

### 样本 39 `47331668`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the tv and facing the bed, is the chair to my front-left, front-right, back-left, or back-right?
The directions refer to the quadr
- QA：模型 A vs GT A（正确）
- 类别：bed, chair, tv
- tags：B3_pair, C8_height
**TOP 视图**（GT → 模型）
- bed：GT ['(6.0, 4.0)'] | 模型 ['(5.0, 4.5)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(2.5, 7.5)']
- tv：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 8.5)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(2.5, 3.0)']
- tv：GT ['(2.0, 6.0)'] | 模型 ['(5.0, 5.5)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(4.0, 2.0)'] | 模型 ['(4.5, 3.5)']
- chair：GT ['(3.0, 3.0)'] | 模型 ['(7.5, 3.0)']
- tv：GT ['(7.0, 6.0)'] | 模型 ['(8.5, 5.5)']

### 样本 40 `42897528`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the washer and facing the refrigerator, is the sofa to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 B vs GT D（错误）
- 类别：refrigerator, sofa, washer
- tags：A1_miss, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.5, 7.5)']
- sofa：GT ['(5.0, 2.0)'] | 模型 ['(5.5, 4.5)']
- washer：GT ['(1.0, 7.0)'] | 模型 []
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.5, 5.5)']
- sofa：GT ['(5.0, 2.0)'] | 模型 ['(5.5, 3.5)']
- washer：GT ['(1.0, 2.0)'] | 模型 []
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(4.0, 4.0)'] | 模型 ['(7.5, 5.5)']
- sofa：GT ['(2.0, 2.0)'] | 模型 ['(4.5, 3.5)']
- washer：GT ['(7.0, 2.0)'] | 模型 []

### 样本 41 `scene0307_02`（scannet · object_rel_direction_hard）
- 问题：If I am standing by the chair and facing the refrigerator, is the washing machine to my front-left, front-right, back-left, or back-right?
The directi
- QA：模型 C vs GT D（错误）
- 类别：chair, refrigerator, washing machine
- tags：A1_miss, C7_missing, QA_wrong
**TOP 视图**（GT → 模型）
- chair：GT ['(4.0, 6.0)'] | 模型 []
- refrigerator：GT ['(4.0, 2.0)'] | 模型 []
- washing machine：GT ['(2.0, 7.0)'] | 模型 ['(5.0, 5.0)']
**FRONT 视图**（GT → 模型）
- chair：GT ['(4.0, 2.0)'] | 模型 []
- refrigerator：GT ['(4.0, 3.0)'] | 模型 []
- washing machine：GT ['(2.0, 2.0)'] | 模型 ['(5.0, 4.5)']
**SIDE 视图**（GT → 模型）
- chair：GT ['(6.0, 2.0)'] | 模型 []
- refrigerator：GT ['(2.0, 3.0)'] | 模型 []
- washing machine：GT ['(7.0, 2.0)'] | 模型 ['(5.0, 4.5)']

### 样本 42 `scene0164_02`（scannet · object_rel_direction_hard）
- 问题：If I am standing by the towel and facing the microwave, is the backpack to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 A vs GT D（错误）
- 类别：backpack, microwave, towel
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- backpack：GT ['(6.0, 1.0)'] | 模型 ['(3.0, 6.0)']
- microwave：GT ['(5.0, 7.0)'] | 模型 ['(5.0, 4.0)']
- towel：GT ['(5.0, 5.0)'] | 模型 ['(4.0, 3.0)']
**FRONT 视图**（GT → 模型）
- backpack：GT ['(6.0, 2.0)'] | 模型 ['(3.0, 2.0)']
- microwave：GT ['(5.0, 5.0)'] | 模型 ['(5.0, 5.0)']
- towel：GT ['(5.0, 3.0)'] | 模型 ['(4.0, 4.0)']
**SIDE 视图**（GT → 模型）
- backpack：GT ['(1.0, 2.0)'] | 模型 ['(6.0, 2.0)']
- microwave：GT ['(7.0, 5.0)'] | 模型 ['(4.0, 5.0)']
- towel：GT ['(5.0, 3.0)'] | 模型 ['(3.0, 4.0)']

### 样本 43 `47331668`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the bed and facing the tv, is the chair to my front-left, front-right, back-left, or back-right?
The directions refer to the quadr
- QA：模型 C vs GT B（错误）
- 类别：bed, chair, tv
- tags：B3_pair, C8_height, QA_wrong
**TOP 视图**（GT → 模型）
- bed：GT ['(6.0, 4.0)'] | 模型 ['(4.5, 4.5)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(2.5, 7.5)']
- tv：GT ['(2.0, 7.0)'] | 模型 ['(7.5, 4.5)']
**FRONT 视图**（GT → 模型）
- bed：GT ['(6.0, 2.0)'] | 模型 ['(4.5, 3.5)']
- chair：GT ['(2.0, 3.0)'] | 模型 ['(2.5, 3.5)']
- tv：GT ['(2.0, 6.0)'] | 模型 ['(7.5, 6.5)']
**SIDE 视图**（GT → 模型）
- bed：GT ['(4.0, 2.0)'] | 模型 ['(4.5, 3.5)']
- chair：GT ['(3.0, 3.0)'] | 模型 ['(7.5, 3.5)']
- tv：GT ['(7.0, 6.0)'] | 模型 ['(4.5, 6.5)']

### 样本 44 `c50d2d1d42`（scannetpp · object_rel_direction_hard）
- 问题：If I am standing by the telephone and facing the door, is the whiteboard to my front-left, front-right, back-left, or back-right?
The directions refer
- QA：模型 A vs GT C（错误）
- 类别：door, telephone, whiteboard
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 4.0)']
- whiteboard：GT ['(5.0, 7.0)'] | 模型 ['(5.0, 1.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(0.0, 3.0)'] | 模型 ['(1.0, 5.0)']
- telephone：GT ['(7.0, 3.0)'] | 模型 ['(5.0, 3.0)']
- whiteboard：GT ['(5.0, 4.0)'] | 模型 ['(5.0, 6.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(3.0, 3.0)'] | 模型 ['(5.0, 5.0)']
- telephone：GT ['(3.0, 3.0)'] | 模型 ['(4.0, 3.0)']
- whiteboard：GT ['(7.0, 4.0)'] | 模型 ['(1.0, 6.0)']

### 样本 45 `47430468`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the stove and facing the stool, is the refrigerator to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 A vs GT D（错误）
- 类别：refrigerator, stool, stove
- tags：A2_extra, B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.5, 3.5)']
- stool：GT ['(3.0, 5.0)'] | 模型 ['(7.5, 6.5)', '(8.5, 6.5)']
- stove：GT ['(1.0, 7.0)'] | 模型 ['(5.5, 4.5)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(2.0, 4.0)'] | 模型 ['(2.5, 5.5)']
- stool：GT ['(3.0, 1.0)'] | 模型 ['(7.5, 3.0)', '(8.5, 3.0)']
- stove：GT ['(1.0, 3.0)'] | 模型 ['(5.5, 4.0)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(4.0, 4.0)'] | 模型 ['(3.5, 5.5)']
- stool：GT ['(5.0, 1.0)'] | 模型 ['(6.5, 3.0)', '(6.5, 3.0)']
- stove：GT ['(7.0, 3.0)'] | 模型 ['(4.5, 4.0)']

### 样本 46 `47334380`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the refrigerator and facing the stove, is the table to my front-left, front-right, back-left, or back-right?
The directions refer 
- QA：模型 D vs GT D（正确）
- 类别：refrigerator, stove, table
- tags：B3_pair
**TOP 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 6.0)'] | 模型 ['(2.0, 3.0)']
- stove：GT ['(2.0, 1.0)'] | 模型 ['(5.0, 3.0)']
- table：GT ['(6.0, 5.0)'] | 模型 ['(5.0, 7.0)']
**FRONT 视图**（GT → 模型）
- refrigerator：GT ['(1.0, 4.0)'] | 模型 ['(2.0, 6.0)']
- stove：GT ['(2.0, 4.0)'] | 模型 ['(5.0, 4.0)']
- table：GT ['(6.0, 2.0)'] | 模型 ['(5.0, 3.0)']
**SIDE 视图**（GT → 模型）
- refrigerator：GT ['(6.0, 4.0)'] | 模型 ['(3.0, 6.0)']
- stove：GT ['(1.0, 4.0)'] | 模型 ['(3.0, 4.0)']
- table：GT ['(5.0, 2.0)'] | 模型 ['(7.0, 3.0)']

### 样本 47 `7b6477cb95`（scannetpp · object_rel_direction_hard）
- 问题：If I am standing by the telephone and facing the cup, is the trash can to my front-left, front-right, back-left, or back-right?
The directions refer t
- QA：模型 B vs GT A（错误）
- 类别：cup, telephone, trash can
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- cup：GT ['(5.0, 3.0)'] | 模型 ['(6.2, 4.8)']
- telephone：GT ['(6.0, 3.0)'] | 模型 ['(4.5, 5.5)']
- trash can：GT ['(3.0, 7.0)'] | 模型 ['(3.5, 6.5)']
**FRONT 视图**（GT → 模型）
- cup：GT ['(5.0, 2.0)'] | 模型 ['(6.2, 5.1)']
- telephone：GT ['(6.0, 2.0)'] | 模型 ['(4.5, 5.2)']
- trash can：GT ['(3.0, 1.0)'] | 模型 ['(3.5, 2.2)']
**SIDE 视图**（GT → 模型）
- cup：GT ['(3.0, 2.0)'] | 模型 ['(4.8, 5.1)']
- telephone：GT ['(3.0, 2.0)'] | 模型 ['(5.5, 5.2)']
- trash can：GT ['(7.0, 1.0)'] | 模型 ['(6.5, 2.2)']

### 样本 48 `47334096`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the stool and facing the tv, is the sofa to my front-left, front-right, back-left, or back-right?
The directions refer to the quad
- QA：模型 B vs GT C（错误）
- 类别：sofa, stool, tv
- tags：B3_pair, QA_wrong
**TOP 视图**（GT → 模型）
- sofa：GT ['(4.0, 4.0)'] | 模型 ['(5.0, 3.0)']
- stool：GT ['(5.0, 1.0)'] | 模型 ['(3.5, 4.5)']
- tv：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 7.5)']
**FRONT 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 ['(5.0, 3.5)']
- stool：GT ['(5.0, 2.0)'] | 模型 ['(3.5, 2.5)']
- tv：GT ['(1.0, 6.0)'] | 模型 ['(5.0, 5.0)']
**SIDE 视图**（GT → 模型）
- sofa：GT ['(4.0, 2.0)'] | 模型 ['(3.0, 3.5)']
- stool：GT ['(1.0, 2.0)'] | 模型 ['(4.5, 2.5)']
- tv：GT ['(5.0, 6.0)'] | 模型 ['(7.5, 5.0)']

### 样本 49 `47331970`（arkitscenes · object_rel_direction_hard）
- 问题：If I am standing by the dishwasher and facing the refrigerator, is the table to my front-left, front-right, back-left, or back-right?
The directions r
- QA：模型 B vs GT A（错误）
- 类别：dishwasher, refrigerator, table
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- dishwasher：GT ['(1.0, 3.0)'] | 模型 ['(4.5, 4.0)']
- refrigerator：GT ['(3.0, 1.0)'] | 模型 ['(2.5, 3.5)']
- table：GT ['(2.0, 4.0)'] | 模型 ['(6.5, 6.5)']
**FRONT 视图**（GT → 模型）
- dishwasher：GT ['(1.0, 2.0)'] | 模型 ['(4.5, 3.5)']
- refrigerator：GT ['(3.0, 4.0)'] | 模型 ['(2.5, 5.5)']
- table：GT ['(2.0, 2.0)'] | 模型 ['(6.5, 3.0)']
**SIDE 视图**（GT → 模型）
- dishwasher：GT ['(3.0, 2.0)'] | 模型 ['(4.0, 3.5)']
- refrigerator：GT ['(1.0, 4.0)'] | 模型 ['(3.5, 5.5)']
- table：GT ['(4.0, 2.0)'] | 模型 ['(6.5, 3.0)']

### 样本 50 `scene0664_02`（scannet · object_rel_direction_hard）
- 问题：If I am standing by the mirror and facing the door, is the trash bin to my front-left, front-right, back-left, or back-right?
The directions refer to 
- QA：模型 C vs GT D（错误）
- 类别：door, mirror, trash bin
- tags：B3_pair, B4_scale, QA_wrong
**TOP 视图**（GT → 模型）
- door：GT ['(4.0, 7.0)'] | 模型 ['(2.0, 5.0)']
- mirror：GT ['(1.0, 5.0)'] | 模型 ['(5.0, 3.5)']
- trash bin：GT ['(3.0, 1.0)'] | 模型 ['(4.5, 3.0)']
**FRONT 视图**（GT → 模型）
- door：GT ['(4.0, 4.0)'] | 模型 ['(2.0, 5.0)']
- mirror：GT ['(1.0, 4.0)'] | 模型 ['(5.0, 6.5)']
- trash bin：GT ['(3.0, 1.0)'] | 模型 ['(4.5, 2.0)']
**SIDE 视图**（GT → 模型）
- door：GT ['(7.0, 4.0)'] | 模型 ['(5.0, 5.0)']
- mirror：GT ['(5.0, 4.0)'] | 模型 ['(3.5, 6.5)']
- trash bin：GT ['(1.0, 1.0)'] | 模型 ['(3.0, 2.0)']
