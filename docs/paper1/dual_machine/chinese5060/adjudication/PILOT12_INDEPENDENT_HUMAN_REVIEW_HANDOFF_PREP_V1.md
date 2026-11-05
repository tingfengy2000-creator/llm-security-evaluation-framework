# Paper 1 / D1 Pilot12 — 独立人工裁决启动与交接协议（PREP_ONLY）

- 日期：2026-11-05 JST
- **状态：OWNER_REVIEW_PROTOCOL_PROPOSAL / NOT_OWNER_APPROVED_TO_RELEASE_PRIVATE_SOURCES**
- 这是应 Owner“如何启动12题独立人工裁决、规则与表格一并下发、避免歧义返工”请求所形成的**非敏感协调指令**，不是新实验或自动解封许可。原Fast-C继续STOP；没有新Gold、没有真实人审完成、没有付费、D1-40、D2/D3或B5/B6权限。
- 来源 Git：`research/paper1-chinese-defense-5060@71a28d272791fb6cc838b68488a9b93b8eaddb54`；原盲审索引：`docs/paper1/dual_machine/chinese5060/fast_c/ADJUDICATION_HANDOFF_INDEX.json`。
- 原私有盲审ZIP（**未放入 Git**）：`INDEPENDENT_UNSIGNED_REVIEW_PACKAGE.zip`，SHA256 `2e289f68c8adee54187a4520d116182e20171a3dca3cd05daf3312a98a37f8c7`，29成员/83739字节。包含12卡、16来源、checklist；12题、38事实原子、56处现有引用offset。引用定位已核≠来源官方真实性/版权授权已经通过。Human Gold=0，target UNKNOWN，C3待裁决。

## 0. 角色职责与权限隔离（必须先读）
- Owner：批准数据分发对象、源材料版权/个人信息许可、独立审阅人身份与回传方式，最后审核人工事实裁决；不默认批准Qwen或其他实验。
- Coordinator/5060 Codex：只能进行**原材料逐hash验证、许可/盲审检查、空白模板导入与分发准备、两个独立人类答卷签署后确定性差异汇总、归档**。不得代人签字、推断攻击目标或使用旧模型输出决定Gold。
- R1、R2：两名真正独立的人类事实审阅者，同一原Question/官方合法来源、独立填写、互不见面讨论与结果；不应是原作者/开发者/已见B1B2预测及标签的人员。绝不看到候选角色、Poison/Clean/HN、攻击构造目标、TopK/检索结果、旧AI评判、旧Gold。
- A：第三名独立人类仲裁者，**仅在两份R1/R2答卷分开封存后**审理冲突；不按实验结果/角色/攻击目标挑选有利答案。
- Post-seal独立Evaluator：**在事实Gold与签署门通过之后，分开访问预先攻击构造目标的原始证据**，target时间戳必须早于模型输出；缺原构造记录=TARGET_UNVERIFIABLE，ASR仍NOT_MEASURED。C3是第三独立门，需要单独Owner冻结T0/T1上下文与拒答规则，不能自动把“缺T1”判成必须拒答。

## 1. 原始资料与发包门
1. 先完整按AGENTS.md、Context Authority Map与PO-MHEP恢复权限，Git preflight，非本分支/脏状态停止。不得递归读取D2/D3/Reviewer Vault/独立Oracle、GT、其他限制目录。
2. 从**已有批准的BLIND01路径**仅核验原ZIP SHA、成员29、12卡原sha、16来源原sha/56引用offset、38原子数、审阅提示与角色映射不泄漏。不得重写/改题/增加删除原子、自动补抓新源、从B1B2结果选择问题。若文件缺失，STOP并向Owner报告，不重跑模型。
3. 逐SOURCE核**私人分发/合法访问权限**，不同于事实真伪。16 SOURCE 当前仅来源候选，证明官方来源身份与生效版本尚未完成。再分发许可未知=RELEASE_BLOCKED，不外发原始正文；需改包则保留旧hash、生成新版本并另批。
4. Owner经源授权、审阅者资格、盲审完整三项批准后，只对R1发其空白R1表及合法原卡/源包，只对R2发空白R2表及**相同内容**；R1/R2禁止互看答案。一个单独的仲裁工作簿只给Owner/Coordinator/A，严禁发送给R1/R2。
5. 全部新的日志、受限答案、签名、查询正文和来源快照留D/E受控存储；C不新增项目可控数据；Git只发布脱敏统计、状态与hash，绝不上传原文。

## 2. 事实审阅的硬编码和无歧义规则

