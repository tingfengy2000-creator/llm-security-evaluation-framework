# LLMGuard 大模型安全评测与可信检索研究框架

LLMGuard Research Framework（简称 LLMGuard）是面向可复现 LLM、RAG 与 Agent 安全评测的
研究框架。

LLMGuard Research Framework 是独立的大模型安全评测与可信检索研究项目，与 Protect AI 的
llm-guard 项目不存在隶属、继承或官方关联关系。

> 项目完整进度、架构重设计、论文与科技立项路线请先阅读：`PROJECT_MASTER_CONTEXT.md`。

本项目按 Stage 1 到 Stage 5 Paper 记录大模型安全评测学习过程，覆盖：

1. garak 的 Probe、Generator、Detector、Harness 与 Report；
2. OpenAI-compatible Mock API；
3. Groq 真实模型安全扫描；
4. Guard Proxy 防护前后 A/B；
5. Input/Output Guard 四组消融；
6. A1-A6 跨层攻击矩阵、T1-T9 Failure Taxonomy 和确定性日志。

## 快速入口

- 面试集中复习：`interview_prep/`
- 实验索引：`experiments/registry.json`
- 规范新源码：`src/llmguard/`
- 受保护的 Stage 5 Paper 历史源码：`src/codeguarder/stage5_paper/`
- 新实验数据：`data/stage5_paper/`
- 新实验报告：`deliverables/stage5_paper/`
- 历史完整性：`provenance/historical_baseline.sha256`

历史产物不移动、不覆盖。确认历史错误时必须新增 correction log。
