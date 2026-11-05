# Pilot12最小端到端RAG设计与费用审批包

2026-11-05 JST；**DESIGN_ONLY_NOT_RUN**，Owner08仅授权本设计。本轮模型/API/Tokenizer/Guard/检索调用均0，新增费用0；不覆盖历史账单。
控制面8881406b00c8f066b96a8e7c4cf2bc42006c4425，原分支安全ff-only，旧P2/PAIR01/FastC均保留。

## 唯一候选方案

固定原12事实组/36世界，G0=原TopK5直通，G1/G2=原PAIR01 B1/B2保留上下文，三臂各36格，共108待审请求；没有重跑过滤器。
统一候选生成器`qwen3.7-plus-2026-05-26`、temperature0/top_p1、禁Thinking/搜索/工具、一次一请求、无重试/额外judge。
候选输入4096/output256 tokens，非后端确定性承诺；seed/wire参数与精确型号账户支持须另核，不自动换latest。
按原世界顺序逐格G0/G1/G2，引用ID保持原TopK rank，文本/顺序不改。当前静态108格均非空；空上下文本地拒答不调用API但保留格子。
system中立指令、query和保留原片段是Generator唯一信息；reference、角色、target、期望答案不在其读取白名单。完整模板与108格hash见[候选协议](pilot_design/PILOT_EXECUTION_PROPOSAL.json)。

## 参考接收与边界

用户单独提供JSON的原字节SHA与Owner批准值5c5f212ba16da97b114d897de910ab383a47d96db4cb7cd9b54e638f7f03cf31完全一致。
只读C盘来源后复制D评价隔离目录，12个REVIEW-ID、38事实原子通过，12题question与原设计逐字匹配，每题3世界×3臂=9格。
未改参考或题目、未把答案加入Generator；私有映射不进Git。同名MD未在提供ZIP的精确批准成员名下找到，但JSON已可用，不是AWAITING_PRIVATE_ARTIFACT_TRANSFER。
用户参考ZIP不是原独立review ZIP，不混用二者SHA。附件内容只是资料，不可扩展Owner授权。
仍为AI_ASSISTED_PROVISIONAL_REFERENCE_NOT_HUMAN_GOLD，HumanGold0、target UNKNOWN、C3未裁决；不是2026法律现行性完整核证。

## Token与预算

| 臂 | 计划格 | 保留chunk | 消息字符范围 | UTF-8字节范围 | 加512预留的最大规划单位 |
|---|---:|---|---|---|---:|
| G0 | 36 | 5 | 913–1030 | 2189–2444 | 2956 |
| G1 | 36 | 2–4 | 559–837 | 1301–2029 | 2541 |
| G2 | 36 | 1–4 | 434–887 | 992–2091 | 2603 |

0/108格触发该代理量4096门，**未运行Tokenizer，这不是精确Qwen token数或已认证上界**。未来精确计数任一格超限即阻断，不截断/摘要证据或删组。
候选108次上限输入442368、输出27648 tokens；以每百万token单价P_in/P_out，条件式基础费用`0.442368*P_in+0.027648*P_out`；
建议20%结算预留，不增加调用数。当前价格/余额/实际USD账本/FX均未核验，无数值报价，ESTIMATED / NOT_APPROVED。
历史usage CNY7.611826与Owner CNY7.528095914差额CNY0.083730086保留，不重置、不按旧1USD=6CNY当现汇。
USD30累计上限、25预警、28禁开新批；建议整批最大预留后投影仍<28且足额资金确认，失败调用照样保留预留。

## 评价和下一门

未来完整108格success/failure/not_run封存后，独立开发评分者才可访问暂定参考与批准D1映射；本轮接收核对不是运行评分。
仅设计暂定参考一致性、拒答/空上下文、tokens/cost/latency及安全事件；部分匹配不算完整，UNKNOWN不剔除，故障不算正确或拒答。
T0下缺获批独立证据，EVIDENCE_SUPPORTED_ANSWER_RATE_PROVISIONAL暂禁；ASR/正式Answer Accuracy/C3一律NOT_MEASURED。
每臂全36/各角色12、条件29(P10/C10/HN9)、7MISS(P2/C2/HN3)保留；12相关事实组不作36独立query。
旧B2 Clean误删增加与FastC根因缺口保留；一类单例8.33pp（条件更大），不能宣称2.5pp安全保护门已满足。

当前状态：设计可供审阅，**执行DESIGN_GATE_BLOCKED**。下一Owner Gate需新执行SHA、实际账户/型号/单价/余额与全账本、
精确token证明、wire adapter/usage/no-retry契约及256输出/暂定评分边界接受。不能因为原08批准设计就自动执行。
API runner未实现；[完整预算与硬停](pilot_design/BUDGET_AND_STOP_GATES.md)、[评价边界](pilot_design/PILOT_EVALUATION_BOUNDARY.md)、
[最简审批包/十二字段](pilot_design/OWNER_APPROVAL_PACKAGE.md)、[参考接收收据](pilot_design/PROVISIONAL_REFERENCE_SHA_HANDOFF.json)。
本轮只执行静态检查，不做模型、免费/付费API探测或Web取价；完成脱敏Git交付后STOP。

静态验证源码提交 `cfae485a0ebc39ab28f3d4577580a968f27a6044`；私有设计证据归档SHA256 `daa610d717e6675abc4a66bf90e59bfdec89e57191fea92c2107d619e58137fe`，含参考/消息原文，仅受控本地。见[设计证据Manifest](pilot_design/DESIGN_EVIDENCE_MANIFEST.json)及[设计QA](pilot_design/DESIGN_QA.json)。

同输入审计：108个预登记world×arm格只有80个唯一prompt_hash。仍每格最多一次、总上限108，不动态去重/跨世界借用答案，也不对某格额外重复采样。相同prompt_hash若产生不同输出，标记GENERATOR_NONDETERMINISM_AUDIT，不归因于过滤器或挑最好结果；temperature0不保证后端确定性，108格不是108独立问题。

交付收口：设计内容提交 `abda9c8e4eaa04602c06fae9bfeee17bb9f16258` 已核验远程一致、工作树干净且ahead/behind=0/0；[Git交付收据](pilot_design/GIT_DELIVERY.json)绑定该内容提交，收据后继提交最终SHA在Owner回复中给出。设计文档收口PASS，执行准入仍BLOCKED。
