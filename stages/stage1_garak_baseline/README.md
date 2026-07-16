# Stage 1：garak 最小安全扫描

## Metadata

- stage_id: `S1`
- canonical_name: `Garak Security Scan Baseline`
- canonical_slug: `stage1_garak_baseline`
- legacy_paths: `stages/stage1_garak/`
- status: `completed`
- objective: 学习 garak 的最小评测闭环。
- source_locations: `llm-security-stage1/scripts/`
- data_locations: garak 内置 probe。
- test_locations: `llm-security-stage1/tests/`
- script_locations: `llm-security-stage1/scripts/run_stage1_scan.ps1`
- deliverable_locations: `deliverables/stage1/`、`deliverables/stage1_learning/`
- evidence_locations: `deliverables/stage1/garak_scan_result.json`
- conclusion_boundary: 脆弱 Mock 只证明扫描机制。
- next_stage: `S2 stage2_openai_mock_api`

目标：理解 `Probe → Generator → Model → Detector → Evaluator → Report` 的最小闭环。

- 学习顺序：[学习路线](../../deliverables/stage1_learning/00_learning_path.md) → 架构说明 → 首次扫描分析；
- 代码：[历史脚本](../../llm-security-stage1/scripts/)；
- 数据：本阶段使用 garak probe，不新增自建攻击数据集；
- 复跑入口：`powershell.exe -ExecutionPolicy Bypass -File .\llm-security-stage1\scripts\run_stage1_scan.ps1`；
- 原始证据：[Stage 1 交付物](../../deliverables/stage1/)；
- 结论边界：脆弱 Mock 的高 ASR 只证明扫描链路和 Detector 判定；
- 面试复习：[Stage 1 面试讲解](../../deliverables/stage1_learning/05_stage1_interview.md)。
