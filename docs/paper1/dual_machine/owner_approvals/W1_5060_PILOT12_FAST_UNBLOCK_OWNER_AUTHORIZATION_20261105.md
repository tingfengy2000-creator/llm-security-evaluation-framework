# Paper 1｜Pilot12 Fast-Unblock 一次性零调用解阻授权（PO-MHEP 十二字段）

- **跨分支唯一 Owner ID：`W1-OD-20261105-5060-FAST-UNBLOCK-11`**
- 日期：2026-11-05 JST。
- **授权状态：`OWNER_APPROVED_FAST_UNBLOCK_OFFLINE_ONLY / LIVE_API_NOT_AUTHORIZED_BY_THIS_DECISION`**。
- 授权原话：Owner明确批准5060“进入一次性Pilot12 Fast-Unblock解阻阶段”，仅在其原研究分支核实D1冻结外传范围及来源使用权，完成百炼唯一地域端点配置和真实传输**正向放行路径的代码及离线测试**，建立108格可信Token严格上界与机器可核USD账本；可专项审议由`max_tokens=256`改为`max_completion_tokens=256`，**仅在证明确有必要且唯一变更**时实施，记录公平性、重新冻结108格和预算及独立离线QA。**明令禁止任何真实API/网络模型探测、其他科学资产/参数变更、D2D3/5090操作**。
- 唯一分支：`research/paper1-chinese-defense-5060`；授权前 HEAD：`731b48419aba2dab3b8ded310d349fcf441c3f1b`。此前实际真实生成0、108格NOT_RUN、费用0，状态`LIVE_GATE_BLOCKED_NO_REQUESTS`；本授权不虚构后续已运行。
- Previous Owner conditional live approval：`W1-OD-20261105-5060-PILOT12-CONDITIONAL-LIVE-10`。**本次Fast-Unblock独立于此前运行权**：即使修复并获得离线全PASS，也**仅交付下一次Owner真实执行审批的单一证据包并STOP**，禁止自动援引Owner10启动108请求。若输出上限字段改动，原proposal SHA、108实际wire SHA相应变化，Owner10对旧manifest的绑定不可直接沿用。

## 1. Issue ID
`W1-OD-20261105-5060-FAST-UNBLOCK-11`，跨双机引用用 OwnerID + 分支 + full Git commit SHA，不借用冲突的本地PODR-154编号。

## 2. Issue name
5060 D1 Pilot12：A外传权利与隐私、B唯一百炼地域和输出限制、C精确或严格有证Token界、D完整数值美元预算、E受审正向放行的**一次性解阻工程**。

## 3. Discovery stage / task
Fast B/P2旧封存36世界；B0/G0原TopK、B1/G1、B2/G2既有过滤输出；108格计划、80唯一prompt hash。Owner10已条件批准但前置证据不全，最新5060提交`731b48419aba2dab3b8ded310d349fcf441c3f1b`合法STOP：API POST0、108 NOT_RUN、46 tests/ruff/mypy通过。当前目标是解除静态执行阻断，**不重做研究设计、不运行真实Pilot**。

## 4. Facts by evidence grade
- `OBSERVED_GIT`：`docs/paper1/dual_machine/chinese5060/W1_5060_PILOT12_CONDITIONAL_LIVE_RUN_REPORT.md`及`pilot_live/ADMISSION_GATE_MATRIX.json`记录A–D未闭合、E仅完成拒绝路径；108个原问题/TopK/排序与旧seal一致、四类有限模式敏感扫描0命中不等于正式隐私审计。
- `OWNER_EXPLICIT_APPROVAL`：允许唯一字段条件修订（不是要求一定修订），前置合法性和计费/Token证据检查、修复代码并本地模拟；真实模型/API请求不获授权。
- `OFFICIAL_PUBLIC_DOC`：百炼官方`OpenAI-compatible Chat` 2026-07-15 文档：`max_tokens`限制answer且将弃用，`max_completion_tokens`覆盖thinking+answer并支持Qwen3.5-Plus及后继Qwen Plus，实际输出计数可能与设置值最多相差10 token；关闭thinking可用顶层`enable_thinking=false`（原生HTTPS而非SDK extra_body）；官方有区域/WorkspaceId专属URL。参考 `https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions`。此为接口文档事实，不是账号级成功响应。
- `OWNER_ATTESTED`：Owner本人已确认模型/地域/真实费率/余额，未在公开Git披露具体数值；保留这一证据级别，不向用户索要密钥/重复截图。
- `UNKNOWN`：16个冻结来源各自允许的第三方传输范围及敏感信息分级、实际账户和Workspace的唯一地域host、请求字段在固定模型的wire/usage真实行为、全108聊天模板的严格Token界、统一全工作线USD已结算/在途/FX/余额及真实批次预留。本次若无法用受控材料证明，则如实`PARTIAL_BLOCKED`，不得编造。

