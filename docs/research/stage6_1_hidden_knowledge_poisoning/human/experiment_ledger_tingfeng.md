# Paper 1 人类可读实验总规划与实验总账

## Human-readable Research Plan & Experiment Ledger

Document Role = `PAPER1_PRIMARY_HUMAN_ENTRY`<br>
Audience = `项目负责人 / 导师与领导 / 新团队成员`<br>
Reading Path = `5 minutes / 15 minutes / 30 minutes`<br>
Current Evidence Cut = `Quality Convergence / Pilot4 Owner acceptance review pending`<br>
Last Updated = `2026-09-01`

> 这是一张“项目地图”，不是 raw evidence，也不产生新授权。读完第 0 节可掌握当前状态；读到第 8 节可理解论文方法；
> 读完第 19 节可进入项目工作。精确状态、协议、决定和证据分别通过链接下钻。

## 0. 先看这里：5 分钟了解 Paper 1

| 问题 | 当前回答 |
| --- | --- |
| 中文论文题目 | 《面向中文检索增强生成系统的版本感知隐蔽知识污染基准与多视角解毒方法》 |
| 英文论文题目 | *Stealthy Factual Poisoning in Versioned RAG Knowledge Bases: A Benchmark and Multi-View Detection Framework* |
| 一句话研究问题 | 在版本、时间和来源关系复杂的中文知识库里，如何识别“语言自然、检索相关、事实却被悄悄改变”的内容，同时不误伤合法旧版本和正常更新？ |
| 一句话核心方法 | 构建 Clean–Poison–Hard Negative 匹配数据，用 Semantic、Entity-Claim、Provenance、Temporal-Version、Retrieval-Behavior 五类互补证据估计风险，再做可校准的过滤或降权。 |
| 当前阶段 | ⏳ Pilot4 数据与标注协议质量收敛完成，等待项目负责人 acceptance review；仍是预标注阶段。 |
| 当前任务 | `S6.1-P1-PILOT4-PREANNOTATION-QUALITY-CONVERGENCE-01`：真实来源、全量语义与 Schema V3 收敛。 |
| 当前完成度 | ✅ `S6.1-P1-R1 = HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK`，Pilot0–2 可行性门完成；🧪 Pilot3 信号诊断完成；🔧 Pilot4 72/72、64 个来源单元、Schema V3 与三个 dry-run workbook 已准备；正式数据、Detector 和正式实验均未开始。 |
| 当前唯一人工动作 | 项目负责人审查完整 72-row review、Schema V3 candidate 与三个 `ANNOTATOR_DRY_RUN_ONLY` 工作簿。 |
| 当前主要 blocker | ⏳ Owner acceptance 尚未给出；因此不能发 A/B，更不能进入 240-group。 |
| 已经可以说什么 | Pilot4 的 72 条候选通过全量语义/可见性 QA，64 个实际官方来源证据单元完成字节/摘录 hash 与锚点验证；这仍不代表人工有效性。 |
| 绝对不能说什么 | 不得说 Pilot4 已接受、A/B 已开始、72 条已有 Ground Truth、240-group 已生成、Dataset 已冻结、Formal Detector 已实现、检测有效或 Paper Result 已形成。 |

当前实验状态固定为：

`PILOT4_QUALITY_CONVERGED / READY_FOR_OWNER_ACCEPTANCE_REVIEW / NO_HUMAN_DISTRIBUTION`

保留的历史状态链：`PILOT4_BALANCED_SET_REPAIRED / READY_FOR_SECOND_OWNER_PREFLIGHT` →
`PILOT4_FINAL_PREANNOTATION_READY_FOR_OWNER_REVIEW` → 当前 quality-convergence 状态。历史 package 不被覆盖。

状态的动态权威入口是 [Current Work State](../../../governance/current_work_state.md)。

## 1. 项目背景：我们到底在研究什么

RAG（Retrieval-Augmented Generation，检索增强生成）先从知识库找文档，再让生成模型依据这些文档回答。它比只依赖模型
参数更容易更新和审计，但也把安全边界扩展到“谁能写入、替换或伪装知识库内容”。

知识污染（knowledge poisoning）是把错误或恶意内容放进知识库，使它被检索并影响回答。隐蔽知识污染（stealthy
knowledge poisoning）更难：文本语法自然、主题相关、与 query 很相似，错误藏在数值、适用条件、版本时间或来源权威中。

版本化知识库尤其困难，因为“与当前事实不同”不等于“恶意”。旧政策、合法修订、尚未生效条款、地区差异和例外条件
都可能是真实文档。若 Detector 只看语义，它可能把这些内容误判为污染。因此 Paper 1 不只需要 Poison，还必须设计
Hard Negative（困难负例）：表面像污染、实际合法，用来测量误伤。

简化例子：

| 类型 | 候选文本 | 解释 |
| --- | --- | --- |
| Clean | “修订后的职业教育法自 2022 年 5 月 1 日起施行。” | 与当前权威版本一致。 |
| Poison | “修订后的职业教育法自 2022 年 6 月 1 日起施行。” | 语言自然但改变了关键生效日期。 |
| Hard Negative | “原职业教育法自 1996 年 9 月 1 日起施行，后被修订文本替代。” | 描述历史版本，日期不同但不是污染。 |

