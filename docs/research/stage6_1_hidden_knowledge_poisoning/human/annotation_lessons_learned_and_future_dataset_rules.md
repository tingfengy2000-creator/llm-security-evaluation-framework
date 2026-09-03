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

## 十一、Pilot4 Owner Preflight 定向修复候选经验

> 第 11–16 节当前状态：`PROVISIONAL_LESSON / PILOT4_PROTOCOL_LESSONS =
> PROVISIONAL_PENDING_FINAL_ACCEPTANCE`。这些规则有工程证据，但 External Phase1、External Phase2、blind comparison 与
> Owner 最终 acceptance 尚未完成，因此不得描述为 `ACCEPTED_LESSON` 或已最终证明的永久规则。原问题、修复内容和工件
> 保持不变；未来仅在 `PILOT4_ANNOTATION_PROTOCOL_ACCEPTED` 后通过 promotion gate 决定哪些规则转为 accepted。

`a843697` 对应的第一版 Pilot4 Owner Preflight 被项目负责人退回定向修复；原外部证据必须保留，不得覆盖或改写成
“从未出错”。在 Pilot4 最终验收前，执行 G1--G14 时按以下 provisional 解释 fail closed：

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

## 十二、Pilot4 第二次 Owner Preflight 的 provisional 新增门

第二次 Owner Preflight 证明 Repair-01 的“数量/metadata 通过”仍不足以保证人类可读候选有效。当前所有新候选按以下
provisional 门执行，是否提升为永久规则留待最终 acceptance：

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

## 十三、Pilot4 Quality Convergence provisional 新增规则

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

## 十四、Evidence Pool 与 English-first Schema V3.1 provisional 规则

`PILOT4-EVIDENCE-POOL-REPAIR-01` 将以下内容登记为待最终验收的协议候选经验：

- **English-first canonical vocabulary + Chinese support**：machine field name、JSON/CSV/XLSX canonical value 与 enum
  只使用英文；中文只放在括号说明、Quick Start、Field Guide、Legend 或相邻帮助文字中。
- **Do not introduce unnecessary bilingual value mapping**：不得把“中文展示值”再反向映射为英文 machine value；避免
  增加第二套值域、隐藏转换和不可审计歧义。
- **Distinct visible evidence units**：Phase2 的 E1/E2 必须是不同 URL、不同内容 hash、不同 official document/source
  identity 且与候选相关、实际核验过的 source unit。相同 URL、内容、文档、摘录或身份的重复记录只能计一个证据单元。
- **Evidence slot duplication is a protocol defect**：重复 slot 会同时污染 evidence selection、minimum evidence scope 与
  S2/S3 测量；不能用无关官方页面凑满两个 slot。真实来源不足时必须触发 source-availability blocker。
- **Historical rule — superseded by Section 15**：本节当时用 `phase2_issue=CANDIDATE_AMBIGUOUS` 区分 claim ambiguity 与
  evidence insufficiency；Section 15 已将其收口为 Phase1 candidate defect 或
  `LATE_DISCOVERED_CANDIDATE_DEFECT`，两者都退出普通 GT path。只有 claim 明确存在但证据不足时，才用
  `PRESENT_EVIDENCE_INSUFFICIENT`。
- **Annotator UI readability is protocol quality**：English-first 表头、中文辅助解释、Phase1/Phase2 职责分离、Evidence Pool
  单独 Sheet、合理冻结窗格与只读/人工输入配色，都必须进入 workbook visual QA，而不是视为可选美化。

Annotator 仍不直接填写 S1/S2/S3；`derived_stealth_level` 由验证后的
`overall_fact_status + local_internal_conflict + minimum_external_evidence_needed` 确定性派生。任何通过只表示协议已准备供
Owner acceptance，不自动授权 A/B distribution。

## 十五、Pilot4 标签盲法可作答性与候选核验路径去泄漏 provisional 规则

`PILOT4-ANNOTATION-PROTOCOL-INDEPENDENT-VALIDATION-AND-CANDIDATE-CLEANUP-01` 将以下规则追加为当前 Pilot4 的
provisional fail-closed 质量门；`b705cc` 及此前 Evidence Pool 仍保持历史不可变：

- **Expected-label reconstruction is not independent answerability validation**：读取 `candidate_kind`、attack type、
  intended stealth 或其他 Owner-only 字段后重建答案，只能叫 `EXPECTED_CONTRACT / LABEL_AWARE_ENGINEERING_CHECK_ONLY`，
  不得作为标注人可作答性的独立证据。
