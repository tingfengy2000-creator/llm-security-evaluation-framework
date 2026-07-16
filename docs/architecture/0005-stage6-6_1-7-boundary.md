# ADR 0005：Stage 6、Stage 6.1、Stage 6.2 与 Stage 7 边界

## 状态

已接受，2026-07-16。

| 阶段 | 定位 | 允许实现 | 不得宣称 |
| --- | --- | --- | --- |
| Stage 6A | 工程正确性基线 | Static Embedding、InMemoryStore、Mock、off/observe、schema/hash/parity | 论文算法或真实模型结论 |
| Stage 6B | 透明防护基线 | filter-baseline、rerank-baseline、WeightedRuleTrustAggregator、效用消融 | 学习型检测创新 |
| Stage 6C | 集成与复现基线 | 真实 Embedding、Chroma、Runner、报告、受控 Groq smoke、跨层实验 | 大规模真实模型统计结论 |
| Stage 6.1 | 论文一 | 中文隐蔽污染基准、多视角检测、难度与迁移实验 | Stage 6 已完成的能力 |
| Stage 6.2 | 论文二 | 多证据可信检索、鲁棒聚合、冲突感知重排、拒答 | 仅靠规则的生产防护率 |
| Stage 7 | Agent 扩展 | Tool/Memory/Planning 攻击、意图检测、风险传播 | 真实危险工具执行 |

## Stage 6 政策冻结

策略模式固定为 `off`、`observe`、`filter-baseline`、`rerank-baseline`、`research`。

- Stage 6A 只实现 `off`、`observe` 与 `PassThroughTrustAggregator`；二者排序和 context hash 必须一致。
- Stage 6B 增加透明、配置化、版本化、可关闭、可解释的规则型基线。
- Stage 6.1/6.2 以插件替换聚合器或策略，不重写 Runner。

## 研究重点映射

R5 `Document Poisoning` 是立项和论文核心入口，后续扩展 entity_attribute_corruption、temporal_shift、causal_inversion、source_impersonation、cross_document_conflict、partial_truth_composition、hidden_instruction、version_rollback、authority_spoofing。

Stage 6 只使用少量透明合成样本。Stage 6.1 才构建中文基准、标注协议、难度分级与训练/验证/测试划分。