## 5. Constraints
AGENTS.md / PO-MHEP、旧D1数据边界、旧P2/PAIR01/FAST C源文件和不可变seal、Human Gold0/target未知、独立Evaluator、原36世界×3臂、原prompt模型及temperature0/top_p1/disable-thinking/search/tools/JSON/n=1/zero retry、C盘受控零新写、D/E≥20GiB余量、USD30总上限/25预警/28禁新批、2.5pp质量边界、5090独立分支与D2D3封印。

## 6. Why now
预检反复因为同一批机器准入缺口在首格STOP。Owner要求缩短可行性Pilot实施周期，仅做一轮集中修复和单包结案，不再把五门拆成额外研究方案或多级非必要文书。

## 7. Downstream risks
将“零敏感正则命中”冒充全面PII/权利许可；把自行创造的授权用于第三方传输；把纯UTF8长度代理当Qwen精确Token；将`max_tokens`与`max_completion_tokens`混为同一run/hash；令多臂差异源于提示词或模型变化；缺历史未结算和外币换算时造出低价预算；修复真实传输放行时提前连接/试探；把模型调用计为已授权；将私有问题、来源快照、答案与标签提交公开Git。

## 8. Options and impacts
A【OWNER APPROVED】：只针对A–E缺口开展**一次静态/本地解阻**、条件只修订唯一输出上限字段、重新冻结全部108 wire请求并制作单一证据包。成本新增API=0；代码和证据可审，可逆；下阶段另批真实执行。
B【NOT SELECTED】：对A–E分别多轮审批与重复复审，会推迟D1 feasibility但不增加实验证据。
C【FORBIDDEN】：直接跑1个smoke、使用线上count-tokens、盲猜地域、改科学输入或缺预算就开真实108；越权且不可复现。

## 9. Recommendation
执行A并控制阻断：对每门只用可检查证据和简短原因，不做新的文献/基准或方法研究。优先评审单字段是否必要；若要改，保留旧V1只读，另生成`V2_SINGLE_FIELD_OUTPUT_CAP`且证明全部108格**只有这一字段不同**、原query/chunks/system/model不变，新的逐格request SHA/new proposal/version/预算分别锁定。绝不在缺外传权限等情况下假造全PASS。

## 10. Rationale and confidence
本授权范围与远程旧报告可明确支持；关于`max_completion_tokens`的官方公开能力信息中高置信但实际账号/region不能通过本次调用实测；未解决数据源许可、Token、账本时必须维持真实0调用。Pilot12样本小，任何正式ASR、Accuracy与2.5pp统计合格断言均禁止。

