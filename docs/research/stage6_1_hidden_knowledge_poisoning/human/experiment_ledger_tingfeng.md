# Paper 1 人类可读实验总规划与实验总账

## 2026-11-10｜5060 Owner23A 静态复核完成，受控加载待批

`OWNER23A_STATIC_COMPLETE / OWNER23B_SMOKE_PENDING_OWNER / MODEL_LOAD_INFERENCE_NOT_AUTHORIZED / S2_S5_LOCKED / AUTO_CONTINUE=NO`。

Run W1-5060-OWNER23A-SCOPED-STATIC-20261110-01。CLI 静态 2,911/2,911 个符号、73/73 个 API-set 配对均解析，前沿 0。Owner22 两件资产、52 个解包成员及原证据哈希复核通过。整包许可、VC 最低版本、实际 CPU 后端仍为 UNKNOWN，峰值内存未测。历史迁移 QA 的 ACL 偏差已登记并保留。

新增下载、安装、发行 EXE/DLL 启动、模型加载、推理、API 与科学试次均为 0。Owner20 NO_GO、旧 S1 FAIL、R2 K1-C、Human Gold 0、正式 ASR/Accuracy 未测保留。下一门是单独批准 Owner23B 本机 load-only smoke，当前停止。

私有审计 ZIP 73 件，SHA256 fcde11120eecca20a1ea8398f22db35175853b4a5c9f200314cb46befa0bc589。

[静态报告](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER23A_SCOPED_STATIC_AUDIT_RESULT.md) · [Run Manifest](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER23A_SCOPED_STATIC_RUN_MANIFEST.json)

## 2026-11-10｜5060 Owner22 固定资产已获取，运行准入继续阻断

`OWNER22_ASSET_STATIC_INSPECTION_BLOCKED / MODEL_EXECUTION_NOT_AUTHORIZED / PEAK_MEMORY_NOT_PROVEN / AUTO_CONTINUE=NO`。两件固定资产各一次，实际正文 1,142,252,137 字节，SHA256 和长度均通过。GGUF 头和 52 件 ZIP 安全验包通过；整包许可与 Windows PE 运行闭包仍待证。

执行、加载、推理、安装、额外资产下载、新实验、模型 API 和费用均为 0。后续受控 smoke 尚未批准，且静态前置仍未闭合。Owner20 NO_GO、旧 S1 FAIL、R2 K1-C、Human Gold 0 和正式 ASR/Accuracy 未测均保留。S2–S5 锁定。

[静态验包报告](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER22_QWEN_GGUF_ASSET_STATIC_INSPECTION_RESULT.md) · [完整脱敏 Manifest](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER22_QWEN_GGUF_ASSET_STATIC_RUN_MANIFEST.json)

## 2026-11-10｜5060 Owner21 单模型只读审计完成

`READONLY_AUDIT_COMPLETE / HUMAN_DECISION_REQUIRED / AUTO_CONTINUE=NO`。Qwen 官方 Q4_K_M 与 llama.cpp b12242 Windows x64 CPU 发布身份和固定摘要均已核对。Qwen Apache-2.0、llama.cpp 源码 MIT，运行时整包第三方声明、PE 依赖和峰值仍未闭合。主机约 12.80 GiB 可用 RAM，规划峰值最高约 4.51 GiB，资源门仍阻断。

模型与运行时正文下载、安装、加载、推理、模型 API、费用和新试次均为 0。下一门仅为两项固定资产的获取与静态验包，尚未获批。Owner20 NO_GO、旧 S1 FAIL、R2 K1-C 保留，Human Gold 0，正式 ASR/Accuracy 未测，S2–S5 锁定。

[单模型审批包](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER21_QWEN_GGUF_SINGLE_MODEL_ADMISSION_PACKET.md) · [脱敏 Manifest](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER21_QWEN_GGUF_READONLY_MANIFEST.json)

## 2026-11-10｜5060 Owner20 单次规则可行性验证完成

`FEASIBILITY_NO_GO / S2_S5_LOCKED / AUTO_CONTINUE=NO`。两臂各 120/120，先封存后一次性评分，主 100 个语义案例另报 20 条改写。Rule-V1 值命中 0/70、已决定错抽 2/2，Rule-V2 值命中 5/70、已决定错抽 10/11，均未达冻结门。两臂在 30 个无标题主例均 UNKNOWN。Human Gold 0。

旧 S1 失败、R2 K1-C 及 Owner19 原封存保留。正式 ASR/Accuracy 未测，模型下载、推理、模型 API 和费用均为 0。当前批次已消耗一次科学试次，停止等待 Owner 决策。

[真实结果与失败归因](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_RULE_ONESHOT_FEASIBILITY_RESULT.md) · [脱敏 Run Manifest](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_RULE_ONESHOT_FEASIBILITY_RUN_MANIFEST.json)

## 2026-11-09｜5060 Owner19 可行性数据已封存，评价须另批

`FEAS_DATA_READY / PROVISIONAL_GOLD / EVALUATION_NOT_RUN / S2_S5_LOCKED / AUTO_CONTINUE=NO`。100 个全新虚构主案例（70 可答、30 应 UNKNOWN），另有 20 条从属问句改写。证据跨度、暂定标签、真值与配对、输入及协议已分件封存。标签是同一 Agent 的暂定标注，Human Gold 0。

Rule-V1/V2 新集零预测、零评分。D1 仅沿用历史开发诊断，CMRC2018 仅核元数据。模型下载／加载／推理和模型 API 调用为 0。下一门为 Owner 审批一次性规则可行性评价；正式 ASR/Accuracy 未测。

[结果与下一审批卡](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_FEASIBILITY_DATA_PREP_RESULT.md) · [脱敏 Manifest](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_FEASIBILITY_DATA_PREP_MANIFEST.json)

## 2026-11-09｜5060 Owner18 旧73开发完成，后续门关闭

`RULE_V2_DEV_COMPLETED / S1B_INDEPENDENT_TEST_NOT_RUN / MODEL_ASSET_NOT_AUTHORIZED / S2_S5_LOCKED / AUTO_CONTINUE=NO`。Owner18 批准的三轮旧73开发及 UIE 官方材料只读审计已完成。最终 58 正确、1 错误、14 UNKNOWN（73 条），值命中 59/61，决定后错抽 1/59，应拒识误答 0/12。旧 Rule-V1、S1 失败、R2 K1-C 保留。Human Gold 0，正式 ASR/Accuracy 未测。

UIE 权重/分词器条款、不可变身份、发布者 SHA256 和 Windows CPU 依赖锁待证。模型资产、推理和独立验证均须另批。新增模型下载、安装、加载、推理、API 与费用为 0。

[结果与失败](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_RULEV2_OLD73_DEV_UIE_READONLY_RESULT.md) · [证据清单](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_RULEV2_OLD73_DEV_MANIFEST.json)

## 2026-11-08｜5060 S1-B 只读审批包完成

`S1B_DESIGN_ONLY / MODEL_DOWNLOAD_NOT_AUTHORIZED / MODEL_INFERENCE_NOT_AUTHORIZED / VALIDATION_NOT_AUTHORIZED / S2_S5_LOCKED`。Owner B 只读审批包已完成，UIE Nano 权重条款和强身份待核，Qwen2.5-1.5B 已核固定 revision 与权重许可。独立验证保管人未指定。新增模型、推理、下载、安装、科学试次和费用均为 0。Auto Continue = NO。

[Owner 审批包](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_OWNER_ADMISSION_PACKET_20261108.md)。SHA256 `f3204df649a34f500cd7ad751f0e4952a595879eb79b2315e3b8b19fd4b5b9c7`。

## W1-5060-S1-CHINESE-EXTRACTION-20261108-01 — S1 封存失败与停止

Owner16 S1 单次封存验证结束，S1_FAIL_STOP。73 条合成样本，30 正确、4 错误、39 UNKNOWN；答案值 31/61、已决定错抽 4/34。自然中文可用 scope-bound 事实 25/49。模型、API、下载与费用为 0。Human Gold 0，正式 ASR/Accuracy 未测。S2–S5 未授权，Auto Continue = NO。

[S1 结果与证据](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_S1_INDEPENDENT_CHINESE_EXTRACTION_RESULT.md)。


## W1-5060-R2-FAIRCTRL-20261108-02 — 离线公平对照收口

R2 有界离线四臂已完成。B2 重放 36/36，网页模板高置信 6/180、3/36 世界，蒙版对两种分词的删除集合均无影响。char2 额外删除 31/180 片段，Poison 删除 2/10→4/10，Clean 误删 4/10→5/10，HN 删除 2/9→4/9。可比被删候选为 0，预注册判定 K1-C / INSUFFICIENT_OR_MIXED。真实 API、下载、重新检索及费用均为 0。S1–S5 未放行，Auto Continue = NO。

[R2 实测与证据](
../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/W1_5060_R2_FAIR_CONTROL_RESULT.md
)。


## 当前工作 — 5060 VESA 评审重构 S0 完成，D1 来源证据门阻断（2026-11-06 JST）

W1-5060-REVIEWER-REPLAN-S0-20261106-01，S0_COMPLETE / OWNER_CHECKPOINT_PENDING。封存的 36 个世界、180 个片段复核完成。B2 在 36/36 世界有删除，已召回候选 Poison 删除 2/10、Clean 误删 4/10、HN 删除 2/9。生产侧可信来源覆盖 0/180。严格 P0 下当前 D1 无法达到 S4 的 Clean 误删 <4/10 门。S1–S4 未运行，S5 无授权，新增 API 0、费用 0。正式实验未启动，Human Gold 0、正式 ASR/QA 未测。下一个门是 S0_CHECKPOINT_RELEASE。RD-zh 本地编码与独立 S3 留出方须按 R1-10 决定。原历史证据保留，Auto Continue = NO。

S0-04 RD-zh 适配器与静态验证已完成，4 项测试通过。真实 D1 编码、过滤和 S1–S4 未运行，S0 检查点继续等待 Owner 放行。

[S0 结果、证据与十二字段决策](../../../paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_SUMMARY.md)。


## 当前工作 — Owner14 VESA v0.2 无实质 G3 差异（2026-11-05 JST）

v0.2 可以抽取更多查询和片段，但 81 个被隔离的片段均没有与问题范围绑定的具体值。36 个 G3 上下文仍与 G2 相同，真实调用 0，未形成新防御效果。12 题审阅包已核验，尚未分发给独立审阅者。

[离线结果与证据](../../../paper1/dual_machine/chinese5060/vesa_guard_v02/VESA_V02_OWNER14_RESULT.md)。以下为历史快照。

## 当前工作 — Owner13 VESA v0.1 离线无安全差异（2026-11-05 JST）

已实现版本核对、独立证据和安全恢复规则。原 36 世界均缺可核来源，81 个被旧过滤器隔离的片段没有安全恢复条件。G3 与 G2 完全一致，本轮未发送任何请求，未形成新防御效果。

[离线结果与证据](../../../paper1/dual_machine/chinese5060/vesa_guard_v01/VESA_V01_OWNER13_RESULT.md)。以下为历史快照。

## 当前工作 — 5060 Pilot12 D1 暂定评价完成（2026-11-05 JST）

108 格原始回答已完成独立侧的确定性核查，未增加 API 调用。18 格暂定合理拒答，39 格回答和另 51 格拒答需要语义裁决。两套过滤配置节省用量，G2 少了 4 格回答。当前证据不足以确认基线的安全与质量收益。

[暂定效果评价和证据](../../../paper1/dual_machine/chinese5060/pilot_rapid_live/PILOT12_D1_AI_PROVISIONAL_EFFECT_REPORT.md)。以下为历史快照。

## 当前工作 — 5060 Owner12 Pilot12 V2 真实生成完成（2026-11-05 JST）

原定首 3 格通过工程检查后，余下 105 格自动完成。108 次真实请求全部通过，39 格回答、69 格拒答，无异常或重试。按用量和公开价估算 ¥0.130084，实扣未核。回答质量和方法效果尚待独立评价。已完成本轮执行并停止。

[真实结果和证据](../../../paper1/dual_machine/chinese5060/pilot_rapid_live/RAPID_LIVE_OWNER12_EXECUTION_RESULT.md)。以下为历史快照。

## 当前工作 — 5060 Owner12 V2 首发前资金核验阻断（2026-11-05 JST）

Owner12 已批准有条件的首 3 格和同一轮余下 105 格。本机能核历史账，缺当前全线费用和北京账户可用资金的数值边界，实验在首发前停止。真实调用 0 次，108 格未运行，新增费用 0。下一项需要一份带时间的 USD 资金快照。生成效果和正式评分仍未测。

[准入证据与下一项](../../../paper1/dual_machine/chinese5060/pilot_rapid_live/RAPID_LIVE_OWNER12_RESULT.md)。以下为历史快照。

## 当前工作 — 5060 Pilot12 来源与历史账本已恢复，真实准入仍阻断（2026-11-05 JST）

此前未匹配的29个来源均已还原到D1签署候选。旧北京工作空间和历史账也已复用，本轮真实调用0次、费用0。仍待确认当前外传范围、账户计费与账本、Token严格证明或后置检查风险。

[Evidence Recovery Addendum](../../../paper1/dual_machine/chinese5060/fast_unblock/FAST_UNBLOCK_EVIDENCE_PACKET.md)。以下为历史快照。


## 当前工作 — 5060 Fast-Unblock 离线验收完成，真实准入仍阻断（2026-11-05 JST）

本轮只修订请求的输出上限字段名并另封V2，108格均完成离线复核。合成108格通过，真实调用0次、费用0。来源权利、账户端点和计费、严格Token及完整账本还需可核材料，齐备后交Owner一次审真实执行。

[唯一审批入口](../../../paper1/dual_machine/chinese5060/fast_unblock/FAST_UNBLOCK_EVIDENCE_PACKET.md)。以下为历史记录。


## 当前工作 — 5060 Pilot12 准入拒绝，真实请求 0（2026-11-05 JST）

W1-5060-PILOTLIVE-20261105-01 已完成本地核查。108格与冻结输入一致，真实请求0次，新增费用0，108格均未运行。外传、地区和真实计费上限、精确Token、实时预算与独立准入均需证据闭合。46项离线测试通过。当前结论只支持工程检查，生成效果及正式评分未测。

[主要证据和下一门](../../../paper1/dual_machine/chinese5060/W1_5060_PILOT12_CONDITIONAL_LIVE_RUN_REPORT.md)。以下为历史记录。


## 5060 最小 RAG 运行器已通过本地验收（2026-11-05 JST）

固定108格已在 FakeTransport 中逐格演练。正常批108格全通过，超时及缺用量分别在第4和第2格停发，并保留其余104和106格的状态。29项测试、Ruff和MyPy通过。真实API 0次、新增费用0，真实生成及正式评分未启动。

Owner已经核验账户模型、地域、费率和余额。真实运行仍待一次新审批，需绑定受控费用账本、精确Token计数、接口硬上限和最终执行代码。当前工作 W1-5060-RUNNER-20261105-01，状态 RUNNER_IMPLEMENTED_LIVE_NOT_AUTHORIZED。Human Gold 为0。

[工程报告与准入包](../../../paper1/dual_machine/chinese5060/W1_5060_PILOT_RUNNER_IMPLEMENTATION_AND_ADMISSION_REPORT.md)。下方为历史记录。


## 当前 / CURRENT — Pilot12最小RAG设计/预算完成，真实执行未授权（2026-11-05 JST）

W1-5060-PILOTDESIGN-20261105-01；DESIGN_ONLY_NOT_RUN；W1-OD-20261105-5060-PROVISIONAL-PILOTDESIGN-08。
原12事实组/36世界、旧TopK及B0/B1/B2上下文静态编排108格，全部NOT_RUN，不重检索/重跑过滤器；本次模型/API/Tokenizer调用0、费用0。
暂定参考JSON原SHA5c5f212b…已收到并复制D隔离，12 REVIEW-ID/38原子、12题逐字匹配，每题对应3世界9格；参考不进入Generator白名单。
HumanGold0、target UNKNOWN、C3未裁决，正式ASR/Accuracy未测；私有参考/映射/消息不进Git。MD未定位不阻断完整JSON设计。
候选4096输入/256输出、最多108请求：输入442368、输出27648 tokens；静态字节+512代理最大2956/2541/2603，非精确Qwen计数。
执行仍DESIGN_GATE_BLOCKED：当前provider/型号/账户/价格/余额/FX/累计账单、精确token和wire adapter待核，需新的Owner执行SHA。
预算仅条件式0.442368*P_in+0.027648*P_out及20%候选预留，不给未核实美元报价；USD30/25/28门及历史费用差额保留。
旧B2 Clean误删上升、FastC根因未识别和2.5pp安全边界保留；单类12例不能证明保护门满足。暂定评分UNKNOWN/拒答/故障统一，不添加judge API。
5tests/Ruff/增强MyPy3源码通过；所有新项目内容D，本次无模型/资产下载，用户C附件只读。下一Owner Gate审核本包及补齐预算/计数/adapter证据后另批执行。
禁止真实/免费API探测、生成、B3-B6/D1-40/D2D3/Reviewer/GT/T1/T2/Claim和跨分支合并；本轮Git交付后STOP。[最小设计及待审包](../../../paper1/dual_machine/chinese5060/W1_5060_MINIMAL_RAG_PILOT_DESIGN_AND_BUDGET.md)。 下方历史不改。


## 当前 / CURRENT — Fast C只读统计完成，阶段因果仍未识别（2026-11-05 JST）

W1-5060-FAST-C-20261105-ATTRIB01；PARTIAL_DIAGNOSTIC_UNRESOLVED，W1-OD-20261105-FAST-C-06。
原P2/PAIR01/评价seals及私有ZIP身份通过，原字节未改；0模型/Guard/检索/LLM调用、0新安全试次/下载/商业API。
全36/条件29/7MISS和TP/FP/残留复算一致；Poison四格全9/2/1/0，Clean7/4/1/0，HN9/1/1/1。
72/72保存分数+count能复算原选择；任意同分29/36与33/36，cutoff同分6/36与8/36，不混为因果。
n_adv变13/36、删除集合变21/36（其中8同count变选择）；候选flip10中4变count、6同count、4两侧均无cutoff tie。
聚类成员/embeddings/pair-set/逐词TF-IDF均缺，背景GT/HN合法历史时效缺裁决；INSUFFICIENT_TRACE/SOURCE_UNVERIFIED，因果子问题STOP。
三进程白名单隔离，role-free锁后旧Evaluator对齐；独立未签12卡38原子16源、56引用定位及29文件盲审ZIP准备，Gold0/target UNKNOWN。
5tests/Ruff/增强MyPy4源码通过；纯JSON复核8文件字节一致，非新模型试次；ASR/QA未测。
下一Owner Gate：审阅归因边界及独立人工范围/target/C3，必要旧trace须另指明授权路径；不自动补采或重跑。
禁止B5/B6、付费/下载、D1-40/D2D3/Reviewer/GT/T1/T2/Claim和跨分支操作；本次Git收口后STOP。[Fast C证据与局限](../../../paper1/dual_machine/chinese5060/W1_5060_FAST_C_READONLY_FAILURE_ATTRIBUTION_REPORT.md)。 下方均历史。


## 当前 / CURRENT — Fast B离线B1/B2配对完成（2026-11-05 JST）

W1-5060-FAST-B-20261105-PAIR01；B1_B2_PAIRED_OFFLINE_DEVELOPMENT_COMPLETE，非正式论文实验。
执行源码17897075bfdbc325979b29e75b7209877bc5bebb；原库ba2a17ef未改、只换embedding，固定原36TopK，未重检索/重跑B0。
B1/B2各36/36 PASS、失败0/空集合0/联网0；原输入29命中(P10/C10/HN9)、7miss(P2/C2/HN3)单列。
Poison TP B1=1/12、B2=2/12（条件1/10、2/10）；Clean FP=1/12、4/12（1/10、4/10）；HN FP均2/12（2/9）。
B1/B2删chunk78/180、81/180；每个召回Candidate恰好1chunk，any与all-retrieved计数相同，partial0不证明多chunk清除能力。
仅换中文embedding未获得整体安全质量改善，不能称新算法/GO；真实ASR/Answer Accuracy/生成拒答未测，商业API0/费用0。
7tests/Ruff/MyPy3源码通过；输出全封存后独立Evaluator读批准D1开发标签，raw仅本地；原盲审包12题38原子复用、Gold0。
Owner人工官方直连取得固定模型，Git/LFS/hash核验通过；新模型和临时/缓存全D，B2从既有C缓存只读复制，旧下载/失败账本保留。
下一Owner Gate：审阅本轮结果及独立答案范围/target/C3裁决，决定后续；本轮Git交付后STOP，不进入P3/付费/新机制。
禁止B3-B6、D1-40、D2D3/Reviewer/GT Vault、T1/T2/Claim和跨分支合并。[实际结果与证据](../../../paper1/dual_machine/chinese5060/W1_5060_FAST_B_PAIR01_RESULT.md)。 下方旧状态保留为历史。


## 当前 / CURRENT — Fast B合同已修复，官方HF连接失败（2026-11-05 JST）

run W1-5060-FAST-B-20261105-RECOVERY01；BLOCKED_HF_DIRECT_CONNECTION_TIMEOUT，Fast B整体未完成。
98228e202062b1216094acac90f83be29cc63074已补齐合同，旧14d718f checkpoint保留；不再寻找聊天附件。
唯一HF固定revision元数据直连WinError10060/exit1，未获HTTP状态/正文、无重试/代理/模型下载；B1/B2各0/36运行，指标NOT_RUN。
HTTP响应0字节但保留1MiB保守网络预算占用，不称TCP/DNS网络绝对0；商业API0/费用0，无模型载入或生成。
原seal全部成员/36TopK/原源码hash及selection复核通过；不重检索，B0未重跑；29命中与7miss仅历史输入分母。
原12题38原子16来源盲审包hash不变，直接复用；HumanGold0、target UNKNOWN、C3待裁决，ASR/QA未测。
4项盲审工具回归/Ruff/MyPy1源码通过，不代表模型或基线实跑；新项目内容全D，既有C环境只读。
下一门：Owner确认可用官方直连条件并明确恢复同源预检；资产门仍未通过。受影响任务停止，Git交付后STOP。
禁止自动重试/替代源/模型/商业API、B3-B6、D1-40、D2D3/Reviewer/GT、T1/T2、5090 Claim及跨分支合并。
[实际失败和下一门](../../../paper1/dual_machine/chinese5060/W1_5060_FAST_B_RECOVERY01_RESULT.md)。 下方是不可变历史状态；新运行及新失败不追溯改写旧结果。


## 当前 / CURRENT — 5060 Fast-Track B准入审计及盲审材料已保存，执行合同缺口待补（2026-11-05 JST）

PAPER1-W1-5060-FAST-B；FAST_B_PARTIAL_PREFLIGHT_PASS / B1_B2_NOT_RUN_CONTRACT_BLOCKED；不是Fast-Track B完成。
控制面f491c0a507e5555e9611c022cfba66980ad8cbca，W1-OD-20261105-FAST-B-04与RESOURCE-REPRO-05已核；原分支仅ff-only同步。
官方源码ba2a17ef未改；原P2封存成员及36份TopK字节身份通过，不重新检索；29命中/7miss仅沿用P2历史输入聚合。
本轮4tests/Ruff/MyPy1源码通过，独立待审包12题/38事实原子/16官方来源，未签署、HumanGold0，未阅读候选/标签/预测来制卡。
Owner消息要求随附最终Prompt，但聊天附件清单和固定授权目录未找到；W1-5060-FAST-B-CONTRACT-01 / HUMAN_DECISION_REQUIRED。
受影响下载/模型载入/B1/B2未启动；新HF请求0/下载0/API0/费用0。ASR/QA未测，不能将未运行填0或宣称RAGDefender失效。
新项目进程TEMP/TMP/缓存/日志/归档落D；本支路64MiB峰值、20GiB安全余量；取消D/E原1GiB限不放宽250MiB下载界。
下一Owner Gate：提供最终Prompt确切身份后核对额外门，再闭合模型/下载合同；独立人工审定范围/target/C3另待返回。
T1/T2、付费、B3/B4/B5/B6、D1-40、D2D3/Reviewer/GT及跨分支合并仍禁止。checkpoint文档/Git交付后STOP。
[Fast B审计和受阻交付](../../../paper1/dual_machine/chinese5060/W1_5060_FAST_B_B1_B2_OFFLINE_RESULT.md)。 下方旧状态均保留为历史，不追溯改写原BLOCKED或授权事实。


