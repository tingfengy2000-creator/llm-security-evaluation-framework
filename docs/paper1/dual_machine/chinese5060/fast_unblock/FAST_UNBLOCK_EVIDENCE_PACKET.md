# Pilot12 Fast-Unblock 单一证据包

2026-11-05 JST · **`FAST_UNBLOCK_PARTIAL_BLOCKED`** · `W1-5060-FAST-UNBLOCK-20261105-01`

完成 V2 单字段冻结、正向检查器、逐格预算与事务引擎。合成全通过完成 108/108，真实模型/API 0 次，真实成功 0、失败 0、未运行 108，新增费用及新增在途 USD 0。真实执行权限仍须由新的 Owner 决议绑定。

| 门 | 实际状态 | 本轮证据与剩余条件 |
| --- | --- | --- |
| A 来源与外传 | OWNER_INPUT_REQUIRED | 原 P2 36 份 chunk 封存逐份核验，108 格关联 46 个实发源文档哈希，其中 17 个匹配角色盲来源快照，另有 29 个未匹配。16 个独立裁决来源是不同集合。六类敏感模式各 0 命中，需逐来源权利、敏感性和指定处理方/地域清单。 |
| B 接口 | OWNER_INPUT_REQUIRED | 108/108 格仅将 `max_tokens=256` 改为 `max_completion_tokens=256`。官方公开能力已核。仍缺唯一实际 Workspace/host、地域与实际计费语义。 |
| C Token | STRICT_TOKEN_BOUND_UNAVAILABLE | 108 条证明索引已封，严格证明 0/108。缺同模型 tokenizer 与完整聊天模板身份，或覆盖实际 framing 的严格上界。 |
| D 费用 | OWNER_INPUT_REQUIRED | Decimal 账本计算器通过合成费率、历史差额、未结算、余额和 USD 25/28/30 检查。现时全线数值及账单来源缺失，实际整批预留为 null。 |
| E 放行 | E_OFFLINE_IMPLEMENTATION_PASS，真实 BLOCKED | 64 项离线测试通过。合成通过后可依原顺序跑首 3 格并进入余 105 格；真实入口在任何凭证读取或连接前拒绝本轮授权。 |

下一次只需补齐一个受控材料组，包含 46 个实发来源与允许处理方/地域的依据、唯一 Workspace host、全 108 格严格输入证明、该地域真实计费界和可核 USD 账本。Owner 既有账户核验沿用 `OWNER_ATTESTED`，私有材料用摘要绑定。新的真实执行决议需绑定候选源码、V2 proposal/plan/grid、全部独立核验材料和固定 D/E 输出路径。旧 Owner 10 绑定 V1。

<details>
<summary>冻结、费用、验收和治理证据</summary>

## 冻结和风险

Context Recovery 核对 AGENTS、PO-MHEP、权威映射、Owner 记录、当前状态、总控、长期要求、实验主表、研究路线、执行日志和 15 条 Git 历史。项目优先 RAG 安全，其后为安全评测、AI Guard 与 Agent 安全。Paper 1 仍为阶段 6.1 的中文隐蔽事实污染 D1 开发。本地专用工作树 `.worktrees/paper1-chinese-defense-5060`，分支及 upstream 均为原 5060 研究分支。由 `731b48419aba2dab3b8ded310d349fcf441c3f1b` 安全快进至合同 `ea7e7d6a585ac96dddf3d1c2dcc37113ee460612`，启动时干净且 ahead/behind 0/0，治理与 Git 一致。仅获准一次离线解阻及唯一字段修订。正式实验、真实发送和下一研究阶段须另批。 [Owner 11](../../owner_approvals/W1_5060_PILOT12_FAST_UNBLOCK_OWNER_AUTHORIZATION_20261105.md)

