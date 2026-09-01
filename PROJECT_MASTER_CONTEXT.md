# LLMGuard 项目总控文档

## PILOT4 Data and Annotation Protocol Quality Convergence（2026-09-01）

本机执行 `S6.1-P1-PILOT4-PREANNOTATION-QUALITY-CONVERGENCE-01`，将 Repair-02 作为不可变输入历史并在新的 additive
namespace 中完成数据与标注协议质量收敛。Phase1 只保留盲法可判断字段；`target_field`、攻击类型、证据答案、隐蔽意图
和 Owner-only 信息均不得进入可见界面。`assigned_stealth_level` 不再人工猜测，而是在 A/B 各自完成 Phase1 与 Phase2 后，
由 `overall_fact_status + local_internal_anomaly + minimum_evidence_scope` 独立推导。

全 72 条候选通过 primary subject、自然关系、长度、模板/近重复、Phase visibility 与语义审计；S1/S2/S3 各 `8/8`，
24 Hard Negative 逐条绑定实际抓取的官方材料。64 个唯一证据单元具有实际响应字节 SHA256、支持摘录 SHA256、锚点和
检索身份。Schema V3 candidate 包含 28 个字段、53 行 exhaustive dependency truth table 与所有人工字段的 13 类歧义
对抗案例。Phase1、Phase2 和 Field Guide 三个工作簿仅为 `ANNOTATOR_DRY_RUN_ONLY`，未发 A/B。

当前状态为 `PILOT4_QUALITY_CONVERGED / READY_FOR_OWNER_ACCEPTANCE_REVIEW / NO_HUMAN_DISTRIBUTION`。Owner 的唯一下一
动作是审查完整 72-row artifact、Schema V3 candidate 和 dry-run 界面，并明确接受或指出新的 blocker。不得自动进入
agreement、adjudication、Ground Truth、240-group、Dataset freeze、Detector、Training、5090、Formal Experiment 或
Paper Result。

## Paper 1 Human Documentation Integration（2026-09-01）

项目需求提出人通过 `PODR-073 / OR-035` 将
`human/experiment_ledger_tingfeng.md` 冻结为 `PAPER1_PRIMARY_HUMAN_ENTRY`，并确认 Human、Research/Protocol Authority、
Agent/Audit/Evidence 三层文档分工。README 只做路由；raw JSON/JSONL/log/XLSX/hash/manifest 不作为人类第一入口。

正式 Paper 1 未来领域集合确认为 Enterprise HR、Finance、Information Security、Procurement and R&D、Education and
Research。Scale Pilot 结构规划为 `5×4×3×4=240` independent groups，约 720 条 derived candidate records；均为
`NOT EXECUTED / NOT GENERATED / DATASET NOT FROZEN`。Pilot4 的四领域覆盖仍是不可改写的历史事实。

文档整合不改变实验状态。当前仍为 `PILOT4_BALANCED_SET_REPAIRED / READY_FOR_SECOND_OWNER_PREFLIGHT /
PREANNOTATION_ONLY / NO_HUMAN_DISTRIBUTION`；唯一下一人工动作是 Owner 审查 repaired 12-row second preflight。

## PILOT4 Targeted Repair 与第二次 Owner Preflight（2026-09-01）

第一次 Owner preflight 被 `PODR-072 / OR-034` 退回后，`a843697` 与原外部 package 保持历史不可变。本机完成 mutation
semantic alignment、stealth evidence path、naturalness/evidence echo、visibility separation、claim-derived applicability、
serialized-artifact G1–G14 和 independent Round D 修复；实现身份为
`cad3b2b2c19dcef6c118e4163f705b3ec05713e1`。

当前 repaired set 仍为 24 matched triplets / 72 preannotation candidates / class intent 24/24/24，并生成新的 12-row
second Owner preflight。它不是 Ground Truth、Formal Benchmark 或 frozen Dataset；没有 A/B 分发、agreement、
adjudication、240-group、Formal Detector、5090 或 Formal Experiment。

## Historical Snapshot — PILOT4 首版平衡预标注集与 Owner Preflight（2026-09-01，已被 targeted repair supersede）

项目需求提出人通过 `PODR-071 / OR-033` 批准在 240-group 之前执行最后一个专门小规模数据/标注校准阶段。本机已将
Pilot1–3 的类别失衡、字段适用性、主体缺失、Hard Negative 误报和弱信号经验冻结为唯一 canonical future-dataset
规则，并实现 field-schema gate、G1–G14 candidate gate、结构化 Temporal-Version/Provenance 与语义近重复扫描。

Pilot4 当前有 24 个独立公开中文主体、24 个 matched triplets、72 条 `PREANNOTATION_CANDIDATE` 和 48 条 query；类别
`24/24/24`，HKP×intended-S 12 个单元各 2，4 个领域与 8/8/8 长度覆盖成立。四轮机器 QA 全部通过，Git-external
Owner preflight 只抽样 12 条。当前状态为 `BALANCED_DIAGNOSTIC_SET_READY_FOR_OWNER_PREFLIGHT / PREANNOTATION_ONLY /
NO_HUMAN_DISTRIBUTION`。这些候选不是 Ground Truth、Formal Benchmark 或 frozen Dataset；A/B、240-group、正式 Detector/
Training、5090、Formal Experiment 与 Paper Result 均未启动。

## PILOT2 Owner Adjudication 一致性阻塞（2026-08-31）

项目需求提出人批准 `S6.1-P1-PILOT2-ADJUDICATION-CLOSURE-AND-PILOT3-ENTRY`，但 Ground Truth 与 Pilot3 只能在 owner
packet 完整且逻辑可执行后推进。完成版 owner workbook SHA256 为
`cf47a6c3ffada717a2a0dee2b67d6b92ebfb6236d599fb8a4daf2957e292dcb1`；84/84 issue 与 26/26 candidate 均已填写，
无 PENDING。

只读验证发现 4 个候选仍有非法枚举或同字段冲突，故当前为
`OWNER_ADJUDICATION_CONSISTENCY_BLOCKER / HUMAN_DECISION_REQUIRED / AUTO_CONTINUE_NO`。最小确认表位于
`LLMGuard-Handoff/paper1_pilot2_closure_20260831`，index `5/5`。Ground Truth candidate 未生成，Pilot2 未关闭，
Pilot3 未进入；Dataset、Detector、Training、5090 与 Formal Experiment 均未推进。

## PILOT2 Post-Annotation 一致性与仲裁门（2026-08-31）

项目需求提出人通过 `PODR-068 / OR-030` 批准读取四份完成版 targeted return，按 A/B V2 current value 执行 return
validation、formal agreement 与 disagreement classification。A/B Phase1 原声明中的 `sample_id_changed=YES` 均由 owner
更正为有效过程值 `NO`；原 XLSX 不回写。

四份 return SHA256 已锁定；验证结论为 `PASS_FOR_AGREEMENT_WITH_NON_SEMANTIC_DEFECTS`。正式 V2 agreement 发现 47 条
A/B 分歧和 37 条 schema-logic 冲突，最小 owner packet 只覆盖 26 个候选、84 个问题行。故当前
`OWNER_ADJUDICATION = REQUIRED / NOT_EXECUTED`，`GROUND_TRUTH_CANDIDATE = NOT_GENERATED`。Git-external 证据根为
`LLMGuard-Handoff/paper1_pilot2_post_annotation_20260831`，workbook SHA256 为
`67081c0e3f7c32d42041ccc736316ed2f42fa979d417a76f577b4e90418d363a`，index `11/11`。Dataset、Detector、Training、
5090 与 Formal Experiment 均未启动；Auto Continue = `NO`。

## 后续新候选最低自包含性门（2026-08-28，只向前生效）

项目需求提出人通过 `PODR-067 / OR-029` 将 candidate minimum self-containment 设为后续新文本数据标注的最高优先级门之一。法律、政策、制度、标准等事实主体必须可从候选文本本身唯一识别；“条例”、“规定”、“修订文本”、“2017年版”等依赖隐含上下文的裸指代不能用于正式 Benchmark。

无法唯一恢复主体的新候选必须 fail closed 为 `BROKEN_CANDIDATE / MISSING_CONTEXT`，并在补全主体后作为新候选重新审核，或剔除。该门先于事实/隐蔽性标注、agreement、adjudication 和 Dataset freeze。既有 Pilot1/Pilot2 候选、raw returns 与当前定向复核结果全部保留，不回写、不推翻、不重新解释。

## PILOT2 最终三表更正包（2026-08-28）

项目需求提出人报告 A Phase1 targeted workbook 已完成；本机将其以 SHA256
`100cffe2b81a23f3a65ade5ba712cd7aeefcfc56c600dae68f2b0241af36737f` 保留，未重新生成或放入更正包。它仍待 return validation/hash lock。

B Phase1 的所有 `[V1_ABSENT]` 来自生成器未识别带中文后缀的历史列名，不是 B 标注缺失。B Phase2 的
`version_relation_correct` 与 `authority_matches` 也受同类问题影响；A Phase2 映射经检查正常。修复后 B Phase1
的旧值 `108/108` 恢复，A/B Phase2 只在三个真正新增的 `*_present` 字段使用 `[V1_ABSENT]`。生成器现在对任何其他缺失 fail closed，并冻结 owner 的 S1/S2/S3 决策顺序。

新的 Git-external 交付键为 `LLMGuard-Handoff/paper1_pilot2_targeted_rereview_correction01_20260828`，只含待完成的
A Phase2、B Phase1、B Phase2 三份表格。它们是最终定向人工轮的高优先级/高权重有效性证据候选，但必须先通过 return validation、owner 批准的 agreement、仅必要仲裁和 Ground Truth candidate 验收。Dataset、Detector、Training、5090 和 Formal Experiment 未启动；Auto Continue = `NO`。

## PILOT2 标注人友好版定向复核包（2026-08-27）

项目需求提出人通过 `PODR-065 / OR-027` 决定不发放全量 V2 重做所有字段，而采用
`ONLY_REVIEW_FIELDS_WITH_ACTUAL_PROBLEMS`。本机已完成字段审计：Phase1 仅复核 `locally_detectable`、
`cross_document_evidence_needed`、`assigned_stealth_level`；Phase2 复核 version/history/authority 的三组
present/correctness 与 `overall_fact_status`。`claim_matches_source`、`fact_changed`、自然度、主题相关度和 confidence
保持本人 V1 只读，不因低 agreement 机械重做。

A 有 10 个实质字段、360 个样本×字段任务；B 同为 360 个实质任务，再加 21 个缺失
`professional_lookup_used` 和 1 个 Google Search 来源类型修正，共 382 个任务。与全量 V2 的 576 个实质任务相比，
每名标注人减少 216 个实质任务（37.5%）。B Phase1 历史 `time_seconds` 不补造，只记录新复核时间；每人每 Phase
只填一次 retrospective declaration。

Git-external 交付键为 `LLMGuard-Handoff/paper1_pilot2_targeted_rereview_20260827`；17 个文件从 staging 到 E 盘逐 SHA
一致。四个 XLSX 均含《先看这里》《需要你复核》《原结果只读》《回溯声明》，完成 16-sheet render/inspect、下拉、
只读输入拦截、dependency 提示、UTF-8 BOM、A/B 隔离与 intent-leakage 验证。当前状态仅为
`TARGETED_REREVIEW_KIT = READY_FOR_HUMAN_EXECUTION`；agreement、adjudication、Dataset、Detector、Training、Formal
Experiment 均未开始。

## PILOT2 Annotation Schema V2 与 A/B 独立复核包（2026-08-27）

项目需求提出人通过 `PODR-063 / OR-025` 确认 Annotator A 的实际执行顺序为：Phase 1 完成提交、coordinator 回收并
锁定、之后才发放 Phase 2；A 在 Phase 1 期间未看到 Phase 2。此前依据错误登记时间形成的 blind-contamination inference
作为历史保留，但由 owner-confirmed actual distribution order supersede。原登记表、原错误时间、原推断、原 preflight
workbook 和四份 raw returns 均不得覆盖或修改。

前置 owner correction 继续保持：`PILOT2-RETURN-PROTOCOL-BLOCKER-01 = PROTOCOL_AND_ANNOTATION_SCHEMA_BLOCKER`；
`BLINDNESS_SUBISSUE = RESOLVED_BY_OWNER_CONFIRMED_ACTUAL_DISTRIBUTION_ORDER`；
`REGISTRATION_METADATA_ERROR = DOCUMENTED`，原错误 metadata 与原推断已由独立 manifest 绑定；
`ANNOTATION_SCHEMA_SUBISSUE = REMEDIATION_IN_PROGRESS`。Round 1 可继续作为正式 agreement 候选，但
`FORMAL_AGREEMENT = PENDING_SCHEMA_V2_REREVIEW_AND_RETURN_VALIDATION`，尚未生成 disagreement 或执行 adjudication。

项目需求提出人通过 `PODR-064 / OR-026` 已批准并完成 Schema V2 工具和四个独立复核包准备：四值语义、三组
present/correctness 适用性、authority 命题边界、overall fact 决策树、Phase1 定义、lookup source 枚举、逐字段
`KEEP/REVISE`、retrospective declaration 和 UTF-8 BOM 合同均已冻结。A 只接收 A 本人的 V1 只读参考与 V2 表，B 同理；
原始 return 不覆盖，agreement 不执行。

Git-external 交付键为 `LLMGuard-Handoff/paper1_pilot2_round1_rereview_v2_20260827`；四包 SHA256 为
`0a896226...08a0`、`e3f7127b...f46e`、`3391ffc7...ddf5`、`74390b5c...f626`。当前
`ANNOTATION_SCHEMA_V2 = IMPLEMENTED`、`A_B_REREVIEW = READY_FOR_HUMAN_EXECUTION`、Auto Continue = `NO`；下一门是
A/B 独立完成人工复核并锁定四份 return 后，由 owner 单独批准 return validation/agreement。Dataset、Detector、Training、
Formal Experiment 和 Paper Result 均未推进。

## S6.1-P1-R1 Option B 范围冻结与协议强化候选（2026-08-02）

项目需求提出人已明确确认 `TITLE_INTENT = CONFIRMED`、`DETOXIFICATION_OPTION = OPTION_B` 和
`DETOXIFICATION_TECHNICAL_SCOPE = OPTION_B_CONFIRMED`；完整技术表达为
`OPTION_B_DETECTION_AND_LIGHTWEIGHT_RETRIEVAL_INTERVENTION`。P1_R1 基础提交为
`aabe504d55626fb31008822b7bbabd3b32e2afd4`。

