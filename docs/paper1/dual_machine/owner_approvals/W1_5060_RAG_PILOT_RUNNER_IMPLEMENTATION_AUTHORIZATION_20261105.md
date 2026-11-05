# Paper 1｜5060 D1 Pilot12 API Runner 实现与执行准入闭合：Owner PO-MHEP 十二字段授权

- **跨分支唯一 Owner 决策号**：`W1-OD-20261105-5060-RUNNER-PREFLIGHT-09`
- 日期：2026-11-05（Asia/Tokyo）
- 源：Owner 本项目监督对话确认“百炼账户的模型、地域、实际费率与剩余额度我已经核实过了，不用太担心费用问题，你的方案我批准”。
- **决策解释**：批准 **Runner 实现、离线/模拟测试、运行准入资料闭合和最终真实执行申请准备**，不代表授予真实 API 请求或108格实验执行权。该区分与前一轮明确的“两次审批门：先实现，再真实执行”一致。
- 状态：`OWNER_EXPLICITLY_APPROVED / IMPLEMENTATION_AND_LOCAL_DRY_RUN_ONLY / LIVE_GENERATION_NOT_APPROVED`。
- 唯一允许分支：`research/paper1-chinese-defense-5060`；授权前远程HEAD：`bbfda7ddd9fe820b908639c7943daef6c87cec6d`。
- 前阶段Owner ID：`W1-OD-20261105-5060-PROVISIONAL-PILOTDESIGN-08`；已提交设计内容SHA：`abda9c8e4eaa04602c06fae9bfeee17bb9f16258`。此授权不改变5090分支和已有独立审批。
- 冻结设计：`W1_5060_MINIMAL_RAG_PILOT_DESIGN_AND_BUDGET.md`、`pilot_design/PILOT_EXECUTION_PROPOSAL.json`，proposal文件 SHA256 `0aaf4cfb28dc1e7d9fea8fcdc8f7143afd56857fa300f8b6e3f8f9d0ff081cb6`、共同system提示 SHA256 `b3c74613bc3700eacdce7dfedc382043013f452e321a13d8639b27817edbd1f1`，原始12题暂定参考 SHA256 `5c5f212ba16da97b114d897de910ab383a47d96db4cb7cd9b54e638f7f03cf31`（参考正文只留 D/E 评价侧）。

## 1. Issue ID
`W1-OD-20261105-5060-RUNNER-PREFLIGHT-09`。跨机引用必须附branch与完整SHA；不复用不同分支同号的 `PODR-154`。

## 2. Issue name
5060 Paper1 Pilot12：百炼固定模型生成适配器（API Runner）、精确Token准入策略、108格冻结请求清单、费用硬门、脱敏封存与离线模拟验收。

## 3. Discovery stage/task
P2真实检索→B1/B2离线过滤→Fast C只读归因→已完成D1 Pilot12最小查询级RAG设计。下一步是**执行前工程实现和安全准入**，不是数据/模型基线改动或真实生成实验。

## 4. Current facts by evidence class
- `OBSERVED_GIT`：36原世界、三臂108候选格、80唯一prompt_hash、历史TopK/PAIR01封存、暂定参考JSON由前次5060本地验SHA并隔离；Runner未实现、真实Pilot NOT_RUN。
- `OWNER_ATTESTED`：Owner本人已核实百炼账户模型、地域、真实费率、可用额度；目前**未向本研究治理仓库提供精确费率、账户记录、余额或账单SHA**。Owner确认使本次工程实施无需重复索取已确认的基础事实，但不是机器校验的数值预算证明，也不免除既定USD约束。
- `SOURCE_DERIVED`：候选模型字面 `qwen3.7-plus-2026-05-26`，G0原TopK、G1/G2复用旧过滤输出，输入候选4096 tokens/输出256，单次单并发、无重试/无工具/无thinking/无judge；proposal本身不是运行批准。
- `UNKNOWN`：正式请求实际支持的wire字段、当前账号下实际返回model_id/usage语义、是否存在离线准确Tokenizer、全108个模型精确Token、统一USD账本与仍可承受的整批最大预留、Runner实现正确性。
- `NOT_MEASURED`：生成输出、ASR、Answer Accuracy、拒答率、模型时延与实际Token费用。

