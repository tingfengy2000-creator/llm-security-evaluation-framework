# S6-T5.5-P1 协议审查记录：EvidenceEnvelope 与 Citation 边界

## 1. 任务身份与状态

- Task ID：`S6-T5.5-P1`
- Task Name：`EvidenceEnvelope and Citation Boundary Freeze`
- 任务性质：`DESIGN_FREEZE / PROTOCOL_REVIEW`
- 当前状态：`Completed, pending human acceptance`
- 父任务：`S6-T5.5 NOT APPROVED`
- 后续任务：`S6-T5.6+ NOT APPROVED`
- 正式 RAG 安全实验：`NOT STARTED`

本记录只冻结协议与未来实现边界。没有创建、修改或运行 `EvidenceEnvelope`、`CitationBinding`、rendering 或
`ContextBuilder` 业务源码；没有读取 Stage 6 fixture/data，也没有调用 Embedding、Chroma、Groq 或 LLM。

## 2. 先解决 Citation 时序矛盾

采用方案 A。`EvidenceEnvelope` **不持有** `citation_id`，也不使用 `None`、空字符串、`E0` 或任何“未绑定”占位值。
它只描述“已检索且已解析校验”的单条证据。`CitationBinding` 是未来 `ContextBuilder` 在最终 Evidence 集合确定后创建的
独立对象。

这使两个 ID 的职责保持清晰：

```text
Evidence UID: 稳定证据身份，可跨同一 immutable corpus snapshot 的运行追溯
Citation ID: 当前 RetrievedContextPackage 内的局部展示编号，只在最终 Context 顺序确定后存在
```

`S6-T5.6 ContextBuilder` 的固定顺序仍为：稳定排序、Evidence UID 去重、数量限制、正文解析、hash 验证、
完整 block 预算选择、连续 Citation ID 分配、`CitationBinding` 创建、单 block 渲染、package 组装。它按最终保留的
Evidence 顺序一次性分配连续 `E1 ... En`，再创建对应 Binding。因此本轮只冻结 allocator 的规则，**不执行**分配；
不会为后来被去重或预算排除的 Evidence 预先生成错误引用。

## 3. 唯一 owner 与构造边界

未来稳定 DTO 的唯一 owner 是 `src/llmguard/domains/retrieval/contracts/`：

- `EvidenceEnvelope`：建议模块 `contracts/evidence_envelope.py`；
- `CitationBinding`、`CitationMode`：同一 contracts owner，或由该模块明确 re-export；
- 所有稳定异常：`contracts/errors.py`；
- `context/` 只拥有行为，不得建立 `context/models.py` 或 DTO 副本。

唯一生产构造行为冻结为未来的 `EvidenceEnvelopeFactory.create(*, evidence: RetrievalEvidence,
resolved_content: ResolvedContent) -> EvidenceEnvelope`。此 factory 的 concrete implementation 属于**单独批准的
S6-T5.5 实现**，本 P1 不创建它。Factory **只接受 canonical RetrievalEvidence**：`evidence.content_ref` 必须是
已验证的 `ContentRef`、scheme 必须为 `corpus`，并且它必须严格等于 `resolved_content.canonical_content_ref`；
`evidence.corpus_snapshot_id`、`chunk_id`、`content_hash` 必须分别等于 ResolvedContent 的同名字段。仅 chunk/hash
相同但 snapshot 或 canonical reference 不同的组合一律拒绝为 `EVIDENCE_CONTENT_MISMATCH`。

legacy `chroma:` 只属于已验收 ContentResolver 的**输入**边界：`legacy chroma: ContentRef ->
LegacyContentRefAdapter -> canonical corpus: ContentRef -> ResolvedContent`。它不进入 EnvelopeFactory；Factory 不接受
legacy Evidence、未验证 ContentRef、任意 legacy record、DocumentRecord、ChunkRecord、裸 metadata 或裸正文 str，且不
猜测、映射或访问 Legacy Adapter。`doc_id`、`parent_doc_id`、来源、版本、rank、metric 与 public_metadata 只能复制自
RetrievalEvidence；正文只能复制自 ResolvedContent。任何调用者都不得以任意正文和自定义 metadata 直接拼装 Envelope。

