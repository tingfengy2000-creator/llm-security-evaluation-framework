# 5060 Codex｜VESA-Guard v0.2：一次修订、一次冻结、最多36次G3真实配对（直接执行）

**完整执行指令。不要重复写预案，不要再次跑G0/G1/G2。**

Owner14:`W1-OD-20261105-5060-VESA-V02-FAST-14`，十二字段原件：`docs/paper1/dual_machine/owner_approvals/W1_5060_VESA_GUARD_V02_FAST_REVISION_AND_G3_AUTH_20261105.md`。授权原件登记提交`4fa4662caa108ef028cf9f1b7a092df9d3a85819`。仅分支`research/paper1-chinese-defense-5060`，授权前HEAD `bfcfaa6490de96b97b12b3304297049dfa627910`。Owner明确**允许实现单一v0.2、执行36世界离线验证；若存在可审计非零差异且出站/预算/独立安全QA通过，在同一任务内最多真实发送36次固定Qwen G3-v0.2，首3通过继续33，不再重复常规流程审批。** 但不能继承Owner12一次费用豁免，未知资金/数据处理权仍要STOP。

## 0. 现场恢复与严格科学输入隔离

按`AGENTS.md`规定先读取context map、PO-MHEP、Owner register/current state、Stage canonical/experiment master、最近15次Git提交；核`git fetch --prune --tags origin`、分支/HEAD、clean和ahead/behind；只有安全FF-only可pull，任何未知本地修改/分叉STOP。简要登记 Context Recovery 与Forward/Paper Risk，立即进入实现，不产生独立“准备阶段”。
冻结：P2 `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`、PAIR01 `bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb`、Qwen `qwen3.7-plus-2026-05-26`、System `b3c74613bc3700eacdce7dfedc382043013f452e321a13d8639b27817edbd1f1`、V2 proposal `e5bd219b7812b8ef97ef916226ac221e177f227808cd0dbc0bbe280920d1b70e`、原grid `78708759e0965e816d9d5b7aaa0bca92d2a6b92562930cd028dc87875d09468c`，原真实108 seal `ca8aa84c7485149c887abe7b60e8890f4c01e81b21e8ac46f19cf83866ff5da4`，v0.1规则 `ff34130b3c26a288dc4ad26420c1188e9f9f17940108475a003e260748f72ab1`和v0.1离线结果 `089b0c3fc13e9f84693452371d5b5c8a31f65c1dcb59e7cfcf7de69a15cb3df1`。
只允许用原36世界签署role-free P2/PAIR01 packets+TopK5文本/rank/B2 retained/removed和**正常在线可得的字段**。原Poison/Clean/HN标签、攻击target、C3、AI参考JSON、任何human review、原108**逐格**生成/评价、D1原候选编制F5和隐藏身份映射均不得进入算法进程，也不得用world_id、source_hash字面、文件顺序反推角色。过去聚合“Clean误删4/10、回答减少”等可作研究动机但不能为单个世界调规则。D2/D3、5090、B5/B6、D1-40完全隔离；C盘项目可控零写，D/E>=20GiB空闲，不下载安装任何新模型/大依赖，不调用任何新LLM Judge/在线搜索。

## 1. 最小 v0.2 算法代码（执行而非只写合同）

在`src/llmguard/domains/retrieval/hidden_poisoning/chinese5060/vesa_guard_v02.py`新增独立实现，不动`vesa_guard_v01.py`及旧B1/B2算法、过去的108次运行/Filter seal。只需最小`scripts/research/freeze_chinese5060_vesa_v02_g3.py`和tests；复用签署packet读取、`pilot_design.messages`、原TopK rank保护、旧V2 provider transport和封存机制。避免建新通用框架。

建议透明接口：
`select_v02(query, topk, b2_retained, observable_metadata=None)->Decision`
其中source metadata若没有外部证明，**自称官方、签署候选、chunk hash和权威文字均只算未验证**，不得把知道的标签映射造为可信。返回原TopK子集、被隔离/被恢复id、每条原文span与scope匹配、冲突/指令风险、覆盖要点差、风险级别、可复算rule hash、NO_TRUST_CLAIM。

