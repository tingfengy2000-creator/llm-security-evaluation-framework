# Paper 1 Canonical Research Route

> Status: ACCEPTED AS CURRENT RESEARCH ROUTE
> Formal experiment: FORMAL_EXPERIMENT = NOT STARTED
> Owner decisions: PODR-035 through PODR-040
> Execution records: REL-2026-0004 through REL-2026-0006

本文是 Paper 1 当前唯一 canonical research route。重大方案变化不得静默覆盖：必须追加/引用 PODR Decision ID、
Research Execution Log ID、related Git commit，并说明 Why changed、Who approved、When 和 Evidence。

## 1. Working Title

中文工作题目：

> 《版本化 RAG 知识库中的隐蔽事实污染：基准构建与多视角检测方法》

英文工作题目：

> *Stealthy Factual Poisoning in Versioned RAG Knowledge Bases: A Benchmark and Multi-View Detection Framework*

两者均为 WORKING TITLE，不是最终投稿标题。

## 2. Research Problem

当污染文档语言自然、主题高度相关、Embedding 与 Query 仍高度相关，只修改少量关键事实，并可能伪装来源、
时间和版本时，如何检测 malicious factual mutation，同时区分 legitimate update、legitimate exception、historical
version、department-specific difference、natural conflict 与 benign noise？

## 3. Motivation

企业/教育/科研知识库中的制度、标准和事实会合法演进；仅依赖语义异常或多数一致性容易把真实更新误判为攻击。
另一方面，高相关、低编辑距离的事实篡改可以进入 Top-K 并影响 Context。Paper 1 因此同时研究 security detection
与 hard-negative utility，不把“过滤更多”自动解释为“更安全”。

## 4. Research Gap

当前外部工作分别提供 retrieval poisoning attack、poisoned-document detection 和 RAG safety benchmark，但 Paper 1
关注的 gap 是：

- version relation + temporal relation + provenance + factual change 的联合建模；
- 恶意变异与合法知识演进的可区分 benchmark；
- 五视角、可解释信号和 hard-negative FPR；
- external benchmark、中文版本化 benchmark 与 generalization 的统一证据链。

这些是 proposed gaps，需未来实验验证，不是已建立的优越性结论。

## 5. Threat Model

攻击者能够影响 retriever-visible 文档或其来源/版本声明，目标是让局部错误事实被高相关查询召回并进入
RetrievedContextPackage。攻击可发生在 indexing/retrieval 前，可能维持自然语言质量和主题相关性。

防御者可使用正文、公开 provenance/version/time 与 retrieval behavior，但不得使用 Evaluator Ground Truth、
poison label、attack ID/goal/category 或 expected answer 作为 inference feature。当前非目标包括生成模型安全结论、
生产部署、自动修复知识库和 Agent side effects。

## 6. External Baselines

| Work | Canonical role | Current status |
| --- | --- | --- |
| PoisonedRAG | PRIMARY_ATTACK_BASELINE | source aligned; reproduction not started |
| GMTP | PRIMARY_DETECTION_BASELINE | source available; internal research not blocked by current plan; strict comparison pending; redistribution license to verify |
| SafeRAG | PRIMARY_BENCHMARK_REFERENCE | source available; internal research not blocked by current plan; strict comparison pending; redistribution license to verify |
| EcoSafeRAG | DEFERRED | not a core baseline unless owner re-approves |

Published Result、Reproduced Result、Our Method Result 必须分栏，不能互相替代。

每项 baseline 独立记录 `SOURCE_ACCESS`、`INTERNAL_REPRODUCTION`、`STRICT_COMPARISON_ELIGIBILITY`、
`REDISTRIBUTION_ELIGIBILITY`、`CODE_LICENSE` 与 `DATASET_LICENSE`。公开仓库不等于无限再分发许可；未确认根
LICENSE 也不自动阻断未来经批准的内部研究工作流。这不是法律结论，明确的 upstream 条款必须遵守。

