# S6.1-P1-R1 正式实验协议强化候选

Document Role = `P1_APPROVAL_GRADE_REVIEW_CANDIDATE`<br>
Authority = `NON_CANONICAL_CANDIDATE`<br>
Status = `REVIEW_CANDIDATE / NOT APPROVED / NOT STARTED`<br>
Primary Authority = [human/research_plan_authority.md](human/research_plan_authority.md)<br>
Supersedes Candidate Draft = [s6_1_p1_protocol_candidate.md](s6_1_p1_protocol_candidate.md)<br>
P1 R1 Base Commit = `aabe504d55626fb31008822b7bbabd3b32e2afd4`

> `Supersedes Candidate Draft` 只表示候选设计版本替代。旧候选作为历史保留；本文件不批准 P1 或 Pilot，不冻结或构建 Dataset，不实现 Detector、过滤或降权，不运行 baseline 或 Formal Experiment，也不产生 Paper Result。

## 1. 决策、定位与候选缺口

项目需求提出人已选择：

- `DETOXIFICATION_OPTION = OPTION_B`
- `TITLE_INTENT = CONFIRMED`
- `DETOXIFICATION_TECHNICAL_SCOPE = OPTION_B_CONFIRMED`
- 完整技术表达：`OPTION_B_DETECTION_AND_LIGHTWEIGHT_RETRIEVAL_INTERVENTION`
- `S6.1-R0-FU1-W2 = HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED`
- `S6.1-R0-FU1 = HUMAN_ACCEPTED / CLOSED`

Paper 1 候选范围包括中文版本化隐蔽知识污染 Benchmark、多视角污染检测、风险分数/视角信号/解释、检测后的轻量过滤或降权，以及检测安全性与检索效用的权衡评估。它明确不包括 trusted context package、完整上下文构造（构建）、多证据可信上下文生成、完整可信检索链、复杂端到端 Agent 防御或生产级 RAG 平台；这些边界保留给 Paper 2 或独立阶段。

前一版候选存在十五项审批缺口：RQ 未绑定可证伪假设；主要/次要终点、评估单位、Benchmark 组成、标注/复核/仲裁、HKP 构造、S1–S3 判定、Hard Negative 匹配与比例、baseline 公平性、五视角接口、Option B 数学定义、数据规模/运行矩阵/资源、统计比较族/样本量、许可发布和可直接执行的进入条件均未完全冻结。本文件逐项给出审批级候选，但保持 `NOT APPROVED / NOT STARTED`。

## 2. 研究目标与核心贡献候选

1. **Contribution 1 — Benchmark**：构建中文版本感知隐蔽知识污染 Benchmark，覆盖事实变化、条件变化、时间/版本变化和来源/权威伪装。
2. **Contribution 2 — Detection**：提出版本感知多视角污染检测方法，联合 Semantic、Entity-Claim、Provenance、Temporal-Version 与 Retrieval-Behavior 五个视角。
3. **Contribution 3 — Lightweight Detoxification**：提出风险驱动的 Hard Filtering 与 Soft Downweighting；不构建 trusted context package。
4. **Contribution 4 — Evaluation**：评估检测性能、Hard Negative 误报、跨攻击/跨领域泛化和安全—效用权衡。

## 3. Research Questions、假设与可证伪性

所有阈值只可在开发集冻结；所有比较以共享 query/group 的 paired design 为优先。`Primary Endpoint` 进入主比较族并接受 Holm correction；secondary endpoint 为解释性或支持性结果。

### RQ1：语义基线能否识别中文隐蔽事实污染？

- Null Hypothesis：最佳 eligible semantic-only baseline 的 AUPRC 不高于同一 test prevalence 下的 label-permutation null 分布。
- Alternative Hypothesis：最佳 semantic-only baseline 的 AUPRC 高于 permutation null。
- Primary Endpoint：Document-level AUPRC，附实际 prevalence。
- Secondary Endpoint：Recall at primary controlled FPR、per-HKP recall、calibration error。
- Comparison Direction：semantic-only > permutation/no-score reference。
- Falsification Condition：grouped 95% CI 下界未超过 permutation null，或 Holm-adjusted primary test 不显著。
- Required Dataset Slice：五领域、HKP-1–4、S1–3 与 matched hard negatives 的 locked test。
- Required Baselines：semantic similarity、generic anomaly detector、semantic-only classifier。

