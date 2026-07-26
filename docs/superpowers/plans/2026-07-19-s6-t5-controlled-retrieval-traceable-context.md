# S6-T5 受控检索与可追溯上下文构建实施计划

> 状态：Design Hardening completed, pending second human review
>
> 业务实现：Not started
>
> 执行规则：每个子任务单独批准、测试先行、独立提交；不得自动连续执行。

> 2026-07-20 状态更新：仅 S6-T5.1 已获单独批准、实施完成并等待人工验收；S6-T5.2–S6-T5.8 仍未批准。

## 1. 计划目标

本计划将 S6-T5 拆成八个可独立审查和回滚的任务，把 S6-T4 的 Embedding/VectorStore 基础设施扩展为：

```text
Identity Chunking -> Dense Retrieval -> traceable Evidence
-> controlled Content Resolution -> Citation-aware Context
-> RetrievedContextPackage
```

本计划不批准任何实现。开始每个任务前都必须重新核对分支、HEAD、干净工作树、上游同步、审批范围和
Stage 1–5/Stage 6 数据完整性。

## 2. 全局实施纪律

1. 新业务代码只进入 `src/llmguard/domains/retrieval/`，不得进入 legacy `src/codeguarder/`。
2. 严格 TDD：先提交或至少保存可复现红灯，再写最小实现使其变绿。
3. 快速测试不得联网；真实 MiniLM/Chroma 只在 S6-T5.7 的显式开关下运行。
4. 不记录完整 Query、正文、Context、标签、密钥或本机绝对路径。
5. 每个任务完成后运行定向测试、架构/namespace/label-isolation、Ruff、MyPy 和 diff 检查。
6. 不实现 BM25、Hybrid、Rewrite、Reranker、Trust、LLM、Evaluator、T10–T15 或正式实验。
7. 任一任务若需要改变已冻结协议，先回到设计评审，不在实现中偷偷扩大范围。
8. 跨层稳定 DTO、value object、hash 与安全 serialization 只在 `contracts/` 定义；`chunking/`、
   `retrieval/`、`context/` 只消费它们，禁止重复 `models.py`。

### 实施前迁移顺序

S6-T5.1 先把 `ChunkRecord` 规划到 `contracts/`；S6-T5.2 再完成 Existing Contract Migration Matrix 中的
`RetrieverQueryRecord` safe projection、RetrievalRequest/Trace、ContentRef 和 RetrievalEvidence 原地演进。
其中旧 `attacks.RetrieverQueryRecord` import 必须 re-export 新 canonical 类型；历史 public record 的
`generation_question` 只能由 loader adapter 消费并丢弃，不能进入 runtime DTO。不得在 retrieval/models.py
建立第二个 RetrievalEvidence。

## 3. S6-T5.1 Chunking Contracts

**先写失败测试**

- `tests/domains/retrieval/chunking/test_chunking_config.py`
- `tests/domains/retrieval/chunking/test_identity_chunker.py`
- `tests/domains/retrieval/chunking/test_chunk_id_stability.py`
- `tests/architecture/test_contract_ownership.py`（或扩展既有 architecture test）
- 覆盖 canonical config hash、tokenizer/revision/overlap 参数、相同输入稳定、正文/配置变化改 ID、标签和
  路径不进入公开对象。

**新增文件**

- `src/llmguard/domains/retrieval/chunking/__init__.py`
- `src/llmguard/domains/retrieval/chunking/base.py`
- `src/llmguard/domains/retrieval/chunking/identity_chunker.py`

**修改文件**

- `src/llmguard/domains/retrieval/contracts/models.py`：只在此原地加入 `ChunkRecord`；
- `src/llmguard/domains/retrieval/contracts/__init__.py`：公开稳定 DTO；
- 必要的 architecture ownership test。

**不允许修改**

- S6-T4 embedding/vectorstore 实现、Stage 6 数据、旧 namespace；不得在 chunking 建立稳定 DTO 或实现
  复杂 Chunker 空壳。

**验收标准**

- IdentityChunker 一文档一 chunk；ID/hash 跨进程稳定；`ChunkRecord` 只存在于 contracts；metadata 只读
  且无标签；未来策略只存在枚举和配置契约，不存在伪实现。