## 7. External Benchmark Track

- PoisonedRAG：NQ、HotpotQA、MS MARCO 上的 standard retrieval poisoning/exposure reference。
- GMTP：poisoned document detection、filtering、FPR、nDCG 与 ASR 的直接方法比较候选。
- SafeRAG：当前优先 Silver Noise 与 Inter-context Conflict；其余任务保持 reference status。
- 所有 strict comparison 必须尽量一致 dataset/split、attack samples/budget、retriever/embedding、Top-K、generator、
  metric definition、seed protocol 和 environment assumptions。
- 任一关键条件不一致时标记 NON_STRICT_COMPARISON，不得写“outperforms SOTA by X%”。

当前仅完成资料和协议对齐，没有运行外部 baseline。

## 8. Versioned Chinese Benchmark Track

第一版领域：enterprise 与 education_research。目标是构造许可清晰、无隐私、可审计、带知识版本关系的
中文 benchmark。每个样本需要 clean/poison/hard-negative 角色、来源、版本链、时间有效性、事实变更和评估标签的
隔离存储。真实企业内部文件不得直接作为公开论文数据。

## 9. Generalization Track

- enterprise -> education_research；
- education_research -> enterprise；
- seen attack -> unseen attack；
- low/medium stealth -> high stealth；
- PoisonedRAG attack -> natural factual poisoning。

本 Track 用于判断方法是否只记住单一领域或生成模板；当前只设计，不执行。

## 10. Dataset Strategy

数据来源顺序为公开许可文档、规则生成、受控模型辅助生成（需单独批准）、人工复核。冻结前必须定义 source
license、snapshot/hash、dedup、version lineage、split、annotation guide、inter-annotator review、label isolation 和
public/private artifact boundary。

External benchmark 与中文 benchmark 分开报告；自建 benchmark 必须通过 external track 验证泛化。

## 11. Attack Taxonomy

当前第一版只包含四类：

1. HKP-1 Numeric / Entity Factual Mutation；
2. HKP-2 Condition / Exception Mutation；
3. HKP-3 Temporal / Version Poisoning；
4. HKP-4 Provenance / Source Camouflage。

禁止自动增加 attack family。任何新 family 必须经过 Research Route Review、Owner Decision 和 ledger entry。
早期讨论中更宽的 taxonomy 不从聊天记忆重建；当前四类由项目负责人在 2026-07-31 明确确认，见 PODR-038
与 REL-2026-0006。相关已提交 LR1 route 基础为 1294632；本次扩展 commit 由 Git 动态解析。

## 12. Stealth Model

- S1 Low：表面异常或变更较明显；
- S2 Medium：语言自然、局部事实变化、来源/时间部分伪装；
- S3 High：主题/风格/Embedding 高一致，关键事实、来源和版本关系均尽量隐蔽。

Stealth 不得只由单一 similarity 或人工主观等级决定；未来协议需冻结可观察维度、标注规则和一致性复核。

## 13. Hard Negatives

Benchmark 必须重点包含：legitimate policy update、legitimate new version、legitimate exception、historical but
valid version、department-specific legitimate difference、natural knowledge conflict、OCR/formatting noise 和
paraphrase。

Hard negatives 用于防止 Detector 学会“与多数文档不同 = poisoned”。必须单独报告 Hard Negative FPR，并按类型
给出分层错误分析。

## 14. Multi-View Detection

| View | First-version signals |
| --- | --- |
| V1 Semantic | naturalness、topic consistency、semantic anomaly |
| V2 Entity-Claim | numeric/date/role/entity/condition/exception/factual relation；cross-document conflict 暂并入此处 |
| V3 Provenance | publisher、source type、source-topic consistency、source chain |
| V4 Temporal-Version | ordering、effective date、repeal/supersede、transition、factual evolution |
| V5 Retrieval-Behavior | similarity、rank、rank shift、target-query concentration、Top-K/package exposure |

