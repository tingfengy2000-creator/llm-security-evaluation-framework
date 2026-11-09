# Paper 1｜Week 1 双机 Tracker

**更新于 2026-11-09 JST · 版本 13 · 维护位置 `research/paper1-chinese-defense-5060`。**

## 2026-11-09｜5060 Owner19 可行性数据已封存，评价须另批

`FEAS_DATA_READY / PROVISIONAL_GOLD / EVALUATION_NOT_RUN / S2_S5_LOCKED / AUTO_CONTINUE=NO`。100 个全新虚构主案例（70 可答、30 应 UNKNOWN），另有 20 条从属问句改写。证据跨度、暂定标签、真值与配对、输入及协议已分件封存。标签是同一 Agent 的暂定标注，Human Gold 0。

Run `W1-5060-S1B-FEAS-DATA-PREP-20261109-01`，总封存 SHA256 `531ac4e6421f6486b8165d443af2cf9d892a7bc3c740483950d03240d35a7c58`。

Rule-V1/V2 新集零预测、零评分。D1 仅沿用历史开发诊断，CMRC2018 仅核元数据。模型下载／加载／推理和模型 API 调用为 0。下一门为 Owner 审批一次性规则可行性评价；正式 ASR/Accuracy 未测。

[结果与下一审批卡](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_FEASIBILITY_DATA_PREP_RESULT.md) · [脱敏 Manifest](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_FEASIBILITY_DATA_PREP_MANIFEST.json)

本条仅更新 5060，5090 保留上次已核快照。

## 2026-11-09｜Owner19 数据封存审查：一次性规则评价待新Owner明确批准

监督端核实 5060 数据提交 `20402e94ed3da6be155a605daba272ec0a7c2cf1` 与远端一致；报告100个主语义案例（70可答、30应拒识）、20从属问句、4域/10家族，角色盲输入/暂定Gold/source truth/配对/评分协议分件封存，seal SHA `531ac4e6421f6486b8165d443af2cf9d892a7bc3c740483950d03240d35a7c58`；实际 Rule-V1/V2 新样本预测/评分仍为0。来源同Agent合成，`NOT_INDEPENDENT_AUTHOR`，Human Gold0；D1/旧73/CMRC未纳入主分母。

公开源码显示30/100不带标题头，其中21/70可回答例不带标题头；Rule-V2使用`《...》`提取主体，缺可识别标题时易拒识，属于**预注册压力测试与性能风险**而非已知实测错误。另有多span支持集的共同Adapter输出与评分一致性问题，必须在**仅旧开发样本或普通unit fixture**中完成静态预检，严禁用新120例试预测/调参。

[监督Gate复核](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_FEASIBILITY_ONE_SHOT_SUPERVISOR_GATE_REVIEW_20261109.md)；[一次性执行Prompt草案（Owner未批不得运行）](chinese5060/W1_5060_S1B_RULE_ONESHOT_FEASIBILITY_PROMPT_DRAFT_OWNER_APPROVAL_REQUIRED.md)。
当前`DATA_PREP_COMPLETE / ONE_SHOT_OWNER_APPROVAL_REQUIRED / NO_NEW_MODEL_OR_API / S2_S5_LOCKED / AUTO_CONTINUE=NO`。该监督记录不是Owner20决定；5090仍无新Claim许可。

## 2026-11-09｜Owner19：规则先行可行性数据准备获批，测试仍须另批

`W1-OD-20261109-5060-S1B-FEAS-DATA-19`。Owner明确选路线A快速验证规则，暂不消耗人工标注成本：允许D1只读开发回归，公开CMRC2018在许可证/固定来源/大小/哈希门下作为补充，主批准备100个新生成的不同语义中文事实/拒识案例（建议70/30）+20从属改写视图。Source-truth在先，文本/问法/accepted span随后，私有输入/暂定Gold隔离封存；AI标签=`PROVISIONAL_NOT_HUMAN_GOLD`，若同一Codex生成，则`NOT_INDEPENDENT_AUTHOR`。D1/旧73绝不能算独立100，CMRC缺版本/scope标注不能冒用VESA人工Gold。

