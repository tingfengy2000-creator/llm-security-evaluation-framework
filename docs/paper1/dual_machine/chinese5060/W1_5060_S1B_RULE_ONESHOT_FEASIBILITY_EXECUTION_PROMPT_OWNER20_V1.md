# 5060 Codex｜Owner20 S1-B Rule-V1/Rule-V2 单次冻结数据可行性对照（生效执行指令）

**执行授权：`W1-OD-20261110-5060-S1B-ONE-SHOT-20` / `OWNER_EXPLICITLY_APPROVED / ONE_SHOT_RULE_V1_V2_FEASIBILITY_ONLY`。**
这份文件已获Owner授权，允许在满足预检后**同一次任务内执行**双臂全量预测、封存、揭盲及统计，**不需要再申请前置技术性许可**，但若触发PO-MHEP重大异常必须立即停止。不要把“加快速度”理解成允许重复科学试次或扩大阶段。

## 0. 权威恢复

Repo：`tingfengy2000-creator/llm-security-evaluation-framework`；唯一分支 `research/paper1-chinese-defense-5060`。
正式 PO-MHEP 十二字段授权：
`docs/paper1/dual_machine/owner_approvals/W1_5060_S1B_RULE_ONESHOT_FEASIBILITY_AUTHORIZATION_20261110.md`
前置监督审查（仅作为风险与指标补充，不代替Owner20许可）：
`docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_FEASIBILITY_ONE_SHOT_SUPERVISOR_GATE_REVIEW_20261109.md`
必须核对`AGENTS.md`、context authority map、PO-MHEP、current work state、Owner Register、R1/R2、数据Seal Manifest、Experiment Master、git branch/upstream/HEAD/status/15 commits；新HEAD不得假设仍为之前数据提交。建立中文Context Recovery Report、FORWARD_RISK_REVIEW和PAPER_RISK_REVIEW。仅可在干净、可fast-forward、与远端一致的5060隔离工作树运行；未知修改不得reset/stash覆盖。

## 1. 不可更改的科学身份

数据准备Run：`W1-5060-S1B-FEAS-DATA-PREP-20261109-01`。
- 总数据seal SHA256：`531ac4e6421f6486b8165d443af2cf9d892a7bc3c740483950d03240d35a7c58`
- runtime INPUT：`bd2bc5e6586789070c20dde123bfe72843181aa861aca229fdb0c23091328dee`
- provisional Gold：`8f745f921424c6e61357ec19800bc4a1f198e92a26d36377a3a238d634598371`
- scoring protocol：`43d4d22770f5887058fabfc0162368e77cd36bd6c7d85d846417789515f5341e`
- data commit：`20402e94ed3da6be155a605daba272ec0a7c2cf1`
- 固定Rule-V1源：`68d34a5d877206f4e6d7d9e2bdda16784145a76a`
- 固定Rule-V2源：`da3cbd9f16ea70ae3ba0ef2aa2408227ecfc0b4f`
- 原主100事实（70 ANSWER、30 UNKNOWN），+20改写，仅用于配对；总运行120视图，不准改变Gold、查询或证据，**不准把120当成120个不同语义案例**。
- 只有当前已有本地规则Python环境；0新模型权重、0新依赖安装、0新网络服务/商业API/免费LLM调用。
- 新 Run ID 建议`W1-5060-S1B-RULE-ONESHOT-20261110-01`（需预留唯一并严格回写manifest），与原数据准备及旧73开发Run分离。

在D/E受控目录对原五档zip、数据成员与封存回执逐字节校验，必须校验Gold但**在role-free预测完成前算法/runner只能看到Hash，不得读取Gold字节**。校验需交由不会返回Gold内容的保管方程序执行。若技术隔离不足STOP，不能先打印Gold或在同进程读取Gold预检。

## 2. Stage P（工程预检，不消耗主新样本）