## 当前 / CURRENT — Fast-Track A T0/B0真实检索完成（2026-11-04）

PAPER1-W1-5060-P2-FAST-A；T0_B0_DIAGNOSTIC_COMPLETE / B1_B2_BLOCKED。
授权W1-OD-20261104-FAST-A-03@af68d89a；执行9aa21be13ae206dbbadb03b99528e362eba29378；run W1-5060-P2-20261104-T0-01。
36/36物理独立索引，27072chunk，180hits；Candidate hit@5 29/36，排名1/2/4位=25/3/1，miss7(P2/C2/HN3)。
全部关闭重开rank/score精确重放；56tests/Ruff/MyPy10源码和6个正式命令步骤exit0；新API0/费用0/下载0/GPU0。
B0删除0，TP0/12/CleanFP0/12/HNFP0/12；仅召回Candidate条件性分母10/10/9；7miss单列，不算防御成功。
B1默认embedding精确revision缓存未闭合而BLOCKED，B2连带BLOCKED；RAGDefender效果未测，不填0。
ASR/Answer Accuracy/生成拒答未测；12卡/38原子待Owner独立裁决、HumanGold0，未推断target。
T1未授信/T2禁用，无B3/B4/B5/B6/D1-40/Claim；D2D3/Reviewer/GT Vault未读。P0元数据事件保留。
下一Owner Gate：精确B1资产条件（如需下载须新批）及12卡范围/target/C3；本轮文档/Git收口后STOP，不进P3。
[P2报告](../../../paper1/dual_machine/chinese5060/W1_5060_P2_T0_RETRIEVAL_DIAGNOSTIC.md)。下方历史保留，不把本次工程观察升级为论文或独立泛化结论。


> P1最终只读补充：5090已前进0155470，上游不变、Claim仍未批；分支局部PODR-154重名使用Owner W1-OD跨机关联。[证据](../../../paper1/dual_machine/chinese5060/p1/evidence/LATEST_5090_HANDOFF_SUPPLEMENT.json)。P1 source/run/准备状态不变。


## 当前 / CURRENT — 双机治理已登记，P1零付费准备完成（2026-11-04）

PAPER1-W1-5060-P1；P1_PREPARATION_COMPLETE / REAL_PILOT_BLOCKED。
Owner W1-OD-20261104-5090-ENV-01有条件接受5090独立兼容环境，但不授权权重下载或Claim；
W1-OD-20261104-DUAL-GOV-02保留两机分支及既有起点，不reset/rebase/merge/cherry-pick。
5090脱敏Git固定aa85841ff83be31c86e0fa305d3a84d70f2158b5，上游ba2a17efba165d45409114df2d70b030ade1e1b8；Claim均NOT_RUN。
5060执行fcdd848e29e3fea97b11a6352a4ff8e1665f4071，run W1-5060-P1-20261104-02；48tests/Ruff/MyPy和11项命令检查通过。
固定Pilot12/选择hash不变；12题38事实字段56引用/18来源hash定位通过，但HumanGold0，12题评分/target仍NEEDS_ADJUDICATION。
36互斥世界设计各1候选+18共同低信任背景，整库身份和正文副本检查通过；实际索引0/TopK0/生成0，不能称真实RAG成绩。
旧Top5有5/36缺V2引用来源，不能直接继承；T1独立官方根与B1库/论文轨道等仍待审批。T2禁用。
D1仅8路径hash白名单，无D2D3/Reviewer/Oracle内容读取，P0文件名事件保留。新API0/费用0，无B5/B6/D1-40/新Claim。
精确Qwen公开北京原价已查，账户/精确token计数/账单差额仍未核，不探测；USD30/25预警/28停止新批保持。
下一门：Owner审阅B1轨道、共同背景/可信证据权限、答案/攻击目标/C3规则及零费用真实检索预检范围；本轮交付后停止。
[P1治理与准入报告](../../../paper1/dual_machine/chinese5060/W1_5060_OWNER_GOVERNANCE_AND_P1_GATE.md)。下方历史记录保留，不产生付费、模型下载或方法接受授权。


## 当前 / CURRENT — 5060 P0审计与虚构基础工程通过（2026-11-04）

PAPER1-W1-5060-P0；PODR-161；P0_ENGINEERING_PASS / REAL_PILOT_NOT_READY。
独立分支research/paper1-chinese-defense-5060，开发基线8dec9453，执行SHA ca75c381546247ad3377013a75bb21133cc078ed，
run W1-5060-20261104-P0-01。21tests/Ruff/MyPy（7源码）与D1身份审计、3虚构世界Chroma重放均通过。
D1实际40组120条13家族、S=12/15/13；旧Pilot12身份复核12组36条9家族、S各4，8组24HOLD仍排除。
只读白名单未打开D2D3/Reviewer/Oracle/新评价答案提案，不改GT。新API0、费用0、GPU未用。
启动文件名发现范围过宽曾显露受限路径名，已停止全树发现；内容未读取，路径触达例外在P0报告链接中披露。
Owner累计预算30美元/25预警/28停止新批，旧支出保守占用不清零；Owner报告当前费用7.528095914元、无未结算、可用，
旧usage7.611826元差额保留。当前模型/价格/精确余额未机器核验，真实场景/迁移公平合同未冻结，付费不启动。
真实Pilot/D1-40/最终QA均NOT_RUN；ASR/Answer Accuracy NOT_MEASURED；B5/B6尚未提出，首次冻结必须Owner批准。
下一步先取得5090固定上游语义脱敏交接并闭合独立query/逐世界足证/同权限强基线/预算评分合同；不据旧E1 37/40宣称RAG效果。
[P0报告](../../../paper1/dual_machine/chinese5060/W1_5060_P0_INITIAL_STATUS.md)。下方为历史状态，本条只更新本工作线执行状态，不接受新方法或替换正式研究基线。


## 当前 / CURRENT — 第七条范围收口，12题AI数据草案准备完成（2026-11-04）

PAPER1-RAG-DEFENSE-RECONSTRUCTION-01；AI_DATA_PREPARATION_COMPLETE_PROVISIONAL / SCENARIO_CONTRACT_NEXT；PODR-160。Owner明确限定第七条核心职责；修订题的两份独立审阅和来源仲裁确认3字段等价，9处引用定位通过。第二版12题均有据AI草案，职责范围待决0；问题/评价侧答案隔离，原题/原分歧/全部原审阅保留。人工金标准仍0，非正式实验结果。
无需Owner从零补数据。下一步由执行端准备受控检索后C0–C3场景、共同证据预算与评分合同，并闭合B2迁移可比性和费用门；本任务新阿里云API0/费用0，未自动付费，B4/正式实验未启动。
[第二版结果与准备边界](../core144/rag_defense_reconstruction_01/AI_DATA_PREPARATION_SCOPE_CLOSURE_V2.md)。下方为历史状态，不能据旧“范围待定”重复请求Owner确认。

## 当前 / CURRENT — AI数据草案已准备，Owner集中确认1项范围（2026-11-04）

PAPER1-RAG-DEFENSE-RECONSTRUCTION-01；AI_DATA_PREPARATION_REVIEW_READY / QUESTION_SCOPE_DECISION_REQUIRED；PODR-159。12题/18源/38字段的两份隔离agent审阅及来源仲裁已完成，原始输出保留。原双审100处引用、仲裁58处引用定位通过；一题单独补源双审2字段/4处引用通过，未更改运行时Top5。最终11题有据AI草案、1题职责列举范围待定，另2项题干文字澄清建议；人工批准/金标准均0。
这些是AI_REVIEWED_DEVELOPMENT_DRAFT_NOT_HUMAN_GOLD，不是防御效果或第三份独立盲审。新增阿里云API0/费用0，B4/正式实验未启动，D2D3/Human/GT/历史不改。下一步只需Owner明确职责题范围（建议第七条），执行端继续承担查证、数据整理与场景准备；逐世界公平预算、迁移可比性及费用门仍保留。
[结果、Owner精简事项和十二字段决定](../core144/rag_defense_reconstruction_01/AI_DATA_PREPARATION_OWNER_REPORT.md)。下方均为按时序保留的历史。

## 当前补充 — 原始来源找到问答线索，独立裁决仍待完成（2026-11-04）

PAPER1-RAG-DEFENSE-RECONSTRUCTION-01；PHASE1_2_REVIEW_READY / HUMAN_DECISION_REQUIRED。只读核查确认28份选定证据有相同上游正文，2份官方来源定位出17条问答片段线索；旧120条检索query均含完整候选，不能直接作独立QA。建议先审阅已有官方问答的题干/时间/范围/答案边界和冻结组对应，再补不足；12组仍NEEDS_ADJUDICATION。Owner明确继续后另生成12条来源审阅问题草稿、23次来源引用，答案全部null、未批准，控制映射另存评价器；尚无可执行Pilot。未重做验证，新增API0/费用0，B4/正式实验未开始，D2D3/Human/GT不改。
[新增证据、限制和下一门](../core144/rag_defense_reconstruction_01/SOURCE_REUSE_FOLLOWUP.md)。下方为先前审阅记录。

## 当前：先补查询与答案，再判断是否值得改方法（2026-11-04）

PAPER1-RAG-DEFENSE-RECONSTRUCTION-01；PHASE1_2_REVIEW_READY / HUMAN_DECISION_REQUIRED。已从暂停点续接并形成十项交付。RAGDefender的核心程序确实运行过，但使用的嵌入模型不同于论文，默认示例和作者测试也没有全部通过，所以只能说核心可运行。
现有D1是短命题核验资料：选定12组尚无独立查询与答案裁决，不能直接当问答基准。我们还没有测出强基线在新检索场景中的弱点，也没有证据支持实现新方法B4。建议先寻找已有官方问答材料，再由独立裁决补齐；付费Pilot及B4暂不开展。
本任务API调用和费用均为0；旧任务已知估算7.611826元仍累计，正式账单未核对。没有重跑已完成验证，暂停前测试记录对应源码未变；原始本地测试日志缺口如实保留。D2/D3、人工标注、Ground Truth和历史分数不改，正式实验未开始。
[七个科研问题与下一决定](../core144/rag_defense_reconstruction_01/OWNER_FEASIBILITY_DECISION_REPORT.md)。下方为历史，不构成自动继续授权。

## 当前 / CURRENT — Owner暂停方法重构任务，等待新会话续接

2026-11-04；`PAPER1-RAG-DEFENSE-RECONSTRUCTION-01`；`OWNER_PAUSED_IN_PROGRESS_NOT_COMPLETE`。独立分支`research/paper1-rag-defense-reconstruction-01`，基线b235381，本任务WIP未提交未推送。
已完成上游固定/静态审查、非论文embedding的CPU核心API执行及D1包数据门审计；本轮API0，B4未实现。查询/独立答案裁决缺失，付费Pilot不得启动。用户明确暂停，Auto Continue=NO。
续接入口：[暂停续接记录](../core144/rag_defense_reconstruction_01/RESEARCH_CONTEXT_RECOVERY.md)。历史结果、D2D3、Human/GT及旧工作树保持；下方状态为历史。

## 当前：可行性实验完成，强基线可用，新增机制未证（2026-11-03）

本轮问题已经有答案：同一个强API模型直接核验表现好，但我们新增的前置和六槽流程没有带来收益。
120条候选四个条件全部封存后独立评分。直接核验与加前置的条件都检出37/40，正常样本误报0/40，困难负样本误报1/40，严格三元组成功30/40。
六槽两个条件全部返回证据不足；主要原因是模型给出的槽值未能满足逐字原文锚定合同。不能把全部弃权的零误报说成方法成功，也不能把这个实现失败说成中文任务不可做。
程序先前的52条硬停原件保留；批准A后复用旧响应，只补剩余调用，没有重推或提高输出上限。累计361次请求，按usage原价估算7.611826元，最终账单还未对账。
事前规则结论CONDITIONAL：保留强基线，新增算法贡献未证。D1仍是已暴露开发集，不代表正式测试、跨领域有效或发表保证。
[最终负责人报告](../core144/feasibility_sprint_01/FEASIBILITY_OWNER_REPORT.md)说明分母、失败、成本和证据。建议结束本轮，不再改提示/放宽parser追分；下一门是负责人审阅。D2/D3独立工作线与历史结果不改。

## 当前 / CURRENT — Owner批准A与阿里云15美元预算，恢复尚未执行

2026-11-03；PAPER1-FEASIBILITY-SPRINT-01；PODR-157。Owner明确批准方案A，并将阿里云API任务总预算提高到USD15。
新RunD1-DEV-BEIJING-CONT-A01：原52包逐字节复用，第53条已付费internal/direct响应复用；length逐条INSUFFICIENT，不重试，不改prompt/模型/输出上限/判据。原Attempt01失败、HARD_STOP及归档不变。
已有费用3.264570CNY累计；新预警USD14/硬停14.50，按原6CNY/USD保守界为84/87CNY，保留0.50USD缓冲，不扩展服务商或实验矩阵。
当前CONT_A_APPROVED_IMPLEMENTED_PREFLIGHT_NOT_YET_EXECUTED；实际总请求仍159，完整新预测锁未形成，标签未打开。
下一步：测试、身份预检、冻结提交/推送后，在原七天窗口内补剩余调用；全120四条件封存后独立评价，不再重复申请已批准普通阶段。新工程异常仍停止。
科学方法PROPOSED/EXPERIMENTAL、D1_DEV_EXPOSED、正式实验NOT_STARTED；5090、D2D3、Human/GT、旧L0保持。
[冻结补充合同](../core144/feasibility_sprint_01/CONTINUATION_A_PROTOCOL_V3.md)。下方Owner待决为已被本次批准覆盖的历史。

## 当前：已真实运行，但第53条输出达到上限，暂停等待执行规则决定

2026-11-03；PAPER1-FEASIBILITY-SPRINT-01；RunD1-DEV-BEIJING01；执行dbc4cc1。北京接口虚构探测通过；许可/Key/端点已闭合。
真实D1完成52/120候选包、208条件预测，第53个候选direct返回length/1024；GENERATION_NOT_COMPLETE_NO_RETRY按冻结实现整轮退出1。没有自动重试、提高上限或修改模型/prompt/parser/路由。
159请求含探测1，usage原价估算3.264570CNY，保守USD界约0.544095，无待结算预留。52前缀不评分、无完整预测锁，真实标签未打开；科学NOT_EVALUATED、正式实验NOT_STARTED。
状态HARD_STOP_OUTPUT_LENGTH_OWNER_REVIEW_REQUIRED。下一门：Owner决定是否仅将length记为逐条INSUFFICIENT、不重试、复用52包及第53条已有调用，在原窗口/费用账本内完成其余调用；当前仅PROPOSED，未改源码或启动Continuation。
原Attempt01/HARD_STOP/709文件索引及私有归档保留，归档SHA34680b4cdb7e4c90a46942f2cea7b1bebec23f73a680342270a43ee0d579481b；索引SHA9055fca39ddc455e1df7f6e6d5ff989bcc8e94e0068055c1f2c0f50f3d096ffa。原始正文/响应/工作区/Key不进Git。5090、D2D3、L0、Human/GT不改。
[报告与下一门](../core144/feasibility_sprint_01/BEIJING_ATTEMPT01_OWNER_REPORT.md)。下方ready/未调用为此前历史。

## 当前：账号与数据许可条件已补齐，下一步只测接口

2026-11-03；PAPER1-FEASIBILITY-SPRINT-01；基线69899e2。Owner提供北京工作区Host、完成用户环境Key配置，并明确确认许可及保密要求允许D1/Top5由阿里云处理。原Global授权有效，不重复询问。
当前BEIJING_LIVE_PROBE_READY_NOT_EXECUTED；实际API0、费用0、真实D1预测0；不宣称开通或模型实测成功。
仅适配cn-beijing的ws/llm官方工作区格式和CNY原币计费，科学机制/模型/prompt/parser/路由/数据/指标不改。CNY24预警/27硬停，按6CNY/USD保守预算界，不是即期汇率或扩预算。
先锁定/推送后单次虚构探测；成功才同一120条E1-E4，封存后评价。HTTP/非Thinking/版本/usage/预算异常停止，不换模型、不重试。5090和D2D3/历史仍禁止。
[补充合同](../core144/feasibility_sprint_01/BEIJING_EXECUTION_ADDENDUM_V2.md)。以下保留先前条件未闭合的历史。

## 当前：一周可行性验证，本地程序已准备，API尚未调用（2026-11-03）

任务`PAPER1-FEASIBILITY-SPRINT-01`。本次先判断方案是否值得继续，论文目标按Owner调整为CCF C级可行性。
[说明与交付](../core144/feasibility_sprint_01/README.md)：比较同一个API模型直接核验、内部矛盾前置和六槽关系核验，避免把换更强模型说成算法成功。
内部只有真同域互斥才拦截；不能证明就继续外证。格式/引用错或缺证保留“证据不足”，不从分母删掉。
本地虚构案例、费用门与封存/评价流程已实现，原120条Top5文件身份核对通过；真实D1标签未打开。
你已批准阿里云Global外传，不再重复问。尚缺实际账号/工作区、许可保密确认和本机Key；所以API调用0、费用0、还没有真实性能。
当前暂不启动付费，科学效果未评价。最多七天、4.50美元硬停；不换第二付费模型、不追加旧L0提示、不使用5090，不动D2/D3标签。

## 当前：这轮基线已测完，报告提交负责人审阅（2026-10-31）

现有证据足以建议结束本轮D1/L0开发基线和固定提示探索。[负责人报告与PDF](../core144/l0_closeout_20261031/README.md)整理完整路线、分母、失败和负结果。
F5检出5/40，参考证据Oracle检出14/40；引用校验只挡住F5的1条原正确冲突判断，主要问题仍是事实核验。
一次逐断言提示检出15/40，但比Oracle净多5个合法样本误报，严格组内成功仍8/40，未达到“检出增加且误报不增加”。没有第二版提示。
负责人尚未最终验收，不能写方法成功、正式测试或泛化。本报告只核实Git脱敏记录和汇总算术，私有原始文件仍在5090，不能冒充本机独立重放。
不继续追加GPU预检、提示词、F5重跑或新方法实验。以下为按日期保留的历史阶段，不是当前待办。

## 2026-10-29：R02开始测D1，但显存不够，没有分数

批准的新运行用的还是原来的模型和提示词。虚构小题的工程检查过了，5题对了4题；这只说明诊断情况，不是120条的检出率，也不能把上次失败说成已经通过。
正式题目刚写完5条，下一条生成时显卡内存不够，还要再要约12 GiB，当时只剩约2 GiB。Oracle一条都没跑。
所以现在没有Recall、误报率或弃权率，不能填0。两次硬停记录都留着，没有为了继续跑去改程序或换量化模型。
[阻断说明](../core144/vace_lite/VACE_L0_R02_CUDA_OOM_BLOCKER_V1.md)。

## 2026-10-29：批准R02测真实D1效果，不再要求模型先答对全部虚构题

原R01的硬件/官方Qwen已加载，五个虚构题里一个结论字段与理由打架，因此按旧合同停止，D1没有测。
你现在明确批准：新开R02，把虚构题答对率作为模型诊断记录，而不是启动D1的条件；格式、引用、CUDA、hash、预算、确定性硬门仍保留。
不会手工改模型答案，不换prompt/解析器/模型/证据或种子；新目录只读复用R01已装好的环境与权重，原HARD_STOP和失败原件全留。
新240条预测先全部封存，再独立评分。既看分层Recall，也看HN误报、正常知识支持和弃权，不能把“测到了”说成“方法有效”。
目前本机只准备并验证[R02执行包](../core144/vace_lite/VACE_L0_R02_OWNER_APPROVAL_AND_EXECUTION_V1.md)，还须5090 Cursor运行后回传；不改D2/D3标注与数据。

## 2026-10-29：5090真的跑了Qwen，但停在虚构小题，没有D1成绩

指定的RTX5090 32GB已经确认，官方Qwen2.5-7B也按冻结版本加载成功，显存和权重校验都过了。
正式120条还没开始。脚本先用5道虚构小题检查模型会不会按规则输出判决。第3题应该判“支持”，模型JSON里的判决却是“矛盾”，虽然它的理由又说两边并不矛盾。
门的规则只看判决是否等于预定答案，所以整次运行停止。另外四题判决正确，同一道题重复生成的原文也一致，因此这不是显卡或随机采样故障。
两个L0条件都没有Recall、误报或弃权率，不能填0，也不能说模型检测能力差。完整原始输出留在5090，不上传Git。
同一目录已经写下硬停文件，不能为了这道题改提示词再跑。下一步等你决定是否维持停止。
[给负责人的阻断说明](../core144/vace_lite/VACE_L0_5090_SYNTHETIC_GATE_BLOCKER_V1.md)。

## 2026-10-29：把数据标注和实验分成两个对话，避免串线

后续本机新对话专门处理D2财务、D3信息安全的数据质量、外部复审及人工标注；原对话继续实验。
新对话不需要重读全部聊天，按[交接入口](../core144/PAPER1_CORE144_D2_D3_DATA_THREAD_HANDOFF_V1.md)和本机私有清单恢复即可。
但分工不代表数据已经验收：D2还剩两个修复后的HN要原GPT/豆包会话定向复审，D3两个“本应需双证据却能单证据反驳”的问题仍需你决定。
目前不发D2/D3 Human工作簿、不冻结GT、不因D1实验好坏改D2/D3。R4_CODEX仍只是代码名，实际是豆包。
原实验5090已回传合成门硬停，见上方，没有D1分数。数据线不改它的源码/参数，也不启动新实验。
如果两个对话同用一个目录，提交和共享总账更新要错开，不能把彼此未提交文件一起提交或覆盖。

## 2026-10-29：交给5090上的Cursor连续跑，睡前只传一个私有ZIP

代码现在包含完整入口：先核设备/模型/预算，再做虚构合成门，通过后跑F5和人工证据Oracle各120条，
所有原始输出先锁定，再独立读标签评分并生成不含模型权重的回传包。你不用逐阶段守着确认。
但“不要阻断”不能变成硬件错误、超24GiB或合成质量失败还强跑；这些会保存日志后停，普通JSON失败则记弃权继续整批。
私有样本、证据和标签不能上传Git，因此还需把约2.2MB的V2 ZIP传给5090，再粘贴[Cursor执行指令](../core144/vace_lite/L0_5090_CURSOR_EXECUTION_PACKAGE_V1.md)。
脚本能续跑未完成条目，不会为追高分重跑已完成结果或改prompt；最终只做D1开发诊断，不动D2/D3或正式GT。
目前只在LOCAL完成CPU工程测试，尚未在5090加载模型。旧5060阻断事实保留，不能把交接就绪说成实验已完成。

## 2026-10-28：强模型基线已批准，但本次打开的机器只有5060，尚不能运行

你批准的下一步是同一Qwen2.5-7B对照“独立Top5证据”和“人工预匹配证据”，不是继续修规则追分。
但本执行机只显示RTX5060 8GB，和指定RTX5090 32GB不符。按你要求，设备预检未通过就停止，
没有先下载十几GB模型、安装依赖或在别的卡上强跑；也没有静默改成量化模型/CPU或控制另一台机器。
目前两个L0条件都未运行，没有检测率；不能把未测量填0，更不能说模型失败。
请明确5090所在的任务/项目入口后再恢复原实验。原科学目标和24GiB上限仍有效，不需重做D1仲裁。
原40组120条/8组24条HOLD、Human、D2/D3、Guide与Evidence均保持。
[具体阻断、选项与恢复条件](../core144/vace_lite/VACE_L0_HARDWARE_PREFLIGHT_BLOCKER_V1.md)。

## 2026-10-28：VACE-F5终于实跑，但95%弃权说明规则还不足以承担事实核验

