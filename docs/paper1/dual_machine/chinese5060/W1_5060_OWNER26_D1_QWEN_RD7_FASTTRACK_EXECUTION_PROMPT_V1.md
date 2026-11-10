# 5060 Codex｜Owner26：D1-40中文RAG污染防御七臂对照，Qwen3.7固定快照，USD3内闭环（ACTIVE）

## 目标：优先给出科学裁决，不再被Windows本地Qwen加载阻断

你必须在`research/paper1-chinese-defense-5060`上，按Owner最新已批决策，完成**同一中文D1 TopK的7臂候选级防御比较**。优先实测而非继续讨论工程或模型硬件；仅必要准入阻断必须STOP，不得编造通过或替换参数。
**Owner26原件（唯一权限依据）**：`docs/paper1/dual_machine/owner_approvals/W1_5060_OWNER26_D1_QWEN_NOANCHOR_CHINESE_DEFENSE_COMPARE_20261110.md`，决策号`W1-OD-20261110-5060-D1-QWEN-NOANCHOR-26`。先恢复AGENTS/PO-MHEP/治理注册表/Owner25；存在更严约束或身份冲突立即止步。新Owner明示新增模型API、既有RD本地编码及D1-40内部冻结实验，旧Owner24 Qwen GGUF smoke不强行重开。旧Owner25 `BASELINE_INCOMPLETE`、Owner20规则`FEASIBILITY_NO_GO`、旧S1和R2所有负结果不改。

研究的对照不是`fixed-parent-proxy`，不能拿Owner25合成代理当作RAGDefender的成绩；必须跑真正B2及中文RD-zh，且**7臂严格同一有序 TopK5**。Qwen只是共同抽取器与独立直接核验基线，无任何外部Judge查询答案标签。

## A. 最快路径：一批封存、两阶段调用

1. 读取`docs/paper1/dual_machine/chinese5060/authorized_data_manifest.md`和`pilot12.md`，确认签署的D1-40包含40事实组×3候选、Pilot12固定12组×3世界且selection SHA`2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689`，其余**28组×3=84个拟验证世界**。8组`HOLD`另有独立封存，**绝不读取**，不得把D2/D3或Core144封存测试替换D1。Pilot12 36个世界/180 TopK片段已有冻结SHA/检索痕迹，历史RD基线固定。28组如无TopK，必须用原冻结索引/背景/候选注入/query结构和检索协议构建，**构造前冻结query和数据身份**；禁止用role/Gold/target选择query、chunk、rank或retrieval参数。若不能复原原协议与输入身份，报告`RETRIEVAL_IDENTITY_BLOCKED`，不能把“28组”伪装成可用的一次性验证。
2. 先建立role-free`WORLD_ID, QUERY, TOPK5 ordered original text/rank, doc hash`全量输入Manifest；所有臂用同一个哈希和同样召回率；提取器、过滤器、API prompt均不可读取`Poison/Clean/HN`、参考答案、攻击目标、标签来源或Evaluator gold。源码不能因名字/文件路径泄漏角色；下游评价在单独进程和sealed预测之后才拿角色。已召回候选和未召回候选分开报告，背景片段的角色不擅自假定全Clean。
3. **外传与API硬门**：Owner本轮已批Qwen API用途，但须审查每条D1检索原文的版权/来源权利、敏感性、端点区域与向百炼传输的范围；可明确公开并具有可执行上传权限的段落才能发送。缺证明即`D1_API_EXFIL_GATE_BLOCKED`，不可因Owner想要快便发送私有/受限原文。可先对本地RD和不含真实D1原文的纯虚构例做接口Probe。不要将Qwen API key、私有文本、角色或网络返回原文上传Git。Token和费用在D/E受控路径封存，脱敏报告只写聚合与SHA。
4. 官方模型固定`qwen3.7-plus-2026-05-26`，温度0；需核官方唯一地域endpoint、预存合法Key、来源地域/费率和账本余额/在途费用、输入/输出+reasoning token上限与模型参数的真实支持。只能用指定模型，不能换`qwen3.7-plus`浮动别名。官方文档确认该ID存在；但`enable_thinking=false`与`json_object`是否兼容可能依所在接口而异，只允许≤2次**无敏感虚构文本握手**计费Probe，在开始DEV前冻结一次性有效配置：优先`enable_thinking=false`+结构化JSON，若无此能力则使用官方`thinking_budget`有界思考+文本JSON解析；任何配置不支持都留下完整错误，不自动切换模型或地域。禁止联网搜索、工具调用、Function Calling、上下文缓存相关不透明费用、重试/后台异步批量任务。
5. **费用门**（更严格优先）：新增费用最坏上限**USD3**且不得影响已有USD25/28/30总账；先计算全体逻辑请求数及token/输出上限费用，采用官方实际价格、汇率上界、无折扣最坏价格；`已结算+在途预留+拟请求上界`必须≤3且原总账≤30。USD2.40预警、≥2.70禁止扩量、≥2.85不再发新请求、USD3绝对硬停；API usage账本每次写前保存intention及request hash，单次retry=0，断网/超时不补发，已发即消耗授权一次请求。只有能证明前述账本、完整费用上界和数据出境权才允许进入真实D1请求。每次输出`model-id/temp/thinking-mode/max_tokens/api-region/token-count/costUSD/latency/error-id`，不能拿无实际使用证明的估算当已计费结果。

