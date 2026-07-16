# Stage 5：Attack Matrix 与 Failure Taxonomy

## Metadata

- stage_id: `S5`
- canonical_name: `Runtime Attack Matrix and Failure Taxonomy`
- canonical_slug: `stage5_runtime_attack_matrix`
- legacy_paths: `stages/stage5_attack_matrix/`
- status: `completed_mock`
- objective: 建立攻击、Guard、指标与失败类型矩阵。
- source_locations: `src/codeguarder/`（受保护历史 Stage 5 实现）
- data_locations: `data/stage5/`
- test_locations: `tests/stage5/`
- script_locations: `scripts/run_stage5_smoke.ps1`
- deliverable_locations: `deliverables/stage5/`
- evidence_locations: `deliverables/stage5/attack_matrix_result.json`
- conclusion_boundary: 当前主结果是确定性 Mock 回归。
- next_stage: `S5P stage5_paper_baseline`

目标：把个案扫描扩展为“攻击类别 × Guard 模式 × 指标 × 失败类型”的可审计评测。

- 学习顺序：[Stage 5 总览](../../deliverables/stage5/00_stage5_overview.md) → 攻击矩阵 → failure taxonomy；
- 代码：[Stage 5 源码](../../src/codeguarder/)；
- 数据：[攻击集](../../data/stage5/attacks/) 与 [benign 集](../../data/stage5/benign/)；
- 安全复跑：`powershell.exe -ExecutionPolicy Bypass -File .\scripts\run_stage5_smoke.ps1`；
- 原始证据：[Stage 5 交付物](../../deliverables/stage5/)；
- 结论边界：当前主结果是确定性 Mock 回归，不能外推为真实模型安全结论；
- 面试重点：T1–T9、Detector Miss、Guard Bypass、Over-block 与 parity validator。