这轮不是新设计稿：同一批签署的40组120条上，真的运行了自适应V03和固定流程NA两个条件。
两者S1只检出1/12、S2检出4/15、S3检出1/13，总Recall15%。HN误报虽为0，但40个HN和40个Clean全部弃权，
正常知识没有一条被系统确认为支持，所以不能把“没误报”当成“能正确保留正常知识”。
系统只成功证明一种内部矛盾、四个公布机关错误和一个版本比较方向错误。它们有原文证书，
不是A0关键词命中；但严格的小语法没能解析其余事实，114/120条要复核。自适应与固定流程准确性相同，成本只差少量操作。
34个漏检中30个参考证据已经检索到，不能主要怪缺证，更不能直接认定上长上下文就能解决。
下一步更值得先做冻结中文NLI/LLM同证据强基线和槽位覆盖检查，判断真实瓶颈；这里只建议，没有启动或下载模型。
原8组24条继续HOLD，D1仍是开发集，不修改任何D1/D2/D3样本、人工答案、Guide或Evidence，不执行正式切分。
[真实效果与区间](../core144/vace_lite/VACE_V03_IMPLEMENTATION_AND_TEST_RECORD.md)、
[为什么不先扩数据](../core144/vace_lite/VACE_V03_NEXT_RESEARCH_DECISION.md)。
本轮完成后停Owner审阅，不宣称正式论文效果、方法优越性或生产有效性；下方设计稿记录保留为历史。

## 2026-10-28：V0.3先证明内部冲突，再按证据缺口补证；本轮只设计

你提出的自适应方向已整理成四份候选稿，不再要求所有文本经过同一个SEPT分类器，也不做A0 OR B1。
第一步是同对象、同时间、同条件下的真正互斥证明；A0只提醒检查，“没发现文内矛盾”不等于安全。
未证实的候选进入官方证据检索，再按缺版本、缺机关角色或缺联合前提选择模块；已充分就停，
预算内仍缺证就INSUFFICIENT转复核，不把未知直接判成Poison/Clean。

本轮特别区分：V0.2本来就是六槽位核验候选，不是B1分类器；V0.3新增明确的路由、证明和成本合同。
先设计固定Top5的公平对照，再另列扩池比较，避免用更多证据制造“自适应更好”的假象。
A0在S1的12次命中加B1的S2/S3检出得到的75%只是用了正确S标签的事后拼接，绝非V0.3实测。
现在所有V0.3检出率、误报率、弃权和成本都未知，没有运行模型或新检测。

[Owner审阅包](../core144/vace_lite/VACE_V03_OWNER_REVIEW_PACKET.md)，
[方法规格](../core144/vace_lite/VACE_LITE_V03_ADAPTIVE_METHOD_SPEC.md)，
[比较](../core144/vace_lite/VACE_V02_V03_COMPARISON.md)，
[评价计划](../core144/vace_lite/VACE_V03_ABLATION_AND_EVALUATION_PLAN.md)。
PODR-148/OR-102/REL-2026-0117；正式科研合同/Research Plan Authority/原题/人工/证据和D2/D3均不改。
本轮停VACE_LITE_V03_OWNER_REVIEW_REQUIRED，等待你审阅，不自动实施。

## 2026-10-28：S1正则就能识别，下一步不能把这部分当方法创新

按你的简化要求，我们先只做了两个无训练对照，仍是已签的40组120条，没有动题或标签。
评委原三句式检出S1全部12条，但S2为0/15、S3为4/13；总Recall40%，HN误报7.5%，Precision84.21%。
通用六类线索总Recall45%，HN误报12.5%、Clean误报15%，扩大词表并不等于会核验事实。
S1组内HN误报还有2/12；12个S1中4个只因“同一”命中，不能说正则理解了矛盾。
因此S1有明显构造句式捷径，不把这部分当VACE核心贡献；原数据和合法HN均保留。

VACE-Lite候选只做六槽位：谁、什么关系、多少/单位、什么条件例外、哪个时间版本、什么机关角色。
先独立找证据，再按同主体/范围/版本对齐，不能确定就INSUFFICIENT转人工复核，而非自动判毒/判安全。
第一版不GNN、不强制长上下文、不训练新模型；当前样本是40–68字的短命题，不宣称长文档检测。
将来必须与同Top5证据的直接LLM/NLI强基线L0比较，收益只能来自真实降低合法HN误报及保持Recall。
[结果与材料入口](../core144/PAPER1_VACE_LITE_R1_RECORD_V1.md)，
[候选方法](../core144/vace_lite/VACE_LITE_V02_METHOD_SPEC.md)，[评价计划](../core144/vace_lite/VACE_LITE_BASELINE_AND_EVALUATION_PLAN.md)。
PODR-147/OR-101/REL-2026-0116；本轮停在V0.2 Owner审阅，不启动实施、D2/D3或正式评测。

## 2026-10-28：终于得到真实检出率，但当前轻量多视角实现还不够可靠

你已完成三项确认、署名和日期，原模板只有五处变化。40个完整三元组（120条）正式用于
本轮开发评价，8组24条继续暂扣；这不是正式GT。我们重新跑了13个事实家族隔离折，
四条件各120条新预测，旧126条隔离分数完全未用。

事前指定主报告B1：S1检出2/12（16.67%），S2为8/15（53.33%），S3为10/13（76.92%）。
总体20/40（50%），但合法HN误报15/40（37.5%），Clean误报45%，整体AUROC只有0.5306。
不能只说“S3检出率不错”：当前浅层多视角实现还没有可信的实用区分度。
文本基线AUROC0.6836、HN误报17.5%，本轮点估计更好，但都不是正式泛化比较。

同18列非Oracle/Oracle的总Recall52.5%→57.5%，S3反而84.62%→76.92%；
S3两份参考证据12/13已经同时召回，说明不能只怪缺第二份证据。Oracle条件仍用浅层表示，
不能直接说是大模型推理不行，更不能据此承诺长上下文能解决。
建议先查“主体—条件—数值—版本”是否被正确表示，再决定扩数据和新模型；没有启动下一任务。
[完整结果、区间、失败与复现入口](../core144/PAPER1_D1_FIRST_DETECTION_RESULTS_RECORD_V1.md)，
[并行状态V21](../core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V21.md)。
PODR-146/OR-100/REL-2026-0115；D1_DEV_EXPOSED，D2/D3不变，正式GT/划分/校准/Stage B均未执行。
下方未签表等是历史，原件和失败过程保留，不需要再重做54条。

## 2026-10-27：首轮检测任务停在未签表，不输出假检出率

已只读检查：三项确认、Owner署名和日期仍为空，文件与刚交付的未签模板字节一致。
因此没有开始四条件训练，也没有S1/S2/S3检测率。请按[最简待办](../core144/PAPER1_D1_FIRST_RESULTS_SIGNATURE_TODO_V1.md)
填C13/C14/C15、C17和G17，另存返回，不需要重做54条。
本轮已批准不含时间T的18维开发消融，后续非Oracle/Oracle可用相同18列比较；
它不替换原21维方法，也不替代数据签署与逐折检查。旧Oracle21仍阻断。
PODR-145/OR-099/REL-2026-0114；40/120仍是建议、8/24继续暂扣，未改数据或正式GT/划分。

## 2026-10-27：不用重做54条，先签较小开发集；检索与特征已经接通

三份AI辅助材料已完整核验，55项建议不是自动生效的真值。我们按原规则和同题证据
重新审查、扫描全部144题，建议保留40个完整三元组（120条），8组三元组继续暂扣。
0028两格不强行填；0038范围前提不明等问题不为凑数量放宽。新增中文表只需你批量确认
“40组集合、适用规则建议、8组隔离”并署名，不要求54条全部再次人工仲裁。
另18个历史范围表述建议不改变真假，仍在待签表中独立展示。

“代码存在但D1没有特征”的工程缺口已推进：33份去重官方文档、144题自主检索，
非Oracle与人工匹配证据条件各生成21列。前者不偷看哪两份是人工答案，后者只作上界诊断。
物化不等于检测有效：没有训练这轮分类器，也没有S1/S2/S3检出率或误报率。
签署前有效评价仍0组0条，未知不是检出率0%。

另有真实新限制：Oracle条件留出某个事实家族时，三个时间特征在训练部分全空，
既定填补策略无法工作；不能偷偷填零或只删Oracle列。冻结Dense模型还会把长文档截至128 tokens，
但尚未证明必要事实被截掉，不能立刻改研究路线去做长上下文。
先确认数据资格，再单独闭合可比模型预检；增加同类数据也不能自动修好这些输入/测量问题。
[本轮记录与文件身份](../core144/PAPER1_D1_QUALITY_AND_SEPT_MATERIALIZATION_RECORD_V1.md)，
[最新状态V19](../core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V19.md)。
D1只是已开发暴露的诊断集；D2/D3、正式真值和正式划分不变。PODR-144/OR-098/REL-2026-0113。

## 2026-10-27：D1探索诊断先停在“还不能可靠测”，不是模型检出率为零

你批准我们先用D1回答方法是否有希望。这次三份AI辅助复核材料都已真正导入，
55个字段有建议、2个仍空；它们只是复核建议，不自动变成正式人工真值。
原来五条暂扣题之外，先发现一条省略关键条件的范围疑点，后来又发现两条与既有
双机关公布问题相同的边界。按相同质量标准整组三元组暂扣，共8组24条；
剩40组120条只是待审上限，不是已经能拿来算准确率的合格数据。

必须如实记录一次执行问题：文本基线在126条初步准入题上已生成家族隔离的预备分数，
后续才发现上述两个漏项，说明首次拟合前质量预检没有真正完成。
分数原件保留但隔离，不报检出率、不挑分数好看的题、不换样本重跑。
因此本轮有效评价是0组0条，S1/S2/S3检出率、误报和置信区间都未知，不能写0%。

多视角的代码存在，但原有矩阵属于Final72，不是D1。还需把D1可信证据语料、版本表、
独立检索和逐题特征真正接起来，才有条件比较实际系统与人工匹配证据上界。
现在不能判断S3是检索少了一份，还是模型不会推理，也没有证实长上下文能解决问题。
先闭合质量与可测输入，比直接扩同类数据或加上下文更重要。

[本轮结果、排除分布与下一决策](../core144/PAPER1_D1_EXPLORATORY_DETECTION_CLOSEOUT_RECORD_V1.md)，
[并行状态V18](../core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V18.md)。
D1现在明确为开发暴露数据，不可再宣称未来独立未见测试；正式Core划分和GT没有执行。
D2/D3原题与证据不动、原门不动，原工作簿和原答都没改。
下一步是Owner有界关闭语义/材料缺口，之后才恢复D1实验，不是自动开始新训练。

2026-10-27续接：10月16日这轮D2审查及修复记录已重新核对，继续完成材料交接和提交。
仍只需原D2两会话复审两条新题；没有新返回，不把文档收口等同整个D2验收通过。

## 2026-10-16：D2不用全量重审，但两条原HN确实要修后复核

先不看样本角色，我们按冻结条文逐项审了37个旧建议：37项可接受，共42格；
三条版本意见按旧规则执行，银行条文也已完整支持。实际阅读哪份证据是个人过程，
不为了两模型一致而改成一个“标准答案”。这份QA不是人工GT。
会议记录没给证据，只能说这项附加主张不能确认；不能说记录不存在。
它不传染给已经有令文支持的国务院通过/公布机关。另一条“其他服务6%”范围确实过宽。

这些判断先封存，然后才看两条原设计，结果都是合法困难负例Hard Negative，
不是故意污染句。因此不能用“本来就是Poison”解释错误，也不能把它们原样发给人。
本次按你已授权的条件各做一处最小修复：补齐法定排除范围、把附加载体改为原令可见的信息。
原句、原答和证据都保留，新版本/新题号；不动其余142条、污染机制和证据路径。
现在只需原D2 GPT/豆包会话分别审这两条Phase1，再锁定后审Phase2，不必重做144条。
完整域验收还没PASS，Human Excel没有提前生成。D1仲裁和D3原门继续独立等待。

[本轮结果与发放入口](../core144/PAPER1_CORE144_D2_OWNER_QA_AND_TWO_HN_REPAIR_RECORD_V1.md)，
[并行状态V17](../core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V17.md)。
PODR-142/OR-096/REL-2026-0111；无GT、切分或训练。

## 2026-10-16：54条已逐条审完，等你在仲裁表里做最终决定

本轮只按你批准的范围审54条，没有让两人重做144题。原题、两人Excel和原答都不动。
已有规则能解释不少差异，例如数字比较错不代表版次错，没写机关名字也可能有机关关系主张。
但两人相同也不保证正确：六条共同的历史比较/历史适用范围建议再审总体状态，另有一条
旧数字转录不清。34条共47格给了作者建议；新仲裁表57个字段最终值均留空，仍由你裁决。
最先看四条：0051没给第十条；0121旧数字OCR成“九卡夭”；0078/0116说两个机关同时
公布，不应先验当成A与非A。两条材料缺口不能用别题补，两个角色问题也不能机械用ZERO。
24条引用/实际阅读线索已审，几条还把机关写反或理由末句写反；只建议追加正确理由，
不假装知道标注人实际读过哪份证据。[材料与中文使用说明入口](../core144/PAPER1_CORE144_D1_BOUNDED54_REVIEW_AND_OWNER_PREP_RECORD_V1.md)。
你可填新表黄色Owner列或按comparison_id逐条回复。现在不是仲裁已完成，更不是GT。
没有补搜、改规则、发真人复核、切分训练或放行D2/D3。下方“等批准54条审查”保留为历史。

## 2026-10-16：D1两位真人答案已经比较，下一步不必全量重标

你已批准A01本次123格首尾空白例外，原件不改。现在144条按完整题文一对一匹配，
各自题号与顺序保持，双方看到的E1/E2也一致。没有按不同盲号或Excel行号硬凑。
Phase2七个语义分类字段共964/1008一致（95.6349%）；31条至少有一项不同，另21条
只差实际看了哪份证据。看证据过程允许不同，不能为一致率把它改成相同。
Phase1还有三条分歧，其中两条文内冲突会影响minimum，要一起审，不机械改字段。
把这些分歧与单份质量反馈去重后是54条待审：31+1+22，而不是54条已经判错。
A两条/B一条反馈缺证据，B24条理由与selection需核对；不能据此直接宣布题坏。
[结果与Owner-only清单入口](../core144/PAPER1_CORE144_D1_HUMAN_AB_COMPARISON_RECORD_V1.md)。原答完整保留，未仲裁、未造GT。
建议下一步单独批准按现有规则有界审54条、准备你的仲裁材料，不要求两人重做144。
D2/D3的原阻断/真人门不变，不能用本轮比较放行它们。

## 2026-10-16：D1两位真人第二阶段回收，先保原件再检查

你确认同一位A、B独立完成自己的两个阶段，只用获准证据、不看对方答案、不新增
搜索或用AI，接收后未改原件。这是人工证明，不假称机器证明。两份Excel先锁原
字节，再查各144条题号/题序/题文/选项/理由：全部完整，没有minimum机械违规。
A有123格只读证据文字首尾空格/换行不同，逐格确认无实质文字变化；B仅空白存储
形式不同。不能悄悄去空格后宣称精确一致。建议你仅批本次123格“呈现等价”，
完整留审计、原件不动，再比A/B；不要求真人为此重标144题，文件例外不等于认可答案。
另有A两题/B一题反馈证据不足，B有24题理由与实际证据选择需核对。这些是待审
线索，不是已判题坏；未跨人合并、算一致率或造GT。
[检查与下一步](../core144/PAPER1_CORE144_D1_HUMAN_PHASE2_RAW_LOCK_AND_RECEIPT_GATE_V1.md)。D2/D3原阻断/真人禁发不变，等你的有界决定。

## 2026-10-16：定向六条收到了，但“格式对”还不等于“可以给真人”

两份下载原件各6条已原样锁定。题号、顺序、字段、英文选项和理由都通过，
没有清洗、排序或改写。Reviewer说仍是原D2隔离会话，我们保留这份转述声明，
不把它当平台日志证明，也不要求你再去重存文件。

补回的两处条文现在都能支持对应事实；两条罚款理由也不再把一般20万上限
和严重100万上限混用。这些是修复带来的实际进展，旧答仍保留。
三项版本栏仍没按已有规则执行：修改决定、明确修订身份、生效转换都算版本
主张，不需要为这些再写V4.4。我们给出本地建议，不静默改Reviewer原答。

还有两件不能放过：材料只说会议通过，却没证明“会议记录里载有通过事项”；
税法的6%有明确排除，不能把除交通运输外所有服务都概括成6%。前者缺证据
不等于现实中一定假；后者是否属于构造缺陷还要看设计合同，不能为了求一致
直接把题改成正确。现在需要Owner有界裁决，必要修题必须另批。

[六条原答、依据与Owner门](../core144/PAPER1_CORE144_D2_TARGETED6_PHASE2_RAW_LOCK_AND_QA_GATE_V1.md)。
此前37项本地建议仍未自动成为你的仲裁。D2真人包继续暂扣，D1/D3门不变。
本轮不改题、不补证据、不改说明书、不造GT，也不再自动让R3/R4重复同样复核。

## 2026-10-15：只补两份证据说明，不改题；43项审查后只请复核6条

你批准后，我们从原冻结正文补回银行监管法第二条、支付条例第八条的完整条文，
包括条件与例外。没有补搜网站，没有改题、题号、顺序和原答。各144条原样保留，
25份原快照/正文、旧74/18份封存文件复核未变；先前漏正文记录也保留。

43项不是43道坏题。读完双方原答并按旧V4–V4.3逐条审查，37项可以给本地规则
建议：是否提版本先看题文；机关、实体内容和版本分开判；出现过去日期不一定
就是历史版本事实。本地建议不冒充你的最终仲裁，没有写进原答或GT。

另外6项请原会话再看：两条补回证据后重判，一条会议记录载体未被证明，一条
其他服务范围解读不同，还有两条答卷理由把一般罚款上限与严重情形上限混了。
后两条是答卷依据问题，不是题文新增错误。不要给Reviewer标准答案，也不能
用两人一致掩盖证据仍不足。只发每人七件六条包，继续原D2 GPT/豆包会话。
[逐件地址和提示词](../core144/PAPER1_CORE144_D2_TARGETED6_PHASE2_V3_OWNER_SEND_CHECKLIST_V1.md)，
[审查记录](../core144/PAPER1_CORE144_D2_PHASE2_EXCERPT_V3_BOUNDED43_REVIEW_RECORD_V1.md)。
收到JSON下载原件再锁哈希。现在不能给D2真人发标注表；D1/D3门不变。不产GT、
不切分、不训练。隔离仍按人工确认记录，新的外部复核尚未执行。

## 2026-10-15：财务第二阶段已返回，先修证据呈现问题，再谈人工发放

两份原答都收到了，先锁原字节与哈希，再核对各144条题号、顺序、字段、英文选项
和理由。格式全部通过，原答没有清洗、重排或改写。隔离登记为你的人工确认，
不是平台日志证明；R4仍是豆包的历史代码。

分类比较有42条需看事实/版本等判断，另15条仅实际证据选择不同。两个人可以
用了不同数量证据却作同一事实判断，所以不能把所有差异都算题错或按票数改答案。
版本字段分歧最多29格；需要按已有V4–V4.3逐条核查，不马上重写说明书。

这里必须补一条更正：两人共同报出的两条缺证据，确实是我们发放摘录的问题。
银行业监督管理法第二条、非银行支付机构条例第八条在原冻结全文里都有，却没进
V2摘录。之前只验证了登记锚点和条文区间，漏掉了两条补充命题的正文需求。
不是Reviewer没有查资料，更不能让他们上网补答案。旧包、旧PASS记录和原答
保留，追加说明，不静默覆盖。还有一条“国务院常务会议记录”载体说法待审。

分类分歧与质量提醒合并后共43条Owner审查项，不是43条确定缺陷。
[原答/结果](../core144/PAPER1_CORE144_D2_PHASE2_RAW_LOCK_AND_COMPARISON_RECORD_V1.md)，
[有界修复与审查待决定](../core144/PAPER1_CORE144_D2_PHASE2_EVIDENCE_AND_REVIEW_BLOCKER_V1.md)。
现在不能给财务真人发标注表。本轮只保全和核查，没有重做V3或改题改答。
D3仍等自己的两项决定；D1真人门不变，没有读取他们答案。无GT、切分、训练。
[状态V11](../core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V11.md)分别保存各条线。

## 2026-10-07：财务可发第二阶段，信息安全先停两条设计缺陷

你批准准备后，我们从所有旧题到新题的记录重新合出两个领域各144题，没有拿
最初题包直接复用。每人的第一阶段回答仍是他自己的回答，自然度8/18处轻微
差异没有投票统一；这只是质量通过，不是标准答案。

这次重点不是“官网链接能打开”，而是冻结证据能否支持实际判断、最少需要
几份证据。25/24份使用来源的快照和正文哈希全部正常，修题也没有偷偷换证据。
但信息安全两条写成“单独机关”“同一对部门联合”：其中一份官方公布文本
就能否定这类绝对说法，原定多证据关系不成立。不能裁掉反证，也不能强改成MULTI。
D3暂不发，等你决定是否有界修这两条；没有改题或规则。

你允许财务使用可追溯摘录，仍完整144题、不拆96+48。摘录保留完整相关条文、
条件/例外上下文和身份/版本/机关原文，并保留原全文哈希、字符区间和摘录哈希。
财务包降至约309KB，证据正文8.3万字；本地完整核验通过，但还没有平台上下文
或输出容量实测。提示词要求读不全/输出不全就停报，不交部分答卷。

[结果与私有证据入口](../core144/PAPER1_CORE144_D2_D3_PHASE2_PREFLIGHT_AND_RELEASE_RECORD_V1.md)，
[逐人七件绝对地址清单](../core144/PAPER1_CORE144_D2_D3_PHASE2_OWNER_SEND_CHECKLIST_V1.md)，
[D3两项待决定](../core144/PAPER1_CORE144_D3_PHASE2_S3_NECESSITY_BLOCKER_V1.md)。
现在只发财务两位原会话：自己的题包/提示词/Schema和四份Guide；R4代码仍是豆包，
不需要新建Codex任务。不要发送原答、映射、Owner包、旧题或信息安全草稿。
D1真人A/B原有门不受影响，本轮没有读取他们答案，没有生成D2/D3人工Excel、
GT、正式切分或模型。允许发不等于已发；[状态V10](../core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V10.md)
分别保存三条工作线。

## 2026-10-06：B的第一阶段原件通过核验，可以单独进入第二阶段

这次收到的是B自己的正确答卷，不是上次两人都填写A表的那两份。原文件不
重存、不改答案，先保存原字节，再核对144条题号、题序、题文、英文选项及
需要的注释，全部通过。B标了16条文本内冲突，这是合法判断，不是格式错误。
这里只核验填写结构，没有拿A的答案、构造答案或Expected来给B改分。

第二阶段仍用原来准备好的B Excel：题号、顺序与第一阶段一一对应，答案格
全部空白。既有规则是各人通过自己的第一阶段门即可继续，所以B无需等A。
[锁定与门控](../core144/PAPER1_CORE144_D1_HUMAN_B01_PHASE1_RAW_LOCK_AND_PHASE2_RELEASE_V1.md)
和[精确发放清单](../core144/PAPER1_CORE144_D1_HUMAN_B01_PHASE2_OWNER_SEND_CHECKLIST_V1.md)
列明两件文件：B第二阶段Excel＋已有详细中文指南。说明书不用再生成新版本。
现在“允许发”不等于“已经发”，请Owner发给同一位B标注人，不能给A或AI。
收回第二阶段时也先锁原件，不替标注人重存。A的已有门不变；D2/D3第二阶段
仍待单独批准准备。本轮没有A/B仲裁、GT、切分或训练。
[状态V9](../core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V9.md)保存各条工作线。

## 2026-10-06：四项复核已收口，第二阶段仍需你批准准备

