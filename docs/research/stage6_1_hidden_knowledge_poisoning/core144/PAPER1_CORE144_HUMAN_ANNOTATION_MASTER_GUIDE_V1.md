# Core144 真人标注主手册 V1

适用对象：HUMAN-A01、HUMAN-B01。适用文件：各自的 Core144 D1 Human Phase1 / Phase2 V1 工作簿。说明用中文；答案中的枚举值必须使用工作簿给出的英文原值。本文是填写说明，不含实际题目答案，也不代表材料已经发放。

> **第一次填写前，请先读第 2–5 节、第 13–17 节、第 22 节和第 29 节速查表。只在 Excel 的【标注表】答案列作答，不在本手册中作答。Phase1 不看证据、不查网页。Phase2 未由负责人单独发给你之前，不要索取或打开。**

## 1. 这份手册是干什么的

你的任务是独立阅读每条 `candidate_text`（候选文本），按固定问题记录判断。第一阶段评价文本表达与文本自身的问题；第二阶段在给定证据范围内判断事实及证据情况。你不需要了解项目历史、算法或数据构造过程，也不负责判断一条文本属于什么实验类别。不要根据题号、题序、措辞模式或相邻题目推测答案。

下文的图书馆、展馆、园区和各项“样例规程”全部虚构。教学证据只在对应案例中假定成立，不是真实法律、政策或你的正式作答依据。案例帮助理解字段边界，不能用来套真实题目。

完整目录：1 用途；2 总原则；3 两阶段流程；4 Excel 操作；5 Phase1 顺序；6 Phase1 字典；7 Phase1 字段；8 Phase1 易错点；9 Phase1 案例；10 Phase1 自检；11 Phase2 开始条件；12 证据使用；13 Phase2 字典；14 总体事实；15 Phase2 顺序；16 版本；17 机关；18 历史与时间；19 最低证据；20 实际证据；21 第二阶段问题；22 次生错误；23 证据充分性；24 理由写法；25 跨字段一致性；26 高危歧义表；27 Phase2 案例；28 FAQ；29 速查表；30 最终检查；31 规则版本。

## 2. 标注总原则

一条题目一次完整判断。先读完再填字段，不要先把某一整列批量填成同一个值。相邻题目可能很相似，但每行仍是独立判断对象。

两位标注员必须独立：不讨论个别题目、不互看工作簿、不复制答案、不借用对方理由。不确定时，按字段允许的不足或不确定值记录具体原因；不能向另一位标注员问“你填什么”。文件损坏、下拉框失效等操作问题可以向负责人报告，不要求负责人先给事实答案。

不得让 ChatGPT、豆包、Claude、DeepSeek 或其他 AI 辅助判断、代写理由、批量填表。Phase1 不得搜索事实；Phase2 不得到网上另找证据。你的记忆不是给定证据。文本是否自然、文本内部是否矛盾、现实事实是否受证据支持，是三个不同问题。

只填写实际存在的字段。没有主张时用对应的 `NOT_PRESENT`，不是自己创建中文值、“不知道”或额外列。没有信息与信息错误必须分开；证据不足与事实已被否定也必须分开。

## 3. 整个两阶段流程

流程固定为：收到自己的 Phase1 → 独立作答 → 原件提交负责人 → 负责人保存原始字节并校验 → 负责人单独放行自己的 Phase2 → 仅用给定证据作答 → 提交自己的 Phase2 原件。

A 完成并不自动放行 B 的 Phase2。不能提前把 Phase2 打开“只看看目录”。Phase1 的正式返回一旦交回，不因后来看到证据而重写。若第二阶段才发现候选缺陷，在第二阶段如实登记，保留第一阶段原答，由负责人处理后续复核。

手册解释两个阶段的规则，但不提供正式题目的第二阶段证据。读懂第二阶段规则不等于已获第二阶段发放许可。

## 4. Excel 里在哪里填，怎样保存

Phase1 有七张说明/工作表：【开始前必读】、【标注表】、【字段说明】、【高危歧义与易错点】、【判断流程】、【虚构示例】、【提交前自检】。只在【标注表】C–H 列填写。A 列题号、B 列题文不改。

Phase2 有十张表：【开始前必读】、【标注表】、【字段说明】、【高危歧义与易错点】、【版本与历史判断】、【权威与机关判断】、【证据判断流程】、【虚构示例】、【冻结证据全文】、【提交前自检】。A–J 是题目和给定证据，只读；K–R 为八个枚举字段，S 为每行必填理由，T 为可选附注。

建议保留原题序逐行填写。工作簿允许筛选或整行排序，但必须确保整行的题号、文本、证据与答案一起移动；绝不能只排某一答案列。不要增删行列、改标题、改 ID、改题文、改证据、合并题目或把说明写进枚举格。当前 D1 每人每阶段 144 行。不能用另一个人的文件替换自己的文件。

保存为 `.xlsx`，不转换 CSV，不用中文替换英文下拉值。提交名称分别为：

- A Phase1：`PAPER1_CORE144_D1_HUMAN_A01_PHASE1_RETURN_V1.xlsx`
- B Phase1：`PAPER1_CORE144_D1_HUMAN_B01_PHASE1_RETURN_V1.xlsx`
- A Phase2：`PAPER1_CORE144_D1_HUMAN_A01_PHASE2_RETURN_V1.xlsx`
- B Phase2：`PAPER1_CORE144_D1_HUMAN_B01_PHASE2_RETURN_V1.xlsx`

完成后交给负责人原文件。负责人应直接保存收到的原件，不再用 Excel 重存；你也不要提交后再覆盖同名原件。确需更正先联系负责人，不能静默换文件。

## 5. Phase1 固定判断顺序

1. 只读本行完整 `candidate_text`，不查资料。
2. 判断中文表达：`text_naturalness`。
3. 判断文本自身两个命题能否同时为真：`local_internal_conflict`。
4. 判断能否独立辨认对象、核心命题和必要条件：`self_containment`。
5. 判断关键指代能否唯一恢复：`ambiguous_referent`。
6. 判断是否有实验元话语或明显机械拼接：`meta_or_template_language`。
7. 任一非正常值，写具体 `issue_note`；然后完成下一行。

不要把“我知道官方规定不是这样”当作第 3 步的依据。只有候选内部可见的不相容命题才属于内部冲突。

## 6. Phase1 完整字段字典

以下八列就是当前工作簿的实际列。前两列是预填只读内容，后六列由你填写。“必填”指每行的填写义务，不代表你需要把只读文字再输入一遍。

| 英文名 / 中文名 | 阶段与必填 | 允许值 | 何时适用、判断对象 | 所需证据 | 常见错误 / 易混字段 | 一致性约束 |
|---|---|---|---|---|---|---|
| `blind_id` / 不透明题号 | P1，预填必有 | 原题号文本 | 每行身份 | 不需证据 | 重编号、与他人题号对齐 | 原值不改；答案跟本行 |
| `candidate_text` / 候选文本 | P1，预填必有 | 原题文 | 五项判断的唯一文本对象 | 仅本行文字 | 修正错字后再判断、借上下行解释 | 不改题文 |
| `text_naturalness` / 文本自然度 | P1，每行必填 | NATURAL / MINOR_ISSUE / UNNATURAL | 表达质量 | 候选自身 | 用事实错误替代语言判断 / conflict | 非 NATURAL 必有 note |
| `local_internal_conflict` / 文本内部冲突 | P1，每行必填 | YES / NO / UNCERTAIN | 同范围不相容命题 | 候选自身，不用常识查证 | 外部错填 YES / naturalness | 非 NO 必有 note |
| `self_containment` / 自包含性 | P1，每行必填 | PASS / FLAG / UNCERTAIN | 核心对象和命题能否独立恢复 | 候选自身 | 少背景就 FLAG / referent | 非 PASS 必有 note |
| `ambiguous_referent` / 指代歧义 | P1，每行必填 | YES / NO / UNCERTAIN | 关键指代是否多解 | 候选自身 | 裸缺对象直接当多解 / self_containment | 非 NO 必有 note |
| `meta_or_template_language` / 模板或实验语言 | P1，每行必填 | YES / NO / UNCERTAIN | 元话语、明显机械结构 | 候选自身 | 正式语言当模板 / naturalness | 非 NO 必有 note |
| `issue_note` / 问题说明 | P1，条件必填 | 中文自由文本；全正常可空 | 解释本行非正常判断 | 引用本行文字 | “感觉不对”、引用网站 / phase2_reason | 五项任一非默认就必填 |

## 7. Phase1 各字段怎么选

### 7.1 `text_naturalness`（文本自然度）

`NATURAL`（自然）：语法正常、表达清楚，普通中文读者能直接理解。正式术语、法规条号、较长句子并不自动不自然。句子自然地表达错误事实或互相矛盾的事实，仍可选 NATURAL。不能因为“结论错”而降低自然度。

`MINOR_ISSUE`（轻微表达问题）：局部冗余、生硬或语序略别扭，核心意思仍清楚，不必猜作者意图。不能仅凭“不喜欢这种文风”或“我怀疑数字错误”使用。

`UNNATURAL`（明显不自然）：明显病句、语法断裂、严重搭配错误或机械拼接显著妨碍阅读。不能把逻辑矛盾本身等同病句；要指出表达层面的具体障碍。

边界：稍加顺口改写即可、原句核心清楚，通常 MINOR_ISSUE；必须补词、重组甚至猜测主谓关系才能理解，才考虑 UNNATURAL。自然度不替代缺上下文或指代字段。

### 7.2 `local_internal_conflict`（文本内部冲突）

`YES`（有）：至少两个文本内可见核心命题，在同一主体、范围、条件和时间语境下不能同时成立。例如同一张卡在同一时刻被说成既有效又无效。必须找出两端，不凭记忆判断。