输出候选是 Poison Risk Score、Prediction、Explainable Signal Contribution。Cross-document conflict 当前并入
V2/V4，避免第一版无限膨胀。Ground Truth 禁止作为 inference feature。

## 15. Baselines

- Always Clean / Majority；
- Version/Temporal Rule；
- TF-IDF 或 character n-gram + Logistic Regression；
- Embedding Outlier；
- GMTP；
- Single-View Detector；
- Multi-View Detector candidate。

LightGBM、XGBoost 和 small MLP 只是 fusion 候选，不预设优胜者，也不自动作为最终 Proposed Method。

## 16. Proposed Method Boundary

暂称 Version-Aware Multi-View Poison Detection。当前只冻结问题、信号类别、输出和比较边界；不冻结最终
feature extractor、fusion estimator、threshold、calibration 或 deployment policy。没有 Detector 实现、训练或结果。

## 17. Metrics

- Primary detection：AUPRC、F1、Recall under controlled FPR、AUROC；
- Safety/retrieval：Filtering Rate、Poisoned@K、Retrieval Poison Rate、ASR；
- Utility：Recall@K、MRR、nDCG@K、Hard Negative FPR；
- Efficiency：feature extraction latency、detector latency、GPU/CPU memory、throughput。

每个指标必须冻结公式、分子/分母、aggregation、threshold、confidence interval 和 missing/invalid handling。

## 18. Statistics

未来 formal protocol 应定义多 seed/repeat、均值/中位数、标准差或置信区间、paired comparison、multiple-comparison
控制、effect size 和 failure/invalid run policy。单次 run、best seed 或仅有工程 smoke 不得填入正式结果表。

## 19. Ablation

| Contribution | Required direct evidence |
| --- | --- |
| Version-aware signals | remove V4；恶意 mutation vs legitimate evolution 分层混淆矩阵 |
| Provenance signals | remove V3；source camouflage vs legitimate department difference |
| Multi-view fusion | same feature budget: best single view vs full multi-view |
| Hard-negative design | with/without hard-negative training on fixed hard-negative test |
| Retrieval behavior | remove V5；Poisoned@K/RPR 与 detection/utility 联合变化 |

## 20. Cross-domain Evaluation

在固定 label policy、attack families、metric definitions 与 resource budget 下执行 enterprise/education_research 双向
迁移；同时报告 in-domain 和 out-of-domain，避免只展示有利方向。

## 21. Unseen Attack Evaluation

按 attack family/template/source/stealth 明确划分 seen/unseen。不得把随机拆分导致的模板泄漏写成 unseen
generalization。计划包含 seen -> unseen 与 S1/S2 -> S3。

## 22. Adaptive Attack Plan

Adaptive attack 属于后期单独审批：攻击者可能针对已知 views 调整自然性、来源、时间或 rank exposure。当前不生成
adaptive samples，不实现 attack optimizer，也不将其纳入第一版自动范围。

## 23. Resource Plan

资源数字必须区分 author-reported facts、Worker Bootstrap evidence 和 baseline-specific measurement。已接受的 Worker
基础事实是 RTX 5090、PyTorch-reported 31.84 GB VRAM、approximately 64 GiB RAM、approximately 2 TB research NVMe、
PyTorch 2.13.0+cu130 / runtime 13.0、FP16/BF16 basic tensor PASS；这些不能自动等价于论文 A6000/H800 或
baseline-specific performance。完整 data/model/index/disk、peak runtime/resource 与 API 成本仍待 R0。

## 24. Dual-machine Execution

LOCAL = CONTROL_PLANE，RTX5090 = COMPUTE_WORKER，Context Sync = Git。Bootstrap 已人工接受，Worker 的
`347dc2b...` branch/remote clean sync 与 baseline tag target 已验证。Worker 执行 R0 前仍必须 pull 最新治理 commit 并核对
branch、RunManifest.git_commit、clean tree、dataset/config/model identity 和 environment fingerprint；不一致 fail
closed。详见 [Dual-Machine Policy](../../governance/dual_machine_execution_policy.md)。

