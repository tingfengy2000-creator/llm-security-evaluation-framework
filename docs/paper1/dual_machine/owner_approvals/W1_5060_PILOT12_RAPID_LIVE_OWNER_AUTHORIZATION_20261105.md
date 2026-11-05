# Paper 1｜Owner12 快速真实Pilot12授权（PO-MHEP十二字段，风险受限）

- **Owner决策ID：`W1-OD-20261105-5060-RAPID-LIVE-12`**
- Owner明确要求“不要反复准备工作，我们没有时间，请快点推进真实实验，验证方法的可能性”。结合前序“我不想那么死板，不要我们自己给自己制造困难”、既有Owner10单次3+105原则许可、Owner11 V2仅字段修订、5090独立/受限等约束，本决策**明确把工程/科研自设门槛转为比例适当的风险控制，并条件授权原V2真实生成**。
- 日期2026-11-05 JST；唯一分支`research/paper1-chinese-defense-5060`；本决策前远程HEAD`c03dd74507ad1a09fd5118933732562fa244cac2`，V2 Runner源码`43be925d57ef6fbe9cbb27d22c7f1495373c6204`。
- **授权状态：`OWNER_APPROVED_CONDITIONAL_REAL_PILOT12_V2 / EXECUTE_AS_SOON_AS_MINIMAL_SAFETY_GATES_PASS`**。不再预设“做完工程后再请一轮正式Owner批准”。本授权覆盖首3格和同一次剩余最多105格；Owner12不表示Git写入时已满足门，程序不可因为本文件存在自动发送。
- 冻结资产：V2 proposal SHA256 `e5bd219b7812b8ef97ef916226ac221e177f227808cd0dbc0bbe280920d1b70e`；私有108完整wire plan `0920add3e5b5383a9b685207cabeb539bb3d414ee1db30c6f7a313d37469bbcc`；有序grid `78708759e0965e816d9d5b7aaa0bca92d2a6b92562930cd028dc87875d09468c`；原V1 `0aaf4cfb28dc1e7d9fea8fcdc8f7143afd56857fa300f8b6e3f8f9d0ff081cb6`；P2 `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`；PAIR01 `bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb`。
- **本决策不直接调用百炼，也不声称实际生成已完成。** 必须由用户可访问D/E私有工作树的5060 Codex实施，登录/密钥只从本机现有环境取，不将密钥等内容写入公开Git。

## 1. Issue ID
`W1-OD-20261105-5060-RAPID-LIVE-12`；双分支引用加branch与完整Git SHA，不复用PODR-154。

## 2. Issue name
以可接受的有界成本/输入长度风险替代无产出形式证明，尽快执行唯一一轮D1 Pilot12 V2：同一Qwen模型固定36世界×G0/G1/G2=108次真实生成，先3后最多105。

## 3. Stage / prior evidence
现有`FAST_UNBLOCK_PARTIAL_BLOCKED`与`EVIDENCE_RECOVERY_PARTIAL_BLOCKED`均为**准入未满足**，真实API=0。V2 108/108严格单字段diff、64项离线Runner测试和事务封存模拟均通过；46/46实际发出source hash身份可溯，29属于已签署D1候选、17对应官方背景快照；北京Workspace Host已有D/E哈希；历史361请求可逐份核，CNY7.611826（Owner过去CNY7.528095914、差额0.083730086，未配对历史预留0）。C门4096是项目自设；108格最大消息2444 UTF8 bytes，闭源Tokenizer严格证明不存在；真实生成仍为0。

## 4. Evidence grades
- `OBSERVED_GIT`：V2原108格、模型、system/query/TopK/顺序、零额外重试/封存与停止能力是既有源代码/日志已验证的事实。
- `OWNER_EXPLICIT`：Owner要求立即推进实测，不要无谓重复准备；此处一次性授权明确接受**首次超4096输入可能已付费和外发**的有限风险，把项目4096门从事前形式证明改成按provider真实usage逐格后置核查。
- `OWNER_ATTESTED`：此前Owner核实百炼模型/地域/费率/余额；本轮批准恢复的北京Workspace为优先适用的研究处理方，但**不因用户作为Owner就替第三方原文认定产权**。
- `DOCUMENTED`：官方固定Qwen3.7 Plus支持北京区域Workspace专属host，`max_completion_tokens`用于包括思考的整体输出，上限可能偏差最多10 Token；非思考固定模型最大输入991808。公开价格北京<=256k每百万输入2元/输出8元，超过256k计费更高。引用官方文档与执行时本地费率。
- `UNKNOWN`：真实端点第一次返回模型身份/usage/实账、当下历史其他工作线费用、全部第三方源权限最终状态。不可将这些未知冒充实测。

