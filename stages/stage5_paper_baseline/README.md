# Stage 5 Paper：确定性研究级评测框架

## Metadata

- stage_id: `S5P`
- canonical_name: `Deterministic Runtime Evaluation Baseline`
- canonical_slug: `stage5_paper_baseline`
- legacy_paths: `stages/stage5_paper/`
- status: `completed_mock`
- objective: 沉淀确定性 AttemptRecord、双 detector 和审计报告。
- source_locations: `src/codeguarder/stage5_paper/`（受保护历史实现）
- data_locations: `data/stage5_paper/`
- test_locations: `tests/stage5_paper/`
- script_locations: `scripts/run_stage5_paper_smoke.ps1`
- deliverable_locations: `deliverables/stage5_paper/`
- evidence_locations: `deliverables/stage5_paper/`
- conclusion_boundary: 论文级契约不等于真实模型全矩阵。
- next_stage: `S6 stage6_rag_security`

目标：沉淀可复现 AttemptRecord、双 Detector、P/I/O/F 与审计报告能力。

- 学习顺序：先完成 Stage 5，再读 [Stage 5 Paper 源码](../../src/codeguarder/stage5_paper/)；
- 代码：[stage5_paper](../../src/codeguarder/stage5_paper/)；
- 数据：复用 Stage 5 透明合成数据；
- 复跑入口：以 [Stage 5 脚本目录](../../scripts/) 中对应 smoke/regression 脚本为准；
- 原始证据：[Stage 5 Paper 交付物](../../deliverables/stage5_paper/)；
- 结论边界：论文级指的是契约、可重复性和审计设计，不代表已完成真实模型全矩阵；
- 面试重点：为什么 Dataset Runner 不等于 garak scheduler，为什么 detector source 必须可追溯。
