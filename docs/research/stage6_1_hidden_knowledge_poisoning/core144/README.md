# Core144 navigation

**当前R02：** [CUDA显存硬停](vace_lite/VACE_L0_R02_CUDA_OOM_BLOCKER_V1.md)，[状态V30](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V30.md)。
预检通过；合成工程通过、语义4/5仅诊断。F5 5条后OOM，无D1指标。R01/R02硬停都保留。

**历史：R02批准：** [Owner批准与执行合同](vace_lite/VACE_L0_R02_OWNER_APPROVAL_AND_EXECUTION_V1.md)，[状态V29](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V29.md)。
同模型/prompt/parser/证据，只将合成语义全对门改诊断。实际执行结果见上方V30。

**当前5090结果（2026-10-29）：** [虚构合成门硬停](vace_lite/VACE_L0_5090_SYNTHETIC_GATE_BLOCKER_V1.md)，[双轨V28](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V28.md)。
RTX5090与官方Qwen2.5-7B已加载；SYN-3期望SUPPORT、实得CONTRADICT。D1未跑，指标未测量。权重和标签不在Git。

**当前分工：** [D2/D3数据标注新对话交接](PAPER1_CORE144_D2_D3_DATA_THREAD_HANDOFF_V1.md)，[双轨V27](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V27.md)。
Owner将新开本机项目Codex对话接数据，原对话继续实验；D2待两个HN定向复审，D3两S3问题仍待Owner，不自动发Human/GT。

**历史：5090交接包：** [合同、命令和粘贴指令](vace_lite/L0_5090_CURSOR_EXECUTION_PACKAGE_V1.md)，
[状态V26](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V26.md)。这是执行前快照。真实5090结果是上方V28合成门硬停。

**历史：5060设备门：** [硬件预检及恢复条件](vace_lite/VACE_L0_HARDWARE_PREFLIGHT_BLOCKER_V1.md)，
[状态V25](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V25.md)。仅说明当时5060不是5090，不覆盖5090本次运行。

**当前VACE-F5实测完成（2026-10-28）：** [报告](vace_lite/VACE_V03_IMPLEMENTATION_AND_TEST_RECORD.md)，
[路由证书](vace_lite/VACE_V03_D1_ROUTE_AND_PROOF_AUDIT.md)，[基线对比](vace_lite/VACE_V03_VS_BASELINES_COMPARISON.md)，
[下一研究决策](vace_lite/VACE_V03_NEXT_RESEARCH_DECISION.md)，[状态V24](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V24.md)。
同40组120条：两条件均总Recall15%，HN-FPR0但95%弃权；当前规则方法未达实用覆盖。
完成D1开发评分后STOP Owner审阅；D1原数据/人工/Guide及D2D3保持，正式GT/split未执行。
下方只设计/未批准实现为旧快照，不覆盖最新PODR-149。

**当前V0.3只设计（2026-10-28）：** [Owner包](vace_lite/VACE_V03_OWNER_REVIEW_PACKET.md)，
[完整路由](vace_lite/VACE_LITE_V03_ADAPTIVE_METHOD_SPEC.md)，[V02/V03比较](vace_lite/VACE_V02_V03_COMPARISON.md)，
[消融/评价](vace_lite/VACE_V03_ABLATION_AND_EVALUATION_PLAN.md)，[状态V23](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V23.md)。
无新预测、训练、GT/Evidence/正式合同或D2D3变化；停VACE_LITE_V03_OWNER_REVIEW_REQUIRED，旧V0.2/A0均保留。

**当前VACE-Lite R1（2026-10-28）：** [A0同120条诊断与候选方法](PAPER1_VACE_LITE_R1_RECORD_V1.md)，
[V0.2规格](vace_lite/VACE_LITE_V02_METHOD_SPEC.md)，[L0/评价计划](vace_lite/VACE_LITE_BASELINE_AND_EVALUATION_PLAN.md)，
[状态V22](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V22.md)。原三式S1=12/12、总16/40、HN-FP3/40；
只证明当前模板风险，不是VACE能力。无训练/改数据/Guide/GT/D2D3/正式切分，停V0.2 Owner审阅。

