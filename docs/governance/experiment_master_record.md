# LLMGuard 实验总记录、证据索引与项目交接入口

> 英文名：Experiment Master Record
>
> 文档性质：项目**唯一的实验控制面**、证据索引和汇总入口。
>
> 首次建立：2026-07-20。最近更新时间应通过本文件的 Git 历史解析；当前 branch、HEAD 和本文件自身提交均为动态 Git 事实，不在本文静态固化。

## 1. 文档元数据与使用说明

### 1.1 职责

本记录统一回答项目实验路线、运行、指标、证据、失败、阻塞项、审批门、结论边界和交接顺序。它是**控制面、索引和汇总入口，不是原始数据仓库，也不替代阶段产物**。

普通文档编辑、日常开发步骤和教学记录不得全部塞入本文；项目推进时间线进入
`research_execution_log.md`，当前任务状态进入 `current_work_state.md`。

- 不记录 API Key、Authorization、完整敏感输出、完整污染文档或本机绝对路径。
- 不覆盖 Stage 1–5 的历史 JSON/JSONL、HTML、日志、报告、数据或代码；历史勘误以新增条目留痕。
- 缺失事实统一写作 `NOT_RECORDED`；存在冲突写作 `REQUIRES_VERIFICATION`；不能用推测补齐。
- 维护人：项目负责人及获授权的维护者。
- 更新触发条件见“持续更新协议”；每次更新均要从原始证据回填，而非从教学材料反推。

### 1.2 文档职责矩阵

| 文档 | 主要职责 | 是否保存当前动态状态 | 是否保存原始实验数据 | 是否是实验总入口 |
| --- | --- | --- | --- | --- |
| [AGENTS.md](../../AGENTS.md) | Codex 启动、范围和完成协议 | 否 | 否 | 否 |
| [context_authority_map.md](context_authority_map.md) | 权威层级、冲突解决与恢复顺序 | 否 | 否 | 否 |
| [long_term_research_requirements.md](long_term_research_requirements.md) | 长期不可变研究要求 | 否 | 否 | 否 |
| [project_owner_decision_register.md](project_owner_decision_register.md) | Owner-confirmed decisions | 否 | 否 | 否 |
| [PROJECT_MASTER_CONTEXT.md](../../PROJECT_MASTER_CONTEXT.md) | 项目架构、路线和长期上下文 | 部分 | 否 | 否 |
| [current_work_state.md](current_work_state.md) | 当前任务与审批门 | 是 | 否 | 否 |
| `experiment_master_record.md` | 实验路线、运行、指标、证据、阻塞、交接 | 是，做动态索引 | 只做索引和汇总 | 是 |
| [research_execution_log.md](research_execution_log.md) | append-only 项目推进时间线 | 否 | 否 | 否 |
| [learning_notes.md](../../deliverables/learning_notes.md) | 教学过程、问题解释和学习反思 | 否 | 否 | 否 |
| [docs/learning](../learning/README.md) | 结构化 Stage Learning Guides | 否 | 否 | 否 |
| Stage-specific deliverables | 原始结果、日志、报告和阶段解释 | 否 | 是 | 否 |
| Run Manifest | 单次正式运行的机器可读事实 | 否 | 是 | 否 |

### 1.3 权威来源优先级

冲突时按以下顺序判断，不能为使表格“更好看”而改写低层证据：

1. 原始输出、日志和 Run Manifest；
2. 对应 Git commit；
3. Stage-specific 验收报告和结果摘要；
4. 本 Experiment Master Record 的索引和汇总；
5. 教学或面试材料。

## 2. 五分钟项目快照

| 项目 | 当前事实 |
| --- | --- |
| 总目标 | 建立从模型层安全评测、Guard 对照到 RAG 安全与可信检索、再到 Agent 安全的可复现研究框架。 |
| 当前最高完成阶段 | S6-T5 Controlled Retrieval and Traceable Context Baseline 已 `HUMAN_ACCEPTED BASELINE`；S6.1-LR1 与 Context Recovery Governance 已 `HUMAN_ACCEPTED`。 |
| 当前任务 | `PILOT4-EXTERNAL-BLIND-OWNER-REVIEW-PACKET-01 = EXTERNAL_LABEL_BLIND_REVIEW_PACKET_AND_TITLE_PROVENANCE`。 |
| 当前审批门 | 等待隔离的外部 GPT/Owner reviewer 返回 `blind_review_id + 11 fields + reasoning`；当前不得解锁 mapping 或加载 expected contract。 |
| 下一批准任务 | none automatically；A/B 72 annotation、240-group、Dataset、Formal Detector、Training 和 Formal Experiment remain closed。 |
| Baseline tag | annotated `s6-t5-rag-baseline-v1` 已恢复；本地/远端 peeled target 均核验为 `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`。 |
| 最近正式安全实验 | Stage 5 Paper Mock 确定性运行，`20260701T081320Z-c29f39`，88 attempts。 |
| 最近工程验证 | H2 resume_02 archive SHA/safety/index `25/25`, H2-A `18/18`, exact local-model CUDA load, single-call and resource evidence passed Control Plane review。 |
| 当前主要阻塞项 | External blind semantic review return pending；formal protocol numeric parameters、Scale Pilot、Dataset 和 method effectiveness 均未冻结。 |
| 当前允许宣称 | c1b/b705cc history preserved；72-row external packet、opaque IDs、isolated mapping、144/144 actual-title provenance and machine no-label-leakage QA passed；不代表语义可作答性、独立人工接受、Ground Truth 或 Detector effectiveness。 |
| 当前禁止宣称 | GMTP reproduction/effectiveness/safety/generalization、strict baseline comparison、P1/formal experiment or paper result。 |

历史审批快照补充：S6-T5.5/5.6/5.7 已按后续记录完成并通过相应人工验收；早期 pending/NOT APPROVED 文字保留为
时间点事实。当前 accepted implementation/integration identities 分别是 `b136ee2` 与 `b6cedf3`；LR1 不改变该 taxonomy。

正式 RAG 安全实验：**Not started**。Historical R0 execution/return snapshots and current R0 acceptance do not change this status。

**阅读入口**：先读 [AGENTS.md](../../AGENTS.md)、[Context Authority Map](context_authority_map.md)、
[PO-MHEP](project_owner_sovereignty_and_mandatory_escalation_principle.md)、[长期研究需求](long_term_research_requirements.md)、
[项目总控](../../PROJECT_MASTER_CONTEXT.md)、[当前任务状态](current_work_state.md)，再读本文、当前 Stage 设计与原始工件。

## 3. 总研究目标与研究问题

项目优先级固定为：

1. RAG Security Research；
2. LLM Security Evaluation Platform；
3. AI Guard Engineering；
4. Agent Security Extension。

长期研究问题包括：模型层攻击如何测量；Input/Output Guard 的独立贡献；Detector 漏报如何识别；知识污染如何影响检索和 Context；如何用可追溯 Evidence 进行多证据信任聚合；以及 RAG 风险如何传播到 Agent 决策。Stage 1–5 已对前两类问题给出当前配置下的实验性证据；Stage 6.1 已有 Pilot-level 数据/标注/信号诊断，但 Formal Detector 与正式效果仍未实现/建立；可信聚合和 Agent 传播仍为 `PLANNED_NOT_IMPLEMENTED`。

## 4. 项目阶段路线图

