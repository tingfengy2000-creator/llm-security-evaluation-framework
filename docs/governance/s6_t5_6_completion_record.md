# S6-T5.6-I1 最小离线 Context Package 完成记录

## 1. 记录身份

- Task ID: `S6-T5.6-I1`
- Task name: `Deterministic Retrieved Context Package Minimal Offline Implementation`
- Task nature: `OFFLINE_ENGINEERING_IMPLEMENTATION / SYNTHETIC_ONLY_TDD`
- Current status: `HUMAN_ACCEPTED`
- Parent task: `S6-T5.6: HUMAN_ACCEPTED`
- Initial candidate implementation: `71067d1`
- Final accepted implementation commit: `b136ee2`
- Previous last accepted implementation commit: `6da27a6`

本记录起初登记的是候选工程实现（`candidate implementation pending human acceptance`），不是人工验收；该历史快照
保留。随后 `GOV-S6-T5.6-ACCEPTANCE` 已接受 I1、I1-H1 与父任务，当前状态以本文件末尾的最终验收附注为准。
也不是正式 RAG 安全实验记录。

## 2. 本轮实现范围

实现位于规范 namespace `src/llmguard/domains/retrieval/`：

- `contracts/context_package.py`：冻结的 ContextBuildConfig、ContextBuildTrace、RetrievedContextPackage。
- `contracts/errors.py`：最小 Context construction 脱敏错误层级。
- `context/budget.py`：以最终渲染字符串 Unicode code point 数判断预算。
- `context/builder.py`：唯一 DeterministicContextBuilder。

构建器只使用 synthetic Request、Evidence 与注入式 in-memory Resolver。它先校验 provenance，稳定排序并精确 UID 去重，
应用数量限制和 instruction，再按候选顺序 resolve -> factory -> temporary Binding -> render -> final budget 判断。
首个不适配候选触发 stable-prefix cutoff；后续候选不读取正文、不调用 Factory 或 renderer。

## 3. 已验证的边界

- Context 配置、Trace 与 Package 的 canonical SHA-256 身份可复算。
- Trace 对每个稳定候选给出唯一且完整的决策分区。
- Package 的 Citation 连续为 `E1...En`，仅在候选实际 fit 后提交。
- 空检索、instruction 超预算、首个完整 block 不适配三类 structural abstention 返回空 context，且不会伪装为 integrity failure。
- request/query、collection、snapshot、重复 UID 冲突和依赖异常均 fail closed；普通公开错误文本不回显正文、Query、ContentRef 或 metadata。
- 普通 `repr()` 与 `to_audit_dict()` 不包含正文、rendered context、Query、ContentRef 或标签；`dataclasses.asdict()` 被明确视为敏感操作。

## 4. 验证与结论边界

测试数据全部是代码内构造的 synthetic 对象。未读取或修改 Stage 6 fixture/data，未调用 Embedding、Chroma、Groq 或 LLM，
未实现 Trust、RetrievalPolicy、reranker、Citation Accuracy、模型生成或正式 RAG 攻击矩阵。

本轮验证结果：

- 最终完整 Stage 6 离线回归：`438 passed, 2837 subtests passed`。
- 治理、namespace、标签隔离和实验总账定向回归：`31 passed, 1548 subtests passed`。
- Context 与架构定向回归：`221 passed, 841 subtests passed`。
- Ruff：通过；scoped MyPy：`Success: no issues found in 45 source files`。
- 变更文件 Markdown 相对链接、secret-shape、绝对路径、protected-path、runtime Git-ignore 与 `git diff --check`：通过。

实施过程中发现并关闭两类工程问题：第一，历史治理测试仍将 I1 写成“未批准/实施中”；本轮将其改为只断言当前
`Completed, pending human acceptance`，同时保留旧协议快照。第二，MyPy 指出 Trace 动态 tuple 输入、Package identity
payload 和 RetrievalEvidence 的受控 `ContentRef` 之间缺少静态类型收窄；实现已改为显式可迭代验证、显式 identity
参数和 `ContentRef` 转换，并由回归、Ruff 与 MyPy 共同验证。

因此本轮只能说明：在当前离线合约和测试覆盖范围内，Context Package 的组合、审计与失败边界可重复验证。
不能说明：检索质量、RAG 安全效果、知识污染防护、可信检索、Citation Accuracy、生产可用性或正式实验结论。

## 5. 后续人工决策

## 最终人工验收附注（2026-07-26）

`GOV-S6-T5.6-ACCEPTANCE` 已将 `S6-T5.6-I1`、`S6-T5.6-I1-H1` 与父任务 `S6-T5.6` 标记为
`HUMAN_ACCEPTED`。`71067d1` 保留为初始 candidate implementation history，最终接受的实现提交为 `b136ee2`；
`6da27a6` 保留为此前已接受实现提交的历史事实。

最终完整 Stage 6 离线回归为 `438 passed, 2837 subtests passed`。此前 `421 passed, 2796 subtests passed`、
`437 passed, 2796 subtests passed` 与 `438 passed, 2833 subtests passed` 是最终复跑之前的历史验证快照；`2833` 到
`2837` 的差异来自验收状态同步时新增的四个治理子断言，不再作为当前最终验收数字。

`S6-T5.7+` 仍为 `NOT APPROVED`，Formal RAG security experiment 仍为 `NOT STARTED`；本验收不得自动开启下一任务。
