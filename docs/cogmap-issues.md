# cogmap 建图问题清单（case-level，50 样本）

> 对齐后离散诊断转成的可检查问题；连续残差不出现。

## 1. 各类问题出现样本数（top10 / arm）

### baseline

| 问题类型 | 样本数 |
|---|---|
| door-window 距离画错 | 5 |
| bed→chair 方向错 | 5 |
| 多画 stool ×1 | 4 |
| stove-table 距离画错 | 4 |
| refrigerator-stove 距离画错 | 4 |
| table→tv 方向错 | 4 |
| table-tv 距离画错 | 4 |
| 漏画 chair ×2 | 3 |
| door→window 方向错 | 3 |
| 漏画 table ×1 | 3 |

### threeview

| 问题类型 | 样本数 |
|---|---|
| z 整体偏高 | 43 |
| door-window 距离画错 | 5 |
| table-tv 距离画错 | 5 |
| stove-table 距离画错 | 4 |
| chair→table 方向错 | 4 |
| chair-tv 距离画错 | 4 |
| refrigerator-stove 距离画错 | 4 |
| 漏画 table ×1 | 3 |
| chair→tv 方向错 | 3 |
| table→tv 方向错 | 3 |

### threeview_3pass

| 问题类型 | 样本数 |
|---|---|
| z 整体偏高 | 25 |
| stove-table 距离画错 | 5 |
| z 整体偏低 | 5 |
| 多画 stool ×1 | 4 |
| chair→table 方向错 | 4 |
| refrigerator-stove 距离画错 | 4 |
| refrigerator→stove 方向错 | 4 |
| door-window 距离画错 | 3 |
| 漏画 chair ×2 | 3 |
| bed→chair 方向错 | 3 |

## 2. 逐样本问题清单

### baseline

