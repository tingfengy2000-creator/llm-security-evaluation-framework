# 给 5060 Codex 的完整执行 Prompt｜Owner16 S1 独立中文事实抽取离线验证

你现在执行 Paper 1 中文检索后防御线的 **S1 独立中文事实抽取验证**，不要重新研究/修改已经冻结的主路线。Owner 已明确批准 **S1 ONLY**，未授权 S2–S5。

## 0. 任务与权威

仓库 `tingfengy2000-creator/llm-security-evaluation-framework`；唯一分支 `research/paper1-chinese-defense-5060`。
唯一授权 `W1-OD-20261108-5060-S1-OFFLINE-16`，文件：
`docs/paper1/dual_machine/owner_approvals/W1_5060_S1_INDEPENDENT_CHINESE_EXTRACTION_OFFLINE_AUTHORIZATION_20261108.md`。
此前 R2 Run `W1-5060-R2-FAIRCTRL-20261108-02`；结论 K1-C。
权威顺序按 `AGENTS.md`、PO-MHEP、Owner Decision、Current Work State、R1/R2 与冻结 S1 设计。先执行 `git fetch --prune --tags origin`、branch/HEAD/status/upstream/15 commits、Context Recovery Report；只在干净可快进的独立工作树上进行。任何漂移/未知修改 STOP，不能 stash/reset/force-push。

阅读：
- `docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/VESA_REVIEW_RESPONSE_P0_M1M2M3_S0S5_DESIGN_V1.md` 的 S1 章节
- `docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_R1_TRACKING_AMENDMENT_20261106.md` 的 R1-06
- `docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_R2_S0_CHECKPOINT_TEMPLATE_TFIDF_ROUTE_20261106.md`
- `docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_K1C_SUPERVISOR_ROUTE_RECOMMENDATION_20261108.md`

先完成 `FORWARD_RISK_REVIEW` 和 `PAPER_RISK_REVIEW`，用新任务 Run ID（建议 `W1-5060-S1-CHINESE-EXTRACTION-20261108-01`）；绝不复写 S0/R2/B2 的 Run Manifest 或原文。

## 1. 唯一研究问题

在与冻结 D1/D2/D3 完全隔离的独立自然中文样本中，验证抽取器是否准确从给定的 query + 正文提取：
- 主体、属性、目标答案值、单位；
- 年月/生效期/版本、条件/否定/例外、地域/机构等 scope；
- 可见原文 source span 与事实依据；
- 无足够依据时明确 UNKNOWN，绝不把假定的新版/自称权威当成已证事实。

本轮只研究**事实抽取器的可靠性**，不研究是否已实现 VESA-P0 的真实信任提升、不启动新的 RAGDefender 过滤、检索、生成或防御端到端比较。

## 2. 数据组织与信息隔离

- 至少60个用于验收的独立中文手写带标注实例，**不能**重复或改写 D1 12题、D2/D3、旧108、S0/R2、S3将来留出；不得以训练/测试泄漏伪造“独立”。
- 可自建额外 development fixtures，用于实现/单元调试；它们不得计入 ≥60 正式 S1 分母。
- 明确列出样本类别与数量，覆盖百分比/金额/年月/数量单位/非法日期、同名异主体、不同版本/生效时间、条件与否定例外、句内多事实、错误单位、未证伪造修订、跨scope 冲突、自然中文无固定答案模板、合法正文混网页导航/下载、真实无答案/UNKNOWN。自然化与显式模板配对必须保留对应关系和分层统计。
- 测试作者/标注者、算法开发端、Evaluator 职责逻辑分离：先由测试数据/标注端冻结实例与可见 source span、scope/Gold 和哈希；算法端只能拿 (query,evidence text) 及允许公开的schema，**不得读取 Gold、角色、target、旧生成输出及任何隐含答案文件**；Evaluator 仅在 role-free 预测不可变封存后比对。
- 如果不能由真正独立人类提供标注，允许离线构造自洽的合成开发门，但严格标记 `AI_AUTHORED / NOT_HUMAN_INDEPENDENT / SEALED_SYNTHETIC_DEVELOPMENT`，不许把Agent自填标注声称 Human Gold 或外部盲审。
- 所有原文、标注、逐样本预测与来源证据留 D/E 白名单；Git 只提交代码、schema、脱敏聚合、SHA和复现实验说明。无合法来源或数据权限时改用完全虚构的本地构造例，不伪造真实来源身份。

## 3. 抽取实现与错误口径

