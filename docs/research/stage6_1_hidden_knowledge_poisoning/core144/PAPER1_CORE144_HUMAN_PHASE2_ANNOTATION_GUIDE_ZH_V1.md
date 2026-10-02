# Core144 Human Phase2 中文标注手册 V1

适用对象：`HUMAN-A01`、`HUMAN-B01`
适用答卷：`PAPER1_CORE144_D1_HUMAN_A01_PHASE2_V1.xlsx` / `PAPER1_CORE144_D1_HUMAN_B01_PHASE2_V1.xlsx`
规则基线：Formal Annotation Guide V4 + V4.1 + V4.2 + V4.3
重要边界：本手册只解释如何独立作答，不提供任何 Core144 真实题目的答案。

## 1. Phase2 到底在标什么

Phase2 判断 Candidate 的核心事实能否被**本行提供的冻结证据**支持，并把“总体事实、文档版本、机关角色、最低证据路径、实际证据使用、行级问题、额外独立错误、证据充分性”分开记录。

Phase1 只看 Candidate，不看 Evidence；Phase2 才允许查看本行的冻结 E1 和可选 E2。Phase2 不会覆盖或修改已提交的 Phase1。即使第二阶段发现第一阶段漏掉题文缺陷，也只能在 `phase2_issue` 中如实登记。

你可以看：

- 自己的 Phase2 Excel；
- 当前行的 Candidate、E1、可选 E2；
- 工作簿中与当前行对应的冻结证据全文、快照标识和官方链接；
- 本手册与工作簿自带说明。

你不能：

- 自己百度、搜索法规库或寻找第三份证据；
- 借用别行 Evidence 回答当前行；
- 使用 ChatGPT、豆包、Claude、DeepSeek 等 AI 替本人判断；
- 查看、讨论或猜测另一位标注人的答案；
- 猜 Clean / Poison / Hard Negative、HKP、S1/S2/S3 或实验意图；
- 根据 `blind_id`、题序、措辞风格猜答案；
- 修改题目、Evidence、ID、行列、工作表或下拉值。

## 2. 一行八步判断法

| 步骤 | 固定动作 | 关键提醒 |
|---|---|---|
| 1 | 先读 Candidate，再读本行 E1/E2 | 先确定 Candidate 自己说了什么；Evidence 元数据不能倒灌出 Candidate 没说的主张。 |
| 2 | 判断 Evidence 是否足够 | 不足就记录不足；不猜、不补搜。 |
| 3 | 填 `overall_fact_status` | 顺序：能否判断 → 是否冲突 → 是否依赖历史/版本范围 → 当前一致。 |
| 4 | 独立填 `version_claim_status` | 先只看 Candidate 是否有文档级版本主张，再用 Evidence 判对错。 |
| 5 | 独立填 `authority_claim_status` | 识别制定、公布、通过、修订、主管等具体角色；普通执行者不是自动的 authority。 |
| 6 | 仅在 overall 为 `FACTUAL_CONFLICT` 时填最低证据路径 | 文内已冲突用 ZERO；单份够用 ONE；必须联合才用 MULTI；其余 NOT_APPLICABLE。 |
| 7 | 填 `evidence_selection` | 记录本人实际用了 NONE / E1 / E2 / E1+E2，不是理论最低需求。 |
| 8 | 填 issue、secondary error、sufficiency 和 reason | 最后做组合检查；`phase2_reason` 每行必填。 |

## 3. 提交前强制组合检查（先看这一表）

| 条件 | 必须满足 |
|---|---|
| `overall_fact_status != FACTUAL_CONFLICT` | `minimum_external_evidence_needed = NOT_APPLICABLE` |
| `overall_fact_status = FACTUAL_CONFLICT` 且本人锁定的 Phase1 `local_internal_conflict = YES` | `minimum_external_evidence_needed = ZERO_EXTERNAL_EVIDENCE_REQUIRED` |
| `overall_fact_status = LEGITIMATE_VERSION_OR_HISTORY` | `version_claim_status` 可以是 `NOT_PRESENT` |
| `version_claim_status = NOT_PRESENT` | 不代表 overall 必须是 `CURRENTLY_CONSISTENT` |
| `overall_fact_status = FACTUAL_CONFLICT` | version / authority 仍可分别为 `PRESENT_CORRECT` |
| `evidence_selection = E1+E2` | 不代表 minimum 必须为 `MULTI_EVIDENCE_OR_VERSION_CHAIN` |
| 普通 Candidate 与 Evidence 不一致 | 通常是 `FACTUAL_CONFLICT`，`phase2_issue` 仍可为 `NONE` |
| Evidence 真正不足 | 不得硬判冲突；使用 `INSUFFICIENT_EVIDENCE` 及相应 issue/sufficiency |
| 判断 version presence | 必须先做 Candidate-only test，不能先看 Evidence 沿革 |
| host / 官方转载页 | 不自动决定 issuer、制定或公布机关 |
| E2 为空 | 不自动是 `EVIDENCE_MISSING` |
| live URL 打不开但冻结材料足够 | 不自动是 `SOURCE_UNREACHABLE` |
| `possible_accidental_secondary_error = YES` | 必须能指出第二个独立 factual atom |
| `phase2_issue != NONE` 或 sufficiency 非充分 | `phase2_reason` 必须具体写明缺口 |

## 4. Excel 20 列地图与填写位置

| 列 | 字段 | 操作 |
|---|---|---|
| A | `blind_id` | 只读，不改 |
| B | `candidate_text` | 只读，不改 |
| C–F | `E1_title` / `E1_excerpt` / `E1_official_url` / `E1_snapshot_ref` | 只读，当前行第一证据 |
| G–J | `E2_title` / `E2_excerpt` / `E2_official_url` / `E2_snapshot_ref` | 只读，可整组为空 |
| K–R | 八个枚举字段 | 必填，只用英文 canonical enum |
| S | `phase2_reason` | 每行必填 |
| T | `reviewer_note` | 可选，不代替 reason |

不要添加中文机器值，不要自行增加列。A/B 两份工作簿的列结构和枚举完全相同，但 ID 与行序各自独立，不能互换或排序。

## 5. `blind_id`（盲题号）

它在问：当前行是哪一道题。它不在问：题目属于什么类别。保持原值，不改写、不重排、不据此猜角色。

允许内容只有工作簿预填的原 ID。常见错误是复制另一人的 ID 或排序后让 ID 与 Candidate 错位。

- 虚构短例 1：`VX-001` 只用于定位本行，不能据编号猜“第一个就是正确项”。
- 虚构短例 2：即使两个 ID 看起来相近，也不能把一行的 E1 借给另一行。

## 6. `candidate_text`（候选文本）

它在问：本行需要核验的原始陈述是什么。它不在问：你希望它怎样写才更自然。只读，不润色、不删句、不补条件。

判断时拆出核心命题、时间、条件、对象、文档版本词和机关角色词。若到 Phase2 才发现主体无法唯一理解，原文仍不改，使用 `LATE_DISCOVERED_CANDIDATE_DEFECT`。

- 虚构短例 1：“甲馆每周一闭馆”是实体日程主张。
- 虚构短例 2：“现行《甲馆规则》自2030年废止”同时包含文档状态和转换主张。

## 7. `E1_title`（第一证据标题）

它帮助识别 E1 是哪一份材料，不单独证明所有事实。标题中的“现行”“修订”属于证据身份信息，不能反向制造 Candidate 的 version claim。

- 虚构短例 1：标题为“甲馆规则（2030修订）”，Candidate 只说“门票八元”，version presence 仍先只看 Candidate。
- 虚构短例 2：标题写“乙委员会转载”，不能仅凭标题把乙认作原始制定机关。

## 8. `E1_excerpt`（第一证据冻结摘录）

它是 E1 中为本行冻结的可读片段。先核对对象、条件、时间和句法范围；不要只找相同数字。摘录不足时可看工作簿提供的同题冻结全文，但不能外扩到别行或自行搜索。

- 虚构短例 1：摘录“未满十岁免票”，不能支持“十岁免票”，边界不同。
- 虚构短例 2：摘录只写公布日期，不能自动证明生效日期。

## 9. `E1_official_url`（第一证据官方链接）

它用于核读与溯源，不是自由搜索入口。网页 host 不等于制定机关。链接暂时打不开时先用冻结摘录/快照；冻结材料足够就继续作答。

- 虚构短例 1：甲政府网站转载乙委员会文件，URL 域名是甲也不能推出甲制定。
- 虚构短例 2：live URL 超时，但冻结全文完整覆盖本题，不自动填 `SOURCE_UNREACHABLE`。

## 10. `E1_snapshot_ref`（第一证据快照标识）

它用于把当前摘录与冻结材料对应起来，不是事实答案、版次标签或让你修改的 SHA。只读。

- 虚构短例 1：快照编号含“2030”不等于 Candidate 提出2030版主张。
- 虚构短例 2：快照与 URL 当前页面有变化时，以提供的冻结范围作答，并在确有必要时说明。

## 11. `E2_title`（第二证据标题）

E2 是可选第二证据；整组为空是合法状态。E2 存在不表示必须选 `E1+E2`，也不表示 minimum 必然 MULTI。

