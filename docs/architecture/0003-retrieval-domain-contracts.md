# ADR 0003：Retrieval Domain 契约与标签隔离

> A1R 补充：规范 Retrieval 根已从 A0 草案中的 `src/codeguarder/` 迁至
> `src/llmguard/`；旧 `codeguarder.stage6_rag` 仅作兼容 facade。
>
> 2026-07-19 长期需求补充：本文的未来契约受
> [长期研究需求基线](../governance/long_term_research_requirements.md) 约束。S6-T5 先实现透明
> Dense Retrieval；Evidence UID、Citation ID、Retrieved/Trusted Context Package 和 abstention
> 字段必须增量加入，不得把未可信分析的上下文提前命名为 Trusted。

## 状态

已接受，2026-07-16。

## 规范目录

未来 Retrieval 领域实现固定为：

```text
src/llmguard/domains/retrieval/
├── contracts/       # RAG 领域不可变对象与 schema
├── attacks/         # R1–R6、攻击配方与研究映射
├── corpus/          # 加载、规范化、切分、快照、污染构造
├── embedding/       # EmbeddingModelSpec 与 Provider
├── vectorstore/     # VectorStore、ChromaStore、InMemoryStore
├── retrieval/       # Retriever、Proxy、Trace、Ranking
├── trust/           # 信号、聚合器、策略
├── context/         # 内容解析、上下文构建和净化
├── generation/      # Prompt 模板与 Provider 适配
├── evaluation/      # GroundTruthVault、指标、Taxonomy、Validator
├── orchestration/   # Runner、Experiment Matrix、Run Context
└── reporting/       # JSON、CSV、Markdown、Figure
```

真实 Chroma 实现固定命名为 `vectorstore/chroma_store.py`；测试替代固定命名为 `vectorstore/in_memory_store.py`。`vector_db_simulator.py` 不得成为规范实现名称；如旧调用确实需要，未来只提供兼容 alias。

## S6-T4 基础设施边界

S6-T4 已实现 `EmbeddingModelSpec`、Static/SentenceTransformers Provider、`VectorStore`、
InMemory 与 Persistent Chroma adapter。该层只处理文本向量、公开 metadata、collection
provenance 和稳定排序；它不创建 `RetrievalEvidence`，不读取 Ground Truth，不决定哪些文档
应被业务检索，也不构建 Prompt 或 Context。

collection fingerprint 只包含语料公开 hash、切分配置 hash、文档向量的
`document_embedding_spec_hash`、距离度量和公开 schema 版本；它不包含本机路径、创建时间、随机数、
query prefix 或 Ground Truth hash。文档 metadata 只允许 `doc_id`、来源、时间、版本、content hash
和有限的公开索引字段。完整正文仍由未来 S6-T5 的受控 ContentResolver 解析；Chroma 的 `documents`
字段仅保存受控 `content_ref`。

## 稳定对象

通用层未来提供 `RunManifest`、`ArtifactReference`、`HashReference`、`ProviderRequest`、`ProviderResponse`、`GuardDecision`、`DetectorVerdict`、`MetricValue` 和 `ValidatorResult`。

Retrieval 领域提供 `DocumentRecord`、`ChunkRecord`、`QueryRecord`、`RetrieverQueryRecord`、
`RetrievalCandidate`、`RetrievalEvidence`、`EvidenceEnvelope`、`EvidenceSignal`、`TrustAssessment`、
`RetrievalDecision`、`RetrievedContextPackage`、`TrustedContextPackage`、`RAGAttemptRecord` 和
`RAGSecurityEnvelope`。`ChunkRecord`、Evidence UID/Citation ID、citation mode 与 abstention 字段的
稳定语义以长期需求基线为准；它们由后续获批任务以测试先行方式实现。

## 标签隔离

Retriever、Chroma metadata、EvidenceSignal、TrustAssessment、Context、Prompt、Provider Request、Retrieval Trace、报告和日志均不得读取或暴露：

```text
poisoned, poison_label, attack_goal, expected_answer,
failure_type, oracle, ground_truth
```

包括文件名、路径、doc_id 前缀、collection 名、source_id 和 debug repr 在内的间接泄露均被禁止。只有 `GroundTruthVault` 和 `RAGEvaluator` 可读取真实标签。

## 兼容性

R1–R6 与 T10–T15 保持原 ID、名称和语义。新增的 `attack_layer`、`attack_mechanism`、`attack_objective`、`corruption_type`、`stealth_level`、`propagation_target` 以及 `failure_stage`、`failure_cause`、`failure_effect` 是正交研究字段，不替代历史分类。

## 验收

迁移后旧 `tests/stage6_rag`、新增 import compatibility 测试和 no-label-leakage 测试都必须通过；公开视图和 Evaluator Ground Truth 视图保持物理分离。
