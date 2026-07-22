# S6-T5.3 Provider-Neutral DenseRetriever 完成记录

- 日期：`2026-07-22`
- 状态：`Completed, pending human acceptance`
- 前置修复：`2ad3d9c feat(vectorstore): carry parent document identity in retrieval metadata`
- 当前实现：`feat(retrieval): add provider-neutral dense retriever`

## 实现范围

实现链路为 `RetrievalRequest -> EmbeddingProvider -> VectorStore -> VectorSearchHit[] -> RetrievalEvidence[] -> RetrievalTrace`。DenseRetriever 仅接受 public metadata schema `1.1` collection，校验 request 的 collection fingerprint、query embedding spec hash、retrieval config hash、provider/store 维度和 collection 状态。

它从 `hit.metadata["parent_doc_id"]` 读取真实父文档身份；不会回退到 chunk ID、source ID 或默认值，不读取语料、ContentResolver、Evaluator 或 GroundTruthVault。Evidence 使用 canonical `corpus:` content reference，Evidence/Trace/audit 不包含 query 正文或文档正文。

## 安全与确定性行为

- 排序：similarity 降序、distance 升序、doc ID 升序；
- 去重：按 chunk ID 去重，同父文档的不同 chunk 保留；
- fail closed：缺少 parent identity、schema 不匹配、request/store provenance 不匹配、重复 chunk provenance 冲突均失败；
- 兼容：schema `1.0` collection 保持可复现，但 DenseRetriever 明确拒绝使用它；schema `1.1` 由 P1 的统一 VectorStore validation 保障。

## 验证与边界

离线 TDD 覆盖 parent identity 从 ChunkRecord 经 VectorDocument、VectorStore 到 Evidence 的一致性，以及排序、去重、三类 request provenance mismatch、legacy schema 拒绝、metadata 缺失/冲突 fail-closed 和无 query/plaintext audit。新增 DenseRetriever/adapter 测试只使用 fake Chroma hit，不创建项目 `runtime/` 目录；但最终全量回归包含既有 S6-T4 Chroma 临时目录持久化测试，因而会初始化临时 Chroma client。该既有回归不是本轮实验运行，也不产生项目 runtime、模型调用或 RAG 指标。未调用真实模型、Groq 或 LLM，未修改 Stage 1–5 或 Stage 6 fixture 数据，未执行正式 RAG 安全实验。

本记录证明工程合同在当前离线测试配置下成立，不证明检索质量、安全效果、RAG 指标或生产可用性。下一步仅等待人工验收；`S6-T5.4 ContentResolver` 尚未批准。

## S6-T5.3-H1：Trace 语义与失败边界加固（2026-07-22）

- 状态：`Completed, pending human review`。
- 性质：人工验收发现项修复，不是新功能，不是正式实验，不改变 S6-T5.3 的人工验收状态。

修复前，`candidate_count` 错误使用 collection 总行数。现已冻结为 `VectorStore.query()` 返回的原始
`VectorSearchHit` 数量，在 metadata 校验、排序和领域去重之前统计；`returned_count` 始终等于最终
`RetrievalEvidence` 数量。例如 collection 为 100 行、`top_k=3`、raw hits 为 3、去重后 evidence 为 2 时，
trace 必须记录 `candidate_count=3`、`returned_count=2`，不再记录 100。

`_validate_store_state()` 现逐项校验 fingerprint、dimension、distance metric、vector schema 和 public
metadata schema。collection name 仅是 fingerprint 的派生展示值，不承担独立安全身份。Embedding provider、
store state 和 store query 的已知或未知底层异常均使用 `raise ... from error` 映射为固定、脱敏的 Retrieval
领域错误；对外错误不回显 query、正文、metadata 原值、ContentRef、路径、标签或 Ground Truth。

新增离线 TDD 覆盖空 collection、`top_k` 大于可用记录、collection 总量大于 `top_k`、重复 raw hit、同父文档
不同 chunk、closed store、错误向量维度、五类 store provenance mismatch、非 tuple/非 hit 输出、敏感底层异常、
连续 evidence rank 及 latency 无关的 trace hash。全部仅使用 Static provider、InMemory store 或 fake store；
未读取 fixture 正文、未调用真实 Embedding、Chroma、Groq 或 LLM，未执行 R1–R6 或正式 RAG 安全实验。

验证记录：新增测试先运行得到 `10 failed, 8 passed`，失败集中在错误的 collection count、未拆分 provenance
error code 和未映射外部异常，符合预期 Red 阶段。实施后，DenseRetriever 定向测试为 `18 passed`；完整 Stage 6
离线组合回归为 `233 passed, 2381 subtests passed`，无 skipped。Ruff、scoped MyPy、标签隔离、秘密形态、
绝对路径、Markdown 链接、保护路径、runtime Git-ignore 与 diff 检查见本轮最终验证记录。