**A｜中文多句事实与适用范围识别**
- 不用整段`fullmatch`作为唯一路径。基于局部正则/句边界/短语规则从自然中文（多句、不同标点、条件在前后、条号/版本不同写法、‘截至’日期、修订/施行/废止、否定、例外、金额/比例/数字含单位）抽取事实span、时间和scope，并记录精确字符位置/字节SHA。
- **不能**把正则命中/词汇出现直接等同“事实真实”“相同版本”；缺同一主体/属性/单位/时间的明确比较前提，关系UNKNOWN。对历史日期问题保留旧版可能正确。
- 模块不得依赖world_id名称/角色、源出处的AI推测，不能凭“年份更新”排序权威。

**B｜内容风险与冲突分级**
- 检查明显向LLM发命令/冒充system、忽略规则、要求泄漏引用等`INSTRUCTION_RISK`；对“对话中引用规则文本作为学术讨论”需有合成反例，避免词面误杀。
- 在可比较scope中仅对确切事实值/否定、时间限定与单位一致的明确冲突给`EXPLICIT_CONFLICT`；数值相同但同源复制不是独立证实，保留`CORRELATED_OR_UNVERIFIED`。
- 风险至少区分`HARD_BLOCK`（明确注入/明显不适用的版本/对当前问题明确冲突）、`CAUTIOUS_RESCUE_CANDIDATE`（未发现明确高风险但来源不受信）、`INSUFFICIENT_OR_AMBIGUOUS`（缺必需scope/覆盖、证据冲突不能解），不把无冲突=>可信。硬阻断证据及理由可审。
- 只从可观察的正文/span得出判断。**严禁**声称能在无上游独立来源元数据时证明“正确事实”或“安全”。

**C｜证据覆盖受限恢复（只对B2删项）**
- 基于原B2保留文本，按当前query涉及的显式主题/属性/必要槽位构造**文本可观测**覆盖表（有或缺、是否实际提供值/限制），与被删候选进行差量核对，记录具体独立span，不因‘多了段文本’就称增加证据。
- 每世界最多从B2移除集合恢复**1条**原TopK候选，必须同时通过：(i) 对所需主题/属性具体相关且补全原保留上下文缺少的一个明确槽位；(ii) 不存在明确越权指令、同scope不一致、可确认不适用版本；(iii) scope/单位/否定条件不产生可识别冲突；(iv) 恢复trace标记`RISK_ACCEPTED_NOT_PROVEN_TRUSTED`与未验证来源；(v) 选择仅用事前固定rank/ID排序，不依据世界标签、人工Gold、旧输出。
- 如只存在模糊相似、无法审计的‘看起来不错’或显式风险信号则保持隔离；不自动放回全部81个片段，不因D1 Clean标签而恢复。可以保守产生0差异，不能为满足API运行条件人为放宽阈值。
- 原TopK、chunk bytes、rank与C1–C5引用不变。不追加新来源、不改写证据、不修改Generator的中立system，不额外增加输入格式解释或模型提示。
- 设计一份v0.2**唯一预注册规则**（具体条件、前述单片恢复上限、确定性排序、可变参数=固定值），记录`RULE_SHA`，先用脱离D1训练/标注的合成中文自然句做正例、反例测试，覆盖多句话、复杂条件、相互冲突、明显诱导指令、同源重复、历史版本合法、否定例外、证据不足和空上下文。然后一次应用36世界并封SHA，不针对任何个例答案修改规则。

## 2. 必须交付真正的离线36世界实验结果

- 只在D/E私有仓储输出唯一`G3_V02_OFFLINE_GRID_PRIVATE.json`、`G3_V02_DECISIONS_PRIVATE.json`、`G3_V02_ROLE_BLIND_AUDIT.json`与冻结SHA，无原文入公开Git。36 world、每格query/model/system/JSON格式与旧V2完全一致，仅contexts选择变化；每个G3 context须是原TopK子集，引用原rank、原chunk text，固定顺序。不得跳过无变化的world，统一36分母。
- 事前冻结source commit+alg rule SHA+依赖版本+36请求hash；独立只读审计不同于算法本身，检查无评分/标签/目标泄漏，避免用世界顺序跨组配角色，输出`changed_worlds`、`restored_count`、新增隔离数、各证据风险类别、空上下文/覆盖、方法耗时，复核36个请求中的每处变化都能从文本与先验条件重算。任何标签泄漏或原TopK字节漂移立刻STOP。
- 若G3与G2 0差异，则`VESA_V02_NO_MEANINGFUL_DIFF`、真实0请求，写出**具体哪个规则阻断了多少候选**，不再开展一轮形式性准备；科研Owner可另行讨论新方法方向。若非零，先确保变化不是随机或只改变json键排序、并且没有刻意恢复明确高风险候选，再直达本合同“有条件真实”阶段。

