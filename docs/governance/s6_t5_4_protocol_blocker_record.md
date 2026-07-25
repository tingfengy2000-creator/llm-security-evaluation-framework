# S6-T5.4 Controlled Corpus ContentResolver 协议 Blocker 记录

- 日期：`2026-07-25`
- Task ID：`S6-T5.4`
- Task Name：`Controlled Corpus ContentResolver`
- 状态：`DESIGN_OR_PROTOCOL_BLOCKER`
- 批准状态：`APPROVED_TO_START`，但实现已按 fail-closed 原则暂停。
- 基线提交：`142528d`

## 1. 发现背景

项目负责人已经单独批准 S6-T5.4 的任务范围：使用既有 `RetrievalEvidence.content_ref` 和
`RetrievalEvidence.content_hash`，从受控 corpus snapshot 解析正文、重新计算 UTF-8 SHA-256 并在不一致时
立即失败。本记录不否定该目标，也不改变 S6-T5.3 的 `HUMAN_ACCEPTED` 状态。

在开始 TDD 前，已核对 S6-T5 冻结规格、实施计划、ADR 0008、现有 `ContentRef` contract、公共数据 loader
以及现有测试。冻结材料明确了 ContentRef 唯一归属、scheme 显式分派、禁止从 Chroma 读取正文、Ground Truth
隔离和 hash mismatch fail-closed；但以下长期公共契约仍未被精确定义。

## 2. 缺失的冻结契约

| 缺口 | 为什么不能自行补齐 | 如果猜测实现的风险 |
| --- | --- | --- |
| Resolver Protocol 的准确返回类型 | 规格只规定“解析正文并校验 hash”，没有规定成功结果是裸 `str`、受控不可审计对象，还是具有显式正文权限生命周期的 contract。 | 后续 EvidenceEnvelope/ContextBuilder 可能被迫适配错误的正文权限语义，扩大泄露面。 |
| corpus snapshot 的受控读取接口 | 当前 public loader 面向数据集加载，不是 snapshot/chunk 的最小只读解析接口；冻结设计没有规定 Resolver 依赖的接口、索引建立方式或关闭/生命周期语义。 | 可能把完整 corpus、文件路径或 evaluator 可见对象暴露给 Resolver，破坏最小权限与标签隔离。 |
| legacy `chroma:` fixture 到 corpus 的唯一映射 | `ContentRef` 能验证 legacy 格式，但冻结材料没有定义旧 fixture identifier 如何唯一对应 approved snapshot 和 chunk。 | 任意 legacy ref 可能错误解析、退回 `doc_id`/`source_id`/文件名，或形成隐式 Chroma 依赖。 |
| 错误分类的归属 | 已有 `ContentRefError` 与 Retrieval errors，但未冻结 `UNKNOWN_CORPUS_SNAPSHOT`、`UNKNOWN_CORPUS_CHUNK`、`CONTENT_HASH_MISMATCH` 等应属于 contracts 还是 context behavior，以及稳定 public exception 形态。 | 出现第二套错误协议，或把 loader 私有异常、正文、路径和 metadata 原值暴露出去。 |

## 3. 正确处置

- 不创建 `src/llmguard/domains/retrieval/context/`，不编写 ContentResolver、fixture adapter 或第二套 DTO；
- 不编写依赖未冻结返回类型的业务 Red 测试，避免为不安全的猜测实现建立伪规格；
- 不读取 corpus 正文、不调用 public loader、不访问 `ground_truth/`，不调用 Chroma、Embedding、Groq 或 LLM；
- 不回退到 `source_id`、`doc_id`、文件名或路径来解析 legacy ref；
- 保留 S6-T5.3、`parent_doc_id` blocker 和 H1 `candidate_count` 修复的历史记录，不改写其证据。

## 4. 请求项目负责人补充的最小决策

恢复 S6-T5.4 前，需明确并冻结：

1. `ContentResolver` 的唯一输入、成功返回类型及正文权限对象的生命周期；
2. 仅按 `corpus_snapshot_id + chunk_id` 提供正文的受控读取 Protocol，以及它能接收的 approved snapshot registry；
3. legacy `chroma:` fixture ref 的固定、可审计、无 fallback 映射表或 adapter contract；
4. ContentResolver 的稳定异常基类、error-code 所有权与外部脱敏消息规则。

这些决定应进入 S6-T5 规格/ADR 或项目负责人决策登记册后，才可以编写 TDD Red 测试并开始实现。

## 5. 结论边界

本 blocker 只说明当前冻结协议不足以安全建立长期 ContentResolver API。它不表示 S6-T5.3 有缺陷，也不产生
ContentResolver、Context、Citation、Trust 或正式 RAG 安全实验结果。`S6-T5.5` 及后续任务仍为 `Not approved`；
正式 RAG 安全实验仍为 `Not started`。

## 6. 本轮验证记录

- ContentResolver 定向测试：`NOT_RUN`。原因是 `tests/domains/retrieval/context/` 及其测试所依赖的稳定
  返回 contract 未冻结；创建它们会把猜测写成长期行为规格。
- ContentRef contract：`2 passed`；S6-T5.3 DenseRetriever：`18 passed`；chunking：`22 passed, 30 subtests passed`；
  embedding/vectorstore 离线测试：`41 passed, 29 subtests passed`。
- architecture：`35 passed, 455 subtests passed`；contract ownership 与 namespace：`6 passed, 6 subtests passed`；
  Stage 6 label isolation：`8 passed, 1199 subtests passed`。
- 全部 Stage 6 离线组合回归：`200 passed, 1955 subtests passed`。这些是既有工程契约回归，不是
  ContentResolver 验收，不是正式 RAG 安全实验。

## 7. S6-T5.4-P1 批准的协议冻结方向（2026-07-25）

项目负责人已批准 `S6-T5.4-P1 Content Resolution Contract and Permission Boundary Freeze`。该子任务只
冻结四项缺失决策的方向：

1. `ContentResolver.resolve(content_ref, expected_content_hash) -> ResolvedContent` 是唯一解析面；
   `ResolvedContent` 由 `contracts/` 唯一拥有，正文是短生命周期、进程内权限对象；
2. Resolver 未来只通过 `ApprovedCorpusSnapshotRegistry` 获得 `CorpusSnapshotReader`，按 snapshot 与
   chunk 最小读取并校验 pinned fingerprint；
3. legacy `chroma:` 只能经 `LegacyContentRefAdapter` 的 immutable exact-match allowlist 和
   `mapping_hash` 迁移，不允许推导或 fallback；
4. 内容解析错误唯一归属 `contracts/errors.py`，分为 Lookup、Integrity、Runtime 三类，所有外部错误
   固定脱敏。

这是批准的**解决方向**，不是业务实现，也不是对语料正文、fixture、Chroma 或 Ground Truth 的访问许可。
`S6-T5.4-P1` 当前为 `Completed, pending human acceptance`；本 blocker 尚未正式 RESOLVED。父任务
`S6-T5.4` 仍是 `APPROVED_TO_START / DESIGN_OR_PROTOCOL_BLOCKER`；只有 P1 获人工验收且后续最小实现
得到单独批准后，才可创建 ContentResolver 的业务 TDD。