- 虚构短例 1：E1 已直接给数值，E2 只补充文档状态；总体冲突最低仍可能 ONE。
- 虚构短例 2：E2 为空，但 E1 完整覆盖命题，可判 `SUFFICIENT`。

## 12. `E2_excerpt`（第二证据冻结摘录）

解释方法与 E1 excerpt 相同。比较 E1/E2 时先查时间、对象、条件、文档身份与版本关系；表面不同不等于来源冲突。

- 虚构短例 1：E1 是旧规则五日，E2 是新规则七日，有明确版本链时可共同支持合法历史。
- 虚构短例 2：E1/E2 同版本同条件却分别写五日/七日且无法调和，才考虑 `SOURCE_CONFLICT`。

## 13. `E2_official_url`（第二证据官方链接）

只用于本行 E2。不得沿链接搜索其他文档，也不得用另一行的 E2 替当前行补证。

- 虚构短例 1：E2 URL 为空时，不得自行搜索“类似规定”补成 E2。
- 虚构短例 2：E2 页面能打开，但内容不覆盖 Candidate 核心命题，仍可能证据不足。

## 14. `E2_snapshot_ref`（第二证据快照标识）

只读，用于确认 E2 冻结身份。它不能替代对摘录/全文的实际阅读。

- 虚构短例 1：两个 snapshot_ref 不等于两份证据都“必要”。
- 虚构短例 2：E2 snapshot 为空与 E2 整组为空一致时，不是格式错误。

## 15. `overall_fact_status`（总体事实状态）

它问 Candidate 的**核心命题整体**在当前表达范围内属于哪一种，不问句子是否自然，也不等同 version 或 authority 子字段。

| 允许值 | 何时选择 | 不能这样理解 |
|---|---|---|
| `CURRENTLY_CONSISTENT` | 冻结证据支持核心事实，且不需依赖历史/旧版限定才成立 | “没有反证”就算支持 |
| `LEGITIMATE_VERSION_OR_HISTORY` | 核心事实正确，但其意义或真值实质依赖历史时期、旧状态、版本语境或跨时间关系 | 历史就是错误；有年份就必选 |
| `FACTUAL_CONFLICT` | 核心事实被证据否定，或文本内部已确认冲突，且不能由合法时间、条件、范围、版本或例外调和 | Candidate 与某一片段措辞不同就算冲突 |
| `INSUFFICIENT_EVIDENCE` | 给定材料不足以可靠决定核心事实 | 凭常识、记忆或 AI 猜一个值 |

判断顺序：证据能否可靠判断？不能 → `INSUFFICIENT_EVIDENCE`。能 → 核心命题是否不可调和地被否定？是 → `FACTUAL_CONFLICT`。否 → 正确性是否实质依赖历史/版本限定？是 → `LEGITIMATE_VERSION_OR_HISTORY`。否则 → `CURRENTLY_CONSISTENT`。

虚构短例：

1. “青舟馆现收八元”，E1 明示当前八元 → `CURRENTLY_CONSISTENT`。
2. “青舟馆在2030年曾收五元”，E1 支持当年五元、E2 支持后来八元 → `LEGITIMATE_VERSION_OR_HISTORY`。
3. “上限九人”，E1 同范围明确七人 → `FACTUAL_CONFLICT`。
4. “2030年修订”，E1/E2 都没有沿革 → `INSUFFICIENT_EVIDENCE`。

常见混淆：overall 判断核心事实，version 判断候选有没有文档级版本主张；合法历史完全可以 version `NOT_PRESENT`。

## 16. 文档版本判断专章：`version_claim_status`

### 16.1 它在问什么

它只判断 Candidate 是否提出**文档级**的版本事件、身份、状态、关系或转换，并在存在时用证据核对。包括修订/修改、原版/修订版/某年版、现行版/历史版、废止、替代、前任/后继、supersession、施行/失效转换、版本绑定，以及明确的 amendment-decision identity。

它不评价金额、比例、天数、处罚、适用条件、普通流程等实体内容。实体内容错，不自动让 version 错。

### 16.2 四个值

| 允许值 | 操作性定义 |
|---|---|
| `NOT_PRESENT` | Candidate 没有文档级版本主张。必须先只看 Candidate 决定。 |
| `PRESENT_CORRECT` | Candidate 有版本主张，且冻结证据支持。 |
| `PRESENT_INCORRECT` | Candidate 有版本主张，且冻结证据明确否定该版本命题。 |
| `PRESENT_EVIDENCE_INSUFFICIENT` | Candidate 有版本主张，但冻结证据不足以判断对错。 |

### 16.3 Candidate-only 四问

1. Candidate 是否明确说了文档修订、版次、状态、关系或生效/失效转换？
2. 它是否只是提到年份、实体数值、普通通过/公布或业务日期？
3. 我是否因为 Evidence 页写“现行有效/修订日期”而给 Candidate 补了主张？
4. 我是否把版本、实体内容和机关角色分别判断？

### 16.4 六个高危边界

- **年份 ≠ Version。**“2030年，《甲规则》规定八元”可只是历史时间背景；“2030年版《甲规则》”才明确版次。
- **Evidence metadata 不得倒灌。**Evidence 写“现行有效、发布日期、历史沿革”，Candidate 未提出版本语义时仍可 `NOT_PRESENT`。
- **Historical ≠ Document Version Claim。**“2030年票价五元”可 overall 合法历史、version `NOT_PRESENT`。
- **“目前”不一定是 Version。**“目前票价八元”通常是实体数值现状；“现行《甲规则》”是文档状态。
- **普通通过/公布/发布不自动是 Version。**“甲会议通过、乙机关公布”主要是 authority/publication；除非同时明确修订、替代、版本或转换。
- **修改决定标题属于 Version。**“《关于修改〈甲规则〉的决定》”标题自身带 modification identity，即使没写年份也有 version claim。

虚构短例：

1. “2030年青岚馆限额八人。”→ `NOT_PRESENT`，年份只限定实体事实。
2. “《青岚馆规则》2030年修订版限额八人。”→ version present，再用证据选正确/错误/不足。
3. “目前补贴五百元。”→ 通常 `NOT_PRESENT`。
4. “现行《补贴办法》仍有效。”→ version state present。

## 17. 机关角色判断专章：`authority_claim_status`

它问 Candidate 是否明确声称某机构是制定、发布/公布、通过、修订、批准、主管/监管等制度性角色，并核对这个**具体角色**。issuer、page publisher、promulgating authority、adopting authority、amending authority、approving authority、competent authority、host 和 official repost institution 必须分开。

| 允许值 | 操作性定义 |
|---|---|
| `NOT_PRESENT` | Candidate 没有上述机关角色主张。普通办理、支付、审核、出具证明等 actor 通常不属于此字段。 |
| `PRESENT_CORRECT` | 有明确角色主张，证据支持该角色。 |
| `PRESENT_INCORRECT` | 有明确角色主张，证据明确否定或指向另一机关。 |
| `PRESENT_EVIDENCE_INSUFFICIENT` | 有明确角色主张，但冻结材料不足以判断。 |

Authority 三问：

1. 这个机构是发布/通过/修订/主管角色，还是普通业务执行者？
2. 我是否把网页 host 或转载方误当原始 issuer？
3. E1/E2 是否真的证明 Candidate 声称的那个角色，而不只是出现同一机构名？

高频错误：

- “学校审核材料”“医院出具证明”“窗口办理申请”“单位支付费用”通常是实体业务角色，不自动产生 authority claim。
- 网页在甲政府站点上，不代表甲制定/公布正文。
- 多个机关可以分别承担通过、公布、批准、转载等角色，不自动冲突。

虚构短例：

1. “服务中心核验预约”→ 普通执行者，`NOT_PRESENT`。
2. “《甲办法》由乙委员会公布”且 E1 署名乙 → `PRESENT_CORRECT`。
3. 甲官网转载正文署名乙，Candidate 称甲制定 → `PRESENT_INCORRECT`。
4. Candidate 称甲主管，但材料只证明甲转载 → `PRESENT_EVIDENCE_INSUFFICIENT`。

## 18. Overall / Version / Authority 三维独立表

| Candidate 情形（均为虚构） | overall | version | authority | 为什么 |
|---|---|---|---|---|
| 修订事件与公布机关都正确，但限额数字错 | FACTUAL_CONFLICT | PRESENT_CORRECT | PRESENT_CORRECT | 实体内容错不联动两个子字段 |
| 修订年份错，公布机关正确 | FACTUAL_CONFLICT | PRESENT_INCORRECT | PRESENT_CORRECT | 版本错不代表机关错 |
| 修订发生正确，但修订机关写错 | FACTUAL_CONFLICT | PRESENT_CORRECT | PRESENT_INCORRECT | 版本事件与机关角色分开 |
| 合法比较两个时期数值，但没说文档版本 | LEGITIMATE_VERSION_OR_HISTORY | NOT_PRESENT | NOT_PRESENT | 历史维度不自动制造版本/机关主张 |
| 现行规则正确，普通窗口负责办理 | CURRENTLY_CONSISTENT | NOT_PRESENT | NOT_PRESENT | 业务 actor 不是 authority |
| 核心数值已被 E1 否定，但修订身份没材料 | FACTUAL_CONFLICT | PRESENT_EVIDENCE_INSUFFICIENT | NOT_PRESENT | 已确定的核心冲突不必随子字段改成总体不足 |

