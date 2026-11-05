# Current Work State

## 当前工作 — 5060 Pilot12 D1 暂定评价完成（2026-11-05 JST）

`OWNER12_LIVE_108 / D1_AI_PROVISIONAL_EVALUATION_01` 已完成零 API 后封存确定性评价。108 格原始响应及 36 世界、12 题映射通过核验，18 格暂定合理拒答，51 格拒答和 39 格回答整体未决。两过滤配置降低 Token，G2 较 G0 净少 4 格回答，其中 Clean 净少 2 格。当前基线效果证据不足，Human Gold 0、target 未知、正式 ASR/QA/C3 未测。待独立人工裁决语义及证据充分性，本轮停止。

[暂定效果评价和证据](../paper1/dual_machine/chinese5060/pilot_rapid_live/PILOT12_D1_AI_PROVISIONAL_EFFECT_REPORT.md)。以下为历史快照。

## 当前工作 — 5060 Owner12 Pilot12 V2 真实生成完成（2026-11-05 JST）

`W1-5060-RAPID-LIVE-20261105-01 / OWNER12_LIVE_108`，`RAPID_LIVE108_COMPLETED`。原 Owner12 加单批费用豁免，冻结 V2 首 3 格工程通过并完成余 105 格。真实 POST 108、HTTP 200 共 108、成功 108、失败 0、未运行 0、重试 0。回答 39、拒答 69，输入 44426、输出 5154 Token，公开价估算 CNY 0.130084，账户实扣未核。Human Gold 0、target 未知、正式 ASR/QA/C3 未测、暂定评价未运行。一次运行授权用毕，文档收口后停止。

[真实结果和证据](../paper1/dual_machine/chinese5060/pilot_rapid_live/RAPID_LIVE_OWNER12_EXECUTION_RESULT.md)。以下为历史快照。

## 当前工作 — 5060 Owner12 V2 首发前资金核验阻断（2026-11-05 JST）

W1-5060-RAPID-LIVE-20261105-01，`RAPID_LIVE_BLOCKED_MINIMAL_ACTION_REQUIRED`。按 Owner12 固定合同 `223ea98c1f72cd24c0a4ded35e7b9af42816ad9f` 完成首发前只读核验。缺当前全线资金数值快照，`HUMAN_DECISION_REQUIRED / Auto Continue = NO`。真实 POST 0，108 格未运行，新增费用 USD 0，Human Gold 0，正式 ASR/QA 未测。4096 后置 usage 已授权。实发文本权利裁决和运行放行改动在硬门后停止。下一项仅需带时间的 USD 全线结算/在途上界及北京账户可用资金下界。

[准入证据与下一项](../paper1/dual_machine/chinese5060/pilot_rapid_live/RAPID_LIVE_OWNER12_RESULT.md)。以下为历史快照。

## 当前工作 — 5060 Owner12直接加速真实Pilot12 V2：风险受限后置usage、首3成功继续105（2026-11-05 JST）

Owner `W1-OD-20261105-5060-RAPID-LIVE-12`批准不再循环证据准备，而是优先真实D1开发生成：唯一5060分支36固定世界×G0/G1/G2、108格、80唯一prompt，V2固定Qwen3.7 Plus快照，首3格工程通过后即继续余105，不另审批。Owner明确接受因当前闭源chat模板不可验证而将项目4096 Token门从事前严格证明改为**逐格回包后真实`usage.prompt_tokens`检查**，最多一个超界请求可能产生外传/费用并立即停发；不能静默放宽数值或重试。预算同时按107正常+单个最大991808超界、高费率、输出266候选/格+>=20% reserve，并持续守USD25警戒/28不新发/30累计硬限。
准入最小剩余：原D1 46来源已有身份（15法规、2官方网页、29候选），需要一次核实Owner控制及第三方外传有权、无明知禁传/PII；复用已封存北京Workspace region/host+适用现有账户，不猜授权地域；本地实际历史费用/余额/在途和保守资金硬门需可数值计算。Runner旧live编译锚应仅受控改为验证Owner12 Git原件+独立Checker事实证据，允许门全PASS即**一次**实际运行；门未过则首格前STOP且最多报告一个精准缺项，不再建新Fast-Unblock。用户本次许可**不代替**无法归Owner控制的第三方材料权利。
当前仅授权刚写入Git：**不能声称已开始真实API**，此前实跑仍0/108、费用USD0、HumanGold0、正式ASR/QA NOT_MEASURED。旧V1/新V2/source/filter SHA不可改、不做D2D3或5090、B5/B6。执行结果应报告真实108格及开发暂定一致性，不能把暂定参考当正式GT或ASR。
[Owner12授权](../paper1/dual_machine/owner_approvals/W1_5060_PILOT12_RAPID_LIVE_OWNER_AUTHORIZATION_20261105.md)；[直接执行Prompt](../paper1/dual_machine/chinese5060/W1_5060_PILOT12_RAPID_V2_LIVE_EXECUTION_PROMPT_V1.md)。以前快照不覆盖。

## 当前工作 — 5060 Pilot12 来源与历史账本已恢复，真实准入仍阻断（2026-11-05 JST）

W1-5060-EVIDENCE-RECOVERY-20261105-01，EVIDENCE_RECOVERY_PARTIAL_BLOCKED。沿用Owner W1-OD-20261105-5060-FAST-UNBLOCK-11，控制合同 f0036bdb6877aca9946e9d048e9d7aa285ef515b。
46/46文档字节身份核验，29/29未匹配项追到签署D1候选，381片段出现核对。恢复旧北京Workspace及361份历史收据，估算CNY7.611826，历史未配对预留0。当前外传/敏感性、账号/计费/统一账本及严格Token证明仍缺。
严格证明0/108；后置usage风险路径仅提案，原4,096门和V2不变。真实API0、费用USD0、108 NOT_RUN、HumanGold0、target未知、正式ASR/QA未测。下一步合并三个证据或裁决项，真正执行另批。

[Evidence Recovery Addendum](../paper1/dual_machine/chinese5060/fast_unblock/FAST_UNBLOCK_EVIDENCE_PACKET.md)。以下为历史快照。


## 当前工作 — 5060基于Owner11继续有限离线证据恢复，不重新批准真实调用（2026-11-05 JST）

Owner在`FAST_UNBLOCK_PARTIAL_BLOCKED`回报后指示“那继续”。此为已有`W1-OD-20261105-5060-FAST-UNBLOCK-11`许可内的继续调查，**不新增真实API或调整科学安全门的批准**。执行范围仅：从冻结D1/P2片段追溯46个拟外传`source_document_hash`（17已匹配原source snapshot、29尚未匹配），清楚区分来源无法匹配与没有使用权；按既存本机资料核百炼唯一region/workspace/已核费率和私有USD账本；利用官方Qwen3.7 Plus 991808 token最大输入长度/byte-BPE文献检查自设4096严格门的可证明性，若不能证明，只提交需Owner另行明确批准的有风险替代方案，不得把猜测上界升格为PASS。
V1/V2全部SHA、模型/原108格/科学参数、旧封存不变；真实0调用、全部108 NOT_RUN、未解D1外传权限不能伪造、C盘禁新项目可控写入、D/E>=20GiB、USD25/28/30合同保留；D2D3、5090不触碰。终点仅简短Evidence Recovery Addendum与最多3项待Owner裁决；完成后STOP。
[从Git直接执行的短路径指令](../paper1/dual_machine/chinese5060/W1_5060_PILOT12_EVIDENCE_RECOVERY_SHORT_PATH_PROMPT_V1.md)。此条只登记新任务指令，**未宣称执行完成**，以前快照不覆盖。

## 当前工作 — 5060 Fast-Unblock 离线验收完成，真实准入仍阻断（2026-11-05 JST）

W1-5060-FAST-UNBLOCK-20261105-01，FAST_UNBLOCK_PARTIAL_BLOCKED。Owner W1-OD-20261105-5060-FAST-UNBLOCK-11，控制合同 ea7e7d6a585ac96dddf3d1c2dcc37113ee460612，离线源码 43be925d57ef6fbe9cbb27d22c7f1495373c6204。
V2原108格独立逐格核验，仅输出上限字段名改为max_completion_tokens，值256。V1字节保全。候选输出账本以266预留。64项离线测试，合成108/108，真实API 0、费用USD0、108 NOT_RUN。Human Gold 0，target未知，C3/正式ASR/QA NOT_MEASURED。
A缺46个实发源的外传范围和敏感性裁决，B缺账户唯一地域端点和实际计费证明，C严格输入证明0/108，D缺统一数值账本，E合成正向和拒绝验收通过但真实许可尚缺。待全部证据闭合后由新Owner真实执行批准绑定V2及源码。

[唯一审批入口](../paper1/dual_machine/chinese5060/fast_unblock/FAST_UNBLOCK_EVIDENCE_PACKET.md)。以下旧当前标题均为当时历史快照。


## 当前工作 — Owner批准5060 Pilot12 Fast-Unblock一次性离线解阻，真实API仍0（2026-11-05 JST）

新Owner决策`W1-OD-20261105-5060-FAST-UNBLOCK-11`仅允许5060继续独立分支在本地/D-E完成剩余执行证据：A冻结D1来源允许第三方外传/敏感性/处理方地域，B百炼固定`qwen3.7-plus-2026-05-26`对应唯一官方地域端点与真实传输**正向代码及Fake模拟**，C全108格经可复核Tokenizer/chat template或严格上界证明输入4096门，D本机全工作线USD数值账本及25/28/30硬门，E独立checker、输入SHA/唯一字段diff和收口证据。**不得发任何真实HTTPS/生成API请求或在线count-tokens/探测，不下载安装新依赖/模型；真实108格继续NOT_RUN。**
若证明原`max_tokens=256`无法控制完整计费输出，可在Owner11唯一批准范围内仅把这个字段改为`max_completion_tokens=256`并删除旧key，原V1保留，另封新V2全108请求与新proposal/预算SHA，做独立离线QA及公平性声明，需考虑官方提及最多10 token偏差；其他scientific inputs, model, prompt, TopK, temperature, scopes全不变。若无需改则V1不变；如需同时改其他字段必须另报Owner。不管所有静态Gate是否PASS，本次任务结束都只能`FAST_UNBLOCK_READY_FOR_OWNER_LIVE_APPROVAL`或`FAST_UNBLOCK_PARTIAL_BLOCKED`，**必需新Owner运行批准后才可解锁真实请求**，不能凭旧Owner10继续发送。
前次`LIVE_GATE_BLOCKED_NO_REQUESTS` HEAD`731b48419aba2dab3b8ded310d349fcf441c3f1b`的A–E阻断与旧历史原样保留；旧P2/PAIR01、36世界/三臂108格/80唯一prompt、29Hit/7MISS、HumanGold0/target UNKNOWN/正式ASR与QA NOT_MEASURED不变，FastC因果未识别、B2 Clean误删上升仍为警示。Owner已核账户/地域/费率/余额仅为OWNER_ATTESTED，不索重复截图/密钥，但实用机器账本不能编造。5090独立分支/D2D3不受影响。C盘禁项目可控新增、D/E≥20GiB；新增真实API费用USD0。
[Owner正式十二字段授权](../paper1/dual_machine/owner_approvals/W1_5060_PILOT12_FAST_UNBLOCK_OWNER_AUTHORIZATION_20261105.md)；[Fast-Unblock Git原生完整Prompt](../paper1/dual_machine/chinese5060/W1_5060_PILOT12_FAST_UNBLOCK_EXECUTION_PROMPT_V1.md)。唯一下一次审批入口：`docs/paper1/dual_machine/chinese5060/fast_unblock/FAST_UNBLOCK_EVIDENCE_PACKET.md`（由5060本轮完成）。此前所有当前节均是历史记录，不覆盖。

## 当前工作 — 5060 Pilot12 准入拒绝，真实请求 0（2026-11-05 JST）

W1-5060-PILOTLIVE-20261105-01，LIVE_GATE_BLOCKED_NO_REQUESTS。Owner W1-OD-20261105-5060-PILOT12-CONDITIONAL-LIVE-10，合同 312f9b17dba2a20c142507ce7df5ec7ae203642d，候选源码 4826ddbf5721e748c499198af931be984807a0db。
108格投影逐字通过，A–E整体未过。真实POST 0、成功0、失败0、未运行108，首3 NOT_RUN，新增费用USD0。无可签发的全PASS manifest。缺逐源外传范围、获准唯一地域端点和256计费上界、严格输入Token、全线预算证据及相应机器放行链。
46项离线测试、Ruff/MyPy通过。Human Gold 0，target未知，独立暂定评价NOT_RUN，C3/ASR/正式QA NOT_MEASURED。下一步仅在证据闭合且经授权恢复时复核，首3与余105的条件权限仍为同一合同。

[本轮准入和封存](../paper1/dual_machine/chinese5060/W1_5060_PILOT12_CONDITIONAL_LIVE_RUN_REPORT.md)。以下旧当前标题均为当时历史快照。


## 当前 / CURRENT — Owner原则授权Pilot12单次3+105有条件真实RAG生成，所有准入证据未闭合前0 API（2026-11-05 JST）

Owner批准`W1-OD-20261105-5060-PILOT12-CONDITIONAL-LIVE-10`：5060可在原分支完成经审计的百炼HTTPS真实Transport、完整108条严格输入Token上界、真正`max_tokens=256`输出及计费上界、私有USD全工作线预算与D1数据合法外传范围，冻结最终源/manifest SHA并由独立本地Checker验证。**只有全部ABCDE硬门PASS**才允许按照原108槽顺序真正发送第1–3格，三个工程协议检查全部成功后可继续第4–108格；首3格计入108，不另加探测，不得retry或按回答正确率筛样。任何硬门UNKNOWN/BLOCKED或第一个请求/用量/费用/网络/数据错误STOP，留108状态与已承诺费用，不自动补跑。此前Owner已核账号/地域/费率/余额属于OWNER_ATTESTED，仍须在D/E账本数值闭合，USD30总限、25预警、28不启新批保持。
本Owner10授权与旧Runner实现隔离不同：**授权存在但前置门仍未过**，未有真实调用时仍`NOT_RUN`，不能把有条件批准记成真实模型成功。固定`qwen3.7-plus-2026-05-26`、36世界×G0/G1/G2、原108私有计划/System、无额外Judge/搜索/思考/重试/改参数。原`max_tokens`与`max_completion_tokens`不同，若旧字段不足以证明计费封顶须停报Owner而非换字段试跑。来源真实性/许可证或外传范围不清，或C盘写入/答案角色泄漏一律阻断。
FastC`PARTIAL_DIAGNOSTIC_UNRESOLVED`、B2误删、29 hit/7 miss与HumanGold0/target未知继续；针对D1暂定答案只在生成结果完整封存后独立评估，正式ASR/Accuracy/C3不得宣布。5090另分支任务不变。禁止B5/B6、D1-40、D2D3/Reviewer/GT Vault、5090 Claims和跨分支并入。
[Owner十二字段条件授权](../paper1/dual_machine/owner_approvals/W1_5060_PILOT12_CONDITIONAL_LIVE_RUN_AUTHORIZATION_20261105.md)；[5060完整3+105执行合同](../paper1/dual_machine/chinese5060/W1_5060_PILOT12_CONDITIONAL_LIVE_3PLUS105_EXECUTION_PROMPT_V1.md)。执行前状态`CONDITIONAL_APPROVAL_GATES_PENDING`；任何结论需实际真请求封存佐证。仅5060分支提交脱敏证据与治理收口后STOP。后续历史状态不覆盖。

## 当前工作 — 5060 Runner 离线验收完成，真实 Pilot 待独立执行审批（2026-11-05 JST）

W1-5060-RUNNER-20261105-01，RUNNER_IMPLEMENTED_LIVE_NOT_AUTHORIZED。Owner W1-OD-20261105-5060-RUNNER-PREFLIGHT-09，控制提交 e378f04835709a0753ab27f913638642714351bb，源码 1a11fd2ef4802d5029619acb3e65c5ad09a4a57e。
ENGINEERING_VALIDATION。固定36世界/三臂108格、80唯一提示词。正常 Fake 108/108；超时 3成功/1失败/104未运行；缺usage 1成功/1失败/106未运行；live拦截退出2。29 tests、Ruff、MyPy 6源码通过。真实生成 NOT_RUN，实际API 0，新增费用 USD0，HumanGold 0，target未知，targeted ASR / 正式QA NOT_MEASURED。
当前实跑门为 LIVE_NOT_AUTHORIZED、TOKEN_GATE_BLOCKED、WIRE_UNVERIFIED、BUDGET_GATE_BLOCKED。账户和地域等已由Owner核验，OWNER_ATTESTED。下次绑定新执行授权、审核后真实传输、精确chat计数、256输出硬上限及全线预算账本和数据外传范围。物理证据只存D/E。

[工程证据和审批包](../paper1/dual_machine/chinese5060/W1_5060_PILOT_RUNNER_IMPLEMENTATION_AND_ADMISSION_REPORT.md)。以下旧“当前”标题均为当时历史快照。


## 当前 / CURRENT — Owner已批准5060 Pilot12 Runner实现/本地Mock验收，真实百炼调用仍需独立执行审批（2026-11-05 JST）

Owner授权`W1-OD-20261105-5060-RUNNER-PREFLIGHT-09`。仅在5060独立研究分支允许实现108固定世界×臂的生成API Runner、FakeTransport干跑、离线准确Token门（若现成身份明确）、价格/统一USD账本硬停、wire契约校验、输入/输出封存及Owner一次性真实运行审批包。可本地离线QA、Ruff/MyPy与D/E受控证据写入；旧G0/G1/G2消息/模型字面`qwen3.7-plus-2026-05-26`/Prompt/Seal保持不变。
Owner已本人核实百炼模型/地域/费率/可用余额，不要求再次提交账号截图或凭证；其信息等级`OWNER_ATTESTED`，实际数值预算/SDK wire/精确token不能自动判PASS；若缺则可交代码，但真实生成始终BLOCKED。
禁止百炼或其它任何真实API/免费probe/模型调用（包含token-count、余额查询）、新依赖/权重下载、实际单格或108次、Retriever/Guard重跑、数据/样本/参数变化、参考或role泄漏、D1-40/D2D3/Reviewer/GT Vault、B5/B6、5090Claims和跨分支操作。继续USD30总限、25预警、28不启新批、2.5pp约束、C禁新增受控项目数据。
原Pilot设计完成但真实生成`NOT_RUN`，HumanGold0，target/C3未知，正式ASR/QA未测；本轮实际模型/API/费用仍0。实施归档脱敏Git收口后STOP，不能自动实际执行。
[十二字段Owner许可](../paper1/dual_machine/owner_approvals/W1_5060_RAG_PILOT_RUNNER_IMPLEMENTATION_AUTHORIZATION_20261105.md)；[完整从Git读取的Runner实施Prompt](../paper1/dual_machine/chinese5060/W1_5060_PILOT12_RUNNER_AND_ADMISSION_IMPLEMENTATION_PROMPT_V1.md)。下方历史记录不覆盖。

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
禁止真实/免费API探测、生成、B3-B6/D1-40/D2D3/Reviewer/GT/T1/T2/Claim和跨分支合并；本轮Git交付后STOP。[最小设计及待审包](../paper1/dual_machine/chinese5060/W1_5060_MINIMAL_RAG_PILOT_DESIGN_AND_BUDGET.md)。 下方历史不改。


## 当前 / CURRENT — Owner接受D1 Pilot12 AI暂定答案，仅授权最小RAG Pilot设计/预算（2026-11-05 JST）

Owner ID `W1-OD-20261105-5060-PROVISIONAL-PILOTDESIGN-08`：原独立12题/38事实原子/16来源的AI辅助暂定参考已批准用于D1可行性设计，不是HumanGold、target或T1证据；HumanGold仍0，target未知，C3未裁决。私有JSON/MD不进公开Git，文件SHA及交接条件记录在Owner授权；5060本机若缺文件则标AWAITING_PRIVATE_ARTIFACT_TRANSFER，不影响只读/零模型调用的方案设计。
新阶段`DESIGN_ONLY_NOT_RUN`：以原P2冻结36世界（29 candidate hit/7 miss）、旧PAIRO1封存B0/B1/B2上下文，设计最小三臂生成与独立后封存评分，候选108次请求只是待审方案，并且token、价格、成本上限及硬停需另作实际账户核算。任何Qwen/其他模型/API调用（包括免费探测）、检索/Guard重跑、参数/样本/答案改动、D1-40/D2D3/Reviewer/GT/B5B6/5090Claim和正式ASR都未授权。
Fast C`PARTIAL_DIAGNOSTIC_UNRESOLVED`及Fast B Clean误删上升保留，原2.5pp质量约束和累计USD30上限仍生效；n=12时单例8.33pp不能证实符合2.5pp保护门。完成脱敏设计与预算、PO-MHEP文档/Git收口后STOP。
[Owner十二字段授权](../paper1/dual_machine/owner_approvals/W1_D1_PROVISIONAL_REFERENCE_AND_RAG_PILOT_DESIGN_OWNER_AUTHORIZATION_20261105.md)；[简化完整执行Prompt](../paper1/dual_machine/chinese5060/W1_5060_PILOT12_MINIMAL_RAG_DESIGN_EXECUTION_PROMPT_V1.md)。此前Fast-C与交接计划均历史不可修改。

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
禁止B5/B6、付费/下载、D1-40/D2D3/Reviewer/GT/T1/T2/Claim和跨分支操作；本次Git收口后STOP。[Fast C证据与局限](../paper1/dual_machine/chinese5060/W1_5060_FAST_C_READONLY_FAILURE_ATTRIBUTION_REPORT.md)。 下方均历史。


## 当前 / CURRENT — Fast-Track C已获批、等待5060只读归因执行（2026-11-05 JST）

Owner授权`W1-OD-20261105-FAST-C-06`：仅对已封存P2/PAIR01作只读失败归因及已有12题独立盲审交接整理。可验证原seal后用无副作用统计复算配对翻转、Stage1/Stage2旧trace和频率同分、Clean/HN误删及Poison漏报；Role-Free Analyst只读旧输出不看标签，Post-Seal Evaluator才可读获准D1开发标签，盲审交接不得读预测和角色。禁止所有科学试次重跑、改模型/参数/阈值/索引/样本、下载/商业API、B3/B4/B5/B6、D1-40、D2/D3/Reviewer/GT、T1/T2、5090 Claim、主线/跨分支合并。
仍保留原P2 hit29/36、MISS7及B1/B2各36/36、Poison TP1→2、Clean FP1→4、HN FP2→2；这些是已完成D1开发历史结果，本轮尚无新归因结论，不可编造统计显著或正式ASR/Accuracy。独立Gold仍0，target UNKNOWN。受限执行Prompt直接入Git，需先读取它、原Owner授权与AGENTS/PO-MHEP；如原raw/profile缺失，局部STOP并报告UNRESOLVED，不得重跑。
[Owner十二字段授权](../paper1/dual_machine/owner_approvals/W1_FAST_TRACK_C_OWNER_AUTHORIZATION_20261105.md)；[5060完整执行Prompt](../paper1/dual_machine/chinese5060/W1_5060_FAST_TRACK_C_READONLY_EXECUTION_PROMPT_V1.md)。本阶段授权已登记，实际执行/结果/归档/Git交付尚待5060独立完成；完成后STOP。历史状态不覆盖。

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
禁止B3-B6、D1-40、D2D3/Reviewer/GT Vault、T1/T2/Claim和跨分支合并。[实际结果与证据](../paper1/dual_machine/chinese5060/W1_5060_FAST_B_PAIR01_RESULT.md)。 下方旧状态保留为历史。