`NO`（没有）：没有这种文内不相容关系。只有一个金额、一个日期，即使你怀疑现实中写错，仍为 NO。不同时间标准、不同对象待遇、制定与转载两种机关角色可以同时成立，不能自动判 YES。

`UNCERTAIN`（文本导致无法确定）：主体、范围、时间、条件或指代模糊，不能确认两句到底是不是在说同一件事。不是“我不知道法律真实内容”。能明确不存在文内冲突就用 NO，不能为了谨慎把所有未知事实都填 UNCERTAIN。

同一文件、同一次公布行为被明确说成“仅由甲机关公布”与“仅由乙机关公布”，范围互斥时为 YES。甲制定、乙转载，或明确甲乙联合公布，不是仅因有两个机关就冲突。

### 7.3 `self_containment`（自包含性）

`PASS`（可独立理解）：本行提供足够信息辨认对象和主要命题；不需要所有背景知识。`FLAG`（缺失关键信息）：没有交代必要对象、文件或条件，必须依赖缺失上下文。`UNCERTAIN`（无法稳定判断）：仅凭文字难以确定缺少的信息是否影响核心理解。

裸写“该办法”“上述规定”“该版本”而没有唯一前件，通常 FLAG。但“栖霞展馆周末开放”没有交代建馆史，并不妨碍理解开放命题，不能 FLAG。

### 7.4 `ambiguous_referent`（指代歧义）

`YES`：关键“其”“该日”“该文件”等有两个或更多合理前件。`NO`：没有指代，或只有唯一合理前件。`UNCERTAIN`：文本本身不能支持稳定的唯一/多解判断。

“关键对象根本没写”与“写了两个对象却不知道指哪个”不同。前者通常 self_containment=FLAG；没有两个现成前件，不自动把 ambiguous_referent 也填 YES。两个字段可以各有问题，但不是强制一同变值。当前工作簿的虚构例子允许对象已列清的 self_containment=PASS 与指代 YES 并存。

### 7.5 `meta_or_template_language`（模板或实验语言）

`YES`：出现“本样本”“候选文本”“正确答案”“为了测试”“核验结果”等明显实验话语，或显著的槽位残留、机械拼装。`NO`：没有这些迹象；普通“根据某规程规定”不是元话语，相似的正式句式也不自动为模板。`UNCERTAIN`：有可见疑点但无法稳定断定，写出疑点。

有模板迹象不意味着自然度必然 UNNATURAL；例如“本样本的正确答案是甲规程”语法流畅，可 NATURAL + meta YES。

### 7.6 `issue_note`（问题说明）

明确布尔规则：`text_naturalness != NATURAL` **或** `local_internal_conflict != NO` **或** `self_containment != PASS` **或** `ambiguous_referent != NO` **或** `meta_or_template_language != NO`，任一成立，note 必填。五项正好为 NATURAL / NO / PASS / NO / NO 时，留空即可。

用一两句中文指出可见文字及原因。例如“‘该日’可指前文两次登记日，不能唯一恢复。”不要只写“有问题”。不要写“网上正确日期是……”或猜测文本类别。多个非默认字段都要有可理解的解释，可以合写在同一格。

## 8. Phase1 高危歧义和典型错误

最常见的串线是把表达质量、逻辑关系与外部真伪合成一件事。请反问自己：“我指出的问题在这行字里能找到吗？”若必须查资料才能知道错在哪里，就不能作为内部冲突理由。

不要看到正式语言就判模板；不要看到两个机关就判冲突；不要只因为缺乏更多背景就判不自包含；不要因为不知道事实就选 UNCERTAIN。也不要把所有不满意都集中填某一个字段。每个非默认值要能够对应一个具体、可见的文本问题。

## 9. Phase1 虚构完整填写案例（案例 01–09）

本节每例只演示第一阶段。**虚构 Evidence：本阶段不提供、不使用。** 第四栏是理由解释，不是 Excel 新增列。案例中 note 内容供学习，不能复制到真实行。

### 案例 01：自然、清楚，没有内部冲突

Candidate：“云岚市图书馆每周三开放阅览室。”

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| text_naturalness | NATURAL | 中文顺畅，不评价开放事实真假 |
| local_internal_conflict | NO | 只有一项开放安排，没有互斥断言 |
| self_containment | PASS | 图书馆、阅览室和时间明确 |
| ambiguous_referent | NO | 没有多解指代 |
| meta_or_template_language | NO | 普通知识陈述，无实验话语 |
| issue_note | 留空 | 五项均正常 |

易错点：不知道真实开放日，不是 UNCERTAIN 的理由。

### 案例 02：自然表达的自相矛盾

Candidate：“同一张云岚展馆月票在星期一上午既有效，又无效。”

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| text_naturalness | NATURAL | 句法清楚，矛盾不等于病句 |
| local_internal_conflict | YES | 同票、同一上午的有效性互斥 |
| self_containment | PASS | 对象和时间足够明确 |
| ambiguous_referent | NO | 同一张票，无多解 |
| meta_or_template_language | NO | 没有模板或实验提示 |
| issue_note | 同一月票在同一上午被同时说成有效和无效。 | 解释冲突 YES，所以必填 |

易错点：不能只因内容矛盾填 UNNATURAL。

### 案例 03：轻微冗余

Candidate：“云岚市图书馆在周三进行开放阅览室的开放。”

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| text_naturalness | MINOR_ISSUE | “进行…的开放”重复生硬，意思仍明确 |
| local_internal_conflict | NO | 没有相反安排 |
| self_containment | PASS | 主要对象和开放安排可理解 |
| ambiguous_referent | NO | 没有指代竞争 |
| meta_or_template_language | NO | 局部冗余本身不足以证明机械模板 |
| issue_note | “进行开放阅览室的开放”累赘，核心仍是周三开放。 | 自然度非默认，必须解释 |

易错点：轻微表达问题不自动成为事实问题。

### 案例 04：语法断裂

Candidate：“云岚展馆申请参观的因为开放提交可以三份。”

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| text_naturalness | UNNATURAL | 主谓关系断裂，不能自然恢复句意 |
| local_internal_conflict | NO | 没有形成两个可辨认互斥命题 |
| self_containment | FLAG | 虽有展馆名，核心申请要求不能恢复 |
| ambiguous_referent | NO | 不是多个先行词的指代问题 |
| meta_or_template_language | NO | 病句本身不证明模板来源 |
| issue_note | 句子主谓关系断裂，无法确认“三份”指什么申请材料。 | 解释两个异常字段 |

易错点：无法理解不等于已证实逻辑矛盾。

### 案例 05：根本未交代对象

Candidate：“该办法要求预约人提前两日登记。”

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| text_naturalness | NATURAL | 句法正常 |
| local_internal_conflict | NO | 没有第二个相反命题 |
| self_containment | FLAG | “该办法”没有前件，具体制度未知 |
| ambiguous_referent | NO | 不是两个已出现办法之间的选择 |
| meta_or_template_language | NO | 没有实验话语 |
| issue_note | “该办法”未交代具体文件，无法独立识别登记要求的对象。 | 自包含性 FLAG 必填 |

易错点：对象缺失与多个对象指代歧义分开。

### 案例 06：对象都有，但指代多解

Candidate：“栖霞园区的甲通知和乙通知同日公布，该文件次日开放申请。”

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| text_naturalness | NATURAL | 表达正常 |
| local_internal_conflict | NO | 没有可见互斥安排 |
| self_containment | PASS | 园区和两个通知对象已给出 |
| ambiguous_referent | YES | “该文件”可能指甲或乙 |
| meta_or_template_language | NO | 没有模板残留 |
| issue_note | “该文件”可指甲通知或乙通知，申请开放日所对应文件不唯一。 | 指代 YES 必填 |

易错点：不要强制所有歧义都同步改 self_containment；分别判断。

### 案例 07：自然的实验话语

Candidate：“本样本的正确答案是《青岚展馆预约办法》。”

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| text_naturalness | NATURAL | 句法通顺 |
| local_internal_conflict | NO | 无互斥断言 |
| self_containment | PASS | 所说答案对象明确 |
| ambiguous_referent | NO | 指代清楚 |
| meta_or_template_language | YES | “本样本”“正确答案”是实验元话语 |
| issue_note | 文本出现“本样本”和“正确答案”，不属于普通事实陈述。 | 元话语 YES 必填 |

易错点：meta YES 与自然度 NATURAL 可并存。

### 案例 08：怀疑外部日期错，但不是内部冲突

Candidate：“《星湾参观规则》自2032年2月1日起施行。”

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| text_naturalness | NATURAL | 日期句表达正常 |
| local_internal_conflict | NO | 只有一个施行日期，没有第二个互斥日期 |
| self_containment | PASS | 文件与事件明确 |
| ambiguous_referent | NO | 无多解指代 |
| meta_or_template_language | NO | 是普通文档事实 |
| issue_note | 留空 | 全部正常；日期真伪留到第二阶段 |

易错点：即使记得另一个日期，也不能在第一阶段用它判 YES。

### 案例 09：同次独占公布机关不相容

Candidate：“《松岛展馆规程》的这次公布仅由甲委员会完成，这次公布的唯一机关又是乙委员会。”

| 字段 | 填写 | 逐字段解释 |
|---|---|---|
| text_naturalness | NATURAL | 两句均可清楚读懂 |
| local_internal_conflict | YES | 同文件、同次公布的独占机关分别为甲乙 |
| self_containment | PASS | 文件、行为和角色均明确 |
| ambiguous_referent | NO | “这次公布”只有一个对象 |
| meta_or_template_language | NO | 未出现实验/槽位残留 |
| issue_note | 同一次公布的唯一机关分别写为甲委员会、乙委员会，不能同时成立。 | 指明互斥角色，不凭网站猜 |