Owner19仅放行**数据准备与预注册封存**；新数据上的Rule-V1/Rule-V2一次性预测/揭盲/评分仍要另批Owner批准。新模型下载/推理、额外LLM API、D2/D3、正式HumanGold、S2–S5、5090 Claims仍禁止。授权时数据准备`APPROVED_NOT_RUN`，新规则性能`NOT_MEASURED`，旧S1 FAIL/R2 K1-C均不变。

[Owner19正式授权](owner_approvals/W1_5060_S1B_FEASIBILITY_DATA_PREP_AUTHORIZATION_20261109.md) · [可直接执行的Codex指令](chinese5060/W1_5060_S1B_FEASIBILITY_DATA_PREP_EXECUTION_PROMPT_V1.md)。

## 2026-11-09｜Owner18 Rule-V2 完成后的监督评审（只读评价，非新授权）

监督端已核验远端实验HEAD `33d67cfbdbc93b90bdcfa27241be6539f28c3f14` 及完整Run Manifest。旧73已暴露开发样本上的V2最终值命中59/61、已决定错抽1/59、应拒识误答0/12，保留同句等价值来源span错误1条、应答却UNKNOWN2条。三轮均留存，旧S1 FAIL不变。模型资产/推理/新独立验证仍未批准；UIE许可和环境锁阻断。对原S1脚本与新Rule-V2源码抽查确认受限字段模式与来源span选择，因此不能推断开放域中文泛化或RAG端到端污染防御成功。

建议Owner在 `A` Rule-V1/V2先行独立验证（需后续另立不复用的多模型公平holdout）与 `B` 等待UIE/Qwen准入后统一四臂盲评之间做决定；任一都需Owner另批独立Gold保管/审阅与一次性评价，不能据本条执行。S2–S5、5090 Claim继续未授权。[完整监督复核](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_RULEV2_SUPERVISOR_REVIEW_20261109.md)。

## 2026-11-09｜5060 Owner18 旧73开发完成，后续门关闭

`RULE_V2_DEV_COMPLETED / S1B_INDEPENDENT_TEST_NOT_RUN / MODEL_ASSET_NOT_AUTHORIZED / S2_S5_LOCKED / AUTO_CONTINUE=NO`。Owner18 批准的三轮旧73开发及 UIE 官方材料只读审计已完成。最终 58 正确、1 错误、14 UNKNOWN（73 条），值命中 59/61，决定后错抽 1/59，应拒识误答 0/12。旧 Rule-V1、S1 失败、R2 K1-C 保留。Human Gold 0，正式 ASR/Accuracy 未测。

最终 Run `W1-5060-S1B-RULEV2-DEV-20261109-03`，执行 SHA `da3cbd9f16ea70ae3ba0ef2aa2408227ecfc0b4f`，私有 Run Manifest SHA256 `c8e6258e73cd6076e1ea25b3cdd35c0c68167d5e44122c1725da260f359d09ee`。

UIE 权重/分词器条款、不可变身份、发布者 SHA256 和 Windows CPU 依赖锁待证。模型资产、推理和独立验证均须另批。新增模型下载、安装、加载、推理、API 与费用为 0。

[结果与失败](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_RULEV2_OLD73_DEV_UIE_READONLY_RESULT.md) · [证据清单](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_RULEV2_OLD73_DEV_MANIFEST.json)

此条仅更新 5060。5090 保留上次已核快照。

## 2026-11-08｜Owner18：仅 Rule-V2 旧73开发 + UIE官方材料只读核查

Owner `W1-OD-20261108-5060-S1B-RULEV2-DEV-18` 明确放行5060在原独立分支使用已暴露的73条S1合成案例与普通本地unit fixtures开发/调试Rule-V2，保留所有迭代、负结果、错抽与原版Rule-V1封存；可以只读核实官方UIE权重/分词器条款、不可变revision/发布者强身份和CPU依赖。不授权模型下载、依赖安装、模型加载/推理、任何新模型调用、S1-B独立验证数据的构造/打开/评价或S2–S5。旧S1 `S1_FAIL_STOP`，原R2 K1-C、HumanGold0、正式ASR/Accuracy未测全部不变。5090仍等待Meta Llama2许可，Claim1–3未运行。

**授权登记时状态：`RULE_V2_DEV_APPROVED_NOT_RUN / UIE_READONLY_APPROVED / MODEL_ASSET_AND_INFERENCE_NOT_AUTHORIZED / NEW_VALIDATION_NOT_AUTHORIZED / Auto Continue=NO`**。新Rule-V2数据与性能以未来真实Run Manifest为准，不得将此批准写成实验完成。

