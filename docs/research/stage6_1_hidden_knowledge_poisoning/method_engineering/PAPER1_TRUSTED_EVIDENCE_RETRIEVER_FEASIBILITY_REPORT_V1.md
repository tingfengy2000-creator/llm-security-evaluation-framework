# Paper 1 Trusted Evidence Retriever Feasibility Report V1

## 结论

本轮完成的是 Final72 development set 上的可信证据检索与版本注册表原型，不是 Detector 训练或正式论文结果。系统在不知道 Candidate 对应人工 E1/E2 的情况下，从 57 份去映射、按快照哈希去重的官方文档中检索；检索 trace 与 Retrieved Signal matrix 先锁定，随后才加载人工 E1/E2 作评价参考。

最终建议为 `DOCUMENT_DETECTOR_READY_WITH_LIMITATIONS`。可信检索路径已经可复现，但 Version Registry 仅有部分时间、authority 和 current/history metadata；八个 Temporal signals 仍为 `ORACLE_ONLY`。

## 输入与物理隔离

- Final72 GT：72 条，只在锁后用于分层分析，不进入 query/ranking。
- Trusted Evidence Corpus：57 documents，SHA256 `331705332f7785ef0c7cd39dbfb294f912e0bb94954974b985e5967dafe8ff7b`。
- Query：`primary_subject + source_title + candidate_text`，72 条，deterministic。
- Oracle E1/E2 mapping：单独 sealed；retrieval 和 signal processes 不接收该参数。
- Retrieval run：12,312 rows，SHA256 `037b8463e6cd2fbf3f4fd5584680e2e9edb3965a39780e92d98a194d7fa5e04a`。

## Retriever

Sparse 使用 frozen Chinese character 2/3-gram BM25。Dense 使用本地 CPU、L2 normalization 的 `paraphrase-multilingual-MiniLM-L12-v2@16e5344f...b4e1`，model tree SHA256 `14be5b8d...1fb7`。Hybrid 在 Oracle load 前冻结为 sparse/dense min-max normalization 后等权平均。K 固定为 1/3/5/10；首轮后没有调参。

| Retriever | E1 R@1/3/5/10 | E2 R@1/3/5/10 | Any R@1/3/5/10 | Both R@1/3/5/10 | MRR |
| --- | --- | --- | --- | --- | --- |
| Sparse | .556/.972/1.000/1.000 | .403/.944/.986/1.000 | .958/1/1/1 | 0/.917/.986/1 | .979 |
| Dense | .125/.278/.292/.458 | .125/.236/.292/.444 | .250/.514/.528/.681 | 0/0/.056/.222 | .409 |
| Hybrid | .542/.972/.986/.986 | .361/.861/.917/1.000 | .903/1/1/1 | 0/.833/.903/.986 | .951 |

这些数字只是 frozen packet E1/E2 reference recall。E1/E2 不是所有可能合法 Evidence 的完整真值。

## Registry 与 Signals

Registry 有 47 families / 57 versions；24 个 matched groups 中 20 个可直接按 family name 对齐。独立支持的 effective start 为 23/57、issuer 或 authority metadata 为 33/57；只有 4 current + 4 historical roles 可由完整 effective-start chronology 推导，其余保持 `UNKNOWN`。PTS V2 为 `COMPUTED=10 / INPUT_MISSING=27 / NOT_APPLICABLE=35`。

三条件均已物理输出为 72×32 S/E/P/T records：Candidate-only 计算 753/2304，Retrieved Evidence 计算 1284/2304，Oracle upper bound 计算 1180/2304。Retrieved 与 Oracle 双方均可计算的 1,179 个 numeric/binary 值精确一致率为 89.48%，MAE 0.0293，Spearman 0.9298。异构 signals 不共享统一 categorical label space，因此不伪造 aggregate Cohen kappa。这些指标衡量 signal stability，不是 Detection accuracy。

42-signal V2 边界：20 `DEPLOYABLE_WITH_TRUSTED_RETRIEVER`、8 `DEPLOYABLE_WITH_VERSION_REGISTRY`、4 `QUERY_RUNTIME_ONLY`、8 `ORACLE_ONLY`、2 `NOT_READY`。V1 的 29 个 Oracle diagnostic signals 中 21 个获得合法替代路径；八个未充分 registry-grounded 的 Temporal signals不升级。

## 风险与下一门

Sparse 的高 recall 与当前小型、同领域、标题/正文高度重合的 57-doc corpus 有关，不能外推到 240-group 或开放网络。未来 benchmark 必须保存统一 trusted corpus membership、version family/role/effective interval/authority、neutral group query、corpus identity 和 retrieval provenance，而不是每个 Candidate 只配“正确两篇”。

下一任务建议：`P1-TRUSTED-VERSION-REGISTRY-COVERAGE-REPAIR-AND-DOCUMENT-DETECTOR-FEATURE-FREEZE-01`。先对缺失 metadata 做 Owner 审批的 additive repair，再冻结非 Oracle Document Detector feature set；仍不得训练 Detector。
