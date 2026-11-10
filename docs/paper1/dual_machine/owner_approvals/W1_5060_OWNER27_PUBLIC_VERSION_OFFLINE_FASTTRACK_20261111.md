# Paper 1｜Owner27：真实中文版本证据离线快速证伪批次（有界授权）

**PO-MHEP ID** `W1-OD-20261111-5060-PUBLIC-VERSION-OFFLINE-27`
**Owner原始指令（2026-11-11）**：“请尽快开启实验 快速推进验证实验”，并附上5060公开版本来源预检结果、8事实单位×8情境预注册草案，要求继续验证。该授权解释为批准**本文件界定的零外部模型与零商业API、分阶段离线研究**，绝非无条件许可复制/外传未知权利的第三方正文、消耗费用、Human Gold签署、解封其他数据或合并主线。
**Decision** `BOUNDED_OFFLINE_EXECUTION_APPROVED / GATED_DEV_FIRST / EVAL_CONDITIONAL`；
**Target branch** `research/paper1-chinese-defense-5060`，前置HEAD `667eb1a81d72a452fdea35028da63109b1191afb`；**执行起始状态** `APPROVED_NOT_RUN`。

## PO-MHEP 12字段
1. **Issue ID**：`W1-OD-20261111-5060-PUBLIC-VERSION-OFFLINE-27`。
2. **目标**：在真实可核中文版本事实基础上，用完全相同有序TopK5证伪“来源绑定+生效时间+适用范围联合门控，比同可信元数据预算的简单规则少误删正常证据、不增加Poison保留/HN误删”；失败保留版本敏感污染基准+RD中文失效分析路线。
3. **发现阶段**：Owner26七臂BLOCKED，RD_B2/RD_ZH各36世界复跑、Poison保留8/10和6/10、Clean误删4/10和5/10、HN误删2/9和4/9；完整七臂 DEV0/36，D1-28 0/84。Owner27预检已登记4谱系、10官网版本，仅3谱系5项确认变化，采集收据0、独立query0、Human Gold0。
4. **事实/推断/未知**：已核来源与旧基线是OBSERVED。当前5项已在开发材料暴露，不能进独立评价。新谱系可提供未暴露验证是HYPOTHESIS。未经核实的正文使用权、额外4事实单位、可信来源登记覆盖和现实过滤改进是UNKNOWN。
5. **继承约束**：AGENTS.md、PO-MHEP、Owner20 Rule-V2 NO_GO、R2公平对照、Owner25 Oracle合成不具同世界RD、Owner26 STOP与D1封存均不可变；D2/D3/HOLD8严格禁；5090 Claims不启动；HumanGold0、ASR/AnswerAccuracy未测。
6. **为何启动**：现在已有5个同对象真实版本变化，可立即进行离线DEV探针，比继续处理已blocked的D1 API账本更快产出可证伪方法证据。
7. **风险**：5项同属3谱系造成伪独立；网站版权/附件权利未知；同组训练评价泄漏；攻击者可控新版或多数伪造；“简单规则”和联合臂信息权限不等；简单规则已经能解决大多数样本；本地MiniLM/TopK漂移；以自动暂定标签冒充人工Gold。
8. **候选选项**：A 先限32 DEV世界并条件性32 EVAL离线、一次性评估；B 完全等待所有权利和人工审查再做任何科学试验；C 重试Owner26商业API七臂或旧D1（仍BLOCKED）。Owner当前加速要求采用A，但保留所有安全/质量阻断。
9. **建议**：分阶段自动执行，无需每个纯工程检查重新报批。优先使用**研究者自行撰写的事实等价中文片段**和自造的污染/背景段进行DEV，不批量抓取或外传原网页正文；所有代理上下文标 `SOURCE_GROUNDED_PARAPHRASE / NOT_NATURAL_ORIGINAL_DOCUMENT`。有确切来源使用权限与出处封存之后，才允许最小必要真实法条/政策摘录的本地研究使用；原始网页HTML/模板与附件不得默认可用。
10. **确信度**：高—现有5事实/隔离缺口；中—离线固定编码与TopK可复现；未知—联合方法比同权限简单规则的增益，任何正式RAG与论文外推。
11. **授权范围**：见下方阶段门；可对公开官网少量**元数据只读核验**，不批量抓取未知权利正文、无外传、无额外模型/依赖下载、无商业API；仅本地已缓存embedding在身份/依赖SHA通过后执行，CPU≤2线程，新增私有磁盘≤5GiB，始终空余≥10GiB，科学批次总墙钟≤90分钟（人工或新来源准备不以假计时绕限）。一次DEV v0，可在DEV内至多一次预登记v1；EVAL单次且不得结果后重新调参。
12. **停止/报告**：身份/权限/数据最小化/角色隔离/预注册/最小召回/可信收据或取样失败即STOP当前阶段，交 `BLOCKED` 或 `INCONCLUSIVE`，不能把少量有利世界改成完整分母。承认所有负例。禁止对D2/D3/HOLD8、5090、正式生成ASR、主线merge、商业API和正式HumanGold作任何越权操作。批次结束 `AUTO_CONTINUE=NO_OUTSIDE_OWNER27`。

