# Paper 1 Document Detector Feature Set V1

Status: `FROZEN_BEFORE_MODEL_FIT / NON_ORACLE / NO_TRAINING`。

主设置：`Q_NO_TITLE + HYBRID + Top5 + Trusted Version Registry V2`。仅 S/E/P/T，共 23 features：Semantic 3、Entity-Claim 9、Provenance 8、Temporal-Version 3。R 属于 Stage B retrieval exposure risk，不进入本 Feature Set。

所有 feature 必须保留 applicability 语义；`NOT_APPLICABLE`、`INPUT_MISSING`、`EVIDENCE_INSUFFICIENT` 不得合并。Raw matrix 只保存值，availability 单独审计；缺失值保持 null，在未来 development protocol 冻结前不得插补或作为 Poison shortcut。

Oracle exclusion：`current_history_binding_conflict`、`effective_interval_conflict`、`successor_exists`、`superseded_version`、`version_distance`、`version_mismatch`。理由：`NO LEGITIMATE INFERENCE PATH`。

Canonical machine-readable contract：Git-external `features/PAPER1_DOCUMENT_DETECTOR_FEATURE_SET_V1.json`。
