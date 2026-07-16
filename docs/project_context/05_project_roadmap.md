# 项目后续路线图

更新时间：2026-07-16。

## 当前策略

当前优先级是先把 Stage 1–5 的代码、实验记录、学习文档和 GitHub 导航整理成稳定基线。Stage 6 保留在独立功能分支中，暂缓扩大实现范围；暂停不等于删除，已经完成的设计、契约和测试继续保留。

## P0：Stage 1–5 Git 同步与证据治理

状态：本轮执行。

完成标准：

- 本地与 `origin/main` 的 Stage 1–5 已跟踪文件一致；
- GitHub 首页能找到各阶段代码、数据、测试和报告；
- 虚拟环境、缓存、临时文件和凭据不进入仓库；
- `experiments/registry.json` 能反映已完成、Mock 和规划状态；
- 通过 Git preflight、秘密检查和历史完整性测试。

## P1：Stage 1–5 教学闭环

目标：把“做过实验”提升为“能够独立讲清楚并复现”。

计划：

1. 补齐 Stage 1 面试章节和各阶段学习状态表；
2. 为 Stage 2–4.1 各整理一个请求级案例，包括 prompt、模型行为、Detector、Guard 日志和结论；
3. 统一 ASR、Detector Miss、Guard Bypass、Over-blocking 等指标口径；
4. 更新 `interview_prep/` 的 30 秒、1 分钟和 3 分钟话术；
5. 建立面试前一键复习索引，不复制大量原始日志。

## P2：Stage 5 真实模型验证

目标：在确定性 Mock 框架稳定后，用严格受控的小样本验证真实模型路径。

前置条件：

- 固定数据集 manifest、模型名、seed 和生成参数；
- 明确 garak detector 与自定义 pattern detector 的判定差异；
- 免费 API 并发为 1，具备限流、重试和失败恢复记录；
- 输出严格脱敏并通过 no-secret-leak validator。

完成后仍只能表述为：在当前攻击矩阵、模型版本、Guard 规则和 Detector 下的实验结果。

## P3：恢复 Stage 6 RAG 基线

恢复时从 `feature/stage6-rag` 继续，不重新设计核心架构。顺序为：

1. 提交当前 Attack Matrix 与标签隔离加固；
2. 实现 SentenceTransformers Embedding 和 Persistent ChromaDB；
3. 实现 Retriever、ContextBuilder 与无标签泄露测试；
4. 实现 EvidenceSignal、pass-through TrustAggregator 和 `off/observe` Policy；
5. 实现确定性 Mock LLM、T10–T15、指标和报告；
6. Mock 回归稳定后，再运行 Groq 小样本。

## P4：Stage 6.1 与 Stage 7

- Stage 6.1：隐蔽知识污染检测、多证据可信评分、来源可信度和冲突感知检索。
- Stage 7：Agent Prompt/Tool/Memory/Planning 安全评测，只执行意图模拟，不执行真实危险工具。
- 两个阶段都必须复用 Stage 6 的 `RetrievalEvidence` 与脱敏审计契约，不反向破坏旧阶段。

## 版本节奏

- 每个阶段使用独立功能分支；
- 每个可验证 Task 使用小提交；
- 合并前运行测试、静态检查、秘密扫描和 Git preflight；
- 合并后更新实验注册表、进度页、学习笔记和面试材料；
- 真实实验使用独立 `run_id`，不覆盖历史结果。
