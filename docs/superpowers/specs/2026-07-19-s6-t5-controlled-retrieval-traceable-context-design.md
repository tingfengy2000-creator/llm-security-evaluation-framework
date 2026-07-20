# S6-T5 受控检索与可追溯上下文构建设计规格

> 英文名：Controlled Retrieval and Traceable Context Construction
>
> 状态：Design Hardening completed, pending second human review
>
> 实现状态：Not started
>
> 审批门：本规格和配套实施计划经人工批准后，才可开始 S6-T5.1。

> 2026-07-20 实施状态更新：S6-T5.1 已在单独人工批准下完成，待人工验收；本规格的 S6-T5.2
> 及之后任务仍未获批准。

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
Dataset QueryRecord
  -> explicit safe projection
  -> RetrieverQueryRecord (RuntimeQueryView)
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

本轮 Design Hardening 更不得创建任何 Python 业务对象或空壳。本规格中的类名和文件名均是经审批后实施
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

### 4.1 唯一稳定契约归属

`src/llmguard/domains/retrieval/contracts/` 是跨层稳定 DTO、value object、schema、canonical hash 与
公共安全序列化契约的唯一归属。`chunking/` 只实现 Chunker Protocol/具体 Chunker，`retrieval/` 只实现
DenseRetriever、排序、转换和运行时 orchestration，`context/` 只实现 ContentResolver、Renderer、Citation
分配和 ContextBuilder。上述实现目录不得重复定义稳定对象。

稳定对象统一为：`ChunkRecord`、`RetrieverQueryRecord`、`RetrievalRequest`、`RetrievalEvidence`、
`RetrievalTrace`、`EvidenceEnvelope`、`CitationBinding`、`RetrievedContextPackage`。它们在获批实现时均
由 `contracts/` 定义并导出；实现层只能 import 和组合它们。

### 4.2 Existing Contract Migration Matrix

| 对象 | 当前位置与字段 | S6-T5 新需求 | canonical 最终位置 | 兼容/迁移与保护测试 |
| --- | --- | --- | --- | --- |
| `DocumentRecord` | `contracts.models`；文档、来源、版本、正文 hash | 无字段迁移 | `contracts/` | 原地保留；现有 contracts/schema 测试继续保护 |
| `QueryRecord` | `contracts.models`；含 `attack_id`、`generation_question`、`expected_clean_doc_ids` | 只能作为 Dataset/Evaluator 原始记录 | `contracts/` | 原地保留；不得传给 Retriever；投影测试保护 |
| `RetrieverQueryRecord` | `attacks.attack_matrix`；`query_id`、`retrieval_query`、`generation_question`、`metadata` | 最小 runtime view：`query_id`、`retrieval_query`、`public_metadata` | `contracts/` | 实现期原地迁移定义；`attacks` 旧 import re-export canonical 类型；历史 public-record 形状由显式 loader adapter 读取并丢弃 generation 字段，测试保护 import identity 与隔离 |
| `ChunkRecord` | 尚未存在 | chunk/parent/index/hash/ref/config/public metadata | `contracts/` | 新建一次；`chunking/` 不建 `models.py` DTO 副本；chunking 测试保护 |
| `RetrievalRequest` | 尚未存在 | request/hash/config/top-k | `contracts/` | 新建一次；Retriever 只接受该类型 |
| `RetrievalEvidence` | `contracts.models`；query/doc/rank/metric/source/hash/`chroma:` ref | Evidence UID、chunk/parent、request/collection、public metadata、双 scheme ContentRef | `contracts/` | 原地演进同一类型；保留旧 import 与 `to_audit_dict()` 语义；兼容 adapter 将 legacy evidence 归一到同一对象，禁止 `retrieval.models.RetrievalEvidence` |
| `RetrievalTrace` | 尚未存在 | 无正文 trace 与 trace hash | `contracts/` | 新建一次；Retriever 生产，Context 不重定义 |
| `EvidenceEnvelope` | 尚未存在 | 受控内存正文与安全审计视图 | `contracts/` | 新建一次；Context 只构造，不重定义 |
| `CitationBinding` | 尚未存在 | Citation 到稳定 Evidence 的映射 | `contracts/` | 新建一次；Context 只分配 |
| `RetrievedContextPackage` | 尚未存在 | 受控 Context、audit view、结构性 abstention | `contracts/` | 新建一次；ContextBuilder 只构造，不称 Trusted |

