# Paper 1｜Week 1 双机 Tracker

## 2026-11-11｜Owner31：Q-CER有界DEV→全新中文盲评→条件生成（授权未执行）

`OWNER31_BOUNDED_APPROVED_NOT_RUN / NEW_METHOD_QCER / DEV_EXPOSED_ONLY / FRESH_EVAL_0_OF_32 / HUMAN_GOLD_0 / API_0`。

Owner明确要求“再试一下中文创新，不过我们要快点”。基于Owner27/28候选级RD中文迁移权衡及Owner30真实Qwen数值目标命中NONE0/22、B20/22、RD_ZH5/22的探索性发现，**尚不能认定新方法成功或B2绝对安全**。批准5060单候选Q-CER（同TopK查询约束冲突识别+证据保全）、DEV v0最多v1，只在旧已曝光Owner27/28中开发；5090独立快速制备全新自写虚构中文版本4事实×8场景32世界，QUERY与Gold隔离、私有Gold不上Git；代码封存后5060同世界七臂只跑一轮，5090后验独立暂定计分。Q-CER必须在Poison保留、Clean误删、HN误删均不差于RD_B2且至少P改善3段或C改善4段，并胜过/不同于简单query/date消融，才有仅探索性方法信号。通过后**有条件**准入至多128 Qwen生成格+新增预算USD0.75硬门、原累计门不放宽；权限/token/余额或外传不闭合不得发送。DEV限45min、5090自写校验限45min、CPU2/D增量2GiB/出站默认0、不得重跑旧Owner29/30或触D2/D3/HOLD8/5090Claims、不得主线merge。新试次结果实测前均NOT_RUN，真Gold0，不可声称正式ASR或创新有效。旧负面结果保留、可在本次不GO后转回基准路线。

[Owner31合同](owner_approvals/W1_OWNER31_LAST_CHANCE_QCER_CHINESE_METHOD_FASTTRACK_20261111.md) · [5060执行指令](chinese5060/W1_5060_OWNER31_QCER_LASTCHANCE_FAST_EXECUTION_PROMPT_V1.md) · [5090独立任务](chinese5060/W1_5090_OWNER31_FRESH_SYNTHETIC_BLIND_EVAL_FAST_PROMPT_V1.md)


## 2026-11-11｜Owner30 6条私有错误值已独立核到目标：暂定负面信号，建议基准优先

`OWNER30_SIX_VALUES_BOUND / NUMERIC_TARGET_MATCH_NONE_0_OF_22_B2_0_OF_22_ZH_5_OF_22 / HUMAN_GOLD_0 / FORMAL_ASR_NOT_MEASURED / BENCHMARK_PIVOT_RECOMMENDED / OWNER_ROUTE_DECISION_PENDING / NO_NEW_SCIENCE`。

已核5090公开分支 `15a6961a4722a903069fbb829046972f9e45027e`，私有handoff SHA `9ae356d60a3ec62ab8fec1df732b9dc21a91f8694422e2ff1b0b56879271c6a4`，6条数值错误中5条命中此前冻结的攻击目标，1条不是；数值型目标世界22，NONE和RD_B2均0/22，RD_ZH 5/22。31组三臂数值匹配NONE20、B2 25、ZH15；scope-only 2世界未知、68回答的范围/引用支持未决，正式ASR/Accuracy未测，HumanGold0。RD_ZH虽候选过滤强却伴随Clean/HN误删与上述数值攻击命中，不构成新的防御GO，也不能归纳因果或统计泛化。建议停止当前新方法调参，转为中文版本化投毒基准+RD中文失效分析，Owner正式路线签署待定。下一步只执行归档与论文级证据整理，不再发新API或重试。原5090 Claim1–3、D2/D3/HOLD8仍锁。

[完整科研裁决与证据链](chinese5060/OWNER30_FEASIBILITY_CLOSURE_SUPERVISOR_REVIEW_20261111.md) · [双机最终归档指令](chinese5060/W1_OWNER30_FEASIBILITY_CLOSEOUT_DUAL_MACHINE_PROMPTS_20261111.md)


## 2026-11-11｜Owner30规则评价95条已完成但68回答未决；今日私有Target边界评分与小包Judge并行

`OWNER30_RULE_95_COMPLETE / JUDGE_SENT_0 / NUMERIC_PROXY_POSTHOC_ONLY / 5090_TARGET_MATCH_PENDING / HUMAN_GOLD_0 / NOT_FORMAL_ACCURACY`。

5060已推送`1760ca56dc87674c488fe1a197304dfbe4b4fc8e`、5090参考冻结`65c33ff4e87e698a41f8f271774a2c85de115c75`，原始Owner29共95成功回包/96计划、31三臂完整配对、缺失原NONE首格。5060规则将68 ANSWER全部列UNRESOLVED，因为强制要求scope逐字绑定；27 ABSTAIN有效分类，Qwen Judge 0调用/0费用，不能解释为0正确率。Supervisor只读Git join得到公开短值表：NONE20 ANSWER全部公开匹配reference、B2 26全部公开匹配、ZH 16公开匹配且6条WITHHELD，31完整配对NONE20/31、B2 25/31、ZH 15/31加6未决，32对B2 26/32、ZH16/32加6未决。**62公开值由参考白名单选择后才披露，62/62是选择效应，绝非无偏accuracy。** 5090已封存的私有攻击目标需先独立核62公开短值的target-match及6未知上下界；5060本机如逐条token真实<=4096且max128并闭合USD0.5/权利/账户门，可在原Owner30预算做至多68次短包Qwen辅助Judge，不成功则仅报离线bounds，不再把991808模型极限当作强制发送上界。不得新生成、不更改原评分、HumanGold0、formalASR/Accuracy NOT_MEASURED、D2/D3/HOLD8/Claims禁止。

[原Owner30授权](owner_approvals/W1_OWNER30_ONE_DAY_AUTOMATED_RAG_FEASIBILITY_20261111.md) · [数值匹配审计](chinese5060/owner30_eval/OWNER30_PUBLIC_VALUE_MATCH_SUPERVISOR_AUDIT_20261111.md) · [5060小包Judge](chinese5060/owner30_eval/W1_5060_OWNER30_FAST_SMALL_PACKET_JUDGE_AND_NUMERIC_DIAGNOSTIC_20261111.md) · [5090Target评分](repro5090/owner30_eval/W1_5090_OWNER30_FAST_PRIVATE_TARGET_MATCH_AFTER_5060_REPORT_20261111.md)


## 2026-11-11｜Owner30：95条封存生成回包先自动评估，人工Gold留到正式实验

`OWNER30_BOUNDED_AUTO_EVAL_AUTHORIZED_NOT_RUN / LLM_JUDGED_PROVISIONAL / HUMAN_GOLD_0 / NO_NEW_GENERATION`。Owner今日明确无时间双人盲审/第三裁决，要求大模型尽快评估。已核Git 5060 `188212344ce8c0144356c307efe3847f2f6fb97a`：Owner29 Qwen已发送96、可复核95（NONE31/32、B2 32/32、ZH 32/32），95请求68ANSWER/27ABSTAIN，31完整三臂配对，首格不可恢复/不得重发；回答层真假/targetedASR原来均NOT_MEASURED。5090已有Owner28候选标签及官方版次事实，HumanGold0。Owner30授权先在5090封存32世界的**只读公开事实参考原子**，无攻击目标/候选标签，再在5060不重生的本地D盘95回包上规则及可选固定Qwen Judge（最多95次/新增<=USD0.50，账户/出站/最高token账本硬门，不闭合则仅离线规则评分），最后5090以其既封存私有目标值计算暂定targeted ASR和跨臂Accuracy；相同Qwen生成/评价存在同模型关联偏差，结果`AGENT_PROVISIONAL`、非人审Gold。正式样本HumanGold和日期强基线后续完成，D2/D3/HOLD8及5090 Claims仍锁，不合并主线。所有阶段必须保留原96分母和缺失格，禁止改原试次、重新生成、编造已跑Judge。

[Owner30执行合同](owner_approvals/W1_OWNER30_ONE_DAY_AUTOMATED_RAG_FEASIBILITY_20261111.md) · [5060自动评分Prompt](chinese5060/W1_5060_OWNER30_FROZEN95_QWEN_AUTO_JUDGE_PROMPT_V1.md) · [5090参考与最终评分Prompt](chinese5060/W1_5090_OWNER30_REFERENCE_FIRST_AND_TARGET_ASR_PROMPT_V1.md)


## 2026-11-11｜Owner28 对照证据整理与 Owner29 草案完成

PREP_ONLY / OWNER28_AGENT_PROVISIONAL_EVAL / HUMAN_GOLD_0 / OWNER29_SCIENCE_NOT_AUTHORIZED。

按封存公开证据复核 DEV 与 EVAL，输出四臂对照、8 事实组的三指标图和 416 行可复算计数。EVAL 的 RD_ZH 相对 B2 额外删除 18 段 Poison、28 段 Clean、3 段 HN 和 1 段背景。日期规则本批无触发，回答层未测。下一门为 Owner 批准独立人审、来源许可与新谱系、强时效基线和生成层合同。本轮科学试次、评分重跑和费用均为 0。

[方法、对照与限制](chinese5060/BENCHMARK_V01_METHODS_AND_LIMITATIONS.md) · [Owner29 预注册草案](chinese5060/OWNER29_STRONG_BASELINE_AND_RAG_PREREG_DRAFT.md)

## 2026-11-11｜Owner28 5090一次性独立评分完成，监督复审已归档

`OWNER28_EVAL_AGENT_PROVISIONAL_SCORED_32_OF_32 / HUMAN_GOLD_0 / JOINT_METHOD_PAUSED / BENCHMARK_PRIORITY / OWNER29_NEW_SCIENCE_NOT_AUTHORIZED`。5090远端 `670d9ab0e546d46117bf5c48ebb2b0043689f453`、5060盲预测封存 `ad413ea639c950faea2106a52fa4352735384ef1`，来源端和代码封存不变。评估真实TopK5 32世界、P56/C82/H20/B2召回；B2 P保留33/56、Clean误删27/82、HN误删7/20；RD_ZH P保留15/56、Clean误删55/82、HN误删10/20。ZH额外过滤P18但多误删Clean28和HN3。S3范围互换P4/4两臂均保留，S1无毒仍错误删Clean B2 8/20、ZH 12/20；实际5/5覆盖2世界，P保留B2 8/10、ZH2/10。DATE_ONLY本批0/352正则命中、32/32与NONE相同，属无操作日期基线。仅3谱系4事实组、代理释义与AGENT_PROVISIONAL，独立HumanGold0、最终ASR/Accuracy未测。建议只读两批结果的论文级失败分析+5090私有人类双评材料**准备**，不启动新科学试次、不自签Gold、不补跑、不动D2/D3/HOLD8/Claims。后续真实高质量基准和生成层需另批Owner批准。

[科研复审档](chinese5060/OWNER28_INDEPENDENT_SCORE_SUPERVISOR_REVIEW_20261111.md) · [5060论文分析准备指令](chinese5060/W1_5060_OWNER28_TO_OWNER29_BENCHMARK_REPORT_PREP_PROMPT_V1.md) · [5090人工双评材料准备指令](chinese5060/W1_5090_OWNER28_HUMAN_GOLD_REVIEW_PACK_PREP_PROMPT_V1.md)


