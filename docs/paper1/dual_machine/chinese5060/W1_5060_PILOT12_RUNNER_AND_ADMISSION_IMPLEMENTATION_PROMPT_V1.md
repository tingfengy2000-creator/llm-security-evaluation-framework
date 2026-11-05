# 5060 Codex｜Paper 1 Pilot12 真实端到端RAG运行器实施（仅本地/Mock，无API请求）｜完整执行 Prompt V1

**这是 Git 内的完整最终指令，不依赖ChatGPT网页附件。** 分支只能是`research/paper1-chinese-defense-5060`，Owner十二字段授权`W1-OD-20261105-5060-RUNNER-PREFLIGHT-09`，原件`docs/paper1/dual_machine/owner_approvals/W1_5060_RAG_PILOT_RUNNER_IMPLEMENTATION_AUTHORIZATION_20261105.md`，其登记提交`93a9e301427376e9ac84d44a8d13369643026c4e`。起点应包含旧Pilot设计最终SHA `bbfda7ddd9fe820b908639c7943daef6c87cec6d`。

**本次批准的是：实现 API Runner + 离线 Mock Test + Token/预算/准入检查 + 下一门审批包。不是批准调用真实百炼、免费试探或运行108格。**
Owner已自行核实模型、账户地域、真实价格与余额。这是`OWNER_ATTESTED`，**不要重复索要账户信息/截图或要求Owner先做Formal Gold**；实测账本/数值闭合未出示时可继续实现，不要假设为已量化验证或免除USD30费用门。

## 0. 上下文恢复与严格范围

1. 完整执行`AGENTS.md`指定的 Context Recovery、PO-MHEP、`FORWARD_RISK_REVIEW`及`PAPER_RISK_REVIEW`；按规定阅读权威映射、状态、Owner决策、长期要求、Experiment Master、研究路线、Research Execution Log和最近15个commit；先做`git fetch --prune --tags origin`/`status`/`branch`/`rev-parse`/`log -15`和upstream状态；仅可clean/upstream一致时`pull --ff-only`。未知修改或非预期branch STOP，不得stash/rebase/reset/merge/cherry-pick/force push。
2. 冻结原 P2 `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`、PAIR01 `bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb`、既有 Pilot Proposal SHA256 `0aaf4cfb28dc1e7d9fea8fcdc8f7143afd56857fa300f8b6e3f8f9d0ff081cb6`、system prompt hash `b3c74613bc3700eacdce7dfedc382043013f452e321a13d8639b27817edbd1f1`。原评价参考JSON `5c5f212ba16da97b114d897de910ab383a47d96db4cb7cd9b54e638f7f03cf31`仅保留D/E受控评价侧；绝不进Generator输入或公开Git。
3. 仅36固定世界×G0/G1/G2，共108格；每格1个计划请求，80唯一prompt_hash不得合并格/复用输出。命令行不得自动追加重试、Judge或联网“健康探测”。非对称7 MISS以及Poison/Clean/HN条件29保留；冻结样本/索引/查询/TopK/Filter输出不可更改。原Fast-C Stage内部因果UNRESOLVED和B2 Clean误删升高保持，不在此轮补采。
4. **新项目文件/日志、临时及缓存仅D/E，C盘禁受控写入**；20GiB余量阈值。令执行必须显式传入受控`--output-dir`在D/E，防止Python/__pycache__/Windows TEMP/SDK缓存偷偷写C；仅已存在依赖，不新增安装/下载/环境迁移/driver changes，不触碰5090分支/Claims。

## 1. 最小代码实现（不是科学试次）

