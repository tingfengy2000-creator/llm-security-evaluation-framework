# 实验结果

## 本阶段目标

记录 Stage 5 Paper 最新离线 run 和后续真实 run，不混用来源。

## 为什么这样设计

先验证框架再消耗真实 API，避免把工程错误当成模型行为。

## 和上一阶段的关系

本阶段沿用四模式对照，但按 A1-A6 与 threat layer 输出 heatmap。

## 当前结论边界

初始结果为 deterministic mock，真实 Groq 状态为 not run。

## 最新离线结果

- execution_id：`20260701T081320Z-c29f39`
- experiment fingerprint：`053cdf03de8feba242ce07fd8d948f4e9cd25dfbb47dd2a067a55db5a74ac625`
- 样本：22
- Attempt：88
- ASR：95.83%
- DMR：0.00%
- GBR：94.44%
- Detector Coverage：8.33%
- Over-block：0.00%
- T1=46、T2=0、T3=34、T4=0、T5=0、T6=4、T7=8、T8=8、T9=8

该 mock 被设计为复述合成风险标记，因此高 ASR 用于证明 taxonomy、Guard boundary 和
报告链能够观察失败。官方 detector coverage 低，说明多数 A1-A6 样本没有对应的
garak 官方 detector，不能把 DMR=0% 解读成 detector 全面可靠。

## 面试时怎么讲

离线 run 证明方法与报告链；真实 run 才用于模型行为讨论。

## 不能夸大的地方

mock 的 ASR 是故意构造的框架测试结果，不是模型安全结论。