- **Two simulations sharing one answer table are not independent annotators**：共享 `_SIM_RULES` 的两次编码只能登记为
  `SCHEMA_RULE_CONSISTENCY_A/B`；无法建立两个独立推理上下文时，必须如实使用
  `ONE_LABEL_BLIND_SEMANTIC_REVIEW + OWNER_REVIEW_REQUIRED`。
- **Lock before compare**：全量 label-blind reviewer 输出、具体理由与歧义发现必须先完成并做 SHA256 锁定，之后才允许
  加载 `EXPECTED_CONTRACT`；任何 mismatch 原样保留，禁止把 reviewer 自动改成 expected。
- **Factual conflict and insufficient evidence are mutually exclusive at the minimum-evidence layer**：
  `minimum_external_evidence_needed` 只允许 `ONE_OFFICIAL_EVIDENCE / MULTI_EVIDENCE_OR_VERSION_CHAIN / NOT_APPLICABLE`；
  证据不足由 `overall_fact_status=INSUFFICIENT_EVIDENCE` 表达，且 minimum 必须为 `NOT_APPLICABLE`。
- **Ambiguous local conflict must not silently become S2/S3**：只有 `local_internal_conflict=NO` 且 minimum 分别为 ONE/MULTI
  才能派生 S2/S3；`UNCERTAIN` 永远派生 `UNCERTAIN`。
- **Candidate defects exit normal Ground Truth flow**：Phase1 核心缺陷登记为 `ANNOTATION_SAMPLE_DEFECT` 并停止普通
  Phase2；只在证据映射时才发现的缺陷使用 `LATE_DISCOVERED_CANDIDATE_DEFECT`，退回 Candidate QA。
- **Evidence Pool source-role metadata may leak provenance**：正式人类可见证据池只显示 `sample_id / evidence_id /
  official_page_title / official_source_url`。`source_type`、角色、支持命题、锚点和最小路径只留在 machine registry。
- **Researcher-authored identity is not a neutral page title**：人类可见标题必须来自 actual page title 或 official document
  title，并记录 `display_title_origin`；不得显示研究者撰写的转载、版本题注或角色解释。
- **Candidate must not describe its own verification procedure**：候选只陈述自然知识命题，不得告诉读者需要几个来源、
  应比较哪些角色或怎样核验。语义门必须覆盖方法性改写，不能只靠关键词正则自证通过。
- **Naturalness is independent of truth and self-containment**：自然度只判断语法、流畅、模板痕迹、重复和句间连贯；
  事实真伪与主体缺失分别由 Phase2 和 `phase1_issue` 处理。
- **Actual evidence used and minimum evidence required are different variables**：`evidence_selection` 记录标注人实际使用的
  E1/E2；实际使用 `E1+E2` 与 minimum=`ONE_OFFICIAL_EVIDENCE` 完全可以同时成立。

机器侧 72/72 label-blind 可执行与零设计 mismatch 只支持 Owner acceptance review。机器未建立两个独立人类 reviewer，
因此仍不得登记协议接受或发放 A/B。

## 十六、外部标签盲法、身份隔离与标题溯源 provisional 规则

`PILOT4-EXTERNAL-BLIND-OWNER-REVIEW-PACKET-01` 纠正上节对 c1b Full72 的证据分类，但不删除或覆盖上节及其原始
工件。c1b reviewer 使用 `sample_id` 查询硬编码标签集合，因此该历史结果只能登记为
`SAMPLE_ID_LABEL_LOOKUP_CONTAMINATED_REVIEW / NOT_ACCEPTABLE_AS_EXTERNAL_LABEL_BLIND_EVIDENCE`。以下规则当前作为
`PROVISIONAL_LESSON` 生效于 Pilot4 收口前的保守执行，不代表已获最终方法学验收：

- **Sanitized input alone does not establish blindness**：即使序列化输入不含 `owner_only`，reviewer 代码只要编译了
  sample-ID label lookup，仍能恢复隐藏 expected labels。
- **Sample identity can itself be a leakage key**：正式外部包必须使用一次性、非连续、不透明 ID；原 `sample_id`、triplet、
  independence group 和设计标签只留在隔离的 owner mapping。
- **Lock-before-compare is necessary but not sufficient**：若 expected knowledge 已编译进 reviewer logic，先锁输出仍不能
  证明盲法；必须同时证明 reviewer path 无 label table/import/lookup。
