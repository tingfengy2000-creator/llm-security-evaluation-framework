# VACE-Lite V0.3：证据充分性驱动的自适应核验候选规格

Task：P1-VACE-LITE-V03-ADAPTIVE-VERIFICATION-DESIGN-01。
2026-10-28；PODR-148 / OR-102 / REL-2026-0117；设计依据提交9f0d42e2df1b9322061e3a98e140487f54998ccb。
状态：`DESIGN_ONLY / VACE_LITE_V03_OWNER_REVIEW_REQUIRED / NO_NEW_DETECTION_EXECUTED`。
本稿不是已验收方法、已冻结正式科研合同或实施授权；不修改V0.2、数据、Guide、人工GT或Evidence。

## 1. 设计结论与真实起点

V0.3不把所有输入送入同一个SEPT融合分类器，也不采用A0 OR B1。
先用Candidate-only语义一致性核验寻找**有证明的同域内部冲突**；没有证明则独立检索官方证据，
依实际未满足的证明义务选择版本、机关角色或联合前提补证，预算耗尽仍不足则弃权。
A0只有线索发现/检查次序作用；B1仅是历史比较条件，绝不作为兜底裁决器。

V0.2已提出六槽位、三态及内部冲突免外证。V0.3的增量是显式状态机、充分性账本、受限补证、
错误隔离和成本公平对照，不把V0.2伪写成强制SEPT或已运行方法。
历史依据：[D1四条件](../PAPER1_D1_FIRST_DETECTION_RESULTS_RECORD_V1.md)、
[A0结果](../PAPER1_VACE_LITE_R1_RECORD_V1.md)、[V0.2](VACE_LITE_V02_METHOD_SPEC.md)。
当前基础单元仍是40–68字短候选命题。无长文档/新模型/新训练或V0.3性能数据。

## 2. 六槽位与证明义务

沿用subject、predicate、value_unit、scope、time_version、source_role。
每项保留原文span、规范化值和OBSERVED / NOT_STATED / NOT_APPLICABLE / UNRESOLVED。
predicate保留关系类型/比较方向；scope保留条件、例外、量词、否定作用域；source_role区分通过、公布、制定、修订、转载。
不增加新的人工字段，不把Evidence中的日期/机关信息反向制造Candidate版本/权威主张。

建立`obligations`：本条所有断言及其必要槽位、适用域和待证明关系。
义务来自Candidate语义和公开任务上下文（如事前给定as_of），不来自GT、Role、HKP或S。
显式机关/版本主张必须先入账，不能只核验数值后就SUPPORT。
NA由Candidate语义决定，不因证据找不到就将义务改成NA；未陈述不自动补“现行/全部/唯一”。
若提取被纠正，保存新解析版本、废止受影响证明并重验；不能偷偷删掉困难断言。

## 3. 路由图（设计，非已执行流程）

```text
Candidate → E0 六槽位与义务 → I 文内一致性（A0仅辅助发现）
                                  ├─有效内部冲突证明 → CONTRADICT / 文内证书
                                  └─未证实/未解析 → R0 独立官方Top5 → F 同域事实绑定
                                                                     ↓
                                                         Q 充分性账本/证据冲突检查
                                  ┌──────────────────────┼───────────────────────┐
                         全义务支持且无未解冲突     一条完整反证义务已成立      证明有缺口
                                  ↓                     ↓                       ↓
                               SUPPORT              CONTRADICT          按缺口选T/P/J/F
                                                                            ↓
                                                            更新账本 → 回Q；不满足停止条件
                                                                            ↓
                                                                  INSUFFICIENT / 复核
```

I是单一信息来源的文内语义视角，不是MLM自然度或A0词面分数。
所有非空合法输入均检查相关命题对，A0阴性不能跳过I或直接放行。
无法生成合法查询、输入解析失败或有不可恢复歧义时记录失败原因并INSUFFICIENT，不伪造检索执行。

