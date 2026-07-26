# S6-T5.5-I1 完成记录：EvidenceEnvelope、Citation 契约与结构化渲染最小实现

## 1. 任务身份与状态

- Task ID：`S6-T5.5-I1`
- Task Name：`EvidenceEnvelope, Citation Contracts and Structural Rendering Minimal Implementation`
- 当前状态：`Completed, pending human acceptance`
- 父任务：`S6-T5.5 Completed, pending human acceptance`
- 实现类型：`ENGINEERING_VALIDATION`，不是 `FORMAL_EXPERIMENT`
- 最后已接受业务实现提交：`11a72f7`（本任务尚未改变该事实）

## 2. 本轮实现了什么

本轮只使用合成、进程内正文，形成以下最小链路：

```text
RetrievalEvidence + ResolvedContent
  -> CanonicalEvidenceEnvelopeFactory
  -> EvidenceEnvelope

CitationMode -> deterministic LF instruction
EvidenceEnvelope + CitationBinding -> one XML-like rendered block
```

稳定 DTO 唯一位于 `contracts/evidence_envelope.py`：`EvidenceEnvelope`、`CitationBinding`、`CitationMode`。
Factory 位于 `context/envelope.py`；instruction 位于 `context/citation.py`；唯一单 block renderer 位于
`context/rendering.py`。没有 `context/models.py`、`ContextBuilder`、`RetrievedContextPackage` 或 package-level
Citation allocator。

## 3. 关键安全边界

- Envelope 的正文只来自 `ResolvedContent`，其 provenance、rank、metric 和公开 metadata 只来自
  `RetrievalEvidence`；Factory 同时校验 canonical `corpus:` ContentRef、snapshot、chunk 与 hash。
- CitationBinding 只验证单个局部 ID 与七项稳定身份字段；不在本轮判断 package 内唯一性、连续编号或分配 `E1...En`。
- renderer 只接受 Envelope + Binding。七项 identity 任一不一致即以
  `CITATION_BINDING_MISMATCH` fail closed，不返回 partial/empty block，也不解释为 abstention。
- XML escaping 仅保护 XML-like 结构；它不构成语义 Prompt Injection 防护。
- `to_audit_dict()` 不含正文；`dataclasses.asdict()` 会形成敏感副本，因此被测试明确标记为非普通审计 API。

## 4. 为什么这样设计

上一任务 S6-T5.3 的 Evidence 只带公开 provenance，S6-T5.4 的 ResolvedContent 才持有经过 hash 校验的正文。
本轮用唯一 Factory 把两者绑定，避免任意调用方用裸字符串、metadata 或 legacy ref 绕过正文完整性和语料身份检查。
企业中这相当于将“正文权限”“可追溯引用”和“渲染权限”拆开：审计日志可以保留 hash、来源和长度，而不扩散正文。

## 5. TDD 与验证留痕

Red 阶段新增测试后，因 DTO、Factory、instruction 与 renderer 尚不存在而出现 7 个收集错误。首次 Green 又发现：
测试辅助函数提前对非法正文求 hash，以及直接使用 `mappingproxy` 会让 `dataclasses.asdict()` 失败。前者改为为非法
对象提供占位 hash；后者采用只读 metadata 包装，使运行时仍深度只读、`asdict()` 明确产生敏感副本。两项都不涉及
Stage 6 fixture、Retriever、Resolver 或历史实验资产。

定向 S6-T5.5-I1 测试通过：`60 passed, 68 subtests passed`；最终完整离线回归通过：
`340 passed, 2616 subtests passed`。Ruff 通过；scoped MyPy 在 42 个 retrieval 源文件上通过。
namespace、context-persistence、experiment-master-record 与 no-label-leakage 定向治理回归通过：
`31 passed, 1527 subtests passed`。本轮 30 个变更文件的 Markdown 相对链接、secret-shape、绝对路径和
受保护路径检查均通过；`git diff --check` 通过，Stage 6 runtime 路径已被 Git ignore。全仓受版本控制文件仍有
31 个历史 secret-shape 文件命中，属于不可改写的历史产物，不得将其误报为本轮新增风险。

