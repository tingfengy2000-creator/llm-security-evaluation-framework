# ADR 0007：Embedding 与 VectorStore 基础设施边界

## 状态

已接受，2026-07-16；由 S6-T4 实施。

## 决策

EmbeddingProvider 与 VectorStore 分离。Provider 只把文本转换成固定维度、有限、不可变的数值
向量；VectorStore 只持久化向量、受控 content reference 与公开 metadata，并返回稳定的领域
`VectorSearchHit`。后续 Retriever 必须依赖 `VectorStore` 协议，不能读取 Chroma 原始对象。

S6-T4 同时提供两种 Provider：不联网、不加载 Torch 的 `StaticEmbeddingProvider` 用于单元测试；
惰性 `SentenceTransformerEmbeddingProvider` 用于固定 revision 的真实模型路径。真实模型测试不
是快速 CI 的强依赖，只有 `LLMGUARD_RUN_REAL_EMBEDDING_TESTS=1` 才执行。

## 原因

- Static Provider 让持久化、排序、fingerprint 与 metadata 测试可在不下载模型时稳定复现；
- 真实 Provider 保留模型版本、维度、归一化、device 与依赖版本，使后续真实语义实验可追溯；
- Chroma API 返回结构与距离细节被 adapter 屏蔽，避免其变化污染 Retriever 领域接口；
- 公开 metadata 白名单和 fingerprint 排除 Ground Truth，使标签隔离成为基础设施约束而非口头
  约定；
- 真实模型下载、缓存和网络失败具有环境依赖，不能让每次本地或 CI 快速回归都承担该风险。

## 后果与边界

`CollectionFingerprint` 在 corpus、切分、模型或向量 schema 的语义字段变化时产生新 collection，
避免覆盖不兼容索引。它不包含机器路径、用户名、创建时间、随机数或评测标签。Chroma 保存
embedding、严格白名单 metadata 与 `content_ref`，不保存完整正文到审计输出。

本 ADR 不实现 Retriever、RetrievalEvidence、ContextBuilder、EvidenceSignal、TrustAggregator、
RetrievalPolicy、LLM、Evaluator 或正式安全实验。它只提供这些后续能力所需的可复现存储边界。