## 阶段包与条件自动推进
**G0 输入与准入**：固定 `PUBLIC_VERSION_SOURCE_REGISTER_DRAFT.json`、`PUBLIC_VERSION_QUERY_PROTOCOL_DRAFT.md`、Git SHA；统计可用事实与谱系。建立证据类分级：URL/元数据 `PUBLIC_METADATA`，研究者自己撰写的同义事实段 `PARAPHRASE`，经逐源确认允许最小本地使用的官方原句 `AUTHORIZED_EXCERPT`；未知授权的第三方原句不得被下载后批量入库。公开网页可阅读≠允许向第三方API传输。权利未知不阻断使用新写的事实摘要做合成DEV，但这种试验只能算源事实约束代理。登记来源、日期、真正生效、对象/scope、原同版条款定位和可信来源独立性。未经独立审阅的Agent标签是`PROVISIONAL`。
**G1 DEV固定32世界**：既已暴露5个变更全部只可DEV/QA；从满足原草案条件的开发谱系以**预先公布的确定性组级选择**选4个事实单位，每单位8情境（32世界、160 TopK5槽），如4事实无法同时满足最低2谱系与条件，则减少并如实报告实际规模，绝不称32/32。独立出题视图只能见对象+地域/人群/时点+谓词，不见答案、Poison、参考差分；世界及角色映射、可信凭据与Gold各自分文件、隔离进程。攻击仅改低信任文档的事实值/条件/时间/伪身份，自造多源改写；不能更改固定query、rank、真实收据。先冻结query、角色盲TopK5、固定Index/背景/注入协议与SHA；若真实检索产生Poison密度不同于预期，不人工补齐。
**G2 T0/T1本地实测**：`T0={NONE,RD_B2,RD_ZH,DATE_ONLY}`；`T1={RD_ZH+SIMPLE_RECEIPT_RULE,RD_ZH+SOURCE_TIME_SCOPE_JOINT,RD_ZH+JOINT_NO_SCOPE}`。T0各臂相同TopK和相同原文编码；T1三臂拿完全相同的可信收据、来源谱系、effective interval和scope字段，收据来自独立可信registry而非待检文本/自称最新版；最简单规则也能读全部元数据，不准因信息限制人为削弱；JOINT_NO_SCOPE只消融使用、输入字节仍相同。要给出明确可运行算法伪代码/代码SHA、source-bind强度、作用域比较/冲突退避与同源去重，不把日期规则/投票/来源标签的组合当原创。全臂输出固定有序原TopK子集，禁止重新检索、改写、回填。DEV可一次v1，所有版本和负结果存档；不能因DEV胜出改Eval构造。
**G3 EVAL来源硬门**：拟在先前已见4谱系全部排除条件下，新确定至少4个未暴露事实单位、至少2个全新文档谱系，并至少2类不同签发来源组合（如不可能标INCONCLUSIVE，不降低条件）；EVAL 4组×8世界=32。材料归属/真实日期与范围逐条可核。预先冻结原句/研究者摘要类型、许可分级、查询和rank，评价标签来源。两名真实独立人工审核+分歧裁决才可称`HUMAN_REVIEWED_EVAL`；如没有人工，允许以与防御器隔离的独立进程先建立并封存`AGENT_PROVISIONAL`一次诊断评分，**只能**叫`EVAL_EXPLORATORY_PROVISIONAL`、HumanGold仍0，不能宣称正式GO/论文可发表泛化。不得后验换组或增补评价来达成PASS。
**G4 一次性评分与裁决**：全部臂于同一有序TopK预测、role-free seal、后独立Evaluator评分；每个预定事实单位及其8情境输出全体预测、候选召回/漏召回、Poison retained/retrieved Poison、Clean/HN误删/召回、非目标片段误删及无统一标签的背景删除单独记；source receipt覆盖、时间/scope误绑、同源3/5改写、4/5和5/5安全边界、Poison reinclusion、0/0分母处理、延迟median/P95，均按事实单位报告。预注册主门：联合臂相对**同T1收据简单规则**已召回Clean误删率至少降低50%（简单规则为0则UNDEFINED），Poison保留数与HN误删数均不增加，伪造可信来源提升0，Poison错误放回0；若联合与简单规则相同则`METHOD_NOVELTY_NO_GO`。32 Eval事实单位仅4组，报告配对世界/组差异与分母、Wilson可作描述但不做独立显著性/推广性宣称。T0 RD是基线迁移对照而不是T1信息公平对照。最终真实ASR、AnswerAccuracy、拒答与HumanGold保持NOT_MEASURED（除非另外正式人工签审）。
**G5 输出/停止**：向独立5060分支写 `OWNER27_OFFLINE_FASTTRACK_RESULT.md`, `OWNER27_OFFLINE_FASTTRACK_RUN_MANIFEST.json` 与query/数据/预测/评价/预算/来源只含脱敏hash的证据索引；逐项绑定执行命令、退出码、模型revision、输入SHA、代码SHA、过滤掩码、分母、错误、重复次数、无API的0费用；原始敏感文件留Git外。更新Tracker、Current Work State、Execution Log、Experiment Master、Project Master与必要human/agent ledger；仅在有新的Owner决定时更新Owner Decision Register，**本授权即新决定**。每阶段失败可停并归档部分DEV，不需要向Owner索要工程小批准。停止时给下一科研方向一句明确建议。

**解释：** 本批是新独立的公开来源版本离线科研批次，与Owner26 D1-28不是同一评价；Owner26 84/84未开始的记录保持0/84。不能把DEV32或Agent provisional Eval当作独立人类真值，也不能宣称模型生成防御已改善。