## 当前 / CURRENT — Fast B人工资产核验通过，离线配对准备（2026-11-05 JST）

Owner补齐固定HF权重并确认直连/无失败重试；全部10必要文件size和Git/LFS身份通过，B2既有固定10文件复制D且hash一致。
W1-5060-FAST-B-20261105-PAIR01；原36TopK字节核验、role-free packets通过；7项输入/索引/封存回归及Ruff/MyPy3源码通过。
下一步仅原库B1/B2离线过滤，模型/算法输出尚未运行，不提前填指标。T0/D1开发，原29命中/7miss不变。
[事前冻结](../paper1/dual_machine/chinese5060/fast_b/B12_EXECUTION_FREEZE.md)；旧连接失败与checkpoint保留，人工资产接续不伪造机器下载日志。
商业API/B3-B6/D1-40/D2D3/Reviewer/GT/T1/T2/Claim仍禁止，原盲审包复用；完成当前配对与Git交付后STOP。


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
[实际失败和下一门](../paper1/dual_machine/chinese5060/W1_5060_FAST_B_RECOVERY01_RESULT.md)。 下方是不可变历史状态；新运行及新失败不追溯改写旧结果。


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
[Fast B审计和受阻交付](../paper1/dual_machine/chinese5060/W1_5060_FAST_B_B1_B2_OFFLINE_RESULT.md)。 下方旧状态均保留为历史，不追溯改写原BLOCKED或授权事实。


## 当前 / CURRENT — 5060 Fast-Track B有条件批准；5090主要公开基线复现路线准备（2026-11-05 JST）

授权 W1-OD-20261105-FAST-B-04 与补充 W1-OD-20261105-RESOURCE-REPRO-05。5060原分支保持；已允许从Hugging Face官方获取固定revision all-MiniLM-L6-v2最小白名单，累计网络下载上限250MiB；D/E项目可控存储放宽原1GiB新增上限、须预冻结单项峰值与安全空间，C盘不新增项目可控内容。身份/参数全部闭合后仅允许复用既有36个P2冻结TopK5进行零API B1公共v0.2库及B2仅换中文embedding开发过滤；并行准备盲于检索结果的12张独立人工裁决材料，不能自造Human Gold。**审批并非执行事实**，新B1/B2实测仍NOT_MEASURED，需等待后续run/manifest。
5090原分支保持；Owner新增授权其做无需任何模型/数据/依赖下载、无商业API的RAGDefender主要图表-Artifact Claim映射与资源许可/脚本静态预检。明确研究目标为优先完整复现3个开源Claim，辅以可行的检索器/消融/性能表；但当前Claim1–3仍NOT_RUN，不许可加载模型下载BEIR或执行正式命令。5090上次smoke测试工具失败保留。
P2既有36/36、hit29/36、7 miss、B0零删除等证据不可重写，D1开发集属性不变；T1/T2、B3/B4、B5/B6、D1-40、D2/D3、正式GT、额外API和主线/跨分支merge均禁止。本阶段推进必须遵守AGENTS.md/PO-MHEP、文件/输入/模型/TopK/参数/结果hash和各自分支文档Closeout。
[Fast-Track B授权](../paper1/dual_machine/owner_approvals/W1_FAST_TRACK_B_OWNER_AUTHORIZATION_20261105.md)；[存储与复现路线补充](../paper1/dual_machine/owner_approvals/W1_STORAGE_AND_REPRO_RESEARCH_DIRECTION_20261105.md)。

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
[P2报告](../paper1/dual_machine/chinese5060/W1_5060_P2_T0_RETRIEVAL_DIAGNOSTIC.md)。下方历史保留，不把本次工程观察升级为论文或独立泛化结论。


## 当前 / CURRENT — Fast-Track A已批准，T0离线执行准备（2026-11-04）

W1-OD-20261104-FAST-A-03；授权提交af68d89a870647be138cf5592ccd4a058e44a8ab。
固定Pilot12/36独立世界：允许零API、零下载本地Embedding+Chroma TopK5、B0及符合全部缓存身份条件的B1/B2。
B1默认embedding精确revision未闭合而BLOCKED，B2连带BLOCKED；不影响合格T0/B0。检索实际输出尚未形成，不提前填结果。
只读固定D1/world白名单；Retriever不读答案/标签/角色，Evaluator仅在全输出封存后读批准D1开发标签。
12张裁决卡独立材料支路，无Gold自批/目标推断；T1/T2、付费、B3/B4、B5/B6、D1-40、Claim仍禁止。
完成真实计数、私有日志/归档、文档及本分支Git交付后停止。
[授权](../paper1/dual_machine/owner_approvals/W1_FAST_TRACK_A_OWNER_AUTHORIZATION_20261104.md)。下方为历史状态，P1旧“未批准T0运行”仅在本次有限范围被覆盖。


> P1最终只读补充：5090已前进0155470，上游不变、Claim仍未批；分支局部PODR-154重名使用Owner W1-OD跨机关联。[证据](../paper1/dual_machine/chinese5060/p1/evidence/LATEST_5090_HANDOFF_SUPPLEMENT.json)。P1 source/run/准备状态不变。


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
[P1治理与准入报告](../paper1/dual_machine/chinese5060/W1_5060_OWNER_GOVERNANCE_AND_P1_GATE.md)。下方历史记录保留，不产生付费、模型下载或方法接受授权。


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
[P0报告](../paper1/dual_machine/chinese5060/W1_5060_P0_INITIAL_STATUS.md)。下方为历史状态，本条只更新本工作线执行状态，不接受新方法或替换正式研究基线。


## 当前 / CURRENT — 第七条范围收口，12题AI数据草案准备完成（2026-11-04）

PAPER1-RAG-DEFENSE-RECONSTRUCTION-01；AI_DATA_PREPARATION_COMPLETE_PROVISIONAL / SCENARIO_CONTRACT_NEXT；PODR-160。Owner明确限定第七条核心职责；修订题的两份独立审阅和来源仲裁确认3字段等价，9处引用定位通过。第二版12题均有据AI草案，职责范围待决0；问题/评价侧答案隔离，原题/原分歧/全部原审阅保留。人工金标准仍0，非正式实验结果。
无需Owner从零补数据。下一步由执行端准备受控检索后C0–C3场景、共同证据预算与评分合同，并闭合B2迁移可比性和费用门；本任务新阿里云API0/费用0，未自动付费，B4/正式实验未启动。
[第二版结果与准备边界](../research/stage6_1_hidden_knowledge_poisoning/core144/rag_defense_reconstruction_01/AI_DATA_PREPARATION_SCOPE_CLOSURE_V2.md)。下方为历史状态，不能据旧“范围待定”重复请求Owner确认。

## 当前 / CURRENT — AI数据草案已准备，Owner集中确认1项范围（2026-11-04）

PAPER1-RAG-DEFENSE-RECONSTRUCTION-01；AI_DATA_PREPARATION_REVIEW_READY / QUESTION_SCOPE_DECISION_REQUIRED；PODR-159。12题/18源/38字段的两份隔离agent审阅及来源仲裁已完成，原始输出保留。原双审100处引用、仲裁58处引用定位通过；一题单独补源双审2字段/4处引用通过，未更改运行时Top5。最终11题有据AI草案、1题职责列举范围待定，另2项题干文字澄清建议；人工批准/金标准均0。
这些是AI_REVIEWED_DEVELOPMENT_DRAFT_NOT_HUMAN_GOLD，不是防御效果或第三份独立盲审。新增阿里云API0/费用0，B4/正式实验未启动，D2D3/Human/GT/历史不改。下一步只需Owner明确职责题范围（建议第七条），执行端继续承担查证、数据整理与场景准备；逐世界公平预算、迁移可比性及费用门仍保留。
[结果、Owner精简事项和十二字段决定](../research/stage6_1_hidden_knowledge_poisoning/core144/rag_defense_reconstruction_01/AI_DATA_PREPARATION_OWNER_REPORT.md)。下方均为按时序保留的历史。

## 当前 / CURRENT — AI辅助数据准备进行中，非付费实验

2026-11-04 JST；PAPER1-RAG-DEFENSE-RECONSTRUCTION-01；AI_SOURCE_REVIEW_IN_PROGRESS。Owner请求LOCAL/其他agent帮助准备实验数据（PODR-159）。新建ai_adjudication_01，12题/18份既有官方来源/38个待核事实字段，两个fork_turns=none的agent分别审阅；不提供候选/组/S/角色、旧预测或对方输出。协议已先于审阅保存。
预期产物仅AI_REVIEWED_DEVELOPMENT_DRAFT_NOT_HUMAN_GOLD；引用定位与语义支持分开核查，缺证/分歧保留，不自动变为Human GT。付费Pilot/B4/正式实验NOT_STARTED；本任务阿里云新增调用0。下一步锁定两份输出后做来源复核与Owner争议清单。下方为历史状态。
[AI准备协议](../research/stage6_1_hidden_knowledge_poisoning/core144/rag_defense_reconstruction_01/AI_DATA_PREPARATION_PROTOCOL_V1.md)。

## 当前补充 — 原始来源找到问答线索，独立裁决仍待完成（2026-11-04）

PAPER1-RAG-DEFENSE-RECONSTRUCTION-01；PHASE1_2_REVIEW_READY / HUMAN_DECISION_REQUIRED。只读核查确认28份选定证据有相同上游正文，2份官方来源定位出17条问答片段线索；旧120条检索query均含完整候选，不能直接作独立QA。建议先审阅已有官方问答的题干/时间/范围/答案边界和冻结组对应，再补不足；12组仍NEEDS_ADJUDICATION。Owner明确继续后另生成12条来源审阅问题草稿、23次来源引用，答案全部null、未批准，控制映射另存评价器；尚无可执行Pilot。未重做验证，新增API0/费用0，B4/正式实验未开始，D2D3/Human/GT不改。
[新增证据、限制和下一门](../research/stage6_1_hidden_knowledge_poisoning/core144/rag_defense_reconstruction_01/SOURCE_REUSE_FOLLOWUP.md)。下方为先前审阅记录。

## 当前 / CURRENT — 方法重构审阅包就绪，查询数据与迁移门待决定

2026-11-04 JST；`PAPER1-RAG-DEFENSE-RECONSTRUCTION-01`；`PHASE1_2_REVIEW_READY / HUMAN_DECISION_REQUIRED`。Owner已明确续接，原暂停快照按日期保留。
固定RAGDefender v0.2在缓存非论文多语种embedding下CPU核心API成功；作者默认示例/官方测试未全过，不是论文复现或迁移就绪。冻结12组36候选均缺独立查询/答案裁决，B0仅上下文直通，查询Pilot未执行。
E1新检索弱点UNKNOWN，NO_CONFIRMED_IMPROVEMENT_GAP，B4未实现。新API0/费用0，累计已知旧usage估算7.611826CNY，账单未对账；15美元累计预算，10预警/14硬停/1缓冲，不自动付费。
复用暂停前19项测试/Ruff/MyPy记录，源码哈希一致；本地检查独立原日志缺口已披露。下一门：Owner决定独立查询裁决与迁移路线；正式实验NOT_STARTED，D2D3/Human/GT/历史不改。
[负责人报告与十二字段决定](../research/stage6_1_hidden_knowledge_poisoning/core144/rag_defense_reconstruction_01/OWNER_FEASIBILITY_DECISION_REPORT.md)。下方状态均为带日期的历史记录。

## 当前 / CURRENT — Owner暂停方法重构任务，等待新会话续接

2026-11-04；`PAPER1-RAG-DEFENSE-RECONSTRUCTION-01`；`OWNER_PAUSED_IN_PROGRESS_NOT_COMPLETE`。独立分支`research/paper1-rag-defense-reconstruction-01`，基线b235381，本任务WIP未提交未推送。
已完成上游固定/静态审查、非论文embedding的CPU核心API执行及D1包数据门审计；本轮API0，B4未实现。查询/独立答案裁决缺失，付费Pilot不得启动。用户明确暂停，Auto Continue=NO。
续接入口：[暂停续接记录](../research/stage6_1_hidden_knowledge_poisoning/core144/rag_defense_reconstruction_01/RESEARCH_CONTEXT_RECOVERY.md)。历史结果、D2D3、Human/GT及旧工作树保持；下方状态为历史。

## 当前 / CURRENT — 完整D1可行性矩阵已评分并封存，CONDITIONAL

2026-11-03；PAPER1-FEASIBILITY-SPRINT-01；RunD1-DEV-BEIJING-CONT-A01；执行44594c8。状态FEASIBILITY_D1_DEV_COMPLETE/OWNER_REVIEW_REQUIRED，事前结论CONDITIONAL。
120候选×4条件=480预测封存后独立评分；E1/E2 TP37/40，S1=12/12/S2=14/15/S3=11/13，CleanFP0/HNFP1，弃权13/120，Strict30/40。
E3/E4 TP0/40、弃权120/120、Strict0/40；结构化118条span/slot绑定失败、2条模型未决；内部120条无有效证书。E2逐ID等于E1、E3等于E4，新增机制无独立收益。
独立主计数/费用核验通过，13家族2000次配对区间保留。结构化原判决有38个Poison为CONTRADICT但全被合同拦住，仅RAW_VERDICT_DIAGNOSTIC，不是修复分数，不改parser或预测。
361物理请求含探测1，D1独立call_id360；原159请求保留、新增202。原价usage估算7.611826CNY，USD保守界约1.268638，低于Owner15预算；无不明请求预留，正式账单未对账。
原Attempt01失败、52逐字节前缀、第53条2次复用及1个物理截断保留；无重试/扩输出/改prompt/换模。预测SHA920f18fd75fa089d3f7dd2d38c54640ed861ea6a55ad7b40a7e532413c7a28e4，锁SHA41ee0bd0ee1e097f1d10ccb7576f853a90d60939fb123f4ecc1fe7bd33526000。
私有归档SHA39fde95915f9eb4c1f7c66eb4275f12d29f7f1528b5e7f589c8a88c015ba5d43，1667文件索引SHA2f13585b98cab5343e451470fb606a84449d17d8f4c867c7eeac04deb1d605f9；原始正文/响应/逐条预测/Key不入Git。
下一门为Owner最终审阅。建议收口本轮、保留强API基线与失败机制，当前E3不可当成功方法；不自动放宽合同、追加提示/调用或耗尽预算。D1_DEV_EXPOSED，正式实验NOT_STARTED；D2D3/Human/GT/旧L0/5090均不变。
[负责人报告](../research/stage6_1_hidden_knowledge_poisoning/core144/feasibility_sprint_01/FEASIBILITY_OWNER_REPORT.md)。下方准备/待决/未评分条目为按日期保留的历史。

## 当前 / CURRENT — Owner批准A与阿里云15美元预算，恢复尚未执行

2026-11-03；PAPER1-FEASIBILITY-SPRINT-01；PODR-157。Owner明确批准方案A，并将阿里云API任务总预算提高到USD15。
新RunD1-DEV-BEIJING-CONT-A01：原52包逐字节复用，第53条已付费internal/direct响应复用；length逐条INSUFFICIENT，不重试，不改prompt/模型/输出上限/判据。原Attempt01失败、HARD_STOP及归档不变。
已有费用3.264570CNY累计；新预警USD14/硬停14.50，按原6CNY/USD保守界为84/87CNY，保留0.50USD缓冲，不扩展服务商或实验矩阵。
当前CONT_A_APPROVED_IMPLEMENTED_PREFLIGHT_NOT_YET_EXECUTED；实际总请求仍159，完整新预测锁未形成，标签未打开。
下一步：测试、身份预检、冻结提交/推送后，在原七天窗口内补剩余调用；全120四条件封存后独立评价，不再重复申请已批准普通阶段。新工程异常仍停止。
科学方法PROPOSED/EXPERIMENTAL、D1_DEV_EXPOSED、正式实验NOT_STARTED；5090、D2D3、Human/GT、旧L0保持。
[冻结补充合同](../research/stage6_1_hidden_knowledge_poisoning/core144/feasibility_sprint_01/CONTINUATION_A_PROTOCOL_V3.md)。下方Owner待决为已被本次批准覆盖的历史。

## Current — D1 prefix archived; output-length hard stop requires Owner decision

2026-11-03；PAPER1-FEASIBILITY-SPRINT-01；RunD1-DEV-BEIJING01；执行dbc4cc1。北京接口虚构探测通过；许可/Key/端点已闭合。
真实D1完成52/120候选包、208条件预测，第53个候选direct返回length/1024；GENERATION_NOT_COMPLETE_NO_RETRY按冻结实现整轮退出1。没有自动重试、提高上限或修改模型/prompt/parser/路由。
159请求含探测1，usage原价估算3.264570CNY，保守USD界约0.544095，无待结算预留。52前缀不评分、无完整预测锁，真实标签未打开；科学NOT_EVALUATED、正式实验NOT_STARTED。
状态HARD_STOP_OUTPUT_LENGTH_OWNER_REVIEW_REQUIRED。下一门：Owner决定是否仅将length记为逐条INSUFFICIENT、不重试、复用52包及第53条已有调用，在原窗口/费用账本内完成其余调用；当前仅PROPOSED，未改源码或启动Continuation。
原Attempt01/HARD_STOP/709文件索引及私有归档保留，归档SHA34680b4cdb7e4c90a46942f2cea7b1bebec23f73a680342270a43ee0d579481b；索引SHA9055fca39ddc455e1df7f6e6d5ff989bcc8e94e0068055c1f2c0f50f3d096ffa。原始正文/响应/工作区/Key不进Git。5090、D2D3、L0、Human/GT不改。
[报告与下一门](../research/stage6_1_hidden_knowledge_poisoning/core144/feasibility_sprint_01/BEIJING_ATTEMPT01_OWNER_REPORT.md)。下方ready/未调用为此前历史。

## Current — Beijing paid gates supplied; live probe not yet executed

2026-11-03；PAPER1-FEASIBILITY-SPRINT-01；基线69899e2。Owner提供北京工作区Host、完成用户环境Key配置，并明确确认许可及保密要求允许D1/Top5由阿里云处理。原Global授权有效，不重复询问。
当前BEIJING_LIVE_PROBE_READY_NOT_EXECUTED；实际API0、费用0、真实D1预测0；不宣称开通或模型实测成功。
仅适配cn-beijing的ws/llm官方工作区格式和CNY原币计费，科学机制/模型/prompt/parser/路由/数据/指标不改。CNY24预警/27硬停，按6CNY/USD保守预算界，不是即期汇率或扩预算。
先锁定/推送后单次虚构探测；成功才同一120条E1-E4，封存后评价。HTTP/非Thinking/版本/usage/预算异常停止，不换模型、不重试。5090和D2D3/历史仍禁止。
[补充合同](../research/stage6_1_hidden_knowledge_poisoning/core144/feasibility_sprint_01/BEIJING_EXECUTION_ADDENDUM_V2.md)。以下保留先前条件未闭合的历史。

## Current — 2026-11-03 bounded feasibility sprint; local engineering, paid gate blocked

Task `PAPER1-FEASIBILITY-SPRINT-01`; branch `research/paper1-feasibility-sprint-01`, isolated from L0 report at512d928; research remote at recovery4dc9161. Dynamic HEAD/upstream must be read from Git.
Status `LOCAL_ENGINEERING_COMPLETE / PAID_EXPERIMENT_BLOCKED`; method `PROPOSED / EXPERIMENTAL`, formal experiment NOT_STARTED.
Owner authorizes one-week local/API feasibility underUSD5, warning4.00/hard4.50; no5090. Global data transfer approved in this chat, not pending repeat approval.
Allowed: code, fictional tests, read-only input audit, strict API gates, separate post-seal evaluator, documentation and Git.
Missing: actual account region/workspace endpoint, license/confidentiality confirmation, environment Key, then live synthetic nonthinking probe. Real D1 requests0/costUSD0.00; E1-E4NOT_RUN, metricsnull.
[Protocol and report](../research/stage6_1_hidden_knowledge_poisoning/core144/feasibility_sprint_01/README.md); [decision gap](../research/stage6_1_hidden_knowledge_poisoning/core144/feasibility_sprint_01/PAID_EXECUTION_DECISION_V1.md).
F5 original120xTop5 bytes verified; runtime no labels/Oracle; old L0/ALIGN01/R05/R06 untouched. D1 remainsD1_DEV_EXPOSED,24HOLD excluded.
Next: Owner supplies remaining account/licensing facts and safely configuresKey; within original window and budget, probe then fixed run may proceed. No new paid provider/model, L0 prompt version,5090, D2D3/GT/Human/official snapshot changes.
Current execution recommendation NO-GO_FOR_PAID_EXECUTION; scientific NOT_EVALUATED, not an empirical method failure. Older entries below are dated history.

## Current — 2026-10-31 D1/L0 baseline owner report prepared; closure recommended, acceptance pending

Task `P1-L0-D1-BASELINE-EVIDENCE-AND-OWNER-REPORT-01`; Owner request is report/evidence preparation, not new inference or scientific acceptance.
[Owner report](../research/stage6_1_hidden_knowledge_poisoning/core144/l0_closeout_20261031/PAPER1_L0_D1_BASELINE_OWNER_REPORT_V1.md).
Evidence cutoff `4dc9161e79b79ece70a7c17144175a19b985770d`; FULL01 240 and ALIGN01 120 new predictions remain sealed.
Oracle alignment net TP+1, legitimate FP+5, strict triplets8/40 unchanged; `TRADEOFF_FPR_INCREASED` preserved.
Status `OWNER_REPORT_READY / OWNER_REVIEW_REQUIRED`; recommendation is end this D1/L0 development/prompt round, not all external S6.1-R0 baselines.
Control plane verifies pinned redacted Git sources and aggregate arithmetic; private raw/hash replay and family-bootstrap reproduction not performed here.
FULL01 peak29.1035GiB leaves0.8965GiB under its30GiB hard cap; precheck memory values do not replace this real-run value.
Next gate is Owner review of scope closure and evidence availability. No prompt rerun, F5 repeat, GPU precheck, VACE-LM, D2/D3, formal GT/split or model change is authorized.
All dated sections below are historical snapshots; the current section supersedes older next-action text only within this reporting scope.

## Current — 2026-10-30 Oracle claim-alignment comparison is complete

Task P1-L0-ORACLE-CLAIM-ALIGNMENT-COMPARISON-01. Run VACE-L0-D1-20261030-ORACLE-ALIGN01. Status ORACLE_CLAIM_ALIGNMENT_DEV_COMPLETE / OWNER_REVIEW_REQUIRED. Execution commit 4f4ece34e434d21b9c2dc076d53efe1587470594.
[Result](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_ORACLE_CLAIM_ALIGNMENT_RESULT_V1.md).
Judgment TRADEOFF_FPR_INCREASED. Overall TP moved from 14/40 to 15/40, while Clean FP moved from 4/40 to 6/40 and HN FP from 2/40 to 5/40. The pre-registered “detection up without extra false positives” rule is not supported. Recall’s paired interval crosses zero. Poison SUPPORT fell from 19 to 15, and model-own INSUFFICIENT rose from 0 to 3. More abstention is not a verification gain. 120 calls, no truncation, peak reserved 21657288704. Prediction lock SHA256 09b0ea5d237158e5472b12cffe5ed3d8807c99bdbce809e9c216896f3d57fda5. FULL01 and the offline audit originals were rechecked and left unchanged. No second prompt, F5 rerun, VACE-LM, D2/D3, or new model.