易错点：如果改成甲制定、乙转载，角色不同就不能沿用 YES。

## 10. Phase1 提交前检查

- [ ] 144 行五项枚举均已填写，都是下拉框英文原值。
- [ ] 每个非默认行有具体 note；没有网页事实或 AI 理由。
- [ ] 自然度、内部冲突、自包含、指代、模板分别判断。
- [ ] 不曾看正式 Phase2、证据或另一人的答卷。
- [ ] 题号、题文、行列未增删；任何整行排序未破坏对应。
- [ ] 按自己的 Phase1 RETURN 文件名保存 `.xlsx`，交回后不重存原件。

## 11. Phase2 开始条件

只有负责人收到并保存**你自己的** Phase1 原件、通过结构校验后，才能单独发给你 Phase2。不要用 A 的进度推定 B 也可以开始。第二阶段不反向修改第一阶段；若发现晚到缺陷，按第 21 节登记。

Phase2 要回答十项：八个枚举、必填 `phase2_reason`、可选 `reviewer_note`。不要把题目列视为可修改答案。每行只有本行允许的 E1、可选 E2，没有自由选择全工作簿证据的权限。

## 12. Phase2 Evidence 使用规则

先读本行冻结摘录，再按 `blind_id` 到【冻结证据全文】查看完整冻结文本。官方 URL 是溯源/核读入口，不是另行检索授权。链接临时打不开，已有摘录或完整快照仍足够，就继续用冻结材料，不能自动 SOURCE_UNREACHABLE。

只有给定来源和提供的回退都不可访问、且确实影响本行判断，才考虑 SOURCE_UNREACHABLE。只缺修订年代或某个主体对应事实，即使网页能打开，也可能是 EVIDENCE_MISSING。可访问与足够回答是两件事。

E2 空白表示本行只提供 E1，不自动是漏页、缺证据或错误。不能自行补 E2，不能借别行 E2，也不能搜索出第三份材料替代。若 E1 已能完成本行所有判断，仍为 SUFFICIENT。若不能，就解释缺哪项依据。

网页当前内容与冻结版本不同时，仍以发给你的冻结文本范围作答，报告具体访问/身份问题，不用新内容悄悄替换。标题、域名、SHA 等只是识别信息；不能因为名字“官方”就推断所有事实正确，更不能由域名推出制定机关。

## 13. Phase2 完整字段字典

实际有二十列。前十列预填只读，后十列填写。和 Phase1 共用的 `blind_id`、`candidate_text` 仍有同样的身份/题文约束，不需你重填。

| 英文名 / 中文名 | 阶段与必填 | 允许值 | 适用对象 / 所需证据 | 常见错误及易混字段 | 一致性约束 |
|---|---|---|---|---|---|
| `blind_id` / 题号 | P2，预填必有 | 原题号 | 本行身份；不需事实证据 | 另编题号 / P1 identity | 对应自己的 P1，不改 |
| `candidate_text` / 题文 | P2，预填必有 | 原文本 | 本行主张 | 修文 / Evidence 文本 | 原值不改 |
| `E1_title` / E1 标题 | P2，预填 | 原标题 | 识别本行第一证据 | 当标题就能证明条文 / version | 不改、与 E1 同一身份 |
| `E1_excerpt` / E1 冻结摘录 | P2，预填 | 原摘录 | 本行事实依据；不足可看同题全文 | 当片段已包含所有背景 / sufficiency | 只用本行冻结范围 |
| `E1_official_url` / E1 官方链接 | P2，预填 | 原 URL | 来源溯源 | 当搜索入口、由 host 猜 issuer | 不改、不扩大范围 |
| `E1_snapshot_ref` / E1 快照标识 | P2，预填 | 原引用/校验文字 | 对应冻结材料身份 | 当事实答案或自行改 SHA | 对应本题 E1 |
| `E2_title` / E2 标题 | P2，可选预填 | 原标题或空 | 第二证据身份 | 空即认为漏页 / issue | 不可补造 E2 |
| `E2_excerpt` / E2 冻结摘录 | P2，可选预填 | 原摘录或空 | 本行第二证据 | 借用其它行证据 / selection | 仅本题 E2 |
| `E2_official_url` / E2 官方链接 | P2，可选预填 | 原 URL 或空 | 第二证据溯源 | 搜索补证 / sufficiency | 空时无 E2 可选 |
| `E2_snapshot_ref` / E2 快照标识 | P2，可选预填 | 原引用或空 | 第二证据身份 | 自造版本号 / version | 不改身份 |
| `overall_fact_status` / 总体事实 | P2，必填 | CURRENTLY_CONSISTENT / LEGITIMATE_VERSION_OR_HISTORY / FACTUAL_CONFLICT / INSUFFICIENT_EVIDENCE | 核心命题；给定证据或已锁文内冲突 | 历史即错 / version | C1、C2、C8，见第 25 节 |
| `version_claim_status` / 版本主张 | P2，必填 | NOT_PRESENT / PRESENT_CORRECT / PRESENT_INCORRECT / PRESENT_EVIDENCE_INSUFFICIENT | 候选文档级主张；存在先只看题文，正确性用证据 | 年份即版本 / overall、authority | 无主张只填 NOT_PRESENT |
| `authority_claim_status` / 机关主张 | P2，必填 | NOT_PRESENT / PRESENT_CORRECT / PRESENT_INCORRECT / PRESENT_EVIDENCE_INSUFFICIENT | 候选明示机关角色；证据证明角色 | host 当 issuer / version | 独立判断，不联动 |
| `minimum_external_evidence_needed` / 最低外部证据 | P2，必填 | ZERO_EXTERNAL_EVIDENCE_REQUIRED / ONE_OFFICIAL_EVIDENCE / MULTI_EVIDENCE_OR_VERSION_CHAIN / NOT_APPLICABLE | 确认总体冲突的最低路径；做单证据检验 | 实际看两份就 MULTI / selection | 总体非冲突必为 NOT_APPLICABLE |
| `evidence_selection` / 实际使用证据 | P2，必填 | NONE / E1 / E2 / E1+E2 | 本人实际使用过程 | 为一致性补报证据 / minimum | 本行无 E2 不填 E2 或 E1+E2 |
| `phase2_issue` / 第二阶段问题 | P2，必填 | NONE / SOURCE_UNREACHABLE / SOURCE_CONFLICT / EVIDENCE_MISSING / LATE_DISCOVERED_CANDIDATE_DEFECT / OTHER | 本行题目/证据/字段接口问题 | 事实错就 OTHER / overall | 不是会话事故字段；非 NONE 解释 |
| `possible_accidental_secondary_error` / 可能次生错误 | P2，必填 | YES / NO / UNCERTAIN | 核心问题之外独立事实原子；本行证据 | 重复计错 / overall | YES 指出另一原子，UNCERTAIN 指出缺口 |
| `evidence_sufficiency` / 证据充分性 | P2，必填 | SUFFICIENT / INSUFFICIENT / UNCERTAIN | 全行必需判断是否可完成 | 可访问即足够 / overall | 核心冲突确定但子字段不足可分开记录 |
| `phase2_reason` / 判断理由 | P2，每行必填 | 中文自由文本 | 候选、证据、字段与最低路径 | “根据资料” / reviewer_note | 每行有具体依据 |
| `reviewer_note` / 补充说明 | P2，可空 | 中文自由文本 | 额外必要说明 | 把必填 reason 移到此格 | 不替代任何必填字段 |

## 14. `overall_fact_status`（总体事实）

按以下顺序判断，不按“看起来像哪一类”判断：先问是否足够决定核心命题；然后是否有无法由合法时间/条件解释的冲突；再问真实命题是否依赖历史或版本限定；最后才归当前一致。

`INSUFFICIENT_EVIDENCE`（证据不足）：冻结材料不能可靠决定总体命题。没有提到修订不等于没有修订；缺旧版不等于旧版断言错。不允许猜一个最像答案的值。已在候选内部直接确认的冲突不需要因外部资料缺少而变成总体不足，但其他字段仍如实记缺口。

`FACTUAL_CONFLICT`（事实冲突）：核心命题被给定证据明确否定，或已由文本内不相容命题确认，且不能靠合法版本、时间、对象、条件或例外调和。候选与证据不同，先核对范围；不是所有不同都冲突。自然度可能仍为 NATURAL。

`LEGITIMATE_VERSION_OR_HISTORY`（合法版本或历史）：命题真实，成立或核心意义实质依赖明确历史时期、旧/新版、历史状态或跨时间关系。删除限定后命题不再以原意义成立。不能仅因出现年份就使用，也不能把现在还能正确说出的历史比较自动改为 CURRENTLY_CONSISTENT。

`CURRENTLY_CONSISTENT`（当前语义一致）：核心事实在它表达的语义下受冻结证据支持，不依赖上述历史限定才能成立。一个已经发生且仍成立的修订/废止事件，可能总体当前一致；它不因有修订一词就必然是合法历史。也不能仅凭“没有发现反证”认定一致，必须有支持。

## 15. Phase2 固定判断顺序

先读候选和本题允许证据，按第 14 节顺序决定 overall。暂时不想版本/机关标签，先确定核心命题和范围。再遮住证据元数据，判断候选**自己**是否提出文档级版本主张；有才用证据判对错。机关主张同样单独识别角色并查证。

随后判断最低确认冲突的证据路径，再记录你实际用了什么。最后检查本行问题、第二独立错误和全行证据充分性，写每行理由。若回查发现某一步依据不足，修正自己的尚未提交答案；不能通过编造依据填齐。

