# 5060 Codex｜Paper 1 Pilot12 FAST-UNBLOCK 一次性解阻执行合同 V1

> **完整的 Git 原生执行 Prompt。立即执行已授权离线工程修复，但所有真正百炼/其他 API 调用始终为 0。不要重做研究方案，不要再建立多轮审批文书。**

**Owner 唯一授权：`W1-OD-20261105-5060-FAST-UNBLOCK-11`；十二字段授权原件：**
`docs/paper1/dual_machine/owner_approvals/W1_5060_PILOT12_FAST_UNBLOCK_OWNER_AUTHORIZATION_20261105.md`，
登记授权 Git commit `82dcd7c77854dc7b85eac5074db5669cd04ad0e0`。
唯一分支`research/paper1-chinese-defense-5060`，授权前HEAD `731b48419aba2dab3b8ded310d349fcf441c3f1b`。

## 0. 执行顺序与安全边界

先从AGENTS.md读取所有12个Canonical Context Sources、项目Owner主权/PO-MHEP、Forward/Paper Risk Review、实验主表及最近15个Git commit；核 `git fetch --prune --tags origin`、`git status --short --branch`、`git branch --show-current`、`git rev-parse HEAD`、`git log -15 --oneline`及upstream。仅clean & linear fast-forward可`pull --ff-only`；不stash/reset/rebase/force-push/merge或cross-branch。若branch偏离、非预期本地修改或权限不符STOP。

强制恢复原科学对象和sha：
- D1 Pilot12 **12事实组×Poison/Clean/HN=36世界**，固定world及臂G0原TopK5、G1原版B1、G2中文Embedding-B2，合计108请求槽，80个唯一prompt_hash，**不跨格复用**；
- 旧P2原TopK seal `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`；PAIR01 seal `bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb`；原方案V1 SHA256 `0aaf4cfb28dc1e7d9fea8fcdc8f7143afd56857fa300f8b6e3f8f9d0ff081cb6`；私有旧108生成计划 `7db82812f893fc0384b2896c98bb5c779504e19a5c45a097945962e840999c96`； system `b3c74613bc3700eacdce7dfedc382043013f452e321a13d8639b27817edbd1f1`；
- 最新被阻断报告 `docs/paper1/dual_machine/chinese5060/W1_5060_PILOT12_CONDITIONAL_LIVE_RUN_REPORT.md`、 `pilot_live/ADMISSION_GATE_MATRIX.json`，状态`LIVE_GATE_BLOCKED_NO_REQUESTS`，真实0 POST/108 NOT_RUN；不可覆盖旧报告/锁封；
- 暂定JSON SHA256 `5c5f212ba16da97b114d897de910ab383a47d96db4cb7cd9b54e638f7f03cf31`只存在评价侧私有D/E，**Generator/Transport/Unblock Agent不得读取其事实答案或标签映射**。HumanGold0、target UNKNOWN、C3与正式ASR/QA NOT_MEASURED。

**本轮禁用一切真实API请求**：真实Chat Completions、免费1-call、count-tokens、余额、身份探测、隐藏SDK下载/telemetry都不准。不得安装或下载模型、依赖、Tokenizer；不得改模型、query、TopK、chunk、prompt、排序、embedding、过滤参数、检索/Guard算法，不读D2/D3/Reviewer/GT Vault；不改5090分支/main。只允许D/E盘受控项目写入，临时/缓存/日志也在D/E，保留>=20GiB可用余量。

## 1. Fast-Unblock A｜一次完成来源与外传资格

基于 **已有**12题/16源/36世界/108完整请求的私有role-free来源索引，出一张简单`SOURCE_TRANSFER_RIGHTS_MATRIX`。每个来源记录`source_hash/source_authority/origin/license_or_usage_basis/intended_processing_scope/third_party_processor/alibaba_region/PII_and_sensitive_result/approval_evidence_hash/decision`，允许结果 `PASS / BLOCKED / OWNER_INPUT_REQUIRED`。
- 先检查已有授权、许可条款、来源网页meta/license、数据是否用户自有/合成/公有领域、仅内部研究许可是否覆盖第三方推理。不可把公开可浏览=允许随意提交模型，也不可要求每个公开法规页面都另行申请许可；根据原文和适用条款记录合理、可证结论。
- 对**实际108条消息中可能发送的内容**进行PII/秘密/授权范围审查，原4类正则0命中只是有限筛查，加入上下文人工可核的高风险审阅路径；不向其他第三方发送原文进行审查。处理方/区域须匹配Owner已核实的百炼账户，workspace ID或端点有缺不编造。
- 输出权限和敏感性**只放D/E私有**，公开Git仅汇总/source hash/决定及短缺口。若一条来源无合法传输证据，应标`OWNER_INPUT_REQUIRED`并将整批Gate标BLOCKED，**不得静默删片段或把它从108格中排除**。