核心难题不是“找出所有不同”，而是“用版本、时间、来源和检索行为证据区分恶意事实改变与合法差异”。

## 2. 专业术语中英文速查

| 术语 | 中文速解 |
| --- | --- |
| RAG | Retrieval-Augmented Generation；先检索知识，再基于检索内容生成回答。 |
| Benchmark | 基准数据与评估协议；不只是一个文件，还包括切分、标签、指标和可复现合同。 |
| Ground Truth | 经冻结流程确认的参考真值；Pilot-only 真值不等于正式 Benchmark 真值。 |
| Clean | 与权威事实、适用范围和版本状态一致的候选。 |
| Poison | 保持自然和相关性、但实质改变事实状态的候选。 |
| Hard Negative | 看起来可疑但实际合法的困难负例，用于测量误报。 |
| Matched Triplet | 同一事实主体下匹配的 Clean、Poison、Hard Negative 三元组。 |
| Version Chain | 同一主张的前版、现版、修订、废止或替代关系链。 |
| Provenance | 内容来自哪里、如何获取、如何派生的来源链。 |
| Authority | 发布主体的权威身份、层级、管辖范围及其是否支持该命题。 |
| HKP | Hidden Knowledge Poisoning；本项目的四类隐蔽知识污染变异。 |
| Stealth | 隐蔽性；错误需要多大证据成本才能被发现。 |
| S1 / S2 / S3 | S1 本文即可发现；S2 一个直接官方证据可确认；S3 需要跨版本/来源的联合证据链。 |
| Semantic View | 语义视角；观察 query 与候选是否相关、表达是否异常。 |
| Entity-Claim View | 实体—主张视角；观察主体、属性、数值、条件等关系。 |
| Provenance View | 来源视角；观察发布者、引用链和权威匹配。 |
| Temporal-Version View | 时间—版本视角；观察生效、失效、修订、替代与版本顺序。 |
| Retrieval-Behavior View | 检索行为视角；观察排名、邻域和扰动下的检索稳定性。 |
| Signal | 某一视角输出的结构化诊断证据或分数，不等于最终预测。 |
| Detector | 将允许的多视角输入融合成污染判断或风险分数的检测器。 |
| Risk Score | 候选为污染的风险估计，需经过校准才能用于阈值决策。 |
| Calibration | 让预测分数与实际风险概率/阈值行为相符。 |
| FPR | False Positive Rate；把真实非污染误报为污染的比例。 |
| Recall | 在真实污染中成功检出的比例。 |
| Precision | 被判为污染的样本中真正是污染的比例。 |
| AUROC | 不同阈值下真阳性率与假阳性率权衡的面积；类别极不平衡时需结合 AUPRC。 |
| AUPRC | Precision–Recall 曲线面积；更直接反映低污染率下的检出质量。 |
| Poisoned@K | Top-K 中污染文档的暴露数量或比例，越低越好。 |
| Recall@K | Top-K 是否保留相关正常文档，越高越好。 |
| MRR | Mean Reciprocal Rank；首个相关结果排名的倒数均值。 |
| nDCG | Normalized Discounted Cumulative Gain；考虑相关性等级和位置的排序质量。 |
| Ablation | 消融实验；删除一个视角或训练设计，测量其独立贡献。 |
| Generalization | 泛化；在未见攻击、领域、版本模式或来源上的表现。 |
| Adaptive Attack | 知道防御规则后主动规避检测的攻击。 |
| Hard Filtering | 风险超过阈值时直接从候选集合移除。 |
| Soft Downweighting | 不直接删除，而按风险降低检索分数。 |
| Dataset Freeze | 数据身份、标签、切分、许可与 hash 被正式锁定，之后不能任意调整。 |
| Formal Experiment | 在冻结协议、数据、代码、参数和统计计划下执行的正式实验。 |

## 3. Paper 1 最终要证明什么

以下是科研证据链，不是已完成结论。`PILOT_SUPPORTED` 只表示 Pilot 提供了可行性或失败模式证据。

| # | 最终主张 | 当前证据状态 | 当前解释 |
| --- | --- | --- | --- |
| 1 | 中文版本化 RAG 存在难被简单语义相似度识别的隐蔽事实污染。 | `PILOT_SUPPORTED` | Pilot3 显示语义/时间诊断信号很弱，支持“问题值得研究”，不构成总体性能结论。 |
| 2 | 可构建含 Clean、Poison、Hard Negative、版本链、权威关系和 S1–S3 的中文 Benchmark。 | `PILOT_SUPPORTED` | Pilot1–4 支持来源、标注和构造可行性；Formal Benchmark 尚未冻结。 |
| 3 | Semantic-only 不足，且容易把合法历史版本误判为污染。 | `PILOT_SUPPORTED` | Pilot3 暴露 HN 误报与弱语义信号；尚无正式对照统计。 |
| 4 | Entity-Claim、Provenance、Temporal-Version、Retrieval-Behavior 提供互补证据。 | `PILOT_SUPPORTED` | 五视角信号可运行，结构化 Temporal/Provenance prototype 已实现；互补收益尚未正式建立。 |
| 5 | Multi-view 方法更可靠地区分真实污染与合法版本差异。 | `NOT YET ESTABLISHED` | Formal Detector 未实现，组合矩阵和正式 test 尚未冻结。 |
| 6 | calibrated risk 的过滤/降权降低污染暴露并保持正常检索效用。 | `NOT YET ESTABLISHED` | Option B 合同与工程 primitive 存在，但 effectiveness 未建立。 |