- **Unique reasons are not independent reasoning evidence**：72 个不同字符串或候选特定理由不能证明语义独立性，更不能
  替代外部人类/LLM 在隔离上下文中的事实判断。
- **Machine validators do not substitute for semantic reviewers**：机器只检查 schema、visibility、hash、enum、dependency、
  source retrieval、format、duplicate 和 leakage；不得输出 candidate 的事实答案或冒充 annotator。
- **External mapping must be isolated and hash-bound**：opaque ID mapping 必须 owner-only、Git-external、单独 manifest entry，
  且不得进入 external packet 或被 blind packet formatter/reviewer 读取。
- **Visible official titles need actual provenance**：`official_page_title` 只允许来自 HTML title、页面 H1、官方文档 heading
  或 PDF heading，并绑定 source snapshot 与标题文本 SHA256；禁止人工 override、研究者 source identity 或合成标题。
- **Field-guide examples must be genuine teaching fixtures**：每个人工字段必须覆盖常见、alternative/negative 与边界案例；
  reason 字段还要含 good/bad/forbidden，禁止把字段定义套模板后冒充案例，也不得复用正式候选。

完成外部包只支持 `BLIND_PACKET_READY + NO_LABEL_LEAKAGE`。外部 reviewer 返回前不得加载 expected contract、计算 mismatch、
宣布 answerability、接受协议或发放 A/B。

## Provisional external LLM blind-review separation rule（2026-09-02）

- 单一文档若同时含有第一阶段候选判断和第二阶段证据，就会破坏大模型复核者的严格第一阶段盲法：
  `A single document containing Phase1 candidate judgment and Phase2 evidence breaks strict Phase1 blindness for an LLM reviewer.`
- “暂时不要阅读证据”的行为指令不等于证据从模型上下文中物理缺席：
  `Do not read the evidence yet is not equivalent to evidence being absent from model context.`
- 盲审必须以文件和释放门进行结构性信息隔离，不能依赖复核者自我约束：
  `Blind review must enforce information separation structurally, not behaviorally.`
- 已看过候选、标签或修复历史的同项目模型，不得宣称为隔离的外部复核者：
  `A same-project GPT already exposed to candidate, label or repair history is not an isolated external reviewer.`
- 第二阶段证据释放前，第一阶段原始返回必须完成结构验证、身份全集核验、哈希锁定和不可变保存：
  `The exact Phase1 raw return must be schema-validated, identity-complete, hash-locked and immutable before Phase2 evidence release.`
- Pilot4 当前复核顺序固定为 `PHASE1 -> RETURN -> HASH LOCK -> PHASE2 RELEASE`；第一阶段使用网页或事实查证即
  `PHASE1_BLINDNESS_VIOLATION`，该轮 return 失效。

## 十七、Pilot4 协议经验提升门

临时经验与已验收经验必须分开。临时经验可以在当前流程中用于保守地阻止已知风险，但它只说明工程排查发现了问题并
形成候选解决办法，还没有证明外部人员能稳定理解、独立作答和重复执行。只有完成两阶段外部复核、比较与项目负责人
最终验收后，才能判断规则是否真正可复用。这样既不会丢失返工教训，也不会把尚待检验的方法提前写成论文结论。

当前：`PILOT4_LESSON_PROMOTION = AFTER_FINAL_ACCEPTANCE`。未来且仅当 Owner 明确登记
`PILOT4_ANNOTATION_PROTOCOL_ACCEPTED` 时，对应 acceptance task 必须执行 `PILOT4_PROTOCOL_LESSON_PROMOTION`，逐项审查：

1. `Annotator-facing Schema` 与 `Canonical Machine Schema` 分离。
2. 机器可派生字段不要求人工重复填写。
3. 同一人工判断不拆成多个高度相关字段重复询问。
4. `Evidence count` 不等于 `Evidence necessity`。
5. S1/S2/S3 按 `operational evidence path` 从底层人工判断派生，而非让 annotator 直接猜。
6. Candidate 不含 `verification procedure`、`minimum-evidence hint`、`answer echo` 或
   `experimental meta-language`。