## Current — 2026-10-30 Oracle claim-alignment comparison is authorized

Task P1-L0-ORACLE-CLAIM-ALIGNMENT-COMPARISON-01. Run VACE-L0-D1-20261030-ORACLE-ALIGN01. No new PODR id. This approval authorizes 120 new Oracle calls and replaces the earlier “no next inference” limit only for that comparison.
[Protocol](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_ORACLE_CLAIM_ALIGNMENT_V1.md).
The only change is one fixed system suffix. FULL01 Oracle stays the sealed control. Metrics are NOT_MEASURED until the 120 predictions are sealed. This is a development prompt comparison, not a formal test. No F5 rerun, VACE-LM, D2/D3, or another prompt round.

## Current — 2026-10-30 sealed FULL01 output audit is complete

Task P1-L0-FULL01-SEALED-OUTPUT-AUDIT-01. No new PODR id. The sealed run remains VACE-L0-D1-20261030-FULL01. Result commit bfc9685e5cdde1757643bd6825e52e34bbc85f52. Execution commit 830bb5b3eb950f30494c9e3ef6affdcc8efc7dcb.
[Offline audit](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_FULL01_OFFLINE_AUDIT_V1.md).
Status FULL01_OFFLINE_OUTPUT_AUDIT_COMPLETE / OWNER_REVIEW_REQUIRED. File identity and the sealed verdict counts match. Output failures are mostly quotes absent from the cited text, plus eight absent UIDs and six JSON syntax failures. One poison CONTRADICT on F5 was blocked by validation; Oracle blocked none. Validation-passed poison SUPPORT remains 22 on F5 and 19 on Oracle. Raw verdicts are diagnostic only. No FULL01 rerun, VACE-LM, D2/D3, or next inference run.

## Current — 2026-10-30 full D1 development run is sealed

Task P1-L0-D1-FULL-EXECUTION-01. Run VACE-L0-D1-20261030-FULL01. No new PODR id. Execution commit 830bb5b3eb950f30494c9e3ef6affdcc8efc7dcb. Adapter SHA256 remains 0cb1d1854ba90d94efa859e03a54f18b25999c4bcaf4c84ac9e43073128eb2d4.
[Execution record](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_FULL01_D1_EXECUTION_V1.md).
Status L0_D1_DEV_FULL_COMPLETE / OWNER_REVIEW_REQUIRED. 240 new predictions, prediction lock, independent scores, and the private archive exist. R05 stays blocked and R06 stays passed. Synthetic semantics stayed diagnostic at 4/5. F5 overall recall is 5/40 and Oracle overall recall is 14/40. Peak reserved is 31249661952 bytes, under the 30 GiB cap. Input rejection count is 0. This is a development result, not a formal test. No VACE-LM, D2/D3, or next run.

## Current — 2026-10-30 full D1 development execution is authorized

Task P1-L0-D1-FULL-EXECUTION-01. Run VACE-L0-D1-20261030-FULL01. No new PODR id. Baseline fdf77cff25158c731a3fdb2dde70a5ad27b0c77d. Adapter SHA256 0cb1d1854ba90d94efa859e03a54f18b25999c4bcaf4c84ac9e43073128eb2d4.
[Execution record](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_FULL01_D1_EXECUTION_V1.md).
R05 stays blocked and R06 stays passed. The run uses the original 31744 input cap, not the R03 7200 cap, and does not carry the capacity-only min_new_tokens=1024 setting. Metrics are NOT_MEASURED until the private archive is sealed. This is a development result, not a formal test.

## Current — 2026-10-30 R06 separates CUDA cache warmup from continued accumulation

Task P1-L0-R06-ALLOCATOR-STABILITY-REVIEW-01. No new PODR or Owner decision id.
[R06 disclosure](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_R06_ALLOCATOR_STABILITY_V1.md).
R05 stays R05_PRECHECK_BLOCKED. Its 512 MiB alternate failure and FAILURE.json were not rewritten. The committed adapter from b5ff81d5dd58493fc20d796ac9806f4678fb0928 was reused. Protocol SHA256 55c9d4aacc7f7571c11f31b32c64d911a3c2bc22c8cdca86a5d4fa8ff95b1db7 was locked before the GPU run.
Synthetic lengths 1294, 8192, 16384, 26493, 1294. Two warmup rounds and five measurement rounds, 1024 new tokens each, no empty_cache. Checkpoint allocated stayed at 15268457984, so every measurement delta against the warmup-2 baseline is 0. Reserved reached 22194159616 on the first long input and then stayed there; the last three measurement checkpoints have span 0. Longest peak reserved is 22194159616, minimum contract headroom 10018095104. No OOM. Status R06_STABILITY_PRECHECK_PASS / OWNER_REVIEW_REQUIRED.
That is a basis to request a small end-to-end trial. It does not authorize the trial, 240 predictions, D1 scoring, R07, VACE-LM, or D2/D3. It is not a proof of no leak or unbounded stability.

## Current — 2026-10-29 R05 explicit GQA efficient SDPA precheck is blocked

Task P1-L0-R05-EXPLICIT-GQA-EFFICIENT-SDPA-PRECHECK-01. No new PODR or Owner decision id. Base commit 71b0b111591b9c2a621a78995c72bad0ed860bbd.
[R05 disclosure](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_R05_EXPLICIT_GQA_PRECHECK_V1.md).
Explicit contiguous KV repeat passed the pre-registered numeric window. The model ran `PyTorchMemEffAttention` on both prefill and decode, the persistent cache stayed at 4 heads, and a repeated fictional generation matched token for token. A 26493-token synthetic input plus 1024 new tokens reserved 21281898496 bytes, with 10930356224 bytes of headroom under 30 GiB. All 240 pack lengths are inside 1294–26493. That is an envelope, not 240 predictions.
The round stops at R05_PRECHECK_BLOCKED. After a long step the CUDA reserved pool rose by 1928 MiB and stayed there on the next short step, above the pre-registered 512 MiB accumulation threshold. The threshold was not loosened and the probe was not rerun. No D1 scoring, R06, VACE-LM, or D2/D3.
The section below still says the R03 run had started and metrics were NOT_MEASURED. That text is historical. Local R03 later wrote COMPLETE.json; this note does not reopen it or fill its scores. R04 remains local only.

## Current — 2026-10-29 R03 tightens max_input_tokens to 7200 and starts a new run

Run VACE-L0-D1-20261029-R03. No new PODR id was on origin at b22a118. The only protocol change is max_input_tokens 31744 → 7200 under bf16+SDPA. No quantization, CPU offload, allocator change, or silent truncation. Over-long rows are INSUFFICIENT / INPUT_TOO_LONG_NO_SILENT_TRUNCATION and stay in the denominator.
[Length-cap disclosure](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_R03_LENGTH_CAP_DISCLOSURE_V1.md).
Cold probes: 7200 tokens reserved 30935089152 (1.19 GiB under the 30 GiB cap, including 256 new tokens). 7400 reserved 31784435712 and was rejected. The R02 OOM row was 10820 tokens and the failed 12.21 GiB allocation. R01 and R02 HARD_STOP files stay in place. D1 metrics remain NOT_MEASURED until this run seals. Diagnostic semantic gate continues from PODR-153; 4/5 is not relabelled as a pass.

## Current — 2026-10-29 R02 engineering check passed, D1 inference stopped on CUDA OOM

P1-VACE-L0-R02-SEMANTIC-DIAGNOSTIC-EXECUTION-01; Run VACE-L0-D1-20261029-R02; source a31ade51c2e6923991b81895163060b80db6da4f; PODR-153/OR-109/REL-2026-0124.
[OOM blocker](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_R02_CUDA_OOM_BLOCKER_V1.md),
[state V30](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V30.md).
Check-only passed on the frozen R01 interpreter, model and input. No download or install. Synthetic engineering_all_pass true; semantic 4/5 and all_pass false are diagnostic only; execution_gate_passed true. Greedy repeat matched.
Five new L0-F5 raw files were written. The next generate raised torch.OutOfMemoryError: allocate 12.21 GiB with 2.01 GiB free, 27.73 GiB already allocated, 30.00 GiB allowed. Oracle not started. No prediction lock, COMPLETE.json or return ZIP. Metrics NOT_MEASURED, not 0.
R01 HARD_STOP unchanged. R02 HARD_STOP retained. No allocator change, quantization, CPU offload, prompt edit or retry. D2/D3 unchanged.
Status L0_STRONG_BASELINE_R02_CUDA_OOM_BLOCKED / HUMAN_DECISION_REQUIRED.

## Current — 2026-10-29 Owner approves independent L0 R02; semantic synthetic accuracy diagnostic, engineering gates retained

P1-VACE-L0-R02-SEMANTIC-DIAGNOSTIC-EXECUTION-01; PODR-153/OR-108/REL-2026-0123; baseb8c6118.
[R02 approval/execution](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_R02_OWNER_APPROVAL_AND_EXECUTION_V1.md),
[parallel stateV29](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V29.md).
Owner explicitly permits R02 with unchanged model/prompt/parser/evidence/parameters; only synthetic semantic accuracy stops being a hard execution gate.
R01 remains failed and immutable, including HARD_STOP and all raw/logs. New R02 directory cannot equal/nest/contain R01; read-only existing model/env/input reuse, no download/install.
Engineering device/CUDA/hash/budget/format/citation/determinism gates remain hard. Raw model verdict and same synthetic expectations unchanged, no repair using reason.
Run VACE-L0-D1-20261029-R02; all240 new predictions lock before separate evaluator reads labels/S. Signed40/120/13families and8/24HOLD unchanged.
The 5090 execution observed after this approval is the CUDA OOM hard stop in the section above, not an unobserved package and not a D1 score.
Next5090 Cursor pulls the exact NEW R02 commit, check-only then run to scoring/private archive; do not resume/delete R01 stop, retune, or claim formal GT/test.
D2/D3 data conversation and gates unchanged; no data/Guide/Human/GT modifications, training, formal split, calibration or VACE-LM.

## Current — 2026-10-29 5090 L0 stopped at the fictional synthetic semantic gate

P1-VACE-L0-F5-ORACLE-STRONG-BASELINE-01; Run VACE-L0-D1-20261029-R01; PODR-151/OR-107/REL-2026-0122.
Execution source remains a83437ab0a685d69114093fd4bd0e6ab22f354aa. Documentation tip before this record was 9831d62; the run did not move onto it.
[Synthetic-gate blocker](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_5090_SYNTHETIC_GATE_BLOCKER_V1.md),
[state V28](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V28.md).
RTX5090 32607 MiB, driver 610.88, CUDA kernel pass, Torch 2.8.0+cu128, Transformers 4.57.1. Official Qwen2.5-7B-Instruct revision a09a35458c702b33eeacc393d103063234e8bc28 weight SHA256 matched the pinned manifest. BF16/SDPA/GPU0 only.
Synthetic gate all_pass false: SYN-3 expected SUPPORT, parsed CONTRADICT, error null. SYN-1/2/4/5 matched; SYN-1 greedy repeat matched. D1_not_loaded_yet. raw count 0. No COMPLETE.json or return ZIP.
L0-F5 and L0-Oracle NOT_EXECUTED. Recall/FPR/Precision/triplets/intervals NOT_MEASURED, not 0. HARD_STOP.json exists; same work directory must not autoretry.
No prompt/parser/model/data change, no D2D3/VACE-LM/training/formal GT/split. Private ZIP, weights, labels and raw stay off Git.
Status L0_STRONG_BASELINE_SYNTHETIC_GATE_BLOCKED / HUMAN_DECISION_REQUIRED.

## Current — 2026-10-29 parallel conversation roles: experiments here, D2/D3 data in a new local Codex chat

P1-CORE144-D2-D3-DATA-THREAD-HANDOFF-01; PODR-152/OR-106/REL-2026-0121; basea83437a.
Owner will open the local project data/annotation conversation; the original conversation retains experiments. No thread/worktree created here.
[Data handoff](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_D3_DATA_THREAD_HANDOFF_V1.md),
[parallel stateV27](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V27.md).
D2 still PENDING_TARGETED_TWO_REVIEW:37 suggestions closed as QA, two HN repairs prepared; Phase1 two-row raw not archived in checked handoff roots, Phase2 draft withheld.
D3 still HUMAN_DECISION_REQUIRED:two S3 single-source counterexamples; no repair/Phase2/Human release under this division decision.
L0 source pin a83437a was executed on the 5090. The return is the synthetic-gate hard stop above, not a D1 score and not permission to rerun. D2/D3 handoff facts in this section are unchanged.
New chat starts recovery/inventory and existing-gate checklists only. Dataset changes, Human distribution/GT and formal experiments still require their own gates.
Shared checkout is not isolation: distinct private namespaces/domain files; serialize shared authority/Git updates, preserve the other lane and unrelated design/PDF.
No Candidate/Human/Evidence/Guide/Expected/model/config/old result mutations; no new experiment, training, formal split or GT freeze.
Status D2_D3_DATA_THREAD_HANDOFF_READY / WAITING_FOR_OWNER_TO_OPEN_THREAD; domain blockers remain open.

## Current — 2026-10-29 5090 Cursor handoff ready, real L0 run not started here

P1-VACE-L0-5090-CURSOR-HANDOFF-01; PODR-151/OR-105/REL-2026-0120; parent P1-VACE-L0-F5-ORACLE-STRONG-BASELINE-01.
Owner now explicitly chooses Cursor on5090, asks one-shot code push and unattended normal-phase continuation.
[Execution package](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/L0_5090_CURSOR_EXECUTION_PACKAGE_V1.md),
[stateV26](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V26.md).
LOCAL5060 blocker remains factual; this decision authorizes handoff preparation and Worker5090 execution, not local substitute inference.
Shared Qwen official revision a09a35458c702b33eeacc393d103063234e8bc28, BF16/SDPA/greedy, same120 F5 vs assignedE1/E2 Oracle.
Runtime/labels separated private ZIP V2 SHA03fae845b50d669373d3b08776caf5a1b2cf068ea7aa5b60dea89a65177e3eb2, not Git.
Source implements check-only, isolated optional setup≤24GiB, hash freeze, synthetic gate, checkpointed240 raw predictions, lock then independent evaluator/archive.
CPU/fictitious tests are not GPU/LLM acceptance. L0_5090_CURSOR_HANDOFF_READY / WORKER_NOT_STARTED; no L0 metrics yet.
Next Owner transfers one private ZIP and prompt to Cursor; normal Worker phases need no new scientific approval.
Stop for identity/budget/CUDA/synthetic/integrity failure; no model/protocol changes, post-result tuning or hard-gate bypass.
Do not expose evaluation labels to inference, upload raw data to Git, run D2D3/VACE-LM/training/formal GT/split.

## Current — 2026-10-28 L0 strong baseline approved, requested hardware absent

P1-VACE-L0-F5-ORACLE-STRONG-BASELINE-01; PODR-150/OR-104/REL-2026-0119.
Owner authorizes official Qwen/Qwen2.5-7B-Instruct, local RTX5090 32GB, new model/dependency≤24GiB, no global changes.
Read-only nvidia-smi enumerates only RTX5060 8151MiB; requested device identity gate FAIL.
[Blocker](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_HARDWARE_PREFLIGHT_BLOCKER_V1.md),
[stateV25](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V25.md).
L0-DEVICE-IDENTITY-BLOCKER-01 / L0_STRONG_BASELINE_PREFLIGHT_BLOCKED / HUMAN_DECISION_REQUIRED.
No claim CUDA software is broken; no kernel/model/synthetic/D1 inference. Model revision/license/weights/runtime freeze not completed.
L0-F5/Oracle NOT_EXECUTED; all detection metrics NOT_MEASURED, not0. No download/install/alternateGPU/CPU/quantization/remote/API.
Current task approval supersedes old not-approved L0 status, not its fail-closed device gate or formal research contract.
Next Owner supplies RTX5090 execution host/project entry. No new scientific approval needed for original aim, but no assumed Worker identity.
D1_DEV40/120/13families and8/24 HOLD, D2D3/Human/Guide/GT/Evidence/history/V03 results unchanged; formal GT/split not executed.
Only evidence/governance/Git preservation allowed before device issue resolves; no automatic new environment or experiment.

## Current — 2026-10-28 VACE-F5 development diagnostic complete, coverage inadequate

P1-VACE-LITE-V03-F5-IMPLEMENTATION-AND-D1-DIAGNOSTIC-01; PODR-149/OR-103/REL-2026-0118.
[Results](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_V03_IMPLEMENTATION_AND_TEST_RECORD.md),
[state V24](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V24.md).
Source559ff45 frozen/pushed before prediction; same signed40groups120rows13families;8/24 HOLD unchanged.
240 new predictions/trace locked before evaluator label/S/role join. Same frozen Hybrid Top5, all120 identities match.
V03-F5 and V02-NA-F5 both S1=1/12,S2=4/15,S3=1/13,total6/40,Clean/HN-FP0/40,Precision6/6.
SUPPORT0/CONTRADICT6/INSUFFICIENT114 each; all80 negatives abstain, strict triplet success0/40.
No continuous score/AUC/AP; no superiority or deployment claim.30/34 missed positives have frozen reference docs already inTop5.
I early exit1; pure external certificates5; NA external_resolved6 includes1 internal certificate (additive audit clarification).
VACE_V03_F5_DEV_DIAGNOSTIC_COMPLETE / OWNER_REVIEW_REQUIRED; scientific coverage inadequate, not an execution blocker.
No rule tuning/refit/old126; protected data/Human/Evidence/Guide/D2D3/history unchanged. Formal GT/split not executed.
Next recommend separately approved L0-F5/Oracle and slot-coverage preflight; DO NOT START L0/E2/D2D3/calibration/Stage B.
Below pre-prediction/design-only records are historical, not the current approval gate.

## Current — 2026-10-28 VACE V0.3-F5 bounded implementation and pre-prediction gate

P1-VACE-LITE-V03-F5-IMPLEMENTATION-AND-D1-DIAGNOSTIC-01; PODR-149/OR-103/REL-2026-0118.
Owner now approves bounded engineering and actual signed D1_DEV scoring; older design-only prohibition below is historical.
[Execution protocol](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_V03_F5_EXECUTION_PROTOCOL_V1.md).
Shared conservative six-slot/proof verifier, adaptive versus fixed nonadaptive, original frozen Hybrid Top5/Registry.
29 synthetic boundary tests plus21 historical contract tests pass; no D1 predictions/scoring yet.
Freeze source/config and gates before new240 prediction seal.
Same40/120/13families;8/24 HOLD; no Oracle/label/S/role runtime routing, no A0/B1 verdict shortcut.
No model training/download/new API/source or D2D3/Candidate/Human/Evidence/Guide/history/formal contract changes.
Next run only after engineering gates; final STOP OWNER_REVIEW_REQUIRED. No L0/E2/D2D3 automatic start.

## Current — 2026-10-28 VACE-Lite V0.3 adaptive verification design only

P1-VACE-LITE-V03-ADAPTIVE-VERIFICATION-DESIGN-01; PODR-148/OR-102/REL-2026-0117.
Source9f0d42e; [Owner packet](../research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_V03_OWNER_REVIEW_PACKET.md),
[state V23](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V23.md).
Candidate-only I needs a real same-domain contradiction certificate; A0 cue is not a verdict, B1 not a fallback.
Otherwise independent official evidence, Q obligations/gaps then bounded T/P/J acquisition; insufficient remains review.
F5 same-pool primary and E2 expansion/NA/L0 comparisons specified, no model or policy executed.
V0.2 was already six-slot/tri-state, not forced SEPT. Posthoc S-based75% is not measured V0.3 performance.
All V0.3 Recall/FPR/cost UNKNOWN/NOT_EXECUTED; old D1/A0/hold/raw/data/Guide/D2D3 unchanged.
Formal Research Plan Authority and long-term contracts unchanged; only new candidate specs/governance authorized.
STOP VACE_LITE_V03_OWNER_REVIEW_REQUIRED; no automatic implementation, training, new detection or formal evaluation.

## Current — 2026-10-28 A0 surface diagnostic complete; VACE-Lite V0.2 candidate review

P1-VACE-LITE-R1-SURFACE-BASELINE-AND-METHOD-REFINEMENT-01; PODR-147/OR-101/REL-2026-0116.
[Record](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_VACE_LITE_R1_RECORD_V1.md),
[state V22](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V22.md).
Same signed40 groups120 rows13families;8/24 HOLD. Original/general separately frozen,240 predictions sealed before scoring.
A0-original S1=12/12,S2=0/15,S3=4/13,total16/40,Clean-FP0/40,HN-FP3/40,Precision16/19.
A0-general=10/12,7/15,1/13,total18/40,Clean-FP6/40,HN-FP5/40,Precision18/29.
Binary-only flags, no fabricated AUC/AP or OOF; historical comparison same120 only, old126 unopened.
Original S1 cue coverage100%,four only 同一; S1 HN-FP2/12. No VACE efficacy claim.
Six-slot V0.2 method/spec and L0/L0-Oracle/slot evaluation are plans only; V0.1 full draft not located.
No VACE/LLM/model training/new data/Guide/GT/threshold/calibration/split or D2D3 execution.
STOP VACE_LITE_V02_OWNER_REVIEW_REQUIRED; next Owner reviews candidate design, no automatic implementation.
Below freeze-stage snapshot and prior D1 experiments remain historical records.

## Current — 2026-10-28 VACE-Lite R1 surface baseline and candidate method refinement

P1-VACE-LITE-R1-SURFACE-BASELINE-AND-METHOD-REFINEMENT-01; PODR-147/OR-101/REL-2026-0116.
Source cf4d669; same signed40 groups120 rows13families;8/24 HOLD unchanged.
External review located and to be raw-locked; V0.1 full draft unavailable, do not fabricate its details.
[Protocol](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_VACE_LITE_R1_A0_PROTOCOL_V1.md).
Now freeze original3 patterns/general6 cues separately before deterministic prediction; labels/S loaded after seal.
Only A0 diagnostic, S1/legitimate-HN cue audit, six-slot V0.2 candidate and L0 plans authorized.
No VACE/model/GT/Guide/data changes, old126, formal split, D2D3 evaluation or calibration.
Next final gate VACE_LITE_V02_OWNER_REVIEW_REQUIRED; finish docs/Git and STOP.

## Current — 2026-10-28 D1 first development results executed and sealed

PODR-146/OR-100/REL-2026-0115; Run D1-FIRST-DETECTION-20261028-R01.
[Results](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_D1_FIRST_DETECTION_RESULTS_RECORD_V1.md),
[state V21](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V21.md).
Real five-cell Owner signature/template audit PASS;40 groups120 candidates13 families accepted D1_DEV_ONLY;8/24 HOLD.
A/B1/B2/C each13-family-fold120 OOF,480 new predictions sealed before role/S evaluation join; old126 not read.
Primary B1 S1 2/12,S2 8/15,S3 10/13,overall20/40,HN-FP15/40,AUROC0.530625,AUPRC0.381391.
Same-column B2/C only: AUROC0.5365625/0.5871875; Original Oracle21 remains BLOCKED.
No high-performance claim; shallow representations and B1 scaling instability remain limitations.
Execution source5128429; first pre-fit JSON list/tuple assertion failure retained; no scientific tuning.
Next STOP; recommend separately approved atom-aligned claim/version failure audit, not started.
D1_DEV_EXPOSED; no Core formal GT/split, calibration, Stage B, real-data/D2D3 edits.
The execution-preflight section below is historical, not a still-pending signature or unrun model gate.

