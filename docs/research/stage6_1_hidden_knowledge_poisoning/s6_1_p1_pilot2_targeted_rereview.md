# S6.1-P1-PILOT2-TARGETED-REREVIEW

## 1. 任务与边界

- 任务：`Pilot2 Annotator-Friendly Targeted Re-review Kit`。
- 执行机器：本机。
- Owner authority：`PODR-065 / OR-027`。
- Base commit：`09aa7e65e95e10a657e44c2b31e23ec02bc4210b`。
- 状态：`TARGETED_REREVIEW_KIT = READY_FOR_HUMAN_EXECUTION`。
- 本任务不修改 Round1 raw、原 preflight/registration/owner correction、完整 V2 包或 Schema V2；不执行 agreement、
  disagreement、adjudication、Dataset freeze、Detector、Training、5090 或 Formal Experiment。

## 2. Targeted Field Audit

### Phase1 — A/B 各 36 行

`locally_detectable`、`cross_document_evidence_needed` 与 `assigned_stealth_level` 必须复核。三者存在明显 V1
解释不稳定，且 stealth level 依赖前两项。自然度、主题相关度与 confidence 定义未变，也不是本轮 Ground Truth
修复的上游字段，保持本人 V1 只读。

### Phase2 — A/B 各 36 行

必须复核 `version_relation_present/correct`、`history_or_update_claim_present/legitimate_update_or_history`、
`authority_claim_present/matches` 与 `overall_fact_status`。前三组修复 V1 缺少 applicability 和 NOT_APPLICABLE 的结构
问题；overall 在上游修复后重新走决策树。

`claim_matches_source` 与 `fact_changed` V1 都为 `34/36` exact、provisional kappa `0.8859`，且 V2 定义未改变，保持
只读。完整字段决策与证据见 Git-external `owner_only/targeted_field_audit.json`。

## 3. Process-only fixes 与工作量

- A：10 个实质字段，`360` 个样本×字段任务；另填 Phase1/Phase2 各一次回溯声明。
- B：同样 `360` 个实质任务；只补 `21` 个 `professional_lookup_used` 缺失项，并修正 `1` 条 Google Search 来源
  类型，共 `382` 个任务；另填两份一次性声明。
- 全量 V2 实质字段为 `16 × 36 = 576` 个任务；每人减少 `216` 个实质任务，即 `37.5%`。
- B Phase1 的 36 个历史 `time_seconds` 维持 `MISSING_NOT_RECOVERABLE`，不得凭记忆补造；只记录本轮
  `rereview_time_seconds`。

## 4. Annotator-friendly package

Git-external 目录：`LLMGuard-Handoff/paper1_pilot2_targeted_rereview_20260827`。A/B 各自 Phase1/Phase2 一个主 XLSX
与机器交换 CSV；工作簿均含《先看这里》《需要你复核》《原结果只读》《回溯声明》。首页冻结四值语义、三个示例、
S1/S2/S3 与 overall fact 决策树；任务表使用下拉、黄色编辑区、灰色只读区、stop-style 输入拦截、自动
KEEP/REVISE 与 applicability 联动提示。

四个 XLSX SHA256：

| Workbook | SHA256 |
| --- | --- |
| A Phase1 | `f2bd1370f6bcf085677ac3c01e77072629a4dcf37fa72433beb70c62267bd8b2` |
| A Phase2 | `d5762525cea6327f7c9f965f7921d634cf49c2690365b3d49d9b5b8cbf32e525` |
| B Phase1 | `e0552955167ff03ae99fce6f7b0427e098e66abf98fb70021227638f23e8cd9c` |
| B Phase2 | `dc0f9ffc818c1b1ef2ef5484f88a3079755e1cae18223820a9646ebf6ef0026e` |

## 5. Validation 与下一门

Raw `4/4` SHA unchanged；完整 V2 tree `32/32` files unchanged；targeted root 独立；A/B own-V1-only；无 peer、
agreement/disagreement marker、candidate intent 或 evaluator label 泄漏；5 个 CSV 为 UTF-8 BOM；XLSX 4/4、16 sheets
render/inspect、dropdown、formula、只读拦截和 dependency 规则通过；staging 到 E 盘 `17/17` SHA 一致。

严格发放顺序：分别发 A/B targeted Phase1；回收并锁定双方 Phase1 后才分别发 Phase2；锁定四份 targeted return 后
停止。后续固定门为 `RETURN_VALIDATION -> FORMAL_AGREEMENT_ANALYSIS -> 必要 disagreement owner adjudication ->
GROUND_TRUTH_CANDIDATE_LOCK`，但每一步均需独立批准。`POST_ANNOTATION_EXPERIMENT =
WAITING_FOR_HUMAN_ANNOTATION_CLOSURE`；Auto Continue = `NO`。
