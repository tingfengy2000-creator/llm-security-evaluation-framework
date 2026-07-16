# Stage 4：Guard Proxy 真实 A/B

## Metadata

- stage_id: `S4`
- canonical_name: `Guard Proxy A/B Evaluation`
- canonical_slug: `stage4_guard_ab`
- legacy_paths: 无；slug 已规范。
- status: `completed`
- objective: 在同一代理链比较无防护与规则防护。
- source_locations: `llm-security-stage1/scripts/guard_proxy.py`
- data_locations: Stage 3 同一小样本 probe。
- test_locations: `llm-security-stage1/tests/test_guard_proxy.py`
- script_locations: `llm-security-stage1/scripts/run_stage4_guarded_scan.ps1`
- deliverable_locations: `deliverables/stage4/`
- evidence_locations: `deliverables/stage4/guarded_groq_scan_result.json`
- conclusion_boundary: rule-based、小样本 A/B。
- next_stage: `S4.1 stage4_1_guard_ablation`

目标：使用同一条 OpenAI-compatible 代理链，比较无防护与规则防护的攻击结果。

- 学习顺序：[Stage 4 总览](../../deliverables/stage4/00_stage4_overview.md) → 代理设计 → 输入输出规则；
- 代码：[Guard Proxy](../../llm-security-stage1/scripts/guard_proxy.py) 与 [编排脚本](../../llm-security-stage1/scripts/run_stage4_guarded_scan.ps1)；
- 数据：与 Stage 3 相同的小样本 probe；
- 复跑入口：`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\llm-security-stage1\scripts\run_stage4_guarded_scan.ps1 -ModelName llama-3.1-8b-instant`；
- 原始证据：[Stage 4 交付物](../../deliverables/stage4/)；
- 结论边界：这是 rule-based baseline 与小样本真实 A/B，不能称为生产防护率；
- 面试重点：解释 prompt parity、upstream call、输入侧节省成本与输出侧兜底。