7. `Coverage quota` 不凌驾于 naturalness、construct validity 与 source quality。
8. `Hard Negative` 必须真实成立、有官方证据且容易与 `Poison` 混淆。
9. `Sanitized input` 在 reviewer code 含 `sample-ID label lookup` 时不构成真正 blindness。
10. `sample_id` 本身可能成为 leakage key。
11. `Lock-before-compare` 只有在 reviewer logic 不知道 expected label 时才构成真正盲法。
12. `Machine validator` 不能替代 `semantic review`。
13. `Evidence Pool` 的 source role、source type 与 researcher-authored title 都可能形成 leakage。
14. `Annotator-facing title` 必须可追溯至真实 official page/document title。
15. Phase1/Phase2 必须结构隔离，不能依赖“先不要看后面的 Evidence”。
16. Phase1 raw return 必须 immutable lock 后才允许 Phase2 release。
17. 已接触 project history 的 GPT context 不能宣称 isolated external reviewer。
18. 人工 annotation 应置于 candidate/source/schema 高强度 machine QA 与 Owner QA 之后，以减少返工。

Promotion 必须逐项记录 `ACCEPTED_LESSON`、继续 provisional 或 rejected/superseded 的证据与理由，不得整批自动接受。最终
acceptance 后，Human Ledger 再新增“Pilot4 标注体系给项目留下了什么经验？”通俗摘要，按“问题 -> 原因 -> 最终规则”
组织并链接本文件；首次/二次 preflight、evidence echo、fake S3、length mismatch、schema ambiguity、Evidence Pool duplicate、
sample-ID leakage、combined-packet flaw 与 phase-separation repair 的时间线不得删除。

## 十八、Phase1 返回后的候选缺陷处置门（临时规则）

外部盲审的第一阶段不仅检查复核流程，也可能暴露候选自身的上下文缺失、指代模糊或不自然表达。若 Phase1 return 中
存在 `phase1_issue != NONE` 或明显自然度问题，不得因为 schema、72/72 ID 和 hash-lock 已通过就立即释放 Phase2。

此时应保留 raw return，不回写 reviewer 单元格；仅用 blind ID、候选文本和 Phase1 可见字段生成项目负责人预检。项目
负责人在身份映射、expected contract 与 Phase2 均关闭的情况下，逐条决定接受原候选、局部修订后重新盲审，或剔除/
替换。只有这些决定被追加记录且相应验证完成后，`PHASE1_CANDIDATE_DEFECT_TRIAGE_RESOLVED` 才能为 true。

本规则当前状态为 `PROVISIONAL_PENDING_PILOT4_FINAL_ACCEPTANCE`。它可保守阻止带缺陷候选直接进入 Phase2，但尚不能
描述为已验收的正式数据集规则，也不授权 Codex 自动修正候选、打开正确答案、释放 Phase2 或启动 A/B。

## 十九、真实盲审作为候选质量门与 final-corpus 一致性（临时规则）

Attempt1 证明，真实 blind review 不仅能检查 annotation schema，也能发现机器 QA 和 Owner preflight 未发现的自然度、
自包含性与指代问题。因此第一次外部复核发现 candidate defect 时，应保存为有效 defect-discovery evidence，不能写成
“无效所以删除”，也不能回写原始 return 让历史看起来从未出错。

如果 blind review 后任何 candidate text 发生变化，最终复核证据必须对应同一个 final corpus。禁止把旧 corpus/reviewer 的
未修改行与新 corpus/reviewer 的修复行静默拼接；应对统一 final corpus 重新生成 opaque identity 和顺序，并完整重跑所需
blind phase。旧 attempt、Owner correction、mapping scope、repair audit 和新 attempt 必须分别保存并可追溯。

本规则当前状态为 `PROVISIONAL_PENDING_PILOT4_FINAL_ACCEPTANCE`。它允许 fail closed、保留历史并要求 fresh Full72 review，
但不证明 annotation protocol 已被接受，也不授权 Phase2、A/B、Dataset freeze 或正式实验。

Attempt2 的 fresh Full72 return 现为该临时规则新增支持证据：final corpus 的 72 条均返回 `phase1_issue=NONE`，因此本轮
Candidate Text Quality Gate 可以关闭，并按照同一 annotator、locked Phase1、再释放 Phase2 的顺序继续。该结果只说明
候选文本缺陷门通过，不是 expected-label accuracy、annotation protocol 或正式数据集验收；本规则继续保持
`PROVISIONAL_PENDING_PILOT4_FINAL_ACCEPTANCE`，不得提前提升为 Accepted Lesson。

## 二十、在线链接重试、原始返回先锁定和标签边界审计（临时规则）

