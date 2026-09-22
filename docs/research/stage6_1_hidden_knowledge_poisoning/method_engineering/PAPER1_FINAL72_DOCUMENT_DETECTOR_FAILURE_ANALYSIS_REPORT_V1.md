# Final72 Document Detector 失败分析（开发集诊断）

Status: `FAILURE_ANALYSIS_COMPLETE / MULTIVIEW_SIGNAL_MIXED / NOT_FORMAL_PAPER_RESULT`. Owner 先批准有界寻找原始八模型 OOF；未找到可核验原件后，依授权做一次严格等配置证据重建。原 Full SEPT OOF、九模型机器汇总、bootstrap、permutation 均是历史 canonical 结果，完全不改。[重建记录](PAPER1_DETECTOR_V1_1_EVIDENCE_RECONSTRUCTION_RECORD_V1.md)与[原 blocker](PAPER1_DOCUMENT_DETECTOR_FAILURE_ANALYSIS_EVIDENCE_BLOCKER_01.md)保留完整时序。

## 结果究竟说明什么

Final72 是已暴露的 24 组三元组开发集，不是 untouched test。Full SEPT 的原始 LOGO AUROC `.6471`、AUPRC `.4964`、Poison>HN `18/24`、固定 `.5` 阈值 HN 误报 `8/24`。S-only AUROC `.6228`、AUPRC `.4664`，与 Full 接近。Full-P 的 AUROC/AUPRC 为约 `.673/.571`，Full-T 为约 `.674/.536`；这说明当前小样本的四视角组合没有稳定地胜过去掉 P/T 的组合，不能删掉 P/T，也不能声称其因果作用或正式效果。Full-S 更弱，表明本轮的多视角信息混合且依赖当前信号可观测性。

最关键的纠错是：P-only 与 T-only 的 Poison>HN 各为 `2 win / 20 tie / 2 loss`，并非各有 22 个 HN 压过 Poison。T-only 的 HN-FPR@0.5 为 `22/24`，反映固定阈值下总体分数位置问题；它本身不能证明“合法历史被系统性排在 Poison 之上”。因此 `TEMPORAL_HISTORICALNESS_CONFUSION=PARTIALLY_SUPPORTED`：T 信息不足且在 Full 中经常压低 P–HN 间隔，但单独 T 的 matched 方向主要是**无区分度**。此结论比简单的“时间视角把历史都判毒”更严格。

## 21 项特征与逐组方向

名义 21 项中 7 项在观测值上恒定：`document_identity_match`、`entity_conflict`、`official_repost`、`official_source`、`predicate_match`、`subject_match`、`version_identity_match`。其中 `document_identity_match`/`official_source`/`subject_match` 在 72 条上完全同向重复，`entity_conflict`/`predicate_match` 完全同向重复；`negation_flip`/`relation_conflict` 是另一对完全重复的**变化**列。故非恒定 14 项中仅有 **13 条不同的变化向量**，这是诊断性有效维数，不是特征选择或新模型。常量原因是可检验的候选解释：官方可信库的同质性、当前抽取器覆盖与信号粒度；本轮不把原因当作已独立证明的事实。

| 恒定特征 | 观测/72 与值 | 可检验的主要解释（非已证明根因） |
| --- | --- | --- |
| `document_identity_match` | 72，均 1 | 同主体证据检索任务使文档身份信号饱和；需测不同版本/同名干扰项。 |
| `official_source` | 72，均 1 | 57 文档统一可信官方库的设计同质性；非官方性本就不在本输入范围。 |
| `subject_match` | 72，均 1 | 当前主体抽取/聚合只在同主题匹配上有观测变化不足。 |
| `entity_conflict` | 72，均 0 | 当前实体冲突抽取器或候选覆盖不足；需人工抽样核对，不将“无冲突”视为已证实。 |
| `predicate_match` | 72，均 0 | 谓词匹配过粗或抽取器未捕获关系；须在 Formal 前做可观测性测试。 |
| `official_repost` | 64，均 0；8 缺失 | 可信池未提供有变异的转载角色，且有缺失；不能将缺失补 0。 |
| `version_identity_match` | 38，均 1；34 缺失 | 已识别版本的同一性饱和，未识别版本需单独保留缺失。 |

P–HN 风险方向：`current_version_semantic_similarity` 在 15 组方向正确、9 组相反；`semantic_version_margin` 为 12/12；`current_fact_match` 仅 3 组可同时比较且方向正确。`provenance_consistency` 仅 4 组有差异（3 正、1 反），其余 20 组打平；`official_source`、`document_identity_match`、`subject_match` 全部打平。`negation_flip` 与 `relation_conflict` 均为 3 正、8 反、13 平；它们还完全重复，不能当两个独立证据。数值矩阵的 null 未携带 N/A 与输入缺失的区分，本报告不把两者混同为安全值；[独立 availability overlay](PAPER1_FINAL72_FEATURE_APPLICABILITY_AUDIT_V1.json)从冻结 V1 availability 文件恢复了保留 21 特征的 N/A、输入缺失与 Evidence 不充分计数。该 overlay 仅供审计，不成为模型输入或更改已有分析目录。

Full 相对 Full-T 的 P–HN 间隔：7 组提高、17 组降低；Full 相对 Full-P：19 组提高、5 组降低。这里的 HELPED/HURT 是“加入该视角后 held-out 分数间隔的符号变化”，不是因果效应，也不与整体 AUROC 排名必然同向。后者尤其说明：即使 P 在多数组提高间隔，少数大幅负向组（如 `INF-05`、`EDU-03`）仍可能拖累整体排序。逐组三类分数及 P–HN、P–Clean 间隔均在私有 handoff namespace `paper1_final72_detector_failure_analysis_20260922` 下的 `PAPER1_FULL_VS_MINUS_VIEW_SCORE_SHIFT_V1.json`；Git 文档不复写原始分数。

