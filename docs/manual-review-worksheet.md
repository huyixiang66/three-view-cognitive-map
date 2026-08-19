# 人工核对工作表（baseline / 三视图 vs GT）

> 2026-08-07 · 配合 `map-compare-aligned.md` 和原视频使用

## 核对步骤（每个样本）

1. 打开原视频，找到问题里的物体，记下：数量、谁在谁左边/前面、远近、高低。
2. 看 GT TOP：这些物体在 10×10 网格里的位置和相对关系。
3. 看模型 TOP（已对齐到 GT 坐标系）：数量和相对关系对不对；距离是偏挤还是偏散。
4. 三视图再看 FRONT/SIDE 的 z：该高的物体有没有画高。
5. 归类：数错实例 / 相对方向反 / 整体平移尺度 / 高度错 / 地图对但答错 / 视频里根本看不到。

注意：GT 是整场景 bbox，视频可能没拍到部分物体；视频里看不到的不算模型漏画。

## 优先核对顺序

1. **地图指标正常但答错**（回答阶段嫌疑，最值得看）
2. **镜像样本**（朝向语义是否真的反了）
3. **对齐后 RMSE>1.5 格**（地图确实画歪）
4. 抽查地图干净且答对的样本，验证标签可信度

## 桶 1：地图指标正常但答错（14 个）

| # | arm | 样本 | 场景 | QA | tags | 镜像 | RMSE | GT TOP | 模型 TOP | 视频观察 | 问题归类 | 建议 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 6 | 6 | c49a8c6cff | 1.5 vs 0.7(错) | QA_wrong | 是 | 0.04 | bed:(6.0,5.0); trash can:(2.0,6.0) | bed:(5.0,5.0); trash can:(8.0,8.0) | | | |
| baseline | 7 | 7 | 3db0a1c8f3 | 1.2 vs 0.8(错) | QA_wrong | 否 | 0.00 | blanket:(1.0,1.0); computer mouse:(3.0,3.0) | blanket:(5.0,5.0); computer mouse:(7.0,3.0) | | | |
| baseline | 9 | 9 | scene0474_04 | 1.1 vs 1.9(错) | QA_wrong | 是 | 0.27 | table:(4.0,6.0); trash bin:(6.0,3.0) | table:(5.0,6.0); trash bin:(3.0,8.0) | | | |
| baseline | 21 | 21 | 31a2c91c43 | B vs A(错) | QA_wrong | 是 | 2.26 | ceiling light:(5.0,8.0); door:(2.0,4.0); toilet:(6.0,2.0) | ceiling light:(5.0,1.0); door:(1.0,5.0); toilet:(4.0,7.0) | | | |
| baseline | 29 | 29 | scene0629_01 | C vs B(错) | QA_wrong | 是 | 1.24 | bed:(7.0,4.0); chair:(6.0,7.0); mirror:(3.0,6.0) | bed:(5.0,6.0); chair:(3.0,4.0); mirror:(1.0,5.0) | | | |
| threeview | 1 | 1 | 09c1414f1b | 0.9 vs 1.8(错) | QA_wrong | 是 | 0.24 | cutting board:(1.0,2.0); suitcase:(2.0,4.0) | cutting board:(5.2,4.1); suitcase:(4.5,5.5) | | | |
| threeview | 6 | 6 | c49a8c6cff | 1.5 vs 0.7(错) | QA_wrong | 否 | 0.08 | bed:(6.0,5.0); trash can:(2.0,6.0) | bed:(5.0,4.5); trash can:(2.5,7.5) | | | |
| threeview | 7 | 7 | 3db0a1c8f3 | 1.1 vs 0.8(错) | QA_wrong | 否 | 0.30 | blanket:(1.0,1.0); computer mouse:(3.0,3.0) | blanket:(4.8,5.2); computer mouse:(6.2,3.8) | | | |
| threeview_3pass | 6 | 6 | c49a8c6cff | 1.5 vs 0.7(错) | QA_wrong | 否 | 0.18 | bed:(6.0,5.0); trash can:(2.0,6.0) | bed:(5.0,6.0); trash can:(2.0,8.0) | | | |
| threeview_3pass | 7 | 7 | 3db0a1c8f3 | 1.0 vs 0.8(错) | QA_wrong | 否 | 0.21 | blanket:(1.0,1.0); computer mouse:(3.0,3.0) | blanket:(5.0,5.0); computer mouse:(7.0,4.0) | | | |

视频路径示例：`~\.cache\huggingface\vsibench\scannetpp\c49a8c6cff.mp4`
先看上面前 10 个；镜像标记可能被个别噪声放大，需结合视频确认是否真的左右翻转。

## 桶 2：镜像样本（86 个）