**当前D1（2026-10-28）：** [首轮真实开发检测结果](PAPER1_D1_FIRST_DETECTION_RESULTS_RECORD_V1.md)，
[状态V21](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V21.md)，[冻结协议](PAPER1_D1_FIRST_DETECTION_PROTOCOL_V1.md)。
Owner真签40/120、8/24 HOLD；A/B1/B2/C各13-fold120新OOF。主B1总Recall50%、HN-FPR37.5%、AUROC0.5306，
不支持当前多视角有效性/正式泛化主张；同列Oracle诊断与失败/不确定性均保留。
旧126未用；D1_DEV_EXPOSED，D2/D3/正式GT/切分不变；完成收口后STOP。下方V19等为历史。

**当前D1（2026-10-27）：** [55建议核验、40组待签表及SEPT物化](PAPER1_D1_QUALITY_AND_SEPT_MATERIALIZATION_RECORD_V1.md)，
[状态V19](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V19.md)。
40组120条建议准入、8组24条HOLD；有效评价0/0，不要求54条全重标。
B/C各144×21已物化但无分类器拟合；Oracle家族折三T训练列全空还须单独决定。
下一步Owner签署质量资格，不是自动启动实验。D2/D3原门及正式GT/划分不变。
下方V18“D1未物化”是历史，旧126隔离分数未复用。

**当前D1探索（2026-10-27）：** [可评估性NOT_EVALUABLE及五份私有产物入口](PAPER1_D1_EXPLORATORY_DETECTION_CLOSEOUT_RECORD_V1.md)。
原件已导入、QA非GT；126条预备OOF因新增质量漏项隔离，未计算性能。
8组24条HOLD，40组120条只是待审上限，实际有效评价0/0，检出率/误报未知。
D1_DEV_EXPOSED，非未来untouched test；[状态V18](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V18.md)
保留D2两题复审和D3原门。Core正式GT/划分未做，无D2/D3数据修改，等Owner质量决定。

**当前D2（2026-10-16）：** [37建议独立处置、两条原HN合同缺陷最小修复](PAPER1_CORE144_D2_OWNER_QA_AND_TWO_HN_REPAIR_RECORD_V1.md)。
只需原D2两会话各做新两条Phase1/2；Phase2暂扣，全144尚未最终验收，不生成可发Human Excel。
[状态V17](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V17.md)保留D1 Owner仲裁等待及D3两S3门。
原题/raw/Guide/Evidence保留，QA不是GT；旧D2未接受37建议的段落是本轮之前历史。

**Current D1 bounded54 (2026-10-16):** [54 reviewed; Owner workbook and Chinese packet ready](PAPER1_CORE144_D1_BOUNDED54_REVIEW_AND_OWNER_PREP_RECORD_V1.md).
34 cases/47 author proposals,57 blank final-field items; two issued-evidence gaps
and two institutional-role scope cases need Owner. Originals/Guide/evidence unchanged,
no effective values/GT or D2/D3 advance. [State V16](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V16.md).
Earlier pending bounded-review approval is historical, not final adjudication permission.

**Current D1 Human A/B comparison (2026-10-16):** [Exact123-cell Owner exception
accepted;144 pairs compared](PAPER1_CORE144_D1_HUMAN_AB_COMPARISON_RECORD_V1.md). Semantic964/1008,31 rows/44 cells;
21 process-only,54 deduplicated review leads (not54 proven defects). Originals/
old literal-parity fact/old50-file index unchanged; no correction/GT. [State V15](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V15.md)
holds next bounded54 Owner triage, retains D2/D3 gates. Older presentation-pending
entries are history within this scope, not a remaining123-cell blocker.

**Current D1 Human Phase2 (2026-10-16):** [Both originals locked; own144 identity/
1152 enums/reasons legal](PAPER1_CORE144_D1_HUMAN_PHASE2_RAW_LOCK_AND_RECEIPT_GATE_V1.md). A01 fixed123 boundary-whitespace-only cells,
zero substantive change; B01 only315 blank-storage differences. A01 exact readonly
gate held,Owner exception pending,no A/B comparison/GT. [State V14](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V14.md)
retains D2 source/scope and D3 S3 gates. OWNER_ATTESTED,not machine proof; no workbook/
Guide/Candidate/Expected changes,split/model. Older D1 waiting-return text is history.

**Current targeted6 returns (2026-10-16):** [Both originals locked and validated](PAPER1_CORE144_D2_TARGETED6_PHASE2_RAW_LOCK_AND_QA_GATE_V1.md),6 own IDs/order/11 fields/48 enums each. Five semantic rows/nine cells, one process-only; restored facts/fine reasons resolved, three covered version execution differences. Carrier/services need Owner bounded disposition; prior37 proposals not accepted, no effective annotation. [State V13](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V13.md) holds Human D2/D3 and preserves D1/D3 gates. No Candidate/source/Guide repair, Expected/GT/hidden roles/split/model; HUMAN_DECISION_REQUIRED. Below is history, not current waiting-for-six instruction.

