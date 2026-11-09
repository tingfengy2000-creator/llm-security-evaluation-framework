# 5060 Codex｜Owner19：S1-B 可行性数据准备/封存/预注册（DATA_PREP_ONLY）

你现在受 Owner19 指示执行 `S1B_FEASIBILITY_DATA_PREPARATION_ONLY`，不是运行抽取器评测。用户明确希望前期用D1、公开数据或LLM生成数据判断可行性，**正式阶段才安排人工标注**。不得扩大为S2–S5或新模型运行。

## 0. 权威与入口

唯一仓库 `tingfengy2000-creator/llm-security-evaluation-framework`、唯一分支 `research/paper1-chinese-defense-5060`。执行前Git fetch/preflight，读取`AGENTS.md`、PO-MHEP、最新`Current Work State`、Owner Decision Register、R1/R2、Owner18结果。
唯一新授权 `W1-OD-20261109-5060-S1B-FEAS-DATA-19`：
`docs/paper1/dual_machine/owner_approvals/W1_5060_S1B_FEASIBILITY_DATA_PREP_AUTHORIZATION_20261109.md`。
既有Rule-V1/Rule-V2源码保持冻结，Rule-V2开发提交 `da3cbd9f16ea70ae3ba0ef2aa2408227ecfc0b4f`，Owner18评审实验HEAD `33d67cfbdbc93b90bdcfa27241be6539f28c3f14`；不调整规则、不优化参数、不运行新数据预测。

## 1. 数据源优先级及分层

- 第一层：`D1_DEV_EXPOSED`，允许只读回归/已有结果整理，不算独立测试，不允许改索引、重检索、重标角色或将D1凑进新100。
- 第二层：`AGENT_GENERATED_PROVISIONAL_FEASIBILITY`：建议主100语义事实和20额外配对，使用当前Codex的写作能力构造**全新**本地虚构中文可见证据，不需要额外模型/API调用。不是人审，不得写Human Gold。如果生成与方法仍属同Agent，必须标 `NOT_INDEPENDENT_AUTHOR`，即便文件和进程隔离也不能声称独立人审/完全独立盲测。
- 第三层：`PUBLIC_DATASET_PROXY`：可选来自CMRC2018官方HFL或作者来源的公开问答+answer_start，CC BY-SA 4.0且须署名，作中文原文span/领域外补充压力测试。只能在数据许可、固定源版/文件大小/hash、来源可信和D/E上限核证后获取批准的最小子集；压缩≤50MiB、解压≤200MiB，0新增pip依赖；任一不能闭合则跳过，不阻断合成主集。CMRC原文问答没有VESA的版本、生效期、可信source proof，不得为其擅自发明真实Gold。不得抓其它未获白名单授权的公开数据。
- D2/D3、旧108隐藏标注或未来S3留出绝对不能读。旧73可经现有授权用于只读去重索引，但不当作新测试。不要把同义改写当独立语义事实。

## 2. 主数据结构与问题覆盖

准备≥100个不同语义情境（建议**70可回答、30应拒识**），另20个同一事实自然化/显式配对视图，主分母100、实际视图数120。至少4个虚构主题域和10个不同虚构source families，避免复制旧73模板。预先定义各类定额与生成种子/规则，不要按抽取器胜败去重选。
必须包含：数字/百分比/金额/日期/单位、当前与旧版及生效范围冲突、机构/地域/群体跨scope、否定/例外、同句重值与不同合法证据span、两处相同数值但scope不等价、多文段事实、修订“传闻/自称权威”而没有独立证明、没有对应值、网页导航夹杂正文、合法重复来源/保守UNKNOWN。
合成样本以`source-truth table -> evidence document -> question -> oracle answer/status/accepted supporting span(s)`方式构造：先定义源事实及其范围/版本/条件、再写文本、问法及oracle；真值只能由该构造表和已验证的原文合法跨度推出，不能引用模型常识或伪造真实法规/官方证明。对每个span必须验证Unicode字符半开区间、UTF-8字节半开区间与证据原文字节对应；多span等价与候选聚类评判标准必须在模型预测前冻结。跨scope文本出现相同值，单独只标相同数字span不能视为合法来源。
数据质量检查：ID唯一、source family去重、内容重复/近重复（D1/旧73只能在已有隔离权限下检查）、答题主/拒识数量、事实/改写配对映射、文本与anchor hash一致、无Gold泄露到推理输入、manifest与seal不可变。AI provisional标签需要依赖规则原子与原文字段自动自证，不得把“模型认为正确”当真实性证明。

