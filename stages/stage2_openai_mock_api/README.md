# Stage 2：OpenAI-compatible Mock API

## Metadata

- stage_id: `S2`
- canonical_name: `OpenAI-Compatible Mock API`
- canonical_slug: `stage2_openai_mock_api`
- legacy_paths: `stages/stage2_mock_api/`
- status: `completed`
- objective: 用可控 Mock 分离 API 协议与模型随机性。
- source_locations: `llm-security-stage1/scripts/mock_openai_compatible_api.py`
- data_locations: `deliverables/stage2/`
- test_locations: `llm-security-stage1/tests/`
- script_locations: `llm-security-stage1/scripts/run_stage2_scan.ps1`
- deliverable_locations: `deliverables/stage2/`
- evidence_locations: `deliverables/stage2/stage2_scan_result.json`
- conclusion_boundary: Mock 不代表真实模型安全性。
- next_stage: `S3 stage3_real_model_scan`

目标：把评测工具与模型随机性分离，理解 vulnerable/guarded 对照。

- 学习顺序：先读 Stage 1，再阅读 [Stage 2 交付物](../../deliverables/stage2/)；
- 代码：[历史脚本与 Mock 服务](../../llm-security-stage1/scripts/)；
- 数据：[Stage 2 结果与说明](../../deliverables/stage2/)；
- 复跑入口：以 [Stage 2 命令记录](../../deliverables/stage2/) 为准；
- 原始证据：[deliverables/stage2](../../deliverables/stage2/)；
- 结论边界：Mock 用于控制变量和接口验证，不代表真实模型安全性；
- 面试重点：解释 OpenAI-compatible、`/v1/chat/completions` 与对照实验的价值。
