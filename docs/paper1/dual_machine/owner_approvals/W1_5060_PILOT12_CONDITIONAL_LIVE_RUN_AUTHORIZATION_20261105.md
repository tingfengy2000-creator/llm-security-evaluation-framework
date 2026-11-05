# Paper 1｜Pilot12 单次受限真实运行：Owner PO-MHEP 十二字段条件授权

- **决策 ID**：`W1-OD-20261105-5060-PILOT12-CONDITIONAL-LIVE-10`
- **日期**：2026-11-05 Asia/Tokyo
- **权限状态**：`OWNER_EXPLICIT_CONDITIONAL_LIVE_AUTHORIZATION / PRE_ADMISSION_BLOCKED`。
- **依据**：Owner于本次项目监督会话明确批准“5060进入最小RAG Pilot的一次性受限真实执行准备与有条件运行阶段”；允许百炼真实传输实现和审核、108格精确Token上界与预算、全部前置硬门PASS及授权绑定后，冻结顺序执行首3格再（仅通过工程检验后）继续最多105格；禁止额外探测/重试/更换模型、Prompt、样本和参数；异常立即停；保留USD30/25/28及D1隔离。
- **作用分支**：`research/paper1-chinese-defense-5060`，授权前HEAD `ce90a34348dff093e132e6f9823ad9b84e4f67d9`，本决议不涉及5090分支。
- **原Runner源码锚点**：`1a11fd2ef4802d5029619acb3e65c5ad09a4a57e`；离线最终交付HEAD见上。
- **冻结方案文件SHA256**：`PILOT_EXECUTION_PROPOSAL.json` `0aaf4cfb28dc1e7d9fea8fcdc8f7143afd56857fa300f8b6e3f8f9d0ff081cb6`；原私有108格 `7db82812f893fc0384b2896c98bb5c779504e19a5c45a097945962e840999c96`；共同system `b3c74613bc3700eacdce7dfedc382043013f452e321a13d8639b27817edbd1f1`；AI暂定参考 `5c5f212ba16da97b114d897de910ab383a47d96db4cb7cd9b54e638f7f03cf31`（仅私有评价侧）；TopK seal `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`、PAIR01 seal `bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb`。
- **事件定位**：本Owner授权不宣称前置门已经PASS，不宣称已经运行或已经产生ASR。执行者不能用AI自己的推断填充Owner记录。

## 1. Issue ID
`W1-OD-20261105-5060-PILOT12-CONDITIONAL-LIVE-10`。跨机引用须附branch及完整Git SHA，不使用曾冲突的`PODR-154`单号。

## 2. Issue name
固定D1 Pilot12、36世界、B0/B1/B2三臂共108格生成实验的真实传输准入、工程性首3格门、剩余105格受限执行与证据封存。

## 3. Stage and discovery
FastC`PARTIAL_DIAGNOSTIC_UNRESOLVED`；D1已收到12题AI-assisted provisional JSON，正式HumanGold0/target UNKNOWN；108格设计封存，Runner已用FakeTransport通过29tests+Ruff/MyPy及模拟全108、timeout/usage故障拦截；真实模型调用=0、Pilot=NOT_RUN。此授权从实现/Mock进入一次性**有条件**真实Pilot，不是放行新算法或正式论文实验。

## 4. Facts / evidence
- `OBSERVED_GIT`：原RunID`W1-5060-RUNNER-20261105-01`离线报告、固定108/80唯一prompt_hash、失败停发及受控日志、source hash与旧预检Gate。
- `OWNER_CONFIRMED`：允许条件性首3格+后续最多105格；Owner此前自行核验百炼模型、地域、费率和账户余额，等级为`OWNER_ATTESTED`，没有向Git披露具体数值。
- `SOURCE_DERIVED_OFFICIAL`：百炼 `qwen3.7-plus-2026-05-26`是固定快照且支持结构化输出；官方OpenAI兼容Chat文档称`max_tokens`即将弃用，`max_completion_tokens`（支持Qwen3.5-Plus及后续）覆盖完整输出，实际计数可能相差至多10 tokens；`enable_thinking=false`需显式。
- `INFERENCE`：首3格如果均完成端点/模型/usage/状态工程审计、没有完整性异常，继续剩余105格可避免无意义第二审批，不根据答案正确率作选择。
- `UNKNOWN/NOT_PASSED`：同模型精确chat token或形式证明的严格上界、真实wire字段/强制256输出限额/隐藏计费、绑定了来源的预算USD与外传权限、受审最终live transport SHA/授权锚点。未知不能自动PASS。

