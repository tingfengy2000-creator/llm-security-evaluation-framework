# Paper 1 标注经验与未来数据规则

文档职责：**未来数据集与人工发放前质量门唯一权威文件**。
适用范围：Pilot3 之后所有候选生成、标注字段设计、人工发放前检查和未来数据集工作。
前瞻边界：Pilot1/Pilot2 已冻结的原始证据和历史候选保持不变。

## 一、构造前强制阅读顺序

未来任何 Paper 1 数据构造任务都必须先读本文，再设计覆盖矩阵、字段或候选。固定顺序为：覆盖矩阵设计 → 字段
质量门 → 候选构造 → G1–G14 准入 → 四轮机器检查 → 项目负责人预检 → 另行批准人工发放。不得让标注人替研究者
发现本可在机器阶段发现的设计缺陷。

## 二、Pilot 暴露的问题

- Pilot2 试验性真值候选中 Clean 为 1、Poison 为 12、Hard Negative 为 23，类别严重失衡。
- 人工隐蔽等级 S1 为 0、S2 为 12、S3 为 0、不适用为 24；生成意图不是人工真值。
- 来源机关视角仅 1/36 可用，因为多数候选没有提出制定机关命题。
- 时序版本视角的描述性 AUROC 约为 0.465；年份词与文本重叠不能代替版本推理。
- Hard Negative 误报共 46 个候选×视角事件：语义 23、实体命题 15、时序版本 8。
- 合法历史、合法更新、例外、范围差异和相近但正确的数值或实体必须被主动覆盖。

## 三、标注字段经验与永久质量门

V1 缺少不适用值，YES/NO/UNCERTAIN 没有操作化，“没有提到”被不同标注人编码成不同值。冻结规则是：适用性字段
为 NO 时，依赖它的正确性字段必须为不适用；命题是否存在和命题是否正确不得混合。

任何新增或变更字段必须通过 `ANNOTATION_FIELD_SCHEMA_GATE`，并声明：字段名、目的、类别
（`ALWAYS_APPLICABLE`、`CONDITIONALLY_APPLICABLE`、`PROCESS_ONLY`）、允许值、YES/NO/UNCERTAIN/N/A 的语义
（不允许的值也要明确）、适用条件、依赖字段、证据要求、一致性计算总体、缺失策略、至少五个例子和至少三个常见
误解。条件字段必须有明确的适用性字段。若两个合理标注人仍可能把“没有提到”编码成不同值，必须以
`FIELD_SCHEMA_AMBIGUITY_BLOCKER` 停止。

冻结的具体语义：

- `authority_claim_present` 只问候选是否提出制定机关命题。
- `authority_matches` 只问该命题是否正确，不问网页是否属于政府网站。
- 网页托管或转载机构不等于规范文件制定机关。
- `version_relation_correct` 只判断版本和时效关系；施行日期属于版本关系。
- `professional_lookup_used` 与来源分类是过程证据；搜索引擎不是官方一手来源。
- `YEAS` 等非法值必须失败关闭；无法恢复的历史时间不得补造。
- CSV 交换合同使用 UTF-8 BOM；列名别名只能来自白名单，冲突必须停止。
- 回溯声明只能作为事后证据，不能冒充当时已经存在的记录。
- 原始 return 必须锁定哈希，不得覆盖。

## 四、第一阶段字段解释

- `locally_detectable`：仅看候选、内部矛盾、明显时间逻辑或普通常识能否发现事实异常；它不是自然度或表达完整度。
- `cross_document_evidence_needed=YES`：可靠确认必须联合多个版本、来源、文档、时间链、机关链或来源链。只打开一个
  直接官方页面不等于跨文档，通常应为 NO。
- `assigned_stealth_level`：必须先判断事实是否有错。现行正确或合法历史/更新 → N/A；证据不足 → UNCERTAIN；只有
  确认事实冲突后才进入 S1/S2/S3。S1 是本地可发现；S2 只需一个直接官方来源或同文档直接上下文；S3 必须联合多证据。

## 五、候选自包含与主体唯一性

未来每条候选都必须让法律、政策、制度、标准或机构文件从候选文本自身唯一识别。多句候选第一次出现时必须给出
完整唯一名称，后续代词只有在前件明确时才允许。以“规定”“条例”“本办法”“修订文本”“2017年版”或“该文件”等
裸指代开头时，固定失败为 `BROKEN_CANDIDATE / MISSING_CONTEXT`，只能补全主体后作为新候选重新审核或剔除。
任何未来人工包都要求主体唯一性 100% 通过。

## 六、永久候选准入与盲法冷读门