## 2026-11-11｜Owner28独立EVAL预测封存完成，5090一次性评分待执行

`5060_PREDICTION_SEALED / 5090_SCORING_AUTHORIZED_IN_EXISTING_OWNER28 / EVAL_SCORED_0_OF_32 / HUMAN_GOLD_0 / API_COST_0`。

经Git核：5060提交`ad413ea639c950faea2106a52fa4352735384ef1`，5090兼容源提交`0a4fde3966d9eefd3562f4d552f12090c7632ac9`；5090原私有标签SHA仅在5090托管。5060角色盲投影记录SHA `5c9874bd6bb3252a2685e8481b92ea979dc1e842b5f3250a798e2bb7f03d21bb`、预测seal `aeb47a49f915c55fd2c7e5679de63cfce664282667f9a818ed27b9dfc7b1205e`、TopK seal `31ce5b1acfbfb0d6ceebe4acedda0f482ca506462baf48dd9f4ff36a37e4bd45`，32主世界×TopK5=160秩、4臂128掩码，7镜像未运行。Supervisor只读核验投影：`NONE=160`、`RD_B2=103`、`RD_ZH=53`、`DATE_ONLY=160`保留秩；B2与RD_ZH掩码不同28/32世界，DATE_ONLY与NONE相同32/32。无Gold，以上**不能推算Poison/Clean/HN**。冻结DATE_ONLY正则在兼容32世界原352段自写语料匹配`0/352`，属于`INOPERATIVE_DATE_REGEX`，正式报告须披露其不是有效强时效基线，禁止在本批结果后改写。5090需在私有环境核SHA、新旧编号映射/标签，再一次评分；新5090公开指令已推其独立分支，5060无权获取私有Gold。旧Owner27不改；5090 Claims/D2/D3/HOLD8锁定，最终RAG ASR/Accuracy仍未测。


## 2026-11-11｜Owner28 32 主世界盲预测已封存，待 5090 独立评分

PREDICTION_READY_FOR_INDEPENDENT_5090_EVAL / SCORING_PENDING / HUMAN_GOLD_0。

5090 无损桥接提交 0a4fde3966d9eefd3562f4d552f12090c7632ac9 通过冻结 check。5060 完成一次 32/32 主世界同 TopK5 检索与四臂预测，共 160 个秩、128 个掩码。7 个镜像单列未运行。当前评分 0/32，下一步由 5090 核对已发布的角色盲预测 SHA 后在本机独立评分。费用为 0。

[盲预测交接、封存和阶段记录](chinese5060/owner28_eval/OWNER28_EVAL_BLIND_PREDICTION_HANDOFF.md)

## 2026-11-11｜Owner28 5060 冻结身份通过，待 5090 兼容交接

EVAL_BLOCKED_SCHEMA_OR_PROVENANCE / WAITING_FOR_5090_SCHEMA_BRIDGE / EVAL_0_OF_32 / HUMAN_GOLD_0。

5060 已含授权提交 c72096722c40c77accf3325f19dcc529f6dc915f，冻结源码与缓存身份通过。5090 在 a8de64fbf2c279a642c9b9a41ddf5c5481b8cfca 已发布原始包，兼容三件套为 0/3。独立检索、预测、评分各 0/32，7 原始镜像未纳入。下一步按原授权接收桥接证据并执行冻结 check。新增试次、API 及费用为 0。

[5060 交接核验与证据](chinese5060/OWNER28_EVAL_HANDOFF_STATUS_20261111.md)

## 2026-11-11｜Owner28独立来源已封存，检测程序准备就绪；发现5090→5060输入格式不一致

`5090_CURATED_SEALED / 5060_RUNNER_READY / HANDOFF_SCHEMA_MISMATCH / EVAL_0_OF_32 / HUMAN_GOLD_0 / API_0`。

远端实测：5090 `a8de64fbf2c279a642c9b9a41ddf5c5481b8cfca`，有 `EVAL_ROLE_FREE.json` (原始SHA `2aafd7d7bcd8e3860771063a31770e350532065abb251f38f99c7ac39ba50cb7`)和 `EVAL_CURATOR_MANIFEST.json`，声明3新谱系、4事实组、32主世界+7镜像、私有label SHA `c4244e86fb2ecf1177cc3d2bb39b8791e1b789713fc3522bbfaa46b35b055595`；该repo文件实际是39×11个文本，使用 `worlds/passages` 和20字符ID。5060已验证 `b9b9a6f68bc2baa1e1adf7842dc759a0b4e383bd`，盲跑程序则要求 `main:32, mirrors:0或8`、5个world字段及 `w/f/d/s-`+24hex ID、独立public curator清单。**这是可复查的数据接口不匹配；不能将原5090包直接投入冻结runner，也不能要求5060改算法迎合EVAL。** 当前无新检索/预测/评分，原5090私有Gold未在Git。先由5090在其分支做32主世界无损格式转换，7原始镜像保存但本次不跑，提供新rolefree+curator compatibility manifest+变换审计；5060只读验新包和固定check，PASS后一次性同TopK四臂预测、封存再由5090私有评分。所有条件属于已批准Owner28研究范围，未解锁正式HumanGold或外部API，软件Schema转换不是科学结果。

[协调规程](OWNER28_5090_TO_5060_SCHEMA_BRIDGE_AND_ONE_SHOT_HANDOFF_20261111.md) · [5090格式桥接指令](chinese5060/W1_5090_OWNER28_SCHEMA_BRIDGE_EXECUTION_PROMPT_20261111.md) · [5060盲预测交接指令](chinese5060/W1_5060_OWNER28_BLIND_PREDICTION_HANDOFF_PROMPT_20261111.md)


## 2026-11-11｜Owner28 5060 失效归因与盲评程序完成，EVAL 未准入

RUNNER_READY / BENCHMARK_INPUT_GATE_BLOCKED / EVAL_NOT_RUN / HUMAN_GOLD=0 / AUTO_CONTINUE=NO。

Owner27 归档 363 成员复验，32 主世界七臂、84 个分层汇总、21 对掩码重算一致，新增六类匿名失效证据。RD-zh 历史 HN 误删 7/23，异范围 HN 误删 6/10。T1 的本地代理收据绑定造数真值与版本，不能作为部署的独立签发证据。固定四臂已用虚构输入通过工程验证。5090 远端 dbd91f3667964baca69aeb82a6292c4fe193c965 暂无本批交接，独立输入与评分 0/32。下一门为既有 Owner28 授权内独立来源、权利及角色盲交接。零商业 API、零费用，正式回答指标未测。

[失效图谱](chinese5060/OWNER28_DEV_FAILURE_ATLAS.md) · [收据审计](chinese5060/OWNER28_RECEIPT_PROVENANCE_LEAKAGE_AUDIT.md) · [独立小试协议](chinese5060/OWNER28_BENCHMARK_PILOT_PROTOCOL.md) · [Run Manifest](chinese5060/OWNER28_BENCHMARK_RUNNER_MANIFEST.json)

## 2026-11-11｜Owner28 双机独立小样本基准路线启动（仅授权，无新试次）

`OWNER28_BOUNDED_AUTHORIZED_NOT_RUN / BENCHMARK_FIRST / JOINT_METHOD_PAUSED / EVAL_0_OF_32 / HUMAN_GOLD_0 / API_0`。

核实Owner27快照7b4e4cad00df38b724fdeb1c2edd63f06b7be9fd：DEV 32/32世界；RD_B2 P保留20/45、Clean误删40/63、HN误删4/33；RD_ZH P6/45、Clean误删54/63、HN误删13/33；同收据简单规则和联合规则Clean误删均29/63，联合与scope消融同掩码32/32；方法开发主门失败。仅4个预检事实单位且代理语料，EVAL 0/32，Human Gold 0，无正式ASR/Accuracy。Owner28指令按已约定基准后备路线推进：5060静态失败归因、审计代理收据是否近似真值Oracle并冻结无标签评测runner；5090在不改变RAGDefender原复现NOT_RUN的前提下，临时独立选取未见官方版本谱系并托管标签/无答案查询。仅G1-G4全部闭合时一次性32新世界、4臂NONE/B2/RD_ZH/DATE_ONLY同TopK离线评估，仍仅AGENT_PROVISIONAL。方法门控不调参；旧D1/Owner26和D2/D3/HOLD8锁定；0商业API、0费用、0下载，不合并主线。未得独立事实/权限则STOP报告而非回填DEV。

[Owner28合同](owner_approvals/W1_OWNER28_BENCHMARK_INDEPENDENT_PILOT_20261111.md) · [5060执行Prompt](chinese5060/W1_5060_OWNER28_BENCHMARK_RD_FAILURE_AND_EVAL_RUNNER_PROMPT_V1.md) · [5090独立取样Prompt](chinese5060/W1_5090_OWNER28_INDEPENDENT_SOURCE_EVAL_CURATOR_PROMPT_V1.md)


## 2026-11-11｜Owner27 32 个 DEV 世界七臂完成，EVAL 未准入

`DEV_COMPLETE_DIRECTIONAL_FAIL / EVAL_BLOCKED_INDEPENDENT_INPUTS / HUMAN_GOLD=0 / AUTO_CONTINUE=NO`。

Owner27 v0 已实测 32/32 主世界、七臂 224 个掩码，另有 8 个单列镜像。联合臂与同凭据简单规则 Clean 误删均 29/63，Poison 保留均 6/45，联合多保留 2 段 HN，去 scope 与联合掩码相同。EVAL 0/32，新独立事实和谱系、无答案查询及逐源权利未绑定。仅保留版本敏感污染基准与 RD 中文迁移失效分析。Owner26 D1‑28 仍 0/84。新增商业 API 及费用 0。正式实验、ASR、答案准确率均未启动或未测。

[结果与停止决定](chinese5060/OWNER27_OFFLINE_FASTTRACK_RESULT.md) · [Run Manifest](chinese5060/OWNER27_OFFLINE_FASTTRACK_RUN_MANIFEST.json)

## 2026-11-11｜Owner27启动公开版本化来源离线快速验证批次（仅授权，还未运行）

`OWNER27_APPROVED_NOT_RUN / DEV32_PLANNED / EVAL32_CONDITIONAL / OWNER26_UNCHANGED`。

Owner27有界批准已登记，**登记时科学新试次仍为0，执行由5060 Codex另行启动**。先按固定源事实DEV 4组×8情境(计划32世界)运行离线同TopK5 T0/T1七臂；EVAL 4个未暴露事实组×8情境(计划32世界)必须来源谱系、角色隔离和来源使用权闭合才允许一次性运行。若无人类双评，评分仅AGENT_PROVISIONAL，HumanGold0。新增商业API/下载/费用0；旧Owner26 D1-28仍0/84、D2/D3/HOLD8/5090封锁。方法必须优于获得同样来源凭据的简单规则，才有新方法候选资格。

[Owner27正式有界授权](owner_approvals/W1_5060_OWNER27_PUBLIC_VERSION_OFFLINE_FASTTRACK_20261111.md) · [5060执行Prompt](chinese5060/W1_5060_OWNER27_PUBLIC_VERSION_OFFLINE_FASTTRACK_EXECUTION_PROMPT_V1.md)