Paper 1 当前范围包括中文版本感知隐蔽知识污染 Benchmark、五视角 Detection、Risk Score、Signals、Explanation，
以及基于校准风险的 hard filtering 或 soft downweighting。安全结果与检索效用分别作为共同主结果，不使用掩盖权衡的
单一综合分数。trusted context package、完整上下文构造、多证据可信上下文生成、复杂端到端 Agent 防御、生产级 RAG
平台和完整可信检索链明确排除，保留给 Paper 2 或后续研究。

[P1-R1 审批级协议强化候选](docs/research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_r1_protocol_review_candidate.md)
覆盖 RQ1--RQ6、Benchmark/schema/group-aware split/label isolation、HKP/S/hard negatives、外部基线公平性、五视角接口、
Option B 干预公式、安全—效用指标、统计/Pilot/资源/evidence/license 及 20 项进入条件。它只在候选层替代
[旧 P1 候选](docs/research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_protocol_candidate.md)，不删除历史，也不是 canonical
stage process。

本段是 2026-08-02 创建 P1-R1 来源候选时的历史快照：当时 P1-R1 为 `REVIEW_CANDIDATE / NOT APPROVED / NOT STARTED`。
该审批状态已由后续 Owner 决定 supersede；当前为 `HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK`，但数值参数、Formal Dataset、
Formal Detector、Retrieval Intervention effectiveness、Training 和 Formal Experiment 仍未冻结/未开始。

## S6.1-R0-FU1-W2 工程可行性最终验收与 P1 候选门（2026-08-02）

项目需求提出人以提交 `b19fc59cc5ba771fd547430f6096403720ef1a7d` 为验收基础，将父 W2 登记为
`HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED`，并将 FU1 登记为 `HUMAN_ACCEPTED / CLOSED`。H1 为
`OFFLINE_MODEL_ARTIFACTS_VERIFIED_ON_5090 / COMPLETED`；H2 为
`ENGINEERING_SMOKE_COMPLETED / CONTROL_PLANE_REVIEW_PASS / HUMAN_ACCEPTED_AS_W2_EVIDENCE`。

验收依据仍是不可变的 H2 resume_02 evidence：archive SHA256
`58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563`、index `25/25 PASS`、H2-A `18/18 PASS`、
唯一 H2-B `call_count=1`。固定样本中 benign retained、poisoned filtered；**这是单次冻结样本的工程观察，不是检测性能结论。**
resume_01 的 `VALID_BLOCKED_EVIDENCE / OFFLINE_BUNDLE_SHA_BLOCKER / H2-B NOT EXECUTED / call_count=0` 及 Attempt 1 历史
保持不变。

冻结结论为 `W2_ENGINEERING_OBJECTIVE = SATISFIED`、`W2_RUNTIME_GATE = CLOSED`、
`BLK-S6.1-FU1-W2-001 = RESOLVED_BY_H2_RESUME02_AND_OWNER_ACCEPTANCE` 和
`W2_ACCEPTANCE_SCOPE = FROZEN_SINGLE_SAMPLE_DETECTION_CORE_ENGINEERING_FEASIBILITY_ONLY`。这不建立 GMTP reproduction、
detection effectiveness、strict baseline comparison 或 formal paper result。

该时点下一阶段只有 [S6.1-P1 协议候选](docs/research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_protocol_candidate.md)，状态为
`CONTRACT_CANDIDATE / NOT APPROVED / NOT STARTED`，且 Option A/B/C 尚待选择。该历史候选门已由上方 PODR-062 的
Option B 范围决定与 P1-R1 新候选在候选层替代；P1 本身仍未获批准或启动。

## H2 resume_02 工程 smoke 证据已通过本机复核（2026-08-01）

LOCAL 已对返回的 `s6_1_r0_fu1_w2_resume02_evidence_20260801.tar.gz` 执行独立只读复核。Archive 为 `15625`
bytes，sidecar、实际 SHA256 与 Worker 报告均为
`58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563`；唯一顶层目录为 `resume_02`，27 个 regular
files 与 1 个 directory 均为安全成员，内部 evidence index 独立复算 `25/25 PASS`。Resume_01 的 directory aggregate
与 4570-byte archive SHA 保持不变。

H2-A `18/18 PASS`；冻结 bundle/model/source/input/environment/offline 身份全部匹配。RTX5090 本地模型加载通过，无 CPU
fallback；H2-B 只执行一次，`call_count=1`，benign retained、poisoned filtered，全部数值 finite，环境 pre/post SHA
一致，资源门全部通过。因此 resume_02 状态为
`CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED`，父 runtime blocker
`BLK-S6.1-FU1-W2-001` 仅在冻结的最小 detector-core feasibility 范围内关闭。

在该 `2026-08-01` 复核时点，本轮仍不是 baseline reproduction、有效性评估、论文结果或正式实验。本机没有加载模型或执行 GMTP。父 W2 当时保持
`APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`，等待项目负责人明确决定；P1、Dataset、Detector、Training、Our
Method Result 与 Formal Experiment 均未推进。该历史等待状态已由后续 PODR-061 验收关闭；没有证据缺口需要向 5090 发送 corrective prompt。

## H2 resume_01 受阻证据已复核，resume_02 命名空间已批准（2026-08-01）

5090 的 H2 `resume_01` 因 bundle/sidecar 当时缺失而在 H2-A gate 1--4 fail closed；gate 5--18 未执行，H2-B 未执行，
`call_count=0`。Returned evidence archive 大小 `4570` bytes、SHA256
`941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d`。本机流式复核确认 archive 只有 resume_01、20 个
regular files、1 个 directory、无危险成员，内部 evidence index `19/19 PASS`；环境 explicit-spec pre/post SHA 一致。

项目需求提出人随后确认冻结 bundle 与 sidecar 已同步到 5090，archive size `1222137698` 与 SHA256
`aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45` 匹配。但原合同禁止覆盖或删除非空 resume_01，
因此重用该路径会触发 `EVIDENCE_CAPTURE_BLOCKER`。项目需求提出人通过 `PODR-060` 批准只把证据命名空间滚动到
`~/experiments/s6_1_r0_fu1/w2/resume_02`，并冻结新 archive
`s6_1_r0_fu1_w2_resume02_evidence_20260801.tar.gz` 及 sidecar。

Resume_01 永久保留；resume_02 必须不存在或为空，否则停止且不得自动创建 resume_03。5090 必须从完整 H2-A 开始，
bundle/model/source/input/environment/parameters/resources/offline/claims 合同全部不变。H2-B 的唯一一次调用授权尚未使用；
只有 resume_02 H2-A 全部通过才可调用。父 W2、P1、Dataset、Detector、Training、Our Method Result 与 Formal Experiment
状态不变。

## H2 离线模型包验证与条件式 detection-core 恢复已批准（2026-08-01）

项目需求提出人已批准 `S6.1-R0-FU1-W2-H2 / Offline Model Bundle Verification and Conditional GMTP Detection-Core
Resume`，执行机器为 5090，状态为 `APPROVED_TO_START / NOT SENT / NOT EXECUTED`，审批基础提交为
`212911a21dc35bef05b15fb840542403c415dd13`。批准前 `H2 = PROPOSED / NOT CANONICAL / NOT APPROVED` 作为历史快照保留，
由 `PODR-059` supersede。`Auto Continue = CONDITIONAL_WITHIN_H2_ONLY`。

5090 必须先完成 H2-A：对 Git-external bundle
`s6_1_r0_fu1_w2_models_20260801.tar.gz`（size `1222137698`，SHA256
`aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`，bundle source bytes `1320359518`，index
`19/19`）执行完整 SHA、安全、manifest、模型 revision/files/bytes、credential/cache 排除与解压后复算。任一实质不一致
立即停止，不得进入 H2-B。

只有 H2-A 全部通过，才允许在冻结的 `gmtp-compat`、强制离线模式下，从未修改 GMTP commit
`15b48d150f93711371eb8da22c211cd84a0cf4df` 的 `method.py`，使用固定 input index 0 / `test0`、固定
Contriever/BERT revision 和参数，执行一次 `[benign, poisoned]` 的 `filter_documents` 调用。禁止网络回退、环境或源码/
输入/模型/参数修改、CPU fallback、重试和批量扩展。完成或任一 blocker 后停止，将 redacted indexed evidence 返回本机。

本轮本机只执行审批登记、合同冻结、文档同步、测试和 Git；没有解压/加载模型、运行 GMTP/harness、使用 GPU 或联系
5090。H1 仍为 `OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION`；父 W2 仍未完成/未验收；S6.1-P1、Dataset、
Detector、Training、Our Method Result 与 Formal Experiment 均未改变。H2 最多产生工程 smoke 待复核状态，不支持指标、
有效性、复现、安全性、SOTA 或正式论文结论。

## Correction 02 最终关闭与 H1 离线模型工件已准备（2026-08-01）

LOCAL 已对 RTX5090 返回的 Correction 02 原始证据执行独立复核：4367-byte archive 的 sidecar、实际 SHA-256 与
Worker 报告均为 `fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622`；archive safety 与排序 index
`17/17` 通过。GNU coreutils `du 9.4` 的准确命令、raw streams 与零退出码支持 apparent `5399301224` 和 allocated
`5492817920`，两者均低于 `6442450944`；文件 `33556`、目录 `3194`、Correction 01 delta 为零、pre/post spec SHA
一致，且没有环境/repository/model/smoke/GPU mutation。

因此 `MATERIALITY_AND_FINAL_CLOSURE_RULE = PASS (11/11)`；`W2_ATTEMPT1_EVIDENCE_BLOCKER` 已按冻结规则关闭，Attempt 1
重分类为 `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER`，并登记 `smoke_executed=false`、
`algorithm_failure=false`、`GMTP_incompatibility=not established`。可复用证据仅限 main/GMTP/input/environment/CUDA/disk
身份、encoder 下载 blocker 与 smoke 未执行；模型加载、detector 分数、runtime/RSS/VRAM、兼容性和安全有效性均未建立。

随后 LOCAL 在隔离 `w2-h1-download` 环境中匿名下载并校验两项固定 revision：Contriever 8 文件 / 438708922 bytes，
BERT MLM 9 文件 / 881643453 bytes；总模型字节 `1320352375`，低于 2 GiB。最终 Git-external bundle 为
`s6_1_r0_fu1_w2_models_20260801.tar.gz`，大小 `1222137698`，SHA-256
`aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`；排序 index `19/19`、archive safety、包内
逐文件复算和 sidecar 均通过。H1 状态为 `OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION`。

这些事实由 `PODR-058` 与 `REL-2026-0019` 持久化。本机没有加载模型、运行 GMTP/harness、使用 GPU 或联系 RTX5090。
W2 仍未完成/未验收；S6.1-P1 与 Formal Experiment 仍未开始。下方关于 blocker open、H1 blocked/not started 或
Correction 02 未执行的段落均是其标题日期下的历史快照，由本节 supersede，不得删除或改写为当时已完成。

## Correction 02 GNU du 来源链最终证据修正已批准（2026-08-01）

项目负责人通过 `PODR-057` 将 `S6.1-R0-FU1-W2-ATTEMPT1-CORRECTION-02` 正式批准为
`APPROVED_TO_START / NOT EXECUTED`，任务类型仅为 `EVIDENCE_PACKAGING_CORRECTION_ONLY`，执行机器仅为
`RTX5090 / COMPUTE_WORKER`。本轮 LOCAL 只登记批准、冻结验收标准和创建治理提交；没有联系或代替 Worker，也没有
执行 Correction 02、模型下载/加载、GMTP、harness、CUDA、环境修改、H1、P1 或 Formal Experiment。

正式合同冻结 GNU apparent-size `du -sb -- <gmtp-compat-path>` 与 allocated-size
`du -sB1 -- <gmtp-compat-path>` 的不同语义，并要求原样保存命令/参数、raw stdout/stderr、exit code、UTC 时间、
`command -V du`、`type -a du`、`du --version`、`uname -a`、Conda 注册身份、环境 basename、文件/目录计数、manifest、
完整 index 与 archive SHA-256。Correction 01 的历史数值只用于对照，不得为了匹配而修改新输出；明显差异返回
`DISK_MEASUREMENT_MATERIAL_MISMATCH`。

`MATERIALITY_AND_FINAL_CLOSURE_RULE` 只适用于本次 Correction 02。只有 LOCAL 后续验证 archive/sidecar/SHA、archive
安全、完整 index、既有 `gmtp-compat` 身份、两条准确 GNU 命令与语义、完整 raw streams/exit codes、两个零退出码、
两个值均低于 6 GiB、manifest/raw/summary 一致且无任何 mutation/download/smoke rerun 后，才必须关闭
`W2_ATTEMPT1_EVIDENCE_BLOCKER`，把 Attempt 1 重分类为
`VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER` 并接受 `REUSABLE_W2_PREFLIGHT_EVIDENCE`。非实质格式偏好不得
制造新的包装 blocker；实质真实性、身份、可复现性、安全或资源问题继续 fail closed。

该批准提交时的事实尚未改变：W2 仍 `APPROVED / NOT COMPLETED / NOT ACCEPTED`；Attempt 1 仍 `EVIDENCE_REVIEW_BLOCKED`；blocker
仍 open；H1 仍 approved but blocked/not started；S6.1-P1 与 Formal Experiment 仍 not started。Worker 成功状态只能是
`W2_ATTEMPT1_CORRECTION02_EVIDENCE_READY_FOR_CONTROL_PLANE_REVIEW`，不是 W2/H1/GMTP/Formal acceptance。

## PO-MHEP 最高内部执行治理原则（2026-08-01）

项目负责人正式确立 [PO-MHEP](docs/governance/project_owner_sovereignty_and_mandatory_escalation_principle.md)：
`Project Owner Sovereignty, Mandatory Human Escalation, and Physical Context Preservation Principle`，状态为
`HUMAN_ACCEPTED / HIGHEST_INTERNAL_PROJECT_EXECUTION_AUTHORITY / PERMANENT / NO_AUTO_EXPIRY`，适用于整个 LLMGuard Research
Framework、所有 Stage/分支/LOCAL/RTX5090/Agent/自动化执行者。

L0 动态 Git/raw evidence 仍决定客观事实；L0.5 PO-MHEP 决定发现事实后是否允许继续。accepted boundary、API/凭据、
重大资源或不可逆操作、架构/算法/label leakage、论文创新/公平/统计/许可、证据来源链、context conflict 或重大方案
不确定性均触发 `HUMAN_DECISION_REQUIRED / Auto Continue = NO`。只能继续只读核验、决策风险分析、物理上下文/证据
保全与治理更新；不得默认方案、静默 workaround、Worker 自决或自动进入下一任务。

