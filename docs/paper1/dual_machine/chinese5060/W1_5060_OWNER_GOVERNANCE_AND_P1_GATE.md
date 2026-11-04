# W1 5060 Owner治理同步与P1准入

2026-11-04 JST；`P1_PREPARATION_COMPLETE / REAL_PILOT_BLOCKED`。完成后停止，不自动进入下一阶段。
本报告与[场景公平性报告](W1_5060_P1_SCENARIO_AND_FAIRNESS_GATE.md)共同交付；不改研究方向、正式基线或Ground Truth。

## 动态Git和Owner明确决定

启动5060 HEAD `066ce0ced75c9bbf61cfec03f3d0d93aa8324f07`；5090最新ref
`aa85841ff83be31c86e0fa305d3a84d70f2158b5`，fetch/git-show已核。
共同祖先`4dc9161e79b79ece70a7c17144175a19b985770d`；启动时分支提交差异14/2。
5060既有开发起点`8dec9453de2ebd5ea03e4cbdf753b2f0d7347177`，5090研究起点为共同祖先。
这些差异按Owner决定保留，不是要求对齐起点的blocker；不能据它们假设两机环境或实验合同相同。
本轮新源码只在`research/paper1-chinese-defense-5060`，执行SHA
`fcdd848e29e3fea97b11a6352a4ff8e1665f4071`；未reset/rebase/merge/cherry-pick。

| Owner Decision | 本次明确来源及接受范围 | 未授予 |
|---|---|---|
| W1-OD-20261104-5090-ENV-01 | Owner当前会话明确说明：5090独立兼容环境有条件接受；原环境保留、差异披露 | 模型下载/许可替代、运行Claim、论文效果接受 |
| W1-OD-20261104-DUAL-GOV-02 | Owner当前会话明确决定：保留两机独立分支及既有起点，优先补差异和审批链 | 重置/变基/跨分支合并/cherry-pick、主线合并 |

两项已追加到`docs/governance/project_owner_decision_register.md`；没有改写旧批准或5090远端文件。
当前P1准备授权来源为本会话两次监督指令：仅零付费工程与协议、固定Pilot12、不得B5/B6/D1-40或变更生成器。

5090脱敏记录的上游SHA `ba2a17efba165d45409114df2d70b030ade1e1b8`，v0.2 tag commit
`2be0bb2f84b2bf4ef4a0f6d8387ad1c0d3df847a`；库和artifacts不是同一执行入口。
官方环境torch2.4.0+cu121在sm120内核失败；独立兼容环境torch2.8.0+cu128，triton3.4.0、sympy1.14.0、bnb0.45.5。
以上是5090Git记录派生事实，本机未重放其原始环境操作。模型权重未下载，Claim1–3均NOT_RUN，ASR/Accuracy未测。
早期run_manifest/claim报告仍写“环境缺失”，按历史R0快照保留；后来的安装章节和本次Owner决定覆盖环境接受状态，
不把旧理由照抄成仍待安装，也不据此自动关闭权重许可与Claim审批门。
完整git-show内容hash及来源链见[p1证据](p1/evidence/HANDOFF_5090_RECEIPT.json)。

## 独立查询准入与证据边界

12题V2身份、38字段、56引用、18源hash通过；36互斥世界设计已保存，原Pilot选择未改变。
全部Query仍为AI开发草案，不是人工Gold；本轮审阅没有产生新的独立盲命题或GT。
12题均需答案等价/条件/版本评分冻结、逐世界足证性、独立官方根、事先攻击目标裁决。
旧Top5有5/36世界缺引用来源；新统一背景的结构存在性不能替代TopK召回或T1可信度。
原文/答案/角色映射/world正文只在Git外；公开矩阵只含计数、hash与状态。

| 准入项 | 状态 | 处理 |
|---|---|---|
| Git/两机起点差异/Owner环境接受链 | VERIFIED_WITH_OWNER_CONDITIONS | 保留各分支，不跨分支改代码 |
| Pilot12身份与来源字节/引用定位 | PASS | 不重新抽样或依据结果删题 |
| D1路径白名单与整库隔离设计 | PASS_FOR_PREPARATION | 非OS沙箱；保留P0事件 |
| 真实chunk/tokenizer/检索索引/TopK | NOT_RUN | 按待审查配置后续零费用预检，不声称已召回 |
| B1原版库vs论文artifact轨道 | OWNER_REVIEW_REQUIRED | 两者分开；默认embedding revision/caches未知 |
| T1独立官方根与固定包 | BLOCKED | 不能授信D1来源副本或按答案选证据 |
| T2按需官方检索 | DISABLED | 不得自动扩源 |
| 答案范围/攻击目标/C3评分 | NEEDS_ADJUDICATION | 不把AI提案升Gold或由标签猜目标 |
| 当前账号精确Qwen可用性/精确token计数 | UNKNOWN_NO_PAID_PROBE | 不用别名替换、不探测 |
| 真实付费Pilot/B5/B6/D1-40/5090 Claim | NOT_APPROVED_TO_START | 本轮停止在合同准备 |

## 费用与模型核验