## 5. Affected constraints
不改原D1/P2/PAIR01/FastC/Pilot12 12组36世界108格、G0/G1/G2、固定`qwen3.7-plus-2026-05-26`、temperature0、top_p1、禁thinking/search/tools、JSON模式、`max_completion_tokens=256`、无重试/无judge/无动态采样，保留2.5pp质量约束为未来论文目标而非本Pilot统计结论。留D/E隔离、C盘受控零新写、最少20GiB、来源/凭证/个人信息保护、5090独立不改、D2D3不读、USD25警戒/28停批/30累计硬限。

## 6. Why now
目前研究成果主要是检索/过滤和模拟，并**未回答G0/G1/G2是否降低模型事实错误**。继续要求闭源服务端形式化Token证明等缺证门可能无限阻断；Owner明确应把D1开发Pilot引向实际生成结果，而非更多重复治理设计。

## 7. Risks accepted and not accepted
**Owner接受的限定风险**：取消108格事前“严格<=4096”证明，固定输入并仅在HTTP成功后用`usage.prompt_tokens`核4096；首次超界请求已发出且可能收费、不能撤销；停止后将其计入FAIL/越界，不重试；严格串行保证最多一个越界发送。冻结V2的`max_completion_tokens=256`按官方+10候选作预算并审计实际usage/hidden reasoning。
**不接受**：发送有明示限制或明显无权第三方材料、PII/密钥/评审目标、把已签`D1_DEV_ONLY`自动改写为已有第三方授权、任意连接可疑host/region、无账号密钥、资金无底、实际调用越预算、为了结果调整任何科学输入、偷跑新实验或不封存原始响应。

## 8. Options / decision
A【OWNER APPROVED】：精简剩余本地门，仅检查真实数据权/敏感性、北京Workspace/可用密钥/受控预算余额和单个最高风险费用情景；C改为逐格后置真实usage、先原序前三格工程成功再余105，已批准全批且完成即STOP。
B【NOT SELECTED】：等待同模型服务端完整tokenizer/chat模板证明，周期未知且非本次科研问题。
C【PROHIBITED】：跳过外传权限与现金风险、偷偷换模型、伪造费用或role-free标签、取消发送事务/停发。

## 9. Owner recommendation
执行A。独立Checker只验证**必需**门，不再要求16/29/46份每份独立手签、每个旧收据对应当前正式账单或全部108逐格精确事前tokens；避免“证明不可能”即永久STOP。对46文档**一次联合范围审查**：15法律规范文本按属性评估，2网页解释检查额外限制，29签署开发候选识别真实创作者/现有许可。Owner本次指示“进行真实研究验证”可作为**其自己控制的项目材料**面向已恢复北京百炼Workspace的研究用途指令，但不能取代任何确知的第三方限制/第三方权限；已知不允许、隐私/秘密或来源严重不明一律在发送前STOP，不得偷偷删除/替换样本。剩余权限未知可出具**一个清晰最小Owner事实声明**而不复审全46。

## 10. Confidence and interpretive limits
冻结与离线工程高置信，后置usage的首次越界经济风险小但非零，Chat模型实际成本/协议须实测。36世界由12事实组相关构成，单例8.33pp，不能证明2.5pp门或正式targetedASR；评价仅后封存独立开发暂定一致性，HumanGold0、target未知、C3/正式QA NOT_MEASURED。

