# LLMGuard 与教育厅立项项目对齐说明

## 依据与边界

本说明依据《面向检索增强生成系统的隐蔽知识污染检测与可信检索关键技术研究》立项申报书整理。该申报书是研究路线依据，不是 LLMGuard 已完成成果证明；文档不复述申报书中的个人信息、联系方式或单位信息。

立项项目计划完成时间为 2028 年 12 月，研究主线为：隐蔽污染威胁建模、中文基准构建、多视角检测、风险感知可信检索、鲁棒证据聚合和原型系统评测。

## 对齐矩阵

| 立项研究内容 | LLMGuard 对应模块 | 当前状态 | 后续成果边界 |
| --- | --- | --- | --- |
| 知识污染威胁建模与数据集 | R1–R6、R5 子类型、CorpusSnapshot、PoisonBuilder | R1–R6 小型透明合成数据已完成 | Stage 6.1 中文基准、标注协议、stealth_level 与数据划分 |
| 隐蔽知识污染检测 | EvidenceSignal、来源/版本/实体/语义/Embedding/行为信号 | 仅完成信号契约预留 | Stage 6.1 规则、ML、深度检测与迁移实验 |
| 多证据可信检索 | TrustAggregator、RetrievalPolicy、可信子集与鲁棒聚合 | 尚未实现 | Stage 6B 透明基线；Stage 6.2 研究方法 |
| 原型系统与评测 | Runner、Experiment Config、Metrics、Reports、Artifact | Stage 5 有确定性评测基础 | Stage 6C 全链路 RAG 原型与受控真实模型 smoke |

## 技术路线映射

```text
立项：威胁数据建模
  → LLMGuard：R1–R6、R5 隐蔽污染子类型、CorpusSnapshot
立项：多视角检测
  → LLMGuard：EvidenceSignal 与 no-label-leakage
立项：可信检索与鲁棒聚合
  → LLMGuard：TrustAggregator + RetrievalPolicy
立项：原型与综合验证
  → LLMGuard：RAG Runner + E0–E5 实验轨道 + 审计报告
```

## 申报书研究计划与项目路线

- 2027 上半年：污染类型、数据预处理和规范，对应 Stage 6.1 数据基准准备；
- 2027 下半年：多视角检测与消融，对应 Stage 6.1 检测方法；
- 2028 上半年：可信检索优化与模块融合，对应 Stage 6B/6.2；
- 2028 下半年：原型、对比实验、论文与软著，对应 Stage 6C、公开 Artifact 和收敛报告。

## 共同约束

- 只使用公开或合成、受控数据；
- 不对生产系统进行未授权攻击；
- 污染样本隔离存储，不进入公开运行日志；
- Ground Truth 只允许 Vault 与 Evaluator 访问；
- 第三方数据、模型和工具遵守许可证；
- 安全、检索效用与运行成本必须同时评估。

## 当前不能写成已完成的内容

LLMGuard 尚未完成中文隐蔽污染基准、联合检测模型、可信重排、鲁棒聚合、跨数据集迁移、真实大规模评测或立项预期论文/软著成果。现有 Stage 1–5 是立项书所述“实验与工程基础”的补充证据，不等同于申报书中团队全部既有成果。