财务两人各3题、信息安全两人各1题的新原答已收到，先按原文件锁字节和哈希，
再核对题号、顺序、字段和选项。五个分类字段全部一致。两个上限明确指2024端点，
循环解释已经消失，人脸题两句现在都明确说同一办法在同一条件下的规范要求。
人脸题的文内矛盾保留，两人自然度仍判正常；没有为了答案一致再修改文本。
[原件、逐项判断和QA门](../core144/PAPER1_CORE144_D2_D3_BOUNDED4_PHASE1_V2_RAW_LOCK_AND_QA_RECORD_V1.md)，
[当前状态V8](../core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V8.md)。
各领域完整144题视图只接入这次新版本答案，财务8处、信息安全18处既有轻微自然度
差异仍原样保留，不靠投票强行统一。这是第一阶段文本质量通过，不是事实验收或GT。
财务两份文件字节一样；不能因此证明独立或互抄，隔离只记你的人工确认。
R4-codex仍是历史代码，实际为豆包。两域第二阶段本轮没有生成或发放，下一步需
你批准准备Phase2题包及发放前核验。D1真人个人流程不变；不启动D2/D3真人、GT、
切分或训练。四份原件和历史版本完整保留；下方待复审描述是历史，不再是当前状态。

## 2026-10-05：Owner只批准再修4题，发回各领域原会话，不重新做全量

本轮只修财务3题、信息安全1题。两句“该上限”明确指2024年修改后的上限；
机关比较题删掉没有增加事实的循环解释；人脸题明确第二句也在说同一办法的
规范要求，而非现实中有人违规限制。没有补入新金额或机关，也没扩充证据。
旧题和两人的原答案保留，新题用新的版本和题号，不能套用旧答案为新题作答。

[修复、证据路径核验与复审说明](../core144/PAPER1_CORE144_D2_D3_BOUNDED4_REPAIR_RECORD_V1.md)，
[当前并行状态V7](../core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V7.md)。
完整领域仍各144题，只改3题/1题；事实原子、证据、查询、家族和填写规则不变。
本机检查通过只说明可以送独立复审，不说明新题已被两人接受。
现在给原D2 R3、原D2 R4豆包各3题，原D3 R3、原D3 R4豆包各1题。
每人只发自己的题包、Schema和提示词，共三件；私有Owner清单列了逐件绝对地址。
**这次不要新建会话，不混用财务和信息安全，不发旧答案、Owner包或证据。**
两域第二阶段仍不发，等四份新JSON原件回收后先锁字节再核验。
D1真人流程仍按已有个人门进行；没有新Human D2/D3、GT、切分或训练。
下方“修复未批准”是本次批准之前的历史，不是当前下一步。


## 2026-10-05：复审答卷格式通过，但4处文本边界还不能带进第二阶段

我们已原样保存财务25题、信息安全32题的两人定向返回。题号、题序、字段和注释
都通过，不需要重新交文件。Owner确认还是各领域原来的隔离会话，豆包继续使用
R4_CODEX代码；这份隔离记录是人工证明，不是机器日志。

“自然/稍生硬”的7处新增差异不影响核心理解，保留不同答案，不为一致而改题。
信息安全中15处双方都看到的文内矛盾也不因此判成题目缺陷。
但财务的两句“该上限”前面各有两个上限，是否唯一指向尚需决定；还有一句循环
解释“原始通过机关”的比较口径，可能是未完全消除的说明旁白。
人脸验证那题已写明存在替代方式，但“仍只能使用”可以理解为现实中受到限制。
规范不允许某行为，与现实有人违反规范，是可以同时成立的；只有两句同在说
规范要求，才构成直接逻辑冲突。这不是把R3或R4整份答案选为正确，也不是改Guide。

[当前四项门控、原件索引及下一步](../core144/PAPER1_CORE144_D2_D3_TARGETED_PHASE1_LOCK_AND_GATE_V1.md)。
建议Owner批准只处理D2三题、D3一题的最小表达修复，然后在原会话定向重审；
也可逐条给出有依据的保留决定。现在没有执行新修复，两域Phase2都暂不发。
各144题合并视图只为方便追溯，不是最终接受答案，更不是GT。
D1人工流程不受影响；本轮没有新Human D2/D3、Expected、真值、切分或模型训练。

## 2026-10-03：不为追求两位 AI 一致而改题，只修真实缺口和已知表面捷径

这轮处理的是 D2 财务和 D3 信息安全的外部 Phase1 质量检查，不是真人标注，
也不产生答案真值。两人对“自然还是稍显生硬”的纯偏好可以保留不同答案；
但题目缺少必要对象、范围或条件，或者反复用某类解说词暗示题目角色，就要修。
我们按冻结字段定义逐条看62条记录：43条需要修复，19条仅自然度差异而不改。
再审查两域完整288题，发现另14条同类表面风险。最终只重审 D2 25题、D3 32题，
不重新让外部模型做两个领域的全量144题。

人脸验证那条题，原文“拒绝”并不能推出“存在替代方式”。新版本在第二个命题
明确同一人已具有第一句所说的替代验证方式，再陈述只能使用人脸的限制。
这是补回设计条件、保留单一矛盾，不是宣布旧题的 YES 答案正确。
缺失的所得类别、文件名称和必要范围只从已有冻结证据补回；比较型题不直接
把两个版本的真实端点都写进题目，以免改变原证据需求路径。

所有旧题、旧答、历史构造记录都保留。事实核心、角色、HKP、证据路径、S和家族
不变；本机复核通过只表示构造侧没有发现额外问题，不代替独立盲审。
[逐条理由、10条自包含修复和49条重叠表面风险ID索引](../core144/PAPER1_CORE144_D2_D3_PHASE1_OWNER_TRIAGE_RECORD_V1.md)。
四份题包必须发回各域原来的 R3 GPT / R4_CODEX 豆包会话，D2/D3不能混用。
每个会话只收题包、Schema、提示词；不发本总账、原答或私有映射。四份定向原答
回收并锁定之前，两域 Phase2 都不发；不发 Human D2/D3，不生成 GT、不切分、不训练。
D1 Human 的已有个人门控不受本轮影响。


## 2026-10-03：D2/D3 外部答卷已回收，先处理文本问题再发证据

财务和信息安全各两份144条答卷已原样保存，题号、题序、字段、枚举和必需注释全部通过。Owner确认全新隔离会话，只登记为人工证明，R4实际模型仍是豆包。两人分类并非完全一致：D2有22条、D3有30条分歧，还要处理双方共同指出的质量问题。D3包括文件名称/人数范围未交代，以及“另一句”“后句”等评论句子本身的写法；D2的“这里比较”“比较不包含”须区分必要事实范围和出题过程说明，不能一律算缺陷。

私有 Owner 包列有 D2 29条、D3 33条原题和两人原注释。[核验、问题边界和下一步](../core144/PAPER1_CORE144_D2_D3_PHASE1_RAW_LOCK_AND_GATE_V1.md)。D3一题前句说“可替代时”不得唯一用人脸验证，后句只说该人拒绝，没有交代存在替代方式，因此不能确认条件相同。两域第二阶段暂扣；Owner逐项决定真实缺陷的版本化修复与偏好差异的保留理由，再做必要的定向盲审。本轮原答、题文和协议未改，未用隐藏角色或正确答案裁判 Reviewer。此次仍是出题质量检查，尚无 Human GT、正式切分或模型结果。

## 2026-10-02：A01 第一阶段原件已锁定，可以只给 A01 发第二阶段

Owner 已确认文件名带 `(2)` 的工作簿才是真正 HUMAN-A01 第一阶段返回。我们没有用 Excel 重存它，而是按原始字节复制到新的只读证据目录；36,361 字节，SHA256 为 `d752d27451fcbae9ffba82b6bb33445452ef8b51e35f68877793687216f21b28`。144 条 A01 题号、题序和题文与原发放件一致，五列选项都合法；15 条非默认判断均有说明。文件名带 `(3)` 的另一份工作簿没有被当成 A01 正式原答，也没有删除或覆盖。

A01 自己的第一阶段门已通过，所以现在可以只把[清单中的一份 A01 第二阶段工作簿](../core144/PAPER1_CORE144_D1_HUMAN_A01_PHASE2_OWNER_SEND_CHECKLIST_V1.md)发回同一个 A 标注员。B 正在完成正确的 B01 第一阶段；A 的完成不能解锁 B 的第二阶段。[锁定和技术核验记录](../core144/PAPER1_CORE144_D1_HUMAN_A01_PHASE1_RAW_LOCK_AND_PHASE2_RELEASE_V1.md)。目前没有 A/B 比较、仲裁或 Ground Truth。

## 2026-09-30：财务领域 D2 已完成内部施工，接下来做信息安全 D3

这轮先把 D2 财务领域做成了 48 组、每组三条，共 144 条候选。做法仍是先锁官方材料，再抽取事实和机关/版本关系，最后写候选并逐条核对；不能先编一个“污染答案”再找材料。D2 的内部检查没有发现额外意外错误，已经准备两份只含题目、不同顺序的 144 条第一阶段盲审包，但**尚未交给 R3/R4**。这只是出题方自己的施工质量检查，不能代替独立盲审，更不是 Ground Truth。具体数量、哈希与限制在 [D2 内部检查记录](../core144/PAPER1_CORE144_D2_FINANCE_INTERNAL_CONSTRUCTION_RECORD_V1.md)。

同一项 Owner 批准允许 D2 内部门槛通过后接着做 D3 信息安全领域，不需要先等 D1 人工标注结果。D3 尚未完成，因此四份跨领域包现在不能一起发。D1 的真人第一阶段 Excel 仍只是可发、没有记录已发；第二阶段仍封存。没有 Core GT、正式切分或训练。旧段落所写“D2/D3 尚无候选”是当时的历史状态。

## 2026-09-28：把“没交代对象”和“指代可能指两个对象”分开

Owner 预审后发现，真人可能把“该文件”一律当成指代歧义。其实两列问的是不同问题：`self_containment` 看本条有没有把关键对象和核心命题交代清楚；`ambiguous_referent` 看已经出现的对象里，指代到底指哪一个是否唯一。只有裸“该文件”而没有两个竞争前件，可以是 FLAG / NO；两个文件都命名了但末句指谁不唯一，可以是 PASS / YES。不能由一列自动决定另一列。

本轮在[中文主手册](../core144/PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md)补了2×2决策表、4个明确虚构的案例及理由写法，字段说明、易错表、速查表同步。原30个案例含05/06一字未改，共34例；这只是解释补强，不是重新打开协议或替真人作答。[只读核验和收口](../core144/PAPER1_CORE144_SELF_CONTAINMENT_REFERENT_CLARIFICATION_RECORD_V1.md)确认四份 Excel、字段枚举均原样保留，题文、ID、题序和历史 raw 未改。两位真人仍未发放，第二阶段仍封存；Owner 接下来审阅更新的 Markdown，既有 PDF 没有同步。尚未实测说明补强对分歧或返工的影响。本轮不执行标注、D2/D3 构造、GT、切分或训练，以下同日手册数量是当时历史。

## 2026-09-28：给真人一份能独立使用的完整标注手册

Owner 在真正发给两位标注员之前，认为 Excel 内的简要说明还不足以统一理解，因此本轮只补一份[中文主标注手册](../core144/PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md)。手册把两阶段流程、每列及每个英文值的选择条件、版本和机关边界、最低证据与实际使用的区别、理由写法和自检完整展开，配了30个完全虚构的案例。它不是实际题目的答案表，也没有让模型替真人标注。

核对四份 Excel 后，主手册按当前字段填写体系编写，不把历史 Pilot 的旧列或旧规则带入。候选、证据、ID、题序、规则和四份 Excel 一字未改；第二阶段仍封存，两位真人尚未发放。我们检查的是说明覆盖和可理解性，尚不能声称已经测得人工分歧降低。[检查记录](../core144/PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_QA_RECORD_V1.md)。下一步是 Owner 先审阅这份手册，再决定是否把解释同步回 Excel、何时发自己的第一阶段工作簿；本轮不启动标注或 D2/D3 构造。

## 2026-09-27：D1 的144条题目已过施工验收，真人说明书和答卷已备好

这一步把 D1 从“机器/外部盲审帮助我们找候选质量问题”推进到“可以让两位真正的人独立标注”。R3 与 R4（代码名仍为 R4-codex，实际豆包）各自完成剩余90条第二阶段审阅；两份原始答案一字不改地锁定。两人对核心事实冲突均判出30条；有7条候选、9个语义字段的边界理解不同，按之前已经接受的 V4–V4.3 规则逐条审过并另记覆盖，不是为了迎合预期答案而改原答。另有12条“我实际用了 E1/E2 哪些证据”的差异，这是各人阅读过程不同，保留即可，不假造统一真值。

把最初 Canary 24 条、第一批30条和剩余90条合起来后，D1 共48组、144条，预人工标注质量门通过。我们给 HUMAN-A01 与 HUMAN-B01 各自制作了整域144条的 Excel：题序和不透明 ID 不同，字段解释、易错边界、填写流程和虚构例子都在文件内。第一阶段只看文本；两人的第一阶段现在是“可发”，**不是已经发了**。第二阶段虽然已预建并附冻结官方证据，但要等每个人自己的第一阶段原件交回、锁定、校验后才给他本人。[Owner 发放清单](../core144/PAPER1_CORE144_D1_HUMAN_PHASE1_GUIDE_V1.md)与[Excel 检查记录](../core144/PAPER1_CORE144_D1_HUMAN_XLSX_USABILITY_AUDIT_V1.md)列有具体路径。

与此同时，D2 财务和 D3 信息安全可以开始从官方证据找事实、锁快照、建版本和候选；不必等 D1 人工交卷。但 D2/D3 绝不能根据 D1 人工答案或模型表现挑“容易做对”的题。[并行总账](../core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V1.md)。现在尚无人工作答，D2/D3 尚无新候选，也没有 Core Ground Truth、正式切分、训练或论文最终效果。下面“待发给 R3/R4”是本日较早历史。

## 2026-09-27：第二阶段90条盲审材料已备好，等 Owner 发给原两位审核员

Owner 已确认四条定向复审确实由原 R3/R4 隔离会话完成（这属于人工证明，不是系统日志证明），并批准只对两个“三份冻结证据”的组，在证明两份已足够回答候选命题后，给审核员呈现指定 E1/E2；第三份仍锁在私有证据档案里。于是我们用86条未改候选和4条新版候选，重新生成了90条 Phase2 盲审题包。给 R3 与 R4 的题目相同，但维持各自原本不同的题序；每条只有本条指定的官方冻结证据，没有类标签、预期答案或构造意图。R4-codex 只是代码名，实际仍是豆包。发放文件和对应提示词请严格按[逐人清单](../formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE2_OWNER_SEND_CHECKLIST_V5.md)交给**原会话**，无需也不能新建第二阶段会话。现在只是“可发给外部盲审”，还没有收到他们的第二阶段答案，更不代表 D1 全48组已验收；真人 A/B、D2/D3、GT、切分、训练仍未开始。[技术验收记录](../formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE2_RELEASE_RECORD_V5.md)。下一节所说“仍待决定”是本日较早的门控历史。

## 2026-09-27：四条修复后盲审通过结构检查；第二阶段仍待证据呈现决定

原来四条候选用了很相似的“两个机关同时公布”说法，可能让模型靠句式猜 Poison。改写后的四条已由原 R3（GPT）和 R4（豆包，代码名仍为 R4-codex）分别复审：两人都读出了四条文本自身的矛盾，都认为文本可独立理解、没有指代歧义或实验模板痕迹。唯一新增分歧只在一条文字是否稍显生硬，Owner 已明确认为不阻断，原答照存，不再改文本或找第三人“投票”。原始 JSON 已按字节锁定；其余86条沿用之前锁定的回答，形成90条第一阶段视图。已识别的四条固定句式不再重复出现，但我们仍保留两个相近词组命中的观察项，不宣称所有外观捷径都绝迹。

第二阶段尚不能发：30组原有证据中有两组各三份官方快照，而审核答卷只提供 E1/E2 两个证据位。已核查23份官方快照的哈希，并列出每组可覆盖命题的两份冻结证据及保留的第三份；是否允许仅在审核员题包中采用这种有界呈现，须 Owner 明确决定。两位审核员本次定向复审的运行隔离也待单独确认。未发真人 A/B，没有 GT、切分或训练。[锁定与门控](../formal240/PAPER1_FORMAL_D1_REMAINING90_TARGETED4_PHASE1_LOCK_AND_GATE_V1.md) · [证据决定说明](../formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE2_EVIDENCE_PROJECTION_DECISION_V1.md)。以下较早的“定向复审待回”是历史状态。

## 2026-09-27：从五领域计划改为三领域 Core144；D1 第二阶段继续暂扣

Owner 已把四条“同一文件同时由两个机关公布”的候选文本内部冲突裁为 YES；六条轻微自然度分歧只记为评审差异，原答都不改。随后封闭审计发现那四条又用了几乎一样的句式，而且只出现在 Poison 中，可能让模型凭写法猜答案。因此本轮只改这四条的表达，不改事实关系和证据，准备给原 R3（GPT）与 R4（代码名 R4-codex、实际为豆包）做四条定向第一阶段复审。现阶段不能把第二阶段90题发出；也没有真人 A/B 标注或 GT。

论文核心数据范围现为 D1 企业人力资源、D2 财务、D3 信息安全，共计划144组/432条。原五领域240组计划保留为历史记录，D4/D5 暂留未来外部扩展。未来可在 D1 真人标注期间并行建设 D2/D3，但必须先完成 D1 机器盲审、全48组质检与真人 Excel 发放准备；目前还没到那一步。[当前 D1 门控](../formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE1_FINAL_GATE_V1.md) · [Core144 范围](../core144/PAPER1_CORE144_SCOPE_DECISION_V1.md)。下面早期“待 Owner 裁决”段落是当时历史快照。

## 2026-09-27：Claude 只看十条争议文本的辅助意见已收到

Claude 的十条原始答卷已原样只读保存，并通过条数、题号、顺序、字段和注释的检查。你人工确认它使用独立盲审会话；这记作 `OWNER_ATTESTED`，不是平台运行日志证明。六条“读起来是否稍别扭”的分歧，Claude 都认为自然，和豆包 R4 一致；四条“同一文件的公布机关同时写成两个机构”的关键分歧，Claude 都认为文字自身矛盾，也和 R4 一致。R3 的轻微表达意见仍是有效原始意见，不会因二比一而被删除。四条矛盾判断需要你最后确认；这些候选还反复使用相似句式，需要再检查是否形成猜答案的外观捷径。详细见[十条原答锁定与分析](../formal240/PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_RAW_LOCK_AND_TRIAGE_V1.md)。第二阶段目前仍不能发；正式人工 A/B、GT、切分和训练都没有开始。下面“Claude 尚未返回”的段落是当时的历史状态。

## 2026-09-27：两位评审的九十条第一阶段答卷已收到，先处理四条关键分歧

你更正了上次误发的 R3 附件：那份隔离事件保留为“误提交”，不代表这次 R3 真正的盲审失败。新的 R3 原答和 R4 豆包原答已经原样只读保存；我们没有改动任何答卷。两份文件各有 90 条，题号、顺序、字段、取值和需要说明的注释均合规。两人在自然度上有六条轻微分歧，在“文字自己是否自相矛盾”上有四条重要分歧；后者都涉及同一文件被同时写成由两个不同机关公布。其他三项文字质量字段完全一致。机械检查通过不等于这些判断已经统一，也不等于数据已经准许进入第二阶段。

按你的提议，已做一份只含这十条候选文字的[Claude 独立辅助盲审包和准确发件清单](../formal240/PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_OWNER_SEND_CHECKLIST_V1.md)。不向 Claude 展示两人的旧答案、隐藏角色或证据。Claude 的意见帮助你判断分歧，但不会自动覆盖原答或代替你最终裁决。[原始锁定与分歧记录](../formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE1_R3_R4_RAW_LOCK_QA_AND_R5_AUXILIARY_V1.md)。第二阶段、正式真人 A/B、GT、切分和训练继续暂扣。下方“尚未收到答卷”的文字是上一时点历史记录。

## 2026-09-27：R4 名字不改，但分发说明按实际豆包环境改正

Owner 澄清：我们一直称为 `R4-codex` 的是审核员**编号**，不是使用了 Codex 软件；这位评审以前实际用的是豆包，后续也仍用豆包。因此九十条题目、题号、顺序和旧答卷一个字都不改，只把给 R4 的“必须新建 Codex projectless 任务”误导性说明改成“新建隔离的豆包会话”。R3 的文件不变。请按[新版逐人完整路径清单](../formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE1_REVIEWER_FILE_CHECKLIST_V2.md)发件，尤其不要再发 R4 旧提示词。历史文档中的平台说法有[追加勘误](../formal240/PAPER1_FORMAL_D1_R4_CODEX_DOUBAO_PROVIDER_PROVENANCE_ERRATUM_V1.md)，并非改动历史原件。当前仍在等两人第一阶段九十条原始返回；Phase2、真人 A/B、Ground Truth、切分和训练都没有放行。以下旧 Codex 运行说明是当时记录，不能再用于发件。

## 2026-09-27：后面 90 条完成内部准备，等你一次性送两位独立评审

HKP2、HKP3、HKP4 各十组、三十条都已按“先锁官方材料、核事实和来源，再写候选文本”的顺序完成构造侧检查。把三批合在一起检查时，我们发现某些错误文本反复使用“没有变化”一类措辞，可能让评审仅凭语言形式猜角色；因此保留旧稿，追加两轮修复，再次核对九十条。现在三类候选各三十条、共同查询与上游信号输入的机械检查通过，外部评审仍需独立发现我们可能漏掉的真实题目或证据问题。这里的“通过”只表示**可以送预标注盲审**，不是 D1 完整验收，更不是真人标签。

这次不再按 HKP2、HKP3、HKP4 分三轮打扰你，而是给 R3、R4 各一份打乱顺序的九十条第一阶段题包。两人只看候选文字，不看证据或隐藏角色。请严格按[逐人文件清单](../formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE1_REVIEWER_FILE_CHECKLIST_V1.md)发送：R3 用全新独立 GPT 会话；R4 用**全新 projectless 空目录 Codex 任务**，不是“新建 Codex Project”。之前你批准的新 Project 例外仅限 HKP1 第一批，本次不能沿用。收到两份原始文件后我们先锁字节、查字段、核缺陷；只有第一阶段关口通过才会给同一两位评审第二阶段材料。真人 A/B、Ground Truth、正式切分和训练仍未启动。旧的“剩余90条待内部构造”段落是历史快照。

## 2026-09-27：第一批 30 条盲审收口；后面 90 条改为一次大批量送审

R3、R4 的第二阶段原始答卷已分别逐字节保存并核对：两人各答 30 条，题号、顺序、字段和值都合规。对“事实是否成立”、证据是否足够、是否有意外第二错误等关键安全问题，两人全部一致；各条证据都被判断足够，也都没有报告额外错误或题目缺陷。唯一差异是六条文字只比较两个时期的实际标准，却没明说**文档版本关系**，R4 仍把它们算成版本主张。你批准统一说明 V4.3：有历史时间比较，不等于文本声称了文件“原版、修订版或被替代”。逐条重读后，这六条只在单独的 Owner 解释记录中归 `NOT_PRESENT`；没有改 R3/R4 原答，也没有让某一方“赢”。[第一批验收记录](../formal240/PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE2_ACCEPTANCE_RECORD_V1.md)。

所以第一批 HKP1 的 10 组、30 条可以作为 D1 的已通过构造批继续往前走。它还不是完整 D1，更不是真人标注或 Ground Truth。你同时决定：后续 HKP2、HKP3、HKP4 仍须各自逐组先锁官方证据、核事实与版本/机关、做自查，但内部质量门通过后不再每 30 条叫你去找外部评审；攒齐 90 条，才由全新的 R3 会话和不关联项目的 R4 空任务一次完成 Phase1，随后由同一会话做 Phase2。[大批量路线](../formal240/PAPER1_FORMAL_D1_REMAINING90_MEGAWAVE_ROUTING_V1.md)。如果某组证据或质量硬门不过，必须停下来修，不能为了凑齐 90 条跳过。真人 A/B、GT、正式切分和训练仍未开始。以下旧段落是当时的历史快照。