## 5. Constraints affected
AGENTS.md与PO-MHEP；D1开发身份/私有Evaluator隔离、P2/PAIR01/FastC不可变；固定108格及80唯一Prompt；USD30累计cap/25 warning/28禁止新付费批；2.5pp安全/质量增量（Pilot12 n=12不能证明）；C盘禁新增项目可控内容，D/E储存且保留20GiB；5090独立分支与其许可审批；无自动数据授权、无密钥外泄。

## 6. Why address now
Owner明确要快速进行可行性验证，已经自行完成百炼账户事实核实。前轮设计已封存，卡点集中在Runner缺失、离线验收、Token真实计数策略、账本与硬停合同。先做好执行层可显著缩短下一次真实Pilot审批至开跑之间的间隔。

## 7. Downstream risks
Runner意外真实HTTP/隐式SDK重试/自动联网检查；provider将模型名路由到alias或不同revision；Thinking、JSON响应、max_tokens、usage或缓存账单语义不一致；精确token缺失却把UTF8代理值当精确值；私有事实参考/角色/目标进入生成器；重复prompt导致跨世界复用答案、故障不留全108分母；账本不含其它工作线/失败在途费；环境/临时文件写C；软硬件安装改变其他论文工作线；把Pilot暂定一致性冒充正式ASR/QA。

## 8. Options / tradeoffs
- **A【OWNER ACCEPTED】**：在5060原分支实现最小可隔离Runner、mock transport dry-run、严格准入与冻结证据，记录Owner已核实账户事实，必要预算数字无法本机验证时只列待执行门；不进行真实HTTP。低成本、可逆、对论文方法无扰动，仍需再批真实执行。
- B【NOT SELECTED】只等完整账单/正式Gold再实现；避免工程风险但拖慢可行性，不符合Owner本次推进。
- C【NOT AUTHORIZED】边写边连接百炼/试1次/直接跑108；能较快得到输出，但无执行SHA、模型usage核验、预算和失败封存，违反合同。

## 9. LOCAL recommendation
执行A。**Provider接口与真实网络必须使用显式双门锁**：离线模式始终使用FakeTransport，网络路径在没有独立Owner执行批准及有效manifest时不得可触达。可以离线读取既有的公开SDK文档/依赖metadata和本地已合法存在的Tokenizer；官方在线公开文档只读查询可做，但不登录、不提交model-inference/token-count请求、不下载权重或依赖。原参考只归独立评价侧。用纯虚构测试数据覆盖正确路径与失败硬停。

## 10. Rationale / confidence
Owner许可边界高置信；旧108格及参考哈希经Git可追溯；Runner使用未来平台的具体wire兼容性、Token精确上界与最新可用余额必须在下一执行门由证据或预先批准的保守上限闭合。成本不是当前阻塞实现的理由，但不会凭“别太担心费用”废除USD30/25/28约束。