[Owner18十二字段授权](owner_approvals/W1_5060_S1B_RULEV2_DEV_AND_UIE_READONLY_AUTH_20261108.md) · [5060执行Prompt](chinese5060/W1_5060_S1B_RULEV2_OLD73_DEV_UIE_READONLY_EXECUTION_PROMPT_V1.md)。

## 2026-11-08｜5060 S1-B 只读审批包完成

`S1B_DESIGN_ONLY / MODEL_DOWNLOAD_NOT_AUTHORIZED / MODEL_INFERENCE_NOT_AUTHORIZED / VALIDATION_NOT_AUTHORIZED / S2_S5_LOCKED`。Owner B 只读审批包已完成，UIE Nano 权重条款和强身份待核，Qwen2.5-1.5B 已核固定 revision 与权重许可。独立验证保管人未指定。新增模型、推理、下载、安装、科学试次和费用均为 0。Auto Continue = NO。

[Owner 审批包](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_OWNER_ADMISSION_PACKET_20261108.md)。SHA256 `f3204df649a34f500cd7ad751f0e4952a595879eb79b2315e3b8b19fd4b5b9c7`。

## 2026-11-08｜S1-B 选择 B：文献复用 + 规则/本地模型对照（设计而非实验许可）

Owner `W1-OD-20261108-5060-S1B-B-DESIGN-17` 确定采用规则与本地开源模型辅助抽取的**研究设计**，特别要求借鉴RAGDefender及相关论文。已拟定`Rule-V1`（旧锁定）/`Rule-V2`（开发）/PaddleNLP UIE轻量中文候选/Qwen2.5-1.5B-Instruct候选；S1-B仍须分别经过模型资产、离线开发推理、独立验证三个新的Owner许可门。资源/许可/具体revision目前待核，不能默认批准。**新增模型下载=0，新增模型调用=0，S1-B科学试次=NOT_RUN**。旧S1 `S1_FAIL_STOP`，S2–S5仍锁。5090仍在Meta Llama2访问审批等待中，Claim1–3未运行。

[PO-MHEP设计提案](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_LITERATURE_MODEL_RESOURCE_INDEPENDENT_VALIDATION_PROPOSAL_20261108.md) · [仅设计核验执行Prompt](chinese5060/W1_5060_S1B_LITERATURE_MODEL_ADMISSION_DESIGN_ONLY_PROMPT_V1.md)。

## W1-5060-S1-CHINESE-EXTRACTION-20261108-01 — S1 封存失败与停止

Owner16 S1 单次封存验证结束，S1_FAIL_STOP。73 条合成样本，30 正确、4 错误、39 UNKNOWN；答案值 31/61、已决定错抽 4/34。自然中文可用 scope-bound 事实 25/49。模型、API、下载与费用为 0。Human Gold 0，正式 ASR/Accuracy 未测。S2–S5 未授权，Auto Continue = NO。

[S1 结果与证据](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1_INDEPENDENT_CHINESE_EXTRACTION_RESULT.md)。


当前研究状态为 **5060 S1 未通过并停止，S2–S5 未授权**。5090 已完成离线 Smoke 和非 Llama 资产下载，Claim 1–3 均未运行。Paper 1 正式实验仍未启动。

旧名 `PAPER1_WEEK1_TRACKER_INIT` 可在旧对话中定位到一次提及。2026-11-06 检查 GitHub 的 9 条公开分支、1 个标签及其可达文件历史，未找到对应文件，原稿的仓库路径、最后修改时间及全文均为 **UNKNOWN**。本页是从已提交证据建立的第一个可维护版本。

## 2026-11-08 5060 R2 实测收口

本批仅为 D1 开发诊断。高置信模板 6/180、3/36 世界，蒙版对两个分词臂均为零变化。char2 使 Clean 误删 4/10→5/10、HN 隔离 2/9→4/9、Poison 删除 2/10→4/10。可比被删候选 0。S1–S5 未放行。

[四臂结果与封存证据](chinese5060/vesa_guard_reviewer_replan/W1_5060_R2_FAIR_CONTROL_RESULT.md)。