## 19. `minimum_external_evidence_needed`（最低外部证据）

它只问：确认**总体 factual conflict** 最少需要多少外部证据。它不问填完全部子字段需要几份，也不问你实际打开几份。

| 允许值 | 必须满足 |
|---|---|
| `ZERO_EXTERNAL_EVIDENCE_REQUIRED` | overall=FACTUAL_CONFLICT，且本人已锁 Phase1 对应行 `local_internal_conflict=YES`；文本自身已足够确认冲突。 |
| `ONE_OFFICIAL_EVIDENCE` | 文内不能自行确认，但 E1 或 E2 任意一份单独就足以确认总体冲突。 |
| `MULTI_EVIDENCE_OR_VERSION_CHAIN` | E1 单独不足、E2 单独也不足，只有联合证据/版本链才足以确认总体冲突。 |
| `NOT_APPLICABLE` | overall 不是 FACTUAL_CONFLICT，包括当前一致、合法历史、证据不足。 |

固定决策树：

1. overall 是否 `FACTUAL_CONFLICT`？否 → `NOT_APPLICABLE`。
2. 本人 Phase1 是否已锁 `local_internal_conflict=YES`？是 → `ZERO_EXTERNAL_EVIDENCE_REQUIRED`。
3. 暂时只留 E1，能否确认总体冲突？能 → `ONE_OFFICIAL_EVIDENCE`。
4. 暂时只留 E2，能否确认总体冲突？能 → `ONE_OFFICIAL_EVIDENCE`。
5. 两份各自不足、联合才够？是 → `MULTI_EVIDENCE_OR_VERSION_CHAIN`。
6. 联合仍不够 → overall 应回到 `INSUFFICIENT_EVIDENCE`，minimum 为 `NOT_APPLICABLE`。

虚构短例：

- Candidate 同时说同一票种“收费”和“免费”，Phase1 已判 YES → ZERO。
- E1 一条就写明上限七人而 Candidate 称九人 → ONE。
- E1 只给旧值、E2 只给新值，必须联读才能否定 Candidate 的变化方向 → MULTI。
- Candidate 得到支持或材料不足 → NOT_APPLICABLE。

## 20. `evidence_selection`（实际使用证据）

它记录你本人实际用过什么：`NONE`、`E1`、`E2`、`E1+E2`。没有使用的不能为了“完整”而填入；E2 为空时不能选 E2 或 E1+E2。

### Minimum 与 Selection 对照

| minimum | selection | 是否可能合法 | 例子 |
|---|---|---|---|
| ZERO | E1 | 是 | 文内已冲突，但你仍用 E1 核对版本子字段 |
| ZERO | E1+E2 | 是 | 文内冲突已足够，两份证据只用于核查 |
| ONE | E1+E2 | 是 | E1 单独已足够，你又实际读了 E2 |
| MULTI | E1+E2 | 通常必须 | 只有联读才能确认总体冲突 |
| NOT_APPLICABLE | E1 | 是 | 当前一致，实际只用 E1 |
| NOT_APPLICABLE | E1+E2 | 是 | 合法历史或不足判断中实际用了两份 |

**实际读两份 Evidence ≠ MULTI。**A01 只用 E1、B01 用 E1+E2，也不自动表示有人错；selection 是个人过程字段。`phase2_reason` 引用了哪份证据，selection 就必须包含它。

## 21. `phase2_issue`（第二阶段行级问题）

| 允许值 | 使用条件 | 不能误用 |
|---|---|---|
| `NONE` | 本行题文/证据/字段接口没有独立问题；普通事实冲突通常仍是 NONE | 不能因 Candidate 错就填 OTHER |
| `SOURCE_UNREACHABLE` | 本行所需来源及给定冻结回退均不可访问，且确实阻碍判断 | live URL 临时失败但快照足够，不用此值 |
| `SOURCE_CONFLICT` | E1/E2 在同一文档身份、时间、对象、条件下互相不可调和 | Candidate 与 Evidence 不同不是来源冲突 |
| `EVIDENCE_MISSING` | 回答明确命题所需的冻结证据本应提供但本行缺失 | E2 空但 E1 已足够，不是 missing |
| `LATE_DISCOVERED_CANDIDATE_DEFECT` | Phase2 才发现 Candidate 自身主体缺失、严重歧义或其他题文缺陷 | 普通事实错误不是题文缺陷 |
| `OTHER` | 真实的其他 row-level candidate/evidence/schema-interface 问题，且前五类都不适用 | 账号、会话、发送或路由事故不是行级 OTHER |

虚构短例：

1. Candidate 称九人、E1 明确七人 → overall 冲突，issue 通常 `NONE`。
2. E1/E2 同版同条同条件分别写七人/九人且无更正关系 → `SOURCE_CONFLICT`。
3. Candidate 明示2030修订，但材料没有沿革 → `EVIDENCE_MISSING`。
4. Candidate 只有“该办法”且无唯一主体 → `LATE_DISCOVERED_CANDIDATE_DEFECT`。

## 22. `possible_accidental_secondary_error`（可能的独立次生错误）

它问：除当前核心问题外，Candidate 是否还有第二个独立、未经支持的 factual atom。

| 允许值 | 定义 |
|---|---|
| `YES` | 能明确指出第二个独立错误原子及其证据依据。 |
| `NO` | 没有第二独立错误；或只是同一错误的重复/直接后果。 |
| `UNCERTAIN` | 存在额外独立主张，但冻结证据不足以判断它是否也错。 |

不算第二错误：

- 同一数值错误换一种说法重复；
- 一个内部矛盾的两端；
- 同一个错误版本状态的直接结果；
- 同一错误日期在标题和正文重复。

虚构正反例：

1. 核心限额九人错，且公布机关甲也错 → `YES`，两个独立原子。
2. “既收费又免费”是一个内部冲突的两端 → `NO`。
3. 同一句两次重复错误“九人” → `NO`。
4. 错称2030废止，并据此说2031不再适用 → 通常是同一版本错误的直接后果，`NO`。
5. 核心数字已被否定，另声称修订年但没有沿革 → `UNCERTAIN`。
6. 核心数字错，但正确写出机关 → `NO`，正确事实不是次生错误。

## 23. `evidence_sufficiency`（证据充分性）

| 允许值 | 操作性定义 |
|---|---|
| `SUFFICIENT` | 当前冻结材料足以完成本行所需 Phase2 判断。 |
| `INSUFFICIENT` | 缺少关键依据，无法可靠完成一个或多个必要判断。 |
| `UNCERTAIN` | 无法稳定判断材料是否足够，例如范围或身份对应关系仍不清楚。 |

“页面能打开”不等于充分；“官方网页”也不等于覆盖核心命题。相反，live URL 打不开但冻结全文足够时，仍可 `SUFFICIENT`。材料不足时不得自行搜索。

虚构短例：

1. E1 明确同对象同条件数值 → `SUFFICIENT`。
2. Candidate 声称修订年，材料完全无沿革 → `INSUFFICIENT`。
3. 材料似乎相关，但无法确认是否同一文档版本 → `UNCERTAIN`。

## 24. `phase2_reason`（必填理由）

每行必须写清：Candidate 声称什么；E1/E2 显示什么；为什么得到 overall、version、authority 和 minimum。建议 2–4 句，具体到对象、数值、条件、时间或角色。

推荐模板：

> Candidate 声称【____】；E1/E2 显示【____】，因此 overall 为【____】。Candidate【有/无】文档版本主张，version 为【____】；【有/无】机关角色主张，authority 为【____】。确认总体冲突最低需要【____】。

| 好理由 | 坏理由 | 为什么 |
|---|---|---|
| “Candidate 称比例40%，E1第五条为30%；E1单独可否定核心数值。文本无版本或机关主张，故 overall=FACTUAL_CONFLICT、version/authority=NOT_PRESENT、minimum=ONE。” | “根据资料。” | 坏理由没有具体命题与依据 |
| “E1旧值五、E2新值七；Candidate 说从五降到四，必须联读两时期才能确认方向错误，minimum=MULTI。” | “感觉变化方向不对。” | 坏理由不可审计 |
| “Candidate 同时说同一票种收费与免费，Phase1已判内部冲突；外证不是确认冲突所必需，minimum=ZERO。” | “明显有毒。” | 不得猜实验角色 |
| “Candidate 明示2030修订，但E1/E2都无沿革，无法判修订年；overall与version均记不足。” | “应该不是2030。” | 不能凭记忆猜 |
| “E1正文署名乙制定，甲仅转载，故甲制定主张错误；host不等于issuer。” | “网上查到是乙。” | 不得引用包外搜索 |
| “E1与E2同版同条同条件分别记二份和三份，且无更正/范围差异，来源无法调和。” | “AI认为E2更可信。” | 禁止 AI 代判、不能擅选 |

## 25. `reviewer_note`（可选补充说明）

它用于补充 reason 放不下的操作性信息，例如“不足只涉及版本沿革，核心数值反证已充分”。可以留空。它不能替代任何枚举，也不能把必填理由全部移到此列。