### RQ2：多视角方法能否在受控误报率下提高检测召回？

- Null Hypothesis：Full Method 相对最佳 eligible semantic-only baseline 的 Recall@primary-FPR 配对差值不大于 0。
- Alternative Hypothesis：该配对差值大于 0。
- Primary Endpoint：Recall at `FPR = 1%`。
- Secondary Endpoint：AUPRC、Recall@5% FPR、Hard Negative FPR、Brier score。
- Comparison Direction：Full Method > best semantic-only baseline。
- Falsification Condition：grouped paired 95% CI 下界不大于 0，或 primary paired test 经 Holm 修正后不显著。
- Required Dataset Slice：完整 locked test 与五领域/HKP/S 分层。
- Required Baselines：RQ1 baselines、simple fusion baselines、Full Method。

### RQ3：Temporal-Version 与 Provenance 信号能否减少合法变化误报？

- Null Hypothesis：加入 Temporal-Version + Provenance 后，Hard Negative FPR 不低于去除两视角的消融模型，或 poison recall 下降超过候选非劣界值 `2 percentage points`。
- Alternative Hypothesis：Hard Negative FPR 降低，且 poison recall 的下降不超过 2 个百分点。
- Primary Endpoint：matched hard-negative FPR paired difference。
- Secondary Endpoint：legitimate-update、historical-version、exception、department-difference 各类 FPR 与 poison recall difference。
- Comparison Direction：FPR 越低越好；recall 满足非劣性。
- Falsification Condition：FPR 改善 CI 包含 0，或 recall 非劣性失败。2 个百分点是审批候选；Pilot 必须验证其业务合理性，正式冻结不得用 test 调整。
- Required Dataset Slice：所有版本/来源 hard negatives 及其匹配 poison examples。
- Required Baselines：Full Method、minus Temporal-Version、minus Provenance、minus both。

### RQ4：完整方法能否跨攻击、隐蔽等级和领域泛化？

- Null Hypothesis：在 held-out HKP、domain 或 version-pattern 上，Full Method 的 macro Recall@1% FPR 不优于最佳 semantic-only baseline。
- Alternative Hypothesis：Full Method 在预注册的 held-out 族上取得更高 macro Recall@1% FPR。
- Primary Endpoint：各 held-out family 的 macro Recall@1% FPR paired difference。
- Secondary Endpoint：AUPRC、worst-group recall、calibration drift。
- Comparison Direction：Full Method > semantic baseline；同时报告 worst group。
- Falsification Condition：primary family 的 Holm-adjusted paired CI/test 不支持提升，或提升只来自单一领域/攻击。
- Required Dataset Slice：unseen attack、unseen domain、unseen version pattern、cross-source transfer。
- Required Baselines：semantic-only、simple fusion、Full Method。

### RQ5：各视角及交互的独立贡献是什么？

- Null Hypothesis：移除任一视角或预注册的关键双视角交互，不改变 Recall@1% FPR/AUPRC。
- Alternative Hypothesis：至少一个视角或交互具有非零配对效应。
- Primary Endpoint：leave-one-view-out 对 Recall@1% FPR 的配对变化。
- Secondary Endpoint：AUPRC、Hard Negative FPR、SHAP/permutation importance 或等价无标签泄漏解释量。
- Comparison Direction：完整方法相对消融更优；负贡献亦如实报告。
- Falsification Condition：所有预注册消融的 adjusted CI 均覆盖 0。
- Required Dataset Slice：locked main test 和 hard-negative slices。
- Required Baselines：五个单视角、两类简单融合、Full Method、五个 leave-one-view-out。

### RQ6：Option B 能否降低污染进入检索集合的概率并保持正常效用？