## 2026-11-08 历史授权：5060 S1 获批、5090 Llama2 等待

Owner `W1-OD-20261108-5060-S1-OFFLINE-16` 已授予5060唯一有界新任务：S1 ≥60例独立中文可见证据事实抽取离线验证（D1/D2/D3/旧108隔离），原错抽率、自然化/span/scope/Wilson门不变，0新下载/0联网/0商业API。**S1 APPROVED_NOT_RUN**，未有S1结果、Run Manifest或通过结论。S2–S5仍锁，R1-10(B)独立S3构造方未定。

5090远端 `dbd91f3667964baca69aeb82a6292c4fe193c965` 未变。Meta Llama2访问 `APPLICATION_SUBMITTED / APPROVAL_UNVERIFIED`，模型 `NOT_DOWNLOADED`、Claim1–3 `NOT_RUN`。不能据申请状态推定已获许可或暗示模型下载。

[Owner16授权](owner_approvals/W1_5060_S1_INDEPENDENT_CHINESE_EXTRACTION_OFFLINE_AUTHORIZATION_20261108.md) · [完整Codex Prompt](chinese5060/W1_5060_S1_INDEPENDENT_CHINESE_EXTRACTION_EXECUTION_PROMPT_V1.md)。

## 2026-11-08 R2 完成后的监督核验与下一审批门

5060 最新已封存 R2 Run `W1-5060-R2-FAIRCTRL-20261108-02`、结果提交 `5968369eaa1b3f8d1af2d9262ef5f3f145c4a83c`。36 世界四臂完成并复算，历史 B2 deleted 81/180、Poison 2/10、Clean 4/10、HN 2/9；char2 deleted 112/180、Poison 4/10、Clean 5/10、HN 4/9；网页模板高置信 6/180、mask 删除差异 0/36。既有抽取器可比较的被删候选 0，可信来源锚 0/180。预注册 `K1-C / INSUFFICIENT_OR_MIXED` 接受为该开发任务的路线分支，S1–S4 仍 NOT_RUN，S5 NOT_AUTHORIZED。5090 Claim1–3 未运行。

控制面 2026-11-08 建议：停止在旧 D1 上后验微调 tokenizer、mask、阈值和 VESA 规则，保留 D1_DEV_EXPOSED；若 Owner 新批准，**先 S1 ≥60 个独立自然中文抽取/作用域测试**核准可信抽取门，再按既有 R1/R2 预注册 S2 A–I、H4+1/H5+0 和可信锚有/无层推进。S3 独立方、S4、S5 均需新 Owner 授权。

[正式监督建议](chinese5060/vesa_guard_reviewer_replan/W1_5060_K1C_SUPERVISOR_ROUTE_RECOMMENDATION_20261108.md)，状态 `SUPERVISOR_RECOMMENDATION / PENDING_OWNER_CONFIRMATION`，**不是新执行批准**；不得据此打开 S1/S2/S3/S4/S5。

## 2026-11-08 控制面恢复与 R2 放行

GitHub 远端实查确认：交接包记录的 5060 HEAD `533a6efed519f9251f4b4848306e232c9710a497` 与检查时远端完全一致；5090 HEAD `dbd91f3667964baca69aeb82a6292c4fe193c965` 亦完全一致，说明新会话恢复前没有遗漏的远端实验提交。随后控制面仅写入治理授权，不伪造实验结果。Owner 本轮 `W1-OD-20261108-5060-R2-OFFLINE-15` 已释放有界 R2 离线任务：`S0-TEMPLATE-COVERAGE_READONLY` + `B2_RAW / RD_ZH_ONLY / RD_TEMPLATE_ONLY / RD_ZH_TEMPLATE` 四臂，并批准 R1-10(A) 仅使用历史 B2 固定 revision 的本地已缓存 encoder。网页模板 mask 只可作用于 Stage1 lexical view；原 TopK、原文、embedding/Stage2、生成上下文、参数和历史结果保持不变。role-free 结果须先封存，再独立揭盲。

在本页第 2 版记录的控制面放行时，**尚无新的模板覆盖计数、四臂结果或 K1 判定**，所以这些仍为 `NOT_RUN / NOT_MEASURED`。R1-10(B)、S1–S5、5090 Claim1–3、D2/D3、正式测试、商业/免费在线模型调用及主线合并均未放行。完成本批后必须按已预注册 K1-A/B/C 选择路线并 STOP 返回 Owner。

