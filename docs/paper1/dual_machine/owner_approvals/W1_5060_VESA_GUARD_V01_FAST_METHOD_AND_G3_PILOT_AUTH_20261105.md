# Paper 1｜VESA-Guard v0.1 快速研发与受限G3 Pilot授权（PO-MHEP十二字段）

**Owner Decision ID：`W1-OD-20261105-5060-VESA-GUARD-V01-FAST-13`**
**决策日期：2026-11-05 JST**。Owner在完整阅读Pilot12实际生成与暂定评价后回答“好的开始，越快越好”，同意先前提出的“第一版VESA-Guard方法实施，原36世界G3配对验证”的下一任务。**本决策批准一次V0.1方法开发和条件满足后最多36个G3真实推理请求，禁止随结果重新调试/重新抽样；不是正式研究的最终放行。** 本决策不声称已实施或已产生成效。

**生效分支：** `research/paper1-chinese-defense-5060`；许可前HEAD `59ceb4ff2267299aa7ed1c6fb0819f952098fcd5`；5090分支只读、不触及。模型 `qwen3.7-plus-2026-05-26`、同北京Workspace、V2 wire/system/temperature0/top_p1/非思考/JSON/`max_completion_tokens=256`为固定对照。没有额外judge、检索API、embedding服务或模型下载。

## 1｜Issue ID
`W1-OD-20261105-5060-VESA-GUARD-V01-FAST-13`，引用完整owner Git commit、Branch与科学证据SHA，不借用冲突`PODR-154`。

## 2｜Issue name
在原RAGDefender B1、中文迁移B2对照已封存后，开发**版本适用性和证据充分性保护**的首个无标签G3候选，并在原36世界做**仅36次**新模型生成与配对探索验证。

## 3｜Stage and current facts
原D1 Pilot12 12事实组×Poison/Clean/HN=36世界，G0/G1/G2 108格真实HTTPS200、无重试、原始响应封存；后续`D1_AI_PROVISIONAL_EVALUATION_01`中，G0/G1/G2回答15/13/11、拒答21/23/25；G2相对G0有5格回答转拒答（均共现参考片段减少），Clean候选误删4/10，Poison候选过滤2/10。108格中39个回答整体语义`UNRESOLVED`、51个拒答合理性未决、18个暂定合理拒答；HumanGold0、attack target UNKNOWN、正式ASR/QA/C3未测。**共现非因果，未确认新算法必然有效**。
原封存：
- 运行 `OWNER12_LIVE_108` output seal `ca8aa84c7485149c887abe7b60e8890f4c01e81b21e8ac46f19cf83866ff5da4`，原108私有归档 `a1a5eb07c74d2513bd8f14ac626799cfdc10f422341bae2cbd7c5c5feb029647`；
- D1暂定评价逐格 `fd04736a1cb924d75833abd58e80ebbaab906d45f485dd660538b1464d9d7f16`，评价ZIP `63b45d46919ba8691ff05c6a1efaaea826b1a8c70fa216d0316a949b067d2f14`，供隔离Evaluator，只能聚合诊断不能进入G3算法实现；
- P2 `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`；PAIR01 `bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb`；V2 `e5bd219b7812b8ef97ef916226ac221e177f227808cd0dbc0bbe280920d1b70e`；旧grid `78708759e0965e816d9d5b7aaa0bca92d2a6b92562930cd028dc87875d09468c`；统一system `b3c74613bc3700eacdce7dfedc382043013f452e321a13d8639b27817edbd1f1`；
- 暂定Reference `5c5f212ba16da97b114d897de910ab383a47d96db4cb7cd9b54e638f7f03cf31`属于隔离Evaluator，绝不供G3算法读取。
真正待验证研究问题：G3能否**在不增加污染事实采纳的前提下**改善可信证据留存与Clean/HN可回答性。

## 4｜Evidence grading
`OBSERVED_GIT`：冻结36世界、G1/G2上下文、真实108次执行统计、暂定配对与误删关联；`SOURCE_DERIVED`：RAGDefender已经是低额外模型调用的检索后过滤，TRIS/SAFER-RAG已研究一致性及自适应证据保留（故“多证据一致性”单独不构成创新）；`INFERENCE`：版本有效性与可信证据覆盖联合约束可减误删但也可能把污染重新引回；`UNKNOWN`：G3语义检测有效性、正式Gold、与现有论文的独特机制和独立泛化收益。

