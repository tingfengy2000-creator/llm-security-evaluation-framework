# 5060 Codex｜Owner18 S1-B Rule-V2（旧73开发）+ UIE 只读许可核验执行指令

你现在执行 Paper1 5060 的**受限开发任务**，不进入新科学试次。Owner明确批准仅限 Rule-V2 使用旧 S1 已暴露73条合成样本与本地普通单测；并行仅只读核实 UIE 官方许可与依赖。**没有批准新模型下载、安装、加载、推理或任何新独立测试。**

## 0. 前置恢复

唯一仓库 `tingfengy2000-creator/llm-security-evaluation-framework`；
唯一分支 `research/paper1-chinese-defense-5060`。
控制面核实的实验/设计 HEAD `ae9f978ea5eb739ec30a677618d17c0c126470f6`；请先读取远端最新值，不能假设该旧点仍是HEAD。
授权编号 `W1-OD-20261108-5060-S1B-RULEV2-DEV-18`，原件：
`docs/paper1/dual_machine/owner_approvals/W1_5060_S1B_RULEV2_DEV_AND_UIE_READONLY_AUTH_20261108.md`。
已批准但**尚未执行**本批，上一封存S1仍是 `S1_FAIL_STOP`。

先执行AGENTS.md的Context Recovery、git branch/HEAD/status/upstream/fast-forward检验、PO-MHEP、FORWARD_RISK_REVIEW、PAPER_RISK_REVIEW。工作树未知改动、冲突、未授权源或缺关键输入即STOP；不要reset/stash/force push。

必读：
- `docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1_INDEPENDENT_CHINESE_EXTRACTION_RESULT.md`
- `docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1_INDEPENDENT_CHINESE_EXTRACTION_MANIFEST.json`
- `docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_OWNER_ADMISSION_PACKET_20261108.md`
- `docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_LITERATURE_MODEL_RESOURCE_INDEPENDENT_VALIDATION_PROPOSAL_20261108.md`
- R1-06/R2、P0/M1/M2/M3冻结规范。

## 1. 数据与实验身份

旧S1：`W1-5060-S1-CHINESE-EXTRACTION-20261108-01`，原73验证 = 61不同语义案例+12显式/自然化从属配对视图，30完整正确、4错误、39 UNKNOWN；有答案命中31/61，错抽4/34，12应拒识中2错误。原S1 Run、源码 SHA `68d34a5d877206f4e6d7d9e2bdda16784145a76a`、Manifest、Gold及预测**只读保全**。
自本轮起，旧73在Rule-V2开发中被显式降级为 `EXPOSED_DEV_FIXTURES`，可以在已授权的私有受控目录下查看这些旧标签调试，但所有统计必须标 `DEVELOPMENT_REUSE / NOT_INDEPENDENT / NOT_HUMAN_GOLD`。不允许改原73样本/标签或只挑容易案例，不允许构建、打开或触碰未来100个不同语义新验证事实或20个从属配对视图，不可读取D1/D2/D3/5090任何隔离数据。

## 2. Rule-V2 最小实现

基于已公开文献技术而非重新发明算法；保留冻结Rule-V1原代码不动，新建隔离模块/配置和可追踪的`Rule-V2`身份。

采用5个可审计环节：
1. Query解析主体、属性、时间/版本/单位、适用范围与显式条件；UNKNOWN与歧义返回具体原因。
2. 原文候选抽取，保留**所有**可能与query相关的数字、比例、金额、日期、版本、名词候选及原文位置；不借助文本以外常识补值。
3. 候选关联主体、属性和作用域；多事实/同名异范围不能无因选最近或选最新。
4. 对否定、例外、生效期、跨条款与未证修订保持保守；仅原文出现的权威宣称不提升P0信任。
5. 通用确定性span/字符/UTF-8偏移与单位/日期/scope核验；证据不能唯一绑定，返回UNKNOWN并保留原因，而非伪造答案。

接口应可被未来 Rule-V1、UIE、Qwen-local 共用：(query, source_original, public_schema) -> candidate(s) + span(s) + scope + status/UNKNOWN + reason。不要把Gold或S1失败角色写入默认算法路径；开发期允许另线对照以定位失败。Rule-V2不执行M1/M2/M3完整防御、不重新检索和过滤、不执行新G3，不修改P0语义。

## 3. 开发范围与评价口径

仅运行旧73的**开发期**对照和新写普通无模型单测（synthetic unit fixtures 不计独立事实集）。至少对下列既知失败归因：query subject/attribute未识别13、scalar未抽到9、多事实消歧6、scope未匹配1；错抽scope/条件2、无证据误答2。必须保留无法修复/新引入副作用。

每个开发迭代保留源码hash、配置、输入hash、73全分母的预测/混淆/UNKNOWN数、错因、关键未证修订与跨scope安全断言、旧规则固定V1历史结果，不改Gold。可以迭代以完成开发；不能由开发指标宣布 S1-B PASS，不把旧73当未见数据。不得为了某个指标牺牲“不应答时不误答”。

报告完整 correct/wrong/UNKNOWN、value hit/answerable、wrong/decided、coverage/abstention、strict scope/span、自然化与显式配对、已知类别前后对比；任何旧73表现提升只是开发线索，不是论文主要效果。

## 4. UIE only read-only

继续核验固定 PaddleNLP `uie_nano_v1.1` 的权重/分词器许可、文件身份与发布者强哈希、不可变权重发行标识；核对Paddle CPU依赖 transitive lock（Python 3.12 / NumPy 2.x / Win x64）是否可用。只看官方静态README/license/metadata与合法公开来源，不下载权重/分词器实际文件、不pip install、不git clone新仓、不缓存模型或 wheel、不触模型API和在线count tokens。许可证无法明确闭合如实`UNKNOWN`；源码Apache-2.0不可替代BOS权重条款；MD5不能写成发行者 SHA256。可提出请求官方维护者澄清的精确问题，但未经Owner授权不代表用户联系第三方。

## 5. 严格禁止与终态

不下载/安装/加载/调用任何模型，包括已缓存未批准权重；不使用在线免费/商业LLM；0模型推理、0额外收费；不执行新独立S1-B科学测试，不偷建验证样本或自评分，不能解封UIE/Qwen Gate1/2/3；不碰旧B2/R2/108、D1、D2/D3、5090/Llama/Claims、S2-S5或主分支。C盘禁项目新可控存储，D/E保持安全余量与私有Gold/正文保密。

若旧73合规访问权限不清、需要新资产/安装/外部服务、版本/偏移失真、发生未知分支冲突或重大P0科学语义变更，立即`HUMAN_DECISION_REQUIRED / Auto Continue=NO`并保留日志。

## 6. 交付/STOP

一次开发任务完成后提供：
- 开发Run ID，建议 `W1-5060-S1B-RULEV2-DEV-20261108-01`（不得冒充正式独立实验）；
- Rule-V2源代码/测试/config/hash；原Rule-V1不可变断言；
- old73开发对照与所有失败/新误答，分母不变，所有迭代和QA日志；
- UIE官方许可/权重SHA与不可变revision/依赖锁现状（PASS或UNKNOWN）；
- API/下载/安装/模型加载/推理/费用均0的证据；
- 只读审计与PO-MHEP/Git治理收口，远端分支、SHA、测试报告；
- 下一次需Owner批准的模型资产、开发模型推理或新独立测试门。

完成后立刻 `RULE_V2_DEV_COMPLETED / S1B_INDEPENDENT_TEST_NOT_RUN / MODEL_ASSET_NOT_AUTHORIZED / S2_S5_LOCKED / AUTO_CONTINUE=NO` 并STOP。失败也如实归档。
