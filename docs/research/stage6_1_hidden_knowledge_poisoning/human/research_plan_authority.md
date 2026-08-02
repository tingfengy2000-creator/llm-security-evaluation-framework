# Paper 1 研究方案权威文件

Document Authority = `PAPER1_RESEARCH_PLAN_AUTHORITY`<br>
Change Permission = `OWNER_CONFIRMATION_REQUIRED`<br>
Current Plan Status = `ACCEPTED_CURRENT_RESEARCH_PLAN`

> 文档职责：Paper 1 当前研究方案的唯一权威入口。阶段事实以 work process 和原始证据为准；历史路线文件只作支撑材料。

## 1. 论文题目与范围

- 已接受英文工作题目：*Stealthy Factual Poisoning in Versioned RAG Knowledge Bases: A Benchmark and Multi-View Detection Framework*。
- 用户最新中文题目：《面向中文检索增强生成系统的版本感知隐蔽知识污染基准与多视角解毒方法》。
- `TITLE_INTENT = CONFIRMED`。
- 已接受技术范围：Benchmark、Detection、Risk Score、Signals、Explanation，以及 Option B 的轻量检索干预。
- `DETOXIFICATION_OPTION = OPTION_B`。
- `DETOXIFICATION_TECHNICAL_SCOPE = OPTION_B_CONFIRMED`。
- `DETOXIFICATION_TECHNICAL_SCOPE_FULL = OPTION_B_DETECTION_AND_LIGHTWEIGHT_RETRIEVAL_INTERVENTION`。
- Option B 只允许基于校准风险的 hard filtering 或 soft downweighting，并同时报告安全与效用；不包含 trusted context package、完整上下文构造、多证据可信上下文生成、复杂端到端 Agent 防御、生产级 RAG 平台或完整可信检索链。
- W2 工程门已以 `ENGINEERING_FEASIBILITY_ONLY` 人工验收并关闭；这不改变研究范围或建立检测有效性。
- [P1-R1 正式实验协议强化候选](../s6_1_p1_r1_protocol_review_candidate.md)为 `REVIEW_CANDIDATE / NOT APPROVED / NOT STARTED`，在候选层替代但不删除[旧 P1 候选](../s6_1_p1_protocol_candidate.md)。

## 2. 研究问题

1. 如何在不依赖明显异常措辞的条件下，构建覆盖版本、时效、权威与例外关系的中文隐蔽知识污染 Benchmark？
2. 多种相互补充的证据视角能否识别检索语义仍然相似、但事实状态已被隐蔽改变的文档？
3. 在受控误报率下，方法能否兼顾污染检测、检索质量、跨攻击与跨领域泛化，并提供可审计解释？

## 3. 威胁模型

- HKP-1 数值/实体污染：改变数值、实体或关键属性。
- HKP-2 条件/例外污染：隐去、添加或替换适用条件和例外。
- HKP-3 时间/版本污染：混淆生效、失效、废止、替代或修订关系。
- HKP-4 来源/权威伪装：伪造来源、权威等级或归属关系。
- S1：轻度隐蔽，局部可察觉；S2：中度隐蔽，与上下文高度一致；S3：高度隐蔽，需要跨文档或版本证据才能判断。
- 防御者可访问检索文档、版本元数据与运行信号，但不得把 evaluator label 暴露给 retriever 或 detector。

## 4. 中文版本化 Benchmark 设计

每个可评估样本绑定版本链与来源身份，显式保存 `effective`、`expiry`、`repeal`、`supersedes`、`amends`、`authority`。数据必须同时覆盖合法更新、历史版本、跨部门差异、例外条件与 hard negatives，从而区分正常版本变化和恶意隐蔽污染。正式 schema、快照、切分和标签隔离合同须在 S6.1-P1 冻结；当前 `Dataset = NOT FROZEN`。

## 5. 外部基线角色