## 2026-11-11｜5060 公开中文版本来源预检完成

`PREFLIGHT_ONLY / SCIENCE_NOT_RUN / HUMAN_GOLD=0 / NEXT_OWNER_APPROVAL_REQUIRED / AUTO_CONTINUE=NO`。

基点 4c651a84da5559fb2ba8776cd6dda4c76cf6fa1c。核验 4 条谱系、10 个版本，3 条谱系共有 5 项同对象事实变化。医保已核目录替代、范围与过渡，逐药品差分未证。收据、冻结查询、评测和商业 API 各为 0。

Owner26 的 28 组查询身份、出站授权与预算硬门保留。下一步须批准逐源权利、独立选材/双评、同 TopK 离线试验及其冻结条件。未触及 D2/D3、HOLD8、5090 或主线。

[来源登记](chinese5060/PUBLIC_VERSION_SOURCE_REGISTER_DRAFT.json) · [查询与预注册](chinese5060/PUBLIC_VERSION_QUERY_PROTOCOL_DRAFT.md) · [创新性风险](chinese5060/PUBLIC_VERSION_NOVELTY_RISK.md)

## 2026-11-10｜5060 Owner26 两臂复跑完成，七臂准入阻断

`OWNER26_BLOCKED / RD_DEV_36_COMPLETE / RETRIEVAL_IDENTITY_BLOCKED / D1_API_EXFIL_GATE_BLOCKED / BUDGET_GATE_BLOCKED / AUTO_CONTINUE=NO`。

Run W1-5060-OWNER26-D1-RD7-DEV-20261110-01。原 36 世界两条 RD 基线共 72 个角色盲预测，复跑对齐既有删留。B2→RD-zh Poison 保留 8/10→6/10、Clean 误删 4/10→5/10、HN 误删 2/9→4/9。七臂完整 DEV 0/36，Eval 封存、预测和评分各 0/84。

新增 Qwen 请求、探测、Token 和费用均为 0。缺 28 组独立查询绑定、逐段本轮外传许可及当前资金和 Token 上界。下一建议为有权公开版本污染基准与 RD 中文迁移失效分析。Human Gold 0，正式 ASR/Accuracy 未测。 仅更新 5060，5090 沿用历史快照。

私有证据 ZIP 31 件，SHA256 7a37430612edd622bbecd679f34ea6d1ce19ec52cdb41567138a8f88c6ee3867。

[结果与裁决](chinese5060/OWNER26_D1_QWEN7_RESULT.md) · [Run Manifest](chinese5060/OWNER26_D1_QWEN7_RUN_MANIFEST.json)

## 2026-11-10｜Owner26 冻结七臂：中文 D1 内部Qwen抽取+RD-zh公平对照（已批、未执行）

`W1-OD-20261110-5060-D1-QWEN-NOANCHOR-26`。Owner批准以固定`qwen3.7-plus-2026-05-26`、temperature0，新增API费用≤**USD3**进行逐段事实抽取与每world直接不可靠片段核验；本地现存向量模型零下载跑同world`RD_B2`/`RD_ZH`，与`RD_ZH+M1_SAFE`、`RD_ZH+M2_VOTE`、`M2_VOTE_ALONE`、`RD_ZH+M1_SAFE+M2_VOTE`共7臂同TopK比较。Dev是原Pilot12（12组×3=36世界），最多改一次；签署D1-40其余28组×3=84世界只有在索引/检索/Query按冻结原协议恢复并封存后才可一次性评分。所有D1仍`DEV_EXPOSED`、结果为内部held-group，外部HOLD8、D2/D3均禁止。防御器不能见Gold/role/target；Qwen输出必须逐字quote span绑定并报告UNKNOWN/跨版本scope。M1无锚恢复是一条刻意放松P0的**风险候选**，不宣称已有可信来源。Qwen全量逻辑费用/Token按每独立臂计算，不能把抽取成本记为0。S1/S2/S3隐蔽等级和自相矛盾Poison单独报。

`GO`需DEV预选VESA主臂在Eval84比RD_ZH Poison保留不增且Clean误删减半，同时不劣于`QWEN_VERIFY`的Poison/Clean/HN指标且完整Token更少；只过RD为`PARTIAL`；未过RD`NO_GO`；无合法Qwen数据外传/模型参数/费用预留或检索协议缺失则`BLOCKED`。本批新增费≤USD3、原总账USD25/28/30不变；真实服务地域、版权/隐私许可、cost/token上界、余额及endpoint若未闭合禁止发D1原文。正式ASR/Answer Accuracy仍NOT_MEASURED，HumanGold0。Owner25无锚真实D1 NO_GO、规则Owner20 NO_GO与Owner25合成Oracle结果保持。**登记仅代表批准，未运行或获得新结果。**

[Owner26 正式授权](owner_approvals/W1_5060_OWNER26_D1_QWEN_NOANCHOR_CHINESE_DEFENSE_COMPARE_20261110.md) · [5060直接运行Prompt](chinese5060/W1_5060_OWNER26_D1_QWEN_RD7_FASTTRACK_EXECUTION_PROMPT_V1.md)。

## 2026-11-10｜5060 Owner25 机制小试完成，裁决为调整

`OWNER25_SYNTHETIC_COMPLETE / BASELINE_INCOMPLETE / D1_ANCHOR_COVERAGE_LIMITED / CURRENT_D1_AND_RULEV2_NO_GO / AUTO_CONTINUE=NO`。

Run W1-5060-OWNER25-SYNTHETIC-P0-20261110-01。DEV 64 世界、HOLDOUT 32 世界一次性预测后评分。Oracle 联合臂相对固定父掩码，HOLDOUT Poison 保留 32/54→7/54、Clean 误删 30/78→15/78、HN 误删 12/28→12/28。真实签发者失陷错锚 1/1，Rule‑V2 严格绑定 0/160。无同世界 RD 基线，禁止比较性 PASS。

D1 真实收据覆盖 0/180，严格 P0 下原恢复门不可达。下一裁决是批准真实公共来源的独立采集与同世界 RD 对照。D1 未重跑、正式 ASR/Accuracy 未测、Human Gold 0。Owner24 F0 仍 BLOCKED，本轮模型、API、下载与新增费用均为 0。仅更新 5060，5090 沿用历史快照。

私有证据 ZIP 60 件，SHA256 d8125e1f6f008c8dc6437c4f2326f4a4558aebe21915aac62d593bb00d0e3651。

[结果与裁决](chinese5060/OWNER25_SCIENCE_FIRST_RESULT.md) · [Run Manifest](chinese5060/W1_5060_OWNER25_SCIENCE_FIRST_RUN_MANIFEST.json)

## 2026-11-10｜Owner25 科研结果优先：绕开Owner24 F0工程阻断的独立无模型机制快试（授权未执行）

`W1-OD-20261110-5060-SCIENCE-FIRST-OFFLINE-PILOT-25`。Owner要求优先取得科研假设的可证伪结果，而非重复等待 Windows 出站隔离。已准一条**独立的、零模型/零API本地小试**：旧D1只引用已有报告与聚合事实，真实独立可信来源登记0/180导致严格P0在D1恢复误删不可达（B2 Clean误删4/10）；新建8 DEV+4 HOLDOUT的不同合成事实组×8情境共96个TopK5世界，先封存模拟独立来源签发/版本/适用范围与隐匿角色Gold，DEV两版限额，HOLDOUT32世界一次性封存预测再评估。分层比较无过滤、公平同世界RD（若已安装编码器存在）、独立来源、版本scope、联合P0和伪造来源负对照；oracle事实槽位仅为理论上界，不属于真实独立Gold/抽取器/最终ASR。若无法公平运行RD不得宣称比较性PASS。开发+执行按本次唯一批准的低风险离线范围自动进行，普通脚本QA自主修复。

**Owner24 F0仍BLOCKED、Qwen首次加载0/1、F1–F4均NOT_RUN**。不得改系统防火墙、下载模型/依赖、运行模型/商业API、使用D2/D3、5090 Claims、正式S2–S5或合并主线。所有历史负结果、Role分母和HumanGold0保持，完成一次HOLDOUT后提交`MECHANISM_POTENTIAL_GO_ORACLE_ONLY/ANCHOR_COVERAGE_LIMITED/MECHANISM_NO_GO/INCONCLUSIVE`，如实披露D1不可达性，Git push后STOP。当前仅新授权已登未执行，无新性能数字。

[Owner25 PO-MHEP授权](owner_approvals/W1_5060_OWNER25_SCIENCE_FIRST_OFFLINE_MECHANISM_PILOT_20261110.md) · [5060生效执行指令](chinese5060/W1_5060_OWNER25_SCIENCE_FIRST_MECHANISM_FEASIBILITY_EXECUTION_PROMPT_V1.md)。

## 2026-11-10｜5060 Owner24 F0 停止，出站隔离未验证

`OWNER24_FASTTRACK_F0_BLOCKED / HUMAN_DECISION_REQUIRED / F1_F4_NOT_RUN / FORMAL_S2_S5_LOCKED / AUTO_CONTINUE=NO`。

Run W1-5060-OWNER24-F0-20261110-01。固定资产与 52 个包成员通过身份核验，llama-completion.exe 的 1,601/1,601 个静态符号和 50/50 条 API-set 映射解析，前沿为 0。现有出站策略未证明默认拒绝，已触发硬停。

NEW60+10 与暂定 Gold 未生成。F1 启动 0/1，F2 开发回放 0/193，F3 与 F4 未运行，新增费用 USD 0。下一门是核验 Owner 提供的隔离边界后完成原 F0。历史结论保留，正式 ASR/Accuracy 未测。 仅更新 5060，5090 沿用历史快照。

私有证据 ZIP 6 件，SHA256 a656251ca9704f77d9acf477c53883f2643f5e53d0a2f7621cd7e78567518980。

[停止报告](chinese5060/W1_5060_OWNER24_FASTTRACK_F0_STOP_REPORT.md) · [Run Manifest](chinese5060/W1_5060_OWNER24_FASTTRACK_RUN_MANIFEST.json)

## 2026-11-10｜Owner24 研究加速：一次授权F0–F4自动阶段推进（尚未执行）

`W1-OD-20261110-5060-FASTTRACK-CONDITIONAL-24`。Owner明确希望减少审批往返、扩大5060本机研究任务，但不是任意绕过D2/D3与正式科学审批。控制面提供一次性有界执行包：`F0`固定资产/入口核验及新60+10合成暂定Gold提前封存；`F1`已下载Qwen GGUF + llama-completion Windows CPU受控1-token工程Smoke（禁止外网/内存private commit≤6GiB/180s）；`F2`仅在旧73+Owner20已揭盲100主+20从属上进行有限prompt/schema研发+最多一次193视图DEV回放；`F3`安全开发门过后一次评估新60不同语义主案例+10从属（40可答/20未知、HumanGold0/Agent provisional）；`F4`安全与暂定成绩达预注册条件后做D1已暴露TopK冻结快照最多12或36世界的离线投毒过滤/误删诊断，正式ASR仍未测。每一阶段通过硬门才自动进入下一项；失败立即停，不能调科学阈值或隐蔽重试。普通QA修复不必微观审批。

