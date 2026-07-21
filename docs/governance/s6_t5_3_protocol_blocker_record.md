# S6-T5.3 DenseRetriever 协议 blocker 记录

- 日期：`2026-07-21`
- 任务：`S6-T5.3 Provider-Neutral DenseRetriever`
- 状态：`DESIGN_OR_PROTOCOL_BLOCKER`
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

## 恢复条件

项目负责人需先批准一个公开、非标签、无正文的 parent-document identity carrier，并明确其 schema owner、VectorStore metadata 白名单、已有 collection 的兼容策略和回归测试。批准后，S6-T5.3 从 TDD Red 阶段恢复；`S6-T5.4 ContentResolver` 仍需独立批准。