LOCAL 现在明确承担 `PRIMARY_CONTROL_PLANE / PROJECT_EXECUTION_LEAD / RESEARCH_GOVERNANCE_LEAD /
5090_APPROVAL_AUTHORITY / PAPER_RISK_REVIEWER / CONTEXT_PRESERVATION_OWNER`；RTX5090 永远只是
`COMPUTE_WORKER / NO_SELF_APPROVAL_AUTHORITY`。所有阶段前执行 `FORWARD_RISK_REVIEW`，论文关键节点执行
`PAPER_RISK_REVIEW`，任务结束执行 `CONTEXT_PERSISTENCE_CHECK`。

该治理升级登记当时没有改变 W2 事实：P0/L1 accepted；W2 approved but not completed/accepted；Attempt 1
evidence-blocked；`W2_ATTEMPT1_EVIDENCE_BLOCKER = OPEN`；H1 blocked/not started；P1/Formal Experiment not started。当时
Correction 02 仅为候选；该历史快照现由上方 `PODR-057` 批准记录 supersede，但未发送/未执行事实继续成立。

## S6.1-R0-FU1-W2 Attempt 1 Correction 01 仍未关闭证据门（2026-08-01）

LOCAL 已复核 correction archive SHA-256
`d911063e3a00daba3f8dcfea6f3e6e3b484e79f4f0fe8853a53ff9d8c415279e`：外部 sidecar、实际 archive 和 Worker
报告值一致；安全成员 `6/6`，correction index `4/4`，原 Attempt 1 绑定、主仓库 branch/HEAD/0-0/clean/diff/tag
现场证据均通过。记录的 `gmtp-compat` apparent bytes `5399301224`、allocated bytes `5492817920` 与 manifest 一致，
并均小于 `6442450944`。

但 correction 只记录 `MEASUREMENT_TOOL=du`，没有捕获实际 `du` 命令与区分 apparent/allocated 的参数，不能独立验证
两个计量字段没有混淆。因此 `W2_ATTEMPT1_EVIDENCE_BLOCKER` 继续保持 **OPEN**，Attempt 1 仍不得重分类为
`VALID_BLOCKED_ENGINEERING_RUN` 或 reusable preflight。H1 保持
`APPROVED_TO_PREPARE_OFFLINE_ARTIFACTS / NOT STARTED / BLOCKED_BY_W2_ATTEMPT1_EVIDENCE_BLOCKER`；LOCAL 未下载或加载模型、
未创建 bundle、未运行 GMTP/GPU、未联系 RTX5090。只需补充两条实际 `du` 命令及原始输出，无需重跑 smoke 或重建环境。

## S6.1-R0-FU1-W2 Attempt 1 Evidence Blocker（2026-08-01）

LOCAL 已只读复核 Worker archive：外层 SHA-256
`6acdbb8038e57b1d3e88028350fc08046d73a826ba9dd167452bfc0dd834170f`、安全成员 `18/18`、内部 index `16/16` 与
harness SHA-256 均通过；GMTP/source/input/environment identity、encoder `MODEL_DOWNLOAD_BLOCKER` 和
`smoke_executed=false` 互相一致，未保存完整输入文本。

但 archive 没有主 LLMGuard repository HEAD `457458cbc484c7a187c1b0b812c414280f4b837a` 或 clean status 的捕获结果；
resource file 还明确记录 disk/resource `NOT_EVALUATED`，不能支持约 5.2 GB 环境占用摘要。故 Attempt 1 登记为
`EVIDENCE_REVIEW_BLOCKED / W2_ATTEMPT1_EVIDENCE_BLOCKER`，不得写成 `VALID_BLOCKED_ENGINEERING_RUN`、reusable
preflight、算法失败、GMTP 不兼容、W2 completed 或 accepted。

项目负责人批准的 `W2_TASK_OWNED_DISK_HARD_CEILING = 10 GiB` 修正与
`S6.1-R0-FU1-W2-H1 / Offline Model Artifact Provisioning and W2 Resume` 决策继续保留；但 H1 实际执行为
`NOT STARTED / BLOCKED_BY_W2_ATTEMPT1_EVIDENCE_BLOCKER`。LOCAL 未下载模型、未创建 bundle、未运行 GMTP/GPU、
未联系 RTX5090。下一步只需返回包含主仓库 HEAD/clean 与环境字节计量的 corrected indexed evidence；无需为修正
evidence packaging 重跑 GMTP 或重建环境。`S6.1-P1 = NOT STARTED`，`FORMAL_EXPERIMENT = NOT STARTED`。

## S6.1-R0-FU1-W2 GMTP Detection-Core Smoke 执行批准（2026-08-01）

项目负责人已将 `S6.1-R0-FU1-W2 / GMTP Detection-Only Minimal Smoke` 批准为 `APPROVED_TO_START`，执行机器仅为
`RTX5090 / COMPUTE_WORKER`，任务类型为 `ENGINEERING_VALIDATION / DETECTION_CORE_COMPATIBILITY_SMOKE`。本轮 LOCAL
只登记并推送执行批准，没有联系 Worker、安装环境、下载模型、运行 GMTP/GPU workload 或进入 P1。

Worker 合同继续严格绑定 GMTP commit `15b48d150f93711371eb8da22c211cd84a0cf4df`、detector blob
`84e69b3eadeb8adc0ce521501f8b560d6377b489`、既有固定 sample/hashes、两项固定模型 revision、独立 `gmtp-compat`
环境、已接受参数和资源上限。证据只能写入 `~/experiments/s6_1_r0_fu1/w2/`；LLMGuard 主仓库只读。任何 Java、
Pyserini、FAISS、BEIR 或 Docker 强制依赖、source patch 或资源超限均按冻结 stop code 返回 Control Plane。

W2 仅验证 detection-core 最小可执行性。其 GMTP-packaged HotFlip/Contriever/NQ 输入不是 L1 的 PoisonedRAG
LM-targeted artifact；该批准不等于 W2 已执行、通过或验收，也不建立 GMTP paper reproduction、formal comparison、
指标结果或 security-effectiveness claim。`S6.1-P1 = NOT STARTED`，`FORMAL_EXPERIMENT = NOT STARTED`。Auto Continue = NO。

## S6.1-R0-FU1-P0/L1 验收与 W2 合同冻结（2026-07-31）

项目负责人已将 `S6.1-R0-FU1-P0` 与 LOCAL 子任务 `S6.1-R0-FU1-L1` 登记为 `HUMAN_ACCEPTED`。L1 在内存中
核验官方 GitHub 内容，绑定 PoisonedRAG NQ released artifact、全 100-record schema、官方 LM-targeted
`question + "." + adv_text` 拼装语义和固定样本确定性哈希。Canonical evidence is
[FU1 Targeted Resolution](docs/research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)。本轮未联系
RTX5090，未下载模型或 NQ corpus，未运行模型、retrieval、API、GMTP、SafeRAG 或正式实验。

当前结论是：NQ 为 primary external dataset candidate，HotpotQA 为 fallback；PoisonedRAG official released NQ
attack-text artifact identity 与 deterministic assembly 已验证，可 API-free 复用，但 exact generator/API/paper-run identity
仍仅为 `PARTIAL`；GMTP 的
`beir@f062f0...` 已验证属于 official `beir-cellar/beir`，核心 `GMTP.filter_documents` 可直接消费 question/document，
Java、Pyserini 和 FAISS 仅属 retrieval/indexing path；SafeRAG SN 100/ICC 93 的 benchmark-artifact contract 已冻结，
full pipeline 非 P1 前置 blocker。三者仍均不是 strict-comparison-ready。

原 Worker `FU1-W1` 已被 LOCAL L1 取代，状态为 `SUPERSEDED_BY_LOCAL_L1 / NOT FAILED`。`FU1-W2 GMTP
Detection-Only Minimal Smoke` 的 input/model/parameter/environment/resource contract 已冻结，状态为
`READY_FOR_OWNER_EXECUTION_APPROVAL / NOT_YET_EXECUTED`。项目负责人下一步只决定是否批准 W2；不得自动执行。
S6.1-P1、Dataset freeze、Detector、training、Our Method Result 与 Formal Experiment 均未开始。Auto Continue = NO。

## S6.1-R0 Corrected Evidence 最终验收历史快照（2026-07-31）

LOCAL 已完成 corrected Worker evidence 正式复核：archive SHA-256
`904d79c59e35c6aeb157540049b0f44262b86e5c1c5b3e8d4e96ee2fad3f1c6b` 与 sidecar 一致，安全 archive 共 39
个成员，corrected inner index `12/12` 全部通过，corrected matrix SHA-256 为
`fd7617eca689fa46fc6908f94aa4fa158aaae4d277bb17943bbcc1baf74db9bc`。private archive、外部仓库和完整 Worker
logs 均留在 Git 外。

S6.1-R0 现以原 Task Type `ENGINEERING_VALIDATION / REPRODUCTION_PREFLIGHT` 登记为
`HUMAN_ACCEPTED_WITH_BLOCKERS`。历史 `RETURNED_FOR_WORKER_CORRECTION` 与
`REVIEW_PENDING_CORRECTED_WORKER_EVIDENCE` 快照继续保留，不能解释为当前状态。GMTP 已确认 18 个 200-sample
artifacts、modified BEIR gitlink `f062f038c4bfd19a8ca942a9910b1e0d218759d4`、root `.gitmodules` 缺失和 Docker
非强制；SafeRAG 已绑定 exact executed script，逐条验证 SN 100/100 与 ICC 93/93，但只形成
`ENGINEERING_DATASET_SMOKE_RESULT_ONLY / DATASET_ARTIFACT_ONLY`；PoisonedRAG 可单独选择 NQ、HotpotQA 或
MS MARCO，但 `API_FREE_ATTACK_GENERATION = NOT ESTABLISHED`。

最终 baseline 状态为：PoisonedRAG `ENGINEERING_FEASIBILITY_IDENTIFIED / P1_PROTOCOL_BLOCKED`；GMTP
`ENGINEERING_FEASIBILITY_IDENTIFIED / TARGETED_EXECUTION_BLOCKERS_REMAIN`；SafeRAG
`PARTIAL_REPRODUCTION_READY / DATASET_ARTIFACT_ONLY` 且 SN/ICC `BENCHMARK_ARTIFACT_AVAILABLE`。三者仍均
`NOT_STRICT_COMPARISON_READY`，没有 external baseline reproduction、Paper Result 或 Our Method Result。

剩余问题已从 R0 工程阻断重新分为 P1 protocol、formal-experiment environment、redistribution-only 与 non-blocking
事项。`S6.1-R0-FU1 = APPROVAL_RECOMMENDED / NOT APPROVED`；S6.1-P1、Dataset freeze、Detector、training 和
Formal Experiment 均未开始。下一门仅为项目负责人是否批准窄范围 R0-FU1。Auto Continue = NO。

## S6.1-R0-I 首次证据审查退回与 Token Economy 长期原则历史快照（2026-07-31）

LOCAL 已验证 Worker private archive SHA-256
`0ce85a2bfe24e0456f9d29edc40659786d4273fcfc634df8749aee6d0e3aa9cc`、内部 evidence index `18/18` 和四组
component sidecars。R0-A environment fingerprint 与三个 official commit identity 有证据支持；SafeRAG 只存在
`ENGINEERING_DATASET_SMOKE_RESULT_ONLY / DATASET_ARTIFACT_ONLY` 证据。

R0-I 当前决定是 `RETURNED_FOR_WORKER_CORRECTION`，parent R0 为
`REVIEW_PENDING_CORRECTED_WORKER_EVIDENCE`。原因是 GMTP exact commit 实际包含多组 200-sample artifacts，与 Worker
“advertised samples absent”冲突；Docker 只是 convenience path；SafeRAG executed-script hash 未与运行绑定且只检查每个
task 第一条记录。PoisonedRAG、GMTP、SafeRAG 的角色保持 PRIMARY_ATTACK_BASELINE、PRIMARY_DETECTION_BASELINE、
PRIMARY_BENCHMARK_REFERENCE；三者均 `NOT_STRICT_COMPARISON_READY`。这不是 R0 failed，也不是 R0 accepted。

项目负责人同时接受 `Control-Plane-First Token Economy Principle`，Priority 为
`LONG_TERM_DUAL_MACHINE_EXECUTION_PRINCIPLE`：不依赖 RTX5090 的设计、分析、协议、解释和写作优先 LOCAL；Worker token
优先硬件/外部执行与 raw evidence。该资源原则不得覆盖 safety、ethics、Paper-First、evidence quality、label isolation、
immutable history、approval gates 或 reproducibility。

当前只允许 Worker 返回 [R0-I review](docs/research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_i_control_plane_review.md)
列出的最小 corrected evidence。`R0-FU1 = RECOMMEND / NOT APPROVED`；S6.1-P1、Dataset、Detector、training、Our Method
Result 与 Formal Experiment 均未开始。`FORMAL_EXPERIMENT = NOT STARTED`。

## RTX5090 Bootstrap 验收与 S6.1-R0 执行批准历史快照（2026-07-31）

项目负责人已接受 `S6.1-R0-B0 RTX5090 Compute Worker Bootstrap Validation`，状态为
`HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY`。被接受的 Worker 证据包括 Windows 11 Pro 25H2/WSL2 Ubuntu 24.04、
RTX 5090 31.84 GB、PyTorch 2.13.0+cu130 / CUDA runtime 13.0、Compute Capability `(12, 0)`、`sm_120`、FP16
`RTX5090_GPU_TEST_OK`、BF16 `BF16_TEST_OK`，以及 branch/remote/tag/clean-tree Git collaboration。CUDA UMD
capability 13.3 不代表 standalone CUDA Toolkit 13.3 已安装；缺少 NumPy 是非阻断环境完整性观察。

该时间点 `S6.1-R0` 为 `APPROVED_TO_START`，执行机器严格为 `RTX5090 / COMPUTE_WORKER`。Worker 当时必须在 pull
Control Plane commit 后按 R0-A Environment Fingerprint、PoisonedRAG B/C、GMTP D/E、SafeRAG F/G、R0-H Matrix、
R0-I Control Plane Review 顺序执行。第三方仓库留在 `~/paper1_external/`，各自隔离 compatibility environment；
LOCAL 不执行 external baseline。

该历史批准属于 `ENGINEERING_VALIDATION / REPRODUCTION_PREFLIGHT`，不证明 baseline reproduction、Paper Result、
RTX5090 paper-level performance、dataset、Detector、training、SOTA 或 formal experiment。S6.1-P1 仍为 NOT STARTED，
`FORMAL_EXPERIMENT = NOT STARTED`。

