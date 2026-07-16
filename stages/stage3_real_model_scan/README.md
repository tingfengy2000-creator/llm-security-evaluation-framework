# Stage 3：Groq 真实 API 安全评测

## Metadata

- stage_id: `S3`
- canonical_name: `Real Model Security Scan`
- canonical_slug: `stage3_real_model_scan`
- legacy_paths: `stages/stage3_groq/`
- status: `completed`
- objective: 通过 OpenAI-compatible API 评测真实模型。
- source_locations: `llm-security-stage1/scripts/`
- data_locations: garak 的 PromptInject 与 Base64 probe。
- test_locations: `llm-security-stage1/tests/test_stage3_scripts.ps1`
- script_locations: `llm-security-stage1/scripts/run_stage3_groq_scan_safe.ps1`
- deliverable_locations: `deliverables/stage3/`
- evidence_locations: `deliverables/stage3/groq_scan_result.json`
- conclusion_boundary: 仅代表当时模型、参数与 detector。
- next_stage: `S4 stage4_guard_ab`

目标：理解 garak 如何经 OpenAI-compatible API 评测真实模型，并正确解释 PASS/FAIL。

- 学习顺序：[Stage 3 总览](../../deliverables/stage3/00_stage3_overview.md) → API 设置 → probe → 结果；
- 代码：[Stage 3 脚本](../../llm-security-stage1/scripts/run_stage3_groq_scan.ps1)；
- 数据：garak 的 `promptinject.HijackHateHumans` 与 `encoding.InjectBase64`；
- 安全复跑：`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\llm-security-stage1\scripts\run_stage3_groq_scan_safe.ps1 -ModelName llama-3.1-8b-instant`；
- 原始证据：[Stage 3 交付物](../../deliverables/stage3/)；
- 结论边界：结果只属于当时的模型、probe、参数和 Detector；Key 仅从环境变量读取；
- 面试复习：[Stage 3 面试要点](../../deliverables/stage3/07_interview_talking_points.md)。