- 固定 S1 schema：query、evidence text、subject、attribute、value、unit、effective_from/to、condition、scope、negation/exception、source span 起止偏移及 UNKNOWN reason；索引偏移必须能映射原文本。对无法可靠定位的字段拒识而非乱指向。
- 开发端允许在 S1 **development fixtures** 上修改规则，必须记录每次代码 SHA、变更原因、前后错误、合成覆盖；不通过 D1 类别标签/旧R2效果调整规则，不改 P0/M1/M2/M3 科研语义。
- 对封存 ≥60 S1 验证集执行固定版本；一旦查看逐样本错误，验证集不再可视作未暴露 holdout，未来修订必须记录为开发再使用，不得删除原失败或只汇报最后一次。
- 每一条需分型：`CORRECT`、`INCORRECT`、`UNKNOWN`；错误至少细分：值/单位错抽、主体/属性错绑、时间/条件/版本scope错绑、source span错绑/找不到证据；独立记录缺失真值/应拒识与误答。
- 报告 `total/decided/correct/wrong/UNKNOWN`、`wrong/total`、`wrong/decided`、coverage/abstain 与自然化前后差异。正确率、错误率分母必须精确标注；UNKNOWN 不能记正确，也不能无解释从指标剔除。
- 分层、点估计和 95% Wilson 区间都输出；绝不把 60 条无错解释为总体错误率≤2% 的统计证明。尤其不得把“未知答案全部UNKNOWN”解释为准确率高。

## 4. S1 既有验收门和停止规则

沿用冻结 S1：
- ≥60 验证样本；
- 答案值抽取准确率 ≥90%；
- M1-safe 使用前 `wrong/decided <=2%` 点估计，且 `decided>0`，不得 all UNKNOWN；
- 误答 / 拒识分别报告 `wrong/total`、`wrong/decided`、coverage；
- source span 与版本/scope 错误单独报告，并给 Wilson 上界。

若准确率 definition 或应 UNKNOWN 样本如何算正确存在未冻结口径冲突，在报告中同时显示各口径和具体不确定性并按 PO-MHEP STOP，不能事后换分母制造 PASS。若任一硬门不达，报告 `S1_FAIL_STOP`，保留负结果；若独立标签/证据无法成立，报告 `S1_INSUFFICIENT_EVIDENCE_STOP`。即使 PASS，也只是 `S1_DEV_OFFLINE_GATE_PASS`，需要 Owner 再批准 S2，不是论文结论。

## 5. 资源、权限和停止

允许本地现有 Python/规则抽取代码、已有资源、可复现无标签 unit tests、私有 S1 synthetic packet 和离线 Evaluator。0商业 API、0免费在线 LLM、0模型/依赖下载、0外部搜索、0真实Qwen、0新向量检索、0付费、0 D2/D3/Reviewer/GT、0 old B2/R2 重跑或重写。C盘无新增项目可控文件，D/E保持资源安全余量。

5090 正等待 Meta Llama2 访问许可。**不得给5090任务、读取5090工作目录、下载Llama2、启动Claim1–3**。R1-10(B) S3构造方仍未指定，不得自行占用 S3 样本。

一旦发现数据/来源越权、Gold进入抽取器、需要安装/下载/联网、抽取定义未冻结、参数/证据身份无法复核或任何研究重大风险，立即 `HUMAN_DECISION_REQUIRED / Auto Continue=NO`，出12字段决策卡并封存已有状态，不要无限准备或静默绕开。

## 6. 验收、证据、提交

要求一次闭环交付（失败也要交）：
- S1 Run ID、任务/源码/配置哈希、验证数据与 Gold 独立锁、角色盲预测与评价双层封存；
- ≥60 真实分母、类别分层与自然化配对；
- correct/wrong/UNKNOWN、value/scope/span细项、`wrong/total`、`wrong/decided`、accuracy/coverage、Wilson CI；
- S1唯一状态 `PASS / FAIL / INSUFFICIENT`，以及不能宣称的外推/Gold/防御效果；
- failure analysis、修订日志、无标签静态测试、Ruff/MyPy/pytest/secret scan/Git-ignore、下载/API/费用皆0的准入证据；
- 按 AGENTS 的 DOCUMENTATION CLOSEOUT GATE 条件式同步 Current Work State、Project Master、Experiment Master、Execution Log、Human/Agent Ledger、Week1 Tracker；不改旧文档事实；
- 独立分支 commit + push、核 remote SHA 和工作树洁净后立即 STOP。

向 Owner 返回精简摘要，尤其回答：“S1 在自然中文中有多少可用 scope-bound 的事实？最严重的 3 类误差是什么？是否有足够理由继续 S2？”。不要自动开展 S2–S5。