- Null Hypothesis：Hard Filtering/Soft Downweighting 不能降低 Poisoned@10，或 clean Recall@10 的下降超过候选非劣界值 `2 percentage points`。
- Alternative Hypothesis：至少一个冻结 intervention 降低 Poisoned@10，且 clean Recall@10 的下降不超过 2 个百分点。
- Primary Endpoints：安全端 `Poisoned@10 paired change`；效用端 `clean Recall@10 paired change`。两者是分开的 co-primary endpoints，必须分别报告并同时满足，不计算掩盖权衡的单一综合分数。
- Secondary Endpoint：poisoned retrieval rate、MRR、nDCG@10、clean retention、over-filter、abstention、latency/resource。
- Comparison Direction：安全指标下降、效用损失受限。
- Falsification Condition：安全收益 CI 包含 0，或 clean Recall@10 非劣性失败；任一失败都不支持 Option B 有效。
- Required Dataset Slice：同一 query 的 clean/poisoned retrieval sets、deployment-like prevalence slices。
- Required Baselines：no intervention、equal-budget random filtering、semantic filtering、eligible GMTP filtering、Full hard filtering、Full soft downweighting。

## 4. 评估单位、上下文和统计独立性

| 单位 | 定义 | 主要用途 | 可见上下文 |
| --- | --- | --- | --- |
| Document Unit | 单个候选检索文档 | 文档级 score/label 的载体 | 文档与允许的公开元数据 |
| Claim Unit | 实体—主张—属性—条件—时间—来源关系 | 事实变化与解释 | 同一文档内的结构化 claim |
| Version-Chain Unit | 同一 claim 的前序/当前/后续版本 | Temporal-Version 与合法更新判断 | 允许的版本链，不含 evaluator labels |
| Query-Document Unit | query 与候选文档组成的样本 | **Detector 主要评估单位** | query、document、允许元数据及必要版本证据 |
| Retrieval-Set Unit | 一个 query 的 Top-K 文档集合 | **Hard Filtering/Soft Downweighting 作用单位** | 同一 query 的候选分数与 detector risk |
| Downstream Task Unit | 检索集合进入生成模型后的回答任务 | 后续次级评估候选 | 仅在单独批准的下游实验使用 |

统计重采样和 split 使用 `independence_group_id`：由 `entity_id`、claim family、`version_chain_id`、source-document family、mutation-template family 与 near-duplicate cluster 的传递闭包形成。任何共享闭包的样本不得跨 split；bootstrap/permutation 以 group 为单位，禁止把同一版本链的 Query-Document 当独立观测。

## 5. Benchmark 数据来源、组成与版本策略

`PRIMARY_DATA_STRATEGY = PUBLIC_TRACEABLE_CHINESE_DOCUMENTS + CONTROLLED_MUTATION + HUMAN_REVIEW`。

- 优先公开、可追溯、具有版本/时效关系的中文政府、教育、科研机构或公开企业制度样例。
- 每个来源记录 URL/source ID、许可/使用条款状态、抓取 UTC、内容 hash、版本身份和 provenance chain。
- 污染通过受控字段变换产生；变换后进行事实变化、语义自然度、检索相关性和隐蔽性人工复核。
- 不使用私人企业内部文档；许可不明原文不默认公开。
- 原文、派生样本、结构化 schema、hash 和统计结果分别判断发布权限。
- 本轮不下载、采集、转换或标注任何数据。

### 5.1 Benchmark 组成候选

- 领域：企业人力资源、财务、信息安全、采购与研发、教育与科研。
- 攻击：HKP-1–4；隐蔽等级：S1–3。
- 每个 poison 尽量绑定一个 clean source、一个合法变化/历史关系和至少一个 matched hard negative。
- group-aware split 候选按 group 数量为 train/dev/test = `70% / 15% / 15%`；test 在任何阈值或模型选择前锁定。
- 训练候选至少 `1 poison : 2 hard negatives`；dev 至少 `1:3`；diagnostic test 至少 `1:4`。另建真实 prevalence 的 deployment-like test slices，候选污染率为 `1%` 和 `5%`，并显式记录 prevalence。
- 这些是比例候选，不是样本已存在或已冻结的事实；正式数量由第 15 节 Pilot 与 power/precision analysis 决定。

## 6. Benchmark Schema 与字段可见性