## 2. Fast-Unblock B｜真实传输正向代码与唯一参数可选修订

1. 从官方公开文档**只读**核百炼指定region唯一Host/WorkspaceID格式、固定快照`qwen3.7-plus-2026-05-26`、`enable_thinking=false`、`response_format={"type":"json_object"}`、官方TLS/HTTP响应和usage计费标准。Owner已核账户/地域/资费/余额无需重复索取截图，但机器实际Workspace/完整host不在本机时写`OWNER_INPUT_REQUIRED`，绝不从IP/Timezone/源码URL猜测。官方说明参考 `https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions`。
2. 限定在已获准`src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/`和`scripts/research/`修复**正向准入放行**、隔离网络Transport与发送事务：先持久化`send_intent`再单发HTTPS POST（程序逻辑可由Fake/Synthetic Transport模拟），真实TLS验证/hostname allowlist、no proxy/no redirect/no automatic retry、串行1、超时立即停、响应字段/usage校验、逐格账本与在途保留、首3格纯工程检查并只有全部PASS可继续至第4–108格。源码默认必须保持真实网络锁。要证明FakeTransport的All-PASS能穿过**内部工程路径**，但**本次Owner11授权**仍须在外层阻断任何真网络；仅真正新的独立Owner Live审批绑定后能进入联网进程，不能因代码自己写`pass`、任何环境变量或旧Owner10合同自动解锁。
3. 输出字段决策严格二选一：
   - `NO_CHANGE_V1`：有资料证明`max_tokens=256`在固定模型+禁thinking模式下完整输出及可计费总量不超可承受上界，则旧请求保持不动，引用原V1所有SHA；
   - `APPROVED_SINGLE_FIELD_V2`：如官方文档表明旧`max_tokens`仅限制答案token、无法为完整输出提供所需计费上界，而`max_completion_tokens`明确覆盖总输出，且已证明它对该快照可用，则**只移除`max_tokens=256`，加入`max_completion_tokens=256`**。这项是Owner11批准的**唯一可能的协议参数差异**；不改数字、thinking开关、其他任何参数与提示/样本。保留原V1文件和私有108请求原字节，不覆盖；新建 `V2_SINGLE_FIELD_OUTPUT_CAP`方案及私有108条完整wire请求清单，108条逐格semantic diff必须证明键集合的唯一差异是旧字段→新字段（路径/引用文本/消息/排序等其余逐字相同），重新生成hash、锁定V2 proposal/plan/request SHA及预算；严格计入官方潜在`+10`真实输出偏差与保守额外费用，不能把256绝对硬顶当有证事实。比较V1↔V2参数对生成长度/JSON截断、配对公平性与将来回归要求的影响；**不跑模型来证字段**。
   - 如证据不足判断该模型的字段支持或必须同时改其他键，`FIELD_CHANGE_UNRESOLVED`、保留V1，标`OWNER_INPUT_REQUIRED/OWNER_NEW_DECISION_REQUIRED`；不创建“假已批准”V2，也不利用本轮联API。
4. 与旧Owner10区分：Owner11仅准**离线**修订字段，Owner10真实运行绑定原V1 SHA，**一旦切到V2，旧Owner10不能被用作live许可**。无论V1/V2，本轮真实 POST=0，下一Owner新批准再进入3+105。

## 3. Fast-Unblock C｜108格可信输入Token证明

对**完整实际HTTP JSON消息内容**和对应chat framing提供本地可审证据：
- 优先已合法在D/E存在、版本/来源/commit可核的目标模型Tokenizer及chat template，逐格精确数；
- 或公开的、可形式证明保守`<=4096`的Tokenizer上界法，证明前提确实适用于本固定模型、Unicode/控制字符和role/chat framing，含可复算程序与反例边界；**不得用`UTF8 bytes +512`代理当证明**，除非给出该上界成立的适用定理、template及逐步证明而非经验猜测；
- 每格输出`request_id/world_hash/arm/request_SHA/tokenizer_OR_bound_method_SHA/token_count_or_upper_bound/chat_overhead/limit4096/proof_status`；最长/总量/缺口都要有。模型本身是闭源服务或chat template不可得时坦承`STRICT_TOKEN_BOUND_UNAVAILABLE`并保留Hard BLOCK；**不要为追求PASS而假造精确Qwen tokens**；
- 绝不发线上Tokenizer、count_tokens或Chat API，也不下载安装运行时代码。

## 4. Fast-Unblock D｜可执行机器账本而不重复折腾Owner