## 11. Explicit Owner decisions; allowed work and invariants
**批准**：
1. 5060只在现有独立远程分支进行Context Recovery、Fast-Unblock A–E的静态元数据/源码/授权文件检查，建立最多16个冻结来源的来源级使用权、必要出处、第三方模型处理地域和所需用途的`SOURCE_TRANSFER_RIGHTS_MATRIX`。区分Owner有权使用、第三方转交是否被允许、PII/敏感性检查；未知保留，不能因为前轮四类正则0命中或仅是公网上下载就授予权利。可让Owner用**一个短的缺项问题**后补，但不阻碍其他工程工作。
2. 依官方只读公开文档+已有的Owner账户地域attestation，在D/E受控私有配置内冻结一个唯一合法百炼区域端点+Workspace关联（若缺Workspace标UNKNOWN），不臆造域名/WorkspaceID。完成窄HTTPS独立transport、授权manifest与validator**正向放行代码**，保持默认fail-closed；用模拟TLS/Socket/fake transport/假账本和严格双门锁覆盖PASS/FAIL，绝不连接真实服务。
3. 仅使用已合法存在的本地Tokenizer、官方离线计数资料或可验证严格上界推导，记录具体chat template/wire消息和版本/输入chat framing，对108格逐格输出严格token上界、证明/限制/工具hash；不接受`UTF8 bytes +512`的旧代理冒充严格上界，不能为此下载/安装Tokenizer或发在线count-tokens。若不能在本轮可信证明，则`TOKEN_GATE_PENDING`且只交付不假PASS。
4. 在D/E受控私有账本按已有费用来源、Owner核实的费率/地域/余额、未结算、FX和历史费用差额填写数值/上界并hash锁定；执行USD30 cap、USD25 warning、USD28不得新批、全108上界和>=20% buffer，受控私有可计算预检，不能虚构数值/模型费用或把Mock费用当实账。若Owner尚未给数字可列一个最小信息缺口；绝不将账户凭证写入公开Git。
5. **唯一允许的科学配置候选变化**：在**官方文档或严格计费证据证明原`max_tokens=256`不足以控制完整输出/计费且改字段是必要时**，可把该字段**只**改成`max_completion_tokens=256`；必须删除原`max_tokens`键，不共存、不改值，不改其他字段。生成新冻结proposal及全部108格request/manifest SHA、记录变化前后比对与配对公平性、输出上界计入可能10 token偏差（例如<=266仅作为文档容差候选，实际账单仍需严密核对）、重新计算整个批次Token/cost/Hard STOP，审视256是否导致JSON截断，绝不自动抬cap。若不必要则保持原V1和`NO_CHANGE`；若需改别的参数，`OWNER_NEW_DECISION_REQUIRED`、STOP这一子项，不继续推衍。
6. 实现受审真正PASS准入后的**本地可执行路径的代码**（`send_intent`先持久、一次HTTP、响应usage与单格真实费用结算、首3个协议检查、4–108门控、异常停发和全108状态封存）及独立本地checker，使用完全虚构数据完成正反模拟；测试应证明在**本次Fast-Unblock审批状态**下，即便假数据所有A–E PASS，`--live`也无法真实发送，不能借旧Owner10或自行生成签名绕过未来Owner Gate。
7. 单独、单一`FAST_UNBLOCK_EVIDENCE_PACKET`（带public脱敏摘要+受控private manifest哈希索引），供下次Owner**一次审批**。分出`PASS/BLOCKED/OWNER_INPUT_REQUIRED`，列未完成项目、方案V1/V2身份、请求hash、model/token/预算/transfer/transport/QA/run lock。必要的独立离线QA、测试、Ruff、MyPy、脱敏/风险治理检查后，合法Git commit/push仅5060分支且STOP。

**禁止**：任何真实模型API/HTTPS POST、免费1-call probe、账号API、count-tokens API、SDK静默联网、下载/安装新模型与依赖、调整其他科学参数、重选样本、重检索/重跑B1B2、修改prompt/system或上下文/chunk顺序、修改角色映射、将参考答案传给生成器、D1-40、D2D3/Reviewer/GT Vault、T1/T2、B5/B6、5090实验/Claims、跨分支/主线合并、对旧proposal/原始seal覆盖写入。

## 12. STOP / next decision
真实API总调用=0是本任务验收的硬约束，不能在任何预检全PASS后直接自动运行。若单包完成`FAST_UNBLOCK_READY_FOR_OWNER_LIVE_APPROVAL`，仅表示离线硬门有充足证据待Owner复核；若仍缺任何门，则`FAST_UNBLOCK_PARTIAL_BLOCKED`并写单独、少量Owner补充项，不因未知把已完成工程丢弃。
**下一Owner Gate**：必须有新明确决策，至少绑定最终源码/commit、旧V1或修订V2的proposal+108请求SHA、可查模型接口/严格Token/外传权利/数值账本、私有证据SHA与运行授权manifest，才能启用真实3+105。该决策需明确覆盖V2（若改字段），旧Owner10不能在配置改动后独自触发真实请求。

## One-packet delivery
- `docs/paper1/dual_machine/chinese5060/W1_5060_PILOT12_FAST_UNBLOCK_RESULT.md`：简明状态与科学边界；
- `docs/paper1/dual_machine/chinese5060/fast_unblock/FAST_UNBLOCK_EVIDENCE_PACKET.md`：**单一**Owner入口，包含A–E门矩阵/来源/Hash/子项PASS-BLOCKED/Next decision；
- `.../fast_unblock/FAST_UNBLOCK_MANIFEST.json`：脱敏可机器核验索引；
- `.../fast_unblock/UNIQUE_FIELD_CHANGE_DIFF.json`：V1→V2前后唯一字段差异、108请求hash/Fairness（未改时显式NO_CHANGE）；
- `.../fast_unblock/FINAL_OFFLINE_QA.json`：源码/测试/独立模拟计数、零网络与合规；
- 私有D/E权限/账本/Token/端点/108请求与签注的SHA清单，Git禁止原文及凭证；必要的Owner决策登记册/Current Work State/Research Execution Log仅**追加当前最新状态**，旧历史不可篡改。