## 3. 真正G3-v0.2模型调用：有条件但**一次授权全批**最多36

**Owner14已经批准**同一次最多36个真实G3调用，只有可核必需安全门通过才能发送；不需要“离线PASS后再请常规Owner批准”。
- 前置最小门：最终V02算法代码commit+规则SHA/36完整wire SHA及`OWNER14`原件字节hash；独立36格离线QA合格；仅已审D1北京Workspace范围的合法外传子集、没有敏感密钥/被明确限制的来源；同旧`qwen3.7-plus-2026-05-26`、同非思考JSON V2参数`max_completion_tokens=256`、temperature0/top_p1，唯一官方北京host/密钥从D/E私有配置读，不写Git。
- **旧Owner12单批USD预算豁免不继承**；账户当前额度/余额和全线已结算/在途数字需可核，按36条4096-token内且至多一次越限单发高档费用预留、>20% buffer，原`USD25 warn / USD28 stop new / USD30 global cap`与资金可用控制有效；用已有真实历史账/明确定值，不索取无必要发票。资金不明就STOP、只报告1个真实最小缺项，不能编造账本或拿¥0.13旧报价代替当前支付能力。
- 真调用按原36world顺序各一格G3，首3是本36格内工程检查，全部HTTP/identity/usage/schema/费用/PIN SHA通过后自动剩33；串行1、0自动重试/0额外探针/0Judge、write-ahead send_intent、首错STOP、全36槽SUCCESS/FAIL/NOT_RUN，不补跑、不重启新序列；每格返回`usage.prompt_tokens<=4096`及`completion_tokens<=266`候选界，缺usage/JSON异常/计费无法核等即停。模型响应不是“正确性验证”，不能按结果选择继续。
- 只在后封存评价侧读取旧G0/G1/G2 108真实输出及原D1 role，并按原36世界、12事实组做G3/G2/G1/G0配对；报告Poison候选恢复与Clean/HN留存的全分母、ABSTAIN变化、效率及费用。暂定参考不能把“字面原子命中”说成答案正确；Human Gold 0时正式ASR/QA/C3均NOT_MEASURED；如果G3回答增加伴随Poison更多应明确交易成本而非改进结论。不得把D1调参+评价作为外部独立试验，后续论文需留出集/消融。

## 4. 并行人工Gold：不阻碍算法但绝不泄漏

- 独立人工裁决的12题/38原子/16来源属先前未签审阅包。可**只在独立Reviewer权限中**组织材料分发、收集真实人审签注、复核引用授权，不得由Agent模拟人工、代签HumanGold、推测攻击目标或替独立Reviewer做标准答案。
- 并行任务与算法Worker隔离目录/权限/Git公开摘要，只能用摘要说独立人审完成了多少，不能把裁决或原语义参考混入`vesa_guard_v02`、训练、阈值或G3冻结前输入。Owner14授权不自动赋予外部Reviewer通信/材料外传权；无实际可访问合法Reviewer时记录`HUMAN_REVIEW_NOT_DISTRIBUTED`，不虚构已启动。

## 5. 一页交付、Git合规与STOP

状态只选：`VESA_V02_G3_36_COMPLETED`、`VESA_V02_G3_PARTIAL_STOPPED`、`VESA_V02_NO_MEANINGFUL_DIFF`、`VESA_V02_G3_GATE_BLOCKED`。一份主报告`docs/paper1/dual_machine/chinese5060/vesa_guard_v02/VESA_V02_OWNER14_RESULT.md`与脱敏`VESA_V02_G3_EVIDENCE_INDEX.json`；私有完整grid/trace/原回包/资金/角色映射只存D/E、严禁公开Git上传；必要AGENTS指定的Owner Register/Current State/Research Log/experiment master只追加最小必要记录。报告必须包含`parsed_query_worlds/parsed_chunk_count`（与v0.1 0/36、0/180比较）、`changed_worlds`、restored/deleted及明确风险处置理由、命中已召回Poison/Clean/HN（只能冻结后独立侧统计）、真实请求数和答案/拒答/Token/cost等（若运行）、源码SHA/36请求SHA/QA/Ruff/MyPy、真实资金核验状态和唯一剩余阻断。只在5060分支合法commit/push，远程核验HEAD、clean/0:0并STOP。禁止再创建一个同主题第3版并自启。优先交出可用的v0.2算法和真正离线变化，而不是再重复一轮预案审批。