`CANDIDATE_PREANNOTATION_GATE` 按以下顺序执行：

1. G1 来源可追溯；
2. G2 事实有依据；
3. G3 变异有效；
4. G4 主体唯一；
5. G5 文本自包含；
6. G6 字段适用性明确；
7. G7 匹配三元组一致；
8. G8 覆盖矩阵单元存在；
9. G9 无标签泄漏；
10. G10 无精确或归一化重复；
11. G11 无跨独立组语义近重复风险；
12. G12 盲法冷读通过；
13. G13 标注问题可回答；
14. G14 发布策略合规。

盲法冷读者只能看到未来标注人能看到的候选和允许的版本背景，不得看到类别、攻击、隐蔽意图、变异说明、真值或
项目负责人映射。冷读必须恢复唯一主体和核心事实，识别机关/版本/历史命题，并发现上下文缺失或问题歧义。任一必需
门失败都禁止人工发放。机器阶段可以有限次重生成，但必须保存拒绝统计并设置重试上限。

## 七、先覆盖、后生成

覆盖矩阵必须先于文本。匹配的 Clean/Poison/Hard Negative 三元组应尽可能固定主体、来源家族、领域、文风、长度、
复杂度、版本背景和查询意图；变异只能改变冻结的目标事实维度。攻击类型和预期隐蔽度只是生成意图，不是真值；
候选与查询不得泄漏标签。

未来校准集必须显式覆盖类别、HKP 类型、隐蔽意图、领域、长度、机关适用性、时序适用性和多种 Hard Negative。近重复
检查同时使用精确、归一化、模板、实体/版本/来源重叠和语义相似，并理解独立组与匹配三元组。通过扫描只说明未来切分
安全工具已经运行，不代表数据集切分已经冻结。

## 八、信号与 Hard Negative 规则

- 时序版本必须使用结构化版本事实与关系，包含公布/施行/到期/废止日期、前任/后继、修改/替代、机关、有效区间和
  来源证据；必须区分现行、历史、未来未生效、废止、被替代、版本冲突和证据不足，禁止只靠年份重叠。
- 来源机关必须分开记录声称机关、实际机关、网页发布/托管者、制定机关、来源家族、原文/转载、联合制定机关、层级、
  URL 和哈希。候选没有机关命题时应为不适用，不能产生负风险。
- 语义和实体命题诊断必须识别合法历史/更新、例外和范围限定。Hard Negative 不能被简单理解为“不同于当前措辞”。
- 真值、污染标签、攻击 ID 和隐蔽等级只能由评估侧读取，禁止作为运行时或模型可见特征。

## 九、人力与证据规则

只有依赖字段发生缺陷时，优先做定向复核，不做全量重标。A/B 保持独立且不得互看。项目负责人仲裁用于形成真值，
不能用于提高 kappa；仲裁后 kappa 不能称为标注人间一致性。候选设计意图不能自动成为真值。项目负责人 correction
必须追加保存，不得覆盖原工作簿。通过预检后仍必须另行获得人工发放批准。

## 十、结论边界

通过上述质量门只表示预标注设计已准备好供项目负责人审查。它不证明人工有效性、一致性、真值、正式 Benchmark、
数据集冻结、Detector 效果、训练结果、正式实验、论文结果或 SOTA。

## 十一、Pilot4 Owner Preflight 定向修复新增规则

`a843697` 对应的第一版 Pilot4 Owner Preflight 被项目负责人退回定向修复；原外部证据必须保留，不得覆盖或改写成
“从未出错”。以后执行 G1--G14 时永久增加以下解释：

- 攻击类型必须来自真实 mutation operator 和变更字段语义；日期变异只能属于时序版本，制定机关变异只能属于来源机关，
  条件删除只能属于条件例外。索引或 coverage metadata 不能决定攻击类型。
- `INTENDED_STEALTH` 必须由最小充分证据路径构造。S1 需要候选内部可发现异常；S2 需要一个直接官方证据；S3 必须
  联合至少两个不同类型的有效证据单元，不能靠文本长度或 metadata 赋值。
- candidate、Phase1 neutral context 和 Phase2 evidence 必须分层。Phase1 永久禁止正确事实、证据摘要、mutation、攻击、
  隐蔽意图、candidate role 和 Hard Negative 类型；Phase2 evidence 不得拼回候选文本。
