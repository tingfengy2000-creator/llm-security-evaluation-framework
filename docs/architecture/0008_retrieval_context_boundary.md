# ADR 0008：受控检索与可追溯上下文边界

## 状态

S6-T5 Design Hardening 已完成，2026-07-19；等待第二次人工审查。Python 实现未开始。

## 背景

S6-T4 只提供向量化和向量存储。如果 Retriever 直接返回正文、ContextBuilder 直接读取 Chroma，或在
Trust 计算前把结果命名为 Trusted Context，就会把检索正确性、正文权限、安全策略和审计混成一个无法
消融的组件。本 ADR 固定 S6-T5 的层间边界。

硬化后的起始边界是：

```text
Dataset QueryRecord -> safe projection -> RetrieverQueryRecord -> RetrievalRequest
                                           |
GroundTruthVault keeps raw record/oracle     +-> DenseRetriever -> Evidence/Trace
```

这里的 **safe projection** 是 Dataset/Public loader 或 orchestration boundary 的显式责任；Retriever 不得
接受含 `attack_id`、`expected_clean_doc_ids` 或 `generation_question` 的 Dataset QueryRecord。

## 决策

### 1. Retriever 不返回正文

Retriever 只返回带稳定身份、来源、rank、distance、similarity、content hash 和 opaque reference 的
`RetrievalEvidence`，另生成不含 Query/正文的 `RetrievalTrace`。这样普通检索日志可审计而不会自动
复制敏感语料，Retriever 也无法越权构造 Prompt。

`RetrieverQueryRecord`、`RetrievalRequest`、`RetrievalEvidence` 和 `RetrievalTrace` 是 `contracts/` 中的
唯一稳定 DTO；`retrieval/` 只实现 orchestration，不能建立第二个 `RetrievalEvidence` 或 `models.py`
副本。现有 attacks 层的 `RetrieverQueryRecord` import 在迁移时必须 re-export canonical 类型，历史数据
shape 仅由显式 loader adapter 兼容。

### 2. 正文通过 ContentRef 受控解析

新规范引用为 `corpus:<corpus_snapshot_id>:<chunk_id>`。ContentRef 必须是 `contracts/` 中唯一的 value
object/validation contract，统一接受 canonical `corpus:` 和 legacy `chroma:`，拒绝未知 scheme、正文和
绝对路径。新 S6-T5 producer 只生成 `corpus:`；S6-T4 fixture 继续使用 `chroma:`。Resolver 根据已验证
scheme 显式分派，legacy scheme 仅映射受控 fixture corpus，不读取 Chroma 正文。

`ContentResolver` 在受控 corpus snapshot 中解析正文并核对 content hash；hash 不一致立即阻断。兼容
validation 只能存在这一个 canonical 位置；必要时 VectorStore 只做委托式调用，不能再复制正则。

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

`EvidenceEnvelope` 与 `RetrievedContextPackage` 是 runtime sensitive object。完整正文或 rendered context
不进入默认 repr；普通审计只能调用 `to_audit_dict()`。`dataclasses.asdict()` 是敏感操作，不能被当作
安全 API；完整对象导出必须经过显式 sensitive artifact policy。异常和 logger payload 同样只能使用
安全 audit representation。

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

### 11. 结构性 abstention 不等于完整性异常

`EMPTY_RETRIEVAL`、`NO_EVIDENCE_AFTER_DEDUPLICATION`、`CONTEXT_BUDGET_EXHAUSTED` 与
`NO_COMPLETE_EVIDENCE_BLOCK_FITS` 表示正常但无可用 Context，可返回 `RetrievedContextPackage` 且令
`abstention_required=true`。这不是 Trust 判断。

`CONTENT_HASH_MISMATCH`、`UNKNOWN_CONTENT_REF`、`INVALID_CONTENT_REF_SCHEME`、
`COLLECTION_FINGERPRINT_MISMATCH`、`REQUEST_EVIDENCE_MISMATCH`、`INVALID_METRIC`、
`CORPUS_SNAPSHOT_INTEGRITY_FAILURE`、`UNEXPECTED_CONTEXT_CONSTRUCTION_FAILURE` 是数据完整性、配置或
安全边界错误，必须抛出脱敏异常且不得返回 Package。Trust-based abstention 仅属于 Stage 6.2。

### 12. Context 预算是跨平台确定性协议

ContextBuilder 的顺序固定为排序、Evidence UID 去重、数量限制、Resolver/hash 验证、Citation 分配和
渲染。预算使用最终 escaped string 的 Unicode code point 数量，Context hash 使用最终 UTF-8 bytes，
换行固定为 LF。预算不足时只排除完整 Evidence block；不允许把截断片段冒充完整证据。

## 哈希与配置边界

