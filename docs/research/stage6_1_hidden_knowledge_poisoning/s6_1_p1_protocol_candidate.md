# S6.1-P1 正式实验协议与 Benchmark 规格候选

Document Role = `P1_PROTOCOL_DESIGN_CANDIDATE`  
Authority = `NON_CANONICAL_CANDIDATE`  
Status = `CONTRACT_CANDIDATE / NOT APPROVED / NOT STARTED`  
Primary Authority = [human/research_plan_authority.md](human/research_plan_authority.md)  
Owner Gate = `HUMAN_DECISION_REQUIRED_BEFORE_P1_APPROVAL`

> 本文只供项目需求提出人审查。它不批准 P1，不冻结 Dataset，不实现 Detector，不启动训练或正式实验，也不能覆盖研究方案权威文件。

## 1. 候选目标与边界

候选任务名为 **Paper 1 Formal Experimental Protocol and Benchmark Specification（Paper 1 正式实验协议与 Benchmark 规格设计）**。P1 若后续获批，首先解决 Research Questions、假设、Benchmark schema、攻击与 hard negative 构造、数据隔离、实验 Track、公平比较、指标、统计、消融、运行证据、资源、许可和论文声明边界。

当前状态：`S6.1-P1 = NOT APPROVED / NOT STARTED`；`Dataset = NOT FROZEN`；`Detector = NOT IMPLEMENTED`；`Training = NOT STARTED`；`Our Method Result = NONE`；`Formal Experiment = NOT STARTED`。

## 2. Research Questions 候选

- RQ1：现有通用语义检测方法能否识别中文 RAG 中自然、主题一致且高检索相关的隐蔽事实污染？
- RQ2：加入实体—主张、来源和时间—版本信号后，是否能够提高受控低误报条件下的检测召回率？
- RQ3：版本感知信号能否区分真正污染与合法更新、历史版本、例外条件及跨部门差异？
- RQ4：多视角方法能否跨攻击类型、隐蔽等级和应用领域泛化？
- RQ5：不同视角对最终检测效果的独立贡献和交互作用是什么？

这些问题仅为 `P1_PROTOCOL_CANDIDATE`。相应零假设、备择假设、主要终点、比较方向和可证伪条件须在 P1 获批前逐项冻结。

## 3. Benchmark 候选

### 3.1 领域、攻击与隐蔽等级

- 领域：企业人力资源、财务、信息安全、采购与研发、教育与科研。
- HKP-1：数值或实体污染。
- HKP-2：条件或例外污染。
- HKP-3：时间或版本污染。
- HKP-4：来源或权威伪装。
- S1、S2、S3：从局部可察觉到需跨文档或版本证据判断的三级隐蔽等级；正式判定规则仍待冻结。

### 3.2 Hard Negative

候选类型为：合法新版本、被废止的历史版本、尚未生效版本、例外条件、地区差异、部门差异、权威来源冲突、同名实体、时间范围不同、无害格式或措辞变化。

### 3.3 版本链 schema

候选字段：`document_id`、`entity_id`、`claim_id`、`version_id`、`predecessor_id`、`successor_id`、`effective_at`、`expires_at`、`repealed_at`、`supersedes`、`amends`、`authority_level`、`jurisdiction`、`department`、`exception_scope`、`provenance`、`label`、`attack_type`、`stealth_level`。

数据划分必须控制实体、模板、来源、时间与版本链泄漏。Ground Truth、`label`、`attack_type`、`stealth_level` 和 evaluator-only 注释不得进入 retriever/detector 可见正文、metadata、embedding input 或 fingerprint。当前不得构建真实 Dataset。

## 4. 方法候选

五视角保持不变：Semantic View、Entity-Claim View、Provenance View、Temporal-Version View、Retrieval-Behavior View。全部状态均为 `PLANNED / NOT IMPLEMENTED`。

P1 只设计各视角的允许输入、输出、特征边界、训练/推理接口、风险聚合与消融关系；不得实现模型、特征提取器、过滤器或可信上下文链。

## 5. 实验 Track 与公平性

- Track A：外部 baseline 与公开 Benchmark；先判定 strict-comparison eligibility，再冻结可比配置。
- Track B：中文版本化 Benchmark；覆盖 HKP-1 至 HKP-4、S1 至 S3 与全部 hard negatives。
- Track C：跨攻击、跨领域和 unseen/adaptive 条件的 transfer evaluation。

Strict comparison 与 transfer evaluation 必须分表、分配置、分结论报告。Baseline 必须使用可追溯 commit/model/data/config，给予等价输入、调参预算和资源约束；无法等价时标记 `NON_STRICT_COMPARISON`，不得借迁移结果声称复现或优越性。