**建议提交**：`feat(retrieval): add deterministic identity chunking contracts`

**回滚边界**：只回滚上述 chunking 新文件、导出和对应测试，不触碰 S6-T4。

**后续审批门**：人工验收 S6-T5.1 后，才可批准 S6-T5.2。

## 4. S6-T5.2 Retrieval Contracts and IDs

**先写失败测试**

- `tests/domains/retrieval/retrieval/test_retrieval_request.py`
- `tests/domains/retrieval/retrieval/test_evidence_uid.py`
- `tests/domains/retrieval/retrieval/test_retrieval_evidence.py`
- `tests/domains/retrieval/retrieval/test_retrieval_trace.py`
- `tests/domains/retrieval/retrieval/test_runtime_query_projection.py`
- `tests/domains/retrieval/retrieval/test_content_ref_compatibility.py`
- `tests/domains/retrieval/retrieval/test_safe_audit_contracts.py`
- 覆盖 Existing Contract Migration Matrix、攻击/expected/generation 字段无法投影到 runtime、Evidence UID
  snapshot 内稳定/跨 snapshot 可变、请求 hash、metric 有限、Trace 无 Query/正文、双 scheme ContentRef、
  `to_audit_dict()` 和 repr-safe 行为。

**新增文件**

- `src/llmguard/domains/retrieval/retrieval/__init__.py`
- `src/llmguard/domains/retrieval/retrieval/errors.py`

**修改文件**

- `src/llmguard/domains/retrieval/contracts/models.py`：原地演进现有 `RetrievalEvidence`，新增
  `RetrieverQueryRecord`、`RetrievalRequest`、`RetrievalTrace`；
- `src/llmguard/domains/retrieval/contracts/identifiers.py`：唯一 canonical hash helper；
- `src/llmguard/domains/retrieval/contracts/content_ref.py`：唯一 `corpus:`/legacy `chroma:` validation；
- `src/llmguard/domains/retrieval/contracts/projections.py`：唯一 safe projection；
- `src/llmguard/domains/retrieval/contracts/__init__.py`、既有 attacks re-export/loader adapter、必要的
  VectorStore 委托式 validation 和兼容测试。

**不允许修改**

- 不创建 `retrieval/models.py` 或第二个 RetrievalEvidence；不创建 DenseRetriever、Resolver、Envelope 或
  ContextBuilder；不把正文放入 Evidence/Trace；不允许 Dataset QueryRecord 进入 Retriever。

**验收标准**

- Request/Evidence/Trace 不变量明确且只在 contracts 定义；旧 imports 保持可用；safe projection 物理剥离
  `attack_id`、`expected_clean_doc_ids` 和 generation 字段；新 producer 只生成 `corpus:`，legacy fixture
  继续接受 `chroma:`；Evidence UID 使用完整 digest，Trace hash 排除时延；禁止字段递归扫描通过。

**建议提交**：`feat(contracts): migrate retrieval runtime contracts and references`

**回滚边界**：只回滚 contracts 演进、attacks re-export/loader adapter 与对应测试；保持旧 `chroma:` fixture
validator 可用，不能回滚成第二套 DTO。

**后续审批门**：人工确认对象序列化和标签隔离后，才可批准 S6-T5.3。

## 5. S6-T5.3 Dense Retriever

**先写失败测试**

- `tests/domains/retrieval/retrieval/test_dense_retriever.py`
- 使用 Static Provider + InMemory Store 覆盖稳定排序、同分 doc ID、空库、超大 top_k、重复 chunk、
  同父文档不同 chunk、非法 metric、维度错误、关闭 store、fingerprint 不一致和异常脱敏。

**新增文件**

- `src/llmguard/domains/retrieval/retrieval/dense_retriever.py`
- 必要时增加 `src/llmguard/domains/retrieval/retrieval/protocols.py`。

**修改文件**

- retrieval 导出；必要的架构依赖测试。

**不允许修改**

- 不依赖具体 SentenceTransformer/Chroma；不读取正文；不构建 Context；不做 Rewrite、BM25、Hybrid、
  rerank、Trust 或 generation。