## 4. EvidenceEnvelope 与 CitationBinding 契约

`EvidenceEnvelope` 字段冻结为：`evidence_uid`、`doc_id`、`chunk_id`、`parent_doc_id`、`source_id`、
`source_type`、`version`、`timestamp`、`content_hash`、`rank`、`distance`、`similarity`、`content`、
`public_metadata`。它必须为 `frozen=True, slots=True, kw_only=True`；`rank > 0`，metric 有限，`content` 的原始
UTF-8 SHA-256 必须等于 `content_hash`，`public_metadata` 深度只读，`content` 使用 `repr=False`。

`CitationBinding` 字段冻结为：`citation_id`、`evidence_uid`、`chunk_id`、`parent_doc_id`、`content_hash`、
`source_id`、`version`、`rank`。`citation_id` 只能是 `E<positive integer>`；在**一个** package 内唯一、连续，且与
最终 Context Evidence 顺序相同。它不保存正文、完整 Query 或 Resolver capability，也不宣称跨 package 稳定。

两种对象的普通 `repr()` 与 `to_audit_dict()` 都不得出现正文；不提供普通正文 serialization。`dataclasses.asdict()`
是敏感操作而非 audit API。显式敏感工件导出本轮冻结为 **deferred and deny-by-default**：在未来获得独立
`SensitiveArtifactPolicy` 审批前，不得增加 `to_dict(include_content=True)` 或任何可无权限导出正文的接口。

## 5. CitationMode、instruction 与 XML-like rendering

`CitationMode` 的稳定枚举值为 `off`、`available`、`required`。未来唯一 instruction generator 位于
`context/citation.py`；它只接收 mode，不接收 Query、正文或标签，并以 LF 结尾返回以下精确字符串：

```text
off:       Use the evidence below to answer the user.\n
available: Use the evidence below to answer the user. You may cite supporting evidence with [E#].\n
required:  Use the evidence below to answer the user. Cite every factual claim with [E#]. If the evidence does not support a claim, say that the evidence is insufficient; do not invent a citation.\n
```

`required` 是回答约束，不是安全保证；本轮不调用 LLM，也不计算 Citation Accuracy。

未来唯一 rendering owner 为 `context/rendering.py`。它使用 `escape_xml_text()` 和 `escape_xml_attribute()`：每次都对
原始输入执行一次 escaping，不将既有实体视为已安全，因此 `&lt;` 会渲染为 `&amp;lt;`。不做 Unicode normalization；
正文先用渲染层规则把 CRLF/CR 转为 LF，再 escape。原始正文 hash 始终在转换前按 UTF-8 bytes 验证。

最终 block 的模板、attribute 顺序与 LF 规则冻结如下；其中 `distance`、`similarity` 必须是有限数，负零归一为
`0.0`，再用 locale-independent `format(value, ".17g")` 表示：

```text
<EVIDENCE citation_id="E<n>" evidence_uid="..." doc_id="..." chunk_id="..." parent_doc_id="..." source_id="..." source_type="..." version="..." timestamp="..." content_hash="..." rank="<base-10 integer>" distance="<float>" similarity="<float>">
<CONTENT>
<escaped content>
</CONTENT>
</EVIDENCE>
```

模板的闭合 `</EVIDENCE>` 后必须恰好带一个 LF；无额外空行。

未来唯一单 block renderer 接口为：

```python
def render_evidence_block(
    *,
    envelope: EvidenceEnvelope,
    binding: CitationBinding,
) -> str: ...
```

它不接受裸 `citation_id`、裸正文、裸 metadata、任意 dict，也不从 Envelope rank 猜测 Citation ID 或自行创建 Binding。
renderer 必须逐项比较 `evidence_uid`、`chunk_id`、`parent_doc_id`、`content_hash`、`source_id`、`version`、`rank`；
Citation ID 只能来自 `binding.citation_id`。任一字段不一致必须以 `CITATION_BINDING_MISMATCH` fail closed：不返回
partial/empty block、不跳过后继续、不重编号掩盖错误，也不解释为 abstention。

