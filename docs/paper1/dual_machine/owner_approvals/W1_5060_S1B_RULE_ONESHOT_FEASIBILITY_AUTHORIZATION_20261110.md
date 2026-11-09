# W1-OD-20261110-5060-S1B-ONE-SHOT-20｜Owner20 单次 Rule-V1/Rule-V2 离线可行性验证授权

**Date**：2026-11-10 JST  
**Status**：`OWNER_EXPLICITLY_APPROVED / ONE_SHOT_RULE_V1_V2_FEASIBILITY_ONLY`  
**Approved branch**：`research/paper1-chinese-defense-5060`  
**Baseline control-plane remote HEAD (before this approval)**：`3299786d05105e091f6e0aef4e2de04826197582`  
**Owner 原话**：“请继续 我们要加快速度”，紧随上轮唯一待决授权请求：“是否批准5060对已封存100个主案例及20条改写进行一次Rule-V1/Rule-V2离线可行性比较，适配器只用旧开发样本预检，双臂先封存后Gold，完成即停止”。本次仅据这一具体前置提议接受 Owner 对`ONE_SHOT_RULE_V1_V2_EVAL`的授权，**不**解释为自动放行任何其它任务或S2–S5。若现场恢复发现本次同意与其它Owner决策冲突，STOP并升级。
**Prior data-prep Run**：`W1-5060-S1B-FEAS-DATA-PREP-20261109-01`；数据提交 `20402e94ed3da6be155a605daba272ec0a7c2cf1`。

## PO-MHEP 十二字段

1. **Issue ID**：`W1-OD-20261110-5060-S1B-ONE-SHOT-20`。
2. **Issue**：固定 Rule-V1/Rule-V2，在已封存的100个主语义案例与20个从属改写视图上完成**仅一次**本地、零新增模型的可行性对照。
3. **Discovery stage/task**：Owner19数据已封存并报告`FEAS_DATA_READY / EVALUATION_NOT_RUN`。上轮监督文件 `W1_5060_S1B_FEASIBILITY_ONE_SHOT_SUPERVISOR_GATE_REVIEW_20261109.md`确认有可行性验证条件但尚未放行；Owner20本轮解除**仅这一道单次试验门**。
4. **Current facts**：
   - `OBSERVED_FACT`：100个新语义主案例（70有答案、30应拒识）+20从属问句改写；10场景类别/4领域/10虚构来源家族，105组支持集/523个原文位置检查；公开Manifest仅脱敏信息；D1/旧73未进入主100。
   - `OBSERVED_FACT`：数据 seal `531ac4e6421f6486b8165d443af2cf9d892a7bc3c740483950d03240d35a7c58`、INPUT `bd2bc5e6586789070c20dde123bfe72843181aa861aca229fdb0c23091328dee`、PROVISIONAL_GOLD `8f745f921424c6e61357ec19800bc4a1f198e92a26d36377a3a238d634598371`、SCORING_PROTOCOL `43d4d22770f5887058fabfc0162368e77cd36bd6c7d85d846417789515f5341e`；Role-free预测计数=0，正式HumanGold=0，实际性能未知。
   - `SOURCE_DERIVED_FACT`：冻结 V2依赖`《...》`标题解析，而生成器在70个可回答主案例中有21个无生成标题头（从分配公式得出）；这是预期风险，不是已观测失败。
   - `INFERENCE`：在未见数据上只运行一次、严格不后验改规则，可快速判断合成数据上的规则抽取使能性；模型准确率/版本真实可信度仍未获证。
   - `UNKNOWN`：新100的实测指标、能否公平映射多span、真实生产与正式知识污染防御收益、真实外部人审标签可信度。
5. **Affected constraints**：Owner18 Rule-V1源`68d34a5d877206f4e6d7d9e2bdda16784145a76a`、Rule-V2源`da3cbd9f16ea70ae3ba0ef2aa2408227ecfc0b4f`不得更改；Owner19输入/Gold/评分封存不变；R2 K1-C、原S1 FAIL、D1_DEV_EXPOSED、D2/D3严格隔离、原108/B2/R2不可重写、P0无可信来源不升权、S2–S5独立审批，5090仅等待Meta Llama2授权。
6. **Why now**：数据与开发代码已封存；继续等待UIE许可或拿旧73迭代造成时间和过拟合浪费。一次性负结果同样能提供清晰路线信号。
7. **Downstream risks**：同Agent造题和模型开发并不满足人工独立；无标题输入结构风险；Gold中多证据集合与V1/V2单span输出适配风险；仅合成文本的source provenance无法证明真实来源可信；加速不得覆盖评估隔离、负结果与可恢复性。
8. **Options**：
   - A `APPROVED` 单次离线规则比较（优点：0新API/模型成本、快速；缺点：合成Gold与模板偏差不能说明真实泛化；工程前置需严格封存；论文仅开发可行性；可通过新证据停止可逆）。
   - B 先只读适配器诊断后再要一次批准（较稳妥但增加等待且同样需一次运行），未选。
   - C 立即切UIE/Qwen（资产、许可与计算门未闭合，风险高且违反当前限制），不允许。