这里的 backward compatibility 指 import 与历史数据读取路径可继续工作，并不承诺继续允许把
`generation_question` 或 evaluator 字段带入新的 runtime DTO。任何旧 shape 的兼容都必须在明确 adapter
处发生，不能污染 canonical runtime contract。

### 4.3 Query 的物理安全投影

`Dataset QueryRecord` 是数据集/评估边界对象，`GroundTruthVault` 保存原始 QueryRecord 与 oracle。数据集
loader 或 orchestration 的 public-boundary adapter 负责调用明确的 **safe projection**，生成只含
`query_id`、`retrieval_query` 和只读 `public_metadata` 的 `RetrieverQueryRecord`。Retriever 只能接受
`RetrieverQueryRecord` 或由其产生的 `RetrievalRequest`，不得接受 Dataset QueryRecord。

`attack_id`、`expected_clean_doc_ids`、`generation_question`、`expected_answer`、`attack_goal`、
`failure_type`、`ground_truth`、`oracle`、`stealth_level` 都不得进入 runtime view；generation question
仅在后续单独的 generation boundary 获批后才可存在。投影测试必须证明这些字段无法进入
RetrievalRequest、RetrievalTrace、EvidenceEnvelope、RetrievedContextPackage、logger payload 或异常。

## 5. Chunking 契约

### 5.1 当前能力与扩展点

当前短文档基线固定为 `one document = one chunk`，获批实现时只提供 `IdentityChunker`。接口冻结为：

- `ChunkingStrategy`：`identity`，未来增加 `fixed_token`、`token_overlap`、`sentence`、`semantic`；
- `ChunkingConfig`：策略、schema version 以及该策略真正影响切分的参数；
- `Chunker` Protocol：输入公开文档，输出由 `contracts/` 定义的不可变 `ChunkRecord` 序列；
- `ChunkRecord`：`chunk_id`、`parent_doc_id`、`chunk_index`、`content`、`content_hash`、
  `content_ref`、`chunking_strategy`、`chunking_config_hash`、`source_id`、`source_type`、
  `version`、`timestamp`、只读 `public_metadata`；
- `IdentityChunker`：不修改正文，一个 `DocumentRecord` 确定地产生一个 chunk。

`ChunkRecord` 是跨 Chunker、Retriever、Context 和 Evaluator 使用的稳定 DTO，因此它属于 `contracts/`；
`chunking/` 只拥有协议、配置解释和具体算法，绝不定义第二个 ChunkRecord。

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

选择方案 A：Evidence UID 显式保留 `content_hash`，即使 `chunk_id` 已经绑定正文。这是有意的
evidence-content binding 冗余：当审计人员只看到 UID 输入时，仍能直接验证“当前 Evidence 指向哪一个
正文 hash”，而无需隐含依赖 Chunk ID 的生成细节。Evidence UID 在**同一个 immutable corpus snapshot 内**
跨运行稳定；corpus snapshot ID 变化时 UID 可以变化，不能宣传为跨任意数据版本的全局不变身份。

canonical 输入为：

```text
evidence_schema_version
corpus_snapshot_id
chunk_id
content_hash
```

