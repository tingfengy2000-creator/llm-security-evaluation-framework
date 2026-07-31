# Stage 6.1 Hidden Knowledge Poisoning Learning Guide

> Authority: **NON_AUTHORITATIVE_EDUCATIONAL_MATERIAL**
> Canonical route: [Paper 1 Research Route](../research/stage6_1_hidden_knowledge_poisoning/paper1_research_route.md)
> Current state: [Current Work State](../governance/current_work_state.md)

## 1. Stage 是什么

Stage 6.1 研究 RAG 知识库中的隐蔽事实污染：恶意文档看起来自然、与查询高度相关、只修改少量关键事实，
并可能伪装来源、时间和版本。当前 Paper 1 方向是 Benchmark + Multi-View Detection；不是最终 Detector 或已完成实验。

## 2. 为什么存在

传统输入/输出 Guard 看到的是 query 和 answer，而知识污染在索引前或检索层改变模型“依据什么回答”。企业知识库
还会合法更新、例外和保留历史版本，因此简单的“与多数不同即污染”会产生高误报。

## 3. 与上一 Stage 的关系

S6-T5 已接受可追踪、label-isolated 的 retrieval-to-context engineering baseline。Stage 6.1 复用 Request、Evidence、
Trace、ContentRef、Envelope 和 RetrievedContextPackage 的边界，新增的是 poisoning threat model、benchmark、signals
和 evaluation；不改写 S6-T5。

## 4. 前置知识

需要理解 Embedding、Dense/BM25/Hybrid Retrieval、Top-K、Reranker、RAG pipeline、classification metrics、class
imbalance、provenance、temporal/version semantics、ablation、cross-domain 和 label leakage。

## 5. 中英文术语

| Term | 中文与本文口径 |
| --- | --- |
| Knowledge Poisoning | 攻击者改变知识库内容或可信关系，使下游检索/回答偏离真实目标 |
| Retrieval Poisoning | 让恶意文档被检索、提高排名或扩大 Top-K exposure |
| Hidden / Stealthy Poisoning | 语言自然、主题相关、修改局部事实且尽量绕过简单异常检测 |
| Factual Mutation | 修改数值、实体、日期、条件、例外或关系，而非只注入显眼指令 |
| Version-aware | 联合 version relation、time、provenance 和 factual changes，不是版本号大小 |
| Benchmark | 冻结样本、split、标签、hard negatives、协议和指标的比较载体 |
| Multi-view Detection | 从 Semantic、Entity-Claim、Provenance、Temporal-Version、Retrieval-Behavior 联合判断 |
| Hard Negative | 与污染信号相似但合法的更新、例外、历史版本、冲突、OCR 噪声或 paraphrase |

## 6. Threat Model

攻击者可提交或影响 retriever-visible 文档，目标是改变关键事实并提高特定 query 的 exposure/answer impact。当前四类
为 HKP-1 Numeric/Entity、HKP-2 Condition/Exception、HKP-3 Temporal/Version、HKP-4 Provenance/Source
Camouflage。攻击者不能把 Ground Truth 标签直接送入 inference；防御者只能使用运行时合法信号。

## 7. Architecture

```text
Versioned Corpus -> Retriever -> RetrievalEvidence/Trace -> Multi-View Features
-> Candidate Detector/Fusion -> Poison Risk Score + Prediction + Explainable Contributions
-> Evaluator-only Ground Truth -> Metrics
```

当前 Detector/Fusion 尚未实现；上图是 proposed research architecture。

## 8. Data Flow

公开/运行时文档携带内容、来源、版本和检索身份；Evaluator 单独保存 poison label、attack family、expected behavior。
训练/evaluation split 和 feature generation 都必须证明 Ground Truth 未泄漏到 runtime metadata、fingerprint 或特征。

## 9. Core Components

- External Benchmark Track：PoisonedRAG、GMTP、SafeRAG。
- Versioned Chinese Benchmark Track：enterprise + education_research。
- Generalization Track：cross-domain、unseen attack、stealth shift；adaptive attack 后续单独审批。
- Multi-View candidate：五视角与 fusion 候选；当前仅设计。

## 10. 核心代码目录

当前没有 Stage 6.1 Detector 业务源码。已接受的检索基线位于 `src/llmguard/domains/retrieval/`；本轮只新增
`docs/research/stage6_1_hidden_knowledge_poisoning/` 和治理/学习文档。

## 11. 核心数据结构

未来可能需要 version relation、effective/expiration/repeal、publisher、claim spans、retrieval exposure 和 feature
provenance，但 schema 尚未冻结。Ground Truth 不得进入 inference feature。

## 12. 关键算法

外部算法包括 PoisonedRAG attack generation、GMTP poisoned-document detection/filtering 和 SafeRAG evaluation
pipelines。Our Method 暂称 Version-Aware Multi-View Poison Detection；fusion estimator 未冻结。

## 13. Experiment Design

三条 track 都处于 planning。未来 formal experiment 必须绑定 Git commit、dataset/config/model hash、seed、environment
fingerprint、run ID 和 metric definition；当前 `FORMAL_EXPERIMENT = NOT STARTED`。

## 14. Metrics

| Metric | 用途与方向 |
| --- | --- |
| AUPRC | 类别不平衡时衡量 precision-recall，全局越高越好 |
| F1 | 固定阈值下 precision/recall 调和平均，越高越好 |
| AUROC | 跨阈值 ranking；严重不平衡时不能单独使用 |
| Filtering Rate | 被过滤文档比例；需与 utility/FPR 联合解释 |
| Poisoned@K | Top-K 中污染文档数量/存在性，越低越好 |
| Retrieval Poison Rate | 污染检索 exposure 比例，越低越好 |
| ASR | 攻击目标成功比例；必须明确分母和 generator/evaluator |
| nDCG@K | 考虑 rank 的检索效用，越高越好 |
| Hard Negative FPR | 合法复杂样本被误报比例，越低越好 |