## 2026-09-26：第一批重新盲审已通过第一阶段，接下来请原两会话看证据

第一批 30 段文字的旧答卷遇到一次会话串位：R3 主动说明自己实际落在有 Canary 和第二阶段历史的旧会话里，所以我们保留原件，但不拿它充当独立盲审。你随后让 R3、R4 都从新会话重新看同一份 V4 第一阶段题目。两份新答卷已经原样保存；题号、顺序和填写值均合规，五项分类判断在 30 条上完全一致。三条解释只是措辞不同，意思一致。

运行方式出现一个真实偏差：R4 在**新建 Codex Project**中作答，而先前要求是不关联项目的 `projectless` 空目录。我们核查了该目录现在只有这一份答卷、没有隐藏说明文件或 Git；但不能由此证明平台历史完全空白。你已明确批准**只限本批这一次**的有界等价例外，不能把“新项目”一般化成 projectless。第一阶段因此收口；第二阶段的 30 条证据题包已准备好，仍须你分别发给 **R3/R4 本批原来的会话**，两人互不见答案，不要再次新建项目或会话。本批还没验收，也不能继续 HKP2。[逐人发件清单与完整路径](../formal240/PAPER1_FORMAL_D1_HKP1_BATCH1_REVIEWER_FILE_CHECKLIST_V1.md)。

## 2026-09-26：正式 D1 第一批先做完题，再请两位独立盲审

你已批准 D1 剩余40组按四批依次构造；我们目前只做了第一批 HKP1 的10组、30段候选文字，尚未把它们发给真人 A/B。每组先保存官方材料、核对原文和版本/来源信息，再写一组正确文本、设计错误文本和“看着接近但仍正确”的文本。共锁定17份有效官方材料；打不开或只返回反爬脚本的页面没有冒充证据。

本机质检在发给评审前修了三类问题：旧/新版节假日规定的生效日期需要补充官方修改决定；四组历史比较题的“合法但难判”文本都直接写出具体数字，而另外两种角色只写比较方向；另有一条把法律明确限定的职业例外写得过宽。我们没有覆盖旧稿，而是依次追加元数据和候选修复，最终 V4 是唯一待分发版本。V4 的文字长度、题号、证据哈希、共同中性查询和没有明显角色型缺失均通过有界机械检查；它们还不是被独立确认的正式数据。尤其“事实原子没有意外错误”目前只是构造侧初检，需要外部复核。[完整门控和发放文件](../formal240/PAPER1_FORMAL_D1_HKP1_BATCH1_PREBLIND_STATUS_V1.md)。

现在请把**V4 第一阶段**题目、格式说明和各自提示词分别交给 R3-gpt、R4-codex；他们只看文字，不能互看或看到答案、证据、Owner 包。收到两份原始30条文件并原样锁定、确认没有阻断问题以后，才能考虑第二阶段。当前 `STOP_EXTERNAL_REVIEW_REQUIRED`，不会自行进入 HKP2，更不会发真人 A/B、生成 GT、切分或训练。

## 2026-09-26：D1 的 8 组试构造通过，下一步先申请剩余 40 组

这次 Canary 是“正式大批量构造前，先用 8 组真实设计槽位把流程走通”的质量关，不是模型比赛。我们逐条核对了 24 段候选文字、冻结的官方依据、两位独立盲审员的第一和第二阶段结果，再检查五类检测线索需要的输入是否真的找得到。正确文本与合法但容易误判的 Hard Negative 没有发现额外事实错误；8 条有意构造的错误各有可解释的单一主机制。两位主评审对每条所用证据都判足够、没有意外第二错误或真正的题目证据缺陷。版本与发布机关能依据冻结的官方材料辨认；8 个共同中性查询也能跑出带分数和来源编号的检索轨迹，但这**不是检索或检测效果分数**。[审计说明](../formal240/PAPER1_FORMAL_D1_CANARY_FINAL_OWNER_ACCEPTANCE_AUDIT_V1.md)。

有一份审计初稿曾把“政府网站托管这篇资料”写得像“该网站就是原发布机关”；我们没有盖掉初稿，而是另存修正版，明确把托管、页面来源、原颁布机关分开。现按你预先设定的“硬门全过才接受”条件，D1 Canary 已验收，可以**单独申请**构造剩余40组。不能现在就把试构造当成完整 D1 数据，更不能发给真人 A/B、生成 Ground Truth、切分、训练或写论文正式结果。你下一步只需要决定是否批准[剩余40组分批构造计划](../formal240/PAPER1_FORMAL_D1_REMAINING40_EXECUTION_PLAN_V2.md)。

验收提交后又补了一次更细的核对：把24条的事实陈述拆成[48个可定位的小断言](../formal240/PAPER1_FORMAL_D1_CANARY_FACT_ATOM_V2_SUPPLEMENT_RECORD.md)，逐个挂回官方依据。40个受支持、8个正是设计好的错误，没有发现额外错误或没法判断的断言；此前较粗的表保留作历史，不掩盖这一补充。项目门控不因此扩大。

## 2026-09-26：两位原评审对 15 条新解释复核一致，Canary 仍待你验收

R3-gpt、R4-codex 已各自交回 V4.2 定向复核文件，我们将原始文件逐字节保存，检查了 15 条题号、顺序、填写字段和选项。两人对 13 条“是否提出版本主张”和 2 条“正确的历史版本对照”全部一致，也都符合 Owner 已冻结的解释。两人写的简短理由用词不同，但没有在这 15 项的有界复核中发现新的阻断问题。[复核记录](../formal240/PAPER1_FORMAL_D1_CANARY_V4_2_TARGETED_RULE_STABILITY_REPORT_V1.md)。

这说明原两位评审现在能稳定按新解释填写这些题，**不等于** Canary 已经通过整体质量验收。你人工确认了两人沿用原隔离会话、收到等价材料且未互看答案；我们将它记为 Owner 声明，而不是机器证明。旧 24 条答卷和 Owner 覆盖记录均未改。下一步需要你单独审阅整个 Canary 的候选、证据、修复和盲审结果并决定接受或退修；在此之前不发真人 A/B、不做其余 40 组、不切分或训练。

## 2026-09-26：先澄清“候选有没有提出版本问题”，再请两位评审定向确认

上一轮两位盲审员主要卡在同一个理解差异：候选只说“某条例第几条规定什么”，而官方证据页又显示“现行有效”或施行日期，这能否算候选提出了版本主张？Owner 现在明确：**先只看候选文本**。如果候选只是引用法条和实体规定，没有写修订、版本、现行/历史或生效转换，就填 `version_claim_status=NOT_PRESENT`；不能把证据页的元数据倒灌成候选的主张。明确点名“关于修改某条例的决定”则确实提出了修改决定的身份；正确性再由冻结证据判断。明确比较 2003 原版和 2010 修订版、且两版证据支持的正确叙述，事实总状态归“合法版本或历史”，不因为今天还能说这句话就归“当前一致”。[人类可读规则](../formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4_2_VERSION_SCOPE_DECISION.md)。

我们逐条检查了 15 个分歧：12 条只是实体规定、1 条确实命名修改决定、2 条是有证据支持的版本对照。Owner 的统一规则已作为[单独覆盖记录](../formal240/PAPER1_FORMAL_D1_CANARY_PHASE2_OWNER_SEMANTIC_ADJUDICATION_OVERLAY_V1.json)保存，**没有改动任何人的原答卷，也没有宣布哪位评审“赢了”**。现在只准备了不带旧答案的 15 条定向题包，让原 R3-gpt、R4-codex 各自确认自己能否稳定执行新解释。这不是正式 Ground Truth，也不是新一轮独立标注。Owner 还未分发；收到两份真正 JSON 文件并核对结果后，才可能讨论 Canary 验收。真人 A/B、其余40组、切分和训练仍暂停。[准备报告](../formal240/PAPER1_FORMAL_D1_CANARY_VERSION_SCOPE_REFINEMENT_REPORT_V1.md)。

## 2026-09-26：第二阶段两位盲审员都已交卷，但版本字段有系统性分歧

R3-gpt 和 R4-codex 的 Phase2 回复已经收到并原样保存。R3 的第一次文件在传输中丢失了 JSON 双引号，我们保留它，没有假装原件有效；同一评审后来重新导出了一份能读取的 JSON。核对发现 24 条题号、顺序、分类答案完全沿用第一次文件；去掉界面生成的引用标记后，24 条理由正文也相同。R4 原文件格式正常。两份可读取答卷各为 24 条，格式和选项检查通过。[锁定及分歧记录](../formal240/PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE2_RAW_LOCK_AND_DISAGREEMENT_BLOCKER_V1.md)。

两人对“事实是否冲突”有 22/24 条一致，对机关、最少外部证据、实际选用证据、证据是否足够等六项字段全部一致；但“是否存在版本主张”只有 11/24 一致。分歧主要不是对官方证据中数字或机关看法不同，而是对“只说某法某条现在规定什么，算不算声明版本”理解不同。还有两条明确比较 2003 年与 2010 年版本的正确陈述，一人归为合法历史，一人归为当前一致。这些差异在真人 A/B 开始前必须先定规则，否则会造成标注返工。当前只整理了双方原值，**没有替 Owner 选择答案、没有接受 Canary，也没有发真人标注包**。R5 仍是非门控参考。Owner 已人工确认两位 Phase2 使用的仍是各自原隔离会话、只使用冻结 E1/E2、未接触仓库/映射/Expected/GT/其他答卷或包外事实；这不是系统审计证明。下一步由 Owner 决定按统一解释逐项仲裁还是进行定向重新盲审；其余 D1 40 组、切分和训练继续暂停。

## 2026-09-26：两条修订文本复核通过，现在可以发第二阶段材料

R3-gpt 和 R4-codex 已分别复核上轮改过的两条候选。两人都认为文字自然；原本设计为“同一人既享受、又不享受年休假”的那条仍被识别为文本内部冲突，另一条没有内部冲突。我们原样保存两份返回，没有为求所有评审一致而再改文本。机器再核对 24 条候选、旧版与新版证据、官方网页哈希、三元组样式和盲包字段；有界检查通过，但它不能代替下一阶段的事实与证据审查。[详细记录](../formal240/PAPER1_FORMAL_D1_CANARY_PHASE1_FINAL_CLOSEOUT_V1.md)。

因此，Owner **现在可以**把冻结的 Phase2 V4 题包及同一套 V4/V4.1 规则分别发给原 R3、R4 会话。这里的“可以发”不等于已经发出或审完，更不等于 Canary 被验收。R5-claude 只是有额度时可用的第三位辅助者；Owner 随后同步了两份真正的 R5 文件，我们已原样保存并核对其 24 条与 2 条返回。R5 在“文字自然度”上和主评审有少量差异，其中一条把刻意的内部矛盾当作不自然；这不等于候选又坏了，不会为了三人一致而改掉设计的矛盾。真人 A/B、其余40组、正式切分与训练继续等待后续门控。

## 2026-09-23：两位新盲审员复现同一措辞小问题，已准备两条定向复核

R3-gpt 和 R4-codex 的第一阶段答卷已按原样保存。Owner 澄清了误贴材料造成的误会：R3 并没有提前做第二阶段，因此没有给 R3 记流程事故。Owner 还确认两人各用全新隔离会话；这属于 **Owner 人工确认**，不是我们拿到了会话系统日志。两份答卷各有 24 条，题号、顺序和选项均有效；五项结构化判断全部一致。两人都指出同两条候选里的“第四条下”略显生硬。

为避免正式真人 A/B 后返工，我们只把这两条的固定短语改为“根据《职工带薪年休假条例》第四条，”，另外 22 条、事实内容和证据不变。两条修订文本使用新盲号，旧文本和旧答卷完整保留；一条原有的“既享受、也不享受”内部矛盾也仍在。现在给两位原评审会话准备的是 **仅两条的第一阶段复核包**，请他们重新判断自然度和内部冲突。第二阶段 V4 材料虽已预建，**还不能发**；只有两人定向复核都通过，才能另行放行。Canary 还没有 Owner 验收，真人 A/B、其余 40 组、切分和训练都不能开始。[锁定与修复记录](../formal240/PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE1_LOCK_AND_TARGETED_REPAIR_RECORD_V1.md)。

## 2026-09-23：把下一轮两位盲审员明确区分为 GPT 与 Codex

Owner 将下一轮的两个新评审席位命名为 `R3-gpt` 和 `R4-codex`，便于日后追溯是谁、在哪种平台完成评审。它们不是此前 R1/R2 的改名，也尚未开始评审。GPT 需要全新独立会话；Codex 更不能沿用当前知道项目构造、答案和旧分歧的工作会话，必须在空白、隔离的环境里只拿到本阶段应看的文件。两人拿到的信息和判定规则等价，平台不同不代表我们在做模型性能比较。

为避免再次出现“第二阶段身份对不上第一阶段”，每一位都要从只看候选文本的 Phase1 重新做起，分别保存原件、哈希和会话/访问证明。**两份** Phase1 都通过，才给两人第二阶段的冻结证据与 V4.1 说明。旧 R1/R2 回复、候选、证据与原协议不改；本轮只把分发前的隔离和登记要求写清楚。[给协调人的 V2 计划](../formal240/PAPER1_FORMAL_D1_CANARY_R3_GPT_R4_CODEX_REVIEW_PLAN_V2.md)可直接照门控执行。Canary 尚未验收，不得发给真人 A/B。

## 2026-09-23：D1 Canary 第二阶段发现“评审会话串位”，改用全新 R3/R4

Owner 收到的第二阶段回复这次确实已保存：原材料是一个同时粘贴 R1、R2 回答的文件，我们先保留整个文件，再不改动字节地截出两段 JSON。两段各 24 条，格式、题号和顺序都对。但所谓 R1 的原文自己说明：这个会话在第一阶段其实扮演 R2，本轮却被指定为 R1。因此，两份看似齐整的回答**不能证明来自两个始终独立的评审链**。R1 仍可帮助发现说明书问题，却不能与 R2 合算正式双审一致性；该问题属于评审流程，不是某条候选文本的事实缺陷。原 R1 把它写入一条 `phase2_issue=OTHER`，我们保留原填写，不假装从未发生。

只作为诊断，两份原文在事实总状态、最少外部证据、次生错误、证据充分性上各 24/24 相同；“版本主张”相差 6 条，“机关主张”相差 4 条，“实际看过的证据”相差 5 条，“候选问题”相差 1 条。差异显示旧说明可能让人把单纯“通过/公布/令号”当成版本，把经办或开证明的机构当成法规权威。我们没有修改任何旧回答，而是新增[通用 V4.1 字段解释](../formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md)，只解释这些边界，枚举和候选、证据均不变。[流程事件](../formal240/PAPER1_FORMAL_D1_BLIND_REVIEW_PROCESS_INCIDENT_V1.md)保留全部来源及哈希。

Owner 已要求使用两个全新、互不相见的 R3/R4 会话，从只看文本的 Phase1 重新开始；各自原件锁定后，才给同一会话 Phase2 证据和 V4.1。四份新原件与分歧处理、Owner Canary 验收之前，不能发给真人 A/B，也不扩到 D1 48 组。本轮是 Canary 提前发现说明歧义和流程缺陷，**不是正式数据失败或论文实验结果**。下方“Phase2 允许释放”是本轮事件之前的历史状态。

## 2026-09-23：D1 Canary 两份独立 Phase1 盲审返回已锁定

Owner 已收回两名独立外部 GPT Reviewer 的第一阶段结果。本轮只把两份原件按原始字节存入新的 E 盘证据目录，再核对它们是否回答了同一份 24 条题目、是否漏行或改动 ID、字段与选项是否合法。两份各为 24/24 条，ID 和顺序完全吻合，没有重复、缺失或额外字段。五个分类判断逐项都是 24/24 一致，没有分歧 ID；两条文字备注虽然用词不同，均指出同一条候选文本内部前后自相矛盾。原件及哈希、核验结果见[本轮锁定记录](../formal240/PAPER1_FORMAL_D1_CANARY_BLIND_PHASE1_RAW_LOCK_RECORD_V1.md)。Reviewer 的独立性来自 Owner 的实际流程确认，不能单凭答案一致反推。

因此，**可以进入向同两名 Reviewer 分别提供第二阶段冻结证据包的下一门**；这只是释放资格，不表示已经发送、收到或分析 Phase2。本轮没有打开内部正确答案/构造角色去评判 Reviewer，更没有批准 Canary、发给真人 A/B、生成剩余 40 组或启动正式实验。下方“Phase1 尚未返回”保留为上轮构造结束时的历史快照，已被本节更新。

## 2026-09-23：D1 为什么先做 8 组 Canary，而不是直接发给人工？

Owner 已批准正式 240 组中 D1 企业人力资源 Wave 的构建，但要求先用 8 个真实槽位、24 条候选检查“官方证据先行—事实锚点—文本—质量审计—外部盲审”能否走通。现在已采集并锁定 14 份政府页面快照（其中 5 份仅证明行政法规当前状态），写出 8 组事实锚点和 24 条构造候选。初版草稿先于完整逐信号预检，因此明确只算草稿；预检后另建正式待审版本。质量检查还发现两条污染文本独有分号，以及一个证据片段未包含难负例所需的第十条，均以保留旧版、追加新版的方式修复，没有抹掉过程痕迹。

目前机器可核验的项目包括：8 组确属冻结矩阵、24 个盲 ID、14/14 原始网页哈希、三元组长度/标点初筛、候选与 Phase1/Phase2 包一致、盲包不含内部 C/P/H、HKP、设计 S 或答案。但是自动抽取只覆盖标题、数字、机构和部分关系词，不能证明所有事实都没有第二处意外错误；S/E/P/T/R 的完整信号数值、按类别缺失率与方差也尚未测量。更重要的是，两名独立外部 GPT 的先文本后证据盲审**尚未返回**，所以 Canary 未验收、不能给真人 A/B，剩余 40 组也未生成。[D1 后续计划](../formal240/PAPER1_FORMAL_D1_FULL_WAVE_CONSTRUCTION_PLAN_V1.md)说明通过盲审与 Owner 验收后才如何分批扩展；所有内部构造证据保存在独立的私有 handoff 包，不能发给盲审者。

下一步由 Owner 分别将当前 Phase1 V2 包与同一 Phase1 prompt 发给 R1/R2，锁定两份独立返回后，才发 Phase2 V3 包与 Phase2 prompt；任何实质分歧先修复并全量重审，不进入 Human A/B。本轮没有正式标注、切分、训练或论文结果。

## 2026-09-22：正式 240 组为什么先冻结规则，而不是马上写 720 条？

项目负责人已决定关闭 Final72 的开发集构建阶段，开始正式规模 Benchmark 的**设计冻结**。Final72 的小样本模型表现有启发，但它被反复用于工程调试，绝不能再叫“未见过的正式测试集”。本轮建立了五个领域、四类污染、三档设计隐蔽度、每格四条独立事实链的 240 个**空槽位**；每组未来才会有当前正确、污染和合法难负例三条，720 只是目标，目前一条正式候选也没有生成。

最重要的修复是把“版本有没有修订、何时生效、是否现行”等**文件版本元信息**，与“修订后具体规定是否正确”和“谁修订发布”拆开判断。正式 V4 新增“文本内部已自相矛盾、无需外部证据”的选项；此前 Pilot 的已锁定答案不回写。隐蔽度最后由人工确认的错误及所需证据派生，不能为了填满 S1/S2/S3 设计格子而硬改真值。完整[标注 V4](../formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md)和[协议包](../formal240/PAPER1_FORMAL_240_GROUP_PROTOCOL_OWNER_ACCEPTANCE_PACKET.md)可供复核。

构建顺序将是先选可信官方证据、厘清版本和发布机关、画出证据路径，再写同一信息需求下的三条候选；每组只用一条中性查询。我们还事先规定了“难”证据库、元数据可观测性、常量/缺失检查以及按完整事实链切分的算法。Seed 已锁，但没有运行切分，更没有训练。下一步只需 Owner 单独审查并批准 D1 企业人力资源 48 组/144 条的实际构建；其他领域、人工分发和正式实验均不能自动开始。

## 2026-09-22：补齐遗漏的逐条分数后，第一版 Detector 告诉了我们什么？

Owner 先批准找原始文件；有界搜索确认原运行只留下完整模型的逐条分数，另八个模型只留下汇总。随后 Owner 授权按**完全相同输入、代码和设置**做一次证据重建：重建的完整模型逐条分数与原件逐项匹配，另外八个模型的汇总也与当时记录一致。原运行、原结果和历史痕迹都未替换。这是恢复分析所需的证据粒度，不是为了提高分数重新训练或一次独立复现实验。

在 Final72 开发集里，来源视角 P 和时间版本视角 T 单独使用时，对 24 组 Poison 与合法历史文本，有 20 组给出相同排序分数；这更像“分不出来”，不能草率说它们把 20 个历史文本判得更危险。合并 T 后有 17 组的 Poison–历史文本分数间隔缩小；合并 P 后有 19 组扩大，但少数组负向幅度较大。21 项输入里七项在观测值上不变，时间版本所需的关键关系仍有缺口。当前多视角结果因此仍是“混合”，不是方法成功或失败的正式结论。[详细分析](../method_engineering/PAPER1_FINAL72_DOCUMENT_DETECTOR_FAILURE_ANALYSIS_REPORT_V1.md)解释难组、来源与版本缺口、哪些假设须去更难且独立的 240-group benchmark 验证。

下一步建议准备正式规模 benchmark 的证据库、版本/权威关系和困难合法历史样本，并在未来每个模型运行时保存逐条分数与折身份。**尚未批准**生成 720 条正式样本、正式训练、风险校准或论文效果宣称。下方“失败分析暂停”是 Owner 决策前的历史记录，不代表当前仍被该证据缺口阻断。

## 2026-09-22：为什么失败分析暂时停下？

第一次 Detector 原型本身有效、结果没有被推翻；它训练过九种固定视角组合。但原始运行最终只保存了完整模型每条候选的折外分数，其它八种组合只保存了汇总分数。新任务要求回答“加上时间版本或来源视角后，具体哪一组变好、哪一组变差”。仅凭 AUROC 等总体数字无法倒推出每组分数；若编造会误导正式 240-group 设计。当前 Owner 明确禁止重训，因此我们暂停这一部分并保留原始证据不动。[决策记录](../method_engineering/PAPER1_DOCUMENT_DETECTOR_FAILURE_ANALYSIS_EVIDENCE_BLOCKER_01.md)给出三条路：提供当时确实存在的原始逐样本文件、单独批准一次严格等配置的追加证据重建，或明确同意只做部分分析。正式实验尚未启动。

## 2026-09-22：第一版 Document Poison Detector 到底怎么训练，得到了什么？

这一次终于真的拟合了第一个文档污染检测原型：固定的 Logistic Regression 把 21 项可独立获得的语义、事实主张、来源、版本信号合在一起。前一轮发现两项“发布机构关系”没有可信候选级输入，所以 Owner 允许在独立 V1.1 中暂缓它们；这不是为了刷分。检索行为 R 属于第二阶段“检索暴露风险”，没有混进文档本身判毒。

Final72 只有 24 条独立事实/版本链，每条链有 Clean、Poison、合法历史 Hard Negative 三种候选。如果普通随机切分，几乎相同的事实链会同时出现在训练和验证中。我们因此做 24 次 Leave-One-Group-Out：每次留出完整的一组三条，只在其余 69 条上计算缺失值填补、标准化并训练，最后每条得到一次折外分数。没有调参、找最佳阈值或做风险校准。

Full SEPT 在这个**已暴露开发集**上的 AUROC 为 `.647`、AUPRC `.496`；Poison 对合法历史 HN 在 24 组中胜出 18 组，但固定 0.5 阈值仍错判 8 个 HN。Semantic-only 的 AUROC `.623`；去掉 P 或 T 的版本若干指标反而高于 Full。所以本轮只能说“有混合信号、原型可运行但限制明显”，不能说多视角已胜出，更不能说论文最终检测效果。Temporal 仅有三项可部署信号，Provenance 还缺两项关系；7 项特征在当前小样本里为常量，57 文档可信库也可能过易。200 次组内标签置换与 2000 次匹配组 bootstrap 已做 sanity/不确定性检查，不提供正式显著性或泛化保证。