**Current D2 V3 bounded review (2026-10-15):** [Two full-article repairs and43 author reviews](PAPER1_CORE144_D2_PHASE2_EXCERPT_V3_BOUNDED43_REVIEW_RECORD_V1.md) complete;144 own records/25 sources/old74+18 files unchanged.37 local proposals are not Owner final adjudication,6 original-session rereviews pending. [Exact seven-file handoffs](PAPER1_CORE144_D2_TARGETED6_PHASE2_V3_OWNER_SEND_CHECKLIST_V1.md) for original D2 GPT/R4_CODEX Doubao only; no rerun144 or private proposals shared. [State V12](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V12.md): D2 machine/Human unaccepted, D1/D3 unchanged, no Expected/GT/split/model. STOP_EXTERNAL_REVIEW_REQUIRED. Older pending-repair entries below are history.

**Current D2 Phase2 returns (2026-10-15):** [Two originals byte-locked](PAPER1_CORE144_D2_PHASE2_RAW_LOCK_AND_COMPARISON_RECORD_V1.md),144 each/own order/eleven fields/enums/reasons PASS.42 semantic rows plus15 process-only differences;43-case semantic/quality union, not43 proven defects. Two V2 clause omissions directly verified against original frozen full texts; additive correction, no old package/raw rewrite. [Owner bounded repair/triage decision](PAPER1_CORE144_D2_PHASE2_EVIDENCE_AND_REVIEW_BLOCKER_V1.md) pending; no V3 execution or Human D2 authorization. [State V11](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V11.md) retains D1 Human gates/D3 two blockers. OWNER_ATTESTED/R4 actual Doubao. No Expected/GT/split/model; old ready-to-send entries below are history.

**Current Phase2 preparation (2026-10-07):** [Final144 replay and source preflight](PAPER1_CORE144_D2_D3_PHASE2_PREFLIGHT_AND_RELEASE_RECORD_V1.md) retain own Phase1 QA views/8 and18 minor variances, used source hashes25/24 and repair drift0. D2 Owner-approved literal complete-article excerpts remain144; two V2 seven-file folders ready, not distributed. [Exact addresses](PAPER1_CORE144_D2_D3_PHASE2_OWNER_SEND_CHECKLIST_V1.md), original D2 sessions only (R4=Doubao), actual platform capacity unverified; incident STOP on incomplete handling, no96+48. D3 two S3 single-source counterexamples hold Phase2 despite hash PASS; [twelve-field Owner decision](PAPER1_CORE144_D3_PHASE2_S3_NECESSITY_BLOCKER_V1.md), no crop/patch executed. [State V10](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V10.md) leaves D1 Human gates unchanged. No Human D2D3, Expected/GT, split/model/R5; below is history.

**Latest D1 Human gate (2026-10-06):** B01's own Phase1 original is
[byte-locked and valid](PAPER1_CORE144_D1_HUMAN_B01_PHASE1_RAW_LOCK_AND_PHASE2_RELEASE_V1.md),
144/144 B01 IDs/order/text,720 legal enums,16/16 required notes. B01-only
Phase2 release is authorized under the existing individual gate. [Send exactly
two B01 files](PAPER1_CORE144_D1_HUMAN_B01_PHASE2_OWNER_SEND_CHECKLIST_V1.md):
unchanged Excel and detailed Chinese guide. Actual delivery is not observed;
no A/B comparison/GT. [Current state V9](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V9.md)
preserves A01 authorization and D2/D3 Phase2 withheld. Older B01-pending entries
below are history, not the current B01 gate.

**Current V2 rereview closeout (2026-10-06):** Four originals3/1 locked and
strictly validated; five categorical fields100%, four material text-visible
items resolved for Phase1 quality QA. [Raw-lock and QA record](PAPER1_CORE144_D2_D3_BOUNDED4_PHASE1_V2_RAW_LOCK_AND_QA_RECORD_V1.md),
[state V8](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V8.md). Current144 reviewer
views retain eight/eighteen prior nonblocking naturalness variances, no vote.
OWNER_ATTESTED only, R4 actual Doubao. Phase1 quality PASS is not Owner dataset
acceptance or GT; both Phase2 unprepared/withheld pending Owner preparation
approval. D1 unchanged; no Human D2/D3, Expected/GT, split or training. Below history.