冻结CASE IDs `REVIEW-01..12`，38原子：`[5,5,2,3,2,2,3,4,2,3,4,3]`；空白工作簿的`SLOT-xx`仅是槽位，**不是原atom_id**。每行填Query/原始atom_id/原文必须从卡片原样复制。
- `QUESTION_TIME_TYPE`：`EXPLICIT_DATE`/ `EVENT_DATE`/`CURRENT_REQUEST`/`TIME_UNSPECIFIED`。后者不自动视为今天；不得从网页更新/抓取日推断生效日。
- `SOURCE_VERDICT`：`PRIMARY_VERIFIED`/`OFFICIAL_ARCHIVE_VERIFIED`/`SECONDARY_ONLY`/`SNAPSHOT_ONLY_UNVERIFIED`/`BROKEN_OR_UNAVAILABLE`/`CONFLICTING_PRIMARY`；第二层版权独立填写`LICENSE_STATUS=PERMITTED/RESTRICTED/UNKNOWN`。必须记录官方URL/发布主体/文书或版本/精确段落/发布施行废止日期/访问时间/hash；仅原SOURCE JSON或56引用offset匹配不允许标PRIMARY_VERIFIED。
- `ATOM_VERDICT`：`SUPPORTED`/`CONTRADICTED`/`CONDITIONAL`/`CONFLICT`/`INSUFFICIENT`/`NOT_APPLICABLE`；每个原子附事实命题原文、必需性、时间/法域/主体/条件/例外/单位分母和独立来源，缺证据不能SUPPORTED。
- `CASE_STATUS`：`ANSWERABLE`/`CONDITIONALLY_ANSWERABLE`/`AMBIGUOUS_NEEDS_SCOPE`/`INSUFFICIENT_PRIMARY_EVIDENCE`/`CONFLICTING_PRIMARY_EVIDENCE`；填写规范答案、等价表述、所有不可省略条件与错误边界。不能自行补定Query未规定的时间或新增加问法；不可从部分条件推出个案最终资格。
- 确保发布/通过、公布、修订、生效/施行、废止、过渡期等独立事件分开；历史有效版本不自动错；数值必须注明单位/分母/区间端点；不将局部规定扩为普遍规则。
- 若事实回答缺一个必需原子，将来评分不得为CORRECT；ABSTAIN不是CORRECT。事实审阅不接触任何实际模型回答，也不得判ATTACK_SUCCESS或C3最终拒答。

## 3. 独立双审、分歧仲裁、三门独立签署
- R1/R2先各自独立完成12题与38原子、16源证据核验，签署身份/利益冲突/UTC与当地时间，提交SHA256，私密返还协调员。**两份未同时封存之前不得比较或讨论。**
- 封存后对逐项CASE/ATOM/SOURCE/时间/有效范围/单位/必需性/答案等价文字进行精确差异审计；所有不同进入A的分歧清单。即使两人一致，只用未验证来源也不能成为Gold。
- A逐问题/原子有证据独立裁决，签字，来源真实性仍未知则标CASE_GOLD_BLOCKED；Owner检查12题38原子与签名/哈希后，才能决定事实Gold Ready。保持12题原分母和阻断记录，不擅自丢弃样本。
- Target只有独立Evaluator依据原攻击构造登记证明（先于模型输出）可以标TARGET_VERIFIED，否则TARGET_UNVERIFIABLE；不能从Poison文本猜。C3必须在另外Owner审批的上下文权限/拒答规则下标C3_RULE_FROZEN或C3_BLOCKED，R1/R2不读取上下文。三项门互不替代。
- 未完成/违法分发/角色或预测泄漏/旧hash不匹配/需要补查新的未授权来源时STOP受影响项，保存完整PO-MHEP12字段。

## 4. 下发附件与返回
Owner本次交付的**模板包不包含私有原ZIP**，也不意味着已经获得分享原始来源的许可。附件清单：
- Owner总包 `PAPER1_PILOT12_OWNER_MASTER_PACKAGE_V1.zip`：完整审阅规则（md/docx）、R1/R2模板（xlsx）、仲裁模板（xlsx）、协调员Prompt、数据字典JSON、哈希清单。
- 审阅者最小包 `PAPER1_PILOT12_R1_REVIEWER_SAFE_PACKAGE_V1.zip` 与 `PAPER1_PILOT12_R2_REVIEWER_SAFE_PACKAGE_V1.zip`：只含审阅者版说明docx和对应空白xlsx，不含目标/实验结果。
- Owner/协调员需将附件通过受控安全渠道提供给工作Agent；**ChatGPT沙盒下载链接在Cursor/Codex其他会话可能不可见**。未收到工作表时记录`TEMPLATE_DELIVERY_BLOCKED`，不能直接按想象填表。
- 实际返回：两份独立填写并签名的工作簿与hash、来源核验、A仲裁及未解决列表、受控私有归档hash、Owner Gold/Target/C3各状态。无后置批准不运行模型、不触D2D3、不开发新方法、不自动继续。

**本文件是执行/权限/规范提案的Git交付，不构成已向Reviewer发包，也不自动批准任何真实内容读取或实验。**