属性均使用 attribute escaping；正文只使用 text escaping。正文中的 `</EVIDENCE>`、`<EVIDENCE>`、`<SYSTEM>` 与
`<INSTRUCTION>` 因此不能改变结构。Escaping **只**保护结构边界，不构成语义 Prompt Injection 防御，也不替代
Guard 或 Trust policy。`S6-T5.5-P1` 不拼接多个 block、不应用预算、不计算 Context hash。

## 6. 错误与标签隔离

错误唯一 owner 为 `contracts/errors.py`。未来实现应使用固定脱敏 message，保留内部 cause 但不外泄正文、Query、
rendered block、路径、metadata 原值或标签。P1 冻结的语义映射为：

| Error code | 未来语义 owner | 使用时机 |
| --- | --- | --- |
| `EVIDENCE_CONTENT_MISMATCH` | Envelope integrity | Evidence 与 ResolvedContent 的 chunk/hash/canonical identity 不一致 |
| `INVALID_EVIDENCE_ENVELOPE` | Envelope input/integrity | 字段、不变量、metric 或正文 hash 不合法 |
| `UNEXPECTED_ENVELOPE_CONSTRUCTION_FAILURE` | Envelope runtime | 不受信依赖或未预期构造失败 |
| `INVALID_CITATION_ID` | Citation input | 不满足 `E<positive integer>` |
| `DUPLICATE_CITATION_ID` | Citation integrity | 同 package 重复 |
| `CITATION_SEQUENCE_INVALID` | Citation integrity | 非连续或未对应最终顺序 |
| `CITATION_BINDING_MISMATCH` | Citation / rendering integrity | Binding 与 Envelope 的七项稳定身份字段任一不一致 |
| `INVALID_CITATION_MODE` | Citation input | 非法枚举或 instruction 请求 |
| `CONTEXT_RENDERING_FAILURE` | Rendering runtime | 结构化 rendering 失败 |

未来实现前必须再次基于现有 `RetrievalContractError` 层级审查具体类名与继承关系；不得在本 P1 为了“预占代码”新增
源码。`CITATION_BINDING_MISMATCH` 的固定脱敏外部消息为 `citation binding does not match evidence`；保留内部 cause
时使用 `raise ... from error`，但不回显正文、rendered block、Query、ContentRef 原值、metadata 原值、标签、
Ground Truth、本机路径或底层异常原文。结构错误必须 fail closed，不能返回空 Envelope，更不能解释为 abstention。

Envelope、Binding、instruction、rendering 和 audit representation 不得携带 evaluator 标签：`poisoned`、
`poison_label`、`label`、`attack_id`、`attack_goal`、`attack_category`、`expected_answer`、`expected_behavior`、
`failure_type`、`ground_truth`、`oracle`、`risk_goal`、`stealth_level`。受控正文可被 Envelope 暂存，但“该正文是否
污染”的标签不得进入运行时对象或渲染结构。

## 7. 与 S6-T5.6 的边界和人工审查问题

S6-T5.5-P1 只解决长期接口语义，不能构成工程能力或实验结果。未来 S6-T5.5 实现获批前，须先对本记录逐条 TDD；
S6-T5.6 ContextBuilder 只有在 T5.5 被人工验收后，才可实际执行 Citation allocation、创建 Binding、创建最终
package、组装多个 Evidence block、应用预算和计算 Context hash。Citation Accuracy、Trust、LLM、真实正文 provider 和
正式 RAG 安全实验均不在本轮范围。

人工审查应确认：方案 A 的时序是否接受；factory 是否能成为唯一生产构造入口；敏感导出继续 deny-by-default 是否
可接受；精确 instruction/template/escaping 是否满足可复现性需求。批准本 P1 不等于批准 S6-T5.5 实现。

## 8. S6-T5.5-P1-H1：Canonical Binding 与 Renderer 协议加固（2026-07-26）