| Stage/Task | 正式名称 | 核心目标 | 当前状态 | 状态类型 | 关键提交/证据 | 下一门禁 |
| --- | --- | --- | --- | --- | --- | --- |
| GOV-PO-MHEP | Project Owner Sovereignty, Mandatory Human Escalation, and Physical Context Preservation Principle | highest internal execution authority、mandatory escalation、forward/paper risk and physical context preservation | human accepted；permanent；no auto expiry | `HIGHEST_INTERNAL_PROJECT_EXECUTION_AUTHORITY` | [PO-MHEP](project_owner_sovereignty_and_mandatory_escalation_principle.md)、PODR-056、REL-2026-0017 | applies to every future task；does not auto-approve execution |
| Stage 1 | Garak Security Scan Baseline | 跑通 Probe → Generator → Detector → Report | 完成 | `ENGINEERING_VALIDATED` | [Stage 1 结果](../../deliverables/stage1/) | 无 |
| Stage 2 | OpenAI-Compatible Mock API | vulnerable/guarded Mock 对照 | 完成 | `FORMAL_EXPERIMENT_COMPLETED` | [Stage 2 结果](../../deliverables/stage2/) | 无 |
| Stage 3 | Real Model Security Scan | Groq 真实模型小样本扫描 | 完成 | `FORMAL_EXPERIMENT_COMPLETED` | [Stage 3 结果](../../deliverables/stage3/) | 扩样需单独设计 |
| Stage 4 | Guard Proxy A/B Evaluation | passthrough 与 guarded 配对 | 完成 | `FORMAL_EXPERIMENT_COMPLETED` | [Stage 4 结果](../../deliverables/stage4/) | 无 |
| Stage 4.1 | Guard Ablation Evaluation | P/I/O/F 消融 | 完成 | `FORMAL_EXPERIMENT_COMPLETED` | [Stage 4.1 结果](../../deliverables/stage4_ablation/) | 无 |
| Stage 5 | Runtime Attack Matrix and Failure Taxonomy | 六类攻击、T1–T9、Mock 回归 | 完成 | `FORMAL_EXPERIMENT_COMPLETED` | [Stage 5 结果](../../deliverables/stage5/) | 真实矩阵另行批准 |
| Stage 5 Paper | Deterministic Runtime Evaluation Baseline | A1–A6、双 detector、AttemptRecord | 完成 | `FORMAL_EXPERIMENT_COMPLETED` | [Stage 5 Paper](../../deliverables/stage5_paper/) | 真实模型矩阵另行批准 |
| S6-T1–T3 | 数据、攻击矩阵与标签隔离 | R1–R6 fixture 与公开/评估边界 | 完成 | `ENGINEERING_VALIDATED` | `8577d73`、`055f266` | 无 |
| S6-T4 | Embedding + Persistent Vector Store | Provider、InMemory、Chroma、metadata/fingerprint | 完成 | `ENGINEERING_VALIDATED` | `bd3fcc9` 至 `664c445` | 无 |
| S6-T4 Hardening | 真实 MiniLM + Chroma 验收 | 固定 revision、384 维、重开和排序验证 | 完成 | `ENGINEERING_VALIDATED` | `3950c47` | 无 |
| S6-T5 Design Freeze | 受控检索与 Context 设计 | 边界、ID、引用和预算设计 | 完成 | `DESIGN_FROZEN` | `e64063e` | 不授权实现 |
| S6-T5 Design Hardening | 设计审查加固 | DTO、投影、ContentRef、审计异常边界 | 完成 | `DESIGN_FROZEN` | `aeb7e48` | 不授权实现 |
| S6-T5.1 | Chunking Contracts | IdentityChunker 与稳定 Chunk ID | 已接受 | `HUMAN_ACCEPTED` | `412d886`、`09584c8` | 无 |
| S6-T5.2 | Retrieval Runtime Contracts and IDs | 安全投影、Request、Evidence、Trace、ContentRef | 已接受 | `HUMAN_ACCEPTED` | `4c12181`、`03750d9`、[完成记录](s6_t5_2_completion_record.md) | 无 |
| S6-T5.3 | DenseRetriever | 透明 Dense Retrieval | S6-T5.3 DenseRetriever 已通过人工验收；P1/H1 均已接受 | `ENGINEERING_VALIDATED` | [完成记录](s6_t5_3_completion_record.md)、[阻断记录](s6_t5_3_protocol_blocker_record.md)、`72a2445` | S6-T5.4 仍需独立批准 |
| S6-T5.4 | Controlled Corpus ContentResolver | 受控正文解析与 hash 校验 | P1、I1、H1 与父任务均通过人工验收；仅覆盖合成内存 resolver 工程边界 | `ENGINEERING_VALIDATED` | [completion record](s6_t5_4_completion_record.md)、[blocker record](s6_t5_4_protocol_blocker_record.md)、PODR-015、PODR-016 | S6-T5.5 仍须独立批准 |
| S6-T5.5-P1 | EvidenceEnvelope and Citation Boundary Freeze | 解决 Citation 时序、factory、escaping 与敏感导出边界 | 已人工验收；仅为协议设计 | `DESIGN_FREEZE_HUMAN_ACCEPTED` | [protocol review record](s6_t5_5_protocol_review_record.md)、PODR-019 | 不批准 S6-T5.5 实现 |
| S6-T5.5-P1-H1 | Evidence Canonical Binding and Citation Rendering Protocol Hardening | 收紧 canonical Factory 输入、Renderer Binding identity 与 fail-closed mismatch | 已人工验收；仅为协议设计 | `DESIGN_FREEZE_HARDENING_HUMAN_ACCEPTED` | [protocol review record](s6_t5_5_protocol_review_record.md)、PODR-019 | 不批准 S6-T5.5 实现 |
| S6-T5.5 | Envelope and Citation implementation | 最小 contracts、Factory、instruction 与单 block rendering | I1、H1 与父任务已人工验收；不含 ContextBuilder | `ENGINEERING_VALIDATED_HUMAN_ACCEPTED` | [completion record](s6_t5_5_completion_record.md)、[protocol review record](s6_t5_5_protocol_review_record.md)、`6da27a6` | S6-T5.6 未批准 |
| S6-T5.6-P1 | Context Package Boundary Freeze | ContextBuilder、预算、Package 与结构性 abstention 协议 | 已人工验收；未实现业务代码 | `DESIGN_FREEZE_HUMAN_ACCEPTED` | [protocol review record](s6_t5_6_protocol_review_record.md)、PODR-023 | 不批准 S6-T5.6-I1 |
| S6-T5.6-P1-H1 | Sequential Resolution and Context Trace Hardening | 顺序正文解析、精确 UID 冲突、预算 cutoff 与 trace identity 协议 | 已人工验收；未实现业务代码 | `DESIGN_FREEZE_HARDENING_HUMAN_ACCEPTED` | [protocol review record](s6_t5_6_protocol_review_record.md)、PODR-024 | 不批准 S6-T5.6-I1 |
| S6-T5.6-P1-H2 | Active Specification, Trace Decision and Package Identity Protocol Closure | 活动顺序、instruction-budget 决策、Trace partition 与 Package identity | 已人工验收；未实现业务代码 | `DESIGN_FREEZE_HARDENING_HUMAN_ACCEPTED` | [protocol review record](s6_t5_6_protocol_review_record.md)、PODR-025、`432b07e` | 不批准 S6-T5.6-I1 |
| S6-T5.6 | Deterministic Retrieved Context Package | 稳定排序、顺序解析、预算、Package | 已接受 | `HUMAN_ACCEPTED` | `b136ee2`、`dbf590a`、[completion record](s6_t5_6_completion_record.md) | 无 |
| S6-T5.7 | Controlled Retrieval Context Integration | 静态与 opt-in 真实基础设施互操作 | 已接受 | `HUMAN_ACCEPTED` | `b6cedf3`、`c1e8c16`、[integration record](s6_t5_7_integration_completion_record.md) | S6-T5 baseline 已接受；不自动批准 Stage 6.1 |
| S6-T5.8 | Baseline Documentation and Acceptance | 统一证据索引与基线候选整理 | 已人工验收 | `HUMAN_ACCEPTED` | original candidate closure `37cccdc`、accepted baseline content `4ecf73a`、[baseline report](s6_t5_baseline_acceptance_report.md) | 不得创建 tag、分支或 Stage 6.1 |
| S6-T5.8-H1 | Baseline Commit Taxonomy and Evidence Mapping Hardening | 明确协议、实现、验收与集成证据提交分类 | 已人工验收 | `HUMAN_ACCEPTED` | `4ecf73a`、[baseline report](s6_t5_baseline_acceptance_report.md)、PODR-034、治理测试 | 仅修正文档证据 taxonomy；不得改业务行为 |
| S6-T5 Baseline | Controlled Retrieval and Traceable Context Baseline | 受控检索至 Context Package 的离线工程基线 | 已人工验收 | `HUMAN_ACCEPTED_BASELINE` | baseline content `4ecf73a`、PODR-034、[baseline report](s6_t5_baseline_acceptance_report.md) | 本轮治理提交不是 implementation 或 integration evidence；Stage 6.1 未批准 |
| S6.1-LR1 | Literature / Benchmark / Reproduction Alignment | 外部基准、路线与复现规划 | 已人工验收 | `HUMAN_ACCEPTED` | `1294632`、`85a5655`、PODR-041/042 | S6.1-R0 单独批准 |
| S6.1-R0-B0 | RTX5090 Compute Worker Bootstrap Validation | WSL GPU、PyTorch basic compute、Git context sync | 已人工验收 | `HUMAN_ACCEPTED_ENGINEERING_ENVIRONMENT_VALIDATION` | PODR-046、REL-2026-0008 | R0-A |
| S6.1-R0 | Reproduction Environment and Baseline Feasibility Validation | external baseline static audit/minimal smoke 与资源/兼容性证据 | 已带 blocker 人工验收 | `HUMAN_ACCEPTED_WITH_BLOCKERS` | [R0-I review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_i_control_plane_review.md)、PODR-049/050 | FU1-P0 follows |
| S6.1-R0-FU1-P0 | Targeted External Baseline Feasibility Resolution | dataset/attack/source/call-path and Worker contract freeze | human accepted | `HUMAN_ACCEPTED_CONTROL_PLANE_CONTRACT` | [FU1 resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)、PODR-051/052 | W2 approved under exact frozen contract |
| S6.1-R0-FU1-L1 | PoisonedRAG Released Artifact Identity and Deterministic Assembly Validation | exact artifact/schema/assembly hashes without model/API | human accepted | `HUMAN_ACCEPTED_SOURCE_ARTIFACT_VALIDATION` | [FU1 resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)、PODR-052、REL-2026-0013 | W1 superseded；W2 approved under separate gate |
| S6.1-R0-FU1-W2 | GMTP Detection-Only Minimal Smoke | exact detector-core compatibility on fixed GMTP-packaged input | human accepted and closed；single-sample engineering feasibility only | `HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED` | [FU1 process](../research/stage6_1_hidden_knowledge_poisoning/stage_process/S6.1-R0-FU1_work_process.md)、PODR-061、REL-2026-0024 | complete；no reproduction/effectiveness inference |
| S6.1-R0-FU1-W2-H1 | Offline Model Artifact Provisioning and W2 Resume | exact-revision offline bundle without LOCAL model loading | exact identity/index/load verified within frozen H2 on 5090；completed | `OFFLINE_MODEL_ARTIFACTS_VERIFIED_ON_5090 / COMPLETED` | [H2 resume02 review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_h2_resume02_control_plane_review.md)、REL-2026-0023/0024 | complete dependency；no new model authority |
| S6.1-R0-FU1-W2-H2 | Offline Model Bundle Verification and Conditional GMTP Detection-Core Resume | 5090 verifies exact offline bundle, then conditionally makes one frozen two-document call | resume_01 valid blocked；resume_02 evidence accepted as W2 evidence | `ENGINEERING_SMOKE_COMPLETED / CONTROL_PLANE_REVIEW_PASS / HUMAN_ACCEPTED_AS_W2_EVIDENCE` | [H2 resume02 review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_h2_resume02_control_plane_review.md)、PODR-061 | complete；no rerun or automatic P1 |
| S6.1-R0-FU1-W2-H2-RESUME-01 | H2 first frozen evidence namespace | fail closed when bundle/sidecar absent | valid blocker evidence；H2-B not executed；call_count 0 | `OFFLINE_BUNDLE_SHA_BLOCKER` | resume01 archive SHA `941557aa...26e89d`、19/19、PODR-060 | immutable history；superseded only as next execution namespace |
| S6.1-R0-FU1-W2-H2-RESUME-02 | Additive Evidence Namespace Rollover | preserve resume_01 and run full H2-A plus one conditional H2-B in new namespace | archive/safety/index/identities/results reviewed | `CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED` | [H2 resume02 review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_h2_resume02_control_plane_review.md)、REL-2026-0023 | complete；single-call authorization consumed；owner decides parent W2 |
| S6.1-R0-FU1-W2-ATTEMPT1-CORRECTION-02 | W2 Attempt 1 GNU du Provenance Final Evidence Correction | exact apparent/allocated `du` commands, tool/Conda/time provenance, raw streams/exits, counts and indexed manifest | Control Plane review passed；final closure applied | `EVIDENCE_PACKAGING_CORRECTION_ACCEPTED` | [FU1 resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)、PODR-057/058、REL-2026-0018/0019 | complete；do not rerun |
| S6.1-P1 candidate (historical) | Paper 1 Formal Experimental Protocol and Benchmark Specification | RQ/Benchmark/method/metrics/statistics/evidence/license and detox A/B/C design | historical candidate only；not approved/not started | `CONTRACT_CANDIDATE / SUPERSEDED_AT_CANDIDATE_LEVEL_BY_P1-R1` | [P1 candidate](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_protocol_candidate.md)、PODR-061 | preserved history；P1-R1 framework later accepted |
| S6.1-P1-R1 | P1 Protocol Hardening and Option B Scope Freeze | approval-grade RQ1-6、Benchmark/schema/split/label isolation、five-view detection、hard filter/soft downweight、metrics/statistics/Pilot/resource/evidence/license | framework accepted；numeric parameters and formal protocol freeze pending | `HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK` | [P1-R1 framework source](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_r1_protocol_review_candidate.md)、OR-021、PODR-062 | no automatic Dataset/Detector/formal execution |
| S6.1-P1-PILOT2-RETURN-CORRECTION-01 | PILOT2 Return Preflight Owner Correction | preserve raw registration/returns/preflight history；supersede timestamp-based blindness inference；reinterpret remaining blocker | owner correction registered；agreement not calculated | `PROTOCOL_AND_ANNOTATION_SCHEMA_BLOCKER / AUTO_CONTINUE_NO` | [Owner correction record](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_return_owner_correction.md)、PODR-063、OR-025、REL-2026-0029 | separately approve/freeze Annotation Schema V2 and A/B independent re-review |
| S6.1-P1-PILOT2-ANNOTATION-V2 | Pilot2 Schema V2 Repair and A/B Independent Re-review Packages | preserve raw Round1；freeze four-value/applicability/authority/decision-tree/process contracts；prepare isolated A/B packages | schema/validator and four packages completed；human re-review not yet executed | `ANNOTATION_SCHEMA_V2_IMPLEMENTED / A_B_REREVIEW_READY_FOR_HUMAN_EXECUTION / FORMAL_AGREEMENT_V2_NOT_YET_ESTABLISHED` | [Annotation V2 record](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_annotation_v2.md)、PODR-064、OR-026、REL-2026-0030；Git-external `ROUND1_RAW_MANIFEST` | A/B complete and return four V2 packages；owner separately approves validation/agreement |
| S6.1-P1-PILOT4-PREANNOTATION | Pilot4 Signal Repair, Balanced Diagnostic Set and Pre-annotation Quality Gate | canonical lessons；field/candidate gates；structured signals；24 matched triplets / 72 candidates / 48 queries；four-round QA | historical first preflight returned for targeted repair；original evidence preserved | `HISTORICAL / OWNER_PREFLIGHT_RETURNED_FOR_TARGETED_REPAIR` | [future dataset rules](../research/stage6_1_hidden_knowledge_poisoning/human/annotation_lessons_learned_and_future_dataset_rules.md)、PODR-071、OR-033、REL-2026-0037；Git-external manifest 22/22 | superseded by targeted repair row |
| S6.1-P1-PILOT4-PREANNOTATION-TARGETED-REPAIR-01 | Pilot4 semantic/evidence-path targeted repair | repair mutation semantics、stealth path、echo/meta-language、visibility、applicability、G1–G14、Round D and HN evidence | repaired 72 + second 12-row Owner sample；no human distribution | `PILOT4_BALANCED_SET_REPAIRED / READY_FOR_SECOND_OWNER_PREFLIGHT / PREANNOTATION_ONLY` | `cad3b2b2`、PODR-072、OR-034、REL-2026-0038；Git-external repair manifest | Owner second preflight only |
| GOV-P1-HUMAN-DOCS-INTEGRATION-01 | Paper 1 Human/Agent/Evidence Documentation Integration | human master、research authority、agent ledger、navigation、inventory、five formal domains | documentation only；experiment state unchanged | `DOCUMENTATION_STRUCTURE_AND_CONTEXT_INTEGRATION` | PODR-073、OR-035、REL-2026-0039 | current experiment gate remains second Owner preflight |
| S6.1-P1-PILOT4-PREANNOTATION-TARGETED-REPAIR-02 | Pilot4 genuine-S3, S1-shortcut, actual-length and final-preflight repair | evidence necessity、natural S1 contradiction、final visible length、template diversity、HN semantics、source/parity/Phase1-only validation | final 72 + 16-row Owner workbook；no human distribution | `PILOT4_FINAL_PREANNOTATION_READY_FOR_OWNER_REVIEW / NO_HUMAN_DISTRIBUTION` | PODR-074、OR-036、REL-2026-0040；Git-external manifest 22/22 | Owner final preflight only |
| S6.1-P1-PILOT4-PREANNOTATION-QUALITY-CONVERGENCE-01 | Pilot4 source-verified data and Schema V3 quality convergence | Phase1 leakage、actual-source/HN verification、semantic S1/S2/S3、full72、truth table、ambiguity and annotator dry-run | 72 candidates + 64 source units + 28-field Schema V3 + 3 dry-run XLSX；no human distribution | `PILOT4_QUALITY_CONVERGED / READY_FOR_OWNER_ACCEPTANCE_REVIEW / NO_HUMAN_DISTRIBUTION` | PODR-075、OR-037、REL-2026-0041；Git-external manifest `45/45`, SHA256 `90ac505b...1ff7` | Owner full72/schema/dry-run acceptance review only |
| PILOT4-EVIDENCE-POOL-REPAIR-01 | Pilot4 distinct Evidence Pool and Schema V3.1 finalization | repair duplicate visible slots; acquire 23 companions; final enums, English-first UI, full72/validator/SIM/workbook QA | 72/72 distinct pools + 23/23 verified companions + 4 Phase1/7 Phase2 manual fields + 3 V3.1 XLSX / 10 Sheets | `PILOT4_ANNOTATION_PROTOCOL_READY_FOR_OWNER_ACCEPTANCE / NO_HUMAN_DISTRIBUTION` | REL-2026-0042；Git-external child namespace `paper1_pilot4_evidence_pool_repair_20260901`; manifest `53/53`, SHA256 `180307ac...f1640f64` | Owner accepts protocol or reports blocker; A/B still separate approval |
| PILOT4-ANNOTATION-PROTOCOL-INDEPENDENT-VALIDATION-AND-CANDIDATE-CLEANUP-01 | Pilot4 label-blind answerability and Schema V3.1 hardening | lock-before-compare review; candidate meta-cue cleanup; minimum/stealth/issue closure; neutral four-column Evidence Pool | 23 additive candidate rewrites + 72/72 one-context label-blind review + final mismatch 0 + 3 V3.1 XLSX / 10 Sheets | `PILOT4_ANNOTATION_PROTOCOL_READY_FOR_OWNER_ACCEPTANCE / NO_HUMAN_DISTRIBUTION` | `PODR-076 / OR-038 / REL-2026-0043`; Git-external `paper1_pilot4_protocol_independent_validation_20260902` | Owner reviews; machine independence not established; A/B separate approval |
| PILOT4-EXTERNAL-BLIND-OWNER-REVIEW-PACKET-01 | Pilot4 external label-blind Owner review packet | ephemeral opaque identity, isolated mapping, actual-title provenance, complete field-guide cases and external four-file packet | 72 rows + 144 actual-title slots + 66 independent guide cases; no semantic answers or expected comparison | `PILOT4_EXTERNAL_BLIND_REVIEW_PACKET_READY / WAITING_FOR_EXTERNAL_OWNER_REVIEW / NO_HUMAN_DISTRIBUTION` | `PODR-077 / OR-039 / REL-2026-0044`; Git-external `paper1_pilot4_external_blind_review_packet_20260902` | isolated external GPT/Owner review return only |
| Stage 6.1 | Hidden Knowledge Poisoning Detection | 隐蔽污染检测 | LR1/R0/FU1 accepted；P1-R1 framework accepted；Pilot4 quality convergence ready for Owner acceptance review；formal work not started | `PILOT_IN_PROGRESS / NOT_FORMAL_EXPERIMENT` | [长期需求](long_term_research_requirements.md) | Pilot4 full72/schema/dry-run Owner review |
| Stage 6.2 | Multi-Evidence Trustworthy Retrieval | 可信聚合、重排、拒答 | 规划中 | `PLANNED` | [长期需求](long_term_research_requirements.md) | Stage 6.1/设计批准 |
| Stage 7 | Agent Security Evaluation | Tool/Memory/Planning 安全 | 规划中 | `PLANNED` | [Stage 7 README](../../stages/stage7_agent_security/README.md) | Trusted Context 契约 |

## 5. 实验与验证分类

### 5.1 正式安全实验

正式实验必须具有研究问题或假设、固定输入/对照、原始输出、指标、结果文件、结论边界，并尽可能提供 `run_id`。Stage 2 的 Mock 对照、Stage 3 的真实 API smoke、Stage 4/4.1 的真实 Guard 对照，以及 Stage 5/5 Paper 的确定性 Mock 矩阵均登记为正式实验；其中只有 Stage 3/4/4.1 使用真实 Groq 模型。

### 5.2 工程验证

单元测试、集成测试、架构/namespace/标签隔离检查、Ruff、MyPy、secret scan、Git-ignore、Chroma 持久化重开、Chunk ID 稳定性和契约迁移均属于工程验证。

