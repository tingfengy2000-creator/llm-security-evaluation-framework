# S6-T5.3 DenseRetriever 协议 blocker 记录

- 日期：`2026-07-21`
- 任务：`S6-T5.3 Provider-Neutral DenseRetriever`
- 状态：`RESOLVED_BY_VERSIONED_PUBLIC_METADATA_CONTRACT`
- 任务审批：已获 `APPROVED_TO_START`；该审批不授权绕过冻结契约。

## 发现

目标链路要求将 `VectorSearchHit[]` 转换为 canonical `RetrievalEvidence[]`。现有 `VectorSearchHit` 只有 `doc_id`、`distance`、`similarity`、`metadata` 与 `rank`；其 metadata 白名单不包含 `parent_doc_id`。与此同时，`RetrievalEvidence` 把 `parent_doc_id` 设为必填公开身份字段，且要求 `doc_id == chunk_id`。

## 为什么必须停止

DenseRetriever 被明确禁止读取或解析语料、访问 ContentResolver、GroundTruthVault 或 Evaluator。它也不能把 `chunk_id` 伪造成 `parent_doc_id`，因为多个不同 chunk 可以属于同一父文档。直接扩充 VectorStore metadata 或修改 stable contracts 会改变冻结边界，必须先获得新的人工设计批准。

## TDD 留痕

本轮没有创建 `test_dense_retriever.py` 的 Red 测试：在 immutable contract 前提下，无法写出一个会转绿且不依赖伪造 parent identity 的有效行为规格。将错误的期望测试写出来再为它补不安全实现，不是合格 TDD。当前可复现证据是 contracts 对字段和白名单的静态核查；获批协议后必须从 Red 测试重新开始。

## 未做事项

- 未创建 `dense_retriever.py`、`protocols.py` 或第二套 DTO。
- 未创建不安全测试替身，未访问 Stage 6 fixture 数据，未读取正文。
- 未调用 Embedding、Chroma、Groq 或 LLM，未执行 R1–R6。

## 决策与修复

项目负责人已批准 `S6-T5.3-P1 Parent Document Identity Carrier`。schema owner 固定为 `vectorstore/models.py`：schema `1.0` 保持历史兼容，schema `1.1` 要求完整 retrieval provenance，并将 `parent_doc_id` 沿 `ChunkRecord -> VectorDocument.metadata -> VectorSearchHit.metadata -> RetrievalEvidence` 传递。adapter 只复用统一验证入口，不读取正文、不接触标签。

## 兼容与验证边界

`public_metadata_schema_version` 进入 CollectionFingerprint，因此 1.0 与 1.1 使用不同 collection，不原地升级或覆盖历史 collection。离线测试验证必填字段、路径/标签拒绝、InMemory 传递、Chroma stable-hit 转换及 fingerprint 隔离。该修复只解除 metadata protocol blocker；DenseRetriever 尚未完成，`S6-T5.4 ContentResolver` 仍需独立批准。

## 闭环结果

- 修复提交：`2ad3d9c feat(vectorstore): carry parent document identity in retrieval metadata`。
- 后续实现：`feat(retrieval): add provider-neutral dense retriever`。
- 验证：schema `1.0` 不变；schema `1.1` 缺少 provenance fail closed；同一 `parent_doc_id` 的不同 chunk 保留；相同 chunk 的冲突 provenance 立即失败；Evidence 的 `parent_doc_id` 直接取自 hit metadata。
- 结论边界：这是离线工程与契约验证，不是检索质量、安全效果或正式 RAG 实验。`S6-T5.4 ContentResolver` 仍未批准。
