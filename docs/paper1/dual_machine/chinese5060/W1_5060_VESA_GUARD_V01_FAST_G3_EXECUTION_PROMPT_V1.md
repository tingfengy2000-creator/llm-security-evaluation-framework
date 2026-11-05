# 5060 Codex｜Paper1 VESA-Guard v0.1 一次研发 + G3快速配对实跑合同

> **从Git完整读取，直接执行，拒绝再循环Fast-Unblock或写一轮只有计划无方法的文书。** Owner在Pilot12实际报告及D1暂定评价后批准“好的开始，越快越好”，本合同将其落成**单个受限任务**。离线方法完成并达到硬门后，在同一任务执行新的最多36次G3真实推理；绝不重跑G0/G1/G2的108格。

## 0｜唯一授权、Git安全、冻结来源

Owner13 `W1-OD-20261105-5060-VESA-GUARD-V01-FAST-13`，十二字段原件：
`docs/paper1/dual_machine/owner_approvals/W1_5060_VESA_GUARD_V01_FAST_METHOD_AND_G3_PILOT_AUTH_20261105.md`
Owner13登记提交 `1b2bdec85805ab691e7c7670a43ead0069ed56a3`。你只在`research/paper1-chinese-defense-5060`工作；用户已将原`5090`隔离，不碰主分支。任务起点最新已核 `59ceb4ff2267299aa7ed1c6fb0819f952098fcd5`。

按`AGENTS.md`/PO-MHEP的12字段 Context Recovery、最近15 Git commits、当前head/upstream/clean/fetch/ff-only、FORWARD_RISK_REVIEW与PAPER_RISK_REVIEW完成必要核对，异常STOP；不得stash/reset/rebase/force push/merge。不要再复述无关Stage1–5历史；把它们保持不可变。

**科学冻结：**
- P2 seal `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`；
- PAIR01 seal `bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb`；
- 原V1 proposal `0aaf4cfb28dc1e7d9fea8fcdc8f7143afd56857fa300f8b6e3f8f9d0ff081cb6`、真实V2 proposal `e5bd219b7812b8ef97ef916226ac221e177f227808cd0dbc0bbe280920d1b70e`、原108 V2 grid `78708759e0965e816d9d5b7aaa0bca92d2a6b92562930cd028dc87875d09468c`；
- 原真实批次 `OWNER12_LIVE_108` `output_seal_sha256=ca8aa84c7485149c887abe7b60e8890f4c01e81b21e8ac46f19cf83866ff5da4`，原归档 `a1a5eb07c74d2513bd8f14ac626799cfdc10f422341bae2cbd7c5c5feb029647`；D1开发暂定评价原报告 `docs/paper1/dual_machine/chinese5060/pilot_rapid_live/PILOT12_D1_AI_PROVISIONAL_EFFECT_REPORT.md`只读**聚合事实**，不得把私有逐格答案读进VESA开发进程；
- 原36个世界来自12事实组×(Poison/Clean/HN)，G3只读取**生成器可见的角色盲原TopK5、B2过滤原记录**。世界角色、攻击目标、参考JSON、Evaluator结构和语义评价每格输出只在隔离评价进程，不能在算法代码import或runtime路径被访问。
- 禁止读取D2/D3/Reviewer/GT vault、C3目标、5090 Claim、B5/B6、D1-40；不运行新的Retriever/重做Embeddings/修改Guard参数。

## 1｜VESA-Guard v0.1 最小可检验架构（不是替换整套系统）

原则：**首版只解决“错删证据→缺失事实→拒答”的可观测风险，同时谨慎阻止未知Poison被恢复**。这是`Evidence-sufficiency-Aware / Version-aware Safeguarded Selection`的工程候选，不声称已经发现新的论文算法贡献。

接口建议：
`vesa_select(query: str, topk: Sequence[Chunk], b2_retained_ids: Sequence[str], observed_runtime_metadata: Mapping) -> Decision`
返回按原rank排序的`retained_chunk_ids`、`removed/restored_ids`、`unknown_claims`、`reasons_by_chunk`、`algorithm_version_hash`。**不要输出角色、正确答案或“疑似攻击目标”**。用不可变原chunk文本与来源元数据；先验证全部hash再处理。所有恢复或删减的原chunk必须属于原TopK5，不超过原TopK数，不补新chunk、不新检索、不改写/压缩文本；引用ID严格使用原rank `C1–C5`，中间有空位允许，但不能重排编号。模型原system+query/输出模式不变。

