# Paper 1｜Week 1 Fast-Track C — Owner 十二字段正式授权

- 跨分支 Owner 授权 ID：`W1-OD-20261105-FAST-C-06`
- 日期：2026-11-05（Asia/Tokyo）
- 状态：`OWNER_EXPLICITLY_APPROVED / READ_ONLY_FAILURE_ATTRIBUTION_ONLY`
- 源：Owner 在当前 ChatGPT 项目监督会话的明确指令，本文件仅作脱敏授权转录，非原聊天字节或实验输出。
- 仅适用分支：`research/paper1-chinese-defense-5060`；原审批前远程 HEAD：`8d14dd180a121970ffb311a4176dca61336f91c2`。
- 已有实验：P2 `W1-5060-P2-20261104-T0-01`；Fast-Track B `W1-5060-FAST-B-20261105-PAIR01`；执行源码 SHA `17897075bfdbc325979b29e75b7209877bc5bebb`。
- 核验锚点：P2 T0 TopK seal `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`；PAIR01 过滤输出 seal `bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb`；独立开发评价 seal `0027a03c490f80d98327fbdd8f787830affde3bcfbf9e6c02bd805bf260c79a1`。原证据不可重写。
- 本次仅准许分析已经存在的**封存输出及批准的 D1 开发标签**。未产生新科学试次；未来数据与评价权限并未扩大。

## 1. Issue ID
`W1-OD-20261105-FAST-C-06`。这不是新编的分支全局 PODR 编号；5060 与 5090 存在历史 `PODR-154` 同号异义，引用时必须包含本 ID、branch、commit SHA。

## 2. Issue name
Fast-Track C：P2/PAIR01 已封存检索与 B1/B2 配对过滤输出的只读失败归因；Stage1/Stage2、频率同分、Poison 漏报、Clean/HN 误删、配对翻转分析；12题独立人工裁决交接包的资料整理。

## 3. Discovery stage/task
5060 Fast-Track B 已提交并停止。此处只批准 `ANALYSIS_OF_IMMUTABLE_D1_DEV_OUTPUTS`；不批准改方法、补试次或查询级生成评价。5090 RAGDefender Claim 工作线仍独立。

## 4. Facts / provenance / unknowns
- `OBSERVED_GIT`：5060 `8d14dd180a121970ffb311a4176dca61336f91c2` 的 P2/PAIR01 报告、manifest 和公开聚合已经在远程；原 seal SHA 如上。
- `SOURCE_DERIVED`：B1/B2 各完成 36/36；Poison 1/12→2/12（条件1/10→2/10），Clean FP 1/12→4/12（条件1/10→4/10），HN FP 2/12→2/12（条件2/9→2/9）；已召回候选 29/36，7 miss（Poison2、Clean2、HN3）；B1/B2 删除 chunk 78/180、81/180。
- `SOURCE_DERIVED`：Poison B2新增过滤2、反向恢复1；Clean新增误删4、反向恢复1；HN新增误删1、恢复1、共同误删1。每个成功召回候选本次只有1个chunk，不能推断多chunk残留消除。
- `OWNER_CONFIRMED`：当前指令明确批准只读归因与独立待审包整理、禁止重跑和新实验。
- `UNKNOWN`：Stage1与Stage2每项错误的充分因果解释是否可由旧profile判定；未标注18背景文档的负类真值；12题独立Human Gold、攻击target与C3边界；真实RAG targeted ASR、Answer Accuracy 和拒答率。

## 5. Affected governance
`AGENTS.md`、Context Authority Map、`project_owner_sovereignty_and_mandatory_escalation_principle.md`（PO-MHEP）、Owner Decision Register、当前工作状态、D1开发身份、P2与PAIR01冻结Run Manifest、输出seal和私有证据分层、Evaluator/GT Vault隔离、不可变历史与两机各自分支治理。

## 6. Why this decision now
观察到 B2 在小样本中文开发集上净增 Poison 过滤1、同时净增 Clean 误删3；在提议新方法或支付查询级评价前，先从封存输出区分**可观察机制、统计相关性、无法判定的因果解释**，并为独立人工裁决准备不泄漏候选标签的材料。

## 7. Downstream risks
标签/攻击目标泄露进 Retriever、Guard 或解释算法；错误把过滤行为/背景删除量等同正式ASR、背景FPR或语义意图；从结果反推修改题目/target；因缺旧trace就悄悄重新调用 defend/encoder；把同分、首调长尾与模型差异不经证据推断因果；基于结果挑选子集或调整 p/m/阈值；误删原始归档；写C盘；把D1探索升级为独立泛化或统计显著性。

## 8. Options/tradeoffs
- A【OWNER ACCEPTED】：在现有封存 P2/PAIR01 与旧只读profile 上做一次可重放的归因聚合与案例矩阵，准备独立盲审交接资料；不得开展新科学试次。新增商业API、模型/语料下载费=0，新增计算仅为文件读取、哈希核验、统计与脱敏归档，保留D/E资源配额与C盘禁写。可逆且不更改原数据。
- B【NOT SELECTED】：直接进入新的 B5/B6 或 Qwen 查询级 Pilot；有机会更快获得性能数值，但没有准确失败机制、Gold及预算审批，违反当前边界。
- C【NOT SELECTED】：不分析旧输出、直接等待独立人工结论；合规但不能缩小方法创新的可验证假设范围。