## 25. Known Risks

- PoisonedRAG paper-result commit/dependency lock/GPU-RAM-disk 未完整确认；
- GMTP/SafeRAG `CODE_LICENSE=UNCONFIRMED`，因此 `REDISTRIBUTION_ELIGIBILITY=TO_VERIFY`；这不自动阻断未来获批的内部研究；
- data/model/API revisions 与 evaluator snapshots 可能不可恢复；
- Worker base PyTorch/Blackwell compute 已通过；各 baseline 的旧 CUDA/PyTorch/FAISS/Pyserini 仍有兼容风险；
- 32 GB VRAM 可能无法容纳论文全部模型矩阵；
- hard negatives、version lineage 和 split leakage 可能削弱结论可信性；
- benchmark/data 许可和公开 artifact 边界尚未关闭。

这些集中登记为 BLK-S6.1-LR1-001；compatibility workaround 只能标记 MITIGATED，不能自动 RESOLVED。

## 26. Confirmed Decisions

- Paper-First Comparative Evidence Principle 是论文工作的最高研究方法优先级，但不覆盖 ethics/privacy/label
  isolation/immutable assets/approval gates；
- PoisonedRAG、GMTP、SafeRAG 分别为第一轮 attack/detection/benchmark reference；EcoSafeRAG DEFERRED；
- Paper 1 当前贡献方向为 Benchmark + Multi-View Detection；
- 第一版四类 HKP、五个 Views；Cross-document conflict 暂并入 V2/V4；
- LOCAL/RTX5090 分别为 Control Plane/Compute Worker；Git 是 context sync；
- S6.1-LR1、Context Recovery Governance 与 Paper-First Principle 已 HUMAN_ACCEPTED；
- RTX5090 Bootstrap 已 `HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY`；
- S6.1-R0 已 `APPROVED_TO_START` on Compute Worker；S6.1-P1 在 R0-I 审核前暂缓。

权威 Decision IDs 见 PODR-035–PODR-047。

## 27. Pending Decisions

- R0-A 至 R0-H 的实际 environment、artifact、compatibility、resource 与 feasibility facts；
- R0-I 完成后 S6.1-P1 是否批准及其具体协议范围；
- 外部 artifact 许可、paper-result commits 和 dependency/model/data snapshots；
- 中文 benchmark 数据源、annotation protocol、split 和 publication license；
- final feature set/fusion、threshold/calibration、statistics 和 adaptive attack；
- Worker environment preparation、smoke/formal reproduction 和预算。

未确认项保持 PENDING_CONFIRMATION 或 UNKNOWN。

## 28. Claims Boundary

可以宣称：Paper 1 路线可由 Git 恢复；RTX5090 Bootstrap 对 WSL GPU、PyTorch cu130、FP16/BF16 basic tensor
computation 和 Git sync 已人工接受；R0 已批准在 Worker 开始。

不能宣称：dataset、Detector、training、reproduction、5090 measurement、统计结果、SOTA、generalization、security
effectiveness 或 production readiness 已完成。

## 29. Publication Positioning

Paper 1 定位是 versioned RAG knowledge base 中 stealthy factual poisoning 的 benchmark 与 multi-view detection。
投稿叙事必须以严格外部对标、中文版本化 gap、hard-negative credibility、cross-domain/unseen robustness 和
reproducibility 为支撑；仅有工程框架或治理文档不足以构成论文结果。

## 30. Next Gate

R0 已批准。RTX5090 pull 最新 Control Plane commit 后按
[S6.1-R0 Reproduction Preflight](s6_1_r0_reproduction_preflight.md) 从 R0-A 串行执行；不匹配或受限依赖 fail
closed。R0-I Control Plane Review 后才可考虑 S6.1-P1。Dataset、Detector、training 与 Formal Experiment 仍需后续
独立批准。Auto Continue = NO，不得从 R0 自动进入 P1。