Chunk、Evidence、Trace、Context 和 Package 身份都使用 `contracts/` 唯一 helper 的 canonical JSON UTF-8
+ SHA-256，排除路径、用户名、时间、随机数和 Ground Truth。Evidence UID 选择显式重复 `content_hash`
作为 evidence-content binding；它只承诺在同一 immutable corpus snapshot 内跨运行稳定，snapshot 变化时
允许变化。短 digest 仅展示，完整 digest 才是身份。文档向量配置继续由 S6-T4 的
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

## S6-T5.4-P1：正文解析权限协议冻结

`S6-T5.4-P1` 冻结而不实现 Content Resolution Contract and Permission Boundary。正文解析从检索证据中分离：
唯一 `ContentResolver` 只接收 `content_ref: ContentRef` 与 `expected_content_hash: str`，并返回
`ResolvedContent`。`ResolvedContent` 必须由 `src/llmguard/domains/retrieval/contracts/` 唯一拥有，正文为
短生命周期、进程内正文权限对象，普通日志、trace、repr、异常与默认序列化不得传播正文。

Resolver 将来只从 `ApprovedCorpusSnapshotRegistry` 取得 `CorpusSnapshotReader`，后者只允许按 chunk ID
读取正文；不提供 corpus 枚举、路径、metadata、标签或 Ground Truth。legacy `chroma:` 只能由
`LegacyContentRefAdapter` 的 immutable `exact-match allowlist` 映射为 canonical `corpus:` ref，使用稳定
`mapping_hash`；不根据 doc_id/source_id/文件名/路径推导，不允许任何 fallback，不访问 Chroma。

错误类型由 `contracts/errors.py` 唯一拥有：`ContentResolutionLookupError`、
`ContentResolutionIntegrityError` 与 `ContentResolutionRuntimeError` 分别描述查找、完整性和运行期失败。
P1 不创建源码、读取正文或实现 reader/registry/adapter；父任务 S6-T5.4 仍是
`APPROVED_TO_START / DESIGN_OR_PROTOCOL_BLOCKER`，直到人工验收与独立实现批准。

### S6-T5.4-P1 人工验收状态附注（2026-07-25）

本 ADR 中的 P1 协议边界已经 `HUMAN_ACCEPTED`，并解决了 S6-T5.4 的 protocol blocker
(`RESOLVED_BY_APPROVED_PROTOCOL_FREEZE`)。该决定不改变“协议与实现分离”的架构原则：父任务只进入
`READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`，`S6-T5.4-I1` 仍为 `NOT YET APPROVED`。

### S6-T5.4-I1 实现状态附注（2026-07-25）

项目负责人随后单独批准 I1；当前最小实现已完成，状态为 `Completed, pending human acceptance`。它以合成内存
reader/registry 验证 `ContentRef`、精确 legacy allowlist 和 UTF-8 SHA-256，而非读取既有语料或调用任何向量库。
`ResolvedContent` 仍只由 `contracts/` 拥有，`context/` 不能创建第二个 DTO。该实现不授权 S6-T5.5、ContextBuilder、
Citation 或正式 RAG 安全实验。

### S6-T5.4 最终人工验收状态附注（2026-07-25）

P1、I1、H1 与父任务当前均为 `HUMAN_ACCEPTED`。这只接受受控正文解析的合成内存工程边界：contracts 唯一 DTO、
最小 resolve capability、UTF-8 hash、exact-match legacy 迁移和注入错误脱敏；不接受或实现真实 provider、
ContextBuilder、Citation、Trust、S6-T5.5 或正式 RAG 安全实验。

### S6-T5.5-P1/P1-H1 人工验收附注（2026-07-26）

P1 与 H1 已 `HUMAN_ACCEPTED`，但此 ADR 的 Factory、Binding、renderer 和 ContextBuilder 仍是未来实现契约，
不是已存在的业务对象。验收仅将 `S6-T5.5` 推进为 `READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`；
`S6-T5.5-I1` 仍为 `NOT YET APPROVED`，不得把设计提交 `25fb83d` 当作业务实现提交。

### S6-T5.5-I1 实现状态附注（2026-07-26）

I1 已获单独批准并完成最小实现：DTO 与错误只在 `contracts/`，Factory/instruction/renderer 只在 `context/` 行为层。
Factory 不接收 legacy/裸正文，renderer 不创建 Binding 或分配编号，且 ContextBuilder 仍不存在。此状态为
`Completed, pending human acceptance`，不改变 S6-T5.6 的 `NOT APPROVED` 审批门。

## S6-T5.5-P1：EvidenceEnvelope 与 Citation 边界冻结