## Current — 2026-10-28 signed D1 development eligibility and execution preflight

P1-D1-DEVELOPMENT-DETECTION-FIRST-RESULTS-01; PODR-146/OR-100/REL-2026-0115.
Owner saved three explicit confirmations plus name/date; exact five logical cells differ from original template.
Actual file retains unsigned-template basename; missing claimed alternate filename logged, not fabricated.
Signed SHA35609f9ea3fa5fad2fca440dab6b16e57c2bc7954b53d0381ac9cae114049b5d.
40 groups120 candidates13 families accepted D1_DEV_ONLY;8 groups24 HOLD. S12/15/13.
A/B1/B2/C train-fold preflight PASS; no fit yet. Original Oracle21 remains BLOCKED by three all-null T columns.
[Protocol](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_D1_FIRST_DETECTION_PROTOCOL_V1.md),
[state V20](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V20.md).
Next freeze execution code, run four fixed new family-OOF conditions, lock predictions before evaluation role/S join.
No tuning/old126 reuse/real-data edits/Core GT/split/calibration/Stage B; D2D3 unchanged.
Earlier unsigned-stop entries are retained history, superseded only by verified signed qualification.

## Current — 2026-10-27 first D1 detection results stopped at unsigned Owner gate

Task P1-D1-DEVELOPMENT-DETECTION-FIRST-RESULTS-01; PODR-145/OR-099/REL-2026-0114.
Source HEAD81e91f44fe1fe1f77fbd61a3e5cfa6f927bd73ed; unique research worktree, upstream0/0 at preflight.
[Minimal todo](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_D1_FIRST_RESULTS_SIGNATURE_TODO_V1.md).
Read-only signature check: C13/C14/C15/C17/G17 all blank; workbook SHA unchanged from unsigned template.
D1_DEV eligibility NOT ACCEPTED;40 groups120 rows remain proposed,8 groups24 rows HOLD.
Owner explicitly approves V1.2-DEV-SEP18, S3/E9/P6, no T, same18 B2/C columns and processing;
this supersedes only the prior need for a separate SEP18 design approval, not dataset signature or fold preflight.
V1.1/extractors/history untouched; original Oracle SEPT21 remains BLOCKED.
A/B1/B2/C NOT_STARTED: no fit, new OOF, metrics, or old126 reuse; do not infer missing signatures.
D1_FIRST_RESULTS_BLOCKED_UNSIGNED / D1_PERFORMANCE_NOT_ESTIMATED; AUTO_CONTINUE=NO.
Next only Owner fills three confirmations/name/date, saves new signed file, returns exact path.
D1_DEV_EXPOSED, no Core formal GT/split or D2D3 changes. V19 materialization remains historical evidence.

## Current — 2026-10-27 D1 quality signature pending / SEPT materialized

Task P1-D1-QUALITY-HOLD-CLOSURE-AND-D1-SEPT-MATERIALIZATION-01;
PODR-144/OR-098/REL-2026-0113; source HEAD2ce4b1cdc0dc9d3953a0c11afc1d5961468bab4e.
[Record](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_D1_QUALITY_AND_SEPT_MATERIALIZATION_RECORD_V1.md),
[state V19](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V19.md).
Owner approved bounded QA/materialization, then offline isolated runtime cap4GiB; actual3,672,518,140 bytes.
55 nonnull/2null audited;33 conformant pending signature,21 HOLD-only,1 scope-unproven;
18 additional historical-status proposals remain QA. No automatic GT promotion.
144 identities/48 triplets scanned; semantic lock precedes restricted construction join.
40 groups120 rows ELIGIBLE_CANDIDATE /8 groups24 rows HOLD; effective evaluated0/0.
New Chinese Owner workbook leaves final fields blank and permits three bounded batch confirmations.
33 corpus docs/34 raw SHA,144 fixed queries,14,256 exact-replayed rankings; Oracle identity read after retrieval lock in engineering process.
B/C each144x21, same Feature Set V1.1/definitions/null semantics, R excluded; no classifier fit.
New engineering blocker: Oracle FEMALE_WORKER_PROTECTION holdout has three all-null train T columns.
No fill0/drop-only-C or model run; quality signature and separate comparable missingness decision required.
D1_DATA_QUALITY_GATE_PENDING / D1_SEPT_MATERIALIZED / D1_PERFORMANCE_NOT_ESTIMATED.
AUTO_CONTINUE=NO. Old126 scores not reused; Core GT/2/1/1 not executed; D1_DEV_EXPOSED.
D2 targeted-two and D3 two-S3 gates/data unchanged. No new source/model/Expected or Human raw overwrite.
This section supersedes V18's not-materialized status only; no detection rate/CI/HN-FPR is known.

## Current — 2026-10-27 D1 exploratory sprint NOT_EVALUABLE; Owner quality gate

Task `P1-D1-EXPLORATORY-DETECTION-FEASIBILITY-SPRINT-01`;
PODR-143/OR-097/REL-2026-0112; source HEAD892915a830f9762d2cf239fcfb21cb8b26f186fb.
Unique branch-bound worktree verified on research/stage6-1-hidden-poisoning.
[Record](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_D1_EXPLORATORY_DETECTION_CLOSEOUT_RECORD_V1.md),
[state V18](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V18.md).
Owner approved D1-only exploratory development, not Core formal training/test/GT.
Three AI-assisted inputs byte-locked;57 aligned field recommendations,55 nonnull,
two0028 unresolved; no automatic QA-to-GT promotion or workbook save.
144 identities/48 groups/13 families restored. Original five HOLD seeds plus0038
scope precaution precede126-row preparatory A fit/13-family OOF, fixed config.
Post-prediction-lock quality check found0093/0098 same institutional-role boundary
outside54; preflight had not fully closed before fit. Quarantine126 OOF; no real
performance metrics calculated, no refit. Whole-triplet holds total8 groups24 rows;
provisional40/120 remains NOT accepted for evaluation. Valid evaluated0/0.
B/C have generic code but no validated D1-bound corpus/registry/retrieval/SEPT matrix
or same-column Oracle adapter; Final72 matrix72x21 matches D1 text0/144.
D1_DEV_EXPOSED; no recall/CI/HN-FPR/Oracle gap or long-context effectiveness claim.
HUMAN_DECISION_REQUIRED / Auto Continue=NO: verify/preserve/governance/Git only.
Next Owner quality/scope decision, then separately bounded D1 materialization;
recommended task P1-D1-QUALITY-HOLD-CLOSURE-AND-D1-SEPT-MATERIALIZATION-01 not started.
D2 targeted-two external gate and D3 two S3 blockers unchanged; no D2/D3 data edits,
Expected/formalGT, formal2/1/1 split, calibration or new source/model/AI call.
Older D1 no-training statements below are historical before this bounded approval;
they do not erase the quarantined preparatory fit or authorize formal results.

Continuation 2026-10-27: the bounded D2 semantic/repair gate below is unchanged.
Owner requests continuation of the interrupted closeout only. Existing55-file seal
12cf8d94b793ed4a2ca3436be8d56217c71f281d623e77e74c0b60d6995aa10c
and prior semantic seal reverified; delivery/Git receipts are additive post-seal.
No new Reviewer return received; full144/Human/GT gates remain withheld.

## Current — 2026-10-16 D2 semantic QA complete; two repaired HN await targeted review

Task `P1-CORE144-D2-PHASE2-OWNER-SEMANTIC-ADJUDICATION-AND-CONSTRUCTION-CONTRACT-AUDIT-01`.
Source HEAD484b04bb6f59b1c7edbe4cb488019c94b774c95c; PODR-142/OR-096/REL-2026-0111.
[Record](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_OWNER_QA_AND_TWO_HN_REPAIR_RECORD_V1.md),
[state V17](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V17.md).
37 historical proposals independently ACCEPT/42 fields; six Owner semantic cases recorded.
Semantic seal814c92c2...edc3e7 precedes private two-case construction read.
Carrier overall insufficient but institutional authority correct; service scope conflict.
Both original roles HN: conditional authorized minimal V2/new-ID repairs,142 rows unchanged.
No raw/Guide/source/process overwrite or GT. Phase1 two-row packages ready for original
D2 R3_GPT/R4_CODEX(actual DOUBAO), Phase2 drafts withheld pending new Phase1 raw lock.
D2_FULL144_PREANNOTATION_ACCEPTANCE=PENDING_TARGETED_TWO_REVIEW; no Human Excel release.
Next: two original-session Phase1 returns, then Phase2, then final144 acceptance audit.
D1 bounded54 Owner adjudication and D3 two S3 blockers remain separate; no Expected,
Human-label feedback, formal split, detector or threshold run. AUTO_CONTINUE=NO.
Older D2 Owner-pending entries below are superseded only by this bounded semantic
QA/conditional repair decision, not full domain acceptance.

## Current — 2026-10-16 D1 bounded54 review complete; Owner adjudication pending

Task `P1-CORE144-D1-HUMAN-AB-BOUNDED54-TRIAGE-AND-OWNER-ADJUDICATION-PREP-01`;
source HEADacabd501d26a10a9169763511f470f656fcfebcf; PODR-141/OR-095/REL-2026-0110.
Owner: “对54条做有界审查并准备Owner仲裁材料”.54/54 queue rows reviewed,
34 cases/47 author proposal cells;57 field items with blank Owner final values.
New Owner workbook/packet only, original Excel/raw/selection/Guide/evidence unchanged.
Priority evidence gaps0051/0121 and role/internal-conflict cases0078/0116
require Owner disposition. No author proposal effective, no GT or automatic rereview.
[Record](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D1_BOUNDED54_REVIEW_AND_OWNER_PREP_RECORD_V1.md),
[state V16](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V16.md).
No Expected/construction mapping/roles/Reviewer answers/new source/Guide change,
split/model or D2/D3 advancement. OWNER_ADJUDICATION_PENDING / AUTO_CONTINUE=NO.
Prior pending bounded-review approval below is superseded only for this exact54
preparation task, not final annotation acceptance.

## Current — 2026-10-16 D1 presentation exception accepted; A/B comparison complete

Task P1-CORE144-D1-HUMAN-PRESENTATION-EXCEPTION-AND-AB-COMPARISON-01.
[Comparison](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D1_HUMAN_AB_COMPARISON_RECORD_V1.md),
[state V15](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V15.md).
PODR-140/OR-094/REL-2026-0109; source HEAD2845e8e. Owner explicitly approves only
the123-cell A01 presentation equivalence and A/B comparison, original bytes unchanged.
Old literal-parity failure remains a historical fact, not normalized away.
144 exact-text pairs/assigned E1E2 bundles match; old50-file index/raw/issued/own
Phase1 hashes unchanged. Phase2 semantic964/1008 (95.6349%),31 rows/44 cells;
21 process-only,92 all-eight-equal. Phase1 differences3 rows,2 local/minimum-linked.
Review union54=31 Phase2+1 extra Phase1+22 extra quality leads, not54 proven errors.
Quality leads27 include A2/B1 insufficiency and B24 reason/selection leads;10 of
the21 process-only rows overlap review union,11 archive-only. No answer correction,
proposed/effective adjudication null, no consensus-as-GT. Direct OWNER_ATTESTED
not machine proof. No Expected/mapping/roles/external Reviewer answers/new source/
workbook save/split/model or D2/D3 advancement. Stop for separately approved
bounded54 triage/adjudication-prep; AUTO_CONTINUE=NO / NO_GT.
Older pending123-cell exception/comparison-withheld entries are superseded only
within this explicitly approved scope. D2 source/scope/D3 S3/Human gates unchanged.

## Current — 2026-10-16 D1 Human Phase2 locked; presentation exception pending

P1-CORE144-D1-HUMAN-DUAL-PHASE2-RAW-LOCK-AND-COMPARISON-01;
source HEAD5d66be1; PODR-139/OR-093/REL-2026-0108.
[Receipt/gate](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D1_HUMAN_PHASE2_RAW_LOCK_AND_RECEIPT_GATE_V1.md),
[state V14](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V14.md).
Both144 raw locked before decode; own IDs/order/Candidate/headers/1152 enums/
144 reasons each legal,0 mechanical crossfield flags. A01 readonly123 boundary-
whitespace changes (60 annotation/48rows,63 fulltext),0 substantive. B01 only315
blank-storage changes. A01 exact readonly gate held; no automatic waiver.
Separate A2/B1 evidence-limitation rows/B24 selection-reference leads retained.
No A/B join/comparison/consensus, Expected/GT/mapping/role load or workbook save.
Direct Owner independence/no-resave confirmation OWNER_ATTESTED, not machine proof.
HUMAN_DECISION_REQUIRED / Auto Continue=NO: readonly verification/evidence/context/
Git only; Owner bounded123-cell presentation decision first. D2 source/scope and
D3 S3/Human gates unchanged. Older D1 pending-return text is history.

## Current — 2026-10-16 D2 targeted6 locked; Owner source/scope decision required

P1-CORE144-D2-TARGETED6-PHASE2-RAW-LOCK-AND-QA-GATE-01; source HEAD1bd7668;
PODR-138/OR-092/REL-2026-0107. [Record](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_TARGETED6_PHASE2_RAW_LOCK_AND_QA_GATE_V1.md),
[state V13](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V13.md).
Both6 original returns locked unchanged before parse; own IDs/order/11 fields/
48 enums/reasons PASS each, zero detected cross-field flags. Five semantic rows/
nine cells plus one process-only. Two restored-clause facts and two fine-reason
scope defects resolved; three version presence execution differences already
covered by V4.2/V4.3, no new rule. Carrier evidence gap and other-services scope
remain two material Owner items. Proposed values not applied, prior37 unaccepted.
Owner-relayed Reviewer isolation declarations, not machine proof/new direct
OWNER_ATTESTED. Original D2 GPT/Doubao provenance; no new reviewer round.
HUMAN_DECISION_REQUIRED / Auto Continue=NO; only read-only evidence/context/Git
preservation pending Owner. No Candidate/Evidence/Guide/raw repair, new source,
Human D2D3, Expected/GT, hidden role loading, split or model. D1/D3 gates unchanged.
Older waiting-for-six-return entries are history; no Human authorization follows.

## Current — 2026-10-15 D2 excerpts V3 repaired; targeted6 original-session gate

P1-CORE144-D2-PHASE2-EXCERPT-V3-REPAIR-AND-BOUNDED43-REVIEW-01;
source HEADa4baf3b; PODR-137/OR-091/REL-2026-0106.
[Repair/review](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_PHASE2_EXCERPT_V3_BOUNDED43_REVIEW_RECORD_V1.md),
[state V12](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V12.md).
Owner approves only two excerpt V3 repairs and43 old-rule bounded cases.
Full article2/8 restored from frozen texts; both144 own records and25 original
hashes/old74/18 sealed files unchanged. Two doc presentations changed,23 equal.
43 author proposals:37 local,6 original-session targeted pending; not Owner final
adjudication/GT; no raw/evidence_selection override. Carrier/services and two
general/severe reason-scope cases remain in six. [Exact seven-file addresses](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_TARGETED6_PHASE2_V3_OWNER_SEND_CHECKLIST_V1.md).
Continue original D2 GPT/R4_CODEX Doubao sessions; unavailable => incident STOP.
D2 machine/Human unaccepted; D1 gates/D3 two blockers unchanged. Old-run isolation
OWNER_ATTESTED; new targeted execution unobserved. No Expected/GT/new source/
Candidate/Guide semantics/split/model. STOP_EXTERNAL_REVIEW_REQUIRED; Auto
Continue=NO. Older pending-repair text below is historical in that approval scope.

## Current — 2026-10-15 D2 Phase2 raw locked; evidence/semantic gate held

Task P1-CORE144-D2-PHASE2-RAW-LOCK-AND-COMPARISON-01;
source HEADc741120d; PODR-136/OR-090/REL-2026-0105.
[Raw identities/comparison](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_PHASE2_RAW_LOCK_AND_COMPARISON_RECORD_V1.md),
[state V11](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V11.md).
Two originals byte-locked before parse;144 each, own V2 ID/order/11 fields,
1152 enums/reasons PASS.42 semantic rows/50 cells;15 process-only differences.
Five quality flags/three candidates; semantic-quality union43, not43 proven defects.
Two source articles exist in frozen fulltext but are omitted from V2:bank-law
article2 and nonbank-payment article8. Additive correction to October7 broad
excerpt-completeness inference; old74-file index/source/package/raw unchanged.
Meeting-record carrier is a separate unresolved proposition-sufficiency item.
D2 NOT machine-preannotation accepted; Human D2 NOT authorized; Owner bounded
V3 excerpt repair/43-case triage decision pending, Auto Continue=NO. No V3 or
Candidate/Guide/answer patch executed. Original D2 sessions OWNER_ATTESTED;
R4 actual Doubao. D3 prior two blockers and D1 Human gates unchanged.
No Expected/GT/R5/Human D2D3/split/model/calibration. Unrelated design/PDF excluded.
Older ready-not-distributed entries are history; Owner now reports D2 returns.

## Current — 2026-10-07 D2 Phase2 excerpts ready; D3 necessity gate held

Task P1-CORE144-D2-D3-PHASE2-PACKAGE-PREFLIGHT-AND-RELEASE-PREP-01;
source HEAD33559e0d; PODR-135/OR-089/REL-2026-0104.
[Preflight/release record](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_D3_PHASE2_PREFLIGHT_AND_RELEASE_RECORD_V1.md),
[state V10](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V10.md).
Replayed current144/48 per domain; source raw/text hashes50/48 PASS, repair-path
drift0; own Phase1 views QA-only retain8/18 naturalness variance. D2 scoped16/16
S3 necessity; two approved traceable-excerpt whole144 V2 seven-file folders
byte-copied to Owner handoff, READY_NOT_DISTRIBUTED. Original full bodies retained.
Actual platform capacity unverified; no96+48 fallback or manufactured limit.
D3 two single-source counterexamples => Phase2 WITHHELD; Owner bounded repair
decision pending, Auto Continue=NO for D3. Hash PASS is not semantic release.
R4_CODEX actual Doubao; original domain sessions only, OWNER_ATTESTED.
D1 individual Human gates unchanged, no human answers read. No new Candidate/
Guide/raw/Evidence rule, Human D2/D3, Expected/GT, R5, split/model/calibration.
Next Owner: exact D2 seven-file send list; separately decide D3 two-item repair.
Unrelated design Markdown/PDF excluded. Older current headings remain history.

## Current — 2026-10-06 D1 B01 own Phase1 locked; B01 Phase2 release authorized

Task `P1-CORE144-D1-B01-PHASE1-RAW-LOCK-AND-PHASE2-RELEASE-01`; source HEAD
64e1152e; PODR-134/OR-088/REL-2026-0103. [B01 raw identity and individual gate](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D1_HUMAN_B01_PHASE1_RAW_LOCK_AND_PHASE2_RELEASE_V1.md),
[state V9](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V9.md).
Raw37,202 bytes locked before parse;144 unique B01 IDs/order/text exact,720
legal enums,16/16 required notes; non-answer cells unchanged. Matching original
B01 Phase2 hash/144 rows/1,440 blank answers/225 official links PASS.
PODR-125's own-human condition is satisfied; B01-only two-file Owner send list
includes unchanged Excel and detailed Chinese manual. Actual distribution not
observed; no annotations generated or changed, no A/B comparison or GT.
A01 existing authorization unchanged; no assumption of A01 delivery/return.
D2/D3 Phase1 quality PASS still requires separate Owner Phase2 preparation
approval; both remain withheld. No Expected, split, model or calibration.
Private experiments/core144_d1_b01_phase1_raw_lock_20261006/ and E-drive mirror;
unrelated design Markdown/PDF excluded. Next: Owner sends two files to same B01.
Older current headings below are retained history, not current B01 gates.

## Current — 2026-10-06 bounded4 V2 raw locked; Phase1 quality QA PASS; Phase2 held

Task `P1-CORE144-D2-D3-BOUNDED4-PHASE1-V2-RAW-LOCK-AND-REVIEW-CLOSEOUT-01`;
source HEAD c4e0b1af; PODR-133/OR-087/REL-2026-0102.
[Raw identities, dispositions and gate](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_D3_BOUNDED4_PHASE1_V2_RAW_LOCK_AND_QA_RECORD_V1.md),
[state V8](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V8.md).
Four V2 originals byte-locked before strict parsing; exact3/1 ID/order/schema/note
checks PASS. Five fields100% targeted agreement; four material text-visible items
resolved for Phase1 QA. Current144 views per reviewer/domain preserve raw lineage
and eight/eighteen prior nonblocking naturalness variances without voting.
Both phase1_quality_gate_pass=true; no Owner dataset acceptance inferred.
Both phase2_release_authorized=false; no Phase2 generation this turn. Next:
Owner approve `P1-CORE144-D2-D3-PHASE2-PACKAGE-PREFLIGHT-AND-RELEASE-PREP-01`.
Original sessions OWNER_ATTESTED only; R4 actual Doubao. D2 byte equality proves
neither independence nor copying. No Candidate/rule/raw change, Expected/GT,
Human D2/D3, R5, split or training. D1 gates unchanged. Unrelated design Markdown
and pre-existing PDF excluded. Older current headings below are history.

## Current — 2026-10-05 Owner-approved bounded4 repair prepared; external rereview next

Task `P1-CORE144-D2-D3-BOUNDED4-MINIMAL-REPAIR-AND-TARGETED-REREVIEW-01`, source
HEAD efd7ed3b; PODR-132 / OR-086 / REL-2026-0101. Owner authorizes D2 three/D3
one only. [Current repair and physical evidence](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_D3_BOUNDED4_REPAIR_RECORD_V1.md)
and [state V7](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V7.md).
Four V4 new-ID rows, old immutable; facts/atoms/paths/metadata/rules/raw unchanged.
Both full corpora retain144 rows/48 groups; unchanged141/143. Four targeted
candidate-only V2 packages3/1 with matching schema/prompt are ready for the
same original D2/D3 R3 GPT and R4_CODEX/Doubao sessions, no new/mixed sessions.
Private Owner send checklist contains exact twelve handoff file addresses.
New-ID reviewer answers do not yet exist; previous provisional144 views are
historical, not accepted current answers. Four returns pending; both Phase1
unaccepted / Phase2 withheld. No Expected/GT/Human answers/R5/new rules or sources,
Human D2/D3, split or training. D1 gates unchanged. Unrelated design Markdown
and PDF excluded. Older current headings below are preserved history.
`STOP_EXTERNAL_TARGETED_REVIEW_REQUIRED / D2_D3_PHASE2_WITHHELD`.


## Current — 2026-10-05 D2/D3 targeted raw locked; four material items hold Phase2

Task `P1-CORE144-D2-D3-TARGETED-PHASE1-RAW-LOCK-AND-DOMAIN-GATE-01`, source
HEAD cbe8e967; PODR-131 / OR-085 / REL-2026-0100. Four targeted returns received
and byte-locked: D2 25 each, D3 32 each, strict count/ID/order/schema/enum/note
checks PASS. Owner confirms same original domain-isolated sessions, authorized
inputs only: OWNER_ATTESTED, not machine proof; R4_CODEX actual provider Doubao.
D2 four targeted disagreement cells (one minor-naturalness nonblock, two
referent and one surface item); D3 seven (six minor nonblocks, one local-scope
blocker). No reviewer voting or raw normalization. No new Candidate/rule.