**Forward Risk Review** 核查数据外传权限、真实授权锚、连接范围、单发/异常重发、失败费用与 D/E 余量。**Paper Risk Review** 核查三臂公平性与可复现性。V2 仍为 12 组、36 世界、原顺序 108 格、80 个唯一提示词。G0/G1/G2 同一 wire、相同模型，原 query、system、TopK、chunk 和过滤结果逐字保全。29 个命中、7 个漏召回保留。旧 Fast C 根因未识别和 B2 Clean 误删警示保留。Human Gold 0、target 未知、C3/正式 ASR/问答准确率 `NOT_MEASURED`。

旧字段一般限制答案长度，新的 `max_completion_tokens` 涵盖推理与答案，官方列出 Qwen3.5-Plus 及后继，固定快照属于该系列，JSON Object 模式也有公开支持。按文档最多 10-token 差异保守预留 266；目标账号、地域和实际计费尚无实测或证实。保持数字 256 和禁 thinking。V2 可能影响生成长度及截断率，三臂统一使用 V2，并在未来用实际 finish reason 审查。V1 与 V2 的生成结果分开统计。[接口说明](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions) · [固定快照](https://www.alibabacloud.com/help/en/model-studio/qwen3-7-plus) · [JSON 输出](https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output)

| 证据 | SHA256 |
| --- | --- |
| V1 proposal | `0aaf4cfb28dc1e7d9fea8fcdc8f7143afd56857fa300f8b6e3f8f9d0ff081cb6` |
| V2 proposal | `e5bd219b7812b8ef97ef916226ac221e177f227808cd0dbc0bbe280920d1b70e` |
| V2 私有完整 wire plan | `0920add3e5b5383a9b685207cabeb539bb3d414ee1db30c6f7a313d37469bbcc` |
| V2 有序 wire grid | `78708759e0965e816d9d5b7aaa0bca92d2a6b92562930cd028dc87875d09468c` |
| 私有证据归档 | `a5e4e30015a843a1c864dcbf642fecdaeb0547bbe3d992d77b7588666e7ca375` |

冻结源码 Git SHA 为 `43be925d57ef6fbe9cbb27d22c7f1495373c6204`。私有归档含 527 项，CRC、成员 SHA 和索引均校验通过，受控 D 盘证据包括源矩阵、逐格 Token 缺项、V2 wire 与差异、账本模板、独立核验、模拟发送意图/返回/失败和全量 seal。源码、配置与日志身份见 [Manifest](FAST_UNBLOCK_MANIFEST.json) · [字段差异](UNIQUE_FIELD_CHANGE_DIFF.json) · [离线 QA](FINAL_OFFLINE_QA.json)。

## 账本和事务

保守上限为输入 442,368、候选输出 28,728 tokens。费率按每百万 token，预留 `1.20 × (0.442368 × P_in + 0.028728 × P_out)`，实现按格向上取整并保留在途。启动要求累计已结算 + 未结算 + 整批预留 < USD 28 且余额足够。25 预警、28 停发、30 累计硬限。历史 CNY 7.611826 与 Owner 数 CNY 7.528095914 的差额 CNY 0.083730086 保留。虚构费率按 4096/266 全上限预留 USD 0.63426240，实际账本模板空缺的值为 null。

独立 checker 绑定 manifest/证据字节、V2 唯一字段、host/region、全格严格 Token、账本与固定路径。事务引擎先独占创建运行目录和逐格 send intent，落盘后单发、核 usage/费用/模型/JSON、首 3 检查点后继续，首错停发并封存全部 108 状态。合成首格超时、第三格 HTTP 错误、第四格缺 usage、第五格 267 超账单均验证停发，未结算预留保留。新 Owner 的真实授权摘要尚未钉定，CLI 和程序入口均拒绝真实执行。没有实测 TLS、账户端点、返回或计费。

额外治理与架构测试 8 项通过、1 项为既有实验主表便携性失败。实施前后同样匹配 5 行历史绝对路径，本轮新增匹配 0 行。

## PO-MHEP 决策记录

1. Issue ID 为 `W1-5060-FAST-UNBLOCK-RELEASE-01`。
2. 问题为静态解阻完成部分，真实准入证据仍缺。
3. 阶段为 Owner 11 Fast-Unblock。
4. `OBSERVED_FACT` 为 V2 独立 108 格比对通过、模拟 108 成功、真实 0。 `SOURCE_DERIVED_FACT` 为 Owner 11 离线许可、官方字段语义。 `INFERENCE` 为 266 候选预算。 `UNKNOWN` 为实际地区和计费界、外传权利、严格计数、数值预算。
5. 受影响约束为原冻结输入和评估隔离、D/E 存储、USD 25/28/30。
6. 这些证据须在首次真实发送前闭合。
7. 风险为外传、超账单、重复付费或把工程结果当研究结论。
8. 选项 A 为零调用封存并停止，保全当前代码。选项 B 为补齐受控材料后由新 Owner 审批限定一次真实执行，发出的请求不可撤回。
9. LOCAL 按 A 收口。
10. 对本地冻结、模拟和零调用高置信，实际供应商行为仍待证。
11. 由 Owner 在同一后续决议审阅外传与地域、可核 Token/预算和新运行绑定。
12. 决定前限于离线证据核对，真实 Pilot、评价和其他阶段保持停止。

</details>


## Evidence Recovery Addendum（2026-11-05 JST）

**EVIDENCE_RECOVERY_PARTIAL_BLOCKED**，W1-5060-EVIDENCE-RECOVERY-20261105-01。真实 API 0、费用 USD 0、108 格 NOT_RUN。原 V1/V2、Runner、数据、阈值保持冻结。Human Gold 0，target 未知，正式 ASR/QA 未测。

- **来源**。46/46 个文档身份闭合。29 个旧未匹配项均逐字连接到签署 D1 候选，覆盖 29 个世界和 75 个请求格。17 个原快照也全与历史 F5 evidence 正文吻合。当前第三方处理权和语境敏感性尚未放行。 [来源附录](evidence_recovery/SOURCE_ORIGIN_RECONCILIATION_SUMMARY.md)
- **账户和账本**。从旧 seal 恢复完整北京 Workspace，仅私有保存。历史 361 份收据和预留逐份核验，CNY 7.611826，历史未配对预留 0。Owner 数与差额保留。当前适用账号、账单与余额待绑定，公开价情景预留 CNY 1.337472。 [账本附录](evidence_recovery/ACCOUNT_AND_LEDGER_RECOVERY.md)
- **Token**。108 格最大 2,444 UTF-8 bytes，严格 4,096 证明 0/108。后置 usage 检查提案已留档，首次越界请求已经发送且可能收费。现有门继续有效。 [C 门证据和风险提案](evidence_recovery/C_GATE_STRICT_PROOF_OR_RISK_OPTION.md)

Owner 待决仅三项：
1. 按本地矩阵一次确认冻结 query/TopK 的当前处理权和敏感性，优先补 29 个项目候选的权利依据及 2 个官方网页的使用范围。
2. 确认沿用已恢复的北京 Workspace，并绑定当前计费界、已结算/在途、可用资金和 FX 的受控汇总。
3. 保持事前严格 Token 门，或待其他门闭合后单独接受后置逐格检查风险。另有真实运行仍须新授权。

两次只读重算的 6 项输出逐字一致，28 项隔离相关测试、Ruff、MyPy 通过。私有归档 SHA256 `37934121700ea2d7da422746a2f35755aead281ab4cc9fd9397719b5ccfe6dcc`，18 项成员校验通过。 [QA 与哈希](evidence_recovery/FINAL_EVIDENCE_RECOVERY_QA.json)

上下文恢复核对 AGENTS、PO-MHEP、Owner 11、当前状态、账本与治理记录。阶段 6.1 D1 开发，优先 RAG 安全及可复现验证。5060 工作树从 `dde903470c877de92df46d8dd2c8348df6d39600` 安全快进至合同 `f0036bdb6877aca9946e9d048e9d7aa285ef515b`，启动时与上游一致且无未提交或未推送修改。Forward/Paper Risk Review 分别将历史授权、文件字节身份、当前可外传性、公开报价和实际计费分开，防止把历史或诊断代理升为准入与科学结论。完成本轮 Git 收口后停止。
