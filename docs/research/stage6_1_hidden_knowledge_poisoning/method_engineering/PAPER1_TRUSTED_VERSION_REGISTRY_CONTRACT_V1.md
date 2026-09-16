# Paper 1 Trusted Version Registry Contract V1

Status: `CONTRACT_FROZEN / REGISTRY_DATA_NOT_YET_BUILT`

Trusted Version Registry 是 inference-time 可信基础设施，不是 Ground Truth。每条记录允许包含：

- stable `document_id`、`version_id` 与 `CURRENT/HISTORICAL` role；
- publication date、`effective_from`、`effective_to`；
- predecessor、successor、superseded-by relation；
- issuer、adopting authority、amending authority；
- official URL 与 frozen trusted document SHA256。

不得包含 Poison/Clean/HN、HKP、S1/S2/S3、Expected、Owner adjudication、GT value 或任何等价标签。Registry 的版本角色
必须由官方版本链和有效区间支持，不能从 Hard Negative 身份反推。

当前 Final72 没有满足该合同的独立 registry。因此 `historical_docs_at_k`、`current_docs_at_k`、dominance、rank/score
gap、`current_missing_topk` 与 `version_diversity` 全部 fail closed 为 `INPUT_MISSING`。本轮没有用 GT 补齐，也没有静默
加入新外部 Evidence。