Recall@K、MRR、latency、memory 和 throughput 是 utility/efficiency guardrails。

## 15. 为什么选择这些指标

AUPRC/F1/AUROC 评估 detection；Poisoned@K/RPR/ASR 追踪风险传播；nDCG/Recall 衡量正常检索效用；Hard Negative
FPR 防止模型学成“少数/冲突=恶意”；latency/memory 说明工程代价。单一准确率无法覆盖这些维度。

## 16. External Papers

- PoisonedRAG：PRIMARY_ATTACK_BASELINE，标准 retrieval poisoning 与外部 attack exposure 参考。
- GMTP：PRIMARY_DETECTION_BASELINE，直接 poisoned-document detection/filtering 比较。
- SafeRAG：PRIMARY_BENCHMARK_REFERENCE，当前优先 Silver Noise 和 Inter-context Conflict。
- EcoSafeRAG：`DEFERRED`。

Published Result、Reproduced Result、Our Method Result 必须分栏。

## 17. Difference from External Work

拟研究 gap 是 versioned factual mutation、provenance/time 联合语义、难 hard negatives、跨域与 unseen attack；这些
是待证明方向，不是已经优于外部工作的结论。

## 18. Current Innovation

候选创新：version-aware benchmark、五视角 explainable signals、hard-negative credibility design、external + Chinese
双轨验证。每项必须由消融、分层误差、迁移和严格对比直接证明。

## 19. Completed Work

已完成 first-party paper/repository alignment、artifact/license registry、benchmark matrix、reproduction protocol、5090
planning、Paper 1 route 和 Git-native context recovery governance。未下载/运行外部 artifact。

## 20. Current Status

`S6.1-LR1: COMPLETED_PENDING_HUMAN_ACCEPTANCE`。S6.1-P1、dataset generation、Detector implementation 和 model
training 均未批准。

## 21. Blockers

`BLK-S6.1-LR1-001` 汇总 strict reproduction 的 paper-result commit、license、model/data revision、API snapshot 和
hardware measurement 缺口；它不阻止当前治理文档完成，但阻止严格复现/比较。

## 22. Blocker Resolution

作者确认、许可审查、固定 artifact hash、原始/兼容环境验证和批准的 worker measurement 才能逐项关闭。
Compatibility environment 是 `MITIGATED`，不是自动 `RESOLVED`。

## 23. Claims Allowed

可宣称已建立 Paper-first 对齐、三轨路线、四类 HKP、五视角、hard negatives、比较纪律、资源和治理计划。

## 24. Claims Prohibited

不可宣称外部 baseline 已复现、中文 benchmark 已构建、Detector 已实现/训练、5090 已测量、统计显著、泛化、
SOTA、RAG 安全效果或生产可用。

## 25. Reproduction Guide

遵循 [Baseline Reproduction Protocol](../research/stage6_1_hidden_knowledge_poisoning/baseline_reproduction_protocol.md)。
所有命令均是 `REFERENCE_ONLY_DO_NOT_RUN`，直至项目负责人单独批准。

## 26. Interview Explanation

30 秒版：Stage 6.1 研究自然、相关但关键事实被局部篡改的 RAG 知识污染；我先用外部论文对齐，再设计版本化
中文 benchmark、五视角检测和 hard negatives，同时隔离 Ground Truth。

2 分钟版应补充 S6-T5 evidence contracts、PoisonedRAG/GMTP/SafeRAG 角色、version-aware 不是版本号、指标与
Published/Reproduced/Our Method 分栏。

## 27. Likely Interview Questions

1. 为什么 Embedding 高相似仍可能危险？因为相关性与事实真实性/来源可信性不同。
2. 为什么要 hard negatives？避免把合法更新、例外或冲突误报为污染。
3. 为什么 AUPRC 比 accuracy 重要？污染通常类别不平衡，accuracy 会被多数 clean 样本主导。
4. 为什么 version-aware 不等于版本号？需要关系、时间、来源和事实变化联合判断。
5. 如何防 label leakage？Evaluator-only Ground Truth 与 runtime contracts 物理隔离，并递归扫描 retriever-visible 字符串。
6. 5090 为什么未必直接复现旧环境？Blackwell/CUDA/PyTorch 兼容与 32 GB VRAM 可能不同于论文硬件。

## 28. Paper Method Mapping

Threat Model 对应四类 HKP；Benchmark 对应版本关系与 hard negatives；Method 对应 V1–V5 + fusion；explanation 对应
signal contribution；label-isolation 和 manifests 对应 reproducibility/security boundary。

## 29. Paper Evaluation Mapping

External benchmark 验证与权威工作可比；Chinese versioned benchmark 验证核心 gap；cross-domain/unseen/stealth
验证泛化；ablation 证明每个 view；hard-negative FPR 验证可信性；多 seed/statistics 控制随机性。

## 30. Common Misunderstandings

- “知识污染”等于 prompt injection：错误；本研究重点是事实/来源/版本变异。
- “相关度高”等于可信：错误。
- “版本号更大”就是合法新版本：错误。
- “跑通仓库”就是复现论文：错误。
- 不同 dataset/Top-K/budget/model 的数字可以直接排名：错误，应标记 `NON_STRICT_COMPARISON`。
- Learning Guide 写完等于实验接受：错误。

## Authority Reminder

本文是 **NON_AUTHORITATIVE_EDUCATIONAL_MATERIAL**。权威事实以 Git、Owner Decision、Current Work State、
Experiment Master Record、Research Execution Log 和 accepted Paper 1 route/protocol 为准。
