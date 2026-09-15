# Paper 1 Metric and Ablation Contract V1

Status = `PLANNED / NO RESULT`

## Detection metrics

| Metric | 冻结含义 |
| --- | --- |
| AUPRC | Poison=1、Clean Current/Hard Negative=0 的 PR 曲线面积 |
| AUROC | 同一二分类任务的 ROC 曲线面积 |
| Recall@1%FPR | 在冻结阈值协议下总体 FPR 不超过 1% 时的 Poison recall |
| Recall@5%FPR | 在冻结阈值协议下总体 FPR 不超过 5% 时的 Poison recall |
| Hard Negative FPR | `预测为 Poison 的有效 Hard Negative 数 / 全部有效 Hard Negative 数` |
| Precision / Recall / F1 | development-selected threshold 下按冻结分母计算 |
| Brier / ECE | 仅用于 Risk calibration 阶段 |

`Hard Negative FPR` 是核心指标：版本感知方法不能通过把全部历史版本判毒来获得高 Poison Recall。正式执行前仍需冻结
threshold ownership、aggregation、invalid/missing handling、CI、seed/repeat 和 paired comparison。

## Ablation matrix

1. S
2. E
3. P
4. T
5. R
6. S+E+P+T+R
7. Full − S
8. Full − E
9. Full − P
10. Full − T
11. Full − R

全部结果必须同时按 HKP1、HKP2、HKP3、HKP4、S1、S2、S3 分层。任何“Full 更好”“T/P 降低 HN FPR”的文字在
实际冻结实验前只能写成 RQ，不能写成结果。
