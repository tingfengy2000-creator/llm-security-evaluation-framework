# S6-T5 受控检索与可追溯上下文构建设计规格

> 英文名：Controlled Retrieval and Traceable Context Construction
>
> 状态：Design Freeze completed, pending human review
>
> 实现状态：Not started
>
> 审批门：本规格和配套实施计划经人工批准后，才可开始 S6-T5.1。

## 1. 背景

S6-T4 已提供可替换的 `EmbeddingProvider`、`VectorStore`、确定性内存实现和持久化 Chroma
adapter。它解决“文本如何变成向量并稳定保存”，没有回答“如何把一次查询变成可审计证据，再安全地
构造模型上下文”。S6-T5 冻结这段中间链路，防止 Retriever、正文权限、Citation 和 Trust 在后续实现
中混为一体。

本规格是 S6-T5 的唯一细化设计。Stage 6 总体规格继续有效；发生冲突时，以项目治理文件、已接受 ADR
和本规格中更窄的 S6-T5 边界为准。

## 2. 目标

目标链路为：

```text
QueryRecord
  -> RetrievalRequest
  -> DenseRetriever
  -> EmbeddingProvider
  -> VectorStore
  -> VectorSearchHit
  -> RetrievalEvidence[] + RetrievalTrace
  -> ContentResolver
  -> EvidenceEnvelope[] + CitationBinding[]
  -> ContextBuilder
  -> RetrievedContextPackage
```

本阶段设计透明 Dense Retrieval、稳定证据身份、无正文检索轨迹、受控正文解析、结构边界转义、
Citation 模式、确定性预算和 abstention 预留。相同公开输入与配置必须得到相同 ID、排序、引用分配和
Context hash。

## 3. 非目标

S6-T5 不得实现或伪装实现 BM25、Hybrid Retrieval、Query Rewrite、Cross-Encoder、Reranker、
EvidenceSignal、TrustAggregator、RetrievalPolicy、Retrieval Guard、LLM/Groq、回答生成、Citation
Accuracy、Faithfulness、T10–T15、正式攻击矩阵、Stage 6.1、Stage 6.2 或 Stage 7。

本轮 Design Freeze 更不得创建任何 Python 业务对象或空壳。本规格中的类名和文件名均是经审批后实施
的契约，不代表代码已经存在。

## 4. 架构与依赖方向

```text
chunking/contracts
        |
        v
embedding protocol + vectorstore protocol       GroundTruthVault / Evaluator
        |                                                   X
        v                                                   X prohibited
retrieval (DenseRetriever, Evidence, Trace)                 X
        |
        v
content resolver (controlled corpus snapshot)
        |
        v
context builder (Envelope, Citation, budget, escaping)
        |
        v
RetrievedContextPackage
        |
        +---- future only ----> EvidenceSignal -> TrustAggregator
                                -> RetrievalPolicy -> TrustedContextPackage
```

固定禁止依赖：VectorStore 不 import Context；Retriever 不 import Ground Truth、具体 Chroma 或具体
SentenceTransformers Provider；Resolver 不 import Evaluator；ContextBuilder 不 import Chroma、
SentenceTransformers 或 `codeguarder`；Stage 7 不直接读取 Chroma，也不消费未经 Trust 判断的
`RetrievedContextPackage`。

## 5. Chunking 契约

### 5.1 当前能力与扩展点

当前短文档基线固定为 `one document = one chunk`，获批实现时只提供 `IdentityChunker`。接口冻结为：

- `ChunkingStrategy`：`identity`，未来增加 `fixed_token`、`token_overlap`、`sentence`、`semantic`；
- `ChunkingConfig`：策略、schema version 以及该策略真正影响切分的参数；
- `Chunker` Protocol：输入公开文档，输出不可变 `ChunkRecord` 序列；
- `ChunkRecord`：`chunk_id`、`parent_doc_id`、`chunk_index`、`content`、`content_hash`、
  `content_ref`、`chunking_strategy`、`chunking_config_hash`、`source_id`、`source_type`、
  `version`、`timestamp`、只读 `public_metadata`；