文字流程：核心可判？否 → 总体不足；是 → 存在不可调和核心冲突？是 → 冲突；否 → 成立依赖历史/版本限定？是 → 合法历史；否 → 当前一致。**版本和机关不是这棵总体树的替代答案，它们仍各自填写。**

## 16. Version：`version_claim_status` 最重要的边界

第一问永远是：“候选对**文档**说了什么？”而不是“证据网页有哪些日期”。文档级修订/修改、废止、替代、原版/修订版身份、现行/历史状态、前任/后继、版本关系、施行/失效转换、版本绑定和修改决定身份才进入版本字段。

`NOT_PRESENT`（未提出）：候选没有文档级版本主张。裸引《某规程》第几条、只说金额比例天数条件、会议通过或普通公布事实，不能自动算版本。不得因为证据页标“现行有效”就反向制造主张。

`PRESENT_CORRECT`（提出且正确）：候选确有版本主张，而且该主张受给定证据支持。数字内容错，受支持的修订事件仍可正确；机关错也不机械改变版本事件。

`PRESENT_INCORRECT`（提出且错误）：被否定的是版本命题本身，如修订年、修订次数、版本身份、施行转换、废止或替代关系。不能仅凭缺证据选此值；也不能因该版里的实体数字错误选此值。

`PRESENT_EVIDENCE_INSUFFICIENT`（提出但证据不足）：明示版本主张，冻结材料却不足以判断。不等于 NOT_PRESENT，也不等于 PRESENT_INCORRECT。

<span style="color:#b42318">**高危：年份 ≠ 版本；历史事实 ≠ 文档版本主张。**</span> “2030年展馆票价为八元”是时间背景下实体数值；“2030年版《展馆规则》”才明确指定文档版次。“目前票价为八元”通常是实体数值现状；“现行《展馆规则》”明确断言文档状态。

“某规程经修订”即使没写年份也有事件主张。“《关于修改〈某规程〉的决定》经会议通过”即使只列通过/公布细节，也因修改决定身份而有版本主张。普通“某规程经会议通过，以第几号令公布”，没有这种版本语义时版本 NOT_PRESENT；机关另判。

两份不同标题、不同年代文档的数字比较，不自动断言它们是同一文档前后版本。只有候选明确说原版—修订版、替代关系等，才是对应版本主张。标题里“调整通知”也不自动证明修订另一文档。

## 17. Authority：`authority_claim_status` 独立判断机关角色

第一问：“候选是否声称谁制定、发布、公布、通过、修订、批准，或者谁具有主管/监管权限？”只是办理申请、出具证明、执行规则、适用规则的普通机构名，不自动是这种主张。

`NOT_PRESENT`：没有该类角色主张。`PRESENT_CORRECT`：有且角色得到证据支持。`PRESENT_INCORRECT`：有且角色被证据否定。`PRESENT_EVIDENCE_INSUFFICIENT`：有但冻结材料无法判断。不能把有机构名字直接判 PRESENT，也不能把未给机关记录直接判错误。

区分网站托管方 host、网页发布者 page publisher、原始制定/发布机关 issuer、通过机关 adopting authority、修订机关 amending authority、批准机关、主管机关及官方转载方。甲网站转载乙委员会文件，不能推出甲制定。甲通过、乙公布，也不自动矛盾；先看角色是否同一且互斥。

版本、机关、实体内容三者独立：修订确有发生但修订机关写错，可以 version PRESENT_CORRECT、authority PRESENT_INCORRECT、overall FACTUAL_CONFLICT。反过来，机关正确也不能证明版本日期正确。不要为了让三列“看起来整齐”同步改错。

## 18. Historical / Temporal：历史与时间专章

**总体 LEGITIMATE_VERSION_OR_HISTORY 可以与 version NOT_PRESENT 同时成立。** 总体问命题是否依赖历史范围；版本字段问候选是否明示文档版本命题，二者范围不同。

做“替换为现在”检查：把明确历史/版本限定去掉，尝试理解为现在的同一个事实。若真假改变，或两个时期的比较失去原来意义，历史范围是实质的。这个检查只是帮助分类，不允许你改正式题文，也不能代替证据支持。

例如两份虚构不同文档分别给出早晚两个展览名额，候选正确比较名额提升。它可能合法历史，且 version NOT_PRESENT。如果明示同一规程的原版与修订版，则版本有主张。只列某会议通过时间，未依赖历史范围才成立，不能自动合法历史。

时间、对象、条件不同可解释冲突时，不能硬填 FACTUAL_CONFLICT。反之，候选把只适用于旧时期的规则当现行，又有证据链否定这个绑定，不能以“旧文本确实写过”免除当前冲突。

## 19. `minimum_external_evidence_needed`（最低外部证据）

它只度量**确认总体事实冲突**的最低外部需求，不度量填完全部字段需要多少材料。先 overall，再 minimum；不能用打开页面数量反推。

`NOT_APPLICABLE`（不适用）：overall 不是 FACTUAL_CONFLICT，包括当前一致、合法历史和总体证据不足。不是表示“完全不用证据”，也不是内部冲突的填写值。

`ZERO_EXTERNAL_EVIDENCE_REQUIRED`（零外部证据）：overall=FACTUAL_CONFLICT，且已锁 Phase1 local_internal_conflict=YES；文本自身同范围不相容断言足以确认。后来又读两份证据核查版本或机关，minimum 仍为 ZERO。

`ONE_OFFICIAL_EVIDENCE`（一份足够）：排除上述内部冲突路径后，E1 **或** E2 中至少一份单独就能确认总体冲突。“或”不要求两份都独立足够。另一份用于旁证或填子字段，不改最低数。

`MULTI_EVIDENCE_OR_VERSION_CHAIN`（必须联合）：E1 单独不足，E2 单独不足，联合证据/版本链才足以确认总体冲突。仅有两个文件、自己恰好看了两个、另一个字段要看第二份，都不满足此条件。

固定检验：先问文内是否已经确认；再暂时只留 E1 看能否确认；再只留 E2；只有两者各自不够而联合够才 MULTI。仅 E1 的行也可以 ONE，但不能因为想填 MULTI 自找 E2。如果总体根本不可确定，回到 overall INSUFFICIENT_EVIDENCE + minimum NOT_APPLICABLE。

## 20. `evidence_selection`（实际使用证据）

这是个人阅读/使用过程，不是“理论最优解”。`NONE`：实际未使用外部证据；`E1`：只使用本题 E1；`E2`：只使用本题 E2；`E1+E2`：两份都实际阅读使用。没有用过的不要报；只有 E1 的行不能填 E2 或 E1+E2。

如果确实读了两份作核验，即使其中一份单独已足够，记录 E1+E2，不为与 minimum 相同改成 E1。内部冲突可 ZERO + E1+E2；单证据冲突可 ONE + E1+E2；正确事实可 NOT_APPLICABLE + E1。

A 实际只用 E1，B 实际用 E1+E2，可以都符合规则。不要为了和对方一致修改此列，也不能把差异当作谁的事实答案错。理由若引用了 E1/E2 的内容，实际选择就应如实包含它；不能写“未用证据”却在 reason 中声称已经核读某条。

## 21. `phase2_issue`（第二阶段问题）

`NONE`（无独立问题）：材料/字段可作答，没有独立题目或证据缺陷。正确事实、合法历史、普通事实错误、已识别内部冲突都可以 NONE。FACTUAL_CONFLICT 不是 issue 名称，不能因为错就填 OTHER。

`SOURCE_UNREACHABLE`（给定来源无法访问）：官方入口与给定快照回退整体不可访问，影响判断。仅在线链接打不开但快照足够时不用。

`SOURCE_CONFLICT`（给定来源冲突）：供给的证据相互不相容，核对时间、对象、条件、版本后仍不能调和。不是“候选与证据不一致”；后者通常是总体事实冲突。旧新版本不同且可解释，不叫 SOURCE_CONFLICT。

`EVIDENCE_MISSING`（必要证据缺失）：题内材料没有支持可靠判断必需的事实或关系。可能整份所需来源未给，也可能现有可读文档缺关键修订记录。仅 E2 空白不构成此值。

`LATE_DISCOVERED_CANDIDATE_DEFECT`（晚发现候选缺陷）：第一阶段未发现，第二阶段才认出核心对象缺失、严重歧义或无法解释的问题。这条需要负责人退回候选质量处理，不以猜测继续普通判定；不重写已交第一阶段。

`OTHER`（其他行级问题）：确实存在本行候选/证据/字段接口问题，且前述值不合适。必须解释具体障碍。账号、会话身份、错发整份文件、独立性事故是整次运行问题，向负责人报告，不能在候选行填 OTHER 充当事故记录。普通错事实、自己不会操作 Excel 也不是 OTHER。

## 22. `possible_accidental_secondary_error`（可能的次生错误）

这是可见事实层面的检查，不要求你知道构造意图。先找核心事实问题，再问是否有另一个**独立事实原子**也被证据否定。独立原子可以单独写成一句主张，并非同一错误的重复说法或直接后果。

`YES`：能指出另一个独立错误及依据。`NO`：没有发现独立次生错误；也用于无核心冲突且未发现其它错误。`UNCERTAIN`：文本确实还有额外可验证主张，但材料不足以决定是否形成第二独立错误。

同一错误数字重复两遍，不算两个错误；内部冲突的两端不各算一个额外错误；错误生效日期导致对同一天适用状态的同一后果，不能仅因此重复计错。金额错误加独立公布机关错误则可 YES。不得猜“这个是不是作者故意设计”，只说明可见原子关系。

## 23. `evidence_sufficiency`（全行证据充分性）