目前没有任何一项处于 `FORMALLY ESTABLISHED`。正式建立必须满足第 18 节的全部条件。

## 4. Benchmark 总体设计

### 4.1 正式五领域

`PAPER1_FORMAL_DOMAIN_SET = OWNER_CONFIRMED`

| ID | 中文领域 | English |
| --- | --- | --- |
| D1 | 企业人力资源 | Enterprise Human Resources / Enterprise HR |
| D2 | 财务 | Finance |
| D3 | 信息安全 | Information Security |
| D4 | 采购与研发 | Procurement and R&D |
| D5 | 教育与科研 | Education and Research |

这五个领域只用于未来 Scale Pilot / Formal Benchmark 规划。Pilot4 实际覆盖四领域，这是不可回写的历史事实。

### 4.2 HKP 与隐蔽等级

| 类型 | 含义 |
| --- | --- |
| HKP1 | 数值或实体被改变。 |
| HKP2 | 适用条件、例外或否定关系被改变。 |
| HKP3 | 生效、失效、废止、替代或版本顺序被改变。 |
| HKP4 | 来源、权威层级、机构归属或引用关系被伪装。 |

- S1：候选自身、内部矛盾、明显时间逻辑或普通常识即可发现事实错误。
- S2：候选本身自然，但一个直接官方来源或同一文件的直接上下文即可确认错误；“打开一个官方页面”不等于跨文档。
- S3：必须依赖多个版本、文档、来源、时间演化、authority chain 或 provenance chain 联合确认。
- 正确候选不评价 S1/S2/S3，而是 `NOT_APPLICABLE`；证据不足时为 `UNCERTAIN`。

### 4.3 Scale Pilot 结构

`5 Domains × 4 HKP × 3 Stealth × 4 Independent Chains = 240 independent groups`

- ✅ `STRUCTURE CONFIRMED`
- 📌 `EXECUTION NOT STARTED`
- 📌 `FORMAL DATASET NOT FROZEN`

若每组生成 Clean + Poison + matched Hard Negative，则约为 `240 × 3 = 720 candidate records`。这个 720 是
`PLANNED DERIVED SIZE / NOT FROZEN / NOT GENERATED`，不是当前数据事实。

## 5. Clean / Poison / Hard Negative

Clean 是正确对照，Poison 是实质事实被改变的攻击候选，Hard Negative 是“像污染但合法”的压力测试。三者应在同一主体、
主张、长度和检索相关度上尽量匹配，避免模型靠格式或主题捷径分类。

Hard Negative 是 Paper 1 的核心，因为真实版本库里最危险的错误不是漏掉明显 Poison，而是把历史、修订、例外或转载
全部删除。关键子类包括：

- `legitimate historical version`：合法历史版本；
- `legitimate update`：合法更新；
- `legitimate exception`：合法例外；
- `scope difference`：地区、部门、对象或条件范围不同；
- `authority repost`：权威来源的合法转载或转发；
- `near-miss-but-true`：表达极像错误，但细节仍为真。

因此 Hard Negative FPR 既是数据质量指标，也是方法是否可部署的关键指标。

## 6. 五视角方法

| View | 中文名称 | 输入 | 主要看什么 | 主要覆盖 | 可能失败 | 当前实现状态 |
| --- | --- | --- | --- | --- | --- | --- |
| Semantic | 语义视角 | query、候选文本、允许的语义特征 | 相关性、局部异常、语义偏移 | 全部 HKP 的表层信号 | 自然改写、合法旧版与污染都可能很相似 | `METHOD CONTRACT ACCEPTED`; `DIAGNOSTIC PROTOTYPE`; 非 Formal Detector |
| Entity-Claim | 实体—主张视角 | 主体、谓词、对象、数值、条件 | 哪个事实槽位发生变化 | HKP1、HKP2 | claim extraction 错误、隐含主体 | `METHOD CONTRACT ACCEPTED`; Pilot3 diagnostic |
| Provenance | 来源视角 | source、issuer、authority、引用关系 | 谁发布、是否匹配命题、来源链是否可信 | HKP4 | 来源信息缺失；Pilot3 中 35/36 为 N/A | `STRUCTURED PROTOTYPE IMPLEMENTED`; engineering only |
| Temporal-Version | 时间—版本视角 | 生效/失效时间、版本关系链 | 旧版、现版、修订与合法历史 | HKP3、部分 HKP2 | 版本链缺失或事实映射不完整 | `STRUCTURED PROTOTYPE IMPLEMENTED`; Pilot3 Temporal AUROC 0.465，仅诊断 |
| Retrieval-Behavior | 检索行为视角 | rank、score、邻域、冻结扰动 | 候选在 Top-K 和邻域中是否异常 | 全部 HKP 的运行时表现 | query 敏感、计算成本、分布漂移 | `METHOD CONTRACT ACCEPTED`; diagnostic primitive |