**验收标准**

- `RetrievalRequest -> Evidence[] + Trace` 全程 provider/store neutral；输出无正文；排序和错误确定性；
  query 只在受控调用内存在。

**建议提交**：`feat(retrieval): add provider-neutral dense retriever`

**回滚边界**：只回滚 DenseRetriever、导出、架构约束和该任务测试。

**后续审批门**：人工验收检索结果和 Trace 后，才可批准 S6-T5.4。

## 6. S6-T5.4 ContentResolver

**先写失败测试**

- `tests/domains/retrieval/context/test_content_resolver.py`
- `tests/domains/retrieval/context/test_content_hash_verification.py`
- 覆盖已在 S6-T5.2 验证的 ContentRef scheme 显式分派、未知 snapshot/chunk、hash mismatch 立即阻断、
  legacy `chroma:` fixture adapter、无 Ground Truth 访问及异常无正文/路径。

**新增文件**

- `src/llmguard/domains/retrieval/context/__init__.py`
- `src/llmguard/domains/retrieval/context/resolver.py`
- `src/llmguard/domains/retrieval/context/errors.py`

**修改文件**

- 仅公开 corpus loader 的受控读取接口或 fixture adapter；Resolver 必须消费 S6-T5.2 的 contracts
  ContentRef，不能重写 validation；如需改变既有 loader，必须先单独审查。

**不允许修改**

- 不把 Chroma 当正文权威源；不读 evaluator/ground truth；不修改 S6-T4 `chroma:` fixture 历史行为。

**验收标准**

- Resolver 只从获准 snapshot 取正文并校验 hash；`chroma:` 只映射 fixture corpus 而不读 Chroma；hash
  mismatch/unknown scheme 必须抛出完整性异常、不得返回 Package；普通日志无正文。

**建议提交**：`feat(retrieval): add controlled corpus content resolver`

**回滚边界**：只回滚 context resolver、受控 loader adapter 和对应测试。

**后续审批门**：人工验收正文权限与兼容迁移后，才可批准 S6-T5.5。

## 7. S6-T5.5 EvidenceEnvelope and Citation

**先写失败测试**

- `tests/domains/retrieval/context/test_evidence_envelope.py`
- `tests/domains/retrieval/context/test_prompt_escaping.py`
- `tests/domains/retrieval/context/test_citation_binding.py`
- `tests/domains/retrieval/context/test_citation_modes.py`
- `tests/domains/retrieval/context/test_sensitive_serialization.py`
- 覆盖双层 ID、最终顺序分配、三种 instruction、五类 XML 字符和伪造 closing/opening tag、`repr=False`、
  repr-safe、`to_audit_dict()`、logger/exception payload、显式 sensitive artifact export，以及 `asdict()`
  被识别为敏感操作而不是安全 API。

**新增文件**

- `src/llmguard/domains/retrieval/context/citation.py`
- `src/llmguard/domains/retrieval/context/rendering.py`

**修改文件**

- `src/llmguard/domains/retrieval/contracts/models.py`：只在此加入 `EvidenceEnvelope`、`CitationBinding` 与
  审计/敏感 artifact contract；context 导出和日志/serialization 架构测试。

**不允许修改**

- 不创建 context models DTO 副本或 ContextBuilder；不把 escaping 宣称为语义防注入；不计算 Citation
  Accuracy；不调用 LLM。

**验收标准**

- Envelope 仅受控内存持有正文；Binding 可回到 Evidence UID；默认 repr/audit 不含正文；完整导出只能
  经 explicit sensitive artifact policy；escaping 保证结构不能被正文闭合；三种 Citation instruction 确定性。

**建议提交**：`feat(context): add evidence envelope and citation contracts`

**回滚边界**：只回滚 Envelope/Citation/rendering、导出和对应测试。

**后续审批门**：人工验收结构边界和 Citation 语义后，才可批准 S6-T5.6。

## 8. S6-T5.6 ContextBuilder

**先写失败测试**