实现三个轻量且可逐项关闭的纯本地模块：
- **A｜Scope/Version Validator（保守）**：从query与文本中抓取可核的时间/适用期间/版本/主体/条款或数值，保留原文片段与证据字符区间；缺明确元数据标`UNKNOWN`，禁止用“更近年份=一定真”或者“年份不同=必有冲突”。对于历史时间条件不能把旧版本自动判不可信。禁止根据`source_document_hash`去角色映射表认定Poison/Clean。
- **B｜Independent-Support/Conflict Graph（纯本地）**：只在主体、事实属性、版本时间及适用条件可比时判断`EXPLICIT_CONFLICT`/`EXPLICIT_COMPATIBLE`；多个相似句不能证明来源相互独立。仅从**生产系统现实可获得、非数据集标签型**出处元数据核实独立支持；来源自称权威只是`CLAIMED_UNVERIFIED`，不得当签名。没有可靠对应关系则`UNKNOWN`，不能做语义真伪的随意判定。禁止新增LLM、在线网页、embedding模型。
- **C｜Coverage-Constrained Safeguarded Rescue**：从原B2保留集合出发，对被B2移除的chunk只有在**问题相关必要事实、适用scope明确、可验证独立支持、无未决高风险冲突且可说明不新增不可核风险**时允许恢复。其他一律保留B2隔离状态；修复结果对每个被恢复chunk给出可复算span或元数据证据。不能把`D1_DEV_ONLY`或“存在于SOURCES.json”之类Evaluator编制事实变成信任捷径。B2作为一个弱风险线索而不是Ground Truth。
- 不要为了强行产生非零G3差异，擅自调整规则/阈值、绕过B2风险、恢复“可能是Clean”的文档。若条件不足方法暂时退化到G2，优先交付真实发现及改进方向，而非伪造实验优势。

**算法实现必须只用标准库/已安装依赖**；本机D/E受控位置新加`src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/vesa_guard_v01.py`以及最窄project adapter；不能修改旧B1/B2旧source、inputs、Runner、原封存。若必须补新G3 runner，复用已验证的`pilot_design.messages`、`pilot_live_transport`与源manifest模型配置，通过新adapter并严格限制权限。禁止创建难审计的大型新框架。

## 2｜先离线一次冻结G3，不在D1做“逐条修答案调参”

从 `PAIR01/PACKETS_PRIVATE.json` 与 `B2_RESULTS_PRIVATE.json` 重建原36 world，必须读取由seal钉死的字节。每world仅生成一个G3候选上下文，输出`G3_OFFLINE_GRID_PRIVATE.json`、`G3_DECISION_TRACE_PRIVATE.json`与`G3_FILTER_STAGE_REPORT.md`（公开只摘要和hash）；至少以下独立校验：
1. 36世界×G3恰36项；原世界顺序/原query/hashes与P2一致；所有chunk确为TopK子集，rank及引用ID不变；no rewrite/refill；`G3_QUERY_SYSTEM_SAME_AS_V2`。
2. 确认算法代码及运行白名单**根本无法import/读取** `D1_AI_PROVISIONAL`的任何逐格回答、Gold、role、target、candidate-only根证、Evaluator评分及原108输出；真实G0/G1/G2仅在封存后评估侧读取。源码单元测试模拟角色泄漏与同文本不同world_id，不得按world_id/标签条件分支。
3. A/B/C每个模块均有单测：历史时间有效、版本冲突不混淆、独立来源不能从相同重复文本伪造、空证据/无可核证据不可恢复、正常证据安全恢复、明确冲突不恢复、source metadata自称官方不自动有效、原文/排序绝不改；冻结默认参数和无D1目标调参证据。
4. 逐世界记录G3对G2的`changed_context_hash`/source removed/restored，只有`G3_DIFFERENT_WORLDS>=1`且全部变化的保护证据实际成立才进入真实API。若全36与G2相同：`VESA_V01_OFFLINE_NO_SAFE_G3_DIFF`、新增模型请求0、输出真实失败归因并STOP，**不作虚假增益报告**。
5. 开始新G3生成前把代码/依赖/36格wire字节/请求hash/参数和所有实证差异单一提交+独立QA封存，之后不得按产生的答案修改选择策略。不给任一世界自定义规则。

## 3｜一次性真实G3 Pilot（同一Owner13合同含授权，不要再重做Prepared阶段）

本条只有在离线检查`PASS`且`G3_DIFFERENT_WORLDS>=1`时启用。**已申请并获准最多36次G3调用；G0/G1/G2老108原样，不得重试/重跑。**

