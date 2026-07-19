# S6-T5 受控检索与可追溯上下文构建实施计划

> 状态：Design Freeze completed, pending human review
>
> 业务实现：Not started
>
> 执行规则：每个子任务单独批准、测试先行、独立提交；不得自动连续执行。

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

## 3. S6-T5.1 Chunking Contracts

**先写失败测试**

- `tests/domains/retrieval/chunking/test_chunking_config.py`
- `tests/domains/retrieval/chunking/test_identity_chunker.py`
- `tests/domains/retrieval/chunking/test_chunk_id_stability.py`
- 覆盖 canonical config hash、tokenizer/revision/overlap 参数、相同输入稳定、正文/配置变化改 ID、标签和
  路径不进入公开对象。

**新增文件**

- `src/llmguard/domains/retrieval/chunking/__init__.py`
- `src/llmguard/domains/retrieval/chunking/models.py`
- `src/llmguard/domains/retrieval/chunking/base.py`
- `src/llmguard/domains/retrieval/chunking/identity_chunker.py`

**修改文件**

- 仅必要的 `src/llmguard/domains/retrieval/__init__.py` 公开导出和架构测试。

**不允许修改**

- S6-T4 embedding/vectorstore 实现、Stage 6 数据、旧 namespace；不得实现复杂 Chunker 空壳。

**验收标准**

- IdentityChunker 一文档一 chunk；ID/hash 跨进程稳定；metadata 只读且无标签；未来策略只存在枚举和
  配置契约，不存在伪实现。

**建议提交**：`feat(retrieval): add deterministic identity chunking contracts`

**回滚边界**：只回滚上述 chunking 新文件、导出和对应测试，不触碰 S6-T4。

**后续审批门**：人工验收 S6-T5.1 后，才可批准 S6-T5.2。

## 4. S6-T5.2 Retrieval Contracts and IDs

**先写失败测试**

- `tests/domains/retrieval/retrieval/test_retrieval_request.py`
- `tests/domains/retrieval/retrieval/test_evidence_uid.py`
- `tests/domains/retrieval/retrieval/test_retrieval_evidence.py`
- `tests/domains/retrieval/retrieval/test_retrieval_trace.py`
- 覆盖 Evidence UID 稳定/变化、请求 hash、metric 有限、Trace 无 Query/正文、repr/dict/nested
  serialization 无标签。

**新增文件**

- `src/llmguard/domains/retrieval/retrieval/__init__.py`
- `src/llmguard/domains/retrieval/retrieval/models.py`
- `src/llmguard/domains/retrieval/retrieval/identifiers.py`
- `src/llmguard/domains/retrieval/retrieval/errors.py`

**修改文件**

- 仅必要的 canonical serialization 公共 helper 和公开导出；不得改 S6-T4 领域语义。

**不允许修改**

- 不创建 DenseRetriever、Resolver、Envelope 或 ContextBuilder；不把正文放入 Evidence/Trace。

**验收标准**

- Request/Evidence/Trace 不变量明确；Evidence UID 使用完整稳定 digest；Trace hash 排除时延；禁止字段
  递归扫描通过。

**建议提交**：`feat(retrieval): add evidence identity and trace contracts`

**回滚边界**：只回滚 retrieval contract、ID helper、导出和对应测试。

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
- 覆盖 canonical `corpus:` 引用、未知 snapshot/chunk、hash mismatch 立即阻断、legacy `chroma:` fixture
  adapter、无 Ground Truth 访问及异常无正文/路径。

**新增文件**

- `src/llmguard/domains/retrieval/context/__init__.py`
- `src/llmguard/domains/retrieval/context/content_ref.py`
- `src/llmguard/domains/retrieval/context/resolver.py`
- `src/llmguard/domains/retrieval/context/errors.py`

**修改文件**

- 仅公开 corpus loader 的受控读取接口或 fixture adapter；如需改变既有 loader，必须先单独审查。

**不允许修改**

- 不把 Chroma 当正文权威源；不读 evaluator/ground truth；不修改 S6-T4 `chroma:` fixture 历史行为。

**验收标准**

- Resolver 只从获准 snapshot 取正文并校验 hash；权限、scheme 和异常边界通过；普通日志无正文。

**建议提交**：`feat(retrieval): add controlled corpus content resolver`

**回滚边界**：只回滚 context resolver、受控 loader adapter 和对应测试。

**后续审批门**：人工验收正文权限与兼容迁移后，才可批准 S6-T5.5。