下一步更合适的是经 Owner 批准做失败组与规模化假设分析，把 HN 易误报、版本元数据、来源角色和检索库难度的要求带进未来 240-group，而不是在 Final72 上反复改模型到分数升高。[完整报告](../method_engineering/PAPER1_FINAL72_DOCUMENT_DETECTOR_PROTOTYPE_REPORT_V1_1.md)可查看九模型、难组和边界；正式 benchmark、校准与检索暴露模型仍未启动。

## 2026-09-16：为什么 Retrieval View 不能简单等于 Poison Detection？

本轮已经建成无标签泄漏的检索实验台：24 个中性“当前规定是什么”query 面对同一套 72 文档，字符 BM25 与固定
revision 的离线 Dense retriever 都保存了完整 rank/score trace。现在能稳定得到 rank、score、重复运行 stability；但没有
Trusted Version Registry，所以 7 个需要 current/history 身份的 R signals 仍不计算。

项目现正式采用两阶段风险：第一阶段用 S/E/P/T 判断文档本身的 `document_poison_risk`；第二阶段结合 query 和 R 判断
`retrieval_exposure_risk`。比如一份真实合法的 2021 年历史文件在“当前规定是什么？”下排名第一，可能造成回答采用旧版本，
所以 retrieval risk 较高；它仍然不是 Poison。

还必须区分“研究时已人工配好的 E1/E2”和真实 inference。Pilot 中直接拿 matched E1/E2 可以诊断 signal 是否有潜力，
但真实系统若没有独立 trusted evidence retrieval 或 version registry，就不可能合法得到同样输入。42 个 signals 中目前
29 个属于这种 oracle-only diagnostic，4 个是 query-runtime 可获得，7 个等待 registry，2 个 MLM/PPL 尚未冻结。

结论不是“Detector 可以训练了”：Document Detector 仍 `NOT_READY`；Retrieval Risk 为
`READY_WITH_LIMITATIONS`。下一步先补独立 Evidence retrieval 与 Trusted Version Registry，不自动训练 Detector。

## 2026-09-15：Final72 五视角信号可行性已完成，尚未训练分类器

我们现在不是在“训练分类器”，而是在检查五种安全证据是否真的存在、能否稳定提取，以及是否包含区分 Poison 和合法历史
Hard Negative 的信息。控制面先从候选、冻结 Evidence 与来源/版本信息生成无标签输入；另一个进程只读取这份输入，生成
72×42=`3024` 条 raw signal 并按 SHA 锁定；第三个进程核验锁定后，才加载 Clean/Poison/Hard Negative、HKP、S 和
matched-group 身份。Raw 中没有这些标签，也没有 Expected、A/B 或 Owner 仲裁值。

实际结果是：Semantic、Entity-Claim、Provenance、Temporal-Version 都有可计算信号，但很多只是确定性规则代理，部分为
常量、近常量或高度相关；Retrieval-Behavior 因 Final72 没有冻结合法 query 与独立 retrieval run，全部 720 项都标为
`INPUT_MISSING`，没有用标签倒推 query。MLM/PPL 没有冻结模型，因此保持 `MODEL_UNAVAILABLE`；GMTP 也因缺少完整可复现
依赖而推迟。类别各 24 条，24 个 Clean/Poison/Hard Negative 匹配组完整；Applicability 没有发现达到门槛的类别泄漏，
七个已知 Evidence 限制样本也没有形成强类别集中。

单信号的 Cliff's delta、AUROC/AUPRC 和 matched-group 方向仅用于 development-set 诊断，不能叫 Detector 准确率，更不能
声称方法优于 baseline、可泛化或达到论文结果。当前结论是 `READY_WITH_VIEW_LIMITATIONS`：S/E/P/T 足以继续方法工程，
但五视角版本在训练前应先补齐 Retrieval 输入。建议的下一任务是
`P1-RETRIEVAL-BEHAVIOR-SIGNAL-HARNESS-01`，仍需 Owner 单独批准。

## 2026-09-15：Final72 Ground Truth 正式接受，进入 Signals / Detection 方法工程

项目负责人已经以“接受，但保留已知冻结证据限制”的方式正式验收 Final72 Ground Truth。72 条候选、576 个最终字段和
每个字段的 A/B、Owner 仲裁与 correction lineage 都完整；11 项 Evidence 限制继续明确写成证据不足或证据缺失，没有被
隐藏或事后补证。Expected V3 仍只是人工仲裁完成后的研究质量对照，不能覆盖人工真值。

Final72 从现在起是开发与方法工程数据，不是论文最终独立测试集。因为我们已经用它校准标注规则、处理仲裁并检查方法，
任何在它上面反复调试的方案都必须叫 development-exposed。未来论文最终效果必须来自扩大后的 Benchmark、按 version chain
分组切分，以及从未参与开发的 test population。

### 我们接下来到底怎样检测知识污染？

`Signals（信号）` 是可观察证据，例如候选更像历史版本还是当前版本、主张中的数字/条件是否与证据冲突、声称机关是否与
真实发布/制定/修订关系一致、检索结果是否被历史版本占据。`Detection（检测）` 是把这些信号组合起来，输出污染风险。
Signals 本身不是答案，也不能读取 Ground Truth。

第一版方法使用五个视角：Semantic 看语言和语义接近度；Entity-Claim 看主体、数值、日期、条件、例外和关系；Provenance
区分网站、页面发布者、制定/通过/修订机关与官方转载；Temporal-Version 判断现行、历史、废止、替代和时间绑定；Retrieval-
Behavior 看 rank、score、top-k 版本构成与稳定性。MLM/PPL 只是语言自然度 baseline/语义信号，GMTP 是可复现时使用的外部
检测 baseline，不是我们的全部方法；核心 proposed method 仍是 Version-aware Multi-view Detection。

本轮只把信号定义、适用性、baseline、Logistic Regression fusion、风险校准候选、证据化解释、指标、消融和 240-group
Scale Readiness 写清并建立代码接口。没有跑实际信号矩阵，没有训练 Detector，没有得到准确率或优越性结论。下一步需由
项目负责人单独批准第一轮 `SIGNAL_FEASIBILITY_AND_SEPARABILITY_STUDY` 的输入、模型、query/retriever、参数和统计合同。

## 2026-09-15：Final72 Ground Truth Candidate 已生成，等待项目负责人最终接受

人工仲裁已经正式结束。系统先从四份不可变 A/B 返回重建全部 72 条、576 个字段：A/B 相同的 498 项直接沿用，两人不同的
78 项使用项目负责人在不知道 Expected V3 时作出的决定，随后再应用 8 条已批准规则 overlay 和 10 条一致性 correction
overlay。每个最终值都能回查 A、B、Owner 决定与 overlay；原始答卷和 Owner 工作簿均未修改。

只有上述 Human-adjudicated candidate 完整锁定后，才第一次把 Expected V3 用于研究者侧质量核验。Expected V3 不是
Ground Truth，也没有覆盖任何人工值。Expected 明确定义的 504 个字段中，469 个与 Human candidate 一致，35 个差异覆盖
28 个样本；其中 4 项是 Expected V3 需要以后另行版本化修正的 QC 缺陷，11 项来自已经由 Owner 以
`INSUFFICIENT_EVIDENCE / EVIDENCE_MISSING` 固定下来的已知 Evidence 限制，20 项是非阻断的人类仲裁差异。Expected 没有
定义 `phase2_issue`，因此其 72 个比较槽位明确记为不可比较，没有虚构预期值。新的 Ground Truth blocker 为 0。

当前产物是 `PILOT4_FINAL72_GROUND_TRUTH_CANDIDATE_V1`，不是已接受的 Ground Truth，也不是正式冻结数据集。Final72 已参与
校准、人工仲裁和研究者 QC，未来只能用于 development / method engineering，不能再称为 untouched final test set。项目
负责人下一步只需决定是否接受该 GT Candidate；在明确接受前，不开始 240-group、正式 Dataset freeze 或 Detector evaluation。

## 2026-09-15：Owner 仲裁一致性已闭合，未解决项为 0

项目负责人已逐项确认上一轮 9 个核验项。控制面没有修改 A/B 原始返回，也没有修改 Owner 原始工作簿，而是新增了 10 个
字段级 correction overlay：4 条把非事实冲突的 minimum 统一为 `NOT_APPLICABLE`；1 条把个人信息保护法样本的
`phase2_issue` 改为 `NONE`；1 条只把证券法样本理由中的 E3 笔误改为 E1；学位条例/学位法样本用 4 条字段记录冻结
packet-only 结论并移除 E3/E4 依赖。合计 6 个值发生变化，4 个值保持不变但理由和证据链得到规范化。

重新检查全部 72 条、576 个字段后，枚举、minimum/overall、内部矛盾、Evidence missing 和有效 Evidence 引用关系全部
通过，未解决一致性 blocker 为 0。原 Owner 工作簿 SHA256 仍为
`a4c65a22dd3a410c7744be5f256206d7217b8fda33d63c58ac99bb386fe95b01`。本轮到此停止：Expected V3 没有加载，Final72
Ground Truth 没有生成，下一步必须由 Owner 单独批准。

## 2026-09-15：Owner 仲裁已回收并锁定，剩余是定向一致性确认

项目负责人已经完成工作簿。控制面把这份返回文件按原始字节保存，没有改写任何填写痕迹；5 个候选缺陷决定和 78 个字段
仲裁全部完整。五个候选都被 Owner 判为“标注理解差异”，没有候选被自动隔离。78 个字段中，Owner 选 A 46 项、选 B 26 项、
选择 A/B 之外的第三值 6 项；其余 498 个字段沿用 A/B 一致结果，因此已形成一个 72 条、576 字段的仲裁后候选视图。

这个候选视图还不是 Ground Truth。原因不是要 A/B 重新标注，而是有少数关系约束需要 Owner 最小追加确认：4 条在 overall
不是 `FACTUAL_CONFLICT` 时仍填写了实质 minimum 值；1 条把决定性 overall 与 `EVIDENCE_MISSING` 并置；4 个理由引用了
工作簿未绑定的 E3/证据3。此前 Owner 已批准的两条规则——“文本内部矛盾时 minimum 为 NOT_APPLICABLE”和“显式修订命题
属于 version claim”——已经作为单独覆盖记录绑定，原工作簿和原填写均保持不变。下一步只需逐项确认建议值或补充 E3 来源，
不需要重新保存工作簿，也不需要重新标注 72 条。

## 2026-09-13：Owner 仲裁工具已准备，Expected 仍未打开

我们没有让系统根据“预期答案”自动判谁对，而是先把 A/B 四份原始答卷的复现性再次固定下来。现在有一份专门给项目
负责人使用的中文工作簿：第一页先处理 5 个“候选本身可能有缺陷”的问题；只有被判为标注理解差异的样本，才进入后面的
普通字段仲裁。其余 78 个分歧按同一候选连续排列，并保留 A/B 原值、理由、规则和冻结官方证据。

所有需要负责人填写的格子目前都是空的，系统没有代做决定。负责人可以从完整下拉选项中选择第三种值，不被迫在 A/B
之间二选一。Expected V3 仍保持封存；只有工作簿填写完成并在下一任务中先按原始字节锁定、校验和提取 Owner 决定后，
才可能单独批准加载 Expected 做研究者 QC。当前没有 Ground Truth，也没有开始数据集冻结、检测器、训练或正式实验。

## 2026-09-13：两位标注人的 Phase2 已锁定，当前需要 Owner 处理分歧

HUMAN-A01 与 HUMAN-B01 都完成了第二阶段。控制面没有改答案，而是先把两本工作簿按原始字节保存，再核验 72 条编号、
顺序、枚举、理由、条件逻辑和 Evidence 链接，最后导出严格八列 CSV。四份人工返回现在全部不可变锁定；只有在这个门
关闭后，A/B 的不同匿名编号才被还原到同一 Candidate。本轮没有加载 Expected V3，也没有把预期答案当裁判。

一致性预检显示：overall fact status 相同 54/72，version 59/72，authority 67/72，minimum evidence 62/72，derived stealth
64/72。`evidence_selection` 反映“实际看了什么”，不是 benchmark 标签，因此它的 18/72 只作过程观察。总体有 78 个需要
实质裁决的字段分歧，覆盖 40 个 Candidate；B 另标出五个 late candidate defect。它们可能是候选缺陷，也可能是标注理解
差异，控制面不能替 Owner 自动决定。

下一步不是重新让 A/B 全量标注，而是 Owner 只看 disagreement-only packet：先判断五个 defect flags，再逐项决定其余分歧。
在裁决完成、pending=0 且所有门重新核验前，不生成 Ground Truth，也不启动 Dataset、Detector、Training、5090 或正式实验。

## 2026-09-09：Phase2 七字段返工风险已审计，V3.2 可以分别发放

HUMAN-A01 与 HUMAN-B01 已各自独立完成 72 条第一阶段标注。控制面没有改动答案，而是按原始字节保存并核对：A 文件
3313 bytes、SHA256 `bb74908f7433bca1c834e8e7ea8e8721316edb1a503202805f90dd0e974d8bac`；B 文件 3658 bytes、
SHA256 `b27d291dcf86088dccc9a7fc7e5dda1e5c1e7af54ac7db7c3bad5d78b215daf2`。两份文件的编码、五列格式、72 个编号、
编号顺序、选项和值与理由规则都通过，因此“双 Phase1 都完成并锁定后才放 Phase2”的门已经关闭。

分发前又做了一次七字段返工风险审计。结果不是协议有错，而是 V3 的 Evidence 入口和真人说明仍可能造成重复理解成本。
因此新建 V3.2：Candidate 同行直接显示 E1/E2 标题和完整官方 URL，live URL 是首选核验入口；`02_证据` 的 144/144
冻结正文继续作为稳定备份。工作表不再加保护，真人可以调行高、列宽、缩放、换行和筛选。Guide V4 用十步流程、
九个完整例和十类常见错误解释七字段；规则、枚举、Candidate、ID、顺序、Evidence 和 Expected 均没有改变。

这一步只让 Phase2 具备受控分发条件，不代表 A/B 已一致。当前还没有计算 agreement、没有仲裁、没有 Ground Truth，
也没有启动 240-group、Dataset freeze、Detector、Training、5090、Formal Experiment 或 Paper Result。下一步仅是 Owner
分别把 A/B 各自的四份 Phase2 V3.2 文件交给本人，并继续保持两人隔离。

## Human-readable Research Plan & Experiment Ledger

Document Role = `PAPER1_PRIMARY_HUMAN_ENTRY`<br>
Audience = `项目负责人 / 导师与领导 / 新团队成员`<br>
Reading Path = `5 minutes / 15 minutes / 30 minutes`<br>
Current Evidence Cut = `Retrieval harness complete / two-stage boundary frozen / deployability audited`<br>
Last Updated = `2026-09-16`

> 这是一张“项目地图”，不是 raw evidence，也不产生新授权。读完第 0 节可掌握当前状态；读到第 8 节可理解论文方法；
> 读完第 19 节可进入项目工作。精确状态、协议、决定和证据分别通过链接下钻。

## 0. 先看这里：5 分钟了解 Paper 1

| 问题 | 当前回答 |
| --- | --- |
| 中文论文题目 | 《面向中文检索增强生成系统的版本感知隐蔽知识污染基准与多视角解毒方法》 |
| 英文论文题目 | *Stealthy Factual Poisoning in Versioned RAG Knowledge Bases: A Benchmark and Multi-View Detection Framework* |
| 一句话研究问题 | 在版本、时间和来源关系复杂的中文知识库里，如何识别“语言自然、检索相关、事实却被悄悄改变”的内容，同时不误伤合法旧版本和正常更新？ |
| 一句话核心方法 | 构建 Clean–Poison–Hard Negative 匹配数据，用 Semantic、Entity-Claim、Provenance、Temporal-Version、Retrieval-Behavior 五类互补证据估计风险，再做可校准的过滤或降权。 |
| 当前阶段 | ✅ Retrieval harness 已完成；Document Risk 与 Retrieval Exposure 已分层。 |
| 当前任务 | `P1-RETRIEVAL-BEHAVIOR-HARNESS-AND-DEPLOYABLE-SIGNAL-BOUNDARY-01`：检索运行与输入威胁模型收口。 |
| 当前完成度 | ✅ 24 queries、72 corpus、Sparse+Dense 双运行、8448-row R matrix、42-signal audit 完成。 |
| 当前唯一人工动作 | Owner 决定是否批准 Trusted Evidence Retriever + Version Registry prototype；不自动训练 Detector。 |
| 当前主要 blocker | 29 signals 仍是 matched-Evidence oracle；7 个 R signals 缺 Trusted Version Registry。 |
| 已经可以说什么 | R 的 rank/score/stability 工具链可复现；Retrieval Risk 已具备受限工程入口。 |
| 绝对不能说什么 | 不得称为 Detector 结果、正式 test 结果、superiority、generalization 或有效防御。 |

当前实验状态固定为：

当前状态枚举如下；它只说明已经批准和仍在等待的边界：
`PILOT4_FINAL72_GT_ACCEPTED / RETRIEVAL_HARNESS_COMPLETE / DOCUMENT_DETECTOR_NOT_READY /
RETRIEVAL_RISK_READY_WITH_LIMITATIONS / NO_DETECTOR_TRAINING / NO_FORMAL_RESULT / AUTO_CONTINUE_NO`

保留的历史状态链含 `PREANNOTATION_ONLY`：`PILOT4_BALANCED_SET_REPAIRED / READY_FOR_SECOND_OWNER_PREFLIGHT` →
`PILOT4_FINAL_PREANNOTATION_READY_FOR_OWNER_REVIEW` → `PILOT4_QUALITY_CONVERGED` → Schema V3.1 hardening → 当前外部盲审包状态。历史 package 不被覆盖。

状态的动态权威入口是 [Current Work State](../../../governance/current_work_state.md)。

历史协议框架事实：`S6.1-P1-R1 = HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK`；该接受不等于数值协议、Dataset 或正式实验冻结。

## 1. 项目背景：我们到底在研究什么

RAG（Retrieval-Augmented Generation，检索增强生成）先从知识库找文档，再让生成模型依据这些文档回答。它比只依赖模型
参数更容易更新和审计，但也把安全边界扩展到“谁能写入、替换或伪装知识库内容”。

知识污染（knowledge poisoning）是把错误或恶意内容放进知识库，使它被检索并影响回答。隐蔽知识污染（stealthy
knowledge poisoning）更难：文本语法自然、主题相关、与 query 很相似，错误藏在数值、适用条件、版本时间或来源权威中。

版本化知识库尤其困难，因为“与当前事实不同”不等于“恶意”。旧政策、合法修订、尚未生效条款、地区差异和例外条件
都可能是真实文档。若 Detector 只看语义，它可能把这些内容误判为污染。因此 Paper 1 不只需要 Poison，还必须设计
Hard Negative（困难负例）：表面像污染、实际合法，用来测量误伤。

简化例子：

| 类型 | 候选文本 | 解释 |
| --- | --- | --- |
| Clean | “修订后的职业教育法自 2022 年 5 月 1 日起施行。” | 与当前权威版本一致。 |
| Poison | “修订后的职业教育法自 2022 年 6 月 1 日起施行。” | 语言自然但改变了关键生效日期。 |
| Hard Negative | “原职业教育法自 1996 年 9 月 1 日起施行，后被修订文本替代。” | 描述历史版本，日期不同但不是污染。 |

核心难题不是“找出所有不同”，而是“用版本、时间、来源和检索行为证据区分恶意事实改变与合法差异”。

### 为什么这次不再重跑 Full72

Pilot4 的外部复核已经证明 72 条候选在 Phase1 没有候选缺陷；Phase2 也不是全面失控，而是绝大多数字段稳定，分歧主要
聚集在“一个正确命题只是提到历史日期，还是必须依赖历史/版本限定才成立”这个字段边界。此前还发现少量 Expected 字段
和 Evidence Pool 设计问题。把这种局部测量工具问题写成“实验失败”不准确，再让 reviewer 重做全部 72 条也会浪费人工。

本轮因此采用更窄但更严格的方法：先把边界、Expected 和 Evidence 逐项修复并保留全部旧版本，再把 21 条真正受影响样本
与 16 条在领域、候选类型、HKP、隐蔽等级和命题结构上匹配的控制样本混合，交给全新的隔离 reviewer。Reviewer 不知道
哪些被修、哪些是控制，也看不到旧 ID、sample ID、mapping、expected 或 mismatch 分类。这样能直接回答“新规则是否更清楚，
同时有没有把原本稳定的判断弄坏”。现在这 37 条已经返回并完成锁定：M4/BR18 与 M8 通过，但 controls overall 只有
13/16。逐项审计显示，主要原因是 Expected V2 仍把若干当前有效更新过度标成“合法历史”，而不是 reviewer 或 Evidence
Pool 全面失效。因此下一步是一次追加式 Expected V3 处置和同 raw 重算，不是继续要求 reviewer 反复标注；协议和 A/B
仍须后续独立批准。

Expected V3 已把上述审计发现变成 7 个追加式字段更正，但没有覆盖 Expected V2，也没有改 reviewer raw。为避免“看答案改
答案”，本机先只读取候选、Guide 和冻结 E1/E2，生成并哈希锁定 Expected V3，之后才加载 reviewer value 做重算。结果把
M2 从 3/16 降到 2/16、控制组 overall 从 13/16 提到 16/16、exact relevant fields 从 29/37 提到 35/37；剩余两条均为
非系统性 reviewer variance。所有冻结门通过后，Owner 正式选择 `ACCEPTED_WITH_NONBLOCKING_NOTES`，关闭校准并确认不需要
R4。现在不再反复做校准标注；下一道门是独立审批正式 A/B 执行，而不是自动发放标注材料。

### Pilot4 最终留下了什么

Pilot4 先暴露了候选自包含性、sample-ID 泄漏、Phase1/Phase2 同上下文、Evidence 重复与 Expected 边界等问题；其根因分别
落在候选设计、盲法隔离、证据传输和控制面标签合同，而不是简单的“reviewer 填错”。最终规则是：候选先过盲法质量门；
Phase1 与 Phase2 结构分离；raw return 先锁定再加载 mapping/Expected；每个证据槽保留冻结官方快照与 URL provenance；
Expected 不是自动真值；自然度只作 QC、evidence selection 只作过程描述；A/B 必须独立，分歧由 Owner 定向仲裁。共 13 条
有证据支持的 lesson 已提升为 accepted，正式 A/B 重复性、Final72 Ground Truth、正式 Dataset/split 和规模化统计仍保持
provisional，必须由后续真实执行证据决定。

## 2. 专业术语中英文速查