[2026-11-08 PO-MHEP 授权](owner_approvals/W1_5060_R2_OFFLINE_FAIR_CONTROL_AUTHORIZATION_20261108.md)。

## 双机 Git 快照

| 工作线 | 分支与本次整理前的远端 HEAD | 该提交时间（JST） | 机器端观测 |
| --- | --- | --- | --- |
| 5060 Codex · 中文检索后防御 | `research/paper1-chinese-defense-5060` · 2026-11-08 恢复前远端核验 `533a6efed519f9251f4b4848306e232c9710a497`；随后仅新增治理授权提交 | 2026-11-08 | R2 有界离线任务已放行；机器本地 HEAD、未提交改动和实时进程仍 UNKNOWN，实验结果须以之后 Run Manifest 为准。 |
| 5090 Cursor · RAGDefender 复现 | `research/paper1-ragdefender-repro-5090` · [dbd91f3667964baca69aeb82a6292c4fe193c965](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/commit/dbd91f3667964baca69aeb82a6292c4fe193c965) | 2026-11-06 02:58:38 | Git 下载清单可查，机器本地 HEAD、工作树及实时进程为 UNKNOWN。 |

分支 HEAD、控制合同和实验执行 SHA 分开记录。5060 S0 证据收口提交为 [25936c71f96d775cca9a7603d27164e952f3a0af](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/commit/25936c71f96d775cca9a7603d27164e952f3a0af)，R1 追加只读核验的控制提交为 [9bd8e29](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/commit/9bd8e29d49b774add5eafb700077e1750d41f309)。RAGDefender 固定上游为 [ba2a17e](https://github.com/SecAI-Lab/RAGDefender/commit/ba2a17efba165d45409114df2d70b030ade1e1b8)。

## 5060 已封存结果

| 项目 | 状态与结果 | 证据 |
| --- | --- | --- |
| D1 Pilot12 检索 | **VERIFIED** · 12 个相关事实组、36 个独立建索引的世界，每世界 1 个候选和 18 个背景文档，TopK5 共 180 片段。候选 hit@5 为 29/36，Poison 10/12、Clean 10/12、HN 9/12。7 次漏召回另计。 | [S0 报告](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_SUMMARY.md) |
| B1/B2 离线过滤 | **VERIFIED** · 各 36/36 世界。B1/B2 总删片段 78/180、81/180。以已召回候选为分母，Poison 删除 1/10、2/10，Clean 误删 1/10、4/10，HN 隔离均为 2/9。B2 仍保留 8/10 个已召回 Poison 候选。 | [S0 脱敏证据索引](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_EVIDENCE_INDEX.json) |
| G0/G1/G2 真实 Qwen | **VERIFIED** · `OWNER12_LIVE_108` 108 次请求成功，0 重试。三臂回答分别 15/36、13/36、11/36，拒答分别 21/36、23/36、25/36。输入/输出 Token 合计 44,426/5,154。CNY 0.130084 为公开费率估算，实扣为 UNKNOWN。 | [Owner12 运行结果](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/c6e36685cd948700f2d65e53031f82d8d13d2f51/docs/paper1/dual_machine/chinese5060/pilot_rapid_live/RAPID_LIVE_OWNER12_EXECUTION_RESULT.md) |
| 回答与拒答暂定评价 | **VERIFIED / PROVISIONAL** · 18 格拒答暂定合理，另 51 格拒答和 39 份回答的整体判断未决。Human Gold = 0，正式 Targeted ASR、Answer Accuracy 与 C3 均未测。 | [暂定评价](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/59ceb4ff2267299aa7ed1c6fb0819f952098fcd5/docs/paper1/dual_machine/chinese5060/pilot_rapid_live/PILOT12_D1_AI_PROVISIONAL_EFFECT_REPORT.md) |
| VESA v0.1 / v0.2 | **VERIFIED · 零变化** · 两版均 0/36 上下文改变，G3 与 G2 请求体逐字节一致，0 恢复、0 新 Qwen、G3 未运行。v0.2 识别到 24/36 个查询世界、102/180 个片段，49/180 个片段抽到具体值。 | [v0.1 结果](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/bfcfaa6490de96b97b12b3304297049dfa627910/docs/paper1/dual_machine/chinese5060/vesa_guard_v01/VESA_V01_OWNER13_RESULT.md) · [v0.2 结果](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/8db8d9f8b48f86dae9f8f9211e1092fbe4ae534d/docs/paper1/dual_machine/chinese5060/vesa_guard_v02/VESA_V02_OWNER14_RESULT.md) |

D1 是 `D1_DEV_EXPOSED`。本页 Pilot12 的 12 组、36 世界与 D1 开发范围的 40 组、120 候选分别计数。D2/D3、独立留出、答案与攻击目标留在各自授权和隔离边界内。上下文变化、候选过滤和回答/拒答计数分别记录。

## 5060 评审、S0 与放行门

S0 run 为 `W1-5060-REVIEWER-REPLAN-S0-20261106-01`，状态 **S0_COMPLETE / OWNER_CHECKPOINT_PENDING**。零新编码、零新检索、零模型调用、零 API 费用。[S0 报告](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_SUMMARY.md) · [S0 脱敏证据索引](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_EVIDENCE_INDEX.json)。

| 评审 | 本次核验状态 |
| --- | --- |
| R1-01 | **VERIFIED，静态完成**。RD-zh 只将 Stage 1 TF-IDF 改为字符二元组，`stop_words=None`。4 项定向单测通过，真实 D1 编码和过滤均 **NOT_RUN**。历史 B2 的 TF-IDF 仍沿用英文词规则和停用词。 |
| R1-02 | **VERIFIED**。旧 `n_tfidf` 36/36 一致，12/36 世界进入大簇分支。两次本地 top5 重放相同，旧记录未存逐词清单。分词造成误删的因果效应尚待反事实对照。 |
| R1-03 | **VERIFIED**。旧抽取器在 B2 被删的 81 片段中抽出 25 个具体值，0/81 与查询范围绑定，81/81 同值/异值判断为 UNKNOWN。保留集合中 1/36 世界有同范围唯一值，独立可信来源锚 0/180。以上按冻结输入及现有抽取器口径统计。 |
| R1-04 | **DESIGN / NOT_RUN**。M1-safe 为探索臂，保留重复同值片段可能提高错值采纳的残余风险。 |
| R1-05 | **DESIGN / NOT_RUN**。M2-detect 与 M2-vote 分臂，后者需要可验证的攻击者控制上界，多数与全毒场景单列。 |
| R1-06 | **DESIGN / NOT_RUN**。S1 独立记录错抽的两个分母、UNKNOWN、错因和区间。 |
| R1-07 | **DESIGN / NOT_RUN**。S2/S3 加入合法共享法规引用场景 I，保留 H 的 4 毒 1 净、5 毒两个变体。 |
| R1-08 | **VERIFIED**。72/72 个世界×B1/B2 臂的历史 Stage 2 计数和索引对齐修复后逻辑，实际余弦先做 L2 归一化，当前无 Stage 2 归一化修正臂。 |
| R1-09 | **HARD_STOP**。S0 已封存，S1–S4 **NOT_RUN**，S5 **NOT_AUTHORIZED**，Auto Continue = NO。 |
| R1-10 | **OWNER_DECISION_REQUIRED**。A 为 36 世界、180 片段的缓存编码器及 RD-zh 离线实跑权限，B 为 S3 独立造题与保管方。 |

R1 源附件由 Owner 提供，公开记录含原件摘要与 SHA-256。[R1 修订合同](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/fbb176f6aa232212a44d336ecb037c39b1220cd4/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_R1_TRACKING_AMENDMENT_20261106.md)。

**S4 证据门（INFERRED）**。冻结输入可信锚 0/180。按严格 P0 和原 B2，Clean 误删下界为 4/10，原门要求 <4/10，故当前输入标记 `S4_FAIL_EVIDENCE_BOUNDARY`，S4 本身仍是 **NOT_RUN**。公平臂出结果后按各臂重新计算。Poison 保留 ≤8/10 是原 D1 开发不退化门。[S0 报告](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_SUMMARY.md)。

**R2（历史预注册，实测见页首）**。评审观察的约 100/189 来自上游证据，D1 TopK180 的网页模板覆盖率为 **UNKNOWN**。下一项诊断限于冻结 TopK 的只读覆盖统计。已预注册 `B2_RAW`、`RD_ZH_ONLY`、`RD_TEMPLATE_ONLY`、`RD_ZH_TEMPLATE` 四臂，控制 Stage 1 分词与词面模板遮蔽，固定原 TopK、向量、Stage 2 和生成正文。四臂对照未实跑。K1 路线选择待证据，M2 与 X-MADAM-RAG 的重叠已登记。[R2 预注册与路线决策](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/1499561c8091fec1aaa042b81b9168ee63ff908d/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_R2_S0_CHECKPOINT_TEMPLATE_TFIDF_ROUTE_20261106.md)。

## 5090 原论文复现

| 项目 | 级别与状态 | 证据 |
| --- | --- | --- |
| 上游审计、环境、离线检查 | **VERIFIED · SMOKE / ALGORITHM_CHECK**。官方环境在 RTX 5090 的 CUDA 内核存在兼容问题，独立兼容环境的最小 CUDA 检查通过。 | [离线 Smoke 与资源门](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/5def0ff/docs/paper1/dual_machine/repro5090/W1_5090_OFFLINE_SMOKE_AND_RESOURCE_GATE.md) |
| 冻结非 Llama 资产 | **VERIFIED（仓库下载收据）**。Vicuna、Contriever、paraphrase-MiniLM 与 NQ、HotpotQA、MS MARCO 已下载。Llama 2 7B chat 未下载，本批模型加载 0、付费 API 0。 | [5090 下载记录](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/dbd91f3667964baca69aeb82a6292c4fe193c965/docs/paper1/dual_machine/repro5090/official_asset_gate/W1_5090_NON_LLAMA_ASSET_DOWNLOAD.md) · [下载清单](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/dbd91f3667964baca69aeb82a6292c4fe193c965/docs/paper1/dual_machine/repro5090/official_asset_gate/NON_LLAMA_DOWNLOAD_MANIFEST.json) |
| Claim 1 PoisonedRAG、Claim 2 Tan et al.、Claim 3 GARAG | 三条均 **NOT_RUN**。无防御/有防御 Targeted ASR 与 QA Accuracy 均 **NOT_MEASURED**。 | [下载清单](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/dbd91f3667964baca69aeb82a6292c4fe193c965/docs/paper1/dual_machine/repro5090/official_asset_gate/NON_LLAMA_DOWNLOAD_MANIFEST.json) |

## Owner 待决

| 决策 | 当前状态与前置 |
| --- | --- |
| 5060 · `S0_CHECKPOINT_RELEASE` | **待放行**。先确认追加只读的 D1 TopK 模板覆盖与四臂计划。进入 S1 需 Owner 显式放行。 |
| 5060 · R1-10(A) | **待授权**。是否准许仅用冻结缓存编码器对原 36 世界、180 片段做离线公平对照。限制为零下载、零新检索、零商业 API，历史 B2 证据原样保存。 |
| 5060 · R1-10(B) | **待指定**。选择独立于 5060 方法开发方的 S3 构造与保管人。任何跨机委派须单独授权。 |
| D1 定位与人工裁决 | **待证据/安排**。公平臂、可作用池和可信来源证据进入 K1 决策。独立人工审阅尚待安排，Human Gold 仍为 0。 |
| 5090 · 后续批次 | **待授权**。Llama 2 获取状态和下载、单格、Claim 正式运行分别核验与批准。 |
| S5 与投稿目标 | S5 保持 **NOT_AUTHORIZED**，须前序门闭合后再单独确认模型、外传及预算。投稿场次与年份待 Owner 确定。 |

5060 放行与角色隔离依据 [Owner 决策登记](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/fa70d97f86d0bf21364907e15447ced80f0e284e/docs/governance/project_owner_decision_register.md)、[5060 动态状态](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/fa70d97f86d0bf21364907e15447ced80f0e284e/docs/governance/current_work_state.md)、[R2 检查点](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/1499561c8091fec1aaa042b81b9168ee63ff908d/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_R2_S0_CHECKPOINT_TEMPLATE_TFIDF_ROUTE_20261106.md)。5090 批次依据 [5090 分批审批包](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/dbd91f3667964baca69aeb82a6292c4fe193c965/docs/paper1/dual_machine/repro5090/official_asset_gate/BATCHED_REPRO_OWNER_APPROVAL_PACK.md) 和最新下载清单。

## 更新规范

1. **事件触发维护。** 每次两机推送新证据、Run 完成/失败/零变化、评审修订或 Owner 改门后，负责更新的控制端先核验双方远端 HEAD，再在本文件更新受影响条目并追加下面的变更记录。无新证据时保留上一已核状态与时间，机器本地状态记 UNKNOWN。
2. **每条带证据。** 记录 JST 时间、分支、远端 HEAD、合同/执行 SHA、Run ID、阶段和分母。证据链接固定到提交。优先核对 Run Manifest、脱敏证据索引及封存汇总，再核对 Owner 决策和动态状态。`VERIFIED` 表示仓库或可访问证据已核，注明证据层级。`REPORTED` 为仅机器或评审回传，`INFERRED` 为由证据推导，`UNKNOWN` 为缺证，`BLOCKED` 为有明确门或缺项。计划、未运行和未测分别标记。
3. **保留历史和权限。** 失败、零变化、分母和旧快照由证据提交与变更记录保留。纠正用追加记录引用原提交，区分开发、Smoke、正式实验和人审。Owner 的新授权引用登记或合同。公开 Git 仅收脱敏汇总与哈希，原 TopK、逐样本标签、目标答案、私有评审附件及凭据保留在受控位置。
4. **独立维护。** 维护提交基于最新远端，从独立副本快进发布到 5060 研究分支。发现远端前移时先复核新证据。运行中的工作树由机器执行者在其收口节点自行协调同步，远端更新与工作会话已接收分别记录。
5. **状态权威。** 本页是双机索引。5060 动态状态以 [Current Work State](../../governance/current_work_state.md) 为准，证据索引以 [Experiment Master Record](../../governance/experiment_master_record.md) 为准，授权以 [Owner Decision Register](../../governance/project_owner_decision_register.md) 为准，冲突按 [Context Authority Map](../../governance/context_authority_map.md) 处理。

## 变更记录

| 日期（JST） | 版本 | 变更与核验基点 |
| --- | --- | --- |
| 2026-11-09 | 12 | 5060 封存 100 个可行性主案例和 20 条改写，Owner19 仅数据准备收口，预测与评分均未运行。 |
| 2026-11-09 | 11 | Owner19认可先可行性后人工标注，以新合成/公开数据准备为主、D1仅回归；未放行新数据一次性评分、模型/API和S2–S5。 |
| 2026-11-09 | 10 | 监督端只读审核Owner18开发完成结果，保留span与领域外风险，提出A先规则盲评/B等待多模型四臂的待Owner决策；不扩大科研许可。 |
| 2026-11-09 | 9 | 5060 完成 Owner18 的旧73开发与 UIE 只读核验，三轮封存，模型及独立验证仍关闭。 |
| 2026-11-08 | 8 | Owner18单独允许 Rule-V2 使用旧73开发及UIE只读许可/依赖核查；新模型资产/推理和独立测试仍未授权，S2–S5保持停止。 |
| 2026-11-08 | 4 | Owner16批准5060单独S1离线验证，状态APPROVED_NOT_RUN，5090 Llama2访问仍待审批；S2–S5继续关闭。 |
| 2026-11-08 | 2 | 新会话按交接包恢复并动态核对双机远端；5060/5090 均与交接 SHA 一致。登记 Owner R2 有界离线授权，释放模板覆盖诊断与四臂公平对照；无新实验结果。 |
| 2026-11-06 | 1 | 建立双机维护页。记录 5060 的旧 G3 零变化、S0 完成、R1/R2 与待放行状态，以及 5090 非 Llama 资产下载后 Claim 未运行。整理前 5060 `fa70d97`，5090 `dbd91f3`。 |
| 2026-11-08 | 3 | 5060 实测四臂、封存、K1-C，保持 5090 历史快照。 |
| 2026-11-08 | 5 | 5060 S1 单次合成开发验证失败，S2–S5 仍未授权。 |
| 2026-11-08 | 6 | Owner选B作为S1-B设计方向，新增文献对照、候选资源与独立验证审批提案；不准新模型下载、推理或科学试次。 |
| 2026-11-08 | 7 | 5060 S1-B 只读资源与独立验证审批包收口，执行门仍关闭。 |