人工审查发现原记录把“Resolver 可解析 legacy `chroma:` 输入”表述得过于接近 Factory 输入边界，且没有把单 block
renderer 的 Binding identity 验证写成唯一接口。本 H1 已明确：Factory 只接受 canonical `corpus:`
RetrievalEvidence，legacy compatibility 在 Resolver 输入边界结束；Factory 不负责 legacy 映射。renderer 唯一输入为
`EvidenceEnvelope + CitationBinding`，且必须验证七项稳定字段后才取用 `binding.citation_id`。

`CITATION_BINDING_MISMATCH` 是新增的 fail-closed Citation/rendering integrity error，固定外部消息为
`citation binding does not match evidence`。它不是 abstention、跳过、重编号或空 block 的理由。本 H1 不创建任何源码，
不调用模型，不读取 fixture；当前状态为 `Completed, pending human review`。P1 仍为 `Completed, pending human
acceptance`，S6-T5.5 与 S6-T5.6+ 仍为 `NOT APPROVED`，正式实验仍为 `NOT STARTED`。

### 8.1 H1 验证留痕与扫描边界

本轮先后运行了协议治理定向测试、Stage 6/architecture/retrieval 离线回归、Ruff、scoped MyPy、Markdown 相对链接、
变更文件 secret-shape 与绝对路径扫描、protected-path、runtime Git-ignore 以及 `git diff --check`。其中，第一次
Markdown 链接扫描因仓库根目录 Markdown 文件的 parent path 为空而在扫描器启动阶段失败；修正扫描器对根目录使用 `.`
作为 parent 后，结果为零个失效相对链接。该失败不读取 fixture、不涉及业务代码，也不表示文档链接失效。

全仓 secret-shape 扫描会命中不可变的 Stage 1--4 HTML 历史报告、历史 guard 测试样例和 `chatgpt_share_2.html` 导出。
这些命中属于既有实验/归档内容，不能在本次纯治理任务中被删除或改写；对本轮 11 个变更文件复扫后，secret-shape 和本机
绝对路径命中均为 0。故本轮的结论是“新增治理变更无 secret/path 命中”，而不是把历史归档误称为不存在的全仓风险。

## 9. GOV-S6-T5.5-P1-ACCEPTANCE：协议人工验收（2026-07-26）

项目负责人已人工接受 `S6-T5.5-P1` 与 `S6-T5.5-P1-H1`。本验收只确认本记录冻结的时序、canonical identity、
Factory/renderer 输入、七字段 Binding 校验、fail-closed 错误、escaping 和敏感导出边界；它不创建或验证
`EvidenceEnvelope`、`CitationBinding`、renderer、`RetrievedContextPackage` 或 `ContextBuilder` 业务实现。

当前权威状态为：P1 与 H1 均为 `HUMAN_ACCEPTED`；`S6-T5.5` 为
`READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`；`S6-T5.5-I1` 为 `NOT YET APPROVED`；`S6-T5.6+` 为
`NOT APPROVED`；正式 RAG 安全实验为 `NOT STARTED`。最后接受的 stage implementation 仍是 S6-T5.4 的
`11a72f7`，本设计提交 `25fb83d` 不得被表述为业务实现提交。

历史 pending/review 快照、H1 修订过程和历史全仓 secret-shape 命中继续保留。对于扫描结论，只能准确记录为：
本轮治理变更未引入新增 secret/path 命中；不得把不可变历史 HTML、测试样例和聊天导出中的既有形态命中表述为全仓零命中。

### 9.1 本次验收验证结果

本次验收实际运行的离线回归为 `290 passed, 2599 subtests passed`；Ruff 和 scoped MyPy 均通过。Markdown 相对链接、
变更文件 secret-shape、变更文件绝对路径、protected-path、runtime Git-ignore 与 `git diff --check` 均通过。
本次全仓 secret-shape 复扫发现 31 个文件包含既有形态命中；它们仍属于前述不可变历史资产，不是本轮引入的内容。
因此验收记录的准确表述保持为“本轮治理变更未引入新增 secret/path 命中”，而不是“全仓零命中”。