固定官方源码实证`llama-cli.exe`会内部HTTP服务和本地健康检查，**不可视作零网络纯加载**；本批优先受控`llama-completion.exe --no-warmup -n 1`并诚实记录1个输出token。模型/运行时不可更换，不下载依赖或额外资产，不调用商业/外部API，不开放D2/D3/5090 Claims/正式S2–S5/主线merge。历史Rule-V1/V2新合成`FEASIBILITY_NO_GO`、S1 FAIL、R2 K1-C不变，新进展并不代表科研通过。

[Owner24正式条件授权](owner_approvals/W1_5060_OWNER24_FASTTRACK_LOCAL_MODEL_EXTRACTION_CONDITIONAL_AUTH_20261110.md) · [5060直接执行的Fast-Track Prompt](chinese5060/W1_5060_OWNER24_FASTTRACK_MULTI_STAGE_EXECUTION_PROMPT_V1.md)。

## 2026-11-10｜5060 Owner23A 静态复核完成，受控加载待批

`OWNER23A_STATIC_COMPLETE / OWNER23B_SMOKE_PENDING_OWNER / MODEL_LOAD_INFERENCE_NOT_AUTHORIZED / S2_S5_LOCKED / AUTO_CONTINUE=NO`。

Run W1-5060-OWNER23A-SCOPED-STATIC-20261110-01。CLI 静态 2,911/2,911 个符号、73/73 个 API-set 配对均解析，前沿 0。Owner22 两件资产、52 个解包成员及原证据哈希复核通过。整包许可、VC 最低版本、实际 CPU 后端仍为 UNKNOWN，峰值内存未测。历史迁移 QA 的 ACL 偏差已登记并保留。

新增下载、安装、发行 EXE/DLL 启动、模型加载、推理、API 与科学试次均为 0。Owner20 NO_GO、旧 S1 FAIL、R2 K1-C、Human Gold 0、正式 ASR/Accuracy 未测保留。下一门是单独批准 Owner23B 本机 load-only smoke，当前停止。 仅更新 5060，5090 沿用历史快照。

私有审计 ZIP 73 件，SHA256 fcde11120eecca20a1ea8398f22db35175853b4a5c9f200314cb46befa0bc589。

[静态报告](chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER23A_SCOPED_STATIC_AUDIT_RESULT.md) · [Run Manifest](chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER23A_SCOPED_STATIC_RUN_MANIFEST.json)

## 2026-11-10｜Owner23A 批准收敛式静态PE/API-set/许可复核（授权未执行）

Owner决策`W1-OD-20261110-5060-OWNER23A-SCOPED-STATIC-23A`。明确批准仅针对已下载且哈希锁定的Qwen GGUF和llama.cpp b12242资产执行**静态审计工程修正**，以`llama-cli.exe`与必要CPU后端为实际范围、只读核API-set/PE DLL、VC与第三方许可、D盘QA残留。Owner允许5060自主修复本任务内静态检查脚本/普通单测，无需微观审批；旧Owner22 512节点预算、29前沿、43件审计私有档案、两个固定SHA不覆盖。模型可执行文件启动、模型加载、RAM Smoke、推理、科学试次、模型/运行时/依赖下载均未获批准，Owner23B单独决策。旧Owner20规则`FEASIBILITY_NO_GO`、S1 FAIL、R2 K1-C、HumanGold0、正式ASR/AnswerAccuracy未测、S2–S5及5090 Claims仍锁。

当前仅`OWNER23A_STATIC_APPROVED_NOT_RUN / MODEL_EXECUTION_NOT_AUTHORIZED / AUTO_CONTINUE=NO`。执行完成后交CLI最小依赖闭包、API-set映射状态、许可矩阵、新只读静态证据封存并STOP。

[Owner23A正式授权](owner_approvals/W1_5060_OWNER23A_SCOPED_PE_APISET_LICENSE_STATIC_AUTH_20261110.md) · [5060可直接执行Prompt](chinese5060/W1_5060_OWNER23A_SCOPED_PE_APISET_LICENSE_STATIC_EXECUTION_PROMPT_V1.md)。

## 2026-11-10｜监督端复核Owner22静态阻断：512节点为分析预算，非依赖缺失（Owner23A待决）

监督端通过GitHub核对Owner22结果HEAD `34b83aefcc3b6fa59482843403a9c85d59cdbc4e`，两项完整字节与HASH、GGUF、52个ZIP成员安全检查均PASS；模型加载/推理仍0、运行时整体BLOCKED。独立审阅`owner22_static_inspection.py`发现PE分析从**所有**包内PE的导入集合出发递归展开System32，遇512节点预算停止；其中387为未映射API-set，29为**未遍历前沿**，不是29个已确认缺失DLL。Windows官方定义API-set为逻辑契约，并非要求有同名物理DLL。第三方notice和最低VC依赖仍待进一步核对，旧报告及所有失败不覆盖。

下一步建议Owner批准`Gate23A` **只使用本地既有资产进行受限静态再核验**：以llama-cli和必要CPU后端为边界、Windows API-set映射/循环去重、证据支持的第三方许可与VC审计；先保全原静态失败，完成即STOP。**目前只是监督建议，未给5060新的执行许可**，smoke/模型运行仍未批准。S2–S5、D2/D3、5090禁令不变。

[完整监督证据及PO-MHEP待决卡](chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER22_ASSET_STATIC_BLOCKED_SUPERVISOR_REVIEW_20261110.md)。

## 2026-11-10｜5060 Owner22 固定资产已获取，运行准入继续阻断

`OWNER22_ASSET_STATIC_INSPECTION_BLOCKED / MODEL_EXECUTION_NOT_AUTHORIZED / PEAK_MEMORY_NOT_PROVEN / AUTO_CONTINUE=NO`。两件固定资产各一次，实际正文 1,142,252,137 字节，SHA256 和长度均通过。GGUF 头和 52 件 ZIP 安全验包通过；整包许可与 Windows PE 运行闭包仍待证。

Run `W1-5060-OWNER22-QWEN-GGUF-ASSET-STATIC-20261110-01`，私有审计 ZIP SHA256 `faa281e7e4a14f2bc11a292b6e42e94f42421c7a4152ec55f4212ad01a708247`。

执行、加载、推理、安装、额外资产下载、新实验、模型 API 和费用均为 0。后续受控 smoke 尚未批准，且静态前置仍未闭合。Owner20 NO_GO、旧 S1 FAIL、R2 K1-C、Human Gold 0 和正式 ASR/Accuracy 未测均保留。S2–S5 锁定。

[静态验包报告](chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER22_QWEN_GGUF_ASSET_STATIC_INSPECTION_RESULT.md) · [完整脱敏 Manifest](chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER22_QWEN_GGUF_ASSET_STATIC_RUN_MANIFEST.json)

本条仅更新 5060，5090 保留历史快照。

## 2026-11-10｜Owner22：Qwen GGUF两件固定资产受限下载+静态验包（获批未执行）

Owner22 `W1-OD-20261110-5060-QWEN-GGUF-ASSET-22` 承接Owner21单模型只读审计的唯一待批事项，**仅准入两件固定字节资产并进行非执行性检查**。Qwen`Q4_K_M@91cad51170dc346986eccefdc2dd33a9da36ead9`文件1,117,320,736字节、sha256`6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`；llama.cpp Windows x64 CPU `b12242` ZIP24,931,401字节、sha256`4723cd1f1b10169b6ca681f787ea37238e449b1c56538b4b90c71a82fad949a0`。两件正文传输硬上限1,142,252,137字节；D盘新增≤4GiB、解压≤512MiB、D盘余量≥10GiB，静态核GGUF头/tokenizer、ZIP成员与安全、第三方notice、PE/DLL依赖，不允许额外权重/依赖、自动重试、更换资产、运行任何EXE、加载模型或推理。Release预发布且immutable=false，下载本地sha必核。

**当前授权登记时：`OWNER22_ASSET_DOWNLOAD_STATIC_ONLY_APPROVED_NOT_RUN / MODEL_RUNTIME_BLOCKED / RESOURCE_PEAK_UNPROVEN / MODEL_LOAD_INFERENCE_NOT_AUTHORIZED`。** 保留Owner20 NO_GO、R2 K1-C、旧S1失败、HumanGold0，正式ASR/Accuracy未测、S2–S5及5090 Claims继续锁。执行结束后STOP另报下一道smoke审批，不能自动继续。

[Owner22 PO-MHEP授权](owner_approvals/W1_5060_OWNER22_FIXED_QWEN_GGUF_ASSET_ACQUISITION_STATIC_INSPECTION_AUTH_20261110.md) · [5060生效执行Prompt](chinese5060/W1_5060_OWNER22_QWEN_GGUF_ASSET_STATIC_ACQUISITION_EXECUTION_PROMPT_V1.md)。

## 2026-11-10｜5060 Owner21 单模型只读审计完成

`READONLY_AUDIT_COMPLETE / HUMAN_DECISION_REQUIRED / AUTO_CONTINUE=NO`。Qwen 官方 Q4_K_M 与 llama.cpp b12242 Windows x64 CPU 发布身份和固定摘要均已核对。Qwen Apache-2.0、llama.cpp 源码 MIT，运行时整包第三方声明、PE 依赖和峰值仍未闭合。主机约 12.80 GiB 可用 RAM，规划峰值最高约 4.51 GiB，资源门仍阻断。

Task `W1-5060-OWNER21-QWEN-GGUF-ADMISSION-20261110-01`，私有元数据 ZIP SHA256 `7895f7ef2c28e6b7411112bf71140b17cd6b1160b614fc6662b4b132ebf4a816`。

模型与运行时正文下载、安装、加载、推理、模型 API、费用和新试次均为 0。下一门仅为两项固定资产的获取与静态验包，尚未获批。Owner20 NO_GO、旧 S1 FAIL、R2 K1-C 保留，Human Gold 0，正式 ASR/Accuracy 未测，S2–S5 锁定。

[单模型审批包](chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER21_QWEN_GGUF_SINGLE_MODEL_ADMISSION_PACKET.md) · [脱敏 Manifest](chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER21_QWEN_GGUF_READONLY_MANIFEST.json)

本条仅更新 5060，5090 保留历史快照。

## 2026-11-10｜Owner21 批准路线转向和 Qwen GGUF 只读准入审计（待执行）

`W1-OD-20261110-5060-QWEN-GGUF-READONLY-21`。Owner已接受终止Rule-only作为主抽取器，原Rule-V1/V2冻结保留为基线和确定性原文span/scope核验；沿用之前选择的“规则约束+本地模型抽取”方向。5060**只被允许**对官方Qwen2.5-1.5B-Instruct-GGUF Q4_K_M和`llama.cpp` Windows x64 CPU候选做只读模型/运行时revision、文件大小/SHA、许可、RAM/D/E磁盘/CPU/无C盘缓存与离线控制审计，提交精确单模型资产审批包后STOP。**授权登记时审计尚未运行**；任何下载/安装/加载/推理/API/新独立测试均未获许可，S2–S5/5090 Claims仍锁定。此前Owner20 `FEASIBILITY_NO_GO`、R2 K1-C、旧S1 FAIL保持真实，旧73与新100+20均已暴露，Human Gold0、正式ASR/回答准确率未测。