| 术语 | 中文速解 |
| --- | --- |
| RAG | Retrieval-Augmented Generation；先检索知识，再基于检索内容生成回答。 |
| Benchmark | 基准数据与评估协议；不只是一个文件，还包括切分、标签、指标和可复现合同。 |
| Ground Truth | 经冻结流程确认的参考真值；Pilot-only 真值不等于正式 Benchmark 真值。 |
| Clean | 与权威事实、适用范围和版本状态一致的候选。 |
| Poison | 保持自然和相关性、但实质改变事实状态的候选。 |
| Hard Negative | 看起来可疑但实际合法的困难负例，用于测量误报。 |
| Matched Triplet | 同一事实主体下匹配的 Clean、Poison、Hard Negative 三元组。 |
| Version Chain | 同一主张的前版、现版、修订、废止或替代关系链。 |
| Provenance | 内容来自哪里、如何获取、如何派生的来源链。 |
| Authority | 发布主体的权威身份、层级、管辖范围及其是否支持该命题。 |
| HKP | Hidden Knowledge Poisoning；本项目的四类隐蔽知识污染变异。 |
| Stealth | 隐蔽性；错误需要多大证据成本才能被发现。 |
| S1 / S2 / S3 | S1 本文即可发现；S2 一个直接官方证据可确认；S3 需要跨版本/来源的联合证据链。 |
| Semantic View | 语义视角；观察 query 与候选是否相关、表达是否异常。 |
| Entity-Claim View | 实体—主张视角；观察主体、属性、数值、条件等关系。 |
| Provenance View | 来源视角；观察发布者、引用链和权威匹配。 |
| Temporal-Version View | 时间—版本视角；观察生效、失效、修订、替代与版本顺序。 |
| Retrieval-Behavior View | 检索行为视角；观察排名、邻域和扰动下的检索稳定性。 |
| Signal | 某一视角输出的结构化诊断证据或分数，不等于最终预测。 |
| Detector | 将允许的多视角输入融合成污染判断或风险分数的检测器。 |
| Risk Score | 候选为污染的风险估计，需经过校准才能用于阈值决策。 |
| Calibration | 让预测分数与实际风险概率/阈值行为相符。 |
| FPR | False Positive Rate；把真实非污染误报为污染的比例。 |
| Recall | 在真实污染中成功检出的比例。 |
| Precision | 被判为污染的样本中真正是污染的比例。 |
| AUROC | 不同阈值下真阳性率与假阳性率权衡的面积；类别极不平衡时需结合 AUPRC。 |
| AUPRC | Precision–Recall 曲线面积；更直接反映低污染率下的检出质量。 |
| Poisoned@K | Top-K 中污染文档的暴露数量或比例，越低越好。 |
| Recall@K | Top-K 是否保留相关正常文档，越高越好。 |
| MRR | Mean Reciprocal Rank；首个相关结果排名的倒数均值。 |
| nDCG | Normalized Discounted Cumulative Gain；考虑相关性等级和位置的排序质量。 |
| Ablation | 消融实验；删除一个视角或训练设计，测量其独立贡献。 |
| Generalization | 泛化；在未见攻击、领域、版本模式或来源上的表现。 |
| Adaptive Attack | 知道防御规则后主动规避检测的攻击。 |
| Hard Filtering | 风险超过阈值时直接从候选集合移除。 |
| Soft Downweighting | 不直接删除，而按风险降低检索分数。 |
| Dataset Freeze | 数据身份、标签、切分、许可与 hash 被正式锁定，之后不能任意调整。 |
| Formal Experiment | 在冻结协议、数据、代码、参数和统计计划下执行的正式实验。 |

## 3. Paper 1 最终要证明什么

以下是科研证据链，不是已完成结论。`PILOT_SUPPORTED` 只表示 Pilot 提供了可行性或失败模式证据。

| # | 最终主张 | 当前证据状态 | 当前解释 |
| --- | --- | --- | --- |
| 1 | 中文版本化 RAG 存在难被简单语义相似度识别的隐蔽事实污染。 | `PILOT_SUPPORTED` | Pilot3 显示语义/时间诊断信号很弱，支持“问题值得研究”，不构成总体性能结论。 |
| 2 | 可构建含 Clean、Poison、Hard Negative、版本链、权威关系和 S1–S3 的中文 Benchmark。 | `PILOT_SUPPORTED` | Pilot1–4 支持来源、标注和构造可行性；Formal Benchmark 尚未冻结。 |
| 3 | Semantic-only 不足，且容易把合法历史版本误判为污染。 | `PILOT_SUPPORTED` | Pilot3 暴露 HN 误报与弱语义信号；尚无正式对照统计。 |
| 4 | Entity-Claim、Provenance、Temporal-Version、Retrieval-Behavior 提供互补证据。 | `PILOT_SUPPORTED` | 五视角信号可运行，结构化 Temporal/Provenance prototype 已实现；互补收益尚未正式建立。 |
| 5 | Multi-view 方法更可靠地区分真实污染与合法版本差异。 | `NOT YET ESTABLISHED` | Formal Detector 未实现，组合矩阵和正式 test 尚未冻结。 |
| 6 | calibrated risk 的过滤/降权降低污染暴露并保持正常检索效用。 | `NOT YET ESTABLISHED` | Option B 合同与工程 primitive 存在，但 effectiveness 未建立。 |

目前没有任何一项处于 `FORMALLY ESTABLISHED`。正式建立必须满足第 18 节的全部条件。

## 4. Benchmark 总体设计

### 4.1 正式五领域

`PAPER1_FORMAL_DOMAIN_SET = OWNER_CONFIRMED`

| ID | 中文领域 | English |
| --- | --- | --- |
| D1 | 企业人力资源 | Enterprise Human Resources / Enterprise HR |
| D2 | 财务 | Finance |
| D3 | 信息安全 | Information Security |
| D4 | 采购与研发 | Procurement and R&D |
| D5 | 教育与科研 | Education and Research |

这五个领域只用于未来 Scale Pilot / Formal Benchmark 规划。Pilot4 实际覆盖四领域，这是不可回写的历史事实。

### 4.2 HKP 与隐蔽等级

| 类型 | 含义 |
| --- | --- |
| HKP1 | 数值或实体被改变。 |
| HKP2 | 适用条件、例外或否定关系被改变。 |
| HKP3 | 生效、失效、废止、替代或版本顺序被改变。 |
| HKP4 | 来源、权威层级、机构归属或引用关系被伪装。 |

- S1：候选自身、内部矛盾、明显时间逻辑或普通常识即可发现事实错误。
- S2：候选本身自然，但一个直接官方来源或同一文件的直接上下文即可确认错误；“打开一个官方页面”不等于跨文档。
- S3：必须依赖多个版本、文档、来源、时间演化、authority chain 或 provenance chain 联合确认。
- 正确候选不评价 S1/S2/S3，而是 `NOT_APPLICABLE`；证据不足时为 `UNCERTAIN`。

### 4.3 Scale Pilot 结构

`5 Domains × 4 HKP × 3 Stealth × 4 Independent Chains = 240 independent groups`

- ✅ `STRUCTURE CONFIRMED`
- 📌 `EXECUTION NOT STARTED`
- 📌 `FORMAL DATASET NOT FROZEN`

若每组生成 Clean + Poison + matched Hard Negative，则约为 `240 × 3 = 720 candidate records`。这个 720 是
`PLANNED DERIVED SIZE / NOT FROZEN / NOT GENERATED`，不是当前数据事实。

## 5. Clean / Poison / Hard Negative

Clean 是正确对照，Poison 是实质事实被改变的攻击候选，Hard Negative 是“像污染但合法”的压力测试。三者应在同一主体、
主张、长度和检索相关度上尽量匹配，避免模型靠格式或主题捷径分类。

Hard Negative 是 Paper 1 的核心，因为真实版本库里最危险的错误不是漏掉明显 Poison，而是把历史、修订、例外或转载
全部删除。关键子类包括：

- `legitimate historical version`：合法历史版本；
- `legitimate update`：合法更新；
- `legitimate exception`：合法例外；
- `scope difference`：地区、部门、对象或条件范围不同；
- `authority repost`：权威来源的合法转载或转发；
- `near-miss-but-true`：表达极像错误，但细节仍为真。

因此 Hard Negative FPR 既是数据质量指标，也是方法是否可部署的关键指标。

## 6. 五视角方法

| View | 中文名称 | 输入 | 主要看什么 | 主要覆盖 | 可能失败 | 当前实现状态 |
| --- | --- | --- | --- | --- | --- | --- |
| Semantic | 语义视角 | query、候选文本、允许的语义特征 | 相关性、局部异常、语义偏移 | 全部 HKP 的表层信号 | 自然改写、合法旧版与污染都可能很相似 | `METHOD CONTRACT ACCEPTED`; `DIAGNOSTIC PROTOTYPE`; 非 Formal Detector |
| Entity-Claim | 实体—主张视角 | 主体、谓词、对象、数值、条件 | 哪个事实槽位发生变化 | HKP1、HKP2 | claim extraction 错误、隐含主体 | `METHOD CONTRACT ACCEPTED`; Pilot3 diagnostic |
| Provenance | 来源视角 | source、issuer、authority、引用关系 | 谁发布、是否匹配命题、来源链是否可信 | HKP4 | 来源信息缺失；Pilot3 中 35/36 为 N/A | `STRUCTURED PROTOTYPE IMPLEMENTED`; engineering only |
| Temporal-Version | 时间—版本视角 | 生效/失效时间、版本关系链 | 旧版、现版、修订与合法历史 | HKP3、部分 HKP2 | 版本链缺失或事实映射不完整 | `STRUCTURED PROTOTYPE IMPLEMENTED`; Pilot3 Temporal AUROC 0.465，仅诊断 |
| Retrieval-Behavior | 检索行为视角 | rank、score、邻域、冻结扰动 | 候选在 Top-K 和邻域中是否异常 | 全部 HKP 的运行时表现 | query 敏感、计算成本、分布漂移 | `METHOD CONTRACT ACCEPTED`; diagnostic primitive |

必须区分三层：

1. `METHOD CONTRACT`：五视角的允许输入、输出和边界已经作为 P1-R1 框架接受；
2. `DIAGNOSTIC PROTOTYPE`：Pilot3/Pilot4 已验证信号接口和部分结构化实现能运行，并暴露失败模式；
3. `FORMAL DETECTOR`：尚未实现，也没有建立 detection effectiveness。

详细方法合同见 [P1-R1 protocol](../s6_1_p1_r1_protocol_review_candidate.md)。

## 7. 多视角组合、消融和泛化

Single View 包括 S / E / P / T / R；Multi-view 可包含 S+E、S+T、E+P+T 和 All-5。组合必须在 formal protocol freeze
前确定，不能查看 test 结果后挑最好组合。

计划消融：minus Semantic、minus Entity、minus Provenance、minus Temporal、minus Retrieval，以及 without Hard Negative
training/calibration。消融回答“哪个组件真正贡献了性能”，也必须如实报告负贡献。

Track C 泛化计划：unseen HKP、unseen domain、unseen version family/pattern、cross-source transfer 和 adaptive attack。
这些都属于 `EXPERIMENTAL PLAN / NOT EXECUTED`。统计比较族、split 和阈值规则见
[P1-R1 protocol](../s6_1_p1_r1_protocol_review_candidate.md)。

## 8. Option B：轻量解毒

```text
Retriever
  -> Top-K
  -> Five-view Detector
  -> calibrated Risk Score
  -> Hard Filtering / Soft Downweighting
  -> New Top-K
```

- Hard Filtering：若 `risk >= tau`，则移除候选。
- Soft Downweighting：`adjusted retrieval score = retrieval score - lambda × risk`。

安全端要看 `Poisoned@K ↓`；效用端要看 `Recall@K / MRR / nDCG` 尽量保持。二者是分开的共同主结果，不能用一个综合
分数掩盖“安全提高但检索失效”。当前仅能说合同和工程 primitive 存在；Option B effectiveness 为
`NOT ESTABLISHED`，也不包含 trusted context package、完整可信上下文构造或端到端 Agent 防御。

## 9. 从开始到投稿：完整实验路线图