- 虚构短例 1：reason 已完整，note 留空。
- 虚构短例 2：overall 已确定冲突，但 version 缺沿革，可在 note 明确“不足仅针对 version 子字段”。

## 26. Evidence 使用规则总表

1. 只用当前行 E1、可选 E2 与工作簿提供的同题冻结全文。
2. E2 整组为空表示本行没有第二份可用 Evidence；不得自找或借用。
3. E2 为空不自动是 `EVIDENCE_MISSING`；要看 E1 是否已覆盖判断需求。
4. live URL 是核读入口，不是自由搜索许可。
5. live URL 暂时失败但冻结材料完整，不自动 `SOURCE_UNREACHABLE`。
6. 页面可打开但不覆盖核心命题，仍可能 `INSUFFICIENT` / `EVIDENCE_MISSING`。
7. E1/E2 表面不同，先查时间、对象、条件、版本和文档身份。
8. 不用另一行 Evidence，不让浏览器搜索建议或外部摘要补题。

## 27. 高危歧义 Top 20

| # | 错误理解 | 正确理解 | 判断方法 | 虚构短例 |
|---:|---|---|---|---|
| 1 | 有年份就 version PRESENT | 年份可能只是事实时间背景 | 先问是否指文档版次/状态/转换 | “2030年票价五元”通常 NOT_PRESENT |
| 2 | historical 就是文档版本 | 历史总体与版本主张是不同维度 | 去掉时间后看事实意义，再单独做 Candidate-only version test | “2030年曾开放”可合法历史 + version NOT_PRESENT |
| 3 | Evidence 写修订就让 Candidate 有 version | Evidence 只能验证，不能制造主张 | 遮住 Evidence 元数据只读 Candidate | 题文只说“上限七人”仍可能 NOT_PRESENT |
| 4 | “目前”都表示现行文档 | “目前”可只修饰实体数值 | 看修饰对象是数值还是文档状态 | “目前票价八元”通常 NOT_PRESENT |
| 5 | “现行《某法》”没有版本主张 | 它明确声称文档 current state | 识别“现行”是否绑定文档 | “现行《甲规则》”是 version present |
| 6 | 通过/公布/发布自动 version | 普通 publication facts 主要是 authority | 看是否还有修订/替代/转换语义 | “甲通过、乙公布”可 version NOT_PRESENT |
| 7 | 修改决定标题也只是普通标题 | 标题本身有 amendment identity | 读完整文档名 | “关于修改〈甲规则〉的决定”是 version present |
| 8 | 出现机构就是 authority | 普通业务 actor 不自动是制度性机关角色 | 问它在做业务还是制定/公布/主管 | “窗口办理”通常 NOT_PRESENT |
| 9 | 官方网站 host 就是 issuer | host/repost 与原始机关不同 | 查正文署名和角色 | 甲站转载乙文件不能推出甲制定 |
| 10 | 多个机关就是机关冲突 | 角色不同可同时成立 | 对齐通过、公布、批准、修订等角色 | 甲通过、乙公布不矛盾 |
| 11 | overall 错则 version/authority 都错 | 三个维度独立 | 分解 substantive/version/authority atoms | 数字错但版次、机关可都正确 |
| 12 | minimum 就是自己实际看了几份 | minimum 是确认总体冲突的最小路径 | 做 ZERO/E1-only/E2-only/joint ablation | 看两份但 E1 单独够，minimum ONE |
| 13 | 实际读两份必然 MULTI | 两份各自是否必要才决定 MULTI | 分别遮住 E1/E2 测试 | E2 只作旁证，仍 ONE |
| 14 | Candidate 错就有 issue | 普通事实错是任务内容，不是题目缺陷 | 问是否另有行级材料/接口问题 | 数值错可 issue NONE |
| 15 | Candidate 与 Evidence 不同就是 SOURCE_CONFLICT | SOURCE_CONFLICT 是 E1 与 E2 互相不可调和 | 比较来源之间而非题文与来源 | Candidate九、E1七是事实冲突 |
| 16 | live URL 失败就 SOURCE_UNREACHABLE | 冻结材料足够时仍可判断 | 检查 excerpt/snapshot/full text | URL超时但快照完整，不用 issue |
| 17 | Evidence 不足可以凭常识选 | 不足必须显式记录 | 禁止包外知识，说明缺口 | 无沿革不猜修订年 |
| 18 | 核心错误本身就是 secondary error | secondary 必须是第二独立原子 | 分离原子与证据 | 一个错误数值不是 secondary |
| 19 | 内部冲突两端是两个错误 | 两端共同构成一个冲突 | 看是否存在第三个独立原子 | 同一票种收费/免费，secondary NO |
| 20 | E2 为空必然 Evidence 缺失 | 单证据可能已经充分 | 看本行判断需求 | E1直接给答案，E2空仍充分 |

## 28. 特殊标注情况 A–J

### A. 两份 Evidence 都支持 Candidate，但时期不同

先判断 Candidate 是否正确限定时期。不同数值可共同支持变化；不要看到不同就判冲突。正确且依赖历史范围时用 `LEGITIMATE_VERSION_OR_HISTORY`。

### B. E1 支持，E2 看似不同

依次核对时间范围、适用对象、条件、版本身份和是否不同文档。只有同范围且无法调和，才考虑 `SOURCE_CONFLICT`。

### C. Candidate 同时有多个 factual atom

分别标出 substantive、version、authority。overall 看核心整体，两个子字段各自判断；secondary 只在另有独立错误时使用。

### D. Version 正确但实体数值错误

可以 `overall=FACTUAL_CONFLICT`、`version=PRESENT_CORRECT`。不要为了“整齐”把 version 改错。

### E. Authority 正确但 Version 错

可以 `authority=PRESENT_CORRECT`、`version=PRESENT_INCORRECT`。两个字段不联动。

### F. Candidate 是合法旧规定

若历史范围明确且 Evidence 支持，不因当前规则不同而判冲突；通常 overall 为合法历史。

### G. Candidate 把旧规定说成“现行”

旧值本身曾真实不等于当前绑定正确。若证据链否定 current binding，属于真正 version-state 问题。

### H. 两份证据都能打开，但没有覆盖核心命题

来源数量和可访问性不等于充分性。填总体不足，并依据具体缺口使用 `EVIDENCE_MISSING` / sufficiency。

### I. Candidate 自己已矛盾，Evidence 又提供信息

minimum 仍可 ZERO；selection 如实填 E1/E2/E1+E2。外证用于子字段不改变文内最低路径。

### J. Phase2 才发现 Candidate 主体无法唯一理解

不替题文补主体，不硬判真伪。使用 `LATE_DISCOVERED_CANDIDATE_DEFECT`，说明具体缺失。

## 29. 完整虚构教学案例（01–30）

以下每例均为**虚构教学案例，不属于 Core144 数据集**。名称、制度和证据均为教学构造，不对应 D1 题目；不得把例中答案机械套到真实行。

### 案例 01：当前事实一致，E2 为空

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《云帆阅览规则》规定，普通读者每次可借三册。”
虚构 E1：同名规则正文明确“每次三册”。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 核心借阅数量受 E1 支持 |
| version_claim_status | NOT_PRESENT | 只陈述实体数量，没有版次/状态 |
| authority_claim_status | NOT_PRESENT | 没有机构角色 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非事实冲突 |
| evidence_selection | E1 | 只使用 E1 |
| phase2_issue | NONE | E2 空不妨碍判断 |
| possible_accidental_secondary_error | NO | 只有一个正确核心原子 |
| evidence_sufficiency | SUFFICIENT | E1 已覆盖核心 |

`phase2_reason`：“Candidate 称每次三册，E1 同范围明确三册，核心事实受支持；文本没有文档版本或机关角色主张，minimum 不适用。”
最容易误判：因为 E2 为空而填 `EVIDENCE_MISSING`。

### 案例 02：当前一致并有正确公布机关

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《月桥参观办法》由甲文化委员会公布，预约期为两日。”
虚构 E1：正文署名甲文化委员会并明确两日。E2：数据库记录同一文件。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 两项事实均受支持 |
| version_claim_status | NOT_PRESENT | 普通公布事实不自动是版本 |
| authority_claim_status | PRESENT_CORRECT | 明示且证明公布机关 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非冲突 |
| evidence_selection | E1 | E1 已足够且实际只用 E1 |
| phase2_issue | NONE | 无行级缺陷 |
| possible_accidental_secondary_error | NO | 没有额外错误 |
| evidence_sufficiency | SUFFICIENT | E1 覆盖内容与机关 |

`phase2_reason`：“E1 同时支持两日预约期和甲委员会公布角色；Candidate 未提出修订、版次或状态，version=NOT_PRESENT。”
最容易误判：把“公布”自动记为 version present。

### 案例 03：合法历史，但没有文档版本主张

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“2030年，星沙馆普通票价为五元。”
虚构 E1：2030年公告记五元。E2：2032年公告记八元。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | LEGITIMATE_VERSION_OR_HISTORY | 五元只在2030历史范围成立 |
| version_claim_status | NOT_PRESENT | 年份限定票价，不是文档版次 |
| authority_claim_status | NOT_PRESENT | 未声称机关角色 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 合法历史不是冲突 |
| evidence_selection | E1+E2 | 两份均用于确认时期变化 |
| phase2_issue | NONE | 时间差异可调和 |
| possible_accidental_secondary_error | NO | 无第二错误 |
| evidence_sufficiency | SUFFICIENT | 两时期证据清楚 |