`SUFFICIENT`：本行允许材料足够完成所有必需判断；也包括核心冲突仅凭候选即可确认、其余没有待证主张的情形。不是“链接都能打开”。

`INSUFFICIENT`：总体判断或重要必需子字段缺依据。比如数字冲突已被 E1 否定，但候选另有修订事件而材料没给沿革，overall 可冲突，version 可 PRESENT_EVIDENCE_INSUFFICIENT，sufficiency 仍不足。必须注明不足在哪个层面，不把整个总体自动抹成未知。

`UNCERTAIN`：不能稳定确定现有材料是否足够完成判断，说明是范围、覆盖还是材料理解问题。不能用来掩盖已经确认的缺证据，也不能因读得慢就选。

不足时不搜索、不请 AI 补资料。未提到某事件通常只是缺口，除非材料明确给了完整排他记录或否定断言；不能把沉默解释为反证。

## 24. `phase2_reason` / `reviewer_note`：怎样写理由

`phase2_reason` 每行必填，建议一两句，复杂关系可稍长。可照此结构组织，不必机械重复全部标签：“候选声称____；E1/E2 的____显示____；所以总体____，版本____，机关____；确认冲突最低需____。”没有冲突时说明 minimum 不适用；没有主张时说明未提出版本/机关命题。

好理由：“候选称预约上限为九人，E1 第三条为七人，单份足以否定；题文没有版本或公布机关主张，故二者未提出。”能看出对象、证据和最低路径。

另一好理由：“候选同一张票同日既有效又无效，文内已确认冲突，最低为零；另外实际读 E1 核对题目对象。”不能写 ZERO 却声称只有网站才能证明内部矛盾。

坏理由：“根据资料”“错了”“感觉不对”“应该是错的”“AI说如此”“网上好像不是”。这些要么无具体依据，要么越出范围。也不要用证据日期倒推不存在的版本主张。

`reviewer_note` 可空，用于必要补充，如哪个快照段落难辨、哪个额外主张缺依据。它不替代必填 reason，不加新置信度列，不写项目类别推测。

## 25. 跨字段一致性规则

| 规则 | 必须保持的关系 | 为什么 / 不要误读 |
|---|---|---|
| C1 | overall 非 FACTUAL_CONFLICT → minimum NOT_APPLICABLE | 最低证据只服务确认冲突 |
| C2 | overall FACTUAL_CONFLICT + 已锁 Phase1 local YES → minimum ZERO_EXTERNAL_EVIDENCE_REQUIRED | 文内已可确认；读证据不改变最低需求 |
| C3 | version NOT_PRESENT 不要求 overall 当前一致 | 实体错误也可能完全无版本主张 |
| C4 | overall LEGITIMATE_VERSION_OR_HISTORY 可搭配 version NOT_PRESENT | 历史命题范围大于文档版本范围 |
| C5 | overall FACTUAL_CONFLICT 可搭配版本/机关都 PRESENT_CORRECT | 核心实体内容仍可能错误 |
| C6 | selection 不决定 minimum | 实际用过两份不等于最低两份 |
| C7 | 事实冲突本身，issue 通常仍 NONE | 错事实与材料/接口缺陷不同 |
| C8 | 核心不足不能武断判冲突；若核心冲突已足够确定，子字段仍可不足 | 指明 sufficiency 不足的层面，不联动抹掉已确认冲突 |
| C9 | 版本/机关是否存在先看候选；正确性再查证据 | 元数据不能制造候选没说的主张 |
| C10 | 本行无 E2 → selection 不选 E2 / E1+E2 | 空 E2 是可选材料设计，不自动 issue |
| C11 | 非默认 Phase1 行有 issue_note；所有 Phase2 行有 phase2_reason | 提供可核验的具体理由 |
| C12 | 整体会话/路由问题单独报告，不作为行级 OTHER | 不污染候选事实判断 |

如果 Phase1 local 是 UNCERTAIN，不能在第二阶段偷偷改成 YES 来套 ZERO。说明现在确认了什么、为什么出现差异，请负责人处理；保留两阶段原答。跨字段检查帮助发现自己的填写矛盾，不是让你按别人的值“对答案”。

## 26. 高危歧义总表（20 项）

| 高危问题 | 错误理解 | 正确理解 | 应该看什么 | 不应该看什么 | 典型错答 | 正确判断方式 |
|---|---|---|---|---|---|---|
| 1 自然度 vs 真伪 | 错事实不自然 | 语言与真伪分开 | 句法表达 | 外部事实记忆 | 因日期错填 UNNATURAL | 表达顺畅仍 NATURAL |
| 2 自然度 vs 内部冲突 | 自相矛盾必病句 | 矛盾可自然表达 | 中文质量和互斥关系分别看 | 对“错”的厌恶 | YES 必伴 UNNATURAL | 两项独立 |
| 3 内部冲突 vs 外部错 | 单一数字错就是文内冲突 | YES 需两端可见 | 同主体范围条件时间 | 网上正确数字 | 只有一个数填 YES | 没有文内两端填 NO |
| 4 年份 vs 版本 | 年份即版次 | 年份可能只是背景 | 候选文档级命题 | 证据年份清单 | 见年份填 PRESENT | 先做存在测试 |
| 5 历史 vs 版本 | 历史必须版本 present | 可合法历史且无文档版本 | 历史限定及文档身份词 | 根据 overall 反推 | 合法历史强填 PRESENT | 两字段分别判断 |
| 6 “目前”两义 | 目前都是现行文档 | 实体现状与文档状态不同 | 修饰的是数值还是文档 | 单一关键词 | 目前票价填版次正确 | 无文档命题 NOT_PRESENT |
| 7 通过/公布 vs 版本 | 公布日自动版本 | 普通事件未必有版本语义 | 是否修订决定/转换 | 日期本身 | 通过会议即 PRESENT | 普通公布无版本，机关另判 |
| 8 普通 actor vs 机关主张 | 机构名就是权威 | 办理/出证未必是发布权限 | 机构承担的具体角色 | 名称级别 | 服务窗口办理填 PRESENT | 无权限/发布主张 NOT_PRESENT |
| 9 host/转载 vs issuer | 官网即制定机关 | 身份可能不同 | 题文角色、正文署名 | 域名联想 | 甲网站即甲制定 | 逐角色证据核对 |
| 10 三判断独立 | overall 错三列都错 | 错误可只在内容 | 独立命题原子 | 联动习惯 | 数字错版次也错 | 事件正确仍 version 正确 |
| 11 minimum vs selection | 看两个最低就两个 | 必需与实际分开 | E1-only/E2-only 是否足够 | 点击数量 | E1+E2 必 MULTI | 单份够即 ONE |
| 12 冲突 vs issue | 错事实都是问题 | issue 是独立材料/接口缺陷 | 可作答性 | 对答案错误的泛称 | 冲突填 OTHER | 可完整判断通常 NONE |
| 13 证据不足 | 未提到即否定 | 沉默通常是缺口 | 是否覆盖核心及子字段 | 记忆补证 | 缺沿革填 INCORRECT | PRESENT_EVIDENCE_INSUFFICIENT |
| 14 次生错误 | 同一错重复就是第二错 | 需独立原子 | 新主张及反证 | 设计意图猜测 | 重复数值填 YES | 重复或同因后果不重复计 |
| 15 候选缺陷 vs 证据问题 | 主体没写算缺官网 | 问题在题文或材料要区分 | 缺口位置 | 为继续而猜对象 | 裸对象仅 EVIDENCE_MISSING | 晚发现用候选缺陷值 |
| 16 双公布机关 | 两机关必矛盾/永不矛盾 | 同次互斥角色才矛盾 | 文件、行为、角色排他性 | 只数机构名 | 制定转载也 YES | 同次唯一机关互斥 YES |
| 17 一个数字错 vs 两原子错 | 两句等于两错 | 独立主张才第二错 | 重复与因果关系 | 句子数量 | 同数字重复填 secondary YES | 独立机关也错才可 YES |
| 18 Evidence 元数据倒灌 | 页现行即题文也声称现行 | 元数据仅验证已有主张 | 候选原句 | 把证据词抄回题文 | 裸法条 PRESENT | 无主张 NOT_PRESENT |
| 19 URL 临时失败 | 一打不开即不可用 | 先看冻结回退是否足够 | 本题摘录/全文 | 单次网络成败 | 立即 SOURCE_UNREACHABLE | 回退够仍 NONE |
| 20 E2 空白 | 没第二证据即缺失 | E2 可选，按命题需要判断 | 本行 E1 覆盖 | 强求每行两个来源 | 自动 EVIDENCE_MISSING | 够则 SUFFICIENT |

## 27. Phase2 虚构完整案例（案例 10–30）

所有 E1/E2 均为**虚构的给定官方记录**，只在本例中成立；不去搜索。未列 E2 的例子只有 E1。各表给出八个枚举及逐字段理由，表后给出必填 reason 与可选 note。题号和证据只读列由题包提供，不是你填写的答案。案例不依赖实际工作簿题号或事实。

### 案例 10：当前事实正确，E2 不必有

Candidate：“《星桥阅读室预约规程》第三条规定，一次可预约七个座位。”

虚构 Evidence：E1 第三条载“一次可预约七个座位”；本例无 E2。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 核心座位数受支持，无历史限定 |
| version_claim_status | NOT_PRESENT | 裸条文引用，没有版本命题 |
| authority_claim_status | NOT_PRESENT | 没有制定/公布机关主张 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 不是冲突 |
| evidence_selection | E1 | 实际只用 E1 |
| phase2_issue | NONE | 单证据足够，无材料缺陷 |
| possible_accidental_secondary_error | NO | 未见其它独立错误 |
| evidence_sufficiency | SUFFICIENT | E1 完成全部必要判断 |