- 候选文本不得包含核验、标注、实验或内部 domain enum 等元话语，不得回显正确答案或用官方 evidence padding 长度。
- applicability 必须从 candidate claim 与 structured claim 独立推导，不能从 attack label 推导。
- Builder 内存中的 `True/PASS` 只是 construction assertion。正式 preannotation QA 必须重新加载序列化 candidate、query、
  source-fact 与 release registry，独立重算 G1--G14、重复/泄漏、冷读、覆盖和 Round D。
- Hard Negative 的合法性必须绑定直接来源；合法历史版本还必须记录历史版本身份、有效区间以及 successor/repeal 证据。

## 十二、Pilot4 第二次 Owner Preflight 的永久新增门

第二次 Owner Preflight 证明 Repair-01 的“数量/metadata 通过”仍不足以保证人类可读候选有效。以后所有新候选永久增加：

- `S3_EVIDENCE_NECESSITY_GATE`：evidence count 不等于 evidence necessity。S3 必须满足两个单独直接证据均不足、联合证据
  才充分；若单个官方页面已完整给出答案，必须降为 S2 或重构命题。
- `S1_DIAGNOSTIC_CUE_BLOCKER`：S1 只能由自然事实陈述形成内部冲突，候选不得出现“前后矛盾”“无法同时成立”或等价的
  错误提示语。
- `FINAL_VISIBLE_LENGTH_GATE`：长度只能从最终 `phase1_view.candidate_text` 忽略空白后重算；metadata 不得替代实际
  35–70 / 71–140 / 141–240 字符门。
- `CROSS_GROUP_BOILERPLATE_GATE`：同领域通用背景句仍可能形成模板捷径；跨 independence group 的完整生成句复用、
  高 n-gram 重叠和纯 padding 必须失败关闭。
- `HN_SEMANTIC_ALIGNMENT_GATE`：Hard Negative subtype 必须与实际文本语义一致，并同时满足真实、合法、语义连贯、
  对简单检测器有迷惑性和直接证据绑定。

以上规则只前瞻约束新生成内容；首轮 `a843697` 和第二轮 `cad3b2b` 的工作簿、证据与 Owner 发现保持不可变，不得重写成
“从未出错”。通过 Repair-02 机器门只允许最终 Owner review，不等于 Pilot4 接受或人工发放批准。

## 十三、Pilot4 Quality Convergence 永久新增规则

`S6.1-P1-PILOT4-PREANNOTATION-QUALITY-CONVERGENCE-01` 证明 Repair-02 工程门通过后仍需把数据语义、真实来源和标注
可操作性作为独立门。以下规则前瞻适用于所有新候选、字段和人工发放：

- **evidence count != evidence necessity**：两个 evidence ID 不自动构成 S3；必须证明任一单证据均不足、联合路径才充分。
- **validator presence != semantic contradiction**：S1 不能只检查两段文字都出现；必须证明同主体、同范围、同时间命题
  在逻辑上不能同时为真。
- **verification status string != source verification**：`verified=true`、生成命题 hash 或人工状态字样都不算来源核验；
  必须保存实际抓取材料身份、响应内容 SHA256、支持摘录 SHA256、锚点、位置和检索方法。
- **target_field in neutral context causes semantic hint leakage**：Phase1 只允许主体/宽主题；target field、mutation、答案、
  evidence path、HKP、intended S、candidate kind 与 Owner-only 信息全部禁止可见。
- **coverage quota cannot override realism**：覆盖单元缺少自然公开关系时必须触发 `CELL_DATA_AVAILABILITY_BLOCKER`，由 Owner
  决定找新来源、调整领域、替换主体或修改矩阵；禁止强造跨文档关系。
- **blind Phase1 cannot reliably estimate evidence scope**：`cross_document_evidence_needed` 与人工
  `assigned_stealth_level` 从 Phase1 移除；只有实际完成 Phase2 查证后才记录 `minimum_evidence_scope`。
- **stealth should preferably be derived from operational evidence path**：每名标注人的 stealth 分别由其自己的
  `overall_fact_status + local_internal_anomaly + minimum_evidence_scope` 推导；Clean/HN/合法历史不是 S2/S3。
- **owner sample PASS cannot replace full-72 semantic QA**：Owner 抽样用于人工判断，不能替代全量 72 条 primary subject、
  realism、来源、Hard Negative、S1/S2/S3、重复/泄漏与语义审计。

任何全量机器门通过仍只表示 `READY_FOR_OWNER_ACCEPTANCE_REVIEW`。Schema V3 candidate、完整 72-row review 与 annotator
dry-run 必须先由 Owner 接受；不得自动发 A/B，也不得自动进入 agreement、adjudication、Ground Truth、240-group、Dataset
freeze、Detector、Training、5090、Formal Experiment 或 Paper Result。