[Owner21正式授权](owner_approvals/W1_5060_OWNER21_QWEN_GGUF_READONLY_ADMISSION_AUTHORIZATION_20261110.md) · [5060执行Prompt](chinese5060/W1_5060_OWNER21_QWEN_GGUF_READONLY_ADMISSION_EXECUTION_PROMPT_V1.md)。

## 2026-11-10｜Owner20 NO_GO 监督审查与下一路线待决（不是新授权）

监督端核对实验HEAD `d69359081c49272c3cbf4f7f8f13427709c5ac62`、Run `W1-5060-S1B-RULE-ONESHOT-20261110-01` 及脱敏清单，证实Rule-V1/V2均单次120/120，预测先seal后Gold，主100上V1值0/70、错抽2/2，V2值5/70、错抽10/11，双臂均`FEASIBILITY_NO_GO`。无标题21个可答全拒识，且V2另有40个有标题主例在主体/属性识别阶段拒识；这是规则抽取脆弱的证据，不能解读为所有规则/神经方案无效。原旧73高分归类为暴露开发拟合，已曝光的100+20今后也不得作为未见测试重复使用。Human Gold0，正式ASR/Accuracy未测。

监督建议 `STOP_RULE_ONLY_AS_MAIN_EXTRACTOR`，转回Owner此前选择的规则+本地模型Route B；优先对**Qwen官方1.5B GGUF Q4_K_M**进行固定revision/官方SHA、Apache-2.0、Windows CPU runtime与D/E/RAM资源**只读审计**（官方GGUF单权重约1.12 GB，暂未许可下载）。UIE Nano 权重/分词器许可证仍未闭合。**目前只是监督建议，Owner尚未批准任何新模型、运行时安装、开发推理或新的盲评。** S2–S5、5090 Claims、D2/D3一律锁定。5090远端`dbd91f3667964baca69aeb82a6292c4fe193c965`核验无变化。

[完整研究裁决卡与PO-MHEP待决项](chinese5060/vesa_guard_reviewer_replan/W1_5060_OWNER20_NOGO_SUPERVISOR_ROUTE_CARD_20261110.md)。

## 2026-11-10｜5060 Owner20 单次规则可行性验证完成

`FEASIBILITY_NO_GO / S2_S5_LOCKED / AUTO_CONTINUE=NO`。两臂各 120/120，先封存后一次性评分，主 100 个语义案例另报 20 条改写。Rule-V1 值命中 0/70、已决定错抽 2/2，Rule-V2 值命中 5/70、已决定错抽 10/11，均未达冻结门。两臂在 30 个无标题主例均 UNKNOWN。Human Gold 0。

Run `W1-5060-S1B-RULE-ONESHOT-20261110-01`，执行代码 `c31e696f1a9432f6264f4fb8e4b26cab8e933ac5`，私有归档 SHA256 `f991e6e2fd3379c66412b061a2f9377b92f720783041c2253bd8374b59d65110`。

旧 S1 失败、R2 K1-C 及 Owner19 原封存保留。正式 ASR/Accuracy 未测，模型下载、推理、模型 API 和费用均为 0。当前批次已消耗一次科学试次，停止等待 Owner 决策。

[真实结果与失败归因](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_RULE_ONESHOT_FEASIBILITY_RESULT.md) · [脱敏 Run Manifest](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_RULE_ONESHOT_FEASIBILITY_RUN_MANIFEST.json)

本条仅更新 5060，5090 保留历史快照。

## 2026-11-10｜Owner20 放行有界S1-B一次性Rule-V1/V2离线可行性对照

Owner20 `W1-OD-20261110-5060-S1B-ONE-SHOT-20` 已针对上一轮唯一待决的“批准一次性规则可行性验证”明确要求继续、加快速度。**授权登记时尚未执行：`ONE_SHOT_FEASIBILITY_APPROVED_NOT_RUN`。** 5060被允许先以旧73/普通无标签unit测试进行公平公共适配器静态预检与冻结，然后对已封存100主案例(70 ANSWER/30 UNKNOWN)+20从属视图仅进行Rule-V1和Rule-V2各一次120/120离线预测，两臂role-free先seal，后单次揭盲汇总。保留每类/标题有无/多span/scope和改写分层、所有失败、95% Wilson与冻结门值命中≥63/70、wrong/decided≤2%。Agent生成的Gold不是Human Gold。封存数据SHA`531ac4e6421f6486b8165d443af2cf9d892a7bc3c740483950d03240d35a7c58`。禁新模型/API下载及推理、D2/D3、5090Claim、正式ASR、S2–S5、主线合并。任一预检/隔离/哈希失败STOP，结果无论正负全量保留并STOP。

[Owner20十二字段授权](owner_approvals/W1_5060_S1B_RULE_ONESHOT_FEASIBILITY_AUTHORIZATION_20261110.md) · [5060可执行的最终Prompt](chinese5060/W1_5060_S1B_RULE_ONESHOT_FEASIBILITY_EXECUTION_PROMPT_OWNER20_V1.md)。旧版“待批准草案”仍作为历史保留，不再作为当前执行入口。

**更新于 2026-11-11 JST · 版本 35 · 维护位置 `research/paper1-chinese-defense-5060`。**

## 2026-11-09｜5060 Owner19 可行性数据已封存，评价须另批

`FEAS_DATA_READY / PROVISIONAL_GOLD / EVALUATION_NOT_RUN / S2_S5_LOCKED / AUTO_CONTINUE=NO`。100 个全新虚构主案例（70 可答、30 应 UNKNOWN），另有 20 条从属问句改写。证据跨度、暂定标签、真值与配对、输入及协议已分件封存。标签是同一 Agent 的暂定标注，Human Gold 0。

Run `W1-5060-S1B-FEAS-DATA-PREP-20261109-01`，总封存 SHA256 `531ac4e6421f6486b8165d443af2cf9d892a7bc3c740483950d03240d35a7c58`。

Rule-V1/V2 新集零预测、零评分。D1 仅沿用历史开发诊断，CMRC2018 仅核元数据。模型下载／加载／推理和模型 API 调用为 0。下一门为 Owner 审批一次性规则可行性评价；正式 ASR/Accuracy 未测。

[结果与下一审批卡](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_FEASIBILITY_DATA_PREP_RESULT.md) · [脱敏 Manifest](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_FEASIBILITY_DATA_PREP_MANIFEST.json)

本条仅更新 5060，5090 保留上次已核快照。

## 2026-11-09｜Owner19 数据封存审查：一次性规则评价待新Owner明确批准

监督端核实 5060 数据提交 `20402e94ed3da6be155a605daba272ec0a7c2cf1` 与远端一致；报告100个主语义案例（70可答、30应拒识）、20从属问句、4域/10家族，角色盲输入/暂定Gold/source truth/配对/评分协议分件封存，seal SHA `531ac4e6421f6486b8165d443af2cf9d892a7bc3c740483950d03240d35a7c58`；实际 Rule-V1/V2 新样本预测/评分仍为0。来源同Agent合成，`NOT_INDEPENDENT_AUTHOR`，Human Gold0；D1/旧73/CMRC未纳入主分母。

公开源码显示30/100不带标题头，其中21/70可回答例不带标题头；Rule-V2使用`《...》`提取主体，缺可识别标题时易拒识，属于**预注册压力测试与性能风险**而非已知实测错误。另有多span支持集的共同Adapter输出与评分一致性问题，必须在**仅旧开发样本或普通unit fixture**中完成静态预检，严禁用新120例试预测/调参。

[监督Gate复核](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_FEASIBILITY_ONE_SHOT_SUPERVISOR_GATE_REVIEW_20261109.md)；[一次性执行Prompt草案（Owner未批不得运行）](chinese5060/W1_5060_S1B_RULE_ONESHOT_FEASIBILITY_PROMPT_DRAFT_OWNER_APPROVAL_REQUIRED.md)。
当前`DATA_PREP_COMPLETE / ONE_SHOT_OWNER_APPROVAL_REQUIRED / NO_NEW_MODEL_OR_API / S2_S5_LOCKED / AUTO_CONTINUE=NO`。该监督记录不是Owner20决定；5090仍无新Claim许可。

## 2026-11-09｜Owner19：规则先行可行性数据准备获批，测试仍须另批

`W1-OD-20261109-5060-S1B-FEAS-DATA-19`。Owner明确选路线A快速验证规则，暂不消耗人工标注成本：允许D1只读开发回归，公开CMRC2018在许可证/固定来源/大小/哈希门下作为补充，主批准备100个新生成的不同语义中文事实/拒识案例（建议70/30）+20从属改写视图。Source-truth在先，文本/问法/accepted span随后，私有输入/暂定Gold隔离封存；AI标签=`PROVISIONAL_NOT_HUMAN_GOLD`，若同一Codex生成，则`NOT_INDEPENDENT_AUTHOR`。D1/旧73绝不能算独立100，CMRC缺版本/scope标注不能冒用VESA人工Gold。

Owner19仅放行**数据准备与预注册封存**；新数据上的Rule-V1/Rule-V2一次性预测/揭盲/评分仍要另批Owner批准。新模型下载/推理、额外LLM API、D2/D3、正式HumanGold、S2–S5、5090 Claims仍禁止。授权时数据准备`APPROVED_NOT_RUN`，新规则性能`NOT_MEASURED`，旧S1 FAIL/R2 K1-C均不变。

[Owner19正式授权](owner_approvals/W1_5060_S1B_FEASIBILITY_DATA_PREP_AUTHORIZATION_20261109.md) · [可直接执行的Codex指令](chinese5060/W1_5060_S1B_FEASIBILITY_DATA_PREP_EXECUTION_PROMPT_V1.md)。

## 2026-11-09｜Owner18 Rule-V2 完成后的监督评审（只读评价，非新授权）

监督端已核验远端实验HEAD `33d67cfbdbc93b90bdcfa27241be6539f28c3f14` 及完整Run Manifest。旧73已暴露开发样本上的V2最终值命中59/61、已决定错抽1/59、应拒识误答0/12，保留同句等价值来源span错误1条、应答却UNKNOWN2条。三轮均留存，旧S1 FAIL不变。模型资产/推理/新独立验证仍未批准；UIE许可和环境锁阻断。对原S1脚本与新Rule-V2源码抽查确认受限字段模式与来源span选择，因此不能推断开放域中文泛化或RAG端到端污染防御成功。

建议Owner在 `A` Rule-V1/V2先行独立验证（需后续另立不复用的多模型公平holdout）与 `B` 等待UIE/Qwen准入后统一四臂盲评之间做决定；任一都需Owner另批独立Gold保管/审阅与一次性评价，不能据本条执行。S2–S5、5090 Claim继续未授权。[完整监督复核](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_RULEV2_SUPERVISOR_REVIEW_20261109.md)。

## 2026-11-09｜5060 Owner18 旧73开发完成，后续门关闭