| 阶段 | 为什么做 | 主要工作 | 输入 | 输出 | 当前状态 | 结束条件 | 下一 Gate | 详细链接 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S6.1-LR1 | 选清研究路线 | 外部工作与 Paper1 对齐 | 论文/仓库 | 路线与角色 | ✅ 已验收 | Owner 接受 | R0 | [LR1](../stage_process/S6.1-LR1_work_process.md) |
| S6.1-R0 | 先查能否复现 | 代码/环境/工件预检 | 外部 baseline | 工程证据与 blocker | ✅ 带边界验收 | 证据可恢复 | FU1 | [R0](../stage_process/S6.1-R0_work_process.md) |
| S6.1-R0-FU1 | 关闭关键工程门 | 来源、bundle、5090 smoke | 冻结合同 | 单样本工程可行性 | ✅ 已关闭 | Owner 验收 | P1-R1 | [FU1](../stage_process/S6.1-R0-FU1_work_process.md) |
| S6.1-P1-R1 | 把想法变协议 | RQ、数据、方法、统计、Option B | LR1/R0/FU1 | 接受的框架 | ✅ 框架已接受 | 数值参数待 Pilot 冻结 | Pilot | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Pilot0 | 工程合同能否运行 | schema、split、泄漏 guard | synthetic fixture | 工程基础设施 | ✅ 已关闭 | 测试与 Owner 验收 | Pilot1 | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot1 | 真实中文来源能否构建 | 版本链、公开来源、候选包 | 官方公开文档 | 36 条候选与包 | ✅ 已关闭 | 来源/包可行 | Pilot2 | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot2 | 人能否可靠标注 | A/B、V2、agreement、owner 仲裁 | 36 条候选 | 36 条 Pilot-only GT | ✅ 可行性关闭 | GT/协议可唯一生成 | Pilot3 | [Pilot2 closure](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| Pilot3 | 信号能否运行 | 五视角 180 条 SignalRecord | Pilot2 GT | 弱信号/失败模式 | 🧪 已完成并停止 | 诊断报告 | Pilot4 | [Pilot3](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| Pilot4 first preflight | 人工发放前低成本检查 | 24 triplets/72 candidates/12-row sample | lessons + public sources | 首版 package | 📌 历史：退回修复 | Owner 指出缺陷 | targeted repair | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot4 targeted repair | 修复实质缺陷 | 语义、stealth、echo、applicability、独立 QA | 首版与 owner feedback | repaired 72 + second sample | 🔧 已完成 | 修复验证通过 | second preflight | [Current State](../../../governance/current_work_state.md) |
| Pilot4 second Owner preflight | 决定能否发人 | Owner 审查 repaired 12 rows | repaired workbook | targeted repair | 📌 历史：已触发 Repair-02 | Owner 明确决定 | Repair-02 | [Current State](../../../governance/current_work_state.md) |
| Pilot4 Repair-02 final preflight | 关闭第二轮系统性缺陷 | Owner 审查 final 16 rows | genuine-S3/S1/length/template/HN evidence | quality convergence | 📌 历史：已进入后续收敛 | Owner 明确决定 | Schema V3/V3.1 | [Current State](../../../governance/current_work_state.md) |
| Pilot4 Protocol hardening | 排除标签感知循环验证与候选核验路径泄漏 | locked Full72、candidate before/after、V3.1 三表 | b705cc + additive candidate version | 外部两阶段盲审路径 | 📌 历史：已进入外部盲审 | 阶段隔离完成 | Phase1 外部复核 | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot4 external Phase1 return | 锁定陌生复核者的第一阶段原始判断并拦截候选缺陷 | 原始 CSV、公开 Phase1 ID 集 | immutable return + 5-row blind triage | 项目负责人盲态处置 | ✅ 历史门已关闭 | fresh Attempt2 72/72 无候选缺陷 | Phase2 已完成 | [Current State](../../../governance/current_work_state.md) |
| Pilot4 targeted R3 | 检查局部协议修复及匹配控制 | 37 行外部 return、Guide V3.2、Expected/Evidence V2 | immutable raw + gate assessment | Expected V2 定向修正决定 | ⚠️ 当前 Owner 门 | 7-field/6-candidate additive decision | 同 raw 重算 gate | [Current State](../../../governance/current_work_state.md) |
| Pilot4 A/B 72 annotation | 获得独立人工判断 | Phase1/2、双锁定 | Owner-accepted package | 四份 returns | 📌 未批准/未开始 | returns hash-lock | agreement | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| Pilot4 agreement | 量化一致性 | 合法子集 agreement | A/B returns | agreement/disagreement | 📌 未开始 | 逻辑/一致性验证 | adjudication | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| Pilot4 adjudication | 解决必要分歧 | Owner 只裁决分歧 | minimal packet | 唯一决定 | 📌 未开始 | residual inconsistency=0 | GT | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Pilot4 72 Ground Truth | 形成小规模参考真值 | 确定性合并与 QA | validated returns/owner decisions | 72 Pilot GT | 📌 未开始 | identity/logic/leakage PASS | re-evaluation | [Experiment Master](../../../governance/experiment_master_record.md) |
| Pilot4 signal re-evaluation | 验证修复方向 | 重新运行 diagnostic signals | 72 Pilot GT | failure-mode comparison | 📌 未开始 | 诊断可解释 | readiness | [P1 process](../stage_process/S6.1-P1_work_process.md) |
| Scale Readiness Gate | 防止盲目扩规模 | 六类 readiness 审计 | Pilot4 closure | PASS/blocked | 📌 未开始 | 六类门均 PASS | Owner scale approval | [第17节](#17-什么情况下才能进入-240-group) |
| 240-group Scale Pilot | 验证规模/方差 | 5×4×3×4 groups | approved design | scale pilot data | 📌 未批准/未生成 | coverage/quality PASS | power analysis | [Research Plan](research_plan_authority.md) |
| Power / Precision Analysis | 决定正式样本量 | CI/方差/稀有组精度 | scale pilot | frozen sample plan | 📌 未开始 | 统计精度达标 | formal freeze | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Formal Dataset / Protocol Freeze | 锁定身份与分析计划 | data/split/license/metrics/seeds | accepted scale evidence | frozen contract | 📌 未开始 | Owner 明确批准 | implementation | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Formal Detector Implementation | 实现最终模型 | 五视角融合与校准 | frozen train/dev | executable detector | 📌 未批准/未实现 | tests + frozen identity | evaluation | [Research Plan](research_plan_authority.md) |
| Formal Detector Evaluation | 测主性能 | locked test evaluation | frozen detector/data | primary metrics | 📌 未开始 | evidence complete | multi-view | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Multi-view Evaluation | 验证组合收益 | single/multi-view compare | same split/budget | paired results | 📌 未开始 | preregistered comparisons | ablation | [第7节](#7-多视角组合消融和泛化) |
| Ablation | 解释组件贡献 | leave-one-view-out 等 | full method | contribution evidence | 📌 未开始 | planned family complete | generalization | [P1-R1](../s6_1_p1_r1_protocol_review_candidate.md) |
| Generalization | 测外推能力 | unseen domain/HKP/version/source | held-out families | generalization results | 📌 未开始 | frozen Track C complete | Option B | [第7节](#7-多视角组合消融和泛化) |
| Option B Detoxification | 测安全—效用权衡 | hard filter/soft downweight | calibrated risk | Poisoned@K + utility | 📌 未开始 | co-primary endpoints | paper evaluation | [第8节](#8-option-b轻量解毒) |
| Paper Evaluation | 汇总证据 | 统计、失败、威胁、复现包 | formal runs | tables/figures | 📌 未开始 | claims audit PASS | writing | [第18节](#18-什么情况下才能称为正式论文结果) |
| Paper Writing | 形成论文 | 方法、结果、局限、工件 | accepted formal evidence | manuscript | 📌 未开始 | Owner/导师审查 | submission | [README](../README.md) |

## 10. Pilot0–Pilot4：为什么每一步都需要

### Pilot0：工程合同可不可运行？

Pilot0 用 synthetic fixture 验证 schema、分组切分、泄漏 guard、攻击/Hard Negative 接口和 manifest 是否可执行。它避免在
真实数据上才发现基础设施错误。结论仅是工程基础设施可行。

### Pilot1：真实公开中文版本来源能不能构建？

Pilot1 审计公开中文版本链、来源许可边界和候选构造，形成 36 条非正式候选。它证明公开来源到盲化包的工程可行性，
不证明 Benchmark 已完成。

### Pilot2：人能不能可靠标注并形成 Ground Truth？

Pilot2 经历 schema 适用性、编码、旧值映射、独立复核和 owner 一致性门，最终形成 36 条 Pilot-only Ground Truth。它证明
标注协议与 GT 生成流程可行，也留下了不可回写的失败证据。

### Pilot3：五视角信号是否能运行、失败模式是什么？

Pilot3 在 36 条 Pilot-only GT 上生成 180 条 SignalRecord。它发现类别失衡、S1/S3 collapse、Provenance 35/36 N/A、
Temporal AUROC 0.465 和 Hard Negative 误报等问题。它是 diagnostic smoke，不是 Detector 性能实验。

### Pilot4：扩 240-group 前最后一次小规模校准

Pilot4 把 Pilot1–3 的教训前移到人工发放前：先设计 coverage 和 field schema，再构造并独立验证 24 matched triplets、
72 条平衡候选。首轮 preflight 被退回后只做 targeted repair。当前 repaired 72 仍是 preannotation candidates。

四个规模不能混淆：`36 records = development/diagnostic evidence`；`72 repaired candidates = balanced Pilot/preannotation
candidates`；`240 groups = future Scale Pilot`；`Formal Dataset = 未来经正式 freeze 的数据`。

## 11. 数据标注流程

```text
Candidate Generation
  -> Machine QA
  -> Owner Preflight
  -> A/B Phase1
  -> hash lock both
  -> A/B Phase2
  -> hash lock both
  -> agreement
  -> disagreement-only packet
  -> Owner adjudication
  -> Ground Truth
```

Phase1 评估候选自身可见的自然度、相关性、局部可检测性和隐蔽等级，不提前看到 Phase2 的官方事实材料。Phase2 用官方
来源和版本背景判断事实、版本、历史/更新和权威命题。盲法防止后一阶段答案反向污染第一阶段难度判断；A/B 独立可测量
协议是否清晰。

Owner 只在双方结果锁定后裁决必要分歧。Owner 的目的不是“提高 kappa”，而是形成可审计的唯一最终决定；agreement 必须
保留标注人真实差异。完整规则见
[标注教训与未来数据规则](annotation_lessons_learned_and_future_dataset_rules.md)。

## 12. 数据构造永久规则

- `subject uniqueness = 100%`：法律、政策、制度和标准主体必须可唯一识别。
- 候选与 query 必须 self-contained；不能依赖“该条例”“2017 年版”等隐含上下文。
- coverage before generation：先冻结覆盖矩阵，再生成文本。
- mutation semantic alignment：attack metadata 必须与实际事实变异一致。
- stealth evidence path：S1/S2/S3 必须来自发现错误所需证据路径。
- no evidence echo：候选不能回显标准答案或证据措辞。
- no experimental meta-language：候选不能出现“本样本”“对照组”等实验语言。
- applicability 必须 claim-derived，不能由生成器意图直接声明。
- `Generator != Validator`：构造者声明 PASS 不等于独立验证。
- G1–G14 全部门禁必须对序列化产物重新计算。
- independent Round D 必须从 source fact 反向核验。
- semantic near-duplicate 必须区分 triplet 内匹配与跨独立组泄漏。
- label isolation：Ground Truth/attack ID 不得进入 retriever 或 inference feature。
- raw return immutable：人工原始 return 不回写；纠正必须追加绑定。

唯一完整规则见 [canonical lessons](annotation_lessons_learned_and_future_dataset_rules.md)。

## 13. 已发生 Blocker 时间线

| 日期 | 阶段 | Blocker | 问题是什么 / 为什么重要 | 解决方案 | 状态 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07-31 | R0 | evidence mismatch | 首次 Worker evidence 与声明不匹配，无法复核 | corrected evidence + 本机 control-plane review | ✅ RESOLVED | [R0 process](../stage_process/S6.1-R0_work_process.md) |
| 2026-08-01 | W2 | model download/evidence blockers | 模型下载失败、磁盘命令来源不完整 | additive correction、offline bundle、H2 resume02 | ✅ `CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED`（仅工程门） | [FU1 process](../stage_process/S6.1-R0-FU1_work_process.md) |
| 2026-08-27 | Pilot2 | distribution metadata issue | 登记时间错误曾导出盲法污染推断 | 保留原记录，追加 owner-confirmed actual order | ✅ RESOLVED / 元数据历史保留 | [Owner correction](../s6_1_p1_pilot2_return_owner_correction.md) |
| 2026-08-27 | Pilot2 | Schema V1 ambiguity | YES/NO/UNCERTAIN、适用性和 authority 命题歧义 | Schema V2 + 独立复核 | ✅ RESOLVED | [Schema V2](../s6_1_p1_pilot2_annotation_v2.md) |
| 2026-08-27 | Pilot2 | NOT_APPLICABLE 缺失 | 正确或不适用命题被迫填错误枚举 | present/correctness dependency | ✅ RESOLVED | [Schema V2](../s6_1_p1_pilot2_annotation_v2.md) |
| 2026-08-27 | Pilot2 | encoding/header/process metadata | GB18030、列名和过程字段影响导入 | UTF-8 BOM 合同与缺陷显式保留 | ✅ RESOLVED | [Targeted review](../s6_1_p1_pilot2_targeted_rereview.md) |
| 2026-08-28 | Pilot2 | V1 mapping defect | 带中文后缀列未识别，旧值被伪装成 absent | allowlisted alias + fail closed | ✅ RESOLVED | [Targeted review](../s6_1_p1_pilot2_targeted_rereview.md) |
| 2026-08-28 | Future data | candidate subject ambiguity | 裸指代使样本缺上下文 | `BROKEN_CANDIDATE / MISSING_CONTEXT` 门 | ✅ RESOLVED AS PERMANENT RULE | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| 2026-08-31 | Pilot2 | agreement disagreements | 47 条 A/B 分歧 + 37 条内部逻辑冲突 | disagreement-only owner packet | ✅ RESOLVED | [Post annotation](../s6_1_p1_pilot2_post_annotation.md) |
| 2026-08-31 | Pilot2 | owner consistency blocker | 4 个候选有非法枚举/同字段冲突 | 独立 owner correction record | ✅ RESOLVED | [Closure](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| 2026-08-31 | Pilot3 | class imbalance | Clean 仅 1 条，无法支持正式估计 | Pilot4 平衡为 24/24/24 intent | ✅ RESOLVED FOR PILOT4 DESIGN | [Pilot3](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| 2026-08-31 | Pilot3 | S1/S3 collapse | 隐蔽等级证据路径不充分 | Pilot4 evidence-path stealth contract | ✅ RESOLVED FOR GENERATION | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| 2026-08-31 | Pilot3 | Provenance 35/36 N/A | 来源命题覆盖不足，视角不可估 | Pilot4 claim-derived applicability/coverage | 🔧 ENGINEERING REPAIR; formal effect open | [Pilot3](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| 2026-08-31 | Pilot3 | Temporal AUROC weak | 诊断 AUROC 0.465 | structured temporal/version repair | 🔧 PROTOTYPE REPAIRED; effectiveness open | [Pilot3](../s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) |
| 2026-08-31 | Pilot3 | HN FP | 合法版本差异产生误报 | 六类 HN 与结构化调整 | 🔧 DESIGN REPAIRED; formal effect open | [Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| 2026-09-01 | Pilot4 | attack metadata misalignment | metadata 与实际变异可能不一致 | mutation-semantic contract + rejection | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | stealth index assignment | S 值由目标格赋值而非证据路径推导 | evidence-path derivation | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | evidence echo | LONG 候选回显答案/证据 | natural rendering + echo blocker | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | experimental meta-language | 文本含实验描述，形成捷径 | meta-language rejection | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | applicability metadata | 适用性由 metadata 意图而非 claim 推导 | claim-derived applicability | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | builder-declared PASS | 构造器自报通过，未验证序列化产物 | independent G1–G14 + Round D | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | HN evidence weakness | 困难负例证据链过弱 | source-fact reverse check | ✅ RESOLVED IN REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | Repair-01 acceptance | 第二次预审发现 S3 necessity、S1 cue、实际长度、模板与 HN 语义问题 | Repair-02 | ✅ SUPERSEDED BY FINAL REPAIR | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | final preannotation acceptance | Repair-02 工程门完成但尚无人工作出接受决定 | quality convergence | ✅ SUPERSEDED BY FULL QUALITY GATES | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-01 | Pilot4 | source/schema/visibility convergence | Phase1 hint、人工跨文档、伪来源核验、HN 支持与字段可操作性存在系统性风险 | actual-source verification + Schema V3 + full72 + dry-run | ⏳ READY FOR OWNER ACCEPTANCE REVIEW | [Current State](../../../governance/current_work_state.md) |
| 2026-09-01 | Pilot4 | duplicate visible evidence slots | 55/72 candidates、23 triplets 的 E1/E2 指向同一 visible official URL | 23 verified companion sources + distinct URL/hash/document identity + A/B independent order + Schema V3.1 | ✅ RESOLVED / OWNER ACCEPTANCE PENDING | [Current State](../../../governance/current_work_state.md) |
| 2026-09-02 | Pilot4 | sample-ID leakage | 早期 Full72 reviewer 可用 `sample_id` 查询隐藏标签集合，脱敏输入不等于真实标签盲法 | 旧结果追加重分类为 contaminated evidence；使用一次性 opaque ID、隔离 mapping 与外部复核路径 | ✅ ENGINEERING REPAIR / FINAL OWNER ACCEPTANCE PENDING | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-02 | Pilot4 | combined Phase1/Phase2 packet flaw | 第一阶段候选与第二阶段证据同时进入一个 LLM 上下文，“先别看 Evidence”不能保证严格盲法 | 保留 combined packet 历史；重建 candidate-only Phase1、withheld Phase2 与 return hash-lock 释放门 | ✅ PHASE-SEPARATION REPAIR / EXTERNAL PHASE1 RETURN PENDING | [Current State](../../../governance/current_work_state.md) |
| 2026-09-02 | Paper 1 governance | documentation closeout gap | 代码、测试或 push 完成后，人类总账和控制面文档仍可能停留在旧任务 | 每项 Paper 1 任务强制执行文档收口清单和跨文档陈旧状态门 | ✅ POLICY ACTIVE | [Closeout contract](../documentation_separation_contract.md) |
| 2026-09-02 | Pilot4 | external Phase1 candidate defects | 外部 blind reviewer 在 Attempt1 的 72 行返回中标记 5 条候选缺上下文、指代模糊或其他局部问题；在处置前释放证据可能把候选缺陷带入 Phase2 | 原始 return 不回写；blind-ID triage、Owner 五项处置、局部修复与 fresh Full72 Attempt2 | ✅ `RESOLVED BY FRESH ATTEMPT2 ZERO-DEFECT RETURN` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-02 | Pilot4 | final-corpus blind review consistency | Owner 接受五项 reviewer issue；若只重标五条并与旧 67 条拼接，会混合不同 corpus/reviewer 的证据 | 五条 source-backed 局部修复；67 条不变；统一 final72 生成 72 个新 ID 与 fresh Full72 Attempt2；Attempt1 永久保留为 defect-discovery evidence | ✅ `ATTEMPT2 PHASE1 LOCKED / PHASE2 RELEASED` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-02 | Pilot4 | final Phase2 expected comparison | 首次返回有 23 条临时访问限制；retry 后全 0，但对比暴露 16 条 primary status 边界、expected/minimum-evidence 问题与一条缺失版本证据 | 两份 raw 分别锁定；raw lock 后才解锁 mapping/expected；生成完整 mismatch taxonomy 和定向修复建议 | ⚠️ `OWNER PROTOCOL ACCEPTANCE PENDING / RECOMMEND TARGETED REPAIR` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-03 | Pilot4 | targeted R3 gate failure | R3 raw 37/37 完整，M4/M8 通过；M2 3/16、controls overall 13/16，且 7 个分歧字段由 Expected V2 缺陷解释 | 保留 R3 raw 与 Expected V2；只申请 additive Expected V3，批准后复用同一 raw 重算，不默认 R4 | ⚠️ `EXPECTED_V2_SYSTEMIC_REPAIR_BLOCKER / OWNER DECISION PENDING` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-03 | Pilot4 | Expected V3 gate closure | Owner 批准 7 字段/6 候选定向修正；V3 在 reviewer load 前由 Guide/Evidence 独立锁定；M2 2/16、controls 16/16、all exact 35/37、A–F PASS | 停止校准，不做 R4；提交 Owner Protocol Final Decision Packet，协议和 A/B 分开审批 | ✅ `CALIBRATION STOP MET / OWNER PROTOCOL DECISION PENDING` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-03 | Pilot4 | Owner protocol acceptance and A/B preflight | Owner 以 nonblocking notes 接受协议并关闭校准；Accepted Stack V1 固定 Final72、Guide V3.2、Expected V3、Evidence Pool V2 与冻结快照+URL provenance；2 条 variance 原样保留 | 提升 13 条证据支持的 lesson；重建 A/B 角色、盲法、双阶段锁定、agreement/Owner 仲裁边界并生成审批包；不发包 | ✅ `PROTOCOL ACCEPTED / A_B EXECUTION APPROVAL PENDING` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-03 | Pilot4 | A/B execution approval and Phase1 packets | Owner 指定 HUMAN-A01/HUMAN-B01 两个不同真人，确认完整隔离、互不看结果和禁用 LLM；批准完整 Final72 A/B execution 与 Phase1 分发 | 各自 72 新 ID/独立顺序，两个五文件 Phase1 包；Phase2 各 144/144 快照预构建但封存 | ✅ `A_B EXECUTION APPROVED / BOTH PHASE1 READY / WAITING OWNER DISTRIBUTION / PHASE2 WITHHELD` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-03 | Pilot4 | A/B human usability V2 | Owner 在实际发放前发现 V1“协议正确但不像给真人看的说明书”；本轮只补字段含义、枚举边界、decision flow、教学与完整填写例、reason 写法、CSV 操作和自检 | V1 不改且未分发；A/B Candidate/ID/顺序不变；三列 Packet 只读、五列 CSV 专门答题；Phase2 人类说明预构建但继续封存 | ✅ `RULE CHANGE 0 / BOTH PHASE1 V2 DISTRIBUTION READY / PHASE2 V2 WITHHELD` | [Execution log](../../../governance/research_execution_log.md) |
| 2026-09-09 | Pilot4 | Phase2 human annotation rework risk control | 双 Phase1 已锁定、Phase2 获准释放后，Owner 在分发前要求确认七字段是否容易导致大规模返工；V3 的内部跳转、保护状态和说明密度不够适合真人连续填写 | 先做只读风险审计；不改协议，只把官方 URL 放到 Candidate 同行、保留冻结快照作备份、移除工作表保护并扩展 Guide V4 | ✅ `SEMANTIC BLOCKER FALSE / A_B V3.2 READY / WAITING OWNER DISTRIBUTION` | [Execution log](../../../governance/research_execution_log.md) |

## 14. 当前项目状态

- `PILOT4_AB_ALL_FOUR_RAWS_LOCKED / OWNER_ADJUDICATION_RETURN_RAW_LOCKED / OWNER_ADJUDICATION_CONSISTENCY_CLOSED / UNRESOLVED_CONSISTENCY_BLOCKER_0 / EXPECTED_V3_NOT_LOADED / NO_GROUND_TRUTH_YET / WAITING_FOR_OWNER_NEXT_APPROVAL`
- `PILOT_LEVEL_ANNOTATION_READINESS_ONLY`
- `PILOT4_A_B_EXECUTION_APPROVED / PILOT4_AB_DUAL_PHASE1_RAW_LOCKED / PHASE2_RELEASE_ALLOWED`
- 历史预检状态 `NO_HUMAN_DISTRIBUTION` 已被本轮 Owner 分发批准取代；它仅作为时间线事实保留，不能描述当前授权。
- `PILOT4_CANDIDATE_CORPUS_POST_EXTERNAL_PHASE1_REPAIR_V1` 已形成 72 条；仍非 Ground Truth、非 Formal Benchmark、非 frozen Dataset。
- class intent 为 Clean / Poison / Hard Negative = `24/24/24`。
- 生成覆盖为 `4 HKP × 3 intended-S × 2 replication = 24 poison cells`，对应 24 matched triplets。
- Attempt1 72-row 原始返回继续按 `5001 bytes` 与 SHA256 `59446c4b...889261` 完整保留；它是有效的缺陷发现证据，不是 final corpus acceptance review。
- Owner 接受五条 issue；五条局部修复的 semantic/source parity 均为 `5/5 PASS`，其余 67 条 candidate text 与源行 byte-identical。
- Attempt2 使用 72 个新 opaque ID，Attempt1 ID 复用为 0；canonical raw SHA256 为 `1e5e81fe...63c9c5`，schema/72 IDs/
  enums/7 reasons PASS；59 条 NATURAL、13 条 MINOR_ISSUE、7 条局部冲突，且 72/72 `phase1_issue=NONE`。六项 release
  fact 全部为 true。第一份 Phase2 raw 的 23 条 `SOURCE_UNREACHABLE` 作为过程证据保留；同一 reviewer retry 的 final raw
  将其降为 0，并以 `16321 bytes` / SHA `6f6cc042...92f1` 锁定。raw-lock-before-expected PASS；Phase1/Phase2 exact 分别
  `58/72` 与 `48/72`。43 个 mismatch 的 taxonomy 为 M1=13、M2=16、M4=3、M5=6、M8=4、M9=1。
- Targeted R3 raw 保持 `12062 bytes` / SHA `80a10a1e...0b4441`。Expected V3 先经 reviewer-blind 独立审计锁定，再加载 raw；
  只改 7 字段/6 候选。V3 overall `35/37`、version/authority/minimum/issue 各 `37/37`、exact `35/37`；M2 `2/16`、
  controls overall/exact `16/16`，M4/BR18 和 M8 4/4 通过，A–F 全部 PASS；只剩 2 条非系统性 reviewer variance。
- A/B Phase1 与 Phase2 已由两位真人独立完成并完成四 raw lock；dual Phase2 gate 后 mapping 已解锁并完成 agreement preflight；Expected V3 未加载。当前有 78 个 material field disagreements（40 samples）与五个 late-candidate-defect flags 待 Owner 裁决；72 Ground Truth 未建立；
  240-group 未开始；Dataset = `NOT FROZEN`（未冻结）。
- Formal Detector = `NOT IMPLEMENTED`（未实现）；Formal Experiment = `NOT STARTED`（未开始）；Our Method Result = `NONE`。

当前 Git 身份与远端同步状态必须动态核验；`a843697`、`cad3b2b2` 与 `871aecf` 均作为不可变历史身份保留。

## 15. 当前下一步

唯一当前动作：**Owner 决定是否批准 `P1-RETRIEVAL-BEHAVIOR-SIGNAL-HARNESS-01`。** 该任务应冻结合法 query、retriever、
corpus、top-k、score 和 repeated-run trace，再补齐 Retrieval View。当前也可以另行讨论四视角 prototype，但任何 Detector
training、threshold tuning、240-group 或正式结果都必须是独立审批，不能由本轮自动继续。

```text
Attempt1 (immutable defect-discovery evidence)
  └─ five Owner-accepted defects -> five repaired + 67 unchanged -> unified final72
       └─ fresh opaque IDs + fresh order -> Attempt2 Phase1 in new isolated reviewer context
            └─ immutable return + zero defects -> Candidate Quality Gate PASS -> same-reviewer Phase2
                 └─ Guide/Expected/Evidence targeted repair -> R3 locked and compared
                      └─ additive Expected V3 -> same-raw gates A-F PASS
                           └─ Owner accepted with nonblocking notes -> calibration closed
                                 └─ A/B approved + roster frozen + V1 preserved but human-usability superseded
                                      └─ V2 manuals/packets ready, Phase2 V2 withheld
                                           └─ dual Phase1 raw locked -> Phase2 V3.2 UX repaired without semantic changes
                                                └─ A/B complete -> Owner adjudication -> Final72 GT accepted
                                                     └─ label-blind 42-signal extraction -> raw lock -> analysis
                                                          └─ current: READY_WITH_VIEW_LIMITATIONS / Retrieval input gap

未来在独立审批下：
Retrieval harness -> optional first multiview detector prototype -> Scale Readiness -> Owner 单独批准 -> 240-group
```

## 16. 论文实验指标

### Detection

- AUPRC：在污染稀少、类别不平衡时，比总体 accuracy 或单独 AUROC 更直接反映“检出的污染有多少是真的”。
- AUROC：看全阈值排序能力，但必须与 prevalence、AUPRC 和低 FPR 指标一起解释。
- Recall@1% FPR：只允许 1% 正常样本被误报时能找回多少污染；真实系统中低误报非常重要。
- Hard Negative FPR：合法历史/更新/例外被误杀的比例，是 Paper 1 的关键指标。
- F1：Precision 与 Recall 的调和平均；依赖阈值和 prevalence。
- Calibration：风险分数是否能支持可解释的阈值决策。

### Retrieval

- Poisoned@K：Top-K 中污染暴露，越低越好。
- Recall@K：相关正常内容是否仍被保留。
- MRR：首个相关结果是否靠前。
- nDCG：多等级相关结果的整体排序质量。

详细统计、配对比较、CI、Holm correction 和主要终点见
[P1-R1 protocol](../s6_1_p1_r1_protocol_review_candidate.md)。

## 17. 什么情况下才能进入 240-group

Scale Readiness Gate 必须至少同时通过六类检查：

| 类别 | 必须回答 |
| --- | --- |
| DATA | Pilot4 72 候选/GT 的平衡、自包含、匹配和失败模式是否支持扩规模？ |
| ANNOTATION | A/B 流程、适用性、agreement 和 owner 仲裁是否可重复且成本可控？ |
| SIGNALS | 五视角 signal 是否有足够覆盖、方向正确、缺失机制可解释？ |
| LEAKAGE | exact/normalized/semantic/template/entity/version/label leakage 是否 fail closed？ |
| SOURCE | 五领域来源、版本链、许可与发布策略是否可追溯？ |
| METHOD | Formal Detector 的输入、融合、校准、baseline fairness 和资源计划是否可冻结？ |

Pilot4 PASS 只关闭小规模校准门，**不自动启动 240-group**。Scale Readiness PASS 后仍需 Owner 单独批准。

## 18. 什么情况下才能称为正式论文结果

| 层级 | 能说明什么 | 不能说明什么 |
| --- | --- | --- |
| Engineering Validation | 代码、schema、环境、接口或证据链能运行 | 方法有效、可泛化 |
| Pilot Diagnostic | 小样本暴露方向、失败模式和协议问题 | 总体性能、最终论文数字 |
| Scale Pilot | 估计方差、样本量、覆盖和资源 | 正式 test 结论，除非协议明确规定 |
| Formal Experiment | 冻结数据/代码/参数/统计计划下的结果 | 未经 claims audit 的论文主张 |
| Paper Result | 通过证据、统计、复现和结论边界审计的正式结果 | 超出协议和数据支持的 SOTA/生产安全承诺 |

例如 Pilot3 Temporal AUROC `0.465` 只能写成“小样本诊断暴露弱时间信号”，不能写成 Paper 1 最终性能。正式论文结果
至少要求 Dataset/Protocol Freeze、正式 Detector 身份、预注册比较、locked test、统计不确定性、失败处理、完整 evidence
index 和 Owner 对 claims 的接受。

## 19. 文件导航：想了解更多应该看哪里

| 我想看什么 | 应该打开哪个文件 |
| --- | --- |
| 5/15/30 分钟掌握 Paper 1 | 本文件 |
| 目录总入口与文件分类 | [Paper 1 README](../README.md) |
| 当前研究方向与边界 | [Research Plan Authority](research_plan_authority.md) |
| 详细实验协议、RQ、指标和统计 | [P1-R1 protocol](../s6_1_p1_r1_protocol_review_candidate.md) |
| 数据标注经验与未来规则 | [Annotation Lessons](annotation_lessons_learned_and_future_dataset_rules.md) |
| Pilot 实际过程 | [S6.1-P1 Work Process](../stage_process/S6.1-P1_work_process.md) |
| 当前正在做什么/禁止什么 | [Current Work State](../../../governance/current_work_state.md) |
| Owner 已确认决定 | [Project Owner Decision Register](../../../governance/project_owner_decision_register.md) |
| 实验控制面与证据索引 | [Experiment Master Record](../../../governance/experiment_master_record.md) |
| 按时间查看执行历史 | [Research Execution Log](../../../governance/research_execution_log.md) |
| AI/Codex 结构化恢复上下文 | [Agent Experiment Ledger](../agent/experiment_ledger_agentUse.md) |
| 人类/机器/证据如何分层 | [Documentation Separation Contract](../documentation_separation_contract.md) |
| 为什么本轮不移动文件 | [Document Inventory](../document_inventory.md) |

> STOP：A/B execution 和 Phase1 分发已由 Owner 批准，但真实分发尚未登记；Owner 现在只分发各自六个 Phase1 V2 文件，V1 不得发送。
> 两份 Phase1 锁定前不释放 Phase2；四份 raw 锁定前不做 agreement；当前不生成 Ground Truth，也不启动 240-group、
> Dataset freeze、Detector、训练、5090 或 Formal Experiment。
# 2026-09-16：系统开始自己找可信证据

过去的信号实验已经知道“这条 Candidate 应该看哪两篇 E1/E2”，只能算诊断上限。本轮先把所有官方快照合并成统一的 57 文档库，隐藏每条 Candidate 的 E1/E2 对应关系，再让 Sparse、Dense 和 Hybrid 检索器自己找证据。检索结果锁定以后，才拿人工对应表检查找得准不准。

结果说明这条路可行但还没完全成熟：Sparse/Hybrid 在这个小型冻结库里表现较好；Version Registry 只有部分版本时间和 current/history 关系，因此 21 个原 Oracle-dependent signals 有了合法替代路径，8 个 Temporal signals 仍不能部署。项目已经从 Benchmark diagnostic 跨到 deployable method prototype，但还没有训练 Detector，也没有论文结果。

# 2026-09-17：先排查“检索器是不是靠题面提示”，再冻结检测器输入

本轮没有训练检测器。我们先补齐冻结官方材料中可以直接证明的版本、机构和有效期信息，再把每条查询做成四种形式：完整信息、去掉来源标题、只用候选正文、只用结构化命题。结果显示，去掉来源标题没有造成实质下降，说明当前原型不是主要靠标题找答案；但自由文本比结构化查询明显更强，说明它仍可能依赖词面重合。这个风险已明确登记，不能把当前高召回当作正式方法效果。

在不看标签、不把缺失当安全、不使用人工 E1/E2 选证据的前提下，项目冻结了第一版 23 项 S/E/P/T 原始特征。它们只是将来模型的输入材料；R 检索行为属于第二阶段，尚未合入。当前可以进入受限的 Detector 开发设计，但下一步应先改善检索难度和结构化查询鲁棒性，再申请训练批准。

# 2026-09-21：第一版 Detector 为什么还没有开始训练？

训练本来计划使用 Leave-One-Group-Out：每次把一个完整的 Clean/Poison/HN 三元组留作验证，其余 23 组训练。这样同一事实/version chain 的三个样本不会跨训练和验证，比随机拆 72 条更能防止泄漏。

但正式 fit 前发现，23 个冻结特征中的 `host_publisher_relation` 和 `publisher_issuer_match` 在所有 72 条里都没有值。训练折既算不出 mode，合同也没有规定“缺失等于 0”。如果 Codex 自己填 0、删掉两列或增加“缺失”特征，就等于改了 Owner 刚冻结的输入规则，而且可能让缺失状态变成类别捷径。因此本轮停在 Phase A：24 组 LOGO 结构已经验证，模型一次也没有 fit，没有 AUROC/AUPRC。Owner 需要决定是补上游 provenance 数据、明确批准恒定工程表示，还是版本化为 21-feature 合同。

# 2026-09-22：输入合同已经修好，但还没有训练模型

负责人这次给了明确顺序：优先从已有官方材料补真实来源信息；不允许把两项全缺失特征填成 0 或加“是否缺失”列；如果现有证据仍无法按原含义计算，就单独冻结 21 列版本。审计发现，官方文档虽然部分记有网站、发布者和机关，但这不等于我们已经知道“候选文档”与这些机构的对应关系。尤其网站域名不能直接当作发布机关；也不能从 Top5 检索文档里挑一篇最支持某个类别的来给候选赋值。所以优先修复未能成立，按负责人事先批准的后备方案保留其他 21 项，旧 23 项原样留档。

新版输入经过了 24 折逐折检查：每次只在训练组里都有足够真实值来计算缺失填补统计量；被排除的两列在三类样本中都是同样缺失，不构成这两列自身的类别捷径。这只是证明“可以安全地开始下一次开发集模型运行”，不是已经训练，更没有准确率或论文结论。Final72 仍只用于方法开发。正式 240 组数据必须在构造时就把网站、页面发布者、文件制定机关和来源链采集齐，不能以后靠人工答案补。[详细审计报告](../method_engineering/PAPER1_DOCUMENT_DETECTOR_MISSINGNESS_OWNER_RESOLUTION_REPORT_V1.md)。