仅旧73已暴露数据和普通不计科学样本的单测，可实现公共adapter、no-label runner、独立Evaluator、sealed-output archiver及数据白名单。冻结源码 SHA/config/运行参数/出站守卫、同`id/query/evidence`输入和V1/V2 schema字段映射。任何算法接口无法一致比较需显式保守降级：缺span或scope时不能补Oracle、不能用Gold猜值，记ERROR/UNKNOWN/strict fail，保留原始字段。
预检`accepted_span_sets`的支持关系：集合之间OR，集合内部AND，证据window、绑定cue及跨段连接键都须被候选引文覆盖；不能通过把整段作为超宽span或拼写Gold答案获得优待。对已暴露数据上构建确定性跨度单测（包括合法同值多个span、不同scope同值、跨段支持、无span），两臂完全同判定。
预先生成release清单（RUN_SRC_SHA、ADAPTER_SHA、SCORER_SHA、INPUT_SHA、GOLD_SHA_HASH_ONLY、ENV_ID、参数/资源界限、角色隔离顺序），经脚本检查后Seal。预检任何阻断STOP向Owner报告，**不得在新120上试预测哪怕1条后再修补**。

## 3. Stage R（单次完整离线 role-free 预测）

当Stage P全部通过：同一原样输入120视图，固定顺序两臂各恰好运行一次（每臂120/120，ERROR保留于全分母），不联网、不重试、不更改任何数据/参数/阈值/模型版本。无论Rule-V2因无标题或scope失败都要真实保留。
在两臂完成后将逐视图源输出、规范化结果、失败、分母及SHA写入D/E受控私有归档。**两臂Role-free archive/receipt均封存且独立只读确认前，不得运行评价器或打开`PROVISIONAL_GOLD`**。
若出现数据/身份/进程阻断：STOP并保存原始失败日志，不启动第二次重跑。不可宣称“已执行但因小失败重试后通过”。

## 4. Stage E（封存后一次性只读揭盲与评分）

独立Evaluator只读取已Seal的两臂输出以及同一份已Seal的`PROVISIONAL_GOLD`和`SCORING_PROTOCOL`，不得调用模型/检索/更改adapter或Gold。
全量报告：100主案例的`correct/wrong/UNKNOWN/ERROR`，值命中/70，决定样本错抽/decided（点估计及95%Wilson）、wrong/100、coverage/abstention、30个应拒识误答、严格scope/version/value/span及多证据支持集、10类分层、文档标题头有无、4域/10来源家族、20改写的配对转移、最差类别、全部失败样本类别与不确定性。保留70主可回答中**预计21个无生成标题头**作为预注册压力测试；实际结果不得先验填写。
冻结决策门：值命中`>=63/70`、`wrong/decided <= 0.02`且decided>0，不允许all UNKNOWN。未证新版/跨scope误答=0只是观察值；是否恶化必须公开但不得擅增正式硬门。严禁将未知/拒识重标正确答案命中，不能把`Rule-V2`不支持span隐式算通过。结果状态仅`FEASIBILITY_PROVISIONAL_GO`、`FEASIBILITY_NO_GO`或证据无效`INCONCLUSIVE_STOP`。

所有Gold由Agent生成，数据作者与研发未独立，明确`AGENT_GENERATED_PROVISIONAL_FEASIBILITY / NOT_INDEPENDENT_AUTHOR / NOT_HUMAN_GOLD`，**即使GO也仅供选择路线，不表示完整VESA方法有效或论文实验成功**。D1仍`DEV_EXPOSED`；正式ASR和Answer Accuracy尚未测。

## 5. 绝对禁止、停止与归档

禁止用新集结果开发Rule-V3、选择子集、删除无标题项、后验改Gold/span/score、重新取样、主100第二次运行、跨分支执行、下载/安装/加载/调用任何未批模型、付费/免费在线LLM与其它外部API、5090 Claim/Llama2操作、读D2/D3/旧108或未来S3、重跑原R2/B2/生成108、开启S2–S5、合并主研究分支。
Stop条件：缺必要授权/封存材料、输入与私有证据哈希不符、模型源或adapter未冻结、Gold泄漏、角色盲输出不全且不可确证、失去可复算性、磁盘/许可证/网络新增风险、正式指标口径歧义或PO-MHEP新升级。立即`HUMAN_DECISION_REQUIRED / Auto Continue=NO`。

归档交付：完整运行命令+exit code+stdout/stderr、manifest与输入/模型/adapter/scorer/env SHA、私有证据归档 SHA、时间/资源/API下载费用账本、测试/ruff/mypy/secret scan、各分母完整指标、失败归因和GO/NO_GO、原Owner19数据与旧S1负结果的显式保全、Git治理与Tracker更新，原分支提交push并验证HEAD/upstream/remote一致，**之后停止**。