展示形式 `EV-<full_sha256>`。正文或 Chunking 变化必须改变 UID；绝对路径、时间、随机值、环境信息和
任何评估标签不得参与。短前缀不能作为唯一键。Chunk、Evidence、Trace、Context 和 Package 的
canonical JSON/UTF-8/SHA-256 规则必须复用 `contracts/` 中唯一的公共 helper；本轮只冻结归属，
不得实现 helper 或允许各模块自行复制 hash 逻辑。

### 6.2 Citation ID 与绑定

Citation ID 只在一个 `RetrievedContextPackage` 内有效，按最终进入 Context 的 Evidence 顺序确定性
分配为 `E1`、`E2`、`E3`，显示为 `[E1]`。`CitationBinding` 保存：`citation_id`、
`evidence_uid`、`chunk_id`、`parent_doc_id`、`content_hash`、`source_id`、`version`、`rank`。

Evidence UID 解决跨运行归因，Citation ID 解决当前回答可读引用，二者不能互相替代。未来 Citation
Accuracy、引用支持度、幻觉溯源和污染证据归因都必须通过该绑定回到稳定 Evidence UID。

## 7. Retrieval 对象与不变量

本节所有对象均由 `contracts/` 定义和导出；`retrieval/` 不得建立 `models.py` 复制它们。Retriever 的
运行时输入先是安全投影 `RetrieverQueryRecord`，再确定性构造 Request。

### 7.1 RetrievalRequest

字段：`request_id`、`query_id`、`retrieval_query`、`retrieval_query_hash`、`top_k`、
`collection_fingerprint`、`query_embedding_spec_hash`、`retrieval_config_hash`。

不变量：`top_k > 0`；query hash 与原始值一致；请求内部可短暂持有查询文本，但普通序列化、repr、
异常和日志只暴露 hash；它只能从 `RetrieverQueryRecord` 构造，不得包含或重新接收 Dataset QueryRecord
中的 attack/expected/generation/oracle 字段。`query_embedding_spec_hash` 包含 query prefix，collection
fingerprint 仍只包含 document-scope embedding hash。

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

ContentRef 是 `contracts/` 中唯一的 canonical value object/validation contract；VectorStore、Evidence 和
Resolver 都委托它验证，不能分别保留相互漂移的正则或 scheme 判断。新规范 ContentRef 为：

```text
corpus:<corpus_snapshot_id>:<chunk_id>
```

它是 opaque、无本机路径的受控引用。兼容迁移顺序固定为：

1. S6-T5.2 在 `contracts/` 建立唯一 ContentRef validation contract；
2. 实现期同时接受 canonical `corpus:` 与 legacy `chroma:`；
3. 新 S6-T5 producer 只生成 `corpus:`；旧 S6-T4 fixture 继续生成 `chroma:`；
4. `RetrievalEvidence` 在其**同一个既有 contract**的原地演进中开始接受两种 scheme；
5. S6-T5.4 的 Resolver 按 scheme 显式分派；legacy `chroma:` 只能映射受控 fixture corpus，绝不能
   从 Chroma 读取正文；
6. 未知 scheme、绝对路径、超长或含正文的 reference 立即失败。

`ContentResolver` Protocol 只接受已验证 ContentRef 和预期 `content_hash`；`CorpusContentResolver` 只从
获准公开 corpus snapshot 解析正文，重新计算 SHA-256 并比较。hash 不一致抛出完整性异常，未知、越界或
不可解析引用抛出明确异常；错误不回显正文、文件路径或标签。回滚时保留旧 `chroma:` validator/fixture
acceptance 测试，撤回新 `corpus:` producer 与 Resolver adapter 即可，不破坏 S6-T4 历史测试。

Resolver 不得 import 或读取 `ground_truth/`、Evaluator、攻击标签和 oracle。

## 10. EvidenceEnvelope 与结构边界