为消除“Citation ID 按最终 Context 顺序分配”与“Envelope 位于 ContextBuilder 之前”的矛盾，本 ADR 冻结
`EvidenceEnvelope` 为无 `citation_id` 的敏感运行时对象。`CitationBinding` 是 package-local 映射，只有未来
S6-T5.6 ContextBuilder 在最终 Evidence 集确定后才创建和分配连续 `E1 ... En`。这避免被去重或预算排除的 Evidence
持有错误的引用编号，也不使用 `None`、空字符串或 `E0` 这类可被误认作有效引用的状态。

稳定 DTO 与错误仍仅归 `contracts/`；未来 `EvidenceEnvelopeFactory.create(evidence, resolved_content)` 是唯一生产构造
行为，Context 不得复制 DTO 或以任意正文/metadata 直接拼装对象。Evidence 贡献 provenance、rank 与 metrics，
ResolvedContent 贡献经过 hash 验证的正文。敏感导出默认拒绝，除非未来有独立批准的 `SensitiveArtifactPolicy`。

未来 rendering 只允许一个 XML escaping API：对原始输入单次 escaping，正文 render-only 地把 CRLF/CR 归一为 LF，
不做 Unicode normalization；正文 hash 始终基于原始 UTF-8 bytes。该 escaping 只保护结构边界，不是 Prompt Injection
语义防护。P1 不实现 DTO、factory、Binding、renderer 或 ContextBuilder；完整冻结记录见
`docs/governance/s6_t5_5_protocol_review_record.md`，当前仅 `Completed, pending human acceptance`。

### S6-T5.5-P1-H1：Canonical Evidence 与 Binding Rendering 加固

Factory 位于 Resolver 之后，只消费 canonical `corpus:` RetrievalEvidence 与已验证 ResolvedContent；legacy `chroma:`
的 exact-match mapping 在 Resolver 输入边界结束，不能被 Factory 重新解释。Factory 必须同时验证 canonical ContentRef、
snapshot、chunk、hash，任何不一致为 `EVIDENCE_CONTENT_MISMATCH`。

renderer 只消费 `EvidenceEnvelope + CitationBinding`，不接收裸 citation ID、正文、metadata 或 dict，也不猜测编号或创建
Binding。它在渲染前逐项校验 UID、chunk、parent、hash、source、version、rank，不一致即以固定脱敏的
`CITATION_BINDING_MISMATCH` 失败。该错误是完整性失败而非 abstention，不能返回 partial block 或重编号。Binding 的创建
和 allocator 调用仍属于未来 S6-T5.6 ContextBuilder；本 H1 不创建源码，状态为 `Completed, pending human review`。

### GOV-S6-T5.5-ACCEPTANCE：实现人工验收附注（2026-07-26）

P1/P1-H1 已在此前通过协议人工验收；项目负责人现进一步将 I1、H1 和父任务 `S6-T5.5` 标记为
`HUMAN_ACCEPTED`。最终接受的 implementation commit 是 `6da27a6`，而 `2cacef7` 必须作为初始实现历史保留。
本附注 supersede 当前状态，不删除前文的 pending/review 历史快照。

验收只确认 synthetic objects 上的 contracts、Factory、不可变 metadata、timestamp、Evidence UID、Binding identity、
脱敏 validation errors、instruction 和单 block renderer。它不改变本 ADR 的核心分层：Envelope/Citation 不等于
ContextBuilder，不等于 RetrievedContextPackage，更不等于 Trust 或正式 RAG 安全效果。`S6-T5.6+` 仍为
`NOT APPROVED`，正式 RAG security experiment 仍为 `NOT STARTED`。

### S6-T5.6-P1：Context Package 协议审查（2026-07-26）

本 ADR 现补充未来 Package 级边界：S6-T5.6-P1 已完成、待人工验收，但只冻结协议。ContextBuilder 只接受
`RetrievalRequest + Sequence[RetrievalEvidence] + CitationMode + ContextBuildConfig`，并仅注入
ContentResolver 与 EvidenceEnvelopeFactory。RetrievalTrace 是审计工件，不作为 build 的第二个真相来源。

为解决 Citation/预算循环，未来实现只能以临时 `E{included_count + 1}` Binding 调用既有 single-block renderer
测试最终字符串。只有完整候选能够放入 Unicode code point 预算时才提交 Binding；第一个不适配候选会触发稳定前缀
停止，避免低 rank 优先级被较短后续 Evidence 反转。临时 Binding 不进入 Package、trace 或 audit，不消耗永久 ID。

未来 `RetrievedContextPackage` 与 `ContextBuildTrace` 仍由 `contracts/` 拥有；前者含敏感 rendered context，后者仅含
counts、UID 与排除原因。`EMPTY_RETRIEVAL`、instruction 超预算和无完整 block 可形成结构性 abstention；hash、
provenance 或 Binding 完整性错误仍必须 fail closed。S6-T5.6 implementation、S6-T5.7+ 与正式 RAG 实验未获批准。