| 外部工作 | 当前角色 | 当前可用证据 | 不得宣称 |
| --- | --- | --- | --- |
| PoisonedRAG | 攻击基线 | 源码身份、发布攻击文本及确定性组装关系 | artifact reuse 不是 attack generation reproduction |
| GMTP | 检测基线 | 源码、输入 schema、检测调用链、固定模型身份及单次 detection-core 工程可行性 | W2 工程门关闭不等于论文复现或检测有效性 |
| SafeRAG | Benchmark 参考 | 部分公开 Benchmark 工件 schema smoke | 不能视为已执行完整 pipeline |

当前未形成统一严格比较；必要时只能标注 `NON_STRICT_COMPARISON`、部分可比或迁移评估。

## 6. 多视角方法

| 视角 | 计划信号 | 当前状态 |
| --- | --- | --- |
| Semantic View | 语义一致性与局部异常 | `PLANNED / NOT IMPLEMENTED` |
| Entity-Claim View | 实体、主张与属性关系 | `PLANNED / NOT IMPLEMENTED` |
| Provenance View | 来源、权威与引用链 | `PLANNED / NOT IMPLEMENTED` |
| Temporal-Version View | 版本、时效与修订关系 | `PLANNED / NOT IMPLEMENTED` |
| Retrieval-Behavior View | 排名、邻域与检索扰动 | `PLANNED / NOT IMPLEMENTED` |

这些视角计划输出风险分数、信号和解释；Option B 计划在冻结阈值下对检索候选执行 hard filtering 或 soft downweighting，并将安全与效用作为分开的共同主结果。尚无 detector 或 retrieval intervention 实现与结果。

## 7. Paper 1 与后续研究边界

Paper 1 包括 Benchmark、Detection、Risk Score、Signals、Explanation，以及严格限于 hard filtering 或 soft downweighting 的轻量检索干预。trusted context package、完整上下文构造、多证据可信上下文生成、复杂端到端 Agent 防御、生产级 RAG 平台和完整可信检索链明确排除并保留给 Paper 2 或后续研究；不得把 Option B 扩张为这些能力。

## 8. 数据设计

- 数据源必须可追溯、许可状态可记录，并按不可变快照固定。
- 文档、查询、版本链、来源、攻击关系与 hard negative 使用稳定 ID。
- Ground Truth、evaluator labels 与私有注释不得进入 retriever 可见字段、metadata 或 fingerprint。
- 划分应控制实体、模板、时间和来源泄漏，并保留自然更新对照组。
- 当前只定义设计原则；未构建、未冻结数据集。

## 9. 实验 Track

- Track A：外部基线与公开 Benchmark；先验证身份、环境与严格可比性，再决定正式复现协议。
- Track B：中文版本化 Benchmark；覆盖 HKP-1 至 HKP-4、S1 至 S3 和版本 hard negatives。
- Track C：跨攻击/跨领域泛化；评估 unseen attack、跨领域与可能的 adaptive attack。

## 10. 指标

- 检测：AUPRC、F1、AUROC、受控 FPR 下 Recall。
- 攻击与检索：Poisoned@K、RPR、ASR、Recall@K、MRR、nDCG、Hard Negative FPR。
- 工程：时间、吞吐、峰值显存和存储开销。
- 具体主指标、K、阈值和汇总方式尚待正式协议冻结。

## 11. 统计协议

计划固定随机种子、报告置信区间和效应量，优先使用配对比较，并保留每次 run 的数据、模型、环境、参数与代码身份。重复次数、显著性检验和多重比较处理在 S6.1-P1 冻结；当前无正式统计结果。

## 12. 消融与泛化

计划进行单视角/多视角、时间与来源信号、风险聚合、hard negative、跨攻击、跨领域、unseen attack 与 adaptive attack 消融或泛化评估。所有项目均为计划，尚未实现或运行。

## 13. 阶段计划

1. S6.1-LR1：路线与基线对齐，已人工验收。
2. S6.1-R0：工程预检，带阻塞项验收。
3. S6.1-R0-FU1：P0/L1/W2 已验收；仅以工程可行性范围关闭。
4. S6.1-P1-R1：审批级强化候选待审，`REVIEW_CANDIDATE / NOT APPROVED / NOT STARTED`；不得冻结或执行数据、Pilot、方法或实验。
5. Benchmark、Detector、Formal Evaluation、Ablation、Generalization、Paper Writing：均需各自审批与证据门。

