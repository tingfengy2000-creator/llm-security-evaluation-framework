# ADR 0008：受控检索与可追溯上下文边界

## 状态

设计已接受为 S6-T5 冻结候选，2026-07-19；等待人工审查。Python 实现未开始。

## 背景

S6-T4 只提供向量化和向量存储。如果 Retriever 直接返回正文、ContextBuilder 直接读取 Chroma，或在
Trust 计算前把结果命名为 Trusted Context，就会把检索正确性、正文权限、安全策略和审计混成一个无法
消融的组件。本 ADR 固定 S6-T5 的层间边界。

## 决策

### 1. Retriever 不返回正文

Retriever 只返回带稳定身份、来源、rank、distance、similarity、content hash 和 opaque reference 的
`RetrievalEvidence`，另生成不含 Query/正文的 `RetrievalTrace`。这样普通检索日志可审计而不会自动
复制敏感语料，Retriever 也无法越权构造 Prompt。

### 2. 正文通过 ContentRef 受控解析

新规范引用为 `corpus:<corpus_snapshot_id>:<chunk_id>`。`ContentResolver` 在受控 corpus snapshot 中
解析正文并核对 content hash；hash 不一致立即阻断。S6-T4 的 `chroma:<doc_id>` 仅作为历史测试 fixture
兼容 scheme，由后续 adapter 显式迁移，不修改历史实现，也不把 Chroma 变成正文权威源。

### 3. Evidence UID 与 Citation ID 分离

Evidence UID 由 corpus snapshot、chunk、正文 hash 和 schema 稳定产生，用于跨运行归因；Citation ID
按当前 Context 最终顺序分配为 `E1`、`E2`，只服务可读回答。`CitationBinding` 保存两者映射，使未来
Citation Accuracy、幻觉溯源和污染归因都能回到稳定证据。

### 4. S6-T5 只输出 RetrievedContextPackage

ContextBuilder 只证明“这些被检索的证据经过受控解析、hash 校验、结构转义和预算后进入了 Context”，
不证明证据可信。因此输出必须叫 `RetrievedContextPackage`，不能提前命名为 Trusted。

### 5. TrustedContextPackage 属于后续 Trust Pipeline

只有经过 `EvidenceSignal -> TrustAggregator -> RetrievalPolicy` 后才能形成 `TrustedContextPackage`。
这条链属于后续获批任务，S6-T5 不提供空壳实现。Stage 7 只能消费 Trusted Context 与脱敏
`RAGSecurityEnvelope`，不得直接消费 Retrieved Context 或 Chroma。

### 6. Citation 是强制长期能力

S6-T5 冻结 `off/available/required` 三种 Citation Mode、结构化证据 ID 和绑定。后续 Generator 必须
真实使用 Citation instruction，Evaluator 必须实现 Citation Accuracy；不能长期保留无行为的占位字段。

### 7. Context 日志不能保存正文

污染正文可在无防护研究基线中进入受控内存 Context，以观察传播，但普通日志、Trace、异常和默认审计
serialization 只保存 ID、hash、有限 metric、来源、版本、数量、时延和错误类型。完整 Query、正文、
rendered Context、Ground Truth、标签、密钥和本机路径均被禁止。

### 8. 当前只实现 Dense Retrieval

Dense Retrieval 直接复用 S6-T4 的 EmbeddingProvider 与 VectorStore，变量最少，便于先验证 ID、排序、
正文权限和 Trace。BM25、Hybrid、Rewrite、Cross-Encoder 和 reranker 会改变实验变量，必须在独立设计和
消融中增量加入。

### 9. 复杂 Chunking 只冻结接口

当前短文档只需要 `IdentityChunker`。Fixed Token、Overlap、Sentence 和 Semantic Chunking 会引入
tokenizer/model revision、阈值和新的实验变量，本阶段只冻结 `Chunker` Protocol、配置 hash 和稳定
Chunk ID，不创建 `pass` 空壳。未来实现相同 Protocol，因此 Retriever 和 ContextBuilder 无需重写。

### 10. Stage 7 只能消费 Trusted Context

Agent 可能把上下文转化为工具调用、记忆和副作用。如果它直接读取 Retrieved Context，检索污染会绕过
Trust 决策进入高风险执行链。固定 Trusted Context + Security Envelope 输入，是把 RAG 风险传播到
Agent 时仍保持最小权限和审计边界的前提。

## 哈希与配置边界

Chunk、Evidence、Trace、Context 和 Package 身份都使用 canonical JSON UTF-8 + SHA-256，排除路径、
用户名、时间、随机数和 Ground Truth。文档向量配置继续由 S6-T4 的
`document_embedding_spec_hash` 进入 collection fingerprint；`query_prefix` 不改变已存文档向量，因此
只进入 `query_embedding_spec_hash` 和未来 RunManifest。

## 结构转义边界

Evidence 正文进入 XML-like block 前必须转义 `& < >` 以及属性内引号，避免正文伪造结构闭合。
Escaping 只保护结构边界，不能阻止语义 Prompt Injection，也不构成完整 Guard。

## 后果

- 优点：检索、正文解析、Context 构建、Trust 和审计可独立测试与消融；正文泄露面更小；Citation 可
  回溯到跨运行稳定证据；未来 Chunking/Hybrid/Trust 可增量扩展。
- 代价：需要维护 ContentResolver、双层 ID、hash 验证和受控序列化；完整 Context 若需持久化必须走
  单独的敏感 artifact policy。
- 当前边界：本 ADR 只冻结决策，不证明 Retriever、Resolver、ContextBuilder、Trust 或 RAG 实验已经
  实现。

## 关联文档

- S6-T5 唯一设计规格：`docs/superpowers/specs/2026-07-19-s6-t5-controlled-retrieval-traceable-context-design.md`
- S6-T5 唯一实施计划：`docs/superpowers/plans/2026-07-19-s6-t5-controlled-retrieval-traceable-context.md`
- S6-T4 边界：`docs/architecture/0007_embedding_vectorstore_boundary.md`
- Trust/Audit 边界：`docs/architecture/0004-trusted-context-vs-audit-envelope.md`
