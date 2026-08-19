# Debate v5 每轮地图指标（strat20 重跑）

> 2026-08-14 重跑 v5，20 样本 18 成功（14/15 BUILD_PARSE_FAIL），QA 9/18。带 round0/1/2/final 逐轮 map_metrics。

| 轮次 | 漏画率 | 多画率 | 对偶距离正确率 | 紧邻正确率 | 高度正确率 |
|---|---|---|---|---|---|
| round0（三 agent 初始建图） | 0.317 | 0.049 | 0.324 | 0.375 | 0.345 |
| round1（结构化偏移互评后） | 0.549 | 0.024 | 0.293 | 0.250 | 0.474 |
| round2（融合参考互评后） | 0.317 | 0.061 | 0.311 | 0.375 | 0.333 |
| final（融合后回答地图） | 0.451 | 0.049 | 0.185 | 0.000 | 0.375 |

## 诊断

1. round1 的结构化互评让漏画率从 0.317 涨到 0.549，地图明显变差；round2 的融合参考互评把它拉回 0.317，说明第二轮是有效的纠偏。
2. 最终融合（reconcile_views）反而把地图做坏：对偶距离 0.311→0.185、紧邻 0.375→0.000、漏画 0.317→0.451。
3. 也就是说当前 v5 的短板不在“三视图 agent 互评”本身，而在最后一步融合；回答阶段拿到的是比 round2 更差的地图。

## 建议

- 下一版先用 round2 的 raw combined 三视图做回答，和 final fused 做 QA 对照，确认融合是否负收益。
- 若确认，重构融合：实例数对齐（round1 漏画回升说明互评 prompt 会删实例）、跨视图 triplets 匹配、而不是 reconcile_views 按位置排序硬合并。
- 两个 BUILD_PARSE_FAIL 样本可单独重试。

## ???????????fused vs round2 ??

? --answer-map both ? strat20 ?????/?????? final fused ? round2 raw combined ???

- fused ?????7/20
- round2 ?????8/20
- ?? round2 ??fused ??2 ???? fused ??round2 ??1 ???????11 ?

????? reconcile ??? QA ?????round2 raw combined ????????????????? v5 ?? answer-map ?? round2??????????? BUILD_PARSE_FAIL ???