## 6. 教学与面试边界

**初学者容易误解**：XML escaping 不是“模型已不会被提示注入”；它只避免正文伪造 XML 标签改变结构。
Citation ID 也不是跨运行稳定 ID，它只是未来 package 内的局部展示编号；Evidence UID 才负责稳定追溯。

**面试可讲**：我先把“检索到什么”与“允许把哪段正文放入上下文”分开，再将正文、来源、hash、rank 与本地引用绑定。
如果 Binding 与 Envelope 不匹配，系统 fail closed，而不是悄悄替换编号或输出残缺 Context。

**不能宣称**：尚未实现 ContextBuilder、budget、package、Citation allocation、Citation Accuracy、Trust、LLM 调用或
R1--R6 正式实验；没有读取 Stage 6 fixture，也没有调用 Embedding、Chroma、Groq 或 LLM。

## 7. S6-T5.5-H1 人工验收发现项修复（2026-07-26）

H1 只加固 I1 的 object immutability 和 validation boundary。修复前，metadata wrapper 的 `_value` 可以被普通属性
赋值替换；Envelope 对 7/9 位小数秒比 RetrievalEvidence 更窄；超大整数 metric 会泄露 Python `OverflowError`；
Binding 字段错误会被误写成 `INVALID_CITATION_ID`。修复后，wrapper 为 slots-only 的不可重绑内部对象，Envelope
复用 RetrievalEvidence 的 UTC timestamp 接受语义，metric/metadata/ID input 统一对外为固定、脱敏错误，Binding
字段错误独立映射为 `INVALID_CITATION_BINDING`。canonical Evidence UID 收紧为 `EV-[0-9a-f]{64}`。

两条历史治理数字不冲突：`31 passed, 1527 subtests passed` 是 I1 时运行
`test_namespace_compatibility.py`、`test_experiment_master_record.py`、`test_context_persistence.py` 与
`test_no_label_leakage.py` 的集合；`41 passed, 1595 subtests passed` 是在前者基础上额外包含
`test_s6_t5_5_protocol_freeze.py` 的集合。两者均为 I1 历史结果，不能静默替换成同一个数字。

H1 的 Red 测试新增后有 20 项失败，分别暴露 wrapper 可重绑、7/9 位小数秒不兼容、metric `OverflowError` 外泄、
noncanonical Evidence UID 被接受、metadata 原始错误消息外泄、citation ID 长度缺口和 Binding 字段错误分类错误。
Green 后的 H1 定向命令与结果为：

```text
python -m pytest tests/architecture/test_namespace_compatibility.py \
  tests/architecture/test_experiment_master_record.py \
  tests/architecture/test_context_persistence.py \
  tests/architecture/test_s6_t5_5_protocol_freeze.py \
  tests/stage6_rag/test_no_label_leakage.py -q -p no:cacheprovider
# 42 passed, 1611 subtests passed

python -m pytest tests/domains/retrieval/context -q -p no:cacheprovider
# 122 passed

python -m pytest tests/architecture tests/stage6_rag tests/domains/retrieval \
  -q -p no:cacheprovider
# 382 passed, 2632 subtests passed
```

Ruff 通过；scoped MyPy 在 42 个 retrieval 源文件上通过。一次误用的不存在目录
`tests/domains/retrieval/context_resolution` 导致 pytest 在 collection 前失败，未执行代码、读取 fixture 或修改文件；
已改用仓库实际的 `tests/domains/retrieval/context/`。本任务仍是 `OFFLINE_ENGINEERING_HARDENING`，不是正式实验。

提交前 H1 changed-file 扫描覆盖 17 个变更文件：Markdown 相对链接、secret-shape、绝对路径和 protected-path 均通过；
`git diff --check`、Stage 1--5/Stage 6 fixture/legacy `src/codeguarder` 完整性检查及 runtime Git-ignore 均通过。全仓受
版本控制文件仍有 31 个既有 historical secret-shape 命中，未将其改写或误报为本轮新增风险。