允许在`src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/`添加独立、可替换的`pilot_runner`、配置/preflight、transport接口、usage/costledger、封存工具；CLI在`scripts/research/run_chinese5060_minimal_rag_pilot.py`；测试在`tests/research/`。不要修改RAGDefender上游、b12.py、旧P2/PAIR01、任何已封存文件或评价参考。
- **DRY_RUN/FAKE模式是唯一可实际执行的模式**：执行开始前物理禁止公网、断言Transport为`FakeTransport`且不会引入任何真实DashScope client；用虚构响应模拟108格生命周期、示范完整封存。设置明确`LIVE_NOT_AUTHORIZED`硬门：没有未来全新Owner执行审批清单和签名/哈希/预算准入，真实transport构造就抛异常，不能仅凭`--live`或环境变量开启。真实HTTP接口可作为不实例化/静态类型的抽象适配层实现；若需要导入SDK发生登录/网络，先STOP而非试。
- **请求编码**：读取冻结角色盲私有input计划的hash，生成器仅接收同一system文本、原query、保留原TopK rank及chunk文本；确认绝不包含role、attack goal、expected、provisional reference/Reviewer/GT。维持已冻结`qwen3.7-plus-2026-05-26`字面模型，`temperature=0`、`top_p=1`、禁thinking/search/tools、非stream、输出JSON `status/answer/citations`、输入4096与输出256为候选硬上限；Provider字段未知只能记录`WIRE_UNVERIFIED`，不得改模型、prompt或参数来凑SDK兼容。
- **token gate**：只可使用已存在、已经核对身份与版本的本地离线tokenizer，对所有108个完整chat-template输入做确定性计数；或提供静态上界方法及`INEXACT/UNKNOWN`标签，不许把UTF-8字节+512代理量叫作精确计数。若需Provider`count-tokens`服务器API（即便免费）或下载Tokenizer，必须另批，不能在本轮发送。设计精确门失败时保留`TOKEN_GATE_BLOCKED`；不得截断、重写或删片段。
- **成本/账户**：读取本地受控脱敏配置；Owner已核实模型/地域/费率/余额的声明只标`OWNER_ATTESTED`，不强迫提供敏感截图/密钥。实现`max_calls=108`、整批最坏费用预留、实时usage/cached/hidden fields及累计账本核算与单格熔断，采用旧`USD30 cap / 25 warn / 28 no new batch`，含全工作线旧费用及差额不抹除；价格/FX/未结算项无证明时`BUDGET_GATE_BLOCKED`，继续交付代码，但不运行真实请求。
- **停止语义**：并发=1、自动SDK重试=0、人工重试=0、额外Judge=0、额外探测=0。空上下文只在Future条件下按冻结策略本地ABSTAIN；任一timeout/HTTP模型/usage/response schema/Token/费用/字节漂移或权限错误均保存失败证据与尚未运行格为`NOT_RUN`，STOP，不自动续跑。fake错误响应不计真实API/费用。
- **封存与隔离**：future输出全部108格成功/失败/NOT_RUN及Raw Response Hash/Run Manifest/usage/异常、不可变密钥脱敏记录；在真实全部输出锁定后才可能由独立开发Evaluator读私有参考与D1标签。Never mix Generator and Evaluator roles;不将C3或targeted ASR写为实测，HumanGold0。
- **假数据测试覆盖**：exact SHA drift/108 grid/80 unique hashes、重复prompt不去重、无法构造live、错误响应JSON/引用/空输出、超4096、超USD预算、费用历史差额、unknown模型返回、missing usage、停止后格状态、mock无外网、C写入防护、缓存/环境路径、评价不能提前读reference。测试必须可在物理断网环境运行。

## 2. 一次性Run Admission Packet（本轮只准备）

生成清晰的`OWNER_LIVE_RUN_APPROVAL_PACKET.md`，不新增不必要审签文书：本次具体代码/manifest/full SHA、原proposal/input、模型/账户地域证据等级、wire真实字段、准确token/未知说明、整批最大费用和历史统一账本、实际USD硬上限、预警/停止、无重试、108请求和后封存独立评价，明确每个`PASS / OWNER_ATTESTED / UNKNOWN / BLOCKED`。待下一次Owner批准**真实生成**的指令需有单独审批编号和实际可执行命令。任何账本或Token不能闭合的情况下仅提交`IMPLEMENTATION_READY_EXECUTION_BLOCKED`，不能假称`EXECUTION_READY`。

Owner已经说账户型号/地域/费用/余额本人核实了：仅确认必要的本地manifest字段，不额外索取账户截图或token；可以给Owner一段最简待确认数值模板，但若无法自动得出，也不因此阻碍当前代码和Mock完成。

## 3. 输出、质量和Git收口

新主报告：
`docs/paper1/dual_machine/chinese5060/W1_5060_PILOT_RUNNER_IMPLEMENTATION_AND_ADMISSION_REPORT.md`

目录`docs/paper1/dual_machine/chinese5060/pilot_runner/`至少有：
- `OWNER_LIVE_RUN_APPROVAL_PACKET.md`
- `PROVIDER_MODEL_TOKEN_BUDGET_GATE.json`
- `DRY_RUN_AND_QA.json`
- `SECURITY_PRIVACY_RESOURCE_AUDIT.md`
- `FAILURES_AND_BLOCKERS.json`、`FINAL_GIT_DELIVERY.json`。
必要新接口脚本、单元测试/静态检查/Ruff/MyPy，记录cmd/stdout/stderr/exit、source SHA、mock trace、假usage、没有网络请求的验证证据；私有计划/原文/参考及mock输出留D/E，Git只提交脱敏报告和程序。按AGENTS/PO-MHEP完成Human/Agent ledger、Current State、Research Execution Log及必要的Experiment Master条件评估，只提交push本5060分支，回报full HEAD、远程一致性、working tree clean、ahead/behind 0/0。

**结束后 STOP。结果必须记：`RUNNER_IMPLEMENTED_LIVE_NOT_AUTHORIZED` 或 `PREFLIGHT_PARTIAL_BLOCKED`；本轮真实API calls=0、新付费=0、108真实生成=NOT_RUN、HumanGold=0、Targeted ASR/正式QA=NOT_MEASURED。无下轮真实Owner批准不得启动任何108格或单次真实调用。**