`EvidenceEnvelope` 是 `contracts/` 定义的受控内存对象，字段为：`citation_id`、`evidence_uid`、`doc_id`、`chunk_id`、
`parent_doc_id`、`source_id`、`source_type`、`version`、`timestamp`、`content_hash`、`rank`、
`distance`、`similarity`、`content`、只读 `public_metadata`。它允许持有正文，`content` 必须使用
`repr=False`，默认 `__repr__` 不显示正文；但这不使对象自动“可安全序列化”。

必须严格区分三种表示：

| 表示 | 用途 | 内容规则 |
| --- | --- | --- |
| Runtime sensitive object | 受控内存中的构建与渲染 | 可含 `content`，不交给普通 logger |
| Safe audit representation | `to_audit_dict()` 的唯一普通审计 API | 不含 `content`、完整 Query 或 rendered context，只含 UID、CitationBinding 摘要、hash、rank、source、版本和数量 |
| Explicit sensitive artifact representation | 受控、显式批准的敏感工件导出 | 仅经 sensitive artifact policy、访问控制和脱敏/保留策略执行 |

`dataclasses.asdict(EvidenceEnvelope)` 被定义为**敏感操作**，不是安全审计 API；禁止普通 logger、Trace、
exception payload 或 nested package audit view 调用 `asdict()` 后记录。不得错误宣称 `asdict()` 天然不含
正文。`RetrievedContextPackage` 同样必须有 repr-safe 与 `to_audit_dict()`；其 audit view 不含
`rendered_context`、嵌套正文或完整 Query。完整 Package/Envelope 的持久化只能通过显式 sensitive artifact
policy，不能复用普通日志。

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

顺序固定且不可重排：先按稳定 rank/Evidence UID 排序，再按 Evidence UID 去重，再应用
`max_evidence_count`，再解析正文并验证 hash，再分配 Citation ID，最后渲染 citation instruction 和
完整 Evidence block。预算使用最终 escaped rendered string 的 **Unicode code point** 数量，不使用平台
字节数；最终 Context hash 始终使用 rendered string 的 UTF-8 bytes。渲染换行固定为 `LF`，禁止平台默认
换行影响 Context hash。

当前预算使用最大总字符数，未来通过 `TokenBudget` Protocol 增加 tokenizer-aware 预算。默认不截断
单条 Evidence：超过预算的完整 block 被排除并记录结构性 reason code；若没有完整 block 能放入，返回
空 Context、`abstention_required=true`。未来若允许 chunk 内截断，必须产生新的 derived content hash 和
provenance，截断片段不得冒充完整 chunk。

## 13. RetrievedContextPackage

字段固定为：`package_id`、`request_id`、`query_id`、`citation_mode`、`evidence_envelopes`、
`citation_bindings`、`rendered_context`、`rendered_context_hash`、`evidence_count`、
`abstention_required`、`abstention_reason_codes`、`context_schema_version`。

普通有证据基线默认 `abstention_required=false`、reason codes 为空；只有结构性“无可用 Context”情况可
返回 Package 且要求 abstention：`EMPTY_RETRIEVAL`、`NO_EVIDENCE_AFTER_DEDUPLICATION`、
`CONTEXT_BUDGET_EXHAUSTED`、`NO_COMPLETE_EVIDENCE_BLOCK_FITS`。`package_id` 由 request、Context hash、citation mode、schema version
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
version、数量、时延和异常类型；它必须调用 `to_audit_dict()` 而不是 `asdict()`。

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

结构性 abstention 与完整性/安全异常严格区分。前者只表示没有可用 Context，并且仅使用上一节列出的四个
reason code；它不代表 Trust 判断。Trust-based abstention 属于 Stage 6.2。

以下情况必须抛出异常，且**不得**返回 Package：`CONTENT_HASH_MISMATCH`、`UNKNOWN_CONTENT_REF`、
`INVALID_CONTENT_REF_SCHEME`、`COLLECTION_FINGERPRINT_MISMATCH`、`REQUEST_EVIDENCE_MISMATCH`、
`INVALID_METRIC`、`CORPUS_SNAPSHOT_INTEGRITY_FAILURE`、`UNEXPECTED_CONTEXT_CONSTRUCTION_FAILURE`。
它们分别映射到未来的领域异常类别，不透传底层实现异常。异常允许包含脱敏 ID、hash、期望/实际维度和
错误类别，禁止 Query、正文、Context、标签、密钥和本机路径。

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