- `IdentityChunker`：不修改正文，一个 `DocumentRecord` 确定地产生一个 chunk。

`parent_doc_id` 是语料快照中的父文档身份；索引层 `doc_id` 在 S6-T5 中等同于当前向量条目的
`chunk_id`，不能再被解释成父文档 ID。这样未来一个父文档拆成多个 chunk 时无需修改 Retriever。

### 5.2 配置与 Chunk ID

统一 hash 算法：字段经 schema 校验后，以排序键、无多余空白的 canonical JSON 序列化为 UTF-8，
再计算 SHA-256。禁止本机路径、用户名、时间、随机数和 Ground Truth 进入任何身份 hash。

`chunking_config_hash` 必须覆盖：

- 所有策略：strategy、schema/implementation version；
- token 策略：tokenizer model ID、不可变 revision、window size、overlap；
- sentence 策略：sentence splitter ID、revision、locale 和边界规则；
- semantic 策略：embedding model ID、revision、threshold、最小/最大 chunk 约束。

`chunk_id` 的 canonical 输入固定为：

```text
chunk_schema_version
corpus_snapshot_id
parent_doc_id
chunk_index
content_hash
chunking_config_hash
```

展示形式为 `CH-<full_sha256>`；完整 digest 是身份，短前缀只能展示。切分配置变化会改变 chunk ID 和
语料的 `chunking_config_hash`，继而改变 S6-T4 collection fingerprint。新增复杂 Chunker 只实现
相同 Protocol，因此 Retriever、ContextBuilder 和 Evaluator 的主协议不变。

## 6. Evidence 与 Citation 双层 ID

### 6.1 Evidence UID

Evidence UID 跨运行、报告和实验稳定追溯，canonical 输入为：

```text
evidence_schema_version
corpus_snapshot_id
chunk_id
content_hash
```

展示形式 `EV-<full_sha256>`。正文或 Chunking 变化必须改变 UID；绝对路径、时间、随机值、环境信息和
任何评估标签不得参与。短前缀不能作为唯一键。

### 6.2 Citation ID 与绑定

Citation ID 只在一个 `RetrievedContextPackage` 内有效，按最终进入 Context 的 Evidence 顺序确定性
分配为 `E1`、`E2`、`E3`，显示为 `[E1]`。`CitationBinding` 保存：`citation_id`、
`evidence_uid`、`chunk_id`、`parent_doc_id`、`content_hash`、`source_id`、`version`、`rank`。

Evidence UID 解决跨运行归因，Citation ID 解决当前回答可读引用，二者不能互相替代。未来 Citation
Accuracy、引用支持度、幻觉溯源和污染证据归因都必须通过该绑定回到稳定 Evidence UID。

## 7. Retrieval 对象与不变量

### 7.1 RetrievalRequest

字段：`request_id`、`query_id`、`retrieval_query`、`retrieval_query_hash`、`top_k`、
`collection_fingerprint`、`query_embedding_spec_hash`、`retrieval_config_hash`。

不变量：`top_k > 0`；query hash 与原始值一致；请求内部可短暂持有查询文本，但普通序列化、repr、
异常和日志只暴露 hash；不得包含 expected answer、attack goal、poison label、Ground Truth 或
failure type。`query_embedding_spec_hash` 包含 query prefix，collection fingerprint 仍只包含
document-scope embedding hash。

### 7.2 RetrievalEvidence

字段：`evidence_uid`、`doc_id`、`chunk_id`、`parent_doc_id`、`content_ref`、`content_hash`、
`source_id`、`source_type`、`version`、`timestamp`、`rank`、`distance`、`similarity`、
`collection_fingerprint`、`retrieval_request_id`、只读 `public_metadata`。

它是一次召回结果的可追溯描述，默认且在普通序列化中都不含正文。rank 从 1 开始；distance 和
similarity 必须有限；collection/request 身份必须与本次请求一致；metadata 继续使用公开白名单。

### 7.3 RetrievalTrace

字段：`trace_id`、`request_id`、`query_id`、`retrieval_query_hash`、
`query_embedding_spec_hash`、`collection_fingerprint`、`top_k`、`candidate_count`、
`returned_count`、`evidence_summaries`、`retrieval_latency_ms`、`trace_schema_version`、
`trace_hash`。

