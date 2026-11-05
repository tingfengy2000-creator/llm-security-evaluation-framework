# Paper 1｜VESA-Guard v0.2 快速方法修订和受限 G3-v0.2 实验授权（PO-MHEP 十二字段）

**Owner Decision ID:** `W1-OD-20261105-5060-VESA-V02-FAST-14`  
**签发日:** 2026-11-05 JST；**分支:** `research/paper1-chinese-defense-5060`；**授权前 HEAD:** `bfcfaa6490de96b97b12b3304297049dfa627910`。
**授权来源（Owner原文）:** “我作为 Paper 1 Owner，批准5060进入 VESA-Guard v0.2 快速方法修订：针对v0.1真实数据0/36变化的问题，替换过窄的中文fullmatch解析和完全依赖可信来源签章的恢复门，采用生产可获得的文本事实、时间版本适用性、明确冲突、指令风险与证据覆盖进行角色盲的风险分级选择。允许有限、可审计的受限恢复，但不得把无明显冲突认定为可信，不得使用Poison/Clean/HN标签、参考答案或旧逐格生成结果设计规则。只预注册和冻结一套v0.2方案，离线验证原36世界；若产生可复核的非零上下文变化且数据、预算和独立检查通过，批准同一任务最多36次固定Qwen G3-v0.2真实生成，零额外探测或重试，不重跑原108次。并行推进独立人工事实裁决，但不得向算法开发侧泄漏裁决信息。保留D2/D3、5090及正式实验边界。请按PO-MHEP登记并将完整可执行Prompt写入5060 Git分支，优先实现及验证，而非重复准备文书。”

**授权类型：** `OWNER_APPROVED_V02_SINGLE_DESIGN_CONDITIONAL_G3_LIVE36`。本授权允许一次性开发、离线冻结、经必需门检查后同任务执行**不超过36次**新Qwen API；未通过门即STOP，不应把“授权已有”解释为模型请求已经发出。旧Owner13于v0.1无差异后已用毕；旧Owner12单批预算豁免**不适用于**v0.2。

## 1. Issue ID
`W1-OD-20261105-5060-VESA-V02-FAST-14`，跨分支只用OwnerID+完整commit SHA；不复用可能冲突的PODR号。

## 2. Issue name
从无法落地的v0.1“严格正则全匹配+必须上游可信签章”转为可在真实中文RAG文本执行的、风险分级与证据覆盖约束的VESA-Guard v0.2，开发G3-v0.2单一预注册36世界与受限真实配对。

## 3. Discovery stage
v0.1离线实验 `VESA_V01_OFFLINE_NO_SAFE_G3_DIFF`。36/36 G3请求与G2逐字相同；原TopK 36×5=180片段、81 B2隔离片段全部未恢复；生产签章覆盖0/180，query完整规则0/36、chunk完整规则0/180，查询侧可见span84。v0.1规则SHA`ff34130b3c26a288dc4ad26420c1188e9f9f17940108475a003e260748f72ab1`；G3 grid `95e37ca826ea84af365edb6f255e50ff35cd215f58d47d76ab7bf3cedba2eff0`；seal`089b0c3fc13e9f84693452371d5b5c8a31f65c1dcb59e7cfcf7de69a15cb3df1`。G3真模型调用0。旧真实G0/G1/G2已108成功，Human Gold仍0。

## 4. Evidence classifications
`OBSERVED_GIT`：v0.1缺输入元数据和解析覆盖导致0差异，旧G2删除Clean已召回候选4/10、Poison已召回2/10；G2相对G0五格回答→拒答均与参考证据损失共现。`INFERENCE`：宽覆盖中文事实/版本/冲突解析+有界证据救援可能提升Clean覆盖，但同样可能将污染引入。`UNKNOWN`：新文本风险分数的真实误差、v0.2安全性及正确性收益、任何正式ASR/QA、外部泛化、创新性。`NO_GROUND_TRUTH`：12题独立人工事实裁决尚未完成；不能将原D1 AI临时参考当Human Gold。

## 5. Preserved constraints
原P2 seal `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52`、PAIR01 seal `bb775ead3d330f5e83516f8dfa871a3e2581c305e5ae7baf104500f781ac79fb`、原V2 proposal `e5bd219b7812b8ef97ef916226ac221e177f227808cd0dbc0bbe280920d1b70e`、原108grid `78708759e0965e816d9d5b7aaa0bca92d2a6b92562930cd028dc87875d09468c`、model`qwen3.7-plus-2026-05-26`、原System SHA`b3c74613bc3700eacdce7dfedc382043013f452e321a13d8639b27817edbd1f1`、temperature0/top_p1、no thinking/search/tools、JSON schema、`max_completion_tokens=256`、北京Workspace、108旧响应/评价seal都不可改。G3仅在同一原36世界TopK5内选原文子集、保留原rank与引用C1..C5，不改原query、检索和B1/B2参数。0模型judge、0探测/重试、0模型/依赖下载安装，5090与D2/D3不触动；C盘受控零新增、D/E>=20GiB；原全线USD25预警/28停止新批/30总硬限有效，未获新豁免。