必须区分三层：

1. `METHOD CONTRACT`：五视角的允许输入、输出和边界已经作为 P1-R1 框架接受；
2. `DIAGNOSTIC PROTOTYPE`：Pilot3/Pilot4 已验证信号接口和部分结构化实现能运行，并暴露失败模式；
3. `FORMAL DETECTOR`：尚未实现，也没有建立 detection effectiveness。

详细方法合同见 [P1-R1 protocol](../s6_1_p1_r1_protocol_review_candidate.md)。

## 7. 多视角组合、消融和泛化

Single View 包括 S / E / P / T / R；Multi-view 可包含 S+E、S+T、E+P+T 和 All-5。组合必须在 formal protocol freeze
前确定，不能查看 test 结果后挑最好组合。

计划消融：minus Semantic、minus Entity、minus Provenance、minus Temporal、minus Retrieval，以及 without Hard Negative
training/calibration。消融回答“哪个组件真正贡献了性能”，也必须如实报告负贡献。

Track C 泛化计划：unseen HKP、unseen domain、unseen version family/pattern、cross-source transfer 和 adaptive attack。
这些都属于 `EXPERIMENTAL PLAN / NOT EXECUTED`。统计比较族、split 和阈值规则见
[P1-R1 protocol](../s6_1_p1_r1_protocol_review_candidate.md)。

## 8. Option B：轻量解毒

```text
Retriever
  -> Top-K
  -> Five-view Detector
  -> calibrated Risk Score
  -> Hard Filtering / Soft Downweighting
  -> New Top-K
```

- Hard Filtering：若 `risk >= tau`，则移除候选。
- Soft Downweighting：`adjusted retrieval score = retrieval score - lambda × risk`。

安全端要看 `Poisoned@K ↓`；效用端要看 `Recall@K / MRR / nDCG` 尽量保持。二者是分开的共同主结果，不能用一个综合
分数掩盖“安全提高但检索失效”。当前仅能说合同和工程 primitive 存在；Option B effectiveness 为
`NOT ESTABLISHED`，也不包含 trusted context package、完整可信上下文构造或端到端 Agent 防御。

## 9. 从开始到投稿：完整实验路线图