summary 只含 Evidence UID、doc/chunk ID、rank、distance、similarity、content hash、source 和
version。Trace 证明“用什么索引和查询配置返回了哪些证据”，不能保存完整 Query、正文、Context 或
评估标签。`trace_hash` 覆盖稳定语义字段，排除 latency；否则同一运行无法确定性复现。

## 8. DenseRetriever 边界

`DenseRetriever` 只依赖 `EmbeddingProvider` 和 `VectorStore` Protocol：验证请求与 collection，调用
`embed_query`，执行向量查询，将 `VectorSearchHit` 转为 `RetrievalEvidence`，最后构造无正文 Trace。

排序固定为 similarity 降序、distance 升序、`doc_id` 升序；adapter 已排序时仍做领域层稳定化。空库
返回空 Evidence 和完整 Trace；`top_k` 大于数量时返回全部可用项；重复 chunk 按稳定 chunk ID 去重，
同父文档的不同 chunk 保留；非法/非有限 metric、维度不匹配、关闭的 store 和 fingerprint 不一致均
分类失败。异常只包含 request/collection/hash/维度和错误类别，不回显查询或正文。

Retriever 不解析 `content_ref`，不读取正文，不构建 Context，不判断 Trust，不访问 evaluator 标签。

## 9. ContentRef 与 ContentResolver

新规范 ContentRef 为：

```text
corpus:<corpus_snapshot_id>:<chunk_id>
```

它是 opaque、无本机路径的受控引用。`ContentResolver` Protocol 只接受 ContentRef 和预期
`content_hash`；`CorpusContentResolver` 只从获准的公开 corpus snapshot 解析正文，重新计算 SHA-256
并比较，不一致时抛出 `ContentHashMismatchError`。未知、越界或不可解析引用抛出
`ContentResolutionError`。错误不回显正文、文件路径或标签。

S6-T4 历史 fixture 使用 `chroma:<doc_id>`，其既有模型和测试保持不变。S6-T5 实现期由兼容解析器或
测试 adapter 显式接受该 legacy scheme，再映射到受控 fixture corpus；新生产对象只生成 `corpus:`
scheme。不得为了迁移修改 S6-T4 历史代码或把 Chroma 变成正文权威源。

Resolver 不得 import 或读取 `ground_truth/`、Evaluator、攻击标签和 oracle。

## 10. EvidenceEnvelope 与结构边界

`EvidenceEnvelope` 是受控内存对象，字段为：`citation_id`、`evidence_uid`、`doc_id`、`chunk_id`、
`parent_doc_id`、`source_id`、`source_type`、`version`、`timestamp`、`content_hash`、`rank`、
`distance`、`similarity`、`content`、只读 `public_metadata`。它允许持有正文，但不得直接写入普通日志、
Trace 或默认 dataclass/dict 审计序列化。

未来 Prompt block 采用确定性 XML-like 表示。属性和正文先做 XML escaping：`&` -> `&amp;`，`<` ->
`&lt;`，`>` -> `&gt;`，属性内 `"` -> `&quot;`、`'` -> `&apos;`。正文中的
`</EVIDENCE>`、`<EVIDENCE>`、`<SYSTEM>`、`<INSTRUCTION>` 因而不能改变 block 结构。

重要边界：XML-like escaping 只保护结构边界，不能单独阻止语义层 Prompt Injection，也不能被描述为
完整安全防护。

## 11. Citation Mode

`CitationMode` 冻结为：

- `off`：Evidence 仍有内部 ID，不向未来模型要求引用；
- `available`：说明证据带 `[E#]` 标记，模型可以引用；
- `required`：要求事实性陈述使用 `[E#]`，无支持证据时不得伪造引用。

S6-T5 不调用 LLM，但 ContextBuilder 必须为三种模式生成固定、可测试的 instruction。后续 Generator
必须真实传入该 instruction，Evaluator 必须真实实现 Citation Accuracy，不能让 Citation 永远停留在
占位字段。

