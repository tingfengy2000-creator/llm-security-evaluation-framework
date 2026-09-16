# Paper 1 Signal Deployability Matrix V2

本矩阵由首轮 Trusted Evidence Retriever / Version Registry prototype 的真实合法输入路径产生，而不是按诊断 AUROC 或标签效果升级。

| V2 status | Count | 含义 |
| --- | ---: | --- |
| `DEPLOYABLE_WITH_TRUSTED_RETRIEVER` | 20 | Retrieved Top-K official Evidence 提供合法 inference path |
| `DEPLOYABLE_WITH_VERSION_REGISTRY` | 8 | PTS V2 与七个 R-version signals 需要 Registry；缺失时显式 unavailable |
| `QUERY_RUNTIME_ONLY` | 4 | query/top-k runtime 才存在 |
| `ORACLE_ONLY` | 8 | Registry-grounded Temporal semantics 尚不足 |
| `NOT_READY` | 2 | MLM/PPL checkpoint/policy 未冻结 |

V1 的 29 个 `DIAGNOSTIC_ONLY / ORACLE_MATCHED_EVIDENCE` 中 21 个已由 Trusted Retriever 或 Registry 路径取代；剩余八个不得从人工 matched E1/E2 推断部署能力。机器可读逐 signal 记录位于 Git-external evidence package 的 `deployability/PAPER1_SIGNAL_DEPLOYABILITY_MATRIX_V2.json`。