- `tests/domains/retrieval/context/test_context_budget.py`
- `tests/domains/retrieval/context/test_retrieved_context_package.py`
- 补充 Citation/escaping 测试，覆盖排序、去重、数量/字符预算、空结果、首条放不下、整 block 丢弃、
  hash mismatch、Context/package hash、Unicode code point 预算、UTF-8 hash、LF 换行、Package
  repr/audit/sensitive artifact 边界，以及结构性 abstention 与完整性异常的分流。

**新增文件**

- `src/llmguard/domains/retrieval/context/budget.py`
- `src/llmguard/domains/retrieval/context/builder.py`

**修改文件**

- `src/llmguard/domains/retrieval/contracts/models.py`：只在此加入 `RetrievedContextPackage` 与安全审计
  representation；context 导出和依赖方向测试。

**不允许修改**

- 不截断单条 Evidence；不在 context 建立 Package DTO 副本；不创建 TrustedContextPackage；不 import
  Chroma、具体 embedding、Evaluator、Trust 或 LLM。

**验收标准**

- 相同 Evidence/config 生成相同 Citation、rendered Context、UTF-8 hash 和 package；顺序固定为排序、
  UID 去重、数量限制、Resolver/hash、Citation、render；预算基于 escaped rendered string 的 Unicode
  code point，换行固定 LF，且只保留完整 block；仅 EMPTY_RETRIEVAL、NO_EVIDENCE_AFTER_DEDUPLICATION、
  CONTEXT_BUDGET_EXHAUSTED、NO_COMPLETE_EVIDENCE_BLOCK_FITS 返回结构性 abstention；hash/scheme/fingerprint/
  metric/request 不一致必须异常且不返回 Package；普通审计不泄漏正文或 rendered context。

**建议提交**：`feat(context): build deterministic retrieved context packages`

**回滚边界**：只回滚 budget/builder/package、导出和对应测试。

**后续审批门**：人工验收完整静态链路后，才可批准 S6-T5.7。

## 9. S6-T5.7 Integration and Security Validation

**先写失败测试**

- `tests/integration/retrieval/test_static_retrieval_context_pipeline.py`
- `tests/integration/retrieval/test_real_retrieval_context_pipeline.py`
- 扩展 architecture/no-label-leakage/namespace/secret/runtime tests，先证明缺失的全链路、重开和泄漏检查
  会失败；补充安全投影、contract ownership、ContentRef 双 scheme、safe audit serialization、异常不返回
  Package 与 LF/UTF-8 budget 的集成验证。

**新增文件**

- 只新增上述集成和必要治理测试；原则上不新增业务模块。

**修改文件**

- 修复集成暴露的 S6-T5 实现缺陷；每次修复保持最小范围。

**不允许修改**

- 不调用 Groq；不创建项目正式 runtime；不实现 Trust/LLM/Evaluator；不通过修改 Stage 1–5 或历史 hash
  消除 CRLF/LF 假阳性。

**验收标准**

- Static 全链路快速稳定；显式真实 MiniLM + 临时 Chroma 可关闭重开并构建 Context；Query 的攻击/expected
  字段不会传播；labels、正文、rendered context、路径、secret、namespace 和 Git-ignore 检查通过；临时文件清理。

**建议提交**：`test(retrieval): validate controlled retrieval context pipeline`

**回滚边界**：按失败来源回滚对应集成测试或最小修复，不跨到其他 Stage。

**后续审批门**：人工确认验收证据后，才可批准 S6-T5.8 文档收尾。

## 10. S6-T5.8 Documentation and Acceptance

**先写失败测试**

- 扩展 `tests/architecture/test_context_persistence.py` 或等价治理测试，验证状态、唯一文档、审批门、
  Stage README、学习记录和禁止夸大边界；不新增无意义业务测试。

**新增文件**

- 经批准的独立 S6-T5 验收报告/脱敏证据索引；如无真实实验，不创建虚假结果文件。

**修改文件**

- `PROJECT_MASTER_CONTEXT.md`
- `docs/governance/current_work_state.md`
- `stages/stage6_rag_security/README.md`
- `deliverables/learning_notes.md`
- 必要的架构索引与面试材料。

**不允许修改**

