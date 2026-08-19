# 三视图 vs TIS vs GT — Failure Case Analysis

基于逐样本对照 `map-compare-detailed.md`

## 0. 指标

所有指标都在 10×10 网格上计算；A/B 类只看 TOP 视图，C 类只用于三视图。

| 标签 |  含义|
|---|---|
| A1 漏实例 | 给定类别集合下，模型画出的实例数少于 GT |
| A2 多/误实例 | 模型画出的实例数多于 GT，或画了类别集合外的物体 |
| B3 对偶距离错误 | 两个类别之间的欧氏距离与 GT 差超过 1 格。对每个类别对取任意实例两两距离的最小值，模型和 GT 各算一次。 |
| B4 尺度漂移 | 整张地图的对偶距离系统性偏大或偏小 |
| B5 紧邻对错误 | GT 中相邻（≤1 格）的类别对距离画错 |
| C6 跨视图坐标冲突 | 同一物体在 top/front/side 之间坐标差超过 1 格 |
| C7 跨视图漏画 | 物体没有在三个视图里都出现 |
| C8 高度排序错误 | front/side 的 z 高度顺序与 GT 不一致 |
| QA_wrong | 答案错误（交叉参考标签，不单独判定地图） |
| QA_map_clean | 答案正确且地图相对指标无异常 |
| MAP_PARSE_FAIL | 模型输出无法解析成地图 JSON |

## 1. 概览

### 1.1 QA

| Arm | 总体 | abs 精确 | abs MRA | rel_dist | dir_easy | dir_medium | dir_hard |
|---|---|---|---|---|---|---|---|
| baseline | 24.0% | 0/10 | 22% | 2/10 | 4/7 | 3/11 | 3/12 |
| threeview | 30.0% | 0/10 | 19% | 2/10 | 2/7 | 6/11 | 5/12 |
| threeview_3pass | 34.0% | 1/10 | 33% | 4/10 | 2/7 | 7/11 | 3/12 |
| threeview_2stage | 32.0% | 1/10 | 33% | 5/10 | 5/7 | 3/11 | 2/12 |

### 1.2 地图指标

| 指标 | baseline | threeview | threeview_3pass | threeview_2stage |
|---|---|---|---|---|
| 漏实例率 | 38.0% | 39.1% | 36.4% | 41.9% |
| 多实例率 | 2.7% | 0.8% | 2.7% | 4.3% |
| 对偶距离准确率 | 38.4% | 36.7% | 37.9% | 44.1% |
| 紧邻对准确率 | 28.0% | 32.0% | 20.0% | 54.2% |
| 尺度中位数 | 1.12 | 0.92 | 1.12 | 0.86 |
| 跨视图缺失率 | - | 39.1% | 36.4% | 41.6% |
| 高度排序准确率 | - | 89.4% | 75.8% | 86.3% |

## 2. 分错误类型案例

### A1 漏实例

涉及样本数：55（baseline#11, baseline#12, baseline#13, baseline#14, baseline#15, baseline#16, baseline#17, baseline#18, baseline#19, baseline#20, baseline#37, threeview#11, threeview#12, threeview#13, threeview#14, threeview#15, threeview#16, threeview#17, threeview#18, threeview#19）

#### baseline #11 `scene0221_01`（scannet · object_rel_distance）
- QA：模型 A vs GT B（错误）
- 诊断：
  - 漏 bed ×1（GT 2 个，模型 1 个）
  - 漏 chair ×2（GT 3 个，模型 1 个）
  - 漏 lamp ×1（GT 2 个，模型 1 个）
  - 漏 pillow ×4（GT 5 个，模型 1 个）

#### baseline #12 `scene0307_02`（scannet · object_rel_distance）
- QA：模型 A vs GT C（错误）
- 诊断：
  - 漏 door ×4（GT 5 个，模型 1 个）
  - 漏 window ×2（GT 3 个，模型 1 个）

#### baseline #13 `47429977`（arkitscenes · object_rel_distance）
- QA：模型 B vs GT D（错误）
- 诊断：
  - 漏 table ×1（GT 2 个，模型 1 个）
  - 多画 chair ×1（GT 3 个，模型 4 个）

#### baseline #14 `scene0653_00`（scannet · object_rel_distance）
- QA：模型 B vs GT C（错误）
- 诊断：
  - 漏 keyboard ×1（GT 2 个，模型 1 个）
  - 漏 monitor ×6（GT 7 个，模型 1 个）
  - 漏 table ×5（GT 6 个，模型 1 个）
  - 漏 window ×1（GT 2 个，模型 1 个）


**漏得最多的实例**：chair×190、table×48、ceiling light×35、monitor×24。其中 chair 是绝对大头（baseline=49、threeview=51、threeview_3pass=45、threeview_2stage=45，合计 190）。这些全是高频多实例类别——一个场景常有 3~7 把椅子、多张桌/灯/显示器，而模型普遍只画 1~2 个；单实例类别（suitcase、clock、backpack 等）基本不漏。