**Current bounded repair (2026-10-05):** Owner approves only D2 three/D3 one.
[Minimal repair and handoff](PAPER1_CORE144_D2_D3_BOUNDED4_REPAIR_RECORD_V1.md)
and [state V7](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V7.md): four new V4 IDs,
old raw preserved, facts/paths unchanged. Four3/1 targeted Phase1 V2 folders
ready for original domain sessions only; no new/mixed sessions. R4 provider Doubao.
Four returns pending; Phase1 unaccepted / Phase2 withheld. D1 unchanged;
no Human D2/D3, Expected/GT, R5, split or training. Older entries below historical.


**Current (2026-10-05):** Four [targeted Phase1 returns locked](PAPER1_CORE144_D2_D3_TARGETED_PHASE1_LOCK_AND_GATE_V1.md),
D2 25 each/D3 32 each, strict checks PASS; original sessions OWNER_ATTESTED.
Seven new minor-naturalness variances nonblocking. D2 three referent/surface items
and D3 one logical-scope blocker keep both Phase2 withheld; Owner four-item
repair/disposition pending. Current144 views are provisional, not final or GT.
[State V6](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V6.md). No new repair, Human
D2/D3, Expected, GT, split or training; D1 unchanged. Below is history.

**Current targeted checkpoint (2026-10-03):** [Owner triage and additive repair](PAPER1_CORE144_D2_D3_PHASE1_OWNER_TRIAGE_RECORD_V1.md)
and [parallel state V5](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V5.md) supersede
only the pending-triage next action below. Original 62 cases: 43 repairs / 19
nonblocking naturalness; full-domain audit adds 14 separate repairs. Send only
changed new-ID texts: D2 25, D3 32, to each domain's original R3 GPT / R4_CODEX
Doubao sessions. Both Phase2 held pending four targeted returns/byte-lock/gates.
Private current distribution: output_v3 under the triage-repair namespace; exact
Owner checklist is in its handoff root. Earlier drafts and Owner/control-plane
materials must not be sent. No final annotation overlay, Human D2/D3, GT, split or
training; D1 Human gates stay independent. Author QA is not blind acceptance.


**Latest external checkpoint (2026-10-03):** Four D2/D3 R3-GPT and
R4_CODEX/Doubao Phase1 originals are [locked and structurally valid](PAPER1_CORE144_D2_D3_PHASE1_RAW_LOCK_AND_GATE_V1.md).
D2 has 22 disagreement rows/26 cells; D3 has 30/34, plus shared quality flags.
Both Phase2 gates remain withheld. [Parallel state V4](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V4.md)
retains the independent D1 Human gates. Private Owner packet: 29+33 cases;
contains existing answers: do not give it to blind reviewers. No candidate/
protocol rewrite, Core GT, split or training. Earlier unsent entries are history.

**Latest D1 Human checkpoint (2026-10-02):** Owner identified the `(2)`
workbook as the actual HUMAN-A01 Phase1 return. It is now
[byte-locked and validated](PAPER1_CORE144_D1_HUMAN_A01_PHASE1_RAW_LOCK_AND_PHASE2_RELEASE_V1.md):
144/144 A01 rows and exact ID/order/Candidate parity; legal enums; all 15
required notes present. The matching A01 Phase2 workbook is authorized for
Owner distribution only through the [exact one-file checklist](PAPER1_CORE144_D1_HUMAN_A01_PHASE2_OWNER_SEND_CHECKLIST_V1.md).
B01 is independently completing the correct B01 Phase1 workbook; B01 Phase2
remains withheld. No A/B comparison, adjudication or GT exists. See the
[current parallel state V3](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V3.md).
Earlier Human-lane statements below are dated history.

**Latest checkpoint (2026-10-02):** D2 Finance and D3 Information Security
each have 48 groups / 144 candidates and have passed bounded, source-bound
**internal construction-author QA**. See the [two-domain summary](PAPER1_CORE144_D2_D3_CONSTRUCTION_SUMMARY_V1.md),
[current parallel-lane state](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V2.md),
and [exact Owner Phase1 reviewer send checklist](PAPER1_CORE144_D2_D3_PHASE1_REVIEWER_SEND_CHECKLIST_V1.md).
Four 144-row R3/R4 candidate-only Phase1 packets are prepared but unsent;
the private packet bytes live in the local ignored `experiments/` namespace.
Independent blind review, Human D1 status beyond the last Owner record,
Core GT, split and training are not inferred from this checkpoint. The dated
entries below are preserved history.

