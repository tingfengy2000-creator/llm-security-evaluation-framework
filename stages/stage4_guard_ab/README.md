# Stage 4：Guard Proxy 真实 A/B

目标：使用同一条 OpenAI-compatible 代理链，比较无防护与规则防护的攻击结果。

- 学习顺序：[Stage 4 总览](../../deliverables/stage4/00_stage4_overview.md) → 代理设计 → 输入输出规则；
- 代码：[Guard Proxy](../../llm-security-stage1/scripts/guard_proxy.py) 与 [编排脚本](../../llm-security-stage1/scripts/run_stage4_guarded_scan.ps1)；
- 数据：与 Stage 3 相同的小样本 probe；
- 复跑入口：`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\llm-security-stage1\scripts\run_stage4_guarded_scan.ps1 -ModelName llama-3.1-8b-instant`；
- 原始证据：[Stage 4 交付物](../../deliverables/stage4/)；
- 结论边界：这是 rule-based baseline 与小样本真实 A/B，不能称为生产防护率；
- 面试重点：解释 prompt parity、upstream call、输入侧节省成本与输出侧兜底。
