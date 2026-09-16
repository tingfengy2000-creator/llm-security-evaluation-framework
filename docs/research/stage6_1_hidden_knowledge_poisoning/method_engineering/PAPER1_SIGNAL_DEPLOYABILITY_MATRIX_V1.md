# Paper 1 Signal Deployability Matrix V1

Status: `42_OF_42_AUDITED / INPUT-AVAILABILITY-BASED / NOT_A_PERFORMANCE_RANKING`

Deployability 只由 inference 时输入是否合法可获得决定，不由 Final72 AUROC 或类间差异决定。逐 signal 的机器可读矩阵位于
Git-external evidence：`paper1_retrieval_behavior_harness_20260915/deployability/`。

| 当前状态 | Signal 数 | 含义 |
| --- | ---: | --- |
| `DIAGNOSTIC_ONLY` | 29 | 当前实现使用人工预匹配 E1/E2；未建立独立 Evidence retrieval，不能直接部署 |
| `QUERY_RUNTIME_ONLY` | 4 | query trace 合法可得；包括 top-k semantic、rank、score、stability |
| `DEPLOYABLE_AFTER_VERSION_REGISTRY` | 7 | 还需要 label-free Trusted Version Registry 才能计算 current/history Top-K 关系 |
| `NOT_READY` | 2 | MLM/PPL 仍需单独冻结 checkpoint、tokenizer 与 policy |

对应 evidence access mode 为：`ORACLE_MATCHED_EVIDENCE_DIAGNOSTIC_ONLY=29`、
`QUERY_RETRIEVAL_TRACE=4`、`VERSION_REGISTRY_LOOKUP=7`、`CANDIDATE_ONLY=2`。

“Oracle-only”不是说 signal 无研究价值，而是当前 Pilot 已经知道 Candidate 对应哪两个 E1/E2；真实系统若没有独立
Evidence retrieval 或 registry，就不应假装拥有同样输入。未来可通过可信检索器把部分 signal 转为
`DEPLOYABLE_AFTER_TRUSTED_RETRIEVER` 路径，但本轮没有自动升级。