`phase2_reason`：“E1 支持2030年五元，E2 只说明后来改为八元，不否定历史事实；年份修饰票价而非文档版本。”
最容易误判：把 historical 自动改成 version `PRESENT_CORRECT`。

### 案例 04：合法旧版，明确版本身份

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《青岚入园规则》2028年版规定闭园时间为18时。”
虚构 E1：2028年版正文为18时。E2：2031年修订版改为19时。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | LEGITIMATE_VERSION_OR_HISTORY | 18时在明确旧版成立 |
| version_claim_status | PRESENT_CORRECT | 明示2028年版且受支持 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 不是冲突 |
| evidence_selection | E1+E2 | 联读确认旧/新版边界 |
| phase2_issue | NONE | 版本差异有合法关系 |
| possible_accidental_secondary_error | NO | 无额外错误 |
| evidence_sufficiency | SUFFICIENT | 两版身份和数值清楚 |

`phase2_reason`：“E1 的2028年版支持18时，E2 后续19时不否定旧版；Candidate 明示版次，version=PRESENT_CORRECT。”
最容易误判：用当前19时把合法旧版判成 FACTUAL_CONFLICT。

### 案例 05：文本内部冲突，minimum 为 ZERO

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“同一种夜场票既一律收费，也一律免费。”
虚构 E1：说明该票收费。E2：空。本人 Phase1 已锁 `local_internal_conflict=YES`。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 同主体同条件的收费/免费不可同时成立 |
| version_claim_status | NOT_PRESENT | 无文档版本主张 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | ZERO_EXTERNAL_EVIDENCE_REQUIRED | 文本自身已确认冲突 |
| evidence_selection | NONE | 本例未用外证确认冲突 |
| phase2_issue | NONE | 错误是正常核验对象，不是题目缺陷 |
| possible_accidental_secondary_error | NO | 冲突两端共同构成一个错误 |
| evidence_sufficiency | SUFFICIENT | 文内冲突足够完成核心判断 |

`phase2_reason`：“Candidate 对同一票种同一条件同时断言收费和免费，Phase1 已锁内部冲突；无需外部证据即可确认，minimum=ZERO。”
最容易误判：把矛盾两端算成两个 secondary errors。

### 案例 06：ZERO 与 E1+E2 可以并存

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“同一许可证在2032年1月1日既生效又不生效。”
虚构 E1：许可证生效记录。E2：发布记录。本人 Phase1 已锁 `local_internal_conflict=YES`，两份均实际核读。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 文内同日状态冲突 |
| version_claim_status | PRESENT_INCORRECT | 明示生效状态且其中含错误断言 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | ZERO_EXTERNAL_EVIDENCE_REQUIRED | 确认总体冲突无需外证 |
| evidence_selection | E1+E2 | 实际读了两份核查子字段 |
| phase2_issue | NONE | 无独立材料问题 |
| possible_accidental_secondary_error | NO | 两端是同一状态冲突 |
| evidence_sufficiency | SUFFICIENT | 文内和证据均可判 |

`phase2_reason`：“同一许可证同日被断言生效和不生效，文内已足够确认；E1/E2 仅用于核对状态与身份，故 selection=E1+E2 但 minimum 仍 ZERO。”
最容易误判：看到 selection=E1+E2 就把 minimum 改成 MULTI。

### 案例 07：单份证据即可否定数值

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《白鹭寄存规则》规定每人最多九个柜格。”
虚构 E1：同条同条件明确最多七个。E2：文件状态页。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 九与七同范围冲突 |
| version_claim_status | NOT_PRESENT | 数量不是版本 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 单独足够 |
| evidence_selection | E1+E2 | 两份均实际读，E2 仅旁证 |
| phase2_issue | NONE | 普通事实错误 |
| possible_accidental_secondary_error | NO | 只有一个数值错误 |
| evidence_sufficiency | SUFFICIENT | E1 足以核验 |

`phase2_reason`：“Candidate 称九格，E1 同范围明确七格；E1 单独即可否定核心数值，E2 只作身份旁证，因此 minimum=ONE、selection=E1+E2。”
最容易误判：因实际读两份而填 MULTI。

### 案例 08：条件删除造成事实冲突

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“访客只要提前一天申请，就一定可以进入资料室。”
虚构 E1：规定“提前一天申请并持有效研究证”方可进入。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | Candidate 删除必要条件并说“一定” |
| version_claim_status | NOT_PRESENT | 条件内容不是版本 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 单独明确完整条件 |
| evidence_selection | E1 | 实际只用 E1 |
| phase2_issue | NONE | 正常的条件事实错误 |
| possible_accidental_secondary_error | NO | 缺条件是单一核心错误 |
| evidence_sufficiency | SUFFICIENT | E1 覆盖必要条件 |

`phase2_reason`：“E1 要求提前申请和有效研究证两项并存，Candidate 删除第二项并断言一定准入；单份 E1 足以确认条件冲突。”
最容易误判：把实体条件错误记为 version `PRESENT_INCORRECT`。

### 案例 09：公布机关错误

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《雪岭预约办法》由甲委员会公布。”
虚构 E1：正文明确乙委员会公布，甲网站只是官方转载。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 核心机关绑定被否定 |
| version_claim_status | NOT_PRESENT | 无版本事件/状态 |
| authority_claim_status | PRESENT_INCORRECT | 甲公布角色错误 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 单份可区分乙与甲 |
| evidence_selection | E1 | 实际用 E1 |
| phase2_issue | NONE | Candidate 错不是来源问题 |
| possible_accidental_secondary_error | NO | 只有机关错误 |
| evidence_sufficiency | SUFFICIENT | 正文角色明确 |

`phase2_reason`：“E1 正文署名乙委员会公布，甲仅转载；Candidate 把 host/repost 绑定为公布机关，E1 单独足以否定。”
最容易误判：把 Candidate-vs-Evidence 差异填成 `SOURCE_CONFLICT`。

### 案例 10：生效转换日期错误

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《松涛通行规则》修订条款自2031年6月1日起施行。”
虚构 E1：修改决定明确2031年7月1日起施行。E2：数据库同样记录7月1日。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 生效日期被明确否定 |
| version_claim_status | PRESENT_INCORRECT | 这是修订条款的生效转换 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 或 E2 单份均足够 |
| evidence_selection | E1+E2 | 实际核读两份 |
| phase2_issue | NONE | 来源一致，无材料缺陷 |
| possible_accidental_secondary_error | NO | 日期是唯一错误 |
| evidence_sufficiency | SUFFICIENT | 日期与身份明确 |

`phase2_reason`：“Candidate 将修订条款生效日写为6月1日，E1/E2均为7月1日；该日期是版本转换，E1单份已足够确认冲突。”
最容易误判：把修订生效日期当作普通实体日期而 version NOT_PRESENT。

### 案例 11：必须联合两个时期才能判断变化方向

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“青禾馆从2030年到2032年将每日名额从五十人下调到六十人。”
虚构 E1：仅证明2030年为五十人。E2：仅证明2032年为六十人。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 五十到六十是上调，不是下调 |
| version_claim_status | NOT_PRESENT | 比较的是业务数值，不是文档版次 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | MULTI_EVIDENCE_OR_VERSION_CHAIN | 任一单份都不能决定变化方向 |
| evidence_selection | E1+E2 | 实际联读两份 |
| phase2_issue | NONE | 证据链完整 |
| possible_accidental_secondary_error | NO | 方向错误是唯一核心错误 |
| evidence_sufficiency | SUFFICIENT | 联合后足够 |

`phase2_reason`：“E1 只给2030年五十人，E2 只给2032年六十人；必须联读才能确认实际上调而非下调，故 minimum=MULTI。”
最容易误判：因为有两个年份而把 version 判 PRESENT。

### 案例 12：必须联合前任/后继关系

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《晨港旧规》取代了《晨港新规》，并继续有效。”
虚构 E1：只证明《晨港旧规》曾经有效。E2：只证明《晨港新规》后来取代旧规并现行有效。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | successor 方向和当前状态均被联合链否定 |
| version_claim_status | PRESENT_INCORRECT | 明示取代关系与 current state |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | MULTI_EVIDENCE_OR_VERSION_CHAIN | E1/E2 各自不足以完整确认关系 |
| evidence_selection | E1+E2 | 实际联读 |
| phase2_issue | NONE | 版本链本身完整 |
| possible_accidental_secondary_error | NO | 状态是错误关系的直接后果 |
| evidence_sufficiency | SUFFICIENT | 联合证据足够 |

`phase2_reason`：“E1 只能证明旧规曾有效，E2 证明新规后来取代旧规；联读才可否定 Candidate 反向取代及继续有效的版本绑定。”
最容易误判：把错误关系与其直接状态后果算成两个 secondary errors。

