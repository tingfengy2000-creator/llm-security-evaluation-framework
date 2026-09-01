# Paper 1 Document Inventory

Document Role = `PAPER1_DOCUMENT_INVENTORY`
Task = `GOV-P1-HUMAN-DOCS-INTEGRATION-01`
Snapshot Date = `2026-09-01`
Movement Policy = `LOGICAL_NAVIGATION_ONLY / NO_FILES_MOVED`

本清单用于解释现有文件的职责与推荐阅读位置，不改变任何文件的权威等级。`incoming links` 是本任务修改前按仓库内
Markdown 文件名引用得到的审计快照，只用于判断移动风险，不是永久稳定标识。

| path | role | authority | current / historical | layer | incoming links | recommended location |
| --- | --- | --- | --- | --- | ---: | --- |
| `README.md` | Paper 1 路由页 | navigation | current | human + agent | 21 | keep root |
| `human/experiment_ledger_tingfeng.md` | 人类可读总规划与总账 | primary human entry | current | human | 4 | keep protected path |
| `human/research_plan_authority.md` | 当前研究方案 | research authority | current | research/protocol | 9 | keep protected path |
| `human/owner_requirement_register.md` | Owner 明确需求登记 | owner authority | append-only current | governance | 3 | keep protected path |
| `human/annotation_lessons_learned_and_future_dataset_rules.md` | 未来数据与标注规则 | canonical rule | current | research/protocol | 5 | keep protected path |
| `agent/experiment_ledger_agentUse.md` | 机器结构化总账 | derived structured ledger | current | agent | 3 | keep protected path |
| `agent/llm_context_archive.md` | 上下文 capsule | derived recovery archive | append-only | agent | 2 | keep agent |
| `documentation_separation_contract.md` | 人类/机器/证据分层合同 | documentation governance | current | governance | 0 | keep root |
| `document_inventory.md` | 文档职责清单 | navigation audit | current | governance | 0 | keep root |
| `stage_process/S6.1-LR1_work_process.md` | LR1 追加式过程 | stage canonical | historical closed | evidence/audit | 3 | keep protected stage_process |
| `stage_process/S6.1-R0_work_process.md` | R0 追加式过程 | stage canonical | historical closed | evidence/audit | 3 | keep protected stage_process |
| `stage_process/S6.1-R0-FU1_work_process.md` | FU1 追加式过程 | stage canonical | historical closed | evidence/audit | 5 | keep protected stage_process |
| `stage_process/S6.1-P1_work_process.md` | P1/Pilot 追加式过程 | stage canonical | current | evidence/audit | 4 | keep protected stage_process |
| `s6_1_p1_r1_protocol_review_candidate.md` | P1-R1 协议来源候选 | accepted framework source; numeric freeze pending | current framework | research/protocol | 9 | keep root due high links |
| `s6_1_p1_protocol_candidate.md` | 旧 P1 协议候选 | non-canonical | historical/superseded | research/protocol | 10 | keep root; classify historical |
| `paper1_research_route.md` | 早期研究路线 | supporting only | historical | human/research | 8 | keep root; classify historical |
| `paper1_benchmark_alignment_matrix.md` | 基线/Benchmark 对齐 | supporting research | current reference | research/protocol | 3 | keep root |
| `s6_1_p1_pilot2_return_owner_correction.md` | Pilot2 顺序纠正 | owner evidence summary | historical resolved | evidence/audit | 4 | keep root |
| `s6_1_p1_pilot2_annotation_v2.md` | Schema V2 记录 | task record | historical closed | evidence/audit | 5 | keep root |
| `s6_1_p1_pilot2_targeted_rereview.md` | 定向复核记录 | task record | historical closed | evidence/audit | 4 | keep root |
| `s6_1_p1_pilot2_post_annotation.md` | Return/agreement 记录 | task record | historical closed | evidence/audit | 4 | keep root |
| `s6_1_p1_pilot2_adjudication_closure.md` | 仲裁阻塞记录 | task record | historical resolved | evidence/audit | 4 | keep root |
| `s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md` | Pilot2 closure/Pilot3 诊断 | task record | historical closed | evidence/audit | 5 | keep root |
| `learning_notes.md` | 可复用研究/工程教训 | supporting | append-only current | human/research | 15 | keep root due high links |
| `baseline_reproduction_protocol.md` | Baseline 复现边界 | protocol | historical reference | research/protocol | 3 | keep root |
| `external_artifact_registry.md` | 外部工件身份 | artifact registry | current reference | evidence/audit | 3 | keep root |
| `hardware_execution_policy.md` | 本机/5090 边界 | execution policy | current | governance | 2 | keep root |
| `s6_1_r0_reproduction_preflight.md` | R0 预检 | task evidence summary | historical | evidence/audit | 2 | keep root |
| `s6_1_r0_i_control_plane_review.md` | R0-I 控制面复核 | task evidence summary | historical | evidence/audit | 7 | keep root |
| `s6_1_r0_fu1_targeted_resolution.md` | FU1 定向解决 | task evidence summary | historical | evidence/audit | 10 | keep root due high links |
| `s6_1_r0_fu1_w2_attempt1_control_plane_review.md` | W2 Attempt1 复核 | task evidence summary | historical | evidence/audit | 5 | keep root |
| `s6_1_r0_fu1_w2_h2_resume02_control_plane_review.md` | W2 H2 resume02 复核 | accepted engineering evidence summary | historical closed | evidence/audit | 5 | keep root |

## Inventory decision

- 受保护路径全部保持不变。
- 高链接密度历史文件不移动，以 README 分类和显式 `historical/superseded` 标签降低歧义。
- raw JSON/JSONL/log/XLSX/hash/manifest 保持 Git-external 或原治理位置，不进入人类主入口。
- 以后若移动低风险文件，必须先证明 `git mv`、全部 incoming links 自动更新、Markdown link validator 通过且语义不变。