[Current evidence and bounded decision](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_D3_TARGETED_PHASE1_LOCK_AND_GATE_V1.md)
and [state V6](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V6.md).
Provisional 144-row views each retain historical119+target25 or112+32, not final
accepted answers. D2 open items=3; D3=1 (normative prohibition versus practical
restriction despite available alternative). Both Phase1 unaccepted / Phase2
withheld. Next Owner: bounded four-text repair/rereview or individually reasoned
disposition. Before decision no repair, Phase2, R5, Human D2/D3, Expected/GT,
split or training. D1 individual Human gates unchanged. Unrelated design.md and
untracked PDF stay excluded. Sections below are historical checkpoints.

## Current — 2026-10-03 Core144 D2/D3 authorized triage and additive targeted repairs

Owner task `P1-CORE144-D2-D3-PHASE1-OWNER-TRIAGE-TARGETED-REPAIR-AND-PHASE2-GATE-01`
supersedes the pending-triage next action below, not historical evidence.
The original 62 cases resolve to 43 REPAIR / 19 NONBLOCKING_VARIANCE / 0 KEEP;
full-domain QA adds 14 separately tracked surface repairs. Final changed sets:
D2 25, D3 32. Necessary-scope repairs: five per domain; D3 includes the explicit
same-alternative-condition repair of CBR-81E40769899B68. Original raw values are
not overridden. Four targeted packages contain only changed new opaque IDs/text.

[Bounded triage/lineage/QA record](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_D3_PHASE1_OWNER_TRIAGE_RECORD_V1.md)
and [parallel state V5](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V5.md)
are current. Evidence/atoms/design roles/HKP/path/S/families and frozen rules remain
unchanged. Internal QA is construction-author/mechanical evidence, not independent
semantic acceptance. Four external targeted replies remain pending; both Phase2
gates are held. Use the original domain-specific R3 GPT / R4_CODEX Doubao sessions,
not fresh sessions and not mixed domains. No Human D2/D3, GT, split or training.
D1 person-level Human gates remain independent and unchanged.

`D2_D3_PHASE1_OWNER_TRIAGE_COMPLETE / TARGETED_REPAIR_PREPARED /
D2_D3_PHASE2_WITHHELD / STOP_EXTERNAL_TARGETED_REVIEW_REQUIRED /
CORE_GT_NOT_FROZEN / SPLIT_NOT_EXECUTED / TRAINING_NOT_STARTED`.


## Current — 2026-10-03 Core144 D2/D3 Phase1 originals locked; both Phase2 gates held

Owner supplies four 144-row originals and attests fresh isolated sessions
(`OWNER_ATTESTED`; R4 provider Doubao). Byte locks, exact reviewer ID/order,
seven keys/enums/required notes all pass. D2 has 22 differing rows/26 cells;
D3 has 30/34. Shared quality flags also need review; these are not defect counts.
[Identities, candidate-only diagnosis and Owner decision](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_D3_PHASE1_RAW_LOCK_AND_GATE_V1.md)
bind the private 29+33-case packet. No mapping/labels/Evidence/Expected/GT/Human
answers loaded. `D2_D3_PHASE1_RAW_LOCK_COMPLETE / PHASE1_STRUCTURE_VALID /
OWNER_PHASE1_TRIAGE_REQUIRED / D2_D3_PHASE2_WITHHELD / CORE_GT_NOT_FROZEN /
SPLIT_NOT_EXECUTED / TRAINING_NOT_STARTED`. D1 person-level gates retain the
dated entry below. Next: Owner chooses exact bounded repairs/nonblocking
decisions; retain original sessions. Old unsent/D3-pending entries are history.

## Current — 2026-10-02 Core144 D1 A01 Phase1 locked; A01-only Phase2 release authorized

Owner identified the `(2)` workbook as the authoritative HUMAN-A01 Phase1
return. The exact bytes are locked read-only outside Git (36,361 bytes; SHA256
`d752d27451fcbae9ffba82b6bb33445452ef8b51e35f68877793687216f21b28`).
The [validation/release record](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D1_HUMAN_A01_PHASE1_RAW_LOCK_AND_PHASE2_RELEASE_V1.md)
passes 144/144 A01 ID/order/Candidate parity, enums and 15/15 required notes.
Owner may now send only the exact A01 Phase2 workbook in the
[A01 checklist](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D1_HUMAN_A01_PHASE2_OWNER_SEND_CHECKLIST_V1.md)
to the same A annotator. B01 is still completing the correct B01 Phase1
workbook; B01 Phase2 remains withheld. The `(3)` workbook remains separate
routing/history evidence. `A01_PHASE2_RELEASE_AUTHORIZED /
A01_PHASE2_NOT_YET_DISTRIBUTED / B01_PHASE1_IN_PROGRESS /
B01_PHASE2_WITHHELD / CORE_GT_NOT_FROZEN / SPLIT_NOT_EXECUTED /
TRAINING_NOT_STARTED`. Prior Human-distribution statements below are dated
history.

## Current — 2026-09-30 Core144 D2 internally constructed; D3 next, no external release yet

The Owner-authorized D2/D3 construction task is in progress. D2 Finance has
completed its **internal construction-only** gate: 48 frozen groups, 144
candidates and two separate 144-row, candidate-only R3/R4 Phase1 packets.
[D2 checkpoint and private evidence index](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D2_FINANCE_INTERNAL_CONSTRUCTION_RECORD_V1.md).
No R3/R4 external D2 review has occurred. Under the same authorization, D3
Information Security is the next evidence-first domain; the combined four-packet
Owner send gate is still closed. D1 Human A/B workbooks remain distribution-ready
but not recorded as distributed; Phase2 is sealed. Do not read D1 Human answers
to construct D3. `D2_FULL144_INTERNAL_QA_ACCEPTED /
D3_CONSTRUCTION_PENDING / EXTERNAL_PHASE1_NOT_STARTED /
CORE_GT_NOT_FROZEN / SPLIT_NOT_EXECUTED / TRAINING_NOT_STARTED`.
Prior "Current" headings below are dated history.

## Current — 2026-09-28 Core144 object/referent boundary clarified; XLSX unchanged

`P1-CORE144-SELF-CONTAINMENT-REFERENT-CLARIFICATION-01` adds only explanation to the [Master Guide](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md): independent object-supply versus multiple-antecedent tests, a 2×2 table, four fictional cases and three note patterns. All original 30 cases (including 05/06) remain verbatim; total cases are now 34. No field, enum, accepted protocol, Candidate, ID/order or raw changes. [New QA/closeout record](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_SELF_CONTAINMENT_REFERENT_CLARIFICATION_RECORD_V1.md) verifies all four XLSX hashes unchanged. `CORE144_SELF_CONTAINMENT_REFERENT_BOUNDARY_CLARIFIED / MASTER_GUIDE_UPDATED / HUMAN_WORKBOOKS_UNCHANGED / HUMAN_AB_NOT_YET_DISTRIBUTED`. Phase2 remains sealed. Next: Owner reviews the Markdown clarification; any later workbook explanation synchronization or distribution is separate. No new annotation, GT, split, training, calibration or D2/D3 construction this turn. Existing PDF is untouched and is not certified as matching this updated Markdown. Prior current headings are dated history, not latest counts.

## Current — 2026-09-28 Core144 Human Master Guide ready; workbooks unchanged

`P1-CORE144-HUMAN-ANNOTATION-MASTER-GUIDE-V1-01` completes an explanation-only [human master guide](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md), integrating current 8/20-column Human XLSX and frozen V4–V4.3, with 31 sections/30 fictional cases/20 high-risk rows. [QA and closeout](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_QA_RECORD_V1.md) records all four workbook SHA values unchanged, no new semantic rule, no data/ID/order change and no actual-answer teaching leakage. `CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_READY / CURRENT_HUMAN_WORKBOOKS_UNCHANGED / HUMAN_AB_NOT_YET_DISTRIBUTED`. Phase1 remains distribution-ready but not sent; Phase2 sealed per person. Next: Owner reviews guide before deciding later Excel explanation sync/distribution. Earlier D2/D3 construction authorization remains historical authority, but this turn performs no D2/D3 construction, Human annotation, GT, split, training or calibration. No formal result. Prior current entries below are dated history.

## Current — 2026-09-27 Core144 D1 Full144 accepted; Human Phase1 ready, D2/D3 lane open

R3/R4 remaining90 Phase2 originals were locked and compared. Nine semantic field differences across seven Candidates were resolved with a separate Owner rule overlay; 12 `evidence_selection` differences remain legitimate reviewer-process differences, not a unique-truth conflict. D1 Full144 machine preannotation acceptance passed: 48 groups, 144 Candidates. Distinct A01/B01 Phase1 XLSX files passed OOXML read-back, visual rendering and leakage QA; they are `DISTRIBUTION_READY_NOT_DISTRIBUTED`. Separate Phase2 XLSX files remain `SEALED_WITHHELD`. [Exact paths and gate](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_D1_HUMAN_PHASE1_GUIDE_V1.md); [parallel lanes](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V1.md). D2/D3 evidence-first construction is authorized and slot preflight has started, but no new D2/D3 Candidates yet. No Human return, Core GT, split or training. Earlier current-state entries below are historical.

## Current — 2026-09-27 D1 remaining90 Phase2 V5 ready for Owner same-session distribution

Owner confirmed R3/R4 targeted-four original-session isolation as `OWNER_ATTESTED` and approved the two exact sufficiency-checked E1/E2 presentations for groups that originally retained three frozen snapshots. All 23 raw official snapshot hashes pass; the third sources remain private and immutable. Two read-only 90-row Phase2 V5 reviewer packets now preserve each reviewer's own Phase1 order and the current 86+4 Candidate lineage. [Exact per-reviewer sending checklist](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE2_OWNER_SEND_CHECKLIST_V5.md) and [release record](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE2_RELEASE_RECORD_V5.md) are authoritative. `PHASE2_PACKET_READY / EXTERNAL_PHASE2_RETURNS_PENDING`; do not create a new Phase2 session. D1 Full48 preannotation acceptance, Human A/B, D2/D3 construction, GT, split and training have not occurred. The earlier pending-Evidence entry below is historical.

## Current — 2026-09-27 targeted-four Phase1 mechanical QA passes; Phase2 evidence decision pending

Both immutable R3/R4 four-row returns match their own package IDs/order and legal schema. Both identify the four intended internal contradictions with self-containment PASS and no ambiguity/template marker; Owner classifies the single new naturalness variance as nonblocking. The final Phase1 overlay retains 86 original 90-row values and substitutes only four versioned IDs/returns. The identified fixed Poison-only authority wording is removed, with residual two-row wording explicitly watched. Official evidence preflight verifies 23/23 raw snapshot hashes; two groups originally have three snapshots while the Phase2 answer contract exposes E1/E2 only. Await explicit Owner decision on [two bounded reviewer-presentation projections](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE2_EVIDENCE_PROJECTION_DECISION_V1.md) and targeted-run isolation attestation. No Phase2 reviewer packet is distributed, and no Human A/B, D2/D3 construction, GT, split or training starts. [Bounded raw-lock report](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_REMAINING90_TARGETED4_PHASE1_LOCK_AND_GATE_V1.md). Older “four returns pending” entries below are historical.

## Current — 2026-09-27 Core144 scope frozen; D1 targeted-four external Phase1 pending

Owner closed four remaining90 text-internal contradictions as YES by candidate semantics, not R4/R5 majority; six naturalness differences are nonblocking. A sealed role audit found the repeated dual-promulgating-organ surface only in four Poison (Clean/HN 0/0), so the prior Phase2 release route is blocked. Exactly four texts/opaque IDs have additive V2 surface repairs, with 86 unchanged; R3-gpt and R4-codex (actual Doubao, `OWNER_ATTESTED`) must rerun those four in their original isolated sessions. [Current gate and sending checklist](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE1_FINAL_GATE_V1.md). `PHASE2_WITHHELD_UNTIL_TARGETED_REVIEW / STOP_EXTERNAL_REVIEW_REQUIRED`.

Owner now defines the current core scope as D1/D2/D3, 144 planned groups/432 candidates; D4/D5 are deferred external extensions and the Formal240 five-domain design is preserved historically. [Core144 decision](../research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_SCOPE_DECISION_V1.md). Future lanes are Lane A `HUMAN_ANNOTATION` and Lane B `CORE_DATA_CONSTRUCTION`; both await D1 machine preannotation acceptance and D1 Human Phase1 Excel readiness before D2/D3 may start. `HUMAN_AB_NOT_STARTED / D2_D3_NOT_STARTED / GT_NOT_CREATED / SPLIT_NOT_EXECUTED / TRAINING_NOT_STARTED`. Older current headings below are dated history.

## Current — 2026-09-27 R5-Claude targeted Phase1 raw locked; Owner decision pending

R5's ten-row auxiliary original is immutable (3,563 bytes; SHA256 `788061588e4a42cbb80fda6aaf866944bc2cc027bbc589076f2313820ad463e3`) and passes strict packet ID/order, seven-key, enum and note checks. Owner attests R5's independent candidate-only isolation; no platform log is claimed. For the six R3/R4 naturalness disagreements, R5 matches R4's `NATURAL`; for the four material internal-conflict disagreements, R5 matches R4's `YES` and cites the same document's two incompatible promulgating authorities. This is auxiliary evidence, not a three-reviewer vote that changes R3 or settles the Owner gate. The repeated `既是…同时又是…` construction surface needs a separate shortcut audit. [Detailed lock and triage](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_RAW_LOCK_AND_TRIAGE_V1.md). `PHASE2_RELEASE_AUTHORIZED=FALSE / OWNER_ADJUDICATION_PENDING / HUMAN_AB_NOT_AUTHORIZED / GT_NOT_CREATED / SPLIT_NOT_EXECUTED / TRAINING_NOT_STARTED`. The preceding R5-package-ready section is a dated snapshot.

## Current — 2026-09-27 D1 remaining90 Phase1 pair locked; auxiliary dispute review pending

Owner corrected a misattached R3 incident file and supplied the actual R3 90-row original. Corrected R3 and R4 originals are read-only, with matching source/copy hashes and exact 90/90 ID/order/schema/enum checks. Their five Phase1 categorical fields agree 84/90, 86/90, 90/90, 90/90, 90/90; six naturalness differences and four material internal-conflict differences remain. The withdrawn incident is preserved as wrong-attachment history, **not** evidence of current R3 isolation failure. [QA and triage](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE1_R3_R4_RAW_LOCK_QA_AND_R5_AUXILIARY_V1.md). Owner attests R3 isolation. R4 described its own Doubao isolation; Owner confirmation is pending. At Owner's suggestion a ten-row candidate-only [Claude auxiliary package](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_OWNER_SEND_CHECKLIST_V1.md) is ready, not sent or returned by this task. `PHASE2_RELEASE_AUTHORIZED=FALSE / HUMAN_AB_NOT_AUTHORIZED / GT_NOT_CREATED / SPLIT_NOT_EXECUTED / TRAINING_NOT_STARTED`. Prior "MegaWave raw not received" sections below are dated snapshots.

## Current — 2026-09-27 R4-codex code retained; Doubao execution route corrected

Owner confirms `R4-codex` is a fixed reviewer code and the actual prior/future R4 model/platform is Doubao. The old Codex Project/projectless attribution is superseded by [additive provenance erratum](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_R4_CODEX_DOUBAO_PROVIDER_PROVENANCE_ERRATUM_V1.md); raw returns and scientific gate decisions are not rewritten. For remaining90 Phase1, use the [V2 exact file checklist](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE1_REVIEWER_FILE_CHECKLIST_V2.md): fresh R3 GPT session, separate fresh R4 Doubao session; R4 code/filenames unchanged. Provider and isolation are `OWNER_ATTESTED`, not platform-log verified. No MegaWave raw has arrived. `STOP_EXTERNAL_REVIEW_REQUIRED / PHASE2_WITHHELD / HUMAN_AB_NOT_AUTHORIZED / GT_NOT_CREATED / SPLIT_NOT_EXECUTED / TRAINING_NOT_STARTED`. Earlier dated Codex-mode paragraphs below are historical snapshots.

## Current — 2026-09-27 D1 remaining90 Phase1 MegaWave ready; external review required

HKP2/HKP3/HKP4 Evidence-first internal construction and bounded QA now cover 30 frozen groups/90 candidates (ten groups per HKP; C/P/H 30/30/30). The private cross-batch audit V2 SHA256 `246ad2ab94a964fb31cb3befe0ded55d62b9e751101de985bf16679a5f1a4155` passed; HKP3 V4 additively repairs S3 role-correlated wording and retains older drafts. The sealed Phase1 manifest SHA256 is `c0e5c428839b7968b976792100115aeba739a92b885df0f1e521596a7670bf21`. Two 90-row, candidate-only packages are prepared with opaque IDs and separate cross-group orders. [Release record](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE1_MEGAWAVE_RELEASE_RECORD_V1.md); [exact R3/R4 file checklist](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_REMAINING90_PHASE1_REVIEWER_FILE_CHECKLIST_V1.md). `D1_REMAINING90_PHASE1_READY / STOP_EXTERNAL_REVIEW_REQUIRED`; no R3/R4 MegaWave return has been received. R3 must start a fresh independent GPT session; R4 a fresh **projectless** empty-directory Codex task, with no HKP1 exception. Phase2, Human A/B, GT, split and training are withheld. The former remaining90-construction-authorized section below is a dated snapshot.

## Current — 2026-09-27 D1 HKP1 Batch-1 accepted; remaining90 internal construction authorized

Both V4 Phase2 originals were byte-locked and validated 30/30, SHA R3 `65bec342aabd38b936694299f6c97330951fd24154beea5e22f648609361cdf0`, R4 `561737885f0801441c0a69cbac61cbdf2388a023b19cc2bdd2b20ad44946e7eb`. Seven of eight categorical fields agree 30/30; version agrees 24/30. The six date/distinct-document comparisons are resolved by Owner's additive [V4.3 rule and overlay](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE2_ACCEPTANCE_RECORD_V1.md), not by rewriting raw or privileging R3. Both reviewers report `SUFFICIENT/NO/NONE` on all 30 Evidence/secondary-error/issue gates. Construction checks and post-lock target comparison pass, so `D1_HKP1_BATCH1_ACCEPTED_FOR_D1_CONSTRUCTION_ONLY`. Owner `PODR-118 / OR-074` supersedes the *review routing* of the old sequential-batch plan: HKP2→HKP3→HKP4 internal Evidence-first QA, then one 90-candidate R3/R4 external MegaWave if all gates pass. Any internal hard blocker stops. Future R4 must be a fresh projectless empty-directory task; the Batch-1 new-Project exception does not transfer. `HUMAN_AB_NOT_AUTHORIZED / GT_NOT_CREATED / SPLIT_NOT_EXECUTED / TRAINING_NOT_STARTED`. The Phase2-pending entry below is a historical snapshot.

## Current — 2026-09-26 D1 HKP1 Batch-1 Phase1 passed with a one-run R4 exception; Phase2 packet ready

The initial R3/R4 returns and R3's inherited Canary/Phase2-session incident remain historical process evidence. Fresh R3/R4 V4 Phase1 originals were byte-locked read-only and each passed strict UTF-8 JSON, 30/30 IDs/order/keys/enums. Their five categorical fields agree 30/30; three notes differ only in wording. Owner attested content isolation. R4 ran in a **new Codex Project**, not the frozen `projectless` mode; read-only inspection found its current directory contained only the matching 7,907-byte return JSON, no hidden file or `.git`. Platform history remains unverified. Owner explicitly approved a **one-run-only bounded equivalence exception** for this R4 Batch-1 Phase1; future batches still require projectless R4. [Run02 gate](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_HKP1_BATCH1_FRESH_PHASE1_LOCK_AND_R4_ENVIRONMENT_GATE_V2.md), [Phase2 release record](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE2_RELEASE_RECORD_V1.md), and [exact reviewer file checklist](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_HKP1_BATCH1_REVIEWER_FILE_CHECKLIST_V1.md). The 30-row/14-source Phase2 packet is ready **for Owner distribution to the same two sessions**, not yet reviewed. `PHASE1_PRIMARY_PAIR_PASS_WITH_BOUNDED_R4_EXCEPTION / PHASE2_PACKET_READY / STOP_EXTERNAL_REVIEW_REQUIRED / BATCH1_NOT_ACCEPTED / HKP2_NOT_STARTED`. No Human A/B, GT, split, training or formal result. The preblind paragraph below is a dated historical snapshot.

## Current — 2026-09-26 D1 remaining40 / HKP1 Batch-1 preblind gate

Owner has separately approved `P1-FORMAL240-D1-REMAINING40-CONSTRUCTION-01` (`PODR-116`). The first frozen HKP1 batch (10 groups/30 candidates; target S 3/3/4) has completed evidence-first construction and bounded local preblind QA. Private authoritative cohort is V4 after additive effective-date metadata, four-S3-HN surface repairs, and one S1-HN factual-scope repair; V1–V3 remain preserved and were not distributed. Seventeen official snapshots were hash-checked. [Batch-1 status and V4 distribution paths](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_HKP1_BATCH1_PREBLIND_STATUS_V1.md). `STOP_EXTERNAL_REVIEW_REQUIRED / R3_R4_PHASE1_RAW_PENDING / PHASE2_WITHHELD / BATCH1_NOT_ACCEPTED / HKP2_NOT_STARTED`. Owner's next action is to send **only V4 Phase1** package/schema/prompt separately to R3-gpt and R4-codex, then return their original 30-row files for byte lock and QA. Reviewer isolation is not yet attested for this new batch. Human A/B, GT, split, training and formal results remain prohibited. The earlier Canary-only approval gate below is historical.

## Current — 2026-09-26 Formal240 D1 Canary accepted for construction planning

Owner's conditional decision `PODR-115 / OR-071` became effective after the [final bounded audit](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_FINAL_OWNER_ACCEPTANCE_AUDIT_V1.md) found all specified hard gates PASS: 8 frozen groups/24 V3 candidates, Phase1 and Phase2 24/24 resolved, Evidence sufficiency/secondary-error/issue 24/24 PASS, controlled Poison and supported Clean/HN, derived S 8/8, Entity-Claim 24/24, HKP3 temporal 2/2, HKP4 provenance 2/2, neutral retrieval smoke 8/8. `D1_CANARY_ACCEPTED_FOR_FULL_WAVE_CONSTRUCTION=TRUE / FORMAL240_CANARY_WORKFLOW_VALIDATED`. This accepts only the Canary workflow and eligibility to request the **next Owner approval** for remaining40 construction; the next task has **not** started. `D1_REMAINING40_OWNER_APPROVAL_REQUIRED / HUMAN_AB_NOT_AUTHORIZED / GT_NOT_CREATED / SPLIT_NOT_EXECUTED / TRAINING_NOT_STARTED / NO_FORMAL_RESULT`. Private Run02 acceptance matrix SHA256 `9847bdc5ae4b053846007a496ca779ef35a47e99a6e1db2c073e86b65afb07ee`; preliminary Run01 is preserved but superseded for a page-publisher metadata misclassification. R3/R4 isolation remains Owner-attested. Existing unrelated design-spec edit remains untouched. Older pending-gate paragraphs below are dated historical snapshots.

Post-commit audit detail: [additive V2 factual-atom supplement](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_FACT_ATOM_V2_SUPPLEMENT_RECORD.md) expands the same 24 frozen candidates into 48 explicit assertion checks; private Run03 SHA256 `f00d10874fa581d0430b7e104f1dd6bd21c38f12f4682209029b02888762a182`. This corrects V1 audit **granularity**, not raw data, Owner decision or approval scope.