### 6.1 分组字段

- Identity：`sample_id`、`document_id`、`query_id`、`entity_id`、`claim_id`、`version_chain_id`、`version_id`、`independence_group_id`。
- Version：`predecessor_id`、`successor_id`、`effective_at`、`expires_at`、`repealed_at`、`supersedes`、`amends`。
- Authority/Provenance：`source_id`、`source_type`、`authority_level`、`jurisdiction`、`department`、`provenance_chain`、`citation_reference`。
- Claim：`subject`、`predicate`、`object`、`numeric_value`、`unit`、`condition_scope`、`exception_scope`、`temporal_scope`。
- Attack：`label`、`attack_type`、`stealth_level`、`mutation_operation`、`changed_claim_fields`、`source_sample_id`。
- Evaluation Only：`annotator_labels`、`adjudicated_label`、`rationale`、`hard_negative_type`、`split`、`evaluator_notes`。

### 6.2 字段可见性矩阵

| 字段族 | Retriever visible | Detector visible | Intervention visible | Evaluator only | Releaseable | Private |
| --- | --- | --- | --- | --- | --- | --- |
| Query/public document text | yes | yes | no direct text need | no | by source license | restricted when license requires |
| Public identity/version/provenance/claim fields | allowlisted subset | yes | document ID + frozen scores only | no | schema/hash or full by license | source restrictions apply |
| Retrieval score/rank | runtime | Retrieval-Behavior only | yes | no | aggregate by default | per-query trace may be private |
| Detector score/calibration/explanation | no | output | yes | no | aggregate + redacted examples | detailed trace if sensitive |
| `label`/attack/HKP/S/mutation fields | **no** | **no at inference** | **no** | yes | redacted/derived only | raw evaluator table |
| annotator/adjudication/rationale/split/evaluator notes | **no** | **no** | **no** | yes | aggregate agreement only | yes |

任何 evaluator-only 字段进入模型可见正文、metadata、embedding input、feature cache、fingerprint 或 intervention input，立即登记 `LABEL_LEAKAGE_BLOCKER` 并 fail closed。

## 7. Group-Aware Split 与泄漏防护

同一 `entity_id`、claim family、`version_chain_id`、source-document family、mutation-template family 或 near-duplicate cluster 的传递闭包不得跨 train/dev/test。测试清单必须包括：exact duplicate、normalized duplicate、semantic near-duplicate、template leakage、entity leakage、version-chain leakage、recursive label-field、metadata leakage 与 embedding-input leakage scan。

Semantic near-duplicate threshold 不在本文凭经验冻结；Pilot 以人工复核的 duplicate/non-duplicate pairs 选择阈值，之后在正式 split 前冻结。任何 scan 无法完成、阈值未冻结或发现跨 split 泄漏均为 `DATA_SPLIT_LEAKAGE_BLOCKER`。

## 8. HKP-1–4 构造合同

所有攻击必须满足：主题/查询相关性保持、至少一个事实状态实质改变、语法流畅、无明显攻击标记、修改可追溯到 `changed_claim_fields`。不得把纯语法错误或明显异常措辞作为主要隐蔽样本。失败变换保留为 invalid/excluded record，不进入成功样本分母。

| 类型 | 可修改 | 不可修改 | 幅度与事实要求 | 失败条件 |
| --- | --- | --- | --- | --- |
| HKP-1 数值/实体 | `object`、`numeric_value`、`unit`、关键实体/属性 | query identity、未声明的其他 claim、来源原文证据 | 每次以一个主 claim 为主；单位变化须产生不同事实，不接受等价换算 | 事实未改变、主题漂移、明显不自然 |
| HKP-2 条件/例外 | `condition_scope`、`exception_scope`、适用/否定关系 | 无关条款与版本身份 | 添加、删除或替换一个关键适用边界，必须改变适用集合 | 只改措辞、不改变适用性、逻辑自相矛盾 |
| HKP-3 时间/版本 | 生效/失效/废止/替代/修订关系与顺序 | 原始链证据和 source identity | 改变一个时间或链关系，并保持表面时间表达合理 | 仍与真实链等价、时间不可能、无需版本证据即可明显发现 |
| HKP-4 来源/权威 | 来源、权威级别、机构归属、引用关系的派生陈述 | 原始 provenance audit record | 伪装必须改变可信权重或归属判断 | 只改格式、来源不存在且明显虚构、无法审计 |

