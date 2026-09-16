# Paper 1 Five-View Signal Contract V1

> 2026-09-16 boundary addendum: S/E/P/T primarily support offline document-level poison risk. R is query-conditioned and
> primarily supports retrieval exposure risk. A legal historical Hard Negative may have high R exposure under a current-state query
> without becoming a Poison document. Matched E1/E2 signals remain diagnostic-only until an independent trusted retriever or version
> registry supplies their inference-time inputs. See [Two-stage Risk Architecture V1](PAPER1_TWO_STAGE_RISK_ARCHITECTURE_V1.md).

Status = `OWNER_FROZEN_METHOD_ENGINEERING_CONTRACT`
Execution = `FINAL72_DEVELOPMENT_SET_FEASIBILITY_RUN_COMPLETE`
Formal result = `NONE`

## 1. 方法位置

Paper 1 方法链固定为：

`Benchmark → Signals → Detection → Risk Score → Explanation → Retrieval Detoxification`

Signal 是可观察证据，不是标签，也不是最终判断。Detection 才使用多个 Signal 形成风险判定。任何 Ground Truth、
poison label、attack ID、HKP 或 stealth label 均不得成为 inference feature。Final72 只能作为
`DEVELOPMENT_AND_METHOD_ENGINEERING_SET`，不得称为 untouched final test。

## 2. 通用 Signal 结构

每个 signal 的机器合同必须包含：`signal_name`、`view`、`definition`、`input_fields`、`output_type`、`value_range`、
`applicability`、`missing_value_semantics`、`evidence_dependency`、`candidate_dependency`、`query_dependency`、
`version_chain_dependency`、`expected_attack_relevance`、`explanation_role`。

每次观测必须表示为：

`SignalObservation = (value, applicable, confidence, evidence_quality, missing_reason, evidence_references)`

- `applicable=false`（canonical state：`NOT_APPLICABLE`）时 `value` 必须为 `null`，不得填 `0`、`SAFE` 或低风险。
- `confidence` 与 `evidence_quality` 分开记录，范围均为 `[0,1]`；缺失时允许为 `null`。
- `missing`、`not applicable` 和真实零值是三种不同状态。
- Evidence 不足不得通过读取 Ground Truth 补齐。
- 每个 signal 在 label load 前冻结 `HIGHER_IS_RISKIER`、`LOWER_IS_RISKIER`、`NON_MONOTONIC` 或 `UNDEFINED`
  orientation；分析阶段不得为提高 AUROC 临时翻转。

本次执行没有改变 42 项 signal 的科学定义。它仅补充计算状态、预声明 orientation 和可复现的 deterministic-rule
extractor；无法满足输入合同的 signal 保持 `null` 并明确写入 `INPUT_MISSING`、`MODEL_UNAVAILABLE` 或
`NOT_APPLICABLE`。

机器级完整定义见 `method_engineering/registry.py`；以下为人类可读冻结摘要。

## 3. Semantic View（S）

| signal | 定义 | 主要依赖 | 适用/缺失边界 | 解释作用 |
| --- | --- | --- | --- | --- |
| `mlm_masked_token_naturalness` | masked-token 合理性 | candidate text + frozen MLM | 模型不可复现时缺失，不等于低风险 | 局部词法异常 |
| `ppl_naturalness` | 归一化 PPL 自然度 | candidate text + frozen causal LM | 模型/revision 缺失即不可用 | 语言流畅性异常 |
| `current_version_semantic_similarity` | 与 current Evidence 的最大相似度 | current Evidence | 无 current Evidence 时 N/A | 当前支持接近度 |
| `historical_version_semantic_similarity` | 与 historical Evidence 的最大相似度 | historical Evidence/version chain | 无历史版本时 N/A | 历史支持接近度 |
| `top_k_semantic_similarity` | query/candidate/top-k 的语义暴露 | query + retrieval results | 无 query 或 retrieval 时缺失 | 检索语义暴露 |
| `semantic_version_margin` | `historical_similarity - current_similarity` | current + historical | 任一侧缺失则 N/A；范围 `[-1,1]` | 正值表示更接近历史版本 |

MLM/PPL 在论文中是 lexical-naturalness baseline / Semantic signal。GMTP 不进入 proposed Temporal View，而是独立外部
poisoning-defense baseline。

## 4. Entity-Claim View（E）

Claim extractor 必须先产生结构化中间表示：

`subject, predicate, object/value, unit, time_scope, condition, exception, authority`