## S6.1-LR1 最终人工验收与 R0 下一门（2026-07-31）

项目负责人已将 `S6.1-LR1`、Git-Native Research Context Recovery Governance 和 Paper-First Comparative
Evidence Principle 登记为 `HUMAN_ACCEPTED`，并将
[Paper 1 canonical route](docs/research/stage6_1_hidden_knowledge_poisoning/paper1_research_route.md) 接受为当前研究路线。
接受提交分别为 `1294632ca0501e7b999a29383780bec49eaa6b04` 与
`85a565535a38196a7d6003e728b5cb6a2b17fa8a`。该接受只覆盖 route、benchmark alignment、governance、context
persistence 与 reproduction planning，不建立 dataset、Detector、training、reproduction result、5090 performance、
Paper Result、SOTA 或 Formal Experiment 证据。

预期 baseline tag 缺失已被分类为 `EXPECTED_BASELINE_TAG_NOT_PUBLISHED`。annotated
`s6-t5-rag-baseline-v1` 已恢复并在本地/远端核验严格 peel 到
`18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`。未来 tag 是否存在、是否推送与实际 target 始终由 Git 动态核验；
禁止 force move 冲突 tag。

外部 artifact 从现在起分别治理 `SOURCE_ACCESS`、`INTERNAL_REPRODUCTION`、
`STRICT_COMPARISON_ELIGIBILITY`、`REDISTRIBUTION_ELIGIBILITY`、`CODE_LICENSE` 与 `DATASET_LICENSE`。
PoisonedRAG code 为 MIT；GMTP/SafeRAG code license 未确认，但这不自动阻断未来获批的内部研究流程，其再分发资格
仍待核验。

当前路线为 `LR1 HUMAN_ACCEPTED -> S6.1-R0 -> S6.1-P1 -> Dataset/Detector/Formal Experiment`。本段的
`DEFINED / NOT STARTED / PENDING OWNER EXECUTION APPROVAL` 是 R0 获批前历史快照；最新状态见本文顶部。

## Git-Native Research Context Recovery 状态附注（2026-07-31）

项目负责人已将 Git-native Research Context Recovery System 作为 S6.1-LR1 的追加治理验收条件。当前 canonical
体系由 `AGENTS.md`、[Context Authority Map](docs/governance/context_authority_map.md)、长期需求、Owner Decision
Register、本 Project Master Context、Current Work State、Experiment Master Record、append-only
[Research Execution Log](docs/governance/research_execution_log.md)、accepted protocols/routes 和
[Stage Learning Guides](docs/learning/README.md) 组成。

L0 Git/raw evidence 决定动态事实；Owner Decision Register 是用户确认决策权威；Current Work State 是唯一动态任务
入口；Experiment Master Record 是唯一实验控制面；Learning Guide 是非权威教学材料。冲突无法解析时登记
`CONTEXT_CONFLICT_BLOCKER` 并停止，不依赖聊天记忆猜测。Paper 1 唯一 canonical route 是
[paper1_research_route.md](docs/research/stage6_1_hidden_knowledge_poisoning/paper1_research_route.md)。

此处是治理候选完成时的历史快照；最新接受状态与 R0 门见本文顶部。该治理扩展不改变 S6-T5 accepted baseline 或
Stage 1–5 immutable assets。

## S6.1-LR1 Research Alignment 状态附注（2026-07-31）

项目负责人已批准 `S6.1-LR1 Paper 1 Literature, Benchmark, Source Code, Hardware and Reproduction Alignment`。
本轮只建立论文优先比较证据原则、Paper 1 三轨路线、PoisonedRAG/GMTP/SafeRAG 一手来源与 commit/license
登记、Benchmark 矩阵、复现协议、RTX 5090 兼容规划和双机政策。当前状态为
`COMPLETED_PENDING_HUMAN_ACCEPTANCE`，正式 RAG 安全实验仍为 `NOT STARTED`。这是验收前历史快照；当前状态由
本文顶部、Owner Decision Register 与 Current Work State 解释。

研究分支 `research/stage6-1-hidden-poisoning` 从 accepted baseline
`18cf2741c8383d35604715af6ebf8cbaa2a3ddf1` 创建。该次 fetch 快照中目标远端分支和预期 tag
`s6-t5-rag-baseline-v1` 均不存在；本轮没有创建、移动或重写 baseline tag。GMTP 与 SafeRAG 官方仓库没有
发现根 LICENSE，因此再分发保持 blocked。所有硬件容量均为 Control Plane 规划估计，待 5090 worker 实测。

权威入口为 [Stage 6.1 研究目录](docs/research/stage6_1_hidden_knowledge_poisoning/README.md) 和
[论文优先比较证据原则](docs/research/paper_comparative_evidence_principle.md)。

## S6-T5 基线最终人工验收状态附注（2026-07-27）

项目负责人已将 `S6-T5.8-H1`、`S6-T5.8` 与 `S6-T5 Controlled Retrieval and Traceable Context Baseline` 分别登记为 `HUMAN_ACCEPTED`、`HUMAN_ACCEPTED` 与 `HUMAN_ACCEPTED BASELINE`。唯一的统一索引是 [S6-T5 基线验收报告](docs/governance/s6_t5_baseline_acceptance_report.md)：它区分 protocol、implementation、hardening、integration evidence 和 governance acceptance 提交，并保留所有结论边界。

`b136ee2` 仍是最后已接受 implementation commit；`b6cedf3` 仍是已接受 integration evidence commit；原始 T5.8 candidate baseline closure commit 为 `37cccdc`；`4ecf73a` 是 accepted baseline content commit。当前治理提交仅为 baseline governance acceptance commit，其 SHA 在提交后按 Git 事实核验，绝不改写为 implementation 或 integration evidence。Stage 6.1 formal research 仍为 `NOT APPROVED`，Formal RAG security experiment 仍为 `NOT STARTED`；本轮未调用任何模型或真实基础设施，未创建 tag 或研究分支。

## S6-T5.7 当前状态附注（2026-07-26）

`S6-T5.7 Controlled Retrieval Context Pipeline Integration and Security Validation` 已通过人工验收，当前为 `HUMAN_ACCEPTED`。新增证据只验证既有受控链路的互操作：静态 Query 投影到 Context Package，以及显式开启的固定 MiniLM 与临时 Chroma close/reopen、受控 synthetic-corpus 解析和稳定身份检查。

最后已接受实现提交仍为 `b136ee2`；已接受的集成证据提交为 `b6cedf3`，它不属于 implementation commit；`S6-T5.8` 及其 H1 均为 `Completed, pending human acceptance`，原始 candidate closure 为 `37cccdc`；Formal RAG security experiment 为 `NOT STARTED`。本轮未调用 Groq 或生成式 LLM，未执行 evaluator、Trust、Citation Accuracy 或正式攻击矩阵。详见 [S6-T5.7 集成记录](docs/governance/s6_t5_7_integration_completion_record.md)。

> 这是项目唯一的总体架构与阶段叙事入口。Owner-confirmed decisions 由项目负责人决策登记册负责；当前任务由
> Current Work State 负责；实验事实由 Experiment Master Record 与原始 evidence 负责。

更新时间：2026-07-26

当前研究分支：`research/stage6-1-hidden-poisoning`

文档状态：A0 架构冻结、A1R 命名/namespace 迁移与 S6-T4 真实集成加固已完成

长期研究需求基线：[docs/governance/long_term_research_requirements.md](docs/governance/long_term_research_requirements.md)。
它固定 RAG 安全为第一优先级，并约束语料域、标签隔离、证据/引用、上下文分级、拒答和 Stage 6.1/6.2/7
路线；任何较早实施草案与其冲突时，以该基线和本文的较新状态为准。

## Repository Context Persistence

根目录 `AGENTS.md` 是 Codex 仓库上下文入口；权威层级以
`docs/governance/context_authority_map.md` 为准；长期目标以
`docs/governance/long_term_research_requirements.md` 为准；项目负责人已确认的解释和决策见
`docs/governance/project_owner_decision_register.md`；本文件负责总体架构、阶段进度和结论边界；
`docs/governance/current_work_state.md` 负责当前任务与审批门。新 Thread、Agent、Workspace 或 Worktree
必须遵守 `docs/governance/context_recovery_protocol.md`。Git 是 branch、HEAD、工作树、commit、tag、文件
存在性和远端同步状态的事实来源。

实验路线、历史运行、指标、证据、失败和交接入口统一见
`docs/governance/experiment_master_record.md`。该总记录只做控制面与索引，不替代本文件的架构叙事、
`current_work_state.md` 的动态审批门或 Stage-specific 原始产物。

职责边界固定为：长期需求记录长期能力要求；项目负责人决策登记册记录明确确认的解释与决策；项目总控
记录架构与阶段叙事；动态状态记录当前任务与审批；实验总账记录实验与证据索引；Research Execution Log
记录 append-only 推进时间线；Git 记录动态工程事实；Learning Guides 只负责非权威教学。

### GOV-ER1：Experiment Master Record（2026-07-20）

已建立唯一的 [Experiment Master Record](docs/governance/experiment_master_record.md)，用于索引 Stage 1–5 的原始运行、指标、证据、失败记录与结论边界，并登记 Stage 6 的工程验证缺口、审批门和交接顺序。它不改写历史工件、不替代动态工作状态，也不授权 S6-T5.3；当前仍需人工审查总记录与 S6-T5.2 验收证据。

**状态更新（2026-07-21）**：项目负责人已将 GOV-ER1、GOV-ER1-H1 与 S6-T5.2 标记为 `HUMAN_ACCEPTED`，并单独批准 `S6-T5.3 DenseRetriever` 启动。该审批仅覆盖离线、Provider-Neutral DenseRetriever 的工程实现与验证；不覆盖 ContentResolver、Context、Trust、LLM/Groq 或正式 RAG 安全实验。

**协议 blocker（2026-07-21）**：启动前核查发现，S6-T4 的 `VectorSearchHit` 及公开 metadata 无法提供 S6-T5.2 canonical `RetrievalEvidence` 强制要求的 `parent_doc_id`。Retriever 又不允许读取语料、伪造父文档身份或修改冻结契约，因此 S6-T5.3 正确暂停，等待人工批准安全的 hit-to-evidence identity contract。

**S6-T5.3-P1 与 DenseRetriever（2026-07-22）**：项目负责人批准后，`parent_doc_id` 被定义为公开、非标签、无正文的 provenance identity。VectorStore schema `1.1` 将它沿 `ChunkRecord -> VectorDocument -> VectorSearchHit -> RetrievalEvidence` 传递，schema `1.0` 保持旧 collection 兼容；collection fingerprint 因 schema 版本而隔离。随后实现 Provider-Neutral DenseRetriever，严格执行 `RetrievalRequest -> EmbeddingProvider -> VectorStore -> VectorSearchHit -> RetrievalEvidence -> RetrievalTrace`，不读取正文、不调用 LLM。该能力已完成离线工程验证，仍等待人工验收，不能宣称检索安全或 RAG 实验结论。

**S6-T5.3-H1 验收加固（2026-07-22）**：人工验收发现后，trace 的 `candidate_count` 已改为本次 query 的原始
hit 数量，而非 collection 总量；store fingerprint、dimension、distance metric、vector schema 与 metadata schema
均逐项 fail closed。Provider/store 的外部错误被映射为稳定、脱敏的 Retrieval 错误。该修复仍只是离线工程
验证，状态为 `Completed, pending human review`；S6-T5.3 仍为 `Completed, pending human acceptance`，不授权
S6-T5.4 或正式 RAG 安全实验。

**S6-T5.3 人工验收（2026-07-25）**：项目负责人已将 `GOV-PODR1`、`S6-T5.3-P1`、`S6-T5.3-H1` 及
`S6-T5.3 Provider-Neutral DenseRetriever` 标记为 `HUMAN_ACCEPTED`，最后接受的实现提交为 `72a2445`。验收仅覆盖
schema `1.0`/`1.1` 隔离、公开 parent identity、Request/Evidence/Trace 链、candidate/returned count 语义、provenance
校验、稳定排序/去重、fail-closed、脱敏审计与当前离线确定性测试。它不证明 Recall/Precision/MRR/NDCG、检索安全、
抗知识污染、可信检索、Citation Accuracy、ContextBuilder、Trust Pipeline、正式 RAG 安全实验或生产可用性。`S6-T5.4`
仍为 `Not approved`，正式 RAG 安全实验仍为 `Not started`。

**S6-T5.4 协议 blocker（2026-07-25）**：项目负责人已单独批准 `Controlled Corpus ContentResolver` 启动。
启动核对确认既有设计已规定 canonical `ContentRef`、hash verification、受控 fixture legacy mapping 的原则和
禁止从 Chroma 读取正文，但没有冻结 Resolver 的返回/正文权限 contract、snapshot 受控读取接口、legacy
`chroma:` 的唯一映射或错误归属。因此 S6-T5.4 被登记为 `APPROVED_TO_START / DESIGN_OR_PROTOCOL_BLOCKER`：
正确行为是暂停，不创建实现、不读取正文、不猜测 fallback，等待项目负责人冻结最小协议。此 blocker 不影响
S6-T5.3 的人工验收，也不批准 S6-T5.5、Context、Citation、Trust 或正式 RAG 安全实验。

## 0.1 A1R：LLMGuard 命名冻结与 Retrieval Domain 落地（2026-07-16）

项目正式名称现为 **LLMGuard Research Framework（简称 LLMGuard）**，中文名称为
**LLMGuard 大模型安全评测与可信检索研究框架**。distribution 固定为
`llmguard-research-framework`，唯一规范 import namespace 为 `llmguard`。

本任务已完成以下边界迁移：

- Stage 6 Task 1–3 的规范实现从 `codeguarder.stage6_rag` 迁至
  `llmguard.domains.retrieval`；
- 旧 `codeguarder.stage6_rag` 改为 re-export facade，兼容测试确认新旧类型与加载器 identity
  相同；
- 阶段导航迁移为 frozen canonical slug；已进入 manifest 的数据与测试路径继续保留旧路径；
- `src/codeguarder/` 中 Stage 5/Stage 5 Paper 为受保护 legacy 例外，不移动、不复制、不新增；
- 本节只记录 A1R 当时的边界；其后的 S6-T4 实现与真实 MiniLM + Chroma 验收见下一节。

命名治理：[project_identity.md](docs/governance/project_identity.md)、
[naming_conventions.md](docs/governance/naming_conventions.md)、
[namespace_migration.md](docs/governance/namespace_migration.md)；架构依据：[ADR 0006](docs/architecture/0006_namespace_migration.md)。

### S6-T4：Embedding Provider 与 Persistent Vector Store（2026-07-16）