| # | arm | 样本 | 场景 | QA | tags | 镜像 | RMSE | GT TOP | 模型 TOP | 视频观察 | 问题归类 | 建议 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 1 | 1 | 09c1414f1b | 1.3 vs 1.8(错) | B3_pair,B4_scale,QA_wrong | 是 | 0.48 | cutting board:(1.0,2.0); suitcase:(2.0,4.0) | cutting board:(5.0,5.0); suitcase:(3.0,8.0) | | | |
| baseline | 5 | 5 | scene0378_01 | 2.0 vs 1.6(错) | B3_pair,QA_wrong | 是 | 0.46 | clock:(3.0,2.0); door:(6.0,1.0) | clock:(5.0,3.0); door:(1.0,5.0) | | | |
| baseline | 6 | 6 | c49a8c6cff | 1.5 vs 0.7(错) | QA_wrong | 是 | 0.04 | bed:(6.0,5.0); trash can:(2.0,6.0) | bed:(5.0,5.0); trash can:(8.0,8.0) | | | |
| baseline | 9 | 9 | scene0474_04 | 1.1 vs 1.9(错) | QA_wrong | 是 | 0.27 | table:(4.0,6.0); trash bin:(6.0,3.0) | table:(5.0,6.0); trash bin:(3.0,8.0) | | | |
| baseline | 10 | 10 | 47333899 | 1.2 vs 0.9(错) | B3_pair,QA_wrong | 是 | 1.00 | stove:(2.0,7.0); table:(2.0,1.0) | stove:(2.0,5.0); table:(5.0,6.0) | | | |
| baseline | 12 | 12 | scene0307_02 | A vs C(错) | A1_miss,B3_pair,B4_scale,B5_adjacent,QA_wrong | 是 | 2.26 | chair:(4.0,6.0); door:(3.0,5.0),(4.0,7.0),(3.0,5.0),(1.0,7.0),(7.0,3.0); radiator:(1.0,5.0); washing machine:(2.0,7.0);  | chair:(5.0,6.0); door:(1.0,5.0); radiator:(8.0,3.0); washing machine:(3.0,8.0); window:(8.0,1.0) | | | |
| baseline | 15 | 15 | 38d58a7a31 | A vs C(错) | A1_miss,B3_pair,B4_scale,B5_adjacent,QA_wrong | 是 | 2.23 | ceiling light:(4.0,1.0),(1.0,2.0),(4.0,6.0),(1.0,3.0),(4.0,5.0),(4.0,3.0),(6.0,1.0),(7.0,6.0),(6.0,4.0),(6.0,3.0); chair | ceiling light:(5.0,1.0); chair:(4.0,6.0); heater:(1.0,7.0); telephone:(5.0,5.0); trash can:(8.0,8.0) | | | |
| baseline | 16 | 16 | 42899461 | C vs A(错) | A1_miss,B3_pair,QA_wrong | 是 | 1.74 | chair:(7.0,4.0),(7.0,3.0),(2.0,4.0),(1.0,4.0); fireplace:(4.0,8.0); sofa:(7.0,6.0); stove:(1.0,1.0); tv:(1.0,7.0) | chair:(3.0,5.0); fireplace:(5.0,2.0); sofa:(5.0,7.0); tv:(5.0,3.0) | | | |
| baseline | 19 | 19 | scene0616_01 | A vs A(对) | A1_miss,B3_pair,B4_scale,B5_adjacent | 是 | 2.15 | chair:(4.0,2.0),(4.0,2.0),(4.0,3.0),(3.0,5.0),(3.0,4.0),(5.0,6.0),(6.0,5.0); lamp:(5.0,1.0); table:(5.0,1.0),(3.0,3.0);  | chair:(4.0,4.0),(6.0,4.0); lamp:(8.0,2.0); table:(5.0,5.0); trash bin:(2.0,2.0); window:(5.0,9.0) | | | |
| baseline | 21 | 21 | 31a2c91c43 | B vs A(错) | QA_wrong | 是 | 2.26 | ceiling light:(5.0,8.0); door:(2.0,4.0); toilet:(6.0,2.0) | ceiling light:(5.0,1.0); door:(1.0,5.0); toilet:(4.0,7.0) | | | |

视频路径示例：`~\.cache\huggingface\vsibench\scannetpp\09c1414f1b.mp4`
先看上面前 10 个；镜像标记可能被个别噪声放大，需结合视频确认是否真的左右翻转。

## 桶 3：对齐后仍偏（RMSE>1.5）（72 个）

