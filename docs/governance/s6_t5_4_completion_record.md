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

## 7. S6-T5.4-H1 人工验收发现项加固（待人工复核）

`S6-T5.4-H1 ContentResolver Capability and Failure-Boundary Hardening` 已完成，状态为
`Completed, pending human review`。它没有新增检索、正文来源、上下文构建或实验能力，只修复 I1 的两项边界：

1. 删除 `CorpusContentResolver.registry` 公共属性。调用方只持有 `resolve()` capability，不能通过公共 API 取得
   registry、reader、`read_chunk` 或原始 chunk mapping；测试需要复用 registry 时由测试 helper 显式返回。
2. 注入 adapter、registry、reader 所抛出的 `ContentResolutionError` 不再原样上抛。resolver 只信任
   `(异常类别, error_code)` 的六个合法组合，并以固定、脱敏消息重新构造异常，再使用 `raise ... from error` 保留内部
   cause。未知 code 或类别/code 交叉均映射为 `ContentResolutionRuntimeError / CONTENT_RESOLUTION_FAILURE`。
3. `ResolvedContent` 的非字符串正文属于 runtime failure，统一为
   `ContentResolutionRuntimeError / CONTENT_RESOLUTION_FAILURE`，不再出现 integrity class 与 runtime code 错配。

验证仅使用 synthetic in-memory content，覆盖 canonical/legacy 正常路径、registry capability 不可见、六个稳定
code/type 映射、伪造或交叉 code、敏感正文/路径不出现在 `str(exception)`、以及 cause 保留。I1 与父任务仍为
`Completed, pending human acceptance`；本 H1 不把它们标为 `HUMAN_ACCEPTED`，也不批准 S6-T5.5 或正式 RAG 实验。

## 8. GOV-S6-T5.4-ACCEPTANCE：最终人工验收（2026-07-25）

项目负责人现已接受 `S6-T5.4-P1`、`S6-T5.4-I1`、`S6-T5.4-H1` 及父任务
`S6-T5.4 Controlled Corpus ContentResolver`。当前状态均为 `HUMAN_ACCEPTED`，最后接受的实现提交为
`11a72f7`。本次验收确认 contracts 唯一 `ResolvedContent`、`ContentRef + expected_content_hash` 唯一输入、
仅 `resolve()` 的公共 API、受控 registry/reader、原始 UTF-8 SHA-256、exact-match legacy mapping、
fail-closed integrity 与异常脱敏/cause 保留；所有验证只使用 synthetic in-memory content。

此前 P1/I1/H1 的 pending 状态、protocol blocker、`RESOLVED_BY_APPROVED_PROTOCOL_FREEZE`、capability escape
和错误穿透发现均保留为历史审计记录。本次验收仍是 `ENGINEERING_VALIDATION`，不是正式 RAG 安全实验，也不证明
检索质量、知识污染防护、Citation Accuracy、Trust 或生产可用性。`S6-T5.5`、S6-T5.6 及后续任务均为
`NOT APPROVED`。