### 案例 13：修订主张存在，但沿革缺失

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《紫杉阅览规则》在2030年完成第三次修订。”
虚构 E1：只给现行实体条文。E2：只给文件标题，没有修订次数或年份。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | INSUFFICIENT_EVIDENCE | 无法判断修订年和次数 |
| version_claim_status | PRESENT_EVIDENCE_INSUFFICIENT | Candidate 明示修订事件，但证据不足 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 未确认事实冲突 |
| evidence_selection | E1+E2 | 两份均核读 |
| phase2_issue | EVIDENCE_MISSING | 所需沿革没有提供 |
| possible_accidental_secondary_error | NO | 只有一个复合版本主张 |
| evidence_sufficiency | INSUFFICIENT | 无法完成核心判断 |

`phase2_reason`：“Candidate 明示2030年第三次修订，但E1/E2都没有沿革、次数或年份，不能将缺记录当反证；总体和版本均记不足。”
最容易误判：凭“没有看到”填 `PRESENT_INCORRECT`。

### 案例 14：冻结来源真正互相冲突

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《溪月寄存规则》规定需提交两份材料。”
虚构 E1：同版同条同条件记两份。E2：同版同条同条件记三份；没有更正、版本或范围说明。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | INSUFFICIENT_EVIDENCE | 无法可靠选择哪份为准 |
| version_claim_status | NOT_PRESENT | Candidate 只说实体数量 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 未可靠确认 Candidate 冲突 |
| evidence_selection | E1+E2 | 两份都实际使用 |
| phase2_issue | SOURCE_CONFLICT | E1/E2 自身不可调和 |
| possible_accidental_secondary_error | NO | 无第二 Candidate 原子 |
| evidence_sufficiency | INSUFFICIENT | 来源冲突阻碍判断 |

`phase2_reason`：“E1/E2 对同版同条同条件分别记二份和三份，冻结材料没有时间、范围或更正关系可调和，因此不能武断判 Candidate。”
最容易误判：挑自己更相信的一份并把 Candidate 判对/错。

### 案例 15：年份只限定事实，不构成 version

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“2033年，南星观景台每日开放八小时。”
虚构 E1：2033年运行公告明确八小时。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | LEGITIMATE_VERSION_OR_HISTORY | 事实受明确历史时期支持 |
| version_claim_status | NOT_PRESENT | 没有某年版、修订或状态主张 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非冲突 |
| evidence_selection | E1 | 实际用 E1 |
| phase2_issue | NONE | 无材料问题 |
| possible_accidental_secondary_error | NO | 单一正确事实 |
| evidence_sufficiency | SUFFICIENT | 时间与时长明确 |

`phase2_reason`：“E1 支持2033年每天八小时；年份限定运行事实而非文档身份，因此 overall 为合法历史而 version=NOT_PRESENT。”
最容易误判：看到“2033年”就选 `PRESENT_CORRECT`。

### 案例 16：无年份的明确修订仍是 version claim

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《青松导览规程》已经修订，将预约入口调整为东门。”
虚构 E1：正式修订文本确认调整为东门。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 修订事件和内容受支持 |
| version_claim_status | PRESENT_CORRECT | “已经修订”明确版本事件 |
| authority_claim_status | NOT_PRESENT | 未说谁修订 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非冲突 |
| evidence_selection | E1 | 实际用 E1 |
| phase2_issue | NONE | 无材料缺陷 |
| possible_accidental_secondary_error | NO | 事件与内容均正确 |
| evidence_sufficiency | SUFFICIENT | E1 覆盖两项 |

`phase2_reason`：“Candidate 明示文档已经修订，E1 也支持修订及东门调整；是否写年份不影响 version presence。”
最容易误判：认为没有年份就一定 `NOT_PRESENT`。

### 案例 17：把旧版说成现行版

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“现行《蓝湾排队规则》规定每组最多四人。”
虚构 E1：旧版为四人。E2：明确新版已取代旧版，现行上限为六人。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 旧值被错误绑定到现行状态 |
| version_claim_status | PRESENT_INCORRECT | “现行”明确文档状态且被否定 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | MULTI_EVIDENCE_OR_VERSION_CHAIN | 需旧版值与取代/现行链联合确认 |
| evidence_selection | E1+E2 | 实际联读 |
| phase2_issue | NONE | 版本链完整 |
| possible_accidental_secondary_error | NO | 实体值与状态误绑定是同一核心问题 |
| evidence_sufficiency | SUFFICIENT | 旧/新关系清楚 |

`phase2_reason`：“E1 证明四人仅属旧版，E2 证明新版已取代并为六人；Candidate 将旧值绑定为现行，需联合版本链确认。”
最容易误判：因为四人曾经正确，就把整体判合法历史；Candidate 明确说了“现行”。

### 案例 18：“目前数值”不自动是文档版本

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“目前，绿洲展馆普通票价为八元。”
虚构 E1：当前票价公告为八元。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 当前实体数值受支持 |
| version_claim_status | NOT_PRESENT | “目前”修饰票价，不是文档状态 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非冲突 |
| evidence_selection | E1 | 实际用 E1 |
| phase2_issue | NONE | 无行级问题 |
| possible_accidental_secondary_error | NO | 单一正确事实 |
| evidence_sufficiency | SUFFICIENT | E1 足够 |

`phase2_reason`：“E1 支持当前票价八元；‘目前’限定实体票价，没有指称某文档现行版，version=NOT_PRESENT。”
最容易误判：把任何“目前/当前”都视为 version state。

### 案例 19：修改决定标题自身构成 version claim

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《关于修改〈云谷参观规程〉的决定》由甲委员会会议通过。”
虚构 E1：确认同名修改决定及甲委员会通过。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 修改决定与通过事实均支持 |
| version_claim_status | PRESENT_CORRECT | 标题明确 amendment identity |
| authority_claim_status | PRESENT_CORRECT | 明示且支持通过机关 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非冲突 |
| evidence_selection | E1 | 实际用 E1 |
| phase2_issue | NONE | 无缺陷 |
| possible_accidental_secondary_error | NO | 两个原子均正确 |
| evidence_sufficiency | SUFFICIENT | E1 覆盖版本和机关 |

`phase2_reason`：“E1 支持修改决定身份及甲委员会通过；标题本身包含修改语义，因此 version present，机关角色也独立正确。”
最容易误判：因句中只有“会议通过”就忽略标题的 modification identity。

### 案例 20：Version 正确，实体内容错误

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《银沙使用规则》2031年修订版把上限调整为九人。”
虚构 E1：确认2031年修订版身份，但该版上限为七人。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 九人与七人冲突 |
| version_claim_status | PRESENT_CORRECT | 2031修订版身份正确 |
| authority_claim_status | NOT_PRESENT | 无机关主张 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 单独足够 |
| evidence_selection | E1 | 实际用 E1 |
| phase2_issue | NONE | 正常实体错误 |
| possible_accidental_secondary_error | NO | 版次正确，只有数值错 |
| evidence_sufficiency | SUFFICIENT | E1 同时覆盖版次与数值 |

`phase2_reason`：“E1 支持2031修订版身份，却明确上限七人；总体数值冲突但版本主张正确，E1单份足够。”
最容易误判：总体错就把 version 一并填 `PRESENT_INCORRECT`。

### 案例 21：修订事件正确，修订机关错误

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《飞泉展陈规程》确已修订，由甲委员会完成修订。”
虚构 E1：确认规程修订。E2：明确修订机关为乙委员会。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 修订机关主张错误 |
| version_claim_status | PRESENT_CORRECT | 修订事件本身正确 |
| authority_claim_status | PRESENT_INCORRECT | 甲不是修订机关 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E2 单独足以否定甲机关 |
| evidence_selection | E1+E2 | 两份均实际使用 |
| phase2_issue | NONE | 正常机关事实冲突 |
| possible_accidental_secondary_error | NO | 修订事件正确，只有机关错 |
| evidence_sufficiency | SUFFICIENT | 事件和机关均可判 |

`phase2_reason`：“E1支持修订事件，E2明确乙委员会修订；Candidate 的版本事件正确、机关绑定错误，E2单独足以确认总体冲突。”
最容易误判：authority 错就把 version 一并判错。

### 案例 22：普通执行者不是 Authority

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《星河预约规则》规定，服务窗口收到申请后发放号码。”
虚构 E1：同条明确窗口执行该流程。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 业务流程受支持 |
| version_claim_status | NOT_PRESENT | 无文档级版本语义 |
| authority_claim_status | NOT_PRESENT | 窗口是业务执行者 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非冲突 |
| evidence_selection | E1 | 实际用 E1 |
| phase2_issue | NONE | 无问题 |
| possible_accidental_secondary_error | NO | 无错误 |
| evidence_sufficiency | SUFFICIENT | 条文足够 |

`phase2_reason`：“E1 支持窗口发放号码；窗口只承担业务操作，Candidate 未声称其制定、公布或主管文档。”
最容易误判：看到机构名就选择 authority `PRESENT_CORRECT`。

### 案例 23：Authority present，但 Version 不存在

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《晨露开放办法》由甲委员会公布，每日开放六小时。”
虚构 E1：正文署名甲委员会公布并载六小时。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 机关与时长均支持 |
| version_claim_status | NOT_PRESENT | 公布事实本身不含版本语义 |
| authority_claim_status | PRESENT_CORRECT | 明确公布机关且正确 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非冲突 |
| evidence_selection | E1 | 实际用 E1 |
| phase2_issue | NONE | 无问题 |
| possible_accidental_secondary_error | NO | 无错误 |
| evidence_sufficiency | SUFFICIENT | E1 足够 |

