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

离线 TDD 覆盖 parent identity 从 ChunkRecord 经 VectorDocument、VectorStore 到 Evidence 的一致性，以及排序、去重、三类 request provenance mismatch、legacy schema 拒绝、metadata 缺失/冲突 fail-closed 和无 query/plaintext audit。未调用真实模型、Groq、LLM 或真实 Chroma runtime，未修改 Stage 1–5 或 Stage 6 fixture 数据，未执行正式 RAG 安全实验。

本记录证明工程合同在当前离线测试配置下成立，不证明检索质量、安全效果、RAG 指标或生产可用性。下一步仅等待人工验收；`S6-T5.4 ContentResolver` 尚未批准。