### A2 多画实例

涉及样本数：21（baseline#2, baseline#3, baseline#13, baseline#25, baseline#33, baseline#35, baseline#41, threeview#2, threeview#13, threeview_2stage#2, threeview_2stage#3, threeview_2stage#13, threeview_2stage#33, threeview_2stage#45, threeview_3pass#2, threeview_3pass#3, threeview_3pass#13, threeview_3pass#25, threeview_3pass#33, threeview_3pass#34）

#### baseline #2 `47334103`（arkitscenes · object_abs_distance）
- QA：模型 0.3 vs GT 3.7（错误）
- 诊断：
  - 多画 stool ×1（GT 1 个，模型 2 个）

#### baseline #3 `42897538`（arkitscenes · object_abs_distance）
- QA：模型 1.5 vs GT 2.6（错误）
- 诊断：
  - 多画 stool ×1（GT 1 个，模型 2 个）

#### baseline #13 `47429977`（arkitscenes · object_rel_distance）
- QA：模型 B vs GT D（错误）
- 诊断：
  - 漏 table ×1（GT 2 个，模型 1 个）
  - 多画 chair ×1（GT 3 个，模型 4 个）

#### baseline #25 `47204578`（arkitscenes · object_rel_direction_easy）
- QA：模型 A vs GT A（正确）
- 诊断：
  - 多画 stool ×1（GT 1 个，模型 2 个）


### B3/B4 对偶距离与尺度漂移

涉及样本数：173（baseline#1, baseline#2, baseline#4, baseline#5, baseline#8, baseline#10, baseline#11, baseline#12, baseline#13, baseline#14, baseline#15, baseline#16, baseline#17, baseline#18, baseline#19, baseline#20, baseline#22, baseline#23, baseline#24, baseline#25）

#### baseline #1 `09c1414f1b`（scannetpp · object_abs_distance）
- QA：模型 1.3 vs GT 1.8（错误）
- 诊断：
  - (cutting board,suitcase) 对偶距离 GT=2.2 模型=3.6 差=1.4 格

#### baseline #2 `47334103`（arkitscenes · object_abs_distance）
- QA：模型 0.3 vs GT 3.7（错误）
- 诊断：
  - (stool,table) 对偶距离 GT=5.1 模型=1.0 差=4.1 格

#### baseline #4 `scene0550_00`（scannet · object_abs_distance）
- QA：模型 3.5 vs GT 2.5（错误）
- 诊断：
  - (door,window) 对偶距离 GT=7.1 模型=5.7 差=1.4 格

#### baseline #5 `scene0378_01`（scannet · object_abs_distance）
- QA：模型 2.0 vs GT 1.6（错误）
- 诊断：
  - (clock,door) 对偶距离 GT=3.2 模型=4.5 差=1.3 格

#### baseline #8 `c50d2d1d42`（scannetpp · object_abs_distance）
- QA：模型 2.0 vs GT 4.6（错误）
- 诊断：
  - (door,telephone) 对偶距离 GT=7.0 模型=4.1 差=2.9 格


### B5 紧邻对错误

涉及样本数：28（baseline#12, baseline#14, baseline#15, baseline#17, baseline#18, baseline#19, baseline#20, threeview#11, threeview#12, threeview#14, threeview#15, threeview#17, threeview#18, threeview#19, threeview#20, threeview_2stage#12, threeview_2stage#14, threeview_2stage#15, threeview_2stage#17, threeview_2stage#19）

#### baseline #12 `scene0307_02`（scannet · object_rel_distance）
- QA：模型 A vs GT C（错误）
- 诊断：
  - (chair,door) 对偶距离 GT=1.0 模型=4.1 差=3.1 格
  - (chair,radiator) 对偶距离 GT=3.2 模型=4.2 差=1.1 格
  - (chair,window) 对偶距离 GT=2.2 模型=5.8 差=3.6 格
  - (door,radiator) 对偶距离 GT=2.0 模型=7.3 差=5.3 格
  - (door,washing machine) 对偶距离 GT=1.0 模型=3.6 差=2.6 格
  - (door,window) 对偶距离 GT=1.0 模型=8.1 差=7.1 格
  - (radiator,washing machine) 对偶距离 GT=2.2 模型=7.1 差=4.8 格
  - (washing machine,window) 对偶距离 GT=0.0 模型=8.6 差=8.6 格

