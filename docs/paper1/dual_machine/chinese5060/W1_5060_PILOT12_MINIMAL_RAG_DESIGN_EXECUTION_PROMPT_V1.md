# 5060 Codex｜Pilot12 最小端到端 RAG 可行性设计（只设计与预算，不运行）

**这是直接在5060独立研究分支可读取的最终Prompt，不依赖ChatGPT附件。**

Owner ID：`W1-OD-20261105-5060-PROVISIONAL-PILOTDESIGN-08`；批准提交：`919b891c067ad30f161a0291f3fe4ea764f8db8a`。
十二字段授权：`docs/paper1/dual_machine/owner_approvals/W1_D1_PROVISIONAL_REFERENCE_AND_RAG_PILOT_DESIGN_OWNER_AUTHORIZATION_20261105.md`。
只允许在`research/paper1-chinese-defense-5060`工作。最新方案不是生成实验许可；5090完全独立。

## 0. Git与安全前置

1. 按AGENTS.md完整Context Recovery、PO-MHEP和Forward/Paper Risk Review，读取Owner Decision Register/Current Work State、既有P2、Fast B PAIR01、Fast C、选样hash和最近15次Git提交。先fetch、检查upstream和clean，必要时只做安全ff-only。不得reset/stash/rebase/merge或覆盖历史。
2. 本轮严格`DESIGN_ONLY_NOT_RUN`：不运行Qwen或其他模型（包括免费的API、token探测、embedding、Guard、Retriever），不下载数据/权重、不调用公网外部模型服务、不重建TopK、不得重跑B1/B2、不得改模型/阈值/样本/参考答案，不读取D2/D3/Reviewer/GT Vault。
3. C盘不新增项目可控文件；小型报告、临时和缓存仅D/E。角色身份、标准答案、旧Evaluator标签不得被注入未来 Generator/Guard/检索输入；只供后封存的独立开发评分器使用。

## 1. 固定证据与暂定参考

- 旧P2已封存36独立检索世界（Pilot12×Poison/Clean/HN），原TopK5 hit29/36（P10、Clean10、HN9），7 miss保留；B0全部直通；Fast B的B1/B2各36/36原离线过滤结果有效，Fast C只读阶段归因部分未识别，以上不许重写。
- Owner**只接受**12题 AI辅助暂定事实答案作D1 feasibility参考，`AI_ASSISTED_PROVISIONAL_REFERENCE_NOT_HUMAN_GOLD`；不认定合法来源T1、不推断target、Human Gold始终0、C3未裁决、正式ASR与Accuracy不可测。
- 监督端私有参考文件：`PAPER1_PILOT12_AI_PROVISIONAL_REFERENCE_V1.json` SHA256 `5c5f212ba16da97b114d897de910ab383a47d96db4cb7cd9b54e638f7f03cf31`；同名`.md` SHA256 `7b0c8303ccb9976648fbd02efdcf2c4cc2d1d8f470bdc92c7c36097f12107092`；原独立review ZIP SHA256 `2e289f68c8adee54187a4520d116182e20171a3dca3cd05daf3312a98a37f8c7`。
- **这些私有文件不在公开Git中**。若本机D/E已有通过校验的副本，可只读确认schema、12个REVIEW-ID和摘要，不要把完整题卡/答案或角色映射提交Git。若没有，注明`AWAITING_PRIVATE_ARTIFACT_TRANSFER`；**继续完成无需答案正文的设计与预算**，不要猜题目/事实、从网页重建、不因缺文件无意义停止整个方案。

## 2. 最小Pilot方案（仅草案，不默认执行）

设计一个**固定全部12事实组、36世界**的成对三臂候选方案：
- `G0=B0`：P2原TopK5不做过滤。
- `G1=B1`：复用Fast-B已封存的公开RAGDefender v0.2过滤后上下文。
- `G2=B2`：复用Fast-B已封存的仅中文Embedding替换过滤后上下文。

建议一世界一臂一次确定性生成，**最多计划108次请求（36×3），并不是已批准API调用额度**。禁止另加judge模型、重复采样、重选组、根据结果动态停止或调整。统一同一个冻结目标生成器候选ID `qwen3.7-plus-2026-05-26`，但在下一Owner Gate前需确认真实提供商账户和精确型号仍可用；不得自动换成其他版本。相同system提示词、相同query、同一世界保留TopK顺序、固定temperature/seed（如API不支持seed如实披露）、同一max_output_tokens、相同全任务时效条件，失配或空上下文必须如实记录。