本文是**唯一动态任务状态入口**，只回答当前正在执行什么、当前批准了什么、哪些工作必须停止。Git 仍动态决定
branch、HEAD、tag、working tree 和 upstream；权威层级见 [Context Authority Map](context_authority_map.md)。

## Repository Facts

- Active branch: `research/stage6-1-hidden-poisoning`.
- Branch base: accepted S6-T5 baseline `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`.
- Baseline tag `s6-t5-rag-baseline-v1`: recovered as an annotated tag and verified locally/remotely on `2026-07-31` to
  peel strictly to `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`. Future existence and target remain dynamic Git facts.
- Worktree, HEAD, working-tree state and upstream synchronization are dynamic Git facts. Verify them with `git rev-parse`, `git status --short` and `git rev-list --left-right --count @{upstream}...HEAD` before every task.
- Historical Stage 1-5 assets and Stage 6 fixture data remain immutable. Corrections are additive records, never rewrites of evidence.
- Experiment route, historical runs, metrics and evidence indexes are recorded in `docs/governance/experiment_master_record.md`; this file remains the sole dynamic task and approval-gate source.
- Chronological project execution is append-only in [Research Execution Log](research_execution_log.md); it does not replace this current-state page.

## Current Task

- **Current as of 2026-09-26 (supersedes targeted-package-ready snapshot):** Original isolated R3-gpt/R4-codex sessions returned the Formal D1 Canary V4.2 15-item targeted rule confirmation. Owner attested same sessions, equal materials, no mutual answer or Owner-overlay access (`OWNER_ATTESTED`, not machine-proven). Each source was copied byte-for-byte to read-only `E:\LLMGuard-Handoff\paper1_formal240_d1_canary_v4_2_targeted_raw_lock_20260926`; strict JSON/schema/ID/order/enum/reason QA passes 15/15 each. Both targeted values agree 15/15 and match the Owner overlay 15/15. [Bounded report](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_V4_2_TARGETED_RULE_STABILITY_REPORT_V1.md) and [machine comparison](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_V4_2_TARGETED_R3_R4_VALIDATION_V1.json) retain lineage. `VERSION_SCOPE_RULE_STABILITY_PASS / CANARY_OWNER_ACCEPTANCE_PENDING / HUMAN_AB_NOT_AUTHORIZED / Auto Continue=NO`. Next: Owner separately reviews the complete Canary quality/evidence/blind-review record and decides accept or repair. No remaining40, Human A/B package, split, GT, training or formal result. Unrelated dirty design spec excluded.

- **Current as of 2026-09-26 (supersedes the unresolved interpretation gate below):** Owner `PODR-114 / OR-070` froze Formal annotation V4.2 for candidate-only version-claim presence, explicit amendment-decision identity, and supported original-versus-revised comparisons. The 15 R3/R4 Phase2 differences were individually checked against frozen candidate text and E1/E2, then recorded in an additive [Owner-semantic overlay](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_PHASE2_OWNER_SEMANTIC_ADJUDICATION_OVERLAY_V1.json) (12 bare substantive, one amendment decision, two historical comparisons). No raw reviewer value, Candidate, Evidence, V4/V4.1 or enum changed. The [15-row targeted package](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_PHASE2_15ITEM_TARGETED_REREVIEW_PACKAGE_V1.json) and symmetric original-session R3/R4 prompts are ready, **not yet distributed**. This is rule confirmation, not fresh independent annotation or GT. `FORMAL_V4_2_VERSION_SCOPE_FROZEN / 15_DISAGREEMENTS_RULE_ADJUDICATED / TARGETED_R3_R4_REREVIEW_READY / CANARY_ACCEPTANCE_PENDING / HUMAN_AB_NOT_AUTHORIZED`. Next: Owner sends V4/V4.1/V4.2 plus the same package separately to original R3/R4 sessions, obtains actual 15-row JSON files, then raw lock/QA; 15/15 agreement and no blocking defect are needed before separate Canary decision. R5 optional; no remaining40, split or training. Existing unrelated design-spec edit excluded.

- **Current as of 2026-09-26 (supersedes the Phase2-not-executed snapshot):** Task `P1-FORMAL240-D1-CANARY-R3R4-PHASE2-RAW-LOCK-AND-DISAGREEMENT-TRIAGE-01`. R3-gpt initial 17,199-byte transport is preserved but was not valid JSON; its 18,396-byte valid re-export and R4-codex 17,607-byte original are separately byte-locked in Git-external `paper1_formal240_d1_canary_phase2_r3r4_raw_lock_20260926`. R3 re-export has identical ID/categorical decisions and, after excluding UI citation markers, identical 24 reason bodies to the initial transport. Both structured returns pass 24/24 packet ID/order/exact schema/enums/reason and internal-conflict/ZERO checks. Owner directly attested original isolated sessions and frozen-E1/E2-only scope; this is not machine-verified. `overall_fact_status` agrees 22/24; `version_claim_status` 11/24; other six categorical fields each 24/24. Fifteen field decisions remain unresolved. [Decision-ready blocker](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE2_RAW_LOCK_AND_DISAGREEMENT_BLOCKER_V1.md) and [machine comparison](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE2_COMPARISON_V1.json) retain both values. `D1-CANARY-PHASE2-VERSION-SCOPE-BLOCKER-01 / HUMAN_DECISION_REQUIRED / Auto Continue=NO / CANARY_OWNER_ACCEPTANCE=PENDING / HUMAN_AB=NOT_AUTHORIZED`. R5 remains non-gating. Await Owner explicit interpretation/adjudication path; do not generate remaining40, split or train. Existing unrelated design-spec edit remains untouched.

- **Current as of 2026-09-26 (supersedes the targeted-review-pending snapshot):** Task `P1-FORMAL240-D1-CANARY-PHASE1-FINAL-CLOSEOUT-AND-PHASE2-RELEASE-PREP-01`, Owner `PODR-113 / OR-069`. R3-gpt and R4-codex targeted Phase1 JSON arrays were byte-sliced from the Owner composite attachment and locked independently; both pass 2/2 exact ID/order/schema/enum and five-field agreement 2/2. Candidate V3's two-item naturalness repair is accepted; the designed internal conflict remains. Candidate V3 SHA `6210a6de8f519fb4a58334ff531954b67e774375d021d099dea050f8fe47032e`; existing Phase2 V4 SHA `2daf08286581cb8d28e70ab95ea844e5cdf41e2a6916980bf41b0a90a548ac38` is promoted without overwrite after 24/24 Evidence parity and bounded mechanical re-QA. [Closeout](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_PHASE1_FINAL_CLOSEOUT_V1.md). `PRIMARY_GATING_PAIR=R3-gpt+R4-codex / PHASE1_PRIMARY_QA_ACCEPTED / PHASE2_RELEASE_AUTHORIZED=TRUE / PHASE2_NOT_EXECUTED`. R5-claude is optional/non-gating; Owner later supplied actual 24-row and 2-row files, both byte-locked and validated in the same new namespace. Its naturalness disagreement is auxiliary and does not override the primary gate. Next: Owner sends V4 packet/schema/Guide V4+V4.1 and separate prompts to the **same** R3/R4 sessions, then submits both Phase2 raw returns. Canary Owner acceptance, Human A/B, remaining40, split and training remain unauthorized. Existing unrelated design-spec edit remains untouched.

- **Current as of 2026-09-23 (superseding the R3/R4-not-started snapshot below):** Task `P1-FORMAL240-D1-CANARY-R3R4-PHASE1-LOCK-AND-TARGETED-NATURALNESS-REPAIR-01`, Owner `PODR-112 / OR-068`. Owner corrected attachment attribution: attachment 1 is `R4-codex`, attachment 2 is `R3-gpt`; both raw JSON files are byte-locked in Git-external `paper1_formal240_d1_canary_r3r4_phase1_raw_lock_20260923`, each 24/24 exact ID/order/keys/enums. Five categorical fields agree 24/24; two replicated `MINOR_ISSUE` rows prompted an exact single-phrase V3 repair with two new opaque IDs. The other 22 candidates and frozen Evidence are unchanged. Owner directly attested fresh isolated sessions and no external search, but no session URL/system access log was supplied: `INDEPENDENCE_EVIDENCE=OWNER_ATTESTED_NOT_MACHINE_VERIFIED`. The two-row targeted Phase1 package is ready; Phase2 V4 is prebuilt/hash-locked but withheld. [Record](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE1_LOCK_AND_TARGETED_REPAIR_RECORD_V1.md). `R3_GPT_PHASE1_LOCKED / R4_CODEX_PHASE1_LOCKED / PHASE1_STRUCTURED_AGREEMENT_COMPLETE / TARGETED_NATURALNESS_REPAIR_PREPARED / WAITING_FOR_R3_R4_TARGETED_REVIEW / PHASE2_RELEASE_AUTHORIZED=FALSE / CANARY_ACCEPTANCE=PENDING / NO_HUMAN_AB`. Next gate: both original reviewer sessions return and separately lock the two repaired candidates' targeted Phase1 results; only on pass can V3 be accepted and V4 release considered. No remaining40, split, training or formal result.

- **Current as of 2026-09-23 (superseding only fresh-reviewer naming and release procedure):** Owner has renamed the future isolated pair to `R3-gpt` + `R4-codex` (`PODR-111 / OR-067`). The [additive V2 plan](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_R3_GPT_R4_CODEX_REVIEW_PLAN_V2.md) and phase prompts are ready; **neither fresh session has started or been attested**. R4-codex must be a new projectless Codex task in an empty isolated directory, not this control-plane/construction session or a fork, with no repository/handoff/context access; an instruction alone is not proof. Both reviewers receive information-equivalent phase files. `PHASE2_RELEASE_AUTHORIZED=FALSE` until **both** new Phase1 raw returns are byte-locked, 24/24 validated and independently attested. Future run-level attestation is separate from candidate JSON. `R3_GPT_REVIEW_SLOT_READY / R4_CODEX_REVIEW_SLOT_READY / FRESH_SESSION_ISOLATION_REQUIRED / WAITING_FOR_R3_GPT_AND_R4_CODEX_PHASE1`. R1/R2 raw and V4/V4.1 remain immutable; Canary acceptance, Human A/B, remaining40, formal split and training are not authorized.

- **Current as of 2026-09-23 (superseding the prior Phase2-release gate):** Owner supplied one composite attachment containing current Phase2 R1/R2 JSON. The whole attachment and two verbatim JSON byte slices are locked in Git-external `paper1_formal240_d1_canary_phase2_preclarification_20260923`; both slices pass 24/24 exact ID/order/schema/enum checks. R1 raw explicitly reports that its session's Phase1 role was R2, so `CURRENT_R1_PHASE2_INDEPENDENCE_VALID=FALSE`. This is a **review-run** incident, not a candidate `phase2_issue`; R1 raw's `OTHER` and note remain untouched. R1/R2 differences are diagnostic-only, never valid independent agreement. [Incident](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_BLIND_REVIEW_PROCESS_INCIDENT_V1.md).
- **Next gate:** Additive [Formal V4.1 field clarification](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md) and [fresh R3/R4 plan](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_R3_R4_REVIEW_PLAN_V1.md) are ready. Owner/coordinator must use two new isolated sessions, lock each Phase1 V2 raw before releasing that session's Phase2 V3 + V4.1, then lock both Phase2 raw and resolve blocking discrepancies. `CANARY_ACCEPTANCE=PENDING / HUMAN_AB=PROHIBITED / D1_REMAINING40=NOT_GENERATED / FORMAL_SPLIT_AND_TRAINING=NOT_STARTED`. The previous Phase1 raw locks remain historical evidence; they do not establish a valid cross-phase R1 chain.

- **Current as of 2026-09-23 (superseding the earlier “R1/R2 pending” snapshot):** Owner supplied two independently produced external GPT Phase1 returns for the D1 Canary and authorized `P1-FORMAL240-D1-CANARY-BLIND-PHASE1-RAW-LOCK-01` (`PODR-109 / OR-065`). Both byte-identical raw copies are locked in Git-external `paper1_formal240_d1_canary_phase1_raw_lock_20260923`; R1/R2 each pass 24/24 exact ID/order/schema/enum validation. All five categorical fields agree 24/24, with zero disagreement IDs. The two nonempty note pairs differ in wording but describe the same internal conflicts. [Lock record](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_BLIND_PHASE1_RAW_LOCK_RECORD_V1.md).
- **Gate / next action:** `PHASE1_R1_LOCKED=TRUE / PHASE1_R2_LOCKED=TRUE / PHASE1_DOUBLE_BLIND_LOCK_COMPLETE=TRUE / PHASE2_RELEASE_AUTHORIZED=TRUE / PHASE2_NOT_DISTRIBUTED_BY_THIS_TASK`. Independence is Owner-attested, not proven by JSON equality. The next separately executed step is Phase2 V3 distribution to the same isolated R1/R2, then raw return lock/QA. Canary Owner acceptance, Human A/B, remaining D1 40 groups, Formal240 split, Detector training and paper results remain pending/not started. The unrelated existing Stage6 design-spec edit is untouched.

- **Current as of 2026-09-23 (superseding the former D1-approval gate):** Owner approved `P1-FORMAL240-D1-EVIDENCE-FIRST-CANARY-AND-PREANNOTATION-QA-01` as an 8-group/24-candidate construction Canary, with external independent blind GPT QA before any Human A/B release (`PODR-108 / OR-064`). Eight selected slots are real frozen D1 matrix slots; 14 official raw webpage snapshots pass hash checks. A prior V0 wording draft predates the full per-signal preflight and remains scratch-only; the post-preflight candidate V2 and phase-separated blind packages are private, additive construction artifacts. Mechanical QA passed its bounded checks but cannot certify full factual/naturalness/annotation determinacy.
- **Current status / next gate:** `D1_CANARY_CONSTRUCTION_V2_AND_MECHANICAL_QA_READY / EXTERNAL_BLIND_REVIEW_PENDING / OWNER_CANARY_ACCEPTANCE_PENDING / NO_HUMAN_AB`. Owner/coordinator must independently lock R1 and R2 Phase1 returns before releasing Phase2; review flags require versioned repair and full re-review. Canary is **not accepted**, remaining D1 40 groups and Human A/B packets do not exist, Formal240 split/Detector training/formal result remain `NOT_STARTED`. Private evidence namespace `paper1_formal240_d1_canary_20260922`; [full-wave plan](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_FULL_WAVE_CONSTRUCTION_PLAN_V1.md). The unrelated pre-existing Stage6 design-spec edit remains untouched and outside task staging.

- **Current as of 2026-09-22 (superseding previous next-gate text):** Owner approved `P1-FORMAL240-ANNOTATION-SCHEMA-V4-AND-CONSTRUCTION-PROTOCOL-FREEZE-01`. Additive Formal V4, 240 **unfilled** factorial group slots, construction/evidence/metadata/annotation/split design contracts are frozen under [Formal240 protocol](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_240_GROUP_BENCHMARK_CONSTRUCTION_PROTOCOL_V1.md). `FINAL72_DEVELOPMENT_PHASE_CLOSED=TRUE` moves construction priority; Final72 remains exposed engineering evidence, not an untouched test or formal result. Pilot4/Final72 history remains immutable.
- **Current status / next gate:** `FORMAL_ANNOTATION_SCHEMA_V4_FROZEN / FORMAL_240_GROUP_PROTOCOL_FROZEN / FORMAL_240_GROUP_MATRIX_FROZEN / WAITING_FOR_OWNER_WAVE_D1_APPROVAL`. Matrix: 240 design slots, 0 formal candidates, 0 annotations, 0 split assignments. Seed `20260922` is algorithm-only. Owner must separately approve D1 enterprise-HR Wave (48 groups/144 candidates). No automatic D1, other waves, formal GT/dataset freeze, split execution, detector training, risk calibration, Stage B or Paper Result; `FORMAL_EXPERIMENT=NOT_STARTED`. The pre-existing unrelated Stage6 design.md edit remains outside this task.

- **Current as of 2026-09-22 (superseding the below blocker snapshot):** Owner approved `A_FIRST_THEN_B_IF_NEEDED` for `P1-FDD-FAILURE-ANALYSIS-EVIDENCE-BLOCKER-01`. Bounded original-artifact search found no attributable eight-model OOF; one-time exact evidence reconstruction then passed canonical Full 72-row OOF and all nine machine-summary identity gates under original input/script/environment/fold configuration. The original run remains immutable. Post-lock 21-feature, matched group, T/P, hard-group, HKP/S/domain and scale-hypothesis analysis is complete as **development-only** evidence. See [reconstruction record](../research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_DETECTOR_V1_1_EVIDENCE_RECONSTRUCTION_RECORD_V1.md) and [analysis](../research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_FINAL72_DOCUMENT_DETECTOR_FAILURE_ANALYSIS_REPORT_V1.md).
- **Status / next gate:** `EXACT_EVIDENCE_RECONSTRUCTION_PASS / FAILURE_ANALYSIS_COMPLETE / MULTIVIEW_SIGNAL_MIXED / FORMAL_EXPERIMENT_NOT_STARTED`. Recommended next priority is formal 240-group benchmark **construction planning**, subject to separate Owner approval. No Final72 re-tuning, formal sample generation, Detector training, calibration, Stage B model or paper superiority claim is authorized. The earlier `HUMAN_DECISION_REQUIRED` below is historical and resolved by this Owner decision.

- **Current as of 2026-09-22**: `P1-DOCUMENT-DETECTOR-FAILURE-ANALYSIS-AND-SCALE-HYPOTHESIS-REFINEMENT-01` is `HUMAN_DECISION_REQUIRED / Auto Continue=NO`. The Owner approved frozen-result diagnosis, but preflight found the original hash-locked run persisted sample-level OOF only for Full SEPT; eight view/ablation models have aggregate metrics but no per-sample scores. Therefore the required 24-group Full-vs-Full-T/P score shifts and view-specific failure analysis are not evaluable under the explicit no-retraining rule. [Decision-ready blocker](../research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_DOCUMENT_DETECTOR_FAILURE_ANALYSIS_EVIDENCE_BLOCKER_01.md): `P1-FDD-FAILURE-ANALYSIS-EVIDENCE-BLOCKER-01`.
- **Next gate**: Owner must choose authentic existing OOF artifact, separately authorized additive exact-run reconstruction, or an explicitly reduced-scope partial analysis. Until then, no model fit, no fabricated group shift, no formal hypotheses acceptance, and no claim that this task is complete. Frozen prototype remains `MULTIVIEW_SIGNAL_MIXED / PROTOTYPE_VALID_WITH_LIMITATIONS`; formal experiment remains not started.

## Completed 2026-09-22 detector prototype snapshot (superseded as current)

- **Current as of 2026-09-22**: `P1-FIRST-DOCUMENT-DETECTOR-V1_1-LOGO-PROTOTYPE-EXECUTION-01` completed the first **development-only** non-Oracle Document Detector fit under Owner approval `PODR-104`. Frozen V1.1 GT/Feature Set/Matrix identities passed; 9 fixed LR models each produced 72/72 OOF predictions under 24 complete-group LOGO folds. Full SEPT AUROC `.6471`, AUPRC `.4964`, Poison>HN `18/24`, HN-FPR@0.5 `8/24`; development finding `MULTIVIEW_SIGNAL_MIXED / PROTOTYPE_VALID_WITH_LIMITATIONS`. See the [human report](../research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_FINAL72_DOCUMENT_DETECTOR_PROTOTYPE_REPORT_V1_1.md) and Git-external hash-locked run `paper1_final72_document_detector_v1_1_logo_20260922`.
- **Next gate**: Owner review and separate approval for failure analysis/scale-hypothesis refinement. No Final72-tuned feature or threshold repair, risk calibration, Stage B, 240-group formal result, untouched-test claim or superiority claim is authorized. `FORMAL_EXPERIMENT=NOT_STARTED`.
- **Git note**: the unrelated pre-existing edit to the Stage 6 trustworthy-retrieval design file remains outside this task; resolve ownership separately. Branch/HEAD/upstream remain dynamic Git facts.

## Completed 2026-09-22 input-resolution snapshot (superseded as current)

- **Current as of 2026-09-22**: `P1-DOCUMENT-DETECTOR-MISSINGNESS-CONTRACT-OWNER-RESOLUTION-01` has completed the Owner-approved A→conditional-C missingness resolution. Option A did not produce a lawful candidate-level relation; Option B was explicitly rejected; additive Option C freezes Feature Set V1.1 and Matrix V1.1 at 72×21 (S3/E9/P6/T3).
- **Gate**: `PHASE_A_PREFLIGHT_PASS / READY_TO_EXECUTE_FIRST_DETECTOR_PROTOTYPE / TRAINING_STARTED_FALSE`. All 24 LOGO training folds have a legal train-only statistic for every retained feature. This is input readiness, not a model, OOF prediction, formal result or automatic execution authority.
- **Evidence**: `E:\LLMGuard-Handoff\paper1_document_detector_missingness_owner_resolution_20260922`; matrix SHA256 `2d418ae2fd6d22f848fcf812a6126fd68ff9b7b880c389a2ca510a5c94dd5b2d`. The original 23-feature artifacts and the 2026-09-21 blocker remain immutable history.
- **Next gate**: separately execute the first Final72 development-only LOGO Detector prototype using exactly V1.1, after a fresh execution preflight. No model fit, threshold tuning, calibration, Stage B or formal benchmark has occurred in this task.

## Historical 2026-09-16 task snapshot (superseded as current)

- Task ID: `P1-RETRIEVAL-BEHAVIOR-HARNESS-AND-DEPLOYABLE-SIGNAL-BOUNDARY-01`.
- Task name: `Paper 1 Retrieval-Behavior Harness, Two-stage Risk Boundary and Deployable Signal Audit`.
- Task type: **OWNER-APPROVED LABEL-BLIND RETRIEVAL HARNESS / THREAT-MODEL AUDIT / TEMPORAL INPUT-GAP AUDIT**.
- Engineering status: **24 QUERY LOCK / 72-DOCUMENT CORPUS LOCK / SPARSE+DENSE DOUBLE TRACE / 8448-ROW R MATRIX LOCK /
  42-SIGNAL DEPLOYABILITY AUDIT / DOCUMENTATION CLOSEOUT**.
- Experiment status: **RETRIEVAL_HARNESS_COMPLETE / TWO_STAGE_RISK_BOUNDARY_FROZEN / DOCUMENT_DETECTOR_NOT_READY /
  RETRIEVAL_RISK_READY_WITH_LIMITATIONS / NO_DETECTOR_TRAINING / NO_FORMAL_RESULT / AUTO_CONTINUE_NO**.
- Documentation gate: **PAPER1_MANDATORY_DOCUMENTATION_CLOSEOUT = OWNER_CONFIRMED / HUMAN_LEDGER_CONTINUOUS_SYNC =
  MANDATORY / TASK_DOCUMENTATION_CLOSEOUT = MANDATORY**. Paper 1 task completion requires execution, tests, evidence,
  documentation closeout and valid Git status; otherwise status is `ENGINEERING_COMPLETED / DOCUMENTATION_CLOSEOUT_PENDING` with
  `TASK_DOCUMENTATION_CLOSEOUT_BLOCKER`.
- Execution base commit: `e46639518aaf58eb9590790917a235e96447898c`.
- Candidate source identity: `candidates_v3_1_additive.jsonl` SHA256
  `15500aa75bced9fb470edaac98f9527e7bb4bc689b86583e6f69b892c48eb210`; final additive corpus SHA256
  `f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d`.
- Execution machine: **本机**. Frozen MiniLM ran CPU/local-only; no download、GPU workload、5090 contact、Detector training、240-group
  generation、formal Dataset or formal experiment occurred.