Automatic pre-check 验证字段差分、文本有效性、hash、非空、长度、语言和检索相关性下限；具体相关性下限由 Pilot 基于 clean distribution 冻结。双人独立审核事实变化、自然度、相关性与攻击类型；第三人仲裁不一致。

## 9. S1–S3 可操作判定与标注协议

- S1：局部句段检查即可发现，但文本自然且主题相关；不依赖外部版本链。
- S2：单文档内较难发现，需要同文档主张/条件或允许的来源交叉核验。
- S3：必须依赖跨文档、版本链、时间或权威关系才能判断；缺少这些证据时应允许 `MISSING_EVIDENCE / ABSTAIN`。

每个样本先 automatic pre-check，再由两名对当前 method output 不可见的标注者独立给出事实标签、HKP、S 等级和 hard-negative type；不一致由第三人仲裁。报告 Cohen's kappa（两人名义标签）或 Krippendorff's alpha（多标注者/缺失或有序 S 等级适用）。候选进入线：`>=0.80` 可接受；`0.67–0.80` 需定向培训、全部争议仲裁并复测；`<0.67` 触发 `ANNOTATION_PROTOCOL_BLOCKER`，回退重写类别/指南，不得扩大正式标注。

## 10. Hard Negative 匹配合同

Hard Negative 包括合法新版本、已废止历史版本、尚未生效版本、合法例外、地区差异、部门差异、权威来源冲突、同名实体、不同时间范围、无害措辞变化、信息缺失但不构成恶意污染、多来源事实并存。

每个正样本尽量匹配同领域、同 claim 类型、相似长度、相似检索相关度与相似语言复杂度的 hard negative。匹配变量、容差、无法匹配原因和 replacement policy 写入 manifest；禁止为了更易分类选择明显短、低相关或措辞异常的 negatives。AUPRC 必须同时给出 test prevalence，禁止只在人工平衡 test 上报告；deployment-like slices 作为独立评估，不与 diagnostic test 混合。

## 11. Baseline 分层与公平性合同

| 层 | Baseline | 作用 |
| --- | --- | --- |
| A | No defense / original retrieval | 干预与污染暴露参考 |
| B | semantic similarity、generic anomaly、semantic-only classifier | 语义基线 |
| C | GMTP 与其他满足许可/任务条件的 published detector | 公开检测方法；先判定可比性 |
| D | Entity-Claim only、Provenance only、Temporal-Version only、Retrieval-Behavior only | 结构化单视角 |
| E | concat + Logistic Regression、concat + tree-based classifier | 无专门版本建模的简单融合 |
| F | Full version-aware multi-view method | 候选完整方法 |
| G | no intervention、equal-budget random、semantic、eligible GMTP、Full hard、Full soft | Option B 干预对照 |

所有 baseline 冻结相同 split、允许输入/metadata、训练与调参机会、seed、threshold-selection rule、模型大小/参数量、运行资源和失败处理。公开方法按证据分类为 `STRICT_REPRODUCTION`、`PARTIAL_REPRODUCTION`、`NON_STRICT_COMPARISON` 或 `TRANSFER_EVALUATION`；不满足 strict 条件时不得比较论文数字或宣称优越性。

## 12. 五视角与融合接口合同

每个视角仅消费第 6 节 allowlist 输入并输出统一对象：

```text
ViewOutput {
  view_name, query_document_id, view_score, feature_vector,
  evidence_items, missing_evidence_flag, confidence,
  explanation_fragment, feature_schema_version
}
```

- Semantic：query/document 语义一致性、局部冲突与异常程度。
- Entity-Claim：实体、主张、属性、条件、数值和单位关系。
- Provenance：来源、权威级别、引用链和机构归属。
- Temporal-Version：生效、失效、废止、替代、修订和版本顺序。
- Retrieval-Behavior：排名变化、邻域异常、Top-K 稳定性和冻结 query perturbation。