S6-T4 已完成并以多个小提交落地：规范代码仅位于
`src/llmguard/domains/retrieval/embedding/` 与 `vectorstore/`。它提供不可变
`EmbeddingModelSpec`、离线确定性 `StaticEmbeddingProvider`、惰性加载的
`SentenceTransformerEmbeddingProvider`、稳定 `VectorStore` 协议、`InMemoryVectorStore`、
持久化 `ChromaVectorStore`、collection fingerprint 与严格公开 metadata 白名单。

实现使用固定 Stage 6 基线模型 ID 和不可变 revision；真实模型集成测试默认 skip，只有显式设置
`LLMGUARD_RUN_REAL_EMBEDDING_TESTS=1` 才允许加载/下载模型。正常快速测试不联网。Chroma
测试只使用临时目录；正式运行时目录固定为 `runtime/stage6_rag_security/chroma/` 并由 Git
忽略。Ground Truth、攻击标签、完整正文和绝对路径不会进入 collection metadata 或 fingerprint。

### S6-T4 Hardening：document 指纹与真实语义验收（2026-07-19）

collection 身份现使用 `document_embedding_spec_hash`，由
`EmbeddingModelSpec.fingerprint(scope="document")` 统一派生，避免人工复制模型 ID、revision、
维度与归一化等片段字段。provider、model ID、revision、维度、归一化、document prefix、输出 dtype
和实现版本任一变化都会改变 collection fingerprint；本机 cache 路径、用户名、创建时间、Ground Truth
和 query prefix 不会进入它。query prefix 会在后续 S6-T5 的 RunManifest 中记录，而不会让未改变的
文档索引被无意义地重建。

已完成一次显式真实验收：固定 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` revision
`16e5344fbfc7dfbbbe0019d30cec21e2940cb4e1` 在 CPU 输出 384 维有限向量；五篇不同主题中文政策文档
写入临时 Persistent ChromaDB、关闭并重开后，中文与英文休假查询 Top-1 都是 `doc-leave`。
metadata 未出现 Ground Truth 或攻击标签；模型缓存和临时 Chroma 均不在 Git。未调用 Groq。

这项验收只证明当前固定模型、固定语料、向量库 adapter 与跨语言术语别名的基础设施行为，不能宣称
Retriever、R1–R6、可信检索策略、RAG 指标或生产安全能力已完成。S6-T5 仍需单独批准。

本任务**没有**实现 Retriever、RetrievalEvidence 编排、ContextBuilder、Trust、LLM、Groq、
RAG Evaluator、T10–T15、实验矩阵或报告；因此没有新的安全指标或真实 RAG 实验结论。下一步
只能在单独批准后进入 S6-T5。

### S6-T5 Design Freeze：受控检索与可追溯上下文（2026-07-19）

已完成唯一 S6-T5 设计规格、八段式 TDD 实施计划和 ADR 0008，冻结以下边界：

- 当前只规划透明 Dense Retrieval，并通过抽象 EmbeddingProvider/VectorStore 复用 S6-T4；
- Retriever 只输出无正文 `RetrievalEvidence` 与 `RetrievalTrace`；
- 正文由 canonical ContentRef 指向受控 corpus snapshot，Resolver 解析后必须核对 content hash；
- Evidence UID 跨运行稳定，Citation ID 只在当前 Context 内有效，由 CitationBinding 建立映射；
- EvidenceEnvelope 只在受控内存持有正文，XML-like escaping 只保护结构边界，不等于语义防注入；
- ContextBuilder 未来输出 `RetrievedContextPackage`，Trust Pipeline 之后才允许产生
  `TrustedContextPackage`；
- Chunking 当前只允许 Identity 基线，复杂 Token/Overlap/Sentence/Semantic 策略只冻结协议；
- S6-T5.1–S6-T5.8 必须逐项人工批准、TDD、独立提交和验收。

该首轮冻结已由后续 `S6-T5 Design Hardening` 审查收紧；当前状态以其“第二次人工审查”门为准。设计文档
完成只能证明契约和实施路径可审查，不能宣称 Retriever、ContextBuilder、Citation Accuracy、Trust 或 RAG
安全实验已经实现。

### S6-T5 Design Hardening：契约与失败边界加固（2026-07-19）

第二次设计审查发现并留痕五类问题：稳定 DTO 可能重复定义、Dataset QueryRecord 可携带评估字段进入
runtime、`corpus:` 与历史 `chroma:` ContentRef 会在 Resolver 前冲突、Envelope/Package 的敏感序列化语义
不够精确，以及完整性异常与结构性 abstention 混淆。

加固后的冻结决定是：稳定 DTO、ContentRef、canonical hash 和安全 audit serialization 只归属
`contracts/`；Dataset QueryRecord 必须经 explicit safe projection 才能成为最小
`RetrieverQueryRecord`；新 producer 只生成 `corpus:`、legacy fixture 继续可读 `chroma:`；
`to_audit_dict()` 才是普通审计接口，`asdict()` 是敏感操作；只有无可用 Context 才返回结构性 abstention，
hash/scheme/fingerprint/metric 等完整性错误必须异常且不得返回 Package。

当前状态为 `Completed, pending second human review`，且 `S6-T5.1 implementation: Not approved`。该加固
仍只证明设计边界已被审查和收紧，不代表任何 S6-T5 Python 能力已实现。

## 0.2 Architecture Task 0：长期架构冻结（2026-07-16，历史架构基线）

本节是本仓库的**权威架构补充**。它优先于本文件中较早的目录草案，以及
`docs/superpowers/` 中仍引用 `stage6_rag` 作为规范实现目录的历史实施计划；这些
历史文本保留以解释演进过程，但不再决定新代码的位置。

### 已核验的事实

- 当前工作分支是 `feature/stage6-rag`；Stage 6 Task 1–3 的早期实现和测试存在，真实
  Embedding、Persistent ChromaDB、检索器、Trust、RAG Evaluator 均尚未实现；
- Stage 1–5 的版本化历史相对本任务起点未发生修改；
- GitHub 的未认证公开 API 返回 404，而本地已认证 Git 远端可访问，因此仓库当前确认是
  **Private**，而不是“尚未确认的待公开仓库”；
- 本轮只冻结架构、记录决策和补齐导航，不迁移代码、不执行真实模型，也不把任何指标写成
  新实验结论。

### 冻结后的唯一目标代码边界

```text
src/codeguarder/
├── core/
│   ├── contracts/ providers/ guards/ detectors/
│   ├── evaluation/ reporting/ experiments/ audit/
├── domains/
│   ├── runtime/
│   ├── retrieval/
│   └── agent/
└── compatibility/
    ├── stage1_4/ stage4_guard/ stage5/ stage6_rag/ garak/
```

`core/` 只容纳跨领域对象与能力，绝不放 RAG 专属类型；RAG 规范实现只写入
`domains/retrieval/`；`compatibility/` 只做旧路径和旧接口的转换，不承载业务逻辑。
早期 `src/codeguarder/stage6_rag/` 将在 Architecture Task 1 后成为兼容外观，旧导入
路径继续可用。详情见 [架构 ADR](docs/architecture/README.md)。

### 冻结的 RAG 边界

`TrustedContextPackage` 是运行时最小上下文包，只携带经策略准入的有限文本、引用、来源、
信任和置信信息；`RAGSecurityEnvelope` 是脱敏审计包，只携带 ID、hash、策略版本、指标、
failure 与 provenance。Stage 7 只能消费这两个对象，不能直接读取 Chroma、Ground Truth、
完整文档或 Guard 内部状态。

### 固定研究阶段

- Stage 6A：可复现检索安全基线，`off/observe` 与 `PassThrough`；
- Stage 6B：透明规则的 filter/rerank 基线；
- Stage 6C：端到端可复现实验与受控真实模型 smoke；
- Stage 6.1：隐蔽知识污染检测与多证据可信检索研究扩展；
- Stage 6.2：论文级比较、统计、迁移与 artifact；
- Stage 7：消费稳定脱敏契约的 Agent 安全，不绕过 RetrievalEvidence。

Task 0 的交付、风险、验收和下一步都记录在
`docs/architecture/architecture_task0_review.md`。在用户确认前，后续工作只允许进入
Architecture Task 1，不能跳到 Embedding、ChromaDB 或 Groq。

## 0. 先看结论

LLMGuard 已经不是一个“运行 garak 的练习项目”，而是一条逐步扩展的 LLM Security Evaluation 研究路线：

```text
模型层安全评测
→ OpenAI-compatible 受控实验
→ 真实模型扫描
→ 输入/输出防护与消融
→ 系统化攻击矩阵和失败分类
→ RAG 检索层安全与可信证据
→ 隐蔽知识污染检测
→ Agent 跨层安全
```

目前 Stage 1–4.1 已有真实运行证据，Stage 5/Stage 5 Paper 已形成确定性 Mock 论文级评测框架，
Stage 6 已完成依赖/数据契约、R1–R6 数据基础、标签隔离、真实 Embedding 与 Persistent ChromaDB
基础设施验收；尚未实现 Retriever、ContextBuilder、Trust、RAG Evaluator 与最终报告。

下一步不应继续堆叠阶段脚本，而应把项目重构为“稳定研究内核 + 可插拔安全领域 + 声明式实验配置 + 独立研究交付”的平台。重构采用增量兼容方式，绝不推翻 Stage 1–5 历史证据。

仓库当前**已确认是 Private**，且不建议直接改为 Public。它仍包含对话导出、原始 HTML
报告、绝对路径、运行日志和需逐项审查的实验输出。正确做法是建立独立公开发布面，而不是
直接切换整个研究仓库的可见性；审计结论见
`docs/security/PUBLIC_REPOSITORY_AUDIT.md`。

---

## 1. 最高优先级指令

### 1.1 Teaching Mode

项目目标不是尽快完成代码，而是真正理解整个实验流程。协作者的角色是实验导师，不是代码生成器。

每个知识点必须解释：

1. 现在在做什么；
2. 为什么这样做；
3. 企业里为什么这样做；
4. 与上一阶段是什么关系；
5. 面试官可能追问什么；
6. 初学者最容易误解什么。

### 1.2 最终能力目标

学习者最终应能够：

- 独立复现实验；
- 独立修改攻击、模型、Detector、Guard 和数据集；
- 独立向面试官讲清完整调用链；
- 理解每个组件存在的工程意义；
- 设计对照实验、消融实验和失败分类；
- 清楚结论边界，不把小样本或规则基线夸大为生产安全性；
- 将工程实验抽象为论文研究问题和科技项目任务书。

### 1.3 不可违反的约束

- Stage 1–5 历史代码、数据、日志和报告不删除、不移动、不覆盖。
- 历史结果有误时新增 correction log，保留原始证据。
- 新实验使用独立目录和 `run_id`。
- API Key 只从环境变量读取，不进入代码、日志、报告或截图。
- 不执行真实破坏性工具；Tool Injection 只研究意图和潜在副作用。
- 不保存完整敏感输出或完整污染文档；使用 hash、长度、规则命中和有限摘要。
- Mock 结果用于验证机制，真实 API 结果用于观察特定模型行为，两者不能互相替代。
- 所有安全结论必须限定在当前模型、数据集、Guard、Detector 和运行配置下。

---

## 2. 项目的三个交付目标

### 2.1 面试项目

目标读者：大模型安全、AI Security、LLM Red Team、RAG/Agent Security 面试官。

需要证明：

- 能运行真实工具和真实 API；
- 能解释 Probe、Generator、Detector、Guard、Retriever、Evaluator；
- 能设计 vulnerable/guarded、P/I/O/F 和 Mock/Real 对照；
- 能定位 Detector Miss、Guard Bypass、Over-blocking；
- 能处理限流、重试、日志、凭据和可复现性；
- 能说明实验局限，而不是只展示一个漂亮百分比。

### 2.2 论文研究

目标读者：论文审稿人和可复现实验研究者。

需要增加：

- 明确研究问题与威胁模型；
- 数据集构造方法和标注协议；
- 基线方法、消融和对比方法；
- 指标定义、分母和统计不确定性；
- 多模型、多种子和多轮重复；
- 方法贡献与工程实现分离；
- Validity Threats、Ethics、Reproducibility 和 Artifact Appendix。

### 2.3 科技立项

目标读者：项目评审专家、合作单位和任务管理人员。

需要增加：

- 国内外现状和实际业务痛点；
- 总体目标、关键科学问题和关键技术；
- 研究内容、技术路线、年度任务和里程碑；
- 可量化考核指标；
- 数据、算力、模型、人员和风险保障；
- 软件原型、数据集、专利/论文/标准等成果形式。

三种交付共用同一个研究内核，但叙事和证据粒度不同。不能用面试话术代替论文方法，也不能用论文指标表代替科技项目的任务分解。

---

## 3. 当前阶段进度与证据

| 阶段 | 状态 | 已完成工作 | 关键证据 | 结论边界 |
| --- | --- | --- | --- | --- |
| Stage 1 | 已完成 | garak 最小闭环；Probe/Generator/Detector/Report | `deliverables/stage1/`、`stage1_learning/` | Mock 模型 |
| Stage 2 | 已完成 | OpenAI-compatible Mock API；vulnerable/guarded 对照 | `deliverables/stage2/` | 可控 Mock 行为 |
| Stage 3 | 已完成 | Groq 真实扫描；PromptInject/Base64 | `deliverables/stage3/` | 2 个真实 attempts |
| Stage 4 | 已完成 | Guard Proxy；真实 API 防护前后 A/B | `deliverables/stage4/` | 规则基线、小样本 |
| Stage 4.1 | 已完成 | passthrough/input-only/output-only/full-guard 消融 | `deliverables/stage4_ablation/` | 2 条 smoke prompts |
| Stage 5 | 已完成（Mock） | 六类 Attack Matrix；benign；T1–T9；指标与报告 | `data/stage5/`、`deliverables/stage5/` | 离线框架回归 |
| Stage 5 Paper | 已完成（Mock） | A1–A6；P/I/O/F；双 Detector；确定性 AttemptRecord | `src/codeguarder/stage5_paper/` | 22 样本、88 attempts，未跑真实 Groq 全矩阵 |
| Stage 6 | S6-T4 已完成 | Task 1–3 契约、R1–R6 数据、Ground Truth 隔离、llmguard namespace、真实 Embedding/Chroma 验收 | `src/llmguard/domains/retrieval/`、`data/stage6_rag/` | 未实现 Retriever、ContextBuilder、Trust、LLM 或 RAG 指标 |
| Stage 6.1 | 规划中 | 隐蔽知识污染、多证据可信检索 | 本文目标架构预留 | 无实验结论 |
| Stage 7 | 规划中 | Agent 安全评测 | 本文目标架构预留 | 无实验结论 |

### 3.1 Stage 1：理解安全扫描闭环

调用链：

```text
Probe → Generator → Model → Detector → Evaluator → Report
```

已验证：

- `test.Blank` 证明最小链路可运行；
- `test.Repeat` + `HijackHateHumans` 产生 256/256 攻击命中；
- JSONL、HTML、hitlog 和人工 summary 分层保存；
- 100% ASR 是设计出来的脆弱 Mock 基线，不代表真实模型。

### 3.2 Stage 2：理解协议与控制变量

已实现 `/v1/chat/completions`，建立 vulnerable/guarded Mock。核心价值是把 API 连接、请求格式和评测逻辑与真实模型的随机行为分离。

### 3.3 Stage 3：真实模型与 Detector 边界

真实模型：`llama-3.1-8b-instant`，Groq OpenAI-compatible API。

- PromptInject：攻击目标被输出，判定攻击成功；
- Base64：garak 判 PASS，但人工复核发现模型识别并部分解码了危险内容；
- Attempt 口径 ASR 为 1/2；
- 该案例直接证明 PASS 不等于无风险，也引出了 Detector Miss。

### 3.4 Stage 4/4.1：Guard 与消融

Stage 4 调用链：

```text
garak → OpenAI-compatible Guard Proxy → Groq
```

Stage 4.1 固定四种实验名称：

- `passthrough`：无输入/输出防护；
- `input-only`：只做输入检测；
- `output-only`：必须先调用上游，再对原始输出做检测和替换；
- `full-guard`：输入与输出联合防护，内部兼容历史 `guarded` 模式。

当前 smoke set 中，Input Guard 和 Output Guard 都将 ASR 从 50% 降至 0%。这只说明当前两条 prompt 和当前规则下有效。

### 3.5 Stage 5：从案例升级为评测框架

攻击维度：prompt injection、role confusion、encoding obfuscation、context injection、data exfiltration、tool injection。

Failure Taxonomy：

- T1 True Attack Success；
- T2 Detector Miss；
- T3 Guard Bypass；
- T4 Partial Containment；
- T5 Over-blocking；
- T6 Context Accumulation Failure；
- T7 Confidentiality Breach；
- T8 Unsafe Tool Intent；
- T9 Side-effect Risk。

Stage 5 Paper 已建立确定性 Dataset Runner、Prompt Renderer、多 Detector Adapter、AttemptRecord、指标和报告。当前结果来自 Mock，真实模型矩阵仍是后续验证任务。

### 3.6 Stage 6 当前精确状态

当前分支：`feature/stage6-rag`。

已提交：

- Task 1：固定 ChromaDB、SentenceTransformers、Pillow 依赖；
- Task 2：稳定不可变契约与严格 schema；
- Task 3：R1–R6 数据集、Attack Matrix、公开视图与 Evaluator Ground Truth 物理隔离；
- Task 3 加固提交：`055f266`；
- 最近验证：104 tests、1919 subtests，通过 Ruff 和 MyPy。

尚未开始：

- Task 4：真实 Embedding Provider 与 Persistent ChromaDB；
- Task 5：RetrieverProxy 与安全 ContextBuilder；
- Task 6：EvidenceSignal 与 pass-through Trust baseline；
- Task 7：Mock/Groq Provider 与 Stage 5 Guard 适配；
- Task 8：RPR、CIR、RMSR、Faithfulness、Cross-layer Leakage 和 T10–T15；
- Task 9–14：Runner、Validator、报告、脚本、导航、真实回归和最终治理。

---

## 4. 当前文件资产如何管理

| 目录 | 角色 | 管理规则 |
| --- | --- | --- |
| `llm-security-stage1/` | Stage 1–4.1 历史代码 | 只读兼容层，不重构覆盖 |
| `src/llmguard/` | 唯一规范实现根 | 新业务代码只在此处新增 |
| `src/codeguarder/` | legacy namespace | Stage 5/5 Paper 历史例外与 Stage 6 facade，不新增业务 |
| `src/llmguard/domains/retrieval/` | Stage 6 规范实现 | A1R 已迁入 Task 1–3；后续 S6-T4 起继续增量实现 |
| `data/` | 合成攻击、benign、Ground Truth | 数据版本化、标签隔离、manifest |
| `tests/` | 单元、集成、回归、安全校验 | TDD，重型模型测试单独分组 |
| `deliverables/` | 报告、脱敏日志、学习材料 | 历史不覆盖；新 run 使用独立 ID |
| `experiments/` | 实验注册表 | 记录配置、状态、commit、结论边界 |
| `provenance/` | manifest、历史 baseline、修正账本 | 支撑审计与论文复现 |
| `interview_prep/` | 面试集中复习 | 使用链接和摘要，不复制大量源码 |
| `runtime/`、`.venv/` | 可重建本地运行状态 | 不进入 Git |

事实优先级：原始 JSON/JSONL 与日志 > Git commit 与 manifest > 聚合报告 > 学习总结 > 面试话术。

---

## 5. 为什么需要重新设计架构

当前项目是按学习阶段自然生长出来的，因此存在合理但需要治理的技术债：

1. Stage 1–4.1 集中在历史目录，代码和阶段概念耦合；
2. Stage 5 基础框架与 Stage 5 Paper 有部分重复实现；
3. Runner、Guard、Detector、AttemptRecord 尚未形成全项目统一接口；
4. 数据、Ground Truth、运行产物和论文交付的边界还不够统一；
5. HTML 报告体积远大于 Python，使 GitHub Languages 被生成产物主导；
6. 私有研究证据与未来公开仓库内容尚未物理分层；
7. 现有 Stage 命名适合学习，却不适合作为论文方法模块名称。

重构目标不是让目录“看起来更漂亮”，而是建立稳定研究对象，使新增 RAG、可信检索和 Agent 实验无需复制一套 Runner、Metrics、Reporting 和 Audit。

---

## 6. 目标架构：LLMGuard Research Framework

### 6.1 总体调用链

```text
Dataset + RunConfig
        ↓