## 11. Owner explicit choices and unresolved gates
**已批准**：
1. 在本分支按项目新代码规则开发`src/llmguard/`最小生成适配器、`scripts/research/`启动入口和`tests/research/`FakeTransport/零联网模拟测试；可新增运行前preflight、后端接口契约、Token计数适配层、账本/熔断/序列化封存模块、文档与脱敏示例，不修改RAGDefender算法、Retriever或历史源文件。
2. 仅从既有D/E白名单只读冻结108格计划、角色盲TopK、B1/B2历史输出，核旧 SHA；可对**既有消息字节**进行本地确定性格式编排/哈希与离线Tokenizer统计（仅若已合法安装，不能为此下载模型或依赖）；不能重检索、重运行Guard、修改消息/样本或参考。
3. 实现纯离线Mock测试（包含成功、非JSON、usage缺失、账号/模型返回不符、超4096 token、超费用/出错、timeout、SDK retry=0、后端隐式网络禁用、停后保留全108结果、空上下文、重复prompt独立格、输出/score严格隔离、C盘禁新增可控字节等）。应证明`DRY_RUN`过程中没有真实网络请求；严格区分Mock usage与实测usage。
4. 准备真实价格/预算核验的**本地、脱敏、可计算入口**，允许Owner已核实事实在受控D/E账本作简短`OWNER_ATTESTED`记录；不用要求用户重新提供同一账户材料、凭证或余额截图。本次没有数值凭证仍可提交Runner代码，但不得让程序自动解除live批准门。维护全工作线费用历史差额、不重置USD30/25/28阈值。
5. 不改变已确定三臂实验输入与评分参考：G0/G1/G2、原36世界、100%全分母与29条件分母、原prompt SHA、候选模型名、参数、错误/拒答政策和AI暂定参考；任何确实需要改变模板/参数以适配wire，先STOP提请Owner明确是否修订设计。
6. 全量验证后提交可由Owner **一次性确认真实Pilot** 的Run Admission Packet：冻结Runner Git SHA、源码/配置Hash、SDK版本与wire、模型/地域/账户有效性证据等级、108格实际精确Token及计数工具身份证据（或未满足注明BLOCKED）、最大USD成本/整批保留、无重试/无judge、完整封存和可恢复停止政策、私有数据隔离与一份`NOT_APPROVED`真实运行命令；准备执行申请，但不得自动开启。

**本次不批准**：
- 任何真实模型/API请求（包括“免费”、1-call smoke、count-tokens、余额接口、账号连接探测）、真实模型Tokenizer/权重下载、新pip/conda安装、模型自动fallback、付费账单、外部上传私有输入、任意科学实验输出；
- 原样本/查询/TopK/检索/Guard/参数/模型、PAIR01运行、B5/B6、D1-40、新数据集D2/D3、Reviewer/GT Vault/T1T2/C3正式评分、5090 Claim运行、跨分支改动和主线合并；
- 由Agent签署HumanGold、推断/虚构攻击target，或将AI provisional correctness说成正式QA。

## 12. Allowed/prohibited until Owner execution gate
只准实现、静态验证、FakeTransport模拟、既有消息的本地离线Token审计、审批包、D/E脱敏归档、本5060分支Git commit/push和治理closeout。涉及首次真实请求、SDK隐式联网、tokenizer缺失需要安装、无法证明账本硬门、模型/参数/分母变更均须STOP并按PO-MHEP十二字段升级。无论是否准备就绪，完工`RUNNER_IMPLEMENTED_LIVE_NOT_AUTHORIZED`或`PREFLIGHT_PARTIAL_BLOCKED`后STOP。

## Exit / expected artifacts
- `docs/paper1/dual_machine/chinese5060/W1_5060_PILOT_RUNNER_IMPLEMENTATION_AND_ADMISSION_REPORT.md`
- `docs/paper1/dual_machine/chinese5060/pilot_runner/OWNER_LIVE_RUN_APPROVAL_PACKET.md`
- `docs/paper1/dual_machine/chinese5060/pilot_runner/PROVIDER_MODEL_TOKEN_BUDGET_GATE.json`
- `docs/paper1/dual_machine/chinese5060/pilot_runner/DRY_RUN_AND_QA.json`
- `docs/paper1/dual_machine/chinese5060/pilot_runner/SECURITY_PRIVACY_RESOURCE_AUDIT.md`
- `docs/paper1/dual_machine/chinese5060/pilot_runner/FINAL_GIT_DELIVERY.json`
- tests+Ruff+MyPy（及环境已有适用静态检查）、私有模拟日志和哈希、PO-MHEP closeout。须报告机器实际head、commit SHA、remote clean与STOP；**没有Owner新的显式真实执行审批不出现真实RAG生成输出**。