phase2_reason：“候选称一次七座，E1 第三条支持；未明示版本或机关，最低冲突路径不适用。” reviewer_note：留空。易错点：E2 空白不等于证据缺失。

### 案例 11：实体错误，版本仍未提出

Candidate：“《星桥阅读室预约规程》第三条规定，一次可预约九个座位。”

虚构 Evidence：E1 为七座；E2 为同一制度的补充说明，也载七座。本例实际核读两份。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 九座被否定 |
| version_claim_status | NOT_PRESENT | 数量错不是版本命题 |
| authority_claim_status | NOT_PRESENT | 无机关主张 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 单份足够 |
| evidence_selection | E1+E2 | 实际核读两份 |
| phase2_issue | NONE | 错事实但题目和材料可作答 |
| possible_accidental_secondary_error | NO | 只有这一数值问题 |
| evidence_sufficiency | SUFFICIENT | 材料完整 |

phase2_reason：“候选九座，E1 第三条七座，单份已否定；E2 也核读过，实际选择两份不改变最低一份。” reviewer_note：留空。易错点：不能把 ONE 改成 MULTI，也不能因数字错判版本错。

### 案例 12：内部冲突，零外部证据

Candidate：“同一张银沙展馆电子票在同一时刻既有效又无效。”已锁 Phase1 local=YES。

虚构 Evidence：E1 提供该票种身份说明，不另有版本或机关主张需要验证。本例实际读 E1。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 同票同刻互斥已在文内确认 |
| version_claim_status | NOT_PRESENT | 票的有效性不是文档版本状态 |
| authority_claim_status | NOT_PRESENT | 无机关角色主张 |
| minimum_external_evidence_needed | ZERO_EXTERNAL_EVIDENCE_REQUIRED | 已锁 local YES，确认冲突无需外部 |
| evidence_selection | E1 | 实际核读 E1 |
| phase2_issue | NONE | 内部冲突本身不是材料问题 |
| possible_accidental_secondary_error | NO | 两端属于同一内部矛盾 |
| evidence_sufficiency | SUFFICIENT | 必需判断均可完成 |

phase2_reason：“同票同刻有效与无效不相容，文内已确认冲突，最低零；实际读 E1 核对票种。” reviewer_note：留空。易错点：本票有效性不等于文档版本，也不能把两端算第二错。

### 案例 13：必须联合才能判断变化方向

Candidate：“对照《星灯借阅规程》2031年原版与2034年修订版，预约名额减少了。”

虚构 Evidence：E1 只载原版名额五个；E2 只载修订版名额六个，分别确认版次。任一单份未给另一版数值。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 联合显示增加不是减少 |
| version_claim_status | PRESENT_CORRECT | 明示两个版次且均受支持 |
| authority_claim_status | NOT_PRESENT | 无机关主张 |
| minimum_external_evidence_needed | MULTI_EVIDENCE_OR_VERSION_CHAIN | 任一单份不知完整变化方向 |
| evidence_selection | E1+E2 | 实际联合使用 |
| phase2_issue | NONE | 两版不同可解释，无来源冲突 |
| possible_accidental_secondary_error | NO | 错在一个方向命题 |
| evidence_sufficiency | SUFFICIENT | 两份够验证全部主张 |

phase2_reason：“E1 原版五个、E2 修订版六个，须联合才知增加；候选写减少，版次本身正确。” reviewer_note：留空。易错点：错误方向不是错误版本身份。

### 案例 14：合法旧版本

Candidate：“《星灯借阅规程》2031年原版曾允许预约五个名额。”

虚构 Evidence：E1 原版五个；E2 2034 修订版六个，确认原版历史身份。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | LEGITIMATE_VERSION_OR_HISTORY | 五个真实但依赖旧版范围 |
| version_claim_status | PRESENT_CORRECT | 明示原版身份受支持 |
| authority_claim_status | NOT_PRESENT | 未说机关 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 不是冲突 |
| evidence_selection | E1+E2 | 实际看两份 |
| phase2_issue | NONE | 历史差异可解释 |
| possible_accidental_secondary_error | NO | 未见第二错误 |
| evidence_sufficiency | SUFFICIENT | 历史和当前范围明确 |

phase2_reason：“E1 支持原版五个，E2 后版六个；五个仅在历史版范围成立，版本身份正确。” reviewer_note：留空。易错点：合法旧事实不是当前数值冲突。

### 案例 15：历史比较，没有文档版本主张

Candidate：“2031年《星灯参观通知》安排五场展览，2034年《海湾活动公告》安排六场，后一次更多。”

虚构 Evidence：E1 第一通知五场；E2 第二公告六场。两份不同文档，未主张修订关系。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | LEGITIMATE_VERSION_OR_HISTORY | 真实比较依赖两个历史时间范围 |
| version_claim_status | NOT_PRESENT | 没说原版/修订/替代关系 |
| authority_claim_status | NOT_PRESENT | 未断言机关角色 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 比较正确，无冲突 |
| evidence_selection | E1+E2 | 两份都用 |
| phase2_issue | NONE | 材料可作答 |
| possible_accidental_secondary_error | NO | 两数及方向均正确 |
| evidence_sufficiency | SUFFICIENT | 证据覆盖比较 |

phase2_reason：“两份冻结文档支持五场与六场及增加方向，历史限定实质必要；候选没有文档级版本关系。” reviewer_note：留空。易错点：合法历史不强迫 version present。

### 案例 16：年份只是背景

Candidate：“2034年《白帆参观须知》包含十个章节。”

虚构 Evidence：E1 完整目录十章，该描述不依赖旧版差异。本例年份仅指叙述背景。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 十章事实受支持，无实质历史差异 |
| version_claim_status | NOT_PRESENT | 未称2034年版或修订 |
| authority_claim_status | NOT_PRESENT | 无机关主张 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非冲突 |
| evidence_selection | E1 | 实际只读 E1 |
| phase2_issue | NONE | 无独立问题 |
| possible_accidental_secondary_error | NO | 没有其它错误 |
| evidence_sufficiency | SUFFICIENT | 目录完整 |

phase2_reason：“E1 十章目录支持候选；2034年是背景而非版次或历史比较，版本未提出。” reviewer_note：留空。易错点：不能遇年份就合法历史或 present。

### 案例 17：明确修订，无年份也算

Candidate：“《甲区样例规程》已经修订。”

虚构 Evidence：E1 明确确认修订发生。本例继承冻结虚构边界例 NO_YEAR_REVISION 的逻辑。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 已发生事件受支持，未只声称旧版内容 |
| version_claim_status | PRESENT_CORRECT | 修订就是文档版本事件 |
| authority_claim_status | NOT_PRESENT | 未说由谁修订 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 无冲突 |
| evidence_selection | E1 | 实际读 E1 |
| phase2_issue | NONE | 材料可作答 |
| possible_accidental_secondary_error | NO | 无独立额外错误 |
| evidence_sufficiency | SUFFICIENT | 修订确认足够 |

phase2_reason：“E1 确认修订；候选虽然无年份仍有版本事件，没有机关断言。” reviewer_note：留空。易错点：版本不要求一定有日期。

### 案例 18：版本正确、实体内容错误

Candidate：“《甲区样例规程》2034年修订版把储物格上限定为十二个。”

虚构 Evidence：E1 确认2034修订版，上限为十个。逻辑继承 CORRECT_REVISION_WRONG_CONTENT，主题为虚构储物格。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 十二与十不符 |
| version_claim_status | PRESENT_CORRECT | 修订版身份正确 |
| authority_claim_status | NOT_PRESENT | 未称机关 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 单份否定数值 |
| evidence_selection | E1 | 实际使用 E1 |
| phase2_issue | NONE | 可清楚判断，无材料问题 |
| possible_accidental_secondary_error | NO | 唯一错误为数值 |
| evidence_sufficiency | SUFFICIENT | 版本和内容均可判 |

phase2_reason：“E1 确认修订版但上限十个，候选十二错误；版本命题自身正确，单份够确认冲突。” reviewer_note：留空。易错点：禁止把内容错误自动填版本错误。

### 案例 19：修订正确、修订机关错误

Candidate：“《丙区样例办法》由样例科技局修订。”

虚构 Evidence：E1 明确有修订，由样例委员会而非科技局完成。继承 CORRECT_REVISION_WRONG_AUTHORITY 的虚构模式。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 修订机关不符 |
| version_claim_status | PRESENT_CORRECT | 修订事件确有发生 |
| authority_claim_status | PRESENT_INCORRECT | 机关角色被明确否定 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 单份含实际修订机关 |
| evidence_selection | E1 | 实际只用 E1 |
| phase2_issue | NONE | 普通可判的机关错误 |
| possible_accidental_secondary_error | NO | 只有一项机关错误 |
| evidence_sufficiency | SUFFICIENT | 事件和机关均可判 |

phase2_reason：“E1 确认委员会修订；修订事件正确，科技局机关归属错误，E1 足以确认总体冲突。” reviewer_note：留空。易错点：机关错不自动版次错。

### 案例 20：只有通过/公布和机关

Candidate：“《青岚展馆预约办法》经甲委员会会议通过，以该委员会第十二号令公布。”

虚构 Evidence：E1 签署记录逐项支持通过、机关和文号；没有修订/生效转换主张。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 所述通过与公布事实受支持 |
| version_claim_status | NOT_PRESENT | 普通通过/公布非自动版本 |
| authority_claim_status | PRESENT_CORRECT | 通过和公布机关受支持 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非冲突 |
| evidence_selection | E1 | 实际读签署记录 |
| phase2_issue | NONE | 无独立问题 |
| possible_accidental_secondary_error | NO | 各事实均正确 |
| evidence_sufficiency | SUFFICIENT | 记录覆盖全部主张 |