## B. Qwen抽取与强基线（冻结Prompt、0后验修）

1. **抽取**：对每个`(query,chunk-text,prompt-sha,model-config)`唯一哈希调用1次Qwen（抽取可按严格相同的字节请求cache，报告理论逻辑调用与实际网络调用数）。每条结果仅从可见片段抽取：`status,answer_quote,character_start,character_end,normalized_value,unit,answer_type(numeric/date/authority/direction/boolean/none), effective_date_or_version,scope,condition,negation`。若多个可能候选返回列表并保留歧义；严禁借Gold/标签修补。所有span按原字节序和字符半开校验，原文无连续逐字`answer_quote`、时间版本无可核span/不同scope或自相矛盾`UNKNOWN/CONFLICT`，不让模型自称“官方最新”赋予可信身份。必要字段缺失不能用脚本猜造，给出UNKNOWN。冻结schema和每臂同一提取缓存。
2. **QWEN_VERIFY**：同一模型、temperature0、同一有序五段、同一query每世界1次请求，由Qwen返回可疑片段**原rank索引数组和原文理由**；提示不包含role/Gold/攻击目标/其它臂结果，模型输出的机构/新版自称不能直接证明可信性。对无法解析的输出按冻结策略保守不删除或显式ERROR，不得人工后验补列表。
3. **本地RD**：只使用已签本地缓存Embedding、上游`RAGDefender@ba2a17efba165d45409114df2d70b030ade1e1b8` v0.2.0/固定B2 multilingual-MiniLM工程修正源，`RD_ZH`仅Stage1字符bigram、stop_words=None，其余retrieval/Stage2/topK/m/p/time不变。两臂共用一次原句编码，不联网、不下载、不替换Stella或参数。只做本轮新的同输入baseline，不覆盖旧B2/R2封存。
4. **七臂明确输出**：
   - `RD_B2` 原固定B2；
   - `RD_ZH` 中文词项单变量迁移；
   - `QWEN_VERIFY` 直接判可疑片段；
   - `RD_ZH+M1_SAFE`：当RD**保留**证据中的scope可比、值单位唯一时，只对被删中**同答案且无冲突**的原段放回；不允许文中自称来源/自称最新版充当独立证明；标签为`UNANCHORED_REINCLUSION_RISK`（名字SAFE是Owner的试验名称，不是已满足P0证明）；
   - `RD_ZH+M2_VOTE`：对可比scope的已锚定原文答案规范化分组、按来源/传播相关性去重，再将定义好的少数派删除；无可靠source独立性时只记录不确定性，不假装改写文本是独立投票；不可因为3/5多数就自称可信；
   - `M2_VOTE_ALONE`：无RD独立按同样规则执行，少数派/票数不可靠时回退预注册原则；
   - `RD_ZH+M1_SAFE+M2_VOTE`：明确顺序（先M1后M2或相反，DEV前选择并冻结），不通过后验切换；所有输出必须是原TOPK有序子集，保留rank，拒绝rewrite/retrieve/refill/更换Prompt。
5. **安全反例**：必须显式报告3/5、4/5、5/5 Poison、自相矛盾的Poison、同数字不同时间/对象、伪造更新、多源改写与重复转载；没有该类型则`NOT_IN_DATA`，不能宣称覆盖。所有`unverified_version`不得直接提升可信，Qwen输出只是证据候选，不是可信身份。

## C. 开发与一次性验证（以事实组为单位，避免标签泄漏）