## 7. S6-T5.5 EvidenceEnvelope and Citation

**先写失败测试**

- `tests/domains/retrieval/context/test_evidence_envelope.py`
- `tests/domains/retrieval/context/test_prompt_escaping.py`
- `tests/domains/retrieval/context/test_citation_binding.py`
- `tests/domains/retrieval/context/test_citation_modes.py`
- 覆盖双层 ID、最终顺序分配、三种 instruction、五类 XML 字符和伪造 closing/opening tag、默认审计
  serialization 不含正文。

**新增文件**

- `src/llmguard/domains/retrieval/context/models.py`
- `src/llmguard/domains/retrieval/context/citation.py`
- `src/llmguard/domains/retrieval/context/rendering.py`

**修改文件**

- context 导出和日志/serialization 架构测试。

**不允许修改**

- 不创建 ContextBuilder；不把 escaping 宣称为语义防注入；不计算 Citation Accuracy；不调用 LLM。

**验收标准**

- Envelope 仅受控内存持有正文；Binding 可回到 Evidence UID；escaping 保证结构不能被正文闭合；三种
  Citation instruction 确定性。

**建议提交**：`feat(context): add evidence envelope and citation contracts`

**回滚边界**：只回滚 Envelope/Citation/rendering、导出和对应测试。

**后续审批门**：人工验收结构边界和 Citation 语义后，才可批准 S6-T5.6。

## 8. S6-T5.6 ContextBuilder

**先写失败测试**

- `tests/domains/retrieval/context/test_context_budget.py`
- `tests/domains/retrieval/context/test_retrieved_context_package.py`
- 补充 Citation/escaping 测试，覆盖排序、去重、数量/字符预算、空结果、首条放不下、整 block 丢弃、
  hash mismatch、Context/package hash、abstention 默认与原因码。

**新增文件**

- `src/llmguard/domains/retrieval/context/budget.py`
- `src/llmguard/domains/retrieval/context/builder.py`
- 必要时增加 `src/llmguard/domains/retrieval/context/package.py`。

**修改文件**

- context 导出和依赖方向测试。

**不允许修改**

- 不截断单条 Evidence；不创建 TrustedContextPackage；不 import Chroma、具体 embedding、Evaluator、
  Trust 或 LLM。

**验收标准**

- 相同 Evidence/config 生成相同 Citation、rendered Context、hash 和 package；预算只保留完整 block；
  空或无可容纳证据要求 abstention；普通日志不泄漏正文。

**建议提交**：`feat(context): build deterministic retrieved context packages`

**回滚边界**：只回滚 budget/builder/package、导出和对应测试。

**后续审批门**：人工验收完整静态链路后，才可批准 S6-T5.7。

## 9. S6-T5.7 Integration and Security Validation

**先写失败测试**

- `tests/integration/retrieval/test_static_retrieval_context_pipeline.py`
- `tests/integration/retrieval/test_real_retrieval_context_pipeline.py`
- 扩展 architecture/no-label-leakage/namespace/secret/runtime tests，先证明缺失的全链路、重开和泄漏检查
  会失败。

**新增文件**

- 只新增上述集成和必要治理测试；原则上不新增业务模块。

**修改文件**

- 修复集成暴露的 S6-T5 实现缺陷；每次修复保持最小范围。

**不允许修改**

- 不调用 Groq；不创建项目正式 runtime；不实现 Trust/LLM/Evaluator；不通过修改 Stage 1–5 或历史 hash
  消除 CRLF/LF 假阳性。

**验收标准**

- Static 全链路快速稳定；显式真实 MiniLM + 临时 Chroma 可关闭重开并构建 Context；标签、正文、路径、
  secret、namespace 和 Git-ignore 检查通过；临时文件清理。

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

- 文档与 Git 事实一致；测试、Ruff、MyPy、secret/absolute path/runtime/history/data 检查有脱敏证据；
  commit 已推送，分支同步、工作树干净。

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
- 真实 MiniLM + 临时 Chroma 重开路径在显式开关下通过；
- ContextBuilder 不依赖 Chroma，Retriever 不依赖具体 embedding provider；
- ContentResolver 不访问 Ground Truth；旧 namespace、Stage 1–5、Stage 6 数据与 runtime Git 治理不变。

## 12. 当前停止点

本计划已冻结实施顺序，但没有批准 S6-T5.1。人工审查并明确回复批准前，不得新增本计划列出的任何
Python 业务文件，不得把 Design Freeze 状态改成 Implementation in progress。