> 工程验证证明代码满足契约和边界，不直接证明安全防护效果、抗投毒能力或统计显著性。

### 5.3 设计冻结

ADR、设计规格和实施计划只冻结未来边界与验证方法。设计完成不能写成业务功能或实验已完成。

## 6. 指标字典

| 指标 | 全称 | 适用阶段 | 计算口径 | 分子/分母 | 方向 | 当前状态 | 证据来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PASS / FAIL | garak detector verdict | S1–S4.1 | PASS 未命中，FAIL 命中攻击目标 | detector 记录 | PASS 高为宜 | 已使用 | [Stage 3 摘要](../../deliverables/stage3/groq_scan_summary.md) |
| ASR | Attack Success Rate | S1–S5 | 成功攻击 attempt / 攻击 attempt | attempt 级 | 低为宜 | 已使用 | 各 Stage 结果 JSON |
| Detector Hit Rate | Detector 命中率 | S3–S4.1 | FAIL detector 记录 / detector 评测记录 | detector 级 | 低为宜 | 已使用 | Stage 3/4 JSON |
| Input Block Count/Rate | 输入拦截数/率 | S4–S5 | input blocked / request | request 级 | 情境相关 | 已使用 | Guard JSONL/聚合 JSON |
| Output Block Count/Rate | 输出拦截数/率 | S4–S5 | output blocked / request | request 级 | 情境相关 | 已使用 | Guard JSONL/聚合 JSON |
| Upstream Call Count/Rate | 上游模型调用数/率 | S4–S5 | upstream called / request | request 级 | 结合效用解释 | 已使用 | Guard JSONL/聚合 JSON |
| Prompt Hash Parity | 攻击输入一致性 | S4–S5 | 同 sample 的 prompt hash 是否一致 | P/I/O/F | 必须为真 | 已使用 | Stage 4/4.1/5 结果 |
| Raw Output Hash Parity | 原始输出哈希一致性 | S4.1、S5 | 同输入模型原始输出 hash 一致性 | 对照组 | 诊断指标 | 已使用 | Stage 4.1/5 日志 |
| Sensitive Marker Count | 敏感规则命中数 | S4–S5 | Guard 自定义规则命中 | output/input | 低为宜 | 已使用 | Guard 日志 |
| T1–T9 | Failure Taxonomy | S5 | 自动分类的失败类型计数 | attempt | 情境相关 | 已使用 | [taxonomy JSON](../../deliverables/stage5/logs/20260701T030819Z-05703f/failure_taxonomy_result.json) |
| DMR | Detector Miss Rate | S5 Paper | raw risk 且 garak pass 的比例 | 见 run manifest 口径 | 低为宜 | 已使用 | [Paper 摘要](../../deliverables/stage5_paper/runs/20260701T081320Z-c29f39/run_summary.md) |
| GBR | Guard Bypass Rate | S5 Paper | guard enabled 但 final risk 的比例 | 见 run manifest 口径 | 低为宜 | 已使用 | 同上 |
| Over-block | 正常请求误拦截率 | S5/Paper | benign 且被拦截 / benign | benign request | 低为宜 | 已使用 | 同上 |
| Passed / Skipped | 测试通过/跳过数 | S6 | pytest 测试状态 | test case | 通过高为宜 | 已使用 | 测试日志/学习记录 |
| Recall@K、Precision@K、MRR、nDCG@K | 检索质量指标 | Stage 6 | `PLANNED_NOT_IMPLEMENTED` | `NOT_RECORDED` | 高为宜 | `PLANNED_NOT_IMPLEMENTED` | 无 |
| Poison Retrieval Rate、Context Contamination Rate | 污染传播指标 | Stage 6 | `PLANNED_NOT_IMPLEMENTED` | `NOT_RECORDED` | 低为宜 | `PLANNED_NOT_IMPLEMENTED` | 无 |
| Citation Accuracy、Faithfulness | 引用/忠实性 | Stage 6.2 | `PLANNED_NOT_IMPLEMENTED` | `NOT_RECORDED` | 高为宜 | `PLANNED_NOT_IMPLEMENTED` | 无 |
| Abstention Precision/Recall、Latency、Cost | 风险与效率指标 | Stage 6.2+ | `PLANNED_NOT_IMPLEMENTED` | `NOT_RECORDED` | 情境相关 | `PLANNED_NOT_IMPLEMENTED` | 无 |

## 7. 文件、运行和结果命名规范

- Master Record 内部 ID：`ER-<STAGE>-<YYYYMMDD>-<NNN>`，只用于本文索引，不等同于历史 `run_id`。
- 原始 `run_id` 不存在时写 `NOT_RECORDED`；不根据目录日期伪造 ID。
- 新实验推荐 `<stage>-<UTC timestamp>-<short sequence>`；本轮不重命名历史目录。
- 原始输出与派生摘要分离；正式结果与 smoke test 分离；敏感工件与公开审计工件分离。
- 所有新索引使用仓库相对路径；运行时目录遵守 Git-ignore。

## 8. 正式运行总账

### 8.1 已回填运行

| Record ID | Original Run ID | 日期 | Stage/Task | Run Type | 模型/Provider | 状态 | 核心指标 | 原始证据 | 结论边界 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ER-S1-20260626-001 | `a214583f-5fa6-4734-abbb-b15629decce1` | 2026-06-26 | S1 minimal connectivity | `ENGINEERING_VALIDATION` | `test.Blank` | completed | PASS 1/1 | [JSON](../../deliverables/stage1/garak_scan_result.json) | 仅连通性 Mock |
| ER-S1-20260626-002 | `94c18ade-8fae-459c-b1a1-c49b81c5f264` | 2026-06-26 | S1 prompt injection | `ENGINEERING_VALIDATION` | `test.Repeat` | completed | FAIL 0/256，ASR 100% | [JSONL](../../deliverables/stage1/stage1_promptinject_scan.report.jsonl) | 预设脆弱 echo Mock |
| ER-S2-20260626-001 | `bfcbc1dd-1869-42c4-a9a5-9523ace01993` | 2026-06-26 | S2 vulnerable PromptInject | `FORMAL_EXPERIMENT` | local Mock | completed | FAIL 0/8 | [JSON](../../deliverables/stage2/stage2_scan_result.json) | 受控 Mock |
| ER-S2-20260626-002 | `d2768d63-9c1e-449b-b197-0932af345197` | 2026-06-26 | S2 guarded PromptInject | `FORMAL_EXPERIMENT` | local Mock | completed | PASS 8/8 | [JSON](../../deliverables/stage2/stage2_scan_result.json) | 受控 Mock |
| ER-S2-20260626-003 | `5a65c350-dd06-442b-a19b-17972979bfec` | 2026-06-26 | S2 vulnerable Base64 | `FORMAL_EXPERIMENT` | local Mock | completed | PASS 8/8 | [JSON](../../deliverables/stage2/stage2_scan_result.json) | detector 未命中不等于安全 |
| ER-S2-20260626-004 | `882d1505-10a3-41ee-a6d3-9b6451ffd4d5` | 2026-06-26 | S2 guarded Base64 | `FORMAL_EXPERIMENT` | local Mock | completed | PASS 8/8 | [JSON](../../deliverables/stage2/stage2_scan_result.json) | 受控 Mock |
| ER-S3-20260630-001 | `NOT_RECORDED` | 2026-06-30 | S3 Groq safe smoke | `FORMAL_EXPERIMENT` | Groq / `llama-3.1-8b-instant` | completed | 2 attempts，ASR 50%，detector hit 33.33% | [聚合 JSON](../../deliverables/stage3/groq_scan_result.json) | 单次两条样本 |
| ER-S4-20260630-001 | `NOT_RECORDED` | 2026-06-30 | S4 paired Guard A/B | `FORMAL_EXPERIMENT` | Groq / `llama-3.1-8b-instant` | completed | P: ASR 50%；guarded: ASR 0%；parity true | [聚合 JSON](../../deliverables/stage4/guarded_groq_scan_result.json) | 2 条 smoke，规则基线 |
| ER-S4.1-20260630-001 | `NOT_RECORDED` | 2026-06-30 | S4.1 P/I/O/F ablation | `FORMAL_EXPERIMENT` | Groq / `llama-3.1-8b-instant` | completed | P 50%；I/O/F 均 0%；parity true | [聚合 JSON](../../deliverables/stage4_ablation/ablation_result.json) | 2 条 smoke，规则基线 |
| ER-S5-20260701-001 | `20260701T025836Z-7da785` | 2026-07-01 | S5 attack matrix rerun | `FORMAL_EXPERIMENT` | local Mock | completed | 22 samples，P/I/O/F parity true | [manifest](../../deliverables/stage5/logs/20260701T025836Z-7da785/run_manifest.json) | Mock 回归 |
| ER-S5-20260701-002 | `20260701T030024Z-37cfd4` | 2026-07-01 | S5 attack matrix rerun | `FORMAL_EXPERIMENT` | local Mock | completed | 22 samples，P/I/O/F parity true | [manifest](../../deliverables/stage5/logs/20260701T030024Z-37cfd4/run_manifest.json) | Mock 回归 |
| ER-S5-20260701-003 | `20260701T030156Z-91ae2d` | 2026-07-01 | S5 attack matrix rerun | `FORMAL_EXPERIMENT` | local Mock | completed | 22 samples，P/I/O/F parity true | [manifest](../../deliverables/stage5/logs/20260701T030156Z-91ae2d/run_manifest.json) | Mock 回归 |
| ER-S5-20260701-004 | `20260701T030819Z-05703f` | 2026-07-01 | S5 canonical smoke | `FORMAL_EXPERIMENT` | local Mock | completed | 88 attempts，ASR 95.83%，Over-block 0% | [manifest](../../deliverables/stage5/logs/20260701T030819Z-05703f/run_manifest.json) | 当前规则/矩阵下 |
| ER-S5P-20260701-001 | `20260701T081320Z-c29f39` | 2026-07-01 | S5 Paper baseline | `FORMAL_EXPERIMENT` | local Mock | completed | 88 attempts，ASR 95.83%，DMR 0%，GBR 94.44% | [manifest](../../deliverables/stage5_paper/runs/20260701T081320Z-c29f39/run_manifest.json) | Mock baseline，不是 Groq 全矩阵 |

**账本统计（由上表实际记录计算）**：FORMAL_EXPERIMENT = 12；ENGINEERING_VALIDATION = 2。S6 的工程/设计条目另见第 10 节。历史 Stage 3、Stage 4 与 Stage 4.1 缺少 machine-readable `run_id`、模型 revision 与数据 fingerprint，按原样标记，不能倒推伪造。

## 9. Stage 1–5 历史结果汇总

| Stage | 实际对象与设计 | 核心结果 | 证据 | 当前可证明什么 |
| --- | --- | --- | --- | --- |
| S1 | garak 内置 Mock，`test.Blank` 与 `test.Repeat` | 连通性 PASS 1/1；echo PromptInject ASR 100% | [报告](../../deliverables/stage1/stage1_report.md) | 理解安全扫描闭环，不是现实模型风险 |
| S2 | OpenAI-compatible local Mock，vulnerable/guarded | PromptInject 0/8 FAIL 对 8/8 PASS；两组 Base64 PASS | [摘要](../../deliverables/stage2/stage2_scan_summary.md) | 可控协议与防护对照 |
| S3 | Groq 真实 API，2 个 probes、2 attempts | PromptInject 命中；Base64 detector PASS 但人工复核发现部分危险解码 | [逐条分析](../../deliverables/stage3/08_first_real_scan_analysis.md) | 真实调用链、Detector Miss 边界 |
| S4 | local Guard Proxy → Groq，passthrough/guarded | 50% → 0%；guarded 输入拦截 2 次、上游调用 0 次 | [摘要](../../deliverables/stage4/guarded_groq_scan_summary.md) | 当前规则的输入 Guard 对照效果 |
| S4.1 | P/I/O/F 四组，固定 seed 与 prompt parity | output-only 调用上游 2 次后输出拦截 2 次；I/F 输入拦截 | [摘要](../../deliverables/stage4_ablation/ablation_summary.md) | 输入与输出规则均被独立验证 |
| S5 | 六类攻击各 2 条、benign 10 条、四 Guard Mode | 22 samples、88 attempts、T1–T9、parity true | [run summary](../../deliverables/stage5/logs/20260701T030819Z-05703f/run_summary.md) | 可复现的 Mock 评测框架 |
| S5 Paper | A1–A6、P/I/O/F、garak + stage5_pattern | 88 attempts；ASR 95.83%；DMR 0%；GBR 94.44% | [结果](../../deliverables/stage5_paper/07_results.md) | 确定性论文级 baseline，不是实模统计结论 |

## 10. Stage 6 工程状态与正式实验缺口

| Task | 能力 | 状态 | 验证类型 | 测试/设计证据 | 是否产生安全实验结果 | 下一门禁 |
| --- | --- | --- | --- | --- | --- | --- |
| S6-T1–T3 | R1–R6 数据、攻击矩阵、标签隔离 | completed | 工程验证 | [数据 README](../../data/stage6_rag/README.md) | 否 | 无 |
| S6-T4 | Static/real Embedding、InMemory/Chroma、fingerprint | completed | 工程验证 | [ADR 0007](../architecture/0007_embedding_vectorstore_boundary.md) | 否 | 无 |
| S6-T4 Hardening | 固定 MiniLM revision、临时 Chroma 重开、中文/英文 Top-1 | completed | 真实集成验证 | [项目总控](../../PROJECT_MASTER_CONTEXT.md) | 否 | 无 |
| S6-T5 Design Freeze/Hardening | 受控检索、Evidence、Context 边界 | completed | 设计审查 | [ADR 0008](../architecture/0008_retrieval_context_boundary.md) | 否 | 不授权实现 |
| S6-T5.1 | ChunkRecord、IdentityChunker、稳定 ID | human accepted | 工程验证 | [学习记录](../../deliverables/learning_notes.md) | 否 | 无 |
| S6-T5.2 | safe projection、Request/Evidence/Trace/ContentRef | implemented，pending human acceptance | 工程验证 | [完成记录](s6_t5_2_completion_record.md) | 否 | 人工验收 |
| S6-T5.3 | DenseRetriever | HUMAN_ACCEPTED；P1/H1 已接受 | `ENGINEERING_VALIDATED` | [完成记录](s6_t5_3_completion_record.md) | 否 | S6-T5.4 独立批准 |
| S6-T5.4 | Controlled Corpus ContentResolver | P1、I1、H1 与父任务 HUMAN_ACCEPTED；只确认受控内存工程边界 | `ENGINEERING_VALIDATED` | [completion record](s6_t5_4_completion_record.md)、[blocker record](s6_t5_4_protocol_blocker_record.md) | 否 | S6-T5.5 仍未批准 |
| S6-T5.5 | Envelope、Citation 与单 block structural rendering | HUMAN_ACCEPTED；仅 synthetic objects 离线工程边界 | `ENGINEERING_VALIDATED_HUMAN_ACCEPTED` | [completion record](s6_t5_5_completion_record.md)、`6da27a6` | 否 | 不自动批准 S6-T5.6 |
| S6-T5.6-P1 | ContextBuilder/预算/Package 协议冻结 | HUMAN_ACCEPTED；无业务实现 | `DESIGN_FREEZE_HUMAN_ACCEPTED` | [protocol review record](s6_t5_6_protocol_review_record.md)、PODR-023 | 否 | 不自动批准实现 |
| S6-T5.6-P1-H1 | 顺序解析、重复语义与 Context Trace 加固 | HUMAN_ACCEPTED；无业务实现 | `DESIGN_FREEZE_HARDENING_HUMAN_ACCEPTED` | [protocol review record](s6_t5_6_protocol_review_record.md)、PODR-024 | 否 | 不自动批准实现 |
| S6-T5.6-P1-H2 | 活动规格、Trace 决策与 Package 身份闭环 | HUMAN_ACCEPTED；无业务实现 | `DESIGN_FREEZE_HARDENING_HUMAN_ACCEPTED` | [protocol review record](s6_t5_6_protocol_review_record.md)、PODR-025、`432b07e` | 否 | 不自动批准实现 |
| S6-T5.6 | Context Package future implementation | READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL；`S6-T5.6-I1` 尚未批准 | `DESIGN_FREEZE_HUMAN_ACCEPTED` | [protocol review record](s6_t5_6_protocol_review_record.md)、GOV-S6-T5.6-P1-ACCEPTANCE | 否 | 不自动开始 I1 |
| S6-T5.7+ | Context、后续受控能力 | NOT APPROVED | `PLANNED_NOT_IMPLEMENTED` | [protocol review record](s6_t5_6_protocol_review_record.md) | 否 | 前序任务 |