- `09c1414f1b`（object_abs_distance）：cutting board-suitcase 距离画错（GT 2.2，模型 3.6）
- `47334103`（object_abs_distance）：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 5.1，模型 1.0）；stool→table 方向错（GT W，模型 N）
- `42897538`（object_abs_distance）：多画 stool ×1（GT 1，模型 2）
- `scene0550_00`（object_abs_distance）：door-window 距离画错（GT 7.1，模型 5.7）
- `scene0378_01`（object_abs_distance）：clock-door 距离画错（GT 3.2，模型 4.5）
- `c50d2d1d42`（object_abs_distance）：door-telephone 距离画错（GT 7.0，模型 4.1）
- `47333899`（object_abs_distance）：stove-table 距离画错（GT 6.0，模型 3.2）
- `scene0221_01`（object_rel_distance）：漏画 lamp ×1（GT 2，模型 1）；漏画 pillow ×4（GT 5，模型 1）；漏画 bed ×1（GT 2，模型 1）；漏画 chair ×2（GT 3，模型 1）；bed→chair 方向错（GT S，模型 SW）；bed→lamp 方向错（GT N，模型 E）
- `scene0307_02`（object_rel_distance）：漏画 window ×2（GT 3，模型 1）；漏画 door ×4（GT 5，模型 1）；chair-door 距离画错（GT 1.0，模型 4.1）；chair→door 方向错（GT NE，模型 E）；chair-radiator 距离画错（GT 3.2，模型 4.2）；chair→radiator 方向错（GT E，模型 N）
- `47429977`（object_rel_distance）：多画 chair ×1（GT 3，模型 4）；漏画 table ×1（GT 2，模型 1）；chair→refrigerator 方向错（GT S，模型 SE）；chair-stove 距离画错（GT 2.2，模型 3.6）；chair→table 方向错（GT SW，模型 S）；chair→tv 方向错（GT W，模型 N）
- `scene0653_00`（object_rel_distance）：漏画 window ×1（GT 2，模型 1）；漏画 monitor ×6（GT 7，模型 1）；漏画 keyboard ×1（GT 2，模型 1）；漏画 table ×5（GT 6，模型 1）；door→keyboard 方向错（GT NE，模型 N）；door-monitor 距离画错（GT 1.4，模型 4.1）
- `38d58a7a31`（object_rel_distance）：漏画 ceiling light ×9（GT 10，模型 1）；漏画 heater ×2（GT 3，模型 1）；漏画 chair ×35（GT 36，模型 1）；ceiling light-chair 距离画错（GT 0.0，模型 5.1）；ceiling light→chair 方向错（GT SE，模型 S）；ceiling light-heater 距离画错（GT 1.0，模型 7.2）
- `42899461`（object_rel_distance）：漏画 stove ×1（GT 1，模型 0）；漏画 chair ×3（GT 4，模型 1）；chair→sofa 方向错（GT SW，模型 W）；chair→tv 方向错（GT SE，模型 S）；fireplace-sofa 距离画错（GT 3.6，模型 5.0）；fireplace-tv 距离画错（GT 3.2，模型 1.0）
- `42899461`（object_rel_distance）：漏画 stove ×1（GT 1，模型 0）；漏画 fireplace ×1（GT 1，模型 0）；漏画 table ×2（GT 3，模型 1）；sofa-table 距离画错（GT 1.4，模型 3.0）；table-tv 距离画错（GT 0.0，模型 3.0）
- `47430034`（object_rel_distance）：漏画 stool ×1（GT 1，模型 0）；漏画 chair ×2（GT 3，模型 1）；漏画 table ×2（GT 3，模型 1）；bed→chair 方向错（GT S，模型 SE）；bed-table 距离画错（GT 1.4，模型 2.8）；bed-tv 距离画错（GT 5.4，模型 3.2）
- `scene0616_01`（object_rel_distance）：漏画 trash bin ×1（GT 2，模型 1）；漏画 chair ×5（GT 7，模型 2）；漏画 table ×1（GT 2，模型 1）；chair-lamp 距离画错（GT 1.4，模型 2.8）；chair→lamp 方向错（GT N，模型 NW）；chair→table 方向错（GT N，模型 E）
- `scene0651_02`（object_rel_distance）：漏画 chair ×2（GT 4，模型 2）；漏画 table ×1（GT 2，模型 1）；chair-sofa 距离画错（GT 2.0，模型 3.6）；chair-table 距离画错（GT 0.0，模型 2.0）；chair→table 方向错（GT NE，模型 E）；counter-sofa 距离画错（GT 5.4，模型 7.2）
- `31a2c91c43`（object_rel_direction_easy）：door→toilet 方向错（GT NW，模型 W）
- `scene0353_00`（object_rel_direction_easy）：bookshelf-door 距离画错（GT 2.0，模型 7.1）；bookshelf-refrigerator 距离画错（GT 4.5，模型 7.2）；bookshelf→refrigerator 方向错（GT SE，模型 S）；door→refrigerator 方向错（GT SE，模型 E）
- `41159525`（object_rel_direction_easy）：refrigerator-stove 距离画错（GT 5.0，模型 4.0）；refrigerator→stove 方向错（GT E，模型 S）；refrigerator-table 距离画错（GT 4.0，模型 7.1）；stove-table 距离画错（GT 6.4，模型 3.2）；stove→table 方向错（GT SW，模型 S）
- `d755b3d9d8`（object_rel_direction_easy）：cup→shoes 方向错（GT SW，模型 NW）；cup-whiteboard 距离画错（GT 6.7，模型 3.2）；shoes-whiteboard 距离画错（GT 5.8，模型 7.3）
- `47204578`（object_rel_direction_easy）：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 6.1，模型 1.4）；stool→table 方向错（GT S，模型 NW）；stool-tv 距离画错（GT 2.0，模型 5.1）；stool→tv 方向错（GT W，模型 NW）；table-tv 距离画错（GT 6.1，模型 4.0）
- `scene0458_00`（object_rel_direction_easy）：door-mirror 距离画错（GT 7.0，模型 5.0）；door→mirror 方向错（GT E，模型 NE）；door-window 距离画错（GT 5.4，模型 8.9）；door→window 方向错（GT N，模型 NE）；mirror-window 距离画错（GT 7.1，模型 4.1）；mirror→window 方向错（GT NW，模型 N）
- `scene0426_00`（object_rel_direction_easy）：lamp-table 距离画错（GT 6.7，模型 4.2）；lamp→table 方向错（GT SE，模型 S）；table-tv 距离画错（GT 6.4，模型 4.0）
- `scene0144_00`（object_rel_direction_medium）：door-lamp 距离画错（GT 6.7，模型 5.0）；door→lamp 方向错（GT SE，模型 S）；door-window 距离画错（GT 8.1，模型 5.7）；door→window 方向错（GT SE，模型 E）；lamp-window 距离画错（GT 4.5，模型 7.0）
- `scene0629_01`（object_rel_direction_medium）：bed→chair 方向错（GT S，模型 SE）
- `5ee7c22ba0`（object_rel_direction_medium）：ceiling light-microwave 距离画错（GT 2.2，模型 4.1）；ceiling light→microwave 方向错（GT NE，模型 SE）；ceiling light-refrigerator 距离画错（GT 4.0，模型 5.8）；microwave-refrigerator 距离画错（GT 6.1，模型 2.2）
- `45261121`（object_rel_direction_medium）：stove-table 距离画错（GT 2.8，模型 4.2）；stove→table 方向错（GT SW，模型 W）；stove-tv 距离画错（GT 4.1，模型 7.8）；table→tv 方向错（GT NW，模型 W）
- `45b0dac5e3`（object_rel_direction_medium）：cup-heater 距离画错（GT 7.2，模型 5.4）；heater-toilet 距离画错（GT 7.1，模型 5.0）
- `scene0695_00`（object_rel_direction_medium）：多画 pillow ×1（GT 1，模型 2）；lamp→pillow 方向错（GT E，模型 NE）；lamp-table 距离画错（GT 6.3，模型 1.0）；lamp→table 方向错（GT S，模型 SE）；pillow-table 距离画错（GT 5.4，模型 4.0）；pillow→table 方向错（GT S，模型 SW）
- `47334096`（object_rel_direction_medium）：sofa→stool 方向错（GT N，模型 SW）；sofa-stove 距离画错（GT 3.6，模型 7.8）；stool-stove 距离画错（GT 5.4，模型 4.2）；stool→stove 方向错（GT S，模型 SW）
- `42446103`（object_rel_direction_medium）：多画 stool ×1（GT 1，模型 2）；stove-tv 距离画错（GT 7.1，模型 4.2）
- `42446049`（object_rel_direction_medium）：refrigerator-stove 距离画错（GT 7.1，模型 4.2）；stove-washer 距离画错（GT 6.1，模型 4.2）；stove→washer 方向错（GT S，模型 SW）
- `scene0144_00`（object_rel_direction_medium）：漏画 printer ×1（GT 2，模型 1）；door-lamp 距离画错（GT 6.7，模型 3.6）；lamp-printer 距离画错（GT 5.0，模型 3.6）；lamp→printer 方向错（GT NE，模型 E）
- `f9f95681fd`（object_rel_direction_medium）：door-kettle 距离画错（GT 6.0，模型 3.2）；door-microwave 距离画错（GT 3.2，模型 2.0）；door→microwave 方向错（GT S，模型 W）；kettle-microwave 距离画错（GT 5.8，模型 1.4）；kettle→microwave 方向错（GT SE，模型 NE）
- `47331668`（object_rel_direction_hard）：bed→chair 方向错（GT E，模型 N）；bed→tv 方向错（GT SE，模型 S）；chair-tv 距离画错（GT 4.0，模型 7.3）
- `42897528`（object_rel_direction_hard）：refrigerator→sofa 方向错（GT NW，模型 S）；refrigerator-washer 距离画错（GT 3.2，模型 8.5）；sofa-washer 距离画错（GT 6.4，模型 4.2）；sofa→washer 方向错（GT SE，模型 S）
- `scene0307_02`（object_rel_direction_hard）：多画 chair ×1（GT 1，模型 2）；chair-washing machine 距离画错（GT 2.2，模型 4.2）；chair→washing machine 方向错（GT SE，模型 E）；refrigerator→washing machine 方向错（GT S，模型 SE）
- `scene0164_02`（object_rel_direction_hard）：backpack-microwave 距离画错（GT 6.1，模型 4.1）；backpack→towel 方向错（GT S，模型 SE）；microwave-towel 距离画错（GT 2.0，模型 3.2）；microwave→towel 方向错（GT N，模型 E）
- `47331668`（object_rel_direction_hard）：bed→chair 方向错（GT E，模型 N）；bed→tv 方向错（GT SE，模型 S）；chair-tv 距离画错（GT 4.0，模型 7.3）
- `c50d2d1d42`（object_rel_direction_hard）：door-whiteboard 距离画错（GT 6.4，模型 3.6）
- `47430468`（object_rel_direction_hard）：refrigerator-stool 距离画错（GT 1.4，模型 4.2）；stool-stove 距离画错（GT 2.8，模型 4.1）
- `47334380`（object_rel_direction_hard）：refrigerator-stove 距离画错（GT 5.1，模型 3.2）
- `7b6477cb95`（object_rel_direction_hard）：cup→telephone 方向错（GT W，模型 SW）；cup→trash can 方向错（GT SE，模型 S）；telephone-trash can 距离画错（GT 5.0，模型 3.2）
- `47334096`（object_rel_direction_hard）：sofa→stool 方向错（GT N，模型 NE）；sofa-tv 距离画错（GT 3.2，模型 5.1）；stool-tv 距离画错（GT 5.7，模型 3.6）
- `47331970`（object_rel_direction_hard）：dishwasher-table 距离画错（GT 1.4，模型 3.2）；dishwasher→table 方向错（GT SW，模型 S）；refrigerator-table 距离画错（GT 3.2，模型 5.8）
- `scene0664_02`（object_rel_direction_hard）：door→mirror 方向错（GT NE，模型 E）；door-trash bin 距离画错（GT 6.1，模型 4.2）

