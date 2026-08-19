# Debate v2 / v3 vs Single — 分层 20 条逐样本对照（修正版）

> 回答协议已统一（debate 回答时也带视频）。数据：`results_debate3_v2_strat20.json`、`results_debate3_v3_strat20.json`、`results_tis_200.json`（single threeview）。T=对，F=错，None=答案未提取到。

## 1. 逐样本表

| id | scene | 题型 | single | v2 | v3 |
|---|---|---|---|---|---|
| 1991 | bde1e479ad | rel_distance | A/T | C/F | A/T |
| 1918 | c50d2d1d42 | rel_distance | A/T | D/F | None/F |
| 3134 | scene0608_00 | rel_distance | A/F | C/F | C/F |
| 2057 | bcd2436daf | rel_distance | D/T | C/F | D/T |
| 3132 | scene0608_00 | rel_distance | D/F | D/F | D/F |
| 3707 | scene0356_00 | direction_easy | A/F | None/F | A/F |
| 1333 | 47430048 | direction_easy | B/T | D/F | B/T |
| 1545 | 5ee7c22ba0 | direction_medium | B/F | C/T | A/F |
| 4249 | scene0328_00 | direction_medium | A/F | None/F | A/F |
| 1533 | 5eb31827b7 | direction_medium | A/F | C/F | A/F |
| 3596 | scene0645_00 | direction_hard | B/F | B/F | B/F |
| 969 | 42445026 | direction_hard | B/F | A/T | None/F |
| 1881 | 25f3b7a318 | direction_hard | C/F | C/F | D/T |
| 5094 | scene0645_00 | route | A/T | A/T | A/T |
| 4991 | 45662924 | route | A/T | A/T | D/F |
| 5028 | c5439f4607 | route | B/T | B/T | None/F |
| 5018 | 47430475 | route | B/T | B/T | B/T |
| 4513 | scene0518_00 | counting | 1/F | 1/F | 1/F |
| 4526 | scene0580_01 | counting | 2/T | 2/T | 2/T |
| 4459 | scene0663_00 | counting | 1/F | 1/F | 1/F |

## 2. 汇总（修正后）

| 方法 | n | QA | 漏画率 | 对偶距离正确 | 跨视图 top_side_y |
|---|---|---|---|---|---|
| single | 20 | 9/20 (45%) | 35% | 21/72 | 0.0 |
| v2 | 20 | 7/20 (35%) | 60% | 12/38 | 2.0 |
| v3 | 20 | 7/20 (35%) | 50% | 15/51 | 0.0 |

## 3. 结论

1. 修正协议后，v2/v3 的 QA 都低于 single，地图指标（漏画、对偶距离）也明显更差。
2. direction 上 v2 有赢有输（1545/969 赢，1333 输，多个 None），净效果不占优。
3. 之前“v2 11/19 有效”是回答协议不公平 + 小样本噪声。
4. 当前 debate 不值得作为 QA 主力；如需继续，只当跨视图一致性修正器，用 scene reconstruction metric 评估。