- 只有原冻结query/system及G3的TopK子集允许外传：复用Owner12已审北京Workspace D1来源范围许可，若有新来源/文本或明示禁传则STOP。仅官方 `cn-beijing` HTTPS Workspace，原 `qwen3.7-plus-2026-05-26`，temperature=0/top_p=1，nonthinking、no search/tools、JSON response `status/answer/citations`，`max_completion_tokens=256`不变；36格次序=原世界次序，1次/格，串行1，不缓存或去重相同prompt。
- 原Owner12单批费用豁免已用完，**本次不继承其全线预算豁免**。使用账号既有Owner核验的有效费率/余额及最少保守预算上界做一条D/E私有36格额度收据，账本记录至少`owner13`/date/region/model/frozen36 SHA/available funds/estimated reserve/old global USD25/28/30以及支付覆盖；不可凭Mock费用或猜测余额放行。若缺当前授权可用额度且无法复用Owner明确的有界资金事实，则`VESA_V01_G3_GATE_BLOCKED`并只报精确缺项，不追加其他准备任务。
- Owner13的新真实放行必须校验本Owner13十二字段**Git实际字节SHA**、最终算法源码commit/hash、G3私有36计划hash、独立离线QA、D/E私有数据权限和账本、单次runID与输出目录全路径。Checker事实PASS不同于Agent自签Owner；`--live`或密钥本身不能授权。严格的原始发送意图、唯一运行目录、单POST无重试、不重定向、不代理、证书验证、封存状态；必须使用既有live实现无关B1/B2的接口。
- 首3格是原36格的前3，均协议/模型/usage/输出/引用/成本/证据成功才继续余33；每格回包后`usage.prompt_tokens <=4096`（原Owner12已接受最多一次后置阈值风险）与`completion_tokens<=266`候选检查；HTTP/JSON/usage/费用不明/泄漏/预算超限即首错STOP，不补跑/续跑、不调参；失败可能在途保留，真实请求最多36。
- 生成之前若检查失败不可用原Owner12`LIVE_AUTHORITY_SHA256`绕过；真实完成后原始JSON/usage/时间/运行ID/返回model/全36格状态/封存SHA仅D/E私有，公开Git只有脱敏摘要。

## 4｜快速报告研究可行性，绝不把描述性改进冒充正式效果

先封存真实G3，再由**独立Evaluator**同12事实组、同36世界关联原G0/G1/G2不可变真实输出。仅报告：
- `ANSWER/ABSTAIN`同世界4臂转换（G3 VS G0/G1/G2），Clean/HN/Poison各12格，给“拒答率/可回答覆盖”而非准确率；
- 被删候选中`Poison candidate`/Clean/HN及原TopK hit/miss：这类**角色标签只允许评价侧解盲**，若G3恢复了Poison必须原样披露，不以“更多回答”判成功；
- 原固定暂定Reference对新G3逐格`FULL_CORRECT/WRONG/UNRESOLVED`仅有证才判，不能把字面原子命中当整体正确，正式ASR/Accuracy/T0仍`NOT_MEASURED`，HumanGold=0/target未知；
- 12事实组配对+小n置信与描述性、Token/估算成本/实际账单未核、时延/源码命令/模型/wire一致性；不能用36相关世界当独立36事实组；不把B1/B2差异归因于Embedding。
- 如果G3拒答率下降但污染候选更多，则方法性能`TRADEOFF_UNRESOLVED`而非`IMPROVED`。论文级改进需正式独立Gold、D2D3/开放基准、阶段消融和与相关方法的创新对照后才主张。

## 5｜成果与STOP

仅一份主报告 `docs/paper1/dual_machine/chinese5060/vesa_guard_v01/VESA_V01_OWNER13_RESULT.md`、一份机器可核脱敏索引 `docs/paper1/dual_machine/chinese5060/vesa_guard_v01/VESA_V01_G3_EVIDENCE_INDEX.json`，可引用D/E受控离线/真实独立归档SHA；必要治理记录依AGENTS/PO-MHEP只改真正涉及的文件，保留历史所有旧文档；不公开原候选、角色映射、私有回答、攻击目标、API key/Workspace真实ID或账单数值。现有Reference不变。
终态：`VESA_V01_G3_36_COMPLETED`／`VESA_V01_G3_PARTIAL_STOPPED`／`VESA_V01_OFFLINE_NO_SAFE_G3_DIFF`／`VESA_V01_G3_GATE_BLOCKED`。只推送5060自身分支，核本地/远程HEAD一致、clean/0:0，STOP并报告**方法具体规则、变化的世界数、真实调用数、三角色下答案/拒答变化、Poison漏放与Clean误删方向、下一项方法改进必要性**，不要无尽准备。