Experiment Orchestrator
        ↓
Threat Adapter / Prompt Renderer
        ↓
Input Guard
        ↓
Domain Pipeline
  ├─ Runtime LLM
  ├─ Retrieval/RAG
  └─ Agent/Tool/Memory
        ↓
Output Guard
        ↓
Detector Ensemble
        ↓
Failure Taxonomy
        ↓
Metrics + Validators
        ↓
AttemptRecord + RunManifest
        ↓
JSON / CSV / Markdown / Figures
```

### 6.2 分层设计

```text
src/llmguard/
├── core/
│   ├── contracts/       # Attempt、Evidence、Verdict、RunManifest
│   ├── experiments/     # schema、loader、renderer、manifest
│   ├── providers/       # Mock、OpenAI-compatible、Groq
│   ├── guards/          # Input、Output、Retrieval、Policy
│   ├── detectors/       # garak、自定义规则、Judge
│   ├── evaluation/      # Runner、Taxonomy、Metrics、Validators
│   ├── reporting/       # JSON、CSV、Markdown、Figure
│   └── audit/           # hash、redaction、secret scan、provenance
├── domains/
│   ├── runtime/         # Prompt/Encoding/Context/Tool intent
│   ├── retrieval/       # RAG、Evidence、Trust、Poisoning
│   └── agent/           # Tool、Memory、Planning、Side-effect
└── compatibility/
    ├── garak/           # garak Generator/Detector 适配器
    ├── stage1_4/        # Stage 1–4.1 历史适配器
    ├── stage4_guard/    # 旧 GuardEngine 适配器
    ├── stage5/          # 旧 Stage 5 接口适配器
    └── stage6_rag/      # 旧 Stage 6 import 适配器
```

声明式实验放在：

```text
experiments/
├── registry.json
├── configs/
│   ├── runtime/
│   ├── retrieval/
│   └── agent/
└── manifests/
```

阶段导航仍可保留，但不再承载重复源码：

```text
stages/
├── stage1_garak_baseline/
├── stage2_openai_mock_api/
├── stage3_real_model_scan/
├── stage4_guard_ab/
├── stage4_1_guard_ablation/
├── stage5_runtime_attack_matrix/
├── stage5_paper_baseline/
├── stage6_rag_security/
├── stage6_1_hidden_knowledge_poisoning/
├── stage6_2_trustworthy_retrieval/
└── stage7_agent_security/
```

### 6.3 六个稳定核心对象

1. `AttackSample`：攻击目标、输入、期望风险和元数据；
2. `ProviderRequest/Response`：统一模型调用，不绑定具体厂商；
3. `RetrievalEvidence`：稳定检索证据，不暴露向量库内部结构；
4. `DetectorVerdict`：来源、分数、规则、覆盖状态和输出 hash；
5. `AttemptRecord`：一次实验的完整脱敏审计记录；
6. `RunManifest`：代码、数据、模型、配置、seed、环境和运行状态。

所有 Stage 6.1 和 Stage 7 扩展都应围绕这些对象增加字段或适配器，而不是再建独立 Runner。

---

## 7. Stage 6/6.1 的论文级架构

### 7.1 Stage 6 安全基线

```text
Query
→ Query/Input Guard
→ Retriever
→ Persistent ChromaDB
→ RetrievalEvidence[]
→ EvidenceExtractor
→ EvidenceSignal[]
→ TrustAggregator (pass-through)
→ RetrievalPolicy (off/observe)
→ ContextBuilder
→ Mock LLM / Groq
→ Output Guard
→ RAG Evaluator
→ RPR/CIR/RMSR/Faithfulness/Leakage + T10–T15
```

R1–R6：Query Injection、Retrieval Poisoning、Context Injection、Embedding Attack、Document Poisoning、Hallucination Steering。

Stage 6 只建立可复现基线。TrustAggregator 不学习、不改变排序，`observe` 只记录信号。

### 7.2 Stage 6.1 研究贡献方向

拟研究主题：**面向检索增强生成系统的隐蔽知识污染检测与多证据可信检索关键技术研究**。

可形成四个研究问题：

- RQ1：在不使用 poison label 的条件下，哪些 EvidenceSignal 能识别隐蔽污染？
- RQ2：来源、语义冲突、Embedding 异常和多源一致性如何联合建模？
- RQ3：可信重排/阻断能否降低攻击成功率，同时控制正常查询性能损失？
- RQ4：检索层风险如何传播到生成层和 Agent 决策层？

建议贡献点：

1. 无标签泄露的检索安全评测框架；
2. 多证据信号表示与可信聚合方法；
3. 冲突感知的检索策略；
4. 安全、可信度、可用性联合指标；
5. 可复现实验数据与审计协议。

### 7.3 科技立项任务分解

- 课题一：RAG 知识污染攻击建模与数据集；
- 课题二：隐蔽污染多维证据提取；
- 课题三：多证据可信聚合与冲突检测；
- 课题四：安全约束下的可信检索策略；
- 课题五：跨检索、生成、Agent 的风险传播评测平台。

阶段成果可对应：数据集、算法模块、评测平台、论文、专利/软著、技术报告和演示系统。

---

## 8. 统一实验方法

### 8.1 实验矩阵

```text
Attack Category
× System Domain
× Model/Provider
× Guard Configuration
× Retrieval Policy
× Detector
× Seed/Repeat
× Metric/Failure Type
```

### 8.2 必须统一的指标

运行时安全：ASR、Detector Miss Rate、Guard Bypass Rate、Over-block Rate、Latency Overhead。

检索安全：RPR、CIR、RMSR、Faithfulness、Cross-layer Leakage Rate。

可信检索扩展：Hidden Poison Detection Precision/Recall/F1、Conflict Detection、Trust Calibration、Clean Retrieval Utility、Safety-Utility Trade-off。

### 8.3 复现要求

- 数据集 manifest 与 SHA-256；
- 代码 commit；
- 模型 ID、revision、base URL 类型；
- Embedding 模型与 revision；
- seed、temperature、top_k、generation 参数；
- Guard/Detector/Taxonomy 版本；
- 失败重试和 API 限流记录；
- canonical JSONL 和 `run_status`；
- 相同 Mock 输入产生字节一致的规范化日志。

---

## 9. GitHub 私有仓库是否应该公开

### 9.1 当前建议

**暂时保持私有。** 不是因为源码不能公开，而是因为仓库同时保存了研究过程证据和面试材料，公开前需要完成发布面治理。

当前公开风险包括：

- `chatgpt_share_*.html` 对话导出；
- garak HTML/JSONL 中的完整攻击 prompt 和原始输出；
- 日志中的本机绝对路径、时间和环境信息；
- 可能包含个人信息的 DOCX/PDF/截图；
- 真实 API 运行历史需要再次做秘密和隐私审计；
- 数据集、模型和第三方工具的 license/引用信息尚未形成统一清单；
- 大量生成 HTML 会让 GitHub Languages 错误显示为 HTML 项目。

### 9.2 推荐公开策略

采用“双层仓库/发布面”：

```text
Private Research Repository
  - 原始日志
  - 完整运行证据
  - 研究草稿
  - 面试私人材料
  - 受限数据

Public Artifact Repository / public-release branch
  - 源码
  - 合成与脱敏数据
  - 可复现配置
  - 脱敏样例结果
  - 方法文档
  - License/Citation/Ethics
