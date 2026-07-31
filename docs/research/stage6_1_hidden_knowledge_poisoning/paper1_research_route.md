# Paper 1 研究路线

## 1. 工作题目

中文工作题目：

> 《版本化 RAG 知识库中的隐蔽事实污染：基准构建与多视角检测方法》

英文工作题目：

> *Stealthy Factual Poisoning in Versioned RAG Knowledge Bases: A Benchmark and Multi-View Detection Framework*

两者均为 `WORKING TITLE`，不是最终投稿标题。

## 2. 科学问题

当污染文档语言自然、主题高度相关、只修改少量关键事实、Embedding 仍高度相似，并可伪装来源、时间和版本时，
如何识别恶意知识污染，并区分合法新版本、真实例外、历史版本、跨部门差异以及自然冲突和噪声？

“版本感知”不是 Git 版本或单独比较 `version_number`，而是联合建模 predecessor/successor、effective time、
expiration/repeal、publishing authority 和版本间事实变化。

## 3. 三轨实验路线

### Track A：External Benchmark

- PoisonedRAG：Primary Attack Baseline。
- GMTP：Primary Detection / Defense Baseline。
- SafeRAG：Primary Benchmark / Evaluation Reference。
- 外部数据：Natural Questions、HotpotQA、MS MARCO，以及 SafeRAG 中与 Paper 1 最相关的 Silver Noise 和
  Inter-context Conflict。
- 强制分栏：`Published Result`、`Reproduced Result`、`Our Method Result`。

本轨首先证明方法并非只在自建数据上有效；当前仅完成资料对齐，未开始运行。

### Track B：Chinese / Versioned Stealthy Poisoning Benchmark

领域：

1. `enterprise`
2. `education_research`

初始污染类型：

- `HKP-1` Numeric / Entity Factual Mutation；
- `HKP-2` Condition / Exception Mutation；
- `HKP-3` Temporal / Version Poisoning；
- `HKP-4` Provenance / Source Camouflage。

Stealth level：`S1 Low`、`S2 Medium`、`S3 High`。

Hard Negative 至少覆盖合法政策更新、新版本、真实例外、历史版本、跨部门合法差异、自然知识冲突、
OCR/格式噪声和近义改写。外部论文对齐验收前不继续扩张 taxonomy。

### Track C：Generalization / Robustness

- enterprise -> education_research；
- education_research -> enterprise；
- seen attack -> unseen attack；
- low stealth -> high stealth；
- PoisonedRAG attack -> natural factual poisoning；
- 后期单独审批 Adaptive Attack。

当前只设计，不执行。

## 4. 方法方向

暂称 `Version-Aware Multi-View Poison Detection`，不是最终方法名，也未冻结最终 fusion estimator。

| View | 初始信号 |
| --- | --- |
| V1 Semantic | 自然性、主题一致性、语义异常 |
| V2 Entity-Claim | 数值、日期、角色、条件、例外、实体关系、跨文档事实冲突 |
| V3 Provenance | 来源主体、类型、主题一致性、来源链 |
| V4 Temporal-Version | 版本顺序、生效/废止/替代、事实变化、版本链异常 |
| V5 Retrieval-Behavior | rank、similarity、target-query concentration、rank shift、Top-K/Context exposure |

输出方向是 `Poison Risk Score + Prediction + Explainable Signal Contributions`。Ground Truth 标签不得成为
inference feature。

## 5. Baseline 与指标

Baselines：Always Clean/Majority、Version/Temporal Rule、TF-IDF/character n-gram + Logistic Regression、
Embedding Outlier、GMTP、Single-View Detector、Multi-View Detector。LightGBM、XGBoost 和 small MLP
只是 fusion 候选，不预设优胜者。

Primary detection：AUPRC、F1、Recall under controlled FPR、AUROC。

Safety / Retrieval：Filtering Rate、Poisoned@K、Retrieval Poison Rate、ASR、Recall@K、MRR、nDCG@K、FPR。

Efficiency：feature extraction latency、detector latency、GPU/CPU memory、throughput。

Hard Negative FPR 必须单独报告。

## 6. 直接创新证据

| 新增部分 | 直接证明实验 |
| --- | --- |
| Version-aware signals | 去掉 V4 的消融；恶意篡改与合法版本演化分层混淆矩阵 |
| Provenance signals | 去掉 V3 的消融；source-camouflage 与合法跨部门差异子集 |
| Multi-view fusion | 相同特征预算下对比最佳 single-view 与 full multi-view |
| Hard Negative design | 含/不含 hard-negative 训练，并在固定 hard-negative test 上比较 FPR |
| Cross-domain generalization | enterprise 与 education_research 双向迁移 |
| Unseen/stealth robustness | seen->unseen 与 S1/S2->S3 固定协议 |

这些是未来待批准实验，不是当前已完成结果。

## 7. 当前结论边界

可以宣称：已形成 Paper 1 的工作问题、外部基准角色、三轨路线、多视角方向和比较纪律。

不能宣称：数据集、Detector、训练、复现、统计结果、SOTA、泛化、安全效果或生产可用性已经完成。