## 4. 模块输入输出合同

| 模块 | 允许输入 | 输出与不可替代条件 |
| --- | --- | --- |
| E0 提取/义务建立 | Candidate、固定schema/词典、公开as_of | 六槽位、命题列表、原文偏移、义务/未解析；不读Evidence/标签 |
| A0 线索发现 | Candidate | cue spans/待查命题对优先级；无事实判决、无终态权限 |
| I 内部核验 | E0命题、原文、A0提示、固定关系语义 | PROVEN_CONFLICT / NOT_PROVEN / UNRESOLVED；仅前者可提交内部证书 |
| R0 检索 | Candidate/已观察槽位、统一冻结官方语料、固定retriever | Top5 UID/排序/score/query/hash；无人工E1/E2身份映射 |
| F 事实对齐 | 义务、合法Evidence spans、已有Registry元数据 | subject/relation/scope/version绑定、支持/反证/缺口候选；相似度不算证明 |
| T 版本补证 | 具体版本/适用时间/前后版本关系缺口、冻结Registry | provenance-backed版本边/区间或仍缺；没收录不等于不存在 |
| P 来源/机关补证 | 证据可采性或显式机关角色缺口、官方元数据/正文 | host/publisher/issuer/adopter/amender/reposter绑定或仍缺；不由域名猜机关 |
| J 联合前提补证 | 明确比较/跨条款命题及缺少的事实前提 | 被约束的缺失前提、互连证据span和关系；不是“再找一篇判毒文档” |
| Q 充分性/调度 | 义务账本、全部已获证据及冲突、剩余预算 | 终态或下一动作+gap reason；不读A0/B1判毒标签、GT或S |
| O 输出分流 | Q/I有效证书、运行trace | 三态、proof refs、review_required及成本；不写成GT或攻击意图 |

所有补证都限于当前获准冻结语料/Registry。新网页、外部证据、人工E1/E2定位服务或新来源均不在本设计授权内；
发现库外缺口输出FROZEN_CORPUS_GAP并提交Owner，不能悄悄扩Evidence。

## 5. I分支的内部冲突证书

证书至少含两个断言的原文偏移和字节hash、各自六槽位、同主体/时间/scope绑定、
互斥关系规则ID及其适用前提、未解析项为空、断言层级/引述状态。
只有以下全部成立才PROVEN_CONFLICT：

1. 两者都是Candidate作出的事实/规范断言，而非引用错误观点、假设、否定引述或不同说话人报道。
2. 同一对象可唯一恢复，关系确实相同；“通过机关”与“公布机关”不是同关系。
3. 时间/版本与条件域的重叠及排他性已被证明；不能因都未写条件就臆造同域。
4. 有已定义的互斥语义：同域P与非P；或单值事实上的不相容精确值/不相交约束。
   不同数字本身不够；“至少5天”与“10天”可以相容。
5. 量词/例外/单位/模态均绑定；“一般允许、例外禁止”不自动冲突；两个机关共同公布不自动互斥。

任一项未知则NOT_PROVEN/UNRESOLVED并走R0，绝不借A0命中补齐证明。
I未发现冲突只说明未证明内部矛盾，不产生SUPPORT。
第一版只对有清晰类型语义的关系给证书，其余回退外证，不能承诺覆盖全部自然语言矛盾。
终态由O验证证书格式、原文span和前提；空证书或不匹配不能提前退出。

## 6. Q充分性标准与有序路由规则

充分性是义务相对冻结语料、已取得证据与核验预算的**操作性充分性**，不是世界事实完备性保证。
高检索分数、命中官方域名、两篇文档数量、A0关键词、B1概率都不能替代充分性。

### Q的三种终态

- SUPPORT：所有适用且必要的义务都有同主体/同scope/版本相容支持span、必要来源可采、无未解决的同域反证。
- CONTRADICT：至少一项义务获得完整、同域、来源可采的相反事实证明，或I证书成立。
  其他未核命题不得被一并宣称已核；输出说明证伪了哪一项。