| # | arm | 样本 | 场景 | QA | tags | 镜像 | RMSE | GT TOP | 模型 TOP | 视频观察 | 问题归类 | 建议 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 2 | 2 | 47334103 | 0.3 vs 3.7(错) | A2_extra,B3_pair,B4_scale,QA_wrong | 否 | 1.80 | stool:(2.0,2.0); table:(7.0,1.0) | stool:(4.0,5.0),(6.0,5.0); table:(5.0,5.0) | | | |
| baseline | 11 | 11 | scene0221_01 | A vs B(错) | A1_miss,B3_pair,QA_wrong | 否 | 2.00 | bed:(4.0,3.0),(2.0,3.0); chair:(3.0,6.0),(1.0,6.0),(2.0,7.0); lamp:(3.0,1.0),(3.0,0.0); microwave:(6.0,1.0); pillow:(2.0 | bed:(3.0,5.0); chair:(7.0,4.0); lamp:(2.0,7.0); microwave:(8.0,3.0); pillow:(3.0,6.0) | | | |
| baseline | 12 | 12 | scene0307_02 | A vs C(错) | A1_miss,B3_pair,B4_scale,B5_adjacent,QA_wrong | 是 | 2.26 | chair:(4.0,6.0); door:(3.0,5.0),(4.0,7.0),(3.0,5.0),(1.0,7.0),(7.0,3.0); radiator:(1.0,5.0); washing machine:(2.0,7.0);  | chair:(5.0,6.0); door:(1.0,5.0); radiator:(8.0,3.0); washing machine:(3.0,8.0); window:(8.0,1.0) | | | |
| baseline | 15 | 15 | 38d58a7a31 | A vs C(错) | A1_miss,B3_pair,B4_scale,B5_adjacent,QA_wrong | 是 | 2.23 | ceiling light:(4.0,1.0),(1.0,2.0),(4.0,6.0),(1.0,3.0),(4.0,5.0),(4.0,3.0),(6.0,1.0),(7.0,6.0),(6.0,4.0),(6.0,3.0); chair | ceiling light:(5.0,1.0); chair:(4.0,6.0); heater:(1.0,7.0); telephone:(5.0,5.0); trash can:(8.0,8.0) | | | |
| baseline | 16 | 16 | 42899461 | C vs A(错) | A1_miss,B3_pair,QA_wrong | 是 | 1.74 | chair:(7.0,4.0),(7.0,3.0),(2.0,4.0),(1.0,4.0); fireplace:(4.0,8.0); sofa:(7.0,6.0); stove:(1.0,1.0); tv:(1.0,7.0) | chair:(3.0,5.0); fireplace:(5.0,2.0); sofa:(5.0,7.0); tv:(5.0,3.0) | | | |
| baseline | 19 | 19 | scene0616_01 | A vs A(对) | A1_miss,B3_pair,B4_scale,B5_adjacent | 是 | 2.15 | chair:(4.0,2.0),(4.0,2.0),(4.0,3.0),(3.0,5.0),(3.0,4.0),(5.0,6.0),(6.0,5.0); lamp:(5.0,1.0); table:(5.0,1.0),(3.0,3.0);  | chair:(4.0,4.0),(6.0,4.0); lamp:(8.0,2.0); table:(5.0,5.0); trash bin:(2.0,2.0); window:(5.0,9.0) | | | |
| baseline | 21 | 21 | 31a2c91c43 | B vs A(错) | QA_wrong | 是 | 2.26 | ceiling light:(5.0,8.0); door:(2.0,4.0); toilet:(6.0,2.0) | ceiling light:(5.0,1.0); door:(1.0,5.0); toilet:(4.0,7.0) | | | |
| baseline | 22 | 22 | scene0353_00 | B vs A(错) | B3_pair,B4_scale,QA_wrong | 是 | 1.87 | bookshelf:(7.0,1.0); door:(7.0,3.0); refrigerator:(5.0,5.0) | bookshelf:(8.0,4.0); door:(1.0,5.0); refrigerator:(2.0,8.0) | | | |
| baseline | 23 | 23 | 41159525 | A vs B(错) | B3_pair,B4_scale,QA_wrong | 是 | 2.21 | refrigerator:(6.0,1.0); stove:(1.0,1.0); table:(6.0,5.0) | refrigerator:(1.0,5.0); stove:(5.0,5.0); table:(8.0,6.0) | | | |
| baseline | 24 | 24 | d755b3d9d8 | A vs A(对) | B3_pair,B4_scale | 是 | 1.70 | cup:(5.0,1.0); shoes:(7.0,4.0); whiteboard:(2.0,7.0) | cup:(4.0,4.0); shoes:(3.0,8.0); whiteboard:(5.0,1.0) | | | |

视频路径示例：`~\.cache\huggingface\vsibench\arkitscenes\47334103.mp4`
先看上面前 10 个；镜像标记可能被个别噪声放大，需结合视频确认是否真的左右翻转。

## 桶 4：地图干净且答对（2 个）

| # | arm | 样本 | 场景 | QA | tags | 镜像 | RMSE | GT TOP | 模型 TOP | 视频观察 | 问题归类 | 建议 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| threeview | 29 | 29 | scene0629_01 | B vs B(对) | QA_map_clean | 否 | 0.33 | bed:(7.0,4.0); chair:(6.0,7.0); mirror:(3.0,6.0) | bed:(5.0,4.5); chair:(2.5,6.0); mirror:(1.5,4.0) | | | |
| threeview_3pass | 29 | 29 | scene0629_01 | B vs B(对) | QA_map_clean | 否 | 0.36 | bed:(7.0,4.0); chair:(6.0,7.0); mirror:(3.0,6.0) | bed:(5.1,5.8); chair:(2.8,8.2); mirror:(1.5,4.5) | | | |

视频路径示例：`~\.cache\huggingface\vsibench\scannet\scene0629_01.mp4`
先看上面前 10 个；镜像标记可能被个别噪声放大，需结合视频确认是否真的左右翻转。