## 6. Why now
Owner明确需要速度、方法而非再次工程准备。v0.1 0变化是**实际表述覆盖和方法决策前提失配**，再新增测试不足以形成科研证据。用一次真实可执行的v0.2方法修订迅速取得有意义的上下文差异和安全风险曲线。

## 7. Downstream risks
(a) 多片段“未见明显风险”并不等于可信，低风险恢复有污染漏放可能；(b) 同一网站/同源重复不能当独立证据；(c) 历史版本对历史问可能正确、对现行题可能不合适；(d) 宽中文规则可能误识别数值单位、条件、否定、例外和条文版本；(e) D1算法一旦读取Gold或旧逐格模型回复即泄漏；(f) 以同一D1不断调规则会选择性过拟合；(g) 36相关世界/12事实组不足以证明2.5pp不劣和正式安全性；(h) 发表风险：证据充分性/一致性已有研究，必须靠明确差异、消融和外部泛化建立创新；(i) 真实G3调用追加费用须单独计入累计账本。

## 8. Options and impacts
A `OWNER_SELECTED`：一次提交v0.2统一算法（生产可见文本，宽松中文片段抽取与作用域比较、明确指令风险/事实冲突、关键事实覆盖差、风险分级有限恢复），封一份计划，离线角色盲运行36世界。若有独立可审>0变化，按本决议一次条件实跑36，无新审常规准备。收益：最快拿到安全-回答覆盖折中证据；风险：恢复可能使Poison漏报；可逆：新G3与旧资产隔离。
B `NOT_SELECTED`：等待完备来源Registry和HumanGold后才开始任何方法实现；公平性更强但重复停滞。
C `FORBIDDEN`：从旧逐格答案/Gold挑有利规则、简单放回全部B2删除项、无预算/外传权限即发送、借用旧Owner12费用豁免。

## 9. Recommended implementation
v0.2应基于**生产时确能观察到**的query/原chunk文本/TopK顺序/B2弱风险输出，提取多种中文写法的主题、属性、数字/比例、时间版次、条件、否定例外/指令特征；对未知标UNKNOWN。将**明确注入指令/越权指令/冲突+适用范围不清**维持隔离；可独立审计的低风险候选则根据当前可信保留上下文中确实缺失的查询要点，**受限最多1片段/世界**作探索恢复（该上限是先验而非按D1标签调整），并公开对应风险状态`RISK_ACCEPTED_NOT_PROVEN_TRUSTED`。不存在充分的生产侧元数据时不得自称来源可靠；不能无风险证据却伪称支持。可在证据充分时主动保留B2之外更多安全上下文，不强求只对先前失败例子产生差异。**算法不以角色、模型历史结果或世界ID编码作为判断信息**。
建议使用先验明确规则/确定性优先级，不做多套阈值搜索；测试应使用与D1文本不同的公开构造或抽象合成中文表述检查适配，而不以D1的答错案例逐条定制。

## 10. Rationale and confidence
可执行改造方向高置信；从过去0/36断言v0.2必然有非零改变或防御改善均无依据。允许新G3但只在有实质context diff、冻结和合规门通过后执行，禁止以无变化构造虚假G3胜利。首轮只是`D1_DEV_EXPLORATORY`，不宣称形式安全/已发布论文结果。

## 11. Explicit Owner approvals and execution contract