验收矩阵至少覆盖：安全投影不携带 `attack_id`/`expected_clean_doc_ids`/generation 字段；唯一 contract
import identity；UID/Chunk ID 稳定性与变化性；canonical ContentRef 双 scheme 迁移；Citation 顺序；
Retriever 无正文；Trace 无 Query/正文；hash mismatch 阻断；恶意标签转义；三种 Citation 模式；空结果、
超大 top_k、同分排序、重复 chunk、预算不足；Context hash；`repr()`、`to_audit_dict()`、logger、exception、
nested package audit view 不泄漏敏感内容；`asdict()` 仅在显式敏感操作测试中出现；真实 Chroma 重开、runtime
ignore、namespace 兼容、Stage 1–5 完整性和禁止依赖方向。

## 18. 与 S6-T4 的兼容

S6-T5 复用现有抽象，不修改 `EmbeddingModelSpec`、Provider、VectorStore、CollectionFingerprint 和
历史测试。查询完整 spec hash 进入 RetrievalRequest/未来 RunManifest，不改变只由文档向量决定的
collection fingerprint。`VectorSearchHit` 经 adapter 转成 Evidence，Chroma 原始对象不会向上传播。

`chroma:` fixture 兼容由 `contracts/` 唯一 ContentRef validator 识别，并在 Resolver adapter 边界显式
映射；新规范和新语料只生成 `corpus:` ContentRef。该迁移允许对既有 VectorStore 的 validation 做最小
委托式兼容演进，但不得改变 S6-T4 的 fixture 行为、collection 语义或历史测试。

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

本文件只冻结 hardened design。下一步是第二次人工审查本规格、迁移矩阵及配套计划；未明确批准前，
S6-T5.1 implementation、任何 Retriever/Resolver/ContextBuilder 代码和 S6-T5.2 以后任务均不得开始。

## 23. S6-T5.1 实施落点与持续边界

S6-T5.1 已以最小实现落实以下冻结约束：`ChunkingStrategy`、`ChunkingConfig`、`ChunkRecord`、
`canonical_json_sha256` 和 `format_corpus_content_ref` 归属 `contracts/`；`Chunker` Protocol、
`ChunkingError` 与 `IdentityChunker` 归属 `chunking/`。没有创建 `chunking/models.py`，也没有修改既有
`RetrievalEvidence` validation。

`identity` 是唯一已经存在的算法：其配置只哈希 strategy、schema_version 与
implementation_version，拒绝 token/sentence/semantic 参数；future enum/config 仅表达并严格验证
未来语义，不能被误认为已有算法。`corpus:` formatter 仅生成最小新 scheme，尚不承担 legacy `chroma:`
迁移或 ContentResolver 解析职责；这两项仍属于 S6-T5.2 以后。

### 23.1 S6-T5.1 Hardening Freeze

`window_size` 不再属于 `ChunkingConfig`：它没有合法策略语义，保留会形成无效稳定 API。fixed token
唯一使用 `max_tokens`，token overlap 唯一使用 `max_tokens + overlap_tokens`。ChunkRecord 使用
`chunk_schema_version`，当前由 `config.schema_version` 显式传入，避免无意义的第二版本来源；它在构造时
重新调用唯一 `derive_chunk_id()`，不接受只满足正则格式但与字段不一致的 ID。

稳定 Chunking 异常在 `contracts/errors.py` 定义，行为层只 re-export。异常消息只使用固定、脱敏的描述；
hash mismatch 可通过 `error_code` 识别，不回显正文、原始 doc ID、路径或 metadata。