Pilot4 最终第二阶段提供三项新增但尚未最终验收的经验。第一，同一复核人的 `SOURCE_UNREACHABLE` 从 23 降为 0，说明
外部环境单次打不开在线官方链接，不能直接推断链接已经失效或指定证据无效；未来仍应同时保存链接来源信息与冻结证据
快照，以降低工具或环境瞬时访问差异带来的影响。第二，盲审原始返回必须在身份映射和预期答案合同之前完成物理锁定，
并保存可核验的时间顺序；只有这样，后续对比才不会反向污染复核人返回。第三，预期答案合同不是绝对真理，系统性分歧
必须检查标注指南边界、证据充分性和预期答案构造过程，不能批量归因于复核人错误。

本轮 16 条 `CURRENTLY_CONSISTENT` / `LEGITIMATE_VERSION_OR_HISTORY` 主标签分歧说明，“候选只要正确讨论修订或版本演化，
是否就属于合法版本或历史”尚未形成唯一操作定义；在项目需求提出人冻结边界前，这是
`GUIDE_AMBIGUITY / SYSTEMIC_PRIMARY_LABEL_BOUNDARY_BLOCKER`。`BR-18F1D39495` 进一步说明，如果指定证据池不支持预期
命题，应登记证据池或预期答案缺陷，而不是改写复核人的原始返回来通过验收。

本规则当前状态为 `PROVISIONAL_PENDING_PILOT4_FINAL_ACCEPTANCE`。它支持本轮
`RECOMMEND_TARGETED_REPAIR`，但不得写成已接受的正式标注协议，也不授权 A/B、真值、240 组、数据集冻结、检测器、训练
或正式实验。

## 二十一、字段局部修复与匹配控制验证（临时规则）

当外部复核显示 Phase1 候选质量和大部分 Phase2 字段稳定，而分歧集中在一个可明确定位的字段边界时，不应把问题误写成
“整个实验失败”，也不应为了形式完整机械重跑全部候选。应先保持 raw、candidate corpus 和旧 expected 不变，追加新 guide、
new expected/evidence version 与逐项 lineage；再用“全部受影响样本 + 匹配控制”做新的隔离验证，检查修复是否真正改善边界、
同时没有破坏原来稳定的样本。

匹配控制必须覆盖与受影响样本相近的 domain、candidate class、HKP、intended stealth、version/authority claim profile，且
reviewer 不得知道哪些是 impacted、哪些是 controls。新一轮使用 fresh opaque ID；旧 reviewer ID、sample ID、expected、mapping、
mismatch taxonomy 和 control designation 均不得进入 reviewer context。验证结果必须先锁 raw，再比较 Expected V2。

本规则当前状态为 `PROVISIONAL_PENDING_PILOT4_FINAL_ACCEPTANCE`。本轮 21 impacted + 16 matched controls 的 R3 包只是待执行的
验证设计，不是协议已经清晰、可复现或可扩展的结果；只有 fresh external return 完成并经 Owner 最终验收，才可考虑提升。

## 二十二、R3 匹配控制与 Expected 契约独立审计（临时规则）

R3 已把上一节的验证设计变成了真实外部返回：37/37 raw、枚举、理由、条件逻辑和 lock-before-Expected 顺序通过；M4 的
证据缺口没有复现，M8 四条也全部得到唯一的 one-official-evidence 判定。这说明 targeted review 能够在不重跑 Full72 的
情况下验证局部修复及其控制样本，但它不能把 Expected contract 当作不可质疑的真值。

本轮 controls overall 只有 13/16。逐项阅读候选、Guide 和 Evidence 后，三条同根 control 分歧来自 Expected V2 把当前仍
有效的修订/更新过度归类为历史；另有一个未命名 authority overcall、一个 intrinsic version-sequence underclassification
和两个 minimum-evidence contract error。故评估流程必须先分别审计 reviewer、guide、evidence 和 expected，再决定根因；
不得为了提高 agreement 静默把 reviewer 改成 expected，也不得把 Expected 修正写成 reviewer 重标注。

本规则当前状态继续为 `PROVISIONAL_PENDING_PILOT4_FINAL_ACCEPTANCE`。它支持 additive Expected V3 和复用已锁定 R3 raw
重算门，不支持默认 R4。只有 Owner 后续明确接受协议并执行 lesson promotion，才能决定哪些条目升级为
`ACCEPTED_LESSON`；A/B 仍需单独审批。