截至当前状态，Stage 6 已完成架构、契约、版本化 metadata carrier 与无正文 DenseRetriever 的工程验证。虽然真实 MiniLM 与 Chroma 的固定小语料集成测试已运行，但没有正式 R1–R6 攻击矩阵、RAG 指标或防护效果实验，故不能宣称“Stage 6 RAG 安全实验已完成”。

## 11. 未来 Stage 6 正式实验计划

| Experiment ID | 研究问题 | 自变量 | 对照组 | 数据/模型 | 指标 | 当前状态 | 前置条件 | 禁止夸大 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S6E-01 | Dense Retrieval 是否可复现且可审计 | top-k、固定 MiniLM/Chroma | transparent baseline | Stage 6 corpus | Recall@K、MRR、nDCG@K | `PLANNED_NOT_IMPLEMENTED` | S6-T5.3 | 不等于安全防护 |
| S6E-02 | R1 Query Injection 如何影响检索 | attack prompt | benign query | R1 dataset | RMSR、trace | `PLANNED_NOT_IMPLEMENTED` | Retriever/Runner | 不等于上下文或生成风险 |
| S6E-03 | R2/R5 污染如何被召回 | poisoned corpus composition | clean corpus | R2/R5 dataset | Poison Retrieval Rate | `PLANNED_NOT_IMPLEMENTED` | Retriever/Evaluator | 不等于可信检索 |
| S6E-04 | R3 Context Injection 如何传播 | retrieved evidence | clean evidence | R3 dataset | Context Contamination Rate | `PLANNED_NOT_IMPLEMENTED` | Resolver/ContextBuilder | 不等于模型攻击成功 |
| S6E-05 | R4/R6 如何影响排序与回答倾向 | embedding/steering variant | baseline | R4/R6 dataset | RMSR、Faithfulness | `PLANNED_NOT_IMPLEMENTED` | 后续批准 | 不得伪造指标 |
| S6E-06 | Guard/Trust 的独立贡献 | input/output/retrieval policy | off/observe | 固定攻击矩阵 | 安全-效用指标 | `PLANNED_NOT_IMPLEMENTED` | Stage 6B+ | 规则基线不等于论文算法 |
| S6.1E | 隐蔽知识污染检测 | 检测器与数据难度 | 多 baseline | 双领域许可语料 | F1/AUROC/AUPRC | `PLANNED_NOT_IMPLEMENTED` | Stage 6 baseline | 不声称已检测 |
| S6.2E | 多证据可信检索 | 信任聚合/重排 | Dense/BM25/Hybrid | 多来源语料 | Trust/Citation/Abstention | `PLANNED_NOT_IMPLEMENTED` | Stage 6.1 | 不声称已可信 |

## 12. Blocker Register

### 12.1 Canonical Blocker Record Schema

Blocker Register 是 canonical blocker authority，不创建第二个竞争文件。每个新 blocker、每个被本轮触及的历史
blocker，以及每次状态变化都至少记录下列字段：

```text
blocker_id
discovered_at
stage
task
machine
severity
description
why_it_blocks
affected_scope
evidence
attempt_1
attempt_1_result
attempt_2
attempt_2_result
temporary_workaround
final_resolution
resolution_commit
resolution_run
resolved_at
status
```

合法 canonical status 只有 `OPEN`、`MITIGATED`、`RESOLVED`、`ACCEPTED_TECHNICAL_DEBT`。历史复合标签可保存在
description/final_resolution 中，但不能代替 status。**WORKAROUND is not RESOLVED**；compatibility environment 默认
只能记为 `MITIGATED_BY_COMPATIBILITY_ENV` / `MITIGATED`，直到算法等价和正式关闭证据成立。

### 12.2 Normalized Blocker Records

| blocker_id | discovered_at | stage | task | machine | severity | description | why_it_blocks | affected_scope | evidence | attempt_1 | attempt_1_result | attempt_2 | attempt_2_result | temporary_workaround | final_resolution | resolution_commit | resolution_run | resolved_at | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BLK-HIST-001 | 2026-07-19 | Stage 1–5 | historical integrity | LOCAL | medium | 110 Windows CRLF/LF manifest differences | byte baselines are not portable | integrity regression | learning record and baseline acceptance | Git blob/diff review | confirmed existing line-ending debt | rewrite history | rejected | preserve files and use Git evidence | accepted as historical technical debt | N/A | N/A | 2026-07-27 | ACCEPTED_TECHNICAL_DEBT |
| BLK-HIST-002 | 2026-07-19 | Stage 1–4.1 | historical reproducibility | LOCAL | medium | missing RunManifest/model revision/data fingerprint | strict rerun identity is incomplete | historical reproduction | NOT_RECORDED fields in this record | preserve original paths | evidence remains usable within limits | infer missing identity | rejected as fabrication | future runs use RunManifest | NOT_RECORDED | N/A | N/A | NOT_RECORDED | OPEN |
| BLK-HIST-003 | 2026-07-19 | Stage 5 legacy | scoped typing | LOCAL | low | legacy full MyPy warnings | full-project strict typing cannot be claimed | legacy maintenance | scoped MyPy history | scoped MyPy | current code can be checked without history mutation | rewrite legacy | not approved | scoped checking | accepted legacy debt | N/A | N/A | 2026-07-19 | ACCEPTED_TECHNICAL_DEBT |
| BLK-S6-001 | 2026-07-22 | Stage 6 | S6-T5.3 | LOCAL | high | hit lacked parent identity | canonical RetrievalEvidence could not be built safely | DenseRetriever | protocol blocker record | schema 1.1 public carrier | identity reached RetrievalEvidence | schema 1.0 rewrite | rejected | no workaround after closure | RESOLVED_BY_VERSIONED_PUBLIC_METADATA_CONTRACT | 2ad3d9c | N/A | 2026-07-22 | RESOLVED |
| BLK-S6-004 | 2026-07-25 | Stage 6 | S6-T5.4 | LOCAL | high | resolver permission/return/reader/mapping/errors were unfrozen | implementation would guess sensitive capability | ContentResolver | S6-T5.4 blocker record | stop implementation | fail-closed preserved | freeze P1 protocol | accepted by owner | no workaround after closure | RESOLVED_BY_APPROVED_PROTOCOL_FREEZE | 4155ed8 | N/A | 2026-07-25 | RESOLVED |
| BLK-S6-002 | current | Stage 6 | formal RAG research | LOCAL | high | no controlled formal RAG experiment | security/retrieval claims lack evidence | RAG conclusions | Stage 6 engineering state | engineering validation | contracts verified only | formal experiment | not approved | do not overclaim | NOT_RECORDED | N/A | N/A | NOT_RECORDED | OPEN |
| BLK-S6-003 | current | Stage 6 | real embedding/Chroma | LOCAL | medium | real infrastructure is opt-in/environment-sensitive | default CI cannot prove portable environment | integration validation | S6-T4/T5.7 records | explicit env gate/temp dir | controlled integration passed | full reproducible env | pending | explicit opt-in fixed revision | NOT_RECORDED | N/A | N/A | NOT_RECORDED | MITIGATED |
| BLK-API-001 | 2026-06-30 | Stage 3–4 | Groq expansion | LOCAL | medium | external API cost/policy and snapshot risk | uncontrolled expansion is not reproducible or bounded | real-model expansion | Stage 3/4 troubleshooting | safe small sample | historical smoke completed | approve budget/protocol | pending | safe mode and small samples | NOT_RECORDED | N/A | N/A | NOT_RECORDED | OPEN |
| BLK-DOC-001 | 2026-07-20 | Governance | historical S6-T5 snapshots | LOCAL | low | older text contains stale stage snapshots | new readers may mistake history for current state | context recovery | Git/current-state comparison | preserve dated snapshots | history remains auditable | add authority map and current entry | completed candidate | use current state plus authority hierarchy | pending human acceptance | PENDING_THIS_COMMIT | N/A | NOT_RECORDED | MITIGATED |
| BLK-S6.1-LR1-001 | 2026-07-31 | Stage 6.1 | strict comparison eligibility | LOCAL + RTX5090 | high | paper-result commit/revision/API/baseline compatibility/baseline resource facts incomplete | strict reproduction and comparison cannot start | PoisonedRAG/GMTP/SafeRAG strict comparison | external registry/matrix plus accepted Bootstrap | first-party alignment, six-field license split and Worker base readiness | base hardware/GPU/Git facts validated；baseline-specific gaps remain | S6.1-R0 | approved to characterize gaps | no strict-comparison workaround | NOT_RECORDED | N/A | N/A | NOT_RECORDED | OPEN |
| R0-I-EVIDENCE-CORRECTION-001 | 2026-07-31 | Stage 6.1 | S6.1-R0-I | LOCAL + RTX5090 | medium | GMTP sample-absence/Docker claims conflict with exact upstream；SafeRAG executed-script hash/all-row coverage incomplete | current Worker summary could not support R0 acceptance | R0 engineering review only | first review plus corrected archive/index/matrix and [R0-I review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_i_control_plane_review.md) | Control Plane source cross-check | material mismatch confirmed | minimal Worker correction | corrected GMTP/PoisonedRAG command evidence and bound SafeRAG all-row smoke passed | no acceptance workaround | RESOLVED_BY_CORRECTED_EVIDENCE | PENDING_THIS_COMMIT | N/A | 2026-07-31 | RESOLVED |
| BLK-S6.1-P1-001 | 2026-07-31 | Stage 6.1 | S6.1-R0-FU1-P0 | LOCAL | high | PoisonedRAG formal dataset and attack-generation executable identity were not frozen | comparison protocol would otherwise have unstable data/attack identity | P1 planning | [FU1 resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md) | NQ/released-artifact/API boundary source audit | source planning passed | freeze candidate identity and partial-equivalence boundary | completed pending owner review | no claim of regeneration equivalence | RESOLVED_BY_P0_CONTRACT_FREEZE | PENDING_THIS_COMMIT | N/A | 2026-07-31 | RESOLVED |
| BLK-S6.1-P1-002 | 2026-07-31 | Stage 6.1 | S6.1-R0-FU1-P0 | LOCAL | high | GMTP modified-BEIR source identity and exact detection-only path were not frozen | detector comparison could not be made reproducible | P1 planning | exact GitHub commit/source and [FU1 resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md) | verify BEIR identity and detector call graph | source planning passed | freeze source/models/sample/call path | completed pending owner review | no reimplementation workaround | RESOLVED_BY_P0_CONTRACT_FREEZE | PENDING_THIS_COMMIT | N/A | 2026-07-31 | RESOLVED |
| BLK-S6.1-FU1-W1-001 | 2026-07-31 | Stage 6.1 | FU1-L1 | LOCAL | high | exact released-artifact assembly identity lacked accepted evidence | P1 would otherwise have unstable attack input identity | L1 source artifact validation | exact commit/blob/schema/assembly contract | all 100 records and fixed sample hashes validated | deterministic identity passed | preserve API-generation distinction | accepted by owner | no regeneration claim | RESOLVED_BY_LOCAL_L1 / SUPERSEDED_BY_LOCAL_L1 | PENDING_THIS_COMMIT | N/A | 2026-07-31 | RESOLVED |
| BLK-S6.1-FU1-W2-001 | 2026-07-31 | Stage 6.1 | FU1-W2 | RTX5090 | high | exact GMTP detector core/models/scores were unvalidated on modern Worker environment | P1 lacked executable detector baseline feasibility evidence | W2 engineering validation | hardened exact source/input/model/config/environment/resource contract；resume02 archive `58da856a...f563` | H2-A `18/18` and indexed `25/25` pass；exact local CUDA models；one redacted two-document call | Control Plane accepted exact minimal feasibility evidence；owner accepted W2 engineering objective | engineering-smoke gate complete | parent W2/FU1 closed | no reproduction/effectiveness/P1 inference | RESOLVED_BY_H2_RESUME02_AND_OWNER_ACCEPTANCE | PENDING_THIS_COMMIT | RUN-H2-R02 | 2026-08-02 | RESOLVED |
| W2_ATTEMPT1_EVIDENCE_BLOCKER | 2026-08-01 | Stage 6.1 | FU1-W2 Attempt 1 review | LOCAL + RTX5090 | high | original archive omitted repository/disk capture；Correction 01 omitted exact command provenance | Attempt 1 classification and H1 start were blocked | Attempt 1 classification and H1 recovery gate | original `6acdbb...170f`；Correction 01 `d911063e...5279e`；Correction 02 `fcfa3f...3622`；[review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_attempt1_control_plane_review.md) | verify all indexed archives and raw command-derived evidence | Correction 02 safe/index `17/17`, exact GNU `du 9.4`, raw values/exits/counts/spec/no-mutation and materiality `11/11` pass | additive Correction 02 | no inference of model load/scores/runtime/compatibility/security effectiveness | RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW | PENDING_THIS_COMMIT | N/A | 2026-08-01 | RESOLVED |
| BLK-S6.1-FE-001 | 2026-07-31 | Stage 6.1 | future formal experiment | RTX5090 | high | full corpus/index, threshold calibration and selected generator/model/service environment are unvalidated | a future formal run environment is not frozen | formal experiment only | FU1 dependency classification | core vs indexing dependencies separated | completed at source level | later targeted formal compatibility validation | not approved | do not infer from W2 core smoke | NOT_RECORDED | N/A | N/A | NOT_RECORDED | OPEN |

