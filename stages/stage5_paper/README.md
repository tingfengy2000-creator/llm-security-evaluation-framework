# Stage 5 Paper：确定性研究级评测框架

目标：沉淀可复现 AttemptRecord、双 Detector、P/I/O/F 与审计报告能力。

- 学习顺序：先完成 Stage 5，再读 [Stage 5 Paper 源码](../../src/codeguarder/stage5_paper/)；
- 代码：[stage5_paper](../../src/codeguarder/stage5_paper/)；
- 数据：复用 Stage 5 透明合成数据；
- 复跑入口：以 [Stage 5 脚本目录](../../scripts/) 中对应 smoke/regression 脚本为准；
- 原始证据：[Stage 5 Paper 交付物](../../deliverables/stage5_paper/)；
- 结论边界：论文级指的是契约、可重复性和审计设计，不代表已完成真实模型全矩阵；
- 面试重点：为什么 Dataset Runner 不等于 garak scheduler，为什么 detector source 必须可追溯。