| 阶段 | 为什么做 | 主要工作 | 输入 | 输出 | 当前状态 | 结束条件 | 下一 Gate | 详细链接 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S6.1-LR1 | 选清研究路线 | 外部工作与 Paper1 对齐 | 论文/仓库 | 路线与角色 | ✅ 已验收 | Owner 接受 | R0 | [LR1](../stage_process/S6.1-LR1_work_process.md) |
| S6.1-R0 | 先查能否复现 | 代码/环境/工件预检 | 外部 baseline | 工程证据与 blocker | ✅ 带边界验收 | 证据可恢复 | FU1 | [R0](../stage_process/S6.1-R0_work_process.md) |
| S6.1-R0-FU1 | 关闭关键工程门 | 来源、bundle、5090 smoke | 冻结合同 | 单样本工程可行性 | ✅ 已关闭 | Owner 验收 | P1-R1 | [FU1](../stage_process/S6.1-R0-FU1_work_process.md) |
| S6.1-P1-R1 | 把想法变协议 | RQ、数据、方法、统计、Option B | LR1/R0/FU1 | 接受的框架 | ✅ 框架已接受 | 数值参数待 Pilot 冻结 | Pilot | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Pilot0 | 工程合同能否运行 | schema、split、泄漏 guard | synthetic fixture | 工程基础设施 | ✅ 已关闭 | 测试与 Owner 验收 | Pilot1 | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot1 | 真实中文来源能否构建 | 版本链、公开来源、候选包 | 官方公开文档 | 36 条候选与包 | ✅ 已关闭 | 来源/包可行 | Pilot2 | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot2 | 人能否可靠标注 | A/B、V2、agreement、owner 仲裁 | 36 条候选 | 36 条 Pilot-only GT | ✅ 可行性关闭 | GT/协议可唯一生成 | Pilot3 | [Pilot2 closure](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| Pilot3 | 信号能否运行 | 五视角 180 条 SignalRecord | Pilot2 GT | 弱信号/失败模式 | 🧪 已完成并停止 | 诊断报告 | Pilot4 | [Pilot3](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| Pilot4 first preflight | 人工发放前低成本检查 | 24 triplets/72 candidates/12-row sample | lessons + public sources | 首版 package | 📌 历史：退回修复 | Owner 指出缺陷 | targeted repair | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot4 targeted repair | 修复实质缺陷 | 语义、stealth、echo、applicability、独立 QA | 首版与 owner feedback | repaired 72 + second sample | 🔧 已完成 | 修复验证通过 | second preflight | [Current State](../../../governance/current_work_state.md) |
| Pilot4 second Owner preflight | 决定能否发人 | Owner 审查 repaired 12 rows | repaired workbook | PASS 或 targeted repair | ⏳ 当前唯一动作 | Owner 明确决定 | A/B 或修复 | [Current State](../../../governance/current_work_state.md) |
| Pilot4 Repair-02 final preflight | 关闭第二轮系统性缺陷 | Owner 审查 final 16 rows | genuine-S3/S1/length/template/HN evidence | PASS 或 candidate-local correction | ⏳ 当前唯一动作 | Owner 明确决定 | 单独批准 A/B 或局部修正 | [Current State](../../../governance/current_work_state.md) |
| Pilot4 A/B 72 annotation | 获得独立人工判断 | Phase1/2、双锁定 | Owner-accepted package | 四份 returns | 📌 未批准/未开始 | returns hash-lock | agreement | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| Pilot4 agreement | 量化一致性 | 合法子集 agreement | A/B returns | agreement/disagreement | 📌 未开始 | 逻辑/一致性验证 | adjudication | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| Pilot4 adjudication | 解决必要分歧 | Owner 只裁决分歧 | minimal packet | 唯一决定 | 📌 未开始 | residual inconsistency=0 | GT | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot4 72 Ground Truth | 形成小规模参考真值 | 确定性合并与 QA | validated returns/owner decisions | 72 Pilot GT | 📌 未开始 | identity/logic/leakage PASS | re-evaluation | [Experiment Master](../../../governance/experiment_master_record.md) |
| Pilot4 signal re-evaluation | 验证修复方向 | 重新运行 diagnostic signals | 72 Pilot GT | failure-mode comparison | 📌 未开始 | 诊断可解释 | readiness | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Scale Readiness Gate | 防止盲目扩规模 | 六类 readiness 审计 | Pilot4 closure | PASS/blocked | 📌 未开始 | 六类门均 PASS | Owner scale approval | [第17节](#17-什么情况下才能进入-240-group) |
| 240-group Scale Pilot | 验证规模/方差 | 5×4×3×4 groups | approved design | scale pilot data | 📌 未批准/未生成 | coverage/quality PASS | power analysis | [Research Plan](research_plan_authority.md) |
| Power / Precision Analysis | 决定正式样本量 | CI/方差/稀有组精度 | scale pilot | frozen sample plan | 📌 未开始 | 统计精度达标 | formal freeze | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Formal Dataset / Protocol Freeze | 锁定身份与分析计划 | data/split/license/metrics/seeds | accepted scale evidence | frozen contract | 📌 未开始 | Owner 明确批准 | implementation | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Formal Detector Implementation | 实现最终模型 | 五视角融合与校准 | frozen train/dev | executable detector | 📌 未批准/未实现 | tests + frozen identity | evaluation | [Research Plan](research_plan_authority.md) |
| Formal Detector Evaluation | 测主性能 | locked test evaluation | frozen detector/data | primary metrics | 📌 未开始 | evidence complete | multi-view | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Multi-view Evaluation | 验证组合收益 | single/multi-view compare | same split/budget | paired results | 📌 未开始 | preregistered comparisons | ablation | [第7节](#7-多视角组合消融和泛化) |
| Ablation | 解释组件贡献 | leave-one-view-out 等 | full method | contribution evidence | 📌 未开始 | planned family complete | generalization | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Generalization | 测外推能力 | unseen domain/HKP/version/source | held-out families | generalization results | 📌 未开始 | frozen Track C complete | Option B | [第7节](#7-多视角组合消融和泛化) |
| Option B Detoxification | 测安全—效用权衡 | hard filter/soft downweight | calibrated risk | Poisoned@K + utility | 📌 未开始 | co-primary endpoints | paper evaluation | [第8节](#8-option-b轻量解毒) |
| Paper Evaluation | 汇总证据 | 统计、失败、威胁、复现包 | formal runs | tables/figures | 📌 未开始 | claims audit PASS | writing | [第18节](#18-什么情况下才能称为正式论文结果) |
| Paper Writing | 形成论文 | 方法、结果、局限、工件 | accepted formal evidence | manuscript | 📌 未开始 | Owner/导师审查 | submission | [README](../README.md) |

## 10. Pilot0–Pilot4：为什么每一步都需要

### Pilot0：工程合同可不可运行？

Pilot0 用 synthetic fixture 验证 schema、分组切分、泄漏 guard、攻击/Hard Negative 接口和 manifest 是否可执行。它避免在
真实数据上才发现基础设施错误。结论仅是工程基础设施可行。

### Pilot1：真实公开中文版本来源能不能构建？

Pilot1 审计公开中文版本链、来源许可边界和候选构造，形成 36 条非正式候选。它证明公开来源到盲化包的工程可行性，
不证明 Benchmark 已完成。

### Pilot2：人能不能可靠标注并形成 Ground Truth？

Pilot2 经历 schema 适用性、编码、旧值映射、独立复核和 owner 一致性门，最终形成 36 条 Pilot-only Ground Truth。它证明
标注协议与 GT 生成流程可行，也留下了不可回写的失败证据。

### Pilot3：五视角信号是否能运行、失败模式是什么？

Pilot3 在 36 条 Pilot-only GT 上生成 180 条 SignalRecord。它发现类别失衡、S1/S3 collapse、Provenance 35/36 N/A、
Temporal AUROC 0.465 和 Hard Negative 误报等问题。它是 diagnostic smoke，不是 Detector 性能实验。

### Pilot4：扩 240-group 前最后一次小规模校准

Pilot4 把 Pilot1–3 的教训前移到人工发放前：先设计 coverage 和 field schema，再构造并独立验证 24 matched triplets、
72 条平衡候选。首轮 preflight 被退回后只做 targeted repair。当前 repaired 72 仍是 preannotation candidates。

四个规模不能混淆：`36 records = development/diagnostic evidence`；`72 repaired candidates = balanced Pilot/preannotation
candidates`；`240 groups = future Scale Pilot`；`Formal Dataset = 未来经正式 freeze 的数据`。

## 11. 数据标注流程

```text
Candidate Generation
  -> Machine QA
  -> Owner Preflight
  -> A/B Phase1
  -> hash lock both
  -> A/B Phase2
  -> hash lock both
  -> agreement
  -> disagreement-only packet
  -> Owner adjudication
  -> Ground Truth
```

Phase1 评估候选自身可见的自然度、相关性、局部可检测性和隐蔽等级，不提前看到 Phase2 的官方事实材料。Phase2 用官方
来源和版本背景判断事实、版本、历史/更新和权威命题。盲法防止后一阶段答案反向污染第一阶段难度判断；A/B 独立可测量
协议是否清晰。

Owner 只在双方结果锁定后裁决必要分歧。Owner 的目的不是“提高 kappa”，而是形成可审计的唯一最终决定；agreement 必须
保留标注人真实差异。完整规则见
[标注教训与未来数据规则](annotation_lessons_learned_and_future_dataset_rules.md)。

## 12. 数据构造永久规则

- `subject uniqueness = 100%`：法律、政策、制度和标准主体必须可唯一识别。
- 候选与 query 必须 self-contained；不能依赖“该条例”“2017 年版”等隐含上下文。
- coverage before generation：先冻结覆盖矩阵，再生成文本。
- mutation semantic alignment：attack metadata 必须与实际事实变异一致。
- stealth evidence path：S1/S2/S3 必须来自发现错误所需证据路径。
- no evidence echo：候选不能回显标准答案或证据措辞。
- no experimental meta-language：候选不能出现“本样本”“对照组”等实验语言。
- applicability 必须 claim-derived，不能由生成器意图直接声明。
- `Generator != Validator`：构造者声明 PASS 不等于独立验证。
- G1–G14 全部门禁必须对序列化产物重新计算。
- independent Round D 必须从 source fact 反向核验。
- semantic near-duplicate 必须区分 triplet 内匹配与跨独立组泄漏。
- label isolation：Ground Truth/attack ID 不得进入 retriever 或 inference feature。
- raw return immutable：人工原始 return 不回写；纠正必须追加绑定。

唯一完整规则见 [canonical lessons](annotation_lessons_learned_and_future_dataset_rules.md)。

## 13. 已发生 Blocker 时间线

| 日期 | 阶段 | Blocker | 问题是什么 / 为什么重要 | 解决方案 | 状态 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07-31 | R0 | evidence mismatch | 首次 Worker evidence 与声明不匹配，无法复核 | corrected evidence + 本机 control-plane review | ✅ RESOLVED | [R0 process](../stage_process/S6.1-R0_work_process.md) |
| 2026-08-01 | W2 | model download/evidence blockers | 模型下载失败、磁盘命令来源不完整 | additive correction、offline bundle、H2 resume02 | ✅ `CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED`（仅工程门） | [FU1 process](../stage_process/S6.1-R0-FU1_work_process.md) |
| 2026-08-27 | Pilot2 | distribution metadata issue | 登记时间错误曾导出盲法污染推断 | 保留原记录，追加 owner-confirmed actual order | ✅ RESOLVED / 元数据历史保留 | [Owner correction](../s6_1_p1_pilot2_return_owner_correction.md) |
| 2026-08-27 | Pilot2 | Schema V1 ambiguity | YES/NO/UNCERTAIN、适用性和 authority 命题歧义 | Schema V2 + 独立复核 | ✅ RESOLVED | [Schema V2](../s6_1_p1_pilot2_annotation_v2.md) |
| 2026-08-27 | Pilot2 | NOT_APPLICABLE 缺失 | 正确或不适用命题被迫填错误枚举 | present/correctness dependency | ✅ RESOLVED | [Schema V2](../s6_1_p1_pilot2_annotation_v2.md) |
| 2026-08-27 | Pilot2 | encoding/header/process metadata | GB18030、列名和过程字段影响导入 | UTF-8 BOM 合同与缺陷显式保留 | ✅ RESOLVED | [Targeted review](../s6_1_p1_pilot2_targeted_rereview.md) |
| 2026-08-28 | Pilot2 | V1 mapping defect | 带中文后缀列未识别，旧值被伪装成 absent | allowlisted alias + fail closed | ✅ RESOLVED | [Targeted review](../s6_1_p1_pilot2_targeted_rereview.md) |
| 2026-08-28 | Future data | candidate subject ambiguity | 裸指代使样本缺上下文 | `BROKEN_CANDIDATE / MISSING_CONTEXT` 门 | ✅ RESOLVED AS PERMANENT RULE | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| 2026-08-31 | Pilot2 | agreement disagreements | 47 条 A/B 分歧 + 37 条内部逻辑冲突 | disagreement-only owner packet | ✅ RESOLVED | [Post annotation](../s6_1_p1_pilot2_post_annotation.md) |
| 2026-08-31 | Pilot2 | owner consistency blocker | 4 个候选有非法枚举/同字段冲突 | 独立 owner correction record | ✅ RESOLVED | [Closure](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| 2026-08-31 | Pilot3 | class imbalance | Clean 仅 1 条，无法支持正式估计 | Pilot4 平衡为 24/24/24 intent | ✅ RESOLVED FOR PILOT4 DESIGN | [Pilot3](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| 2026-08-31 | Pilot3 | S1/S3 collapse | 隐蔽等级证据路径不充分 | Pilot4 evidence-path stealth contract | ✅ RESOLVED FOR GENERATION | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| 2026-08-31 | Pilot3 | Provenance 35/36 N/A | 来源命题覆盖不足，视角不可估 | Pilot4 claim-derived applicability/coverage | 🔧 ENGINEERING REPAIR; formal effect open | [Pilot3](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| 2026-08-31 | Pilot3 | Temporal AUROC weak | 诊断 AUROC 0.465 | structured temporal/version repair | 🔧 PROTOTYPE REPAIRED; effectiveness open | [Pilot3](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| 2026-08-31 | Pilot3 | HN FP | 合法版本差异产生误报 | 六类 HN 与结构化调整 | 🔧 DESIGN REPAIRED; formal effect open | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| 2026-09-01 | Pilot4 | attack metadata misalignment | metadata 与实际变异可能不一致 | mutation-semantic contract + rejection | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | stealth index assignment | S 值由目标格赋值而非证据路径推导 | evidence-path derivation | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | evidence echo | LONG 候选回显答案/证据 | natural rendering + echo blocker | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | experimental meta-language | 文本含实验描述，形成捷径 | meta-language rejection | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | applicability metadata | 适用性由 metadata 意图而非 claim 推导 | claim-derived applicability | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | builder-declared PASS | 构造器自报通过，未验证序列化产物 | independent G1–G14 + Round D | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | HN evidence weakness | 困难负例证据链过弱 | source-fact reverse check | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | Repair-01 acceptance | 第二次预审发现 S3 necessity、S1 cue、实际长度、模板与 HN 语义问题 | Repair-02 | ✅ SUPERSEDED BY FINAL REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | final preannotation acceptance | Repair-02 工程门完成但尚无人工作出接受决定 | quality convergence | ✅ SUPERSEDED BY FULL QUALITY GATES | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | source/schema/visibility convergence | Phase1 hint、人工跨文档、伪来源核验、HN 支持与字段可操作性存在系统性风险 | actual-source verification + Schema V3 + full72 + dry-run | ⏳ READY FOR OWNER ACCEPTANCE REVIEW | [Current State](../../../governance/current_work_state.md) |

## 14. 当前项目状态

- `PILOT4_QUALITY_CONVERGED / READY_FOR_OWNER_ACCEPTANCE_REVIEW`
- `PREANNOTATION_ONLY`
- `NO_HUMAN_DISTRIBUTION`
- 72 repaired candidates 已存在；仍非 Ground Truth、非 Formal Benchmark、非 frozen Dataset。
- class intent 为 Clean / Poison / Hard Negative = `24/24/24`。
- 生成覆盖为 `4 HKP × 3 intended-S × 2 replication = 24 poison cells`，对应 24 matched triplets。
- 完整 72-row review、Schema V3 candidate 与三个 dry-run workbook 正在等待人工审查。
- A/B 未开始；72 Ground Truth 未建立；240-group 未开始；Dataset = `NOT FROZEN`（未冻结）。
- Formal Detector = `NOT IMPLEMENTED`（未实现）；Formal Experiment = `NOT STARTED`（未开始）；Our Method Result = `NONE`。

当前 Git 身份与远端同步状态必须动态核验；`a843697`、`cad3b2b2` 与 `871aecf` 均作为不可变历史身份保留。

## 15. 当前下一步

唯一当前动作：**Owner reviews full 72-row Pilot4 quality artifact, Schema V3 candidate and three dry-run workbooks**。

```text
Owner Quality Acceptance Review
  ├─ PASS
  │    -> 另行决定是否批准 A/B 72 annotation（不会自动开始）
  └─ FAIL
       -> 登记具体 blocker；同 root cause 连续重现则 ROOT_CAUSE_REPAIR_FAILURE 并停止

未来在独立审批下：
A/B -> agreement -> adjudication -> 72 GT
    -> signal re-evaluation -> Scale Readiness
    -> Owner 单独批准 -> 240-group
```

## 16. 论文实验指标

### Detection

- AUPRC：在污染稀少、类别不平衡时，比总体 accuracy 或单独 AUROC 更直接反映“检出的污染有多少是真的”。
- AUROC：看全阈值排序能力，但必须与 prevalence、AUPRC 和低 FPR 指标一起解释。
- Recall@1% FPR：只允许 1% 正常样本被误报时能找回多少污染；真实系统中低误报非常重要。
- Hard Negative FPR：合法历史/更新/例外被误杀的比例，是 Paper 1 的关键指标。
- F1：Precision 与 Recall 的调和平均；依赖阈值和 prevalence。
- Calibration：风险分数是否能支持可解释的阈值决策。

### Retrieval

- Poisoned@K：Top-K 中污染暴露，越低越好。
- Recall@K：相关正常内容是否仍被保留。
- MRR：首个相关结果是否靠前。
- nDCG：多等级相关结果的整体排序质量。

详细统计、配对比较、CI、Holm correction 和主要终点见
[P1-R1 protocol](../s6_1_p1_r1_protocol_review_candidate.md)。

## 17. 什么情况下才能进入 240-group

Scale Readiness Gate 必须至少同时通过六类检查：

| 类别 | 必须回答 |
| --- | --- |
| DATA | Pilot4 72 候选/GT 的平衡、自包含、匹配和失败模式是否支持扩规模？ |
| ANNOTATION | A/B 流程、适用性、agreement 和 owner 仲裁是否可重复且成本可控？ |
| SIGNALS | 五视角 signal 是否有足够覆盖、方向正确、缺失机制可解释？ |
| LEAKAGE | exact/normalized/semantic/template/entity/version/label leakage 是否 fail closed？ |
| SOURCE | 五领域来源、版本链、许可与发布策略是否可追溯？ |
| METHOD | Formal Detector 的输入、融合、校准、baseline fairness 和资源计划是否可冻结？ |

Pilot4 PASS 只关闭小规模校准门，**不自动启动 240-group**。Scale Readiness PASS 后仍需 Owner 单独批准。

## 18. 什么情况下才能称为正式论文结果

| 层级 | 能说明什么 | 不能说明什么 |
| --- | --- | --- |
| Engineering Validation | 代码、schema、环境、接口或证据链能运行 | 方法有效、可泛化 |
| Pilot Diagnostic | 小样本暴露方向、失败模式和协议问题 | 总体性能、最终论文数字 |
| Scale Pilot | 估计方差、样本量、覆盖和资源 | 正式 test 结论，除非协议明确规定 |
| Formal Experiment | 冻结数据/代码/参数/统计计划下的结果 | 未经 claims audit 的论文主张 |
| Paper Result | 通过证据、统计、复现和结论边界审计的正式结果 | 超出协议和数据支持的 SOTA/生产安全承诺 |

例如 Pilot3 Temporal AUROC `0.465` 只能写成“小样本诊断暴露弱时间信号”，不能写成 Paper 1 最终性能。正式论文结果
至少要求 Dataset/Protocol Freeze、正式 Detector 身份、预注册比较、locked test、统计不确定性、失败处理、完整 evidence
index 和 Owner 对 claims 的接受。

## 19. 文件导航：想了解更多应该看哪里

| 我想看什么 | 应该打开哪个文件 |
| --- | --- |
| 5/15/30 分钟掌握 Paper 1 | 本文件 |
| 目录总入口与文件分类 | [Paper 1 README](../README.md) |
| 当前研究方向与边界 | [Research Plan Authority](research_plan_authority.md) |
| 详细实验协议、RQ、指标和统计 | [P1-R1 protocol](../s6_1_p1_r1_protocol_review_candidate.md) |
| 数据标注经验与未来规则 | [Annotation Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| Pilot 实际过程 | [S6.1-P1 Work Process](../stage_process/S6.1-P1_work_process.md) |
| 当前正在做什么/禁止什么 | [Current Work State](../../../governance/current_work_state.md) |
| Owner 已确认决定 | [Project Owner Decision Register](../../../governance/project_owner_decision_register.md) |
| 实验控制面与证据索引 | [Experiment Master Record](../../../governance/experiment_master_record.md) |
| 按时间查看执行历史 | [Research Execution Log](../../../governance/research_execution_log.md) |
| AI/Codex 结构化恢复上下文 | [Agent Experiment Ledger](../agent/experiment_ledger_agentUse.md) |
| 人类/机器/证据如何分层 | [Documentation Separation Contract](../documentation_separation_contract.md) |
| 为什么本轮不移动文件 | [Document Inventory](../document_inventory.md) |

> STOP：Repair-02 只准备最终 16-row Owner review；不接受 Pilot4，不分发 A/B，不启动 240-group、Detector、训练、5090 或 Formal Experiment。