- Current ordered step: STOP after harness closeout. The next recommended but separately gated task is
  `P1-TRUSTED-EVIDENCE-RETRIEVER-AND-VERSION-REGISTRY-PROTOTYPE-01`; Detector training is not automatically authorized.
- Current blocker: **DOCUMENT DETECTOR INPUT THREAT MODEL NOT CLOSED**. Twenty-nine S/E/P/T signals still depend on oracle-matched
  E1/E2. Seven R signals require a Trusted Version Registry; they remain input-missing rather than using GT/HN roles.
- Current evidence: Git-external namespace `paper1_retrieval_behavior_harness_20260915`. Query/corpus locks are
  `d101d2d4...6f1f` / `0194e1d3...446b`. Sparse and Dense each have two full 1728-row traces. The 8448-row R matrix SHA256 is
  `eeebe7ea92857b0b04dbfb983497b0e28b72f785f507f1acd046cd3cedc6fdef`; 7104 rows compute rank/score/stability and 1344 rows remain
  input-missing for seven version-aware signal types. Query/corpus leakage is zero; locks precede first label load.
- Owner acceptance: `PILOT4_ANNOTATION_PROTOCOL_ACCEPTED=TRUE / ACCEPTED_WITH_NONBLOCKING_NOTES`；all frozen A–F gates passed；
  the two nonblocking reviewer variances remain immutable and do not trigger R4.
- Accepted stack: `PILOT4_ACCEPTED_ANNOTATION_STACK_V1` points to the existing Final72 corpus、Attempt2 final Phase1 protocol/raw、
  Guide V3.2、Expected V3、Evidence Pool V2 and `FROZEN_OFFICIAL_SNAPSHOT_PLUS_URL_PROVENANCE`; it creates no rewritten accepted content.
- A/B execution: Owner named two different independent humans, `HUMAN-A01` and `HUMAN-B01`, and froze complete isolation plus
  `NO_LLM_ASSISTANCE`. The original V1 packages remain immutable/not distributed and are now superseded for distribution because
  their human-facing explanations were insufficient. Additive V2 keeps all 72 candidates、opaque IDs、independent order and exact
  five-column CSV schema unchanged；Packet V2 is a three-column read-only question sheet, while CSV is the only answer sheet.
  Both Phase1 V2 returns are now complete and locked. The additive Phase2 V3.2 workbooks keep Candidate visible beside E1/E2 titles
  and full official URLs plus seven highlighted inputs, retain 144/144 frozen Evidence snapshots as backup, remove sheet protection,
  and preserve canonical English enum dropdowns. Guide V4 adds explanation only. All four raw locks still precede mapping/Expected comparison.
  Git-external V1 namespace remains `paper1_pilot4_ab_execution_20260903` with manifest SHA256
  `aa8742baccab4072a0fe901bcd430b46011cea9b436738a730164f166f0d7d91`；V2 is additive under
  `paper1_pilot4_ab_usability_repair_20260903`; the current additive release namespace is
  `paper1_pilot4_dual_phase1_phase2_v3_20260908`; V3 is immutable but superseded for distribution by
  `paper1_pilot4_phase2_usability_repair_20260909`.
- R3 raw facts: `12062 bytes`；SHA256 `80a10a1ebf2e2321198c750e92214b8d26f9b2a8f4161c64ebf38cae830b4441`；
  exact 8 columns；37 rows / 37 unique opaque IDs；enum、reason and internal consistency PASS；raw-lock-before-Expected PASS；
  mapping parity `37/37`；affected/control `21/16`.
- Expected V3 facts: reviewer-blind independent justification PASS；Expected V3 SHA256
  `dc549ff6adbacc6a87049c08c7db7e414b9d52dafc19c31f98b5c10490031433`；exact row diff `7 fields / 6 candidates`；
  candidate/reviewer changes `0`；Expected V1/V2、Guide、Evidence、mapping and prior comparison/acceptance artifacts unchanged.
- R3 V3 comparison facts: overall `35/37`；version `37/37`；authority `37/37`；minimum evidence `37/37`；issue `37/37`；
  exact relevant fields `35/37`. M2 residual `2/16`；same-root cluster `2`；controls overall/exact `16/16`；M4/BR18 PASS；
  M8 `4/4` PASS；gates A–F all PASS. Residual taxonomy contains only two non-systemic `R3-M1 REVIEWER_VARIANCE`；
  Expected V3 defect `0`；Evidence defect `0`；Guide systemic blocker `0`.
- Calibration decision: `PILOT4_PREANNOTATION_CALIBRATION=CLOSED / PILOT4_CALIBRATION_STOP_CONDITION_MET=TRUE /
  R4_EXTERNAL_REVIEW_REQUIRED=FALSE`. R1/R2 remain historical calibration evidence；R3 is final targeted validation evidence.
- Pilot4 lesson status: thirteen evidence-supported protocol lessons are individually promoted to
  `ACCEPTED_PILOT4_PROTOCOL_LESSON`; claims requiring actual A/B、Ground Truth、Dataset freeze or scale evidence remain provisional.
- Combined-packet correction: the `5d6b4b5` combined packet is preserved unchanged as
  `COMBINED_PACKET_ENGINEERING_ARTIFACT / NOT_APPROVED_FOR_BLIND_SEMANTIC_REVIEW` and
  `SUPERSEDED_FOR_REVIEW_BY_PHASE_SEPARATED_PROTOCOL`. Evidence being present in one LLM context breaks strict Phase1 blindness;
  a behavioral “do not read yet” instruction is not structural separation.
- Attempt2 final comparison facts: first Phase2 raw SHA256 `d7aed1b2...f6cd` remains immutable process evidence；final Phase2 raw is
  `16321 bytes` / SHA256 `6f6cc042...92f1` and supersedes it for analysis. Raw lock preceded mapping/expected load；mapping and final
  corpus parity are 72/72；Phase1 exact is 58/72 and Phase2 exact is 48/72. This comparison authorization is consumed and does not
  authorize protocol acceptance or A/B.
- Attempt1 history: raw bytes `5001`, SHA256 `59446c4be65b035be29528de81b6b8f8aa4113007df8fcac962fe4058a889261`；
  exact five-column schema、72/72 opaque IDs、enums and conditional reasons passed. Owner accepted all five blind-level issues and
  required local repair. Attempt1 remains `VALID_DEFECT_DISCOVERY_REVIEW / NOT_FINAL_CORPUS_ACCEPTANCE_REVIEW` and all files are
  immutable.
- Repair/Attempt2 facts: controlled Attempt1 mapping output `5/5` with 0 unauthorized rows；semantic and source parity `5/5`；67
  unaffected candidate texts and source lines byte-identical；final additive corpus 72；Attempt2 raw SHA256
  `1e5e81fee3825071a77d520c6da5cbfc4c2b59125aca0499cda6c7e2f363c9c5`；exact schema/72 IDs/enums/7 reasons PASS；
  `phase1_issue=NONE` is 72/72. Attempt2 Phase2 has 72 rows / 144 distinct slots and is released as an unfilled packet only.
- Historical correction: the `c1b1245` Full72 result is
  `SAMPLE_ID_LABEL_LOOKUP_CONTAMINATED_REVIEW / NOT_ACCEPTABLE_AS_EXTERNAL_LABEL_BLIND_EVIDENCE` because reviewer logic used
  `sample_id` to query compiled label sets. Its locked output, mismatch chain, final comparison and workbooks remain immutable.
- Historical completed task identity: `S6.1-P1-PILOT2-ADJUDICATION-CLOSURE-AND-PILOT3-ENTRY` closed Pilot2 feasibility and
  established the Pilot3 diagnostic baseline; the immutable closure history remains governed by `PODR-070 / OR-032`.
- Permanent prospective candidate gate (`PODR-067 / OR-029`): every annotation candidate created or newly introduced after
  `2026-08-28` must identify its legal/policy/institutional/standards subject unambiguously from the candidate text itself. Bare
  references such as “条例”、“规定”、“修订文本”、“2017年版” fail closed as `BROKEN_CANDIDATE / MISSING_CONTEXT` and must be
  rewritten or excluded before formal Benchmark admission. Frozen historical candidates and returns are preserved and are not
  retroactively rewritten, relabeled or reinterpreted by this rule.
- Historical superseded H2 snapshot: `PROPOSED / NOT CANONICAL / NOT APPROVED`; preserve as history.
- Formal RAG security experiment: **NOT STARTED**.
- Canonical formal status: `FORMAL_EXPERIMENT = NOT STARTED`.
- Git-Native Research Context Recovery Governance: **HUMAN_ACCEPTED**.
- PO-MHEP: **HUMAN_ACCEPTED / HIGHEST_INTERNAL_PROJECT_EXECUTION_AUTHORITY / PERMANENT / NO_AUTO_EXPIRY**.
- LOCAL role: **PRIMARY_CONTROL_PLANE / PROJECT_EXECUTION_LEAD / RESEARCH_GOVERNANCE_LEAD / 5090_APPROVAL_AUTHORITY /
  PAPER_RISK_REVIEWER / CONTEXT_PRESERVATION_OWNER**.
- RTX5090 role: **COMPUTE_WORKER / NO_SELF_APPROVAL_AUTHORITY**.
- Paper-First Comparative Evidence Principle: **HUMAN_ACCEPTED**.
- Paper 1 current research plan authority: [research_plan_authority.md](../research/stage6_1_hidden_knowledge_poisoning/human/research_plan_authority.md), **ACCEPTED_CURRENT_RESEARCH_PLAN**. The formerly canonical `paper1_research_route.md` remains historical/supporting and does not override it.
- RTX5090 Compute Worker Bootstrap: **HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY**.
- Historical superseded execution snapshot — S6.1-R0: **APPROVED_TO_START**.
- Historical first-review snapshot — S6.1-R0-I: **RETURNED_FOR_WORKER_CORRECTION**.
- Historical first-review parent snapshot — S6.1-R0: **REVIEW_PENDING_CORRECTED_WORKER_EVIDENCE**.
- Parent S6.1-R0: **HUMAN_ACCEPTED_WITH_BLOCKERS**.
- S6.1-R0-FU1: **HUMAN_ACCEPTED / CLOSED**.
- Historical P0 snapshot: **COMPLETED_PENDING_OWNER_REVIEW**.
- S6.1-R0-FU1-P0: **HUMAN_ACCEPTED**.
- S6.1-R0-FU1-L1: **HUMAN_ACCEPTED**.
- Historical S6.1-R0-FU1-W1 candidate: **SUPERSEDED_BY_LOCAL_L1 / NOT FAILED**.
- Historical S6.1-R0-FU1-W2 snapshot: **READY_FOR_OWNER_EXECUTION_APPROVAL / NOT_YET_EXECUTED**.
- S6.1-R0-FU1-W2: **HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED**.
- W2_ENGINEERING_OBJECTIVE: **SATISFIED**.
- W2_RUNTIME_GATE: **CLOSED**.
- W2_ACCEPTANCE_SCOPE: **FROZEN_SINGLE_SAMPLE_DETECTION_CORE_ENGINEERING_FEASIBILITY_ONLY**.
- S6.1-R0-FU1-W2-ATTEMPT1: **VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER**；`smoke_executed=false`；
  `algorithm_failure=false`；`GMTP_incompatibility=not established`.
- S6.1-R0-FU1-W2-ATTEMPT1-CORRECTION-01 gap: **RESOLVED_BY_CORRECTION_02**.
- S6.1-R0-FU1-W2-H1: **OFFLINE_MODEL_ARTIFACTS_VERIFIED_ON_5090 / COMPLETED**.
- S6.1-R0-FU1-W2-H2: **ENGINEERING_SMOKE_COMPLETED / CONTROL_PLANE_REVIEW_PASS / HUMAN_ACCEPTED_AS_W2_EVIDENCE**.
- S6.1-R0-FU1-W2-H2-RESUME-01: **VALID_BLOCKED_EVIDENCE / OFFLINE_BUNDLE_SHA_BLOCKER / H2-B NOT EXECUTED / call_count=0**.
- S6.1-R0-FU1-W2-H2-RESUME-02: **CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED / call_count=1**.
- S6.1-R0-FU1-W2-ATTEMPT1-CORRECTION-02: **CONTROL_PLANE_REVIEW_PASS / FINAL_CLOSURE_APPLIED** under
  `PODR-057` and `PODR-058`.
- S6.1-P1-R1: **HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK**.
- P1 numeric parameters: **PENDING_PILOT_EVIDENCE**；formal protocol: **NOT YET FROZEN**.
- S6.1-P1: **PILOT4_FINAL72_GT_ACCEPTED / PILOT4_GT_CONSTRUCTION_CLOSED /
  PAPER1_SIGNAL_DETECTION_ENGINEERING_STARTED / FINAL72_DEVELOPMENT_SET_ACTIVE /
  FORMAL_SCALE_BENCHMARK_PENDING / NO_FORMAL_DETECTOR_RESULT_YET /
  NOT FORMAL_EXPERIMENT**.
- S6.1-P1-PILOT0: **HUMAN_ACCEPTED / ENGINEERING_INFRASTRUCTURE_ONLY / CLOSED**.
- S6.1-P1-PILOT1: **HUMAN_ACCEPTED / REAL_PUBLIC_SOURCE_AND_PACKET_FEASIBILITY_ONLY / CLOSED**.
- Historical S6.1-P1-PILOT1: **COMPLETED_PENDING_REVIEW / REAL_PUBLIC_SOURCE_FEASIBILITY_ONLY**；superseded by OR-024.
- S6.1-P1-PILOT2: **HUMAN_ACCEPTED / ANNOTATION_PROTOCOL_AND_GROUND_TRUTH_FEASIBILITY_ONLY / CLOSED**.
- PILOT2_ROUND1_RAW: **PRESERVED_IMMUTABLE**.
- PILOT2_ROUND1: **PRESERVED_FOR_SCHEMA_V2_INDEPENDENT_REREVIEW**.
- A_PHASE1_STRICT_BLINDNESS: **OWNER_CONFIRMED_PRESERVED**.
- ANNOTATION_SCHEMA_V2: **IMPLEMENTED**.
- A_B_REREVIEW: **FOUR_TARGETED_RETURNS_RECEIVED / HASH_LOCKED / VALIDATED_FOR_AGREEMENT**.
- FORMAL_AGREEMENT_V2: **COMPLETED_ON_A_B_V2_CURRENT_VALUES**.
- OWNER_ADJUDICATION: **COMPLETION_PASS / OWNER_CORRECTION_BOUND_SEPARATELY / CONSISTENCY_PASS / NO_PENDING**.
- GROUND_TRUTH_CANDIDATE: **GENERATED / 36_RECORDS / PILOT_ONLY / NOT_FORMAL_DATASET**.
- PILOT3: **ENGINEERING_AND_SIGNAL_FEASIBILITY_ESTABLISHED / PILOT_DIAGNOSTIC_ONLY / STOPPED**.
- Historical PILOT4 first preflight: **OWNER_PREFLIGHT_RETURNED_FOR_TARGETED_REPAIR / a843697 EVIDENCE PRESERVED**.
- Historical PILOT4 second preflight: **SECOND_OWNER_PREFLIGHT_RETURNED_FOR_TARGETED_REPAIR / cad3b2b EVIDENCE PRESERVED**.
- PILOT4: **PILOT4_ANNOTATION_PROTOCOL_ACCEPTED / PILOT4_CALIBRATION_CLOSED /
  PILOT4_A_B_EXECUTION_COMPLETED / OWNER_ADJUDICATION_CLOSED /
  PILOT4_FINAL72_GT_ACCEPTED / ACCEPTED_WITH_KNOWN_EVIDENCE_LIMITATIONS /
  PILOT4_GT_CONSTRUCTION_CLOSED**.
- PILOT4 Final72: **PILOT4_FINAL72_GROUND_TRUTH_V1 / 72 RECORDS / 576 VALUES /
  DEVELOPMENT_AND_METHOD_ENGINEERING_SET / NOT_UNTOUCHED_FINAL_TEST / NOT_FORMAL_FROZEN_DATASET**.
- PAPER1_FORMAL_DOMAIN_SET: **OWNER_CONFIRMED / ENTERPRISE_HR / FINANCE / INFORMATION_SECURITY /
  PROCUREMENT_AND_R_AND_D / EDUCATION_AND_RESEARCH**.
- SCALE_PILOT_STRUCTURE: **5 DOMAINS × 4 HKP × 3 STEALTH × 4 INDEPENDENT CHAINS = 240 GROUPS /
  NOT EXECUTED / APPROX 720 DERIVED CANDIDATES NOT GENERATED / DATASET NOT FROZEN**.
- FIVE_VIEW_METHOD_CONTRACT: **ACCEPTED / SIGNAL_CONTRACT_V1_OWNER_FROZEN**；METHOD ENGINEERING:
  **SCHEMA_REGISTRY_INTERFACES_READY / SIGNAL_FEASIBILITY_EXECUTION_NOT_APPROVED**；FORMAL DETECTOR: **NOT IMPLEMENTED**；
  DETECTION EFFECTIVENESS: **NOT ESTABLISHED**.
- ANNOTATION_MODE: **TWO_INDEPENDENT_ANNOTATORS_WITH_OWNER_ADJUDICATION**.
- BLINDNESS_SUBISSUE: **RESOLVED_BY_OWNER_CONFIRMED_ACTUAL_DISTRIBUTION_ORDER**.
- REGISTRATION_METADATA_SUBISSUE: **DOCUMENTED_AND_EVIDENCE_BOUND / ORIGINAL_METADATA_PRESERVED**.
- REGISTRATION_METADATA_ERROR: **DOCUMENTED**.
- ANNOTATION_SCHEMA_SUBISSUE: **TARGETED_RETURNS_VALIDATED / LOGIC_CONFLICTS_ESCALATED_TO_OWNER_PACKET**.
- RETURN_FILE_CONTRACT_SUBISSUE: **V2_CONTRACT_EXECUTED / NON_SEMANTIC_DEFECTS_PRESERVED**.
- ROUND1_PRESERVATION: **APPROVED / PRESERVED_IMMUTABLE**.
- SCHEMA_V2_REREVIEW: **HUMAN_COMPLETED / FOUR_RETURNS_HASH_LOCKED / FORMAL_AGREEMENT_COMPLETED**.
- Historical S6.1-P1: **APPROVED_FOR_PILOT0_INFRASTRUCTURE_ONLY / NOT FORMAL_EXPERIMENT**；superseded by OR-023.
- Historical S6.1-P1-PILOT0: **COMPLETED_PENDING_REVIEW**；superseded by final owner acceptance under OR-023.
- HUMAN_ANNOTATION: **TARGETED A/B PHASE1+2 RETURNS RECEIVED / ORIGINAL XLSX IMMUTABLE**；
  ANNOTATION_AGREEMENT: **FORMAL_V2_ANALYSIS_COMPLETED / OWNER_ADJUDICATION_REQUIRED**.
- REAL_DOUBLE_ANNOTATION / 240_GROUP_PILOT: **NOT APPROVED / NOT STARTED**.
- Historical REAL_DATA_PILOT / 240_GROUP_PILOT: **NOT APPROVED / NOT STARTED**；PILOT1 did not authorize human annotation or the 240-group Pilot.
- MINIMAL_MATRIX / FULL_MATRIX: **NOT APPROVED**.
- Dataset: **NOT FROZEN**.
- Dataset Generation: **NOT APPROVED**.
- Detector: **NOT IMPLEMENTED**.
- Detector Implementation: **NOT APPROVED**.
- Retrieval Intervention: **NOT IMPLEMENTED**.
- Retrieval Intervention Implementation: **NOT APPROVED**.
- Training: **NOT STARTED**.
- Model Training: **NOT APPROVED**.
- Our Method Result: **NONE**.
- Corrected review blocker: `R0-I-EVIDENCE-CORRECTION-001` is **RESOLVED_BY_CORRECTED_EVIDENCE**；its discovery and first
  return remain historical evidence。
- `BLK-S6.1-LR1-001` remains **OPEN** for future strict comparison；license/redistribution issues remain separate from internal
  research access。
- P0 source/planning blockers remain resolved. L1 additionally resolves `BLK-S6.1-FU1-W1-001` through exact artifact/schema/
  assembly evidence and supersedes the Worker W1 route. Parent W2 acceptance gate is closed under PODR-061. The historical
  `W2_ATTEMPT1_EVIDENCE_BLOCKER` is
  **RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW**。`BLK-S6.1-FU1-W2-001` is
  **RESOLVED_BY_H2_RESUME02_AND_OWNER_ACCEPTANCE** only for the exact frozen minimal detector-core feasibility gate.
- `GMTP_REPRODUCTION = NOT ESTABLISHED`；`DETECTION_EFFECTIVENESS = NOT ESTABLISHED`；
  `STRICT_BASELINE_COMPARISON = NOT ESTABLISHED`；`FORMAL_PAPER_RESULT = NONE`.
- In the single frozen sample pair, benign was retained and poisoned was filtered. 这是单次冻结样本的工程观察，不是检测性能结论。
- `DETOXIFICATION_OPTION = OPTION_B`；`DETOXIFICATION_TECHNICAL_SCOPE = OPTION_B_CONFIRMED`；
  `DETOXIFICATION_TECHNICAL_SCOPE_FULL = OPTION_B_DETECTION_AND_LIGHTWEIGHT_RETRIEVAL_INTERVENTION`.
- Paper 1 intervention is limited to hard filtering or soft downweighting. Trusted context packages, complete context construction,
  multi-evidence trusted context generation, complex end-to-end Agent defense, production RAG platforms and a complete trusted
  retrieval chain are excluded and reserved for Paper 2 or later work.
- Attempt 1 archive integrity passed narrowly: outer SHA-256
  `6acdbb8038e57b1d3e88028350fc08046d73a826ba9dd167452bfc0dd834170f`, safe members `18/18`, evidence index `16/16` and
  harness SHA-256 `8411af2042774f1a18eec95e97a14ade088acbc35f09942ae9ffea4e8ea5fc06`.
- Attempt 1 evidence supports GMTP/source/input/environment identity, encoder `MODEL_DOWNLOAD_BLOCKER` and
  `smoke_executed=false`, but does not contain main-repository HEAD/clean evidence or the claimed 5.2 GB environment measurement.
- Correction 01 archive SHA-256
  `d911063e3a00daba3f8dcfea6f3e6e3b484e79f4f0fe8853a53ff9d8c415279e` passed sidecar/recompute/Worker comparison, safe members
  `6/6` and correction index `4/4`. It binds the original Attempt 1 and supplies passing main-repository integrity evidence.
- Correction 01 reports apparent bytes `5399301224` and allocated bytes `5492817920`, both below `6442450944` and internally
  consistent with its manifest. It does not capture the actual `du` commands or flags, so field provenance and non-confusion were
  not independently verifiable at that review；the later Correction 02 facts below supersede that historical gate state.
- Correction 02 archive `s6_1_r0_fu1_w2_attempt1_correction02_20260801.tar.gz` is 4367 bytes with SHA-256
  `fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622`. Sidecar/recomputation/report, archive safety and
  sorted evidence index `17/17` passed. GNU coreutils `du 9.4` raw evidence supports apparent `5399301224` from `du -sb` and
  allocated `5492817920` from `du -sB1`, zero exits, unchanged counts/spec identity and both values below `6442450944`.
