# CodeGuarder 大模型安全评测项目

这是一个面向大模型安全岗位学习、实验复现和面试展示的项目。目标不是只运行工具，而是理解攻击构造、模型调用、风险检测、防护对照、失败分类和报告审计的完整流程。

## 已完成主线

1. Stage 1：garak Probe、Generator、Detector、Harness 与 Report。
2. Stage 2：OpenAI-compatible Mock API 与 vulnerable/guarded 对照。
3. Stage 3：Groq 真实模型安全扫描。
4. Stage 4：Guard Proxy 防护前后 A/B。
5. Stage 4.1：Input/Output Guard 四组消融。
6. Stage 5：六类攻击矩阵、T1–T9 Failure Taxonomy 和指标框架。
7. Stage 5 Paper：A1–A6 跨层模型、P/I/O/F、双检测器和确定性 AttemptRecord。

Stage 6 RAG 安全基线目前位于独立功能分支，暂未合入默认分支。

## 快速入口

- 项目目标、进度与路线图：`docs/project_context/`
- Stage 1–5 文件地图：`docs/git/REPOSITORY_MAP.md`
- 面试集中复习：`interview_prep/`
- 实验索引：`experiments/registry.json`
- Stage 1–4.1 代码：`llm-security-stage1/`
- Stage 5 论文级框架：`src/codeguarder/stage5_paper/`
- Stage 5 数据：`data/stage5_paper/`
- Stage 5 报告：`deliverables/stage5_paper/`
- 历史完整性：`provenance/historical_baseline.sha256`

## 结论纪律

Mock 结果用于验证机制和可复现性，真实 API 结果用于观察特定模型行为。PASS 不等于绝对安全，FAIL 不等于程序失败。所有结论都限定在当前模型、攻击矩阵、Guard 规则和 Detector 下。

历史产物不移动、不覆盖。确认历史错误时必须新增 correction log。
