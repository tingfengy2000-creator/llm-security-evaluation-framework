# Paper 1 240-Group Scale Readiness Spec V1

Status = `PREPARED / DATA_NOT_GENERATED / DATASET_NOT_FROZEN`

## 目标结构

`5 domains × 4 HKP × 3 stealth levels × 4 independent version chains = 240 independent groups`

若每组包含 Clean / Poison / matched Hard Negative，预计约 720 candidates；本任务没有生成这些数据。

## Scale readiness gate

正式生成前必须冻结：

- 五领域 source/license/snapshot/provenance；
- version-chain identity、effective/repeal/supersede relations；
- Candidate 最低自包含性与主体唯一识别；
- Clean/Poison/Hard Negative 同链匹配规则；
- HKP1–4 与 S1–3 coverage；
- 独立人工标注、Owner adjudication、Evidence sufficiency 与 immutable raw policy；
- dedup/near-duplicate/template/entity/source/time leakage scan；
- public/private artifact boundary；
- frozen query/retriever/embedding/config identity。

## Hard leakage gate

未来 split 必须 `VERSION_CHAIN_GROUP_AWARE`：同一 version chain 的 Clean、Poison、Hard Negative 必须整体进入同一个
train、dev 或 untouched test partition。禁止同链跨 split；同源近重复、同模板和同实体链泄漏还需独立扫描。

Final72 已参与协议校准、人工仲裁和研究者 QC，只能作为 development/method-engineering set，不能进入未来 untouched
final test population。