运行前设计证明：生成器只接收question、冻结TopK过滤后的引用及中立指令，**无role、candidate标签、expected_answer、攻击目标或参考答案**。先写出拟冻结的完整消息模板、输入排序、hash、空结果策略和调用/超时/重试限制。完整分母36、按三个角色各12与召回条件分母29（P10/C10/HN9）均报告；不把7miss算防御成功。

拟议结果的名称只能是`PROVISIONAL_REFERENCE_CONSISTENCY`、`EVIDENCE_SUPPORTED_ANSWER_RATE_PROVISIONAL`（若可由独立证据支持）、`ABSTENTION_RATE`、`CONTEXT_EMPTY_RATE`、`LATENCY/TOKENS/COST`以及安全事件审计。No targeted ASR（目标未知），No正式Answer Accuracy（HumanGold0），No C3（未裁决）。评分器只能在三个臂输出完整封存之后访问暂定参考和批准D1角色映射；不得交给生成器。应预先规定答案等价、历史时效、错答/部分正确、格式拒答、故障、零证据和无法判定的统一策略；缺人工边界写UNKNOWN，不擅自硬判。

## 3. 预算审批包必须可核算

- 给出call计划表：固定108次请求为建议上限，任何额外重试/评判单独申请。记录每次 `request_id/world_hash/arm/prompt_hash/input_token_est/actual_input_token/actual_output_token/max_output_tokens/latency/price_version/cost` 的计划字段，不含真实未发生的usage。
- 推荐申请**每次输入最大4096、输出最多256 tokens（均仅待审批）**。据此108次请求的上限为输入442368、输出27648 tokens。必须估计TopK和模板真实长度：如果超过4096，按PO-MHEP阻断**该格/整个设计**，不能静默截断检索证据或省略组；应把token规划不足列为决策问题。若API计费机制/缓存价格或输出超限机制不确定则不报价承诺。
- 只用**待核官方当前单价/账户实际计费记录**计算`cost_upper_bound = input_cap*current_input_unit_price + output_cap*current_output_unit_price + retry/overhead reserve`，并标出总USD30上限、USD25预警、USD28不得启动新付费批、既有费用差额尚待对账。没有实价、汇率、账单或余额核查时，任何成本只写`ESTIMATED / NOT_APPROVED`，不能把估计人民币直接折抵美元硬门。
- 定义硬停：模型/账号ID不符、无Owner新批准、输入/输出token预算超额、费用累计突破前置门、请求未返回可封存usage、实际异常/隐式网络重试、角色/GT泄漏、TopK输入SHA漂移、C盘意外写入、数据权限/空输出路径冲突。**本轮不得为了检查是否可用而发送任何真实API请求。**
- 原安全保护：ASR增量≤2.5pp、QA下降≤2.5pp、HN-FPR和拒答率增量≤2.5pp、baseline ASR0不得新增成功攻击；D1每类12样本的单例步长8.33pp，因此首轮仅报告观察信号和uncertainty，不得宣称2.5pp统计保护门已验证满足。

## 4. 交付与STOP

至少交付：
1. `docs/paper1/dual_machine/chinese5060/W1_5060_MINIMAL_RAG_PILOT_DESIGN_AND_BUDGET.md`：1份可审批核心方案（不写成长篇论文）；
2. `docs/paper1/dual_machine/chinese5060/pilot_design/PILOT_EXECUTION_PROPOSAL.json`：36世界×3臂、候选命令/提示、隔离和stop规则，全部`NOT_RUN`；
3. `.../pilot_design/BUDGET_AND_STOP_GATES.md`、`.../pilot_design/PILOT_EVALUATION_BOUNDARY.md`、`.../pilot_design/PROVISIONAL_REFERENCE_SHA_HANDOFF.json`、`.../pilot_design/DESIGN_QA.json`；
4. 仅输出脱敏/角色盲的公开Git内容，私有参考、标签、raw和未来答案仅D/E受控归档。按AGENTS/PO-MHEP检查必要的治理账本、Current State、Research Execution Log，Git commit/push仅5060分支，回报最终完整SHA、工作树/upstream、待Owner决策项，**STOP**。

严禁自动进入真实Qwen/其他LLM Pilot、B3/B4、B5/B6、D1-40、新样本、D2/D3、GT授信、正式ASR/C3、5090 Claim、主线/跨机merge。所有当前调用次数、费用、ASR、Answer Accuracy仍分别是`0/0/NOT_MEASURED/NOT_MEASURED`，零费用仅指本次设计活动，不覆盖历史账单。
