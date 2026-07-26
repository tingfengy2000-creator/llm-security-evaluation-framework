# S6-T5.6-I1-H1 Context Package 完整性加固记录

## 1. 记录身份

- Task ID: `S6-T5.6-I1-H1`
- Task name: `Context Trace Integrity, Config Identity and Dependency Redaction Hardening`
- Task nature: `OFFLINE_ENGINEERING_HARDENING / SYNTHETIC_ONLY_TDD`
- Current status: `Completed, pending human acceptance`
- Parent task: `S6-T5.6-I1: Completed, pending human acceptance`
- Parent task: `S6-T5.6: Completed, pending human acceptance`
- Initial implementation candidate: `71067d1`
- Last accepted implementation commit: `6da27a6`
- S6-T5.7+: `NOT APPROVED`
- Formal RAG security experiment: `NOT STARTED`

本记录是对 I1 人工复核发现项的追加留痕，不改写 I1、P1、P1-H1 或 P1-H2 的历史记录。它不是正式 RAG 安全实验，也不是人工验收结论。

## 2. 发现、风险与修复

### H1-01: Trace 分区可覆盖但不一定符合构建情景

**发现**：旧校验只确认 UID 集合覆盖、互斥和计数，仍可能接受 `included -> budget excluded -> included`、多个预算排除、instruction 超预算同时又解析正文等不可能由稳定前缀算法产生的 Trace。

**风险**：审计对象会看似完整，却无法证明实际选择顺序；攻击或缺陷可伪造“未访问正文”的记录，削弱最小权限和可复现性。

**修复**：将 Trace 校验收紧为四个可验证情景：空检索、instruction 超预算、全部适配、首个或部分候选不适配。校验 resolved 顺序、included 前缀、至多一个 budget excluded、cutoff 后缀和每个 UID 的 decision 对齐。

### H1-02: Package 声明的配置哈希未与公开预算字段重新绑定

**发现**：Package 可以携带与 `max_evidence_count`、`max_context_characters` 或 schema 不匹配的预声明 config hash，只要 Trace 复制同一字符串就能通过。

**风险**：相同 Package identity 可能被错误解释为相同构建条件，破坏审计和复现前提。

**修复**：从 Package 的公开 schema 和 limits 重建 `ContextBuildConfig`，要求其 canonical hash 同时等于 Package 与 Trace hash。package ID 的既有 payload 不变。

### H1-03: 注入依赖可伪造 ContextConstructionError 或携带自定义 code

**发现**：Resolver、EnvelopeFactory 或 renderer 抛出的 `ContextConstructionError` 曾因类型相同而被信任，且合法类别中的自定义 error code 可能穿越边界。

**风险**：不可信依赖可影响外部错误分类，或把正文片段、内部 code 伪装成系统错误的一部分。

**修复**：在三个依赖边界分别使用 allowlist 重建固定脱敏错误。仅 Builder 自身产生的 `ContextConstructionError` 保持 canonical；依赖抛出的同名错误与未知错误统一重建为 `ContextConstructionRuntimeError`，并通过 `raise ... from error` 保留内部 cause。

### H1-04: Structural abstention 原因可与 Trace 情景错配

**发现**：空检索、instruction 超预算和首个候选不适配三种 abstention reason 曾只检查“有一个 reason”，没有检查 reason 是否由 Trace 支持。

**风险**：审计者可能把预算失败误读为空检索，或把未访问后续正文的 cutoff 情景误归类。

**修复**：Package 在身份校验时把三种 reason 与各自的 Trace 情景一一绑定；任一交叉组合 fail closed。

## 3. TDD 与验证

- 先加入 malformed Trace、config mutation、reason/trace mismatch 和 injected dependency error 的失败测试，再实现最小修复。
- 定向回归：`24 passed`。
- Stage 6 离线测试、架构测试与 label-isolation：`437 passed, 2796 subtests passed`。
- Ruff：通过；scoped MyPy：通过。
- 本轮未读取或修改 Stage 6 fixture/data，未修改 Stage 1-5，未调用 Embedding、Chroma、Groq 或 LLM，未执行正式 RAG 安全实验。
- 验证留痕：首次 runtime Git-ignore 检查把 PowerShell 的“无输出”误当作布尔失败；按 `$LASTEXITCODE` 复核后，`.gitignore` 的 `runtime/stage6_rag_security/` 规则已正确覆盖 Chroma 运行时探针，无需修改忽略规则。

## 4. 结论边界

可说明：当前 synthetic/offline 工程对象能拒绝上述四类不一致或错误穿透情形。

不可说明：检索质量、Citation Accuracy、RAG 安全效果、知识污染防护、可信检索或生产可用性已得到证明。

## 5. 教学与面试提示

**我现在做什么**：把“Trace 是一个可审计的执行证明”落实为数据不变量，而不是只保存若干统计数字。

**为什么企业需要它**：安全审计不仅要知道最终 Context 包含什么，还要能证明哪些候选为何未被读取，避免将不可信依赖的异常语义当成系统事实。

**与上一阶段的关系**：S6-T5.4 控制单条正文解析，S6-T5.5 固定单条证据渲染边界，I1 将多条证据组合为 Package；H1 只加固 I1 的一致性和错误边界，不增加新的 RAG 功能。

**面试追问**：为什么不只校验 Trace 的 UID 集合？回答：集合相同不代表构建顺序相同；稳定前缀算法还需要证明 resolved、included、budget excluded 和 cutoff 的时序关系。

**常见误解**：离线测试全绿不等于“模型不会被 prompt injection 攻击”。本轮没有模型调用，也没有正式攻击矩阵。
