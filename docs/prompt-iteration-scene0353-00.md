# Prompt 迭代：scene0353_00（vsi_subset_200[108]）

## 原结果（200 批，threeview 单次）

- 题目：refrigerator / bed / window / trash bin 中哪个离 door 最近
- GT：D（trash bin）；模型：B（bed），错误
- 地图问题：漏画 refrigerator；door 被放在角落，trash bin 距离判断错

## 本次尝试的 3 个变体

| 变体 | 说明 | missed | pairs | 答案 |
|---|---|---|---|---|
| countall | 强制每个 focus 类别都必须出现 | 0 | 2/10 | B（仍错） |
| anchor | 以题目参考物为锚点，自检各候选相对远近 | 1 | 2/6 | D（正确） |
| both | countall + anchor | 0 | 3/10 | B（仍错） |

## 观察

- countall 能修复漏画（refrigerator 出现），但没有修复相对布局，答案仍错。
- anchor 单独用时地图绝对坐标仍与 GT 差很远，但模型在自己地图内以 door 为锚重新核算了距离，推理自洽地选择了 trash bin，答案变正确。
- both 反而退回 B：指令叠加可能让模型在“补全类别”和“锚点自检”之间产生冲突，需要单独验证。

## 结论

单个 failure case 上，anchor 自检是一个有信号的方向，但单样本不能下结论；下一步在 200 批里 threeview 的 rel_distance 错题（约 13 条）上批量验证 anchor 变体，统计命中率后再决定是否回灌主 prompt。