## Temporal 与 Provenance 缺口

当前 T 只有 `current_fact_match`、`historical_fact_match`、`present_time_substitution_signal` 三项；均只在 10/72 行有数值。PTS V3 在 40 个 temporal-applicable 样本中只计算了 10 个，另外 22 个 Evidence 不充分、8 个输入缺失。`historical_fact_match` 和 PTS 本身是非单调信号，不能简单以“越大越危险”比较。六项仍属 Oracle-only 的 T 能力包括 version mismatch、superseded relation、effective interval、current/history binding、successor 和 version distance；目前不能偷偷并回 Full。因此现有 T 更像局部事实/历史支持提示，而非完整的“历史正确但冒充当前”判别器。`TEMPORAL_HISTORICALNESS_CONFUSION` 仅部分支持，主要观测是覆盖不足与 20/24 matched ties。

P 当前六项中三项恒定，`claimed_authority_match` 仅 8 行观测，另有 `host_publisher_relation`、`publisher_issuer_match` 两项因缺可信候选级关系而正式 deferred。57 文档官方可信库中“是否官方”天然难区分三类候选；真正需要的是 host、页面发布者、签发/修订机关、权威角色、文档与版本身份之间的**关系**。P-only 的 20 个 matched ties 与这些缺口一致，但不能单凭现有 OOF 锁定唯一机制。Full-P 优于 Full 的几个 aggregate 指标是当前数据与模型的现象，不代表 P 在正式有丰富关系变异的语料中无用。

## 难组、分层与系数

七个需要重点复查的组为 `EDU-06`、`FIN-03`、`FIN-04`、`HR-03`、`INF-01`、`INF-04`、`INF-05`。其中 `FIN-03`、`INF-01`、`INF-05` 的 Full P–HN 间隔分别约 `-1.42/-1.48/-1.64`，`HR-03` 仅约 `-0.04`。每组的三种候选摘录、冻结 Q_NO_TITLE Hybrid Top5 检索 ID、S/E/P/T 值与标签后诊断标签保存在独立私有 `PAPER1_DOCUMENT_DETECTOR_HARD_GROUP_ANALYSIS_V1.json`，未用人工 E1/E2 替换检索结果。failure taxonomy 的 `*_CANDIDATE` 是可能机制，不是已证明的单因果解释。

[F1–F12 分类空间](PAPER1_DOCUMENT_DETECTOR_FAILURE_TAXONOMY_SCHEMA_V1.json)区分语义不足、历史性混淆、当前版本绑定缺口、来源同质、元数据覆盖、检索歧义、常量/低方差、冗余、领域/HKP 模式、小 N 不稳及其他。逐组工件只为有相应观测的类别打候选标签；没有打 F6/F11 等标签**不表示**这些机制已被排除。当前较强的全局证据是可观测性/常量、相关冗余和证据库难度；“历史性混淆”只得到部分支持。

按 HKP 分层，Full P>HN 为 HKP1 `5/6`、HKP2 `5/6`、HKP3 `5/6`、HKP4 `3/6`；S-only 在 HKP3 仅 `1/6`，但 Full 为 `5/6`。按 S1/S2/S3，Full 分别为 `6/8`、`7/8`、`5/8`，并不支持当前 Pilot 上“越隐蔽单调越差”的正式趋势。四领域 Full 分别为教育 `5/6`、财经采购 `4/6`、劳动人事 `5/6`、信息治理 `4/6`。各分层样本极小，须在未来独立链和 untouched test 中检验。

Full 的 24 折系数诊断为 8 项与预声明风险方向同号、3 项反号、7 项恒定、3 项非单调不应比较符号。反号的 `exception_conflict`、`negation_flip`、`relation_conflict` 不自动说明合同错误：后二者完全重复；`condition_conflict` 与其在共同观测子集上的 Spearman 为 1，`current_fact_match` 与当前语义相似度共同观测 10 行上相关约 `.93`。小样本（69 train/21 features）、相关性与缺失覆盖均可能让条件系数不稳定；不能解释为因果重要性，也不在本轮删列重训。

## 对 240-group 的约束与下一步

五视角架构保持 S/E/P/T/R：Stage A 为 S+E+P+T 文档风险，Stage B 才结合 R/query 估计检索暴露。`MULTIVIEW_SIGNAL_MIXED` 保持。正式 240 independent groups 不能机械复制 Final72：需预先保存来源充分的 version family/role/interval/successor/current binding、host/publisher/issuer/authority/repost 关系；统一官方库需同主体不同版本、同机关不同断言和词面相似但无关的官方干扰项；HN 需与 Poison 更接近却保持合法历史真实性。正式特征冻结前做 observability/variance/availability 预检，正式运行按 [输出保留合同](PAPER1_EXPERIMENT_OUTPUT_CONTRACT_V1.md)保存所有视角及消融逐样本分数与折身份。

[五项可证伪规模假设](PAPER1_FORMAL_SCALE_HYPOTHESES_V1.json)仅用于规划。`NEXT_RESEARCH_PRIORITY=MOVE_TO_FORMAL_240_GROUP_BENCHMARK_CONSTRUCTION`，但这**不是**自动批准生成 720 条或启动正式训练。当前瓶颈主要是可观测性、证据库难度与小 N；无证据支持现在在 Final72 继续调 LR 或自动换 XGBoost。MLM/PPL/GMTP 仍是未来独立 baseline bundle。Paper 1 的核心多视角假设仍值得在新、独立、困难的版本链 benchmark 上检验，尚未得到验证。