phase2_reason：“E1 支持甲委员会通过及第十二号令公布；没有文档版本事件，机关主张正确。” reviewer_note：留空。易错点：文号或公布时间不是自动版本。

### 案例 21：版本而无机关，生效日期错误

Candidate：“《赤湾样例规则》2034年修订版自六月一日起施行。”

虚构 Evidence：E1 确认该修订版，但明示七月一日施行。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 施行转换日期错误 |
| version_claim_status | PRESENT_INCORRECT | 日期执行文档版本转换功能 |
| authority_claim_status | NOT_PRESENT | 没有机关 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 单份否定日期 |
| evidence_selection | E1 | 实际用 E1 |
| phase2_issue | NONE | 可判普通版本错误 |
| possible_accidental_secondary_error | NO | 日期是唯一核心错误 |
| evidence_sufficiency | SUFFICIENT | 日期清楚 |

phase2_reason：“E1 为七月一日施行，候选六月一日被否定；这是版本转换日期而非普通业务日期。” reviewer_note：留空。易错点：日期是否属于版本要看其功能。

### 案例 22：缺修订记录，不能断言不存在

Candidate：“《甲区样例规程》的现行版于2030年修订。”

虚构 Evidence：E1 只给实体条文，E2 只给现行名称，无修订沿革。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | INSUFFICIENT_EVIDENCE | 核心修订年无法可靠判断 |
| version_claim_status | PRESENT_EVIDENCE_INSUFFICIENT | 明示修订年但缺依据 |
| authority_claim_status | NOT_PRESENT | 未称机关 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 未确认冲突 |
| evidence_selection | E1+E2 | 两份都核读 |
| phase2_issue | EVIDENCE_MISSING | 必需沿革没有提供 |
| possible_accidental_secondary_error | NO | 没有第二独立主张 |
| evidence_sufficiency | INSUFFICIENT | 不能完成核心判断 |

phase2_reason：“候选声称2030修订，E1/E2 均无沿革，无法判修订年；不是反证，总体和版本均记不足。” reviewer_note：留空。易错点：没有记载不等于 PRESENT_INCORRECT。

### 案例 23：普通执行者不是发布机关

Candidate：“《星湾预约规则》规定，服务窗口收到预约后发放号码。”

虚构 Evidence：E1 对应条文支持窗口操作。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 业务规则受支持 |
| version_claim_status | NOT_PRESENT | 无版本身份或转换 |
| authority_claim_status | NOT_PRESENT | 窗口只是执行者 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 非冲突 |
| evidence_selection | E1 | 实际用 E1 |
| phase2_issue | NONE | 无材料问题 |
| possible_accidental_secondary_error | NO | 无第二错误 |
| evidence_sufficiency | SUFFICIENT | 条文够判断 |

phase2_reason：“E1 支持窗口发号码；窗口是业务执行者，候选并未说它制定或主管文档。” reviewer_note：留空。易错点：机构名不能自动制造 authority。

### 案例 24：官网转载不等于制定

Candidate：“《青石园样例规程》由甲委员会制定。”

虚构 Evidence：E1 虽托管在甲官网，但正文署名乙委员会，明确甲仅转载、原制定机关为乙。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 制定机关被否定 |
| version_claim_status | NOT_PRESENT | 没有版本事件 |
| authority_claim_status | PRESENT_INCORRECT | 甲仅转载，不是制定者 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 明确两种角色 |
| evidence_selection | E1 | 实际读 E1 正文 |
| phase2_issue | NONE | 正文身份足够，无独立问题 |
| possible_accidental_secondary_error | NO | 只有机关绑定错误 |
| evidence_sufficiency | SUFFICIENT | 角色可验证 |

phase2_reason：“E1 正文明示乙制定、甲转载，甲官网托管不能支持甲制定，单份足够否定。” reviewer_note：留空。易错点：不能单看域名。

### 案例 25：总体冲突已定，版本子字段仍不足

Candidate：“《星桥预约规则》2030年修订版规定上限九座。”

虚构 Evidence：E1 明确本题所涉上限为七座，但冻结材料未提供任何修订年/版次沿革，无法判2030身份。上限冲突不依赖未知版次才能确认，本例证据明确覆盖候选所指范围。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | E1 已可靠否定所涉九座命题 |
| version_claim_status | PRESENT_EVIDENCE_INSUFFICIENT | 修订年仍无记录 |
| authority_claim_status | NOT_PRESENT | 无机关命题 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | 确认总体核心冲突只需 E1 |
| evidence_selection | E1 | 实际只用 E1 |
| phase2_issue | EVIDENCE_MISSING | 缺修订身份依据 |
| possible_accidental_secondary_error | UNCERTAIN | 额外版次主张无法判断是否另错 |
| evidence_sufficiency | INSUFFICIENT | 全行重要子字段不能完成 |

phase2_reason：“E1 对候选范围已否定九座，故总体冲突及最低一份确定；修订年记录缺失，版本与可能额外错误仍不足。” reviewer_note：“不足针对版次，非核心数值反证。” 易错点：只有核心冲突已足够确定才可此组合，不能靠猜测绕过总体不足。

### 案例 26：一个数字错误外，另有独立机关错误

Candidate：“《白帆储物规则》由甲委员会公布，每人可用九个格子。”

虚构 Evidence：E1 明示乙委员会公布，每人七个格子，两个事实相互独立。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | FACTUAL_CONFLICT | 数值与机关分别被否定 |
| version_claim_status | NOT_PRESENT | 未声称版本身份/转换 |
| authority_claim_status | PRESENT_INCORRECT | 公布机关甲错 |
| minimum_external_evidence_needed | ONE_OFFICIAL_EVIDENCE | E1 单份可确认总体冲突 |
| evidence_selection | E1 | 实际用 E1 |
| phase2_issue | NONE | 两错可明确判断，无资料障碍 |
| possible_accidental_secondary_error | YES | 核心数量错误外另有独立公布机关错误 |
| evidence_sufficiency | SUFFICIENT | 两原子均有依据 |

phase2_reason：“E1 为七格、乙公布；候选九格为核心错误，甲公布为第二独立错误，单份证据足够。” reviewer_note：留空。易错点：不是按句子数计错，也不猜作者设计。

### 案例 27：晚发现文本缺陷

Candidate：“该规程要求访客先领取该证件。”此前 Phase1 未发现对象缺失。

虚构 Evidence：E1 提供两种不同规程和证件制度，无法唯一确定题文指哪一种。不能用 E1 替作者补全对象。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | INSUFFICIENT_EVIDENCE | 核心对象无法唯一绑定 |
| version_claim_status | NOT_PRESENT | 没有文档级版本主张 |
| authority_claim_status | NOT_PRESENT | 没有机关主张 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 无可靠总体冲突 |
| evidence_selection | E1 | 实际核读 E1 |
| phase2_issue | LATE_DISCOVERED_CANDIDATE_DEFECT | 问题在题文自身对象缺失 |
| possible_accidental_secondary_error | UNCERTAIN | 无法稳定分解额外事实是否错误 |
| evidence_sufficiency | INSUFFICIENT | 本行不可可靠完成 |

phase2_reason：“‘该规程/该证件’无唯一对象，E1 两制度不能替题文补主体，第二阶段登记晚发现缺陷。” reviewer_note：“请负责人退回题文质量处理，不改已交 Phase1。” 易错点：不是增加网页就能补救的普通来源缺失。

### 案例 28：现状数值和现行文档是不同主张

Candidate：“根据2034年《参观票价答复》，目前普通参观票价为八元。”

虚构 Evidence：E1 同年答复确认当时的目前票价八元，本例以其明确历史答复范围作比较基准；E2 后来答复票价十元。两份实际核读。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | LEGITIMATE_VERSION_OR_HISTORY | 八元成立依赖2034答复的时间范围 |
| version_claim_status | NOT_PRESENT | “目前”修饰票价，不是文档现行版 |
| authority_claim_status | NOT_PRESENT | 未指定答复的发布机关或权限关系 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 历史命题受支持 |
| evidence_selection | E1+E2 | 两份均实际读 |
| phase2_issue | NONE | 时间差异可调和 |
| possible_accidental_secondary_error | NO | 不是把后来的十元当八元反证 |
| evidence_sufficiency | SUFFICIENT | 历史语境明确 |

phase2_reason：“E1 的2034答复支持当时八元，E2 后来十元不否定历史范围；‘目前票价’没有文档版本主张。” reviewer_note：留空。易错点：若候选无历史答复限定而直接称当前八元，应另按证据时间范围判断，不能照抄此例。

### 案例 29：明确修改决定身份

Candidate：“《关于修改〈青岚展馆规程〉的决定》经甲委员会会议通过。”

虚构 Evidence：E1 确认同名修改决定及甲委员会通过。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | CURRENTLY_CONSISTENT | 修改决定及通过事实受支持 |
| version_claim_status | PRESENT_CORRECT | 决定名明确修改文档身份 |
| authority_claim_status | PRESENT_CORRECT | 通过机关甲正确 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 无总体冲突 |
| evidence_selection | E1 | 实际用 E1 |
| phase2_issue | NONE | 没有材料缺陷 |
| possible_accidental_secondary_error | NO | 事件和机关均正确 |
| evidence_sufficiency | SUFFICIENT | 所有主张可判 |

phase2_reason：“E1 支持修改决定身份与甲通过，版本事件和机关分别成立；没有总体冲突。” reviewer_note：留空。易错点：不是所有“经会议通过”都 version NOT_PRESENT，标题本身可有修改语义。

### 案例 30：来源不可调和，不是候选自动错