- INSUFFICIENT：缺必要绑定、来源/版本未解决、可信证据冲突、预算/解析/语料缺口；不映射为Poison或Clean。

每次Q须先审已获证据的同域冲突和来源可采性，再接受外证证明；不能挑选最支持“有毒”的一份。
跨版本数值不同先查适用域，不当作同域冲突。可信官方证据自身未决时，受影响义务暂不可裁。

### 路由优先级（同时多缺口时按以下固定顺序，不按标签排序）

| 顺序/条件 | 动作 | 缺口仍在时 |
| --- | --- | --- |
| 0 原文/解析/UID或hash不合法 | 标记FORMAT_OR_IDENTITY_ERROR，禁止使用坏证据；可在预算内重取同一冻结工件 | INSUFFICIENT，不做事实推断 |
| 1 证据可采性未确认 | P处理SOURCE_ADMISSIBILITY_GAP | 不用来源不明材料给结论 |
| 2 版本或当前/历史适用绑定、比较关系缺失 | T处理VERSION_BINDING_GAP / VERSION_RELATION_GAP | 没有版本登记不是反证 |
| 3 显式机关—角色未绑定 | P处理CLAIMED_AUTHORITY_ROLE_GAP | 无权威主张时不强补发布者空字段 |
| 4 比较/联合命题缺某端事实或必要桥接 | J处理JOINT_PREMISE_GAP | 从已观测主体/关系/版本生成目标查询 |
| 5 其他值/范围/实体span未绑定 | F并按允许预算目标检索处理FACT_OR_SCOPE_GAP | 不用global数字/否定词袋补证 |
| 6 没有可执行新动作、出现重复查询或用尽预算 | 停止，列出剩余gap与已尝试动作 | INSUFFICIENT / 人工复核 |

普通公布日期不自动触发版本主张；但无显式版本主张的规范句若需要当前适用性且绑定缺失，可触发T。
这只补适用证据，不改变Candidate的version_claim存在与否。
一份官方文档若已给出两端必要前提，可以充分；两个文档也可能不充分。
不能为了猜测的S3强制补第二份，更不能将annotator的evidence_selection当检索输入。

## 7. 有限补证与两个候选运行档（均待另批）

**F5同池档（建议优先做公平性验证）**：外证首轮固定Top5；T/P可查冻结Registry元数据，
正文证据仅可来自该Top5。缺失第二前提且不在池内则INSUFFICIENT，不偷偷扩池。
I证书成立可以不消费外部证据，其他分支与非自适应/L0使用相同首轮证据池。

**E2受限扩池档（后续工程比较）**：首轮Top5，最多两个目标正文获取动作，每动作Top5，
所有读取的新增正文（包括Registry链接回取）按UID去重并计入上限，至多15份正文；
Registry解析/缓存命中另记数，不通过“元数据读取”免费带入正文。
这是PROPOSED_BUDGET_PROFILE，不是本轮资源或检索配置变更批准。

只查询具体未满足的义务；query由Candidate已观察槽位+已核证据锚点+gap组成，
不能从正确答案、GT值或“该题应属于哪级”补词。已取得UID不可重复计为新证据。
每个gap/action签名最多尝试一次；每次要么新增可采绑定/证据，要么消耗有限预算并记录无进展。
签名由规范化义务/可观测锚点/动作与冻结版本构成，不靠随机换词绕过去重；解析修订、缓存或重试不重置总预算。
预算停止不能变成SUPPORT。新反证使旧证书失效时保留版本记录并重验，不静默覆盖。
模型调用/token/延迟上限尚未选择模型，须执行前单独冻结；预算不能只有文档数而隐去LLM调用数。

## 8. Runtime与Evaluator隔离

