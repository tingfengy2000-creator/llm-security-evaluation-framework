# Stage 5：Attack Matrix 与 Failure Taxonomy

目标：把个案扫描扩展为“攻击类别 × Guard 模式 × 指标 × 失败类型”的可审计评测。

- 学习顺序：[Stage 5 总览](../../deliverables/stage5/00_stage5_overview.md) → 攻击矩阵 → failure taxonomy；
- 代码：[Stage 5 源码](../../src/codeguarder/)；
- 数据：[攻击集](../../data/stage5/attacks/) 与 [benign 集](../../data/stage5/benign/)；
- 安全复跑：`powershell.exe -ExecutionPolicy Bypass -File .\scripts\run_stage5_smoke.ps1`；
- 原始证据：[Stage 5 交付物](../../deliverables/stage5/)；
- 结论边界：当前主结果是确定性 Mock 回归，不能外推为真实模型安全结论；
- 面试重点：T1–T9、Detector Miss、Guard Bypass、Over-block 与 parity validator。
