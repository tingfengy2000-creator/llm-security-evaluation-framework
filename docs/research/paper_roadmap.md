# 论文路线图

## 基线与创新分离

Stage 6 是可复现的 RAG Security Baseline：数据管线、攻击管线、透明基线、指标、评估协议和审计机制。它不是论文创新本身。

## 论文一：中文隐蔽知识污染基准与多视角检测

建议题目：**面向中文检索增强生成系统的隐蔽知识污染基准与多视角检测方法**。

研究问题：如何在不向运行时泄露 poison label 的前提下，识别中文语境中主题贴合、局部正确、来源可伪装的隐蔽知识污染？

预期方法：R5 子类型、stealth_level、多视角 EvidenceSignal、规则基线、传统机器学习、深度模型、解释性与跨数据集迁移。

核心指标：Precision、Recall、F1、AUROC、AUPRC、按 stealth_level 分层结果、迁移性能与误报成本。

## 论文二：面向污染风险的多证据可信检索与鲁棒聚合

建议题目：**面向污染风险的多证据可信检索与鲁棒聚合方法**。

研究问题：如何同时利用相关性、来源可靠性、冲突、时效性和风险，减少污染传播并维持正常检索效用？

预期方法：TrustAggregator、冲突感知重排、风险过滤、可信证据子集、鲁棒聚合和低置信度拒答。

核心指标：Retrieval Poison Rate、Poisoned@K、RMSR、Cross-layer Propagation、Recall@K、MRR、NDCG@K、Safety-Utility-Efficiency Trade-off、Trust Calibration。

## 论文实验纪律

- 使用明确的训练/验证/测试划分；
- 多模型、多语料、多种子重复；
- 规则基线、传统 ML、深度模型和消融并列；
- Faithfulness、Answer Correctness、Citation Accuracy、Evidence Consistency、Evidence Trustworthiness 分开报告；
- LLM-as-a-Judge 只作辅助轨道，不覆盖确定性主指标；
- 不把 Mock 回归或小样本 Groq 结果写成统计显著的真实模型结论；
- 提供数据卡、模型卡、配置、manifest 与可复现 Artifact。