#### baseline #14 `scene0653_00`（scannet · object_rel_distance）
- QA：模型 B vs GT C（错误）
- 诊断：
  - (door,monitor) 对偶距离 GT=1.4 模型=4.1 差=2.7 格
  - (door,table) 对偶距离 GT=1.4 模型=4.5 差=3.1 格
  - (door,window) 对偶距离 GT=6.3 模型=8.2 差=1.9 格
  - (keyboard,monitor) 对偶距离 GT=0.0 模型=2.0 差=2.0 格
  - (keyboard,window) 对偶距离 GT=1.4 模型=5.0 差=3.6 格
  - (monitor,table) 对偶距离 GT=0.0 模型=3.0 差=3.0 格
  - (monitor,window) 对偶距离 GT=1.0 模型=4.1 差=3.1 格
  - (table,window) 对偶距离 GT=1.0 模型=5.7 差=4.7 格

#### baseline #15 `38d58a7a31`（scannetpp · object_rel_distance）
- QA：模型 A vs GT C（错误）
- 诊断：
  - (ceiling light,chair) 对偶距离 GT=0.0 模型=5.1 差=5.1 格
  - (ceiling light,heater) 对偶距离 GT=1.0 模型=7.2 差=6.2 格
  - (ceiling light,telephone) 对偶距离 GT=1.4 模型=4.0 差=2.6 格
  - (ceiling light,trash can) 对偶距离 GT=1.0 模型=7.6 差=6.6 格
  - (chair,heater) 对偶距离 GT=1.0 模型=3.2 差=2.2 格
  - (chair,trash can) 对偶距离 GT=1.4 模型=4.5 差=3.1 格
  - (heater,telephone) 对偶距离 GT=1.0 模型=4.5 差=3.5 格
  - (heater,trash can) 对偶距离 GT=6.0 模型=7.1 差=1.1 格

#### baseline #17 `42899461`（arkitscenes · object_rel_distance）
- QA：模型 B vs GT A（错误）
- 诊断：
  - (sofa,table) 对偶距离 GT=1.4 模型=3.0 差=1.6 格
  - (table,tv) 对偶距离 GT=0.0 模型=3.0 差=3.0 格


### C7 跨视图漏画

涉及样本数：23（threeview#11, threeview#12, threeview#13, threeview#14, threeview#15, threeview#16, threeview#17, threeview#18, threeview#19, threeview#20, threeview#37, threeview_3pass#11, threeview_3pass#12, threeview_3pass#13, threeview_3pass#14, threeview_3pass#15, threeview_3pass#16, threeview_3pass#17, threeview_3pass#18, threeview_3pass#19）

#### threeview #11 `scene0221_01`（scannet · object_rel_distance）
- QA：模型 A vs GT B（错误）
- 诊断：
  - microwave：T无 / F无 / S无

#### threeview #12 `scene0307_02`（scannet · object_rel_distance）
- QA：模型 A vs GT C（错误）

#### threeview #13 `47429977`（arkitscenes · object_rel_distance）
- QA：模型 B vs GT D（错误）

#### threeview #14 `scene0653_00`（scannet · object_rel_distance）
- QA：模型 D vs GT C（错误）

#### threeview #15 `38d58a7a31`（scannetpp · object_rel_distance）
- QA：模型 C vs GT C（正确）


### C8 高度排序错误

涉及样本数：35（threeview#12, threeview#13, threeview#14, threeview#16, threeview#18, threeview#20, threeview#26, threeview#28, threeview#36, threeview#37, threeview#42, threeview#43, threeview_3pass#10, threeview_3pass#11, threeview_3pass#12, threeview_3pass#13, threeview_3pass#14, threeview_3pass#15, threeview_3pass#16, threeview_3pass#17）

#### threeview #12 `scene0307_02`（scannet · object_rel_distance）
- QA：模型 A vs GT C（错误）
- 诊断：
  - (radiator,washing machine) GT z 3>2，模型 4.0<4.5

#### threeview #13 `47429977`（arkitscenes · object_rel_distance）
- QA：模型 B vs GT D（错误）
- 诊断：
  - (chair,table) GT z 3>2，模型 3.0<4.0
  - (refrigerator,stove) GT z 4<5，模型 6.0>4.0
  - (refrigerator,tv) GT z 4<6，模型 6.0>5.0
  - (stove,table) GT z 5>2，模型 4.0<4.0

#### threeview #14 `scene0653_00`（scannet · object_rel_distance）
- QA：模型 D vs GT C（错误）
- 诊断：
  - (door,monitor) GT z 5>3，模型 5.0<5.5

#### threeview #16 `42899461`（arkitscenes · object_rel_distance）
- QA：模型 C vs GT A（错误）
- 诊断：
  - (chair,sofa) GT z 3<4，模型 3.0<3.0

#### threeview #18 `47430034`（arkitscenes · object_rel_distance）
- QA：模型 D vs GT C（错误）
- 诊断：
  - (bed,chair) GT z 4>3，模型 3.0<3.5
  - (bed,table) GT z 4>2，模型 3.0<3.0


## 3. 结论

1. 三视图（单次/3-pass）整体高于 TIS 俯视 baseline，但幅度小、分题型有升有降。
2. 三类地图共同的系统性问题是漏画实例和长距离对偶误差；三视图额外有跨视图漏画。