融合层候选输出 `poison_risk ∈ [0,1]`、`calibrated_risk`、view contributions、final label、explanation 与 abstention reason。缺少必要版本/来源证据时不得静默填零；必须输出 `MISSING_EVIDENCE / ABSTAIN`。至少比较 Logistic Regression fusion、tree-based fusion 与 planned full fusion method；本轮不选择神经网络规模或实现接口。

## 13. Option B 干预合同

### 13.1 Hard Filtering

对 Retrieval-Set 中文档 `i`：

```text
remove(i) iff calibrated_risk_i >= tau_filter
```

`tau_filter` 只在 dev 按 primary controlled FPR 与 utility constraint 冻结；设置 `max_filter_count` 和 `max_filter_fraction` 双预算。预算值由 Pilot 的 Top-K/clean utility 分布确定。过滤后少于冻结的 `min_remaining_documents` 时输出 abstention，不回填未审计文档，不在 test 调阈值。

### 13.2 Soft Downweighting

```text
adjusted_score_i = normalized_retrieval_score_i - lambda * calibrated_risk_i
```

`normalized_retrieval_score` 的方向、范围和按-query 归一化方法在 dev 前固定；候选优先使用可审计的 `[0,1]` min-max（全相等时固定为 0.5 并记录）。`lambda >= 0` 仅在 dev 冻结；risk 必须来自同一冻结 detector。重排 tie-break 使用稳定 `document_id`；test-time tuning、用 evaluator label 改 score 或按结果反复选择 lambda 均禁止。

Hard/Soft 分别报告安全收益、clean utility loss、over-filter、abstention、latency 与资源；不使用单一综合分数隐藏权衡。`Retrieval Intervention = NOT IMPLEMENTED`。

## 14. 指标、阈值和统计分辨率

### 14.1 Detector

- Primary：AUPRC、Recall@`1% FPR`、Hard Negative FPR。
- Secondary：Recall@`5% FPR`、AUROC、F1 at frozen threshold、ECE、Brier score、per-HKP/S/domain recall。
- `1%` 是低误报部署目标候选；`5%` 是较宽松的 sensitivity boundary。二者在协议批准后固定，不由 test 选择。

### 14.2 Intervention

- 安全：Poisoned@K、poisoned retrieval rate、filtering success rate；downstream ASR 仅在单独批准的 downstream experiment 使用。
- 效用：clean Recall@K、MRR、nDCG、clean document retention、over-filter、abstention。
- 主 K 候选为 `K=10`，用于与 W2/常见 retrieval set 宽度衔接；`K=5` 与 `K=20` 为 sensitivity，不得择优汇报。
- 工程：latency、throughput、peak RAM/VRAM、disk、model size。

### 14.3 所需负样本量

若真实 FPR 约 1%，95% 正态近似半宽 0.5 个百分点需要约
`1.96^2 * 0.01 * 0.99 / 0.005^2 = 1,522` 个独立 negative groups。候选最低取 `2,000` 个 test negative groups（每领域至少 400），既提供约 20 个预期 false positives，也允许 Wilson/group-bootstrap CI；若 Pilot 显示聚类设计效应，按 design effect 上调。零误报时同时报告 rule-of-three 上界，绝不写成 FPR=0 的确定结论。

Positive group 数量按 Pilot 的 observed recall 通过 precision/power analysis 冻结：总体 recall CI 目标半宽不大于 5 个百分点，关键边际 slice 不大于 10 个百分点。完整 HKP×S×domain 交叉若无法达到该分辨率，只作 exploratory，不提升为主结论。

## 15. 统计协议与两阶段样本量冻结