`RULE_V2_DEV_COMPLETED / S1B_INDEPENDENT_TEST_NOT_RUN / MODEL_ASSET_NOT_AUTHORIZED / S2_S5_LOCKED / AUTO_CONTINUE=NO`。Owner18 批准的三轮旧73开发及 UIE 官方材料只读审计已完成。最终 58 正确、1 错误、14 UNKNOWN（73 条），值命中 59/61，决定后错抽 1/59，应拒识误答 0/12。旧 Rule-V1、S1 失败、R2 K1-C 保留。Human Gold 0，正式 ASR/Accuracy 未测。

最终 Run `W1-5060-S1B-RULEV2-DEV-20261109-03`，执行 SHA `da3cbd9f16ea70ae3ba0ef2aa2408227ecfc0b4f`，私有 Run Manifest SHA256 `c8e6258e73cd6076e1ea25b3cdd35c0c68167d5e44122c1725da260f359d09ee`。

UIE 权重/分词器条款、不可变身份、发布者 SHA256 和 Windows CPU 依赖锁待证。模型资产、推理和独立验证均须另批。新增模型下载、安装、加载、推理、API 与费用为 0。

[结果与失败](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_RULEV2_OLD73_DEV_UIE_READONLY_RESULT.md) · [证据清单](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_RULEV2_OLD73_DEV_MANIFEST.json)

此条仅更新 5060。5090 保留上次已核快照。

## 2026-11-08｜Owner18：仅 Rule-V2 旧73开发 + UIE官方材料只读核查

Owner `W1-OD-20261108-5060-S1B-RULEV2-DEV-18` 明确放行5060在原独立分支使用已暴露的73条S1合成案例与普通本地unit fixtures开发/调试Rule-V2，保留所有迭代、负结果、错抽与原版Rule-V1封存；可以只读核实官方UIE权重/分词器条款、不可变revision/发布者强身份和CPU依赖。不授权模型下载、依赖安装、模型加载/推理、任何新模型调用、S1-B独立验证数据的构造/打开/评价或S2–S5。旧S1 `S1_FAIL_STOP`，原R2 K1-C、HumanGold0、正式ASR/Accuracy未测全部不变。5090仍等待Meta Llama2许可，Claim1–3未运行。

**授权登记时状态：`RULE_V2_DEV_APPROVED_NOT_RUN / UIE_READONLY_APPROVED / MODEL_ASSET_AND_INFERENCE_NOT_AUTHORIZED / NEW_VALIDATION_NOT_AUTHORIZED / Auto Continue=NO`**。新Rule-V2数据与性能以未来真实Run Manifest为准，不得将此批准写成实验完成。

[Owner18十二字段授权](owner_approvals/W1_5060_S1B_RULEV2_DEV_AND_UIE_READONLY_AUTH_20261108.md) · [5060执行Prompt](chinese5060/W1_5060_S1B_RULEV2_OLD73_DEV_UIE_READONLY_EXECUTION_PROMPT_V1.md)。

## 2026-11-08｜5060 S1-B 只读审批包完成

`S1B_DESIGN_ONLY / MODEL_DOWNLOAD_NOT_AUTHORIZED / MODEL_INFERENCE_NOT_AUTHORIZED / VALIDATION_NOT_AUTHORIZED / S2_S5_LOCKED`。Owner B 只读审批包已完成，UIE Nano 权重条款和强身份待核，Qwen2.5-1.5B 已核固定 revision 与权重许可。独立验证保管人未指定。新增模型、推理、下载、安装、科学试次和费用均为 0。Auto Continue = NO。

[Owner 审批包](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_OWNER_ADMISSION_PACKET_20261108.md)。SHA256 `f3204df649a34f500cd7ad751f0e4952a595879eb79b2315e3b8b19fd4b5b9c7`。

## 2026-11-08｜S1-B 选择 B：文献复用 + 规则/本地模型对照（设计而非实验许可）

Owner `W1-OD-20261108-5060-S1B-B-DESIGN-17` 确定采用规则与本地开源模型辅助抽取的**研究设计**，特别要求借鉴RAGDefender及相关论文。已拟定`Rule-V1`（旧锁定）/`Rule-V2`（开发）/PaddleNLP UIE轻量中文候选/Qwen2.5-1.5B-Instruct候选；S1-B仍须分别经过模型资产、离线开发推理、独立验证三个新的Owner许可门。资源/许可/具体revision目前待核，不能默认批准。**新增模型下载=0，新增模型调用=0，S1-B科学试次=NOT_RUN**。旧S1 `S1_FAIL_STOP`，S2–S5仍锁。5090仍在Meta Llama2访问审批等待中，Claim1–3未运行。

[PO-MHEP设计提案](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1B_LITERATURE_MODEL_RESOURCE_INDEPENDENT_VALIDATION_PROPOSAL_20261108.md) · [仅设计核验执行Prompt](chinese5060/W1_5060_S1B_LITERATURE_MODEL_ADMISSION_DESIGN_ONLY_PROMPT_V1.md)。

## W1-5060-S1-CHINESE-EXTRACTION-20261108-01 — S1 封存失败与停止

Owner16 S1 单次封存验证结束，S1_FAIL_STOP。73 条合成样本，30 正确、4 错误、39 UNKNOWN；答案值 31/61、已决定错抽 4/34。自然中文可用 scope-bound 事实 25/49。模型、API、下载与费用为 0。Human Gold 0，正式 ASR/Accuracy 未测。S2–S5 未授权，Auto Continue = NO。

[S1 结果与证据](chinese5060/vesa_guard_reviewer_replan/W1_5060_S1_INDEPENDENT_CHINESE_EXTRACTION_RESULT.md)。


当前研究状态为 **5060 S1 未通过并停止，S2–S5 未授权**。5090 已完成离线 Smoke 和非 Llama 资产下载，Claim 1–3 均未运行。Paper 1 正式实验仍未启动。

旧名 `PAPER1_WEEK1_TRACKER_INIT` 可在旧对话中定位到一次提及。2026-11-06 检查 GitHub 的 9 条公开分支、1 个标签及其可达文件历史，未找到对应文件，原稿的仓库路径、最后修改时间及全文均为 **UNKNOWN**。本页是从已提交证据建立的第一个可维护版本。

## 2026-11-08 5060 R2 实测收口

本批仅为 D1 开发诊断。高置信模板 6/180、3/36 世界，蒙版对两个分词臂均为零变化。char2 使 Clean 误删 4/10→5/10、HN 隔离 2/9→4/9、Poison 删除 2/10→4/10。可比被删候选 0。S1–S5 未放行。

[四臂结果与封存证据](chinese5060/vesa_guard_reviewer_replan/W1_5060_R2_FAIR_CONTROL_RESULT.md)。

## 2026-11-08 历史授权：5060 S1 获批、5090 Llama2 等待

Owner `W1-OD-20261108-5060-S1-OFFLINE-16` 已授予5060唯一有界新任务：S1 ≥60例独立中文可见证据事实抽取离线验证（D1/D2/D3/旧108隔离），原错抽率、自然化/span/scope/Wilson门不变，0新下载/0联网/0商业API。**S1 APPROVED_NOT_RUN**，未有S1结果、Run Manifest或通过结论。S2–S5仍锁，R1-10(B)独立S3构造方未定。

5090远端 `dbd91f3667964baca69aeb82a6292c4fe193c965` 未变。Meta Llama2访问 `APPLICATION_SUBMITTED / APPROVAL_UNVERIFIED`，模型 `NOT_DOWNLOADED`、Claim1–3 `NOT_RUN`。不能据申请状态推定已获许可或暗示模型下载。

[Owner16授权](owner_approvals/W1_5060_S1_INDEPENDENT_CHINESE_EXTRACTION_OFFLINE_AUTHORIZATION_20261108.md) · [完整Codex Prompt](chinese5060/W1_5060_S1_INDEPENDENT_CHINESE_EXTRACTION_EXECUTION_PROMPT_V1.md)。

## 2026-11-08 R2 完成后的监督核验与下一审批门

5060 最新已封存 R2 Run `W1-5060-R2-FAIRCTRL-20261108-02`、结果提交 `5968369eaa1b3f8d1af2d9262ef5f3f145c4a83c`。36 世界四臂完成并复算，历史 B2 deleted 81/180、Poison 2/10、Clean 4/10、HN 2/9；char2 deleted 112/180、Poison 4/10、Clean 5/10、HN 4/9；网页模板高置信 6/180、mask 删除差异 0/36。既有抽取器可比较的被删候选 0，可信来源锚 0/180。预注册 `K1-C / INSUFFICIENT_OR_MIXED` 接受为该开发任务的路线分支，S1–S4 仍 NOT_RUN，S5 NOT_AUTHORIZED。5090 Claim1–3 未运行。

控制面 2026-11-08 建议：停止在旧 D1 上后验微调 tokenizer、mask、阈值和 VESA 规则，保留 D1_DEV_EXPOSED；若 Owner 新批准，**先 S1 ≥60 个独立自然中文抽取/作用域测试**核准可信抽取门，再按既有 R1/R2 预注册 S2 A–I、H4+1/H5+0 和可信锚有/无层推进。S3 独立方、S4、S5 均需新 Owner 授权。

[正式监督建议](chinese5060/vesa_guard_reviewer_replan/W1_5060_K1C_SUPERVISOR_ROUTE_RECOMMENDATION_20261108.md)，状态 `SUPERVISOR_RECOMMENDATION / PENDING_OWNER_CONFIRMATION`，**不是新执行批准**；不得据此打开 S1/S2/S3/S4/S5。

## 2026-11-08 控制面恢复与 R2 放行

GitHub 远端实查确认：交接包记录的 5060 HEAD `533a6efed519f9251f4b4848306e232c9710a497` 与检查时远端完全一致；5090 HEAD `dbd91f3667964baca69aeb82a6292c4fe193c965` 亦完全一致，说明新会话恢复前没有遗漏的远端实验提交。随后控制面仅写入治理授权，不伪造实验结果。Owner 本轮 `W1-OD-20261108-5060-R2-OFFLINE-15` 已释放有界 R2 离线任务：`S0-TEMPLATE-COVERAGE_READONLY` + `B2_RAW / RD_ZH_ONLY / RD_TEMPLATE_ONLY / RD_ZH_TEMPLATE` 四臂，并批准 R1-10(A) 仅使用历史 B2 固定 revision 的本地已缓存 encoder。网页模板 mask 只可作用于 Stage1 lexical view；原 TopK、原文、embedding/Stage2、生成上下文、参数和历史结果保持不变。role-free 结果须先封存，再独立揭盲。

在本页第 2 版记录的控制面放行时，**尚无新的模板覆盖计数、四臂结果或 K1 判定**，所以这些仍为 `NOT_RUN / NOT_MEASURED`。R1-10(B)、S1–S5、5090 Claim1–3、D2/D3、正式测试、商业/免费在线模型调用及主线合并均未放行。完成本批后必须按已预注册 K1-A/B/C 选择路线并 STOP 返回 Owner。

[2026-11-08 PO-MHEP 授权](owner_approvals/W1_5060_R2_OFFLINE_FAIR_CONTROL_AUTHORIZATION_20261108.md)。

## 双机 Git 快照