既有预算合同`USD25 warning / USD28 no new batch / USD30 hard cap`全部保留；Owner账户/地域/费率/余额已核实为`OWNER_ATTESTED`，这不是零数值账本。
- 在D/E受控 `BUDGET_PRIVATE.json` 或已有模板中录入**实际可证**模型/region/计费币种、每百万输入输出Token费率、USD转换基准和日期、历史全工作线结算与待结算、失败在途、历史CNY7.611826与Owner数7.528095914差额处理、账户可用额度或Owner bounded承诺、Price/Fx/ledger evidence hashes；不要在公开Git出现凭证、账号、余额数值。
- 重新按V1或V2的真实token/保守上界、输出含潜在偏差、108请求及20%预留算最大`batch_reservation_usd`，验证 `settled+pending+reserve <28`，到25预警，不到30硬限，余额足够，异币换算一致；按十进制避免浮点误差；未知数值记null且拒绝PASS。
- 提供可在**离线完全断网**以虚构账本样例测试的计算器及`BUDGET_GATE_LOCAL_QA`；用户此前已核实账户，缺某数只给简洁、非敏感补全字段，不再次索要API Key或重复截图，不能宣称数值账本已闭合。

## 5. Fast-Unblock E｜正向准入与单独再次执行许可

正向放行必须实现但本轮不能真执行：
- 将 A/B/C/D 每项 `PASS / BLOCKED / OWNER_INPUT_REQUIRED`和对应固定文件SHA收束到`FAST_UNBLOCK_MANIFEST`，用与Runner逻辑独立的本地Checker验证科学哈希/出站host/资金/Token proof/文件路径/版本/V1或V2唯一字段改变/秘密隔离，输出`E_OFFLINE_IMPLEMENTATION_PASS`或`E_BLOCKED`。
- 用合成数据覆盖 **全部门PASS但本次Owner11仍禁止真实发送**、A/B/C/D任意fail都会停、HTTP异常时前3或后105首故障停、usage缺失和超账单、原始108格全分母、双重send_intent防重复、无需真实Secret、全量seal、资源C写入拒绝、无D2D3或5090读取。旧46tests+新增tests/Ruff/MyPy通过，历史架构1失败只记录旧五行，新引入违规0。
- `--live`、旧Owner10、用户环境变量、本轮自动生成的pass manifest不能单独解锁。真正未来Owner必须新批准固定**最终源码commit + V1/V2 config/request SHA + 私有转出审批 + Token计数证明 + 数值预算 + Runner版本**后才可以使真实路径联网；本次零调用。
- 不得把本次静态材料称为真实Qwen端点验证，不测ASR/正式QA/C3，也不启动独立模型Judge。

## 6. 只交付**单包**，收口STOP

所有必要内容放一个入口，而不是五次重复审批：
1. `docs/paper1/dual_machine/chinese5060/fast_unblock/FAST_UNBLOCK_EVIDENCE_PACKET.md`：唯一Owner下一轮入口，**一页摘要+可展开证据指针**，A–E状态、V1或V2唯一字段、108 SHA、实际外传边界/Token/费用硬门/正向路径QA、待Owner补充的最少字段与下一次真实执行准入条件；
2. `.../fast_unblock/FAST_UNBLOCK_MANIFEST.json`：脱敏hash/证据等级/源码身份/预算&Token证明摘要；
3. `.../fast_unblock/UNIQUE_FIELD_CHANGE_DIFF.json`：逐格diff统计与新旧SHA，若没改写`NO_CHANGE`；
4. `.../fast_unblock/FINAL_OFFLINE_QA.json`：测试/网络0/Runner纯Mock正向+阻断行为；
5. `docs/paper1/dual_machine/chinese5060/W1_5060_PILOT12_FAST_UNBLOCK_RESULT.md`：一句总状态、关键复核事实、blockers和Owner下一步；
6. 本次私有证据只放D/E新Run目录并带原始hash/ZIP清单；Git只提交代码、脱敏SHA和授权索引，不入私有参考/role/原请求/endpoint密钥/账单明文。只更新必需Owner Register、Current State、Research Log、Agent/Human ledger并遵守AGENTS，不重写历史raw/旧封存。执行完成Git commit/push自身分支、fetch并回读远程SHA/clean/0:0，再STOP。

**终态只选 `FAST_UNBLOCK_READY_FOR_OWNER_LIVE_APPROVAL` 或 `FAST_UNBLOCK_PARTIAL_BLOCKED`。不论哪种，真实模型/HTTPS请求0、真实生成108`NOT_RUN`、新增模型费用0、Human Gold0、TargetedASR/正式AnswerAccuracy`NOT_MEASURED`。不要开启第二套Pilot或把模型表现当成已测结果。**