### 12.3 Historical Summary View

| Blocker ID | 首次发现 | 类别 | 严重级别 | 影响范围 | 状态 | 当前证据 | 临时处理 | 最终解决条件 | 下一动作 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BLK-HIST-001 | 2026-07-19 | 历史完整性 | medium | Stage 1–5 hash 检查 | `ACCEPTED_TECHNICAL_DEBT` | [学习记录](../../deliverables/learning_notes.md) 的 CRLF/LF 留痕 | Git diff/blob 核验 | 新的跨平台基线方案经批准 | 不重写历史文件 |
| BLK-HIST-002 | 2026-07-19 | 可复现性 | medium | Stage 1–4.1 | `OPEN` | 本账本 `NOT_RECORDED` 字段 | 保留原始路径和摘要 | 新实验采用 Run Manifest | 不倒填旧事实 |
| BLK-HIST-003 | 2026-07-19 | 类型检查 | low | legacy Stage 5 | `ACCEPTED_TECHNICAL_DEBT` | 全量 MyPy 的既有 legacy 告警 | scoped MyPy | 历史资产单独批准后修复 | 不修改 legacy |
| BLK-S6-001 | 2026-07-22 | 设计/协议 | high | S6-T5.3 | `RESOLVED` | [阻断记录](s6_t5_3_protocol_blocker_record.md) | `RESOLVED_BY_VERSIONED_PUBLIC_METADATA_CONTRACT`；不伪造 parent ID、不读取语料、不改写 schema `1.0` | P1 离线回归 | DenseRetriever 继续保持 fail-closed |
| BLK-S6-004 | 2026-07-25 | 设计/协议 | high | S6-T5.4 | `RESOLVED` | [S6-T5.4 blocker](s6_t5_4_protocol_blocker_record.md) | `RESOLVED_BY_APPROVED_PROTOCOL_FREEZE`；保留 fail-closed 历史 | 协议与实现验收已完成 | 不改写原 blocker evidence |
| BLK-S6-002 | 当前 | 研究缺口 | high | RAG 安全结论 | `OPEN` | 第 10 节 | 不夸大工程验证 | 完成受控正式实验 | 先获批 DenseRetriever |
| BLK-S6-003 | 当前 | 环境依赖 | medium | 真实 Embedding/Chroma | `MITIGATED` | S6-T4 真实集成记录 | 环境变量显式开启、临时目录 | 固定可复现环境文档 | 仅按批准运行 |
| BLK-API-001 | 2026-06-30 | 真实 API 成本/策略 | medium | Groq 扩样 | `OPEN` | [Stage 3/4 文档](../../deliverables/stage3/06_troubleshooting.md) | safe 模式和小样本 | 批准预算和实验设计 | 不无控制扩样 |
| BLK-DOC-001 | 2026-07-20 | 文档漂移 | low | 早期 S6-T5 架构索引/设计快照 | `OPEN` | Git 已有 `4c12181`，但部分历史文本仍称 Python 未开始 | 当前状态与本记录作为动态事实入口 | 在不改写历史叙述前提下添加历史快照说明 | 后续治理审查 |
| BLK-S6.1-LR1-001 | 2026-07-31 | strict comparison 准入 | high | Paper 1 strict comparison | `OPEN` | [Artifact Registry](../research/stage6_1_hidden_knowledge_poisoning/external_artifact_registry.md)、accepted R0/FU1 | source artifact and engineering feasibility improved；internal research, strict comparison and redistribution remain separate | later approved P1/formal protocol/environment | await P1 protocol decision |
| R0-I-EVIDENCE-CORRECTION-001 | 2026-07-31 | evidence correctness/provenance | medium | R0 acceptance only | `RESOLVED` | corrected archive/index/matrix verified；GMTP/PoisonedRAG command evidence and SafeRAG bound all-row smoke passed | no acceptance workaround | `RESOLVED_BY_CORRECTED_EVIDENCE` | retain first-return snapshot |
| BLK-S6.1-P1-001 | 2026-07-31 | P1 source planning | high | PoisonedRAG comparison identity | `RESOLVED` | NQ/released-artifact/partial-equivalence contract frozen and L1 identity accepted | no generation-reproduction claim | `RESOLVED_BY_P0_CONTRACT_FREEZE / VALIDATED_BY_LOCAL_L1` | preserve P1 gate |
| BLK-S6.1-P1-002 | 2026-07-31 | P1 source planning | high | GMTP detection comparison | `RESOLVED` | official BEIR/source/model/sample/call path frozen | no runtime claim | `RESOLVED_BY_P0_CONTRACT_FREEZE` | preserve W2 gate |
| BLK-S6.1-FU1-W1-001 | 2026-07-31 | LOCAL artifact validation | high | PoisonedRAG input identity | `RESOLVED_BY_LOCAL_L1 / SUPERSEDED` | exact commit/blob/schema/assembly/hash evidence | no API regeneration claim | PODR-052 + REL-2026-0013 | closed |
| BLK-S6.1-FU1-W2-001 | 2026-07-31 | Worker validation | high | GMTP executable core | `RESOLVED` | resume02 SHA/safe/index `25/25`, H2-A `18/18`, exact models/source/input/environment, one CUDA call and redacted resources/results；PODR-061 owner acceptance | frozen engineering-feasibility only | `RESOLVED_BY_H2_RESUME02_AND_OWNER_ACCEPTANCE` | closed |
| W2_ATTEMPT1_EVIDENCE_BLOCKER | 2026-08-01 | evidence completeness | high | Attempt 1 classification / H1 start | `RESOLVED` | Correction 02 SHA/safe/index `17/17`, exact GNU `du` commands/raw streams, resource/no-mutation and materiality `11/11` pass | preserve earlier fail-closed history；do not infer runtime facts | `RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW` | H1/W2 later completed under separate evidence and owner gates |
| BLK-S6.1-FE-001 | 2026-07-31 | formal environment | high | future formal experiment | `OPEN` | core/index/generation/evaluation dependencies separated | none | validate selected formal data/index/generator/threshold path | formal experiment remains unapproved |

## 13. Failed Run Register

| Record ID | 日期 | Stage | 命令/入口 | 失败现象 | 根因 | 是否影响数据 | 修复/复验 | 证据 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ER-F-S3-20260630-001 | 2026-06-30 | S3 | safe scan wrapper | 无 API 响应或 Eval | PowerShell stderr 与 `ErrorActionPreference=Stop` 冲突 | 否，非有效实验 | 仅原生 garak 调用期间放宽错误处理；后续 scan 完成 | [学习记录](../../deliverables/learning_notes.md) |
| ER-F-S4-20260630-001 | 2026-06-30 | S4 | `runs/20260630_175419` | 上游 403 | Proxy 上游网络/权限诊断不足 | 否，不计 ASR | 增加脱敏诊断，做单变量直连 | [学习记录](../../deliverables/learning_notes.md) |
| ER-F-S4-20260630-002 | 2026-06-30 | S4 | `runs/20260630_180237` | Proxy 路径 403，直连成功 | `NO_PROXY` 作用域错误 | 否，不计 ASR | 仅在 garak 子进程设置；`222810` 回归完成 | [学习记录](../../deliverables/learning_notes.md) |
| ER-F-S6-20260720-001 | 2026-07-20 | S6-T5.1 | TDD Red | 缺少导出/包导致 collection error | 预期 Red 阶段 | 否，预期测试失败 | 实现后 Green，通过定向与回归测试 | [学习记录](../../deliverables/learning_notes.md) |

预期 TDD Red 不被归类为项目缺陷；它证明测试先于实现。失效/失败运行保留在账本中，后续成功不得删除这些记录。

## 14. Approval Gate Register

| Gate ID | 当前任务 | 已完成证据 | 人工验收状态 | 获批后可开始 | 仍禁止 | 负责人 |
| --- | --- | --- | --- | --- | --- | --- |
| GATE-GOV-PO-MHEP | Highest internal execution authority | canonical principle、authority/startup/context persistence contracts、owner decision and governance tests | `HUMAN_ACCEPTED / PERMANENT` | applies as mandatory governance to all tasks | cannot alter L0 facts or auto-approve any execution | 项目负责人 |
| GATE-GOV-ER1 | Experiment Master Record | 本文、入口同步、治理测试、GOV-ER1-H1 十列账本加固 | `HUMAN_ACCEPTED` | 已完成 | 不自动批准 S6-T5.4 | 项目负责人 |
| GATE-S6-T5.2 | Retrieval Runtime Contracts and IDs | `4c12181`、完成记录、回归测试 | `HUMAN_ACCEPTED` | 已批准 S6-T5.3 | S6-T5.4 及以后 | 项目负责人 |
| GATE-S6-T5.3 | Provider-Neutral DenseRetriever | P1 metadata contract、H1 hardening、完成记录、离线 TDD 证据 | `HUMAN_ACCEPTED` | 不自动批准任何后续任务 | ContentResolver 及以后 | 项目负责人 |
| GATE-S6-T5.4 | Controlled Corpus ContentResolver | P1、I1、H1 人工验收、合成内存实现、定向/架构/隔离测试 | `HUMAN_ACCEPTED_ENGINEERING_VALIDATION` | 已被独立 S6-T5.5 验收所继承 | S6-T5.6 及以后 | 项目负责人 |
| GATE-S6-T5.5 | EvidenceEnvelope、Citation Contracts and Structural Rendering | P1/P1-H1 协议验收、I1/H1 实现验收、离线工程与治理验证 | `HUMAN_ACCEPTED_ENGINEERING_VALIDATION` | 不自动批准任何后续任务 | S6-T5.6 及以后 | 项目负责人 |
| GATE-S6-T5.6-P1 | Context Package Boundary Freeze | 临时 Binding、最终 renderer 预算、safe trace 与 abstention 协议 | `DESIGN_FREEZE_HUMAN_ACCEPTED` | 父任务可单独申请实现审批 | S6-T5.6-I1 及以后 | 项目负责人 |
| GATE-S6-T5.6-P1-H1 | Sequential Resolution and Context Trace Hardening | 顺序正文解析、精确 UID 投影、预算 cutoff 与 trace identity | `DESIGN_FREEZE_HARDENING_HUMAN_ACCEPTED` | 父任务可单独申请实现审批 | S6-T5.6-I1 及以后 | 项目负责人 |
| GATE-S6-T5.6-P1-H2 | Active Specification, Trace Decision and Package Identity Closure | 活动顺序、instruction-budget candidate decision、Trace decision partition 与非冗余 Package identity | `DESIGN_FREEZE_HARDENING_HUMAN_ACCEPTED` | 父任务可单独申请实现审批 | S6-T5.6-I1 及以后 | 项目负责人 |
| GATE-S6.1-R0-B0 | RTX5090 Compute Worker Bootstrap | WSL GPU、PyTorch FP16/BF16、Git branch/tag sync | `HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY` | R0 可按独立批准开始 | 不证明 baseline/Paper result | 项目负责人 |
| GATE-S6.1-R0 | Reproduction Environment and Baseline Feasibility Validation | LR1/Bootstrap accepted；original and corrected evidence verified；blockers normalized | `HUMAN_ACCEPTED_WITH_BLOCKERS` | owner may separately approve R0-FU1 | R0-FU1 execution、S6.1-P1、formal experiment | 项目负责人 |
| GATE-S6.1-R0-I | Control Plane evidence review | historical return preserved；corrected archive `12/12` and matrix verified；three corrections passed | `HUMAN_ACCEPTED_WITH_BLOCKERS` | owner decision on R0-FU1 | automatic R0-FU1、S6.1-P1、formal experiment | 项目负责人 |
| GATE-S6.1-R0-FU1-P0 | Targeted baseline source/contract freeze | NQ/attack identity、official BEIR、GMTP detector core、SafeRAG artifacts、L1/W2 candidates | `HUMAN_ACCEPTED` | L1 completed locally；owner may separately approve W2 | automatic Worker execution、S6.1-P1、formal experiment | 项目负责人 |
| GATE-S6.1-R0-FU1-L1 | Released PoisonedRAG artifact/schema/assembly validation | exact commit/blob/SHA；100x5 schema；official assembly；five ordered hashes plus aggregate | `HUMAN_ACCEPTED` | former W1 superseded；owner may decide W2 | attack-generation reproduction claim、automatic W2/P1 | 项目负责人 |
| GATE-S6.1-R0-FU1-W2 | GMTP detection-core compatibility smoke | exact repo/source/input/model/parameter/environment/resource/output contract；resume02 `25/25`；H2-A `18/18`；one H2-B call | `HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED` | engineering gate complete | P1、formal experiment、metrics、reproduction/effectiveness/paper/security claims | 项目负责人 |
| GATE-S6.1-R0-FU1-W2-ATTEMPT1 | Worker evidence completeness review | original + Correction 01 + Correction 02 SHA/safety/index/binding/repository/GNU-disk/no-mutation evidence | `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER` | narrow preflight evidence reusable；H1 artifact-only authority applied | model-load/scores/runtime/compatibility/security inference、W2 acceptance | Control Plane |
| GATE-S6.1-R0-FU1-W2-H1 | Offline Model Artifact Provisioning and W2 Resume | exact snapshots, 17 model files, 19-entry index, 2 GiB gate, safe bundle and sidecar | `OFFLINE_MODEL_ARTIFACTS_VERIFIED_ON_5090 / COMPLETED` | completed as dependency of accepted H2 smoke evidence | automatic new model use、P1 | 项目负责人 |
| GATE-S6.1-R0-FU1-W2-H2 | Offline bundle verification and conditional detection-core resume | H2-A `18/18`; frozen environment/offline local model load; exactly one fixed call; archive/index `25/25` | `ENGINEERING_SMOKE_COMPLETED / CONTROL_PLANE_REVIEW_PASS / HUMAN_ACCEPTED_AS_W2_EVIDENCE` | complete | retry/rerun/mutation/network、P1/formal claims | Control Plane reviewed；项目负责人 accepted as W2 evidence |
| GATE-S6.1-R0-FU1-W2-H2-RESUME-02 | Additive evidence namespace rollover | resume_01 unchanged；resume02 archive SHA `58da856a...f563`; safe members；index `25/25`; H2-A/H2-B/resource evidence | `CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED` | accepted as W2 engineering evidence | second call、resume_03、reproduction/effectiveness/P1 claims | Control Plane / PODR-061 |
| GATE-S6.1-P1-CANDIDATE | Historical Paper 1 formal protocol and Benchmark specification candidate | RQ1-5, schema, HKP/S, hard negatives, five views, Tracks, metrics, statistics, evidence/resource/license and detox A/B/C | `CONTRACT_CANDIDATE / SUPERSEDED_AT_CANDIDATE_LEVEL_BY_P1-R1` | preserved as historical design input | Dataset、Detector、Training、Formal Experiment、Paper Result | PODR-061 historical gate |
| GATE-S6.1-P1-R1 | P1 protocol hardening and Option B scope freeze | owner-confirmed Option B；RQ1-6；group-aware Benchmark/splits；field visibility；baseline fairness；safety/utility co-primary outcomes；statistics、Pilot、resource、evidence、license and 20 entry conditions | `HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK` | numeric parameters and formal freeze remain separate | Dataset freeze、Detector/Retrieval Intervention implementation、Training、Formal Experiment、Paper Result | 项目负责人 / PODR-062 |
| GATE-S6.1-P1-PILOT4-SECOND-PREFLIGHT | repaired Pilot4 preannotation review | repaired 12-row sample；mutation/stealth/echo/visibility/applicability/G1–G14/Round D evidence | `READY_FOR_SECOND_OWNER_PREFLIGHT / NO_HUMAN_DISTRIBUTION` | owner accepts or requests targeted repair；PASS still needs separate A/B approval | automatic A/B、agreement、GT、240-group、Dataset freeze、Detector/Training、5090、Formal Experiment | 项目负责人 / PODR-072 |
| GATE-S6.1-P1-PILOT4-FINAL-PREFLIGHT | Repair-02 final Pilot4 preannotation review | 16-row sample；genuine S3 necessity、natural S1、actual length、template/HN/source/parity、G1–G14/Round D evidence | `READY_FOR_OWNER_REVIEW / NO_HUMAN_DISTRIBUTION` | owner confirms no systemic blocker or requests candidate-local correction | automatic A/B、agreement、GT、240-group、Dataset freeze、Detector/Training、5090、Formal Experiment | 项目负责人 / PODR-074 |
| GATE-S6.1-P1-PILOT4-EXTERNAL-BLIND-RETURN | External label-blind semantic review return | isolated reviewer receives only opaque-ID candidate/E1/E2/guide and returns 11 fields with reasoning | `WAITING_FOR_EXTERNAL_OWNER_REVIEW / NO_HUMAN_DISTRIBUTION` | later separately approved mapping unlock and expected comparison | current comparison、protocol acceptance、A/B、agreement、GT、240-group、Dataset freeze、Detector/Training、5090、Formal Experiment | 项目负责人 / PODR-077 |
| GATE-S6.1-R0-FU1-W2-CORRECTION-02 | Command-derived disk measurement evidence | archive SHA `fcfa3f...3622`, safe `17/17`, GNU `du 9.4`, raw streams/exits/counts/no-mutation, materiality `11/11` | `CONTROL_PLANE_REVIEW_PASS / FINAL_CLOSURE_APPLIED` | historical evidence blocker closed | rerun/repackaging churn、GMTP/model load、P1/formal experiment | RTX5090 evidence；Control Plane accepted |