9. **LOCAL recommendation**：执行A，但必须在新120条预测前仅以旧73或单测完成公共adapter的无Gold静态预检与hash冻结。后续整个主120一次执行，双臂全部role-free结果归档后才只读揭盲评分；无法预检或身份偏差即STOP，不让工程修补改变科学结果。
10. **Rationale and confidence**：本次 Owner 的“继续”针对前一轮唯一待决单次实验，授权意图明确。对允许任务的把握高，对结果方向和可发表性无预判。若现场发现新增未决重大风险，按PO-MHEP独立升级。
11. **Explicit decision resolved / pending**：`ONE_SHOT_RULE_V1_V2_EVAL=APPROVED_BOUNDED`；`COMMON_ADAPTER_DEV_ONLY_PREFLIGHT=APPROVED`（仅旧73/普通无标签测试，不能在主120上跑）；`OWNER_AUTH_NEW_MODEL_DOWNLOAD/LOAD/INFERENCE=NO`；`S1B_FUTURE_INDEPENDENT_HUMAN_VALIDATION=NOT_APPROVED`；`S2,S3,S4,S5=NOT_APPROVED`；`5090_CLAIMS=NOT_APPROVED`。关于未证新版/跨scope误答为0：**维持观察项**，不是新增事后硬门。
12. **Allowed / prohibited**：
   - **允许**：校验所有原封存 ZIP及回执/文件哈希；用旧73或无标签普通单测预检并冻结公共adapter（不得通过新集调适配）；旧冻结Rule-V1/Rule-V2在同一 D/E 私有Role-free INPUT 120条中各一次完整离线抽取；输出状态包含Error/UNKNOWN不剔除分母；两臂先独立seal并形成SHA；之后由隔离Evaluator一次只读揭盲`PROVISIONAL_GOLD`、只算原预注册score；按100主/20从属、70/30、10类别、标题有无、自然问法、来源家族报告完整分母/95%Wilson/最差类别，判`FEASIBILITY_PROVISIONAL_GO / FEASIBILITY_NO_GO / INCONCLUSIVE_STOP`；只做脱敏汇总、日志、manifest和Git收口。建议Run ID `W1-5060-S1B-RULE-ONESHOT-20261110-01`。
   - **禁止**：把旧D1/旧73/CMRC并入新100、重复跑主120优化、分批看到新集结果再修改规则/adapter、在评价前读取Gold/source truth/分组标签、先查看部分真值、重建或改旧封存、改预注册阈值/难度/配对/采样、下载依赖/权重或运行任何新模型/LLM API、D2/D3/5090、重检索/生成、S2–S5、主研究分支merge/cherry-pick、宣布Human Gold/正式ASR/AnswerAccuracy或RAG防御增益。
   - **STOP**：私有样本不可验证、SHA漂移、adapter无法公允映射`accepted_span_sets`、标签隔离泄漏、磁盘容量不足、需要新依赖/网络、无法提供两臂完整120条、角色盲输出前发生揭盲、适配器/来源身份不一致或科学重大语义冲突。`Auto Continue=NO`，归档失败后返回Owner，不可自动修复导致新的科学试次。

## Frozen gate and metrics

- 主100不同语义案例，70可答/30应拒识。值命中分母**70**且至少**63/70**才达≥90%点估计；`wrong/decided`≤2%且`decided>0`、非all UNKNOWN，`wrong/100`另报。严格source-span/scope和Value指标区分。30条应拒识出现的误答按原协议记录，不可更改为成功。
- 20条改写视图仅作为`COMPANION`配对分析，不可加到100主分母，不可把120视为独立案例。
- 同句等价支持位置：Gold已预注册`accepted_span_sets`，集合之间OR、集合内部AND，跨段必须包含所有证据键；不能宽放span，也不能事后修改原S1 Gold。
- 每类别/标题有无/自然或显式样式/虚构来源家族单独报告命中/严格错误及拒识，指出最差类别；Wilson 95%上下界按样本量报告，不能据点估计推断真实错误率<2%。
- 若通过标`FEASIBILITY_PROVISIONAL_GO`，只可向Owner申请后续研究设计，不能自动执行S2/模型/人工标注；失败保留原始结果后停止。

## Expected evidence

Git前置检查、唯一可重放Run Manifest、旧73上的adapter测试、冻结源码/config/环境、双臂120条完整Role-free预测与SHA、Gold解封时序证据、全量Evaluator摘要、10类分层和标题分层、候选错误与异常、测试与静态/脱敏检查、真实外联/模型/API/费用均0、私有D/E ZIP/SHA索引、治理日志与Git commit/push后核 remote，全部完成后STOP。