Candidate：“《溪谷展馆预约规则》规定同类访客提交两份材料。”

虚构 Evidence：E1 同条同条件载两份；E2 明示同一版本同一条同一条件载三份，提供材料没有能调和的时间、范围或更正关系。

| 字段 | 答案 | 理由 |
|---|---|---|
| overall_fact_status | INSUFFICIENT_EVIDENCE | 无法可靠解决来源间不相容 |
| version_claim_status | NOT_PRESENT | 候选本身只是实体条文 |
| authority_claim_status | NOT_PRESENT | 无机关主张 |
| minimum_external_evidence_needed | NOT_APPLICABLE | 没有可靠确认总体冲突 |
| evidence_selection | E1+E2 | 两份都核读 |
| phase2_issue | SOURCE_CONFLICT | 冻结来源彼此冲突，非仅候选与来源不同 |
| possible_accidental_secondary_error | NO | 无第二独立候选主张 |
| evidence_sufficiency | INSUFFICIENT | 来源冲突使可靠判断不足 |

phase2_reason：“同版同条件 E1 两份、E2 三份，给定资料无调和关系，不能择一武断判候选错，登记来源冲突。” reviewer_note：留空。易错点：旧新版本数值不同但有关系时不能套 SOURCE_CONFLICT。

## 28. FAQ：常见问题

**Q1 我知道事实错，Phase1 能直接标冲突吗？** 不能。只有候选自身至少两个同范围不相容命题才能 YES。

**Q2 句子内部矛盾是否必然 UNNATURAL？** 不必然。语法顺畅可 NATURAL + YES，两个字段分别评价。

**Q3 有年份版本一定 PRESENT 吗？** 不一定。年份背景、业务日期不自动成为文档版本；看候选是否明示版次、修订或转换等。

**Q4 Evidence 写现行有效，为什么 version 可能 NOT_PRESENT？** 因为候选没提出文档状态；证据只能验证主张，不能制造主张。

**Q5 “目前标准”为什么不一定是版本？** 它可能只描述实体数值。只有“现行某文档/某版”等文档级状态才进版本字段。

**Q6 两个机关出现一定冲突吗？** 不。先辨制定、通过、公布、转载等角色。只有同次行为相同范围下的互斥断言才文内冲突。

**Q7 用了两份 Evidence，最低为什么 ONE？** 一份已足够确认总体冲突，另份实际作核验/子字段依据；实际过程不决定最低路径。

**Q8 事实错，issue 应 OTHER 吗？** 不。普通事实错通常 NONE。OTHER 仅其他真实行级问题。

**Q9 两个人 selection 不同怎么办？** 你如实填自己的使用过程，不与对方对答案；负责人以后处理过程差异。

**Q10 证据不足能自己搜索吗？** 不能。记录缺哪项依据与不足状态，仅用提供的本行材料。

**Q11 不知选哪个能问另一人吗？** 不能问具体答案。按字段的不确定值说明理由；操作问题向负责人报告。

**Q12 能用 AI 解释后再自己填吗？** 不能。这仍会让外部 AI 参与判断，破坏独立人工作答。

**Q13 内部冲突 ZERO 还能看证据吗？** Phase2 可用本行证据核对子字段；selection 如实记录，minimum 仍 ZERO。

**Q14 E2 空白怎么办？** 本行只给 E1。够就充分，不够记录缺口，不自行补 E2。

**Q15 修订内容数字错，版本一定错吗？** 不。修订事件/身份受支持可 PRESENT_CORRECT，数字错误归总体；机关同样独立。

**Q16 整个事实已确认冲突，但某个子字段缺证据呢？** overall 保留已确定冲突，子字段填对应不足，sufficiency 说明全行不足；不得用这一例外猜测核心冲突。

**Q17 第二阶段发现第一阶段遗漏能改第一阶段吗？** 已提交原件不能回写。晚发现候选缺陷在 Phase2 如实记录并报告负责人。

**Q18 浏览器打不开官方链接是否立即不足？** 先看冻结摘录/同题全文。回退材料足够就不因单次网络失败改答案。

## 29. 一页式人工标注速查表

| Phase1 五项 | 怎么填 |
|---|---|
| text_naturalness | NATURAL 通顺；MINOR_ISSUE 轻微生硬；UNNATURAL 明显表达障碍。真伪不参与。 |
| local_internal_conflict | YES 同主体/条件/时间下文内互斥；NO 没有；UNCERTAIN 文本范围模糊。 |
| self_containment | PASS 核心可独立理解；FLAG 必要对象/上下文缺失；UNCERTAIN 难以稳定判断。 |
| ambiguous_referent | YES 关键指代多解；NO 无多解；UNCERTAIN 文本无法稳定区分。 |
| meta_or_template_language | YES 实验话语/明显拼接；NO 没有；UNCERTAIN 有疑点难断定。 |

任一非 NATURAL / NO / PASS / NO / NO → issue_note 必填。

| Phase2 八项 + 理由 | 速查 |
|---|---|
| overall_fact_status | 核心不足→INSUFFICIENT_EVIDENCE；不可调和否定→FACTUAL_CONFLICT；支持且依赖历史→LEGITIMATE_VERSION_OR_HISTORY；否则支持→CURRENTLY_CONSISTENT。 |
| version_claim_status | 候选无文档级主张→NOT_PRESENT；有→PRESENT_CORRECT / PRESENT_INCORRECT / PRESENT_EVIDENCE_INSUFFICIENT。 |
| authority_claim_status | 无机关角色主张→NOT_PRESENT；有→同上三种 PRESENT 值；普通业务执行者不是发布机关。 |
| minimum_external_evidence_needed | 非冲突→NOT_APPLICABLE；冲突且锁定 local YES→ZERO_EXTERNAL_EVIDENCE_REQUIRED；单份够→ONE_OFFICIAL_EVIDENCE；各自不够联合够→MULTI_EVIDENCE_OR_VERSION_CHAIN。 |
| evidence_selection | 实际 NONE / E1 / E2 / E1+E2；不是最低需求。 |
| phase2_issue | NONE / SOURCE_UNREACHABLE / SOURCE_CONFLICT / EVIDENCE_MISSING / LATE_DISCOVERED_CANDIDATE_DEFECT / OTHER；普通错不自动 issue。 |
| possible_accidental_secondary_error | YES 第二独立事实错误；NO 没有；UNCERTAIN 额外主张缺依据。 |
| evidence_sufficiency | SUFFICIENT 全行可判；INSUFFICIENT 缺必需依据；UNCERTAIN 充分性不能稳定判定。 |
| phase2_reason | 每行必填候选+证据+为什么；reviewer_note 可空。 |

版本四问：候选说了文档级主张吗？是否仅年份/实体/普通公布？证据是否验证而非制造主张？版本与实体/机关分开了吗？

机关三问：是发布/通过/修订/主管角色还是普通执行者？是否把 host/转载当 issuer？给定材料能否证明该角色？

五个禁止：不查额外网页；不让 AI 参与；不与另一人对答案；不改题文/ID/结构；不提前看 Phase2 或回写已提交 Phase1。

## 30. 提交前最终 Checklist

Phase1：

- [ ] 没看正式证据或 Phase2，没查网页，没猜实验类别。
- [ ] 自然度不是真伪，冲突只看文本内部。
- [ ] 五项每行完整，异常均有具体 issue_note。
- [ ] 144 行、题号、题文、列结构和对应关系未变。

Phase2（仅单独放行后）：

- [ ] 只用本行 E1、可选 E2 和提供的同题冻结回退。
- [ ] 先判核心 overall，版本存在先只看候选，机关独立判断。
- [ ] ZERO / ONE / MULTI / NOT_APPLICABLE 按最低路径，不按实际点击。
- [ ] selection 如实，无 E2 的行不报 E2。
- [ ] 普通事实错误没有误填 issue，额外错误有独立原子依据。
- [ ] 不足就说明缺口，不搜索补证；每行都有 phase2_reason。

两阶段共用：本人独立完成，无 AI、无互看、无讨论答案；保存自己的规定 RETURN 文件名与 `.xlsx` 格式；原件提交后不再重存覆盖。最终接收由负责人核验，本手册没有自动发放、接受或开始下一阶段的效力。

## 31. 本手册规则版本与审计出处

当前填写体系：Core144 Human 工作簿 V1。基础规则 Formal Guide V4；追加解释 V4.1（机关、版本与行级 issue 范围）、V4.2（候选自身版本主张、修改决定身份）、V4.3（历史/时间不自动等于文档版本）。本手册把人工所需规则全部展开，不要求你读其他文档才能填写。

当前工作簿的 Phase1 五项判断与 issue_note 是实际填写体系；早期文档中的别种第一阶段列不供本次填写。第二阶段内部冲突使用 ZERO_EXTERNAL_EVIDENCE_REQUIRED；版本只评文档级事件/身份/状态/关系/转换，实体内容和机关独立。不要把较早说明书的不同填写方法拼进当前答卷。

以下链接仅供研究审计，不是额外证据或作答前提；不得据此浏览实际候选答案或其它标注人材料：

- [V4 基础规则](../formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md)
- [V4.1 字段范围](../formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md)
- [V4.2 候选自身版本主张](../formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4_2_VERSION_SCOPE_DECISION.md)
- [V4.3 时间与版本分离](../formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4_3_TEMPORAL_VS_VERSION_SCOPE.md)
- [冻结虚构边界例](../formal240/PAPER1_FORMAL_ANNOTATION_BOUNDARY_EXAMPLES_V1.json)

本手册新增解释和虚构教学例，不修改冻结规则或工作簿。正式题目答案只能来自你本人按阶段独立判断；教学案例不是实际题目的答案表。
