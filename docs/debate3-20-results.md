# 三 Agent Debate Baseline — 前 20 条结果

> 数据：`src/results_debate3_20.json`（20 条，19 有效，1 条 `CRITIQUE_API_FAIL`）。对比同一批样本的 single threeview（`results_tis_200.json` 前 20 条）。

## 1. QA

| 方法 | 有效样本 | QA 正确 |
|---|---|---|
| debate3 | 19 | 2/19 |
| single threeview | 20 | 2/20 |

QA 没有变化。

## 2. 地图指标

| 方法 | 漏画率 | 对偶距离 |
|---|---|---|
| debate3 | 35/55 (64%) | 0/0（无有效类别对） |
| single threeview | 46/69 (67%) | 0/0 |

漏画率轻微改善（64% vs 67%），但样本少且误差大，不构成结论。

## 3. 跨视图一致性（三对共享轴残差中位）

两个方法都是 0.0（因为前 20 条大多是 counting / size / room / abs，单类别样本多，跨视图配对少，指标不敏感）。

## 4. 结论

- 前 20 条样本构成不适合衡量 debate：counting/size/room 类别少、`pairs=0`，跨视图一致性也测不出。
- debate 和 single 在当前子集上基本持平。
- 建议换成“分层 20 条”（覆盖 rel_distance / direction / route / appearance 等多物体、相对布局题型），或直接全量 200，再判断 debate 是否有效。