**当前审批顺序**：既有 S6-T5 验收历史保持不变；S6.1-LR1、Context Recovery、Paper-First 和 current route 已接受；
PO-MHEP is `HUMAN_ACCEPTED / HIGHEST_INTERNAL_PROJECT_EXECUTION_AUTHORITY / PERMANENT` and applies without changing L0 facts；
`S6.1-R0-B0` 已 `HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY`；historical R0 execution approval remains preserved；
historical R0-I `RETURNED_FOR_WORKER_CORRECTION` remains preserved；the superseding decision is
`S6.1-R0 = HUMAN_ACCEPTED_WITH_BLOCKERS`。R0-FU1 is `HUMAN_ACCEPTED / CLOSED`；P0/L1 are
`HUMAN_ACCEPTED`；the former Worker W1 is `SUPERSEDED_BY_LOCAL_L1 / NOT FAILED`；W2 is
`HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED`。Attempt 1 is `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER`;
the historical evidence blocker is resolved；H1 artifacts are verified on 5090；H2 resume_01 remains valid blocked evidence with
H2-B not executed/call_count zero；resume_02 is `CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED` with the
single H2-B authorization consumed。Option B is confirmed at scope level；P1-R1 is
`HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK` with numeric/formal freezes open。Pilot0–2 feasibility gates are closed，Pilot3 is
diagnostic only，and Pilot4 Repair-02 is final-preannotation pending Owner review。A/B 72 annotation、240-group、Dataset、
Formal Detector、Retrieval Intervention effectiveness、training and formal RAG experiment remain unapproved/not started。

## 15. 当前结论边界

### EVIDENCE_BACKED

- Stage 3 已完成 Groq `llama-3.1-8b-instant` 的两条真实攻击 smoke；PromptInject 命中，Base64 存在 detector PASS 但人工复核显示危险解码的案例。
- Stage 4 已在相同 prompt hash 下观察到规则型 guarded 组 ASR 从 50% 到 0%。
- Stage 4.1 已独立验证 output-only 先调用上游、记录原始输出 hash、再替换危险输出。
- Stage 5/Stage 5 Paper 已保存确定性 Mock 的攻击矩阵、AttemptRecord、T1–T9、验证器与报告。
- Stage 6 已建立 embedding/vector store、chunking 与检索运行时契约的工程边界和标签隔离基础。

### INFERENCE

- Stage 3 Base64 案例表明仅依赖当前 garak detector 的 PASS/FAIL 可能漏掉部分危险行为，因而需要人工复核或多 detector；这是对当前样本的推断，不是全模型统计结论。

### PLANNED

- DenseRetriever、ContentResolver、ContextBuilder、Citation Accuracy、Trust-aware Retrieval、R1–R6 正式攻击矩阵、Stage 6.1/6.2、Stage 7。

### NOT_ESTABLISHED

- 正式 RAG 安全实验、抗知识污染能力、可信检索、生产级防护率、统计显著性、论文投稿/发表和 Agent 安全效果。

## 16. 证据地图

| 能力/结论 | 原始结果 | 日志 | 摘要 | 测试/设计 | Commit | 证据等级 |
| --- | --- | --- | --- | --- | --- | --- |
| garak 最小扫描闭环 | [S1 JSONL](../../deliverables/stage1/stage1_min_scan.report.jsonl) | `NOT_RECORDED` | [S1 report](../../deliverables/stage1/stage1_report.md) | S1 学习材料 | `NOT_RECORDED` | `E2_UNIT_VALIDATED` |
| OpenAI-compatible Mock 对照 | [S2 JSON](../../deliverables/stage2/stage2_scan_result.json) | [API JSONL](../../deliverables/stage2/api_requests.jsonl) | [S2 summary](../../deliverables/stage2/stage2_scan_summary.md) | Mock API 文档 | `NOT_RECORDED` | `E4_FORMAL_SINGLE_RUN` |
| Groq 真实小样本扫描 | [S3 JSON](../../deliverables/stage3/groq_scan_result.json) | [run log](../../deliverables/stage3/runs/20260630_154855-safe/stage3_console.log) | [S3 analysis](../../deliverables/stage3/08_first_real_scan_analysis.md) | garak 原始 JSONL | `NOT_RECORDED` | `E4_FORMAL_SINGLE_RUN` |
| Guard A/B | [S4 JSON](../../deliverables/stage4/guarded_groq_scan_result.json) | [guard logs](../../deliverables/stage4/guard_logs.jsonl) | [S4 summary](../../deliverables/stage4/guarded_groq_scan_summary.md) | parity 记录 | `NOT_RECORDED` | `E4_FORMAL_SINGLE_RUN` |
| Input/Output 消融 | [S4.1 JSON](../../deliverables/stage4_ablation/ablation_result.json) | [logs](../../deliverables/stage4_ablation/logs/20260630_230629/) | [S4.1 summary](../../deliverables/stage4_ablation/ablation_summary.md) | output-only 验证 | `NOT_RECORDED` | `E4_FORMAL_SINGLE_RUN` |
| Stage 5 Mock 矩阵 | [manifest](../../deliverables/stage5/logs/20260701T030819Z-05703f/run_manifest.json) | [attempts](../../deliverables/stage5/logs/20260701T030819Z-05703f/attempts.jsonl) | [summary](../../deliverables/stage5/logs/20260701T030819Z-05703f/run_summary.md) | validators | `NOT_RECORDED` | `E5_REPEATED_CONTROLLED_EXPERIMENT` |
| S6-T4 基础设施 | `NOT_RECORDED` | `NOT_RECORDED` | [ADR](../architecture/0007_embedding_vectorstore_boundary.md) | 真实集成测试 | `3950c47` | `E3_INTEGRATION_VALIDATED` |
| S6-T5.2 契约 | `NOT_RECORDED` | `NOT_RECORDED` | [completion record](s6_t5_2_completion_record.md) | 定向/架构/隔离测试 | `4c12181` | `E2_UNIT_VALIDATED` |

## 17. 项目交接指南

新成员接手顺序：

1. 阅读 [AGENTS.md](../../AGENTS.md)；
2. 阅读 [长期需求](long_term_research_requirements.md)；
3. 阅读 [项目总控](../../PROJECT_MASTER_CONTEXT.md)；
4. 阅读 [当前任务状态](current_work_state.md)；
5. 阅读本文；
6. 阅读当前 Stage 的设计规格与实施计划；
7. 检查 Git 状态与审批门；
8. 打开最近正式实验或工程验证的原始证据；
9. 运行当前任务允许的快速验证命令。

通用 Git 检查命令：

```powershell
git branch --show-current
git rev-parse HEAD
git status --short
git rev-list --left-right --count @{upstream}...HEAD
git log -15 --oneline
```

检查历史资产未被覆盖：使用 `git diff --name-only HEAD -- deliverables data/stage5 src/codeguarder`，并遵守历史完整性测试的 CRLF/LF 技术债说明。检查密钥与 runtime：运行 task-scoped secret scan，确认 `runtime/` 仍由 `.gitignore` 覆盖。

## 18. 每次运行记录模板

```text
## Run Record: ER-<STAGE>-<YYYYMMDD>-<NNN>

- Record ID:
- Original Run ID:
- Run Type:
- Date/Time UTC:
- Stage/Task:
- Research Question:
- Hypothesis:
- Branch:
- Git Commit:
- Environment:
- Model:
- Model Revision:
- API/Provider:
- Dataset:
- Dataset Hash:
- Configuration:
- Command:
- Guard Mode:
- Random Seed:
- Sample Count:
- Status:
- Primary Metrics:
- Secondary Metrics:
- Raw Outputs:
- Logs:
- Summary:
- Failed Cases:
- Blockers:
- Claims Supported:
- Claims Not Supported:
- Reviewer:
- Acceptance Status:
```

所有未知字段必须填 `NOT_RECORDED`，不能留空。

## 19. 持续更新协议

以下事件必须触发更新：新正式实验、smoke test、工程验证、失败运行、新 blocker/解除 blocker、审批门变化、阶段验收、指标/数据/模型/revision 变化、结果路径变化、结论边界变化、任务废弃或替代。

每次更新按以下顺序执行：

1. 读取原始证据；
2. 新增或更新对应 Run Record；
3. 更新阶段仪表盘、Blocker、Approval Gate 和结论边界；
4. 更新 Change Log；
5. 检查全部相对链接、绝对路径和密钥；
6. 运行治理测试；
7. 提交并推送。

正式 Run Record 默认 append-only。错误修正必须写 Change Log；无效运行标记 `INVALIDATED`，不能删除；失败记录不能因后续成功而删除；派生摘要必须可追溯到原始结果。

## S6-T5.6-I1-H1 Candidate Hardening Record (2026-07-26)

- Status: `Completed, pending human acceptance`.
- Scope: only Trace scenario invariants, Package public configuration identity, injected dependency error redaction, and abstention/Trace correspondence.
- Evidence: [H1 completion record](s6_t5_6_i1_h1_completion_record.md), targeted tests, full offline retrieval/architecture/label-isolation regression, Ruff and scoped MyPy.
- Historical boundary: `71067d1` remains the initial I1 candidate history; last accepted implementation commit remains `6da27a6`.
- Non-claims: no fixture/data read or modification, model invocation, formal RAG security experiment, retrieval-quality conclusion, Citation Accuracy conclusion, or production-readiness conclusion.

## GOV-S6-T5.6-ACCEPTANCE: Deterministic Context Package Final Acceptance (2026-07-26)

- Status: `HUMAN_ACCEPTED` for `S6-T5.6-I1-H1`, `S6-T5.6-I1` and parent `S6-T5.6`; P1, P1-H1 and P1-H2 remain `HUMAN_ACCEPTED`.
- Final accepted implementation commit: `b136ee2`; initial candidate implementation history: `71067d1`; previous accepted implementation commit: `6da27a6`.
- Accepted boundary: synthetic/offline ContextBuildConfig, ContextBuildTrace, RetrievedContextPackage, DeterministicContextBuilder, stable sort, exact duplicate handling, sequential resolution, stable-prefix budget selection, package-local Citation allocation, Unicode/UTF-8 identity, structural abstention, Trace scenario invariants, public config hash binding, dependency redaction, reason/Trace correspondence and safe audit.
- Final validation evidence: complete Stage 6 offline regression `438 passed, 2837 subtests passed`; Ruff and scoped MyPy passed. `421/2796`, `437/2796` and `438/2833` are dated pre-final-validation snapshots, not current acceptance figures. The four-subtest increase from `2833` comes from governance assertions added during acceptance-state synchronization.
- Non-claims: retrieval quality, prompt-injection defense, knowledge-poisoning detection, Citation Accuracy, trustworthy retrieval, Chroma/MiniLM/LLM full chain, formal RAG security experiment and production readiness.
- Next gate: `S6-T5.7+` remains `NOT APPROVED`; Formal RAG security experiment remains `NOT STARTED`.

## S6-T5.7 Controlled Retrieval Context Pipeline Integration Validation (2026-07-26)

- Status: `HUMAN_ACCEPTED`.
- Evidence: [completion record](s6_t5_7_integration_completion_record.md), static integration, explicit MiniLM + temporary Chroma integration, offline and architecture regressions.
- Scope: candidate interoperability evidence for existing accepted components only; no new pipeline business module and no frozen contract modification.
- Claim boundary: no retrieval-quality, security-effectiveness, Citation Accuracy, trustworthy-retrieval, LLM-generation, formal-experiment or production-readiness claim.
- Integrity: the legacy SHA-256 manifest still reports its accepted CRLF/LF baseline debt; Git protected-path diff confirms this task did not modify Stage 1-5 or Stage 6 fixture/data.
- Acceptance: project owner accepted this documented integration evidence. `b6cedf3` is the accepted integration evidence commit, not an implementation commit; last accepted implementation commit remains `b136ee2`.
- Environment note: the opt-in real MiniLM test uses `local_files_only=False`; a new environment may download the pinned revision only when explicitly enabled. Default offline regression does not depend on network access or model download.
- Next gate: the project owner must separately decide whether to approve `S6-T5.8`. It remains `NOT APPROVED`; formal RAG security experiment remains `NOT STARTED`.

## 20. Change Log

