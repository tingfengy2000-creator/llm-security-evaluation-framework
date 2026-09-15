# Paper 1 Final72 五视角 Signal Feasibility Report V1

Status: `FINAL72_SIGNAL_FEASIBILITY_COMPLETE / READY_WITH_VIEW_LIMITATIONS`

> 本文只报告 Final72 development set 的描述性诊断，不是 Detector 结果、正式 test 结果或论文显著性结论。

## 为什么做

本轮不是训练分类器，而是检查五种安全证据是否真实存在、能否稳定提取，以及是否可能区分 Poison 与合法历史
Hard Negative。72 条样本由 24 个完整匹配组组成，三类各 24 条。

## Label-blind 物理顺序

先从冻结 Candidate/Evidence 创建仅含文本、来源和 Evidence 的安全投影，再由独立进程生成 72×42=`3024` 行 raw
matrix。raw SHA256 为 `ab63568b86b035fa26291e8459606aacf8b745ce7f97e4b628a1da9d390fc4fd`，标签字段扫描为 0；
锁定时间早于首次 label load。锁后分析矩阵 SHA256 为
`86a9e14be536d664e3f85f6e32f0eb172b1c47ce0ab94bb1292ab7bcc037447d`。

## 各 View 的可用性

| View | COMPUTED | NOT_APPLICABLE | INPUT_MISSING | MODEL_UNAVAILABLE | 结论 |
| --- | ---: | ---: | ---: | ---: | --- |
| Semantic | 154 | 0 | 134 | 144 | `READY_WITH_LIMITATIONS` |
| Entity-Claim | 443 | 205 | 0 | 0 | `READY_WITH_LIMITATIONS` |
| Provenance | 317 | 98 | 161 | 0 | `READY_WITH_LIMITATIONS` |
| Temporal-Version | 266 | 160 | 222 | 0 | `READY_WITH_LIMITATIONS` |
| Retrieval-Behavior | 0 | 0 | 720 | 0 | `INPUT_GAP` |

MLM/PPL 没有获批冻结模型，因此不下载临时模型；GMTP 缺兼容 retriever/gradient/token-attribution/MLM bundle，状态为
`DEFERRED_WITH_REASON`。

## Poison 与 Hard Negative 的描述性差异

- `date_conflict` 与 `effective_interval_conflict` 在可比较的 3 对 3 子集上 Cliff's delta=`1.0`，但没有同组双方均可用
  的 matched pair，覆盖太小，不能推广。
- `numeric_conflict`：10 Poison vs 13 Hard Negative，delta=`0.40`，diagnostic AUROC=`0.70`；匹配组仅 3 组方向正确、
  4 组 tie、17 组不可用。
- `current_version_semantic_similarity`：24 vs 24，delta=`0.132`，diagnostic AUROC=`0.566`；匹配组 16/24 方向正确、
  8/24 相反，是覆盖最完整的弱信号。
- `condition_conflict`、`negation_flip` 的预声明方向呈反向差异，说明当前全局 cue proxy 不能直接当可靠风险信号。

## Poison 与 Clean Current 的描述性差异

`current_version_semantic_similarity` 覆盖 24/24，delta=`0.288`、diagnostic AUROC=`0.644`；日期/施行区间信号仍只在
3 对 4 小子集上可算。所有 AUROC/AUPRC 都是单变量 development diagnostic，不是 Detector 结果。

## 弱信号与冗余

`subject_match`、`entity_conflict`、`predicate_match`、`official_source`、`document_identity_match`、`official_repost`、
`present_time_substitution_signal` 为常量；`current_fact_match`、`version_identity_match`、`version_mismatch` 近常量。
发现 7 个 |rho|≥0.90 的 pair，形成 3 个簇：condition/negation/relation、date/effective-interval/numeric、
version-identity/version-mismatch。本轮未自动删除任何 signal。

## HKP 与 stealth 观察

Poison–HN 的最强 subgroup 差异分别由 HKP1 current-version similarity、HKP2 negation cue、HKP3 numeric conflict、
HKP4 negation cue，以及 S1 numeric、S2 version identity、S3 current-version similarity 给出。每格样本很小；其中反向 cue
结果仅用于发现规则缺陷，不能解释成机制已验证。

## Leakage 与 Evidence missingness

raw feature 中 Expected、GT value、A/B、Owner adjudication 使用均为 0；applicability rate 的跨类最大差未达到 0.25，
本轮 finding=0。11 项已知 Evidence limitation 分布在 7 个 sample；按 sample 的 class rate 为 Clean 16.7%、Poison 8.3%、
Hard Negative 4.2%，最大差 0.125，未观察到强类别集中，但 missingness 仍禁止进入 feature。

## Readiness

结论为 `READY_WITH_VIEW_LIMITATIONS`。S/E/P/T 已有可复现但质量参差的 signals；Temporal 核心只有部分字段可算，
Retrieval 完全缺输入。因此可以继续做受限的第一版方法工程准备，但必须单独审批；不能把当前结果称为 Five-view
Detector 效果。

下一优先任务应建立 label-blind Retrieval harness，并同步补齐显式 version role/effective interval/authority role metadata；
正式 Detector training、threshold tuning、240-group 和正式 test 仍未获批准。
