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

`S6-T5.6 ContextBuilder` 的固定顺序仍为：稳定排序、Evidence UID 去重、数量限制、正文解析与 hash 验证、
预算选择、Citation ID 分配、渲染。它按最终保留的 Evidence 顺序一次性分配连续 `E1 ... En`，再创建对应的
`CitationBinding`。因此本轮只冻结 allocator 的规则，**不执行**分配；不会为后来被去重或预算排除的 Evidence
预先生成错误引用。

## 3. 唯一 owner 与构造边界

未来稳定 DTO 的唯一 owner 是 `src/llmguard/domains/retrieval/contracts/`：

- `EvidenceEnvelope`：建议模块 `contracts/evidence_envelope.py`；
- `CitationBinding`、`CitationMode`：同一 contracts owner，或由该模块明确 re-export；
- 所有稳定异常：`contracts/errors.py`；
- `context/` 只拥有行为，不得建立 `context/models.py` 或 DTO 副本。

唯一生产构造行为冻结为未来的 `EvidenceEnvelopeFactory.create(*, evidence: RetrievalEvidence,
resolved_content: ResolvedContent) -> EvidenceEnvelope`。此 factory 的 concrete implementation 属于**单独批准的
S6-T5.5 实现**，本 P1 不创建它。工厂必须验证 chunk、hash 与 canonical `corpus:` snapshot/chunk identity；legacy
`chroma:` 必须已经由已验收 Resolver 的 exact-match mapping 归一化。`doc_id`、`parent_doc_id`、来源、版本、rank 和
metric 只能复制自 `RetrievalEvidence`；正文只能复制自 `ResolvedContent`；`public_metadata` 只能复制已冻结的
Evidence public metadata。任何调用者都不得以任意 `str` 正文和自定义 metadata 直接拼装 Envelope。

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
| `INVALID_CITATION_MODE` | Citation input | 非法枚举或 instruction 请求 |
| `CONTEXT_RENDERING_FAILURE` | Rendering runtime | 结构化 rendering 失败 |

具体类名与继承关系必须在获批实现前基于现有 `RetrievalContractError` 层级再次审查；不得在本 P1 为了“预占代码”新增
源码。结构错误必须 fail closed，不能返回空 Envelope，更不能解释为 abstention。

Envelope、Binding、instruction、rendering 和 audit representation 不得携带 evaluator 标签：`poisoned`、
`poison_label`、`label`、`attack_id`、`attack_goal`、`attack_category`、`expected_answer`、`expected_behavior`、
`failure_type`、`ground_truth`、`oracle`、`risk_goal`、`stealth_level`。受控正文可被 Envelope 暂存，但“该正文是否
污染”的标签不得进入运行时对象或渲染结构。

## 7. 与 S6-T5.6 的边界和人工审查问题

S6-T5.5-P1 只解决长期接口语义，不能构成工程能力或实验结果。未来 S6-T5.5 实现获批前，须先对本记录逐条 TDD；
S6-T5.6 ContextBuilder 只有在 T5.5 被人工验收后，才可创建最终 package、CitationBinding、多个 Evidence block、
预算和 Context hash。Citation Accuracy、Trust、LLM、真实正文 provider 和正式 RAG 安全实验均不在本轮范围。

人工审查应确认：方案 A 的时序是否接受；factory 是否能成为唯一生产构造入口；敏感导出继续 deny-by-default 是否
可接受；精确 instruction/template/escaping 是否满足可复现性需求。批准本 P1 不等于批准 S6-T5.5 实现。