- 不把单元/集成测试写成生产防护率；不宣称 Trust、Citation Accuracy、RAG 指标或攻击矩阵完成；不
  自动开始下一 Task。

**验收标准**

- 文档与 Git 事实一致；Existing Contract Migration Matrix、第二次审批门与未实现边界可追溯；测试、Ruff、
  MyPy、secret/absolute path/runtime/history/data 检查有脱敏证据；commit 已推送，分支同步、工作树干净。

**建议提交**：`docs(retrieval): record s6-t5 acceptance and learning evidence`

**回滚边界**：只回滚 S6-T5 验收文档和治理状态，不删除已经接受的实现提交。

**后续审批门**：人工决定进入后续 Stage 6 Trust baseline 设计还是先补技术债；不得自动进入。

## 11. 总体验收矩阵

全部八个任务完成后才可宣称 S6-T5 实现完成。至少验证：

- Chunk ID/Evidence UID 跨运行稳定，语义输入变化时改变；
- Citation ID 按最终 Context 顺序分配；
- Retriever 和 Trace 都不返回/保存正文；
- ContentResolver hash mismatch 阻断；
- 恶意 XML-like 标签无法突破结构边界；
- Citation `off/available/required` 输出确定；
- 空库、超大 top_k、同分、重复 chunk 和预算不足行为明确；
- Context hash 稳定，标签与敏感文本不进入 repr/log/exception/trace；
- Dataset QueryRecord 只能经 safe projection 进入 runtime；
- stable DTO 只由 `contracts/` 定义，旧 import 通过显式 re-export 兼容；
- `corpus:` 与 legacy `chroma:` 在唯一 ContentRef contract 中校验，未知 scheme 失败；
- `asdict()` 不被当成安全 API，Envelope/Package 只有 `to_audit_dict()` 可进入普通审计；
- 结构性 abstention 与完整性异常不会混淆；
- 真实 MiniLM + 临时 Chroma 重开路径在显式开关下通过；
- ContextBuilder 不依赖 Chroma，Retriever 不依赖具体 embedding provider；
- ContentResolver 不访问 Ground Truth；旧 namespace、Stage 1–5、Stage 6 数据与 runtime Git 治理不变。

## 12. 当前停止点

本计划已完成 Design Hardening，但没有批准 S6-T5.1。第二次人工审查并明确回复批准前，不得新增本计划
列出的任何 Python 业务文件，不得把 Design Hardening 状态改成 Implementation in progress。

## 13. S6-T5.1 实施留痕（2026-07-20）

本节是对当前人工批准任务的实际状态补充，不改变后续审批门。已先运行第 3 节列出的四个新测试文件
Red 阶段，再新增 `contracts/hashing.py`、`contracts/chunking.py`、
`chunking/{__init__,base,errors,identity_chunker}.py`，并导出稳定契约。Green 阶段覆盖一文一块、
UTF-8 hash 完整性、稳定 ID、config hash、metadata 深冻结、标签/绝对路径拒绝与 contracts ownership；
没有触及本计划后续的 Retriever/Context/Trust 工作。S6-T5.2 仍须单独人工批准。

### 13.1 S6-T5.1 Hardening 实施留痕（2026-07-20）

人工审查后新增验收测试并先运行 Red：初始失败原因为 contracts 尚未导出统一
`ChunkingConfigurationError`。修复后，`window_size` 被删除、异常稳定归属迁至 contracts、ChunkRecord
增加 schema version 和对象级 ID 校验、metadata 改为先验证 key 类型再排序。该加固不新增任何
Retriever、Evidence、Trace、Resolver、Citation、Context 或 Trust 代码。最终状态为
`Completed, pending final human acceptance`，S6-T5.2 仍未批准。

## 14. S6-T5.3 审批状态说明（2026-07-21）

本节是对项目负责人最新人工审批的追加说明，不改写上文的历史审批快照。GOV-ER1、GOV-ER1-H1 与 S6-T5.2 已获 `HUMAN_ACCEPTED`；`S6-T5.3 DenseRetriever` 已获 `APPROVED_TO_START`，仅允许 Provider-Neutral、离线、无正文的工程实现与验证。`S6-T5.4 ContentResolver` 及后续任务、真实模型/Chroma 运行和正式 RAG 安全实验仍未获批准。