首次运行本次治理回归时，测试捕获了三项状态漂移：协议记录的“未实现”措辞与断言不一致、Stage README 使用了
`P1-H1` 缩写而未写全任务 ID、旧 context-persistence 断言仍把 S6-T5.5 写成 `NOT APPROVED`。均已修正为当前
人工验收状态；这不是业务实现问题。`PROJECT_MASTER_CONTEXT.md` 中仍保留的 pending 文字属于明确标注的历史快照，
不应被删除或误判为当前状态。

## 10. S6-T5.5-H1：Evidence 与 Citation 契约不可变性和验证加固（2026-07-26）

本 H1 是 I1 人工验收发现项的窄范围离线加固，而不是新的 Context 能力。`_FrozenPublicMetadata` 现为无
`__dict__` 的 slots-only 内部包装器：外层 `_value` 不能重绑，内部 mapping/sequence 继续深度只读，普通
`to_audit_dict()` 始终返回 detached dict/list。`dataclasses.asdict()` 仍会显式形成含正文和 metadata 的敏感副本，
因此没有新增普通敏感导出 API。

Envelope timestamp 现在与已验收 `RetrievalEvidence` 共用同一 canonical UTC 语义：接受任意长度的小数秒和
`Z`/`+00:00`，仍拒绝非 UTC、无 timezone、非法日期、CR/LF 和非字符串。Envelope metric 的
`OverflowError`、`ValueError`、`TypeError` 统一转换为 `INVALID_EVIDENCE_ENVELOPE`，固定公开消息为
`evidence envelope is invalid`，并以 `raise ... from error` 保留内部原因。metadata 类型、标签、路径、深度、
cycle 和不支持值也使用同一对外错误，不回显原始输入。

为收紧跨运行证据身份，新增 canonical Evidence UID 规则 `EV-[0-9a-f]{64}`；Envelope 与 Binding 都必须使用它。
Citation ID 仍为不超过 128 字符的 `E<positive integer>`。CitationMode 非法仍是
`INVALID_CITATION_MODE` / `citation mode is invalid`；Citation ID 非法仍是
`INVALID_CITATION_ID` / `citation id is invalid`；Binding 的 evidence UID、chunk、parent、hash、source、version
或 rank 非法现在明确为 `INVALID_CITATION_BINDING` / `citation binding is invalid`。七项 Binding 与 Envelope
身份不一致的 `CITATION_BINDING_MISMATCH` 语义不变。

本 H1 不改变 RetrievalEvidence、ResolvedContent、ContentResolver、DenseRetriever、Factory canonical checks 或
renderer exact output；不读取 fixture、不调用 Embedding、Chroma、Groq 或 LLM，不创建 ContextBuilder、Package、
预算或 Citation allocator。当前状态为 `Completed, pending human review`；I1 和父任务仍为
`Completed, pending human acceptance`，S6-T5.6+ 为 `NOT APPROVED`，正式 RAG 安全实验为 `NOT STARTED`，最后接受的
业务实现提交仍为 `11a72f7`。

## 11. GOV-S6-T5.5-ACCEPTANCE：I1/H1 与父任务人工验收（2026-07-26）

项目负责人已在保留第 1--10 节历史记录的前提下，将 `S6-T5.5-I1`、`S6-T5.5-H1` 和父任务 `S6-T5.5` 标记为
`HUMAN_ACCEPTED`。`2cacef7` 保留为 I1 初始实现历史；`6da27a6` 是最终接受的 hardening implementation commit。
第 9 节的 P1/P1-H1 协议人工验收和本节的实现人工验收共同构成当前边界。

本决定只确认本文冻结并实现的 contracts、Factory、immutable metadata、timestamp semantics、canonical Evidence UID、
Binding identity validation、redacted validation errors、instruction 和单 block renderer。它不把上述离线工程验证提升为
`FORMAL_EXPERIMENT`，不证明 Citation Accuracy、检索质量、安全效果、ContextBuilder、Context Package、Trust、LLM
集成或生产可用性。

`S6-T5.6` 和 `S6-T5.7+` 均为 `NOT APPROVED`；正式 RAG security experiment 为 `NOT STARTED`。历史 pending/review
快照及全仓 31 个既有 secret-shape 文件命中继续保留；本轮结论只能是新增治理变更未引入 secret/path 命中。