## 14. 正式实验进入条件

- W2 与外部基线可行性 blocker 关闭并获人工验收。
- 数据来源、许可、schema、快照、切分和 label isolation 冻结。
- 外部 baseline 的严格/非严格可比类别与运行配置冻结。
- 模型 revision、环境、随机种子、指标、统计和资源预算冻结。
- 项目需求提出人明确批准 S6.1-P1 及后续相应阶段。

当前 `S6.1-P1-R1 = REVIEW_CANDIDATE / NOT APPROVED / NOT STARTED`、`S6.1-P1 = NOT APPROVED / NOT STARTED`，不得自动进入 Pilot、Dataset Construction、Detector Implementation、Retrieval Intervention Implementation、Training 或 Formal Experiment。

## 15. 结论边界

- Published Result 仅指外部论文公开结论。
- Reproduced Result 必须来自冻结协议下的成功复现；当前无完整严格复现。
- Engineering Validation 可说明身份、schema、环境、固定输入、证据闭环和 smoke，不说明论文效果。
- Our Formal Result 当前为 `NONE`；`FORMAL_EXPERIMENT = NOT STARTED`。
- S6-T5 只证明受控检索到上下文的工程基线，不证明 RAG 安全或隐蔽污染检测。

## 16. 风险与缓解

| 风险 | 缓解原则 |
| --- | --- |
| 外部依赖与模型供应链不稳定 | 固定 commit/revision，离线包与 5090 独立验证分离 |
| 基线任务不等价 | 明确角色和可比类别，不强行合并指标 |
| 标签或 Ground Truth 泄漏 | 对全部 retriever 可见字符串递归扫描并设置失败关闭测试 |
| 工程 smoke 被误写为论文结果 | 使用四类结果与 claims matrix |
| 中文版本数据真实性与许可风险 | 建立来源、版本、权威和再分发登记 |
| Option B 被扩张成完整可信检索或 Agent 防御 | 只允许 hard filtering / soft downweighting；超出能力保留给 Paper 2 或后续研究 |

## 17. 方案变更记录

| Change ID | 日期 | 原方案 | 新方案 | 变更原因 | 用户确认 | 影响阶段 | Commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RPC-001 | 2026-07 | 广义 Stage 6 RAG 方向 | Paper-first 中文版本化隐蔽知识污染 | 聚焦可发表问题与可比较证据 | 是 | S6.1-LR1+ | `1294632ca0501e7b999a29383780bec49eaa6b04` |
| RPC-002 | 2026-08-01 | `paper1_research_route.md` 同时承担当前方案入口 | 本文件成为唯一当前方案权威；原路线降级为历史与支撑材料 | 建立单一职责和 Human/LLM 分离 | 是 | Paper 1 全局 | 本次文档重构提交 |
| RPC-003 | 2026-08-01 | 英文工作题目 | 登记最新中文题目，同时保持当前已接受技术范围 | 反映项目需求提出人题目意图 | 是；技术范围待确认 | Paper 1 全局 | 本次文档重构提交 |
| RPC-004 | 2026-08-02 | W2 等待人工决定 | W2/FU1 以单样本 detection-core 工程可行性范围验收关闭；P1 仅形成非权威协议候选 | 前置工程门已满足，但科学结论与正式实验仍需独立协议和审批 | 是；解毒 A/B/C 待确认 | FU1 closure / P1 candidate | PODR-061；本次提交 |
| RPC-005 | 2026-08-02 | 解毒 A/B/C 待确认、旧 P1 合同候选 | 选择 Option B；Paper 1 冻结为检测与轻量 hard filtering/soft downweighting，并形成审批级 P1-R1 强化候选 | 使题目中的“解毒”具有可证伪、可预算和不扩张的技术边界 | 是；OR-021 / PODR-062 | S6.1-P1-R1 review gate | 本次提交 |

历史与支撑路线：[paper1_research_route.md](../paper1_research_route.md)，其 `Document Role = HISTORICAL_AND_SUPPORTING_RESEARCH_ROUTE`，不能覆盖本文件。