## 15. S6-T5.3 协议 blocker 说明（2026-07-21）

启动前的实现层核查确认：`VectorSearchHit` 只返回 `doc_id`、metric、rank 与白名单 metadata，而 canonical `RetrievalEvidence` 强制要求真实 `parent_doc_id`。当前白名单未包含该字段，且 S6-T5.3 禁止读取语料、伪造身份或修改冻结 contracts。任务因此进入 `DESIGN_OR_PROTOCOL_BLOCKER`：不创建 DenseRetriever、不写不安全测试替身，也不以临时 adapter 绕过边界；恢复实现必须先获得人工批准的 identity 信息载体与对应 contract 变更。

## 16. S6-T5.3-P1 与 DenseRetriever 实施留痕（2026-07-22）

项目负责人批准了公开、非标签、无正文的 `parent_doc_id` carrier。`2ad3d9c` 保留 schema `1.0`，新增 schema `1.1` retrieval-ready metadata 与统一 validation；schema 版本进入 collection fingerprint，避免旧 collection 被原地升级。随后 DenseRetriever 以 TDD 实现 `RetrievalRequest -> EmbeddingProvider -> VectorStore -> VectorSearchHit -> RetrievalEvidence -> RetrievalTrace`，仅接受 schema `1.1`，按 similarity、distance、doc ID 稳定排序，按 chunk 去重，冲突 provenance 或缺失 parent identity fail closed。新增 DenseRetriever/adapter 测试不启动项目 runtime 或真实 Chroma；完整回归中保留的既有 S6-T4 临时 Chroma 测试仅验证历史 adapter，不构成新实验。它不读取正文、不会访问标签或 GroundTruth、不调用真实模型或 LLM。S6-T5.3 当前为 `Completed, pending human acceptance`；S6-T5.4 仍未批准。

## 17. S6-T5.4-P1 协议冻结实施记录（2026-07-25）

本子任务名称为 `Content Resolution Contract and Permission Boundary Freeze`。它只完成文档、治理与静态
协议回归测试：不修改 `src/`、不创建 ContentResolver、不创建 `ResolvedContent` 实现、不读 corpus 正文、不修改
fixture 数据，不调用模型、Embedding、Chroma、Groq 或 LLM。

冻结输入是项目负责人的四项决定：唯一 `ContentResolver.resolve(content_ref: ContentRef,
expected_content_hash: str) -> ResolvedContent` 接口；contracts 唯一拥有的正文能力 DTO；
`CorpusSnapshotReader` / `ApprovedCorpusSnapshotRegistry` 最小读取面；以及
`LegacyContentRefAdapter` 的 `exact-match allowlist` 与 `mapping_hash`。错误统一归 `contracts/errors.py`，
`context/errors.py` 未来仅可 re-export。

本轮的 TDD 仅指向“设计记录是否完整、状态是否未越权”的治理测试，不是 ContentResolver 业务 Red 测试。
P1 完成后的任务状态应写为 `Completed, pending human acceptance`；父任务 S6-T5.4 仍保持
`APPROVED_TO_START / DESIGN_OR_PROTOCOL_BLOCKER`，不得因为设计冻结就宣称 blocker 已正式解决。只有 P1
人工验收后，才可另行批准最小实现与业务 TDD；`S6-T5.5` 及后续任务仍为 Not approved。

## 18. S6-T5.4-P1 人工验收状态附注（2026-07-25）

项目负责人已接受 P1 设计冻结，blocker 状态为 `RESOLVED_BY_APPROVED_PROTOCOL_FREEZE`，父任务状态为
`READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`。本计划仍不自动授权实现：下一步必须是单独审批的
`S6-T5.4-I1`，当前状态 `NOT YET APPROVED`；不得开始 ContentResolver TDD、读取正文或进入 S6-T5.5。

## 19. S6-T5.4-I1 最小实现状态附注（2026-07-25）