## 5. Constraints
AGENTS.md、PO-MHEP、冻结TopK/PAIR01/Pilot12三臂、29候选召回+7MISS、标签独立Evaluator、D1资料合法传输与隐私、C盘禁新增项目可控内容/D/E最少20GiB、USD总30/25警戒/28不可新开批、不能宣称2.5pp性能门满足、5090分支隔离、无新研究路线/参数调整。

## 6. Why now
Pilot方案和Mock Runner已完成，主要可行性问题必须依靠真实同一Qwen版本回答结果验证。Owner要求压缩周期，允许一份条件审批覆盖固定108格，并设置严格首3格工程检查。

## 7. Risks
真实HTTP前置网络锁实现偏差、错误region/模型或明文数据外传、自动重定向/代理/重试、模型输出隐藏thinking与被弃用参数语义、字节代理被误作精确token、失效费率或账本、失败响应缺usage但仍可能计费、首3格故障后继续、以生成结果反馈选样、非独立36事实组当独立统计样本、以AI答案当HumanGold。

## 8. Options/impact
- **A【OWNER APPROVED CONDITIONALLY】**：实现窄真实传输，严格全部机器可验证硬门和源/数据/授权hash后启动冻结序列；首3格仅检工程协议，不检最终答案质量；全PASS后继续剩余最多105格，首个异常停发、封存。成本上界由执行前真实账本绑定，风险受硬门限制，原科学资产不可逆更改为零；真实请求有外传与费用不可回滚风险。
- **B【NOT SELECTED】**：分成首3格与余105格两次独立Owner批次；更严格但增加流程成本。除非出现硬门失败或需变更范围，否则不强制重复授权。
- **C【FORBIDDEN】**：跳过精确token/账本/网络/隐私、假设Owner已经替机器校验、直接解`--live`，或换模型/Prompt/参数消除不兼容；严重破坏科研与费用控制。

## 9. Recommendation
执行A，但其“原则同意”不是免门通行证：**本次授权同时涵盖首3格与后105格的条件权限，只有在最终Runner源码/工作树、模型wire、严格Token上界、全工作线USD预算、D1允许发送正文范围和受控Run Manifest均锁定且全部PASS后，才可物理创建第一次HTTPS POST。** 不能一边补证一边试错式发送。

## 10. Rationale/confidence
Owner许可和Mock历史高置信；真实模型行为无实测。单次固定108实验最多查询调用108（包括首3），禁止探测/judge/重试。由于12独立事实组单个变化8.33pp，小Pilot只支持探索性结论，不能据此证明既有2.5pp安全保护门满足。

## 11. Decisions and execution release gate