### threeview

- `09c1414f1b`（object_abs_distance）：z 整体偏高（平均 +1.9 格）
- `47334103`（object_abs_distance）：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 5.1，模型 0.9）；stool→table 方向错（GT W，模型 SW）；z 整体偏高（平均 +2.2 格）
- `42897538`（object_abs_distance）：refrigerator-stool 距离画错（GT 4.0，模型 2.5）；z 整体偏高（平均 +1.6 格）
- `scene0550_00`（object_abs_distance）：door-window 距离画错（GT 7.1，模型 3.5）；z 整体偏高（平均 +0.5 格）
- `scene0378_01`（object_abs_distance）：clock-door 距离画错（GT 3.2，模型 5.3）；z 整体偏高（平均 +0.5 格）
- `c49a8c6cff`（object_abs_distance）：z 整体偏高（平均 +1.2 格）
- `3db0a1c8f3`（object_abs_distance）：z 整体偏高（平均 +2.0 格）
- `c50d2d1d42`（object_abs_distance）：door-telephone 距离画错（GT 7.0，模型 5.0）；z 整体偏高（平均 +1.5 格）
- `scene0474_04`（object_abs_distance）：table-trash bin 距离画错（GT 3.6，模型 2.0）；z 整体偏高（平均 +1.5 格）
- `47333899`（object_abs_distance）：stove-table 距离画错（GT 6.0，模型 3.4）；z 整体偏高（平均 +1.0 格）
- `scene0221_01`（object_rel_distance）：漏画 lamp ×1（GT 2，模型 1）；漏画 pillow ×4（GT 5，模型 1）；漏画 bed ×1（GT 2，模型 1）；漏画 microwave ×1（GT 1，模型 0）；漏画 chair ×2（GT 3，模型 1）；bed→chair 方向错（GT S，模型 SE）
- `scene0307_02`（object_rel_distance）：漏画 window ×2（GT 3，模型 1）；漏画 door ×4（GT 5，模型 1）；chair-door 距离画错（GT 1.0，模型 3.6）；chair→door 方向错（GT NE，模型 NW）；chair-radiator 距离画错（GT 3.2，模型 5.0）；chair→radiator 方向错（GT E，模型 SE）
- `47429977`（object_rel_distance）：多画 chair ×1（GT 3，模型 4）；漏画 table ×1（GT 2，模型 1）；chair→refrigerator 方向错（GT S，模型 SE）；chair-stove 距离画错（GT 2.2，模型 3.6）；chair→stove 方向错（GT SE，模型 E）；chair→table 方向错（GT SW，模型 E）
- `scene0653_00`（object_rel_distance）：漏画 window ×1（GT 2，模型 1）；漏画 monitor ×6（GT 7，模型 1）；漏画 keyboard ×1（GT 2，模型 1）；漏画 table ×5（GT 6，模型 1）；door-monitor 距离画错（GT 1.4，模型 4.9）；door-table 距离画错（GT 1.4，模型 4.6）
- `38d58a7a31`（object_rel_distance）：漏画 ceiling light ×9（GT 10，模型 1）；漏画 heater ×2（GT 3，模型 1）；漏画 chair ×35（GT 36，模型 1）；ceiling light→chair 方向错（GT SE，模型 NE）；ceiling light-heater 距离画错（GT 1.0，模型 4.2）；ceiling light→heater 方向错（GT W，模型 SW）
- `42899461`（object_rel_distance）：漏画 stove ×1（GT 1，模型 0）；漏画 chair ×3（GT 4，模型 1）；chair-sofa 距离画错（GT 2.0，模型 3.0）；chair-tv 距离画错（GT 3.0，模型 5.0）；chair→tv 方向错（GT SE，模型 S）；fireplace-tv 距离画错（GT 3.2，模型 0.0）
- `42899461`（object_rel_distance）：漏画 stove ×1（GT 1，模型 0）；漏画 table ×2（GT 3，模型 1）；fireplace-sofa 距离画错（GT 3.6，模型 5.5）；fireplace→sofa 方向错（GT NW，模型 W）；fireplace-table 距离画错（GT 2.2，模型 3.5）；fireplace→table 方向错（GT N，模型 W）
- `47430034`（object_rel_distance）：漏画 stool ×1（GT 1，模型 0）；漏画 chair ×2（GT 3，模型 1）；漏画 table ×2（GT 3，模型 1）；bed-chair 距离画错（GT 4.0，模型 2.7）；bed→chair 方向错（GT S，模型 SE）；bed-table 距离画错（GT 1.4，模型 2.5）
- `scene0616_01`（object_rel_distance）：漏画 trash bin ×1（GT 2，模型 1）；漏画 chair ×6（GT 7，模型 1）；漏画 table ×1（GT 2，模型 1）；chair→lamp 方向错（GT N，模型 NE）；chair→table 方向错（GT N，模型 NE）；chair→trash bin 方向错（GT W，模型 N）
- `scene0651_02`（object_rel_distance）：漏画 counter ×1（GT 1，模型 0）；漏画 chair ×3（GT 4，模型 1）；漏画 table ×1（GT 2，模型 1）；chair→sofa 方向错（GT N，模型 NW）；chair-table 距离画错（GT 0.0，模型 2.0）；chair→table 方向错（GT NE，模型 W）
- `31a2c91c43`（object_rel_direction_easy）：ceiling light-toilet 距离画错（GT 6.1，模型 1.4）；door-toilet 距离画错（GT 4.5，模型 3.2）；door→toilet 方向错（GT NW，模型 W）；z 整体偏高（平均 +1.0 格）
- `scene0353_00`（object_rel_direction_easy）：bookshelf-door 距离画错（GT 2.0，模型 6.0）；bookshelf→refrigerator 方向错（GT SE，模型 S）；door→refrigerator 方向错（GT SE，模型 E）；z 整体偏高（平均 +2.0 格）
- `41159525`（object_rel_direction_easy）：refrigerator-stove 距离画错（GT 5.0，模型 2.8）；refrigerator→stove 方向错（GT E，模型 SE）；refrigerator-table 距离画错（GT 4.0，模型 5.2）；stove-table 距离画错（GT 6.4，模型 4.0）；z 整体偏高（平均 +1.2 格）
- `d755b3d9d8`（object_rel_direction_easy）：cup-shoes 距离画错（GT 3.6，模型 2.2）；cup→shoes 方向错（GT SW，模型 W）；cup-whiteboard 距离画错（GT 6.7，模型 3.0）；z 整体偏高（平均 +1.7 格）
- `47204578`（object_rel_direction_easy）：stool-table 距离画错（GT 6.1，模型 3.4）；stool→table 方向错（GT S，模型 SW）；stool-tv 距离画错（GT 2.0，模型 3.8）；stool→tv 方向错（GT W，模型 SW）；table-tv 距离画错（GT 6.1，模型 0.5）；table→tv 方向错（GT N，模型 S）
- `scene0458_00`（object_rel_direction_easy）：door-mirror 距离画错（GT 7.0，模型 3.6）；door→mirror 方向错（GT E，模型 N）；door-window 距离画错（GT 5.4，模型 6.9）；door→window 方向错（GT N，模型 NE）；mirror-window 距离画错（GT 7.1，模型 3.4）；mirror→window 方向错（GT NW，模型 NE）
- `scene0426_00`（object_rel_direction_easy）：lamp-table 距离画错（GT 6.7，模型 0.0）；lamp→table 方向错（GT SE，模型 E）；lamp-tv 距离画错（GT 2.8，模型 0.0）；lamp→tv 方向错（GT SW，模型 E）；table-tv 距离画错（GT 6.4，模型 0.0）；table→tv 方向错（GT NW，模型 E）
- `scene0144_00`（object_rel_direction_medium）：door-lamp 距离画错（GT 6.7，模型 3.5）；door-window 距离画错（GT 8.1，模型 7.0）；lamp→window 方向错（GT NE，模型 SE）；z 整体偏高（平均 +1.5 格）
- `scene0629_01`（object_rel_direction_medium）：chair→mirror 方向错（GT E，模型 NE）；z 整体偏高（平均 +1.3 格）
- `5ee7c22ba0`（object_rel_direction_medium）：ceiling light→microwave 方向错（GT NE，模型 E）；ceiling light→refrigerator 方向错（GT S，模型 SE）；microwave-refrigerator 距离画错（GT 6.1，模型 2.4）；z 整体偏高（平均 +2.2 格）
- `45261121`（object_rel_direction_medium）：stove→table 方向错（GT SW，模型 W）；stove-tv 距离画错（GT 4.1，模型 5.4）；z 整体偏高（平均 +0.8 格）
- `45b0dac5e3`（object_rel_direction_medium）：cup-heater 距离画错（GT 7.2，模型 2.1）；cup-toilet 距离画错（GT 5.1，模型 2.2）；cup→toilet 方向错（GT S，模型 SW）；heater-toilet 距离画错（GT 7.1，模型 3.4）；z 整体偏高（平均 +2.2 格）
- `scene0695_00`（object_rel_direction_medium）：lamp-pillow 距离画错（GT 4.1，模型 2.8）；lamp→pillow 方向错（GT E，模型 NE）；lamp-table 距离画错（GT 6.3，模型 0.0）；lamp→table 方向错（GT S，模型 E）；pillow-table 距离画错（GT 5.4，模型 2.8）；pillow→table 方向错（GT S，模型 SW）
- `47334096`（object_rel_direction_medium）：sofa-stool 距离画错（GT 3.2，模型 2.0）；sofa→stool 方向错（GT N，模型 NW）；stool→stove 方向错（GT S，模型 SW）；z 整体偏高（平均 +0.7 格）
- `42446103`（object_rel_direction_medium）：stool→stove 方向错（GT S，模型 SE）；stool-tv 距离画错（GT 5.1，模型 3.6）；stool→tv 方向错（GT W，模型 NW）
- `42446049`（object_rel_direction_medium）：refrigerator-stove 距离画错（GT 7.1，模型 3.2）；refrigerator→stove 方向错（GT NW，模型 W）；stove-washer 距离画错（GT 6.1，模型 2.5）；stove→washer 方向错（GT S，模型 SW）；z 整体偏高（平均 +0.8 格）
- `scene0144_00`（object_rel_direction_medium）：漏画 printer ×1（GT 2，模型 1）；door-lamp 距离画错（GT 6.7，模型 5.0）；door-printer 距离画错（GT 6.3，模型 4.7）；door→printer 方向错（GT E，模型 SE）；lamp-printer 距离画错（GT 5.0，模型 0.7）；lamp→printer 方向错（GT NE，模型 N）
- `f9f95681fd`（object_rel_direction_medium）：door-microwave 距离画错（GT 3.2，模型 5.7）；door→microwave 方向错（GT S，模型 W）；kettle-microwave 距离画错（GT 5.8，模型 1.1）；kettle→microwave 方向错（GT SE，模型 NE）；z 整体偏高（平均 +1.2 格）
- `47331668`（object_rel_direction_hard）：bed-tv 距离画错（GT 5.0，模型 4.0）；chair-tv 距离画错（GT 4.0，模型 2.7）；z 整体偏高（平均 +0.8 格）
- `42897528`（object_rel_direction_hard）：refrigerator-sofa 距离画错（GT 3.6，模型 5.7）；refrigerator→sofa 方向错（GT NW，模型 W）；refrigerator-washer 距离画错（GT 3.2，模型 6.0）；refrigerator→washer 方向错（GT S，模型 SW）；sofa-washer 距离画错（GT 6.4，模型 5.1）；z 整体偏高（平均 +2.2 格）
- `scene0307_02`（object_rel_direction_hard）：chair-refrigerator 距离画错（GT 4.0，模型 5.0）；chair→refrigerator 方向错（GT N，模型 NE）；chair-washing machine 距离画错（GT 2.2，模型 5.0）；chair→washing machine 方向错（GT SE，模型 NE）；refrigerator-washing machine 距离画错（GT 5.4，模型 1.4）；refrigerator→washing machine 方向错（GT S，模型 SE）
- `scene0164_02`（object_rel_direction_hard）：backpack-microwave 距离画错（GT 6.1，模型 4.2）；microwave-towel 距离画错（GT 2.0，模型 0.6）；microwave→towel 方向错（GT N，模型 NE）；z 整体偏高（平均 +1.5 格）
- `c50d2d1d42`（object_rel_direction_hard）：door-telephone 距离画错（GT 7.0，模型 5.8）；door-whiteboard 距离画错（GT 6.4，模型 3.5）；z 整体偏高（平均 +1.5 格）
- `47430468`（object_rel_direction_hard）：refrigerator-stool 距离画错（GT 1.4，模型 4.5）；stool→stove 方向错（GT SE，模型 E）；z 整体偏高（平均 +1.3 格）
- `47334380`（object_rel_direction_hard）：refrigerator-stove 距离画错（GT 5.1，模型 2.0）；refrigerator→stove 方向错（GT N，模型 NW）；stove-table 距离画错（GT 5.7，模型 4.2）；stove→table 方向错（GT SW，模型 W）；z 整体偏高（平均 +1.3 格）
- `7b6477cb95`（object_rel_direction_hard）：cup→telephone 方向错（GT W，模型 S）；cup-trash can 距离画错（GT 4.5，模型 1.6）；cup→trash can 方向错（GT SE，模型 S）；telephone-trash can 距离画错（GT 5.0，模型 0.8）；z 整体偏高（平均 +2.7 格）
- `47334096`（object_rel_direction_hard）：sofa→stool 方向错（GT N，模型 NE）；sofa-tv 距离画错（GT 3.2，模型 5.0）；stool-tv 距离画错（GT 5.7，模型 2.9）；z 整体偏高（平均 +1.3 格）
- `47331970`（object_rel_direction_hard）：dishwasher-table 距离画错（GT 1.4，模型 4.3）；dishwasher→table 方向错（GT SW，模型 S）；refrigerator-table 距离画错（GT 3.2，模型 5.7）；z 整体偏高（平均 +1.3 格）
- `scene0664_02`（object_rel_direction_hard）：door-mirror 距离画错（GT 3.6，模型 6.5）；door→trash bin 方向错（GT N，模型 NE）；mirror-trash bin 距离画错（GT 4.5，模型 1.1）；mirror→trash bin 方向错（GT NW，模型 W）；z 整体偏高（平均 +1.5 格）