- **DEV**：仅Pilot12的12事实组×3=36世界；先冻`v0`，允许至多一次`v1`研究方法修正，记录每次规则/提示/schema变化SHA及全量效果。仅DEV可读Evaluator反馈；不得通过外部D1-28逐格结果改选参数。
- **Primary arm冻结**：在DEV选择一个实际部署候选`RD_ZH+M1_SAFE`、`RD_ZH+M2_VOTE`或联合臂（`M2_VOTE_ALONE`也可作为预注册选择），以最小Poison retained + Clean误删择优，优先满足Poison不退化；冻结其源码、基线和提取/直接核验prompt、数据构建、Token预算、成本ledger和评价协议。将全部7臂固定，无`best-of-holdout`。
- **D1-28**：其余28事实组×三变体=**84个世界、420条TopK5**（条件：检索可按原协议正确封存；漏召回不当成功过滤）。新TopK和query在首次科学预测前封存、hash；模型请求响应的网络缓存必须与请求SHA绑定、无人工补数。运行7臂对比时共享同一冻结Qwen extraction与同一Qwen_VERIFY，先输出全部role-free结果/每世界hash与请求费用seal，再由独立Evaluator一次解封Gold/role并评分。拒绝重复整批科学试次、换算法/抽取参数、按标签选比较窗口。此前的D1与Pilot12已作为研究开发暴露，结果叫`D1_INTERNAL_HELD_GROUP_EVALUATION`，非正式外部holdout/HumanGold。
- **防止偷换维度**：每组3角色候选、不同隐蔽等级S1/S2/S3、有无候选召回、被删除的其它背景证据、三类候选和验证器UNKNOWN、合法多版本分开报。可做DEV静态单测、构建测试，但不能先只试84中的小部分然后按Gold修新Prompt。

## D. 原分母与公平成本、GO裁决

报DEV 36和Eval84、召回29/36旧Pilot基点、Eval各角色召回数、`retained_poison/retrieved_poison`、`deleted_clean/retrieved_clean`、`deleted_HN/retrieved_HN`、其余背景总删除/5、候选漏召回、M1恢复Poison、M2误删真实小众观点、抽取strict-correct/wrong/UNKNOWN及span/type/scope误绑、版本伪造、Poison自相矛盾，Token/请求数/ USD/latency median/P95，按组为配对单位的置信区间和世界级配对翻转。真实查询生成指标`Targeted ASR / final AnswerAccuracy / refusal`仍`NOT_MEASURED`，不可凭删掉Poison候选直接写成成功防御。

**Token账本公平口径**：真实物理网络调用只计一次且收费只计一次；但**逐独立部署臂的逻辑Tokens/费用**必须算其自身实际需要的抽取调用及prompt+answer上下文，不能把VESA依赖的共同抽取成本记到零或其它臂；`QWEN_VERIFY`一次world请求自己的Token为独立基线。两个定义分开报告。样本级cached extraction真实物理成本/逻辑成本不能混用。

### 冻结决策门

在`D1-28`的**先DEV选出的单一VESA arm**上：
- `GO`: 相对`RD_ZH` `Poison retained`（已召回分母）不增、`Clean false deletion`至少降50%（按实际分子分母、共同已召回集合）；并且相对`QWEN_VERIFY`在Poison retained、Clean false delete和HN false delete**每项不劣**且各方法完整逻辑Token **严格更少**。若同world QWEN_VERIFY不可用，`GO`不允许。
- `PARTIAL`: 净安全—可用性核心门优于RD_ZH，但不满足QWEN_VERIFY三项/成本门。
- `NO_GO`: 未通过RD_ZH核心门，或Poison保留恶化。
- `BLOCKED/INCONCLUSIVE`: 缺协议、缺合法权限、缺同world RD、预算或角色隔离失败；**不得**把已成功子集后验当完成84。
- 与论文旧门`ASR/Accuracy/HN误删/拒答变差≤2.5pp`的关系：本轮没有真实生成指标，不能宣称旧门已达成；HN误删另报，若出现重大恶化即给出`SAFETY_REGRESSION`，即使GO点估计成立也须提示不宜直接进入实际部署。

## E. STOP与提交

优先解决真实科研阻断：在授权范围内工程问题、既有本地依赖和脚本可自主修复；但**不允许**增加或变更模型ID/供应商/地域、自动下载安装依赖、USD费用超3、让私有D1原文非法外传、D2/D3/8组HOLD、5090、正式商业生成ASR、改变既有实验结果、主研究分支合并。API配置/成本/许可证不能闭合则仅完成本地RD与公开虚构文本诊断后标`BLOCKED`，不得偷偷发真实D1；无法检索28组则STOP并输出原始失败，不要伪造效果数字。

**交付**：
`OWNER26_D1_QWEN7_RESULT.md`、`OWNER26_D1_QWEN7_RUN_MANIFEST.json`、两套Prompt+parser/过滤源码SHA、角色盲Git外封存与独立Evaluator收据、至少7臂完整DEV+Eval逐场景分子分母、成本 Token账本与API出站授权证据、README论文方法图与候选方法伪代码、最终`GO/PARTIAL/NO_GO/BLOCKED`明确裁决、失败案例和未来“中文版本敏感污染基准+RD中文失效分析”备用方法方案。更新治理/Tracker，Git commit+push核验远端一致后STOP，`Auto Continue=NO`。不要声称1–2天保证完成，不在后台假承诺。