## 11. Authorization details: permitted execution / minimal gates
**本Owner12是一次性受限真实运行的先验授权**，不要求首3成功后再次征求Owner；若所有硬门在本机可核PASS，Codex可**立即**按原序执行。
1. A（最小合法外传）：只发送既有冻结108格system/question/retainedTopK到同一受控北京百炼Workspace；检查46源来源索引已全对应、scope为这一次研究验证，确认29候选的创作/许可或Owner有效处理授权、2官方网页的使用范围，以及上下文敏感内容/PII/密码；已知禁传或无法作出必要权利声明不得发。以一条组合的D/E受控范围声明+SHA对应所有46源，不必46签；不传额外raw whole docs、标签、参考、GT或财务信息。
2. B（唯一实际目标）：从历史封存恢复`cn-beijing` Workspace专属URL（不得打印WorkspaceID），官方host allowlist/region与当前API密钥归属匹配；仅POST`/compatible-mode/v1/chat/completions`，TLS证书校验、代理/redirect/SDK重试禁用、不加额外探测；请求模型仍是固定快照，V2唯一输出字段维持。首次响应若模型/usage不匹配STOP。
3. C（明确放宽）：完全取消“发送前108条严格<=4096证明”的准入要求，保存全部原wire的byte SHA与统计；每次返回必验`usage.prompt_tokens`，若>4096（含缓存前完整prompt）或usage缺失，**将本格记为已调用异常并立即STOP**，不能根据它重选样本或补跑。第一次超界发送/费用可能已发生，明确为Owner接受的开发阶段风险。单请求最多用该模型官方最大输入991808 Token与更高价档估计“**一个最大越界请求**”的成本，以未完成107格至多4096加一格最多991808的结构预留预算，严格串行、收到usage后再发下一格。
4. D（现金硬门，优先简化）：从已有历史361账单和Owner自核当前账户/余额/费率复用D/E私有数值/可用资金；如正式账单当日不可取，可用有来源的官方北京高价档上界+明确记入历史未结算和Owner当下有界账户承诺构造保守USD上界，不强制上交公开截图、逐单发票或完美FX表。预算必须覆盖正常108格及**一次最大越界请求**、V2候选266输出/次、>=20% reserve、失败在途，整体`settled_usd + pending_usd + batch_reserve_usd < 28`且账户剩余额度覆盖；>=25警戒、>=28不发新的任何请求，USD30累计不越。可增加本Pilot私有批次成本硬限，但不能削弱原门。**数字缺失或账户支付能力不明时仍不得发送**；不把未来费用当作0。独立Checker同时验证序列、实际用量、实时扣款上界、上一请求未结算预留、首错停止。
5. E（实际可启用的代码）：将旧`LIVE_AUTHORITY_SHA256=None`升级为对**本Git已批准Owner12决策文件实际SHA256**的检查+该文件所明确授权的V2/模型/36世界/108格/输出D/E与冻结输入SHA；配套建立run-time`RUN_ADMISSION_MANIFEST`来锁最终可执行源码hash、D/E私有范围声明hash/预算/账户region/本轮108请求SHA/输出目录。该Manifest由独立Checker签发通过/失败状态，**不伪造Owner对未来未知hash已经逐字签名**；Owner12明确委托Checker对事实边界核验后执行已批准范围，不能由Agent随手写一个PASS替代验证。要求checker测试既可在合成全PASS下到达真实发送代码，也能够在任一缺项时物理拒绝联网。仅修复运行解锁/Checker/token过度门，无其它模型/科学路径更改。
6. 已合规准入时，执行原序前3格，每格先落`send_intent`持久证据、单发、核模型/usage/output≤266与JSON/schema/finish reason/实际费用/原始输出hash及硬停；三格工程均通过，自动继续同一次4–108，**不依据正确性筛选/不读取暂定参考**。任何HTTP/计费/回包/硬限/泄漏/文件系统异常STOP，剩余`NOT_RUN`不补跑/不重试。静态不变的后端代码不得单凭\"--live\"或密钥环境变量偷偷开启。
7. 全部请求或停止后立即封存原始响应、HTTP和每格usage、费用、受控raw与全108槽状态，摘要/各Hash只提交5060分支，参考JSON只在生成封存之后交独立D1开发Evaluator计算`PROVISIONAL_REFERENCE_CONSISTENCY`和拒答/成本，非正式ASR/Answer Accuracy。不得启动D2/D3/GT/5090Claim、算法B5/B6或新样本和额外模型请求。

## 12. STOP and evidence delivery
本授权只允许**一次**V2 Pilot12真实序列，首次HTTP后不得再自行重发第一格或重开批次；任何未能闭合的**真实前置数据权或预算**，明确输出`RAPID_LIVE_BLOCKED_MINIMAL_ACTION_REQUIRED`并附**最多一个具体Owner声明/数据值缺口**，其余工作不重做。不把strict tokenizer证明或“未匹配source hash”当阻断理由。合法完成若108格`RAPID_LIVE108_COMPLETED`，首三格停`RAPID_INITIAL3_STOPPED`，中途停`RAPID_PARTIAL_STOPPED`。报告真实请求数/usage/CNY和USD核账/异常/答案暂定一致性（如可隔离）、SHA和Git自分支clean/0:0；实验完结提交push并STOP。历史证据只读保留，5090无变化。