## 5｜Constraints
PO-MHEP、AGENTS、原事实组/36世界/TopK5、原查询与context原文、旧P2/PAIR01等不可变；不改检索/Embedding/Generator参数或世界顺序；算法只读取生产RAG时现实可获得的**角色盲字段**，不能读取Poison/Clean/HN标签、攻击target、AI参考答案、模型结果、旧分组标记、原F5候选编制来源身份、12题Gold、原评价映射或基于已知成功例的例外列表。保持D1开发而非独立验证边界；D2D3、5090、B5/B6、D1-40、正式标签/GT不触碰；D/E数据、20GiB保留、C盘受控零新增。

## 6｜Why now
D1 108个真实结果已经揭示现有B2正常候选误删与拒答增加，但没有足够事实正确性证据。Owner要求尽快提出首版方法并得到相同冻结世界G3探索结果，而不是新增大规模治理或重复原108调用。

## 7｜Risks
(1) 恢复Clean候选的同时恢复Poison，造成ASR恶化；(2) 检测器按数据集特有字段偷看角色；(3) 根据D1未决输出反复调参，形成训练测试泄漏；(4) 版本匹配与可信来源必须来自可核元数据，不能凭出处自称或年份较新就信任；(5) HN旧版本对历史问题可能合法，不能简单判过时；(6) 小n=12不支持2.5pp严格不劣证明；(7) 已有SAFER-RAG/TRIS/其他方法重叠，不能未经新颖性对照声称SOTA；(8) G3新API不在已用完的Owner12费用豁免内。

## 8｜Options
A【Owner选择，Fast-track】先**一次性预注册**简单可解释的、只用原TopK5及角色盲B2输出的版本/冲突证据核查与保留约束，先在D/E离线逐世界生成唯一G3、测试、封SHA；不根据真实G0/G1/G2具体答案挑选规则。若全部最小门PASS、G3确有至少一处合理上下文差异，一次性允许**最多36个**Qwen真实API调用，同世界每格仅1次，随后仅只读探索评价。如果上下文36格都与G2相同，则0新API，报告未形成新方法而不是虚构收益。
B【不选】先做完整Gold/D2D3后再写任何代码；利于正式结论但不利于快速方法可行性验证。
C【不选】一开始就加载大模型判别器/额外API或D1暴露标签用于逐条调参；成本、泄漏和公平性问题更严重。

## 9｜Owner recommendation
**方法具体优先级：** V0.1作为一个**风险门控的证据充分性保留器**，以封存的G2候选删除作为弱风险信号，但**不自动恢复所有G2删除项**；只在可观察且有证据的版本/来源适用性及独立支持关系成立时修复不必要删除。风险过高或冲突不可分辨则默认隔离/拒答。先做最小可解释实现；不强制在没有可信元数据时创造一个“版本事实提取器”。如确定保留策略无法带来可解释差异，只报告`NO_SAFE_G3_DIFFERENCE`并STOP，不花费36个新生成调用。所有权重和阈值如果存在必须事前定值并在读取任何逐格结果之前冻结，不准基于D1回答率回填。

## 10｜Rationale and confidence
真实生成高置信；G2片段损失与回答转拒答共现有直接数据；其因果关联以及G3收益均未知。首版开发/消融属于方案探索，**不能直接写成论文级创新有效性**。正式实验仍需要非开发集、独立Gold/攻击target、合理统计/置信区间、与最新对手方法比较。

## 11｜Owner approvals; staged but single authorization

**阶段I：立刻允许一次G3算法开发及离线36世界自检**
1. 仅在 `src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/` 新增独立`vesa_guard_v01.py`或同等隔离模块和`scripts/research/`/tests/research/；不得篡改B1/B2原封存和代码、历史原始outputs。必要时仅在新增G3 adapter/runner上调用原`pilot_design.messages`和原固定模型transport。
2. 输入只取原已封存`PACKETS_PRIVATE.json` 36世界TopK和对应B2 retained/removed decisions。可以读取B1输出作对比诊断但**不能读取评价/攻击角色/事实答案/生成结果用于算法决策**；元数据若仅见于Evaluator或是某候选攻击标注，不允许当生产可用真实性信号。验证所有输入是源Git签名的role-blind bytes。
3. S1：对query和每个chunk做保守**事实范围/版本限定可见性**抽取；未知映射标UNKNOWN而非猜。S2：构建跨chunk关系：明确同一主体/属性/时间scope内冲突，独立来源支持，弱相似但不能证明独立或真伪；对source_authority_claim不得当官方签章。S3：在**不恢复高风险未知文档**的前提下，考虑将B2删掉但独立可信支持、版本适用且无未解冲突的证据恢复，严格限定最多原TopK5，保留原rank与`C1..C5`，不得摘要、改写、拼新文本或加额外来源。
4. 若无法从现有role-blind生产元数据证明独立来源或版本归属，S3可明确SKIP/UNKNOWN，不能使用D1“source in official snapshot”这类数据集泄漏捷径。整个G3可退化到G2，但不得为求差异而放回所有删除项。
5. 需输出每格`kept/removed/restored/risk`和可审理由（基于原文片段span SHA、元数据字段、客观匹配），统计Clean/HN/Poison的误删**只能在G3规则冻结之后**由独立Evaluator解盲计算。算法运行过程严禁通过world ID词形或来源hash映射标签；任何可证明标签泄漏即STOP。
6. G3的生成消息用原固定 `SYSTEM_TEMPLATE`、原query、保留TopK片段（原引用rank ID），只改context选取，保持`max_completion_tokens=256`及模型其它wire参数和V2 JSON响应格式。原36世界顺序，**最多36个请求ID**，无多选备选G3或超参搜索。先离线 `G3_OFFLINE_GRID.json`+diff/seal、受控日志、pytest/Ruff/MyPy、初步系统风险对照；代码固定提交并SHA锁，**不根据某个世界的答案正确性调规则**。