## 12. ContextBuilder 与预算策略

输入先按 Retriever 的稳定 rank 和 Evidence UID 排序，再按 Evidence UID 去重；`max_evidence_count`
限制数量。Resolver 逐条解析并验证 hash，随后分配 Citation ID、构造 Envelope/Binding 和 escaped
block。Context hash 是最终 UTF-8 rendered context 的 SHA-256。

当前预算使用最大总字符数，未来通过 `TokenBudget` Protocol 增加 tokenizer-aware 预算。默认不截断
单条 Evidence：预算不足时只加入完整 block，放不下的后续 block 被整体丢弃并记录 reason code。若第
一条也放不下，则返回空 Context、`abstention_required=true` 和预算不足原因；空 Evidence 同样返回
空 Context并要求 abstention。未来若允许 chunk 内截断，必须产生新的 derived content hash 和
provenance，截断片段不得冒充完整 chunk。

预算计算包含 citation instruction、结构标签和正文转义后的真实长度。构建结果必须确定性；正文 hash
不一致立即阻断，不能跳过后继续生成看似成功的 Context。

## 13. RetrievedContextPackage

字段固定为：`package_id`、`request_id`、`query_id`、`citation_mode`、`evidence_envelopes`、
`citation_bindings`、`rendered_context`、`rendered_context_hash`、`evidence_count`、
`abstention_required`、`abstention_reason_codes`、`context_schema_version`。

普通有证据基线默认 `abstention_required=false`、reason codes 为空；空召回、预算无法容纳证据或明确
构建失败时必须要求 abstention。`package_id` 由 request、Context hash、citation mode、schema version
和 Evidence UID 序列确定性产生。

它只叫 `RetrievedContextPackage`，因为内容尚未经过可信分析。后续边界为：

```text
RetrievedContextPackage
  -> EvidenceSignal
  -> TrustAggregator
  -> RetrievalPolicy
  -> TrustedContextPackage
```

`TrustedContextPackage` 本轮不得实现。Stage 7 未来只能消费 `TrustedContextPackage +
RAGSecurityEnvelope`，不得直接消费 Retrieved Context。

## 14. 权限、日志与序列化

正文权限仅存在于 Chunker 的受控输入、Resolver 的受控返回、EvidenceEnvelope 内存和
RetrievedContextPackage 的受控运行时字段。普通日志只允许 ID、hash、rank、有限 metric、source、
version、数量、时延和异常类型。

禁止普通日志、Trace、默认审计 serialization 和异常保存完整 Query、正文、rendered context、API
Key、本机绝对路径或评估标签。测试必须递归扫描 `repr()`、dataclass serialization、`dict()`、nested
mapping、异常对象、Trace 和日志 payload。受控 package 若需要落盘必须使用显式敏感 artifact policy，
不复用普通 logger。

## 15. Ground Truth 与标签隔离

`ChunkRecord` public view、`VectorDocument`、`VectorSearchHit`、`RetrievalRequest`、
`RetrievalEvidence`、`RetrievalTrace`、Envelope metadata、CitationBinding、Retrieved Context、
rendered context 和 prompt instruction 均不得出现：

```text
poisoned, poison_label, label, attack_id, attack_goal, attack_category,
expected_answer, expected_behavior, failure_type, ground_truth, oracle,
risk_goal, stealth_level
```

污染正文可以在无防护基线中进入受控 Context，以研究传播；“该正文是污染样本”的标签绝不能进入运行时
链路。Resolver 不读 Ground Truth，ContextBuilder 不 import Evaluator 或 GroundTruthVault。

## 16. 异常模型

未来实现使用领域异常，不透传底层杂乱异常：`RetrievalConfigurationError`、
`RetrievalRuntimeError`、`RetrievalMetricError`、`RetrievalDimensionError`、
`ContentResolutionError`、`ContentHashMismatchError`、`ContextBudgetError`、
`ContextConstructionError`。异常允许包含脱敏 ID、hash、期望/实际维度和错误类别，禁止 Query、正文、
Context、标签、密钥和本机路径。

## 17. 测试策略

计划中的单元测试布局：

