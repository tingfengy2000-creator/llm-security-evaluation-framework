# 面试话术

## 本阶段目标

用 30 秒、1 分钟和追问回答解释研究设计。

## 为什么这样设计

面试官关注控制变量、分母、detector 来源、误拦和可复现性。

## 和上一阶段的关系

从“跑通 garak”递进到“独立设计跨层评测框架”。

## 当前结论边界

真实 Stage 5 Paper Groq 实验尚未运行。

## 面试时怎么讲

30 秒：我用 Dataset Runner、OpenAI-compatible Guard Proxy、双 detector 和 T1-T9，
对 A1-A6 运行 P/I/O/F 四模式，并通过 canonical log 保证离线复现。

1 分钟：官方 garak detector 只负责适用输出，自定义 pattern 作为合成 oracle；
O 模式必须先调用模型、保存 raw hash，再执行 Output Guard。指标同时覆盖安全、误拦、
调用成本和延迟。

## 不能夸大的地方

A1/A2 是 manifestation simulation，所有结论只适用于当前攻击矩阵和规则 baseline。