- The frozen `MATERIALITY_AND_FINAL_CLOSURE_RULE` therefore closes `W2_ATTEMPT1_EVIDENCE_BLOCKER`. Accepted reusable evidence is
  limited to main/GMTP/input/environment/CUDA/disk identities, the encoder download blocker and smoke-not-executed fact；model
  loading, detector outputs/scores, runtime/RSS/VRAM, compatibility and security effectiveness are not reusable evidence.
- H1 prepared exact public snapshots `facebook/contriever-msmarco@abe8c1493371369031bcb1e02acb754cf4e162fa` (8 files,
  438708922 bytes) and `google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594` (9 files,
  881643453 bytes). Total model bytes are `1320352375`, below 2 GiB. The Git-external transfer archive SHA-256 is
  `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`; H2 resume02 evidence verifies its identity/index and
  local CUDA load on 5090 within the frozen smoke.
- Resource contract is corrected for a future resumed W2 to task-owned disk hard ceiling `10 GiB` (`gmtp-compat <=6 GiB`, two
  exact models `<=2 GiB`, harness/evidence/archive `<=256 MiB`); RAM/VRAM/runtime ceilings remain unchanged. The archive itself
  reports disk/resource limits `NOT_EVALUATED`.
- Environment observation resolved narrowly: R0-A records NumPy 2.4.6 in `llmguard-paper1`；this remains environment evidence,
  not a baseline result。
- Evidence archive SHA-256:
  historical first archive `0ce85a2bfe24e0456f9d29edc40659786d4273fcfc634df8749aee6d0e3aa9cc` with index `18/18`；
  corrected archive `904d79c59e35c6aeb157540049b0f44262b86e5c1c5b3e8d4e96ee2fad3f1c6b` with index `12/12` and matrix
  `fd7617eca689fa46fc6908f94aa4fa158aaae4d277bb17943bbcc1baf74db9bc`。
- LOCAL Control Plane read exact small GitHub source/artifact content in memory for L1；it did not acquire the NQ corpus, install
  dependencies, invoke a model/API service, run retrieval/GMTP/SafeRAG or contact RTX5090.
- Canonical entry: [Stage 6.1 research README](../research/stage6_1_hidden_knowledge_poisoning/README.md).
- Canonical Paper 1 route: [Paper 1 Research Route](../research/stage6_1_hidden_knowledge_poisoning/paper1_research_route.md).
- Canonical FU1-P0 resolution: [Targeted Resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md).
- Canonical H2 resume02 review: [Control Plane Evidence Review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_h2_resume02_control_plane_review.md).
- Current non-authoritative P1-R1 candidate: [Protocol Hardening and Option B Scope Freeze](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_r1_protocol_review_candidate.md).
- Historical non-authoritative P1 candidate: [Formal Protocol and Benchmark Specification](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_protocol_candidate.md).
- Context recovery entry: [Context Authority Map](context_authority_map.md).
- Highest internal execution authority: [PO-MHEP](project_owner_sovereignty_and_mandatory_escalation_principle.md).

## Accepted Baseline

- Last accepted architecture task: `A1R` namespace migration and governance freeze.
- Last accepted implementation stage task: `S6-T5.6 Deterministic Context Package Implementation`.
- Last accepted integration-validation task: `S6-T5.7 Controlled Retrieval Context Pipeline Integration`.
- Last accepted governance task: `GOV-S6-T5-BASELINE-ACCEPTANCE`.
- Historical acceptance snapshot: `GOV-S6-T5.6-ACCEPTANCE`; historical stage label: Last accepted stage task: `S6-T5.6 Deterministic Context Package Implementation`.
- Last accepted implementation commit: `b136ee2`.
- Last accepted integration evidence commit: `b6cedf3`. This is a test/governance evidence commit, never an implementation commit.
- Protocol acceptance closure commit: `432b07e`. It is a governance/design commit, never an implementation commit.
- Accepted capability boundary: deterministic, label-isolated provider-neutral DenseRetriever engineering behavior, including the S6-T5.3-H1 trace and failure-boundary hardening; the S6-T5.4 synthetic in-memory ContentResolver boundary; the S6-T5.5 EvidenceEnvelope/Citation boundary; and the S6-T5.6 synthetic/offline deterministic Context Package boundary. S6-T5.7 additionally accepts controlled integration evidence for these existing components. This does not establish retrieval quality, security effectiveness, context safety, trust policy, LLM integration, or a formal RAG experiment.

## Historical S6-T5 Acceptance Task Snapshot

- Task ID: `GOV-S6-T5-BASELINE-ACCEPTANCE`.
- Task name: `S6-T5 Controlled Retrieval and Traceable Context Baseline Final Human Acceptance`.
- Task type: **GOVERNANCE_BASELINE_ACCEPTANCE_RECORD**.
- Status: **HUMAN_ACCEPTED**. The Git commit created by this task is the baseline governance acceptance record and remains subject to post-commit SHA verification.
- S6-T5.6-P1: HUMAN_ACCEPTED.
- S6-T5.6-P1-H1: HUMAN_ACCEPTED.
- S6-T5.6-P1-H2: HUMAN_ACCEPTED.
- S6-T5.6: HUMAN_ACCEPTED.
- S6-T5.6-I1: HUMAN_ACCEPTED.
- S6-T5.6-I1-H1: HUMAN_ACCEPTED. It hardens only trace scenarios, package configuration identity, dependency error redaction and abstention/trace consistency.
- S6-T5.7: **HUMAN_ACCEPTED**. Static and opt-in real-infrastructure integration evidence is recorded in [S6-T5.7 completion record](s6_t5_7_integration_completion_record.md). Its accepted evidence commit is `b6cedf3`, not a new implementation commit.
- S6-T5.8-H1: **HUMAN_ACCEPTED**. It corrects only the commit-evidence taxonomy and semantic mapping in the [S6-T5 baseline acceptance report](s6_t5_baseline_acceptance_report.md).
- S6-T5.8: **HUMAN_ACCEPTED**. Its original candidate baseline closure commit remains `37cccdc`; its accepted baseline content commit is `4ecf73a`.
- S6-T5 Controlled Retrieval and Traceable Context Baseline: **HUMAN_ACCEPTED BASELINE**. The baseline governance acceptance commit is `CURRENT_ACCEPTANCE_COMMIT / verify from Git after commit`; it is neither an implementation commit nor an integration evidence commit.
- Historical approval snapshot: S6-T5.8 was `APPROVED_TO_START / DOCUMENTATION_IN_PROGRESS` under `PODR-032`; this is not its current status.
- Historical approval snapshot: S6-T5.8-H1 was `APPROVED_TO_START / DOCUMENTATION_HARDENING_IN_PROGRESS`; this is not its current status.
- Historical pre-LR1 snapshot: Stage 6.1 formal research: NOT APPROVED.
- Formal RAG security experiment: NOT STARTED.
- Historical approval-gate snapshot, not the current status: `S6-T5.7+: NOT APPROVED`. The accepted S6-T5.6 implementation history remains `71067d1` (initial candidate), `b136ee2` (final accepted implementation) and `6da27a6` (previous accepted implementation).
- S6-T5.5-P1: **HUMAN_ACCEPTED**.
- S6-T5.5-P1-H1: **HUMAN_ACCEPTED**. Factory only accepts canonical `corpus:` RetrievalEvidence; renderer only accepts Envelope + Binding and fails closed on seven-field mismatch.
- S6-T5.5: **HUMAN_ACCEPTED**.
- S6-T5.5-I1: **HUMAN_ACCEPTED**. Initial implementation commit `2cacef7` remains historical evidence.
- S6-T5.5-H1: **HUMAN_ACCEPTED**. Final hardening commit `6da27a6` fixes metadata immutability, timestamp parity, canonical Evidence UID and fixed redacted input-error semantics without adding ContextBuilder behavior.
- S6-T5.4-P1: **HUMAN_ACCEPTED**.
- Governance acceptance record: `GOV-S6-T5.4-P1-ACCEPTANCE`.
- S6-T5.4 protocol blocker: **RESOLVED_BY_APPROVED_PROTOCOL_FREEZE**. The original discovery, risks and fail-closed stop remain preserved in the blocker record.
- S6-T5.4: **HUMAN_ACCEPTED**.
- S6-T5.4-I1: **HUMAN_ACCEPTED**. It remains an offline engineering implementation, not a formal RAG security experiment.
- S6-T5.4-H1: **HUMAN_ACCEPTED**. It is an acceptance hardening fix, not a new retrieval or RAG capability.
- Blocker record: [S6-T5.4 protocol blocker](s6_t5_4_protocol_blocker_record.md).
- S6-T5.5-P1 review record: [EvidenceEnvelope and Citation boundary freeze](s6_t5_5_protocol_review_record.md).

## Stage 6 Implementation State

- Task ID: `S6-T5.3`.
- Task name: `Provider-Neutral DenseRetriever`.
- Status: **HUMAN_ACCEPTED**.
- GOV-ER1: **HUMAN_ACCEPTED**.
- GOV-ER1-H1: **HUMAN_ACCEPTED**.
- GOV-PODR1: **HUMAN_ACCEPTED**.
- S6-T5.2 `Retrieval Runtime Contracts and IDs`: **HUMAN_ACCEPTED**. Its completed scope is explicit safe query projection, canonical `RetrieverQueryRecord`, deterministic `RetrievalRequest`, `ContentRef`, evidence UID, chunk-level `RetrievalEvidence`, safe evidence summaries, deterministic `RetrievalTrace`, and legacy import/adapter compatibility.
- S6-T5.3-P1: **HUMAN_ACCEPTED**. Public metadata schema `1.1` carries a validated, non-label, no-body `parent_doc_id` from VectorDocument to VectorSearchHit; schema `1.0` remains legacy-compatible.
- S6-T5.3: **HUMAN_ACCEPTED**. DenseRetriever accepts only schema `1.1` hits, validates request/store provenance, and produces canonical `RetrievalEvidence` plus `RetrievalTrace` without reading the corpus.
- S6-T5.3-H1: **HUMAN_ACCEPTED**. Trace `candidate_count` means raw query hits before sorting/deduplication; store provenance and provider/store failure boundaries fail closed with redacted Retrieval errors.
- S6-T5.4: **HUMAN_ACCEPTED**. I1 implements only contracts, injected protocols and synthetic in-memory dependencies; it does not read Stage 6 fixture content or create a real fixture mapping.
- S6-T5.4-H1: **HUMAN_ACCEPTED**. The resolver has no public registry/reader escape hatch; injected adapter, registry and reader errors are re-instantiated with fixed redacted messages while preserving causes.
- Audit boundary: ordinary `repr()` and `to_audit_dict()` omit retrieval query text, document plaintext and content-reference expansion. Runtime query objects physically exclude evaluator fields.

## Approval Gate

- `S6.1-LR1` is `HUMAN_ACCEPTED` at commits `1294632ca0501e7b999a29383780bec49eaa6b04` and
  `85a565535a38196a7d6003e728b5cb6a2b17fa8a` for its benchmark alignment and Context Recovery Governance records.
- The accepted scope is research route, benchmark alignment, governance, context persistence and reproduction planning only.
- Historical R0 execution approval and first `RETURNED_FOR_WORKER_CORRECTION` review remain preserved。The superseding corrected-
  evidence decision is `S6.1-R0 = HUMAN_ACCEPTED_WITH_BLOCKERS`。
- Next operational action: Owner reviews the Pilot4 A/B disagreement-only packet. Begin with the five
  `LATE_DISCOVERED_CANDIDATE_DEFECT` flags, then adjudicate the remaining material field disagreements. No automatic Ground Truth,
  Candidate/Evidence repair, 240-group scale-up、Dataset freeze、formal Detector、training、5090 or Formal Experiment is authorized.
- Human accepted: GOV-ER1, GOV-ER1-H1, GOV-PODR1, S6-T5.2, S6-T5.3-P1, S6-T5.3-H1, S6-T5.3 DenseRetriever, S6-T5.4-P1, S6-T5.4-I1, S6-T5.4-H1, and S6-T5.4.
- S6-T5.3 human acceptance is limited to its documented offline engineering scope and deterministic test behavior.
- `S6-T5.4` is **HUMAN_ACCEPTED**. Its acceptance does not approve S6-T5.6 ContextBuilder behavior; that remains a separate boundary.
- `S6-T5.5-P1` and `S6-T5.5-P1-H1` are **HUMAN_ACCEPTED** design protocols. Their I1/H1 implementation was separately accepted; S6-T5.6-P1 now freezes the future package-level selection contract without implementing it.
- `S6-T5.5-I1`, `S6-T5.5-H1` and parent `S6-T5.5` are **HUMAN_ACCEPTED**. They implement only Envelope/Citation contracts and one structural block.
- The acceptance did not authorize Citation allocation, a package or ContextBuilder before I1. The separately approved I1 now implements only those frozen offline behaviors; it does not authorize Trust or model calls.
- S6-T5.6 P1/H1/H2 are HUMAN_ACCEPTED protocol records. `S6-T5.6-I1`, `S6-T5.6-I1-H1` and parent S6-T5.6 are HUMAN_ACCEPTED synthetic/offline implementations.
- S6-T5.7 is HUMAN_ACCEPTED only for the documented controlled retrieval-context engineering evidence. It does not change the accepted implementation commit or establish a formal RAG experiment.
- S6-T5 baseline final acceptance does not create a tag, a Stage 6.1 branch, or a formal RAG experiment.
- Historical S6-T5 snapshot: the project owner had to separately approve Stage 6.1; that snapshot is superseded only for the documentation-only S6.1-LR1 scope.

## Must Not Start

- Automatic 5090 contact/transmission by Codex or any replay of Correction 02. Its evidence-only run and 本机 review are complete.
- On 本机: any external baseline workload, archive extraction, model loading, GMTP/harness smoke, dataset acquisition, GPU computation or formal
  experiment. The narrowly approved H1 public-artifact download is complete and grants no continuing download authority.
- On 5090: overwrite/delete/rename resume_01；reuse or rerun resume_02；automatic resume_03；a second H2-B call；anything beyond the exact frozen H2 contract；network fallback、
  environment mutation、algorithm reimplementation、silent source patch、parameter/input/model substitution or formal workload。
- Everywhere: any unapproved owner-decision change, 240-group scale-up, Dataset formal freeze, formal Detector/Retrieval
  Intervention implementation, training, 5090 work, Paper Result, Formal Experiment or SOTA comparison.
- Additional ContentResolver changes, document-content access beyond synthetic test inputs, Trust policy, retrieval guard, or any S6-T5.8 behavior beyond the completed documentation closure.
- Groq, mock/real LLM invocation, evaluator, metrics, T10-T15, formal RAG attack matrix or report generation.
- New Stage 6 business code under `src/codeguarder/`, any mutation of Stage 1-5, or any mutation of Stage 6 data fixtures.

## Current Claims Boundary

Can additionally claim: H2 resume_01 produced valid fail-closed evidence for a missing bundle/sidecar；its 4,570-byte archive SHA
`941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d`, safe 20-file/1-directory layout and 19/19 index passed 本机 review；H2-B did not execute and call_count is zero。Resume_02 archive SHA
`58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563`, safe 27-file/1-directory layout and independently
recomputed `25/25` index passed；H2-A is `18/18 PASS`, exact local models loaded on RTX5090 without CPU fallback, the authorized
H2-B call executed exactly once, and the redacted two-document outputs/resource values are accepted as engineering-smoke evidence
only。Correction 02 passed 本机 raw-evidence review and the final materiality rule closed the historical
`W2_ATTEMPT1_EVIDENCE_BLOCKER`。Attempt 1 is `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER`, with the narrow reusable
preflight boundary recorded above。H1 prepared two exact-revision offline model snapshots and an integrity-checked transfer bundle
  that is now verified on 5090 for the frozen H2 smoke。P0 and L1 are `HUMAN_ACCEPTED`；the exact released NQ attack-text artifact identity, all 100 records and
official deterministic LM-targeted assembly are verified；API-free reuse is verified feasible while API-free generation and exact
paper-generation identity remain unresolved/partial。The GMTP W2 input, models, parameters, isolated environment and resource
ceiling are frozen and W2/FU1 are accepted and closed only for engineering feasibility。The original
baseline roles remain unchanged。PO-MHEP is permanently accepted as the highest internal execution authority。

Can claim: within the offline engineering-test scope, the `S6-T5 Controlled Retrieval and Traceable Context Baseline` is HUMAN_ACCEPTED. It comprises deterministic and label-isolated retrieval runtime contracts, provider-neutral DenseRetriever, the synthetic ContentResolver, EvidenceEnvelope/Citation boundaries, deterministic Context Package behavior, and S6-T5.7 controlled integration evidence including an opt-in fixed MiniLM plus temporary Chroma close/reopen check. `4ecf73a` is the accepted baseline content commit; the current governance acceptance commit is not an implementation or integration-evidence commit. Historical public loader imports remain compatible through the canonical `llmguard` type.

Can claim: the four selected PILOT2 targeted returns were hash-locked; formal A/B V2 agreement preserves 47 disagreement records
and 37 schema-logic conflicts. Owner decisions plus a separately bound correction resolve all 84 issues across 26 candidates without
rewriting the workbook. The Pilot-only Ground Truth contains 36 executable records (Clean 1 / Poison 12 / Hard Negative 23), and
Pilot2 is closed only for annotation-protocol and Ground-Truth feasibility. A deterministic CPU-only Pilot3 generated 180 separated
five-view signal records; this establishes engineering/signal diagnostic execution, not detector effectiveness.

Can claim: the b705cc quality-convergence/Evidence Pool history remains unchanged and the additive hardened candidate version has
23 targeted text repairs. All 72 pools retain two distinct units and A/B deterministic slot-order separation; the human-visible pool
now has four columns with official page/document titles only. Schema V3.1 retains 4 Phase1 and 7 Phase2 manual fields. A separate
visible-input-only process locked one 72/72 semantic review before expected-contract comparison; attempt01 mismatches remain evidence,
final mismatch is zero, validator and all 10 rendered workbook Sheets pass. This is annotation-protocol readiness for Owner acceptance
only. It is explicitly not independent A/B evidence, human validity or distribution.

Can claim: the externally completed targeted R3 raw remains immutable at `12062 bytes` / SHA256 `80a10a1e...0b4441`. Expected V3
was independently derived from candidate、Guide and frozen Evidence and SHA-locked before reviewer values were parsed；its exact
diff is seven fields across six candidates. V3 agreement is overall `35/37` and exact relevant fields `35/37`; controls are 16/16,
M2 is 2/16, M4/M8 pass and frozen gates A–F pass. This supports `RECOMMEND_ACCEPT_WITH_NONBLOCKING_NOTES` and stopping calibration,
not Owner protocol acceptance or benchmark performance.

Cannot claim: the two-document smoke reproduces GMTP；its two scores establish detector effectiveness, calibration, safety,
generalization or a paper metric；any
external baseline was reproduced；strict comparison is ready；SafeRAG pipeline is ready；dataset/
Detector/Our Method/training/result exists；or retrieval quality/security, SOTA, production readiness or formal-experiment outcomes
are established.

## Known Technical Debt

- Historical CRLF/LF hash-baseline false positives remain historical facts; do not rewrite their files to silence checks.
- Dynamic Git state must not be represented as a static assertion in this document.
- S6-T5.3 must preserve all frozen contracts; any need to change them is a `DESIGN_OR_PROTOCOL_BLOCKER`.
- Resolved protocol record: the former hit boundary lacked `parent_doc_id`; schema `1.1` now carries it through the public metadata contract without changing legacy schema `1.0`. See [S6-T5.3 blocker record](s6_t5_3_protocol_blocker_record.md).

## Historical update — 2026-09-16

- Date: `2026-09-16`.
- Updated by: 本机 executing
  `P1-RETRIEVAL-BEHAVIOR-HARNESS-AND-DEPLOYABLE-SIGNAL-BOUNDARY-01 / REL-2026-0066`.
- Query/corpus/run/signal locks pass before labels. Sparse and frozen-offline Dense each preserve two complete traces. The R matrix
  computes rank/score/stability while version-aware composition remains input-missing. No Detector、threshold、240-group、5090、
  Formal Experiment or Paper Result occurred; Auto Continue=`NO`.
# 2026-09-16 — Trusted Evidence Retriever / Version Registry prototype

- Current task: `P1-TRUSTED-EVIDENCE-RETRIEVER-AND-VERSION-REGISTRY-PROTOTYPE-01` completed.
- Status: `TRUSTED_EVIDENCE_RETRIEVAL_COMPLETE / VERSION_REGISTRY_READY_WITH_LIMITATIONS / DOCUMENT_DETECTOR_READY_WITH_LIMITATIONS`.
- 57-doc trusted corpus and 72 Candidate-derived queries were locked before Oracle E1/E2 evaluation; label/oracle-query leakage is zero.
- Registry metadata remains partial; eight Temporal signals stay `ORACLE_ONLY`. No Detector training, threshold tuning, risk calibration, 240-group run or formal result occurred.
- Next gate: Owner approval for registry coverage repair and non-Oracle Document Detector feature freeze.

# 2026-09-17 — Registry V2, query robustness and Detector feature freeze

- Task `P1-TRUSTED-VERSION-REGISTRY-COVERAGE-REPAIR-QUERY-ROBUSTNESS-AND-DOCUMENT-DETECTOR-FEATURE-FREEZE-01` completed.
- Registry V2 uses only frozen Evidence/accepted metadata: current/history `5/5`, effective interval `26`, authority/issuer `55`, predecessor/successor `1/1`. Unsupported values remain missing; chronology alone is not supersession.
- Four query conditions and 12 deterministic runs were locked before Oracle evaluation. `Q_FULL→Q_NO_TITLE` Hybrid Any-R@1 delta is `-0.0139` and MRR delta `-0.0069` (`SOURCE_TITLE_RISK=NONE`). `Q_TEXT_ONLY→Q_STRUCTURED` deltas are `+0.1667/+0.0833` (`LEXICAL_OVERLAP_RISK=MATERIAL`).
- The deployment-realistic frozen setting is `Q_NO_TITLE + HYBRID`, not the best post-hoc setting. Feature Set V1 contains 23 raw non-Oracle S/E/P/T features; R remains Stage B and six Temporal features remain Oracle diagnostic only.
- Current gate: `DOCUMENT_DETECTOR_READY_WITH_LIMITATIONS`. No Detector was trained; no threshold, calibration, 240-group execution, 5090 run, formal test or result claim occurred.

# 2026-09-21 — First Document Detector Phase A blocked before fitting

- Current task: `P1-FIRST-DOCUMENT-DETECTOR-PROTOTYPE-PREFLIGHT-AND-DEVELOPMENT-EXECUTION-01`.
- Owner approved protocol freeze and prototype training only after every blocking Phase A gate passed.
- Input identity、23 frozen features、72 rows、R/Oracle exclusion、zero blocking leakage、24 matched groups and 24-fold LOGO all pass.
- Missingness gate fails: `host_publisher_relation` and `publisher_issuer_match` are `INPUT_MISSING` in 72/72 rows, have zero observed values and no frozen neutral representation. Training-fold mode is undefined.
- Status: `PHASE_A_BLOCKED / PHASE_B_NOT_AUTHORIZED / TRAINING_STARTED_FALSE / P1-FDD-PREFLIGHT-BLOCKER-01 / HUMAN_DECISION_REQUIRED / Auto Continue=NO`.
- No OOF prediction, metric, ablation, coefficient, bootstrap, permutation control, calibration, Risk or Retrieval Exposure model exists. Next gate is Owner selection of an additive upstream repair, explicit all-missing engineering representation, or versioned 21-feature contract.