Runtime仅获Candidate、opaque ID（仅trace键）、公开as_of、固定政策、冻结官方库/Registry与预算。
禁止字段：GT、label、construction_role、group/family split标识、HKP、S1/S2/S3、target/derived S、
Owner/Expected、A/B/R3/R4答案、minimum_external_evidence_needed、evidence_selection和人工E1/E2映射。
这些可在预测/路由trace锁定后由Evaluator关联，不能在Q内充当捷径或目标补证条件。
来源文档本身依法可观测的version family允许使用；评测group/family身份与构造簇不允许进入Runtime。

模块输入用白名单schema；Retriever/Router进程无标签vault路径权限，ID不可解析推断角色。
缓存键只含内容/模型/配置/证据UID及hash，不含标签、S、构造路径；日志不暴露完整标注文件。
未来测试同一Candidate换opaque ID、删除评价metadata后路由应不变；cache warm/cold及worker批次需审计。
Oracle诊断用独立Evaluator入口封装证据，仅标为ORACLE_ONLY，主路由器不得提供“取正确E1/E2”API。

## 9. 输出与成本trace

输出字段设计：candidate_uid、candidate_hash、parser_version、obligations、route_trace、
verdict、proof_refs、unresolved_gaps、review_required、budget_used、policy/model/corpus/registry hashes。
每个route event保存step_id、state_before/after、observable_gap、action/query、证据UID/span/hash、
证书版本、停止理由、调用/token/时延/字节数、缓存状态；proof可回到原文，不只是一段自由解释。

CONTRADICT→冲突风险标记，SUPPORT→当前证据支持，INSUFFICIENT→复核；不等同恶意意图/全局安全/正式GT。
第一版不编造连续概率。若后续要排序风险，须独立冻结分数方向、缺失/弃权语义和train/dev阈值策略。
本轮无实际routing trace、新预测、模型权重或检测指标。

## 10. 错误传播与科研可行性

| 首因 | 传播风险 | 设计控制与未来验证 |
| --- | --- | --- |
| A0cue被误当证明 | 合法HN提前判毒 | A0无终态权；I必须独立证书，测试无cue冲突和带cue合法句 |
| 断言/主体/scope提取错 | I假冲突或错误目标查询 | span/量词/模态/引述绑定、独立slot参考；未知不证明 |
| I错误提前终止 | 后续外证没有纠错机会 | 独立审I证书、报告早退HN误报；预算内shadow审计仅另批，不用GT改Runtime |
| 检索miss或官方库缺口 | 外部漏检/过多弃权 | 原因区分REFERENCE_MISS/CORPUS_GAP；检索命中率不是检测率 |
| T/P注册不完整/角色混淆 | 正确历史/转载被判毒 | 义务驱动补证；不存在证明不能由登记缺失推断 |
| Q过早判充分 | 少读反证导致假SUPPORT/假CONTRADICT | 完整义务、已获证据冲突检查、固定更完整证据对照；有限库充分性局限显式报告 |
| 为省成本大量弃权 | HN-FPR看似降低而任务未完成 | 全体分母Recall、弃权分布、复核预算和成本联合报告 |
| 原文span/JSON/上下文截断 | 伪引用、丢第二前提 | hash/偏移/解析验证；失败弃权，记录截断而非填答案 |

若I与外证退出是互斥实际路径，HN-FPR可分解为“早退I误报项＋到达外证后的误报项”；
分层Recall同理必须用真实route trace作条件计数。不能把A0的S1表现和B1在S2/S3的边际数字拼成新性能。
成本表达式是C_I + 1{进入外证}·(C_R0+C_F+补证动作成本)，各项须将来实测，不代入假定分流比例。

可行性结论：模块设计可实现且较统一SEPT更可审计，但slot抽取、I证明精度、Registry覆盖、
充分性误判和调度收益均未验证。自适应/六槽位本身不是已证明创新；只有公平的HN/Recall/成本证据才能支撑价值。
无真实V0.3检测率；“75%理想化分流”不是实测、不是正式上界。本轮完成后STOP等待Owner审阅。