**阶段II：一次性受限G3真实Pilot（该阶段权限已包含在本决策，满足门即运行，不再单独申请常规审批）**
7. 若G3 `NONTRIVIAL_SAFE_DIFFERENCE` 且36个世界/原TopK/subset hash/引用/role-blind审核PASS，已冻结规则+源代码SHA，原D1处理权/北京Workspace仍适用于该subset、API key受控，且当前账户资金/可用余额与全球USD25/28/30约束可按真实可得数值或Owner已有有界确认计算，则允许**仅G3 36个模型请求**（每格一次、串行、0探测/重试，首3作为本36格内工程检查）。若当前账户预算豁免缺失，不可继承Owner12豁免；本决策只授权必要的一个新G3小批次和不大于先前同型号输入边界的固定子集。新一轮须重新确认钱/余额足以承担最坏一次异常请求，不得虚构；前置未知则只报告单个所需Owner数据点并STOP。
8. 本决策对**新的≤36次**的API权限仅在Owner13原文hash、最终G3代码提交sha、私有冻结36计划sha和最小审计PASS绑定后生效。原G0/G1/G2生成输出保持只读，不再跑108次；首3格后同一次完成其余33，首次真实HTTP后任何错立停，未完成格NOT_RUN，禁止另批重试/继续。真实usage>4096即STOP（Owner沿用已明确接受的项目自设后置usage风险），输出上限266候选，单并发1、send_intent先落盘/日志hash、源数据仅北京Workspace、全36完整封存。
9. 对照Qwen完全同ID/wire/system/时间条件；不得在G3偷偷加“请更倾向回答”的新提示或做answer后修订。评估用原12事实组×3世界角色作为**独立评价侧**标签，复用封存G0/G1/G2真实响应但报告运行时点/随机性混杂，不将36相关世界当独立36个事实；有真实Gold之前只能报ABSTAIN/ANSWER、来源覆盖、候选删留、Token、延迟、费用及AI暂定/UNRESOLVED上下界，不得发布正式ASR/QA或声称改进成功。

## 12｜STOP, terminal states and evidence
仅一份精简交付：`docs/paper1/dual_machine/chinese5060/vesa_guard_v01/VESA_V01_OWNER13_RESULT.md`、`vesa_guard_v01/VESA_V01_G3_EVIDENCE_INDEX.json`（只含脱敏统计/SHA）、私有D/E `G3_PLAN_PRIVATE.json` `G3_CONTEXT_DECISIONS_PRIVATE.json` `G3_RESPONSE_*.bin`/归档SHA（真实调用前后按实际）。无原文/答案/role/target/密钥/付款资料进公开Git。按现有AGENTS/PO-MHEP做必要治理记录即可，不重复写大型方案报告。
许可终态：`VESA_V01_OFFLINE_NO_SAFE_G3_DIFF`、`VESA_V01_G3_GATE_BLOCKED`、`VESA_V01_G3_36_COMPLETED`、`VESA_V01_G3_PARTIAL_STOPPED`。若发现规则必须调用新外部服务、必须使用GT/标签或动模型参数则 `HUMAN_DECISION_REQUIRED`，本次合法STOP，不能暗改。D1开发Pilot即使G3表现好，也不得进入正式发表结论或D2/D3打开。仅5060分支独立git commit/push, 远程与本地SHA、clean/0:0核后STOP。