| 工作线 | 分支与本次整理前的远端 HEAD | 该提交时间（JST） | 机器端观测 |
| --- | --- | --- | --- |
| 5060 Codex · 中文检索后防御 | `research/paper1-chinese-defense-5060` · 2026-11-08 恢复前远端核验 `533a6efed519f9251f4b4848306e232c9710a497`；随后仅新增治理授权提交 | 2026-11-08 | R2 有界离线任务已放行；机器本地 HEAD、未提交改动和实时进程仍 UNKNOWN，实验结果须以之后 Run Manifest 为准。 |
| 5090 Cursor · RAGDefender 复现 | `research/paper1-ragdefender-repro-5090` · [dbd91f3667964baca69aeb82a6292c4fe193c965](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/commit/dbd91f3667964baca69aeb82a6292c4fe193c965) | 2026-11-06 02:58:38 | Git 下载清单可查，机器本地 HEAD、工作树及实时进程为 UNKNOWN。 |

分支 HEAD、控制合同和实验执行 SHA 分开记录。5060 S0 证据收口提交为 [25936c71f96d775cca9a7603d27164e952f3a0af](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/commit/25936c71f96d775cca9a7603d27164e952f3a0af)，R1 追加只读核验的控制提交为 [9bd8e29](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/commit/9bd8e29d49b774add5eafb700077e1750d41f309)。RAGDefender 固定上游为 [ba2a17e](https://github.com/SecAI-Lab/RAGDefender/commit/ba2a17efba165d45409114df2d70b030ade1e1b8)。

## 5060 已封存结果

| 项目 | 状态与结果 | 证据 |
| --- | --- | --- |
| D1 Pilot12 检索 | **VERIFIED** · 12 个相关事实组、36 个独立建索引的世界，每世界 1 个候选和 18 个背景文档，TopK5 共 180 片段。候选 hit@5 为 29/36，Poison 10/12、Clean 10/12、HN 9/12。7 次漏召回另计。 | [S0 报告](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_SUMMARY.md) |
| B1/B2 离线过滤 | **VERIFIED** · 各 36/36 世界。B1/B2 总删片段 78/180、81/180。以已召回候选为分母，Poison 删除 1/10、2/10，Clean 误删 1/10、4/10，HN 隔离均为 2/9。B2 仍保留 8/10 个已召回 Poison 候选。 | [S0 脱敏证据索引](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_EVIDENCE_INDEX.json) |
| G0/G1/G2 真实 Qwen | **VERIFIED** · `OWNER12_LIVE_108` 108 次请求成功，0 重试。三臂回答分别 15/36、13/36、11/36，拒答分别 21/36、23/36、25/36。输入/输出 Token 合计 44,426/5,154。CNY 0.130084 为公开费率估算，实扣为 UNKNOWN。 | [Owner12 运行结果](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/c6e36685cd948700f2d65e53031f82d8d13d2f51/docs/paper1/dual_machine/chinese5060/pilot_rapid_live/RAPID_LIVE_OWNER12_EXECUTION_RESULT.md) |
| 回答与拒答暂定评价 | **VERIFIED / PROVISIONAL** · 18 格拒答暂定合理，另 51 格拒答和 39 份回答的整体判断未决。Human Gold = 0，正式 Targeted ASR、Answer Accuracy 与 C3 均未测。 | [暂定评价](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/59ceb4ff2267299aa7ed1c6fb0819f952098fcd5/docs/paper1/dual_machine/chinese5060/pilot_rapid_live/PILOT12_D1_AI_PROVISIONAL_EFFECT_REPORT.md) |
| VESA v0.1 / v0.2 | **VERIFIED · 零变化** · 两版均 0/36 上下文改变，G3 与 G2 请求体逐字节一致，0 恢复、0 新 Qwen、G3 未运行。v0.2 识别到 24/36 个查询世界、102/180 个片段，49/180 个片段抽到具体值。 | [v0.1 结果](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/bfcfaa6490de96b97b12b3304297049dfa627910/docs/paper1/dual_machine/chinese5060/vesa_guard_v01/VESA_V01_OWNER13_RESULT.md) · [v0.2 结果](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/8db8d9f8b48f86dae9f8f9211e1092fbe4ae534d/docs/paper1/dual_machine/chinese5060/vesa_guard_v02/VESA_V02_OWNER14_RESULT.md) |

D1 是 `D1_DEV_EXPOSED`。本页 Pilot12 的 12 组、36 世界与 D1 开发范围的 40 组、120 候选分别计数。D2/D3、独立留出、答案与攻击目标留在各自授权和隔离边界内。上下文变化、候选过滤和回答/拒答计数分别记录。

## 5060 评审、S0 与放行门

S0 run 为 `W1-5060-REVIEWER-REPLAN-S0-20261106-01`，状态 **S0_COMPLETE / OWNER_CHECKPOINT_PENDING**。零新编码、零新检索、零模型调用、零 API 费用。[S0 报告](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_SUMMARY.md) · [S0 脱敏证据索引](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_EVIDENCE_INDEX.json)。

| 评审 | 本次核验状态 |
| --- | --- |
| R1-01 | **VERIFIED，静态完成**。RD-zh 只将 Stage 1 TF-IDF 改为字符二元组，`stop_words=None`。4 项定向单测通过，真实 D1 编码和过滤均 **NOT_RUN**。历史 B2 的 TF-IDF 仍沿用英文词规则和停用词。 |
| R1-02 | **VERIFIED**。旧 `n_tfidf` 36/36 一致，12/36 世界进入大簇分支。两次本地 top5 重放相同，旧记录未存逐词清单。分词造成误删的因果效应尚待反事实对照。 |
| R1-03 | **VERIFIED**。旧抽取器在 B2 被删的 81 片段中抽出 25 个具体值，0/81 与查询范围绑定，81/81 同值/异值判断为 UNKNOWN。保留集合中 1/36 世界有同范围唯一值，独立可信来源锚 0/180。以上按冻结输入及现有抽取器口径统计。 |
| R1-04 | **DESIGN / NOT_RUN**。M1-safe 为探索臂，保留重复同值片段可能提高错值采纳的残余风险。 |
| R1-05 | **DESIGN / NOT_RUN**。M2-detect 与 M2-vote 分臂，后者需要可验证的攻击者控制上界，多数与全毒场景单列。 |
| R1-06 | **DESIGN / NOT_RUN**。S1 独立记录错抽的两个分母、UNKNOWN、错因和区间。 |
| R1-07 | **DESIGN / NOT_RUN**。S2/S3 加入合法共享法规引用场景 I，保留 H 的 4 毒 1 净、5 毒两个变体。 |
| R1-08 | **VERIFIED**。72/72 个世界×B1/B2 臂的历史 Stage 2 计数和索引对齐修复后逻辑，实际余弦先做 L2 归一化，当前无 Stage 2 归一化修正臂。 |
| R1-09 | **HARD_STOP**。S0 已封存，S1–S4 **NOT_RUN**，S5 **NOT_AUTHORIZED**，Auto Continue = NO。 |
| R1-10 | **OWNER_DECISION_REQUIRED**。A 为 36 世界、180 片段的缓存编码器及 RD-zh 离线实跑权限，B 为 S3 独立造题与保管方。 |

R1 源附件由 Owner 提供，公开记录含原件摘要与 SHA-256。[R1 修订合同](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/fbb176f6aa232212a44d336ecb037c39b1220cd4/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_R1_TRACKING_AMENDMENT_20261106.md)。

**S4 证据门（INFERRED）**。冻结输入可信锚 0/180。按严格 P0 和原 B2，Clean 误删下界为 4/10，原门要求 <4/10，故当前输入标记 `S4_FAIL_EVIDENCE_BOUNDARY`，S4 本身仍是 **NOT_RUN**。公平臂出结果后按各臂重新计算。Poison 保留 ≤8/10 是原 D1 开发不退化门。[S0 报告](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/25936c71f96d775cca9a7603d27164e952f3a0af/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_S0_S4_SUMMARY.md)。

**R2（历史预注册，实测见页首）**。评审观察的约 100/189 来自上游证据，D1 TopK180 的网页模板覆盖率为 **UNKNOWN**。下一项诊断限于冻结 TopK 的只读覆盖统计。已预注册 `B2_RAW`、`RD_ZH_ONLY`、`RD_TEMPLATE_ONLY`、`RD_ZH_TEMPLATE` 四臂，控制 Stage 1 分词与词面模板遮蔽，固定原 TopK、向量、Stage 2 和生成正文。四臂对照未实跑。K1 路线选择待证据，M2 与 X-MADAM-RAG 的重叠已登记。[R2 预注册与路线决策](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/1499561c8091fec1aaa042b81b9168ee63ff908d/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_R2_S0_CHECKPOINT_TEMPLATE_TFIDF_ROUTE_20261106.md)。

## 5090 原论文复现

| 项目 | 级别与状态 | 证据 |
| --- | --- | --- |
| 上游审计、环境、离线检查 | **VERIFIED · SMOKE / ALGORITHM_CHECK**。官方环境在 RTX 5090 的 CUDA 内核存在兼容问题，独立兼容环境的最小 CUDA 检查通过。 | [离线 Smoke 与资源门](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/5def0ff/docs/paper1/dual_machine/repro5090/W1_5090_OFFLINE_SMOKE_AND_RESOURCE_GATE.md) |
| 冻结非 Llama 资产 | **VERIFIED（仓库下载收据）**。Vicuna、Contriever、paraphrase-MiniLM 与 NQ、HotpotQA、MS MARCO 已下载。Llama 2 7B chat 未下载，本批模型加载 0、付费 API 0。 | [5090 下载记录](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/dbd91f3667964baca69aeb82a6292c4fe193c965/docs/paper1/dual_machine/repro5090/official_asset_gate/W1_5090_NON_LLAMA_ASSET_DOWNLOAD.md) · [下载清单](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/dbd91f3667964baca69aeb82a6292c4fe193c965/docs/paper1/dual_machine/repro5090/official_asset_gate/NON_LLAMA_DOWNLOAD_MANIFEST.json) |
| Claim 1 PoisonedRAG、Claim 2 Tan et al.、Claim 3 GARAG | 三条均 **NOT_RUN**。无防御/有防御 Targeted ASR 与 QA Accuracy 均 **NOT_MEASURED**。 | [下载清单](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/dbd91f3667964baca69aeb82a6292c4fe193c965/docs/paper1/dual_machine/repro5090/official_asset_gate/NON_LLAMA_DOWNLOAD_MANIFEST.json) |

## Owner 待决

| 决策 | 当前状态与前置 |
| --- | --- |
| 5060 · `S0_CHECKPOINT_RELEASE` | **待放行**。先确认追加只读的 D1 TopK 模板覆盖与四臂计划。进入 S1 需 Owner 显式放行。 |
| 5060 · R1-10(A) | **待授权**。是否准许仅用冻结缓存编码器对原 36 世界、180 片段做离线公平对照。限制为零下载、零新检索、零商业 API，历史 B2 证据原样保存。 |
| 5060 · R1-10(B) | **待指定**。选择独立于 5060 方法开发方的 S3 构造与保管人。任何跨机委派须单独授权。 |
| D1 定位与人工裁决 | **待证据/安排**。公平臂、可作用池和可信来源证据进入 K1 决策。独立人工审阅尚待安排，Human Gold 仍为 0。 |
| 5090 · 后续批次 | **待授权**。Llama 2 获取状态和下载、单格、Claim 正式运行分别核验与批准。 |
| S5 与投稿目标 | S5 保持 **NOT_AUTHORIZED**，须前序门闭合后再单独确认模型、外传及预算。投稿场次与年份待 Owner 确定。 |

5060 放行与角色隔离依据 [Owner 决策登记](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/fa70d97f86d0bf21364907e15447ced80f0e284e/docs/governance/project_owner_decision_register.md)、[5060 动态状态](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/fa70d97f86d0bf21364907e15447ced80f0e284e/docs/governance/current_work_state.md)、[R2 检查点](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/1499561c8091fec1aaa042b81b9168ee63ff908d/docs/paper1/dual_machine/chinese5060/vesa_guard_reviewer_replan/REVIEWER_R2_S0_CHECKPOINT_TEMPLATE_TFIDF_ROUTE_20261106.md)。5090 批次依据 [5090 分批审批包](https://github.com/tingfengy2000-creator/llm-security-evaluation-framework/blob/dbd91f3667964baca69aeb82a6292c4fe193c965/docs/paper1/dual_machine/repro5090/official_asset_gate/BATCHED_REPRO_OWNER_APPROVAL_PACK.md) 和最新下载清单。

## 更新规范

1. **事件触发维护。** 每次两机推送新证据、Run 完成/失败/零变化、评审修订或 Owner 改门后，负责更新的控制端先核验双方远端 HEAD，再在本文件更新受影响条目并追加下面的变更记录。无新证据时保留上一已核状态与时间，机器本地状态记 UNKNOWN。
2. **每条带证据。** 记录 JST 时间、分支、远端 HEAD、合同/执行 SHA、Run ID、阶段和分母。证据链接固定到提交。优先核对 Run Manifest、脱敏证据索引及封存汇总，再核对 Owner 决策和动态状态。`VERIFIED` 表示仓库或可访问证据已核，注明证据层级。`REPORTED` 为仅机器或评审回传，`INFERRED` 为由证据推导，`UNKNOWN` 为缺证，`BLOCKED` 为有明确门或缺项。计划、未运行和未测分别标记。
3. **保留历史和权限。** 失败、零变化、分母和旧快照由证据提交与变更记录保留。纠正用追加记录引用原提交，区分开发、Smoke、正式实验和人审。Owner 的新授权引用登记或合同。公开 Git 仅收脱敏汇总与哈希，原 TopK、逐样本标签、目标答案、私有评审附件及凭据保留在受控位置。
4. **独立维护。** 维护提交基于最新远端，从独立副本快进发布到 5060 研究分支。发现远端前移时先复核新证据。运行中的工作树由机器执行者在其收口节点自行协调同步，远端更新与工作会话已接收分别记录。
5. **状态权威。** 本页是双机索引。5060 动态状态以 [Current Work State](../../governance/current_work_state.md) 为准，证据索引以 [Experiment Master Record](../../governance/experiment_master_record.md) 为准，授权以 [Owner Decision Register](../../governance/project_owner_decision_register.md) 为准，冲突按 [Context Authority Map](../../governance/context_authority_map.md) 处理。

## 变更记录

| 日期（JST） | 版本 | 变更与核验基点 |
| --- | --- | --- |
| 2026-11-11 | 35 | Owner28 两批对照、方法限制与 Owner29 草案完成，仅报告准备。 |
| 2026-11-11 | 34 | Owner28 一次性 32 主世界盲预测封存，等待 5090 独立评分。 |
| 2026-11-11 | 33 | Owner28 5060 冻结身份通过，5090 兼容文件 0/3，独立评价 0/32。 |
| 2026-11-11 | 32 | Owner28 5060 只读失效图谱、收据审计和四臂工具通过，EVAL 0/32 等独立交接。 |
| 2026-11-11 | 31 | Owner27 32 主世界七臂完成，联合主门失败，EVAL 独立输入阻断。 |
| 2026-11-11 | 30 | 5060 核公开中文版本来源和研究邻近工作，形成独立查询预注册草案，科学试验未批准。 |
| 2026-11-10 | 29 | Owner26 两条 RD DEV 复跑，七臂未达到数据与预算准入。 |
| 2026-11-10 | 27 | Owner25 合成机制 64 DEV 与 32 HOLDOUT 完成。原 D1 与 Rule‑V2 路线 NO_GO，公平 RD 基线缺失。 |
| 2026-11-10 | 25 | Owner24 F0 固定资产与 completion 静态依赖通过，网络隔离未验证，F1–F4 未运行。 |
| 2026-11-10 | 23 | 5060 完成 Owner23A 静态审计，CLI 和 API-set 通过，Owner23B 实际加载待批。 |
| 2026-11-10 | 20 | 5060 两件固定资产字节核验、GGUF 与 ZIP 安全检查通过；许可及 PE 依赖未闭合，运行仍锁定。 |
| 2026-11-10 | 18 | 5060 完成 Owner21 单模型只读审计，资产身份闭合，运行时与资源准入待证。 |
| 2026-11-10 | 15 | 5060 Owner20 单次评价已完成，两臂均未达可行性门，锁定后续阶段。 |
| 2026-11-09 | 12 | 5060 封存 100 个可行性主案例和 20 条改写，Owner19 仅数据准备收口，预测与评分均未运行。 |
| 2026-11-09 | 11 | Owner19认可先可行性后人工标注，以新合成/公开数据准备为主、D1仅回归；未放行新数据一次性评分、模型/API和S2–S5。 |
| 2026-11-09 | 10 | 监督端只读审核Owner18开发完成结果，保留span与领域外风险，提出A先规则盲评/B等待多模型四臂的待Owner决策；不扩大科研许可。 |
| 2026-11-09 | 9 | 5060 完成 Owner18 的旧73开发与 UIE 只读核验，三轮封存，模型及独立验证仍关闭。 |
| 2026-11-08 | 8 | Owner18单独允许 Rule-V2 使用旧73开发及UIE只读许可/依赖核查；新模型资产/推理和独立测试仍未授权，S2–S5保持停止。 |
| 2026-11-08 | 4 | Owner16批准5060单独S1离线验证，状态APPROVED_NOT_RUN，5090 Llama2访问仍待审批；S2–S5继续关闭。 |
| 2026-11-08 | 2 | 新会话按交接包恢复并动态核对双机远端；5060/5090 均与交接 SHA 一致。登记 Owner R2 有界离线授权，释放模板覆盖诊断与四臂公平对照；无新实验结果。 |
| 2026-11-06 | 1 | 建立双机维护页。记录 5060 的旧 G3 零变化、S0 完成、R1/R2 与待放行状态，以及 5090 非 Llama 资产下载后 Claim 未运行。整理前 5060 `fa70d97`，5090 `dbd91f3`。 |
| 2026-11-08 | 3 | 5060 实测四臂、封存、K1-C，保持 5090 历史快照。 |
| 2026-11-08 | 5 | 5060 S1 单次合成开发验证失败，S2–S5 仍未授权。 |
| 2026-11-08 | 6 | Owner选B作为S1-B设计方向，新增文献对照、候选资源与独立验证审批提案；不准新模型下载、推理或科学试次。 |
| 2026-11-08 | 7 | 5060 S1-B 只读资源与独立验证审批包收口，执行门仍关闭。 |


## 2026-11-11｜Owner29 生成可行性首格停发

`OWNER29_RAPID_LIVE_STOPPED / 1_SENT / 0_VERIFIED / 95_NOT_RUN / AUTO_CONTINUE_NO`。Owner 确认余额、角色盲外传及本批新增 USD 5。首格已发送，Runner 回包字段读取异常，实际扣费和回答均未知；首格保留预留。离线修正全路径通过，正式指标仍未测。 [OWNER29 快速生成首格停发报告](chinese5060/OWNER29_RAPID_GENERATION_STOP_REPORT.md)


## 2026-11-11｜Owner29 剩余 95 格真实生成完成

`95_REMAINDER_VERIFIED / 95_SUCCESS_OF_96 / 31_COMPLETE_TRIPLES / DESCRIPTIVE_ONLY / STOP`。Owner 批准仅续跑 95 格，沿用 USD 5 与角色盲外传范围，旧首格未重发。续跑 95 格均成功，总计发送 96 格、失败 1 格、未运行 0 格。仅描述回答与拒答，Human Gold 为 0，正式 ASR 和 Accuracy 未测。[真实续跑结果与证据](chinese5060/OWNER29_RAPID_GENERATION_REMAINDER_RESULT.md)


## 2026-11-11｜Owner30 G0 封存回包核验完成

`G0_VERIFIED / G1_AWAITING_REFERENCE / RULE_SCORED_0 / JUDGE_SENT_0 / HUMAN_GOLD_0`。已在读取真实回答前冻结规则，核验 95 份回包、31 个完整三臂世界和首格缺失。5090 两份公开参考文件尚未到达。新增生成、评分调用及费用均为 0。 [5060 G0 核验与证据](chinese5060/owner30_eval/OWNER30_ANSWER_EXPORT_REPORT.md)


## 2026-11-11｜Owner30 确定性评价与安全交接

`95_RULE_PROCESSED / 27_ABSTAIN / 68_UNRESOLVED / JUDGE_BLOCKED / HUMAN_GOLD_0 / STOP`。5090 32 个公开参考已准入。31 个完整三臂配对的正确性及来源支持无可判读差，Judge 0 次，费用 USD 0.00。仅发布通过安全审计的逐格结构字段和 62 个公开短值，5090 独立目标匹配待执行。 [5060 暂定评价及清单](chinese5060/owner30_eval/OWNER30_AUTO_ANSWER_GRADE_REPORT.md)


## 2026-11-11｜Owner30 短包准入与数值代理诊断

`68_PACKETS_FROZEN / 62_NUMERIC_MATCH / 6_NUMERIC_MISMATCH / 27_ABSTAIN / JUDGE_NOT_ADMITTED / STOP`。31 个配对世界三臂数值匹配 20、25、15；保留全部原未决，Human Gold 为 0。Token、账本和外传准入缺失，Judge 0 次、新增 USD 0.00。 [补充报告](chinese5060/owner30_eval/OWNER30_QWEN_JUDGE_SUPPLEMENT_REPORT.md)


## 2026-11-11｜5060 Owner30 最终科研证据归档

`SCIENTIFIC_TRIALS_STOPPED / OWNER_ROUTE_DECISION_PENDING / AUTO_CONTINUE=NO`。Owner27–30 完整链已归档，联合门控暂停。31 配对世界三臂数值匹配 20、25、15；5090 暂定短值目标命中为 0/22、0/22、5/22。2 个纯范围世界仍未知，68 条回答的范围和引用支持未决。Human Gold 为 0，正式 Accuracy/ASR 未测，原作者 Claim1–3 未运行。建议基准与失效分析优先，路线及后续资源待 Owner 决定。本次仅文档，无新科研试次。 [最终决策简报](chinese5060/PAPER1_FEASIBILITY_FINAL_DECISION_BRIEF.md)