`phase2_reason`：“E1支持甲委员会公布及六小时；普通公布行为属于机关角色，不自动构成修订或版次主张。”
最容易误判：让 authority present 机械带动 version present。

### 案例 24：Version present，但 Authority 不存在

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《远帆借阅规则》旧版已被新版替代。”
虚构 E1：旧版身份记录。E2：新版明确替代旧版。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 替代关系受支持 |
| version_claim_status | PRESENT_CORRECT | 明示前后版本关系 |
| authority_claim_status | NOT_PRESENT | 没有谁实施替代的机关主张 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非冲突 |
| evidence_selection | E1+E2 | 实际联读版本链 |
| phase2_issue | NONE | 无问题 |
| possible_accidental_secondary_error | NO | 关系正确 |
| evidence_sufficiency | SUFFICIENT | 两版关系明确 |

`phase2_reason`：“E1/E2共同支持旧版被新版替代；Candidate 没有声称制定、公布或修订机关，authority=NOT_PRESENT。”
最容易误判：有 version 就认为 authority 必须 present。

### 案例 25：Host / Repost 与 Issuer 分离

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《海雾展馆细则》由甲局制定。”
虚构 E1：甲局官网转载正文；正文明确乙委员会制定，甲局为转载单位。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 制定机关被否定 |
| version_claim_status | NOT_PRESENT | 无版本主张 |
| authority_claim_status | PRESENT_INCORRECT | 甲只是 host/repost |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 同页已区分角色 |
| evidence_selection | E1 | 实际核读 E1 正文 |
| phase2_issue | NONE | 来源本身不冲突 |
| possible_accidental_secondary_error | NO | 仅机关绑定错误 |
| evidence_sufficiency | SUFFICIENT | 角色说明完整 |

`phase2_reason`：“E1虽托管在甲局官网，但正文明确乙委员会制定、甲局转载；host/repost不能证明甲是issuer。”
最容易误判：只看 URL 域名，不读正文角色。

### 案例 26：Selection 多于 Minimum

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《云栈容量规则》规定同一时段最多十二人。”
虚构 E1：明确最多十人。E2：同一现行记录也写十人；两份都实际阅读。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 十二被十否定 |
| version_claim_status | NOT_PRESENT | 容量是实体内容 |
| authority_claim_status | NOT_PRESENT | 无机关主张 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 或 E2 任一单份足够 |
| evidence_selection | E1+E2 | 本人实际读了两份 |
| phase2_issue | NONE | 来源一致 |
| possible_accidental_secondary_error | NO | 单一数值错误 |
| evidence_sufficiency | SUFFICIENT | 任一来源足够 |

`phase2_reason`：“E1和E2都将上限写为十人，Candidate十二人冲突；任一单份都可确认，故minimum=ONE而selection=E1+E2。”
最容易误判：把 minimum 写成 MULTI 以配合 selection。

### 案例 27：E2 空白但 Evidence 充分

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《岚谷票务规则》规定儿童票为四元。”
虚构 E1：同条同对象明确四元。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 核心数值受支持 |
| version_claim_status | NOT_PRESENT | 无版本语义 |
| authority_claim_status | NOT_PRESENT | 无机关角色 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非冲突 |
| evidence_selection | E1 | 只有 E1 且已使用 |
| phase2_issue | NONE | E2 非必要 |
| possible_accidental_secondary_error | NO | 无错误 |
| evidence_sufficiency | SUFFICIENT | E1 已完整覆盖 |

`phase2_reason`：“E1直接支持儿童票四元；本行无需第二证据即可完成所有判断，E2空白不是证据缺失。”
最容易误判：认为两证据槽必须填满。

### 案例 28：来源与冻结回退均不可访问

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《青帆观展办法》规定预约后两日内确认。”
虚构 E1：标题存在，但冻结摘录损坏、全文快照不可读取、官方 URL 持续不可达。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | INSUFFICIENT_EVIDENCE | 无可读依据判断两日 |
| version_claim_status | NOT_PRESENT | Candidate 没有版本主张 |
| authority_claim_status | NOT_PRESENT | 没有机关主张 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 未确认冲突 |
| evidence_selection | NONE | 没有实际可用的 E1 内容 |
| phase2_issue | SOURCE_UNREACHABLE | live 与冻结回退都不可用并阻碍判断 |
| possible_accidental_secondary_error | NO | 无第二主张 |
| evidence_sufficiency | INSUFFICIENT | 无法完成核心判断 |

`phase2_reason`：“E1摘录/快照均不可读且官方链接不可达，无法核验两日确认期；没有自行补搜，记录来源不可达与总体不足。”
最容易误判：只要 live URL 一次打不开就套用本例；必须先确认冻结回退也不可用。

### 案例 29：Phase2 才发现 Candidate 主体缺失

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“该办法要求申请人提前两日提交材料。”
虚构 E1：同时包含两份不同办法及不同提前期，无法确定 Candidate 指哪一份。E2：空。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | INSUFFICIENT_EVIDENCE | 核心文档对象无法唯一绑定 |
| version_claim_status | NOT_PRESENT | 没有文档版本事件/状态 |
| authority_claim_status | NOT_PRESENT | 没有机关角色 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 未确认事实冲突 |
| evidence_selection | E1 | 实际核读 E1 |
| phase2_issue | LATE_DISCOVERED_CANDIDATE_DEFECT | 题文“该办法”没有唯一主体 |
| possible_accidental_secondary_error | UNCERTAIN | 无法稳定分解其他原子 |
| evidence_sufficiency | INSUFFICIENT | 增加证据不能替题文补主体 |

`phase2_reason`：“Candidate 的‘该办法’无前文唯一名称，E1中又有两种制度，无法仅凭本行确定对象；登记晚发现题文缺陷，不勉强判真伪。”
最容易误判：用 Evidence 中自己更熟悉的办法替 Candidate 补主体。

### 案例 30：核心数字错，另有独立机关疑点

**虚构教学案例，不属于 Core144 数据集。**

Candidate：“《晴岛储物规则》由甲委员会公布，每人可用九个格子。”
虚构 E1：明确每人七格。E2：只显示乙官网转载，未给原公布机关，无法确认甲是否公布。

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | E1 已明确否定九格 |
| version_claim_status | NOT_PRESENT | 无版本主张 |
| authority_claim_status | PRESENT_EVIDENCE_INSUFFICIENT | 有公布机关主张，但材料只证明转载 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 单独确认核心数字冲突 |
| evidence_selection | E1+E2 | 两份均实际使用 |
| phase2_issue | EVIDENCE_MISSING | 缺少原公布机关证据 |
| possible_accidental_secondary_error | UNCERTAIN | 机关是独立原子，但无法判是否错误 |
| evidence_sufficiency | INSUFFICIENT | 核心可判，机关子字段仍不足 |

`phase2_reason`：“E1以七格否定Candidate九格，故总体冲突及minimum=ONE确定；Candidate另称甲公布，但E2仅证明乙转载，缺原公布机关依据，authority与secondary均记不足/不确定。”
最容易误判：因为一个子字段不足，就把已经由 E1 明确确认的核心冲突改成总体不足。

## 30. FAQ（25 项）

**Q1：看到年份是否一定 version PRESENT？**
不一定。年份可以只限定实体事实的时间。只有文档级修订、版次、状态、关系或转换才算。

**Q2：Evidence 写“现行有效”，为什么 Candidate 仍可能 version NOT_PRESENT？**
因为 version presence 先只看 Candidate。Evidence 元数据不能反向制造 Candidate 没说的主张。

**Q3：合法历史为什么 version 还能 NOT_PRESENT？**
overall 的历史范围比文档版本更广。某年票价、名额或状态可以是合法历史，但 Candidate 没谈文档版次。

**Q4：“目前”什么时候属于 version？**
“目前票价”通常是实体数值现状；“现行《某规则》”把状态绑定到文档，属于 version。

**Q5：两个官方机关为什么不一定 authority conflict？**
它们可分别是通过、公布、批准、修订、转载或 host。只有相同角色同一范围下不可兼容才冲突。

**Q6：我看了两份 Evidence，minimum 为什么还能 ONE？**
因为其中一份单独已经足够确认总体冲突。selection 记录实际过程，minimum 记录理论最低路径。

**Q7：E1/E2 不一致是不是一定 SOURCE_CONFLICT？**
不是。先查时期、对象、条件、版本和文档身份；可由这些差异解释时不是来源冲突。

**Q8：Candidate 错是不是 phase2_issue=OTHER？**
不是。普通事实错误通常 issue=NONE。OTHER 只用于真实的其他行级接口问题。

**Q9：URL 打不开怎么办？**
先用冻结摘录、快照和同题全文。它们足够就继续；只有所需来源和回退都不可用并阻碍判断，才 SOURCE_UNREACHABLE。

**Q10：E2 为空怎么办？**
只使用 E1。E1 足够就正常作答；不足就记录具体缺口，不自行寻找 E2。

**Q11：Evidence 不够能不能自己查？**
不能。使用不足值并写明缺什么。