```text
tests/domains/retrieval/
  chunking/test_chunking_config.py
  chunking/test_identity_chunker.py
  chunking/test_chunk_id_stability.py
  retrieval/test_retrieval_request.py
  retrieval/test_evidence_uid.py
  retrieval/test_retrieval_evidence.py
  retrieval/test_retrieval_trace.py
  retrieval/test_dense_retriever.py
  context/test_content_resolver.py
  context/test_content_hash_verification.py
  context/test_evidence_envelope.py
  context/test_prompt_escaping.py
  context/test_citation_binding.py
  context/test_citation_modes.py
  context/test_context_budget.py
  context/test_retrieved_context_package.py
tests/integration/retrieval/
  test_static_retrieval_context_pipeline.py
  test_real_retrieval_context_pipeline.py
```

每个实施子任务严格先红后绿。快速测试只用 Static Provider、InMemory Store 和 fixture corpus，不联网。
真实 MiniLM + 临时 Chroma 测试继续由显式环境变量开启，不作为快速 CI 强依赖。

验收矩阵至少覆盖：UID/Chunk ID 稳定性与变化性、Citation 顺序、Retriever 无正文、Trace 无 Query/正文、
hash mismatch 阻断、恶意标签转义、三种 Citation 模式、空结果、超大 top_k、同分排序、重复 chunk、
预算不足、Context hash、递归标签/序列化泄漏、真实 Chroma 重开、runtime ignore、namespace 兼容、
Stage 1–5 完整性和禁止依赖方向。

## 18. 与 S6-T4 的兼容

S6-T5 复用现有抽象，不修改 `EmbeddingModelSpec`、Provider、VectorStore、CollectionFingerprint 和
历史测试。查询完整 spec hash 进入 RetrievalRequest/未来 RunManifest，不改变只由文档向量决定的
collection fingerprint。`VectorSearchHit` 经 adapter 转成 Evidence，Chroma 原始对象不会向上传播。

`chroma:` fixture 兼容只在 Resolver adapter 边界完成；新规范和新语料使用 `corpus:` ContentRef。

## 19. Stage 6.1、6.2 与 Stage 7 扩展

Stage 6.1 在 Retrieved Evidence 上增量产生隐蔽污染检测 `EvidenceSignal`，不重写 Retriever。
Stage 6.2 通过 TrustAggregator、冲突感知策略、Citation 核验和拒答生成 Trusted Context，不重写
ContextBuilder 主协议。复杂 Chunker、BM25、Hybrid 与 reranker 均通过现有协议和新配置增量加入。

Stage 7 只能接收 Trusted Context 与脱敏安全审计 Envelope，不得直接 import VectorStore、Chroma、
Resolver 或 Ground Truth。

## 20. 能证明与不能证明

设计获批后可证明：S6-T5 已有唯一、可审查的对象契约、权限边界、确定性规则、测试矩阵和分阶段实施
计划；它能指导团队在不破坏 S6-T4 的前提下实现可追溯 Dense Retrieval。

本设计不能证明任何 Python 功能已实现，不能证明污染攻击成功率、检索质量、引用准确率、可信评分、
生产安全性或论文方法有效。即便未来基线实现通过，也只能表述为“在当前固定语料、配置和评测协议下”。

## 21. 面试与研究表达

面试时可讲：“我没有让 Retriever 直接返回正文，而是先生成稳定 Evidence 和无正文 Trace，再通过受控
ContentRef 解析、hash 校验、结构转义和 CitationBinding 构造 Retrieved Context。这样检索、正文权限、
可信判断和审计可以独立测试，污染传播也能追溯到具体证据。”

企业价值是最小权限、索引可重建和事故可追溯；论文价值是把召回、上下文进入、可信判断和生成影响分成
可消融的观测点。不能把 XML escaping 说成完整防注入，也不能把 Retrieved Context 称为 Trusted。

## 22. 审批结论

本文件只冻结设计。下一步是人工审查本规格及配套计划；未明确批准前，S6-T5.1 Python 实现、任何
Retriever/Resolver/ContextBuilder 代码和 S6-T5.2 以后任务均不得开始。
