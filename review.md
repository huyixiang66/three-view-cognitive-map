# 人工核对问卷（看视频填空）

> 每道题只有一张卡，四个 arm（baseline / 三视图 / 3-pass / 两阶段）的答案和地图都在参考表里。
> 打开视频（路径在卡片里），只看问题里的物体，回答填空；填完我负责汇总分析。
> 注意：GT 是整场景 bbox，视频没拍到的物体不算模型漏画。

## 问题 `31a2c91c43`（scannetpp · object_rel_direction_easy）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannetpp\31a2c91c43.mp4`
- 问题：If I am standing by the ceiling light and facing the toilet, is the door to the left or the right of the toilet?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____右
- 视频里你看到了几个「ceiling light」：____1
- 视频里你看到了几个「door」：____1
- 视频里你看到了几个「toilet」：____1
2. 站在「ceiling light」面向「toilet」，视频里「door」偏向哪边（左/右/前/后/看不清）：____右
3. 视频里「ceiling light」和「toilet」哪个更高（或差不多 / 看不清）：____灯
- 画面里「ceiling light」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____在天花板上
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____右
- 画面里「toilet」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____左
4. 视频里「ceiling light」和「toilet」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____1-3
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：ceiling light 在天花板上

参考（不用填）：
- GT TOP：ceiling light:(5.0,8.0); door:(2.0,4.0); toilet:(6.0,2.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | B | 错 | QA_wrong | 是 | 2.26 | ceiling light:(5.0,1.0); door:(1.0,5.0); toilet:(4.0,7.0) |
| threeview | A | 对 | B3_pair,B4_scale | 否 | 1.40 | ceiling light:(5.0,5.0); door:(1.0,5.0); toilet:(4.0,4.0) |
| threeview_2stage | A | 对 | B3_pair,B4_scale | 否 | 1.29 | ceiling light:(5.0,5.0); door:(2.0,8.0); toilet:(4.0,3.0) |
| threeview_3pass | B | 错 | QA_wrong | 是 | 2.54 | ceiling light:(5.0,1.0); door:(1.0,5.0); toilet:(5.0,8.0) |


## 问题 `3db0a1c8f3`（scannetpp · object_abs_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannetpp\3db0a1c8f3.mp4`
- 问题：Measuring from the closest point of each object, what is the distance between the blanket and the computer mouse (in meters)?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：__
- 视频里你看到了几个「blanket」：____4
- 视频里你看到了几个「computer mouse」：____1
2. 视频里「blanket」和「computer mouse」隔得近还是远（很近 / 中等 / 很远 / 看不清）：__很远__
3. 视频里「blanket」和「computer mouse」哪个更高（或差不多 / 看不清）：__鼠标
- 画面里「blanket」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____看不清
- 画面里「computer mouse」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____右边
4. 视频里「blanket」和「computer mouse」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____>3m
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____鼠标没注意，我就看见电脑了
6. 备注：

参考（不用填）：
- GT TOP：blanket:(1.0,1.0); computer mouse:(3.0,3.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | 1.2 | 错 | QA_wrong | 否 | 0.00 | blanket:(5.0,5.0); computer mouse:(7.0,3.0) |
| threeview | 1.1 | 错 | QA_wrong | 否 | 0.30 | blanket:(4.8,5.2); computer mouse:(6.2,3.8) |
| threeview_2stage | 1.8 | 错 | B3_pair,B4_scale,QA_wrong | 否 | 0.58 | blanket:(3.0,4.0); computer mouse:(7.0,6.0) |
| threeview_3pass | 1.0 | 错 | QA_wrong | 否 | 0.21 | blanket:(5.0,5.0); computer mouse:(7.0,4.0) |


## 问题 `7b6477cb95`（scannetpp · object_rel_direction_hard）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannetpp\7b6477cb95.mp4`
- 问题：If I am standing by the telephone and facing the cup, is the trash can to my front-left, front-right, back-left, or back-right?
The directions refer to the quad
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____front-left
- 视频里你看到了几个「cup」：____1
- 视频里你看到了几个「telephone」：____1
- 视频里你看到了几个「trash can」：____1
2. 站在「telephone」面向「cup」，视频里「trash can」偏向哪边（左/右/前/后/看不清）：____左前
3. 视频里「telephone」和「cup」哪个更高（或差不多 / 看不清）：____差不多
- 画面里「cup」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____右
- 画面里「telephone」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____更右
- 画面里「trash can」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____左
4. 视频里「telephone」和「cup」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____<1
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____都出现
6. 备注：____

参考（不用填）：
- GT TOP：cup:(5.0,3.0); telephone:(6.0,3.0); trash can:(3.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | D | 错 | B3_pair,QA_wrong | 否 | 0.56 | cup:(3.0,4.0); telephone:(4.0,5.0); trash can:(3.0,8.0) |
| threeview | D | 错 | B3_pair,B4_scale,QA_wrong | 否 | 1.27 | cup:(4.8,4.2); telephone:(3.5,4.5); trash can:(3.2,3.8) |
| threeview_2stage | B | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.11 | cup:(6.2,4.8); telephone:(4.5,5.5); trash can:(3.5,6.5) |
| threeview_3pass | D | 错 | QA_wrong | 否 | 0.35 | cup:(4.0,3.0); telephone:(5.0,4.0); trash can:(3.0,8.0) |


## 问题 `c49a8c6cff`（scannetpp · object_abs_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannetpp\c49a8c6cff.mp4`
- 问题：Measuring from the closest point of each object, what is the distance between the trash can and the bed (in meters)?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：1
- 视频里你看到了几个「bed」：1
- 视频里你看到了几个「trash can」：1
2. 视频里「trash can」和「bed」隔得近还是远（很近 / 中等 / 很远 / 看不清）：较近
3. 视频里「trash can」和「bed」哪个更高（或差不多 / 看不清）：床
- 画面里「bed」偏向左边还是右边（左 / 右 / 中间 / 没看清）：右
- 画面里「trash can」偏向左边还是右边（左 / 右 / 中间 / 没看清）：左
4. 视频里「trash can」和「bed」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：1米左右
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：都出现
6. 备注：____

参考（不用填）：
- GT TOP：bed:(6.0,5.0); trash can:(2.0,6.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | 1.5 | 错 | QA_wrong | 是 | 0.04 | bed:(5.0,5.0); trash can:(8.0,8.0) |
| threeview | 1.5 | 错 | QA_wrong | 否 | 0.08 | bed:(5.0,4.5); trash can:(2.5,7.5) |
| threeview_2stage | 1.2 | 错 | QA_wrong | 否 | 0.33 | bed:(5.0,4.5); trash can:(2.5,6.5) |
| threeview_3pass | 1.5 | 错 | QA_wrong | 否 | 0.18 | bed:(5.0,6.0); trash can:(2.0,8.0) |


## 问题 `scene0474_04`（scannet · object_abs_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0474_04.mp4`
- 问题：Measuring from the closest point of each object, what is the distance between the table and the trash bin (in meters)?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：2
- 视频里你看到了几个「table」：1
- 视频里你看到了几个「trash bin」：____1
2. 视频里「table」和「trash bin」隔得近还是远（很近 / 中等 / 很远 / 看不清）：____中等
3. 视频里「table」和「trash bin」哪个更高（或差不多 / 看不清）：____table
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____左
- 画面里「trash bin」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____右
4. 视频里「table」和「trash bin」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____1-3
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____都出现
6. 备注：____

参考（不用填）：
- GT TOP：table:(4.0,6.0); trash bin:(6.0,3.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | 1.1 | 错 | QA_wrong | 是 | 0.27 | table:(5.0,6.0); trash bin:(3.0,8.0) |
| threeview | 0.4 | 错 | B3_pair,QA_wrong | 是 | 0.57 | table:(5.0,5.0); trash bin:(3.0,5.0) |
| threeview_2stage | 0.3 | 错 | B3_pair,B4_scale,QA_wrong | 否 | 0.72 | table:(5.5,5.5); trash bin:(4.0,5.0) |
| threeview_3pass | 1.3 | 错 | QA_wrong | 否 | 0.00 | table:(5.0,5.0); trash bin:(3.0,8.0) |


## 问题 `scene0629_01`（scannet · object_rel_direction_medium）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0629_01.mp4`
- 问题：If I am standing by the bed and facing the chair, is the mirror to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____back
- 视频里你看到了几个「bed」：____1
- 视频里你看到了几个「chair」：____1
- 视频里你看到了几个「mirror」：____1
2. 站在「bed」面向「chair」，视频里「mirror」偏向哪边（左/右/前/后/看不清）：____后
3. 视频里「bed」和「chair」哪个更高（或差不多 / 看不清）：____差不多
- 画面里「bed」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____中间
- 画面里「chair」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____右
- 画面里「mirror」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____左
4. 视频里「bed」和「chair」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____1
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____都出现
6. 备注：____

参考（不用填）：
- GT TOP：bed:(7.0,4.0); chair:(6.0,7.0); mirror:(3.0,6.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | C | 错 | QA_wrong | 是 | 1.24 | bed:(5.0,6.0); chair:(3.0,4.0); mirror:(1.0,5.0) |
| threeview | B | 对 | QA_map_clean | 否 | 0.33 | bed:(5.0,4.5); chair:(2.5,6.0); mirror:(1.5,4.0) |
| threeview_2stage | B | 对 | C8_height | 否 | 0.30 | bed:(5.0,4.5); chair:(2.5,6.5); mirror:(1.5,4.0) |
| threeview_3pass | B | 对 | QA_map_clean | 否 | 0.36 | bed:(5.1,5.8); chair:(2.8,8.2); mirror:(1.5,4.5) |


## 问题 `38d58a7a31`（scannetpp · object_rel_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannetpp\38d58a7a31.mp4`
- 问题：Measuring from the closest point of each object, which of these objects (telephone, heater, chair, ceiling light) is the closest to the trash can?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「ceiling light」：____
- 视频里你看到了几个「chair」：____
- 视频里你看到了几个「heater」：____
- 视频里你看到了几个「telephone」：____
- 视频里你看到了几个「trash can」：____
2. 视频里「trash can」旁边，哪个物体看起来最近（）：____
3. 视频里「ceiling light」和「chair」哪个更高（或差不多 / 看不清）：____
- 画面里「ceiling light」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「chair」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「heater」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「telephone」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「trash can」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「ceiling light」和「chair」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：ceiling light:(4.0,1.0),(1.0,2.0),(4.0,6.0),(1.0,3.0),(4.0,5.0),(4.0,3.0),(6.0,1.0),(7.0,6.0),(6.0,4.0),(6.0,3.0); chair:(1.0,6.0),(3.0,6.0),(4.0,4.0),(5.0,5.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,QA_ | 是 | 2.23 | ceiling light:(5.0,1.0); chair:(4.0,6.0); heater:(1.0,7.0); telephone:(5.0,5.0); trash can:(8.0,8.0) |
| threeview | C | 对 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 是 | 1.51 | ceiling light:(5.0,5.0); chair:(5.5,4.5); heater:(2.0,8.0); telephone:(4.0,3.5); trash can:(6.5,3.5) |
| threeview_2stage | C | 对 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 是 | 1.58 | ceiling light:(3.5,4.0),(6.5,7.0); chair:(4.0,6.0),(6.0,5.0); heater:(2.5,4.5); telephone:(4.5,5.5); trash can |
| threeview_3pass | C | 对 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 否 | 1.88 | ceiling light:(5.0,1.0); chair:(3.0,7.0),(7.0,7.0); heater:(9.0,6.0); telephone:(4.0,5.0); trash can:(2.0,8.0) |


## 问题 `41159525`（arkitscenes · object_rel_direction_easy）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\41159525.mp4`
- 问题：If I am standing by the stove and facing the table, is the refrigerator to the left or the right of the table?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「refrigerator」：____
- 视频里你看到了几个「stove」：____
- 视频里你看到了几个「table」：____
2. 站在「stove」面向「table」，视频里「refrigerator」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「stove」和「table」哪个更高（或差不多 / 看不清）：____
- 画面里「refrigerator」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stove」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「stove」和「table」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：refrigerator:(6.0,1.0); stove:(1.0,1.0); table:(6.0,5.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 错 | B3_pair,B4_scale,QA_wrong | 是 | 2.21 | refrigerator:(1.0,5.0); stove:(5.0,5.0); table:(8.0,6.0) |
| threeview | A | 错 | B3_pair,QA_wrong | 是 | 2.25 | refrigerator:(1.5,3.8); stove:(4.3,3.8); table:(4.9,7.8) |
| threeview_2stage | A | 错 | B3_pair,B4_scale,QA_wrong | 是 | 2.05 | refrigerator:(2.5,3.5); stove:(4.5,3.5); table:(5.5,6.5) |
| threeview_3pass | A | 错 | B3_pair,C8_height,QA_wrong | 是 | 2.32 | refrigerator:(2.0,4.0); stove:(5.0,3.0); table:(6.0,7.0) |


## 问题 `42446049`（arkitscenes · object_rel_direction_medium）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\42446049.mp4`
- 问题：If I am standing by the washer and facing the refrigerator, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 13
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「refrigerator」：____
- 视频里你看到了几个「stove」：____
- 视频里你看到了几个「washer」：____
2. 站在「washer」面向「refrigerator」，视频里「stove」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「washer」和「refrigerator」哪个更高（或差不多 / 看不清）：____
- 画面里「refrigerator」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stove」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「washer」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「washer」和「refrigerator」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：refrigerator:(1.0,6.0); stove:(6.0,1.0); washer:(7.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | B | 错 | B3_pair,QA_wrong | 是 | 2.92 | refrigerator:(2.0,5.0); stove:(5.0,8.0); washer:(8.0,5.0) |
| threeview | C | 对 | B3_pair,B4_scale,C8_height | 否 | 1.70 | refrigerator:(2.5,4.5); stove:(5.5,3.5); washer:(8.0,4.0) |
| threeview_2stage | B | 错 | A1_miss,B3_pair,B4_scale,C7_missing,QA_w | 是 | 1.38 | refrigerator:(3.5,4.5); stove:(6.5,5.5) |
| threeview_3pass | C | 对 | B3_pair,B4_scale,C8_height | 否 | 1.48 | refrigerator:(2.0,5.0); stove:(5.0,4.0); washer:(8.0,6.0) |


## 问题 `42446103`（arkitscenes · object_rel_direction_medium）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\42446103.mp4`
- 问题：If I am standing by the stove and facing the tv, is the stool to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees i
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「stool」：____
- 视频里你看到了几个「stove」：____
- 视频里你看到了几个「tv」：____
2. 站在「stove」面向「tv」，视频里「stool」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「stove」和「tv」哪个更高（或差不多 / 看不清）：____
- 画面里「stool」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stove」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「tv」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「stove」和「tv」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：stool:(3.0,3.0); stove:(3.0,7.0); tv:(8.0,2.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | C | 错 | A2_extra,B3_pair,QA_wrong | 是 | 2.36 | stool:(3.0,6.0),(4.0,6.0); stove:(5.0,2.0); tv:(8.0,5.0) |
| threeview | A | 对 | B3_pair | 否 | 0.74 | stool:(5.0,5.0); stove:(3.0,8.0); tv:(8.0,3.0) |
| threeview_2stage | C | 错 | A1_miss,B3_pair,C7_missing,QA_wrong | 否 | 0.73 | stove:(4.0,8.0); tv:(7.0,4.0) |
| threeview_3pass | C | 错 | B3_pair,QA_wrong | 是 | 2.13 | stool:(5.0,8.0); stove:(3.0,5.0); tv:(8.0,3.0) |


## 问题 `42897528`（arkitscenes · object_rel_direction_hard）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\42897528.mp4`
- 问题：If I am standing by the washer and facing the refrigerator, is the sofa to my front-left, front-right, back-left, or back-right?
The directions refer to the qua
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「refrigerator」：____
- 视频里你看到了几个「sofa」：____
- 视频里你看到了几个「washer」：____
2. 站在「washer」面向「refrigerator」，视频里「sofa」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「washer」和「refrigerator」哪个更高（或差不多 / 看不清）：____
- 画面里「refrigerator」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「sofa」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「washer」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「washer」和「refrigerator」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：refrigerator:(2.0,4.0); sofa:(5.0,2.0); washer:(1.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | D | 对 | B3_pair,B4_scale | 是 | 2.25 | refrigerator:(2.0,8.0); sofa:(5.0,5.0); washer:(8.0,2.0) |
| threeview | D | 对 | B3_pair,B4_scale | 否 | 1.44 | refrigerator:(2.0,8.0); sofa:(5.5,3.5); washer:(8.0,8.0) |
| threeview_2stage | B | 错 | A1_miss,C7_missing,QA_wrong | 是 | 0.23 | refrigerator:(2.5,7.5); sofa:(5.5,4.5) |
| threeview_3pass | B | 错 | B3_pair,B4_scale,QA_wrong | 是 | 2.05 | refrigerator:(2.0,3.0); sofa:(5.0,7.0); washer:(8.0,3.0) |


## 问题 `42899461`（arkitscenes · object_rel_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\42899461.mp4`
- 问题：Measuring from the closest point of each object, which of these objects (chair, sofa, fireplace, stove) is the closest to the tv?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「chair」：____
- 视频里你看到了几个「fireplace」：____
- 视频里你看到了几个「sofa」：____
- 视频里你看到了几个「stove」：____
- 视频里你看到了几个「tv」：____
2. 视频里「tv」旁边，哪个物体看起来最近（）：____
3. 视频里「chair」和「fireplace」哪个更高（或差不多 / 看不清）：____
- 画面里「chair」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「fireplace」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「sofa」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stove」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「tv」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「chair」和「fireplace」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：chair:(7.0,4.0),(7.0,3.0),(2.0,4.0),(1.0,4.0); fireplace:(4.0,8.0); sofa:(7.0,6.0); stove:(1.0,1.0); tv:(1.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | C | 错 | A1_miss,B3_pair,QA_wrong | 是 | 1.74 | chair:(3.0,5.0); fireplace:(5.0,2.0); sofa:(5.0,7.0); tv:(5.0,3.0) |
| threeview | C | 错 | A1_miss,B3_pair,C7_missing,C8_height,QA_ | 否 | 0.89 | chair:(2.0,4.0); fireplace:(5.0,8.0); sofa:(5.0,4.0); tv:(5.0,8.0) |
| threeview_2stage | A | 对 | A1_miss,B3_pair,C7_missing,C8_height | 否 | 0.95 | chair:(3.0,4.5),(7.0,4.5),(2.5,7.0),(7.5,7.0); sofa:(5.0,3.5); tv:(5.0,8.5) |
| threeview_3pass | C | 错 | A1_miss,B3_pair,C7_missing,C8_height,QA_ | 否 | 1.29 | chair:(3.0,6.0),(7.0,6.0); fireplace:(5.0,2.0); sofa:(5.0,7.0); tv:(5.0,3.0) |


## 问题 `45b0dac5e3`（scannetpp · object_rel_direction_medium）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannetpp\45b0dac5e3.mp4`
- 问题：If I am standing by the cup and facing the heater, is the toilet to my left, right, or back?
An object is to my back if I would have to turn at least 135 degree
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「cup」：____
- 视频里你看到了几个「heater」：____
- 视频里你看到了几个「toilet」：____
2. 站在「cup」面向「heater」，视频里「toilet」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「cup」和「heater」哪个更高（或差不多 / 看不清）：____
- 画面里「cup」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「heater」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「toilet」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「cup」和「heater」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：cup:(6.0,1.0); heater:(0.0,5.0); toilet:(7.0,6.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 错 | B3_pair,QA_wrong | 是 | 3.02 | cup:(3.0,3.0); heater:(8.0,5.0); toilet:(4.0,8.0) |
| threeview | C | 对 | B3_pair,B4_scale | 否 | 1.69 | cup:(3.5,4.5); heater:(1.5,5.0); toilet:(4.5,6.5) |
| threeview_2stage | A | 错 | A1_miss,C7_missing,QA_wrong | 否 | - | toilet:(5.1,8.2) |
| threeview_3pass | A | 错 | B3_pair,QA_wrong | 是 | 2.36 | cup:(3.0,5.0); heater:(8.0,4.0); toilet:(5.0,7.0) |


## 问题 `47204578`（arkitscenes · object_rel_direction_easy）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\47204578.mp4`
- 问题：If I am standing by the tv and facing the table, is the stool to the left or the right of the table?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「stool」：____
- 视频里你看到了几个「table」：____
- 视频里你看到了几个「tv」：____
2. 站在「tv」面向「table」，视频里「stool」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「tv」和「table」哪个更高（或差不多 / 看不清）：____
- 画面里「stool」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「tv」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「tv」和「table」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：stool:(1.0,1.0); table:(2.0,7.0); tv:(3.0,1.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 对 | A2_extra,B3_pair,B4_scale | 否 | 2.02 | stool:(4.0,4.0),(6.0,4.0); table:(5.0,5.0); tv:(5.0,9.0) |
| threeview | B | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.90 | stool:(3.5,5.0); table:(5.0,8.0); tv:(5.0,8.5) |
| threeview_2stage | A | 对 | A1_miss,B3_pair,C7_missing | 否 | 2.15 | table:(5.0,5.5); tv:(5.0,5.5) |
| threeview_3pass | A | 对 | A2_extra,B3_pair,B4_scale | 否 | 1.77 | stool:(3.5,5.0),(6.5,5.0); table:(5.0,5.0); tv:(5.0,1.0) |


## 问题 `47331668`（arkitscenes · object_rel_direction_hard）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\47331668.mp4`
- 问题：If I am standing by the tv and facing the bed, is the chair to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a 
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「bed」：____
- 视频里你看到了几个「chair」：____
- 视频里你看到了几个「tv」：____
2. 站在「tv」面向「bed」，视频里「chair」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「tv」和「bed」哪个更高（或差不多 / 看不清）：____
- 画面里「bed」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「chair」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「tv」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「tv」和「bed」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：bed:(6.0,4.0); chair:(2.0,3.0); tv:(2.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | C | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.96 | bed:(5.0,5.0); chair:(3.0,8.0); tv:(5.0,1.0) |
| threeview | A | 对 | B3_pair | 否 | 0.43 | bed:(5.0,4.5); chair:(2.5,7.5); tv:(5.0,8.5) |
| threeview_2stage | A | 对 | B3_pair,C8_height | 否 | 0.43 | bed:(5.0,4.5); chair:(2.5,7.5); tv:(5.0,8.5) |
| threeview_3pass | C | 错 | B3_pair,C8_height,QA_wrong | 是 | 1.77 | bed:(5.0,5.0); chair:(3.0,7.0); tv:(5.0,2.0) |


## 问题 `47331668`（arkitscenes · object_rel_direction_hard）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\47331668.mp4`
- 问题：If I am standing by the bed and facing the tv, is the chair to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a 
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「bed」：____
- 视频里你看到了几个「chair」：____
- 视频里你看到了几个「tv」：____
2. 站在「bed」面向「tv」，视频里「chair」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「bed」和「tv」哪个更高（或差不多 / 看不清）：____
- 画面里「bed」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「chair」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「tv」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「bed」和「tv」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：bed:(6.0,4.0); chair:(2.0,3.0); tv:(2.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | D | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.96 | bed:(5.0,5.0); chair:(3.0,8.0); tv:(5.0,1.0) |
| threeview | B | 对 | C8_height | 否 | 0.37 | bed:(5.0,4.5); chair:(2.5,6.5); tv:(5.0,8.5) |
| threeview_2stage | C | 错 | B3_pair,C8_height,QA_wrong | 否 | 1.05 | bed:(4.5,4.5); chair:(2.5,7.5); tv:(7.5,4.5) |
| threeview_3pass | D | 错 | B3_pair,B4_scale,C8_height,QA_wrong | 是 | 1.96 | bed:(5.0,5.0); chair:(3.0,8.0); tv:(5.0,1.0) |


## 问题 `47334096`（arkitscenes · object_rel_direction_medium）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\47334096.mp4`
- 问题：If I am standing by the stool and facing the sofa, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「sofa」：____
- 视频里你看到了几个「stool」：____
- 视频里你看到了几个「stove」：____
2. 站在「stool」面向「sofa」，视频里「stove」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「stool」和「sofa」哪个更高（或差不多 / 看不清）：____
- 画面里「sofa」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stool」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stove」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「stool」和「sofa」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：sofa:(4.0,4.0); stool:(5.0,1.0); stove:(7.0,6.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 错 | B3_pair,B4_scale,QA_wrong | 否 | 1.69 | sofa:(3.0,8.0); stool:(5.0,5.0); stove:(8.0,2.0) |
| threeview | B | 错 | B3_pair,QA_wrong | 是 | 1.30 | sofa:(5.2,4.1); stool:(3.5,5.2); stove:(8.1,7.5) |
| threeview_2stage | A | 错 | A1_miss,B3_pair,C7_missing,QA_wrong | 否 | 0.49 | sofa:(3.5,4.5); stove:(7.5,7.5) |
| threeview_3pass | C | 对 | A2_extra,B3_pair,B4_scale,C8_height | 否 | 1.15 | sofa:(3.0,8.0); stool:(2.0,4.0),(4.0,4.0); stove:(8.0,3.0) |


## 问题 `47334096`（arkitscenes · object_rel_direction_hard）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\47334096.mp4`
- 问题：If I am standing by the stool and facing the tv, is the sofa to my front-left, front-right, back-left, or back-right?
The directions refer to the quadrants of a
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「sofa」：____
- 视频里你看到了几个「stool」：____
- 视频里你看到了几个「tv」：____
2. 站在「stool」面向「tv」，视频里「sofa」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「stool」和「tv」哪个更高（或差不多 / 看不清）：____
- 画面里「sofa」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stool」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「tv」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「stool」和「tv」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：sofa:(4.0,4.0); stool:(5.0,1.0); tv:(1.0,5.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.55 | sofa:(4.0,7.0); stool:(3.0,5.0); tv:(5.0,2.0) |
| threeview | B | 错 | B3_pair,B4_scale,QA_wrong | 否 | 1.25 | sofa:(5.0,3.5); stool:(3.5,6.0); tv:(5.0,8.5) |
| threeview_2stage | B | 错 | B3_pair,QA_wrong | 否 | 1.01 | sofa:(5.0,3.0); stool:(3.5,4.5); tv:(5.0,7.5) |
| threeview_3pass | A | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.51 | sofa:(4.0,6.0); stool:(4.0,4.0); tv:(5.0,2.0) |


## 问题 `47334103`（arkitscenes · object_abs_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\47334103.mp4`
- 问题：Measuring from the closest point of each object, what is the distance between the table and the stool (in meters)?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「stool」：____
- 视频里你看到了几个「table」：____
2. 视频里「table」和「stool」隔得近还是远（很近 / 中等 / 很远 / 看不清）：____
3. 视频里「table」和「stool」哪个更高（或差不多 / 看不清）：____
- 画面里「stool」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「table」和「stool」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：stool:(2.0,2.0); table:(7.0,1.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | 0.3 | 错 | A2_extra,B3_pair,B4_scale,QA_wrong | 否 | 1.80 | stool:(4.0,5.0),(6.0,5.0); table:(5.0,5.0) |
| threeview | 0.3 | 错 | A2_extra,B3_pair,B4_scale,QA_wrong | 否 | 1.62 | stool:(4.2,4.8),(5.8,4.8); table:(5.1,5.3) |
| threeview_2stage | 0.3 | 错 | A2_extra,B3_pair,B4_scale,QA_wrong | 否 | 1.80 | stool:(3.5,5.0),(6.5,5.0),(5.0,3.5),(5.0,6.5); table:(5.0,5.0) |
| threeview_3pass | 0.4 | 错 | A2_extra,B3_pair,B4_scale,QA_wrong | 否 | 1.80 | stool:(4.0,5.0),(6.0,5.0); table:(5.0,5.0) |


## 问题 `47429977`（arkitscenes · object_rel_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\47429977.mp4`
- 问题：Measuring from the closest point of each object, which of these objects (stove, chair, refrigerator, table) is the closest to the tv?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「chair」：____
- 视频里你看到了几个「refrigerator」：____
- 视频里你看到了几个「stove」：____
- 视频里你看到了几个「table」：____
- 视频里你看到了几个「tv」：____
2. 视频里「tv」旁边，哪个物体看起来最近（）：____
3. 视频里「chair」和「refrigerator」哪个更高（或差不多 / 看不清）：____
- 画面里「chair」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「refrigerator」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stove」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「tv」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「chair」和「refrigerator」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：chair:(4.0,1.0),(3.0,2.0),(3.0,1.0); refrigerator:(2.0,7.0); stove:(1.0,3.0); table:(6.0,4.0),(3.0,1.0); tv:(6.0,1.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | B | 错 | A1_miss,A2_extra,B3_pair,QA_wrong | 否 | 1.16 | chair:(5.0,6.0),(7.0,6.0),(6.0,5.0),(6.0,7.0); refrigerator:(2.0,2.0); stove:(4.0,2.0); table:(6.0,6.0); tv:(9 |
| threeview | B | 错 | A1_miss,A2_extra,B3_pair,B4_scale,C7_mis | 是 | 1.58 | chair:(5.0,6.0),(7.0,6.0),(6.0,5.0),(6.0,7.0); refrigerator:(2.0,3.0); stove:(4.0,2.0); table:(6.0,6.0); tv:(8 |
| threeview_2stage | B | 错 | A1_miss,A2_extra,B3_pair,B4_scale,C7_mis | 否 | 0.82 | chair:(5.5,6.5),(7.5,6.5),(6.5,5.5),(6.5,7.5); refrigerator:(2.5,2.5); stove:(4.5,2.0); table:(6.5,6.5) |
| threeview_3pass | D | 对 | A1_miss,A2_extra,B3_pair,C7_missing,C8_h | 是 | 2.20 | chair:(4.0,5.0),(6.0,5.0),(5.0,4.0),(5.0,6.0); refrigerator:(2.0,2.0); stove:(2.0,8.0); table:(5.0,5.0); tv:(8 |


## 问题 `47430468`（arkitscenes · object_rel_direction_hard）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\47430468.mp4`
- 问题：If I am standing by the stove and facing the stool, is the refrigerator to my front-left, front-right, back-left, or back-right?
The directions refer to the qua
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「refrigerator」：____
- 视频里你看到了几个「stool」：____
- 视频里你看到了几个「stove」：____
2. 站在「stove」面向「stool」，视频里「refrigerator」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「stove」和「stool」哪个更高（或差不多 / 看不清）：____
- 画面里「refrigerator」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stool」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stove」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「stove」和「stool」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：refrigerator:(2.0,4.0); stool:(3.0,5.0); stove:(1.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | B | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.63 | refrigerator:(1.0,5.0); stool:(4.0,8.0); stove:(5.0,4.0) |
| threeview | C | 错 | B3_pair,B4_scale,QA_wrong | 否 | 0.98 | refrigerator:(2.5,8.5); stool:(4.5,4.5); stove:(5.0,7.5) |
| threeview_2stage | A | 错 | A2_extra,B3_pair,B4_scale,QA_wrong | 是 | 1.81 | refrigerator:(2.5,3.5); stool:(7.5,6.5),(8.5,6.5); stove:(5.5,4.5) |
| threeview_3pass | B | 错 | A1_miss,B3_pair,B4_scale,C7_missing,QA_w | 否 | 0.75 | refrigerator:(4.5,4.5); stool:(5.0,8.0) |


## 问题 `5ee7c22ba0`（scannetpp · object_rel_direction_medium）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannetpp\5ee7c22ba0.mp4`
- 问题：If I am standing by the refrigerator and facing the microwave, is the ceiling light to my left, right, or back?
An object is to my back if I would have to turn 
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「ceiling light」：____
- 视频里你看到了几个「microwave」：____
- 视频里你看到了几个「refrigerator」：____
2. 站在「refrigerator」面向「microwave」，视频里「ceiling light」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「refrigerator」和「microwave」哪个更高（或差不多 / 看不清）：____
- 画面里「ceiling light」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「microwave」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「refrigerator」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「refrigerator」和「microwave」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：ceiling light:(4.0,3.0); microwave:(3.0,1.0); refrigerator:(4.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.87 | ceiling light:(4.0,1.0); microwave:(3.0,5.0); refrigerator:(1.0,6.0) |
| threeview | A | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.61 | ceiling light:(5.0,5.0); microwave:(5.2,8.2); refrigerator:(2.8,7.8) |
| threeview_2stage | B | 对 | B3_pair,B4_scale | 否 | 1.13 | ceiling light:(3.0,5.0); microwave:(4.0,4.0); refrigerator:(2.0,3.0) |
| threeview_3pass | B | 对 | B3_pair,B4_scale | 否 | 1.25 | ceiling light:(5.0,1.0); microwave:(3.0,5.0); refrigerator:(8.0,6.0) |


## 问题 `c50d2d1d42`（scannetpp · object_rel_direction_hard）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannetpp\c50d2d1d42.mp4`
- 问题：If I am standing by the telephone and facing the door, is the whiteboard to my front-left, front-right, back-left, or back-right?
The directions refer to the qu
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「door」：____
- 视频里你看到了几个「telephone」：____
- 视频里你看到了几个「whiteboard」：____
2. 站在「telephone」面向「door」，视频里「whiteboard」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「telephone」和「door」哪个更高（或差不多 / 看不清）：____
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「telephone」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「whiteboard」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「telephone」和「door」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：door:(0.0,3.0); telephone:(7.0,3.0); whiteboard:(5.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | D | 错 | B3_pair,QA_wrong | 是 | 2.26 | door:(1.0,5.0); telephone:(7.0,6.0); whiteboard:(4.0,3.0) |
| threeview | C | 对 | B3_pair | 否 | 0.83 | door:(1.5,9.0); telephone:(4.5,4.0); whiteboard:(5.0,8.5) |
| threeview_2stage | A | 错 | B3_pair,QA_wrong | 是 | 2.16 | door:(1.0,5.0); telephone:(5.0,4.0); whiteboard:(5.0,1.0) |
| threeview_3pass | D | 错 | B3_pair,C8_height,QA_wrong | 是 | 2.87 | door:(1.0,5.0); telephone:(4.0,7.0); whiteboard:(5.0,2.0) |


## 问题 `d755b3d9d8`（scannetpp · object_rel_direction_easy）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannetpp\d755b3d9d8.mp4`
- 问题：If I am standing by the cup and facing the whiteboard, is the shoes to the left or the right of the whiteboard?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「cup」：____
- 视频里你看到了几个「shoes」：____
- 视频里你看到了几个「whiteboard」：____
2. 站在「cup」面向「whiteboard」，视频里「shoes」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「cup」和「whiteboard」哪个更高（或差不多 / 看不清）：____
- 画面里「cup」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「shoes」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「whiteboard」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「cup」和「whiteboard」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：cup:(5.0,1.0); shoes:(7.0,4.0); whiteboard:(2.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 对 | B3_pair,B4_scale | 是 | 1.70 | cup:(4.0,4.0); shoes:(3.0,8.0); whiteboard:(5.0,1.0) |
| threeview | B | 错 | B3_pair,B4_scale,QA_wrong | 否 | 1.29 | cup:(5.0,5.0); shoes:(4.0,7.0); whiteboard:(5.0,2.0) |
| threeview_2stage | A | 对 | B3_pair | 否 | 1.26 | cup:(4.5,5.5); shoes:(3.5,7.5); whiteboard:(5.0,2.0) |
| threeview_3pass | B | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.52 | cup:(4.0,5.0); shoes:(3.0,8.0); whiteboard:(5.0,2.0) |


## 问题 `f9f95681fd`（scannetpp · object_rel_direction_medium）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannetpp\f9f95681fd.mp4`
- 问题：If I am standing by the door and facing the kettle, is the microwave to my left, right, or back?
An object is to my back if I would have to turn at least 135 de
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「door」：____
- 视频里你看到了几个「kettle」：____
- 视频里你看到了几个「microwave」：____
2. 站在「door」面向「kettle」，视频里「microwave」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「door」和「kettle」哪个更高（或差不多 / 看不清）：____
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「kettle」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「microwave」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「door」和「kettle」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：door:(1.0,3.0); kettle:(7.0,3.0); microwave:(2.0,6.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.65 | door:(1.0,5.0); kettle:(4.0,6.0); microwave:(3.0,5.0) |
| threeview | A | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.77 | door:(1.5,8.5); kettle:(6.5,4.0); microwave:(5.5,4.5) |
| threeview_2stage | A | 错 | A1_miss,B3_pair,C7_missing,QA_wrong | 否 | 0.38 | door:(1.0,8.0); microwave:(4.0,5.0) |
| threeview_3pass | A | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.72 | door:(1.0,8.0); kettle:(5.0,5.0); microwave:(4.0,5.0) |


## 问题 `scene0221_01`（scannet · object_rel_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0221_01.mp4`
- 问题：Measuring from the closest point of each object, which of these objects (chair, bed, pillow, lamp) is the closest to the microwave?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「bed」：____
- 视频里你看到了几个「chair」：____
- 视频里你看到了几个「lamp」：____
- 视频里你看到了几个「microwave」：____
- 视频里你看到了几个「pillow」：____
2. 视频里「microwave」旁边，哪个物体看起来最近（）：____
3. 视频里「bed」和「chair」哪个更高（或差不多 / 看不清）：____
- 画面里「bed」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「chair」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「lamp」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「microwave」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「pillow」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「bed」和「chair」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：bed:(4.0,3.0),(2.0,3.0); chair:(3.0,6.0),(1.0,6.0),(2.0,7.0); lamp:(3.0,1.0),(3.0,0.0); microwave:(6.0,1.0); pillow:(2.0,1.0),(4.0,1.0),(4.0,1.0),(4.0,1.0),(2.0

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 错 | A1_miss,B3_pair,QA_wrong | 否 | 2.00 | bed:(3.0,5.0); chair:(7.0,4.0); lamp:(2.0,7.0); microwave:(8.0,3.0); pillow:(3.0,6.0) |
| threeview | A | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 否 | 0.76 | bed:(5.0,5.0); chair:(2.5,7.5); lamp:(2.5,2.5); pillow:(5.0,2.5) |
| threeview_2stage | B | 对 | A1_miss,B3_pair,C7_missing | 否 | 0.78 | bed:(5.0,5.0); chair:(2.5,7.0); lamp:(3.0,3.0); pillow:(4.5,3.5),(5.5,3.5) |
| threeview_3pass | A | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 是 | 0.89 | bed:(5.0,7.0); chair:(8.0,7.0); lamp:(2.0,4.0); pillow:(4.0,5.0),(6.0,5.0) |


## 问题 `scene0307_02`（scannet · object_rel_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0307_02.mp4`
- 问题：Measuring from the closest point of each object, which of these objects (window, chair, door, washing machine) is the closest to the radiator?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「chair」：____
- 视频里你看到了几个「door」：____
- 视频里你看到了几个「radiator」：____
- 视频里你看到了几个「washing machine」：____
- 视频里你看到了几个「window」：____
2. 视频里「radiator」旁边，哪个物体看起来最近（）：____
3. 视频里「chair」和「door」哪个更高（或差不多 / 看不清）：____
- 画面里「chair」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「radiator」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「washing machine」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「window」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「chair」和「door」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：chair:(4.0,6.0); door:(3.0,5.0),(4.0,7.0),(3.0,5.0),(1.0,7.0),(7.0,3.0); radiator:(1.0,5.0); washing machine:(2.0,7.0); window:(4.0,1.0),(2.0,7.0),(4.0,1.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,QA_ | 是 | 2.26 | chair:(5.0,6.0); door:(1.0,5.0); radiator:(8.0,3.0); washing machine:(3.0,8.0); window:(8.0,1.0) |
| threeview | A | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 否 | 1.82 | chair:(4.5,4.5); door:(1.5,2.5); radiator:(7.5,8.5); washing machine:(3.5,6.5); window:(5.0,9.0) |
| threeview_2stage | A | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 否 | 1.47 | door:(2.0,8.0); washing machine:(4.0,4.0); window:(8.0,5.0) |
| threeview_3pass | A | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 否 | 2.16 | chair:(5.0,5.0); door:(1.0,1.0); radiator:(4.0,9.0); washing machine:(8.0,8.0); window:(4.0,9.0) |


## 问题 `scene0307_02`（scannet · object_rel_direction_hard）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0307_02.mp4`
- 问题：If I am standing by the chair and facing the refrigerator, is the washing machine to my front-left, front-right, back-left, or back-right?
The directions refer 
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「chair」：____
- 视频里你看到了几个「refrigerator」：____
- 视频里你看到了几个「washing machine」：____
2. 站在「chair」面向「refrigerator」，视频里「washing machine」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「chair」和「refrigerator」哪个更高（或差不多 / 看不清）：____
- 画面里「chair」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「refrigerator」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「washing machine」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「chair」和「refrigerator」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：chair:(4.0,6.0); refrigerator:(4.0,2.0); washing machine:(2.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 错 | A2_extra,B3_pair,B4_scale,QA_wrong | 否 | 0.70 | chair:(4.0,5.0),(5.0,5.0); refrigerator:(2.0,8.0); washing machine:(8.0,8.0) |
| threeview | C | 错 | B3_pair,B4_scale,QA_wrong | 是 | 2.12 | chair:(5.5,4.5); refrigerator:(2.5,8.5); washing machine:(1.5,7.5) |
| threeview_2stage | C | 错 | A1_miss,C7_missing,QA_wrong | 否 | - | washing machine:(5.0,5.0) |
| threeview_3pass | D | 对 | A2_extra,B3_pair,B4_scale | 否 | 1.17 | chair:(4.0,5.0),(5.0,6.0); refrigerator:(2.0,8.0); washing machine:(8.0,2.0) |


## 问题 `scene0353_00`（scannet · object_rel_direction_easy）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0353_00.mp4`
- 问题：If I am standing by the bookshelf and facing the door, is the refrigerator to the left or the right of the door?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「bookshelf」：____
- 视频里你看到了几个「door」：____
- 视频里你看到了几个「refrigerator」：____
2. 站在「bookshelf」面向「door」，视频里「refrigerator」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「bookshelf」和「door」哪个更高（或差不多 / 看不清）：____
- 画面里「bookshelf」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「refrigerator」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「bookshelf」和「door」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：bookshelf:(7.0,1.0); door:(7.0,3.0); refrigerator:(5.0,5.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | B | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.87 | bookshelf:(8.0,4.0); door:(1.0,5.0); refrigerator:(2.0,8.0) |
| threeview | A | 对 | B3_pair,B4_scale | 是 | 1.71 | bookshelf:(7.5,4.5); door:(1.5,5.0); refrigerator:(3.5,7.5) |
| threeview_2stage | A | 对 | A1_miss,C7_missing | 否 | - | door:(5.0,1.5) |
| threeview_3pass | B | 错 | B3_pair,B4_scale,C8_height,QA_wrong | 是 | 1.92 | bookshelf:(8.0,3.0); door:(1.0,5.0); refrigerator:(2.0,8.0) |


## 问题 `scene0426_00`（scannet · object_rel_direction_easy）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0426_00.mp4`
- 问题：If I am standing by the tv and facing the lamp, is the table to the left or the right of the lamp?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「lamp」：____
- 视频里你看到了几个「table」：____
- 视频里你看到了几个「tv」：____
2. 站在「tv」面向「lamp」，视频里「table」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「tv」和「lamp」哪个更高（或差不多 / 看不清）：____
- 画面里「lamp」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「tv」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「tv」和「lamp」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：lamp:(5.0,1.0); table:(2.0,7.0); tv:(7.0,3.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 对 | B3_pair | 否 | 0.87 | lamp:(2.0,3.0); table:(5.0,6.0); tv:(5.0,2.0) |
| threeview | B | 错 | B3_pair,QA_wrong | 否 | 2.29 | lamp:(5.0,5.0); table:(5.0,5.0); tv:(5.0,5.0) |
| threeview_2stage | B | 错 | B3_pair,B4_scale,QA_wrong | 是 | 2.16 | lamp:(4.5,5.2); table:(5.5,5.5); tv:(5.5,5.8) |
| threeview_3pass | B | 错 | B3_pair,B4_scale,QA_wrong | 是 | 2.05 | lamp:(8.0,3.0); table:(5.0,5.0); tv:(5.0,2.0) |


## 问题 `scene0458_00`（scannet · object_rel_direction_easy）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0458_00.mp4`
- 问题：If I am standing by the window and facing the door, is the mirror to the left or the right of the door?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「door」：____
- 视频里你看到了几个「mirror」：____
- 视频里你看到了几个「window」：____
2. 站在「window」面向「door」，视频里「mirror」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「window」和「door」哪个更高（或差不多 / 看不清）：____
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「mirror」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「window」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「window」和「door」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：door:(8.0,6.0); mirror:(1.0,6.0); window:(6.0,1.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | B | 对 | B3_pair,B4_scale | 否 | 2.13 | door:(1.0,8.0); mirror:(5.0,5.0); window:(9.0,4.0) |
| threeview | A | 错 | B3_pair,B4_scale,C8_height,QA_wrong | 是 | 2.28 | door:(2.0,1.5); mirror:(5.0,3.5); window:(8.0,5.0) |
| threeview_2stage | B | 对 | B3_pair,B4_scale,C8_height | 是 | 2.36 | door:(2.5,1.5); mirror:(5.0,5.0); window:(7.5,8.5) |
| threeview_3pass | B | 对 | B3_pair,C8_height | 否 | 0.59 | door:(1.0,5.0); mirror:(5.0,2.0); window:(5.0,8.0) |


## 问题 `scene0616_01`（scannet · object_rel_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0616_01.mp4`
- 问题：Measuring from the closest point of each object, which of these objects (table, trash bin, chair, lamp) is the closest to the window?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「chair」：____
- 视频里你看到了几个「lamp」：____
- 视频里你看到了几个「table」：____
- 视频里你看到了几个「trash bin」：____
- 视频里你看到了几个「window」：____
2. 视频里「window」旁边，哪个物体看起来最近（）：____
3. 视频里「chair」和「lamp」哪个更高（或差不多 / 看不清）：____
- 画面里「chair」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「lamp」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「trash bin」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「window」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「chair」和「lamp」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：chair:(4.0,2.0),(4.0,2.0),(4.0,3.0),(3.0,5.0),(3.0,4.0),(5.0,6.0),(6.0,5.0); lamp:(5.0,1.0); table:(5.0,1.0),(3.0,3.0); trash bin:(7.0,4.0),(7.0,4.0); window:(1

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | A | 对 | A1_miss,B3_pair,B4_scale,B5_adjacent | 是 | 2.15 | chair:(4.0,4.0),(6.0,4.0); lamp:(8.0,2.0); table:(5.0,5.0); trash bin:(2.0,2.0); window:(5.0,9.0) |
| threeview | D | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 否 | 1.21 | chair:(5.0,3.5); lamp:(4.0,5.5); table:(5.0,5.0); trash bin:(3.0,4.5); window:(5.0,9.0) |
| threeview_2stage | A | 对 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 是 | 1.33 | chair:(4.0,5.0),(6.0,5.0); lamp:(3.0,3.0); table:(5.0,5.0); trash bin:(3.0,5.0); window:(5.0,9.0) |
| threeview_3pass | A | 对 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 是 | 2.55 | chair:(4.0,5.0),(6.0,5.0); lamp:(2.0,8.0); table:(5.0,5.0); trash bin:(8.0,3.0); window:(5.0,1.0) |


## 问题 `scene0664_02`（scannet · object_rel_direction_hard）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0664_02.mp4`
- 问题：If I am standing by the mirror and facing the door, is the trash bin to my front-left, front-right, back-left, or back-right?
The directions refer to the quadra
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「door」：____
- 视频里你看到了几个「mirror」：____
- 视频里你看到了几个「trash bin」：____
2. 站在「mirror」面向「door」，视频里「trash bin」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「mirror」和「door」哪个更高（或差不多 / 看不清）：____
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「mirror」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「trash bin」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「mirror」和「door」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：door:(4.0,7.0); mirror:(1.0,5.0); trash bin:(3.0,1.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | D | 对 | B3_pair | 否 | 0.76 | door:(1.0,5.0); mirror:(5.0,3.0); trash bin:(4.0,8.0) |
| threeview | C | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.68 | door:(1.5,8.0); mirror:(5.0,2.5); trash bin:(4.0,3.0) |
| threeview_2stage | C | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.53 | door:(2.0,5.0); mirror:(5.0,3.5); trash bin:(4.5,3.0) |
| threeview_3pass | D | 对 | B3_pair | 否 | 1.17 | door:(1.0,5.0); mirror:(5.0,2.0); trash bin:(3.0,8.0) |


## 问题 `scene0695_00`（scannet · object_rel_direction_medium）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0695_00.mp4`
- 问题：If I am standing by the lamp and facing the pillow, is the table to my left, right, or back?
An object is to my back if I would have to turn at least 135 degree
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「lamp」：____
- 视频里你看到了几个「pillow」：____
- 视频里你看到了几个「table」：____
2. 站在「lamp」面向「pillow」，视频里「table」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「lamp」和「pillow」哪个更高（或差不多 / 看不清）：____
- 画面里「lamp」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「pillow」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「lamp」和「pillow」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：lamp:(5.0,1.0); pillow:(1.0,2.0); table:(3.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | C | 对 | A2_extra,B3_pair,B4_scale | 否 | 1.59 | lamp:(8.0,3.0); pillow:(3.0,4.0),(4.0,4.0); table:(8.0,4.0) |
| threeview | C | 对 | B3_pair | 否 | 1.84 | lamp:(5.0,4.0); pillow:(3.0,6.0); table:(5.0,4.0) |
| threeview_2stage | B | 错 | A2_extra,B3_pair,B4_scale,QA_wrong | 否 | 2.02 | lamp:(2.5,3.5),(7.5,3.5); pillow:(4.0,4.5),(6.0,4.5); table:(2.5,3.5),(7.5,3.5) |
| threeview_3pass | C | 对 | A2_extra,B3_pair,B4_scale | 否 | 1.82 | lamp:(2.0,3.0); pillow:(3.0,5.0),(4.0,5.0); table:(3.0,4.0) |


## 问题 `09c1414f1b`（scannetpp · object_abs_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannetpp\09c1414f1b.mp4`
- 问题：Measuring from the closest point of each object, what is the distance between the cutting board and the suitcase (in meters)?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____2
- 视频里你看到了几个「cutting board」：____1
- 视频里你看到了几个「suitcase」：____1
2. 视频里「cutting board」和「suitcase」隔得近还是远（很近 / 中等 / 很远 / 看不清）：____较近，中间隔了墙
3. 视频里「cutting board」和「suitcase」哪个更高（或差不多 / 看不清）：____砧板
- 画面里「cutting board」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____说不清楚
- 画面里「suitcase」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____说不清楚
4. 视频里「cutting board」和「suitcase」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____2
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____都出现
6. 备注：____

参考（不用填）：
- GT TOP：cutting board:(1.0,2.0); suitcase:(2.0,4.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | 1.3 | 错 | B3_pair,B4_scale,QA_wrong | 是 | 0.48 | cutting board:(5.0,5.0); suitcase:(3.0,8.0) |
| threeview | 0.9 | 错 | QA_wrong | 是 | 0.24 | cutting board:(5.2,4.1); suitcase:(4.5,5.5) |
| threeview_2stage | 1.8 | 对 | A1_miss,C7_missing | 否 | - | suitcase:(5.5,6.5) |
| threeview_3pass | 1.65 | 错 | B3_pair,B4_scale,QA_wrong | 是 | 0.48 | cutting board:(5.0,5.0); suitcase:(3.0,8.0) |


## 问题 `42897538`（arkitscenes · object_abs_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\42897538.mp4`
- 问题：Measuring from the closest point of each object, what is the distance between the stool and the refrigerator (in meters)?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「refrigerator」：____
- 视频里你看到了几个「stool」：____
2. 视频里「stool」和「refrigerator」隔得近还是远（很近 / 中等 / 很远 / 看不清）：____
3. 视频里「stool」和「refrigerator」哪个更高（或差不多 / 看不清）：____
- 画面里「refrigerator」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stool」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「stool」和「refrigerator」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：refrigerator:(3.0,7.0); stool:(3.0,3.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | 1.5 | 错 | A2_extra,QA_wrong | 否 | 0.03 | refrigerator:(2.0,8.0); stool:(4.0,5.0),(5.0,5.0) |
| threeview | 1.2 | 错 | B3_pair,QA_wrong | 否 | 0.54 | refrigerator:(3.2,8.1); stool:(4.8,6.2) |
| threeview_2stage | 1.8 | 错 | A2_extra,QA_wrong | 是 | 0.22 | refrigerator:(2.5,2.0); stool:(4.5,5.0),(5.5,5.0),(6.5,5.0),(7.5,5.0) |
| threeview_3pass | 1.7 | 错 | A2_extra,QA_wrong | 是 | 0.59 | refrigerator:(2.0,4.0); stool:(5.0,8.0),(7.0,8.0) |


## 问题 `45261121`（arkitscenes · object_rel_direction_medium）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\45261121.mp4`
- 问题：If I am standing by the table and facing the tv, is the stove to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees i
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「stove」：____
- 视频里你看到了几个「table」：____
- 视频里你看到了几个「tv」：____
2. 站在「table」面向「tv」，视频里「stove」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「table」和「tv」哪个更高（或差不多 / 看不清）：____
- 画面里「stove」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「tv」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「table」和「tv」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：stove:(3.0,2.0); table:(5.0,4.0); tv:(7.0,1.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | C | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.45 | stove:(2.0,8.0); table:(5.0,5.0); tv:(8.0,3.0) |
| threeview | B | 错 | B3_pair,QA_wrong | 是 | 1.35 | stove:(2.5,3.5); table:(5.2,5.5); tv:(5.2,8.2) |
| threeview_2stage | C | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.42 | stove:(2.0,3.0); table:(5.0,5.0); tv:(8.0,8.0) |
| threeview_3pass | B | 错 | B3_pair,B4_scale,C8_height,QA_wrong | 否 | 0.51 | stove:(3.0,2.0); table:(5.0,6.0); tv:(8.0,3.0) |


## 问题 `47331970`（arkitscenes · object_rel_direction_hard）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\47331970.mp4`
- 问题：If I am standing by the dishwasher and facing the refrigerator, is the table to my front-left, front-right, back-left, or back-right?
The directions refer to th
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「dishwasher」：____
- 视频里你看到了几个「refrigerator」：____
- 视频里你看到了几个「table」：____
2. 站在「dishwasher」面向「refrigerator」，视频里「table」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「dishwasher」和「refrigerator」哪个更高（或差不多 / 看不清）：____
- 画面里「dishwasher」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「refrigerator」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「dishwasher」和「refrigerator」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：dishwasher:(1.0,3.0); refrigerator:(3.0,1.0); table:(2.0,4.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | C | 错 | B3_pair,B4_scale,QA_wrong | 否 | 0.87 | dishwasher:(4.0,5.0); refrigerator:(2.0,3.0); table:(7.0,6.0) |
| threeview | B | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.33 | dishwasher:(3.5,2.5); refrigerator:(1.5,2.5); table:(6.0,6.0) |
| threeview_2stage | B | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.01 | dishwasher:(4.5,4.0); refrigerator:(2.5,3.5); table:(6.5,6.5) |
| threeview_3pass | B | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.09 | dishwasher:(4.0,5.0); refrigerator:(2.0,8.0); table:(6.0,3.0) |


## 问题 `47333899`（arkitscenes · object_abs_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\47333899.mp4`
- 问题：Measuring from the closest point of each object, what is the distance between the table and the stove (in meters)?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「stove」：____
- 视频里你看到了几个「table」：____
2. 视频里「table」和「stove」隔得近还是远（很近 / 中等 / 很远 / 看不清）：____
3. 视频里「table」和「stove」哪个更高（或差不多 / 看不清）：____
- 画面里「stove」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「table」和「stove」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：stove:(2.0,7.0); table:(2.0,1.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | 1.2 | 错 | B3_pair,QA_wrong | 是 | 1.00 | stove:(2.0,5.0); table:(5.0,6.0) |
| threeview | 1.5 | 错 | B3_pair,QA_wrong | 否 | 0.93 | stove:(3.5,8.2); table:(5.5,5.5) |
| threeview_2stage | 1.2 | 错 | B3_pair,QA_wrong | 是 | 0.85 | stove:(3.0,4.0); table:(6.0,6.0) |
| threeview_3pass | 2.5 | 错 | C8_height,QA_wrong | 是 | 0.35 | stove:(2.0,3.0); table:(6.0,6.0) |


## 问题 `scene0144_00`（scannet · object_rel_direction_medium）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0144_00.mp4`
- 问题：If I am standing by the window and facing the lamp, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 135 degrees
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「door」：____
- 视频里你看到了几个「lamp」：____
- 视频里你看到了几个「window」：____
2. 站在「window」面向「lamp」，视频里「door」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「window」和「lamp」哪个更高（或差不多 / 看不清）：____
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「lamp」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「window」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「window」和「lamp」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：door:(8.0,1.0); lamp:(5.0,7.0); window:(1.0,5.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | C | 对 | B3_pair,B4_scale | 否 | 1.27 | door:(1.0,5.0); lamp:(5.0,2.0); window:(5.0,9.0) |
| threeview | None | 错 | B3_pair,C8_height,QA_wrong | 是 | 1.38 | door:(1.5,5.0); lamp:(5.0,5.0); window:(8.5,5.0) |
| threeview_2stage | C | 对 | B3_pair,C8_height | 否 | 1.10 | door:(1.5,5.0); lamp:(5.0,5.0); window:(5.0,8.5) |
| threeview_3pass | C | 对 | B3_pair,C8_height | 否 | 0.76 | door:(1.0,5.0); lamp:(5.0,3.0); window:(9.0,5.0) |


## 问题 `scene0144_00`（scannet · object_rel_direction_medium）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0144_00.mp4`
- 问题：If I am standing by the lamp and facing the printer, is the door to my left, right, or back?
An object is to my back if I would have to turn at least 135 degree
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「door」：____
- 视频里你看到了几个「lamp」：____
- 视频里你看到了几个「printer」：____
2. 站在「lamp」面向「printer」，视频里「door」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「lamp」和「printer」哪个更高（或差不多 / 看不清）：____
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「lamp」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「printer」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「lamp」和「printer」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：door:(8.0,1.0); lamp:(5.0,7.0); printer:(2.0,3.0),(2.0,3.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | C | 对 | A1_miss,B3_pair | 否 | 1.05 | door:(1.0,5.0); lamp:(4.0,3.0); printer:(7.0,5.0) |
| threeview | C | 对 | A1_miss,B3_pair,B4_scale,C7_missing,C8_h | 否 | 1.33 | door:(1.2,8.5); lamp:(3.8,4.2); printer:(4.1,4.8) |
| threeview_2stage | A | 错 | A1_miss,B3_pair,B4_scale,C7_missing,C8_h | 是 | 1.47 | door:(1.5,9.0); lamp:(5.0,4.0); printer:(4.5,4.5) |
| threeview_3pass | C | 对 | A1_miss,B3_pair,B4_scale,C7_missing,C8_h | 否 | 0.94 | door:(1.0,5.0); lamp:(8.0,3.0); printer:(7.0,5.0) |


## 问题 `scene0164_02`（scannet · object_rel_direction_hard）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0164_02.mp4`
- 问题：If I am standing by the towel and facing the microwave, is the backpack to my front-left, front-right, back-left, or back-right?
The directions refer to the qua
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「backpack」：____
- 视频里你看到了几个「microwave」：____
- 视频里你看到了几个「towel」：____
2. 站在「towel」面向「microwave」，视频里「backpack」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「towel」和「microwave」哪个更高（或差不多 / 看不清）：____
- 画面里「backpack」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「microwave」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「towel」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「towel」和「microwave」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：backpack:(6.0,1.0); microwave:(5.0,7.0); towel:(5.0,5.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | C | 错 | B3_pair,B4_scale,QA_wrong | 否 | 1.11 | backpack:(2.0,8.0); microwave:(3.0,4.0); towel:(6.0,5.0) |
| threeview | B | 错 | B3_pair,B4_scale,C8_height,QA_wrong | 否 | 0.62 | backpack:(6.5,4.5); microwave:(3.5,7.5); towel:(3.2,7.0) |
| threeview_2stage | A | 错 | B3_pair,B4_scale,QA_wrong | 是 | 1.10 | backpack:(3.0,6.0); microwave:(5.0,4.0); towel:(4.0,3.0) |
| threeview_3pass | C | 错 | B3_pair,B4_scale,QA_wrong | 否 | 1.13 | backpack:(8.0,7.0); microwave:(3.0,5.0); towel:(4.0,2.0) |


## 问题 `scene0378_01`（scannet · object_abs_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0378_01.mp4`
- 问题：Measuring from the closest point of each object, what is the distance between the door and the clock (in meters)?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「clock」：____
- 视频里你看到了几个「door」：____
2. 视频里「door」和「clock」隔得近还是远（很近 / 中等 / 很远 / 看不清）：____
3. 视频里「door」和「clock」哪个更高（或差不多 / 看不清）：____
- 画面里「clock」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「door」和「clock」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：clock:(3.0,2.0); door:(6.0,1.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | 2.0 | 错 | B3_pair,QA_wrong | 是 | 0.46 | clock:(5.0,3.0); door:(1.0,5.0) |
| threeview | 3.5 | 错 | B3_pair,B4_scale,QA_wrong | 是 | 0.76 | clock:(5.0,1.0); door:(1.5,5.0) |
| threeview_2stage | 1.3 | 错 | B3_pair,QA_wrong | 是 | 0.41 | clock:(5.0,8.0); door:(3.0,8.0) |
| threeview_3pass | 3 | 错 | B3_pair,B4_scale,QA_wrong | 否 | 0.88 | clock:(5.0,1.0); door:(1.0,5.0) |


## 问题 `scene0550_00`（scannet · object_abs_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0550_00.mp4`
- 问题：Measuring from the closest point of each object, what is the distance between the door and the window (in meters)?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「door」：____
- 视频里你看到了几个「window」：____
2. 视频里「door」和「window」隔得近还是远（很近 / 中等 / 很远 / 看不清）：____
3. 视频里「door」和「window」哪个更高（或差不多 / 看不清）：____
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「window」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「door」和「window」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：door:(4.0,8.0); window:(5.0,1.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | 3.5 | 错 | B3_pair,QA_wrong | 否 | 0.50 | door:(1.0,5.0); window:(5.0,1.0) |
| threeview | 3.1 | 错 | B3_pair,B4_scale,QA_wrong | 否 | 1.25 | door:(1.5,9.1); window:(5.0,9.5) |
| threeview_2stage | 2.8 | 错 | B3_pair,QA_wrong | 是 | 0.75 | door:(1.5,5.0); window:(5.0,8.5) |
| threeview_3pass | 2.5 | 对 | B3_pair | 否 | 0.50 | door:(1.0,5.0); window:(5.0,9.0) |


## 问题 `scene0651_02`（scannet · object_rel_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0651_02.mp4`
- 问题：Measuring from the closest point of each object, which of these objects (counter, chair, table, trash bin) is the closest to the sofa?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「chair」：____
- 视频里你看到了几个「counter」：____
- 视频里你看到了几个「sofa」：____
- 视频里你看到了几个「table」：____
- 视频里你看到了几个「trash bin」：____
2. 视频里「sofa」旁边，哪个物体看起来最近（）：____
3. 视频里「chair」和「counter」哪个更高（或差不多 / 看不清）：____
- 画面里「chair」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「counter」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「sofa」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「trash bin」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「chair」和「counter」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：chair:(7.0,4.0),(5.0,3.0),(5.0,4.0),(6.0,3.0); counter:(3.0,6.0); sofa:(5.0,1.0); table:(3.0,2.0),(5.0,3.0); trash bin:(1.0,6.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | C | 对 | A1_miss,B3_pair,B5_adjacent | 否 | 0.86 | chair:(3.0,5.0),(7.0,5.0); counter:(1.0,8.0); sofa:(5.0,2.0); table:(5.0,5.0); trash bin:(1.0,9.0) |
| threeview | C | 对 | A1_miss,B3_pair,B5_adjacent,C7_missing,C | 是 | 1.10 | chair:(3.0,5.0); sofa:(5.0,3.0); table:(5.0,5.0); trash bin:(2.0,8.0) |
| threeview_2stage | B | 错 | A1_miss,B3_pair,C7_missing,C8_height,QA_ | 否 | 0.91 | chair:(4.5,5.5),(6.5,5.5),(5.5,4.5),(5.5,6.5); counter:(2.0,7.5); sofa:(3.5,4.5); table:(5.5,5.5); trash bin:( |
| threeview_3pass | B | 错 | A1_miss,B3_pair,B5_adjacent,C7_missing,C | 否 | 0.61 | chair:(4.0,4.0),(6.0,4.0),(4.0,6.0),(6.0,6.0); counter:(2.0,8.0); sofa:(5.0,2.0); table:(5.0,5.0); trash bin:( |


## 问题 `scene0653_00`（scannet · object_rel_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannet\scene0653_00.mp4`
- 问题：Measuring from the closest point of each object, which of these objects (window, monitor, table, keyboard) is the closest to the door?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「door」：____
- 视频里你看到了几个「keyboard」：____
- 视频里你看到了几个「monitor」：____
- 视频里你看到了几个「table」：____
- 视频里你看到了几个「window」：____
2. 视频里「door」旁边，哪个物体看起来最近（）：____
3. 视频里「door」和「keyboard」哪个更高（或差不多 / 看不清）：____
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「keyboard」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「monitor」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「window」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「door」和「keyboard」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：door:(7.0,7.0); keyboard:(2.0,3.0),(6.0,2.0); monitor:(1.0,6.0),(2.0,3.0),(2.0,3.0),(6.0,1.0),(7.0,1.0),(6.0,4.0),(6.0,6.0); table:(1.0,6.0),(2.0,3.0),(6.0,4.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | B | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,QA_ | 否 | 0.99 | door:(1.0,5.0); keyboard:(5.0,6.0); monitor:(5.0,4.0); table:(5.0,7.0); window:(9.0,3.0) |
| threeview | D | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 是 | 1.14 | door:(1.5,8.0); keyboard:(5.0,5.5); monitor:(5.0,4.5); table:(5.0,5.0); window:(8.5,5.0) |
| threeview_2stage | B | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 是 | 1.15 | door:(8.0,2.0); keyboard:(5.0,5.5); monitor:(5.0,4.8); table:(5.0,5.0); window:(2.0,5.0) |
| threeview_3pass | B | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 是 | 1.57 | door:(9.0,4.0); keyboard:(5.0,6.0); monitor:(5.0,4.0); table:(5.0,7.0); window:(1.0,3.0) |


## 问题 `42899461`（arkitscenes · object_rel_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\42899461.mp4`
- 问题：Measuring from the closest point of each object, which of these objects (table, tv, sofa, stove) is the closest to the fireplace?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「fireplace」：____
- 视频里你看到了几个「sofa」：____
- 视频里你看到了几个「stove」：____
- 视频里你看到了几个「table」：____
- 视频里你看到了几个「tv」：____
2. 视频里「fireplace」旁边，哪个物体看起来最近（）：____
3. 视频里「fireplace」和「sofa」哪个更高（或差不多 / 看不清）：____
- 画面里「fireplace」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「sofa」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stove」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「tv」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「fireplace」和「sofa」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：fireplace:(4.0,8.0); sofa:(7.0,6.0); stove:(1.0,1.0); table:(6.0,7.0),(1.0,7.0),(6.0,3.0); tv:(1.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | B | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,QA_ | 否 | 0.30 | sofa:(5.0,2.0); table:(5.0,5.0); tv:(5.0,8.0) |
| threeview | B | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 否 | 0.99 | fireplace:(5.0,9.0); sofa:(5.0,3.5); table:(5.0,5.5); tv:(5.0,8.5) |
| threeview_2stage | B | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 否 | 0.30 | sofa:(5.0,2.5); table:(5.0,5.5); tv:(5.0,8.5) |
| threeview_3pass | B | 错 | A1_miss,B3_pair,B5_adjacent,C7_missing,C | 否 | 0.88 | fireplace:(5.0,8.0); sofa:(5.0,3.0); table:(5.0,5.0); tv:(5.0,8.0) |


## 问题 `47334380`（arkitscenes · object_rel_direction_hard）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\47334380.mp4`
- 问题：If I am standing by the refrigerator and facing the stove, is the table to my front-left, front-right, back-left, or back-right?
The directions refer to the qua
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「refrigerator」：____
- 视频里你看到了几个「stove」：____
- 视频里你看到了几个「table」：____
2. 站在「refrigerator」面向「stove」，视频里「table」偏向哪边（左/右/前/后/看不清）：____
3. 视频里「refrigerator」和「stove」哪个更高（或差不多 / 看不清）：____
- 画面里「refrigerator」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stove」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「refrigerator」和「stove」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：refrigerator:(1.0,6.0); stove:(2.0,1.0); table:(6.0,5.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | D | 对 | B3_pair | 否 | 0.57 | refrigerator:(2.0,4.0); stove:(5.0,3.0); table:(5.0,8.0) |
| threeview | D | 对 | B3_pair,B4_scale | 否 | 1.22 | refrigerator:(1.5,3.5); stove:(3.5,3.5); table:(6.5,6.5) |
| threeview_2stage | D | 对 | B3_pair | 否 | 0.76 | refrigerator:(2.0,3.0); stove:(5.0,3.0); table:(5.0,7.0) |
| threeview_3pass | D | 对 | B3_pair,C8_height | 否 | 0.99 | refrigerator:(2.0,8.0); stove:(3.0,5.0); table:(6.0,5.0) |


## 问题 `47430034`（arkitscenes · object_rel_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\arkitscenes\47430034.mp4`
- 问题：Measuring from the closest point of each object, which of these objects (chair, stool, table, bed) is the closest to the tv?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「bed」：____
- 视频里你看到了几个「chair」：____
- 视频里你看到了几个「stool」：____
- 视频里你看到了几个「table」：____
- 视频里你看到了几个「tv」：____
2. 视频里「tv」旁边，哪个物体看起来最近（）：____
3. 视频里「bed」和「chair」哪个更高（或差不多 / 看不清）：____
- 画面里「bed」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「chair」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「stool」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「table」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「tv」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「bed」和「chair」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：bed:(5.0,2.0); chair:(5.0,7.0),(6.0,7.0),(1.0,2.0); stool:(4.0,3.0); table:(4.0,3.0),(6.0,7.0),(1.0,2.0); tv:(7.0,7.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | D | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,QA_ | 否 | 1.27 | bed:(5.0,5.0); chair:(3.0,8.0); table:(3.0,7.0); tv:(8.0,4.0) |
| threeview | D | 错 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 否 | 0.52 | bed:(5.0,4.5); chair:(2.5,5.5); table:(2.5,4.0); tv:(5.0,8.5) |
| threeview_2stage | C | 对 | A1_miss,B3_pair,B4_scale,C7_missing,C8_h | 否 | 1.01 | bed:(5.0,4.0); chair:(3.0,7.0); table:(3.0,8.0); tv:(3.0,9.0) |
| threeview_3pass | C | 对 | A1_miss,B3_pair,B4_scale,B5_adjacent,C7_ | 否 | 0.94 | bed:(5.0,4.0); chair:(3.0,8.0); table:(5.0,8.0); tv:(5.0,9.5) |


## 问题 `c50d2d1d42`（scannetpp · object_abs_distance）
- 视频：`C:\Users\贝贝\.cache\huggingface\vsibench\scannetpp\c50d2d1d42.mp4`
- 问题：Measuring from the closest point of each object, what is the distance between the door and the telephone (in meters)?
填空（只看视频）：
1. 只看视频，这道题的答案你认为是：____
- 视频里你看到了几个「door」：____
- 视频里你看到了几个「telephone」：____
2. 视频里「door」和「telephone」隔得近还是远（很近 / 中等 / 很远 / 看不清）：____
3. 视频里「door」和「telephone」哪个更高（或差不多 / 看不清）：____
- 画面里「door」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
- 画面里「telephone」偏向左边还是右边（左 / 右 / 中间 / 没看清）：____
4. 视频里「door」和「telephone」大概相隔多远（<1米 / 1~3米 / >3米 / 看不清）：____
5. 这些物体视频里都出现了吗（都出现 / 只出现部分 / 都没看清）：____
6. 备注：____

参考（不用填）：
- GT TOP：door:(0.0,3.0); telephone:(7.0,3.0)

| arm | 模型答案 | 对错 | tags | 镜像 | RMSE | 模型TOP（对齐） |
|---|---|---|---|---|---|---|
| baseline | 2.0 | 错 | B3_pair,QA_wrong | 否 | 1.02 | door:(1.0,5.0); telephone:(5.0,4.0) |
| threeview | 4.5 | 错 | B3_pair,QA_wrong | 否 | 0.71 | door:(1.2,8.8); telephone:(4.2,4.8) |
| threeview_2stage | 2.0 | 错 | B3_pair,QA_wrong | 否 | 1.02 | door:(1.0,5.0); telephone:(5.0,4.0) |
| threeview_3pass | 2.1 | 错 | B3_pair,QA_wrong | 否 | 1.02 | door:(1.0,5.0); telephone:(5.0,4.0) |