**批准以下范围，不需要在首3格全工程通过后为后105格再申请Owner：**
1. 仅在原5060分支实现真实百炼HTTPS传输，且仅一个经本地静态审核确认的region专属官方`/compatible-mode/v1/chat/completions`端点；精准模型`qwen3.7-plus-2026-05-26`。严格TLS、host allowlist、禁止重定向/环境代理/静默SDK retry，单个POST、并发1，单格最长总90秒，超时即STOP。仅由受控Runner进程从环境读取密钥且不记录。
2. 冻结36世界×G0/G1/G2、原顺序108格、80相同prompt_hash可重复但不可合并、B0原TopK和B1/B2旧封存删除、所有Prompt/Query/片段及次序不变；仅两个既有消息角色system/user；不加入参考答案/角色/目标/额外提示；输出JSON schema和模型设置保留原proposal。任何输入SHA或参数变更先STOP并升级Owner。
3. 允许只读官方模型接口文档、使用已存在合法工具离线计算108条完整wire+chat framing的**严格可验证Token精确数或保守上界**，并核freeze/方法SHA。旧`UTF8字节+512`仅代理量，不等于证据。**如无可验证上界则0次真实调用**。禁止为此额外API探测或下载/安装tokenizer（该类需单独批准）。
4. 旧候选`max_tokens=256`与`enable_thinking=false`在真实Wire可证明满足输出计费上界时保持不变。官方的`max_completion_tokens`是另一字段；若必须切换、增加/减少cap或修改请求体语义，属于参数变更，**不能自动切换**，按PO-MHEP提请Owner明确批准。官方`max_completion_tokens`的潜在10-token误差不能被误称为旧`max_tokens`的精确误差保证。预算在确认真实计费前不得假定只有256；如缺可信上界，不请求。
5. 全工作线统一预算：冻结真实费率/区域/币种/FX/已结算/在途未结算/余额或可用上界，以及从原CNY账本差额到USD commitment的处理，D/E私有预算JSON hash锁；按所有108请求上界、额外计费差异和≥20%不确定性预留（不增加请求），投影已结算+未结算+整个批次reserve**严格小于USD28**、余额覆盖；≥25警戒、≥28停止新请求/新批、累计不得超过USD30。Owner已有基础账户核验可记录`OWNER_ATTESTED`但必须数值化才PASS；不得要求密钥或公开截图，更不得编造数字。
6. **D1外传范围**：只允许冻结36世界的原query与保留TopK片段（以及已冻结中立system），作为推理正文发往获准百炼地域/账号；只发送实际被调用格的文本。需先用可复查的来源使用权/访问授权、个人/敏感信息检测与外传范围记录证明合法。不得传角色标签、攻击target、答题参考、Evaluator/GT vault、其他私有日志、原始来源文档整体、API/凭证/其他数据；发现数据许可不清或敏感内容需删改，STOP并提Owner处理，不得静默清洗或改原实验输入。
7. **Run解锁为先验Owner条件授权的证据闭合，不是Agent追加Owner签名**：批准文档SHA + 冻结proposal SHA + 最终Runner源码Git commit及源文件SHA + 全108私有输入SHA + 计数证据 + model/wire身份审核 + 外传allowlist + 预算数值hash + D/E路径 + 驱动单一审批`RUN_ADMISSION_MANIFEST`一一绑定；必须独立QA/checker验证所有门`PASS`且保护自动锁；如某项`UNKNOWN/BLOCKED`，保持`LIVE_NOT_AUTHORIZED`、0 POST并交付未闭合报告。禁止仅凭命令`--live`或更改布尔标志、环境变量、自己签Owner身份绕锁。
8. 若准入全PASS，按原冻结顺序执行首次3格（不得另选题或插入探测）。每格结束检查真实返回的model、HTTP/TLS、JSON fields、finish_reason、实际Token usage/reasoning/cached、账单边界、日志和输出封存。三格均为协议成功且无任何预算/数据/格式/网络异常才允许继续第四至最多108格；**不以事实正确率决定是否继续，不读取参考**。
9. **任何**HTTP异常/超时、缺usage、response非预期、返回模型别名、非JSON或格式错误、finish_reason=length/被截断、输出或隐藏token越限、费用不明、余额异常、SSL/重定向/代理/网络误路由、输入/身份/权限变更、脱敏/数据泄漏、文件写C、磁盘余量低于20GiB、账本校验失败，立即STOP，无第二次发送、无重试/回滚重发/自动恢复。所有108格保留`SUCCESS/FAIL/NOT_RUN`，失败预留不当0。
10. 封存前不调用AI judge，不读取临时参考答案来选答或分配组；**完成所有实际与NOT_RUN结果字节封存并建立SHA索引后**，才允许独立D1开发评价根据已获批准的 provisional JSON计算`PROVISIONAL_REFERENCE_CONSISTENCY`、拒答/覆盖/用量/时延/费用等。此评价只用于D1，不改变HumanGold0、target未知、C3/TargetedASR/正式AnswerAccuracy`NOT_MEASURED`；若无明确封存和独立角色隔离，就只提交原始生成证据，不开启评分。
11. 禁止修改原冻结科学资产或运行B5/B6、D1-40、D2/D3/Reviewer/GT、T1/T2、5090Claim、跨分支合并。严格区分新增Runner传输逻辑（获准）与算法/模型配置更改（不获准）。

## 12. Conditions and STOP
本决策是**单次Run条件授权**；若执行启动且实际发送了任意一格，不得再另起新的108格实验或补跑/失败恢复。条件不足时只允许准备、离线测试、Git提交、归档BLOCKED报告；没有实际HTTP前不能宣称`RUNNING`。如首3格或后续异常，留完整状态后STOP且PO-MHEP记录失败；不因合同存在而自动允许新的批次。最迟完成当前条件性任务后保存受控原始响应/HTTP状态/Provider ID/usage/费用/全108格、完整RunManifest/冻结SHA、异常和测试、脱敏Git科研登记，只推送5060分支并STOP。

## Evidence / terminal statuses
准入未闭合：`LIVE_GATE_BLOCKED_NO_REQUESTS`；前3格工程检查失败：`LIVE_INITIAL3_STOPPED`；后105运行异常：`LIVE_PARTIAL_STOPPED`；完整108格合法完成：`LIVE_PILOT108_COMPLETED_PENDING_PROVISIONAL_EVAL` 或在后封存独立评价合规完成时 `LIVE_PILOT108_COMPLETED_D1_PROVISIONAL_EVAL`。只有真实 provider request ledger 支持才称调用发生；Mock永远不是科学输出。须报告真实请求数/成功/失败/NOT_RUN、真实费用/未知结算、全部SHA、最终远程HEAD、branch clean/0:0。