历史快照之后，项目负责人单独批准 I1。`ContentRef + expected_content_hash -> CorpusContentResolver ->
ApprovedCorpusSnapshotRegistry -> CorpusSnapshotReader -> ResolvedContent` 已以 TDD 完成，当前为
`Completed, pending human acceptance`。测试只使用合成内存正文和 mapping，未读取 Stage 6 fixture，未调用
Embedding、Chroma、Groq 或 LLM。S6-T5.5 仍为 `NOT APPROVED`，正式 RAG 安全实验仍为 `NOT STARTED`。

## 20. S6-T5.4 最终人工验收状态附注（2026-07-25）

项目负责人已接受 P1、I1、H1 和 S6-T5.4；当前均为 `HUMAN_ACCEPTED`。该事实追加在历史 pending 快照之后，
不改写历史。后续 S6-T5.5、S6-T5.6 及以后任务仍为 `NOT APPROVED`，不自动开始 EvidenceEnvelope、Citation、
ContextBuilder 或正式 RAG 安全实验。

## 21. S6-T5.5-P1 协议审查执行记录（2026-07-25）

本轮 `S6-T5.5-P1 EvidenceEnvelope and Citation Boundary Freeze` 只修改设计、ADR、治理材料和静态治理测试。
它不执行第 7 节列出的 TDD/源码任务；这些任务只在未来父任务 `S6-T5.5` 得到单独实现批准后才可开始。

冻结决定采用 Citation 时序方案 A：Envelope 没有 `citation_id`；future ContextBuilder 在最终 Evidence 集、预算选择
完成后，按最终顺序创建 Binding 并分配 package-local 的连续 `E1 ... En`。不接受 `None`、空字符串或 `E0` 作为普通
业务可误用的未绑定 Citation。唯一未来工厂为 `EvidenceEnvelopeFactory.create(evidence, resolved_content)`；DTO 和错误
归属 contracts，context 只能实现行为。`文档`、label、Ground Truth、Query、rendered block 不得进入普通审计、repr、
logger 或异常。

本轮同时冻结 exact LF instruction、XML-like template、单次 escaping、render-only CRLF/CR 到 LF 归一与不进行
Unicode normalization；escaping 只保护结构边界，并不构成语义防注入。敏感 artifact export 延期且默认关闭。详情见
`docs/governance/s6_t5_5_protocol_review_record.md`。执行状态为 `Completed, pending human acceptance`；S6-T5.5、
S6-T5.6+ 和正式 RAG 安全实验仍未批准。

## 22. S6-T5.5-P1-H1 协议加固执行记录（2026-07-26）

人工审查指出 Factory 的 legacy 表述会模糊 Resolver 与 Envelope 的责任。本 H1 仅补充设计和治理测试：Factory 只接受
canonical `corpus:` RetrievalEvidence，并验证 ContentRef equality、snapshot、chunk 与 hash；legacy `chroma:` 只在
ContentResolver 输入通过 exact-match adapter 映射，不得进入 Factory。未来 renderer 的唯一输入冻结为
`Envelope + Binding`，它必须逐项验证七项 Binding/Evidence identity，并以 `CITATION_BINDING_MISMATCH` fail closed。

Citation allocation 与 Binding 创建仍是 S6-T5.6 ContextBuilder 的运行期职责；H1 不实现 DTO、factory、renderer、
Binding 或 ContextBuilder。H1 状态为 `Completed, pending human review`；P1 仍为 `Completed, pending human
acceptance`，`S6-T5.5`、`S6-T5.6+` 和正式 RAG 安全实验未获批准。

## 23. GOV-S6-T5.5-P1-ACCEPTANCE：协议人工验收执行记录（2026-07-26）

项目负责人已将 P1 与 P1-H1 设为 `HUMAN_ACCEPTED`。这是对本计划第 7 节未来实现前置协议的人工接受，
不是第 7 节 TDD/源码任务的启动许可。`S6-T5.5` 现为 `READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`，
但 `S6-T5.5-I1` 仍为 `NOT YET APPROVED`；S6-T5.6+、ContextBuilder、Citation Accuracy、Trust、LLM 和正式
RAG 安全实验保持未批准/未开始。最后接受的 stage implementation commit 仍为 `11a72f7`，`25fb83d` 仅是协议加固提交。