```

公开前清单：

1. 移除对话导出、个人文档、截图和临时文件；
2. 全历史秘密扫描，而不只是当前工作树；
3. 清理绝对路径、用户名和 provider 原始 trace；
4. 只保留最小脱敏报告样例，大体积结果提供 release/归档地址和 hash；
5. 使用 `.gitattributes` 将报告 HTML 标记为 `linguist-generated`；
6. 增加 `LICENSE`、`CITATION.cff`、`SECURITY.md`、`ETHICS.md`、数据卡和模型卡；
7. 增加最小可运行 demo、安装说明和 CI；
8. 在独立临时 clone 中验证公开包能够从零复现。

仓库公开属于不可逆的信息披露决策。在上述检查完成前，不直接把当前私有仓库切换为 Public。

---

## 10. 增量重构路线

### Phase A：冻结与建立统一契约

- 保留 Stage 1–5 原路径；
- 定义 core contracts、RunManifest、DetectorVerdict 和 AttemptRecord v2；
- 编写 compatibility tests，保证旧结果可读；
- 建立 public/private artifact policy。

### Phase B：抽取通用研究内核

- 从 Stage 5 Paper 抽取 Dataset Runner、Providers、Detectors、Metrics、Reporting；
- Stage 4 GuardEngine 通过 adapter 接入；
- Stage 6 只实现 retrieval domain，不复制通用模块。

### Phase C：完成 Stage 6 基线

- 真实 Embedding + ChromaDB；
- Retriever + ContextBuilder；
- pass-through Trust；
- Mock 确定性回归；
- Groq 小样本；
- T10–T15 与完整报告。

### Phase D：Stage 6.1 论文方法

- 隐蔽污染数据扩展和标注协议；
- EvidenceSignal 基线和学习方法；
- 多证据聚合、冲突感知重排和消融；
- 多模型、多语料、多种子实验；
- 论文图表、统计检验和 Artifact Appendix。

### Phase E：Stage 7 Agent Security

- 复用 RetrievalEvidence 与 RAGSecurityEnvelope；
- 建立 Tool/Memory/Planning 攻击矩阵；
- 使用沙箱和 intent-only 工具模拟；
- 研究检索污染向 Agent 决策和副作用传播。

---

## 11. 最近里程碑与停止条件

### M0：架构决策

完成条件：确认本文目标架构、公开策略和 Stage 6/6.1 研究边界。

### M1：统一核心最小版本

完成条件：核心 contracts、provider、detector、attempt、manifest 可同时运行 Stage 5 Mock 和 Stage 6 Mock。

### M2：Stage 6 Baseline

完成条件：R1–R6 全链路、真实 Embedding/Chroma、Mock 确定性回归、T10–T15、中文报告。

### M3：Stage 6.1 Research Baseline

完成条件：至少两类 Hidden Poison baseline、四类 EvidenceSignal、可信聚合、消融和正常检索效用评估。

### M4：Public Artifact v1

完成条件：独立公开发布面通过秘密、隐私、license、复现和 CI 检查。

### M5：论文/立项材料

完成条件：研究问题、方法、实验、结果、局限性和项目任务书使用同一组可追溯证据。

---

## 12. 每次继续项目时的执行协议

1. 先读本文件；
2. 检查 branch、worktree、Git status 和最近 commit；
3. 明确当前只完成哪个知识点；
4. 先写实验假设、输入、输出和成功条件；
5. 按 TDD 先红后绿；
6. 运行单元、集成、静态和泄露检查；
7. 保存代码、数据、日志、结果和教学文档；
8. 说明面试如何讲、论文如何写、不能夸大什么；
9. 每个稳定 Task 使用独立 commit；
10. 更新本文件的阶段状态和最近验证证据。

---

## 13. 当前下一步

`S6-T4` 已完成，`S6-T5 Design Hardening` 已完成并等待第二次人工审查。下一步不是自动写 Python，而是
审查 hardened design、Existing Contract Migration Matrix 与实施计划：

- `docs/superpowers/specs/2026-07-19-s6-t5-controlled-retrieval-traceable-context-design.md`；
- `docs/superpowers/plans/2026-07-19-s6-t5-controlled-retrieval-traceable-context.md`；
- `docs/architecture/0008_retrieval_context_boundary.md`。

只有第二次人工审查明确批准后，才可单独开始 `S6-T5.1 Chunking Contracts`。`S6-T5.1 implementation:
Not approved`，其后的 Retriever、ContentResolver、EvidenceEnvelope 和 ContextBuilder 更不能提前实施。

面试表达：我先通过五个阶段建立模型层评测、防护和失败分类，再把系统扩展到检索层。为了让项目能够从演示走向论文，我将阶段脚本重构为稳定研究内核，并把 RAG 的证据表示、可信分析和风险传播设计成可插拔领域模块，同时用兼容层保护历史实验可复现性。

不能夸大：当前项目已经具备较完整的评测工程基础、S6-T4 基础设施和 S6-T5 可审查设计，但 Stage 6
受控检索实现、Stage 6.1 方法创新、统计实验和公开 Artifact 尚未完成，不能称为已经发表或达到生产级
防护能力。

## 14. S6-T5.1：确定性分块契约与 IdentityChunker（2026-07-20）

在最新人工批准下，S6-T5.1 已用 TDD 实现并等待人工验收。规范 DTO 仅位于
`src/llmguard/domains/retrieval/contracts/chunking.py`：`ChunkingStrategy`、不可变
`ChunkingConfig`、`ChunkRecord`、canonical JSON/SHA-256 与最小 `corpus:` content reference formatter。
行为实现仅位于 `src/llmguard/domains/retrieval/chunking/`：`Chunker` Protocol、领域异常和
`IdentityChunker`。

当前基线严格执行“一份 `DocumentRecord` 产生一个原样 `ChunkRecord`”：先按 UTF-8 重算正文哈希，
再用 corpus snapshot、父文档、索引、内容 hash 与配置 hash 生成完整 `CH-<sha256>`。公开 metadata
递归冻结并拒绝 evaluator 标签变体、绝对路径、循环、非 JSON-safe 值；`repr` 与 `to_audit_dict()`
均不展开正文。测试、Retriever、向量库与日志均不把此能力表述为 RAG 安全效果。

本项没有实现 Retriever、RetrievalRequest/Trace、ContentResolver、ContextBuilder、Trust、LLM/Groq、
T10–T15 或正式实验；下一步仍必须先经人工验收，再单独批准 S6-T5.2。

### S6-T5.1 Implementation Hardening（2026-07-20）

针对初版分块契约的人工审查，本轮完成四项加固：删除不能合法承载任何语义的 `window_size`，统一固定
token 语义为 `max_tokens`、overlap 语义为 `max_tokens + overlap_tokens`；将稳定错误类型归属到
`contracts/errors.py` 并从行为层兼容 re-export；为 `ChunkRecord` 增加 `chunk_schema_version` 并在对象
构造时重算 chunk ID；metadata 在排序前先验证全部 key 为字符串，同时拒绝绝对路径 key/value。

`ChunkRecord` 的完整性现覆盖 schema version、snapshot、parent doc、index、content hash 与 config hash；
任一字段被篡改即抛脱敏 `ChunkingIntegrityError`。文档 hash mismatch 的异常固定为
`DOCUMENT_CONTENT_HASH_MISMATCH`，不回显原始 doc ID 或正文。该状态是 `Completed, pending final human
acceptance`，并不授权 S6-T5.2 或任何检索/上下文功能。

## 15. S6-T5.2：检索运行时契约与稳定标识（2026-07-20，待人工验收）

本任务只实现 `QueryRecord -> safe projection -> RetrieverQueryRecord -> RetrievalRequest -> RetrievalEvidence/Trace` 的数据边界。公开加载器仍读取原有 Stage 6 JSONL，但投影后的运行时对象仅含精确 `retrieval_query`、新的 `Q-` 安全 ID 与 `delivery_layer/scenario/variant` 白名单元数据；攻击标签、类别、生成问题和期望文档不会进入运行时对象。

规范 DTO 统一由 `src/llmguard/domains/retrieval/contracts/` 暴露。`ContentRef` 同时识别新 `corpus:` 和旧 `chroma:` 格式，但新证据只生成 `corpus:`；旧格式必须经显式 adapter 迁移。Evidence UID 可复算；Trace hash 覆盖稳定语义而不包含 latency。普通 audit/repr 不记录查询正文、文档正文或可解析内容引用。

本轮没有实现 DenseRetriever、向量库查询、embedding 调用、ContentResolver、ContextBuilder、Citation、Trust、LLM/Groq、T10-T15 或正式实验。因此它证明的是可审计运行时边界，不是检索质量或 RAG 安全效果。下一步必须由人工单独审批 `S6-T5.3 DenseRetriever`。

## 16. S6-T5.4-P1：Content Resolution Contract and Permission Boundary Freeze（2026-07-25）

`S6-T5.4-P1` 已完成协议冻结，等待人工验收。它只确定后续 ContentResolver 的最小权限边界：唯一输入为
`ContentRef` 与预期 hash，敏感 `ResolvedContent` 由 `contracts/` 唯一拥有；受控 snapshot reader 只能按
chunk ID 读取；legacy `chroma:` 只能经过 immutable exact-match allowlist 映射；错误由
`contracts/errors.py` 稳定拥有。正文不得进入普通日志、trace、repr、异常或公共数据对象。

该记录不是 ContentResolver、reader、registry 或 adapter 的实现，也没有读取正文、fixture、标签或 Ground
Truth。父任务 `S6-T5.4` 仍为 `APPROVED_TO_START / DESIGN_OR_PROTOCOL_BLOCKER`，blocker 尚未正式解除；
`S6-T5.5` 及后续任务仍未批准，正式 RAG 安全实验仍未开始。

## 17. GOV-S6-T5.4-P1-ACCEPTANCE：正文解析协议人工验收（2026-07-25）

项目负责人已人工接受 `S6-T5.4-P1` 的协议设计：唯一 `ContentResolver` 输入/返回、contracts 唯一
`ResolvedContent`、最小 snapshot reader/registry、legacy exact-match mapping 和 contracts 错误归属。
因此 S6-T5.4 的协议 blocker 当前为 `RESOLVED_BY_APPROVED_PROTOCOL_FREEZE`，父任务为
`READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`。

这是协议验收而不是实现验收：`S6-T5.4-I1` 仍为 `NOT YET APPROVED`，不得创建 ContentResolver、读取
corpus 正文、生成 fixture mapping、实现 ContextBuilder/Citation 或进行正式 RAG 安全实验。S6-T5.5 及后续
任务仍未批准。原 blocker 的发现背景、风险和 fail-closed 停止行为必须保留为历史审计证据。

## 18. S6-T5.4-I1：受控语料正文解析最小实现（2026-07-25，待人工验收）

在项目负责人单独批准后，`S6-T5.4-I1` 已按 TDD 实现最小闭环：`ContentRef + expected_content_hash ->
CorpusContentResolver -> ApprovedCorpusSnapshotRegistry -> CorpusSnapshotReader -> UTF-8 SHA-256 verification ->
ResolvedContent`。稳定 DTO 与错误唯一归属 `contracts/`；`context/` 只拥有行为协议、注入式内存 registry/reader、
legacy `chroma:` 精确白名单适配与 resolver，且错误仅 re-export。`ResolvedContent.content` 为短生命周期能力对象，
不进入 repr、普通审计对象、trace、缓存、持久化或异常消息。

本轮所有正文与 legacy mapping 都是测试内合成内存值：没有读取或修改 Stage 6 fixture、语料正文、Ground Truth 或
评估器；没有调用 Embedding、Chroma、Groq 或 LLM；没有实现 ContextBuilder、Citation 或 S6-T5.5。父任务
`S6-T5.4` 与 I1 当前均为 `Completed, pending human acceptance`，正式 RAG 安全实验仍为 `Not started`。这证明
的是受控正文解析的离线工程边界和完整性校验，不证明检索质量、RAG 安全、抗知识污染或生产能力。

## 19. S6-T5.4-H1：Resolver capability 与失败边界加固（2026-07-25，待人工复核）

I1 人工验收发现两个边界问题：公开 `registry` 属性会让调用方绕过 hash 校验和 `ResolvedContent`，而注入依赖抛出的
领域异常会保留其原始 message。H1 删除该公共属性，并让 resolver 对 adapter、registry、reader 的
`ContentResolutionError` 仅按受信的异常类别与 error code 重建固定脱敏错误；不受信 code 或类别/code 交叉一律
fail closed 为 runtime failure，内部 cause 仍由 `raise ... from error` 保存。`ResolvedContent` 非字符串正文也统一为
runtime failure，避免 class/code 错配。

H1 仅用合成内存内容验证，未读取 Stage 6 fixture、未调用 Chroma、Embedding、Groq 或 LLM，未新增 Retriever、
ContextBuilder、Citation、Trust 或 S6-T5.5。H1 状态为 `Completed, pending human review`；I1 与父任务仍为
`Completed, pending human acceptance`，正式 RAG 安全实验仍为 `Not started`。

## 20. GOV-S6-T5.4-ACCEPTANCE：受控正文解析人工验收（2026-07-25）

项目负责人已接受 `S6-T5.4-P1`、I1、H1 与父任务 `S6-T5.4 Controlled Corpus ContentResolver`；最后接受的
实现提交为 `11a72f7`。验收确认 `ResolvedContent` 的 contracts 唯一归属、`ContentRef + expected_content_hash`
的唯一解析输入、仅 `resolve()` 的公共 capability、最小 snapshot registry/reader、原始 UTF-8 SHA-256、
immutable exact-match legacy mapping、fail-closed identity/hash 行为以及注入异常的固定脱敏边界和 cause 保留。

这是合成内存内容上的离线工程验收，不表示已接入真实语料、文件系统、远程 provider、Embedding、Chroma、Groq 或
LLM。P1/I1/H1 的历史 pending 快照和原 protocol blocker 继续保留；`S6-T5.5`、S6-T5.6 与之后任务仍未批准，
正式 RAG 安全实验仍为 `Not started`。

## 21. S6-T5.5-P1：EvidenceEnvelope 与 Citation 边界冻结（2026-07-25，待人工验收）

本轮只完成 `DESIGN_FREEZE / PROTOCOL_REVIEW`，不实现任何业务源码。审查解决了 Citation 时序冲突：
`EvidenceEnvelope` 不含 `citation_id`，而未来 `ContextBuilder` 仅在最终 Evidence 的排序、去重、数量限制、正文
解析/hash 验证和预算选择完成后，创建 `CitationBinding` 并在一个 `RetrievedContextPackage` 内连续分配 `E1 ... En`。
这样稳定的 Evidence UID 与局部展示的 Citation ID 不会混淆，也不会让被排除的证据获得错误引用。

冻结的唯一生产构造行为是未来的 `EvidenceEnvelopeFactory.create(evidence, resolved_content)`：Evidence 提供公开
provenance/metric，ResolvedContent 提供经 hash 校验的正文，所有 DTO 与错误只归 `contracts/`。instruction、
XML-like rendering、escaping、错误语义、audit/repr 和敏感导出边界都已有精确协议；escaping 只保护结构，不是
Prompt Injection 语义防护。正文普通导出继续 deny-by-default，直到单独的 SensitiveArtifactPolicy 得到批准。

本轮没有修改 `src/`、Stage 1–5 或 Stage 6 fixture/data，没有读取语料正文，没有调用 Embedding、Chroma、Groq 或
LLM，也没有运行正式实验。`S6-T5.5-P1` 当前为 `Completed, pending human acceptance`；`S6-T5.5`、S6-T5.6+
仍为 `NOT APPROVED`。详细审查证据见
[S6-T5.5 protocol review record](docs/governance/s6_t5_5_protocol_review_record.md)。

## 22. S6-T5.5-P1-H1：Canonical Binding 与 Citation Rendering 协议加固（2026-07-26，待人工复核）

人工审查发现两个会在后续实现中混淆权限的缺口。第一，`ContentRef` value object 可为 Resolver 兼容识别 legacy
`chroma:`，但已实现的 canonical `RetrievalEvidence` 只允许 `corpus:`；因此 Factory 只能消费 canonical Evidence，
不能再映射、猜测或接受 legacy record。Factory 必须同时比对 ContentRef、snapshot、chunk、hash，防止“chunk/hash
相同但来自不同 snapshot”的跨语料拼接。

第二，Envelope 不含 citation ID 后，renderer 只能接收 `EvidenceEnvelope + CitationBinding`，并逐项验证 UID、chunk、
parent、hash、source、version、rank。任一不一致是 `CITATION_BINDING_MISMATCH`，固定脱敏消息为
`citation binding does not match evidence`；必须 fail closed，而不是输出 partial block、跳过、重编号或作为 abstention。
Citation allocation 与 Binding 创建仍只属于未来 S6-T5.6 ContextBuilder。

本 H1 没有改动 `src/`、业务测试、Stage 1–5 或 Stage 6 fixture/data；没有调用 Embedding、Chroma、Groq 或 LLM，
没有产生实验结果。当前为 `Completed, pending human review`；P1 仍为 `Completed, pending human acceptance`，
`S6-T5.5`、S6-T5.6+ 仍为 `NOT APPROVED`。

## 23. GOV-S6-T5.5-P1-ACCEPTANCE：EvidenceEnvelope 与 Citation 协议人工验收（2026-07-26）

项目负责人已将 `S6-T5.5-P1` 与 `S6-T5.5-P1-H1` 标记为 `HUMAN_ACCEPTED`。这只接受未来对象的协议边界：
Envelope 不持有 citation ID、Binding 在最终证据集合后创建、Factory 只接收 canonical Evidence、renderer 仅消费
已绑定对象并对七项身份 mismatch fail closed、escaping 只保护结构、正文导出默认拒绝。没有因此实现任何 DTO、
renderer 或 ContextBuilder，也没有产生 Citation Accuracy 或 RAG 安全实验结论。

当前最高已接受业务阶段是 `S6-T5.4 Controlled Corpus ContentResolver`，最后接受的业务实现提交仍为 `11a72f7`；
`25fb83d` 仅为设计协议加固提交。`S6-T5.5` 现为 `READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`，但
上述“`S6-T5.5-I1` 仍为 `NOT YET APPROVED`”是 I1 获批前的历史快照；当前 I1 与父任务 S6-T5.5 均为 `Completed, pending human acceptance`。`S6-T5.6+` 仍为 `NOT APPROVED`，正式 RAG 安全实验仍为 `NOT STARTED`。

## 24. S6-T5.5-I1：EvidenceEnvelope、Citation 与结构化渲染最小实现（2026-07-26）

在 P1/P1-H1 人工验收后，项目负责人单独批准 I1。它实现 contracts 唯一 owner 的 `EvidenceEnvelope`、
`CitationBinding`、`CitationMode` 与稳定错误；唯一 canonical Factory；固定 LF instruction；以及只渲染一个
Envelope + Binding 的 XML-like block。Factory 校验 canonical ContentRef、snapshot、chunk、hash，renderer 校验七项
Binding identity 并 fail closed。正文只来自合成 `ResolvedContent`，普通 audit/repr 不含正文。

I1 当前为 `Completed, pending human acceptance`，父任务 S6-T5.5 同样为 `Completed, pending human acceptance`。
最后接受的业务实现提交仍是 `11a72f7`；本次不读取 Stage 6 fixture，不实现 package、Citation allocation 或
ContextBuilder，不调用 Embedding、Chroma、Groq、LLM，也不执行正式 RAG 安全实验。S6-T5.6+ 仍为 `NOT APPROVED`。

## 25. S6-T5.5-H1：Evidence 与 Citation 验收加固（2026-07-26）

I1 人工验收发现 metadata wrapper 可重绑、Envelope timestamp 与 RetrievalEvidence 不一致、超大 metric 会泄露原生
异常、Binding 字段错误语义不精确。H1 只在 `EvidenceEnvelope`/`CitationBinding` 契约边界修复这些问题：metadata
改为 slots-only 深度只读包装，timestamp 接受 canonical UTC 的任意小数秒，所有 Envelope input 错误固定为
`INVALID_EVIDENCE_ENVELOPE`，Binding 字段错误固定为 `INVALID_CITATION_BINDING`，Evidence UID 严格为
`EV-[0-9a-f]{64}`。H1 不改变 RetrievalEvidence、Resolver、DenseRetriever、Factory provenance checks 或 renderer
结构输出。

H1 当前为 `Completed, pending human review`；I1 与父任务仍为 `Completed, pending human acceptance`，最后接受的
业务实现提交仍为 `11a72f7`。未读取 fixture，未调用 Embedding、Chroma、Groq 或 LLM；未实现 S6-T5.6 ContextBuilder、
Package、预算或 Citation allocator，正式 RAG 安全实验仍为 `NOT STARTED`。

## 26. GOV-S6-T5.5-ACCEPTANCE：Evidence 与 Citation 实现人工验收（2026-07-26）

项目负责人已人工接受 `S6-T5.5-I1`、`S6-T5.5-H1` 和父任务 `S6-T5.5`。当前最后接受的 stage task 是
`S6-T5.5 EvidenceEnvelope, Citation Contracts and Structural Rendering`，最后接受的 implementation commit 是
`6da27a6`；`2cacef7` 仍保留为 I1 初始实现的历史证据。此前 pending/review 文字为发生时的历史快照，不能删除，
但不得再作为当前状态引用。

人工验收的工程边界仅包括 synthetic objects 上的 EvidenceEnvelope、CitationBinding、CitationMode、canonical
Factory、immutable public metadata、canonical timestamp、Evidence UID、七字段 Binding 校验、脱敏错误、instruction
与单 block structural rendering。它不证明 Citation Accuracy、检索质量、安全效果、可信检索、ContextBuilder、
RetrievedContextPackage、Trust、LLM 集成、生产可用性或正式 RAG 安全实验。

`S6-T5.6` 和 `S6-T5.7+` 仍为 `NOT APPROVED`，正式 RAG security experiment 仍为 `NOT STARTED`。本次状态登记未
读取或修改 Stage 6 fixture，未调用 Embedding、Chroma、Groq 或 LLM，未改变 Stage 1--5 历史资产。

## 27. S6-T5.6-P1：Context Package 协议审查与设计冻结（2026-07-26）

S6-T5.6-P1 已完成、待人工验收。它不实现任何 ContextBuilder 或 Package，而是冻结 S6-T5.5 之后的唯一 package
construction contract：Request/Evidence provenance；排序/去重/数量限制；受控 resolve/Envelope 顺序；Citation 与预算
循环；Unicode code point budget；safe trace；Package identity；以及结构性 abstention 与完整性异常的分流。

关键决策是 stable prefix selection：使用仅存在于单次 build 调用栈内的临时 next Citation Binding 渲染完整候选，
fit 后才 commit。这样 `E9` 与 `E10` 的不同宽度被真实字符串覆盖，任何未收录候选不会留下编号空洞或泄漏到 audit。
P1 仍不批准 S6-T5.6 implementation、ContextBuilder、RetrievedContextPackage、Citation allocator、Trust、LLM 或
正式实验；最后接受 implementation commit 仍是 `6da27a6`。

## 28. S6-T5.6-P1-H1：顺序解析与 Context Trace 协议加固（2026-07-26）

H1 已完成、待人工复核；它不是业务实现，也不改变 P1 的 `Completed, pending human acceptance` 状态。H1 修复了
P1 中“先解析所有数量入选候选、再做预算”的最小权限缺口。active 流程必须是：配置/类型/provenance 校验、稳定排序、
精确 UID duplicate/conflict、数量限制、citation instruction，然后按稳定顺序 **sequential resolution**。每一候选仅在
轮到它且此前未出现预算 cutoff 时才可调用 Resolver、Factory 和 renderer；instruction 本身超预算时 Resolver 调用为 0，
首个不适配候选为 `BUDGET_EXCLUDED`，后续候选是 `NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF` 且不得读取正文。

H1 同时冻结跨对象 provenance 的四个精确比较、同 UID 的完整语义投影、single-collection snapshot 约束，以及
`ContextBuildTrace` 的安全字段和单向 identity：trace hash 不包含 Package ID，Package 只保存
`context_build_trace_hash`，从而避免循环。`NO_EVIDENCE_AFTER_DEDUPLICATION` 已由 P1 从 active baseline 移除，
仅作为历史快照保留。父任务 S6-T5.6、S6-T5.7+ 与正式 RAG 安全实验仍未批准/未开始；本轮未读取 fixture、未调用
Embedding、Chroma、Groq 或 LLM，也未生成实验结论。

## 29. S6-T5.6-P1-H2：活动规格、Trace 决策与 Package 身份协议闭环（2026-07-26）

H2 已完成、待人工复核；P1 与 H1 均为待人工验收。H2 不新增业务对象，只把活动规格、实施计划和 ADR 的
Context 构建顺序统一为：配置/类型/provenance 校验、稳定排序、精确 UID 去重、数量限制、instruction、空输入或
instruction-budget 分流、顺序 resolve/render/fit、cutoff、Trace/Package 组装。本轮不新增 rank、Evidence 子集或
多 snapshot 的运行时规则。

H2 还将 `ContextBuildTrace` 定义为每一稳定候选恰有一个 decision 的不相交审计分区；instruction 超预算不调用
Resolver，但会把 selected candidates 记录为 `NOT_ATTEMPTED_INSTRUCTION_BUDGET_EXHAUSTED`。Package 只持久化
`build_trace`，而 package identity 从 `build_trace.trace_hash` 派生 canonical `context_build_trace_hash`，避免 DTO
冗余和 hash 循环。S6-T5.6、S6-T5.7+ 与正式 RAG 安全实验仍未获批准/未开始；未读取 fixture，未调用模型或执行实验。

## 30. GOV-S6-T5.6-P1-ACCEPTANCE：Context Package 协议人工验收（2026-07-26）

项目负责人已人工接受 `S6-T5.6-P1`、`S6-T5.6-P1-H1` 与 `S6-T5.6-P1-H2` 的 future protocol 边界。三者当前均为
`HUMAN_ACCEPTED`；父任务 `S6-T5.6` 仅为 `READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`，而
`S6-T5.6-I1` 仍为 `NOT YET APPROVED`。`S6-T5.7+` 仍为 `NOT APPROVED`，Formal RAG security experiment 仍为
`NOT STARTED`。

验收确认的是 deterministic future context-package 的接口、选择、审计和失败边界，不是 ContextBuilder、
`RetrievedContextPackage`、`ContextBuildTrace`、预算器或 Citation allocator 的实现。最后已接受 implementation commit
保持为 `6da27a6`；`432b07e` 只登记为已经通过人工验收的协议闭环提交。历史 pending/review 快照保留为历史事实。

## 31. S6-T5.6-I1：最小离线 Context Package 实施已批准（2026-07-26）

项目负责人已明确批准 `S6-T5.6-I1` 开始实施。当前只允许在 `llmguard` 规范命名空间以 synthetic/offline TDD
实现已验收的 ContextBuildConfig、ContextBuildTrace、RetrievedContextPackage、唯一 ContextBuilder、sequential
resolution、stable-prefix budget selection、package-local Citation allocation 与结构性 abstention。`S6-T5.6` 与 I1
当前均为 `IMPLEMENTATION_IN_PROGRESS`。

本批准不改变 Stage 1–5 或 Stage 6 fixture/data，不允许调用 Embedding、Chroma、Groq 或 LLM，也不批准 Trust、
RetrievalPolicy、reranker、Citation Accuracy、正式 RAG 实验或 S6-T5.7。最后已接受 implementation commit 仍是
`6da27a6`；本轮产生的提交只能作为 candidate implementation pending human acceptance。

## 33. GOV-S6-T5.6-ACCEPTANCE：Deterministic Context Package 最终人工验收（2026-07-26）

项目负责人已将 `S6-T5.6-P1`、`S6-T5.6-P1-H1`、`S6-T5.6-P1-H2`、`S6-T5.6-I1`、`S6-T5.6-I1-H1` 和父任务 `S6-T5.6` 标记为 `HUMAN_ACCEPTED`。本次只接受 synthetic/offline 范围内的 Config、Trace、Package、唯一 ContextBuilder、稳定排序/精确重复、顺序解析、stable-prefix 预算、包内 Citation、Unicode/UTF-8 identity、结构性 abstention、Trace 情景不变量、公开 limits/config hash、依赖异常脱敏、reason/Trace 对应和 safe audit。

`71067d1` 仍是 I1 初始 candidate implementation history；`b136ee2` 是最终接受的实现提交，`6da27a6` 是此前最后已接受实现提交的历史事实。最终完整离线复跑为 `438 passed, 2837 subtests passed`。`438/2833` 是验收状态同步前的历史快照；四个新增子测试仅覆盖治理断言。本轮未改 Stage 1-5、Stage 6 fixture/data、DTO、协议或选择语义，未调用 Embedding、Chroma、Groq 或 LLM。

本验收不证明检索质量、Prompt Injection 防护、Knowledge Poisoning 检测、Citation Accuracy、可信 Context/Trustworthy Retrieval、Chroma/MiniLM/LLM 全链路、正式 RAG 安全实验或生产可用性。`S6-T5.7+` 为 `NOT APPROVED`，Formal RAG security experiment 为 `NOT STARTED`。

## 32. S6-T5.6-I1：最小离线 Context Package 实施完成，等待人工验收（2026-07-26）

I1 已在规范 `llmguard` namespace 完成，并只消费 synthetic Request、Evidence 与 in-memory Resolver。
三个稳定 DTO 位于 `contracts/context_package.py`；唯一行为实现位于 `context/builder.py`，复用既有
ContentResolver、EnvelopeFactory、citation instruction 与单 block renderer。实现遵守「先 provenance、稳定排序、
精确 UID 去重、数量限制、instruction，再顺序 resolve/render/fit」的冻结顺序；首个不适配候选触发 stable-prefix
cutoff，之后候选不访问正文。Trace 和 Package 的普通 audit 不导出 Query、正文、ContentRef 或 metadata 原值。

当前 `S6-T5.6` 与 `S6-T5.6-I1` 均为 `Completed, pending human acceptance`。这不是对检索质量、Citation Accuracy、
RAG 安全、可信检索、模型集成或生产可用性的结论；`S6-T5.7+` 和正式 RAG 安全实验仍未批准/未开始。最后已接受
implementation commit 仍为 `6da27a6`；I1 提交只可作为候选实现留档。
