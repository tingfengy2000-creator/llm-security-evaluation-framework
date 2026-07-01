# Stage 5 Paper 总览

## 本阶段目标

建立 Training、Retrieval、Runtime 三层攻击模型，使用 A1-A6、P/I/O/F、双 detector
和 T1-T9 形成论文级评测框架。

## 为什么这样设计

攻击来源、防护位置、检测器和失败原因必须分层，否则单一 ASR 无法解释系统边界。

## 和上一阶段的关系

Stage 5 已验证矩阵框架；本阶段新增真实 HTTP Proxy、官方 garak detector、稳定
AttemptRecord 和可重复 canonical log。

## 当前结论边界

A1/A2 是训练层风险的运行时表现模拟，不是真实训练投毒。真实 Groq 尚未在本阶段运行。

## 面试时怎么讲

我把评测从 prompt 列表升级为跨层威胁模型和可审计实验系统。

## 不能夸大的地方

smoke 数据不能代表生产流量，rule-based baseline 不是生产级纵深防护。