**Latest construction checkpoint (2026-09-30):** [D2 Finance internal QA and private artifact index](PAPER1_CORE144_D2_FINANCE_INTERNAL_CONSTRUCTION_RECORD_V1.md) records 48 groups/144 candidates and two *prepared, unsent* 144-row Phase1 packets. This is construction-author QA, not R3/R4 or Human acceptance. D3 evidence-first construction follows under the same Owner approval; no combined external release, GT, split or training. Earlier status paragraphs below are dated history.

**Latest clarification (2026-09-28):** [Master Guide](PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md) now separates object-information supply and competing referents, with a 2×2 table/four additional fictional cases. All original30, including05/06, are preserved; total34 cases. [Additive QA/closeout](PAPER1_CORE144_SELF_CONTAINMENT_REFERENT_CLARIFICATION_RECORD_V1.md). Enums/schema/four XLSX/Candidate/ID/order/Phase2/raw unchanged; Human A/B not distributed, Phase2 sealed. Owner reviews updated Markdown next; the existing PDF is untouched and not parity-certified. Earlier same-day counts below are history.

**Current (2026-09-28):** [中文真人主标注手册 V1](PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md) expands the actual current workbook fields and frozen V4–V4.3 with 30 fictional cases. [Read-only schema/parity and closeout](PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_QA_RECORD_V1.md). Four XLSX, Candidate/ID/order and semantics are unchanged; Human A/B not yet distributed; Phase2 sealed. Owner reviews the guide next, then decides any future Excel explanation sync/distribution. This documentation task does not run D2/D3 construction, annotation, GT, split or training. Below are dated earlier statuses.

**Current (2026-09-27):** [D1 Full144 preannotation acceptance](PAPER1_CORE144_D1_PREANNOTATION_ACCEPTANCE_RECORD_V1.md) passes. The [A/B Human Phase1 V1 workbooks](PAPER1_CORE144_D1_HUMAN_PHASE1_GUIDE_V1.md) are distribution-ready but not sent, with Phase2 V1 separately sealed. [Usability and leakage QA](PAPER1_CORE144_D1_HUMAN_XLSX_USABILITY_AUDIT_V1.md). [Parallel D1 Human and D2/D3 construction lanes](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V1.md) are open; D2/D3 have [slot preflight only](PAPER1_CORE144_D2_D3_CONSTRUCTION_LANE_PREFLIGHT_V1.md), no new Candidates. No Core GT, split or training. Older pending-Phase2 paragraphs below are historical.

Current D1 remaining90: Owner-attested targeted R3/R4 same-session provenance and the bounded two-group frozen-Evidence projection permit one 90-row Phase2 V5 external handoff. Send only the [reviewer-specific exact files](../formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE2_OWNER_SEND_CHECKLIST_V5.md) to the original conversations. External returns and D1 Full48 preannotation acceptance are still pending; no Human A/B, D2/D3 construction, GT, split or training. The prior held-state paragraph below is historical.

Current D1 remaining90: both targeted-four Phase1 raw files are immutable/structurally valid, but Phase2 distribution is held pending a bounded E1/E2 evidence-presentation decision for two original three-snapshot groups and targeted-session isolation confirmation. [Exact gate](../formal240/PAPER1_FORMAL_D1_REMAINING90_TARGETED4_PHASE1_LOCK_AND_GATE_V1.md). Core144 remains D1/D2/D3; no Human A/B, D2/D3 construction, GT, split or detector training has begun.

- [Owner scope decision](PAPER1_CORE144_SCOPE_DECISION_V1.md): current D1/D2/D3 core, historical Formal240 preserved, D4/D5 deferred.
- [Exact frozen-matrix subset](PAPER1_CORE144_GROUP_MATRIX_VIEW_V1.jsonl) and [selection manifest](PAPER1_CORE144_DOMAIN_SELECTION_V1.json).
- [Benchmark contract](PAPER1_CORE144_BENCHMARK_CONTRACT_V1.md) and [domain-pipelined plan](PAPER1_CORE144_PARALLEL_EXECUTION_PLAN_V1.md).

The current D1 remaining90 Phase1 gate is [documented in Formal240](../formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE1_FINAL_GATE_V1.md). These scope documents do not authorize split, Ground Truth or detector training.