**Q12：A/B 的 evidence_selection 不一样怎么办？**
各自如实记录。它是个人过程字段，差异不自动表示有人错。

**Q13：overall 错了，version 是否也必须错？**
不必须。实体内容错时 version 可以正确或不存在。

**Q14：什么叫第二个独立错误？**
与核心错误逻辑独立、可单独陈述和核验的另一个 factual atom，例如核心数字错且公布机关也错。

**Q15：Phase1 我标了 local conflict YES，Phase2 怎么处理？**
若总体确为 FACTUAL_CONFLICT，则 minimum=ZERO；仍可读 E1/E2核对子字段，selection 如实填。

**Q16：不确定时应该选什么？**
使用相应的 `INSUFFICIENT_EVIDENCE`、`PRESENT_EVIDENCE_INSUFFICIENT`、`UNCERTAIN`，并解释不确定来源；不要猜。

**Q17：能否问另一标注人？**
不能讨论具体题目或答案。操作问题可问负责人。

**Q18：能否使用 AI？**
不能。AI 提示、摘要或判断都会破坏独立人工标注。

**Q19：reason 写多长？**
通常 2–4 句，足够指出 Candidate 主张、Evidence 依据、核心结论和关键边界。

**Q20：reviewer_note 和 phase2_reason 有什么区别？**
reason 每行必填并承载主要依据；note 可空，只作补充，不能替代 reason。

**Q21：一个官方页面够不够，取决于它“官方”吗？**
不只看身份，要看内容是否覆盖同对象、范围、条件和时间下的核心命题。

**Q22：Candidate 与 E1 不同，能否直接判 FACTUAL_CONFLICT？**
先核对是否同一时间、对象、条件、版本和范围；只有不能合法调和时才冲突。

**Q23：有修订事实但没写年份，version 还算 present 吗？**
算。“修订/修改”本身就是版本事件，不要求必须出现年份。

**Q24：通过、公布、发布日期属于 version 吗？**
普通 publication facts 不自动属于 version；若日期承担施行/失效转换或修改决定身份，则可能属于。

**Q25：Phase2 发现题文问题，能否回改 Phase1？**
不能回写已提交原件。用 `LATE_DISCOVERED_CANDIDATE_DEFECT` 记录并报告负责人。

## 31. Phase2 一页速查

### 31.1 八步

读 Candidate → 读本行 E1/E2 → 判 Evidence 是否够 → 判 overall → Candidate-only 判 version → 独立判 authority → 判 minimum 并记 selection → 填 issue/secondary/sufficiency/reason。

### 31.2 八个枚举字段

| 字段 | 速查 |
|---|---|
| overall_fact_status | 支持当前语义 CURRENTLY_CONSISTENT；正确且依赖历史 LEGITIMATE_VERSION_OR_HISTORY；不可调和否定 FACTUAL_CONFLICT；材料不够 INSUFFICIENT_EVIDENCE |
| version_claim_status | 无文档级主张 NOT_PRESENT；有则 CORRECT / INCORRECT / EVIDENCE_INSUFFICIENT |
| authority_claim_status | 无制度性机关角色 NOT_PRESENT；有则 CORRECT / INCORRECT / EVIDENCE_INSUFFICIENT |
| minimum_external_evidence_needed | 非冲突 NOT_APPLICABLE；文内冲突 ZERO；单份够 ONE；各自不足联合够 MULTI |
| evidence_selection | 实际 NONE / E1 / E2 / E1+E2 |
| phase2_issue | NONE / SOURCE_UNREACHABLE / SOURCE_CONFLICT / EVIDENCE_MISSING / LATE_DISCOVERED_CANDIDATE_DEFECT / OTHER |
| possible_accidental_secondary_error | 第二独立原子 YES；没有 NO；证据不足 UNCERTAIN |
| evidence_sufficiency | 全行足够 SUFFICIENT；不够 INSUFFICIENT；难稳定判断 UNCERTAIN |

### 31.3 Version Candidate-only 四问

1. Candidate 明示修订、版次、状态、关系或转换了吗？
2. 是否只是年份、实体数值或普通通过/公布？
3. 是否把 Evidence 元数据倒灌给 Candidate？
4. 是否与实体内容、机关角色分开？

### 31.4 Authority 三问

1. 是制定/公布/通过/修订/主管，还是普通执行者？
2. 是否把 host/repost 当 issuer？
3. Evidence 是否证明了同一个具体角色？

### 31.5 ZERO / ONE / MULTI

overall 非 FACTUAL_CONFLICT → NOT_APPLICABLE。
overall 冲突且本人 Phase1 local=YES → ZERO。
E1 或 E2 单独够 → ONE。
两份各自不够、联合才够 → MULTI。
联合仍不够 → overall INSUFFICIENT_EVIDENCE + minimum NOT_APPLICABLE。

### 31.6 Minimum 与 Selection

Minimum 问“最少需要多少”；Selection 问“我实际用了什么”。ZERO+E1、ZERO+E1+E2、ONE+E1+E2、MULTI+E1+E2 都可能合法。实际看两份不等于 MULTI。

### 31.7 Top 10 禁止误判

1. 年份不自动 version。
2. Evidence 元数据不倒灌 Candidate。
3. 历史不等于错误，也不自动是文档版本。
4. 普通 actor 不自动 authority。
5. host/repost 不等于 issuer。
6. overall/version/authority 不联动。
7. minimum 不等于 selection。
8. Candidate 错不自动 phase2_issue。
9. URL 失败不自动 SOURCE_UNREACHABLE。
10. E2 空不自动 EVIDENCE_MISSING。

### 31.8 强制组合复核

| 条件 | 必须满足 |
|---|---|
| overall 非冲突 | minimum=NOT_APPLICABLE |
| overall 冲突 + Phase1 local=YES | minimum=ZERO |
| overall 合法历史 | version 可 NOT_PRESENT |
| selection=E1+E2 | minimum 不必 MULTI |
| 普通事实冲突 | issue 可 NONE |
| Evidence 不足 | 不猜 FACTUAL_CONFLICT |
| version presence | 先只看 Candidate |
| host/repost | 不自动 authority |
| secondary=YES | 指出第二独立原子 |
| reason | 每行具体引用 Candidate 与 E1/E2 |

## 32. 提交前 Checklist

- [ ] 我只用了本行提供的 frozen Evidence。
- [ ] 我没有自己搜索网页或法规库。
- [ ] 我没有使用任何 AI。
- [ ] 我先判断了 overall，再判断子字段。
- [ ] version presence 是先只看 Candidate 判断的。
- [ ] 我把 authority 与普通业务 actor 分开。
- [ ] 我把 minimum 与 selection 分开。
- [ ] 我没有把普通 FACTUAL_CONFLICT 误写成 issue。
- [ ] secondary error 确实是独立第二 factual atom。
- [ ] evidence_sufficiency 不是按网页数量或能否打开判断。
- [ ] 每行 phase2_reason 都有具体 Evidence 依据。
- [ ] 我没有猜 C/P/H、HKP、S 或设计意图。
- [ ] 我没有查看或讨论另一位标注员答案。
- [ ] 我没有增删行、列、工作表，也没有修改 ID、Candidate 或 Evidence。
- [ ] 八个枚举都使用 Excel 下拉中的英文原值。
- [ ] 文件仍为 .xlsx，并按负责人指定的 RETURN 文件名保存。

## 33. 独立性、保存与交回

HUMAN-A01 和 HUMAN-B01 各自使用自己的 Phase2 工作簿和同一份本手册。不得交换工作簿、ID、答案或讨论具体题目。填写时可使用 Excel、WPS 或 LibreOffice，但不要排序整表、增删内容或更改格式结构。

完成后按负责人指定文件名保存并直接交回原始保存件。Owner 收到后会先按原字节锁定；因此提交后不要再由中间人打开重存、另存为 CSV 或做复制粘贴规范化。

正式发放只包含：

- HUMAN-A01：`PAPER1_CORE144_D1_HUMAN_A01_PHASE2_V1.xlsx` + 本手册；
- HUMAN-B01：`PAPER1_CORE144_D1_HUMAN_B01_PHASE2_V1.xlsx` + 本手册。

不得发放 R3/R4 答案、内部映射、Expected、GT、Owner overlay、C/P/H、HKP 或 S。旧 PDF 不作为当前 Phase2 权威说明。

## 34. 规则版本与边界声明

本手册将 Formal Guide V4 的八字段合同、V4.1 的 version/authority/row-level issue 范围、V4.2 的 Candidate-only version scope 与 amendment-decision identity、V4.3 的 temporal/historical 与 document-version 分离，整合为真人可直接执行的说明。

本手册使用当前 Core144 Human Phase2 工作簿的实际 20 列与 K–R 下拉枚举。它不引入新字段、新 enum、新答案或新 Evidence，不修改任何 A/B 工作簿。若工作簿内简短提示与本手册在措辞详略上不同，以当前冻结 V4–V4.3 的上述操作性边界理解；如遇真正无法调和的合同冲突，应停止该行并向 Owner 报告，不自行改 Excel。

所有案例均为虚构教学案例，不属于 Core144 数据集。它们只演示判断方法，不能当作真实题目的答案表。