## 9. LOCAL recommendation
执行 A。采取 **Role-Free Analyst / Post-Seal Independent Evaluator / Blinded Adjudication Handoff** 的物理/进程与路径权限分离。能由旧trace证明的步骤给出哈希与原命令索引；不能证明则标 `UNRESOLVED`，不可为归因临时重跑科学路径。

## 10. Rationale and confidence
授权文字高确定性；P2/PAIR01 已存 Git 的聚合指标与封存hash高可追溯性；因果路径与背景标签没有充分证据时只能列假设与替代解释。12个事实组/36角色世界属于D1开发，不允许独立泛化或伪造显著性、ASR和QA结论。

## 11. Explicit Owner choices and unresolved gates
**准许**：
1. 5060 仅只读核验并分析 P2 与 PAIR01 现存封存文件：输入/输出/评价 seal、逐世界 private results、已有 profile、已有对象身份与统计字段；不得覆盖原字节。
2. 仅对**已有输出**作确定性重算/交叉表/差异分解，包括 Candidate Hit@5、B1/B2 配对反转、Stage1的已有n_adv估计、Stage2既有TF-IDF/频率分数与处理次序、tie/低index选择、Poison漏报与Clean/HN误删、candidate残留与chunk删除、不含主观GT的背景删除风险。只有旧trace字段足够时才可判断某个阶段对结果的必要条件；没有 trace 时写 `UNRESOLVED`，不能用重跑代替。
3. 继续保留原完整36世界（每类12）与召回条件性29世界（P10/C10/HN9），单列7 MISS；可按样本已封存身份输出仅存本地的行级差异与公开脱敏聚合，不得以结果筛样本或更换分母。
4. 可以**复用并整理**现有12题/38原子/16来源的盲审卡、来源、答案候选有效时间/条件、target证据空缺、C3需裁决项。交接给独立审阅者前须隔离检索/PAIR01结果、角色映射、旧预测和任何攻击目标猜测。Reviewer/GT Vault/D2/D3原始资产不得由本5060任务打开。
5. 可以新增**仅分析与治理类文件、无副作用本地统计程序或脚本**以重算旧输出，不可改原 guard/embedding/retrieval runtime/阈值/模型/候选/检索世界；不调用新的RAGDefender defend/encode/retrieve、LLM生成或已有科学脚本，亦不启动A/B对照重试。若需要科学路径调用，就STOP申请新授权。
6. 原始/private数据和新私人行级失败案例留D/E受控目录；新代码/日志/缓存/TEMP及归档不得新写C盘。保留原来源路径、文件SHA、读取日志与输出封存hash；完成本分支脱敏Git治理和状态收口后STOP。

**未批准**：任何重建索引、重检索、运行B0/B1/B2科学试次、修改参数/阈值/模型/样本、B3/B4生成、B5/B6设计实现及真实运行、商业API/付费、新下载、D1-40、D2/D3/Reviewer/GT Vault、T1/T2、独立Gold签署/target推断或C3评分、5090 Claim1–3、跨分支/主线合并。

## 12. Allowed/prohibited before next gate
允许新任务的有限只读证据分析、确定性统计、脱敏结果报告、12题未签独立盲审交接资料与文档/Git closeout；禁止任何新增科学试次、资产权限越界、参数调优与正式效果声明。发生缺少原始私有证据、seal/索引损坏、身份或访问权限不明、必须重跑才能解释、统计混淆或标签泄漏风险即 `STOP / HUMAN_DECISION_REQUIRED`，保留原证据并提交PO-MHEP十二字段异常报告。

## Exit / Deliverable gate
- `docs/paper1/dual_machine/chinese5060/W1_5060_FAST_C_READONLY_FAILURE_ATTRIBUTION_REPORT.md`：已审证据锚点、逐类别和配对翻转矩阵、Stage1/2 trace充分性、频率同分与可识别性、HN合法历史与Clean误删风险、Poison保留风险、confounder及`UNRESOLVED`。
- `docs/paper1/dual_machine/chinese5060/fast_c/` 下脱敏机器可读统计、旧输出 SHA 验证收据、执行/文件打开清单、`FAILURES_AND_LIMITS.json`、`ADJUDICATION_HANDOFF_INDEX.json`、Run/Analysis Manifest 与私有归档 SHA、完整分母复算校验。
- 检查适用测试、Ruff/MyPy（若新统计代码）、最小权限/脱敏、文档链接/来源、Git工作树及远程一致性，完成 AGENTS/PO-MHEP 必要closeout，仅本5060分支commit/push，报告最终完整SHA并STOP。
- 成功状态只可为 `FAST_C_READONLY_DIAGNOSTIC_COMPLETE`；若原证据不足则 `PARTIAL_DIAGNOSTIC_UNRESOLVED`；均不能自动升级为方法创新、独立Gold或论文正式成绩。