- 至少 5 个随机 seeds；Full Matrix 候选使用 10 seeds。
- 95% CI；按 `independence_group_id` 执行 `10,000` 次 grouped bootstrap。
- 模型/干预比较优先 paired grouped bootstrap；无法稳定 bootstrap 时使用 `10,000` 次 paired permutation test。
- 连续/概率指标报告 paired mean/median difference 和 standardized effect size；二分类配对可补充 risk difference/odds ratio。
- Primary comparison family：RQ1–RQ6 的预注册 primary endpoints；Holm correction。
- Secondary exploratory family：分层、calibration、额外交互和 sensitivity；明确 exploratory，不混入 primary family。
- 所有 per-domain/per-HKP/per-S 报告样本量、prevalence、CI；不只报告宏平均。
- failed run 纳入 failure-rate 与资源分母；invalid run 仅按预冻结规则排除并保留；missing result 不做成功值插补，报告 missingness 并做 worst-case sensitivity。

### Stage A — Pilot（仍未批准）

候选规模为 240 个独立 source/version-chain groups，覆盖五领域、12 个 HKP×S 组合和至少 240 个 matched hard negatives；只估计标注一致性、类别难度、variance/design effect、近重复阈值、运行时间/资源和 intervention utility margin。Pilot 可以促使协议修订，但不得进入 final test、不得作为 Paper Result。

### Stage B — Formal Freeze

用 Pilot 估计的 agreement、recall/FPR、组内相关、效应大小、runtime 和 failure rate 完成 power/precision analysis；再冻结正式 group 数、slice coverage、资源、阈值和 run matrix。不得凭 Pilot 的“好结果”选择方法或 test threshold。

## 16. 实验 Tracks

- Track A：外部 baseline 复现与可比性；严格区分 `STRICT_REPRODUCTION`、`PARTIAL_REPRODUCTION`、`NON_STRICT_COMPARISON`、`TRANSFER_EVALUATION`。
- Track B：中文版本化 Benchmark 主实验；包含 HKP-1–4、S1–3、hard negatives、五领域、Detector 与 Option B intervention。
- Track C：unseen attack/domain/version pattern、adaptive attack、cross-source transfer。

Track 间不得共享 test 调参信息。Track C 的 holdout family 在训练前冻结；任何 test feedback 导致的新版本必须生成新 protocol/run family，旧结果保留。

## 17. 候选运行矩阵与资源估算

运行的基本键为：`baseline × view_combination × attack_scope × stealth_scope × domain_scope × seed × intervention_mode × threshold_policy × split`。HKP/S/domain 通常作为同一 locked run 的分层输出，不为每个 slice 重复训练；只有 leave-family-out generalization 产生独立训练 run。

### 17.1 MINIMAL_PUBLISHABLE_MATRIX

| 类别 | 组合 | Seeds | Logical runs |
| --- | ---: | ---: | ---: |
| Detector baselines/full/5 leave-one-view-out | 16 | 5 | 80 |
| Intervention modes | 6 | 5 | 30 |
| Leave-one-HKP/domain/version-pattern generalization | 10 | 5 | 50 |
| **总计** |  |  | **160** |

候选资源上界：约 `100 GPU-hours`、`160 CPU-hours`、`200 GB` task-owned disk、`20 GB` indexed evidence。估算假设 detector/generalization 每 run 不超过 0.5 GPU-hour、intervention 不超过 0.25 GPU-hour，并含约 20% 失败/调度余量；Pilot 必须用实测替换，超出即重新审批。

### 17.2 FULL_MATRIX

| 类别 | 组合 | Seeds | Logical runs |
| --- | ---: | ---: | ---: |
| Detector baselines/full/ablations | 16 | 10 | 160 |
| Intervention modes | 6 | 10 | 60 |
| HKP/domain/version/source/adaptive holdouts | 21 | 10 | 210 |
| Threshold/calibration sensitivity jobs | 3 | 10 | 30 |
| **总计** |  |  | **460** |

候选资源上界：约 `300 GPU-hours`、`500 CPU-hours`、`500 GB` task-owned disk、`60 GB` indexed evidence，包含 external-baseline compatibility 与 20% failure/scheduling allowance。它不是资源批准；Pilot 若显示单 run 上界、模型大小或证据量超过假设，必须 `RESOURCE_BUDGET_REVIEW_REQUIRED`。

## 18. Evidence 与 Run Manifest

每个正式 run 绑定：`run_id`、`task_id`、Git commit、dirty/clean、data snapshot、schema version、split hash、model revision、environment hash、parameters、seed、threshold、intervention mode、start/end UTC、exit code、wall time、peak resource、raw result、derived result、evidence index 与 claims classification。

