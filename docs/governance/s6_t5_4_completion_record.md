# S6-T5.4-I1 完成记录：受控语料正文解析最小实现

## 1. 任务身份与当前状态

- 任务：`S6-T5.4-I1 Controlled Corpus ContentResolver Minimal Implementation`
- 当前状态：`Completed, pending human acceptance`
- 父任务：`S6-T5.4 Completed, pending human acceptance`
- 当前分支：`feature/stage6-rag`
- 实现基线：`4155ed8`
- 实现类型：`ENGINEERING_VALIDATION`，不是 `FORMAL_EXPERIMENT`

## 2. 本轮实现了什么

实现了受控、无副作用的最小链路：

```text
ContentRef + expected_content_hash
  -> CorpusContentResolver
  -> ApprovedCorpusSnapshotRegistry
  -> CorpusSnapshotReader
  -> exact chunk read
  -> UTF-8 SHA-256 verification
  -> ResolvedContent
```

`ResolvedContent` 与 Content Resolution 错误唯一归属 `contracts/`。行为层 `context/` 仅包含 Protocol、
`CorpusContentResolver`、合成内存 reader/registry 和 legacy `chroma:` 到 canonical `corpus:` 的 immutable
exact-match adapter。未知引用、未知 snapshot/chunk、reader 身份不一致、hash 不一致和未预期底层异常均 fail closed，
并使用固定脱敏错误消息。

## 3. 为什么这样设计

检索 evidence 本身不应携带正文。正文解析是短生命周期权限操作，所以接口要求 caller 同时提供引用和预期内容 hash，
并只允许按精确 chunk ID 读取。这样后续 ContextBuilder 即使获批，也不能通过枚举语料、猜测 legacy ref 或忽略
内容完整性来取得正文。

企业中常见的风险是索引引用、正文库和评估标签混用。该设计将正文权限、完整性校验和审计脱敏固定在单点，便于审查、
告警和后续替换真实 snapshot provider。

## 4. TDD 与验证证据

先建立失败测试，再实现最小代码。测试覆盖：DTO 不可变性、正文不进入 repr/audit、UTF-8 与 CRLF/NFD hash 语义、
unknown snapshot/chunk、reader provenance、hash mismatch、legacy exact-match/no fallback、异常脱敏、DTO owner、
无 Chroma/GroundTruth/legacy 业务导入。

本轮只使用 synthetic in-memory body 与 mapping；未读取或修改 `data/stage6_rag/` 的正文/fixture，未调用
Embedding、Chroma、Groq、LLM，也没有产生正式实验结果或 runtime 数据。

## 5. 可讲述的面试价值与边界

可以说：我把 RAG 从“检索命中后直接拼接正文”的隐式流程，拆成受控的正文权限边界，使用 canonical reference、
snapshot identity、UTF-8 SHA-256 和 fail-closed 规则保护后续上下文构建。

不能说：已证明检索安全、抗知识污染、Citation Accuracy、R1-R6 攻击防护率或生产可用性。S6-T5.5、ContextBuilder、
Citation 及正式 RAG 安全实验均未获批准。

## 6. 人工验收问题

1. 该最小 resolver 是否满足正文权限与审计隔离要求？
2. legacy `chroma:` 的 exact-match allowlist 是否足以作为受控迁移边界？
3. 是否批准后续任务的独立设计审查？本记录不自动批准 S6-T5.5。
