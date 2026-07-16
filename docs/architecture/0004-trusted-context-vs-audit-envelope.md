# ADR 0004：TrustedContextPackage 与 RAGSecurityEnvelope 分离

## 状态

已接受，2026-07-16。

## 决策

`TrustedContextPackage` 与 `RAGSecurityEnvelope` 必须是两个不同对象。

| 对象 | 用途 | 可包含内容 | 禁止内容 |
| --- | --- | --- | --- |
| `TrustedContextPackage` | 运行时业务上下文，提供给 ContextBuilder、LLM 与 Stage 7 | 受限文本片段、evidence_id、citation、来源、信任摘要、策略决策、聚合置信度、拒答标记 | Ground Truth、完整污染语料、向量库内部对象、审计细节 |
| `RAGSecurityEnvelope` | 脱敏审计与跨阶段追溯 | doc_id、hash、evidence hash、failure types、metrics、policy version、run_id、provenance | 可用于直接生成的完整上下文、原始文档、Ground Truth |

## 原因

运行时对象需要最小可用证据，审计对象需要可追溯但不可泄露。若把两者合并，Agent 可能读到内部审计状态或敏感文本，审计日志也可能变成业务 Prompt 的隐性输入。

## Stage 7 协议

Stage 7 的正式 RAG 输入固定为：

```text
TrustedContextPackage + RAGSecurityEnvelope
```

Stage 7 不得直接读取 ChromaDB、Ground Truth、原始完整污染文档或 Retrieval Guard 内部状态。工具实验默认使用 intent-only、mock tool、sandbox 和无破坏性副作用。

## EvidenceSignal 扩展契约

未来 `EvidenceSignal` 至少具备：

```text
signal_id, signal_type, signal_scope, subject_ids, score, confidence,
polarity, features, method_version, evidence_hash, reason_codes, available_at
```

`signal_scope` 为 document、candidate、evidence_set、query、context、generation；`polarity` 为 trust、risk、neutral；`available_at` 为 pre_retrieval、post_retrieval、pre_generation、post_generation。

`generation_influence_signal` 只允许由 Evaluator 在生成后计算，不得反馈影响同一次检索决策。
