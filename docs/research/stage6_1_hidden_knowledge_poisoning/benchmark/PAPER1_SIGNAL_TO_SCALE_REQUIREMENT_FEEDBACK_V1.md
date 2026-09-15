# Paper 1 Signal-to-Scale Requirement Feedback V1

Status: `FINAL72_FEASIBILITY_FEEDBACK / FUTURE_SCALE_INPUT_REQUIREMENT`

## 目的

Final72 五视角运行证明，仅保留 Candidate 文本和最终标签不足以支持完整检测链。未来 240-group / 约 720 Candidate
在生成前必须把下列 feature-plane metadata 纳入版本化 schema，避免数据完成后再反向补字段。

## 每个 Candidate 必须保留

- 稳定 `sample_id`、`candidate_text`、`source_title`、唯一 `primary_subject` 和结构化 claim spans；
- subject、predicate、object/value、unit、time_scope、condition、exception、authority 的可审计解析结果；
- 文本、解析器、规则、模型及 prompt（若使用）的版本、hash、determinism 信息；
- Candidate feature-plane 元数据与 evaluator-only class/HKP/S/group label 物理分离。

## 每条 Version Chain 必须保留

- 稳定 chain/version/document ID、predecessor、successor、`effective_from`、`effective_to`、repeal/replacement relation；
- 明确的 `CURRENT` / `HISTORICAL` role、evaluation `as_of` 时间和 role 证据来源；
- Clean、Poison、Hard Negative 同一 chain 不得跨 train/dev/test 的 group-aware split key。

## 每个 Evidence 单元必须保留

- Evidence ID、官方标题、完整 URL、冻结 snapshot、content hash、retrieval timestamp 和验证状态；
- Evidence 所属 document/version ID，以及它支持的 claim span，但不得编码 Candidate class；
- `host`、page publisher、issuing/adopting/amending authority、official repost institution 的独立字段；
- Evidence 缺失/不足的原因，不得把缺失本身当作安全值或预测捷径。

## Query 与 Retrieval 必须保留

- 真实、标签无关且在运行前冻结的 query/query_id；禁止从 Poison label 反向构造；
- corpus snapshot、chunking、embedding、retriever、Top-K、score semantics、seed 与 config hash；
- 每次 top-k 的 rank、score、document/version identity，以及至少两次可比 trace 支持 ranking stability；
- raw retrieval trace 必须在加载 class/HKP/S label 前锁定。

## Final72 暴露出的具体缺口

- 10 个 Retrieval signals、共 720 instances 因无冻结 query/retrieval trace 而不可计算；
- publisher/issuer、host/publisher 与部分 repost role 尚未结构化；
- current/historical role 目前依赖低置信 deterministic year proxy，应在 scale schema 中改为显式元数据；
- Present-Time Substitution 仅 7/72 可计算，需显式 historical/current fact binding 与有效区间；
- MLM/PPL 需要另行冻结 checkpoint、tokenizer、revision、mask policy、device 和 determinism contract。

## 边界

本反馈只约束未来 scale 数据的可检测性与可复现性，不授权生成 240 groups、冻结 Formal Dataset、训练 Detector 或
运行正式测试。