### threeview_3pass

- `09c1414f1b`（object_abs_distance）：cutting board-suitcase 距离画错（GT 2.2，模型 3.6）
- `47334103`（object_abs_distance）：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 5.1，模型 1.0）；stool→table 方向错（GT W，模型 N）；z 整体偏高（平均 +2.0 格）
- `42897538`（object_abs_distance）：多画 stool ×1（GT 1，模型 2）
- `scene0550_00`（object_abs_distance）：door-window 距离画错（GT 7.1，模型 5.7）
- `scene0378_01`（object_abs_distance）：clock-door 距离画错（GT 3.2，模型 5.7）
- `c49a8c6cff`（object_abs_distance）：z 整体偏高（平均 +0.5 格）
- `3db0a1c8f3`（object_abs_distance）：z 整体偏高（平均 +1.5 格）
- `c50d2d1d42`（object_abs_distance）：door-telephone 距离画错（GT 7.0，模型 4.1）；z 整体偏高（平均 +1.5 格）
- `scene0474_04`（object_abs_distance）：z 整体偏高（平均 +0.5 格）
- `47333899`（object_abs_distance）：stove-table 距离画错（GT 6.0，模型 5.0）
- `scene0221_01`（object_rel_distance）：漏画 lamp ×1（GT 2，模型 1）；漏画 pillow ×3（GT 5，模型 2）；漏画 bed ×1（GT 2，模型 1）；漏画 microwave ×1（GT 1，模型 0）；漏画 chair ×2（GT 3，模型 1）；bed→chair 方向错（GT S，模型 SW）
- `scene0307_02`（object_rel_distance）：漏画 window ×2（GT 3，模型 1）；漏画 door ×4（GT 5，模型 1）；chair-door 距离画错（GT 1.0，模型 5.7）；chair→door 方向错（GT NE，模型 NW）；chair-washing machine 距离画错（GT 2.2，模型 4.2）；chair-window 距离画错（GT 2.2，模型 4.1）
- `47429977`（object_rel_distance）：多画 chair ×1（GT 3，模型 4）；漏画 table ×1（GT 2，模型 1）；chair-refrigerator 距离画错（GT 5.1，模型 3.6）；chair-stove 距离画错（GT 2.2，模型 3.6）；chair→stove 方向错（GT SE，模型 E）；chair→table 方向错（GT SW，模型 E）
- `scene0653_00`（object_rel_distance）：漏画 window ×1（GT 2，模型 1）；漏画 monitor ×6（GT 7，模型 1）；漏画 keyboard ×1（GT 2，模型 1）；漏画 table ×5（GT 6，模型 1）；door→keyboard 方向错（GT NE，模型 N）；door-monitor 距离画错（GT 1.4，模型 4.0）
- `38d58a7a31`（object_rel_distance）：漏画 ceiling light ×9（GT 10，模型 1）；漏画 heater ×2（GT 3，模型 1）；漏画 chair ×34（GT 36，模型 2）；ceiling light-chair 距离画错（GT 0.0，模型 6.3）；ceiling light→chair 方向错（GT SE，模型 S）；ceiling light-heater 距离画错（GT 1.0，模型 6.4）
- `42899461`（object_rel_distance）：漏画 stove ×1（GT 1，模型 0）；漏画 chair ×2（GT 4，模型 2）；chair→fireplace 方向错（GT S，模型 SE）；chair→sofa 方向错（GT SW，模型 NW）；fireplace-sofa 距离画错（GT 3.6，模型 5.0）；fireplace-tv 距离画错（GT 3.2，模型 1.0）
- `42899461`（object_rel_distance）：漏画 stove ×1（GT 1，模型 0）；漏画 table ×2（GT 3，模型 1）；fireplace-sofa 距离画错（GT 3.6，模型 5.0）；fireplace→sofa 方向错（GT NW，模型 W）；fireplace→table 方向错（GT N，模型 W）；fireplace-tv 距离画错（GT 3.2，模型 0.0）
- `47430034`（object_rel_distance）：漏画 stool ×1（GT 1，模型 0）；漏画 chair ×2（GT 3，模型 1）；漏画 table ×2（GT 3，模型 1）；bed-table 距离画错（GT 1.4，模型 4.0）；bed→table 方向错（GT SE，模型 S）；chair-table 距离画错（GT 0.0，模型 2.0）
- `scene0616_01`（object_rel_distance）：漏画 trash bin ×1（GT 2，模型 1）；漏画 chair ×5（GT 7，模型 2）；漏画 table ×1（GT 2，模型 1）；chair-lamp 距离画错（GT 1.4，模型 3.6）；chair→table 方向错（GT N，模型 E）；chair-trash bin 距离画错（GT 1.4，模型 2.8）
- `scene0651_02`（object_rel_distance）：漏画 table ×1（GT 2，模型 1）；chair-table 距离画错（GT 0.0，模型 1.4）；chair→table 方向错（GT NE，模型 W）；counter-sofa 距离画错（GT 5.4，模型 6.7）；counter→sofa 方向错（GT N，模型 NW）；counter→table 方向错（GT N，模型 NW）
- `31a2c91c43`（object_rel_direction_easy）：z 整体偏高（平均 +0.7 格）
- `scene0353_00`（object_rel_direction_easy）：bookshelf-door 距离画错（GT 2.0，模型 7.3）；bookshelf-refrigerator 距离画错（GT 4.5，模型 7.8）；bookshelf→refrigerator 方向错（GT SE，模型 S）；door→refrigerator 方向错（GT SE，模型 E）；z 整体偏高（平均 +1.0 格）
- `41159525`（object_rel_direction_easy）：refrigerator-stove 距离画错（GT 5.0，模型 3.2）；refrigerator→stove 方向错（GT E，模型 SE）；stove-table 距离画错（GT 6.4，模型 4.1）
- `d755b3d9d8`（object_rel_direction_easy）：cup→shoes 方向错（GT SW，模型 NW）；cup-whiteboard 距离画错（GT 6.7，模型 3.2）；z 整体偏高（平均 +1.7 格）
- `47204578`（object_rel_direction_easy）：多画 stool ×1（GT 1，模型 2）；stool-table 距离画错（GT 6.1，模型 1.5）；stool→table 方向错（GT S，模型 W）；stool-tv 距离画错（GT 2.0，模型 4.3）；stool→tv 方向错（GT W，模型 NW）；table-tv 距离画错（GT 6.1，模型 4.0）
- `scene0458_00`（object_rel_direction_easy）：door-mirror 距离画错（GT 7.0，模型 5.0）；mirror-window 距离画错（GT 7.1，模型 6.0）
- `scene0426_00`（object_rel_direction_easy）：lamp-table 距离画错（GT 6.7，模型 3.6）；lamp→table 方向错（GT SE，模型 S）；table-tv 距离画错（GT 6.4，模型 3.0）；table→tv 方向错（GT NW，模型 W）；z 整体偏高（平均 +1.0 格）
- `scene0144_00`（object_rel_direction_medium）：door-lamp 距离画错（GT 6.7，模型 4.5）；lamp→window 方向错（GT NE，模型 E）；z 整体偏高（平均 +0.7 格）
- `scene0629_01`（object_rel_direction_medium）：chair→mirror 方向错（GT E，模型 NE）；z 整体偏高（平均 +0.6 格）
- `5ee7c22ba0`（object_rel_direction_medium）：ceiling light-microwave 距离画错（GT 2.2，模型 4.5）；ceiling light→microwave 方向错（GT NE，模型 E）；ceiling light-refrigerator 距离画错（GT 4.0，模型 5.8）；ceiling light→refrigerator 方向错（GT S，模型 SE）；z 整体偏高（平均 +1.7 格）
- `45261121`（object_rel_direction_medium）：stove-table 距离画错（GT 2.8，模型 4.5）
- `45b0dac5e3`（object_rel_direction_medium）：cup-heater 距离画错（GT 7.2，模型 5.1）；cup-toilet 距离画错（GT 5.1，模型 2.8）；heater-toilet 距离画错（GT 7.1，模型 4.2）；z 整体偏高（平均 +1.3 格）
- `scene0695_00`（object_rel_direction_medium）：多画 pillow ×1（GT 1，模型 2）；lamp-pillow 距离画错（GT 4.1，模型 2.2）；lamp→pillow 方向错（GT E，模型 SE）；lamp-table 距离画错（GT 6.3，模型 1.4）；lamp→table 方向错（GT S，模型 SE）；pillow-table 距离画错（GT 5.4，模型 1.0）
- `47334096`（object_rel_direction_medium）：多画 stool ×1（GT 1，模型 2）；sofa→stool 方向错（GT N，模型 NW）；sofa-stove 距离画错（GT 3.6，模型 7.1）；sofa→stove 方向错（GT SW，模型 W）；stool-stove 距离画错（GT 5.4，模型 4.1）；stool→stove 方向错（GT S，模型 SW）
- `42446103`（object_rel_direction_medium）：stool→stove 方向错（GT S，模型 SW）；stove-tv 距离画错（GT 7.1，模型 5.4）；z 整体偏低（平均 -0.7 格）
- `42446049`（object_rel_direction_medium）：refrigerator-stove 距离画错（GT 7.1，模型 3.2）；refrigerator→stove 方向错（GT NW，模型 W）；stove-washer 距离画错（GT 6.1，模型 3.6）；stove→washer 方向错（GT S，模型 SW）
- `scene0144_00`（object_rel_direction_medium）：漏画 printer ×1（GT 2，模型 1）；door→printer 方向错（GT E，模型 SE）；lamp-printer 距离画错（GT 5.0，模型 2.2）；lamp→printer 方向错（GT NE，模型 N）；z 整体偏高（平均 +0.7 格）
- `f9f95681fd`（object_rel_direction_medium）：door-microwave 距离画错（GT 3.2，模型 4.2）；door→microwave 方向错（GT S，模型 W）；kettle-microwave 距离画错（GT 5.8，模型 1.0）；kettle→microwave 方向错（GT SE，模型 NE）；z 整体偏高（平均 +1.0 格）
- `47331668`（object_rel_direction_hard）：bed-chair 距离画错（GT 4.1，模型 2.8）；bed→chair 方向错（GT E，模型 NE）；bed-tv 距离画错（GT 5.0，模型 3.0）；bed→tv 方向错（GT SE，模型 S）；chair-tv 距离画错（GT 4.0，模型 5.4）
- `42897528`（object_rel_direction_hard）：refrigerator-sofa 距离画错（GT 3.6，模型 5.0）；refrigerator→sofa 方向错（GT NW，模型 W）；refrigerator-washer 距离画错（GT 3.2，模型 6.0）；sofa-washer 距离画错（GT 6.4，模型 5.0）
- `scene0307_02`（object_rel_direction_hard）：多画 chair ×1（GT 1，模型 2）；chair→refrigerator 方向错（GT N，模型 NW）；chair-washing machine 距离画错（GT 2.2，模型 5.0）；refrigerator-washing machine 距离画错（GT 5.4，模型 8.5）；refrigerator→washing machine 方向错（GT S，模型 SE）；z 整体偏高（平均 +1.3 格）
- `scene0164_02`（object_rel_direction_hard）：backpack-towel 距离画错（GT 4.1，模型 6.4）；backpack→towel 方向错（GT S，模型 SE）；microwave-towel 距离画错（GT 2.0，模型 3.2）；microwave→towel 方向错（GT N，模型 E）
- `47331668`（object_rel_direction_hard）：bed→chair 方向错（GT E，模型 N）；bed→tv 方向错（GT SE，模型 S）；chair-tv 距离画错（GT 4.0，模型 7.3）
- `c50d2d1d42`（object_rel_direction_hard）：door-telephone 距离画错（GT 7.0，模型 3.6）；door-whiteboard 距离画错（GT 6.4，模型 5.0）；telephone→whiteboard 方向错（GT SE，模型 S）；z 整体偏高（平均 +1.3 格）
- `47430468`（object_rel_direction_hard）：漏画 stove ×1（GT 1，模型 0）；refrigerator-stool 距离画错（GT 1.4，模型 3.5）；z 整体偏高（平均 +0.8 格）
- `47334380`（object_rel_direction_hard）：refrigerator-stove 距离画错（GT 5.1，模型 3.2）；refrigerator→stove 方向错（GT N，模型 NW）；stove-table 距离画错（GT 5.7，模型 3.0）；stove→table 方向错（GT SW，模型 W）
- `7b6477cb95`（object_rel_direction_hard）：cup→telephone 方向错（GT W，模型 SW）；z 整体偏高（平均 +1.7 格）
- `47334096`（object_rel_direction_hard）：sofa-stool 距离画错（GT 3.2，模型 2.0）；sofa→stool 方向错（GT N，模型 SE）；sofa→tv 方向错（GT E，模型 SE）；stool-tv 距离画错（GT 5.7，模型 2.2）；stool→tv 方向错（GT SE，模型 E）；z 整体偏低（平均 -1.0 格）
- `47331970`（object_rel_direction_hard）：dishwasher→refrigerator 方向错（GT NW，模型 N）；dishwasher-table 距离画错（GT 1.4，模型 2.8）；dishwasher→table 方向错（GT SW，模型 SE）；refrigerator-table 距离画错（GT 3.2，模型 6.4）
- `scene0664_02`（object_rel_direction_hard）：door-mirror 距离画错（GT 3.6，模型 5.0）；door→mirror 方向错（GT NE，模型 E）；door-trash bin 距离画错（GT 6.1，模型 3.6）；mirror-trash bin 距离画错（GT 4.5，模型 6.3）；z 整体偏高（平均 +1.0 格）
