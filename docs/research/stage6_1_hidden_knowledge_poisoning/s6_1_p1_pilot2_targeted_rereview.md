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

## 6. Correction 01 — V1 列名映射与最终三表（2026-08-28）

项目需求提出人报告 A Phase1 已完成。本机观测到该文件为 `33057` bytes，SHA256
`100cffe2b81a23f3a65ade5ba712cd7aeefcfc56c600dae68f2b0241af36737f`；它未被重新生成、复制进更正包或覆盖，当前仍是
`OWNER_REPORTED_COMPLETED / PENDING_RETURN_VALIDATION_AND_FORMAL_LOCK`。

B Phase1 的三个旧值列在 raw/full-V2 中并未缺失；它们的历史列名带有中文后缀，而旧生成器只用精确英文列名查找，
因此错误地将 `108/108` 个任务显示为 `[V1_ABSENT]`。B Phase2 的 `version_relation_correct`、
`authority_matches` 也有同类列名后缀；A Phase2 无同类映射缺陷。此问题是生成器/测试缺陷，不是 B 的历史标注缺失。

修复后，B Phase1 的 `[V1_ABSENT]` 为 `0`；B Phase2 与 A Phase2 只有三个 V1 中真正不存在的新增
`version_relation_present / history_or_update_claim_present / authority_claim_present` 保留该标记。生成器现在只接受白名单
历史 alias；其他非预期缺失或 alias 冲突会立即 fail closed。首页同时冻结 owner 解释：`version_context` 为已知正确的
参考证据；只有事实冲突才评 S1/S2/S3；一个直接官方来源是 S2 且不算 cross-document；S3 需要多证据链联合推理。

Git-external 更正交付键为 `LLMGuard-Handoff/paper1_pilot2_targeted_rereview_correction01_20260828`，只含待填的 A Phase2、B Phase1、
B Phase2 三份 XLSX/CSV、coordinator 说明和 owner-only manifest。三份表完成 `12/12` sheets 视觉复核、公式错误扫描、
下拉/只读保护、UTF-8 BOM、映射分布和门控回归；staging 到 E 盘 `8/8` 文件 SHA 一致。三份 XLSX SHA256 为 A Phase2
`5cfbb13fe8874aa1da06e30f3f37300402290f781b82b805468104b9a58e51c7`、B Phase1
`15f7f49b62f7c2b33ad6d57701d2b82e84d64090055ef20258321b8b097ba3d5`、B Phase2
`461e8b5ce10113d72bd0f2d331227a53240ee28ab23efc3c8d86d02c289b1eb2`。这是最终三表人工轮的准备，不是 agreement、Ground Truth 或正式实验结果。

固定后续路由为：三份独立 return → return validation/hash lock → owner 批准 agreement → 仅必要分歧仲裁 → Ground Truth candidate
验收 → 另行批准标注后实验准备。项目需求提出人将本轮结果指定为高优先级/高权重有效性证据候选，并要求不再进行无条件全量重复标注；这不跳过上述门。Auto Continue = `NO`。