successful、failed、invalid、excluded runs 和 rerun reason 全部追加保存；正式 run 目录不可覆盖。Raw 与 derived results 分离，derived artifact 必须记录输入 hash 和生成命令。缺 Git/data/model/environment/parameter/index 任一身份即 `RUN_MANIFEST_BLOCKER`，不得进入正式聚合。

## 19. 许可与发布协议

逐项登记原始文档、派生样本、模型、baseline 源码、运行结果许可，以及 public/private/hash-only/authorization-required 字段。候选发布级别：

- `PUBLIC_FULL`：仅用于许可明确允许原文和派生样本再分发的条目。
- `PUBLIC_REDACTED`：发布 schema、必要片段/脱敏派生和统计，隐藏受限原文。
- `HASH_ONLY`：只发布 identity/hash/manifest 与复现申请说明。
- `INTERNAL_ONLY`：许可、隐私或合同不允许公开的工件。

默认是最小授权：许可状态未知时不得升级为 PUBLIC。Benchmark 主表必须把 runtime visibility 与 releaseability 分开，防止 evaluator-only 字段因“可发布”误入模型输入。

## 20. P1 正式进入条件

P1 获批前以下二十项必须全部满足：Option B 范围登记；RQ/假设；schema；数据来源；标注；HKP/S；hard negatives；split/leakage；baseline 分类；五视角接口；Option B 公式；指标；统计；Pilot 目标；运行矩阵；资源；可执行 evidence contract；许可发布；claims boundary；项目需求提出人明确批准。

当前状态：

- `S6.1-P1-R1 = REVIEW_CANDIDATE / NOT APPROVED / NOT STARTED`
- `S6.1-P1 = NOT APPROVED / NOT STARTED`
- `Dataset = NOT FROZEN`
- `Pilot = NOT APPROVED / NOT STARTED`
- `Detector = NOT IMPLEMENTED`
- `Retrieval Intervention = NOT IMPLEMENTED`
- `Training = NOT STARTED`
- `Our Method Result = NONE`
- `Formal Experiment = NOT STARTED`

## 21. Forward Risk Review 与 Paper Risk Review

- `FORWARD_RISK_REVIEW = PASS_FOR_REVIEW_CANDIDATE_ONLY`：Option B 与 Paper 2 trusted-context boundary 已分离；接口、split、evidence 和资源前置，可降低后期重构风险。
- `PAPER_RISK_REVIEW = PASS_FOR_OWNER_REVIEW_WITH_OPEN_FREEZES`：主要 reviewer attack surface 是数据真实性/许可、hard-negative 难度、version-chain leakage、baseline 可比性、1% FPR 分辨率、utility margin 与选择性报告。本文给出处理合同，但在 Pilot/正式数量/发布策略获批前不得称为 accepted protocol。
- Remaining blockers：`P1_R1_OWNER_REVIEW_REQUIRED`、`PILOT_NOT_APPROVED`、`DATASET_NOT_FROZEN`、`FORMAL_ENVIRONMENT_NOT_FROZEN`。

## 22. 需要项目需求提出人决定

P1-R1 完成后只保留四项高层决定：

1. 是否接受本 P1-R1 正式协议框架？
2. 是否批准只用于样本量、标注一致性和资源估计的小规模 Pilot？
3. 正式路线选择 `MINIMAL_PUBLISHABLE_MATRIX` 还是 `FULL_MATRIX`？
4. Benchmark 发布策略选择 `PUBLIC_FULL / PUBLIC_REDACTED / HASH_ONLY / INTERNAL_ONLY` 中的哪一级或按许可逐条混合？

技术参数的当前推荐是 primary FPR `1%`、secondary FPR `5%`、primary `K=10`、sensitivity `K=5/20`、5 seeds（Full 10）、10,000 grouped resamples、2,000 test negative groups minimum、group-aware 70/15/15 和两阶段 Pilot → power/precision freeze。项目负责人只需决定框架、Pilot、矩阵规模和发布策略；任何批准仍须单独明确登记。
