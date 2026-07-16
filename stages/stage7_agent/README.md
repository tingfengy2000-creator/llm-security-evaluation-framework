# Stage 7：Agent 安全（规划）

目标：在不执行真实破坏性工具的前提下，研究检索证据如何影响 Agent 的工具意图、记忆、计划与副作用风险。

- 前置学习：完成 Stage 5 的 T1–T9 和 Stage 6 的 RetrievalEvidence/TrustedContextPackage；
- 代码：尚未创建；未来只写入 `src/codeguarder/domains/agent/`；
- 数据：尚未创建；仅使用沙箱和 intent-only 工具样本；
- 运行命令：尚未提供，不能把规划写成已实现实验；
- 证据：暂无运行结果；
- 结论边界：Stage 7 不可直接访问 Chroma、Ground Truth、完整语料或 Guard 内部状态；
- 面试重点：解释跨层传播、最小权限、工具副作用隔离，以及为什么 RAG 安全是 Agent 安全的输入前提。