| signal | 判断内容 | N/A 边界 | 主要攻击相关性 |
| --- | --- | --- | --- |
| `subject_match` | 主体是否一致 | 主体不能唯一恢复 | HKP1/HKP4 |
| `predicate_match` | 谓词/关系是否一致 | 谓词不可对齐 | HKP1–4 |
| `entity_conflict` | 核心实体冲突 | 无可比较实体 | HKP1/HKP4 |
| `numeric_conflict` | 数值与单位冲突 | 无可比较数值 | HKP1 |
| `date_conflict` | 同一范围内日期冲突 | 无可比较日期 | HKP1/HKP3 |
| `condition_conflict` | 适用条件冲突 | 无条件命题 | HKP2 |
| `exception_conflict` | 例外被改变或遗漏 | 例外不适用/无证据 | HKP2 |
| `negation_flip` | 肯定/否定极性翻转 | 命题不可对齐 | HKP1/HKP2 |
| `relation_conflict` | subject-predicate-object 冲突 | 关系元组不可对齐 | HKP1–4 |

## 5. Provenance View（P）

必须区分 `host`、`page publisher`、`issuing authority`、`adopting authority`、`amending authority` 和
`official repost institution`。官方转载机构不自动等于制定/修订机关。

| signal | 判断内容 | N/A 边界 |
| --- | --- | --- |
| `official_source` | 来源是否符合冻结的官方来源政策 | 来源身份缺失 |
| `host_publisher_relation` | host 与页面发布者的关系 | 任一身份缺失 |
| `publisher_issuer_match` | 发布者是否等于发布/制定机关 | 任一身份缺失 |
| `claimed_authority_match` | Candidate 声称机关是否匹配权威链 | Candidate 无 authority claim 时 N/A，不是安全零 |
| `document_identity_match` | 标题、标识符、主体是否属于同一文件 | 文件身份不可绑定 |
| `version_identity_match` | 声称版本是否匹配冻结版本 | 无版本命题时 N/A |
| `official_repost` | 是否为官方转载而非原始制定机关 | provenance chain 不足 |
| `provenance_consistency` | host/publisher/issuer/adopter/amender 的整体一致性 | 少于两个可识别角色 |

## 6. Temporal-Version View（T，核心视角）

| signal | 判断内容 | 主要 Evidence 依赖 |
| --- | --- | --- |
| `current_fact_match` | 是否符合当前有效事实 | current Evidence |
| `historical_fact_match` | 是否符合历史版本事实 | historical Evidence |
| `version_mismatch` | 声称版本与 Evidence 版本是否冲突 | version chain |
| `superseded_version` | 相关时间是否已有 successor | chain + as-of |
| `effective_interval_conflict` | 命题时间是否落在有效区间外 | effective/repeal dates |
| `current_history_binding_conflict` | 是否把历史事实错误绑定为当前事实 | current + historical chain |
| `successor_exists` | 是否存在后继版本 | version chain |
| `version_distance` | 声称版本与当前版本的距离 | version chain |
| `present_time_substitution_signal` | 历史限定成立、去掉限定作为当前命题后不成立 | historical + current Evidence |

Present-Time Substitution Signal：若历史限定命题有 Evidence 支持，但去除历史/版本限定后作为 current claim 不再成立，
则 `VERSION_SENSITIVE=true`；若 Candidate 同时声称当前适用，则 `CURRENT_VERSION_MISBINDING_RISK` 上升。语言自然度不能
替代这个推理。

## 7. Retrieval-Behavior View（R）

| signal | 定义 | 依赖 |
| --- | --- | --- |
| `retrieval_rank` | frozen query 下 Candidate rank | retrieval trace |
| `retrieval_score` | frozen retriever score | comparable score |
| `historical_docs_at_k` | top-k 历史版本数量 | trace + version metadata |
| `current_docs_at_k` | top-k 当前版本数量 | trace + version metadata |
| `historical_dominance_at_k` | version-identifiable top-k 中历史文档占比 | current/historical counts |
| `historical_current_rank_gap` | best current rank − best historical rank | 双方均召回 |
| `historical_current_score_gap` | best historical score − best current score | 双方 score 可比 |
| `current_missing_topk` | top-k 是否没有 current document | current identity |
| `version_diversity` | top-k 版本多样性 | version metadata |
| `ranking_stability` | 冻结扰动/重复条件下排名稳定性 | 至少两份可比 trace |

这些 signal 不要求 gradient，也不假设 GMTP 可直接兼容当前 retriever。

## 8. Claims boundary

本合同只冻结可实现的输入/输出和缺失语义。它不证明任何 view 可分离 Poison，不证明 Five-view 优于 Semantic-only，
不证明 Temporal/Provenance 能降低 Hard Negative FPR，也不产生风险校准或解毒结果。