历史361物理calls，输入2,984,761/output205,288tokens，usage估算CNY7.611826；本轮新增0。
Owner同会话报告CNY5.903857258+1.624238656=7.528095914、无未结算、账户可继续用；
差额CNY0.083730086保留，不能推断活动折扣或周期。具体账户余额及账单范围未机器对账。

本轮已查官方精确快照页：北京输入≤256K原价每百万token输入CNY2、输出CNY8，超过256K档为6/24；
不使用别名优惠、Batch价或缓存折扣。页面列出精确快照不证明本账户已开通。
来源：[阿里云qwen3.7-plus精确快照及北京价格](https://help.aliyun.com/zh/model-studio/qwen3-7-plus)。
另一价格总表直连曾超时，未用第三方或静默替代；上述官方模型页可核价格。[价格与费用方案](p1/evidence/PRICE_AND_BUDGET_PLAN.json)。

条件式最坏单批=一个物理请求，输入cap16384，输入/输出各预留16token：

| 用途 | 输出上限 | CNY最坏保留 |
|---|---:|---:|
| 生成 | 2048 | 0.049312 |
| 核验 | 1024 | 0.041120 |
| 可选未来judge（当前禁用） | 2048 | 0.049312 |

36世界×5方法，每信任层最多180生成、360核验；计入可选180judge时上界CNY32.555520；
若同时T0/T1为65.111040，加历史较高usage为72.722866。仅是参数cap成立时的算术情景，
不含C3、额外方案、未知收费或重试，也不保证本账户可付或整个研究完成。不得据此启动批次。
精确输入token计数尚缺，故不能把16384当实际已验证token数；估算不代替逐请求provider usage与结算。
累计上限USD30、USD25预警、投影达到USD28停止新批，沿用6CNY/USD仅为历史保守记账界，不是现汇。
每次准入需合并生成/核验/评判/探测、其他工作线支出与预留；未知usage保留最坏额度，无并发/自动重试/昂贵fallback。

## 十二字段决策记录

1. Issue ID：W1-5060-P1-ADMISSION-01。
2. 名称：查询Pilot合同已准备，科学及付费准入未闭合。
3. 阶段：Week1 / 5060 P1零付费准备。
4. OBSERVED_FACT：48tests与11命令检查通过、36世界设计无身份/规范化正文串味、无新索引或模型运行；
   SOURCE_DERIVED_FACT：5090安装/失败/NOT_RUN来自固定Git；Owner两个决定来自当前消息；
   INFERENCE：旧F5不能作新Query效果、36世界设计还不能证明足证；UNKNOWN：账号/精确token计数、T1可信根、评分/目标。
5. 约束：白名单/不触D2D3/不改GT、固定样本与生成器、原版/迁移分开、同权限强基线、累计预算及机制审批。
6. 现在处理原因：防止无效检索或不公平证据权限先产生付费结果。
7. 风险：索引/正文串味、答案泄漏、token截断、把库当论文复现、AI一致性当Gold、未知账号与收费、错误论文归因。
8. 选项A（推荐）：Owner审阅本候选合同，先授权闭合来源根/答案范围/目标与零费用真实检索预检；付费仍锁住。
   成本0API、可逆，缺点是需逐题裁决与资产pin；有利于可复现和后续正式实验。
   选项B：直接启动付费Pilot，不满足当前约束，不能执行；不存在因进度而自动豁免的选项。
9. LOCAL建议：交付本次准备，保持付费和方法门关闭，等待Owner明确下一批准项。
10. 理由/置信度：字节/引用/隔离工程高置信；语义正确性、方法缺口、生成安全收益未知。
11. 待Owner：B1库轨道命名/参数、18源共同背景与T1固定包权限、逐题评分与攻击目标、C3边界、下一阶段实际检索预检范围；
    首次B5冻结与D1-40保持以后单独审批，不在本轮申请替代批准。
12. 决定前允许：本轮证据保存、文档及本分支Git交付；禁止付费探测/Pilot、模型下载/Claim、B5/B6/D1-40和跨分支合并。

文档收口、run/hash与私有索引见[p1/evidence](p1/evidence/P1_RUN_MANIFEST.json)；完成推送后停止。

| 证据 | SHA256 |
|---|---|
| 待审查协议 | `6691273c5269ce52cb2c99629e3155daef38ebb36ccca01ae4402bc0cb22692c` |
| P1 Run Manifest | `a91721d9739d53092e022aa1abb3c9650540b8bc6cc135f83e89e785d2d3b2f6` |
| 世界设计索引canonical hash | `1e3e175685194b7c95ccc8ebdd59ec7188bcc26aa40fa2fe6e6c72176bb1a3bd` |
| 私有证据索引文件 | `4995030167c2e37c4174428bcfaa9776ab7dc55a185421e44e1dcab9067cf5d4` |
| Git外归档 | `87818359e8894eec302fa039107610434b7eaeec3ed348b4d1a11e23c83be745` |

world索引canonical hash采用UTF-8、排序键、无空白JSON的SHA256；其余表项为文件原始字节SHA256。
验证原始argv/cwd/stdout/stderr/exit及本地Query/答案/世界正文均留受控目录，不进入公开Git。