| 日期 | 变更类型 | 影响章节 | 变更原因 | 证据 | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-07-20 | 建立 | 全文 | 创建唯一实验总记录，回填 Stage 1–5、登记 Stage 6 工程状态和当前审批门；未进入 S6-T5.3 | 本文链接的原始工件与 Git 历史 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-20 | 账本结构加固 | 第 2、8、14、20 节 | 修复 S3、S4、S4.1、S5 与 S5 Paper 的十列字段错位；新增列数、枚举、唯一性和计数一致性测试；不改写历史运行事实 | 本文第 8 节、治理测试和学习记录 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-21 | 人工审批状态更新 | 第 2、12、14、20 节 | 项目负责人验收 GOV-ER1、GOV-ER1-H1、S6-T5.2，并批准 S6-T5.3 启动；S6-T5.4+ 与正式 RAG 安全实验仍未批准 | 当前工作状态、审批文本与 Git 历史 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-21 | 协议 blocker 留痕 | 第 2、4、12、14、20 节 | S6-T5.3 启动前发现 hit-to-evidence 缺少必填 `parent_doc_id`；按冻结契约、无正文和标签隔离边界暂停实现 | [S6-T5.3 blocker record](s6_t5_3_protocol_blocker_record.md)、当前工作状态 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-22 | P1 修复与 DenseRetriever 完成 | 第 2、4、12、14、20 节 | schema `1.1` 传递公开 parent identity；Provider-Neutral DenseRetriever 经离线 TDD 验证后等待人工验收 | [完成记录](s6_t5_3_completion_record.md)、[blocker record](s6_t5_3_protocol_blocker_record.md) | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-22 | S6-T5.3-H1 验收加固 | 第 2、4、12、14、20 节 | candidate_count 改为 raw query hits，补齐 store provenance 与脱敏失败边界；仍是离线工程验证、等待人工复核 | [完成记录](s6_t5_3_completion_record.md)、定向 TDD | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | S6-T5.3 人工验收登记 | 第 2、4、10、14、15、20 节 | 项目负责人验收 GOV-PODR1、S6-T5.3-P1、S6-T5.3-H1 和 Provider-Neutral DenseRetriever；验收不改变工程验证分类，不批准 S6-T5.4 或正式 RAG 实验 | [完成记录](s6_t5_3_completion_record.md)、[决策登记册](project_owner_decision_register.md)、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | S6-T5.4 协议 blocker | 第 2、4、10、12、14、20 节 | 项目负责人已批准启动范围，但 Resolver 返回/权限、snapshot reader、legacy mapping 和 error ownership 未冻结；按 fail-closed 原则停止实现 | [blocker record](s6_t5_4_protocol_blocker_record.md)、冻结规格/ADR 审查 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | S6-T5.4-P1 协议冻结 | 第 2、4、10、12、14、20 节 | 冻结 ContentResolver 输入/返回、正文能力 DTO 所有权、受控 snapshot reader、legacy exact-match mapping 与错误层级；P1 完成但待人工验收，未实现正文解析 | [blocker record](s6_t5_4_protocol_blocker_record.md)、PODR-013、设计规格、ADR | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | GOV-S6-T5.4-P1-ACCEPTANCE | 第 2、4、10、12、14、20 节 | 项目负责人接受 P1 协议设计，将 blocker 标记为 RESOLVED_BY_APPROVED_PROTOCOL_FREEZE；S6-T5.4 仅进入独立实现审批等待状态 | [blocker record](s6_t5_4_protocol_blocker_record.md)、PODR-014、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | S6-T5.4-I1 受控正文解析最小实现 | 第 2、4、10、14、20 节 | 仅用合成内存正文实现 `ContentRef + expected hash -> ResolvedContent`、受控 snapshot registry/reader 与 legacy exact-match adapter；未读取 Stage 6 fixture，待人工验收 | [completion record](s6_t5_4_completion_record.md)、PODR-015、定向/架构/隔离测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | S6-T5.4-H1 capability/failure-boundary 加固 | 第 2、4、10、14、20 节 | 删除公开 registry capability；将注入 adapter/registry/reader 的领域异常按受信 type/code 重新构造为固定脱敏外部错误，未知或交叉 code fail closed 为 runtime；仅合成内存测试，待人工复核 | [completion record](s6_t5_4_completion_record.md)、定向/架构/隔离测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | GOV-S6-T5.4-ACCEPTANCE | 第 2、4、10、12、14、20 节 | 项目负责人接受 P1、I1、H1 与父任务；保持工程验证分类，不批准 S6-T5.5、ContextBuilder、Citation 或正式 RAG 实验 | [completion record](s6_t5_4_completion_record.md)、PODR-016、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-25 | S6-T5.5-P1 协议审查 | 第 2、4、12、14、20 节 | 冻结无 `citation_id` Envelope、由未来 ContextBuilder 创建的 package-local CitationBinding、确定性 instruction/XML escaping 和默认关闭敏感导出；未创建业务代码或实验结果，待人工验收 | [protocol review record](s6_t5_5_protocol_review_record.md)、规格、计划、ADR、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-26 | S6-T5.5-P1-H1 协议加固 | 第 2、4、12、14、20 节 | Factory 只接收 canonical Evidence；legacy `chroma:` 只在 Resolver 输入边界；renderer 只消费 Envelope + Binding，七项 identity mismatch 以 `CITATION_BINDING_MISMATCH` fail closed；无源码或实验结果，待人工复核 | [protocol review record](s6_t5_5_protocol_review_record.md)、规格、计划、ADR、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-26 | GOV-S6-T5.5-P1-ACCEPTANCE | 第 2、4、12、14、20 节 | 项目负责人接受 P1 与 H1 协议；S6-T5.5 仅进入独立实现审批准备，I1 未批准；不创建业务源码或实验结果 | [protocol review record](s6_t5_5_protocol_review_record.md)、PODR-019、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-26 | S6-T5.5-I1 最小 Evidence/Citation 实现 | 第 2、4、12、14、20 节 | 仅用 synthetic Evidence/ResolvedContent 实现 Envelope、Binding、CitationMode、canonical Factory、instruction 与单 block rendering；不创建 package/allocator/ContextBuilder，不读 fixture、不调用模型 | [completion record](s6_t5_5_completion_record.md)、定向/架构/隔离测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-26 | S6-T5.5-H1 I1 验收发现项加固 | 第 2、4、12、14、20 节 | 仅修复 metadata 不可变、timestamp 兼容、canonical Evidence UID 与固定错误语义；不创建 ContextBuilder/Package/allocator，不读 fixture、不调用模型 | [protocol review record](s6_t5_5_protocol_review_record.md)、[completion record](s6_t5_5_completion_record.md)、TDD/离线回归 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-26 | GOV-S6-T5.5-ACCEPTANCE | 第 2、4、10、12、14、20 节 | 项目负责人接受 I1、H1 与父任务；保留 `2cacef7` 初始实现历史，以 `6da27a6` 作为最终接受实现提交；不批准 S6-T5.6+ 或正式 RAG 实验 | [completion record](s6_t5_5_completion_record.md)、[protocol review record](s6_t5_5_protocol_review_record.md)、PODR-022、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-26 | S6-T5.6-P1 Context Package 协议审查 | 第 2、4、10、12、14、20 节 | 冻结临时 Binding 的精确 renderer 预算、稳定前缀选择、safe build trace、Package 和结构性 abstention；不创建业务源码或实验结果，待人工验收 | [protocol review record](s6_t5_6_protocol_review_record.md)、PODR-023、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-26 | S6-T5.6-P1-H1 协议加固 | 第 2、4、10、12、14、20 节 | 修订 P1 的全量预解析缺口：预算选择与正文解析顺序化，冻结精确 UID 重复投影、cutoff 不访问正文与 trace/package 单向身份；不创建源码或实验结果，待人工复核 | [protocol review record](s6_t5_6_protocol_review_record.md)、PODR-024、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-26 | S6-T5.6-P1-H2 协议闭环 | 第 2、4、10、12、14、20 节 | 清除活动章节的旧顺序，冻结 instruction-budget candidate decision、Trace tuple partition 与 Package/Trace 无冗余 identity；不创建源码或实验结果，待人工复核 | [protocol review record](s6_t5_6_protocol_review_record.md)、PODR-025、治理测试 | 通过 `git log -1 -- docs/governance/experiment_master_record.md` 动态解析 |
| 2026-07-26 | GOV-S6-T5.6-P1-ACCEPTANCE | 第 2、4、10、12、14、20 节 | 项目负责人接受 P1、P1-H1 与 P1-H2 的未来 Context Package 协议；父任务仅进入 `READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`，`S6-T5.6-I1` 仍未批准。`6da27a6` 保持最后已接受 implementation commit，`432b07e` 仅为协议闭环提交 | [protocol review record](s6_t5_6_protocol_review_record.md)、PODR-026、治理测试 | 不创建源码、不读 fixture、不调用模型 |
| 2026-07-26 | S6-T5.6-I1 实施批准 | 第 2、4、10、12、14、20 节 | 项目负责人批准合成离线 TDD 实现 Context Config/Trace/Package 与唯一 ContextBuilder；I1 和父任务进入 `IMPLEMENTATION_IN_PROGRESS`，新提交尚不属于 last accepted implementation | PODR-027、当前任务指令、已验收协议 | 不读 fixture、不调用 Embedding/Chroma/LLM、不进入 Trust、S6-T5.7 或正式实验 |
| 2026-07-26 | GOV-S6-T5.7-ACCEPTANCE | 第 2、12、14、20 节 | 项目负责人接受既有检索到 Context Package 受控集成验证；`b6cedf3` 仅为集成证据提交，`b136ee2` 仍为最后已接受 implementation commit；S6-T5.8 与正式实验未获批准 | [S6-T5.7 completion record](s6_t5_7_integration_completion_record.md)、PODR-031、治理测试 | 本轮纯治理提交，未改业务源码、测试 fixture/data 或历史资产 |
| 2026-07-26 | S6-T5.8 baseline documentation closure | 第 2、4、12、14、20 节 | 汇总 S6-T5.1--T5.7 的脱敏证据、提交身份、测试快照、环境说明和技术债；候选 closure 完成但等待人工验收，不创建 accepted baseline SHA、tag 或 Stage 6.1 分支 | [baseline report](s6_t5_baseline_acceptance_report.md)、PODR-032、治理测试 | 纯文档/治理候选，未改业务源码、历史资产或 fixture/data |
| 2026-07-26 | S6-T5.8-H1 evidence taxonomy hardening | 第 2、4、12、14、20 节 | 将基线矩阵拆分为 protocol design/hardening/acceptance、implementation/hardening/acceptance、integration evidence/acceptance；原始 closure `37cccdc` 仅作候选事实，不是 accepted baseline SHA | [baseline report](s6_t5_baseline_acceptance_report.md)、PODR-033、语义治理测试 | 纯文档/治理候选，未改业务源码、历史资产或 fixture/data |
| 2026-07-27 | GOV-S6-T5-BASELINE-ACCEPTANCE | 第 2、4、12、14、20 节 | 项目负责人接受 S6-T5.8-H1、S6-T5.8 与整个 S6-T5 基线；`4ecf73a` 为 accepted baseline content commit；本轮新提交仅是 baseline governance acceptance commit | [baseline report](s6_t5_baseline_acceptance_report.md)、PODR-034、治理测试 | 不改业务源码/测试 fixture/data；不创建 tag/研究分支；不开始正式实验 |
| 2026-07-31 | S6.1-LR1 research alignment | 第 2、12、14、20 节 | 建立 paper-first 比较证据原则，核验 PoisonedRAG/GMTP/SafeRAG 一手论文、仓库、commit、许可、协议和硬件事实；只形成 Benchmark/复现/双机控制面文档 | [Stage 6.1 research README](../research/stage6_1_hidden_knowledge_poisoning/README.md)、PODR-035、治理测试 | `FORMAL_EXPERIMENT = NOT STARTED`；无数据/模型下载、无 API/模型调用、无实验 Run Record |
| 2026-07-31 | Git-native context recovery governance | 第 1、2、12、17、19、20 节 | 明确本文只做实验控制面；增强 canonical Blocker schema/status；连接 authority map、execution ledger、dual-machine Git sync 和 learning 非权威边界 | [Context Authority Map](context_authority_map.md)、[Research Execution Log](research_execution_log.md)、PODR-036--040、context-persistence tests | 纯治理/文档；不创建实验 Run Record，不改变 S6-T5 baseline 或 Stage 1--5 evidence |
| 2026-07-31 | S6.1-LR1 final human acceptance and R0 definition | 第 2、4、12、14、20 节 | 接受 LR1/Context/Paper-First/current route；拆分 artifact access/use/comparison/redistribution；定义 R0-before-P1 | PODR-041--045、REL-2026-0007、R0 definition、governance tests | R0 未开始；无 external run/data/model/5090/Paper Result |
| 2026-07-31 | RTX5090 Bootstrap acceptance and R0 execution approval | 第 2、4、12、14、20 节 | 接受 Worker base environment/Git/GPU validation；批准 R0-A 至 I；保持 LOCAL 禁止执行与 Formal Experiment stop | PODR-046--047、REL-2026-0008--0009、R0 definition、governance tests | Bootstrap only；无 external baseline/Paper result；R0 尚待 Worker pull 后执行 |
| 2026-07-31 | S6.1-R0-I evidence review and token-economy governance | 第 2、4、12、14、15、20 节 | archive/index integrity passed；exact-upstream review found GMTP sample/Docker mismatch and SafeRAG provenance/coverage gap；returned minimal correction；registered Control-Plane-First principle | [R0-I review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_i_control_plane_review.md)、PODR-048--049、REL-2026-0010、governance tests | `RETURNED_FOR_WORKER_CORRECTION`；no R0 acceptance、R0-FU1/P1/formal execution |
| 2026-07-31 | S6.1-R0 corrected-evidence final acceptance | 第 2、4、12、14、15、20 节 | corrected archive/index/matrix and all three baseline corrections passed；accepted R0 engineering preflight with downstream blockers；historical return preserved | [R0-I review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_i_control_plane_review.md)、PODR-050、REL-2026-0011、governance tests | `HUMAN_ACCEPTED_WITH_BLOCKERS`；R0-FU1 approval recommended but not approved；P1/formal experiment not started |
| 2026-07-31 | S6.1-R0-FU1-P0 targeted resolution | 第 2、4、12、14、20 节 | approved LOCAL-first P0 froze NQ/attack artifact boundary、official GMTP BEIR/call path、SafeRAG artifact contract and exact W1/W2 candidates | [FU1 resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)、PODR-051、REL-2026-0012、governance tests | `COMPLETED_PENDING_OWNER_REVIEW`；W1/W2/P1/formal experiment not approved/not started |
| 2026-07-31 | FU1-P0/L1 acceptance and W2 contract freeze | 第 2、4、12、14、20 节 | owner accepted P0；LOCAL L1 verified exact PoisonedRAG released artifact, whole schema and deterministic assembly；historical W1 superseded；W2 input/model/parameter/environment/resource contract hardened without execution | [FU1 resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)、PODR-052、REL-2026-0013、governance tests | `P0/L1 HUMAN_ACCEPTED`；W2 ready for owner decision but not run；P1/formal experiment closed |
| 2026-08-01 | FU1-W2 execution approval | 第 2、4、12、14、20 节 | owner approved the exact frozen GMTP detection-core smoke on RTX5090；LOCAL registered governance only and did not execute Worker/model/GPU work | [FU1 resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)、PODR-053、REL-2026-0014、governance tests | `W2 APPROVED_TO_START / NOT_YET_EXECUTED`；P1/formal experiment not started |
| 2026-08-01 | W2 Attempt 1 evidence blocker and H1 recovery gate | 第 2、4、12、14、20 节 | archive integrity and partial identities passed, but mandatory main-repository HEAD/clean and disk measurement evidence were absent；stopped before offline downloads；registered 10 GiB resource correction and owner-approved H1 as blocked/not started | [Attempt 1 review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_attempt1_control_plane_review.md)、PODR-054、REL-2026-0015、governance tests | `W2_ATTEMPT1_EVIDENCE_BLOCKER`；no bundle/model/GMTP/P1/formal execution |
| 2026-08-01 | W2 Attempt 1 Correction 01 remains evidence-blocked | 第 2、12、14、20 节 | correction SHA/safe/index/original binding/main repository passed；reported disk values are consistent and under ceiling, but exact `du` commands/flags/raw outputs are absent；H1 did not start | [Attempt 1 review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_attempt1_control_plane_review.md)、PODR-055、REL-2026-0016、governance tests | parent blocker remains open；no model/bundle/GMTP/P1/formal execution |
| 2026-08-01 | GOV-PO-MHEP highest internal execution authority | 第 1、2、4、12、14、15、20 节 | owner established permanent mandatory escalation, LOCAL/Worker sovereignty, forward/paper risk review, physical context persistence and canonical Git sync；prepared Correction 02 candidate only | [PO-MHEP](project_owner_sovereignty_and_mandatory_escalation_principle.md)、PODR-056、REL-2026-0017、governance tests | no Worker contact/execution、H1/model/GMTP/P1/formal experiment；W2 blocker unchanged |
| 2026-08-01 | Correction 02 final evidence correction approval | 第 2、4、12、14、20 节 | owner approved exact GNU apparent/allocated `du` provenance capture on RTX5090 and froze `MATERIALITY_AND_FINAL_CLOSURE_RULE`；LOCAL registered governance only | [FU1 resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)、PODR-057、REL-2026-0018、governance tests | not sent/executed；blocker/H1/P1/formal status unchanged |
| 2026-08-01 | Correction 02 final closure and H1 offline artifacts | 第 2、4、12、14、20 节 | Correction 02 safe/index/GNU provenance/materiality passed；Attempt 1 reclassified valid blocked；exact Contriever/BERT snapshots and safe indexed bundle prepared locally | [Attempt 1 review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_attempt1_control_plane_review.md)、PODR-058、REL-2026-0019、governance tests | H1 pending 5090 verification；no model load/GMTP/GPU；W2/P1/formal not completed or started |
| 2026-08-01 | H2 conditional engineering resume approval | 第 2、4、12、14、20 节 | owner approved 5090 H2-A bundle verification and, only after full pass, exactly one frozen H2-B two-document detection-core call；本机 registered governance only | [FU1 work process](../research/stage6_1_hidden_knowledge_poisoning/stage_process/S6.1-R0-FU1_work_process.md)、PODR-059、REL-2026-0021、governance tests | `NOT SENT / NOT EXECUTED`；no model load/GMTP/GPU on 本机；W2/P1/formal unchanged |
| 2026-08-01 | H2 resume_01 blocker review and resume_02 rollover | 第 2、4、12、14、20 节 | resume_01 missing-bundle blocker evidence passed 本机 safety/index review；owner confirmed bundle sync and approved new immutable evidence namespace only | [FU1 work process](../research/stage6_1_hidden_knowledge_poisoning/stage_process/S6.1-R0-FU1_work_process.md)、PODR-060、REL-2026-0022、governance tests | resume_01 preserved；resume_02 not executed；H2-B/P1/formal unchanged |
| 2026-08-01 | H2 resume_02 Control Plane evidence acceptance | 第 2、4、12、14、20 节 | resume02 SHA/safe/index `25/25`, H2-A `18/18`, exact local CUDA model load, one H2-B call, redacted results/resources and resume_01 no-mutation independently reviewed | [H2 resume02 review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_h2_resume02_control_plane_review.md)、REL-2026-0023、governance tests | minimal feasibility blocker resolved；parent W2 not completed/accepted；P1/formal unchanged |
| 2026-08-02 | Parent W2 engineering-feasibility acceptance and P1 candidate | 第 2、4、12、14、15、20 节 | owner accepted/closed W2 and FU1 only for frozen single-sample engineering feasibility；preserved resume histories；prepared non-authoritative RQ/Benchmark/method/metrics/statistics/detox candidate | [P1 candidate](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_protocol_candidate.md)、PODR-061、REL-2026-0024、governance tests | P1/Dataset/Detector/Training/Formal Experiment not approved/not started；no paper result |
| 2026-08-02 | S6.1-P1-R1 Option B protocol hardening | 第 2、4、12、14、15、20 节 | owner selected Option B；froze Paper 1 to detection plus lightweight hard filtering/soft downweighting；prepared approval-grade RQ1-6, Benchmark, baseline fairness, safety/utility, statistics, Pilot/resource/evidence/license candidate | [P1-R1 candidate](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_r1_protocol_review_candidate.md)、OR-021、PODR-062、REL-2026-0025、governance tests | review candidate only；P1/Pilot/Dataset/Detector/Retrieval Intervention/Training/Formal Experiment not approved or started；no paper result |
| 2026-08-27 | S6.1-P1-PILOT2 targeted re-review kit | 第 2、4、12、14、15、20 节 | 在 immutable raw 与完整 V2 上审计实际问题字段，冻结 A/B Phase1 三字段、Phase2 七字段及 B-only 21+1 process fixes；生成四个带下拉、只读与联动提示的 XLSX，减少每人 37.5% 实质任务 | [targeted record](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_targeted_rereview.md)、PODR-065、OR-027、REL-2026-0031、artifact/schema tests | `READY_FOR_HUMAN_EXECUTION` only；no agreement/adjudication/Dataset/Detector/Training/5090/Formal Experiment/Paper Result |
| 2026-08-28 | PILOT2 targeted V1 mapping correction | 第 2、4、12、14、15、20 节 | 证实 B Phase1 的 108 个旧值被列名后缀误读为 absent；修复 B Phase1 三列和 B Phase2 两列映射，检查 A Phase2，加入非预期缺失/alias 冲突 fail-closed 与 owner 决策树；保留已完成 A Phase1 不变 | [targeted record](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_targeted_rereview.md)、PODR-066、OR-028、REL-2026-0032、builder/artifact tests | `THREE_CORRECTED_WORKBOOKS_READY` only；A1 pending validation/lock；no agreement/adjudication/Dataset/Detector/Training/5090/Formal Experiment/Paper Result |
| 2026-08-28 | Prospective candidate self-containment gate | 第 2、4、12、14、15、20 节 | 冻结后续新候选的主体唯一可识别门；裸指代或无法恢复主体为 `BROKEN_CANDIDATE / MISSING_CONTEXT`，必须重写为新候选或剔除；增加可执行准入记录与 formal-Benchmark fail-closed guard | [research plan authority](../research/stage6_1_hidden_knowledge_poisoning/human/research_plan_authority.md)、PODR-067、OR-029、REL-2026-0033、candidate-admission tests | prospective only；historical Pilot1/Pilot2 unchanged；no Dataset freeze/agreement/experiment |
| 2026-08-31 | PILOT2 post-annotation validation and formal agreement | 第 2、4、12、14、15、20 节 | 四份 targeted return hash-lock；V2-over-V1 解析；conditional applicable-subset agreement；47 A/B disagreements + 37 logic conflicts；最小 packet 覆盖 26 candidates | [post-annotation record](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_post_annotation.md)、PODR-068、OR-030、REL-2026-0034、Git-external evidence index `11/11` | `WAIT_FOR_OWNER_ADJUDICATION`；Ground Truth not generated；Dataset/Detector/Training/5090/Formal Experiment not started |
| 2026-08-31 | PILOT2 owner-adjudication closure validation | 第 2、4、12、14、15、20 节 | 完成版 workbook hash binding；84/84 issue 与 26/26 candidate completion pass；发现 4 candidates 的非法枚举/同字段冲突；生成最小 reconfirmation table | [closure attempt](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_adjudication_closure.md)、PODR-069、OR-031、REL-2026-0035、Git-external index `5/5` | `OWNER_ADJUDICATION_CONSISTENCY_BLOCKER`；Ground Truth not generated；Pilot2 not closed；Pilot3 not started |
| 2026-08-31 | PILOT2 closure and PILOT3 signal feasibility | 第 2、4、12、14、15、20 节 | 独立绑定四候选五字段 owner correction；残余冲突/PENDING 为 0；生成 36 条 Pilot-only Ground Truth；完成质量审计、Pilot2 feasibility closure 与本机 180-record 五视角 smoke | [closure and Pilot3 record](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md)、PODR-070、OR-032、REL-2026-0036、Git-external closure/Pilot3 indexes | `PILOT2 CLOSED FOR FEASIBILITY / PILOT3 PILOT_DIAGNOSTIC_ONLY`；signals weak；no Dataset freeze/240-group/formal Detector/Training/5090/Formal Experiment/Paper Result |
| 2026-09-01 | PILOT4 balanced preannotation and signal repair | 第 2、4、12、14、15、20 节 | 冻结 canonical lessons；实现 field-schema/G1-G14/near-duplicate/structured signal contracts；构造 24 triplets、72 candidates、48 queries；四轮 QA 与 12-row Owner sample | [future dataset rules](../research/stage6_1_hidden_knowledge_poisoning/human/annotation_lessons_learned_and_future_dataset_rules.md)、PODR-071、OR-033、REL-2026-0037、Git-external manifest 22/22 | `READY_FOR_OWNER_PREFLIGHT / PREANNOTATION_ONLY / NO_HUMAN_DISTRIBUTION`；no Ground Truth/Dataset freeze/Detector/5090/Formal Experiment |
| 2026-09-01 | PILOT4 targeted repair and second Owner preflight | 第 2、4、12、14、15、20 节 | 保留 a843697 首轮失败历史；按 mutation semantics/evidence path 重建候选；分离 Phase1/Phase2/owner；独立重载重算 G1--G14 与 Round D；生成新 12-row workbook | [future dataset rules](../research/stage6_1_hidden_knowledge_poisoning/human/annotation_lessons_learned_and_future_dataset_rules.md)、PODR-072、OR-034、REL-2026-0038、Git-external repair manifest | `READY_FOR_SECOND_OWNER_PREFLIGHT / PREANNOTATION_ONLY / NO_HUMAN_DISTRIBUTION`；not accepted；no A/B/Ground Truth/freeze/training/5090/formal experiment |
| 2026-09-01 | Paper 1 human documentation integration | 第 2、4、12、14、15、20 节 | 建立 0–19 人类总规划/总账、Research Authority 与 Agent ledger 同步、README 第一屏路由、文档清单和人机证据分层；Owner 确认未来正式五领域与 `5×4×3×4=240` scale structure | [human ledger](../research/stage6_1_hidden_knowledge_poisoning/human/experiment_ledger_tingfeng.md)、PODR-073、OR-035、REL-2026-0039 | `DOCUMENTATION_STRUCTURE_AND_CONTEXT_INTEGRATION` only；Pilot4 experiment status unchanged；240 groups/约720 records not executed/generated/frozen |
| 2026-09-01 | PILOT4 final preannotation repair | 第 2、4、12、14、15、20 节 | 保留前两轮 Owner preflight；重构八个 genuine-S3；删除 S1 明示捷径；按最终文本执行长度门；去模板 padding；修复 HN 与来源/非目标 parity；重建 final 72 与 16-row Owner workbook | [future dataset rules](../research/stage6_1_hidden_knowledge_poisoning/human/annotation_lessons_learned_and_future_dataset_rules.md)、PODR-074、OR-036、REL-2026-0040、Git-external manifest `22/22` | `PILOT4_FINAL_PREANNOTATION_READY_FOR_OWNER_REVIEW / NO_HUMAN_DISTRIBUTION`；not accepted；no A/B/GT/freeze/training/5090/formal experiment |
| 2026-09-01 | PILOT4 data/protocol quality convergence | 第 2、4、12、14、15、20 节 | 清除 Phase1 target hint；以实际 HTTP/PDF 内容核验 64 source units 和 24 HN；全量审计 72；冻结 28-field Schema V3 candidate、53-row truth table、ambiguity gate 与 3 个 dry-run XLSX | [future dataset rules](../research/stage6_1_hidden_knowledge_poisoning/human/annotation_lessons_learned_and_future_dataset_rules.md)、PODR-075、OR-037、REL-2026-0041、Git-external quality-convergence manifest | `PILOT4_QUALITY_CONVERGED / READY_FOR_OWNER_ACCEPTANCE_REVIEW / NO_HUMAN_DISTRIBUTION`；not accepted；no A/B/GT/freeze/training/5090/formal experiment |
| 2026-09-01 | PILOT4 Evidence Pool / Schema V3.1 repair | 第 2、4、12、14、15、20 节 | 55/72 duplicate visible slots 经 23 个 verified companion source 修复为 0/72；冻结 distinct-unit counting、A/B independent order、final version/authority semantics 与 English-first UI | [future dataset rules](../research/stage6_1_hidden_knowledge_poisoning/human/annotation_lessons_learned_and_future_dataset_rules.md)、REL-2026-0042、Git-external evidence-pool-repair namespace | `PILOT4_ANNOTATION_PROTOCOL_READY_FOR_OWNER_ACCEPTANCE / NO_HUMAN_DISTRIBUTION`；not accepted；no A/B/GT/freeze/training/5090/formal experiment |
| 2026-09-02 | PILOT4 external blind Owner review packet | 第 2、4、12、14、15、20 节 | 将 c1b Full72 重分类为 sample-ID label lookup contaminated history；生成 72 个不透明身份、隔离 mapping、144/144 真实标题来源、66 个独立案例和四文件外部包；机器不填答案、不比较 expected contract | [future dataset rules](../research/stage6_1_hidden_knowledge_poisoning/human/annotation_lessons_learned_and_future_dataset_rules.md)、PODR-077、OR-039、REL-2026-0044、Git-external external-blind namespace | `PILOT4_EXTERNAL_BLIND_REVIEW_PACKET_READY / WAITING_FOR_EXTERNAL_OWNER_REVIEW / NO_HUMAN_DISTRIBUTION`；no acceptance/A-B/GT/freeze/training/5090/formal experiment |