## 3. 隔离的私有文件与公开证据

输入、truth ledger、Gold/accepted spans、配对组、source licensing、generation plan 和评分协议分开放D/E白名单；算法新预测运行器**这次不得启动**。Git只提交 schema、generator/validator代码、无私有案例原文的脱敏aggregate、SHA256、PO-MHEP/Tracker治理、不含Gold的下一批审批卡。不能上传D1/D2/D3私有文本、公开集大量原文、合成未公开测试题正文/答案、密钥。
建议 `Run ID = W1-5060-S1B-FEAS-DATA-PREP-20261109-01`，标记`DATA_PREP_NOT_SCIENTIFIC_TRIAL`。明确数据来源层、真实注释级别、每层语义案例数/视图数与各哈希，暂定`HUMAN_GOLD=0`。

## 4. 预注册评价计划（不要运行）

未来待Owner19后的专门 ONE_SHOT approval 才可比较冻结Rule-V1和Rule-V2：同query与evidence、同schema与span/verifier、安全约束、完整主100个不同事实分母，20配对另计；value hit/answerable≥90%、wrong/decided≤2%、coverage/abstain、wrong/total、scope/span严格正确、应拒识误答、未证新版与跨scope误答、自然化与显式差异、Wilson 95% CI、程序失败及来源分层。必须预先确定多合法span的`accepted_span_sets`等价规则，并禁止改旧S1任何Gold与旧唯一span错例。
新合成集通过规则不能证明真实可信来源核验，也不能自动推断最终RAG ASR；保留`UNVERIFIED_TEXT_ONLY`与原P0。未证新版/跨scope误答零新增为建议guard，不自行作为已批硬门。
**绝不运行 Rule-V1/Rule-V2 在新样本上的预测、评分、揭盲或调参**；只有等Owner看到完整无Gold Manifest后另行批准一次盲评。
将来若用户要保留同一批验证集作本地UIE/Qwen公平对照，则在四臂全部准备齐之前不能将其当未暴露集多次评估。此次选择的规则先行A将消耗其“模型未见”资格，后续模型公平比较需另外封存新数据。

## 5. 网络/资源/许可边界

允许当前Codex会话自身生成合成文本；**不允许另外调用商业API、免费在线LLM、本地未获批模型或下载任何权重/安装依赖**。有限CMRC2018数据获取须严格满足Owner19源版本/许可/大小白名单；若不满足则仅只读元数据并走合成主集。不要联网抓站点或训练数据、没有来源的正式法规正文。磁盘/缓存/TEMP全部D/E且预留安全空间；无新C盘可控数据。5090 Meta Llama2还在访问审批，绝对不能给5090 Claim任务。

## 6. 停止/交付

任何Gold/输入泄露、无法做稳定可复核且非模板重复的新语义主100、需新增模型调用/下载、公开资产未经许可、触碰D2/D3/5090、需要修改冻结Rule-V1/V2、不能验证span或公开许可、越过单次评价门立即STOP记录十二字段决策卡。
交付：Context Recovery Report、数据来源许可表、100主案例/20从属分层和去重质量、source/Gold seal与哈希、评分协议/accepted spans、私有归档位置与脱敏Manifest、测试/安全检查、下载/调用/费用实际记录、Git commit+push/远端SHA、给Owner审批后续一次规则盲评的run manifest草案。
收口：`FEAS_DATA_READY_OR_FAIL / PROVISIONAL_GOLD / EVALUATION_NOT_RUN / S2_S5_LOCKED / AUTO_CONTINUE=NO`，提交之后停止，不暗中开始测试。