**I. v0.2方法代码与离线研究（立即执行）**
- 原分支增量新增 `vesa_guard_v02.py` /新adapter/小测试，不修改`vesa_guard_v01.py`及原G0/G1/G2、已封存输入和预算。
- 输入为36角色盲`PACKETS_PRIVATE.json` /原P2 TopK/ `B2_RESULTS_PRIVATE.json`的生产可用子集：`query`、TopK片段原文、rank、来源公开可见但未经认证的声明（仅作弱提示）、B2保留状态。禁止读取原世界角色、worldID语义、候选签署链、AI参考/Gold、前108逐格模型回复、任何Evaluator输出；允许引用全局聚合已知基线诊断作为科研动机，但不可通过world标签训练/配规则。
- 实现三层可消融机制：①中文广覆盖事实scope识别（支持非整段匹配、多事实句、日期/版本/条件/例外）；②指令/越权风险、显式同范围冲突、未知冲突与独立支持分级，重复片段不计独立证据；③基于原保留事实覆盖缺口的**最多每世界1条**`CAUTIOUS_RESCUE`，且必须有可核事实相关性、版本时间未明显不适用、无明显注入/同范围矛盾，不允许只凭风险“没检出”恢复。若候选多，按事前固定规则（如原rank先后+确定性ID）处理；避免将自称权威当真伪签名。
- 不要求上游来源签章才能进入**低风险的试探恢复**，但无签章则`PROVENANCE_UNVERIFIED`、不能升级`TRUSTED`；将恢复决策记录为风险接受与理由，不得在论文中称形式净化。覆盖未证/有争议/显式注入则不恢复。
- 先用独立构造样例单测≥覆盖关键中文自然表达与数值/时间/否定/例外，再对原36世界执行**仅一套v0.2预注册规则**，生成只读私有完整`G3_V02_GRID`、差异和安全风险记录及SHA。若36格都等同G2，实跑0并提交`NO_MEANINGFUL_DIFF`；不能无穷调正则/阈值追求样本命中。若产生>0格变化则封源码和全部36请求，再独立离线安全审计确认非污染角色标签驱动、原TopK子集引用合法及未明知风险强制恢复。

**II. 实跑（只有全部必需门PASS；无需再次单独Owner一般放行）**
- 与原Owner13不同，Owner14**明确重新授权**一次新36格G3-v0.2本机北京百炼Qwen真实生成，原Owner13 v0.1已结束且不能“续跑”；该许可不等于默认账户资金/法律权限PASS。
- 必须有最终算法源码commit+规则SHA+36 grid/request hash+Owner14 Git原件hash+独立QA+合法出站内容的本地机器审计+有效账户余额/全线累计USD资金与本批保守预留（25/28/30保持）；旧Owner12单次预算豁免不得沿用。若资金必要数值不存在/有禁止外传数据，则STOP并**仅报告最小精确阻断**，不要又造5个准备包。
- 凭原36世界顺序G3各1次，首3格工程通过继续33，零额外API/探测/模型Judge/retry、serial=1、HTTPS官方北京Workspace、同一model/system/V2 wire参数。`usage.prompt_tokens>4096`、usage缺失、completion超候选266、HTTP/schema/费用/凭证/输出seal/必要隐私问题即停后续，保留实际付费责任及全部36槽状态。原Owner12后置Token风险接受适用相同固定阈值，但本批次新授权须独立费用封存。
- 旧G0/G1/G2真实108条仅作冻结对照，绝不重发；G3输出封存后独立评价才读取D1 role与暂定reference，统计12事实组×3世界配对、Poison候选重新进入数量、Clean误删、HN留存、ABSTAIN与答案覆盖、Token/延迟/估算费。**正式ASR、AnswerAccuracy、HumanGold、C3保持未测**。

**III. 并行的12题Human Gold独立工作**
- 可从既有未署名12题/38事实原子/16独立来源材料**只做分发与独立人工审阅的组织**；Agent不得代替人签署事实Gold、不得替独立审阅者做裁决，也不得向算法worker提供标注、attack targets或评价回答。若组织独立审阅须遵守既有许可/保密/审阅者盲化，并与v0.2本地算法运行在物理文件和权限级隔离。无需等人类裁决才开始v0.2开发或DevPilot，但最终正式指标必须等待。

## 12. STOP / archival / next gate
终态唯一：`VESA_V02_G3_36_COMPLETED`、`VESA_V02_G3_PARTIAL_STOPPED`、`VESA_V02_NO_MEANINGFUL_DIFF`、`VESA_V02_G3_GATE_BLOCKED`。只一份易审结果报告与脱敏hash index：`docs/paper1/dual_machine/chinese5060/vesa_guard_v02/VESA_V02_OWNER14_RESULT.md`和`VESA_V02_G3_EVIDENCE_INDEX.json`；私有G3原文、请求、证据和任何人审材料只在D/E受控目录，Git绝不上传，记录算法源commit/rule SHA/36 plan与运行SHA、对G2具体上下文变化数和角色揭盲后的风险方向、真实API调用0..36及实际usage/cost/latency。流程禁止自我复审第二轮v0.2或扩大至D2/D3/5090；不完成正式论文claim。仅在5060原研究分支合法git push，核remote HEAD/clean/0:0后STOP。工作成果优先于文书，治理登记仅必要差异与不可变历史索引。
