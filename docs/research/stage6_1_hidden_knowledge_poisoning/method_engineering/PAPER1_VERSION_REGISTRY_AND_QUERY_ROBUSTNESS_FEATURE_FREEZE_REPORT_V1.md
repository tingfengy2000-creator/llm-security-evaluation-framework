# Paper 1 Version Registry、Query Robustness 与 Feature Freeze Report V1

## 结论

本轮没有直接训练 Detector。原因是上一轮 `Q_FULL` 的 Sparse Any-Evidence Recall@1 达到 0.958，但 query 同时含 source title 和完整 Candidate，57-doc Pilot corpus 又缺少足够 hard distractors；如果直接训练，Detector 可能学习 Pilot 的词面捷径，而不是可部署的版本推理。

最终状态为 `READY_WITH_LIMITATIONS`。Registry V2、四条件 Query audit、23-feature non-Oracle Document Detector Feature Set 和无标签 raw matrix 已冻结；六个仍无充分合法 inference path 的 Temporal features 被明确排除。

## Registry V1 → V2

V2 只重新读取既有 57 份冻结官方快照和 V1 accepted metadata。没有下载或加入新 Evidence，也没有读取 Clean/HN、GT、Expected 或 Owner decision 来补 metadata。

| Coverage | V1 | V2 |
| --- | ---: | ---: |
| CURRENT | 4 | 5 |
| HISTORICAL | 4 | 5 |
| effective interval | 23 | 26 |
| issuer/authority | 33 | 55 |
| predecessor | 0 | 1 |
| successor | 0 | 1 |
| supersession records | 0 | 2 |

新增关系只来自官方正文明确的“原《…》同时废止”语句。单纯时间先后只写 `chronologically_precedes`，不升级为 supersession。V1 中非法日期（例如月字段大于 12）不会进入 V2。不能由冻结 Evidence 支持的字段保持 `EVIDENCE_INSUFFICIENT`；需要新证据的补强必须另行审批。

Registry V2 SHA256：`1e76808efd3bf30115d399ac96ea2777eddd47a36cef693d569b2344acba20dc`。

## Query robustness

四套 72-query 在 Oracle E1/E2 load 前分别锁定。Sparse 固定 char 2/3-gram BM25、k1=1.2、b=0.75；Dense 固定 MiniLM revision/tree、CPU/local-only/L2；Hybrid 固定等权规则。12 runs 均确定性复跑一致。

以下为 Hybrid 的 Any/Both Recall@1/3/5/10 与 MRR：

| Query | Any Recall | Both Recall | MRR |
| --- | --- | --- | ---: |
| Q_FULL | .903 / 1 / 1 / 1 | 0 / .833 / .903 / .986 | .951 |
| Q_NO_TITLE | .917 / 1 / 1 / 1 | 0 / .778 / .903 / .972 | .958 |
| Q_TEXT_ONLY | .889 / 1 / 1 / 1 | 0 / .722 / .847 / .931 | .944 |
| Q_STRUCTURED | .722 / 1 / 1 / 1 | 0 / .764 / .861 / .917 | .861 |

完整 E1/E2、Sparse/Dense/Hybrid 指标位于 Git-external `evaluation/PAPER1_QUERY_ROBUSTNESS_METRICS_V1.json`。

### Source-title shortcut

Q_FULL 与 Q_NO_TITLE 的 Hybrid ΔAny-R@1=-0.0139、ΔMRR=-0.0069，冻结阈值下为 `SOURCE_TITLE_DEPENDENCE_RISK=NONE`。去掉 title 没有降低覆盖，因此没有理由让 title 继续进入下一阶段 query。

### Lexical-overlap shortcut

Q_TEXT_ONLY 相对 Q_STRUCTURED 的 Hybrid ΔAny-R@1=+0.1667、ΔMRR=+0.0833，结论为 `LEXICAL_OVERLAP_DEPENDENCE=MATERIAL`。不能只把 Q_TEXT_ONLY 的高 recall 当作方法有效；长 Candidate 与官方原文共享词面是 Pilot corpus 的现实捷径。Structured query 更接近 claim-level retrieval，但当前 extractor 仍损失信息，不能直接替代主设置。

## Evidence corpus difficulty

57-doc corpus 的 3,960 个 Candidate–nonreference pairs 中有 268 个 same-domain、32 个 same-subject/version-family、14 个 same-authority distractors；按冻结阈值没有 lexically-similar irrelevant hard distractor。结论为 `EVIDENCE_CORPUS_TOO_EASY_FOR_FORMAL_EVALUATION`。这不否定 Pilot 的工程价值，但禁止把 recall 外推为 formal retrieval performance。

未来 240-group 必须加入 same-domain、same-subject different-version、same-authority、current/history near-duplicate 和 lexically similar irrelevant hard distractors。

## Chosen non-Oracle setting

冻结 `Q_NO_TITLE + HYBRID + Top5`。选择顺序是 non-Oracle、label-blind、可部署、抗 title shortcut、确定性、覆盖足够；不是选择最高 recall。Q_NO_TITLE 去掉 source title，仍保留 Candidate 的完整可见 claim；Hybrid 使用预先冻结的 Sparse/Dense 等权规则。Q_STRUCTURED 作为重要 robustness diagnostic 保留，但在 extractor 信息损失修复前不作为 V1 主设置。

## PTS V3 与 Deployability V3

PTS V3：`COMPUTED=10 / EVIDENCE_INSUFFICIENT=22 / INPUT_MISSING=8 / NOT_APPLICABLE=32`。N/A、missing 和 evidence-insufficient 物理分开。

42 signals：20 `DEPLOYABLE_RETRIEVER_BACKED`、10 `DEPLOYABLE_REGISTRY_BACKED`、4 `QUERY_RUNTIME_ONLY`、6 `ORACLE_DIAGNOSTIC_ONLY`、2 `NOT_READY`。V2 Oracle-only 8 降为 V3 的 6；升级的是 `current_fact_match` 与 `historical_fact_match`，两者只在 Registry-partitioned Evidence 可用时产生值。

## Document Detector Feature Set V1

Feature Set 共 23 个：Semantic 3、Entity-Claim 9、Provenance 8、Temporal-Version 3。Retrieval Behavior R 不进入 Stage A Document Detector。六个排除项为：

- `current_history_binding_conflict`
- `effective_interval_conflict`
- `successor_exists`
- `superseded_version`
- `version_distance`
- `version_mismatch`

排除理由统一为 `NO LEGITIMATE INFERENCE PATH`。Feature 没有按 Final72 AUROC、AUPRC 或 effect size 选择。

Raw matrix 为 72 rows × 23 features，SHA256 `c1a8dfa250ab62843d9234754f27936667c2a760dbdae8be4f5405bb47dc30c0`。它不含标签、class/HKP/S、Expected、Owner/A-B、repair history、原 sample/group ID 或路径。Availability/status 单独保存，不作为 V1 model feature；null 不做 class-derived imputation。

## 下一门

当前可以准备第一版 Document Detector prototype 的单独执行合同，但仍未批准任何 fitting。精确下一任务建议：`P1-FIRST-DOCUMENT-DETECTOR-PROTOTYPE-PREFLIGHT-AND-DEVELOPMENT-PROTOCOL-FREEZE-01`，先冻结 group-aware development protocol、missingness handling、feature normalization 和禁止 test tuning 的门，再由 Owner 单独批准训练。