## 6. 指标候选

主要 detector 指标：AUPRC、F1 at frozen threshold、Recall at controlled FPR；AUROC 为次要指标。必须同时报告每攻击类型、每隐蔽等级、每领域、Hard Negative FPR、版本差异误报率、calibration、inference latency 和 memory usage。

如研究检索与攻击链，retrieval hit、poisoned retrieval rate、filtering rate、downstream ASR 必须作为独立链路指标报告，不得混入纯 detector comparison，也不得用它们替代 detector 指标。

## 7. 统计协议候选

- 不少于 5 个随机种子；报告 95% confidence interval。
- 使用 bootstrap；优先 paired comparison；报告 effect size。
- 多重比较使用 Holm correction。
- threshold 在 test 前冻结，禁止在 test set 调参。
- 按攻击类型、领域和隐蔽等级分层报告。
- 所有失败运行和无效运行原样保留并说明排除规则，不得只保留成功种子。

正式样本量、bootstrap 次数、FPR 水平、主要比较族和效应量形式仍须在批准前冻结；本文不生成结果。

## 8. Ablation、Generalization 与运行证据候选

候选消融包括单视角、移除时间/来源信号、风险聚合、hard negative 训练策略及视角交互；泛化包括跨 HKP、跨 S 等级、跨领域、unseen attack 和 adaptive attack。每个 run manifest 至少绑定 run ID、Git SHA、数据快照/schema、split、模型 revision、环境 hash、参数、seed、threshold、资源、起止状态、退出码、结果文件和证据索引。

Evidence contract 必须保存失败/无效运行、原始与派生结果分离、hash/index、环境 pre/post、资源测量、声明分类和私有工件边界。不得把 W2 单样本 smoke 纳入正式指标分母。

## 9. 资源、准入与发布边界

P1 批准前须冻结数据规模、运行矩阵、GPU/RAM/VRAM/disk/time ceiling、停止条件和超限升级规则。正式实验准入至少要求：协议获 owner 明确批准；Dataset/schema/split/label isolation 与许可证状态冻结；baseline 可比类别冻结；模型、环境、参数、阈值、seed、指标和统计冻结；run/evidence contract 可执行；资源获批。

代码访问、内部复现和再分发分别判断。发布前逐项登记源码、数据、模型及派生工件许可证；私有 query/document、原始证据、模型 bundle 和受限工件不得因论文提交自动公开。

## 10. “解毒方法”互斥范围选项

`TITLE_INTENT = CONFIRMED`；`DETOXIFICATION_TECHNICAL_SCOPE = SCOPE_CONFIRMATION_REQUIRED`。

| 选项 | 定义 | Paper 1 范围 | 创新性 | 实验量 | Paper 2 边界 | 投稿风险 | 工程复杂度 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Option A | 只含风险检测、信号解释和人工处置建议 | 最窄，聚焦 Benchmark + Detector + Explanation | 依赖版本感知 Benchmark 与多视角检测贡献 | 最低，主实验/消融/泛化仍需完整 | 自动干预与可信检索完整留给 Paper 2 | 容易被追问“解毒”是否名实相符，但主张最易守住 | 最低 |
| Option B | 检测后自动过滤或降权，不含可信上下文包 | 增加 intervention 与 utility 边界 | 可展示检测到检索干预的闭环 | 中等，增加阈值、utility、过滤/降权与 downstream 对照 | 可信上下文构建仍留给 Paper 2 | 需证明干预收益且不过度过滤，比较口径更复杂 | 中等 |
| Option C | 检测、过滤、重排和可信上下文构建 | 最宽，接近端到端解毒系统 | 系统完整性最高，但贡献容易分散 | 最高，需 detector、retrieval、context、downstream 全链和更多消融 | 与 Paper 2 的可信检索边界显著重叠 | 范围膨胀、复现负担与审稿攻击面最高 | 最高 |

三个选项互斥，本轮不推荐、不选择、不据题目措辞默认扩展。`HUMAN_DECISION_REQUIRED_BEFORE_P1_APPROVAL`。

## 11. 论文结论边界

W2 的唯一可接受结论是 `FROZEN_SINGLE_SAMPLE_DETECTION_CORE_ENGINEERING_FEASIBILITY_ONLY`。`GMTP_REPRODUCTION = NOT ESTABLISHED`；`DETECTION_EFFECTIVENESS = NOT ESTABLISHED`；`STRICT_BASELINE_COMPARISON = NOT ESTABLISHED`；`FORMAL_PAPER_RESULT = NONE`。任何 P1 正式结论只能来自未来获批、冻结、执行并验收的正式实验。

